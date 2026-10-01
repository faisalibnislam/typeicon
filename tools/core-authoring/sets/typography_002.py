"""TypeIcon Core: typography, part 2 (layout, lists, tables, proofing marks, punctuation).

Text lines sit on 2 px strokes; glyphs are drawn from 2 px skeletons, never from font text.
Inside a shell, text lines are `detail` (knocked out in Filled); outside they are `line`.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt

CAT = "typography"


def tl(x0, y0, x1, y1=None, inside=False):
    """Text line (inside a shell: detail)."""
    y1 = y0 if y1 is None else y1
    f = detail if inside else line
    return f(seg(x0, y0, x1, y1))


def rows(spans, ys, inside=False):
    return [tl(x0, y, x1, inside=inside) for (x0, x1), y in zip(spans, ys)]


def head(S, tip, direction, size=2.5, inside=False):
    """Arrowhead chevron at tip; direction in degrees (0 = pointing right)."""
    a = math.radians(direction)
    pts = []
    for off in (150, -150):
        b = a + math.radians(off)
        pts.append((tip[0] + size * 1.2 * math.cos(b), tip[1] + size * 1.2 * math.sin(b)))
    f = detail if inside else line
    return f(poly([pts[0], tip, pts[1]], r=S.r * 0.5))


def arrow(S, p0, p1, both=False, size=2.2, inside=False):
    ang = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
    f = detail if inside else line
    out = [f(seg(*p0, *p1)), head(S, p1, ang, size, inside)]
    if both:
        out.append(head(S, p0, ang + 180, size, inside))
    return out


def dashes(p0, p1, dash=3.0, gap=2.0, inside=False):
    """Dashed straight stroke from p0 to p1 as separate segments."""
    f = detail if inside else line
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
    n = max(1, round((L + gap) / (dash + gap)))
    d = (L - gap * (n - 1)) / n
    out, t = [], 0.0
    for _ in range(n):
        out.append(f(seg(p0[0] + ux * t, p0[1] + uy * t, p0[0] + ux * (t + d), p0[1] + uy * (t + d))))
        t += d + gap
    return out


def sq(x, y, w, h, rx=0.0):
    return Part("dot", rect(x, y, w, h, rx))


def glyph_T(x, y, w, h, inside=False):
    f = detail if inside else line
    return [f(seg(x, y, x + w, y)), f(seg(x + w / 2, y, x + w / 2, y + h))]


def glyph_A(S, x0, top, x1, base, bar=None, inside=False):
    f = detail if inside else line
    mid = (x0 + x1) / 2
    bar = top + (base - top) * 0.68 if bar is None else bar
    t = (bar - top) / (base - top)
    xl, xr = mid - 0.75 - t * (mid - 0.75 - x0), mid + 0.75 + t * (x1 - mid - 0.75)
    return [f(poly([(x0, base), (mid - 0.75, top), (mid + 0.75, top), (x1, base)], r=S.r * 0.5)), f(seg(xl, bar, xr, bar))]


def page(S, x=4, y=2, w=16, h=20, rx=None):
    return shell(rect(x, y, w, h, S.R if rx is None else rx))


# ============================================================================ text flow and alignment

@icon("space-symbol", CAT, "Open box mark that shows a typed space character.",
      tags=["space", "whitespace", "blank", "visible space", "spacebar", "invisible characters"])
def _(S):
    return [line(poly([(3.5, 8.5), (3.5, 15.5), (20.5, 15.5), (20.5, 8.5)], r=S.r))]


@icon("decimal-tab", CAT, "Numbers of different lengths lined up on a dashed decimal point line.",
      tags=["decimal tab", "tab stop", "align decimals", "numbers", "column", "tab"])
def _(S):
    return [*dashes((12, 2.5), (12, 21.5), 4, 2.5),
            *rows([(3, 9), (6, 9), (4.5, 9)], [5.5, 12, 18.5]),
            *rows([(15, 19), (15, 21), (15, 18)], [5.5, 12, 18.5])]


@icon("justify-all-lines", CAT, "Justified text with the short last line stretched out by outward arrows.",
      tags=["justify all lines", "force justify", "full justify", "stretch last line", "alignment", "text"])
def _(S):
    return [*rows([(3, 21)] * 3, [4, 9, 14]),
            line(seg(3, 19.5, 8.5, 19.5)), head(S, (3, 19.5), 180), line(seg(15.5, 19.5, 21, 19.5)), head(S, (21, 19.5), 0)]


@icon("vertical-justification", CAT, "Text frame with lines spread evenly top to bottom and a double arrow beside it.",
      tags=["vertical justify", "distribute lines", "vertical alignment", "text frame", "spread lines", "justify vertically"])
def _(S):
    return [shell(rect(3, 3, 13, 18, S.R)), *rows([(6, 13)] * 3, [7, 12, 17], inside=True),
            *arrow(S, (20, 3), (20, 21), both=True)]


@icon("align-to-spine", CAT, "Open book whose text lines on both pages sit against the centre fold.",
      tags=["align to spine", "inside margin", "gutter", "book layout", "facing pages", "binding side"])
def _(S):
    return [shell(poly([(2.5, 5), (12, 7), (21.5, 5), (21.5, 19), (12, 21), (2.5, 19)], closed=True, r=S.r)),
            detail(seg(12, 7, 12, 21)),
            *rows([(5.5, 9), (7, 9)], [11, 15], inside=True), *rows([(15, 18.5), (15, 17)], [11, 15], inside=True)]


@icon("widows-and-orphans", CAT, "Two pages where a lone short line starts the second page.",
      tags=["widow", "orphan", "stray line", "page break", "typesetting", "paragraph control"])
def _(S):
    return [shell(rect(2, 3, 9.5, 18, S.R)), shell(rect(12.5, 3, 9.5, 18, S.R)),
            *rows([(5, 8.5)] * 3, [8, 12, 16], inside=True), tl(15.5, 7, 19, inside=True)]


@icon("keep-with-next", CAT, "Heading bar and text lines tied together by a chain link.",
      tags=["keep with next", "heading stays with paragraph", "keep together", "chain", "pagination", "link"])
def _(S):
    return [solid(rect(3, 3, 11, 4, 1 if S.name == "rounded" else 0)),
            *rows([(3, 14), (3, 14), (3, 10)], [12, 16.5, 21]),
            line("M17.5 10.5V6.5a2.5 2.5 0 0 1 5 0V10.5"), line("M17.5 13.5V17.5a2.5 2.5 0 0 0 5 0V13.5")]


@icon("keep-lines-together", CAT, "Paragraph lines held as one block by a bracket at its side.",
      tags=["keep lines together", "no page break inside", "paragraph control", "bracket", "group lines", "pagination"])
def _(S):
    return [line(poly([(7, 3), (3.5, 3), (3.5, 21), (7, 21)], r=S.r * 0.5)),
            *rows([(11, 21), (11, 21), (11, 21), (11, 17)], [4.5, 9.5, 14.5, 19.5])]


@icon("line-length", CAT, "Text lines with a horizontal dimension arrow under one full line.",
      tags=["line length", "measure", "characters per line", "column width", "dimension", "readability"])
def _(S):
    return [*rows([(3, 21), (3, 21), (3, 16)], [4, 9, 14]), *arrow(S, (3, 20), (21, 20), both=True)]


@icon("text-rivers", CAT, "Justified paragraph with a wavy gap running down through the word spaces.",
      tags=["rivers", "white space channel", "word gaps", "justified text problem", "typography", "river"])
def _(S):
    g = [8, 14, 9, 15]
    return [x for y, gx in zip([4.5, 9.5, 14.5, 19.5], g) for x in (tl(3, y, gx - 2), tl(gx + 2, y, 21))]


@icon("text-frame", CAT, "Dashed frame with corner handles and a capital T inside.",
      tags=["text frame", "text box", "text container", "frame", "type tool", "layout"])
def _(S):
    return [*dashes((9, 5), (15, 5), 2.5, 1.5), *dashes((9, 19), (15, 19), 2.5, 1.5),
            *dashes((5, 9), (5, 15), 2.5, 1.5), *dashes((19, 9), (19, 15), 2.5, 1.5),
            sq(3, 3, 4, 4), sq(17, 3, 4, 4), sq(3, 17, 4, 4), sq(17, 17, 4, 4),
            *glyph_T(9, 9, 6, 6)]


@icon("threaded-text-frames", CAT, "Two text boxes joined by a curved arrow so text flows from one to the next.",
      tags=["threaded text", "linked frames", "text flow", "story", "continue text", "overflow"])
def _(S):
    return [shell(rect(2.5, 2.5, 11, 8, S.R)), shell(rect(10.5, 13.5, 11, 8, S.R)),
            tl(5.5, 6.5, 10.5, inside=True), tl(13.5, 17.5, 18.5, inside=True),
            line("M13.5 6.5H18a1 1 0 0 1 1 1V11"), head(S, (19, 12.5), 90, 2)]


@icon("overset-text", CAT, "Full text box with a small plus marker at its corner for hidden extra text.",
      tags=["overset", "overflow text", "hidden text", "text overflow", "red plus", "layout"])
def _(S):
    return [shell(rect(2.5, 2.5, 14, 14, S.R)), *rows([(5.5, 13.5)] * 3, [6.5, 10, 13.5], inside=True),
            line(seg(14.5, 19.5, 21.5, 19.5)), line(seg(18, 16, 18, 23))]


@icon("shrink-text-to-fit", CAT, "Narrow text box holding a capital A with arrows pressing in from both sides.",
      tags=["shrink to fit", "fit text", "autofit", "scale text down", "resize text", "text box"])
def _(S):
    return [shell(rect(6.5, 3, 11, 18, S.R)), *glyph_A(S, 9.5, 8.5, 14.5, 15.5, bar=13, inside=True),
            line(poly([(1.5, 9), (4, 12), (1.5, 15)], r=S.r * 0.5)), line(poly([(22.5, 9), (20, 12), (22.5, 15)], r=S.r * 0.5))]


# ============================================================================ columns, pages and wrapping

def la(cx, cy, r=3.0, inside=False):
    """Small single-storey a: bowl plus a stem on its right."""
    f = detail if inside else line
    return [f(circle(cx, cy, r)), f(seg(cx + r, cy - r, cx + r, cy + r))]


def lb(cx, cy, r=3.0, inside=False):
    """Small b: bowl plus a tall stem on its left."""
    f = detail if inside else line
    return [f(circle(cx, cy, r)), f(seg(cx - r, cy - r - 1.6, cx - r, cy + r))]


def lc(cx, cy, r=3.0, inside=False):
    f = detail if inside else line
    return f(arc(cx, cy, r, 40, 320))


@icon("span-columns", CAT, "Wide heading bar spanning two columns of text lines below it.",
      tags=["span columns", "span all columns", "column span", "heading across columns", "multi column", "layout"])
def _(S):
    return [solid(rect(3, 3, 18, 4, 1 if S.name == "rounded" else 0)),
            *rows([(3, 10), (3, 10), (3, 8)], [11.5, 16, 20.5]), *rows([(14, 21), (14, 21), (14, 19)], [11.5, 16, 20.5])]


@icon("column-break", CAT, "Two text columns where the first stops early at a dashed break line.",
      tags=["column break", "break column", "next column", "multi column", "layout", "flow"])
def _(S):
    return [*rows([(3, 10), (3, 10)], [4.5, 9.5]), *dashes((3, 15), (10, 15), 2.5, 1.5),
            *rows([(14, 21)] * 3 + [(14, 18)], [4.5, 9.5, 14.5, 19.5])]


@icon("page-border", CAT, "Page outline with a second decorative frame inside its edge.",
      tags=["page border", "frame", "decorative border", "certificate", "page frame", "document"])
def _(S):
    return [shell(rect(3, 2, 18, 20, S.R)), detail(rect(7, 6, 10, 12, min(S.R, 3))), *rows([(9.5, 14.5), (9.5, 14.5)], [10, 14], inside=True)]


@icon("anchored-image", CAT, "Picture frame beside text lines with a small anchor tying it to the paragraph.",
      tags=["anchor", "anchored object", "pin image", "image anchor", "float image", "layout"])
def _(S):
    return [shell(rect(3, 3, 10, 9, min(S.R, 3))), detail(poly([(5, 10), (8, 6.5), (11, 10)], r=S.r * 0.5)),
            *rows([(3, 13), (3, 10)], [16.5, 20.5]),
            line(circle(18.5, 5, 1.8)), line(seg(18.5, 7, 18.5, 18.5)), line(seg(16.5, 10, 20.5, 10)),
            line("M15 14.5a3.5 3.5 0 0 0 7 0")]


@icon("wrap-top-and-bottom", CAT, "Full-width picture block with text lines only above and below it.",
      tags=["wrap top and bottom", "text wrapping", "break text", "image layout", "above and below", "wrap"])
def _(S):
    return [tl(3, 3.5, 21), shell(rect(3, 8, 18, 8, min(S.R, 3))),
            detail(poly([(6, 14), (9.5, 10.5), (12.5, 13.5), (14, 12), (18, 14)], r=S.r * 0.5)), tl(3, 20.5, 21)]


@icon("wrap-behind-text", CAT, "Dashed picture block sitting beneath text lines that run across it.",
      tags=["behind text", "wrap behind", "watermark", "text over image", "text wrapping", "background image"])
def _(S):
    return [*dashes((7, 4), (17, 4), 3, 2), *dashes((7, 20), (17, 20), 3, 2),
            *dashes((7, 7), (7, 17), 3, 2), *dashes((17, 7), (17, 17), 3, 2),
            *rows([(3, 21)] * 3, [8, 12, 16])]


@icon("wrap-in-front-of-text", CAT, "Solid picture block covering the middle of several text lines.",
      tags=["in front of text", "wrap in front", "overlay image", "cover text", "text wrapping", "float"])
def _(S):
    return [*rows([(3, 21)] * 4, [4.5, 9.5, 14.5, 19.5]), solid(rect(7.5, 7, 9, 10, 1.5 if S.name == "rounded" else 0))]


@icon("wrap-tight", CAT, "Round picture with text lines ending close around its curved edge.",
      tags=["tight wrap", "contour wrap", "text wrapping", "round image", "wrap around shape", "layout"])
def _(S):
    cx, cy, r = 16, 12, 5
    out = [shell(circle(cx, cy, r)), detail(poly([(13, 14), (16, 10.5), (19, 14)], r=S.r * 0.5))]
    for y in (4.5, 8.5, 12, 15.5, 19.5):
        dy = abs(y - cy)
        R = r + 3.2
        end = 21 if dy >= R else cx - math.sqrt(R * R - dy * dy)
        if end - 3 >= 3:
            out.append(tl(3, y, min(end, 21)))
    return out


@icon("inline-image", CAT, "Text lines with a small picture frame set into one line like a word.",
      tags=["inline image", "in line with text", "inline picture", "image in text", "text layout", "figure"])
def _(S):
    return [tl(3, 4, 21), tl(3, 12, 6.5), shell(rect(8.5, 7.5, 7, 9, min(S.R, 3))), tl(17.5, 12, 21), tl(3, 20, 21)]


@icon("bleed-area", CAT, "Page with a dashed bleed line outside its trim edge and artwork running past it.",
      tags=["bleed", "print bleed", "trim", "crop marks", "print layout", "edge to edge"])
def _(S):
    return [shell(rect(7, 7, 10, 10, min(S.R, 3))), *dashes((3, 3), (21, 3), 3, 2), *dashes((3, 21), (21, 21), 3, 2),
            *dashes((3, 3), (3, 21), 3, 2), *dashes((21, 3), (21, 21), 3, 2),
            solid(poly([(3.5, 3.5), (12, 3.5), (3.5, 12)], closed=True))]


@icon("page-imposition", CAT, "Printed sheet divided into eight page panels, the top row turned upside down.",
      tags=["imposition", "print sheet", "signature", "page layout", "booklet", "press sheet"])
def _(S):
    xs = (4.5, 9.5, 14.5, 19.5)
    return [shell(rect(2, 3, 20, 18, min(S.R, 3))), detail(seg(7, 3, 7, 21)), detail(seg(12, 3, 12, 21)), detail(seg(17, 3, 17, 21)),
            detail(seg(2, 12, 22, 12)), *[dot(x, 9.2, 0.9) for x in xs], *[dot(x, 15.8, 0.9) for x in xs]]


@icon("perfect-binding", CAT, "Book block with a thick glued spine edge and stacked page lines.",
      tags=["perfect binding", "glue binding", "paperback", "spine", "book binding", "print finishing"])
def _(S):
    return [solid(rect(3, 3, 4, 18, 1 if S.name == "rounded" else 0)), shell(rect(7, 3, 14, 18, min(S.R, 3))),
            *rows([(10.5, 17.5)] * 3, [8, 12, 16], inside=True)]


# ============================================================================ lists

def stem(x, y, h=5, inside=False):
    return tl(x, y - h / 2, x, y + h / 2, inside=inside) if False else (detail if inside else line)(seg(x, y - h / 2, x, y + h / 2))


@icon("multilevel-list", CAT, "Outline list with numbered entries at two indent levels.",
      tags=["multilevel list", "outline", "nested numbering", "sub items", "legal numbering", "hierarchy"])
def _(S):
    return [stem(4, 5, 4), tl(8, 5, 21), stem(8, 12, 4), dot(11, 13, 1), stem(14, 12, 4), tl(17.5, 12, 21),
            stem(8, 19, 4), dot(11, 20, 1), stem(14, 19, 4), tl(17.5, 19, 21)]


@icon("lettered-list", CAT, "Three list lines led by the small letters a, b and c.",
      tags=["lettered list", "alphabetical list", "a b c list", "alpha list", "outline", "sub list"])
def _(S):
    return [*la(5.5, 4.8, 2.6), tl(12, 4.8, 21), *lb(5.5, 12.2, 2.6), tl(12, 12.2, 21), lc(5.5, 19.6, 2.6), tl(12, 19.6, 21)]


@icon("roman-numeral-list", CAT, "Three list lines led by the roman numerals I, II and III.",
      tags=["roman numerals", "roman list", "i ii iii", "outline list", "legal list", "numbered list"])
def _(S):
    return [stem(3.5, 5, 5), tl(13, 5, 21),
            stem(3.5, 12, 5), stem(6.8, 12, 5), tl(13, 12, 21),
            stem(3.5, 19, 5), stem(6.8, 19, 5), stem(10.1, 19, 5), tl(14.5, 19, 21)]


@icon("definition-list", CAT, "Heavy term bars each followed by an indented description line.",
      tags=["definition list", "glossary", "term and description", "dl", "dictionary", "key value"])
def _(S):
    return [solid(rect(3, 3, 8, 3, 0.8 if S.name == "rounded" else 0)), tl(7, 9, 21), tl(7, 12.5, 18),
            solid(rect(3, 16, 11, 3, 0.8 if S.name == "rounded" else 0)), tl(7, 22, 20)]


@icon("dash-list", CAT, "Three list lines each led by a short dash.",
      tags=["dash list", "hyphen list", "dashed bullets", "bulleted list", "list", "minus bullet"])
def _(S):
    return [x for y in (5, 12, 19) for x in (tl(3, y, 6.5), tl(10, y, 21))]


@icon("toggle-list", CAT, "List lines led by solid triangles, one turned down over indented lines.",
      tags=["toggle list", "collapsible list", "expand", "disclosure triangle", "outline", "tree list"])
def _(S):
    return [solid(poly([(3, 2.5), (3, 6.5), (6.5, 4.5)], closed=True)), tl(9.5, 4.5, 21),
            solid(poly([(2.5, 8.5), (7, 8.5), (4.75, 12)], closed=True)), tl(9.5, 10.5, 21),
            tl(11, 15.5, 21), tl(11, 20.5, 18)]


def _digit2(x, y):
    """Small numeral 2 about 5 wide and 8 tall with its top-left at (x, y)."""
    return line(f"M{fmt(x)} {fmt(y + 2.3)}C{fmt(x)} {fmt(y + 0.6)} {fmt(x + 1.2)} {fmt(y)} {fmt(x + 2.5)} {fmt(y)}"
                f"C{fmt(x + 3.9)} {fmt(y)} {fmt(x + 5)} {fmt(y + 0.8)} {fmt(x + 5)} {fmt(y + 2.3)}"
                f"C{fmt(x + 5)} {fmt(y + 4)} {fmt(x + 2)} {fmt(y + 5)} {fmt(x)} {fmt(y + 8)}H{fmt(x + 5)}", stroke_miterlimit="2")


@icon("restart-numbering", CAT, "Numbered lines 1 and 2, then a circular arrow before a new line numbered 1.",
      tags=["restart numbering", "start at 1", "reset list", "renumber", "numbered list", "list numbering"])
def _(S):
    return [_digit2(2.5, 4), tl(10, 8, 21), line(arc(5.5, 18, 3, -50, 230)), head(S, (7.5, 15.2), 10, 1.5),
            stem(11.5, 18, 4), tl(15, 18, 21)]


@icon("bullet-point", CAT, "Single solid round bullet beside a short text line.",
      tags=["bullet", "bullet point", "dot", "list marker", "unordered list", "round bullet"])
def _(S):
    return [solid(circle(6, 12, 3.25)), tl(12, 12, 21)]


@icon("arrow-bullet-list", CAT, "Three list lines each led by a small arrowhead bullet.",
      tags=["arrow bullets", "arrowhead list", "chevron list", "bulleted list", "list markers", "pointer list"])
def _(S):
    return [x for y in (5, 12, 19) for x in (line(poly([(3.5, y - 2.5), (6.5, y), (3.5, y + 2.5)], r=S.r * 0.5)), tl(10, y, 21))]


@icon("alphabetical-order", CAT, "Letters A and Z stacked with a downward arrow beside them.",
      tags=["alphabetical", "sort a to z", "alphabetic order", "sorting", "order by name", "az"])
def _(S):
    return [line(poly([(3, 10.5), (6.25, 3.5), (7.75, 3.5), (11, 10.5)], r=S.r * 0.5)), line(seg(4.6, 8, 9.4, 8)),
            line(poly([(3.5, 14), (10.5, 14), (3.5, 20.5), (10.5, 20.5)], r=S.r * 0.3), stroke_miterlimit="2"), line(seg(18, 3, 18, 19)), head(S, (18, 19.5), 90)]


# ============================================================================ tables

@icon("cell-alignment", CAT, "Table cell with centred text lines in the middle of its border.",
      tags=["cell alignment", "align cell", "center text in cell", "table cell", "vertical align", "table"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, S.R)), *rows([(7, 17), (9.5, 14.5), (8, 16)], [8.5, 12, 15.5], inside=True)]


@icon("cell-padding", CAT, "Table cell with a dashed inner box showing the space between its content and border.",
      tags=["cell padding", "cell margin", "inner spacing", "table padding", "table cell", "spacing"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, S.R)),
            *dashes((8.5, 8), (15.5, 8), 2.5, 2, inside=True), *dashes((8.5, 16), (15.5, 16), 2.5, 2, inside=True),
            *dashes((8, 8.5), (8, 15.5), 2.5, 2, inside=True), *dashes((16, 8.5), (16, 15.5), 2.5, 2, inside=True)]


@icon("draw-table", CAT, "Small table grid whose last border line is still being drawn by a pencil.",
      tags=["draw table", "table pencil", "sketch table", "insert table by drawing", "grid", "table tool"])
def _(S):
    A, B, C, D = (14.46, 11.78), (21.18, 18.5), (18.5, 21.18), (11.78, 14.46)
    return [line(poly([(3, 11), (3, 3), (11, 3), (11, 11)], r=S.r)), line(seg(7, 3, 7, 11)), line(seg(3, 7, 11, 7)),
            shell(poly([(11, 11), A, B, C, D], closed=True, r=S.r * 0.3)), detail(seg(*A, *D))]


@icon("text-to-table", CAT, "Text lines, an arrow and a small table grid showing text turned into a table.",
      tags=["text to table", "convert text to table", "turn text into table", "insert table from text", "transform", "table"])
def _(S):
    return [*rows([(2.5, 7)] * 3, [6, 12, 18]), line(seg(8.5, 12, 11.5, 12)), head(S, (11.5, 12), 0, 2),
            shell(rect(13.5, 5, 8, 14, min(S.R, 2))), detail(seg(17.5, 5, 17.5, 19)), detail(seg(13.5, 12, 21.5, 12))]


@icon("distribute-columns", CAT, "Table with three equal columns and an even spacing scale above them.",
      tags=["distribute columns", "equal column width", "even columns", "table columns", "same width", "table"])
def _(S):
    return [line(seg(3, 4.5, 21, 4.5)), *[line(seg(x, 2.5, x, 6.5)) for x in (3, 9, 15, 21)],
            shell(rect(3, 9, 18, 12, min(S.R, 3))), detail(seg(9, 9, 9, 21)), detail(seg(15, 9, 15, 21))]


@icon("diagonal-cell-split", CAT, "Table corner cell crossed by a diagonal line with a text mark in each half.",
      tags=["diagonal header", "split cell diagonally", "diagonal line cell", "corner cell", "table header", "matrix table"])
def _(S):
    return [shell(rect(3, 3, 18, 18, min(S.R, 3))), detail(seg(3, 3, 21, 21)),
            tl(12, 7.5, 18, inside=True), tl(6, 16.5, 12, inside=True)]


@icon("repeat-header-row", CAT, "Same heavy header row repeated at the top of a table on the next page.",
      tags=["repeat header row", "header row", "table header", "page break", "continued table", "repeat headers"])
def _(S):
    return [solid(rect(3, 2, 18, 3.5, 1 if S.name == "rounded" else 0)),
            line(poly([(3, 5.5), (3, 9.5), (21, 9.5), (21, 5.5)], r=S.r * 0.5)), line(seg(12, 5.5, 12, 9.5)),
            *dashes((3, 12.5), (21, 12.5), 3, 2),
            solid(rect(3, 15, 18, 3.5, 1 if S.name == "rounded" else 0)),
            line(poly([(3, 18.5), (3, 21.5), (21, 21.5), (21, 18.5)], r=S.r * 0.5)), line(seg(12, 18.5, 12, 21.5))]


@icon("split-table", CAT, "Table grid cut into two parts with a dashed cut line between them.",
      tags=["split table", "break table", "divide table", "cut table", "separate table", "table"])
def _(S):
    return [line(poly([(3, 9), (3, 3), (21, 3), (21, 9)], r=S.r)), line(seg(12, 3, 12, 9)),
            *dashes((3, 12), (21, 12), 3, 2),
            line(poly([(3, 15), (3, 21), (21, 21), (21, 15)], r=S.r)), line(seg(12, 15, 12, 21))]


@icon("table-gridlines", CAT, "Table drawn in dotted lines with no solid borders.",
      tags=["gridlines", "table gridlines", "dotted table", "borderless table", "show gridlines", "table"])
def _(S):
    out = []
    for v in (3, 12, 21):
        out += dashes((v, 3), (v, 21), 3, 2) + dashes((3, v), (21, v), 3, 2)
    return out


@icon("erase-table-border", CAT, "Small table grid with an eraser wiping out part of an inner line.",
      tags=["erase border", "remove table border", "table eraser", "delete line", "table cleanup", "eraser"])
def _(S):
    return [shell(rect(3, 3, 12, 12, min(S.R, 3))), detail(seg(3, 9, 15, 9)), detail(seg(9, 3, 9, 6.5)),
            shell(poly([(13.5, 18), (17, 14.5), (21, 18.5), (17.5, 22)], closed=True, r=S.r * 0.5)),
            detail(seg(15.3, 20.2, 19.2, 16.3))]


@icon("tab-leader", CAT, "Short word, a row of dots and a number joined by a dotted tab leader.",
      tags=["tab leader", "dot leader", "dotted leader", "table of contents line", "price list", "tab stop"])
def _(S):
    return [tl(3, 7, 9), dot(11.5, 7, 1), dot(14.2, 7, 1), dot(16.9, 7, 1), tl(19, 7, 21.5),
            tl(3, 17, 11), dot(13.5, 17, 1), dot(16.2, 17, 1), tl(19, 17, 21.5)]


@icon("table-of-figures", CAT, "List of small picture thumbnails each followed by a dotted leader and a page number.",
      tags=["table of figures", "list of figures", "figure index", "illustrations list", "captions list", "thumbnail list"])
def _(S):
    return [x for y in (5.5, 12, 18.5) for x in
            (solid(rect(3, y - 2.5, 5, 5, 1 if S.name == "rounded" else 0)), dot(11, y, 1), dot(13.7, y, 1), dot(16.4, y, 1), tl(19, y, 21.5))]


# ============================================================================ review and proofing

@icon("comment-thread", CAT, "Two stacked speech bubbles joined by a thin reply line.",
      tags=["comment thread", "replies", "reply chain", "conversation", "discussion", "review comments"])
def _(S):
    return [shell(rect(7, 2.5, 14, 7, min(S.R, 3))), shell(rect(7, 14.5, 14, 7, min(S.R, 3))),
            line(poly([(6.5, 6), (3.5, 6), (3.5, 18), (6.5, 18)], r=S.r * 0.5))]


@icon("inline-comment", CAT, "Text line with a highlighted word and a small speech bubble above it.",
      tags=["inline comment", "comment on word", "annotation", "highlight comment", "margin note", "review"])
def _(S):
    return [shell(poly([(8, 2.5), (21, 2.5), (21, 10), (13, 10), (10.5, 12.5), (10.5, 10), (8, 10)], closed=True, r=S.r)),
            tl(3, 19, 6.5), solid(rect(8.5, 15.5, 7, 7, 1 if S.name == "rounded" else 0)), tl(17.5, 19, 21.5)]


@icon("suggest-edits", CAT, "Text with a crossed-out word and a pencil writing a replacement above it.",
      tags=["suggest edits", "suggesting mode", "track changes", "propose edit", "edit suggestion", "redline"])
def _(S):
    A, B, C, D = (16.1, 9.65), (20.1, 5.6), (17.9, 3.4), (13.85, 7.4)
    return [tl(3, 10, 10.5), shell(poly([(13, 10.5), A, B, C, D], closed=True, r=S.r * 0.3)),
            tl(3, 18, 6.5), tl(9, 18, 15), line(seg(8.5, 21, 15.5, 15)), tl(17.5, 18, 21)]


@icon("change-bar", CAT, "Text lines with a thick bar in the margin beside two of them.",
      tags=["change bar", "revision bar", "margin bar", "modified lines", "track changes", "revision mark"])
def _(S):
    return [*rows([(8, 21), (8, 21), (8, 21), (8, 18)], [4.5, 9.5, 14.5, 19.5]),
            solid(rect(2.5, 7, 2.5, 10, 0.8 if S.name == "rounded" else 0))]


# ============================================================================ proofreading marks

def tmark(x, y, w=6, h=7):
    return glyph_T(x, y, w, h)


@icon("stet-mark", CAT, "Word with a dotted underline and a small scribbled note in the margin that means let it stand.",
      tags=["stet", "let it stand", "keep as is", "ignore correction", "proofreading", "undo edit"])
def _(S):
    return [*lb(6, 9, 2.6), *la(12, 9, 2.6), *[dot(x, 16.5, 1) for x in (3.5, 6.5, 9.5, 12.5, 15.5)],
            line("M21.5 10C21.5 8.5 20.3 8 19.5 8C18.3 8 17.5 8.8 17.5 9.8C17.5 11.8 21.5 11.5 21.5 13.8C21.5 15 20.5 15.7 19.5 15.7C18.5 15.7 17.7 15.2 17.5 14.1")]


@icon("transpose-mark", CAT, "Two letters with an S-shaped proofreading curve looping over one and under the other.",
      tags=["transpose", "swap letters", "swap order", "proofreading mark", "reorder", "tr"])
def _(S):
    return [*la(6.5, 13.5, 2.5), *glyph_T(14.5, 10, 6, 6.5), line("M3.5 7.5C3.5 2.5 10.5 2.5 12 11C13.5 20 21.5 22 21.5 18.5")]


@icon("insert-space-mark", CAT, "Text line with a caret mark below it and a hash sign above for inserting a space.",
      tags=["insert space", "add space", "caret", "hash mark", "proofreading", "space needed"])
def _(S):
    return [line(seg(9.5, 2.5, 9.5, 8.5)), line(seg(14.5, 2.5, 14.5, 8.5)), line(seg(7, 4, 17, 4)), line(seg(7, 7, 17, 7)),
            tl(3, 12.5, 21), line(poly([(8.5, 20.5), (12, 16), (15.5, 20.5)], r=S.r * 0.5))]


@icon("capitalize-proof-mark", CAT, "Lowercase letter with three short lines under it, the proofreading mark for capitals.",
      tags=["capitalize", "make capital", "capital letters mark", "three lines", "proofreading", "uppercase mark"])
def _(S):
    return [*la(12, 7, 3.3), tl(6.5, 14.5, 17.5), tl(6.5, 17.5, 17.5), tl(6.5, 20.5, 17.5)]


@icon("lowercase-proof-mark", CAT, "Capital letter crossed by a single slash, the proofreading mark for lowercase.",
      tags=["lowercase mark", "make lowercase", "slash through letter", "proofreading", "small letters", "lc"])
def _(S):
    return [*glyph_T(6, 5, 12, 15), line(seg(19.5, 4, 6.5, 21))]


@icon("endnote", CAT, "Page with a short rule near the bottom and a numbered note beneath it.",
      tags=["endnote", "footnote", "reference note", "notes section", "citation", "numbered note"])
def _(S):
    return [shell(rect(3.5, 2.5, 17, 19, min(S.R, 3))), *rows([(7, 17), (7, 14)], [6.5, 10], inside=True),
            detail(seg(7, 13.5, 11, 13.5)), stem(7.5, 17.5, 3, inside=True), tl(11, 17.5, 17, inside=True)]


@icon("cross-reference", CAT, "Text with a small number linked by a curved arrow to a heading elsewhere on the page.",
      tags=["cross reference", "see also", "link to section", "reference", "jump to heading", "internal link"])
def _(S):
    return [tl(3, 4.5, 14), stem(18, 4.5, 3), tl(3, 10, 12),
            solid(rect(3, 17, 9, 3.5, 0.8 if S.name == "rounded" else 0)),
            line("M18 8.5V15a3.5 3.5 0 0 1-3.5 3.5H14.5"), head(S, (13.8, 18.7), 180, 2)]


@icon("comments-sidebar", CAT, "Page of text with a column of small speech bubbles along its right side.",
      tags=["comments sidebar", "comment pane", "margin comments", "review panel", "annotations list", "feedback"])
def _(S):
    bub = lambda y: shell(poly([(16.5, y), (21.5, y), (21.5, y + 3.5), (18.5, y + 3.5), (17, y + 5), (17, y + 3.5), (16.5, y + 3.5)], closed=True, r=0), stroke_miterlimit="2")
    return [shell(rect(2.5, 2.5, 11.5, 19, min(S.R, 3))), *rows([(5.5, 11)] * 4, [6.5, 10.5, 14.5, 18.5], inside=True),
            solid(rect(16.5, 3, 5, 4, 1 if S.name == "rounded" else 0)), solid(rect(16.5, 10, 5, 4, 1 if S.name == "rounded" else 0)),
            solid(rect(16.5, 17, 5, 4, 1 if S.name == "rounded" else 0))]


@icon("mark-as-final", CAT, "Document with a small ribbon seal at its lower corner.",
      tags=["mark as final", "final version", "approved document", "seal", "ribbon", "read only"])
def _(S):
    return [shell(rect(3.5, 2.5, 13, 19, min(S.R, 3))), *rows([(7, 13), (7, 11)], [7, 11], inside=True),
            shell(circle(17, 15.5, 3.5)), dot(17, 15.5, 0.9), line(seg(15.5, 19, 14.7, 22)), line(seg(18.5, 19, 19.3, 22))]


@icon("errata-slip", CAT, "Narrow slip of paper with two lines tucked between the pages of an open book.",
      tags=["errata", "correction slip", "erratum", "loose insert", "book correction", "printed correction"])
def _(S):
    return [shell(rect(9, 2.5, 6.5, 11, min(S.R, 2))), *rows([(10.5, 14)] * 2, [6, 9.5], inside=True),
            shell(poly([(2.5, 13), (12, 15), (21.5, 13), (21.5, 20), (12, 22), (2.5, 20)], closed=True, r=S.r)),
            detail(seg(12, 15, 12, 22))]


# ============================================================================ punctuation and accents

@icon("em-dash", CAT, "Long dash standing between two upright letter strokes.",
      tags=["em dash", "long dash", "dash punctuation", "interruption", "punctuation", "mdash"])
def _(S):
    return [line(seg(3.5, 7.5, 3.5, 16.5)), line(seg(20.5, 7.5, 20.5, 16.5)), line(seg(7.5, 12, 16.5, 12))]


@icon("en-dash", CAT, "Medium dash between the digits 1 and 9 as a numeric range.",
      tags=["en dash", "range dash", "number range", "dash punctuation", "punctuation", "ndash"])
def _(S):
    return [line(poly([(2.5, 9.5), (4.5, 7.5), (4.5, 16.5)], r=0)), line(seg(8.5, 12, 14, 12)),
            line(circle(18.5, 10.5, 2.5)), line(seg(21, 10.5, 21, 16.5))]


@icon("interpunct", CAT, "Single dot at mid letter height between two letters.",
      tags=["interpunct", "middle dot", "word separator", "centered dot", "punctuation", "latin dot"])
def _(S):
    return [*lb(6, 13.5, 3), *la(18, 13.5, 3), solid(circle(12, 13.5, 1.4))]


@icon("apostrophe", CAT, "Small curved comma mark raised high beside the letter s.",
      tags=["apostrophe", "possessive", "contraction", "single quote mark", "punctuation", "tick"])
def _(S):
    return [solid(circle(7.5, 6, 1.8)), line("M9 7.5C9 9.5 8 11 6.5 12"),
            line("M20.5 12C20.5 10.5 19 10 17.5 10C15.5 10 14.5 11 14.5 12.5C14.5 15 20.5 15 20.5 17.5C20.5 19.5 19 20.5 17.5 20.5C15.7 20.5 14.7 19.5 14.5 18")]


@icon("full-stop", CAT, "Solid round dot on the baseline after a short word.",
      tags=["full stop", "period", "end of sentence", "point", "punctuation", "dot"])
def _(S):
    return [*la(5.5, 15.5, 2.6), lc(12.5, 15.5, 2.6), solid(circle(19, 18, 2))]


def _comma_mark(cx, cy, flip=False):
    """Small filled dot with a curved tail, a comma-shaped quotation mark."""
    sgn = -1 if flip else 1
    return [solid(circle(cx, cy, 1.7)), line(f"M{fmt(cx + 1.4 * sgn)} {fmt(cy + 1.4)}C{fmt(cx + 1.4 * sgn)} {fmt(cy + 3.4)} {fmt(cx + 0.2 * sgn)} {fmt(cy + 5)} {fmt(cx - 1.4 * sgn)} {fmt(cy + 6)}")]


@icon("smart-quotes", CAT, "Curly double quotation marks next to a pair of straight vertical quote marks.",
      tags=["smart quotes", "curly quotes", "typographic quotes", "straight quotes", "quotation marks", "punctuation"])
def _(S):
    return [*_comma_mark(5, 5.5), *_comma_mark(10.5, 5.5), line(seg(15.5, 13, 15.5, 19)), line(seg(20.5, 13, 20.5, 19))]


@icon("low-quotation-marks", CAT, "Low comma-shaped double quote at the baseline and a raised pair on the other side.",
      tags=["low quotes", "german quotes", "double low quotes", "quotation marks", "opening quote", "punctuation"])
def _(S):
    return [*_comma_mark(4.5, 15), *_comma_mark(10, 15), *_comma_mark(14, 4.5, flip=True), *_comma_mark(19.5, 4.5, flip=True)]


@icon("cjk-corner-brackets", CAT, "Pair of East Asian quotation brackets, an upper left corner and a lower right corner.",
      tags=["corner brackets", "cjk quotes", "japanese quotes", "chinese quotes", "kagikakko", "quotation brackets"])
def _(S):
    return [line(poly([(11.5, 4), (4, 4), (4, 12)], r=S.r)), line(poly([(12.5, 20), (20, 20), (20, 12)], r=S.r))]


@icon("irony-mark", CAT, "Backwards question mark with its hook opening to the left.",
      tags=["irony mark", "sarcasm mark", "reversed question mark", "rhetorical question", "punctuation", "percontation"])
def _(S):
    return [line("M16 8.5C16 6 14.2 4.5 12 4.5C9.8 4.5 8 6 8 8C8 11.5 12 12 12 15"), solid(circle(12, 19.5, 1.6))]


def pt(cx, cy, r, deg):
    return (cx + r * math.cos(math.radians(deg)), cy + r * math.sin(math.radians(deg)))


@icon("dinkus", CAT, "Three asterisks spaced in a row as a section break.",
      tags=["dinkus", "section break", "scene break", "asterisks", "ornament", "divider"])
def _(S):
    out = []
    for cx in (5, 12, 19):
        for a in (-90, -18, 54, 126, 198):
            (x0, y0), (x1, y1) = pt(cx, 12, 0.8, a), pt(cx, 12, 3.4, a)
            out.append(line(seg(x0, y0, x1, y1)))
    return out


@icon("grave-accent", CAT, "Lowercase e with a short stroke slanting down to the right above it.",
      tags=["grave accent", "accent mark", "diacritic", "backtick", "e grave", "french accent"])
def _(S):
    return [line(arc(12, 15.5, 4.5, 45, 360)), line(seg(7.5, 15.5, 16.5, 15.5)), line(seg(8.5, 4, 12.5, 8))]


@icon("caron", CAT, "Lowercase c with a small v-shaped mark above it.",
      tags=["caron", "hacek", "diacritic", "accent mark", "c with caron", "check accent"])
def _(S):
    return [lc(12, 16, 4.6), line(poly([(8, 4.5), (12, 8.5), (16, 4.5)], r=S.r * 0.5))]


@icon("dot-above", CAT, "Capital I with a single round dot above it.",
      tags=["dot above", "overdot", "diacritic", "dotted i", "turkish i", "accent mark"])
def _(S):
    return [solid(circle(12, 4.5, 1.8)), line(seg(12, 10, 12, 21)), line(seg(8.5, 10, 15.5, 10)), line(seg(8.5, 21, 15.5, 21))]


@icon("dotless-i", CAT, "Lowercase i stem without its dot beside a dotted i for comparison.",
      tags=["dotless i", "turkish i", "i without dot", "diacritic", "letter i", "character"])
def _(S):
    return [line(seg(6.5, 9.5, 6.5, 20)), line(seg(17.5, 9.5, 17.5, 20)), solid(circle(17.5, 4.8, 1.7))]


@icon("solidus", CAT, "Forward slash between the digits 1 and 2.",
      tags=["solidus", "slash", "forward slash", "fraction slash", "virgule", "punctuation"])
def _(S):
    return [line(poly([(2.5, 11), (4.5, 9), (4.5, 18)], r=0)), line(seg(10, 20, 14, 4)),
            line("M17 11.5C17 9.5 18.3 8.5 19.5 8.5C21 8.5 22 9.5 22 11C22 13 19.5 14.5 17 18H22")]


@icon("block-selection", CAT, "Text lines with a tall column selection box cutting across them.",
      tags=["block selection", "column selection", "rectangular selection", "box select", "vertical selection", "text editing"])
def _(S):
    return [*[tl(2.5, y, 5.5) for y in (5, 10, 15, 20)], *[tl(18.5, y, 21.5) for y in (5, 10, 15, 20)],
            shell(rect(8, 2.5, 8, 19, min(S.R, 2))), *rows([(10.5, 13.5)] * 3, [7, 12, 17], inside=True)]


@icon("overtype-mode", CAT, "Letters either side of a solid block cursor covering one letter.",
      tags=["overtype", "overwrite mode", "block cursor", "replace typing", "insert key", "text editing"])
def _(S):
    return [*la(5.5, 14, 2.6), solid(rect(10, 5, 5, 14, 0.8 if S.name == "rounded" else 0)), lc(18.6, 14, 2.6)]


@icon("vertical-text-cursor", CAT, "Sideways I-beam cursor beside columns of vertical text marks.",
      tags=["vertical text cursor", "sideways cursor", "vertical writing", "text direction", "caret", "cursor"])
def _(S):
    return [line(seg(3, 12, 10, 12)), line(seg(3, 8.5, 3, 15.5)), line(seg(10, 8.5, 10, 15.5)),
            line(seg(14.5, 3, 14.5, 17)), line(seg(19.5, 3, 19.5, 21))]
