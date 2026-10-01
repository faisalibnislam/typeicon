"""TypeIcon Core: inclusive (batch 001): hearing, low vision, braille and daily-living aids."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, transform_path

CAT = "inclusive"


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def tf(d, k=1.0, dx=0.0, dy=0.0, flip=False):
    """Scale (and optionally mirror) a path, then shift it."""
    a = -k if flip else k
    return path_to_d(transform_path(P(d), (a, 0, 0, k, dx, dy)))


def waves(cx, cy, radii, a0=-45, a1=45):
    return [line(arc(cx, cy, r, a0, a1)) for r in radii]


# head in profile facing left, nose at the left edge
HEAD = ("M9 21V17.2C7 16.5 5.8 15 5.6 13.6L3.8 13L5.3 10.5C5.8 6 8.5 3.5 12 3.5"
        "C16.5 3.5 19.5 7 19 11.5C18.7 14 17 15.5 15.5 16.5V21Z")


# ============================================================================ hearing

@icon("text-telephone", CAT, "Desk text telephone with a handset on top and a small keyboard below",
      tags=["tty", "tdd", "deaf", "text phone", "relay", "typing", "accessibility"], aliases=["tty"])
def _(S):
    return [
        shell(rect(4, 3, 16, 4, rr(S, 2))),
        line(seg(7, 7, 7, 11)),
        line(seg(17, 7, 17, 11)),
        shell(rect(3, 11, 18, 10, rr(S, 3))),
        detail(seg(7, 14.5, 17, 14.5)),
        dot(8, 18, 1.1), dot(12, 18, 1.1), dot(16, 18, 1.1),
    ]


@icon("remote-microphone-system", CAT, "Clip-on microphone sending wireless waves to a behind-the-ear hearing aid",
      tags=["fm system", "hearing", "wireless mic", "classroom", "deaf", "assistive listening"])
def _(S):
    return [
        shell(rect(2, 8, 5, 12, rr(S, 2.5))),
        detail(seg(4.5, 11.5, 4.5, 16.5)),
        *waves(7.5, 14, [3.5, 6.5], -45, 45),
        shell("M15.5 5.5A6.5 7.5 0 0 1 21.5 12.5C21.5 16 20.5 18.5 19.5 20.2A1.8 1.8 0 0 1 16.3 18.4C17 16.5 17.4 14.5 17.4 12.5C17.4 10 16.8 7.8 15.5 5.5Z"),
    ]


@icon("personal-sound-amplifier", CAT, "Palm-sized amplifier box with a dial, below a pair of headphones",
      tags=["psap", "hearing", "listening", "volume", "earphones", "assistive device"])
def _(S):
    return [
        line(arc(12, 9, 6.5, 180, 360)),
        shell(rect(4, 8.5, 3, 5.5, 1.25)),
        shell(rect(17, 8.5, 3, 5.5, 1.25)),
        shell(rect(5, 16, 14, 5.5, rr(S, 2.5))),
        detail(seg(8, 18.75, 12.5, 18.75)),
        dot(16, 18.75, 1),
    ]


@icon("amplified-telephone", CAT, "Desk phone with big number keys and sound waves rising from the handset",
      tags=["loud phone", "hearing", "volume", "big button phone", "elderly", "assistive"])
def _(S):
    return [
        shell(rect(3, 6, 13, 4, rr(S, 2))),
        *waves(16, 8, [3.5, 6.5], -50, 50),
        shell(rect(3, 14, 18, 7, rr(S, 3))),
        dot(7.5, 17.5, 1.4), dot(12, 17.5, 1.4), dot(16.5, 17.5, 1.4),
    ]


@icon("hearing-aid-battery", CAT, "Button cell battery with a peel-off tab on its face",
      tags=["hearing aid", "cell", "zinc air", "power", "tab", "replacement"])
def _(S):
    return [
        shell("M3.5 9V14A7.5 4 0 0 0 18.5 14V9A7.5 4 0 0 0 3.5 9Z"),
        detail("M3.5 9A7.5 4 0 0 0 18.5 9"),
        shell(poly([(14, 9.5), (19.5, 5), (22, 7.5), (17.5, 12)], closed=True, r=S.r)),
    ]


@icon("bone-anchored-hearing-device", CAT, "Head in profile with a round sound processor on the skull behind the ear",
      tags=["baha", "bone conduction", "implant", "hearing", "deaf", "processor"])
def _(S):
    return [
        shell(HEAD),
        detail("M12.5 9.2A2.2 2.2 0 1 0 12.5 13.4"),
        shell(circle(17, 9.5, 2.6)),
        dot(17, 9.5, 0.8),
    ]


@icon("cued-speech", CAT, "Face in profile with a hand held beside the mouth showing a handshape",
      tags=["lip reading", "speechreading", "hand cues", "deaf", "communication", "phonemes"])
def _(S):
    return [
        shell(tf(HEAD, 0.62, 14, 1, flip=True)),
        shell(rect(13, 14.5, 8, 6.5, rr(S, 3))),
        line(seg(15, 14.5, 15, 9)),
        line(seg(19, 14.5, 19, 9.5)),
    ]


@icon("live-captions", CAT, "Rounded screen showing a speech wave above two lines of caption text",
      tags=["subtitles", "real time", "transcription", "speech to text", "deaf", "video call"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, rr(S, 3))),
        detail(poly([(5, 8), (7, 8), (8.5, 5.5), (10.5, 10.5), (12, 6.5), (13.5, 8), (19, 8)])),
        detail(seg(6, 12.5, 18, 12.5)),
        detail(seg(6, 16, 13, 16)),
    ]


@icon("sound-recognition", CAT, "Phone showing a sound wave with a small bell alert beside it",
      tags=["sound alert", "deaf", "notification", "doorbell", "smoke alarm", "listening"])
def _(S):
    return [
        shell(rect(3, 6, 13, 16, rr(S, 3))),
        detail(poly([(6, 14), (8, 14), (9.5, 11), (11.5, 17), (13, 14)])),
        solid("M16.5 9.5H21.5C20.6 8.6 20.5 7.6 20.5 6.5A1.5 1.5 0 0 0 17.5 6.5C17.5 7.6 17.4 8.6 16.5 9.5Z"),
        solid(circle(19, 10.5, 0.9)),
    ]


@icon("flash-notification", CAT, "Back of a phone with its camera light flashing bright rays",
      tags=["led alert", "deaf", "visual alert", "ringing", "flashing light", "notification"])
def _(S):
    return [
        shell(rect(3, 3, 11, 18, rr(S, 3))),
        detail(circle(8.5, 8, 2.2)),
        line(seg(17, 6, 21, 4)),
        line(seg(17.5, 10, 22, 10)),
        line(seg(17, 14, 21, 16)),
    ]


@icon("sign-language-video", CAT, "Video window showing a person signing with both hands raised",
      tags=["video relay", "vrs", "interpreter", "deaf", "asl", "call"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, rr(S, 3))),
        detail(circle(12, 8.5, 2)),
        detail("M7.5 18A4.5 4.5 0 0 1 16.5 18"),
        dot(6.5, 11.5, 1.2), dot(17.5, 11.5, 1.2),
    ]


@icon("deaf-awareness-card", CAT, "Wallet card with an ear symbol on the left and text lines on the right",
      tags=["id card", "communication card", "hearing loss", "deaf", "badge", "awareness"])
def _(S):
    return [
        shell(rect(2, 4, 20, 16, rr(S, 3))),
        detail("M5.8 11A2.8 2.8 0 1 1 11.2 12C10.3 13 10.3 14.2 9.2 15A1.4 1.4 0 0 1 7.2 14.2"),
        detail(seg(14, 9, 19, 9)),
        detail(seg(14, 13, 19, 13)),
    ]


@icon("captioning-glasses", CAT, "Eyeglasses with two short lines of text floating on one lens",
      tags=["smart glasses", "subtitles", "ar", "deaf", "live captions", "wearable"])
def _(S):
    return [
        shell(rect(2.5, 6, 8.5, 12, rr(S, 4))),
        shell(rect(13, 6, 8.5, 12, rr(S, 4))),
        line(seg(11, 9.5, 13, 9.5)),
        detail(seg(5.5, 10.5, 8, 10.5)),
        detail(seg(5.5, 14, 8, 14)),
    ]


@icon("talking-watch", CAT, "Round wristwatch with sound waves coming from its face",
      tags=["speaking watch", "blind", "time", "audio", "low vision", "wearable"])
def _(S):
    return [
        shell(rect(6, 2.5, 6, 4, rr(S, 1.5))),
        shell(rect(6, 17.5, 6, 4, rr(S, 1.5))),
        shell(circle(9, 12, 5.5)),
        detail(poly([(9, 9), (9, 12), (11.3, 12)])),
        *waves(9, 12, [8.5, 11.5], -35, 35),
    ]


@icon("tactile-watch", CAT, "Wristwatch with raised dots at the hour positions and an open cover",
      tags=["braille watch", "blind", "touch", "time", "low vision", "wearable"])
def _(S):
    return [
        shell(rect(9, 2, 6, 4, rr(S, 1.5))),
        shell(rect(9, 18, 6, 4, rr(S, 1.5))),
        shell(circle(12, 12, 7)),
        dot(12, 7.8, 1.1), dot(12, 16.2, 1.1), dot(7.8, 12, 1.1), dot(16.2, 12, 1.1),
        detail(seg(12, 12, 14, 10)),
    ]


# ============================================================================ low vision

def bdots(x0, y0, pat, dx=3.2, dy=3.2, r=1.0):
    """Braille dots: pat lists dot numbers 1-6 (1-3 down the left column, 4-6 down the right)."""
    out = []
    for n in pat:
        col, row = (0, n - 1) if n <= 3 else (1, n - 4)
        out.append(dot(x0 + col * dx, y0 + row * dy, r))
    return out


@icon("liquid-level-indicator", CAT, "Mug with a small device on the rim and two prongs reaching into the drink",
      tags=["cup", "blind", "pour", "beep", "low vision", "kitchen aid", "fill"])
def _(S):
    return [
        shell("M3.5 8H15.5V16.5A3.5 3.5 0 0 1 12 20H7A3.5 3.5 0 0 1 3.5 16.5Z"),
        line("M15.5 10.5H18A2.5 2.5 0 0 1 18 15.5H15.5"),
        shell(rect(5.5, 2.5, 6, 5, rr(S, 1.5))),
        detail(seg(7, 8, 7, 13)),
        detail(seg(10.5, 8, 10.5, 13)),
    ]


@icon("bump-dots", CAT, "Round oven knob with three raised dots stuck around its edge",
      tags=["tactile marker", "bump on", "locator dots", "blind", "low vision", "appliance dial"])
def _(S):
    return [
        shell(circle(12, 12, 4.6)),
        detail(seg(12, 12, 14.2, 9.8)),
        dot(12, 3.5, 1.4), dot(19.4, 16.25, 1.4), dot(4.6, 16.25, 1.4),
    ]


@icon("stand-magnifier", CAT, "Round lens on a short three-legged stand above a line of text",
      tags=["desk magnifier", "reading aid", "low vision", "zoom", "lens", "magnifying glass stand"])
def _(S):
    return [
        shell(circle(12, 8, 5.5)),
        detail(arc(12, 8, 2.5, 200, 280)),
        line(seg(7.5, 12.5, 4.5, 19)),
        line(seg(16.5, 12.5, 19.5, 19)),
        line(seg(12, 14, 12, 19)),
        line(seg(2.5, 21, 21.5, 21)),
    ]


@icon("bar-magnifier", CAT, "Clear magnifying bar lying across lines of text with one line enlarged",
      tags=["reading bar", "line magnifier", "low vision", "dyslexia", "reading aid", "ruler lens"])
def _(S):
    return [
        line(seg(3, 4, 21, 4)),
        shell(rect(2, 8, 20, 8, rr(S, 3))),
        detail(seg(5.5, 12, 18.5, 12)),
        line(seg(3, 20, 21, 20)),
    ]


@icon("head-worn-magnifier", CAT, "Headband visor with two thick magnifying lenses flipped down in front of the eyes",
      tags=["loupe glasses", "visor", "low vision", "close work", "craft", "reading aid"])
def _(S):
    return [
        line("M4.5 13A7.5 7.5 0 0 1 19.5 13"),
        shell(rect(3.5, 12, 7, 7.5, min(S.R, 3.5))),
        shell(rect(13.5, 12, 7, 7.5, min(S.R, 3.5))),
        line(seg(10.5, 15.5, 13.5, 15.5)),
    ]


@icon("handheld-monocular", CAT, "Short single-eye telescope with a wrist strap, seen from the side",
      tags=["spotting scope", "low vision", "distance viewing", "telescope", "zoom", "magnifier"])
def _(S):
    return [
        shell(rect(2.5, 10.5, 4.5, 3, min(S.R, 1.5))),
        shell(rect(7, 8.5, 6, 7, min(S.R, 2.5))),
        shell(rect(13, 6.5, 8, 11, min(S.R, 3))),
        detail(seg(17, 9.5, 17, 14.5)),
    ]


@icon("vision-assist-glasses", CAT, "Eyeglasses with a small camera on top and sound waves for spoken descriptions",
      tags=["smart glasses", "blind", "camera", "ai describe", "low vision", "wearable"])
def _(S):
    return [
        shell(circle(6.5, 15, 4)),
        shell(circle(17.5, 15, 4)),
        line("M10.5 14.5A1.8 1.8 0 0 1 13.5 14.5"),
        solid(rect(15, 4.5, 6, 3.5, 1)),
        line(arc(7, 8.5, 2.5, 195, 285)),
        line(arc(7, 8.5, 5.5, 195, 285)),
    ]


@icon("signature-guide", CAT, "Card with a rectangular cut-out window and a short signature scribble inside it",
      tags=["sign here", "writing guide", "blind", "low vision", "template", "form filling"])
def _(S):
    return [
        shell(rect(2, 4, 20, 16, rr(S, 3))),
        detail(rect(5, 8.5, 14, 7, rr(S, 1))),
        detail(poly([(8, 13), (10, 11), (12, 13.2), (14, 11), (16, 12.5)])),
    ]


@icon("raised-line-paper", CAT, "Sheet of paper with thick raised writing lines",
      tags=["tactile paper", "writing guide", "blind", "low vision", "notebook", "handwriting"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 3))),
        Part("dot", rect(7, 6.5, 10, 3, 1.5)),
        Part("dot", rect(7, 11, 10, 3, 1.5)),
        Part("dot", rect(7, 15.5, 10, 3, 1.5)),
    ]


@icon("tactile-drawing-board", CAT, "Drawing board with a raised star and a stylus drawing on it",
      tags=["raised drawing", "blind", "stylus", "tactile graphics", "art", "touch"])
def _(S):
    star = []
    for i in range(10):
        rad = 5 if i % 2 == 0 else 2.2
        a = math.radians(-90 + i * 36)
        star.append((9 + rad * math.cos(a), 13.5 + rad * math.sin(a)))
    return [
        shell(rect(2, 4, 20, 17, rr(S, 3))),
        detail(poly(star, closed=True, r=S.r * 0.3)),
        line(seg(21, 2.5, 14.5, 9)),
    ]


@icon("tactile-ruler", CAT, "Ruler with raised notches along its top edge and braille dots between them",
      tags=["braille ruler", "measure", "blind", "low vision", "tactile", "school"])
def _(S):
    return [
        shell(rect(2, 6, 20, 12, rr(S, 2.5))),
        detail(seg(6, 6.5, 6, 10)),
        detail(seg(10, 6.5, 10, 10)),
        detail(seg(14, 6.5, 14, 10)),
        detail(seg(18, 6.5, 18, 10)),
        dot(8, 14.2, 1), dot(12, 14.2, 1), dot(16, 14.2, 1),
    ]


@icon("braille-dice", CAT, "Cube die with braille dots on its faces instead of pips",
      tags=["game", "blind", "tactile game", "accessible toy", "play", "touch"])
def _(S):
    return [
        shell(poly([(12, 3), (20, 7.5), (20, 16.5), (12, 21), (4, 16.5), (4, 7.5)], closed=True, r=S.r)),
        detail(poly([(4, 7.5), (12, 12), (20, 7.5)])),
        detail(seg(12, 12, 12, 21)),
        dot(12, 7.4, 0.9),
        dot(7.3, 13.3, 0.9), dot(8.3, 17.2, 0.9),
        dot(16.7, 13.3, 0.9), dot(15.7, 17.2, 0.9),
    ]


@icon("braille-playing-card", CAT, "Playing card with a diamond in the middle and a small braille cell in the corner",
      tags=["cards", "game", "blind", "accessible", "tactile", "poker"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rr(S, 3))),
        *bdots(8.5, 6.2, [1, 2, 4], dx=3, dy=3, r=0.95),
        detail(poly([(14, 11), (17, 15), (14, 19), (11, 15)], closed=True)),
    ]


@icon("braille-medicine-box", CAT, "Medicine carton with a cross on its front and a row of braille dots",
      tags=["pharmacy", "blind", "drug label", "tablets", "packaging", "tactile label"])
def _(S):
    return [
        shell(rect(2.5, 5, 19, 15, rr(S, 3))),
        detail(seg(2.5, 9, 21.5, 9)),
        detail(seg(7, 12.5, 7, 17.5)),
        detail(seg(4.5, 15, 9.5, 15)),
        dot(14, 13.5, 1), dot(17.5, 13.5, 1), dot(14, 17, 1),
    ]


@icon("tactile-room-sign", CAT, "Wall sign plate with raised letters above a row of braille dots",
      tags=["door sign", "wayfinding", "blind", "tactile", "ada signage", "braille sign"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 17, rr(S, 3))),
        detail(poly([(6, 12), (8.5, 6.5), (11, 12)])),
        detail(seg(7, 10, 10, 10)),
        detail(poly([(18, 6.5), (14.5, 6.5), (14.5, 12), (18, 12)])),
        detail(seg(14.5, 9.2, 17.2, 9.2)),
        dot(7, 16.5, 1), dot(12, 16.5, 1), dot(17, 16.5, 1),
    ]


# ============================================================================ daily living

def rot(pts, deg=45, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * sn, cy + (x - cx) * sn + (y - cy) * c) for x, y in pts]


@icon("braille-elevator-button", CAT, "Round call button with a raised arrow above a pair of braille dots",
      tags=["lift", "call button", "blind", "tactile", "up", "accessible elevator"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(poly([(8.5, 11), (12, 6.5), (15.5, 11)], closed=True)),
        dot(9.8, 15.3, 1), dot(14.2, 15.3, 1),
    ]


@icon("talking-book-player", CAT, "Boxy handheld audio book player with a speaker grille, disc slot and big buttons",
      tags=["audiobook", "daisy player", "blind", "reading", "cassette", "listening device"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 3))),
        dot(8, 6.5, 0.9), dot(12, 6.5, 0.9), dot(16, 6.5, 0.9),
        detail(seg(7.5, 10, 16.5, 10)),
        detail(circle(8.5, 15.5, 1.6)),
        detail(circle(15.5, 15.5, 1.6)),
    ]


@icon("talking-color-identifier", CAT, "Handheld sensor touching a fabric swatch with a speech bubble above it",
      tags=["colour identifier", "color reader", "blind", "clothing", "speaks colors", "low vision"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 6, rr(S, 3))),
        dot(8.5, 5.5, 0.9), dot(12, 5.5, 0.9), dot(15.5, 5.5, 0.9),
        shell(rect(3.5, 12.5, 6, 9, rr(S, 2.5))),
        shell(rect(12.5, 12.5, 9, 9, rr(S, 2))),
        detail(seg(14, 18.5, 20, 15)),
    ]


@icon("banknote-identifier", CAT, "Small reader with a banknote half inserted and sound waves beside it",
      tags=["money reader", "currency", "blind", "low vision", "cash", "speaks denomination"])
def _(S):
    return [
        line("M5.5 13V4H14.5V13"),
        dot(10, 8.5, 1.3),
        *waves(15, 8.5, [4, 7], -45, 45),
        shell(rect(2.5, 12.5, 19, 8, rr(S, 3))),
        detail(seg(6, 16.5, 15, 16.5)),
        dot(18.2, 16.5, 0.9),
    ]


@icon("tactile-exhibit", CAT, "Small bust on a plinth with two hands reaching in to feel its surface",
      tags=["touch tour", "museum", "blind", "sculpture", "hands on", "accessible art"])
def _(S):
    return [
        shell(circle(12, 6.2, 3)),
        shell("M7.5 17C7.5 12.5 9.5 10.8 12 10.8C14.5 10.8 16.5 12.5 16.5 17Z"),
        shell(rect(5, 17, 14, 4.5, rr(S, 1.5))),
        line(seg(2.5, 14.5, 6, 12.5)),
        line(seg(21.5, 14.5, 18, 12.5)),
    ]


@icon("contrasting-stair-nosing", CAT, "Side view of steps with a bold strip along the front edge of each tread",
      tags=["stairs", "low vision", "safety", "trip hazard", "edge marking", "building access"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 17), (9, 17), (9, 12), (15, 12), (15, 7), (21, 7), (21, 21)], closed=True, r=S.r * 0.6)),
        Part("dot", rect(4.5, 18.2, 3, 1.6)),
        Part("dot", rect(10.5, 13.2, 3, 1.6)),
        Part("dot", rect(16.5, 8.2, 3, 1.6)),
    ]


@icon("gait-belt", CAT, "Wide belt with a buckle and fabric loop handles along its length",
      tags=["transfer belt", "caregiver", "patient handling", "walking aid", "mobility", "support"])
def _(S):
    return [
        line(poly([(4.5, 10), (4.5, 5.5), (8.5, 5.5), (8.5, 10)], r=S.r)),
        line(poly([(15.5, 10), (15.5, 5.5), (19.5, 5.5), (19.5, 10)], r=S.r)),
        shell(rect(2, 10, 20, 7, rr(S, 2))),
        detail(rect(9.5, 12.2, 5, 2.6, 0.6)),
    ]


@icon("ceiling-track-hoist", CAT, "Overhead ceiling rail with a motor unit holding a sling by two straps",
      tags=["patient lift", "overhead lift", "transfer", "caregiver", "mobility", "hoist"])
def _(S):
    return [
        line(seg(2, 3, 22, 3)),
        shell(rect(8, 4.5, 8, 5, rr(S, 2))),
        line(seg(10, 9.5, 5, 15)),
        line(seg(14, 9.5, 19, 15)),
        shell("M3.5 15H20.5C19.5 19.5 16 21 12 21C8 21 4.5 19.5 3.5 15Z"),
    ]


@icon("bath-lift", CAT, "Bathtub with a seat raised on a scissor base above the water line",
      tags=["bathing aid", "bath chair", "mobility", "elderly", "bathroom", "lift"])
def _(S):
    return [
        shell("M2.5 11H21.5V15C21.5 18.5 19.5 20 16.5 20H7.5C4.5 20 2.5 18.5 2.5 15Z"),
        shell(rect(6, 7.5, 11, 2.5, 1)),
        line(seg(6, 2.5, 6, 7.5)),
        detail(poly([(8, 17), (11.5, 13.5), (15, 17)])),
    ]


@icon("bath-transfer-bench", CAT, "Bench straddling a bath wall with two legs inside the tub and two outside",
      tags=["shower chair", "tub bench", "bathing aid", "elderly", "bathroom", "seat"])
def _(S):
    return [
        line(seg(3, 2.5, 3, 8)),
        shell(rect(3, 7.5, 18, 3, 1)),
        shell(rect(9.5, 10.5, 3.5, 10.5, rr(S, 1))),
        line(seg(4.5, 10.5, 4.5, 21)),
        line(seg(19.5, 10.5, 19.5, 18.5)),
        line(seg(13, 18.5, 22, 18.5)),
    ]


@icon("toilet-safety-frame", CAT, "Toilet seen from the front with a tubular armrest frame on both sides",
      tags=["toilet rail", "grab bar", "commode frame", "elderly", "bathroom", "support"])
def _(S):
    return [
        shell(rect(3, 3, 6, 7.5, rr(S, 2))),
        shell("M3 11.5H17C17 15 14.5 17.5 12 18.5V21H7V18.5C4.5 17.5 3 15 3 11.5Z"),
        line(poly([(21, 21), (21, 8), (13.5, 8)], r=S.r)),
    ]


@icon("pressure-relief-mattress", CAT, "Mattress of rounded air cells with a small pump box at the foot",
      tags=["air mattress", "bed sore", "pressure ulcer", "care", "hospital bed", "cushion"])
def _(S):
    return [
        shell("M2.5 19V13A2.4 2.4 0 0 1 7.3 13A2.4 2.4 0 0 1 12.1 13A2.4 2.4 0 0 1 16.9 13V19Z"),
        detail(seg(7.3, 13.5, 7.3, 18.5)),
        detail(seg(12.1, 13.5, 12.1, 18.5)),
        line(seg(17, 15.5, 18.5, 15.5)),
        shell(rect(18.5, 12.5, 3.5, 6, rr(S, 1.5))),
    ]


@icon("long-handled-shoehorn", CAT, "Tall slim shoehorn with a curved scoop at the bottom and a hook at the top",
      tags=["shoe aid", "dressing aid", "reach", "elderly", "footwear", "mobility"])
def _(S):
    return [
        line("M12 13.5V5.5A3.2 3.2 0 0 1 18.4 5.5"),
        shell("M10.5 12.5H13.5V14C16 16 16.5 19 15.5 21H8.5C7.5 19 8 16 10.5 14Z", stroke_miterlimit="2"),
    ]


@icon("dressing-stick", CAT, "Long dowel with a C-shaped hook on one end and a short push hook on the other",
      tags=["dressing aid", "reach", "pull on clothes", "elderly", "mobility", "stick"])
def _(S):
    return [
        line(poly(rot([(12, 21), (12, 5.5), (6.5, 5.5), (6.5, 9)]), r=S.r)),
        line(poly(rot([(8.5, 21), (15.5, 21)]))),
    ]


@icon("elastic-shoelaces", CAT, "Sneaker with coiled elastic laces and a small lock toggle instead of a bow",
      tags=["no tie laces", "shoes", "dressing aid", "easy fasten", "footwear", "stretch laces"])
def _(S):
    return [
        shell("M3.5 6.5H8.5C9 9 11 10.5 14 11C18 11.5 21 13 21 16V18H3.5Z"),
        detail(seg(3.5, 15, 21, 15)),
        line("M9.5 11.8C9.5 8.8 12 8.8 12 11.8C12 8.8 14.5 8.8 14.5 11.8"),
        dot(17.2, 11.8, 1.1),
    ]


@icon("rocker-knife", CAT, "Knife with a deep curved blade that rocks, and a T-shaped handle on top",
      tags=["adaptive cutlery", "one handed", "kitchen aid", "cutting", "eating aid", "arthritis"])
def _(S):
    return [
        shell(rect(6, 2.5, 12, 3.5, rr(S, 1.75))),
        line(seg(12, 6, 12, 13.5)),
        shell("M3.5 13.5H20.5C19 18.5 15.5 20.5 12 20.5C8.5 20.5 5 18.5 3.5 13.5Z"),
    ]


@icon("plate-guard", CAT, "Round plate with a raised curved wall along half of its rim",
      tags=["scoop dish", "adaptive plate", "eating aid", "one handed", "dining", "tableware"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        Part("dot", path_to_d(ST(arc(12, 12, 6.6, -70, 70), 3.2 if S.name == "line" else 3.6, S.cap, S.join))),
    ]


@icon("cutout-cup", CAT, "Tapered cup with a U-shaped notch cut into the rim",
      tags=["nose cutout", "drinking aid", "adaptive cup", "dysphagia", "tableware", "care"])
def _(S):
    return [
        shell(poly([(3.5, 4), (9, 4), (9, 8.5), (15, 8.5), (15, 4), (20.5, 4), (18, 20), (6, 20)], closed=True, r=S.r)),
    ]


@icon("one-handed-cutting-board", CAT, "Cutting board with raised corner rails and spikes holding a potato in place",
      tags=["kitchen aid", "one hand", "food prep", "adaptive", "chopping", "stroke"])
def _(S):
    return [
        shell(ellipse(12, 8.5, 6.5, 4.2)),
        line(seg(9.5, 12.5, 9.5, 16)),
        line(seg(14.5, 12.5, 14.5, 16)),
        shell(rect(2, 16, 20, 4.5, rr(S, 1.5))),
        line(poly([(3.5, 16), (3.5, 12.5), (6, 12.5)], r=S.r)),
        line(poly([(20.5, 16), (20.5, 12.5), (18, 12.5)], r=S.r)),
    ]


@icon("kettle-tipper", CAT, "Kettle tilted in a hinged stand to pour into a cup below",
      tags=["pouring aid", "kettle stand", "tremor", "arthritis", "kitchen aid", "hot water"])
def _(S):
    body = rot([(3.5, 6), (13.5, 6), (13.5, 16), (3.5, 16)], 25, 9, 11)
    spout = rot([(13.5, 9), (17.5, 7.5)], 25, 9, 11)
    return [
        shell(poly(body, closed=True, r=S.r)),
        line(poly(spout)),
        shell(rect(15.5, 16.5, 6, 4.5, rr(S, 1.5))),
        dot(18.8, 13.6, 0.9),
        line(seg(2.5, 21, 12, 21)),
        line(seg(7, 21, 7, 18)),
    ]


@icon("universal-cuff", CAT, "Strap cuff with a pocket that holds a spoon handle upright",
      tags=["utensil holder", "grip aid", "adaptive cutlery", "eating aid", "weak grip", "arthritis"])
def _(S):
    return [
        shell(rect(10, 13, 11, 8, rr(S, 3))),
        line(seg(13, 15, 17.5, 9.5)),
        shell(path_to_d(transform_path(P(ellipse(0, 0, 2.6, 4.3)), (math.cos(math.radians(40)), math.sin(math.radians(40)), -math.sin(math.radians(40)), math.cos(math.radians(40)), 18.3, 6.3)))),
        line(seg(10, 17, 3, 17)),
    ]


@icon("key-turner", CAT, "Large paddle handle holding a key at its tip for easier twisting",
      tags=["key holder", "grip aid", "arthritis", "weak grip", "door", "adaptive tool"])
def _(S):
    return [
        shell(rect(2.5, 8, 12, 8, min(S.R, 4))),
        detail(seg(6, 10.5, 6, 13.5)),
        detail(seg(10, 10.5, 10, 13.5)),
        line(seg(14.5, 12, 21.5, 12)),
        line(seg(19, 12, 19, 16)),
        line(seg(21.5, 12, 21.5, 15)),
    ]


@icon("tap-turner", CAT, "Long lever arm clamped across a round faucet head to make turning easier",
      tags=["faucet aid", "tap aid", "grip", "arthritis", "weak grip", "bathroom"])
def _(S):
    return [
        shell(circle(9.5, 14.5, 6.5)),
        detail(circle(9.5, 14.5, 2.2)),
        shell(poly(rot([(9.5, 12.8), (23, 12.8), (23, 16.2), (9.5, 16.2)], -42, 9.5, 14.5), closed=True, r=S.r), stroke_miterlimit="2"),
    ]


@icon("lever-tap", CAT, "Faucet with one long lever handle reaching sideways for easy operation",
      tags=["mixer tap", "faucet", "accessible bathroom", "elbow operation", "arthritis", "sink"])
def _(S):
    return [
        shell(rect(7.5, 11, 6, 10, rr(S, 2))),
        line(poly([(10.5, 11), (10.5, 5.5), (18.5, 5.5), (18.5, 8.5)], r=S.r)),
        line(seg(3, 3, 10.5, 5.5)),
        dot(18.5, 12.5, 1.1),
    ]


@icon("doorknob-lever-adapter", CAT, "Round doorknob with a long lever arm fitted over it",
      tags=["door handle", "knob extender", "arthritis", "weak grip", "accessible door", "lever"])
def _(S):
    return [
        line(seg(3, 2.5, 3, 21.5)),
        line(seg(3, 10, 5.5, 10)),
        shell(circle(10, 10, 4.5)),
        shell(poly(rot([(9, 8.5), (21, 8.5), (21, 11.5), (9, 11.5)], 32, 10, 10), closed=True, r=S.r)),
    ]


@icon("rocker-light-switch", CAT, "Wall plate with one large rocker paddle switch filling most of it",
      tags=["light switch", "wall plate", "easy switch", "accessible", "electrical", "arthritis"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 3))),
        detail(rect(7.5, 6, 9, 12, rr(S, 2))),
        Part("dot", rect(8.5, 12.5, 7, 4.2, 0.8)),
    ]


@icon("big-button-tv-remote", CAT, "Chunky remote control with four very large round buttons",
      tags=["simple remote", "large button", "elderly", "dementia", "low vision", "television"])
def _(S):
    return [
        shell(rect(6.5, 2, 11, 20, rr(S, 3.5))),
        detail(seg(10.5, 5.2, 13.5, 5.2)),
        dot(9.7, 10.5, 2), dot(14.3, 10.5, 2), dot(9.7, 16.5, 2), dot(14.3, 16.5, 2),
    ]


@icon("leg-lifter", CAT, "Strap with a hand loop at one end and a foot loop at the other",
      tags=["leg lift strap", "mobility aid", "bed", "car transfer", "elderly", "dressing aid"])
def _(S):
    return [
        shell(rect(2.5, 14.5, 7, 7, min(S.R, 3.5))),
        shell(rect(14.5, 2.5, 7, 7, min(S.R, 3.5))),
        line(seg(8, 15, 16, 9)),
    ]


@icon("seat-cane", CAT, "Walking stick with a folding fabric seat on three legs near the handle",
      tags=["folding stool", "cane chair", "walking aid", "elderly", "rest", "mobility"])
def _(S):
    return [
        line("M12 8V5.5A3 3 0 0 1 18 5.5"),
        shell(poly([(3.5, 8.5), (20.5, 8.5), (17.5, 11.5), (6.5, 11.5)], closed=True, r=S.r * 0.6)),
        line(seg(7.5, 11.5, 4.5, 21.5)),
        line(seg(16.5, 11.5, 19.5, 21.5)),
        line(seg(12, 11.5, 12, 21.5)),
    ]


@icon("threshold-ramp", CAT, "Small wedge ramp laid against a doorway step, seen from the side",
      tags=["door ramp", "wheelchair", "step", "accessible entrance", "mobility", "curb"])
def _(S):
    return [
        shell(poly([(3.5, 20), (14, 13), (21, 13), (21, 20)], closed=True, r=S.r), stroke_miterlimit="2"),
        line(seg(21, 3, 21, 13)),
    ]


# ============================================================================ wheelchairs and reading aids

def wheel(S, cx=9.5, cy=15.5, r=5.5):
    return [line(circle(cx, cy, r)), dot(cx, cy, 1.5)]


@icon("tilt-in-space-wheelchair", CAT, "Wheelchair in side view with the seat and backrest tilted back together and a headrest",
      tags=["tilt chair", "reclining wheelchair", "posture", "pressure relief", "care chair", "mobility"])
def _(S):
    return [
        *wheel(S),
        line(poly([(3, 3.5), (6, 10), (15.5, 8), (17.5, 17.5), (20.5, 17.5)], r=S.r)),
        solid(poly([(1.5, 3.2), (4.6, 1.6), (5.6, 3.6), (2.5, 5.2)], closed=True)),
        dot(17.5, 20.5, 1.5),
    ]


@icon("standing-wheelchair", CAT, "Wheelchair in side view with the seat raised to a standing position and knee pads",
      tags=["stand up wheelchair", "upright", "mobility", "rehab", "standing frame", "care"])
def _(S):
    return [
        *wheel(S, 9.5, 16, 5),
        line(poly([(6, 2.5), (8.5, 12), (13, 12)], r=S.r)),
        line(poly([(15.5, 6), (16, 17.5), (20.5, 17.5)], r=S.r)),
        solid(rect(13.5, 5, 4, 6, 1)),
        line(seg(7.5, 7.5, 13.5, 7.5)),
        dot(17.5, 20.5, 1.5),
    ]


@icon("all-terrain-wheelchair", CAT, "Wheelchair in side view riding on a rubber track instead of wheels",
      tags=["track chair", "off road", "outdoor", "beach", "trail", "mobility"])
def _(S):
    return [
        line(poly([(4.5, 2.5), (6, 7.5), (14.5, 7.5), (17, 12), (20.5, 12)], r=S.r)),
        line(seg(10, 7.5, 10, 15)),
        shell(rect(2.5, 15, 19, 6.5, min(S.R, 3.25))),
        dot(7, 18.25, 1.2), dot(17, 18.25, 1.2),
    ]


@icon("wheelchair-cushion", CAT, "Square seat cushion with a grid of rounded air cells",
      tags=["seat pad", "pressure relief", "gel cushion", "air cushion", "pressure sore", "comfort"])
def _(S):
    return [
        shell(rect(2.5, 4, 19, 16, rr(S, 3))),
        detail(circle(7.5, 9.3, 1.3)), detail(circle(12, 9.3, 1.3)), detail(circle(16.5, 9.3, 1.3)),
        detail(circle(7.5, 14.7, 1.3)), detail(circle(12, 14.7, 1.3)), detail(circle(16.5, 14.7, 1.3)),
    ]


@icon("wheelchair-lap-tray", CAT, "Flat tray with a curved cutout for the body at its front edge",
      tags=["lap tray", "table", "armrest tray", "eating", "activity tray", "mobility"])
def _(S):
    cut = "M3 4.5H21V19.5H16.5A4.5 4.5 0 0 0 7.5 19.5H3Z" if S.name == "line" else "M6 4.5H18A3 3 0 0 1 21 7.5V16.5A3 3 0 0 1 18 19.5H16.5A4.5 4.5 0 0 0 7.5 19.5H6A3 3 0 0 1 3 16.5V7.5A3 3 0 0 1 6 4.5Z"
    return [
        shell(cut),
        detail(seg(7, 8.5, 17, 8.5)),
    ]


@icon("wheelchair-joystick", CAT, "Armrest control box with a ball-topped joystick and a small display",
      tags=["power chair", "drive control", "electric wheelchair", "controller", "mobility", "joystick"])
def _(S):
    return [
        shell(circle(8, 5.5, 3)),
        line(seg(8, 8.5, 8, 12)),
        shell(rect(2.5, 12, 19, 9, rr(S, 3))),
        detail(rect(12.5, 14.7, 6, 3.3, 0.8)),
    ]


@icon("wheelchair-securement", CAT, "Wheelchair wheel held by a ratchet strap hooked to a floor track",
      tags=["tie down", "restraint", "vehicle transport", "van", "safety strap", "accessible transport"])
def _(S):
    return [
        *wheel(S, 9, 9.5, 5.5),
        shell(poly([(2.5, 19), (21.5, 19), (21.5, 21.5), (2.5, 21.5)], closed=True, r=S.r)),
        line(seg(14, 12.5, 18.5, 19)),
        solid(poly(rot([(15, 14.5), (17.6, 14.5), (17.6, 16.8), (15, 16.8)], -35, 16.3, 15.6), closed=True)),
    ]


@icon("wheelchair-push-gloves", CAT, "Fingerless padded glove seen from the palm side",
      tags=["gloves", "wheelchair user", "grip", "hand protection", "push rim", "mobility"])
def _(S):
    return [
        line(seg(7, 9, 7, 4.5)), line(seg(10.5, 9, 10.5, 3.5)), line(seg(14, 9, 14, 3.5)), line(seg(17.5, 9, 17.5, 4.5)),
        shell(rect(5.5, 9, 13, 12, min(S.R, 4))),
        detail(seg(8.5, 13, 15.5, 13)),
        line(poly([(5.5, 15), (2.5, 12), (2.5, 9.5)], r=S.r)),
    ]


@icon("wheelchair-scale", CAT, "Low platform scale with a ramp on one side and a readout on a post",
      tags=["weighing", "patient weight", "ramp scale", "clinic", "mobility", "health"])
def _(S):
    return [
        shell(rect(13, 2.5, 8.5, 5.5, rr(S, 1.5))),
        detail(seg(15.2, 5.25, 19.3, 5.25)),
        line(seg(17.2, 8, 17.2, 16.5)),
        shell(poly([(3.5, 21), (8, 16.5), (21, 16.5), (21, 21)], closed=True, r=S.r), stroke_miterlimit="2"),
    ]


@icon("page-turner", CAT, "Open book with a motorized arm lifting and turning one page",
      tags=["book aid", "reading aid", "automatic", "paralysis", "motor", "assistive device"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 6, 4, rr(S, 1.5))),
        line(seg(8.5, 5.5, 14, 8)),
        shell(poly([(2, 12), (12, 14), (22, 12), (22, 20.5), (12, 22), (2, 20.5)], closed=True, r=S.r)),
        detail(seg(12, 14, 12, 22)),
        line("M12 14C12.5 9.5 16 8 19 9"),
    ]


@icon("universal-book-holder", CAT, "Adjustable arm clamped to a table edge that holds an open book upright",
      tags=["book stand", "reading stand", "table clamp", "hands free", "arthritis", "reading aid"])
def _(S):
    return [
        shell(rect(11, 2.5, 10.5, 12.5, rr(S, 2))),
        detail(seg(16.25, 5, 16.25, 12.5)),
        line(poly([(6.5, 17), (6.5, 11), (11, 11)], r=S.r)),
        shell(rect(2.5, 17, 9, 4.5, 1)),
        line(seg(4.5, 14.5, 4.5, 19)),
    ]


# ============================================================================ animals, transport and driving

@icon("hearing-dog", CAT, "Dog head in profile with one ear raised and sound waves arriving above it",
      tags=["assistance dog", "deaf", "alert dog", "service animal", "sound", "listening"])
def _(S):
    head = [(3.5, 18), (3.5, 12), (5.5, 10), (10, 10), (12.5, 12), (20, 12), (21.5, 13.5), (21.5, 16), (19, 17), (13, 17), (11, 20.5), (6, 20.5)]
    return [
        shell(poly(head, closed=True, r=S.r), stroke_miterlimit="2"),
        shell(poly([(5.5, 10.5), (7, 4), (11, 10.5)], closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
        dot(9.5, 13.8, 0.95),
        dot(20, 14, 0.8),
        line(arc(13, 8, 3, -75, -15)),
        line(arc(13, 8, 5.8, -75, -15)),
    ]


@icon("mobility-assistance-dog", CAT, "Dog wearing a handle harness standing beside a wheelchair wheel",
      tags=["service dog", "assistance dog", "wheelchair", "retrieve", "harness", "disability"])
def _(S):
    raw = [(2.5, 9.5), (5, 7.5), (6.5, 4.5), (8, 7), (10, 9), (15, 9), (16, 9), (18.5, 6.5), (17, 10.5), (16.5, 13), (16.5, 20.5), (14.5, 20.5),
           (14.5, 15), (9, 15), (9, 20.5), (7.5, 20.5), (7.5, 13.5), (5.5, 12), (4.5, 12), (2.5, 11.5)]
    body = [(2 + (x - 2.5) * 0.8, 20.5 - (20.5 - y) * 0.85) for x, y in raw]
    return [
        shell(poly(body, closed=True, r=S.r * 0.7), stroke_miterlimit="2"),
        line(poly([(7, 8), (7, 4.5), (10, 4.5), (10, 8)], r=S.r)),
        line(circle(19, 15.8, 3.3)),
        dot(19, 15.8, 0.9),
    ]


@icon("seizure-alert-dog", CAT, "Lying dog with a head raised and a pulse line above it",
      tags=["epilepsy", "service dog", "alert dog", "medical alert", "warning", "assistance dog"])
def _(S):
    body = [(3, 19.5), (3, 15), (6.5, 12.5), (12.5, 12.5), (14, 9), (17, 7.5), (20.5, 9.5), (19.5, 12), (16.5, 12.5), (16.5, 16.5), (21, 16.5), (21, 19.5)]
    return [
        shell(poly(body, closed=True, r=S.r), stroke_miterlimit="2"),
        dot(17.6, 9.6, 0.9),
        line(poly([(2, 7), (4.5, 7), (6, 3.5), (8, 9.5), (9.5, 7), (12, 7)])),
    ]


@icon("guide-horse", CAT, "Miniature horse in side view wearing a harness with an upright handle",
      tags=["service animal", "blind", "guide animal", "miniature horse", "harness", "mobility"])
def _(S):
    body = [(4, 10), (5.5, 8.5), (13.5, 8.5), (15.5, 5), (15.5, 2.8), (17.5, 4.2), (21, 7.8), (21, 10), (18.5, 10), (17, 11.5), (16.5, 14.5), (16.5, 21), (14.8, 21), (14.8, 15), (7, 15), (7, 21), (5.3, 21), (5.3, 14.5)]
    return [
        shell(poly(body, closed=True, r=S.r), stroke_miterlimit="2"),
        line(poly([(9.5, 8.5), (9.5, 4.5), (12.5, 4.5)], r=S.r)),
        dot(18.3, 6.8, 0.9),
        line(seg(4, 10, 2.5, 14.5)),
    ]


@icon("hippotherapy", CAT, "Horse with a rider seated on a pad and a helper walking beside holding the rider",
      tags=["equine therapy", "horse riding", "rehabilitation", "therapeutic riding", "disability", "sidewalker"])
def _(S):
    def sc(pts):
        return [(8.5 + (x - 3) * 0.78, 6.5 + (y - 2) * 0.78) for x, y in pts]
    horse = [(4, 10), (5.5, 8.5), (13.5, 8.5), (15.5, 5), (15.5, 2.8), (17.5, 4.2), (21, 7.8), (21, 10), (18.5, 10), (17, 11.5), (16.5, 14.5), (16.5, 21), (14.8, 21), (14.8, 15), (7, 15), (7, 21), (5.3, 21), (5.3, 14.5)]
    return [
        shell(poly(sc(horse), closed=True, r=S.r * 0.7), stroke_miterlimit="2"),
        dot(14.2, 6.2, 1.5),
        line(seg(14.2, 8, 14.2, 11)),
        dot(3, 8.5, 1.5),
        line(seg(3, 10.5, 3, 16)),
        line(seg(3, 16, 1.8, 21)), line(seg(3, 16, 4.2, 21)),
        line(seg(3, 12, 10, 11.2)),
    ]


@icon("kneeling-bus", CAT, "Bus in side view lowered at the front door with a ramp unfolding to the curb",
      tags=["low floor bus", "accessible transit", "wheelchair ramp", "public transport", "mobility", "boarding"])
def _(S):
    return [
        shell(rect(2, 3.5, 16, 12, rr(S, 3))),
        detail(seg(5, 7.5, 11, 7.5)),
        detail(rect(13.5, 6, 2.5, 7.5, 0.5)),
        shell(circle(6, 16.5, 2.4)),
        shell(circle(12, 16.5, 2.4)),
        line(seg(18, 15.5, 22.5, 20)),
        line(seg(20, 21.5, 22.5, 21.5)),
    ]


@icon("wheelchair-accessible-train-car", CAT, "Train carriage in side view with a wheelchair space panel beside a wide sliding door",
      tags=["rail", "accessible train", "wheelchair space", "wide door", "public transport", "mobility"])
def _(S):
    return [
        shell(rect(2, 3, 20, 14, rr(S, 3))),
        detail(rect(14, 5.5, 5, 11)),
        dot(7, 6.8, 1),
        detail(poly([(7, 9), (7, 11.5), (10, 11.5), (10.8, 14)])),
        line(seg(5, 19.5, 8, 19.5)), line(seg(16, 19.5, 19, 19.5)),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("driving-hand-controls", CAT, "Steering wheel with a hand lever running down from it toward the pedals",
      tags=["adapted car", "disabled driver", "paraplegic", "accelerator", "brake", "vehicle adaptation"])
def _(S):
    return [
        line(circle(15, 8, 6)),
        dot(15, 8, 1.6),
        line(seg(15, 8, 15, 14)),
        line(seg(15, 8, 10, 6)),
        line(seg(15, 8, 20, 6)),
        solid(circle(7, 13, 2)),
        line(poly([(7, 15), (5, 19)], r=S.r)),
        shell(poly([(3, 19), (12, 19), (12, 21.5), (3, 21.5)], closed=True, r=S.r)),
    ]


@icon("steering-spinner-knob", CAT, "Steering wheel rim with a small round knob mounted on it",
      tags=["steering aid", "one hand driving", "adapted car", "spinner", "disabled driver", "grip"])
def _(S):
    return [
        line(circle(11.5, 12.5, 8.5)),
        shell(circle(11.5, 12.5, 2.2)),
        line(seg(3, 12.5, 9.3, 12.5)),
        line(seg(13.7, 12.5, 20, 12.5)),
        line(seg(11.5, 14.7, 11.5, 21)),
        shell(rect(14, 2.5, 6.5, 6.5, min(S.R, 3.25))),
    ]

