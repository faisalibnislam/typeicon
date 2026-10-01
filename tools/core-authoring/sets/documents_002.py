"""TypeIcon Core: documents (batch 002): paper records, print and scan gear, forms and format files.

Shared silhouettes: the `file` page of files.py (5-19 x 2.5-21.5, fold top right) for file-format icons, and a
plain portrait sheet for forms and records. Letters are never drawn; formats are told by a small picture above a
solid tag band.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, polar  # noqa: F401

CAT = "documents"

PAGE = [(5, 2.5), (14, 2.5), (19, 7.5), (19, 21.5), (5, 21.5)]
FOLD = [(14, 2.5), (14, 7.5), (19, 7.5)]


def page(S):
    return [shell(poly(PAGE, closed=True, r=S.r)), detail(poly(FOLD, r=S.r * 0.5))]


def block(x, y, w, h):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h))


def sheet(S, x=4.5, y=2.5, w=15, h=19):
    return shell(rect(x, y, w, h, S.R))


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def rot(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


# ============================================================================ chunk 1

@icon("bamboo-slips", CAT, "Three bamboo strips bound together with two cords",
      tags=["bamboo", "ancient book", "scroll", "chinese", "writing", "strips", "history"])
def _(S):
    out = [shell(rect(x, 3, 3, 18, 0 if S.name == 'line' else 1.5)) for x in (3.5, 10.5, 17.5)]
    for y in (8, 16):
        out += [line(seg(6.5, y, 10.5, y)), line(seg(13.5, y, 17.5, y))]
    return out


@icon("palm-leaf-manuscript", CAT, "Stack of long narrow leaves threaded on a cord between two boards",
      tags=["palm leaf", "manuscript", "ancient book", "leaves", "cord", "writing", "india"])
def _(S):
    return [shell(rect(2.5, 3, 19, 3, min(S.R, 1.5))), shell(rect(2.5, 18, 19, 3, min(S.R, 1.5))),
            line(seg(4.5, 10, 19.5, 10)), line(seg(4.5, 14, 19.5, 14)), detail(seg(17, 6.5, 17, 17.5))]


@icon("punched-tape", CAT, "Long paper strip with a row of small sprocket holes and larger data holes",
      tags=["paper tape", "punch tape", "computing history", "teleprinter", "data", "holes", "retro"])
def _(S):
    out = [shell(rect(2.5, 5.5, 19, 13, S.R))]
    for x in (6, 10, 14, 18):
        out.append(dot(x, 12, 0.8))
    for x, y in ((7.5, 9), (12, 9), (16.5, 9), (9.5, 15), (14, 15), (18, 15)):
        out.append(dot(x, y, 1))
    return out


@icon("herbarium-sheet", CAT, "Sheet with a pressed plant sprig and a label in the lower right corner",
      tags=["herbarium", "pressed plant", "specimen", "botany", "plant", "collection", "science"])
def _(S):
    return [sheet(S), detail(seg(10, 18, 10, 6.5)), detail(seg(10, 14, 7.5, 11.5)), detail(seg(10, 11, 13, 8.5)),
            block(13.5, 16, 3.5, 3)]


@icon("restaurant-menu", CAT, "Tall menu card with a fork and a knife on the cover",
      tags=["menu", "restaurant", "dining", "food", "cafe", "fork", "knife", "eat"])
def _(S):
    fork = "M7.5 6.5V9.5a1.5 1.5 0 0 0 3 0V6.5M9 11V17.5"
    knife = "M15 17.5V6.5c1.7 0 2 2 2 4 0 1.4-.6 2.2-2 2.5"
    return [sheet(S, 4, 2.5, 16, 19), detail(fork), detail(knife)]


@icon("receipt-printer", CAT, "Compact thermal printer with a receipt coming out of the top",
      tags=["pos printer", "thermal printer", "till", "till roll", "checkout", "receipt", "shop"])
def _(S):
    tip = [(6.5, 13), (6.5, 6), (8.33, 3), (10.17, 6), (12, 3), (13.83, 6), (15.67, 3), (17.5, 6), (17.5, 13)]
    return [shell(poly(tip, closed=True, r=S.r * 0.4)), detail(seg(10, 9.5, 14, 9.5)),
            shell(rect(3.5, 13, 17, 8, rr(S, 3))), dot(17, 17, 1)]


@icon("photo-printer", CAT, "Compact printer with a mountain photo coming out of the front",
      tags=["photo printing", "snapshot printer", "picture", "print photo", "instant print", "image"])
def _(S):
    return [shell(rect(3, 3, 18, 8.5, rr(S, 3))), dot(17, 7, 1),
            shell(rect(6.5, 11.5, 11, 10, min(S.R, 1))),
            detail(poly([(8.25, 19.25), (11.25, 15.75), (13.5, 18.25), (15.25, 16.75)], r=S.r * 0.5))]


@icon("pen-scanner", CAT, "Pen shaped scanner gliding along a line of text and lighting it",
      tags=["handheld scanner", "text scanner", "reading pen", "ocr", "highlighter scanner", "scan text"])
def _(S):
    pen = rot([(9.5, 1.5), (14.5, 1.5), (14.5, 13.5), (13, 17), (11, 17), (9.5, 13.5)], 25, 12, 17)
    win = rot([(12, 5), (12, 9)], 25, 12, 17)
    return [shell(poly(pen, closed=True, r=S.r * 0.6)), detail(seg(win[0][0], win[0][1], win[1][0], win[1][1])),
            line(seg(3, 21, 8, 21)), line(seg(11, 21, 14, 21)), line(seg(17, 21, 21, 21))]


@icon("book-scanner", CAT, "Open book lying in a V shaped cradle under an overhead camera arm",
      tags=["book digitizing", "overhead scanner", "library scanner", "archive scanning", "camera arm"])
def _(S):
    book = [(3, 12), (10, 15), (17, 12), (17, 18), (10, 21), (3, 18)]
    return [shell(poly(book, closed=True, r=S.r * 0.6)), detail(seg(10, 15, 10, 21)),
            shell(rect(7, 2.5, 7, 4.5, min(S.R, 1.5))), line(poly([(20.5, 21), (20.5, 4.75), (14, 4.75)], r=S.r))]


@icon("film-scanner", CAT, "Small box scanner with a strip of negative film entering from the side",
      tags=["negative scanner", "slide scanner", "film strip", "photo digitizing", "35mm", "transparency"])
def _(S):
    return [shell(rect(9, 4.5, 12.5, 15, rr(S, 3))), dot(17.5, 9, 1), detail(seg(13, 15.5, 18, 15.5)),
            line(poly([(9, 8), (2.5, 8), (2.5, 16), (9, 16)])), block(4.5, 10.5, 3, 3)]


@icon("mobile-scan", CAT, "Phone screen with four corner brackets framing a page",
      tags=["scan document", "phone scanner", "camera scan", "capture", "scanning app", "digitize"])
def _(S):
    br = [poly([(8.5, 9.5), (8.5, 7.5), (10.5, 7.5)]), poly([(13.5, 7.5), (15.5, 7.5), (15.5, 9.5)]),
          poly([(8.5, 14.5), (8.5, 16.5), (10.5, 16.5)]), poly([(13.5, 16.5), (15.5, 16.5), (15.5, 14.5)])]
    return [shell(rect(5, 2.5, 14, 19, S.R)), *[detail(b) for b in br], detail(seg(10.5, 12, 13.5, 12))]


@icon("print-queue", CAT, "Printer with a column of three pages lined up beside it",
      tags=["print jobs", "spooler", "waiting pages", "printing list", "job queue", "documents waiting"])
def _(S):
    col = [shell(rect(15, y, 6.5, 4, min(S.R, 1.5))) for y in (3.5, 10, 16.5)]
    return [shell(rect(2.5, 10.5, 9.5, 9, rr(S, 2.5))), line(poly([(4.5, 10.5), (4.5, 5), (10, 5), (10, 10.5)], r=S.r)),
            dot(9.5, 15, 1), *col]


@icon("certified-copy", CAT, "Page with a stamped rectangle marking it as a copy and a small seal",
      tags=["true copy", "certified", "duplicate", "copy stamp", "notarized", "attested", "photocopy"])
def _(S):
    return [*page(S), detail(rect(8, 9.5, 8, 4.5, min(S.R, 1))), detail(seg(8.5, 18, 11.5, 18)), dot(15.5, 17.5, 1.75)]


def dashed_rect(x, y, w, h, arm=3.0, dl=2.5, r=0.0, role=detail):
    """Dashed outline: an L at each corner and evenly spaced dashes along each side."""
    x2, y2 = x + w, y + h
    out = [role(poly([(x, y + arm), (x, y), (x + arm, y)], r=r)), role(poly([(x2 - arm, y), (x2, y), (x2, y + arm)], r=r)),
           role(poly([(x2, y2 - arm), (x2, y2), (x2 - arm, y2)], r=r)), role(poly([(x + arm, y2), (x, y2), (x, y2 - arm)], r=r))]

    def mids(length):
        m = length - 2 * arm
        n = 0
        while (m - (n + 1) * dl) / (n + 2) >= 1.6:
            n += 1
        g = (m - n * dl) / (n + 1)
        return [arm + g * (k + 1) + dl * k for k in range(n)]
    for a in mids(w):
        out += [role(seg(x + a, y, x + a + dl, y)), role(seg(x + a, y2, x + a + dl, y2))]
    for a in mids(h):
        out += [role(seg(x, y + a, x, y + a + dl)), role(seg(x2, y + a, x2, y + a + dl))]
    return out


@icon("tracing-paper", CAT, "Dashed translucent sheet laid partly over a drawing on a page beneath",
      tags=["trace", "overlay", "vellum", "drawing", "copy drawing", "draft", "layer"])
def _(S):
    return [shell(rect(3, 3, 12, 13, rr(S, 2))), dot(7.5, 7.5, 1.75), *dashed_rect(9, 9, 12, 12, arm=3.5, dl=2)]


# ============================================================================ chunk 2

@icon("book-cart", CAT, "Library trolley with two shelves of books and small wheels",
      tags=["book trolley", "library cart", "shelving cart", "returns", "librarian", "school library"])
def _(S):
    up = [block(7.5, 5.5, 2, 4), block(11, 4.5, 2, 5), block(14.5, 6, 2, 3.5)]
    low = [block(7.5, 13.5, 2, 3.5), block(11, 12.5, 2, 4.5), block(14.5, 14, 2, 3)]
    return [shell(rect(3.5, 3, 17, 15, min(S.R, 3))), detail(seg(3.5, 11, 20.5, 11)), *up, *low,
            dot(7, 20.75, 1.25), dot(17, 20.75, 1.25)]


@icon("book-drop", CAT, "Return box with a slot in the front and a book dropping into it",
      tags=["book return", "library drop box", "return slot", "library", "returns", "overnight drop"])
def _(S):
    return [line(poly([(7, 10), (7, 2.5), (17, 2.5), (17, 10)], r=S.r)), line(seg(10.5, 3, 10.5, 9)),
            shell(rect(3, 9.5, 18, 12, S.R)), detail(seg(7.5, 15, 16.5, 15))]


@icon("file-rtf", CAT, "Page with a folded corner and a solid tag band across its lower half",
      tags=["rtf", "rich text", "formatted text", "document", "word processor", "file format"])
def _(S):
    return [*page(S), detail(seg(8.5, 10.5, 15.5, 10.5)), block(8, 15, 8, 4)]


@icon("file-bookmark", CAT, "Page with a folded corner and a ribbon bookmark with a notched tail",
      tags=["saved file", "bookmarked page", "favorite document", "ribbon", "marker", "read later"])
def _(S):
    return [*page(S), detail(poly([(8, 2.5), (8, 13), (9.5, 11.5), (11, 13), (11, 2.5)], r=S.r * 0.4)),
            detail(seg(8, 17.5, 16, 17.5))]


@icon("virtual-folder", CAT, "Folder drawn with a dashed outline and a solid tab",
      tags=["virtual", "smart folder", "saved search", "collection", "label folder", "dynamic folder"])
def _(S):
    tab = poly([(2, 4.5), (9.5, 4.5), (11.5, 8.5), (2, 8.5)], closed=True, r=S.r * 0.6)
    return [solid(tab), *dashed_rect(3, 8, 18, 12, arm=3, dl=2.5, r=S.r)]


@icon("folder-shortcut", CAT, "Folder with a small square in the lower left corner holding a curved arrow",
      tags=["shortcut", "alias", "link", "symlink", "folder link", "quick access"])
def _(S):
    outline = poly([(12.5, 20.5), (21.5, 20.5), (21.5, 7), (11.5, 7), (9.5, 4.5), (2.5, 4.5), (2.5, 12)], r=S.r)
    arrow = poly([(6, 19.5), (6, 18), (7.25, 17), (9.5, 17)], r=S.r * 0.4)
    head = poly([(8, 15.25), (9.75, 17), (8, 18.75)])
    return [line(outline), shell(rect(2.5, 12.5, 10, 9, min(S.R, 2))), detail(arrow), detail(head)]


@icon("lottery-ticket", CAT, "Ticket with a grid of small numbers, three of them circled",
      tags=["lottery", "lotto", "raffle", "draw", "numbers", "gambling", "jackpot", "pick numbers"])
def _(S):
    R = S.R
    x, y, w, h, by = 2.5, 3, 19, 18, 7
    d = (f"M{fmt(x + R)} {y}H{fmt(x + w - R)}A{R} {R} 0 0 1 {x + w} {y + R}V{by - 1.5}A1.5 1.5 0 0 0 {x + w} {by + 1.5}"
         f"V{y + h - R}A{R} {R} 0 0 1 {fmt(x + w - R)} {y + h}H{fmt(x + R)}A{R} {R} 0 0 1 {x} {y + h - R}"
         f"V{by + 1.5}A1.5 1.5 0 0 0 {x} {by - 1.5}V{y + R}A{R} {R} 0 0 1 {fmt(x + R)} {y}Z")
    marks = [(7, 11.75), (12, 16.25), (17, 11.75)]
    plain = [(12, 11.75), (7, 16.25), (17, 16.25)]
    return [shell(d), detail(seg(5, 7, 19, 7)),
            *[detail(circle(px, py, 1.75)) for px, py in marks], *[dot(px, py, 0.9) for px, py in plain]]


@icon("scratch-card", CAT, "Card with a coated panel partly scratched away and a coin beside it",
      tags=["scratcher", "scratch off", "instant win", "lottery card", "prize", "coin", "gift card"])
def _(S):
    coat = poly([(5.5, 6.5), (14.5, 6.5), (12.5, 8.5), (14.5, 10.5), (12.5, 12), (14.5, 13.5), (5.5, 13.5)],
                closed=True, r=S.r * 0.3)
    return [shell(rect(2.5, 3, 19, 18, S.R)), Part("dot", coat), detail(seg(16.5, 7.5, 17.5, 8.5)), detail(seg(16.5, 11.5, 17.5, 12.5)),
            detail(circle(16.5, 17, 1.5))]


@icon("lyric-sheet", CAT, "Page with a music note at the top left and short verse lines below",
      tags=["lyrics", "song words", "songbook", "verse", "music sheet", "karaoke", "chorus"])
def _(S):
    return [*page(S), dot(8.5, 10.5, 1.5), detail(seg(10, 10.5, 10, 6)),
            detail(seg(8, 14.5, 16, 14.5)), detail(seg(8, 18, 13, 18))]


@icon("cartouche", CAT, "Upright rounded oblong with a short bar at its base enclosing three small glyphs",
      tags=["hieroglyph", "egyptian", "pharaoh", "royal name", "ancient egypt", "oval", "glyphs"])
def _(S):
    body = rect(6, 2.5, 12, 15.5, 3 if S.name == "line" else 6)
    return [shell(body), dot(12, 6.75, 1.4), detail(seg(10.5, 10.5, 13.5, 10.5)),
            detail(poly([(10, 15), (12, 13.5), (14, 15)])), line(seg(4.5, 21, 19.5, 21))]


@icon("hornbook", CAT, "Paddle shaped board with a short handle and letters on its face",
      tags=["horn book", "primer", "alphabet board", "early reading", "abc", "old school", "paddle"])
def _(S):
    pts = [(6, 2.5), (18, 2.5), (18, 15), (14, 15), (14, 21.5), (10, 21.5), (10, 15), (6, 15)]
    return [shell(poly(pts, closed=True, r=S.r)), detail(seg(9.5, 6.5, 14.5, 6.5)), detail(seg(9.5, 10.5, 12.5, 10.5))]


@icon("daisy-wheel", CAT, "Print wheel with thin spokes radiating from a hub, each ending in a small letter pad",
      tags=["print wheel", "typewriter", "impact printer", "typing element", "retro office", "letters"])
def _(S):
    out = [shell(circle(12, 12, 2.5))]
    for i in range(8):
        a = -90 + i * 45
        p1, p2, p3 = polar(12, 12, 3.5, a), polar(12, 12, 7.25, a), polar(12, 12, 8.4, a)
        pad = dot(p3[0], p3[1], 1.6) if S.name == "rounded" else Part("dot", poly(rot([(p3[0] - 1.5, p3[1] - 1.5), (p3[0] + 1.5, p3[1] - 1.5), (p3[0] + 1.5, p3[1] + 1.5), (p3[0] - 1.5, p3[1] + 1.5)], a + 90, p3[0], p3[1]), closed=True))
        out += [line(seg(*p1, *p2)), pad]
    return out


@icon("dust-jacket", CAT, "Hardcover book with its paper jacket partly slid off, showing the plain board beneath",
      tags=["book jacket", "book cover", "hardback", "sleeve", "cover", "wrapper", "hardcover"])
def _(S):
    return [line(poly([(9.5, 3), (3.5, 3), (3.5, 21), (9.5, 21)], r=S.r)),
            shell(rect(9.5, 3, 12, 18, S.R)), detail(seg(12.5, 8, 18.5, 8)), detail(seg(12.5, 12, 16.5, 12))]


@icon("book-light", CAT, "Small clip-on lamp with a bendy neck clipped to the edge of an open book",
      tags=["reading light", "clip light", "night reading", "lamp", "bedtime", "booklight"])
def _(S):
    book = [(12, 13.5), (8, 12), (2.5, 12), (2.5, 21), (8, 21), (12, 22), (16, 21), (21.5, 21), (21.5, 12), (16, 12)]
    return [shell(poly(book, closed=True, r=S.r)), detail(seg(12, 13.5, 12, 22)),
            line(poly([(18.5, 12), (18.5, 7.5), (15.5, 4.5)], r=S.r)), shell(poly([(9, 3), (16, 3), (14.5, 7), (10.5, 7)], closed=True, r=S.r * 0.4))]


@icon("paid-stamp", CAT, "Slanted rectangular stamp mark with a border and a word in the middle",
      tags=["paid", "settled", "invoice stamp", "payment received", "cleared", "rubber stamp", "receipt stamp"])
def _(S):
    def R(x, y, w, h):
        return rot([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], -14)
    blocks = [Part("dot", poly(R(x, 10, 1.75, 4), closed=True)) for x in (6.5, 9.75, 13, 16.25)]
    return [shell(poly(R(3.5, 5.5, 17, 13), closed=True, r=S.r * 0.8)), *blocks]


# ============================================================================ chunk 3

def form_sheet(S):
    return shell(rect(3.5, 2.5, 17, 19, S.R))


@icon("page-margins", CAT, "Page outline with a dashed inner rectangle marking the margins on all four sides",
      tags=["margins", "layout", "print area", "page setup", "gutter", "text area", "border"])
def _(S):
    return [sheet(S), *dashed_rect(8.5, 6, 7, 12, arm=2.5, dl=2, r=S.r * 0.5)]


@icon("cornell-notes", CAT, "Page divided into a narrow cue column, a wide notes area and a summary strip at the bottom",
      tags=["note taking", "study notes", "lecture notes", "cues", "summary", "student", "study method"])
def _(S):
    return [sheet(S), detail(seg(9.5, 2.5, 9.5, 15.5)), detail(seg(4.5, 15.5, 19.5, 15.5)),
            detail(seg(12, 6.5, 17, 6.5)), detail(seg(12, 10.5, 17, 10.5)), detail(seg(7.5, 19, 16.5, 19))]


@icon("handwriting-paper", CAT, "Ruled page with solid lines and dashed midlines for practising handwriting",
      tags=["writing practice", "penmanship", "lined paper", "primary school", "letters", "guidelines", "cursive"])
def _(S):
    out = [sheet(S), detail(seg(5.5, 6, 18.5, 6)), detail(seg(5.5, 14, 18.5, 14))]
    for y in (10, 18):
        out += [detail(seg(6.5, y, 9.5, y)), detail(seg(11.5, y, 14.5, y))]
    return out


def briefcase_mark(cx=12, cy=8.5):
    return [detail(rect(cx - 4, cy - 1.5, 8, 5, 1)), detail(poly([(cx - 1.5, cy - 1.5), (cx - 1.5, cy - 3.5), (cx + 1.5, cy - 3.5), (cx + 1.5, cy - 1.5)]))]


@icon("job-description", CAT, "Page with a small briefcase at the top and bulleted lines below",
      tags=["job posting", "role", "vacancy", "hiring", "career", "position", "recruitment"])
def _(S):
    return [form_sheet(S), *briefcase_mark(12, 9), dot(7, 15.5, 1), detail(seg(10, 15.5, 16.5, 15.5)),
            dot(7, 18.5, 1), detail(seg(10, 18.5, 14.5, 18.5))]


def handshake_mark(cx=12, cy=9):
    return [dot(cx - 5.25, cy, 1.25), dot(cx + 5.25, cy, 1.25),
            detail(poly([(cx - 4, cy), (cx - 1.5, cy - 2), (cx + 1.5, cy - 2), (cx + 4, cy)])),
            detail(poly([(cx - 3, cy + 1.75), (cx, cy + 1.75), (cx + 3, cy + 1.75)]))]


@icon("bill-of-sale", CAT, "Page with a handshake at the top and two signature lines at the bottom",
      tags=["sale agreement", "purchase record", "transfer of ownership", "deal", "contract", "receipt of sale"])
def _(S):
    return [form_sheet(S), *handshake_mark(12, 8.5), detail(seg(6.5, 18, 10.75, 18)), detail(seg(13.25, 18, 17.5, 18))]


def car_mark(cx=12, cy=9):
    body = [(cx - 5, cy + 2), (cx - 5, cy), (cx - 3, cy), (cx - 1.75, cy - 2), (cx + 1.75, cy - 2), (cx + 3, cy), (cx + 5, cy), (cx + 5, cy + 2)]
    return [detail(poly(body)), dot(cx - 3, cy + 2.25, 1.1), dot(cx + 3, cy + 2.25, 1.1)]


@icon("vehicle-title", CAT, "Page with a small car at the top and a round seal in the lower corner",
      tags=["car title", "ownership document", "registration", "pink slip", "dmv", "vehicle papers", "car sale"])
def _(S):
    return [form_sheet(S), *car_mark(12, 8), detail(seg(6.5, 14.5, 10.5, 14.5)), detail(seg(6.5, 18.5, 10.5, 18.5)),
            detail(circle(15.5, 17.25, 1.5))]


@icon("business-license", CAT, "Framed certificate with a small shop awning at the top",
      tags=["trade license", "permit", "company registration", "shop permit", "certificate", "storefront", "authorization"])
def _(S):
    awning = poly([(8, 10), (9.25, 6.5), (14.75, 6.5), (16, 10)], closed=True)
    return [shell(rect(2.5, 3, 19, 18, S.R)), detail(awning), detail(seg(12, 6.5, 12, 10)),
            detail(seg(7, 14, 17, 14)), detail(seg(7, 17.5, 12, 17.5)), dot(16, 17.5, 1.25)]


@icon("divorce-decree", CAT, "Page with a single ring split into two broken halves at the top",
      tags=["divorce", "separation", "legal papers", "broken ring", "family court", "dissolution", "marriage end"])
def _(S):
    return [form_sheet(S), detail(arc(10.75, 8.5, 3.25, 100, 260)), detail(arc(13.25, 8.5, 3.25, -80, 80)),
            detail(seg(7, 15, 17, 15)), detail(seg(7, 18.5, 13, 18.5))]


@icon("inventory-sheet", CAT, "Page with rows that each begin with a small box and end with a count",
      tags=["stock list", "stocktake", "stock count", "checklist", "warehouse", "items", "counting sheet"])
def _(S):
    out = [form_sheet(S)]
    for y in (7, 12, 17):
        out += [block(6.5, y - 1.5, 3, 3), detail(seg(11.5, y, 14, y)), detail(seg(16, y, 17.5, y))]
    return out


def tag_mark(cx=12, cy=8.5):
    return [detail(poly([(cx - 4.5, cy - 2), (cx + 1.5, cy - 2), (cx + 4.5, cy), (cx + 1.5, cy + 2), (cx - 4.5, cy + 2)], closed=True)),
            dot(cx - 2, cy, 0.8)]


@icon("sales-quote", CAT, "Page with a small price tag at the top and item lines with a total below",
      tags=["quotation", "estimate", "price quote", "proposal", "pricing", "offer", "bid"])
def _(S):
    return [form_sheet(S), *tag_mark(12, 8), detail(seg(6.5, 13.5, 11, 13.5)), detail(seg(14, 13.5, 17.5, 13.5)),
            detail(seg(6.5, 17, 11, 17)), block(14, 16, 3.5, 2)]


def ship_mark(cx=12, cy=8):
    hull = [(cx - 6, cy + 1), (cx + 6, cy + 1), (cx + 4, cy + 3.5), (cx - 4, cy + 3.5)]
    return [detail(poly(hull, closed=True)), block(cx - 4, cy - 2.5, 3, 2.5), block(cx, cy - 2.5, 3, 2.5)]


@icon("bill-of-lading", CAT, "Page with a small cargo ship at the top and table lines below",
      tags=["shipping document", "freight", "cargo", "consignment", "export", "maritime", "manifest"])
def _(S):
    return [form_sheet(S), *ship_mark(12, 7.5), detail(seg(3.5, 14, 20.5, 14)), detail(seg(3.5, 18, 20.5, 18)),
            detail(seg(11.5, 14, 11.5, 21.5))]


@icon("large-print-book", CAT, "Book with a large letter A printed on its cover",
      tags=["big print", "low vision", "accessible book", "easy reading", "large type", "elderly reading", "enlarged text"])
def _(S):
    return [sheet(S), detail(seg(8.5, 2.5, 8.5, 21.5)),
            detail(poly([(10.5, 15.5), (13.75, 7.5), (17, 15.5)])), detail(seg(11.6, 12.75, 15.9, 12.75)), detail(seg(11, 18.25, 16.5, 18.25))]


@icon("document-summary", CAT, "Long page with many lines beside a short page with two lines, an arrow pointing from long to short",
      tags=["summary", "condense", "tldr", "abstract", "shorten", "digest", "executive summary"])
def _(S):
    out = [shell(rect(3, 2.5, 6, 19, min(S.R, 2))), shell(rect(16, 6.5, 5, 11, min(S.R, 2)))]
    out += [detail(seg(5.25, y, 6.75, y)) for y in (6.5, 10, 13.5, 17)]
    out += [detail(seg(17.75, 10.5, 19.25, 10.5)), detail(seg(17.75, 13.5, 19.25, 13.5))]
    out += [line(seg(10.75, 12, 13.75, 12)), line(poly([(12.25, 10), (14, 12), (12.25, 14)]))]
    return out


@icon("red-tape", CAT, "Stack of papers tied up with a ribbon crossing over the top",
      tags=["bureaucracy", "paperwork", "admin burden", "forms pile", "tied bundle", "official procedure", "ribbon"])
def _(S):
    return [line(poly([(6, 9.5), (6, 5.5), (20.5, 5.5), (20.5, 17)], r=S.r)), shell(rect(3.5, 9.5, 13, 11.5, S.R)),
            detail(seg(8, 9.5, 8, 21)), detail(seg(12, 9.5, 12, 21))]


@icon("page-thumbnails", CAT, "Grid of four small pages with the top left one marked as selected",
      tags=["pages panel", "page preview", "slide sorter", "contact sheet", "document pages", "navigator", "thumbnails"])
def _(S):
    r = min(S.R, 2) / 2 if S.name == "line" else 1.5
    return [shell(rect(3, 3, 7, 7, r)), block(5, 5, 3, 3), shell(rect(14, 3, 7, 7, r)),
            shell(rect(3, 14, 7, 7, r)), shell(rect(14, 14, 7, 7, r))]


# ============================================================================ chunk 4

@icon("document-pouch", CAT, "Flat clear pouch holding a page, closed with a round snap button on the flap",
      tags=["snap wallet", "plastic envelope", "document wallet", "file pouch", "carrying case", "a4 sleeve", "stud wallet"])
def _(S):
    return [shell(rect(3.5, 4, 17, 16, S.R)), detail(seg(3.5, 8.5, 20.5, 8.5)), dot(12, 8.5, 1.5),
            detail(seg(7.5, 13.5, 16.5, 13.5)), detail(seg(7.5, 16.75, 13, 16.75))]


@icon("cylinder-seal", CAT, "Small stone cylinder rolling across a clay strip and leaving a band of pattern",
      tags=["roller seal", "mesopotamia", "ancient seal", "clay tablet", "impression", "archaeology", "stamp roller"])
def _(S):
    body = "M7 3.5H16A2.5 4.5 0 0 1 16 12.5H7A2.5 4.5 0 0 1 7 3.5Z"
    return [shell(body), detail("M7 3.5A2.5 4.5 0 0 1 7 12.5"), shell(rect(2.5, 16, 19, 5, S.R)),
            dot(10, 18.5, 0.8), dot(13.25, 18.5, 0.8), dot(16.5, 18.5, 0.8)]


@icon("trifold-display-board", CAT, "Standing board with a wide center panel and two angled side panels showing pinned sheets",
      tags=["science fair", "poster board", "project board", "exhibit", "presentation board", "tri-fold", "display"])
def _(S):
    outline = [(3, 7), (8, 5), (16, 5), (21, 7), (21, 19), (16, 21), (8, 21), (3, 19)]
    return [shell(poly(outline, closed=True, r=S.r * 0.5)), detail(seg(8, 5, 8, 21)), detail(seg(16, 5, 16, 21)),
            block(10.5, 8, 3, 4), dot(5.5, 12, 0.9), dot(18.5, 12, 0.9), detail(seg(10.5, 16, 13.5, 16))]


@icon("multi-step-form", CAT, "Form page with a row of three joined step circles at the top and fields below",
      tags=["wizard", "stepper", "progress steps", "onboarding form", "checkout steps", "survey pages", "application form"])
def _(S):
    return [form_sheet(S), detail(seg(7.5, 7, 16.5, 7)), dot(7.5, 7, 1.75), dot(12, 7, 1.75), dot(16.5, 7, 1.75),
            detail(seg(7, 12.5, 17, 12.5)), detail(seg(7, 16.5, 17, 16.5))]


@icon("reading-ruler", CAT, "Clear strip laid over lines of text, tinting a single line",
      tags=["reading guide", "line focus", "dyslexia", "tracking ruler", "highlight strip", "overlay", "screen ruler"])
def _(S):
    return [line(seg(4, 4.5, 20, 4.5)), shell(rect(2.5, 9.5, 19, 6, rr(S, 2))), detail(seg(6, 12.5, 18, 12.5)),
            line(seg(4, 20.5, 16, 20.5))]


@icon("book-strap", CAT, "Stack of three books held together by a leather strap with a buckle and a carrying handle",
      tags=["book belt", "school books", "carry books", "student", "book carrier", "buckle strap", "handle"])
def _(S):
    steps = [(3, 21), (3, 16), (4.5, 16), (4.5, 11), (6, 11), (6, 6.5), (18, 6.5), (18, 11), (19.5, 11), (19.5, 16), (21, 16), (21, 21)]
    return [shell(poly(steps, closed=True, r=S.r * 0.5)), detail(seg(4.5, 16, 19.5, 16)), detail(seg(6, 11, 18, 11)),
            line(poly([(9, 6.5), (9, 3.5), (15, 3.5), (15, 6.5)], r=S.r)), detail(seg(14.5, 6.5, 14.5, 21)), block(13, 12, 3, 2.5)]


@icon("torn-page", CAT, "Notebook page with a ragged torn left edge and punch holes at the torn side",
      tags=["ripped paper", "torn sheet", "removed page", "missing page", "tear", "notebook", "scrap"])
def _(S):
    pts = [(19, 2.5), (19, 21.5), (9, 21.5), (7, 19), (9.5, 16.5), (6.5, 14), (9, 11.5), (7, 9), (9.5, 6.5), (7, 4.5), (9, 2.5)]
    return [shell(poly(pts, closed=True, r=S.r * 0.4)), dot(11.25, 8.25, 1), dot(11.25, 15.25, 1),
            detail(seg(14, 8, 17, 8)), detail(seg(14, 12, 17, 12)), detail(seg(14, 16, 17, 16))]


@icon("document-handover", CAT, "Two hands passing a single sheet of paper between them",
      tags=["pass document", "give paper", "hand over", "submit", "deliver papers", "exchange", "transfer"])
def _(S):
    sheet_a = line(poly([(8.5, 11), (8.5, 3), (15.5, 3), (15.5, 4.5)], r=S.r))
    sheet_b = line(poly([(15.5, 14.5), (15.5, 17), (13.5, 17)], r=S.r))
    return [sheet_a, sheet_b, shell(rect(3, 14, 8, 5, min(S.R, 2.5))), shell(rect(13, 7, 8, 5, min(S.R, 2.5))),
            detail(seg(6, 14, 6, 19)), detail(seg(18, 7, 18, 12))]


@icon("seating-chart", CAT, "Page with a grid of small desk rectangles, each with a short name line",
      tags=["seating plan", "classroom layout", "desks", "table plan", "wedding seating", "class chart", "seats"])
def _(S):
    out = [form_sheet(S)]
    for x in (6.5, 12.5):
        for y, ny in ((5.5, 10.5), (13.5, 18.5)):
            out += [block(x, y, 5, 3), detail(seg(x + 1, ny, x + 4, ny))]
    return out


@icon("sign-up-sheet", CAT, "Clipboard with numbered name lines and a pen tied on a string",
      tags=["attendance", "volunteer list", "roster", "sign in sheet", "names", "registration", "signup"])
def _(S):
    out = [shell(rect(3.5, 4.25, 13, 17.25, S.R)), shell(rect(6, 2.5, 8, 4, min(S.R, 1.5)))]
    for y in (10.5, 14, 17.5):
        out += [dot(6.75, y, 0.9), detail(seg(9.5, y, 13.5, y))]
    out += [line(poly([(14, 4.5), (19.5, 4.5), (19.5, 9)], r=S.r)),
            shell(poly([(18, 9), (21, 9), (21, 17), (19.5, 19.5), (18, 17)], closed=True, r=S.r * 0.3))]
    return out


@icon("gradebook", CAT, "Open book with a grid of small cells on one page and a grade mark on the other",
      tags=["grades", "marks", "teacher record", "report card", "class record", "a plus", "scores"])
def _(S):
    pts = [(12, 6), (8, 4.5), (2.5, 4.5), (2.5, 18.5), (8, 18.5), (12, 20.5), (16, 18.5), (21.5, 18.5), (21.5, 4.5), (16, 4.5)]
    return [shell(poly(pts, closed=True, r=S.r)), detail(seg(12, 6, 12, 20.5)), detail(seg(3.5, 9.5, 11, 9.5)),
            detail(seg(3.5, 14, 11, 14)), detail(seg(7.25, 4.5, 7.25, 18.5)),
            detail(poly([(13.75, 16), (16, 9.5), (18.25, 16)])), detail(seg(14.6, 13.5, 17.4, 13.5))]


@icon("circuit-schematic", CAT, "Page with a zigzag resistor, a capacitor gap and connecting lines",
      tags=["electronics diagram", "wiring diagram", "circuit diagram", "resistor", "capacitor", "electrical", "engineering drawing"])
def _(S):
    zig = poly([(8, 8.5), (9, 6), (10.75, 11), (12.5, 6), (14.25, 11), (15, 8.5)], r=S.r * 0.3)
    return [form_sheet(S), detail(seg(5, 8.5, 8, 8.5)), detail(zig), detail(seg(15, 8.5, 19, 8.5)),
            detail(seg(5, 16.5, 10.25, 16.5)), detail(seg(10.25, 13.5, 10.25, 19.5)), detail(seg(13.75, 13.5, 13.75, 19.5)),
            detail(seg(13.75, 16.5, 19, 16.5))]


@icon("playbook", CAT, "Clipboard showing X and O marks with a curved arrow tracing a play",
      tags=["game plan", "strategy", "coach", "football play", "tactics", "team plan", "diagram plays"])
def _(S):
    return [shell(rect(5, 4, 14, 17.5, S.R)), shell(rect(8.5, 2.5, 7, 4, min(S.R, 1.5))),
            detail(seg(7.25, 9, 9.75, 11.5)), detail(seg(9.75, 9, 7.25, 11.5)), detail(circle(15.5, 10.25, 1.5)),
            detail("M8.5 14C8.5 18 11.5 18 14.5 17.5"), detail(poly([(13.25, 15.5), (15.25, 17.5), (13, 19)]))]


@icon("character-sheet", CAT, "Page with a portrait box, stat boxes and a small twenty sided die",
      tags=["rpg", "tabletop", "dungeons", "role playing", "player sheet", "stats", "d20", "game master"])
def _(S):
    hexa = regular(15.25, 16.25, 2.4, 6, start=-90)
    return [form_sheet(S), detail(rect(6.5, 5.5, 5, 5.5, 1)), block(14, 5.5, 3.5, 2.25), block(14, 9, 3.5, 2.25),
            detail(seg(6.5, 15, 10, 15)), detail(seg(6.5, 18.5, 10, 18.5)), detail(poly(hexa, closed=True))]


@icon("golf-scorecard", CAT, "Narrow card with a grid of hole numbers and a small pencil beside it",
      tags=["golf", "score sheet", "course card", "holes", "par", "round", "tally"])
def _(S):
    return [shell(rect(3, 2.5, 11, 19, S.R)), detail(seg(3, 8.5, 14, 8.5)), detail(seg(3, 14.5, 14, 14.5)), detail(seg(8.5, 2.5, 8.5, 21.5)),
            shell(poly([(18, 4), (21, 4), (21, 16), (19.5, 19.5), (18, 16)], closed=True, r=S.r * 0.3)), detail(seg(18, 7.5, 21, 7.5))]


# ============================================================================ chunk 5

BAND = (7, 15.5, 10, 4)


def fmt_file(S, *mark):
    return [*page(S), *mark, block(*BAND)]


@icon("file-webp", CAT, "Page with a folded corner, a small mountain picture and a solid tag band below",
      tags=["webp", "web image", "image format", "picture file", "google image", "compressed image", "lossy image"])
def _(S):
    return fmt_file(S, detail(poly([(8, 13.25), (10.75, 9.5), (13, 12), (14.5, 10.75), (16.5, 13.25)], r=S.r * 0.4)))


@icon("file-bmp", CAT, "Page with a folded corner, a few pixel squares and a solid tag band below",
      tags=["bmp", "bitmap", "raster image", "pixel image", "windows bitmap", "image format", "pixels"])
def _(S):
    return fmt_file(S, block(8, 9, 2, 2), block(12, 9, 2, 2), block(10, 12, 2, 2), block(14, 12, 2, 2))


@icon("file-eps", CAT, "Page with a folded corner, a small pen nib and a solid tag band below",
      tags=["eps", "postscript", "vector art", "encapsulated postscript", "print graphic", "illustrator", "vector format"])
def _(S):
    return fmt_file(S, detail(poly([(12, 8.75), (14.25, 12.5), (12, 14), (9.75, 12.5)], closed=True, r=S.r * 0.3)))


@icon("file-flac", CAT, "Page with a folded corner, a short waveform and a solid tag band below",
      tags=["flac", "lossless audio", "audio format", "sound file", "music file", "hi-fi", "waveform"])
def _(S):
    return fmt_file(S, detail(seg(8.5, 11, 8.5, 13.5)), detail(seg(12, 9, 12, 14)), detail(seg(15.5, 10.5, 15.5, 13.5)))


@icon("file-avi", CAT, "Page with a folded corner, a small film frame and a solid tag band below",
      tags=["avi", "video format", "movie file", "video clip", "film frame", "media file", "windows video"])
def _(S):
    return fmt_file(S, detail(rect(8, 9.25, 8, 4.25, min(S.R, 1))))


@icon("file-tar", CAT, "Page with a folded corner, a short zipper track and a solid tag band below",
      tags=["tar", "tarball", "archive format", "tape archive", "unix archive", "bundle", "gz"])
def _(S):
    return fmt_file(S, detail(poly([(12, 8.5), (14, 9.75), (10, 11.25), (14, 12.75), (12, 14)], r=S.r * 0.3)))


@icon("activity-book", CAT, "Book with a small maze on the cover and a pencil leaning beside it",
      tags=["puzzle book", "maze book", "kids activities", "workbook", "colouring and puzzles", "children", "games book"])
def _(S):
    maze = poly([(6.5, 17), (6.5, 7.5), (11.5, 7.5), (11.5, 13), (9, 13), (9, 10.5)])
    return [shell(rect(3, 3, 12, 18, S.R)), detail(maze),
            shell(poly([(18.5, 4), (21, 4), (21, 16.5), (19.75, 20), (18.5, 16.5)], closed=True, r=S.r * 0.3)), detail(seg(18.5, 7.5, 21, 7.5))]


@icon("poetry-book", CAT, "Book with a feather quill laid diagonally across its cover",
      tags=["poems", "verse", "anthology", "literature", "quill", "poet", "sonnets"])
def _(S):
    blade = "M17 6C11 6.5 8.5 10.5 9.5 15.5C14 14.5 17 11.5 17 6Z"
    return [sheet(S, 3.5, 2.5, 17, 19), detail(blade), detail(seg(9.5, 15.5, 14.5, 9)), detail(seg(9.5, 15.5, 7.5, 18.5))]


@icon("mystery-novel", CAT, "Book with a detective fedora hat on its cover",
      tags=["detective", "whodunit", "crime fiction", "thriller", "sleuth", "fedora", "noir"])
def _(S):
    return [sheet(S, 3.5, 2.5, 17, 19), detail(seg(7, 2.5, 7, 21.5)), detail(seg(9.5, 13, 18, 13)),
            detail(poly([(10.5, 13), (11, 9), (16.5, 9), (17, 13)], r=S.r * 0.3)), detail(seg(10, 17.5, 17, 17.5))]


@icon("science-fiction-book", CAT, "Book with a ringed planet and a small rocket on its cover",
      tags=["sci-fi", "space novel", "fantasy book", "futuristic", "alien worlds", "planet", "rocket ship"])
def _(S):
    rocket = poly([(11, 19), (11, 16), (12.5, 14), (14, 16), (14, 19)], closed=True, r=S.r * 0.3)
    return [sheet(S, 3.5, 2.5, 17, 19), detail(seg(7, 2.5, 7, 21.5)), detail(circle(14, 8, 2.25)),
            detail(ellipse(14, 8, 4.75, 1.5)), detail(rocket)]


@icon("acceptance-letter", CAT, "Open envelope with a letter rising out of it and a graduation cap on the letter",
      tags=["admission letter", "offer letter", "university", "college", "graduation", "congratulations", "enrollment"])
def _(S):
    front = poly([(3, 12), (12, 17), (21, 12), (21, 21), (3, 21)], closed=True, r=S.r * 0.6)
    letter = poly([(7, 14.2), (7, 3), (17, 3), (17, 14.2)], r=S.r)
    return [line(letter), shell(front), detail(poly([(12, 5.75), (15.5, 7.5), (12, 9.25), (8.5, 7.5)], closed=True))]


@icon("wireless-printer", CAT, "Printer with signal arcs rising above it",
      tags=["wifi printer", "network printer", "bluetooth printing", "print from phone", "airprint", "remote printing", "office"])
def _(S):
    tray = poly([(6.5, 14), (8, 11), (16, 11), (17.5, 14)], closed=True, r=S.r * 0.3)
    return [shell(tray), shell(rect(3, 14, 18, 7, rr(S, 3))), detail(seg(7.5, 17.5, 16.5, 17.5)), dot(12, 8, 0.9),
            line(arc(12, 8, 2.75, -135, -45)), line(arc(12, 8, 5.25, -135, -45))]


@icon("braille-printer", CAT, "Embosser with a page coming out that is covered in raised dot cells",
      tags=["braille embosser", "tactile printing", "blind", "accessibility", "raised dots", "visually impaired", "braille paper"])
def _(S):
    dots = [(8.75, 5.5), (8.75, 8.25), (11, 5.5), (14, 5.5), (14, 8.25), (16.25, 8.25)]
    return [line(poly([(6, 12), (6, 3), (18, 3), (18, 12)], r=S.r)), *[dot(x, y, 0.8) for x, y in dots],
            shell(rect(3, 12, 18, 9, rr(S, 3))), detail(seg(7.5, 16.5, 16.5, 16.5))]


@icon("file-preview", CAT, "Page with a folded corner and an open eye in the middle",
      tags=["quick look", "preview", "view file", "peek", "show document", "read only", "visible"])
def _(S):
    return [*page(S), detail("M7.5 14.5Q12 9.5 16.5 14.5Q12 19.5 7.5 14.5Z"), dot(12, 14.5, 1.3)]


@icon("file-info", CAT, "Page with a folded corner and a lowercase i inside a circle",
      tags=["file details", "properties", "about file", "metadata", "information", "help document", "readme"])
def _(S):
    return [*page(S), detail(circle(12, 14.5, 3.75)), dot(12, 13, 0.8), detail(seg(12, 15, 12, 16.25))]


@icon("ransom-note", CAT, "Note made of cut out letters of mismatched sizes glued in uneven rows",
      tags=["kidnap note", "cut out letters", "anonymous letter", "threat note", "collage text", "crime", "clippings"])
def _(S):
    def tile(x, y, w, h, deg):
        c = (x + w / 2, y + h / 2)
        pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        return Part("dot", poly(rot(pts, deg, c[0], c[1]), closed=True))
    return [form_sheet(S), tile(6, 5.5, 3, 4, -8), tile(10.5, 6.5, 2.5, 3, 6), tile(14.5, 5, 3.5, 5, -4),
            tile(6, 12, 3.5, 3, 7), tile(11, 11.5, 2.5, 4.5, -6), tile(15, 12.5, 3, 3, 5),
            tile(6.5, 17, 2.5, 3, -5), tile(11, 17, 3.5, 2.5, 4)]


@icon("newspaper-holder", CAT, "Newspaper hanging from a long wooden rod clamped along its fold",
      tags=["newspaper rack", "reading room", "periodical hanger", "cafe newspaper", "news stick", "library", "press"])
def _(S):
    return [shell(rect(4, 3, 16, 3.5, 1.5)), dot(2.75, 4.75, 1.25), dot(21.25, 4.75, 1.25),
            shell(rect(5.5, 8, 13, 13.5, rr(S, 2))), block(8, 10.5, 8, 2.5), detail(seg(12, 14.5, 12, 21.5)),
            detail(seg(8, 16, 10, 16)), detail(seg(14, 16, 16, 16)), detail(seg(8, 19, 10, 19))]


@icon("3d-scanner", CAT, "Cube on a flat turntable with a scanning head casting a fan of light lines onto it",
      tags=["3d scanning", "object scanner", "photogrammetry", "digitizing objects", "turntable", "laser scanner", "model capture"])
def _(S):
    cube = poly([(9, 6.5), (13.5, 9), (13.5, 14), (9, 16.5), (4.5, 14), (4.5, 9)], closed=True, r=S.r * 0.5)
    return [shell(cube), detail(poly([(4.5, 9), (9, 11.5), (13.5, 9)])), detail(seg(9, 11.5, 9, 16.5)),
            shell(rect(2.5, 19, 13, 2.5, 1)), shell(rect(16.5, 3, 5, 4, min(S.R, 1.5))),
            line(seg(19, 9.5, 16.5, 12)), line(seg(19.5, 9.5, 16.5, 16.5))]


@icon("file-barcode", CAT, "Page with a folded corner and a block of vertical barcode bars in the middle",
      tags=["barcode file", "label data", "scan code", "product code", "inventory file", "upc", "bars"])
def _(S):
    return [*page(S), block(6.5, 10, 2, 9), block(10, 10, 1.5, 9), block(13, 10, 2.5, 9), block(16.25, 10, 1.25, 9)]


@icon("folder-mail", CAT, "Folder with a small closed envelope on its front",
      tags=["email folder", "inbox folder", "mail archive", "messages", "correspondence", "saved emails", "letters"])
def _(S):
    folder = [(3, 5), (9.5, 5), (11.5, 7.5), (21, 7.5), (21, 20), (3, 20)]
    return [shell(poly(folder, closed=True, r=S.r)), detail(rect(7.5, 11, 9, 6.5, 1)),
            detail(poly([(7.5, 11), (12, 14.5), (16.5, 11)]))]
