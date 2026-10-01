"""TypeIcon Core: files & documents.

File-type icons share one silhouette: the v0.1 `file` page (5–19 × 2.5–21.5, fold at the top right).
The distinguishing mark sits in the upper and left part of the page so the variant badges
(bottom-right box 13–23) do not hide it.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt

CAT = "files"

PAGE = [(5, 2.5), (14, 2.5), (19, 7.5), (19, 21.5), (5, 21.5)]
FOLD = [(14, 2.5), (14, 7.5), (19, 7.5)]


def page(S):
    """The shared document silhouette with its folded corner."""
    return [shell(poly(PAGE, closed=True, r=S.r)), detail(poly(FOLD, r=S.r * 0.5))]


def block(x, y, w, h):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h))


def tri(pts):
    return Part("dot", poly(pts, closed=True))


def rot_pts(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in pts]


def outline_region(d, miter=4.0):
    """Region of a closed outline filled to its outer stroke edge (Filled silhouettes)."""
    return U(P(d), ST(d, 2.0, "butt", "miter", miter))


def _pie(S):
    """Pie chart with one quarter marked."""
    return [detail(circle(12, 14.5, 3.75)), detail(poly([(12, 10.75), (12, 14.5), (15.75, 14.5)], r=S.r * 0.3))]


# ============================================================================ file types

@icon("file-text", CAT, "Document page with lines of plain text",
      tags=["text", "txt", "document", "plain text", "notes", "page"], aliases=["file-txt"])
def _(S):
    return [*page(S), detail(seg(9, 8.5, 11, 8.5)), detail(seg(9, 12.5, 15, 12.5)), detail(seg(9, 16.5, 15, 16.5))]


@icon("file-image", CAT, "Document page showing a small landscape picture",
      tags=["image", "picture", "photo", "jpg", "png", "graphic"], aliases=["file-picture", "file-photo"])
def _(S):
    return [*page(S), dot(9.5, 8.5, 1.5), detail(poly([(5, 18), (10, 13), (13, 16), (14.5, 14.5), (19, 19)], r=S.r))]


@icon("file-video", CAT, "Document page with a play triangle",
      tags=["video", "movie", "film", "mp4", "clip", "media"], aliases=["file-movie"])
def _(S):
    pts = [(9.5, 9), (15.5, 12.75), (9.5, 16.5)]
    return [*page(S), detail(poly(pts, closed=True, r=S.r * 0.5))]


@icon("file-audio", CAT, "Document page with a music note",
      tags=["audio", "music", "sound", "mp3", "song", "wav"], aliases=["file-music", "file-sound"])
def _(S):
    return [*page(S), dot(10, 16.5, 2), detail(poly([(11.5, 16.5), (11.5, 10), (14.5, 11.5)], r=S.r * 0.5))]


@icon("file-zip", CAT, "Document page with a zipper; a compressed archive",
      tags=["zip", "archive", "compressed", "rar", "7z", "package"], aliases=["file-archive", "file-compressed"])
def _(S):
    teeth = [block(8, 3.5, 2, 2), block(10, 5.5, 2, 2), block(8, 7.5, 2, 2), block(10, 9.5, 2, 2)]
    return [*page(S), *teeth, detail(rect(9, 12.5, 3, 4, min(S.R, 1)))]


@icon("file-pdf", CAT, "Document page with a picture block and text lines; a print-ready PDF",
      tags=["pdf", "acrobat", "portable document", "print", "document"])
def _(S):
    return [*page(S), detail(seg(9, 8.5, 11, 8.5)), block(8, 11, 8, 4.5), detail(seg(9, 18, 15, 18))]


@icon("file-spreadsheet", CAT, "Document page divided into a grid of cells",
      tags=["spreadsheet", "excel", "xls", "sheet", "table", "cells"], aliases=["file-excel", "file-sheet"])
def _(S):
    return [*page(S), detail(seg(5, 11.5, 19, 11.5)), detail(seg(5, 16.5, 19, 16.5)), detail(seg(10.5, 11.5, 10.5, 21.5))]


@icon("file-presentation", CAT, "Document page with a slide on a stand",
      tags=["presentation", "slides", "powerpoint", "ppt", "keynote", "deck"], aliases=["file-slides", "file-powerpoint"])
def _(S):
    return [*page(S), *_pie(S)]


@icon("file-document", CAT, "Document page with a heading and paragraph lines; a word-processing file",
      tags=["document", "word", "doc", "docx", "letter", "writing"], aliases=["file-word", "file-doc"])
def _(S):
    return [*page(S), block(8, 6.5, 4, 3.5), detail(seg(9, 13, 15, 13)), detail(seg(9, 16.5, 15, 16.5))]


@icon("file-font", CAT, "Document page with a letter A; a font file",
      tags=["font", "typeface", "ttf", "otf", "typography", "glyph"], aliases=["file-type"])
def _(S):
    return [*page(S), detail(poly([(8.5, 18), (12, 9), (15.5, 18)], r=S.r * 0.5)), detail(seg(10, 15, 14, 15))]


@icon("file-vector", CAT, "Document page with a curve between two anchor points; a vector graphic",
      tags=["vector", "svg", "eps", "illustration", "bezier", "graphic"], aliases=["file-svg"])
def _(S):
    return [*page(S), block(7.5, 15.5, 3, 3), block(13, 11, 3, 3), detail("M9 15.5C9 13.5 10.5 12.5 13 12.5")]


@icon("file-3d", CAT, "Document page with a cube; a 3D model file",
      tags=["3d", "model", "cube", "obj", "stl", "mesh"], aliases=["file-model"])
def _(S):
    hexa = [(12, 10), (16, 12.25), (16, 16.25), (12, 18.5), (8, 16.25), (8, 12.25)]
    return [*page(S), detail(poly(hexa, closed=True, r=S.r * 0.5)), detail(poly([(8, 12.25), (12, 14.5), (16, 12.25)], r=S.r * 0.5)), detail(seg(12, 14.5, 12, 18.5))]


@icon("file-database", CAT, "Document page with a database cylinder",
      tags=["database", "db", "sql", "sqlite", "data", "storage"], aliases=["file-db"])
def _(S):
    return [*page(S), detail(ellipse(12, 11.5, 3.5, 1.25)), detail("M8.5 11.5V17.25C8.5 18.1 10 18.75 12 18.75C14 18.75 15.5 18.1 15.5 17.25V11.5"),
            detail("M8.5 14.75C8.5 15.6 10 16.25 12 16.25C14 16.25 15.5 15.6 15.5 14.75")]


@icon("file-json", CAT, "Document page with curly braces; a JSON data file",
      tags=["json", "data", "braces", "config", "api", "object"])
def _(S):
    left = "M10.5 10.5C9.3 10.5 8.8 11 8.8 12V13.3C8.8 14.1 8.4 14.5 7.5 14.5C8.4 14.5 8.8 14.9 8.8 15.7V17C8.8 18 9.3 18.5 10.5 18.5"
    right = "M13.5 10.5C14.7 10.5 15.2 11 15.2 12V13.3C15.2 14.1 15.6 14.5 16.5 14.5C15.6 14.5 15.2 14.9 15.2 15.7V17C15.2 18 14.7 18.5 13.5 18.5"
    return [*page(S), detail(left), detail(right)]


@icon("file-csv", CAT, "Document page with rows of separated values",
      tags=["csv", "comma separated", "data", "table", "export", "values"])
def _(S):
    out = []
    for y in (11, 14.5, 18):
        out += [detail(seg(8.5, y, 11, y)), detail(seg(13, y, 15.5, y))]
    return [*page(S), *out]


@icon("file-shield", CAT, "Document page with a shield; a protected file",
      tags=["protected", "secure", "security", "safe", "privacy", "guard"], aliases=["file-protected"])
def _(S):
    d = poly([(12, 10), (16, 11.5), (16, 14.5), (12, 18.5), (8, 14.5), (8, 11.5)], closed=True, r=S.r * 0.66)
    return [*page(S), detail(d)]


@icon("file-certificate", CAT, "Document page with a seal and ribbon; a certificate file",
      tags=["certificate", "award", "seal", "credential", "diploma", "verified"], aliases=["file-award"])
def _(S):
    return [*page(S), detail(circle(11, 12, 2.5)), detail(poly([(9.4, 14.2), (8.75, 18.75), (11, 17.5), (13.25, 18.75), (12.6, 14.2)], r=S.r * 0.4))]


@icon("file-invoice", CAT, "Document page with item lines and amounts; an invoice file",
      tags=["invoice", "bill", "billing", "payment", "statement", "accounting"], aliases=["file-bill"])
def _(S):
    return [*page(S), detail(seg(8.5, 8.5, 11, 8.5)),
            detail(seg(8.5, 12.5, 12, 12.5)), detail(seg(14, 12.5, 15.5, 12.5)),
            detail(seg(8.5, 16.5, 15.5, 16.5))]


@icon("file-report", CAT, "Document page with a small line chart; a report file",
      tags=["report", "analytics", "statistics", "summary", "chart", "results"])
def _(S):
    return [*page(S), detail(seg(9, 8.5, 11, 8.5)), detail(poly([(8.5, 17.5), (11, 14), (13, 15.5), (15.5, 11.5)], r=S.r))]


@icon("file-stack", CAT, "Stack of two document pages",
      tags=["files", "documents", "stack", "batch", "multiple", "pile"], aliases=["files-stack"])
def _(S):
    front = [(3, 6.5), (11, 6.5), (15.5, 11), (15.5, 21.5), (3, 21.5)]
    return [
        shell(poly(front, closed=True, r=S.r)), detail(poly([(11, 6.5), (11, 11), (15.5, 11)], r=S.r * 0.5)),
        line(poly([(7, 4.5), (7, 2.5), (15, 2.5), (20.5, 8), (20.5, 17.5), (18.5, 17.5)], r=S.r)),
    ]


# ============================================================================ folders

FOLDER = [(3, 5), (9.5, 5), (11.5, 7.5), (21, 7.5), (21, 20), (3, 20)]


def mini_folder(x, y, w, h, S, tab=3.0):
    return poly([(x, y), (x + tab, y), (x + tab + 1.5, y + 1.5), (x + w, y + 1.5), (x + w, y + h), (x, y + h)], closed=True, r=S.r * 0.66)


@icon("folder-open", CAT, "Open folder with its front flap tilted forward",
      tags=["open", "directory", "browse", "explore", "files", "folder"], aliases=["directory-open"])
def _(S):
    outer = [(3, 20), (3, 5), (9.5, 5), (11.5, 7.5), (18.5, 7.5), (18.5, 10.5), (21, 10.5), (17.75, 20)]
    return [shell(poly(outer, closed=True, r=S.r)), detail(poly([(3, 20), (6.5, 10.5), (18.5, 10.5)], r=S.r))]


@icon("folders", CAT, "Two folders, one behind the other",
      tags=["directories", "collections", "multiple", "group", "files", "folder"], aliases=["directories"])
def _(S):
    front = [(2.5, 9), (8, 9), (9.5, 11), (17.5, 11), (17.5, 21), (2.5, 21)]
    back = [(6.5, 6.5), (6.5, 4), (11.5, 4), (13, 6), (21, 6), (21, 17.5)]
    return [shell(poly(front, closed=True, r=S.r)), line(poly(back, r=S.r))]


@icon("folder-tree", CAT, "Parent folder branching to two sub-folders",
      tags=["hierarchy", "directory tree", "structure", "nested", "subfolder", "explorer"], aliases=["directory-tree"])
def _(S):
    return [
        shell(mini_folder(2.5, 2.5, 8, 5.5, S)),
        shell(mini_folder(13, 6.5, 8.5, 5.5, S)),
        shell(mini_folder(13, 16, 8.5, 5.5, S)),
        line(poly([(5.5, 10), (5.5, 19), (11, 19)], r=S.r)),
        line(seg(5.5, 10, 11, 10)),
    ]


@icon("folder-zip", CAT, "Folder with a zipper; a compressed folder",
      tags=["zip", "compressed", "archive", "package", "directory", "rar"], aliases=["folder-compressed", "folder-archive"])
def _(S):
    teeth = [block(10, 8.5, 2, 2), block(12, 10.5, 2, 2), block(10, 12.5, 2, 2)]
    return [shell(poly(FOLDER, closed=True, r=S.r)), *teeth, block(10.5, 14.5, 3, 3)]


@icon("folder-shared", CAT, "Folder with a person on it; a folder shared with others",
      tags=["shared", "team", "collaboration", "people", "directory", "access"], aliases=["folder-user", "folder-team"])
def _(S):
    return [shell(poly(FOLDER, closed=True, r=S.r)), dot(12, 11.75, 1.75),
            detail("M8.5 17.5C8.5 16 10 15 12 15C14 15 15.5 16 15.5 17.5")]


# ============================================================================ clipboards

BOARD = (5, 4, 14, 17.5)
CLIP = (8.5, 2.5, 7, 4)


def _board(S):
    x, y, w, h = BOARD
    cx, _, cw, _ = CLIP
    return [shell(poly([(cx, y), (x, y), (x, y + h), (x + w, y + h), (x + w, y), (cx + cw, y)], r=S.R)),
            shell(rect(*CLIP, min(S.R, 1.5)))]


def _board_filled(*details, dots=()):
    def f():
        x, y, w, h = BOARD
        cx, cy, cw, ch = CLIP
        board = outline_region(rect(x, y, w, h, 2))
        clip = outline_region(rect(cx, cy, cw, ch, 1.5))
        body = U(D(board, P(rect(cx - 2.5, cy - 2.5, cw + 5, ch + 5, 2.5))), clip)
        knock = [ST(dd, 2.0) for dd in details] + [P(circle(px, py, pr)) for px, py, pr in dots]
        return D(body, *knock) if knock else body
    return f


@icon("clipboard", CAT, "Clipboard with a clip at the top",
      tags=["board", "paste", "copy", "notes", "form", "checklist"], filled=_board_filled())
def _(S):
    return _board(S)


_CL_ROWS = (10.5, 14, 17.5)


@icon("clipboard-list", CAT, "Clipboard holding a bulleted list",
      tags=["checklist", "tasks", "todo", "inventory", "list", "board"], aliases=["checklist-board"],
      filled=_board_filled(*[seg(11, y, 16, y) for y in _CL_ROWS], dots=[(8.5, y, 1.25) for y in _CL_ROWS]))
def _(S):
    out = []
    for y in _CL_ROWS:
        out += [dot(8.5, y, 1.25), detail(seg(11, y, 16, y))]
    return [*_board(S), *out]


_CT_LINES = [seg(8.5, 10.5, 15.5, 10.5), seg(8.5, 14, 15.5, 14), seg(8.5, 17.5, 12.5, 17.5)]


@icon("clipboard-text", CAT, "Clipboard holding lines of text",
      tags=["notes", "document", "form", "memo", "text", "board"], filled=_board_filled(*_CT_LINES))
def _(S):
    return [*_board(S), *[detail(d) for d in _CT_LINES]]


# ============================================================================ books and notebooks

@icon("notebook", CAT, "Spiral-bound notebook",
      tags=["spiral", "notepad", "jotter", "notes", "school", "writing"], aliases=["spiral-notebook"])
def _(S):
    rings = [line(seg(3.5, y, 8, y)) for y in (6, 10, 14, 18)]
    return [shell(rect(6, 2.5, 13, 19, S.R)), *rings, detail(seg(11, 7, 16, 7))]


@icon("book", CAT, "Closed hardcover book seen from the front",
      tags=["read", "reading", "novel", "literature", "education", "manual"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 19, S.R)), detail(seg(8.5, 2.5, 8.5, 21.5)), detail(seg(11.5, 7, 16, 7)), detail(seg(11.5, 10.5, 14.5, 10.5))]


@icon("book-open", CAT, "Open book with two facing pages",
      tags=["reading", "read", "pages", "documentation", "guide", "study"], aliases=["open-book"])
def _(S):
    pts = [(12, 6), (8, 4.5), (2.5, 4.5), (2.5, 18.5), (8, 18.5), (12, 20.5), (16, 18.5), (21.5, 18.5), (21.5, 4.5), (16, 4.5)]
    return [shell(poly(pts, closed=True, r=S.r)), detail(seg(12, 6, 12, 20.5))]


@icon("books", CAT, "Pile of three books lying flat",
      tags=["pile", "stack", "reading", "study", "literature", "collection"], aliases=["book-stack"])
def _(S):
    rr = min(S.R, 1.5)
    return [
        shell(rect(3, 15.5, 18, 6, rr)), shell(rect(5, 9.5, 15, 6, rr)), shell(rect(3.5, 3.5, 14, 6, rr)),
        detail(seg(3, 15.5, 21, 15.5)), detail(seg(5, 9.5, 17.5, 9.5)),
        detail(seg(15, 18.5, 21, 18.5)), detail(seg(5, 12.5, 11, 12.5)), detail(seg(12, 6.5, 17.5, 6.5)),
    ]


# ============================================================================ storage

@icon("archive", CAT, "Filing cabinet with three drawers",
      tags=["filing cabinet", "records", "storage", "drawers", "office", "files"], aliases=["filing-cabinet"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 19, S.R)), detail(seg(4.5, 8.83, 19.5, 8.83)), detail(seg(4.5, 15.17, 19.5, 15.17)),
            detail(seg(10.5, 5.67, 13.5, 5.67)), detail(seg(10.5, 12, 13.5, 12)), detail(seg(10.5, 18.33, 13.5, 18.33))]


@icon("archive-box", CAT, "Storage box with a lid and a hand slot",
      tags=["box", "storage", "archived", "store", "records", "package"], aliases=["storage-box"])
def _(S):
    return [shell(rect(2.5, 3, 19, 5.5, min(S.R, 1.5))), shell(poly([(4, 8.5), (4, 21), (20, 21), (20, 8.5)], closed=True, r=S.R)),
            detail(seg(4, 8.5, 20, 8.5)), detail(seg(10, 12.5, 14, 12.5))]


@icon("inbox", CAT, "Tray with an arrow pointing into it; incoming items",
      tags=["incoming", "received", "mail", "messages", "tray", "in tray"], aliases=["in-tray"])
def _(S):
    return [shell(rect(3, 3.5, 18, 17, S.R)), detail(poly([(3, 13.5), (8, 13.5), (9.5, 16.5), (14.5, 16.5), (16, 13.5), (21, 13.5)], r=S.r)),
            detail(seg(12, 5.5, 12, 11)), detail(poly([(9.5, 8.5), (12, 11), (14.5, 8.5)], r=S.r * 0.5))]


@icon("outbox", CAT, "Tray with an arrow pointing out of it; outgoing items",
      tags=["outgoing", "sent", "mail", "messages", "tray", "out tray"], aliases=["out-tray"])
def _(S):
    return [shell(rect(3, 3.5, 18, 17, S.R)), detail(poly([(3, 13.5), (8, 13.5), (9.5, 16.5), (14.5, 16.5), (16, 13.5), (21, 13.5)], r=S.r)),
            detail(seg(12, 6, 12, 11.5)), detail(poly([(9.5, 8.5), (12, 6), (14.5, 8.5)], r=S.r * 0.5))]


def _rot_path(ops, deg):
    """ops: list of ('M'|'L', (x, y)) or ('A', r, large, sweep, (x, y)); rotate every point about (12, 12)."""
    out = ""
    for op in ops:
        if op[0] in "ML":
            (x, y), = rot_pts([op[1]], deg)
            out += f"{op[0]}{fmt(x)} {fmt(y)}"
        else:
            _, r, large, sweep, p = op
            (x, y), = rot_pts([p], deg)
            out += f"A{fmt(r)} {fmt(r)} 0 {large} {sweep} {fmt(x)} {fmt(y)}"
    return out


@icon("paperclip", CAT, "Paperclip; an attachment",
      tags=["attachment", "attach", "clip", "file", "email", "office"], aliases=["attachment", "attach"])
def _(S):
    ops = [("M", (16, 8)), ("L", (16, 16)), ("A", 4, 0, 1, (8, 16)), ("L", (8, 6.5)), ("A", 2, 0, 1, (12, 6.5)), ("L", (12, 15))]
    return [line(_rot_path(ops, 45))]


@icon("document-signed", CAT, "Document page with a signature on a line",
      tags=["signed", "signature", "agreement", "approved", "sign", "contract"], aliases=["signed-document"])
def _(S):
    sig = "M8.5 15C9.5 12.5 10.5 11 11.2 11.5C12 12 10.5 15 11.5 15.5C12.3 15.9 13 13.5 13.7 13.5C14.4 13.5 14 15 15.5 14.5"
    return [*page(S), detail(seg(9, 8.5, 11, 8.5)), detail(sig), detail(seg(8.5, 18.5, 15.5, 18.5))]


# ============================================================================ business papers

SHEET = (4.5, 2.5, 15, 19)


def sheet(S):
    return shell(rect(*SHEET, S.R))


@icon("contract", CAT, "Agreement page with text and a signature line marked with a cross",
      tags=["agreement", "legal", "terms", "deal", "sign here", "document"], aliases=["agreement"])
def _(S):
    return [sheet(S), detail(seg(8, 6.5, 16, 6.5)), detail(seg(8, 10, 16, 10)),
            detail(seg(8, 13.5, 10.5, 16)), detail(seg(10.5, 13.5, 8, 16)), detail(seg(8, 18, 16, 18))]


@icon("receipt", CAT, "Paper receipt with a torn zigzag bottom edge",
      tags=["purchase", "till", "payment", "bill", "proof", "shopping"], aliases=["till-receipt"])
def _(S):
    zig = [(19, 21.5), (16.67, 19.5), (14.33, 21.5), (12, 19.5), (9.67, 21.5), (7.33, 19.5), (5, 21.5)]
    return [shell(poly([(5, 2.5), (19, 2.5), *zig], closed=True, r=S.r * 0.5)),
            detail(seg(8.5, 7, 15.5, 7)), detail(seg(8.5, 10.5, 15.5, 10.5)), detail(seg(8.5, 14, 12, 14))]


@icon("invoice", CAT, "Invoice sheet with a header block, item lines and a total",
      tags=["bill", "billing", "payment due", "statement", "accounting", "charge"])
def _(S):
    return [sheet(S), block(7.5, 5.5, 5, 3.5),
            detail(seg(8, 12.5, 11.5, 12.5)), detail(seg(13.5, 12.5, 16, 12.5)),
            detail(seg(8, 16, 11.5, 16)), detail(seg(13.5, 16, 16, 16))]


@icon("report", CAT, "Report sheet with a title and a bar chart",
      tags=["summary", "analysis", "results", "statistics", "review", "document"])
def _(S):
    return [sheet(S), detail(seg(8, 6.5, 13, 6.5)), block(7.5, 13, 2.5, 5), block(10.75, 10, 2.5, 8), block(14, 12, 2.5, 6)]


def _cert_parts(S):
    body = poly([(4.5, 16.5), (2.5, 16.5), (2.5, 3.5), (21.5, 3.5), (21.5, 16.5), (11.5, 16.5)], r=S.R)
    return body


@icon("certificate", CAT, "Certificate with a seal and ribbon",
      tags=["award", "diploma", "achievement", "credential", "accreditation", "qualification"], aliases=[],
      filled=lambda: _cert_filled())
def _(S):
    return [shell(_cert_parts(S)), detail(seg(12.5, 7.5, 18.5, 7.5)), detail(seg(14.5, 11, 18.5, 11)),
            shell(circle(8.5, 11, 2.75)), line(poly([(7, 13.75), (6.5, 20.5), (8.5, 19), (10.5, 20.5), (10, 13.75)], r=S.r * 0.4))]


def _cert_filled():
    sheet_r = outline_region(rect(2.5, 3.5, 19, 13, 2))
    seal = P(circle(8.5, 11, 3.75))
    body = D(sheet_r, P(circle(8.5, 11, 5.25)), P(rect(4.5, 13, 8, 5)))
    ribbon = outline_region(poly([(7, 13.75), (6.5, 20.5), (8.5, 19), (10.5, 20.5), (10, 13.75)], closed=True))
    return U(D(body, ST(seg(12.5, 7.5, 18.5, 7.5), 2), ST(seg(14.5, 11, 18.5, 11), 2)), seal, ribbon)


@icon("id-card", CAT, "Identity card with a portrait and details",
      tags=["identity", "badge", "membership", "license", "profile", "credentials"], aliases=["identity-card"])
def _(S):
    return [shell(rect(2.5, 4.5, 19, 15, S.R)), dot(8, 10, 2),
            detail("M5 16.5C5 14.6 6.3 13.5 8 13.5C9.7 13.5 11 14.6 11 16.5"),
            detail(seg(13.5, 9.5, 18.5, 9.5)), detail(seg(13.5, 13, 17, 13))]


@icon("passport", CAT, "Passport booklet with a globe emblem",
      tags=["travel", "identity", "border", "visa", "citizenship", "document"])
def _(S):
    return [sheet(S), detail(circle(12, 10, 3.75)), detail(seg(8.25, 10, 15.75, 10)),
            detail(seg(9, 17.5, 15, 17.5))]


def _ticket_d(S):
    rr = min(S.R, 2.0)
    a = f"A{fmt(rr)} {fmt(rr)} 0 0 1 "
    corners = rr > 0
    return (f"M{fmt(2.5 + rr)} 5.5H{fmt(21.5 - rr)}" + (f"{a}21.5 {fmt(5.5 + rr)}" if corners else "") +
            "V10A2 2 0 0 0 21.5 14" + f"V{fmt(18.5 - rr)}" + (f"{a}{fmt(21.5 - rr)} 18.5" if corners else "") +
            f"H{fmt(2.5 + rr)}" + (f"{a}2.5 {fmt(18.5 - rr)}" if corners else "") +
            "V14A2 2 0 0 0 2.5 10" + f"V{fmt(5.5 + rr)}" + (f"{a}{fmt(2.5 + rr)} 5.5" if corners else "") + "Z")


@icon("ticket", CAT, "Admission ticket with side notches and a tear line",
      tags=["admission", "event", "pass", "entry", "coupon", "stub"], aliases=["admission-ticket"])
def _(S):
    return [shell(_ticket_d(S)), detail(seg(15.5, 8, 15.5, 10)), detail(seg(15.5, 14, 15.5, 16))]


# ============================================================================ notes

@icon("sticky-note", CAT, "Square sticky note with a folded corner",
      tags=["post-it", "memo", "reminder", "note", "sticky", "annotation"], aliases=["post-it"])
def _(S):
    return [shell(poly([(3, 3), (21, 3), (21, 21), (9, 21), (3, 15)], closed=True, r=S.r)),
            detail(poly([(9, 21), (9, 15), (3, 15)], r=S.r * 0.5))]


@icon("note", CAT, "Notepad sheet with binding rings and lines",
      tags=["notepad", "memo", "jot", "write", "pad", "reminder"], aliases=["notepad", "memo"])
def _(S):
    rings = [line(seg(x, 2, x, 6.5)) for x in (8.5, 12, 15.5)]
    return [shell(rect(4.5, 4.5, 15, 17, S.R)), *rings, detail(seg(8, 10.5, 16, 10.5)), detail(seg(8, 14, 16, 14)), detail(seg(8, 17.5, 12.5, 17.5))]


@icon("notes", CAT, "Two overlapping notes, the front one with lines",
      tags=["memos", "notes", "annotations", "stack", "writing", "reminders"], aliases=["memos"])
def _(S):
    return [shell(rect(3, 7, 13.5, 14.5, S.R)), line(poly([(7.5, 5), (7.5, 2.5), (21, 2.5), (21, 16.5), (18.5, 16.5)], r=S.R)),
            detail(seg(6.5, 11.5, 13, 11.5)), detail(seg(6.5, 15, 13, 15)), detail(seg(6.5, 18.5, 10, 18.5))]


@icon("journal", CAT, "Journal with an elastic strap and a ribbon bookmark",
      tags=["diary", "planner", "log", "notebook", "personal", "writing"], aliases=["diary"])
def _(S):
    return [sheet(S), detail(seg(15.5, 2.5, 15.5, 21.5)),
            detail(poly([(9, 2.5), (9, 9.5), (10.5, 8), (12, 9.5), (12, 2.5)], r=S.r * 0.4))]


def _scroll_shapes(S):
    top = rect(3.5, 2.5, 15, 4.5, 2.25)
    bottom = rect(5.5, 17, 15, 4.5, 2.25)
    return top, bottom


@icon("scroll", CAT, "Parchment scroll rolled at the top and bottom",
      tags=["parchment", "manuscript", "ancient", "decree", "proclamation", "history"], aliases=["parchment"],
      filled=lambda: _scroll_filled())
def _(S):
    top, bottom = _scroll_shapes(S)
    return [shell(top), shell(bottom), line(seg(6, 7, 6, 17)), line(seg(18, 7, 18, 17)),
            detail(seg(9, 11, 15, 11)), detail(seg(9, 14, 13, 14))]


def _scroll_filled():
    top = outline_region(rect(3.5, 2.5, 15, 4.5, 2.25))
    bottom = outline_region(rect(5.5, 17, 15, 4.5, 2.25))
    body = P(rect(5, 9.5, 14, 5))
    return D(U(top, bottom, body), P(circle(6, 4.75, 1)), P(circle(18, 19.25, 1)))


@icon("newspaper", CAT, "Folded newspaper with a headline photo and columns",
      tags=["news", "press", "article", "daily", "headlines", "media"], aliases=["news"])
def _(S):
    return [shell(poly([(6, 17.5), (6, 3.5), (21, 3.5), (21, 20.5), (5.5, 20.5)], r=S.R)),
            line("M6 8H3V18.5C3 19.6 3.9 20.5 5 20.5" if S.name == "rounded" else "M6 8H3V20.5H6"),
            block(9, 6.5, 4.5, 4.5), detail(seg(16, 7.5, 18, 7.5)), detail(seg(16, 10.5, 18, 10.5)),
            detail(seg(9.5, 14.5, 18, 14.5)), detail(seg(9.5, 17.5, 15, 17.5))]


@icon("magazine", CAT, "Magazine cover with a masthead and a portrait",
      tags=["periodical", "publication", "glossy", "issue", "cover", "fashion"], aliases=["periodical"])
def _(S):
    return [sheet(S), block(7.5, 5.5, 9, 2.5), dot(12, 12.5, 2),
            detail("M8 19.5C8 17.2 9.8 16 12 16C14.2 16 16 17.2 16 19.5")]


@icon("catalog", CAT, "Catalogue booklet with a grid of products",
      tags=["catalogue", "brochure", "products", "listing", "shop", "booklet"], aliases=["catalogue"])
def _(S):
    return [sheet(S), block(7.5, 6, 3.5, 3.5), block(13, 6, 3.5, 3.5), block(7.5, 11.5, 3.5, 3.5), block(13, 11.5, 3.5, 3.5),
            detail(seg(8, 18, 16, 18))]


@icon("library", CAT, "Shelf of standing books with one leaning",
      tags=["bookshelf", "books", "collection", "reading", "study", "archive"], aliases=["bookshelf-books"])
def _(S):
    rr = min(S.R, 1)
    lean = [(16, 21), (19.76, 19.63), (16, 9.29), (12.24, 10.66)]
    return [
        shell(rect(3.5, 5, 4, 16, rr)), shell(rect(7.5, 8, 4.5, 13, rr)),
        shell(poly(lean, closed=True, r=S.r * 0.4)),
        detail(seg(7.5, 8, 7.5, 21)), detail(seg(3.5, 8.5, 7.5, 8.5)), detail(seg(7.5, 11.5, 12, 11.5)),
        line(seg(2, 21, 22, 21)),
    ]


@icon("dossier", CAT, "Folder holding papers with a label on the front",
      tags=["case file", "file folder", "records", "dossier", "confidential", "papers"], aliases=["case-file"],
      filled=lambda: _dossier_filled())
def _(S):
    body = [(3, 8), (9, 8), (10.5, 10), (21, 10), (21, 21), (3, 21)]
    from geometry import path_to_d
    paper = D(ST(_dossier_paper(), 2, S.cap, S.join), _dossier_cut())
    return [shell(poly(body, closed=True, r=S.r)), Part("solid", path_to_d(paper)), detail(rect(7, 13.5, 7.5, 4, min(S.R, 1)))]


_DOSSIER_BODY = [(3, 8), (9, 8), (10.5, 10), (21, 10), (21, 21), (3, 21)]


def _dossier_paper():
    return poly(rot_pts([(7, 2.5), (18, 2.5), (18, 14), (7, 14)], 8, 12.5, 9), closed=True)


def _dossier_cut():
    return U(P(poly(_DOSSIER_BODY, closed=True)), ST(poly(_DOSSIER_BODY, closed=True), 5, "butt", "miter"))


def _dossier_filled():
    body = outline_region(poly(_DOSSIER_BODY, closed=True))
    paper = D(outline_region(_dossier_paper()), _dossier_cut())
    return U(D(body, ST(rect(7, 13.5, 7.5, 4, 1), 2)), paper)


@icon("envelope-document", CAT, "Envelope with a letter sliding out",
      tags=["letter", "mail", "correspondence", "document", "post", "message"], aliases=["letter-envelope"])
def _(S):
    return [shell(rect(6, 2.5, 12, 8.5, min(S.R, 1.5))), shell(rect(3, 10, 18, 11, S.R)),
            detail(seg(3, 10, 21, 10)), detail(seg(9, 6, 15, 6)), detail(poly([(3, 11), (12, 16.5), (21, 11)], r=S.r))]


# ============================================================================ pages

@icon("page-blank", CAT, "Blank sheet of paper",
      tags=["blank", "empty", "sheet", "paper", "new page", "page"], aliases=["blank-page"])
def _(S):
    return [shell(poly([(4.5, 2.5), (19.5, 2.5), (19.5, 21.5), (9, 21.5), (4.5, 17)], closed=True, r=S.r)),
            detail("M4.5 17C7.5 17 9 18.5 9 21.5")]


@icon("pages", CAT, "Two sheets of paper, one tilted behind the other",
      tags=["sheets", "papers", "multiple pages", "documents", "stack", "pile"], aliases=["sheets"],
      filled=lambda: _pages_filled())
def _(S):
    from geometry import path_to_d
    back = _pages_back()
    region = D(ST(back, 2, S.cap, S.join), P(rect(1.5, 4.5, 16, 19)))
    return [shell(rect(3.5, 6.5, 12, 15, S.R)), Part("solid", path_to_d(region)),
            detail(seg(7, 11, 12, 11)), detail(seg(7, 14.5, 12, 14.5))]


def _pages_back():
    pts = rot_pts([(8.5, 3), (19.5, 3), (19.5, 17.5), (8.5, 17.5)], 10, 14, 10)
    return poly(pts, closed=True)


def _pages_filled():
    front = outline_region(rect(3.5, 6.5, 12, 15, 2))
    back = D(outline_region(_pages_back()), P(rect(1.5, 4.5, 16, 19)))
    return U(D(front, ST(seg(7, 11, 12, 11), 2), ST(seg(7, 14.5, 12, 14.5), 2)), back)


@icon("cover-page", CAT, "Title page with a centred title and author line",
      tags=["title page", "cover", "front page", "title", "report cover", "book cover"], aliases=["title-page"])
def _(S):
    return [sheet(S), dot(12, 7, 1.75), detail(seg(8, 11.5, 16, 11.5)), detail(seg(9.5, 15, 14.5, 15)), detail(seg(10.5, 18.5, 13.5, 18.5))]


@icon("table-of-contents", CAT, "Page listing entries with page numbers",
      tags=["contents", "toc", "index", "chapters", "outline", "navigation"], aliases=["toc", "contents"])
def _(S):
    out = []
    for y in (7, 11, 15):
        out += [detail(seg(8, y, 12, y)), detail(seg(14.5, y, 16, y))]
    return [sheet(S), *out]


@icon("manuscript", CAT, "Handwritten page with wavy lines of script",
      tags=["handwriting", "draft", "writing", "author", "script", "original"], aliases=["handwritten"])
def _(S):
    def wave(y, x1=16):
        return f"M8 {y}C9 {y - 1.2} 10 {y - 1.2} 11 {y}C12 {y + 1.2} 13 {y + 1.2} 14 {y}C14.7 {y - 0.8} 15.4 {y - 1} {x1} {y - 0.5}"
    return [sheet(S), detail(wave(8)), detail(wave(13)), detail(seg(8, 17.5, 12, 17.5))]


@icon("blueprint", CAT, "Architectural floor-plan drawing on a sheet",
      tags=["floor plan", "architecture", "plan", "drawing", "construction", "layout"], aliases=["floor-plan"])
def _(S):
    room = poly([(10, 16.5), (6.5, 16.5), (6.5, 7.5), (17.5, 7.5), (17.5, 16.5), (15.5, 16.5)], r=S.r * 0.5)
    return [shell(rect(2.5, 4, 19, 16, S.R)), detail(room), detail(seg(15.5, 16.5, 15.5, 11)), detail("M10 16.5A5.5 5.5 0 0 1 15.5 11")]
