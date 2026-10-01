"""TypeIcon Core: ui (batch ui_001): windows, bars, layouts, menus and screen patterns.

Shares the interface family's keyshapes so the two sets read as one:
  * screen / panel frame   rect(3, 3, 18, 18, S.R)
  * window                 rect(3, 4, 18, 16, S.R)
  * phone                  rect(5, 2, 14, 20, S.R * .75)
  * monitor                rect(3, 3, 18, 13, S.R) on a stand
Dividers inside a frame are `detail`s (knocked out in Filled). Small marks use `pip()`.
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


# =========================================================================== windows & desktop

@ui("window-restore", "Two overlapping windows offset diagonally; restore a window to its previous size.",
    ["restore down", "unmaximize", "window", "overlap", "resize", "title bar"])
def _(S):
    return [line(poly([(7, 7), (7, 3), (21, 3), (21, 17), (17, 17)], r=S.r)),
            shell(rect(3, 7, 14, 14, S.R * 0.75)), detail(seg(3, 11, 17, 11))]


@ui("window-cascade", "Three windows stacked diagonally from top left to bottom right.",
    ["cascade", "arrange windows", "stack", "overlap", "desktop", "window"])
def _(S):
    return [line(poly([(3, 14), (3, 3), (14, 3)], r=S.r)), line(poly([(7, 17), (7, 7), (17, 7)], r=S.r)),
            shell(rect(11, 11, 10, 10, S.R * 0.6)), detail(seg(11, 14.5, 21, 14.5))]


@ui("window-tile", "Screen divided into four equal windows, each with its own title bar.",
    ["tile windows", "arrange", "grid", "quadrants", "four windows", "split screen"])
def _(S):
    out = []
    for x in (3, 13.5):
        for y in (3, 13.5):
            out += [tile(S, x, y, 7.5, 7.5), detail(seg(x, y + 3, x + 7.5, y + 3))]
    return out


@ui("window-snap", "A window snapped to the left half of the screen beside a dashed empty slot.",
    ["snap", "snap layout", "split screen", "half screen", "arrange", "dock window"])
def _(S):
    return [shell(rect(3, 3, 8, 18, S.R * 0.6)), detail(seg(3, 7, 11, 7)), *dashed_rect(S, 14, 3, 7, 18)]


@ui("pop-out-window", "Arrow leaving a window toward a second, detached window.",
    ["pop out", "detach", "undock", "new window", "open separately", "tear off"])
def _(S):
    return [shell(rect(3, 11, 11, 10, S.R * 0.6)), detail(seg(3, 14.5, 14, 14.5)),
            tile(S, 14, 3, 7, 7), line(poly([(6.5, 8.5), (6.5, 5.5), (10.5, 5.5)], r=S.r)),
            arrow_head(S, (10.5, 5.5), 0, 2.5)]


@ui("virtual-desktops", "Three screens in a row, the middle one active, above a bar.",
    ["workspaces", "virtual desktop", "spaces", "desktops", "task view", "switch desktop"])
def _(S):
    return [shell(rect(8, 5, 8, 9, S.R * 0.5)), blk(S, 2, 7, 3, 5, 1), blk(S, 19, 7, 3, 5, 1),
            line(seg(7, 19, 17, 19))]


@ui("show-desktop", "Monitor with an empty screen and two windows minimised to its bottom edge.",
    ["minimise all", "minimize all", "desktop", "clear screen", "hide windows", "peek"])
def _(S):
    return [shell(rect(3, 3, 18, 13, S.R)), line(seg(12, 16, 12, 20)), line(seg(7, 20.5, 17, 20.5)),
            blk(S, 6, 11, 4, 2), blk(S, 11.5, 11, 4, 2)]


@ui("status-bar", "Top of a phone screen with the time at the left and a battery at the right.",
    ["status bar", "notification bar", "phone", "battery", "time", "signal", "mobile"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(seg(3, 10, 21, 10)), detail(seg(6.5, 6.5, 9.5, 6.5)),
            blk(S, 14, 5.5, 4.5, 2, 0.5)]


@ui("system-tray", "Taskbar corner with an up caret opening a small tray of hidden status icons.",
    ["notification area", "tray", "taskbar", "hidden icons", "status icons", "overflow"])
def _(S):
    return [tile(S, 3, 3, 10, 8), pip(S, 6.5, 7, 1.1, 0.2), pip(S, 9.5, 7, 1.1, 0.2),
            shell(rect(2, 14, 20, 7, S.R * 0.6)), chev(S, 6, 17.5, w=2, h=2, deg=-90, kind=detail),
            pip(S, 12, 17.5, 1.1, 0.1), pip(S, 17, 17.5, 1.1, 0.1)]


@ui("toolbar", "Horizontal bar holding a row of tool buttons, the first one selected.",
    ["tool bar", "tools", "buttons", "action bar", "controls", "editor"])
def _(S):
    return [shell(rect(2, 6, 20, 12, S.R * 0.75)), detail(rect(5, 9, 6, 6, S.R * 0.3)),
            pip(S, 14.5, 12, 1.3, 0.1), pip(S, 18.5, 12, 1.3, 0.1)]


@ui("floating-toolbar", "Small pill of tools hovering above lines of text.",
    ["formatting bar", "context toolbar", "bubble menu", "inline toolbar", "text selection", "floating"])
def _(S):
    pill = rect(4, 3, 16, 7, 1.5 if isL(S) else 3.5)
    return [shell(pill), pip(S, 8, 6.5, 1.1, 0.1), pip(S, 12, 6.5, 1.1, 0.1), pip(S, 16, 6.5, 1.1, 0.1),
            line(seg(3, 15, 21, 15)), line(seg(3, 20, 15, 20))]


@ui("ribbon-toolbar", "Toolbar panel with tabs on top and groups of large and small buttons below.",
    ["ribbon", "command bar", "tabs", "office", "toolbar", "menu bar"])
def _(S):
    return [line(seg(3, 4, 7, 4)), line(seg(10, 4, 14, 4)),
            shell(rect(2, 8, 20, 12, S.R * 0.75)), blk(S, 5, 11, 4, 6),
            detail(seg(12, 8, 12, 20)), pip(S, 15.5, 12, 1.1, 0.1), pip(S, 18.5, 12, 1.1, 0.1),
            pip(S, 15.5, 16, 1.1, 0.1), pip(S, 18.5, 16, 1.1, 0.1)]


@ui("tool-palette", "Tall narrow strip of tool buttons, the top one selected.",
    ["tools panel", "toolbox", "tool bar", "vertical toolbar", "palette", "editor tools"])
def _(S):
    return [shell(rect(7, 2, 10, 20, S.R * 0.75)), blk(S, 9.5, 4.5, 5, 5, 1),
            pip(S, 12, 13, 1.3, 0.1), pip(S, 12, 18, 1.3, 0.1)]


@ui("inspector-panel", "Window with a right-hand panel of label and value rows beside an empty canvas.",
    ["inspector", "properties", "attributes panel", "details pane", "settings panel", "design tool"])
def _(S):
    out = [win(S), detail(seg(11, 4, 11, 20))]
    for y in (8, 12, 16):
        out += [pip(S, 13.75, y, 0.9, 0.1), detail(seg(16, y, 18.5, y))]
    return out


@ui("scrollbar", "Scroll track with arrow buttons at both ends and a thumb near the top.",
    ["scroll bar", "scroll", "thumb", "slider", "overflow", "scrolling"])
def _(S):
    return [shell(rect(7, 2, 10, 20, S.R * 0.75)), chev(S, 12, 5.25, w=2.5, h=2.25, deg=-90, kind=detail),
            blk(S, 10.5, 8.75, 3, 5, 1.5), chev(S, 12, 18.75, w=2.5, h=2.25, deg=90, kind=detail)]


@ui("tab-group", "Row of three browser tabs with a bar under the first two grouping them.",
    ["tab groups", "grouped tabs", "browser tabs", "tab bar", "organise tabs", "organize tabs"])
def _(S):
    k = 1.5 if isL(S) else 2.5

    def tab(x0, x1):
        return f"M{x0} 15V{7 + k}A{k} {k} 0 0 1 {x0 + k} 7H{x1 - k}A{k} {k} 0 0 1 {x1} {7 + k}V15Z"
    return [shell(tab(2, 14)), detail(seg(8, 7, 8, 15)), shell(tab(17, 22)), line(seg(2, 19.5, 14, 19.5))]


@ui("address-bar", "Long rounded field with a small padlock at the left and a web address after it.",
    ["url bar", "address bar", "location bar", "omnibox", "web address", "secure site", "browser"])
def _(S):
    shackle = "M5.75 11.5V10.25A1.5 1.5 0 0 1 8.75 10.25V11.5"
    return [shell(rect(2, 6.5, 20, 11, 2 if isL(S) else 5.5)), detail(shackle), blk(S, 4.75, 11.5, 5, 3.5, 0.75),
            detail(seg(12.5, 12, 14.5, 12)), detail(seg(16.5, 12, 18.5, 12))]


@ui("bookmarks-bar", "Browser window with a strip of small bookmark ribbons under its top bar.",
    ["bookmarks bar", "favourites bar", "favorites bar", "saved links", "browser", "bookmarks toolbar"])
def _(S):
    out = [win(S), detail(seg(3, 8.5, 21, 8.5))]
    for x in (7, 11.5, 16):
        out.append(Part("dot", poly([(x - 1.4, 11), (x + 1.4, 11), (x + 1.4, 16), (x, 14.5), (x - 1.4, 16)], closed=True,
                                    r=0 if isL(S) else 0.4)))
    return out


@ui("quick-settings-panel", "Panel of round quick toggles, some switched on, above a brightness slider.",
    ["quick settings", "control centre", "control center", "toggles", "shortcuts panel", "notification shade"])
def _(S):
    return [frame(S), dot(8.5, 8.5, 2.6), detail(circle(15.5, 8.5, 1.9)),
            detail(circle(8.5, 15.5, 1.9)), dot(15.5, 15.5, 2.6)]


@ui("system-nav-buttons", "Bar holding back triangle, home circle and recent apps square buttons.",
    ["navigation bar", "back button", "home button", "recents", "android", "soft keys", "nav bar"])
def _(S):
    tri = Part("dot", poly([(8.5, 9.75), (8.5, 14.25), (5, 12)], closed=True, r=0 if isL(S) else 0.6))
    return [shell(rect(2, 6, 20, 12, 2 if isL(S) else 6)), tri, pip(S, 12, 12, 2, 0.25), blk(S, 15.25, 10, 4, 4, 1)]


def _star5(cx, cy, ro, ri):
    pts = []
    for i in range(10):
        r = ro if i % 2 == 0 else ri
        a = math.radians(-90 + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


@ui("app-icon", "Rounded app tile with a star in the middle.",
    ["application", "app", "program", "launcher icon", "shortcut", "software"])
def _(S):
    return [shell(rect(3, 3, 18, 18, 3.5 if isL(S) else 6)),
            Part("dot", poly(_star5(12, 12.4, 5.6, 2.4), closed=True, r=0 if isL(S) else 0.5))]


@ui("app-folder", "Rounded tile holding four small app tiles; a folder of apps.",
    ["app group", "folder", "apps", "home screen", "collection", "app library"])
def _(S):
    out = [shell(rect(3, 3, 18, 18, 3.5 if isL(S) else 6))]
    for x in (7, 13):
        for y in (7, 13):
            out.append(blk(S, x, y, 4, 4, 1.2))
    return out


@ui("wallpaper-screen", "Phone whose screen shows a landscape of mountains and a sun.",
    ["wallpaper", "background", "lock screen", "home screen", "backdrop", "personalise", "personalize"])
def _(S):
    return [phone(S), detail(poly([(5, 18.5), (9.5, 13), (12.5, 16), (14.5, 14), (19, 18.5)], r=S.r)),
            pip(S, 14.5, 7.5, 1.6, 0.2)]


@ui("multiple-displays", "Two monitors side by side, the right one smaller.",
    ["dual monitor", "two screens", "extend display", "second screen", "multi monitor", "external display"])
def _(S):
    return [shell(rect(2, 4, 11, 10, S.R * 0.75)), line(seg(7.5, 14, 7.5, 18)), line(seg(4.5, 19, 10.5, 19)),
            shell(rect(16, 7, 6, 7, S.R * 0.5)), line(seg(19, 14, 19, 18)), line(seg(17, 19, 21, 19))]


@ui("theater-mode", "Very wide video frame with a play button and a progress bar beneath.",
    ["theatre mode", "theater mode", "wide player", "cinema mode", "video", "widescreen"])
def _(S):
    play = Part("dot", poly([(10, 7.5), (10, 13.5), (15, 10.5)], closed=True, r=0 if isL(S) else 0.6))
    return [shell(rect(1.5, 4, 21, 13, S.R * 0.75)), play, line(seg(2, 20.5, 22, 20.5))]


@ui("layout-hero", "Page with a large banner block across the top and lines of text below.",
    ["hero section", "banner", "header image", "landing", "above the fold", "jumbotron"])
def _(S):
    return [frame(S), blk(S, 6, 6, 12, 6, 1), detail(seg(6, 15, 18, 15)), detail(seg(6, 18.5, 13, 18.5))]


@ui("layout-holy-grail", "Page layout with a header, a footer and a middle band of left rail, content and right rail.",
    ["holy grail", "three column", "header footer", "page template", "sidebars", "web layout"])
def _(S):
    return [frame(S), detail(seg(3, 7.5, 21, 7.5)), detail(seg(3, 16.5, 21, 16.5)),
            detail(seg(8, 7.5, 8, 16.5)), detail(seg(16, 7.5, 16, 16.5))]


@ui("layout-bento", "Bento grid of uneven cells: one large tile, one tall tile and two small tiles.",
    ["bento grid", "bento box", "tiles", "uneven grid", "cards", "feature grid"])
def _(S):
    return [tile(S, 3, 3, 10, 10), tile(S, 17, 3, 4, 18), blk(S, 2, 16, 5, 6, 1),
            blk(S, 9, 16, 5, 6, 1)]


@ui("layout-feed", "Column of post cards, each with an avatar and lines of text.",
    ["feed", "timeline", "posts", "news feed", "social", "stream"])
def _(S):
    out = []
    for y in (2.5, 13.5):
        out += [tile(S, 4, y, 16, 8), dot(8.25, y + 4, 1.9),
                detail(seg(12, y + 2.5, 16.5, y + 2.5)), detail(seg(12, y + 5.5, 15, y + 5.5))]
    return out


@ui("layout-centered", "Page with a narrow column of text centred between wide empty margins.",
    ["centered layout", "centred", "single column", "reading width", "content column", "article"])
def _(S):
    return [frame(S), detail(seg(9, 8, 15, 8)), detail(seg(9, 12, 15, 12)), detail(seg(9, 16, 15, 16))]


@ui("layout-magazine", "Page with a headline across the top, a big image at the left and text columns at the right.",
    ["magazine layout", "editorial", "article", "news page", "blog layout", "publication"])
def _(S):
    return [frame(S), detail(seg(6, 7, 18, 7)), blk(S, 6, 10, 6, 8, 1),
            detail(seg(15, 11, 18, 11)), detail(seg(15, 14.5, 18, 14.5)),
            detail(seg(15, 18, 18, 18))]


@ui("layout-master-detail", "Window split into a narrow list of rows and a large detail pane.",
    ["master detail", "list detail", "split view", "two pane", "email layout", "inbox"])
def _(S):
    out = [win(S), detail(seg(10, 4, 10, 20)), blk(S, 13, 7.5, 5, 5, 1), detail(seg(13, 16, 18, 16))]
    for y in (8, 12, 16):
        out.append(detail(seg(5.5, y, 7.5, y)))
    return out


@ui("layout-pricing-tiers", "Three pricing cards side by side with the middle one taller and highlighted.",
    ["pricing table", "plans", "tiers", "subscription", "compare plans", "pricing page"])
def _(S):
    mid = D(P(rect(9, 3, 6, 18, 0 if isL(S) else 1.5)), ST(seg(10.75, 8, 13.25, 8), 2))
    if isF(S):
        mid = D(P(rect(8.5, 2.5, 7, 19, 0)), ST(seg(10.75, 8, 13.25, 8), 2))
    return [tile(S, 2.5, 7, 4.5, 12), solid(path_to_d(mid)), tile(S, 17, 7, 4.5, 12)]


@ui("layout-profile-header", "Page with a wide cover strip and a round avatar overlapping its lower edge above text lines.",
    ["profile page", "cover photo", "avatar", "user profile", "account header", "social profile"])
def _(S):
    return [frame(S), detail(seg(3, 9, 4.5, 9)), detail(seg(11.5, 9, 21, 9)), dot(8, 9, 2.75),
            detail(seg(6, 15, 16, 15)), detail(seg(6, 18.5, 12, 18.5))]


@ui("layout-sidebar-both", "Page layout with narrow panels on both the left and right edges around a wide centre.",
    ["two sidebars", "left and right panels", "three pane", "sidebars", "side panels", "app layout"])
def _(S):
    out = [frame(S), detail(seg(8, 3, 8, 21)), detail(seg(16, 3, 16, 21))]
    for y in (7.5, 11.5):
        out += [pip(S, 5.5, y, 0.9, 0.1), pip(S, 18.5, y, 0.9, 0.1)]
    return out


@ui("layout-split-hero", "Banner split in two: text lines and a button at the left, a picture at the right.",
    ["split hero", "hero section", "landing", "two column", "image and text", "banner"])
def _(S):
    return [frame(S), detail(seg(12, 3, 12, 21)), detail(seg(6, 7.5, 9, 7.5)), detail(seg(6, 11, 8, 11)),
            blk(S, 5.5, 14.5, 4, 3, 1),
            detail(poly([(12, 18), (15, 13.5), (17.5, 16), (18.5, 15), (21, 17.5)], r=S.r)), pip(S, 17.5, 7.5, 1.4, 0.2)]


@ui("layout-grid-sidebar", "Window with a narrow left sidebar and a two by two grid of tiles.",
    ["sidebar grid", "gallery", "dashboard", "file browser", "catalogue", "catalog"])
def _(S):
    out = [frame(S), detail(seg(8, 3, 8, 21))]
    for x in (10.5, 15.5):
        for y in (5.5, 13):
            out.append(blk(S, x, y, 3.5, 5.5, 1))
    return out


@ui("column-guides", "Frame filled with tall column bars separated by equal gutters; a column grid.",
    ["column grid", "layout grid", "guides", "gutters", "12 column", "design grid"])
def _(S):
    out = [frame(S)]
    for x in (5.5, 9.5, 13.5, 17.5):
        out.append(blk(S, x, 5.5, 1.5, 13, 0.75))
    return out


@ui("icon-keylines", "Square template with a circle and diagonal guide lines; icon design keylines.",
    ["keyline", "icon grid", "icon template", "guides", "design grid", "pixel grid"])
def _(S):
    c = 3 + S.R * (1 - math.sqrt(0.5))
    return [frame(S), detail(circle(12, 12, 5.5)), detail(seg(c, c, 24 - c, 24 - c)), detail(seg(24 - c, c, c, 24 - c))]


@ui("safe-area", "Phone with a dashed inner area kept clear of its rounded corners and top notch.",
    ["safe area", "insets", "notch", "screen edges", "mobile layout", "cutout"])
def _(S):
    out = [phone(S), detail(seg(10.5, 4.5, 13.5, 4.5))]
    for cx, cy, sx, sy in ((8.5, 8, 1, 1), (15.5, 8, -1, 1), (15.5, 18.5, -1, -1), (8.5, 18.5, 1, -1)):
        out.append(detail(poly([(cx, cy + sy * 2.5), (cx, cy), (cx + sx * 2.5, cy)], r=S.r)))
    return out


@ui("breakpoint-ruler", "Ruler with three markers above it at different widths; responsive breakpoints.",
    ["breakpoints", "responsive", "media query", "screen width", "viewport", "ruler"])
def _(S):
    out = [shell(rect(2, 13, 20, 7, S.R * 0.6))]
    for x in (7, 12, 17):
        out.append(detail(seg(x, 13, x, 16)))
    for x in (5, 12, 19):
        out.append(Part("dot", poly([(x - 2.5, 5), (x + 2.5, 5), (x, 9)], closed=True, r=0 if isL(S) else 0.6)))
    return out


@ui("golden-ratio-grid", "Rectangle divided into shrinking squares with a spiral curling through them.",
    ["golden ratio", "golden spiral", "fibonacci", "composition", "phi", "proportion"])
def _(S):
    inner = [seg(14.5, 5, 14.5, 17.5), seg(14.5, 12.5, 22, 12.5), arc(14.5, 17.5, 12.5, 180, 270), arc(14.5, 12.5, 7.5, 270, 360)]
    if isF(S):  # solid would swallow the spiral: heavy outline with the smallest square filled instead
        return [line(rect(2, 5, 20, 12.5, 1)), *(line(d) for d in inner), solid(rect(14.5, 12.5, 7.5, 5))]
    return [shell(rect(2, 5, 20, 12.5, S.R * 0.5)), *(detail(d) for d in inner)]


@ui("cascading-menu", "Menu list with one row open and a submenu opening beside it.",
    ["submenu", "nested menu", "flyout menu", "context menu", "dropdown", "multi level menu"])
def _(S):
    return [tile(S, 2, 3, 10.5, 14), detail(seg(4.5, 7, 10, 7)), detail(seg(4.5, 10.5, 7, 10.5)),
            chev(S, 9.5, 10.5, w=1.5, h=1.5, deg=0, kind=detail), detail(seg(4.5, 14, 10, 14)),
            tile(S, 15.5, 8.5, 6.5, 12.5), detail(seg(18, 12.5, 19.5, 12.5)), detail(seg(18, 16.5, 19.5, 16.5))]


@ui("radial-menu", "Round menu split into four segments around a centre dot, one segment highlighted.",
    ["pie menu", "radial menu", "circular menu", "marking menu", "wheel menu", "context menu"])
def _(S):
    diag = [seg(*pt(12, 12, 4.5, a), *pt(12, 12, 9, a)) for a in (-135, -45, 45, 135)]
    out = [shell(circle(12, 12, 9)), dot(12, 12, 2), *(detail(d) for d in diag)]
    if not isF(S):
        wedge = P(poly([(12, 12), pt(12, 12, 14, -135), pt(12, 12, 14, -90), pt(12, 12, 14, -45)], closed=True))
        seg_ = D(I_(P(circle(12, 12, 9)), wedge), P(circle(12, 12, 4.5)), *(ST(d, 2) for d in diag[:2]))
        out.append(solid(path_to_d(seg_)))
    return out


@ui("navigation-rail", "Window with a narrow bar of icon buttons down its left edge.",
    ["nav rail", "side navigation", "icon bar", "activity bar", "left rail", "app navigation"])
def _(S):
    return [frame(S), detail(seg(9, 3, 9, 21)), pip(S, 6, 7.5, 1.2, 0.1), pip(S, 6, 12, 1.2, 0.1), pip(S, 6, 16.5, 1.2, 0.1)]


@ui("navigation-drawer", "Phone with a menu panel slid in from the left over a dimmed screen.",
    ["nav drawer", "side menu", "slide out menu", "off canvas", "hamburger menu", "drawer"])
def _(S):
    out = [phone(S), detail(seg(14, 2, 14, 22))]
    for y, x1 in ((7, 11.5), (11, 10.5), (15, 11.5)):
        out.append(detail(seg(7.5, y, x1, y)))
    return out


@ui("bottom-sheet", "Phone with a rounded sheet risen from the bottom edge, a grab bar on top.",
    ["bottom sheet", "sheet", "drawer", "panel", "mobile", "slide up"])
def _(S):
    k = 1.5 if isL(S) else 2.5
    edge = f"M5 {11 + k}A{k} {k} 0 0 1 {5 + k} 11H{19 - k}A{k} {k} 0 0 1 19 {11 + k}"
    return [phone(S), detail(edge), detail(seg(10.5, 15, 13.5, 15))]


@ui("action-sheet", "Group of stacked option buttons above a separate cancel button.",
    ["action sheet", "options menu", "share sheet", "choices", "mobile menu", "cancel"])
def _(S):
    return [shell(rect(3, 2.5, 18, 12, S.R * 0.75)), detail(seg(3, 6.5, 21, 6.5)), detail(seg(3, 10.5, 21, 10.5)),
            shell(rect(3, 17.5, 18, 4, S.R * 0.5))]


@ui("segmented-control", "Pill divided into three segments with the first one selected.",
    ["segmented control", "segmented button", "button group", "toggle group", "tabs", "switcher"])
def _(S):
    k = 2 if isL(S) else 5
    out = [shell(rect(2, 7, 20, 10, k)), detail(seg(8.67, 7, 8.67, 17)), detail(seg(15.33, 7, 15.33, 17))]
    if not isF(S):
        out.append(solid(path_to_d(D(I_(P(rect(2, 7, 20, 10, k)), P(rect(2, 7, 6.67, 10))),
                                     ST(seg(8.67, 7, 8.67, 17), 2)))))
    return out


_INF = ("M12 17C10.3 15 9 14 7.2 14A3 3 0 0 0 7.2 20C9 20 10.3 19 12 17C13.7 15 15 14 16.8 14"
        "A3 3 0 0 1 16.8 20C15 20 13.7 19 12 17Z")


@ui("infinite-scroll", "List rows fading out above an infinity sign; endless scrolling.",
    ["infinite scroll", "endless feed", "lazy loading", "continuous scroll", "feed", "pagination"])
def _(S):
    return [line(seg(3, 3.5, 21, 3.5)), line(seg(3, 8.5, 9, 8.5)), line(seg(13, 8.5, 18, 8.5)), line(_INF)]


@ui("load-more", "List rows above a wide button holding three dots.",
    ["load more", "show more", "more results", "see more", "next page", "expand list"])
def _(S):
    return [line(seg(3, 3.5, 21, 3.5)), line(seg(3, 8.5, 21, 8.5)), shell(rect(3, 13, 18, 8, S.R * 0.75)),
            pip(S, 8, 17, 1.1, 0.1), pip(S, 12, 17, 1.1, 0.1), pip(S, 16, 17, 1.1, 0.1)]


@ui("pull-refresh-gesture", "Phone with its list pulled down and a refresh arrow in the gap at the top.",
    ["pull to refresh", "swipe down", "reload", "refresh", "update feed", "mobile gesture"])
def _(S):
    return [phone(S), detail(arc(12, 8.25, 3, -30, 215)),
            arrow_head(S, pt(12, 8.25, 3, 215), 305, 2.25, kind=detail),
            detail(seg(5, 13.5, 19, 13.5)), detail(seg(8, 17.5, 16, 17.5))]


@ui("list-swipe-actions", "List row slid sideways to reveal two action buttons at its end.",
    ["swipe actions", "swipe to delete", "row actions", "slide", "mobile list", "archive"])
def _(S):
    return [line(seg(3, 3.5, 21, 3.5)), tile(S, 2, 8.5, 10, 7), blk(S, 14.5, 7.5, 3, 9, 0.75), blk(S, 19, 7.5, 3, 9, 0.75),
            line(seg(3, 20.5, 21, 20.5))]


@ui("reorder-list", "List rows with grip handles, the middle row lifted out of line to move it.",
    ["reorder", "drag and drop", "sort list", "rearrange", "move row", "sortable"])
def _(S):
    out = []
    for y in (3.5, 20.5):
        out += [line(seg(3, y, 5, y)), line(seg(8.5, y, 21, y))]
    out += [tile(S, 5, 8.5, 17, 7), detail(seg(8, 10.75, 10, 10.75)), detail(seg(8, 13.25, 10, 13.25)),
            detail(seg(13, 12, 19, 12))]
    return out


@ui("reading-progress", "Page with a progress bar across its top, two thirds filled.",
    ["reading progress", "scroll progress", "progress bar", "article", "read time", "scroll indicator"])
def _(S):
    out = [frame(S), detail(seg(3, 7.5, 21, 7.5)), detail(seg(7, 12, 17, 12)), detail(seg(7, 16, 14, 16))]
    if isF(S):
        out.append(detail(seg(15.5, 5, 19.5, 5)))
    else:
        out.append(solid(path_to_d(I_(P(rect(3, 3, 12.5, 4.5)), P(rect(3, 3, 18, 18, S.R))))))
    return out


@ui("focus-ring", "Button surrounded by an offset outline ring; keyboard focus indicator.",
    ["focus ring", "focus outline", "keyboard focus", "focus visible", "accessibility", "selected control"])
def _(S):
    return [line(rect(2.5, 5, 19, 14, 2.5 if isL(S) else 7)), shell(rect(6.5, 9, 11, 6, 1 if isL(S) else 3)),
            detail(seg(9.5, 12, 14.5, 12))]


@ui("skip-to-content", "Page with a small button in the header and an arrow jumping down past it to the content.",
    ["skip link", "skip navigation", "jump to content", "accessibility", "keyboard", "bypass"])
def _(S):
    path = "M13 6H17.5V17" if isL(S) else "M13 6H15A2.5 2.5 0 0 1 17.5 8.5V17"
    return [frame(S), detail(seg(3, 9, 21, 9)), blk(S, 5.5, 5, 5, 2, 0.75), detail(path),
            arrow_head(S, (17.5, 17.5), 90, 2.25, kind=detail),
            detail(seg(6.5, 13, 12.5, 13)), detail(seg(6.5, 17, 11, 17))]


@ui("tab-bar-mobile", "Phone with a bottom tab bar of icon buttons, the first one selected.",
    ["tab bar", "bottom navigation", "bottom tabs", "mobile nav", "app tabs", "navigation bar"])
def _(S):
    return [phone(S), detail(seg(5, 16, 19, 16)), pip(S, 8.5, 19, 1.3, 0.1), dot(12, 19, 0.9), dot(15.5, 19, 0.9)]


@ui("confirmation-dialog", "Dialog card with two lines of text and a pair of buttons, one filled.",
    ["confirm", "confirmation", "alert dialog", "are you sure", "prompt", "ok cancel"])
def _(S):
    return [shell(rect(2, 4, 20, 16, S.R)), detail(seg(6, 8.5, 18, 8.5)), detail(seg(6, 12, 13, 12)),
            detail(seg(6.5, 16, 10, 16)), blk(S, 13, 14.5, 5.5, 3, 1)]


@ui("input-dialog", "Dialog card with a title, an empty text field and a filled button.",
    ["prompt", "input dialog", "rename", "enter text", "text entry", "form dialog"])
def _(S):
    return [shell(rect(2, 3, 20, 18, S.R)), detail(seg(6, 7, 12, 7)), detail(rect(6, 10.5, 12, 3, 0.5 if isL(S) else 1.5)),
            blk(S, 12.5, 16, 5.5, 2.5, 1)]


@ui("coach-mark", "Dimmed screen with a spotlight on one button and a tooltip pointing at it.",
    ["coach mark", "onboarding tip", "product tour", "walkthrough", "spotlight", "feature hint"])
def _(S):
    tip = poly([(12, 5.5), (18, 5.5), (18, 10), (14, 10), (12, 12)], closed=True, r=S.r * 0.4)
    if isF(S):
        body = D(P(rect(2, 2, 20, 20, 2)), P(circle(8.5, 15.5, 4)), ST(tip, 2))
        return [solid(path_to_d(U(body, P(circle(8.5, 15.5, 1.75)))))]
    return [frame(S), detail(circle(8.5, 15.5, 3)), dot(8.5, 15.5, 1.1), detail(tip)]


@ui("notification-banner", "Screen with a wide notification bar across its top holding a bell and a line of text.",
    ["banner", "notification", "alert bar", "announcement", "heads up", "top banner"])
def _(S):
    if isF(S):
        body = U(D(P(rect(1, 3, 22, 18, 3)), P(rect(5, 7, 14, 5, 1))), P(circle(7.75, 9.5, 1.25)), ST(seg(10.5, 9.5, 16.5, 9.5), 2))
        return [solid(path_to_d(body))]
    band = D(P(rect(5, 7, 14, 5, 0 if isL(S) else 1.5)), P(circle(7.75, 9.5, 1.1)), ST(seg(10.5, 9.5, 16.5, 9.5), 1.5))
    return [shell(rect(2, 4, 20, 16, S.R)), solid(path_to_d(band))]


@ui("push-notification", "Phone with a notification card near the top showing an app square and text.",
    ["push notification", "alert", "message preview", "mobile notification", "lock screen", "heads up"])
def _(S):
    card = rect(6.5, 4.5, 11, 6, 0 if isL(S) else 1.5)
    marks = [P(rect(8, 6.25, 2.5, 2.5, 0 if isL(S) else 0.75)), ST(seg(12, 7.5, 16, 7.5), 1.5)]
    texts = [seg(8.5, 14.5, 15.5, 14.5), seg(8.5, 18, 13, 18)]
    if isF(S):
        body = U(D(P(rect(4, 1, 16, 22, 2.5)), P(rect(6.5, 4.5, 11, 6, 1)), *(ST(t, 2) for t in texts)), *marks)
        return [solid(path_to_d(body))]
    return [shell(rect(5, 2, 14, 20, S.R * 0.75)), solid(path_to_d(D(P(card), *marks))), *(detail(t) for t in texts)]


@ui("skeleton-loader", "Card of placeholder shapes, a circle and thick bars, shown while content loads.",
    ["skeleton screen", "placeholder", "loading state", "shimmer", "content loader", "ghost"])
def _(S):
    return [shell(rect(2, 4, 20, 16, S.R)), dot(7.5, 9.5, 2.5),
            blk(S, 11.5, 7, 7, 2.5, 1.25), blk(S, 11.5, 10.5, 4.5, 2.5, 1.25), blk(S, 5, 15, 14, 2.5, 1.25)]


@ui("splash-screen", "Phone showing a bold round logo in the middle and a small spinner near the bottom.",
    ["splash screen", "launch screen", "app start", "loading screen", "startup", "boot"])
def _(S):
    return [phone(S), dot(12, 10, 4), dot(9.75, 18, 0.9), dot(12, 18, 0.9), dot(14.25, 18, 0.9)]


@ui("onboarding-screens", "Phone with a picture, a line of text and three page dots; welcome screens.",
    ["onboarding", "welcome screens", "intro", "walkthrough", "get started", "tutorial"])
def _(S):
    return [phone(S), blk(S, 8.5, 5.5, 7, 5.5, 1), detail(seg(8.5, 14, 15.5, 14)),
            detail(seg(8.5, 18, 10.5, 18)), dot(13.25, 18, 1), dot(15.5, 18, 1)]


@ui("login-form", "Avatar above a username field and a password field with hidden characters.",
    ["login", "log in", "sign in", "authentication", "credentials", "password field"])
def _(S):
    k = min(S.R * 0.5, 1.5)
    out = [shell(circle(12, 4.5, 2.5)), shell(rect(3, 9.5, 18, 4, k)), shell(rect(3, 17, 18, 4, k))]
    out += [pip(S, x, 19, 0.9, 0.1) for x in (7, 10.5, 14)]
    return out


@ui("signup-form", "Form of stacked fields, a tick box and a wide filled button.",
    ["sign up", "register", "registration", "create account", "join", "onboarding form"])
def _(S):
    k = min(S.R * 0.5, 1.5)
    return [shell(rect(3, 3, 18, 3.5, k)), shell(rect(3, 9, 18, 3.5, k)), blk(S, 3, 14.5, 2.5, 2.5, 0.6),
            line(seg(8, 15.75, 15, 15.75)), blk(S, 2, 19, 20, 3.5, 1.75)]


@ui("consent-banner", "Screen with a bar across its bottom holding a round cookie and two small buttons.",
    ["cookie banner", "cookie consent", "privacy notice", "gdpr", "consent", "accept cookies"])
def _(S):
    return [line(poly([(3, 10), (3, 3), (21, 3), (21, 10)], r=S.R)), shell(rect(2, 13, 20, 8, S.R * 0.75)),
            detail(circle(6.75, 17, 1.75)), blk(S, 11, 15.75, 3.5, 2.5, 0.75), blk(S, 16, 15.75, 3.5, 2.5, 0.75)]


@ui("chat-launcher", "Round floating chat button in the bottom right corner of a page.",
    ["chat widget", "live chat", "support chat", "chat bubble", "help button", "messenger"])
def _(S):
    bub = "M14.5 13.5H19.5V17.5H16.5L14.5 19Z" if isL(S) else "M15.3 13.5H18.7A0.8 0.8 0 0 1 19.5 14.3V16.7A0.8 0.8 0 0 1 18.7 17.5H16.5L14.5 19V14.3A0.8 0.8 0 0 1 15.3 13.5Z"
    return [line(poly([(10, 21), (3, 21), (3, 3), (21, 3), (21, 10)], r=S.R)), line(seg(7, 7.5, 14, 7.5)),
            shell(circle(17, 16.25, 5)), Part("dot", bub)]
