"""TypeIcon Core: body."""
import math as _m
import re as _re

from dsl import arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401


@icon("tooth", "body", "A single tooth (molar)", tags=["dental", "dentist", "teeth", "mouth"], aliases=["molar"])
def _(S):
    return [shell("M7 3.5C4.5 3.5 3.5 5.5 3.5 8C3.5 11 5 13 6 15L7 20C7.3 21 8.7 21 9 20L10.5 14.5C10.8 13.5 13.2 13.5 13.5 14.5L15 20C15.3 21 16.7 21 17 20L18 15C19 13 20.5 11 20.5 8C20.5 5.5 19.5 3.5 17 3.5C15 3.5 14 4.5 12 4.5C10 4.5 9 3.5 7 3.5Z" if S.name == "rounded" else
                  "M7 3.5C4.5 3.5 3.5 5.5 3.5 8C3.5 11 5 13 6 15L7.5 21L10.5 14L13.5 14L16.5 21L18 15C19 13 20.5 11 20.5 8C20.5 5.5 19.5 3.5 17 3.5C15 3.5 14 4.5 12 4.5C10 4.5 9 3.5 7 3.5Z")]


@icon("footprints", "body", "Two footprints", tags=["feet", "steps", "walk", "trail"])
def _(S):
    return [
        shell(rect(4, 3, 5, 9, 2.5)), shell(rect(4.5, 13.5, 4, 3.5, 1.2 if S.name == "line" else 1.75)),
        shell(rect(15, 7, 5, 9, 2.5)), shell(rect(15.5, 17.5, 4, 3.5, 1.2 if S.name == "line" else 1.75)),
    ]


# --------------------------------------------------------------------------- helpers

from dsl import D as _D, I as _I, P as _P, ST as _ST, U as _U, fmt as _f, path_to_d as _p2d  # noqa: E402


def _hl_parts(outline, clip_in):
    """Highlighted zone of a body outline: solid in Line/Rounded."""
    return solid(_p2d(_I(_P(outline), _P(clip_in))))


def _hl_filled(outline, clip_in, clip_out=None, extra=(), knock=()):
    """Filled design for a highlighted zone: silhouette, 2 px gap, solid zone."""
    def f():
        body = _solid(outline)
        for k in knock:
            body = _D(body, _ST(k, 2))
        out = _P(clip_out) if clip_out else _U(_P(clip_in), _ST(clip_in, 4, "butt", "miter"))
        return _U(_D(body, out), _I(body, _P(clip_in)), *extra)
    return f


def _solid(d, w=2.0):
    """Filled silhouette of a closed Line outline (fill + outer half of the stroke)."""
    return _U(_P(d), _ST(d, w, "butt", "miter"))


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


# --------------------------------------------------------------------------- head & face

_HEAD = "M8 21V17.2C5.6 15.8 4 13.3 4 10.5C4 6.4 7.6 3 12 3C16.1 3 19 5.9 19 9.5L20.5 12.8L19 13.3V15.5C19 16.6 18.1 17.5 17 17.5H14V21Z"
_HEAD_R = "M8 20V17.2C5.6 15.8 4 13.3 4 10.5C4 6.4 7.6 3 12 3C16.1 3 19 5.9 19 9.5L20.2 12Q20.6 12.9 19.7 13.1L19 13.3V15.5C19 16.6 18.1 17.5 17 17.5H14V20C14 20.6 13.6 21 13 21H9C8.4 21 8 20.6 8 20Z"


@icon("head", "body", "Side profile of a human head", tags=["profile", "person", "human", "silhouette", "mind"])
def _(S):
    d = _pick(S,
              "M8 21V17.2C5.6 15.8 4 13.3 4 10.5C4 6.4 7.6 3 12 3C16.1 3 19 5.9 19 9.5L20.5 12.8L19 13.3V15.5C19 16.6 18.1 17.5 17 17.5H14V21Z",
              "M8 20V17.2C5.6 15.8 4 13.3 4 10.5C4 6.4 7.6 3 12 3C16.1 3 19 5.9 19 9.5L20.2 12Q20.6 12.9 19.7 13.1L19 13.3V15.5C19 16.6 18.1 17.5 17 17.5H14V20C14 20.6 13.6 21 13 21H9C8.4 21 8 20.6 8 20Z")
    return [shell(d)]


@icon("face", "body", "Front view of a human face", tags=["person", "human", "portrait", "head", "facial"])
def _(S):
    return [
        shell(ellipse(12, 12, 7, 9)),
        line("M5 10.3C3.8 10.2 3 11 3 12.3C3 13.8 3.8 15 5.3 14.8"),
        line("M19 10.3C20.2 10.2 21 11 21 12.3C21 13.8 20.2 15 18.7 14.8"),
        dot(9.3, 10.5), dot(14.7, 10.5),
        detail(poly([(12, 11), (12, 14), (11, 14)], r=min(S.r, 0.8))),
        detail(seg(10, 17, 14, 17)),
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


@icon("ear", "body", "A human ear", tags=["hear", "listen", "hearing", "sound", "audio"])
def _(S):
    o, i = _ear(0, 0, 1)
    return [line(o), line(i)]


@icon("ear-hearing", "body", "An ear with sound waves; hearing", tags=["hear", "listen", "sound", "audio", "hearing"], aliases=["hearing"])
def _(S):
    o, i = _ear(-3, 1.2, 0.9)
    return [line(o), line(i), line(arc(12.5, 11, 5.5, -40, 40)), line(arc(12.5, 11, 8.5, -40, 40))]


@icon("nose", "body", "A nose in side profile", tags=["smell", "scent", "sniff", "face", "nostril"])
def _(S):
    return [
        line("M10 3C10 7 9.4 10 8 12.6C6.9 14.6 5.9 16.2 6.7 17.7C7.5 19.2 9.6 19.3 10.6 18C11.2 18.9 12.8 18.9 13.4 18C14.4 19.3 16.5 19.2 17.3 17.7C18.1 16.2 17.1 14.6 16 12.6C14.6 10 14 7 14 3"),
    ]


@icon("lips", "body", "Closed lips", tags=["kiss", "mouth", "lipstick", "beauty", "smooch"])
def _(S):
    d = _pick(S,
              "M2.5 12C5 8.5 7.5 6.5 9.5 6.5C10.6 6.5 11.4 7.1 12 7.8C12.6 7.1 13.4 6.5 14.5 6.5C16.5 6.5 19 8.5 21.5 12C19 15.5 16 17.5 12 17.5C8 17.5 5 15.5 2.5 12Z",
              "M3.2 11.2C5.5 8.2 7.8 6.5 9.5 6.5C10.6 6.5 11.4 7.1 12 7.8C12.6 7.1 13.4 6.5 14.5 6.5C16.2 6.5 18.5 8.2 20.8 11.2Q21.4 12 20.8 12.8C18.5 15.8 15.8 17.5 12 17.5C8.2 17.5 5.5 15.8 3.2 12.8Q2.6 12 3.2 11.2Z")
    return [shell(d, stroke_miterlimit="2"), detail("M6.5 12.3C10 13.1 14 13.1 17.5 12.3")]


def _mouth_d(S):
    return _pick(S,
                 "M2.5 11C5 7.5 7.8 6 9.8 6C10.8 6 11.5 6.5 12 7C12.5 6.5 13.2 6 14.2 6C16.2 6 19 7.5 21.5 11C19.5 16 16 19 12 19C8 19 4.5 16 2.5 11Z",
                 "M3.1 10.2C5.5 7.3 8 6 9.8 6C10.8 6 11.5 6.5 12 7C12.5 6.5 13.2 6 14.2 6C16 6 18.5 7.3 20.9 10.2Q21.6 11 21.2 11.8C19.2 16.3 15.8 19 12 19C8.2 19 4.8 16.3 2.8 11.8Q2.4 11 3.1 10.2Z")


_MOUTH_IN = "M6 11.2C9.5 10.2 14.5 10.2 18 11.2C16.5 14.2 14.5 15.5 12 15.5C9.5 15.5 7.5 14.2 6 11.2Z"


@icon("mouth", "body", "An open mouth", tags=["speak", "talk", "lips", "oral", "open"],
      filled=lambda: _D(_solid(_mouth_d(type("S", (), {"name": "line"}))), _P(_MOUTH_IN), _ST(_MOUTH_IN, 2)))
def _(S):
    return [shell(_mouth_d(S), stroke_miterlimit="2"), detail(_MOUTH_IN)]


@icon("teeth", "body", "A wide grin showing the teeth", tags=["dental", "dentist", "tooth", "grin", "smile"])
def _(S):
    d = _pick(S, "M3 7.5H21C21 14 17 19 12 19C7 19 3 14 3 7.5Z",
              "M5 7.5H19Q21 7.5 20.8 9.5C20.1 15 16.5 19 12 19C7.5 19 3.9 15 3.2 9.5Q3 7.5 5 7.5Z")
    return [shell(d), detail(seg(3.5, 12, 20.5, 12)), detail(seg(8, 7.5, 8, 12)), detail(seg(12, 7.5, 12, 12)),
            detail(seg(16, 7.5, 16, 12)), detail(seg(10, 12, 10, 16.5)), detail(seg(14, 12, 14, 16.5))]


@icon("tongue", "body", "A tongue sticking out of a mouth", tags=["taste", "lick", "mouth", "cheeky"])
def _(S):
    return [
        line("M3 7C7 10.5 17 10.5 21 7"),
        shell("M7.5 9.6V15.5A4.5 4.5 0 0 0 16.5 15.5V9.6" + "C13.5 10.3 10.5 10.3 7.5 9.6Z"),
        detail(seg(12, 12.5, 12, 15.5)),
    ]


@icon("jaw", "body", "Head in profile with the jawline marked", tags=["mandible", "jawbone", "chin", "tmj", "dental"])
def _(S):
    return [shell(_pick(S, _HEAD, _HEAD_R)), detail("M8.5 8.5V11C8.5 12.9 10 14.3 12 14.3H16")]


def _hair_face():
    return "M8 14.5C8 12 9.6 10 12 9.5C12.8 11.4 14.4 12.4 16 12.5V15C16 17.2 14.2 19 12 19C9.8 19 8 17.2 8 15Z"


_HAIR = "M5 21C3.6 18.5 4 15 4 11.5C4 6.6 7.6 3 12 3C16.4 3 20 6.6 20 11.5C20 15 20.4 18.5 19 21Z"
_HAIR_R = "M5.8 21Q4.6 21 4.4 19.8C3.9 17.3 4 14.3 4 11.5C4 6.6 7.6 3 12 3C16.4 3 20 6.6 20 11.5C20 14.3 20.1 17.3 19.6 19.8Q19.4 21 18.2 21Z"


@icon("hair", "body", "A head of long hair framing a face", tags=["hairstyle", "haircut", "salon", "barber", "wig"],
      filled=lambda: _D(_solid(_HAIR), _P(_hair_face()), _ST(_hair_face(), 2)))
def _(S):
    outer = _pick(S, _HAIR, _HAIR_R)
    return [shell(outer), detail(_hair_face())]


@icon("beard", "body", "A full beard and moustache", tags=["facial hair", "barber", "man", "grooming", "hipster"])
def _(S):
    return [
        line("M4 10V9A8 8 0 0 1 20 9V10"),
        shell(_pick(S,
                    "M4 11.5C4 17.5 7.5 21 12 21C16.5 21 20 17.5 20 11.5C18.3 13 16.8 13.4 15 12.8C13.8 12.4 12.8 12 12 12C11.2 12 10.2 12.4 9 12.8C7.2 13.4 5.7 13 4 11.5Z",
                    "M4 12.5C4 18 7.5 21 12 21C16.5 21 20 18 20 12.5C20 11.6 19.2 11.4 18.6 11.9C17.5 12.9 16.3 13.2 15 12.8C13.8 12.4 12.8 12 12 12C11.2 12 10.2 12.4 9 12.8C7.7 13.2 6.5 12.9 5.4 11.9C4.8 11.4 4 11.6 4 12.5Z"),
              stroke_miterlimit="2"),
        detail(seg(10, 16, 14, 16)),
    ]


@icon("mustache", "body", "A curled moustache", tags=["moustache", "facial hair", "barber", "man", "movember"], aliases=["moustache"])
def _(S):
    d = _pick(S,
              "M12 10C13.5 8 16 7.5 18 8.7C19.3 9.5 20 11 21.5 10C21.5 13.5 19.3 15.8 16.3 15.3C14.3 15 12.8 13.8 12 13C11.2 13.8 9.7 15 7.7 15.3C4.7 15.8 2.5 13.5 2.5 10C4 11 4.7 9.5 6 8.7C8 7.5 10.5 8 12 10Z",
              "M12 10C13.5 8 16 7.5 18 8.7C19 9.3 19.7 10.3 20.6 10.2C21.1 10.1 21.5 10.4 21.4 11C21 14 18.9 15.7 16.3 15.3C14.3 15 12.8 13.8 12 13C11.2 13.8 9.7 15 7.7 15.3C5.1 15.7 3 14 2.6 11C2.5 10.4 2.9 10.1 3.4 10.2C4.3 10.3 5 9.3 6 8.7C8 7.5 10.5 8 12 10Z")
    return [shell(d, stroke_miterlimit="2")]


_EYE_SMALL = "M4.5 15C6.8 12.2 9.3 11 12 11C14.7 11 17.2 12.2 19.5 15C17.2 17.8 14.7 19 12 19C9.3 19 6.8 17.8 4.5 15Z"
_EYE_SMALL_R = "M5.1 14.2C7.3 11.9 9.6 11 12 11C14.4 11 16.7 11.9 18.9 14.2Q19.6 15 18.9 15.8C16.7 18.1 14.4 19 12 19C9.6 19 7.3 18.1 5.1 15.8Q4.4 15 5.1 14.2Z"


@icon("eyebrow", "body", "An eye with a raised eyebrow", tags=["brow", "eye", "face", "expression", "beauty"])
def _(S):
    return [line("M3.5 8.5C7.5 5 15 4.3 20.5 7"), shell(_pick(S, _EYE_SMALL, _EYE_SMALL_R)), dot(12, 15, 1.75)]


_EYE_BIG = "M3 14C5.5 10.7 8.5 9 12 9C15.5 9 18.5 10.7 21 14C18.5 17.3 15.5 19 12 19C8.5 19 5.5 17.3 3 14Z"
_EYE_BIG_R = "M3.6 13.2C6 10.5 8.8 9 12 9C15.2 9 18 10.5 20.4 13.2Q21.1 14 20.4 14.8C18 17.5 15.2 19 12 19C8.8 19 6 17.5 3.6 14.8Q2.9 14 3.6 13.2Z"


@icon("eyelashes", "body", "An open eye with long eyelashes", tags=["lashes", "mascara", "eye", "beauty", "makeup"])
def _(S):
    return [
        shell(_pick(S, _EYE_BIG, _EYE_BIG_R)), detail(circle(12, 14, 2.5)),
        line(seg(5.8, 10.8, 4, 8)), line(seg(9.3, 9.4, 8.4, 6)), line(seg(14.7, 9.4, 15.6, 6)), line(seg(18.2, 10.8, 20, 8)),
    ]


@icon("eye-closed", "body", "A closed eye with lashes", tags=["sleep", "blink", "hidden", "rest", "eye"])
def _(S):
    return [
        line("M3 9.5C6 13.5 9 15 12 15C15 15 18 13.5 21 9.5"),
        line(seg(5.6, 12.3, 3.8, 15)), line(seg(9.6, 14.5, 9, 17.8)), line(seg(14.4, 14.5, 15, 17.8)), line(seg(18.4, 12.3, 20.2, 15)),
    ]


@icon("eyeball", "body", "An eyeball looking to the side", tags=["eye", "vision", "sight", "optic", "look"])
def _(S):
    return [
        shell(circle(12, 12, 9)), detail(circle(14.5, 10.5, 3)), dot(14.5, 10.5, 1.25),
        detail(arc(12, 12, 5.5, 150, 200)),
    ]


@icon("iris", "body", "Iris and pupil of an eye, front view", tags=["eye", "pupil", "scan", "biometric", "vision"])
def _(S):
    parts = [shell(circle(12, 12, 9)), dot(12, 12, 2.5)]
    for k in range(8):
        a, b = pt_on(12, 12, 4.8, k * 45 + 22.5), pt_on(12, 12, 6.3, k * 45 + 22.5)
        parts.append(detail(seg(*a, *b)))
    return parts


@icon("neck", "body", "Chin, neck and shoulders", tags=["throat", "nape", "cervical", "shoulders", "posture"])
def _(S):
    return [
        shell(ellipse(12, 6.5, 3.5, 4)),
        line("M10 10.3V14C10 15.3 9 16 7 16.4C4.8 16.9 3.5 18.3 3.5 21"),
        line("M14 10.3V14C14 15.3 15 16 17 16.4C19.2 16.9 20.5 18.3 20.5 21"),
    ]


# --------------------------------------------------------------------------- hands & limbs



def _fingers(xs, tops):
    """Upright fingers side by side: xs = boundaries (len n+1), tops = tip heights (len n).
    Returns (path from xs[0] at tip-start up over all tips down to xs[-1] start, separator segments)."""
    d = ""
    seps = []
    for k, top in enumerate(tops):
        w = xs[k + 1] - xs[k]
        r = w / 2
        y0 = top + r
        d += f"V{_f(y0)}A{_f(r)} {_f(r)} 0 0 1 {_f(xs[k + 1])} {_f(y0)}"
        if k + 1 < len(tops):
            seps.append((xs[k + 1], max(y0, tops[k + 1] + (xs[k + 2] - xs[k + 1]) / 2)))
    return d, seps


def _hand(S, sep_to=12.5):
    xs = [7.5, 10.9, 14.3, 17.7, 21.1]
    tops = [5.5, 3.5, 4.5, 7]
    tipd, seps = _fingers(xs, tops)
    # thumb, 30 degrees out from the index finger
    d = ("M9 21C8 19.8 6.2 17.6 3.8 15.6" + "A1.7 1.7 0 0 1 5.9 12.7" + "L7.5 15" + tipd +
         "V15C21.1 18.3 19 21 16 21Z")
    if S.name != "line":
        d = ("M10.5 21C9.3 21 8.5 20.4 7.8 19.4L3.8 15.6A1.7 1.7 0 0 1 5.9 12.7L7.5 15" + tipd +
             "V15C21.1 18.3 19 21 16 21Z")
    return d, [detail(seg(x, y, x, sep_to)) for x, y in seps]


@icon("hand", "body", "An open hand, palm facing forward", tags=["palm", "stop", "high five", "wave", "fingers"], aliases=["palm"])
def _(S):
    d, seps = _hand(S)
    return [shell(d)] + seps


def _capsule_finger(base, ang, length, r):
    """Points for a finger: returns (left_base, left_tip, right_tip, right_base) and tip arc radius."""
    ux, uy = _m.sin(_m.radians(ang)), -_m.cos(_m.radians(ang))
    nx, ny = -uy, ux  # to the right of the finger direction
    bx, by = base
    tx, ty = bx + ux * length, by + uy * length
    return ((bx - nx * r, by - ny * r), (tx - nx * r, ty - ny * r), (tx + nx * r, ty + ny * r), (bx + nx * r, by + ny * r))


def _spread_hand(S):
    r = 1.6
    fingers = [((9.1, 12.2), -20, 6.2), ((12.3, 11.2), -4, 7.6), ((15.4, 11.6), 11, 6.8), ((18.1, 12.9), 27, 4.8)]
    d = ""
    first = None
    for k, (b, a, L) in enumerate(fingers):
        lb, lt, rt, rb = _capsule_finger(b, a, L, r)
        if first is None:
            first = lb
            d += f"L{_f(lb[0])} {_f(lb[1])}"
        else:
            d += f"L{_f(lb[0])} {_f(lb[1])}"
        d += f"L{_f(lt[0])} {_f(lt[1])}A{_f(r)} {_f(r)} 0 0 1 {_f(rt[0])} {_f(rt[1])}L{_f(rb[0])} {_f(rb[1])}"
    thumb = _capsule_finger((6.6, 16.8), -58, 4.2, r)
    start = (9.5, 21)
    out = (f"M{_f(start[0])} {_f(start[1])}L{_f(thumb[0][0])} {_f(thumb[0][1])}L{_f(thumb[1][0])} {_f(thumb[1][1])}"
           f"A{_f(r)} {_f(r)} 0 0 1 {_f(thumb[2][0])} {_f(thumb[2][1])}L{_f(thumb[3][0])} {_f(thumb[3][1])}" + d[0:] +
           "C20.2 16 19.2 19.4 16 21Z")
    return out


@icon("hand-open", "body", "A hand with the fingers spread wide", tags=["palm", "fingers", "spread", "open", "five"])
def _(S):
    return [shell(_spread_hand(S), stroke_miterlimit="2")]


@icon("fist", "body", "A clenched fist seen from the front", tags=["punch", "power", "strength", "solidarity", "fight"])
def _(S):
    xs = [5.5, 9, 12.5, 16, 19.5]
    tops = [6, 5, 5, 6]
    tipd, seps = _fingers(xs, tops)
    d = ("M8 21V18.5C6.5 17.5 5.5 16 5.5 14" + tipd + "V14C19.5 16 18.5 17.5 17 18.5V21Z")
    if S.name != "line":
        d = ("M9.5 21Q8 21 8 19.5V18.5C6.5 17.5 5.5 16 5.5 14" + tipd + "V14C19.5 16 18.5 17.5 17 18.5V19.5Q17 21 15.5 21Z")
    return [shell(d)] + [detail(seg(x, y, x, 10.5)) for x, y in seps] + [detail(seg(5.5, 10.5, 19.5, 10.5)),
                                                                         detail("M5.5 14.5H11.5C12.9 14.5 14 13.4 14 12V10.5")]


@icon("bicep", "body", "A flexed arm showing the biceps", tags=["muscle", "strong", "strength", "gym", "fitness", "flex"], aliases=["arm", "flex"])
def _(S):
    d = _pick(S,
              "M3 20.5V14.5C4 10.5 6.5 8 9.5 8C11.8 8 13.3 9.2 14 11V9H13.5C12.7 9 12 8.3 12 7.5V4.8C12 3.8 12.8 3 13.8 3H18.5C19.6 3 20.5 3.9 20.5 5V16C20.5 18.5 18.5 20.5 16 20.5Z",
              "M5 20.5Q3 20.5 3 18.5V14.5C4 10.5 6.5 8 9.5 8C11.8 8 13.3 9.2 14 11V9H13.5C12.7 9 12 8.3 12 7.5V4.8C12 3.8 12.8 3 13.8 3H18.5C19.6 3 20.5 3.9 20.5 5V16C20.5 18.5 18.5 20.5 16 20.5Z")
    return [shell(d), detail(seg(14.5, 6, 20.5, 6))]


_ELBOW = "M3 20.5V15H14.5V9.5H13.5C12.7 9.5 12 8.8 12 8V4.8C12 3.8 12.8 3 13.8 3H18.8C19.8 3 20.5 3.8 20.5 4.8V20.5Z"
_ELBOW_R = "M3 19.5V16Q3 15 4 15H14.5V9.5H13.5C12.7 9.5 12 8.8 12 8V4.8C12 3.8 12.8 3 13.8 3H18.8C19.8 3 20.5 3.8 20.5 4.8V17.5Q20.5 20.5 17.5 20.5H4Q3 20.5 3 19.5Z"


@icon("elbow", "body", "An arm bent at the elbow with the joint highlighted", tags=["joint", "arm", "bend", "tennis elbow", "limb"],
      filled=_hl_filled(_ELBOW, circle(20.5, 20.5, 5), circle(20.5, 20.5, 7), extra=(_ST(seg(14.5, 6.5, 20.5, 6.5), 2),)))
def _(S):
    o = _pick(S, _ELBOW, _ELBOW_R)
    return [shell(o), _hl_parts(o, circle(20.5, 20.5, 5)), detail(seg(14.5, 6.5, 20.5, 6.5))]


def _wrist_outline(S):
    hd, _ = _hand(S)
    if S.name != "line":
        hd = hd.replace("M10.5 21C9.3 21 8.5 20.4 7.8 19.4L3.8 15.6", "M9 21C8.3 20.2 7.9 19.8 7.8 19.4L3.8 15.6")
    hd = hd.replace("M9 21", "M9 30L9 21").replace("16 21Z", "16 21L16 30Z")
    return _rot(hd, 0, 12, 12, k=0.72, dx0=-0.3, dy0=-4)


_WRIST_BAND = rect(0, 15.5, 24, 2.5)
_WRIST_OUT = rect(0, 13.5, 24, 6.5)


@icon("wrist", "body", "A hand and forearm with the wrist highlighted", tags=["joint", "hand", "forearm", "carpal", "sprain"],
      filled=_hl_filled(_wrist_outline(type("S", (), {"name": "line"})), _WRIST_BAND, _WRIST_OUT))
def _(S):
    o = _wrist_outline(S)
    _, seps = _hand(S)
    return [shell(o), _hl_parts(o, _WRIST_BAND)] + [detail(_rot(p.d, 0, 12, 12, k=0.72, dx0=-0.3, dy0=-4)) for p in seps]


_BUST = "M3 21V16C3 12.7 5.7 10.5 9 10.5H15C18.3 10.5 21 12.7 21 16V21Z"
_BUST_R = "M5 21Q3 21 3 19V16C3 12.7 5.7 10.5 9 10.5H15C18.3 10.5 21 12.7 21 16V19Q21 21 19 21Z"


@icon("shoulder", "body", "Upper body with one shoulder highlighted", tags=["joint", "upper body", "deltoid", "posture", "pain"],
      filled=_hl_filled(_BUST, circle(3.5, 11, 5.5), circle(3.5, 11, 7.5), extra=(_P(circle(12, 5.5, 4)),)))
def _(S):
    o = _pick(S, _BUST, _BUST_R)
    return [shell(circle(12, 5.5, 3)), shell(o), _hl_parts(o, circle(3.5, 11, 5.5))]


# --------------------------------------------------------------------------- legs & feet

_LEG = ("M6 3H15.5C15.5 6 14.3 8.3 14 10.5C13.8 12.5 14.2 14.5 13.8 16.8L19 18.2C20.3 18.6 21 19.3 21 20.2V21H9.5C9.5 19.5 9.8 18 9.5 16.8"
        "C9 14.5 7.2 13.5 7.2 10.8C7.2 8.6 6 6.5 6 3Z")
_LEG_R = ("M7.5 3H14Q15.5 3 15.4 4.5C15.2 6.8 14.3 8.6 14 10.5C13.8 12.5 14.2 14.5 13.8 16.8L19 18.2C20.3 18.6 21 19.3 21 20.2Q21 21 20.2 21H10.5Q9.5 21 9.5 20C9.5 19 9.7 17.8 9.5 16.8"
          "C9 14.5 7.2 13.5 7.2 10.8C7.2 8.6 6.1 6.8 6 4.5Q6 3 7.5 3Z")


@icon("leg", "body", "A leg and foot in side view", tags=["limb", "thigh", "calf", "lower body", "walk"])
def _(S):
    return [shell(_pick(S, _LEG, _LEG_R))]


_KNEE = "M5.5 4H15C17.5 4 19 5.7 18.8 8L18.2 16L20.2 17.2C20.7 17.5 21 18 21 18.6V21H13.2L13.2 16.5C13.2 14 13.4 12.2 13.2 10.5H5.5A3.25 3.25 0 0 1 5.5 4Z"
_KNEE_R = "M5.5 4H15C17.5 4 19 5.7 18.8 8L18.2 16L20.2 17.2C20.7 17.5 21 18 21 18.6V20Q21 21 20 21H14.2Q13.2 21 13.2 20L13.2 16.5C13.2 14 13.4 12.2 13.2 10.5H5.5A3.25 3.25 0 0 1 5.5 4Z"


@icon("knee", "body", "A bent leg with the knee highlighted", tags=["joint", "leg", "kneecap", "patella", "sit"],
      filled=_hl_filled(_KNEE, circle(19.5, 3.5, 6), circle(19.5, 3.5, 8)))
def _(S):
    o = _pick(S, _KNEE, _KNEE_R)
    return [shell(o), _hl_parts(o, circle(19.5, 3.5, 6))]


_FOOT = ("M6.5 3H11V11.8C11 13.1 11.9 14.2 13.2 14.6L18.6 16.2C20.1 16.7 21 17.8 21 19C21 20.2 20.2 21 19 21H16.8C15.3 21 14.6 20 12.7 20"
         "C10.8 20 10.2 21 8.5 21H6C4.8 21 4 20.2 4 19C4 17.5 5 16.4 5.8 15.4C6.3 14.7 6.5 14 6.5 13Z")
_FOOT_R = ("M7.5 3H10Q11 3 11 4V11.8C11 13.1 11.9 14.2 13.2 14.6L18.6 16.2C20.1 16.7 21 17.8 21 19C21 20.2 20.2 21 19 21H16.8C15.3 21 14.6 20 12.7 20"
           "C10.8 20 10.2 21 8.5 21H6C4.8 21 4 20.2 4 19C4 17.5 5 16.4 5.8 15.4C6.3 14.7 6.5 14 6.5 13V4Q6.5 3 7.5 3Z")


@icon("foot", "body", "A human foot in side view", tags=["feet", "heel", "toes", "walk", "podiatry"])
def _(S):
    return [shell(_pick(S, _FOOT, _FOOT_R))]


@icon("ankle", "body", "A foot with the ankle highlighted", tags=["joint", "foot", "heel", "sprain", "achilles"],
      filled=_hl_filled(_FOOT, circle(8.8, 14.5, 3.5), circle(8.8, 14.5, 5.5)))
def _(S):
    o = _pick(S, _FOOT, _FOOT_R)
    return [shell(o), _hl_parts(o, circle(8.8, 14.5, 3.5))]


@icon("toe", "body", "Front of a foot seen from above, showing the toes", tags=["toes", "foot", "big toe", "podiatry", "feet"])
def _(S):
    return [
        line("M5 21V14.5C5 12.3 7.5 11 12 11C16.5 11 19 12.3 19 14.5V21"),
        shell(ellipse(7.5, 5.8, 2.2, 2.8)), dot(12, 4.8, 1.4), dot(15.3, 5.6, 1.3), dot(18, 7.2, 1.2), dot(20, 9.8, 1.1),
    ]


def _baby_foot(cx, cy, S=None):
    if S is not None and S.name == "line":
        return (f"M{_f(cx)} {_f(cy - 3.5)}C{_f(cx + 2.6)} {_f(cy - 3.5)} {_f(cx + 3)} {_f(cy - 1)} {_f(cx + 2.6)} {_f(cy + 1.5)}"
                f"L{_f(cx + 1.8)} {_f(cy + 5)}L{_f(cx - 1.8)} {_f(cy + 5)}L{_f(cx - 2.6)} {_f(cy + 1.5)}"
                f"C{_f(cx - 3)} {_f(cy - 1)} {_f(cx - 2.6)} {_f(cy - 3.5)} {_f(cx)} {_f(cy - 3.5)}Z")
    sole = f"M{_f(cx)} {_f(cy - 3.5)}C{_f(cx + 2.6)} {_f(cy - 3.5)} {_f(cx + 3)} {_f(cy - 1)} {_f(cx + 2.6)} {_f(cy + 1.5)}C{_f(cx + 2.3)} {_f(cy + 3.5)} {_f(cx + 1.6)} {_f(cy + 5)} {_f(cx)} {_f(cy + 5)}C{_f(cx - 1.6)} {_f(cy + 5)} {_f(cx - 2.4)} {_f(cy + 3.5)} {_f(cx - 2.6)} {_f(cy + 1.5)}C{_f(cx - 3)} {_f(cy - 1)} {_f(cx - 2.6)} {_f(cy - 3.5)} {_f(cx)} {_f(cy - 3.5)}Z"
    return sole


@icon("baby-feet", "body", "A pair of small baby footprints", tags=["baby", "newborn", "footprints", "infant", "birth"])
def _(S):
    parts = []
    for cx, cy, sgn in ((7, 13, -1), (17, 9.5, 1)):
        parts.append(shell(_baby_foot(cx, cy, S)))
        for dx, dy in ((-2.2, -6.6), (0.4, -7.2), (2.8, -6.2)):
            parts.append(dot(cx + dx * (-sgn) if sgn < 0 else cx + dx, cy + dy, 1))
    return parts


@icon("fingernail", "body", "A fingertip with its nail", tags=["nail", "manicure", "finger", "beauty", "polish"])
def _(S):
    return [
        line("M7 21V9A5 5 0 0 1 17 9V21"),
        shell(_pick(S, "M9.5 13.5V8.5A2.5 2.5 0 0 1 14.5 8.5V13.5Z", "M11 13.5Q9.5 13.5 9.5 12V8.5A2.5 2.5 0 0 1 14.5 8.5V12Q14.5 13.5 13 13.5Z")),
        detail(seg(10, 17.5, 14, 17.5)),
    ]


_HIPS = "M5 3H19C19.8 6 20.5 9 20.5 12.5L19.5 21H13.5L12.5 13.5H11.5L10.5 21H4.5L3.5 12.5C3.5 9 4.2 6 5 3Z"
_HIPS_R = "M6 3H18Q19 3 19.3 4C19.9 6.5 20.5 9.3 20.5 12.5L19.6 20Q19.5 21 18.5 21H14.4Q13.5 21 13.4 20.1L12.5 13.5H11.5L10.6 20.1Q10.5 21 9.6 21H5.5Q4.5 21 4.4 20L3.5 12.5C3.5 9.3 4.1 6.5 4.7 4Q5 3 6 3Z"


@icon("hip", "body", "Lower body with one hip highlighted", tags=["joint", "pelvis", "hips", "waist", "hip replacement"],
      filled=_hl_filled(_HIPS, circle(3.5, 9.5, 5.5), circle(3.5, 9.5, 7.5)))
def _(S):
    o = _pick(S, _HIPS, _HIPS_R)
    return [shell(o), _hl_parts(o, circle(3.5, 9.5, 5.5))]


@icon("pelvis", "body", "The pelvis bone, front view", tags=["hip bone", "skeleton", "bone", "sacrum", "anatomy"])
def _(S):
    d = _pick(S,
              "M12 6.5C10.5 5 8 3.8 5 4C3.5 4.1 3 5 3 6.5C3 9.5 4 12 5.8 13.8C6.8 14.8 7.3 16 7.3 17.5V20H10C10.5 18.8 11.2 18.3 12 18.3C12.8 18.3 13.5 18.8 14 20H16.7V17.5C16.7 16 17.2 14.8 18.2 13.8C20 12 21 9.5 21 6.5C21 5 20.5 4.1 19 4C16 3.8 13.5 5 12 6.5Z",
              "M12 6.5C10.5 5 8 3.8 5 4C3.5 4.1 3 5 3 6.5C3 9.5 4 12 5.8 13.8C6.8 14.8 7.3 16 7.3 17.5V19Q7.3 20 8.3 20H9.3Q10 20 10.4 19.2C10.8 18.6 11.3 18.3 12 18.3C12.7 18.3 13.2 18.6 13.6 19.2Q14 20 14.7 20H15.7Q16.7 20 16.7 19V17.5C16.7 16 17.2 14.8 18.2 13.8C20 12 21 9.5 21 6.5C21 5 20.5 4.1 19 4C16 3.8 13.5 5 12 6.5Z")
    return [shell(d), detail(ellipse(12, 12.3, 2.6, 2.3)), detail(seg(12, 6.5, 12, 10))]


# --------------------------------------------------------------------------- torso

_TORSO = "M9.5 3V5.3C7.3 5.8 5.2 6.3 4 7.6C3.3 8.4 3 9.5 3 10.8V16H5.6L6.5 21H17.5L18.4 16H21V10.8C21 9.5 20.7 8.4 20 7.6C18.8 6.3 16.7 5.8 14.5 5.3V3Z"
_TORSO_R = ("M9.5 3V5.3C7.3 5.8 5.2 6.3 4 7.6C3.3 8.4 3 9.5 3 10.8V15Q3 16 4 16H5.6L6.4 20.1Q6.5 21 7.4 21H16.6Q17.5 21 17.6 20.1L18.4 16H20Q21 16 21 15"
            "V10.8C21 9.5 20.7 8.4 20 7.6C18.8 6.3 16.7 5.8 14.5 5.3V3Z")


def _torso(S, *details):
    return [shell(_pick(S, _TORSO, _TORSO_R)), detail(seg(5.6, 10.5, 5.6, 16)),
            detail(seg(18.4, 10.5, 18.4, 16))] + list(details)


@icon("chest", "body", "A bare torso showing the chest muscles", tags=["torso", "pecs", "pectoral", "upper body", "thorax"])
def _(S):
    return _torso(S, detail("M7.5 9.5C7.8 11.7 9.3 12.7 11 12.2"), detail("M16.5 9.5C16.2 11.7 14.7 12.7 13 12.2"))


@icon("back-body", "body", "A torso seen from behind with the spine and shoulder blades", tags=["back", "spine", "posture", "back pain", "torso"], aliases=["back-pain"])
def _(S):
    return _torso(S, detail(seg(12, 8, 12, 18.5)), detail("M9 8.8C9.4 10 9.4 11.3 9 12.5"), detail("M15 8.8C14.6 10 14.6 11.3 15 12.5"))


@icon("belly-button", "body", "A torso with the navel", tags=["navel", "belly", "stomach", "abdomen", "tummy"], aliases=["navel"])
def _(S):
    return _torso(S, detail(ellipse(12, 13.5, 1.1, 1.6)))


@icon("pregnant", "body", "Side profile of a pregnant person", tags=["pregnancy", "maternity", "expecting", "mother", "baby bump"], aliases=["pregnancy"])
def _(S):
    body = _pick(S,
                 "M8.5 8.5H11.8C12.8 8.5 13.5 9.2 13.7 10C16.8 10.8 18.5 12.8 18.5 15C18.5 17 16.8 18.3 14.5 18.3H13.5V21H8C8 17 7.4 13.3 7.4 10.5C7.4 9.4 7.7 8.5 8.5 8.5Z",
                 "M8.5 8.5H11.8C12.8 8.5 13.5 9.2 13.7 10C16.8 10.8 18.5 12.8 18.5 15C18.5 17 16.8 18.3 14.5 18.3H13.5V20Q13.5 21 12.5 21H9Q8 21 8 20C8 16.5 7.4 13.3 7.4 10.5C7.4 9.4 7.7 8.5 8.5 8.5Z")
    return [shell(circle(10.5, 4.5, 2.5)), shell(body), detail(poly([(10, 10.5), (10.4, 14.8), (13.8, 15.2)], r=S.r))]


# --------------------------------------------------------------------------- organs

@icon("heart-organ", "body", "The anatomical heart with its main vessels", tags=["heart", "cardiac", "cardiology", "organ", "anatomy"], aliases=["anatomical-heart"])
def _(S):
    body = ("M7 9.5C8.3 8.3 10 8 11.5 8.8C13.3 7.3 16.3 7.3 18.3 9.3C20.8 11.8 20.6 16.3 17.8 19.1C15.8 21.1 12.5 21.5 10 20.2"
            "C6.5 18.4 4.8 14.5 5.3 11.8C5.5 10.8 6.2 10.2 7 9.5Z")
    return [
        shell(body),
        line("M9.5 8.3V3"),
        line("M13 7.9V5.5A2.5 2.5 0 0 1 18 5.5V6.5"),
        detail("M12.5 12C12.3 14.5 13.5 16.5 16 18"),
    ]


@icon("brain", "body", "A brain seen from the side", tags=["mind", "think", "intelligence", "neurology", "psychology", "idea"])
def _(S):
    d = ("M6.5 17C4.3 16.6 3 14.8 3 12.8C3 11.3 3.6 10.2 4.5 9.5C4.3 6.6 6.4 4.5 9 4.5C10.2 3.6 11.5 3.2 13 3.3C15.3 3.4 17 4.6 17.8 6.3"
         "C19.9 7 21 8.8 21 10.8C21 13.3 19.2 15.2 16.8 15.4C16.3 16.8 15 17.7 13.5 17.7L13.5 21H11V17.2Z")
    return [
        shell(d),
        detail("M7.5 9.3C8.3 8.2 9.8 8 11 8.7"), detail("M12.5 6.5C13.8 7 14.4 8.2 14.2 9.5"),
        detail("M8 13C9.3 13.8 11 13.6 12 12.5"), detail("M15.5 11.5C16.8 11.5 17.8 10.8 18.3 9.8"),
    ]


def _lung(sx):
    d = "M10 8C7.2 8 4 12 3.5 16.5C3.2 19 4.5 20.7 7 20.2L9.5 19.7C10.2 19.5 10.5 19 10.5 18.3V8.8C10.5 8.3 10.4 8 10 8Z"
    return _rot(d, 0, 12, 12, sx=sx)


@icon("lungs", "body", "A pair of lungs with the windpipe", tags=["breathe", "respiratory", "breath", "pulmonary", "organ"])
def _(S):
    return [
        shell(_lung(1)), shell(_lung(-1)),
        line("M12 3V10.5M12 10.5L10.5 12M12 10.5L13.5 12"),
    ]


@icon("stomach", "body", "The stomach", tags=["digestion", "gastric", "belly", "organ", "gut"])
def _(S):
    d = ("M8 3H11V6C11 7.5 11.8 8.5 13 8.7C14 8.9 15 8.5 15.8 7.7C17.8 5.9 21 7.3 21 10.5C21 16 17 20.5 11.5 20.5C9.8 20.5 8.2 20 7 19"
         "L5 21.2L3.2 19.5L5.5 17.2C4.8 15.3 5.3 13 7 11.5C7.7 10.8 8 10 8 9Z")
    return [shell(d, stroke_miterlimit="2"), detail("M11.5 16.5C14.8 16.5 17 14.3 17.5 11")]


@icon("liver", "body", "The liver", tags=["hepatic", "organ", "digestion", "anatomy", "detox"])
def _(S):
    d = _pick(S,
              "M3 10C3 6.5 6 4.5 10 4.5C14 4.5 17.5 5 20.3 5.8L21 7L10.5 17.8C7 20.8 3 17.8 3 13.5Z",
              "M3 10C3 6.5 6 4.5 10 4.5C14 4.5 17.5 5 20 5.7C21 6 21.3 7.2 20.5 7.9L10.5 17.8C7 20.8 3 17.8 3 13.5Z")
    return [shell(d, stroke_miterlimit="2"), detail("M12.5 5C12.2 8.5 11.2 11 9.5 13")]


def _bean(cx, cy, sx):
    d = ("M12 4C15.5 4 18 7 18 11C18 15 15.5 18 12.5 18C10.8 18 10 16.8 10.3 15.5C10.5 14.3 11.5 13.5 11.5 12.2"
         "C11.5 10.8 10.3 10.2 10 8.8C9.6 6.5 10.3 4 12 4Z")
    return _rot(d, 0, 12, 12, sx=sx, dx0=cx - 12, dy0=cy - 12)


@icon("kidneys", "body", "A pair of kidneys with ureters", tags=["renal", "urology", "organ", "nephrology", "anatomy"])
def _(S):
    left = "M8.5 4C5.5 4 3 6.8 3 10.5C3 14.2 5.3 16.5 7.5 16.5C9 16.5 9.8 15.5 9.5 14.3C9.3 13.3 8.5 12.8 8.5 11.3C8.5 10 9.5 9.3 9.8 8.2C10.3 6 9.8 4 8.5 4Z"
    right = _rot(left, 0, 12, 12, sx=-1)
    return [shell(left), shell(right),
            line("M8.6 11.3C10.2 11.8 10.8 13.5 10.8 15.5V21"), line("M15.4 11.3C13.8 11.8 13.2 13.5 13.2 15.5V21")]


@icon("kidney", "body", "A single kidney with its ureter", tags=["renal", "urology", "organ", "nephrology", "anatomy"])
def _(S):
    d = ("M10 3C6.3 3 4 6.5 4 10.5C4 14.8 6.6 18 10 18C12 18 13 16.8 12.7 15.3C12.4 14 11.3 13.2 11.3 11.3C11.3 9.8 12.5 8.8 12.8 7.5"
         "C13.3 5 12.3 3 10 3Z")
    return [shell(d), line("M11.4 11.2H14C15.4 11.2 16.5 12.3 16.5 13.7V21")]


_GUT_FRAME = "M3 21V3H21V21H14V17H17V7H7V21Z"
_GUT_COIL = "M17 14H11.2A2 2 0 0 1 11.2 10H14.5"


@icon("intestines", "body", "The large intestine framing the coiled small intestine", tags=["bowel", "gut", "digestion", "colon", "organ"],
      filled=lambda: _U(_solid(_GUT_FRAME), _ST(_GUT_COIL, 2)))
def _(S):
    frame = _pick(S, "M3 21V3H21V21H14V17H17V7H7V21Z",
                  "M3 20V6A3 3 0 0 1 6 3H18A3 3 0 0 1 21 6V18A3 3 0 0 1 18 21H15Q14 21 14 20V18Q14 17 15 17H17V7H7V20Q7 21 6 21H4Q3 21 3 20Z")
    return [shell(frame), line(_GUT_COIL)]


@icon("bladder", "body", "The urinary bladder", tags=["urinary", "urology", "organ", "pee", "incontinence"])
def _(S):
    d = "M12 18C8 18 5 15.5 5 12C5 8.8 7.5 7 10 7.5C11 7.7 11.5 8 12 8C12.5 8 13 7.7 14 7.5C16.5 7 19 8.8 19 12C19 15.5 16 18 12 18Z"
    return [shell(d), line("M8 7.6C7.3 6.2 6.5 4.8 6.5 3"), line("M16 7.6C16.7 6.2 17.5 4.8 17.5 3"), line(seg(12, 18, 12, 21))]


@icon("womb", "body", "The uterus with fallopian tubes and ovaries", tags=["uterus", "gynecology", "fertility", "pregnancy", "ovaries", "women"], aliases=["uterus"])
def _(S):
    d = _pick(S,
              "M8 6H16C17 6 17.6 6.9 17.3 7.9L15 14.8C14.7 15.6 14 16 14 17V20.5H10V17C10 16 9.3 15.6 9 14.8L6.7 7.9C6.4 6.9 7 6 8 6Z",
              "M8 6H16C17 6 17.6 6.9 17.3 7.9L15 14.8C14.7 15.6 14 16 14 17V19.5Q14 20.5 13 20.5H11Q10 20.5 10 19.5V17C10 16 9.3 15.6 9 14.8L6.7 7.9C6.4 6.9 7 6 8 6Z")
    return [shell(d), detail(poly([(10, 9), (12, 12), (14, 9)], r=S.r)),
            line("M7 7C5.5 5.2 3.5 5.5 3.2 7.5"), line("M17 7C18.5 5.2 20.5 5.5 20.8 7.5"),
            shell(circle(4, 10.5, 1.5)), shell(circle(20, 10.5, 1.5))]


@icon("thyroid", "body", "The butterfly-shaped thyroid gland", tags=["gland", "endocrine", "hormone", "throat", "organ"])
def _(S):
    d = _pick(S,
              "M12 11C11 11 10.4 10.3 10 9L6.5 3.2C5.3 6.5 3.5 10.5 3.5 14C3.5 17.5 5 19.8 7 19.5C8.8 19.2 9.5 17.5 10 16C10.5 14.8 11.2 14.3 12 14.3"
              "C12.8 14.3 13.5 14.8 14 16C14.5 17.5 15.2 19.2 17 19.5C19 19.8 20.5 17.5 20.5 14C20.5 10.5 18.7 6.5 17.5 3.2L14 9C13.6 10.3 13 11 12 11Z",
              "M12 11C11 11 10.4 10.3 10 9L7.4 4.3C7 3.6 6.1 3.6 5.8 4.4C4.5 7.6 3.5 11 3.5 14C3.5 17.5 5 19.8 7 19.5C8.8 19.2 9.5 17.5 10 16C10.5 14.8 11.2 14.3 12 14.3"
              "C12.8 14.3 13.5 14.8 14 16C14.5 17.5 15.2 19.2 17 19.5C19 19.8 20.5 17.5 20.5 14C20.5 11 19.5 7.6 18.2 4.4C17.9 3.6 17 3.6 16.6 4.3L14 9C13.6 10.3 13 11 12 11Z")
    return [shell(d, stroke_miterlimit="2"), line(seg(12, 3, 12, 8))]


# --------------------------------------------------------------------------- skeleton

_BONE = "M7 10A2.5 2.5 0 1 0 3.14 12A2.5 2.5 0 1 0 7 14L17 14A2.5 2.5 0 1 0 20.86 12A2.5 2.5 0 1 0 17 10Z"


@icon("bone", "body", "A single bone", tags=["skeleton", "anatomy", "fracture", "orthopedic", "calcium"])
def _(S):
    return [shell(_rot(_BONE, -45, k=0.98), stroke_miterlimit="2")]


@icon("skull", "body", "A human skull, front view", tags=["skeleton", "head", "anatomy", "death", "danger", "halloween"])
def _(S):
    d = _pick(S, "M12 3C7.3 3 4 6.3 4 10.5C4 13 5.2 14.8 7 15.7V21H17V15.7C18.8 14.8 20 13 20 10.5C20 6.3 16.7 3 12 3Z",
              "M12 3C7.3 3 4 6.3 4 10.5C4 13 5.2 14.8 7 15.7V19C7 20.1 7.9 21 9 21H15C16.1 21 17 20.1 17 19V15.7C18.8 14.8 20 13 20 10.5C20 6.3 16.7 3 12 3Z")
    return [shell(d), dot(8.8, 11, 2), dot(15.2, 11, 2), detail(seg(12, 13.5, 12, 15)),
            detail(seg(10.3, 18, 10.3, 21)), detail(seg(13.7, 18, 13.7, 21))]


@icon("spine", "body", "A column of vertebrae", tags=["vertebrae", "backbone", "back", "posture", "chiropractic", "skeleton"], aliases=["backbone"])
def _(S):
    parts = []
    for y in (3, 9.5, 16):
        pts = [(8, y), (16, y), (20, y + 1.75), (16, y + 3.5), (8, y + 3.5), (4, y + 1.75)]
        parts.append(shell(poly(pts, closed=True, r=min(S.r, 1)), stroke_miterlimit="2"))
    return parts


@icon("ribs", "body", "A rib cage, front view", tags=["ribcage", "chest", "skeleton", "thorax", "anatomy"])
def _(S):
    parts = [line(seg(12, 3, 12, 16))]
    for y in (5, 9, 13):
        parts.append(line(f"M10 {y}C6.5 {y} 4.5 {y + 1.5} 4.5 {y + 4.5}"))
        parts.append(line(f"M14 {y}C17.5 {y} 19.5 {y + 1.5} 19.5 {y + 4.5}"))
    return parts


@icon("skeleton", "body", "A simple human skeleton", tags=["bones", "anatomy", "x-ray", "halloween", "skull"])
def _(S):
    return [
        shell(ellipse(12, 4.9, 3, 3)), dot(10.9, 4.9, 1), dot(13.1, 4.9, 1),
        line(seg(12, 8.6, 12, 15)),
        line("M6.5 16L7.5 9.5H16.5L17.5 16"),
        line(seg(9.5, 12, 14.5, 12)),
        shell(rect(9, 15, 6, 2.5, min(S.R, 1.25))),
        line(seg(10, 17.5, 9, 21)), line(seg(14, 17.5, 15, 21)),
    ]


# --------------------------------------------------------------------------- cells & fluids

@icon("blood-drop", "body", "A drop of blood", tags=["blood", "donate", "drop", "donor", "bleed", "type"], aliases=["blood"])
def _(S):
    d = _pick(S, "M12 2.5C12 2.5 18.5 9.8 18.5 14.5A6.5 6.5 0 0 1 5.5 14.5C5.5 9.8 12 2.5 12 2.5Z",
              "M11.1 3.5Q12 2.5 12.9 3.5C14.5 5.4 18.5 10.3 18.5 14.5A6.5 6.5 0 0 1 5.5 14.5C5.5 10.3 9.5 5.4 11.1 3.5Z")
    return [shell(d, stroke_miterlimit="8" if S.name == "line" else "4"), detail("M9 14.5A3 3 0 0 0 12 17.5")]


@icon("dna", "body", "A DNA double helix", tags=["genetics", "gene", "helix", "biology", "genome", "science"])
def _(S):
    return [
        line("M7 3C7 7.5 17 7.5 17 12C17 16.5 7 16.5 7 21"),
        line("M17 3C17 7.5 7 7.5 7 12C7 16.5 17 16.5 17 21"),
        line(seg(8.5, 4.5, 15.5, 4.5)), line(seg(8.5, 19.5, 15.5, 19.5)), line(seg(9.2, 12, 14.8, 12)),
    ]


@icon("cell", "body", "A living cell with its nucleus", tags=["biology", "cell", "nucleus", "microbiology", "organism", "science"])
def _(S):
    d = "M12 3.5C16.8 3.5 20.5 6.8 20.5 11.5C20.5 16.8 16.8 20.5 11.8 20.5C6.8 20.5 3.5 17 3.5 12.3C3.5 7.2 7.2 3.5 12 3.5Z"
    return [shell(d), detail(circle(13.5, 10, 3)), dot(8, 14.8, 1.25), detail("M12.5 16.5C13.8 17.2 15.3 16.8 16.3 15.5")]


@icon("neuron", "body", "A nerve cell with dendrites and an axon", tags=["nerve", "neurology", "brain", "synapse", "neural", "science"])
def _(S):
    return [
        shell(circle(7.5, 7.5, 3)),
        line(seg(9.6, 9.6, 16, 16)), line("M20 16.8L16 16L16.8 20"),
        dot(20.5, 17, 1.3), dot(17, 20.5, 1.3),
        line("M5.5 5.2L3 3.5"), line("M4.5 8.5L2.5 9"), line("M8.6 4.6L9.2 2.5"), line("M10.3 6.8L12.5 5.5"), line("M6.7 10.4L6 12.5"),
    ]


@icon("vein", "body", "A blood vessel carrying blood cells", tags=["blood vessel", "artery", "circulation", "vascular", "blood"], aliases=["blood-vessel"])
def _(S):
    return [
        line("M3 8C8 8 9.5 5 15 5H21"), line("M3 16C8 16 9.5 13 15 13H21"),
        dot(7.3, 12.1, 1.5), dot(12.3, 10.3, 1.5), dot(17.3, 9, 1.5),
    ]


@icon("muscle-fiber", "body", "A spindle-shaped muscle with its fibres", tags=["muscle", "fibre", "tissue", "anatomy", "strength"], aliases=["muscle"])
def _(S):
    body = _pick(S, "M5.5 12C8 6.5 16 6.5 18.5 12C16 17.5 8 17.5 5.5 12Z", "M5.9 11.3C8.5 6.5 15.5 6.5 18.1 11.3Q18.5 12 18.1 12.7C15.5 17.5 8.5 17.5 5.9 12.7Q5.5 12 5.9 11.3Z")
    return [
        shell(body, stroke_miterlimit="2"),
        line(seg(2, 12, 5.5, 12)), line(seg(18.5, 12, 22, 12)),
        detail("M8.5 10.2C10.5 9.4 13.5 9.4 15.5 10.2"), detail("M8.5 13.8C10.5 14.6 13.5 14.6 15.5 13.8"),
    ]
