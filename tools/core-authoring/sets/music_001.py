"""TypeIcon Core: musical instruments (music batch 001).

Strings, keyboards, winds, brass and drums drawn from the instruments themselves. Long instruments
either stand upright or lie on the 45° diagonal (body to the bottom-left, head to the top-right),
like the guitar family in media.py. Bows and beaters that cross a body are drawn over it: the Filled
style cuts a thin gap either side so they stay readable.
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
    """Rotate points clockwise on screen about (cx, cy)."""
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


def outline(*ds) -> str:
    """One closed outline from the union of several closed shapes."""
    return path_to_d(U(*[P(d) for d in ds]))


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


def over_filled(draw, over_ds, gap=1.25):
    """Filled design where the open strokes `over_ds` (bows, beaters) lie across the body with a gap."""
    def f():
        base = filled_region(draw(LINE, False))
        cut = U(*[ST(d, 2.5 + 2 * gap, "round", "round") for d in over_ds])
        return U(D(base, cut), *[ST(d, 2.5) for d in over_ds])
    return f


def scroll(S, x, y_from, y_top):
    """Violin-family neck ending in a scroll (hooked in Rounded, squared in Line)."""
    if S.name == "rounded":
        return line(f"M{fmt(x)} {fmt(y_from)}V{fmt(y_top + 1.25)}C{fmt(x)} {fmt(y_top)} {fmt(x + 1)} {fmt(y_top - 0.5)} {fmt(x + 2)} {fmt(y_top)}")
    return line(f"M{fmt(x)} {fmt(y_from)}V{fmt(y_top)}H{fmt(x + 2)}")


# ============================================================================ bowed and plucked strings

_CELLO_BOW = seg(17.75, 2.5, 20.25, 19.5)


def _cello(S, bow=True):
    body = outline(ellipse(10, 9.5, 4, 3.25), ellipse(10, 15.25, 5, 4.25))
    parts = [shell(body), detail(seg(10, 6.25, 10, 12.5)), detail(seg(8.5, 15.5, 11.5, 15.5)), scroll(S, 10, 6.25, 2.5),
             line(seg(10, 19.5, 10, 22))]
    if bow:
        parts += [line(_CELLO_BOW), shell(poly([(18.2, 17.5), (20.6, 17.1), (21, 19.9), (18.6, 20.3)], closed=True, r=S.r * 0.3))]
    return parts


@icon("cello", CAT, "Cello standing on its endpin with its bow leaning beside it",
      tags=["violoncello", "strings", "orchestra", "bow", "classical", "instrument"])
def _(S):
    return _cello(S)


_BASS = sym(12, (12, 7.5), [((13.6, 7.5), (15, 9.2), (15.6, 11.2)), ((16, 12.4), (14.9, 12.9), (14.9, 13.8)),
                             ((14.9, 14.6), (17.5, 15.2), (17.5, 17.4)), ((17.5, 19.6), (15, 20.25), (12, 20.25))])


@icon("double-bass", CAT, "Tall upright double bass with sloped shoulders, f-holes and an endpin",
      tags=["upright bass", "contrabass", "string bass", "jazz", "orchestra", "instrument"],
      aliases=["upright-bass", "contrabass"])
def _(S):
    return [shell(_BASS), detail(seg(12, 7.5, 12, 13)), detail(seg(10, 15.5, 10, 18)), detail(seg(14, 15.5, 14, 18)),
            scroll(S, 12, 7.5, 2), line(seg(12, 20.25, 12, 22))]


@icon("violin-bow", CAT, "Violin bow: a long stick with the hair beneath and a frog at the grip end",
      tags=["bow", "fiddle bow", "strings", "orchestra", "string instrument", "cello bow"])
def _(S):
    k = S.r * 0.5
    return [line(rp([(10, 24.5), (10, 0), (14, 2), (14, 18)], closed=False, r=k)),
            shell(rp([(10, 18), (14.5, 18), (14.5, 21.5), (10, 21.5)], r=min(S.R, 1) * 0.5))]


@icon("lyre", CAT, "Lyre: two curved arms joined by a crossbar with strings down to a sound box",
      tags=["ancient greek", "harp", "strings", "apollo", "poetry", "instrument"])
def _(S):
    arm_l = "M8 17.5C4 16 3 11 4.5 8C5.3 6.4 5.3 4.8 4 3"
    arm_r = "M16 17.5C20 16 21 11 19.5 8C18.7 6.4 18.7 4.8 20 3"
    return [shell(rect(6, 17, 12, 4.5, min(S.R, 2))), line(arm_l), line(arm_r), line(seg(4.5, 6.5, 19.5, 6.5)),
            line(seg(9, 6.5, 9, 17)), line(seg(12, 6.5, 12, 17)), line(seg(15, 6.5, 15, 17))]


@icon("lute", CAT, "Lute: rounded pear-shaped body with a rosette and a pegbox bent back",
      tags=["renaissance", "medieval", "strings", "oud", "baroque", "instrument"])
def _(S):
    body = rpath([("M", (11, 8.5)), ("C", (8.5, 11.5), (6.5, 14), (6.5, 17.5)), ("C", (6.5, 21), (9, 23), (12, 23)),
                  ("C", (15, 23), (17.5, 21), (17.5, 17.5)), ("C", (17.5, 14), (15.5, 11.5), (13, 8.5)), ("Z",)])
    peg = rp([(12, 8.5), (12, 3), (15.5, 3)], closed=False, r=S.r * 0.6)
    return [shell(body), detail(rcircle(12, 15.5, 1.75)), detail(rseg(10, 19.5, 14, 19.5)), line(peg)]


@icon("mandolin", CAT, "Mandolin: teardrop body with an oval sound hole and a flat headstock",
      tags=["strings", "folk", "bluegrass", "italian", "plucked", "instrument"])
def _(S):
    body = "M12 9.5C14.2 11.2 17 12.5 17 16.5A5 5 0 0 1 7 16.5C7 12.5 9.8 11.2 12 9.5Z"
    return [shell(body), detail(ellipse(12, 15.75, 1.5, 2)), line(seg(12, 9.5, 12, 6)),
            shell(rect(10.25, 2, 3.5, 4, min(S.R, 1))), line(seg(7.5, 4, 10.25, 4)), line(seg(13.75, 4, 16.5, 4))]


@icon("banjo", CAT, "Banjo: round drum body, long neck and a short fifth-string peg",
      tags=["bluegrass", "country", "folk", "strings", "plucked", "instrument"])
def _(S):
    c = (7.5, 16.5)

    def al(t, p=0.0):
        return (c[0] + t * 0.7071 + p * 0.7071, c[1] - t * 0.7071 + p * 0.7071)
    head = rp([al(13, -1.3), al(13, 1.3), al(17.5, 1.3), al(17.5, -1.3)], deg=0, r=S.r * 0.4)
    return [shell(circle(*c, 5.5)), detail(circle(*c, 3)), line(seg(*al(5.5), *al(13))), shell(head),
            line(seg(*al(9), *al(9, -2.5)))]


@icon("ukulele", CAT, "Ukulele: small figure-eight body, short neck and four tuning pegs",
      tags=["uke", "hawaiian", "strings", "small guitar", "plucked", "instrument"], aliases=["uke"])
def _(S):
    body = outline(circle(12, 17.5, 4.5), circle(12, 11.75, 3.25))
    return [shell(body), dot(12, 14, 1.25), line(seg(12, 8.5, 12, 6.5)), shell(rect(10.5, 2, 3, 4.5, min(S.R, 1))),
            dot(8.25, 3, 0.9), dot(8.25, 5.5, 0.9), dot(15.75, 3, 0.9), dot(15.75, 5.5, 0.9)]


def _axis(c, t, p=0.0):
    """Point t along the 45° guitar axis (up-right) from c, offset p across it (down-right positive)."""
    return (c[0] + (t + p) * 0.7071, c[1] + (p - t) * 0.7071)


@icon("bass-guitar", CAT, "Electric bass guitar: offset body, extra-long neck and four tuners",
      tags=["bass", "electric bass", "four string", "band", "rock", "instrument"], aliases=["electric-bass"])
def _(S):
    body = outline(rcircle(12, 19.5, 4), rpath([("M", (8.3, 18)), ("C", (7.8, 15.5), (8.2, 13), (9.6, 13)),
                                                       ("C", (10.8, 13), (11.2, 15), (11.2, 17)), ("Z",)]),
                   rpath([("M", (12.8, 17)), ("C", (13.2, 15.6), (14, 14.6), (14.9, 14.9)),
                          ("C", (15.9, 15.3), (15.9, 17), (15.5, 18.5)), ("Z",)]))
    head = rp([(11, -0.5), (13, -0.5), (13, 2.5), (11, 2.5)], r=S.r * 0.4)
    return [shell(body), detail(rseg(10.5, 19.5, 13.5, 19.5)), line(rseg(12, 15.5, 12, 2.5)), shell(head),
            line(rseg(13, 1, 15, 1)), line(rseg(9, 1, 11, 1))]


@icon("double-neck-guitar", CAT, "Electric guitar with two parallel necks rising from one body",
      tags=["twin neck", "double neck", "rock", "electric guitar", "twelve string", "instrument"], aliases=["twin-neck-guitar"])
def _(S):
    body = rpath([("M", (7.5, 16)), ("C", (8.5, 16.5), (9, 17), (10, 17)), ("L", (14, 17)), ("C", (15, 17), (15.5, 16.5), (16.5, 16)),
                  ("C", (17.5, 18), (17.5, 20), (16.5, 21.3)), ("C", (15.5, 22.5), (14, 23), (12, 23)),
                  ("C", (10, 23), (8.5, 22.5), (7.5, 21.3)), ("C", (6.5, 20), (6.5, 18), (7.5, 16)), ("Z",)])
    return [shell(body), detail(rseg(9.5, 20, 14.5, 20)), line(rseg(10, 17, 10, 3)), line(rseg(14, 17, 14, 3)),
            solid(rp([(8.75, 0.5), (11.25, 0.5), (11.25, 3.5), (8.75, 3.5)], r=rnd(S, 0, 0.6))),
            solid(rp([(12.75, 0.5), (15.25, 0.5), (15.25, 3.5), (12.75, 3.5)], r=rnd(S, 0, 0.6)))]


@icon("resonator-guitar", CAT, "Acoustic guitar with a large round metal resonator plate on its body",
      tags=["resonator", "metal body", "slide guitar", "blues", "bluegrass", "instrument"])
def _(S):
    body = outline(circle(12, 16.25, 5.75), circle(12, 9.5, 4))
    return [shell(body), detail(circle(12, 16, 3.25)), dot(12, 16, 1), line(seg(12, 5.5, 12, 3.5)),
            solid(rect(10.5, 1.75, 3, 2.5, rnd(S, 0, 0.8)))]


@icon("balalaika", CAT, "Balalaika: triangular body, small sound hole and a long neck",
      tags=["russian", "folk", "strings", "triangle guitar", "plucked", "instrument"])
def _(S):
    body = poly([(12, 10), (20, 21), (4, 21)], closed=True, r=rnd(S, 0.6, 2))
    return [shell(body, stroke_miterlimit="2"), detail(circle(12, 16.75, 1.5)), line(seg(12, 10, 12, 5.5)),
            shell(rect(10.5, 2, 3, 3.5, min(S.R, 1)))]


@icon("sitar", CAT, "Sitar: long wide neck with a large gourd at the bottom and a small one at the top",
      tags=["indian", "classical", "strings", "raga", "gourd", "instrument"])
def _(S):
    neck = rp([(10.5, 1), (13.5, 1), (13.5, 16), (10.5, 16)], r=S.r * 0.4)
    return [shell(outline(rcircle(12, 19.5, 5), neck)), detail(rseg(12, 16.5, 12, 22)),
            shell(rcircle(15.75, 5, 2.25)), line(rseg(10.5, 3.5, 8, 3.5)), line(rseg(10.5, 7, 8, 7))]


_ERHU_BOW = seg(3, 16, 21, 11)


def _erhu(S, bow=True):
    drum = poly(regular(12, 17, 3.25, 6, start=0), closed=True, r=S.r * 0.5)
    parts = [shell(drum), line(seg(12, 13.75, 12, 2.5)), line(seg(12, 20.25, 12, 22)),
             line(seg(8.5, 4, 12, 4)), line(seg(8.5, 7.5, 12, 7.5))]
    if bow:
        parts.append(line(_ERHU_BOW))
    return parts


@icon("erhu", CAT, "Erhu: two-string fiddle with a small drum body, tall neck, two pegs and a bow",
      tags=["chinese fiddle", "two string", "chinese", "bowed", "strings", "instrument"],
      filled=over_filled(_erhu, [_ERHU_BOW]))
def _(S):
    return _erhu(S)


@icon("shamisen", CAT, "Shamisen: small square body, long thin neck, pegs and a fan-shaped plectrum",
      tags=["japanese", "three string", "strings", "plucked", "bachi", "instrument"])
def _(S):
    bachi = rpath([("M", (17.4, 21.5)), ("L", (18.6, 21.5)), ("L", (21, 13)), ("Q", (18, 11.6), (15, 13)), ("Z",)], deg=12, cx=18, cy=17)
    return [shell(rect(4, 13.5, 9, 8, min(S.R, 2.5))), line(seg(8.5, 13.5, 8.5, 2.5)),
            line(seg(5.5, 4, 8.5, 4)), line(seg(8.5, 6.5, 11.5, 6.5)), line(seg(5.5, 9, 8.5, 9)),
            shell(bachi, stroke_miterlimit="2")]


@icon("zither", CAT, "Zither seen from above: flat box with a round sound hole, strings and a fretboard",
      tags=["concert zither", "folk", "strings", "plucked", "alpine", "instrument"])
def _(S):
    box = "M3 5.5H14.5C18.5 5.5 21 8 21 12C21 16 18.5 18.5 14.5 18.5H3Z" if S.name == "line" else \
        "M5 5.5H14.5C18.5 5.5 21 8 21 12C21 16 18.5 18.5 14.5 18.5H5A2 2 0 0 1 3 16.5V7.5A2 2 0 0 1 5 5.5Z"
    return [shell(box), detail(circle(15, 12, 2.25)), detail(seg(5.5, 9.25, 10.5, 9.25)), detail(seg(5.5, 12.5, 10.5, 12.5)),
            detail(seg(3, 15.25, 18, 15.25))]


_APPAL = sym(12, (12, 6), [((13.8, 6), (15, 7.8), (15, 9.8)), ((15, 11.6), (14.1, 12.4), (14.1, 13.8)),
                            ((14.1, 15.2), (16.25, 16), (16.25, 18.2)), ((16.25, 20.4), (14.5, 21.75), (12, 21.75))])


@icon("appalachian-dulcimer", CAT, "Appalachian dulcimer from above: long hourglass body with a centre fretboard",
      tags=["mountain dulcimer", "lap dulcimer", "folk", "strings", "fretted", "instrument"], aliases=["mountain-dulcimer"])
def _(S):
    return [shell(_APPAL), detail(seg(12, 8, 12, 20)), dot(9.75, 9.75, 0.9), dot(14.25, 9.75, 0.9),
            dot(9.6, 17.5, 0.9), dot(14.4, 17.5, 0.9), shell(rect(10.75, 2, 2.5, 4, min(S.R, 1))), line(seg(13.25, 3.5, 15, 3.5))]


@icon("morin-khuur", CAT, "Morin khuur: trapezoid body and a long neck topped by a carved horse head",
      tags=["horsehead fiddle", "mongolian", "bowed", "two string", "strings", "instrument"], aliases=["horsehead-fiddle"])
def _(S):
    body = poly([(8.5, 13.5), (15.5, 13.5), (17, 21.5), (7, 21.5)], closed=True, r=S.r * 0.6)
    head = poly([(11, 8.5), (11, 3.5), (11.75, 2), (13, 3), (16.5, 5.25), (15.75, 7), (13, 6.5), (13, 8.5)], closed=True, r=S.r * 0.4)
    return [shell(body), shell(head, stroke_miterlimit="2"), line(seg(12, 8.5, 12, 13.5)), detail(seg(12, 15.5, 12, 19.5)),
            line(seg(9, 11, 12, 11))]


@icon("ektara", CAT, "Ektara: gourd resonator with a split bamboo neck holding one string",
      tags=["one string", "baul", "bengali", "folk", "drone", "instrument"], aliases=["iktar"])
def _(S):
    return [shell(circle(12, 17.5, 4.5)), line(poly([(8.5, 14.75), (12, 4), (15.5, 14.75)], r=S.r)),
            line(seg(12, 4, 12, 2)), line(seg(9.5, 3, 14.5, 3)), detail(seg(12, 13, 12, 19))]


@icon("berimbau", CAT, "Berimbau: tall curved wooden bow with one wire string and a gourd",
      tags=["capoeira", "brazilian", "musical bow", "percussion", "gourd", "instrument"])
def _(S):
    return [line("M15 2.5C8 7 8 17 15 21.5"), line(seg(15, 2.5, 15, 21.5)), shell(circle(7, 16.5, 3)),
            line(seg(10, 16.5, 15, 16.5))]


@icon("cigar-box-guitar", CAT, "Cigar box guitar: a rectangular box body with a stick neck running through it",
      tags=["homemade guitar", "blues", "diy", "three string", "folk", "instrument"])
def _(S):
    return [shell(rect(4, 11, 16, 9, min(S.R, 2))), line(seg(12, 11, 12, 4.5)), line(seg(12, 20, 12, 22)),
            solid(rect(10.5, 2, 3, 3.5, rnd(S, 0, 0.8))), detail(seg(12, 13, 12, 18)), detail(circle(7.75, 15.5, 1.5)),
            detail(seg(14.5, 17.5, 17.5, 17.5))]


@icon("washtub-bass", CAT, "Washtub bass: an upturned tub with a broom handle and a single string",
      tags=["gutbucket", "jug band", "folk", "homemade", "skiffle", "instrument"], aliases=["gutbucket"])
def _(S):
    tub = poly([(2.5, 21.5), (21.5, 21.5), (19.5, 15.5), (4.5, 15.5)], closed=True, r=S.r * 0.6)
    return [shell(tub), detail(seg(3.5, 18.5, 20.5, 18.5)), line(seg(6, 15.5, 8.5, 2.5)), line(seg(8.5, 2.5, 13, 15.5))]


# ============================================================================ keyboards

@icon("harpsichord", CAT, "Harpsichord from above: angular wing-shaped case with two keyboards at the front",
      tags=["baroque", "keyboard", "clavecin", "early music", "classical", "instrument"])
def _(S):
    case = poly([(3.5, 21.5), (3.5, 2.5), (8.5, 2.5), (20.5, 14.5), (20.5, 21.5)], closed=True, r=S.r)
    parts = [shell(case, stroke_miterlimit="2"), detail(seg(3.5, 14.5, 20.5, 14.5)), detail(seg(3.5, 18, 20.5, 18)),
             detail(seg(8, 14.5, 8, 6.5))]
    parts += [detail(seg(x, 18, x, 21.5)) for x in (8, 12, 16)]
    return parts


@icon("upright-piano", CAT, "Upright piano: tall cabinet with a keyboard across the middle and pedals below",
      tags=["piano", "keyboard", "home piano", "practice", "cabinet", "instrument"])
def _(S):
    parts = [line(seg(2.5, 3, 21.5, 3)), shell(rect(4, 3, 16, 15.5, min(S.R, 2))), detail(seg(4, 9.5, 20, 9.5)),
             detail(seg(4, 14, 20, 14)), line(seg(6, 18.5, 6, 21.5)), line(seg(18, 18.5, 18, 21.5)),
             dot(10.5, 20.75, 1), dot(13.5, 20.75, 1)]
    parts += [detail(seg(x, 9.5, x, 12)) for x in (8, 12, 16)]
    return parts


@icon("pipe-organ", CAT, "Pipe organ: a symmetric row of pipes above a console with keyboards",
      tags=["organ", "church organ", "cathedral", "keyboard", "pipes", "instrument"], aliases=["church-organ"])
def _(S):
    pipes = [line(seg(x, 14, x, top)) for x, top in ((4.5, 8), (8.25, 5), (12, 2.5), (15.75, 5), (19.5, 8))]
    return pipes + [shell(rect(3, 14, 18, 7.5, min(S.R, 2))), detail(seg(3, 17.5, 21, 17.5))]


@icon("harmonium", CAT, "Harmonium: box with a keyboard on top, a bellows flap at the back and stop knobs",
      tags=["pump organ", "reed organ", "indian", "devotional", "keyboard", "instrument"])
def _(S):
    return [shell(poly([(3.5, 9.5), (20.5, 3), (20.5, 9.5)], closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
            shell(rect(3, 9.5, 18, 12, min(S.R, 2))), detail(seg(3, 13.5, 21, 13.5)),
            dot(7, 17.75, 1), dot(10.33, 17.75, 1), dot(13.67, 17.75, 1), dot(17, 17.75, 1)]


@icon("concertina", CAT, "Concertina: hexagonal ends with buttons joined by pleated bellows",
      tags=["squeezebox", "bellows", "folk", "sea shanty", "irish", "instrument"])
def _(S):
    top = [(8.5, 8), (10.25, 6), (12, 8), (13.75, 6), (15.5, 8)]
    bot = [(x, 24 - y) for x, y in top]
    return [shell(poly(regular(5.5, 12, 3.75, 6, start=0), closed=True, r=S.r * 0.4)),
            shell(poly(regular(18.5, 12, 3.75, 6, start=0), closed=True, r=S.r * 0.4)),
            line(poly(top, r=S.r * 0.5)), line(poly(bot, r=S.r * 0.5)), line(seg(12, 8, 12, 16)),
            dot(5.5, 12, 1), dot(18.5, 12, 1)]


@icon("melodica", CAT, "Melodica: a small keyboard body with a flexible mouthpiece tube",
      tags=["pianica", "blow organ", "keyboard", "school", "wind", "instrument"], aliases=["pianica"])
def _(S):
    parts = [shell(rect(2.5, 7, 14, 10, min(S.R, 2)))]
    parts += [detail(seg(x, 7, x, 12)) for x in (6.25, 9.5, 12.75)]
    parts += [line("M16.5 12C20.5 12 21 15 19.75 17.5L18.5 20"), shell(rect(16.5, 19.5, 3.5, 2.5, rnd(S, 0, 1)))]
    return parts


@icon("synthesizer", CAT, "Synthesizer: a wide keyboard with knobs and a small display above the keys",
      tags=["synth", "keyboard", "electronic", "analog", "music production", "instrument"], aliases=["synth"])
def _(S):
    parts = [shell(rect(2, 5, 20, 14, min(S.R, 2))), detail(seg(2, 11, 22, 11))]
    parts += [detail(seg(x, 11, x, 19)) for x in (7, 12, 17)]
    parts += [dot(5.5, 8, 1.1), dot(9, 8, 1.1), detail(seg(13, 8, 18.5, 8))]
    return parts


@icon("modular-synthesizer", CAT, "Modular synthesizer: rack of modules with knobs, jacks and a patch cable",
      tags=["modular synth", "rack synth", "patch cable", "electronic", "analog", "instrument"])
def _(S):
    parts = [shell(rect(2.5, 3, 19, 18, S.R)), detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21))]
    parts += [dot(5.75, 6.75, 1.25), dot(5.75, 11, 1.25), dot(12, 6.75, 1.25), dot(18.25, 6.75, 1.25), dot(18.25, 11, 1.25)]
    parts.append(detail("M5.75 17C5.75 12 12 20 12 14.5" if S.name == "rounded" else "M5.75 17.5V15L12 17V13.5"))
    parts += [dot(12, 13.5, 1), dot(5.75, 17.5, 1), dot(18.25, 17.5, 1)]
    return parts


@icon("keytar", CAT, "Keytar: a keyboard worn like a guitar with keys along the body and a neck grip",
      tags=["keyboard guitar", "synth", "80s", "electronic", "strap", "instrument"])
def _(S):
    body = rp([(8, 10), (16, 10), (16, 21.5), (8, 21.5)], r=rnd(S, 0.5, 2))
    parts = [shell(body)]
    parts += [Part("dot", rp([(8, y - 0.8), (12, y - 0.8), (12, y + 0.8), (8, y + 0.8)])) for y in (12.75, 15.75, 18.75)]
    parts += [line(rseg(12, 10, 12, 2.5)), shell(rp([(10.5, 0), (13.5, 0), (13.5, 3), (10.5, 3)], r=rnd(S, 0, 1)))]
    return parts


@icon("theremin", CAT, "Theremin: a small cabinet with an upright rod antenna and a side loop antenna",
      tags=["electronic", "sci-fi", "spooky", "antenna", "touchless", "instrument"])
def _(S):
    return [shell(rect(6, 10, 12, 6, min(S.R, 2))), line(seg(16, 10, 16, 2.5)),
            line("M6 11.25H4.25A1.75 1.75 0 0 0 4.25 14.75H6" if S.name == "rounded" else "M6 11.25H3V14.75H6"),
            line(seg(12, 16, 12, 21)), line(seg(8, 21.25, 16, 21.25))]


# ============================================================================ woodwinds and pipes

def tube(d, w, cap="butt", join="miter") -> str:
    """Closed outline of a pipe of width w along the centre line d."""
    return path_to_d(ST(d, w, cap, join))


@icon("clarinet", CAT, "Clarinet: straight tube with a mouthpiece at the top, keys and a small flared bell",
      tags=["woodwind", "reed", "jazz", "orchestra", "klezmer", "instrument"])
def _(S):
    body = outline(rect(10, 6, 4, 12), poly([(10, 17.5), (14, 17.5), (16.5, 21.5), (7.5, 21.5)], closed=True),
                   poly([(10.75, 6.5), (11.25, 2.5), (12.75, 2.5), (13.25, 6.5)], closed=True))
    return [shell(body, stroke_linejoin="round") if S.name == "rounded" else shell(body, stroke_miterlimit="2"),
            detail(seg(10, 6, 14, 6)), dot(12, 9.5, 0.9), dot(12, 12.5, 0.9), dot(12, 15.5, 0.9)]


@icon("oboe", CAT, "Oboe: thin conical tube with keys, ending in a tiny double reed",
      tags=["woodwind", "double reed", "orchestra", "classical", "english horn", "instrument"])
def _(S):
    body = poly([(10.75, 6.5), (13.25, 6.5), (14.5, 20), (15, 21.5), (9, 21.5), (9.5, 20)], closed=True, r=S.r * 0.4)
    return [shell(body, stroke_miterlimit="2"), line(seg(12, 6.5, 12, 3.5)), solid(rect(11.25, 1.75, 1.5, 2.25, rnd(S, 0, 0.5))),
            line(seg(14, 10, 15.5, 10)), line(seg(8.25, 13.5, 10, 13.5)), line(seg(14.25, 16.5, 15.75, 16.5))]


@icon("bassoon", CAT, "Bassoon: tall wooden tube with a thin curved crook holding the reed",
      tags=["woodwind", "double reed", "orchestra", "fagotto", "low", "instrument"], aliases=["fagotto"])
def _(S):
    d = 15
    body = rp([(11, 1.75), (15, 1.75), (15, 22.25), (11, 22.25)], deg=d, r=rnd(S, 1, 2))
    c = rpt(11, 7, deg=d)
    crook = (f"M{fmt(c[0])} {fmt(c[1])}C{fmt(c[0] - 3)} {fmt(c[1] - 0.5)} {fmt(c[0] - 5.5)} {fmt(c[1] + 0.5)} "
             f"{fmt(c[0] - 6.25)} {fmt(c[1] + 4)}")
    return [shell(body), detail(rseg(11, 4.5, 15, 4.5, deg=d)), line(crook), dot(*rpt(13, 13, deg=d), 0.9),
            dot(*rpt(13, 17, deg=d), 0.9)]


@icon("recorder", CAT, "Recorder: straight wooden pipe with a beak mouthpiece, a window and finger holes",
      tags=["flute", "school", "woodwind", "descant", "fipple", "instrument"])
def _(S):
    body = rp([(10, 2), (14, 3), (14, 20), (15, 23), (9, 23), (10, 20)], deg=-45, r=S.r * 0.5)
    parts = [shell(body, stroke_miterlimit="2"), detail(rseg(10, 6.5, 14, 6.5, deg=-45))]
    parts += [dot(*rpt(12, y, deg=-45), 0.9) for y in (10.5, 13.75, 17)]
    return parts


@icon("pan-flute", CAT, "Pan flute: a row of pipes bound together, stepping from long to short",
      tags=["pan pipes", "panpipes", "syrinx", "andean", "wind", "instrument"], aliases=["pan-pipes", "panpipes"])
def _(S):
    xs = [3, 6.6, 10.2, 13.8, 17.4, 21]
    ys = [21, 18, 15, 12, 9]
    pts = [(3, 3), (21, 3), (21, ys[4])]
    for i in range(4, 0, -1):
        pts += [(xs[i], ys[i]), (xs[i], ys[i - 1])]
    pts += [(3, 21)]
    parts = [shell(poly(pts, closed=True, r=S.r * 0.5))]
    parts += [detail(seg(xs[i], 3, xs[i], ys[i - 1] - 0.01 + 0.01)) for i in range(1, 5)]
    parts.append(detail(seg(3, 6.5, 21, 6.5)))
    return parts


@icon("ocarina", CAT, "Ocarina: rounded egg-shaped vessel flute with a mouthpiece and finger holes",
      tags=["vessel flute", "clay flute", "sweet potato", "wind", "ceramic", "instrument"])
def _(S):
    body = outline(ellipse(13.5, 13, 8, 5.5), rect(2.5, 10.5, 5, 4, rnd(S, 0, 1.2)))
    return [shell(body), dot(11, 10.75, 1.1), dot(14.5, 10.25, 1.1), dot(18, 11.25, 1.1), dot(15.5, 15, 1.1)]


@icon("harmonica", CAT, "Harmonica: long flat mouth organ with a row of square holes along its front",
      tags=["mouth organ", "blues harp", "harp", "blues", "folk", "instrument"], aliases=["mouth-organ"])
def _(S):
    parts = [shell(rect(2, 7, 20, 10, S.R * 0.75)), detail(seg(2, 11, 22, 11))]
    parts += [Part("dot", rect(x - 1, 12.75, 2, 2.25, rnd(S, 0, 0.6))) for x in (5.5, 9.17, 12.83, 16.5)]
    return parts


@icon("didgeridoo", CAT, "Didgeridoo: very long wooden tube that flares slightly at the far end",
      tags=["didjeridu", "aboriginal", "australian", "drone", "wind", "instrument"], aliases=["didjeridu"])
def _(S):
    body = rp([(10.5, -0.25), (13.5, -0.25), (14, 15.5), (15, 23), (9, 23), (10, 15.5)], r=S.r * 0.6)
    parts = [shell(body, stroke_miterlimit="2")]
    parts += [dot(*rpt(12, y), 0.9) for y in (7.5, 11)]
    parts += [detail(rseg(10, 15.5, 14, 15.5)), detail(rseg(10.5, 2.75, 13.5, 2.75))]
    return parts


@icon("shakuhachi", CAT, "Shakuhachi: end-blown bamboo flute with nodes, a notched top and a rounded root end",
      tags=["japanese flute", "bamboo flute", "zen", "end blown", "wind", "instrument"])
def _(S):
    body = ("M10 4L14 2.5V15.5C14 17 15.5 18 15.5 19.75C15.5 21 14.25 21.5 12 21.5C9.75 21.5 8.5 21 8.5 19.75"
            "C8.5 18 10 17 10 15.5Z")
    return [shell(body, stroke_miterlimit="2"), detail(seg(10, 8, 14, 8)), detail(seg(10, 13, 14, 13)), dot(12, 10.5, 0.9),
            dot(12, 16.5, 0.9)]


@icon("shawm", CAT, "Shawm: conical wooden pipe with a flared bell, a disc near the top and a short reed",
      tags=["medieval", "renaissance", "double reed", "wind", "bombard", "instrument"])
def _(S):
    body = rpath([("M", (11, 5)), ("L", (13, 5)), ("L", (14, 14)), ("C", (14.5, 17.5), (16, 19.75), (17.5, 21.5)), ("L", (6.5, 21.5)),
                  ("C", (8, 19.75), (9.5, 17.5), (10, 14)), ("Z",)], deg=40)
    return [shell(body, stroke_miterlimit="2"), line(rseg(9.25, 4, 14.75, 4, deg=40)), line(rseg(12, 4, 12, 1.5, deg=40)),
            dot(*rpt(12, 9, deg=40), 0.9) if False else line(rseg(13.5, 10, 15.5, 10, deg=40))]


def taper(p0, c1, c2, p3, w0, w1, n=10):
    """Closed outline of a horn along a cubic curve, width going from w0 to w1."""
    def at(t):
        u = 1 - t
        x = u ** 3 * p0[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t ** 3 * p3[0]
        y = u ** 3 * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t ** 3 * p3[1]
        dx = 3 * u * u * (c1[0] - p0[0]) + 6 * u * t * (c2[0] - c1[0]) + 3 * t * t * (p3[0] - c2[0])
        dy = 3 * u * u * (c1[1] - p0[1]) + 6 * u * t * (c2[1] - c1[1]) + 3 * t * t * (p3[1] - c2[1])
        L = math.hypot(dx, dy) or 1
        return x, y, -dy / L, dx / L
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        x, y, nx, ny = at(t)
        w = (w0 + (w1 - w0) * t) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return left + right[::-1]


@icon("crumhorn", CAT, "Crumhorn: narrow capped wind pipe whose lower end curves up into a J hook",
      tags=["renaissance", "medieval", "capped reed", "wind", "early music", "instrument"])
def _(S):
    pipe = tube("M10 6V14.5A4.5 4.5 0 0 0 19 14.5V12.5", 4, rnd(S, "butt", "round"))
    parts = [shell(pipe), shell(rect(7, 2, 6, 4, rnd(S, 0, 1.5))), dot(10, 9.5, 0.9), dot(10, 13, 0.9)]
    return parts


@icon("serpent-horn", CAT, "Serpent: a wind instrument whose tube winds in a tall S shape",
      tags=["serpent", "early brass", "bass horn", "wind", "baroque", "instrument"])
def _(S):
    body = "M16 5C10 5 7.5 8 10 10.5C12.5 13 17.5 12.5 17.5 16.5C17.5 20 13 21.5 7 20.5"
    return [line(body), line(seg(16, 5, 16, 2.5)), line(seg(14.5, 2.5, 17.5, 2.5)),
            shell(poly([(7, 18.5), (3, 16.5), (3, 22), (7, 22.5)], closed=True, r=S.r * 0.4))]


@icon("sheng", CAT, "Sheng: a cluster of bamboo pipes of different heights rising from a round cup",
      tags=["chinese mouth organ", "mouth organ", "chinese", "reed", "wind", "instrument"])
def _(S):
    edges = [4, 7.2, 10.4, 13.6, 16.8, 20]
    tops = [8, 4, 2.5, 5, 9]
    pts = [(edges[0], 14)]
    for i, t in enumerate(tops):
        pts += [(edges[i], t), (edges[i + 1], t)]
    pts += [(edges[5], 14)]
    cup = "M3.5 14H20.5C20.5 18.5 17 21.5 12 21.5C7 21.5 3.5 18.5 3.5 14Z"
    parts = [shell(outline(poly(pts, closed=True), cup), stroke_linejoin=S.join), detail(seg(3.5, 14, 20.5, 14))]
    parts += [detail(seg(edges[i + 1], max(tops[i], tops[i + 1]), edges[i + 1], 14)) for i in range(4)]
    return parts + [line(seg(20, 17.5, 22, 17.5))]


@icon("hulusi", CAT, "Hulusi: a gourd with a small bulb on top and three bamboo pipes coming out below",
      tags=["cucurbit flute", "gourd flute", "chinese", "yunnan", "wind", "instrument"])
def _(S):
    gourd = outline(circle(12, 6, 2.75), circle(12, 11.5, 4.5))
    return [shell(gourd), line(seg(12, 16, 12, 22)), line(seg(8, 14.5, 8, 19.5)), line(seg(16, 14.5, 16, 19.5)),
            line(seg(12, 3.25, 12, 1.75)) if False else dot(12, 11.5, 1.1)]


# ============================================================================ brass and horns

@icon("trombone", CAT, "Trombone: a long U-shaped slide, a mouthpiece and a forward-facing bell",
      tags=["brass", "slide", "jazz", "big band", "orchestra", "instrument"])
def _(S):
    return [line(seg(4, 8, 13, 8)), line(seg(3.5, 6.5, 3.5, 9.5)) if False else line(seg(4, 6.5, 4, 9.5)),
            shell(poly([(13, 7), (21, 3.5), (21, 12.5), (13, 9)], closed=True, r=S.r * 0.4)),
            shell(rect(3, 14, 18.5, 5, rnd(S, 1, 2.5))), line(seg(8, 8, 8, 14))]


@icon("french-horn", CAT, "French horn: circular coiled tubing with an inner loop and a wide flared bell",
      tags=["horn", "brass", "orchestra", "classical", "coil", "instrument"])
def _(S):
    return [line(circle(10, 10.5, 7)), line(circle(10, 10.5, 3)), line(seg(3.25, 8.5, 2, 3)),
            shell(poly([(13.5, 16), (21.5, 13.5), (21.5, 21.5), (15.5, 17.5)], closed=True, r=S.r * 0.4))]


@icon("tuba", CAT, "Tuba: a large upright brass horn with coiled tubing, valves and a huge bell pointing up",
      tags=["brass", "bass", "oompah", "band", "orchestra", "instrument"])
def _(S):
    bell = "M4.5 2.5H19.5C16.5 3.5 14.5 5.5 14.5 9.5H9.5C9.5 5.5 7.5 3.5 4.5 2.5Z"
    body = outline(bell, ellipse(12, 15.5, 6, 6))
    return [shell(body, stroke_miterlimit="2")] + [detail(seg(x, 13.5, x, 17.5)) for x in (9, 12, 15)] + \
        [line(seg(6, 14, 3, 11))]


def _ring_behind(cx, cy, r, bx, by, br, pad=1.5):
    """Arc of a ring (cx, cy, r) that stays outside a circle (bx, by, br + pad) drawn in front of it."""
    d = math.hypot(bx - cx, by - cy)
    R = br + pad
    a = math.degrees(math.atan2(by - cy, bx - cx))
    h = math.degrees(math.acos((r * r + d * d - R * R) / (2 * r * d)))
    return arc(cx, cy, r, a + h, a - h + 360)


@icon("sousaphone", CAT, "Sousaphone: brass tubing wrapped in a big circle with a huge bell facing forward over the top",
      tags=["tuba", "marching band", "brass", "bass", "parade", "instrument"])
def _(S):
    return [line(_ring_behind(9.5, 14.5, 6.5, 15.5, 8, 5.5)), shell(circle(15.5, 8, 5.5)), dot(15.5, 8, 2),
            line(seg(3, 14.5, 3, 19))]


@icon("bugle", CAT, "Bugle: a simple brass horn with one loop of tubing, no valves and a flared bell",
      tags=["brass", "military", "reveille", "call", "scout", "instrument"])
def _(S):
    return [line(rect(4, 9, 11, 8, 4)), line(seg(8, 17, 2.5, 17)), line(seg(2.5, 15.5, 2.5, 18.5)),
            shell(poly([(13, 7.5), (21, 4), (21, 13.5), (13, 10.5)], closed=True, r=S.r * 0.4))]


@icon("hunting-horn", CAT, "Hunting horn: brass tubing coiled into a single ring with a flared bell",
      tags=["horn", "hunt", "post horn", "brass", "call", "instrument"])
def _(S):
    return [line(arc(10, 14, 7, -80, 250)), line(seg(7.6, 20.6, 5, 22)),
            shell(poly([(11.2, 6), (15, 6), (21.5, 2.5), (21.5, 12), (15, 8.5), (11.2, 8.5)], closed=True, r=S.r * 0.4))]


@icon("shofar", CAT, "Shofar: a curved ram's horn with a narrow mouth end and a wide open end",
      tags=["ram's horn", "jewish", "rosh hashanah", "yom kippur", "horn", "instrument"])
def _(S):
    pts = taper((3.5, 18.5), (8, 21.5), (11, 11.5), (15, 10.5), 2, 5.5, 8)
    top = taper((15, 10.5), (16.75, 10), (18.5, 7.5), (19, 5), 5.5, 6.5, 4)
    body = outline(poly(pts, closed=True), poly(top, closed=True))
    return [shell(body, stroke_linejoin=S.join), detail(seg(*pts[8], *pts[9])) if False else detail(seg(12.25, 10, 14.5, 14.75))]


@icon("carnyx", CAT, "Carnyx: a tall vertical war trumpet topped with an open-mouthed animal head",
      tags=["celtic", "war horn", "iron age", "trumpet", "boar", "instrument"])
def _(S):
    head = poly([(10, 11), (9.5, 6), (11, 3.5), (11, 1.75), (13.25, 3.25), (21, 4.5), (15.5, 6.75), (20.5, 10), (14, 10), (13.5, 11)],
                closed=True, r=S.r * 0.3)
    return [shell(head, stroke_miterlimit="2"), dot(12.5, 6, 1), line(seg(11.75, 11, 11.75, 22)), line(seg(8.5, 19.5, 11.75, 19.5))]


@icon("vuvuzela", CAT, "Vuvuzela: a long straight plastic horn that widens steadily into a large bell",
      tags=["stadium horn", "football", "soccer", "fan", "noise", "horn"])
def _(S):
    body = rp([(11.5, 0), (12.5, 0), (15.25, 19.5), (17, 22.25), (7, 22.25), (8.75, 19.5)], r=S.r * 0.4)
    return [shell(body, stroke_miterlimit="2"), detail(rseg(8.75, 19.5, 15.25, 19.5))]


@icon("air-horn", CAT, "Air horn: an aerosol can with a trumpet horn on top and sound waves",
      tags=["horn", "party", "stadium", "boat horn", "loud", "noise"])
def _(S):
    return [shell(rect(3.5, 12, 7, 10, min(S.R, 2))), shell(rect(5, 9, 4, 3, 0)),
            shell(poly([(7, 6.5), (12, 6.5), (17, 3), (17, 12), (12, 8.5), (7, 8.5)], closed=True, r=S.r * 0.3)),
            line(arc(17, 7.5, 3.5, -45, 45))]


@icon("jaw-harp", CAT, "Jaw harp: a small horseshoe-shaped metal frame with a springy tongue through it",
      tags=["juice harp", "mouth harp", "trump", "twang", "folk", "instrument"], aliases=["mouth-harp"])
def _(S):
    frame = "M9.25 20V12A4.5 4.5 0 1 1 14.75 12V20"
    return [line(frame), line(poly([(12, 6.5), (12, 20), (15, 22)], r=S.r))]


@icon("bullroarer", CAT, "Bullroarer: a flat pointed wooden slat on a long cord, swung in a circle",
      tags=["whirled", "aboriginal", "ritual", "rhombus", "swing", "instrument"])
def _(S):
    slat = rpath([("M", (16, 9)), ("C", (18.5, 12), (18.5, 17), (16, 21.5)), ("C", (13.5, 17), (13.5, 12), (16, 9)), ("Z",)], deg=-45, cx=16, cy=15)
    return [shell(slat), line(seg(3.5, 3.5, 11.75, 10.5)), dot(3.5, 3.5, 1.5), line(arc(8, 8, 13.5, 20, 70))]


# ============================================================================ drums

@icon("drum-kit", CAT, "Drum kit: a bass drum with two toms on top and a cymbal on a stand",
      tags=["drum set", "drums", "drummer", "band", "percussion", "instrument"], aliases=["drum-set"])
def _(S):
    return [shell(circle(9.5, 15.75, 5.75)), dot(9.5, 15.75, 1.5), shell(rect(3, 5, 5, 4.25, min(S.R, 1.5))),
            shell(rect(10, 5, 5, 4.25, min(S.R, 1.5))), line(seg(16, 4, 22, 2.5)), line(seg(19, 3.25, 19, 21.5)),
            line(seg(16.5, 21.5, 21.5, 21.5))]


_TIMPANI_MALLET = seg(9.5, 7, 20, 2.5)


def _timpani(S, mallet=True):
    parts = [shell("M3 9.5H21C21 15.5 17 19 12 19C7 19 3 15.5 3 9.5Z"), line(seg(8, 18, 6, 22)), line(seg(16, 18, 18, 22))]
    if mallet:
        parts += [line(_TIMPANI_MALLET), shell(circle(8, 7.5, 1.5))]
    return parts


@icon("timpani", CAT, "Timpani: a large kettle-shaped drum on legs with a mallet resting on the head",
      tags=["kettle drum", "kettledrum", "orchestra", "percussion", "timpano", "instrument"], aliases=["kettle-drum"])
def _(S):
    return _timpani(S)


@icon("congas", CAT, "Congas: two tall barrel-shaped drums standing side by side",
      tags=["conga", "tumbadora", "latin", "cuban", "hand drum", "percussion"], aliases=["conga-drums"])
def _(S):
    def barrel(cx, top):
        h = 21.5 - top
        return poly([(cx - 3, top), (cx + 3, top), (cx + 3.75, top + h * 0.4), (cx + 2.5, 21.5), (cx - 2.5, 21.5),
                     (cx - 3.75, top + h * 0.4)], closed=True, r=rnd(S, 0, 2))
    return [shell(barrel(7, 3)), shell(barrel(17, 6.5)), detail(seg(3.5, 6, 10.5, 6)), detail(seg(13.5, 9.5, 20.5, 9.5))]


@icon("djembe", CAT, "Djembe: a goblet-shaped hand drum with a wide head and rope lacing",
      tags=["african drum", "hand drum", "goblet drum", "west african", "percussion", "instrument"])
def _(S):
    body = sym(12, (12, 3), [((16, 3), (20, 3), (20, 4.5)), ((20, 9), (14, 11.5), (14, 14)),
                             ((14, 17), (16.5, 18.5), (16.5, 21.5)), ((15, 21.5), (13.5, 21.5), (12, 21.5))])
    return [shell(body), detail(poly([(6.5, 6), (9.25, 10), (12, 6), (14.75, 10), (17.5, 6)], r=S.r * 0.5))]


@icon("tabla", CAT, "Tabla: a pair of hand drums, one tall and narrow, one wide and round, each with a dark centre",
      tags=["indian drums", "dayan", "bayan", "hand drum", "percussion", "instrument"])
def _(S):
    bayan = "M2.5 12A5 2.5 0 0 1 12.5 12C12.5 18 10.5 21.5 7.5 21.5C4.5 21.5 2.5 18 2.5 12Z"
    dayan = "M14.25 7A3.25 2 0 0 1 20.75 7L20 21.5H15Z"
    return [shell(bayan), detail(ellipse(7.5, 12, 5, 2.5)) if False else detail("M2.5 12A5 2.5 0 0 0 12.5 12"),
            dot(7.5, 11.75, 1), shell(dayan), detail("M14.25 7A3.25 2 0 0 0 20.75 7"), dot(17.5, 6.9, 0.9)]


@icon("cajon", CAT, "Cajon: a wooden box drum in three-quarter view with a round sound hole on its side",
      tags=["box drum", "peruvian", "flamenco", "acoustic", "percussion", "instrument"])
def _(S):
    outer = poly([(3.5, 7), (8.5, 2.5), (20.5, 2.5), (20.5, 17), (15.5, 21.5), (3.5, 21.5)], closed=True, r=rnd(S, 0, 2))
    return [shell(outer), detail(poly([(3.5, 7), (15.5, 7), (20.5, 2.5)])), detail(seg(15.5, 7, 15.5, 21.5)),
            detail(ellipse(18, 12, 1.25, 2.25)) if False else dot(18, 12.25, 1.4)]


@icon("taiko", CAT, "Taiko: a big studded barrel drum lying on a crossed wooden stand",
      tags=["japanese drum", "barrel drum", "festival", "ensemble", "percussion", "instrument"])
def _(S):
    body = "M5.5 4C10 1.5 14 1.5 18.5 4A2.5 6 0 0 1 18.5 16C14 18.5 10 18.5 5.5 16A2.5 6 0 0 1 5.5 4Z"
    parts = [shell(body), detail("M5.5 4A2.5 6 0 0 0 5.5 16")]
    parts += [dot(x, y, 0.85) for x, y in ((8.5, 5.5), (9.4, 8.2), (9.6, 11), (9.1, 13.9))]
    parts += [line(seg(8, 17, 15.5, 21.5)), line(seg(16, 17, 8.5, 21.5))]
    return parts


@icon("frame-drum", CAT, "Frame drum: a wide shallow round drum with a thin rim and a double-ended tipper",
      tags=["bodhran", "daf", "hand drum", "celtic", "percussion", "instrument"])
def _(S):
    body = outline(ellipse(11, 10, 8.5, 5.5), rect(2.5, 10, 17, 3), ellipse(11, 13, 8.5, 5.5))
    return [shell(body), detail("M2.5 10A8.5 5.5 0 0 0 19.5 10"), line(seg(14.5, 21, 20.5, 17)),
            dot(14.5, 21, 1.5) if S.name == "rounded" else Part("dot", rect(13, 19.5, 3, 3)),
            dot(20.5, 17, 1.5) if S.name == "rounded" else Part("dot", rect(19, 15.5, 3, 3))]


@icon("talking-drum", CAT, "Talking drum: an hourglass drum with cords running from head to head",
      tags=["dundun", "west african", "hourglass drum", "hand drum", "percussion", "instrument"])
def _(S):
    waist = ["M9 6C11 9.5 11 14.5 9 18", "M15 6C13 9.5 13 14.5 15 18"] if S.name == "rounded" else \
        ["M9 6L11 12L9 18", "M15 6L13 12L15 18"]
    return [shell(ellipse(12, 4, 7, 1.75)), shell(ellipse(12, 20, 7, 1.75)), line(seg(5, 4, 5, 20)), line(seg(19, 4, 19, 20)),
            line(waist[0]), line(waist[1])]


@icon("steelpan", CAT, "Steelpan: a shallow steel drum with dimpled note areas and two sticks",
      tags=["steel drum", "caribbean", "trinidad", "calypso", "percussion", "instrument"], aliases=["steel-drum"])
def _(S):
    body = outline(ellipse(12, 14, 9.5, 5), rect(2.5, 14, 19, 3), ellipse(12, 17, 9.5, 5))
    return [shell(body), detail("M2.5 14A9.5 5 0 0 0 21.5 14"), detail(ellipse(12, 14, 5, 2.25)),
            detail(seg(2.5, 14, 7, 14)), detail(seg(17, 14, 21.5, 14)),
            line(seg(8, 7, 13, 2.5)), dot(7.5, 7.5, 1.4), line(seg(13, 7, 18, 2.5)), dot(12.5, 7.5, 1.4)]
