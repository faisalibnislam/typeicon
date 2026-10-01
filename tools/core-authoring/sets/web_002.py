"""TypeIcon Core: web (batch 002): community and conversion, domains and hosting, email, tracking and search/SEO."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import ST as _ST, circle_d, fmt, path_to_d, polar

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


def cyc(S, cx, cy, r, a0, a1, role=line, size=2.8):
    tip = polar(cx, cy, r, a1)
    return [role(arc(cx, cy, r, a0, a1)), head(S, tip, a1 + 90, size, role)]


def cursor(S, x, y, k=1.0):
    pts = [(0, 0), (0, 8), (2, 6.25), (3.4, 9.2), (5.1, 8.4), (3.75, 5.5), (6.25, 5.5)]
    return Part("dot", poly([(x + px * k, y + py * k) for px, py in pts], closed=True, r=L(S, 0, 0.5)))


def rot(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rrect_pts(cx, cy, w, h, deg):
    return rot([(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)], deg, cx, cy)


def gauge_arc(cx, cy, r, role=detail):
    return role(f"M{fmt(cx - r)} {fmt(cy)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx + r)} {fmt(cy)}")


def pagebox(S, x, y, w, h):
    return shell(rect(x, y, w, h, min(S.R, 3)))


def globe(S, cx, cy, r, mer=True, eq=True):
    out = [shell(circle(cx, cy, r))]
    if mer:
        out.append(detail(ellipse(cx, cy, r * 0.45, r)))
    if eq:
        out.append(detail(seg(cx - r, cy, cx + r, cy)))
    return out


def env(S, x, y, w, h, flap=0.55):
    """Envelope: outline plus flap V."""
    return [shell(rect(x, y, w, h, min(S.R, 2.5))),
            detail(poly([(x + 1.1, y + 1.1), (x + w / 2, y + h * flap), (x + w - 1.1, y + 1.1)], r=S.r))]


def envdots(S, x, y, w, h, flap=0.5):
    """Envelope as small detail-weight outline (for use inside other shells)."""
    return [detail(rect(x, y, w, h, 1)), detail(poly([(x + 0.8, y + 0.8), (x + w / 2, y + h * flap), (x + w - 0.8, y + 0.8)]))]


def person(S, cx, cy, k=1.0, role=line):
    """Head dot with shoulder arc; cy is head centre."""
    return [dot(cx, cy, 1.9 * k),
            role(f"M{fmt(cx - 3.6 * k)} {fmt(cy + 8 * k)}V{fmt(cy + 6.5 * k)}A{fmt(3.6 * k)} {fmt(3.6 * k)} 0 0 1 {fmt(cx + 3.6 * k)} {fmt(cy + 6.5 * k)}V{fmt(cy + 8 * k)}")]


def tagshape(S, x, y, w, h, tip=3.5):
    """Horizontal tag: flat left edge, pointed right end."""
    return poly([(x, y), (x + w - tip, y), (x + w, y + h / 2), (x + w - tip, y + h), (x, y + h)], closed=True, r=S.r)


def flame(S, cx, top, w, h):
    """Solid flame silhouette."""
    x0, x1 = cx - w / 2, cx + w / 2
    b = top + h
    if S.name == "line":
        return solid(f"M{fmt(cx)} {fmt(top)}L{fmt(x1)} {fmt(top + h * 0.6)}L{fmt(cx + w * 0.3)} {fmt(b)}H{fmt(cx - w * 0.3)}L{fmt(x0)} {fmt(top + h * 0.6)}L{fmt(cx - w * 0.15)} {fmt(top + h * 0.45)}Z")
    return solid(f"M{fmt(cx)} {fmt(top)}C{fmt(cx + w * 0.2)} {fmt(top + h * 0.3)} {fmt(x1)} {fmt(top + h * 0.45)} {fmt(x1)} {fmt(top + h * 0.7)}"
                 f"A{fmt(w / 2)} {fmt(h * 0.3)} 0 0 1 {fmt(x0)} {fmt(top + h * 0.7)}C{fmt(x0)} {fmt(top + h * 0.5)} {fmt(cx - w * 0.2)} {fmt(top + h * 0.35)} {fmt(cx)} {fmt(top)}Z")


def magnifier(S, cx, cy, r, hl=5.5):
    a = math.radians(45)
    hx = cx + (r + hl) * math.cos(a)
    hy = cy + (r + hl) * math.sin(a)
    sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
    return [shell(circle(cx, cy, r)), line(seg(sx, sy, hx, hy))]


def key(S, cx, cy, r=3.2, length=10):
    """Horizontal key with bow on the left."""
    x0 = cx + r
    return [shell(circle(cx, cy, r)), line(seg(x0, cy, x0 + length, cy)),
            line(seg(x0 + length - 2, cy, x0 + length - 2, cy + 3)), line(seg(x0 + length - 5, cy, x0 + length - 5, cy + 2.5))]


def stars(S, cx, cy, n=5, step=3.6, r=1.7):
    out = []
    x0 = cx - (n - 1) * step / 2
    for i in range(n):
        pts = []
        for j in range(10):
            rr = r if j % 2 == 0 else r * 0.45
            pts.append(polar(x0 + i * step, cy, rr, -90 + j * 36))
        out.append(Part("solid", poly(pts, closed=True)))
    return out


def thin(d, w=1.0):
    """Thin solid stroke (a fine line the 2 px stroke could not draw) as a solid-region part."""
    return Part("dot", path_to_d(_ST(d, w, "butt", "round")))


def lines(x, y, widths, gap=3.0, role=detail):
    return [role(seg(x, y + i * gap, x + w, y + i * gap)) for i, w in enumerate(widths)]


# ============================================================================ community and conversion

@icon("orphan-page", CAT, "Small sitemap tree of connected boxes with one page box floating alone to the side",
      tags=["orphan page", "unlinked page", "no internal links", "sitemap", "isolated page", "seo", "site structure"])
def _(S):
    b = L(S, 0, 1.8)
    return [
        shell(rect(2, 2, 6, 4, b)), shell(rect(7, 10, 6, 4, b)), shell(rect(7, 18, 6, 4, b)),
        line(seg(4, 6, 4, 20)), line(seg(4, 12, 7, 12)), line(seg(4, 20, 7, 20)),
        shell(rect(17, 8, 5, 8, min(S.R, 2.5))),
    ]


@icon("vote-arrows", CAT, "Up chevron above a number one and a down chevron below it in a narrow column",
      tags=["upvote", "downvote", "voting", "karma", "rating", "like dislike", "score", "forum"])
def _(S):
    return [
        line(poly([(7, 7.5), (12, 3), (17, 7.5)], r=S.r)),
        line(poly([(10.2, 12), (12.5, 10), (12.5, 15.5)], r=S.r * 0.5)),
        line(poly([(7, 16.5), (12, 21), (17, 16.5)], r=S.r)),
    ]


@icon("subscribe-button", CAT, "Rounded button with a bell on its left and a short text line",
      tags=["subscribe", "follow", "notify me", "bell", "channel", "call to action", "notifications"])
def _(S):
    bell = f"M6.2 14.6L7.6 13V10.6A2.2 2.2 0 0 1 12 10.6V13L13.4 14.6Z"
    return [
        shell(rect(2, 5.5, 20, 13, L(S, 2, 6.5))),
        Part("dot", bell), dot(9.8, 15.8, 0.9),
        detail(seg(15.8, 12, 19, 12)),
    ]


@icon("ban-hammer", CAT, "Large hammer striking down on a round user avatar",
      tags=["ban", "banhammer", "moderation", "block user", "admin", "punish", "suspend account"])
def _(S):
    head_ = poly(rrect_pts(15, 9, 8, 4, 45), closed=True, r=S.r * 0.5)
    return [
        shell(circle(7.5, 16.5, 5.5)),
        dot(7.5, 14.4, 1.6), Part("dot", "M4.8 20.2A2.7 2.7 0 0 1 10.2 20.2Z"),
        shell(head_),
        line(seg(16.4, 7.6, 21, 3)),
    ]


@icon("flame-war", CAT, "Two facing speech bubbles with a flame rising between them",
      tags=["flame war", "argument", "heated debate", "comments fight", "toxic", "conflict", "trolling"])
def _(S):
    left = [(2, 12.5), (10.5, 12.5), (10.5, 19), (7, 19), (4.2, 21.5), (4.2, 19), (2, 19)]
    right = [(22 - x, y) for x, y in left]
    return [shell(poly(left, closed=True, r=S.r)), shell(poly(right, closed=True, r=S.r)),
            flame(S, 12, 1.8, 7.6, 8.2)]


@icon("lurker", CAT, "Pair of eyes peeking over the top edge of a browser window",
      tags=["lurking", "silent user", "watcher", "peeking", "passive reader", "spectator", "forum"])
def _(S):
    return win(S, 2, 12, 20, 9, 4.5) + [
        shell(ellipse(7.5, 6.8, 3.3, 3.0)), shell(ellipse(16.5, 6.8, 3.3, 3.0)),
        dot(8.3, 7, 1.0), dot(15.7, 7, 1.0),
    ]


@icon("user-generated-content", CAT, "Content block with three small people each sending an arrow up into it",
      tags=["ugc", "user content", "community posts", "reviews", "crowd sourced", "contributions", "submissions"])
def _(S):
    out = [shell(rect(3, 2.5, 18, 5.5, min(S.R, 2))), detail(seg(7, 5.25, 14, 5.25))]
    for x in (6, 12, 18):
        out += [line(seg(x, 13.6, x, 10.6)), head(S, (x, 10.4), -90, 2.0), dot(x, 16.3, 1.5),
                Part("dot", f"M{fmt(x - 2.3)} 21.6A2.3 2.3 0 0 1 {fmt(x + 2.3)} 21.6Z")]
    return out


@icon("social-proof-notification", CAT, "Small toast card with a round avatar and two text lines over page lines",
      tags=["social proof", "toast", "recent purchase", "popup notification", "fomo", "conversion", "live activity"])
def _(S):
    return [
        line(seg(3, 3.2, 21, 3.2)), line(seg(3, 6.6, 14, 6.6)),
        shell(rect(2, 11, 20, 10, min(S.R, 3))),
        dot(7, 16, 2.0), detail(seg(11.5, 14.3, 18, 14.3)), detail(seg(11.5, 18.1, 16, 18.1)),
    ]


@icon("exit-intent-popup", CAT, "Cursor leaving the top of a browser window while a modal pops up in the middle",
      tags=["exit intent", "leaving page", "popup", "modal", "retention", "last chance offer", "conversion"])
def _(S):
    return [
        shell(rect(2, 9.5, 20, 12, min(S.R, 3))),
        shell(rect(7, 13, 10, 6, 1.5)),
        cursor(S, 15.5, 1.5, 0.75),
        line(seg(10.5, 7, 10.5, 3.2)), head(S, (10.5, 2.8), -90, 2.2),
    ]


@icon("newsletter-popup", CAT, "Modal box with an envelope on top, an input line and a button",
      tags=["newsletter", "signup modal", "email capture", "subscribe popup", "lead capture", "overlay", "mailing list"])
def _(S):
    return [
        shell(rect(2, 2, 20, 20, min(S.R, 3))),
        detail(rect(6.5, 5, 11, 6, 1)), detail(poly([(6.5, 5), (12, 8.6), (17.5, 5)])),
        detail(seg(6.5, 15, 17.5, 15)),
        Part("dot", rect(7, 17.6, 10, 2.2, 0.6)),
    ]


@icon("form-abandonment", CAT, "Half filled form with a small figure walking away from it",
      tags=["abandoned form", "drop off", "incomplete form", "checkout exit", "bounce", "conversion loss", "funnel"])
def _(S):
    return [
        shell(rect(2, 3, 12, 18, min(S.R, 3))),
        detail(seg(5.5, 8, 10.5, 8)), detail(seg(5.5, 12, 10.5, 12)), detail(seg(5.5, 16, 8, 16)),
        dot(19, 8, 1.7),
        line(poly([(19, 11), (19, 15.5)])),
        line(poly([(16.5, 13), (19, 11.5), (21.5, 13.5)], r=S.r * 0.5)),
        line(poly([(16.5, 20.5), (19, 15.5), (21.5, 20.5)], r=S.r * 0.5)),
    ]


@icon("cart-drawer", CAT, "Browser window with a side panel sliding in from the right showing a cart and an item line",
      tags=["mini cart", "slide out cart", "side cart", "basket drawer", "ecommerce", "checkout panel", "shopping"])
def _(S):
    return win(S, 2, 3, 20, 18, 4.5) + [
        detail(seg(9.5, 7.5, 9.5, 21)),
        detail(poly([(12, 10.5), (13.5, 10.5), (14.8, 15), (19.5, 15)], r=0)),
        detail(poly([(14, 12), (20.5, 12), (19.5, 15)], r=0)),
        detail(seg(12.5, 18.5, 19.5, 18.5)),
    ]


@icon("promo-code-field", CAT, "Input field with a small coupon ticket on its left and an apply tick on its right",
      tags=["coupon code", "discount code", "voucher", "promo", "apply code", "checkout field", "ecommerce"])
def _(S):
    tick = "M4 9.5H12V11.1A1.1 1.1 0 0 0 12 13.3V14.5H4V13.3A1.1 1.1 0 0 0 4 11.1Z"
    return [
        shell(rect(2, 6.5, 20, 11, min(S.R, 3))),
        Part("dot", tick),
        detail(seg(15, 6.5, 15, 17.5)),
        line(poly([(17, 12.2), (18.3, 13.6), (20.4, 10.8)], r=S.r * 0.4)),
    ]


@icon("abandoned-cart", CAT, "Shopping cart standing alone with a small cobweb in the corner above it",
      tags=["abandoned basket", "cart recovery", "left behind", "ecommerce", "checkout drop off", "unpurchased", "retargeting"])
def _(S):
    return [
        line(poly([(2, 9), (5, 9), (7.5, 17)], r=S.r * 0.5)),
        shell(poly([(6, 11.5), (20, 11.5), (18.4, 17), (7.6, 17)], closed=True, r=S.r * 0.6)),
        dot(9.5, 20.6, 1.4), dot(16.5, 20.6, 1.4),
        line(seg(22, 2, 14.5, 2)), line(seg(22, 2, 22, 9)), line(seg(22, 2, 16.7, 7.3)),
        line("M14.5 2Q16.5 7.5 22 9"),
    ]


@icon("custom-domain", CAT, "Address bar joined to a globe below it by a link line",
      tags=["own domain", "branded url", "domain mapping", "connect domain", "website address", "vanity url", "dns"])
def _(S):
    return [
        shell(rect(2, 2, 20, 4.5, 2.25)), detail(seg(6, 4.25, 13, 4.25)),
        line(seg(12, 6.5, 12, 10.5)),
        *globe(S, 12, 16, 5.5),
    ]


@icon("dns-propagation", CAT, "Globe with ripple arcs spreading out from one point on its surface",
      tags=["dns", "propagation", "domain update", "nameserver change", "ripple", "spreading", "ttl"])
def _(S):
    cx, cy, r = 9.5, 14.5, 7.5
    px, py = polar(cx, cy, r, -45)
    return [
        shell(circle(cx, cy, r)), detail(ellipse(cx, cy, 3.2, r)), detail(seg(cx - r, cy, cx + r, cy)),
        line(arc(px, py, 4.2, -85, -5)), line(arc(px, py, 7.2, -85, -5)),
    ]


# ============================================================================ domains and hosting

@icon("dns-record", CAT, "Small globe above a three row table with a label column and a value column",
      tags=["dns", "a record", "cname", "mx record", "nameserver", "zone file", "domain settings"])
def _(S):
    return [
        shell(circle(12, 4.8, 3.0)),
        shell(rect(2, 11, 20, 11, min(S.R, 2.5))),
        detail(seg(2, 14.7, 22, 14.7)), detail(seg(2, 18.3, 22, 18.3)), detail(seg(8.5, 11, 8.5, 22)),
    ]


@icon("subdomain", CAT, "Large globe with a branch line leading down to two smaller globes",
      tags=["sub domain", "blog.example.com", "domain branch", "dns", "child domain", "host name", "prefix"])
def _(S):
    return [
        *globe(S, 12, 6.5, 4.5),
        line(seg(12, 11, 12, 14)), line(seg(6, 14, 18, 14)), line(seg(6, 14, 6, 16)), line(seg(18, 14, 18, 16)),
        shell(circle(6, 19.2, 3.2)), shell(circle(18, 19.2, 3.2)),
    ]


@icon("top-level-domain", CAT, "Tag shape with a bold dot followed by three short letters",
      tags=["tld", ".com", "domain extension", "suffix", "dot com", "domain name", "registry"])
def _(S):
    return [
        shell(tagshape(S, 2, 5, 20, 14, 4)),
        dot(6.2, 14, 1.3),
        detail(seg(9.2, 12, 10.8, 12)), detail(seg(12.8, 12, 14.4, 12)), detail(seg(16.4, 12, 18, 12)),
    ]


@icon("whois-record", CAT, "Globe peeking above an ID card showing a head silhouette and lines",
      tags=["whois", "domain owner", "registrant", "domain lookup", "registration details", "identity card", "ownership"])
def _(S):
    return [
        line(arc(12, 8.5, 6.5, 171, 369)),
        line(f"M9 8.5A3 6.5 0 0 1 15 8.5"), line(seg(5.5, 8.5, 18.5, 8.5)),
        shell(rect(2, 11.5, 20, 10, min(S.R, 2.5))),
        dot(7.5, 15.3, 1.6), Part("dot", "M4.9 20.5A2.6 2.6 0 0 1 10.1 20.5Z"),
        detail(seg(13, 15.2, 19, 15.2)), detail(seg(13, 18.8, 17, 18.8)),
    ]


@icon("domain-for-sale", CAT, "Globe with a price tag hanging beside it",
      tags=["sell domain", "domain marketplace", "buy domain", "premium domain", "price tag", "listing", "domain auction"])
def _(S):
    return [
        *globe(S, 7.5, 14.5, 5.5),
        shell(poly(rot([(14, 5.5), (20, 5.5), (20, 13.5), (17, 17), (14, 13.5)], 28, 17, 11), closed=True, r=S.r)),
        dot(*rot([(17, 8.5)], 28, 17, 11)[0], 1.1),
    ]


@icon("parked-domain", CAT, "Globe with a square parking sign letter P standing beside it",
      tags=["parked", "parking page", "unused domain", "reserved domain", "placeholder", "holding page", "dormant"])
def _(S):
    return [
        *globe(S, 7.5, 15, 5.5),
        shell(rect(13, 2, 9, 9.5, min(S.R, 2))),
        detail("M16.4 9V5.2H18.4A1.5 1.5 0 0 1 18.4 8.2H16.4"),
        line(seg(17.5, 11.5, 17.5, 21)),
    ]


@icon("domain-transfer", CAT, "Two globes side by side with an arrow carrying a small tag from the left one to the right one",
      tags=["transfer domain", "move registrar", "auth code", "epp code", "switch registrar", "domain migration", "dns"])
def _(S):
    return [
        shell(circle(6.5, 17.5, 4.5)), dot(6.5, 17.5, 1.2), shell(circle(17.5, 17.5, 4.5)), dot(17.5, 17.5, 1.2),
        shell(tagshape(S, 8.5, 1.5, 7, 4.5, 2)),
        *arrow(S, 5, 9, 19, 9, 3.0),
    ]


@icon("localhost", CAT, "Laptop with a curved arrow looping around inside its screen",
      tags=["local host", "127.0.0.1", "dev server", "local development", "loopback", "this computer", "self hosted"])
def _(S):
    return [
        shell(rect(4, 3, 16, 12, min(S.R, 2))),
        shell(poly([(2, 18), (22, 18), (20.5, 21), (3.5, 21)], closed=True, r=S.r * 0.5)),
        *cyc(S, 12, 9, 3.2, -60, 250, role=detail, size=2.6),
    ]


@icon("shared-hosting", CAT, "One server box with three small houses sitting on top of it",
      tags=["shared server", "web hosting", "hosting plan", "multiple sites", "budget hosting", "cpanel", "server"])
def _(S):
    out = [shell(rect(2, 13, 20, 8, min(S.R, 2.5))), dot(6, 17, 1.1), detail(seg(10, 17, 18, 17))]
    for x in (2.5, 9.5, 16.5):
        out.append(solid(poly([(x, 10), (x, 7.4), (x + 2.25, 4.8), (x + 4.5, 7.4), (x + 4.5, 10)], closed=True)))
    return out


@icon("virtual-private-server", CAT, "Server box split into three compartments by dashed walls with the middle one highlighted",
      tags=["vps", "virtual server", "cloud server", "isolated hosting", "vm", "dedicated resources", "partition"])
def _(S):
    d = "M4.5 {y}H7M10.75 {y}H13.25M17 {y}H19.5"
    return [
        shell(rect(2, 2.5, 20, 19, min(S.R, 3))),
        detail(d.format(y=8.5)), detail(d.format(y=15.5)),
        Part("dot", rect(5, 10.9, 14, 2.6, 0.6)),
    ]


@icon("hosting-control-panel", CAT, "Browser window filled with a grid of six small tiles",
      tags=["cpanel", "hosting dashboard", "plesk", "site manager", "admin panel", "server settings", "web hosting"])
def _(S):
    out = win(S, 2, 3, 20, 18, 4.5)
    for r in range(2):
        for c in range(3):
            out.append(Part("dot", rect(4.6 + c * 5.6, 10.4 + r * 5.4, 3.6, 3.4, L(S, 0, 0.8))))
    return out


@icon("ftp-transfer", CAT, "Folder and server side by side with two opposite arrows between them",
      tags=["ftp", "sftp", "file upload", "file transfer", "upload download", "sync files", "remote server"])
def _(S):
    return [
        shell(poly([(2, 8), (5, 8), (6.3, 9.6), (9, 9.6), (9, 19), (2, 19)], closed=True, r=S.r * 0.6)),
        shell(rect(15, 5, 7, 15, min(S.R, 2))),
        detail(seg(15, 10, 22, 10)), dot(18.5, 15.5, 1.0),
        *arrow(S, 10.5, 10.5, 14, 10.5, 2.4), *arrow(S, 14, 15, 10.5, 15, 2.4),
    ]


@icon("http-header", CAT, "Message page whose top band holds three short key and value line pairs",
      tags=["header", "headers", "request header", "response header", "http", "metadata", "content type"])
def _(S):
    out = [shell(rect(2, 2, 20, 20, min(S.R, 3))), detail(seg(2, 18, 22, 18))]
    for y in (6, 10, 14):
        out += [detail(seg(5, y, 8, y)), detail(seg(10.5, y, 19, y))]
    return out


@icon("url-encoding", CAT, "Address bar with percent signs placed between short text segments",
      tags=["percent encoding", "urlencode", "escape characters", "%20", "query string", "uri", "special characters"])
def _(S):
    def pct(x):
        return [dot(x - 1.9, 9.9, 1.1), dot(x + 1.9, 14.1, 1.1), detail(seg(x + 2.2, 9.2, x - 2.2, 14.8))]
    return [
        shell(rect(1.5, 6, 21, 12, 6 if S.name == "rounded" else 2)),
        *pct(7), *pct(17), detail(seg(10.8, 12, 13.2, 12)),
    ]


@icon("preview-deployment", CAT, "Browser window with an eye in the page and a small branch mark beside it",
      tags=["preview", "staging", "deploy preview", "branch deploy", "pull request preview", "vercel", "review app"])
def _(S):
    eye = f"M3.8 14.5Q8.5 9.5 13.2 14.5Q8.5 19.5 3.8 14.5Z"
    return win(S, 2, 3, 20, 18, 4.5) + [
        detail(eye), dot(8.5, 14.5, 1.3),
        dot(17.5, 10.5, 1.2), dot(17.5, 18.5, 1.2), line(seg(17.5, 10.5, 17.5, 18.5)),
    ]


@icon("webmail", CAT, "Browser window with an envelope in the middle of the page",
      tags=["web mail", "online email", "inbox in browser", "email client", "mail in browser", "message", "hosted mail"])
def _(S):
    return win(S, 2, 3, 20, 18, 4.5) + envdots(S, 6.5, 10.5, 11, 7, 0.55)


# ============================================================================ email

def pct(x, y, role=detail, k=1.0):
    return [dot(x - 1.9 * k, y - 2.1 * k, 1.1 * k), dot(x + 1.9 * k, y + 2.1 * k, 1.1 * k),
            role(seg(x + 2.2 * k, y - 2.9 * k, x - 2.2 * k, y + 2.9 * k))]


@icon("mail-server", CAT, "Two stacked server units with an envelope in front of the lower corner",
      tags=["smtp server", "email server", "mail host", "imap", "postfix", "exchange", "server rack"])
def _(S):
    r = min(S.R, 1.5)
    return [
        shell(rect(2, 1.8, 14, 4.6, r)), shell(rect(2, 8.4, 14, 4.6, r)),
        dot(5, 4.1, 0.8), dot(5, 10.7, 0.8),
        *env(S, 8, 17, 14, 5, 0.6),
    ]


@icon("email-template", CAT, "Envelope beside a page showing a header block, an image block and two text lines",
      tags=["newsletter layout", "email design", "html template", "email builder", "campaign template", "layout", "mailer"])
def _(S):
    return [
        *env(S, 2, 8, 7.5, 7.5, 0.5),
        shell(rect(13, 2, 9, 20, min(S.R, 2.5))),
        Part("dot", rect(15.5, 5, 4, 1.8, 0.4)), Part("dot", rect(15.5, 8.8, 4, 3.4, 0.4)),
        detail(seg(15.5, 15.6, 19.5, 15.6)), detail(seg(15.5, 19, 18, 19)),
    ]


@icon("drip-campaign", CAT, "Faucet dripping a line of small envelopes downward",
      tags=["drip", "automated sequence", "email automation", "nurture", "timed emails", "faucet", "email flow"])
def _(S):
    return [
        line(poly([(2, 4.5), (14.5, 4.5), (14.5, 7.5)])),
        line(seg(6, 4.5, 6, 1.8)), line(seg(3.8, 1.8, 8.2, 1.8)),
        *env(S, 10.5, 10, 8, 6, 0.55),
        Part("dot", rect(12.5, 19, 4, 3, 0.5)),
    ]


@icon("email-autoresponder", CAT, "Envelope with a small robot head above its flap",
      tags=["auto reply", "out of office", "automatic response", "bot email", "autoreply", "vacation responder", "automation"])
def _(S):
    return [
        *env(S, 2, 11.5, 20, 10.5, 0.55),
        shell(rect(7, 3.5, 10, 5.5, min(S.R, 2))),
        dot(10, 6.25, 0.9), dot(14, 6.25, 0.9),
        line(seg(12, 3.5, 12, 2)),
    ]


@icon("unsubscribe-link", CAT, "Envelope with an exit door bracket and outward arrow at its lower right",
      tags=["unsubscribe", "opt out", "leave list", "stop emails", "remove subscription", "exit", "footer link"])
def _(S):
    return [
        *env(S, 2, 2, 16, 11, 0.55),
        line(poly([(17.5, 16.5), (14.5, 16.5), (14.5, 21.5), (17.5, 21.5)])),
        *arrow(S, 16.5, 19, 21.8, 19, 2.6),
    ]


@icon("double-opt-in", CAT, "Envelope with two stacked check marks beside it",
      tags=["confirm subscription", "opt in", "confirmation email", "consent", "verify email", "gdpr", "two step signup"])
def _(S):
    return [
        *env(S, 2, 6, 13, 12, 0.55),
        line(poly([(17.5, 6.5), (19.3, 8.3), (22, 4.8)], r=S.r * 0.4)),
        line(poly([(17.5, 15), (19.3, 16.8), (22, 13.3)], r=S.r * 0.4)),
    ]


@icon("lead-magnet", CAT, "Horseshoe magnet pulling a small open ebook up toward its poles",
      tags=["freebie", "opt in offer", "ebook download", "gated content", "lead generation", "magnet", "attract"])
def _(S):
    mag = "M5 11.5V8.5A7 7 0 0 1 19 8.5V11.5H15.5V8.5A3.5 3.5 0 0 0 8.5 8.5V11.5Z"
    book = L(S, "M5 22V16.5L12 15.5L19 16.5V22L12 21L5 22Z", "M5 22V16.5C8 15 10.5 15.5 12 16.5C13.5 15.5 16 15 19 16.5V22C16 20.8 13.5 21 12 22C10.5 21 8 20.8 5 22Z")
    return [shell(mag), shell(book), detail(seg(12, 16, 12, 21.5))]


@icon("email-subscriber", CAT, "Person bust holding an envelope in front of the chest",
      tags=["subscriber", "newsletter reader", "mailing list member", "contact", "recipient", "audience", "email contact"])
def _(S):
    return [
        dot(12, 5.2, 3.2),
        shell(L(S, "M3 21V17.5L7 12.8H17L21 17.5V21Z", "M3 21V18A9 6 0 0 1 21 18V21Z")),
        detail(rect(7.5, 15, 9, 5, 0.5)), detail(poly([(7.5, 15), (12, 18), (16.5, 15)])),
    ]


@icon("spam-filter", CAT, "Funnel with several small envelopes entering the top and a mesh line inside",
      tags=["spam", "junk filter", "inbox filter", "email filtering", "anti spam", "block junk", "funnel"])
def _(S):
    out = [shell(poly([(3, 9), (21, 9), (14, 15.5), (14, 21.5), (10, 21.5), (10, 15.5)], closed=True, r=S.r)),
           detail(seg(7.5, 12, 16.5, 12))]
    for x in (3.5, 10, 16.5):
        out.append(Part("dot", rect(x, 2.5, 4, 3, 0.5)))
    return out


@icon("email-deliverability", CAT, "Envelope flying along a curved path into an inbox tray",
      tags=["inbox placement", "delivery rate", "reach inbox", "sender reputation", "email delivery", "arrives", "mail flow"])
def _(S):
    return [
        shell(poly([(2, 14.5), (8, 14.5), (9.5, 17), (14.5, 17), (16, 14.5), (22, 14.5), (22, 21.5), (2, 21.5)], closed=True, r=S.r)),
        *env(S, 10, 3.5, 10, 7, 0.55),
        line("M2 10C3 5 6 4.5 8 5"),
    ]


@icon("bounced-email", CAT, "Envelope hitting a wall and bouncing back along a curved return arrow",
      tags=["bounce", "undeliverable", "hard bounce", "soft bounce", "returned mail", "failed delivery", "invalid address"])
def _(S):
    return [
        line(seg(21.5, 3, 21.5, 21)),
        *env(S, 3, 13, 12, 8, 0.55),
        line("M18 12.5C18 4 10 3 5.5 6.5"),
        head(S, (5.5, 6.5), 135, 2.8),
    ]


@icon("transactional-email", CAT, "Envelope with a receipt slip with a torn top edge sticking out of it",
      tags=["receipt email", "order confirmation", "invoice email", "password reset", "automated message", "billing email", "notification"])
def _(S):
    zig = "M7 11V4.2L8.6 2.8L10.2 4.2L11.8 2.8L13.4 4.2L15 2.8L16.6 4.2V11"
    return [
        shell(zig + "Z") if False else line(zig),
        *env(S, 2, 10.5, 20, 11.5, 0.5),
        detail(seg(9.5, 7.5, 14, 7.5)),
    ]


@icon("welcome-email", CAT, "Open envelope with a waving hand rising out of it",
      tags=["welcome", "onboarding email", "greeting", "hello", "new member", "first email", "wave"])
def _(S):
    return [
        shell(rect(2, 12, 20, 9.5, min(S.R, 2.5))),
        detail(poly([(2, 12), (12, 17.5), (22, 12)], r=S.r)),
        solid(rect(9, 7.5, 6, 4, 1)), solid(rect(9.2, 3.8, 1.5, 4.5, 0.7)),
        solid(rect(11.3, 2.6, 1.5, 5.5, 0.7)), solid(rect(13.4, 3.8, 1.5, 4.5, 0.7)),
    ]


@icon("email-warmup", CAT, "Envelope beside a thermometer with a small flame in its bulb",
      tags=["warm up", "sender warming", "ip warming", "reputation", "deliverability", "gradual sending", "heat"])
def _(S):
    f = "M19 16.3C20 17.5 20.8 18.2 20.8 19.2A1.8 1.8 0 0 1 17.2 19.2C17.2 18.4 17.9 17.8 19 16.3Z"
    return [
        *env(S, 2, 7, 10, 10, 0.55),
        shell(rect(17, 2, 4, 13, 2)), shell(circle(19, 18, 3.5)),
        Part("dot", f),
    ]


@icon("spam-score", CAT, "Semicircle gauge with a needle and a small envelope under its pivot",
      tags=["spam rating", "spam check", "spamassassin", "junk score", "email test", "gauge", "risk score"])
def _(S):
    return [
        line("M3 14A9 9 0 0 1 21 14"),
        line(seg(12, 13.5, 17, 8)), dot(12, 13.5, 1.6),
        *env(S, 7.5, 16.8, 9, 5.2, 0.6),
    ]


@icon("email-open-rate", CAT, "Open envelope with a percent sign inside its raised flap",
      tags=["open rate", "opens", "email stats", "campaign metrics", "read rate", "engagement", "percentage opened"])
def _(S):
    return [
        shell(poly([(2, 10), (12, 2.5), (22, 10), (22, 21), (2, 21)], closed=True, r=S.r)),
        detail(poly([(2, 10), (12, 16.5), (22, 10)], r=S.r)),
        *pct(12, 9.3, detail, 1.0),
    ]


# ============================================================================ tracking and analytics

def tag_solid(cx, base, rotd, w=4.6, h=8.5, hole=0.9):
    """Solid hanging-tag silhouette with a punched hole, standing on (cx, base) and tilted by rotd degrees."""
    pts = [(cx - w / 2, base), (cx - w / 2, base - h * 0.62), (cx, base - h), (cx + w / 2, base - h * 0.62), (cx + w / 2, base)]
    pts = rot(pts, rotd, cx, base)
    hx, hy = rot([(cx, base - h * 0.55)], rotd, cx, base)[0]
    return solid(path_to_d(D(P(poly(pts, closed=True)), P(circle(hx, hy, hole)))))


@icon("tag-manager", CAT, "Open box container with three small tags standing out over its rim",
      tags=["gtm", "tracking tags", "script container", "marketing tags", "pixel manager", "tag container", "analytics setup"])
def _(S):
    return [
        shell(poly([(2, 12), (22, 12), (19.5, 21.5), (4.5, 21.5)], closed=True, r=S.r)),
        tag_solid(6, 9.5, -14), tag_solid(12, 9.5, 0), tag_solid(18, 9.5, 14),
    ]


@icon("event-tracking", CAT, "Arrow cursor clicking with ripple arcs, beside a column of three dots",
      tags=["click tracking", "events", "analytics events", "interaction", "goal tracking", "user actions", "custom events"])
def _(S):
    return [
        cursor(S, 7, 9, 1.2),
        line(arc(7, 9, 3.2, 195, 265)), line(arc(7, 9, 5.6, 200, 262)),
        dot(19.5, 5, 1.6), dot(19.5, 12, 1.6), dot(19.5, 19, 1.6),
    ]


@icon("data-layer", CAT, "Three stacked flat layers with code chevrons on the top layer",
      tags=["datalayer", "layers", "tag data", "tracking data", "stack", "analytics layer", "variables"])
def _(S):
    return [
        shell(poly([(12, 2), (22, 8), (12, 14), (2, 8)], closed=True, r=S.r)),
        detail(poly([(10.4, 6), (8.6, 8), (10.4, 10)])), detail(poly([(13.6, 6), (15.4, 8), (13.6, 10)])),
        line(poly([(2, 12), (12, 18), (22, 12)], r=S.r)),
        line(poly([(2, 16), (12, 22), (22, 16)], r=S.r)),
    ]


@icon("tracking-snippet", CAT, "Code angle brackets with a small eye between them",
      tags=["tracking code", "script tag", "pixel", "analytics snippet", "embed code", "monitoring script", "spy pixel"])
def _(S):
    eye = L(S, "M8.6 12Q12 7.8 15.4 12Q12 16.2 8.6 12Z", ellipse(12, 12, 3.8, 2.7))
    return [
        line(poly([(7, 5.5), (2, 12), (7, 18.5)], r=S.r)), line(poly([(17, 5.5), (22, 12), (17, 18.5)], r=S.r)),
        shell(eye), dot(12, 12, 1.1),
    ]


@icon("user-session", CAT, "Browser window with a small person avatar and a stopwatch side by side",
      tags=["session", "visit", "session duration", "time on site", "visitor session", "session replay", "analytics"])
def _(S):
    return win(S, 2, 3, 20, 18, 4.5) + [
        dot(8, 12, 1.8), Part("dot", "M4.8 18.2A3.2 3.2 0 0 1 11.2 18.2Z"),
        shell(circle(16.2, 15, 3.6)), detail(seg(16.2, 15, 16.2, 13)),
        line(seg(16.2, 10.3, 16.2, 11.4)),
    ]


@icon("unique-visitors", CAT, "Row of three people with the middle one marked by a fingerprint on the chest",
      tags=["unique users", "distinct visitors", "new visitors", "audience size", "fingerprint", "identity", "analytics"])
def _(S):
    out = [
        dot(3.8, 11.5, 1.5), Part("solid", "M1.5 20A2.3 2.3 0 0 1 6.1 20V20Z") if False else solid("M1.8 20.5V18.8A2 2 0 0 1 5.8 18.8V20.5Z"),
        dot(20.2, 11.5, 1.5), solid("M18.2 20.5V18.8A2 2 0 0 1 22.2 18.8V20.5Z"),
        shell(circle(12, 6, 3.2)),
        shell(L(S, "M7.5 21.5V17L9.5 13.5H14.5L16.5 17V21.5Z", "M7.5 21.5V17.5A4.5 4 0 0 1 16.5 17.5V21.5Z")),
        thin("M10 19.8V17.6A2 2 0 0 1 14 17.6V19.8", 0.9), thin("M11.5 19.8V17.8A0.5 0.5 0 0 1 12.5 17.8V19.8", 0.8),
    ]
    return out


@icon("exit-page", CAT, "Browser page with an arrow leaving through its right edge",
      tags=["exit", "last page", "leave site", "drop off page", "bounce page", "session end", "analytics"])
def _(S):
    return win(S, 2, 3, 16, 18, 4.5) + [
        *arrow(S, 8.5, 14, 22, 14, 3.0),
    ]


@icon("returning-visitor", CAT, "Person with a looping arrow curling back up toward a browser window",
      tags=["repeat visitor", "return visit", "loyal user", "retention", "come back", "recurring", "analytics"])
def _(S):
    return [
        dot(7.5, 14, 2.1), solid("M3 21.5V20A4.5 4.5 0 0 1 12 20V21.5Z"),
        line("M3 10C3 5.5 6.5 4.5 10.5 6"), head(S, (11.2, 6.3), 18, 2.8),
        *win(S, 14, 3, 8, 9, 3.5, 2),
    ]


@icon("cross-device-tracking", CAT, "Phone, laptop and tablet linked by dotted lines to one person above",
      tags=["multi device", "cross device", "device graph", "user identity", "omnichannel", "tracking", "phone laptop tablet"])
def _(S):
    out = [dot(12, 3.6, 1.9), solid("M8.5 10V9A3.5 3.5 0 0 1 15.5 9V10Z"),
           shell(rect(2, 15.5, 4, 6.5, L(S, 0, 1.6))), shell(rect(9.5, 16.5, 5, 5.5, L(S, 0, 1.6))), shell(rect(18, 14, 4, 8, L(S, 0, 1.6)))]
    for (tx, ty) in ((4, 13.3), (12, 14.4), (20, 11.8)):
        for f in (0.35, 0.7):
            out.append(dot(12 + (tx - 12) * f, 12 + (ty - 12) * f, 0.7))
    return out


# ============================================================================ search and SEO

@icon("search-intent", CAT, "Magnifying glass with a small thought bubble rising above it",
      tags=["user intent", "why searching", "query intent", "informational", "transactional", "navigational", "searcher goal"])
def _(S):
    return [
        *magnifier(S, 8.5, 14.5, 5.2),
        shell(ellipse(17, 6, 4.6, 3.4)),
        dot(14.8, 6, 0.8), dot(17.2, 6, 0.8), dot(19.6, 6, 0.8) if False else dot(17, 6, 0.8),
    ]


@icon("knowledge-panel", CAT, "Search results lines on the left and a tall boxed card with an image block on the right",
      tags=["knowledge graph", "info box", "entity card", "search sidebar", "fact card", "serp feature", "brand panel"])
def _(S):
    return [
        line(seg(2, 6, 9, 6)), line(seg(2, 11, 9, 11)), line(seg(2, 16, 9, 16)),
        shell(rect(12.5, 2.5, 9.5, 19, min(S.R, 2.5))),
        Part("dot", rect(15, 5.2, 4.5, 4.4, 0.6)),
        detail(seg(15, 13.2, 19.5, 13.2)), detail(seg(15, 17, 18.2, 17)),
    ]


@icon("sitelinks", CAT, "One bold result line with a two by two grid of short link lines indented under it",
      tags=["site links", "search result links", "sub links", "serp sitelinks", "quick links", "deep links", "navigation links"])
def _(S):
    return [
        Part("solid", rect(2, 2.8, 14, 3, 0.6)),
        line(seg(6, 11, 11, 11)), line(seg(14.5, 11, 19.5, 11)),
        line(seg(6, 16, 11, 16)), line(seg(14.5, 16, 19.5, 16)),
        line(seg(3, 8.8, 3, 19.5)) if False else line(seg(2, 10, 2, 10)) if False else line(seg(3, 9, 3, 20)),
    ]


@icon("search-snippet", CAT, "Single search result with a bold title line, a short address line and two text lines",
      tags=["serp result", "snippet", "meta description", "search listing", "result preview", "organic result", "title and url"])
def _(S):
    return [
        shell(rect(2, 2, 20, 20, min(S.R, 3))),
        Part("dot", rect(5, 5, 11, 2.6, 0.5)),
        detail(seg(5, 10.5, 9, 10.5)),
        detail(seg(5, 14.5, 19, 14.5)), detail(seg(5, 18, 15, 18)),
    ]


@icon("rich-snippet", CAT, "Search result with a thumbnail, a title line and a row of five stars under it",
      tags=["review stars", "star rating snippet", "structured data", "schema markup", "serp feature", "enhanced result", "rating result"])
def _(S):
    return [
        shell(rect(2, 2, 7, 7, min(S.R, 1.5))),
        line(seg(12, 4, 22, 4)), line(seg(12, 8, 18, 8)),
        *stars(S, 12, 15, 5, 4.2, 2.0),
        line(seg(2, 20.5, 16, 20.5)),
    ]


@icon("meta-tag", CAT, "Tag shape with angle brackets drawn on its face",
      tags=["meta", "html meta", "head tag", "meta description", "seo tag", "metadata", "code tag"])
def _(S):
    return [
        shell(tagshape(S, 1.5, 4.5, 21, 15, 4.5)),
        detail(poly([(9, 8.8), (6, 12), (9, 15.2)])), detail(poly([(13, 8.8), (16, 12), (13, 15.2)])),
    ]


@icon("title-tag", CAT, "Browser tab shape with a bold capital T inside it",
      tags=["page title", "title element", "seo title", "tab title", "html title", "heading", "serp title"])
def _(S):
    return [
        shell(L(S, "M2 20.5V6.5L4 4.5H15L17 6.5V20.5Z", "M2 20.5V7.5A3 3 0 0 1 5 4.5H14A3 3 0 0 1 17 7.5V20.5Z")),
        line(seg(17, 20.5, 22, 20.5)),
        detail(seg(6.2, 9.5, 12.8, 9.5)), detail(seg(9.5, 9.5, 9.5, 17)),
    ]


@icon("keyword-research", CAT, "Magnifying glass hovering over a key",
      tags=["keyword finder", "keyword tool", "search terms", "keyword ideas", "seo research", "key", "query research"])
def _(S):
    return [
        *magnifier(S, 8.5, 7.5, 4.8),
        shell(circle(5, 19, 2.6)), line(seg(7.6, 19, 20, 19)), line(seg(17.5, 19, 17.5, 22)), line(seg(14.5, 19, 14.5, 21.4)),
    ]


@icon("keyword-stuffing", CAT, "Page bulging at the sides with words and tags spilling out of the top",
      tags=["over optimization", "black hat seo", "spam keywords", "repeated keywords", "seo penalty", "too many keywords", "bloated page"])
def _(S):
    barrel = L(S, "M5.5 21.5L3 17V11L5.5 8H18.5L21 11V17L18.5 21.5Z", "M5.5 21.5C2 18 2 11 5.5 8H18.5C22 11 22 18 18.5 21.5Z")
    return [
        shell(barrel),
        detail(seg(7.5, 12, 16.5, 12)), detail(seg(7.5, 16, 14.5, 16)),
        Part("solid", rect(5, 3, 4.5, 2, 0.5)), Part("solid", rect(11, 1.6, 3.2, 2.2, 0.5)),
        solid(poly([(16, 5), (16, 2.5), (20.5, 2.5), (22, 3.8), (20.5, 5)], closed=True)),
    ]


@icon("keyword-difficulty", CAT, "Key lying under a semicircle gauge with the needle pointing high",
      tags=["keyword competition", "ranking difficulty", "kd score", "competitive keyword", "hard keyword", "gauge", "seo difficulty"])
def _(S):
    return [
        line("M3.5 12.5A8.5 8.5 0 0 1 20.5 12.5"),
        line(seg(12, 12, 17.2, 6.2)), dot(12, 12, 1.6),
        shell(circle(5, 19, 2.6)), line(seg(7.6, 19, 20, 19)), line(seg(17.5, 19, 17.5, 22)), line(seg(14.5, 19, 14.5, 21.4)),
    ]


@icon("search-volume", CAT, "Magnifying glass with three rising bars inside its lens",
      tags=["monthly searches", "query volume", "search demand", "keyword volume", "popularity", "bars", "search count"])
def _(S):
    return [
        *magnifier(S, 10.5, 10.5, 7.5),
        Part("dot", rect(6.8, 12, 2.2, 3.4, 0.4)), Part("dot", rect(10, 9.6, 2.2, 5.8, 0.4)), Part("dot", rect(13.2, 7.6, 2.2, 7.8, 0.4)),
    ]


@icon("search-ranking", CAT, "Three step podium with a magnifying glass standing on the top step",
      tags=["serp position", "rank tracking", "first place", "top result", "podium", "ranking position", "page one"])
def _(S):
    return [
        shell(poly([(2, 21.5), (2, 17.5), (8, 17.5), (8, 14.5), (16, 14.5), (16, 18.5), (22, 18.5), (22, 21.5)], closed=True, r=S.r * 0.5)),
        *magnifier(S, 11, 7, 3.6),
    ]


@icon("domain-authority", CAT, "Globe with a semicircle gauge above it and the needle near full",
      tags=["da score", "site authority", "domain rating", "trust score", "link strength", "seo metric", "gauge"])
def _(S):
    return [
        line("M4.5 9A7.5 7.5 0 0 1 19.5 9"),
        line(seg(12, 8.5, 17.4, 3.8)), dot(12, 8.5, 1.5),
        *globe(S, 12, 17.3, 4.7),
    ]


@icon("organic-traffic", CAT, "Leaf with an upward trending arrow running along its midrib",
      tags=["natural traffic", "free traffic", "unpaid search", "seo growth", "eco", "growth", "search visitors"])
def _(S):
    return [
        shell(L(S, "M3 21L4 12L10 5L21 3L20 14L13 20Z", "M3.5 20.5C3 11 9 4 21 3C21.5 15 14.5 21 3.5 20.5Z")),
        detail(poly([(7, 16.5), (11, 12.5), (13.5, 14.5), (17.5, 9.5)])),
        head(S, (17.8, 9.2), -52, 2.6, detail),
    ]


@icon("geotargeting", CAT, "Target ring with crosshair ticks and a map pin in the centre",
      tags=["geo targeting", "local targeting", "location targeting", "regional ads", "local seo", "radius", "map pin"])
def _(S):
    pin = "M12 17.8C9.8 15 8.4 13.6 8.4 11.4A3.6 3.6 0 0 1 15.6 11.4C15.6 13.6 14.2 15 12 17.8Z"
    hole = path_to_d(D(P(pin), P(circle(12, 11.2, 1.3))))
    return [
        shell(circle(12, 12, 8)),
        line(seg(12, 2, 12, 4.5)), line(seg(12, 19.5, 12, 22)), line(seg(2, 12, 4.5, 12)), line(seg(19.5, 12, 22, 12)),
        Part("dot", hole),
    ]


@icon("seo-audit", CAT, "Clipboard with rising bars and a magnifying glass over its corner",
      tags=["site audit", "seo check", "website review", "technical seo", "health check", "checklist", "inspection"])
def _(S):
    return [
        shell(rect(2, 4, 12, 17.5, min(S.R, 2))),
        Part("dot", rect(5, 1.8, 6, 3.4, 0.8)) if False else detail(seg(5.5, 4, 10.5, 4)),
        Part("dot", rect(4.8, 14.5, 2, 3.5, 0.3)), Part("dot", rect(8, 11.5, 2, 6.5, 0.3)),
        *magnifier(S, 17.3, 14.3, 3.5, 3.3),
    ]


@icon("search-index", CAT, "Card catalog drawer with index cards and a magnifying glass resting on top",
      tags=["indexing", "indexed pages", "crawl", "catalog", "index card", "search database", "sitemap"])
def _(S):
    return [
        shell(rect(2, 13, 16, 8.5, min(S.R, 2))),
        detail(rect(7, 16, 6, 2.5, 0.5)) if False else Part("dot", rect(7, 16, 6, 2.2, 0.4)),
        Part("solid", rect(3.5, 7.5, 4, 3.5, 0.4)), Part("solid", rect(9, 7.5, 4, 3.5, 0.4)),
        *magnifier(S, 17, 7.3, 3.6, 3.4),
    ]


@icon("search-engine-optimization", CAT, "Magnifying glass with an upward arrow rising through its lens",
      tags=["seo", "optimize for search", "rank higher", "search growth", "improve ranking", "arrow up", "organic search"])
def _(S):
    return [
        *magnifier(S, 10.5, 10.5, 7.5),
        detail(seg(10.5, 14.8, 10.5, 6.8)), head(S, (10.5, 6.2), -90, 3.0, detail),
    ]


@icon("pillar-page", CAT, "Large central page joined by short lines to four smaller pages around it",
      tags=["pillar content", "topic cluster", "hub page", "cornerstone content", "content hub", "internal links", "seo structure"])
def _(S):
    out = [shell(rect(8, 7, 8, 10, L(S, 0, 2.6)))]
    for sx, sy, ex, ey in ((1.5, 1.5, 8.2, 7.2), (18, 1.5, 15.8, 7.2), (1.5, 18, 8.2, 16.8), (18, 18, 15.8, 16.8)):
        out.append(Part("solid", rect(sx, sy, 4.5, 4.5, L(S, 0, 1.2))))
        out.append(line(seg(sx + 2.25, sy + 2.25, ex, ey)))
    return out


@icon("evergreen-content", CAT, "Page with a small evergreen pine tree in its lower half",
      tags=["timeless content", "always relevant", "pine tree", "long lasting", "durable content", "seo content", "article"])
def _(S):
    tree = poly([(12, 11.5), (9.2, 15.2), (10.8, 15.2), (8.2, 18.6), (11.2, 18.6), (11.2, 20), (12.8, 20), (12.8, 18.6), (15.8, 18.6), (13.2, 15.2), (14.8, 15.2)], closed=True)
    return [
        shell(rect(4, 1.5, 16, 21, min(S.R, 3))),
        detail(seg(8, 5.5, 16, 5.5)), detail(seg(8, 8.8, 13, 8.8)),
        Part("dot", tree),
    ]


# ----------------------------------------------------------------------------- late additions

@icon("win-back-email", CAT, "Envelope above a boomerang shaped curved arrow that swings back",
      tags=["win back", "re engagement", "lapsed subscriber", "come back", "inactive customers", "retention email", "boomerang"])
def _(S):
    return [
        *env(S, 5, 2.5, 12, 8.5, 0.55),
        line("M21 5.5C21.5 15 14 20 5.5 15.5"), head(S, (5, 15.2), 208, 3.0),
    ]


@icon("html-email", CAT, "Envelope with angle bracket code tags and a slash printed on its front",
      tags=["html mail", "coded email", "rich email", "email markup", "responsive email", "code", "email development"])
def _(S):
    return [
        *env(S, 2, 3, 20, 18, 0.36),
        detail(poly([(8.8, 12), (6.2, 15), (8.8, 18)])), detail(poly([(15.2, 12), (17.8, 15), (15.2, 18)])),
        detail(seg(13, 12, 11, 18)),
    ]
