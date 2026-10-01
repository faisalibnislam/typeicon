"""TypeIcon Core: crafts (batch crafts_004): fibre and textile tools, beading and jewellery making,
candle and soap making, dried flowers, leather work, printmaking, camera gear and hobby builds.

Objects are drawn front-on or from the side. Long hand tools are drawn upright and turned 45 degrees
clockwise so the handle points to the bottom-left. Running stitches are dashes whose length is corrected for
the cap style, so Line and Rounded show the same rhythm of stitches.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path.parser import parse_path
from geometry import SCALE, D, P, ST, U, fmt, path_to_d, rotation

CAT = "crafts"
TILT = 45


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    """Container corner radius: small in Line, full in Rounded (capped for small shapes)."""
    if cap is None:
        return S.R
    return min(1.0, cap / 2) if S.name == "line" else cap


def tf(d, m):
    """Apply an affine matrix (a, b, c, d, e, f) to a d-string, keeping open paths open."""
    pen = SVGPathPen(None, ntos=fmt)
    parse_path(d, TransformPen(pen, m))
    return pen.getCommands()


def rot(d, deg=TILT, cx=12.0, cy=12.0):
    """Rotate a d-string clockwise on screen about (cx, cy)."""
    return tf(d, rotation(deg, cx, cy))


def mv(d, dx, dy):
    return tf(d, (1, 0, 0, 1, dx, dy))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def grow(d, g):
    """Region d expanded by g px (cuts a clean gap where one part passes behind another)."""
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def band(d, w=2.0):
    """Outline of a 2 px (or w px) stroke along d, as a closed region."""
    return path_to_d(ST(d, w, "butt", "miter"))


def hole(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def fit(parts, cx=12.0, cy=12.0):
    """Translate parts so their drawn bounds are centred on (cx, cy), snapped to half pixels."""
    regions = []
    for p in parts:
        regions.append(P(p.d) if p.kind in ("shell", "dot", "solid") else ST(p.d, 2.0))
    x0, y0, x1, y1 = U(*regions).bounds
    dx = round((cx - (x0 + x1) / 2 / SCALE) * 2) / 2
    dy = round((cy - (y0 + y1) / 2 / SCALE) * 2) / 2
    if dx == 0 and dy == 0:
        return parts
    return [Part(p.kind, mv(p.d, dx, dy), p.attrs) for p in parts]


def tilt(parts, deg=TILT, centre=True):
    """Turn an upright design (handle down) clockwise, then centre it."""
    out = [Part(p.kind, rot(p.d, deg), p.attrs) for p in parts]
    return fit(out) if centre else out


def dash(S, x1, y1, x2, y2):
    """A running-stitch dash: Rounded shortens it by its round caps so both styles show the same length."""
    if S.name == "rounded":
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy)
        k = min(0.95, 1.0 / ln) if ln else 0
        x1, y1, x2, y2 = x1 + dx * k * 0.5, y1 + dy * k * 0.5, x2 - dx * k * 0.5, y2 - dy * k * 0.5
    return seg(x1, y1, x2, y2)


def dash_arc(S, cx, cy, r, a0, a1):
    """Arc dash (clockwise from a0 to a1 degrees), shortened for round caps in Rounded."""
    if S.name == "rounded":
        k = math.degrees(0.9 / r)
        a0, a1 = a0 + k, a1 - k
    return arc(cx, cy, r, a0, a1)


def spool(cx, cy, w=5.0, h=6.0, S=None):
    """Tiny thread spool mark (two flanges and a thread body) as one solid outline."""
    f = 1.4
    body = rect(cx - w / 2 + 0.9, cy - h / 2 + f - 0.2, w - 1.8, h - 2 * f + 0.4)
    top = rect(cx - w / 2, cy - h / 2, w, f, 0.4 if S and S.name == "rounded" else 0)
    bot = rect(cx - w / 2, cy + h / 2 - f, w, f, 0.4 if S and S.name == "rounded" else 0)
    return union(top, body, bot)


# ============================================================================ needlework and fibre

@icon("french-knot", CAT, "Embroidery needle touching a round thread knot sitting on a strip of fabric",
      tags=["embroidery", "knot stitch", "needlework", "hand stitch", "sewing", "stitch"])
def _(S):
    base = rect(3, 16.5, 18, 4.5, rr(S, 2.25))
    return [
        shell(base),
        shell(circle(10, 11.5, 3.5)),
        line(seg(21, 2.5, 13.5, 9.5)),
        line(seg(10, 7.5, 10, 4.5)),
    ]


@icon("sashiko", CAT, "Square of fabric stitched with a wave of nested arcs in dashed running stitch",
      tags=["japanese embroidery", "running stitch", "visible mending", "boro", "stitching", "needlework"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, rr(S, 3)))]
    for a0, a1 in ((190, 232), (249, 291), (308, 350)):
        parts.append(detail(dash_arc(S, 12, 20, 4.5, a0, a1)))
    for a0, a1 in ((200, 222), (234, 256), (268, 290), (302, 324), (336, 355)):
        parts.append(detail(dash_arc(S, 12, 20, 8.5, a0, a1)))
    return parts


def _spiral(cx, cy, d, halves):
    """Spiral from half circles of growing radius, starting at the centre and turning clockwise."""
    x, y = cx, cy
    out = f"M{fmt(x)} {fmt(y)}"
    for k in range(1, halves + 1):
        r = k * d / 2
        if k % 2:  # over the top to the right
            nx = x + 2 * r
        else:  # under the bottom to the left
            nx = x - 2 * r
        out += f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(nx)} {fmt(y)}"
        x = nx
    return out, x


@icon("spinning-bobbin", CAT, "Spinning wheel bobbin lying on its side with a wide flange at each end and spun yarn wound between",
      tags=["bobbin", "spinning wheel", "yarn", "spun yarn", "spinning", "fibre"])
def _(S):
    body = union(rect(3, 4, 4, 16, rr(S, 1.5)), rect(17, 4, 4, 16, rr(S, 1.5)), rect(6, 7.5, 12, 9))
    return [
        shell(body),
        detail(seg(7, 7.5, 7, 16.5)),
        detail(seg(17, 7.5, 17, 16.5)),
        detail(seg(9.5, 16.5, 11.5, 7.5)),
        detail(seg(12.5, 16.5, 14.5, 7.5)),
    ]


@icon("rug-loom", CAT, "Tall upright frame loom with warp threads above a partly woven rug with a diamond pattern",
      tags=["loom", "frame loom", "rug weaving", "tapestry", "weaving", "warp"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 2))),
        detail(seg(8, 2.5, 8, 11)),
        detail(seg(12, 2.5, 12, 11)),
        detail(seg(16, 2.5, 16, 11)),
        detail(seg(4, 11, 20, 11)),
        detail(poly([(12, 13.75), (15, 16.5), (12, 19.25), (9, 16.5)], closed=True, r=L(S, 0, 0.6))),
    ]


@icon("knitting-machine", CAT, "Long flat knitting machine bed with a row of needles and a carriage with a handle on top",
      tags=["knitting", "machine knitting", "carriage", "needle bed", "yarn", "textile"])
def _(S):
    body = union(rect(2, 12.5, 20, 7.5, rr(S, 2)), rect(11, 7, 9, 6, rr(S, 1.5)))
    parts = [shell(body), line(poly([(13, 7), (13, 3.5), (18, 3.5), (18, 7)], r=S.r))]
    for x in (4.5, 8, 11.5, 15, 18.5):
        parts.append(detail(dash(S, x, 16.25, x + 1.5, 16.25)))
    return parts


@icon("sock-blocker", CAT, "Flat foot-shaped board with a hanging hole and a knitted sock cuff pulled over it",
      tags=["sock blocking", "sock form", "sock board", "knitting", "blocking", "socks"])
def _(S):
    board = "M6 6.5A3.5 3.5 0 0 1 13 6.5V12.5L18.5 15.2C21 16.5 21.5 21 18 21H9.5C7.5 21 6 19.5 6 17.5Z"
    return [shell(board), dot(9.5, 6.5, 1.3), detail(seg(6, 10, 13, 10)), detail(seg(9.5, 17, 16, 17))]


@icon("blocking-mat", CAT, "Square foam blocking mat with a knitted piece pinned flat at its corners",
      tags=["blocking board", "foam mat", "knitting", "crochet", "pins", "blocking"])
def _(S):
    sw = poly([(12, 6.5), (17.5, 12), (12, 17.5), (6.5, 12)], closed=True, r=L(S, 0, 1))
    return [shell(rect(3, 3, 18, 18, rr(S, 3))), detail(sw),
            dot(12, 6.5, 1.6), dot(17.5, 12, 1.6), dot(12, 17.5, 1.6), dot(6.5, 12, 1.6)]


@icon("pattern-weight", CAT, "Domed pattern weight with a knob resting on a flat sheet of pattern paper",
      tags=["sewing pattern", "pattern paper", "dressmaking", "weight", "cutting fabric", "sewing"])
def _(S):
    dome = union("M6.5 16A5.5 5.5 0 0 1 17.5 16Z", circle(12, 8.5, 1.8))
    return [
        shell(union(dome, rect(2.5, 15.5, 19, 5, rr(S, 1.5)))),
        detail(seg(9, 15.5, 15, 15.5)),
    ]


@icon("fabric-marker", CAT, "Capped fabric marker pen with the dotted line it has drawn on cloth",
      tags=["fabric pen", "marking pen", "chalk pen", "sewing", "quilting", "tracing"])
def _(S):
    pen = [
        shell(rect(9.5, 2.5, 5, 6.5, rr(S, 1.5))),
        shell(poly([(9.5, 9), (14.5, 9), (14.5, 15.5), (12, 19), (9.5, 15.5)], closed=True, r=L(S, 0, 1))),
    ]
    pen = tilt(pen, 45, centre=False)
    pen = [Part(p.kind, mv(p.d, 3, -3), p.attrs) for p in pen]
    parts = pen + [dot(3.5, 20.5, 1.2), dot(7.5, 20.5, 1.2), dot(11.5, 20.5, 1.2)]
    return parts


@icon("sewing-machine-needle", CAT, "Sewing machine needle with a flat-sided shank at the top and the eye near its point",
      tags=["machine needle", "sewing machine", "needle", "sewing", "replacement needle", "stitch"])
def _(S):
    return [
        shell(rect(9, 2.5, 6, 7, rr(S, 1))),
        detail(seg(12.5, 2.5, 12.5, 9.5)),
        line(seg(12, 9.5, 12, 13.5)),
        shell(ellipse(12, 16, 1.8, 2.5)),
        line(poly([(12, 18.5), (12, 20.5)])),
        solid(poly([(11, 20.5), (13, 20.5), (12, 22)], closed=True)),
    ]


@icon("button-box", CAT, "Small open tin filled with sewing buttons of different sizes",
      tags=["button tin", "buttons", "sewing box", "haberdashery", "notions", "sewing"])
def _(S):
    box = rect(3, 12, 18, 9, rr(S, 2))
    b1, b2 = circle(8.5, 9.5, 4), circle(16, 8, 3.5)
    return [
        shell(minus(b1, grow(box, 2))),
        shell(minus(b2, grow(box, 2), grow(b1, 2))),
        shell(box),
        dot(7.3, 8.5, 1), dot(9.7, 8.5, 1),
        dot(15, 7, 0.9), dot(17, 7, 0.9),
        detail(seg(3, 15.5, 21, 15.5)),
    ]


@icon("sewing-thread-rack", CAT, "Upright board with pegs holding two rows of thread spools",
      tags=["thread rack", "spool rack", "thread holder", "spools", "sewing room", "storage"])
def _(S):
    parts = [shell(rect(3, 2.5, 18, 19, rr(S, 2)))]
    for cx in (8.5, 15.5):
        for cy in (8, 16):
            parts.append(hole(spool(cx, cy, 5, 6, S)))
    return parts


# ============================================================================ pompoms, beads and jewellery

def heart_d(cx, cy, w):
    """Heart of width w centred on (cx, cy)."""
    k = w / 16.0
    return tf("M12 20L4.4 12.6A4.6 4.6 0 0 1 11 6.3L12 7.3L13 6.3A4.6 4.6 0 0 1 19.6 12.6Z",
              (k, 0, 0, k, cx - 12 * k, cy - 13 * k))


def star_d(cx, cy, ro, ri=None, r=0.0):
    ri = ro * 0.45 if ri is None else ri
    pts = [pt_on(cx, cy, ro if i % 2 == 0 else ri, -90 + i * 36) for i in range(10)]
    return poly(pts, closed=True, r=r)


@icon("pompom-maker", CAT, "C-shaped pompom maker ring wrapped in yarn with its opening on one side",
      tags=["pom pom maker", "pompom", "yarn", "knitting", "craft tool", "bobble"])
def _(S):
    ring = (f"M{fmt(pt_on(12, 12, 9, 35)[0])} {fmt(pt_on(12, 12, 9, 35)[1])}"
            f"A9 9 0 1 1 {fmt(pt_on(12, 12, 9, -35)[0])} {fmt(pt_on(12, 12, 9, -35)[1])}"
            f"L{fmt(pt_on(12, 12, 3.5, -35)[0])} {fmt(pt_on(12, 12, 3.5, -35)[1])}"
            f"A3.5 3.5 0 1 0 {fmt(pt_on(12, 12, 3.5, 35)[0])} {fmt(pt_on(12, 12, 3.5, 35)[1])}Z")
    parts = [shell(ring, stroke_miterlimit="2")]
    for a in (80, 130, 180, 230, 280):
        a0, a1 = pt_on(12, 12, 3.5, a), pt_on(12, 12, 9, a)
        parts.append(detail(seg(*a0, *a1)))
    return parts


@icon("seed-beads", CAT, "Small bowl heaped with tiny seed beads",
      tags=["beads", "beading", "bead tray", "bead mat", "beadwork", "jewellery making"])
def _(S):
    bowl = poly([(3, 12.5), (21, 12.5), (18, 20.5), (6, 20.5)], closed=True) if S.name == "line" else "M3 12.5H21C21 17.5 17.5 20.5 12 20.5C6.5 20.5 3 17.5 3 12.5Z"
    parts = [shell(bowl)]
    for x, y in ((7.5, 8.8), (12, 8.8), (16.5, 8.8), (9.75, 5), (14.25, 5)):
        parts.append(dot(x, y, 1.5))
    return parts


@icon("bead-loom", CAT, "Small bead loom with warp threads stretched between two posts and a band of beads woven in a diamond",
      tags=["beading loom", "loom beading", "beadwork", "seed beads", "bracelet", "weaving"])
def _(S):
    band = rect(8, 6.5, 8, 11, rr(S, 1.5))
    return [
        shell(rect(2.5, 4, 3.5, 16, rr(S, 1.5))), shell(rect(18, 4, 3.5, 16, rr(S, 1.5))),
        line(seg(6, 9, 8, 9)), line(seg(6, 15, 8, 15)), line(seg(16, 9, 18, 9)), line(seg(16, 15, 18, 15)),
        shell(band),
        detail(poly([(12, 9), (14, 12), (12, 15), (10, 12)], closed=True, r=L(S, 0, 0.5))),
    ]


@icon("charm-bracelet", CAT, "Chain with a heart charm and a star charm hanging from it",
      tags=["charms", "bracelet", "jewellery", "jewelry", "bangle", "gift"])
def _(S):
    return [
        line("M3 3.5Q12 9 21 3.5"),
        line(seg(7.5, 5.7, 7.5, 9)),
        shell(heart_d(7.5, 13.8, 8)),
        line(seg(16.5, 5.7, 16.5, 9)),
        shell(star_d(16.5, 14.6, 5, 2.4, r=L(S, 0, 0.6))),
    ]


@icon("resin-mold", CAT, "Square silicone resin mould with shaped cavities, one of them filled with resin",
      tags=["resin mould", "silicone mold", "epoxy resin", "casting", "resin art", "mould"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 4))),
        detail(circle(8.5, 8.5, 2.5)),
        detail(poly([(15.5, 6.5), (18, 10.75), (13, 10.75)], closed=True, r=L(S, 0, 0.6))),
        detail(rect(6, 13, 5, 5, L(S, 0, 1.2))),
        hole(heart_d(15.5, 15.6, 6.6)),
    ]


# ============================================================================ leather, candles and soap

@icon("leather-tooling", CAT, "Swivel knife cutting a curling line into a piece of leather",
      tags=["swivel knife", "leather carving", "leathercraft", "tooling", "leather work", "carving"])
def _(S):
    knife = [
        line(arc(12, 4.5, 3.5, 15, 165)),
        shell(rect(10.2, 6.5, 3.6, 6, L(S, 1, 1.8))),
        solid(poly([(11.2, 12.5), (12.8, 12.5), (12, 16.3)], closed=True)),
    ]
    knife = [Part(p.kind, rot(p.d, 28, 12, 16.3), p.attrs) for p in knife]
    return [
        shell(rect(2.5, 15, 19, 6.5, rr(S, 2.5))),
        detail("M5.5 19C8 17.3 11 20 13.5 18.7C15.5 17.8 17.5 18.7 18.5 19.5"),
    ] + knife


@icon("saddle-stitch", CAT, "Piece of leather with a row of slanted hand stitches along its middle",
      tags=["leather stitching", "hand stitching", "saddle stitching", "leathercraft", "sewing", "stitch"])
def _(S):
    parts = [shell(rect(2.5, 6.5, 19, 11, rr(S, 2.5)))]
    for x in (6, 10, 14, 18):
        parts.append(detail(dash(S, x - 1, 14, x + 1, 10)))
    return parts


@icon("candle-wick", CAT, "Waxed candle wick standing upright on a round metal sustainer tab",
      tags=["wick", "candle making", "wick tab", "sustainer", "wax", "candle"])
def _(S):
    return [
        line("M12 14V6C12 4.5 13 3.5 14.5 3"),
        shell(rect(9.5, 14, 5, 3.5, L(S, 0.5, 1.5))),
        shell(rect(4, 17.5, 16, 3.5, L(S, 0.5, 1.75))),
    ]


@icon("wax-melting-pot", CAT, "Metal pouring pitcher with a spout and handle standing in a pan of hot water",
      tags=["pouring pitcher", "melting pot", "double boiler", "candle making", "wax", "soap making"])
def _(S):
    pan = rect(2.5, 13, 19, 8, rr(S, 3))
    pitcher = poly([(6, 5.5), (15, 5.5), (15, 14), (7, 14)], closed=True, r=L(S, 0, 1))
    spout = poly([(6, 5.5), (3.5, 3.5), (6.5, 8.5)], closed=True)
    body = union(pitcher, spout)
    return [
        shell(minus(body, grow(pan, 2))),
        line(poly([(15, 7.5), (18.5, 7.5), (18.5, 10.5)], r=S.r)),
        shell(pan),
        detail("M6 17Q7.5 15.8 9 17T12 17T15 17T18 17"),
    ]


def _hex(cx, cy, r, S):
    return poly(regular(cx, cy, r, 6, -90), closed=True, r=L(S, 0, 0.4))


@icon("beeswax-candle-rolling", CAT, "Honeycomb beeswax sheet being rolled around a wick into a candle",
      tags=["beeswax", "rolled candle", "honeycomb sheet", "candle making", "wax", "wick"])
def _(S):
    return [
        shell(rect(3, 6.5, 5.5, 15, rr(S, 2.5))),
        line(seg(5.75, 6.5, 5.75, 2.5)),
        shell(poly([(8.5, 9), (21, 7), (21, 19), (8.5, 21.5)], closed=True, r=L(S, 0, 1))),
        detail(_hex(13, 12.25, 2.3, S)),
        detail(_hex(13, 17.25, 2.3, S)),
        detail(_hex(17.3, 14.75, 2.3, S)),
    ]


@icon("bath-bomb-mold", CAT, "Two metal half-sphere mould shells held apart with a round bath bomb between them",
      tags=["bath bomb mould", "bath bomb", "fizzer", "mold", "spa", "bath"])
def _(S):
    left = "M6.5 5.5A4 6.5 0 0 0 6.5 18.5Z"
    right = "M17.5 5.5A4 6.5 0 0 1 17.5 18.5Z"
    return [shell(left), shell(right), shell(circle(12, 12, 3))]


@icon("potpourri", CAT, "Small bowl filled with dried petals, a leaf and a cinnamon stick",
      tags=["pot pourri", "dried petals", "fragrance", "home scent", "dried flowers", "bowl"])
def _(S):
    bowl = "M3 13.5H21C21 18 17 21 12 21C7 21 3 18 3 13.5Z"
    leaf = "M4.5 11.5C4.5 7.5 7 5.5 10.5 5.5C10.5 9 8.5 11.5 4.5 11.5Z"
    stick = rect(13.5, 4, 3.5, 9.5, L(S, 0.5, 1.75))
    stick = rot(stick, 30, 15.25, 8.75)
    return [
        shell(bowl),
        shell(minus(leaf, grow(bowl, 2))),
        detail(seg(6, 10, 9, 7)),
        shell(minus(stick, grow(bowl, 2))),
        dot(11.5, 10.75, 1.4),
    ]


# ============================================================================ flowers and nature

def _leaf(cx, cy, length, width, deg):
    """Pointed leaf centred on (cx, cy), its long axis turned deg clockwise from vertical."""
    h, k = length / 2, width * 0.66
    d = (f"M{fmt(cx)} {fmt(cy - h)}C{fmt(cx + k)} {fmt(cy - h * 0.4)} {fmt(cx + k)} {fmt(cy + h * 0.4)} {fmt(cx)} {fmt(cy + h)}"
         f"C{fmt(cx - k)} {fmt(cy + h * 0.4)} {fmt(cx - k)} {fmt(cy - h * 0.4)} {fmt(cx)} {fmt(cy - h)}Z")
    return rot(d, deg, cx, cy)


@icon("dried-flower-bouquet", CAT, "Small bundle of dried stems with seed heads, tied with a string bow",
      tags=["dried flowers", "bouquet", "lavender bundle", "everlasting flowers", "floristry", "posy"])
def _(S):
    return [
        line(seg(12, 21, 12, 8)),
        line(seg(12, 21, 6.5, 9.5)),
        line(seg(12, 21, 17.5, 9.5)),
        shell(_leaf(12, 5.5, 5.5, 3, 0)),
        shell(_leaf(5.5, 7, 5.5, 3, -25)),
        shell(_leaf(18.5, 7, 5.5, 3, 25)),
        shell(poly([(12, 16), (7.5, 13.5), (7.5, 18.5)], closed=True, r=L(S, 0, 0.8))),
        shell(poly([(12, 16), (16.5, 13.5), (16.5, 18.5)], closed=True, r=L(S, 0, 0.8))),
    ]


@icon("flower-arranging", CAT, "Low shallow vase with three flower stems set at different angles",
      tags=["floral arrangement", "flower arrangement", "floristry", "vase", "ikebana", "centrepiece"])
def _(S):
    return [
        shell(rect(3, 16, 18, 5, rr(S, 2.5))),
        line("M11 16C10 12 8 9 5 6.5"),
        line("M12.5 16C13 12 13.5 8.5 14 5"),
        line("M14 16C15.5 14 17.5 12.5 20 12"),
        dot(5, 6.5, 2.2), dot(14, 5, 2.2), dot(20, 12, 1.8),
    ]


@icon("floral-tape", CAT, "Roll of florist tape beside a flower stem wrapped in slanted bands",
      tags=["florist tape", "stem wrap", "floristry", "tape", "wiring flowers", "corsage"])
def _(S):
    return [
        line(seg(18, 2.5, 18, 21.5)),
        line(seg(14.5, 7, 21.5, 4.5)),
        line(seg(14.5, 11.5, 21.5, 9)),
        line(seg(14.5, 16, 21.5, 13.5)),
        shell(circle(7.5, 16, 5)),
        dot(7.5, 16, 1.5),
    ]


@icon("wreath-frame", CAT, "Round wire wreath frame of two rings joined by a zigzag of struts",
      tags=["wreath ring", "wire frame", "wreath making", "floristry", "christmas wreath", "hoop"])
def _(S):
    pts = []
    for i in range(12):
        a = -90 + i * 30
        pts.append(pt_on(12, 12, 9 if i % 2 == 0 else 5, a))
    return [line(circle(12, 12, 9)), line(circle(12, 12, 5)), detail(poly(pts, closed=True, r=L(S, 0, 0.8)))]


@icon("nature-journal", CAT, "Open notebook with a leaf sketched on one page and a pressed leaf on the other",
      tags=["nature notebook", "field journal", "sketchbook", "pressed leaf", "botany", "nature study"])
def _(S):
    left = poly([(12, 6), (7, 4), (2.5, 4.5), (2.5, 19.5), (7, 19), (12, 21)], closed=True, r=L(S, 0, 1.2))
    right = poly([(12, 6), (17, 4), (21.5, 4.5), (21.5, 19.5), (17, 19), (12, 21)], closed=True, r=L(S, 0, 1.2))
    return [
        shell(union(left, right)),
        detail(seg(12, 6, 12, 21)),
        detail(_leaf(7.25, 12, 7, 3, 20)),
        hole(_leaf(16.75, 12, 7.5, 4.2, 20)),
    ]


# ============================================================================ cameras and art curiosities

@icon("rangefinder-camera", CAT, "Compact film camera with a round lens, a small viewfinder window in the top corner and a rewind knob",
      tags=["film camera", "35mm camera", "rangefinder", "analogue camera", "photography", "vintage camera"])
def _(S):
    return [
        shell(rect(2.5, 7, 19, 13, rr(S, 3))),
        solid(rect(4.5, 4.5, 4, 2.5, L(S, 0, 0.8))),
        solid(rect(15.5, 5, 3, 2, L(S, 0, 0.8))),
        detail(circle(10.5, 13.5, 3.5)),
        hole(rect(16, 9.5, 3.5, 2.5, L(S, 0, 0.8))),
    ]


@icon("golden-spiral", CAT, "Golden rectangle split into shrinking squares with a spiral sweeping through them",
      tags=["golden ratio", "fibonacci spiral", "phi", "composition", "divine proportion", "design"])
def _(S):
    spiral = "M3 17A12 12 0 0 1 15 5A7 7 0 0 1 22 12A4.5 4.5 0 0 1 17.5 16.5"
    return [
        shell(rect(3, 5, 19, 12, rr(S, 1.5))),
        detail(seg(15, 5, 15, 17)),
        detail(seg(15, 12, 22, 12)),
        line(spiral),
    ]


@icon("fleuron", CAT, "Printer's flower ornament: a heart-shaped leaf on a curling stem",
      tags=["printers flower", "hedera", "ornament", "typography", "dinkus", "floral heart"])
def _(S):
    leaf = "M12 2.5C8.5 6 4 8.5 4 12A4 4 0 0 0 12 13.5A4 4 0 0 0 20 12C20 8.5 15.5 6 12 2.5Z"
    stem = "M12 13.5C12 17 11 19.5 13.5 20.5C16 21.5 19 20 19 17.5C19 15.5 16.5 15.5 16 17.5"
    return [shell(leaf), line(stem), detail(seg(12, 6.5, 12, 10))]


@icon("flipbook", CAT, "Small pad with a folded page corner and a stick figure drawn on the page",
      tags=["flip book", "animation", "flick book", "cartoon", "drawing", "motion"])
def _(S):
    page = poly([(3, 3), (20, 3), (20, 14), (13, 21), (3, 21)], closed=True, r=L(S, 0, 1.5))
    return [
        shell(page),
        shell(poly([(20, 14), (13, 21), (13, 14)], closed=True, r=L(S, 0, 1))),
        dot(9, 7.5, 1.6),
        detail(poly([(9, 10), (9, 14), (6.5, 17.5)], r=L(S, 0, 0.8))),
        detail(seg(9, 14, 11.5, 17.5)),
    ]

# ============================================================================ more fibre and textile work

@icon("shibori", CAT, "Square of resist-dyed cloth patterned with a grid of four diamond motifs",
      tags=["tie dye", "resist dye", "japanese dyeing", "indigo", "fabric dye", "textile"])
def _(S):
    sp, _x = _spiral(10.2, 12.9, 3.6, 3)
    return [shell(rect(3, 3, 18, 18, rr(S, 3))), detail(sp)]


@icon("wool-roving", CAT, "Soft rope of combed wool roving coiled in a loose spiral with a fluffy loose end",
      tags=["roving", "wool", "spinning fibre", "felting", "fibre arts", "combed top"])
def _(S):
    sp, _x = _spiral(12, 11, 4.0, 4)
    return [
        line(sp),
        line(seg(4, 11, 3, 15)),
        line(seg(4, 11, 6.5, 16)),
    ]


@icon("jewelry-pliers", CAT, "Round nose pliers with conical jaws and a loop of wire at the tip",
      tags=["round nose pliers", "jewellery pliers", "wire bending", "wire wrapping", "beading tool", "loop"])
def _(S):
    return [
        shell(poly([(9, 11.5), (9.5, 7), (11.5, 2.5), (12.5, 2.5), (14.5, 7), (15, 11.5)], closed=True, r=L(S, 0, 0.8))),
        shell(poly([(9, 11), (12, 11), (9, 21.5), (5, 21.5)], closed=True, r=L(S, 0, 1))),
        shell(poly([(12, 11), (15, 11), (19, 21.5), (15, 21.5)], closed=True, r=L(S, 0, 1))),
        detail(seg(12, 5, 12, 10)),
        line("M14.5 7C19.5 5.5 21 10 17 10.5"),
    ]


@icon("gauge-swatch", CAT, "Knitted swatch with a ruler along its bottom edge used to count stitches per inch",
      tags=["knitting gauge", "tension square", "stitch count", "swatch", "ruler", "knitting"])
def _(S):
    body = union(rect(5, 3, 14, 13, rr(S, 2)), rect(2.5, 15, 19, 6, rr(S, 1.5)))
    parts = [shell(body), detail(seg(5, 15, 19, 15))]
    for x in (9.5, 14.5):
        parts.append(detail(seg(x, 5.5, x, 12.5)))
    for x in (6.5, 10, 13.5, 17):
        parts.append(detail(seg(x, 15, x, 18.5)))
    return parts


@icon("needle-gauge", CAT, "Flat needle gauge card with round holes that grow in size and a ruler scale down one edge",
      tags=["knitting needle gauge", "needle sizer", "needle size", "knitting", "crochet hook gauge", "measuring"])
def _(S):
    parts = [shell(rect(3, 2.5, 18, 19, rr(S, 2.5)))]
    for cy, r in ((6.5, 1), (11.25, 1.6), (17, 2.4)):
        parts.append(hole(circle(8.5, cy, r)))
    for i, y in enumerate((6, 9.5, 13, 16.5)):
        parts.append(detail(seg(21, y, 21 - (3.5 if i % 2 == 0 else 2.2), y)))
    return parts


@icon("cable-knit-pattern", CAT, "Band of knitting with a twisted rope cable running down the middle",
      tags=["cable stitch", "aran", "fisherman knit", "knitting pattern", "twisted stitch", "sweater"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 2.5))),
        detail("M9 3.5C9 8 15 8 15 12.5C15 17 9 17 9 21"),
        detail("M15 3.5C15 8 9 8 9 12.5C9 17 15 17 15 21"),
    ]


@icon("fabric-bundle", CAT, "Stack of folded fabric pieces tied with a ribbon bow",
      tags=["fat quarters", "quilting fabric", "fabric stack", "fabric pack", "textile bundle", "sewing"])
def _(S):
    stack = union(rect(3, 10, 16.5, 4, rr(S, 1.5)), rect(4.5, 13.5, 16.5, 4, rr(S, 1.5)), rect(3, 17, 16.5, 4, rr(S, 1.5)))
    return [
        shell(stack),
        detail(seg(4.5, 14, 19.5, 14)),
        detail(seg(4.5, 17.5, 19.5, 17.5)),
        detail(seg(12, 10, 12, 21)),
        shell(rot(ellipse(8, 6, 3.6, 2.1), -22, 8, 6)),
        shell(rot(ellipse(16, 6, 3.6, 2.1), 22, 16, 6)),
    ]


# ============================================================================ jewellery findings, leather and print studio

@icon("lobster-clasp", CAT, "Teardrop jewellery clasp with a small spring lever on top and a ring at its tip",
      tags=["lobster claw clasp", "trigger clasp", "necklace clasp", "jewellery findings", "fastener", "jewelry making"])
def _(S):
    body = "M8 12L11.3 8.1A6 6 0 1 1 11.3 15.9Z"
    return [
        shell(body),
        shell(rect(13.5, 2.5, 4, 4, rr(S, 1.5))),
        detail(seg(11.5, 12, 18, 12)),
        shell(circle(4.6, 12, 2.6)),
    ]


@icon("pricking-iron", CAT, "Leather pricking iron with a row of pointed prongs at the tip marking stitch holes",
      tags=["stitch marker", "stitching chisel", "diamond chisel", "leathercraft", "saddle stitch", "punch"])
def _(S):
    body = union(rect(9, 2.5, 6, 9.5, rr(S, 2)), poly([(9.5, 11), (14.5, 11), (19, 16.5), (5, 16.5)], closed=True, r=L(S, 0, 1)))
    parts = [shell(body)]
    for x in (5, 8.5, 12, 15.5):
        parts.append(solid(poly([(x, 16.5), (x + 3.5, 16.5), (x + 1.75, 21.5)], closed=True)))
    return parts


@icon("etching-plate", CAT, "Metal etching plate with a scratched line drawing and an etching needle resting on it",
      tags=["printmaking", "intaglio", "drypoint", "copper plate", "etching needle", "engraving"])
def _(S):
    needle = [
        shell(rect(10, 2.5, 2.5, 6, rr(S, 1))),
        line(seg(11.25, 8.5, 11.25, 14)),
    ]
    needle = [Part(p.kind, rot(p.d, 45, 11.25, 14), p.attrs) for p in needle]
    return [
        shell(rect(3, 9, 14.5, 12.5, rr(S, 2))),
        detail("M6 18C7.5 14 9.5 18.5 11 15.5"),
    ] + needle


@icon("sun-print", CAT, "Dark paper with a pale leaf silhouette left where the leaf blocked the sun above",
      tags=["cyanotype", "solar print", "sun paper", "leaf print", "botanical print", "photogram"])
def _(S):
    parts = [
        shell(rect(3, 10.5, 18, 11, rr(S, 2.5))),
        detail(_leaf(11.5, 16, 8, 4.6, 35)),
        shell(circle(17.5, 4.5, 1.9)),
    ]
    for a in (180, 135, 90):
        p0, p1 = pt_on(17.5, 4.5, 4.2, a), pt_on(17.5, 4.5, 5.6, a)
        parts.append(line(seg(*p0, *p1)))
    return parts


def scallop(cx, cy, R, n, bulge):
    """Closed outline of n outward arcs around a circle of radius R (a plate with a scalloped rim)."""
    pts = [pt_on(cx, cy, R, -90 + i * 360 / n) for i in range(n)]
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(1, n + 1):
        x, y = pts[i % n]
        d += f"A{fmt(bulge)} {fmt(bulge)} 0 0 1 {fmt(x)} {fmt(y)}"
    return d + "Z"


def wobbly(x0, y0, x1, y1, step=4.0, amp=0.7):
    """Rectangle outline whose edges ripple slightly, like a torn deckle edge."""
    d = f"M{fmt(x0)} {fmt(y0)}"
    sign = 1
    edges = [((x0, y0), (x1, y0), (0, -1)), ((x1, y0), (x1, y1), (1, 0)),
             ((x1, y1), (x0, y1), (0, 1)), ((x0, y1), (x0, y0), (-1, 0))]
    for (ax, ay), (bx, by), (nx, ny) in edges:
        ln = math.hypot(bx - ax, by - ay)
        n = max(1, round(ln / step))
        for i in range(1, n + 1):
            t0, t1 = (i - 0.5) / n, i / n
            cx, cy = ax + (bx - ax) * t0 + nx * amp * sign, ay + (by - ay) * t0 + ny * amp * sign
            ex, ey = ax + (bx - ax) * t1, ay + (by - ay) * t1
            d += f"Q{fmt(cx)} {fmt(cy)} {fmt(ex)} {fmt(ey)}"
            sign = -sign
    return d + "Z"


@icon("limited-edition-print", CAT, "Art print sheet with a picture in the middle, a pencil signature and an edition number in the corner",
      tags=["numbered print", "signed print", "edition", "giclee", "artist print", "collectible"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 2.5))),
        detail(rect(6.5, 5.5, 11, 7.5, L(S, 0, 1))),
        dot(10, 8.5, 1.1),
        detail("M6.5 18C8 15.5 9.2 19.5 10.8 17"),
        detail(seg(15.5, 19, 17.5, 16.5)),
    ]


@icon("live-edge-slab", CAT, "Thick slice of wood with straight cut ends and wavy natural bark edges along both long sides",
      tags=["live edge", "wood slab", "river table", "woodworking", "tabletop", "natural edge"])
def _(S):
    slab = "M3 9C4.5 6 6.5 5 8 7C9.5 9 11 4.5 13.5 5C16 5.5 16.5 8 18.5 7C19.5 6.5 20.5 5.5 21 5V18H3Z"
    return [
        shell(slab),
        detail("M6.5 13C9 11 12 14 14.5 12"),
        dot(17.5, 14.5, 1.3),
    ]


@icon("clay-wire-cutter", CAT, "Thin cutting wire with a wooden toggle handle at each end, sagging in the middle",
      tags=["pottery", "ceramics", "clay cutting", "wire tool", "potter tool", "toggle handle"])
def _(S):
    return [
        shell(rect(2.5, 6.5, 4, 10, rr(S, 2))),
        shell(rect(17.5, 6.5, 4, 10, rr(S, 2))),
        line("M6.5 11.5C8 20 16 20 17.5 11.5"),
    ]


@icon("deckle-edge-paper", CAT, "Sheet of handmade paper with rough feathered deckle edges all around",
      tags=["handmade paper", "torn edge", "artisan paper", "rag paper", "papermaking", "stationery"])
def _(S):
    return [
        shell(wobbly(4, 2.5, 20, 21.5, 4.0, 0.8)),
        detail(seg(8, 8, 16, 8)),
        detail(seg(8, 12, 16, 12)),
        detail(seg(8, 16, 13, 16)),
    ]


@icon("flat-file-cabinet", CAT, "Low wide cabinet of shallow drawers, each with a small pull handle, standing on short feet",
      tags=["map drawers", "plan chest", "art storage", "drawers", "archive cabinet", "studio furniture"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 15, rr(S, 2))),
        detail(seg(2.5, 8.5, 21.5, 8.5)),
        detail(seg(2.5, 13.5, 21.5, 13.5)),
        dot(12, 6, 0.9), dot(12, 11, 0.9), dot(12, 16, 0.9),
        line(seg(6, 18.5, 6, 21.5)),
        line(seg(18, 18.5, 18, 21.5)),
    ]


# ============================================================================ studio storage, display and hobby builds

@icon("art-caddy", CAT, "Open carry tray with a centre handle holding two pencils and a paint tube",
      tags=["art supplies", "supply caddy", "craft organiser", "brush holder", "paint tray", "studio storage"])
def _(S):
    parts = [
        shell(poly([(3, 14), (21, 14), (19.5, 21), (4.5, 21)], closed=True, r=L(S, 0, 1.5))),
        shell(union(rect(10.75, 4.5, 2.5, 9.5), rect(8, 2.5, 8, 3))),
        line(seg(5, 14, 5, 8)),
        line(seg(7.25, 14, 7.25, 8)),
        shell(rect(16.5, 7.5, 4, 6.5, L(S, 0.5, 1.75))),
    ]
    for x in (5, 7.25):
        parts.append(solid(poly([(x - 1, 8), (x + 1, 8), (x, 5.5)], closed=True)))
    return parts


@icon("card-pack", CAT, "Foil trading card pack torn open along a jagged top edge with a card sticking out",
      tags=["booster pack", "trading cards", "card game", "collectible cards", "sealed pack", "tcg"])
def _(S):
    pack = poly([(4.5, 10), (7, 8.2), (9, 10), (12, 7.8), (14, 9.6), (19.5, 6.5), (19.5, 21), (4.5, 21)], closed=True, r=L(S, 0, 0.6))
    card = rot(rect(8.5, 2.5, 7, 9, rr(S, 1.5)), 12, 12, 7)
    return [
        shell(minus(card, grow(pack, 1.6))),
        shell(pack),
        detail(seg(4.5, 18, 19.5, 18)),
        hole(star_d(12, 14, 3, 1.35, r=L(S, 0, 0.3))),
    ]


@icon("display-plate", CAT, "Decorative round plate with an inner ring and centre dot standing upright on a small stand",
      tags=["wall plate", "china plate", "collectible plate", "ceramics", "commemorative plate", "plate stand"])
def _(S):
    parts = [shell(circle(12, 10.2, 8.2)), detail(circle(12, 10.2, 4)), dot(12, 10.2, 1.3)]
    return parts + [line(seg(12, 19.5, 12, 21.5)), line(seg(7.5, 21.5, 16.5, 21.5))]


@icon("truss-bridge-model", CAT, "Model bridge built from craft sticks with a zigzag triangle truss along its side",
      tags=["craft stick bridge", "popsicle stick bridge", "engineering project", "steam project", "model", "truss"])
def _(S):
    return [
        shell(rect(3, 6, 18, 10, rr(S, 1.5))),
        detail(poly([(3, 15), (7.5, 7), (12, 15), (16.5, 7), (21, 15)], r=L(S, 0, 0.8))),
        line(seg(6, 16, 6, 21.5)),
        line(seg(18, 16, 18, 21.5)),
    ]


@icon("relief-carving", CAT, "Flat wooden panel with a raised carved leaf standing out from the background",
      tags=["wood carving", "carved panel", "woodcarving", "bas relief", "chisel work", "carved leaf"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 2.5))),
        detail(_leaf(12, 12, 12.5, 7.5, 40)),
        detail(rot(seg(12, 9.5, 12, 14.5), 40, 12, 12)),
    ]


@icon("stop-motion", CAT, "Camera on a small tripod aimed at a little clay figure",
      tags=["claymation", "animation", "stop motion animation", "frame by frame", "clay figure", "filming"])
def _(S):
    return [
        shell(rect(2.5, 5, 9, 7, rr(S, 2))),
        shell(rect(11, 6.5, 2.5, 4, L(S, 0, 1))),
        line(seg(7, 12, 4, 21)),
        line(seg(7, 12, 10, 21)),
        shell(circle(18, 8.5, 2.4)),
        shell(rect(15, 12.5, 6, 8.5, rr(S, 3))),
    ]


@icon("bobblehead", CAT, "Figure with an oversized round head on a coiled spring neck above a small body",
      tags=["bobble head", "nodding figure", "collectible", "spring neck", "desk toy", "figurine"])
def _(S):
    return [
        shell(circle(12, 8, 5.5)),
        hole(circle(9.75, 7.5, 0.9)),
        hole(circle(14.25, 7.5, 0.9)),
        line("M10.5 14.5L13.5 15.5L10.5 16.5L13.5 17.5"),
        shell(rect(8, 18, 8, 3.5, rr(S, 1.75))),
    ]


@icon("rangoli", CAT, "Symmetrical floor pattern of six petals radiating from a central dot",
      tags=["kolam", "floor art", "diwali", "indian folk art", "mandala", "festival decoration"])
def _(S):
    parts = []
    for i in range(6):
        a = i * 60
        cx, cy = pt_on(12, 12, 6.6, a - 90)
        parts.append(shell(_leaf(cx, cy, 7.2, 4.2, a)))
    parts.append(hole(circle(12, 12, 1.4)))
    return parts


@icon("poster-tube", CAT, "Long cardboard poster tube with a cap on each end and a carry strap along its side",
      tags=["mailing tube", "print tube", "art storage", "shipping tube", "drawing tube", "carry strap"])
def _(S):
    tube = union(rect(8.5, 3, 7, 18, rr(S, 1)), rect(7.5, 3, 9, 3.5, rr(S, 1)), rect(7.5, 17.5, 9, 3.5, rr(S, 1)))
    parts = [shell(tube), line("M16.5 9.5C20.5 10.5 20.5 14.5 16.5 15.5")]
    return tilt(parts, 45)


@icon("braiding-disk", CAT, "Round braiding disk with slots around the rim and cords gathered through the centre hole into a braid",
      tags=["kumihimo", "braiding", "cord braiding", "disc braiding", "japanese braid", "friendship bracelet"])
def _(S):
    parts = [shell(circle(12, 10, 8)), hole(circle(12, 10, 2))]
    for i in range(8):
        a = -90 + i * 45 + 22.5
        parts.append(detail(seg(*pt_on(12, 10, 5.4, a), *pt_on(12, 10, 8, a))))
    parts.append(line("M12 12Q9.5 14.5 12 17T12 22"))
    return parts


@icon("model-catapult", CAT, "Small wooden catapult with an A-frame, a throwing arm with a cup and a ball ready to fly",
      tags=["trebuchet", "siege model", "stem project", "launcher", "medieval model", "wooden kit"])
def _(S):
    return [
        shell(rect(3, 18.5, 18, 3, rr(S, 1.25))),
        line(poly([(6.5, 18.5), (11, 9.5), (15.5, 18.5)])),
        line(seg(4, 14, 18, 5.5)),
        line(arc(18.5, 4.5, 2.6, 10, 170)),
        dot(18.5, 2.4, 1.5),
    ]


@icon("water-rocket", CAT, "Plastic bottle rocket turned upside down with three fins and a nose cone on a launch tube",
      tags=["bottle rocket", "pressure rocket", "science project", "model rocket", "stem experiment", "launch"])
def _(S):
    body = union(rect(8, 8.5, 8, 9.5, rr(S, 1)), poly([(8, 8.5), (12, 3), (16, 8.5)], closed=True))
    return [
        shell(body),
        shell(poly([(8, 13.5), (4.5, 19), (8, 18.5)], closed=True, r=L(S, 0, 0.6))),
        shell(poly([(16, 13.5), (19.5, 19), (16, 18.5)], closed=True, r=L(S, 0, 0.6))),
        detail("M8 12.5Q10 11.5 12 12.5T16 12.5"),
        shell(rect(10.5, 18, 3, 2.5, rr(S, 1))),
        line(seg(8, 21.5, 16, 21.5)),
    ]


# ============================================================================ camera and studio gear, tattoo gear

@icon("360-camera", CAT, "Slim upright stick camera with round lenses bulging from both faces",
      tags=["360 degree camera", "panoramic camera", "spherical camera", "vr camera", "action camera", "immersive video"])
def _(S):
    body = union(rect(9, 2.5, 6, 19, rr(S, 3)), circle(12, 8, 4.6))
    return [
        shell(body),
        hole(circle(12, 8, 1.8)),
        hole(circle(12, 16.5, 0.9)),
    ]


@icon("stereo-camera", CAT, "Wide vintage camera body with two round lenses side by side on its front",
      tags=["3d camera", "twin lens camera", "stereoscopic", "stereo photography", "vintage camera", "dual lens"])
def _(S):
    body = union(rect(2.5, 8, 19, 12, rr(S, 3)), rect(9.5, 4.5, 5, 4.5, rr(S, 1)))
    return [
        shell(body),
        detail(circle(7.5, 14, 2.8)),
        detail(circle(16.5, 14, 2.8)),
        hole(circle(7.5, 14, 0.8)),
        hole(circle(16.5, 14, 0.8)),
    ]


@icon("trail-camera", CAT, "Weatherproof game camera box strapped between tree trunk edges, with a lens and a sensor window",
      tags=["game camera", "wildlife camera", "trail cam", "hunting camera", "motion sensor camera", "nature monitoring"])
def _(S):
    cam = rect(6.5, 6, 11, 11, rr(S, 2))
    return [
        line(seg(3.5, 2.5, 3.5, 21.5)),
        line(seg(20.5, 2.5, 20.5, 21.5)),
        line(seg(3.5, 9, 6.5, 9)),
        line(seg(17.5, 9, 20.5, 9)),
        line(seg(3.5, 15.5, 6.5, 15.5)),
        line(seg(17.5, 15.5, 20.5, 15.5)),
        shell(cam),
        detail(circle(12, 12.5, 2.3)),
        hole(rect(9.5, 8, 5, 1.2, 0.6)),
    ]


@icon("led-light-panel", CAT, "Flat rectangular LED light panel with a grid of small lamps on a short stem and stand",
      tags=["video light", "photography light", "studio light", "panel light", "lighting", "led lamp"])
def _(S):
    parts = [shell(rect(3, 2.5, 18, 13, rr(S, 2)))]
    for x in (6.5, 10, 14, 17.5):
        for y in (6, 9, 12):
            parts.append(hole(circle(x, y, 0.9)))
    parts += [line(seg(12, 15.5, 12, 19.5)), line(seg(6.5, 21.5, 17.5, 21.5))]
    return parts


@icon("slide-carousel", CAT, "Round projector slide tray with narrow slots around its ring and a square slide above it",
      tags=["slide projector", "slide tray", "photo slides", "35mm slides", "retro projector", "transparencies"])
def _(S):
    parts = [
        shell(circle(12, 14, 7.5)),
        hole(circle(12, 14, 1.8)),
        shell(rect(9, 2.5, 6, 6, rr(S, 1))),
    ]
    for i in range(10):
        a = -90 + i * 36 + 18
        if abs(((a + 90) % 360) - 0) < 40 or abs(((a + 90) % 360) - 360) < 40:
            continue
        parts.append(detail(seg(*pt_on(12, 14, 4.2, a), *pt_on(12, 14, 7.5, a))))
    return parts
