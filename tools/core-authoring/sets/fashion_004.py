"""TypeIcon Core: fashion (batch fashion_004).

Accessories, sewing and needlecraft tools, fasteners, trims and fabric patterns, plus a few fashion
places and garments. Everything is drawn front-on as a simple symbol on the 24 grid.
"""
import math

from dsl import D, I, P, Part, ST, U, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar  # noqa: F401

CAT = "fashion"


# --------------------------------------------------------------------------- helpers

def _sector(cx, cy, r, a0, a1):
    """Pie sector (closed path) from angle a0 to a1, clockwise on screen, degrees."""
    x0, y0 = polar(cx, cy, r, a0)
    x1, y1 = polar(cx, cy, r, a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f"M{fmt(cx)} {fmt(cy)}L{fmt(x0)} {fmt(y0)}A{fmt(r)} {fmt(r)} 0 {large} 1 {fmt(x1)} {fmt(y1)}Z"


def _union_d(*ds):
    """Outline of the union of closed shapes (fluffy or lobed silhouettes)."""
    return path_to_d(U(*[P(d) for d in ds]))


def _scallops(p0, p1, n, bulge):
    """Continuation path from p0 to p1 made of n arcs bulging to one side (+ right of travel)."""
    out = []
    for i in range(n):
        x1 = p0[0] + (p1[0] - p0[0]) * (i + 1) / n
        y1 = p0[1] + (p1[1] - p0[1]) * (i + 1) / n
        seglen = math.hypot(p1[0] - p0[0], p1[1] - p0[1]) / n
        rr = seglen / 2 * bulge
        out.append(f"A{fmt(rr)} {fmt(rr)} 0 0 1 {fmt(x1)} {fmt(y1)}")
    return "".join(out)


# ============================================================================ chunk 1: neckwear and accessories

@icon("side-release-buckle", CAT, "Plastic strap buckle: a male clip with two prongs sliding into its open female socket.",
      tags=["buckle", "clip", "strap", "backpack", "fastener", "belt", "clasp"])
def _(S):
    rr = min(S.R, 2)
    return [
        shell(rect(2.5, 6, 6, 12, rr)),
        line(seg(8.5, 9, 16, 9)),
        line(seg(8.5, 15, 16, 15)),
        line(poly([(13.5, 5), (21, 5), (21, 19), (13.5, 19)], r=S.r)),
    ]


@icon("cummerbund", CAT, "Wide pleated waist sash with horizontal pleats, worn with a tuxedo.",
      tags=["sash", "tuxedo", "formal", "waist", "pleated", "black tie", "waistband"])
def _(S):
    body = "M3 6Q12 8 21 6V18Q12 20 3 18Z"
    return [
        shell(body),
        detail("M3 10.5Q12 12.5 21 10.5"),
        detail("M3 14Q12 16 21 14"),
    ]


@icon("pageant-sash", CAT, "Wide ribbon sash worn diagonally from shoulder to hip, with a rosette and two tails at the hip.",
      tags=["sash", "pageant", "beauty queen", "ribbon", "winner", "prom", "miss"])
def _(S):
    band = poly([(2.5, 3), (10.5, 3), (19, 13), (12, 14.5)], closed=True)
    return [
        shell(_union_d(band, circle(15.5, 14, 3.4))),
        dot(15.5, 14, 1.2),
        line(poly([(13.5, 18), (11.5, 21.5)])),
        line(poly([(17.5, 18), (20, 21.5)])),
        dot(8.2, 6.8, 1.0),
    ]


@icon("bolo-tie", CAT, "Braided cord necktie with a round clasp slide and metal tips on the hanging ends.",
      tags=["western", "cowboy", "string tie", "cord", "neckwear", "clasp", "slide"])
def _(S):
    return [
        line("M4.5 3Q5.5 7.6 9.9 7.9"),
        line("M19.5 3Q18.5 7.6 14.1 7.9"),
        shell(circle(12, 10, 3)),
        dot(12, 10, 1.1),
        line(seg(10.5, 12.6, 9.6, 18.5)),
        line(seg(13.5, 12.6, 14.4, 18.5)),
        solid(poly([(8.4, 18.5), (10.8, 18.5), (10.3, 21.5), (8.9, 21.5)], closed=True)),
        solid(poly([(13.2, 18.5), (15.6, 18.5), (15.1, 21.5), (13.7, 21.5)], closed=True)),
    ]


@icon("ascot-tie", CAT, "Wide folded neck scarf with a small knot, a flared lower end and a pin.",
      tags=["cravat", "scarf", "neckwear", "formal", "gentleman", "pin", "victorian"], aliases=["cravat"])
def _(S):
    return [
        shell(circle(12, 6, 2.5) if S.name == "rounded" else poly(regular(12, 6, 3, 4, start=-45), closed=True)),
        shell(poly([(9.5, 9), (14.5, 9), (19, 21), (12, 18), (5, 21)], closed=True, r=S.r)),
        dot(12, 13.2, 1.1),
    ]


@icon("neckerchief", CAT, "Triangular scarf worn tied around the neck with the ends held in a ring.",
      tags=["scarf", "kerchief", "scout", "bandana", "neck scarf", "woggle", "cowboy"], aliases=["kerchief"])
def _(S):
    outline = "M3 4Q12 10 21 4L12 21Z" if S.name == "line" else "M3.5 4.5Q12 10 20.5 4.5Q21.5 4.5 21 5.5L12.8 20Q12 21.3 11.2 20L3 5.5Q2.5 4.5 3.5 4.5Z"
    return [shell(outline), detail(circle(12, 11.5, 2))]


@icon("pocket-square", CAT, "Suit breast pocket with a folded square of cloth showing three points.",
      tags=["handkerchief", "suit", "jacket", "formal", "wedding", "groom", "fold"])
def _(S):
    k = S.r * 0.6
    outline = poly([(3, 21), (3, 11), (5, 11), (7, 5), (10, 8.5), (12, 4), (14, 8.5), (17, 5), (19, 11), (21, 11), (21, 21)],
                   closed=True, r=k)
    return [shell(outline), detail(seg(3.5, 14.5, 20.5, 14.5))]


@icon("feather-boa", CAT, "Long fluffy strand of feathers draped in an S curve.",
      tags=["boa", "feather", "costume", "cabaret", "showgirl", "fluffy", "dress up"])
def _(S):
    n = 9
    bumps = 5
    amp = 0.75 if S.name == "line" else 0.95
    left, right = [], []
    for i in range(n * 4 + 1):
        t = i / (n * 4)
        cx = 12 + 5.5 * math.sin(2 * math.pi * t)
        cy = 4.2 + 15.6 * t
        dx = 5.5 * 2 * math.pi * math.cos(2 * math.pi * t)
        dy = 15.6
        ln = math.hypot(dx, dy)
        nx, ny = dy / ln, -dx / ln
        w = 2.5 + amp * math.cos(2 * math.pi * bumps * t) + (0.0 if 0.06 < t < 0.94 else -0.6)
        left.append((cx + nx * w, cy + ny * w))
        right.append((cx - nx * w, cy - ny * w))
    pts = left + right[::-1]
    mids = [((pts[i][0] + pts[(i + 1) % len(pts)][0]) / 2, (pts[i][1] + pts[(i + 1) % len(pts)][1]) / 2) for i in range(len(pts))]
    d = f"M{fmt(mids[-1][0])} {fmt(mids[-1][1])}"
    for i in range(len(pts)):
        d += f"Q{fmt(pts[i][0])} {fmt(pts[i][1])} {fmt(mids[i][0])} {fmt(mids[i][1])}"
    return [shell(d + "Z")]


@icon("epaulette", CAT, "Shoulder board with a button and a row of hanging fringe.",
      tags=["shoulder", "military", "uniform", "officer", "fringe", "naval", "rank"])
def _(S):
    board = poly([(6, 3), (18, 3), (20, 13), (4, 13)], closed=True, r=S.r * 0.8)
    return [
        shell(board),
        dot(12, 7.6, 1.3),
        line(seg(4, 13, 4, 20.5)),
        line(seg(8, 13, 8, 20.5)),
        line(seg(12, 13, 12, 20.5)),
        line(seg(16, 13, 16, 20.5)),
        line(seg(20, 13, 20, 20.5)),
    ]


@icon("wrist-corsage", CAT, "Small flower cluster with two leaves sitting on an elastic wrist band.",
      tags=["corsage", "prom", "wedding", "flowers", "bracelet", "homecoming", "floral"])
def _(S):
    pet = 2.5 + (0.3 if S.name == "rounded" else 0)
    petals = [circle(*polar(12, 8, 3.1, a), pet) for a in (-90, -18, 54, 126, 198)]
    leaf_l = "M6.5 12Q3 12 2.8 9Q6 9 6.5 12Z"
    leaf_r = "M17.5 12Q21 12 21.2 9Q18 9 17.5 12Z"
    return [
        shell(_union_d(*petals)),
        dot(12, 8, 1.2),
        shell(ellipse(12, 18, 8.5, 3)),
        line(leaf_l),
        line(leaf_r),
    ]


@icon("tie-rack", CAT, "Rail with three neckties hanging from it.",
      tags=["ties", "neckties", "closet", "wardrobe", "hanger", "organizer", "storage"])
def _(S):
    def tie(x):
        return shell(poly([(x - 1, 5), (x + 1, 5), (x + 1.6, 18), (x, 20.5), (x - 1.6, 18)], closed=True, r=S.r * 0.3))
    return [
        line(seg(2.5, 4, 21.5, 4)),
        tie(5.5), tie(12), tie(18.5),
    ]


@icon("fingerless-gloves", CAT, "Glove cut off at the knuckles so the fingers stick out, with a gloved thumb.",
      tags=["gloves", "knitted", "winter", "biker", "mitts", "hand warmer", "cut off"])
def _(S):
    body = poly([(7, 21), (7, 17), (3.5, 13.5), (5.5, 11.5), (8, 14), (8, 11.5), (18, 11.5), (18, 21)], closed=True, r=S.r * 0.6)
    return [
        shell(body),
        detail(seg(8.5, 18, 17.5, 18)),
        line(seg(9.5, 4.5, 9.5, 11.5)),
        line(seg(13, 4.5, 13, 11.5)),
        line(seg(16.5, 4.5, 16.5, 11.5)),
    ]


@icon("opera-gloves", CAT, "Long elegant glove with a raised hand and a forearm tube that ends in a scalloped cuff.",
      tags=["long gloves", "evening", "formal", "gala", "satin", "elegant", "formalwear"])
def _(S):
    body = poly([(8, 21), (8, 13), (4.5, 10), (6.5, 8), (8, 9.5), (8, 6), (10, 3), (14, 3), (16, 6), (16, 21)], closed=True, r=S.r * 0.7)
    return [
        shell(body),
        detail("M8.5 17.5Q10.3 19.5 12 17.5Q13.7 19.5 15.5 17.5"),
    ]


@icon("hand-muff", CAT, "Fur hand warmer drawn as a tube with an open end.",
      tags=["muff", "hand warmer", "fur", "winter", "cold", "victorian", "warm"])
def _(S):
    body = "M18 6.5H10A5.5 5.5 0 0 0 10 17.5H18A2.75 5.5 0 0 0 18 6.5Z"
    return [
        shell(body),
        detail("M18 6.5A2.75 5.5 0 0 0 18 17.5" if S.name == "line" else "M18 7A2.25 5 0 0 0 18 17"),
    ]


@icon("folding-fan", CAT, "Hand fan opened into a half circle with radiating ribs and a pivot at the bottom.",
      tags=["fan", "hand fan", "japanese", "spanish", "cooling", "flamenco", "ribs"])
def _(S):
    cx, cy = 12, 19.5
    ribs = [detail(f"M{fmt(polar(cx, cy, 4.5, a)[0])} {fmt(polar(cx, cy, 4.5, a)[1])}L{fmt(polar(cx, cy, 10, a)[0])} {fmt(polar(cx, cy, 10, a)[1])}") for a in (240, 270, 300)]
    return [shell(_sector(cx, cy, 11, 205, 335))] + ribs + [dot(cx, cy - 0.2, 1.1)]


# ============================================================================ chunk 2: small accessories and sewing tools

def _zig(p0, p1, n, amp):
    """Zigzag polyline from p0 to p1 with n teeth (sideways offset amp)."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    ln = math.hypot(dx, dy)
    nx, ny = -dy / ln, dx / ln
    pts = [p0]
    for i in range(n * 2):
        t = (i + 1) / (n * 2)
        sgn = 1 if i % 2 == 0 else -1
        off = 0 if i == n * 2 - 1 else sgn * amp
        pts.append((p0[0] + dx * t + nx * off, p0[1] + dy * t + ny * off))
    return pts


@icon("handkerchief", CAT, "Square cloth set on the diagonal with one folded corner and a small embroidered mark.",
      tags=["hanky", "hankie", "cloth", "tissue", "pocket", "cotton", "embroidered"], aliases=["hanky"])
def _(S):
    a = math.radians(16)
    c, s_ = math.cos(a), math.sin(a)
    def tr(x, y):
        return (12 + x * c - y * s_, 12 + x * s_ + y * c)
    h = 8.6
    corners = [tr(-h, -h), tr(h, -h), tr(h, h), tr(-h, h)]
    fold = [tr(0, -h), tr(h * 0.05, -h * 0.05), tr(h, 0)]
    return [
        shell(poly(corners, closed=True, r=S.r * 0.6)),
        detail(poly([tr(0.5, -h), tr(0.5, -0.5), tr(h, -0.5)], r=S.r * 0.3)),
        dot(*tr(-3.6, 3.6), 1.4),
    ]


@icon("walking-cane", CAT, "Straight walking stick with a curved crook handle and a rubber tip.",
      tags=["cane", "walking stick", "gentleman", "elderly", "mobility", "support", "crook"])
def _(S):
    return [
        line("M15 18V9A4.5 4.5 0 0 0 6 9V11"),
        solid(rect(13.5, 18, 3, 3.5, 0.6 if S.name == "rounded" else 0)),
    ]


@icon("hair-clip", CAT, "Open alligator style hair clip with two hinged jaws.",
      tags=["barrette", "hair", "accessory", "clasp", "hairstyle", "alligator clip", "salon"], aliases=["barrette"])
def _(S):
    k = S.r * 0.6
    return [
        shell(poly([(3.5, 8), (21, 4.5), (21, 8.5), (3.5, 11.5)], closed=True, r=k)),
        shell(poly([(3.5, 12.5), (21, 15.5), (21, 19.5), (3.5, 16)], closed=True, r=k)),
    ]


@icon("hair-bow", CAT, "Large ribbon bow with two loops, a knot and two short tails.",
      tags=["ribbon", "bow", "hair", "accessory", "girl", "gift", "barrette"])
def _(S):
    def side(m):
        x = lambda v: 12 + m * (v - 12)
        d = f"M{x(10.5)} 11.5C{x(8)} 6 {x(4)} 4.5 {x(3)} 8C{x(2.5)} 12 {x(5)} 15 {x(10.5)} 12.5Z"
        return d
    return [
        shell(side(1)),
        shell(side(-1)),
        shell(rect(10, 9.5, 4, 5.5, 1 if S.name == "rounded" else 0)),
        line(poly([(10.8, 16), (8, 21)])),
        line(poly([(13.2, 16), (16, 21)])),
    ]


@icon("hair-stick", CAT, "Ornamental hair stick with a dangling bead, pushed through a round bun.",
      tags=["hairpin", "bun", "chinese", "japanese", "kanzashi", "updo", "accessory"])
def _(S):
    return [
        shell(circle(8, 16, 4.6)),
        dot(8, 16, 1.2),
        line(seg(11.4, 12.6, 19, 5)),
        line(seg(4.6, 19.4, 3.6, 20.4)),
        dot(19.6, 4.4, 1.5),
        line(seg(16.6, 7.4, 16.6, 10.2)),
        dot(16.6, 12.3, 1.4),
    ]


@icon("shirt-collar", CAT, "Close view of a pointed shirt collar over a button placket.",
      tags=["collar", "dress shirt", "formal", "button", "office", "neckline", "shirt"])
def _(S):
    k = S.r * 0.5
    return [
        shell(poly([(6.5, 3), (3.5, 11.5), (11.5, 14), (9, 4.5)], closed=True, r=k)),
        shell(poly([(17.5, 3), (20.5, 11.5), (12.5, 14), (15, 4.5)], closed=True, r=k)),
        line(seg(12, 14.5, 12, 21)),
        dot(12, 17.3, 1.5),
    ]


@icon("jeans-pocket", CAT, "Back pocket of a pair of jeans with a pointed bottom and curved decorative stitching.",
      tags=["denim", "pocket", "stitching", "jeans", "back pocket", "trousers", "pants"])
def _(S):
    return [
        shell(poly([(4, 3), (20, 3), (20, 14), (12, 21), (4, 14)], closed=True, r=S.r)),
        detail("M7.5 7.5Q12 13.5 16.5 7.5"),
    ]


@icon("thread-spool", CAT, "Spool wound with thread and a loose strand trailing from the side.",
      tags=["thread", "cotton", "sewing", "reel", "bobbin", "tailor", "stitch"], aliases=["spool-of-thread"])
def _(S):
    body = poly([(5, 3), (19, 3), (19, 6), (17, 6), (17, 18), (19, 18), (19, 21), (5, 21), (5, 18), (7, 18), (7, 6), (5, 6)],
                closed=True, r=S.r * 0.4)
    return [
        shell(body),
        detail(seg(7.5, 10, 16.5, 10)),
        detail(seg(7.5, 14, 16.5, 14)),
        line("M17 12Q21.5 12 21.5 16"),
    ]


@icon("bobbin", CAT, "Short sewing machine bobbin in perspective: two round flanges with thread wound between them.",
      tags=["sewing machine", "thread", "spool", "bottom thread", "tailor", "stitch", "reel"])
def _(S):
    w = 5.0 if S.name == "line" else 5.4
    outline = _union_d(ellipse(12, 6.5, 8, 3), ellipse(12, 17.5, 8, 3), rect(12 - w, 6.5, 2 * w, 11))
    return [
        shell(outline),
        detail(ellipse(12, 6.5, 2.4, 0.9)),
        detail(f"M{fmt(12 - w + 0.5)} 11Q12 13.4 {fmt(12 + w - 0.5)} 11"),
    ]


@icon("seam-ripper", CAT, "Small tool with a grip and a forked hook tip; the longer prong ends in a ball.",
      tags=["unpick", "unstitch", "sewing", "tailor", "remove stitches", "rip", "thread"])
def _(S):
    import math as _m
    def rot(pts, deg=45, cx=12.0, cy=12.0):
        a = _m.radians(deg)
        c, s_ = _m.cos(a), _m.sin(a)
        return [(cx + (x - cx) * c - (y - cy) * s_, cy + (x - cx) * s_ + (y - cy) * c) for x, y in pts]
    def sg(a, b):
        (x1, y1), (x2, y2) = rot([a, b])
        return seg(x1, y1, x2, y2)
    grip = rot([(9.5, 11), (14.5, 11), (14.5, 21), (9.5, 21)])
    bx, by = rot([(9, 3.3)])[0]
    return [
        shell(poly(grip, closed=True, r=S.r * 0.6)),
        line(sg((12, 11), (12, 7.5))),
        line(sg((12, 7.5), (9, 3.3))),
        line(sg((12, 7.5), (14.6, 5.6))),
        dot(bx, by, 1.5),
    ]


@icon("pinking-shears", CAT, "Open scissors whose blades have zigzag teeth for cutting fabric edges.",
      tags=["scissors", "zigzag", "sewing", "tailor", "fabric", "cut", "dressmaking"])
def _(S):
    piv = (12, 10.5)
    parts = []
    for side in (-1, 1):
        c = (12 + side * 4.25, 17.5)
        ux, uy = piv[0] - c[0], piv[1] - c[1]
        L = math.hypot(ux, uy)
        ux, uy = ux / L, uy / L
        start = (c[0] + ux * 2.5, c[1] + uy * 2.5)
        mid = (piv[0] + ux * 3.4, piv[1] + uy * 3.4)
        tip = (piv[0] + ux * 9, piv[1] + uy * 9)
        parts += [shell(circle(*c, 2.5)), line(poly([start, mid])), line(poly(_zig(mid, tip, 2, 0.95)))]
    return parts


@icon("thread-snips", CAT, "Small spring-loaded snips: two short crossing blades joined by a U shaped spring bow.",
      tags=["scissors", "thread cutter", "embroidery", "sewing", "trim", "snip", "clipper"])
def _(S):
    return [
        line(poly([(5, 3), (15.5, 16.5)])),
        line(poly([(19, 3), (8.5, 16.5)])),
        line("M8.5 16.5A3.5 3.5 0 0 0 15.5 16.5"),
    ]


@icon("tailors-chalk", CAT, "Flat triangular tailor's chalk with a dashed chalk line marked below it.",
      tags=["marking", "fabric", "sewing", "pattern", "tailor", "draw", "mark"])
def _(S):
    return [
        shell(poly([(3, 10.5), (12, 3), (15.5, 13)], closed=True, r=S.r)),
        line(seg(3.5, 19.5, 9, 19.5)),
        line(seg(12.5, 19.5, 20.5, 19.5)),
    ]


@icon("needle-threader", CAT, "Small coin-shaped handle holding a thin wire diamond loop for threading needles.",
      tags=["needle", "thread", "sewing", "tool", "wire loop", "eye", "helper"])
def _(S):
    handle = poly(regular(12, 17, 4.6, 8, start=-22.5), closed=True) if S.name == "line" else circle(12, 17, 4.6)
    return [
        shell(handle),
        dot(12, 17, 1.2),
        line(poly([(12, 12.4), (12, 10), (8.8, 6.3), (12, 2.5), (15.2, 6.3), (12, 10)], r=S.r * 0.4)),
    ]


@icon("dress-form", CAT, "Headless torso mannequin on a tall pole with tripod feet.",
      tags=["mannequin", "tailor", "dressmaking", "sewing", "fitting", "torso", "seamstress"])
def _(S):
    torso = poly([(9.5, 3), (14.5, 3), (18, 6), (16.5, 10.5), (18, 15), (6, 15), (7.5, 10.5), (6, 6)], closed=True, r=S.r)
    return [
        shell(torso),
        line(seg(12, 15, 12, 19)),
        line(poly([(7.5, 21.5), (12, 18.5), (16.5, 21.5)])),
    ]


# ============================================================================ chunk 3: forms, yarn and weaving

def _rot(pts, deg=45, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s_ = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s_, cy + (x - cx) * s_ + (y - cy) * c) for x, y in pts]


def _rseg(a, b, deg=45):
    (x1, y1), (x2, y2) = _rot([a, b], deg)
    return seg(x1, y1, x2, y2)


def _rot_path(cmds, deg=45):
    """Path from ("M"|"L", p), ("A", r, large, sweep, p), ("Q", c, p), ("C", c1, c2, p), ("Z",) with rotated points."""
    def pt(p):
        q = _rot([p], deg)[0]
        return f"{fmt(q[0])} {fmt(q[1])}"
    out = []
    for c in cmds:
        if c[0] in ("M", "L"):
            out.append(c[0] + pt(c[1]))
        elif c[0] == "A":
            out.append(f"A{fmt(c[1])} {fmt(c[1])} 0 {c[2]} {c[3]} {pt(c[4])}")
        elif c[0] == "Q":
            out.append("Q" + pt(c[1]) + " " + pt(c[2]))
        elif c[0] == "C":
            out.append("C" + pt(c[1]) + " " + pt(c[2]) + " " + pt(c[3]))
        else:
            out.append("Z")
    return "".join(out)


@icon("mannequin", CAT, "Full-body shop display figure with a smooth round head and arms, standing on a base plate.",
      tags=["shop dummy", "display", "retail", "store window", "clothing", "dummy", "fashion"])
def _(S):
    torso = poly([(8.5, 9), (15.5, 9), (14.5, 12), (15.5, 15), (8.5, 15), (9.5, 12)], closed=True, r=S.r * 0.7)
    return [
        shell(circle(12, 5, 1.8)),
        shell(torso),
        line(seg(8.5, 10, 5.8, 15.5)),
        line(seg(15.5, 10, 18.2, 15.5)),
        line(seg(10, 15, 10, 20.5)),
        line(seg(14, 15, 14, 20.5)),
        line(seg(6.5, 21, 17.5, 21)),
    ]


@icon("sewing-pattern", CAT, "Paper pattern piece with a double-headed grain line arrow.",
      tags=["dressmaking", "template", "paper pattern", "sewing", "tailor", "cutting", "garment"])
def _(S):
    outline = "M4 3H13.5Q13.5 9.5 20 10.5V21H4Z"
    return [
        shell(outline),
        detail("M10 8V17"),
        detail(poly([(8.3, 9.8), (10, 8), (11.7, 9.8)])),
        detail(poly([(8.3, 15.2), (10, 17), (11.7, 15.2)])),
    ]


@icon("knitting-needles", CAT, "Two crossed knitting needles with round end knobs.",
      tags=["knit", "yarn", "wool", "needles", "craft", "stitch", "hobby"])
def _(S):
    return [
        line(seg(3.5, 20.5, 17, 7)),
        line(seg(20.5, 20.5, 7, 7)),
        shell(circle(18.6, 5.4, 2.0)),
        shell(circle(5.4, 5.4, 2.0)),
    ]


@icon("yarn-ball", CAT, "Round ball of yarn with diagonal wraps and a loose tail.",
      tags=["wool", "knitting", "crochet", "thread", "craft", "skein", "string"])
def _(S):
    return [
        shell(circle(11, 11, 8.3)),
        detail("M4.6 9Q10 10.5 13 16"),
        detail("M8 4.2Q13.5 6.5 16.5 12"),
        line("M14.5 17.5Q19.5 19.5 21 15.5"),
    ]


@icon("yarn-skein", CAT, "Twisted hank of yarn with a paper band wrapped around the middle.",
      tags=["wool", "hank", "knitting", "crochet", "yarn", "craft", "fiber"])
def _(S):
    top = rect(6, 3, 12, 18, 6 if S.name == "rounded" else 4)
    band = rect(4.5, 9, 15, 6, 0)
    return [
        shell(_union_d(top, band)),
        detail("M9.5 5.6L14.5 7.4"),
        detail("M9.5 18.4L14.5 16.6"),
    ]


@icon("crochet-hook", CAT, "Crochet hook with a thumb rest and a small hooked tip.",
      tags=["crochet", "yarn", "hook", "craft", "amigurumi", "needlework", "handmade"])
def _(S):
    return [
        line(_rseg((12, 9), (12, 21.5))),
        line(_rot_path([("M", (12, 9)), ("L", (12, 5)), ("A", 1.8, 0, 1, (15.4, 3.6))])),
        shell(poly(_rot([(10.3, 12), (13.7, 12), (13.7, 16.5), (10.3, 16.5)], 45), closed=True, r=S.r * 0.6)),
    ]


@icon("granny-square", CAT, "Crochet granny square made of concentric rings of stitches around a small centre.",
      tags=["crochet", "motif", "blanket", "afghan", "yarn", "craft", "patchwork"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(rect(7.5, 7.5, 9, 9, 1 if S.name == "rounded" else 0)),
        dot(12, 12, 1.4),
        detail(seg(4.5, 4.5, 6.5, 6.5)),
        detail(seg(19.5, 4.5, 17.5, 6.5)),
        detail(seg(4.5, 19.5, 6.5, 17.5)),
        detail(seg(19.5, 19.5, 17.5, 17.5)),
    ]


@icon("embroidery-hoop", CAT, "Round embroidery hoop with a screw tab at the top holding fabric stitched with a small flower.",
      tags=["cross stitch", "needlework", "sewing", "frame", "thread", "craft", "handmade"])
def _(S):
    pr = 1.3 if S.name == "line" else 1.45
    petals = [dot(*polar(12, 14, 2.7, a), pr) for a in (-90, -18, 54, 126, 198)]
    return [
        shell(circle(12, 14, 8)),
        shell(rect(9.5, 2.5, 5, 3.5, 1.2 if S.name == "rounded" else 0)),
        *petals,
    ]


@icon("weaving-loom", CAT, "Frame loom with vertical warp threads and two woven rows of weft across the lower half.",
      tags=["weave", "warp", "weft", "textile", "tapestry", "craft", "fibre art"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(8, 5, 8, 19)),
        detail(seg(12, 5, 12, 19)),
        detail(seg(16, 5, 16, 19)),
        detail("M5 11Q6.5 9.5 8 11T12 11T16 11T19 11"),
        detail("M5 16Q6.5 17.5 8 16T12 16T16 16T19 16"),
    ]


@icon("weaving-shuttle", CAT, "Boat shaped weaving shuttle with pointed ends and a slot holding a bobbin of yarn, a strand trailing off.",
      tags=["loom", "weft", "weave", "textile", "craft", "yarn", "wooden"])
def _(S):
    deg = -35
    body = _rot_path([("M", (2, 12)), ("Q", (8, 6), (12, 6.5)), ("Q", (16, 6), (22, 12)), ("Q", (16, 18), (12, 17.5)), ("Q", (8, 18), (2, 12)), ("Z",)], deg)
    slot = poly(_rot([(9, 10.5), (15, 10.5), (15, 13.5), (9, 13.5)], deg), closed=True)
    return [shell(body), detail(slot)]


@icon("spinning-wheel", CAT, "Spinning wheel with a spoked wheel on a stand and an upright post holding the spindle.",
      tags=["spin", "yarn", "wool", "fibre", "treadle", "craft", "traditional"])
def _(S):
    cx, cy, r = 8.5, 11.5, 6
    spokes = [detail(f"M{fmt(polar(cx, cy, 2.6, a)[0])} {fmt(polar(cx, cy, 2.6, a)[1])}L{fmt(polar(cx, cy, 5.2, a)[0])} {fmt(polar(cx, cy, 5.2, a)[1])}") for a in (0, 90, 180, 270)]
    return [
        shell(circle(cx, cy, r)),
        *spokes,
        dot(cx, cy, 1.3),
        line(seg(14.5, 11.5, 21, 11.5)),
        line(seg(19.5, 11.5, 19.5, 21)),
        line(seg(17.5, 7, 21.5, 7)),
        line(seg(19.5, 7, 19.5, 11.5)),
        line(seg(8.5, 17.5, 8.5, 21)),
        line(seg(5, 21, 21.5, 21)),
    ]


@icon("drop-spindle", CAT, "Hand spindle with a top hook, yarn wound on the shaft and a round whorl disc near the bottom.",
      tags=["spin", "yarn", "wool", "fibre", "handspinning", "craft", "whorl"])
def _(S):
    return [
        line("M12 5V3.6Q12 2.6 13.6 2.6"),
        shell(ellipse(12, 8.6, 3.8, 3.5)),
        detail("M9.6 8.6Q12 10 14.4 8.6"),
        shell(ellipse(12, 17.5, 7, 2)),
        line(seg(12, 19.8, 12, 21.8)),
    ]


@icon("sewn-patch", CAT, "Square embroidered badge patch with a dashed stitched border and a star in the middle.",
      tags=["badge", "embroidery", "iron-on", "emblem", "merit", "sew", "applique"])
def _(S):
    star = poly([polar(12, 12, 3.4 if i % 2 == 0 else 1.5, -90 + i * 36) for i in range(10)], closed=True)
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(8, 6.6, 11, 6.6)), detail(seg(13, 6.6, 16, 6.6)),
        detail(seg(8, 17.4, 11, 17.4)), detail(seg(13, 17.4, 16, 17.4)),
        detail(seg(6.6, 8, 6.6, 11)), detail(seg(6.6, 13, 6.6, 16)),
        detail(seg(17.4, 8, 17.4, 11)), detail(seg(17.4, 13, 17.4, 16)),
        solid(star),
    ]


@icon("sewing-pin", CAT, "Straight pin with a round ball head.",
      tags=["pin", "straight pin", "dressmaking", "tailor", "needle", "pinning", "sewing"])
def _(S):
    return [
        shell(circle(17.5, 6.5, 3)),
        line(seg(15.3, 8.7, 4, 20)),
    ]


@icon("hook-and-eye", CAT, "Small metal hook fastener with its flat plate, beside the matching loop eye and plate.",
      tags=["fastener", "clasp", "closure", "bra hook", "sewing", "haberdashery", "dress"])
def _(S):
    rr = min(S.R, 1.5)
    return [
        shell(rect(2.5, 8, 4, 8, rr)),
        line("M6.5 10H11A2 2 0 0 1 11 14H9.5"),
        shell(rect(17.5, 8, 4, 8, rr)),
        line("M17.5 9.5H15.5A2.5 2.5 0 0 0 15.5 14.5H17.5"),
    ]


# ============================================================================ chunk 4: fasteners, trims, labels and cutting tools

@icon("snap-fastener", CAT, "Two part press stud shown apart: one half with a round knob, the other with a socket ring.",
      tags=["press stud", "popper", "snap button", "closure", "sewing", "haberdashery", "fastener"], aliases=["press-stud"])
def _(S):
    def disc(cx):
        return poly(regular(cx, 12, 4.2, 8, start=-22.5), closed=True) if S.name == "line" else circle(cx, 12, 4.2)
    return [
        shell(disc(6.2)),
        dot(6.2, 12, 1.7),
        shell(disc(17.8)),
        detail(circle(17.8, 12, 1.2)),
    ]


@icon("hook-and-loop-fastener", CAT, "Two strips pulled apart, the upper with tiny hooks and the lower with fuzzy loops.",
      tags=["velcro", "touch fastener", "strap", "closure", "shoe", "sticky strip", "fastener"], aliases=["touch-fastener"])
def _(S):
    rr = min(S.R, 1)
    parts = [shell(rect(3, 3, 18, 4.5, rr)), shell(rect(3, 16.5, 18, 4.5, rr))]
    for x in (6.5, 12, 17.5):
        parts.append(line(f"M{fmt(x)} 7.5V10.5Q{fmt(x)} 11.8 {fmt(x + 1.4)} 11.8"))
        parts.append(line(f"M{fmt(x - 2)} 16.5A2 2 0 0 1 {fmt(x + 2)} 16.5"))
    return parts


@icon("toggle-fastener", CAT, "Wooden toggle peg with a sewn cord band, beside the cord loop it slides through.",
      tags=["toggle", "duffle coat", "peg", "button", "closure", "rope loop", "fastener"])
def _(S):
    return [
        shell(rect(3, 4.5, 6, 15, 3 if S.name == "rounded" else 2)),
        detail(seg(3.5, 12, 8.5, 12)),
        line("M21.5 8.5H16.5A3.5 3.5 0 0 0 16.5 15.5H21.5"),
    ]


@icon("eyelet", CAT, "Round metal grommet ring set into a square of fabric.",
      tags=["grommet", "hole", "lace hole", "rivet", "fabric", "sewing", "banner"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(circle(12, 12, 5.2)),
        detail(circle(12, 12, 1.6) if S.name == "rounded" else rect(10.6, 10.6, 2.8, 2.8, 0)),
    ]


@icon("ribbon-spool", CAT, "Roll of ribbon around a centre tube, with a loose end with a swallowtail cut hanging down the side.",
      tags=["ribbon", "spool", "gift wrap", "trim", "craft", "satin", "roll"])
def _(S):
    tail = poly([(14.5, 12), (21.5, 12), (21.5, 21.5), (18, 19), (14.5, 21.5)], closed=True)
    return [
        shell(_union_d(circle(10.5, 10.5, 7.5), tail)),
        detail(circle(10.5, 10.5, 2.5)),
    ]


@icon("sequins", CAT, "Cluster of three overlapping round shiny discs, each with a centre hole.",
      tags=["spangles", "paillettes", "sparkle", "glitter", "costume", "sewing", "embellishment"])
def _(S):
    r = 4.4 + (0.2 if S.name == "rounded" else 0)
    cs = [(8, 8), (16.2, 9.5), (11, 16.5)]
    return [shell(_union_d(*[circle(x, y, r) for x, y in cs]))] + [dot(x, y, 1.1) for x, y in cs]


@icon("lace-trim", CAT, "Strip of lace with a scalloped lower edge and a row of small holes.",
      tags=["lace", "trim", "edging", "doily", "wedding", "sewing", "ribbon"])
def _(S):
    d = "M3 6H21V15" + "".join(f"A2.25 2.25 0 0 1 {fmt(21 - 4.5 * (i + 1))} 15" for i in range(4)) + "Z"
    return [shell(d)] + [dot(x, 10.3, 1.2) for x in (7.5, 12, 16.5)]


@icon("tassel", CAT, "Hanging tassel with a top loop, a gathered neck band and a fan of loose threads.",
      tags=["fringe", "decoration", "curtain", "bookmark", "cord", "trim", "graduation"])
def _(S):
    return [
        line("M9.5 10V5A2.5 2.5 0 0 1 14.5 5V10"),
        shell(rect(8.5, 10, 7, 3.4, min(S.R, 1.2))),
        line(seg(9.8, 13.4, 6.8, 21)),
        line(seg(11.4, 13.4, 10.2, 21)),
        line(seg(12.6, 13.4, 13.8, 21)),
        line(seg(14.2, 13.4, 17.2, 21)),
    ]


@icon("clothing-label", CAT, "Sewn-in garment label with folded stitched ends and a care symbol in the middle.",
      tags=["tag", "care label", "washing instructions", "garment", "brand label", "sewing", "wash"])
def _(S):
    return [
        shell(rect(3, 6, 18, 12, S.R)),
        detail(seg(7, 8, 7, 16)),
        detail(seg(17, 8, 17, 16)),
        detail(poly([(12, 9.6), (14.6, 14.2), (9.4, 14.2)], closed=True, r=S.r * 0.4)),
    ]


@icon("clothing-size", CAT, "Swing tag on a string loop with a large letter M for the garment size.",
      tags=["size tag", "price tag", "medium", "swing tag", "hang tag", "apparel", "label"])
def _(S):
    tag = poly([(9, 6), (15, 6), (18, 9), (18, 21), (6, 21), (6, 9)], closed=True, r=S.r)
    return [
        shell(tag),
        detail(poly([(9, 18), (9, 13), (12, 16.5), (15, 13), (15, 18)])),
        dot(12, 9, 1.0),
        line("M12 9V7.5Q12 3 15.5 3Q19.5 3 19.5 6.5"),
    ]


@icon("clothing-security-tag", CAT, "Round plastic anti-theft tag clamped with a pin through the edge of a garment.",
      tags=["anti-theft", "retail", "shop", "alarm tag", "shoplifting", "store", "security"])
def _(S):
    return [
        shell(circle(8, 12, 4.8)),
        dot(8, 12, 1.6),
        shell(rect(16, 6, 3, 12, 0)),
        line(seg(12.8, 12, 20.4, 12)),
        dot(20.4, 12, 1.3),
    ]


@icon("tracing-wheel", CAT, "Tilted handle with a small spiked wheel that rolls a dotted line onto fabric.",
      tags=["pattern transfer", "sewing", "dotted line", "dressmaking", "tailor", "marking", "perforate"])
def _(S):
    deg = 45
    wheel = _rot([polar(12, 15.8, 4.6 if i % 2 == 0 else 3.3, -90 + i * 30) for i in range(12)], deg)
    grip = _rot([(9, 1.5), (15, 1.5), (14, 10), (10, 10)], deg)
    return [
        shell(poly(grip, closed=True, r=S.r * 0.6)),
        line(_rseg((12, 10), (12, 12.4), deg)),
        shell(poly(wheel, closed=True, r=S.r * 0.25)),
        dot(14.5, 20.5, 1.1),
        dot(17.5, 20.5, 1.1),
        dot(20.5, 20.5, 1.1),
    ]


@icon("rotary-cutter", CAT, "Fabric rotary cutter: a grip handle with a small round blade at the end.",
      tags=["cutter", "quilting", "fabric", "sewing", "blade", "craft", "pizza cutter"])
def _(S):
    deg = 30
    grip = poly(_rot([(9.5, 2.5), (14.5, 2.5), (14.5, 12), (9.5, 12)], deg), closed=True, r=S.r * 0.8)
    bx, by = _rot([(12, 17)], deg)[0]
    return [
        shell(grip),
        shell(circle(bx, by, 3.7)),
        dot(bx, by, 1.0),
    ]


@icon("fabric-swatch", CAT, "Two fabric samples stacked with zigzag pinked top edges.",
      tags=["sample", "textile", "cloth", "material", "pinked edge", "sewing", "swatches"])
def _(S):
    front = [(3, 21)] + _zig((3, 10), (15, 10), 3, 1.1) + [(15, 21)]
    back = [(6, 8)] + _zig((6, 4.6), (21, 4.6), 3, 1.1) + [(21, 16.5), (18, 16.5)]
    return [
        shell(poly(front, closed=True)),
        line(poly(back)),
    ]


@icon("leather-hide", CAT, "Flat animal hide outline with four leg points, a neck and a tail, with stitch marks.",
      tags=["skin", "cowhide", "leatherwork", "pelt", "tanning", "craft", "animal hide"])
def _(S):
    pts = [(9, 3), (15, 3), (15.5, 7), (20.5, 6), (19.5, 11.5), (16.5, 12.5), (20, 20.5), (15, 18.5), (12, 21), (9, 18.5), (4, 20.5),
           (7.5, 12.5), (4.5, 11.5), (3.5, 6), (8.5, 7)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.7)),
        detail(seg(12, 8, 12, 10)),
        detail(seg(12, 13, 12, 15)),
    ]


# ============================================================================ chunk 5: fabric patterns

def _swatch(S):
    return shell(rect(3, 3, 18, 18, S.R))


def _blob(d):
    """Solid pattern mark: black in Line/Rounded, knocked out of the swatch in Filled."""
    return Part("dot", d)


@icon("knit-fabric", CAT, "Square swatch of knitted fabric showing rows of V shaped stitches.",
      tags=["knitting", "stockinette", "wool", "jersey", "sweater", "textile", "stitches"])
def _(S):
    parts = [_swatch(S)]
    for y in (7.4, 12.2, 17):
        for x in (8.5, 15.5):
            parts.append(detail(poly([(x - 2, y - 1.3), (x, y + 1.3), (x + 2, y - 1.3)])))
    return parts


@icon("plaid-fabric", CAT, "Square swatch with crossing horizontal and vertical bands of different widths.",
      tags=["tartan", "check", "flannel", "checkered", "pattern", "textile", "scottish"])
def _(S):
    return [
        _swatch(S),
        _blob(rect(6.5, 4.5, 4, 15, 0)),
        _blob(rect(4.5, 6.5, 15, 4, 0)),
        detail(seg(15.5, 5, 15.5, 19)),
        detail(seg(5, 15.5, 19, 15.5)),
    ]


@icon("polka-dot-fabric", CAT, "Square swatch covered in evenly spaced round dots in offset rows.",
      tags=["spots", "dotted", "retro", "pattern", "textile", "print", "dots"])
def _(S):
    pts = [(7.5, 7), (12, 7), (16.5, 7), (9.75, 12), (14.25, 12), (7.5, 17), (12, 17), (16.5, 17)]
    return [_swatch(S)] + [dot(x, y, 1.3) for x, y in pts]


@icon("pinstripe-fabric", CAT, "Square swatch with thin evenly spaced vertical lines.",
      tags=["stripes", "suit", "tailoring", "vertical lines", "pattern", "textile", "banker"])
def _(S):
    return [_swatch(S)] + [detail(seg(x, 5.5, x, 18.5)) for x in (7, 10.3, 13.7, 17)]


@icon("gingham-fabric", CAT, "Square swatch with an even checkerboard of shaded and blank squares.",
      tags=["checkered", "checks", "picnic", "tablecloth", "pattern", "textile", "squares"])
def _(S):
    parts = [_swatch(S)]
    for i in range(4):
        for j in range(4):
            if (i + j) % 2 == 0:
                parts.append(_blob(rect(4.5 + 4 * i - 0.5, 4.5 + 4 * j - 0.5, 4, 4, 0)))
    return parts


@icon("herringbone-fabric", CAT, "Square swatch with columns of short slanted lines forming a zigzag weave.",
      tags=["tweed", "weave", "zigzag", "suit", "pattern", "textile", "twill"])
def _(S):
    parts = [_swatch(S)]
    for c, x0 in enumerate((5.6, 10.2, 14.8)):
        ys = (7, 11.5, 16) if c != 1 else (9.3, 13.8)
        for y in ys:
            if c % 2 == 0:
                parts.append(detail(seg(x0, y + 1.5, x0 + 3.6, y - 1.5)))
            else:
                parts.append(detail(seg(x0, y - 1.5, x0 + 3.6, y + 1.5)))
    return parts


@icon("argyle-fabric", CAT, "Square swatch with a large diamond crossed by thin diagonal lines, like an argyle sock.",
      tags=["diamond", "sweater", "golf", "socks", "pattern", "textile", "lattice"])
def _(S):
    return [
        _swatch(S),
        detail(poly([(12, 6), (18, 12), (12, 18), (6, 12)], closed=True)),
        detail(seg(5.6, 5.6, 18.4, 18.4)),
        detail(seg(18.4, 5.6, 5.6, 18.4)),
    ]


@icon("paisley-fabric", CAT, "Square swatch with a teardrop paisley motif whose tail curls over.",
      tags=["boteh", "teardrop", "bandana", "pattern", "textile", "print", "indian"])
def _(S):
    return [
        _swatch(S),
        detail("M18 6.6C11 6 6.2 9.6 6.2 14.6C6.2 17.4 8.3 18.8 10.7 18.8C13.6 18.8 15.4 16.6 15 14.5C14.8 12.8 13.2 12 12.2 13"),
        dot(9.8, 15.3, 1.1),
    ]


@icon("chevron-fabric", CAT, "Square swatch with stacked V shaped zigzag stripes.",
      tags=["zigzag", "stripes", "v pattern", "pattern", "textile", "print", "arrows"])
def _(S):
    return [_swatch(S)] + [detail(poly([(5.5, y - 1.8), (12, y + 1.8), (18.5, y - 1.8)])) for y in (7.3, 12.3, 17.3)]


@icon("camouflage-fabric", CAT, "Swatch covered in irregular interlocking blob shapes like military camouflage.",
      tags=["camo", "army", "military", "hunting", "pattern", "textile", "woodland"])
def _(S):
    return [
        _swatch(S),
        _blob("M5.5 7C5.5 5.6 7 5.3 8.6 5.6C10.3 6 11.3 7.3 10.6 8.7C9.8 10.3 7.6 10.5 6.4 9.6C5.8 9.1 5.5 8.2 5.5 7Z"),
        _blob("M13.3 5.6C15.3 4.9 18.4 5.7 18.5 7.7C18.5 9.6 16.4 10.6 14.8 9.6C13.4 8.8 12.6 6.2 13.3 5.6Z"),
        _blob("M5.5 14.4C7 12.4 10 12.8 11.6 14.4C13 15.8 12.4 18 10.4 18.6C8 19.2 5.6 18 5.3 16.5C5.2 15.8 5.3 15 5.5 14.4Z"),
        _blob("M14.3 12.2C16.5 11.7 18.8 13.2 18.6 15.4C18.4 17.4 16.2 18.6 14.6 17.6C13.2 16.8 12.6 12.8 14.3 12.2Z"),
    ]


@icon("leopard-print", CAT, "Swatch covered in irregular open-centred rosette spots like a leopard coat.",
      tags=["animal print", "rosettes", "spots", "cheetah", "pattern", "textile", "safari"])
def _(S):
    return [
        _swatch(S),
        detail(arc(8.4, 8.4, 2.5, 40, 320)),
        detail(arc(16.2, 11, 2.5, 220, 140)),
        detail(arc(9.6, 16.6, 2.5, 120, 40)),
        dot(16.5, 17.3, 1.0),
        dot(15.6, 5.8, 0.9),
    ]


@icon("zebra-print", CAT, "Swatch covered in bold curved stripes that taper to points, like zebra hide.",
      tags=["animal print", "stripes", "black and white", "safari", "pattern", "textile", "wild"])
def _(S):
    def stripe(x, lean=5.0):
        return (f"M{fmt(x)} 4.8C{fmt(x + lean)} 9.5 {fmt(x + lean)} 14.5 {fmt(x)} 19.2"
                f"C{fmt(x + lean * 0.16)} 14.5 {fmt(x + lean * 0.16)} 9.5 {fmt(x)} 4.8Z")
    return [_swatch(S), _blob(stripe(5)), _blob(stripe(9.8)), _blob(stripe(14.6))]


# ============================================================================ chunk 6: places, outfits and garments

@icon("fitting-room", CAT, "Changing booth with a half drawn curtain on a rail and a clothes hanger beside it.",
      tags=["changing room", "try on", "store", "boutique", "curtain", "shopping", "dressing room"])
def _(S):
    return [
        line(seg(2.5, 4, 21.5, 4)),
        shell("M3.5 4H12Q13.2 9 11.6 14Q10.6 18 12 21H3.5Z"),
        detail("M7.5 7V18"),
        line("M17.5 12.4V11.2A1.6 1.6 0 1 0 15.9 9.6"),
        line(poly([(17.5, 12.4), (14, 18), (21, 18), (17.5, 12.4)], r=S.r * 0.3)),
    ]


@icon("clothes-rack", CAT, "Garment rail with two shirts hanging from it, standing on two wheels.",
      tags=["garment rack", "rail", "wardrobe", "boutique", "retail", "clothing store", "hanging"])
def _(S):
    def shirt(cx, top):
        return shell(poly([(cx - 1.2, top), (cx - 3, top + 1.8), (cx - 2.4, top + 3.8), (cx - 1.7, top + 3.4), (cx - 1.7, top + 8.5),
                           (cx + 1.7, top + 8.5), (cx + 1.7, top + 3.4), (cx + 2.4, top + 3.8), (cx + 3, top + 1.8), (cx + 1.2, top)],
                          closed=True, r=S.r * 0.3))
    return [
        line(seg(3, 4, 21, 4)),
        line(seg(3, 4, 3, 19)),
        line(seg(21, 4, 21, 19)),
        shirt(8.5, 6.5), shirt(15.5, 6.5),
        dot(3, 20.6, 1.3), dot(21, 20.6, 1.3),
    ]


@icon("outfit", CAT, "Flat lay of a shirt above a pair of trousers with a pair of shoes below.",
      tags=["look", "clothes", "coordinated", "wardrobe", "fashion", "style", "ootd"])
def _(S):
    k = S.r * 0.4
    shirt = [(9.3, 2.5), (14.7, 2.5), (19, 5), (17.4, 7), (15.5, 6.2), (15.5, 8.3), (8.5, 8.3), (8.5, 6.2), (6.6, 7), (5, 5)]
    pants = [(8, 11.3), (16, 11.3), (16.6, 17.6), (13, 17.6), (12, 14), (11, 17.6), (7.4, 17.6)]
    return [
        shell(poly(shirt, closed=True, r=k)),
        shell(poly(pants, closed=True, r=k)),
        solid(ellipse(8.6, 21, 2.3, 1.0)),
        solid(ellipse(15.4, 21, 2.3, 1.0)),
    ]


@icon("catwalk", CAT, "Long runway in perspective with a model standing at the far end and two spotlight beams.",
      tags=["runway", "fashion show", "model", "stage", "designer", "show", "spotlight"])
def _(S):
    return [
        shell(poly([(9.5, 9.5), (14.5, 9.5), (21, 21), (3, 21)], closed=True, r=S.r * 0.3)),
        detail(seg(12, 12.6, 12, 14)),
        detail(seg(12, 16.4, 12, 18)),
        dot(12, 3.4, 1.4),
        line(seg(12, 5.6, 12, 9.5)),
        line(seg(3.5, 3.5, 7.2, 7.5)),
        line(seg(20.5, 3.5, 16.8, 7.5)),
    ]


@icon("tuxedo", CAT, "Dinner jacket with a V shaped white shirt front, satin lapels and a black bow tie.",
      tags=["dinner jacket", "formal", "black tie", "wedding", "suit", "groom", "gala"])
def _(S):
    jacket = poly([(7, 3), (17, 3), (21, 7), (20, 21), (4, 21), (3, 7)], closed=True, r=S.r * 0.6)
    bow = "M9.6 5.1L12 6.6L14.4 5.1V8.1L12 6.6L9.6 8.1Z"
    return [
        shell(jacket),
        detail(poly([(7, 3.4), (12, 13.5), (17, 3.4)])),
        detail(seg(12, 13.5, 12, 20)),
        _blob(bow),
    ]


@icon("sports-bra", CAT, "Racerback sports bra top with narrow straps and a thick elastic band under the chest.",
      tags=["bra", "activewear", "workout", "gym", "yoga", "fitness", "athletic"])
def _(S):
    top = poly([(5.5, 3), (8.5, 3), (12, 8.3), (15.5, 3), (18.5, 3), (19.5, 10), (19, 16.5), (5, 16.5), (4.5, 10)], closed=True, r=S.r * 0.6)
    return [
        shell(top),
        detail(seg(5.3, 12.3, 18.7, 12.3)),
    ]


@icon("locket", CAT, "Heart shaped locket opened like a book on a fine chain.",
      tags=["pendant", "necklace", "jewelry", "heart", "keepsake", "photo", "gift"])
def _(S):
    left = "M11.2 10C11.2 8.2 9.6 7.2 7.8 7.6C5.6 8.2 5 10.8 6.6 13.3L11.2 19.4Z"
    right = "M12.8 10C12.8 8.2 14.4 7.2 16.2 7.6C18.4 8.2 19 10.8 17.4 13.3L12.8 19.4Z"
    return [
        line(seg(4, 2.8, 11.2, 7.2)),
        line(seg(20, 2.8, 12.8, 7.2)),
        shell(left),
        shell(right),
        dot(8.7, 12.4, 0.0 + 0.9),
    ]


@icon("snowsuit", CAT, "Child's one piece puffy snowsuit with a hood, a quilted chest band and cuffed sleeves.",
      tags=["snow suit", "winter", "kids", "toddler", "onesie", "ski", "cold weather"])
def _(S):
    body = poly([(9, 8.5), (15, 8.5), (20.5, 11.5), (19.5, 17), (16.5, 16.5), (16, 21.5), (12.8, 21.5), (12, 17.5), (11.2, 21.5), (8, 21.5),
                 (7.5, 16.5), (4.5, 17), (3.5, 11.5)], closed=True, r=S.r * 0.7)
    return [
        shell(_union_d(body, circle(12, 5.3, 3.1))),
        detail(seg(8.6, 12.6, 15.4, 12.6)),
        detail(seg(4.2, 14.8, 7.4, 15.3)),
        detail(seg(19.8, 14.8, 16.6, 15.3)),
    ]
