"""TypeIcon Core: Devanagari consonant letters, batch 004 (dha to gya).

Each letter is a hand drawn 2 px stroke skeleton: a headline bar at y 5.5 and a vertical stem at x 16.5 running
to y 20, with the left hand shapes drawn from the letter itself. All parts are open strokes, so Filled keeps the
counters with a heavier stroke and Rounded gets round caps and joins.
"""
from dsl import circle, icon, line, poly, seg  # noqa: F401

CAT = "scripts"
H = 5.5   # headline y
X = 16.5  # stem x


def pa(d):
    return line(d)


def head(x1=3, x2=21):
    return pa(seg(x1, H, x2, H))


def stem(y1=H):
    return pa(seg(X, y1, X, 20))


@icon("devanagari-dha", CAT, "Devanagari letter dha, a curled loop on the left joined to a tall stem with a short headline.",
      tags=["devanagari", "dha", "hindi", "sanskrit", "letter", "consonant", "indic", "alphabet"])
def _(S):
    return [head(12, 21), stem(),
            pa("M16.5 12.5H12.5C8 12.5 6 14.5 6 16.5C6 19 8.5 20 11 20C13.5 20 15 18.5 15 16.5C15 14.5 13 12.5 12.5 12.5")]


@icon("devanagari-na", CAT, "Devanagari letter na, a short curved stroke joined by a low bar to a stem under a headline.",
      tags=["devanagari", "na", "hindi", "sanskrit", "letter", "consonant", "indic", "alphabet"])
def _(S):
    return [head(), stem(), pa("M7.5 5.5V11C7.5 14.5 9 16 12 16H16.5")]


@icon("devanagari-pa", CAT, "Devanagari letter pa, a cup with a short left arm and a tall stem topped by a short headline.",
      tags=["devanagari", "pa", "hindi", "sanskrit", "letter", "consonant", "indic", "alphabet"])
def _(S):
    return [head(12, 21), stem(), pa("M7 10.5V15C7 18.5 9 20 12 20H16.5")]


@icon("devanagari-pha", CAT, "Devanagari letter pha, the pa cup and stem with a small curl hooking off the right side.",
      tags=["devanagari", "pha", "hindi", "sanskrit", "letter", "consonant", "indic", "alphabet"])
def _(S):
    return [head(12, 20), pa(seg(X, H, X, 20)), pa("M7 10.5V15C7 18.5 9 20 12 20H16.5"),
            pa("M16.5 10.5C20 9.5 21.5 11.5 20.5 13.5C19.8 15 18 15 16.5 14.5")]


@icon("devanagari-ba", CAT, "Devanagari letter ba, a closed round loop with a small diagonal inside, joined to a stem under a headline.",
      tags=["devanagari", "ba", "hindi", "sanskrit", "letter", "consonant", "indic", "alphabet"])
def _(S):
    return [head(), stem(), pa(circle(10, 14.5, 4.5)), pa("M14.5 14.5H16.5"), pa("M9 13L11.5 16")]


@icon("devanagari-bha", CAT, "Devanagari letter bha, an open cup with a small inner curl joined to a stem with a short headline.",
      tags=["devanagari", "bha", "hindi", "sanskrit", "letter", "consonant", "indic", "alphabet"])
def _(S):
    return [head(12, 21), stem(),
            pa("M10.5 10.5C8 10.5 6.5 12 6.5 15C6.5 18.5 9 20 12.5 20H16.5"),
            pa("M10.5 15.5C11.5 14 13.5 14.5 13.5 16")]


@icon("devanagari-ma", CAT, "Devanagari letter ma, a tall cup joined to a stem on the right under a full flat headline.",
      tags=["devanagari", "ma", "hindi", "sanskrit", "letter", "consonant", "indic", "alphabet"])
def _(S):
    return [head(), stem(), pa("M7 5.5V14C7 18 9.5 20 13 20H16.5")]


@icon("devanagari-ya", CAT, "Devanagari letter ya, a cup with a small inward hook at the top left joined to a stem.",
      tags=["devanagari", "ya", "hindi", "sanskrit", "letter", "consonant", "indic", "alphabet"])
def _(S):
    return [head(12, 21), stem(), pa("M11 10C7.5 9.5 6.5 12 6.5 15C6.5 18.5 9 20 12.5 20H16.5")]


@icon("devanagari-ra", CAT, "Devanagari letter ra, a small curled stroke like a hooked 2 hanging from a short headline.",
      tags=["devanagari", "ra", "hindi", "sanskrit", "letter", "consonant", "indic", "alphabet"])
def _(S):
    return [head(7, 17), pa("M12 5.5V9.5"), pa("M15.5 10C13 9 9.5 9.5 10 12C10.5 14.5 15 14.5 14 17.5C13.3 19.5 10 20.5 7.5 19")]


@icon("devanagari-la", CAT, "Devanagari letter la, a curled 3 like stroke on the left joined to a stem under a full headline.",
      tags=["devanagari", "la", "hindi", "sanskrit", "letter", "consonant", "indic", "alphabet"])
def _(S):
    return [head(), stem(), pa("M7.5 9.5C10.5 8.5 13 9.5 12.5 12C12 14 8.5 13.5 8.5 13.5C12.5 13 13.5 15.5 12.5 18C11.5 20 8 20 6.5 18.5"), pa(seg(12.5, 12, 16.5, 12))]


@icon("devanagari-va", CAT, "Devanagari letter va, a closed round loop on the left joined to a stem under a full headline.",
      tags=["devanagari", "va", "hindi", "sanskrit", "letter", "consonant", "indic", "alphabet"])
def _(S):
    return [head(), stem(), pa(circle(10.5, 14.5, 4.5)), pa(seg(15, 14.5, 16.5, 14.5))]


@icon("devanagari-sha", CAT, "Devanagari letter sha, a curled loop with a short slanted stroke, joined to a stem under a headline.",
      tags=["devanagari", "sha", "hindi", "sanskrit", "letter", "consonant", "indic", "alphabet"])
def _(S):
    return [head(), stem(), pa("M9 5.5V8"), pa("M12.5 10C9 9.5 6.5 11.5 7 14.5C7.5 17.5 11 18 13.5 17"), pa(seg(10, 12.5, 14, 18.5))]


@icon("devanagari-ssa", CAT, "Devanagari letter ssa, a cup crossed by a diagonal stroke and joined to a stem under a full headline.",
      tags=["devanagari", "ssa", "hindi", "sanskrit", "letter", "consonant", "indic", "alphabet"])
def _(S):
    return [head(), stem(), pa("M7 5.5V14C7 18 9.5 20 13 20H16.5"), pa(seg(7, 20, 13, 9))]


@icon("devanagari-sa", CAT, "Devanagari letter sa, a curled hook on the left joined by a short bar to a stem under a headline.",
      tags=["devanagari", "sa", "hindi", "sanskrit", "letter", "consonant", "indic", "alphabet"])
def _(S):
    return [head(), stem(), pa("M6.5 9.5C10 8.5 12.5 10 12 12.5C11.5 15 8 15.5 7 17.5C6.5 19 8.5 20 11 19.5"), pa(seg(11.5, 14.5, 16.5, 14.5))]


@icon("devanagari-ha", CAT, "Devanagari letter ha, a curled 3 like stroke with a tail flicking right at the bottom, hanging from a headline with no stem.",
      tags=["devanagari", "ha", "hindi", "sanskrit", "letter", "consonant", "indic", "alphabet"])
def _(S):
    return [head(5, 19), pa("M12 5.5V8.5"), pa("M15.5 9C12.5 8 9.5 9.5 10 11.5C10.5 13.5 14 13.5 14 15.5C14 18.5 10 19.5 7.5 18"), pa("M14 15.5C16 15.5 18.5 16.5 19 19")]


@icon("devanagari-ksha", CAT, "Devanagari letter ksha, a looped ka like shape with a crossing curl joined to a stem under a headline.",
      tags=["devanagari", "ksha", "hindi", "sanskrit", "letter", "consonant", "indic", "alphabet"])
def _(S):
    return [head(), stem(), pa(circle(9.5, 11.5, 3.5)), pa("M6 15C8 20 13 20 16.5 17"), pa(seg(13, 11.5, 16.5, 11.5))]


@icon("devanagari-tra", CAT, "Devanagari letter tra, the ta shape with a small slanted stroke joining its stem near the foot.",
      tags=["devanagari", "tra", "hindi", "sanskrit", "letter", "consonant", "indic", "alphabet"])
def _(S):
    return [head(), stem(), pa("M7.5 5.5V11C7.5 14.5 9 16 12 16H16.5"), pa(seg(9, 20, 13.5, 16))]


@icon("devanagari-gya", CAT, "Devanagari letter gya, a zigzag ja shape fused to a curled stroke and a stem under a headline.",
      tags=["devanagari", "gya", "hindi", "sanskrit", "letter", "consonant", "indic", "alphabet"])
def _(S):
    return [head(), stem(), pa("M5.5 9L10.5 12L6.5 15"), pa("M6.5 15C9 14 12.5 15 12 17.5C11.5 20 8 20 6.5 18"), pa(seg(10.5, 12, 16.5, 12))]
