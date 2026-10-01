"""TypeIcon Core: ui (batch ui_004): editor and view modes, form fields, design-tool layout controls, keys and device screens.

Uses the same keyshapes as the other ui modules: frame rect(3, 3, 18, 18), window rect(3, 4, 18, 16),
phone rect(5, 2, 14, 20). Dividers inside a frame are `detail`s (knocked out in Filled) and small marks use `pip`/`blk`.
Every Filled design is built from `fn(FILL)` (Line geometry), so a drawing can branch on `isF(S)`.
"""
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
    """Small solid block: square corners in Line, rounded in Rounded."""
    return Part("dot", rect(x, y, w, h, 0 if isL(S) else min(k, w / 2, h / 2)))


def tri(S, pts, k=0.6):
    """Small solid polygon."""
    return Part("dot", poly(pts, closed=True, r=0 if isL(S) else k))


def frame(S):
    return shell(rect(3, 3, 18, 18, S.R))


def win(S, y0=4.0, h=16.0):
    return shell(rect(3, y0, 18, h, S.R))


def phone(S):
    return shell(rect(5, 2, 14, 20, S.R * 0.75))


def pt(cx, cy, r, deg):
    a = math.radians(deg)
    return (cx + r * math.cos(a), cy + r * math.sin(a))


def head(S, tip, deg, size=3.0, kind=line):
    """Open arrowhead whose tip points along `deg` (0 = right, 90 = down)."""
    a = math.radians(deg)
    pts = []
    for s in (135, -135):
        b = a + math.radians(s)
        pts.append((tip[0] + size * math.cos(b), tip[1] + size * math.sin(b)))
    return kind(poly([pts[0], tip, pts[1]], r=S.r))


def mx(d_pts):
    return [(24 - x, y) for x, y in d_pts]


def mountain(S, x, y, w, h):
    """Small solid mountain peak sitting on the baseline y + h."""
    return tri(S, [(x, y + h), (x + w / 2, y), (x + w, y + h)], 0.4)


# =========================================================================== editor and document views

@ui("syntax-highlight", "Three lines of code made of solid and plain dashes, as coloured code appears in an editor.",
    ["code colour", "code color", "syntax colouring", "editor theme", "highlighting", "source code", "tokens"])
def _(S):
    return [blk(S, 3, 3.5, 6, 3, 0.8), line(seg(12, 5, 21, 5)),
            line(seg(6, 12, 11, 12)), blk(S, 14, 10.5, 7, 3, 0.8),
            blk(S, 3, 17.5, 5, 3, 0.8), line(seg(11, 19, 15, 19)), line(seg(18, 19, 21, 19))]


@ui("format-document", "Ragged lines on the left, an arrow, and neatly aligned lines on the right.",
    ["auto format", "prettify", "tidy code", "reformat", "align code", "beautify", "clean up"])
def _(S):
    return [line(seg(2, 6, 8, 6)), line(seg(2, 12, 5, 12)), line(seg(2, 18, 7, 18)),
            line(seg(9.5, 12, 14, 12)), head(S, (14.5, 12), 0, 2.5),
            line(seg(17, 6, 22, 6)), line(seg(17, 12, 22, 12)), line(seg(17, 18, 22, 18))]


def _brace(x0, y0, y1, flip=False):
    ym = (y0 + y1) / 2
    pts = lambda *a: a
    d = (f"M{x0 + 3} {y0}Q{x0} {y0} {x0} {y0 + 3}V{ym - 3}Q{x0} {ym} {x0 - 2.5} {ym}"
         f"Q{x0} {ym} {x0} {ym + 3}V{y1 - 3}Q{x0} {y1} {x0 + 3} {y1}")
    if not flip:
        return d
    d = (f"M{24 - x0 - 3} {y0}Q{24 - x0} {y0} {24 - x0} {y0 + 3}V{ym - 3}Q{24 - x0} {ym} {24 - x0 + 2.5} {ym}"
         f"Q{24 - x0} {ym} {24 - x0} {ym + 3}V{y1 - 3}Q{24 - x0} {y1} {24 - x0 - 3} {y1}")
    return d


@ui("bracket-pair", "A matching pair of curly braces with a small dot under each.",
    ["curly braces", "matching brackets", "braces", "code", "pair", "highlight match", "editor"])
def _(S):
    return [line(_brace(6, 2.5, 16.5)), line(_brace(6, 2.5, 16.5, True)),
            pip(S, 6.5, 20.5, 1.25, 0.25), pip(S, 17.5, 20.5, 1.25, 0.25)]


@ui("split-editor", "Window divided into two panes by a vertical line, each pane holding short lines of code.",
    ["split view", "side by side", "two panes", "code editor", "compare", "editor group", "split pane"])
def _(S):
    return [win(S), detail(seg(12, 4, 12, 20)),
            detail(seg(6, 9, 9, 9)), detail(seg(6, 14, 8.5, 14)),
            detail(seg(15, 9, 18, 9)), detail(seg(15, 14, 17.5, 14))]


@ui("text-direction-vertical", "A column of small letter blocks beside a downward arrow, for top to bottom writing.",
    ["vertical text", "top to bottom", "writing mode", "vertical writing", "cjk", "text flow", "column text"])
def _(S):
    return [blk(S, 4, 3, 6, 4, 1), blk(S, 4, 10, 6, 4, 1), blk(S, 4, 17, 6, 4, 1),
            line(seg(17, 3, 17, 20.5)), head(S, (17, 21), 90, 3)]


@ui("view-thumbnails", "Four picture thumbnails in a grid, each showing a small mountain.",
    ["thumbnail view", "image grid", "photo grid", "previews", "gallery view", "pictures", "icons view"])
def _(S):
    out = []
    for x in (3, 13):
        for y in (3, 13):
            out += [shell(rect(x, y, 8, 8, S.R * 0.5)), mountain(S, x + 2, y + 2.5, 4, 3)]
    return out


@ui("miller-columns", "Three narrow columns side by side with a highlighted row stepping down in each.",
    ["column view", "finder columns", "cascading lists", "hierarchy browser", "file browser", "drill down", "miller"])
def _(S):
    return [win(S), detail(seg(9, 4, 9, 20)), detail(seg(15, 4, 15, 20)),
            blk(S, 4.5, 7, 3, 2.5, 0.6), blk(S, 10.5, 11, 3, 2.5, 0.6), blk(S, 16.5, 15, 3, 2.5, 0.6)]


@ui("two-page-spread", "Open book spread of two facing pages with a line of text on each.",
    ["facing pages", "book view", "two page view", "double page", "open book", "reading view", "spread"])
def _(S):
    return [shell(poly([(2, 6), (12, 8), (22, 6), (22, 19), (12, 21), (2, 19)], closed=True, r=S.r)),
            detail(seg(12, 8, 12, 21)), detail(seg(5.5, 11.5, 9, 12.5)), detail(seg(5.5, 15.5, 8.5, 16.2)),
            detail(seg(18.5, 11.5, 15, 12.5)), detail(seg(18.5, 15.5, 15.5, 16.2))]


@ui("continuous-scroll-view", "Two stacked pages with a double ended scroll arrow beside them.",
    ["continuous scroll", "scroll pages", "vertical pages", "pdf scroll", "page flow", "scrolling view", "long document"])
def _(S):
    return [shell(rect(3, 2.5, 11, 8, S.R * 0.6)), shell(rect(3, 13.5, 11, 8, S.R * 0.6)),
            line(seg(19.5, 6, 19.5, 18)), head(S, (19.5, 5, ), -90, 2.5), head(S, (19.5, 19), 90, 2.5)]


@ui("presentation-mode", "Screen on a tripod stand showing a play triangle.",
    ["slideshow", "present", "start presentation", "projector screen", "fullscreen slides", "play slides", "talk"])
def _(S):
    return [shell(rect(3, 2.5, 18, 12, S.R * 0.75)),
            tri(S, [(10, 5.5), (10, 11.5), (15, 8.5)], 0.6),
            line(seg(12, 14.5, 7, 21.5)), line(seg(12, 14.5, 17, 21.5)), line(seg(12, 14.5, 12, 19.5))]


@ui("slide-sorter", "Six slide thumbnails in two columns with the middle left one outlined as selected.",
    ["slide sorter", "slide overview", "reorder slides", "slides grid", "presentation tiles", "deck view", "thumbnails"])
def _(S):
    out = []
    for r, y in enumerate((2, 9.5, 17)):
        for c, x in enumerate((2, 13.5)):
            if (r, c) == (1, 0):
                out.append(shell(rect(x + 1, y + 1, 7.5, 3.5, S.R * 0.4)))
            else:
                out.append(blk(S, x, y, 8.5, 5, 0.8))
    return out


@ui("speaker-notes", "A slide above lines of notes with a small speech bubble.",
    ["presenter notes", "notes pane", "talking points", "slide notes", "script", "presentation notes", "comments"])
def _(S):
    bub = poly([(15, 14.5), (21, 14.5), (21, 19), (18, 19), (16, 21), (16, 19), (15, 19)], closed=True, r=S.r)
    return [shell(rect(3, 2, 18, 9, S.R * 0.6)), line(seg(3, 15.5, 11, 15.5)), line(seg(3, 20, 8, 20)), shell(bub)]


@ui("density-compact", "Five horizontal lines packed closely together.",
    ["compact", "tight spacing", "dense", "small rows", "condensed", "table density", "more rows"])
def _(S):
    return [line(seg(3, y, 21, y)) for y in (4, 8, 12, 16, 20)]


@ui("density-comfortable", "Three horizontal lines spaced widely apart.",
    ["comfortable", "roomy", "relaxed spacing", "loose", "airy", "table density", "fewer rows"])
def _(S):
    return [line(seg(3, y, 21, y)) for y in (5, 12, 19)]


@ui("ar-view", "A small cube framed by four corner brackets, as seen in an augmented reality viewfinder.",
    ["augmented reality", "ar", "view in your space", "3d preview", "place object", "camera view", "viewfinder"])
def _(S):
    hexp = regular(12, 12, 5.5, 6)
    c = (12, 12)
    out = [shell(poly(hexp, closed=True, r=S.r * 0.5)), detail(seg(*c, *hexp[1])), detail(seg(*c, *hexp[3])),
           detail(seg(*c, *hexp[5]))]
    for cx, cy, sx, sy in ((2.5, 2.5, 1, 1), (21.5, 2.5, -1, 1), (21.5, 21.5, -1, -1), (2.5, 21.5, 1, -1)):
        out.append(line(poly([(cx, cy + sy * 4.5), (cx, cy), (cx + sx * 4.5, cy)], r=S.r)))
    return out


# =========================================================================== more view modes and helpers

def tabpath(x0, x1, yt, yb, k):
    return f"M{x0} {yb}V{yt + k}A{k} {k} 0 0 1 {x0 + k} {yt}H{x1 - k}A{k} {k} 0 0 1 {x1} {yt + k}V{yb}Z"


def open_rect(x0, y0, x1, y1, R, gap=None, right_open=None):
    """Rounded rectangle outline as an open path. gap=(a, b): top edge omitted between x=a and x=b.
    right_open=x: right edge omitted, the path ends on the top and bottom edges at x."""
    if gap:
        a, b = gap
        return (f"M{b} {y0}H{x1 - R}A{R} {R} 0 0 1 {x1} {y0 + R}V{y1 - R}A{R} {R} 0 0 1 {x1 - R} {y1}H{x0 + R}"
                f"A{R} {R} 0 0 1 {x0} {y1 - R}V{y0 + R}A{R} {R} 0 0 1 {x0 + R} {y0}H{a}")
    return (f"M{right_open} {y0}H{x0 + R}A{R} {R} 0 0 0 {x0} {y0 + R}V{y1 - R}A{R} {R} 0 0 0 {x0 + R} {y1}H{right_open}")


def dashed_rect(S, x, y, w, h, kind=line, dash=4.0):
    trim = 0 if isL(S) else 0.75
    arm_w = (w - dash) / 2 - 3.5 / 2 if w > 10 else w / 2 - 1.75
    arm_h = (h - dash) / 2 - 3.5 / 2 if h > 10 else h / 2 - 1.75
    x1, y1 = x + w, y + h
    parts = []
    for cx, cy, sx, sy in ((x, y, 1, 1), (x1, y, -1, 1), (x1, y1, -1, -1), (x, y1, 1, -1)):
        parts.append(kind(poly([(cx, cy + sy * (arm_h - trim)), (cx, cy), (cx + sx * (arm_w - trim), cy)], r=S.r)))
    if w > 10:
        m = x + w / 2
        for yy in (y, y1):
            parts.append(kind(seg(m - dash / 2 + trim, yy, m + dash / 2 - trim, yy)))
    if h > 10:
        m = y + h / 2
        for xx in (x, x1):
            parts.append(kind(seg(xx, m - dash / 2 + trim, xx, m + dash / 2 - trim)))
    return parts


def star4(cx, cy, r):
    k = r * 0.32
    return [(cx, cy - r), (cx + k, cy - k), (cx + r, cy), (cx + k, cy + k), (cx, cy + r), (cx - k, cy + k),
            (cx - r, cy), (cx - k, cy - k)]


def star5(cx, cy, ro, ri):
    pts = []
    for i in range(10):
        r = ro if i % 2 == 0 else ri
        a = math.radians(-90 + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


@ui("view-3d", "Wireframe cube with three short axis arrows rising from a corner.",
    ["3d view", "three dimensional", "axes", "xyz", "perspective", "model view", "gizmo"])
def _(S):
    hx = regular(15, 8.5, 5.5, 6)
    c = (15, 8.5)
    return [shell(poly(hx, closed=True, r=S.r * 0.5)), detail(seg(*c, *hx[1])), detail(seg(*c, *hx[3])),
            detail(seg(*c, *hx[5])),
            line(seg(4, 21, 4, 12.5)), head(S, (4, 12), -90, 2.2),
            line(seg(4, 21, 12.5, 21)), head(S, (13, 21), 0, 2.2),
            line(seg(4, 21, 8.5, 17))]


@ui("timeline-view", "A horizontal line with three bars of different lengths staggered above and below it.",
    ["timeline", "schedule view", "gantt", "calendar bars", "time axis", "milestones", "project plan"])
def _(S):
    return [line(seg(2, 12, 22, 12)), blk(S, 3, 5, 8, 3.5, 1), blk(S, 8.5, 15.5, 8, 3.5, 1), blk(S, 14, 5, 7, 3.5, 1)]


@ui("focus-view", "A single card in the centre with edges of two more cards cut off at the left and right sides.",
    ["focus", "carousel", "current item", "cards", "spotlight", "centered card", "cover flow"])
def _(S):
    return [shell(rect(8, 4, 8, 16, S.R * 0.6)),
            line(poly([(2, 8), (3.5, 8), (3.5, 16), (2, 16)], r=0)), line(poly([(22, 8), (20.5, 8), (20.5, 16), (22, 16)], r=0))]


def _outline_mode_filled():
    c = P(circle(9.5, 9.5, 7.5))
    ring = ST(rect(10.5, 10.5, 10, 10, 2), 2.0, "butt", "miter", 4.0)
    cut = ST(rect(10.5, 10.5, 10, 10, 2), 5.0, "butt", "miter", 4.0)
    return U(D(c, cut), ring)


@icon("outline-mode", CAT, "A circle and a square overlapping, both drawn as thin wireframe outlines with no fill.",
      tags=["wireframe", "outline view", "no fill", "vector view", "keyline", "shape outlines", "design"],
      filled=_outline_mode_filled)
def _(S):
    return [line(circle(9.5, 9.5, 6.5)), line(rect(10.5, 10.5, 10, 10, 2 if isL(S) else 3))]


@ui("infinite-canvas", "A fading grid of dots around an infinity sign in the middle.",
    ["endless canvas", "unlimited space", "whiteboard", "pan and zoom", "boundless", "workspace", "infinity"])
def _(S):
    out = [line("M12 12C9.5 8.5 4.5 8.5 4.5 12S9.5 15.5 12 12S19.5 8.5 19.5 12 14.5 15.5 12 12")]
    for x, y, r in ((4, 3.5, 1.5), (12, 3.5, 1.5), (20, 3.5, 1.5), (4, 20.5, 1.5), (12, 20.5, 1.5), (20, 20.5, 1.5)):
        out.append(pip(S, x, y, r, 0.0))
    return out


@ui("card-flip", "A card turned part way round with a curved arrow circling it.",
    ["flip card", "turn over", "flashcard", "rotate card", "reveal back", "flip animation", "other side"])
def _(S):
    tip = pt(13, 12, 8, 50)
    return [shell(poly([(3, 4), (12, 7), (12, 17), (3, 20)], closed=True, r=S.r)),
            line(arc(13, 12, 8, -50, 50)), head(S, tip, 140, 2.5)]


@ui("preview-pane", "Window with a short list on the left and a page with an eye on the right.",
    ["preview", "reading pane", "quick look", "details pane", "file preview", "side preview", "peek"])
def _(S):
    eye = "M12.5 12.5Q16 8.5 19.5 12.5Q16 16.5 12.5 12.5Z"
    return [win(S), detail(seg(9.5, 4, 9.5, 20)), detail(seg(5, 8.5, 7, 8.5)), detail(seg(5, 12.5, 7, 12.5)),
            detail(seg(5, 16.5, 7, 16.5)), detail(eye), pip(S, 16, 12.5, 1.0, 0.1)]


@ui("hot-corner", "A screen with a bright quarter circle in its top right corner and a pointer arrow heading into it.",
    ["screen corner", "active corner", "corner trigger", "mouse corner", "desktop gesture", "mission control", "shortcut"])
def _(S):
    quarter = Part("dot", "M20 5H14A6 6 0 0 0 20 11Z")
    return [shell(rect(3, 4, 18, 13, S.R)), quarter, line(seg(12, 20.5, 12, 17)), line(seg(8, 21, 16, 21)),
            line(seg(6.5, 13.5, 11.5, 8.5)), head(S, (12, 8), -45, 2.8)]


@ui("screen-saver", "Monitor whose screen shows a few small stars and a bouncing ball with its trail.",
    ["screensaver", "idle screen", "sleep display", "lock screen", "stars", "bouncing ball", "dvd logo"])
def _(S):
    return [shell(rect(3, 3, 18, 13, S.R)), line(seg(12, 16, 12, 20)), line(seg(8, 20.5, 16, 20.5)),
            tri(S, star4(7.5, 7.5, 1.9), 0.2), tri(S, star4(12, 6.5, 1.5), 0.2),
            dot(16.5, 10, 2.1), detail(seg(7.5, 12.5, 12.5, 11))]


@ui("detach-tab", "Two tabs on a bar with a third tab lifted off below and trailing short motion lines.",
    ["pop out tab", "tear off tab", "move tab to window", "separate tab", "undock tab", "drag tab out", "browser"])
def _(S):
    k = 1.5 if isL(S) else 2.5
    return [shell(tabpath(2, 9.5, 3, 9, k)), shell(tabpath(11.5, 19, 3, 9, k)), line(seg(2, 9.5, 22, 9.5)),
            shell(rect(11.5, 14, 10.5, 7.5, S.R * 0.6)), line(seg(3, 15.5, 7, 15.5)), line(seg(3, 20, 7, 20))]


@ui("tab-overview", "Browser frame holding a two by two grid of tab thumbnails.",
    ["tab grid", "all tabs", "tab switcher", "tab manager", "tab thumbnails", "browser tabs", "open tabs"])
def _(S):
    return [frame(S), detail(seg(3, 7.5, 21, 7.5)), blk(S, 5.5, 10.5, 5.5, 3.5, 0.8), blk(S, 13, 10.5, 5.5, 3.5, 0.8),
            blk(S, 5.5, 16, 5.5, 3.5, 0.8), blk(S, 13, 16, 5.5, 3.5, 0.8)]


@ui("vote-counter", "An upward caret, a short number dash and a downward caret stacked in a column.",
    ["upvote downvote", "score", "karma", "rating counter", "like counter", "vote buttons", "thread votes"])
def _(S):
    return [line(poly([(7, 8), (12, 3), (17, 8)], r=S.r)), line(seg(9, 12, 15, 12)),
            line(poly([(7, 16), (12, 21), (17, 16)], r=S.r))]


@ui("message-composer", "Wide rounded text field with a paperclip at the left and a paper plane send button at the right.",
    ["message box", "chat input", "write message", "compose", "attach and send", "reply box", "text field"])
def _(S):
    clip = "M9.5 9V14a2.25 2.25 0 0 1-4.5 0V9.5"
    plane = [(14.5, 8.5), (20.5, 12), (14.5, 15.5), (16, 12)]
    return [shell(rect(2, 5.5, 20, 13, 2.5 if isL(S) else 6.5)), detail(clip), tri(S, plane, 0.4)]


@ui("figure-caption", "A picture frame with a mountain inside and a short caption line under it.",
    ["image caption", "photo caption", "figure label", "picture description", "alt text", "media caption", "illustration"])
def _(S):
    return [shell(rect(3, 3, 18, 12, S.R * 0.75)), mountain(S, 6, 7.5, 7, 5.5), mountain(S, 11, 9.5, 6, 3.5),
            line(seg(7, 19.5, 17, 19.5))]


@ui("callout-block", "Rounded block with a thick bar down its left side, a small dot and two lines of text.",
    ["callout", "note block", "info box", "admonition", "highlight box", "aside", "alert box"])
def _(S):
    return [shell(rect(3, 4, 18, 16, S.R)), blk(S, 5.5, 7, 2, 10, 0.5), pip(S, 11.5, 8.5, 1.1, 0.1),
            detail(seg(14.5, 8.5, 18, 8.5)), detail(seg(11, 14.5, 18, 14.5))]


@ui("labeled-divider", "A horizontal line broken in the middle by a small rounded label.",
    ["divider with text", "separator label", "or divider", "section break", "rule with label", "line with label", "hr"])
def _(S):
    return [line(seg(2, 12, 5, 12)), shell(rect(8, 9, 8, 6, S.R * 0.8 if isL(S) else 3)), line(seg(19, 12, 22, 12))]


@ui("user-chip", "A rounded pill with a small avatar disc at the left end and a short name line.",
    ["avatar chip", "user tag", "mention pill", "assignee", "member badge", "name tag", "profile chip"])
def _(S):
    return [shell(rect(2, 6.5, 20, 11, 2 if isL(S) else 5.5)), dot(7.5, 12, 2.2), detail(seg(12.5, 12, 18, 12))]


@ui("transfer-list", "Two tall list panels side by side with a right arrow and a left arrow between them.",
    ["dual list", "move items", "shuttle", "select from list", "list swap", "available and selected", "dual listbox"])
def _(S):
    return [shell(rect(3, 3, 4.5, 18, S.R * 0.5)), shell(rect(16.5, 3, 4.5, 18, S.R * 0.5)),
            line(seg(10.5, 9, 13.5, 9)), head(S, (13.7, 9), 0, 2),
            line(seg(10.5, 15, 13.5, 15)), head(S, (10.3, 15), 180, 2)]


# =========================================================================== controls and fields

@ui("segmented-progress-bar", "A row of four short separate bars, the first two tall and solid and the last two slim and empty.",
    ["step progress", "stepper bar", "progress steps", "multi step", "completion", "wizard progress", "stages"])
def _(S):
    out = []
    for i, x in enumerate((2, 7.4, 12.8, 18.2)):
        if i < 2:
            out.append(blk(S, x, 8 - (0.5 if isF(S) else 0), 3.8, 8 + (1 if isF(S) else 0), 1.2))
        else:
            out.append(blk(S, x, 11 - (0.25 if isF(S) else 0), 3.8, 2 + (0.5 if isF(S) else 0), 0.8))
    return out


@ui("circular-slider", "A round track with the arc filled two thirds of the way round and ending in a round knob.",
    ["dial", "radial slider", "knob", "circular progress", "round control", "rotary", "angle picker"])
def _(S):
    knob = pt(12, 12, 8, 30)
    out = [line(arc(12, 12, 8, 150, 390)), dot(knob[0], knob[1], 2.6)]
    for a in (68, 90, 112):
        p = pt(12, 12, 8, a)
        out.append(dot(p[0], p[1], 1.0))
    return out


@ui("on-screen-joystick", "A large ring with a smaller solid disc pushed toward its upper right.",
    ["virtual joystick", "thumbstick", "touch controls", "game controller", "analog stick", "directional pad", "mobile game"])
def _(S):
    out = [shell(circle(12, 12, 9)), dot(14.8, 9.2, 3.6), pip(S, 7, 12.5, 1.3, 0.2), pip(S, 11.5, 17, 1.3, 0.2)]
    return out


@ui("image-hotspot", "A photo frame with a mountain and a small dot inside a pulsing ring above it.",
    ["hotspot", "clickable area", "image map", "interactive image", "annotation point", "product tag", "tap target"])
def _(S):
    return [shell(rect(3, 4, 18, 16, S.R)), detail(poly([(4, 18.5), (8.5, 13), (12.5, 18.5)], r=S.r)),
            detail(circle(15, 10, 3)), dot(15, 10, 1.0)]


@ui("annotation-pin", "A speech bubble with a pointed tail like a map pin and a short dash inside it.",
    ["comment pin", "note marker", "feedback pin", "review comment", "location comment", "marker bubble", "pinned comment"])
def _(S):
    R = 1.5 if isL(S) else 3
    d = (f"M{5 + R} 2.5H{19 - R}A{R} {R} 0 0 1 19 {2.5 + R}V{12 - R}A{R} {R} 0 0 1 {19 - R} 12H14.5L12 20L9.5 12H{5 + R}"
         f"A{R} {R} 0 0 1 5 {12 - R}V{2.5 + R}A{R} {R} 0 0 1 {5 + R} 2.5Z")
    return [shell(d), detail(seg(9.5, 7.2, 14.5, 7.2))]


@ui("resizable-panels", "Window split in two by a divider with a small grip handle in its middle.",
    ["resize panes", "drag divider", "splitter", "adjustable split", "panel handle", "split view", "resize handle"])
def _(S):
    return [win(S), detail(seg(14, 4, 14, 7.5)), detail(seg(14, 16.5, 14, 20)), blk(S, 12.5, 9, 3, 6, 1.5),
            detail(seg(6, 9, 10, 9)), detail(seg(6, 13, 9, 13))]


@ui("floating-label-field", "A text field whose short label sits in a gap in the top border with the entry text below.",
    ["floating label", "material input", "labeled input", "text input", "form field", "outlined field", "input label"])
def _(S):
    R = 2 if isL(S) else 4
    return [line(open_rect(2.5, 6.5, 21.5, 19, R, gap=(5.5, 12))), line(seg(8, 6.5, 10, 6.5)) if False else
            line(seg(7.5, 6.5, 10, 6.5)), line(seg(6.5, 13, 15.5, 13))]


@ui("input-prefix", "A text field with a small separate box at its left end that holds a symbol.",
    ["input addon", "prefix box", "field prefix", "at sign", "username field", "input group", "leading label"])
def _(S):
    return [shell(rect(2, 6.5, 20, 11, S.R)), detail(seg(9.5, 6.5, 9.5, 17.5)), dot(5.75, 12, 1.4),
            detail(seg(13, 12, 18, 12))]


@ui("input-with-button", "A long text field joined at its right end to a solid rounded button.",
    ["search box with button", "subscribe field", "input group", "email signup", "field and button", "submit field", "form row"])
def _(S):
    R = 2 if isL(S) else 5
    return [line(open_rect(2.5, 7, 21, 17, R, right_open=15)), solid(rect(15, 6, 7, 12, R * 0.7)),
            line(seg(6.5, 12, 10.5, 12))]


@ui("disclosure-row", "A wide list row with a short label at the left and a small chevron at the right end.",
    ["list row", "navigation row", "settings row", "drill in", "expand row", "table row", "menu item"])
def _(S):
    return [shell(rect(2, 6, 20, 12, S.R)), detail(seg(6, 12, 12.5, 12)),
            detail(poly([(16.5, 9.5), (19, 12), (16.5, 14.5)], r=S.r))]


@ui("radio-card", "A rounded card with a solid radio dot in its top left corner and two lines of text.",
    ["selectable card", "option card", "choice card", "radio option", "plan picker", "pick one", "selected card"])
def _(S):
    return [shell(rect(3, 3, 18, 18, 3 if isL(S) else 5)), pip(S, 8, 8, 2.0, 0.2),
            detail(seg(6.5, 13.5, 17.5, 13.5)), detail(seg(6.5, 17, 12, 17))]


@ui("pattern-fill", "A square outline filled with evenly spaced diagonal hatching lines.",
    ["hatch", "hatching", "diagonal lines", "texture fill", "stripes", "fill pattern", "swatch"])
def _(S):
    out = [frame(S)]
    for c in (16, 24, 32):
        out.append(detail(seg(3.5, c - 3.5, c - 3.5, 3.5) if c < 24 else seg(c - 20.5, 20.5, 20.5, c - 20.5)))
    return out


@ui("noise-texture", "A square outline scattered with tiny dots of different sizes.",
    ["grain", "noise", "speckle", "random dots", "texture", "dither", "stipple"])
def _(S):
    out = [frame(S)]
    for x, y, r in ((7.5, 7.5, 1.0), (13, 7, 1.4), (17, 10.5, 1.0), (10, 11.5, 1.1), (15, 15, 1.5), (7.5, 16, 1.4),
                    (12, 17.2, 0.9)):
        out.append(dot(x, y, r))
    return out


@ui("outline-stroke", "A thick line turned into a hollow outline, shown above a thin solid line with an arrow between.",
    ["expand stroke", "stroke to path", "convert stroke", "hollow line", "outline path", "vector", "design tool"])
def _(S):
    return [shell(rect(3, 3, 18, 6, 3)), line(seg(12, 17, 12, 13.5)), head(S, (12, 12.5), -90, 2.2),
            line(seg(3, 20, 21, 20))]


@ui("offset-path", "A small solid star surrounded by a larger star outline at an even distance.",
    ["offset", "expand path", "inset outline", "path offset", "contour", "grow shape", "vector"])
def _(S):
    return [shell(poly(star5(12, 12.6, 10.3, 5.6), closed=True, r=S.r)),
            tri(S, star5(12, 12.9, 4.0, 1.9), 0.3)]


@ui("constrain-proportions", "The letters W and H stacked with a small chain link joining them at the right.",
    ["lock aspect ratio", "keep proportions", "width height link", "proportional scaling", "link dimensions", "aspect lock", "resize"])
def _(S):
    return [line(poly([(2.5, 4), (4.5, 10), (7, 6), (9.5, 10), (11.5, 4)], r=S.r)),
            line(seg(3, 14, 3, 21)), line(seg(11, 14, 11, 21)), line(seg(3, 17.5, 11, 17.5)),
            line(poly([(15, 6.5), (19.5, 6.5), (19.5, 17.5), (15, 17.5)], r=S.r))]


@ui("adjustment-layer", "A diamond layer with a half filled circle on it, stacked above a second layer.",
    ["adjustments", "filter layer", "layer effect", "levels", "non destructive", "photo editing", "contrast layer"])
def _(S):
    return [shell(poly([(12, 2.5), (22, 8), (12, 13.5), (2, 8)], closed=True, r=S.r)),
            detail(circle(12, 8, 2.4)), Part("dot", "M9.6 8A2.4 2.4 0 0 0 14.4 8Z"),
            line(poly([(2, 12.5), (12, 18), (22, 12.5)], r=S.r))]


@ui("component-variants", "A dashed rounded frame holding a row of three small diamonds.",
    ["variants", "component set", "design system", "variant set", "states", "options", "figma"])
def _(S):
    out = dashed_rect(S, 2.5, 5.5, 19, 13)
    for cx in (7, 12, 17):
        out.append(tri(S, [(cx, 9.8), (cx + 2.3, 12), (cx, 14.2), (cx - 2.3, 12)], 0.3))
    return out


# =========================================================================== layout controls

@ui("stack-layout", "Three equal blocks stacked in a column with even gaps and an arrow running down the side.",
    ["vertical stack", "column layout", "auto layout vertical", "stack of items", "vstack", "spacing", "flow down"])
def _(S):
    return [blk(S, 3, 2.5, 12, 4.5, 1), blk(S, 3, 9.75, 12, 4.5, 1), blk(S, 3, 17, 12, 4.5, 1),
            line(seg(19.5, 3, 19.5, 19)), head(S, (19.5, 20), 90, 2.5)]


@ui("flex-wrap", "Two rows of small boxes with a bent arrow carrying the top row's end around to the start of the next row.",
    ["wrap", "line wrap", "flow layout", "wrapping row", "flexbox", "next line", "css layout"])
def _(S):
    return [blk(S, 3, 3, 4.5, 4.5, 1), blk(S, 9.75, 3, 4.5, 4.5, 1), blk(S, 16.5, 3, 4.5, 4.5, 1),
            line(poly([(18.75, 10), (18.75, 12.5), (5.25, 12.5), (5.25, 14.5)], r=S.r)), head(S, (5.25, 15.6), 90, 2.2),
            blk(S, 3, 17.5, 4.5, 4.5, 1), blk(S, 9.75, 17.5, 4.5, 4.5, 1)]


@ui("absolute-position", "A frame with a small box pinned inside it, a dot on each side marking its distance to two edges.",
    ["absolute layout", "fixed position", "offset from edge", "pin to corner", "position absolute", "top left offset", "css position"])
def _(S):
    return [frame(S), detail(rect(10.5, 10.5, 6, 6, S.R * 0.4)), pip(S, 6.5, 13.5, 0.9, 0.1), pip(S, 13.5, 6.5, 0.9, 0.1)]


@ui("overflow-clip", "A frame with a larger circle running through its right edge, the outside part drawn as dashes.",
    ["clip content", "overflow hidden", "cropped content", "mask", "cut off", "hidden overflow", "css overflow"])
def _(S):
    return [shell(rect(3, 4, 12, 16, S.R)), detail(arc(15, 12, 6.5, 90, 270)),
            line(arc(15, 12, 6.5, -48, -16)), line(arc(15, 12, 6.5, 16, 48))]


@ui("scroll-container", "A box with lines of content running off its bottom and a slim scrollbar down its right side.",
    ["scrollable area", "scroll box", "overflow scroll", "scroll region", "scrollable panel", "long content", "scroll view"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(seg(6.5, 8, 13.5, 8)), detail(seg(6.5, 12.5, 13.5, 12.5)),
            detail(seg(6.5, 17, 11, 17)), detail(seg(17.5, 7, 17.5, 13))]


@ui("background-removal", "A head and shoulders silhouette in front of a checkerboard backdrop.",
    ["remove background", "cutout", "transparent background", "subject isolation", "photo editing", "magic eraser", "png"])
def _(S):
    body = "M7.5 20.5C7.5 17 9.5 15.5 12 15.5S16.5 17 16.5 20.5Z"
    return [frame(S), dot(12, 11.5, 2.8), Part("dot", body),
            blk(S, 5.5, 5.5, 2.5, 2.5, 0.4), blk(S, 11, 5.5, 2.5, 2.5, 0.4), blk(S, 16, 5.5, 2.5, 2.5, 0.4),
            blk(S, 5.5, 11, 2.5, 2.5, 0.4), blk(S, 16, 11, 2.5, 2.5, 0.4)]


@ui("object-selection", "A person silhouette inside a dashed outline, with a pointer arrow at its lower right corner.",
    ["select subject", "smart select", "select object", "magic select", "detect object", "photo editing", "selection tool"])
def _(S):
    out = dashed_rect(S, 3, 3, 13, 18, dash=4)
    cursor = [(14.5, 13), (14.5, 21), (16.7, 19), (18.2, 22), (19.6, 21.4), (18.2, 18.5), (21, 18.3)]
    out += [dot(9.5, 9.5, 2.3), Part("dot", "M5.5 18C5.5 14.5 7 13.5 9.5 13.5S13.5 14.5 13.5 18Z"),
            tri(S, cursor, 0.3)]
    return out


@ui("rgb-channels", "Three overlapping circles arranged in a triangle with a solid dot where all three meet.",
    ["red green blue", "rgb", "colour channels", "color channels", "additive color", "color mixing", "screen colors"])
def _(S):
    return [line(circle(12, 9.4, 5.8)), line(circle(14.94, 14.5, 5.8)), line(circle(9.06, 14.5, 5.8)),
            (tri(S, regular(12, 12.9, 1.9, 3), 0) if S.name == "line" else dot(12, 12.9, 1.2))]


@ui("cmyk-channels", "Four overlapping rings arranged in a square, each with a solid dot of a different size.",
    ["cmyk", "cyan magenta yellow black", "print colours", "print colors", "ink channels", "subtractive color", "separations"])
def _(S):
    return [line(circle(8.3, 8.3, 4.6)), line(circle(15.7, 8.3, 4.6)), line(circle(8.3, 15.7, 4.6)),
            line(circle(15.7, 15.7, 4.6)),
            pip(S, 8.3, 8.3, 0.9, 0), pip(S, 15.7, 8.3, 1.2, 0), pip(S, 8.3, 15.7, 1.5, 0), pip(S, 15.7, 15.7, 1.8, 0)]


@ui("key-meta", "A rounded keycap with a small solid diamond in its centre.",
    ["meta key", "command key", "super key", "windows key", "modifier key", "keyboard shortcut", "keycap"])
def _(S):
    return [shell(rect(3, 3, 18, 18, 3 if isL(S) else 6)),
            tri(S, [(12, 7.5), (16.5, 12), (12, 16.5), (7.5, 12)], 0.6)]


@ui("cursor-rotate", "An arrow pointer with a curved arrow sweeping around its tip.",
    ["rotate cursor", "rotate handle", "turn object", "rotation pointer", "pivot", "spin", "mouse rotate"])
def _(S):
    cursor = [(9, 10), (9, 20), (11.6, 17.6), (13.6, 22), (15.6, 21.1), (13.6, 16.8), (17, 16.6)]
    return [shell(poly(cursor, closed=True, r=S.r * 0.5)), line(arc(9, 10, 6, 180, 270)), head(S, (9.6, 4), 0, 2.4)]


@ui("ring-silent-switch", "The edge of a phone with a small sliding switch sticking out and a bell on its face.",
    ["mute switch", "silent mode", "ring silent", "vibrate switch", "ringer", "phone side button", "sound off"])
def _(S):
    bell = "M12.5 16.5H19.5M13.5 16.5V13A2.5 2.5 0 0 1 18.5 13V16.5"
    return [shell(rect(8, 2.5, 14, 19, S.R * 0.75)), blk(S, 4, 7, 4, 5, 1), detail(bell), pip(S, 16, 19.2, 0.8, 0.0)]


@ui("always-on-display", "A phone with a dim clock ring and a single small notification dot on its dark screen.",
    ["aod", "lock screen clock", "ambient display", "always on", "dim screen", "standby", "idle display"])
def _(S):
    return [phone(S), detail(circle(12, 9.5, 3)), pip(S, 12, 17.5, 1.1, 0.1)]


@ui("locate-device", "A phone with a radar arc on each side and a small dot above it.",
    ["find my phone", "find device", "ping device", "track device", "lost phone", "device location", "ring my phone"])
def _(S):
    return [shell(rect(9.5, 7.5, 5, 10, S.R * 0.4)), line(arc(12, 12.5, 7, -40, 40)), line(arc(12, 12.5, 7, 140, 220)),
            pip(S, 12, 3.8, 1.2, 0.2)]


@ui("device-transfer", "Two phones side by side with a curved arrow arching from the left one to the right one.",
    ["send to device", "move to new phone", "phone to phone", "share between devices", "migrate data", "handoff", "airdrop"])
def _(S):
    return [shell(rect(3, 9, 6, 12, S.R * 0.4)), shell(rect(15, 9, 6, 12, S.R * 0.4)),
            line("M6 6.5Q12 0.5 18 6"), head(S, (18.4, 6.4), 60, 2.4)]


@ui("navigation-stack", "Three screen cards stacked in depth with a back chevron on the front one.",
    ["screen stack", "navigation history", "push screen", "back stack", "card stack", "page stack", "drill down"])
def _(S):
    return [line(poly([(8, 6), (8, 3), (21, 3), (21, 12)], r=S.r)),
            line(poly([(5.5, 9.5), (5.5, 7.5), (18.5, 7.5), (18.5, 12)], r=S.r)) if False else
            line(poly([(5.5, 9), (5.5, 7), (17, 7)], r=S.r)),
            shell(rect(3, 11, 15, 10, S.R * 0.6)), detail(poly([(11.5, 14), (8.5, 16), (11.5, 18)], r=S.r))]


@ui("page-curl", "A page with its bottom right corner peeled up and folded back.",
    ["peel", "curled corner", "page turn", "folded corner", "dog ear", "next page", "page flip"])
def _(S):
    return [shell(poly([(5, 3), (19, 3), (19, 14), (13, 21), (5, 21)], closed=True, r=S.r)),
            detail(poly([(19, 14), (12.1, 15.1), (13, 21)], r=S.r)), detail(seg(8, 8, 15, 8))]


@ui("search-overlay", "A dimmed screen with diagonal hatching below a bright search field across its top.",
    ["spotlight", "command search", "quick search", "search modal", "global search", "dimmed background", "find anything"])
def _(S):
    return [frame(S), detail(rect(6, 6, 12, 5, 2 if isL(S) else 2.5)),
            detail(seg(6, 18.5, 9, 15.5)), detail(seg(11, 18.5, 14, 15.5)), detail(seg(16, 18.5, 18.5, 16))]


@ui("layout-three-pane", "A window split into a narrow folder column, a middle list column and a wide reading pane.",
    ["three column layout", "mail layout", "email client", "folders list preview", "master detail", "three panes", "reader layout"])
def _(S):
    return [win(S), detail(seg(8.5, 4, 8.5, 20)), detail(seg(13.5, 4, 13.5, 20)), pip(S, 5.5, 8, 1.0, 0.1),
            detail(seg(10.5, 8, 11.5, 8)) if False else pip(S, 11, 8, 1.0, 0.1), detail(seg(16, 8.5, 19, 8.5)),
            detail(seg(16, 12.5, 19, 12.5))]


@ui("layout-auth-split", "A screen split in half with an image block on one side and two fields and a button on the other.",
    ["login layout", "sign in page", "split screen login", "auth page", "sign up layout", "register screen", "login template"])
def _(S):
    return [frame(S), detail(seg(12, 3, 12, 21)), blk(S, 5.5, 5.5, 4.5, 13, 0.8),
            detail(seg(14.5, 7.5, 18.5, 7.5)), detail(seg(14.5, 11.5, 18.5, 11.5)), blk(S, 14.5, 15, 4.5, 3, 0.6)]


@ui("layout-article", "A page with a bold title bar, a wide picture block beneath it and a line of text.",
    ["article layout", "blog post layout", "story page", "news article", "post template", "headline and image", "content page"])
def _(S):
    return [shell(rect(4, 2, 16, 20, S.R)), blk(S, 7, 5, 10, 2.5, 0.6), blk(S, 7, 9.5, 10, 5.5, 0.8),
            detail(seg(7, 18.5, 17, 18.5))]


@ui("layout-product-detail", "A page with a square picture on the left and a title line, price dash and button on the right.",
    ["product page", "item detail", "shop layout", "ecommerce page", "product template", "buy page", "listing detail"])
def _(S):
    return [frame(S), blk(S, 5.5, 6, 6, 6, 1), detail(seg(5.5, 16, 10.5, 16)),
            detail(seg(14, 7.5, 18.5, 7.5)), detail(seg(14, 11, 17, 11)), blk(S, 14, 14.5, 5, 3.5, 0.8)]


@ui("isolation-mode", "One bold circle standing out beside faint dashed outlines of a square and a small circle.",
    ["isolate", "focus on object", "hide others", "solo", "isolate layer", "dim others", "single object view"])
def _(S):
    out = dashed_rect(S, 3, 3, 8, 8)
    out.append(shell(circle(16.5, 13.5, 4.6)))
    for a0, a1 in ((-60, 10), (60, 130), (180, 250)):
        out.append(line(arc(7, 18, 3, a0, a1)))
    return out


@ui("checkbox-tree", "A parent checkbox with a branch line to two child checkboxes, the upper one ticked solid.",
    ["tree select", "nested checkboxes", "hierarchical selection", "select all children", "permissions tree", "indeterminate", "check hierarchy"])
def _(S):
    def box(x, y):
        out = [shell(rect(x + 1, y + 1, 4, 4, S.R * 0.3))]
        if isF(S):
            out.append(Part("dot", rect(x + 2, y + 2, 2, 2)))
        return out
    return (box(2, 9) + [line(seg(8, 12, 11.5, 12)), line(seg(11.5, 6, 11.5, 18)), line(seg(11.5, 6, 15, 6)),
                         line(seg(11.5, 18, 15, 18)), blk(S, 15, 3, 6, 6, 1)] + box(15, 15))
