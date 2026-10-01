"""TypeIcon Core: hobbies (batch 002): kites, magic, genealogy, ham radio, props and crafts."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "hobbies"


def L(S, a, b):
    return a if S.name == "line" else b


def dia(cx, cy, hw, hh, S, k=0.7):
    return poly([(cx, cy - hh), (cx + hw, cy), (cx, cy + hh), (cx - hw, cy)], closed=True, r=S.r * k)


# ============================================================================ kites

@icon("stunt-kite", CAT, "Swept-back delta kite with two control lines running down to handles",
      tags=["kite", "sport kite", "delta kite", "wind", "flying", "outdoor"])
def _(S):
    return [shell(poly([(12, 3), (21, 14), (12, 10.5), (3, 14)], closed=True, r=S.r)),
            detail(seg(12, 3, 12, 10.5)),
            line(poly([(3, 14), (9, 20.5)])), line(poly([(21, 14), (15, 20.5)])),
            line(seg(7.5, 21.5, 10.5, 21.5)), line(seg(13.5, 21.5, 16.5, 21.5))]


@icon("parafoil-kite", CAT, "Curved soft kite canopy with cell dividers and bridle lines meeting at one point",
      tags=["kite", "foil kite", "ram air", "wind", "flying", "outdoor"])
def _(S):
    top = "M4 8Q12 1 20 8"
    d = top + "V13Q12 8 4 13Z"
    return [shell(d), detail(seg(9, 5.5, 9, 11)), detail(seg(15, 5.5, 15, 11)),
            line(poly([(5, 13), (12, 20.5)])), line(poly([(19, 13), (12, 20.5)])),
            line(poly([(12, 10.5), (12, 20.5)]))]


@icon("sled-kite", CAT, "Rectangular sled kite with two vertical spars and a V bridle below",
      tags=["kite", "sled", "wind", "flying", "outdoor", "spar"])
def _(S):
    return [shell(rect(5, 3, 14, 12, S.R)), detail(seg(10, 3, 10, 15)), detail(seg(14, 3, 14, 15)),
            line(poly([(6, 15), (12, 21)])), line(poly([(18, 15), (12, 21)]))]


@icon("fighter-kite", CAT, "Small diamond kite with a bowed spar across the top and a short tail",
      tags=["kite", "diamond kite", "wind", "flying", "tail", "outdoor"])
def _(S):
    return [shell(poly([(12, 2.5), (19, 10), (12, 18), (5, 10)], closed=True, r=S.r)),
            detail(seg(12, 2.5, 12, 18)), detail("M5 10Q12 6.5 19 10"),
            line("M12 18Q8.5 19.5 12 20.5"), dot(12.5, 21.5, 1.25)]


@icon("centipede-kite", CAT, "Chain of round discs joined by a line with a face on the front disc",
      tags=["kite", "chain kite", "dragon kite", "discs", "flying", "outdoor"])
def _(S):
    h, a, b = (16.5, 7.5, 4.5), (9.5, 13.5, 3.0), (4.5, 19, 2.5)

    def link(p, q):
        ang = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
        s = polar(p[0], p[1], p[2], ang)
        e = polar(q[0], q[1], q[2], ang + 180)
        return line(seg(s[0], s[1], e[0], e[1]))
    return [shell(circle(*h)), shell(circle(*a)), shell(circle(*b)), link(h, a), link(a, b),
            dot(15, 6.5, 1.0), dot(18.5, 6.5, 1.0), detail(seg(15, 9, 18, 9))]


@icon("octopus-kite", CAT, "Round kite head with a face and three wavy tails hanging below like tentacles",
      tags=["kite", "tails", "face", "wind", "flying", "outdoor", "ribbon"])
def _(S):
    return [shell(circle(12, 8, 5.5)), dot(10, 7, 1.0), dot(14, 7, 1.0),
            line("M8.8 12.8C6 15 9 17 6.5 21"), line("M12 13.5C9.5 16 14.5 18 12 21.5"),
            line("M15.2 12.8C18 15 15 17 17.5 21")]


@icon("tetrahedral-kite", CAT, "Large triangular kite made of four triangle cells with a flying line below",
      tags=["kite", "tetrahedral", "pyramid", "cells", "triangle", "flying", "outdoor"])
def _(S):
    return [shell(poly([(12, 3), (21, 18), (3, 18)], closed=True, r=S.r)),
            detail(poly([(7.5, 10.5), (16.5, 10.5), (12, 18)], closed=True)),
            line(seg(12, 18, 12, 22))]


@icon("rokkaku-kite", CAT, "Six-sided kite with one vertical spar, two cross spars and a short bridle",
      tags=["kite", "hexagon", "fighting kite", "spars", "flying", "outdoor"])
def _(S):
    return [shell(poly([(12, 2), (19, 6.5), (19, 14), (12, 19), (5, 14), (5, 6.5)], closed=True, r=S.r)),
            detail(seg(12, 2, 12, 19)), detail(seg(5, 8.5, 19, 8.5)), detail(seg(5, 13.5, 19, 13.5)),
            line(seg(12, 19, 12, 22))]


@icon("kite-flying", CAT, "Person on a small hill holding a line up to a diamond kite in the sky",
      tags=["kite", "flying a kite", "outdoor", "hill", "person", "wind", "play"])
def _(S):
    return [shell(circle(7, 7.5, 2)), line(seg(7, 10.5, 7, 15)), line(poly([(5.5, 17.5), (7, 15), (8.5, 17.5)])),
            line(poly([(7, 12), (10, 10.5)])),
            line("M2 21Q7 17 12 19.5T22 20"),
            shell(dia(17.5, 6, 3, 4, S, 0.6)), line("M10 10.5Q15 10.5 17.5 10")]


@icon("kite-train", CAT, "Three small diamond kites stacked in a diagonal row along one flying line",
      tags=["kite", "kite chain", "string of kites", "flying", "outdoor", "diagonal"])
def _(S):
    out = []
    for cx, cy in [(18, 5.8), (11.5, 12), (5, 18.2)]:
        pts = [(cx, cy - 3.6), (cx + 2.9, cy), (cx, cy + 3.6), (cx - 2.9, cy)]
        out.append(shell(poly(pts, closed=True, r=S.r * 0.3)))
    return out


# ============================================================================ stage magic

def edge(c, r, toward):
    ang = math.degrees(math.atan2(toward[1] - c[1], toward[0] - c[0]))
    return polar(c[0], c[1], r, ang)


@icon("substitution-trunk", CAT, "Large travel trunk with a curved lid, two straps and a padlock on the front",
      tags=["trunk", "magic trick", "stage magic", "chest", "illusion", "box", "padlock"])
def _(S):
    return [shell("M3 20V9Q3 4 8 4H16Q21 4 21 9V20Z"),
            detail(seg(3, 10, 21, 10)), detail(seg(6.5, 5.5, 6.5, 20)), detail(seg(17.5, 5.5, 17.5, 20)),
            Part("dot", rect(10, 12.5, 4, 4, 0.6))]


@icon("multiplying-balls", CAT, "Open hand with a small ball pinched between each pair of fingers",
      tags=["magic trick", "close-up magic", "balls", "sleight of hand", "hand", "fingers", "conjuring"])
def _(S):
    out = [shell(rect(3, 13, 19, 8, S.R))]
    for x in (4.5, 10, 15.5, 21):
        out.append(line(seg(x, 13, x, 4.5)))
    for x in (7.25, 12.75, 18.25):
        out.append(dot(x, 9.5, 1.8))
    return out


@icon("magician-table", CAT, "Small table with a draped cloth holding a top hat and a magic wand",
      tags=["magic", "stage magic", "props", "table", "top hat", "wand", "performance"])
def _(S):
    return [shell(poly([(3, 14), (21, 14), (19, 18), (5, 18)], closed=True, r=S.r * 0.5)),
            line(seg(12, 18, 12, 21)), line(seg(8.5, 21.5, 15.5, 21.5)),
            shell(rect(5.5, 3, 5.5, 6, L(S, 0, 1))), line(seg(3.5, 10, 13, 10)),
            line(poly([(15, 11), (20.5, 5)]))]


@icon("magic-kit", CAT, "Open magic box with a ball, a playing card and a wand sticking out",
      tags=["magic set", "conjuring", "toy", "tricks", "wand", "cards", "ball", "box"])
def _(S):
    return [shell(rect(3, 12.5, 18, 8.5, S.R)),
            shell(circle(7, 7.2, 2.2)), shell(rect(10.5, 4, 4.5, 8.5, L(S, 0, 1))),
            line(poly([(18.5, 12), (20.5, 4)])), dot(12, 17, 1.2)]


@icon("ball-and-vase", CAT, "Small goblet with a pointed lid lifted above a ball resting in the cup",
      tags=["magic trick", "cups and balls", "vase", "lid", "goblet", "conjuring", "illusion"])
def _(S):
    return [shell(poly([(12, 2), (16.5, 6), (7.5, 6)], closed=True, r=S.r * 0.6)),
            shell("M6.5 12.5H17.5Q17.5 18.5 12 18.5Q6.5 18.5 6.5 12.5Z"),
            line(seg(12, 18.5, 12, 21)), line(seg(8.5, 21.5, 15.5, 21.5)),
            shell(circle(12, 11, 2.0))]


@icon("cut-rope-trick", CAT, "Rope cut in the middle by a pair of scissors with sparkles",
      tags=["magic trick", "rope", "scissors", "cut and restored", "close-up magic", "conjuring"])
def _(S):
    return [line("M2 8Q4.5 4.5 8 7.5"), line("M16 7.5Q19.5 4.5 22 8"),
            line(poly([(10.5, 8.5), (14.5, 16.5)])), line(poly([(13.5, 8.5), (9.5, 16.5)])),
            shell(circle(8.5, 19, 2.2)), shell(circle(15.5, 19, 2.2))]


@icon("appearing-cane", CAT, "Magic wand with three flowers bursting out of its top end",
      tags=["magic trick", "flowers", "wand", "cane", "bouquet", "conjuring", "stage magic"])
def _(S):
    out = [shell(rect(10, 14, 4, 8, L(S, 0, 1))), detail(seg(10, 18, 14, 18))]
    base = (12, 14)
    for c in [(5.5, 6.5), (12, 4), (18.5, 6.5)]:
        e = edge(c, 2.4, base)
        out.append(line(seg(base[0], base[1], e[0], e[1])))
        out.append(shell(circle(c[0], c[1], 2.4)))
    return out


# ============================================================================ genealogy

@icon("fan-chart", CAT, "Half circle split into rings and radiating segments showing generations of ancestors",
      tags=["genealogy", "family history", "ancestry", "fan chart", "pedigree", "generations", "family tree"])
def _(S):
    c = (12, 19)
    out = [shell(L(S, "M2 19A10 10 0 0 1 22 19Z", "M2.2 17A10 10 0 0 1 21.8 17Q22 19 20 19H4Q2 19 2.2 17Z")), detail(arc(12, 19, 5, 180, 360)), detail(seg(12, 19, 12, 14))]
    for ang in (240, 300):
        a, b = polar(12, 19, 5, ang), polar(12, 19, 10, ang)
        out.append(detail(seg(a[0], a[1], b[0], b[1])))
    return out


@icon("dna-ancestry", CAT, "Double helix strand beside a small family tree of three joined nodes",
      tags=["genealogy", "dna test", "ancestry", "genetic", "family tree", "heritage", "helix"])
def _(S):
    return [line("M3.5 3C3.5 6 9.5 6 9.5 9S3.5 12 3.5 15S9.5 18 9.5 21"),
            line("M9.5 3C9.5 6 3.5 6 3.5 9S9.5 12 9.5 15S3.5 18 3.5 21"),
            dot(17.5, 5, 2.2), dot(14.8, 19, 2.2), dot(20.2, 19, 2.2),
            line(seg(17.5, 6, 17.5, 12.5)), line(poly([(14.8, 18), (14.8, 12.5), (20.2, 12.5), (20.2, 18)]))]


def box(S, x, y, w, h):
    return shell(rect(x, y, w, h, min(S.R, 1.5)))


@icon("descendant-chart", CAT, "One box at the top branching down into two and then four boxes",
      tags=["genealogy", "family tree", "descendants", "chart", "hierarchy", "org chart", "family history"])
def _(S):
    xs = [4.4, 9.6, 14.8, 20.0]
    out = [box(S, 9.5, 3, 5, 3.5), box(S, 4.5, 10.5, 5, 3.5), box(S, 14.5, 10.5, 5, 3.5)]
    out += [line(poly([(12, 6.5), (12, 8.5)])), line(poly([(7, 10.5), (7, 8.5), (17, 8.5), (17, 10.5)]))]
    for mx, (a, b) in [(7, (xs[0], xs[1])), (17, (xs[2], xs[3]))]:
        out.append(line(poly([(mx, 14), (mx, 15.5)])))
        out.append(line(poly([(a, 17.5), (a, 15.5), (b, 15.5), (b, 17.5)])))
    for x in xs:
        out.append(solid(rect(x - 1.7, 17.5, 3.4, 3.8)))
    return out


@icon("family-group-sheet", CAT, "Record form with two parent boxes at the top and a list of child rows beneath",
      tags=["genealogy", "family history", "form", "record", "parents", "children", "worksheet"])
def _(S):
    return [shell(rect(4, 2, 16, 20, S.R)),
            Part("dot", rect(7, 5, 4, 3, 0.5)), Part("dot", rect(13, 5, 4, 3, 0.5)),
            detail(seg(7.5, 12, 16.5, 12)), detail(seg(7.5, 15.5, 16.5, 15.5)), detail(seg(7.5, 19, 13, 19))]


@icon("parish-register", CAT, "Thick ledger book open with ruled lines and a small cross at the top of the left page",
      tags=["genealogy", "church records", "baptism", "marriage", "burial", "ledger", "register", "family history"])
def _(S):
    return [shell(poly([(12, 6), (3, 4.5), (3, 19), (12, 20.5), (21, 19), (21, 4.5)], closed=True, r=S.r)),
            detail(seg(12, 6, 12, 20.5)),
            detail(seg(7.5, 7.5, 7.5, 11)), detail(seg(6, 9, 9, 9)),
            detail(seg(6, 14, 9.5, 14.5)), detail(seg(15, 9, 18, 8.5)), detail(seg(15, 12, 18, 11.5)), detail(seg(15, 15.5, 18, 15.5))]


@icon("passenger-list", CAT, "Paper list with rows of lines and a small steamship at the top",
      tags=["genealogy", "immigration", "ship manifest", "passengers", "ellis island", "records", "family history"])
def _(S):
    return [shell(rect(4, 2, 16, 20, S.R)),
            detail(poly([(6.5, 9.5), (8.5, 12), (15.5, 12), (17.5, 9.5)], closed=True)),
            detail(seg(12, 5, 12, 9.5)),
            detail(seg(7.5, 15.5, 16.5, 15.5)), detail(seg(7.5, 19, 13, 19))]


@icon("gravestone-rubbing", CAT, "Arched headstone with a cross and a crayon shading across it",
      tags=["genealogy", "cemetery", "headstone", "grave", "rubbing", "crayon", "family history"])
def _(S):
    return [shell("M3.5 21V9A5.5 5.5 0 0 1 14.5 9V21Z"),
            detail(seg(9, 6, 9, 13)), detail(seg(6.5, 8.5, 11.5, 8.5)),
            shell(poly([(14.5, 18.5), (19.5, 13.5), (21.5, 15.5), (16.5, 20.5)], closed=True, r=S.r * 0.3))]


@icon("family-bible", CAT, "Thick book with a cross on the cover and a ribbon marker hanging below",
      tags=["genealogy", "family history", "heirloom", "religious book", "record", "cross", "ribbon"])
def _(S):
    return [shell(rect(5, 2, 14, 17, S.R)), detail(seg(8.5, 2, 8.5, 19)),
            detail(seg(14, 5, 14, 12.5)), detail(seg(11.5, 8, 16.5, 8)),
            line(seg(16.5, 19, 16.5, 22))]


@icon("oral-history", CAT, "Person speaking in a speech bubble beside a small handheld recorder",
      tags=["genealogy", "interview", "recording", "storytelling", "memories", "elder", "family history"])
def _(S):
    return [shell(circle(7, 9.5, 3)), line("M2 21V19.5A5 5 0 0 1 12 19.5V21"),
            shell(poly([(13.5, 2.5), (21.5, 2.5), (21.5, 8.5), (16.5, 8.5), (13.5, 10.5)], closed=True, r=S.r * 0.6)),
            shell(rect(15.5, 13, 6, 9, min(S.R, 1.5))), dot(18.5, 16.5, 1.2), detail(seg(17, 19.5, 20, 19.5))]


@icon("relationship-chart", CAT, "Square grid table with shaded cells along the diagonal for tracing cousin relationships",
      tags=["genealogy", "cousins", "kinship", "table", "grid", "family history", "chart"])
def _(S):
    out = [shell(rect(3, 3, 18, 18, S.R)), detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)),
           detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15))]
    for c in (6, 12, 18):
        out.append(Part("dot", rect(c - 1.5, c - 1.5, 3, 3)))
    return out


# ============================================================================ amateur radio

@icon("paddle-key", CAT, "Morse paddle key with two upright finger paddles on a heavy flat base",
      tags=["morse code", "ham radio", "cw", "telegraph key", "amateur radio", "keyer", "paddles"])
def _(S):
    return [shell(rect(3, 16, 18, 5, S.R)),
            shell(rect(6.5, 4, 3.5, 12, min(S.R, 1.7))), shell(rect(14, 4, 3.5, 12, min(S.R, 1.7)))]


@icon("qsl-card", CAT, "Postcard with callsign lines, a small antenna and radio waves for confirming a contact",
      tags=["ham radio", "amateur radio", "callsign", "confirmation card", "postcard", "dx", "contact"])
def _(S):
    return [shell(rect(2, 4, 20, 16, S.R)),
            detail(seg(5.5, 9, 11.5, 9)), detail(seg(5.5, 13, 10, 13)), detail(seg(5.5, 16.5, 8.5, 16.5)),
            detail(seg(17, 17, 17, 10.5)), detail("M14.5 9.5A3.5 3.5 0 0 1 19.5 9.5")]


@icon("antenna-tuner", CAT, "Front panel of a radio accessory box with a small gauge and two large tuning knobs",
      tags=["ham radio", "amateur radio", "atu", "tuner", "knobs", "matching", "transmitter"])
def _(S):
    return [shell(rect(2, 3, 20, 18, S.R)),
            detail(arc(12, 10.5, 5, 200, 340)), detail(seg(12, 10.5, 14, 7.5)),
            detail(circle(7, 16.5, 2.3)), detail(circle(17, 16.5, 2.3))]


@icon("swr-meter", CAT, "Radio meter box with an analog gauge showing two needles and a small knob below",
      tags=["ham radio", "amateur radio", "standing wave ratio", "gauge", "power meter", "antenna test", "swr"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)),
            detail(arc(12, 14, 6.5, 195, 345)), detail(seg(12, 14, 8.5, 8.5)), detail(seg(12, 14, 15.5, 9.5)),
            dot(12, 18.2, 1.3)]


@icon("radio-direction-finding", CAT, "Handheld three-element yagi antenna with a grip and a signal wave arriving from ahead",
      tags=["ham radio", "fox hunting", "foxhunt", "transmitter hunt", "yagi", "radio orienteering", "tracking"])
def _(S):
    return [line(seg(3, 12, 14.5, 12)), line(seg(3, 12, 3, 21)),
            line(seg(7.5, 5, 7.5, 19)), line(seg(12, 6.5, 12, 17.5)),
            line(arc(16, 12, 3.4, 320, 40)), line(arc(16, 12, 6.2, 322, 38))]


@icon("radio-repeater", CAT, "Tall antenna mast on a hilltop with signal arcs radiating out to both sides",
      tags=["ham radio", "amateur radio", "relay", "repeater", "hill", "tower", "coverage"])
def _(S):
    return [line("M2 21Q12 12 22 21"), line(seg(12, 16.5, 12, 8.5)), dot(12, 8, 1.5),
            line(arc(12, 8, 4, 140, 220)), line(arc(12, 8, 7.8, 140, 220)),
            line(arc(12, 8, 4, 320, 40)), line(arc(12, 8, 7.8, 320, 40))]


@icon("shortwave-receiver", CAT, "Tabletop radio with a long tuning scale, a large knob and a telescopic antenna",
      tags=["shortwave", "ham radio", "swl", "listening", "radio", "receiver", "dial", "world radio"])
def _(S):
    return [shell(rect(2, 9, 20, 12, S.R)), line(poly([(17.5, 9), (20.5, 2.5)])),
            detail(seg(5, 12.5, 12.5, 12.5)), detail(seg(5, 17, 12.5, 17)), detail(circle(17.5, 15, 2.4))]


@icon("radio-logbook", CAT, "Open logbook with ruled lines and a small antenna mast drawn on the left page",
      tags=["ham radio", "amateur radio", "station log", "contacts", "qso", "notebook", "ledger"])
def _(S):
    return [shell(poly([(12, 6), (3, 4.5), (3, 19), (12, 20.5), (21, 19), (21, 4.5)], closed=True, r=S.r)),
            detail(seg(12, 6, 12, 20.5)),
            detail(poly([(5.8, 7), (7.5, 9.5), (9.2, 7)])), detail(seg(7.5, 9.5, 7.5, 13)),
            detail(seg(6, 16, 9.5, 16.5)), detail(seg(15, 9, 18, 8.5)), detail(seg(15, 12, 18, 11.5)), detail(seg(15, 15.5, 18, 15.5))]


@icon("antenna-rotator", CAT, "Beam antenna seen from above with a curved rotation arrow circling around it",
      tags=["ham radio", "amateur radio", "rotor", "turn", "yagi", "beam", "antenna control"])
def _(S):
    R = 8.5
    p = polar(12, 12, R, 300)
    d = (0.866, 0.5)
    n = (-0.5, 0.866)
    w1 = (p[0] - d[0] * 3 + n[0] * 2.2, p[1] - d[1] * 3 + n[1] * 2.2)
    w2 = (p[0] - d[0] * 3 - n[0] * 2.2, p[1] - d[1] * 3 - n[1] * 2.2)
    return [line(arc(12, 12, R, 20, 300)), line(poly([w1, p, w2])),
            line(seg(6, 12, 18, 12)),
            line(seg(9, 8.2, 9, 15.8)), line(seg(15, 9, 15, 15))]


@icon("hex-beam-antenna", CAT, "Top view of a hexagonal antenna frame with six spokes around a central hub",
      tags=["ham radio", "amateur radio", "hexbeam", "wire antenna", "hexagon", "beam", "hf"])
def _(S):
    out = [shell(poly(regular(12, 12, 9.5, 6), closed=True, r=S.r))]
    for ang in range(-90, 270, 60):
        a, b = polar(12, 12, 3.2, ang), polar(12, 12, 9.5, ang)
        out.append(detail(seg(a[0], a[1], b[0], b[1])))
    out.append(dot(12, 12, 1.4))
    return out


@icon("cubical-quad-antenna", CAT, "Square wire loop antenna seen on its corner with an inner loop and four spreader arms",
      tags=["ham radio", "amateur radio", "quad", "loop antenna", "diamond", "spreaders", "hf"])
def _(S):
    out = [shell(poly([(12, 2.5), (21.5, 12), (12, 21.5), (2.5, 12)], closed=True, r=S.r * 2.2)),
           detail(poly([(12, 8.5), (15.5, 12), (12, 15.5), (8.5, 12)], closed=True, r=S.r))]
    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        out.append(detail(seg(12 + dx * 3.5, 12 + dy * 3.5, 12 + dx * 9.5, 12 + dy * 9.5)))
    return out


@icon("moonbounce", CAT, "Dish antenna aimed at a crescent moon with signal arcs travelling between them",
      tags=["ham radio", "eme", "earth moon earth", "dish", "moon", "weak signal", "amateur radio"])
def _(S):
    from geometry import path_to_d
    moon = path_to_d(D(P(circle(18, 6, 4.4)), P(circle(20.4, 4.4, 3.8))))
    return [shell("M2.5 16.5A6.5 6.5 0 0 0 15.5 16.5Z"), line(seg(9, 16.5, 9, 12.5)),
            line(arc(9, 12, 3.5, 295, 335)), line(arc(9, 12, 6.8, 305, 330))
            , shell(moon)]


@icon("sstv-image", CAT, "Small picture being drawn line by line next to radio wave arcs",
      tags=["ham radio", "slow scan tv", "picture", "image transmission", "scan lines", "amateur radio", "sstv"])
def _(S):
    return [shell(rect(2, 5, 12, 14, S.R)), detail(seg(5, 9, 11, 9)), detail(seg(5, 12.5, 11, 12.5)),
            line(arc(16, 12, 3, 315, 45)), line(arc(16, 12, 6, 315, 45))]


@icon("mobile-whip-antenna", CAT, "Car seen from the side with a long thin whip antenna bending back from the roof",
      tags=["ham radio", "amateur radio", "mobile", "vehicle", "car", "whip", "radio antenna"])
def _(S):
    return [shell(poly([(2.5, 18), (2.5, 14.5), (6, 13.5), (8.5, 10), (15.5, 10), (18.5, 13.5), (21.5, 14.5), (21.5, 18)], closed=True, r=S.r)),
            shell(circle(7, 18, 2.2)), shell(circle(17, 18, 2.2)),
            line("M14.5 10Q14.5 5 9 2.5")]


@icon("ground-plane-antenna", CAT, "Vertical antenna rod with four radial wires drooping from its base",
      tags=["ham radio", "amateur radio", "vertical antenna", "radials", "gp", "antenna", "rod"])
def _(S):
    return [line(seg(12, 2.5, 12, 12.5)), dot(12, 12.5, 1.8),
            line(poly([(12, 12.5), (3, 17)])), line(poly([(12, 12.5), (7.5, 20)])),
            line(poly([(12, 12.5), (16.5, 20)])), line(poly([(12, 12.5), (21, 17)]))]


@icon("log-periodic-antenna", CAT, "Horizontal boom with parallel elements that shorten from back to front",
      tags=["ham radio", "amateur radio", "lpda", "tv antenna", "wideband", "directional", "elements"])
def _(S):
    out = [line(seg(2, 12, 22, 12))]
    for x, h in [(4.5, 8.5), (8.5, 6.6), (12.5, 4.8), (16.5, 3.4), (20.5, 2.2)]:
        out.append(line(seg(x, 12 - h, x, 12 + h)))
    return out


@icon("discone-antenna", CAT, "Flat disc on top of a downward-opening cone of rods on a short mast",
      tags=["ham radio", "amateur radio", "wideband antenna", "scanner antenna", "disc", "cone", "vhf"])
def _(S):
    return [line(seg(6, 4.5, 18, 4.5)),
            shell(poly([(12, 8), (20, 19), (4, 19)], closed=True, r=S.r)),
            detail(seg(12, 8, 12, 19)), line(seg(12, 19, 12, 22))]


@icon("radio-field-day", CAT, "Small tent with a wire antenna strung from its peak to a pole",
      tags=["ham radio", "amateur radio", "portable", "camping", "emergency", "field day", "outdoor operating"])
def _(S):
    return [shell(poly([(2, 19), (8.5, 8), (15, 19)], closed=True, r=S.r)),
            detail(seg(8.5, 13.5, 8.5, 19)),
            line(seg(20.5, 3.5, 20.5, 19)), line(seg(8.5, 8, 20.5, 4)),
            line(seg(17, 19, 22, 19))]


@icon("amateur-satellite-contact", CAT, "Handheld crossed yagi antenna aimed up at a small satellite",
      tags=["ham radio", "amateur radio", "satellite", "oscar", "yagi", "space contact", "orbit"])
def _(S):
    def rrect(cx, cy, u0, u1, v0, v1):
        ax, ay = 0.7071, -0.7071
        px, py = 0.7071, 0.7071
        return [(cx + u * ax + v * px, cy + u * ay + v * py) for u, v in [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]]
    c = (15.5, 8.5)
    out = [shell(poly(rrect(c[0], c[1], -2, 2, -2, 2), closed=True, r=S.r * 0.6)),
           solid(poly(rrect(c[0], c[1], 3.2, 7, -1.9, 1.9), closed=True)),
           solid(poly(rrect(c[0], c[1], -7, -3.2, -1.9, 1.9), closed=True))]
    out.append(line(seg(2.5, 21.5, 10, 14)))
    for t, h in [(3, 4), (6.5, 3.2), (9.5, 2.4)]:
        px, py = 2.5 + t * 0.7071, 21.5 - t * 0.7071
        out.append(line(seg(px - 0.7071 * h, py - 0.7071 * h, px + 0.7071 * h, py + 0.7071 * h)))
    return out


@icon("j-pole-antenna", CAT, "Vertical antenna shaped like a tall letter J with a short stub beside the long element",
      tags=["ham radio", "amateur radio", "j-pole", "vhf", "vertical antenna", "stub", "homemade antenna"])
def _(S):
    return [line("M15.5 2.5V16A3.75 3.75 0 0 1 8 16V9"), line(seg(8, 13, 3.5, 13)), dot(3.5, 13, 1.6)]


@icon("end-fed-wire-antenna", CAT, "Long sloping wire running from a small house up to a tall tree",
      tags=["ham radio", "amateur radio", "end fed", "wire antenna", "long wire", "random wire", "hf"])
def _(S):
    c = (18, 7, 3.6)
    e = edge((c[0], c[1]), c[2], (11.5, 13))
    return [shell(poly([(2, 21), (2, 13), (6.5, 9), (11, 13), (11, 21)], closed=True, r=S.r)),
            Part("dot", rect(5, 15, 3, 3, 0.4)),
            line(seg(11, 13, e[0], e[1])),
            shell(circle(*c)), line(seg(18, 10.6, 18, 21))]


# ============================================================================ props, play and crafts

@icon("kendama", CAT, "Wooden skill toy with a cross-shaped handle, a spike on top and a ball hanging on a string",
      tags=["skill toy", "cup and ball", "japanese toy", "trick", "juggling", "wooden toy", "play"])
def _(S):
    return [line(seg(12, 2.5, 12, 5.5)), shell(rect(3, 5.5, 18, 4, min(S.R, 2))),
            shell(rect(10, 9.5, 4, 5, min(S.R, 1.2))),
            line(seg(12, 14.5, 12, 17)), shell(circle(12, 19, 2.2))]


@icon("juggling-balls", CAT, "Three round beanbag balls in an arc with small motion marks above",
      tags=["juggling", "circus", "balls", "cascade", "beanbag", "skill", "performance"])
def _(S):
    out = []
    for cx, cy in [(5.5, 16), (12, 8.5), (18.5, 16)]:
        out.append(shell(circle(cx, cy, 3.3)))
    out += [line("M3 10.5Q3.8 7 6.5 5.5"), line("M21 10.5Q20.2 7 17.5 5.5")]
    return out


@icon("juggling-rings", CAT, "Three thin rings flying in an arc with small motion marks above",
      tags=["juggling", "circus", "rings", "flying rings", "cascade", "skill", "performance"])
def _(S):
    return [line(ellipse(5.5, 16, 4, 2.6)), line(ellipse(12, 8.5, 4, 2.6)), line(ellipse(18.5, 16, 4, 2.6)),
            line("M3 10.5Q3.8 7 6.5 5.5"), line("M21 10.5Q20.2 7 17.5 5.5")]


@icon("spinning-plate", CAT, "Plate balanced and spinning on top of a thin vertical stick with motion lines",
      tags=["circus", "plate spinning", "balance", "stick", "juggling", "performance", "skill"])
def _(S):
    return [shell("M2.5 9C3 12.5 7.5 13 12 13S21 12.5 21.5 9Z"),
            line(seg(12, 13, 12, 22)), line("M5 5.5Q12 3 19 5.5")]


@icon("poi-balls", CAT, "Two weighted balls on cords swinging out from a central hand along circular trails",
      tags=["poi", "spinning", "fire dancing", "juggling", "swinging", "performance", "flow arts"])
def _(S):
    b1, b2 = (5, 18.5), (19, 5.5)
    out = [shell(circle(*b1, 3)), shell(circle(*b2, 3)), dot(12, 12, 1.8)]
    for b in (b1, b2):
        a = edge(b, 3, (12, 12))
        out.append(line(seg(a[0], a[1], 12, 12)))
    out += [line(arc(12, 12, 10.2, 180, 235)), line(arc(12, 12, 10.2, 0, 55))]
    return out


@icon("larp-foam-sword", CAT, "Padded foam sword with a thick rounded blade, a crossguard and a wrapped grip",
      tags=["larp", "live action role play", "foam weapon", "costume", "cosplay", "battle game", "toy sword"])
def _(S):
    return [shell(rect(9.5, 2, 5, 12.5, min(S.R, 2.4))), detail(seg(12, 5, 12, 12)),
            shell(rect(6, 14.5, 12, 2.5, min(S.R, 1.2))),
            line(seg(12, 17, 12, 20)), dot(12, 21, 1.4)]


@icon("magnet-fishing", CAT, "Round magnet on a rope pulling an old key up out of wavy water",
      tags=["magnet", "fishing", "treasure hunting", "scavenging", "rope", "water", "outdoor hobby"])
def _(S):
    return [line(seg(12, 2, 12, 5)), shell(rect(8, 5, 8, 5, min(S.R, 2))),
            shell(circle(12, 13.8, 2.2)), line(seg(12, 16, 12, 20)), line(seg(12, 18.5, 14.5, 18.5)),
            line("M2 21Q4.5 19.5 7 21T12 21T17 21T22 21")]


@icon("aquascape", CAT, "Planted aquarium tank with a rock, curved water plants and rising bubbles",
      tags=["aquarium", "fish tank", "planted tank", "aquascaping", "plants", "hardscape", "nature aquarium"])
def _(S):
    return [shell(rect(2, 4, 20, 17, S.R)),
            detail(poly([(4.5, 18), (8, 12), (11.5, 18)])),
            detail("M15 18Q13 14.5 15 11"), detail("M18.5 18Q20 15 18.5 12.5"),
            dot(13.5, 7.5, 0.9), dot(17, 6.5, 0.9)]


@icon("pond-dipping", CAT, "Small net with a long handle dipping into wavy water beside a tray holding a tiny creature",
      tags=["nature study", "pond", "net", "wildlife", "explore", "outdoor activity", "bug hunting"])
def _(S):
    return [shell("M3 11H13Q13 18.5 8 18.5Q3 18.5 3 11Z"), detail(seg(6.5, 11, 6.5, 17)), detail(seg(9.5, 11, 9.5, 17)),
            line(poly([(13, 11), (21, 3)])),
            line("M2 21.5Q4 20 6 21.5T10 21.5"), shell(rect(14, 14, 8, 6.5, min(S.R, 2))), dot(18, 17.3, 1.3)]


@icon("bullet-journal", CAT, "Open notebook with a dot grid page on the left and a bulleted task list on the right",
      tags=["journaling", "planner", "dot grid", "notebook", "to-do list", "organizing", "stationery"])
def _(S):
    out = [shell(poly([(12, 6), (3, 4.5), (3, 19), (12, 20.5), (21, 19), (21, 4.5)], closed=True, r=S.r)),
           detail(seg(12, 6, 12, 20.5))]
    for x in (6.2, 9.2):
        for y in (9, 12.5, 16):
            out.append(dot(x, y, 0.9))
    for y in (9, 12.5, 16):
        out.append(dot(14.6, y, 1.0))
        out.append(detail(seg(17, y, 18.6, y)))
    return out


@icon("crystal-growing", CAT, "Jar of solution with a string hanging from a pencil across the rim and crystals on it",
      tags=["science experiment", "crystals", "salt", "sugar", "jar", "diy science", "kids activity"])
def _(S):
    return [line(seg(3, 5.5, 21, 5.5)), shell(rect(5, 8, 14, 13, S.R)),
            detail(seg(12, 5.5, 12, 12)),
            detail(poly([(12, 12.5), (15, 15.5), (12, 19), (9, 15.5)], closed=True))]


@icon("emf-meter", CAT, "Handheld meter with a row of indicator lights across the top and a short antenna",
      tags=["ghost hunting", "electromagnetic field", "paranormal", "detector", "gauss meter", "handheld", "lights"])
def _(S):
    return [line(seg(12, 2, 12, 5)), shell(rect(5.5, 5, 13, 17, S.R)),
            dot(9, 9, 1.1), dot(12, 9, 1.1), dot(15, 9, 1.1),
            detail(rect(8.5, 12, 7, 4, 0.5)), dot(12, 19.3, 1.2)]


@icon("diamond-painting", CAT, "Canvas of small square facets with a pen applicator picking up one gem",
      tags=["craft", "gems", "rhinestones", "mosaic", "painting by numbers", "sparkle", "diy art"])
def _(S):
    return [shell(rect(2, 11, 13, 11, S.R)), detail(seg(8.5, 11, 8.5, 22)), detail(seg(2, 16.5, 15, 16.5)),
            line(seg(21.5, 2.5, 17, 7)), dot(15.3, 8.7, 1.7)]


@icon("popsicle-stick-craft", CAT, "Small house shape built from rounded craft sticks laid side by side",
      tags=["craft sticks", "lolly sticks", "kids craft", "diy", "house", "wood craft", "model"])
def _(S):
    return [shell(poly([(3, 11), (12, 3), (21, 11), (21, 21), (3, 21)], closed=True, r=S.r)),
            detail(seg(3, 11.5, 21, 11.5)), detail(seg(9, 11.5, 9, 21)), detail(seg(15, 11.5, 15, 21))]


@icon("matchstick-model", CAT, "Small sailing ship built from matchsticks with tiny round heads",
      tags=["matchsticks", "model ship", "craft", "miniature", "hobby", "diy", "wooden model"])
def _(S):
    return [line(seg(12, 3, 12, 15)), shell(poly([(12, 4.5), (19, 13.5), (12, 13.5)], closed=True, r=S.r * 0.5)),
            shell(poly([(10, 6.5), (5, 13.5), (10, 13.5)], closed=True, r=S.r * 0.5)),
            line(poly([(3, 15.5), (5.5, 20), (18.5, 20), (21, 15.5)], closed=False)), line(seg(3, 15.5, 21, 15.5)),
            dot(12, 2.5, 1.4), dot(3, 15.5, 1.5), dot(21, 15.5, 1.5)]


@icon("origami-owl", CAT, "Folded paper owl in front view with two ear points, two round eyes and a beak fold",
      tags=["origami", "paper folding", "paper craft", "bird", "owl", "folded paper", "diy"])
def _(S):
    return [shell(poly([(4.5, 3), (9, 6.5), (15, 6.5), (19.5, 3), (19.5, 15), (12, 21.5), (4.5, 15)], closed=True, r=S.r)),
            dot(8.8, 11, 1.9), dot(15.2, 11, 1.9), detail(seg(12, 14, 12, 18))]


@icon("origami-turtle", CAT, "Folded paper turtle from above with a hexagon shell, four pointed legs and a head",
      tags=["origami", "paper folding", "paper craft", "turtle", "tortoise", "folded paper", "diy"])
def _(S):
    out = [shell(poly(regular(12, 13, 6.5, 6), closed=True, r=S.r)), dot(12, 3.8, 1.9),
           detail(poly(regular(12, 13, 2.6, 6), closed=True))]
    for ang in (-30, 30, 150, 210):
        a, b = polar(12, 13, 6.5, ang), polar(12, 13, 10.6, ang)
        out.append(line(seg(a[0], a[1], b[0], b[1])))
    return out


@icon("coin-display-tray", CAT, "Flat tray with a grid of round recessed slots, two of them holding coins",
      tags=["coin collecting", "numismatics", "collection", "display", "tray", "coins", "hobby"])
def _(S):
    out = [shell(rect(2, 4.5, 20, 15, S.R))]
    for y in (9.5, 15):
        for x in (6.5, 12, 17.5):
            if (x, y) in ((12, 9.5), (17.5, 15)):
                out.append(detail(circle(x, y, 2.1)))
            else:
                out.append(dot(x, y, 1.1))
    return out


@icon("stamp-booklet", CAT, "Folded card booklet opened to show a pane of six perforated stamps",
      tags=["stamp collecting", "philately", "postage", "booklet", "stamps", "mail", "collection"])
def _(S):
    return [shell(rect(2, 4, 20, 16, S.R)), detail(rect(5.5, 7.5, 13, 9)),
            detail(seg(9.8, 7.5, 9.8, 16.5)), detail(seg(14.2, 7.5, 14.2, 16.5)), detail(seg(5.5, 12, 18.5, 12))]


@icon("rose-arch", CAT, "Curved garden arch with climbing rose blooms along both sides",
      tags=["garden", "roses", "arbour", "trellis", "climbing plants", "flowers", "landscaping"])
def _(S):
    out = [line("M5 21.5V10A7 7 0 0 1 19 10V21.5")]
    for x, y in [(5, 17), (5, 12.5), (7.2, 5.6), (13.5, 3.2), (18.8, 7.5), (19, 14)]:
        out.append(dot(x, y, 2.1))
    return out


@icon("gear-drawing-set", CAT, "Round spirograph gear ring tracing a looping rosette pattern",
      tags=["spirograph", "drawing", "geometric art", "gears", "pattern", "toy", "stencil"])
def _(S):
    pts = []
    Rr, r, dd = 8.0, 3.0, 2.4
    n = 90
    for i in range(n + 1):
        t = 2 * math.pi * 3 * i / n
        pts.append((12 + (Rr - r) * math.cos(t) + dd * math.cos((Rr - r) / r * t),
                    12 + (Rr - r) * math.sin(t) - dd * math.sin((Rr - r) / r * t)))
    return [shell(circle(12, 12, 9.5)), detail(poly(pts, closed=True))]


@icon("wargame-terrain", CAT, "Broken stone wall ruin with a crumbled top edge and a rubble block on a round base",
      tags=["tabletop wargaming", "miniatures", "scenery", "ruins", "stone wall", "terrain", "hobby model"])
def _(S):
    return [shell(poly([(4, 18), (4, 7), (8, 7), (8, 10), (12, 10), (12, 4), (16, 4), (16, 18)], closed=True, r=S.r)),
            detail(seg(4, 13.5, 16, 13.5)), detail(seg(10, 13.5, 10, 18)),
            solid(rect(18, 15, 3.5, 3.5)), line("M2.5 18.8A9.5 2 0 0 0 21.5 18.8")]


@icon("old-family-photo", CAT, "Old photograph with three standing figures and a mounting corner",
      tags=["genealogy", "family history", "vintage photo", "portrait", "heirloom", "memories", "album"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)),
            dot(7.5, 8.5, 1.5), detail(seg(7.5, 11.5, 7.5, 17)),
            dot(12, 10.5, 1.5), detail(seg(12, 13.5, 12, 17)),
            dot(16.5, 8.5, 1.5), detail(seg(16.5, 11.5, 16.5, 17))]


@icon("family-recipe-card", CAT, "Index card with handwritten lines and a small heart in the corner",
      tags=["genealogy", "family history", "recipe", "cooking", "heirloom", "card", "kitchen"])
def _(S):
    heart = "M17 15C12.5 12 14.5 7.5 16.5 8.5 16.8 8.7 17 9.2 17 9.2S17.2 8.7 17.5 8.5C19.5 7.5 21.5 12 17 15Z"
    return [shell(rect(2, 4, 20, 16, S.R)),
            detail(seg(5.5, 8.5, 12.5, 8.5)), detail(seg(5.5, 12.5, 12.5, 12.5)), detail(seg(5.5, 16.5, 10.5, 16.5)),
            Part("dot", heart)]


@icon("jigsaw-roll-mat", CAT, "Felt mat partly rolled around a tube with jigsaw pieces lying on the flat part",
      tags=["jigsaw", "puzzle", "puzzle mat", "storage", "felt", "roll up", "puzzle accessory"])
def _(S):
    return [shell(rect(8.5, 8, 13, 11, S.R)),
            shell(circle(8.5, 13.5, 5.5)), detail(circle(8.5, 13.5, 2)),
            Part("dot", rect(14.5, 10.5, 3, 3)), Part("dot", circle(18.1, 12, 1.0)),
            Part("dot", rect(16, 15, 3, 3)), Part("dot", circle(14.6, 16.5, 1.0))]
