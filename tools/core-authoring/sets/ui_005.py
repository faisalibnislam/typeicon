"""TypeIcon Core: ui (batch ui_005): text styling, rulers, dialogs, keyboards, buttons and input fields."""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, I, P, ST, U, Part, Style, arc, circle, detail, dot, ellipse, filled_region, fmt, icon, line, path_to_d, poly,
    rect, regular, seg, shell, solid,
)

CAT = "ui"
FILL = Style("filled", "butt", "miter", R=2.0, r=0.0)  # pseudo-style: parts for the Filled design


def isF(S) -> bool:
    return S.name == "filled"


def isL(S) -> bool:
    return S.name != "rounded"


def ui(name, description, tags, aliases=()):
    """Register a ui icon whose Filled design is built from `fn(FILL)`."""
    def deco(fn):
        return icon(name, CAT, description, tags=tags, aliases=aliases, filled=lambda: filled_region(fn(FILL)))(fn)
    return deco


# --------------------------------------------------------------------------- helpers

def pip(S, x, y, r=1.75, grow=0.5):
    """Small solid mark: square in Line, disc in Rounded, larger disc in Filled."""
    if isF(S):
        return Part("dot", circle(x, y, r + grow))
    if S.name == "line":
        s = r * 0.9
        return Part("dot", rect(x - s, y - s, 2 * s, 2 * s))
    return Part("dot", circle(x, y, r))


def blk(S, x, y, w, h, k=1.0):
    """Small solid block (knocked out of a Filled shell): square corners in Line, rounded in Rounded."""
    return Part("dot", rect(x, y, w, h, 0 if isL(S) else min(k, w / 2, h / 2)))


def frame(S):
    return shell(rect(3, 3, 18, 18, S.R))


def win(S, y0=4.0, h=16.0):
    return shell(rect(3, y0, 18, h, S.R))


def phone(S):
    return shell(rect(5, 2, 14, 20, S.R * 0.75))


def tile(S, x, y, w, h):
    return shell(rect(x, y, w, h, S.R * 0.5))


def chev(S, cx, cy, w=3.0, h=None, deg=90, kind=line):
    """Open chevron centred on (cx, cy): half-width w (across), depth h (along `deg`)."""
    h = w if h is None else h
    a = math.radians(deg)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    tip = (cx + ux * h / 2, cy + uy * h / 2)
    b = (cx - ux * h / 2, cy - uy * h / 2)
    return kind(poly([(b[0] + nx * w, b[1] + ny * w), tip, (b[0] - nx * w, b[1] - ny * w)], r=S.r))


def dashed_rect(S, x, y, w, h, kind=line, dash=4.0):
    """Rectangle drawn as corner Ls plus one centred dash per long side (gaps >= 2 px in every style)."""
    trim = 0 if isL(S) else 0.75
    arm_w = (w - dash) / 2 - 3.5 / 2 if w > 10 else w / 2 - 1.75
    arm_h = (h - dash) / 2 - 3.5 / 2 if h > 10 else h / 2 - 1.75
    x1, y1 = x + w, y + h
    parts = []
    for cx, cy, sx, sy in ((x, y, 1, 1), (x1, y, -1, 1), (x1, y1, -1, -1), (x, y1, 1, -1)):
        parts.append(kind(poly([(cx, cy + sy * (arm_h - trim)), (cx, cy), (cx + sx * (arm_w - trim), cy)], r=S.r)))
    if w > 10:
        mx = x + w / 2
        for yy in (y, y1):
            parts.append(kind(seg(mx - dash / 2 + trim, yy, mx + dash / 2 - trim, yy)))
    if h > 10:
        my = y + h / 2
        for xx in (x, x1):
            parts.append(kind(seg(xx, my - dash / 2 + trim, xx, my + dash / 2 - trim)))
    return parts


def pt(cx, cy, r, deg):
    a = math.radians(deg)
    return (cx + r * math.cos(a), cy + r * math.sin(a))


def I_(a, b):
    return I(a, b)


def arrow_head(S, tip, deg, size=3.0, kind=line):
    """Open arrowhead whose tip points along `deg` (0 = right, 90 = down)."""
    a = math.radians(deg)
    pts = []
    for s in (135, -135):
        b = a + math.radians(s)
        pts.append((tip[0] + size * math.cos(b), tip[1] + size * math.sin(b)))
    return kind(poly([pts[0], tip, pts[1]], r=S.r))


def star_d(cx, cy, ro, ri=None):
    ri = ro * 0.45 if ri is None else ri
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        r = ro if i % 2 == 0 else ri
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return poly(pts, closed=True)


# =========================================================================== chunk 1: prompts, pages and text styles

@ui("grid-overlay", "Photo frame split into nine parts by two vertical and two horizontal guide lines.",
    ["rule of thirds", "composition grid", "camera grid", "guides", "photo", "crop guides", "viewfinder"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)),
            detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)),
            detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15)),
            pip(S, 12, 12, 1.5, 0.5)]


@ui("rating-prompt", "Dialog card with a row of three stars and two buttons beneath.",
    ["rate us", "rate this app", "review prompt", "star rating", "feedback dialog", "app rating", "popup"])
def _(S):
    return [shell(rect(2, 3, 20, 18, S.R)),
            Part("dot", star_d(7, 8.5, 2.3)), Part("dot", star_d(12, 8.5, 2.3)), Part("dot", star_d(17, 8.5, 2.3)),
            blk(S, 5, 14.5, 6, 3.5, 1), blk(S, 13, 14.5, 6, 3.5, 1)]


@ui("feedback-tab", "Page with a narrow tab on its right edge holding a speech bubble mark.",
    ["feedback button", "side tab", "feedback widget", "give feedback", "comment tab", "survey", "support"])
def _(S):
    return [shell(rect(3, 3, 13, 18, S.R)), shell(rect(16, 8, 5, 9, S.R * 0.5)),
            detail(seg(6.5, 8, 12.5, 8)), detail(seg(6.5, 12, 12.5, 12)), detail(seg(6.5, 16, 10, 16)),
            pip(S, 18.5, 12.5, 1.0, 0.0)]


@ui("loading-overlay", "Card covered by hatching with a small spinner arc at its centre.",
    ["busy overlay", "blocking loader", "loading screen", "please wait", "spinner", "disabled content", "scrim"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)),
            detail(seg(6, 9.5, 9.5, 6)), detail(seg(14.5, 18, 18, 14.5)),
            detail(arc(12, 12, 3.5, -45, 225))]


@ui("stacked-toasts", "Three toast notifications stacked with the newest bar in front.",
    ["toast", "snackbar", "notifications", "stack", "alerts", "messages queue", "toasts"])
def _(S):
    return [line(seg(9, 6.5, 15, 6.5)), line(seg(6, 10.5, 18, 10.5)),
            shell(rect(3, 14, 18, 7, S.R * 0.75)),
            pip(S, 6.5, 17.5, 1.1, 0.1), detail(seg(10, 17.5, 17.5, 17.5))]


@ui("resize-grip", "Square corner with three short diagonal grip lines of decreasing length.",
    ["resize handle", "drag corner", "window corner", "textarea resize", "grip", "resizer", "size grip"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)),
            detail(seg(16, 17.5, 17.5, 16)), detail(seg(11.5, 17.5, 17.5, 11.5)), detail(seg(7.5, 17, 17, 7.5))]


@ui("frosted-glass", "Rounded translucent card laid over a circle that shows through softly.",
    ["glassmorphism", "blur", "translucent", "acrylic", "backdrop blur", "glass effect", "frosted"])
def _(S):
    card = rect(9, 8, 12, 13, S.R + 1)
    ring = D(ST(circle(8, 9, 5.5), 2, "butt", "miter", 4), P(rect(7, 6, 16, 17, S.R + 2)))
    return [solid(path_to_d(ring)), shell(card), detail(seg(12.5, 17, 17.5, 12))]


@ui("permission-prompt", "Address bar with a small popup card hanging from it holding text and two buttons.",
    ["permission request", "allow block", "site permission", "browser popup", "camera permission", "ask to allow", "consent"])
def _(S):
    return [shell(rect(3, 2.5, 18, 5, S.R * 0.6)), pip(S, 6.5, 5, 1, 0),
            shell(rect(5, 10, 14, 11, S.R * 0.75)), detail(seg(8, 13.5, 16, 13.5)),
            blk(S, 8, 16, 3.5, 2.5, 0.6), blk(S, 12.5, 16, 3.5, 2.5, 0.6)]


@ui("page-numbers", "Page with text lines and a numeral one centred at its bottom edge.",
    ["page number", "footer number", "numbering", "insert page number", "document footer", "pagination", "folio"])
def _(S):
    return [shell(rect(5, 2, 14, 20, S.R * 0.75)),
            detail(seg(8, 6.5, 16, 6.5)), detail(seg(8, 10, 16, 10)),
            detail(poly([(10.5, 15.5), (12.5, 14), (12.5, 19.5)], r=S.r))]


@ui("page-header-footer", "Page with a solid band at its top and another at its bottom around the body text.",
    ["header and footer", "running header", "page margins", "document header", "footer", "letterhead", "edit header"])
def _(S):
    return [shell(rect(5, 2, 14, 20, S.R * 0.75)),
            blk(S, 7.5, 4.5, 9, 2.5, 0.5), blk(S, 7.5, 17, 9, 2.5, 0.5),
            detail(seg(8, 10.5, 16, 10.5)), detail(seg(8, 13.5, 14, 13.5))]


@ui("watermark", "Page with a wide diagonal stripe laid across its text lines.",
    ["draft stamp", "confidential", "background text", "document watermark", "overlay text", "page stamp", "brand stamp"])
def _(S):
    from geometry import transform_path, rotation
    sp = transform_path(P(rect(6, 10.5, 12, 3.5, 0)), rotation(-40, 12, 12))
    return [shell(rect(5, 2, 14, 20, S.R * 0.75)),
            detail(seg(8, 6, 14, 6)), detail(seg(10, 19, 16, 19)),
            Part("dot", path_to_d(sp))]


@ui("hyphenation", "Lines of text where the top line ends with a short hyphen breaking a word.",
    ["hyphen", "word break", "split word", "auto hyphenate", "line break", "justify text", "typography"])
def _(S):
    return [line(seg(3, 6, 15, 6)), line(seg(18, 6, 21, 6)),
            line(seg(3, 11, 8, 11)), line(seg(11, 11, 21, 11)),
            line(seg(3, 16, 21, 16)), line(seg(3, 20.5, 14, 20.5))]


@ui("outlined-text", "Capital letter A drawn as a hollow outline.",
    ["text outline", "stroke text", "hollow letter", "outline font", "text stroke", "letter outline", "typography"])
def _(S):
    return [shell(poly([(2, 21), (9.5, 3), (14.5, 3), (22, 21), (16.5, 21), (15.4, 18), (8.6, 18), (7.5, 21)],
                       closed=True, r=S.r * 0.6)),
            detail(poly([(9.8, 14), (12, 8), (14.2, 14)], closed=True, r=S.r * 0.3))]


@ui("text-shadow", "Capital letter A with a solid copy offset behind it to the lower right.",
    ["drop shadow", "text effect", "shadow text", "letter shadow", "typography", "emboss", "depth"])
def _(S):
    front = [(2.5, 17), (7.5, 4.5), (12.5, 17)]
    back = [(p[0] + 5, p[1] + 3.5) for p in front]
    fd = poly(front, r=S.r) + seg(4.5, 12.5, 10.5, 12.5)
    bd = poly(back, r=S.r) + seg(9.5, 16, 15.5, 16)
    shadow = D(ST(bd, 3.0, "butt", "miter", 4), ST(fd, 5.2, "butt", "miter", 4))
    return [line(poly(front, r=S.r)), line(seg(4.5, 12.5, 10.5, 12.5)), solid(path_to_d(shadow))]


# =========================================================================== chunk 2: typography, rulers, documents

def rotp(pts, deg, cx, cy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


@ui("small-caps", "A tall capital A followed by two shorter capitals of equal small height.",
    ["small capitals", "smallcaps", "font variant", "typography", "uppercase small", "text style", "letter case"])
def _(S):
    return [line(poly([(2.5, 19), (6, 5), (9.5, 19)], r=S.r)), line(seg(4, 14, 8, 14)),
            line(seg(11.5, 12, 16, 12)), line(seg(13.75, 12, 13.75, 19)),
            line(seg(18, 12, 22, 12)), line(seg(20, 12, 20, 19))]


@ui("indent-markers", "Ruler with an hourglass marker of two small triangles at its left end.",
    ["ruler", "indent", "paragraph indent", "hanging indent", "margin marker", "text ruler", "first line indent"])
def _(S):
    return [line(seg(3, 6, 21, 6)), line(seg(13, 6, 13, 9)), line(seg(18, 6, 18, 9)),
            solid(poly([(3.5, 10), (10, 10), (6.75, 14.2)], closed=True, r=S.r * 0.5)),
            solid(poly([(3.5, 21), (10, 21), (6.75, 16.8)], closed=True, r=S.r * 0.5))]


@ui("tab-stops", "Ruler with two small L shaped markers standing on its tick marks.",
    ["tab stop", "tab ruler", "left tab", "text ruler", "tabulation", "align text", "ruler tabs"])
def _(S):
    return [line(seg(3, 18, 21, 18)), line(seg(6, 18, 6, 21)), line(seg(10.5, 18, 10.5, 20)),
            line(seg(15, 18, 15, 21)), line(seg(19.5, 18, 19.5, 20)),
            line(poly([(6, 4), (6, 14), (11, 14)], r=S.r)), line(poly([(15, 4), (15, 14), (20, 14)], r=S.r))]


@ui("read-aloud", "Lines of text with a small speaker giving off sound waves at the right.",
    ["text to speech", "tts", "narrate", "listen", "speak text", "audio reading", "screen reader"])
def _(S):
    return [line(seg(3, 6, 9, 6)), line(seg(3, 12, 9, 12)), line(seg(3, 18, 8, 18)),
            shell(poly([(11.5, 10), (13.5, 10), (16.5, 7.5), (16.5, 16.5), (13.5, 14), (11.5, 14)], closed=True,
                       r=S.r * 0.4)),
            line(arc(16.5, 12, 3.3, -50, 50)), line(arc(16.5, 12, 6, -50, 50))]


@ui("line-focus", "Faint lines of text above and below one line framed by a highlight band.",
    ["reading ruler", "focus line", "reading guide", "highlight line", "line spotlight", "dyslexia", "reading mode"])
def _(S):
    return [line(seg(4, 4.5, 20, 4.5)), line(seg(4, 19.5, 20, 19.5)),
            shell(rect(2, 8, 20, 8, S.R * 0.75)), detail(seg(6, 12, 18, 12))]


@ui("remove-duplicates", "Two identical table rows with the lower one struck through.",
    ["deduplicate", "dedupe", "unique rows", "delete duplicates", "spreadsheet", "clean data", "repeated rows"])
def _(S):
    return [shell(rect(3, 3, 18, 7, S.R * 0.6)), detail(seg(9, 3, 9, 10)),
            shell(rect(3, 14, 18, 7, S.R * 0.6)), detail(seg(6, 19, 18, 16))]


@ui("cell-dropdown", "Table cell with a caret button at its right edge and a short list beneath.",
    ["dropdown cell", "select cell", "data validation", "cell menu", "spreadsheet list", "picklist", "choice cell"])
def _(S):
    return [shell(rect(2, 3, 20, 9, S.R * 0.6)), detail(seg(16, 3, 16, 12)),
            chev(S, 19, 7.5, w=2.2, h=2.2, deg=90, kind=detail), detail(seg(5, 7.5, 12, 7.5)),
            line(seg(4, 16, 16, 16)), line(seg(4, 20, 11, 20))]


@ui("sheet-tabs", "Spreadsheet grid above a row of three tabs, the first one solid.",
    ["worksheet tabs", "sheets", "workbook", "spreadsheet tabs", "switch sheet", "excel tabs", "pages bar"])
def _(S):
    return [shell(rect(3, 3, 18, 12, S.R * 0.75)), detail(seg(9, 3, 9, 15)), detail(seg(15, 3, 15, 15)),
            detail(seg(3, 9, 21, 9)),
            Part("solid", rect(3, 17.5, 5.5, 3.5, 0 if isL(S) else 1.2)),
            line(seg(11, 19.25, 15, 19.25)), line(seg(17.5, 19.25, 21, 19.25))]


@ui("rotate-text", "Capital letter A tilted at an angle with a curved arrow arcing beside it.",
    ["text rotation", "angle text", "tilt text", "orientation", "turn text", "slanted text", "spin text"])
def _(S):
    pts = rotp([(3.5, 19), (8.5, 6), (13.5, 19)], -28, 9, 12)
    bar = rotp([(5.5, 14.5), (11.5, 14.5)], -28, 9, 12)
    return [line(poly(pts, r=S.r)), line(seg(*bar[0], *bar[1])),
            line(arc(10, 12, 11, -40, 40)),
            arrow_head(S, pt(10, 12, 11, 40), 130, 3.0)]


@ui("slide-transition", "Two slides side by side with a curved arrow arcing from the first to the second.",
    ["slide change", "presentation transition", "next slide", "slideshow", "animation between slides", "powerpoint", "keynote"])
def _(S):
    return [shell(rect(2, 14, 8.5, 7, S.R * 0.6)), shell(rect(13.5, 14, 8.5, 7, S.R * 0.6)),
            line(arc(12, 12, 7.5, -160, -25)),
            arrow_head(S, pt(12, 12, 7.5, -25), 65, 3.0)]


@ui("presentation-handout", "Page with three small slide thumbnails stacked on its left and text lines beside each.",
    ["handout", "slide handout", "notes page", "print slides", "slides per page", "presentation print", "lecture notes"])
def _(S):
    out = [shell(rect(3, 2, 18, 20, S.R * 0.75))]
    for y in (5, 10, 15):
        out += [blk(S, 5.5, y, 6, 4, 0.8), detail(seg(14, y + 2, 18, y + 2))]
    return out


def ptr_pts(x, y, s):
    base = [(0, 0), (0, 13), (3.3, 10), (5.6, 15), (8, 14), (5.7, 9), (9.8, 8.6)]
    return [(x + px * s, y + py * s) for px, py in base]


@ui("cursor-chat", "Arrow pointer with a small speech bubble attached at its lower right.",
    ["cursor message", "chat with cursor", "collaboration cursor", "live cursor", "multiplayer comment", "say something", "pointer chat"])
def _(S):
    return [shell(poly(ptr_pts(3, 2.5, 0.8), closed=True, r=S.r * 0.4)),
            shell(poly([(12.5, 12.5), (22, 12.5), (22, 19.5), (17, 19.5), (13.5, 22), (13.5, 19.5), (12.5, 19.5)],
                       closed=True, r=S.R * 0.5)),
            pip(S, 17.25, 16, 1.0, 0.0)]


@ui("alpha-slider", "Slider bar with checkerboard squares on the left and a round handle.",
    ["opacity slider", "transparency", "alpha channel", "color opacity", "checkerboard", "color picker", "opacity control"])
def _(S):
    return [shell(rect(2, 8, 20, 8, S.R * 0.9)),
            blk(S, 4.5, 9.9, 2.3, 2.3, 0.3), blk(S, 6.8, 12.2, 2.3, 2.3, 0.3), blk(S, 9.1, 9.9, 2.3, 2.3, 0.3),
            pip(S, 16, 12, 2.4, 0.2)]


@ui("gradient-stops", "Gradient bar with fading blocks above three pointed stop markers.",
    ["gradient editor", "color stops", "gradient slider", "color ramp", "gradient bar", "blend", "fade"])
def _(S):
    out = [shell(rect(2, 3, 20, 9, S.R * 0.75)),
           blk(S, 4.5, 5.5, 3.5, 4, 0.3), blk(S, 10.2, 5.5, 2.5, 4, 0.3), blk(S, 15.5, 5.5, 1.5, 4, 0.3)]
    for cx in (4.5, 12, 19.5):
        out.append(shell(poly([(cx - 2.5, 21), (cx - 2.5, 17), (cx, 14.5), (cx + 2.5, 17), (cx + 2.5, 21)],
                              closed=True, r=S.r * 0.5)))
    return out


# =========================================================================== chunk 3: editors, dialogs, keyboards, buttons

@ui("node-editor", "Two rounded boxes with socket dots on their edges joined by a curved wire.",
    ["node graph", "visual programming", "blueprint", "flow editor", "connect nodes", "shader graph", "wire nodes"])
def _(S):
    return [shell(rect(2, 3.5, 8, 7, S.R * 0.6)), shell(rect(14, 13.5, 8, 7, S.R * 0.6)),
            line("M10 7C13 7 11 17 14 17"),
            Part("solid", circle(10, 7, 1.7)), Part("solid", circle(14, 17, 1.7))]


@ui("step-sequencer", "Four by four grid of small squares with a scattered pattern of solid squares.",
    ["drum machine", "beat grid", "pattern sequencer", "music steps", "sequencer", "beat maker", "tracker"])
def _(S):
    on = {(0, 0), (3, 0), (1, 1), (2, 2), (0, 3), (2, 3)}
    out = []
    sz = 3.6 if isF(S) else 3.2
    r = 1.1 if isF(S) else 0.85
    for j in range(4):
        for i in range(4):
            cx, cy = 4.5 + i * 5, 4.5 + j * 5
            if (i, j) in on:
                out.append(Part("solid", rect(cx - sz / 2, cy - sz / 2, sz, sz, 0 if isL(S) else 1.4)))
            else:
                out.append(Part("solid", circle(cx, cy, r) if not isL(S) else rect(cx - r, cy - r, 2 * r, 2 * r)))
    return out


@ui("level-meter", "Two columns of stacked short bars, one taller than the other, like an audio level meter.",
    ["vu meter", "audio level", "volume meter", "equalizer bars", "sound level", "signal level", "peak meter"])
def _(S):
    out = []
    for k, y in enumerate((4.5, 8.5, 12.5, 16.5, 20.5)):
        out.append(line(seg(3.5, y, 10, y)))
        if k >= 2:
            out.append(line(seg(14, y, 20.5, y)))
    return out


@ui("transform-origin", "Square with a circled crosshair at its middle and short guide ticks from each edge.",
    ["pivot point", "anchor point", "origin point", "center point", "rotation origin", "transform center", "registration"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(circle(12, 12, 2.4)),
            detail(seg(3, 12, 6.5, 12)), detail(seg(17.5, 12, 21, 12)),
            detail(seg(12, 3, 12, 6.5)), detail(seg(12, 17.5, 12, 21))]


@ui("arrange-in-grid", "Scattered small squares on the left and the same squares in a neat grid on the right joined by an arrow.",
    ["auto arrange", "snap to grid", "tidy up", "align items", "organize", "sort icons", "grid layout"])
def _(S):
    sq_ = 3.0
    out = []
    for x, y in ((2.5, 3.5), (5.5, 10.5), (2.5, 17)):
        out.append(Part("solid", rect(x, y, sq_, sq_, 0 if isL(S) else 0.7)))
    for x in (15.5, 19.5):
        for y in (8.5, 12.5):
            out.append(Part("solid", rect(x, y, sq_, sq_, 0 if isL(S) else 0.7)))
    out += [line(seg(8.5, 12, 12.5, 12)), arrow_head(S, (12.8, 12), 0, 2.2)]
    return out


@ui("text-on-path", "Three small letters standing along a curved line.",
    ["type on a path", "curved text", "text along curve", "arc text", "wavy text", "text curve", "warp text"])
def _(S):
    glyphs = [[[(-1.6, 5), (-1.6, 0), (1.8, 0)]],
              [[(-2.2, 5), (2.2, 5)], [(0, 5), (0, 0)]],
              [[(-2.2, 5), (0, 0), (2.2, 5)]]]
    out = [line(arc(12, 24, 11.2, -140, -40))]
    for a, strokes in zip((-114, -90, -66), glyphs):
        ux, uy = math.cos(math.radians(a)), math.sin(math.radians(a))
        tx, ty = -uy, ux
        base = 14.6
        for st in strokes:
            pts = [(12 + ux * (base + v) + tx * u, 24 + uy * (base + v) + ty * u) for u, v in st]
            out.append(line(poly(pts, r=S.r * 0.4)))
    return out


@ui("glyphs-panel", "Panel split into four cells each holding a different letter or symbol.",
    ["special characters", "character map", "symbols picker", "glyph palette", "insert symbol", "unicode", "font glyphs"])
def _(S):
    return [shell(rect(2, 2, 20, 20, S.R)), detail(seg(12, 2, 12, 22)), detail(seg(2, 12, 22, 12)),
            detail(poly([(4.5, 9.8), (7, 4.5), (9.5, 9.8)], r=0)), detail(seg(5.4, 8, 8.6, 8)),
            Part("dot", star_d(17, 7.2, 2.7)), Part("dot", circle(7, 17, 2.0)) if False else Part("dot", rect(5.5, 15.5, 3, 3, 0 if isL(S) else 0.8)),
            detail(seg(15.5, 17, 18.5, 17)), detail(seg(17, 15.5, 17, 18.5))]


@ui("file-dialog", "Dialog window with a folder list, a file name field and a solid button at the bottom right.",
    ["open file", "save as", "file picker", "choose file", "browse files", "file chooser", "upload dialog"])
def _(S):
    return [shell(rect(2, 3, 20, 18, S.R * 0.75)), detail(seg(2, 7, 22, 7)),
            detail(seg(5, 10.5, 12, 10.5)), detail(seg(5, 13.5, 10, 13.5)),
            detail(seg(5, 17.5, 13, 17.5)), blk(S, 15.5, 15.5, 4.5, 3.5, 0.7)]


@ui("progress-dialog", "Dialog card with a title line, a partly filled progress bar and a small cancel button.",
    ["progress window", "copying files", "installing", "please wait dialog", "task progress", "download progress", "loading dialog"])
def _(S):
    return [shell(rect(2, 4, 20, 16, S.R * 0.75)), detail(seg(5, 8, 12, 8)),
            blk(S, 5, 10.5, 8, 2.6, 0.5), detail(seg(15.5, 11.8, 19, 11.8)),
            blk(S, 13.5, 15, 5.5, 2.5, 0.6)]


@ui("charge-limit", "Horizontal battery filled most of the way with a dashed stop line near its end.",
    ["battery limit", "charge cap", "stop charging at 80", "battery health", "optimized charging", "limit charge", "battery protection"])
def _(S):
    return [shell(rect(2, 7, 17, 10, S.R * 0.9)), Part("solid", rect(19.5, 10, 2.5, 4, 0.5 if not isL(S) else 0)),
            blk(S, 4.5, 9.5, 9, 5, 0.5), detail(seg(15.5, 9, 15.5, 15)),
            line(seg(15.5, 2.5, 15.5, 4.2)), line(seg(15.5, 19.8, 15.5, 21.5))]


@ui("wifi-calling", "Wifi signal arcs above a telephone handset.",
    ["voip", "call over wifi", "wifi phone", "internet calling", "wireless call", "wi-fi calling", "voice over wifi"])
def _(S):
    return [line(arc(12, 12.5, 4, -135, -45)), line(arc(12, 12.5, 8.2, -135, -45)), pip(S, 12, 12, 1.3, 0.2),
            line("M6.5 18.5Q12 13.5 17.5 18.5"),
            Part("solid", rect(3.5, 17.5, 5, 3.5, 0 if isL(S) else 1.2)), Part("solid", rect(15.5, 17.5, 5, 3.5, 0 if isL(S) else 1.2))]


@ui("group-by", "List rows sorted into two groups, each topped by a solid header bar.",
    ["grouping", "group rows", "group header", "categorize list", "sections", "sort into groups", "group items"])
def _(S):
    rx = 0 if isL(S) else 1.0
    return [Part("solid", rect(3, 3, 18, 3, rx)), line(seg(6, 9, 18, 9)), line(seg(6, 12.5, 15, 12.5)),
            Part("solid", rect(3, 15, 18, 3, rx)), line(seg(6, 21, 17, 21))]


@ui("thumbnail-size", "Small image square beside a large image square with a short slider beneath.",
    ["image size", "preview size", "grid size", "zoom thumbnails", "icon size", "gallery size", "resize thumbnails"])
def _(S):
    return [shell(rect(2, 6, 7, 7, S.R * 0.5)), shell(rect(12, 3, 10, 10, S.R * 0.6)),
            line(seg(3, 19, 21, 19)), pip(S, 13, 19, 2.3, 0.2)]


def trail(S, x, y, s=1.0):
    return poly([(x, y + 9.5 * s), (x, y), (x + 6.5 * s, y + 6.5 * s)], r=S.r * 0.5)


@ui("pointer-trails", "Arrow pointer followed by two fading partial copies trailing behind it.",
    ["mouse trail", "cursor trail", "pointer motion", "cursor echo", "mouse trails", "pointer ghost", "cursor movement"])
def _(S):
    return [shell(poly(ptr_pts(14, 10, 0.72), closed=True, r=S.r * 0.4)),
            line(trail(S, 9.5, 7, 0.7)), line(trail(S, 5, 3.8, 0.7))]


@ui("pointer-size", "Small solid pointer and a larger outlined pointer above a double headed arrow.",
    ["cursor size", "mouse pointer size", "bigger cursor", "accessibility pointer", "cursor scale", "large cursor", "resize cursor"])
def _(S):
    return [solid(poly(ptr_pts(3, 3, 0.5), closed=True, r=S.r * 0.3)),
            shell(poly(ptr_pts(12, 2.5, 0.8), closed=True, r=S.r * 0.4)),
            line(seg(4, 19.5, 20, 19.5)), arrow_head(S, (3.2, 19.5), 180, 2.4), arrow_head(S, (20.8, 19.5), 0, 2.4)]


@ui("link-preview", "Card with an image block across its top, a title line and a short link line beneath.",
    ["url preview", "link card", "unfurl", "rich link", "open graph", "link unfurl", "web card"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), blk(S, 5.5, 5.5, 13, 5, 0.8),
            detail(seg(6, 14, 18, 14)), detail(seg(6, 17.5, 12, 17.5))]


@ui("icon-picker", "Popover panel holding a three by three grid of dots, one of them larger and highlighted.",
    ["emoji picker", "symbol picker", "choose icon", "icon chooser", "icon grid", "icon palette", "select icon"])
def _(S):
    out = [shell(poly([(2, 2), (22, 2), (22, 18), (14, 18), (12, 21), (10, 18), (2, 18)], closed=True, r=S.R * 0.7))]
    for j, y in enumerate((6.2, 10, 13.8)):
        for i, x in enumerate((6.5, 12, 17.5)):
            hot = (i, j) == (1, 1)
            out.append(Part("dot", circle(x, y, 1.9 if hot else 0.9)))
    return out


@ui("value-scrubber", "Number field with a double headed horizontal arrow hovering above its label.",
    ["scrub value", "drag to change", "number drag", "drag label", "numeric input", "adjust value", "scrubby"])
def _(S):
    return [line(seg(4, 5, 14, 5)), arrow_head(S, (3.2, 5), 180, 2.2), arrow_head(S, (14.8, 5), 0, 2.2),
            shell(rect(2, 10, 20, 10, S.R * 0.75)), detail(seg(5, 15, 8.5, 15)), detail(seg(12, 15, 19, 15))]


@ui("hex-color-field", "Input field with a solid color square at its left and a hash sign.",
    ["hex code", "color input", "color code field", "hex value", "web color", "css color", "rgb hex"])
def _(S):
    return [shell(rect(2, 5, 20, 14, S.R * 0.75)), blk(S, 4.5, 9, 4, 6, 0.6),
            detail(seg(13, 8, 13, 16)), detail(seg(17, 8, 17, 16)),
            detail(seg(11, 10, 19, 10)), detail(seg(11, 14, 19, 14))]


@ui("unit-input", "Input field with a number dash and a small separated unit label at its right end.",
    ["px input", "unit field", "css units", "measurement input", "size input", "unit selector", "number with unit"])
def _(S):
    return [shell(rect(2, 7, 20, 10, S.R * 0.75)), detail(seg(5, 12, 10.5, 12)),
            detail(seg(14, 7, 14, 17)), blk(S, 16.2, 11, 3.6, 2, 0.4)]


@ui("shortcut-tooltip", "Tooltip bubble with a caret, holding a short label line and a small keycap square.",
    ["keyboard shortcut hint", "hotkey tooltip", "key hint", "shortcut hint", "tooltip", "command hint", "accelerator"])
def _(S):
    return [shell(poly([(2, 4), (22, 4), (22, 15), (14, 15), (12, 18.5), (10, 15), (2, 15)], closed=True,
                       r=S.R * 0.7)),
            detail(seg(5, 9.5, 12, 9.5)), blk(S, 15.2, 7.7, 3.6, 3.6, 0.6)]


@ui("scroll-snap", "Row of three cards with a vertical dashed line through the centre card.",
    ["snap scrolling", "carousel snap", "align to center", "card carousel", "swipe cards", "snap point", "scroll alignment"])
def _(S):
    return [shell(rect(2, 7, 4.5, 10, S.R * 0.5)), shell(rect(9, 7, 6, 10, S.R * 0.6)), shell(rect(17.5, 7, 4.5, 10, S.R * 0.5)),
            detail(seg(12, 10, 12, 14)), line(seg(12, 2, 12, 4)), line(seg(12, 20, 12, 22))]


@ui("three-way-toggle", "Pill shaped switch track with three position dots and the round knob resting in the middle.",
    ["tri-state switch", "three position switch", "segmented toggle", "triple toggle", "slider switch", "mode switch", "three states"])
def _(S):
    return [shell(rect(2, 7, 20, 10, 3.0 if isL(S) else 5.0)),
            Part("dot", circle(6.2, 12, 1.0)), Part("dot", circle(12, 12, 2.9)), Part("dot", circle(17.8, 12, 1.0))]


@ui("split-keyboard", "Tablet screen with two separate keyboard halves at its lower left and lower right corners.",
    ["thumb keyboard", "tablet keyboard", "split keys", "two part keyboard", "ipad keyboard", "split layout", "divided keyboard"])
def _(S):
    return [shell(rect(2, 3, 20, 18, S.R)), blk(S, 4.5, 12.5, 6, 5, 0.8), blk(S, 13.5, 12.5, 6, 5, 0.8),
            pip(S, 12, 6.5, 1.0, 0.0)]


@ui("floating-keyboard", "Tablet screen with a small compact keyboard panel hovering in the middle.",
    ["movable keyboard", "undocked keyboard", "mini keyboard", "detached keyboard", "tablet floating keys", "small keyboard", "compact keyboard"])
def _(S):
    return [shell(rect(2, 3, 20, 18, S.R)), shell(rect(6.5, 9, 11, 8, S.R * 0.5)),
            pip(S, 9.7, 12, 0.8, 0.0), pip(S, 12, 12, 0.8, 0.0), pip(S, 14.3, 12, 0.8, 0.0),
            detail(seg(9.5, 14.5, 14.5, 14.5))]


@ui("predictive-text", "Row of three word suggestion pills above the top edge of a keyboard.",
    ["word suggestions", "autocomplete", "suggestion bar", "quicktype", "next word", "keyboard suggestions", "autosuggest"])
def _(S):
    out = [Part("solid", rect(x, 2.5, 5.5, 4.5, 0.8 if isL(S) else 2.2)) for x in (2, 9.25, 16.5)]
    out += [shell(rect(2, 10, 20, 11, S.R * 0.7)), pip(S, 6, 13.7, 0.9, 0), pip(S, 10, 13.7, 0.9, 0),
            pip(S, 14, 13.7, 0.9, 0), pip(S, 18, 13.7, 0.9, 0), detail(seg(7, 17.8, 17, 17.8))]
    return out


@ui("swipe-typing", "Keyboard keys with a single curving line gliding across them and ending in a dot.",
    ["glide typing", "gesture typing", "swipe keyboard", "path typing", "trace typing", "shape writing", "swype"])
def _(S):
    out = [shell(rect(2, 3, 20, 18, S.R))]
    for y in (7.5, 16.5):
        for x in (6, 10, 14, 18):
            out.append(pip(S, x, y, 0.8, 0.0))
    out += [detail("M5.5 16.5C9 5 13 19 17.5 8"), Part("dot", circle(17.5, 8, 1.6))]
    return out


@ui("autofill-field", "Input field with a short text dash and a four pointed sparkle at its right end.",
    ["autocomplete field", "ai fill", "smart fill", "auto fill form", "suggested input", "magic fill", "fill automatically"])
def _(S):
    cx, cy, ro, ri = 17.5, 12, 3.0, 1.0
    sp = poly([(cx, cy - ro), (cx + ri, cy - ri), (cx + ro, cy), (cx + ri, cy + ri), (cx, cy + ro),
               (cx - ri, cy + ri), (cx - ro, cy), (cx - ri, cy - ri)], closed=True)
    return [shell(rect(2, 6.5, 20, 11, S.R * 0.75)), detail(seg(5, 12, 10.5, 12)), Part("dot", sp)]


@ui("text-loupe", "Round magnifier bubble floating above a line of text, showing an enlarged text cursor.",
    ["magnifier", "cursor loupe", "text magnifier", "caret magnifier", "touch loupe", "text selection zoom", "edit text mobile"])
def _(S):
    return [shell(circle(12, 9, 6.5)), detail(seg(12, 5.5, 12, 12.5)), detail(seg(10, 5.5, 14, 5.5)),
            detail(seg(10, 12.5, 14, 12.5)), line(seg(3, 20.5, 21, 20.5))]


@ui("text-edit-menu", "Small pill menu split into three segments pointing down at highlighted text.",
    ["context menu", "copy paste menu", "selection menu", "edit menu", "cut copy paste", "text selection menu", "callout bar"])
def _(S):
    return [shell(poly([(2, 3), (22, 3), (22, 11), (14, 11), (12, 13.5), (10, 11), (2, 11)], closed=True,
                       r=S.R * 0.9)),
            detail(seg(8.7, 3, 8.7, 11)), detail(seg(15.3, 3, 15.3, 11)),
            Part("dot", circle(5.3, 7, 1.0)), Part("dot", circle(12, 7, 1.0)), Part("dot", circle(18.7, 7, 1.0)),
            line(seg(3, 18.5, 6, 18.5)), blk(S, 8.5, 16, 13, 5, 0.8)]


@ui("zoom-controls", "Two stacked square buttons joined together, the top with a plus and the bottom with a minus.",
    ["zoom in out", "plus minus buttons", "map zoom", "zoom buttons", "magnify controls", "scale buttons", "stepper"])
def _(S):
    return [shell(rect(5, 2, 14, 20, S.R)), detail(seg(5, 12, 19, 12)),
            detail(seg(9.5, 7, 14.5, 7)), detail(seg(12, 4.5, 12, 9.5)), detail(seg(9.5, 17, 14.5, 17))]


@ui("desktop-icons", "Screen with a column of three small icon squares at its left edge.",
    ["desktop shortcuts", "icon grid", "home screen", "desktop view", "show desktop icons", "file icons", "launcher icons"])
def _(S):
    return [shell(rect(2, 3, 20, 18, S.R)),
            blk(S, 5, 5.5, 3.5, 3.5, 0.6), blk(S, 5, 10.25, 3.5, 3.5, 0.6), blk(S, 5, 15, 3.5, 3.5, 0.6),
            pip(S, 14, 8, 1.0, 0.0), pip(S, 17.5, 8, 1.0, 0.0)] if False else [
        shell(rect(2, 3, 20, 18, S.R)),
        blk(S, 5.5, 5.5, 3.5, 3.5, 0.6), blk(S, 5.5, 10.25, 3.5, 3.5, 0.6), blk(S, 5.5, 15, 3.5, 3.5, 0.6)]


@ui("ghost-button", "Rounded button drawn as a dashed outline with a short label line inside.",
    ["outline button", "secondary button", "dashed button", "empty button", "text button", "placeholder button", "tertiary button"])
def _(S):
    return [*dashed_rect(S, 2, 6, 20, 12), line(seg(8, 12, 16, 12))]


@ui("loading-button", "Rounded button with a small spinner arc in place of its label.",
    ["button spinner", "submit loading", "busy button", "processing button", "pending action", "loading state", "wait button"])
def _(S):
    return [shell(rect(2, 6, 20, 12, S.R * 1.5)), detail(arc(12, 12, 2.8, -60, 210))]


@ui("disabled-button", "Rounded button with diagonal hatching at both ends and a short pale label line.",
    ["inactive button", "unavailable button", "greyed out", "button disabled", "not clickable", "locked button", "dimmed button"])
def _(S):
    return [shell(rect(2, 6, 20, 12, S.R * 1.5)), detail(seg(5.5, 14.5, 8, 9.5)), detail(seg(16, 14.5, 18.5, 9.5)),
            detail(seg(10, 12, 14, 12))]


@ui("underline-tabs", "Row of three short tab labels with a thick underline beneath the first over a baseline.",
    ["tab bar", "tabs", "tab navigation", "active tab", "tab underline", "segmented tabs", "navigation tabs"])
def _(S):
    return [line(seg(3, 8, 8, 8)), line(seg(10.5, 8, 15.5, 8)), line(seg(18, 8, 22, 8)),
            line(seg(2, 19, 22, 19)), Part("solid", rect(2, 14.5, 9.5, 4.5, 0 if isL(S) else 1.0))]


@ui("text-truncate", "Line of text inside a box that ends abruptly in three small dots at the edge.",
    ["ellipsis", "overflow text", "cut off text", "line clamp", "text overflow", "truncated", "read more"])
def _(S):
    return [shell(rect(2, 6, 20, 12, S.R * 0.75)), detail(seg(5, 12, 11, 12)),
            Part("dot", circle(14.2, 12, 0.9)), Part("dot", circle(16.7, 12, 0.9)), Part("dot", circle(19.2, 12, 0.9))]
