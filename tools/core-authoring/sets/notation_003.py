"""TypeIcon Core: notation (batch notation_003).

Typography marks, currency and unit signs, and engineering drawing symbols. Letters are open strokes
(line parts) built from a tiny stroke alphabet, so Line and Rounded differ by caps, joins and corner
fillets, and Filled makes the strokes heavier. Frames and closed figures use shells.
"""
from __future__ import annotations

import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d

CAT = "notation"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def ep(cx, cy, rx, ry, a):
    r = math.radians(a)
    return cx + rx * math.cos(r), cy + ry * math.sin(r)


def earc(cx, cy, rx, ry, a0, a1, move=True):
    """Elliptical arc from angle a0 to a1 (degrees, screen angles; increasing = clockwise on screen)."""
    x0, y0 = ep(cx, cy, rx, ry, a0)
    x1, y1 = ep(cx, cy, rx, ry, a1)
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 1 if a1 > a0 else 0
    head = f"M{fmt(x0)} {fmt(y0)}" if move else ""
    return f"{head}A{fmt(rx)} {fmt(ry)} 0 {large} {sweep} {fmt(x1)} {fmt(y1)}"


def pl(S, pts, closed=False, r=None):
    return line(poly(pts, closed=closed, r=S.r if r is None else r))


def arrow_head(S, tip, frm, size=4.0, spread=38.0, kind=None):
    """Open arrowhead chevron at tip for a shaft arriving from frm."""
    dx, dy = tip[0] - frm[0], tip[1] - frm[1]
    a = math.atan2(dy, dx)
    pts = []
    for s in (+1, -1):
        b = a + math.pi + s * math.radians(spread)
        pts.append((tip[0] + size * math.cos(b), tip[1] + size * math.sin(b)))
    return (kind or line)(poly([pts[0], tip, pts[1]], r=S.r), stroke_miterlimit="1.6")


def arrow(S, p0, p1, size=4.0, kind=None, back=0.8):
    d = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    q = (p1[0] - (p1[0] - p0[0]) / d * back, p1[1] - (p1[1] - p0[1]) / d * back)
    return [(kind or line)(seg(*p0, *q)), arrow_head(S, p1, p0, size, kind=kind)]


def diamond(x, y, r):
    return solid(poly([(x, y - r), (x + r, y), (x, y + r), (x - r, y)], closed=True))


# ---- tiny stroke alphabet: each returns a list of d-strings (open strokes) inside box (x, y, w, h)

def g_A(S, x, y, w, h, bar=0.66):
    by = y + h * bar
    return [poly([(x, y + h), (x + w / 2, y), (x + w, y + h)], r=S.r), seg(x + w * 0.22, by, x + w * 0.78, by)]


def g_bowl(x, y, w, bh, rr=None):
    """Right-hand bowl of P/R/B from the stem at x: top y, height bh."""
    r = bh / 2 if rr is None else rr
    return f"M{fmt(x)} {fmt(y)}H{fmt(x + w - r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x + w - r)} {fmt(y + 2 * r)}H{fmt(x)}"


def g_P(S, x, y, w, h, bh=None):
    bh = h * 0.55 if bh is None else bh
    return [seg(x, y, x, y + h), g_bowl(x, y, w, bh)]


def g_R(S, x, y, w, h, bh=None):
    bh = h * 0.55 if bh is None else bh
    return [seg(x, y, x, y + h), g_bowl(x, y, w, bh), poly([(x + w * 0.35, y + bh), (x + w, y + h)], r=0)]


def g_B(S, x, y, w, h):
    m = y + h / 2
    return [seg(x, y, x, y + h), g_bowl(x, y, w * 0.9, h / 2), g_bowl(x, m, w, h / 2)]


def g_C(S, x, y, w, h, gap=42):
    return [earc(x + w / 2, y + h / 2, w / 2, h / 2, -gap, -360 + gap)]


def g_G(S, x, y, w, h, gap=42):
    cx, cy, rx, ry = x + w / 2, y + h / 2, w / 2, h / 2
    ex = cx + rx
    return [earc(cx, cy, rx, ry, -gap, -360) + f"H{fmt(cx + rx * 0.15)}"]


def g_F(S, x, y, w, h, arm=0.45):
    return [poly([(x + w, y), (x, y), (x, y + h)], r=S.r), seg(x, y + h * arm, x + w * 0.8, y + h * arm)]


def g_K(S, x, y, w, h):
    return [seg(x, y, x, y + h), poly([(x + w, y), (x, y + h * 0.62)], r=0), poly([(x + w * 0.28, y + h * 0.42), (x + w, y + h)], r=0)]


def g_N(S, x, y, w, h):
    return [poly([(x, y + h), (x, y), (x + w, y + h), (x + w, y)], r=S.r)]


def g_T(S, x, y, w, h):
    return [seg(x, y, x + w, y), seg(x + w / 2, y, x + w / 2, y + h)]


def g_W(S, x, y, w, h):
    return [poly([(x, y), (x + w * 0.25, y + h), (x + w / 2, y + h * 0.3), (x + w * 0.75, y + h), (x + w, y)], r=S.r)]


def g_V(S, x, y, w, h):
    return [poly([(x, y), (x + w / 2, y + h), (x + w, y)], r=S.r)]


def g_H(S, x, y, w, h):
    return [seg(x, y, x, y + h), seg(x + w, y, x + w, y + h), seg(x, y + h / 2, x + w, y + h / 2)]


def g_L(S, x, y, w, h):
    return [poly([(x, y), (x, y + h), (x + w, y + h)], r=S.r)]


def g_J(S, x, y, w, h):
    r = min(w * 0.8, 4.5)
    return [f"M{fmt(x + w)} {fmt(y)}V{fmt(y + h - r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x + w - r)} {fmt(y + h)}H{fmt(x + w - 2 * r)}"]


def g_S(S, x, y, w, h):
    cx, rx, ry = x + w / 2, w / 2, h / 4
    return [earc(cx, y + ry, rx, ry, -25, -270) + earc(cx, y + 3 * ry, rx, ry, -90, 155, move=False)]


def g_m(S, x, y, w, h):
    r = w / 4
    return [seg(x, y, x, y + h), f"M{fmt(x)} {fmt(y + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x + w / 2)} {fmt(y + r)}V{fmt(y + h)}",
            f"M{fmt(x + w / 2)} {fmt(y + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x + w)} {fmt(y + r)}V{fmt(y + h)}"]


def g_h(S, x, y, w, h, xh):
    """Lowercase h: ascender from y, x-height xh (px from top of box to arch top)."""
    r = w / 2
    return [seg(x, y, x, y + h), f"M{fmt(x)} {fmt(y + xh + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x + w)} {fmt(y + xh + r)}V{fmt(y + h)}"]


def g_n(S, x, y, w, h):
    return g_h(S, x, y, w, h, 0)


def g_d(S, x, y, w, h, xh):
    """Lowercase d: bowl at left, ascender at right."""
    bh = h - xh
    r = min(w, bh) / 2
    return [seg(x + w, y, x + w, y + h), earc(x + w - r, y + h - r, r, r, 0, 360 - 1e-3)[:0] + circle(x + w - r, y + h - r, r)]


def g_x(S, x, y, w, h):
    return [seg(x, y, x + w, y + h), seg(x + w, y, x, y + h)]


def g_z(S, x, y, w, h):
    return [poly([(x, y), (x + w, y), (x, y + h), (x + w, y + h)], r=S.r)]


def g_o(S, x, y, w, h):
    return [ellipse(x + w / 2, y + h / 2, w / 2, h / 2)]


def g_k(S, x, y, w, h, xh):
    return [seg(x, y, x, y + h), poly([(x + w, y + xh), (x, y + xh + (h - xh) * 0.62)], r=0),
            poly([(x + w * 0.3, y + xh + (h - xh) * 0.42), (x + w, y + h)], r=0)]


def gl(S, parts):
    return [line(d) for d in parts]


# ============================================================================ typography

def fat_A(S, x0, x1, yt, yb, t, by, bt):
    """Solid capital A with leg thickness t and crossbar at by (thickness bt), as a d-string."""
    xm = (x0 + x1) / 2
    r = L(S, 0.0, 0.6)
    left = poly([(x0, yb), (x0 + t, yb), (xm + t / 2, yt), (xm - t / 2, yt)], closed=True, r=r)
    right = poly([(x1, yb), (x1 - t, yb), (xm - t / 2, yt), (xm + t / 2, yt)], closed=True, r=r)
    # crossbar between the leg inner edges
    slope = (x1 - x0 - t) / 2 / (yb - yt)
    lx = x0 + t + (yb - by) * 0 - ((yb - (by + bt / 2)) * (-1)) * 0
    inner_l = x0 + (yb - (by + bt / 2)) * (xm - t / 2 - x0 - 0) / (yb - yt) + t / 2
    inner_r = x1 - (yb - (by + bt / 2)) * (x1 - (xm + t / 2)) / (yb - yt) - t / 2
    bar = rect(inner_l, by - bt / 2, inner_r - inner_l, bt)
    return path_to_d(U(P(left), P(right), P(bar)))


@icon("blackletter-font", CAT, "Capital A drawn in angular gothic blackletter style.",
      tags=["blackletter", "gothic", "fraktur", "old english", "typeface", "font", "calligraphy"])
def _(S):
    r = L(S, 0.0, 0.5)
    return [solid(poly([(4, 20.5), (8, 20.5), (13, 5.5), (9, 5.5)], closed=True, r=r)),
            line(poly([(12.5, 7), (17.5, 12), (17.5, 19.5)], r=S.r)),
            line(seg(9, 14, 15, 14)),
            diamond(6, 21, 2), diamond(17.5, 21, 2)]


@icon("slab-serif-font", CAT, "Capital A with thick rectangular slab serifs.",
      tags=["slab serif", "egyptian", "serif", "typeface", "font", "typography", "letter a"])
def _(S):
    return [line(poly([(6.5, 19), (10.5, 5), (13.5, 5), (17.5, 19)], r=S.r)),
            line(seg(9.2, 14.5, 14.8, 14.5)),
            line(seg(3.5, 19.5, 9.5, 19.5)), line(seg(14.5, 19.5, 20.5, 19.5))]


@icon("x-height", CAT, "Lowercase h and x crossing guide lines marking baseline, x-height and ascender.",
      tags=["x-height", "baseline", "ascender", "typography", "font metrics", "type", "guide lines"])
def _(S):
    out = []
    for gy in (4, 12, 20):
        out += [line(seg(2, gy, 5, gy)), line(seg(19, gy, 22, gy))]
    out += [line(seg(7.5, 4, 7.5, 20)), line("M7.5 15.5A2.25 2.25 0 0 1 12 15.5V20"),
            line(seg(14, 12, 18, 20)), line(seg(18, 12, 14, 20))]
    return out


@icon("text-baseline", CAT, "Short word resting on a baseline with a descender dipping below it.",
      tags=["baseline", "descender", "typography", "text line", "font metrics", "type", "text"])
def _(S):
    return [line(seg(2, 15, 22, 15)),
            line(seg(5, 8, 5, 15)), line("M5 11.2A3 3 0 0 1 11 11.2V15"),
            line(poly([(14, 8), (17.2, 15), (20.5, 8)], r=0)), line(seg(17.2, 15, 14.3, 20.5))]


@icon("font-weight-scale", CAT, "Three capital A letters growing from thin to regular to heavy.",
      tags=["font weight", "bold", "thin", "regular", "typography", "weights", "type"])
def _(S):
    return [line(poly([(3, 19.5), (5.25, 6), (7.5, 19.5)], r=S.r * 0.5)), line(seg(3.9, 15, 6.6, 15)),
            solid(fat_A(S, 9, 15, 6, 20, 2.8, 15.5, 2.4)),
            solid(fat_A(S, 16, 22, 6, 20, 3.6, 16, 3))]


@icon("kerning-pair", CAT, "Letters A and V set apart with a bracket measuring the gap between them.",
      tags=["kerning", "letter spacing", "typography", "tracking", "av pair", "type", "gap"])
def _(S):
    return [line(poly([(2, 15), (5.5, 4), (9, 15)], r=S.r)), line(seg(3.4, 11.5, 7.6, 11.5)),
            line(poly([(15, 4), (18.5, 15), (22, 4)], r=S.r)),
            line(seg(9, 17.5, 9, 21)), line(seg(15, 17.5, 15, 21)), line(seg(9, 19.25, 15, 19.25))]


@icon("typesetting-composing-stick", CAT, "Composing stick tray holding a row of metal type.",
      tags=["composing stick", "letterpress", "typesetting", "movable type", "printing", "type sorts", "print shop"])
def _(S):
    return [shell(poly([(2, 5), (6, 5), (6, 14), (22, 14), (22, 20), (2, 20)], closed=True, r=S.r)),
            solid(rect(9, 6, 3, 7.5)), solid(rect(13.5, 6, 3, 7.5)), solid(rect(18, 6, 3, 7.5))]


@icon("dele-mark", CAT, "Proofreading delete mark: a looped stroke with a curling tail.",
      tags=["dele", "delete mark", "proofreading", "proof mark", "editing", "copyediting", "remove text"])
def _(S):
    return [line(ellipse(10.5, 15, 5.5, 4.75)),
            line("M10.5 10.25C10.5 6.5 13 3.75 20 4.75")]


@icon("insertion-caret", CAT, "Proofreading caret under a gap in a line of text with a word written above.",
      tags=["caret", "insert mark", "proofreading", "proof mark", "editing", "copyediting", "insert text"])
def _(S):
    return [line(seg(2, 14, 10, 14)), line(seg(16, 14, 22, 14)),
            line(poly([(10, 21), (13, 16), (16, 21)], r=S.r)),
            line(circle(6.5, 6.5, 2.75)), line(seg(9.25, 3.75, 9.25, 9.25)),
            line(seg(13.5, 3, 13.5, 9.25))]


@icon("close-up-mark", CAT, "Proofreading close-up mark: two arcs pulling separated letters together.",
      tags=["close up", "close space", "proofreading", "proof mark", "editing", "copyediting", "remove space"])
def _(S):
    return [line("M9 3.5Q12 8.5 15 3.5"), line("M9 20.5Q12 15.5 15 20.5")] + \
        gl(S, g_h(S, 2.5, 6, 4.5, 12, 4.5)) + gl(S, g_h(S, 17.5, 6, 4, 12, 4.5))


@icon("true-false", CAT, "Check mark and cross mark side by side for true and false.",
      tags=["true", "false", "yes no", "correct incorrect", "boolean", "quiz", "right wrong"])
def _(S):
    return [line(poly([(2.5, 12.5), (6, 16.5), (11, 7.5)], r=S.r)),
            line(seg(14.5, 8, 21.5, 16)), line(seg(21.5, 8, 14.5, 16))]


@icon("cent-sign", CAT, "Cent sign: a lowercase c with a vertical stroke through it.",
      tags=["cent", "currency", "penny", "coin", "money", "us cent", "price"])
def _(S):
    return [line(earc(12, 12, 6, 6.5, -45, -315)), line(seg(12, 3.5, 12, 20.5))]


# ============================================================================ currency signs

def glyph_W(S):
    return poly([(2.5, 4.5), (7.25, 19), (12, 8), (16.75, 19), (21.5, 4.5)], r=S.r)


@icon("won-sign", CAT, "Won sign: a capital W crossed by two horizontal bars.",
      tags=["won", "korean won", "currency", "krw", "korea", "money", "south korea"])
def _(S):
    return [line(glyph_W(S), stroke_miterlimit="1.5"), line(seg(2, 9.5, 22, 9.5)), line(seg(2, 14.25, 22, 14.25))]


@icon("franc-sign", CAT, "Franc sign: a capital F with an extra bar crossing its stem.",
      tags=["franc", "swiss franc", "currency", "chf", "french franc", "money", "switzerland"])
def _(S):
    return gl(S, g_F(S, 8, 3.5, 10.5, 17, 0.4)) + [line(seg(4, 15, 13, 15))]


@icon("turkish-lira-sign", CAT, "Turkish lira sign: an upright stem with two slanted bars and a curved foot.",
      tags=["lira", "turkish lira", "currency", "try", "turkey", "money", "tl"])
def _(S):
    return [line("M8 3V15C8 18.5 11 20.5 17 20.5"), line(seg(3.5, 12, 17, 8)), line(seg(3.5, 16.5, 17, 12.5))]


@icon("philippine-peso-sign", CAT, "Philippine peso sign: a capital P with two horizontal bars across it.",
      tags=["peso", "philippine peso", "currency", "php", "philippines", "money", "piso"])
def _(S):
    return gl(S, g_P(S, 7, 3, 10, 18, 11)) + [line(seg(3, 6.25, 19, 6.25)), line(seg(3, 10.75, 19, 10.75))]


@icon("naira-sign", CAT, "Naira sign: a capital N crossed by two horizontal bars.",
      tags=["naira", "nigerian naira", "currency", "ngn", "nigeria", "money", "africa"])
def _(S):
    return [line(poly([(5.5, 20), (5.5, 4), (18.5, 20), (18.5, 4)], r=S.r), stroke_miterlimit="1.5"),
            line(seg(2, 9.5, 22, 9.5)), line(seg(2, 14.5, 22, 14.5))]


@icon("shekel-sign", CAT, "Shekel sign: two interlocking square hooks, one opening up and one opening down.",
      tags=["shekel", "new shekel", "currency", "ils", "israel", "money", "sheqel"])
def _(S):
    return [line(poly([(3, 20), (3, 5), (10, 5), (10, 15)], r=S.r)), line(poly([(21, 4), (21, 19), (14, 19), (14, 9)], r=S.r))]


@icon("dong-sign", CAT, "Dong sign: a lowercase d with a bar across its ascender and a line underneath.",
      tags=["dong", "vietnamese dong", "currency", "vnd", "vietnam", "money", "underline"])
def _(S):
    return [line(circle(9.25, 11.5, 4.75)), line(seg(14, 3, 14, 16.5)), line(seg(10.5, 5.5, 17.5, 5.5)),
            line(seg(4, 20.5, 20, 20.5))]


@icon("kip-sign", CAT, "Kip sign: a capital K with a horizontal bar crossing its stem.",
      tags=["kip", "lao kip", "currency", "lak", "laos", "money", "southeast asia"])
def _(S):
    return gl(S, g_K(S, 8.5, 3.5, 10, 17)) + [line(seg(3.5, 12, 13, 12))]


@icon("tugrik-sign", CAT, "Tugrik sign: a capital T with two slanted strokes crossing its stem.",
      tags=["tugrik", "tugrug", "mongolian tugrik", "currency", "mnt", "mongolia", "money"])
def _(S):
    return gl(S, g_T(S, 4, 4.5, 16, 16)) + [line(seg(8, 13, 16, 9)), line(seg(8, 18, 16, 14))]


@icon("hryvnia-sign", CAT, "Hryvnia sign: a reversed S shape crossed by two horizontal bars.",
      tags=["hryvnia", "ukrainian hryvnia", "currency", "uah", "ukraine", "money", "grivna"])
def _(S):
    cx, rx, ry = 12, 6, 4.25
    top, bot = 3.5 + ry, 3.5 + 3 * ry
    d = earc(cx, top, rx, ry, -155, 90) + earc(cx, bot, rx, ry, -90, -335, move=False)
    return [line(d), line(seg(3, 9.5, 21, 9.5)), line(seg(3, 14.5, 21, 14.5))]


@icon("cedi-sign", CAT, "Cedi sign: a capital C with a slanted stroke through it.",
      tags=["cedi", "ghana cedi", "currency", "ghs", "ghana", "money", "africa"])
def _(S):
    return [line(earc(12.5, 12, 6.5, 8.5, -42, -318)), line(seg(14.5, 2.5, 9.5, 21.5))]


@icon("tenge-sign", CAT, "Tenge sign: a capital T with a second parallel bar above its top.",
      tags=["tenge", "kazakhstani tenge", "currency", "kzt", "kazakhstan", "money", "central asia"])
def _(S):
    return [line(seg(4, 4.5, 20, 4.5)), line(seg(4, 9, 20, 9)), line(seg(12, 4.5, 12, 20.5))]


@icon("ruble-sign", CAT, "Ruble sign: a capital P with a horizontal bar across its stem below the bowl.",
      tags=["ruble", "rouble", "russian ruble", "currency", "rub", "russia", "money"])
def _(S):
    return gl(S, g_P(S, 8, 3, 9, 18, 8.5)) + [line(seg(4, 15.5, 14, 15.5))]


@icon("manat-sign", CAT, "Manat sign: an arch with a vertical stroke rising through its centre.",
      tags=["manat", "azerbaijani manat", "currency", "azn", "azerbaijan", "money", "arch"])
def _(S):
    return [line("M5 20.5V12A7 7 0 0 1 19 12V20.5"), line(seg(12, 2.5, 12, 20.5))]


@icon("lari-sign", CAT, "Lari sign: an arch with two short strokes on top and a flat foot line.",
      tags=["lari", "georgian lari", "currency", "gel", "georgia", "money", "caucasus"])
def _(S):
    return [line("M6 20.5V14A6 6 0 0 1 18 14V20.5"), line(seg(3, 20.5, 21, 20.5)),
            line(seg(9.5, 3.5, 9.5, 8.5)), line(seg(14.5, 3.5, 14.5, 8.5))]


@icon("baht-sign", CAT, "Baht sign: a capital B with its stem running through the top and bottom.",
      tags=["baht", "thai baht", "currency", "thb", "thailand", "money", "southeast asia"])
def _(S):
    return [line(seg(7, 2.5, 7, 21.5)), line(g_bowl(7, 5, 9, 7)), line(g_bowl(7, 12, 10.5, 7))]


@icon("costa-rican-colon-sign", CAT, "Colon currency sign: a capital C crossed by two slanted strokes.",
      tags=["colon", "costa rican colon", "salvadoran colon", "currency", "crc", "costa rica", "money"])
def _(S):
    return [line(earc(12, 12, 7.5, 8.5, -42, -318)), line(seg(8.5, 20.5, 12.5, 3.5)), line(seg(12.5, 20.5, 16.5, 3.5))]


@icon("guarani-sign", CAT, "Guarani sign: a capital G with a vertical stroke passing through it.",
      tags=["guarani", "paraguayan guarani", "currency", "pyg", "paraguay", "money", "south america"])
def _(S):
    cx, cy, rx, ry = 12.5, 12, 7, 8.5
    return [line(earc(cx, cy, rx, ry, -42, -360) + f"H{fmt(cx + 1.5)}"), line(seg(10, 2.5, 10, 21.5))]


@icon("dram-sign", CAT, "Dram sign: an arch with two horizontal bars across its legs.",
      tags=["dram", "armenian dram", "currency", "amd", "armenia", "money", "caucasus"])
def _(S):
    return [line("M6 19V11.5A6 6 0 0 1 18 11.5V19"), line(seg(3, 14.5, 21, 14.5)), line(seg(3, 19, 21, 19))]


@icon("florin-sign", CAT, "Florin sign: a slanted italic f with a hooked top and a tail below the baseline.",
      tags=["florin", "guilder", "gulden", "currency", "netherlands", "money", "italic f"])
def _(S):
    return [line("M18 4.5C13.5 3 11.5 5 11 8.5L8.5 18.5C8 20.5 6.5 21 3.5 20.5"), line(seg(7.5, 11.5, 16.5, 11.5))]


@icon("currency-sign", CAT, "Generic currency sign: a small circle with four short rays at the corners.",
      tags=["currency", "generic currency", "money", "unspecified currency", "scarab", "monetary", "symbol"])
def _(S):
    out = [line(circle(12, 12, 4.25))]
    for a in (45, 135, 225, 315):
        x0, y0 = pt_on(12, 12, 7.5, a)
        x1, y1 = pt_on(12, 12, 10, a)
        out.append(line(seg(x0, y0, x1, y1)))
    return out


@icon("peseta-sign", CAT, "Peseta sign: a capital P followed by a small ts.",
      tags=["peseta", "spanish peseta", "currency", "pts", "spain", "money", "old currency"])
def _(S):
    return gl(S, g_P(S, 3, 4, 7.5, 16, 8.5)) + [line(seg(14.5, 10, 14.5, 19.5)), line(seg(12, 12.5, 17, 12.5))] + \
        gl(S, g_S(S, 18, 12.5, 4.5, 7.5))


@icon("brazilian-real-sign", CAT, "Real currency sign: a capital R followed by a dollar sign.",
      tags=["real", "brazilian real", "currency", "brl", "brazil", "money", "r$"])
def _(S):
    return gl(S, g_R(S, 3, 4, 8, 16, 8.5)) + gl(S, g_S(S, 15, 6.5, 5.5, 11)) + [line(seg(17.75, 3.5, 17.75, 20.5))]


@icon("zloty-sign", CAT, "Zloty sign: a lowercase z followed by an l with a slanted stroke through it.",
      tags=["zloty", "zloti", "polish zloty", "currency", "pln", "poland", "money"])
def _(S):
    return gl(S, g_z(S, 3, 9, 7.5, 11)) + [line(seg(16, 3.5, 16, 20)), line(seg(12.5, 15, 19.5, 9.5))]


@icon("celsius", CAT, "Degree Celsius: a small raised ring followed by a capital C.",
      tags=["celsius", "centigrade", "degrees", "temperature", "weather", "unit", "degree c"])
def _(S):
    return [line(circle(5.5, 7.5, 2.5)), line(earc(16, 13.5, 5.5, 7, -45, -315))]


@icon("fahrenheit", CAT, "Degree Fahrenheit: a small raised ring followed by a capital F.",
      tags=["fahrenheit", "degrees", "temperature", "weather", "unit", "degree f", "us temperature"])
def _(S):
    return [line(circle(5.5, 7.5, 2.5))] + gl(S, g_F(S, 12.5, 6.5, 9, 14, 0.5))


@icon("kelvin", CAT, "Kelvin unit: a capital K beside a small thermometer.",
      tags=["kelvin", "absolute temperature", "si unit", "thermodynamic", "physics", "unit", "temperature"])
def _(S):
    return gl(S, g_K(S, 3.5, 4, 8, 16)) + [shell("M16 14.76V6A2 2 0 0 1 20 6V14.76A3 3 0 1 1 16 14.76Z"), dot(18, 17, 1)]


@icon("angstrom-sign", CAT, "Angstrom sign: a capital A with a small ring above it.",
      tags=["angstrom", "unit of length", "wavelength", "atomic scale", "physics", "unit", "a ring"])
def _(S):
    return [line(circle(12, 5.5, 2.25))] + gl(S, g_A(S, 4.5, 11, 15, 10, 0.68))


@icon("liter-sign", CAT, "Liter sign: a cursive script lowercase l with a looped top.",
      tags=["liter", "litre", "volume", "script l", "unit", "capacity", "metric"])
def _(S):
    return [line("M6.5 17.5C9.5 16 15 8.5 15 5.5C15 3 12.5 3 11.5 5.5C10 9 9 14 10 17.5C10.5 19.5 13 20 17.5 16")]


# ============================================================================ unit signs

@icon("decibel", CAT, "Decibel unit: the letters dB beside two curved sound waves.",
      tags=["decibel", "db", "sound level", "loudness", "volume", "acoustics", "unit"])
def _(S):
    out = [line(circle(5, 15.75, 3)), line(seg(8, 7, 8, 18.75))]
    out += gl(S, g_B(S, 11, 7, 3.5, 12))
    out += [line(earc(15, 13, 3, 3, -40, 40)), line(earc(15, 13, 6.5, 6.5, -40, 40))]
    return out


@icon("hertz", CAT, "Hertz unit: the letters Hz above a short sine wave.",
      tags=["hertz", "hz", "frequency", "cycles per second", "wave", "signal", "unit"])
def _(S):
    return gl(S, g_H(S, 4.5, 3, 5.5, 8)) + gl(S, g_z(S, 13.5, 3, 6, 8)) + \
        [line("M2 17.5A5 3 0 0 1 12 17.5A5 3 0 0 0 22 17.5")]


@icon("square-meter", CAT, "Square meter: a lowercase m with a small raised 2.",
      tags=["square meter", "square metre", "m2", "area", "floor area", "unit", "metric"])
def _(S):
    return gl(S, g_m(S, 2, 10, 10.5, 10.5)) + [line(earc(18.5, 6, 2.25, 2.25, 180, 410) + "L16.5 11H21.25")]


@icon("cubic-meter", CAT, "Cubic meter: a lowercase m with a small raised 3.",
      tags=["cubic meter", "cubic metre", "m3", "volume", "capacity", "unit", "metric"])
def _(S):
    return gl(S, g_m(S, 2, 10, 10.5, 10.5)) + [line(earc(18.5, 5.4, 2.25, 2.0, -160, 90) + earc(18.5, 9.4, 2.4, 2.0, -90, 160, move=False))]


@icon("kilogram-unit", CAT, "Kilogram unit: a weight with a handle loop and kg on its face.",
      tags=["kilogram", "kg", "weight", "mass", "unit", "metric", "scale weight"])
def _(S):
    return [shell(poly([(2.5, 20.5), (5.5, 8), (18.5, 8), (21.5, 20.5)], closed=True, r=S.r)),
            line("M9.5 8V5.5A2.5 2.5 0 0 1 14.5 5.5V8"),
            detail(seg(8, 11.5, 8, 18.5)), detail(seg(12, 12.5, 8, 15.5)), detail(seg(9.5, 14.5, 12, 18.5)),
            detail(circle(16, 15.25, 2.25)), detail(seg(18.25, 13, 18.25, 19))]


@icon("watt-unit", CAT, "Watt unit: a capital W beside a small lightning bolt.",
      tags=["watt", "power", "electric power", "wattage", "energy rate", "unit", "si unit"])
def _(S):
    return [line(poly([(2.5, 6), (5.75, 19), (9, 9.5), (12.25, 19), (15.5, 6)], r=S.r, ), stroke_miterlimit="1.5"),
            line(poly([(20.5, 4), (17.5, 12.5), (21.5, 12.5), (18, 21)], r=S.r))]


@icon("volt-unit", CAT, "Volt unit: a capital V inside a circle with plus and minus marks beside it.",
      tags=["volt", "voltage", "electric potential", "potential difference", "unit", "si unit", "v"])
def _(S):
    return [line(circle(9.5, 12, 7.5)), line(poly([(6.5, 9), (9.5, 15.5), (12.5, 9)], r=S.r * 0.5)),
            line(seg(17.5, 6, 21.5, 6)), line(seg(19.5, 4, 19.5, 8)), line(seg(17.5, 18, 21.5, 18))]


@icon("ampere-unit", CAT, "Ampere unit: a capital A inside a circle with an arrow along a wire.",
      tags=["ampere", "amp", "amps", "electric current", "current", "unit", "si unit"])
def _(S):
    return [line(circle(8.75, 12, 7.25))] + gl(S, g_A(S, 5.75, 8, 6, 8, 0.72)) + arrow(S, (16.5, 12), (21.5, 12), 3.2)


@icon("newton-unit", CAT, "Newton force unit: a capital N with a force arrow pushing a small block.",
      tags=["newton", "force", "unit", "si unit", "physics", "push", "n"])
def _(S):
    return [line(poly([(2.5, 18), (2.5, 6), (10.5, 18), (10.5, 6)], r=S.r), stroke_miterlimit="1.5")] + \
        arrow(S, (13.5, 12), (18, 12), 3.2) + [solid(rect(19.5, 8, 2.5, 8))]


@icon("joule-unit", CAT, "Joule energy unit: a capital J beside a small flame.",
      tags=["joule", "energy", "heat", "work", "unit", "si unit", "physics"])
def _(S):
    return [line("M9 4.5V15A4 4 0 0 1 5 19H3.5"),
            shell("M15.5 20.5C12 20.5 11.5 17.5 13 15C14 13.3 13.5 11.5 13 9C16.5 10.5 17 12.5 17 14C18.5 13 19 11.5 19 10C21 12 21.5 15 21 17C20.5 19 18.5 20.5 15.5 20.5Z")]


@icon("imperial-to-metric", CAT, "Ruler with inch marks on top and centimeter marks below, joined by a double arrow.",
      tags=["imperial", "metric", "inches", "centimeters", "unit conversion", "convert units", "measurement"])
def _(S):
    out = [shell(rect(2, 3.5, 20, 17, S.R))]
    for x in (7, 12, 17):
        out.append(detail(seg(x, 4.5, x, 7.5)))
    for x in (6, 10, 14, 18):
        out.append(detail(seg(x, 16.5, x, 19.5)))
    out += [detail(seg(7, 12, 17, 12)), arrow_head(S, (17.5, 12), (13, 12), 2.6, kind=detail), arrow_head(S, (6.5, 12), (11, 12), 2.6, kind=detail)]
    return out


@icon("centerline-symbol", CAT, "Centerline symbol: a capital C overlapping a capital L on one shared stem.",
      tags=["centerline", "center line", "drafting", "engineering drawing", "cl", "axis", "technical drawing"])
def _(S):
    return [line(earc(11, 12, 8, 8.5, -50, -310)), line(poly([(11, 3.5), (11, 20.5), (20, 20.5)], r=S.r))]


@icon("flatness-symbol", CAT, "Flatness tolerance: a slanted parallelogram inside a rectangular frame.",
      tags=["flatness", "gd&t", "geometric tolerance", "engineering drawing", "tolerance frame", "parallelogram", "surface flatness"])
def _(S):
    return [shell(rect(2, 4.5, 20, 15, S.R)),
            detail(poly([(6.5, 15), (9.5, 9), (17.5, 9), (14.5, 15)], closed=True, r=S.r))]


@icon("cylindricity-symbol", CAT, "Cylindricity tolerance: a small circle between two slanted parallel lines.",
      tags=["cylindricity", "gd&t", "geometric tolerance", "engineering drawing", "cylinder", "roundness", "form tolerance"])
def _(S):
    return [line(circle(12, 12, 2.75)), line(seg(8.8, 5, 3.2, 19)), line(seg(20.8, 5, 15.2, 19))]


@icon("concentricity-symbol", CAT, "Concentricity tolerance: two circles sharing one centre.",
      tags=["concentricity", "coaxial", "gd&t", "geometric tolerance", "engineering drawing", "concentric circles", "target"])
def _(S):
    return [line(circle(12, 12, L(S, 8.5, 8))), line(circle(12, 12, L(S, 3.25, 3.5)))]


@icon("position-tolerance-symbol", CAT, "Position tolerance: a circle with a crosshair extending beyond its edge.",
      tags=["position", "true position", "gd&t", "geometric tolerance", "engineering drawing", "crosshair", "location tolerance"])
def _(S):
    return [line(circle(12, 12, 5)), line(seg(12, 2.5, 12, 21.5)), line(seg(2.5, 12, 21.5, 12))]


@icon("total-runout-symbol", CAT, "Total runout tolerance: two slanted arrows joined at their base by a horizontal line.",
      tags=["runout", "total runout", "gd&t", "geometric tolerance", "engineering drawing", "arrows", "rotation tolerance"])
def _(S):
    return [line(seg(6.5, 19.5, 15.5, 19.5))] + arrow(S, (6.5, 19.5), (8.5, 4.5), 3.4, back=1.2) + arrow(S, (15.5, 19.5), (17.5, 4.5), 3.4, back=1.2)


@icon("surface-profile-symbol", CAT, "Surface profile tolerance: a closed dome with a flat base.",
      tags=["surface profile", "profile of a surface", "gd&t", "geometric tolerance", "engineering drawing", "dome", "semicircle"])
def _(S):
    return [shell("M3 16.5A9 9 0 0 1 21 16.5Z")]


@icon("line-profile-symbol", CAT, "Line profile tolerance: an open semicircular arc.",
      tags=["line profile", "profile of a line", "gd&t", "geometric tolerance", "engineering drawing", "arc", "semicircle"])
def _(S):
    return [line("M3 16.5A9 9 0 0 1 21 16.5")]


@icon("angularity-symbol", CAT, "Angularity tolerance: a shallow angle made of a base line and a slanted line.",
      tags=["angularity", "gd&t", "geometric tolerance", "engineering drawing", "acute angle", "orientation tolerance", "slant"])
def _(S):
    return [line(poly([(21, 19), (3, 19), (16, 5)], r=S.r))]


@icon("countersink-symbol", CAT, "Countersink symbol: a wide V shape opening upward.",
      tags=["countersink", "csk", "engineering drawing", "hole callout", "wide v", "screw head", "drafting"])
def _(S):
    return [line(poly([(2.5, 5.5), (12, 15.5), (21.5, 5.5)], r=S.r))]


@icon("counterbore-symbol", CAT, "Counterbore symbol: a square-cornered U opening upward.",
      tags=["counterbore", "cbore", "engineering drawing", "hole callout", "recess", "drafting", "socket head"])
def _(S):
    return [line(poly([(4, 4.5), (4, 19.5), (20, 19.5), (20, 4.5)], r=S.r))]


@icon("depth-symbol", CAT, "Depth symbol: a vertical arrow pointing down at a short horizontal bar.",
      tags=["depth", "deep", "engineering drawing", "hole depth", "drafting", "dimension", "downward arrow"])
def _(S):
    return arrow(S, (12, 3), (12, 15.5), 4.5) + [line(seg(6.5, 20, 17.5, 20))]


@icon("datum-feature-symbol", CAT, "Datum feature: a letter A in a square box joined to a filled triangle on a surface line.",
      tags=["datum", "datum feature", "gd&t", "engineering drawing", "reference surface", "datum a", "drafting"])
def _(S):
    return [shell(rect(6, 2.5, 12, 12, min(S.R, 2))),
            detail(poly([(9.25, 12), (12, 5), (14.75, 12)], r=S.r * 0.5)), detail(seg(10.3, 10, 13.7, 10)),
            solid(poly([(12, 15.5), (8, 20.5), (16, 20.5)], closed=True)), line(seg(2.5, 21, 21.5, 21))]


@icon("feature-control-frame", CAT, "Feature control frame: a long rectangle divided into three cells.",
      tags=["feature control frame", "fcf", "gd&t", "tolerance frame", "engineering drawing", "geometric tolerance", "callout"])
def _(S):
    return [shell(rect(2, 6, 20, 12, S.R)),
            detail(seg(8.5, 7, 8.5, 17)), detail(seg(14.5, 7, 14.5, 17)),
            dot(5.25, 12, 1.4), detail(seg(10.5, 12, 12.5, 12)), detail(poly([(17, 14.5), (18.75, 9.5), (20.5, 14.5)], r=0))]


@icon("surface-finish-symbol", CAT, "Surface texture symbol: a check-mark shape with an extended right leg and a top bar.",
      tags=["surface finish", "surface texture", "roughness", "machining symbol", "engineering drawing", "ra", "drafting"])
def _(S):
    return [line(poly([(2.5, 12.5), (6.5, 19), (13.5, 5), (21.5, 5)], r=S.r))]


@icon("fillet-weld-symbol", CAT, "Fillet weld symbol: a small right triangle under a reference line with an arrow leading off.",
      tags=["fillet weld", "weld symbol", "welding", "engineering drawing", "reference line", "drafting", "joint"])
def _(S):
    return [line(seg(8.5, 9, 21.5, 9)), solid(poly([(11.5, 9.5), (11.5, 16), (18, 9.5)], closed=True))] + \
        arrow(S, (8.5, 9), (3.5, 19), 4)


@icon("first-angle-projection", CAT, "First angle projection symbol: a truncated cone beside two concentric circles.",
      tags=["first angle projection", "projection symbol", "orthographic", "engineering drawing", "drafting", "cone", "view layout"])
def _(S):
    return [shell(poly([(2.5, 4.5), (2.5, 19.5), (10, 16), (10, 8)], closed=True, r=S.r)),
            line(circle(17.5, 12, 3.75)), dot(17.5, 12, 1.25)]


@icon("section-view-symbol", CAT, "Section cutting plane line: dashes with heavy ends and arrows showing view direction.",
      tags=["section view", "cutting plane", "section line", "engineering drawing", "drafting", "cut", "view direction"])
def _(S):
    return [line(seg(5, 13, 5, 19)), line(seg(19, 13, 19, 19)),
            line(seg(8.5, 16, 11, 16)), line(seg(13, 16, 15.5, 16))] + arrow(S, (5, 13), (5, 3.5), 3.6) + arrow(S, (19, 13), (19, 3.5), 3.6)


@icon("thread-callout", CAT, "Screw thread callout: a leader arrow pointing at a threaded rod, labelled M.",
      tags=["thread callout", "screw thread", "metric thread", "m8", "engineering drawing", "hole callout", "drafting"])
def _(S):
    return [shell(rect(14, 2.5, 8, 15, min(S.R, 2))), detail(seg(14.5, 7.5, 21.5, 5)), detail(seg(14.5, 12, 21.5, 9.5)),
            detail(seg(14.5, 16.5, 21.5, 14))] + \
        arrow(S, (6.5, 12), (11.2, 10.5), 3) + [line(poly([(2.5, 21), (2.5, 15.5), (6.5, 19.5), (10.5, 15.5), (10.5, 21)], r=S.r * 0.6), stroke_miterlimit="1.5")]


@icon("radius-callout", CAT, "Radius callout: a rounded corner with a leader line labelled R.",
      tags=["radius callout", "fillet radius", "corner radius", "engineering drawing", "drafting", "dimension", "r label"])
def _(S):
    return [line("M3 21V11A8 8 0 0 1 11 3H21")] + arrow(S, (13, 13), (5.8, 5.8), 3.6) + gl(S, g_R(S, 15.5, 13.5, 5, 7.5, 4))


@icon("weld-all-around", CAT, "Weld all around symbol: a reference line with a small circle at the arrow joint.",
      tags=["weld all around", "weld symbol", "welding", "engineering drawing", "circle symbol", "drafting", "joint"])
def _(S):
    return [line(seg(9, 9, 21.5, 9)), line(circle(9, 9, 3))] + arrow(S, (7.2, 11.5), (3.5, 19), 4)
