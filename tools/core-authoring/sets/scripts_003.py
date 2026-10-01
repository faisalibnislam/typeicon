"""TypeIcon Core: scripts, part 3 (hiragana ma to n, katakana i to n, Devanagari vowels and first consonants).

Each glyph is a schematic of the letter built from a few 2 px strokes so it reads at 24 px: polylines (sharp
corners in Line, 1.5 px fillets in Rounded) and smooth splines. Devanagari letters hang from a headline at y 5
(or y 8 when a vowel mark sits above it). All parts are open strokes, so Filled keeps the counters and only gets
a heavier stroke.
"""
from dsl import circle, dot, icon, line, poly

CAT = "scripts"


def spline(pts, t=0.5):
    """Smooth open path through the points (Catmull-Rom converted to cubic segments)."""
    p = [pts[0]] + list(pts) + [pts[-1]]
    d = f"M{pts[0][0]:g} {pts[0][1]:g}"
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        d += f"C{c1[0]:.2f} {c1[1]:.2f} {c2[0]:.2f} {c2[1]:.2f} {p2[0]:g} {p2[1]:g}"
    return d


def build(S, strokes):
    out = []
    for s in strokes:
        k = s[0]
        if k == "p":
            out.append(line(poly(s[1], r=S.r)))
        elif k == "s":
            out.append(line(spline(s[1])))
        elif k == "c":
            out.append(line(circle(s[1], s[2], s[3])))
        elif k == "d":
            out.append(dot(s[1], s[2], 1.5))
    return out


def xf(strokes, k=0.8, dy=8.0):
    """Squash a Devanagari body (headline at y=5) so there is room for marks above the headline."""
    def m(p):
        return (p[0], round(dy + (p[1] - 5) * k, 2))
    out = []
    for s in strokes:
        if s[0] in ("p", "s"):
            out.append((s[0], [m(q) for q in s[1]]))
        else:
            out.append(("c", s[1], round(dy + (s[2] - 5) * k, 2), round(s[3] * k, 2)))
    return out


GLYPHS = {}

# --------------------------------------------------------------------------- hiragana
GLYPHS["hiragana-mu"] = [
    ("p", [(4, 8), (14, 8)]),
    ("s", [(9, 4), (9.5, 12), (8.5, 17), (5.5, 18.5), (4.5, 15.5), (8, 15.5), (13, 19), (18, 16), (19.5, 12)]),
    ("p", [(17, 4), (19, 7.5)]),
]
GLYPHS["hiragana-me"] = [
    ("s", [(8, 3.5), (9.5, 10), (7, 16), (5, 14), (6.5, 9.5), (12, 9), (17, 12), (18, 17), (14, 20), (10, 18)]),
    ("p", [(16, 4), (11, 10), (7, 18)]),
]
GLYPHS["hiragana-mo"] = [
    ("s", [(10, 3), (10, 14), (11, 19), (15, 19.5), (19, 17)]),
    ("p", [(5, 8), (16, 8)]),
    ("p", [(5, 13), (17, 12.5)]),
]
GLYPHS["hiragana-ya"] = [
    ("s", [(3.5, 10.5), (8, 8.5), (14, 9), (17.5, 11), (17, 15)]),
    ("p", [(7, 3.5), (10, 5.5)]),
    ("p", [(15, 3), (8, 21)]),
]
GLYPHS["hiragana-yu"] = [
    ("s", [(7, 3), (6, 11), (7, 18), (9, 15)]),
    ("s", [(12, 13), (13, 9), (17, 8), (19.5, 12), (18, 18), (14, 19)]),
    ("p", [(13, 3), (13, 21)]),
]
GLYPHS["hiragana-yo"] = [
    ("p", [(5, 8), (16, 8)]),
    ("s", [(11, 3), (11, 13), (7, 15), (6.5, 19), (11, 20.5), (16, 18)]),
]
GLYPHS["hiragana-ra"] = [
    ("p", [(8, 3.5), (12.5, 5)]),
    ("s", [(8, 9.5), (14, 10.5), (16, 14), (14.5, 18.5), (10.5, 20.5), (7, 18.5), (8, 15.5)]),
]
GLYPHS["hiragana-ri"] = [
    ("s", [(6.5, 4), (6.5, 11), (8, 15.5), (11, 16.5)]),
    ("s", [(16, 3), (16, 11), (13.5, 17), (9, 21)]),
]
GLYPHS["hiragana-ru"] = [
    ("s", [(6, 5), (14, 5), (8.5, 10.5), (14.5, 11), (17.5, 14.5), (15, 19), (10, 19), (9, 15.5), (13, 15)]),
]
GLYPHS["hiragana-re"] = [
    ("s", [(7, 3), (7, 12), (5, 18)]),
    ("s", [(3, 9), (10, 8), (10, 14), (11, 18), (15.5, 19), (19, 14), (20, 9.5)]),
]
GLYPHS["hiragana-ro"] = [
    ("s", [(6, 5), (14, 5), (8.5, 10.5), (14.5, 11), (17.5, 15), (14, 19.5), (7, 19)]),
]
GLYPHS["hiragana-wa"] = [
    ("s", [(7, 3), (7, 12), (5, 18)]),
    ("s", [(3, 9), (10, 8), (10, 15), (13, 19), (19, 17.5), (20, 11.5), (15, 10)]),
]
GLYPHS["hiragana-wo"] = [
    ("p", [(6, 5.5), (17, 5.5)]),
    ("s", [(13, 3), (9.5, 9.5), (15, 10), (10, 14.5), (8, 18), (12, 20), (19, 18)]),
]
GLYPHS["hiragana-n"] = [
    ("s", [(10, 3), (7.5, 12), (5, 19), (9, 16), (13, 12), (14, 17), (20, 15.5)]),
]

# --------------------------------------------------------------------------- katakana
GLYPHS["katakana-i"] = [("p", [(15, 4), (7, 12)]), ("p", [(13, 9), (13, 20)])]
GLYPHS["katakana-u"] = [("p", [(12, 3), (12, 6)]), ("p", [(5, 13), (5, 9), (19, 9), (18, 14), (12, 20)])]
GLYPHS["katakana-o"] = [("p", [(4, 8), (20, 8)]), ("p", [(12, 3), (12, 18), (9, 20.5)]), ("p", [(11, 10), (5, 18)])]
GLYPHS["katakana-ka"] = [("p", [(4, 9), (17, 9), (17, 17), (14, 20)]), ("p", [(10, 3), (9, 13), (5, 20)])]
GLYPHS["katakana-ki"] = [("p", [(5, 8), (19, 8)]), ("p", [(4, 13.5), (20, 13.5)]), ("p", [(10, 3), (13, 21)])]
GLYPHS["katakana-ku"] = [("p", [(12, 3), (6, 10)]), ("p", [(9, 7), (19, 7), (11, 20)])]
GLYPHS["katakana-ke"] = [("p", [(11, 3), (5, 10)]), ("p", [(9, 9), (20, 9)]), ("p", [(14, 9), (13.5, 15), (8, 20)])]
GLYPHS["katakana-ko"] = [("p", [(5, 5), (19, 5), (19, 19), (5, 19)])]
GLYPHS["katakana-sa"] = [("p", [(4, 8), (20, 8)]), ("p", [(8, 3), (8, 13)]), ("p", [(16, 3), (16, 13), (11, 20)])]
GLYPHS["katakana-shi"] = [("p", [(4, 4), (8, 6.5)]), ("p", [(4, 10), (8, 12.5)]), ("s", [(4, 20), (12, 17), (19, 6)])]
GLYPHS["katakana-su"] = [("p", [(5, 6), (18, 6), (7, 20)]), ("p", [(12.5, 13), (19, 19)])]
GLYPHS["katakana-se"] = [("p", [(4, 10), (19, 10), (19, 7)]), ("p", [(9, 4), (9, 17), (20, 17)])]
GLYPHS["katakana-so"] = [("p", [(6, 5), (8, 9)]), ("p", [(17, 4), (14, 12), (8, 20)])]
GLYPHS["katakana-ta"] = [("p", [(12, 3), (6, 10)]), ("p", [(9, 7), (19, 7), (8, 20)]), ("p", [(10, 12), (13, 14)])]
GLYPHS["katakana-chi"] = [("p", [(15, 3), (7, 6)]), ("p", [(4, 11), (20, 11)]), ("p", [(12, 6), (12, 16), (8, 20.5)])]
GLYPHS["katakana-tsu"] = [("p", [(6, 4), (8, 9)]), ("p", [(12, 3), (14, 8.5)]), ("p", [(19, 4), (15, 13), (8, 20)])]
GLYPHS["katakana-te"] = [("p", [(7, 5), (17, 5)]), ("p", [(4, 11), (20, 11)]), ("p", [(12, 11), (12, 17), (8, 20.5)])]
GLYPHS["katakana-na"] = [("p", [(4, 9), (20, 9)]), ("s", [(12, 3), (11.5, 12), (5, 20)])]
GLYPHS["katakana-nu"] = [("p", [(5, 5), (17, 5), (6, 20)]), ("p", [(9, 11), (19, 19)])]
GLYPHS["katakana-ne"] = [("p", [(11, 3), (13, 5)]), ("p", [(5, 9), (19, 9), (6, 17)]), ("p", [(12, 12), (12, 21)]), ("p", [(16, 14), (19, 18)])]
GLYPHS["katakana-ha"] = [("p", [(9, 6), (4, 19)]), ("p", [(15, 6), (20, 19)])]
GLYPHS["katakana-hi"] = [("p", [(5, 4), (5, 19), (19, 19)]), ("p", [(5, 11), (18, 8)])]
GLYPHS["katakana-ho"] = [("p", [(4, 8), (20, 8)]), ("p", [(12, 3), (12, 19), (9, 21)]), ("p", [(8, 13), (5, 19)]), ("p", [(16, 13), (19, 19)])]
GLYPHS["katakana-ma"] = [("p", [(5, 6), (19, 6), (8, 15)]), ("p", [(11, 14), (18, 20)])]
GLYPHS["katakana-mi"] = [("p", [(8, 4), (18, 7)]), ("p", [(6, 10), (19, 13)]), ("p", [(4, 16), (20, 19)])]
GLYPHS["katakana-mu"] = [("p", [(11, 4), (5, 18), (19, 18)]), ("p", [(16, 12), (19, 15)])]
GLYPHS["katakana-me"] = [("s", [(18, 4), (14, 12), (6, 20)]), ("p", [(5, 7), (18, 18)])]
GLYPHS["katakana-mo"] = [("p", [(6, 5), (18, 5)]), ("p", [(6, 11), (18, 11)]), ("s", [(12, 3), (12, 15), (14, 18), (19, 18)])]
GLYPHS["katakana-ya"] = [("p", [(4, 11), (19, 8), (17, 15)]), ("p", [(13, 3), (8, 21)])]
GLYPHS["katakana-yu"] = [("p", [(5, 6), (16, 6), (16, 19)]), ("p", [(3, 19), (21, 19)])]
GLYPHS["katakana-yo"] = [("p", [(5, 5), (19, 5), (19, 19), (5, 19)]), ("p", [(5, 12), (19, 12)])]
GLYPHS["katakana-ra"] = [("p", [(7, 4), (17, 4)]), ("p", [(4, 10), (19, 10), (17, 16), (8, 20)])]
GLYPHS["katakana-ri"] = [("p", [(7, 4), (7, 14)]), ("s", [(16, 3), (16, 12), (12, 18), (8, 21)])]
GLYPHS["katakana-ru"] = [("s", [(7, 5), (7, 14), (4, 19)]), ("s", [(15, 4), (15, 16), (17, 19), (20, 14)])]
GLYPHS["katakana-re"] = [("p", [(8, 3), (8, 18), (20, 9)])]
GLYPHS["katakana-wa"] = [("p", [(5, 11), (5, 6), (19, 6), (18, 12), (11, 20)])]
GLYPHS["katakana-wo"] = [("p", [(5, 5), (19, 5)]), ("p", [(5, 11), (19, 11)]), ("p", [(19, 5), (18, 12), (9, 20)])]
GLYPHS["katakana-n"] = [("p", [(4, 5), (8, 8)]), ("p", [(5, 20), (13, 17), (20, 6)])]

# --------------------------------------------------------------------------- devanagari
def hd(a=3, b=21, y=5):
    return ("p", [(a, y), (b, y)])


def stem(x=16.5, y1=5, y2=20):
    return ("p", [(x, y1), (x, y2)])


THREE = ("s", [(5, 8.5), (9, 7), (10.5, 9.5), (7, 12), (10.5, 14), (10.5, 17), (7, 19.5), (4.5, 17.5)])
AA = [hd(), THREE, ("p", [(10, 12), (13, 12)]), stem(13), stem(18.5)]
EE = ("s", [(14, 5), (14, 8.5), (10, 12), (6, 14), (8, 18), (12, 19), (15, 17)])
UU = ("s", [(8, 5), (8, 7.5), (12, 9.5), (8, 11.5), (7.5, 15), (11, 18), (16, 18), (19, 16)])
I_ = ("s", [(15, 5), (8, 8), (11, 11), (15, 13), (15.5, 17), (11.5, 20), (7, 18.5)])
KA_LOOP = ("c", 8, 12, 3)

GLYPHS["devanagari-aa"] = AA
GLYPHS["devanagari-i"] = [hd(4, 20), I_]
GLYPHS["devanagari-ii"] = xf([hd(4, 20), I_], 0.8, 8) + [("s", [(10, 6), (13, 3.5), (17, 5)])]
GLYPHS["devanagari-u"] = [hd(4, 20), UU]
GLYPHS["devanagari-uu"] = xf([hd(4, 20), UU], 0.85, 5) + [("s", [(11, 19), (14, 21), (18, 19.5)])]
GLYPHS["devanagari-vocalic-r"] = [hd(3, 19), ("s", [(6, 8), (10, 7), (12, 10), (9, 12.5), (6, 12.5), (6, 16), (9, 19), (13, 18.5)]),
                                  ("s", [(17, 5), (17, 14), (18, 18), (15, 20.5)])]
GLYPHS["devanagari-e"] = [hd(6, 16), EE]
GLYPHS["devanagari-ai"] = xf([hd(6, 16), EE], 0.8, 8) + [("p", [(8, 3), (10, 6)]), ("p", [(12, 3), (14, 6)])]
GLYPHS["devanagari-o"] = xf(AA, 0.8, 8) + [("p", [(10, 3), (13, 6)])]
GLYPHS["devanagari-au"] = xf(AA, 0.8, 8) + [("p", [(8, 3), (10.5, 6)]), ("p", [(12, 3), (14.5, 6)])]
GLYPHS["devanagari-ka"] = [hd(), stem(14), KA_LOOP, ("p", [(11, 12), (14, 12)]), ("s", [(14, 14.5), (18, 14.5), (19, 17.5), (16, 20)])]
GLYPHS["devanagari-kha"] = [hd(), stem(16.5), ("c", 9, 12, 3.5), ("p", [(12.5, 12), (16.5, 12)])]
GLYPHS["devanagari-ga"] = [hd(), ("p", [(7, 5), (7, 17), (4.5, 20)]), ("p", [(7, 12), (16.5, 12)]), stem(16.5)]
GLYPHS["devanagari-gha"] = [hd(12, 21), stem(16.5), ("p", [(5, 12), (16.5, 12)]),
                            ("s", [(5, 12), (5, 16), (8, 19.5), (11, 16), (11, 12)])]
GLYPHS["devanagari-nga"] = [hd(), ("s", [(5, 8.5), (9, 7), (10.5, 9.5), (7, 12), (10.5, 14), (10.5, 17), (7, 19.5), (4.5, 17.5)]),
                            ("d", 17, 14)]
GLYPHS["devanagari-cha"] = [hd(), stem(16), ("p", [(10, 12), (16, 12)]),
                            ("s", [(10, 12), (6.5, 12), (5, 15), (7.5, 17.5), (10.5, 16)])]
GLYPHS["devanagari-chha"] = [hd(4, 20), ("c", 9, 9.7, 2.8), ("c", 9, 15.7, 3.3),
                             ("s", [(12.3, 15.7), (16, 15), (18, 18), (15, 20.5)])]
GLYPHS["devanagari-ja"] = [hd(), stem(16.5), ("p", [(5, 9), (11, 9), (6, 14.5), (16.5, 14.5)])]
GLYPHS["devanagari-jha"] = [hd(), stem(17.5), THREE, ("p", [(10.5, 12), (17.5, 12)])]
GLYPHS["devanagari-nya"] = [hd(), stem(16.5), ("s", [(13, 9), (8, 8), (5.5, 11), (8, 13), (11, 12.5)]),
                            ("p", [(4, 14), (16.5, 14)]), ("s", [(8, 14), (8, 17.5), (11, 20)])]
GLYPHS["devanagari-tta"] = [hd(4, 20), ("s", [(15, 5), (15, 8), (10, 9), (7, 12), (8, 16), (12, 18.5), (16, 17.5), (17.5, 14.5)])]
GLYPHS["devanagari-ttha"] = [hd(4, 20), ("c", 12, 13, 5.5)]
GLYPHS["devanagari-dda"] = [hd(4, 20), ("s", [(15, 5), (15, 8), (10, 8.5), (6.5, 12), (8, 15.5), (13, 15.5), (17.5, 16.5), (18, 19.5), (15, 21)])]
GLYPHS["devanagari-ddha"] = [hd(4, 20), ("s", [(15, 5), (15, 7.5), (9, 8.5), (6.5, 11), (9, 13), (14, 13.5), (17, 16), (14, 19.5), (9, 19.5), (6, 17)])]
GLYPHS["devanagari-nna"] = [hd(), stem(17), ("c", 8, 11.5, 3.2), ("p", [(11.2, 11.5), (17, 11.5)]), ("p", [(8, 14.7), (8, 19)])]
GLYPHS["devanagari-ta"] = [hd(), stem(16.5), ("p", [(8, 12), (16.5, 12)]), ("s", [(8, 12), (5, 14), (5.5, 17.5), (9, 19.5), (12, 18)])]
GLYPHS["devanagari-tha"] = [hd(11, 21), stem(17), ("c", 8, 13.5, 3.2), ("p", [(11.2, 13.5), (17, 13.5)]),
                            ("s", [(8, 16.7), (9, 19.5), (13, 19.5)])]
GLYPHS["devanagari-da"] = [hd(4, 20), ("s", [(7, 7), (10, 6.5), (15, 8), (14, 11.5), (8, 15.5), (8, 19), (12, 20), (16, 18)])]


# --------------------------------------------------------------------------- registration
# name: (letter, shape phrase for the description)
META = {
    "hiragana-mu": ("mu", "a crossbar with a looping stroke and a small dash at the upper right"),
    "hiragana-me": ("me", "two crossing strokes that form an overlapping loop"),
    "hiragana-mo": ("mo", "a hooked vertical stroke crossed by two short bars"),
    "hiragana-ya": ("ya", "a curved stroke, a small dash and a long diagonal"),
    "hiragana-yu": ("yu", "a tall curved stroke beside a round loop with a vertical line through it"),
    "hiragana-yo": ("yo", "a short bar crossing a vertical stroke that ends in a small loop"),
    "hiragana-ra": ("ra", "a short dash above a stroke that swings into a round bowl"),
    "hiragana-ri": ("ri", "two upright strokes, a short hooked one and a longer curving one"),
    "hiragana-ru": ("ru", "a zigzag stroke ending in a round bowl with a small closed loop"),
    "hiragana-re": ("re", "a tall vertical crossed by a zigzag with an upward flick"),
    "hiragana-ro": ("ro", "a zigzag stroke ending in a round open bowl"),
    "hiragana-wa": ("wa", "a tall vertical crossed by a zigzag with a wide rounded belly"),
    "hiragana-wo": ("wo", "a short bar over a slanted zigzag with a flat curved tail"),
    "hiragana-n": ("n", "one stroke with a long diagonal, a small hump and a rising flick"),
    "katakana-i": ("i", "a short diagonal with a vertical stem hanging from it"),
    "katakana-u": ("u", "a short tick above a flat roof that bends into a hook"),
    "katakana-o": ("o", "a crossbar with a hooked stem and a diagonal stroke"),
    "katakana-ka": ("ka", "a horizontal stroke with a hooked right end and a slanted stroke"),
    "katakana-ki": ("ki", "two horizontal bars crossed by a slightly slanted vertical"),
    "katakana-ku": ("ku", "a short stroke joined to a bar that bends into a long diagonal"),
    "katakana-ke": ("ke", "a short diagonal, a bar and a long curving stroke"),
    "katakana-ko": ("ko", "a squared bracket of top bar, upright and bottom bar"),
    "katakana-sa": ("sa", "a crossbar with two vertical strokes, the right one curving left"),
    "katakana-shi": ("shi", "two short dashes and a long rising stroke"),
    "katakana-su": ("su", "a bar bending into a long diagonal with a short branch"),
    "katakana-se": ("se", "a bar with a small hook crossed by a stem that turns into a flat base"),
    "katakana-so": ("so", "a short upright dash and a long sweeping stroke"),
    "katakana-ta": ("ta", "a bent long diagonal with a short left stroke and a small dash inside"),
    "katakana-chi": ("chi", "a slanted dash over a bar with a stem curving down to the left"),
    "katakana-tsu": ("tsu", "two short dashes above a long sweeping stroke"),
    "katakana-te": ("te", "two bars with a stem dropping from the middle and curving left"),
    "katakana-na": ("na", "a horizontal bar crossed by a vertical stroke curving left"),
    "katakana-nu": ("nu", "a bar bending into a long diagonal crossed by a short stroke"),
    "katakana-ne": ("ne", "a dot, a bent bar, a short stem and a small stroke to the right"),
    "katakana-ha": ("ha", "two separate strokes spreading apart like an open inverted V"),
    "katakana-hi": ("hi", "a stem with a flat base and a short stroke running right"),
    "katakana-ho": ("ho", "a crossbar with a hooked stem and two small diagonal dashes"),
    "katakana-ma": ("ma", "a bar bending into a short diagonal with a small dash below"),
    "katakana-mi": ("mi", "three short parallel strokes sloping down to the right"),
    "katakana-mu": ("mu", "a sloping stroke turning into a flat base with a small dash"),
    "katakana-me": ("me", "a long curving stroke crossed by a short diagonal"),
    "katakana-mo": ("mo", "two bars crossed by a stem that turns right into a base"),
    "katakana-ya": ("ya", "a hooked horizontal stroke crossed by a long slanted stroke"),
    "katakana-yu": ("yu", "a top bar, a right upright and a long flat base"),
    "katakana-yo": ("yo", "three horizontal bars joined by an upright on the right"),
    "katakana-ra": ("ra", "a short dash above a longer stroke that bends into a hook"),
    "katakana-ri": ("ri", "a short upright beside a longer one curving to the left"),
    "katakana-ru": ("ru", "a short curved stroke beside an upright with an upward flick"),
    "katakana-re": ("re", "a single vertical stroke turning into a rising flick"),
    "katakana-wa": ("wa", "a short upright joined to a roof that bends into a hook"),
    "katakana-wo": ("wo", "two horizontal bars joined by a stroke that bends into a hook"),
    "katakana-n": ("n", "a short dash and a long rising stroke"),
    "devanagari-aa": ("aa", "a curled 3 shaped stroke beside two vertical stems under a headline"),
    "devanagari-i": ("i", "a hooked curling stroke hanging below a headline"),
    "devanagari-ii": ("ii", "the curling i stroke with a small hook above the headline"),
    "devanagari-u": ("u", "a 3 shaped curve whose lower end sweeps into a tail"),
    "devanagari-uu": ("uu", "the u curve with an extra curl hooking off its tail"),
    "devanagari-vocalic-r": ("vocalic r", "a curled bowl with a short hooked stroke dropping on the right"),
    "devanagari-e": ("e", "a narrow angled curl folding back at the bottom"),
    "devanagari-ai": ("ai", "the e curl with two small slanted strokes above the headline"),
    "devanagari-o": ("o", "the aa shape with a small slanted stroke above the headline"),
    "devanagari-au": ("au", "the aa shape with two small slanted strokes above the headline"),
    "devanagari-ka": ("ka", "a vertical stem with a small loop on the left and a curled hook on the right"),
    "devanagari-kha": ("kha", "a small round loop joined to a vertical stem"),
    "devanagari-ga": ("ga", "a short hooked upright joined by a bar to a full stem"),
    "devanagari-gha": ("gha", "a small u shaped loop joined to a tall stem"),
    "devanagari-nga": ("nga", "a curled 3 shaped stroke with a single dot to its right"),
    "devanagari-cha": ("cha", "a short bar with a curled hook on the left joined to a stem"),
    "devanagari-chha": ("chha", "two small stacked loops with a tail on the right and no stem"),
    "devanagari-ja": ("ja", "a zigzag stroke joined to a vertical stem"),
    "devanagari-jha": ("jha", "a curled 3 shaped stroke joined by a bar to a vertical stem"),
    "devanagari-nya": ("nya", "a curled stroke crossed by a bar that runs to a vertical stem"),
    "devanagari-tta": ("tta", "a single rounded hook with a curled tail"),
    "devanagari-ttha": ("ttha", "a closed round loop"),
    "devanagari-dda": ("dda", "a backwards c shaped curve ending in a small curl"),
    "devanagari-ddha": ("ddha", "two stacked curves with a hook at the bottom"),
    "devanagari-nna": ("nna", "a loop, a short bar and a tall vertical stem"),
    "devanagari-ta": ("ta", "a short curved hook joined by a bar to a vertical stem"),
    "devanagari-tha": ("tha", "a small looped curl joined to a stem under a partial headline"),
    "devanagari-da": ("da", "a hooked curl with a small tail at the bottom"),
}
SCRIPT = {"hiragana": ("Hiragana", "japanese", ["kana", "japanese", "hiragana", "syllable"]),
          "katakana": ("Katakana", "japanese", ["kana", "japanese", "katakana", "syllable"]),
          "devanagari": ("Devanagari", "hindi", ["devanagari", "hindi", "sanskrit", "indic"])}


def reg(name, strokes):
    kind = name.split("-")[0]
    letter, shape = META[name]
    label = SCRIPT[kind][0]
    tags = SCRIPT[kind][2] + [letter, "letter", "alphabet"]

    @icon(name, CAT, f"{label} letter {letter}, drawn as {shape}.", tags=tags)
    def _(S):
        return build(S, strokes)


for _name, _strokes in GLYPHS.items():
    reg(_name, _strokes)
