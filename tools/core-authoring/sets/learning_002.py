"""TypeIcon Core: learning (batch learning_002): writing systems, language lessons, graduation, exams and
campus life.

Script icons are single letterforms drawn as 2 px stroke skeletons (never font text). Graduation icons share one
flat mortarboard; exam icons share one portrait sheet.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path.parser import parse_path
from geometry import SCALE, D, P, ST, U, fmt, path_to_d, rotation

CAT = "learning"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def tf(d, m):
    pen = SVGPathPen(None, ntos=fmt)
    parse_path(d, TransformPen(pen, m))
    return pen.getCommands()


def rot(d, deg, cx=12.0, cy=12.0):
    return tf(d, rotation(deg, cx, cy))


def mv(d, dx, dy):
    return tf(d, (1, 0, 0, 1, dx, dy))


def flip(d):
    return tf(d, (-1, 0, 0, 1, 24, 0))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def glyph(S, ch, x, y, w, h, sw=1.6):
    """Tiny letter drawn as a thin solid mark (x, y = top-left of its box). Solid outside shells, knocked out inside."""
    f = lambda v: fmt(v)
    sk = {
        "A": f"M0 {f(h)}L{f(w/2)} 0L{f(w)} {f(h)}M{f(w*.22)} {f(h*.66)}H{f(w*.78)}",
        "E": f"M{f(w)} 0H0V{f(h)}H{f(w)}M0 {f(h/2)}H{f(w*.8)}",
        "I": f"M{f(w/2)} 0V{f(h)}",
        "O": ellipse(w / 2, h / 2, w / 2, h / 2),
        "U": f"M0 0V{f(h - w/2)}A{f(w/2)} {f(w/2)} 0 0 0 {f(w)} {f(h - w/2)}V0",
        "B": f"M0 {f(h)}V0H{f(w*.55)}C{f(w*1.0)} 0 {f(w*1.0)} {f(h/2)} {f(w*.55)} {f(h/2)}H0M{f(w*.55)} {f(h/2)}"
             f"C{f(w*1.1)} {f(h/2)} {f(w*1.1)} {f(h)} {f(w*.55)} {f(h)}H0",
        "C": f"M{f(w*.95)} {f(h*.2)}C{f(w*.8)} {f(-h*.05)} 0 {f(-h*.02)} 0 {f(h/2)}C0 {f(h*1.02)} {f(w*.8)} {f(h*1.05)} {f(w*.95)} {f(h*.8)}",
        "D": f"M0 0H{f(w*.45)}C{f(w*1.1)} 0 {f(w*1.1)} {f(h)} {f(w*.45)} {f(h)}H0Z",
        "a": ellipse(w * .42, h * .68, w * .42, h * .32) + f"M{f(w*.84)} {f(h*.4)}V{f(h)}",
        "n": f"M0 {f(h)}V{f(h*.4)}M0 {f(h*.6)}C0 {f(h*.25)} {f(w)} {f(h*.25)} {f(w)} {f(h*.6)}V{f(h)}",
    }[ch]
    d = tf(sk, (1, 0, 0, 1, x, y))
    return Part("dot", path_to_d(ST(d, sw, S.cap, S.join, 3.0)))


# ============================================================================ writing systems

@icon("cyrillic-script", CAT, "Cyrillic capital zhe: a vertical stem with a K shape mirrored on each side",
      tags=["cyrillic", "russian", "alphabet", "zhe", "writing system", "slavic", "letter"])
def _(S):
    k = S.r
    return [line(seg(12, 3.5, 12, 20.5)),
            line(poly([(4, 4), (12, 12), (4, 20)], r=k)),
            line(poly([(20, 4), (12, 12), (20, 20)], r=k))]


@icon("greek-script", CAT, "Greek capital omega beside a lowercase alpha",
      tags=["greek", "alphabet", "omega", "alpha", "writing system", "letters", "hellenic"])
def _(S):
    omega = ("M2.5 19.5H6.5C4 17.5 2.5 15 2.5 11.5A4.5 4.5 0 0 1 11.5 11.5C11.5 15 10 17.5 7.5 19.5H11.5")
    alpha = ("M21 10C18 9.5 14.5 11 14.5 14.5C14.5 17.5 16 19 17.8 19C19.5 19 20.3 17 20.3 14.5V10"
             "M20.3 14.5C20.3 17.5 20.8 18.8 22 19")
    return [line(omega), line(alpha)]


@icon("arabic-script", CAT, "Arabic letter ain: a small hook on top and a wide curve sweeping below the line",
      tags=["arabic", "alphabet", "ain", "writing system", "letters", "calligraphy", "persian"])
def _(S):
    return [line("M17 4.5C12 4 9 6.5 10 8.5C10.8 10 13.5 10.5 15 10"),
            line("M13.5 10C9 11 4.5 13.5 5.5 17C6.5 20.5 13 20.5 17 17.5C19 16 20 14 20.5 11.5")]


@icon("hebrew-script", CAT, "Hebrew letter aleph: a slanted stroke with an arm rising on each side",
      tags=["hebrew", "alphabet", "aleph", "writing system", "letters", "jewish", "israel"])
def _(S):
    k = S.r
    return [line(seg(18.5, 4, 5.5, 20)),
            line(poly([(5, 4), (5, 9.5), (10.5, 13)], r=k)),
            line(poly([(19, 20), (19, 14.5), (13.5, 11)], r=k))]


@icon("devanagari-script", CAT, "Devanagari letter a hanging from a flat headline bar",
      tags=["devanagari", "hindi", "sanskrit", "alphabet", "writing system", "letters", "indic", "a"])
def _(S):
    return [line(seg(3, 5.5, 21, 5.5)),
            line(seg(16.5, 5.5, 16.5, 20)),
            line("M16.5 12H10C6 12 6 7.5 9.5 7.5"),
            line("M10 12C5 12.5 5 20 10 20C13 20 15 18 16.5 16"),
            line(seg(16.5, 12, 20.5, 16))]


@icon("bengali-script", CAT, "Bengali letter a hanging from a flat top bar with a looped body",
      tags=["bengali", "bangla", "alphabet", "writing system", "letters", "indic", "bangladesh"])
def _(S):
    return [line(seg(3, 5.5, 21, 5.5)),
            line(seg(15.5, 5.5, 15.5, 20)),
            line("M15.5 11H11"),
            line(ellipse(8.5, 13.5, 3.5, 4.5)),
            line(seg(15.5, 20, 20, 17))]


@icon("tamil-script", CAT, "Tamil letter a with two rounded loops and a tall stroke on the right",
      tags=["tamil", "alphabet", "writing system", "letters", "dravidian", "india", "sri lanka"])
def _(S):
    return [line(circle(7.5, 8, 3)),
            line("M7.5 11C3.5 12 3.5 19.5 9 19.5C12.5 19.5 14 16 14 12.5"),
            line("M18.5 4V19.5"),
            line("M18.5 4C16.5 3.5 15.5 4.5 15.5 6")]


@icon("thai-script", CAT, "Thai letter ko kai: a small head loop and a rounded arch",
      tags=["thai", "ko kai", "alphabet", "writing system", "letters", "thailand", "consonant"])
def _(S):
    return [line("M6.5 20V10C6.5 4 17.5 4 17.5 10V20"),
            line("M6.5 10.5C6.5 7.8 10.5 7.8 10.5 10.5C10.5 13.2 6.5 13.2 6.5 10.5")]


@icon("hangul-script", CAT, "Korean hangul syllable han built from a circle with a cap, a vertical bar and an L-shaped stroke",
      tags=["hangul", "korean", "alphabet", "han", "writing system", "letters", "korea", "syllable"])
def _(S):
    k = S.r
    return [line(seg(5, 3.5, 10, 3.5)),
            line(circle(7.5, 9, 2.75)),
            line(seg(16, 3, 16, 12.5)), line(seg(16, 7.5, 20, 7.5)),
            line(poly([(6, 16), (6, 20.5), (18, 20.5)], r=k))]


@icon("chinese-character", CAT, "Chinese character wen meaning writing: a dot, a bar and two crossing strokes",
      tags=["chinese", "hanzi", "kanji", "wen", "character", "writing system", "mandarin", "cjk"])
def _(S):
    return [line(seg(12, 3, 12, 6)),
            line(seg(4.5, 8.5, 19.5, 8.5)),
            line(seg(14.5, 8.5, 5.5, 20.5)),
            line(seg(8.5, 10.5, 19.5, 20.5))]


@icon("hiragana", CAT, "Japanese hiragana letter a with a bar, a stem and a round looping stroke",
      tags=["hiragana", "japanese", "kana", "a", "alphabet", "writing system", "letters", "japan"])
def _(S):
    return [line(seg(5.5, 8, 17.5, 8)),
            line("M11.5 3.5C11.3 9 10.5 13 8.5 15"),
            line("M9 12C4.5 14 4.5 20 10 20C15.5 20 19.5 16.5 17.5 13C16 10.5 12 11 9.5 15.5")]


@icon("katakana", CAT, "Japanese katakana letter a made of angular hooked strokes",
      tags=["katakana", "japanese", "kana", "a", "alphabet", "writing system", "letters", "japan"])
def _(S):
    k = S.r
    return [line(poly([(4.5, 6), (19, 6), (19, 9.5), (10, 20)], r=k)),
            line(seg(9.5, 6, 5.5, 14.5))]


@icon("georgian-script", CAT, "Georgian letter an: a rounded curling form",
      tags=["georgian", "mkhedruli", "alphabet", "an", "writing system", "letters", "georgia"])
def _(S):
    return [line("M19 6C13 4 6.5 6.5 6.5 12.5C6.5 18.5 14 20 17.5 15.5C19 13.5 17.5 10 14 10.5"),
            line(seg(14, 10.5, 12.5, 14))]


@icon("armenian-script", CAT, "Armenian capital letter ayb: two stems joined by a curve at the bottom",
      tags=["armenian", "ayb", "alphabet", "writing system", "letters", "armenia", "capital"])
def _(S):
    return [line(seg(6, 3.5, 6, 14)),
            line("M6 12C6 20 18 20 18 12"),
            line(seg(18, 3.5, 18, 20.5))]


@icon("ethiopic-script", CAT, "Ethiopic syllable a: a short top bar over a stem with three legs",
      tags=["ethiopic", "ge'ez", "amharic", "fidel", "alphabet", "writing system", "ethiopia", "letters"])
def _(S):
    return [line(seg(8.5, 4.5, 15.5, 4.5)),
            line(seg(12, 4.5, 12, 11.5)),
            line(seg(12, 11.5, 5.5, 20.5)),
            line(seg(12, 11.5, 12, 20.5)),
            line(seg(12, 11.5, 18.5, 20.5))]


@icon("gujarati-script", CAT, "Gujarati letter a: a round body with no top bar and a curl on the right",
      tags=["gujarati", "alphabet", "writing system", "letters", "indic", "india", "gujarat"])
def _(S):
    return [line(circle(9, 13.5, 4.5)),
            line(seg(13.5, 13.5, 16.5, 13.5)),
            line("M16.5 4.5V13.5C16.5 17.5 18 19.5 20.5 19.5")]


@icon("gurmukhi-script", CAT, "Gurmukhi letter ura hanging from a flat headline with an open curved body",
      tags=["gurmukhi", "punjabi", "alphabet", "ura", "writing system", "letters", "sikh", "indic"])
def _(S):
    return [line(seg(3, 5.5, 21, 5.5)),
            line(seg(12, 5.5, 12, 10)),
            line("M12 10C6 10 4.5 15 7 18C9.5 21 15.5 20.5 18 16.5"),
            line(seg(12, 14.5, 17, 14.5))]


@icon("telugu-script", CAT, "Telugu letter a: a rounded spiral body under a small tick mark",
      tags=["telugu", "alphabet", "writing system", "letters", "dravidian", "india", "andhra"])
def _(S):
    return [line("M15.5 11C12.5 8.5 6 10 6 15C6 20 12.5 21 16 17.5C18 15.5 17.5 12.5 14.5 12.5"),
            line(poly([(9.5, 6), (12, 3.5), (14.5, 6)], r=S.r * 0.6))]


@icon("kannada-script", CAT, "Kannada letter a: a small hooked loop above a larger round loop",
      tags=["kannada", "alphabet", "writing system", "letters", "dravidian", "india", "karnataka"])
def _(S):
    return [line("M6.5 7C6.5 3.5 12 3.5 12 7C12 10 6.5 10 6.5 7"),
            line("M12 7H17"),
            line(circle(12, 16, 4.5))]


@icon("malayalam-script", CAT, "Malayalam letter a made of joined round loops in a row",
      tags=["malayalam", "alphabet", "writing system", "letters", "dravidian", "india", "kerala"])
def _(S):
    return [line(circle(6, 14.5, 3.25)),
            line("M8.3 12.2C10 5.5 15 5.5 16.5 11"),
            line(circle(17.5, 15.5, 3.25)),
            line(seg(20.75, 15.5, 20.75, 8.5))]


@icon("sinhala-script", CAT, "Sinhala letter a: a round curling body with an upward tail",
      tags=["sinhala", "sinhalese", "alphabet", "writing system", "letters", "sri lanka", "indic"])
def _(S):
    return [line(circle(10, 14.5, 5)),
            line("M15 14.5C18 13 19.5 9 18 5.5C17 3.5 14.5 4.5 15 6.5")]


@icon("khmer-script", CAT, "Khmer letter ka with two small rounded arches and a hooked foot",
      tags=["khmer", "cambodian", "alphabet", "ka", "writing system", "letters", "cambodia"])
def _(S):
    return [line("M4.5 18V11C4.5 5 10.5 5 10.5 11C10.5 5 16.5 5 16.5 11V17.5C16.5 20.5 20.5 20.5 20.5 17.5")]


@icon("burmese-script", CAT, "Burmese letter ka: a circle open at the bottom with a small curl inside",
      tags=["burmese", "myanmar", "alphabet", "ka", "writing system", "letters", "kha", "letter"])
def _(S):
    return [line(arc(12, 11, 7.5, 125, 415)),
            line("M8.5 11C8.5 8.5 12.5 8.5 12.5 11C12.5 13.2 9.5 13 9.5 11.5")]


@icon("tibetan-script", CAT, "Tibetan letter ka hanging from a top bar with angled legs",
      tags=["tibetan", "alphabet", "ka", "writing system", "letters", "tibet", "buddhist"])
def _(S):
    return [line(seg(3, 5, 21, 5)),
            line("M8.5 5C5 8 6 12.5 10 12C13 11.5 14.5 8.5 14.5 5"),
            line(seg(10, 12, 5.5, 20.5)),
            line(seg(10, 12, 17, 20.5))]


@icon("runic-script", CAT, "Single rune fehu: a stem with two short strokes angled up to the right",
      tags=["rune", "fehu", "futhark", "norse", "viking", "germanic", "old norse", "writing system"])
def _(S):
    return [line(seg(7.5, 3.5, 7.5, 20.5)),
            line(seg(7.5, 9.5, 16.5, 4.5)),
            line(seg(7.5, 15.5, 16.5, 10.5))]


@icon("morse-alphabet", CAT, "Chart page with rows of dots and dashes for the letters A, B and C",
      tags=["morse code", "dots and dashes", "telegraph", "code chart", "signal", "cipher", "alphabet"])
def _(S):
    return [shell(rect(2, 3, 20, 18, rr(S, 2.5))),
            dot(6, 7.5), detail(seg(9, 7.5, 12.5, 7.5)),
            detail(seg(5, 12, 8.5, 12)), dot(11, 12), dot(14.5, 12), dot(18, 12),
            detail(seg(5, 16.5, 8.5, 16.5)), dot(11, 16.5), detail(seg(13.5, 16.5, 17, 16.5)), dot(19.25, 16.5)]


# ============================================================================ language and literacy lessons

def sheet(S, x=4, y=2.5, w=16, h=19):
    return shell(rect(x, y, w, h, rr(S, 2.5)))


@icon("essay", CAT, "Page with a centred title line and indented paragraph lines below",
      tags=["composition", "paper", "writing assignment", "english", "report", "article", "homework"])
def _(S):
    return [sheet(S),
            detail(seg(8.5, 7, 15.5, 7)),
            detail(seg(9, 11.5, 17, 11.5)), detail(seg(7, 15.5, 17, 15.5)),
            detail(seg(7, 19, 12, 19))]


@icon("anagram", CAT, "Two letter tiles with a curved arrow swapping their places",
      tags=["word puzzle", "rearrange letters", "scramble", "word game", "swap", "unscramble", "spelling"])
def _(S):
    k = S.r * 0.6
    return [shell(rect(2.5, 13, 8, 8, rr(S, 1.5))), shell(rect(13.5, 13, 8, 8, rr(S, 1.5))),
            glyph(S, "A", 4.6, 15.1, 3.8, 3.8, 1.4), glyph(S, "B", 15.7, 15.1, 3.6, 3.8, 1.4),
            line(arc(12, 10, 6.5, 180, 360)),
            line(poly([(3.3, 7.5), (5.5, 10.3), (8, 8.5)], r=k)),
            line(poly([(16, 8.5), (18.5, 10.3), (20.7, 7.5)], r=k))]


@icon("etymology", CAT, "Word block on top with roots branching down beneath it",
      tags=["word origin", "roots", "linguistics", "language history", "dictionary", "derivation", "vocabulary"])
def _(S):
    return [shell(rect(4, 3, 16, 6.5, rr(S, 2))),
            detail(seg(8.5, 6.25, 15.5, 6.25)),
            line(seg(12, 9.5, 12, 21.5)),
            line(seg(12, 13.5, 6.5, 17.5)), line(seg(12, 13.5, 17.5, 17.5)),
            line(seg(12, 18, 8.5, 21.5)), line(seg(12, 18, 15.5, 21.5))]


@icon("plot-diagram", CAT, "Mountain-shaped story arc with dots at the beginning, the peak and the end",
      tags=["story arc", "narrative", "climax", "literature", "story structure", "exposition", "rising action", "fiction"])
def _(S):
    arcline = (poly([(3.5, 18), (14, 5.5), (20.5, 18)]) if S.name == "line"
               else "M3.5 18C8 18 10 5.5 14 5.5C17.5 5.5 19 16 20.5 18")
    return [line(arcline), dot(3.5, 18, 2.2), dot(14, 5.5, 2.2), dot(20.5, 18, 2.2)]


@icon("word-of-the-day", CAT, "Calendar page with the letters Aa in the centre",
      tags=["daily word", "vocabulary", "dictionary", "calendar", "new word", "language learning", "flashcard"])
def _(S):
    return [shell(rect(3, 4, 18, 17, rr(S, 2.5))),
            line(seg(8, 2, 8, 6)), line(seg(16, 2, 16, 6)),
            detail(seg(3, 9, 21, 9)),
            glyph(S, "A", 5.5, 12, 5.5, 6.5), glyph(S, "a", 13, 13.3, 5, 5.2)]


@icon("phonics", CAT, "Letter A and an apple with small sound waves between them",
      tags=["letter sounds", "reading", "early literacy", "a is for apple", "kindergarten", "pronounce", "sound out"])
def _(S):
    apple = ("M17.5 10.5C15.8 9 13 10.5 13 14C13 18 14.8 21 17.5 20.5C20.2 21 22 18 22 14C22 10.5 19.2 9 17.5 10.5Z")
    return [line(poly([(2.5, 20), (5.75, 8.5), (9, 20)], r=S.r * 0.4), stroke_miterlimit="2"), line(seg(4, 16, 7.5, 16)),
            line(arc(8.5, 5.5, 2.4, -40, 40)), line(arc(8.5, 5.5, 4.6, -40, 40)),
            shell(apple),
            line(seg(17.5, 10.5, 18.2, 7))]


@icon("braille-slate", CAT, "Hinged slate frame with rows of cell windows and a pointed stylus below it",
      tags=["braille", "blind", "visually impaired", "writing frame", "stylus", "tactile", "accessibility"])
def _(S):
    cells = []
    for yy in (6, 11.25):
        for xx in (5, 10.5, 16):
            cells.append(mark(rect(xx, yy, 3.5, 3.25, L(S, 0, 0.8))))
    return [shell(rect(2.5, 3.5, 19, 13, rr(S, 2.5))),
            *cells,
            shell(rect(3, 18.5, 5, 3.5, rr(S, 1.5))),
            line(seg(8, 20.25, 20.5, 20.25))]


@icon("braille-writer", CAT, "Braille typewriter with six keys, a space bar and a sheet of paper rolled in at the top",
      tags=["braille machine", "blind", "tactile writing", "visually impaired", "typewriter", "accessibility"])
def _(S):
    return [shell(rect(6, 2, 12, 8, rr(S, 1.5))),
            dot(10.5, 4.75, 1), dot(13.5, 4.75, 1), dot(13.5, 7.5, 1),
            shell(rect(2.5, 9.5, 19, 12, rr(S, 3))),
            dot(5.5, 13.5, 1.2), dot(8.5, 13.5, 1.2), dot(11, 13.5, 1.2),
            dot(13, 13.5, 1.2), dot(15.5, 13.5, 1.2), dot(18.5, 13.5, 1.2),
            detail(seg(8, 18, 16, 18))]


def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])


def beads(curves, step):
    """Points spaced roughly `step` apart along a chain of cubic curves."""
    pts = []
    for c in curves:
        pts += [cubic(*c, i / 60) for i in range(61)]
    out, acc, last = [pts[0]], 0.0, pts[0]
    for q in pts[1:]:
        acc += math.hypot(q[0] - last[0], q[1] - last[1])
        last = q
        if acc >= step:
            out.append(q)
            acc = 0.0
    return out


@icon("syllable-blocks", CAT, "Word bar split into three joined blocks with one dot under each block",
      tags=["syllables", "word breaks", "phonics", "reading", "word parts", "spelling", "split word", "clap"])
def _(S):
    return [shell(rect(2.5, 4, 19, 9, rr(S, 2.5))),
            detail(seg(9, 4, 9, 13)), detail(seg(15.5, 4, 15.5, 13)),
            dot(5.75, 18.5, 1.6), dot(12.25, 18.5, 1.6), dot(18.5, 18.5, 1.6)]


@icon("vowels", CAT, "Letters A E I O U in two rows with a small bar under them",
      tags=["vowel letters", "aeiou", "phonics", "alphabet", "grammar", "spelling", "english", "language"])
def _(S):
    w, h = 4.8, 6
    return [glyph(S, "A", 2.5, 3, w, h), glyph(S, "E", 9.6, 3, w, h), glyph(S, "I", 16.7, 3, w, h),
            glyph(S, "O", 5.9, 12, w, h), glyph(S, "U", 13.4, 12, w, h),
            line(seg(3.5, 21, 20.5, 21))]


@icon("word-family", CAT, "House with a word ending on its roof and three word lines inside",
      tags=["word families", "rhyming words", "spelling patterns", "phonics", "reading", "at family", "ending"])
def _(S):
    return [shell(poly([(2.5, 10.5), (12, 2.5), (21.5, 10.5), (21.5, 21.5), (2.5, 21.5)], closed=True, r=S.r)),
            detail(seg(10, 9.5, 14, 9.5)),
            detail(seg(6.5, 13.75, 17.5, 13.75)), detail(seg(6.5, 17.75, 17.5, 17.75))]


@icon("book-report", CAT, "Sheet with a small book drawing at the top and paragraph lines below",
      tags=["report", "reading assignment", "review", "summary", "literature", "homework", "school"])
def _(S):
    bookp = "M12 7.4L7.2 6V11.3L12 12.7L16.8 11.3V6Z"
    book = minus(bookp, rect(11.3, 5, 1.4, 9))
    return [sheet(S), mark(book),
            detail(seg(7, 15.5, 17, 15.5)), detail(seg(7, 18.25, 13, 18.25))]


@icon("punctuation-marks", CAT, "Question mark, exclamation mark, comma and full stop in a two by two grid",
      tags=["period", "comma", "exclamation", "question mark", "grammar", "writing", "full stop", "sentence"])
def _(S):
    return [line("M3.5 6C3.5 2.5 9 2.5 9 6C9 8.5 6.25 8.5 6.25 11"), dot(6.25, 14, 1.4),
            line(seg(17.5, 3, 17.5, 10.5)), dot(17.5, 14, 1.4),
            dot(6, 19, 1.5),
            dot(17.5, 18.5, 1.6), line("M17.5 19.5C17.5 21 16.7 21.6 15.8 22")]


@icon("sand-tray", CAT, "Shallow tray of sand with a fingertip tracing a curved line in it",
      tags=["sand writing", "tactile learning", "montessori", "handwriting practice", "sensory", "letter tracing", "early years"])
def _(S):
    finger = rot(rect(14, 2.5, 4.5, 10, 2.25), 18, 16.25, 7.5)
    return [shell(rect(2.5, 13, 19, 8, rr(S, 2))),
            detail("M6 17.5C8 14.8 10 19.5 12 17C14 14.8 16 18 18 16"),
            shell(finger)]


@icon("sandpaper-letter", CAT, "Small board with one gritty letter S shown as a line of dots",
      tags=["montessori", "tactile letters", "texture", "phonics", "handwriting", "early literacy", "letter cards"])
def _(S):
    curves = [((15.5, 7.5), (15, 4.5), (8.5, 4.5), (8.5, 8.5)),
              ((8.5, 8.5), (8.5, 12.5), (15.5, 11.5), (15.5, 15.5)),
              ((15.5, 15.5), (15.5, 19.5), (8.5, 19.5), (8.5, 16.5))]
    return [shell(rect(3, 2.5, 18, 19, rr(S, 2.5))), *[dot(x, y, 1.05) for x, y in beads(curves, 2.9)]]


# ============================================================================ graduation and campus life

def cap_h(w):
    return w * 0.48


def cap_shell(S, cx, cy, w):
    """Flat mortarboard top (a rhombus) centred on (cx, cy)."""
    h = cap_h(w)
    return shell(poly([(cx - w / 2, cy), (cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2)], closed=True, r=S.r * 0.5),
                 stroke_miterlimit="2")


def cap_base(cx, cy, w, depth=None):
    """Skull-cap under the board: open stroke that starts inside the rhombus."""
    h = cap_h(w)
    x0, x1 = cx - 0.29 * w, cx + 0.29 * w
    ya = cy + 0.2 * h
    yb = ya + (depth if depth is not None else 0.4 * w)
    return line(f"M{fmt(x0)} {fmt(ya)}V{fmt(yb - 1.5)}C{fmt(x0)} {fmt(yb)} {fmt(cx - 0.12 * w)} {fmt(yb + 0.5)} {fmt(cx)} {fmt(yb + 0.5)}"
                f"C{fmt(cx + 0.12 * w)} {fmt(yb + 0.5)} {fmt(x1)} {fmt(yb)} {fmt(x1)} {fmt(yb - 1.5)}V{fmt(ya)}")


def cap_mark(cx, cy, w):
    """Small solid mortarboard silhouette with a hanging tassel (d-string for mark())."""
    h = cap_h(w)
    top = poly([(cx - w / 2, cy), (cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2)], closed=True)
    x0, x1 = cx - 0.27 * w, cx + 0.27 * w
    ya, yb = cy + 0.2 * h, cy + h / 2 + 0.26 * w
    base = f"M{fmt(x0)} {fmt(ya)}H{fmt(x1)}V{fmt(yb - 0.6)}Q{fmt(cx)} {fmt(yb + 0.9)} {fmt(x0)} {fmt(yb - 0.6)}Z"
    tassel = rect(cx + w / 2 - 0.6, cy, 1.2, 0.4 * w)
    return union(top, base, tassel)


@icon("class-ring", CAT, "Chunky ring with a large oval stone carrying a small mortarboard",
      tags=["graduation ring", "school ring", "senior ring", "keepsake", "jewelry", "high school", "college"])
def _(S):
    stone = (poly([(8.5, 2.5), (15.5, 2.5), (19.5, 7.5), (15.5, 12.5), (8.5, 12.5), (4.5, 7.5)], closed=True)
             if S.name == "line" else ellipse(12, 7.5, 7.5, 5.5))
    return [shell(stone),
            mark(cap_mark(12, 7.4, 8)),
            line(arc(12, 15.75, 6.25, 316, 584))]


@icon("yearbook", CAT, "Thick hardcover book with a mortarboard and year lines on the cover",
      tags=["annual", "school memories", "senior year", "graduating class", "keepsake", "photo book", "alumni"])
def _(S):
    return [shell(rect(4, 2.5, 16, 19, rr(S, 2))),
            detail(seg(7.5, 2.5, 7.5, 21.5)),
            mark(cap_mark(14, 7.6, 7)),
            detail(seg(11, 14.5, 17, 14.5)), detail(seg(11, 18, 15, 18))]


@icon("honor-cord", CAT, "Braided cord tied in a loop with a tassel at the end of each tail",
      tags=["graduation cord", "honour cord", "regalia", "academic honors", "commencement", "award", "society"])
def _(S):
    def tassel(x):
        return mark(poly([(x - 1.2, 18), (x + 1.2, 18), (x + 2.2, 22.5), (x + 0.8, 22.5), (x + 0.8, 20.8), (x - 0.8, 20.8),
                          (x - 0.8, 22.5), (x - 2.2, 22.5)], closed=True))
    if S.name == "line":
        d = "M7.5 17L12 11.5L16.5 6.5L12 3L7.5 6.5L12 11.5L16.5 17"
    else:
        d = "M7.5 17L12 11.5C15.5 7.5 15.5 3 12 3C8.5 3 8.5 7.5 12 11.5L16.5 17"
    return [line(d), tassel(7.5), tassel(16.5)]


@icon("academic-hood", CAT, "Academic hood with a scooped neck edge and a velvet trim band, as worn hanging down the back",
      tags=["graduate hood", "regalia", "gown", "degree colors", "doctoral hood", "commencement", "masters"])
def _(S):
    return [shell("M2.5 7C4.5 4.5 7.5 3.5 9 4C9.5 7 14.5 7 15 4C16.5 3.5 19.5 4.5 21.5 7L17.5 20.5C15.5 21.5 8.5 21.5 6.5 20.5Z",
                  stroke_miterlimit="2"),
            detail(poly([(6, 13), (12, 17.5), (18, 13)], r=S.r * 0.5))]


@icon("alumni", CAT, "Three graduates in mortarboards standing shoulder to shoulder",
      tags=["graduates", "former students", "old boys", "old girls", "class of", "reunion", "alumnus", "school community"])
def _(S):
    def person(cx):
        return [mark(cap_mark(cx, 5.5, 6.5)), shell(circle(cx, 11.5, 2.1)),
                line(f"M{fmt(cx - 2.3)} 21.5C{fmt(cx - 2.3)} 18 {fmt(cx - 1.2)} 15.8 {fmt(cx)} 15.8C{fmt(cx + 1.2)} 15.8 {fmt(cx + 2.3)} 18 {fmt(cx + 2.3)} 21.5")]
    return person(4.5) + person(12) + person(19.5)


@icon("honor-roll", CAT, "Unrolled scroll with a star at the top and lines of names",
      tags=["dean's list", "honour roll", "high achievers", "merit list", "student awards", "recognition", "scroll"])
def _(S):
    star = poly([pt_on(12, 7.6, 2.8 if i % 2 == 0 else 1.2, -90 + i * 36) for i in range(10)], closed=True)
    return [shell(rect(5.5, 3, 13, 15.5, rr(S, 1.5))),
            mark(star),
            detail(seg(9, 11.5, 15, 11.5)), detail(seg(9, 15, 15, 15)),
            shell(rect(3, 18.5, 18, 3.5, rr(S, 1.75)))]


@icon("doctoral-tam", CAT, "Soft round velvet cap with a puffed crown and a tassel hanging from the side",
      tags=["tam hat", "doctoral cap", "phd", "graduate cap", "regalia", "academic dress", "bonnet"])
def _(S):
    if S.name == "line":
        crown = poly([(2, 14), (2.5, 10), (7.5, 6), (16.5, 6), (21.5, 10), (22, 14)], closed=True)
    else:
        crown = "M2 14C1.5 8.5 6.5 6 12 6C17.5 6 22.5 8.5 22 14Z"
    return [shell(crown),
            line("M5 14V18C8.5 19.5 15.5 19.5 19 18V14"),
            dot(12, 4.5, 1.4),
            line("M12 4.5C16.5 2.5 22 5.5 22 10V12.5"), dot(22, 15, 1.5)]


@icon("diploma-cover", CAT, "Open folder with a crest on the left and a certificate on the right",
      tags=["certificate holder", "diploma folder", "degree", "graduation", "award folder", "credentials", "school crest"])
def _(S):
    crest = poly([(4.75, 7.75), (9.75, 7.75), (9.75, 12), (7.25, 15.25), (4.75, 12)], closed=True)
    return [shell(rect(2.5, 3.5, 19, 17, rr(S, 2.5))),
            detail(seg(12, 3.5, 12, 20.5)),
            mark(crest),
            detail(seg(15, 8, 19, 8)), detail(seg(15, 11.5, 19, 11.5)), dot(17, 16, 1.6)]


@icon("commencement-speech", CAT, "Lectern with a mortarboard resting on its top and a microphone on a short neck",
      tags=["graduation speech", "valedictorian", "podium", "address", "ceremony", "keynote", "public speaking"])
def _(S):
    return [cap_shell(S, 8.5, 4.5, 9),
            shell(poly([(3.5, 12), (20.5, 12), (18.5, 9), (5.5, 9)], closed=True, r=S.r * 0.4)),
            shell(poly([(6.5, 12), (17.5, 12), (16.5, 21.5), (7.5, 21.5)], closed=True, r=S.r * 0.4)),
            line(seg(17, 9, 17, 5.5)), dot(17, 3.75, 1.75)]


@icon("framed-diploma", CAT, "Certificate with a ribbon seal inside a picture frame hanging from a nail",
      tags=["wall certificate", "degree on the wall", "credentials", "graduation keepsake", "office decor", "achievement", "frame"])
def _(S):
    return [line(poly([(7, 8), (12, 2.5), (17, 8)], r=S.r * 0.3)),
            shell(rect(3, 7, 18, 14.5, rr(S, 2))),
            detail(seg(7.5, 11.5, 16.5, 11.5)), detail(seg(7.5, 14.5, 12.5, 14.5)),
            dot(16.25, 16, 1.5)]


@icon("academic-transcript", CAT, "Document with a table of course lines, a grade column and a round seal at the bottom",
      tags=["grade report", "records", "marks", "gpa", "student record", "courses", "report card", "official"])
def _(S):
    return [sheet(S),
            detail(seg(7, 7.5, 12, 7.5)), detail(seg(14.5, 7.5, 17, 7.5)),
            detail(seg(7, 11.5, 12, 11.5)), detail(seg(14.5, 11.5, 17, 11.5)),
            dot(12, 17, 2.2)]


@icon("video-lecture", CAT, "Screen showing a teacher figure beside a small board, with a play bar below",
      tags=["online lesson", "recorded class", "e-learning", "mooc", "webinar", "remote teaching", "tutorial video"])
def _(S):
    return [shell(rect(2.5, 3, 19, 12.5, rr(S, 2.5))),
            dot(7, 7.25, 1.6), detail("M4.75 13.25C4.75 10.5 9.25 10.5 9.25 13.25"),
            detail(seg(12.5, 7, 18.5, 7)), detail(seg(12.5, 10.5, 17, 10.5)),
            mark(poly([(3, 18), (3, 22), (6.5, 20)], closed=True)), line(seg(9, 20, 21, 20))]


@icon("micro-credential", CAT, "Hexagon badge with two ribbon tails and a mortarboard in the centre",
      tags=["digital badge", "short course", "certificate", "skills", "nanodegree", "upskilling", "achievement"])
def _(S):
    return [shell(poly(regular(12, 9.5, 8, 6), closed=True, r=S.r), stroke_miterlimit="2"),
            mark(cap_mark(12, 8.6, 8)),
            line(seg(8.5, 16, 7, 22)), line(seg(15.5, 16, 17, 22))]


@icon("homeschooling", CAT, "House outline with a mortarboard sitting on the roof",
      tags=["home education", "learning at home", "home school", "family learning", "parent teacher", "unschooling", "distance learning"])
def _(S):
    return [shell(poly([(3.5, 15.5), (12, 10.5), (20.5, 15.5), (20.5, 21.5), (3.5, 21.5)], closed=True, r=S.r)),
            mark(cap_mark(12, 5.5, 11)),
            detail(poly([(10, 21.5), (10, 18), (14, 18), (14, 21.5)], r=S.r * 0.5))]


# ============================================================================ tutoring, exams and campus

def ring(cx, cy, ro, ri):
    """Thin solid ring (for bubbles and radio buttons)."""
    return minus(circle(cx, cy, ro), circle(cx, cy, ri))


def seated(cx, head_y=8, base_y=18, half=2.4):
    """Head and shoulders of a person sitting at a table (base_y = table top)."""
    return [shell(circle(cx, head_y, 2.1)),
            line(f"M{fmt(cx - half)} {fmt(base_y)}V{fmt(head_y + 5.5)}C{fmt(cx - half)} {fmt(head_y + 3.8)} {fmt(cx - 1)} {fmt(head_y + 3.4)} {fmt(cx)} {fmt(head_y + 3.4)}"
                 f"C{fmt(cx + 1)} {fmt(head_y + 3.4)} {fmt(cx + half)} {fmt(head_y + 3.8)} {fmt(cx + half)} {fmt(head_y + 5.5)}V{fmt(base_y)}")]


@icon("tutoring", CAT, "Two people seated at a small table sharing one open book",
      tags=["one on one", "private lessons", "mentor", "homework help", "coaching", "teacher and student", "study session"])
def _(S):
    return [*seated(4.5, 6.5, 18.5, 2.2), *seated(19.5, 6.5, 18.5, 2.2),
            mark(minus("M12 13.5L7.6 12.2V15.6L12 17L16.4 15.6V12.2Z", rect(11.3, 11, 1.4, 8))),
            line(seg(2.5, 18.5, 21.5, 18.5)), line(seg(4.5, 18.5, 4.5, 21.5)), line(seg(19.5, 18.5, 19.5, 21.5))]


@icon("lesson-plan", CAT, "Clipboard with a numbered list whose first item is a small apple",
      tags=["teaching plan", "curriculum", "schedule", "teacher planner", "syllabus", "scheme of work", "class outline"])
def _(S):
    apple = "M8.2 9.3C7.6 8.6 5.9 9 5.9 10.8C5.9 12.4 6.9 13.2 8.2 12.9C9.5 13.2 10.5 12.4 10.5 10.8C10.5 9 8.8 8.6 8.2 9.3Z"
    return [shell(rect(4, 4.5, 16, 17, rr(S, 2))),
            shell(rect(9, 2.5, 6, 3.5, rr(S, 1))),
            mark(apple),
            detail(seg(12.5, 11.25, 17, 11.25)),
            dot(8.2, 15.25, 1), detail(seg(12.5, 15.25, 17, 15.25)),
            dot(8.2, 19, 1), detail(seg(12.5, 19, 15.5, 19))]


@icon("ai-tutor", CAT, "Robot head with an antenna wearing a mortarboard",
      tags=["robot teacher", "artificial intelligence", "chatbot", "virtual tutor", "edtech", "smart learning", "bot"])
def _(S):
    return [line(seg(12, 4.4, 12, 2.5)),
            cap_shell(S, 12, 7.5, 13),
            shell(rect(4.5, 11.5, 15, 10, rr(S, 3))),
            dot(9, 15.5, 1.5), dot(15, 15.5, 1.5), detail(seg(9.5, 19, 14.5, 19))]


@icon("online-exam", CAT, "Laptop showing answer checkboxes with a small timer beside it",
      tags=["remote exam", "e-assessment", "computer test", "digital test", "timed quiz", "screen test", "proctored"])
def _(S):
    return [shell(rect(2.5, 10, 12, 8.5, rr(S, 1.5))),
            mark(rect(5, 11.4, 2.3, 2.3, 0.4)), detail(seg(9.3, 12.55, 12, 12.55)),
            mark(rect(5, 14.7, 2.3, 2.3, 0.4)),
            line(seg(1.5, 21, 15.5, 21)),
            shell(circle(18.5, 8, 3.25)), line(seg(17.5, 3.4, 19.5, 3.4)), dot(18.5, 8, 0.9)]


@icon("answer-sheet", CAT, "Sheet with rows of small answer bubbles, a few filled in",
      tags=["bubble sheet", "optical mark", "test form", "multiple choice form", "exam paper", "fill the circle"])
def _(S):
    parts = [sheet(S)]
    rows = [(7.5, 1), (12, 0), (16.5, 2)]
    for y, pick in rows:
        for i, x in enumerate((8, 12, 16)):
            parts.append(mark(circle(x, y, 1.45) if i == pick else ring(x, y, 1.7, 0.85)))
    return parts


@icon("multiple-choice", CAT, "Four stacked options with round buttons, one of them filled in",
      tags=["quiz question", "options", "radio buttons", "a b c d", "test item", "survey", "pick one"])
def _(S):
    parts = []
    for i, y in enumerate((4.5, 9.75, 15, 20.25)):
        parts.append(mark(circle(5, y, 2) if i == 1 else ring(5, y, 2.2, 1.1)))
        parts.append(line(seg(10, y, 21 if i % 2 == 0 else 19, y)))
    return parts


@icon("fill-in-the-blank", CAT, "Lines of text with an empty box in the middle of a sentence",
      tags=["cloze", "missing word", "gap fill", "worksheet", "complete the sentence", "question type", "blank"])
def _(S):
    return [line(seg(3, 5.5, 21, 5.5)),
            line(seg(3, 12, 7, 12)), line(rect(9.5, 9, 5, 6, L(S, 0, 1.5))), line(seg(17, 12, 21, 12)),
            line(seg(3, 18.5, 14, 18.5))]


@icon("exam-hall", CAT, "Top view of evenly spaced single desks in rows with a clock on the front wall",
      tags=["examination room", "test room", "invigilator", "seating plan", "sports hall exam", "desks in rows", "assessment"])
def _(S):
    parts = [shell(circle(12, 5, 3)), dot(12, 5, 0.9)]
    for y in (12, 16, 20):
        for x in (5, 12, 19):
            parts.append(solid(rect(x - 2.5, y - 1.25, 5, 2.5, L(S, 0, 0.6))))
    return parts


@icon("answer-key", CAT, "Sheet with a key in the corner and a column of letter answers",
      tags=["marking scheme", "solutions", "teacher copy", "mark sheet", "correct answers", "grading guide", "exam key"])
def _(S):
    key = union(ring(7.5, 6.6, 2.4, 1.1), rect(9.7, 6, 7.3, 1.3), rect(14.4, 7.2, 1.3, 1.9), rect(16.6, 7.2, 1.3, 1.9))
    return [sheet(S), mark(key),
            glyph(S, "A", 7, 12, 3.4, 3.8, 1.3), detail(seg(13, 13.9, 17, 13.9)),
            glyph(S, "C", 7, 17, 3.4, 3.8, 1.3), detail(seg(13, 18.9, 15.5, 18.9))]


@icon("oral-exam", CAT, "Student and examiner sitting on either side of a desk with a speech bubble between them",
      tags=["viva", "spoken test", "interview", "speaking assessment", "language exam", "defense", "questioning"])
def _(S):
    bubble = poly([(8, 2.5), (16, 2.5), (16, 8.5), (13, 8.5), (11.5, 10.5), (10.5, 8.5), (8, 8.5)], closed=True, r=S.r * 0.5)
    return [*seated(4.5, 11.5, 19, 2.2), *seated(19.5, 11.5, 19, 2.2),
            shell(bubble),
            line(seg(2.5, 19, 21.5, 19))]


@icon("proctor", CAT, "Standing figure with a large eye above rows of desks",
      tags=["invigilator", "exam supervisor", "monitor", "watching", "test supervision", "surveillance", "exam watch"])
def _(S):
    parts = [line("M5.5 4.5Q12 -1 18.5 4.5Q12 10 5.5 4.5Z"), dot(12, 4.5, 1.5),
             shell(circle(12, 13, 2.1)),
             line("M8.5 21.5V18.5C8.5 16.5 10 16 12 16C14 16 15.5 16.5 15.5 18.5V21.5")]
    for x in (4.5, 19.5):
        for y in (14.5, 19.5):
            parts.append(solid(rect(x - 2, y - 1, 4, 2, 0.5)))
    return parts


@icon("exam-results", CAT, "Opened envelope with a sheet sliding out showing a letter grade",
      tags=["grades letter", "score report", "results day", "mark sheet", "result notification", "a grade", "report"])
def _(S):
    return [line(poly([(6.5, 11), (6.5, 3.5), (17.5, 3.5), (17.5, 11)], r=S.r * 0.5)),
            glyph(S, "A", 9.4, 5.5, 5.2, 4.2),
            shell(rect(2.5, 10.5, 19, 11, rr(S, 2.5))),
            detail(poly([(2.5, 11.5), (12, 17), (21.5, 11.5)], r=S.r * 0.4))]


@icon("graded-essay", CAT, "Page of text lines with a circled score at the top and a tick in the margin",
      tags=["marked paper", "teacher feedback", "corrections", "assessment", "homework grade", "red pen", "score"])
def _(S):
    return [sheet(S), mark(ring(16, 7.4, 2.9, 1.3)),
            detail(seg(7, 7.4, 11, 7.4)), detail(seg(7, 12, 17, 12)), detail(seg(7, 16, 14, 16)),
            detail(poly([(15, 18.2), (16.2, 19.4), (18.5, 16.6)], r=S.r * 0.3))]


@icon("lecture-hall", CAT, "Curved tiers of seats rising toward the back and facing a small lectern",
      tags=["auditorium", "amphitheatre", "university classroom", "tiered seating", "large class", "theatre seating", "campus"])
def _(S):
    parts = [shell(rect(10, 18.5, 4, 3, rr(S, 0.8)))]
    for r, a0, a1 in ((6, 208, 332), (10, 214, 326), (14, 222, 318)):
        n = int(math.radians(a1 - a0) * r / 3.4) + 1
        for i in range(n):
            x, y = pt_on(12, 22, r, a0 + (a1 - a0) * i / (n - 1))
            parts.append(dot(x, y, 1.15) if S.name == "rounded" else mark(rect(x - 1.1, y - 1.1, 2.2, 2.2)))
    return parts


@icon("scholarship", CAT, "Mortarboard floating above a cupped hand that holds a coin",
      tags=["student funding", "grant", "bursary", "tuition aid", "financial aid", "award money", "education fund"])
def _(S):
    return [cap_shell(S, 12, 5.5, 13), cap_base(12, 5.5, 13, 1.2),
            shell(circle(12, 14.75, 2.75)),
            line("M3 16.5C3 19.5 7.5 21.5 12 21.5C16.5 21.5 21 19.5 21 16.5")]


@icon("tuition-fee", CAT, "Mortarboard with a price tag hanging from its tassel",
      tags=["school fees", "course cost", "education cost", "student debt", "college price", "payment", "enrolment fee"])
def _(S):
    return [cap_shell(S, 10, 7, 16), cap_base(10, 7, 16, 3.5),
            line(seg(18, 7, 18, 12)),
            shell(poly([(18, 12), (20.75, 14.75), (20.75, 21.5), (15.25, 21.5), (15.25, 14.75)], closed=True, r=S.r * 0.4)),
            dot(18, 16.75, 0.9)]


@icon("enrollment-form", CAT, "Clipboard form with a mortarboard and text lines, and a pencil beside it",
      tags=["admission", "registration", "application form", "sign up", "student intake", "school application", "apply"])
def _(S):
    return [shell(rect(3, 4.5, 13, 17, rr(S, 2))),
            shell(rect(6, 2.5, 7, 3.5, rr(S, 1))),
            mark(cap_mark(9.5, 10.2, 7)),
            detail(seg(6, 15.5, 13, 15.5)), detail(seg(6, 18.75, 10.5, 18.75)),
            shell(poly([(18.2, 5), (21.2, 5), (21.2, 17), (19.7, 20.5), (18.2, 17)], closed=True, r=S.r * 0.3))]


@icon("academic-calendar", CAT, "Calendar page with a mortarboard in place of the date",
      tags=["school year", "term dates", "semester", "timetable", "school calendar", "enrolment deadline", "academic year"])
def _(S):
    return [shell(rect(3, 4, 18, 17, rr(S, 2.5))),
            line(seg(8, 2, 8, 6)), line(seg(16, 2, 16, 6)),
            detail(seg(3, 9, 21, 9)),
            mark(cap_mark(12, 13.2, 9))]


@icon("seminar", CAT, "Oval table seen from above with six chairs around it and papers on it",
      tags=["discussion group", "roundtable", "workshop", "meeting room", "tutorial", "study group", "boardroom"])
def _(S):
    table = rect(6.25, 8, 11.5, 8, 2.5) if S.name == "line" else ellipse(12, 12, 5.75, 4)
    parts = [shell(table), mark(rect(8.5, 10.6, 2.4, 2.8, 0.3)), mark(rect(13, 10.6, 2.4, 2.8, 0.3))]
    for x, y in ((9, 4.25), (15, 4.25), (9, 19.75), (15, 19.75), (2.9, 12), (21.1, 12)):
        parts.append(dot(x, y, 1.5) if S.name == "rounded" else mark(rect(x - 1.4, y - 1.4, 2.8, 2.8)))
    return parts


@icon("field-trip", CAT, "Small school bus with a pennant flag on its roof and a map pin above it",
      tags=["school outing", "excursion", "class trip", "bus trip", "educational visit", "museum visit", "school bus"])
def _(S):
    pin = "M6.5 9.5C4 7 3.5 5.8 3.5 4.6A3 3 0 0 1 9.5 4.6C9.5 5.8 9 7 6.5 9.5Z"
    return [shell(pin), dot(6.5, 4.6, 1),
            line(seg(17, 12.5, 17, 4)), mark(poly([(17, 3.5), (21.5, 5.25), (17, 7)], closed=True)),
            shell(rect(2.5, 12.5, 19, 7, rr(S, 2.5))),
            mark(rect(5, 14.25, 3.5, 2.5, 0.4)), mark(rect(10.25, 14.25, 3.5, 2.5, 0.4)),
            solid(circle(7, 20.6, 1.7)), solid(circle(17, 20.6, 1.7))]


@icon("parent-teacher-meeting", CAT, "Two adults facing a teacher across a desk with a report card on it",
      tags=["parents evening", "conference", "school meeting", "progress report", "guardians", "teacher talk", "report card"])
def _(S):
    return [*seated(4, 6.5, 18.5, 1.6), *seated(10, 6.5, 18.5, 1.6), *seated(19.3, 6.5, 18.5, 2.2),
            mark(rect(13.3, 16.2, 2.4, 1.8, 0.3)),
            line(seg(2, 18.5, 22, 18.5)), line(seg(4, 18.5, 4, 21.5)), line(seg(19.3, 18.5, 19.3, 21.5))]


@icon("study-abroad", CAT, "Mortarboard hovering above a globe with a small plane flying away at the lower right",
      tags=["exchange student", "overseas study", "international education", "foreign university", "global learning", "travel"])
def _(S):
    w, cx, cy = 9, 10.5, 4.5
    h = cap_h(w)
    flat = union(poly([(cx - w / 2, cy), (cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2)], closed=True, r=S.r * 0.6),
                 rect(cx + w / 2 - 0.6, cy, 1.2, 4))
    return [shell(circle(10.5, 15.5, 6.5)),
            detail(seg(4, 15.5, 17, 15.5)), detail(ellipse(10.5, 15.5, 3, 6.5)),
            mark(flat),
            mark(poly([(18.6, 13.5), (23, 12), (20.6, 17.4), (20, 15)], closed=True, r=S.r * 0.6))]


@icon("vocational-training", CAT, "Mortarboard above a crossed wrench and screwdriver",
      tags=["trade school", "apprenticeship", "technical education", "skills training", "tvet", "career course", "craft"])
def _(S):
    return [cap_shell(S, 12, 5, 14),
            line(seg(6, 11.5, 17.5, 21)), shell(circle(5.5, 11, 2)),
            line(seg(18, 11.5, 6.5, 21)),
            line(seg(16.4, 10.4, 19.6, 12.6))]


@icon("college-pennant", CAT, "Long triangular felt pennant on a short stick with a letter C on it",
      tags=["school spirit", "team flag", "college flag", "university pennant", "fan memorabilia", "mascot", "sports"])
def _(S):
    return [line(seg(3.5, 2.5, 3.5, 21.5)),
            shell(poly([(4.5, 5.5), (20.5, 12), (4.5, 18.5)], closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
            glyph(S, "C", 7.6, 9.9, 3.8, 4.2, 1.4)]
