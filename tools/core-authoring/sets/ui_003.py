"""TypeIcon Core: ui (batch ui_003): device settings, design-tool actions, table and editor patterns.

Same keyshapes as ui_001: phone rect(5, 2, 14, 20), frame rect(3, 3, 18, 18), window rect(3, 4, 18, 16).
Dividers and marks inside a frame are `detail`s / `Part("dot")` (knocked out in Filled).
Every Filled design is built from `fn(FILL)` (Line geometry) unless a drawing passes `filled=`.
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, I, P, ST, U, Part, Style, arc, circle, detail, dot, ellipse, filled_region, fmt, icon, line, path_to_d, poly,
    rect, regular, seg, shell, solid,
)
from geometry import rect_d  # noqa: F401

CAT = "ui"
FILL = Style("filled", "butt", "miter", R=2.0, r=0.0)


def isF(S) -> bool:
    return S.name == "filled"


def isL(S) -> bool:
    return S.name != "rounded"


def ui(name, description, tags, aliases=(), filled=None):
    def deco(fn):
        fl = filled if filled is not None else (lambda: filled_region(fn(FILL)))
        return icon(name, CAT, description, tags=tags, aliases=aliases, filled=fl)(fn)
    return deco


def pip(S, x, y, r=1.75, grow=0.5):
    if isF(S):
        return Part("dot", circle(x, y, r + grow))
    if S.name == "line":
        s = r * 0.9
        return Part("dot", rect(x - s, y - s, 2 * s, 2 * s))
    return Part("dot", circle(x, y, r))


def blk(S, x, y, w, h, k=1.0):
    return Part("dot", rect(x, y, w, h, 0 if isL(S) else min(k, w / 2, h / 2)))


def frame(S):
    return shell(rect(3, 3, 18, 18, S.R))


def win(S, y0=4.0, h=16.0):
    return shell(rect(3, y0, 18, h, S.R))


def phone(S):
    return shell(rect(5, 2, 14, 20, S.R * 0.75))


def tile(S, x, y, w, h):
    return shell(rect(x, y, w, h, S.R * 0.5))


def pt(cx, cy, r, deg):
    a = math.radians(deg)
    return (cx + r * math.cos(a), cy + r * math.sin(a))


def arrow_head(S, tip, deg, size=3.0, kind=line):
    a = math.radians(deg)
    pts = []
    for s in (135, -135):
        b = a + math.radians(s)
        pts.append((tip[0] + size * math.cos(b), tip[1] + size * math.sin(b)))
    return kind(poly([pts[0], tip, pts[1]], r=S.r))


def chev(S, cx, cy, w=3.0, h=None, deg=90, kind=line):
    h = w if h is None else h
    a = math.radians(deg)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    tip = (cx + ux * h / 2, cy + uy * h / 2)
    b = (cx - ux * h / 2, cy - uy * h / 2)
    return kind(poly([(b[0] + nx * w, b[1] + ny * w), tip, (b[0] - nx * w, b[1] - ny * w)], r=S.r))


def star5(cx, cy, ro, ri):
    pts = []
    for i in range(10):
        r = ro if i % 2 == 0 else ri
        a = math.radians(-90 + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def clip(d_region, d_by):
    """Intersection of two d-strings (filled regions) as a d-string."""
    return path_to_d(I(P(d_region), P(d_by)))


def stroke_d(d, w=2.0, cap="butt", join="miter"):
    return ST(d, w, cap, join, 4.0)


def dashed_rect(S, x, y, w, h, kind=line, dash=4.0):
    """Rectangle drawn as corner Ls plus one centred dash per long side."""
    trim = 0 if isL(S) else 0.75
    arm_w = (w - dash) / 2 - 3.5 / 2 if w > 10 else w / 2 - 1.75
    arm_h = (h - dash) / 2 - 3.5 / 2 if h > 10 else h / 2 - 1.75
    x1, y1 = x + w, y + h
    parts = []
    for cx, cy, sx, sy in ((x, y, 1, 1), (x1, y, -1, 1), (x1, y1, -1, -1), (x, y1, 1, -1)):
        parts.append(kind(poly([(cx, cy + sy * (arm_h - trim)), (cx, cy), (cx + sx * (arm_w - trim), cy)], r=S.r)))
    if w > 10:
        mx = x + w / 2
        for yy in (y, y1):
            parts.append(kind(seg(mx - dash / 2 + trim, yy, mx + dash / 2 - trim, yy)))
    if h > 10:
        my = y + h / 2
        for xx in (x, x1):
            parts.append(kind(seg(xx, my - dash / 2 + trim, xx, my + dash / 2 - trim)))
    return parts


# =========================================================================== device settings

@ui("screen-time", "Phone with a small hourglass on its screen.",
    ["screen time", "usage", "digital wellbeing", "app timer", "phone usage", "hourglass", "limit"])
def _(S):
    return [phone(S), detail(poly([(9, 7), (15, 7), (9, 17), (15, 17)], closed=True))]


@ui("restart-device", "Power symbol whose circle is a circular arrow looping back toward the stem.",
    ["restart", "reboot", "power cycle", "reset device", "turn off and on", "power", "shutdown"])
def _(S):
    return [line(arc(12, 13.5, 8, -60, 240)), arrow_head(S, pt(12, 13.5, 8, 240), 330, 3.2),
            line(seg(12, 3, 12, 12))]


@ui("system-update", "Phone with a circular arrow on its screen and a dot at its centre.",
    ["system update", "software update", "os update", "firmware", "upgrade", "install update", "refresh"])
def _(S):
    return [phone(S), detail(arc(12, 12, 3.6, 30, 330)), arrow_head(S, pt(12, 12, 3.6, 330), 60, 2.2, kind=detail)]


@ui("data-saver", "Circle open at the top with a small plus sign in its centre.",
    ["data saver", "data saving", "reduce data", "low data", "mobile data", "cellular data", "bandwidth"])
def _(S):
    return [line(arc(12, 12, 9, -65, 245)), line(seg(12, 9, 12, 15)), line(seg(9, 12, 15, 12))]


@ui("data-roaming", "Rising signal bars with a capital R at their upper left.",
    ["data roaming", "roaming", "international", "abroad", "cellular", "signal", "travel data"])
def _(S):
    bars = [blk(S, 10, 17, 3, 4, 0.8), blk(S, 14.5, 13, 3, 8, 0.8), blk(S, 19, 9, 3, 12, 0.8)]
    return [line(poly([(4, 13), (4, 3), (8, 3), (10, 5), (10, 7), (8, 9), (4, 9)], r=S.r)),
            line(seg(8, 9, 11, 13))] + [Part("solid", b.d) for b in bars]


@ui("haptics", "Fingertip pressing a surface with short curved vibration lines on both sides.",
    ["haptic feedback", "vibration", "vibrate", "touch feedback", "tap feedback", "buzz", "touch"])
def _(S):
    return [shell(rect(9.5, 2.5, 5, 11.5, S.R * 0.6)), line(seg(3, 19, 21, 19)),
            line(arc(12, 11, 7, 150, 210)), line(arc(12, 11, 7, -30, 30))]


@ui("developer-options", "Phone with a pair of curly braces on its screen.",
    ["developer options", "dev mode", "debug", "usb debugging", "code", "programmer", "braces"])
def _(S):
    l = "M11 7.5H10.25A1.5 1.5 0 0 0 8.75 9V10.5A1.5 1.5 0 0 1 7.5 12A1.5 1.5 0 0 1 8.75 13.5V15A1.5 1.5 0 0 0 10.25 16.5H11"
    r = "M13 7.5H13.75A1.5 1.5 0 0 1 15.25 9V10.5A1.5 1.5 0 0 0 16.5 12A1.5 1.5 0 0 0 15.25 13.5V15A1.5 1.5 0 0 1 13.75 16.5H13"
    return [phone(S), detail(l), detail(r)]


def _drop_d(S=None):
    if S is not None and S.name == "rounded":
        return "M12 3.8C11.2 4.5 5.5 10 5.5 14.5A6.5 6.5 0 0 0 18.5 14.5C18.5 10 12.8 4.5 12 3.8Z"
    return "M12 2.8C12 2.8 5.5 9.5 5.5 14.5A6.5 6.5 0 0 0 18.5 14.5C18.5 9.5 12 2.8 12 2.8Z"


def _invert_filled():
    d = _drop_d()
    outer = U(P(d), stroke_d(d, 2.0))
    hole = I(D(P(d), stroke_d(d, 3.6)), P(rect_d(12, 0, 12, 24)))
    return D(outer, hole)


@ui("invert-colors", "Water drop split down the middle, the left half solid and the right half outlined.",
    ["invert colors", "invert colours", "negative", "reverse colors", "color inversion", "contrast", "drop"],
    filled=_invert_filled)
def _(S):
    d = _drop_d(S)
    left = clip(d, rect_d(0, 0, 12, 24))
    return [shell(d), Part("solid", left)]


@ui("grayscale-mode", "Circle split into a solid band, a dotted band and an empty band.",
    ["grayscale", "greyscale", "grayscale mode", "black and white", "monochrome", "no color", "bedtime mode"])
def _(S):
    c = circle(12, 12, 9)
    left = clip(c, rect_d(0, 0, 9, 24))
    out = [shell(c), Part("solid", left)]
    for y in (7.5, 12, 16.5):
        out.append(pip(S, 12.5, y, 1.5, 0.1))
    if isF(S):
        out.append(detail(seg(16, 4, 16, 20)))
    return out


@ui("storage-meter", "Database cylinder above a capsule bar that is mostly filled.",
    ["storage", "disk usage", "storage meter", "space used", "capacity", "memory usage", "quota"])
def _(S):
    cyl = "M7 5V10A5 2 0 0 0 17 10V5"
    out = [shell(ellipse(12, 5, 5, 2)), line(cyl),
           shell(rect(2, 15, 20, 6, 2 if isL(S) else 3))]
    if isF(S):
        out.append(Part("dot", rect(15, 16.5, 5, 3, 1.5)))
    else:
        out.append(Part("solid", rect(4, 17, 11, 2, 1)))
    return out


@ui("gaming-mode", "Landscape phone with a small game controller pad and two buttons on its screen.",
    ["gaming mode", "game mode", "game boost", "performance mode", "controller", "gamepad", "play"])
def _(S):
    return [shell(rect(2, 5, 20, 14, S.R * 0.9)), detail(seg(5.5, 12, 10.5, 12)), detail(seg(8, 9.5, 8, 14.5)),
            pip(S, 15.5, 13, 1.1, 0.2), pip(S, 18.5, 10.5, 1.1, 0.2)]


@ui("one-handed-mode", "Phone with its content pulled to the lower right and a thumb arc beside it.",
    ["one handed mode", "one-hand", "reachability", "shrink screen", "thumb", "reach", "small screen"])
def _(S):
    return [shell(rect(3, 3, 12, 18, S.R * 0.75)), detail(poly([(8, 21), (8, 11), (15, 11)])),
            line(arc(9, 14, 11, -35, 35))]


@ui("refresh-rate", "Monitor with a ball and three short motion lines trailing behind it.",
    ["refresh rate", "hz", "frame rate", "fps", "smooth display", "screen speed", "motion"])
def _(S):
    return [shell(rect(2, 3, 20, 14, S.R)), line(seg(9, 21, 15, 21)),
            detail(seg(5.5, 7, 9, 7)), detail(seg(5.5, 10, 11, 10)), detail(seg(5.5, 13, 9, 13)),
            Part("dot", circle(16, 10, 2.5))]


@ui("battery-health", "Horizontal battery outline with a small heart inside.",
    ["battery health", "battery condition", "battery care", "charge capacity", "battery life", "power", "wellbeing"])
def _(S):
    heart = "M11.5 15.2L8 11.7A2 2 0 0 1 11.5 9.4A2 2 0 0 1 15 11.7Z"
    return [shell(rect(2, 6, 18, 12, S.R * 0.6)), blk(S, 20, 9.5, 2, 5, 0.8), Part("dot", heart)]


@ui("usb-tethering", "Phone joined by a cable to a small globe.",
    ["usb tethering", "tethering", "share internet", "hotspot cable", "internet sharing", "connect phone", "usb"])
def _(S):
    return [shell(rect(2, 2, 8, 13, S.R * 0.5)), line(poly([(6, 15), (6, 18.5), (11.6, 18.5)], r=S.r)),
            shell(circle(16.5, 15.5, 5.5)), detail(seg(11, 15.5, 22, 15.5)), detail(seg(16.5, 10, 16.5, 21))]


@ui("kids-mode", "Phone whose screen shows a smiling face above a small star.",
    ["kids mode", "child mode", "parental controls", "children", "safe mode", "kid friendly", "family"])
def _(S):
    return [phone(S), Part("dot", circle(9.5, 7.5, 1.1)), Part("dot", circle(14.5, 7.5, 1.1)),
            detail(arc(12, 8.5, 3.5, 30, 150)),
            Part("dot", poly(star5(12, 16.5, 2.6, 1.2), closed=True, r=0 if isL(S) else 0.3))]


# =========================================================================== design-tool actions

@ui("shape-union", "Two overlapping squares merged into one combined outline.",
    ["union", "combine shapes", "merge shapes", "boolean add", "unite", "join shapes", "pathfinder"])
def _(S):
    return [shell(poly([(3, 3), (15, 3), (15, 9), (21, 9), (21, 21), (9, 21), (9, 15), (3, 15)], closed=True, r=S.r))]


@ui("shape-subtract", "Square with a corner cut away by a second square that is shown only as a dashed outline.",
    ["subtract", "boolean subtract", "minus front", "cut out", "difference", "knock out", "pathfinder"])
def _(S):
    return [shell(poly([(3, 3), (15, 3), (15, 9), (9, 9), (9, 15), (3, 15)], closed=True, r=S.r)),
            line(poly([(18, 9), (21, 9), (21, 12)], r=S.r)), line(poly([(21, 18), (21, 21), (18, 21)], r=S.r)),
            line(poly([(12, 21), (9, 21), (9, 18)], r=S.r))]


@ui("shape-intersect", "Two overlapping square outlines with only the overlapping area filled.",
    ["intersect", "boolean intersect", "overlap", "common area", "intersection", "shared area", "pathfinder"])
def _(S):
    return [line(rect(3, 3, 12, 12, S.R * 0.5)), line(rect(9, 9, 12, 12, S.R * 0.5)), solid(rect(9, 9, 6, 6))]


@ui("shape-exclude", "Two overlapping squares filled except for the area they share.",
    ["exclude", "exclude overlap", "boolean exclude", "xor", "subtract overlap", "difference", "pathfinder"])
def _(S):
    return [shell(poly([(3, 3), (16, 3), (16, 8), (8, 8), (8, 16), (3, 16)], closed=True, r=S.r)),
            shell(poly([(16, 8), (21, 8), (21, 21), (8, 21), (8, 16), (16, 16)], closed=True, r=S.r))]


@ui("group-objects", "Circle and square inside a dashed bounding box with handles at its corners.",
    ["group", "group objects", "group layers", "bundle", "bounding box", "selection box", "design tool"])
def _(S):
    out = [line(seg(8, 4, 16, 4)), line(seg(8, 20, 16, 20)), line(seg(4, 8, 4, 16)), line(seg(20, 8, 20, 16))]
    for x, y in ((3, 3), (21, 3), (3, 21), (21, 21)):
        out.append(blk(S, x - 1.75, y - 1.75, 3.5, 3.5, 0.8))
    out += [shell(circle(9.5, 9.5, 2.8)), shell(rect(12.5, 12.5, 5.5, 5.5, S.R * 0.3))]
    return out


@ui("ungroup-objects", "Circle and square pulled apart, each with its own small corner bracket.",
    ["ungroup", "ungroup objects", "separate", "split group", "release group", "break apart", "design tool"])
def _(S):
    return [line(poly([(2, 7), (2, 2), (7, 2)], r=S.r)), shell(circle(9, 9, 3.8)),
            shell(rect(13, 13, 6.5, 6.5, S.R * 0.4)), line(poly([(22, 17), (22, 22), (17, 22)], r=S.r))]


@ui("distribute-spacing", "Two bars between two edge guides with the same gap on every side.",
    ["distribute", "equal spacing", "even spacing", "space evenly", "distribute horizontally", "align", "gaps"])
def _(S):
    return [line(seg(3, 3, 3, 21)), line(seg(21, 3, 21, 21)), blk(S, 6.67, 6, 4, 12, 1), blk(S, 13.33, 8.5, 4, 7, 1)]


def _mountain(S):
    return clip(poly([(4, 20), (4, 15), (9, 9.5), (12, 13), (14.5, 10.5), (20, 16.5), (20, 20)], closed=True),
                circle(12, 12, 4.2))


@ui("clipping-mask", "Circle showing a mountain picture inside it, with the square it was cut from drawn dashed.",
    ["clipping mask", "clip", "mask", "crop to shape", "cutout", "image mask", "design tool"])
def _(S):
    return dashed_rect(S, 3, 3, 18, 18) + [shell(circle(12, 12, 5.2)), Part("dot", _mountain(S))]


@ui("flatten-layers", "Downward arrow pressing onto a single flat diamond.",
    ["flatten", "flatten layers", "merge layers", "merge down", "flatten image", "collapse layers", "rasterize"])
def _(S):
    return [line(seg(12, 2.5, 12, 9)), arrow_head(S, (12, 9), 90, 3.0),
            shell(poly([(12, 12.5), (21, 17.25), (12, 22), (3, 17.25)], closed=True, r=S.r * 0.6))]


_BA = circle(8.5, 9, 5.5)
_BB = circle(15.5, 9, 5.5)


def _blend_filled():
    body = U(P(_BA), P(_BB))
    lens = D(I(P(_BA), P(_BB)), U(stroke_d(_BA, 2.0), stroke_d(_BB, 2.0)))
    body = D(body, lens)
    crescent = D(P(_BB), P(_BA))
    for x0 in (13, 17.5):
        body = D(body, I(stroke_d(seg(x0, 15, x0 + 8, 7), 2.0), D(crescent, stroke_d(_BA, 2.0))))
    return U(body, ST("M12 19L15 21.5L18 19", 2.5, "butt", "miter", 4.0)) if False else \
        U(body, ST("M9 19L12 22L15 19", 2.5, "butt", "miter", 4.0))


@ui("blend-mode", "Two overlapping circles, the left one solid and the right one striped, with a down caret below.",
    ["blend mode", "blending", "layer blend", "overlay", "multiply", "mix", "opacity"], filled=_blend_filled)
def _(S):
    crescent_b = D(P(_BB), P(_BA))
    stripes = U(*[stroke_d(seg(x0, 15, x0 + 8, 7), 2.0) for x0 in (13, 17.5)])
    hatch = path_to_d(I(stripes, crescent_b))
    left = path_to_d(D(P(_BA), P(_BB)))
    return [shell(_BA), shell(_BB), Part("solid", left), Part("solid", hatch),
            chev(S, 12, 20, w=3, h=2.5, deg=90)]


@ui("drop-shadow", "Square outline with a solid shadow along its lower right side.",
    ["drop shadow", "shadow", "box shadow", "elevation", "depth", "effects", "text shadow"])
def _(S):
    shadow = path_to_d(D(P(rect(8, 8, 14, 14)), P(rect(2, 2, 15, 15))))
    return [line(rect(3, 3, 13, 13, S.R * 0.5)), solid(shadow)]


@ui("inner-shadow", "Square outline with a thick shaded band along the inside of its top and left edges.",
    ["inner shadow", "inset shadow", "inset", "inside shadow", "pressed", "effects", "depth"])
def _(S):
    band = path_to_d(D(P(rect(3, 3, 18, 18)), P(rect(8, 8, 14, 14))))
    return [line(rect(3, 3, 18, 18, S.R)), solid(path_to_d(I(P(band), P(rect(3, 3, 17, 17)))))]


@ui("corner-radius", "Rectangle corner with a rounded arc at the top right and a radius line inside it.",
    ["corner radius", "border radius", "rounded corners", "round corner", "radius", "curvature", "shape settings"])
def _(S):
    d = "M3 21V3H13A8 8 0 0 1 21 11V21" if isL(S) else "M3 21V6.5A3.5 3.5 0 0 1 6.5 3H13A8 8 0 0 1 21 11V21"
    return [line(d), line(seg(13, 11, 15.6, 8.4)), pip(S, 13, 11, 1.5, 0.2)]


def _sw_filled():
    return U(P(rect(2, 3, 20, 2, 1)), P(rect(2, 8, 20, 4, 2)), P(rect(2, 15, 20, 6, 3)))


@ui("stroke-width", "Three horizontal bars stacked from thin to thick.",
    ["stroke width", "line width", "line weight", "thickness", "border width", "stroke weight", "outline width"],
    filled=_sw_filled)
def _(S):
    return [blk(S, 3, 3, 18, 2, 1), blk(S, 3, 8, 18, 4, 2), blk(S, 3, 15, 18, 6, 3)]


@ui("dashed-stroke", "A dashed line above a dotted line above a solid line.",
    ["dashed stroke", "dashed line", "dotted line", "line style", "stroke style", "border style", "dash pattern"])
def _(S):
    out = [line(seg(3, 5, 7, 5)), line(seg(10, 5, 14, 5)), line(seg(17, 5, 21, 5)), line(seg(3, 19, 21, 19))]
    for x in (4, 8, 12, 16, 20):
        out.append(pip(S, x, 12, 1.0, 0.1))
    return out


@ui("border-all", "Square divided into four cells with every outer and inner border drawn bold.",
    ["border all", "all borders", "table borders", "cell borders", "grid lines", "gridlines", "spreadsheet"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R * 0.75)), detail(seg(12, 3, 12, 21)), detail(seg(3, 12, 21, 12))]


def rot(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def tangent_pt(p, c, r, side):
    """Tangent point from external point p to circle (c, r); side = +1 / -1 picks the side."""
    dx, dy = c[0] - p[0], c[1] - p[1]
    d = math.hypot(dx, dy)
    a = math.atan2(dy, dx)
    b = math.asin(r / d)
    t = math.sqrt(d * d - r * r)
    ang = a + side * b
    return (p[0] + t * math.cos(ang), p[1] + t * math.sin(ang))


@ui("border-outer", "Square with a bold outer edge and faint dotted dividing lines inside.",
    ["outer border", "outside borders", "box border", "cell border", "table outline", "frame cells", "spreadsheet"])
def _(S):
    out = [shell(rect(3, 3, 18, 18, S.R * 0.75))]
    for p in ((12, 12), (12, 7), (12, 17), (7, 12), (17, 12)):
        out.append(pip(S, p[0], p[1], 1.0, 0.1))
    return out


@ui("border-inner", "Square with a faint dotted outer edge and bold crossing lines inside.",
    ["inner border", "inside borders", "inner lines", "cell dividers", "grid dividers", "table lines", "spreadsheet"])
def _(S):
    out = [line(seg(12, 3, 12, 21)), line(seg(3, 12, 21, 12))]
    seen = set()
    for t in (3, 7.5, 16.5, 21):
        for p in ((t, 3), (t, 21), (3, t), (21, t)):
            if p not in seen:
                seen.add(p)
                out.append(pip(S, p[0], p[1], 1.0, 0.1))
    return out


@ui("line-tool", "Diagonal straight line with a small square handle at each end.",
    ["line tool", "draw line", "straight line", "vector line", "anchor points", "segment", "drawing"])
def _(S):
    return [line(seg(7, 17, 17, 7)), shell(rect(2.5, 16.5, 5, 5, S.R * 0.3)), shell(rect(16.5, 2.5, 5, 5, S.R * 0.3))]


@ui("skew-tool", "Slanted parallelogram with a double-headed sideways arrow above it.",
    ["skew", "skew tool", "shear", "slant", "distort", "italic transform", "transform"])
def _(S):
    return [shell(poly([(9, 11), (21, 11), (15, 21), (3, 21)], closed=True, r=S.r)),
            line(seg(5, 5, 19, 5)), arrow_head(S, (3, 5), 180, 2.5), arrow_head(S, (21, 5), 0, 2.5)]


@ui("perspective-grid", "Trapezoid grid whose lines narrow toward a vanishing point at the top.",
    ["perspective", "perspective grid", "vanishing point", "depth grid", "3d grid", "floor grid", "drawing guide"])
def _(S):
    return [shell(poly([(9, 4), (15, 4), (21, 21), (3, 21)], closed=True, r=S.r)),
            detail(seg(12, 4, 12, 21)), detail(seg(6.5, 11.5, 17.5, 11.5)), detail(seg(4.8, 16.5, 19.2, 16.5))]


@ui("warp-tool", "Rectangle mesh whose top and bottom edges ripple like a wave.",
    ["warp", "warp tool", "mesh warp", "distort", "wave", "liquify", "bend"])
def _(S):
    return [shell("M4 5C9 1.5 15 8.5 20 5V19C15 22.5 9 15.5 4 19Z"),
            detail("M4 12C9 8.5 15 15.5 20 12"), detail("M12 5V19")]


@ui("slice-tool", "Craft knife with a long triangular blade pointing to the upper left.",
    ["slice", "slice tool", "cut", "crop slice", "cutter", "blade", "export slice"])
def _(S):
    return [shell(poly([(10.4, 13.6), (13.6, 10.4), (3.5, 3.5)], closed=True, r=S.r * 0.4)),
            shell(poly([(13.6, 10.4), (21.6, 18.4), (18.4, 21.6), (10.4, 13.6)], closed=True, r=S.r * 0.4))]


@ui("healing-brush", "Adhesive bandage laid at an angle with a small round brush tip beside it.",
    ["healing brush", "spot healing", "retouch", "repair", "bandage", "blemish remover", "photo editing"])
def _(S):
    body = rot([(8, 5.5), (22, 5.5), (22, 12.5), (8, 12.5)], -40, 15, 9)
    pad = rot([(12.5, 5.5), (17.5, 5.5), (17.5, 12.5), (12.5, 12.5)], -40, 15, 9)
    return [shell(poly(body, closed=True, r=S.r)), detail(poly(pad[:2])), detail(poly(pad[2:])),
            shell(circle(6.5, 18, 3.5))]


@ui("smudge-tool", "Pointing fingertip dragging a wavy smear behind it.",
    ["smudge", "smudge tool", "smear", "blend with finger", "finger paint", "drag paint", "photo editing"])
def _(S):
    a, b, h = (16.5, 3.5), (9.5, 11.5), 2.5
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * h, dx / L * h
    p = lambda q, s: f"{fmt(q[0] + s * nx)} {fmt(q[1] + s * ny)}"
    d = f"M{p(a, 1)}L{p(b, 1)}A{h} {h} 0 0 1 {p(b, -1)}L{p(a, -1)}Z"
    return [shell(d), line("M3 20C5.5 15.5 8 22.5 11 18S16.5 15.5 21 18.5")]


@ui("tone-curve", "Square graph with an S-shaped curve rising from the bottom left to the top right.",
    ["tone curve", "curves", "levels", "contrast curve", "color curve", "gamma", "photo editing"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R * 0.75)), detail("M6 18C12 18 10 6 18 6")]


@ui("vignette", "Photo frame with a clear oval in the middle and dark shading in its corners.",
    ["vignette", "vignetting", "edge darkening", "corner shading", "photo effect", "darken edges", "lens effect"])
def _(S):
    inner = rect(3, 5, 18, 14)
    hole = ellipse(12, 12, 6.2, 4.2)
    if isF(S):
        return [shell(rect(2, 4, 20, 16, S.R)), Part("dot", ellipse(12, 12, 7.2, 5))]
    return [shell(rect(2, 4, 20, 16, S.R)), Part("solid", path_to_d(D(P(inner), P(hole))))]


@ui("hotspot-area", "Screen with a dashed box over a button area and a pointer arrow pressing on it.",
    ["hotspot", "hotspot area", "clickable area", "click zone", "interactive region", "tap target", "image map"])
def _(S):
    cur = poly([(11, 10.5), (11, 18), (13.2, 16), (15, 19.2), (16.5, 18.3), (14.7, 15.2), (17.5, 14.8)], closed=True)
    return [frame(S)] + dashed_rect(S, 6, 6, 11, 9, kind=detail) + [Part("dot", cur)]


@ui("prototype-flow", "Two small screens joined by a curved arrow that starts from a dot on the first.",
    ["prototype", "prototype flow", "interaction link", "screen link", "user flow", "connection", "navigate to"])
def _(S):
    return [shell(rect(2, 2, 9, 9, S.R * 0.4)), pip(S, 6.5, 6.5, 1.1, 0.2),
            line("M6.5 6.5H14A4 4 0 0 1 18 10.5V12.5"), arrow_head(S, (18, 13), 90, 2.5),
            shell(rect(14, 14, 8, 8, S.R * 0.4))]


@ui("screen-flow", "Three small phone screens in a row with an arrow running beneath them.",
    ["screen flow", "user journey", "flow chart screens", "app flow", "wireframe flow", "storyboard", "sequence of screens"])
def _(S):
    out = [shell(rect(x, 3, 5, 10, S.R * 0.4)) for x in (2.5, 9.5, 16.5)]
    return out + [line(seg(3, 19, 19, 19)), arrow_head(S, (21, 19), 0, 2.5)]


# =========================================================================== motion, layout and tokens

@ui("keyframe", "Horizontal timeline with two solid diamonds on it.",
    ["keyframe", "key frame", "animation keyframe", "timeline marker", "motion", "animation", "waypoint"])
def _(S):
    out = [line(seg(2, 12, 22, 12))]
    for cx in (6, 18):
        out.append(solid(poly([(cx, 8), (cx + 4, 12), (cx, 16), (cx - 4, 12)], closed=True, r=S.r * 0.5)))
    return out


def _bez(p0, p1, p2, p3, t0, t1, n=6):
    pts = []
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        u = 1 - t
        pts.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return pts


@ui("motion-path", "Small ball at the start of a dashed curving path that ends in an arrowhead.",
    ["motion path", "animation path", "path animation", "trajectory", "move along path", "animate position", "curve"])
def _(S):
    p0, p1, p2, p3 = (5, 13), (5, 5), (10, 4.5), (18, 4.5)
    out = [Part("solid", circle(5, 19, 2.8))]
    for t0, t1 in ((0.0, 0.3), (0.42, 0.66), (0.78, 1.0)):
        out.append(line(poly(_bez(p0, p1, p2, p3, t0, t1), r=0)))
    out.append(arrow_head(S, (21, 4.5), 0, 3))
    return out


@ui("animation-timeline", "Panel with short bars on three tracks and a vertical playhead line between them.",
    ["animation timeline", "timeline", "tracks", "playhead", "motion editor", "video editing", "sequence"])
def _(S):
    return [frame(S), detail(seg(14.5, 3, 14.5, 21)),
            blk(S, 6, 6, 6, 2, 0.8), blk(S, 17.5, 11, 2.5, 2, 0.8), blk(S, 6, 11, 3.5, 2, 0.8),
            blk(S, 6, 16, 6, 2, 0.8), blk(S, 17.5, 16, 2.5, 2, 0.8)]


@ui("onion-skin", "Three identical balls along an arc, two faint outlines behind one solid.",
    ["onion skin", "onionskin", "ghost frames", "previous frames", "animation frames", "frame by frame", "tweening"])
def _(S):
    if S.name == "rounded":
        return [line(circle(4.6, 18.4, 3.4)), line(circle(11.3, 10.7, 3.4)), solid(circle(19.2, 5.6, 3.6))]
    return [line(circle(5, 18, 3)), line(circle(11.5, 10.5, 3)), solid(circle(19, 6, 3.2))]


@ui("before-after", "Photo frame split by a vertical divider with a round drag knob in the middle.",
    ["before after", "compare", "comparison slider", "image compare", "slider compare", "difference", "split view"])
def _(S):
    return [frame(S), detail(seg(12, 3, 12, 8.5)), detail(seg(12, 15.5, 12, 21)), detail(circle(12, 12, 3.5))]


@ui("actual-size", "Frame holding the ratio 1:1 for viewing at true size.",
    ["actual size", "100 percent", "1:1", "true size", "pixel perfect", "reset zoom", "zoom 100"])
def _(S):
    return [shell(rect(2, 4, 20, 16, S.R)), detail(poly([(6, 9.5), (8, 8), (8, 16)])),
            Part("dot", circle(12, 10.5, 1.0)), Part("dot", circle(12, 13.5, 1.0)),
            detail(poly([(16, 9.5), (18, 8), (18, 16)]))]


@ui("artboard-grid", "Four small artboards in a two by two grid, each with a short label dash above it.",
    ["artboards", "artboard grid", "frames", "canvas pages", "screens overview", "design canvas", "multiple pages"])
def _(S):
    out = []
    for x in (3, 14):
        out += [line(seg(x, 2.5, x + 3.5, 2.5)), shell(rect(x, 5, 7, 5.5, S.R * 0.4)),
                line(seg(x, 14, x + 3.5, 14)), shell(rect(x, 16.5, 7, 5.5, S.R * 0.4))]
    return out


@ui("component-instance", "Diamond outline with a smaller hollow diamond inside, marking a linked copy.",
    ["component instance", "instance", "linked copy", "symbol", "master component", "reusable component", "design system"])
def _(S):
    return [shell(poly([(12, 2), (22, 12), (12, 22), (2, 12)], closed=True, r=S.r * 1.5)),
            detail(poly([(12, 8), (16, 12), (12, 16), (8, 12)], closed=True, r=S.r * 0.5))]


@ui("type-scale", "The letter T repeated three times from large to small along one baseline.",
    ["type scale", "typography scale", "font sizes", "text sizes", "heading sizes", "modular scale", "typographic hierarchy"])
def _(S):
    out = []
    for x0, w, y0 in ((2, 8.5, 4.5), (12, 6, 10.5), (19.4, 3.2, 16)):
        mx = x0 + w / 2
        out += [line(seg(x0, y0, x0 + w, y0)), line(seg(mx, y0, mx, 20))]
    return out


@ui("color-tokens", "Row of four tall swatches fading from fully filled to empty.",
    ["color tokens", "design tokens", "color palette", "swatches", "shades", "tints", "color scale"])
def _(S):
    out = []
    for i, x in enumerate((2, 7.33, 12.67, 18)):
        f = (1.0, 0.66, 0.33, 0.0)[i]
        out.append(shell(rect(x, 3 if isF(S) else 4, 4, 18 if isF(S) else 16, 1 if isL(S) else 2)))
        if isF(S):
            if f < 1:
                out.append(Part("dot", rect(x + 1, 4.5, 2, 15 * (1 - f))))
        elif f > 0:
            out.append(Part("solid", rect(x + 1, 19 - 14 * f, 2, 14 * f)))
    return out


@ui("persona-card", "Card with a user avatar at the left and three trait lines beside it.",
    ["persona", "persona card", "user profile card", "user persona", "audience profile", "ux research", "profile"])
def _(S):
    return [shell(rect(2, 4, 20, 16, S.R)), Part("dot", circle(8, 10, 2)),
            detail("M4.8 16.2A3.2 3.2 0 0 1 11.2 16.2"),
            detail(seg(14, 8.5, 19, 8.5)), detail(seg(14, 12, 19, 12)), detail(seg(14, 15.5, 17.5, 15.5))]


@ui("table-cell", "Three by three grid of cells with only the centre cell filled.",
    ["table cell", "cell", "grid cell", "spreadsheet cell", "selected cell", "data cell", "single cell"])
def _(S):
    return [line(rect(3, 3, 18, 18, S.R * 0.5)), line(seg(9, 3, 9, 21)), line(seg(15, 3, 15, 21)),
            line(seg(3, 9, 21, 9)), line(seg(3, 15, 21, 15)), solid(rect(9, 9, 6, 6))]


@ui("table-header-row", "Table whose top row is filled and bold, with three lighter rows beneath.",
    ["table header", "header row", "column headers", "table head", "data table", "spreadsheet header", "grid header"])
def _(S):
    top = clip(rect(2, 2, 20, 7), rect(2, 2, 20, 20, S.R * 0.5 + 1))
    return [line(rect(3, 3, 18, 18, S.R * 0.5)), solid(top), line(seg(3, 12.5, 21, 12.5)), line(seg(3, 16.75, 21, 16.75))]


@ui("key-value-list", "Rows with a bold label bar on the left and a lighter value line on the right.",
    ["key value", "key value list", "description list", "properties list", "details list", "label and value", "attributes"])
def _(S):
    out = []
    for y in (5, 11.5, 18):
        out += [blk(S, 3, y - 1.5, 6, 3, 1.5), line(seg(12, y, 21, y))]
    return out


@ui("fill-handle", "Selected cell with a bold border and a small solid square on its lower right corner.",
    ["fill handle", "autofill", "drag to fill", "copy down", "spreadsheet fill", "extend selection", "series fill"])
def _(S):
    return [shell(rect(3, 3, 12, 9, S.R * 0.4)), blk(S, 12.25, 9.5, 5, 5, 1),
            pip(S, 9, 17, 1.0, 0.1), pip(S, 9, 21, 1.0, 0.1)]


@ui("transpose", "Two small tables joined by a curved arrow, one split into rows and the other into columns.",
    ["transpose", "rows to columns", "swap rows and columns", "pivot", "flip table", "table rotate", "spreadsheet"])
def _(S):
    return [shell(rect(2, 2, 8, 8, S.R * 0.4)), detail(seg(2, 6, 10, 6)),
            shell(rect(14, 14, 8, 8, S.R * 0.4)), detail(seg(18, 14, 18, 22)),
            line("M6 12.5V15A3 3 0 0 0 9 18H11.5"), arrow_head(S, (12.2, 18), 0, 2.3)]


# =========================================================================== tables and editors

@ui("spreadsheet-grid", "Grid whose top row and first column are shaded header bands, with cell lines in the body.",
    ["spreadsheet", "spreadsheet grid", "sheet", "rows and columns", "excel", "data grid", "worksheet"])
def _(S):
    band = path_to_d(D(I(P(rect(2, 2, 20, 20)), P(rect(2, 2, 20, 20, S.R * 0.5 + 1))), P(rect(8.5, 8.5, 14, 14))))
    return [line(rect(3, 3, 18, 18, S.R * 0.5)), solid(band), line(seg(14.5, 8, 14.5, 21)), line(seg(8, 14.5, 21, 14.5))]


@ui("nested-table", "Table grid with a smaller table inside one of its cells.",
    ["nested table", "table in table", "sub table", "inner table", "child table", "grid in grid", "embedded table"])
def _(S):
    return [line(rect(3, 3, 18, 18, S.R * 0.5)), line(seg(9, 3, 9, 21)), line(seg(3, 9, 21, 9)),
            line(rect(12.5, 12.5, 5, 5, S.R * 0.2)), solid(rect(14, 14, 2, 2))]


@ui("code-folding", "Three code lines with a fold arrow at the start and the lower lines indented.",
    ["code folding", "fold code", "collapse block", "collapse code", "fold region", "outline code", "editor gutter"])
def _(S):
    return [chev(S, 5, 5.5, w=2.5, h=2, deg=90), line(seg(10, 5.5, 20, 5.5)), line(seg(5, 10, 5, 20)),
            line(seg(10, 12, 20, 12)), line(seg(10, 18, 17, 18))]


@ui("minimap", "Editor window with a narrow strip at its right edge holding a highlighted viewport box.",
    ["minimap", "code minimap", "document overview", "scroll overview", "code overview", "editor overview", "outline strip"])
def _(S):
    return [win(S), detail(seg(15, 4, 15, 20)), detail(seg(6, 8, 12, 8)), detail(seg(6, 12, 10, 12)),
            detail(seg(6, 16, 12, 16)), blk(S, 16.5, 7.5, 3, 5.5, 0.8)]


@ui("multi-cursor", "Three text lines each followed by a tall cursor bar in the same column.",
    ["multi cursor", "multiple cursors", "multi select", "column edit", "simultaneous edit", "add cursor", "code editor"])
def _(S):
    out = []
    for y, x1 in ((5, 11.5), (12, 8), (19, 11.5)):
        out += [line(seg(3, y, x1, y)), line(seg(15, y - 3, 15, y + 3)), line(seg(18, y, 21, y))]
    return out


@ui("indent-guides", "Code lines at three indent levels with dotted vertical guides marking each level.",
    ["indent guides", "indentation guides", "indent lines", "nesting lines", "block guides", "tab guides", "code editor"])
def _(S):
    out = [line(seg(3, 4.5, 15, 4.5)), line(seg(9.5, 9.5, 19, 9.5)), line(seg(16, 14.5, 21, 14.5)),
           line(seg(16, 19.5, 21, 19.5))]
    for y in (9.5, 14.5, 19.5):
        out.append(pip(S, 5, y, 1.0, 0.1))
    for y in (14.5, 19.5):
        out.append(pip(S, 12, y, 1.0, 0.1))
    return out


@ui("show-whitespace", "Text lines with dots marking the spaces between words and a pilcrow at the end.",
    ["show whitespace", "invisible characters", "formatting marks", "show invisibles", "paragraph mark", "spaces and tabs", "hidden characters"])
def _(S):
    return [line(seg(3, 6, 8, 6)), pip(S, 11, 6, 1.0, 0.1), line(seg(14, 6, 21, 6)),
            line(seg(3, 17, 9, 17)),
            line("M20 21V12H15.5A3.25 3.25 0 0 0 15.5 18.5H17"), line(seg(17, 12, 17, 21))]


@ui("find-and-replace", "Magnifying glass above two small arrows that point in opposite directions.",
    ["find and replace", "find replace", "search and replace", "replace text", "substitute", "swap text", "text editor"])
def _(S):
    return [shell(circle(8.5, 8.5, 5)), line(seg(12.5, 12.5, 15.5, 15.5)),
            line(seg(14, 17, 20.5, 17)), arrow_head(S, (20.5, 17), 0, 2), line(seg(20, 21, 13.5, 21)),
            arrow_head(S, (13.5, 21), 180, 2)]


@ui("text-selection-handles", "Highlighted text with a teardrop handle hanging from each end of the selection.",
    ["selection handles", "text selection", "drag handles", "select text", "mobile text selection", "caret handles", "highlight"])
def _(S):
    drop = lambda x: f"M{x} 12.5L{x + 2.3} 16.2A2.7 2.7 0 1 1 {x - 2.3} 16.2Z"
    return [shell(rect(5, 3, 14, 9.5, S.R * 0.3)), detail(seg(8.5, 7.75, 15.5, 7.75)),
            solid(drop(5)), solid(drop(19))]


@ui("select-all", "Dashed selection frame around three solid lines of content.",
    ["select all", "select everything", "highlight all", "whole selection", "ctrl a", "mark all", "selection"])
def _(S):
    return dashed_rect(S, 3, 3, 18, 18) + [line(seg(7, 8, 17, 8)), line(seg(7, 12, 17, 12)), line(seg(7, 16, 13, 16))]


@ui("deselect", "Dashed selection frame with a diagonal slash cutting through its lower right corner.",
    ["deselect", "clear selection", "unselect", "select none", "drop selection", "cancel selection", "selection"])
def _(S):
    parts = dashed_rect(S, 3, 3, 15, 15)
    parts.pop(2)
    return parts + [line(seg(13.5, 22, 22, 13.5))]


@ui("invert-selection", "Square with its corners filled around a circular window outlined with dashes.",
    ["invert selection", "reverse selection", "inverse selection", "select inverse", "flip selection", "opposite selection", "selection"])
def _(S):
    out = [shell(rect(3, 3, 18, 18, S.R))]
    if isF(S):
        out.append(Part("dot", circle(12, 12, 7)))
    else:
        out.append(Part("solid", path_to_d(D(P(rect(4, 4, 16, 16)), P(circle(12, 12, 7))))))
    for a0 in (20, 110, 200, 290):
        out.append(line(arc(12, 12, 3.8, a0, a0 + 50)))
    return out


@ui("distraction-free-mode", "Screen with one short text line in the middle and wide empty margins around it.",
    ["distraction free", "focus mode", "zen mode", "minimal mode", "writing mode", "full screen editor", "clean view"])
def _(S):
    return [shell(rect(2, 4, 20, 16, S.R)), detail(seg(8.5, 12, 15.5, 12))]


@ui("reader-view", "Browser window with a centred column of text lines below a top bar.",
    ["reader view", "reading mode", "reader mode", "article view", "clean reading", "text only view", "browser"])
def _(S):
    return [win(S), detail(seg(3, 8.5, 21, 8.5)), blk(S, 8.5, 11, 7, 2, 0.8), detail(seg(8.5, 15.5, 15.5, 15.5))]


@ui("comment-out", "Two forward slashes followed by a dashed faded line of text.",
    ["comment out", "comment code", "disable line", "double slash", "line comment", "toggle comment", "code editor"])
def _(S):
    return [line(seg(3, 17, 7, 7)), line(seg(8.5, 17, 12.5, 7)), line(seg(15, 12, 17.5, 12)), line(seg(19.5, 12, 21.5, 12))]
