"""TypeIcon Core: holidays & celebrations.

Celebration icons get the minimal badge set (plus, minus, check, x, off) in the bottom-right corner.
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, P, ST, U, arc, circle, detail, dot, ellipse, filled_region, icon, line, path_to_d, poly, pt_on, rect, regular,
    seg, shell, solid,
)
from geometry import LINE, SCALE, fmt

CAT = "celebration"


# --------------------------------------------------------------------------- helpers

def rnd(S, line_val, rounded_val):
    return line_val if S.name == "line" else rounded_val


def pts_d(pts):
    return "".join(("M" if i == 0 else "L") + f"{fmt(x)} {fmt(y)}" for i, (x, y) in enumerate(pts))


def rot(pts, deg, cx=12.0, cy=12.0):
    """Rotate points clockwise on screen by deg about (cx, cy)."""
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in pts]


def outside(region, p0, p1, n=240):
    """Runs of the segment p0-p1 that lie outside a pathops region (grid units)."""
    runs, cur = [], []
    for i in range(n + 1):
        t = i / n
        p = (p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t)
        if region.contains((p[0] * SCALE, p[1] * SCALE)):
            if len(cur) > 1:
                runs.append((cur[0], cur[-1]))
            cur = []
        else:
            cur.append(p)
    if len(cur) > 1:
        runs.append((cur[0], cur[-1]))
    return runs


def flame(x, y_tip, h=3.2, w=1.6):
    """Small teardrop flame, tip at (x, y_tip)."""
    yb = y_tip + h
    return (f"M{fmt(x)} {fmt(y_tip)}C{fmt(x + w * 0.4)} {fmt(y_tip + h * 0.35)} {fmt(x + w)} {fmt(y_tip + h * 0.55)} "
            f"{fmt(x + w)} {fmt(yb - w)}A{fmt(w)} {fmt(w)} 0 0 1 {fmt(x - w)} {fmt(yb - w)}"
            f"C{fmt(x - w)} {fmt(y_tip + h * 0.55)} {fmt(x - w * 0.4)} {fmt(y_tip + h * 0.35)} {fmt(x)} {fmt(y_tip)}Z")


def star_pts(cx, cy, ro, ri, n=5, start=-90.0):
    return [pt_on(cx, cy, ro if i % 2 == 0 else ri, start + i * 180 / n) for i in range(2 * n)]


# =========================================================================== icons

@icon("birthday-cake", CAT, "Birthday cake with icing and three lit candles",
      tags=["birthday", "cake", "party", "candles", "anniversary", "celebrate"])
def _(S):
    icing = "M4 16C5.3 16 5.3 17.5 6.67 17.5S8 16 9.33 16S10.67 17.5 12 17.5S13.33 16 14.67 16S16 17.5 17.33 17.5S18.7 16 20 16"
    parts = [shell(rect(4, 12, 16, 9, S.R * 0.75)), detail(icing)]
    for x in (8, 12, 16):
        parts += [line(seg(x, 9, x, 12)), solid(flame(x, 3.75))]
    return parts


@icon("fireworks", CAT, "Two firework bursts in the sky", tags=["firework", "new year", "celebration", "burst", "sparkle", "festival"])
def _(S):
    parts = []
    for i in range(8):
        a = -90 + i * 45
        r0, r1 = (3, 7.5) if i % 2 == 0 else (3.25, 6.5)
        parts.append(line(seg(*pt_on(14, 9.5, r0, a), *pt_on(14, 9.5, r1, a))))
    parts += [line(seg(*pt_on(6, 17.5, 1.5, a), *pt_on(6, 17.5, 3.75, a))) for a in (-90, 0, 90, 180)]
    return parts + [dot(14, 9.5, 1.1)]


@icon("christmas-tree", CAT, "Christmas tree with a star on top and baubles", tags=["xmas", "christmas", "holiday", "fir", "noel", "december"],
      aliases=["xmas-tree"])
def _(S):
    tree = [(12, 6), (15.5, 10), (14, 10), (17.5, 14), (16, 14), (19.5, 18.5), (4.5, 18.5), (8, 14), (6.5, 14), (10, 10), (8.5, 10)]
    return [shell(poly(tree, closed=True, r=S.r * 0.4)), line(seg(12, 18.5, 12, 21.5)),
            solid(poly(star_pts(12, 3.6, 2.5, 1.05), closed=True)), dot(10, 15.75, 1.1), dot(12.75, 12.25, 1.1)]


_PUMPKIN = ellipse(12, 13.5, 9, 7)
_EYES = ([(6.75, 12.25), (10.25, 12.25), (8.5, 9.25)], [(13.75, 12.25), (17.25, 12.25), (15.5, 9.25)])
_MOUTH = [(6.5, 15), (8.5, 17.5), (10.25, 15.75), (12, 17.5), (13.75, 15.75), (15.5, 17.5), (17.5, 15)]


def _pumpkin_filled():
    body = U(P(ellipse(12, 13.5, 10, 8)), ST(poly([(12, 6.5), (12.25, 4.5), (14.5, 3.25)]), 2.5))
    return D(body, *[P(poly(e, closed=True)) for e in _EYES], ST(poly(_MOUTH), 2.0))


@icon("pumpkin-halloween", CAT, "Carved jack-o'-lantern pumpkin", tags=["halloween", "jack-o-lantern", "pumpkin", "spooky", "october", "autumn"],
      aliases=["jack-o-lantern"], filled=_pumpkin_filled)
def _(S):
    return [shell(_PUMPKIN), line(poly([(12, 6.5), (12.25, 4.5), (14.5, 3.25)], r=S.r * 0.5)),
            *[solid(poly(e, closed=True)) for e in _EYES], line(poly(_MOUTH, r=S.r * 0.4))]


@icon("candle", CAT, "Lit pillar candle", tags=["flame", "light", "memorial", "advent", "wax", "candlelight"])
def _(S):
    fl = "M12 3C13.6 4.8 14.5 5.9 14.5 7A2.5 2.5 0 0 1 9.5 7C9.5 5.9 10.4 4.8 12 3Z" if S.name == "rounded" else \
        "M12 3L14.5 6.75A2.5 2.5 0 0 1 9.5 6.75Z"
    return [shell(fl, stroke_miterlimit="2"), line(seg(12, 9.5, 12, 12)), shell(rect(8, 12, 8, 9, S.R * 0.5)),
            detail(seg(10.75, 14.5, 10.75, 17.5))]


_MEN_W = (8.5, 5.5, 2.5)
_MEN_X = (3.5, 6.5, 9.5, 12, 14.5, 17.5, 20.5)


def _menorah_arm(w):
    return f"M{fmt(12 - w)} 8V10A{fmt(w)} {fmt(w)} 0 0 0 {fmt(12 + w)} 10V8"


def _menorah_filled():
    arms = [ST(_menorah_arm(w), 2.0) for w in _MEN_W]
    flames = [P(flame(x, 2.75, h=3.5, w=1.25)) for x in _MEN_X]
    return U(*arms, ST(seg(12, 7.5, 12, 20), 2.5), P(rect(7, 19, 10, 3, 0.5)), *flames)


@icon("menorah", CAT, "Seven-branched menorah with flames", tags=["hanukkah", "chanukah", "jewish", "candelabrum", "festival of lights", "judaism"],
      aliases=["hanukkah"], filled=_menorah_filled)
def _(S):
    parts = [line(seg(12, 8, 12, 20.5)), line(seg(7.5, 20.5, 16.5, 20.5))]
    for w in _MEN_W:
        parts.append(line(_menorah_arm(w)))
    for x in _MEN_X:
        parts.append(solid(flame(x, 3.25, h=3, w=1.1)))
    return parts


@icon("lantern", CAT, "Round paper lantern with ribs and a tassel", tags=["paper lantern", "chinese new year", "lunar new year", "festival", "ramadan", "light"])
def _(S):
    return [shell(ellipse(12, 12, 8.5, 6.5)), detail(ellipse(12, 12, 3.75, 6.2)),
            line(seg(8.5, 4.5, 15.5, 4.5)), line(seg(8.5, 19.5, 15.5, 19.5)), line(seg(12, 2.5, 12, 4.5)), line(seg(12, 19.5, 12, 22))]


@icon("easter-egg", CAT, "Decorated Easter egg with a zigzag band", tags=["easter", "egg", "spring", "paschal", "hunt", "painted egg"])
def _(S):
    egg = "M12 3C8.2 3 5 8.8 5 13.8A7 7 0 0 0 19 13.8C19 8.8 15.8 3 12 3Z"
    zig = [(5.4, 11), (7.6, 13), (9.8, 11), (12, 13), (14.2, 11), (16.4, 13), (18.6, 11)]
    return [shell(egg), detail(poly(zig, r=S.r * 0.4)), dot(9, 16.5, 1.1), dot(12, 17.25, 1.1), dot(15, 16.5, 1.1)]


_HEART = ("M12 18.5C7 15.3 4.75 12.6 4.75 10C4.75 7.9 6.4 6.25 8.5 6.25C10 6.25 11.3 7.1 12 8.4"
          "C12.7 7.1 14 6.25 15.5 6.25C17.6 6.25 19.25 7.9 19.25 10C19.25 12.6 17 15.3 12 18.5Z")


def _cupid_arrow():
    guard = U(P(_HEART), ST(_HEART, 5.0))
    return outside(guard, (3.5, 20.5), (19, 5))


@icon("valentine", CAT, "Heart pierced by Cupid's arrow", tags=["valentines day", "love", "cupid", "romance", "heart", "february"],
      aliases=["cupid"])
def _(S):
    parts = [shell(_HEART, stroke_miterlimit="8")]
    for a, b in _cupid_arrow():
        parts.append(line(seg(*a, *b)))
    parts.append(line(poly([(15.5, 4.5), (20, 4), (19.5, 8.5)], r=S.r * 0.5)))
    return parts


def _ring_arcs():
    r, g = 5.5, math.degrees(2 * math.asin(3.5 / (2 * 5.5)))
    top = math.degrees(math.atan2(-4.61, 3))       # left ring, crossing where the right ring passes over
    bot = math.degrees(math.atan2(4.61, -3))       # right ring, crossing where it passes under
    return [arc(9, 14.5, r, top + g / 2, top - g / 2 + 360), arc(15, 14.5, r, bot + g / 2, bot - g / 2 + 360)]


@icon("wedding-ring", CAT, "Two interlocked wedding rings with a diamond", tags=["wedding", "marriage", "engagement", "rings", "bride", "anniversary"],
      aliases=["wedding-rings"])
def _(S):
    gem = [(6.75, 5.5), (8, 4), (10, 4), (11.25, 5.5), (9, 8)]
    return [*[line(a) for a in _ring_arcs()], shell(poly(gem, closed=True, r=S.r * 0.3), stroke_miterlimit="2")]


@icon("champagne", CAT, "Champagne bottle with the cork popping", tags=["cheers", "toast", "celebrate", "sparkling wine", "new year", "party"],
      aliases=["champagne-bottle"])
def _(S):
    bottle = [(10.75, 8.5), (13.25, 8.5), (13.25, 11), (16, 13.75), (16, 21), (8, 21), (8, 13.75), (10.75, 11)]
    cork = [(10.25, 3.25), (13.25, 2.75), (13.6, 5.25), (10.6, 5.75)]
    return [shell(poly(bottle, closed=True, r=S.r * 0.66)), detail(seg(8, 16, 16, 16)), detail(seg(8, 19.25, 16, 19.25)),
            shell(poly(cork, closed=True, r=S.r * 0.3)),
            line(seg(7.5, 4.5, 5.5, 3.5)), line(seg(7.5, 7.5, 5.5, 8.5)), line(seg(16.5, 5, 18.5, 4)), line(seg(16.5, 8, 18.5, 9))]


@icon("party-hat", CAT, "Cone party hat with a pompom", tags=["party", "birthday", "celebration", "hat", "cone", "festive"])
def _(S):
    cone = [(12, 6.5), (18.5, 19.5), (5.5, 19.5)]
    return [shell(poly(cone, closed=True, r=S.r * 0.66)), shell(circle(12, 4, rnd(S, 1.6, 1.75))),
            dot(11.5, 12.5, 1.1), dot(14, 16.25, 1.1), dot(9.5, 16.5, 1.1)]


@icon("gift-box", CAT, "Wrapped gift box with a ribbon and bow", tags=["present", "gift", "birthday", "christmas", "surprise", "wrapped"],
      )
def _(S):
    bow_l = "M12 8C10.5 4.5 6.5 3.5 6.5 6C6.5 7.5 8.5 8 12 8Z"
    bow_r = "M12 8C13.5 4.5 17.5 3.5 17.5 6C17.5 7.5 15.5 8 12 8Z"
    return [shell(rect(3, 8, 18, 4.5, S.R * 0.5)), shell(rect(4.5, 12.5, 15, 8.5, S.R * 0.5)),
            detail(seg(4, 12.5, 20, 12.5)), detail(seg(12, 8, 12, 21)),
            shell(bow_l, stroke_miterlimit="2"), shell(bow_r, stroke_miterlimit="2")]


_RIB_A = ((5.5, 21), (16, 8.5))     # strand passing over
_RIB_B = ((8, 8.5), (18.5, 21))     # strand passing under
_RIB_LOOP = "C18 5.8 16.5 3 12 3C7.5 3 6 5.8 8 8.5"


@icon("ribbon", CAT, "Looped awareness ribbon", tags=["awareness", "support", "cause", "charity", "campaign", "solidarity"],
      aliases=["awareness-ribbon"])
def _(S):
    (a0, a1), (b0, b1) = _RIB_A, _RIB_B
    main = f"M{fmt(a0[0])} {fmt(a0[1])}L{fmt(a1[0])} {fmt(a1[1])}{_RIB_LOOP}L{fmt(b1[0])} {fmt(b1[1])}"
    return [line(main, stroke_miterlimit="2")]


@icon("bell-christmas", CAT, "Christmas bell tied with a bow", tags=["christmas", "jingle", "xmas", "holiday", "bell", "chime"],
      aliases=["christmas-bell"])
def _(S):
    bell = "M4.5 19C6.5 18 6.5 16 6.8 14C7.3 11 9.3 9.5 12 9.5C14.7 9.5 16.7 11 17.2 14C17.5 16 17.5 18 19.5 19Z"
    bow_l = "M12 6.5C10.5 4 7 3.5 7 5.5C7 7 9.5 7 12 6.5Z"
    bow_r = "M12 6.5C13.5 4 17 3.5 17 5.5C17 7 14.5 7 12 6.5Z"
    return [shell(bell, stroke_miterlimit="2"), line(seg(12, 6.5, 12, 9.5)),
            shell(bow_l, stroke_miterlimit="2"), shell(bow_r, stroke_miterlimit="2"), dot(12, 21, 1.5)]


def _globe_d():
    r, cy = 7.5, 9.75
    dy = 16 - cy
    dx = math.sqrt(r * r - dy * dy)
    return f"M{fmt(12 - dx)} 16A{fmt(r)} {fmt(r)} 0 1 1 {fmt(12 + dx)} 16Z"


@icon("snowglobe", CAT, "Snow globe with a little tree inside", tags=["snow globe", "winter", "christmas", "souvenir", "snow", "decoration"],
      aliases=["snow-globe"])
def _(S):
    base = [(6.5, 16), (17.5, 16), (19, 21), (5, 21)]
    return [shell(_globe_d()), shell(poly(base, closed=True, r=S.r * 0.5)), detail(seg(6.5, 16, 17.5, 16)),
            detail(poly([(12, 7.5), (15, 13), (9, 13)], closed=True, r=S.r * 0.4)), dot(8.25, 8, 1), dot(15.75, 7, 1), dot(16.5, 11.25, 1)]


_WC = (12.0, 11.25)
_BOW = ("M12 18.75C10.3 16.7 7.25 16.4 7.25 18.4C7.25 19.9 9.8 19.8 12 18.75Z",
        "M12 18.75C13.7 16.7 16.75 16.4 16.75 18.4C16.75 19.9 14.2 19.8 12 18.75Z")
_BOW_TAILS = (seg(11, 19.5, 9.75, 21.75), seg(13, 19.5, 14.25, 21.75))


def _bow_guard(gap=1.5):
    parts = [P(b) for b in _BOW] + [ST(b, 2.0) for b in _BOW] + [ST(t, 2.0) for t in _BOW_TAILS]
    body = U(*parts)
    return U(body, ST(path_to_d(body), 2 * (gap + 1)))


def _wreath_ticks():
    cx, cy = _WC
    return [seg(*pt_on(cx, cy, 4.9, a - 16), *pt_on(cx, cy, 7.6, a + 16)) for a in range(-90, 30, 30)] + \
           [seg(*pt_on(cx, cy, 4.9, a - 16), *pt_on(cx, cy, 7.6, a + 16)) for a in range(150, 270, 30)]


def _circle_runs(cx, cy, r, guard, n=180):
    pts = [pt_on(cx, cy, r, 90 + 360 * i / n) for i in range(n + 1)]
    runs, cur = [], []
    for p in pts:
        if guard.contains((p[0] * SCALE, p[1] * SCALE)):
            if len(cur) > 1:
                runs.append(cur)
            cur = []
        else:
            cur.append(p)
    if len(cur) > 1:
        runs.append(cur)
    return runs


def _wreath_filled():
    cx, cy = _WC
    ring = D(P(circle(cx, cy, 9.5)), P(circle(cx, cy, 3.25)), *[ST(t, 1.5) for t in _wreath_ticks()], _bow_guard(1.0))
    bow = U(*[U(P(b), ST(b, 2.0)) for b in _BOW], *[ST(t, 2.5) for t in _BOW_TAILS])
    return U(ring, bow)


@icon("wreath", CAT, "Holiday wreath of twisted greenery tied with a bow", tags=["christmas", "garland", "advent", "door", "holly", "xmas"],
      aliases=["christmas-wreath"], filled=_wreath_filled)
def _(S):
    cx, cy = _WC
    guard = _bow_guard()
    parts = [line(pts_d(r)) for r in _circle_runs(cx, cy, 8.5, guard)] + [line(circle(cx, cy, 4.25))]
    parts += [line(t) for t in _wreath_ticks()]
    return parts + [shell(b, stroke_miterlimit="2") for b in _BOW] + [line(t) for t in _BOW_TAILS]
