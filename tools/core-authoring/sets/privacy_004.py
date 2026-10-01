"""TypeIcon Core: privacy, cyber attacks, authentication and cryptography (batch 004)."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "privacy"


def _pick(S, sharp, soft):
    return sharp if S.name == "line" else soft


def dashed_rect(x, y, w, h, dash=3.0, gap=3.5):
    """Dashes walking clockwise around a rectangle, bending at the corners."""
    pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]
    segs = []
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        segs.append((ax, ay, bx, by, math.hypot(bx - ax, by - ay)))
    total = sum(s[4] for s in segs)

    def at(t):
        t = t % total
        for ax, ay, bx, by, L in segs:
            if t <= L:
                f = t / L
                return ax + (bx - ax) * f, ay + (by - ay) * f
            t -= L
        return pts[0]

    def corners_between(t0, t1):
        acc, out = 0.0, []
        for ax, ay, bx, by, L in segs:
            acc += L
            if t0 < acc < t1:
                out.append((bx, by))
        return out

    n = int(total // (dash + gap))
    step = total / n
    d = ""
    for i in range(n):
        t0 = i * step + gap / 2
        t1 = t0 + dash
        p = [at(t0)] + corners_between(t0, t1) + [at(t1)]
        d += "M" + "L".join(f"{fmt(a)} {fmt(b)}" for a, b in p)
    return d


@icon("book-cipher", CAT, "Open book with one word circled and a row of number dots beneath it.",
      tags=["book cipher", "code book", "secret code", "cryptography", "encryption", "cipher", "word code"])
def _(S):
    return [shell(poly([(3, 3.5), (12, 5.5), (21, 3.5), (21, 16), (12, 18), (3, 16)], closed=True, r=S.r)),
            detail("M12 5.5V18"),
            line(ellipse(7.5, 9.5, 2.5, 1.5)),
            detail("M15 8.5H18.5"),
            detail("M15 12H18.5"),
            dot(6, 20.8, 1), dot(9.5, 20.8, 1), dot(14.5, 20.8, 1), dot(18, 20.8, 1)]


@icon("cipher-grille", CAT, "Card with rectangular holes cut in it so only some letters show through.",
      tags=["cipher grille", "cardan grille", "stencil code", "cryptography", "secret message", "mask", "hidden text"])
def _(S):
    return [shell(rect(3.5, 3, 17, 18, _pick(S, 0.5, 3))),
            detail(rect(6.5, 6, 7, 3, _pick(S, 0, 1))),
            detail(rect(10.5, 13, 7, 3, _pick(S, 0, 1)))]


@icon("safe-exchange-zone", CAT, "Signpost with a two-way arrow panel and a security camera on top of the post.",
      tags=["safe exchange", "meetup spot", "monitored", "camera", "signpost", "safe trade", "surveillance"])
def _(S):
    return [line("M10 5.5V8.5"), line("M10 20V22"),
            shell(rect(4.5, 2, 9, 3.5, _pick(S, 0.5, 1.5))),
            shell(poly([(13.5, 3.75), (18, 2), (18, 5.5)], closed=True, r=S.r)),
            shell(rect(3, 8.5, 18, 11.5, _pick(S, 0.5, 2.5))),
            detail("M7 12.6H16.5M15 11.3L16.5 12.6L15 13.9"),
            detail("M17 16H7.5M9 14.7L7.5 16L9 17.3")]


@icon("card-cloning", CAT, "Solid access card with an arrow copying it to a dashed duplicate card.",
      tags=["card cloning", "skimming", "copy card", "duplicate", "rfid clone", "badge copy", "access card"])
def _(S):
    return [shell(rect(2, 3, 13, 8, _pick(S, 0.5, 2))),
            detail("M2 6.5H15"),
            line(dashed_rect(9, 14, 13, 7, dash=_pick(S, 3.5, 1.5), gap=_pick(S, 3.0, 5.0))),
            line("M19.5 4V10.5M17.5 8.5L19.5 10.5L21.5 8.5")]


@icon("relay-attack", CAT, "Key fob on the left and a car on the right with a signal relay box between them.",
      tags=["relay attack", "keyless entry", "car theft", "key fob", "signal amplifier", "wireless", "hack"])
def _(S):
    return [shell(rect(2, 12, 5.5, 9, _pick(S, 0.5, 2))),
            dot(4.75, 16.5, 1.1),
            shell(rect(9, 2, 6, 3.5, _pick(S, 0.5, 1.5))),
            line("M9 6.8L6.5 8L8 9.2L5 10.6"),
            line("M15 6.8L17.5 8L16 9.2L19 10.6"),
            shell(poly([(11, 18), (11, 15), (13, 14.5), (14.5, 12), (18.5, 12), (20, 14.5), (22, 15), (22, 18)], closed=True, r=S.r)),
            dot(13.8, 19.3, 1.6), dot(19.2, 19.3, 1.6)]
