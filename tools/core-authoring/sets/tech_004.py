"""TypeIcon Core: tech (batch 004): web platform, machine learning and PC hardware concepts.

Windows are 20 x 18 frames with a header line; small marks (nodes, sparkles, eyes) are `mark`/`dot` parts so
they knock out of Filled shells. Nodes in networks are solid dots joined by open lines.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar, rotation, transform_path

CAT = "tech"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def mark(d) -> Part:
    return Part("dot", d)


def tf(d, m):
    return path_to_d(transform_path(P(d), m))


def mv(d, dx, dy):
    return tf(d, (1, 0, 0, 1, dx, dy))


def sc(d, k, cx=12.0, cy=12.0):
    """Scale a path about (cx, cy)."""
    return tf(d, (k, 0, 0, k, cx - k * cx, cy - k * cy))


def sparkle(cx, cy, r):
    pts = [polar(cx, cy, r if i % 2 == 0 else r * 0.36, -90 + i * 45) for i in range(8)]
    return poly(pts, closed=True)


def win(S, x=2, y=3, w=20, h=18, bar=4):
    """Browser window frame with a header line."""
    return [shell(rect(x, y, w, h, rr(S, 3))), detail(seg(x, y + bar, x + w, y + bar))]


def chev(tip, frm, size=2.2):
    """Open arrowhead (polyline points) with its point at tip, coming from frm."""
    dx, dy = tip[0] - frm[0], tip[1] - frm[1]
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    bx, by = tip[0] - ux * size, tip[1] - uy * size
    return [(bx - uy * size, by + ux * size), tip, (bx + uy * size, by - ux * size)]


def arrow(S, a, b, size=2.2):
    """Line arrow from a to b with an open head."""
    return [line(seg(*a, *b)), line(poly(chev(b, a, size), r=S.r))]


def carrow(S, cx, cy, r, a0, a1, size=2.0, k=line):
    """Clockwise circular arrow from angle a0 to a1 (degrees) with an open head (k = line or detail)."""
    tip = polar(cx, cy, r, a1)
    t = math.radians(a1)
    frm = (tip[0] + math.sin(t), tip[1] - math.cos(t))  # opposite of travel direction
    return [k(arc(cx, cy, r, a0, a1)), k(poly(chev(tip, frm, size), r=S.r))]


def node(S, x, y, r=1.8):
    """Network node: square in Line, round in Rounded (solid mark)."""
    if S.name == "line":
        return dot_sq(x, y, r)
    return dot(x, y, r)


def dot_sq(x, y, r):
    return Part("dot", rect(x - r, y - r, 2 * r, 2 * r))


def gear_d(cx, cy, ro, ri, n=6, tooth=0.5):
    pts = []
    step = 360 / n
    for i in range(n):
        a = -90 + i * step
        w = step * tooth / 2
        pts += [polar(cx, cy, ri, a - step / 2 + 3), polar(cx, cy, ro, a - w), polar(cx, cy, ro, a + w)]
        pts.append(polar(cx, cy, ri, a + step / 2 - 3))
    return poly(pts, closed=True)


def gear(S, cx, cy, ro=5.0, ri=3.6, n=6, hole=1.3, k=shell):
    return [k(gear_d(cx, cy, ro, ri, n)), mark(circle(cx, cy, hole))]


def robot(S, x, y, w=14, h=11, eye=1.3, ant=True):
    """Robot head whose body rect starts at (x, y)."""
    cx = x + w / 2
    parts = [shell(rect(x, y, w, h, rr(S, 3)))]
    if ant:
        parts += [line(seg(cx, y - 2.5, cx, y)), mark(circle(cx, y - 3.2, 1.2))]
    parts += [mark(circle(cx - w * 0.22, y + h * 0.42, eye)), mark(circle(cx + w * 0.22, y + h * 0.42, eye))]
    return parts


# --------------------------------------------------------------------------- web platform

@icon("css-selector", CAT, "Hash sign inside four selection corner brackets.",
      tags=["css", "selector", "hash", "id selector", "style rule", "web development"])
def _(S):
    c = lambda p: line(poly(p, r=S.r))
    return [c([(3, 7), (3, 3), (7, 3)]), c([(17, 3), (21, 3), (21, 7)]),
            c([(21, 17), (21, 21), (17, 21)]), c([(7, 21), (3, 21), (3, 17)]),
            line(seg(10, 8, 10, 16)), line(seg(14, 8, 14, 16)),
            line(seg(8, 10, 16, 10)), line(seg(8, 14, 16, 14))]


@icon("responsive-design", CAT, "Desktop monitor next to a smaller phone showing a layout that adapts to screen size.",
      tags=["responsive", "adaptive layout", "breakpoints", "mobile friendly", "multi device", "web design"])
def _(S):
    return [shell(rect(2, 4, 12, 9, rr(S, 2))), line(seg(8, 13, 8, 17)), line(seg(5, 17.5, 11, 17.5)),
            shell(rect(16.5, 8, 5, 12, rr(S, 2))), mark(circle(19, 17.5, 0.8))]


@icon("media-query", CAT, "Monitor screen with an at sign inside, the symbol that starts a CSS media rule.",
      tags=["media query", "css", "breakpoint", "at rule", "responsive", "screen width"])
def _(S):
    return [shell(rect(2, 3, 20, 15, rr(S, 3))), line(seg(8, 21, 16, 21)),
            detail(arc(12, 10.5, 4.4, 30, 335)), mark(circle(11.3, 10.5, 1.2)), detail(seg(14.8, 8.5, 14.8, 12.5))]


@icon("flexbox", CAT, "Container box holding three flexible blocks in a row with a double arrow showing they stretch.",
      tags=["flexbox", "css", "flex layout", "flex container", "row", "web layout"])
def _(S):
    return [shell(rect(2, 3, 20, 18, rr(S, 3))),
            mark(rect(5.5, 7, 3.5, 6)), mark(rect(10.25, 7, 3.5, 6)), mark(rect(15, 7, 3.5, 6)),
            detail(seg(6, 17, 18, 17)),
            detail(poly([(8, 15), (6, 17), (8, 19)])), detail(poly([(16, 15), (18, 17), (16, 19)]))]


@icon("css-grid", CAT, "Square divided into a three by three grid where the top right cell spans two columns.",
      tags=["css grid", "grid layout", "columns", "rows", "web layout", "template"])
def _(S):
    return [shell(rect(3, 3, 18, 18, rr(S, 3))),
            detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15)),
            detail(seg(9, 3, 9, 21)), detail(seg(15, 9, 15, 21))]


@icon("virtual-dom", CAT, "Tree of nodes where the left branch is solid and the right branch is drawn as hollow ghost nodes.",
      tags=["virtual dom", "dom tree", "diffing", "ui library", "reconciliation", "component tree"])
def _(S):
    ring = lambda x, y: shell(circle(x, y, 2.4))
    return [line(seg(12, 5, 6, 12)), line(seg(12, 5, 18, 12)), line(seg(6, 12, 6, 19)), line(seg(18, 12, 18, 19)),
            dot(12, 4.5, 1.8), dot(6, 12, 1.8), dot(6, 20, 1.8), ring(18, 12), ring(18, 20)]


@icon("single-page-app", CAT, "Browser window with a looping arrow in the page area, one page that updates in place.",
      tags=["spa", "single page application", "client side routing", "web app", "reload", "dynamic page"])
def _(S):
    return win(S) + carrow(S, 12, 14.5, 3.8, -50, 235, k=detail)


@icon("progressive-web-app", CAT, "Browser window with a plus badge at the corner that offers to install the page as an app.",
      tags=["pwa", "installable", "web app", "add to home screen", "offline", "install"])
def _(S):
    return [shell(rect(2, 3, 15, 12, rr(S, 3))), detail(seg(2, 7, 17, 7)),
            line(seg(19.5, 16.5, 19.5, 21.5)), line(seg(17, 19, 22, 19))]


@icon("service-worker", CAT, "Browser window with a gear in the page area for the background script behind it.",
      tags=["service worker", "background script", "offline cache", "pwa", "browser api", "worker"])
def _(S):
    return win(S) + gear(S, 12, 14.2, 4.6, 3.3, 6, 1.2, k=detail)


@icon("web-worker", CAT, "Browser window with a hard hat in the page area for a script that works in the background.",
      tags=["web worker", "thread", "background thread", "parallel", "worker", "javascript"])
def _(S):
    return win(S) + [detail(arc(12, 17.5, 4.5, 180, 360) + "Z"), detail(seg(5.5, 17.5, 18.5, 17.5)),
                     detail(seg(12, 13, 12, 17.5))]


@icon("server-side-rendering", CAT, "Server unit sending a finished page window down an arrow to the browser.",
      tags=["ssr", "server rendering", "html generation", "universal rendering", "prerender", "web server"])
def _(S):
    return [shell(rect(3, 2.5, 18, 6, rr(S, 2))), mark(circle(6.5, 5.5, 0.9)), detail(seg(10, 5.5, 18, 5.5)),
            line(seg(12, 10.5, 12, 13)), line(poly([(10, 11.5), (12, 13.5), (14, 11.5)], r=S.r)),
            shell(rect(3, 15, 18, 6.5, rr(S, 2))), detail(seg(3, 17.5, 21, 17.5))]


@icon("page-not-found", CAT, "Browser window with a sad face, the error shown when a web address has no page.",
      tags=["404", "not found", "error page", "missing page", "broken link", "http error"])
def _(S):
    return win(S) + [mark(circle(9.5, 12, 1.2)), mark(circle(14.5, 12, 1.2)), detail(arc(12, 19, 3.6, 222, 318))]


@icon("server-error", CAT, "Browser window with a lightning bolt in the page area for a crashed server.",
      tags=["500", "internal server error", "crash", "server failure", "http error", "outage"])
def _(S):
    bolt = poly([(13.5, 9), (9, 15), (12, 15), (10.5, 20), (15.5, 13.5), (12.5, 13.5)], closed=True, r=S.r * 0.5)
    return win(S) + [mark(bolt)]


@icon("access-forbidden", CAT, "Browser window with a no entry circle in the page area for a page you may not open.",
      tags=["403", "forbidden", "access denied", "blocked", "permission denied", "http error"])
def _(S):
    return win(S) + [detail(circle(12, 14.3, 4.8)), detail(seg(8.9, 17.7, 15.1, 10.9))]


@icon("robots-txt", CAT, "Document page with a small robot head on it, the file that tells crawlers what to skip.",
      tags=["robots.txt", "crawler", "seo", "web bot", "search engine", "crawl rules"])
def _(S):
    page = poly([(5, 2), (14, 2), (19, 7), (19, 22), (5, 22)], closed=True, r=S.r)
    return [shell(page), detail(poly([(14, 2), (14, 7), (19, 7)])),
            detail(rect(8, 12, 8, 6.5, rr(S, 1.5))), detail(seg(12, 9.5, 12, 12)),
            mark(circle(10.3, 15, 0.9)), mark(circle(13.7, 15, 0.9))]


def star_d(cx, cy, r, ri=None, n=5):
    ri = ri or r * 0.45
    return poly([polar(cx, cy, r if i % 2 == 0 else ri, -90 + i * 180 / n) for i in range(2 * n)], closed=True)


def eye_d(cx, cy, w, h):
    return f"M{fmt(cx - w)} {fmt(cy)}Q{fmt(cx)} {fmt(cy - h)} {fmt(cx + w)} {fmt(cy)}Q{fmt(cx)} {fmt(cy + h)} {fmt(cx - w)} {fmt(cy)}Z"


@icon("favicon", CAT, "Browser tab and page with a small star in the page area, the little icon shown on a tab.",
      tags=["favicon", "tab icon", "site icon", "browser tab", "bookmark icon", "website logo"])
def _(S):
    body = poly([(2, 21), (2, 4), (11, 4), (11, 8), (22, 8), (22, 21)], closed=True, r=S.r)
    return [shell(body), mark(star_d(12, 15, 4.6))]


@icon("web-accessibility", CAT, "Browser window with a small person with outstretched arms in the page area.",
      tags=["accessibility", "a11y", "inclusive web", "wcag", "screen reader", "accessible website"])
def _(S):
    return win(S) + [mark(circle(12, 10.3, 1.3)), detail(seg(8, 13, 16, 13)), detail(seg(12, 13, 12, 16)),
                     detail(poly([(10, 19.3), (12, 16), (14, 19.3)], r=S.r))]


@icon("cors-policy", CAT, "Globe with a small shield at its lower corner, the guard on requests between websites.",
      tags=["cors", "cross origin", "web security", "same origin", "http headers", "allowed origins"])
def _(S):
    sh = poly([(18, 14.5), (21, 15.5), (21, 18.5), (18, 21.5), (15, 18.5), (15, 15.5)], closed=True, r=S.r * 0.7)
    return [shell(circle(9, 9, 6)), detail(ellipse(9, 9, 2.6, 6)), detail(seg(3, 9, 15, 9)), shell(sh)]


@icon("url-shortener", CAT, "Chain link squeezed by two arrows pressing in from above and below.",
      tags=["short link", "link shortener", "compress url", "short url", "redirect", "link management"])
def _(S):
    return [line("M12 9H9A3 3 0 0 0 9 15H12"), line("M12 9H15A3 3 0 0 1 15 15H12"), line(seg(9.5, 12, 14.5, 12)),
            line(seg(12, 2, 12, 5)), line(poly([(10, 3.7), (12, 5.7), (14, 3.7)], r=S.r)),
            line(seg(12, 22, 12, 19)), line(poly([(10, 20.3), (12, 18.3), (14, 20.3)], r=S.r))]


@icon("web-scraper", CAT, "Browser window with a spider crawling across the page area to collect data.",
      tags=["scraper", "crawler", "spider", "data extraction", "web harvesting", "bot"])
def _(S):
    legs = []
    for sx in (-1, 1):
        for (x0, y0, x1, y1) in ((1.8, 13.3, 4.8, 10.8), (2.2, 14.9, 5.5, 15.1), (1.8, 16.5, 4.2, 19.3)):
            legs.append(detail(seg(12 + sx * x0, y0, 12 + sx * x1, y1)))
    return win(S) + legs + [mark(circle(12, 15, 2)), mark(circle(12, 11.9, 1.3))]


@icon("headless-browser", CAT, "Browser window with a crossed out eye in the page area, a browser that runs with no visible screen.",
      tags=["headless", "automation", "scripted browser", "no ui", "testing", "background browser"])
def _(S):
    return win(S) + [detail(eye_d(12, 14.3, 5.5, 4.2)), mark(circle(12, 14.3, 1.3)), detail(seg(8, 19, 16, 9.8))]


@icon("iframe-embed", CAT, "Browser window with a smaller framed window inside its page area.",
      tags=["iframe", "embed", "inline frame", "embedded page", "nested window", "widget"])
def _(S):
    return win(S) + [detail(rect(6, 10.5, 12, 7, rr(S, 1.5)))]


@icon("neural-network", CAT, "Three columns of nodes with every node joined to all nodes in the next column.",
      tags=["neural network", "deep learning", "layers", "nodes", "machine learning", "ai"])
def _(S):
    A = [(4, 7), (4, 17)]
    B = [(12, 7), (12, 17)]
    C = [(20, 7), (20, 17)]
    parts = [line(seg(*a, *b)) for a in A for b in B] + [line(seg(*b, *c)) for b in B for c in C]
    return parts + [node(S, x, y, 2.2) for x, y in A + B + C]


@icon("ai-agent", CAT, "Robot head beside a short checklist of three lines.",
      tags=["ai agent", "autonomous agent", "assistant", "task list", "bot", "automation"])
def _(S):
    return robot(S, 2.5, 9, 11, 9, 1.2) + [line(seg(17, 8, 21.5, 8)), line(seg(17, 12.5, 21.5, 12.5)),
                                            line(seg(17, 17, 21.5, 17))]


@icon("large-language-model", CAT, "Open book of text with a sparkle above it for a model trained on writing.",
      tags=["llm", "language model", "text generator", "text model", "generative ai", "chatbot"])
def _(S):
    book = "M3 10C6 9 9 9.5 12 11.5C15 9.5 18 9 21 10V20C18 19 15 19.5 12 21.5C9 19.5 6 19 3 20Z"
    return [shell(book), detail(seg(12, 11.5, 12, 21.5)), mark(sparkle(12, 5, 3.8)), mark(sparkle(19, 5.5, 1.9))]


@icon("prompt-input", CAT, "Text field with a blinking cursor on the left and a sparkle send button on the right.",
      tags=["prompt", "ai chat input", "message box", "text box", "ask ai", "chat field"])
def _(S):
    return [shell(rect(2, 6, 20, 12, rr(S, 4))), mark(rect(5.5, 9.5, 1.5, 5)), mark(sparkle(17, 12, 3.6))]


@icon("prompt-engineering", CAT, "Text field with two lines of text and a wrench standing beside it.",
      tags=["prompt design", "prompting", "tuning prompts", "instructions", "wrench", "ai tooling"])
def _(S):
    return [shell(rect(2, 4, 11, 15, rr(S, 2))), detail(seg(5.5, 9, 9.5, 9)), detail(seg(5.5, 13, 9.5, 13)),
            line(arc(18.5, 8, 2.6, 310, 590)), line(seg(18.5, 10.6, 18.5, 21))]


@icon("vector-embedding", CAT, "Three arrows fanning out from one origin point to three points in space.",
      tags=["embedding", "vectors", "semantic space", "latent space", "similarity", "word vectors"])
def _(S):
    o = (5, 19)
    parts = []
    for t in ((19.5, 15), (16, 4.5), (6, 4.5)):
        parts += arrow(S, o, t, 2.4)
    return parts + [dot(*o, 1.9)]


@icon("attention-mechanism", CAT, "Four small nodes along the bottom all linked to one larger highlighted node above.",
      tags=["attention", "self attention", "focus", "token weights", "transformer", "weights"])
def _(S):
    top = (12, 5)
    xs = (3.5, 9, 15, 20.5)
    return [line(seg(x, 19, *top)) for x in xs] + [node(S, x, 19, 1.7) for x in xs] + [node(S, *top, 2.7)]


@icon("transformer-model", CAT, "Eye above two stacked layer blocks, the attention based network.",
      tags=["transformer", "encoder decoder", "self attention", "llm architecture", "layers", "blocks"])
def _(S):
    return [line(eye_d(12, 5, 8, 3.4)), mark(circle(12, 5, 1.3)),
            shell(rect(4, 10, 16, 4, rr(S, 1.5))), shell(rect(4, 17, 16, 4, rr(S, 1.5)))]


def bubble_d(R, x=2, y=3, w=20, h=14, tail_x=7, tail_h=5):
    """Speech bubble outline with a tail on the bottom edge."""
    r, b = x + w, y + h
    return (f"M{fmt(x + R)} {fmt(y)}H{fmt(r - R)}A{fmt(R)} {fmt(R)} 0 0 1 {fmt(r)} {fmt(y + R)}V{fmt(b - R)}"
            f"A{fmt(R)} {fmt(R)} 0 0 1 {fmt(r - R)} {fmt(b)}H{fmt(tail_x + 5)}L{fmt(tail_x)} {fmt(b + tail_h)}V{fmt(b)}"
            f"H{fmt(x + R)}A{fmt(R)} {fmt(R)} 0 0 1 {fmt(x)} {fmt(b - R)}V{fmt(y + R)}A{fmt(R)} {fmt(R)} 0 0 1 {fmt(x + R)} {fmt(y)}Z")


@icon("generative-ai", CAT, "Picture frame with a mountain and sun above it and a large sparkle at the corner.",
      tags=["generative ai", "ai art", "image generation", "create with ai", "sparkle", "synthetic media"])
def _(S):
    return [shell(rect(2, 6, 16, 15, rr(S, 3))),
            detail(poly([(2, 18), (7, 13), (10.5, 16.5), (13, 14), (18, 18.5)])),
            mark(circle(13.5, 10.3, 1.2)), mark(sparkle(18.5, 5.5, 4))]


@icon("text-to-image", CAT, "Letter T with an arrow pointing to a small framed picture.",
      tags=["text to image", "prompt to picture", "image generator", "ai art", "diffusion", "render"])
def _(S):
    return [line(seg(2.5, 6, 8.5, 6)), line(seg(5.5, 6, 5.5, 18)),
            line(seg(10, 12, 13.5, 12)), line(poly([(12, 10.3), (13.7, 12), (12, 13.7)], r=S.r)),
            shell(rect(16.5, 7, 5, 10, rr(S, 2))), mark(circle(19, 10.5, 0.9)),
            mark(poly([(17.8, 15.2), (19, 13), (20.2, 15.2)], closed=True))]


@icon("text-to-speech", CAT, "Letter T with an arrow pointing to curved sound waves.",
      tags=["text to speech", "tts", "read aloud", "voice synthesis", "narration", "speech output"])
def _(S):
    return [line(seg(2.5, 6, 8.5, 6)), line(seg(5.5, 6, 5.5, 18)),
            line(seg(10, 12, 13, 12)), line(poly([(11.5, 10.3), (13.2, 12), (11.5, 13.7)], r=S.r)),
            line(arc(14, 12, 3.6, -50, 50)), line(arc(14, 12, 7, -50, 50))]


@icon("computer-vision", CAT, "Processor chip with pins on every side and an eye in the middle.",
      tags=["computer vision", "machine vision", "image recognition", "ai eye", "vision chip", "sight"])
def _(S):
    pins = []
    for v in (9.5, 14.5):
        pins += [line(seg(v, 2.5, v, 5)), line(seg(v, 19, v, 21.5)), line(seg(2.5, v, 5, v)), line(seg(19, v, 21.5, v))]
    return [shell(rect(5, 5, 14, 14, rr(S, 3))), detail(eye_d(12, 12, 4.4, 3)), mark(circle(12, 12, 1.1))] + pins


@icon("object-detection", CAT, "Two bounding boxes, each drawn tightly around a different simple shape.",
      tags=["object detection", "bounding box", "detector", "image recognition", "annotation", "vision"])
def _(S):
    tri = poly([(14.5, 20), (17, 15.5), (19.5, 20)], closed=True)
    return [shell(rect(2.5, 3, 11, 8.5, L(S, 1, 3))), mark(circle(8, 7.2, 1.9)),
            shell(rect(10.5, 14, 11, 8, L(S, 1, 3))), mark(tri)]


@icon("image-segmentation", CAT, "Picture frame with a mountain skyline split into separate outlined regions.",
      tags=["segmentation", "image regions", "semantic segmentation", "masks", "vision", "pixel labels"])
def _(S):
    return [shell(rect(2, 3, 20, 18, rr(S, 3))),
            detail(poly([(2, 16), (8, 10), (13, 14.5), (16.5, 11.5), (22, 16.5)])),
            detail(seg(8, 10, 8, 21)), detail(seg(16.5, 11.5, 16.5, 21)), mark(circle(16.5, 7, 1.3))]


@icon("pose-estimation", CAT, "Stick figure built from joint dots joined by lines, with arms and legs bent.",
      tags=["pose estimation", "skeleton tracking", "body tracking", "keypoints", "motion capture", "joints"])
def _(S):
    pts = [(12, 3.5), (7, 9), (17, 9), (4.5, 14), (19.5, 14), (12, 14), (8.5, 18.5), (15.5, 18.5), (7, 22), (17, 22)]
    segs = [((12, 6.5), (12, 14)), ((7, 9), (17, 9)), ((7, 9), (4.5, 14)), ((17, 9), (19.5, 14)),
            ((12, 14), (8.5, 18.5)), ((8.5, 18.5), (7.5, 21.5)), ((12, 14), (15.5, 18.5)), ((15.5, 18.5), (16.5, 21.5))]
    return [line(seg(*a, *b)) for a, b in segs] + [dot(x, y, 1.5 if i else 2.2) for i, (x, y) in enumerate(pts)]


@icon("natural-language-processing", CAT, "Speech bubble with a gear inside for software that works with human language.",
      tags=["nlp", "language processing", "text analysis", "linguistics", "chatbot", "language ai"])
def _(S):
    return [shell(bubble_d(L(S, 2, 4), 2, 2.5, 20, 15, 7, 4.5))] + gear(S, 12, 10, 4.2, 3.0, 6, 1.0, k=detail)


@icon("sentiment-analysis", CAT, "Speech bubble holding a smiling face, used to rate whether text is positive.",
      tags=["sentiment", "opinion mining", "emotion detection", "tone analysis", "positive negative", "text mood"])
def _(S):
    return [shell(bubble_d(L(S, 2, 4), 2, 2.5, 20, 15, 7, 4.5)), mark(circle(9, 8.5, 1.2)), mark(circle(15, 8.5, 1.2)),
            detail(arc(12, 9, 3.8, 40, 140))]


@icon("data-classification", CAT, "Circle, square and triangle each above a matching open bin.",
      tags=["classification", "sorting data", "categories", "labels", "bins", "supervised learning"])
def _(S):
    bins = [line(poly([(x - 2, 13.5), (x - 2, 21), (x + 2, 21), (x + 2, 13.5)], r=S.r)) for x in (5, 12, 19)]
    return bins + [mark(circle(5, 6.5, 2.2)), mark(rect(10, 4.5, 4, 4)),
                   mark(poly([(16.8, 8.7), (19, 4.5), (21.2, 8.7)], closed=True))]


@icon("data-clustering", CAT, "Three rings, each holding a small group of dots.",
      tags=["clustering", "k means", "groups", "unsupervised learning", "segments", "grouping"])
def _(S):
    parts = []
    for cx, cy in ((7, 7), (17, 7), (12, 16.5)):
        parts += [shell(circle(cx, cy, 4)), node(S, cx - 1.3, cy + 0.5, 1.1), node(S, cx + 1.3, cy - 0.5, 1.1)]
    return parts


@icon("decision-tree", CAT, "Diamond decision node splitting into two branches that end in round leaves.",
      tags=["decision tree", "branching", "classifier", "if else", "flowchart", "machine learning"])
def _(S):
    return [shell(poly([(12, 2.5), (16.5, 6), (12, 9.5), (7.5, 6)], closed=True, r=S.r)),
            line(poly([(6, 18.5), (6, 12.5), (18, 12.5), (18, 18.5)], r=S.r)), line(seg(12, 9.5, 12, 12.5)),
            dot(6, 19, 2.3), dot(18, 19, 2.3)]


@icon("random-forest", CAT, "Three Y shaped branching trees side by side, each ending in leaf dots.",
      tags=["random forest", "ensemble", "tree ensemble", "bagging", "decision trees", "machine learning"])
def _(S):
    parts = []
    for cx in (4.5, 12, 19.5):
        parts += [line(seg(cx, 21, cx, 14)), line(poly([(cx - 2.6, 7), (cx, 14), (cx + 2.6, 7)], r=S.r)),
                  node(S, cx - 2.6, 6, 1.4), node(S, cx + 2.6, 6, 1.4)]
    return parts


@icon("gradient-descent", CAT, "Bowl shaped curve with balls rolling down one side toward the lowest point.",
      tags=["gradient descent", "optimization", "minimum", "learning rate", "loss surface", "training"])
def _(S):
    return [line("M3 4Q12 36 21 4"), dot(5, 10.3, 2.3), dot(8, 16.8, 1.8), dot(12, 20, 1.3)]


@icon("loss-curve", CAT, "Axes with a curve that falls steeply and then levels off near the bottom.",
      tags=["loss curve", "training loss", "learning curve", "convergence", "error over time", "epochs"])
def _(S):
    return [line(poly([(3, 3), (3, 21), (21, 21)], r=S.r)), line("M7 5C8 16 11 17.5 20 18")]


@icon("overfitting", CAT, "Scatter of dots with a wiggly line that passes through every single dot.",
      tags=["overfitting", "overfit", "noise fitting", "variance", "model error", "generalization"])
def _(S):
    return [line("M2.5 15C5 15 5.5 7 8 7C10.5 7 9.5 16 12 16C14.5 16 13.5 8 16 8C18.5 8 18 14 21.5 14"),
            node(S, 8, 7, 1.9), node(S, 12, 16, 1.9), node(S, 16, 8, 1.9), node(S, 21, 14, 1.9), node(S, 3, 15, 1.9)]


BRAIN = ("M6.5 17C4.3 16.6 3 14.8 3 12.8C3 11.3 3.6 10.2 4.5 9.5C4.3 6.6 6.4 4.5 9 4.5C10.2 3.6 11.5 3.2 13 3.3"
         "C15.3 3.4 17 4.6 17.8 6.3C19.9 7 21 8.8 21 10.8C21 13.3 19.2 15.2 16.8 15.4C16.3 16.8 15 17.7 13.5 17.7L13.5 21H11V17.2Z")
BRAIN_DETAILS = ["M7.5 9.3C8.3 8.2 9.8 8 11 8.7", "M12.5 6.5C13.8 7 14.4 8.2 14.2 9.5",
                 "M8 13C9.3 13.8 11 13.6 12 12.5", "M15.5 11.5C16.8 11.5 17.8 10.8 18.3 9.8"]


def brain(S, cx, cy, k, details=True):
    """Side view brain scaled by k about its centre and moved to (cx, cy)."""
    m = (k, 0, 0, k, cx - 12 * k, cy - 12 * k)
    parts = [shell(tf(BRAIN, m))]
    if details:
        parts += [detail(tf(d, m)) for d in BRAIN_DETAILS[:4 if k >= 0.8 else (2 if k >= 0.58 else 0)]]
    return parts


def cyl(S, cx, y0, y1, rx, ry, bands=()):
    x1, x2 = cx - rx, cx + rx
    body = (f"M{fmt(x1)} {fmt(y0)}A{fmt(rx)} {fmt(ry)} 0 0 1 {fmt(x2)} {fmt(y0)}V{fmt(y1)}"
            f"A{fmt(rx)} {fmt(ry)} 0 0 1 {fmt(x1)} {fmt(y1)}Z")
    parts = [shell(body)]
    for y in (y0, *bands):
        parts.append(detail(f"M{fmt(x1)} {fmt(y)}A{fmt(rx)} {fmt(ry)} 0 0 0 {fmt(x2)} {fmt(y)}"))
    return parts


@icon("training-data", CAT, "Stack of data cylinders with an arrow pointing into a small brain.",
      tags=["training data", "dataset", "learning examples", "data feed", "corpus", "machine learning"])
def _(S):
    return (cyl(S, 6.5, 5, 18, 4.5, 2, bands=(11.5,)) +
            [line(seg(12.5, 12, 13.5, 12)), line(poly([(12, 10.5), (13.7, 12), (12, 13.5)], r=S.r))] +
            brain(S, 18, 12, 0.5, details=False))


@icon("data-labeling", CAT, "Picture frame with a mountain and a small price style tag hanging off its corner.",
      tags=["labeling", "annotation", "tagging data", "ground truth", "image tags", "dataset labels"])
def _(S):
    tag = poly([(19, 11), (21.5, 13.5), (21.5, 21), (16.5, 21), (16.5, 13.5)], closed=True, r=S.r * 0.6)
    return [shell(rect(2, 3, 12.5, 11, rr(S, 2))), detail(poly([(2, 12), (6, 7.5), (9, 10.5), (11, 8.5), (14.5, 12)])),
            shell(tag), mark(circle(19, 15, 0.9))]


@icon("model-training", CAT, "Brain above a progress bar that is partly filled, a model learning from data.",
      tags=["training", "learning", "epochs", "fit model", "progress", "machine learning"])
def _(S):
    return brain(S, 12, 9, 0.62) + [shell(rect(3, 17, 18, 4, L(S, 0.5, 2))), mark(rect(4, 18, 8, 2))]


@icon("model-inference", CAT, "Brain with a check mark beside it, a trained model returning an answer.",
      tags=["inference", "prediction", "model run", "serving", "forward pass", "ai result"])
def _(S):
    return brain(S, 9.5, 9, 0.8) + [line(poly([(14, 18), (17, 21), (22, 15.5)], r=S.r))]


@icon("fine-tuning", CAT, "Brain beside a round tuning knob with a pointer.",
      tags=["fine tuning", "adjust model", "calibrate", "tweak", "knob", "model adaptation"])
def _(S):
    return brain(S, 8.5, 12, 0.62) + [shell(circle(18.5, 12, 2.6)), detail(seg(18.5, 12, 18.5, 9.4)),
                                       line(seg(17, 18, 20, 18)), line(seg(17, 6, 20, 6))]


@icon("reinforcement-learning", CAT, "Small robot head with a looping arrow above it and a reward star.",
      tags=["reinforcement learning", "reward", "agent environment", "policy", "trial and error", "rl"])
def _(S):
    return (robot(S, 2.5, 12, 10, 8, 1.1) + carrow(S, 16.5, 7, 3.6, 40, 330, 1.9) + [mark(star_d(18.5, 17, 3.6))])


@icon("convolution-kernel", CAT, "Four by four grid with a two by two block of cells highlighted as the sliding filter.",
      tags=["convolution", "kernel", "filter", "cnn", "sliding window", "image processing"])
def _(S):
    return [shell(rect(2, 2, 20, 20, rr(S, 3))), detail(seg(7, 2, 7, 22)), detail(seg(12, 2, 12, 22)),
            detail(seg(17, 2, 17, 22)), detail(seg(2, 7, 22, 7)), detail(seg(2, 12, 22, 12)), detail(seg(2, 17, 22, 17)),
            mark(rect(3, 3, 3, 3)), mark(rect(8, 3, 3, 3)), mark(rect(3, 8, 3, 3)), mark(rect(8, 8, 3, 3))]


@icon("feature-map", CAT, "Grid in front of two offset grids behind it, a stack of feature channels.",
      tags=["feature map", "channels", "activation map", "cnn layer", "tensor slices", "layers"])
def _(S):
    return [shell(rect(2, 11, 12, 10, rr(S, 2))), detail(seg(8, 11, 8, 21)), detail(seg(2, 16, 14, 16)),
            line(poly([(5, 8), (17, 8), (17, 17.5)], r=S.r)), line(poly([(8, 5), (20, 5), (20, 14.5)], r=S.r))]


@icon("confusion-matrix", CAT, "Two by two grid with check marks in the two diagonal cells.",
      tags=["confusion matrix", "true positive", "false positive", "classifier accuracy", "evaluation", "metrics"])
def _(S):
    return [shell(rect(3, 3, 18, 18, rr(S, 3))), detail(seg(12, 3, 12, 21)), detail(seg(3, 12, 21, 12)),
            detail(poly([(5.8, 7.8), (7.5, 9.5), (10, 6)])), detail(poly([(14.8, 16.8), (16.5, 18.5), (19, 15)]))]


@icon("roc-curve", CAT, "Axes with a bowed curve rising above a dashed diagonal reference line.",
      tags=["roc", "auc", "receiver operating", "true positive rate", "classifier curve", "evaluation"])
def _(S):
    return [line(poly([(3, 3), (3, 21), (21, 21)], r=S.r)), line("M4 20C5 9 10 5 20 4"),
            line(seg(8, 16, 9.5, 14.5)), line(seg(12.5, 11.5, 14, 10)), line(seg(17, 7, 18.5, 5.5))]


@icon("hyperparameter", CAT, "Small brain beside three slider controls with knobs at different positions.",
      tags=["hyperparameter", "settings", "learning rate", "tuning", "config", "sliders"])
def _(S):
    parts = brain(S, 7.5, 12, 0.62)
    for y, kx in ((6, 18), (12, 21), (18, 17)):
        parts += [line(seg(15, y, 22, y)), node(S, kx - 1, y, 1.9)]
    return parts


@icon("model-weights", CAT, "Kettlebell whose round body holds a tiny three node network.",
      tags=["weights", "parameters", "checkpoint", "model file", "heavy model", "learned values"])
def _(S):
    body = "M6 21.5L4.5 15.5A7.5 7.5 0 0 1 19.5 15.5L18 21.5Z"
    return [line(poly([(7.5, 10), (7.5, 4.5), (16.5, 4.5), (16.5, 10)], r=S.r)), shell(body),
            detail(seg(9.5, 16.5, 14.5, 14.5)), detail(seg(14.5, 14.5, 13.2, 19)), detail(seg(9.5, 16.5, 13.2, 19)),
            mark(circle(9.5, 16.5, 1.2)), mark(circle(14.5, 14.5, 1.2)), mark(circle(13.2, 19, 1.2))]


@icon("retrieval-augmented-generation", CAT, "Document page, a magnifying glass below it and a sparkle above for answers grounded in sources.",
      tags=["rag", "retrieval", "grounded answers", "search then generate", "knowledge base", "citations"])
def _(S):
    return [shell(rect(2, 3, 9, 12, rr(S, 2))), detail(seg(4.5, 7, 8.5, 7)), detail(seg(4.5, 10.5, 8.5, 10.5)),
            shell(circle(16.5, 16.5, 3.4)), line(seg(19.2, 19.2, 21.5, 21.5)), mark(sparkle(17, 6, 4.4))]


@icon("context-window", CAT, "Window frame holding two rows of small token squares.",
      tags=["context window", "tokens", "prompt length", "memory limit", "input size", "llm limit"])
def _(S):
    return [shell(rect(2, 4, 20, 16, rr(S, 3))),
            mark(rect(5.5, 7.5, 3.5, 3.5)), mark(rect(10.25, 7.5, 3.5, 3.5)), mark(rect(15, 7.5, 3.5, 3.5)),
            mark(rect(5.5, 13, 3.5, 3.5)), mark(rect(10.25, 13, 3.5, 3.5))]


def spiral_d(cx, cy, r0, r1, turns=2.0, n=26):
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append(polar(cx, cy, r0 + (r1 - r0) * t, -90 + 360 * turns * t))
    return poly(pts, r=0)


@icon("ai-hallucination", CAT, "Robot head with a swirl floating above it, a model imagining things that are not there.",
      tags=["hallucination", "made up answer", "confabulation", "ai error", "dizzy", "false output"])
def _(S):
    return [line(spiral_d(12, 6.3, 0.6, 4.2, 1.8)), shell(rect(4, 13, 16, 8.5, rr(S, 3))),
            mark(circle(9, 16.5, 1.3)), mark(circle(15, 16.5, 1.3)), detail(seg(9.5, 19.5, 14.5, 19.5))]


def hexv(cx, cy, r):
    return [polar(cx, cy, r, -90 + i * 60) for i in range(6)]


def mid(a, b):
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


@icon("synthetic-data", CAT, "Table grid with a pair of sparkles at its corner, rows of data created by a generator.",
      tags=["synthetic data", "generated data", "fake data", "data augmentation", "mock dataset", "simulated rows"])
def _(S):
    return [shell(rect(2, 8, 13, 13, L(S, 1, 3))), detail(seg(2, 13, 15, 13)), detail(seg(8.5, 8, 8.5, 21)),
            mark(sparkle(18, 6, 4.2)), mark(sparkle(19.5, 14, 1.9))]


@icon("anomaly-detection", CAT, "Row of ordinary dots with one dot floating far above them inside a ring.",
      tags=["anomaly", "outlier", "fraud detection", "unusual value", "abnormal", "monitoring"])
def _(S):
    return [node(S, 4, 17, 1.6), node(S, 9, 16, 1.6), node(S, 14, 18, 1.6), node(S, 19, 16.5, 1.6),
            shell(circle(12, 6.5, 3.8)), node(S, 12, 6.5, 1.3)]


@icon("recommendation-engine", CAT, "Gear with a star at its centre, the machinery that picks what you may like next.",
      tags=["recommendation", "recommender", "suggested for you", "personalisation", "personalization", "taste"])
def _(S):
    return [shell(gear_d(12, 12, 9.5, 7.2, 8, 0.5)), mark(star_d(12, 12, 4))]


@icon("digital-twin", CAT, "A solid cube beside an identical cube drawn with broken edges, the real object and its copy.",
      tags=["digital twin", "virtual copy", "simulation", "mirror model", "iot", "replica"])
def _(S):
    def cube(cx, cy, r):
        v = hexv(cx, cy, r)
        return v, [detail(seg(cx, cy, *v[i])) for i in (1, 3, 5)]
    v, inner = cube(7, 16, 4.6)
    parts = [shell(poly(v, closed=True, r=S.r * 0.6))] + [detail(seg(7, 16, *v[i])) for i in (1, 3, 5)]
    gv = hexv(17, 8, 4.6)
    for i in range(6):
        a, b = gv[i], gv[(i + 1) % 6]
        m = mid(a, b)
        parts.append(line(seg(m[0] + (a[0] - m[0]) * 0.55, m[1] + (a[1] - m[1]) * 0.55,
                              m[0] + (b[0] - m[0]) * 0.55, m[1] + (b[1] - m[1]) * 0.55)))
    return parts


@icon("humanoid-robot", CAT, "Full body robot with a square head, boxy torso, arms and two legs.",
      tags=["humanoid", "android", "bipedal robot", "robotics", "robot body", "automaton"])
def _(S):
    return [shell(rect(8, 2, 8, 6, rr(S, 2))), mark(circle(10.4, 5, 0.9)), mark(circle(13.6, 5, 0.9)),
            line(seg(12, 8, 12, 10)), shell(rect(6.5, 10, 11, 7, rr(S, 2))), mark(circle(12, 13.5, 1.2)),
            line(seg(3.5, 10.5, 3.5, 16)), line(seg(20.5, 10.5, 20.5, 16)),
            line(seg(9.5, 17, 9.5, 21.5)), line(seg(14.5, 17, 14.5, 21.5))]


@icon("multi-agent-system", CAT, "Three small robot heads joined by lines in a triangle.",
      tags=["multi agent", "agents", "swarm", "collaboration", "orchestration", "agent network"])
def _(S):
    def head(x, y):
        return [shell(rect(x, y, 7, 6, rr(S, 2))), mark(circle(x + 2.2, y + 3, 0.8)), mark(circle(x + 4.8, y + 3, 0.8))]
    return (head(8.5, 2.5) + head(2, 15.5) + head(15, 15.5) +
            [line(seg(10.5, 10, 7, 14)), line(seg(13.5, 10, 17, 14)), line(seg(10.8, 18.5, 13.2, 18.5))])


@icon("ai-model", CAT, "Cube with a small three node network drawn on its right face.",
      tags=["ai model", "model", "neural model", "3d model", "network cube", "machine learning"])
def _(S):
    v = hexv(12, 12, 9.3)
    return [shell(poly(v, closed=True, r=S.r * 0.6))] + [detail(seg(12, 12, *v[i])) for i in (1, 3, 5)] + [
        detail(seg(15.3, 14.5, 18, 11.8)), detail(seg(15.3, 14.5, 16.8, 17.2)), detail(seg(18, 11.8, 16.8, 17.2)),
        mark(circle(15.3, 14.5, 1.1)), mark(circle(18, 11.8, 1.1)), mark(circle(16.8, 17.2, 1.1))]


@icon("neural-processing-unit", CAT, "Processor chip with pins on every side and a tiny three node network in the middle.",
      tags=["npu", "ai accelerator", "neural chip", "tensor chip", "ai processor", "inference chip"])
def _(S):
    pins = []
    for v in (9.5, 14.5):
        pins += [line(seg(v, 2.5, v, 5)), line(seg(v, 19, v, 21.5)), line(seg(2.5, v, 5, v)), line(seg(19, v, 21.5, v))]
    return [shell(rect(5, 5, 14, 14, rr(S, 3))), detail(poly([(8.5, 12), (15.5, 8.5), (15.5, 15.5)], closed=True)),
            mark(circle(8.5, 12, 1.4)), mark(circle(15.5, 8.5, 1.4)), mark(circle(15.5, 15.5, 1.4))] + pins


@icon("gpu-graphics-card", CAT, "Long graphics card with two round fans, a mounting bracket at one end and edge connector below.",
      tags=["gpu", "graphics card", "video card", "pc hardware", "render", "pcie"])
def _(S):
    return [shell(rect(5, 5, 17, 12, rr(S, 3))), detail(circle(10.5, 11, 3.4)), detail(circle(17, 11, 3.4)),
            mark(circle(10.5, 11, 1.1)), mark(circle(17, 11, 1.1)),
            line(seg(2, 4, 2, 18.5)), line(seg(8, 20.5, 19, 20.5))]


@icon("tensor-cube", CAT, "Cube with a dividing line across each face, a block of multi dimensional numbers.",
      tags=["tensor", "3d array", "multi dimensional", "ndarray", "data cube", "deep learning"])
def _(S):
    v = hexv(12, 12, 9.3)
    c = (12, 12)
    top = [c, v[5], v[0], v[1]]
    left = [c, v[5], v[4], v[3]]
    right = [c, v[1], v[2], v[3]]
    cuts = []
    for f in (top, left, right):
        cuts.append(detail(seg(*mid(f[0], f[1]), *mid(f[2], f[3]))))
    return [shell(poly(v, closed=True, r=S.r * 0.6))] + [detail(seg(12, 12, *v[i])) for i in (1, 3, 5)] + cuts


@icon("perceptron", CAT, "Three input lines merging into one circle that has a single arrow leaving it.",
      tags=["perceptron", "single neuron", "inputs and output", "weighted sum", "artificial neuron", "ai basics"])
def _(S):
    ins = [(3, 5), (3, 12), (3, 19)]
    return ([line(seg(*p, 10.8, 12)) for p in ins] + [node(S, *p, 1.7) for p in ins] +
            [shell(circle(14, 12, 3.8)), line(seg(18.8, 12, 22, 12))])


@icon("activation-function", CAT, "Axes with an S shaped curve that flattens at both ends.",
      tags=["activation function", "sigmoid", "nonlinearity", "relu style", "neuron output", "curve"])
def _(S):
    return [line(poly([(3, 3), (3, 21), (21, 21)], r=S.r)), line("M6 17C12 17 12 7 20 7")]


@icon("chain-of-thought", CAT, "Two speech bubbles with an arrow stepping from the first down to the second.",
      tags=["chain of thought", "reasoning steps", "step by step", "thinking", "llm reasoning", "intermediate steps"])
def _(S):
    return [shell(rect(2, 3, 11, 6.5, rr(S, 2.5))), shell(rect(11, 14.5, 11, 6.5, rr(S, 2.5))),
            line(poly([(5.5, 12), (5.5, 17.7), (8, 17.7)], r=S.r)), line(poly([(6.9, 16.2), (8.4, 17.7), (6.9, 19.2)], r=S.r))]


@icon("ai-safety", CAT, "Shield with a sparkle in the middle, protection for artificial intelligence systems.",
      tags=["ai safety", "alignment", "guardrails", "responsible ai", "trust", "protection"])
def _(S):
    sh = poly([(12, 2.5), (20, 5.5), (20, 12), (17.5, 18.5), (12, 21.7), (6.5, 18.5), (4, 12), (4, 5.5)], closed=True,
              r=L(S, 0.5, 3))
    return [shell(sh), mark(sparkle(12, 12, 5))]


@icon("motherboard", CAT, "Square circuit board with a processor socket, memory slots and an expansion slot.",
      tags=["motherboard", "mainboard", "pc board", "circuit board", "computer hardware", "pcb"])
def _(S):
    return [shell(rect(2, 2, 20, 20, rr(S, 3))), detail(rect(5, 5, 7, 7, rr(S, 1))),
            detail(seg(16, 5, 16, 12)), detail(seg(19, 5, 19, 12)), detail(seg(5, 17, 14, 17)), mark(rect(17, 15.5, 2.5, 3))]


@icon("cpu-cooler", CAT, "Square heat sink block with a round fan on its face and a screw in each corner.",
      tags=["cpu cooler", "fan", "cooling", "pc cooling", "air cooler", "thermal"])
def _(S):
    blades = [detail(arc(12, 12, 3.4, a, a + 75)) for a in (-80, 40, 160)]
    return [shell(rect(2, 2, 20, 20, rr(S, 3))), detail(circle(12, 12, 6.3))] + blades + [mark(circle(12, 12, 1.1))] + [
        mark(circle(x, y, 0.9)) for x, y in ((4.8, 4.8), (19.2, 4.8), (4.8, 19.2), (19.2, 19.2))]


@icon("heat-sink", CAT, "Metal base with tall parallel fins rising from its top.",
      tags=["heatsink", "heat sink", "fins", "cooling", "radiator", "pc part"])
def _(S):
    return [shell(rect(3, 15, 18, 6, rr(S, 2))), line(seg(5, 3, 5, 15)), line(seg(9.7, 3, 9.7, 15)),
            line(seg(14.3, 3, 14.3, 15)), line(seg(19, 3, 19, 15))]


@icon("thermal-paste", CAT, "Syringe pushing a dab of grey paste onto a flat chip surface.",
      tags=["thermal paste", "thermal compound", "cpu paste", "heat transfer", "pc building", "syringe"])
def _(S):
    return [line(seg(9, 2.5, 15, 2.5)), line(seg(12, 2.5, 12, 5)), shell(rect(8.5, 5, 7, 8, rr(S, 1.5))),
            line(seg(12, 13, 12, 16)), mark(ellipse(12, 18.4, 3.6, 1.5)), line(seg(3, 21, 21, 21))]


@icon("power-supply-unit", CAT, "Boxy power supply with a round fan grille on its face and two cables leaving the side.",
      tags=["psu", "power supply", "pc power", "atx", "computer hardware", "cables"])
def _(S):
    blades = [detail(arc(10, 12, 3, a, a + 75)) for a in (-80, 40, 160)]
    return [shell(rect(2, 4, 16, 16, rr(S, 3))), detail(circle(10, 12, 5.6))] + blades + [mark(circle(10, 12, 1))] + [
        line(seg(18, 9, 22, 9)), line(seg(18, 15, 22, 15))]
