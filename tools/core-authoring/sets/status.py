"""TypeIcon Core: alerts & status."""
import math

from dsl import (  # noqa: F401
    LINE, arc, circle, detail, dot, ellipse, filled_region, icon, line, poly, pt_on, rect, regular, seg, shell, solid,
)
from geometry import D, P, ST, U, fmt, path_to_d, polar

CAT = "status"


# --------------------------------------------------------------------------- local helpers

def P2(x, y):
    return f"{fmt(x)} {fmt(y)}"


def octagon(cx, cy, r):
    """Regular octagon with flat top, circumradius r."""
    return regular(cx, cy, r, 8, start=-90 + 22.5)


def dashed_ring(S, cx, cy, r, n, gap):
    """n arcs on a circle leaving `gap` px of visible space between dashes in both styles."""
    circ = 2 * math.pi * r
    cap = 1.0 if S.name == "rounded" else 0.0  # round caps reach 1 px past each end
    step = 360 / n
    half_gap_deg = (gap / 2 + cap) / circ * 360
    return [line(arc(cx, cy, r, -90 + i * step + half_gap_deg, -90 + (i + 1) * step - half_gap_deg)) for i in range(n)]


CHECK = [(8, 12.25), (11, 15.25), (16.25, 9)]


def person(S, hx=8.5, hy=9.0, hr=3.5, x0=2.5, x1=14.5, top=14.5, bottom=21.0):
    """Head and shoulders, shifted left so a status indicator fits at the top right."""
    rr = 4.5 if S.name == "line" else 5.5
    body = (f"M{P2(x0, bottom)}V{fmt(top + rr)}A{fmt(rr)} {fmt(rr)} 0 0 1 {P2(x0 + rr, top)}"
            f"H{fmt(x1 - rr)}A{fmt(rr)} {fmt(rr)} 0 0 1 {P2(x1, top + rr)}V{fmt(bottom)}")
    return [shell(circle(hx, hy, hr)), line(body)]


IND = (18.25, 5.75)  # status indicator centre
IND_R = 3.5


def bell_body(cx=12.0, top=4.5, w=6.0, bottom=16.5, flare=1.5):
    return (f"M{P2(cx - w, bottom)}V{fmt(top + w)}A{fmt(w)} {fmt(w)} 0 0 1 {P2(cx + w, top + w)}V{fmt(bottom)}"
            f"L{P2(cx + w + flare, bottom + 2)}H{fmt(cx - w - flare)}Z")


# ============================================================================ alerts

@icon("alert-circle", CAT, "Exclamation mark in a circle; an alert or error notice.",
      tags=["alert", "error", "attention", "exclamation", "important", "notice"], aliases=["exclamation-circle"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(seg(12, 7, 12, 13)), dot(12, 16.5, 1.3)]


@icon("alert-octagon", CAT, "Exclamation mark in an octagon; a critical error or stop warning.",
      tags=["critical", "error", "danger", "stop", "exclamation", "alert"], aliases=["exclamation-octagon"])
def _(S):
    return [shell(poly(octagon(12, 12, 9.6), closed=True, r=S.r)), detail(seg(12, 7, 12, 13)), dot(12, 16.5, 1.3)]


@icon("ban", CAT, "Circle with a diagonal bar; banned, blocked or not allowed.",
      tags=["ban", "blocked", "forbidden", "prohibited", "not allowed", "deny"], aliases=["prohibited", "forbidden"])
def _(S):
    a, b = polar(12, 12, 9, 225), polar(12, 12, 9, 45)
    if S.name == "rounded":
        # Rounded: the bar floats inside the ring with round ends.
        a, b = polar(12, 12, 5.25, 225), polar(12, 12, 5.25, 45)
    return [shell(circle(12, 12, 9)), detail(seg(*a, *b))]


@icon("stop-sign", CAT, "Octagonal stop sign on a post.",
      tags=["stop", "halt", "traffic sign", "road sign", "end", "stop sign"])
def _(S):
    return [shell(poly(octagon(12, 9.5, 7), closed=True, r=S.r * 0.8)),
            detail(seg(8.75, 9.5, 15.25, 9.5)),
            line(seg(12, 16.5, 12, 22))]


@icon("loader-circle", CAT, "Three-quarter circular arc; loading or in progress.",
      tags=["loading", "spinner", "progress", "wait", "busy", "pending"], aliases=["loading"])
def _(S):
    return [line(arc(12, 12, 9, -90, 180)), dot(*polar(12, 12, 9, 214), 1.1), dot(*polar(12, 12, 9, 243), 1.1)]


@icon("bell-ring", CAT, "Bell with ringing marks on both sides; an active alert.",
      tags=["ringing", "alarm", "notification", "alert", "reminder", "bell"], aliases=["bell-ringing"])
def _(S):
    return [shell(bell_body(12, 5, 5.25, 16, 1.5)), line(seg(10, 20.5, 14, 20.5)),
            line(arc(12, 10.25, 9, 195, 240)), line(arc(12, 10.25, 9, 300, 345))]


def _badge_draw(S):
    c, r = (18, 6), 3.25
    body = rect(3, 6, 15, 15, S.R * 0.75)
    return [shell(body), dot(*c, r)]


def _clip_rect_d(S, c, keep_r):
    """Rounded-square outline, as an open path, with the part near c removed."""
    x0, y0, x1, y1 = 3, 6, 18, 21
    R = S.R * 0.75
    # Start where the top edge leaves the clearance circle, run anticlockwise round to the right edge.
    xt = c[0] - math.sqrt(max(0.0, keep_r ** 2 - (y0 - c[1]) ** 2))
    yr = c[1] + math.sqrt(max(0.0, keep_r ** 2 - (x1 - c[0]) ** 2))
    return (f"M{P2(xt, y0)}H{fmt(x0 + R)}A{fmt(R)} {fmt(R)} 0 0 0 {P2(x0, y0 + R)}V{fmt(y1 - R)}"
            f"A{fmt(R)} {fmt(R)} 0 0 0 {P2(x0 + R, y1)}H{fmt(x1 - R)}A{fmt(R)} {fmt(R)} 0 0 0 {P2(x1, y1 - R)}"
            f"V{fmt(yr)}")


def _badge_filled():
    c, r = (18, 6), 3.25
    body = P(rect(2, 5, 17, 17, 1.5))
    return U(D(body, P(circle(*c, r + 1.75))), P(circle(*c, r)))


@icon("badge-status", CAT, "Rounded square with a dot at its corner; an unread badge or status marker.",
      tags=["badge", "notification dot", "unread", "status", "indicator", "new"], filled=_badge_filled)
def _(S):
    c, r = (18, 6), 3.25
    return [line(_clip_rect_d(S, c, r + 3)), dot(*c, r)]


@icon("flag-status", CAT, "Triangular pennant on a pole; flagged or marked for attention.",
      tags=["flagged", "pennant", "marker", "priority", "follow up", "status"], aliases=["pennant"])
def _(S):
    return [line(seg(5.5, 22, 5.5, 2.5)),
            shell(poly([(5.5, 3), (19.5, 8.25), (5.5, 13.5)], closed=True, r=S.r * 0.6), stroke_miterlimit="2.5")]


# ============================================================================ circles

def _ccd_filled():
    ring = U(*(ST(p.d, 2.5, "butt") for p in dashed_ring(LINE, 12, 12, 9.25, 8, 2.75)))
    return U(ring, D(P(circle(12, 12, 6.5)), ST(poly(CHECK), 2)))


@icon("circle-check-dashed", CAT, "Check mark inside a dashed circle; a pending or partial completion.",
      tags=["pending", "draft", "check", "optional", "partial", "complete"], filled=_ccd_filled)
def _(S):
    return [*dashed_ring(S, 12, 12, 9, 8, 2.75), line(poly(CHECK, r=S.r))]


@icon("circle-dashed", CAT, "Dashed circle; an empty, draft or not-started state.",
      tags=["dashed", "empty", "draft", "not started", "placeholder", "todo"])
def _(S):
    return dashed_ring(S, 12, 12, 9, 10, 2.75)


@icon("circle-dot", CAT, "Circle with a dot at its centre; selected or active state.",
      tags=["selected", "active", "record", "target", "point", "radio"])
def _(S):
    return [shell(circle(12, 12, 9)), dot(12, 12, 3.5 if S.name == "rounded" else 3)]


def _half_draw(S):
    r = 5.75
    if S.name == "rounded":
        f = 1.5
        half = (f"M{P2(12, 12 - r)}V{fmt(12 + r)}A{r} {r} 0 0 1 {P2(12 - r, 12)}A{r} {r} 0 0 1 {P2(12, 12 - r)}Z")
        half = (f"M{P2(12, 12 - r + f)}V{fmt(12 + r - f)}Q{P2(12, 12 + r)} {P2(12 - f, 12 + r - 0.2)}"
                f"A{r} {r} 0 0 1 {P2(12 - f, 12 - r + 0.2)}Q{P2(12, 12 - r)} {P2(12, 12 - r + f)}Z")
    else:
        half = f"M{P2(12, 12 - r)}V{fmt(12 + r)}A{r} {r} 0 0 1 {P2(12, 12 - r)}Z"
    return [shell(circle(12, 12, 9)), solid(half)]


def _half_filled():
    return D(P(circle(12, 12, 10)), P(f"M{P2(12, 6.25)}V17.75A5.75 5.75 0 0 0 12 6.25Z"))


@icon("circle-half", CAT, "Circle half filled; half done, contrast or partial state.",
      tags=["half", "partial", "contrast", "50 percent", "in progress", "theme"], filled=_half_filled)
def _(S):
    return _half_draw(S)


# ============================================================================ presence

def _moon():
    c, r = IND, IND_R
    return path_to_d(D(P(circle(*c, r)), P(circle(c[0] + 2, c[1] - 1.6, r * 0.8))))


def _busy():
    c, r = IND, IND_R
    return path_to_d(D(P(circle(*c, r)), P(rect(c[0] - 2.1, c[1] - 0.75, 4.2, 1.5))))


@icon("status-online", CAT, "Person with a solid dot; online or available.",
      tags=["online", "available", "active", "presence", "present", "status"], aliases=["available"])
def _(S):
    return [*person(S), dot(*IND, IND_R)]


@icon("status-offline", CAT, "Person with an empty ring; offline or invisible.",
      tags=["offline", "invisible", "unavailable", "away", "presence", "status"])
def _(S):
    return [*person(S), line(circle(*IND, IND_R - 1))]


@icon("status-busy", CAT, "Person with a no-entry dot; busy or do not disturb.",
      tags=["busy", "do not disturb", "dnd", "occupied", "presence", "status"], aliases=["do-not-disturb"])
def _(S):
    return [*person(S), solid(_busy())]


@icon("status-away", CAT, "Person with a crescent moon; away or idle.",
      tags=["away", "idle", "inactive", "afk", "presence", "status"], aliases=["idle"])
def _(S):
    return [*person(S), solid(_moon())]


# ============================================================================ progress & protection

@icon("progress-check", CAT, "Check mark inside a three-quarter progress ring; step complete, more to go.",
      tags=["progress", "complete", "step done", "milestone", "check", "partial"])
def _(S):
    return [line(arc(12, 12, 9, -90, 180)), line(poly(CHECK, r=S.r))]


_SHIELD = "M12 2.5L20 5.5V11C20 16 16.6 19.8 12 21.5C7.4 19.8 4 16 4 11V5.5Z"
_SHIELD_R = ("M10.95 2.9L5.05 5.1Q4 5.5 4 6.6V11C4 16 7.4 19.8 12 21.5C16.6 19.8 20 16 20 11V6.6"
             "Q20 5.5 18.95 5.1L13.05 2.9Q12 2.5 10.95 2.9Z")


@icon("shield-status", CAT, "Shield with a pulse line; system health or protection status.",
      tags=["health", "protection", "security status", "monitoring", "pulse", "uptime"], aliases=["shield-pulse"])
def _(S):
    pulse = [(6.5, 11.5), (9, 11.5), (10.5, 8.5), (13.5, 14.5), (15, 11.5), (17.5, 11.5)]
    return [shell(_SHIELD if S.name == "line" else _SHIELD_R), detail(poly(pulse, r=S.r * 0.4))]
