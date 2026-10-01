"""TypeIcon Core: emoji and emotions.

Every face shares one face circle (r 9) and varies only eyes, brows and mouth, so the set reads as a family.
Line and Rounded differ on purpose: Line eyes are crisp upright bars and Line strokes end square; Rounded eyes
are soft ovals and strokes end round. Filled is a solid disc with the features cut out (open mouths become
holes). Props that overlap the face edge (a hat, a heart, Zs) cut the face ring with a clean gap.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, seg, shell, solid  # noqa: F401
from geometry import D, P, ROUNDED, ST, Style, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "emotions"
FILL = Style("filled", "round", "round", R=4.0, r=1.5)  # pseudo-style: feature geometry for the Filled design
FACE = circle(12, 12, 9)
GAP = 1.75


class Hole(Part):
    """A closed feature (open mouth) drawn as an outline in Line/Rounded and cut out whole in Filled."""


class Inset(Part):
    """A stroke inside a Hole (teeth, a mask pleat): a detail in Line/Rounded, kept solid inside the Filled hole."""


def hole(d):
    return Hole("detail", d, {})


def inset(d):
    return Inset("detail", d, {})


def mark(d):
    """Solid feature (eye, tear): solid in Line/Rounded, cut out of the Filled face."""
    return Part("dot", d)


def L(S, a, b):
    return a if S.name == "line" else b


def eye(S, x, y=10):
    return mark(rect(x - 1.1, y - 1.6, 2.2, 3.2) if S.name == "line" else ellipse(x, y, 1.2, 1.6))


def eyes(S, y=10, dx=3):
    return [eye(S, 12 - dx, y), eye(S, 12 + dx, y)]


def _region(p):
    if p.kind == "shell" or isinstance(p, Hole):
        return U(P(p.d), ST(p.d, 2))
    if p.kind in ("line", "detail"):
        return ST(p.d, 2, "round", "round")
    return P(p.d)


def _grow(path, g):
    return U(path, ST(path_to_d(path), 2 * g, "round", "round"))


def face(name, description, tags, aliases=(), over=None):
    """Register a face. `fn(S)` returns the features; `over(S)` returns props overlapping the face edge."""
    def deco(fn):
        def draw(S):
            props = over(S) if over else []
            if props:
                cutter = _grow(U(*[_region(p) for p in props]), GAP)
                ring = solid(path_to_d(D(ST(FACE, 2, S.cap, S.join), cutter)))
            else:
                ring = shell(FACE)
            return [ring, *fn(S), *props]

        def filled():
            body = P(circle(12, 12, 10))
            extras = []
            props = over(FILL) if over else []
            if props:
                body = D(body, _grow(U(*[_region(p) for p in props]), GAP))
                for p in props:
                    extras.append(U(P(p.d), ST(p.d, 2)) if p.kind == "shell" else
                                  ST(p.d, 2.5, "round", "round") if p.kind == "line" else P(p.d))
            feats = fn(FILL)
            for p in feats:
                if isinstance(p, Inset):
                    continue
                if isinstance(p, Hole):
                    body = D(body, U(P(p.d), ST(p.d, 2)))
                elif p.kind in ("detail", "line"):
                    body = D(body, ST(p.d, 2, "round", "round"))
                elif p.kind in ("dot", "solid"):
                    body = D(body, P(p.d))
                elif p.kind == "shell":
                    body = D(body, U(P(p.d), ST(p.d, 2)))
            extras += [ST(p.d, 2, "butt", "miter") for p in feats if isinstance(p, Inset)]
            return U(body, *extras)

        return icon(name, CAT, description, tags=tags, aliases=aliases, filled=filled)(draw)
    return deco


# --------------------------------------------------------------------------- shared mouths and marks

SMILE = "M8 14.5C9 16.3 10.4 17 12 17C13.6 17 15 16.3 16 14.5"
FROWN = "M8.5 17.5C9.3 16 10.5 15.3 12 15.3C13.5 15.3 14.7 16 15.5 17.5"
GRIN = "M7.5 13.5H16.5C16.5 16.4 14.5 18.3 12 18.3C9.5 18.3 7.5 16.4 7.5 13.5Z"


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


# ============================================================================ happy

@face("smile", "Smiling face", ["happy", "smiley", "emoji", "glad", "positive", "face"], aliases=["smiley", "happy"])
def _(S):
    return [*eyes(S), detail(SMILE)]


@face("laugh", "Laughing face with squinting eyes and an open grin", ["joy", "lol", "haha", "funny", "happy", "emoji"], aliases=["lol"])
def _(S):
    return [detail(arc(9, 10.5, 1.75, 180, 360)), detail(arc(15, 10.5, 1.75, 180, 360)), hole(GRIN)]


@face("wink", "Winking face", ["wink", "playful", "flirt", "joke", "emoji", "face"])
def _(S):
    return [eye(S, 9), detail(arc(15, 10.5, 1.75, 180, 360)), detail("M8 15C9.5 16.8 11 17.2 12.5 17C14.5 16.7 15.7 15.5 16.5 13.8")]


@face("relieved", "Relieved face with calm closed eyes", ["calm", "relief", "phew", "content", "peaceful", "emoji"], aliases=["content"])
def _(S):
    return [detail(arc(9, 9.5, 1.75, 0, 180)), detail(arc(15, 9.5, 1.75, 0, 180)), detail(SMILE)]


@face("heart-eyes", "Smiling face with hearts for eyes", ["love", "adore", "crush", "in love", "heart", "emoji"], aliases=["in-love"])
def _(S):
    return [mark(heart(8.75, 9.8, 0.46, S)), mark(heart(15.25, 9.8, 0.46, S)), detail(SMILE)]


@face("star-struck", "Grinning face with stars for eyes", ["starstruck", "wow", "amazed", "excited", "fan", "emoji"], aliases=["starstruck"])
def _(S):
    return [mark(star(8.75, 9.6, 2.8, 1.2, S)), mark(star(15.25, 9.6, 2.8, 1.2, S)), hole(GRIN)]


@face("cool", "Face wearing sunglasses", ["sunglasses", "chill", "confident", "awesome", "swag", "emoji"], aliases=["sunglasses-face"])
def _(S):
    k = L(S, 0, 1)
    lens_l = poly([(5.5, 8.75), (11, 8.75), (11, 11), (9.5, 12.75), (7, 12.75), (5.5, 11)], closed=True, r=k)
    lens_r = poly([(13, 8.75), (18.5, 8.75), (18.5, 11), (17, 12.75), (14.5, 12.75), (13, 11)], closed=True, r=k)
    return [mark(lens_l), mark(lens_r), detail(seg(10, 9.75, 14, 9.75)), detail(seg(3.2, 9.75, 6, 9.75)), detail(seg(18, 9.75, 20.8, 9.75)),
            detail("M9.5 16.5C11.5 17.5 14 17 15.5 15.3")]


@face("party-face", "Face in a party hat", ["party", "celebrate", "birthday", "hooray", "festive", "emoji"], aliases=["partying-face"],
      over=lambda S: [shell(poly([(4.8, 7.7), (11.2, 4.2), (4.2, 1.8)], closed=True, r=L(S, 0, 1)), stroke_miterlimit="8")])
def _(S):
    return [eye(S, 10, 11), eye(S, 16, 11), detail("M9 15.5C10 17 11.3 17.6 12.6 17.6C14.1 17.6 15.4 16.8 16.3 15.3"),
            dot(19.5, 4, 1.1), dot(21, 8.5, 1.1)]


# ============================================================================ sad and upset

@face("sad", "Sad face with a frown", ["unhappy", "sorrow", "down", "disappointed", "frown", "emoji"], aliases=["unhappy", "frown"])
def _(S):
    return [*eyes(S), detail(FROWN)]


@face("cry", "Crying face with a tear", ["crying", "tears", "sad", "upset", "weep", "emoji"], aliases=["crying"])
def _(S):
    return [*eyes(S, 9.5), detail(FROWN), mark(drop(15, 12.6, 1.5, 15.6))]


@face("worried", "Worried face with raised brows", ["anxious", "nervous", "concerned", "uneasy", "fear", "emoji"], aliases=["anxious"])
def _(S):
    return [detail(seg(7.3, 8.3, 10.3, 7)), detail(seg(16.7, 8.3, 13.7, 7)), *eyes(S, 11), detail("M9 17C10 15.9 11 15.5 12 15.5C13 15.5 14 15.9 15 17")]


@face("angry", "Angry face with lowered brows", ["mad", "rage", "annoyed", "furious", "grumpy", "emoji"], aliases=["mad"])
def _(S):
    return [detail(seg(7.3, 7, 10.5, 8.5)), detail(seg(16.7, 7, 13.5, 8.5)), *eyes(S, 11.5), detail("M8.5 17.3C9.5 16.2 10.7 15.8 12 15.8C13.3 15.8 14.5 16.2 15.5 17.3")]


@face("grimace", "Grimacing face showing clenched teeth", ["awkward", "cringe", "eek", "nervous", "oops", "emoji"], aliases=["grimacing"])
def _(S):
    return [*eyes(S), hole(rect(7, 13.5, 10, 4.5, L(S, 1, 2.25))), inset(seg(10.33, 13.5, 10.33, 18)), inset(seg(13.67, 13.5, 13.67, 18))]


# ============================================================================ neutral and puzzled

@face("neutral", "Neutral face with a straight mouth", ["meh", "indifferent", "expressionless", "blank", "straight face", "emoji"], aliases=["meh"])
def _(S):
    return [*eyes(S), detail(seg(8.5, 15.5, 15.5, 15.5))]


@face("surprised", "Surprised face with an open mouth", ["shocked", "wow", "astonished", "amazed", "gasp", "emoji"], aliases=["shocked"])
def _(S):
    return [*eyes(S, 9.5), hole(ellipse(12, 15.8, 2, 2.3))]


@face("confused", "Confused face with a wavy mouth", ["puzzled", "unsure", "huh", "perplexed", "bewildered", "emoji"], aliases=["puzzled"])
def _(S):
    return [*eyes(S), detail("M8 16.5C9 15.2 10 15.2 11 16C12 16.8 13 16.8 14 16C14.8 15.4 15.5 15.3 16 15.5")]


@face("thinking", "Thinking face with a raised brow and a hand on the chin", ["think", "hmm", "ponder", "wonder", "consider", "emoji"],
      aliases=["hmm"],
      over=lambda S: [shell(rect(13.5, 17.5, 7, 4, L(S, 1, 2))), line(seg(14.5, 17.5, 14.5, 14))])
def _(S):
    return [detail("M13.2 7.2C14.2 6.3 15.8 6.2 16.8 7"), eye(S, 9, 10.5), eye(S, 15, 10.5), detail(seg(8, 15.5, 11.5, 14.6))]


@face("sleepy", "Sleeping face with closed eyes and a Z", ["sleep", "tired", "zzz", "bored", "night", "emoji"], aliases=["sleeping"],
      over=lambda S: [line(poly([(16.5, 2.5), (21, 2.5), (16.5, 7.5), (21, 7.5)], r=L(S, 0, 0.5)), stroke_miterlimit="8")])
def _(S):
    return [detail(seg(6.75, 11, 10.25, 11)), detail(seg(13.75, 11, 17.25, 11)), hole(ellipse(12, 16, 1.4, 1.6))]


@face("sick", "Face wearing a medical mask", ["ill", "mask", "flu", "unwell", "virus", "emoji"], aliases=["ill", "mask-face"])
def _(S):
    mask = rect(6.5, 12.5, 11, 6, L(S, 1, 2.5))
    return [*eyes(S, 9), hole(mask), detail(seg(3.5, 11.5, 6.5, 13.5)), detail(seg(20.5, 11.5, 17.5, 13.5)), inset(seg(9, 15.5, 15, 15.5))]


# ============================================================================ playful and silly

@face("kiss", "Face blowing a kiss with a heart", ["kissing", "love", "smooch", "affection", "flirt", "emoji"], aliases=["kissing"],
      over=lambda S: [mark(heart(19, 16, 0.62, S))])
def _(S):
    return [eye(S, 9), detail(arc(15, 10, 1.75, 180, 360)),
            detail("M11 13.8C12.8 13.8 13.6 14.4 13.6 15.1C13.6 15.7 12.8 16.1 12 16.1C12.8 16.1 13.6 16.5 13.6 17.1C13.6 17.8 12.8 18.4 11 18.4")]


@face("tongue-out", "Face sticking out its tongue", ["silly", "tongue", "playful", "cheeky", "joke", "emoji"], aliases=["cheeky"])
def _(S):
    return [*eyes(S, 9.5), detail(seg(7.5, 14.5, 16.5, 14.5)), hole("M10 14.5V17A2 2 0 0 0 14 17V14.5Z")]


@face("zipper-mouth", "Face with a zipped mouth", ["secret", "quiet", "silence", "shh", "mute", "emoji"], aliases=["zip-it"])
def _(S):
    return [*eyes(S, 9.5), detail(seg(7, 15.5, 17, 15.5)), detail(seg(9.5, 13.8, 9.5, 17.2)), detail(seg(12, 13.8, 12, 17.2)),
            detail(seg(14.5, 13.8, 14.5, 17.2))]


@face("nerd", "Nerdy face with round glasses and buck teeth", ["geek", "smart", "glasses", "clever", "study", "emoji"], aliases=["geek"])
def _(S):
    return [detail(circle(8.5, 10, 2.4)), detail(circle(15.5, 10, 2.4)), detail(seg(10.9, 10, 13.1, 10)),
            detail(seg(3.1, 10.5, 6.1, 10)), detail(seg(20.9, 10.5, 17.9, 10)),
            detail("M8 14.5C9 16 10.4 16.6 12 16.6C13.6 16.6 15 16 16 14.5"), mark(rect(10.8, 16.4, 2.4, 2.2, L(S, 0, 0.6)))]


# ============================================================================ characters (own outlines, same family proportions)

def _skull(S):
    if S.name == "line":
        return "M4.2 16.5A9 9 0 1 1 19.8 16.5L17 17.8V21H7V17.8Z"
    return "M4.2 16.5A9 9 0 1 1 19.8 16.5L17.9 17.4Q17 17.8 17 18.8V19.5Q17 21 15.5 21H8.5Q7 21 7 19.5V18.8Q7 17.8 6.1 17.4Z"


@icon("skull-emoji", CAT, "Cartoon skull with big eye sockets", tags=["dead", "death", "spooky", "halloween", "lol", "emoji"],
      filled=lambda: D(U(P(_skull(FILL)), ST(_skull(FILL), 2)),
                       P(ellipse(8.7, 11.5, 2.3, 2.6)), P(ellipse(15.3, 11.5, 2.3, 2.6)), P(poly([(12, 14.6), (13.2, 16.6), (10.8, 16.6)], closed=True)),
                       ST(seg(10.5, 18.5, 10.5, 21.5), 2, "round"), ST(seg(13.5, 18.5, 13.5, 21.5), 2, "round")))
def _(S):
    return [shell(_skull(S)), mark(ellipse(8.7, 11.5, 2.3, 2.6)), mark(ellipse(15.3, 11.5, 2.3, 2.6)),
            mark(poly([(12, 14.6), (13.2, 16.6), (10.8, 16.6)], closed=True, r=L(S, 0, 0.4))),
            detail(seg(10.5, 18.5, 10.5, 21)), detail(seg(13.5, 18.5, 13.5, 21))]


def _pile(S):
    k = L(S, 0.35, 0)
    tiers = [rect(3, 14.5, 18, 7, 3.5 - k), rect(5, 9.5, 14, 6.5, 3.25 - k), rect(7.5, 5, 9, 5.5, 2.75 - k),
             "M9.5 6C9.5 4.2 11.2 3.8 12.3 2.5C14 3.5 14.5 5 14 6.5Z"]
    return path_to_d(U(*[P(t) for t in tiers]))


_POOP_FACE = lambda S: [eye(S, 9.5, 12.25), eye(S, 14.5, 12.25), "M9 17C10 18.3 11 18.8 12 18.8C13 18.8 14 18.3 15 17"]  # noqa: E731


@icon("poop-emoji", CAT, "Smiling swirl of poop", tags=["poop", "poo", "funny", "silly", "toilet", "emoji"], aliases=["poop", "poo"],
      filled=lambda: D(U(P(_pile(FILL)), ST(_pile(FILL), 2)), P(ellipse(9.5, 12.25, 1.2, 1.6)), P(ellipse(14.5, 12.25, 1.2, 1.6)),
                       ST(_POOP_FACE(FILL)[2], 2, "round", "round")))
def _(S):
    f = _POOP_FACE(S)
    return [shell(_pile(S)), f[0], f[1], detail(f[2])]
