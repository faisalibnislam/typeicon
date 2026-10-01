"""TypeIcon Core: accessibility."""
import math as _m
import re as _re

from dsl import arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from dsl import fmt as _f


def _pick(S, sharp, soft):
    return sharp if S.name == "line" else soft


def _rot(d, deg, cx=12.0, cy=12.0, sx=1.0, k=1.0, dx0=0.0, dy0=0.0):
    """Rotate / mirror (sx=-1) / scale (k) / shift an absolute path (M L H V C Q A Z commands)."""
    c, s_ = _m.cos(_m.radians(deg)), _m.sin(_m.radians(deg))

    def tp(x, y):
        x = cx + (x - cx) * sx
        dx, dy = x - cx, y - cy
        return cx + dx0 + k * (dx * c - dy * s_), cy + dy0 + k * (dx * s_ + dy * c)
    out = []
    cur = (0.0, 0.0)
    start = cur
    for cmd, args in _re.findall(r"([MLHVCQAZ])([^MLHVCQAZ]*)", d):
        nums = [float(v) for v in _re.findall(r"-?\d*\.?\d+(?:e-?\d+)?", args)]
        if cmd == "A":
            res = []
            for i in range(0, len(nums), 7):
                rx, ry, rot, la, sw, x, y = nums[i:i + 7]
                cur = (x, y)
                if sx < 0:
                    sw = 1 - sw
                x, y = tp(x, y)
                res += [_f(rx * k), _f(ry * k), _f(rot), str(int(la)), str(int(sw)), _f(x), _f(y)]
            out.append("A" + " ".join(res))
        elif cmd == "Z":
            out.append("Z")
            cur = start
        elif cmd in "HV":
            pts = []
            for v in nums:
                cur = (v, cur[1]) if cmd == "H" else (cur[0], v)
                pts += list(tp(*cur))
            out.append("L" + " ".join(_f(v) for v in pts))
        else:
            pts = []
            for i in range(0, len(nums), 2):
                pts += list(tp(nums[i], nums[i + 1]))
            cur = (nums[-2], nums[-1])
            if cmd == "M":
                start = cur
            out.append(cmd + " ".join(_f(v) for v in pts))
    return "".join(out)


@icon("accessibility-person", "accessibility", "A person with outstretched arms inside a circle; universal access",
      tags=["accessibility", "a11y", "universal access", "inclusive", "disability"], aliases=["universal-access"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        dot(12, 6.6, 1.6),
        detail(poly([(7.3, 9.6), (12, 10.6), (16.7, 9.6)], r=S.r)),
        detail(poly([(9.3, 17.6), (12, 14), (14.7, 17.6)], r=S.r)),
        detail(seg(12, 10.6, 12, 14)),
    ]


def _hand_d(S):
    """Open hand, palm forward (same construction as body/hand, without finger separators)."""
    xs = [7.5, 10.9, 14.3, 17.7, 21.1]
    tops = [5.5, 3.5, 4.5, 7]
    tip = ""
    for k, top in enumerate(tops):
        r = (xs[k + 1] - xs[k]) / 2
        tip += f"V{_f(top + r)}A{_f(r)} {_f(r)} 0 0 1 {_f(xs[k + 1])} {_f(top + r)}"
    start = "M9 21C8 19.8 6.2 17.6 3.8 15.6" if S.name == "line" else "M10.5 21C9.3 21 8.5 20.4 7.8 19.4L3.8 15.6"
    return start + "A1.7 1.7 0 0 1 5.9 12.7L7.5 15" + tip + "V15C21.1 18.3 19 21 16 21Z"


@icon("sign-language", "accessibility", "A signing hand in motion", tags=["sign", "asl", "deaf", "interpreter", "gesture", "hands"],
      aliases=["asl"])
def _(S):
    h = _hand_d(S)
    t = dict(deg=-15, cx=12, cy=12, k=0.74, dx0=-3, dy0=2.6)
    hand = _rot(h, **t)
    seps = [detail(_rot(seg(x, y, x, 12.5), **t)) for x, y in ((10.9, 5.3), (14.3, 6.2), (17.7, 8.7))]
    return [shell(hand)] + seps + [line(arc(12.5, 12, 6.8, -68, -28)), line(arc(12.5, 12, 9.8, -62, -32))]


@icon("braille", "accessibility", "A card with raised Braille dots", tags=["blind", "tactile", "reading", "dots", "visually impaired"])
def _(S):
    parts = [shell(rect(3, 5, 18, 14, S.R))]
    for x, y in ((7.5, 9), (7.5, 12), (10.5, 9), (13.5, 9), (13.5, 15), (16.5, 9), (16.5, 12)):
        parts.append(dot(x, y, 1.1))
    return parts


@icon("audio-description", "accessibility", "The letters AD with sound waves; audio description",
      tags=["ad", "described video", "narration", "blind", "audio", "accessibility"])
def _(S):
    return [
        line(poly([(2.5, 17), (5, 7), (7.5, 17)], r=S.r), stroke_miterlimit="8"),
        line(seg(3.5, 13.8, 6.5, 13.8)),
        shell(_pick(S, "M9.5 7V17H10.5A4 5 0 0 0 10.5 7Z", "M10.5 7A4 5 0 0 1 10.5 17H10.5Q9.5 17 9.5 16V8Q9.5 7 10.5 7Z")),
        line(arc(13.5, 12, 4.5, -40, 40)), line(arc(13.5, 12, 7.5, -40, 40)),
    ]


def _ear(ox, oy, s):
    X = lambda v: _f(ox + s * v)  # noqa: E731
    Y = lambda v: _f(oy + s * v)  # noqa: E731
    outer = (f"M{X(7)} {Y(9)}C{X(7)} {Y(5.7)} {X(9.5)} {Y(3)} {X(13)} {Y(3)}C{X(16.5)} {Y(3)} {X(19)} {Y(5.7)} {X(19)} {Y(9)}"
             f"C{X(19)} {Y(11.8)} {X(17.5)} {Y(13)} {X(16.3)} {Y(14.5)}C{X(15.3)} {Y(15.8)} {X(15.2)} {Y(17.5)} {X(14.4)} {Y(19)}"
             f"C{X(13.5)} {Y(20.7)} {X(11)} {Y(21.5)} {X(9)} {Y(20)}")
    inner = (f"M{X(10.8)} {Y(9.5)}C{X(10.8)} {Y(8)} {X(11.8)} {Y(7)} {X(13)} {Y(7)}C{X(14.3)} {Y(7)} {X(15.2)} {Y(8)} {X(15.2)} {Y(9.2)}"
             f"C{X(15.2)} {Y(10.8)} {X(13.8)} {Y(11.4)} {X(13.1)} {Y(12.8)}")
    return outer, inner


@icon("hearing-loop", "accessibility", "An ear with the letter T; hearing loop available",
      tags=["induction loop", "t-coil", "hearing aid", "deaf", "hard of hearing", "telecoil"], aliases=["induction-loop"])
def _(S):
    o, i = _ear(-3.5, -0.5, 0.9)
    return [line(o), line(i), line(seg(14.5, 14.5, 21, 14.5)), line(seg(17.75, 14.5, 17.75, 21))]


@icon("blind-cane", "accessibility", "A person walking with a white cane", tags=["blind", "visually impaired", "white cane", "walking", "guide"],
      aliases=["white-cane"])
def _(S):
    return [
        shell(circle(9.5, 4.5, 2)),
        line("M9 8.5L8 14L5.5 21M8 14L11 17.5L11.5 21"),
        line(poly([(8.8, 9.5), (12, 12.5)], r=S.r)),
        line(seg(12, 12.5, 18.5, 21)),
    ]


@icon("service-dog", "accessibility", "A guide dog wearing a harness with a handle", tags=["guide dog", "assistance dog", "blind", "harness", "dog"],
      aliases=["guide-dog"])
def _(S):
    body = [(5.5, 11.5), (14.5, 11.5), (15.5, 7.5), (17.5, 5.5), (18.5, 7.5), (21, 9), (21, 11), (18, 11.5), (17.5, 14.5), (17.5, 21),
            (15.5, 21), (15.5, 16), (8.5, 16), (8.5, 21), (6.5, 21), (5.5, 15)]
    return [
        shell(poly(body, closed=True, r=S.r), stroke_miterlimit="2"),
        line(seg(5.5, 12, 3, 9)),
        line(poly([(12, 11.5), (9, 5), (6, 5)], r=S.r)),
    ]


@icon("low-vision", "accessibility", "An eye with a partly broken outline; low vision",
      tags=["partially sighted", "visually impaired", "sight", "eye", "vision"], aliases=["partial-sight"])
def _(S):
    return [
        line("M14 5.2C13.4 5.1 12.7 5 12 5C8 5 4.5 7 2 12C4.5 17 8 19 12 19C12.7 19 13.4 18.9 14 18.8"),
        line("M16 5.8C17.6 6.5 18.9 7.6 20 9"), line(_pick(S, "M21.2 10.6L22 12L21.2 13.4", "M21.2 10.6Q22 12 21.2 13.4")),
        line("M20 15C18.9 16.4 17.6 17.5 16 18.2"),
        shell(circle(12, 12, 3)),
    ]


_HEAD = "M8 21V17.2C5.6 15.8 4 13.3 4 10.5C4 6.4 7.6 3 12 3C16.1 3 19 5.9 19 9.5L20.5 12.8L19 13.3V15.5C19 16.6 18.1 17.5 17 17.5H14V21Z"
_HEAD_R = ("M8 20V17.2C5.6 15.8 4 13.3 4 10.5C4 6.4 7.6 3 12 3C16.1 3 19 5.9 19 9.5L20.2 12Q20.6 12.9 19.7 13.1L19 13.3V15.5"
           "C19 16.6 18.1 17.5 17 17.5H14V20C14 20.6 13.6 21 13 21H9C8.4 21 8 20.6 8 20Z")


@icon("cognitive", "accessibility", "A head in profile with a spiral inside; cognitive accessibility",
      tags=["cognition", "learning", "neurodiversity", "mind", "memory", "understanding"], aliases=["neurodiversity"])
def _(S):
    return [shell(_pick(S, _HEAD, _HEAD_R)), detail("M11.5 10.5A1.5 1.5 0 1 1 13 12C11 12 9.5 10.5 9.5 8.8C9.5 7.3 10.8 6.2 12.5 6.2C14.5 6.2 16 7.8 16 9.8")]


@icon("mobility-aid", "accessibility", "A wheeled walking frame (rollator)", tags=["walker", "rollator", "zimmer", "mobility", "elderly", "walking frame"],
      aliases=["walker", "rollator"])
def _(S):
    return [
        line(_pick(S, "M3.5 4H8V16.8M8 4L15.3 16.8", "M3.5 4H6.5Q8 4 8 5.5V16.8M8.7 5.3L15.3 16.8")),
        line(seg(8, 11, 11.3, 11)),
        shell(circle(16.5, 19, 2)), shell(circle(8, 19, 2)),
    ]


def _easy_filled():
    from dsl import D, P, ST, U
    page = rect(4, 3, 16, 18, 2)
    return D(U(P(page), ST(page, 2)), P(rect(7, 6.5, 4, 4)), P(rect(7, 13.5, 4, 4)),
             ST(seg(13.5, 8.5, 17, 8.5), 2), ST(seg(13.5, 15.5, 17, 15.5), 2))


@icon("easy-read", "accessibility", "A page of pictures next to short lines of text; easy read",
      tags=["easy read", "plain language", "simple text", "learning disability", "pictures", "document"], aliases=["plain-language"],
      filled=_easy_filled)
def _(S):
    r = 0 if S.name == "line" else 0.75
    return [
        shell(rect(4, 3, 16, 18, S.R)),
        solid(rect(7, 6.5, 4, 4, r)), detail(seg(13.5, 8.5, 17, 8.5)),
        solid(rect(7, 13.5, 4, 4, r)), detail(seg(13.5, 15.5, 17, 15.5)),
    ]
