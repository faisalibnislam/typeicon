"""TypeIcon Core: faces (batch 001): expressive faces, animal faces, emotion symbols and face masks.

Most faces share the emotions family construction: one face outline (usually the r 9 circle) with the
features inside it. Line eyes are crisp upright bars and Line strokes end square; Rounded eyes are soft ovals
and strokes end round. Filled is a solid face with the features cut out (open mouths become holes). Props that
overlap the face edge (hands, tears, a halo, horns) cut the face outline with a clean gap.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, Style, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "faces"
FILL = Style("filled", "round", "round", R=4.0, r=1.5)  # pseudo-style: feature geometry for the Filled design
FACE = circle(12, 12, 9)
GAP = 1.75


class Hole(Part):
    """A closed feature (open mouth) drawn as an outline in Line/Rounded and cut out whole in Filled."""


class Inset(Part):
    """A stroke inside a Hole (teeth, a tongue line): a detail in Line/Rounded, kept solid inside the Filled hole."""


def hole(d):
    return Hole("detail", d, {})


def inset(d):
    return Inset("detail", d, {})


def mark(d):
    """Solid feature (eye, tear): solid in Line/Rounded, cut out of the Filled face."""
    return Part("dot", d)


def L(S, a, b):
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx, cy):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rpts(pts, deg, cx, cy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def thick(d, w, S):
    return path_to_d(ST(d, w, S.cap, S.join))


# --------------------------------------------------------------------------- features

def eye(S, x, y=10, k=1.0):
    return mark(rect(x - 1.1 * k, y - 1.6 * k, 2.2 * k, 3.2 * k) if S.name == "line" else ellipse(x, y, 1.2 * k, 1.6 * k))


def eyes(S, y=10, dx=3):
    return [eye(S, 12 - dx, y), eye(S, 12 + dx, y)]


def happy_eye(x, y=10.5, r=1.75):
    """Closed laughing eye (an upturned arc)."""
    return detail(arc(x, y, r, 180, 360))


def calm_eye(x, y=9.5, r=1.75):
    """Closed resting eye (a downturned arc)."""
    return detail(arc(x, y, r, 0, 180))


def lidded(S, x, y, look=0.0, w=1.9, pr=1.35):
    """Half-closed eye: a flat lid with the pupil hanging below it, shifted by `look`."""
    lid = ST(seg(x - w, y, x + w, y), 2, S.cap, S.join)
    cx = x + look
    half = P(f"M{fmt(cx - pr)} {fmt(y)}A{fmt(pr)} {fmt(pr)} 0 0 0 {fmt(cx + pr)} {fmt(y)}Z")
    half = transform_path(half, (1, 0, 0, 1, 0, 0.6))
    return mark(path_to_d(U(lid, half)))


def glossy(x, y, r, hx=-0.75, hy=-0.75, hr=0.8):
    """Big round eye with a shine highlight."""
    return mark(path_to_d(D(P(circle(x, y, r)), P(circle(x + hx, y + hy, hr)))))


def heart(cx, cy, s, S):
    """Small heart centred on (cx, cy), about 7.6 * s wide; sharp in Line, soft in Rounded."""
    sharp = "M12 20L4.4 12.6A4.6 4.6 0 0 1 11 6.3L12 7.3L13 6.3A4.6 4.6 0 0 1 19.6 12.6Z"
    soft = "M10.6 18.6L4.4 12.6A4.6 4.6 0 0 1 11 6.3L11.3 6.6Q12 7.3 12.7 6.6L13 6.3A4.6 4.6 0 0 1 19.6 12.6L13.4 18.6Q12 20 10.6 18.6Z"
    base = P(sharp if S.name == "line" else soft)
    m = (s, 0, 0, s, cx - 12 * s, cy - 12.6 * s)
    return path_to_d(transform_path(base, m))


def star(cx, cy, R, r, S):
    pts = [polar(cx, cy, R if k % 2 == 0 else r, -90 + k * 36) for k in range(10)]
    return poly(pts, closed=True, r=L(S, 0, 0.35))


def drop(cx, top, r, cy):
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + r * 0.4)} {fmt(top + (cy - top) * 0.4)} {fmt(cx + r)} {fmt(cy - r * 0.5)} {fmt(cx + r)} {fmt(cy)}"
            f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx - r)} {fmt(cy)}"
            f"C{fmt(cx - r)} {fmt(cy - r * 0.5)} {fmt(cx - r * 0.4)} {fmt(top + (cy - top) * 0.4)} {fmt(cx)} {fmt(top)}Z")


def tear(cx, cy, r, deg=0.0, length=2.3):
    """Tear drop whose round end is centred on (cx, cy), tip pointing up and turned clockwise by deg."""
    d = drop(cx, cy - r * length, r, cy)
    return rot(d, deg, cx, cy) if deg else d


def mitten(x, y, w, h, S, thumb="left", tilt=0.0):
    """Open hand seen from the palm: a rounded palm with a thumb to one side."""
    palm = rect(x, y, w, h, L(S, 1.2, min(w, h) / 2 - 0.2))
    if thumb == "left":
        th = rect(x - 1.7, y + h * 0.35, 3.2, 2.4, L(S, 0.6, 1.2))
        th = rot(th, 40, x, y + h * 0.35 + 1.2)
    else:
        th = rect(x + w - 1.5, y + h * 0.35, 3.2, 2.4, L(S, 0.6, 1.2))
        th = rot(th, -40, x + w, y + h * 0.35 + 1.2)
    d = union(palm, th)
    return rot(d, tilt, x + w / 2, y + h / 2) if tilt else d


def hand(x, y, S, n=2, fw=3.0, fl=2.6, ph=4.4, thumb="left", deg=0.0, tl=3.0, lens=None, seps=True, solid=False):
    """Small open hand: `n` finger capsules above a palm (top-left corner x, y) and a thumb; returns [shell, details].

    Fingers run from y - fl (or y - lens[i]) down into the palm; the finger separations are details (knocked out in
    Filled). The whole hand is turned clockwise by `deg` about the palm centre.
    """
    w = n * fw
    cx, cy = x + w / 2, y + ph / 2
    r = fw / 2
    lens = lens or [fl] * n
    regs = [P(rect(x, y, w, ph, L(S, 0.8, min(2.2, ph / 2))))]
    for i in range(n):
        fx = x + r + i * fw
        regs.append(ST(seg(fx, y - lens[i] + r, fx, y + 1), fw, "round", "round"))
    if thumb == "left":
        regs.append(ST(seg(x + 0.9, y + ph * 0.55, x + 0.9 - tl * 0.62, y + ph * 0.55 - tl * 0.78), 2.8, "round", "round"))
    elif thumb == "right":
        regs.append(ST(seg(x + w - 0.9, y + ph * 0.55, x + w - 0.9 + tl * 0.62, y + ph * 0.55 - tl * 0.78), 2.8, "round", "round"))
    region = U(*regs)
    d = path_to_d(region)
    sl = [seg(x + i * fw, y - min(lens[i - 1], lens[i]) + r + 0.2, x + i * fw, y + 0.6) for i in range(1, n)] if seps else []
    if deg:
        d = rot(d, deg, cx, cy)
        sl = [rot(sd, deg, cx, cy) for sd in sl]
    if solid:  # tiny hands read best as silhouettes; they stay solid in every style
        return [mark(d)]
    return [shell(d), *[detail(sd) for sd in sl]]


SMILE = "M8 14.5C9 16.3 10.4 17 12 17C13.6 17 15 16.3 16 14.5"
FROWN = "M8.5 17.5C9.3 16 10.5 15.3 12 15.3C13.5 15.3 14.7 16 15.5 17.5"
GRIN = "M7.5 13.5H16.5C16.5 16.4 14.5 18.3 12 18.3C9.5 18.3 7.5 16.4 7.5 13.5Z"


# --------------------------------------------------------------------------- the face builder

def _region(p):
    if p.kind == "shell" or isinstance(p, Hole):
        return U(P(p.d), ST(p.d, 2))
    if p.kind in ("line", "detail"):
        return ST(p.d, 2, "round", "round")
    return P(p.d)


def _grow(path, g):
    return U(path, ST(path_to_d(path), 2 * g, "round", "round"))


def _cutter(props):
    regs = [_region(p) for p in props if p.kind != "detail"]
    return _grow(U(*regs), GAP) if regs else None


def face(name, description, tags, aliases=(), over=None, base=None):
    """Register a face. `fn(S)` returns the features; `over(S)` returns props overlapping the face edge.

    `base` is the face outline: a d-string or a function of the style (default: the r 9 circle).
    Prop details (finger lines on a hand) are knocked out of the prop in Filled.
    """
    def outline(S):
        if base is None:
            return FACE
        return base(S) if callable(base) else base

    def deco(fn):
        def draw(S):
            b = outline(S)
            props = over(S) if over else []
            cutter = _cutter(props) if props else None
            if cutter is not None:
                ring = solid(path_to_d(D(ST(b, 2, S.cap, S.join), cutter)))
            else:
                ring = shell(b)
            return [ring, *fn(S), *props]

        def filled():
            b = outline(FILL)
            body = U(P(b), ST(b, 2))
            props = over(FILL) if over else []
            cutter = _cutter(props) if props else None
            if cutter is not None:
                body = D(body, cutter)
            feats = fn(FILL)
            for p in feats:
                if isinstance(p, Inset):
                    continue
                if isinstance(p, Hole) or p.kind == "shell":
                    body = D(body, U(P(p.d), ST(p.d, 2)))
                elif p.kind in ("detail", "line"):
                    body = D(body, ST(p.d, 2, "round", "round"))
                elif p.kind in ("dot", "solid"):
                    body = D(body, P(p.d))
            extras = [ST(p.d, 2, "butt", "miter") for p in feats if isinstance(p, Inset)]
            shells = [U(P(p.d), ST(p.d, 2)) for p in props if p.kind == "shell"]
            if shells:
                reg = U(*shells)
                knocks = [ST(p.d, 2, "round", "round") for p in props if p.kind == "detail"]
                if knocks:
                    reg = D(reg, *knocks)
                extras.append(reg)
            for p in props:
                if p.kind == "line":
                    extras.append(ST(p.d, 2.5, "round", "round"))
                elif p.kind in ("dot", "solid"):
                    extras.append(P(p.d))
            return U(body, *extras)

        return icon(name, CAT, description, tags=tags, aliases=aliases, filled=filled)(draw)
    return deco


# ============================================================================ chunk 1: joy, love and attitude

@face("tears-of-joy", "Laughing face with tears springing from both eyes",
      ["laugh", "lol", "crying laughing", "hilarious", "funny", "joy", "emoji"],
      over=lambda S: [mark(tear(3.7, 14.2, 1.7, 35)), mark(tear(20.3, 14.2, 1.7, -35))])
def _(S):
    return [happy_eye(8.75), happy_eye(15.25), hole(GRIN)]


def _melt(S):
    return ("M5.2 13.2A7.3 7.3 0 1 1 18.8 13.2C19.4 15.2 21.8 16.4 21.8 18.6C21.8 20.2 20.8 21 19 21H5"
            "C3.2 21 2.2 20.2 2.2 18.6C2.2 16.4 4.6 15.2 5.2 13.2Z")


@face("melting-face", "Smiling face melting down into a puddle",
      ["melting", "melt", "hot", "embarrassed", "overwhelmed", "dread", "emoji"], base=_melt)
def _(S):
    return [eye(S, 9.2, 8.3), eye(S, 14.8, 8.8), detail("M8.4 12C9.5 13.4 11 14 12.6 13.9C13.8 13.8 14.8 13.3 15.6 12.6"),
            mark(drop(7, 14.6, 1.3, 17.6))]


@face("innocent-face", "Smiling face with a halo above the head",
      ["innocent", "angel", "halo", "saint", "good", "blessed", "emoji"],
      base=circle(12, 13, 8.5),
      over=lambda S: [line(ellipse(12, 3.6, 6.5, 1.8))])
def _(S):
    return [happy_eye(8.75, 12), happy_eye(15.25, 12), detail("M8.3 15.5C9.3 17.2 10.6 17.9 12 17.9C13.4 17.9 14.7 17.2 15.7 15.5")]


@face("adoring-face", "Smiling face with closed eyes and small hearts around the head",
      ["love", "adore", "affection", "hearts", "in love", "grateful", "emoji"],
      over=lambda S: [mark(heart(4.3, 4.6, 0.36, S)), mark(heart(19.9, 4.2, 0.3, S)), mark(heart(20.2, 18.4, 0.36, S))])
def _(S):
    return [happy_eye(8.75), happy_eye(15.25), detail(SMILE)]


@face("zany-face", "Goofy face with one big eye, one small eye and the tongue hanging out",
      ["zany", "crazy", "goofy", "silly", "wacky", "wild", "emoji"])
def _(S):
    return [detail(circle(8.3, 9.3, 2.6)), dot(8.8, 9.8, 1.05), eye(S, 15.8, 8.6, 0.85),
            detail(seg(6.8, 15.2, 17, 12.8)),
            hole("M12.6 14.3L16.2 13.4L16.9 16.2A1.9 1.9 0 0 1 13.2 17.1Z")]


@face("hugging-face", "Smiling face with two open hands raised as if offering a hug",
      ["hug", "hugs", "embrace", "warm", "welcome", "cuddle", "emoji"],
      over=lambda S: [*hand(2.2, 16, S, thumb="right", deg=-15), *hand(15.8, 16, S, thumb="left", deg=15)])
def _(S):
    return [happy_eye(8.75, 9.8), happy_eye(15.25, 9.8), detail("M9.5 14C10.2 15.1 11 15.6 12 15.6C13 15.6 13.8 15.1 14.5 14")]


@face("smirking-face", "Face with sideways half-closed eyes and a lopsided smile",
      ["smirk", "smug", "sly", "cheeky", "flirt", "suggestive", "emoji"])
def _(S):
    return [lidded(S, 8.5, 9.5, 0.7), lidded(S, 15.5, 9.5, 0.7), detail("M8.5 16H12.5C14.3 16 15.6 15.2 16.4 13.5")]


@face("unamused-face", "Face with half-closed sideways eyes and a flat turned-down mouth",
      ["unamused", "bored", "unimpressed", "annoyed", "meh", "side eye", "emoji"])
def _(S):
    return [lidded(S, 8.5, 9.5, -0.7), lidded(S, 15.5, 9.5, -0.7), detail("M9 17C9.5 16 10.3 15.7 12 15.7C13.7 15.7 14.5 16 15 17")]


@face("eye-roll-face", "Face rolling its eyes upward with a flat mouth",
      ["eye roll", "rolling eyes", "annoyed", "whatever", "sarcasm", "exasperated", "emoji"])
def _(S):
    return [detail(ellipse(8.4, 10, 2.3, 2.8)), detail(ellipse(15.6, 10, 2.3, 2.8)), dot(8.4, 8.6, 1.1), dot(15.6, 8.6, 1.1),
            detail(seg(9, 16.3, 15, 16.3))]


@face("lying-face", "Face with a long pointed nose and a nervous smile",
      ["lie", "liar", "lying", "fib", "dishonest", "long nose", "emoji"],
      over=lambda S: [shell(L(S, poly([(10.8, 11), (22, 12.3), (22, 13.7), (10.8, 15)], closed=True),
                                    "M10.8 12.3Q10.8 11 12.1 11.15L20.9 12.2A0.8 0.8 0 0 1 20.9 13.8L12.1 14.85Q10.8 15 10.8 13.7Z"))])
def _(S):
    return [eye(S, 8.5, 8.3), eye(S, 14.5, 8.3), detail("M7.8 18C8.8 17 9.8 17 10.8 17.8C11.8 18.6 12.8 18.6 13.8 17.8C14.6 17.2 15.3 17 16 17.2")]


@face("drooling-face", "Dreamy face with a slack open mouth and a drop of drool",
      ["drool", "drooling", "hungry", "craving", "yummy", "desire", "emoji"])
def _(S):
    return [calm_eye(8.75), calm_eye(15.25), hole(ellipse(11, 15.2, 2.6, 1.9)), mark(drop(14.6, 15.8, 1.35, 18.6))]


@face("woozy-face", "Tipsy face with uneven eyes, a wavy mouth and blushing cheeks",
      ["woozy", "tipsy", "drunk", "dizzy", "intoxicated", "buzzed", "emoji"])
def _(S):
    return [eye(S, 8.5, 9.6, 1.1), lidded(S, 15.5, 10, 0.3, 1.8, 1.2),
            detail("M8.5 16.2C9.4 15.1 10.3 15.1 11.2 15.9C12.1 16.7 13 16.7 13.9 15.9C14.6 15.3 15.2 15.1 15.9 15.2"),
            dot(5.8, 13.2, 1.1), dot(18.2, 13.2, 1.1)]


@face("monocle-face", "Face wearing a monocle with one raised brow",
      ["monocle", "posh", "fancy", "inspect", "scrutinize", "curious", "emoji"])
def _(S):
    return [detail(arc(8.5, 8.4, 2.2, 205, 335)), eye(S, 8.5, 10.8), detail(circle(15.4, 10.3, 2.9)), dot(15.4, 10.3, 1.1),
            detail("M16.9 13.6C17.6 15 17.6 16.6 17 18"), detail(seg(8.6, 16.3, 12.4, 16.3))]


@face("pleading-face", "Face with huge shining eyes and a small frown",
      ["pleading", "puppy eyes", "please", "begging", "cute", "sad", "emoji"])
def _(S):
    k = L(S, 0, 1)
    return [detail(seg(6.8, 7.6 + 0.1 * k, 9.8, 6.5)), detail(seg(17.2, 7.6 + 0.1 * k, 14.2, 6.5)),
            glossy(8.6, 11.3, 2.5), glossy(15.4, 11.3, 2.5), detail("M10 17.7Q12 16.1 14 17.7")]


def _dashes(cx, cy, r, n, frac, start=-90.0):
    step = 360 / n
    return [line(arc(cx, cy, r, start + i * step - step * frac / 2, start + i * step + step * frac / 2)) for i in range(n)]


@icon("dotted-line-face", CAT, "Face drawn in a dashed outline as if fading away",
      tags=["dotted line face", "invisible", "fading", "disappear", "hidden", "introvert", "emoji"])
def _(S):
    return [*_dashes(12, 12, 9, 12, 0.42), dot(9, 10, 1.2), dot(15, 10, 1.2),
            line(arc(12, 11.5, 4.5, 25, 50)), line(arc(12, 11.5, 4.5, 78, 102)), line(arc(12, 11.5, 4.5, 130, 155))]


def _sigh_puff(S):
    return [shell(union(circle(17.4, 17, 2.1), circle(19.9, 15.4, 2), circle(20.2, 18.4, 1.7)))]


@face("exhaling-face", "Face with closed eyes blowing out a small puff of air in a long sigh",
      ["exhale", "sigh", "relief", "phew", "tired", "breathe out", "emoji"], over=_sigh_puff)
def _(S):
    return [calm_eye(8.4, 9.8), calm_eye(14.8, 9.8), hole(ellipse(12.2, 15.8, 1.2, 1.3))]


# ============================================================================ chunk 2: blush, bother and bumps

def _salute_hand(S):
    fingers = ST(seg(4.6, 9.4, 11.4, 5.2), 4.4, "round", "round")
    wrist = ST(seg(4.4, 9.8, 3.2, 13.6), 4.2, "round", "round")
    return [shell(path_to_d(U(fingers, wrist))), detail(seg(5.6, 8.9, 10.8, 5.7))]


@face("saluting-face", "Face with a flat hand raised to the brow in a salute",
      ["salute", "saluting", "respect", "yes sir", "military", "duty", "emoji"], over=_salute_hand)
def _(S):
    return [eye(S, 11.4, 12.3), eye(S, 16.2, 11.4), detail(seg(10, 17, 15.8, 16.2))]


@face("flushed-face", "Face with wide eyes, a tiny mouth and blushing cheeks",
      ["flushed", "embarrassed", "blush", "shocked", "awkward", "red faced", "emoji"])
def _(S):
    return [detail(circle(8.7, 9.6, 2.2)), eye(S, 8.7, 9.6, 0.55), detail(circle(15.3, 9.6, 2.2)), eye(S, 15.3, 9.6, 0.55),
            hole(L(S, rect(10.9, 15.2, 2.2, 2.4, 0.4), ellipse(12, 16.4, 1.2, 1.3))), dot(6.4, 14.4, 1.6), dot(17.6, 14.4, 1.6)]


@face("blushing-face", "Smiling face with closed eyes and blush lines on the cheeks",
      ["blushing", "blush", "shy", "flattered", "happy", "sweet", "emoji"])
def _(S):
    return [happy_eye(8.75, 10), happy_eye(15.25, 10),
            detail(seg(5.4, 15, 6.4, 13.2)), detail(seg(8.2, 15, 9.2, 13.2)), detail(seg(14.8, 15, 15.8, 13.2)), detail(seg(17.6, 15, 18.6, 13.2)),
            detail("M10 16.7Q12 18.2 14 16.7")]


@face("determined-face", "Determined face with a headband, lowered brows and a tight mouth",
      ["determined", "focused", "motivated", "fighting spirit", "headband", "resolve", "emoji"],
      base=circle(11, 12.6, 8.3),
      over=lambda S: [dot(19.6, 8, 1.5), line(seg(20.4, 7.2, 22.4, 4.4)), line(seg(20.6, 8.8, 22.6, 11.2))])
def _(S):
    k = L(S, 0, 0.5)
    return [detail(seg(4.2, 8, 18, 8)),
            mark(poly([(6.4, 10.9), (9.8, 11.9), (9.8, 13.8), (6.4, 13.8)], closed=True, r=k)),
            mark(poly([(15.6, 10.9), (12.2, 11.9), (12.2, 13.8), (15.6, 13.8)], closed=True, r=k)),
            detail(seg(8.5, 17.4, 13.5, 17.4))]


def _pout_base(S):
    return union(circle(11.4, 12, 8.6), circle(16.2, 15.4, 5.2))


@face("pouting-face", "Sulking face with pushed-out lips, a puffed cheek and lowered brows",
      ["pout", "pouting", "sulk", "sulking", "grumpy", "huff", "emoji"], base=_pout_base)
def _(S):
    return [detail(seg(5.8, 7.2, 9.2, 8.6)), detail(seg(16.4, 7.2, 13, 8.6)), eye(S, 7.6, 11.2), eye(S, 13.8, 11.2),
            hole(ellipse(9.4, 16.4, 1.6, 1.3))]


def _puff(cx, cy, s=1.0, flip=False):
    k = -1 if flip else 1
    return mark(union(circle(cx, cy, 1.6 * s), circle(cx + 1.7 * s * k, cy - 0.9 * s, 1.7 * s), circle(cx + 1.4 * k * s, cy + 1.1 * s, 1.2 * s)))


@face("fuming-face", "Angry face with gritted teeth and steam puffing from both sides of the head",
      ["fuming", "furious", "steaming", "rage", "livid", "angry", "emoji"],
      over=lambda S: [_puff(3.4, 11.6, 0.85, True), _puff(20.6, 11.6, 0.85)])
def _(S):
    return [detail(seg(7, 7.6, 10.4, 9.2)), detail(seg(17, 7.6, 13.6, 9.2)), eye(S, 9, 11.6, 0.85), eye(S, 15, 11.6, 0.85),
            hole(rect(7.6, 14.4, 8.8, 3.8, L(S, 0.8, 1.9))), inset(seg(10.5, 14.4, 10.5, 18.2)), inset(seg(13.5, 14.4, 13.5, 18.2))]


def _grawlix():
    bar = P(rect(6.3, 13.4, 11.4, 5.4, 1.2))
    k = 1.1
    cuts = [P(rect(7.9, 14.4, k, 3.4)), P(rect(9.6, 14.4, k, 3.4)), P(rect(7.4, 15.1, 3.8, k)), P(rect(7.4, 16.6, 3.8, k)),
            P(rect(12.3, 14.3, 1.3, 2.3)), P(circle(12.95, 17.5, 0.7)),
            P(rect(14.7, 14.3, 1.3, 2.3)), P(circle(15.35, 17.5, 0.7))]
    return path_to_d(D(bar, *cuts))


@face("cursing-face", "Angry face with a bar of symbols covering the mouth",
      ["cursing", "swearing", "profanity", "censored", "rage", "grawlix", "emoji"])
def _(S):
    return [detail(seg(7, 7.4, 10.4, 9)), detail(seg(17, 7.4, 13.6, 9)), eye(S, 9, 11, 0.85), eye(S, 15, 11, 0.85), mark(_grawlix())]


@face("cross-eyed-face", "Goofy face with both pupils turned toward the nose and an open grin",
      ["cross eyed", "goofy", "silly", "derp", "dizzy", "confused", "emoji"])
def _(S):
    return [detail(ellipse(8.4, 9.6, 2.3, 2.8)), detail(ellipse(15.6, 9.6, 2.3, 2.8)), eye(S, 9.5, 10.2, 0.62), eye(S, 14.5, 10.2, 0.62),
            hole(L(S, "M8 14.4H16C16 16.8 14.2 18.4 12 18.4C9.8 18.4 8 16.8 8 14.4Z",
                   "M9.2 14.4H14.8Q16 14.4 15.9 15.6C15.6 17.4 14 18.4 12 18.4C10 18.4 8.4 17.4 8.1 15.6Q8 14.4 9.2 14.4Z"))]


@face("gap-toothed-grin", "Wide grinning face showing upper teeth with one tooth missing",
      ["gap tooth", "missing tooth", "toothless", "kid", "grin", "tooth fairy", "emoji"])
def _(S):
    return [*eyes(S, 9.2), hole("M6.6 12.8H17.4C17.4 16.3 15.1 18.9 12 18.9C8.9 18.9 6.6 16.3 6.6 12.8Z"),
            inset(seg(7.4, 14.6, 10.5, 14.6)), inset(seg(13.5, 14.6, 16.6, 14.6))]


@face("smiling-tear-face", "Smiling face with happy closed eyes and a single tear on one cheek",
      ["smiling through tears", "bittersweet", "touched", "grateful", "proud", "moved", "emoji"])
def _(S):
    return [happy_eye(8.75, 10), happy_eye(15.25, 10), mark(tear(6.1, 15.1, 1.3)),
            detail("M9.2 14.6C10.1 16 11 16.6 12.1 16.6C13.3 16.6 14.3 16 15.2 14.6")]


@face("holding-back-tears", "Face with glossy eyes brimming with tears and a wobbly pressed mouth",
      ["holding back tears", "teary", "emotional", "moved", "about to cry", "sad", "emoji"])
def _(S):
    return [detail(seg(6.6, 7.2, 9.6, 6.2)), detail(seg(17.4, 7.2, 14.4, 6.2)),
            glossy(8.6, 10.6, 2.3), glossy(15.4, 10.6, 2.3), mark(tear(6, 14.2, 1.1, 0, 2)), mark(tear(18, 14.2, 1.1, 0, 2)),
            detail(poly([(8.8, 17), (10.4, 16), (12, 17), (13.6, 16), (15.2, 17)], r=L(S, 0, 0.6)))]


def _cloud(S):
    return path_to_d(U(P(circle(6.6, 17, 3.3)), P(circle(11.6, 15.4, 4.1)), P(circle(16.9, 16.8, 3.4)),
                       P(rect(6.6, 16.5, 10.3, 3.8))))


@face("face-in-clouds", "Face half hidden behind a puffy cloud with only the eyes showing",
      ["head in the clouds", "daydream", "absent minded", "foggy", "spaced out", "dreamy", "emoji"],
      over=lambda S: [shell(_cloud(S))])
def _(S):
    return [eye(S, 9, 7.7), eye(S, 15, 7.7)]


def _bump(S):
    return union(circle(12, 13, 8.5), circle(15, 4.6, 2.5))


@face("knocked-out-face", "Dazed face with crossed-out eyes and a bump on top of the head",
      ["knocked out", "ko", "dazed", "unconscious", "dizzy", "beaten", "emoji"], base=_bump)
def _(S):
    return [detail(seg(6.9, 10.1, 9.9, 13.1)), detail(seg(9.9, 10.1, 6.9, 13.1)),
            detail(seg(14.1, 10.1, 17.1, 13.1)), detail(seg(17.1, 10.1, 14.1, 13.1)), hole(ellipse(12, 17.3, 1.5, 1.4))]


@face("injured-face", "Face with a bandage around the head and a plaster on one cheek",
      ["injured", "hurt", "bandage", "wounded", "accident", "ouch", "emoji"])
def _(S):
    k = L(S, 0.3, 0.9)
    return [detail(seg(4.5, 7, 19.5, 7)), eye(S, 8.8, 10.8, 0.9), eye(S, 15.2, 10.8, 0.9),
            mark(rot(rect(14.4, 14.2, 4.6, 2.2, k), -35, 16.7, 15.3)), detail("M8.6 17.6Q10.2 16.4 11.8 17.6")]


@face("cold-face", "Freezing face with chattering teeth and a snowflake beside the head",
      ["cold", "freezing", "chilly", "shivering", "winter", "frozen", "emoji"],
      over=lambda S: [line(seg(19.4, 1.8, 19.4, 7.8)), line(seg(16.8, 3.3, 22, 6.3)), line(seg(16.8, 6.3, 22, 3.3))])
def _(S):
    return [eye(S, 8.6, 10), eye(S, 14.6, 10), hole(rect(7, 13.4, 10, 5, L(S, 0.8, 2))),
            inset(poly([(7.4, 17.9), (9.7, 13.9), (12, 17.9), (14.3, 13.9), (16.6, 17.9)]))]



# ============================================================================ chunk 3: shock, mischief and characters

@face("overheated-face", "Hot face with droopy eyes, the tongue hanging out and sweat flying off",
      ["hot", "overheated", "heatwave", "sweating", "exhausted", "summer", "emoji"])
def _(S):
    return [mark(tear(5.4, 14, 1.2, 0, 2.2)), mark(tear(18.6, 14, 1.2, 0, 2.2)), lidded(S, 8.6, 9.2, 0, 1.9, 1.3), lidded(S, 15.4, 9.2, 0, 1.9, 1.3), detail(seg(7.8, 13.6, 16.2, 13.6)),
            hole("M9.9 13.6V17.6A2.1 2.1 0 0 0 14.1 17.6V13.6Z"), inset(seg(12, 13.6, 12, 16))]


@face("screaming-face", "Long face with hands pressed to the cheeks, wide eyes and a tall open mouth",
      ["scream", "screaming", "horror", "terrified", "shock", "fear", "emoji"],
      base=ellipse(12, 11.6, 6.9, 9.4),
      over=lambda S: [*hand(1.8, 15.6, S, n=3, fw=1.9, ph=3.8, thumb=None, deg=-14, lens=(2.8, 3.6, 3.2), seps=False, solid=True),
                      *hand(16.5, 15.6, S, n=3, fw=1.9, ph=3.8, thumb=None, deg=14, lens=(3.2, 3.6, 2.8), seps=False, solid=True)])
def _(S):
    return [mark(ellipse(9.4, 8.6, 1.5, 2.1) if S.name != "line" else rect(8, 6.6, 2.8, 4, 0.2)),
            mark(ellipse(14.6, 8.6, 1.5, 2.1) if S.name != "line" else rect(13.2, 6.6, 2.8, 4, 0.2)),
            hole(ellipse(12, 15.6, 1.9, 3.2))]


@face("confounded-face", "Frustrated face with tightly squeezed eyes and a zigzag mouth",
      ["confounded", "frustrated", "scrunched", "ugh", "stressed", "upset", "emoji"])
def _(S):
    return [detail(poly([(7, 7.8), (10.2, 9.8), (7, 11.8)], r=S.r)), detail(poly([(17, 7.8), (13.8, 9.8), (17, 11.8)], r=S.r)),
            detail(poly([(7.4, 16.6), (9.2, 14.8), (11, 16.6), (12.8, 14.8), (14.6, 16.6), (16.4, 14.8)], r=L(S, 0, 0.5)))]


@face("nervous-laugh-face", "Grinning face with closed eyes, teeth and a sweat drop on the forehead",
      ["nervous laugh", "awkward", "sweat smile", "phew", "relief", "embarrassed", "emoji"],
      over=lambda S: [mark(tear(19, 6.6, 1.6))])
def _(S):
    return [happy_eye(8.5, 10.3), happy_eye(14.9, 10.3), hole(GRIN), inset(seg(7.5, 15.4, 16.5, 15.4))]


def _long_jaw(S):
    return "M4.5 9.5A7.5 7.5 0 0 1 19.5 9.5V14.2C19.5 18.7 16.3 21.5 12 21.5C7.7 21.5 4.5 18.7 4.5 14.2Z"


@face("jaw-drop-face", "Astonished face with wide eyes and the jaw dropped into a very long open mouth",
      ["jaw drop", "astonished", "shocked", "speechless", "stunned", "omg", "emoji"], base=_long_jaw)
def _(S):
    return [detail(circle(8.8, 8.4, 1.9)), eye(S, 8.8, 8.4, 0.5), detail(circle(15.2, 8.4, 1.9)), eye(S, 15.2, 8.4, 0.5),
            hole(rect(9.6, 12.6, 4.8, 7, L(S, 1, 2.4)))]


def _blown(S):
    zig = poly([(4, 13), (6, 11), (8, 12.6), (10, 10.8), (12, 12.4), (14, 10.8), (16, 12.6), (18, 11), (20, 13)], r=L(S, 0, 0.6))
    return zig + "A8 8 0 0 1 4 13Z"


@face("mind-blown-face", "Face whose head bursts open at the top into a cloud blast",
      ["mind blown", "exploding head", "amazed", "shocked", "wow", "boom", "emoji"], base=_blown,
      over=lambda S: [shell(union(circle(7.6, 4.8, 2.2), circle(12, 3.9, 2.6), circle(16.4, 4.8, 2.2), rect(7.6, 4.4, 8.8, 2.6),
                                   rect(10.7, 6, 2.6, 5.6, L(S, 0.3, 1.2))))])
def _(S):
    return [eye(S, 9, 15, 0.9), eye(S, 15, 15, 0.9), hole(ellipse(12, 18.4, 1.3, 1.2))]


def _puffed(S):
    return union(circle(12, 11, 8), circle(6.7, 15, 4.5), circle(17.3, 15, 4.5))


@face("puffed-cheeks-face", "Face with round inflated cheeks holding its breath",
      ["puffed cheeks", "holding breath", "blowfish", "bloated", "full", "cheeks", "emoji"], base=_puffed)
def _(S):
    return [calm_eye(8.8, 9.2, 1.6), calm_eye(15.2, 9.2, 1.6), hole(ellipse(12, 15.6, 1.4, 1.1))]


@face("duck-face", "Selfie face with pushed-out duck lips and one raised eyebrow",
      ["duck face", "selfie", "pout", "kissy", "posing", "sassy", "emoji"])
def _(S):
    return [detail(arc(15, 7.6, 2.2, 205, 335)), eye(S, 9, 10.4), eye(S, 15, 10.4),
            hole("M8.6 15.6C8.6 13.9 10.8 13.6 12 14.4C13.2 13.6 15.4 13.9 15.4 15.6C15.4 17.3 13.2 17.6 12 16.9C10.8 17.6 8.6 17.3 8.6 15.6Z"),
            inset(seg(9.6, 15.65, 14.4, 15.65))]


@face("biting-lip-face", "Nervous face with raised brows and the upper teeth biting the lower lip",
      ["biting lip", "nervous", "flirty", "anxious", "tempted", "uh oh", "emoji"])
def _(S):
    return [detail(seg(6.8, 7.6, 9.8, 6.6)), detail(seg(17.2, 7.6, 14.2, 6.6)), eye(S, 9, 10.4), eye(S, 15, 10.4),
            detail("M7.8 15.2C9 18.2 15 18.2 16.2 15.2"), hole(rect(10.2, 13.2, 3.6, 3, L(S, 0.3, 1))), inset(seg(12, 13.2, 12, 16.2))]


@face("evil-grin-face", "Scheming face with slanted brows, narrow eyes and a wide toothy grin",
      ["evil grin", "mischief", "scheming", "villain", "sinister", "wicked", "emoji"])
def _(S):
    k = L(S, 0, 0.4)
    return [detail(seg(6.4, 6.9, 10.3, 8.7)), detail(seg(17.6, 6.9, 13.7, 8.7)),
            mark(poly([(6.8, 10.3), (10.3, 11.3), (10.3, 12.5), (6.8, 12.1)], closed=True, r=k)),
            mark(poly([(17.2, 10.3), (13.7, 11.3), (13.7, 12.5), (17.2, 12.1)], closed=True, r=k)),
            hole("M5.8 13.4C8.2 15.4 15.8 15.4 18.2 13.4C17.5 17.4 15 19.2 12 19.2C9 19.2 6.5 17.4 5.8 13.4Z"),
            inset(seg(9.4, 14.6, 9.4, 18.6)), inset(seg(12, 15, 12, 19.2)), inset(seg(14.6, 14.6, 14.6, 18.6))]


def _horns(S):
    left = "M5.2 7.6C4 5.8 3.9 4 4.6 2.4C5.7 4 7.3 4.8 9.6 4.6Z"
    right = "M18.8 7.6C20 5.8 20.1 4 19.4 2.4C18.3 4 16.7 4.8 14.4 4.6Z"
    if S.name != "line":
        left = "M5.2 7.6C4 5.8 3.9 4 4.4 2.8Q4.7 2.2 5.2 2.8C6.2 4.1 7.5 4.7 9.3 4.6Z"
        right = "M18.8 7.6C20 5.8 20.1 4 19.6 2.8Q19.3 2.2 18.8 2.8C17.8 4.1 16.5 4.7 14.7 4.6Z"
    return [shell(left), shell(right)]


@face("devil-face", "Grinning face with two small horns and slanted brows",
      ["devil", "imp", "evil", "naughty", "horns", "mischievous", "emoji"], over=_horns)
def _(S):
    k = L(S, 0, 0.4)
    return [mark(poly([(6.8, 9.4), (10.4, 10.6), (10.4, 12.6), (6.8, 12.6)], closed=True, r=k)),
            mark(poly([(17.2, 9.4), (13.6, 10.6), (13.6, 12.6), (17.2, 12.6)], closed=True, r=k)),
            detail("M7.6 15C8.8 17 10.3 17.9 12 17.9C13.7 17.9 15.2 17 16.4 15")]


@face("cyborg-face", "Face split into a human half and a metal half with a round lens eye",
      ["cyborg", "android", "robot", "bionic", "machine", "sci fi", "emoji"])
def _(S):
    return [detail(seg(12, 3, 12, 21)), eye(S, 8.2, 10), detail("M6.8 14.8C7.8 16.6 9.6 17.4 12 17.4"),
            detail(circle(16.2, 9.6, 2.3)), dot(16.2, 9.6, 1), detail(seg(12, 13.6, 20.9, 13.6)), detail(seg(12, 17.4, 16.2, 17.4))]


def _fuzzy(S):
    n = 13
    bumps = [P(circle(*polar(12, 12.8, 7.6, -90 + i * 360 / n + 360 / n / 2), 1.9)) for i in range(n)]
    horn = P(poly([(10.5, 5.6), (12, 2.4), (13.5, 5.6)], closed=True))
    return path_to_d(U(P(circle(12, 12.8, 7.6)), *bumps, horn))


@face("cute-monster-face", "Fuzzy round monster with one big eye, a small horn and two little fangs",
      ["monster", "cute monster", "cyclops", "creature", "fuzzy", "kids", "emoji"], base=_fuzzy)
def _(S):
    return [detail(circle(12, 11, 3)), eye(S, 12, 11, 0.7), detail("M8.2 15.4C9.6 17.4 14.4 17.4 15.8 15.4"),
            mark(poly([(9.8, 16.8), (11.3, 17.3), (10.6, 18.9)], closed=True)), mark(poly([(14.2, 16.8), (12.7, 17.3), (13.4, 18.9)], closed=True))]


@icon("sun-with-face", CAT, "Smiling sun with a face and short rays all around",
      tags=["sun face", "sunny", "sunshine", "morning", "happy", "weather", "emoji"])
def _(S):
    rays = [line(seg(*polar(12, 12, 8.5, a), *polar(12, 12, 10.5, a))) for a in range(0, 360, 45)]
    return [shell(circle(12, 12, 5.6)), eye(S, 10, 11, 0.62), eye(S, 14, 11, 0.62), detail("M9.8 13.6Q12 15.4 14.2 13.6"), *rays]


def _lemon(S):
    d = rot("M14.2 17.6A4.2 4.2 0 0 0 22.6 17.6Z", -30, 18.4, 17.6)
    rind = rot(arc(18.4, 17.6, 2.3, 10, 170), -30, 18.4, 17.6)
    return [shell(d), detail(rind)]


@face("sour-face", "Puckered face with squeezed eyes next to a lemon wedge",
      ["sour", "lemon", "tart", "bitter", "yuck", "pucker", "emoji"], over=_lemon)
def _(S):
    return [detail(poly([(6.6, 8), (9.8, 9.8), (6.6, 11.6)], r=S.r)), detail(poly([(16.6, 8), (13.4, 9.8), (16.6, 11.6)], r=S.r)),
            hole(ellipse(10.8, 15.4, 1.3, 1.5))]



# ============================================================================ chunk 4: monkeys, cats and reactions

def _monkey(S):
    return union(circle(12, 12.6, 7.4), circle(4.3, 12.2, 2.4), circle(19.7, 12.2, 2.4))


def _muzzle(y=15.2):
    return [dot(10.9, y, 0.75), dot(13.1, y, 0.75), detail(f"M9.2 {fmt(y + 2)}Q12 {fmt(y + 3.8)} 14.8 {fmt(y + 2)}")]


MASK = "M5.6 15.4C4.6 10.4 8.2 7.6 12 10.2C15.8 7.6 19.4 10.4 18.4 15.4"


@face("see-no-evil-monkey", "Monkey face with both hands covering its eyes",
      ["see no evil", "monkey", "oops", "embarrassed", "can't look", "shy", "emoji"], base=_monkey,
      over=lambda S: [*hand(4.6, 10.4, S, n=3, fw=2.2, ph=3.2, thumb=None, deg=-20, lens=(2.2, 3, 2.6), seps=False, solid=True),
                      *hand(12.8, 10.4, S, n=3, fw=2.2, ph=3.2, thumb=None, deg=20, lens=(2.6, 3, 2.2), seps=False, solid=True)])
def _(S):
    return _muzzle(15.8)


@face("hear-no-evil-monkey", "Monkey face with both hands pressed over its ears",
      ["hear no evil", "monkey", "not listening", "la la la", "ignore", "ears", "emoji"], base=_monkey,
      over=lambda S: [*hand(1.6, 12, S, n=3, fw=1.9, ph=3.6, thumb=None, deg=-12, lens=(2.2, 2.8, 2.4), seps=False, solid=True),
                      *hand(16.7, 12, S, n=3, fw=1.9, ph=3.6, thumb=None, deg=12, lens=(2.4, 2.8, 2.2), seps=False, solid=True)])
def _(S):
    return [detail(MASK), eye(S, 9.6, 12.2, 0.8), eye(S, 14.4, 12.2, 0.8), *_muzzle(15.6)]


@face("speak-no-evil-monkey", "Monkey face with both hands covering its mouth",
      ["speak no evil", "monkey", "oops", "secret", "shh", "no comment", "emoji"], base=_monkey,
      over=lambda S: [*hand(5.4, 16.4, S, n=3, fw=2.2, ph=3.2, thumb=None, deg=-62, lens=(2.2, 3, 2.6), seps=False, solid=True),
                      *hand(12, 16.4, S, n=3, fw=2.2, ph=3.2, thumb=None, deg=62, lens=(2.6, 3, 2.2), seps=False, solid=True)])
def _(S):
    return [detail(MASK), eye(S, 9.6, 12.2, 0.8), eye(S, 14.4, 12.2, 0.8)]


def _cat(S):
    r = L(S, 0, 1.2)
    ears = [P(poly([(3.4, 12), (4.4, 2.8), (10.6, 7.2)], closed=True, r=r)), P(poly([(20.6, 12), (19.6, 2.8), (13.4, 7.2)], closed=True, r=r))]
    return path_to_d(U(P(ellipse(12, 13.9, 8.6, 7.2)), *ears))


def _nose(S, y=14.2):
    return mark(poly([(10.9, y), (13.1, y), (12, y + 1.4)], closed=True, r=L(S, 0, 0.4)))


def _whiskers():
    return [detail(seg(3.6, 14.8, 7, 15.6)), detail(seg(20.4, 14.8, 17, 15.6))]


@face("grinning-cat-face", "Cat face with pointed ears, whiskers and a wide open grin",
      ["grinning cat", "happy cat", "cat", "kitty", "smiling cat", "pet", "emoji"], base=_cat)
def _(S):
    return [eye(S, 8.8, 11.4, 0.9), eye(S, 15.2, 11.4, 0.9), _nose(S, 13.4), *_whiskers(),
            hole("M8.6 16H15.4C15.4 18 13.9 19.3 12 19.3C10.1 19.3 8.6 18 8.6 16Z")]


@face("crying-cat-face", "Sad cat face with whiskers, an open mouth and a tear on one cheek",
      ["crying cat", "sad cat", "cat", "kitty", "tears", "upset", "emoji"], base=_cat)
def _(S):
    return [eye(S, 8.8, 11.2, 0.9), eye(S, 15.2, 11.2, 0.9), _nose(S, 13.6), *_whiskers(),
            detail("M9.8 18.8C10.3 17.6 11 17 12 17C13 17 13.7 17.6 14.2 18.8"), mark(tear(16.4, 15.8, 1.1, 0, 2.1))]


@face("heart-eyes-cat-face", "Cat face with hearts for eyes and a smile",
      ["heart eyes cat", "cat in love", "cat", "kitty", "adore", "love", "emoji"], base=_cat)
def _(S):
    return [mark(heart(8.7, 11.2, 0.4, S)), mark(heart(15.3, 11.2, 0.4, S)), _nose(S, 13.8), *_whiskers(),
            detail("M9.4 17C10.2 18.2 11 18.6 12 18.6C13 18.6 13.8 18.2 14.6 17")]


@face("weary-cat-face", "Shocked cat face with an open mouth and both paws raised to the cheeks",
      ["weary cat", "scared cat", "cat", "kitty", "shocked", "horror", "emoji"], base=_cat,
      over=lambda S: [*hand(2.2, 17, S, n=3, fw=1.9, ph=3.6, thumb=None, deg=-12, lens=(1.8, 2.3, 1.9), seps=False, solid=True),
                      *hand(16.1, 17, S, n=3, fw=1.9, ph=3.6, thumb=None, deg=12, lens=(1.9, 2.3, 1.8), seps=False, solid=True)])
def _(S):
    return [detail(circle(8.8, 11, 1.8)), detail(circle(15.2, 11, 1.8)), _nose(S, 13.4), hole(ellipse(12, 17.6, 1.5, 1.8))]


@face("concentrating-face", "Focused face with squinting eyes and the tip of the tongue poking out",
      ["concentrating", "focused", "thinking hard", "effort", "determined", "working", "emoji"])
def _(S):
    return [detail(seg(6.8, 7.4, 10, 8.6)), detail(seg(17.2, 7.4, 14, 8.6)),
            lidded(S, 8.6, 11, 0, 1.8, 0.9), lidded(S, 15.4, 11, 0, 1.8, 0.9),
            detail(seg(8.4, 16, 13.4, 16)), hole("M13.4 16V16.8A1.7 1.7 0 0 0 16.8 16.8V16Z")]


@face("yelling-face", "Face yelling with a huge open mouth and shout lines bursting out",
      ["yelling", "shouting", "scream", "loud", "angry", "rant", "emoji"], base=circle(10, 12, 8.2),
      over=lambda S: [line(seg(20, 9.4, 22.4, 7.6)), line(seg(20.6, 12.8, 23, 12.8)), line(seg(20, 16.2, 22.4, 18))])
def _(S):
    return [detail(seg(5.4, 6.8, 8.8, 8.2)), detail(seg(14.6, 6.8, 11.2, 8.2)), eye(S, 7.4, 10.2, 0.85), eye(S, 12.6, 10.2, 0.85),
            hole(L(S, rect(6.6, 13, 6.8, 5.4, 1.4), ellipse(10, 15.7, 3.4, 2.7)))]


@face("wincing-face", "Wincing face with one eye squeezed shut and clenched teeth pulled to one side",
      ["wincing", "ouch", "pain", "cringe", "yikes", "hurt", "emoji"])
def _(S):
    return [detail(poly([(6.6, 8.2), (9.8, 9.8), (6.6, 11.4)], r=S.r)), lidded(S, 15.4, 9.6, 0, 1.9, 1.3),
            hole(poly([(8.4, 14.8), (16.8, 13.4), (16.8, 17.6), (8.4, 17.6)], closed=True, r=L(S, 0.4, 1.4))),
            inset(seg(11.2, 14.4, 11.2, 17.6)), inset(seg(14, 13.9, 14, 17.6))]


@face("hair-raising-face", "Frightened face with wide eyes and spiky hair standing on end",
      ["scared", "frightened", "hair raising", "spooked", "terrified", "fright", "emoji"], base=circle(12, 14.2, 7.6),
      over=lambda S: [line(seg(*polar(12, 14.2, 9.8, a), *polar(12, 14.2, 12.3, a))) for a in (-145, -117.5, -90, -62.5, -35)])
def _(S):
    return [detail(circle(9, 13, 1.8)), eye(S, 9, 13, 0.5), detail(circle(15, 13, 1.8)), eye(S, 15, 13, 0.5),
            hole(ellipse(12, 18, 1.3, 1.4))]


@face("bubble-gum-face", "Face with half-closed eyes blowing a big round bubble of gum",
      ["bubble gum", "chewing gum", "blowing bubble", "bored", "cool", "casual", "emoji"],
      over=lambda S: [shell(circle(13.4, 16.6, 4.6)), detail(arc(13.4, 16.6, 2.4, 195, 255))])
def _(S):
    return [lidded(S, 8.5, 9.4, 0, 1.9, 1.3), lidded(S, 15.5, 9.4, 0, 1.9, 1.3)]


@icon("paper-bag-head", CAT, "Paper bag pulled over a head with two cut-out eye holes",
      tags=["paper bag", "hiding", "embarrassed", "anonymous", "shame", "incognito", "disguise"])
def _(S):
    top = [(4.8, 6), (6.6, 3.8), (8.4, 6), (10.2, 3.8), (12, 6), (13.8, 3.8), (15.6, 6), (17.4, 3.8), (19.2, 6)]
    body = poly(top + [(19.2, 21), (4.8, 21)], closed=True, r=S.r)
    return [shell(body), detail(seg(4.8, 8.6, 19.2, 8.6)), detail(ellipse(9.4, 12.8, 1.2, 1.4)), detail(ellipse(14.6, 12.8, 1.2, 1.4)),
            detail(L(S, seg(10.2, 17, 13.8, 17), "M10.2 16.8Q12 17.8 13.8 16.8"))]



# ============================================================================ chunk 5: symbols, masks and stacked objects

from dsl import filled_region  # noqa: E402


def _sil_stroke(parts, S):
    regs = []
    for p in parts:
        if p.kind == "shell":
            regs.append(U(P(p.d), ST(p.d, 2, S.cap, S.join)))
        elif p.kind in ("line", "detail"):
            regs.append(ST(p.d, 2, S.cap, S.join))
        else:
            regs.append(P(p.d))
    return U(*regs)


def layered(name, description, tags, back, front, aliases=()):
    """Register an icon whose `front(S)` parts sit in front of `back(S)`: the back is cut with a clean gap."""
    def draw(S):
        cut = _grow(_sil_stroke([p for p in front(S) if p.kind != "detail"], S), GAP)
        out = []
        for p in back(S):
            reg = P(p.d) if p.kind in ("dot", "solid") else ST(p.d, 2, S.cap, S.join)
            left = D(reg, cut)
            if abs(left.area) > 0.01:
                out.append(solid(path_to_d(left)))
        return out + front(S)

    def filled():
        fr = front(FILL)
        f = filled_region(fr)
        b = filled_region(back(FILL))
        cut = _grow(_sil_stroke([p for p in fr if p.kind in ("shell", "line")], FILL), GAP)
        return U(D(b, cut), f)

    return icon(name, CAT, description, tags=tags, aliases=aliases, filled=filled)(draw)


def _mask_front(S):
    return [shell(ellipse(8.6, 14.2, 5.6, 5.9)), dot(6.6, 12.8, 1), dot(10.6, 12.8, 1),
            detail("M6 15.6C6.8 17 7.6 17.6 8.6 17.6C9.6 17.6 10.4 17 11.2 15.6"), line(seg(8.6, 21.1, 8.6, 23.2))]


def _sad_back(S):
    return [shell(circle(15.2, 9, 6.8)), eye(S, 17.8, 7.4, 0.85), detail("M16 13.4C16.8 12.2 17.8 11.8 19.6 12.4")]


layered("fake-smile-mask", "Sad face half hidden behind a smiling mask held on a stick",
        ["fake smile", "mask", "pretending", "hiding feelings", "two faced", "masking", "emotions"], _sad_back, _mask_front)


@face("mixed-feelings-face", "Face split down the middle, smiling on one side and frowning on the other",
      ["mixed feelings", "ambivalent", "conflicted", "bittersweet", "torn", "mood swing", "emoji"])
def _(S):
    return [detail(seg(12, 3, 12, 21)), detail(arc(8.4, 8.6, 2.1, 205, 335)), eye(S, 8.4, 10.8, 0.9), eye(S, 15.6, 10.8, 0.9),
            detail("M6.6 14.4C7.6 16.2 9.4 17.2 12 17.2"), detail(seg(14, 7.4, 17.4, 8.4)), detail("M12 15.2C14.2 15.2 15.8 16 17 17.6")]


@icon("emotion-wheel", CAT, "Circle divided into wedges with a small smiling face in the centre",
      tags=["emotion wheel", "feelings wheel", "mood chart", "emotions", "therapy", "check in", "wellbeing"])
def _(S):
    spokes = [detail(seg(*polar(12, 12, 4.7, a), *polar(12, 12, 9, a))) for a in (-60, 0, 60, 120, 180, 240)]
    return [shell(circle(12, 12, 9)), detail(circle(12, 12, 4.7)), *spokes, dot(10.6, 11.1, 0.75), dot(13.4, 11.1, 0.75),
            detail(L(S, "M10.3 13.2H13.7", "M10.4 13Q12 14.3 13.6 13"))]


def _ring_back(S):
    band = path_to_d(D(P(circle(12, 14.6, 6.6)), P(circle(12, 14.6, 3.8))))
    return [shell(band)]


def _stone(S):
    gem = ellipse(12, 5.8, 4.8, 3.8) if S.name != "line" else poly([(8.6, 2), (15.4, 2), (16.8, 3.8), (16.8, 7.8), (15.4, 9.6), (8.6, 9.6), (7.2, 7.8), (7.2, 3.8)], closed=True)
    return [shell(gem), dot(10.4, 5, 0.75), dot(13.6, 5, 0.75), detail("M10.3 6.8Q12 8 13.7 6.8")]


layered("mood-ring", "Finger ring with a large oval stone showing a small smiling face",
        ["mood ring", "ring", "feelings", "mood", "jewelry", "jewellery", "retro"], _ring_back, _stone)


@icon("anger-symbol", CAT, "Four curved vein marks arranged in a cross, the cartoon anger mark",
      tags=["anger", "angry mark", "vein", "irritated", "annoyed", "comic", "manga"])
def _(S):
    return [line(arc(3.2, 3.2, 6.6, 8, 82)), line(arc(20.8, 3.2, 6.6, 98, 172)), line(arc(20.8, 20.8, 6.6, 188, 262)),
            line(arc(3.2, 20.8, 6.6, 278, 352))]


@icon("dizzy-symbol", CAT, "Small star with a curling spiral trail swooping behind it",
      tags=["dizzy", "dazed", "seeing stars", "spinning", "sparkle", "comic", "woozy"])
def _(S):
    return [shell(star(17.2, 6.8, 4.4, 2, S)), line("M12.6 7.4C7.4 7.2 3.4 10.2 3.4 14.2C3.4 18 6.4 20.4 9.8 20.4C13 20.4 15 18.2 14.6 15.8C14.2 13.6 11.8 12.8 10 13.8")]


@icon("looking-eyes", CAT, "Pair of big eyes with the pupils glancing to one side",
      tags=["eyes", "looking", "side eye", "watching", "glance", "peek", "emoji"])
def _(S):
    return [shell(ellipse(6.8, 12, 3.8, 6.8)), shell(ellipse(17.2, 12, 3.8, 6.8)), eye(S, 5.2, 13, 1.05), eye(S, 15.6, 13, 1.05)]


def _burst(S):
    pts = []
    n = 11
    for i in range(n * 2):
        a = -90 + i * 180 / n
        R = 9.2 if i % 2 == 0 else 6.9
        pts.append(polar(12, 10.6, R, a) if i != 13 else (4.2, 21.4))
    return poly(pts, closed=True, r=L(S, 0, 0.6))


@icon("angry-speech-bubble", CAT, "Jagged spiky speech bubble with an exclamation mark inside",
      tags=["angry speech", "shout", "yell", "rant", "outburst", "comic", "argument"])
def _(S):
    return [shell(_burst(S), stroke_miterlimit="8"),
            detail(seg(12, 6.6, 12, 11.4)), dot(12, 14.2, 1.3)]


@icon("pixel-smiley", CAT, "Smiley face built from square pixels with a stepped smile",
      tags=["pixel", "8 bit", "retro", "smiley", "game", "pixel art", "emoji"])
def _(S):
    k = L(S, 0, 0.8)
    out = [(8, 3), (16, 3), (16, 5), (19, 5), (19, 8), (21, 8), (21, 16), (19, 16), (19, 19), (16, 19), (16, 21), (8, 21), (8, 19),
           (5, 19), (5, 16), (3, 16), (3, 8), (5, 8), (5, 5), (8, 5)]
    return [shell(poly(out, closed=True, r=k)), mark(rect(8, 8, 2.6, 2.6, L(S, 0, 0.5))), mark(rect(13.4, 8, 2.6, 2.6, L(S, 0, 0.5))),
            detail(poly([(7.5, 12.5), (7.5, 14.5), (9.5, 14.5), (9.5, 16.2), (14.5, 16.2), (14.5, 14.5), (16.5, 14.5), (16.5, 12.5)], r=k))]


def _profile(S):
    return ("M7.4 21V17.8C5 16.3 3.6 13.8 3.6 10.9C3.6 6.4 7.3 3 11.8 3C16 3 19 5.9 19.3 9.7L21 13.2H19.3V15.8"
            "C19.3 17 18.4 17.8 17.2 17.8H15.2V21")


@icon("emotional-intelligence", CAT, "Head in profile with a heart inside it and small rays around the heart",
      tags=["emotional intelligence", "empathy", "eq", "self awareness", "compassion", "wellbeing", "mindfulness"])
def _(S):
    rays = [detail(seg(*polar(11.2, 10.6, 4.6, a), *polar(11.2, 10.6, 5.8, a))) for a in (-145, -90, -35)]
    return [shell(_profile(S) if S.name == "line" else _profile(S).replace("L21 13.2H19.3", "L20.6 12.4Q21 13.2 20.2 13.2H19.3")),
            mark(heart(11.2, 11.2, 0.36, S)), *rays]


# ============================================================================ chunk 6: theatre masks and stage faces

def _hannya(S):
    return "M5 8.4C5 5.6 8 4.6 12 4.6C16 4.6 19 5.6 19 8.4V13C19 17.8 16 21.4 12 21.4C8 21.4 5 17.8 5 13Z"


def _hannya_horns(S):
    left = "M6 6.2C4.3 5.3 3.4 4 3.3 2.4C5 3.3 6.9 3.6 8.8 3.8Z"
    right = "M18 6.2C19.7 5.3 20.6 4 20.7 2.4C19 3.3 17.1 3.6 15.2 3.8Z"
    if S.name != "line":
        left = "M6 6.2C4.2 5.2 3.3 3.8 3.1 2.4Q3.1 1.6 3.8 2C5.4 2.9 7 3.3 8.6 3.6Z"
        right = "M18 6.2C19.8 5.2 20.7 3.8 20.9 2.4Q20.9 1.6 20.2 2C18.6 2.9 17 3.3 15.4 3.6Z"
    return [shell(left), shell(right)]


@face("hannya-mask", "Horned demon mask with staring eyes and a wide mouth of teeth and fangs",
      ["hannya", "demon mask", "noh mask", "oni", "japanese mask", "jealousy", "theatre"], base=_hannya, over=_hannya_horns)
def _(S):
    return [detail(seg(6.8, 8, 10.4, 9.8)), detail(seg(17.2, 8, 13.6, 9.8)), eye(S, 8.6, 12, 0.85), eye(S, 15.4, 12, 0.85),
            hole(L(S, "M6.8 14.8H17.2C17.2 18.2 15 19.8 12 19.8C9 19.8 6.8 18.2 6.8 14.8Z",
                   "M8 14.8H16Q17.2 14.8 17.1 16C16.8 18.4 14.8 19.8 12 19.8C9.2 19.8 7.2 18.4 6.9 16Q6.8 14.8 8 14.8Z")),
            inset(seg(7.6, 16.6, 16.4, 16.6)), inset(seg(9.4, 14.8, 9.4, 18.4)), inset(seg(14.6, 14.8, 14.6, 18.4))]


def _okame(S):
    return union(circle(12, 11.2, 8.2), ellipse(12, 14.8, 8.8, 6.6))


@face("okame-mask", "Round smiling mask with full cheeks, crescent eyes, high dot brows and parted hair",
      ["okame", "otafuku", "japanese mask", "good fortune", "smiling mask", "festival", "theatre"], base=_okame)
def _(S):
    return [detail("M4.4 8.6C6.2 5.4 9.8 5 12 7C14.2 5 17.8 5.4 19.6 8.6"), dot(8.6, 10, 0.95), dot(15.4, 10, 0.95),
            happy_eye(8.8, 13.6, 1.6), happy_eye(15.2, 13.6, 1.6), mark(L(S, rect(11, 16.8, 2, 1.8, 0.3), ellipse(12, 17.7, 1.15, 0.95)))]


def _hyottoko(S):
    return union(circle(11.2, 12.8, 8.2), circle(17.8, 17, 2.9))


@face("hyottoko-mask", "Comic mask with lips pursed to one side, uneven eyes and a scarf knotted on top",
      ["hyottoko", "japanese mask", "comic mask", "festival", "clown", "blowing", "theatre"], base=_hyottoko,
      over=lambda S: [shell(rect(9, 1.4, 4.4, 3.2, L(S, 0.8, 1.6)))])
def _(S):
    return [detail(seg(5, 7.4, 17.4, 7.4)), detail(circle(8, 11.4, 2)), dot(8, 11.4, 0.9), eye(S, 14.2, 11.6, 0.75), dot(17.9, 17.1, 0.95)]


@face("kabuki-face", "Stage face with bold makeup stripes sweeping up from the eyes and a downturned mouth",
      ["kabuki", "kumadori", "stage makeup", "japanese theatre", "actor", "drama", "theatre"], base=ellipse(12, 12.4, 8, 9.2))
def _(S):
    return [detail("M9.8 9.6C8.4 8.8 7.3 7.2 6.8 5.2"), detail("M14.2 9.6C15.6 8.8 16.7 7.2 17.2 5.2"),
            detail("M9.4 12.6C7.6 12.4 5.8 11 4.8 8.8"), detail("M14.6 12.6C16.4 12.4 18.2 11 19.2 8.8"),
            eye(S, 10.2, 13.6, 0.7), eye(S, 13.8, 13.6, 0.7), detail("M9 18.6C10 17.2 14 17.2 15 18.6")]


def _opera(S):
    return "M4 4.8C8.4 2.6 15.6 2.6 20 4.8C20.6 12.6 17.2 19.2 12 21.4C6.8 19.2 3.4 12.6 4 4.8Z"


@face("peking-opera-mask", "Painted opera mask with upswept wing brows, bold eye patches and a forehead emblem",
      ["peking opera", "beijing opera", "chinese opera", "painted face", "jingju", "stage mask", "theatre"], base=_opera)
def _(S):
    k = L(S, 0, 0.5)
    return [mark(poly([(12, 5), (13.5, 6.9), (12, 8.8), (10.5, 6.9)], closed=True, r=k)),
            detail("M10.6 10.6C9.2 9.4 7.4 8.8 5.4 9"), detail("M13.4 10.6C14.8 9.4 16.6 8.8 18.6 9"),
            mark(rot(ellipse(8.4, 13, 2.4, 1.4), 18, 8.4, 13)), mark(rot(ellipse(15.6, 13, 2.4, 1.4), -18, 15.6, 13)),
            detail("M10.2 17.4Q12 18.6 13.8 17.4")]


def _kk_back(S):
    return [shell("M4.2 10A7.8 7.8 0 0 1 19.8 10Z" if S.name == "line" else "M6.2 10Q4.2 10 4.5 8A7.8 7.8 0 0 1 19.5 8Q19.8 10 17.8 10Z"),
            detail(arc(12, 10, 4.6, 200, 340))]


def _kk_front(S):
    ridge = []
    n = 8
    for i in range(n + 1):
        a = math.radians(14 + i * (152 / n))
        rx, ry = (7.4, 7.2) if i % 2 == 0 else (8.8, 8.4)
        ridge.append((12 + rx * math.cos(a), 13.6 + ry * math.sin(a)))
    return [shell(ellipse(12, 13.6, 5.4, 5.8)), line(poly(ridge, r=L(S, 0, 0.4))),
            mark(ellipse(9.6, 12.6, 1.5, 0.8)), mark(ellipse(14.4, 12.6, 1.5, 0.8)), detail("M10.4 16.2Q12 17.2 13.6 16.2")]


layered("kathakali-face", "Painted dance face with a tall round crown and a ridged frame along the jaw",
        ["kathakali", "kerala", "indian dance", "classical dance", "painted face", "dance drama", "theatre"], _kk_back, _kk_front)
