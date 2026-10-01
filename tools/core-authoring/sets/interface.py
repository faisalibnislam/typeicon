"""TypeIcon Core: interface & layout.

Visual language: UI chrome is drawn from a few shared keyshapes so the family reads as one set at 16 px:
  * screen / panel frame   rect(3, 3, 18, 18, S.R)       (layouts, tables, frames)
  * window                 rect(3, 4, 18, 16, S.R)       (window, app-window, browser, modal)
  * control / field        rect(2, 6, 20, 12, S.R * .75) (button, input, search field, toast)
Dividers inside a frame are `detail`s, so Filled becomes a solid panel with knocked-out gutters.
Small marks use `pip()`: square in Line (crisp), round in Rounded, a slightly larger disc in Filled.

Every icon's Filled design is built from `fn(FILL)` (a pseudo-style with Line geometry), so a drawing can
branch on `isF(S)` where the solid version needs its own geometry.
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, P, ST, U, Part, Style, arc, circle, detail, dot, ellipse, filled_region, fmt, icon, line, path_to_d, poly,
    rect, regular, seg, shell, solid,
)

CAT = "interface"
FILL = Style("filled", "butt", "miter", R=2.0, r=0.0)  # pseudo-style: parts for the Filled design


def isF(S) -> bool:
    return S.name == "filled"


def isL(S) -> bool:
    return S.name != "rounded"


def ui(name, description, tags, aliases=()):
    """Register an interface icon whose Filled design is built from `fn(FILL)`."""
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


def frame(S):
    return shell(rect(3, 3, 18, 18, S.R))


def win(S, y0=4.0, h=16.0):
    return shell(rect(3, y0, 18, h, S.R))


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
    """Rectangle drawn as corner Ls plus one centred dash per side (gaps >= 2 px in every style)."""
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


# =========================================================================== layouts

@ui("dashboard", "Dashboard made of a tall panel, a round gauge widget and a small tile.",
    ["overview", "panel", "widgets", "home", "analytics", "admin"])
def _(S):
    return [tile(S, 3, 3, 7, 18), shell(circle(17.5, 6.5, 3.5)), tile(S, 14, 14, 7, 7)]


@ui("sidebar", "Panel with a sidebar on the left; show or hide the sidebar.",
    ["panel", "side panel", "navigation", "drawer", "toggle sidebar", "left"], aliases=["panel-left"])
def _(S):
    return [frame(S), detail(seg(9, 3, 9, 21))]


@ui("sidebar-right", "Panel with a sidebar on the right; show or hide the inspector.",
    ["panel", "side panel", "inspector", "drawer", "details", "right"], aliases=["panel-right"])
def _(S):
    return [frame(S), detail(seg(15, 3, 15, 21))]


@ui("layout-columns", "Page layout divided into three columns.",
    ["columns", "layout", "three columns", "split", "grid"], aliases=["columns"])
def _(S):
    return [frame(S), detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21))]


@ui("layout-rows", "Page layout divided into three rows.",
    ["rows", "layout", "stack", "sections", "horizontal"])
def _(S):
    return [frame(S), detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15))]


@ui("layout-grid", "Page layout divided into a two-by-two grid of cells.",
    ["grid", "layout", "quadrants", "cells", "tiles"])
def _(S):
    return [frame(S), detail(seg(12, 3, 12, 21)), detail(seg(3, 12, 21, 12))]


@ui("layout-sidebar", "Page layout with a header and a left sidebar.",
    ["layout", "sidebar", "header", "template", "app shell"])
def _(S):
    return [frame(S), detail(seg(3, 8, 21, 8)), detail(seg(9, 8, 9, 21))]


@ui("layout-bottombar", "Screen layout with a bar along the bottom, like a tab bar.",
    ["layout", "tab bar", "bottom navigation", "footer", "mobile"], aliases=["layout-footer"])
def _(S):
    return [frame(S), detail(seg(3, 16, 21, 16))]


@ui("layout-navbar", "Screen layout with a navigation bar across the top.",
    ["layout", "header", "top bar", "navigation bar", "app bar"], aliases=["layout-header"])
def _(S):
    return [frame(S), detail(seg(3, 8, 21, 8))]


@ui("layout-cards", "Card layout: one wide card above two small cards.",
    ["cards", "layout", "tiles", "feed", "gallery"])
def _(S):
    return [tile(S, 3, 3, 18, 8), tile(S, 3, 15, 7, 6), tile(S, 14, 15, 7, 6)]


@ui("layout-list", "List layout of full-width rows.",
    ["list view", "rows", "layout", "stacked", "feed"])
def _(S):
    return [tile(S, 3, 3, 18, 7), detail(seg(7, 6.5, 14, 6.5)), tile(S, 3, 14, 18, 7), detail(seg(7, 17.5, 14, 17.5))]


@ui("layout-masonry", "Masonry layout: two columns of tiles with staggered heights.",
    ["masonry", "pinterest", "gallery", "staggered", "tiles", "layout"])
def _(S):
    return [tile(S, 3, 3, 7, 9), tile(S, 3, 16, 7, 5), tile(S, 14, 3, 7, 5), tile(S, 14, 12, 7, 9)]


@ui("table", "Table with a header row and two columns.",
    ["spreadsheet", "grid", "rows", "columns", "data", "cells"])
def _(S):
    return [frame(S), detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15)), detail(seg(10, 3, 10, 21))]


@ui("kanban", "Kanban board: three columns holding different numbers of cards.",
    ["board", "columns", "tasks", "project", "agile", "trello"], aliases=["kanban-board"])
def _(S):
    return [frame(S), detail(seg(7.5, 7, 7.5, 17)), detail(seg(12, 7, 12, 12)), detail(seg(16.5, 7, 16.5, 14))]


# =========================================================================== windows

@ui("window", "Application window with a title bar.",
    ["window", "app", "desktop", "frame", "screen"])
def _(S):
    return [win(S), detail(seg(3, 9, 21, 9))]


@ui("app-window", "Application window with window controls in the title bar.",
    ["application", "window", "program", "desktop", "macos"])
def _(S):
    return [win(S), detail(seg(3, 10, 21, 10)), pip(S, 6.5, 7, 1, 0.25), pip(S, 10, 7, 1, 0.25)]


@ui("browser", "Web browser window with an open tab.",
    ["web", "internet", "website", "page", "tab"], aliases=["web-browser"])
def _(S):
    return [win(S), detail(poly([(10, 4), (10, 9), (21, 9)], r=S.r))]


@ui("tabs", "Panel with a row of three tabs; the first one is active.",
    ["tab bar", "tabbed", "navigation", "pages", "switch"])
def _(S):
    return [frame(S), detail(seg(9, 3, 9, 8)), detail(seg(15, 3, 15, 8)), detail(seg(9, 8, 21, 8))]


# =========================================================================== controls

def _pill(S):
    return shell(rect(2, 5, 20, 14, 3.5 if isL(S) else 7))


@ui("toggle-on", "Switch turned on: knob on the right.",
    ["switch", "on", "enabled", "active", "setting"], aliases=["switch-on"])
def _(S):
    return [_pill(S), dot(15, 12, 4)]


@ui("toggle-off", "Switch turned off: hollow knob on the left.",
    ["switch", "off", "disabled", "inactive", "setting"], aliases=["switch-off"])
def _(S):
    return [_pill(S), detail(circle(9, 12, 3))]


@ui("slider-horizontal", "Horizontal slider: a track with a round knob.",
    ["slider", "range", "volume", "seek", "control", "input"], aliases=["range-slider"])
def _(S):
    return [line(seg(3, 12, 6, 12)), shell(circle(9, 12, 3)), line(seg(12, 12, 21, 12))]


@ui("checkbox", "Empty checkbox.", ["check box", "unchecked", "option", "form", "select", "todo"], aliases=["checkbox-empty"])
def _(S):
    if isF(S):
        return [solid(path_to_d(D(P(rect(2, 2, 20, 20, 2.5)), P(rect(5, 5, 14, 14, 1)))))]
    return [frame(S)]


@ui("checkbox-checked", "Ticked checkbox.", ["checked", "check box", "selected", "done", "form", "todo"])
def _(S):
    return [frame(S), detail(poly([(7.5, 12), (10.5, 15), (16.5, 9)], r=S.r))]


def _radio_label(S):
    return [line(seg(15.5, 9.5, 21, 9.5)), line(seg(15.5, 14.5, 19, 14.5))]


@ui("radio-button", "Empty radio button beside its label.", ["radio", "option", "unselected", "choice", "form"])
def _(S):
    if isF(S):
        return [solid(path_to_d(D(P(circle(7.5, 12, 5.5)), P(circle(7.5, 12, 3))))), *_radio_label(S)]
    return [shell(circle(7.5, 12, 4.5)), *_radio_label(S)]


@ui("radio-selected", "Selected radio button beside its label.", ["radio", "option", "selected", "choice", "form", "checked"],
    aliases=["radio-checked"])
def _(S):
    if isF(S):
        ring = D(P(circle(7.5, 12, 5.5)), P(circle(7.5, 12, 3.75)))
        return [solid(path_to_d(U(ring, P(circle(7.5, 12, 2.25))))), *_radio_label(S)]
    return [shell(circle(7.5, 12, 4.5)), dot(7.5, 12, 2), *_radio_label(S)]


def _field(S, y=6.0, h=12.0):
    return shell(rect(2, y, 20, h, S.R * 0.75))


@ui("dropdown", "Select box with a downward chevron.", ["select", "combo box", "picker", "menu", "options", "form"],
    aliases=["select-box"])
def _(S):
    return [_field(S), detail(seg(6, 12, 10, 12)), chev(S, 16, 12, w=3, h=3, kind=detail)]


@ui("button", "Push button with a label.", ["cta", "action", "control", "submit", "click"])
def _(S):
    return [_field(S), detail(seg(8, 12, 16, 12))]


@ui("input-field", "Text input field with a caret.", ["text field", "text box", "input", "form", "type"],
    aliases=["text-field", "textbox"])
def _(S):
    return [_field(S), detail(seg(6.5, 9, 6.5, 15))]


@ui("form", "Form with a labelled field and a button.", ["fields", "sign up", "survey", "input", "submit"])
def _(S):
    return [line(seg(3, 3.5, 11, 3.5)), shell(rect(3, 7.5, 18, 5, S.R * 0.5)), shell(rect(3, 17, 9, 4, S.R * 0.5))]


@ui("search-field", "Search box with a magnifying glass.", ["search bar", "find", "query", "input", "lookup"],
    aliases=["search-bar", "search-box"])
def _(S):
    return [_field(S, 5, 14), detail(circle(8, 11.5, 2.5)), detail(seg(9.9, 13.4, 11.5, 15)), detail(seg(15, 12, 18, 12))]


# =========================================================================== lists

@ui("list-checks", "Checklist: rows each with a tick.", ["checklist", "todo", "tasks", "done", "list"], aliases=["checklist"])
def _(S):
    out = []
    for y in (5.5, 12, 18.5):
        out += [line(poly([(3, y), (5, y + 2), (8.5, y - 1.5)], r=S.r)), line(seg(12, y, 21, y))]
    return out


@ui("list-ordered", "Numbered list with rows 1 and 2.", ["numbered", "ordered list", "numbers", "steps", "list"],
    aliases=["numbered-list"])
def _(S):
    two = "M3.5 15.5C3.5 14.2 4.6 13.5 6 13.5C7.4 13.5 8.5 14.3 8.5 15.8C8.5 17.6 3.5 18.8 3.5 21H8.5"
    return [line(poly([(3.5, 5), (6, 3), (6, 10)], r=S.r)), line(two),
            line(seg(12, 6.5, 21, 6.5)), line(seg(12, 17.5, 21, 17.5))]


@ui("list-tree", "Tree list: an item with two nested children.", ["tree", "hierarchy", "outline", "nested", "structure"],
    aliases=["tree-view"])
def _(S):
    return [pip(S, 4.5, 4.5), line(seg(8.5, 4.5, 18, 4.5)),
            line(poly([(4.5, 8.5), (4.5, 18.5), (8, 18.5)], r=S.r)), line(seg(4.5, 12, 8, 12)),
            line(seg(11.5, 12, 21, 12)), line(seg(11.5, 18.5, 21, 18.5))]


@ui("list-details", "Detailed list: rows with a thumbnail, title and subtitle.",
    ["details", "list view", "media list", "rows", "thumbnails"])
def _(S):
    out = []
    for y in (3, 14):
        out += [tile(S, 3, y, 7, 7), line(seg(13, y + 1.5, 21, y + 1.5)), line(seg(13, y + 5.5, 18, y + 5.5))]
    return out


# =========================================================================== handles & overflow

@ui("more-horizontal", "Three dots in a row; more options.", ["more", "options", "ellipsis", "overflow", "menu", "meatballs"],
    aliases=["ellipsis", "dots-horizontal"])
def _(S):
    return [pip(S, x, 12) for x in (5, 12, 19)]


@ui("more-vertical", "Three stacked dots; more options.", ["more", "options", "kebab", "overflow", "menu", "vertical"],
    aliases=["dots-vertical"])
def _(S):
    return [pip(S, 12, y) for y in (5, 12, 19)]


@ui("grip-vertical", "Six-dot grip in two columns; drag to move.", ["drag", "grip", "handle", "reorder", "move"])
def _(S):
    return [pip(S, x, y, 1.5) for x in (9, 15) for y in (5, 12, 19)]


@ui("grip-horizontal", "Six-dot grip in two rows; drag to move.", ["drag", "grip", "handle", "reorder", "move"])
def _(S):
    return [pip(S, x, y, 1.5) for x in (5, 12, 19) for y in (9, 15)]


@ui("drag-handle", "Two bars between up and down chevrons; drag to reorder.",
    ["drag", "reorder", "sort", "handle", "move", "rearrange"])
def _(S):
    return [chev(S, 12, 4.75, w=3.5, h=3.5, deg=-90), line(seg(4, 10, 20, 10)), line(seg(4, 14, 20, 14)),
            chev(S, 12, 19.25, w=3.5, h=3.5, deg=90)]


@ui("adjustments", "Two tracks with upright bar knobs; adjust or tune.", ["tune", "adjust", "controls", "settings", "equalizer", "mixer"],
    aliases=["tune"])
def _(S):
    out = []
    for y, x in ((7, 15), (17, 9)):
        out += [line(seg(3, y, 21, y)), line(seg(x, y - 3.5, x, y + 3.5))]
    return out


def _hslider(S, y, x, r=2.0):
    return [line(seg(3, y, x - r, y)), shell(circle(x, y, r)), line(seg(x + r, y, 21, y))]


@ui("sliders-horizontal", "Three horizontal sliders with round knobs; filters or settings.",
    ["sliders", "filters", "controls", "settings", "preferences", "options"], aliases=["filters"])
def _(S):
    return _hslider(S, 5, 15) + _hslider(S, 12, 8) + _hslider(S, 19, 14)


@ui("sliders-vertical", "Three vertical sliders with round knobs; mixer or levels.",
    ["sliders", "mixer", "equalizer", "levels", "controls", "settings"])
def _(S):
    out = []
    for x, y in ((5, 8), (12, 15), (19, 10)):
        out += [line(seg(x, 3, x, y - 2)), shell(circle(x, y, 2)), line(seg(x, y + 2, x, 21))]
    return out


# =========================================================================== system

@ui("command", "Command key symbol (⌘); keyboard shortcut.", ["cmd", "shortcut", "mac", "keyboard", "hotkey", "key"],
    aliases=["cmd"])
def _(S):
    if isL(S):
        k = 1.75  # outer loop corners softened a little so the crisp version still reads as a loop
        d = (f"M9 9V{3 + k}Q9 3 {9 - k} 3H{3 + k}Q3 3 3 {3 + k}V9H{21 - k}Q21 9 21 {9 - k}V{3 + k}Q21 3 {21 - k} 3H{15 + k}Q15 3 15 {3 + k}"
             f"V21H{21 - k}Q21 21 21 {21 - k}V{15 + k}Q21 15 {21 - k} 15H{3 + k}Q3 15 3 {15 + k}V{21 - k}Q3 21 {3 + k} 21H{9 - k}Q9 21 9 {21 - k}Z")
    else:
        d = ("M9 9V6A3 3 0 1 0 6 9H18A3 3 0 1 0 15 6V18A3 3 0 1 0 18 15H6A3 3 0 1 0 9 18Z")
    return [line(d)]


@ui("keyboard-shortcut", "Keycap seen from above; keyboard shortcut or hotkey.",
    ["hotkey", "keycap", "key", "shortcut", "keyboard", "control"], aliases=["hotkey", "keycap"])
def _(S):
    c = 3 + S.R * (1 - math.sqrt(0.5))  # where the frame's corner arc meets the diagonal
    return [frame(S), detail(rect(7, 6, 10, 9, S.R * 0.5)),
            detail(seg(c, c, 7, 6)), detail(seg(24 - c, c, 17, 6)), detail(seg(c, 24 - c, 7, 15)), detail(seg(24 - c, 24 - c, 17, 15))]


@ui("spinner", "Eight radial strokes; loading in progress.", ["loading", "busy", "wait", "progress", "activity"],
    aliases=["activity-indicator"])
def _(S):
    out = []
    for i in range(8):
        a = math.radians(i * 45 - 90)
        c, s_ = math.cos(a), math.sin(a)
        out.append(line(seg(12 + 5.5 * c, 12 + 5.5 * s_, 12 + 9 * c, 12 + 9 * s_)))
    return out


@ui("loader", "Ring of dots shrinking around a circle; loading.", ["loading", "wait", "busy", "progress", "buffering"])
def _(S):
    sizes = [2.1, 1.9, 1.7, 1.5, 1.35, 1.2, 1.05]
    out = []
    for i, r in enumerate(sizes):
        a = math.radians(-90 + i * 45)
        out.append(pip(S, 12 + 8 * math.cos(a), 12 + 8 * math.sin(a), r, 0.35))
    return out


@ui("progress-bar", "Progress bar, partly filled.", ["progress", "loading", "percent", "completion", "status", "upload"])
def _(S):
    if isF(S):
        body = D(P(rect(1, 6, 22, 12, 2)), P(rect(14, 9, 5, 6, 0.5)))
        return [solid(path_to_d(body))]
    return [shell(rect(2, 7, 20, 10, 1.5 if isL(S) else 5)), solid(rect(5, 10, 8, 4, 0 if isL(S) else 2))]


@ui("notification-dot", "App tile with a dot badge on its corner; unread notification.",
    ["badge", "unread", "notification", "alert", "new", "indicator"], aliases=["badge-dot"])
def _(S):
    if isF(S):
        body = U(D(P(rect(2, 2, 20, 20, 2)), P(circle(18, 6, 6))), P(circle(18, 6, 3.75)))
        return [solid(path_to_d(body))]
    return [line(poly([(12, 3), (3, 3), (3, 21), (21, 21), (21, 12)], r=S.R)), dot(18, 6, 3.5)]


_PIN = [(8, 3), (16, 3), (14.5, 5), (14.5, 10), (18, 14), (6, 14), (9.5, 10), (9.5, 5)]


@ui("pin", "Push pin; pin an item in place.", ["pushpin", "thumbtack", "attach", "keep", "sticky", "favorite"])
def _(S):
    return [shell(poly(_PIN, closed=True, r=S.r * 0.5)), line(seg(12, 14, 12, 21))]


@ui("unpin", "Push pin with a slash; unpin an item.", ["unpin", "detach", "release", "remove pin", "unstick"], aliases=["pin-off"])
def _(S):
    slash = seg(3.5, 3.5, 20.5, 20.5)
    gap = ST(slash, 5, "round", "round")
    if isF(S):
        pin = U(P(poly(_PIN, closed=True)), ST(poly(_PIN, closed=True), 2), ST(seg(12, 14, 12, 21), 2.5))
        return [solid(path_to_d(D(pin, gap))), line(slash)]
    pin = U(ST(poly(_PIN, closed=True, r=S.r * 0.5), 2, S.cap, S.join), ST(seg(12, 14, 12, 21), 2, S.cap, S.join))
    return [solid(path_to_d(D(pin, gap))), line(slash)]


@ui("picture-in-picture", "Window with a small overlay window in its corner.", ["pip", "overlay", "mini player", "floating", "video"],
    aliases=["pip"])
def _(S):
    if isF(S):
        return [win(S), detail(rect(9, 6, 10, 8))]
    return [win(S), solid(rect(10, 7, 8, 6, 0 if isL(S) else 1.5))]


@ui("split-view", "Panel split in two with a drag handle on the divider.", ["split", "split screen", "compare", "divide", "panes"],
    aliases=["split-screen"])
def _(S):
    return [frame(S), detail(seg(12, 3, 12, 21)), solid(rect(10, 8.5, 4, 7, 0.5 if isL(S) else 2))]


# =========================================================================== design tools

def _diamond(cx, cy, h):
    return [(cx, cy - h), (cx + h, cy), (cx, cy + h), (cx - h, cy)]


@ui("component", "Four diamonds arranged in a diamond; a reusable component.", ["symbol", "main component", "design system", "figma", "reusable"])
def _(S):
    k, h = 5.8, 3.2
    return [shell(poly(_diamond(12 + dx, 12 + dy, h), closed=True, r=S.r * 0.5)) for dx, dy in ((0, -k), (k, 0), (0, k), (-k, 0))]


@ui("components", "Three blocks and a fourth lifted and turned; a component library or add-ons.",
    ["blocks", "library", "modules", "add-ons", "extensions", "plugins"], aliases=["blocks"])
def _(S):
    return [tile(S, 3, 3, 7, 7), tile(S, 3, 14, 7, 7), tile(S, 14, 14, 7, 7),
            shell(poly(_diamond(17.5, 6.5, 4.6), closed=True, r=S.r * 0.5))]


@ui("frame-corners", "Four corner brackets around a rectangle; frame or fit to view.",
    ["frame", "corners", "focus", "fit", "bounds", "viewport"])
def _(S):
    out = [line(poly(p, r=S.r)) for p in ([(3, 8), (3, 3), (8, 3)], [(16, 3), (21, 3), (21, 8)],
                                          [(21, 16), (21, 21), (16, 21)], [(8, 21), (3, 21), (3, 16)])]
    return out + [shell(rect(8, 8.5, 8, 7, S.R * 0.5))]


@ui("section", "Content section with a label above it.", ["group", "container", "block", "area", "region"])
def _(S):
    return [line(seg(3, 3.5, 10, 3.5)), shell(rect(3, 7.5, 18, 13.5, S.R))]


@ui("divider", "Horizontal rule between two blocks of content.", ["separator", "rule", "line", "hr", "split"],
    aliases=["separator"])
def _(S):
    return [tile(S, 4, 3, 16, 5), line(seg(2, 12, 22, 12)), tile(S, 4, 16, 16, 5)]


@ui("spacing", "Double arrow between two bars; spacing or gap.", ["gap", "space", "distance", "gutter", "vertical spacing"])
def _(S):
    return [line(seg(3, 3, 21, 3)), chev(S, 12, 8.5, w=3, h=3, deg=-90), line(seg(12, 7.5, 12, 16.5)),
            chev(S, 12, 15.5, w=3, h=3, deg=90), line(seg(3, 21, 21, 21))]


@ui("padding", "Box with a dashed inner edge; padding inside an element.", ["inset", "box model", "inner space", "css", "spacing"])
def _(S):
    return [frame(S), *dashed_rect(S, 8, 8, 8, 8, kind=detail)]


@ui("margin", "Box inside a dashed outer edge; margin around an element.", ["outset", "box model", "outer space", "css", "spacing"])
def _(S):
    return [*dashed_rect(S, 3, 3, 18, 18), tile(S, 8, 8, 8, 8)]


@ui("z-index", "Card in front of two stacked cards; stacking order.", ["stack", "depth", "order", "bring to front", "arrange", "layer order"],
    aliases=["stacking-order"])
def _(S):
    return [tile(S, 3, 3, 10, 10), line(poly([(17, 7), (17, 17), (7, 17)], r=S.r)), line(poly([(21, 11), (21, 21), (11, 21)], r=S.r))]


@ui("layers-ui", "Two stacked layers; the layers panel.", ["layers", "stack", "levels", "overlay", "arrange"])
def _(S):
    return [shell(poly([(12, 4), (21, 9), (12, 14), (3, 9)], closed=True, r=S.r)), line(poly([(3, 14), (12, 19), (21, 14)], r=S.r))]


# =========================================================================== overlays & navigation components

@ui("modal", "Dialog box with a close button.", ["dialog", "popup", "overlay", "lightbox", "window", "alert"],
    aliases=["dialog"])
def _(S):
    return [frame(S), detail(seg(14.5, 7, 17.5, 10)), detail(seg(17.5, 7, 14.5, 10)), detail(seg(7, 15, 17, 15))]


@ui("popover", "Panel with a caret pointing up at what opened it.", ["popup", "flyout", "overlay", "bubble", "menu"])
def _(S):
    pts = [(3, 8), (7, 8), (10, 4), (13, 8), (21, 8), (21, 21), (3, 21)]
    return [shell(poly(pts, closed=True, r=S.R * 0.75)), detail(seg(7, 12.5, 17, 12.5)), detail(seg(7, 16.5, 13, 16.5))]


@ui("tooltip", "Small label bubble pointing down at an element.", ["hint", "help text", "hover", "info", "bubble"])
def _(S):
    pts = [(3, 4), (21, 4), (21, 15), (15, 15), (12, 19), (9, 15), (3, 15)]
    return [shell(poly(pts, closed=True, r=S.R * 0.75)), detail(seg(7, 9.5, 17, 9.5))]


@ui("toast", "Toast message bar with a tick and a line of text.", ["snackbar", "notification", "message", "banner", "alert"],
    aliases=["snackbar"])
def _(S):
    return [_field(S), detail(poly([(5.5, 12), (7.5, 14), (10.5, 11)], r=S.r)), detail(seg(13.5, 12, 18.5, 12))]


@ui("accordion", "Accordion: an open section with content above a closed one.",
    ["collapse", "expand", "sections", "disclosure", "faq", "collapsible"])
def _(S):
    return [line(seg(3, 4.5, 13, 4.5)), chev(S, 18, 4.5, w=3, h=3, deg=-90),
            tile(S, 3, 9, 18, 6),
            line(seg(3, 19.5, 13, 19.5)), chev(S, 18, 19.5, w=3, h=3, deg=90)]


@ui("carousel", "Carousel: a card in focus with the neighbouring cards peeking in.",
    ["slider", "slideshow", "gallery", "swipe", "cards"])
def _(S):
    return [tile(S, 7, 4, 10, 16), line(seg(3, 7, 3, 17)), line(seg(21, 7, 21, 17))]


@ui("pagination", "Page indicator: dots with the current page drawn long.", ["pages", "page dots", "indicator", "paging", "steps"],
    aliases=["page-dots"])
def _(S):
    bar = solid(rect(8.5, 10.25, 7, 3.5, 0 if isL(S) else 1.75)) if not isF(S) else solid(rect(8.25, 9.75, 7.5, 4.5, 2.25))
    return [pip(S, 4.5, 12), bar, pip(S, 19.5, 12)]


@ui("breadcrumb", "Two arrow-shaped steps in a path; breadcrumb trail.", ["path", "trail", "navigation", "hierarchy", "location"],
    aliases=["breadcrumbs"])
def _(S):
    return [shell(poly([(3, 8), (7, 8), (9.5, 12), (7, 16), (3, 16)], closed=True, r=S.r * 0.5)),
            shell(poly([(12, 8), (18, 8), (20.5, 12), (18, 16), (12, 16), (14.5, 12)], closed=True, r=S.r * 0.5))]


@ui("stepper", "Two steps joined by a line: one done, one to come.", ["steps", "progress", "wizard", "timeline", "onboarding"])
def _(S):
    return [dot(5.5, 5.5, 3), line(seg(5.5, 10.5, 5.5, 13.5)), shell(circle(5.5, 18.5, 2.5)),
            line(seg(12, 5.5, 21, 5.5)), line(seg(12, 18.5, 19, 18.5))]


@ui("menu-2", "Menu of three lines getting shorter.", ["menu", "hamburger", "navigation", "lines", "drawer"])
def _(S):
    return [line(seg(3, 6, 21, 6)), line(seg(3, 12, 16, 12)), line(seg(3, 18, 11, 18))]


@ui("menu-dots", "Round button holding three dots; overflow menu.", ["more", "options", "overflow", "menu", "ellipsis"])
def _(S):
    return [shell(circle(12, 12, 9)), *(pip(S, x, 12, 1.4, 0.1) for x in (8, 12, 16))]


# =========================================================================== apps & screens

@ui("app-grid", "Nine dots in a three-by-three grid; app switcher.", ["apps", "waffle", "launcher", "grid", "switcher"],
    aliases=["app-launcher"])
def _(S):
    return [pip(S, x, y, 1.9, 0.35) for x in (5, 12, 19) for y in (5, 12, 19)]


@ui("launcher", "Round launcher button with four app dots.", ["apps", "start", "app drawer", "home", "open apps"])
def _(S):
    return [shell(circle(12, 12, 9)), *(pip(S, x, y, 1.5, 0.1) for x in (9.5, 14.5) for y in (9.5, 14.5))]


@ui("home-screen", "Phone home screen with app icons and a dock.", ["mobile", "apps", "phone", "springboard", "screen"])
def _(S):
    k = 1.25 if isL(S) else 1.4
    apps = [Part("dot", rect(x - k, y - k, 2 * k, 2 * k, 0 if isL(S) else 0.9)) for x in (9.5, 14.5) for y in (6.5, 10.5, 14.5)]
    return [shell(rect(5, 2, 14, 20, S.R * 0.75)), *apps, detail(seg(9, 18.5, 15, 18.5))]


@ui("widget", "Widgets: three tiles and a round one.", ["widgets", "tiles", "gadgets", "blocks", "apps"], aliases=["widgets"])
def _(S):
    return [shell(circle(6.5, 6.5, 3.5)), tile(S, 14, 3, 7, 7), tile(S, 3, 14, 7, 7), tile(S, 14, 14, 7, 7)]


# =========================================================================== pointers & selection

_ARROW = [(5, 3.5), (5, 19.5), (9.4, 15.6), (12.3, 21.5), (15, 20.2), (12.2, 14.4), (18, 14.4)]


def _pointer(tip, k):
    return [(tip[0] + k * (x - 5), tip[1] + k * (y - 3.5)) for x, y in _ARROW]


@ui("cursor-click", "Mouse pointer with click rays at its tip.", ["click", "tap", "pointer", "mouse", "select", "press"],
    aliases=["click"])
def _(S):
    t = 0 if isL(S) else 0.5
    return [shell(poly(_pointer((10, 10), 0.62), closed=True, r=S.r * 0.3)),
            line(seg(10, 2 + t, 10, 6 - t)), line(seg(2 + t, 10, 6 - t, 10)), line(seg(3.8 + t, 3.8 + t, 6.3 - t, 6.3 - t))]


@ui("select-area", "Dashed selection box with square handles at its corners.",
    ["selection", "bounding box", "transform", "select", "handles"], aliases=["bounding-box"])
def _(S):
    out = [pip(S, x, y, 2, 0.25) for x in (4, 20) for y in (4, 20)]
    trim = 0 if isL(S) else 0.75
    for a, b in ((9.5 + trim, 14.5 - trim),):
        out += [line(seg(a, 4, b, 4)), line(seg(a, 20, b, 20)), line(seg(4, a, 4, b)), line(seg(20, a, 20, b))]
    return out


@ui("lasso", "Lasso loop with a trailing rope; freeform selection.", ["lasso tool", "freeform", "select", "selection", "rope"])
def _(S):
    return [line(ellipse(12, 9.5, 8.5, 6)), line("M6.5 14.2C5.3 16 5.6 18.2 7.4 19.2C8.6 19.9 9 20.8 8.5 21.5")]


@ui("marquee", "Dashed rectangle; marquee selection tool.", ["marquee tool", "rectangle select", "selection", "dashed", "select"],
    aliases=["dashed-box"])
def _(S):
    return dashed_rect(S, 3, 3, 18, 18)


@ui("resize", "Small box growing into a larger one along a diagonal arrow.", ["scale", "resize", "enlarge", "dimensions", "transform"])
def _(S):
    return [line(rect(3, 3, 18, 18, S.R)), shell(rect(3, 13, 8, 8, S.R * 0.5)), line(seg(13.5, 10.5, 16.5, 7.5)),
            line(poly([(12, 7), (17, 7), (17, 12)], r=S.r))]


@ui("crop-ui", "Two interlocking crop marks.", ["crop", "trim", "cut", "frame", "image"])
def _(S):
    e = 0.5 if isL(S) else 0
    return [line(poly([(7, 3 - e), (7, 17), (21 + e, 17)], r=S.r)), line(poly([(3 - e, 7), (17, 7), (17, 21 + e)], r=S.r))]


@ui("aspect", "Frame with corner marks; aspect ratio.", ["aspect ratio", "ratio", "proportions", "dimensions", "size"])
def _(S):
    return [shell(rect(2, 5, 20, 14, S.R)), detail(poly([(6, 12), (6, 9), (9, 9)], r=S.r)),
            detail(poly([(18, 12), (18, 15), (15, 15)], r=S.r))]


@ui("grid-dots", "Frame filled with a dot grid; snap to grid.", ["dot grid", "snap", "canvas", "guides", "pattern"])
def _(S):
    return [frame(S), *(pip(S, x, y, 1.1, 0) for x in (7.5, 12, 16.5) for y in (7.5, 12, 16.5))]


@ui("ruler-ui", "L-shaped canvas rulers with tick marks.", ["rulers", "guides", "measure", "canvas", "design"])
def _(S):
    return [shell(poly([(3, 3), (21, 3), (21, 8), (8, 8), (8, 21), (3, 21)], closed=True, r=S.r)),
            detail(seg(12.5, 8, 12.5, 5.5)), detail(seg(16.5, 8, 16.5, 5.5)),
            detail(seg(8, 12.5, 5.5, 12.5)), detail(seg(8, 16.5, 5.5, 16.5))]
