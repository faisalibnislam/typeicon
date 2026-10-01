"""TypeIcon Core: music batch 002 (world percussion, small instruments and notation marks).

Percussion and idiophones drawn from the objects themselves, followed by the signs of written music.
Notation signs are drawn from plain strokes, arcs and dots so they stay clear at 16 px.
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


def rpt(x, y, deg=45.0, cx=12.0, cy=12.0):
    return rot([(x, y)], deg, cx, cy)[0]


def rpath(cmds, deg=45.0, cx=12.0, cy=12.0) -> str:
    """Path from commands with rotated points: ("M", p) ("L", p) ("A", rx, ry, large, sweep, p) ("C", c1, c2, p) ("Z",)."""
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


def rell(cx, cy, rx, ry, deg, px, py):
    """Closed ellipse centred (cx, cy) rotated by deg about (px, py)."""
    return rpath([("M", (cx - rx, cy)), ("A", rx, ry, 1, 1, (cx + rx, cy)), ("A", rx, ry, 1, 1, (cx - rx, cy)), ("Z",)],
                 deg, px, py)


def outline(*ds) -> str:
    return path_to_d(U(*[P(d) for d in ds]))


# ============================================================================ struck and shaken percussion

@icon("gong", CAT, "Round gong with a raised centre boss hanging in a frame",
      tags=["tam-tam", "percussion", "temple", "chinese gong", "ceremony", "instrument"])
def _(S):
    return [line(poly([(3, 21.5), (3, 3.5), (21, 3.5), (21, 21.5)], r=S.r)), line(seg(12, 3.5, 12, 9)),
            shell(circle(12, 14.5, 5)), dot(12, 14.5, 1.5)]


@icon("cymbal", CAT, "Cymbal: a thin domed disc with a small cup on a stand rod",
      tags=["crash", "ride", "percussion", "drum kit", "brass", "instrument"])
def _(S):
    return [line(seg(12, 3.5, 12, 8)),
            shell("M2.5 12.5C6 9.5 9 8.5 12 8.5C15 8.5 18 9.5 21.5 12.5C18 13.5 15 14 12 14C9 14 6 13.5 2.5 12.5Z"),
            line(seg(12, 14, 12, 20.5)), line(poly([(7, 21.5), (12, 19), (17, 21.5)], r=S.r))]


@icon("hi-hat", CAT, "Hi-hat: two cymbals facing each other on a tall stand",
      tags=["drum kit", "cymbals", "percussion", "drummer", "pedal", "instrument"])
def _(S):
    return [line(seg(12, 2.5, 12, 6)), line(poly([(3, 9), (12, 6), (21, 9)], r=S.r)),
            line(poly([(3, 13), (12, 16), (21, 13)], r=S.r)), line(seg(12, 16, 12, 20)),
            line(poly([(6.5, 21.5), (12, 19.5), (17.5, 21.5)], r=S.r))]


@icon("triangle-instrument", CAT, "Metal triangle hanging from a cord with a beater",
      tags=["percussion", "orchestra", "ding", "chime", "instrument", "music"])
def _(S):
    tri = poly([(18.5, 16), (12, 6), (3, 20.5), (15, 20.5)], r=S.r)
    return [line(tri), line(seg(12, 6, 12, 2.5)), line(seg(18.5, 3, 15.5, 11)), dot(18.8, 2.6, 1.5)]


def _maraca(S, sgn):
    px, py = 12, 17
    head = rell(12, 7, 3.25, 4.25, sgn * 35, px, py)
    return [shell(head), line(rseg(12, 11.25, 12, 21.5, sgn * 35, px, py))]


@icon("maracas", CAT, "Pair of maracas crossed at the handles",
      tags=["shaker", "rattle", "latin", "percussion", "salsa", "instrument"])
def _(S):
    return _maraca(S, 1) + _maraca(S, -1)


def _clave_filled():
    st = [(9.75, 2.5), (14.25, 2.5), (14.25, 21.5), (9.75, 21.5)]
    a = U(P(rp(st, True, 0, 45)), ST(rp(st, True, 0, 45), 2, "butt", "miter", 4))
    b = U(P(rp(st, True, 0, -45)), ST(rp(st, True, 0, -45), 2, "butt", "miter", 4))
    cut = U(P(rp(st, True, 0, -45)), ST(rp(st, True, 0, -45), 4, "butt", "miter", 4))
    return U(D(a, cut), b)


@icon("claves", CAT, "Claves: two short round sticks crossed in an X",
      tags=["percussion", "latin", "wooden sticks", "rhythm", "cuban", "instrument"], filled=_clave_filled)
def _(S):
    k = rnd(S, 0, 1.25)
    st = [(9.75, 2.5), (14.25, 2.5), (14.25, 21.5), (9.75, 21.5)]
    return [shell(rp(st, True, k, 45)), shell(rp(st, True, k, -45))]


@icon("guiro", CAT, "Guiro: a long hollow gourd with rows of ridges and a scraper stick",
      tags=["gourd", "latin", "scraper", "percussion", "rasp", "instrument"])
def _(S):
    return [shell(rect(2.5, 11, 19, 8.5, rnd(S, 2, 4))), detail(seg(7, 13.5, 7, 17)), detail(seg(10.5, 13.5, 10.5, 17)),
            detail(seg(14, 13.5, 14, 17)), detail(seg(17.5, 13.5, 17.5, 17)), line(seg(6, 3.5, 15, 11))]


@icon("cabasa", CAT, "Cabasa: a cylinder wrapped in rows of steel beads on a handle",
      tags=["afuche", "shaker", "beads", "latin", "percussion", "instrument"])
def _(S):
    parts = [shell(rect(5.5, 2.5, 13, 11.5, rnd(S, 1.5, 4))), shell(rect(10, 14, 4, 7.5, rnd(S, 0.5, 2)))]
    parts += [dot(x, y, 1) for y in (6.5, 10.5) for x in (9, 12, 15)]
    return parts


@icon("shekere", CAT, "Shekere: a round gourd with a narrow neck covered in a net of beads",
      tags=["african", "gourd rattle", "beaded", "percussion", "shaker", "instrument"])
def _(S):
    body = outline(circle(12, 15.25, 7), rect(10, 3, 4, 9))
    return [shell(body), dot(12, 11.75, 1), dot(8.75, 15.25, 1), dot(15.25, 15.25, 1), dot(12, 18.75, 1),
            dot(12, 15.25, 1)]


@icon("rain-stick", CAT, "Rain stick: a long closed tube with a spiral inside and falling grains",
      tags=["rainmaker", "percussion", "nature sound", "tube", "shaker", "instrument"])
def _(S):
    k = rnd(S, 0, 2.5)
    return [shell(rp([(8.5, 2), (15.5, 2), (15.5, 22), (8.5, 22)], True, k)),
            detail(rseg(8.5, 7, 15.5, 9.5)), detail(rseg(8.5, 12.5, 15.5, 15)), dot(4, 4, 1), dot(7.5, 2.75, 1), dot(3, 8, 1)]


@icon("tubular-bells", CAT, "Tubular bells: metal tubes of stepped lengths hanging from a bar",
      tags=["chimes", "orchestra", "percussion", "church bells", "hanging tubes", "instrument"])
def _(S):
    parts = [line(seg(2.5, 3.5, 21.5, 3.5))]
    for x, h in ((4.5, 14), (12, 11), (19.5, 8)):
        parts += [line(seg(x, 3.5, x, 7)), shell(rect(x - 1.5, 7, 3, h, rnd(S, 0.5, 1.5)))]
    return parts


@icon("sleigh-bells", CAT, "Sleigh bells: two round jingle bells hanging from a leather strap",
      tags=["jingle bells", "winter", "christmas", "percussion", "holiday", "instrument"])
def _(S):
    parts = [shell(rect(2.5, 3.5, 19, 4, rnd(S, 1, 2)))]
    for x in (6.75, 17.25):
        parts += [line(seg(x, 7.5, x, 11.5)), shell(circle(x, 15.5, 3.5)), detail(seg(x, 16, x, 19))]
    return parts


@icon("agogo-bells", CAT, "Agogo bells: two cone bells of different sizes joined by a bent handle",
      tags=["agogo", "cowbell", "samba", "brazil", "percussion", "iron bell"])
def _(S):
    return [shell(poly([(2.5, 3.5), (11, 3.5), (9.25, 14), (4.25, 14)], True, S.r)),
            shell(poly([(14.5, 8), (21.5, 8), (19.75, 14), (16, 14)], True, S.r)),
            line(poly([(6.75, 14), (6.75, 19.5), (17.9, 19.5), (17.9, 14)], r=S.r))]


@icon("wood-block", CAT, "Wood block: a hollow block with a slot along its side and a mallet",
      tags=["temple block", "percussion", "clack", "rhythm", "mallet", "instrument"])
def _(S):
    return [shell(rect(2.5, 10.5, 17, 10, rnd(S, 1.5, 3))), detail(seg(6.5, 15.5, 15.5, 15.5)),
            line(seg(21, 3, 14.5, 9)), dot(21, 3, 1.5)]


@icon("slit-drum", CAT, "Slit drum: a hollow log lying on its side with a long slit cut along the top",
      tags=["log drum", "tongue drum", "african", "percussion", "wooden drum", "instrument"])
def _(S):
    body = outline(ellipse(6.5, 12.5, 3.5, 6), rect(6.5, 6.5, 15, 12, rnd(S, 1.5, 4)))
    return [shell(body), detail("M6.5 6.5A3.5 6 0 0 1 6.5 18.5"), detail(seg(12, 12.5, 18.5, 12.5))]


@icon("washboard-instrument", CAT, "Washboard instrument: a wooden frame holding rows of corrugated metal, played by scraping",
      tags=["skiffle", "jug band", "zydeco", "scraper", "percussion", "folk"])
def _(S):
    wave = "q1.25 -1.5 2.5 0t2.5 0t2.5 0t2.5 0"
    return [shell(rect(4.5, 2.5, 15, 19, rnd(S, 1.5, 3.5))), detail(seg(4.5, 6.5, 19.5, 6.5)),
            detail("M7 12" + wave), detail("M7 17" + wave)]


@icon("finger-cymbals", CAT, "Finger cymbals: two small discs with centre holes joined by an elastic loop",
      tags=["zills", "belly dance", "tingsha", "percussion", "chime", "instrument"])
def _(S):
    return [shell(circle(7.5, 7.5, 4)), shell(circle(16.5, 16.5, 4)), dot(7.5, 7.5, 1.25), dot(16.5, 16.5, 1.25),
            line("M7.5 7.5C12 1 22 2 18.5 10.5")]


@icon("handpan", CAT, "Handpan: two joined steel domes like a saucer with a raised note on top",
      tags=["tuned drum", "steel drum", "meditation", "percussion", "tuned", "instrument"])
def _(S):
    body = ("M2.5 13C2.5 8 7 6 12 6C17 6 21.5 8 21.5 13C21.5 15.5 17 17 12 17C7 17 2.5 15.5 2.5 13Z" if S.name == "rounded"
            else "M2.5 13.5L4 10.5C6 7.5 9 6 12 6C15 6 18 7.5 20 10.5L21.5 13.5L19.5 16C17.5 16.8 14.5 17 12 17C9.5 17 6.5 16.8 4.5 16Z")
    return [shell(body), dot(12, 10.5, 2), dot(6.5, 13, 1), dot(17.5, 13, 1)]


@icon("steel-tongue-drum", CAT, "Steel tongue drum seen from above with tongues cut around the centre",
      tags=["tank drum", "tuned percussion", "meditation", "handpan", "percussion", "instrument"])
def _(S):
    parts = [shell(circle(12, 12, 9.5))]
    for k in range(6):
        a = math.radians(-90 + 60 * k)
        parts.append(detail(seg(12 + 3.5 * math.cos(a), 12 + 3.5 * math.sin(a), 12 + 6.75 * math.cos(a), 12 + 6.75 * math.sin(a))))
    return parts + [dot(12, 12, 1.5)]


@icon("udu", CAT, "Udu: a round clay pot drum with a neck opening and a hole in its side",
      tags=["clay drum", "pot drum", "nigeria", "african", "percussion", "instrument"])
def _(S):
    body = outline(circle(12, 14.5, 7.5), rect(9, 3.5, 6, 8, rnd(S, 0.5, 2)))
    return [shell(body), dot(9.5, 15.5, 2), detail(seg(9, 6, 15, 6))]


@icon("damaru", CAT, "Damaru: a small hourglass drum with knotted cords swinging from its waist",
      tags=["shiva drum", "hindu", "tibetan", "hourglass drum", "percussion", "instrument"])
def _(S):
    return [shell(ellipse(12, 4.5, 6.5, 1.75)), shell(ellipse(12, 19.5, 6.5, 1.75)),
            line(poly([(5.5, 4.5), (11, 12), (5.5, 19.5)], r=S.r * 2)), line(poly([(18.5, 4.5), (13, 12), (18.5, 19.5)], r=S.r * 2)),
            line(seg(13, 12, 18.5, 12)), line(seg(11, 12, 5.5, 12)),
            Part("dot", rect(18.5, 10.5, 3, 3)) if S.name == "line" else dot(20, 12, 1.6),
            Part("dot", rect(2.5, 10.5, 3, 3)) if S.name == "line" else dot(4, 12, 1.6)]


@icon("angklung", CAT, "Angklung: a bamboo frame holding two tuned bamboo tubes of different lengths",
      tags=["bamboo", "indonesian", "shaken", "rattle", "percussion", "instrument"])
def _(S):
    return [line(poly([(3, 3), (3, 21.5), (21, 21.5), (21, 3), (3, 3)], r=S.r)),
            shell(rect(7, 5.5, 3, 12, rnd(S, 0.5, 1.5))), shell(rect(14, 5.5, 3, 8, rnd(S, 0.5, 1.5)))]


@icon("kalimba", CAT, "Kalimba: a wooden board with a row of metal tines and a round sound hole",
      tags=["thumb piano", "mbira", "african", "tines", "lamellophone", "instrument"])
def _(S):
    return [shell(rect(3.5, 2.5, 17, 19, rnd(S, 1.5, 3.5))), detail(seg(7, 7.5, 7, 14)), detail(seg(12, 5, 12, 14)),
            detail(seg(17, 7.5, 17, 14)), detail(seg(5.5, 14, 18.5, 14)), dot(12, 18.25, 1.6)]


@icon("balafon", CAT, "Balafon: wooden bars on a frame with round gourd resonators hanging below",
      tags=["african xylophone", "gyil", "marimba", "gourd", "percussion", "instrument"])
def _(S):
    parts = [line(seg(2.5, 11, 21.5, 11))]
    for x, top in ((4.75, 3), (12, 3), (19.25, 3)):
        parts += [shell(rect(x - 1.75, top, 3.5, 6.5, rnd(S, 0.5, 1.5))), line(seg(x, 11, x, 14.5)), dot(x, 17.75, 2.75)]
    return parts


@icon("vibraslap", CAT, "Vibraslap: a bent rod with a ball at one end and a toothed box at the other",
      tags=["percussion", "rattle", "sound effect", "jawbone", "latin", "instrument"])
def _(S):
    return [line(poly([(4.5, 5), (4.5, 19.5), (16.5, 19.5), (16.5, 17)], r=S.r)), dot(4.5, 4.5, 2.25),
            shell(rect(11.5, 6.5, 10, 10.5, rnd(S, 1, 2))), detail(seg(14.75, 9.5, 14.75, 14)), detail(seg(18.25, 9.5, 18.25, 14))]


@icon("pellet-drum", CAT, "Pellet drum: a small hand drum on a stick with two beads on cords",
      tags=["rattle drum", "tibetan", "handle drum", "percussion", "shaman", "instrument"])
def _(S):
    return [shell(circle(12, 8, 5.5)), line("M6.5 8C3 9 3 12 4 15"), line("M17.5 8C21 9 21 12 20 15"),
            dot(4, 16.5, 1.75), dot(20, 16.5, 1.75), line(seg(12, 13.5, 12, 21.5))]


@icon("egg-shaker", CAT, "Egg shaker: an egg-shaped rattle with motion arcs beside it",
      tags=["maraca", "rhythm egg", "shaker", "percussion", "rattle", "instrument"])
def _(S):
    egg = rpath([("M", (12, 5.5)), ("C", (15.5, 5.5), (18.25, 10), (18.25, 14.5)), ("C", (18.25, 18.5), (15.5, 21), (12, 21)),
                 ("C", (8.5, 21), (5.75, 18.5), (5.75, 14.5)), ("C", (5.75, 10), (8.5, 5.5), (12, 5.5)), ("Z",)], 25, 12, 13)
    return [shell(egg), dot(11, 14, 1), dot(14, 17, 1), line(arc(12, 13, 9.75, 150, 210)), line(arc(12, 13, 9.75, -30, 30))]


@icon("drum-pad", CAT, "Drum pad controller: a square with rubber pads and a row of knobs above",
      tags=["pad controller", "sampler", "beat maker", "midi", "electronic drums", "production"])
def _(S):
    parts = [shell(rect(2.5, 2.5, 19, 19, rnd(S, 2, 4))), dot(7, 6.5, 1.25), dot(12, 6.5, 1.25), dot(17, 6.5, 1.25)]
    for y in (10.5, 15.5):
        for x in (5.5, 10.5, 15.5):
            parts.append(Part("dot", rect(x, y, 3, 3, rnd(S, 0.3, 1))))
    return parts


@icon("drum-machine", CAT, "Drum machine: a box with a small screen, a knob and a row of step buttons",
      tags=["beat box", "sequencer", "rhythm machine", "electronic", "beat maker", "production"])
def _(S):
    k = rnd(S, 0.3, 1)
    return [shell(rect(2.5, 4.5, 19, 15, rnd(S, 2, 4))), Part("dot", rect(5, 7.5, 7, 3, k)), dot(17, 9, 1.5),
            Part("dot", rect(5, 13.5, 3, 3, k)), Part("dot", rect(10.5, 13.5, 3, 3, k)), Part("dot", rect(16, 13.5, 3, 3, k))]


@icon("sistrum", CAT, "Sistrum: an arched metal frame with loose rods and jingles on a handle",
      tags=["ancient egypt", "rattle", "isis", "jingles", "percussion", "ritual"])
def _(S):
    return [line("M6.5 16V9A5.5 5.5 0 0 1 17.5 9V16"), line(seg(5, 16, 19, 16)), line(seg(3.5, 8.5, 20.5, 8.5)),
            line(seg(3.5, 12.5, 20.5, 12.5)), shell(rect(10.5, 16, 3, 5.5, rnd(S, 0.5, 1.5)))]


@icon("wooden-fish-drum", CAT, "Wooden fish drum: a round hollow block with a slit mouth, a handle loop and a small mallet",
      tags=["muyu", "temple block", "buddhist", "chanting", "percussion", "mokugyo"])
def _(S):
    return [shell(circle(10.5, 14, 7.5)), line(circle(10.5, 4, 2)), detail(seg(5.25, 15.5, 15.75, 15.5)),
            dot(7.5, 11, 1.1), line(seg(20.5, 4.5, 17, 8.5)), dot(20.5, 4, 1.5)]


@icon("glass-harp", CAT, "Glass harp: wine glasses filled to different levels, played by rubbing the rims",
      tags=["glass armonica", "wine glasses", "water glasses", "singing glasses", "tuned glasses", "rim tone"])
def _(S):
    def glass(x, level):
        return [shell(f"M{x - 3} 4.5H{x + 3}C{x + 3} 9 {x + 1.75} 11.5 {x} 11.5C{x - 1.75} 11.5 {x - 3} 9 {x - 3} 4.5Z"),
                line(seg(x, 11.5, x, 19.5)), line(seg(x - 3.25, 20.5, x + 3.25, 20.5)), detail(seg(x - 3, level, x + 3, level))]
    return glass(6.5, 8.5) + glass(17.5, 6.5)


@icon("bell-lyre", CAT, "Bell lyre: a marching glockenspiel with metal bars in a lyre frame on a pole",
      tags=["glockenspiel", "marching band", "orchestra bells", "percussion", "xylophone", "lyre"])
def _(S):
    return [line("M4 2.5C2.5 9 6 16 12 16C18 16 21.5 9 20 2.5"), line(seg(8, 6.5, 8, 12)), line(seg(12, 3.5, 12, 12)),
            line(seg(16, 6.5, 16, 12)), line(seg(12, 16, 12, 21.5))]


@icon("ghungroo", CAT, "Ghungroo: a strap hung with clusters of small round brass bells",
      tags=["ghungru", "anklet", "dance bells", "kathak", "indian dance", "jingle"])
def _(S):
    parts = [shell(rect(2.5, 3.5, 19, 4.5, rnd(S, 1, 2)))]
    for x in (4.5, 9.5, 14.5, 19.5):
        parts += [line(seg(x, 8, x, 11.5)), dot(x, 13, 1.6)]
    for x in (7, 12, 17):
        parts += [line(seg(x, 14, x, 16.5)), dot(x, 19, 1.6)]
    return parts


@icon("drum-mallet", CAT, "Drum mallet: a stick with a round felt head",
      tags=["timpani mallet", "marimba", "percussion", "beater", "drumstick", "felt"])
def _(S):
    return [line(seg(3.5, 20.5, 13.5, 10.5)), shell(circle(16.75, 7.25, 4.5))]


@icon("kick-drum-pedal", CAT, "Kick drum pedal: a foot plate with a hinged arm and a beater head",
      tags=["bass drum pedal", "drum kit", "drummer", "foot pedal", "percussion", "beater"])
def _(S):
    return [shell(poly([(2.5, 15.5), (13, 19), (13, 21.5), (2.5, 21.5)], True, S.r)), line(seg(14.5, 19, 17.5, 8.5)),
            shell(circle(18, 5.25, 2.75))]


# ============================================================================ notation: clefs and accidentals

@icon("treble-clef", CAT, "Treble clef: a tall G clef with a looping spiral around its stem",
      tags=["g clef", "clef", "sheet music", "notation", "staff", "score"])
def _(S):
    hook = dot(7.5, 19.5, 1.4) if S.name == "rounded" else Part("dot", rect(6.25, 18.25, 2.6, 2.6))
    return [line("M12.5 2V18C12.5 21 9 21.5 8 19.75"), hook, line("M12.5 2C16.5 3.5 17.5 7.5 15 10"),
            line("M12.5 17.5C6 18.5 4 10 9.5 9.5C15 9 18 13 16 15.5")]


@icon("bass-clef", CAT, "Bass clef: a curl that sweeps down to a point with two dots beside it",
      tags=["f clef", "clef", "sheet music", "notation", "staff", "score"])
def _(S):
    return [line("M6.5 9.5C6.5 5.5 9.5 3.5 12 3.5C15.5 3.5 17 6 17 8.5C17 14 12.5 18.5 4.5 21.5"), dot(6.5, 9.5, 2.25),
            dot(20.5, 6.25, 1.3), dot(20.5, 11.75, 1.3)]


@icon("alto-clef", CAT, "Alto clef: a C clef of two facing curves on a thick and a thin bar",
      tags=["c clef", "viola clef", "clef", "sheet music", "notation", "score"])
def _(S):
    return [Part("solid", rect(3, 3, 3.5, 18)), line(seg(9.25, 3, 9.25, 21)),
            line("M11.5 3.5C17 3.5 19.5 6.5 17.5 9C16 10.8 13.5 11 11.5 12C13.5 13 16 13.2 17.5 15C19.5 17.5 17 20.5 11.5 20.5")]


@icon("percussion-clef", CAT, "Percussion clef: two thick vertical bars between five staff lines",
      tags=["neutral clef", "unpitched", "drums", "notation", "staff", "score"])
def _(S):
    parts = []
    for y in (4, 8, 12, 16, 20):
        parts += [line(seg(2.5, y, 6, y)), line(seg(18, y, 21.5, y))]
    return parts + [Part("solid", rect(8.25, 4, 2.75, 16)), Part("solid", rect(13, 4, 2.75, 16))]




@icon("sharp-sign", CAT, "Sharp sign: two upright strokes crossed by two rising bars",
      tags=["accidental", "raise pitch", "semitone", "notation", "sheet music", "hash"])
def _(S):
    k = rnd(S, 0, 0.75)
    return [line(seg(9, 3, 9, 21)), line(seg(15, 3, 15, 21)),
            Part("solid", poly([(4, 11.25), (20, 7.25), (20, 10.25), (4, 14.25)], True, k)),
            Part("solid", poly([(4, 17), (20, 13), (20, 16), (4, 20)], True, k))]


@icon("flat-sign", CAT, "Flat sign: a tall upright stroke with a rounded bowl at the bottom right",
      tags=["accidental", "lower pitch", "semitone", "notation", "sheet music", "b"])
def _(S):
    return [line(seg(8.5, 2.5, 8.5, 20.5)), shell("M8.5 20.5C13 18.5 18 16 17.5 12.5C17 9.5 11 10 8.5 14.5Z")]


@icon("natural-sign", CAT, "Natural sign: two offset upright strokes joined by a slanted box",
      tags=["accidental", "cancel accidental", "notation", "sheet music", "pitch", "score"])
def _(S):
    return [line(seg(9, 2.5, 9, 10)), line(seg(15, 14.5, 15, 21.5)),
            shell(poly([(9, 10), (15, 8.5), (15, 14.5), (9, 16)], True, S.r * 0.5))]


@icon("double-sharp", CAT, "Double sharp: a small bold X with square ends",
      tags=["accidental", "raise two semitones", "notation", "sheet music", "pitch", "x"])
def _(S):
    k = rnd(S, 0, 1)
    parts = [line(seg(5.5, 5.5, 18.5, 18.5)), line(seg(18.5, 5.5, 5.5, 18.5))]
    for x, y in ((3, 3), (16, 3), (3, 16), (16, 16)):
        parts.append(Part("solid", rect(x, y, 5, 5, k)))
    return parts


@icon("double-flat", CAT, "Double flat: two flat signs side by side",
      tags=["accidental", "lower two semitones", "notation", "sheet music", "pitch", "bb"])
def _(S):
    def flat(x):
        return [line(seg(x, 2.5, x, 20.5)),
                shell(f"M{x} 20.5C{x + 3} 19 {x + 5.5} 17 {x + 5.25} 14.5C{x + 5} 12.25 {x + 1.25} 12.25 {x} 15.25Z")]
    return flat(5.5) + flat(14)


# ============================================================================ notation: notes, rests and signs

def _head(S, cx, cy, rx, ry, deg):
    """Tilted oval note head; Rounded is a true ellipse, Line a squarer superellipse."""
    if S.name == "rounded":
        return rell(cx, cy, rx, ry, deg, cx, cy)
    pts = []
    n = 2.8
    for k in range(24):
        t = 2 * math.pi * k / 24
        c, sn = math.cos(t), math.sin(t)
        pts.append((cx + rx * math.copysign(abs(c) ** (2 / n), c), cy + ry * math.copysign(abs(sn) ** (2 / n), sn)))
    return poly(rot(pts, deg, cx, cy), closed=True)


def _open_head_filled(cx, cy, rx, ry, deg, extra=None):
    def f():
        outer = P(rell(cx, cy, rx + 1, ry + 1, deg, cx, cy))
        hole = P(rell(cx, cy, rx * 0.5, ry * 0.85, deg + 55, cx, cy))
        body = D(outer, hole)
        return U(body, *extra) if extra else body
    return f


_WHOLE_F = _open_head_filled(12, 12, 7.5, 4.25, -20)


@icon("whole-note", CAT, "Whole note: an open oval note head with no stem",
      tags=["semibreve", "note", "sheet music", "notation", "rhythm", "duration"], filled=_WHOLE_F)
def _(S):
    return [shell(_head(S, 12, 12, 7.5, 4.25, -20))]


_HALF_F = _open_head_filled(9, 16.5, 5.5, 3.6, -20, extra=[ST("M14.25 16.5V3", 2.5, "butt", "miter", 4)])


@icon("half-note", CAT, "Half note: an open oval note head with a straight stem",
      tags=["minim", "note", "sheet music", "notation", "rhythm", "duration"], filled=_HALF_F)
def _(S):
    return [shell(_head(S, 9, 16.5, 5.5, 3.6, -20)), line(seg(14.5, 16.5, 14.5, 3))]


def _quarter_filled():
    return U(P(rell(9, 16.5, 6, 4.25, -20, 9, 16.5)), ST("M14 16.5V3", 2.5, "butt", "miter", 4))


@icon("quarter-note", CAT, "Quarter note: a solid oval note head with a straight stem",
      tags=["crotchet", "note", "sheet music", "notation", "rhythm", "beat"], filled=_quarter_filled)
def _(S):
    return [Part("solid", rell(9, 16.5, 5.75, 4, -20, 9, 16.5)), line(seg(13.75, 16.5, 13.75, 3))]


@icon("whole-rest", CAT, "Whole rest: a small solid bar hanging below a staff line",
      tags=["semibreve rest", "rest", "silence", "notation", "sheet music", "pause"])
def _(S):
    k = rnd(S, 0, 0.6)
    return [line(seg(2.5, 6, 21.5, 6)), line(seg(2.5, 12, 21.5, 12)), line(seg(2.5, 18, 21.5, 18)),
            Part("solid", rect(8, 6, 8, 3, k))]


@icon("half-rest", CAT, "Half rest: a small solid bar sitting on top of a staff line",
      tags=["minim rest", "rest", "silence", "notation", "sheet music", "pause"])
def _(S):
    k = rnd(S, 0, 0.6)
    return [line(seg(2.5, 6, 21.5, 6)), line(seg(2.5, 12, 21.5, 12)), line(seg(2.5, 18, 21.5, 18)),
            Part("solid", rect(8, 9, 8, 3, k))]


@icon("quarter-rest", CAT, "Quarter rest: a zigzag stroke ending in a hooked curl",
      tags=["crotchet rest", "rest", "silence", "notation", "sheet music", "pause"])
def _(S):
    return [line(poly([(9.5, 2.5), (14.5, 8.5), (9.5, 14)], r=S.r * 0.8)),
            line("M9.5 14C15.5 14 16.5 18 14 20C12.5 21.25 10.5 20.5 10.5 18.5")]


@icon("eighth-rest", CAT, "Eighth rest: a slanted stroke with a dot and a hook at the top",
      tags=["quaver rest", "rest", "silence", "notation", "sheet music", "pause"])
def _(S):
    return [dot(7.5, 8, 2.25), line("M7.5 8C10.5 10 13.5 9 15.5 5"), line(seg(15.5, 5, 9.5, 21.5))]


@icon("fermata", CAT, "Fermata: a semicircular arch with a dot beneath its middle",
      tags=["pause", "hold", "bird's eye", "notation", "sheet music", "sustain"])
def _(S):
    return [line(arc(12, 16, 9, 180, 360)), dot(12, 15.25, 1.75)]


@icon("repeat-sign", CAT, "Repeat sign: a thin and a thick barline with two dots to their left",
      tags=["repeat", "barline", "end repeat", "notation", "sheet music", "reprise"])
def _(S):
    return [dot(6.5, 9.25, 1.5), dot(6.5, 14.75, 1.5), line(seg(11.5, 3, 11.5, 21)),
            Part("solid", rect(15, 3, 3.5, 18, rnd(S, 0, 0.6)))]


@icon("volta-bracket", CAT, "Volta bracket: an ending bracket with a hook down to a barline and the number 1",
      tags=["first ending", "repeat", "ending", "notation", "sheet music", "score"])
def _(S):
    return [line(poly([(3.5, 21.5), (3.5, 4.5), (21, 4.5)], r=S.r)), line(poly([(8, 12.5), (10.5, 10), (10.5, 19)], r=S.r * 0.5))]


@icon("coda-sign", CAT, "Coda sign: a circle crossed by a vertical and a horizontal line",
      tags=["coda", "jump", "ending", "notation", "sheet music", "score"])
def _(S):
    return [line(circle(12, 12, 5.5)), line(seg(12, 2.5, 12, 21.5)), line(seg(2.5, 12, 21.5, 12))]


@icon("segno", CAT, "Segno: a slanted S crossed by a diagonal stroke with a dot on each side",
      tags=["sign", "repeat", "d.s.", "notation", "sheet music", "score"])
def _(S):
    return [line("M17 6C14 3 8 4 8.5 8C9 11.5 15.5 12.5 15.5 16C15.5 20 9 21 6.5 18"), line(seg(19, 3.5, 5, 20.5)),
            dot(4.5, 9, 1.4), dot(19.5, 15, 1.4)]


@icon("crescendo", CAT, "Crescendo: a hairpin opening from a point on the left to wide on the right",
      tags=["getting louder", "dynamics", "hairpin", "notation", "sheet music", "swell"])
def _(S):
    return [line(poly([(21, 5), (5, 13), (21, 21)], r=S.r))]


@icon("decrescendo", CAT, "Decrescendo: a hairpin starting wide on the left and closing to a point on the right",
      tags=["diminuendo", "getting softer", "dynamics", "hairpin", "notation", "sheet music"])
def _(S):
    return [line(poly([(3, 3), (19, 11), (3, 19)], r=S.r))]


def _nhead(cx, cy, rx=3.25, ry=2.4, deg=-20):
    """Solid oval note head."""
    return Part("solid", rell(cx, cy, rx, ry, deg, cx, cy))


@icon("dynamic-forte", CAT, "Dynamic forte: a bold italic letter f as written under music for loud",
      tags=["f", "loud", "dynamics", "notation", "sheet music", "strong"])
def _(S):
    return [line("M18 3.5C14.5 2 12 3.5 11 7.5L7.25 19.5C6.75 21.25 5 21.5 4 20.5"), line(seg(6.5, 11.5, 15.5, 11.5))]


@icon("dynamic-piano", CAT, "Dynamic piano: a bold italic letter p as written under music for soft",
      tags=["p", "soft", "quiet", "dynamics", "notation", "sheet music"])
def _(S):
    return [line(seg(9.5, 8.5, 6, 21.5)), line("M9 11.5C12 7.5 18.5 8 18 12.5C17.5 16.5 12.5 17 8.25 14.5")]


@icon("slur-mark", CAT, "Slur: two note heads joined by a long gentle arc above them",
      tags=["legato", "phrase", "tie", "notation", "sheet music", "smooth"])
def _(S):
    return [line("M5.5 12.5C8 3 16 3 18.5 12.5"), _nhead(6, 17.5), _nhead(18, 17.5)]


@icon("trill-mark", CAT, "Trill: the letters tr above a wavy line",
      tags=["ornament", "tr", "shake", "notation", "sheet music", "embellishment"])
def _(S):
    wave = "q1.5 -3 3 0t3 0t3 0t3 0t3 0t3 0"
    return [line("M6 3V11C6 12.5 6.8 13 8 12.5"), line(seg(3.5, 6, 8.5, 6)), line(seg(11.5, 6.5, 11.5, 13)),
            line("M11.5 9C12 6.5 14 6 15 7"), line("M3 19" + wave)]


@icon("mordent", CAT, "Mordent: a short zigzag with a vertical stroke through its middle",
      tags=["ornament", "embellishment", "trill", "notation", "sheet music", "pralltriller"])
def _(S):
    return [line(poly([(3, 13.5), (7.5, 8.5), (12, 13.5), (16.5, 8.5), (21, 13.5)], r=S.r * 0.6)), line(seg(12, 3.5, 12, 20.5))]


@icon("turn-ornament", CAT, "Turn: a sideways S curl lying above a note head",
      tags=["gruppetto", "ornament", "embellishment", "notation", "sheet music", "flourish"])
def _(S):
    return [line("M3.5 10.5C3.5 5.5 9 5 12 8.5C15 12 20.5 11.5 20.5 7"), _nhead(12, 18.5, 3.5, 2.5)]


@icon("glissando", CAT, "Glissando: a wavy line sliding diagonally between a low note and a high note",
      tags=["slide", "portamento", "sweep", "notation", "sheet music", "harp"])
def _(S):
    pts = []
    for i in range(5):
        t = i / 4
        off = 0 if i in (0, 4) else (1.7 if i % 2 else -1.7)
        pts.append((8 + 8 * t + off * 0.707, 16 - 8 * t + off * 0.707))
    return [_nhead(5, 19, 3, 2.25), _nhead(19, 5, 3, 2.25), line(poly(pts, r=S.r * 0.6))]


@icon("grace-note", CAT, "Grace note: a small slashed note beside a full-size note",
      tags=["acciaccatura", "ornament", "embellishment", "notation", "sheet music", "appoggiatura"])
def _(S):
    return [_nhead(5.5, 18.5, 2.75, 2), line(seg(7.75, 18, 7.75, 8)), line(seg(4.5, 12.5, 11, 9.5)),
            _nhead(16, 17.5, 4.25, 3), line(seg(19.6, 17, 19.6, 3.5))]


@icon("triplet-notes", CAT, "Triplet: three beamed notes under a bracket with the number 3",
      tags=["tuplet", "rhythm", "three", "notation", "sheet music", "beam"])
def _(S):
    parts = [_nhead(4.5, 18.5, 2.75, 2), _nhead(11.25, 18.5, 2.75, 2), _nhead(18, 18.5, 2.75, 2)]
    for x in (6.6, 13.35, 20.1):
        parts.append(line(seg(x, 18, x, 11.5)))
    parts.append(Part("solid", rect(6.25, 11, 14.5, 2.5)))
    parts += [line(poly([(5, 8), (5, 4), (9.5, 4)], r=S.r * 0.4)), line(poly([(15, 4), (20, 4), (20, 8)], r=S.r * 0.4)),
              line("M10.5 3H13.5L12 5.25C14 5.25 14.5 8 12.25 8.25C11.25 8.4 10.5 7.9 10.25 7.25")]
    return parts


@icon("breath-mark", CAT, "Breath mark: a comma shape above the top line of a staff",
      tags=["pause", "phrase", "breathe", "notation", "sheet music", "luftpause"])
def _(S):
    return [dot(14, 5.5, 2), line("M14.25 5.5C14.5 9 13 11.5 10.25 13.5"), line(seg(3, 19, 21, 19))]


@icon("caesura", CAT, "Caesura: two slanted strokes marking a break in the music",
      tags=["railroad tracks", "pause", "break", "notation", "sheet music", "stop"])
def _(S):
    return [line(seg(6, 21, 11, 3)), line(seg(13, 21, 18, 3))]


@icon("final-barline", CAT, "Final barline: a thin line beside a thick line closing the staff",
      tags=["double bar", "end", "staff", "notation", "sheet music", "finish"])
def _(S):
    parts = [line(seg(2.5, y, 16, y)) for y in (4, 8, 12, 16, 20)]
    return parts + [line(seg(16, 4, 16, 20)), Part("solid", rect(19, 3.5, 2.75, 17, rnd(S, 0, 0.6)))]


def _four(y0):
    return [line(seg(14, y0, 14, y0 + 7.5)), line(poly([(14, y0), (6.5, y0 + 5.25), (17.5, y0 + 5.25)]))]


@icon("time-signature", CAT, "Time signature: a 4 stacked over a 4",
      tags=["meter", "4/4", "beats per bar", "notation", "sheet music", "rhythm"])
def _(S):
    return [line(poly([(14, 2.5), (6.5, 7.75), (17.5, 7.75)], r=S.r * 0.4)), line(seg(14, 2.5, 14, 10)),
            line(poly([(14, 14), (6.5, 19.25), (17.5, 19.25)], r=S.r * 0.4)), line(seg(14, 14, 14, 21.5))]


@icon("common-time", CAT, "Common time: a large C time signature after a barline",
      tags=["4/4", "meter", "time signature", "notation", "sheet music", "rhythm"])
def _(S):
    return [line(seg(3.5, 4, 3.5, 20)), line(arc(14, 12, 6.5, 40, 320))]


@icon("cut-time", CAT, "Cut time: a C time signature with a vertical line struck through it",
      tags=["alla breve", "2/2", "meter", "time signature", "notation", "sheet music"])
def _(S):
    return [line(seg(3.5, 4, 3.5, 20)), line(arc(14, 12, 6.5, 40, 320)), line(seg(14, 3, 14, 21))]


@icon("pedal-marking", CAT, "Pedal marking: a letter P followed by an asterisk release mark",
      tags=["ped", "sustain pedal", "piano", "notation", "sheet music", "release"])
def _(S):
    return [line(poly([(5, 20), (5, 4), (9, 4)], r=S.r * 0.4)), line("M9 4C13.5 4 13.5 12 9 12H5"),
            line(seg(17.5, 12.5, 17.5, 19.5)), line(seg(14.25, 14.25, 20.75, 17.75)), line(seg(20.75, 14.25, 14.25, 17.75))]


@icon("octave-marking", CAT, "Octave marking: the number 8 followed by a dashed line ending in a hook",
      tags=["8va", "ottava", "octave higher", "notation", "sheet music", "transpose"])
def _(S):
    return [line(circle(5.5, 5, 1.75)), line(circle(5.5, 9.75, 2.25)), line(seg(10.5, 7, 13, 7)), line(seg(15, 7, 17.5, 7)),
            line(poly([(19.5, 7), (21.25, 7), (21.25, 12)], r=S.r * 0.5)), _nhead(12, 18.5, 3.5, 2.5)]
