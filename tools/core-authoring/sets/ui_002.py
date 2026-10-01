"""TypeIcon Core: ui (batch ui_002): input controls, cursors, keycaps and keyboard/pointer patterns.

Same keyshapes as ui_001: frame rect(3,3,18,18), phone rect(5,2,14,20). Keycaps are rect(2,4,20,16).
Small marks use `pip` / `blk`; every Filled design is built from `fn(FILL)` (Line geometry).
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, I, P, ST, U, Part, Style, arc, circle, detail, dot, ellipse, filled_region, fmt, icon, line, path_to_d, poly,
    rect, regular, seg, shell, solid,
)

CAT = "ui"
FILL = Style("filled", "butt", "miter", R=2.0, r=0.0)


def isF(S) -> bool:
    return S.name == "filled"


def isL(S) -> bool:
    return S.name != "rounded"


def ui(name, description, tags, aliases=()):
    def deco(fn):
        return icon(name, CAT, description, tags=tags, aliases=aliases, filled=lambda: filled_region(fn(FILL)))(fn)
    return deco


def pip(S, x, y, r=1.5, grow=0.4):
    if isF(S):
        return Part("dot", circle(x, y, r + grow))
    if S.name == "line":
        s = r * 0.9
        return Part("dot", rect(x - s, y - s, 2 * s, 2 * s))
    return Part("dot", circle(x, y, r))


def blk(S, x, y, w, h, k=1.0):
    return Part("dot", rect(x, y, w, h, 0 if isL(S) else min(k, w / 2, h / 2)))


def tri(S, pts, k=0.5):
    """Small solid triangle/polygon, softened in Rounded."""
    return Part("dot", poly(pts, closed=True, r=0 if isL(S) else k))


def chev(S, cx, cy, w=3.0, h=None, deg=90, kind=line):
    h = w if h is None else h
    a = math.radians(deg)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    tip = (cx + ux * h / 2, cy + uy * h / 2)
    b = (cx - ux * h / 2, cy - uy * h / 2)
    return kind(poly([(b[0] + nx * w, b[1] + ny * w), tip, (b[0] - nx * w, b[1] - ny * w)], r=S.r))


def dashed_rect(S, x, y, w, h, kind=line, dash=4.0):
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


def arrow_head(S, tip, deg, size=3.0, kind=line):
    a = math.radians(deg)
    pts = []
    for s in (135, -135):
        b = a + math.radians(s)
        pts.append((tip[0] + size * math.cos(b), tip[1] + size * math.sin(b)))
    return kind(poly([pts[0], tip, pts[1]], r=S.r))


def star_pts(cx, cy, ro, ri, n=5):
    out = []
    for i in range(n * 2):
        a = math.radians(-90 + i * 180 / n)
        r = ro if i % 2 == 0 else ri
        out.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return out


PTR = [(0, 0), (0, 10.5), (2.8, 8), (4.8, 12.6), (6.8, 11.7), (4.8, 7.2), (8.4, 7.2)]


def ptr_pts(x, y, s=1.0):
    return [(x + px * s, y + py * s) for px, py in PTR]


def pointer(S, x=3, y=2.5, s=1.0):
    """Arrow pointer, tip at (x, y)."""
    return shell(poly(ptr_pts(x, y, s), closed=True, r=S.r * 0.45), stroke_miterlimit="3")


def keycap(S, x=2, y=4, w=20, h=16):
    return shell(rect(x, y, w, h, min(S.R, 3)))


# =========================================================================== social and content patterns

@ui("read-receipt", "Two check marks side by side, the second one offset, showing a message was delivered and read.",
    ["double check", "seen", "delivered", "message read", "double tick", "chat status"])
def _(S):
    return [line(poly([(2, 12.5), (6, 16.5), (14, 7.5)], r=S.r)),
            line(poly([(11, 16), (20, 7.5)], r=S.r))]


@ui("reaction-bar", "Rounded bar of quick emoji reactions: a heart and two dots in a pill.",
    ["reactions", "emoji reactions", "react", "like bar", "quick reply", "emoji picker"])
def _(S):
    heart = "M7 15.4L4.6 12.9A1.6 1.6 0 0 1 7 10.8A1.6 1.6 0 0 1 9.4 12.9Z"
    return [shell(rect(2, 6, 20, 12, 6 if not isL(S) else 4)), Part("dot", heart), pip(S, 13.5, 12, 1.2, 0.3), pip(S, 18, 12, 1.2, 0.3)]


@ui("avatar-group", "Three overlapping user avatars in a row, the middle one in front.",
    ["avatars", "team members", "people", "participants", "face pile", "collaborators"])
def _(S):
    return [shell(circle(12, 8, 3.2)),
            line(poly([(6.5, 19.5), (6.5, 17.5), (9, 14.5), (15, 14.5), (17.5, 17.5), (17.5, 19.5)], r=S.r) if isL(S)
                 else "M6.5 19.5V18A4.5 4.5 0 0 1 11 14H13A4.5 4.5 0 0 1 17.5 18V19.5"),
            pip(S, 3.5, 10.5, 1.4, 0.3), line(seg(2.5, 18, 2.5, 15.5)),
            pip(S, 20.5, 10.5, 1.4, 0.3), line(seg(21.5, 18, 21.5, 15.5))]


@ui("activity-feed", "Vertical timeline with three dots, each followed by a short line of text.",
    ["timeline", "feed", "history", "updates", "log", "recent activity"])
def _(S):
    return [line(seg(5, 3, 5, 21)),
            pip(S, 5, 5, 2.0, 0.3), pip(S, 5, 12, 2.0, 0.3), pip(S, 5, 19, 2.0, 0.3),
            line(seg(10, 5, 20, 5)), line(seg(10, 12, 20, 12)), line(seg(10, 19, 16, 19))]


@ui("tag-cloud", "Cluster of rounded pill tags of different widths in two rows.",
    ["tags", "labels", "word cloud", "topics", "keywords", "categories"])
def _(S):
    rr = 3 if not isL(S) else 2
    return [shell(rect(3, 4, 9, 6, rr)), shell(rect(16, 4, 5, 6, rr)),
            shell(rect(3, 14, 5, 6, rr)), shell(rect(12, 14, 9, 6, rr))]


@ui("corner-ribbon", "Card with a diagonal ribbon band across its top right corner and a text line below.",
    ["ribbon", "badge", "new label", "sale tag", "banner", "sash"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)),
            Part("dot", poly([(11, 3), (17, 3), (21, 7), (21, 12)], closed=True)),
            detail(seg(6.5, 17, 13, 17))]


@ui("placeholder-box", "Square frame crossed by two diagonal lines, the sign for a missing image or empty slot.",
    ["placeholder", "missing image", "image placeholder", "empty slot", "wireframe", "mockup"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(seg(7, 7, 17, 17)), detail(seg(17, 7, 7, 17))]


@ui("testimonial-card", "Card with a quote mark at the top, a line of text and a small avatar with a name line.",
    ["testimonial", "quote card", "review", "customer quote", "feedback", "praise"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)),
            pip(S, 7.5, 7.2, 1.4, 0.2), pip(S, 12, 7.2, 1.4, 0.2),
            detail(seg(7.5, 8, 6.8, 10)), detail(seg(12, 8, 11.3, 10)),
            detail(seg(7, 13, 17, 13)),
            pip(S, 7.5, 17, 1.3, 0.2), detail(seg(11, 17, 17, 17))]


@ui("hover-card", "Pointer resting on an underlined word with a small profile card floating above it.",
    ["hover preview", "preview card", "popover", "tooltip card", "link preview", "mouseover"])
def _(S):
    return [shell(rect(3, 2.5, 18, 8, S.R * 0.6)), detail(seg(7, 6.5, 15, 6.5)),
            line(seg(3, 20.5, 10, 20.5)),
            pointer(S, 11, 12.5, 0.75)]


@ui("ad-slot", "Wide dashed frame with a small tag in its corner, marking a reserved advertising space.",
    ["advertisement", "ad space", "banner ad", "sponsored", "placement", "ad unit"])
def _(S):
    return [*dashed_rect(S, 2.5, 6, 19, 12, dash=4), blk(S, 5, 8.5, 4, 2, 0.5)]


@ui("button-group", "Three rectangular buttons joined edge to edge in a single rounded strip.",
    ["segmented control", "button bar", "joined buttons", "toggle group", "button set", "split control"])
def _(S):
    return [shell(rect(2, 7, 20, 10, S.R)), detail(seg(8.7, 7, 8.7, 17)), detail(seg(15.3, 7, 15.3, 17))]


@ui("split-button", "Rounded button divided into a wide label part and a narrow part with a down arrow.",
    ["dropdown button", "menu button", "action menu", "combo button", "more actions", "split action"])
def _(S):
    return [shell(rect(2, 6, 20, 12, S.R)), detail(seg(16, 6, 16, 18)), detail(seg(5.5, 12, 12, 12)),
            tri(S, [(17.3, 10.6), (20.7, 10.6), (19, 13.4)], 0.4)]


@ui("icon-button", "Round button with a small star glyph at its centre.",
    ["round button", "fab", "circle button", "action button", "favorite button", "glyph button"])
def _(S):
    return [shell(circle(12, 12, 9)),
            Part("dot", poly(star_pts(12, 12.4, 4.6, 2.1), closed=True, r=0 if isL(S) else 0.7))]


@ui("knob-control", "Round rotary knob with a pointer mark and tick marks arced around its lower half.",
    ["knob", "dial", "rotary", "volume knob", "potentiometer", "turn control"])
def _(S):
    out = [shell(circle(12, 11.5, 5)), detail(seg(12, 8, 12, 11.5))]
    for a in (15, 50, 90, 130, 165):
        r = math.radians(a)
        out.append(line(seg(12 + 8 * math.cos(r), 11.5 + 8 * math.sin(r), 12 + 10 * math.cos(r), 11.5 + 10 * math.sin(r))))
    return out


@ui("number-input", "Input field with a short number dash and stacked up and down arrows at its right end.",
    ["number field", "numeric input", "spinner", "stepper input", "spin box", "counter field"])
def _(S):
    return [shell(rect(2, 6, 20, 12, S.R)), detail(seg(6, 12, 11, 12)),
            tri(S, [(17.3, 11), (20.7, 11), (19, 8.6)], 0.4), tri(S, [(17.3, 13), (20.7, 13), (19, 15.4)], 0.4)]


@ui("quantity-selector", "Pill with a minus at the left, a number mark in the middle and a plus at the right.",
    ["quantity", "stepper", "increment decrement", "amount", "cart quantity", "plus minus"])
def _(S):
    return [shell(rect(2, 6, 20, 12, 6 if not isL(S) else 4)), detail(seg(5.5, 12, 8.5, 12)),
            detail(seg(15.5, 12, 18.5, 12)), detail(seg(17, 10.5, 17, 13.5)), detail(seg(12, 9.7, 12, 14.3))]


# =========================================================================== sliders, pickers and fields

@ui("stepped-slider", "Horizontal track with five tick marks beneath and a round thumb on the middle step.",
    ["discrete slider", "steps", "range steps", "rating scale", "stepper slider", "ticks"])
def _(S):
    out = [line(seg(3, 9, 8, 9)), line(seg(16, 9, 21, 9)), shell(circle(12, 9, 3.2))]
    for x in (3, 7.5, 12, 16.5, 21):
        out.append(line(seg(x, 15, x, 19)))
    return out


@ui("hue-slider", "Horizontal bar striped with vertical colour bands and a round handle resting on it.",
    ["color slider", "colour slider", "hue", "spectrum", "color picker", "gradient bar"])
def _(S):
    return [shell(rect(2, 7, 20, 10, 5 if not isL(S) else 3)), detail(seg(6, 8, 6, 16)), detail(seg(10, 8, 10, 16)),
            detail(circle(16, 12, 3.2))]


@ui("checkbox-indeterminate", "Rounded square with a short horizontal dash across its centre; a partly selected checkbox.",
    ["mixed checkbox", "partial selection", "select some", "tri-state", "minus box", "partially checked"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(seg(8, 12, 16, 12))]


@ui("scroll-wheel-picker", "Picker wheel: a highlighted middle row between a faded row above and a faded row below.",
    ["wheel picker", "spinner picker", "phone picker", "select wheel", "drum picker", "scroll picker"])
def _(S):
    return [shell(rect(2, 8.5, 20, 7, S.R * 0.6)), detail(seg(7, 12, 17, 12)),
            line(seg(8, 4, 16, 4)), line(seg(9, 20, 15, 20))]


@ui("time-picker", "Clock face beside stacked up and down arrows for choosing a time.",
    ["time input", "clock picker", "select time", "hour minute", "time spinner", "timepicker"])
def _(S):
    return [shell(circle(8.5, 12, 6.5)), detail(poly([(8.5, 8.5), (8.5, 12), (11, 13.5)], r=S.r * 0.5)),
            tri(S, [(17.7, 10.5), (21.3, 10.5), (19.5, 7.7)], 0.4), tri(S, [(17.7, 13.5), (21.3, 13.5), (19.5, 16.3)], 0.4)]


@ui("text-area", "Tall field with lines of text and a small diagonal resize mark in its bottom right corner.",
    ["textarea", "multiline input", "comment box", "message field", "resizable field", "long text"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(seg(7, 8, 17, 8)), detail(seg(7, 12, 17, 12)),
            detail(seg(7, 16, 10, 16)), detail(seg(14, 17.5, 17.5, 14))]


@ui("tag-input", "Input field holding two small pill tags followed by a text cursor.",
    ["chips input", "token field", "multi select input", "tags field", "keywords input", "email chips"])
def _(S):
    return [shell(rect(2, 6, 20, 12, S.R)), blk(S, 5, 9.5, 4.5, 5, 2), blk(S, 11, 9.5, 4.5, 5, 2),
            detail(seg(18.5, 9.5, 18.5, 14.5))]


@ui("filter-chip", "Rounded pill with a check mark at the left and a short label dash.",
    ["chip", "selected chip", "filter tag", "choice chip", "toggle chip", "pill filter"])
def _(S):
    return [shell(rect(2, 6, 20, 12, 6 if not isL(S) else 4)),
            detail(poly([(5.8, 12.2), (7.8, 14.2), (11, 10)], r=S.r * 0.5)), detail(seg(14.5, 12, 18, 12))]


@ui("file-dropzone", "Dashed frame with a down arrow dropping into a tray, the area to drop files on.",
    ["drop zone", "drag and drop upload", "upload area", "drop files here", "dropzone", "file target"])
def _(S):
    return [*dashed_rect(S, 3, 3, 18, 18), line(seg(12, 7.5, 12, 13.5)), arrow_head(S, (12, 14), 90, 3),
            line(poly([(8, 16.8), (8, 17.5), (16, 17.5), (16, 16.8)], r=0))]


@ui("password-strength", "Password field of dots above a meter of four bars, the first three filled.",
    ["strength meter", "password meter", "weak strong", "security level", "password check", "complexity"])
def _(S):
    out = [shell(rect(2, 3, 20, 9, S.R * 0.75)), pip(S, 6.5, 7.5, 1.1, 0.2), pip(S, 10.5, 7.5, 1.1, 0.2),
           pip(S, 14.5, 7.5, 1.1, 0.2)]
    for i in range(4):
        x = 2.5 + i * 5.25
        out.append(Part("solid", rect(x, 15.5, 4, 3.5, 0 if isL(S) else 1)) if i < 3 else line(seg(x, 17.25, x + 4, 17.25)))
    return out


@ui("rich-text-editor", "Editor window with a toolbar of bold, italic and underline marks above lines of text.",
    ["wysiwyg", "text editor", "formatting toolbar", "word processor", "compose", "editor"])
def _(S):
    return [shell(rect(2, 3, 20, 18, S.R)), detail(seg(2, 9.5, 22, 9.5)),
            blk(S, 5, 4.8, 3, 3, 0.8), detail(seg(12, 4.5, 11, 7.5)), detail(seg(15.5, 7.5, 19, 7.5)),
            detail(seg(6, 13.2, 18, 13.2)), detail(seg(6, 16.8, 13, 16.8))]


@ui("dial-pad", "Keypad of three columns of round buttons with a larger call button beneath.",
    ["keypad", "phone keypad", "dialer", "number pad", "call pad", "dialpad"])
def _(S):
    out = []
    for y in (3.5, 8.5, 13.5):
        for x in (6, 12, 18):
            out.append(pip(S, x, y, 1.5, 0.3))
    out.append(shell(circle(12, 19, 2.6)))
    return out


@ui("switch-list", "Three stacked rows of text, each with a switch at its right, the first two switched on.",
    ["settings list", "toggle list", "preferences", "switches", "options list", "on off list"])
def _(S):
    rr = 2.5 if not isL(S) else 1.5
    return [line(seg(3, 5, 10, 5)), line(seg(3, 12, 10, 12)), line(seg(3, 19, 10, 19)),
            Part("solid", rect(14, 2.5, 8, 5, rr)), Part("solid", rect(14, 9.5, 8, 5, rr)),
            shell(rect(14.5, 17, 7, 4, 2 if not isL(S) else 1))]


@ui("video-chapters", "Video frame above a progress bar split into four chapter segments, the first two filled.",
    ["chapters", "segments", "video progress", "timeline markers", "scrub bar", "sections"])
def _(S):
    out = [shell(rect(2, 3, 20, 10, S.R)), tri(S, [(10.5, 5.8), (14.5, 8), (10.5, 10.2)], 0.4)]
    for i in range(4):
        x = 2.5 + i * 5.5
        out.append(Part("solid", rect(x, 17, 4, 3, 0 if isL(S) else 1)) if i < 2 else line(seg(x, 18.5, x + 4, 18.5)))
    return out


@ui("video-player", "Wide video screen with a play triangle in the centre and a progress bar along the bottom.",
    ["player", "media player", "movie", "play video", "streaming", "video controls"])
def _(S):
    return [shell(rect(2, 3, 20, 18, S.R)), tri(S, [(10, 6.3), (15.5, 9.8), (10, 13.3)], 0.5),
            detail(seg(6, 17, 18, 17))]


@ui("sentiment-slider", "Track between a frowning face at the left and a smiling face at the right, thumb near the right end.",
    ["mood slider", "satisfaction", "feedback scale", "rating slider", "happy sad", "emotion scale"])
def _(S):
    return [pip(S, 3.8, 3.5, 1.0, 0.2), pip(S, 7.2, 3.5, 1.0, 0.2),
            line("M3 10.5Q5.5 6.8 8 10.5" if not isL(S) else "M3 10.5L5.5 7.5L8 10.5"),
            pip(S, 16.8, 3.5, 1.0, 0.2), pip(S, 20.2, 3.5, 1.0, 0.2),
            line("M16 6.8Q18.5 10.5 21 6.8" if not isL(S) else "M16 6.8L18.5 9.8L21 6.8"),
            line(seg(3, 17, 13, 17)), line(seg(19, 17, 21, 17)), shell(circle(16, 17, 3))]


# =========================================================================== pointers and cursors

@ui("cursor-wait", "Arrow pointer with a small hourglass at its lower right, showing the system is busy.",
    ["busy cursor", "loading cursor", "hourglass", "please wait", "pointer waiting", "mouse busy"])
def _(S):
    return [pointer(S, 3, 2.5, 0.85),
            shell(poly([(14.5, 13.5), (20.5, 13.5), (17.5, 17.5)], closed=True)),
            shell(poly([(14.5, 21.5), (20.5, 21.5), (17.5, 17.5)], closed=True))]


@ui("cursor-progress", "Arrow pointer with a small partly drawn spinner beside its tail; working in the background.",
    ["working in background", "progress cursor", "loading", "spinner cursor", "busy pointer", "app starting"])
def _(S):
    return [pointer(S, 3, 2.5, 0.85), line(arc(17.5, 17.5, 4, 20, 290)), line(seg(17.5, 17.5, 17.5, 17.5))][:2]


@ui("cursor-context-menu", "Arrow pointer with a small menu card of lines at its lower right.",
    ["right click", "context menu", "pointer menu", "popup menu", "secondary click", "shortcut menu"])
def _(S):
    return [pointer(S, 3, 2.5, 0.8), shell(rect(12, 11.5, 10, 10, S.R * 0.5)),
            detail(seg(14.5, 15.3, 19.5, 15.3)), detail(seg(14.5, 18.7, 19.5, 18.7))]


@ui("cursor-cell", "Thick plus sign with a hollow outline, like the cursor for selecting spreadsheet cells.",
    ["spreadsheet cursor", "cell select", "sheet cursor", "thick cross", "cell pointer", "grid select"])
def _(S):
    pts = [(9.5, 3), (14.5, 3), (14.5, 9.5), (21, 9.5), (21, 14.5), (14.5, 14.5), (14.5, 21), (9.5, 21), (9.5, 14.5),
           (3, 14.5), (3, 9.5), (9.5, 9.5)]
    return [shell(poly(pts, closed=True, r=S.r))]


@ui("cursor-col-resize", "Two vertical bars side by side with arrowheads pointing outward, the column resize cursor.",
    ["resize column", "column resize", "split cursor", "drag divider", "horizontal resize", "adjust width"])
def _(S):
    return [line(seg(10, 6, 10, 18)), line(seg(14, 6, 14, 18)),
            line(seg(3.5, 12, 10, 12)), line(seg(14, 12, 20.5, 12)),
            arrow_head(S, (3.5, 12), 180, 2.8), arrow_head(S, (20.5, 12), 0, 2.8)]


@ui("cursor-alias", "Arrow pointer with a small curved shortcut arrow at its lower right, for creating a link or alias.",
    ["shortcut cursor", "link cursor", "create alias", "drag to link", "symlink", "pointer shortcut"])
def _(S):
    return [pointer(S, 3, 2.5, 0.85), line("M13.5 21C13.5 17 15.5 15 20 15" if not isL(S) else "M13.5 21V19Q13.5 15 18 15H20"),
            arrow_head(S, (20.5, 15), 0, 2.4)]


@ui("cursor-drag", "Arrow pointer carrying a small dashed rectangle, an item being dragged.",
    ["drag cursor", "dragging", "move item", "drag and drop", "carry", "copy cursor"])
def _(S):
    return [pointer(S, 3, 2.5, 0.85), *dashed_rect(S, 12.5, 12.5, 9, 8.5, dash=2)]


@ui("collaborator-cursors", "Two arrow pointers at different positions, each trailing a small name tag.",
    ["multiplayer cursors", "live cursors", "co-editing", "presence", "team cursors", "shared editing"])
def _(S):
    return [pointer(S, 2.5, 2.5, 0.6), blk(S, 9.5, 7.5, 7, 3.2, 1.2),
            pointer(S, 8.5, 12, 0.6), blk(S, 15.5, 17, 6.5, 3.2, 1.2)]


@ui("mouse-scroll", "Computer mouse outline with a scroll wheel and an arrow chevron above it.",
    ["scroll wheel", "scroll mouse", "wheel scroll", "mouse wheel", "scrolling", "scroll up"])
def _(S):
    return [chev(S, 12, 4.2, 3, 2.5, -90), shell(rect(7, 8.5, 10, 13, 5)), detail(seg(12, 11.5, 12, 14.5))]


@ui("double-click", "Arrow pointer with two nested arcs radiating from its tip.",
    ["double tap", "click twice", "open item", "mouse double click", "dbl click", "select word"])
def _(S):
    return [pointer(S, 9, 9, 0.9), line(arc(9, 9, 3.8, 180, 270)), line(arc(9, 9, 7.2, 180, 270))]


# =========================================================================== keycaps

@ui("key-escape", "Keycap with a circle and an arrow pointing out to the top left; the escape key.",
    ["esc", "escape key", "cancel key", "exit key", "keyboard key", "keycap"])
def _(S):
    return [keycap(S), detail(circle(15, 14.8, 2.6)), detail(seg(8, 8, 11, 11)),
            detail(poly([(7.6, 11.6), (7.6, 7.6), (11.6, 7.6)], r=S.r * 0.4))]


@ui("key-tab", "Wide keycap with an arrow pointing to a vertical bar, the tab key.",
    ["tab", "tab key", "indent key", "keyboard key", "keycap", "next field"])
def _(S):
    return [keycap(S), detail(seg(6, 12, 14.5, 12)), arrow_head(S, (14.5, 12), 0, 3, detail), detail(seg(18, 8, 18, 16))]


@ui("key-shift", "Keycap with a solid upward arrow with a stem; the shift key.",
    ["shift", "shift key", "capital key", "upper case", "keyboard key", "keycap"])
def _(S):
    return [keycap(S), blk(S, 0, 0, 0, 0) if False else Part("dot", poly([(12, 7.5), (16.5, 12.3), (13.8, 12.3), (13.8, 16.5), (10.2, 16.5), (10.2, 12.3), (7.5, 12.3)], closed=True, r=0 if isL(S) else 0.5))]


@ui("key-capslock", "Keycap with a solid shift arrow above a bar and a small indicator light in its corner.",
    ["caps lock", "capslock", "caps key", "capital letters", "keyboard key", "uppercase lock"])
def _(S):
    return [keycap(S), Part("dot", poly([(12, 6.8), (15.8, 10.8), (13.6, 10.8), (13.6, 13.6), (10.4, 13.6), (10.4, 10.8), (8.2, 10.8)], closed=True, r=0 if isL(S) else 0.4)),
            blk(S, 8.5, 15.2, 7, 1.8, 0.6), pip(S, 18.5, 7.2, 0.9, 0.2)]


@ui("key-control", "Keycap with an upward caret on its face; the control key.",
    ["ctrl", "control key", "ctrl key", "modifier key", "keyboard key", "keycap"])
def _(S):
    return [keycap(S), detail(poly([(7.5, 14.5), (12, 9.5), (16.5, 14.5)], r=S.r * 0.4))]


@ui("key-option", "Keycap showing the option symbol: a line that steps down diagonally with a short bar above its right end.",
    ["alt", "option key", "alt key", "modifier key", "keyboard key", "keycap"])
def _(S):
    return [keycap(S), detail(poly([(6.5, 8.5), (10, 8.5), (14, 15.5), (17.5, 15.5)], r=S.r * 0.4)),
            detail(seg(13.5, 8.5, 17.5, 8.5))]


@ui("key-backspace", "Pentagon shaped delete key pointing left with an x inside.",
    ["backspace", "delete left", "erase key", "back delete", "keyboard key", "clear character"])
def _(S):
    return [shell(poly([(8, 5), (21, 5), (21, 19), (8, 19), (2.5, 12)], closed=True, r=S.r)),
            detail(seg(12.5, 9.5, 17.5, 14.5)), detail(seg(17.5, 9.5, 12.5, 14.5))]


@ui("key-delete", "Keycap with an outlined arrow pointing right with a flat tail; the forward delete key.",
    ["del", "forward delete", "delete key", "remove key", "keyboard key", "keycap"])
def _(S):
    return [keycap(S), detail(poly([(6.5, 8.5), (13.5, 8.5), (17.5, 12), (13.5, 15.5), (6.5, 15.5)], closed=True, r=S.r * 0.4))]


@ui("key-spacebar", "Very wide flat keycap with a small open bracket symbol in its centre; the space bar.",
    ["space", "space bar", "spacebar key", "keyboard key", "keycap", "blank key"])
def _(S):
    return [shell(rect(1.5, 7.5, 21, 9, min(S.R, 3))), detail(poly([(8, 10.5), (8, 13), (16, 13), (16, 10.5)]))]


@ui("key-home", "Keycap with a small house outline; the home key.",
    ["home key", "start of line", "go home", "keyboard key", "keycap", "beginning"])
def _(S):
    return [keycap(S), detail(poly([(6.5, 12.5), (12, 7.5), (17.5, 12.5)], r=S.r * 0.4)),
            detail(poly([(8.5, 11), (8.5, 16.5), (15.5, 16.5), (15.5, 11)]))]


@ui("key-end", "Keycap with a diagonal arrow pointing to a corner bracket at the bottom right; the end key.",
    ["end key", "end of line", "last", "keyboard key", "keycap", "go to end"])
def _(S):
    return [keycap(S), detail(seg(7.5, 8, 15, 15.5)), detail(poly([(10.5, 15.5), (15.5, 15.5), (15.5, 10.5)], r=S.r * 0.4))]


@ui("key-print-screen", "Keycap with four corner brackets framing an area, like a screen capture; the print screen key.",
    ["prtsc", "print screen", "screenshot key", "capture", "keyboard key", "keycap"])
def _(S):
    out = [keycap(S)]
    for x, y, sx, sy in ((6.8, 8, 1, 1), (17.2, 8, -1, 1), (6.8, 16, 1, -1), (17.2, 16, -1, -1)):
        out.append(detail(poly([(x, y + sy * 2.4), (x, y), (x + sx * 2.4, y)])))
    return out


@ui("key-menu", "Keycap with three horizontal lines; the menu key.",
    ["menu key", "context key", "application key", "keyboard key", "keycap", "hamburger key"])
def _(S):
    return [keycap(S), detail(seg(7, 8.5, 17, 8.5)), detail(seg(7, 12, 17, 12)), detail(seg(7, 15.5, 17, 15.5))]


@ui("key-eject", "Keycap with an upward triangle above a flat bar; the eject key.",
    ["eject", "eject key", "open tray", "disc eject", "keyboard key", "keycap"])
def _(S):
    return [keycap(S), tri(S, [(12, 7), (17, 12.3), (7, 12.3)], 0.5), blk(S, 7, 14.3, 10, 2, 0.5)]


@ui("key-enter", "Tall L shaped keycap with a bent return arrow in its lower part; the enter key.",
    ["return key", "enter key", "return", "new line", "keyboard key", "submit key"])
def _(S):
    return [shell(poly([(3, 3), (21, 3), (21, 21), (11, 21), (11, 12.5), (3, 12.5)], closed=True, r=S.r)),
            detail(poly([(17, 7), (17, 15.5), (13.5, 15.5)])), arrow_head(S, (13.5, 15.5), 180, 2.4, detail)]


@ui("arrow-keys", "Four arrow keys laid out in an inverted T, drawn as chevrons.",
    ["cursor keys", "direction keys", "navigation keys", "keyboard arrows", "up down left right", "d-pad keys"])
def _(S):
    return [chev(S, 12, 6.5, 3.4, 3.4, -90), chev(S, 4.5, 17.5, 3.4, 3.4, 180),
            chev(S, 12, 17.5, 3.4, 3.4, 90), chev(S, 19.5, 17.5, 3.4, 3.4, 0)]


# =========================================================================== keyboard and pointer features

def kb_small(S, y=12.5, h=8.5):
    return [shell(rect(2, y, 20, h, S.R * 0.75)), detail(seg(8.5, y + h / 2, 15.5, y + h / 2)),
            pip(S, 5.2, y + h / 2, 0.9, 0.1), pip(S, 18.8, y + h / 2, 0.9, 0.1)]


@ui("keyboard-brightness", "Small keyboard with short rays fanning out above its top edge; the keyboard backlight.",
    ["backlight", "keyboard light", "key illumination", "backlit keys", "keyboard glow", "light level"])
def _(S):
    return [shell(rect(2, 11, 20, 10, S.R * 0.75)), pip(S, 6, 14.5, 1, 0.2), pip(S, 10, 14.5, 1, 0.2),
            pip(S, 14, 14.5, 1, 0.2), pip(S, 18, 14.5, 1, 0.2), detail(seg(7, 17.8, 17, 17.8)),
            line(seg(12, 2.5, 12, 6.5)), line(seg(6, 4.2, 8, 7)), line(seg(18, 4.2, 16, 7))]


@ui("keyboard-language", "Keyboard with a small globe above its right corner; switch the typing language.",
    ["input language", "keyboard layout", "language switch", "multilingual keyboard", "ime", "international keyboard"])
def _(S):
    return [*kb_small(S, 14.5, 7), shell(circle(16, 7.2, 5)), detail(ellipse(16, 7.2, 1.8, 5)), detail(seg(11.5, 7.2, 20.5, 7.2))]


@ui("voice-typing", "Keyboard with a small microphone above its centre; dictate instead of typing.",
    ["dictation", "speech to text", "voice input", "talk to type", "voice keyboard", "mic keyboard"])
def _(S):
    return [*kb_small(S, 14.5, 7),
            Part("dot", rect(10, 1.8, 4, 6.5, 2)),
            line("M7.3 6.3A4.7 4.7 0 0 0 16.7 6.3" if not isL(S) else "M7.3 6.3V7.2L9.5 10.5H14.5L16.7 7.2V6.3")]


@ui("handwriting-input", "Writing area with a looping handwritten stroke ending in a pencil tip.",
    ["handwriting", "pen input", "scribble", "write by hand", "stylus input", "ink"])
def _(S):
    return [shell(rect(2, 3, 20, 18, S.R)),
            detail("M5 14.5C6 10 8.2 10 8.7 12.5S10.6 15 12 12" if not isL(S) else "M5 14.5L7 10.5L9 14.5L12 11.5"),
            detail(seg(15, 16.5, 19, 11.5)), pip(S, 13.8, 17.2, 0.9, 0.1)]


@ui("shortcut-cheatsheet", "Card listing keyboard shortcuts: small key squares each beside a short line of text.",
    ["shortcut list", "hotkeys", "cheat sheet", "keyboard help", "key bindings", "commands list"])
def _(S):
    out = [shell(rect(3, 3, 18, 18, S.R))]
    for y in (7.3, 12, 16.7):
        out += [blk(S, 6, y - 1.4, 3, 2.8, 0.6), detail(seg(12, y, 18, y))]
    return out


@ui("sticky-keys", "Keycap with a shift arrow and a pushpin pressed into its top edge; modifier keys that stay held.",
    ["sticky keys", "key lock", "accessibility keyboard", "hold modifier", "toggle keys", "pinned key"])
def _(S):
    return [shell(rect(2, 7, 20, 14, min(S.R, 3))),
            Part("dot", poly([(10.5, 10), (14.3, 14), (12.2, 14), (12.2, 18), (8.8, 18), (8.8, 14), (6.7, 14)], closed=True)),
            pip(S, 17.5, 2.8, 1.7, 0.2), detail(seg(17.5, 4.5, 17.5, 10))]


@ui("mouse-buttons", "Computer mouse from above with its two top buttons marked and the left one filled.",
    ["left click", "mouse click", "mouse buttons", "primary button", "click", "mouse"])
def _(S):
    return [shell(rect(6, 2, 12, 20, 6 if not isL(S) else 5)), detail(seg(6, 10.5, 18, 10.5)), detail(seg(12, 2, 12, 10.5)),
            Part("dot", rect(7, 3, 4, 6.5, 1.5 if not isL(S) else 0))]


@ui("trackpad-gesture", "Rounded trackpad with two fingertip dots and arrows above them showing a two finger swipe.",
    ["two finger swipe", "touchpad gesture", "scroll gesture", "trackpad swipe", "multitouch", "touchpad"])
def _(S):
    return [shell(rect(2, 3, 20, 18, S.R)), pip(S, 8, 15, 1.8, 0.2), pip(S, 16, 15, 1.8, 0.2),
            line(seg(8, 11, 8, 6.5)), arrow_head(S, (8, 6.5), -90, 2.3),
            line(seg(16, 11, 16, 6.5)), arrow_head(S, (16, 6.5), -90, 2.3)]


@ui("vibration-mode", "Phone outline with a zigzag line on each side showing it vibrating.",
    ["vibrate", "silent mode", "haptic", "buzz", "phone shake", "ringer off"])
def _(S):
    zig = [(5.2, 6.5), (3.4, 9.5), (5.2, 12.5), (3.4, 15.5), (5.2, 18)]
    return [shell(rect(8.5, 2.5, 7, 19, S.R * 0.6)), line(poly(zig, r=S.r * 0.4)),
            line(poly([(24 - x, y) for x, y in zig], r=S.r * 0.4)), pip(S, 12, 18.5, 0.9, 0.1)]


@ui("auto-rotate", "Phone outline with two curved arrows circling around it; automatic screen rotation.",
    ["screen rotation", "rotate screen", "orientation lock", "landscape portrait", "rotate phone", "turn screen"])
def _(S):
    def tip(a):
        return (12 + 9.5 * math.cos(math.radians(a)), 12 + 9.5 * math.sin(math.radians(a)))
    return [shell(rect(8.5, 6.5, 7, 11, S.R * 0.6)),
            line(arc(12, 12, 9.5, 205, 318)), arrow_head(S, tip(318), 318 + 90, 2.6),
            line(arc(12, 12, 9.5, 25, 138)), arrow_head(S, tip(138), 138 + 90, 2.6)]


@ui("system-theme", "Circle split down the middle with a sun at the left and a crescent moon at the right; follow system light or dark.",
    ["auto theme", "light dark auto", "appearance", "match system", "theme switch", "day night"])
def _(S):
    cres = "M17.4 8.3A3.9 3.9 0 1 0 17.4 15.7A3.1 3.1 0 0 1 17.4 8.3Z"
    return [shell(circle(12, 12, 9)), detail(seg(12, 4, 12, 20)), pip(S, 7.3, 12, 1.5, 0.2), Part("dot", cres)]


@ui("blue-light-filter", "Monitor with a small crescent moon on its screen and a warm tinted band across the lower half.",
    ["night light", "night shift", "eye comfort", "warm screen", "reduce blue light", "evening mode"])
def _(S):
    return [shell(rect(2, 3, 20, 14, S.R)), Part("dot", rect(5, 11, 14, 3, 0 if isL(S) else 1)),
            Part("dot", "M9.7 6.2A2.4 2.4 0 1 0 9.7 10.2A1.9 1.9 0 0 1 9.7 6.2Z"), pip(S, 15, 7.5, 0.9, 0.1),
            line(seg(12, 17, 12, 20.5)), line(seg(8, 20.5, 16, 20.5))]
