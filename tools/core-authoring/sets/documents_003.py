"""TypeIcon Core: documents (batch 003). Office papers, forms, cards and paper-handling tools."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt

CAT = "documents"

PAGE = [(5, 2.5), (14, 2.5), (19, 7.5), (19, 21.5), (5, 21.5)]
FOLD = [(14, 2.5), (14, 7.5), (19, 7.5)]


def page(S):
    """Document page with a folded corner."""
    return [shell(poly(PAGE, closed=True, r=S.r)), detail(poly(FOLD, r=S.r * 0.5))]


def sheet(S, x=5, y=2.5, w=14, h=19):
    return shell(rect(x, y, w, h, S.R))


def receipt_pts(x0=5, x1=19, top=2.5, bottom=21.5, n=4, depth=2):
    w = (x1 - x0) / n
    pts = [(x0, top), (x1, top), (x1, bottom - depth)]
    for i in range(n):
        pts.append((x1 - (i + 0.5) * w, bottom))
        if i < n - 1:
            pts.append((x1 - (i + 1) * w, bottom - depth))
    pts.append((x0, bottom - depth))
    return pts


def receipt(S, **kw):
    return shell(poly(receipt_pts(**kw), closed=True, r=S.r * 0.5))


def tri(pts):
    return Part("dot", poly(pts, closed=True))


# ============================================================================ chunk 1

@icon("folder-desktop", CAT, "Folder with a small computer monitor on its front",
      tags=["desktop folder", "computer files", "pc", "monitor", "workstation", "directory"])
def _(S):
    return [shell(poly([(2, 4.5), (9, 4.5), (11.5, 7.5), (22, 7.5), (22, 20.5), (2, 20.5)], closed=True, r=S.r)),
            detail(rect(8, 10.5, 8, 4, min(S.R, 2))), detail(seg(12, 14.5, 12, 17)), detail(seg(9.5, 17, 14.5, 17))]


@icon("all-in-one-printer", CAT, "Printer with a scanner lid raised on top and a page in the output tray",
      tags=["multifunction printer", "scanner", "copier", "office machine", "print", "scan"])
def _(S):
    return [shell(poly([(5, 9), (6.5, 3.5), (17.5, 3.5), (19, 9)], closed=True, r=S.r)),
            shell(rect(2.5, 9, 19, 8, S.R)),
            dot(17.5, 13, 1),
            detail(poly([(7, 17), (7, 21), (17, 21), (17, 17)], r=S.r * 0.5))]


@icon("library-book", CAT, "Upright book with a call number label on its cover and a spine band",
      tags=["library", "borrowed book", "call number", "catalogue", "lending", "shelf"])
def _(S):
    return [shell(rect(5, 2.5, 14, 19, S.R)),
            detail(seg(8.5, 3, 8.5, 21)),
            detail(seg(11.5, 7, 16, 7)),
            detail(rect(11, 14, 5, 4, 0.5 if S.name == "rounded" else 0))]


@icon("adoption-papers", CAT, "Page showing a tall and a short figure holding hands above a signature line",
      tags=["adoption", "custody", "family paperwork", "child", "legal form", "parent"])
def _(S):
    return [sheet(S, 4, 2.5, 16, 19),
            dot(8.5, 6.5, 1.5), detail(seg(8.5, 9, 8.5, 14)),
            dot(15.5, 9, 1.25), detail(seg(15.5, 11, 15.5, 14)),
            detail(seg(8.5, 10.5, 15.5, 12.25)),
            detail(seg(8, 18, 16, 18))]


@icon("mortgage-document", CAT, "Page with a small house and a percent sign at the top and text lines below",
      tags=["mortgage", "home loan", "house", "interest rate", "property", "deed"])
def _(S):
    return [sheet(S, 4, 2.5, 16, 19),
            detail(poly([(6.5, 10), (6.5, 7.5), (9, 5.5), (11.5, 7.5), (11.5, 10)], closed=True)),
            dot(14.5, 6, 1), dot(17.5, 9.5, 1), detail(seg(17.5, 5.5, 14.5, 10)),
            detail(seg(7, 14, 17, 14)), detail(seg(7, 18, 13, 18))]


@icon("donation-receipt", CAT, "Receipt slip with a zigzag bottom edge and a coin dropping into a cupped hand",
      tags=["donation", "charity", "gift aid", "tax receipt", "giving", "fundraising"])
def _(S):
    return [receipt(S),
            dot(12, 7.5, 2),
            detail("M7.5 12C9 15.5 15 15.5 16.5 12")]


@icon("jury-summons", CAT, "Envelope with an address window and a small gavel printed on its front",
      tags=["summons", "jury duty", "court", "gavel", "legal notice", "official letter"])
def _(S):
    head = [(19.68, 12.56), (17.56, 14.68), (13.32, 10.44), (15.44, 8.32)]
    return [shell(rect(2, 4.5, 20, 15, S.R)),
            detail(rect(5, 8, 6, 4.5, 0)),
            solid(poly(head, closed=True)),
            detail(seg(16.5, 11.5, 12.5, 15.5))]


@icon("rubric", CAT, "Page with a scoring table of four columns and criteria rows",
      tags=["rubric", "grading", "scoring", "marking scheme", "criteria", "assessment"])
def _(S):
    return [sheet(S, 4, 2.5, 16, 19),
            detail(seg(4, 9, 20, 9)), detail(seg(4, 15, 20, 15)),
            detail(seg(8, 9, 8, 21)), detail(seg(12, 9, 12, 21)), detail(seg(16, 9, 16, 21)),
            dot(6, 6, 1), dot(10, 6, 1), dot(14, 6, 1), dot(18, 6, 1)]


@icon("size-chart", CAT, "Shirt outline above a table with small, medium and large columns",
      tags=["size guide", "clothing sizes", "measurements", "small medium large", "fit", "apparel"])
def _(S):
    shirt = [(8.5, 2.5), (4, 5), (5.5, 8), (8, 7), (8, 10), (16, 10), (16, 7), (18.5, 8), (20, 5), (15.5, 2.5)]
    return [shell(poly(shirt, closed=True, r=S.r * 0.6)),
            sheet(S, 3, 13, 18, 8.5),
            detail(seg(9, 13, 9, 21.5)), detail(seg(15, 13, 15, 21.5)),
            dot(6, 17.25, 0.75), dot(12, 17.25, 1.0), dot(18, 17.25, 1.25)]


@icon("energy-label", CAT, "Tall label with stepped bars of increasing length and an arrow pointing at one",
      tags=["energy rating", "efficiency", "appliance label", "eco", "rating scale", "consumption"])
def _(S):
    return [shell(rect(3, 2.5, 14, 19, S.R)),
            detail(seg(6.5, 6.5, 8.5, 6.5)), detail(seg(6.5, 10.5, 10.5, 10.5)),
            detail(seg(6.5, 14.5, 12.5, 14.5)), detail(seg(6.5, 18.5, 14.5, 18.5)),
            tri([(19.5, 14.5), (22, 12), (22, 17)])]


@icon("gift-receipt", CAT, "Receipt slip with a zigzag bottom edge and a small ribbon bow at the top",
      tags=["gift", "present", "exchange", "return slip", "store receipt", "bow"])
def _(S):
    return [receipt(S),
            tri([(12, 7), (8, 4.8), (8, 9.2)]), tri([(12, 7), (16, 4.8), (16, 9.2)]),
            detail(seg(8, 13, 16, 13)), detail(seg(8, 16.5, 13, 16.5))]


@icon("inspection-tag", CAT, "Hanging tag with a string hole and a grid of month marks with one punched out",
      tags=["inspection", "certificate tag", "maintenance", "safety check", "service tag", "month punch"])
def _(S):
    pts = [(8, 2.5), (16, 2.5), (19, 6), (19, 21.5), (5, 21.5), (5, 6)]
    parts = [shell(poly(pts, closed=True, r=S.r)), dot(12, 5.5, 1.1)]
    for yy in (10.5, 14, 17.5):
        for xx in (8.5, 12, 15.5):
            if (xx, yy) != (15.5, 14):
                parts.append(dot(xx, yy, 1))
    return parts


@icon("microfilm-reel", CAT, "Open reel wound with film strip and a loose tail leaving it",
      tags=["microfilm", "microfiche", "archive", "film reel", "records", "library archive"])
def _(S):
    tail = "M16.2 13.5C16.6 17.5 18.5 19.5 21.5 19.5"
    return [shell(circle(10.5, 10.5, 8.5)),
            detail(circle(10.5, 10.5, 4.5)),
            dot(10.5, 10.5, 1.25),
            line(tail)]


@icon("document-workflow", CAT, "Three small pages in a row joined by arrows from left to right",
      tags=["workflow", "approval chain", "document flow", "process", "routing", "pipeline"])
def _(S):
    parts = []
    for x in (3, 10.25, 17.5):
        parts.append(shell(rect(x, 7.5, 3.5, 9, 0)))
    parts.append(tri([(7.9, 10.6), (7.9, 13.4), (9.3, 12)]))
    parts.append(tri([(15.15, 10.6), (15.15, 13.4), (16.55, 12)]))
    return parts


@icon("numbering-stamp", CAT, "Hand stamp with a knob on top and a row of rotating number wheels above the base",
      tags=["numbering machine", "number stamp", "bates", "sequence", "rubber stamp", "counter"])
def _(S):
    return [shell(poly([(9, 7), (10, 2.5), (14, 2.5), (15, 7)], closed=True, r=S.r * 0.6)),
            shell(rect(5, 8, 14, 6, min(S.R, 2))),
            detail(seg(9.67, 8, 9.67, 14)), detail(seg(14.33, 8, 14.33, 14)),
            shell(rect(3, 17, 18, 4, min(S.R, 2)))]


# ============================================================================ chunk 2

@icon("paper-drill", CAT, "Press with a hollow drill bit lowered over a stack of paper on its base",
      tags=["paper drill", "hole punch press", "bookbinding", "print shop", "drilling", "stack of paper"])
def _(S):
    return [line(poly([(3, 21), (21, 21), (21, 3.5), (9, 3.5)], r=S.r)),
            line(seg(9, 4.5, 9, 7.5)),
            line(poly([(6.5, 13), (6.5, 7.5), (11.5, 7.5), (11.5, 13)], r=S.r * 0.4)),
            shell(rect(3.5, 15.5, 12, 3, 0))]


@icon("corner-rounder", CAT, "Card with one rounded corner and the small square-cornered offcut flying away",
      tags=["corner punch", "round corner", "card cutter", "craft punch", "trim", "scrapbooking"])
def _(S):
    chip = "M13.5 4.5H19.5V10.5A6 6 0 0 0 13.5 4.5Z"
    return [shell("M3 8H10A6 6 0 0 1 16 14V21H3Z" if S.name == "rounded" else "M3 8H10A6 6 0 0 1 16 14V21H3Z"),
            solid(chip)]


@icon("index-card-ring", CAT, "Stack of index cards held together by a metal ring through a punched corner hole",
      tags=["flash cards", "index cards", "study cards", "binder ring", "note cards", "revision"])
def _(S):
    return [line("M6 8V5H21V16H18"),
            shell(rect(3, 8, 15, 12, S.R)),
            detail(circle(6.5, 11.5, 1.6)),
            detail(seg(10.5, 12, 14.5, 12)), detail(seg(10.5, 16, 14, 16))]


@icon("dieline", CAT, "Flat unfolded box net with a row of panels, top and bottom flaps and dashed fold lines",
      tags=["die cut", "packaging template", "box net", "unfolded box", "fold lines", "printing"])
def _(S):
    pts = [(7.5, 4), (12, 4), (12, 9), (21, 9), (21, 15), (12, 15), (12, 20), (7.5, 20), (7.5, 15), (3, 15), (3, 9), (7.5, 9)]
    parts = [shell(poly(pts, closed=True, r=S.r * 0.5))]
    for x in (7.5, 12, 16.5):
        parts += [detail(seg(x, 10, x, 11.5)), detail(seg(x, 12.5, x, 14))]
    return parts


@icon("manicule", CAT, "Printer's pointing hand with an extended index finger and a small cuff",
      tags=["pointing hand", "index finger", "printers mark", "fist", "point right", "typography"])
def _(S):
    hand = [(7, 10), (9, 10), (10, 7), (12.5, 7), (13, 10), (20, 10), (21.5, 11.5), (20, 13), (15, 13),
            (15.5, 16), (14, 19), (7, 19)]
    return [line(poly([(3.5, 9), (3.5, 20)], r=0)),
            shell(poly(hand, closed=True, r=S.r)),
            detail(seg(11, 15, 13.5, 15))]


@icon("pay-envelope", CAT, "Small envelope with a window showing a banknote and a line for a name",
      tags=["pay packet", "wages", "salary envelope", "cash pay", "payroll", "banknote window"])
def _(S):
    return [shell(rect(2, 4.5, 20, 15, S.R)),
            detail(rect(5, 7.5, 10, 5.5, 0)), dot(10, 10.25, 1.3),
            detail(seg(5, 16.5, 12, 16.5)), detail(seg(18, 9, 18, 13))]


@icon("galley-proof", CAT, "Narrow strip of typeset lines with small correction marks in the margins",
      tags=["proofreading", "proof", "typesetting", "editing marks", "printer proof", "copyedit"])
def _(S):
    return [shell(rect(8, 2.5, 9, 19, S.R)),
            detail(seg(10.5, 7, 14.5, 7)), detail(seg(10.5, 11, 14.5, 11)), detail(seg(10.5, 15, 13.5, 15)),
            line(poly([(2.5, 11.5), (4, 8.5), (5.5, 11.5)], r=0)),
            line(seg(19.5, 7, 22, 7)), line(seg(19.5, 15, 22, 15))]


@icon("thumbprint-signature", CAT, "Page with a text line and a thumbprint whorl above the signature line",
      tags=["thumbprint", "fingerprint signature", "sign", "notary", "witness", "legal page"])
def _(S):
    return [sheet(S, 5, 2.5, 14, 19),
            detail(seg(8, 5.5, 16, 5.5)),
            detail(arc(12, 12.25, 3.75, 120, 420)), dot(12, 12.25, 1.2),
            detail(seg(8, 19, 16, 19))]


@icon("file-layers", CAT, "Page with a folded corner and three stacked diamond layers in the middle",
      tags=["layers", "stack", "file layers", "pdf layers", "levels", "versions"])
def _(S):
    pts = [(5, 2.5), (15, 2.5), (19, 6.5), (19, 21.5), (5, 21.5)]
    fold = [(15, 2.5), (15, 6.5), (19, 6.5)]
    return [shell(poly(pts, closed=True, r=S.r)), detail(poly(fold, r=S.r * 0.5)),
            detail(poly([(12, 8), (16.5, 10), (12, 12), (7.5, 10)], closed=True)),
            detail(poly([(7.5, 13), (12, 15), (16.5, 13)])),
            detail(poly([(7.5, 16), (12, 18), (16.5, 16)]))]


@icon("meal-planner", CAT, "Page with a plate, fork and knife above three rows of planned meals",
      tags=["meal plan", "menu planner", "weekly menu", "diet plan", "food schedule", "dinner"])
def _(S):
    return [sheet(S, 3, 2.5, 18, 19),
            detail(circle(12, 6.5, 1.5)), detail(seg(7, 4.5, 7, 8.5)), detail(seg(17, 4.5, 17, 8.5)),
            dot(7, 12, 1), detail(seg(10.5, 12, 17, 12)),
            dot(7, 15.5, 1), detail(seg(10.5, 15.5, 17, 15.5)),
            dot(7, 19, 1), detail(seg(10.5, 19, 15, 19))]


@icon("thesaurus", CAT, "Book with two arrows pointing in opposite directions on its cover",
      tags=["synonyms", "antonyms", "word finder", "dictionary", "vocabulary", "similar words"])
def _(S):
    return [shell(rect(5, 2.5, 14, 19, S.R)),
            detail(seg(8.5, 3, 8.5, 21)),
            detail(seg(11.5, 9, 16.5, 9)), detail(poly([(14.5, 7), (16.5, 9), (14.5, 11)])),
            detail(seg(11.5, 15, 16.5, 15)), detail(poly([(13.5, 13), (11.5, 15), (13.5, 17)]))]


@icon("folder-public", CAT, "Folder with a small globe on its front",
      tags=["public folder", "shared folder", "world", "open access", "web folder", "globe"])
def _(S):
    return [shell(poly([(2, 4), (9, 4), (11.5, 7), (22, 7), (22, 21), (2, 21)], closed=True, r=S.r)),
            detail(circle(12, 14, 4)), detail(ellipse(12, 14, 1.8, 4)), detail(seg(8, 14, 16, 14))]


@icon("first-day-cover", CAT, "Envelope with a postage stamp and a round commemorative postmark overlapping it",
      tags=["philately", "stamp collecting", "postmark", "commemorative", "postage", "collector"])
def _(S):
    return [shell(rect(2, 4, 20, 16, S.R)),
            detail(rect(15, 7, 4, 5.5, 0)),
            detail(circle(13, 11, 2.75)),
            detail(seg(5, 9.5, 8, 9.5)), detail(seg(5, 12.5, 8, 12.5)),
            detail(seg(5, 17, 13, 17))]


@icon("research-poster", CAT, "Wide poster with a title bar and three columns holding a chart, bars and text",
      tags=["scientific poster", "conference poster", "academic", "presentation board", "findings", "symposium"])
def _(S):
    return [shell(rect(2, 4, 20, 16, S.R)),
            detail(seg(5.5, 8, 18.5, 8)),
            dot(6.5, 14.5, 1.5),
            detail(seg(10.5, 17, 10.5, 14)), detail(seg(13.5, 17, 13.5, 12)),
            detail(seg(16.5, 12.5, 19, 12.5)), detail(seg(16.5, 16, 19, 16))]


# ============================================================================ chunk 3

@icon("tabbed-notebook", CAT, "Closed notebook with a row of stepped divider tabs sticking out of its right edge",
      tags=["dividers", "binder", "index tabs", "organiser", "sections", "notebook tabs"])
def _(S):
    return [shell(rect(3, 2.5, 14, 19, S.R)),
            detail(seg(6.5, 3, 6.5, 21)),
            detail(seg(10, 8, 14, 8)),
            line(seg(17, 5.5, 21.5, 5.5)), line(seg(17, 10.5, 21.5, 10.5)), line(seg(17, 15.5, 21.5, 15.5))]


@icon("aperture-card", CAT, "Card with a rectangular film window on one side and columns of punched holes on the other",
      tags=["microfilm card", "engineering drawing", "punch card", "archive card", "film window", "records"])
def _(S):
    parts = [shell(rect(2.5, 5, 19, 14, S.R)), detail(rect(6, 8, 5.5, 8, 0))]
    for x in (15, 18):
        for y in (9, 12, 15):
            parts.append(dot(x, y, 0.85))
    return parts


@icon("embossing-label-maker", CAT, "Handheld label tool with a round letter dial on top and a strip of tape coming out",
      tags=["label maker", "embosser", "tape labeller", "labeler", "raised letters", "dymo style"])
def _(S):
    return [shell(circle(9, 6.5, 4)), dot(9, 6.5, 1),
            shell(rect(2.5, 13, 13.5, 8, S.R)),
            line(poly([(16, 15), (22, 15), (22, 19), (16, 19)], r=0)),
            dot(18, 17, 0.7), dot(20.5, 17, 0.7)]


@icon("handwriting-recognition", CAT, "Handwritten squiggle on the left, an arrow, and neat typed text lines on the right",
      tags=["handwriting", "ocr", "ink to text", "convert handwriting", "scan text", "digitise notes"])
def _(S):
    return [line("M2 13C3 8 4.5 8 5.3 12.5S7 16.5 8.3 10.5"),
            line(seg(10, 12, 14.5, 12)), line(poly([(12.5, 10), (14.5, 12), (12.5, 14)], r=S.r * 0.5)),
            line(seg(17, 7, 22, 7)), line(seg(17, 12, 22, 12)), line(seg(17, 17, 21, 17))]


@icon("organ-donor-card", CAT, "Wallet card with a heart beside a plus sign above a signature line",
      tags=["organ donation", "donor", "donate", "heart card", "transplant", "consent card"])
def _(S):
    heart = "M8.5 13.5C4.5 11 4.5 7 6.8 7C8 7 8.5 8 8.5 8.6C8.5 8 9 7 10.2 7C12.5 7 12.5 11 8.5 13.5Z"
    return [shell(rect(2, 5, 20, 14, S.R)),
            detail(heart),
            detail(seg(17, 7.5, 17, 11.5)), detail(seg(15, 9.5, 19, 9.5)),
            detail(seg(5, 16, 19, 16))]


@icon("ration-book", CAT, "Open booklet with a grid of perforated tear-out stamps on each page",
      tags=["ration coupons", "food stamps", "voucher book", "coupons", "wartime", "tear-off tickets"])
def _(S):
    return [shell(rect(2, 5, 20, 14, S.R)),
            detail(seg(12, 5, 12, 19)),
            detail(seg(7.5, 6, 7.5, 8)), detail(seg(7.5, 10, 7.5, 14)), detail(seg(7.5, 16, 7.5, 18)),
            detail(seg(4, 12, 6.5, 12)), detail(seg(8.5, 12, 10.5, 12)),
            detail(seg(17.5, 6, 17.5, 8)), detail(seg(17.5, 10, 17.5, 14)), detail(seg(17.5, 16, 17.5, 18)),
            detail(seg(14, 12, 16.5, 12)), detail(seg(18.5, 12, 20.5, 12))]


@icon("ostracon", CAT, "Irregular pottery shard with short scratched lines of writing",
      tags=["pottery shard", "potsherd", "ancient writing", "archaeology", "clay fragment", "inscription"])
def _(S):
    pts = [(3.5, 9), (8, 3.5), (17, 4), (20.5, 10), (17.5, 14.5), (18.5, 19), (10, 20.5), (4, 16)]
    return [shell(poly(pts, closed=True, r=S.r)),
            detail(seg(8, 9, 14, 8.5)), detail(seg(8, 12.5, 15.5, 12.5)), detail(seg(9, 16, 13, 16))]


@icon("label-roll", CAT, "Roll of labels on a backing strip running to the right with one label peeling at its corner",
      tags=["sticker roll", "label tape", "blank labels", "shipping labels", "peel", "adhesive labels"])
def _(S):
    label = [(13, 9.5), (17, 9.5), (19.5, 12), (19.5, 14.5), (13, 14.5)]
    return [shell(circle(8, 12, 6)), dot(8, 12, 1.5),
            line(seg(8, 6, 22, 6)), line(seg(8, 18, 22, 18)),
            shell(poly(label, closed=True, r=S.r * 0.4))]


@icon("file-package", CAT, "Page with a folded corner and a small closed box with a tape line in the middle",
      tags=["package", "bundle", "archive", "zip", "attachment box", "parcel"])
def _(S):
    return [*page(S),
            detail(rect(7.5, 11, 9, 7, 0)), detail(seg(12, 11, 12, 14.5))]


@icon("appointment-card", CAT, "Small card with a calendar tile on the left and two short lines for date and time",
      tags=["appointment", "reminder card", "booking", "schedule", "date and time", "visit card"])
def _(S):
    return [shell(rect(2, 5, 20, 14, S.R)),
            detail(rect(5.5, 8.5, 6, 6.5, 0)), detail(seg(5.5, 11.5, 11.5, 11.5)),
            detail(seg(15, 9.5, 19.5, 9.5)), detail(seg(15, 14, 18, 14))]


@icon("fore-edge-painting", CAT, "Closed book seen from its page edge with a small landscape painted on the pages",
      tags=["book edge", "hidden painting", "antique book", "rare book", "page edge art", "bookbinding"])
def _(S):
    return [shell(rect(3, 4, 18, 16, S.R)),
            detail(seg(3, 7, 21, 7)), detail(seg(3, 17, 21, 17)),
            detail(poly([(6, 14.5), (10, 10.5), (13, 13.5), (15, 12), (18, 14.5)])),
            dot(17, 10, 1)]


@icon("compliment-slip", CAT, "Short wide slip with a letterhead band at the top and one handwritten line below",
      tags=["with compliments", "note slip", "letterhead", "office stationery", "memo slip", "business note"])
def _(S):
    return [shell(rect(2, 6, 20, 12, S.R)),
            detail(seg(2, 10, 22, 10)),
            detail("M6 15C8 12.5 9 12.5 10 15S12 17.5 14 15S16 12.5 18 15")]
