"""TypeIcon Core: music (music batch 004).

Notation marks, signal waves, studio and stage gear, dance and performance scenes, and a few world
instruments. Everything is drawn from the objects themselves and kept to simple shapes.
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, P, ST, U, Part, arc, circle, detail, dot, ellipse, filled_region, icon, line, path_to_d, poly, pt_on, rect,
    regular, seg, shell, solid,
)
from geometry import LINE, fmt, rotation, transform_path

CAT = "music"


def rnd(S, line_val, rounded_val):
    return line_val if S.name == "line" else rounded_val


def nh(cx, cy, rx=2.2, ry=1.6, deg=-20.0):
    """Tilted oval note head as a closed path."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    p1 = (cx - rx * c, cy - rx * s)
    p2 = (cx + rx * c, cy + rx * s)
    return (f"M{fmt(p1[0])} {fmt(p1[1])}A{fmt(rx)} {fmt(ry)} {fmt(deg)} 1 0 {fmt(p2[0])} {fmt(p2[1])}"
            f"A{fmt(rx)} {fmt(ry)} {fmt(deg)} 1 0 {fmt(p1[0])} {fmt(p1[1])}Z")


def cr_path(pts, closed=False):
    """Smooth cubic path through points (Catmull-Rom)."""
    n = len(pts)
    out = [f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"]
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        out.append(f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}")
    if closed:
        out.append("Z")
    return "".join(out)


# ============================================================================ notation

@icon("music-scale", CAT, "Four beamed notes climbing step by step, a rising scale",
      tags=["scale", "notes", "ascending", "do re mi", "practice", "run", "music theory"])
def _(S):
    parts = []
    xs = [4.5, 9, 13.5, 18]
    for i, x in enumerate(xs):
        y = 19.5 - i * 2.6
        parts.append(solid(nh(x, y, 2.3, 1.7, -22)))
        sx = x + 1.9
        by = 9.6 - i * 2.35
        parts.append(line(seg(sx, y - 0.6, sx, by)))
    parts.append(line(seg(6.4, 9.6, 19.9, 2.6)))
    return parts


@icon("music-chord", CAT, "Three note heads stacked on one stem, a chord",
      tags=["chord", "harmony", "notes", "triad", "stacked notes", "music theory", "simultaneous"])
def _(S):
    parts = []
    for y in (19, 14, 9):
        parts.append(solid(nh(9, y, 2.4, 1.8, -22)))
    parts.append(line(seg(11.1, 18.4, 11.1, 3.5)))
    parts.append(line(rnd(S, "M11.1 3.5L17 7.5", "M11.1 3.5Q15.5 4.5 17 8.5")))
    return parts


@icon("double-whole-note", CAT, "Open oval note head with a vertical bar on each side, a breve",
      tags=["breve", "double whole note", "long note", "notation", "rhythm", "note value", "music theory"],
      aliases=["breve-note"])
def _(S):
    return [
        shell(ellipse(12, 12, 5.2, 3.6) if S.name == "rounded" else poly([(6.8, 12), (9.5, 8.4), (14.5, 8.4), (17.2, 12), (14.5, 15.6), (9.5, 15.6)], closed=True, r=0.0)),
        line(seg(3, 7, 3, 17)),
        line(seg(21, 7, 21, 17)),
    ]


@icon("measure-repeat", CAT, "Slanted slash with a dot on each side between two bar lines, repeat the last measure",
      tags=["repeat measure", "simile", "repeat sign", "bar repeat", "notation", "rhythm", "sheet music"])
def _(S):
    return [
        line(seg(3, 4, 3, 20)),
        line(seg(21, 4, 21, 20)),
        solid(poly([(8.8, 17.5), (12.4, 17.5), (15.2, 6.5), (11.6, 6.5)], closed=True)),
        dot(7.3, 8.5, 1.5),
        dot(16.7, 15.5, 1.5),
    ]


@icon("multi-measure-rest", CAT, "Thick horizontal bar between two short end bars, many measures of rest",
      tags=["multirest", "rest", "silence", "bars of rest", "notation", "orchestra part", "sheet music"])
def _(S):
    return [
        line(seg(3, 8, 3, 16)),
        line(seg(21, 8, 21, 16)),
        solid(rect(6.5, 9.5, 11, 5)),
    ]


@icon("chant-notation", CAT, "Four-line staff with square note heads and a clef, plainchant",
      tags=["gregorian chant", "plainchant", "neume", "square notation", "monastic", "church music", "sacred"])
def _(S):
    parts = []
    for y in (4.5, 9.5, 14.5, 19.5):
        parts.append(line(seg(10, y, 22, y)))
    parts.append(line(poly([(6.5, 7), (3, 7), (3, 17), (6.5, 17)], r=S.r * 0.5)))
    for cx, cy in ((13.5, 14.5), (18.5, 9.5)):
        parts.append(solid(rect(cx - 2.4, cy - 2.4, 4.8, 4.8)))
    return parts


# ============================================================================ signals

@icon("square-wave", CAT, "Signal line alternating between a high and a low level with sharp right angles",
      tags=["square wave", "waveform", "oscillator", "synth", "signal", "pulse", "clock"])
def _(S):
    return [line(poly([(2, 16.5), (6, 16.5), (6, 7.5), (12, 7.5), (12, 16.5), (18, 16.5), (18, 7.5), (22, 7.5)], r=S.r))]


@icon("sawtooth-wave", CAT, "Signal line of long rising ramps each ending in a sudden vertical drop",
      tags=["sawtooth", "saw wave", "waveform", "oscillator", "synth", "signal", "ramp"])
def _(S):
    return [line(poly([(2, 17), (8.5, 7), (8.5, 17), (15.5, 7), (15.5, 17), (22, 7)], r=S.r))]


@icon("adsr-envelope", CAT, "Shape that rises sharply, dips to a flat sustain level and slopes back to zero",
      tags=["adsr", "envelope", "attack decay sustain release", "synth", "sound design", "amplitude", "curve"])
def _(S):
    return [shell(poly([(3, 19), (8, 5), (12.5, 11), (17, 11), (21, 19)], closed=True, r=S.r))]


@icon("crossfade", CAT, "Two lines crossing in an X above a horizontal slider, one fading in while one fades out",
      tags=["crossfader", "dj", "fade", "transition", "mix", "blend", "audio editing"])
def _(S):
    return [
        line(seg(3, 3.5, 21, 13)),
        line(seg(3, 13, 21, 3.5)),
        line(seg(3, 19.5, 21, 19.5)),
        shell(rect(9.5, 16.5, 5, 6, min(S.R, 1.5))),
    ]


def _cardioid(cx, cy, a, open_=0.0):
    pts = [(cx, cy + open_)]
    for k in range(1, 12):
        th = math.radians(k * 30)
        r = a * (1 + math.cos(th))
        pts.append((cx + r * math.sin(th), cy - r * math.cos(th)))
    pts.append((cx, cy + open_))
    return pts


@icon("cardioid-pattern", CAT, "Round polar plot with a heart-shaped pickup curve inside it",
      tags=["cardioid", "polar pattern", "microphone pattern", "pickup", "directional", "heart curve", "audio"])
def _(S):
    pts = _cardioid(12, 15.8, 4.4, rnd(S, 0, 0.8))
    return [shell(circle(12, 12, 9.5)), detail(cr_path(pts))]


@icon("spatial-audio", CAT, "Head in front view with sound arcs curving around both sides",
      tags=["surround", "3d audio", "immersive", "head tracking", "binaural", "headphones"])
def _(S):
    return [
        shell(circle(12, 12, 3.4)),
        line(arc(12, 12, 7.2, -42, 42)),
        line(arc(12, 12, 7.2, 138, 222)),
        line(arc(12, 12, 10.6, -42, 42)),
        line(arc(12, 12, 10.6, 138, 222)),
    ]


@icon("music-recognition", CAT, "Phone with a music note on its screen and listening arcs beside it",
      tags=["song identifier", "listen", "what song", "audio fingerprint", "tune id", "detect music"])
def _(S):
    return [
        shell(rect(3, 2.5, 10, 19, rnd(S, 2, 3))),
        solid(nh(7.3, 15.5, 1.9, 1.5, -20)),
        line(seg(9.1, 15, 9.1, 8)),
        line(poly([(9.1, 8), (11.4, 9.6)])),
        line(arc(13.5, 12, 5.2, -48, 48)),
        line(arc(13.5, 12, 9, -48, 48)),
    ]


@icon("pitch-wheel", CAT, "Two tall keyboard wheels side by side, one with a centre notch and one ridged",
      tags=["pitch bend", "mod wheel", "modulation", "synth", "keyboard", "controller", "midi"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 7.5, 19, rnd(S, 2, 3.75))),
        detail(seg(5.5, 12, 9, 12)),
        shell(rect(13, 2.5, 7.5, 19, rnd(S, 2, 3.75))),
        detail(seg(15.3, 8.5, 18.2, 8.5)),
        detail(seg(15.3, 12, 18.2, 12)),
        detail(seg(15.3, 15.5, 18.2, 15.5)),
    ]


@icon("fingering-chart", CAT, "Tube of a woodwind beside a column of open and filled finger holes",
      tags=["fingering", "finger chart", "woodwind", "flute", "recorder", "tutorial", "how to play"])
def _(S):
    return [
        shell(rect(3, 2.5, 6, 19, rnd(S, 1, 3))),
        shell(circle(16, 5, 2)),
        solid(circle(16, 12, 2.5)),
        shell(circle(16, 19, 2)),
    ]


# ============================================================================ helpers for instruments

def rot(pts, deg=45.0, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rp(pts, closed=True, r=0.0, deg=45.0, cx=12.0, cy=12.0):
    return poly(rot(pts, deg, cx, cy), closed=closed, r=r)


def rseg(x1, y1, x2, y2, deg=45.0, cx=12.0, cy=12.0):
    (a, b), (c, d) = rot([(x1, y1), (x2, y2)], deg, cx, cy)
    return seg(a, b, c, d)


def rpt(x, y, deg=45.0, cx=12.0, cy=12.0):
    return rot([(x, y)], deg, cx, cy)[0]


def outline(*ds) -> str:
    return path_to_d(U(*[P(d) for d in ds]))


def cubic_pt(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


# ============================================================================ instruments

def rotd(d, deg=45.0):
    """Rotate a path string about the canvas centre."""
    return path_to_d(transform_path(P(d), rotation(deg, 12, 12)))


@icon("grand-piano", CAT, "Grand piano from the side with a raised lid, a long slab body and two legs",
      tags=["piano", "concert grand", "baby grand", "keys", "pianist", "recital", "keyboard instrument"])
def _(S):
    return [
        shell(rect(2.5, 11, 19, 5, rnd(S, 1.5, 2.5))),
        shell(poly([(7, 10.5), (20.5, 3.5), (20.5, 10.5)], closed=True, r=S.r * 0.5)) if False else
        shell(poly([(7.5, 9), (20, 3.5), (20, 9)], closed=True, r=S.r * 0.5)),
        line(seg(5, 16.5, 5, 21.5)),
        line(seg(19, 16.5, 19, 21.5)),
    ]


@icon("bongo-drums", CAT, "Two small joined hand drums of different sizes standing side by side",
      tags=["bongos", "hand drum", "latin percussion", "conga", "salsa", "rhythm", "percussion"])
def _(S):
    return [
        shell("M2.8 8L4.5 20H9.5L11 8"),
        shell("M11.4 7L13 20H19.5L20.6 7"),
        shell(ellipse(6.9, 8, 4.1, 1.8)),
        shell(ellipse(16, 7, 4.6, 2)),
    ]


@icon("darbuka", CAT, "Goblet-shaped hand drum with a wide head, a narrow waist and a flared open foot",
      tags=["doumbek", "goblet drum", "middle eastern drum", "belly dance", "tarabuka", "percussion", "hand drum"],
      aliases=["doumbek"])
def _(S):
    foot = "L10 17L7.5 21H16.5L14 17" if S.name == "line" else "V17C14 17 16 19 16.5 21H7.5C8 19 10 17 10 17V14"
    body = "M5 5C5 10 10 10 10 14" + ("V17L7.5 21H16.5L14 17V14" if S.name == "line" else "V17C10 17 8 19 7.5 21H16.5C16 19 14 17 14 17V14") + "C14 10 19 10 19 5Z"
    return [shell(body), detail(ellipse(12, 5, 7, 2)), detail(seg(9.4, 18.5, 14.6, 18.5))]


@icon("timbales", CAT, "Two open metal drums on a stand with a small cowbell mounted between them",
      tags=["timbal", "latin percussion", "salsa", "cowbell", "drum", "stand", "percussion"])
def _(S):
    def drum(cx):
        return [shell(f"M{fmt(cx - 3.5)} 10V14A3.5 1.5 0 0 0 {fmt(cx + 3.5)} 14V10"),
                shell(ellipse(cx, 10, 3.5, 1.5))]
    return drum(5.5) + drum(18.5) + [
        shell(poly([(10.5, 3.5), (13.5, 3.5), (14.5, 9), (9.5, 9)], closed=True, r=S.r * 0.3)),
        line(seg(12, 9.5, 12, 17)),
        line(poly([(6, 21), (12, 16.5), (18, 21)])),
    ]


@icon("caxixi", CAT, "Small woven basket rattle with a flat round base and a loop handle on top",
      tags=["shaker", "rattle", "basket", "brazilian percussion", "berimbau", "handle", "rhythm"])
def _(S):
    return [
        shell(poly([(4, 20.5), (7.5, 11), (16.5, 11), (20, 20.5)], closed=True, r=S.r)),
        detail(seg(6.2, 16, 17.8, 16)),
        detail(seg(12, 11.5, 12, 20)),
        line("M9 11C9 5 15 5 15 11"),
    ]


@icon("oud", CAT, "Oud: deep pear-shaped body with three sound holes and a short neck bent back at the pegbox",
      tags=["arabic lute", "middle eastern", "string instrument", "fretless", "lute", "maqam", "instrument"],
      aliases=["ud"])
def _(S):
    body = outline(ellipse(12, 16.2, 6, 5.6), rect(10.5, 8, 3, 8))
    return [
        shell(rotd(body)),
        dot(*rpt(12, 14.2), 1.1),
        dot(*rpt(9.3, 17.6), 1.1),
        dot(*rpt(14.7, 17.6), 1.1),
        line(rotd("M12 8.5V4.5L15.5 3")),
    ]


@icon("veena", CAT, "Veena: long horizontal neck with a large round bowl at one end and a smaller gourd under the other",
      tags=["vina", "saraswati", "indian classical", "carnatic", "string instrument", "gourd", "raga"],
      aliases=["vina"])
def _(S):
    return [
        shell(circle(6.6, 17.4, 4.6)),
        line(seg(10, 14, 21, 3)),
        shell(circle(16.6, 12.2, 2.5)),
        detail(seg(5, 17.4, 8.2, 17.4)) if False else dot(6.6, 17.4, 1.2),
    ]


@icon("kantele", CAT, "Kantele from above: a wing-shaped wooden box with strings fanning from the narrow end to the wide end",
      tags=["finnish zither", "plucked strings", "folk", "nordic", "harp zither", "string instrument", "kalevala"])
def _(S):
    top = lambda x: 5 - 2 * (x - 3) / 18
    bot = lambda x: 12 + 8 * (x - 3) / 18
    parts = [shell(poly([(3, 5), (21, 3), (21, 20), (3, 12)], closed=True, r=S.r))]
    for f in (0.3, 0.5, 0.7):
        y1 = top(8) + (bot(8) - top(8)) * f
        y2 = top(18) + (bot(18) - top(18)) * f
        parts.append(detail(seg(8, y1, 18, y2)))
    return parts


@icon("moon-guitar", CAT, "Moon guitar: a perfectly round flat body with a short fretted neck and four tuning pegs",
      tags=["yueqin", "chinese guitar", "round body", "string instrument", "folk", "peking opera", "lute"],
      aliases=["yueqin"])
def _(S):
    body = outline(circle(12, 16, 6), rect(10.5, 7, 3, 8), rect(10, 2, 4, 6))
    parts = [shell(rotd(body)), dot(*rpt(12, 16), 1.6)]
    for y in (3.6, 6.4):
        parts.append(line(rotd(seg(7.6, y, 10, y))))
        parts.append(line(rotd(seg(14, y, 16.4, y))))
    return parts


@icon("arched-harp", CAT, "Arched harp: a boat-shaped body with one long neck arching up over the strings",
      tags=["ancient harp", "egyptian harp", "burmese harp", "saung", "string instrument", "strings", "lyre"])
def _(S):
    p0, p1, p2, p3 = (20, 16.5), (20, 6), (14, 2.5), (5, 3.5)
    parts = [shell("M3 16.5H21C20 19.5 17 21.5 12 21.5C7 21.5 4 19.5 3 16.5Z"),
             line(f"M{p0[0]} {p0[1]}C{p1[0]} {p1[1]} {p2[0]} {p2[1]} {p3[0]} {p3[1]}")]
    for x in (8, 11.5, 15, 18.3):
        lo, hi = 0.0, 1.0
        for _ in range(40):
            mid = (lo + hi) / 2
            if cubic_pt(p0, p1, p2, p3, mid)[0] > x:
                lo = mid
            else:
                hi = mid
        y = cubic_pt(p0, p1, p2, p3, (lo + hi) / 2)[1]
        parts.append(line(seg(x, y + 1, x, 16.5)))
    return parts


@icon("aulos", CAT, "Aulos: a pair of long reed pipes joined at the mouthpiece and spreading apart in a V",
      tags=["double flute", "ancient greek", "double pipe", "reed pipes", "wind instrument", "antiquity", "diaulos"])
def _(S):
    parts = []
    for sgn in (-1, 1):
        pipe = rp([(9.5, 3), (14.5, 3), (13.3, 20.5), (10.7, 20.5)], deg=sgn * 15, cx=12, cy=21)
        parts.append(shell(pipe))
        for y in (8, 12.5, 17):
            cx, cy = rpt(12, y, deg=sgn * 15, cx=12, cy=21)
            parts.append(dot(cx, cy, 0.9))
    return parts


@icon("khene", CAT, "Khene: a row of long bamboo pipes of equal length fixed through a small wind chest near the bottom",
      tags=["laos", "thai", "mouth organ", "bamboo", "free reed", "southeast asian", "folk instrument"],
      aliases=["khaen"])
def _(S):
    parts = [shell(rect(2.5, 14, 19, 4.5, min(S.R, 2)))]
    for x in (5, 9, 13, 17, 21):
        if x < 21:
            parts.append(line(seg(x, 2.5, x, 14)))
    parts.append(line(seg(19.5, 2.5, 19.5, 14)) if False else line(seg(12, 18.5, 12, 21.5)))
    return parts


@icon("fanfare-trumpet", CAT, "Long straight herald trumpet with a flared bell and a square banner hanging from the tube",
      tags=["herald trumpet", "fanfare", "royal", "announcement", "ceremony", "brass", "medieval"])
def _(S):
    return [
        line(seg(2.5, 7.5, 15.5, 7.5)),
        shell(poly([(15, 6.5), (21.5, 3.5), (21.5, 11.5), (15, 8.5)], closed=True, r=S.r * 0.6)),
        shell(rect(5.5, 10.5, 9, 10, min(S.R, 1.5))),
        detail(seg(7.5, 15.5, 12.5, 15.5)),
    ]


@icon("ear-trumpet", CAT, "Antique hearing horn: a curved cone with a wide flared mouth and a narrow earpiece",
      tags=["hearing horn", "hearing aid", "antique", "deaf", "listening", "old fashioned", "acoustic"],
      aliases=["hearing-horn"])
def _(S):
    body = ("M13.5 3.5L20.5 10.5C18 15 13 17.5 9.5 18.5C7.5 19 6 19.5 4 21L3.5 19.5"
            "C4 17 6 14.5 8.5 12.5C10.5 10.5 12.5 8 13.5 3.5Z")
    return [shell(body), detail(nh(17, 7, 5, 1.8, 45))]


@icon("temple-bell", CAT, "Large bronze bell hanging from a small roof frame on two posts",
      tags=["pagoda bell", "buddhist", "shrine", "gong", "bronze bell", "meditation", "asian temple"])
def _(S):
    return [
        line(poly([(2, 8), (12, 3), (22, 8)], r=S.r)),
        line(seg(4, 8.5, 4, 21)),
        line(seg(20, 8.5, 20, 21)),
        line(seg(12, 5, 12, 8.5)),
        shell("M10 8.5L9 13C9 16 7.5 17 7.5 18.5H16.5C16.5 17 15 16 15 13L14 8.5Z"),
    ]


@icon("clash-cymbals", CAT, "Pair of large round cymbals touching, each with a raised bell, and clash marks above",
      tags=["cymbals", "crash", "marching band", "orchestra", "percussion", "clap", "hand cymbals"],
      aliases=["hand-cymbals"])
def _(S):
    return [
        shell(circle(6, 15.5, 5)),
        shell(circle(18, 15.5, 5)),
        dot(6, 15.5, 1.3),
        dot(18, 15.5, 1.3),
        line(seg(12, 7, 12, 3)),
        line(seg(8.5, 7, 7, 3.5)),
        line(seg(15.5, 7, 17, 3.5)),
    ]


@icon("spring-drum", CAT, "Short tube drum with a long coiled spring hanging down from its head",
      tags=["thunder drum", "spring reverb", "thunder sound", "theatre effect", "percussion", "coil", "sound effect"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 6, min(S.R, 2))),
        line(poly([(12, 9), (16.5, 11.3), (7.5, 14), (16.5, 16.6), (7.5, 19), (12, 21.5)])),
    ]


# ============================================================================ studio and stage gear

@icon("guitar-headstock", CAT, "Guitar headstock from the front with three tuning pegs on each side and a string running down",
      tags=["tuning pegs", "machine heads", "tuners", "restring", "guitar neck", "nut", "tuning"])
def _(S):
    parts = [
        shell(poly([(8.5, 3), (15.5, 3), (15.5, 13), (13.5, 16.5), (10.5, 16.5), (8.5, 13)], closed=True, r=S.r)),
        line(seg(10.5, 17, 10.5, 21.5)),
        line(seg(13.5, 17, 13.5, 21.5)),
        detail(seg(12, 6, 12, 13)),
    ]
    for y in (4.5, 8.5, 12.5):
        parts.append(line(seg(5.5, y, 8.5, y)))
        parts.append(dot(3.8, y, 1.5))
        parts.append(line(seg(15.5, y, 18.5, y)))
        parts.append(dot(20.2, y, 1.5))
    return parts


@icon("violin-scroll", CAT, "Violin head close up: a spiral scroll on top of the pegbox with four tuning pegs",
      tags=["violin head", "scroll", "pegbox", "fiddle", "viola", "luthier", "string instrument"])
def _(S):
    parts = [
        shell(circle(12, 5.8, 3.4)),
        shell(rect(9.5, 10, 5, 8, rnd(S, 0.5, 1.5))),
        line(seg(12, 18.5, 12, 22)),
        dot(12, 5.8, 1.0),
    ]
    for y, side in ((12.2, -1), (13.6, 1), (16.2, -1), (17.4, 1)):
        x0 = 9.5 if side < 0 else 14.5
        parts.append(line(seg(x0, y, x0 + side * 3.5, y)))
        parts.append(dot(x0 + side * 4.6, y, 1.3))
    return parts


@icon("pedalboard", CAT, "Flat board carrying a row of three stomp box pedals with footswitches",
      tags=["pedal board", "guitar effects", "stompbox", "effects chain", "guitarist", "rig", "footswitch"])
def _(S):
    parts = [shell(rect(2, 16.5, 20, 5, rnd(S, 1.5, 2.5)))]
    for cx in (5, 12, 19):
        parts.append(shell(rect(cx - 2.6, 3.5, 5.2, 11.5, rnd(S, 1.5, 2.5))))
        parts.append(dot(cx, 6.8, 0.9))
        parts.append(dot(cx, 11.6, 1.1))
    return parts


@icon("patch-bay", CAT, "Rack panel with two rows of jack sockets and a patch cable looping between two of them",
      tags=["patchbay", "jacks", "routing", "rack", "cables", "studio wiring", "audio patch"])
def _(S):
    parts = [shell(rect(2, 3, 20, 10.5, rnd(S, 2, 3)))]
    for x in (6, 10, 14, 18):
        parts.append(dot(x, 6.4, 1.2))
        parts.append(dot(x, 10.2, 1.2))
    parts.append(line("M6 10.2V15.5C6 20 14 20 14 15.5V10.2"))
    return parts


@icon("flight-case", CAT, "Road case with a carry handle, a lid seam, two latches and metal corner trim",
      tags=["road case", "rack case", "equipment case", "touring", "roadie", "gear", "transport"])
def _(S):
    return [
        shell(rect(2.5, 7, 19, 14, rnd(S, 1.5, 3))),
        detail(seg(2.5, 12, 21.5, 12)),
        solid(rect(5, 10.5, 3.5, 4.5)),
        solid(rect(15.5, 10.5, 3.5, 4.5)),
        line(poly([(9.5, 7), (9.5, 3.5), (14.5, 3.5), (14.5, 7)], r=S.r)),
    ]


@icon("cd-case", CAT, "Square jewel case with a hinge strip on the left and a disc visible through the front",
      tags=["jewel case", "compact disc", "album", "cd", "audio disc", "music collection", "sleeve"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rnd(S, 1.5, 3))),
        detail(seg(7, 3, 7, 21)),
        detail(circle(14, 12, 4.6)),
        dot(14, 12, 1.0),
    ]


@icon("horn-speaker", CAT, "Flared horn loudspeaker on a short pole with sound arcs leaving its mouth",
      tags=["horn loudspeaker", "pa horn", "public address", "megaphone speaker", "outdoor speaker", "announce"])
def _(S):
    return [
        shell(rect(2.5, 9, 4, 6, rnd(S, 0.5, 1.5))),
        shell(poly([(6.5, 9.5), (14, 5), (14, 19), (6.5, 14.5)], closed=True, r=S.r * 0.6)),
        line(seg(10, 17, 10, 21.5)),
        line(arc(14.5, 12, 3.6, -45, 45)),
        line(arc(14.5, 12, 7, -45, 45)),
    ]


@icon("wireless-microphone", CAT, "Handheld microphone with a round grille and a short antenna at the base, with signal arcs",
      tags=["cordless mic", "radio mic", "handheld mic", "karaoke", "stage", "presenter", "no cable"])
def _(S):
    return [
        shell(circle(9.5, 7.5, 4.4)),
        detail(seg(6, 7.5, 13, 7.5)),
        shell(poly([(7.6, 12), (11.4, 12), (10.8, 19), (8.2, 19)], closed=True, r=S.r * 0.5)),
        line(seg(9.5, 19.5, 9.5, 22)),
        line(arc(9.5, 7.5, 7.8, -32, 32)),
        line(arc(9.5, 7.5, 11, -32, 32)),
    ]


@icon("bodypack-transmitter", CAT, "Small transmitter box with a stubby antenna, a belt clip at the side and a cable leaving the front",
      tags=["belt pack", "wireless pack", "lavalier transmitter", "headset mic", "stage", "presenter", "radio pack"])
def _(S):
    return [
        shell(rect(7, 8, 10, 13, rnd(S, 1.5, 3))),
        line(seg(14, 8, 14, 3)),
        detail(seg(9.5, 12, 14.5, 12)),
        dot(12, 17, 1.1),
        line(poly([(17, 11), (20.5, 11), (20.5, 18)], r=S.r)),
        line(poly([(7, 18.5), (3, 18.5), (3, 10.5)], r=S.r)),
    ]


@icon("binaural-microphone", CAT, "Dummy head and neck in profile with a microphone capsule set in the ear",
      tags=["dummy head", "3d audio recording", "asmr", "stereo head", "ear mic", "spatial recording", "binaural"])
def _(S):
    head = outline(circle(12.5, 9.5, 6.5), poly([(6.6, 8.5), (3.4, 12.6), (7, 13.2)], closed=True), rect(10, 14, 5, 7))
    return [shell(head), dot(14.6, 10, 1.8)]


@icon("parabolic-microphone", CAT, "Bowl-shaped dish reflector with a microphone on a stick at its focus and a pistol grip below",
      tags=["parabolic dish mic", "bird recording", "sports microphone", "nature recording", "eavesdrop", "field recording", "reflector"])
def _(S):
    return [
        shell("M10 2.5C1.5 6.5 1.5 15.5 10 19.5Z"),
        line(seg(5.2, 11, 15, 11)),
        shell(rect(15, 9, 6.5, 4, rnd(S, 1, 2))),
        shell(rect(13, 14.5, 3.4, 7, rnd(S, 1, 1.7))),
    ]


@icon("recording-studio", CAT, "Mixing desk in front of a glass window with a microphone standing in the booth behind it",
      tags=["studio", "control room", "mixing desk", "vocal booth", "sound engineer", "record label", "session"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 10, rnd(S, 1.5, 3))),
        dot(12, 6.3, 1.9),
        line(seg(12, 8.3, 12, 11)),
        shell(poly([(2.5, 21.5), (21.5, 21.5), (19.5, 15.5), (4.5, 15.5)], closed=True, r=S.r * 0.5)),
        dot(8, 18.6, 0.9),
        dot(12, 18.6, 0.9),
        dot(16, 18.6, 0.9),
    ]


@icon("audio-guide", CAT, "Handheld audio player with a speaker slot, a number keypad and a lanyard loop",
      tags=["museum guide", "tour guide device", "audio tour", "headset guide", "visitor guide", "number keypad", "gallery"])
def _(S):
    parts = [
        shell(rect(6.5, 6, 11, 16, rnd(S, 2, 3.5))),
        detail(seg(9.5, 9.5, 14.5, 9.5)),
        line("M10 6C10 1.5 14 1.5 14 6"),
    ]
    for y in (14, 18):
        for x in (9.5, 12, 14.5):
            parts.append(dot(x, y, 0.9))
    return parts


@icon("stage-truss", CAT, "Triangular lattice truss beam across the top with two stage lights hanging below it",
      tags=["lighting rig", "truss", "concert lighting", "stage lights", "spotlights", "gantry", "theatre"])
def _(S):
    parts = [
        line(seg(2, 3.5, 22, 3.5)),
        line(seg(2, 8.5, 22, 8.5)),
        line(poly([(2, 8.5), (5.5, 3.5), (9, 8.5), (12.5, 3.5), (16, 8.5), (19.5, 3.5), (22, 8.5)])),
    ]
    for cx in (7, 17):
        parts.append(line(seg(cx, 9, cx, 12)))
        parts.append(shell(poly([(cx - 2, 12), (cx + 2, 12), (cx + 3.6, 19), (cx - 3.6, 19)], closed=True, r=S.r * 0.6)))
    return parts


def _star(cx, cy, ro, ri, n=4, start=-90.0):
    pts = []
    for i in range(n * 2):
        r = ro if i % 2 == 0 else ri
        a = math.radians(start + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


@icon("strobe-light", CAT, "Box light with a flat lamp face and a sharp four-point starburst flashing above it",
      tags=["strobe", "flash", "club lighting", "disco lights", "stage effect", "flashing light", "rave"])
def _(S):
    return [
        solid(poly(_star(12, 6.2, 5.6, 1.4), closed=True)),
        shell(rect(3, 13.5, 18, 8, rnd(S, 1.5, 3))),
        detail(seg(8, 16.5, 8, 18.5)),
        detail(seg(12, 16.5, 12, 18.5)),
        detail(seg(16, 16.5, 16, 18.5)),
    ]


@icon("laser-show", CAT, "Five thin straight beams fanning upward from a small projector at the bottom",
      tags=["laser lights", "laser beams", "light show", "concert lasers", "rave", "projector", "nightclub"])
def _(S):
    parts = [shell(rect(9, 18.5, 6, 3.3, rnd(S, 0.5, 1.6)))]
    for a in (-90, -112, -68, -134, -46):
        x0, y0 = pt_on(12, 18.5, 4.5, a)
        x1, y1 = pt_on(12, 18.5, 15.5, a)
        parts.append(line(seg(x0, y0, x1, y1)))
    return parts


@icon("concert-program", CAT, "Folded booklet with a music note and two lines of text on the cover",
      tags=["programme", "playbill", "setlist booklet", "recital program", "event leaflet", "theatre", "brochure"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rnd(S, 1.5, 3))),
        solid(nh(10.4, 11, 1.9, 1.4, -20)),
        line(seg(12.2, 10.6, 12.2, 5.6)),
        line("M12.2 5.6Q14.6 5.8 14.6 8.6"),
        detail(seg(8.5, 15.3, 15.5, 15.3)),
        detail(seg(8.5, 18.3, 12.5, 18.3)),
    ]


@icon("twirling-baton", CAT, "Long rod with a rubber ball at each end and curved motion arcs showing it spinning",
      tags=["baton twirling", "majorette", "marching", "parade", "drum major", "spin", "color guard"])
def _(S):
    return [
        line(seg(7.6, 16.4, 16.4, 7.6)),
        shell(circle(5.6, 18.4, 2.6)),
        shell(circle(18.4, 5.6, 2.6)),
        line(arc(12, 12, 10, 5, 40)),
        line(arc(12, 12, 10, 185, 220)),
    ]


# ============================================================================ more instruments

@icon("electric-organ", CAT, "Home organ: two stacked keyboards on a cabinet with a row of drawbars above and a pedal below",
      tags=["organ", "home organ", "combo organ", "drawbars", "keyboard", "church", "lounge"])
def _(S):
    parts = [
        shell(rect(2.5, 7, 19, 10, rnd(S, 1.5, 3))),
        detail(seg(2.5, 12, 21.5, 12)),
        line(seg(5, 17.5, 5, 21.5)),
        line(seg(19, 17.5, 19, 21.5)),
    ]
    for x in (6, 10, 14, 18):
        parts.append(line(seg(x, 2.5, x, 5)))
    return parts


@icon("pedal-steel-guitar", CAT, "Pedal steel guitar: a long flat body on four legs with floor pedals and a steel bar resting on the strings",
      tags=["steel guitar", "country music", "nashville", "slide", "lap steel", "twang", "pedals"])
def _(S):
    return [
        shell(rect(2.5, 6.5, 19, 7, rnd(S, 1.5, 3))),
        detail(seg(5, 10, 19, 10)),
        solid(rect(14.5, 2.8, 5, 2.4)),
        line(seg(5, 14, 5, 21.5)),
        line(seg(19, 14, 19, 21.5)),
        line(seg(9.5, 14, 9.5, 18)),
        line(seg(14.5, 14, 14.5, 18)),
        dot(9.5, 20, 1.3),
        dot(14.5, 20, 1.3),
    ]


@icon("marching-tenor-drums", CAT, "Top view of a curved cluster of four round drums with two small drums between them",
      tags=["tenor drums", "quad drums", "drumline", "marching band", "snare", "parade", "percussion"],
      aliases=["quads-drums"])
def _(S):
    return [
        shell(circle(4.8, 16.5, 2.9)),
        shell(circle(8.6, 8.6, 2.9)),
        shell(circle(15.4, 8.6, 2.9)),
        shell(circle(19.2, 16.5, 2.9)),
        dot(10.3, 18, 1.5) if S.name == "rounded" else Part("dot", rect(8.8, 16.5, 3, 3)),
        dot(13.7, 18, 1.5) if S.name == "rounded" else Part("dot", rect(12.2, 16.5, 3, 3)),
    ]


@icon("chimta", CAT, "Long flat fire tongs joined at the top with small jingles along both arms",
      tags=["punjabi tongs", "folk percussion", "jingles", "bhangra", "sikh", "tongs", "indian instrument"])
def _(S):
    parts = [
        shell(circle(12, 3.8, 1.7)),
        line(seg(12, 5.5, 8.6, 21.5)),
        line(seg(12, 5.5, 15.4, 21.5)),
    ]
    for y in (10, 14.5, 19):
        t = (y - 5.5) / 16
        lx, rx = 12 - 3.4 * t, 12 + 3.4 * t
        parts.append(dot(lx - 3.4, y, 1.4))
        parts.append(dot(rx + 3.4, y, 1.4))
    return parts


@icon("musical-spoons", CAT, "Two spoons held back to back with their handles together, with clack marks above",
      tags=["spoons", "folk percussion", "clacking", "bones", "irish music", "rhythm", "cutlery"])
def _(S):
    return [
        shell(nh(7, 8, 4.6, 3.3, 79)),
        shell(nh(17, 8, 4.6, 3.3, 101)),
        line(seg(8.7, 12.5, 11.4, 21.5)),
        line(seg(15.3, 12.5, 12.6, 21.5)),
        line(seg(12, 3, 12, 5.5)),
    ]


@icon("ratchet-noisemaker", CAT, "Handle with a cogwheel and a wooden flap that clacks around it, with motion arcs",
      tags=["rattle", "gragger", "noisemaker", "football rattle", "party", "purim", "clacker"])
def _(S):
    parts = [
        shell(rect(10.5, 15, 3, 7, rnd(S, 1, 1.5))),
        shell(circle(12, 11, 3.6)),
        shell(poly([(13.8, 7.2), (19.5, 1.8), (21.6, 3.9), (15.9, 9.3)], closed=True, r=S.r * 0.4)),
        line(arc(12, 11, 8, 170, 240)),
    ]
    return parts


@icon("flexatone", CAT, "Flexatone: a flexible steel sheet in a frame on a handle with two small ball beaters on springs",
      tags=["flex-a-tone", "wobble", "sound effect", "percussion", "orchestra", "eerie", "spring beaters"])
def _(S):
    return [
        shell(poly([(5, 2.5), (19, 2.5), (17.5, 12.5), (6.5, 12.5)], closed=True, r=S.r)),
        shell(rect(10.5, 12.5, 3, 9, rnd(S, 1, 1.5))),
        line(seg(6.5, 11.5, 3.6, 17)),
        dot(3.1, 18.6, 1.6),
        line(seg(17.5, 11.5, 20.4, 17)),
        dot(20.9, 18.6, 1.6),
    ]


@icon("frog-guiro", CAT, "Carved wooden frog with a ridged back and a scraper stick resting across the ridges",
      tags=["guiro", "wooden frog", "scraper", "percussion", "ribbit sound", "thai instrument", "rasp"])
def _(S):
    body = outline(ellipse(13.5, 15, 8, 4.4), circle(5.3, 13.4, 3.1))
    return [
        shell(body),
        dot(5.2, 12.6, 0.9),
        detail(seg(11, 11.3, 11, 13.3)),
        detail(seg(15, 11.3, 15, 13.3)),
        detail(seg(19, 12.5, 19, 14.3)),
        line(seg(8.5, 4.5, 21, 10)),
        line(seg(7.5, 18, 6.5, 21.5)),
        line(seg(17, 18.5, 20.5, 21.5)),
    ]


@icon("bird-whistle", CAT, "Small ceramic bird whistle with a mouthpiece tail and water wave lines inside the body",
      tags=["water whistle", "clay whistle", "bird call", "warbler", "ceramic", "toy", "chirp"])
def _(S):
    body = outline(ellipse(11.5, 14, 7, 5), circle(17, 8.6, 3.3),
                   poly([(19.7, 7.4), (22, 9.2), (19.8, 10.6)], closed=True),
                   poly([(6, 12), (3, 6.2), (5.4, 5), (8.4, 10.6)], closed=True))
    return [
        shell(body),
        detail("M8 15q1.6-1.8 3.2 0t3.2 0"),
        dot(17.6, 8.2, 0.9),
    ]


# ============================================================================ dance and performance

def head(x, y, r=2.2):
    return dot(x, y, r)


def mark(d):
    return Part("dot", d)


@icon("tango-dance", CAT, "Couple in a deep dip: one partner stands and the other leans far back in their arms",
      tags=["tango", "ballroom", "couple dance", "dip", "partner dance", "dance couple", "argentine"])
def _(S):
    return [
        head(6.5, 3.8),
        line(seg(6.5, 7, 7.5, 13.5)),
        line(poly([(7.5, 13.5), (5, 21.5)])),
        line(poly([(7.5, 13.5), (11.5, 17.5), (11, 21.5)], r=S.r)),
        line(poly([(6.8, 9), (12.5, 11.5)], r=0)),
        head(19, 15.5),
        line("M12.5 10.8Q18.2 10.2 18.6 13"),
        line(poly([(12.5, 10.8), (16.8, 5.6), (20.6, 6.4)], r=S.r)),
    ]


@icon("circle-dance", CAT, "Ring of six dancers seen from above, holding hands in a circle",
      tags=["round dance", "folk dance", "hora", "ring dance", "holding hands", "community dance", "celebration"])
def _(S):
    parts = []
    for k in range(6):
        a = -90 + k * 60
        x, y = pt_on(12, 12, 7.6, a)
        parts.append(dot(x, y, 2.2))
        parts.append(line(arc(12, 12, 7.6, a + 20, a + 40)))
    return parts


@icon("sufi-whirling", CAT, "Whirling dancer in a tall hat and a wide bell skirt, one palm raised and one lowered",
      tags=["whirling dervish", "sema", "mevlevi", "spinning", "turkish dance", "sufism", "rumi"])
def _(S):
    return [
        shell(poly([(10.4, 2), (13.6, 2), (13.2, 6.5), (10.8, 6.5)], closed=True, r=S.r * 0.3)),
        head(12, 8.6, 1.6),
        line(seg(12, 10, 12, 12.6)),
        line(seg(12, 11, 18.5, 6.5)),
        line(seg(12, 11, 5.5, 14.5)),
        shell("M10.5 12.6C9.5 16 5.5 17 3 19.8C8 22.8 16 22.8 21 19.8C18.5 17 14.5 16 13.5 12.6Z"),
    ]


@icon("limbo-dance", CAT, "Dancer bent far backward to pass under a low horizontal bar held on two poles",
      tags=["limbo", "how low can you go", "caribbean", "party game", "luau", "bar", "bend back"])
def _(S):
    return [
        line(seg(2.5, 7, 21.5, 7)),
        line(seg(3, 7, 3, 21.5)),
        line(seg(21, 7, 21, 21.5)),
        head(7.2, 14.6),
        line("M15.5 14.5Q11 13 9.6 13.6"),
        line(poly([(15.5, 14.5), (18, 18), (16.6, 21.5)], r=S.r)),
        line(poly([(15.5, 14.5), (16.2, 18), (14, 21.5)], r=S.r)) if False else line(poly([(15.5, 14.5), (14.4, 18), (12.5, 21.5)], r=S.r)),
    ]


@icon("line-dancing", CAT, "Row of three dancers in cowboy hats standing side by side",
      tags=["country dance", "western dance", "barn dance", "cowboy hat", "group dance", "boot scootin", "honky tonk"])
def _(S):
    parts = []
    for x in (5, 12, 19):
        parts += [
            line(seg(x - 2.6, 5.4, x + 2.6, 5.4)),
            solid(rect(x - 1.3, 2.6, 2.6, 2)),
            head(x, 8.4, 1.8),
            line(seg(x, 10.5, x, 15.8)),
            line(seg(x, 11.6, x - 2.4, 14.6)),
            line(seg(x, 11.6, x + 2.4, 14.6)),
            line(seg(x, 15.8, x - 1.6, 21.5)),
            line(seg(x, 15.8, x + 1.6, 21.5)),
        ]
    return parts


@icon("crowd-surfing", CAT, "Person lying flat on a row of raised hands, carried over a crowd",
      tags=["crowd surf", "mosh pit", "concert crowd", "rock show", "festival", "stage dive", "audience"])
def _(S):
    parts = [
        head(19.5, 6.5, 2.3),
        shell(rect(2.5, 4.6, 14.5, 5.8, rnd(S, 2, 2.9))),
    ]
    for x0, x1 in ((3, 5), (8, 9.3), (13.3, 13), (19, 16.5)):
        parts.append(line(seg(x0, 21.5, x1, 13.6)))
    return parts


@icon("music-band", CAT, "Three band members side by side, one with a guitar, one with a microphone and one with drumsticks",
      tags=["band", "group", "rock band", "trio", "musicians", "gig", "live music"])
def _(S):
    parts = []
    for x in (4.5, 12, 19.5):
        parts += [
            head(x, 4.6, 2),
            line(seg(x, 7.4, x, 14.5)),
            line(seg(x, 14.5, x - 2, 21.5)),
            line(seg(x, 14.5, x + 2, 21.5)),
        ]
    parts += [
        line(seg(1.8, 19, 8, 11.5)),
        shell(circle(3.6, 17.2, 1.8)) if False else dot(3.4, 17.4, 2),
        line(seg(12, 9.5, 15.5, 7.2)),
        dot(16.4, 6.6, 1.3),
        line(seg(19.5, 10, 17.3, 8)),
        line(seg(19.5, 10, 22, 8.3)),
    ]
    return parts


@icon("orchestra", CAT, "Fan of seated musicians in two curved rows around a conductor at the front",
      tags=["symphony", "ensemble", "philharmonic", "concert hall", "musicians", "classical", "conductor"])
def _(S):
    parts = [head(12, 17, 2.3), line(seg(12, 19.6, 12, 22))]
    for a in (215, 245, 295, 325):
        x, y = pt_on(12, 21, 6.6, a)
        parts.append(dot(x, y, 1.5))
    for a in (205, 225, 245, 270, 295, 315, 335):
        x, y = pt_on(12, 21, 11, a)
        parts.append(dot(x, y, 1.5))
    return parts


@icon("mic-drop", CAT, "Microphone tipped upside down and falling, with speed lines above it",
      tags=["drop the mic", "mic fall", "boom", "finale", "performance end", "rapper", "stand up comedy"])
def _(S):
    return [
        line(seg(7, 2.5, 7, 6)),
        line(seg(12, 2, 12, 6)),
        line(seg(17, 2.5, 17, 6)),
        line(seg(12, 9.5, 12, 14)),
        shell(poly([(10.2, 9.5), (13.8, 9.5), (13.2, 15), (10.8, 15)], closed=True, r=S.r * 0.5)),
        shell(circle(12, 18.8, 3)),
        detail(seg(9.8, 18.8, 14.2, 18.8)) if False else dot(12, 18.8, 0.9),
    ]


@icon("maypole", CAT, "Tall pole topped with a garland and ribbons spiralling down to the ground",
      tags=["may day", "ribbon dance", "spring festival", "folk tradition", "village green", "english folk", "celebration"])
def _(S):
    return [
        line(seg(12, 5, 12, 21.5)),
        dot(12, 3.6, 2),
        line("M12 6Q2 12 3.5 21.5"),
        line("M12 6Q22 12 20.5 21.5"),
        line("M12 6Q6.5 13 8 21.5") if False else line("M12 9Q7 14 7.4 21.5"),
        line("M12 9Q17 14 16.6 21.5"),
    ]


@icon("disco-ball", CAT, "Mirror ball covered in square facets hanging from a short chain with two sparkles",
      tags=["mirror ball", "glitter ball", "party", "nightclub", "dance floor", "70s", "reflective"])
def _(S):
    return [
        line(seg(11, 2.5, 11, 6)),
        shell(circle(11, 14, 7.5)),
        detail(seg(3.5, 14, 18.5, 14)),
        detail(ellipse(11, 14, 3.6, 7.5)),
        solid(poly(_star(19.6, 4.6, 2.8, 0.8), closed=True)),
    ]


@icon("dance-floor", CAT, "Checkered dance floor seen in perspective with two tiles lit up",
      tags=["lit floor", "tiles", "nightclub", "disco floor", "party", "light up floor", "saturday night"])
def _(S):
    return [
        shell(poly([(6, 5), (18, 5), (22, 20), (2, 20)], closed=True, r=S.r * 0.5)),
        detail(seg(12, 5, 12, 20)),
        detail(seg(4, 12.5, 20, 12.5)) if False else detail(seg(3.9, 12.5, 20.1, 12.5)),
        mark(poly([(8, 6.8), (10.4, 6.8), (10.4, 10.8), (6.8, 10.8)], closed=True)),
        mark(poly([(13.6, 14.4), (18.6, 14.4), (19.3, 18.2), (13.6, 18.2)], closed=True)),
    ]


def _foot(cx, cy, deg):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)

    def rp_(x, y):
        return (cx + x * ca - y * sa, cy + x * sa + y * ca)
    sole = rp_(0, -1.2)
    heel = rp_(0, 3.4)
    return [solid(nh(sole[0], sole[1], 2.8, 1.8, deg + 90)), dot(heel[0], heel[1], 1.4)]


@icon("dance-steps", CAT, "Three footprints in a zigzag under a curved arrow showing the order of the steps",
      tags=["footwork", "step pattern", "dance lesson", "choreography", "footprints", "learn to dance", "waltz steps"])
def _(S):
    parts = []
    for cx, cy, d in ((5.5, 17, -8), (12, 13, 8), (18.5, 17, -8)):
        parts += _foot(cx, cy, d)
    parts.append(line("M5 8Q12 1 17.2 6"))
    parts.append(line(poly([(14.6, 3.6), (17.6, 6.3), (14, 7.6)], r=S.r * 0.3)))
    return parts
