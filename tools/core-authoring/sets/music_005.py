"""TypeIcon Core: music batch 005 (dance, accessories, notation and everyday music scenes).

Dancers are drawn as simple figures (solid head, strokes for limbs) so they stay readable at 16 px.
Small solid marks use Part("dot") so the Filled style knocks them out of a solid body.
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, P, ST, U, Part, arc, circle, detail, dot, ellipse, filled_region, icon, line, path_to_d, poly, pt_on, rect,
    regular, seg, shell, solid,
)
from geometry import LINE, fmt

CAT = "music"


def rnd(S, line_val, rounded_val):
    return line_val if S.name == "line" else rounded_val


def head(x, y, r=2.2):
    return dot(x, y, r)


def mark(d):
    """Small solid mark (knocked out of a Filled body)."""
    return Part("dot", d)


def rotp(pts, deg, cx, cy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def note(x, y, h=6.5, r=1.6, flag=True):
    """Small eighth note: head at (x, y), stem up on its right."""
    sx = x + r - 0.1
    parts = [dot(x, y, r), line(seg(sx, y, sx, y - h))]
    if flag:
        parts.append(line(f"M{fmt(sx)} {fmt(y - h)}q2.5 0.5 2.5 3"))
    return parts


# --------------------------------------------------------------------------- notation and media

@icon("sixteenth-rest", CAT, "Sixteenth rest: a slanted stroke with two hooked flags ending in dots on its left",
      tags=["rest", "silence", "pause", "notation", "sheet music", "sixteenth", "semiquaver rest"],
      aliases=["semiquaver-rest"])
def _(S):
    return [
        line(seg(14.5, 3, 10.5, 21)),
        line("M9.5 8.6Q12 8.6 13.6 6.8"),
        dot(8.6, 8.6, 1.7),
        line("M8.3 14.6Q10.8 14.6 12.3 12.8"),
        dot(7.4, 14.6, 1.7),
    ]


@icon("music-video", CAT, "Screen with a play triangle and a small music note in the corner",
      tags=["video", "clip", "mv", "screen", "play", "film", "media", "concert video"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 19, 15, S.R)),
        mark(poly([(6.5, 8.8), (6.5, 15.2), (11.5, 12)], closed=True, r=S.r * 0.4)),
        dot(14.6, 15.2, 1.5),
        detail(seg(16.1, 15.2, 16.1, 9.2)),
        detail("M16.1 9.2q2 0.4 2.2 2.4"),
    ]


@icon("audiobook", CAT, "Open book with a pair of headphones resting over its top edge",
      tags=["audio book", "listen", "narration", "reading", "spoken word", "headphones", "podcast"])
def _(S):
    book = poly([(3, 13.5), (12, 14.5), (21, 13.5), (21, 21), (12, 20), (3, 21)], closed=True, r=S.r)
    return [
        line(arc(12, 8.5, 6.5, 180, 360)),
        shell(rect(3.5, 7.5, 3, 4.5, rnd(S, 1, 1.5))),
        shell(rect(17.5, 7.5, 3, 4.5, rnd(S, 1, 1.5))),
        shell(book),
        detail(seg(12, 14.5, 12, 20)),
    ]


@icon("explicit-content", CAT, "Rounded square containing a bold capital letter E",
      tags=["explicit", "parental advisory", "mature", "adult lyrics", "rating", "warning", "label", "e"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(poly([(15.3, 8), (9.3, 8), (9.3, 16), (15.3, 16)], r=S.r * 0.4)),
        detail(seg(9.3, 12, 14, 12)),
    ]


@icon("dance-mat", CAT, "Square dance floor mat with four arrow panels around an empty centre",
      tags=["dance pad", "arcade", "rhythm game", "stepping", "floor mat", "game", "fitness"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, S.R)),
        mark(poly([(12, 5.2), (14.6, 8.6), (9.4, 8.6)], closed=True, r=S.r * 0.3)),
        mark(poly([(12, 18.8), (14.6, 15.4), (9.4, 15.4)], closed=True, r=S.r * 0.3)),
        mark(poly([(5.2, 12), (8.6, 9.4), (8.6, 14.6)], closed=True, r=S.r * 0.3)),
        mark(poly([(18.8, 12), (15.4, 9.4), (15.4, 14.6)], closed=True, r=S.r * 0.3)),
    ]


# --------------------------------------------------------------------------- accessories

@icon("string-winder", CAT, "Crank-shaped string winder with a slotted cup that fits over a tuning peg",
      tags=["peg winder", "guitar string", "restring", "tuning peg", "crank", "luthier", "accessory"])
def _(S):
    return [
        shell(rect(4.5, 15, 8, 6.5, rnd(S, 1, 2))),
        detail(seg(8.5, 18.25, 8.5, 21)),
        line(seg(8.5, 15, 8.5, 4)),
        line(seg(8.5, 4, 18, 4)),
        shell(rect(16.5, 4, 3.5, 9.5, rnd(S, 1, 1.75))),
    ]


@icon("drum-key", CAT, "T-shaped drum key with a flat wing handle and a square socket",
      tags=["tuning key", "drum tuning", "lug", "tension rod", "wrench", "accessory", "percussion"])
def _(S):
    return [
        shell(rect(3, 3.5, 18, 4.5, rnd(S, 1, 2.25))),
        shell(rect(10.5, 8, 3, 8.5, 0)),
        shell(rect(9, 16.5, 6, 5, rnd(S, 0.5, 1.5))),
        mark(rect(11, 18.5, 2, 1.5, 0)),
    ]


@icon("drum-throne", CAT, "Round padded drum seat on a short column with splayed legs",
      tags=["drum stool", "seat", "stool", "drummer", "chair", "drum kit", "practice room"])
def _(S):
    return [
        shell(rect(4, 3.5, 16, 5.5, rnd(S, 2, 2.75))),
        line(seg(12, 9, 12, 14.5)),
        line(poly([(5.5, 21), (12, 14.5), (18.5, 21)], r=S.r)),
        line(seg(12, 14.5, 12, 21)),
    ]


@icon("keyboard-stand", CAT, "X-shaped folding stand holding a flat keyboard on top",
      tags=["piano stand", "synth stand", "x stand", "keys", "stage", "gear", "support"])
def _(S):
    return [
        shell(rect(2, 3.5, 20, 7, rnd(S, 1, 2.5))),
        detail(seg(7.5, 7.2, 7.5, 10.5)),
        detail(seg(12, 7.2, 12, 10.5)),
        detail(seg(16.5, 7.2, 16.5, 10.5)),
        line(seg(6.5, 21, 17.5, 12.5)),
        line(seg(17.5, 21, 6.5, 12.5)),
    ]


@icon("drum-practice-pad", CAT, "Round rubber practice pad on a small stand with two drumsticks crossed on top",
      tags=["practice pad", "drum pad", "rudiments", "sticks", "silent practice", "percussion", "training"])
def _(S):
    return [
        shell(rect(3, 13, 18, 4.5, rnd(S, 1.5, 2.25))),
        line(seg(12, 17.5, 12, 21.5)),
        line(seg(8, 21.5, 16, 21.5)),
        line(seg(4, 5, 17, 12)),
        line(seg(20, 5, 7, 12)),
    ]


@icon("light-stick", CAT, "Concert light stick with a handle and a glowing round lamp head with rays",
      tags=["glow stick", "lightstick", "concert", "fan", "cheer", "idol", "pen light", "lamp"])
def _(S):
    return [
        shell(rect(8.5, 6, 7, 7, rnd(S, 1.5, 3.5))),
        shell(rect(10, 13, 4, 8.5, rnd(S, 0.8, 1.5))),
        line(seg(12, 1.5, 12, 3)),
        line(seg(4.5, 9.5, 6, 9.5)),
        line(seg(18, 9.5, 19.5, 9.5)),
        line(seg(5.5, 3.5, 6.8, 4.8)),
        line(seg(18.5, 3.5, 17.2, 4.8)),
    ]


@icon("harmonica-holder", CAT, "Harmonica held on a U-shaped wire neck rack",
      tags=["harp rack", "neck brace", "hands free", "blues harp", "mouth organ", "folk", "accessory"])
def _(S):
    return [
        shell(rect(5, 3, 14, 6, rnd(S, 1, 2))),
        mark(circle(8.6, 6, 0.9)),
        mark(circle(12, 6, 0.9)),
        mark(circle(15.4, 6, 0.9)),
        line(f"M5 6H3V12a9 8.5 0 0 0 18 0V6H19"),
    ]


@icon("bell-tree", CAT, "Vertical rod carrying a stack of nested bowl-shaped bells that shrink toward the top",
      tags=["mark tree", "chimes", "percussion", "shimmer", "orchestra", "sweep", "bells"])
def _(S):
    return [
        dot(12, 3.2, 1.7),
        line(seg(12, 3.2, 12, 14)),
        line("M3.5 21.5C3.5 17.5 7 15.5 12 15.5S20.5 17.5 20.5 21.5"),
        line("M6.5 15.5C6.5 12.5 9 11 12 11S17.5 12.5 17.5 15.5"),
        line("M8.8 11C8.8 8.8 10.2 7.5 12 7.5S15.2 8.8 15.2 11"),
    ]


# --------------------------------------------------------------------------- dancers

@icon("disco-dance", CAT, "Dancer with one arm pointing up and out to the sky and the other hand on the hip",
      tags=["disco", "dancing", "saturday night", "party", "club", "70s", "pose", "nightclub"])
def _(S):
    return [
        head(11, 4.6),
        line(seg(11, 7.8, 11, 14.5)),
        line(seg(11, 9.2, 18.5, 3.2)),
        line(poly([(11, 9.2), (5.5, 11.8), (10.5, 14.5)], r=S.r)),
        line(poly([(8, 21), (11, 14.5), (15.5, 21)], r=S.r)),
    ]


def _fan(S, px, py, a1, a2, r=7, n=3):
    """Fan sector whose rim is n scallops."""
    pts = [pt_on(px, py, r, a1 + (a2 - a1) * i / n) for i in range(n + 1)]
    chord = math.hypot(pts[1][0] - pts[0][0], pts[1][1] - pts[0][1])
    out = f"M{fmt(px)} {fmt(py)}L{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for q in pts[1:]:
        out += f"A{fmt(chord * 0.62)} {fmt(chord * 0.62)} 0 0 1 {fmt(q[0])} {fmt(q[1])}"
    return out + "Z"


@icon("fan-dance", CAT, "Dancer holding two large open folding fans spread out to each side",
      tags=["folding fan", "fans", "traditional dance", "performance", "asian dance", "stage", "dancer"])
def _(S):
    def rib(px, py, deg, r=7.6):
        q = pt_on(px, py, r, deg)
        return seg(px, py, q[0], q[1])
    return [
        head(12, 4.6, 2.1),
        line(seg(12, 7.8, 12, 15)),
        line(seg(12, 9.5, 9, 10.5)),
        line(seg(12, 9.5, 15, 10.5)),
        line(poly([(9.5, 21), (12, 15), (14.5, 21)], r=S.r)),
        shell(_fan(S, 9, 11, 150, 230, 7.6)),
        detail(rib(9, 11, 190)),
        shell(_fan(S, 15, 11, 310, 390, 7.6)),
        detail(rib(15, 11, 350)),
    ]


@icon("irish-dance", CAT, "Dancer standing stiff with arms held straight down and one leg kicked high in front",
      tags=["jig", "step dance", "reel", "folk dance", "celtic", "ireland", "high kick", "dancer"])
def _(S):
    return [
        head(9.5, 4.6),
        line(seg(9.5, 7.8, 9.5, 14.5)),
        line(seg(9.5, 9.5, 6, 15.5)),
        line(poly([(9.5, 14.5), (19, 10.5)], r=S.r)),
        line(poly([(9.5, 14.5), (9.5, 18), (8.5, 21)], r=S.r)),
    ]


@icon("cancan-dance", CAT, "Dancer holding up a ruffled skirt with one leg kicked high",
      tags=["can can", "cabaret", "french dance", "showgirl", "frills", "high kick", "moulin", "dancer"])
def _(S):
    skirt = "M9 9.5L13 9.5L18.5 16C17 17.6 15.3 17.6 14 16.4C12.6 17.8 10.7 17.8 9.5 16.4C8 17.8 6.2 17.6 5 16Z"
    return [
        head(11, 4.4, 2.1),
        shell(skirt),
        line(seg(11, 7.6, 11, 9.5)),
        line(seg(14.5, 12.5, 21, 5.5)),
        line(seg(9, 17, 8.5, 21.5)),
        line(poly([(10.5, 8.3), (6, 10.5), (6.5, 13.2)], r=S.r)),
    ]


@icon("charleston-dance", CAT, "Dancer in a straight flapper dress with a fringed hem, one knee flicked out and arms swinging",
      tags=["charleston", "flapper", "1920s", "roaring twenties", "jazz age", "fringe dress", "dancer", "swing"])
def _(S):
    dress = "M9.5 8.6H14.5L15.6 15L14.3 16.2L13 15.2L11.7 16.2L10.4 15.2L9.1 16.2L8.4 15Z"
    return [
        head(12, 4.5),
        shell(dress),
        line(seg(10.5, 16, 10, 21.5)),
        line(poly([(13.2, 16), (18.5, 17), (17.8, 21.5)], r=S.r)),
        line(poly([(9.5, 9.6), (5, 11.5), (4.5, 15)], r=S.r)),
        line(poly([(14.5, 9.6), (18.5, 10.5), (20, 7)], r=S.r)),
    ]


@icon("belly-dancer", CAT, "Dancer with arms raised in curves, a long skirt, a tilted hip scarf and coin fringe",
      tags=["bellydance", "oriental dance", "hip scarf", "coins", "middle eastern dance", "raqs sharqi", "dancer"])
def _(S):
    return [
        head(12, 5, 2.1),
        line("M12 8.5Q5.5 8.5 6.5 2.5"),
        line("M12 8.5Q18.5 8.5 17.5 2.5"),
        line(seg(12, 8, 12, 12)),
        shell(poly([(9, 13), (15, 11.8), (18.5, 21.5), (5.5, 21.5)], closed=True, r=S.r * 0.6)),
        mark(circle(9.3, 17, 1.05)), mark(circle(12.2, 16.6, 1.05)), mark(circle(15, 16.2, 1.05)),
    ]


@icon("sword-dance", CAT, "Dancer balanced on one foot between two crossed swords laid on the ground",
      tags=["sabre dance", "scottish", "highland", "swords", "folk dance", "balance", "dancer", "traditional"])
def _(S):
    return [
        head(12, 3.6, 2),
        line(seg(12, 6.6, 12, 13)),
        line(poly([(12, 8), (7, 6), (5.5, 9)], r=S.r)),
        line(poly([(12, 8), (17, 6), (18.5, 9)], r=S.r)),
        line(poly([(12, 13), (17, 14.5), (15.5, 17)], r=S.r)),
        line(seg(12, 13, 12, 17.5)),
        line(seg(3.5, 18.5, 20.5, 21.5)),
        line(seg(3.5, 21.5, 20.5, 18.5)),
    ]


@icon("poi-spinning", CAT, "Figure swinging two balls on cords, with circular trails on each side",
      tags=["poi", "fire spinning", "juggling", "flow arts", "festival", "performer", "swing", "circus"])
def _(S):
    parts = [
        head(12, 4.6, 2.1),
        line(seg(12, 7.8, 12, 15)),
        line(seg(12, 9.5, 8, 13)),
        line(seg(12, 9.5, 16, 13)),
        line(poly([(9.5, 21), (12, 15), (14.5, 21)], r=S.r)),
    ]
    for cx, sgn in ((8, -1), (16, 1)):
        parts.append(line(arc(cx, 13, 5, 90, 270) if sgn < 0 else arc(cx, 13, 5, 270, 450)))
        bx, by = cx + sgn * 3.6, 13 - 3.6
        parts.append(dot(bx, by, 1.9))
    return parts


@icon("color-guard", CAT, "Figure spinning a large waving flag on a tall pole",
      tags=["flag", "marching band", "flag twirling", "drill team", "winter guard", "banner", "parade", "performer"])
def _(S):
    flag = rnd(S, "M12.5 2.5C15 0.8 17 4.5 21 3V11C17 12.5 15 9 12.5 10.5Z",
               "M12.5 2.5C15 0.8 17 4.5 20.5 3V11C17 12.5 15 9 12.5 10.5Z")
    return [
        head(6, 7, 2.1),
        line(seg(6, 10, 6, 16)),
        line(poly([(6, 11.5), (12.5, 13.5)], r=0)),
        line(poly([(3.5, 21.5), (6, 16), (8.5, 21.5)], r=S.r)),
        line(seg(12.5, 2.5, 12.5, 21.5)),
        shell(flag),
    ]


@icon("ribbon-dance", CAT, "Figure holding a short stick with a long ribbon swirling into loops above",
      tags=["rhythmic gymnastics", "ribbon", "streamer", "twirl", "gymnast", "performance", "dancer", "swirl"])
def _(S):
    return [
        head(7, 10, 2.1),
        line(seg(7, 13, 7, 18)),
        line(seg(7, 14.5, 12, 11)),
        line(poly([(4.5, 21.5), (7, 18), (9.5, 21.5)], r=S.r)),
        line(seg(12, 11, 14, 8.5)),
        line("M14 8.5C10 5 13 2 17 3.5C21 5 20.5 10 17 9.5C14.5 9 15.5 6 18 6.5"),
    ]


@icon("conga-dance", CAT, "Line of three dancers one behind the other, hands linked on the shoulders ahead",
      tags=["conga line", "party dance", "wedding", "group dance", "train", "celebration", "latin", "dancers"])
def _(S):
    parts = [line(seg(4.5, 9, 19.5, 9))]
    for x in (4.5, 12, 19.5):
        parts += [head(x, 4.8, 1.9), line(seg(x, 7.5, x, 13.5)),
                  line(poly([(x - 1.6, 20), (x, 13.5), (x + 1.6, 20)], r=S.r))]
    return parts


# --------------------------------------------------------------------------- scenes

@icon("lullaby", CAT, "Crescent moon with two small music notes floating beside it",
      tags=["bedtime", "sleep", "night", "baby", "nursery", "goodnight", "soothing", "moon song"])
def _(S):
    return [
        shell("M11 3.5A8.5 8.5 0 1 0 11 20.5A10.5 10.5 0 0 1 11 3.5Z"),
        dot(16, 18, 1.6), dot(20.2, 16.6, 1.6),
        line(seg(17.5, 18, 17.5, 10.5)),
        line(seg(21.7, 16.6, 21.7, 9.1)),
        line(seg(17.5, 10.5, 21.7, 9.1)),
    ]


@icon("listening-to-music", CAT, "Head and shoulders of a person wearing headphones with a music note beside them",
      tags=["headphones", "listen", "playlist", "streaming", "audio", "enjoying music", "earphones", "person"])
def _(S):
    return [
        shell(circle(10, 10.5, 3.3)),
        line(arc(10, 10.5, 6.6, 180, 360)),
        shell(rect(2.5, 9.5, 2.8, 5, rnd(S, 0.8, 1.4))),
        shell(rect(14.7, 9.5, 2.8, 5, rnd(S, 0.8, 1.4))),
        line("M3.5 21.5V20.5a4.5 4.5 0 0 1 4.5-4.5h4a4.5 4.5 0 0 1 4.5 4.5v1"),
        dot(19, 8.5, 1.5),
        line(seg(20.4, 8.5, 20.4, 3)),
        line("M20.4 3q1.8 0.4 1.8 2.6"),
    ]


@icon("birdsong", CAT, "Small songbird on a twig with its beak open and music notes rising",
      tags=["singing bird", "tweet", "morning", "nature", "songbird", "chirp", "spring", "dawn chorus"])
def _(S):
    body = "M3.5 8L8.5 12.5C8.5 10.5 10.5 9.5 12.5 9.5C15.5 9.5 17 11.5 17 14C17 17 15 18 12.5 18H8.5C6.8 18 6.3 16.6 6.5 15.2Z"
    return [
        shell(body),
        line(poly([(17, 11.3), (20.5, 10.3)], r=0)),
        line(poly([(17, 13.3), (20, 14.3)], r=0)),
        mark(circle(14, 12.5, 0.9)),
        line(seg(3, 21, 21, 20)),
        dot(17.5, 4.5, 1.4), line(seg(18.8, 4.5, 18.8, 1.5)),
        dot(21, 7, 1.0),
    ]


@icon("campfire-song", CAT, "Acoustic guitar leaning beside a small campfire with a music note rising above",
      tags=["campfire", "singalong", "camping", "guitar", "sing along", "bonfire", "outdoors", "folk"])
def _(S):
    body = "M4.5 12.5C4.5 10.6 9.5 10.6 9.5 12.5C9.5 14.3 11 15 11 18C11 20.5 9 21.5 7 21.5C5 21.5 3 20.5 3 18C3 15 4.5 14.3 4.5 12.5Z"
    flame = "M17 8.5C19.3 11.5 20.3 13.5 20.3 15.8C20.3 18.3 18.8 19.5 17 19.5C15.2 19.5 13.7 18.3 13.7 15.8C13.7 13.5 14.7 12 17 8.5Z"
    return [
        shell(body),
        mark(circle(7, 16.6, 1.2)),
        line(seg(7, 3.5, 7, 11)),
        line(seg(12.5, 21.5, 21.5, 21.5)),
        shell(flame),
        dot(18.5, 4.5, 1.3), line(seg(19.7, 4.5, 19.7, 1.6)),
    ]


# --------------------------------------------------------------------------- instruments

@icon("paiban", CAT, "Clapper of flat wooden slats tied together at one end and fanned slightly open",
      tags=["clapper", "castanets", "chinese percussion", "wooden slats", "rhythm", "folk", "clappers", "kuaiban"])
def _(S):
    parts = []
    for ang in (-24, 0, 24):
        pts = rotp([(10.6, 3), (13.4, 3), (13.4, 18), (10.6, 18)], ang, 12, 19.5)
        parts.append(shell(poly(pts, closed=True, r=S.r * 0.2)))
    parts.append(line(seg(8.5, 19.5, 15.5, 19.5)))
    return parts


@icon("pipa", CAT, "Pear-shaped lute held upright with a short neck, frets and a bent-back pegbox",
      tags=["chinese lute", "plucked strings", "chinese music", "instrument", "strings", "traditional", "lute"])
def _(S):
    body = "M12 9.5C15 9.5 16.5 12 18.5 15.5C20 18.5 17 21.5 12 21.5C7 21.5 4 18.5 5.5 15.5C7.5 12 9 9.5 12 9.5Z"
    return [
        shell(body),
        line(seg(12, 9.5, 12, 3.5)),
        line("M12 3.5L9.5 1.8"),
        detail(seg(9.6, 13.6, 14.4, 13.6)),
        detail(seg(9, 16.6, 15, 16.6)),
        mark(rect(10.5, 19, 3, 1.2, 0)),
    ]


@icon("sarangi", CAT, "Squat bowed instrument with a waisted box body, wide short neck, side pegs and a bow",
      tags=["indian bowed", "hindustani", "bowed strings", "folk fiddle", "instrument", "strings", "rajasthani"])
def _(S):
    body = "M6.5 12.5H14.5C15.5 12.5 15.5 14.5 14.5 15.5C15.5 16.5 15.5 17.5 14.5 18.5C14.5 20.5 14 21.5 12.5 21.5H8.5C7 21.5 6.5 20.5 6.5 18.5C5.5 17.5 5.5 16.5 6.5 15.5C5.5 14.5 5.5 12.5 6.5 12.5Z"
    return [
        shell(body),
        shell(rect(8, 3.5, 5, 9, 0)),
        line(seg(5, 6, 8, 6)), line(seg(5, 9, 8, 9)),
        line(seg(17.5, 3, 20, 21)),
    ]


@icon("ranat", CAT, "Boat-shaped wooden resonator on a small stand with a row of bars across the top",
      tags=["xylophone", "thai", "southeast asia", "gamelan", "mallet", "percussion", "wooden bars", "traditional"])
def _(S):
    parts = [line(seg(x, 3.5, x, 9)) for x in (5.5, 9.2, 12.8, 16.5)]
    parts.append(shell("M2.5 9.5H21.5C20.5 14 17 16 12 16S3.5 14 2.5 9.5Z"))
    parts += [line(seg(12, 16, 12, 20.5)), line(seg(8, 21, 16, 21))]
    return parts


@icon("gong-circle", CAT, "Horseshoe of small kettle gongs set in a ring, each with a raised boss",
      tags=["gong chime", "kettle gongs", "gamelan", "bonang", "kulintang", "percussion", "ensemble", "southeast asia"])
def _(S):
    parts = []
    for ang in (130, 200, 270, 340, 410):
        x, y = pt_on(12, 11.5, 7.3, ang)
        parts.append(shell(poly(regular(x, y, 3.1, 8, start=-22.5), closed=True, r=S.r * 0.5)))
        parts.append(mark(circle(x, y, 0.8)))
    parts.append(line(seg(3, 21, 21, 21)))
    return parts


@icon("whirly-tube", CAT, "Corrugated ring of flexible tube with ridges, swung in a circle",
      tags=["whirlie", "corrugaphone", "hummer", "swinging tube", "sound toy", "science", "percussion", "educational"])
def _(S):
    ro, ri = 9, 5.5
    a1, a2 = 130, 410
    def P_(r, a):
        x, y = pt_on(12, 12, r, a)
        return f"{fmt(x)} {fmt(y)}"
    d = (f"M{P_(ro, a1)}A{ro} {ro} 0 1 1 {P_(ro, a2)}L{P_(ri, a2)}A{ri} {ri} 0 1 0 {P_(ri, a1)}Z")
    parts = [shell(d)]
    for ang in (170, 215, 260, 305, 350):
        x1, y1 = pt_on(12, 12, ri, ang)
        x2, y2 = pt_on(12, 12, ro, ang)
        parts.append(detail(seg(x1, y1, x2, y2)))
    return parts


@icon("cylinder-phonograph", CAT, "Small box with a wax cylinder on a horizontal spindle and a narrow horn above it",
      tags=["phonograph", "wax cylinder", "edison", "antique", "gramophone", "vintage audio", "horn", "retro"])
def _(S):
    return [
        shell(rect(3, 14.5, 18, 6.5, rnd(S, 1, 2))),
        shell(rect(5, 9, 9, 5.5, rnd(S, 0.5, 1.5))),
        shell(poly([(14, 10), (20.5, 3.5), (21.5, 8), (14, 13)], closed=True, r=S.r * 0.5)),
        mark(circle(17.5, 18, 1)),
    ]


@icon("carol-singing", CAT, "Two singers side by side sharing an open song sheet with a music note above",
      tags=["christmas carols", "caroling", "choir", "winter", "holiday songs", "singers", "hymn", "duet"])
def _(S):
    return [
        head(6.5, 10, 2.2), head(17.5, 10, 2.2),
        line("M2.5 21.5V19a4 4 0 0 1 8 0v2.5"),
        line("M13.5 21.5V19a4 4 0 0 1 8 0v2.5"),
        shell(rect(7.5, 14, 9, 7, rnd(S, 0.5, 1))),
        detail(seg(12, 14, 12, 21)),
        *note(10.3, 6.5, 4.5, 1.5),
    ]


@icon("whistling", CAT, "Head in profile with pursed lips and a small music note coming out",
      tags=["whistle", "whistling a tune", "puckered lips", "humming", "happy", "profile", "face", "tune"])
def _(S):
    face = "M5 21V16.5C3 14.5 2.5 11 3.5 8.5C4.8 5 8 3 11.5 3C14.5 3 16.5 5 16.5 7.5L18.5 10.3L16.7 11.2L17.6 12.6L16.5 13.6V16L13 17.3V21Z"
    return [
        shell(face),
        mark(circle(12.5, 8.2, 0.9)),
        dot(19.8, 15.2, 1.4), line(seg(21.2, 15.2, 21.2, 9.5)),
    ]
