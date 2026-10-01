"""TypeIcon Core: writing-system letters (Greek, Cyrillic, Hebrew, Arabic), batch 1.

Each letter is a simple 2 px stroke skeleton drawn by hand (not font text). Cap height runs y 4 to 20 for
Cyrillic and Greek capitals, lowercase Greek sits between y 8 and 20, Hebrew letters sit in a y 6 to 19 box and
Arabic letters use a low baseline with dots above or below. All parts are open strokes, so Filled keeps the
counters and only gets a heavier stroke; Rounded gets round caps/joins and 1.5 px fillets on straight corners.
"""
from dsl import circle, dot, ellipse, icon, line, poly, rect, seg  # noqa: F401

CAT = "scripts"


def pl(S, *pts, closed=False, miter=None):
    """Polyline stroke with the style's corner fillet (miter caps the spike on acute joins)."""
    d = poly(list(pts), closed=closed, r=S.r)
    return line(d, stroke_miterlimit=str(miter)) if miter else line(d)


def pa(d):
    """Raw path stroke."""
    return line(d)


# ============================================================================ Greek

@icon("greek-lowercase-delta", CAT, "Lowercase Greek letter delta with a round bowl and a hooked stem.",
      tags=["delta", "greek", "letter", "lowercase", "change", "alphabet"])
def _(S):
    return [pa(circle(11.5, 15, 5)), pa("M11.5 10C10 7 12 4 17.5 5")]


@icon("greek-lowercase-omega", CAT, "Lowercase Greek letter omega, a wide w made of two joined bowls.",
      tags=["omega", "greek", "letter", "lowercase", "alphabet", "end"])
def _(S):
    return [pa("M4.5 9V13.5C4.5 20 12 20 12 12.5C12 20 19.5 20 19.5 13.5V9")]


@icon("greek-lowercase-sigma", CAT, "Lowercase Greek letter sigma, a round bowl with a bar running out to the right.",
      tags=["sigma", "greek", "letter", "lowercase", "alphabet", "sum"])
def _(S):
    return [pa(circle(10.5, 14.5, 5.5)), pa("M10.5 9H19.5")]


@icon("greek-final-sigma", CAT, "Greek final sigma, a c shape whose lower end curls into a small hook.",
      tags=["sigma", "final sigma", "greek", "letter", "word ending", "alphabet"])
def _(S):
    return [pa("M18 8C11 5.5 5.5 8 5.5 12.5C5.5 16.5 8.5 18 11.5 18C15 18 16 19 15.5 21")]


@icon("greek-theta-symbol", CAT, "Greek cursive theta symbol, an oval with a looped hook over the top right.",
      tags=["theta", "theta symbol", "greek", "letter", "angle", "alphabet"])
def _(S):
    return [pa(ellipse(10.5, 14, 5, 6)), pa("M8 9C7 5 12 3 17 4C19.5 4.5 19 8 16 8.5")]


@icon("greek-koppa", CAT, "Archaic Greek koppa, a circle sitting on a short vertical stem.",
      tags=["koppa", "qoppa", "greek", "archaic", "letter", "alphabet"])
def _(S):
    return [pa(circle(12, 10, 6)), pa("M12 16V20")]


@icon("greek-sampi", CAT, "Greek sampi, a large arch curving to the lower left with two short diagonals inside.",
      tags=["sampi", "greek", "archaic", "numeral", "letter", "alphabet"])
def _(S):
    return [pa("M19 12C19 7 15 5 11.5 5.5C7.5 6 5 9 5 14"), pa("M12 10L9 19"), pa("M17 12L14 19")]


@icon("greek-stigma", CAT, "Greek stigma, a final sigma with a small flick at the top and a hook below.",
      tags=["stigma", "sigma tau", "greek", "numeral", "letter", "alphabet"])
def _(S):
    return [pa("M19.5 5H14C8 5 5.5 8 5.5 12.5C5.5 17 8.5 18.5 11.5 18.5C15 18.5 16 19.5 15.5 21.5")]


# ============================================================================ Cyrillic (capitals, y 4 to 20)

@icon("cyrillic-be", CAT, "Cyrillic capital Be: a stem with a flat top bar and a closed bowl at the lower right.",
      tags=["be", "cyrillic", "russian", "letter", "capital", "alphabet", "b"])
def _(S):
    return [pa("M18 4H6.5V20H13A4 4 0 0 0 13 12H6.5")]


@icon("cyrillic-ghe", CAT, "Cyrillic capital Ghe: a vertical stem with one arm across the top.",
      tags=["ghe", "ge", "cyrillic", "russian", "letter", "capital", "alphabet", "g"])
def _(S):
    return [pl(S, (7, 20), (7, 4), (17, 4))]


@icon("cyrillic-ghe-with-upturn", CAT, "Cyrillic capital Ghe with upturn, used in Ukrainian: the top arm ends in a tick.",
      tags=["ghe", "upturn", "cyrillic", "ukrainian", "letter", "capital", "alphabet"])
def _(S):
    return [pl(S, (7, 20), (7, 8), (16, 8), (16, 4))]


@icon("cyrillic-ghe-with-stroke", CAT, "Cyrillic capital Ghe with stroke: an upside down L crossed by a short bar.",
      tags=["ghe", "stroke", "cyrillic", "kazakh", "letter", "capital", "alphabet"])
def _(S):
    return [pl(S, (8.5, 20), (8.5, 4), (18, 4)), pa("M5 12H13")]


@icon("cyrillic-de", CAT, "Cyrillic capital De: a narrow frame on a wide base bar with two short feet.",
      tags=["de", "cyrillic", "russian", "letter", "capital", "alphabet", "d"])
def _(S):
    return [pl(S, (8.5, 18), (10.5, 5), (16.5, 5), (16.5, 18)), pl(S, (5.5, 21), (5.5, 18), (19.5, 18), (19.5, 21))]


@icon("cyrillic-i", CAT, "Cyrillic capital I: two vertical stems joined by a diagonal, like a mirrored N.",
      tags=["i", "cyrillic", "russian", "letter", "capital", "alphabet", "mirrored n"])
def _(S):
    return [pl(S, (7, 4), (7, 20), (17, 4), (17, 20), miter=1.5)]


@icon("cyrillic-short-i", CAT, "Cyrillic capital Short I: the mirrored N shape topped by a small curved breve.",
      tags=["short i", "i kratkoe", "cyrillic", "russian", "letter", "capital", "alphabet", "breve"])
def _(S):
    return [pl(S, (7, 11), (7, 20), (17, 11), (17, 20), miter=1.5), pa("M9 3.5C9.5 7.5 14.5 7.5 15 3.5")]


@icon("cyrillic-el", CAT, "Cyrillic capital El: a flat top bar on a straight right leg and a left leg that sweeps outward.",
      tags=["el", "ell", "cyrillic", "russian", "letter", "capital", "alphabet", "l"])
def _(S):
    return [pa("M5 20C8 19 9 12 9 4H17.5V20")]


@icon("cyrillic-pe", CAT, "Cyrillic capital Pe: two vertical stems joined by a flat top bar.",
      tags=["pe", "cyrillic", "russian", "letter", "capital", "alphabet", "p", "doorway"])
def _(S):
    return [pl(S, (7, 20), (7, 4), (17, 4), (17, 20))]


@icon("cyrillic-tse", CAT, "Cyrillic capital Tse: a squared U whose base runs out into a short descender tail.",
      tags=["tse", "ts", "cyrillic", "russian", "letter", "capital", "alphabet", "tail"])
def _(S):
    return [pl(S, (5.5, 4), (5.5, 17), (19, 17), (19, 21)), pa("M15 4V17")]


@icon("cyrillic-che", CAT, "Cyrillic capital Che: a short left stem curving into a bar that meets a tall right stem.",
      tags=["che", "ch", "cyrillic", "russian", "letter", "capital", "alphabet"])
def _(S):
    return [pa("M6.5 4V8C6.5 11.5 8.5 13 12.5 13H17"), pa("M17 4V20")]


@icon("cyrillic-sha", CAT, "Cyrillic capital Sha: three vertical stems joined by a flat base, like a comb.",
      tags=["sha", "sh", "cyrillic", "russian", "letter", "capital", "alphabet", "comb"])
def _(S):
    return [pl(S, (5, 4), (5, 20), (19, 20), (19, 4)), pa("M12 4V20")]


@icon("cyrillic-shcha", CAT, "Cyrillic capital Shcha: the three pronged Sha with a short tail under its lower right corner.",
      tags=["shcha", "shch", "cyrillic", "russian", "letter", "capital", "alphabet", "tail"])
def _(S):
    return [pl(S, (4.5, 4), (4.5, 17), (18.5, 17), (18.5, 21)), pa("M11.5 4V17"), pa("M18.5 4V17")]


@icon("cyrillic-hard-sign", CAT, "Cyrillic capital Hard Sign: a short top bar on a stem with a closed bowl at the lower right.",
      tags=["hard sign", "yer", "tverdy znak", "cyrillic", "russian", "letter", "capital", "alphabet"])
def _(S):
    return [pa("M4.5 5H9.5V20H14.5A4 4 0 0 0 14.5 12H9.5")]


@icon("cyrillic-soft-sign", CAT, "Cyrillic capital Soft Sign: a plain stem with a closed bowl at the lower right.",
      tags=["soft sign", "yer", "myagkiy znak", "cyrillic", "russian", "letter", "capital", "alphabet"])
def _(S):
    return [pa("M7 4V20H13A4 4 0 0 0 13 12H7")]


@icon("cyrillic-yeru", CAT, "Cyrillic capital Yeru: a stem with a bowl followed by a separate tall bar on the right.",
      tags=["yeru", "yery", "y", "cyrillic", "russian", "letter", "capital", "alphabet"])
def _(S):
    return [pa("M5 4V20H10.5A4 4 0 0 0 10.5 12H5"), pa("M19 4V20")]


@icon("cyrillic-e", CAT, "Cyrillic capital E: a backwards C opening to the left with a short bar across the middle.",
      tags=["e", "e oborotnoe", "cyrillic", "russian", "letter", "capital", "alphabet", "reversed e"])
def _(S):
    return [pa("M5.5 5.5C11 3 17 5 17 12C17 19 11 21 5.5 18.5"), pa("M8 12H17")]


@icon("cyrillic-yu", CAT, "Cyrillic capital Yu: a stem on the left joined by a short bar to a tall oval.",
      tags=["yu", "cyrillic", "russian", "letter", "capital", "alphabet"])
def _(S):
    return [pa("M4.5 4V20"), pa("M4.5 12H9"), pa(ellipse(14, 12, 5, 8))]


@icon("cyrillic-ya", CAT, "Cyrillic capital Ya: a mirrored R with a bowl at the upper left and a leg kicking out to the lower left.",
      tags=["ya", "cyrillic", "russian", "letter", "capital", "alphabet", "mirrored r"])
def _(S):
    return [pa("M17 20V4H11A4 4 0 0 0 11 12H17"), pa("M10.5 12L6 20")]


@icon("cyrillic-yo", CAT, "Cyrillic capital Yo: an E with three arms topped by two dots.",
      tags=["yo", "e with diaeresis", "cyrillic", "russian", "letter", "capital", "alphabet", "umlaut"])
def _(S):
    return [pl(S, (17, 9), (7, 9), (7, 20), (17, 20)), pa("M7 14.5H15"), dot(9.5, 4.5, 1.5), dot(14.5, 4.5, 1.5)]


@icon("cyrillic-ukrainian-ie", CAT, "Cyrillic capital Ukrainian Ie: a C opening to the right with a short bar across the middle.",
      tags=["ie", "ukrainian ie", "ye", "cyrillic", "ukrainian", "letter", "capital", "alphabet"])
def _(S):
    return [pa("M18.5 6C13 3.5 7 5.5 7 12C7 18.5 13 20.5 18.5 18"), pa("M7 12H12.5")]


@icon("cyrillic-yi", CAT, "Cyrillic capital Yi, used in Ukrainian: a single stem with two dots above.",
      tags=["yi", "ukrainian yi", "i with diaeresis", "cyrillic", "ukrainian", "letter", "capital", "alphabet"])
def _(S):
    return [pa("M12 10V20"), dot(8.5, 5.5, 1.5), dot(15.5, 5.5, 1.5)]


@icon("cyrillic-dje", CAT, "Cyrillic capital Dje, used in Serbian: a top bar over a stem with a humped arm ending in a hook.",
      tags=["dje", "serbian", "cyrillic", "letter", "capital", "alphabet", "hook"])
def _(S):
    return [pa("M4.5 5H17.5"), pa("M8 5V19"), pa("M8 12C11 10 16 10 16 14V17C16 19.5 14.5 20.5 12.5 20")]


@icon("cyrillic-tshe", CAT, "Cyrillic capital Tshe, used in Serbian: a top bar over a stem with a humped arm, like an h.",
      tags=["tshe", "serbian", "cyrillic", "letter", "capital", "alphabet", "h"])
def _(S):
    return [pa("M4.5 5H17.5"), pa("M8 5V20"), pa("M8 12C11 10 16 10 16 14V20")]


@icon("cyrillic-lje", CAT, "Cyrillic capital Lje, used in Serbian: the El shape joined to a stem with a closed bowl.",
      tags=["lje", "serbian", "cyrillic", "letter", "capital", "alphabet", "lj", "ligature"])
def _(S):
    return [pa("M3.5 20C6 19 7 12 7 5H11V20H14.5A4 4 0 0 0 14.5 12H11")]


@icon("cyrillic-nje", CAT, "Cyrillic capital Nje, used in Serbian: an H whose right stem carries a closed bowl.",
      tags=["nje", "serbian", "cyrillic", "letter", "capital", "alphabet", "nj", "ligature"])
def _(S):
    return [pa("M5 4V20"), pa("M5 12H11"), pa("M11 4V20H14.5A4 4 0 0 0 14.5 12H11")]


@icon("cyrillic-dzhe", CAT, "Cyrillic capital Dzhe: a squared U with a short stem dropping from the centre of its base.",
      tags=["dzhe", "dzh", "serbian", "macedonian", "cyrillic", "letter", "capital", "alphabet"])
def _(S):
    return [pl(S, (6, 4), (6, 16), (18, 16), (18, 4)), pa("M12 16V21")]


@icon("cyrillic-short-u", CAT, "Cyrillic capital Short U, used in Belarusian: a y shape with a curved breve above.",
      tags=["short u", "belarusian", "cyrillic", "letter", "capital", "alphabet", "breve", "u"])
def _(S):
    return [pa("M6 11L12.5 17.5"), pa("M18 11L9.5 21"), pa("M9 3.5C9.5 7.5 14.5 7.5 15 3.5")]


@icon("cyrillic-yat", CAT, "Historic Cyrillic capital Yat: a tall stem crossed near the top by a bar, with a bowl at the lower right.",
      tags=["yat", "jat", "historic", "old russian", "cyrillic", "letter", "capital", "alphabet"])
def _(S):
    return [pa("M7.5 4V20H13.5A4 4 0 0 0 13.5 12H7.5"), pa("M4 7.5H12")]


@icon("cyrillic-en-with-descender", CAT, "Cyrillic capital En with descender, used in Kazakh: an H with a tail under its right stem.",
      tags=["en", "descender", "kazakh", "cyrillic", "letter", "capital", "alphabet", "ng", "tail"])
def _(S):
    return [pl(S, (5.5, 4), (5.5, 17)), pa("M5.5 10.5H15.5"), pl(S, (15.5, 4), (15.5, 17), (19, 17), (19, 21))]


@icon("cyrillic-big-yus", CAT, "Historic Cyrillic capital Big Yus: a small triangle on a wide bar with a stem and two splayed legs.",
      tags=["big yus", "yus", "historic", "old church slavonic", "cyrillic", "letter", "capital", "alphabet"])
def _(S):
    return [pl(S, (12, 4), (8.5, 10), (15.5, 10), closed=True), pa("M4 10H20"), pa("M12 10V20"),
            pa("M8.5 10L5 20"), pa("M15.5 10L19 20")]


@icon("cyrillic-little-yus", CAT, "Historic Cyrillic capital Little Yus: a tall A shape with a short stem hanging from the crossbar.",
      tags=["little yus", "yus", "historic", "old church slavonic", "cyrillic", "letter", "capital", "alphabet"])
def _(S):
    return [pl(S, (5, 20), (12, 4), (19, 20), miter=2), pa("M8 12.5H16"), pa("M12 12.5V19")]


@icon("cyrillic-ksi", CAT, "Historic Cyrillic capital Ksi: a double bowl like a 3 with a check mark above and a tail below.",
      tags=["ksi", "xi", "historic", "old church slavonic", "cyrillic", "letter", "capital", "alphabet"])
def _(S):
    return [pa("M8.5 3.5L11 6 15.5 3"), pa("M6.5 8.5H13A2.5 2.5 0 0 1 13 13.5H9.5"),
            pa("M13 13.5A2.75 2.75 0 0 1 13 19H9.5C7 19 6.5 21 8.5 21.5")]


# ============================================================================ Hebrew (y 6 to 19 box)

@icon("hebrew-bet", CAT, "Hebrew letter bet: a flat roof and right wall over a base that juts past the wall.",
      tags=["bet", "beth", "hebrew", "letter", "alphabet", "b", "aleph-bet"])
def _(S):
    return [pl(S, (5.5, 6.5), (16, 6.5), (16, 18.5)), pa("M5.5 18.5H19")]


@icon("hebrew-gimel", CAT, "Hebrew letter gimel: a narrow stroke with a small head and a foot kicking out to the lower left.",
      tags=["gimel", "gimmel", "hebrew", "letter", "alphabet", "g", "aleph-bet"])
def _(S):
    return [pl(S, (8.5, 6.5), (14.5, 6.5), (14.5, 13), (9, 19))]


@icon("hebrew-dalet", CAT, "Hebrew letter dalet: a wide flat roof overhanging a single right leg.",
      tags=["dalet", "daleth", "hebrew", "letter", "alphabet", "d", "aleph-bet"])
def _(S):
    return [pa("M4.5 6.5H19.5"), pa("M16 6.5V19")]


@icon("hebrew-he", CAT, "Hebrew letter he: a flat roof on a full right leg with a shorter left leg floating below.",
      tags=["he", "hey", "hebrew", "letter", "alphabet", "h", "aleph-bet"])
def _(S):
    return [pl(S, (5, 6.5), (17.5, 6.5), (17.5, 19)), pa("M8 11V19")]


@icon("hebrew-vav", CAT, "Hebrew letter vav: a single vertical stroke with a small head tipping to the left.",
      tags=["vav", "waw", "vau", "hebrew", "letter", "alphabet", "v", "aleph-bet"])
def _(S):
    return [pl(S, (8.5, 6.5), (13.5, 6.5), (13.5, 19))]


@icon("hebrew-zayin", CAT, "Hebrew letter zayin: a vertical stroke topped by a short horizontal head.",
      tags=["zayin", "zain", "hebrew", "letter", "alphabet", "z", "aleph-bet"])
def _(S):
    return [pa("M8.5 6.5H15.5"), pa("M12 6.5V19")]


@icon("hebrew-het", CAT, "Hebrew letter het: a flat roof resting on two full length legs, like a doorway.",
      tags=["het", "chet", "heth", "hebrew", "letter", "alphabet", "kh", "aleph-bet"])
def _(S):
    return [pl(S, (6, 19), (6, 6.5), (18, 6.5), (18, 19))]


@icon("hebrew-tet", CAT, "Hebrew letter tet: a rounded cup open at the top whose left arm curls inward into a hook.",
      tags=["tet", "teth", "hebrew", "letter", "alphabet", "t", "aleph-bet"])
def _(S):
    return [pa("M17.5 6V13A6 6 0 0 1 5.5 13V10C5.5 8 8 7 10.5 9")]


@icon("hebrew-yod", CAT, "Hebrew letter yod: a small comma shaped stroke hanging from a tiny head.",
      tags=["yod", "yud", "hebrew", "letter", "alphabet", "y", "aleph-bet", "smallest letter"])
def _(S):
    return [pa("M9 7H13.5C15 7 15.5 8.5 14.5 10.5L11.5 15")]


@icon("hebrew-kaf", CAT, "Hebrew letter kaf: a rounded backwards C open to the left with curved top and bottom strokes.",
      tags=["kaf", "kaph", "hebrew", "letter", "alphabet", "k", "aleph-bet"])
def _(S):
    return [pa("M5.5 6.5H11C16 6.5 18 8.5 18 12.5C18 16.5 16 18.5 11 18.5H5.5")]


@icon("hebrew-lamed", CAT, "Hebrew letter lamed: a tall stem that turns into a horizontal stroke and curves down into a hook.",
      tags=["lamed", "lamedh", "hebrew", "letter", "alphabet", "l", "aleph-bet", "ascender"])
def _(S):
    return [pa("M7.5 4V9.5H13C16 9.5 18 11.5 18 14C18 17 15 19 10.5 19")]


@icon("hebrew-mem", CAT, "Hebrew letter mem: a slanted left stroke over a flat base and right wall with a gap at the lower left.",
      tags=["mem", "hebrew", "letter", "alphabet", "m", "aleph-bet"])
def _(S):
    return [pl(S, (9, 18.5), (17.5, 18.5), (17.5, 6.5), (11.5, 6.5), (6, 14))]


@icon("hebrew-nun", CAT, "Hebrew letter nun: a narrow backwards C with a short roof, a right stem and a base running left.",
      tags=["nun", "hebrew", "letter", "alphabet", "n", "aleph-bet"])
def _(S):
    return [pl(S, (11, 6.5), (16.5, 6.5), (16.5, 18.5), (6, 18.5))]


@icon("hebrew-samekh", CAT, "Hebrew letter samekh: a closed rounded loop whose flat top bar overhangs at the upper left.",
      tags=["samekh", "samech", "hebrew", "letter", "alphabet", "s", "aleph-bet", "loop"])
def _(S):
    return [pa(rect(8, 6.5, 10, 12.5, min(S.R + 1, 4))), pa("M4.5 6.5H9")]


@icon("hebrew-ayin", CAT, "Hebrew letter ayin: two upright strokes in a y shape, the right one curving into a tail along the base.",
      tags=["ayin", "ain", "hebrew", "letter", "alphabet", "aleph-bet", "eye"])
def _(S):
    return [pa("M17.5 6.5V11C17.5 16.5 13 18.5 6.5 18.5"), pa("M7 6.5L11.5 14")]


@icon("hebrew-pe", CAT, "Hebrew letter pe: a rounded backwards C open to the left with a small curl at its top left corner.",
      tags=["pe", "peh", "hebrew", "letter", "alphabet", "p", "f", "aleph-bet"])
def _(S):
    return [pa("M6.5 11.5C6 8 8 6.5 11 6.5H13C16.5 6.5 18 8.5 18 12.5C18 16.5 16 18.5 12 18.5H5.5")]


@icon("hebrew-tsadi", CAT, "Hebrew letter tsadi: slanted left and right arms joined above a flat base that extends left.",
      tags=["tsadi", "tzadi", "tsade", "hebrew", "letter", "alphabet", "ts", "aleph-bet"])
def _(S):
    return [pl(S, (6, 6.5), (11.5, 12.5), (11.5, 18.5), (5.5, 18.5), miter=2), pa("M17 6.5L11.5 12.5")]


@icon("hebrew-qof", CAT, "Hebrew letter qof: a flat roof curving down on the right and a separate long stem dropping below the base.",
      tags=["qof", "kuf", "koof", "hebrew", "letter", "alphabet", "q", "aleph-bet"])
def _(S):
    return [pa("M5.5 6.5H13C16 6.5 17.5 8 17.5 11V13"), pa("M8 11.5V21")]


@icon("hebrew-resh", CAT, "Hebrew letter resh: a short roof on a single right leg with a rounded top right corner.",
      tags=["resh", "hebrew", "letter", "alphabet", "r", "aleph-bet"])
def _(S):
    return [pa("M5.5 6.5H12C15.5 6.5 17 8 17 11.5V19")]


@icon("hebrew-shin", CAT, "Hebrew letter shin: three upright arms joined at a curved base, spreading up like a crown.",
      tags=["shin", "sin", "hebrew", "letter", "alphabet", "sh", "aleph-bet", "crown"])
def _(S):
    return [pa("M5.5 6.5V12C5.5 17 8 19 12 19C16 19 18.5 17 18.5 12V6.5"), pa("M12 19V8")]


@icon("hebrew-tav", CAT, "Hebrew letter tav: a flat roof on a right leg with a left leg ending in a small foot.",
      tags=["tav", "taw", "hebrew", "letter", "alphabet", "t", "aleph-bet", "last letter"])
def _(S):
    return [pl(S, (5, 6.5), (17.5, 6.5), (17.5, 19)), pl(S, (9.5, 6.5), (9.5, 19), (5.5, 19))]


@icon("hebrew-final-kaf", CAT, "Hebrew final kaf: a short flat roof bending into a long vertical stem that drops below the line.",
      tags=["final kaf", "kaf sofit", "hebrew", "letter", "alphabet", "word ending", "aleph-bet"])
def _(S):
    return [pa("M5.5 6.5H11.5C14.5 6.5 15.5 8 15.5 10.5V21")]


@icon("hebrew-final-mem", CAT, "Hebrew final mem: a closed box with a flat base and a small notch at the top left corner.",
      tags=["final mem", "mem sofit", "hebrew", "letter", "alphabet", "word ending", "aleph-bet", "box"])
def _(S):
    return [pl(S, (6, 11), (6, 19), (18, 19), (18, 6.5), (10.5, 6.5))]


@icon("hebrew-final-pe", CAT, "Hebrew final pe: a roof with an inward curl at the left joined to a long right stem below the line.",
      tags=["final pe", "pe sofit", "hebrew", "letter", "alphabet", "word ending", "aleph-bet"])
def _(S):
    return [pa("M6 11C5.5 8 7.5 6.5 10.5 6.5H12.5C15 6.5 16 8 16 10.5V21")]


@icon("hebrew-final-tsadi", CAT, "Hebrew final tsadi: two short arms meeting on a long straight stem that descends below the line.",
      tags=["final tsadi", "tsadi sofit", "hebrew", "letter", "alphabet", "word ending", "aleph-bet"])
def _(S):
    return [pl(S, (6.5, 7.5), (11.5, 12.5), (11.5, 21)), pa("M17 6.5L11.5 12.5")]


# ============================================================================ Arabic (low baseline, dots above or below)

def _bowl(y):
    """Shallow canoe bowl whose lowest point sits at y."""
    return pa(f"M4 {y - 6}C4 {y - 1.5} 7 {y} 10 {y}H14C17 {y} 20 {y - 1.5} 20 {y - 6}")


def _hook(top, bottom=None, tail=19):
    """Folded top stroke over a deep reversed C sweep (jim, hah, kha family)."""
    b = top + 10.5 if bottom is None else bottom
    return pa(f"M17 {top}H11A{(b - top) / 2:g} {(b - top) / 2:g} 0 0 0 11 {b}H{tail}")


def _dal(y):
    """Small angular hook: slanted stroke bending into a base that runs left."""
    return [(13, y), (16, y + 9.5), (7, y + 9.5)]


def _ra(y):
    """Comma like stroke sweeping down to the left."""
    return pa(f"M16 {y}C16.5 {y + 5.5} 14 {y + 10} 7 {y + 11.5}")


def _teeth(y):
    """Three upright teeth on a baseline that ends in a deep round bowl on the left."""
    return [pa(f"M17.5 {y - 5}V{y}"), pa(f"M13 {y - 5}V{y}"), pa(f"M8.5 {y - 5}V{y}"),
            pa(f"M19 {y}H9C5.5 {y} 4 {y + 2} 4 {y + 3.5}C4 {y + 5.5} 6 {y + 6} 9 {y + 6}H14")]


def _sad(y):
    """Flat loop lying on its side on a baseline that ends in a deep round bowl."""
    return [pa(ellipse(14, y - 3.5, 5, 3.5)),
            pa(f"M19 {y}H9C5.5 {y} 4 {y + 2} 4 {y + 3.5}C4 {y + 5.5} 6 {y + 6} 9 {y + 6}H14")]


@icon("arabic-ba", CAT, "Arabic letter ba: a wide shallow bowl like a canoe with one dot below.",
      tags=["ba", "baa", "arabic", "letter", "alphabet", "b", "dot below"])
def _(S):
    return [_bowl(14), dot(12, 19, 1.6)]


@icon("arabic-ta", CAT, "Arabic letter ta: the shallow bowl with two dots side by side above it.",
      tags=["ta", "taa", "arabic", "letter", "alphabet", "t", "two dots"])
def _(S):
    return [_bowl(19), dot(9.5, 9, 1.6), dot(14.5, 9, 1.6)]


@icon("arabic-tha", CAT, "Arabic letter tha: the shallow bowl with three dots in a small triangle above it.",
      tags=["tha", "thaa", "arabic", "letter", "alphabet", "th", "three dots"])
def _(S):
    return [_bowl(19), dot(12, 5.2, 1.5), dot(8.5, 10, 1.5), dot(15.5, 10, 1.5)]


@icon("arabic-jim", CAT, "Arabic letter jim: a folded top stroke over a deep reversed C sweep with one dot inside.",
      tags=["jim", "jeem", "arabic", "letter", "alphabet", "j", "dot inside"])
def _(S):
    return [_hook(5), dot(12.5, 10.5, 1.6)]


@icon("arabic-hah", CAT, "Arabic letter hah: a folded top stroke over a deep reversed C sweep with no dots.",
      tags=["hah", "haa", "arabic", "letter", "alphabet", "h", "no dots"])
def _(S):
    return [_hook(6.5)]


@icon("arabic-kha", CAT, "Arabic letter kha: the folded top stroke and deep reversed C sweep with one dot above.",
      tags=["kha", "khaa", "arabic", "letter", "alphabet", "kh", "dot above"])
def _(S):
    return [_hook(9.5), dot(13, 4.5, 1.6)]


@icon("arabic-dal", CAT, "Arabic letter dal: a small angular hook, a slanted stroke bending into a flat base.",
      tags=["dal", "daal", "arabic", "letter", "alphabet", "d", "hook"])
def _(S):
    return [pl(S, *_dal(8))]


@icon("arabic-dhal", CAT, "Arabic letter dhal: the small angular dal hook with one dot above it.",
      tags=["dhal", "thal", "dhaal", "arabic", "letter", "alphabet", "dh", "dot above"])
def _(S):
    return [pl(S, *_dal(11)), dot(12, 5, 1.6)]


@icon("arabic-ra", CAT, "Arabic letter ra: a small curved stroke like a comma sweeping down to the left.",
      tags=["ra", "raa", "arabic", "letter", "alphabet", "r", "comma"])
def _(S):
    return [_ra(7)]


@icon("arabic-zay", CAT, "Arabic letter zay: the comma shaped ra stroke with one dot above it.",
      tags=["zay", "zayn", "zai", "arabic", "letter", "alphabet", "z", "dot above"])
def _(S):
    return [_ra(10.5), dot(13, 5, 1.6)]


@icon("arabic-sin", CAT, "Arabic letter sin: three small upward teeth ending on the left in a deep round bowl.",
      tags=["sin", "seen", "arabic", "letter", "alphabet", "s", "teeth"])
def _(S):
    return _teeth(11)


@icon("arabic-shin", CAT, "Arabic letter shin: the three toothed sin with three dots in a triangle above the teeth.",
      tags=["shin", "sheen", "arabic", "letter", "alphabet", "sh", "three dots"])
def _(S):
    return _teeth(14.5) + [dot(12, 3.8, 1.3), dot(9, 6.8, 1.3), dot(15, 6.8, 1.3)]


@icon("arabic-sad", CAT, "Arabic letter sad: a flat closed loop on its side ending on the left in a deep round bowl.",
      tags=["sad", "saad", "arabic", "letter", "alphabet", "s", "loop"])
def _(S):
    return _sad(12.5)


@icon("arabic-dad", CAT, "Arabic letter dad: the flat side loop and deep bowl of sad with one dot above the loop.",
      tags=["dad", "daad", "arabic", "letter", "alphabet", "d", "dot above", "loop"])
def _(S):
    return _sad(15) + [dot(14, 4.8, 1.6)]
