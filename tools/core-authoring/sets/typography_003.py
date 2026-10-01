"""TypeIcon Core: typography, batch 003 (editor commands, writing systems, type tools and layout)."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "typography"


def chev(x, y, dx, s=2.25, r=0.0):
    """Arrow head chevron with tip at (x, y) pointing along dx (+1 right, -1 left)."""
    return poly([(x - dx * s, y - s), (x, y), (x - dx * s, y + s)], r=r)


def block(x, y, w, h):
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h))


def ring_arrow(cx, cy, r, a0, a1, head=2.4):
    """Circular arrow: arc from a0 to a1 (clockwise) with a solid head at the end."""
    t = math.radians(a1)
    ex, ey = cx + r * math.cos(t), cy + r * math.sin(t)
    tx, ty = -math.sin(t), math.cos(t)
    nx, ny = math.cos(t), math.sin(t)
    tip = (ex + tx * head, ey + ty * head)
    a = (ex + nx * head, ey + ny * head)
    b = (ex - nx * head, ey - ny * head)
    return [line(arc(cx, cy, r, a0, a1)), solid(poly([tip, a, b], closed=True))]


def board(S, y0=4, h=18):
    return [shell(rect(5, y0, 14, h, S.R)), shell(rect(9, y0 - 2, 6, 4, min(S.R, 1.5)))]


# ============================================================================ editor commands

@icon("match-whole-word", CAT, "Letters a and b inside square brackets, the whole word search option.",
      tags=["whole word", "find", "search", "match word", "exact word", "regex", "editor"])
def _(S):
    return [line(poly([(5, 4), (2.5, 4), (2.5, 17), (5, 17)], r=S.r * 0.5)),
            line(poly([(19, 4), (21.5, 4), (21.5, 17), (19, 17)], r=S.r * 0.5)),
            line(circle(8.5, 11.5, 2.25)), line(seg(10.75, 9, 10.75, 13.75)),
            line(seg(13.5, 6.5, 13.5, 13.75)), line(circle(15.75, 11.5, 2.25)),
            line(seg(4.5, 21, 19.5, 21))]


@icon("paste-as-text", CAT, "Clipboard with a capital T on its sheet, pasting without formatting.",
      tags=["paste", "plain text", "no formatting", "clipboard", "paste special", "unformatted", "editor"])
def _(S):
    return [*board(S), detail(seg(9, 10, 15, 10)), detail(seg(12, 10, 12, 18))]


@icon("clipboard-history", CAT, "Clipboard outline with a small clock at its lower corner.",
      tags=["clipboard", "history", "recent copies", "copy history", "paste", "clock", "editor"])
def _(S):
    return [line(poly([(19, 9), (19, 4), (5, 4), (5, 21), (9, 21)], r=S.r * 0.5)),
            shell(rect(9, 2, 6, 4, min(S.R, 1.5))),
            shell(circle(16.5, 16.5, 5.5)),
            detail(poly([(16.5, 13.5), (16.5, 16.5), (18.5, 17.5)]))]


@icon("insert-symbol", CAT, "Omega sign inside a rounded square, the insert symbol command.",
      tags=["symbol", "special character", "omega", "insert", "character map", "glyph", "editor"])
def _(S):
    om = "M7.5 17H10.5C8.5 15.8 7.5 14 7.5 12A4.5 4.5 0 0 1 16.5 12C16.5 14 15.5 15.8 13.5 17H16.5"
    return [shell(rect(3, 3, 18, 18, S.R)), detail(om, stroke_miterlimit="2")]


@icon("insert-equation", CAT, "Pi sign and an equals mark inside a rounded square, the insert equation command.",
      tags=["equation", "pi", "math", "formula", "insert", "equals", "editor"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)),
            detail(seg(6.5, 9, 13.5, 9)), detail(seg(8.5, 9, 8.5, 16)),
            detail(poly([(12, 9), (12, 15), (13.5, 16)], r=S.r * 0.5)),
            detail(seg(15.5, 10.5, 18, 10.5)), detail(seg(15.5, 14, 18, 14))]


@icon("autosave", CAT, "Document with a circular arrow and a small cloud at its lower corner.",
      tags=["autosave", "auto save", "saving", "sync", "cloud", "backup", "document"])
def _(S):
    return [line(poly([(14.5, 9), (14.5, 6), (11.5, 3), (3.5, 3), (3.5, 21), (8.5, 21)], r=S.r * 0.5)),
            detail(poly([(11.5, 3), (11.5, 6), (14.5, 6)])),
            detail(seg(6.5, 9, 9.5, 9)), detail(seg(6.5, 13, 9, 13)),
            *ring_arrow(16.5, 16.5, 5.25, 15, 310),
            solid("M14.2 19A1.6 1.6 0 0 1 14.6 15.9A2 2 0 0 1 18.2 15.5A1.8 1.8 0 0 1 19 19Z")]


# ============================================================================ writing systems

@icon("ruby-annotation", CAT, "Large character with a row of tiny marks above it, ruby annotation over East Asian text.",
      tags=["ruby", "furigana", "annotation", "pronunciation", "japanese", "cjk", "reading guide"])
def _(S):
    return [line(seg(4.5, 3.5, 7.5, 3.5)), line(seg(10.5, 3.5, 13.5, 3.5)), line(seg(16.5, 3.5, 19.5, 3.5)),
            line(seg(4, 12.5, 20, 12.5)), line(seg(12, 8, 12, 21)),
            line(poly([(11, 14), (6.5, 20)], r=0)), line(poly([(13, 14), (17.5, 20)], r=0))]


@icon("emphasis-dots", CAT, "Three character marks in a row, each with a small dot above it.",
      tags=["emphasis marks", "dots above", "bouten", "kenten", "emphasis", "cjk", "stress"])
def _(S):
    h = 2.5 if S.name == "line" else 1.5

    def ko(cx):
        return [line(seg(cx - h, 11, cx + h, 11)), line(seg(cx, 11, cx, 20.5)), line(seg(cx - h, 20.5, cx + h, 20.5))]
    return [dot(5, 4.5, 1.5), dot(12, 4.5, 1.5), dot(19, 4.5, 1.5), *ko(5), *ko(12), *ko(19)]


@icon("kashida-justification", CAT, "Cursive stroke with a stretched middle and arrows pointing outward above it.",
      tags=["kashida", "tatweel", "arabic", "justify", "stretch", "elongation", "cursive"])
def _(S):
    return [line(seg(5, 7, 19, 7)), line(chev(3.5, 7, -1, 2.5, S.r * 0.4)), line(chev(20.5, 7, 1, 2.5, S.r * 0.4)),
            line("M3 14.5C5 14.5 5.5 18.5 8 18.5H16C18.5 18.5 19 14.5 21 14.5")]


@icon("bidirectional-text", CAT, "Two lines of text, one running left to right and one right to left, each with an arrow.",
      tags=["bidi", "rtl", "ltr", "mixed direction", "arabic", "hebrew", "text direction"])
def _(S):
    return [line(seg(3, 6, 20, 6)), line(chev(21, 6, 1, 2.25, S.r * 0.5)),
            line(seg(3, 11, 14, 11)), line(seg(10, 15.5, 21, 15.5)),
            line(seg(4, 20.5, 21, 20.5)), line(chev(3, 20.5, -1, 2.25, S.r * 0.5))]


@icon("boustrophedon", CAT, "Three text lines joined into a zigzag path that turns around at each line end.",
      tags=["boustrophedon", "zigzag", "ancient writing", "alternating direction", "snake", "serpentine", "writing direction"])
def _(S):
    return [line("M3 5H17A3.5 3.5 0 0 1 17 12H7A3.5 3.5 0 0 0 7 19H19"), line(chev(21, 19, 1, 2.25, S.r * 0.5))]


@icon("phonetic-transcription", CAT, "Schwa sign between two slashes, a phonetic transcription.",
      tags=["ipa", "phonetic", "pronunciation", "schwa", "phonetics", "linguistics", "transcription"])
def _(S):
    return [line(seg(6.5, 3.5, 3, 20.5)), line(seg(21, 3.5, 17.5, 20.5)),
            line(seg(8.5, 12.5, 15.5, 12.5)), line(arc(12, 12.5, 3.5, 215, 180))]


@icon("transliteration", CAT, "Latin letter A, an arrow and a Cyrillic letter Ya, converting between scripts.",
      tags=["transliterate", "romanization", "script conversion", "cyrillic", "latin", "alphabet", "convert"])
def _(S):
    return [line(seg(4, 4.5, 19, 4.5)), line(chev(21, 4.5, 1, 2.25, S.r * 0.5)),
            line(poly([(2.5, 21), (6, 11), (9.5, 21)], r=S.r * 0.4)), line(seg(4, 17.5, 8, 17.5)),
            line(poly([(21, 10.5), (18, 10.5), (16.25, 12), (16.25, 14), (18, 15.5), (21, 15.5)], r=S.r * 0.5)),
            line(seg(21, 10.5, 21, 21)), line(seg(18, 15.5, 15.5, 21))]


@icon("enclosed-character", CAT, "Letter A inside a circle with a second circle overlapping behind it.",
      tags=["circled letter", "enclosed alphanumeric", "circled character", "badge letter", "initial", "monogram", "symbol"])
def _(S):
    return [shell(circle(10, 14, 7)),
            line(arc(15, 9, 6, 212, 418)),
            detail(poly([(7, 18), (10, 9.5), (13, 18)], r=S.r * 0.4)), detail(seg(8.25, 15.5, 11.75, 15.5))]


@icon("dyslexia-friendly-text", CAT, "Letters b and d with weighted bottoms standing on a thick baseline.",
      tags=["dyslexia", "readable", "accessibility", "b and d", "reading aid", "inclusive", "letters"])
def _(S):
    return [line(seg(4, 3, 4, 16)), line(circle(7, 13, 3)),
            line(seg(20, 3, 20, 16)), line(circle(17, 13, 3)),
            solid(rect(2, 19, 20, 2.5))]


# ============================================================================ type tools and print shop

def rot(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def axis(tip, direction_deg):
    """Local frame (u along the body from the tip, v sideways) for a tool lying along a direction."""
    a = math.radians(direction_deg)
    d = (math.cos(a), math.sin(a))
    n = (-d[1], d[0])
    return lambda u, v: (tip[0] + d[0] * u + n[0] * v, tip[1] + d[1] * u + n[1] * v)


@icon("typing-speed", CAT, "Keyboard with a small speedometer gauge above it.",
      tags=["typing speed", "wpm", "words per minute", "keyboard", "gauge", "typing test", "performance"])
def _(S):
    return [line(arc(12, 10, 7, 180, 360)), line(seg(12, 10, 15.5, 5.5)), dot(12, 10, 1.5),
            shell(rect(2.5, 14, 19, 7, min(S.R, 2))),
            dot(6.5, 17.5, 1), dot(10, 17.5, 1), dot(14, 17.5, 1), dot(17.5, 17.5, 1)]


@icon("grease-pencil", CAT, "Wax marking pencil with a spiral paper wrapper and a peeled tip.",
      tags=["china marker", "wax pencil", "grease pencil", "marking pencil", "glass pencil", "peel pencil", "mark"])
def _(S):
    def R(pts):
        return rot(pts, 45)
    return [shell(poly(R([(12, 2.5), (15, 7), (15, 21), (9, 21), (9, 7)]), closed=True, r=S.r * 0.6)),
            detail(poly(R([(9, 7), (15, 7)]))),
            detail(poly(R([(9, 12), (15, 16)]))),
            detail(poly(R([(9, 17), (15, 21)])))]


@icon("typewriter-eraser", CAT, "Pencil shaped eraser with a round rubber end and a small brush at the other end.",
      tags=["eraser", "typewriter", "correction", "rubber", "brush", "erase", "office"])
def _(S):
    def R(pts):
        return rot(pts, 45)
    return [shell(poly(R([(9, 2.5), (15, 2.5), (15, 16), (9, 16)]), closed=True, r=S.r * 0.6)),
            detail(poly(R([(9, 7), (15, 7)]))),
            line(poly(R([(10, 16), (8.5, 21)]))), line(poly(R([(12, 16), (12, 21.5)]))), line(poly(R([(14, 16), (15.5, 21)])))]


@icon("pica-ruler", CAT, "Straight ruler with long and short type scale marks along its top edge.",
      tags=["pica", "points", "type ruler", "line gauge", "measure", "typographer", "printing"])
def _(S):
    return [shell(rect(2.5, 7, 19, 10, min(S.R, 2))),
            detail(seg(6.5, 7, 6.5, 12)), detail(seg(10.5, 7, 10.5, 10.5)), detail(seg(14.5, 7, 14.5, 12)),
            detail(seg(18.5, 7, 18.5, 10.5)), block(5, 14, 2.5, 1.5), block(13, 14, 2.5, 1.5)]


@icon("linen-tester", CAT, "Small folding magnifier with a square lens on a hinged base.",
      tags=["thread counter", "linen tester", "loupe", "magnifier", "print inspection", "textile", "lens"])
def _(S):
    return [shell(rect(7, 3, 10, 9, min(S.R, 2))), detail(seg(9.5, 8, 11.5, 6)),
            line(seg(7, 12, 5, 16)), line(seg(17, 12, 19, 16)),
            shell(rect(2.5, 16, 19, 5, min(S.R, 1.5)))]


@icon("printers-chase", CAT, "Rectangular metal frame with a crossbar, lines of type on one side and locking wedges on the other.",
      tags=["chase", "letterpress", "type frame", "printing", "forme", "typesetting", "quoins"])
def _(S):
    return [shell(rect(2.5, 3.5, 19, 17, min(S.R, 2))), detail(seg(14, 3.5, 14, 20.5)),
            detail(seg(5.5, 8, 11.5, 8)), detail(seg(5.5, 12, 11.5, 12)), detail(seg(5.5, 16, 11.5, 16)),
            Part("dot", poly([(16.5, 6.5), (19, 6.5), (19, 9.5)], closed=True)),
            Part("dot", poly([(16.5, 17.5), (19, 17.5), (16.5, 14.5)], closed=True))]


@icon("type-slug", CAT, "Long metal bar with a row of raised letters cast along its top edge.",
      tags=["slug", "linotype", "line of type", "hot metal", "typesetting", "letterpress", "metal type"])
def _(S):
    rx = 0 if S.name == "line" else 2.5
    return [shell(rect(2.5, 12, 19, 7, rx)),
            block(4.5, 5.5, 2, 6.5), block(8.5, 7.5, 3, 4.5), block(13, 5.5, 2, 6.5), block(17.5, 7.5, 2, 4.5)]


@icon("dry-transfer-lettering", CAT, "Sheet printed with a letter A and a pencil rubbing over it.",
      tags=["rub on lettering", "transfer sheet", "burnish", "lettering", "rub down", "graphic design"])
def _(S):
    f = axis((14.5, 13.5), -45)
    body = [f(0, 0), f(2.5, -2), f(8, -2), f(8, 2), f(2.5, 2)]
    return [shell(rect(2.5, 3, 12, 18, min(S.R, 2))),
            detail(poly([(5, 17), (8.5, 7), (12, 17)], r=S.r * 0.4)), detail(seg(6.2, 13.5, 10.8, 13.5)),
            shell(poly(body, closed=True, r=S.r * 0.5))]


@icon("proof-press", CAT, "Flat bed printing press with a large roller held on two posts above the bed and a hand crank.",
      tags=["proofing press", "letterpress", "printing press", "roller", "galley proof", "print shop"])
def _(S):
    rx = 0 if S.name == "line" else 2
    return [shell(rect(2.5, 16, 19, 5, rx)), shell(rect(4.5, 4.5, 14, 7, 3.5)),
            line(seg(7.5, 11.5, 7.5, 16)), line(seg(15.5, 11.5, 15.5, 16)),
            line(poly([(18.5, 8), (21.5, 8), (21.5, 3.5)], r=S.r * 0.5))]


@icon("book-chapter", CAT, "Open book with a large numeral 1 and a text line on the left page and text lines on the right.",
      tags=["chapter", "chapter one", "book", "heading", "novel", "section start", "reading"])
def _(S):
    return [shell(poly([(2.5, 4.5), (9, 4.5), (12, 6.5), (15, 4.5), (21.5, 4.5), (21.5, 19.5), (15, 19.5), (12, 21.5),
                        (9, 19.5), (2.5, 19.5)], closed=True, r=S.r)),
            detail(seg(12, 6.5, 12, 21.5)),
            detail(poly([(5.5, 10), (7.5, 8.5), (7.5, 13)])), detail(seg(5.5, 16, 9.5, 16)),
            detail(seg(14.5, 9, 18.5, 9)), detail(seg(14.5, 12.5, 18.5, 12.5)), detail(seg(14.5, 16, 18.5, 16))]


@icon("ghostwriter", CAT, "Small ghost holding a pen that writes a line.",
      tags=["ghostwriter", "ghost writer", "anonymous author", "ghost", "pen", "uncredited", "writing"])
def _(S):
    return [shell("M2.5 17V8.5A5.5 5.5 0 0 1 13.5 8.5V17L11 14.5L8 17L5 14.5Z".replace("L5 14.5Z", "L5 14.5Z")),
            dot(6, 9, 1.1), dot(10, 9, 1.1),
            line(seg(20.5, 3.5, 16.5, 11)), solid(poly([(14.5, 15), (15.5, 10.5), (18.5, 12)], closed=True)),
            line(seg(12.5, 21, 21.5, 21))]


@icon("digital-notepad", CAT, "Thin tablet with handwritten lines on its screen and a stylus resting on it.",
      tags=["tablet", "stylus", "handwriting", "note taking", "digital notes", "e-ink", "notepad"])
def _(S):
    return [shell(rect(2.5, 2.5, 13, 19, min(S.R, 3))),
            detail("M5.5 9C6.5 6.5 8 6.5 8.5 9S10.5 11.5 12.5 9"), detail(seg(5.5, 14, 12.5, 14)),
            line(seg(21, 4, 17, 12)), solid(poly([(15, 16), (16, 11), (19, 13)], closed=True))]


@icon("letter-stamps", CAT, "Two small rubber stamps with round handles and the letters T and A on their bases.",
      tags=["alphabet stamps", "rubber stamps", "letter stamp set", "stamping", "craft", "printing", "ink"])
def _(S):
    def stamp(cx):
        return [shell(rect(cx - 2, 2.5, 4, 4, min(S.R, 1.5))), line(seg(cx, 6.5, cx, 11.5)),
                shell(rect(cx - 3.5, 11.5, 7, 9, min(S.R, 1.5)))]
    return [*stamp(7), *stamp(17),
            detail(seg(5.5, 15, 8.5, 15)), detail(seg(7, 15, 7, 18)),
            detail(poly([(15.3, 18), (17, 14.5), (18.7, 18)]))]


@icon("calligraphy-guide-sheet", CAT, "Sheet crossed by horizontal ruled lines and evenly spaced slanted guide lines.",
      tags=["guide sheet", "practice sheet", "slant lines", "lettering", "handwriting", "ruled", "penmanship"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)),
            detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15)),
            detail(seg(11, 3, 6.5, 21)), detail(seg(17.5, 3, 13, 21))]


@icon("didone-font", CAT, "Capital A with a heavy right stroke, hairline left stroke and thin flat serifs.",
      tags=["didone", "modern serif", "high contrast", "fashion type", "stroke contrast", "serif"])
def _(S):
    return [shell(poly([(11.5, 4), (14.5, 4), (19, 19.5), (15.5, 19.5)], closed=True, r=S.r * 0.4)),
            solid(poly([(11.8, 4), (12.8, 4), (6.2, 19.5), (5.2, 19.5)], closed=True)),
            solid(rect(8, 13, 7, 1.2)),
            solid(rect(3, 19.6, 6.5, 1.2)), solid(rect(13, 19.6, 8.5, 1.2))]


@icon("seven-segment-digits", CAT, "Digital figure eight built from seven separate bars like a calculator display.",
      tags=["seven segment", "7 segment", "digital display", "lcd", "led digits", "calculator", "numerals"])
def _(S):
    return [line(seg(8, 3.5, 16, 3.5)), line(seg(8, 12, 16, 12)), line(seg(8, 20.5, 16, 20.5)),
            line(seg(5.5, 6, 5.5, 10)), line(seg(18.5, 6, 18.5, 10)),
            line(seg(5.5, 14, 5.5, 18)), line(seg(18.5, 14, 18.5, 18))]


# ============================================================================ letterforms and marks

@icon("letter-aperture", CAT, "Lowercase c with three dots marking the opening between its stroke ends.",
      tags=["aperture", "letter opening", "counter", "open counter", "c shape", "typeface anatomy", "legibility"])
def _(S):
    return [line(arc(10.5, 12, 7.5, 42, 318)), dot(20.5, 8, 1.1), dot(20.5, 12, 1.1), dot(20.5, 16, 1.1)]


@icon("side-bearings", CAT, "Letter n inside a glyph box with the empty strips at its left and right sides marked off.",
      tags=["sidebearing", "side bearing", "letter spacing", "glyph metrics", "kerning", "font design", "spacing"])
def _(S):
    return [shell(rect(2, 3, 20, 18, min(S.R, 2))),
            detail(seg(6, 3, 6, 21)), detail(seg(18, 3, 18, 21)),
            detail(seg(9.5, 9, 9.5, 17)), detail("M9.5 12A2.5 2.5 0 0 1 14.5 12V17")]


@icon("cjk-full-stop", CAT, "Two character marks followed by a small hollow circle at the baseline, the ideographic full stop.",
      tags=["ideographic full stop", "japanese period", "chinese period", "maru", "cjk punctuation", "kuten", "end of sentence"])
def _(S):
    h = 2.5 if S.name == "line" else 1.5
    return [line(seg(4.5 - h, 11.5, 4.5 + h, 11.5)), line(seg(4.5, 5, 4.5, 20)),
            line(rect(9.5, 7, 5, 12, 0 if S.name == "line" else 1)),
            shell(circle(19.5, 18.25, 2.25))]


@icon("eyebrow-heading", CAT, "Short line of small spaced text above a thick heading bar and two body lines.",
      tags=["eyebrow", "kicker", "overline", "heading", "label above title", "web design", "typographic hierarchy"])
def _(S):
    rx = 0 if S.name == "line" else 1.5
    return [line(seg(3, 4, 5.5, 4)), line(seg(8, 4, 10.5, 4)), line(seg(13, 4, 15.5, 4)),
            solid(rect(3, 8, 18, 4, rx)),
            line(seg(3, 16, 21, 16)), line(seg(3, 20.5, 14, 20.5))]


@icon("shape-poem", CAT, "Short lines of text growing wider row by row to form the outline of a tree.",
      tags=["concrete poetry", "calligram", "poem shape", "visual poetry", "text art", "tree", "typographic art"])
def _(S):
    return [line(seg(10.5, 3.5, 13.5, 3.5)), line(seg(8, 7.5, 16, 7.5)), line(seg(5.5, 11.5, 18.5, 11.5)),
            line(seg(3, 15.5, 21, 15.5)), line(seg(12, 18, 12, 21.5))]


@icon("palimpsest", CAT, "Page with bold lines of text written over dashed traces of older writing beneath.",
      tags=["palimpsest", "overwritten text", "manuscript", "erased text", "parchment", "old writing", "layers"])
def _(S):
    return [shell(poly([(4.5, 2.5), (14.5, 2.5), (19.5, 7.5), (19.5, 21.5), (4.5, 21.5)], closed=True, r=S.r)),
            detail(poly([(14.5, 2.5), (14.5, 7.5), (19.5, 7.5)], r=S.r * 0.5)),
            detail(seg(8, 11, 16, 11)),
            detail(seg(8, 15, 10, 15)), detail(seg(12, 15, 14, 15)),
            detail(seg(8, 19, 14, 19))]


@icon("underline-skip-ink", CAT, "Letters g and y with an underline that breaks where their tails cross it.",
      tags=["skip ink", "underline gap", "descenders", "text decoration", "css", "typography", "underline"])
def _(S):
    return [line(circle(6, 8, 3)), line("M9 5V17.5A2.5 2.5 0 0 1 6.5 20H5.5"),
            line(seg(14, 5, 17.3, 12.5)), line(seg(20.5, 5, 15, 20)),
            line(seg(2, 17.5, 6, 17.5)), line(seg(11.5, 17.5, 13.5, 17.5)), line(seg(19, 17.5, 22, 17.5))]


@icon("hook-above-accent", CAT, "Lowercase a with a small question mark shaped hook above it.",
      tags=["hook above", "vietnamese", "hoi", "diacritic", "accent mark", "tone mark", "a with hook"])
def _(S):
    return [line(circle(10.5, 16, 3.75)), line(seg(14.25, 12.5, 14.25, 19.5)),
            line("M9.5 5.5A2.25 2.25 0 1 1 12 7.5C11.5 7.8 11.5 8 11.5 8.5")]


@icon("typewriter-key", CAT, "Round typewriter key with a letter on its face, standing on a neck above a slanted lever arm.",
      tags=["typewriter", "key", "keycap", "typebar", "retro", "manual typewriter", "vintage"])
def _(S):
    return [shell(circle(12, 9, 7)),
            detail(poly([(8.5, 12.5), (12, 5), (15.5, 12.5)], r=S.r * 0.4)), detail(seg(10, 10.5, 14, 10.5)),
            line(poly([(4, 21.5), (12, 17), (20, 21.5)], r=S.r * 0.5)), line(seg(12, 16, 12, 17.5))]


@icon("proportion-wheel", CAT, "Two stacked round discs with a ring of scale marks between them and a small window at the middle.",
      tags=["proportion wheel", "scaling wheel", "crop calculator", "picture scaling", "layout tool", "dial", "paste-up"])
def _(S):
    marks = []
    for i in range(12):
        x, y = polar(12, 12, 7, i * 30)
        marks.append(dot(x, y, 0.9) if S.name != "line" else Part("dot", rect(x - 0.8, y - 0.8, 1.6, 1.6)))
    return [shell(circle(12, 12, 9.5)), detail(circle(12, 12, 4.5)), *marks, Part("dot", rect(10.75, 10.75, 2.5, 2.5))]


@icon("ornamental-rule", CAT, "Horizontal rule with a small diamond and two curling flourishes at its centre.",
      tags=["ornament", "fleuron", "divider", "flourish", "decorative rule", "section break", "dinkus"])
def _(S):
    return [line(seg(2, 12, 7.5, 12)), line(seg(16.5, 12, 22, 12)),
            shell(poly([(12, 9.5), (14.5, 12), (12, 14.5), (9.5, 12)], closed=True, r=S.r * 0.3)),
            line("M12 9C12 5 8.5 4.5 7.5 7"), line("M12 15C12 19 15.5 19.5 16.5 17")]


@icon("ai-writing-assistant", CAT, "Pen nib writing a line, with a four point sparkle beside it.",
      tags=["ai writing", "writing assistant", "generate text", "autocomplete", "copilot", "magic write", "sparkle"])
def _(S):
    f = axis((5, 18.5), -45)
    nib = [f(0, 0), f(6.5, -3.3), f(11.5, -3.3), f(11.5, 3.3), f(6.5, 3.3)]
    return [shell(poly(nib, closed=True, r=S.r * 0.5)), detail(poly([f(0.5, 0), f(5.5, 0)])),
            line(seg(3, 21.5, 11, 21.5)),
            solid(poly([(18, 2), (19.3, 4.7), (22, 6), (19.3, 7.3), (18, 10), (16.7, 7.3), (14, 6), (16.7, 4.7)], closed=True))]


# ============================================================================ paragraph and page layout

@icon("paragraph-shading", CAT, "Text lines above and below a hatched shaded band, shading behind a paragraph.",
      tags=["shading", "background colour", "paragraph shading", "highlight block", "text background", "fill"])
def _(S):
    return [line(seg(3, 3.5, 21, 3.5)),
            shell(rect(2.5, 7, 19, 10, min(S.R, 2))),
            detail(seg(8, 7, 5, 17)), detail(seg(14, 7, 11, 17)), detail(seg(20, 7, 17, 17)),
            line(seg(3, 20.5, 15, 20.5))]


@icon("paragraph-border", CAT, "Block of text lines enclosed by a thin rectangular outline.",
      tags=["paragraph border", "text box border", "boxed paragraph", "frame text", "outline", "callout"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, S.R)),
            detail(seg(7, 8, 17, 8)), detail(seg(7, 12, 17, 12)), detail(seg(7, 16, 13, 16))]


# ============================================================================ documents and notes

@icon("table-of-authorities", CAT, "Page with citation rows ending in page numbers and a small gavel at its lower corner.",
      tags=["table of authorities", "legal citations", "gavel", "legal brief", "case law", "index of cases", "law document"])
def _(S):
    f = axis((11.5, 21), -45)
    head = [f(5.5, -4), f(9, -4), f(9, 4), f(5.5, 4)]
    return [line(poly([(14.5, 9), (14.5, 6), (11.5, 3), (3.5, 3), (3.5, 21), (8, 21)], r=S.r * 0.5)),
            detail(poly([(11.5, 3), (11.5, 6), (14.5, 6)])),
            detail(seg(6.5, 9.5, 9, 9.5)), detail(seg(6.5, 13.5, 9, 13.5)), detail(seg(6.5, 17.5, 8.5, 17.5)),
            shell(poly(head, closed=True, r=S.r * 0.4)), line(seg(*f(0, 0), *f(5.5, 0)))]


@icon("handwritten-markup", CAT, "Page with text lines, a hand drawn loop around a word and an arrow leading out to the margin.",
      tags=["markup", "proofreading", "annotation", "circle word", "hand drawn", "editing marks", "review"])
def _(S):
    return [line(poly([(15, 2.5), (4.5, 2.5), (4.5, 21.5), (15, 21.5)], r=S.r * 0.5)),
            detail(seg(7.5, 6.5, 12.5, 6.5)), detail(seg(7.5, 17.5, 12.5, 17.5)),
            line("M7.5 12C7.5 9.5 12 9.5 12 12C12 14.5 7.5 14.5 7.5 12"),
            line(poly([(12.5, 12), (21, 12)])), line(chev(22, 12, 1, 2, S.r * 0.4))]


@icon("synchronized-scrolling", CAT, "Two narrow document pages with a pair of vertical arrows linking them.",
      tags=["synchronized scroll", "sync scroll", "side by side", "compare documents", "linked scrolling", "diff view", "lockstep"])
def _(S):
    return [shell(rect(2, 3, 6, 18, min(S.R, 1.5))), shell(rect(16, 3, 6, 18, min(S.R, 1.5))),
            line(seg(12, 6.5, 12, 17.5)), line(poly([(9.75, 8.75), (12, 6.5), (14.25, 8.75)], r=S.r * 0.5)),
            line(poly([(9.75, 15.25), (12, 17.5), (14.25, 15.25)], r=S.r * 0.5))]


@icon("synced-block", CAT, "Two content blocks stacked on the left with circular sync arrows on their right.",
      tags=["synced block", "linked block", "shared content", "reusable block", "sync", "notes app", "live copy"])
def _(S):
    return [shell(rect(2.5, 3, 11.5, 7, min(S.R, 1.5))), shell(rect(2.5, 14, 11.5, 7, min(S.R, 1.5))),
            *ring_arrow(18.5, 12, 3.2, 215, 340, 1.7), *ring_arrow(18.5, 12, 3.2, 35, 160, 1.7)]


@icon("master-page", CAT, "Page in front of a second page behind it, with the letter A on the front page.",
      tags=["master page", "parent page", "page template", "layout", "layers", "page layout"])
def _(S):
    return [line(poly([(7, 8), (7, 4), (20, 4), (20, 17), (16, 17)], r=S.r * 0.5)),
            shell(rect(3, 8, 13, 13, min(S.R, 2))),
            detail(poly([(6.5, 18.5), (9.5, 11.5), (12.5, 18.5)], r=S.r * 0.4)), detail(seg(7.8, 16, 11.2, 16))]


@icon("page-construction-canon", CAT, "Two facing pages each crossed by diagonal lines with a small text block at the crossing.",
      tags=["canon of page construction", "villard", "page layout", "book design", "margins", "diagonals", "golden canon"])
def _(S):
    return [shell(rect(2, 3, 9, 18, min(S.R, 1.5))), shell(rect(13, 3, 9, 18, min(S.R, 1.5))),
            detail(seg(2, 3, 11, 21)), detail(seg(11, 3, 2, 21)), detail(seg(13, 3, 22, 21)), detail(seg(22, 3, 13, 21)),
            Part("dot", rect(5, 9.5, 3, 5)), Part("dot", rect(16, 9.5, 3, 5))]


@icon("comic-sound-effect", CAT, "Jagged burst shape with a bold slanted letter inside.",
      tags=["onomatopoeia", "comic", "pow", "sound effect", "speech burst", "graphic novel", "action word"])
def _(S):
    pts = []
    for i in range(14):
        pts.append(polar(12, 12, 10.5 if i % 2 == 0 else 7.5, -90 + i * 360 / 14))

    def sk(x, y):
        return (x + (12 - y) * 0.2, y)
    a = [sk(7.5, 17), sk(11, 7), sk(14.5, 17)]
    return [shell(poly(pts, closed=True, r=S.r * 0.4)),
            detail(poly(a, r=S.r * 0.3)), detail(seg(*sk(8.8, 14.2), *sk(13.2, 14.2)))]


@icon("acronym", CAT, "Three stacked words whose first letters are drawn larger and bold in a column.",
      tags=["acronym", "initialism", "abbreviation", "first letters", "initials", "mnemonic", "spelled out"])
def _(S):
    rx = 0 if S.name == "line" else 1.2
    return [solid(rect(3, 3, 3.5, 5, rx)), line(seg(9, 5.5, 21, 5.5)),
            solid(rect(3, 9.5, 3.5, 5, rx)), line(seg(9, 12, 18, 12)),
            solid(rect(3, 16, 3.5, 5, rx)), line(seg(9, 18.5, 20, 18.5))]


@icon("replacement-character", CAT, "Diamond with a question mark inside, the symbol shown for an unreadable character.",
      tags=["unicode replacement", "unknown character", "encoding error", "mojibake", "unreadable text", "missing glyph", "fffd"])
def _(S):
    return [shell(poly([(12, 2), (22, 12), (12, 22), (2, 12)], closed=True, r=S.r * 1.2)),
            detail("M9.5 10A2.5 2.5 0 1 1 12 12.5C12 13.2 12 13.5 12 14"), dot(12, 17, 1.1)]


@icon("interlinear-translation", CAT, "Bold lines of text each with a dotted smaller line directly beneath it.",
      tags=["interlinear", "gloss", "line by line translation", "parallel lines", "bilingual", "language learning", "annotation"])
def _(S):
    def dots(y, n):
        return [dot(3.5 + 3 * i, y, 0.9) for i in range(n)]
    return [line(seg(3, 4.5, 21, 4.5)), *dots(9, 7), line(seg(3, 14.5, 17, 14.5)), *dots(19.5, 5)]


@icon("parallel-text", CAT, "Open book with the letter A on the left page and a Cyrillic letter on the right, each above a text line.",
      tags=["parallel text", "bilingual book", "dual language", "translation", "side by side text", "bitext", "reading"])
def _(S):
    return [shell(poly([(2.5, 4.5), (9, 4.5), (12, 6.5), (15, 4.5), (21.5, 4.5), (21.5, 19.5), (15, 19.5), (12, 21.5),
                        (9, 19.5), (2.5, 19.5)], closed=True, r=S.r)),
            detail(seg(12, 6.5, 12, 21.5)),
            detail(poly([(5.2, 13), (7.2, 8.5), (9.2, 13)], r=S.r * 0.3)),
            detail(poly([(14.8, 13), (14.8, 8.5), (19.2, 8.5), (19.2, 13)])),
            detail(seg(5.5, 16.5, 9.5, 16.5)), detail(seg(14.5, 16.5, 18.5, 16.5))]


@icon("scansion-marks", CAT, "Row of short syllable bars with alternating breve and stress marks above them.",
      tags=["scansion", "prosody", "metre", "meter", "stress marks", "poetry", "iambic"])
def _(S):
    h = 1.75 if S.name == "line" else 0.75
    out = []
    for i, cx in enumerate((3.5, 9, 14.5, 20)):
        out.append(line(seg(cx - h, 18, cx + h, 18)))
        if i % 2 == 0:
            out.append(line(f"M{cx - 1.5} 6.5C{cx - 1.5} 10.5 {cx + 1.5} 10.5 {cx + 1.5} 6.5"))
        else:
            out.append(line(seg(cx - 1.5, 10.5, cx + 1.5, 5.5)))
    return out


@icon("typewriter-typeball", CAT, "Sphere covered in raised character bumps with a clip at its top.",
      tags=["typeball", "type element", "golf ball typewriter", "print head", "typewriter", "retro office"])
def _(S):
    ds = [(8, 14), (12, 14), (16, 14), (10, 10.5), (14, 10.5), (10, 17.5), (14, 17.5)]
    rx = 0 if S.name == "line" else 2
    return [shell(circle(12, 14, 8)), shell(rect(9.5, 1.5, 5, 3.5, rx)), *[dot(x, y, 1.1) for x, y in ds]]


@icon("fluid-typography", CAT, "Small phone and wide monitor side by side, the monitor showing a larger letter A.",
      tags=["fluid type", "responsive typography", "clamp", "scalable text", "viewport units", "web design", "responsive text"])
def _(S):
    return [shell(rect(2, 8, 6, 12, min(S.R, 1.5))), Part("dot", rect(4.25, 13, 1.5, 2.5)),
            shell(rect(11, 4, 11, 10, min(S.R, 1.5))),
            detail(poly([(13.7, 11.5), (16.5, 6.5), (19.3, 11.5)], r=S.r * 0.3)),
            line(seg(16.5, 14, 16.5, 18.5)), line(seg(13, 19.5, 20, 19.5))]


@icon("code-ligature", CAT, "Equals sign and greater than sign above a merged double arrow, a programming ligature.",
      tags=["ligature", "programming font", "fat arrow", "code font", "arrow function", "monospace"])
def _(S):
    return [line(seg(3, 4, 9.5, 4)), line(seg(3, 8, 9.5, 8)), line(poly([(12.5, 3), (16.5, 6), (12.5, 9)], r=S.r * 0.5)),
            solid(poly([(9.5, 11.5), (14.5, 11.5), (12, 14)], closed=True)),
            line(seg(3, 16, 15, 16)), line(seg(3, 20, 15, 20)), line(poly([(14.5, 13.5), (20, 18), (14.5, 22.5)], r=S.r * 0.5))]


# ============================================================================ notes, links and marks

@icon("postscript-note", CAT, "Letter page with a signature scribble and a short extra line below led by two letter marks.",
      tags=["postscript", "ps", "p.s.", "afterthought", "letter", "signature", "note at the end"])
def _(S):
    rx = 0 if S.name == "line" else 1
    return [shell(poly([(4.5, 2.5), (19.5, 2.5), (19.5, 21.5), (4.5, 21.5)], closed=True, r=S.r)),
            detail(seg(8, 6.5, 16, 6.5)),
            detail("M8 12C9 8.5 10.5 8.5 11 12S12.5 15 13.5 11S15 9.5 16 11"),
            Part("dot", rect(8, 16, 2, 3, rx)), Part("dot", rect(11.5, 16, 2, 3, rx)), detail(seg(15.5, 17.5, 16.5, 17.5))]


@icon("spoiler-text", CAT, "Lines of text with a speckled hidden block covering part of the middle line.",
      tags=["spoiler", "hidden text", "redacted", "blur text", "reveal", "censored"])
def _(S):
    return [line(seg(3, 5, 21, 5)),
            line(seg(3, 12, 6.5, 12)), shell(rect(8.5, 8.5, 8, 7, min(S.R, 1.5))),
            dot(11, 11.5, 0.9), dot(14, 12.5, 0.9), dot(12.5, 14, 0.8), line(seg(18.5, 12, 21, 12)),
            line(seg(3, 19, 15, 19))]


@icon("backlinks", CAT, "Two note pages with a bent arrow running from the lower page back up to the upper one.",
      tags=["backlink", "linked mentions", "references back", "wiki links", "note linking", "bidirectional links", "knowledge base"])
def _(S):
    return [shell(rect(2.5, 2.5, 9, 10.5, min(S.R, 1.5))), shell(rect(12, 11, 9.5, 10.5, min(S.R, 1.5))),
            detail(seg(5.5, 6.5, 8.5, 6.5)), detail(seg(15, 15.5, 18.5, 15.5)),
            line(poly([(12, 18), (7, 18), (7, 15.5)], r=S.r * 0.5)), line(chev(7, 14.5, 0, 0))] if False else [
            shell(rect(2.5, 2.5, 9, 10.5, min(S.R, 1.5))), shell(rect(12, 11, 9.5, 10.5, min(S.R, 1.5))),
            detail(seg(5.5, 6.5, 8.5, 6.5)), detail(seg(15, 15.5, 18.5, 15.5)),
            line(poly([(12, 18.5), (7, 18.5), (7, 16)], r=S.r * 0.5)),
            solid(poly([(4.75, 16), (9.25, 16), (7, 13.75)], closed=True))]


@icon("diacritic-anchor", CAT, "Lowercase a with a small crosshair above it marking where an accent attaches.",
      tags=["anchor point", "mark attachment", "diacritic", "opentype", "glyph anchor", "font design", "accent position"])
def _(S):
    return [line(circle(10.5, 18, 2.9)), line(seg(13.4, 15.5, 13.4, 20.9)),
            line(circle(12, 7.5, 2.25)), line(seg(12, 1.5, 12, 3.5)),
            line(seg(5.5, 7.5, 7.5, 7.5)), line(seg(16.5, 7.5, 18.5, 7.5))]


@icon("horizontal-in-vertical-text", CAT, "Vertical column of character boxes with two small digits set side by side in the middle.",
      tags=["tate chu yoko", "vertical text", "upright digits", "cjk layout", "horizontal in vertical", "japanese typesetting", "rotated numbers"])
def _(S):
    rx = 0 if S.name == "line" else 1
    return [shell(rect(8.5, 2, 7, 5.5, rx)), shell(rect(8.5, 17, 7, 5, rx)),
            line(seg(8, 10.5, 8, 14.5)), line(ellipse(13.75, 12.5, 2, 2.5))]


@icon("erasing-shield", CAT, "Thin flat plate pierced with a round hole, a narrow slot and a square opening.",
      tags=["eraser shield", "erasing shield", "drafting", "correction tool", "stencil", "drawing aid", "templates"])
def _(S):
    return [shell(rect(2, 5, 20, 14, S.R)),
            detail(circle(7, 12, 1.75)), detail(seg(12, 9.5, 12, 14.5)), detail(rect(15.5, 10, 3.5, 4, 0))]
