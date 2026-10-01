"""TypeIcon Core: documents, batch 001 (file types, folders, forms, certificates and special books)."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d

CAT = "documents"

PAGE = [(5, 2.5), (14, 2.5), (19, 7.5), (19, 21.5), (5, 21.5)]
FOLD = [(14, 2.5), (14, 7.5), (19, 7.5)]
SHEET = (5, 2.5, 14, 19)


def page(S):
    """The shared document silhouette with its folded corner."""
    return [shell(poly(PAGE, closed=True, r=S.r)), detail(poly(FOLD, r=S.r * 0.5))]


def sheet(S):
    return shell(rect(*SHEET, S.R))


def block(x, y, w, h):
    """Solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h))


def tri(pts):
    return Part("dot", poly(pts, closed=True))


def tag(S):
    """Type label across the lower part of a file page."""
    return block(7.5, 17, 9, 2.5)


# ============================================================================ file types

@icon("file-exe", CAT, "Page with a folded corner, a command prompt mark and a type label at the bottom",
      tags=["exe", "executable", "program", "application", "installer", "binary", "windows"])
def _(S):
    return [*page(S), detail(poly([(8.5, 9.5), (11, 11.75), (8.5, 14)], r=S.r * 0.5)), detail(seg(13, 14, 16, 14)), tag(S)]


@icon("file-ebook", CAT, "Page with a folded corner and a small open book in the middle",
      tags=["ebook", "epub", "digital book", "reading", "mobi", "kindle", "e-book"])
def _(S):
    return [*page(S), detail(poly([(8, 10), (8, 17.5), (12, 19), (16, 17.5), (16, 10), (12, 11.5)], closed=True, r=S.r * 0.4))]


@icon("file-gif", CAT, "Page with a folded corner, a looping arrow and a type label at the bottom",
      tags=["gif", "animated", "animation", "loop", "image", "meme"])
def _(S):
    return [*page(S), detail(arc(12, 12.75, 2.75, 30, 300)), tri([(15.3, 11.5), (12.6, 11.8), (14.2, 9)]), tag(S)]


@icon("file-png", CAT, "Page with a folded corner, a checkered transparency grid and a type label at the bottom",
      tags=["png", "transparent", "image", "graphic", "transparency", "raster"])
def _(S):
    return [*page(S), block(8, 9.25, 3.25, 3.25), block(11.25, 12.5, 3.25, 3.25), tag(S)]


@icon("file-jpg", CAT, "Page with a folded corner, a small mountain and sun picture and a type label at the bottom",
      tags=["jpg", "jpeg", "photo", "picture", "image", "photograph"])
def _(S):
    return [*page(S), dot(15, 10.75, 1.25), detail(poly([(8, 14.5), (10.75, 11), (13.5, 14.5)], r=S.r * 0.5)), tag(S)]


@icon("file-tiff", CAT, "Page with a folded corner, two stacked image layers and a type label at the bottom",
      tags=["tiff", "tif", "layers", "scan", "image", "print"])
def _(S):
    return [*page(S), tri([(12, 8.75), (16.25, 10.5), (12, 12.25), (7.75, 10.5)]),
            detail(poly([(8.5, 13), (12, 14.75), (15.5, 13)], r=S.r * 0.5)), tag(S)]


@icon("file-raw", CAT, "Page with a folded corner, a camera lens aperture and a type label at the bottom",
      tags=["raw", "camera raw", "photo", "lens", "aperture", "uncompressed", "dng"])
def _(S):
    hexa = [(12 + 1.7 * math.cos(math.radians(60 * i)), 12.5 + 1.7 * math.sin(math.radians(60 * i))) for i in range(6)]
    return [*page(S), detail(circle(12, 12.5, 3.75)), tri(hexa), tag(S)]


@icon("file-mp3", CAT, "Page with a folded corner, a music note and a type label at the bottom",
      tags=["mp3", "music", "song", "audio", "track", "sound"])
def _(S):
    return [*page(S), dot(10.25, 13.5, 1.75), detail(poly([(12, 13.5), (12, 9), (15, 10.75)], r=S.r * 0.5)), tag(S)]


@icon("file-mp4", CAT, "Page with a folded corner, a small play frame and a type label at the bottom",
      tags=["mp4", "movie", "video", "film", "clip", "media"])
def _(S):
    return [*page(S), detail(rect(7.5, 9, 9, 6.5, min(S.R, 1.5))), tri([(11, 10.75), (14, 12.25), (11, 13.75)]), tag(S)]


@icon("file-wav", CAT, "Page with a folded corner, a short sound waveform and a type label at the bottom",
      tags=["wav", "waveform", "sound", "audio", "recording", "uncompressed"])
def _(S):
    return [*page(S), detail(seg(8.5, 11.5, 8.5, 13.5)), detail(seg(11.5, 9.5, 11.5, 15.5)),
            detail(seg(14.5, 10.5, 14.5, 14.5)), tag(S)]


@icon("file-midi", CAT, "Page with a folded corner and a small strip of piano keys",
      tags=["midi", "piano", "keyboard", "music", "notes", "synth", "sequence"])
def _(S):
    return [*page(S), detail(rect(7.5, 10.5, 9, 8, min(S.R, 1))), block(9.25, 10.5, 2, 4.5), block(12.75, 10.5, 2, 4.5)]


@icon("file-calendar", CAT, "Page with a folded corner and a small calendar with two binding tabs",
      tags=["calendar", "ics", "schedule", "events", "dates", "agenda"])
def _(S):
    return [*page(S), detail(rect(7.5, 10.5, 9, 8, min(S.R, 1))), block(7.5, 10.5, 9, 3.5), block(9, 9, 1.5, 2), block(12.5, 9, 1.5, 2)]


@icon("file-disc-image", CAT, "Page with a folded corner and a disc with a centre hole",
      tags=["iso", "disc image", "cd", "dvd", "optical disc", "burn", "dmg"])
def _(S):
    return [*page(S), detail(circle(12, 14, 4.5)), dot(12, 14, 1.25)]


@icon("file-cad", CAT, "Page with a folded corner and a drafting crosshair with a square pick box",
      tags=["cad", "drafting", "dwg", "crosshair", "technical drawing", "design"])
def _(S):
    return [*page(S), detail(poly([(8.5, 9.5), (8.5, 18), (16, 18)], closed=True, r=S.r * 0.5)), dot(10.5, 16, 0.9)]


@icon("file-map", CAT, "Page with a folded corner, a zigzag route and a location pin",
      tags=["map", "gps", "gpx", "route", "location", "kml", "navigation"])
def _(S):
    pin = "M14 17.5C14 17.5 11.25 15 11.25 12.75A2.75 2.75 0 0 1 16.75 12.75C16.75 15 14 17.5 14 17.5Z"
    return [*page(S), detail(pin), dot(14, 12.75, 1), detail(poly([(7.5, 10), (8.75, 13), (7.5, 15.5), (9.5, 18.5)], r=S.r * 0.5))]


@icon("file-subtitles", CAT, "Page with a folded corner and two short caption bars stacked near the bottom",
      tags=["subtitles", "captions", "srt", "vtt", "closed captions", "transcript", "video text"])
def _(S):
    return [*page(S), block(7.5, 12.5, 9, 2.25), block(9.5, 16.25, 5, 2.25)]


@icon("file-key", CAT, "Page with a folded corner and a small key lying diagonally across it",
      tags=["key", "encrypted", "certificate", "pem", "private key", "credentials", "security"])
def _(S):
    return [*page(S), detail(circle(10, 12, 2.25)), detail(seg(11.6, 13.6, 16, 18)), detail(seg(14, 16, 15.75, 14.25))]


@icon("file-email", CAT, "Page with a folded corner and a small closed envelope in the middle",
      tags=["email", "eml", "message", "mail", "envelope", "msg", "saved email"])
def _(S):
    return [*page(S), detail(rect(7.5, 10.5, 9, 8, min(S.R, 1))), detail(poly([(7.5, 10.5), (12, 14.5), (16.5, 10.5)], r=S.r * 0.5))]


@icon("file-shortcut", CAT, "Page with a folded corner and a curved arrow pointing out at the lower left",
      tags=["shortcut", "link", "alias", "symlink", "pointer", "lnk", "reference"])
def _(S):
    return [*page(S), detail("M8 19V16.5A3 3 0 0 1 11 13.5H14"), tri([(14, 11.25), (17.5, 13.5), (14, 15.75)])]


def _corrupt(S):
    top = [(5, 2.5), (14, 2.5), (19, 7.5), (19, 11), (15.5, 9), (12, 12), (8.5, 9.5), (5, 11.5)]
    bot = [(5, 16), (8.5, 14), (12, 16.5), (15.5, 13.5), (19, 15.5), (19, 21.5), (5, 21.5)]
    return [shell(poly(top, closed=True, r=S.r * 0.4)), detail(poly(FOLD, r=S.r * 0.5)), shell(poly(bot, closed=True, r=S.r * 0.4))]


@icon("file-corrupted", CAT, "Page broken into two offset halves along a jagged tear",
      tags=["corrupted", "broken", "damaged", "error", "unreadable", "torn", "bad file"], aliases=["file-broken"])
def _(S):
    return _corrupt(S)


@icon("file-template", CAT, "Page with a folded corner, a title block and dashed placeholder lines",
      tags=["template", "placeholder", "blank form", "layout", "boilerplate", "starter", "skeleton"])
def _(S):
    return [*page(S), block(8, 9, 4, 2), detail(seg(8.25, 14, 10.5, 14)), detail(seg(13, 14, 15.75, 14)),
            detail(seg(8.25, 17.5, 10.5, 17.5)), detail(seg(13, 17.5, 15.75, 17.5))]


def _mini(S, x, y, w, h):
    f = 2.0
    return poly([(x, y), (x + w - f, y), (x + w, y + f), (x + w, y + h), (x, y + h)], closed=True, r=S.r * 0.5)


@icon("file-merge", CAT, "Two small pages at the top with lines converging into one larger page below",
      tags=["merge", "combine", "join", "consolidate", "pdf merge", "unite", "concatenate"])
def _(S):
    return [shell(_mini(S, 3, 2.5, 6, 6)), shell(_mini(S, 15, 2.5, 6, 6)),
            line(poly([(6, 8.5), (6, 11.5), (12, 14)], r=S.r)), line(poly([(18, 8.5), (18, 11.5), (12, 14)], r=S.r)),
            line(seg(12, 14, 12, 16.5)), shell(_mini(S, 7, 16.5, 10, 5))]


@icon("file-split", CAT, "One page at the top with lines diverging into two smaller pages below",
      tags=["split", "divide", "separate", "extract", "break apart", "pdf split", "burst"])
def _(S):
    return [shell(_mini(S, 7, 2.5, 10, 5)), line(seg(12, 7.5, 12, 10)),
            line(poly([(6, 15.5), (6, 12.5), (12, 10)], r=S.r)), line(poly([(18, 15.5), (18, 12.5), (12, 10)], r=S.r)),
            shell(_mini(S, 3, 15.5, 6, 6)), shell(_mini(S, 15, 15.5, 6, 6))]


@icon("file-convert", CAT, "Two pages side by side above a double-headed arrow; a format conversion",
      tags=["convert", "conversion", "transform", "exchange", "format change", "transcode", "swap"])
def _(S):
    left = [(3, 3.5), (7, 3.5), (9.5, 6), (9.5, 14.5), (3, 14.5)]
    right = [(14.5, 3.5), (18.5, 3.5), (21, 6), (21, 14.5), (14.5, 14.5)]
    return [shell(poly(left, closed=True, r=S.r * 0.5)), shell(poly(right, closed=True, r=S.r * 0.5)),
            line(seg(6.5, 19, 17.5, 19)), tri([(3.5, 19), (7.5, 16.75), (7.5, 21.25)]), tri([(20.5, 19), (16.5, 16.75), (16.5, 21.25)])]


@icon("file-rename", CAT, "Page with a folded corner and a text field at the bottom holding a text cursor",
      tags=["rename", "edit name", "file name", "text field", "cursor", "relabel", "change name"])
def _(S):
    return [*page(S), detail(seg(8.5, 9.5, 11.5, 9.5)), detail(rect(7.5, 13.5, 9, 5.5, min(S.R, 1))), block(8.75, 16.25, 2.5, 1.5), block(13.25, 14.75, 1.25, 3)]


@icon("file-diagram", CAT, "Page with a folded corner and three small boxes joined by connector lines",
      tags=["diagram", "flowchart", "org chart", "chart", "structure", "tree", "workflow"])
def _(S):
    return [*page(S), block(10, 9, 4, 3), detail("M12 12V14M9.25 15.5V14H14.75V15.5"), block(7.5, 15.5, 3.5, 3), block(13, 15.5, 3.5, 3)]


@icon("file-cloud", CAT, "Page with a folded corner and a small cloud outline in the middle",
      tags=["cloud", "online", "remote", "synced", "cloud storage", "backup", "upload"])
def _(S):
    return [*page(S), detail("M9.5 17.5A2.5 2.5 0 0 1 9.15 12.6A3.4 3.4 0 0 1 15.3 12A2.75 2.75 0 0 1 15 17.5Z")]


def dashes(pts, dash, gap, closed=False):
    """Dashes along straight edges: each edge gets whole dashes that start and end on its corners."""
    out = []
    pts = list(pts) + ([pts[0]] if closed else [])
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        L = math.hypot(x2 - x1, y2 - y1)
        n = max(1, round((L + gap) / (dash + gap)))
        d = dash if n > 1 else L
        g = (L - n * d) / (n - 1) if n > 1 else 0
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        for i in range(n):
            a = i * (d + g)
            out.append(seg(x1 + ux * a, y1 + uy * a, x1 + ux * (a + d), y1 + uy * (a + d)))
    return "".join(out)


@icon("draft-document", CAT, "Page drawn with a dashed outline and folded corner, with faint dashed text lines",
      tags=["draft", "unsaved", "work in progress", "unpublished", "document", "wip", "placeholder"])
def _(S):
    dd = 3.0 if S.name == "line" else 2.0
    gg = 2.0 if S.name == "line" else 3.0
    return [line(dashes(PAGE, dd, gg, closed=True)), line(dashes([(9, 11.5), (15, 11.5)], 2.0, 2.0)),
            line(dashes([(9, 15.5), (15, 15.5)], 2.0, 2.0))]


# ============================================================================ folders

FOLDER = [(3, 5), (9.5, 5), (11.5, 7.5), (21, 7.5), (21, 20), (3, 20)]


def folder(S):
    return shell(poly(FOLDER, closed=True, r=S.r))


@icon("folder-image", CAT, "Folder with a small mountain and sun picture on its front",
      tags=["images", "pictures", "photos", "gallery", "album", "media folder", "camera roll"])
def _(S):
    return [folder(S), dot(16.5, 12, 1.25), detail(poly([(6.5, 17.5), (10, 13), (13, 16.5), (14.5, 15), (17.5, 17.5)], r=S.r))]


@icon("folder-music", CAT, "Folder with a single music note on its front",
      tags=["music", "songs", "audio", "playlist", "albums", "tracks", "media folder"])
def _(S):
    return [folder(S), dot(10.5, 16.5, 2), detail(poly([(12, 16.5), (12, 10.75), (16, 12.5)], r=S.r * 0.5))]


@icon("folder-video", CAT, "Folder with a small film frame and play triangle on its front",
      tags=["videos", "movies", "clips", "footage", "film", "media folder", "recordings"])
def _(S):
    return [folder(S), detail(rect(7, 11.25, 10, 6.5, min(S.R, 1.5))), tri([(11, 12.5), (14, 14.5), (11, 16.5)])]


@icon("folder-document", CAT, "Folder with a lined page sticking up out of its top edge",
      tags=["documents", "papers", "files", "paperwork", "docs folder", "contents", "records"])
def _(S):
    return [shell(poly([(3, 20), (3, 11.5), (21, 11.5), (21, 20)], closed=True, r=S.r)),
            line(poly([(6.5, 11.5), (6.5, 3.5), (17.5, 3.5), (17.5, 11.5)], r=S.r)), detail(seg(9.5, 7.5, 14.5, 7.5))]


@icon("folder-cloud", CAT, "Folder with a small cloud outline on its front",
      tags=["cloud", "online folder", "sync", "remote", "cloud storage", "backup", "shared drive"])
def _(S):
    return [folder(S), detail("M9.5 17.5A2.5 2.5 0 0 1 9.15 12.6A3.4 3.4 0 0 1 15.3 12A2.75 2.75 0 0 1 15 17.5Z")]


@icon("folder-home", CAT, "Folder with a small house outline on its front",
      tags=["home", "home folder", "user folder", "personal", "house", "default", "main directory"])
def _(S):
    return [folder(S), detail(poly([(12, 10.5), (16.5, 14), (16.5, 17), (7.5, 17), (7.5, 14)], closed=True, r=S.r * 0.5))]


@icon("folder-network", CAT, "Folder above a short stem that ends in a bar with three node dots",
      tags=["network", "network drive", "shared folder", "server", "nas", "mapped drive", "lan"])
def _(S):
    return [shell(mini_folder(6.5, 2.5, 11, 7, S)), line(seg(12, 9.5, 12, 14)),
            line(poly([(5.5, 17), (5.5, 14), (18.5, 14), (18.5, 17)], r=S.r)), line(seg(12, 14, 12, 17)),
            dot(5.5, 19.5, 1.75), dot(12, 19.5, 1.75), dot(18.5, 19.5, 1.75)]


def mini_folder(x, y, w, h, S, tab=3.5):
    return poly([(x, y), (x + tab, y), (x + tab + 1.5, y + 1.5), (x + w, y + 1.5), (x + w, y + h), (x, y + h)], closed=True, r=S.r * 0.66)


# ============================================================================ office paper

@icon("lever-arch-file", CAT, "Tall box file seen from the spine with a label window and a round finger hole",
      tags=["lever arch", "box file", "binder", "archive file", "ring binder", "office", "filing"])
def _(S):
    return [shell(rect(5.5, 2.5, 13, 19, S.R)), detail(rect(8.5, 5.25, 7, 3.75, min(S.R, 1))), dot(12, 16, 2.25)]


def star_pts(cx, cy, ro, ri, n=5):
    return [(cx + (ro if i % 2 == 0 else ri) * math.cos(math.radians(-90 + i * 180 / n)),
             cy + (ro if i % 2 == 0 else ri) * math.sin(math.radians(-90 + i * 180 / n))) for i in range(2 * n)]


@icon("classified-document", CAT, "Page with a folded corner, a bold star at the top and a diagonal stamped band",
      tags=["classified", "confidential", "secret", "restricted", "top secret", "stamped", "sensitive"])
def _(S):
    return [*page(S), tri(star_pts(10.25, 10, 2.75, 1.2)), tri([(6.5, 19), (6.5, 16.5), (17.5, 13), (17.5, 15.5)])]


@icon("paper-tray", CAT, "Printer paper tray front with a finger pull slot and a stack of sheets above it",
      tags=["paper tray", "printer tray", "paper feed", "in tray", "stack of paper", "sheets", "office"])
def _(S):
    return [shell(rect(2.5, 13, 19, 8, S.R)), block(9.5, 16.25, 5, 1.75),
            line(poly([(4.5, 13), (4.5, 9.5), (19.5, 9.5), (19.5, 13)], r=S.r)),
            line(poly([(7, 9.5), (7, 5.5), (17, 5.5), (17, 9.5)], r=S.r))]


@icon("permission-slip", CAT, "Half page with a tear-off line across the middle and a signature line below",
      tags=["permission slip", "consent form", "school trip", "tear off", "signature", "parent form", "reply slip"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 19, S.R)), detail(seg(8, 6.5, 16, 6.5)), detail(seg(8, 9.5, 13, 9.5)),
            detail(dashes([(7.5, 13), (16.5, 13)], 2, 2)), detail(seg(8, 18, 16, 18))]


@icon("deposit-slip", CAT, "Short wide slip with dotted amount fields on the right and a coin on the left",
      tags=["deposit slip", "bank slip", "paying in", "bank form", "cash deposit", "banking", "teller"])
def _(S):
    return [shell(rect(2.5, 6.5, 19, 11, S.R)), detail(ellipse(8, 10.5, 2.75, 1.25)),
            detail("M5.25 10.5V13.5C5.25 14.3 6.5 14.9 8 14.9C9.5 14.9 10.75 14.3 10.75 13.5V10.5"),
            detail(dashes([(13, 10), (18.5, 10)], 2, 1.5)), detail(dashes([(13, 14), (18.5, 14)], 2, 1.5))]


@icon("attendance-sheet", CAT, "Page with a grid of rows and columns holding ticks and crosses",
      tags=["attendance", "roll call", "register", "present absent", "class list", "sign in sheet", "roster"])
def _(S):
    return [sheet(S), detail(seg(4.5, 9, 19.5, 9)), detail(seg(4.5, 15, 19.5, 15)), detail(seg(10.5, 2.5, 10.5, 21.5)),
            detail(poly([(13, 6), (14.25, 7.25), (16.5, 4.75)], r=S.r * 0.3)),
            detail(seg(13, 10.75, 16, 13.25)), detail(seg(16, 10.75, 13, 13.25)),
            detail(poly([(13, 18.25), (14.25, 19.5), (16.5, 17)], r=S.r * 0.3))]


@icon("insurance-policy", CAT, "Page with a folded corner and an open umbrella above a hooked handle",
      tags=["insurance", "policy", "coverage", "protection", "cover note", "umbrella", "assurance"])
def _(S):
    return [*page(S), detail("M7.75 13.5A4.25 4.25 0 0 1 16.25 13.5Z"), detail("M12 13.5V17.5A1.25 1.25 0 0 1 9.5 17.5")]


@icon("bank-statement", CAT, "Page headed by a small columned bank with two columns of figures below",
      tags=["bank statement", "account statement", "transactions", "balance", "banking", "finance", "ledger"])
def _(S):
    return [*page(S), tri([(12, 8.75), (16.5, 11), (7.5, 11)]), block(8.5, 12, 1.5, 3), block(11.25, 12, 1.5, 3), block(14, 12, 1.5, 3),
            detail(seg(8.5, 18, 11.25, 18)), detail(seg(13, 18, 15.5, 18))]


@icon("pay-stub", CAT, "Narrow slip with a perforated stub edge and a dollar sign above a text line",
      tags=["pay stub", "payslip", "wage slip", "salary", "paycheck", "earnings", "payroll"])
def _(S):
    return [shell(rect(5, 2.5, 14, 19, S.R)), detail(dashes([(9, 4.5), (9, 19.5)], 2.5, 2)),
            detail("M16 8H13.25A1.5 1.5 0 0 0 13.25 11H14.75A1.5 1.5 0 0 1 14.75 14H12"), detail(seg(13.25, 6, 13.25, 8)), detail(seg(13.25, 14, 13.25, 16)),
            detail(seg(12, 18.5, 16, 18.5))]


@icon("utility-bill", CAT, "Page with a folded corner, a lightning bolt and a water drop above an amount line",
      tags=["utility bill", "electricity", "water bill", "gas bill", "household bills", "energy", "statement"])
def _(S):
    return [*page(S), tri([(11, 8.75), (7.5, 12.75), (9.75, 12.75), (8.75, 15.5), (12.5, 11.5), (10.25, 11.5)]),
            Part("dot", "M14.5 9.25L12.25 12.75A2.6 2.6 0 1 0 16.75 12.75Z"), detail(seg(8.5, 18, 15.5, 18))]


@icon("balance-sheet", CAT, "Page with two columns of lines and an equals sign centred at the bottom",
      tags=["balance sheet", "accounting", "assets", "liabilities", "equity", "financial statement", "books"])
def _(S):
    return [sheet(S), detail(seg(12, 4.5, 12, 12.5)), detail(seg(7.5, 6.5, 10, 6.5)), detail(seg(7.5, 10.5, 10, 10.5)),
            detail(seg(14, 6.5, 16.5, 6.5)), detail(seg(14, 10.5, 16.5, 10.5)),
            detail(seg(9.5, 15.25, 14.5, 15.25)), detail(seg(9.5, 18.25, 14.5, 18.25))]


@icon("credit-report", CAT, "Page with a half circle gauge dial and needle at the top and text lines below",
      tags=["credit report", "credit score", "rating", "gauge", "financial health", "creditworthiness", "score"])
def _(S):
    return [sheet(S), detail(arc(12, 11.5, 4, 180, 360)), detail(seg(12, 11.5, 14.25, 8.75)), dot(12, 11.5, 1.25),
            detail(seg(8, 15.75, 16, 15.75)), detail(seg(8, 18.5, 13, 18.5))]


@icon("stock-certificate", CAT, "Wide certificate with a round seal on the left and a rising line chart on the right",
      tags=["stock certificate", "shares", "equity", "bond", "securities", "investment", "share certificate"])
def _(S):
    return [shell(rect(2.5, 4.5, 19, 15, S.R)), detail(circle(8, 12.5, 2.5)),
            detail(seg(13, 8.5, 18.5, 8.5)), detail(poly([(12.75, 16), (15, 13.5), (16.5, 14.75), (18.75, 11.5)], r=S.r * 0.5))]


@icon("iou-note", CAT, "Small note with the letters IOU written across it",
      tags=["iou", "i owe you", "debt", "promissory note", "loan", "owed", "note"])
def _(S):
    return [shell(rect(2, 6.5, 20, 11, S.R)), detail(seg(5.75, 9.5, 5.75, 14.5)), detail(ellipse(10.5, 12, 1.75, 2.5)),
            detail("M15.25 9.5V12A2 2 0 0 0 19.25 12V9.5")]


@icon("bank-passbook", CAT, "Bound booklet opened to ruled ledger lines",
      tags=["passbook", "bank book", "savings book", "account book", "ledger", "deposits", "banking"])
def _(S):
    pts = [(12, 7), (8, 5.5), (2.5, 5.5), (2.5, 18.5), (8, 18.5), (12, 20), (16, 18.5), (21.5, 18.5), (21.5, 5.5), (16, 5.5)]
    return [shell(poly(pts, closed=True, r=S.r)), detail(seg(12, 7, 12, 20)), detail(seg(5.25, 10.5, 9, 10.5)), detail(seg(5.25, 14, 9, 14)),
            detail(seg(15, 10.5, 18.75, 10.5)), detail(seg(15, 14, 18.75, 14))]


@icon("receipt-book", CAT, "Bound pad of receipt slips with a perforated stub edge and a sheet behind",
      tags=["receipt book", "duplicate book", "carbon copy", "invoice pad", "stub book", "cash receipts", "pad"])
def _(S):
    return [shell(rect(2.5, 7, 16, 13.5, S.R)), line(poly([(6.5, 7), (6.5, 3.5), (21.5, 3.5), (21.5, 16), (18.5, 16)], r=S.r)),
            detail(dashes([(7.5, 9), (7.5, 18.5)], 2, 2)), detail(seg(10.5, 11, 15.5, 11)), detail(seg(10.5, 16, 15.5, 16))]


@icon("syllabus", CAT, "Page with a graduation cap at the top and a short numbered list below",
      tags=["syllabus", "course outline", "curriculum", "class plan", "school", "lesson plan", "graduation"])
def _(S):
    return [*page(S), tri([(12, 8.75), (17, 10.5), (12, 12.25), (7, 10.5)]),
            tri([(9, 11.75), (9, 13.5), (12, 14.5), (15, 13.5), (15, 11.75), (12, 12.75)]),
            dot(8, 16.75, 0.9), detail(seg(10.5, 16.75, 16, 16.75)), dot(8, 19, 0.9), detail(seg(10.5, 19, 16, 19))]


@icon("patent", CAT, "Page with a light bulb at the top and a small ribbon seal in the lower corner",
      tags=["patent", "invention", "intellectual property", "idea", "ip", "inventor", "filing"])
def _(S):
    return [*page(S), detail("M10.75 9.5A3 3 0 0 1 12.6 14.75V15.5H8.9V14.75A3 3 0 0 1 10.75 9.5Z"), detail(seg(9.75, 17.5, 11.75, 17.5)),
            dot(15.5, 16.5, 1.75), tri([(14.3, 17.8), (13.6, 20), (15.3, 19.3)]), tri([(16.7, 17.8), (17.4, 20), (15.7, 19.3)])]


@icon("property-deed", CAT, "Document with a small house at the top and a round seal with ribbon tails at the bottom",
      tags=["deed", "property", "title deed", "real estate", "ownership", "land", "conveyance"])
def _(S):
    return [*page(S), tri([(12, 8.75), (16, 11.75), (16, 14), (8, 14), (8, 11.75)]), dot(12, 17, 1.75),
            tri([(10.8, 18.2), (10, 20), (11.8, 19.4)]), tri([(13.2, 18.2), (14, 20), (12.2, 19.4)])]


@icon("last-will", CAT, "Page with a quill feather across it and a wax seal at the bottom",
      tags=["will", "testament", "last will", "inheritance", "estate", "legacy", "quill"])
def _(S):
    return [*page(S), detail("M9.5 14.75C9.5 11.5 12 9.25 16 9C16 12.75 13.75 14.75 9.5 14.75Z"), detail(seg(7.5, 17, 12.5, 12)),
            dot(15, 18, 1.5)]


@icon("lease-agreement", CAT, "Page with a small house and a key at the top above a signature line",
      tags=["lease", "rental agreement", "tenancy", "rent contract", "landlord", "tenant", "let"])
def _(S):
    return [*page(S), tri([(9.75, 9), (12.5, 11.5), (12.5, 14.25), (7, 14.25), (7, 11.5)]),
            detail(circle(15, 12, 1.5)), detail(seg(15, 13.5, 15, 16.75)), detail(seg(15, 15.75, 16.5, 15.75)), detail(seg(8.5, 19, 15.5, 19))]


def _rot(pts, deg, cx, cy):
    a = math.radians(deg)
    c, s_ = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s_, cy + (x - cx) * s_ + (y - cy) * c) for x, y in pts]


@icon("court-order", CAT, "Page with a small gavel at the top and text lines below",
      tags=["court order", "judgment", "ruling", "gavel", "legal", "judge", "injunction"])
def _(S):
    head = _rot([(10.5, 8.75), (16, 8.75), (16, 11.5), (10.5, 11.5)], 45, 13.25, 10.125)
    return [*page(S), tri(head), detail(seg(12.25, 11.5, 8.25, 15.5)), detail(seg(8.5, 19, 15.5, 19))]


@icon("affidavit", CAT, "Page with a raised right hand at the top and a signature line at the bottom",
      tags=["affidavit", "oath", "sworn statement", "declaration", "testimony", "notary", "swear"])
def _(S):
    return [*page(S), block(10, 9, 1.25, 4), block(11.75, 8.5, 1.25, 4.5), block(13.5, 9.25, 1.25, 3.75), block(15.25, 10.75, 1.25, 2.25),
            block(9.5, 12.75, 7, 3.25), tri([(9.5, 14.5), (7.5, 12.5), (8.75, 11.5), (9.5, 12.5)]), detail(seg(8.5, 19, 15.5, 19))]


@icon("law-book", CAT, "Thick hardcover book with a balance scale on its cover and a spine band",
      tags=["law book", "statute", "legal code", "justice", "scales", "legislation", "jurisprudence"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 19, S.R)), detail(seg(8.5, 2.5, 8.5, 21.5)), detail(seg(13.25, 6.5, 13.25, 16.5)),
            detail(seg(10.5, 8.5, 16, 8.5)), Part("dot", "M9.4 11.25H12.1A1.35 1.35 0 0 1 9.4 11.25Z"),
            Part("dot", "M14.4 11.25H17.1A1.35 1.35 0 0 1 14.4 11.25Z"), detail(seg(11.25, 17, 15.25, 17))]


@icon("marriage-certificate", CAT, "Wide certificate with two interlocked rings in the centre",
      tags=["marriage", "wedding", "marriage license", "rings", "matrimony", "union", "civil ceremony"])
def _(S):
    return [shell(rect(2.5, 4.5, 19, 15, S.R)), detail(circle(9.75, 12, 3)), detail(circle(14.25, 12, 3))]


@icon("death-certificate", CAT, "Wide certificate with a single lily flower in the centre",
      tags=["death certificate", "lily", "funeral", "bereavement", "deceased", "obituary", "remembrance"])
def _(S):
    return [shell(rect(2.5, 4.5, 19, 15, S.R)),
            Part("dot", "M12 7.75C10.5 9.5 10.5 11.75 12 13.75C13.5 11.75 13.5 9.5 12 7.75Z"),
            Part("dot", "M11.5 14C9 14 7.5 12 7.25 9.75C9.75 10 11.25 11.5 11.5 14Z"),
            Part("dot", "M12.5 14C15 14 16.5 12 16.75 9.75C14.25 10 12.75 11.5 12.5 14Z"),
            detail(seg(12, 13.75, 12, 17))]


# ============================================================================ cards, tickets and slips

def barcode(x0, x1, y0, y1):
    """Solid bars of mixed widths between x0 and x1."""
    out, x, k = [], x0, 0
    widths = [1, 1.5, 1, 1, 1.5, 1, 1.5, 1, 1, 1, 1.5, 1]
    while k < len(widths) and x + widths[k] <= x1 + 0.01:
        out.append(block(x, y0, widths[k], y1 - y0))
        x += widths[k] + 1.0
        k += 1
    return out


@icon("library-card", CAT, "Card with a small open book in the corner and a barcode strip along the bottom",
      tags=["library card", "borrower", "membership card", "lending", "books", "reader card", "barcode"])
def _(S):
    return [shell(rect(2.5, 4.5, 19, 15, S.R)),
            detail(poly([(5.75, 8.25), (5.75, 12.5), (8.75, 13.5), (11.75, 12.5), (11.75, 8.25), (8.75, 9.25)], closed=True, r=S.r * 0.4)),
            detail(seg(14.5, 9, 18.5, 9)), *barcode(5, 19, 15.25, 17.25)]


@icon("warranty-card", CAT, "Card with a shield on the left and text lines on the right",
      tags=["warranty", "guarantee", "protection plan", "coverage card", "after sales", "shield", "cover"])
def _(S):
    return [shell(rect(2.5, 4.5, 19, 15, S.R)),
            detail(poly([(8, 8), (11.25, 9.25), (11.25, 12.5), (8, 15.5), (4.75, 12.5), (4.75, 9.25)], closed=True, r=S.r * 0.66)),
            detail(seg(14, 9, 18.5, 9)), detail(seg(14, 12.5, 17.5, 12.5)), detail(seg(14, 16, 18, 16))]


def _board(S):
    x, y, w, h = 5, 4, 14, 17.5
    return [shell(poly([(8.5, y), (x, y), (x, y + h), (x + w, y + h), (x + w, y), (15.5, y)], r=S.R)), shell(rect(8.5, 2.5, 7, 4, min(S.R, 1.5)))]


@icon("work-order", CAT, "Clipboard holding a page with a small wrench at the top and a checklist line",
      tags=["work order", "job card", "service ticket", "maintenance", "repair request", "task sheet", "clipboard"])
def _(S):
    return [*_board(S), detail(arc(14.25, 11.5, 2.4, -15, 285)), detail(seg(12.55, 13.2, 9, 16.75)), detail(seg(9, 19.25, 15, 19.25))]


@icon("police-report", CAT, "Page with a folded corner and a bold star badge above text lines",
      tags=["police report", "incident report", "crime report", "law enforcement", "badge", "statement", "sheriff"])
def _(S):
    return [*page(S), tri(star_pts(11, 11.5, 3.5, 1.6)), detail(seg(8.5, 17, 15.5, 17))]


@icon("sick-note", CAT, "Page with a folded corner, a small thermometer and a signature squiggle at the bottom",
      tags=["sick note", "medical certificate", "doctor's note", "fit note", "absence", "illness", "sick leave"])
def _(S):
    return [*page(S), detail(seg(10.5, 9, 10.5, 12.75)), dot(10.5, 14.25, 2), detail(seg(13.75, 10, 15.25, 10)), detail(seg(13.75, 13, 15.25, 13)),
            detail("M8.5 19C9.75 17.25 10.75 20 12 18.5C13 17.5 14 19 15.5 18.5")]


@icon("raffle-ticket", CAT, "Ticket with a numbered stub on the left separated by a vertical perforated line",
      tags=["raffle", "lottery", "draw ticket", "tombola", "prize draw", "stub", "numbered ticket"])
def _(S):
    return [shell(rect(2.5, 5.5, 19, 13, S.R)), detail(dashes([(9, 7.5), (9, 16.5)], 2, 1.5)),
            detail(seg(5, 10, 6.5, 10)), detail(seg(5, 14, 6.5, 14)), detail(seg(12.5, 9.5, 18.5, 9.5)), detail(seg(12.5, 14, 16.5, 14))]


@icon("ticket-roll", CAT, "Coiled roll of tickets on the left with one ticket strip pulled out flat",
      tags=["ticket roll", "admission tickets", "tear-off tickets", "roll of tickets", "carnival", "queue ticket", "entry"])
def _(S):
    return [shell(circle(7, 12, 4.75)), dot(7, 12, 1.25),
            line(poly([(7, 7.25), (21, 7.25), (21, 16.75), (7, 16.75)], r=S.r)), detail(dashes([(16, 9.25), (16, 14.75)], 2, 1.5))]


@icon("flash-cards", CAT, "Two stacked cards, the front one showing a question mark",
      tags=["flash cards", "flashcards", "study cards", "revision", "memorise", "quiz", "question and answer"])
def _(S):
    return [shell(rect(3, 8, 14, 12, S.R)), detail("M7.75 12.25A2.25 2.25 0 1 1 10.75 14.25C10.25 14.65 10 15.1 10 15.75"), dot(10, 18, 0.95),
            line(poly([(7, 8), (7, 5), (21, 5), (21, 16), (17, 16)], r=S.r))]


def _mask(cx, cy, smile):
    face = P(ellipse(cx, cy, 2.75, 3.25))
    holes = [P(circle(cx - 1.1, cy - 1, 0.75)), P(circle(cx + 1.1, cy - 1, 0.75))]
    if smile:
        holes.append(ST(f"M{fmt(cx - 1.4)} {fmt(cy + 0.9)}Q{fmt(cx)} {fmt(cy + 2.6)} {fmt(cx + 1.4)} {fmt(cy + 0.9)}", 1.0))
    else:
        holes.append(ST(f"M{fmt(cx - 1.4)} {fmt(cy + 2.1)}Q{fmt(cx)} {fmt(cy + 0.5)} {fmt(cx + 1.4)} {fmt(cy + 2.1)}", 1.0))
    return Part("dot", path_to_d(D(face, *holes)))


@icon("theater-program", CAT, "Booklet cover with comedy and tragedy masks",
      tags=["theatre program", "playbill", "stage programme", "drama", "masks", "show booklet", "performance"])
def _(S):
    return [shell(rect(5, 2.5, 14, 19, S.R)), _mask(10.25, 9.5, True), _mask(13.75, 15.25, False)]


# ============================================================================ reference documents and books

@icon("datasheet", CAT, "Page with a folded corner, a small technical drawing of a part and a table below",
      tags=["datasheet", "data sheet", "specification", "spec sheet", "technical document", "component", "specs"])
def _(S):
    return [*page(S), detail(circle(12, 12, 2.25)), detail(seg(7.25, 12, 8.75, 12)), detail(seg(15.25, 12, 16.75, 12)),
            detail(seg(7, 17, 17, 17)), detail(seg(11.5, 17, 11.5, 20))]


@icon("terms-of-service", CAT, "Tall page of dense text lines with a checkbox and a short line at the bottom",
      tags=["terms of service", "terms and conditions", "tos", "user agreement", "eula", "legal terms", "accept terms"])
def _(S):
    return [sheet(S), detail(seg(8, 6, 16, 6)), detail(seg(8, 9, 16, 9)), detail(rect(7.5, 13.5, 5, 5, min(S.R, 1))), detail(seg(15, 16, 16.5, 16))]


@icon("picture-book", CAT, "Wide landscape book with a large sun and hill picture on its cover",
      tags=["picture book", "children's book", "storybook", "illustrated book", "kids", "story time", "nursery"])
def _(S):
    return [shell(rect(2.5, 5, 19, 14, S.R)), detail(seg(6, 5, 6, 19)), dot(17, 9.75, 1.5), detail(poly([(8.5, 17), (12, 12.5), (15, 16.25), (16.25, 15), (19, 17)], r=S.r))]


@icon("board-book", CAT, "Small chunky book with thick rounded corners and a star on its cover",
      tags=["board book", "baby book", "toddler book", "chunky book", "first book", "thick pages", "nursery"])
def _(S):
    rr = 3 if S.name == "line" else 5
    return [shell(rect(4.5, 3.5, 15, 17, rr)), detail(seg(8.5, 3.5, 8.5, 20.5)), tri(star_pts(14.25, 12, 3.25, 1.45))]


@icon("instruction-manual", CAT, "Thin booklet with three small numbered step marks on its cover",
      tags=["instruction manual", "user guide", "how to", "steps", "handbook", "assembly guide", "directions"])
def _(S):
    return [sheet(S), block(7.5, 5.5, 2.5, 2.5), detail(seg(12, 6.75, 16, 6.75)), block(7.5, 10.75, 2.5, 2.5),
            detail(seg(12, 12, 16, 12)), block(7.5, 16, 2.5, 2.5), detail(seg(12, 17.25, 16, 17.25))]


@icon("lab-notebook", CAT, "Bound notebook with a chemistry flask on its cover",
      tags=["lab notebook", "laboratory", "science journal", "experiment log", "research notes", "chemistry", "flask"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 19, S.R)), detail(seg(8, 2.5, 8, 21.5)), _flask_shifted()]


def _flask_shifted():
    body = P("M12.5 6.5H15.5V10L18.25 15.5C18.6 16.2 18.2 17 17.4 17H10.6C9.8 17 9.4 16.2 9.75 15.5L12.5 10Z")
    bubble = P(circle(13.75, 14, 0.8))
    return Part("dot", path_to_d(D(body, bubble)))


@icon("antique-book", CAT, "Thick old book with metal corner guards and a clasp across the fore edge",
      tags=["antique book", "old book", "rare book", "vintage", "tome", "clasp", "ancient text"])
def _(S):
    return [shell(rect(3.5, 2.5, 15, 19, S.R)), detail(seg(7.5, 2.5, 7.5, 21.5)), detail(seg(10.5, 8, 15, 8)),
            tri([(18.5, 3.5), (15, 3.5), (18.5, 7)]), tri([(18.5, 20.5), (15, 20.5), (18.5, 17)]),
            solid(rect(17.5, 10.5, 4, 3))]


@icon("book-box-set", CAT, "Slipcase seen from its open side with three book spines showing",
      tags=["box set", "book set", "slipcase", "trilogy", "series", "collection", "boxed set"])
def _(S):
    return [shell(rect(3.5, 3, 17, 18, S.R)), detail(seg(9.25, 3, 9.25, 21)), detail(seg(14.75, 3, 14.75, 21)),
            block(5, 7.5, 2.5, 1.75), block(10.75, 7.5, 2.5, 1.75), block(16.25, 7.5, 2.5, 1.75),
            block(5, 14.5, 2.5, 1.75), block(10.75, 14.5, 2.5, 1.75), block(16.25, 14.5, 2.5, 1.75)]


def _thumb_d(S):
    rr = min(S.R, 2)
    parts = [f"M{fmt(4.5 + rr)} 2.5H{fmt(19.5 - rr)}"]
    if rr:
        parts.append(f"A{fmt(rr)} {fmt(rr)} 0 0 1 19.5 {fmt(2.5 + rr)}")
    y = 2.5 + rr
    for c in (6.75, 12, 17.25):
        parts.append(f"V{fmt(c - 2)}A2 2 0 0 0 19.5 {fmt(c + 2)}")
        y = c + 2
    parts.append(f"V{fmt(21.5 - rr)}")
    if rr:
        parts.append(f"A{fmt(rr)} {fmt(rr)} 0 0 1 {fmt(19.5 - rr)} 21.5")
    parts.append(f"H{fmt(4.5 + rr)}")
    if rr:
        parts.append(f"A{fmt(rr)} {fmt(rr)} 0 0 1 4.5 {fmt(21.5 - rr)}")
    parts.append(f"V{fmt(2.5 + rr)}")
    if rr:
        parts.append(f"A{fmt(rr)} {fmt(rr)} 0 0 1 {fmt(4.5 + rr)} 2.5")
    return "".join(parts) + "Z"


@icon("thumb-index", CAT, "Thick book edge with a column of semicircle alphabet tabs cut into the pages",
      tags=["thumb index", "alphabet tabs", "dictionary", "index tabs", "directory", "finger cut", "reference book"])
def _(S):
    return [shell(_thumb_d(S)), detail(seg(8, 2.5, 8, 21.5))]


@icon("stone-tablet", CAT, "Upright slab with an arched top and carved text lines",
      tags=["stone tablet", "commandments", "engraved", "ancient law", "monument", "inscription", "tablet of law"])
def _(S):
    return [shell("M6.5 21.5V9.5A5.5 5.5 0 0 1 17.5 9.5V21.5Z"), detail(seg(9.5, 9.5, 14.5, 9.5)), detail(seg(9.5, 13, 14.5, 13)),
            detail(seg(9.5, 16.5, 14.5, 16.5))]
