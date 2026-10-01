"""TypeIcon Core: typography (batch typography_001).

Text styling effects, font features and the anatomy of letterforms. Letters are drawn from 2 px strokes
(never font text); emphasised parts are heavier solid strokes. Line and Rounded differ by caps, joins and
fillets; Filled makes strokes heavier or knocks details out of solid shells.
"""
from __future__ import annotations

import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d

CAT = "typography"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    return a if S.name == "line" else b


def lines(ds):
    return [line(d) for d in ds]


def fat(S, d, w=4.2):
    """Heavy solid stroke of a d-string (an emphasised part of a letter)."""
    return solid(path_to_d(ST(d, w, S.cap, S.join)))


def gA(S, x0, top, x1, base, bar=None, flat=0.75):
    """Capital A as d-strings: two legs with a flat apex and a crossbar."""
    mid = (x0 + x1) / 2
    bar = top + (base - top) * 0.68 if bar is None else bar
    t = (bar - top) / (base - top)
    xl, xr = mid - flat - t * (mid - flat - x0), mid + flat + t * (x1 - mid - flat)
    return [poly([(x0, base), (mid - flat, top), (mid + flat, top), (x1, base)], r=S.r * 0.5), seg(xl, bar, xr, bar)]


def sheared(pts, k, yc=12.0):
    return [(x + (yc - y) * k, y) for x, y in pts]


def ext_arrow(S, tip, frm, size=3.0):
    """Open arrowhead at tip for a shaft arriving from frm."""
    a = math.atan2(tip[1] - frm[1], tip[0] - frm[0])
    pts = [(tip[0] + size * math.cos(a + math.pi + s * math.radians(40)),
            tip[1] + size * math.sin(a + math.pi + s * math.radians(40))) for s in (1, -1)]
    return line(poly([pts[0], tip, pts[1]], r=S.r * 0.5), stroke_miterlimit="1.6")


# ============================================================================ text effects

@icon("double-underline", CAT, "Capital A with two parallel lines beneath it.",
      tags=["double underline", "underline", "text format", "emphasis", "editor", "decoration"])
def _(S):
    return lines(gA(S, 5, 3, 19, 13)) + [line(seg(4, 17, 20, 17)), line(seg(4, 21, 20, 21))]


@icon("dotted-underline", CAT, "Capital A with a row of dots beneath it.",
      tags=["dotted underline", "underline", "text format", "dots", "editor", "decoration"])
def _(S):
    return lines(gA(S, 5, 3, 19, 16)) + [dot(x, 20.5, 1.25) for x in (4, 8, 12, 16, 20)]


@icon("dashed-underline", CAT, "Capital A with a dashed line beneath it.",
      tags=["dashed underline", "underline", "text format", "dashes", "editor", "decoration"])
def _(S):
    return lines(gA(S, 5, 3, 19, 16)) + [line(seg(3.5, 20.5, 8, 20.5)), line(seg(10, 20.5, 14, 20.5)),
                                         line(seg(16, 20.5, 20.5, 20.5))]


@icon("overline", CAT, "Capital A with a single bar above its apex.",
      tags=["overline", "overbar", "text format", "line above", "editor", "decoration"])
def _(S):
    return [line(seg(4, 4, 20, 4))] + lines(gA(S, 5, 9, 19, 21, flat=0.9))


@icon("double-strikethrough", CAT, "Letter S crossed by two close parallel lines.",
      tags=["double strikethrough", "strikethrough", "crossed out", "text format", "delete", "editor"])
def _(S):
    return [line("M16.8 6.6C16 5 14.3 3.5 12 3.5C9.3 3.5 7.3 5.3 7.3 7.5C7.3 8.6 7.6 9.4 8.2 10"),
            line("M15.9 14C16.5 14.8 16.8 15.6 16.8 16.4C16.8 18.6 14.8 20.5 12 20.5C9.5 20.5 7.6 19.3 6.9 17.6"),
            line(seg(3, 10, 21, 10)), line(seg(3, 14, 21, 14))]


@icon("bold-italic", CAT, "Heavy slanted letter B with thick strokes leaning right.",
      tags=["bold italic", "bold", "italic", "emphasis", "text format", "slanted", "editor"])
def _(S):
    k = 0.22
    rr = 2.6
    stem = poly(sheared([(7.5, 4), (7.5, 20)], k))
    b1 = poly(sheared([(7.5, 4), (13.5, 4), (16.5, 7.8), (13.5, 12), (7.5, 12)], k), r=rr)
    b2 = poly(sheared([(7.5, 12), (14.5, 12), (17.5, 16.2), (14.5, 20), (7.5, 20)], k), r=rr)
    return [fat(S, stem, 3.4), fat(S, b1, 3.4), fat(S, b2, 3.4)]


@icon("embossed-text", CAT, "Capital A with a raised shadow edge offset to its lower right.",
      tags=["embossed text", "emboss", "raised", "shadow", "3d text", "text effect", "bevel"])
def _(S):
    return lines(gA(S, 3, 3.5, 13, 16)) + [line(seg(15.5, 10.5, 19, 18.5)), line(seg(6, 21, 19, 21))]


@icon("glowing-text", CAT, "Capital A surrounded by short radiating rays.",
      tags=["glowing text", "glow", "neon", "shine", "rays", "text effect", "light"])
def _(S):
    ray = []
    for a in (-90, -50, -130, -12, -168):
        x0, y0 = pt_on(12, 13, 8.2, a)
        x1, y1 = pt_on(12, 13, 10.5, a)
        ray.append(line(seg(x0, y0, x1, y1)))
    return lines(gA(S, 7.5, 8, 16.5, 19)) + ray


@icon("gradient-text", CAT, "Bold capital A that fades from solid strokes on the left to dashes on the right.",
      tags=["gradient text", "gradient", "fade", "hatching", "fill", "text effect", "color"])
def _(S):
    return [fat(S, seg(4.5, 21, 10.2, 4.5), 4.4), fat(S, seg(8, 15.5, 12.5, 15.5), 3.6),
            line(seg(14.2, 15.5, 16.8, 15.5)),
            line(seg(12.8, 6.5, 14.6, 11.5)), line(seg(16.4, 15, 19.5, 21))]


@icon("extruded-text", CAT, "Capital A with depth lines running back from its corners like a 3D block letter.",
      tags=["extruded text", "extrude", "3d text", "depth", "block letter", "text effect", "dimension"])
def _(S):
    return lines(gA(S, 3, 8, 14, 21, flat=0.8)) + [
        line(seg(8.2, 8, 12.5, 3.5)), line(seg(12.5, 3.5, 20, 16)), line(seg(14, 21, 20, 16)),
        line(seg(9.7, 8, 13.8, 3.5))][:3]


@icon("reflected-text", CAT, "Capital A standing on a line with a broken upside-down copy beneath.",
      tags=["reflected text", "reflection", "mirror", "flip", "text effect", "shadow", "below"])
def _(S):
    return lines(gA(S, 6, 3, 18, 11)) + [line(seg(3, 13, 21, 13)),
                                         line(seg(8, 16, 9.4, 19)), line(seg(14.6, 19, 16, 16)),
                                         line(seg(10.5, 21, 13.5, 21))]


@icon("knockout-text", CAT, "Solid rounded square with the letter A cut out of it.",
      tags=["knockout text", "knockout", "cutout", "reversed text", "negative", "mask", "text effect"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R))] + [detail(d) for d in gA(S, 7.5, 7, 16.5, 17, flat=0.8)]


@icon("warped-text", CAT, "Letter A inside a lens-shaped envelope with curved guide lines.",
      tags=["warped text", "warp", "arc text", "envelope distort", "curved text", "text effect", "bend"])
def _(S):
    return [line("M3 9Q12 -2 21 9"), line("M3 15Q12 26 21 15")] + lines(gA(S, 8.5, 6.5, 15.5, 17.5, flat=0.7))


@icon("sketched-text", CAT, "Capital A drawn with loose crossing strokes that overshoot at the ends.",
      tags=["sketched text", "sketch", "hand drawn", "pencil", "rough", "text effect", "doodle"])
def _(S):
    return [line(seg(3.5, 21, 13, 3)), line(seg(20.5, 21, 10.5, 3.5)), line(seg(5.5, 15.5, 20.5, 16))]


@icon("distressed-text", CAT, "Bold capital A with gaps and specks worn out of its strokes.",
      tags=["distressed text", "grunge", "worn", "rough", "vintage", "text effect", "texture"])
def _(S):
    return [fat(S, seg(4.5, 21, 7.5, 14.5), 3.6), fat(S, seg(9, 11.5, 11.5, 6), 3.6),
            fat(S, seg(14.5, 7, 19.5, 21), 3.6),
            line(seg(8.5, 16, 12, 16)), line(seg(14, 16, 16, 16)),
            dot(5, 4.5, 1.25), dot(20, 7, 1.0)]

def legx(S, y, x0, top, x1, base, flat=0.75):
    """x of the left leg of gA at height y (the right leg mirrors it about the centre)."""
    mid = (x0 + x1) / 2
    return (mid - flat) - (y - top) / (base - top) * (mid - flat - x0)


def lc_a(S, cx, cy, rx, ry):
    return [ellipse(cx, cy, rx, ry), seg(cx + rx, cy - ry, cx + rx, cy + ry)]


def lc_b(S, cx, cy, rx, ry, top):
    return [ellipse(cx, cy, rx, ry), seg(cx - rx, top, cx - rx, cy + ry)]


@icon("glitch-text", CAT, "Capital A sliced into three bands with the middle band shifted sideways.",
      tags=["glitch text", "glitch", "distortion", "slice", "digital", "text effect", "offset"])
def _(S):
    x0, top, x1, base = 4, 3, 20, 21

    def band(ya, yb, dx=0.0):
        a, b = legx(S, ya, x0, top, x1, base), legx(S, yb, x0, top, x1, base)
        mid = 12 + dx
        return [line(seg(a + dx, ya, b + dx, yb)), line(seg(2 * 12 - a + dx, ya, 2 * 12 - b + dx, yb))]
    out = band(3, 8) + band(11, 15, 3) + band(18, 21)
    out.append(line(seg(8.2 + 3, 13.5, 15.8 + 3, 13.5)))
    return out


@icon("perspective-text", CAT, "Receding page of ruled text lines that narrows toward the top.",
      tags=["perspective text", "perspective", "vanishing point", "3d text", "receding", "text effect", "skew"])
def _(S):
    return [shell(poly([(8, 3.5), (16, 3.5), (21.5, 20.5), (2.5, 20.5)], closed=True, r=S.r)),
            detail(seg(6.3, 9.5, 17.7, 9.5)), detail(seg(4.4, 15, 19.6, 15))]


@icon("camel-case", CAT, "The letters a, B and c with a raised capital under a hump arc.",
      tags=["camel case", "camelcase", "naming convention", "programming", "capital letter", "variable name", "coding style"])
def _(S):
    return [line(ellipse(4.2, 18.3, 2.4, 2.5)), line(seg(6.6, 15.8, 6.6, 20.8)),
            line(seg(10.5, 9, 10.5, 21)),
            line("M10.5 9H13A3 3 0 0 1 13 15H10.5"), line("M10.5 15H13.5A3 3 0 0 1 13.5 21H10.5"),
            line("M9.5 6.3A3.6 3 0 0 1 17 6.3"),
            line(arc(20, 18.3, 2.4, 45, 315))]


@icon("snake-case", CAT, "Letters a and b joined by an underscore at the baseline.",
      tags=["snake case", "snake_case", "underscore", "naming convention", "programming", "variable name", "coding style"])
def _(S):
    return lines(lc_a(S, 4.9, 12.5, 2.5, 3.7)) + lines(lc_b(S, 19.1, 12.5, 2.5, 3.7, 3.5)) + [line(seg(9.5, 20.5, 14.5, 20.5))]


@icon("kebab-case", CAT, "Letters a and b joined by a short hyphen at mid height.",
      tags=["kebab case", "kebab-case", "hyphen", "dash", "naming convention", "programming", "coding style"])
def _(S):
    return lines(lc_a(S, 4.9, 14, 2.5, 3.7)) + lines(lc_b(S, 19.1, 14, 2.5, 3.7, 5)) + [line(seg(10.7, 14, 13.3, 14))]


@icon("raised-initial", CAT, "Large capital A on the first line of text, rising above the text block.",
      tags=["raised initial", "initial cap", "drop cap", "raised cap", "paragraph", "typesetting", "first letter"])
def _(S):
    return lines(gA(S, 3, 3, 11, 12, flat=0.7)) + [line(seg(13.5, 12, 21, 12)),
                                                   line(seg(3, 16.5, 21, 16.5)), line(seg(3, 21, 15, 21))]


@icon("text-expansion", CAT, "Abbreviation A with a dot, an arrow, and a longer block of text.",
      tags=["text expansion", "text expander", "abbreviation", "snippet", "shortcut", "autotext", "expand"])
def _(S):
    return lines(gA(S, 2.2, 8.5, 8, 16.5, flat=0.6)) + [dot(10, 15.8, 1.1),
            line(seg(12, 12, 14, 12)), ext_arrow(S, (15, 12), (12, 12), 2.4),
            line(seg(17.5, 6, 22, 6)), line(seg(17.5, 12, 22, 12)), line(seg(17.5, 18, 22, 18))]


@icon("paraphrase", CAT, "Two text lines with a pair of circular arrows between them for a rewrite.",
      tags=["paraphrase", "rewrite", "reword", "rephrase", "rewrite text", "ai writing", "text"])
def _(S):
    cx, cy, r = 12, 12, 3.8
    out = [line(seg(3, 3.5, 21, 3.5)), line(seg(3, 20.5, 15, 20.5))]
    out += [line(arc(cx, cy, r, 200, 335)), line(arc(cx, cy, r, 20, 155))]
    for a in (335, 155):
        tip = pt_on(cx, cy, r, a)
        back = pt_on(cx, cy, r, a - 25)
        out.append(ext_arrow(S, tip, back, 2.4))
    return out


@icon("expand-text", CAT, "A short text line that opens out into three longer lines.",
      tags=["expand text", "elaborate", "lengthen", "make longer", "ai writing", "text", "grow"])
def _(S):
    return [line(seg(2.5, 12, 6.5, 12)),
            line(poly([(8.5, 8.5), (11.5, 12), (8.5, 15.5)], r=S.r * 0.5)),
            line(seg(14.5, 5, 22, 5)), line(seg(14.5, 12, 22, 12)), line(seg(14.5, 19, 22, 19))]


@icon("writers-block", CAT, "Pen nib pressed against a small brick wall.",
      tags=["writers block", "writer's block", "stuck", "blocked", "creative block", "no ideas", "brick wall", "writing"])
def _(S):
    nib = "M12 12C10 8.5 8.5 6.5 6 5.5H2.5V18.5H6C8.5 17.5 10 15.5 12 12Z"
    return [shell(nib),
            detail(seg(7.5, 12, 11, 12)), dot(5.6, 12, 1.2),
            shell(rect(15, 3.5, 6.5, 17, min(S.R, 1.5))),
            detail(seg(15, 9.2, 21.5, 9.2)), detail(seg(15, 14.8, 21.5, 14.8)),
            detail(seg(18.2, 3.5, 18.2, 9.2)), detail(seg(18.2, 14.8, 18.2, 20.5))]


def quill(S, shift=(0, 0)):
    dx, dy = shift
    return [shell(f"M{fmt(21.5+dx)} {fmt(2.5+dy)}C{fmt(16+dx)} {fmt(3+dy)} {fmt(11.5+dx)} {fmt(6.5+dy)} {fmt(11+dx)} {fmt(12.5+dy)}"
                  f"C{fmt(17+dx)} {fmt(12+dy)} {fmt(21+dx)} {fmt(8+dy)} {fmt(21.5+dx)} {fmt(2.5+dy)}Z"),
            line(seg(20+dx, 4+dy, 8+dx, 16+dy))]


@icon("pen-name", CAT, "Quill pen crossing in front of a small domino eye mask.",
      tags=["pen name", "pseudonym", "alias", "nom de plume", "anonymous author", "ghostwriter", "quill", "mask"])
def _(S):
    mask = ("M2.5 14.5C2.5 13.3 3.5 12.7 5 13C6.5 13.4 8.5 13.4 10 13C11.5 12.7 12.5 13.3 12.5 14.5"
            "C12.5 17 10.8 19 8.8 19C7.9 19 7.5 18.3 7.5 18.3C7.5 18.3 7.1 19 6.2 19C4.2 19 2.5 17 2.5 14.5Z")
    blade = "M21.5 2.5C16 3 11.5 5.5 11 11C16.5 10.5 21 8 21.5 2.5Z"
    return [shell(mask), shell(blade), line(seg(20, 4, 7, 17.5))]


@icon("style-manual", CAT, "Closed book with a large letter A on the cover and a bookmark ribbon.",
      tags=["style manual", "style guide", "brand book", "typography guide", "editorial style", "handbook", "book"])
def _(S):
    return ([shell(rect(4, 2.5, 16, 19, S.R))] +
            [detail(d) for d in gA(S, 6.5, 10, 13.5, 18, flat=0.7)] +
            [detail(poly([(15.5, 2.5), (15.5, 9), (17, 7.8), (18.5, 9), (18.5, 2.5)], r=0))])


@icon("variable-font", CAT, "Capital A above a horizontal slider with a round knob.",
      tags=["variable font", "font axis", "weight slider", "adjustable font", "opentype variations", "slider", "font"])
def _(S):
    return lines(gA(S, 6, 3, 18, 13)) + [line(seg(3, 19.5, 9.5, 19.5)), line(seg(17, 19.5, 21, 19.5)),
                                          line(circle(13.2, 19.5, 2.3))]


@icon("font-width", CAT, "Capital A with horizontal arrows pointing outward from both sides.",
      tags=["font width", "width axis", "condensed", "expanded", "stretch", "font stretch", "typography"])
def _(S):
    return (lines(gA(S, 8.5, 4.5, 15.5, 19.5, bar=15, flat=0.7)) +
            [line(seg(6, 12, 2.5, 12)), ext_arrow(S, (2.5, 12), (6, 12), 2.5),
             line(seg(18, 12, 21.5, 12)), ext_arrow(S, (21.5, 12), (18, 12), 2.5)])


@icon("optical-size", CAT, "Small bold A beside a large thin A on a shared baseline.",
      tags=["optical size", "opsz", "display size", "text size", "font axis", "size specific", "typography"])
def _(S):
    return lines(gA(S, 2, 3, 12.5, 20, flat=0.8)) + [fat(S, seg(15.3, 20, 18.4, 12.5), 3.2),
                                                     fat(S, seg(21.5, 20, 18.4, 12.5), 3.2)]


def pixel_d(rows, x0, y0, c):
    """Union of square cells (rows of '0'/'1' strings) as a single d-string."""
    from geometry import rect_d
    parts = [P(rect_d(x0 + i * c, y0 + j * c, c, c, 0)) for j, r in enumerate(rows) for i, ch in enumerate(r) if ch == "1"]
    return path_to_d(U(*parts))


@icon("font-interpolation", CAT, "Three vertical stems growing from thin to heavy above a line of end and mid points.",
      tags=["font interpolation", "interpolate", "weight blend", "master blend", "intermediate weight", "variable fonts", "morph"])
def _(S):
    return [line(seg(5, 3.5, 5, 14)), fat(S, seg(12, 3.5, 12, 14), 3.4), fat(S, seg(19, 3.5, 19, 14), 5.0),
            line(seg(6.5, 19.5, 17.5, 19.5)), line(circle(4, 19.5, 1.4)), dot(12, 19.5, 1.5), dot(20.5, 19.5, 1.5)]


@icon("pixel-font", CAT, "Capital A built from square pixel blocks on a stepped grid.",
      tags=["pixel font", "bitmap font", "pixel art", "8-bit", "retro type", "dot matrix", "blocky letters"])
def _(S):
    rows = ["01110", "10001", "10001", "11111", "10001", "10001", "10001"]
    return [shell(pixel_d(rows, 5.75, 3.2, 2.5))]


@icon("geometric-sans-font", CAT, "Lowercase a made from a perfect circle and a straight vertical stem.",
      tags=["geometric sans", "geometric typeface", "circle letter", "single storey a", "modernist type", "sans serif"])
def _(S):
    return [line(circle(9.8, 13.5, 5.5)), line(seg(15.3, 7, 15.3, 20)), line(seg(18, 20, 22, 20))][:2]


@icon("handwritten-font", CAT, "Loose handwritten letters A and a with a flowing underline swoosh.",
      tags=["handwritten font", "handwriting", "script font", "cursive", "pen lettering", "casual type", "hand drawn font"])
def _(S):
    return [line("M3 17C5 12.5 7 7.5 8.8 4C10.2 8.5 11.7 13 12.5 17"),
            line("M5.2 13.2C7 12.7 9.5 12.8 10.8 13.6"),
            line(circle(17, 12.7, 2.7)), line("M19.7 10.2C19.7 13 19.7 15 21 17"),
            line("M3 20.5C8 19.2 14 22 21 20")]


@icon("dingbat-font", CAT, "Grid of four small symbols: a star, a heart, a check mark and scissors.",
      tags=["dingbat font", "dingbats", "symbol font", "ornament font", "special characters", "glyph set"])
def _(S):
    star = poly([pt_on(7, 7.2, r, -90 + i * 36) for i, r in enumerate([4.4, 1.9] * 5)], closed=True, r=S.r * 0.3)
    heart = "M17 10.5C14 8.2 13 6.8 13 5.5C13 4.3 14 3.5 15.1 3.5C16 3.5 16.7 4 17 4.7C17.3 4 18 3.5 18.9 3.5C20 3.5 21 4.3 21 5.5C21 6.8 20 8.2 17 10.5Z"
    return [shell(star), shell(heart),
            line(poly([(3.5, 17), (6, 19.5), (10.5, 14.5)], r=S.r * 0.4)),
            line(circle(15, 19.3, 1.6)), line(circle(20.4, 19.3, 1.6)),
            line(seg(16, 17.8, 20.8, 12.8)), line(seg(19.4, 17.8, 14.6, 12.8))]


@icon("icon-font", CAT, "Tall glyph cell with a baseline guide containing a small house symbol.",
      tags=["icon font", "symbol font", "glyph cell", "ligature icons", "webfont icons", "pictogram font"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 19, min(S.R, 2))), detail(seg(4.5, 17.2, 19.5, 17.2)),
            detail(poly([(8, 11.2), (12, 7), (16, 11.2)], r=S.r * 0.5)),
            detail(poly([(9.2, 10.4), (9.2, 14), (14.8, 14), (14.8, 10.4)], r=0))]


@icon("font-fallback", CAT, "Dashed outline letter A with an arrow pointing to a solid letter A.",
      tags=["font fallback", "fallback font", "font stack", "substitute font", "backup typeface", "css font family", "replace font"])
def _(S):
    return [line(seg(1.8, 18, 2.9, 14.3)), line(seg(3.5, 12.2, 4.6, 8.5)),
            line(seg(6.4, 8.5, 7.5, 12.2)), line(seg(8.1, 14.3, 9.2, 18)),
            line(seg(10.8, 12, 12.8, 12)), ext_arrow(S, (13.8, 12), (10.8, 12), 2.2)] + \
        lines(gA(S, 15.2, 6, 22.5, 18, flat=0.7))


@icon("embedded-font", CAT, "Document page with a square badge holding the letter A on its lower right.",
      tags=["embedded font", "embed font", "font in document", "pdf fonts", "packaged font", "document font", "font license"])
def _(S):
    return [line(poly([(10, 21.5), (4.5, 21.5), (4.5, 2.5), (16.5, 2.5), (16.5, 11)], r=S.r * 0.5)),
            line(seg(8, 7, 13, 7)), line(seg(8, 11.5, 12, 11.5)),
            shell(rect(11, 13.5, 10, 8.5, min(S.R, 2)))] + [detail(d) for d in gA(S, 13.3, 15.5, 18.7, 20.3, flat=0.4)][:1]


@icon("missing-glyph", CAT, "Tall empty rectangle crossed by an X, the placeholder box for a missing character.",
      tags=["missing glyph", "tofu", "notdef", "undefined character", "placeholder box", "unsupported character", "broken text"])
def _(S):
    return [shell(rect(6, 3, 12, 18, min(S.R, 2.5))), detail(seg(6, 3, 18, 21)), detail(seg(18, 3, 6, 21))]


@icon("font-hinting", CAT, "Pixel grid with squares filled along the strokes of a capital A.",
      tags=["font hinting", "hinting", "grid fitting", "pixel snapping", "screen rendering", "rasterizer", "ttf instructions"])
def _(S):
    cells = ["010", "111", "101"]
    return [shell(rect(2.5, 2.5, 19, 19, S.R)), detail(seg(8.8, 2.5, 8.8, 21.5)), detail(seg(15.2, 2.5, 15.2, 21.5)),
            detail(seg(2.5, 8.8, 21.5, 8.8)), detail(seg(2.5, 15.2, 21.5, 15.2))] + [
        solid(rect(c - 1.5, r - 1.5, 3, 3, 0)) for j, row in enumerate(cells) for i, ch in enumerate(row)
        if ch == "1" for c, r in [((5.65, 12, 18.35)[i], (5.65, 12, 18.35)[j])]]


@icon("hand-lettering", CAT, "Brush pen drawing a swooping stroke that runs from thick to thin.",
      tags=["hand lettering", "brush lettering", "calligraphy", "brush pen", "lettering art", "swash stroke", "script"])
def _(S):
    return [line(seg(21.5, 2.5, 13.5, 10.5)), fat(S, seg(13.5, 10.5, 10.2, 13.8), 3.8),
            fat(S, "M3.5 20.5C4.8 18 7 16.5 9.6 16.4", 4.4),
            line("M10 16.3C13 16 14.5 19.5 20 18")]


@icon("swash-letter", CAT, "Capital A whose right leg sweeps into a long flourish beneath the baseline.",
      tags=["swash letter", "swash", "flourish", "ornamental capital", "calligraphic", "decorative letter", "alternate glyph"])
def _(S):
    return [line(seg(3, 17, 9.6, 3.2)),
            line("M10.4 3.4L14 12.5C15.2 16.5 14 20.6 8 20.8C6 20.9 4.5 20.2 4 19.2"),
            line(seg(5.6, 12.4, 12.4, 12.4))]


@icon("stylistic-alternates", CAT, "Double-storey lowercase a and single-storey lowercase a with a swap arrow between.",
      tags=["stylistic alternates", "alternate glyphs", "stylistic set", "ss01", "single storey a", "double storey a", "opentype feature"])
def _(S):
    return [line("M2.5 8.5C3.2 6.2 5 5.5 6.6 5.5C8.8 5.5 10 7 10 9.2V19"),
            line(ellipse(6.4, 14.8, 3.1, 3.3)),
            line(seg(11.6, 12, 12.8, 12)), ext_arrow(S, (10.8, 12), (12.8, 12), 2.2), ext_arrow(S, (13.6, 12), (11.6, 12), 2.2),
            line(ellipse(18.2, 13.8, 2.8, 3.6)), line(seg(21, 10.2, 21, 17.4))]


@icon("old-style-figures", CAT, "Digits 1, 3 and 4 with the 3 and 4 dropping below the baseline.",
      tags=["old style figures", "oldstyle numerals", "text figures", "onum", "lowercase numbers", "hanging digits", "opentype feature"])
def _(S):
    return [line(seg(4.5, 5, 4.5, 13)), line(seg(2.8, 6.6, 4.5, 5)),
            line("M9 9.3C9.4 8.4 10.6 8.2 11.6 8.5C13.4 9.2 13.4 11.6 11.4 12.6C14 12.8 14.6 16 12.6 17.6C11.5 18.4 9.8 18.4 8.8 17.4"),
            line("M20 8.5V19"), line(poly([(20, 8.5), (15.5, 15), (22, 15)], r=0))]


@icon("tabular-figures", CAT, "Two rows of digits lined up in equal-width columns.",
      tags=["tabular figures", "tabular numbers", "tnum", "monospaced digits", "aligned numbers", "number columns", "opentype feature"])
def _(S):
    out = []
    for x in (5, 12, 19):
        out += [line(seg(x, 3.5, x, 10.5)), line(seg(x - 1.7, 5.2, x, 3.5))]
        out.append(line(ellipse(x, 17, 1.6, 3.3)))
    return out


@icon("slashed-zero", CAT, "Tall oval zero with a diagonal slash through its centre.",
      tags=["slashed zero", "zero with slash", "digit zero", "zero", "monospace number", "o vs 0", "opentype feature"])
def _(S):
    return [line(rect(6, 3, 12, 18, L(S, 5, 6))), line(seg(8.5, 17, 15.5, 7))]


@icon("discretionary-ligature", CAT, "Letters s and t joined at the top by a curved connecting arc.",
      tags=["discretionary ligature", "dlig", "st ligature", "joined letters", "decorative ligature", "historical ligature", "opentype feature"])
def _(S):
    return [line("M9.6 11C8.6 9.6 7.5 9.3 6.3 9.3C4.7 9.3 3.7 10.2 3.7 11.4C3.7 12.7 5 13.1 6.3 13.5C7.6 13.9 9.2 14.4 9.2 15.8C9.2 17.2 7.8 18 6.3 18C4.9 18 3.7 17.5 3.1 16.6"),
            line(seg(16, 6, 16, 17)), line(seg(13, 10.5, 20, 10.5)),
            line("M16 17C16 18.7 17.2 19.5 19 19.5"),
            line("M6 9.3C7.5 3.5 13 2.5 16 6")]


@icon("full-width-character", CAT, "Narrow letter A beside a wide letter A that fills a square cell.",
      tags=["full width character", "fullwidth", "zenkaku", "double width", "cjk width", "square cell", "monospace cjk"])
def _(S):
    return lines(gA(S, 2, 8, 7.5, 19, flat=0.5)) + [shell(rect(10.5, 7.5, 11.5, 12, min(S.R, 2)))] + \
        [detail(d) for d in gA(S, 13, 10, 19.5, 17, flat=0.5)]


@icon("letter-ascender", CAT, "Lowercase h with the part of its stem above the x height drawn solid.",
      tags=["ascender", "letter ascender", "tall stem", "h stem", "x height", "type anatomy", "typeface parts"])
def _(S):
    return [fat(S, seg(7, 3, 7, 9.5), 4.2), line(seg(7, 9.5, 7, 21)),
            line("M7 13.5C7.5 10.8 9.8 9.5 11.8 9.5C14.5 9.5 17 11 17 14V21")]


@icon("letter-descender", CAT, "Lowercase p with the part of its stem below the baseline drawn solid.",
      tags=["descender", "letter descender", "tail stem", "p stem", "baseline", "type anatomy", "typeface parts"])
def _(S):
    return [line(seg(7, 7.5, 7, 16)), fat(S, seg(7, 16, 7, 21.5), 4.2), line(ellipse(12.5, 11.8, 5.5, 4.4))]


@icon("cap-height", CAT, "Capital H with two guide ticks and a vertical arrow measuring its height.",
      tags=["cap height", "capital height", "type measurement", "baseline to top", "vertical metric", "font metrics", "typography terms"])
def _(S):
    return [line(seg(3.5, 4, 3.5, 20)), line(seg(11, 4, 11, 20)), line(seg(3.5, 12, 11, 12)),
            line(seg(14, 4, 22, 4)), line(seg(14, 20, 22, 20)),
            line(seg(18, 6.5, 18, 17.5)), ext_arrow(S, (18, 4.8), (18, 9), 3.4), ext_arrow(S, (18, 19.2), (18, 15), 3.4)]


@icon("tittle", CAT, "Lowercase i with its dot circled by a small ring.",
      tags=["tittle", "dot of i", "i dot", "diacritic dot", "letter dot", "type anatomy", "typeface parts"])
def _(S):
    return [line(circle(12, 6, 3.4)), dot(12, 6, 1.1), line(seg(12, 13.2, 12, 21))]


@icon("letter-crossbar", CAT, "Capital A outline with only its crossbar drawn heavy.",
      tags=["crossbar", "letter crossbar", "a bar", "horizontal stroke", "type anatomy", "typeface parts", "letter parts"])
def _(S):
    d = gA(S, 3.5, 3, 20.5, 21, bar=15)
    return [line(d[0]), fat(S, seg(8.2, 15, 15.8, 15), 4.2)]


@icon("letter-apex", CAT, "Capital A with a small circle marking the pointed top where its strokes meet.",
      tags=["apex", "letter apex", "peak of letter", "a top", "type anatomy", "typeface parts", "letter parts"])
def _(S):
    d = gA(S, 4, 7, 20, 21, flat=0.8)
    return lines(d) + [line(circle(12, 6.8, 3.4))]


@icon("letter-vertex", CAT, "Capital V with a small circle marking the pointed bottom where its strokes meet.",
      tags=["vertex", "letter vertex", "point of v", "v bottom", "type anatomy", "typeface parts", "letter parts"])
def _(S):
    return [line(poly([(3.5, 3), (12, 17.5), (20.5, 3)], r=S.r)), line(circle(12, 18, 3.2))]


@icon("letter-bowl", CAT, "Lowercase b with its rounded bowl drawn heavy and its stem light.",
      tags=["bowl", "letter bowl", "b bowl", "rounded stroke", "type anatomy", "typeface parts", "letter parts"])
def _(S):
    return [line(seg(7, 3, 7, 20)), fat(S, circle(13.2, 14.3, 4.6), 4.2)]


@icon("letter-counter", CAT, "Capital O outline with the enclosed inner space filled solid.",
      tags=["counter", "letter counter", "enclosed space", "inner space", "o shape", "type anatomy", "typeface parts"])
def _(S):
    return [line(rect(4.5, 3, 15, 18, L(S, 5, 7.5))), solid(rect(9, 7.2, 6, 9.6, L(S, 2.5, 3)))]


@icon("letter-ear", CAT, "Double-storey lowercase g with the small flag at its upper right circled.",
      tags=["ear", "letter ear", "g ear", "flag of g", "type anatomy", "typeface parts", "letter parts"])
def _(S):
    return [line(ellipse(9.5, 8.5, 4, 3.6)),
            line("M7 12.3C4.5 13.5 4 16 5.5 18.2C7 20.3 10 21 13 20.5C16 20 16.5 17.5 15 15.5C14 14.3 11.5 13.6 9.5 12.1"),
            line(seg(13.5, 6.5, 16.2, 6.5)), line(circle(18.2, 6.4, 2.6))][:4]


@icon("letter-spine", CAT, "Capital S with its central diagonal stroke drawn heavy and its ends light.",
      tags=["spine", "letter spine", "s curve", "central stroke", "type anatomy", "typeface parts", "letter parts"])
def _(S):
    return [line("M16.8 6.6C16 5 14.3 3.5 12 3.5C9.3 3.5 7.3 5.3 7.3 7.5C7.3 8.6 7.6 9.4 8.2 10"),
            fat(S, "M7.8 9.6C10 11.5 14 12.5 16.2 14.4", 4.6),
            line("M15.9 14C16.5 14.8 16.8 15.6 16.8 16.4C16.8 18.6 14.8 20.5 12 20.5C9.5 20.5 7.6 19.3 6.9 17.6")]


@icon("letter-tail", CAT, "Capital Q with the short tail stroke across its bottom drawn heavy.",
      tags=["tail", "letter tail", "q tail", "cross stroke", "type anatomy", "typeface parts", "letter parts"])
def _(S):
    return [line(rect(3.5, 2.5, 15, 16.5, L(S, 5.5, 7.5))), fat(S, seg(12.5, 14.5, 21, 21), 4.2)]


def earc(cx, cy, rx, ry, a0, a1):
    """Elliptical arc d-string from angle a0 to a1 (degrees, clockwise on screen)."""
    def p(a):
        r = math.radians(a)
        return cx + rx * math.cos(r), cy + ry * math.sin(r)
    (x0, y0), (x1, y1) = p(a0), p(a1)
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 1 if a1 > a0 else 0
    return f"M{fmt(x0)} {fmt(y0)}A{fmt(rx)} {fmt(ry)} 0 {large} {sweep} {fmt(x1)} {fmt(y1)}"


@icon("letter-terminal", CAT, "Lowercase c with the end of its upper arm circled.",
      tags=["terminal", "letter terminal", "stroke end", "ball terminal", "c terminal", "type anatomy", "typeface parts"])
def _(S):
    return [line(arc(11.5, 13, 7, 38, 318)), line(circle(17.6, 8.2, 2.8))]


@icon("letter-spur", CAT, "Capital G with the small projection at its lower right circled.",
      tags=["spur", "letter spur", "g spur", "projection", "type anatomy", "typeface parts", "letter parts"])
def _(S):
    return [line(arc(10.5, 12, 7.2, 40, 322)), line(seg(10.8, 12, 17.7, 12)), line(seg(17.7, 12, 17.7, 16)),
            line(circle(17.7, 16.8, 2.9))]


@icon("letter-stem", CAT, "Lowercase l with its main vertical stroke drawn heavy and a light curved foot.",
      tags=["stem", "letter stem", "vertical stroke", "main stroke", "l stem", "type anatomy", "typeface parts"])
def _(S):
    return [fat(S, seg(10, 3.5, 10, 16.5), 4.4), line("M10 16C10 19.2 11.8 20.5 15 20.5")]


@icon("letter-shoulder", CAT, "Lowercase n with the arched curve that springs from its stem drawn heavy.",
      tags=["shoulder", "letter shoulder", "n arch", "arch stroke", "curved stroke", "type anatomy", "typeface parts"])
def _(S):
    return [line(seg(6.5, 9, 6.5, 20.5)), fat(S, "M6.5 13.8C7 11.2 9.5 9.8 12 9.8C15.2 9.8 17.5 11.5 17.5 14.5", 4.4),
            line(seg(17.5, 14.5, 17.5, 20.5))]


@icon("letter-arm", CAT, "Capital E with its top horizontal stroke drawn heavy.",
      tags=["arm", "letter arm", "horizontal arm", "e arm", "type anatomy", "typeface parts", "letter parts"])
def _(S):
    return [line(poly([(18, 4), (7, 4), (7, 20), (18, 20)], r=S.r * 0.5)), line(seg(7, 12, 15, 12)),
            fat(S, seg(7, 4, 18, 4), 4.2)]


@icon("letter-leg", CAT, "Capital R with its diagonal lower stroke drawn heavy.",
      tags=["leg", "letter leg", "r leg", "diagonal stroke", "type anatomy", "typeface parts", "letter parts"])
def _(S):
    return [line(seg(6.5, 3.5, 6.5, 20.5)), line("M6.5 3.5H12.5A4.5 4.5 0 0 1 12.5 12.5H6.5"),
            fat(S, seg(11.3, 12.5, 18.5, 20.5), 4.2)]


@icon("letter-loop", CAT, "Double-storey lowercase g with its closed lower loop below the baseline drawn heavy.",
      tags=["loop", "letter loop", "g loop", "lower bowl", "closed loop", "type anatomy", "typeface parts"])
def _(S):
    return [line(ellipse(11.5, 7.5, 4, 3.4)), line(seg(15.5, 6.2, 18.5, 6.2)), line(seg(11.5, 10.9, 11.5, 14)),
            fat(S, ellipse(11.5, 17.6, 5.5, 3.2), 3.4)]


@icon("letter-overshoot", CAT, "Round letter O rising above and dipping below a flat H beside it.",
      tags=["overshoot", "letter overshoot", "round letter", "optical correction", "baseline overshoot", "type anatomy", "typeface parts"])
def _(S):
    return [line(seg(3.5, 6.5, 3.5, 17.5)), line(seg(9.5, 6.5, 9.5, 17.5)), line(seg(3.5, 12, 9.5, 12)),
            line(ellipse(17, 12, 4.5, 7.3))]


@icon("stroke-contrast", CAT, "Letter O with thick sides and thin top and bottom.",
      tags=["stroke contrast", "contrast", "thick and thin", "high contrast type", "didone", "type anatomy", "typeface parts"])
def _(S):
    return [line(earc(12, 12, 6.8, 8.5, 218, 322)), line(earc(12, 12, 6.8, 8.5, 38, 142)),
            fat(S, earc(12, 12, 6.8, 8.5, 128, 232), 4.6), fat(S, earc(12, 12, 6.8, 8.5, -52, 52), 4.6)]


@icon("stress-axis", CAT, "Letter O with uneven stroke weight and a tilted dashed line through its thinnest points.",
      tags=["stress axis", "stress", "tilted axis", "slanted stress", "oblique stress", "type anatomy", "typeface parts"])
def _(S):
    return [line(earc(12, 12, 8, 9, 18, 142)), line(earc(12, 12, 8, 9, 198, 322)),
            fat(S, earc(12, 12, 8, 9, -52, 30), 3.8), fat(S, earc(12, 12, 8, 9, 128, 212), 3.8),
            line(seg(10.8, 8, 11.4, 10.6)), line(seg(12.6, 13.4, 13.2, 16))]


@icon("ink-trap", CAT, "Thick corner junction of two strokes with a small wedge notch cut into the inside corner.",
      tags=["ink trap", "ink traps", "notch", "junction cut", "print compensation", "type anatomy", "typeface parts"])
def _(S):
    return [shell(poly([(3.5, 3.5), (10.5, 3.5), (10.5, 12), (6.8, 17.4), (12.6, 14), (20.5, 14), (20.5, 20.5), (3.5, 20.5)],
                       closed=True, r=S.r * 0.5))]


@icon("em-square", CAT, "Square frame holding a letter A that stands on a baseline guide.",
      tags=["em square", "em box", "units per em", "glyph box", "type design grid", "font metrics", "typography terms"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(seg(3, 17, 21, 17))] + [detail(d) for d in gA(S, 7.5, 6.5, 16.5, 17, flat=0.7)]


@icon("advance-width", CAT, "Letter n between two side ticks with a dimension arrow spanning the full width below.",
      tags=["advance width", "glyph width", "sidebearing", "character width", "horizontal metrics", "font metrics", "typography terms"])
def _(S):
    return [line(seg(3.5, 3, 3.5, 15)), line(seg(20.5, 3, 20.5, 15)),
            line(seg(8.5, 6.5, 8.5, 13.5)), line("M8.5 9.3C9 7.7 10.2 7 11.7 7C13.8 7 15.5 8 15.5 10V13.5"),
            line(seg(6, 19.5, 18, 19.5)), ext_arrow(S, (3.5, 19.5), (7, 19.5), 3.0), ext_arrow(S, (20.5, 19.5), (17, 19.5), 3.0)]


@icon("vertical-metrics", CAT, "Capital H and a lowercase p beside a ruler with four ticks for cap, x height, baseline and descender.",
      tags=["vertical metrics", "font metrics", "ascent descent", "line height", "x height", "baseline", "typography terms"])
def _(S):
    return [line(seg(3, 4, 3, 16)), line(seg(8, 4, 8, 16)), line(seg(3, 10, 8, 10)),
            line(seg(12, 9, 12, 21)), line(ellipse(15, 12.7, 2.6, 3.3)),
            line(seg(21, 4, 21, 21)), line(seg(18.5, 4, 21, 4)), line(seg(18.5, 9, 21, 9)),
            line(seg(18.5, 16, 21, 16)), line(seg(18.5, 21, 21, 21))]


@icon("word-spacing", CAT, "Two word blocks on a line with a two-headed arrow in the gap between them.",
      tags=["word spacing", "word gap", "space between words", "interword space", "tracking", "text spacing", "typography terms"])
def _(S):
    return [shell(rect(2.5, 5, 5.5, 14, min(S.R, 2))), shell(rect(16, 5, 5.5, 14, min(S.R, 2))),
            line(seg(10.8, 12, 13.2, 12)), ext_arrow(S, (10, 12), (12, 12), 2.0), ext_arrow(S, (14, 12), (12, 12), 2.0)]


@icon("baseline-shift", CAT, "Capital A beside a smaller raised letter a with a short up arrow beneath it.",
      tags=["baseline shift", "raised text", "superscript offset", "vertical offset", "text rise", "character offset", "typography terms"])
def _(S):
    return lines(gA(S, 2, 6, 11, 19.5, flat=0.7)) + [
        line(ellipse(17.5, 9.8, 2.4, 2.6)), line(seg(19.9, 7.2, 19.9, 12.4)),
        line(seg(17.5, 20.5, 17.5, 16.5)), ext_arrow(S, (17.5, 15.2), (17.5, 19), 2.6)]


@icon("hanging-punctuation", CAT, "Left-aligned text lines with an opening quotation mark sitting outside the left edge.",
      tags=["hanging punctuation", "optical margin alignment", "quote mark outside", "margin hang", "typesetting", "text alignment", "quotation"])
def _(S):
    return [line(seg(3, 7.5, 4.3, 3.5)), line(seg(6, 7.5, 7.3, 3.5)),
            line(seg(10, 5, 21, 5)), line(seg(10, 10, 21, 10)), line(seg(10, 15, 21, 15)), line(seg(10, 20, 17, 20))]


@icon("first-line-indent", CAT, "Paragraph whose first line starts further in, marked by a small arrow.",
      tags=["first line indent", "paragraph indent", "indentation", "indent first line", "paragraph spacing", "text format", "typesetting"])
def _(S):
    return [line(seg(2.5, 5, 5.5, 5)), ext_arrow(S, (8, 5), (5, 5), 2.4),
            line(seg(11.5, 5, 21.5, 5)), line(seg(2.5, 10, 21.5, 10)), line(seg(2.5, 15, 21.5, 15)), line(seg(2.5, 20, 15, 20))]


@icon("hanging-indent", CAT, "Paragraph with the first line flush left and the lines below it indented.",
      tags=["hanging indent", "reverse indent", "bibliography indent", "indentation", "paragraph format", "text format", "typesetting"])
def _(S):
    return [line(seg(2.5, 5, 21.5, 5)), line(seg(8.5, 10, 21.5, 10)), line(seg(8.5, 15, 21.5, 15)), line(seg(8.5, 20, 17, 20)),
            line(seg(2.5, 12.5, 2.5, 17.5))][:4]


@icon("non-breaking-space", CAT, "Letters a and b joined by a small upturned arc bridging the space between them.",
      tags=["non breaking space", "nbsp", "no break space", "hard space", "keep together", "glue words", "whitespace"])
def _(S):
    return [line(ellipse(5.5, 11.2, 2.6, 3.6)), line(seg(8.1, 7.6, 8.1, 14.8)),
            line(ellipse(18.5, 11.2, 2.6, 3.6)), line(seg(15.9, 4, 15.9, 14.8)),
            line("M5.5 18.5C5.5 21.8 18.5 21.8 18.5 18.5")]
