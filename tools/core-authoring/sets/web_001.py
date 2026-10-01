"""TypeIcon Core: web (batch 001): browser features, page types, web culture, internet infrastructure, ads, security and links."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import circle_d, fmt, path_to_d, polar

CAT = "web"


def L(S, sharp, soft):
    return sharp if S.name == "line" else soft


def win(S, x, y, w, h, bar=4.5, cap=None):
    """Browser window: outline plus a title bar line."""
    return [shell(rect(x, y, w, h, S.R if cap is None else min(S.R, cap))), detail(seg(x, y + bar, x + w, y + bar))]


def head(S, tip, deg, size=3.0, role=line):
    pts = []
    for s in (-1, 1):
        a = math.radians(deg + 180 + s * 40)
        pts.append((tip[0] + size * math.cos(a), tip[1] + size * math.sin(a)))
    return role(poly([pts[0], tip, pts[1]], r=S.r * 0.5))


def arrow(S, x1, y1, x2, y2, size=3.0, role=line):
    deg = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return [role(seg(x1, y1, x2, y2)), head(S, (x2, y2), deg, size, role)]


def cursor(S, x, y, k=1.0):
    pts = [(0, 0), (0, 8), (2, 6.25), (3.4, 9.2), (5.1, 8.4), (3.75, 5.5), (6.25, 5.5)]
    return Part("dot", poly([(x + px * k, y + py * k) for px, py in pts], closed=True, r=L(S, 0, 0.5)))


def globe(S, cx, cy, r, mer=True, eq=True):
    out = [shell(circle(cx, cy, r))]
    if mer:
        out.append(detail(ellipse(cx, cy, r * 0.45, r)))
    if eq:
        out.append(detail(seg(cx - r, cy, cx + r, cy)))
    return out


def tab(S, x, y, w, h):
    """Browser tab: rounded top corners, open flat bottom edge (closed shape)."""
    r = L(S, 1, 3.5)
    return shell(f"M{fmt(x)} {fmt(y + h)}V{fmt(y + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x + r)} {fmt(y)}H{fmt(x + w - r)}"
                 f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x + w)} {fmt(y + r)}V{fmt(y + h)}Z")


def crescent(cx, cy, r, off=0.45, cut=0.8):
    """Solid crescent moon opening to the upper right."""
    a = P(circle_d(cx, cy, r))
    b = P(circle_d(cx + r * off, cy - r * off, r * cut))
    return solid(path_to_d(D(a, b)))


def sq(x, y, w, h, rx=0.0) -> Part:
    return Part("dot", rect(x, y, w, h, rx))


def person(cx, cy, k=1.0, role=detail):
    """Head dot with a shoulder arc; cy is the head centre."""
    return [dot(cx, cy, 1.7 * k),
            role(f"M{fmt(cx - 3.2 * k)} {fmt(cy + 7.4 * k)}V{fmt(cy + 6.6 * k)}A{fmt(3.2 * k)} {fmt(3.2 * k)} 0 0 1 {fmt(cx + 3.2 * k)} {fmt(cy + 6.6 * k)}V{fmt(cy + 7.4 * k)}")]


def lines(x, y, widths, gap=3.0, role=detail):
    return [role(seg(x, y + i * gap, x + w, y + i * gap)) for i, w in enumerate(widths)]


def link(S, cx, cy, k=1.0, role=line):
    """Horizontal chain link: two open capsules and a bar between them."""
    r = 3.5 * k
    xl = cx - 1.2 * k
    xr = cx + 1.2 * k
    ln = 5.8 * k
    left = f"M{fmt(xl)} {fmt(cy - r)}H{fmt(xl - ln + r)}A{fmt(r)} {fmt(r)} 0 0 0 {fmt(xl - ln + r)} {fmt(cy + r)}H{fmt(xl)}"
    right = f"M{fmt(xr)} {fmt(cy - r)}H{fmt(xr + ln - r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(xr + ln - r)} {fmt(cy + r)}H{fmt(xr)}"
    return [role(left), role(right), role(seg(cx - 3.2 * k, cy, cx + 3.2 * k, cy))]


# ============================================================================ browser features

@icon("browser-extension", CAT, "Browser window with a solid jigsaw puzzle piece in the page",
      tags=["browser extension", "add-on", "plugin", "puzzle piece", "browser add on", "web extension"])
def _(S):
    piece = U(P(rect(8, 11, 8.5, 8, 0.8)), P(circle_d(12.2, 10.2, 2)), P(circle_d(17.4, 15, 2)))
    return [shell(rect(2, 2, 20, 20, S.R)), detail(seg(2, 6.5, 22, 6.5)), Part("dot", path_to_d(piece))]


@icon("vertical-tabs", CAT, "Browser window with a narrow left column of four stacked tab rows, the top one solid",
      tags=["vertical tabs", "tab sidebar", "side tabs", "tab list", "tree tabs", "tab column", "browser sidebar"])
def _(S):
    return [shell(rect(2, 3, 20, 18, S.R)), detail(seg(10, 3, 10, 21)),
            sq(4, 5.4, 4.2, 2.2, 0.6), detail(seg(4.5, 10.5, 7.5, 10.5)), detail(seg(4.5, 14.5, 7.5, 14.5)),
            detail(seg(4.5, 18.5, 7.5, 18.5)),
            detail(seg(13, 8, 19, 8)), detail(seg(13, 12, 19, 12)), detail(seg(13, 16, 17, 16))]


@icon("sleeping-tab", CAT, "Browser tab with a crescent moon and a z floating above it",
      tags=["sleeping tab", "tab suspend", "inactive tab", "memory saver", "discarded tab", "snooze tab", "idle tab"])
def _(S):
    return [tab(S, 2, 12, 20, 9), detail(seg(6, 17, 12, 17)),
            line(poly([(3.5, 3.5), (8, 3.5), (3.5, 8), (8, 8)], r=S.r * 0.5)),
            crescent(17.5, 6.5, 4.2)]


@icon("audio-playing-tab", CAT, "Browser tab with a speaker and two sound waves inside it",
      tags=["audio tab", "tab playing sound", "speaker tab", "noisy tab", "mute tab", "media playing", "sound indicator"])
def _(S):
    spk = poly([(5.5, 11.4), (8, 11.4), (11.5, 8.4), (11.5, 17.6), (8, 14.6), (5.5, 14.6)], closed=True, r=L(S, 0, 0.5))
    return [tab(S, 2, 5, 20, 16), Part("dot", spk),
            detail(arc(11.5, 13, 3.6, -50, 50)), detail(arc(11.5, 13, 6.4, -50, 50))]


@icon("too-many-tabs", CAT, "Browser window whose top edge is crowded with a dense row of squeezed tabs",
      tags=["too many tabs", "tab overload", "tab hoarding", "crowded tabs", "tab strip", "tab clutter", "open tabs"])
def _(S):
    pts = [(2, 9)]
    for i in range(3):
        x0 = 2 + 6.67 * i
        pts += [(x0 + 1.3, 4), (x0 + 5.37, 4), (x0 + 6.67, 9)]
    return [shell(poly([(2, 9), (22, 9), (22, 21), (2, 21)], closed=True, r=S.r)),
            line(poly(pts, r=S.r * 0.4)), detail(seg(6, 14, 18, 14)), detail(seg(6, 17.5, 13, 17.5))]


@icon("browser-profiles", CAT, "Browser window with two small people side by side in the page",
      tags=["browser profiles", "user profiles", "switch profile", "multiple users", "accounts", "avatars", "work and personal"])
def _(S):
    return win(S, 2, 3, 20, 18, 4.5) + person(7.8, 11.6) + person(16.2, 11.6)


@icon("kiosk-mode", CAT, "Freestanding kiosk with a tall screen showing a full-screen page and no toolbar",
      tags=["kiosk mode", "full screen", "public terminal", "self service", "locked browser", "digital signage", "kiosk"])
def _(S):
    return [shell(rect(5, 2, 14, 14, min(S.R, 3))), detail(seg(8.5, 6, 15.5, 6)), detail(seg(8.5, 9.5, 15.5, 9.5)),
            detail(seg(8.5, 13, 12.5, 13)), line(seg(12, 16, 12, 20)), line(seg(7.5, 21, 16.5, 21))]


@icon("web-clipper", CAT, "Browser window above a dashed cut line with a pair of scissors cutting along it",
      tags=["web clipper", "clip page", "save article", "snip", "capture content", "scissors", "bookmark clip"])
def _(S):
    return [shell(rect(2, 2, 20, 10, min(S.R, 3))), detail(seg(2, 5.5, 22, 5.5)),
            line(seg(2, 18.5, 4.5, 18.5)), line(seg(6.5, 18.5, 9, 18.5)),
            line(seg(17.5, 17.2, 10.5, 20.6)), line(seg(17.5, 20.6, 10.5, 17.2)),
            line(circle(19.8, 16.8, 1.9)), line(circle(19.8, 21, 1.9))]


@icon("full-page-screenshot", CAT, "Tall web page framed by four camera corner brackets",
      tags=["full page screenshot", "scrolling capture", "page capture", "long screenshot", "snapshot", "screen grab", "capture"])
def _(S):
    b = L(S, 0, 1.0)
    return [shell(rect(7, 5, 10, 14, min(S.R, 2))), detail(seg(7, 8.5, 17, 8.5)), detail(seg(10, 12, 14, 12)),
            detail(seg(10, 15, 14, 15)),
            line(poly([(3, 6), (3, 2.5), (6.5, 2.5)], r=b)), line(poly([(21, 6), (21, 2.5), (17.5, 2.5)], r=b)),
            line(poly([(3, 18), (3, 21.5), (6.5, 21.5)], r=b)), line(poly([(21, 18), (21, 21.5), (17.5, 21.5)], r=b))]


@icon("page-loading-bar", CAT, "Browser window with a partly filled progress bar in the page",
      tags=["page loading", "progress bar", "loading bar", "page load", "loading indicator", "waiting", "load progress"])
def _(S):
    return win(S, 2, 3, 20, 18, 4.5) + [detail(rect(5, 12, 14, 3.6, 1.8)), sq(5, 12, 8, 3.6, 1.8)]


@icon("page-crash", CAT, "Browser window with a crack across the top corner and a sad face in the page",
      tags=["page crash", "aw snap", "tab crashed", "browser error", "sad face", "broken page", "crashed"])
def _(S):
    return win(S, 2, 3, 20, 18, 4.5) + [
        detail(circle(10.5, 14.5, 4.2)),
        dot(9, 13.4, 0.9), dot(12, 13.4, 0.9), detail(arc(10.5, 18.2, 2.6, 215, 325)),
        detail(poly([(17, 7.5), (19.5, 10.5), (17.5, 13), (20.5, 16)], r=0))]


@icon("search-results-page", CAT, "Browser page with a magnifier and query line on top and three stacked result lines",
      tags=["search results", "serp", "results page", "search page", "search engine", "result list", "find"])
def _(S):
    return [shell(rect(2, 2, 20, 20, S.R)), detail(circle(7, 7, 2.2)), detail(seg(8.6, 8.6, 10, 10)),
            detail(seg(13, 7, 19, 7)),
            detail(seg(5.5, 14, 18.5, 14)), detail(seg(5.5, 18, 18.5, 18))]


@icon("new-tab-page", CAT, "Browser window with a centered search bar and a grid of six shortcut tiles",
      tags=["new tab", "start page", "home page", "shortcuts", "speed dial", "tab page", "browser home"])
def _(S):
    out = win(S, 2, 2, 20, 20, 4.5) + [sq(6, 7.6, 12, 2.4, 1.2)]
    for r_ in (12.5, 16.6):
        for c in (4.5, 10, 15.5):
            out.append(sq(c, r_, 4, 3, 0.8))
    return out


@icon("mobile-browser", CAT, "Smartphone with an address bar across the top of its screen and page lines below",
      tags=["mobile browser", "phone web", "mobile web", "mobile site", "smartphone browsing", "address bar", "responsive"])
def _(S):
    return [shell(rect(6, 2, 12, 20, min(S.R, 3))), sq(8.5, 5, 7, 2.2, 1.1),
            detail(seg(9, 11, 15, 11)), detail(seg(9, 14.5, 15, 14.5)), detail(seg(9, 18, 12.5, 18))]


@icon("desktop-site-view", CAT, "Desktop monitor with a small smartphone standing in front of its lower right side",
      tags=["desktop site", "desktop version", "request desktop site", "full site", "switch to desktop", "wide layout", "monitor and phone"])
def _(S):
    return [shell(rect(2, 3, 13, 10, min(S.R, 3))), line(seg(8.5, 13, 8.5, 17)), line(seg(5, 18, 12, 18)),
            shell(rect(17, 8, 5, 13, min(S.R, 2)))]

# ============================================================================ page types and web culture

@icon("user-agent", CAT, "Browser window with a small ID card showing a head and two text lines in the page",
      tags=["user agent", "browser identity", "ua string", "client id", "http header", "browser id card", "request header"])
def _(S):
    return win(S, 2, 2, 20, 20, 4.5) + [
        detail(rect(6, 10.5, 12, 8, 1.5)), dot(9.6, 13.8, 1.1), detail(seg(13, 13.4, 15.5, 13.4)),
        detail(seg(13, 16.2, 15.5, 16.2))]


@icon("browser-storage", CAT, "Browser window with a database cylinder in the page",
      tags=["browser storage", "local storage", "cookies storage", "indexeddb", "web storage", "session storage", "client data"])
def _(S):
    cyl = ("M8 11.2A4 1.7 0 0 1 16 11.2A4 1.7 0 0 1 8 11.2M8 11.2V18A4 1.7 0 0 0 16 18V11.2M8 14.6A4 1.7 0 0 0 16 14.6")
    return win(S, 2, 2, 20, 20, 4.5) + [detail(cyl)]


@icon("coming-soon-page", CAT, "Browser window with a small rocket standing in the page",
      tags=["coming soon", "launch page", "teaser page", "pre launch", "rocket", "under wraps", "landing page"])
def _(S):
    body = "M12 8.8C14 10.6 14.6 13.6 13.8 16.4H10.2C9.4 13.6 10 10.6 12 8.8Z"
    return win(S, 2, 2, 20, 20, 4.5) + [
        detail(body), dot(12, 12.6, 1.0),
        detail(poly([(10.4, 14.6), (8.2, 17.4), (10.3, 16.8)], r=0)), detail(poly([(13.6, 14.6), (15.8, 17.4), (13.7, 16.8)], r=0)),
        detail(seg(12, 17.6, 12, 19.2))]


@icon("under-construction-page", CAT, "Browser window with a solid traffic cone on the left and a barrier on the right",
      tags=["under construction", "work in progress", "site building", "traffic cone", "barrier", "not ready", "coming back"])
def _(S):
    return win(S, 2, 2, 20, 20, 4.5) + [
        Part("dot", poly([(8, 10), (10, 10), (12.6, 17.6), (5.4, 17.6)], closed=True, r=0)), sq(4.4, 17.6, 9.2, 1.8, 0.4),
        detail(rect(14, 10.5, 7, 4.2, 0.5)), detail(seg(15.6, 14.7, 15.6, 19)), detail(seg(19.4, 14.7, 19.4, 19))]


@icon("maintenance-page", CAT, "Browser window with a wrench and a screwdriver crossed in the page",
      tags=["maintenance page", "site down for maintenance", "scheduled downtime", "repair", "wrench", "screwdriver", "be right back"])
def _(S):
    return win(S, 2, 2, 20, 20, 4.5) + [
        detail(seg(7, 18.5, 14.2, 13.2)), detail(arc(15.6, 11.4, 2.6, 0, 270)),
        detail(seg(16.6, 18.4, 8.6, 11.4)), detail(seg(7.6, 10.3, 9.6, 10.3))]


@icon("thank-you-page", CAT, "Browser window with a solid heart above a short centered text line",
      tags=["thank you page", "confirmation page", "order complete", "thanks", "heart", "success page", "post signup"])
def _(S):
    heart = "M12 16.6C12 16.6 7 13.6 7 10.6A2.7 2.7 0 0 1 12 9.4A2.7 2.7 0 0 1 17 10.6C17 13.6 12 16.6 12 16.6Z"
    return win(S, 2, 2, 20, 20, 4.5) + [Part("dot", heart), detail(seg(8, 19.2, 16, 19.2))]


@icon("faq-page", CAT, "Browser page with a large question mark and three accordion chevrons beside it",
      tags=["faq", "faq page", "frequently asked questions", "help page", "questions and answers", "accordion", "support page"])
def _(S):
    out = [shell(rect(2, 2, 20, 20, S.R)),
           detail("M5.2 8.4A2.8 2.8 0 1 1 8 11.2V13.4"), dot(8, 17, 1.2)]
    for y in (7, 12, 17):
        out.append(detail(poly([(14.8, y - 1), (17, y + 1), (19.2, y - 1)], r=0)))
    return out


@icon("team-page", CAT, "Browser page with a grid of six small round heads, each with a short name line under it",
      tags=["team page", "meet the team", "staff page", "our people", "employees", "people grid", "company team"])
def _(S):
    out = [shell(rect(2, 2, 20, 20, S.R))]
    for y in (6.4, 14.2):
        for x in (6.2, 12, 17.8):
            out += [dot(x, y, 1.45), detail(seg(x - 1.3, y + 4, x + 1.3, y + 4))]
    return out


@icon("about-page", CAT, "Browser page with a round portrait on the left and text lines on the right and below",
      tags=["about page", "about us", "company story", "bio page", "who we are", "profile page", "our story"])
def _(S):
    return [shell(rect(2, 2, 20, 20, S.R)), dot(8, 9, 3.2),
            detail(seg(13.5, 7, 19, 7)), detail(seg(13.5, 11, 19, 11)),
            detail(seg(5, 15, 19, 15)), detail(seg(5, 18.6, 15, 18.6))]


@icon("wiki-article", CAT, "Article page with a solid infobox at the right, a heading bar and text lines",
      tags=["wiki article", "encyclopedia page", "wiki page", "reference article", "knowledge base", "infobox"])
def _(S):
    return [shell(rect(2, 2, 20, 20, S.R)), sq(14, 5, 5.5, 7.5, 0.6),
            detail(seg(5, 6, 10.5, 6)), detail(seg(5, 9.5, 10.5, 9.5)), detail(seg(5, 13, 10.5, 13)),
            detail(seg(5, 16.4, 19, 16.4)), detail(seg(5, 19.6, 14, 19.6))]


@icon("discussion-forum", CAT, "Stack of three thread rows, each with a round avatar, a title line and a reply bubble",
      tags=["discussion forum", "message board", "threads", "forum", "community board", "topics list", "bulletin"])
def _(S):
    out = []
    for y in (5.2, 12, 18.8):
        out += [dot(4.6, y, 1.8), line(seg(9, y, 15, y)),
                Part("dot", poly([(17.2, y - 2), (21.4, y - 2), (21.4, y + 1.4), (19.6, y + 1.4), (18.2, y + 3), (18.2, y + 1.4), (17.2, y + 1.4)], closed=True, r=0))]
    return out


@icon("comment-section", CAT, "Article text lines above two comment rows with round avatars, the second one indented",
      tags=["comment section", "comments", "replies", "article comments", "reader comments", "discussion thread", "user comments"])
def _(S):
    return [shell(rect(2, 2, 20, 20, S.R)), detail(seg(5.5, 5.8, 18.5, 5.8)), detail(seg(5.5, 9, 14, 9)),
            dot(6.2, 13.6, 1.5), detail(seg(10, 13.6, 18.5, 13.6)),
            dot(9.2, 18.2, 1.5), detail(seg(13, 18.2, 18.5, 18.2))]


@icon("blogroll", CAT, "Header bar over three list rows, each with a small solid site tile and a text line",
      tags=["blogroll", "link list", "blog links", "recommended blogs", "friends links", "sidebar links", "link roll"])
def _(S):
    out = [Part("dot", rect(3, 2.8, 18, 3, S.R * 0.3))]
    for y in (11, 15.6, 20.2):
        out += [sq(3, y - 1.8, 3.6, 3.6, 1.0), line(seg(9.5, y, 21, y))]
    return out


@icon("webring", CAT, "Circle of five small web page tiles sitting on a closed ring",
      tags=["webring", "web ring", "site ring", "linked sites", "circular links", "network of sites", "retro web"])
def _(S):
    cx, cy, r = 12, 12.4, 8.2
    out = [line(circle(cx, cy, r))]
    for i in range(5):
        x, y = polar(cx, cy, r, -90 + 72 * i)
        out.append(sq(x - 2.5, y - 2.1, 5, 4.2, L(S, 0.2, 1.6)))
    return out


@icon("visitor-counter", CAT, "Retro counter strip of boxed digit cells with an eye above it",
      tags=["visitor counter", "hit counter", "page views", "retro counter", "odometer", "site visits", "web counter"])
def _(S):
    eye = "M4.5 8C7 3.8 17 3.8 19.5 8C17 12.2 7 12.2 4.5 8Z"
    return [shell(eye), dot(12, 8, 1.7), shell(rect(2, 15, 20, 6, L(S, 1, 3))),
            detail(seg(7, 15, 7, 21)), detail(seg(12, 15, 12, 21)), detail(seg(17, 15, 17, 21))]



# ============================================================================ internet infrastructure and culture

@icon("bulletin-board-system", CAT, "Old boxy monitor with menu lines on its screen and a cable running to a small modem",
      tags=["bbs", "bulletin board system", "dial up", "modem", "retro computing", "old internet", "terminal"])
def _(S):
    return [shell(rect(2, 2, 14, 11, min(S.R, 2.5))), detail(seg(5, 6, 13, 6)), detail(seg(5, 9, 10, 9)),
            line(seg(6, 15.3, 12, 15.3)),
            line(poly([(16, 7.5), (20, 7.5), (20, 17.4)], r=S.r * 0.5)),
            shell(rect(10, 17.5, 12, 4, min(S.R, 1.5))), dot(13.5, 19.5, 0.7), dot(16.5, 19.5, 0.7)]


@icon("internet-cafe", CAT, "Two screens on stands at a desk with a steaming coffee cup standing between them",
      tags=["internet cafe", "cyber cafe", "public computers", "coffee shop wifi", "cybercafe", "net cafe", "computer rental"])
def _(S):
    cup = poly([(9.4, 12.6), (13.4, 12.6), (12.9, 17.4), (9.9, 17.4)], closed=True, r=S.r * 0.4)
    return [shell(rect(2, 3.5, 6.6, 6.2, 1.2)), shell(rect(15.4, 3.5, 6.6, 6.2, 1.2)),
            line(seg(5.3, 9.7, 5.3, 15)), line(seg(18.7, 9.7, 18.7, 15)),
            line(seg(2, 19.6, 22, 19.6)),
            shell(cup), line(arc(13.4, 14.8, 1.6, -80, 80)),
            line("M11.4 5Q10.6 6 11.4 7Q12.2 8 11.4 9")]


@icon("web-portal", CAT, "Browser window with an open arched doorway in the page and an arrow passing through it",
      tags=["web portal", "gateway", "entry point", "login portal", "doorway", "enter site", "access point"])
def _(S):
    return win(S, 2, 2, 20, 20, 4.5) + [
        detail("M9 20V13A3 3 0 0 1 15 13V20"),
        detail(seg(4, 16.5, 11, 16.5)), head(S, (12.2, 16.5), 0, 2.2, detail)]


@icon("web-archive", CAT, "Archive box with the edges of stacked web pages standing up out of its open top",
      tags=["web archive", "archived pages", "page snapshots", "preservation", "stored site", "history of the web"])
def _(S):
    return [shell(rect(3, 12, 18, 9, min(S.R, 2))), detail(seg(9.5, 15.8, 14.5, 15.8)),
            line(poly([(5, 12), (5, 7), (19, 7), (19, 12)], r=S.r * 0.5)),
            line(poly([(8, 7), (8, 3), (16, 3), (16, 7)], r=S.r * 0.5))]


@icon("web-directory", CAT, "Open index book with a small globe on the left page and tabs down the right edge",
      tags=["web directory", "site directory", "link directory", "index of sites", "yellow pages", "catalog", "listing"])
def _(S):
    return [shell(rect(2, 3.5, 16, 17, min(S.R, 2.5))), detail(seg(10, 3.5, 10, 20.5)),
            detail(circle(6, 12, 2.6)), detail(seg(3.4, 12, 8.6, 12)), detail(seg(13, 8, 15, 8)), detail(seg(13, 12, 15, 12)), detail(seg(13, 16, 15, 16)),
            sq(19.2, 6, 2.8, 3, 0.5), sq(19.2, 11, 2.8, 3, 0.5), sq(19.2, 16, 2.8, 3, 0.5)]


@icon("extranet", CAT, "Tall office building and a shorter partner building joined by a line that crosses a dashed boundary",
      tags=["extranet", "partner network", "b2b portal", "shared access", "supplier portal", "external network", "intranet extension"])
def _(S):
    return [shell(rect(2, 5, 7, 16, min(S.R, 1.5))), shell(rect(15, 11, 7, 10, min(S.R, 1.5))),
            dot(5.5, 9, 0.9), dot(5.5, 13, 0.9), dot(18.5, 15, 0.9),
            line(seg(9, 18, 15, 18)),
            line(seg(12, 2.5, 12, 5.2)), line(seg(12, 8.2, 12, 11)), line(seg(12, 14, 12, 15))]


@icon("captive-portal", CAT, "Wifi symbol above a small browser window showing a wide sign in button",
      tags=["captive portal", "wifi login", "hotspot sign in", "guest wifi", "splash page", "network login", "hotel wifi"])
def _(S):
    return [dot(12, 9.5, 1.3), line(arc(12, 9.5, 3.6, -135, -45)), line(arc(12, 9.5, 6.6, -135, -45)),
            shell(rect(3, 13, 18, 8, min(S.R, 2.5))), sq(7.5, 16, 9, 2.6, 1.3)]


@icon("internet-service-provider", CAT, "Building with an antenna mast on its roof and a cable running across to a small house",
      tags=["isp", "internet service provider", "broadband company", "telecom", "connection provider", "cable company", "home internet"])
def _(S):
    return [shell(rect(2, 8, 8, 13, min(S.R, 1.5))), dot(6, 12.5, 0.9), dot(6, 16.5, 0.9),
            line(seg(6, 8, 6, 3)), dot(6, 3, 1.1),
            shell(poly([(14.5, 21), (14.5, 14), (18.5, 10), (22.5, 14), (22.5, 21)], closed=True, r=S.r * 0.5)),
            line(seg(10, 18.5, 14.5, 18.5))]


@icon("net-neutrality", CAT, "Equals sign above three parallel lines of equal width, each carrying one data block",
      tags=["net neutrality", "equal access", "open internet", "fair traffic", "isp rules", "no throttling", "equal treatment"])
def _(S):
    return [line(seg(8, 3.5, 16, 3.5)), line(seg(8, 7, 16, 7)),
            line(seg(2, 12.5, 22, 12.5)), line(seg(2, 16.5, 22, 16.5)), line(seg(2, 20.5, 22, 20.5)),
            sq(5, 11, 4, 3, 0.6), sq(11, 15, 4, 3, 0.6), sq(16.5, 19, 4, 3, 0.6)]


@icon("geo-restriction", CAT, "Globe with a lowered barrier arm and post crossing in front of it",
      tags=["geo restriction", "geo blocking", "region lock", "country block", "not available in your region", "geofence", "blocked location"])
def _(S):
    return globe(S, 12, 9.5, 7.3) + [sq(2, 14, 3, 7, 0.5), line(seg(5, 16.4, 22, 16.4))]


@icon("web-filter", CAT, "Funnel sitting on a browser window with a few dots caught inside it",
      tags=["web filter", "content filter", "url filter", "parental controls", "blocklist", "safe browsing", "internet filter"])
def _(S):
    return [shell(poly([(3, 2.5), (21, 2.5), (13.5, 10), (13.5, 12.5), (10.5, 12.5), (10.5, 10), ], closed=True, r=S.r * 0.6)),
            dot(8.5, 5.5, 0.9), dot(15.5, 5.5, 0.9),
            shell(rect(4, 14, 16, 7, min(S.R, 2))), detail(seg(4, 17.3, 20, 17.3))]


@icon("bot-traffic", CAT, "Small robot head with an arrow cursor pointing into a browser window next to it",
      tags=["bot traffic", "crawler", "automated visits", "scraper", "non human traffic", "spider", "robot visitors"])
def _(S):
    return [shell(rect(2, 10, 8, 8, min(S.R, 2))), line(seg(6, 10, 6, 6.5)), dot(6, 5.5, 1.1),
            dot(4.4, 13.5, 0.9), dot(7.6, 13.5, 0.9), detail(seg(4.4, 16, 7.6, 16)),
            shell(rect(13, 4, 9, 16, min(S.R, 2))), detail(seg(13, 8, 22, 8)), cursor(S, 14.6, 11.5, 0.8)]


@icon("internet-exchange-point", CAT, "Central square hub with six spokes running out to small dots and squares around it",
      tags=["ixp", "internet exchange", "peering", "network hub", "interconnect", "backbone", "data exchange"])
def _(S):
    out = [shell(rect(9, 9, 6, 6, min(S.R, 1.5)))]
    for i in range(6):
        a = -90 + 60 * i
        x, y = polar(12, 12, 8.8, a)
        p0, p1 = polar(12, 12, 4.4, a), polar(12, 12, 6.6, a)
        out.append(line(seg(p0[0], p0[1], p1[0], p1[1])))
        out.append(dot(x, y, 2.0) if i % 2 == 0 else sq(x - 1.9, y - 1.9, 3.8, 3.8, 0.6))
    return out


@icon("port-forwarding", CAT, "Router box with two antennas and an arrow leading from it to a small door on the right",
      tags=["port forwarding", "nat", "open port", "router rule", "network redirect", "firewall rule", "home server access"])
def _(S):
    return [shell(rect(2, 13, 11, 7, min(S.R, 2))), line(seg(5, 13, 5, 8)), line(seg(10, 13, 10, 8)),
            dot(5.5, 16.5, 0.8), dot(8.5, 16.5, 0.8),
            line(seg(13, 16.5, 14.8, 16.5)), head(S, (16, 16.5), 0, 2.2),
            shell(rect(17, 6, 5, 14, min(S.R, 2))), dot(19.5, 13.5, 0.7)]


@icon("traffic-surge", CAT, "Server rack with three arrows pressing in from the left and a zigzag heat line above it",
      tags=["traffic surge", "traffic spike", "load spike", "viral traffic", "overload", "ddos", "high demand"])
def _(S):
    out = [shell(rect(12, 6, 10, 6, min(S.R, 2))), shell(rect(12, 14, 10, 6, min(S.R, 2))),
           dot(15, 9, 0.8), dot(15, 17, 0.8),
           line(poly([(13, 3.5), (15, 1.8), (17, 3.5), (19, 1.8), (21, 3.5)], r=0))]
    for y in (6.5, 12, 17.5):
        out += [line(seg(2, y, 7.5, y)), head(S, (8.5, y), 0, 2.2)]
    return out


# ============================================================================ behaviour, security and advertising

def shield_d(cx, top, w, h, flat=False):
    """Shield outline path (top point/flat, curved sides to a bottom point)."""
    x0, x1 = cx - w / 2, cx + w / 2
    sh = top + h * 0.27
    return (f"M{fmt(cx)} {fmt(top)}L{fmt(x1)} {fmt(top + h * 0.12)}V{fmt(sh + h * 0.2)}C{fmt(x1)} {fmt(top + h * 0.78)} {fmt(cx + w * 0.2)} {fmt(top + h * 0.92)} {fmt(cx)} {fmt(top + h)}"
            f"C{fmt(cx - w * 0.2)} {fmt(top + h * 0.92)} {fmt(x0)} {fmt(top + h * 0.78)} {fmt(x0)} {fmt(sh + h * 0.2)}V{fmt(top + h * 0.12)}Z")


def house(S, x0, x1, ytop, ybot, role=shell):
    xm = (x0 + x1) / 2
    return role(poly([(x0, ybot), (x0, ytop + (x1 - x0) / 2 + 0.5), (xm, ytop), (x1, ytop + (x1 - x0) / 2 + 0.5), (x1, ybot)], closed=True, r=S.r * 0.5))


def wifi(S, cx, cy, radii=(3.2, 6.0), role=line):
    return [dot(cx, cy, 1.2)] + [role(arc(cx, cy, r_, -135, -45)) for r_ in radii]


@icon("digital-divide", CAT, "Two houses side by side with a dashed gap between them, only the left one with a wifi signal above",
      tags=["digital divide", "internet access gap", "connectivity gap", "rural internet", "inequality", "have and have not", "broadband gap"])
def _(S):
    return [house(S, 2, 9.5, 11, 21), house(S, 14.5, 22, 11, 21),
            *wifi(S, 5.75, 8, (2.8, 5.2)),
            line(seg(12, 11.5, 12, 14.5)), line(seg(12, 17.5, 12, 21))]


@icon("internet-shutdown", CAT, "Globe with a power plug pulled away from its wall socket beside it",
      tags=["internet shutdown", "internet blackout", "network outage", "disconnected", "unplugged", "cut off", "censorship blackout"])
def _(S):
    return globe(S, 8, 12, 6, mer=True, eq=True) + [
        sq(15, 2, 7, 3.4, 1.0),
        shell(rect(15, 10, 7, 6, min(S.R, 2))), line(seg(17, 10, 17, 7.6)), line(seg(20, 10, 20, 7.6)),
        line(seg(18.5, 16, 18.5, 21))]


@icon("web-surfing", CAT, "Surfboard riding a wave with a small arrow cursor above it",
      tags=["web surfing", "surf the web", "browsing", "internet surfing", "net surfing", "wave", "surfboard"])
def _(S):
    return [shell("M4 15Q11 10.6 20 9.4Q13 14.6 4 15Z"), cursor(S, 9.6, 2.2, 0.75),
            line("M2 19.4Q5 16.6 8 19.4T14 19.4T20 19.4")]


@icon("doomscrolling", CAT, "Smartphone with a weary face on the first feed card, more cards below and a long down arrow beside it",
      tags=["doomscrolling", "endless scroll", "infinite feed", "bad news scrolling", "social media addiction", "phone addiction", "scrolling"])
def _(S):
    return [shell(rect(3, 2, 12, 20, min(S.R, 3))),
            dot(7, 7.5, 0.9), dot(11, 7.5, 0.9), detail(arc(9, 12.6, 2.2, 215, 325)),
            detail(seg(3, 16.2, 15, 16.2)), detail(seg(6, 19.4, 12, 19.4)),
            line(seg(19.5, 4, 19.5, 17.5)), head(S, (19.5, 19), 90, 2.6)]


@icon("online-voting", CAT, "Browser window with a ballot paper dropping into a ballot box in the page",
      tags=["online voting", "e voting", "electronic voting", "internet ballot", "digital election", "ballot box", "cast vote"])
def _(S):
    return win(S, 2, 2, 20, 20, 4.5) + [
        detail(poly([(9, 13.6), (9, 8.6), (15, 8.6), (15, 13.6)], r=0)),
        detail(rect(5.5, 13.6, 13, 6, 1)), detail(seg(9, 11.2, 12, 11.2))]


@icon("online-auction", CAT, "Browser window with an auction gavel striking its sound block in the page",
      tags=["online auction", "bidding", "gavel", "bid now", "auction site", "sold", "winning bid"])
def _(S):
    a = math.radians(-40)
    cx, cy = 10.5, 11.2
    hw, hh = 4.2, 2.2
    pts = [(cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a)) for dx, dy in ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh))]
    ha = a + math.pi / 2
    return win(S, 2, 2, 20, 20, 4.5) + [
        detail(poly(pts, closed=True, r=0)), detail(seg(cx, cy, cx + 5.6 * math.cos(ha), cy + 5.6 * math.sin(ha))),
        detail(seg(11, 19, 19, 19))]


@icon("cross-site-scripting", CAT, "Browser window with angle brackets and a slash typed into an input field",
      tags=["xss", "cross site scripting", "script injection", "code injection", "html injection", "vulnerability", "security flaw"])
def _(S):
    return win(S, 2, 2, 20, 20, 4.5) + [
        detail(rect(4, 10, 16, 8.5, 1.5)),
        detail(poly([(9.6, 12.2), (7.4, 14.2), (9.6, 16.2)], r=0)), detail(poly([(14.4, 12.2), (16.6, 14.2), (14.4, 16.2)], r=0)),
        detail(seg(11, 16, 13, 12.4))]


@icon("web-application-firewall", CAT, "Shield with a brick pattern across it",
      tags=["waf", "web application firewall", "application security", "request filtering", "shield", "brick wall", "protect website"])
def _(S):
    return [shell(shield_d(12, 2.2, 17, 19.6)),
            detail(seg(5, 9.5, 19, 9.5)), detail(seg(5.5, 14.2, 18.5, 14.2)),
            detail(seg(12, 9.5, 12, 14.2)), detail(seg(8.5, 14.2, 8.5, 18.4)), detail(seg(15.5, 14.2, 15.5, 18.4))]


@icon("typosquatting", CAT, "Address bar with a text line and a mismatched character, a fishing hook hanging from its end",
      tags=["typosquatting", "lookalike domain", "misspelled url", "url hijacking", "fake domain", "phishing link", "typo domain"])
def _(S):
    return [shell(rect(2, 2.5, 20, 7, L(S, 2, 3.5))), detail(seg(5.5, 6, 10, 6)), detail(circle(12.8, 6.2, 1.0)), dot(16, 6, 0.9),
            line("M17.5 9.5V16A3 3 0 0 1 11.5 16V14.5"), line(poly([(11.5, 14.5), (13, 16.4)], r=0))]


@icon("content-security-policy", CAT, "Browser window with a small shield on the left and three ticked lines on the right",
      tags=["csp", "content security policy", "allowlist", "script policy", "http header", "web security", "approved sources"])
def _(S):
    out = win(S, 2, 2, 20, 20, 4.5) + [detail(shield_d(8, 9, 7, 9.8))]
    for y in (10.6, 14.4, 18.2):
        out += [detail(poly([(13.5, y), (14.7, y + 1.2), (16.6, y - 1.1)], r=0)), detail(seg(18.4, y, 19.4, y))]
    return out


@icon("website-defacement", CAT, "Browser window with a spray can and a scribbled squiggle across the page",
      tags=["defacement", "website hacked", "graffiti", "spray paint", "vandalism", "hacked site", "web attack"])
def _(S):
    return win(S, 2, 2, 20, 20, 4.5) + [
        detail("M4.5 18Q6 11.5 8 15.6T11 14.5"),
        detail(rect(14.5, 12.2, 5, 7.8, 0.8)), sq(15.8, 9.8, 2.4, 2, 0.4),
        dot(12.8, 10.4, 0.6), dot(11.6, 12.2, 0.6)]


@icon("dark-pattern", CAT, "Dialog box with a large solid accept button and a tiny close cross tucked in the corner",
      tags=["dark pattern", "deceptive design", "manipulative ui", "sneaky button", "trick design", "confirmshaming", "hidden close"])
def _(S):
    return [shell(rect(2, 3, 20, 18, min(S.R, 3))), line(seg(18.8, 5.4, 20.2, 6.8)), line(seg(20.2, 5.4, 18.8, 6.8)), detail(seg(5, 8, 13, 8)),
            sq(5, 12, 14, 5, 1.5)]


@icon("interstitial-ad", CAT, "Browser window fully covered by an ad panel with a small countdown ring and two text lines",
      tags=["interstitial ad", "full page ad", "popup ad", "splash ad", "skip ad", "countdown", "overlay ad"])
def _(S):
    return win(S, 2, 2, 20, 20, 4.5) + [
        detail(rect(4.5, 9, 15, 10, 1)), detail(seg(7, 12.4, 11.5, 12.4)), detail(seg(7, 15.6, 10.5, 15.6)), detail(circle(15.6, 14, 2.2))]


@icon("skyscraper-ad", CAT, "Browser window with a tall narrow solid ad down the right side beside lines of text",
      tags=["skyscraper ad", "tall banner", "sidebar ad", "vertical banner", "display ad", "banner advertising", "ad unit"])
def _(S):
    return win(S, 2, 2, 20, 20, 4.5) + [
        sq(16, 8.5, 3.8, 10.5, 0.6), detail(seg(5, 10, 12, 10)), detail(seg(5, 13.5, 12, 13.5)), detail(seg(5, 17, 10, 17))]


@icon("pay-per-click", CAT, "Arrow cursor clicking on a coin",
      tags=["pay per click", "ppc", "cost per click", "click ad", "advertising cost", "search ads", "paid clicks"])
def _(S):
    return [shell(circle(15.4, 15.4, 6.2)), detail(circle(15.4, 15.4, 2.6)), cursor(S, 2.5, 2.5, 0.95)]



@icon("retargeting-ad", CAT, "Person silhouette and an ad card joined by a curved arrow that loops back over the top",
      tags=["retargeting", "remarketing", "follow up ad", "ad tracking", "ad loop", "returning visitor", "audience ads"])
def _(S):
    return [dot(6, 13, 1.9), line("M2.6 20.6V19.8A3.4 3.4 0 0 1 9.4 19.8V20.6"),
            shell(rect(13.5, 11.5, 8.5, 9, min(S.R, 2))), detail(seg(15.8, 16, 19.7, 16)),
            line("M18 9C18 2.5 6 2.5 6 8.6"), head(S, (6, 9.2), 90, 2.4)]


@icon("ad-network", CAT, "Central node linked by lines to four small browser windows, each holding a solid ad block",
      tags=["ad network", "advertising network", "ad exchange", "publisher network", "ad platform", "display network", "ad serving"])
def _(S):
    out = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            wx, wy = 12 + sx * 6.9, 12 + sy * 7.2
            ang = math.atan2(wy - 12, wx - 12)
            p0 = (12 + 3.4 * math.cos(ang), 12 + 3.4 * math.sin(ang))
            p1 = (wx - 3.8 * math.cos(ang), wy - 3.6 * math.sin(ang))
            out += [line(seg(p0[0], p0[1], p1[0], p1[1])),
                    shell(rect(wx - 4, wy - 3.2, 8, 6.4, min(S.R, 1.4))), sq(wx - 2, wy - 1.0, 4, 2.0, 0.3)]
    out.append(dot(12, 12, 2.2))
    return out


@icon("clickbait", CAT, "Headline card with a hook dangling on a line above it and a big exclamation mark beside the hook",
      tags=["clickbait", "sensational headline", "bait", "misleading title", "hook", "exclamation", "shocking news"])
def _(S):
    return [line(seg(7, 2.5, 7, 8.5)), dot(7, 11.5, 1.4),
            line("M17 1.5V8A3 3 0 0 1 11 8V6.5"), line(poly([(11, 6.5), (12.6, 8.2)], r=0)),
            shell(rect(2, 14.5, 20, 7, min(S.R, 2.5))), detail(seg(5.5, 18, 18.5, 18))]


def cookie_d(cx, cy, r):
    base = P(circle_d(cx, cy, r))
    bite = P(circle_d(cx + r * 0.78, cy - r * 0.78, r * 0.38))
    return path_to_d(D(base, bite))


@icon("cookie-wall", CAT, "Cookie with a bite taken out standing above a brick wall",
      tags=["cookie wall", "cookie consent wall", "consent gate", "accept cookies", "tracking consent", "gdpr banner", "cookie banner"])
def _(S):
    return [shell(cookie_d(12, 8, 6.2)), dot(9.6, 8.2, 0.9), dot(12.6, 11, 0.9), dot(12, 5.4, 0.8),
            shell(rect(2, 16, 20, 5.5, min(S.R, 1.5))),
            detail(seg(9.5, 16, 9.5, 18.7)), detail(seg(16.5, 16, 16.5, 18.7)), detail(seg(13, 18.7, 13, 21.5))]


@icon("paywall", CAT, "Browser window with two text lines above and a brick wall with a coin slot across its lower half",
      tags=["paywall", "subscription wall", "premium content", "pay to read", "metered access", "locked article", "subscribe to continue"])
def _(S):
    return win(S, 2, 2, 20, 20, 4.5) + [
        detail(seg(5, 10, 19, 10)),
        detail(seg(2, 13.5, 22, 13.5)), detail(seg(2, 17.5, 22, 17.5)),
        detail(seg(8, 13.5, 8, 17.5)), detail(seg(16, 13.5, 16, 17.5)), detail(seg(12, 17.5, 12, 22)),
        sq(9.8, 15, 4.4, 1.0, 0.4)]


@icon("members-area", CAT, "Browser window with a membership card showing a star and a small avatar",
      tags=["members area", "member portal", "membership", "vip area", "private section", "members only", "subscriber zone"])
def _(S):
    star = []
    for j in range(10):
        rr = 3.1 if j % 2 == 0 else 1.4
        star.append(polar(8.4, 14.2, rr, -90 + j * 36))
    return win(S, 2, 2, 20, 20, 4.5) + [
        detail(rect(4, 9.5, 16, 9.5, 1.5)), Part("dot", poly(star, closed=True)),
        dot(15.6, 12.9, 1.4), detail("M13.2 17V16.5A2.4 2.4 0 0 1 18 16.5V17")]


@icon("affiliate-link", CAT, "Chain link with a small coin attached to its lower right end",
      tags=["affiliate link", "referral link", "partner link", "commission", "affiliate marketing", "tracking link", "earn per sale"])
def _(S):
    return link(S, 9.5, 8.5, 0.9) + [shell(circle(17.4, 17, 4.2)), detail(circle(17.4, 17, 1.5))]


@icon("utm-tag", CAT, "Address bar with three small tags hanging from it on short strings",
      tags=["utm", "utm tag", "campaign tracking", "url parameters", "query string", "tracking code", "campaign link"])
def _(S):
    out = [shell(rect(2, 2.5, 20, 6.5, L(S, 2, 3.2))), detail(seg(5.5, 5.75, 15, 5.75))]
    for x in (6, 12, 18):
        out += [line(seg(x, 9, x, 12.4)),
                shell(poly([(x - 2.4, 12.4), (x + 2.4, 12.4), (x + 2.4, 18.6), (x, 21), (x - 2.4, 18.6)], closed=True, r=S.r * 0.4)),
                dot(x, 14.8, 0.7)]
    return out


@icon("deep-link", CAT, "Chain link above an arrow that dives into a stack of layered app screens",
      tags=["deep link", "app link", "universal link", "in app link", "direct link", "uri scheme", "open in app"])
def _(S):
    return link(S, 12, 4.8, 0.82) + [
        line(seg(12, 9.4, 12, 12.2)), head(S, (12, 13.6), 90, 2.4),
        line(seg(7, 15.4, 17, 15.4)), shell(rect(4, 17, 16, 4.5, min(S.R, 2)))]


@icon("jump-link", CAT, "Page with a solid hash sign at the top left and a curved arrow jumping down to a heading bar",
      tags=["jump link", "anchor link", "in page link", "fragment link", "skip to section", "hash link", "table of contents link"])
def _(S):
    return [shell(rect(2, 2, 20, 20, S.R)),
            sq(6, 4.6, 1.8, 7.6, 0.4), sq(10.6, 4.6, 1.8, 7.6, 0.4), sq(4.4, 6.4, 9.6, 1.8, 0.4), sq(4.4, 9.6, 9.6, 1.8, 0.4),
            detail("M15.5 7C19.5 7 19.5 13.6 15.5 15.6"), head(S, (15, 15.8), 150, 2.2, detail),
            sq(5, 16.8, 8, 2.4, 0.5)]


@icon("link-building", CAT, "Small rising wall of solid bricks with a chain link resting on top",
      tags=["link building", "backlinks", "seo links", "earn links", "outreach", "wall of links", "off page seo"])
def _(S):
    out = link(S, 12, 5.6, 0.8)
    for x in (2, 9.1, 16.2):
        out.append(sq(x, 17.3, 5.8, 4, 0.5))
    for x in (5.55, 12.65):
        out.append(sq(x, 12.2, 5.8, 4, 0.5))
    return out


@icon("anchor-text", CAT, "Line of text with one underlined word and a chain link above that word",
      tags=["anchor text", "link text", "clickable text", "hyperlink label", "underlined word", "seo anchor", "link wording"])
def _(S):
    return link(S, 13.5, 6, 0.8) + [
        line(seg(2, 14, 7, 14)), line(seg(10, 14, 17, 14)), line(seg(19.5, 14, 22, 14)),
        line(seg(10, 18.4, 17, 18.4))]


@icon("internal-links", CAT, "Browser window with three small page blocks joined to each other by a link path",
      tags=["internal links", "site links", "page to page links", "interlinking", "link structure", "navigation links", "seo links"])
def _(S):
    return win(S, 2, 2, 20, 20, 4.5) + [
        sq(4.4, 9.4, 4.6, 3.6, 0.6), sq(15, 9.4, 4.6, 3.6, 0.6), sq(9.7, 16.4, 4.6, 3.6, 0.6),
        line(seg(9, 11.2, 15, 11.2)), line("M6.7 13V18.2H9.7"), line("M14.3 18.2H17.3V13")]


@icon("toxic-link", CAT, "Chain link above a small skull",
      tags=["toxic link", "bad backlink", "spam link", "harmful link", "dangerous url", "malicious link", "link penalty"])
def _(S):
    skull = "M7.7 16A4.3 4.3 0 1 1 16.3 16V18.4H14.5V20.8H9.5V18.4H7.7Z"
    return link(S, 12, 5, 0.85) + [shell(skull), dot(10.2, 15.9, 1.0), dot(13.8, 15.9, 1.0)]


@icon("link-equity", CAT, "Chain link with a water drop falling from it onto a small page below",
      tags=["link equity", "link juice", "page authority", "seo value", "passing value", "link strength"])
def _(S):
    drop = "M12 9.8C13.6 11.8 14.4 12.8 14.4 13.8A2.4 2.4 0 0 1 9.6 13.8C9.6 12.8 10.4 11.8 12 9.8Z"
    page = poly([(6.5, 21.5), (6.5, 16.6), (14.5, 16.6), (17.5, 19.2), (17.5, 21.5)], closed=True, r=S.r * 0.4)
    return link(S, 12, 4.2, 0.85) + [Part("dot", drop), shell(page)]


@icon("link-farm", CAT, "Three upright chain loops on stems growing from a ground line like crops",
      tags=["link farm", "spam links", "link scheme", "pbn", "black hat seo", "bulk links", "crop of links"])
def _(S):
    out = [line(seg(2, 20.2, 22, 20.2))]
    for x, top in ((5, 8.6), (12, 3.4), (19, 7)):
        out += [shell(rect(x - 2, top, 4, 7.6, 2)), line(seg(x, top + 7.6, x, 20.2))]
    return out


@icon("link-exchange", CAT, "Two pages at opposite corners with two curved arrows swapping between them",
      tags=["link exchange", "reciprocal links", "link swap", "partner links", "trade links", "two way links", "link trading"])
def _(S):
    return [shell(rect(2, 3, 7, 10, min(S.R, 2))), detail(seg(4, 7, 7, 7)), detail(seg(4, 10, 6.2, 10)),
            shell(rect(15, 11, 7, 10, min(S.R, 2))), detail(seg(17, 15, 20, 15)), detail(seg(17, 18, 19.2, 18)),
            line("M10.5 6.5C15 4.2 18.5 5.6 18.5 8.6"), head(S, (18.5, 9.4), 90, 2.4),
            line("M13.5 17.5C9 19.8 5.5 18.4 5.5 15.4"), head(S, (5.5, 14.6), -90, 2.4)]


@icon("canonical-url", CAT, "Three small page tabs with arrows pointing to one main page that wears a crown",
      tags=["canonical url", "canonical tag", "preferred url", "duplicate content", "master page", "rel canonical", "original source"])
def _(S):
    out = [Part("solid", poly([(12.5, 5), (12.5, 2.2), (14.7, 3.8), (17, 1.8), (19.3, 3.8), (21.5, 2.2), (21.5, 5)], closed=True, r=0)),
           shell(rect(12.5, 7, 9.5, 14, min(S.R, 2))), detail(seg(15.5, 12, 19, 12)), detail(seg(15.5, 15.5, 19, 15.5))]
    for y in (8.2, 14, 19.8):
        out += [sq(2, y - 1.6, 4.4, 3.2, 0.5), line(seg(7.6, y, 9.4, y)), head(S, (10.8, y), 0, 2.0)]
    return out


@icon("redirect-chain", CAT, "Three pages in a row joined by two curved arrows hopping from one to the next",
      tags=["redirect chain", "multiple redirects", "301 chain", "hops", "redirect hops", "forwarding chain", "url redirects"])
def _(S):
    out = []
    for x in (2.5, 9.5, 16.5):
        out.append(shell(rect(x, 14.5, 5, 6.5, 1.0)))
    out += [line("M5 12.6Q8.6 5 12 12.6"), head(S, (12, 12.8), 75, 2.2),
            line("M12 12.6Q15.6 5 19 12.6"), head(S, (19, 12.8), 75, 2.2)]
    return out


@icon("redirect-loop", CAT, "Two small pages facing each other joined by two curved arrows that form an endless circle",
      tags=["redirect loop", "infinite redirect", "too many redirects", "circular redirect", "err too many redirects", "endless loop", "bounce"])
def _(S):
    cx, cy, r = 12, 12, 8.4
    out = [shell(rect(2, 9.5, 4.6, 5.5, 1.0)), shell(rect(17.4, 9.5, 4.6, 5.5, 1.0)),
           line(arc(cx, cy, r, 212, 330)), head(S, polar(cx, cy, r, 330), 60, 2.4),
           line(arc(cx, cy, r, 32, 150)), head(S, polar(cx, cy, r, 150), 240, 2.4)]
    return out
