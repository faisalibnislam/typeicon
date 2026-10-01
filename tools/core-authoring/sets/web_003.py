"""TypeIcon Core: web (batch 003): accessibility, performance, CMS, page layout, design process and forms."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import circle_d, fmt, polar

CAT = "web"


def L(S, sharp, soft):
    return sharp if S.name == "line" else soft


def win(S, x, y, w, h, bar=4.5, cap=None):
    """Browser window: outline plus a title bar line."""
    return [shell(rect(x, y, w, h, S.R if cap is None else min(S.R, cap))), detail(seg(x, y + bar, x + w, y + bar))]


def head(S, tip, deg, size=3.0, role=line):
    """Open arrowhead whose tip is at `tip`, pointing along `deg` (0 = right, 90 = down)."""
    pts = []
    for s in (-1, 1):
        a = math.radians(deg + 180 + s * 40)
        pts.append((tip[0] + size * math.cos(a), tip[1] + size * math.sin(a)))
    return role(poly([pts[0], tip, pts[1]], r=S.r * 0.5))


def arrow(S, x1, y1, x2, y2, size=3.0, role=line):
    deg = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return [role(seg(x1, y1, x2, y2)), head(S, (x2, y2), deg, size, role)]


def cyc(S, cx, cy, r, a0, a1, role=line, size=2.8):
    """Circular arrow: clockwise arc from a0 to a1 degrees with a head at the end."""
    tip = polar(cx, cy, r, a1)
    return [role(arc(cx, cy, r, a0, a1)), head(S, tip, a1 + 90, size, role)]


def cursor(S, x, y, k=1.0):
    pts = [(0, 0), (0, 8), (2, 6.25), (3.4, 9.2), (5.1, 8.4), (3.75, 5.5), (6.25, 5.5)]
    return Part("dot", poly([(x + px * k, y + py * k) for px, py in pts], closed=True, r=L(S, 0, 0.5)))


def corners(x, y, w, h, n=3.0):
    """Four corner brackets (a focus or frame marker); returns one d string."""
    return (f"M{fmt(x)} {fmt(y + n)}V{fmt(y)}H{fmt(x + n)}M{fmt(x + w - n)} {fmt(y)}H{fmt(x + w)}V{fmt(y + n)}"
            f"M{fmt(x + w)} {fmt(y + h - n)}V{fmt(y + h)}H{fmt(x + w - n)}M{fmt(x + n)} {fmt(y + h)}H{fmt(x)}V{fmt(y + h - n)}")


def rot(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rrect_pts(cx, cy, w, h, deg):
    return rot([(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)], deg, cx, cy)


def eye_d(cx, cy, hw, hh, S):
    if S.name == "line":
        return f"M{fmt(cx - hw)} {fmt(cy)}Q{fmt(cx)} {fmt(cy - 2 * hh)} {fmt(cx + hw)} {fmt(cy)}Q{fmt(cx)} {fmt(cy + 2 * hh)} {fmt(cx - hw)} {fmt(cy)}Z"
    k = hw * 0.4
    return (f"M{fmt(cx - hw)} {fmt(cy)}C{fmt(cx - hw + k)} {fmt(cy - hh * 1.3)} {fmt(cx - k)} {fmt(cy - hh)} {fmt(cx)} {fmt(cy - hh)}"
            f"S{fmt(cx + hw - k)} {fmt(cy - hh * 1.3)} {fmt(cx + hw)} {fmt(cy)}"
            f"C{fmt(cx + hw - k)} {fmt(cy + hh * 1.3)} {fmt(cx + k)} {fmt(cy + hh)} {fmt(cx)} {fmt(cy + hh)}"
            f"S{fmt(cx - hw + k)} {fmt(cy + hh * 1.3)} {fmt(cx - hw)} {fmt(cy)}Z")


def gauge_arc(cx, cy, r, role=detail):
    return role(f"M{fmt(cx - r)} {fmt(cy)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx + r)} {fmt(cy)}")


def pagebox(S, x, y, w, h):
    return shell(rect(x, y, w, h, min(S.R, 3)))


# ============================================================================ accessibility

@icon("search-penalty", CAT, "Search result page with a downward arrow and a gavel beside it",
      tags=["seo penalty", "ranking drop", "demoted", "search ranking", "sanction", "deindexed"])
def _(S):
    hd = poly(rrect_pts(18, 16, 7, 4, 45), closed=True, r=S.r * 0.5)
    return [
        pagebox(S, 2, 3, 10, 18),
        detail(seg(5, 8, 9, 8)), detail(seg(5, 12, 9, 12)), detail(seg(5, 16, 7.5, 16)),
        *arrow(S, 18, 2.5, 18, 9, 2.8),
        shell(hd),
        line(seg(16.4, 17.7, 13.8, 20.3)),
    ]


@icon("seo-cloaking", CAT, "Page with a theatre mask on top and a robot and a person below",
      tags=["cloaking", "black hat seo", "hidden content", "deceptive", "bot vs human", "seo", "spam"])
def _(S):
    mask = L(S, "M7 5.5H17V9L14.5 12H9.5L7 9Z", "M7 5.5H17V9.5Q17 12 12 12Q7 12 7 9.5Z")
    return [
        shell(rect(3, 2.5, 18, 19, min(S.R, 3))),
        detail(mask),
        dot(9.8, 8, 0.9), dot(14.2, 8, 0.9),
        detail(seg(3, 14.5, 21, 14.5)),
        Part("dot", rect(6, 16.5, 4, 3, L(S, 0, 0.8))),
        dot(16.5, 17.5, 1.7),
    ]


@icon("alt-text", CAT, "Image frame with a mountain and sun and two caption lines below",
      tags=["alt attribute", "image description", "screen reader", "accessible image", "caption", "alternative text"])
def _(S):
    return [
        shell(rect(2, 3, 20, 11, min(S.R, 3))),
        detail(poly([(2, 12), (8, 7.5), (12, 11), (15, 8.5), (22, 13)], r=S.r)),
        dot(16.5, 6.8, 1.1),
        line(seg(2, 18, 22, 18)),
        line(seg(2, 21, 14, 21)),
    ]


@icon("aria-label", CAT, "Button shape with a small tag tied to its corner by a string",
      tags=["aria", "accessible name", "label attribute", "screen reader label", "wai-aria", "accessibility tag"])
def _(S):
    return [
        shell(rect(2, 3, 15, 9, S.R)),
        detail(seg(6, 7.5, 13, 7.5)),
        line("M10 12Q10 18 14.5 18"),
        shell(poly([(14.5, 18), (17, 15.2), (22, 15.2), (22, 20.8), (17, 20.8)], closed=True, r=S.r * 0.7)),
    ]


@icon("contrast-ratio", CAT, "Outlined square overlapped by a solid square, with a colon mark beside them",
      tags=["color contrast", "wcag contrast", "legibility", "light and dark", "contrast checker", "ratio"],
      filled=lambda: U(D(P(rect(2, 2, 12, 12)), P(rect(8.5, 8.5, 15, 15))), P(rect(10, 10, 12, 12)), P(circle(19, 4, 1.25)), P(circle(19, 8, 1.25))))
def _(S):
    return [
        line(f"M7.5 14H2V2H14V7.5"),
        Part("solid", rect(10, 10, 12, 12, S.R * 0.5)),
        dot(19, 4, 1.25), dot(19, 7.5, 1.25),
    ]


@icon("keyboard-navigation", CAT, "Key with a tab arrow inside and focus brackets around it",
      tags=["tab key", "focus ring", "keyboard accessible", "keyboard only", "focus order", "tabindex"])
def _(S):
    return [
        shell(rect(6, 6, 12, 12, min(S.R, 3))),
        detail(seg(8.8, 12, 14, 12)), detail(poly([(12, 9.5), (14.5, 12), (12, 14.5)], r=S.r * 0.4)),
        line(corners(2, 2, 20, 20, 3.5)),
    ]


@icon("dyslexic-font", CAT, "Letters b and a with heavy weighted bottoms on a baseline",
      tags=["dyslexia friendly", "readable font", "weighted letters", "reading aid", "typeface", "accessible typography"])
def _(S):
    return [
        line(seg(5.5, 3, 5.5, 15)),
        line(circle(8.5, 11.5, 3)),
        line(circle(17.5, 11.5, 3)), line(seg(20.5, 8.5, 20.5, 15)),
        Part("solid", rect(2.5, 16, 8.5, 3.2, L(S, 0, 1.2))),
        Part("solid", rect(14, 16, 8, 3.2, L(S, 0, 1.2))),
    ]


@icon("reduced-motion", CAT, "Three horizontal speed lines ending beside a pause symbol",
      tags=["prefers reduced motion", "no animation", "stop motion", "vestibular", "pause animation", "calm"])
def _(S):
    return [
        line(seg(2, 8, 7.5, 8)), line(seg(2, 12, 9, 12)), line(seg(2, 16, 7.5, 16)),
        shell(circle(16, 12, 6.5)),
        detail(seg(14, 9.5, 14, 14.5)), detail(seg(18, 9.5, 18, 14.5)),
    ]


@icon("colorblind-mode", CAT, "Eye whose iris is split into a solid half and an outlined half",
      tags=["color blind", "colour blindness", "daltonism", "accessible colours", "vision deficiency", "color vision"])
def _(S):
    return [
        shell(eye_d(12, 12, 10, 5.5, S)),
        detail(circle(12, 12, 4)),
        Part("dot", "M12 8A4 4 0 0 0 12 16Z"),
    ]


@icon("semantic-html", CAT, "Page outline split into a header bar, a nav strip, a main area and a footer bar",
      tags=["html5 elements", "page structure", "landmarks", "header footer", "markup", "document outline"])
def _(S):
    return [
        shell(rect(3, 2, 18, 20, min(S.R, 3))),
        detail(seg(3, 6.5, 21, 6.5)), detail(seg(3, 17.5, 21, 17.5)), detail(seg(9, 6.5, 9, 17.5)),
        detail(seg(12.5, 10.5, 17.5, 10.5)), detail(seg(12.5, 13.5, 16, 13.5)),
    ]


@icon("switch-access", CAT, "Large round push button on a flat base with a cable running off to the side",
      tags=["big button", "adaptive switch", "assistive switch", "single switch", "motor impairment", "press button"])
def _(S):
    return [
        shell(L(S, "M8 15C8 6.5 20 6.5 20 15Z", "M8 15C8 8 10 6 14 6S20 8 20 15Z")),
        shell(rect(6, 15, 16, 6, min(S.R, 2.5))),
        line(poly([(6, 18), (2.5, 18), (2.5, 10)], r=S.r)),
    ]


@icon("screen-magnifier", CAT, "Monitor with a magnifying glass over a letter on the screen",
      tags=["zoom screen", "enlarge text", "low vision", "magnification", "screen zoom", "accessibility zoom"])
def _(S):
    return [
        shell(rect(2, 3, 20, 14, min(S.R, 3))),
        line(seg(12, 17, 12, 21)), line(seg(8, 21, 16, 21)),
        detail(circle(10.5, 10, 4)), detail(seg(13.5, 13, 16.5, 15.5)),
        dot(10.5, 10, 1.1),
    ]


@icon("accessibility-audit", CAT, "Clipboard with a small standing figure and arms outstretched",
      tags=["a11y audit", "wcag check", "accessibility review", "compliance test", "checklist", "inspection"])
def _(S):
    return [
        shell(rect(4, 4, 16, 18, S.R)),
        shell(rect(9, 2, 6, 4, min(S.R, 1.5))),
        dot(12, 10, 1.5), detail(seg(8, 13, 16, 13)),
        detail(poly([(10, 19), (12, 13.5), (14, 19)], r=S.r)),
    ]


@icon("readability-score", CAT, "Page with text lines and a half-circle gauge at the bottom",
      tags=["reading level", "reading score", "plain language", "text complexity", "copy grade", "legibility"])
def _(S):
    return [
        shell(rect(3, 2, 18, 20, min(S.R, 3))),
        detail(seg(7, 6.5, 17, 6.5)), detail(seg(7, 10, 14, 10)),
        gauge_arc(12, 19, 5), detail(seg(12, 19, 14.5, 15.8)),
    ]


@icon("focus-trap", CAT, "Dialog box with corner brackets and a circular arrow cycling inside",
      tags=["modal focus", "tab loop", "dialog accessibility", "keyboard trap", "focus lock", "cycle focus"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, S.R)),
        *cyc(S, 12, 12, 4.5, -50, 225, detail, 2.6),
    ]


@icon("braille-display", CAT, "Flat bar with raised dot cells across the top and small keys along the front edge",
      tags=["refreshable braille", "braille reader", "tactile display", "blind", "assistive device", "braille cells"])
def _(S):
    return [
        shell(rect(2, 4.5, 20, 10.5, S.R)),
        dot(5.2, 8.5, 1), dot(7.6, 11.5, 1), dot(10.8, 8.5, 1), dot(10.8, 11.5, 1), dot(14.5, 8.5, 1),
        dot(14.5, 11.5, 1), dot(17.7, 8.5, 1), dot(19.9, 11.5, 1),
        Part("solid", rect(3.5, 18, 3.5, 3, L(S, 0, 0.8))), Part("solid", rect(10.25, 18, 3.5, 3, L(S, 0, 0.8))),
        Part("solid", rect(17, 18, 3.5, 3, L(S, 0, 0.8))),
    ]


@icon("eye-gaze-control", CAT, "Eye with a dotted line from its pupil down to a cursor on a monitor",
      tags=["eye tracking", "gaze input", "look to click", "hands free", "assistive control", "eye mouse"])
def _(S):
    return [
        shell(eye_d(12, 5.5, 8, 3.4, S)),
        dot(12, 5.5, 1.5),
        dot(12, 10.2, 0.9), dot(12, 12.6, 0.9),
        shell(rect(2, 14, 20, 8, min(S.R, 2.5))),
        cursor(S, 10.5, 15.8, 0.45),
    ]


@icon("audio-captcha", CAT, "Verification box with an empty checkbox, a speaker and a sound wave",
      tags=["captcha audio", "accessible captcha", "listen challenge", "human check", "spoken code", "verify human"])
def _(S):
    spk = poly([(12, 10.5), (13.8, 10.5), (16.2, 8.3), (16.2, 15.7), (13.8, 13.5), (12, 13.5)], closed=True, r=L(S, 0, 0.4))
    return [
        shell(rect(2, 4, 20, 16, S.R)),
        detail(rect(5, 9.5, 5, 5, L(S, 0, 1))),
        Part("dot", spk),
        detail(arc(15.5, 12, 3.4, -40, 40)),
    ]


@icon("web-vitals", CAT, "Three small half-circle gauges with needles at different angles",
      tags=["core web vitals", "lcp", "cls", "page experience", "performance metrics", "speed gauges"])
def _(S):
    out = []
    for cx, cy, a in ((6.5, 7.5, 200), (17.5, 7.5, 290), (12, 17.5, 340)):
        out += [shell(circle(cx, cy, 3.6)), detail(seg(cx, cy, *polar(cx, cy, 2.6, a)))]
    return out


@icon("layout-shift", CAT, "Solid content block with a dashed ghost copy below it and a downward arrow",
      tags=["cls", "content jump", "page jank", "visual stability", "shifting layout", "reflow"])
def _(S):
    return [
        shell(rect(2.5, 3, 13, 6.5, min(S.R, 2.5))),
        line(corners(2.5, 12.5, 13, 8, 3)),
        *arrow(S, 20, 4.5, 20, 19.5, 3.2),
    ]


@icon("lazy-loading", CAT, "Page with a solid image block at the top and dashed empty placeholders below it",
      tags=["deferred images", "load on scroll", "placeholder", "defer loading", "performance", "images below the fold"])
def _(S):
    return [
        shell(rect(3, 2, 18, 20, min(S.R, 3))),
        Part("dot", poly([(6.5, 10.5), (10.5, 5.5), (13, 8.2), (15, 6.5), (17.5, 10.5)], closed=True, r=L(S, 0, 0.5))),
        detail(corners(6.5, 13.5, 11, 5, 2)),
    ]


@icon("code-splitting", CAT, "Three separate code chunk blocks with gaps between them, each holding short code lines",
      tags=["chunking", "split bundle", "dynamic import", "bundle splitting", "lazy chunks", "bundler"])
def _(S):
    return [
        shell(rect(2, 3, 9, 8, min(S.R, 2.5))), detail(seg(5, 7, 8, 7)),
        shell(rect(2, 13, 9, 8, min(S.R, 2.5))), detail(seg(5, 17, 8, 17)),
        shell(rect(13, 3, 9, 18, min(S.R, 2.5))), detail(seg(16, 8, 19, 8)), detail(seg(16, 12, 19, 12)), detail(seg(16, 16, 19, 16)),
    ]


@icon("tree-shaking", CAT, "Small tree with a few leaves falling away from its branches",
      tags=["dead code", "unused code removal", "bundle optimisation", "dead code elimination", "shake", "prune"])
def _(S):
    return [
        shell(circle(9.5, 8.5, 6)),
        line(seg(9.5, 14.5, 9.5, 21)),
        detail(seg(9.5, 12, 9.5, 8)),
        line(seg(6, 21, 13, 21)),
        dot(19, 6, 1.4), dot(18, 12, 1.4), dot(21, 17, 1.4),
    ]


@icon("page-hydration", CAT, "Browser window with a water drop falling onto the page",
      tags=["hydrate", "ssr", "interactive page", "client rendering", "water drop", "server rendered"])
def _(S):
    drop = L(S, "M12 8.5L8.6 13.6A4 4 0 1 0 15.4 13.6Z", "M12 8.5C12 8.5 8.5 11.8 8.5 14.2A3.5 3.5 0 0 0 15.5 14.2C15.5 11.8 12 8.5 12 8.5Z")
    return [*win(S, 2, 3, 20, 18), detail(drop)]


@icon("performance-budget", CAT, "Wallet with a small speed gauge on its front",
      tags=["speed budget", "size limit", "load time limit", "web performance", "thresholds", "kb budget"])
def _(S):
    return [
        shell(rect(2, 5, 20, 15, S.R)),
        detail(rect(15.5, 10.5, 6.5, 5.5, 1)),
        gauge_arc(9, 16.5, 4.2), detail(seg(9, 16.5, 11.2, 13.8)),
    ]


@icon("http-compression", CAT, "Narrow file page squeezed between two clamp jaws with inward arrows",
      tags=["gzip", "brotli", "compressed response", "deflate", "transfer size", "squeeze"])
def _(S):
    return [
        line(seg(2.5, 5, 2.5, 19)), line(seg(21.5, 5, 21.5, 19)),
        head(S, (7, 12), 0, 2.4), head(S, (17, 12), 180, 2.4),
        line(seg(2.5, 12, 6.6, 12)), line(seg(21.5, 12, 17.4, 12)),
        shell(poly([(9.5, 4), (13.5, 4), (15.5, 6), (15.5, 20), (9.5, 20)], closed=True, r=S.r * 0.5)),
        detail(seg(12.5, 12, 12.5, 15)),
    ]


@icon("image-compression", CAT, "Large image frame with an arrow pointing to a smaller image frame",
      tags=["optimise images", "reduce image size", "shrink photo", "webp", "smaller file", "resize image"])
def _(S):
    return [
        shell(rect(2, 2, 14, 12, min(S.R, 3))),
        detail(poly([(2, 12), (7, 7.5), (10.5, 10.5), (12.5, 8.5), (16, 11.5)], r=S.r)),
        dot(11.5, 5.5, 1),
        shell(rect(16.5, 14.5, 5.5, 5.5, min(S.R, 1.5))),
        *arrow(S, 2.5, 19, 12.5, 19, 3),
    ]


@icon("page-cache", CAT, "Page standing in an open box with a small lightning bolt beside it",
      tags=["cached page", "static copy", "fast reload", "stored page", "full page cache", "speed"])
def _(S):
    return [
        line(poly([(5.5, 13), (5.5, 2.5), (11, 2.5), (14.5, 6), (14.5, 13)], r=S.r)),
        shell(rect(2.5, 13, 16, 8, min(S.R, 2.5))),
        line(poly([(20, 2.5), (17.5, 7.5), (21, 7.5), (18.5, 12.5)], r=S.r * 0.6)),
    ]


@icon("render-blocking-script", CAT, "Script tag block standing in front of a browser window like a barrier",
      tags=["blocking javascript", "slow script", "defer script", "async script", "page speed", "script tag"])
def _(S):
    return [
        line("M5 13H2V2H22V13H19"), line(seg(2, 6.5, 22, 6.5)),
        shell(rect(5, 12.5, 14, 9, min(S.R, 2.5))),
        detail(poly([(10, 15), (8.2, 17), (10, 19)], r=S.r * 0.5)),
        detail(poly([(14, 15), (15.8, 17), (14, 19)], r=S.r * 0.5)),
    ]


@icon("bundle-size", CAT, "Parcel box sitting on a small weighing scale",
      tags=["javascript size", "kilobytes", "weight of code", "package weight", "build output", "payload size"])
def _(S):
    return [
        shell(rect(6, 2.5, 12, 9.5, min(S.R, 2.5))),
        detail(seg(12, 2.5, 12, 6.5)),
        shell(rect(2.5, 14.5, 19, 7, min(S.R, 2.5))),
        dot(12, 18, 1.2),
    ]


@icon("dropped-frames", CAT, "Film strip with a solid frame on each side and a dashed empty frame between",
      tags=["frame drops", "jank", "stutter", "lag", "fps drop", "missing frame"])
def _(S):
    return [
        shell(rect(2, 5.5, 6, 13, min(S.R, 2.5))),
        line(corners(9.5, 5.5, 5, 13, 2.5)),
        shell(rect(16, 5.5, 6, 13, min(S.R, 2.5))),
    ]


# ============================================================================ content management and layout

def gear_pts(cx, cy, ro, ri, n):
    pts = []
    for i in range(n):
        a = 360 / n * i
        w = 360 / n
        for off, r in ((-0.30, ri), (-0.17, ro), (0.17, ro), (0.30, ri)):
            pts.append(polar(cx, cy, r, a + off * w))
    return pts


def star_pts(cx, cy, ro, ri):
    return [polar(cx, cy, ro if i % 2 == 0 else ri, -90 + i * 36) for i in range(10)]


def gavel(S, cx, cy):
    hd = poly(rrect_pts(cx, cy, 7, 4, 45), closed=True, r=S.r * 0.5)
    return [shell(hd), line(seg(cx - 1.6, cy + 1.7, cx - 4.2, cy + 4.3))]


@icon("container-query", CAT, "Outer box with a smaller component inside it and a short ruler along the inner top edge",
      tags=["css container", "@container", "component responsive", "element query", "resize by parent", "container width"])
def _(S):
    return [
        shell(rect(2, 2.5, 20, 19, S.R)),
        detail(seg(6, 7, 18, 7)), detail(seg(6, 5.5, 6, 8.5)), detail(seg(18, 5.5, 18, 8.5)),
        detail(rect(7.5, 11.5, 9, 6, min(S.R, 2))),
    ]


@icon("content-management-system", CAT, "Browser window with stacked content blocks and a pencil beside it",
      tags=["cms", "edit website", "publish content", "admin panel", "page editor", "website backend"])
def _(S):
    pencil = poly([(17.6, 8.5), (21.2, 8.5), (21.2, 17), (19.4, 20.5), (17.6, 17)], closed=True, r=S.r * 0.5)
    return [
        *win(S, 2, 3, 13, 18),
        Part("dot", rect(5, 9, 7, 3, L(S, 0, 0.6))), Part("dot", rect(5, 14.5, 7, 3, L(S, 0, 0.6))),
        shell(pencil),
    ]


@icon("headless-cms", CAT, "Stack of content blocks with three arrows fanning out to a watch, a monitor and a phone",
      tags=["api first cms", "decoupled cms", "content api", "omnichannel", "multi device content", "content hub"])
def _(S):
    return [
        shell(rect(2, 3, 7, 18, min(S.R, 2.5))), detail(seg(2, 9, 9, 9)), detail(seg(2, 15, 9, 15)),
        line(seg(10.5, 6, 13.5, 6)), head(S, (14, 6), 0, 2.2),
        line(seg(10.5, 12, 13.5, 12)), head(S, (14, 12), 0, 2.2),
        line(seg(10.5, 18, 13.5, 18)), head(S, (14, 18), 0, 2.2),
        dot(19.5, 6, 2.3), Part("dot", rect(16.5, 9.8, 6, 4.4, L(S, 0, 0.8))), Part("dot", rect(18, 16, 3.6, 5.5, L(S, 0, 0.8))),
    ]


@icon("block-editor", CAT, "Stacked content blocks with a round plus inserter beside the middle one",
      tags=["add block", "block based editing", "insert block", "page blocks", "content blocks"])
def _(S):
    return [
        shell(rect(2.5, 2, 13, 5.5, min(S.R, 2))),
        shell(rect(2.5, 9.25, 9, 5.5, min(S.R, 2))),
        shell(rect(2.5, 16.5, 13, 5.5, min(S.R, 2))),
        shell(circle(18.5, 12, 3.6)),
        detail(seg(17.1, 12, 19.9, 12)), detail(seg(18.5, 10.6, 18.5, 13.4)),
    ]


@icon("page-builder", CAT, "Browser window with an arrow cursor dragging a section block toward a dashed slot",
      tags=["drag and drop builder", "visual builder", "layout editor", "wysiwyg", "section blocks", "site builder"])
def _(S):
    return [
        *win(S, 2, 3, 20, 18),
        detail(corners(5, 8.5, 14, 4.5, 2)),
        Part("dot", rect(6, 16, 8, 2.5, L(S, 0, 0.8))),
        cursor(S, 14, 14.5, 0.9),
    ]


@icon("content-calendar", CAT, "Calendar grid with small post blocks placed on several of its days",
      tags=["editorial calendar", "publishing schedule", "post planner", "social calendar", "content plan", "schedule posts"])
def _(S):
    return [
        shell(rect(2, 4, 20, 17.5, S.R)),
        detail(seg(2, 9, 22, 9)),
        line(seg(7, 2, 7, 6)), line(seg(17, 2, 17, 6)),
        Part("dot", rect(4.5, 12, 7, 2, L(S, 0, 0.8))), Part("dot", rect(14.5, 12, 3, 2, L(S, 0, 0.8))),
        Part("dot", rect(4.5, 16.5, 3, 2, L(S, 0, 0.8))), Part("dot", rect(10, 16.5, 7.5, 2, L(S, 0, 0.8))),
    ]


@icon("user-roles", CAT, "Three people of different sizes, the tallest wearing a small crown",
      tags=["permissions", "admin editor author", "role management", "access levels", "team roles", "capabilities"])
def _(S):
    return [
        dot(12, 10.5, 2.6),
        line("M7 21A5 5 0 0 1 17 21"),
        line(poly([(9.2, 6.5), (9.2, 3.2), (10.8, 4.8), (12, 2.5), (13.2, 4.8), (14.8, 3.2), (14.8, 6.5)], r=S.r * 0.3)),
        dot(4.5, 14, 1.8), line("M2 21A3.2 3.2 0 0 1 7 18.5"),
        dot(19.5, 14, 1.8), line("M22 21A3.2 3.2 0 0 0 17 18.5"),
    ]


@icon("website-theme", CAT, "Browser window with a paint palette on the page",
      tags=["site design", "skin", "colour scheme", "template style", "appearance", "theme switcher"])
def _(S):
    return [
        *win(S, 2, 3, 20, 18),
        detail("M12 9.5C8 9.5 5.5 12 5.5 14.5C5.5 17.5 8 19 10.5 19C12.5 19 12 17.2 13.8 17.2H16C18.2 17.2 19.5 15.8 19.5 14.2C19.5 11.5 16.5 9.5 12 9.5Z"),
        dot(9, 13.4, 0.8), dot(12, 12.3, 0.8), dot(15.5, 13.4, 0.8),
    ]


@icon("comment-moderation", CAT, "Speech bubble with a small gavel beside its lower corner",
      tags=["moderate comments", "approve comments", "spam review", "community moderation", "comment queue", "review replies"])
def _(S):
    return [
        shell(poly([(2, 3), (16, 3), (16, 13), (9, 13), (5, 17), (5, 13), (2, 13)], closed=True, r=S.r * 1.5)),
        detail(seg(6, 8, 12, 8)),
        *gavel(S, 18.5, 17),
    ]


@icon("static-site-generator", CAT, "Gear feeding a stack of plain pages, one carrying a lightning bolt",
      tags=["ssg", "build site", "jamstack", "pre-render", "generate pages", "static build"])
def _(S):
    return [
        shell(poly(gear_pts(7, 12, 5.6, 4.2, 6), closed=True, r=S.r * 0.4)),
        dot(7, 12, 1.5),
        line("M15 7.5H21"), line("M17 4.5H21"),
        shell(rect(12.5, 10, 9, 11.5, min(S.R, 2.5))),
        detail(poly([(17.5, 12.5), (15.8, 16), (18.2, 16), (16.5, 19.5)], r=S.r * 0.3)),
    ]


@icon("featured-image", CAT, "Post page with a large image block marked by a star above a line of text",
      tags=["post thumbnail", "hero image", "cover image", "lead image", "article image", "blog header image"])
def _(S):
    return [
        shell(rect(2.5, 2, 19, 20, min(S.R, 3))),
        detail(rect(5.5, 5, 13, 8, min(S.R, 1.5))),
        Part("dot", poly(star_pts(12, 9, 3, 1.3), closed=True, r=0)),
        detail(seg(5.5, 17.5, 15, 17.5)),
    ]


@icon("multisite-network", CAT, "Browser window at the top linked by lines to three smaller windows below",
      tags=["multi-site install", "site network", "many sites", "sub sites", "network admin", "site family"])
def _(S):
    return [
        shell(rect(6.5, 2, 11, 8, min(S.R, 2.5))),
        detail(seg(6.5, 5.5, 17.5, 5.5)),
        line("M12 10V12.5M4.5 15V12.5H19.5V15M12 12.5V15"),
        shell(rect(2, 15, 5, 6.5, min(S.R, 1.5))), shell(rect(9.5, 15, 5, 6.5, min(S.R, 1.5))), shell(rect(17, 15, 5, 6.5, min(S.R, 1.5))),
    ]


@icon("code-playground", CAT, "Browser window split into a code pane with a bracket and a live preview pane",
      tags=["sandbox", "live editor", "try code", "html css preview", "snippet runner"])
def _(S):
    return [
        *win(S, 2, 3, 20, 18),
        detail(seg(12, 7.5, 12, 21)),
        detail(poly([(8.6, 10.5), (6, 14), (8.6, 17.5)], r=S.r * 0.5)),
        Part("dot", rect(14.5, 10.5, 5, 4, L(S, 0, 0.8))),
    ]


@icon("z-pattern-layout", CAT, "Page outline with a bold Z path from the top left corner to the bottom right",
      tags=["z layout", "reading pattern", "eye path", "landing page scan", "visual flow", "zig zag scan"])
def _(S):
    return [
        shell(rect(2.5, 2, 19, 20, min(S.R, 3))),
        detail(poly([(6, 6.5), (18, 6.5), (6, 17.5), (18, 17.5)], r=S.r * 0.4)),
    ]


@icon("f-pattern-layout", CAT, "Page outline with an F shaped set of scan lines along the top and left side",
      tags=["f layout", "reading pattern", "eye tracking pattern", "text scan", "content skim", "f shaped"])
def _(S):
    return [
        shell(rect(2.5, 2, 19, 20, min(S.R, 3))),
        detail(poly([(18, 6.5), (6.5, 6.5), (6.5, 18)], r=S.r * 0.4)),
        detail(seg(6.5, 12, 14, 12)),
    ]


# ============================================================================ page layout

def tri_pts(cx, cy, r):
    return [polar(cx, cy, r, -90 + 120 * i) for i in range(3)]


@icon("asymmetric-layout", CAT, "Page split into a wide left column of blocks and a narrow right column",
      tags=["uneven columns", "off balance layout", "two column page", "wide and narrow", "editorial layout", "unequal grid"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, S.R)),
        detail(seg(16, 3, 16, 21)),
        Part("dot", rect(5, 6.5, 8, 5.5, L(S, 0, 0.8))),
        detail(seg(5, 16, 12.5, 16)),
        detail(seg(19, 7, 19, 17)),
    ]


@icon("broken-grid-layout", CAT, "Grid of blocks where one tall image block breaks out of its row",
      tags=["overlapping layout", "grid breaking", "editorial grid", "experimental layout", "offset blocks", "collage layout"])
def _(S):
    return [
        shell(rect(2, 2, 10, 8, min(S.R, 2.5))),
        shell(rect(14, 2, 8, 4, min(S.R, 2))),
        shell(rect(2, 13, 7, 8, min(S.R, 2.5))),
        shell(rect(12, 9, 10, 12, min(S.R, 2.5))),
        dot(17, 13.5, 1),
    ]


@icon("map-list-layout", CAT, "Screen split into a list of three rows on the left and a map with a pin on the right",
      tags=["store locator layout", "split view", "listings and map", "directory page", "real estate search", "results with map"])
def _(S):
    pin = L(S, "M16.5 18L13.2 12.8A3.8 3.8 0 1 1 19.8 12.8Z", "M16.5 18C16.5 18 12.7 14.6 12.7 11.8A3.8 3.8 0 0 1 20.3 11.8C20.3 14.6 16.5 18 16.5 18Z")
    return [
        shell(rect(2, 3, 20, 18, S.R)),
        detail(seg(10, 3, 10, 21)),
        detail(seg(4.5, 8, 8, 8)), detail(seg(4.5, 12, 8, 12)), detail(seg(4.5, 16, 8, 16)),
        detail(pin), dot(16.5, 11.8, 0.9),
    ]


@icon("product-listing-layout", CAT, "Page with a narrow filter column of checkboxes beside a two by two grid of product cards",
      tags=["shop page", "catalog layout", "faceted filters", "category page", "ecommerce grid", "product grid"])
def _(S):
    out = [shell(rect(2, 3, 20, 18, S.R)), detail(seg(8.5, 3, 8.5, 21))]
    for y in (7, 11.5, 16):
        out.append(Part("dot", rect(4, y, 2.5, 2.5, L(S, 0, 0.5))))
    for x in (11, 16.5):
        for y in (6.5, 13):
            out.append(Part("dot", rect(x, y, 4, 5, L(S, 0, 0.8))))
    return out


@icon("client-logo-strip", CAT, "Horizontal band holding a row of four plain shapes: circle, square, triangle and hexagon",
      tags=["trusted by", "customer logos", "partner logos", "logo bar", "social proof", "brand strip"])
def _(S):
    return [
        shell(rect(2, 6.5, 20, 11, S.R)),
        dot(6.2, 12, 1.7),
        Part("dot", rect(9.7, 10.3, 3.4, 3.4, L(S, 0, 0.5))),
        Part("dot", poly(tri_pts(15.4, 12.3, 2.1), closed=True)),
        Part("dot", poly(regular(19.2, 12, 1.9, 6), closed=True)),
    ]


@icon("feature-grid", CAT, "Three by two grid of small squares, each with a short line under it",
      tags=["features section", "benefits grid", "six features", "icon grid", "landing page features", "service blocks"])
def _(S):
    out = []
    for x in (2.5, 9.5, 16.5):
        for y, ly in ((2.5, 10.5), (13.5, 21)):
            out.append(Part("solid", rect(x, y, 5, 4.5, L(S, 0, 1))))
            out.append(line(seg(x, ly, x + 5, ly)))
    return out


@icon("visual-hierarchy", CAT, "Three stacked text bars shrinking in size and weight from top to bottom",
      tags=["typographic scale", "heading levels", "emphasis", "content priority", "size contrast", "layout order"])
def _(S):
    return [
        Part("solid", rect(3, 3, 18, 6, L(S, 0, 1.2))),
        Part("solid", rect(3, 12, 13, 3.5, L(S, 0, 1))),
        line(seg(3, 20, 9.5, 20)),
    ]


@icon("above-the-fold", CAT, "Page with a dashed horizontal line across its middle and content filled in above it",
      tags=["fold line", "first screen", "hero area", "visible without scrolling", "top of page", "initial viewport"])
def _(S):
    return [
        shell(rect(4, 2, 16, 20, min(S.R, 3))),
        Part("dot", rect(7, 5, 10, 3.5, L(S, 0, 0.8))),
        detail(seg(7, 10.5, 14, 10.5)),
        detail(seg(5.5, 14, 8, 14)), detail(seg(10.5, 14, 13, 14)), detail(seg(15.5, 14, 18, 14)),
        detail(seg(7, 18, 11, 18)),
    ]


@icon("long-scroll-page", CAT, "Tall page passing behind a corner-bracket screen frame with a scroll arrow beside it",
      tags=["infinite scroll", "single page site", "scrolling page", "tall page", "one page layout", "scroll down"])
def _(S):
    return [
        shell(rect(5.5, 1.5, 9, 21, min(S.R, 2.5))),
        detail(seg(8, 6, 12, 6)), detail(seg(8, 18, 12, 18)),
        line(corners(2, 7.5, 16, 9, 3.2)),
        line(seg(21, 5, 21, 19)), head(S, (21, 4.5), -90, 2.3), head(S, (21, 19.5), 90, 2.3),
    ]


@icon("shape-divider", CAT, "Two stacked page sections separated by a wavy edge",
      tags=["wave divider", "section separator", "curved section", "svg divider", "wavy edge", "landing page section"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, S.R)),
        detail("M2 12C5.5 8.5 8.5 8.5 12 12S18.5 15.5 22 12"),
        detail(seg(6, 6.5, 14, 6.5)),
        detail(seg(10, 18, 18, 18)),
    ]


@icon("lightbox-gallery", CAT, "Framed enlarged picture in the centre with small arrows on both sides",
      tags=["image popup", "photo viewer", "gallery overlay", "slideshow modal", "enlarge image", "next previous photo"])
def _(S):
    return [
        line(poly([(4, 9), (2.3, 12), (4, 15)], r=S.r * 0.5)),
        line(poly([(20, 9), (21.7, 12), (20, 15)], r=S.r * 0.5)),
        shell(rect(7, 4, 10, 16, min(S.R, 2.5))),
        detail(poly([(7, 16.5), (10.5, 12.5), (12.5, 14.5), (14, 13), (17, 16)], r=S.r * 0.4)),
        dot(12.8, 8.5, 1),
    ]


@icon("fluid-layout", CAT, "Page with content blocks and two outward arrows at its sides showing it stretches",
      tags=["liquid layout", "percentage widths", "stretchy page", "flexible width", "responsive width", "full width"])
def _(S):
    return [
        shell(rect(6.5, 3.5, 11, 17, min(S.R, 3))),
        Part("dot", rect(9, 7, 6, 4, L(S, 0, 0.8))), detail(seg(9, 15.5, 15, 15.5)),
        line(seg(4.5, 12, 2.5, 12)), head(S, (2.2, 12), 180, 2.2),
        line(seg(19.5, 12, 21.5, 12)), head(S, (21.8, 12), 0, 2.2),
    ]


@icon("mobile-first", CAT, "Large phone outline in front of a smaller monitor outline behind it",
      tags=["mobile first design", "phone first", "small screen first", "progressive enhancement", "responsive strategy", "handset"])
def _(S):
    return [
        line("M7 5.5V3H22V14H11.5"),
        line(seg(16.5, 14, 16.5, 19)), line(seg(13.5, 19, 19.5, 19)),
        shell(rect(2, 6, 9.5, 16, min(S.R, 3))),
        dot(6.75, 18.5, 0.9),
    ]


@icon("browser-viewport", CAT, "Browser window with dashed corner brackets marking the visible area of a longer page",
      tags=["visible area", "viewport size", "window size", "screen area", "vh vw", "visible region"])
def _(S):
    return [
        *win(S, 2, 3, 20, 18),
        detail(corners(5, 9.5, 14, 8, 2.5)),
    ]


# ============================================================================ visual style, page sections and process

@icon("neumorphism", CAT, "Rounded square button raised from a flat surface, with a light edge top left and a shadow edge bottom right",
      tags=["soft ui", "soft shadows", "embossed button", "raised button", "skeuomorphic flat", "extruded"])
def _(S):
    return [
        line("M2.5 14V8A5.5 5.5 0 0 1 8 2.5H14"),
        line("M21.5 10V16A5.5 5.5 0 0 1 16 21.5H10"),
        shell(rect(6.5, 6.5, 11, 11, L(S, 2, 5))),
    ]


@icon("lorem-ipsum", CAT, "Dashed frame holding three lines of wavy placeholder text",
      tags=["dummy text", "placeholder text", "filler copy", "sample paragraph", "greeking", "latin text"])
def _(S):
    return [
        line(corners(2.5, 3, 19, 18, 3.5)),
        line("M6 8Q7.5 6.5 9 8T12 8T15 8T18 8"),
        line("M6 12Q7.5 10.5 9 12T12 12T15 12T18 12"),
        line("M6 16Q7.5 14.5 9 16T12 16"),
    ]


@icon("css-box-model", CAT, "Four nested rectangles, each smaller one centred inside the one before",
      tags=["margin border padding", "content box", "box sizing", "css layout", "spacing model", "element box"])
def _(S):
    return [
        shell(rect(2, 2, 20, 20, S.R)),
        detail(rect(6, 6, 12, 12, min(S.R, 2))),
        detail(rect(10, 10, 4, 4, 0)),
    ]


@icon("author-box", CAT, "Box with a round portrait on the left and a name line with bio lines on the right",
      tags=["about the author", "byline box", "writer bio", "post author", "profile card", "contributor"])
def _(S):
    return [
        shell(rect(2, 4.5, 20, 15, S.R)),
        dot(7.8, 12, 2.9),
        detail(seg(13.5, 9, 19, 9)), detail(seg(13.5, 12.5, 19, 12.5)), detail(seg(13.5, 16, 17, 16)),
    ]


@icon("related-posts", CAT, "Two lines of article text above a row of three small cards with image blocks",
      tags=["related articles", "more like this", "recommended reading", "you may also like", "post suggestions", "read next"])
def _(S):
    return [
        line(seg(2.5, 3.5, 21.5, 3.5)), line(seg(2.5, 7.5, 15, 7.5)),
        Part("solid", rect(2, 12, 5.5, 9, L(S, 0, 1))), Part("solid", rect(9.25, 12, 5.5, 9, L(S, 0, 1))), Part("solid", rect(16.5, 12, 5.5, 9, L(S, 0, 1))),
    ]


@icon("social-share-bar", CAT, "Vertical strip of four small circles stuck to the left edge of a page",
      tags=["share buttons", "floating share", "social icons", "sticky share", "side bar share", "share links"])
def _(S):
    return [
        shell(rect(9, 2.5, 13, 19, min(S.R, 3))),
        detail(seg(12.5, 8, 18.5, 8)), detail(seg(12.5, 12, 18.5, 12)), detail(seg(12.5, 16, 16, 16)),
        dot(4.2, 5, 1.7), dot(4.2, 9.7, 1.7), dot(4.2, 14.4, 1.7), dot(4.2, 19, 1.7),
    ]


@icon("zigzag-sections", CAT, "Page with three rows where the image block alternates between left and right of the text",
      tags=["alternating sections", "checkerboard layout", "image text rows", "z layout rows", "landing page rows", "staggered content"])
def _(S):
    return [
        shell(rect(2.5, 2, 19, 20, min(S.R, 3))),
        Part("dot", rect(5.5, 4.8, 5.5, 3.5, L(S, 0, 0.6))), detail(seg(13.5, 6.5, 18.5, 6.5)),
        detail(seg(5.5, 12, 10.5, 12)), Part("dot", rect(13, 10.2, 5.5, 3.5, L(S, 0, 0.6))),
        Part("dot", rect(5.5, 15.7, 5.5, 3.5, L(S, 0, 0.6))), detail(seg(13.5, 17.5, 18.5, 17.5)),
    ]


@icon("fullscreen-menu-overlay", CAT, "Window covered by a panel with three large centred menu lines and a close cross",
      tags=["hamburger menu open", "full page navigation", "menu takeover", "nav overlay", "mobile menu open", "close menu"])
def _(S):
    return [
        shell(rect(2, 2.5, 20, 19, S.R)),
        detail(seg(16, 5, 19.5, 8.5)), detail(seg(19.5, 5, 16, 8.5)),
        detail(seg(6, 12, 18, 12)), detail(seg(6, 15.2, 18, 15.2)), detail(seg(6, 18.4, 18, 18.4)),
    ]


@icon("full-bleed-image", CAT, "Page with text lines and an image band that stretches to both page edges",
      tags=["edge to edge image", "wide image", "hero band", "full width photo", "banner image", "bleed"])
def _(S):
    return [
        shell(rect(3, 2, 18, 20, min(S.R, 3))),
        detail(seg(7, 5.5, 17, 5.5)),
        Part("dot", poly([(3, 17.5), (3, 11), (21, 11), (21, 17.5)], closed=True)),
        detail(seg(7, 8, 13, 8)),
    ]


@icon("scroll-reveal", CAT, "Page whose blocks change from solid to outlined to dashed going down, with a scroll arrow at its side",
      tags=["reveal on scroll", "fade in on scroll", "scroll animation", "appear when visible", "animate on scroll", "entrance effect"])
def _(S):
    return [
        shell(rect(2, 2, 14.5, 20, min(S.R, 3))),
        Part("dot", rect(5, 5, 8.5, 3.5, L(S, 0, 0.6))),
        detail(rect(5.5, 10.5, 7.5, 3, 0)),
        detail(corners(5, 16, 8.5, 3.5, 1.5)),
        *arrow(S, 21, 5, 21, 18.5, 2.4),
    ]


@icon("web-design", CAT, "Browser window with a pen nib and a ruler crossed on the page",
      tags=["website design", "ui design", "layout design", "designer", "site mockup", "creative web"])
def _(S):
    nib = L(S, "M8.5 10.5H14.5L16 14L11.5 19.5L7 14Z", "M9.5 10.5H13.5Q15 10.5 16 14L11.5 19.5L7 14Q8 10.5 9.5 10.5Z")
    return [
        *win(S, 2, 3, 20, 18),
        detail(nib), dot(11.5, 13, 0.9), detail(seg(11.5, 15.5, 11.5, 19)),
        detail(seg(19, 10.5, 19, 19)), detail(seg(17.5, 10.5, 20.5, 10.5)), detail(seg(17.5, 19, 20.5, 19)),
    ]


@icon("usability-testing", CAT, "Person at a monitor with an eye above the screen",
      tags=["user testing", "ux research", "observe users", "usability study", "think aloud", "test session"])
def _(S):
    return [
        dot(5, 12.5, 2.2), line("M1.8 21A3.2 3.8 0 0 1 8.2 21"),
        shell(rect(10, 12, 12, 8, min(S.R, 2.5))),
        line(seg(16, 20, 16, 22)),
        shell(eye_d(16, 6, 5.5, 2.6, S)), dot(16, 6, 1),
    ]


@icon("design-handoff", CAT, "Artboard frame with a bent arrow leading down to code angle brackets",
      tags=["design to code", "developer handoff", "spec sheet", "hand over design", "design to dev", "implementation"])
def _(S):
    return [
        shell(rect(2, 2, 10, 9, min(S.R, 2.5))),
        detail(seg(5, 6.5, 9, 6.5)),
        line(poly([(14.5, 6.5), (19.5, 6.5), (19.5, 11)], r=S.r * 0.5)), head(S, (19.5, 11.6), 90, 2.4),
        line(poly([(12.5, 15), (9.5, 18), (12.5, 21)], r=S.r * 0.5)),
        line(seg(17, 14.8, 14.6, 21.2)),
        line(poly([(19, 15), (22, 18), (19, 21)], r=S.r * 0.5)),
    ]


@icon("cross-browser-testing", CAT, "Three overlapping browser windows with a tick in the front one",
      tags=["browser compatibility", "multi browser", "compatibility check", "browser matrix", "rendering test"])
def _(S):
    return [
        line("M5.5 11H2V2H14.5V5"),
        line("M9.5 15.5H6V6.5H18V10"),
        shell(rect(10, 11, 12, 10.5, min(S.R, 2.5))),
        detail(poly([(13, 16.5), (15.3, 18.7), (19, 14.3)], r=S.r * 0.4)),
    ]


@icon("fieldset", CAT, "Rectangle border whose top edge is broken by a short legend label, with two input lines inside",
      tags=["form group", "legend", "grouped fields", "form section", "html fieldset", "field group"])
def _(S):
    return [
        line(poly([(5, 5), (2.5, 5), (2.5, 21), (21.5, 21), (21.5, 5), (17, 5)], r=S.r)),
        Part("solid", rect(7, 3.7, 8, 2.6, L(S, 0, 1))),
        line(seg(6.5, 11, 17.5, 11)), line(seg(6.5, 16, 17.5, 16)),
    ]


@icon("input-mask", CAT, "Input field showing a pattern of grouped underscores separated by dashes",
      tags=["formatted input", "phone number mask", "masked field", "pattern entry", "placeholder format", "input format"])
def _(S):
    return [
        shell(rect(2, 7.5, 20, 9, S.R)),
        Part("dot", rect(4.5, 13, 2.6, 1.4)), Part("dot", rect(8, 13, 2.6, 1.4)),
        Part("dot", rect(11.7, 11.6, 1.8, 1.2)),
        Part("dot", rect(14.6, 13, 2.6, 1.4)), Part("dot", rect(18, 13, 2, 1.4)),
    ]


@icon("terms-checkbox", CAT, "Ticked checkbox beside a small document with a folded corner",
      tags=["accept terms", "agree to policy", "consent box", "terms and conditions", "i agree", "legal checkbox"])
def _(S):
    return [
        shell(rect(2, 7, 9, 9, min(S.R, 2.5))),
        detail(poly([(4.6, 11.7), (6.2, 13.3), (8.9, 10)], r=S.r * 0.4)),
        shell(poly([(14, 3), (19, 3), (22, 6), (22, 21), (14, 21)], closed=True, r=S.r)),
        detail(seg(16.8, 11, 19.5, 11)), detail(seg(16.8, 15, 19.5, 15)),
    ]


@icon("form-submissions", CAT, "Inbox tray holding a stack of form sheets with field lines",
      tags=["form responses", "received entries", "submitted forms", "lead inbox", "form data", "entries list"])
def _(S):
    return [
        line(poly([(5.5, 14), (5.5, 2.5), (18.5, 2.5), (18.5, 14)], r=S.r)),
        line(seg(9, 6.5, 15, 6.5)), line(seg(9, 10, 13, 10)),
        shell(poly([(2, 13), (7, 13), (8.5, 16), (15.5, 16), (17, 13), (22, 13), (22, 21), (2, 21)], closed=True, r=S.r * 0.6)),
    ]


@icon("site-health", CAT, "Browser window with a heartbeat pulse line across the page",
      tags=["website health", "uptime check", "site status", "health monitor", "site audit", "vital signs"])
def _(S):
    return [
        *win(S, 2, 3, 20, 18),
        detail(poly([(4.5, 14.5), (8, 14.5), (10, 10.5), (13, 18.5), (15, 13), (16.5, 14.5), (19.5, 14.5)], r=S.r * 0.5)),
    ]
