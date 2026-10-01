"""TypeIcon Core: web (batch 004): captchas, forms, marketing, monitoring and browser security."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from dsl import I
from geometry import LINE, circle_d, fmt, polar

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



# ============================================================================ forms and captchas

@icon("form-builder", CAT, "Form sheet with field bars and an arrow cursor placing a new field",
      tags=["form designer", "drag and drop form", "form editor", "survey builder", "field editor", "no code form"])
def _(S):
    return [
        shell(rect(2, 3, 13, 18, min(S.R, 3))),
        detail(seg(5, 8, 12, 8)), detail(seg(5, 12, 12, 12)), detail(seg(5, 16, 9, 16)),
        cursor(S, 17, 11, 0.95),
    ]


@icon("character-limit", CAT, "Text area box with a small slash counter in its lower right corner",
      tags=["max length", "character count", "text counter", "word limit", "textarea", "input limit"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, min(S.R, 3))),
        detail(seg(5, 7.5, 19, 7.5)), detail(seg(5, 11, 14, 11)),
        line(seg(16.5, 18, 18.5, 14.5)),
        line(seg(13, 13.5, 13, 16.5)), line(seg(20, 15.5, 20, 18.5)),
    ]


@icon("image-captcha-grid", CAT, "Three by three grid of image tiles with two tiles ticked",
      tags=["captcha", "select all images", "human check", "verification grid", "bot test"])
def _(S):
    return [
        shell(rect(2, 2, 20, 20, min(S.R, 3))),
        detail(seg(8.67, 2, 8.67, 22)), detail(seg(15.33, 2, 15.33, 22)),
        detail(seg(2, 8.67, 22, 8.67)), detail(seg(2, 15.33, 22, 15.33)),
        Part("dot", rect(10.8, 4.8, 2.4, 2.4)), Part("dot", rect(4.8, 17.8, 2.4, 2.4)),
    ]


@icon("puzzle-captcha", CAT, "Picture frame with a puzzle piece gap and a slider bar with a knob underneath",
      tags=["slider captcha", "slide to verify", "jigsaw captcha", "human check", "drag puzzle", "bot test"])
def _(S):
    gap = L(S, "M13 8H14.5A1.5 1.5 0 1 1 17.5 8H19V13H13Z",
            "M13.8 8H14.5A1.5 1.5 0 1 1 17.5 8H18.2Q19 8 19 8.8V12.2Q19 13 18.2 13H13.8Q13 13 13 12.2V8.8Q13 8 13.8 8Z")
    return [
        shell(rect(2, 2.5, 20, 12, min(S.R, 3))),
        detail(poly([(2, 12), (6.5, 8), (10, 11)], r=S.r)),
        detail(gap),
        shell(rect(2, 17.5, 20, 4.5, 2.25)),
        dot(5.5, 19.75, 1.2),
    ]


@icon("address-autocomplete", CAT, "Input field with a map pin and a dropdown of two suggestion lines",
      tags=["address lookup", "location search", "place suggestions", "typeahead", "geocoding", "autosuggest"])
def _(S):
    pin = L(S, "M6.5 9.5L4.3 6.2A2.7 2.7 0 1 1 8.7 6.2Z", "M6.5 9.4L4.5 6.4A2.5 2.5 0 1 1 8.5 6.4Z")
    return [
        shell(rect(2, 2, 20, 8, min(S.R, 3))),
        solid(pin),
        detail(seg(12, 6, 19, 6)),
        dot(4.5, 14.5, 1.1), line(seg(8, 14.5, 20, 14.5)),
        dot(4.5, 19.5, 1.1), line(seg(8, 19.5, 16, 19.5)),
    ]


@icon("booking-form", CAT, "Form sheet with a small calendar at the top and two field lines below",
      tags=["reservation form", "appointment form", "schedule form", "date picker form", "book now", "reserve"])
def _(S):
    return [
        shell(rect(3, 2, 18, 20, min(S.R, 3))),
        shell(rect(6, 5, 12, 6, 1)),
        detail(seg(6, 7.4, 18, 7.4)),
        detail(seg(6, 15, 18, 15)), detail(seg(6, 18.5, 13, 18.5)),
    ]


@icon("broken-image", CAT, "Image frame with a mountain and a jagged torn split down the middle",
      tags=["image error", "missing image", "failed to load", "404 image", "image not found", "torn picture"])
def _(S):
    left = [(2, 3), (11, 3), (9, 8), (12, 11.5), (9, 16), (11, 21), (2, 21)]
    right = [(15, 3), (22, 3), (22, 21), (15, 21), (13, 16), (16, 11.5), (13, 8)]
    return [
        shell(poly(left, closed=True, r=S.r)),
        shell(poly(right, closed=True, r=S.r)),
        detail(poly([(2, 17), (6, 12.5), (9, 16)], r=S.r)),
        dot(5.5, 7.5, 1.1),
    ]


@icon("event-listener", CAT, "Ear beside a button shape with small sound arcs between them",
      tags=["event handler", "listen", "onclick", "javascript events", "callback", "subscribe"])
def _(S):
    ear = "M3 9.5A4.5 4.5 0 0 1 12 9.5C12 12.2 9 12.6 9 15.2A2.5 2.5 0 0 1 4 15.2"
    return [
        line(ear),
        detail("M6.5 9.5A1.5 1.5 0 0 1 9 9.5"),
        line(arc(11, 12.5, 2.6, -45, 45)),
        shell(rect(16.5, 8, 5.5, 8, 2.75)),
    ]


@icon("hreflang-tag", CAT, "Two pages each showing a different script letter, joined by a two way arrow",
      tags=["hreflang", "language tag", "alternate language", "multilingual seo", "international seo", "locale link"])
def _(S):
    return [
        shell(rect(2, 2.5, 9, 12, min(S.R, 2.5))),
        shell(rect(13, 2.5, 9, 12, min(S.R, 2.5))),
        detail(poly([(4.7, 11.5), (6.5, 6), (8.3, 11.5)], r=0)), detail(seg(5.3, 9.6, 7.7, 9.6)),
        detail(poly([(15.5, 6.5), (17.5, 6.5), (17.5, 11.5)], r=0)), detail(seg(15.5, 11.5, 19.5, 11.5)),
        line(seg(4, 19, 20, 19)),
        head(S, (4, 19), 180, 2.6), head(S, (20, 19), 0, 2.6),
    ]


@icon("browser-sandbox", CAT, "Browser window sitting inside an open sandbox tray",
      tags=["sandboxed iframe", "isolation", "safe environment", "secure browsing", "contained", "sandbox attribute"])
def _(S):
    tray = L(S, "M2 11V21H22V11", "M2 11V18A3 3 0 0 0 5 21H19A3 3 0 0 0 22 18V11")
    return [
        shell(rect(6, 3, 12, 14, min(S.R, 3))),
        detail(seg(6, 7, 18, 7)),
        line(tray),
    ]


@icon("same-origin-policy", CAT, "Two browser windows side by side with a short brick wall between them",
      tags=["cors", "origin", "cross origin", "browser security", "domain isolation", "sop", "blocked request"])
def _(S):
    return [
        shell(rect(2, 6, 6, 11, L(S, 0, 2))), detail(seg(2, 9, 8, 9)),
        shell(rect(16, 6, 6, 11, L(S, 0, 2))), detail(seg(16, 9, 22, 9)),
        solid(rect(10.5, 3, 3, 5.5, L(S, 0, 0.8))), solid(rect(10.5, 9.5, 3, 5, L(S, 0, 0.8))), solid(rect(10.5, 15.5, 3, 5.5, L(S, 0, 0.8))),
    ]


@icon("content-marketing", CAT, "Megaphone with a small document page coming out of its bell",
      tags=["content strategy", "blog promotion", "publish content", "announce", "article marketing", "inbound content"])
def _(S):
    cone = [(2, 10), (5, 10), (11, 6.5), (11, 17.5), (5, 14), (2, 14)]
    return [
        shell(poly(cone, closed=True, r=S.r)),
        line(seg(6, 14.5, 7, 19.5)),
        shell(rect(15, 5, 7, 11, min(S.R, 2))),
        detail(seg(17.5, 9, 19.5, 9)), detail(seg(17.5, 12, 19.5, 12)),
    ]


# ============================================================================ marketing and monitoring

@icon("inbound-marketing", CAT, "Horseshoe magnet drawing three small person silhouettes toward it",
      tags=["attract customers", "lead generation", "magnet marketing", "organic traffic", "pull marketing", "draw in visitors"])
def _(S):
    u = L(S, "M6 12V9A6 6 0 0 1 18 9V12", "M6 11.5V9A6 6 0 0 1 18 9V11.5")
    out = [line(u), Part("solid", rect(4.5, 9, 3, 3)), Part("solid", rect(16.5, 9, 3, 3))]
    for x in (5.5, 12, 18.5):
        out += [dot(x, 16.3, 1.4), line(f"M{fmt(x - 2.2)} 21.5A2.2 2.2 0 0 1 {fmt(x + 2.2)} 21.5")]
    return out


@icon("personalized-email", CAT, "Envelope with a name label strip across its front",
      tags=["mail merge", "custom greeting", "name tag", "email personalization", "dynamic fields", "newsletter name"])
def _(S):
    return [
        shell(rect(2, 4, 20, 16, min(S.R, 3))),
        detail(poly([(2.5, 5.5), (12, 12), (21.5, 5.5)], r=S.r)),
        Part("dot", rect(7, 14, 10, 3, L(S, 0, 1.5))),
    ]


def pulse(S, y, a=2.6):
    return line(poly([(2, y), (7.5, y), (9.5, y - a), (12.5, y + a), (14.5, y), (22, y)], r=S.r * 0.6))


@icon("real-user-monitoring", CAT, "Person silhouette with a heartbeat pulse line running beneath",
      tags=["rum", "real user monitoring", "visitor performance", "field data", "web vitals", "user experience tracking"])
def _(S):
    return [
        shell(circle(12, 6, 3.5)),
        line("M5.5 14.5A6.5 6 0 0 1 18.5 14.5"),
        pulse(S, 19.5, 2.2),
    ]


@icon("synthetic-monitoring", CAT, "Small robot head with a heartbeat pulse line running beneath",
      tags=["synthetic tests", "scripted checks", "uptime probe", "bot monitoring", "automated test", "proactive monitoring"])
def _(S):
    return [
        shell(rect(5, 4.5, 14, 9, min(S.R, 3))),
        line(seg(12, 4.5, 12, 2)),
        dot(9.5, 9, 1.2), dot(14.5, 9, 1.2),
        pulse(S, 19.5, 2.2),
    ]


def _duo_filled():
    fr = "M2 3H22V21H2Z"
    body = U(P(rect(2, 3, 20, 18, 0)), ST(rect(2, 3, 20, 18, 0), 2, LINE.cap, LINE.join, 4))
    stripes = U(*[ST(seg(*c), 2, LINE.cap, LINE.join, 4) for c in ((12, 20, 21, 11), (12, 14.5, 21, 5.5), (12, 9, 17, 4))])
    return D(body, I(stripes, P(rect(12, 3, 11, 18, 0))))


@icon("duotone-image", CAT, "Image frame with the left half solid and the right half hatched",
      tags=["two tone", "duotone", "halftone", "photo filter", "image effect", "color overlay"], filled=_duo_filled)
def _(S):
    return [
        shell(rect(2, 3, 20, 18, min(S.R, 3))),
        solid(rect(4, 5, 7, 14, L(S, 0, 1))),
        line(seg(13.5, 19, 20, 12.5)), line(seg(13.5, 14, 20, 7.5)), line(seg(13.5, 9, 17, 5.5)),
    ]


@icon("free-shipping-bar", CAT, "Progress bar mostly filled above a small delivery truck",
      tags=["shipping threshold", "free delivery", "cart progress", "spend more", "ecommerce banner", "delivery goal"])
def _(S):
    cab = poly([(17, 13.5), (20, 13.5), (22, 16.5), (22, 18.5), (17, 18.5)], closed=True, r=S.r)
    return [
        shell(rect(2, 3, 20, 7, 3.5)),
        Part("dot", rect(4.5, 5.5, 12, 2, 1)),
        shell(rect(3, 13.5, 14, 5, L(S, 0, 1.5))),
        shell(cab),
        dot(7, 19.5, 1.8), dot(18.5, 19.5, 1.8),
    ]


@icon("math-captcha", CAT, "Input field showing a dot, a plus sign, a dot and an equals sign",
      tags=["arithmetic captcha", "sum question", "human check", "solve the sum", "bot test", "verification question"])
def _(S):
    return [
        shell(rect(2, 5.5, 20, 13, min(S.R, 4))),
        dot(5, 12, 1.1),
        detail(seg(7.5, 12, 10.5, 12)), detail(seg(9, 10.5, 9, 13.5)),
        dot(13, 12, 1.1),
        detail(seg(15.5, 11, 18.5, 11)), detail(seg(15.5, 13.2, 18.5, 13.2)),
    ]


def globe(S, cx, cy, r=4.5):
    return [shell(circle(cx, cy, r)), detail(seg(cx - r, cy, cx + r, cy)), detail(ellipse(cx, cy, r * 0.4, r))]


@icon("cross-domain-tracking", CAT, "Two globes at opposite corners with a small tag between them",
      tags=["cross site", "multi domain analytics", "linker", "visitor journey", "cookie sharing", "domain linking", "tracking"])
def _(S):
    return [
        *globe(S, 5.5, 5.5, 3.8), *globe(S, 18.5, 18.5, 3.8),
        shell(poly(regular(12, 12, 1.9, 4, -45), closed=True, r=S.r)),
    ]


@icon("buddy-list", CAT, "Narrow chat window with four name lines each led by a status dot",
      tags=["contacts list", "friends online", "instant messenger", "presence", "roster", "chat contacts", "status"])
def _(S):
    out = [shell(rect(4, 2, 16, 20, min(S.R, 3))), detail(seg(4, 6, 20, 6))]
    for y in (9.5, 12.8, 16.1, 19.4):
        out += [dot(8, y, 1.0), detail(seg(11, y, 17, y))]
    return out


@icon("chain-email", CAT, "Envelope with two interlocked chain links hanging below it",
      tags=["chain letter", "forwarded message", "spam chain", "viral email", "send to ten friends", "hoax email"])
def _(S):
    return [
        shell(rect(5, 2, 17, 10, min(S.R, 3))),
        detail(poly([(5.5, 3.5), (13.5, 8.5), (21.5, 3.5)], r=S.r)),
        line(rect(2, 15.5, 11, 6, L(S, 2.5, 3))),
        line(rect(10, 15.5, 12, 6, L(S, 2.5, 3))),
    ]


@icon("listicle", CAT, "Article page with three rows each holding a marker, an image block and a text line",
      tags=["list article", "top ten", "numbered list post", "ranked list", "roundup", "slideshow post"])
def _(S):
    out = [shell(rect(2, 2, 20, 20, min(S.R, 3)))]
    for y in (7.5, 12.5, 17.5):
        out += [dot(5.5, y, 1.1), Part("dot", rect(8.5, y - 2, 4.5, 4, L(S, 0, 1))), detail(seg(15.5, y, 19, y))]
    return out


@icon("live-blog", CAT, "Post page with a solid live dot at the top of a short vertical timeline of entries",
      tags=["live updates", "real time feed", "liveblogging", "breaking news", "event coverage", "timeline feed"])
def _(S):
    return [
        shell(rect(2, 2, 20, 20, min(S.R, 3))),
        dot(7, 7, 2.2), detail(seg(12, 7, 19, 7)),
        detail(seg(7, 10, 7, 14)),
        dot(7, 12, 0.01) if False else dot(7, 17, 1.6), detail(seg(12, 17, 17, 17)),
        detail(seg(12, 12, 19, 12)),
    ]


# ============================================================================ web tools and layout

@icon("bookmarklet", CAT, "Bookmark ribbon with code angle brackets on it",
      tags=["javascript bookmark", "favelet", "browser snippet", "bookmark script", "saved script", "one click tool"])
def _(S):
    rib = [(4, 2), (20, 2), (20, 21), (12, 16), (4, 21)]
    return [
        shell(poly(rib, closed=True, r=S.r)),
        detail(poly([(10.5, 6.5), (8, 9.5), (10.5, 12.5)], r=0)),
        detail(poly([(13.5, 6.5), (16, 9.5), (13.5, 12.5)], r=0)),
    ]


@icon("email-list-cleaning", CAT, "Broom sweeping away from a short list of lines toward an envelope",
      tags=["list hygiene", "remove invalid emails", "bounced addresses", "subscriber cleanup", "clean mailing list", "unsubscribe cleanup"])
def _(S):
    return [
        line(seg(2, 4, 12, 4)), line(seg(2, 8.5, 12, 8.5)),
        shell(rect(15, 2, 7, 6.5, min(S.R, 2))),
        detail(poly([(15.5, 3), (18.5, 5.8), (21.5, 3)], r=0)),
        line(seg(2, 18, 10, 18)),
        shell(poly([(10, 14), (22, 12.5), (22, 22), (10, 21)], closed=True, r=S.r)),
        detail(seg(14.5, 14, 14.5, 21.5)), detail(seg(18.5, 13.5, 18.5, 21.8)),
    ]


@icon("conditional-form-logic", CAT, "Form field bar splitting into two branching arrows leading to two different bars",
      tags=["branching form", "if then form", "skip logic", "show hide fields", "form rules", "dynamic form", "survey logic"])
def _(S):
    return [
        shell(rect(7, 2, 10, 5, min(S.R, 2))),
        line(seg(12, 7, 12, 10.5)),
        line(poly([(6, 14.5), (6, 10.5), (18, 10.5), (18, 14.5)], r=S.r * 0.6)),
        head(S, (6, 15.5), 90, 2.4), head(S, (18, 15.5), 90, 2.4),
        shell(rect(2, 18, 8, 4, min(S.R, 2))),
        shell(rect(14, 18, 8, 4, min(S.R, 2))),
    ]


@icon("content-repurposing", CAT, "One document at the top with two arrows leading down to a video card and an image card",
      tags=["reuse content", "repackage", "content recycling", "multi format", "convert article to video", "atomize content"])
def _(S):
    return [
        shell(rect(7, 2, 10, 7.5, min(S.R, 2))),
        detail(seg(9.5, 5.7, 14.5, 5.7)),
        *arrow(S, 9, 11, 6.2, 13.3, 2.2), *arrow(S, 15, 11, 17.8, 13.3, 2.2),
        shell(rect(2, 15, 8, 7, min(S.R, 2))),
        Part("dot", poly([(4.8, 17.3), (7.8, 18.5), (4.8, 19.7)], closed=True, r=0)),
        shell(rect(14, 15, 8, 7, min(S.R, 2))),
        detail(poly([(14, 20.5), (17, 17.8), (22, 21)], r=0)),
    ]


@icon("mailto-link", CAT, "Two chain links on a diagonal with a small envelope at the lower right",
      tags=["email link", "mailto", "href mailto", "contact link", "email hyperlink", "click to email"])
def _(S):
    return [
        line(poly(rrect_pts(8.5, 8.5, 9, 5, -45), closed=True, r=L(S, 0.4, 2.4))),
        line(poly(rrect_pts(14, 14, 9, 5, -45), closed=True, r=L(S, 0.4, 2.4))),
        shell(rect(14, 16, 8, 6, min(S.R, 1.5))),
        detail(poly([(14.5, 16.8), (18, 19.8), (21.5, 16.8)], r=0)),
    ]


@icon("keyboard-warrior", CAT, "Keyboard with a small sword crossed over it",
      tags=["troll", "online fighter", "internet argument", "flame war", "armchair critic", "comment section fighter"])
def _(S):
    blade = poly([(12, 1.5), (13.7, 3.5), (13.7, 8), (10.3, 8), (10.3, 3.5)], closed=True, r=0)
    return [
        shell(rect(2, 13, 20, 8.5, min(S.R, 3))),
        dot(6, 16, 0.8), dot(10, 16, 0.8), dot(14, 16, 0.8), dot(18, 16, 0.8),
        detail(seg(7, 19, 17, 19)),
        shell(blade),
        line(seg(8, 9.5, 16, 9.5)),
        line(seg(12, 9.5, 12, 12)),
    ]


@icon("hotlinking", CAT, "Two browser windows linked by a chain link standing between them",
      tags=["inline linking", "bandwidth theft", "remote image", "linked image", "direct link", "leeching"])
def _(S):
    return [
        shell(rect(2, 2, 12, 9, L(S, 0, 2))), detail(seg(2, 5.5, 14, 5.5)),
        shell(rect(10, 14, 12, 8, L(S, 0, 2))), detail(seg(10, 17.5, 22, 17.5)),
        line(rect(16.5, 3.5, 4.5, 8.5, L(S, 2, 2.25))),
    ]


@icon("responsive-table", CAT, "Wide table grid on the left with an arrow to narrow stacked cards on the right",
      tags=["mobile table", "table layout", "stacked rows", "adaptive table", "responsive design", "data table mobile"])
def _(S):
    return [
        shell(rect(2, 4, 9, 16, min(S.R, 2))),
        detail(seg(6.5, 4, 6.5, 20)), detail(seg(2, 9.3, 11, 9.3)), detail(seg(2, 14.7, 11, 14.7)),
        *arrow(S, 12, 12, 14.5, 12, 2.0),
        shell(rect(16, 3, 6, 8, min(S.R, 2))), detail(seg(16, 7, 22, 7)),
        shell(rect(16, 13, 6, 8, min(S.R, 2))), detail(seg(16, 17, 22, 17)),
    ]


@icon("online-queue", CAT, "Browser window with small people lined up above a partly filled progress line",
      tags=["waiting room", "virtual queue", "line up", "please wait", "traffic control", "ticket queue", "wait list"])
def _(S):
    out = [*win(S, 2, 2, 20, 20, 5.5)]
    for x in (7, 12, 17):
        out += [dot(x, 10.3, 1.4), line(f"M{fmt(x - 2.2)} 14.6A2.2 2.2 0 0 1 {fmt(x + 2.2)} 14.6")]
    out += [detail(seg(5, 18, 12, 18)), dot(15, 18, 0.9), dot(18, 18, 0.9)]
    return out


@icon("bot-check-page", CAT, "Browser window with a shield in the middle and three loading dots below",
      tags=["human verification", "checking your browser", "security check", "anti bot", "challenge page", "ddos protection page"])
def _(S):
    sh = L(S, "M12 8L16.5 9.5V12.5Q16.5 14.8 12 16Q7.5 14.8 7.5 12.5V9.5Z", "M12 8L16.5 9.5V12.5Q16.5 14.8 12 16Q7.5 14.8 7.5 12.5V9.5Z")
    return [
        *win(S, 2, 2, 20, 20, 5),
        detail(sh),
        dot(9, 18.8, 0.9), dot(12, 18.8, 0.9), dot(15, 18.8, 0.9),
    ]


@icon("crowdsourcing", CAT, "Three small people each sending an arrow up into one large lightbulb",
      tags=["crowd ideas", "collective input", "community ideas", "crowd wisdom", "idea collection", "open innovation"])
def _(S):
    out = [
        shell(circle(12, 6.5, 4.5)),
        line(seg(10, 13.3, 14, 13.3)),
    ]
    for x in (6, 12, 18):
        out += [dot(x, 21, 1.2), *arrow(S, x, 18.2, x, 15.5, 2.0)]
    return out
