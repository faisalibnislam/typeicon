"""TypeIcon Core: writing-system letters, batch 2 (Arabic, Hangul, Hiragana).

Each letter is a simple 2 px stroke skeleton drawn by hand (not font text). Arabic letters sit on a low baseline
with dots above or below, Hangul jamo are built from straight strokes in a y 4 to 20 box, Hiragana are single
hand drawn strokes. All parts are open strokes, so Filled keeps the counters and only gets a heavier stroke;
Rounded gets round caps/joins and 1.5 px fillets on straight corners.
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


def _bowl(y):
    return pa(f"M4 {y - 6}C4 {y - 1.5} 7 {y} 10 {y}H14C17 {y} 20 {y - 1.5} 20 {y - 6}")


# ============================================================================ Arabic

@icon("arabic-tah", CAT, "Arabic letter tah: a flat closed loop lying on the line with a tall straight stroke rising from its left end.",
      tags=["tah", "taa", "arabic", "letter", "alphabet", "t", "loop"])
def _(S):
    return [pa(ellipse(14, 15.5, 6, 3.5)), pa("M8 4V15.5")]


@icon("arabic-zah", CAT, "Arabic letter zah: the flat tah loop and tall upright stroke with one dot above the loop.",
      tags=["zah", "zaa", "dhah", "arabic", "letter", "alphabet", "z", "dot above"])
def _(S):
    return [pa(ellipse(14, 15.5, 6, 3.5)), pa("M8 4V15.5"), dot(15.5, 8.5, 1.6)]


@icon("arabic-ghayn", CAT, "Arabic letter ghayn: a small open c shaped head on a large curve that sweeps below the line, with one dot above.",
      tags=["ghayn", "ghain", "arabic", "letter", "alphabet", "gh", "dot above"])
def _(S):
    return [pa("M17 10C14 8 10.5 8 10.5 10.5C10.5 12.5 13 13 16.5 13"),
            pa("M16.5 13C18.5 17 15 20 11 20C7 20 4.5 18 4.5 15"), dot(14, 4.5, 1.6)]


@icon("arabic-fa", CAT, "Arabic letter fa: a small round loop on the right end of a long flat stroke that curls up at the left, with one dot above.",
      tags=["fa", "faa", "arabic", "letter", "alphabet", "f", "dot above", "loop"])
def _(S):
    return [pa(circle(16.5, 13.5, 3.5)), pa("M16.5 17H8C5.5 17 4.5 16 4.5 13"), dot(16.5, 5, 1.6)]


@icon("arabic-qaf", CAT, "Arabic letter qaf: a small round loop above a deep round bowl that sweeps below the line, with two dots above.",
      tags=["qaf", "qaaf", "arabic", "letter", "alphabet", "q", "two dots", "loop"])
def _(S):
    return [pa(circle(13.5, 11.5, 2.8)), pa("M19 14C19 19.5 15 20 12 20C8 20 5 19 5 14"),
            dot(11.5, 4.6, 1.3), dot(15.5, 4.6, 1.3)]


@icon("arabic-kaf", CAT, "Arabic letter kaf: a tall upright stroke on the left joined to a flat base that curls up at the right, with a small zigzag inside.",
      tags=["kaf", "kaaf", "arabic", "letter", "alphabet", "k"])
def _(S):
    return [pa("M6.5 4V18H17C19 18 19.5 17 19.5 15"), pa("M15 8L11 11L15 14")]


@icon("arabic-lam", CAT, "Arabic letter lam: a tall straight stroke that curves at its foot into a deep round bowl rising back up on the left.",
      tags=["lam", "laam", "arabic", "letter", "alphabet", "l", "bowl"])
def _(S):
    return [pa("M16 3V14C16 18.5 12.5 20 10 20C6.5 20 5 18 5 15")]


@icon("arabic-mim", CAT, "Arabic letter mim: a small closed round loop on the line with a straight tail dropping down beneath it.",
      tags=["mim", "meem", "arabic", "letter", "alphabet", "m", "loop"])
def _(S):
    return [pa(circle(12, 8.5, 3.5)), pa("M12 12V21")]


@icon("arabic-nun", CAT, "Arabic letter nun: a deep round open bowl like a cup with one dot above its centre.",
      tags=["nun", "noon", "arabic", "letter", "alphabet", "n", "dot above", "bowl"])
def _(S):
    return [pa("M5 11A7 9 0 0 0 19 11"), dot(12, 6, 1.6)]


@icon("arabic-heh", CAT, "Arabic letter heh: a rounded loop with a smaller loop folded inside it.",
      tags=["heh", "haa", "arabic", "letter", "alphabet", "h", "loop"])
def _(S):
    return [pa("M12 19C7.5 19 5 16 5 13C5 9 9 7 19 4C17 8 19 11 19 13C19 16.5 16 19 12 19Z"), pa(circle(12.5, 14, 2))]


@icon("arabic-waw", CAT, "Arabic letter waw: a small round head loop with a tail curving down and to the left below the line.",
      tags=["waw", "waaw", "arabic", "letter", "alphabet", "w", "o", "u", "loop"])
def _(S):
    return [pa(circle(15, 8.5, 3.5)), pa("M17.5 11C18 17 14 20 6 19.5")]


@icon("arabic-ya", CAT, "Arabic letter ya: a small curl at the top right dropping into a wide bowl that sweeps back right under the line, with two dots below.",
      tags=["ya", "yaa", "arabic", "letter", "alphabet", "y", "two dots below"])
def _(S):
    return [pa("M18.5 5V9C18.5 12 15.5 13 12.5 13H8C5 13 4 10.5 5.5 9"), pa("M8 17H20"),
            dot(10.5, 21, 1.2), dot(15.5, 21, 1.2)]


@icon("arabic-alif-maqsura", CAT, "Arabic letter alif maqsura: the ya shape of a top curl and wide sweeping bowl with no dots.",
      tags=["alif maqsura", "alef maksura", "arabic", "letter", "alphabet", "ya", "no dots"])
def _(S):
    return [pa("M18.5 5V10C18.5 14 15.5 15 12.5 15H8C5 15 4 12 5.5 10.5"), pa("M8 19.5H20")]


@icon("arabic-hamza", CAT, "Arabic hamza: a small standalone hooked mark like a backwards c whose lower end flicks out into a short tail.",
      tags=["hamza", "hamzah", "arabic", "glottal stop", "letter", "alphabet", "mark"])
def _(S):
    return [pa("M16 6C11 5 8.5 8 11.5 10.5C8.5 12 8 14.5 10.5 15.5H18")]


@icon("arabic-ta-marbuta", CAT, "Arabic ta marbuta: a small closed round loop like heh with two dots side by side above it.",
      tags=["ta marbuta", "teh marbuta", "arabic", "letter", "alphabet", "two dots", "loop"])
def _(S):
    return [pa("M12 20C8 20 6 18 6 15.5C6 12.5 9 11 17 9.5C16 12 18 13.5 18 15.5C18 18 16 20 12 20Z"), dot(9, 4.5, 1.5), dot(15, 4.5, 1.5)]


@icon("arabic-lam-alif", CAT, "Arabic lam alif ligature: two tall strokes that meet in a V and join in a small curve at the base.",
      tags=["lam alif", "laa", "ligature", "arabic", "letter", "alphabet", "no"])
def _(S):
    return [pa("M17 4L10.5 16"), pa("M7.5 4C7.5 11 10 15.5 13 16.5C15.5 17.3 16.5 15.5 15 14.5")]


@icon("arabic-peh", CAT, "Arabic script letter peh: the shallow canoe shaped bowl with three dots in a triangle below it.",
      tags=["peh", "pe", "persian", "urdu", "arabic", "letter", "alphabet", "p", "three dots below"])
def _(S):
    return [_bowl(10), dot(9, 16, 1.4), dot(15, 16, 1.4), dot(12, 20.5, 1.4)]


@icon("arabic-tcheh", CAT, "Arabic script letter tcheh: the folded top stroke and deep reversed C sweep of jim with three dots inside the curve.",
      tags=["tcheh", "cheh", "persian", "urdu", "arabic", "letter", "alphabet", "ch", "three dots"])
def _(S):
    return [pa("M18 4.5H11A7.25 7.25 0 0 0 11 19H19"), dot(14, 9, 1.3), dot(11.5, 13.5, 1.3), dot(16.5, 13.5, 1.3)]


@icon("arabic-jeh", CAT, "Arabic script letter jeh: the comma like ra stroke with three dots in a triangle above it.",
      tags=["jeh", "zheh", "persian", "arabic", "letter", "alphabet", "zh", "three dots"])
def _(S):
    return [pa("M16 11C16.5 15 14 18 8 19.5"), dot(13.5, 3.6, 1.3), dot(10.5, 7, 1.3), dot(16.5, 7, 1.3)]


@icon("arabic-gaf", CAT, "Arabic script letter gaf: a slanted stroke joined to a flat base that curls up at the right, with a second short slanted bar above it.",
      tags=["gaf", "persian", "urdu", "arabic", "letter", "alphabet", "g", "double bar"])
def _(S):
    return [pa("M11.5 8L7 18H17C19 18 19.5 17 19.5 15"), pa("M16.5 3L14.5 6.5")]


# ============================================================================ Hangul consonants and vowels

def sg(x1, y1, x2, y2):
    return line(seg(x1, y1, x2, y2))


def _tags(*extra):
    return ["hangul", "korean", "jamo", "letter", "alphabet", *extra]


@icon("hangul-giyeok", CAT, "Hangul consonant giyeok: a horizontal stroke across the top that turns sharply down at the right end.",
      tags=_tags("giyeok", "gieok", "g", "k", "consonant"))
def _(S):
    return [pl(S, (6, 5), (18, 5), (18, 19))]


@icon("hangul-digeut", CAT, "Hangul consonant digeut: a squared C of a top bar, a left upright and a longer bottom bar.",
      tags=_tags("digeut", "digeud", "d", "t", "consonant"))
def _(S):
    return [pl(S, (16, 5), (6, 5), (6, 19), (19, 19))]


@icon("hangul-rieul", CAT, "Hangul consonant rieul: three horizontal strokes joined by alternating uprights, like a squared S.",
      tags=_tags("rieul", "lieul", "r", "l", "consonant"))
def _(S):
    return [pl(S, (6, 5), (18, 5), (18, 12), (6, 12), (6, 19), (18, 19))]


@icon("hangul-bieup", CAT, "Hangul consonant bieup: two vertical stems joined by a middle crossbar and a bottom bar.",
      tags=_tags("bieup", "bieub", "b", "p", "consonant"))
def _(S):
    return [pl(S, (7, 4), (7, 19), (17, 19), (17, 4)), sg(7, 11.5, 17, 11.5)]


@icon("hangul-jieut", CAT, "Hangul consonant jieut: a horizontal top bar with an upside down V hanging from its centre.",
      tags=_tags("jieut", "jieud", "j", "ch", "consonant"))
def _(S):
    return [sg(5, 6, 19, 6), pl(S, (6, 19), (12, 6), (18, 19))]


@icon("hangul-chieut", CAT, "Hangul consonant chieut: the jieut shape of a top bar over an upside down V, with a short tick above the bar.",
      tags=_tags("chieut", "chieud", "ch", "aspirated", "consonant"))
def _(S):
    return [sg(12, 3, 12, 6), sg(5, 9.5, 19, 9.5), pl(S, (6, 20), (12, 9.5), (18, 20))]


@icon("hangul-kieuk", CAT, "Hangul consonant kieuk: the giyeok right angle with an extra short horizontal stroke through its middle.",
      tags=_tags("kieuk", "kieuk", "k", "aspirated", "consonant"))
def _(S):
    return [pl(S, (6, 5), (18, 5), (18, 19)), sg(8, 12, 18, 12)]


@icon("hangul-pieup", CAT, "Hangul consonant pieup: a top bar and a longer bottom bar joined by two short vertical stems.",
      tags=_tags("pieup", "pieub", "p", "aspirated", "consonant"))
def _(S):
    return [sg(7, 5, 17, 5), sg(9, 5, 9, 19), sg(15, 5, 15, 19), sg(4.5, 19, 19.5, 19)]


@icon("hangul-hieut", CAT, "Hangul consonant hieut: a short tick on top of a horizontal bar, sitting above a small circle.",
      tags=_tags("hieut", "hieud", "h", "consonant"))
def _(S):
    return [sg(12, 3, 12, 5.5), sg(5.5, 8.5, 18.5, 8.5), line(circle(12, 16.5, 4))]


@icon("hangul-ssanggiyeok", CAT, "Hangul double consonant ssanggiyeok: two small giyeok right angles side by side.",
      tags=_tags("ssanggiyeok", "double giyeok", "kk", "tense", "consonant"))
def _(S):
    return [pl(S, (5, 6), (10, 6), (10, 18)), pl(S, (14, 6), (19, 6), (19, 18))]


@icon("hangul-ssangdigeut", CAT, "Hangul double consonant ssangdigeut: two small squared C digeut shapes side by side.",
      tags=_tags("ssangdigeut", "double digeut", "tt", "tense", "consonant"))
def _(S):
    return [pl(S, (9, 6), (5, 6), (5, 18), (10, 18)), pl(S, (18, 6), (14, 6), (14, 18), (19, 18))]


@icon("hangul-ssangbieup", CAT, "Hangul double consonant ssangbieup: two small bieup boxes with crossbars side by side.",
      tags=_tags("ssangbieup", "double bieup", "pp", "tense", "consonant"))
def _(S):
    return [pl(S, (4.5, 5), (4.5, 19), (9.5, 19), (9.5, 5)), sg(4.5, 12, 9.5, 12),
            pl(S, (14.5, 5), (14.5, 19), (19.5, 19), (19.5, 5)), sg(14.5, 12, 19.5, 12)]


@icon("hangul-ssangsiot", CAT, "Hangul double consonant ssangsiot: two small upside down V shapes like tiny tents side by side.",
      tags=_tags("ssangsiot", "double siot", "ss", "tense", "consonant"))
def _(S):
    return [pl(S, (3.75, 19), (7, 7), (10.25, 19)), pl(S, (13.75, 19), (17, 7), (20.25, 19))]


@icon("hangul-ssangjieut", CAT, "Hangul double consonant ssangjieut: two small jieut shapes, each a top bar over an upside down V.",
      tags=_tags("ssangjieut", "double jieut", "jj", "tense", "consonant"))
def _(S):
    return [sg(3.5, 6, 10.5, 6), pl(S, (3.75, 19), (7, 8.5), (10.25, 19)), sg(13.5, 6, 20.5, 6), pl(S, (13.75, 19), (17, 8.5), (20.25, 19))]


@icon("hangul-a", CAT, "Hangul vowel a: a tall vertical stroke with one short tick sticking out to the right at mid height.",
      tags=_tags("a", "ah", "vowel", "tick right"))
def _(S):
    return [sg(9.5, 3.5, 9.5, 19.5), sg(9.5, 10.5, 17, 10.5)]


@icon("hangul-ya", CAT, "Hangul vowel ya: a tall vertical stroke with two short ticks sticking out to the right.",
      tags=_tags("ya", "yah", "vowel", "two ticks right"))
def _(S):
    return [sg(9.5, 3.5, 9.5, 19.5), sg(9.5, 8, 17, 8), sg(9.5, 14, 17, 14)]


@icon("hangul-eo", CAT, "Hangul vowel eo: a tall vertical stroke with one short tick sticking out to the left at mid height.",
      tags=_tags("eo", "uh", "o", "vowel", "tick left"))
def _(S):
    return [sg(14.5, 4.5, 14.5, 20.5), sg(14.5, 13.5, 8, 13.5)]


@icon("hangul-yeo", CAT, "Hangul vowel yeo: a tall vertical stroke with two short ticks sticking out to the left.",
      tags=_tags("yeo", "yuh", "vowel", "two ticks left"))
def _(S):
    return [sg(14.5, 4.5, 14.5, 20.5), sg(14.5, 10, 8, 10), sg(14.5, 16, 8, 16)]


@icon("hangul-yo", CAT, "Hangul vowel yo: a long horizontal base bar with two short vertical ticks standing on it.",
      tags=_tags("yo", "vowel", "two ticks up"))
def _(S):
    return [sg(4, 19, 20, 19), sg(9, 10, 9, 19), sg(15, 10, 15, 19)]


@icon("hangul-ae", CAT, "Hangul vowel ae: two tall vertical strokes side by side with one short tick running from the left stroke toward the right one.",
      tags=_tags("ae", "eh", "vowel"))
def _(S):
    return [sg(7, 4, 7, 20), sg(17, 4, 17, 20), sg(7, 12, 13, 12)]


@icon("hangul-e", CAT, "Hangul vowel e: two tall vertical strokes side by side with one short tick sticking out to the left of the left stroke.",
      tags=_tags("e", "eh", "vowel"))
def _(S):
    return [sg(12, 4, 12, 20), sg(18, 4, 18, 20), sg(5, 12, 12, 12)]


@icon("hangul-yae", CAT, "Hangul vowel yae: two tall vertical strokes side by side with two short ticks running from the left stroke toward the right one.",
      tags=_tags("yae", "yeh", "vowel"))
def _(S):
    return [sg(7, 4, 7, 20), sg(17, 4, 17, 20), sg(7, 9, 13, 9), sg(7, 15, 13, 15)]


@icon("hangul-ye", CAT, "Hangul vowel ye: two tall vertical strokes side by side with two short ticks sticking out to the left of the left stroke.",
      tags=_tags("ye", "yeh", "vowel"))
def _(S):
    return [sg(12, 4, 12, 20), sg(18, 4, 18, 20), sg(5, 9, 12, 9), sg(5, 15, 12, 15)]


@icon("hangul-wa", CAT, "Hangul vowel wa: a short upright tick on a horizontal bar at the lower left, beside a tall vertical with a tick to the right.",
      tags=_tags("wa", "vowel", "compound"))
def _(S):
    return [sg(3.5, 18, 10.5, 18), sg(7, 11, 7, 18), sg(15, 4, 15, 20), sg(15, 12, 20.5, 12)]


@icon("hangul-wae", CAT, "Hangul vowel wae: a short upright tick on a horizontal bar at the lower left, beside two tall verticals with a tick between them.",
      tags=_tags("wae", "weh", "vowel", "compound"))
def _(S):
    return [sg(3, 18, 8.5, 18), sg(5.75, 11, 5.75, 18), sg(12.5, 4, 12.5, 20), sg(19.5, 4, 19.5, 20), sg(12.5, 12, 15.5, 12)]


@icon("hangul-oe", CAT, "Hangul vowel oe: a short upright tick on a horizontal bar at the lower left, beside a plain tall vertical stroke.",
      tags=_tags("oe", "we", "vowel", "compound"))
def _(S):
    return [sg(4, 18, 11, 18), sg(7.5, 11, 7.5, 18), sg(17, 4, 17, 20)]


@icon("hangul-wo", CAT, "Hangul vowel wo: a horizontal bar with a short stem dropping below it at the lower left, beside a tall vertical with a tick to the left.",
      tags=_tags("wo", "wuh", "vowel", "compound"))
def _(S):
    return [sg(3, 13, 9, 13), sg(6, 13, 6, 19), sg(18, 4, 18, 20), sg(18, 12, 14, 12)]


@icon("hangul-we", CAT, "Hangul vowel we: a horizontal bar with a short stem dropping below it, beside two tall verticals with a tick out to the left.",
      tags=_tags("we", "weh", "vowel", "compound"))
def _(S):
    return [sg(3, 13, 7, 13), sg(5, 13, 5, 19), sg(15, 4, 15, 20), sg(20.5, 4, 20.5, 20), sg(15, 12, 11.5, 12)]


@icon("hangul-wi", CAT, "Hangul vowel wi: a horizontal bar with a short stem dropping below it at the lower left, beside a plain tall vertical stroke.",
      tags=_tags("wi", "wee", "vowel", "compound"))
def _(S):
    return [sg(3.5, 13, 10, 13), sg(6.75, 13, 6.75, 19), sg(17, 4, 17, 20)]


@icon("hangul-ui", CAT, "Hangul vowel ui: a plain horizontal bar at the lower left beside a plain tall vertical stroke on the right.",
      tags=_tags("ui", "eui", "vowel", "compound"))
def _(S):
    return [sg(3.5, 17, 11.5, 17), sg(17, 4, 17, 20)]


# ============================================================================ Hiragana (hand drawn strokes)

def _hira(*extra):
    return ["hiragana", "japanese", "kana", "letter", "syllable", *extra]


@icon("hiragana-i", CAT, "Hiragana i: two short near vertical strokes side by side, the left one longer with a small hook at its foot.",
      tags=_hira("i", "ee", "vowel"))
def _(S):
    return [pa("M8 4.5C7 10 6.5 14.5 8.5 17.5C9.5 19 11 18.5 11.5 16.5"), pa("M17 8.5C17.5 11.5 18 14 18.5 16")]


@icon("hiragana-u", CAT, "Hiragana u: a short dash on top above a stroke that arcs right and sweeps down into a hook to the lower left.",
      tags=_hira("u", "oo", "vowel"))
def _(S):
    return [pa("M9.5 4.5L14.5 4"), pa("M8.5 10C12 8.5 16 9.5 16 13C16 17 12.5 19.5 8.5 20.5")]


@icon("hiragana-e", CAT, "Hiragana e: a short dash on top above a zigzag that runs right, cuts down to the left, then ends in a long tail to the right.",
      tags=_hira("e", "eh", "vowel"))
def _(S):
    return [pa("M9 4L14 5"), pa("M8 10.5C10 10 13 9.5 15.5 10C13 12 10 14 8.5 15.5C11 17 15 18.5 19 19")]


@icon("hiragana-o", CAT, "Hiragana o: a horizontal bar crossed by a vertical stroke that loops into a round belly on the right, with a small dash at the upper right.",
      tags=_hira("o", "oh", "vowel"))
def _(S):
    return [pa("M5 9H15"), pa("M10 4C9.5 9 9 14 8.5 17C7.5 20.5 4.5 19 5 16.5C5.5 13.5 12 12 15 14.5C17.5 16.5 14.5 20 10 19.5"),
            pa("M17.5 4.5L19.5 7")]


@icon("hiragana-ka", CAT, "Hiragana ka: an angular stroke like a 7 with a hooked foot crossed by a slanted downstroke, plus a separate short dash at the right.",
      tags=_hira("ka", "kah", "k"))
def _(S):
    return [pa("M4.5 9.5C8 9 12 9 15 9C16 14 14 18 10.5 19.5"), pa("M10 3.5C9.5 10 8.5 15 5.5 19"), pa("M19 5.5L19.5 9")]


@icon("hiragana-ki", CAT, "Hiragana ki: two horizontal bars crossed by a slanted stroke, with a separate open curve at the bottom.",
      tags=_hira("ki", "kee", "k"))
def _(S):
    return [pa("M6 6.5L18 5.5"), pa("M5.5 11L18.5 10"), pa("M14 3L10 12.5"),
            pa("M17 16C12 15 8 16.5 8.5 18.5C9 20.5 13 20.5 17 19.5")]


@icon("hiragana-ke", CAT, "Hiragana ke: a tall curved upright on the left, and on the right a horizontal bar crossed by a long stroke curving down to the left.",
      tags=_hira("ke", "keh", "k"))
def _(S):
    return [pa("M6.5 4C6 10 6 15 7 19.5"), pa("M11 9.5H19"), pa("M14.5 4C14.5 12 14 17 10.5 20")]


@icon("hiragana-ko", CAT, "Hiragana ko: two short curved horizontal strokes stacked, the top one ending in a small hook and the bottom one curving up at the right.",
      tags=_hira("ko", "koh", "k"))
def _(S):
    return [pa("M6.5 6.5H15.5C17 6.5 17.5 7 17 8.5"), pa("M5.5 17C8 20 14 20.5 19 17.5")]


@icon("hiragana-sa", CAT, "Hiragana sa: a horizontal bar crossed by a slanted stroke, above a separate open curve like a backwards c.",
      tags=_hira("sa", "sah", "s"))
def _(S):
    return [pa("M5 8.5H19"), pa("M14 3.5L10.5 12.5"), pa("M17.5 15.5C11 14.5 8.5 17 9.5 19C10.5 21 15 20.5 17.5 19.5")]


@icon("hiragana-shi", CAT, "Hiragana shi: a single long stroke that drops straight down and curves up to the right at the bottom like a hook.",
      tags=_hira("shi", "si", "she", "sh"))
def _(S):
    return [pa("M8.5 4V14C8.5 18 10.5 19.5 13 19.5C16 19.5 17.5 18 18.5 15.5")]


@icon("hiragana-su", CAT, "Hiragana su: a horizontal bar crossed by a vertical stroke that makes a small loop before dropping into a tail.",
      tags=_hira("su", "soo", "s"))
def _(S):
    return [pa("M5 7.5H19"), pa("M12 4V11.5"), pa("M12 11.5C16.5 11.5 17.5 16.5 14 17.5C11 18 10 14 12.5 13.3"), pa("M14 17.5C13.5 19.5 11.5 20.5 9.5 20")]


@icon("hiragana-se", CAT, "Hiragana se: a long horizontal bar crossed by a short right upright and a longer left upright that curves into a flat base.",
      tags=_hira("se", "seh", "s"))
def _(S):
    return [pa("M4.5 9.5H19.5"), pa("M9 4.5V15C9 18 11 19.5 14 19.5H19"), pa("M16 5V12.5")]


@icon("hiragana-so", CAT, "Hiragana so: a zigzag of a diagonal and a long horizontal, with a curved tail sweeping down and back to the right.",
      tags=_hira("so", "soh", "s"))
def _(S):
    return [pa("M15.5 4.5L8 9.5H17.5"), pa("M13 9.5C9.5 12 9 15 10 17.5C11 20 15 20.5 18 18")]


@icon("hiragana-ta", CAT, "Hiragana ta: a cross shaped stroke on the left beside two short horizontal strokes stacked on the right.",
      tags=_hira("ta", "tah", "t"))
def _(S):
    return [pa("M4.5 9.5H13"), pa("M9 4.5C8.5 10 7 15 4.5 19"), pa("M14 12H19.5"), pa("M13.5 17.5C15 19 18 19 19.5 17.5")]


@icon("hiragana-chi", CAT, "Hiragana chi: a horizontal bar crossed by a slanted stroke that bends into a rounded bowl opening to the left, like a 5.",
      tags=_hira("chi", "ti", "chee", "ch"))
def _(S):
    return [pa("M6.5 7H16.5"), pa("M12 4C11 8 10 11 8.5 12.5C12 11.5 17 12.5 17.5 16C18 19.5 13 20.5 9 18.5")]


@icon("hiragana-tsu", CAT, "Hiragana tsu: a single wide arch that starts flat on the left, curves over at the right and sweeps down into a hook to the lower left.",
      tags=_hira("tsu", "tsoo", "small tsu", "ts"))
def _(S):
    return [pa("M4.5 10.5C8 8 16 7.5 18.5 11.5C19.5 15.5 14 18.5 9.5 19")]


@icon("hiragana-te", CAT, "Hiragana te: a horizontal stroke that folds back at the right end and curves down into a long c shape.",
      tags=_hira("te", "teh", "t"))
def _(S):
    return [pa("M5 7.5H18C13 10 9.5 13 9.5 16C9.5 19 13 20 17.5 19")]


@icon("hiragana-to", CAT, "Hiragana to: a short slanted stroke above a second stroke that curves down and back to the right into a flat base.",
      tags=_hira("to", "toh", "t"))
def _(S):
    return [pa("M9 4L12.5 6.5"), pa("M12 9C9 11 8.5 14 9.5 16.5C10.5 19 14 19.5 18.5 17.5")]


@icon("hiragana-na", CAT, "Hiragana na: a cross shaped stroke with a short dash on the right, above a small loop at the lower right.",
      tags=_hira("na", "nah", "n"))
def _(S):
    return [pa("M4.5 8.5H11"), pa("M8 4C7.5 10 6 14 4 16.5"), pa("M14 5.5L19 6.5"),
            pa("M12.5 10C13 12 12 14 12 15.5C12 19 17 20 18 17C18.5 15 16 14 14.5 15.5")]


@icon("hiragana-ni", CAT, "Hiragana ni: a tall curved upright on the left beside two short horizontal strokes stacked on the right.",
      tags=_hira("ni", "nee", "n"))
def _(S):
    return [pa("M7.5 4C7 10 7 15 7.5 19.5"), pa("M12.5 8.5H19"), pa("M12 17C14 18.5 17 18.5 19 17")]


@icon("hiragana-nu", CAT, "Hiragana nu: two crossing diagonal strokes forming an overlapping loop that ends in a small round curl at the lower right.",
      tags=_hira("nu", "noo", "n"))
def _(S):
    return [pa("M6.5 5.5C9 8 12 12 14.5 15.5C17 19 19.5 18 18 15.5C16.5 13 14.5 14 15 16"),
            pa("M10.5 4C10 9 8.5 14 6.5 17C5 19.5 4.5 17.5 6 15.5")]


@icon("hiragana-ne", CAT, "Hiragana ne: a tall vertical stroke on the left crossed by a zigzag that loops around to the right and ends in a small curl.",
      tags=_hira("ne", "neh", "n"))
def _(S):
    return [pa("M7 4V19"), pa("M4 11.5C7 10.5 10 9 12 7C11.5 12 11.5 16 12.5 18C14 20.5 18.5 19 18.5 16.5C18.5 14 15 14 14.5 16")]


@icon("hiragana-no", CAT, "Hiragana no: a single spiral stroke that starts near the centre and curves over the top and around, like a cursive at sign.",
      tags=_hira("no", "noh", "n", "spiral"))
def _(S):
    return [pa("M12.5 12C9.5 12 9 15.5 11 17.5C14 20 19 17 19 12C19 7 14 4 9.5 6C5.5 8 5 13 7 16")]


@icon("hiragana-ha", CAT, "Hiragana ha: a tall upright on the left, and on the right a horizontal bar crossed by a stroke ending in a small loop.",
      tags=_hira("ha", "hah", "h", "wa particle"))
def _(S):
    return [pa("M6.5 4C6 10 6 15 7 19.5"), pa("M11.5 8H19"), pa("M15 4V14"),
            pa("M15 14C19 14.5 19 19.5 15.5 19.5C12 19.5 11.5 16 14 15.5")]


@icon("hiragana-hi", CAT, "Hiragana hi: a single stroke that starts with a short flick, dips into a deep round bowl and rises with a flick at the right.",
      tags=_hira("hi", "hee", "h"))
def _(S):
    return [pa("M5 8C7 7.5 10.5 8 11 10.5C11.5 15 13 19.5 10 19.5C7 19.5 7 15.5 11.5 14C15 13 18.5 13.5 19 8.5")]


@icon("hiragana-fu", CAT, "Hiragana fu: four small separate strokes, a top curve, a central hooked bowl and a short stroke on each side.",
      tags=_hira("fu", "hu", "foo", "f"))
def _(S):
    return [pa("M10 4.5C11.5 3.5 13.5 3.5 14.5 5"), pa("M12.5 8.5C9 11.5 8 14 10 16.5C12 19 15 18 14.5 15.5C14 13.5 11.5 13.5 11 15.5"),
            pa("M4.5 20L7 16.5"), pa("M17 16.5L19.5 20")]


@icon("hiragana-he", CAT, "Hiragana he: a single stroke rising to a short peak on the left and descending in a longer gentle slope to the right.",
      tags=_hira("he", "heh", "h", "e particle"))
def _(S):
    return [pa("M4 14C6 12 8 9.5 9.5 8.5C11 8 12 8.5 13 9.5C15 12 17 15 19.5 17.5")]


@icon("hiragana-ho", CAT, "Hiragana ho: a tall upright on the left, and on the right two horizontal bars crossed by a stroke ending in a small loop.",
      tags=_hira("ho", "hoh", "h"))
def _(S):
    return [pa("M6.5 4C6 10 6 15 7 19.5"), pa("M11.5 7H19"), pa("M11.5 11.5H19"), pa("M15 4V14.5"),
            pa("M15 14.5C19 15 19 20 15.5 20C12 20 11.5 16.5 14 16")]


@icon("hiragana-ma", CAT, "Hiragana ma: two horizontal bars crossed by a vertical stroke that ends in a small loop at the bottom.",
      tags=_hira("ma", "mah", "m"))
def _(S):
    return [pa("M5.5 7H18.5"), pa("M6 11.5H18"), pa("M12 4V14.5C9 14 7 16 8 18.5C9 20.5 14 20 18 17.5")]


@icon("hiragana-mi", CAT, "Hiragana mi: a stroke that zigzags into a loop at the lower left and sweeps right, crossed by a short slanted stroke at the right.",
      tags=_hira("mi", "mee", "m"))
def _(S):
    return [pa("M5 8.5C8 7.5 11 9 11 12C10 15 8 18 6 18C4 18 4.5 15 8 13.5C12 12 15 14 17 17.5C18 19 19 19 19.5 18"),
            pa("M16 5L14 10.5")]
