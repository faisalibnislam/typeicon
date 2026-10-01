"""TypeIcon Core: music notation, gear, studio and stage (music batch 003).

Notation marks, instrument accessories, microphones, studio and PA equipment, stage items and dance.
Everything is drawn from the object itself. Long accessories lie on the 45 degree diagonal like the
instruments in music_001.py.
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, P, ST, U, Part, arc, circle, detail, dot, ellipse, filled_region, icon, line, path_to_d, poly, pt_on, rect,
    regular, seg, shell, solid,
)
from geometry import LINE, fmt

CAT = "music"


# --------------------------------------------------------------------------- helpers

def rnd(S, line_val, rounded_val):
    return line_val if S.name == "line" else rounded_val


def rot(pts, deg=45.0, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rp(pts, closed=True, r=0.0, deg=45.0, cx=12.0, cy=12.0):
    return poly(rot(pts, deg, cx, cy), closed=closed, r=r)


def rseg(x1, y1, x2, y2, deg=45.0, cx=12.0, cy=12.0):
    (a, b), (c, d) = rot([(x1, y1), (x2, y2)], deg, cx, cy)
    return seg(a, b, c, d)


def rcircle(x, y, r, deg=45.0, cx=12.0, cy=12.0):
    (a, b), = rot([(x, y)], deg, cx, cy)
    return circle(a, b, r)


def rpt(x, y, deg=45.0, cx=12.0, cy=12.0):
    return rot([(x, y)], deg, cx, cy)[0]


def rpath(cmds, deg=45.0, cx=12.0, cy=12.0) -> str:
    """Path from commands with rotated points: ("M", p) ("L", p) ("A", rx, ry, large, sweep, p) ("C", c1, c2, p) ("Q", c, p) ("Z",)."""
    out = []

    def pt(p):
        q = rot([p], deg, cx, cy)[0]
        return f"{fmt(q[0])} {fmt(q[1])}"
    for c in cmds:
        op = c[0]
        if op in ("M", "L"):
            out.append(op + pt(c[1]))
        elif op == "A":
            out.append(f"A{fmt(c[1])} {fmt(c[2])} {fmt(deg)} {c[3]} {c[4]} " + pt(c[5]))
        elif op == "Q":
            out.append("Q" + pt(c[1]) + " " + pt(c[2]))
        elif op == "C":
            out.append("C" + pt(c[1]) + " " + pt(c[2]) + " " + pt(c[3]))
        elif op == "Z":
            out.append("Z")
    return "".join(out)


def sym(cx, p0, segs) -> str:
    """Closed outline symmetric about x = cx. p0 is the top point on the axis; segs are cubic
    segments (c1, c2, p) of the right half, ending back on the axis at the bottom."""
    def m(p):
        return (2 * cx - p[0], p[1])

    def f(p):
        return f"{fmt(p[0])} {fmt(p[1])}"
    out = [f"M{f(p0)}"]
    for c1, c2, p in segs:
        out.append(f"C{f(c1)} {f(c2)} {f(p)}")
    for i in reversed(range(len(segs))):
        c1, c2, _ = segs[i]
        prev = p0 if i == 0 else segs[i - 1][2]
        out.append(f"C{f(m(c2))} {f(m(c1))} {f(m(prev))}")
    out.append("Z")
    return "".join(out)


def head(x, y, rx=2.6, ry=2.0, deg=-20):
    """Solid tilted note head centred on (x, y)."""
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    n = 16
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        ex, ey = rx * math.cos(t), ry * math.sin(t)
        pts.append((x + ex * ca - ey * sa, y + ex * sa + ey * ca))
    return Part("dot", poly(pts, closed=True))


def wave(x, y0, y1, amp, n):
    """Vertical wavy line from y0 to y1 with n half waves."""
    step = (y1 - y0) / n
    out = f"M{fmt(x)} {fmt(y0)}"
    for i in range(n):
        side = -1 if i % 2 == 0 else 1
        out += f"Q{fmt(x + side * amp * 2)} {fmt(y0 + step * (i + 0.5))} {fmt(x)} {fmt(y0 + step * (i + 1))}"
    return out


# ============================================================================ notation and music paper

@icon("accent-mark", CAT, "Sideways accent wedge above a filled note head",
      tags=["accent", "articulation", "emphasis", "notation", "music theory", "stress"])
def _(S):
    return [line(poly([(5, 3.5), (19, 7), (5, 10.5)], r=S.r)), head(12, 17.5, 3.6, 2.6)]


@icon("arpeggio-mark", CAT, "Wavy arpeggio line beside a stack of three chord notes with one stem",
      tags=["arpeggio", "broken chord", "rolled chord", "notation", "chord", "music theory"])
def _(S):
    return [line(wave(5, 3.5, 20.5, 1.1, 6)), head(13.5, 5.5, 2.7, 2.0), head(13.5, 12, 2.7, 2.0), head(13.5, 18.5, 2.7, 2.0),
            line(seg(16.2, 18.5, 16.2, 3))]


@icon("tremolo-mark", CAT, "Note stem crossed by three short slanted slashes",
      tags=["tremolo", "repeat", "notation", "trill", "music theory", "slashes"])
def _(S):
    return [head(8.5, 19, 3.2, 2.4), line(seg(11.7, 19, 11.7, 3)),
            line(seg(6.5, 7.5, 17, 4)), line(seg(6.5, 11.75, 17, 8.25)), line(seg(6.5, 16, 17, 12.5))]


@icon("music-staff", CAT, "Five-line music staff with a barline at each end",
      tags=["staff", "stave", "notation", "lines", "sheet music", "music theory"], aliases=["stave"])
def _(S):
    k = rnd(S, 0, 1)
    return [shell(rect(3, 4, 18, 16, k)), detail(seg(3, 8, 21, 8)), detail(seg(3, 12, 21, 12)), detail(seg(3, 16, 21, 16))]


@icon("grand-staff", CAT, "Two music staves joined by a curly brace at the left and a barline at the right",
      tags=["staff", "piano", "brace", "treble", "bass", "notation", "keyboard"])
def _(S):
    brace = "M7 3C4.5 3 5.5 8 3.5 12C5.5 16 4.5 21 7 21"
    return [line(brace), line(seg(10, 5, 21, 5)), line(seg(10, 9, 21, 9)), line(seg(10, 15, 21, 15)), line(seg(10, 19, 21, 19)),
            line(seg(10, 5, 10, 19)), line(seg(21, 5, 21, 19))]


@icon("chord-diagram", CAT, "Guitar chord grid with three strings, a top nut, two frets and three finger dots",
      tags=["chord", "chord chart", "guitar", "fretboard", "fingering", "strings", "ukulele"])
def _(S):
    return [line(seg(4, 4, 20, 4)),
            line(seg(6, 4, 6, 21)), line(seg(12, 4, 12, 21)), line(seg(18, 4, 18, 21)),
            line(seg(6, 11, 18, 11)), line(seg(6, 17, 18, 17)),
            dot(12, 7.5, 2.2), dot(18, 14, 2.2), dot(6, 14, 2.2)]


@icon("sheet-music", CAT, "Page of sheet music with a title line and a pair of beamed notes",
      tags=["score", "notation", "music page", "composition", "printed music", "notes", "song"])
def _(S):
    k = min(S.R, 3)
    return [shell(rect(4.5, 2.5, 15, 19, k)), detail(seg(8.5, 6.5, 15.5, 6.5)),
            head(9, 17.5, 2.2, 1.7), head(14.5, 16, 2.2, 1.7),
            detail(seg(10.9, 17.2, 10.9, 10.5)), detail(seg(16.4, 15.7, 16.4, 9)), detail(seg(10.9, 10.5, 16.4, 9))]


@icon("circle-of-fifths", CAT, "Ring divided into twelve segments around a centre dot",
      tags=["circle of fifths", "key signatures", "music theory", "keys", "harmony", "chords", "scales"])
def _(S):
    parts = [shell(circle(12, 12, 9)), detail(circle(12, 12, 4.75))]
    for i in range(12):
        a = -75 + 30 * i
        x0, y0 = pt_on(12, 12, 4.75, a)
        x1, y1 = pt_on(12, 12, 9, a)
        parts.append(detail(seg(x0, y0, x1, y1)))
    parts.append(dot(12, 12, 1.5))
    return parts


@icon("piano-roll", CAT, "Piano roll editor with a keyboard strip at the left and note bars of different lengths",
      tags=["sequencer", "daw", "midi editor", "note grid", "music production", "keys", "composition"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(seg(8.5, 3, 8.5, 21)), detail(seg(3, 9.75, 8.5, 9.75)),
            detail(seg(3, 14.25, 8.5, 14.25)),
            detail(seg(11.5, 7.5, 17, 7.5)), detail(seg(13.5, 12, 18, 12)), detail(seg(11.5, 16.5, 15.5, 16.5))]


@icon("music-composition", CAT, "Quill pen writing a note on a music staff line",
      tags=["composing", "songwriting", "write music", "quill", "score", "composer", "notation"])
def _(S):
    blade = "M9.5 14C7.5 8.5 12.5 3.5 20 3.5C19.5 10.5 15 15.5 9.5 14Z"
    return [shell(blade), detail(seg(10.5, 13, 16.5, 7)), line(seg(9.5, 14, 5.5, 18)),
            line(seg(3, 21, 21, 21)), head(15.5, 18.5, 2.3, 1.8)]


@icon("songbook", CAT, "Closed book with a music note on the cover and a ribbon bookmark",
      tags=["music book", "hymnal", "fake book", "song collection", "lessons", "notes", "library"])
def _(S):
    return [shell(rect(5, 2.5, 14, 17, min(S.R, 3))), detail(seg(8.5, 2.5, 8.5, 19.5)),
            head(12.9, 14.6, 2.3, 1.75), detail(seg(15, 14.4, 15, 6.5)), detail(poly([(15, 6.5), (17.25, 9.5)])),
            line(seg(16, 19.5, 16, 22))]


@icon("lyrics", CAT, "Lines of song text with a small music note in the top corner",
      tags=["song words", "verse", "chorus", "text", "karaoke", "words", "singalong"])
def _(S):
    return [line(seg(3, 6.5, 12, 6.5)), line(seg(3, 12, 21, 12)), line(seg(3, 17.5, 15, 17.5)),
            head(16.6, 7, 2.1, 1.6), line(seg(18.5, 6.8, 18.5, 2.5))]


@icon("music-stand", CAT, "Folding music stand with a sheet on its ledge, a central pole and tripod legs",
      tags=["sheet holder", "orchestra", "practice", "rehearsal", "score holder", "stand", "lessons"])
def _(S):
    return [shell(rect(5, 2, 14, 12, min(S.R, 2))), detail(seg(8.5, 6, 15.5, 6)), detail(seg(8.5, 10, 15.5, 10)),
            line(seg(3, 17, 21, 17)), line(seg(12, 17, 12, 19)),
            line(poly([(6, 22), (12, 19), (18, 22)], r=S.r))]


@icon("conductor-baton", CAT, "Thin conductor's baton with a pear-shaped cork handle",
      tags=["conducting", "orchestra", "maestro", "stick", "choir director", "tempo", "wand"])
def _(S):
    pear = rpath([("M", (12, 12)), ("C", (11, 12), (10.2, 13.5), (9.6, 15.5)), ("C", (9, 18), (10, 21.5), (12, 21.5)),
                  ("C", (14, 21.5), (15, 18), (14.4, 15.5)), ("C", (13.8, 13.5), (13, 12), (12, 12)), ("Z",)])
    return [line(rseg(12, 12.5, 12, 1.5)), solid(pear)]


def outline(*ds) -> str:
    """One closed outline from the union of several closed shapes."""
    return path_to_d(U(*[P(d) for d in ds]))


# ============================================================================ instrument accessories

@icon("guitar-pick", CAT, "Rounded triangular guitar pick with three grip dots",
      tags=["plectrum", "guitar", "strum", "bass", "accessory", "ukulele", "mediator"], aliases=["plectrum"])
def _(S):
    bottom = rnd(S, ((20, 13), (15.5, 18.5), (12, 21)), ((20, 13), (16.5, 19), (12, 20)))
    body = sym(12, (12, 3), [((16.5, 3), (20, 4.5), (20, 8.5)), bottom])
    return [shell(body), dot(9.5, 8.5, 1.2), dot(14.5, 8.5, 1.2), dot(12, 12.5, 1.2)]


@icon("capo", CAT, "Guitar capo: a clamp bar across the neck with strings above and below it",
      tags=["guitar", "transpose", "fretboard", "clamp", "accessory", "key change", "strings"])
def _(S):
    return [line(seg(8, 2, 8, 9.5)), line(seg(16, 2, 16, 9.5)), line(seg(8, 14.5, 8, 22)), line(seg(16, 14.5, 16, 22)),
            line(seg(12, 2, 12, 9.5)), line(seg(12, 14.5, 12, 22)),
            shell(rect(4.5, 9.5, 15, 5, min(S.R, 2.5))), detail(seg(9, 12, 15, 12))]


@icon("guitar-case", CAT, "Hard guitar case in the silhouette of a guitar with two latch bars",
      tags=["gig bag", "hard case", "travel", "instrument case", "carry", "luggage", "musician"])
def _(S):
    body = outline(ellipse(12, 16.25, 6.5, 5.5), ellipse(12, 10, 4.5, 3.75), rect(10, 2.5, 4, 7.5))
    return [shell(body), detail(seg(9, 13.5, 15, 13.5)), detail(seg(8.5, 18.5, 15.5, 18.5))]


@icon("violin-case", CAT, "Tapered violin case lying flat with a carry handle, a seam and two latches",
      tags=["fiddle", "viola", "strings", "instrument case", "travel", "carry", "orchestra"])
def _(S):
    body = poly([(2.5, 11.5), (6.5, 8), (21.5, 8), (21.5, 19.5), (6.5, 19.5), (2.5, 16)], closed=True, r=S.r)
    return [shell(body), line(poly([(10, 8), (10, 4.5), (17, 4.5), (17, 8)], r=S.r * 0.5)), detail(seg(6.5, 13, 21.5, 13)),
            dot(12, 16.5, 1.0), dot(18, 16.5, 1.0)]


@icon("brass-mouthpiece", CAT, "Brass mouthpiece with a wide rim, a deep cup and a tapering shank",
      tags=["trumpet", "trombone", "horn", "cornet", "embouchure", "accessory", "brass"])
def _(S):
    body = poly([(5, 3), (19, 3), (19, 5), (15.5, 8.5), (14.5, 11.5), (15.5, 21), (8.5, 21), (9.5, 11.5), (8.5, 8.5), (5, 5)],
                closed=True, r=S.r * 0.5)
    return [shell(body), detail(seg(7, 6.25, 17, 6.25))]


@icon("trumpet-mute", CAT, "Straight mute: a long cone with two cork strips, lying on the diagonal",
      tags=["trumpet", "brass", "jazz", "practice", "cone", "silencer", "trombone"])
def _(S):
    body = rp([(11, 2), (13, 2), (17.5, 21), (6.5, 21)], r=S.r * 0.6)
    return [shell(body), detail(rseg(6.5, 11, 17.5, 11)), detail(rseg(6.5, 16, 17.5, 16))]


# ============================================================================ studio and stage electronics

@icon("guitar-tuner", CAT, "Clip-on tuner with a round needle display and a headstock clamp underneath",
      tags=["tuning", "pitch", "chromatic", "headstock", "strings", "accessory", "intonation"])
def _(S):
    return [shell(rect(3.5, 2.5, 17, 12, S.R)), detail(arc(12, 10, 4, 200, 340)), line(seg(12, 10, 14.5, 6.5)),
            line(seg(12, 14.5, 12, 18.5)), line(poly([(7, 22), (7, 18.5), (17, 18.5), (17, 22)], r=S.r * 0.5))]


@icon("patch-cable", CAT, "Audio patch cable with a straight jack plug at each end and a looping cable",
      tags=["jack", "instrument cable", "guitar cable", "quarter inch", "cord", "lead", "connect"])
def _(S):
    return [line(seg(6, 2, 6, 6)), shell(rect(4, 6, 4, 6, rnd(S, 0, 1))), line(seg(18, 2, 18, 6)),
            shell(rect(16, 6, 4, 6, rnd(S, 0, 1))),
            line("M6 12V14C6 22 18 22 18 14V12")]


_DIN_KEY = {
    "line": "M13.75 3.17A9 9 0 1 1 10.25 3.17L10.25 6.25L13.75 6.25Z",
    "rounded": "M13.75 3.17A9 9 0 1 1 10.25 3.17L10.25 5A1.75 1.75 0 0 0 13.75 5Z",
}


@icon("midi-connector", CAT, "Round DIN plug face with a key notch and five pins in an arc",
      tags=["din", "five pin", "synth", "cable", "connector", "sequencer", "keyboard"], aliases=["din-connector"])
def _(S):
    parts = [shell(_DIN_KEY[S.name])]
    for a in (0, 45, 90, 135, 180):
        x, y = pt_on(12, 12.5, 5.5, a)
        parts.append(dot(x, y, 1.3))
    return parts


@icon("condenser-microphone", CAT, "Large studio condenser microphone with a mesh capsule inside a round shock-mount ring",
      tags=["studio mic", "vocal mic", "recording", "shock mount", "spider mount", "podcast", "large diaphragm"])
def _(S):
    return [line(circle(12, 10.5, 8.5)), shell(rect(9, 5, 6, 11, rnd(S, 1.5, 3))), detail(seg(9, 10.5, 15, 10.5)),
            line(seg(12, 19, 12, 22))]


@icon("shotgun-microphone", CAT, "Long shotgun microphone tube with slotted sides and a pistol grip",
      tags=["boom mic", "film", "video", "directional", "interview tube", "field recording", "camera mic"])
def _(S):
    k = rnd(S, 0, 2)
    return [shell(rp([(9, 1.5), (15, 1.5), (15, 15), (9, 15)], r=k)), detail(rseg(9, 5, 15, 5)), detail(rseg(9, 8.5, 15, 8.5)),
            detail(rseg(9, 12, 15, 12)), line(rseg(12, 15, 10.5, 22))]


@icon("lavalier-microphone", CAT, "Tiny lavalier microphone on a clothing clip with a looping cable",
      tags=["lapel mic", "clip-on mic", "wireless mic", "interview", "presenter", "tie mic", "lav"], aliases=["lapel-microphone"])
def _(S):
    return [shell(rect(9, 2, 6, 7, 3)), shell(rect(7.5, 11, 9, 4, rnd(S, 1, 1.5))), line(seg(12, 9, 12, 11)),
            line("M12 15V17C12 21.5 18 18.5 18 22")]


def fuzz(cx, cy, rx, ry, n=18, bump=0.9, deg=0.0):
    """Shaggy outline: an ellipse whose radius alternates between two values."""
    a0 = math.radians(deg)
    pts = []
    for i in range(n * 2):
        t = math.pi * i / n
        k = 1 + (bump / min(rx, ry)) * (1 if i % 2 == 0 else 0)
        ex, ey = rx * k * math.cos(t), ry * k * math.sin(t)
        pts.append((cx + ex * math.cos(a0) - ey * math.sin(a0), cy + ex * math.sin(a0) + ey * math.cos(a0)))
    return pts


@icon("boom-microphone", CAT, "Microphone in a shaggy windscreen on the end of a long boom pole",
      tags=["boom pole", "film set", "sound recordist", "fuzzy cover", "dead cat", "video production", "location sound"])
def _(S):
    ws = poly(rot(fuzz(12, 6.5, 2.6, 4.6, 12, 1.0, 0), 45), closed=True, r=S.r * 0.2)
    return [shell(ws), line(rseg(12, 12, 12, 22))]


@icon("gooseneck-microphone", CAT, "Microphone on a long bendy gooseneck rising from a small base",
      tags=["flexible mic", "desk mic", "podium", "conference", "lectern", "announcer", "speech"])
def _(S):
    return [shell(rect(15, 2, 5.5, 8, 2.75)), line("M17.75 10C17.75 15 8 13 8 18.5V20.5"), line(seg(4, 21, 12, 21))]


@icon("mic-boom-arm", CAT, "Desk boom arm with a clamp base, a bent arm and a microphone hanging from its end",
      tags=["studio arm", "desk mount", "podcast", "broadcast", "scissor arm", "stand", "clamp"])
def _(S):
    return [shell(rect(2.5, 18, 8, 3.5, min(S.R, 1.5))), line(poly([(6.5, 18), (6.5, 8.5), (17.5, 4.5)], r=S.r)),
            shell(rect(14.75, 7, 5.5, 9.5, 2.75)), line(seg(17.5, 4.5, 17.5, 7))]


@icon("pop-filter", CAT, "Round mesh pop filter screen on a bendy arm",
      tags=["pop screen", "plosives", "vocal booth", "recording", "studio", "microphone", "podcast"])
def _(S):
    h = 6.6
    parts = [shell(circle(12, 9.5, 7.5))]
    for o in (-3.5, 3.5):
        parts.append(detail(seg(12 + o, 9.5 - h, 12 + o, 9.5 + h)))
        parts.append(detail(seg(12 - h, 9.5 + o, 12 + h, 9.5 + o)))
    parts += [line(seg(12, 17, 12, 18.5)), line("M12 18.5C12 21 16 19.5 16 22")]
    return parts


@icon("microphone-windscreen", CAT, "Handheld microphone with a shaggy foam windscreen over its head",
      tags=["foam cover", "windshield", "wind muff", "outdoor", "interview", "reporter", "fur"])
def _(S):
    ws = poly(fuzz(12, 8, 5.2, 5.2, 14, 1.0, 0), closed=True, r=S.r * 0.2)
    return [shell(ws), shell(rect(9.75, 15, 4.5, 7, rnd(S, 0.5, 2)))]


@icon("vocal-booth", CAT, "Curved reflection shield behind a microphone on a stand",
      tags=["isolation shield", "reflection filter", "recording", "studio", "voice over", "sound booth", "vocalist"])
def _(S):
    return [line("M3 20V11A9 9 0 0 1 21 11V20"), shell(rect(9.5, 8, 5, 7.5, 2.5)), line(seg(12, 15.5, 12, 20)),
            line(seg(8, 20, 16, 20))]


@icon("acoustic-panel", CAT, "Square acoustic foam panel with two rows of wedges",
      tags=["sound treatment", "studio foam", "soundproofing", "absorber", "recording room", "pyramid foam", "wedge"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(poly([(3, 9), (7.5, 5.5), (12, 9), (16.5, 5.5), (21, 9)])),
            detail(poly([(3, 18), (7.5, 14.5), (12, 18), (16.5, 14.5), (21, 18)]))]


@icon("on-air-sign", CAT, "Rounded lit studio sign with a broadcast dot and waves, hung by two short mounts",
      tags=["broadcast", "recording light", "live", "studio", "radio", "podcast", "do not disturb"])
def _(S):
    return [shell(rect(2.5, 7.5, 19, 11, S.R)), line(seg(7, 7.5, 7, 3.5)), line(seg(17, 7.5, 17, 3.5)),
            dot(12, 13, 1.6), detail(arc(12, 13, 4.25, -40, 40)), detail(arc(12, 13, 4.25, 140, 220))]


@icon("audio-interface", CAT, "Audio interface box with two input jacks, a small gain knob and a large volume knob",
      tags=["sound card", "recording", "home studio", "usb interface", "xlr", "preamp", "daw"])
def _(S):
    return [shell(rect(2.5, 6.5, 19, 11, S.R)), dot(6.75, 12, 1.7), dot(11.5, 12, 1.7), detail(circle(17, 12, 2.5))]


@icon("dj-controller", CAT, "DJ controller with two jogwheels at the sides and a fader between them",
      tags=["deck", "mixer", "decks", "turntablism", "club", "midi controller", "scratch"])
def _(S):
    return [shell(rect(2, 5.5, 20, 13, S.R)), detail(circle(6.75, 12, 3.1)), detail(circle(17.25, 12, 3.1)),
            dot(6.75, 12, 1.0), dot(17.25, 12, 1.0), detail(seg(12, 8.5, 12, 15.5))]


@icon("effects-pedal", CAT, "Guitar stompbox pedal with two knobs, a small light and a footswitch",
      tags=["stompbox", "guitar pedal", "distortion", "overdrive", "reverb", "delay", "fx"], aliases=["stompbox"])
def _(S):
    return [shell(rect(5, 2, 14, 20, S.R)), dot(9, 6, 1.6), dot(15, 6, 1.6), dot(12, 10.5, 0.9), detail(circle(12, 16.25, 2.6))]


@icon("wah-pedal", CAT, "Wah pedal seen from the side: a hinged sloping treadle on a low base",
      tags=["guitar pedal", "expression pedal", "rocker", "treadle", "foot", "effect", "volume pedal"])
def _(S):
    return [shell(rect(3, 17.5, 18, 4, min(S.R, 2))),
            shell(poly([(3, 14.5), (21, 6.5), (21, 14.5)], closed=True, r=S.r)),
            dot(17.5, 11.25, 1.0)]


@icon("guitar-amplifier", CAT, "Combo guitar amplifier with a row of knobs on top and a round speaker grille",
      tags=["amp", "combo amp", "electric guitar", "cabinet", "tube amp", "practice amp", "stage"], aliases=["guitar-amp"])
def _(S):
    return [shell(rect(3, 3.5, 18, 17.5, S.R)), dot(7.5, 7, 1.15), dot(12, 7, 1.15), dot(16.5, 7, 1.15),
            detail(circle(12, 15, 4.25)), dot(12, 15, 1.3)]


@icon("amp-stack", CAT, "Amplifier head sitting on a speaker cabinet with four round speakers",
      tags=["half stack", "guitar amp", "rock", "cabinet", "stage", "loud", "backline"])
def _(S):
    return [shell(rect(3, 2, 18, 6, rnd(S, 1, 2.5))), dot(7, 5, 1.0), dot(11, 5, 1.0), dot(17, 5, 1.0),
            shell(rect(3.5, 9.5, 17, 12.5, rnd(S, 1, 3))), dot(8.5, 13.75, 1.9), dot(15.5, 13.75, 1.9),
            dot(8.5, 18.5, 1.9), dot(15.5, 18.5, 1.9)]


@icon("pa-speaker", CAT, "Trapezoid PA speaker cabinet on a tripod pole stand",
      tags=["loudspeaker", "public address", "sound system", "party", "dj speaker", "stand", "live sound"])
def _(S):
    body = poly([(6, 2.5), (18, 2.5), (16.5, 13.5), (7.5, 13.5)], closed=True, r=S.r * 0.6)
    return [shell(body), dot(12, 5.5, 1.0), dot(12, 9.75, 1.9), line(seg(12, 13.5, 12, 18.5)),
            line(poly([(6, 22), (12, 18.5), (18, 22)], r=S.r))]


@icon("stage-monitor-wedge", CAT, "Floor monitor wedge speaker angled up with a driver below its sloped face",
      tags=["monitor", "foldback", "stage", "floor speaker", "wedge", "band", "live sound"])
def _(S):
    return [shell(poly([(2.5, 20), (21.5, 20), (21.5, 5), (2.5, 14)], closed=True, r=S.r)), dot(13, 14.5, 2.0), dot(18, 13, 1.0)]


@icon("line-array", CAT, "Line array speaker stack hanging in a gentle curve from a rigging bar",
      tags=["flown speakers", "concert", "pa system", "rigging", "festival", "sound reinforcement", "stack"])
def _(S):
    body = poly([(7, 6.5), (16, 6.5), (16.5, 12), (18, 17), (20, 22), (9, 22), (8, 17), (7.3, 12)], closed=True, r=S.r * 0.6)
    return [line(seg(5, 2.5, 18, 2.5)), line(seg(9, 2.5, 9, 6.5)), line(seg(15, 2.5, 15, 6.5)), shell(body),
        detail(seg(7.2, 11, 16.2, 11)), detail(seg(8, 15.5, 17.6, 15.5))]


@icon("speaker-driver", CAT, "Front view of a loudspeaker driver: square frame, cone surround and dust cap",
      tags=["woofer", "cone", "tweeter", "subwoofer", "hi-fi", "audio component", "diy speaker"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, S.R)), detail(circle(12, 12, 6.25)), dot(12, 12, 2.6)]


@icon("record-crate", CAT, "Crate of vinyl records with a square sleeve and a record label standing up behind the front slat",
      tags=["vinyl", "digging", "record shop", "lp", "collection", "dj", "albums"])
def _(S):
    return [line(poly([(5, 11), (5, 3), (19, 3), (19, 11)], r=S.r)), dot(12, 7, 1.7),
            shell(rect(3, 11.5, 18, 9.5, rnd(S, 1, 2))), detail(seg(3, 16.25, 21, 16.25))]


@icon("vu-meter", CAT, "Analog VU meter window with an arched scale and a needle",
      tags=["level meter", "audio level", "analog", "decibel", "gauge", "signal", "mixer"])
def _(S):
    return [shell(rect(2.5, 4.5, 19, 15, S.R)), detail(arc(12, 16.25, 6.75, 205, 335)), line(seg(12, 16.25, 15, 11.25)),
            dot(12, 16.25, 1.3)]


@icon("field-recorder", CAT, "Handheld field recorder with a wide stereo microphone head, a small screen and buttons",
      tags=["portable recorder", "audio recorder", "interview", "sound design", "stereo mic", "handheld", "dictaphone"])
def _(S):
    body = outline(rect(5, 2, 14, 8.5, rnd(S, 1.5, 4)), rect(6.5, 8, 11, 14, rnd(S, 1.5, 3)))
    return [shell(body), detail(seg(12, 2, 12, 8.5)), detail(seg(5, 10.5, 19, 10.5)), detail(rect(9.5, 13.25, 5, 3.25)),
            dot(10, 19.5, 1.0), dot(14, 19.5, 1.0)]


@icon("audio-knob", CAT, "Rotary audio knob with a pointer line and a row of tick dots around it",
      tags=["dial", "potentiometer", "volume knob", "control", "mixer", "gain", "synth"])
def _(S):
    parts = [shell(poly(regular(12, 12, 5.5, 12), closed=True, r=S.r)), detail(seg(12, 12, 12, 8))]
    for a in (135, 180, 225, 270, 315, 360, 405):
        x, y = pt_on(12, 12, 8.6, a)
        parts.append(dot(x, y, 0.95))
    return parts


@icon("audio-fader", CAT, "Vertical mixer fader: a slot track, a rectangular fader cap and level ticks at the side",
      tags=["slider", "channel fader", "mixing desk", "level", "volume", "console", "gain"])
def _(S):
    return [line(seg(14, 3, 14, 9)), line(seg(14, 14, 14, 21)), shell(rect(9.5, 9, 9, 5, min(S.R, 2))), line(seg(3, 4, 6.5, 4)), line(seg(3, 8, 6.5, 8)),
            line(seg(3, 12, 6.5, 12)), line(seg(3, 16, 6.5, 16)), line(seg(3, 20, 6.5, 20))]


@icon("multitrack-audio", CAT, "Three stacked audio tracks, each a row of waveform bars of different heights",
      tags=["daw", "tracks", "timeline", "recording", "editing", "mixing", "waveform"])
def _(S):
    def track(y, hs):
        return [line(seg(4 + 4 * i, y - h / 2, 4 + 4 * i, y + h / 2)) for i, h in enumerate(hs)]
    return track(5, [2, 5, 3, 5, 2]) + track(12, [4, 2, 6, 3, 5]) + track(19, [3, 5, 2, 4, 2])


@icon("spectrogram", CAT, "Frame of dotted columns of different heights, like a heat map of sound over time",
      tags=["frequency", "sound analysis", "fft", "audio analysis", "heat map", "spectrum", "visualizer"])
def _(S):
    parts = [shell(rect(2.5, 2.5, 19, 19, S.R))]
    for x, n in ((7, 2), (12, 4), (17, 3)):
        for i in range(n):
            parts.append(dot(x, 17 - 3.5 * i, 1.2))
    return parts


@icon("karaoke", CAT, "Lyric screen with text lines and a microphone in front of its lower corner",
      tags=["sing along", "lyrics screen", "singer", "party", "bar", "music video", "mic"])
def _(S):
    return [line(poly([(11.5, 15), (3, 15), (3, 3), (21, 3), (21, 7)], r=S.r * 0.5)), line(seg(6.5, 7, 15, 7)),
            line(seg(6.5, 11, 10, 11)),
            shell(rect(14, 10.5, 7, 8.5, 3.5)), line(seg(17.5, 19, 17.5, 22))]


@icon("record-needle", CAT, "Tonearm with a cartridge and a stylus touching the grooves of a record",
      tags=["turntable", "stylus", "cartridge", "tonearm", "vinyl", "phono", "playing"])
def _(S):
    return [line(arc(12, 23, 9.5, 180, 360)), line(arc(12, 23, 4.5, 180, 360)),
            line(seg(20.5, 2.5, 11, 9)), shell(rp([(8, 8.5), (12.5, 8.5), (12.5, 12), (8, 12)], r=S.r * 0.3, deg=-15, cx=10, cy=10)),
            line(seg(9.2, 12.5, 9.2, 14.2))]


# ============================================================================ stage, events and memorabilia

@icon("concert-stage", CAT, "Stage platform with a curtain swept back at each side and a spotlight cone in the middle",
      tags=["theatre", "venue", "live music", "show", "performance", "gig", "auditorium"])
def _(S):
    return [line(seg(2.5, 2.5, 21.5, 2.5)), line("M4 2.5C7 6 7 10.5 4 14.5"), line("M20 2.5C17 6 17 10.5 20 14.5"),
            line(seg(10.75, 6, 9.75, 14)), line(seg(13.25, 6, 14.25, 14)),
            shell(rect(2.5, 17.5, 19, 4, rnd(S, 0.5, 1.5)))]


@icon("stage-light", CAT, "Stage light hanging from a bar with a cone of light shining below it",
      tags=["spotlight", "par can", "theatre lighting", "concert", "lighting rig", "floodlight", "gig"])
def _(S):
    can = poly([(9.5, 5), (14.5, 5), (17, 12), (7, 12)], closed=True, r=S.r * 0.5)
    return [line(seg(5, 2, 19, 2)), line(seg(12, 2, 12, 5)), shell(can), line(seg(7.5, 15.5, 4, 22)),
            line(seg(12, 15.5, 12, 22)), line(seg(16.5, 15.5, 20, 22))]


@icon("fog-machine", CAT, "Fog machine box with a nozzle blowing a cloud of fog",
      tags=["smoke machine", "haze", "stage effect", "party", "halloween", "theatre", "dry ice"])
def _(S):
    cloud = "M11.5 10.5H18A3 3 0 0 0 18.5 4.5A4.5 4.5 0 0 0 10.5 5.5A2.5 2.5 0 0 0 11.5 10.5Z"
    return [shell(rect(2.5, 14, 13, 7.5, S.R)), line(seg(15.5, 16.5, 19, 16.5)), shell(cloud), dot(21, 13.5, 0.9)]


@icon("setlist", CAT, "Taped sheet with a numbered list of song lines",
      tags=["song order", "gig list", "running order", "playlist", "stage", "band", "repertoire"])
def _(S):
    k = min(S.R, 3)
    tape = lambda cx, cy, d: Part("dot", poly(rot([(cx - 2.6, cy - 1), (cx + 2.6, cy - 1), (cx + 2.6, cy + 1), (cx - 2.6, cy + 1)], d, cx, cy), closed=True))
    return [shell(rect(5, 3, 14, 18.5, k)), dot(8.75, 8.5, 1.0), detail(seg(11.5, 8.5, 16, 8.5)), dot(8.75, 13, 1.0),
            detail(seg(11.5, 13, 16, 13)), dot(8.75, 17.5, 1.0), detail(seg(11.5, 17.5, 14.5, 17.5)),
            tape(5.25, 3.25, -40), tape(18.75, 3.25, 40)]


def star_pts(cx, cy, ro, ri):
    pts = []
    for i in range(10):
        a = math.radians(-90 + 36 * i)
        r = ro if i % 2 == 0 else ri
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


@icon("backstage-pass", CAT, "Laminated pass card hanging from a lanyard with a star and a text band",
      tags=["vip", "access pass", "all access", "lanyard", "crew", "badge", "concert ticket"])
def _(S):
    return [line(poly([(8.5, 2), (12, 8), (15.5, 2)], r=S.r)), shell(rect(5.5, 8.5, 13, 13.5, min(S.R, 3))),
            Part("dot", poly(star_pts(12, 13, 2.9, 1.3), closed=True)), detail(seg(8.5, 18.25, 15.5, 18.25))]


@icon("gold-record", CAT, "Framed vinyl disc with a centre label above a small plaque",
      tags=["award", "platinum", "sales award", "hit record", "achievement", "album", "trophy"])
def _(S):
    return [shell(rect(3, 2, 18, 15.5, S.R)), detail(circle(12, 9.75, 5)), dot(12, 9.75, 1.3), solid(rect(8, 19.5, 8, 2.5))]


@icon("opera-glasses", CAT, "Opera glasses: two round barrels joined by a bridge on a slim handle",
      tags=["theatre binoculars", "lorgnette", "show", "audience", "viewing", "ballet", "performance"])
def _(S):
    k = rnd(S, 2.5, 4)
    return [shell(rect(2.5, 2.5, 8.5, 8.5, k)), shell(rect(13, 2.5, 8.5, 8.5, k)), dot(6.75, 6.75, 1.1), dot(17.25, 6.75, 1.1),
            line(seg(11, 6.75, 13, 6.75)), line(seg(12, 11, 12, 22))]


# ============================================================================ audiences, performers and dance

HR = 2.25  # head radius of the stick figures (same as people.py)


def limb(S, *pts):
    return line(poly(list(pts), r=S.r))


@icon("concert-crowd", CAT, "Three fans seen from behind, a taller one in the middle, under a spotlight glow",
      tags=["audience", "fans", "gig", "festival", "cheering", "live music", "mosh pit"])
def _(S):
    parts = [line(seg(12, 2, 12, 4.5)), line(seg(7.5, 3, 8.5, 5.5)), line(seg(16.5, 3, 15.5, 5.5))]
    parts += [dot(12, 9.5, 1.9), line("M8 17.5V16.5A4 4 0 0 1 16 16.5V17.5")]
    for x in (5.5, 18.5):
        parts += [dot(x, 15.5, 2.0), line(f"M{fmt(x - 3.5)} 22V21A3.5 3.5 0 0 1 {fmt(x + 3.5)} 21V22")]
    return parts


@icon("busking", CAT, "Open instrument case on the ground with coins in it and a guitar standing beside it",
      tags=["street musician", "street performer", "tips", "coins", "guitar", "donation", "sidewalk"])
def _(S):
    body = outline(circle(18.5, 16.75, 3.75), circle(18.5, 11.25, 2.6))
    return [shell(rect(2, 13.5, 12.5, 8, rnd(S, 1, 2))), dot(5.5, 17.5, 1.0), dot(8.25, 17.5, 1.0), dot(11, 17.5, 1.0),
            shell(body), dot(18.5, 16.75, 1.0), line(seg(18.5, 8.75, 18.5, 2.5))]


@icon("choir", CAT, "Three singers in long robes standing in a row with their mouths open",
      tags=["chorus", "singers", "church", "vocal group", "hymn", "carol", "ensemble"])
def _(S):
    parts = []
    for x in (4.75, 12, 19.25):
        parts.append(dot(x, 5.25, 1.9))
        parts.append(line(poly([(x - 2.4, 21.5), (x, 10), (x + 2.4, 21.5)], r=S.r * 0.4)))
    return parts


@icon("disc-jockey", CAT, "Person wearing headphones behind a deck with two platters, hands on the records",
      tags=["dj", "turntables", "club", "mixing", "nightlife", "party", "decks"])
def _(S):
    return [dot(12, 6.5, HR), line(arc(12, 6.5, 4.5, 180, 360)), line(seg(7.5, 6, 7.5, 8.5)), line(seg(16.5, 6, 16.5, 8.5)),
            limb(S, (7, 14.5), (8.5, 11.5), (15.5, 11.5), (17, 14.5)),
            shell(rect(2.5, 15.5, 19, 6, S.R)), dot(8, 18.5, 1.6), dot(16, 18.5, 1.6)]


@icon("ballroom-dancing", CAT, "Dancing couple in a waltz hold, one figure with a flaring skirt and hands joined overhead",
      tags=["waltz", "couple dance", "partner dance", "formal dance", "tango", "social dance", "prom"])
def _(S):
    skirt = poly([(17.5, 10.5), (13.5, 21.5), (21.5, 21.5)], closed=True, r=S.r * 0.5)
    return [dot(6.5, 4.5, HR), dot(17.5, 4.5, HR), limb(S, (6.5, 8.5), (6.5, 15)), limb(S, (4.5, 21.5), (6.5, 15), (9, 21.5)),
            limb(S, (6.5, 9.5), (12, 6.5), (17.5, 9.5)), shell(skirt)]


@icon("breakdancing", CAT, "Breakdancer upside down spinning on the head with the legs spread in a V",
      tags=["b-boy", "b-girl", "hip hop", "headspin", "street dance", "freeze", "dance battle"])
def _(S):
    return [
        dot(12, 19.5, HR), limb(S, (12, 16.5), (12, 10)), limb(S, (4.5, 3.5), (12, 10), (19.5, 3.5)),
        limb(S, (6, 21.5), (8.5, 16.5), (12, 15)), limb(S, (18, 21.5), (15.5, 16.5), (12, 15))]


@icon("flamenco-dancer", CAT, "Dancer with one arm raised high and a long ruffled dress swirling out",
      tags=["spanish dance", "spain", "ruffled dress", "castanets", "andalusia", "folk dance", "tablao"])
def _(S):
    dress = poly([(10, 10.5), (13, 10.5), (21.5, 21.5), (18.5, 19.5), (15.5, 21.5), (12.5, 19.5), (9.5, 21.5), (6.5, 19.5), (3, 21.5)],
                 closed=True, r=S.r * 0.3)
    return [dot(11, 4.5, HR), limb(S, (11.5, 9.5), (14.5, 6), (17, 2.5)), limb(S, (10, 10.5), (7, 11), (8, 14)), shell(dress)]


@icon("hula-dance", CAT, "Dancer in a grass skirt with a flower at the ear and both arms swaying to one side",
      tags=["hawaii", "hawaiian", "luau", "polynesian", "island dance", "lei", "tropical"])
def _(S):
    skirt = poly([(9.5, 13), (14.5, 13), (17, 21.5), (7, 21.5)], closed=True, r=S.r * 0.4)
    return [dot(11, 4.5, HR), dot(15.25, 2.75, 1.0), limb(S, (12, 9), (16.5, 8.5), (20.5, 5.5)), limb(S, (9.5, 10), (7, 12), (4.5, 10.5)),
            shell(skirt), detail(seg(10.5, 14, 9.5, 21)), detail(seg(13.5, 14, 14.5, 21))]


@icon("indian-classical-dance", CAT, "Dancer in a wide bent-knee stance with one arm out in a hand gesture and a pleated fan skirt",
      tags=["bharatanatyam", "kathak", "odissi", "mudra", "india", "classical dance", "south asian"])
def _(S):
    fan = poly([(12, 13.5), (9, 21.5), (15, 21.5)], closed=True, r=S.r * 0.3)
    return [dot(12, 4.5, HR), limb(S, (12, 8.5), (12, 13.5)), limb(S, (12, 9.5), (17, 9.5), (21.5, 7)),
            limb(S, (12, 9.5), (7.5, 11), (4.5, 8.5)), limb(S, (12, 13.5), (5.5, 15.5), (5.5, 21.5)),
            limb(S, (12, 13.5), (18.5, 15.5), (18.5, 21.5)), shell(fan)]


@icon("lion-dance", CAT, "Front view of a lion dance head with big eyes, a horn and a fringe above two legs",
      tags=["chinese new year", "lunar new year", "festival", "parade", "costume", "southern lion", "dragon and lion"])
def _(S):
    head = poly([(4.5, 6), (19.5, 6), (20.5, 14.5), (18, 12.5), (15, 14.5), (12, 12.5), (9, 14.5), (6, 12.5), (3.5, 14.5)],
                closed=True, r=S.r * 0.6)
    return [line(seg(12, 6, 12, 2)), dot(12, 2, 1.0), shell(head), dot(8.5, 9.25, 1.4), dot(15.5, 9.25, 1.4),
            limb(S, (8, 15.5), (8, 21.5)), limb(S, (16, 15.5), (16, 21.5))]


@icon("audio-balance", CAT, "Horizontal balance slider with the knob centred, a centre tick and arrows to the left and right",
      tags=["pan", "stereo balance", "left right", "panning", "speaker balance", "volume", "slider"])
def _(S):
    return [line(poly([(6, 8), (2.5, 12), (6, 16)], r=S.r)), line(poly([(18, 8), (21.5, 12), (18, 16)], r=S.r)),
            line(seg(8, 12, 16, 12)), dot(12, 12, 2.6), line(seg(12, 3.5, 12, 7))]
