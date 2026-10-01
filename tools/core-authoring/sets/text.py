"""TypeIcon Core: text & editor.

Letterforms are drawn from 2 px strokes (never font text) on a cap height of 4–20. Toolbar icons (bold,
italic, align, lists …) keep to whole-pixel stroke centres so they stay crisp at 16 px in editors. Text
lines use the rows y = 5 / 10 / 15 / 20.
"""
import math

from dsl import D, P, ST, U, arc, circle, detail, dot, ellipse, filled_region, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import LINE, fmt, polar

CAT = "text"
ROWS = (5, 10, 15, 20)


def _rows(spans):
    """Horizontal text lines: spans is a list of (x0, x1) per row in ROWS."""
    return [line(seg(x0, y, x1, y)) for (x0, x1), y in zip(spans, ROWS) if x1 > x0]


# ============================================================================ character formatting

@icon("bold", CAT, "Letter B; bold text formatting.", tags=["bold", "strong", "text", "format", "weight", "editor"])
def _(S):
    if S.name == "line":
        b = "M7 4H13A3 3 0 0 1 16 7V9A3 3 0 0 1 13 12H14A3 3 0 0 1 17 15V17A3 3 0 0 1 14 20H7Z"
    else:
        b = "M7 4H12A4 4 0 0 1 12 12H13A4 4 0 0 1 13 20H7Z"
    return [line(b), line(seg(7, 12, 12, 12))]


@icon("italic", CAT, "Slanted letter I; italic text formatting.", tags=["italic", "emphasis", "slant", "oblique", "text", "format"])
def _(S):
    return [line(seg(10, 4, 19, 4)), line(seg(5, 20, 14, 20)), line(seg(15, 4, 9, 20))]


@icon("underline", CAT, "Letter U over a line; underlined text.", tags=["underline", "underscore", "text", "format", "editor"])
def _(S):
    return [line("M7 3V11A5 5 0 0 0 17 11V3"), line(seg(5, 20, 19, 20))]


@icon("strikethrough", CAT, "Letter S struck through by a line; strikethrough text.",
      tags=["strikethrough", "strike", "crossed out", "delete", "text", "format"], aliases=["strike"])
def _(S):
    return [line("M16.8 6.6C16 5 14.3 4 12 4C9.3 4 7.3 5.5 7.3 7.7C7.3 8.6 7.6 9.3 8.2 10"),
            line("M15.9 14.2C16.5 14.8 16.8 15.5 16.8 16.4C16.8 18.5 14.8 20 12 20C9.5 20 7.6 19 6.9 17.4"),
            line(seg(4, 12, 20, 12))]


# ============================================================================ headings and blocks

@icon("heading", CAT, "Letter H; a heading or title style.", tags=["heading", "header", "title", "h", "text", "format"])
def _(S):
    return [line(seg(6, 4, 6, 20)), line(seg(18, 4, 18, 20)), line(seg(6, 12, 18, 12))]


def _h(S):
    return [line(seg(4, 4, 4, 20)), line(seg(11, 4, 11, 20)), line(seg(4, 12, 11, 12))]


@icon("heading-1", CAT, "H1; first-level heading.", tags=["heading 1", "h1", "title", "header", "text", "format"], aliases=["h1"])
def _(S):
    return [*_h(S), line(poly([(15.5, 12.5), (18.5, 10), (18.5, 20)], r=S.r * 0.5))]


@icon("heading-2", CAT, "H2; second-level heading.", tags=["heading 2", "h2", "subtitle", "header", "text", "format"], aliases=["h2"])
def _(S):
    return [*_h(S), line("M15 12.8C15 11.2 16.2 10 17.9 10C19.6 10 20.8 11.1 20.8 12.7C20.8 14.6 19 15.9 15 20H21",
                         stroke_miterlimit="2")]


@icon("heading-3", CAT, "H3; third-level heading.", tags=["heading 3", "h3", "subheading", "header", "text", "format"], aliases=["h3"])
def _(S):
    return [*_h(S), line("M15.2 11.4C15.7 10.5 16.7 10 17.9 10C19.5 10 20.6 11 20.6 12.4C20.6 13.9 19.4 14.8 17.6 14.8"
                         "C19.6 14.8 20.9 15.8 20.9 17.4C20.9 19 19.6 20 17.8 20C16.5 20 15.4 19.5 14.8 18.6")]


@icon("paragraph", CAT, "Block of text lines with an indented first line; a paragraph.",
      tags=["paragraph", "body text", "normal text", "block", "text", "format"])
def _(S):
    return _rows([(9, 21), (3, 21), (3, 21), (3, 14)])


def _quote_mark(S, cx, cy=15.0):
    body = circle(cx, cy, 3.25) if S.name != "line" else rect(cx - 3.25, cy - 3.25, 6.5, 6.5, 1.25)
    return [solid(body), line(f"M{fmt(cx - 3)} {fmt(cy)}V12.5C{fmt(cx - 3)} 9.2 {fmt(cx - 0.8)} 6.8 {fmt(cx + 2.5)} 6")]


@icon("quote", CAT, "Pair of opening quotation marks; a quotation.",
      tags=["quote", "quotation", "citation", "testimonial", "cite", "marks"], aliases=["quotation-marks"])
def _(S):
    return [*_quote_mark(S, 7), *_quote_mark(S, 17)]


@icon("blockquote", CAT, "Text lines beside a vertical bar; a block quotation.",
      tags=["blockquote", "block quote", "quotation", "indent", "cite", "text"])
def _(S):
    return [line(seg(4, 4, 4, 20)), *_rows([(9, 21), (9, 18), (9, 21), (9, 16)])]


@icon("code-inline", CAT, "Angle brackets on a rounded chip; inline code.",
      tags=["inline code", "code", "monospace", "snippet", "markdown", "developer"], aliases=["inline-code"])
def _(S):
    return [shell(rect(2, 6, 20, 12, min(S.R * 1.5, 6))),
            detail(poly([(9.5, 9), (6.5, 12), (9.5, 15)], r=S.r * 0.5)),
            detail(poly([(14.5, 9), (17.5, 12), (14.5, 15)], r=S.r * 0.5))]


@icon("code-block", CAT, "Angle brackets inside a square frame; a code block.",
      tags=["code block", "code", "snippet", "pre", "markdown", "developer"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)),
            detail(poly([(10, 8), (7, 12), (10, 16)], r=S.r * 0.5)),
            detail(poly([(14, 8), (17, 12), (14, 16)], r=S.r * 0.5))]


# ============================================================================ links

def _half_links(S, gap_end=10):
    k = 5 if S.name != "line" else 3
    if k == 5:
        left = f"M{gap_end} 7H8A5 5 0 0 0 8 17H{gap_end}"
        right = f"M{24 - gap_end} 7H16A5 5 0 0 1 16 17H{24 - gap_end}"
    else:
        left = f"M{gap_end} 7H6A3 3 0 0 0 3 10V14A3 3 0 0 0 6 17H{gap_end}"
        right = f"M{24 - gap_end} 7H18A3 3 0 0 1 21 10V14A3 3 0 0 1 18 17H{24 - gap_end}"
    return [line(left), line(right)]


@icon("link-2", CAT, "Two open links joined by a bar; insert a hyperlink.",
      tags=["link", "hyperlink", "url", "chain", "insert link", "href"])
def _(S):
    return [*_half_links(S), line(seg(8, 12, 16, 12))]


@icon("unlink", CAT, "Two separated link halves with break marks; remove a hyperlink.",
      tags=["unlink", "remove link", "broken link", "detach", "hyperlink", "url"])
def _(S):
    return [*_half_links(S, 9), line(seg(12, 2.5, 12, 6)), line(seg(12, 18, 12, 21.5))]


# ============================================================================ alignment

@icon("align-left", CAT, "Text lines aligned to the left edge.", tags=["align left", "left", "alignment", "flush left", "text", "paragraph"])
def _(S):
    return _rows([(3, 21), (3, 15), (3, 19), (3, 13)])


@icon("align-center", CAT, "Text lines centred on the middle.", tags=["align center", "centre", "center", "alignment", "text", "paragraph"])
def _(S):
    return _rows([(3, 21), (7, 17), (5, 19), (8, 16)])


@icon("align-right", CAT, "Text lines aligned to the right edge.", tags=["align right", "right", "alignment", "flush right", "text", "paragraph"])
def _(S):
    return _rows([(3, 21), (9, 21), (5, 21), (11, 21)])


@icon("align-justify", CAT, "Text lines filling the full width; justified text.",
      tags=["justify", "justified", "alignment", "full width", "text", "paragraph"], aliases=["justify"])
def _(S):
    return _rows([(3, 21), (3, 21), (3, 21), (3, 21)])


def _box(S, x, y, w, h):
    return shell(rect(x, y, w, h, min(S.R, 1.5)))


@icon("align-top", CAT, "Two blocks hanging from a top line; align to top.",
      tags=["align top", "top", "vertical align", "alignment", "layout", "position"])
def _(S):
    return [line(seg(3, 3, 21, 3)), _box(S, 5, 7, 5, 14), _box(S, 14, 7, 5, 8)]


@icon("align-middle", CAT, "Two blocks centred on a horizontal line; align to middle.",
      tags=["align middle", "middle", "vertical center", "alignment", "layout", "position"])
def _(S):
    return [_box(S, 5, 4, 5, 16), _box(S, 14, 8, 5, 8), line(seg(3, 12, 21, 12))]


@icon("align-bottom", CAT, "Two blocks standing on a bottom line; align to bottom.",
      tags=["align bottom", "bottom", "vertical align", "alignment", "layout", "position"])
def _(S):
    return [line(seg(3, 21, 21, 21)), _box(S, 5, 3, 5, 14), _box(S, 14, 9, 5, 8)]


@icon("indent", CAT, "Text lines with the middle rows pushed right by a chevron; increase indent.",
      tags=["indent", "increase indent", "tab", "nest", "text", "paragraph"])
def _(S):
    return [*_rows([(3, 21), (11, 21), (11, 21), (3, 21)]), line(poly([(3.5, 9.5), (6.5, 12.5), (3.5, 15.5)], r=S.r * 0.5))]


@icon("outdent", CAT, "Text lines with a chevron pointing back left; decrease indent.",
      tags=["outdent", "decrease indent", "unindent", "untab", "text", "paragraph"])
def _(S):
    return [*_rows([(3, 21), (11, 21), (11, 21), (3, 21)]), line(poly([(7, 9.5), (4, 12.5), (7, 15.5)], r=S.r * 0.5))]


# ============================================================================ letterform helpers

def _A(S, x0, top, x1, base, bar=None):
    """Capital A: two legs meeting at an apex, crossbar at `bar` (default two-thirds down)."""
    mid = (x0 + x1) / 2
    bar = top + (base - top) * 0.68 if bar is None else bar
    t = (bar - top) / (base - top)
    xl, xr = mid - 0.75 - t * (mid - 0.75 - x0), mid + 0.75 + t * (x1 - mid - 0.75)
    return [line(poly([(x0, base), (mid - 0.75, top), (mid + 0.75, top), (x1, base)], r=S.r * 0.5)), line(seg(xl, bar, xr, bar))]


def _a(S, cx, cy, rx, ry):
    """Single-storey lowercase a: an oval bowl with a stem on its right side."""
    return [line(ellipse(cx, cy, rx, ry)), line(seg(cx + rx, cy - ry, cx + rx, cy + ry))]


def _arrow_h(S, x0, x1, y, head=2.5, left=False, right=True):
    out = [line(seg(x0, y, x1, y))]
    if right:
        out.append(line(poly([(x1 - head, y - head), (x1, y), (x1 - head, y + head)], r=S.r * 0.5)))
    if left:
        out.append(line(poly([(x0 + head, y - head), (x0, y), (x0 + head, y + head)], r=S.r * 0.5)))
    return out


def _arrow_v(S, x, y0, y1, head=2.5, up=True, down=False):
    out = [line(seg(x, y0, x, y1))]
    if up:
        out.append(line(poly([(x - head, y0 + head), (x, y0), (x + head, y0 + head)], r=S.r * 0.5)))
    if down:
        out.append(line(poly([(x - head, y1 - head), (x, y1), (x + head, y1 - head)], r=S.r * 0.5)))
    return out


def _small_two(x, y):
    """Small numeral 2 (5 wide, 7.5 tall) with its top-left at (x, y)."""
    return line(f"M{fmt(x)} {fmt(y + 2.2)}C{fmt(x)} {fmt(y + 1)} {fmt(x + 1)} {fmt(y)} {fmt(x + 2.5)} {fmt(y)}"
                f"C{fmt(x + 4)} {fmt(y)} {fmt(x + 5)} {fmt(y + 1)} {fmt(x + 5)} {fmt(y + 2.3)}"
                f"C{fmt(x + 5)} {fmt(y + 3.8)} {fmt(x + 3.6)} {fmt(y + 4.8)} {fmt(x)} {fmt(y + 7.5)}H{fmt(x + 5)}",
                stroke_miterlimit="2")


# ============================================================================ type and case

@icon("text-size", CAT, "Large and small letter T; change the text size.",
      tags=["text size", "font size", "scale", "larger", "smaller", "type"], aliases=["font-size"])
def _(S):
    return [line(seg(3, 4, 15, 4)), line(seg(9, 4, 9, 20)), line(seg(13, 11, 21, 11)), line(seg(17, 11, 17, 20))]


@icon("font-family", CAT, "Letter A beside a drop-down chevron; choose a font.",
      tags=["font", "typeface", "font picker", "family", "type", "text"])
def _(S):
    return [*_A(S, 3, 4, 15, 20), line(poly([(17, 10.5), (19.25, 12.75), (21.5, 10.5)], r=S.r * 0.5))]


@icon("typography", CAT, "Letters A and g; type and typography settings.",
      tags=["typography", "type", "font", "typeface", "lettering", "text style"])
def _(S):
    return [*_A(S, 3, 4, 12, 17, bar=12.5),
            line(ellipse(17.25, 13.5, 3.25, 3.5)),
            line("M20.5 10V18.5C20.5 20.4 19.2 21.5 17.2 21.5C16 21.5 14.9 21 14.2 20.2")]


@icon("letter-case", CAT, "Capital A beside a small a; change letter case.",
      tags=["case", "change case", "capitalize", "upper lower", "text", "format"], aliases=["change-case"])
def _(S):
    return [*_A(S, 3, 4, 11, 20, bar=15), *_a(S, 17, 15.5, 3.5, 4.5)]


@icon("uppercase", CAT, "Capital A with an arrow pointing up; make text uppercase.",
      tags=["uppercase", "capitals", "all caps", "upper case", "text", "format"], aliases=["all-caps"])
def _(S):
    return [*_A(S, 3, 4, 13, 20, bar=15), *_arrow_v(S, 18.5, 4, 14, up=True)]


@icon("lowercase", CAT, "Small a with an arrow pointing down; make text lowercase.",
      tags=["lowercase", "small letters", "lower case", "minuscule", "text", "format"])
def _(S):
    return [*_a(S, 8, 14.5, 4.5, 5.5), *_arrow_v(S, 18.5, 9, 19, up=False, down=True)]


@icon("superscript", CAT, "Capital A with a small raised 2; superscript text.",
      tags=["superscript", "raised", "exponent", "power", "text", "format"])
def _(S):
    return [*_A(S, 3, 5, 13, 20, bar=15.5), _small_two(16, 3)]


@icon("subscript", CAT, "Capital A with a small lowered 2; subscript text.",
      tags=["subscript", "lowered", "index", "chemical", "text", "format"])
def _(S):
    return [*_A(S, 3, 4, 13, 19, bar=14.5), _small_two(16, 13)]


# ============================================================================ colour, cleanup, proofing

@icon("text-color", CAT, "Letter A over a solid colour bar; text colour.",
      tags=["text color", "font colour", "colour", "color", "foreground", "format"], aliases=["font-color"])
def _(S):
    return [*_A(S, 6, 3, 18, 15, bar=11), solid(rect(3, 18, 18, 3.5, 0 if S.name == "line" else 1.25))]


@icon("clear-formatting", CAT, "Letter T with a small cross; remove text formatting.",
      tags=["clear formatting", "remove format", "plain text", "reset", "text", "format"], aliases=["remove-formatting"])
def _(S):
    return [line(seg(3, 4, 15, 4)), line(seg(9, 4, 9, 20)), line(seg(14, 14, 20, 20)), line(seg(20, 14, 14, 20))]


@icon("spell-check", CAT, "Letter A with a check mark; check spelling.",
      tags=["spelling", "spell check", "proofread", "grammar", "correct", "text"], aliases=["spellcheck"])
def _(S):
    return [*_A(S, 3, 3, 12, 14, bar=10.5), line(poly([(12, 17), (15, 20), (21, 13)], r=S.r * 0.5))]


@icon("translate", CAT, "Latin A beside a Chinese character; translate text.",
      tags=["translate", "language", "translation", "localize", "i18n", "multilingual"])
def _(S):
    return [*_A(S, 3, 3, 11, 13, bar=10),
            line(seg(17, 11, 17, 13)), line(seg(13, 14, 21, 14)),
            line("M14.5 14C15.4 17.4 17.4 19.9 21 21"), line("M19.5 14C18.6 17.4 16.6 19.9 13 21")]


# ============================================================================ layout of text

@icon("text-wrap", CAT, "Text line that wraps back to the next line with an arrow.",
      tags=["wrap", "word wrap", "line break", "text flow", "reflow", "text"])
def _(S):
    return [line(seg(3, 4, 21, 4)),
            line("M3 11H16.5A3.5 3.5 0 0 1 16.5 18H12.5"),
            line(poly([(15, 15.5), (12.5, 18), (15, 20.5)], r=S.r * 0.5)),
            line(seg(3, 18, 8, 18))]


@icon("line-height", CAT, "Vertical double arrow beside text lines; line spacing.",
      tags=["line height", "line spacing", "leading", "spacing", "text", "paragraph"], aliases=["line-spacing"])
def _(S):
    return [*_arrow_v(S, 5, 3, 21, up=True, down=True),
            line(seg(10, 6, 21, 6)), line(seg(10, 12, 21, 12)), line(seg(10, 18, 21, 18))]


@icon("letter-spacing", CAT, "Letter A between two bars over a double arrow; letter spacing.",
      tags=["letter spacing", "tracking", "kerning", "character spacing", "text", "type"])
def _(S):
    return [line(seg(3, 3, 3, 14)), line(seg(21, 3, 21, 14)), *_A(S, 7, 3, 17, 14, bar=10.5),
            *_arrow_h(S, 3, 21, 19, left=True, right=True)]


def _pilcrow(S):
    return [shell("M11 4H9.5C7.6 4 6 5.4 6 7.25C6 9.1 7.6 10.5 9.5 10.5H11Z"),
            line(poly([(11, 14), (11, 4), (17, 4)], r=S.r * 0.5)), line(seg(15, 4, 15, 14))]


@icon("text-direction-ltr", CAT, "Paragraph mark over a right-pointing arrow; left-to-right text.",
      tags=["left to right", "ltr", "text direction", "writing direction", "paragraph", "bidi"], aliases=["ltr"])
def _(S):
    return [*_pilcrow(S), *_arrow_h(S, 3, 21, 18.5, right=True)]


@icon("text-direction-rtl", CAT, "Paragraph mark over a left-pointing arrow; right-to-left text.",
      tags=["right to left", "rtl", "text direction", "arabic", "hebrew", "bidi"], aliases=["rtl"])
def _(S):
    return [*_pilcrow(S), *_arrow_h(S, 3, 21, 18.5, left=True, right=False)]


@icon("columns-text", CAT, "Text set in two columns.",
      tags=["columns", "two columns", "newspaper", "layout", "text", "multi-column"], aliases=["text-columns"])
def _(S):
    return [*_rows([(3, 10), (3, 10), (3, 10), (3, 8)]), *_rows([(14, 21), (14, 21), (14, 21), (14, 18)])]


@icon("horizontal-rule", CAT, "Full-width rule between lines of words; insert a horizontal rule.",
      tags=["horizontal rule", "hr", "divider", "separator", "line", "break"], aliases=["horizontal-line"])
def _(S):
    return [line(seg(3, 4, 10, 4)), line(seg(13, 4, 21, 4)),
            line(seg(3, 12, 21, 12)),
            line(seg(3, 20, 7, 20)), line(seg(10, 20, 21, 20))]


# ============================================================================ insert (object + plus in the top-right corner)

def _plus_segs(cx=18.0, cy=6.0):
    return [seg(cx - 3, cy, cx + 3, cy), seg(cx, cy - 3, cx, cy + 3)]


def _plus_filled(base_parts, cut=None, c=(18.0, 6.0)):
    """Filled: the object's solid design cut clear of the plus, then a heavy plus.
    `cut` is an explicit region (x0, y1) = everything right of x0 and above y1; default follows the plus shape."""
    body = filled_region(base_parts)
    if cut is None:
        gap = U(*(ST(d, 7.0, "round", "round") for d in _plus_segs(*c)))
    else:
        x0, y1 = cut
        gap = P(rect(x0, -2, 28 - x0, y1 + 2, 0))
    return U(D(body, gap), *(ST(d, 2.5, "butt") for d in _plus_segs(*c)))


def _cut_frame(S):
    """18 x 18 frame with its top-right corner left open for the plus."""
    return line(poly([(11, 3), (3, 3), (3, 21), (21, 21), (21, 13)], r=S.R))


@icon("table-insert", CAT, "Table whose top-right cell holds a plus; insert a table.",
      tags=["insert table", "add table", "table", "grid", "spreadsheet", "cells"], aliases=["insert-table", "table-plus"],
      filled=lambda: _plus_filled([shell(rect(3, 3, 18, 18, LINE.R)), detail(seg(10, 3, 10, 21)), detail(seg(3, 14, 21, 14))],
                                  cut=(10, 13), c=(17, 7)))
def _(S):
    return [line(poly([(21, 14), (21, 21), (3, 21), (3, 3), (11 if S.name == "line" else 10, 3)], r=S.R)),
            line(seg(10, 3, 10, 21)), line(seg(3, 14, 21, 14)),
            *(line(d) for d in _plus_segs(17, 7))]


MOUNTAINS = [(3, 17), (8.5, 11.5), (13, 16), (16, 13), (21, 17)]


@icon("image-insert", CAT, "Picture frame with a plus in its corner; insert an image.",
      tags=["insert image", "add image", "picture", "photo", "media", "upload"], aliases=["insert-image", "image-plus"],
      filled=lambda: _plus_filled([shell(rect(3, 3, 18, 18, LINE.R)), detail(poly(MOUNTAINS)), dot(8, 7.5, 1.75)], cut=(12, 12)))
def _(S):
    return [_cut_frame(S), line(poly(MOUNTAINS, r=S.r)), dot(8, 7.5, 1.75), *(line(d) for d in _plus_segs())]


def _arc_clear(cx, cy, r, clearance=4.0):
    """Longest arc of the circle that keeps `clearance` (centre-line distance) from the plus strokes."""
    def dist(px, py, a, b):
        (ax, ay), (bx, by) = a, b
        t = max(0, min(1, ((px - ax) * (bx - ax) + (py - ay) * (by - ay)) / ((bx - ax) ** 2 + (by - ay) ** 2)))
        return math.hypot(px - ax - t * (bx - ax), py - ay - t * (by - ay))
    segs = [((15, 6), (21, 6)), ((18, 3), (18, 9))]
    ok = [min(dist(*polar(cx, cy, r, a), *sg) for sg in segs) >= clearance for a in range(360)]
    best, start = (0, 0), None
    for i in range(720):
        if ok[i % 360]:
            start = i if start is None else start
            if i - start + 1 > best[1] - best[0] and i - start < 360:
                best = (start, i + 1)
        else:
            start = None
    return arc(cx, cy, r, best[0], best[1] - 1)


def _face(cx=11, cy=13):
    return [dot(cx - 3, cy - 2, 1.4), dot(cx + 3, cy - 2, 1.4),
            f"M{fmt(cx - 3.5)} {fmt(cy + 2)}C{fmt(cx - 2.6)} {fmt(cy + 3.6)} {fmt(cx - 1.4)} {fmt(cy + 4.4)} {fmt(cx)} {fmt(cy + 4.4)}"
            f"C{fmt(cx + 1.4)} {fmt(cy + 4.4)} {fmt(cx + 2.6)} {fmt(cy + 3.6)} {fmt(cx + 3.5)} {fmt(cy + 2)}"]


@icon("emoji-insert", CAT, "Smiling face with a plus in its corner; insert an emoji.",
      tags=["insert emoji", "emoji", "smiley", "emoticon", "reaction", "add emoji"], aliases=["insert-emoji"],
      filled=lambda: _plus_filled([shell(circle(11, 13, 8.5)), *_face()[:2], detail(_face()[2])]))
def _(S):
    f = _face()
    return [line(_arc_clear(11, 13, 8.5)), f[0], f[1], line(f[2]), *(line(d) for d in _plus_segs())]


# ============================================================================ mentions, tags, markup

def _at(cx, cy, r_in, r_out):
    """@ sign: inner ring, stem down its right side, outer arc wrapping round to the lower right."""
    x = cx + r_in
    tail = (cx + r_out * math.cos(math.radians(50)), cy + r_out * math.sin(math.radians(50)))
    k = (r_out - r_in) / 2
    return [circle(cx, cy, r_in),
            f"M{fmt(x)} {fmt(cy - r_in)}V{fmt(cy + 1)}C{fmt(x)} {fmt(cy + 1 + k)} {fmt(x + k * 0.6)} {fmt(cy + 1 + k * 1.4)} "
            f"{fmt(x + k)} {fmt(cy + 1 + k * 1.4)}C{fmt(cx + r_out - 0.2)} {fmt(cy + 1 + k * 1.4)} {fmt(cx + r_out)} {fmt(cy + 1)} {fmt(cx + r_out)} {fmt(cy)}"
            f"A{fmt(r_out)} {fmt(r_out)} 0 1 0 {fmt(tail[0])} {fmt(tail[1])}"]


@icon("at-sign", CAT, "The @ sign; addresses and handles.", tags=["at", "at sign", "email", "handle", "address", "arroba"],
      aliases=["arroba"])
def _(S):
    ring, rest = _at(12, 12, 3.5, 9)
    return [line(ring), line(rest)]


_BUBBLE = [(3, 4), (21, 4), (21, 17), (11.5, 17), (7, 21), (7, 17), (3, 17)]


@icon("mention", CAT, "Letter a inside a round speech bubble; mention someone with @.",
      tags=["mention", "at", "tag someone", "handle", "notify", "comment"])
def _(S):
    p1, p2 = polar(12, 11.5, 9, 150), polar(12, 11.5, 9, 112)
    tip = (3.5, 20.5) if S.name == "line" else (4, 20)
    bubble = (f"M{fmt(p2[0])} {fmt(p2[1])}A9 9 0 1 0 {fmt(p1[0])} {fmt(p1[1])}L{fmt(tip[0])} {fmt(tip[1])}Z")
    return [shell(bubble, stroke_miterlimit="8"), detail(circle(11, 11.5, 2.75)),
            detail("M13.75 8.75V13.3C13.75 14.5 14.5 15.2 15.4 15.2C16.4 15.2 17 14.4 17 13.3")]


@icon("hashtag", CAT, "Speech bubble holding a # sign; a hashtag or topic.",
      tags=["hashtag", "hash", "topic", "tag", "trending", "social"])
def _(S):
    return [shell(poly(_BUBBLE, closed=True, r=S.r * 1.3)),
            detail(seg(10.5, 7, 9.5, 14)), detail(seg(14.5, 7, 13.5, 14)), detail(seg(7.5, 9, 16.5, 9)), detail(seg(7.5, 12.5, 16.5, 12.5))]


@icon("markdown", CAT, "Letter M and a down arrow in a rounded box; Markdown.",
      tags=["markdown", "md", "markup", "formatting", "readme", "text"])
def _(S):
    return [shell(rect(2, 5, 20, 14, min(S.R, 3))),
            detail(poly([(6, 15.5), (6, 8.5), (9, 12), (12, 8.5), (12, 15.5)], r=S.r * 0.5)),
            detail(seg(17, 8.5, 17, 15)), detail(poly([(14.5, 12.5), (17, 15), (19.5, 12.5)], r=S.r * 0.5))]


@icon("word-count", CAT, "Text lines above the numerals 1 2 3; count words.",
      tags=["word count", "count", "statistics", "characters", "length", "text"])
def _(S):
    three = ("M16 14C16.4 13.4 17.2 13 18.2 13C19.5 13 20.5 13.8 20.5 14.9C20.5 16 19.6 16.7 18.3 16.7"
             "C19.7 16.7 20.8 17.4 20.8 18.6C20.8 19.8 19.7 20.5 18.3 20.5C17.3 20.5 16.4 20.1 15.9 19.4")
    return [line(seg(3, 4, 21, 4)), line(seg(3, 9, 15, 9)),
            line(poly([(3.5, 14.5), (5.5, 13), (5.5, 20.5)], r=S.r * 0.5)), _small_two(8.75, 13), line(three)]


@icon("text-recognition", CAT, "Letter T inside scanning corners; recognise text (OCR).",
      tags=["ocr", "text recognition", "scan text", "extract text", "optical", "read"], aliases=["ocr"])
def _(S):
    c = [poly([(3, 8), (3, 3), (8, 3)], r=S.r), poly([(16, 3), (21, 3), (21, 8)], r=S.r),
         poly([(21, 16), (21, 21), (16, 21)], r=S.r), poly([(8, 21), (3, 21), (3, 16)], r=S.r)]
    return [*(line(d) for d in c), line(seg(8, 8, 16, 8)), line(seg(12, 8, 12, 16))]


# ============================================================================ pens (tip at the lower left, 45°)

def _axis(origin, deg=-45.0):
    """Map local (u along the pen towards its back end, v across it) to grid coordinates."""
    ox, oy = origin
    c, s_ = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return lambda u, v: (ox + u * c - v * s_, oy + u * s_ + v * c)


@icon("highlighter", CAT, "Highlighter with a slanted chisel tip over a highlighted line.",
      tags=["highlighter", "highlight", "marker", "emphasis", "annotate", "text"], aliases=["highlight"])
def _(S):
    m = _axis((5.5, 15.5))
    body = [m(0, -2.5), m(4, -2.5), m(4, -3.75), m(15, -3.75), m(15, 3.75), m(4, 3.75), m(4, 2.5), m(2, 2.5)]
    return [shell(poly(body, closed=True, r=S.r * 0.5)), detail(seg(*m(7, -3.75), *m(7, 3.75))),
            line(seg(3, 21, 11, 21))]


@icon("marker-pen", CAT, "Felt-tip marker with a rounded nib and cap band.",
      tags=["marker", "felt tip", "sharpie", "pen", "draw", "annotate"], aliases=["felt-pen"])
def _(S):
    m = _axis((3.5, 20.5))
    a, b = m(4, -2), m(4, 2)
    nib = (f"M{fmt(a[0])} {fmt(a[1])}L{fmt(m(1.5, -1.25)[0])} {fmt(m(1.5, -1.25)[1])}"
           f"A1.25 1.25 0 0 0 {fmt(m(1.5, 1.25)[0])} {fmt(m(1.5, 1.25)[1])}L{fmt(b[0])} {fmt(b[1])}Z")
    body = [m(4, -3.5), m(19, -3.5), m(19, 3.5), m(4, 3.5)]
    return [shell(nib), shell(poly(body, closed=True, r=S.r)), detail(seg(*m(9, -3.5), *m(9, 3.5)))]


@icon("fountain-pen", CAT, "Fountain-pen nib with a breather hole and slit; pen tool.",
      tags=["fountain pen", "nib", "pen tool", "calligraphy", "vector", "write"], aliases=["pen-nib"])
def _(S):
    nib = [(8, 3), (16, 3), (16, 7.5), (18.5, 12.5), (12, 21), (5.5, 12.5), (8, 7.5)]
    return [shell(poly(nib, closed=True, r=S.r * 0.66)), detail(seg(8, 7.5, 16, 7.5)),
            dot(12, 12.5, 1.6), detail(seg(12, 14.5, 12, 19))]


@icon("ink-pen", CAT, "Fountain pen writing with its nib; handwriting in ink.",
      tags=["ink pen", "fountain pen", "write", "handwriting", "sign", "letter"], aliases=["writing-pen"])
def _(S):
    m = _axis((3.5, 20.5))
    nib = [m(0, 0), m(6, -3), m(6, 3)]
    body = [m(6, -3), m(16.5, -3), m(19.5, 0), m(16.5, 3), m(6, 3)]
    if S.name != "line":
        body = [m(6, -3), m(16.5, -3), m(18.5, -1.2), m(18.5, 1.2), m(16.5, 3), m(6, 3)]
    return [shell(poly(nib, closed=True, r=S.r * 0.4)), shell(poly(body, closed=True, r=S.r * 0.66)),
            detail(seg(*m(10, -3), *m(10, 3)))]


def _quill_vane(m):
    pts = []
    for i in range(13):
        u = 5 + 16 * i / 12
        pts.append(m(u, -4.5 * math.sin(math.pi * i / 12) ** 0.8))
    for i in range(12, -1, -1):
        u = 5 + 16 * i / 12
        pts.append(m(u, 2.5 * math.sin(math.pi * i / 12) ** 0.9))
    return pts


@icon("quill", CAT, "Feather quill pen; writing by hand.",
      tags=["quill", "feather", "writing", "poetry", "author", "calligraphy"], aliases=["feather-pen"])
def _(S):
    m = _axis((3, 21))
    return [shell(poly(_quill_vane(m), closed=True)),
            line(seg(*m(0, 0), *m(5, 0))), detail(seg(*m(5, 0), *m(17, 0))),
            detail(seg(*m(11, 0), *m(14.5, -3.4)))]


@icon("signature-pen", CAT, "Pen finishing a handwritten signature.",
      tags=["signature", "sign", "autograph", "e-sign", "approve", "contract"], aliases=["sign-here"])
def _(S):
    m = _axis((11.5, 14.5))
    pen = [m(0, 0), m(4, -2.5), m(12, -2.5), m(12, 2.5), m(4, 2.5)]
    return [shell(poly(pen, closed=True, r=S.r * 0.5)), detail(seg(*m(4, -2.5), *m(4, 2.5))),
            line("M3 19C4.5 15.5 6.5 14 7.5 15C8.5 16 6.5 20 7.8 20.5C9 21 10 17 11 16.8C12 16.6 11.5 19.5 13 19.5C14 19.5 15 18.8 16 18.5H21")]
