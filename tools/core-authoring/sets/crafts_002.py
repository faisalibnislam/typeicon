"""TypeIcon Core: crafts (batch 002, fibre crafts, woodwork, making, photography gear and collecting).

Visual language: fluffy yarn is a scalloped circle, long hand tools lean on a 45 degree diagonal, camera
gear is drawn in side view with a flat ground line where a stand needs one.
"""
from __future__ import annotations

import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, LINE, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "crafts"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rpts(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rpoly(pts, deg, closed=True, r=0.0, cx=12.0, cy=12.0):
    return poly(rpts(pts, deg, cx, cy), closed=closed, r=r)


def rseg(x1, y1, x2, y2, deg, cx=12.0, cy=12.0):
    (a, b), (c, d) = rpts([(x1, y1), (x2, y2)], deg, cx, cy)
    return seg(a, b, c, d)


def rot(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def mark(d):
    """Small solid mark: solid in stroke styles, knocked out of a Filled shell."""
    return Part("dot", d)


def scallop(cx, cy, R, n, k=0.6, start=-90.0):
    """Closed ring of n outward bumps through n points on a circle of radius R (k >= 0.5 sets bump depth)."""
    pts = [polar(cx, cy, R, start + i * 360 / n) for i in range(n)]
    chord = 2 * R * math.sin(math.pi / n)
    rb = chord * k
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(n):
        q = pts[(i + 1) % n]
        d += f"A{fmt(rb)} {fmt(rb)} 0 0 1 {fmt(q[0])} {fmt(q[1])}"
    return d + "Z"


def solid_of(ds, w=2.0):
    """Filled silhouette of closed outlines (region plus its stroke)."""
    return U(*[U(P(d), ST(d, w, "butt", "miter", 4.0)) for d in ds])


# ============================================================================ fibre crafts

@icon("pom-pom", CAT, "Fluffy round ball of yarn with its tie ends sticking up on top",
      tags=["pompom", "yarn ball", "fluffy", "knitting", "hat topper", "tassel"])
def _(S):
    return [
        shell(scallop(12, 14, 6, 9, L(S, 0.72, 0.56))),
        line(L(S, "M9 2.5L12 6.5L15 2.5", "M9 2.5Q11.5 4 12 6.5Q12.5 4 15 2.5")),
    ]


@icon("amigurumi", CAT, "Small crocheted toy bear with a big round head, round ears and a stubby body",
      tags=["crochet toy", "crochet bear", "stuffed toy", "plush", "handmade toy", "yarn toy"])
def _(S):
    head = union(circle(12, 9.5, 5.5), circle(7, 4.8, 2.2), circle(17, 4.8, 2.2))
    body = rect(6.5, 14.5, 11, 7.5, L(S, 2, 3.5))
    return [
        shell(union(head, body)),
        detail(arc(12, 9.5, 5.5, 38, 142)),
        dot(10, 9, 1), dot(14, 9, 1),
        detail(seg(12, 17.5, 12, 19.5)),
    ]


@icon("punch-needle", CAT, "Pen shaped punch needle with a slanted hollow tip and yarn running from its handle",
      tags=["punch needle", "rug punch", "embroidery", "yarn", "needle punch", "textile art"])
def _(S):
    deg = 45
    handle = rpoly([(9, 3.5), (15, 3.5), (15, 14.5), (9, 14.5)], deg, r=L(S, 0.6, 2.5))
    tip = rpoly([(10.5, 14.5), (13.5, 14.5), (13.5, 18), (10.5, 21.5)], deg, r=S.r * 0.3)
    return [
        shell(handle),
        shell(tip, stroke_miterlimit="2"),
        detail(rseg(12, 6.5, 12, 11.5, deg)),
        line(L(S, "M18.4 5.6L20.5 4.5L21.5 2", "M18.4 5.6Q21 4.5 21.5 2")),
    ]


@icon("felting-needle", CAT, "Thin felting needle with a bent top poking into a fluffy ball of wool",
      tags=["needle felting", "felting", "wool", "roving", "felt", "fibre art", "fiber art"])
def _(S):
    return [
        shell(scallop(9.5, 15, 5.2, 9, L(S, 0.72, 0.56), -70)),
        line(L(S, "M21.5 5L19 2.5L11 10.5", "M21.5 5L20.2 3.7Q19 2.5 17.8 3.7L11 10.5")),
    ]


@icon("basket-weaving", CAT, "Round woven basket with over and under strips and upright stakes above the rim",
      tags=["basketry", "weaving", "wicker", "rattan", "cane", "handwoven", "basket making"])
def _(S):
    body = poly([(3, 10), (21, 10), (18.5, 21), (5.5, 21)], closed=True, r=S.r)
    return [
        shell(body),
        line(seg(7.5, 3.5, 7.5, 10)), line(seg(12, 3.5, 12, 10)), line(seg(16.5, 3.5, 16.5, 10)),
        detail(seg(4.5, 15.5, 19.5, 15.5)),
        detail(seg(9.5, 10, 9.5, 15.5)), detail(seg(14.5, 10, 14.5, 15.5)),
        detail(seg(12, 15.5, 12, 21)),
    ]


@icon("tatting-shuttle", CAT, "Pointed oval tatting shuttle with thread wound inside and a small lace ring on its thread",
      tags=["tatting", "lace making", "shuttle", "lace", "needlework", "thread"])
def _(S):
    a, b, y, h = 2.5, 15.5, 16, 3.5
    r = ((b - a) ** 2 / 4 + h * h) / (2 * h)
    sh = f"M{a} {y}A{fmt(r)} {fmt(r)} 0 0 1 {b} {y}A{fmt(r)} {fmt(r)} 0 0 1 {a} {y}Z"
    return [
        shell(sh, stroke_miterlimit="8"),
        detail(seg(6.5, 16, 11.5, 16)),
        line(L(S, "M15.5 16Q19 15.5 18.5 11", "M15.5 16Q18.5 16 18.5 11")),
        shell(scallop(18.5, 6.5, 2.8, 7, L(S, 0.8, 0.56))),
    ]


def _bobbin(S, cx):
    return [
        line(seg(cx, 4.5, cx, 8)),
        shell(rect(cx - 2, 8, 4, 8.5, L(S, 0.5, 2))),
        dot(cx, 19.25, 1.75),
    ]


@icon("lace-bobbins", CAT, "Two slim wooden lace bobbins with beads on their ends and threads meeting at the top",
      tags=["bobbin lace", "lace making", "bobbins", "pillow lace", "lacework", "thread"])
def _(S):
    return _bobbin(S, 7.5) + _bobbin(S, 16.5) + [
        line(L(S, "M7.5 4.5L12 2L16.5 4.5", "M7.5 4.5Q10 2.5 12 2Q14 2.5 16.5 4.5")),
    ]


def _x(cx, cy, h=1.75):
    return f"M{fmt(cx - h)} {fmt(cy - h)}L{fmt(cx + h)} {fmt(cy + h)}M{fmt(cx - h)} {fmt(cy + h)}L{fmt(cx + h)} {fmt(cy - h)}"


@icon("cross-stitch", CAT, "Square of fabric with a block of four X shaped cross stitches",
      tags=["cross stitch", "counted thread", "embroidery", "needlework", "stitch", "aida"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(_x(8.5, 8.5)), detail(_x(15.5, 8.5)), detail(_x(8.5, 15.5)), detail(_x(15.5, 15.5)),
    ]


def _floss_fill():
    body = rect(2, 8.5, 20, 7, 3.5)
    bands = [rect(6, 7, 3, 10, 0.5), rect(15, 7, 3, 10, 0.5)]
    return D(solid_of([body] + bands), ST("M10.5 14L12 10M12.5 14L14 10", 1.6))


@icon("embroidery-floss", CAT, "Short skein of twisted embroidery thread with two paper bands around it",
      tags=["floss", "embroidery thread", "skein", "stranded cotton", "thread", "needlework"], filled=_floss_fill)
def _(S):
    return [
        line("M6 8.5H5.5A3.5 3.5 0 0 0 5.5 15.5H6"),
        line("M18 8.5H18.5A3.5 3.5 0 0 1 18.5 15.5H18"),
        line(seg(9, 8.5, 15, 8.5)), line(seg(9, 15.5, 15, 15.5)),
        shell(rect(6, 7, 3, 10, L(S, 0.5, 1.5))), shell(rect(15, 7, 3, 10, L(S, 0.5, 1.5))),
        line(seg(11, 13.5, 13, 10.5)),
    ]


@icon("floss-bobbin", CAT, "Flat card with notched ends and embroidery thread wound around its middle",
      tags=["floss card", "thread card", "embroidery", "bobbin", "floss organiser", "floss organizer"])
def _(S):
    card = [(5, 2.5), (10, 2.5), (12, 5), (14, 2.5), (19, 2.5), (19, 21.5), (14, 21.5), (12, 19), (10, 21.5), (5, 21.5)]
    return [
        shell(poly(card, closed=True, r=S.r * 0.5)),
        detail(seg(5, 9.5, 19, 9.5)), detail(seg(5, 14.5, 19, 14.5)),
        line(seg(2.5, 12, 5, 12)), line(seg(19, 12, 21.5, 12)),
    ]


@icon("dye-pot", CAT, "Round dye pot with side handles and a stick lifting out a dripping piece of cloth",
      tags=["dyeing", "fabric dye", "dye bath", "tie dye", "natural dye", "textile"])
def _(S):
    pot = L(S, "M4.5 12H19.5V17.5Q19.5 21.5 15.5 21.5H8.5Q4.5 21.5 4.5 17.5Z",
            "M6 12H18A1.5 1.5 0 0 1 19.5 13.5V17.5Q19.5 21.5 15.5 21.5H8.5Q4.5 21.5 4.5 17.5V13.5A1.5 1.5 0 0 1 6 12Z")
    cloth = L(S, "M11 2.5H16.5V9L15 7.5L13.75 9L12.5 7.5L11 9Z",
              "M11 4A1.5 1.5 0 0 1 12.5 2.5H15A1.5 1.5 0 0 1 16.5 4V9Q15 7 13.75 9Q12.5 7 11 9Z")
    return [
        shell(pot),
        line(seg(2, 14.5, 4.5, 14.5)), line(seg(19.5, 14.5, 22, 14.5)),
        line(seg(7, 10, 13.75, 2.5)),
        shell(cloth, stroke_miterlimit="2"),
        detail(L(S, "M7.5 16.5L9.5 15.5L11.5 16.5L13.5 15.5L15.5 16.5L16.5 16",
                 "M7.5 16.5Q9.5 14.5 11.5 16.5Q13.5 18.5 15.5 16.5")),
    ]


@icon("pincushion", CAT, "Round tomato shaped pincushion with segment lines and pins stuck in the top",
      tags=["pin cushion", "pins", "sewing", "tomato", "notions", "dressmaking"])
def _(S):
    body = L(S, "M3 15.5C3 11.5 7 9.5 12 9.5S21 11.5 21 15.5C21 19 18 20.5 12 20.5S3 19 3 15.5Z",
             ellipse(12, 15, 9, 5.5))
    return [
        shell(body),
        detail("M9 10Q6.5 15 9 20"), detail("M15 10Q17.5 15 15 20"),
        line(seg(12, 9.5, 12, 5)), dot(12, 3.8, 1.6),
        line(seg(7.5, 10.5, 5.5, 7)), dot(4.9, 5.9, 1.6),
        line(seg(16, 10, 17.5, 6)), dot(18, 4.8, 1.6),
    ]


@icon("running-stitch", CAT, "Dashed line of running stitches along a fabric edge with a needle and thread at the end",
      tags=["running stitch", "hand sewing", "stitch", "sewing", "tacking", "basting"])
def _(S):
    eye = rot(ellipse(19, 9, 1.6, 2.8), -45, 19, 9)
    return [
        line(seg(2.5, 16, 5, 16)), line(seg(7.5, 16, 10, 16)), line(seg(12.5, 16, 15, 16)),
        line(L(S, "M20.6 11L21 14L17.5 16", "M20.6 11Q22 16 17.5 16")),
        line(seg(10.5, 2.5, 17.5, 7.5)),
        shell(eye),
        line(seg(2, 20.5, 22, 20.5)),
    ]


@icon("sewing-gauge", CAT, "Short sewing gauge ruler with tick marks and a pointed sliding marker",
      tags=["seam gauge", "hem gauge", "sewing ruler", "measuring", "sliding gauge", "sewing"])
def _(S):
    pts = [(2, 9), (13, 9), (13, 6.5), (18, 6.5), (18, 9), (22, 9), (22, 15), (18, 15), (18, 17), (15.5, 19.5),
           (13, 17), (13, 15), (2, 15)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.6)),
        detail(seg(4.5, 9, 4.5, 12.5)), detail(seg(7.5, 9, 7.5, 11.5)), detail(seg(10.5, 9, 10.5, 12.5)),
        detail(seg(15.5, 9, 15.5, 14)),
    ]


# ============================================================================ woodwork, jewellery and making

@icon("whittling-knife", CAT, "Short whittling knife with a thick rounded wooden handle and a short straight blade",
      tags=["whittling", "carving knife", "wood carving", "woodwork", "sloyd knife", "bushcraft"])
def _(S):
    deg = 45
    blade = rpoly([(10.5, 11), (10.5, 5.5), (13.5, 2), (13.5, 11)], deg, r=S.r * 0.3)
    handle = rpoly([(9.5, 11), (14.5, 11), (15, 22), (9, 22)], deg, r=L(S, 1, 3))
    return [
        shell(blade, stroke_miterlimit="8"),
        shell(handle),
    ]


@icon("dowel-joint", CAT, "Two boards pulled apart with round wooden dowel pegs sticking out of one board toward matching holes",
      tags=["dowel", "dowelling", "doweling", "wood joint", "joinery", "woodwork", "peg"])
def _(S):
    notched = poly([(16, 3.5), (21.5, 3.5), (21.5, 20.5), (16, 20.5), (16, 17.5), (17.5, 17.5), (17.5, 14.5), (16, 14.5),
                    (16, 9.5), (17.5, 9.5), (17.5, 6.5), (16, 6.5)], closed=True, r=S.r * 0.3)
    return [
        shell(rect(2.5, 3.5, 6, 17, L(S, 1, 2))),
        line(seg(8.5, 8, 14.5, 8)), line(seg(8.5, 16, 14.5, 16)),
        shell(notched),
    ]


@icon("wood-glue", CAT, "Squeeze bottle of wood glue with a pointed spout cap and a wood grain label",
      tags=["glue", "pva", "adhesive", "woodwork", "carpenter's glue", "wood adhesive"])
def _(S):
    bottle = poly([(6, 21.5), (6, 11.5), (9, 8.5), (10, 8.5), (10, 6.5), (11.2, 6.5), (12, 3.5), (12.8, 6.5), (14, 6.5),
                   (14, 8.5), (15, 8.5), (18, 11.5), (18, 21.5)], closed=True, r=S.r * 0.6)
    return [
        shell(bottle, stroke_miterlimit="3"),
        detail(L(S, "M8.5 14.5L10.5 13.5L13 15L15.5 14", "M8.5 14.5Q10.5 12.5 12.5 14.5Q14 16 15.5 14")),
        detail(L(S, "M8.5 18.5L10.5 17.5L13 19L15.5 18", "M8.5 18.5Q10.5 16.5 12.5 18.5Q14 20 15.5 18")),
    ]


def _along(pts, deg, ox, oy):
    """Local points (axis pointing up from the origin) turned clockwise by deg and moved to (ox, oy)."""
    return [(ox + x, oy + y) for x, y in rpts(pts, deg, 0, 0)]


@icon("wood-burning-pen", CAT, "Wood burning pen with a hot metal tip drawing a smoking line on a wooden slab",
      tags=["pyrography", "wood burning", "woodburning", "burner pen", "wood art", "craft"])
def _(S):
    deg, ox, oy = 45, 9.5, 15
    tip = poly(_along([(0, 0), (1.5, -4), (-1.5, -4)], deg, ox, oy), closed=True, r=S.r * 0.3)
    grip = poly(_along([(-2, -4), (2, -4), (2, -13), (-2, -13)], deg, ox, oy), closed=True, r=L(S, 0.6, 2))
    return [
        shell(tip, stroke_miterlimit="8"),
        shell(grip),
        shell(rect(2, 17, 20, 4.5, L(S, 1, 2))),
        line(L(S, "M4 13.5L5 12L4 10.5L5 9", "M4 13.5Q5.5 12 4.5 11Q3.5 10 5 8.5")),
    ]


@icon("marquetry", CAT, "Square wooden panel inlaid with a four pointed star of light and dark veneer",
      tags=["inlay", "veneer", "woodwork", "parquetry", "intarsia", "decorative wood"])
def _(S):
    c = 12
    o, w = 7, 2.2
    parts = [shell(rect(2.5, 2.5, 19, 19, S.R))]
    for k, (dx, dy) in enumerate([(0, -1), (1, 0), (0, 1), (-1, 0)]):
        px, py = c + dx * o, c + dy * o
        sx, sy = -dy * w, dx * w
        parts.append(mark(poly([(c, c), (px, py), (c + sx, c + sy)], closed=True, r=L(S, 0, 0.3))))
    parts.append(detail(poly([(c, c - o), (c + w, c - w), (c + o, c), (c + w, c + w), (c, c + o), (c - w, c + w),
                              (c - o, c), (c - w, c - w)], closed=True, r=L(S, 0, 0.5)), stroke_miterlimit="8"))
    return parts


@icon("ring-mandrel", CAT, "Tall tapered ring mandrel with a ring slipped halfway down its cone",
      tags=["ring sizer", "ring stick", "jewellery", "jewelry", "ring size", "metalsmith", "triblet"])
def _(S):
    return [
        shell(poly([(10.3, 2.5), (13.7, 2.5), (17, 21.5), (7, 21.5)], closed=True, r=S.r * 0.4), stroke_miterlimit="3"),
        shell(ellipse(12, 12.5, 6, 2.4)),
    ]


@icon("wire-wrapped-stone", CAT, "Pointed crystal wrapped in spiralling wire with a hanging loop at the top",
      tags=["wire wrapping", "crystal pendant", "jewellery", "jewelry", "pendant", "gemstone", "wire wrap"])
def _(S):
    stone = poly([(8.5, 8), (15.5, 8), (15.5, 16), (12, 21.5), (8.5, 16)], closed=True, r=S.r * 0.6)
    return [
        shell(stone, stroke_miterlimit="6"),
        detail(seg(8.5, 11, 15.5, 13.5)), detail(seg(8.5, 15.5, 15.5, 18)),
        shell(circle(12, 4.5, 2.2)),
    ]


@icon("beading", CAT, "Beading needle and thread with round beads strung along it and a loose bead beside",
      tags=["beads", "bead", "jewellery making", "jewelry making", "stringing", "bracelet", "necklace"])
def _(S):
    return [
        line(seg(2.5, 21.5, 3.9, 20.1)),
        shell(circle(6, 18, 2.3)),
        line(seg(7.6, 16.4, 8.9, 15.1)),
        shell(circle(11, 13, 2.3)),
        line(seg(12.6, 11.4, 18.3, 5.7)),
        shell(rot(ellipse(19.8, 4.2, 1.4, 2.4), 45, 19.8, 4.2)),
        shell(circle(17.5, 17, 2.3)),
    ]


@icon("dipped-candles", CAT, "Pair of hand dipped taper candles hanging from one shared wick looped over a rod",
      tags=["taper candles", "candle dipping", "candle making", "beeswax", "wax", "hand dipped"])
def _(S):
    def taper(cx):
        return L(S, poly([(cx - 0.9, 8.5), (cx + 0.9, 8.5), (cx + 1.8, 21.5), (cx - 1.8, 21.5)], closed=True),
                 f"M{fmt(cx - 0.9)} 8.5H{fmt(cx + 0.9)}L{fmt(cx + 1.8)} 20.3A1.2 1.2 0 0 1 {fmt(cx + 0.6)} 21.5H{fmt(cx - 0.6)}"
                 f"A1.2 1.2 0 0 1 {fmt(cx - 1.8)} 20.3Z")
    return [
        line(seg(3, 3.5, 21, 3.5)),
        line("M8 8.5V6H16V8.5"),
        shell(taper(8)), shell(taper(16)),
    ]


@icon("candle-making", CAT, "Small pouring pitcher with a handle tipping melted wax into a jar that has an upright wick",
      tags=["candle making", "wax", "container candle", "soy wax", "pouring", "candle jar"])
def _(S):
    body = rpoly([(3, 3.5), (11, 3.5), (10, 11.5), (4, 11.5)], 38, r=L(S, 0.6, 1.5), cx=7, cy=7)
    handle = poly(rpts([(3.3, 5), (1.5, 6), (2, 9), (3.7, 10)], 38, 7, 7), r=S.r)
    return [
        shell(rect(10, 14, 11.5, 7.5, L(S, 1.5, 3))),
        line(seg(17, 14, 17, 10.5)),
        shell(body),
        line(handle),
        line("M12.4 9.3Q13.5 11.5 13.5 14"),
    ]


@icon("soap-making", CAT, "Silicone soap mould with two bars inside and one soap bar popped out beside it",
      tags=["soap making", "soap mould", "soap mold", "cold process", "handmade soap", "melt and pour"])
def _(S):
    return [
        shell(rect(2, 3, 12, 18, L(S, 1.5, 3))),
        detail(rect(5, 6, 6, 4.5, L(S, 0, 1.5))), detail(rect(5, 13.5, 6, 4.5, L(S, 0, 1.5))),
        shell(rect(16, 12, 6, 9.5, L(S, 1.5, 3))),
        dot(18, 7.5, 1.5), dot(20.5, 4, 1),
    ]


def _flower(cx, cy):
    return [dot(cx + dx, cy + dy, 1.05) for dx, dy in [(0, -1.4), (1.4, 0), (0, 1.4), (-1.4, 0)]]


@icon("resin-pour", CAT, "Cup pouring a thick stream of resin into a round mould with a pressed flower inside",
      tags=["epoxy", "resin art", "resin casting", "uv resin", "pouring", "mould", "mold"])
def _(S):
    cup = rpoly([(14, 2.5), (20.5, 2.5), (19.5, 9), (15, 9)], 40, r=L(S, 0.6, 1.5), cx=17, cy=6)
    return [
        shell(cup),
        line("M13.3 7.5Q11.5 9.5 11.5 13.5"),
        shell(ellipse(12, 17.5, 9.5, 4)),
    ] + _flower(7.5, 17.5)

# ============================================================================ camera supports and cameras

@icon("tripod", CAT, "Camera tripod with a mounting head on a centre column above three splayed legs",
      tags=["camera stand", "photography", "stand", "three legs", "support", "video"])
def _(S):
    return [
        shell(rect(7.5, 2.5, 9, 4, min(S.R, 1.5))),
        line(seg(12, 6.5, 12, 10)),
        shell(rect(9.5, 10, 5, 3, min(S.R, 1))),
        line(seg(10.5, 13, 4.5, 21.5)), line(seg(12, 13, 12, 21.5)), line(seg(13.5, 13, 19.5, 21.5)),
    ]


@icon("monopod", CAT, "Single telescoping camera pole with a small mounting plate on top and a rubber foot",
      tags=["camera pole", "unipod", "photography", "support", "stand", "stick"])
def _(S):
    return [
        shell(rect(7.5, 2.5, 9, 3, L(S, 0.5, 1.5))),
        shell(rect(10, 5.5, 4, 8.5, L(S, 0.5, 2))),
        line(seg(12, 14, 12, 19)),
        shell(L(S, "M10.5 19H13.5L14.5 21.5H9.5Z", "M11.5 19H12.5A2 2 0 0 1 14.5 21H9.5A2 2 0 0 1 11.5 19Z")),
    ]


@icon("gimbal", CAT, "Handheld gimbal stabiliser with a bent arm holding a phone upright above a grip handle",
      tags=["stabilizer", "stabiliser", "steady", "phone gimbal", "video", "vlog", "handheld"])
def _(S):
    return [
        shell(rect(10, 2.5, 9, 11.5, L(S, 1.5, 3))),
        line(L(S, "M10 8.5H5.5V16H12", "M10 8.5H6.5Q5.5 8.5 5.5 9.5V16H12")),
        shell(rect(11.5, 14.5, 5, 7, L(S, 1, 2.5))),
        dot(14.5, 11, 1),
    ]


@icon("twin-lens-camera", CAT, "Tall box camera with two round lenses stacked one above the other and a folding hood",
      tags=["tlr", "twin lens reflex", "medium format", "vintage camera", "film camera", "retro camera"])
def _(S):
    return [
        line(L(S, "M6.5 6V2.5H17.5V6", "M6.5 6L7.5 2.5H16.5L17.5 6")),
        shell(rect(5, 6, 14, 15.5, S.R)),
        detail(circle(12, 10.5, 2.3)),
        detail(circle(12, 17, 2.3)),
    ]


@icon("view-camera", CAT, "Large format view camera with a lens board and a back joined by folding bellows on a rail",
      tags=["large format", "bellows camera", "field camera", "4x5", "vintage camera", "film camera"])
def _(S):
    return [
        shell(rect(4, 7, 3, 9, min(S.R, 1))),
        line(seg(2, 11.5, 4, 11.5)),
        line(L(S, "M7 8L9 5.5L11 7L13 4.5L15 6L17 3.5", "M7 8Q8.5 5 9.5 6.5Q11 8 11.5 5.5Q12.5 3 13.5 5Q15 7 15.5 4.5L17 3.5")),
        line(L(S, "M7 15L9 17.5L11 16L13 18.5L15 17L17 19.5", "M7 15Q8.5 18 9.5 16.5Q11 15 11.5 17.5Q12.5 20 13.5 18Q15 16 15.5 18.5L17 19.5")),
        shell(rect(17, 2.5, 4, 18, min(S.R, 1))),
        line(seg(5.5, 16, 5.5, 21.5)), line(seg(19, 20.5, 19, 21.5)),
        line(seg(2.5, 21.5, 21.5, 21.5)),
    ]


def _pinhole_fill():
    box = D(solid_of([rect(10, 4, 11.5, 16)]), P(rect(8.5, 11, 3, 2)), ST("M17 8.5V15.5M15 13.5L17 15.5L19 13.5", 2))
    return U(box, ST("M3.5 8L10 12L3.5 16", 2.5, "butt", "miter", 4.0))


@icon("pinhole-camera", CAT, "Closed box camera with a tiny hole in the front and light rays passing through it",
      tags=["camera obscura", "pinhole", "optics", "light rays", "diy camera", "physics"], filled=_pinhole_fill)
def _(S):
    return [
        line(poly([(10, 11), (10, 4), (21.5, 4), (21.5, 20), (10, 20), (10, 13)], r=S.r)),
        line(L(S, "M3.5 8L10 12L3.5 16", "M3.5 8L10 12L3.5 16")),
        line(L(S, "M17 8.5V15.5M15 13.5L17 15.5L19 13.5", "M17 8.5V15.5M15 13.5L17 15.5L19 13.5")),
    ]


@icon("action-camera", CAT, "Small cube action camera with a large round lens off centre and a mounting clip below",
      tags=["sports camera", "helmet camera", "pov camera", "waterproof camera", "video", "adventure"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 13.5, S.R)),
        detail(circle(15, 10.25, 3.3)),
        detail(rect(5.5, 6.5, 3.5, 2, 0) if S.name == "line" else rect(5.5, 6.5, 3.5, 2, 1)),
        shell(L(S, "M9.5 17H14.5V21.5H9.5Z", "M9.5 17H14.5V20A1.5 1.5 0 0 1 13 21.5H11A1.5 1.5 0 0 1 9.5 20Z")),
    ]


@icon("telephoto-lens", CAT, "Long telephoto camera lens with a narrow mount, zoom ring and wide front hood",
      tags=["zoom lens", "long lens", "telephoto", "camera lens", "wildlife photography", "sports photography"])
def _(S):
    pts = [(2, 10), (4.5, 10), (4.5, 8), (15.5, 8), (15.5, 5), (22, 5), (22, 19), (15.5, 19), (15.5, 16), (4.5, 16),
           (4.5, 14), (2, 14)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.6)),
        detail(seg(8.5, 8, 8.5, 16)), detail(seg(12, 8, 12, 16)),
    ]


@icon("fisheye-lens", CAT, "Short camera lens with a big bulging dome of glass on its front",
      tags=["fisheye", "wide angle", "ultra wide", "camera lens", "180 degree", "distortion"])
def _(S):
    return [
        shell(L(S, "M3.5 13.5A8.5 8.5 0 0 1 20.5 13.5Z", "M3.5 13.5A8.5 8.5 0 0 1 20.5 13.5Z")),
        shell(rect(5.5, 13.5, 13, 5, min(S.R, 1.5))),
        shell(rect(7.5, 18.5, 9, 3, min(S.R, 1))),
        detail(arc(12, 13.5, 5, 215, 260)),
    ]


@icon("lens-cap", CAT, "Round lens cap with pinch grip tabs on each side and a raised ring on its face",
      tags=["lens cover", "camera cap", "cap", "lens protection", "photography", "accessory"])
def _(S):
    return [
        shell(circle(12, 12, 9.5)),
        detail(circle(12, 12, 4.5)),
        detail(L(S, "M6 9.5L4.5 12L6 14.5", "M6 9.5Q4.2 12 6 14.5")),
        detail(L(S, "M18 9.5L19.5 12L18 14.5", "M18 9.5Q19.8 12 18 14.5")),
    ]


@icon("lens-hood", CAT, "Front view of a petal shaped lens hood with four shallow curved cutouts around a round glass opening",
      tags=["lens shade", "petal hood", "tulip hood", "flare", "camera lens", "accessory"])
def _(S):
    return [
        shell("M3.5 3.5Q12 6.5 20.5 3.5Q17.5 12 20.5 20.5Q12 17.5 3.5 20.5Q6.5 12 3.5 3.5Z", stroke_miterlimit="6"),
        detail(circle(12, 12, 3.8)),
    ]


@icon("lens-filter", CAT, "Thin threaded filter ring holding a round glass disc with glare lines across it",
      tags=["uv filter", "nd filter", "polariser", "polarizer", "camera filter", "lens filter", "glass"])
def _(S):
    return [
        shell(circle(12, 12, 9.5)),
        detail(circle(12, 12, 6.5)),
        detail(L(S, "M8.5 13L13 8.5", "M8.5 13L13 8.5")), detail(seg(10.5, 15.5, 15.5, 10.5)),
    ]


@icon("lens-blower", CAT, "Rubber bulb air blower with a tapered nozzle puffing air to clean a lens",
      tags=["air blower", "rocket blower", "dust blower", "sensor cleaning", "lens cleaning", "camera care"])
def _(S):
    return [
        shell(L(S, "M12 10.5C16 10.5 18 13.5 18 16.5C18 19.8 15.5 21.5 12 21.5S6 19.8 6 16.5C6 13.5 8 10.5 12 10.5Z",
                ellipse(12, 16, 6, 5.5))),
        shell(poly([(10, 10.5), (14, 10.5), (12.8, 6), (11.2, 6)], closed=True, r=S.r * 0.4)),
        line(seg(12, 2, 12, 4)),
        line(seg(8.5, 2.5, 9.5, 4)), line(seg(15.5, 2.5, 14.5, 4)),
    ]


@icon("camera-bag", CAT, "Boxy padded camera shoulder bag with a front flap, a lens badge and a strap",
      tags=["camera case", "gadget bag", "photo bag", "shoulder bag", "photography", "kit bag"])
def _(S):
    return [
        line(L(S, "M5 9V3.5H19V9", "M5 9V5A1.5 1.5 0 0 1 6.5 3.5H17.5A1.5 1.5 0 0 1 19 5V9")),
        shell(rect(2.5, 9, 19, 12.5, S.R)),
        detail(L(S, "M2.5 12.5H21.5", "M2.5 12.5H21.5")),
        detail(circle(12, 16.5, 2)),
    ]


@icon("film-canister", CAT, "Short film cartridge with a spool knob on top and a strip of film leader from its side",
      tags=["35mm film", "film roll", "film cartridge", "analog", "analogue", "film photography"])
def _(S):
    return [
        shell(rect(9.5, 2.5, 4, 3, min(S.R, 1))),
        shell(rect(3, 5.5, 11, 16, min(S.R, 2.5))),
        shell(L(S, "M14 9H21.5V17.5H14", "M14 9H18Q21.5 9 21.5 12.5V17.5H14")),
        mark(rect(16, 10.5, 1.8, 1.5)), mark(rect(16, 15, 1.8, 1.5)),
    ]


# ============================================================================ more fibre crafts and making

def earc(cx, cy, rx, ry, a0, a1, deg=0.0, n=10):
    """Points along an elliptical arc (angles in degrees), then turned clockwise by deg about the centre."""
    pts = [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
            cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    return rpts(pts, deg, cx, cy)


def rq(p0, c, p1, deg, n=8):
    """Open quadratic curve (p0, control c, p1) turned by deg about (12, 12), as a polyline d-string."""
    pts = [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0],
            (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1]) for t in (i / n for i in range(n + 1))]
    return poly(rpts(pts, deg))


def star(cx, cy, ro, ri, n):
    pts = []
    for i in range(2 * n):
        r = ro if i % 2 == 0 else ri
        pts.append(polar(cx, cy, r, -90 + i * 180 / n))
    return pts


@icon("tufting-gun", CAT, "Pistol grip tufting gun with a slanted needle nose pushing yarn into a cloth",
      tags=["tufting", "rug tufting", "rug making", "yarn gun", "carpet", "textile art", "diy rug"])
def _(S):
    return [
        shell(rect(6, 3, 15, 6.5, L(S, 2, 3.25))),
        shell(poly([(15, 9.5), (20.5, 9.5), (19, 19), (14.5, 19)], closed=True, r=S.r * 0.6)),
        line(seg(8.5, 9.5, 5, 17)),
        line(seg(2, 19.5, 9, 19.5)),
        line("M2.5 21.5H8.5"),
    ]


@icon("quilting-ruler", CAT, "Clear quilting ruler with a diagonal line and tick marks, and a rotary cutter beside it",
      tags=["quilting", "rotary cutter", "patchwork", "cutting mat", "fabric cutting", "sewing", "ruler"])
def _(S):
    cutter = union(circle(19, 6.5, 2.8), rect(17, 9, 4, 12.5, L(S, 0.5, 2)))
    return [
        shell(rect(2.5, 2.5, 11, 19, L(S, 1, 2.5))),
        detail(seg(2.5, 7, 5.5, 7)), detail(seg(2.5, 12, 5.5, 12)), detail(seg(2.5, 17, 5.5, 17)),
        detail(seg(8, 19, 11, 5)),
        shell(cutter),
    ]


@icon("buttonhole", CAT, "Square of fabric with a buttonhole slit and stitches crossing it above and below",
      tags=["button hole", "sewing", "satin stitch", "tailoring", "garment", "fabric", "slit"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        mark(rect(6.5, 11, 11, 2, L(S, 0, 1))),
        detail(seg(8.5, 6.5, 8.5, 9)), detail(seg(12, 6.5, 12, 9)), detail(seg(15.5, 6.5, 15.5, 9)),
        detail(seg(8.5, 15, 8.5, 17.5)), detail(seg(12, 15, 12, 17.5)), detail(seg(15.5, 15, 15.5, 17.5)),
    ]


@icon("iron-on-transfer", CAT, "Clothes iron pressing a square transfer sheet onto a flat t-shirt",
      tags=["heat transfer", "iron on", "htv", "t-shirt printing", "vinyl", "pressing", "custom shirt"])
def _(S):
    tee = [(8, 11), (3, 13.5), (5, 17.5), (7, 16.5), (7, 21.5), (17, 21.5), (17, 16.5), (19, 17.5), (21, 13.5), (16, 11)]
    return [
        line(L(S, "M12 4.5V2.5H19.5V4.5", "M12 4.5V3.5A1 1 0 0 1 13 2.5H18.5A1 1 0 0 1 19.5 3.5V4.5")),
        shell(poly([(2.5, 8), (8, 4.5), (21.5, 4.5), (21.5, 8)], closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
        shell(poly(tee, closed=True, r=S.r * 0.6)),
        detail(rect(10, 14.5, 4, 4, 0)),
    ]


@icon("chip-carving", CAT, "Round wooden plate with a rosette of triangular chip cuts arranged in a circle",
      tags=["wood carving", "woodcarving", "rosette", "carved plate", "geometric carving", "woodwork", "knife carving"])
def _(S):
    parts = [shell(circle(12, 12, 9.5))]
    for i in range(6):
        a = -90 + i * 60
        tip = polar(12, 12, 3.2, a)
        b1, b2 = polar(12, 12, 7.3, a - 14), polar(12, 12, 7.3, a + 14)
        parts.append(mark(poly([tip, b1, b2], closed=True, r=L(S, 0, 0.5))))
    parts.append(dot(12, 12, 1.1))
    return parts


@icon("leather-punch", CAT, "Rotary leather punch: pincer handles with a round wheel of punch holes at the jaw",
      tags=["hole punch", "leatherwork", "leather craft", "belt punch", "revolving punch", "pliers", "leather tool"])
def _(S):
    deg = 45
    hole = lambda x, y: dot(*rpts([(x, y)], deg)[0], 1.0)
    h1 = rq((10.5, 13), (9.5, 17), (8, 21.5), deg) if S.name == "rounded" else rseg(10.5, 13, 8, 21.5, deg)
    h2 = rq((13.5, 13), (14.5, 17), (16, 21.5), deg) if S.name == "rounded" else rseg(13.5, 13, 16, 21.5, deg)
    return [
        shell(rot(circle(12, 5.2, 4.4), deg)),
        hole(12, 3.3), hole(13.7, 6.2), hole(10.3, 6.2),
        shell(rpoly([(10.5, 9.6), (13.5, 9.6), (13.5, 13), (10.5, 13)], deg, closed=True, r=S.r * 0.4)),
        line(h1), line(h2),
    ]


# ============================================================================ studio lighting

@icon("softbox", CAT, "Softbox light: a large rectangular diffuser tapering back to a light head, on a stand",
      tags=["studio light", "diffuser", "photography lighting", "strobe", "portrait lighting", "video light", "light modifier"])
def _(S):
    return [
        shell(poly([(21, 2.5), (21, 13.5), (9.5, 11.5), (9.5, 4.5)], closed=True, r=S.r * 0.6)),
        detail(seg(17.5, 5.5, 17.5, 10.5)),
        shell(rect(4, 6.5, 5.5, 3.5, L(S, 0.5, 1.5))),
        line(seg(14, 13, 14, 21.5)),
        line(seg(14, 17.5, 9, 21.5)), line(seg(14, 17.5, 19, 21.5)),
    ]


@icon("photo-umbrella", CAT, "Open photography umbrella tilted toward a flash head that points into it on a light stand",
      tags=["umbrella light", "reflective umbrella", "shoot through umbrella", "flash", "studio lighting", "portrait", "speed light"])
def _(S):
    cx, cy, R = 14.5, 9, 7.5
    deg = 45
    canopy = f"M{cx - R} {cy}A{R} {R} 0 0 1 {cx + R} {cy}Z"
    return [
        shell(rot(canopy, deg, cx, cy)),
        line(rseg(cx, cy, cx, cy + 6.5, deg, cx, cy)),
        shell(rect(2.5, 12.5, 6.5, 4.5, L(S, 0.5, 2))),
        line(seg(5.75, 17, 5.75, 21.5)),
        line(seg(5.75, 19.5, 3, 21.5)), line(seg(5.75, 19.5, 8.5, 21.5)),
    ]


@icon("reflector-disc", CAT, "Round collapsible photo reflector disc with a rim and a curved shine streak, tilted on an angle",
      tags=["photography reflector", "5 in 1 reflector", "light bounce", "fill light", "silver reflector", "diffuser", "studio"])
def _(S):
    return [
        shell(rot(ellipse(12, 12, 10, 7), -35)),
        detail(poly(earc(12, 12, 6, 3.4, 150, 255, -35), r=S.r * 0.5)),
    ]


@icon("studio-backdrop", CAT, "Two stands holding a crossbar with a paper backdrop rolling down toward the floor",
      tags=["photo backdrop", "background paper", "seamless paper", "backdrop stand", "photo studio", "portrait studio", "muslin"])
def _(S):
    return [
        line(seg(3.5, 3.5, 3.5, 21.5)), line(seg(20.5, 3.5, 20.5, 21.5)),
        line(seg(1.5, 21.5, 5.5, 21.5)), line(seg(18.5, 21.5, 22.5, 21.5)),
        line(seg(2.5, 3.5, 21.5, 3.5)),
        shell(L(S, "M7 6H17V17Q17 20.5 13 20.5H9Q7 20.5 7 18Z", "M7 6H17V17Q17 20.5 13 20.5H9Q7 20.5 7 18Z")),
    ]


@icon("light-stand", CAT, "Tall light stand with a clamp and a flared light head on top, on a three legged base",
      tags=["lighting stand", "c stand", "studio stand", "flash stand", "photography", "video lighting", "tripod base"])
def _(S):
    return [
        shell(poly([(9, 2.5), (15, 2.5), (19, 8), (5, 8)], closed=True, r=S.r * 0.6)),
        line(seg(12, 8, 12, 21.5)),
        shell(rect(10.5, 11.5, 3, 3, L(S, 0, 1))),
        line(seg(12, 17.5, 5.5, 21.5)), line(seg(12, 17.5, 18.5, 21.5)),
    ]


@icon("beauty-dish", CAT, "Shallow round beauty dish reflector with a small deflector plate on a stem in its centre",
      tags=["reflector dish", "portrait light", "fashion lighting", "studio light", "light modifier", "strobe", "photography"])
def _(S):
    return [
        shell("M12 3A7 9 0 0 0 12 21Z"),
        line(seg(6, 12, 16.5, 12)),
        shell(rect(16, 7.5, 3.5, 9, L(S, 0.5, 1.75))),
    ]


@icon("light-tent", CAT, "Cube shaped fabric light tent with an open front and a small product bottle sitting inside",
      tags=["photo tent", "lightbox", "light box", "product photography", "diffusion cube", "shooting tent", "studio"])
def _(S):
    bottle = union(rect(6.5, 15, 6, 6, L(S, 0.5, 1.5)), rect(8.5, 12, 2, 3.5))
    return [
        shell(poly([(3, 8.5), (8, 3), (21, 3), (21, 15.5), (16, 21.5), (3, 21.5)], closed=True, r=S.r)),
        detail(poly([(3, 8.5), (16, 8.5), (16, 21.5)], r=S.r * 0.7)),
        detail(seg(16, 8.5, 21, 3)),
        mark(bottle),
    ]


@icon("camera-slider", CAT, "Camera slider rail on short legs with a camera sitting on a sliding carriage",
      tags=["dolly", "motion control", "video slider", "track", "filmmaking", "timelapse rail", "cinematography"])
def _(S):
    return [
        shell(rect(6, 2.5, 12, 7.5, L(S, 1.5, 3))),
        detail(circle(12, 6.25, 1.5)),
        line(seg(9.5, 10, 9.5, 14.5)), line(seg(14.5, 10, 14.5, 14.5)),
        shell(rect(2.5, 14.5, 19, 3.5, L(S, 1, 1.75))),
        line(seg(5, 18, 5, 21.5)), line(seg(19, 18, 19, 21.5)),
    ]


@icon("cable-release", CAT, "Coiled camera cable release with a threaded tip on one end and a plunger button on the other",
      tags=["remote shutter", "shutter release", "remote release", "long exposure", "cable", "plunger", "camera accessory"])
def _(S):
    return [
        line(seg(4.5, 5, 4.5, 8)),
        shell(rect(2, 8, 5, 8, L(S, 0.5, 2))),
        line(L(S, "M7 12Q9 4 11 12T15 12T17.5 12", "M7 12Q9 4 11 12T15 12T17.5 12")),
        shell(rect(17.5, 10.5, 4.5, 3, L(S, 0, 1))),
        detail(seg(19, 10.5, 19, 13.5)),
    ]


@icon("flash-bulb", CAT, "Vintage flash bulb unit with a round dish reflector, a bulb in the centre and a short handle",
      tags=["flashbulb", "vintage flash", "press camera flash", "old camera", "flashgun", "retro photography", "strobe"])
def _(S):
    bulb = "M12 4.3A2.8 2.8 0 0 1 13.6 9.4V11.2H10.4V9.4A2.8 2.8 0 0 1 12 4.3Z"
    return [
        shell(union(circle(12, 9, 7.5), rect(10, 14, 4, 7.5, L(S, 0.5, 1.5)))),
        mark(bulb),
    ]


@icon("photo-enlarger", CAT, "Darkroom photo enlarger: a column with a lamp head and bellows pointing down at the baseboard",
      tags=["darkroom", "enlarging", "print making", "darkroom printing", "analogue photography", "analog photography", "film printing"])
def _(S):
    return [
        line(seg(4.5, 3, 4.5, 19)),
        line(seg(4.5, 5.5, 8.5, 5.5)),
        shell(rect(8.5, 3, 11, 5, L(S, 1, 2))),
        shell(poly([(10, 8), (18, 8), (16.5, 13), (11.5, 13)], closed=True, r=S.r * 0.4)),
        shell(rect(12, 13, 4, 2.5, L(S, 0, 1))),
        shell(rect(2, 19, 20, 2.5, L(S, 1, 1.25))),
    ]


@icon("developing-tray", CAT, "Shallow photo developing tray with ripples in the liquid and a print sheet dipping in",
      tags=["darkroom tray", "chemical tray", "print developing", "darkroom", "analogue photography", "analog photography", "fixer bath"])
def _(S):
    return [
        shell(rot(rect(11, 2.5, 7, 9, L(S, 0.5, 1.5)), 12, 14.5, 7)),
        shell(poly([(2.5, 11), (21.5, 11), (19.5, 20.5), (4.5, 20.5)], closed=True, r=S.r * 0.8)),
        detail(L(S, "M7 15.5L9 14L11 15.5L13 14L15 15.5L17 14", "M7 15.5Q9 13.5 11 15.5T15 15.5T18 14.5")),
    ]


@icon("safelight", CAT, "Darkroom safelight: a box lamp hanging from a hook with a glowing window and light rays below",
      tags=["darkroom lamp", "red light", "darkroom", "amber light", "photo lab", "analogue photography", "analog photography"])
def _(S):
    return [
        line(seg(12, 2, 12, 4.5)),
        shell(rect(3, 4.5, 18, 11, L(S, 1.5, 3.5))),
        mark(rect(6.5, 8, 11, 4.5, L(S, 0, 1.5))),
        line(seg(6.5, 18.5, 4, 21.5)), line(seg(12, 18.5, 12, 21.5)), line(seg(17.5, 18.5, 20, 21.5)),
    ]


@icon("developing-tank", CAT, "Round lidded film developing tank beside a spiral reel holding a wound film strip",
      tags=["film tank", "film developing", "darkroom", "reel", "analogue photography", "analog photography"])
def _(S):
    return [
        shell(rect(3.5, 3, 8, 3.5, L(S, 1, 1.75))),
        shell(rect(2.5, 6.5, 10, 15, L(S, 1.5, 3))),
        shell(circle(17.5, 15, 4.5)),
        dot(17.5, 15, 1.4),
    ]


@icon("slide-mount", CAT, "Square slide mount frame with a rectangular window showing a small mountain picture",
      tags=["photo slide", "35mm slide", "transparency", "diapositive", "projector slide", "film slide", "retro photography"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, L(S, 1.5, 3.5))),
        detail(rect(6, 6, 12, 12, 0)),
        mark(poly([(8, 15.5), (11, 10.5), (13.5, 14), (15, 12), (17, 15.5)], closed=True, r=L(S, 0, 0.4))),
    ]


@icon("photo-strip", CAT, "Tall strip of three square photo frames like a photo booth strip",
      tags=["photo booth", "photobooth", "photo booth strip", "snapshots", "four frames", "film strip", "memories"])
def _(S):
    return [
        shell(rect(5, 1.5, 14, 21, L(S, 1.5, 3))),
        mark(rect(8.5, 4.5, 7, 4, L(S, 0, 1))),
        mark(rect(8.5, 10, 7, 4, L(S, 0, 1))),
        mark(rect(8.5, 15.5, 7, 4, L(S, 0, 1))),
    ]


@icon("green-screen", CAT, "Green screen backdrop panel on two stands with a person silhouette in front of it",
      tags=["chroma key", "chromakey", "video backdrop", "greenscreen", "virtual background", "compositing", "filmmaking"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 13.5, L(S, 1.5, 3))),
        dot(12, 6.5, 2),
        mark(L(S, "M8 13.5V11Q8 9.5 12 9.5Q16 9.5 16 11V13.5Z", "M8 13.5V11Q8 9.5 12 9.5Q16 9.5 16 11V13.5Z")),
        line(seg(6, 16, 6, 21.5)), line(seg(18, 16, 18, 21.5)),
        line(seg(3.5, 21.5, 8.5, 21.5)), line(seg(15.5, 21.5, 20.5, 21.5)),
    ]


# ============================================================================ photo effects and collecting

@icon("panorama", CAT, "Very wide curved picture frame with a mountain skyline running across it",
      tags=["panoramic photo", "wide shot", "wide angle", "landscape photo", "pano", "stitched photo", "camera mode"])
def _(S):
    return [
        shell("M2 7.5Q12 3.5 22 7.5V16.5Q12 20.5 2 16.5Z" if S.name == "line" else "M2 8Q12 3.5 22 8V16Q12 20.5 2 16Z"),
        detail(poly([(5, 15), (9, 10.5), (12, 13.5), (15, 10), (19, 15)], r=S.r)),
    ]


@icon("timelapse", CAT, "Stopwatch face with a stack of small picture frames fanning out behind it",
      tags=["time lapse", "interval shooting", "interval timer", "speed up", "video effect", "sequence", "frames"])
def _(S):
    return [
        line(poly([(16.5, 6), (21.5, 6), (21.5, 18), (17.5, 18)])),
        line(poly([(14.5, 3.5), (18.5, 3.5)])),
        shell(circle(10.5, 14, 7.5)),
        line(seg(10.5, 4.5, 10.5, 6.5)),
        detail(poly([(10.5, 9.5), (10.5, 14), (13.5, 14)], r=S.r * 0.4)),
    ]


@icon("self-timer", CAT, "Camera body with a small countdown clock face above its corner",
      tags=["camera timer", "countdown", "delay", "timed shot", "selfie timer", "group photo", "timer"])
def _(S):
    return [
        shell(rect(2.5, 11.5, 14, 10, L(S, 1.5, 3))),
        detail(circle(9.5, 16.5, 2)),
        shell(circle(17.5, 6.5, 4.5)),
        detail(poly([(17.5, 4.2), (17.5, 6.5), (19.3, 6.5)])),
    ]


@icon("white-balance", CAT, "A sun with short rays at the top left and a light bulb at the bottom right",
      tags=["wb", "colour temperature", "color temperature", "kelvin", "camera setting", "tint", "photo editing"])
def _(S):
    rays = []
    for k in range(8):
        a = k * 45
        x1, y1 = polar(6.5, 6.5, 3.7, a)
        x2, y2 = polar(6.5, 6.5, 5.0, a)
        rays.append(line(seg(x1, y1, x2, y2)))
    bulb = union(circle(16, 13.5, 4.6), rect(14, 17, 4, 4.5, L(S, 0.5, 1.5)))
    return [
        dot(6.5, 6.5, 2),
        *rays,
        shell(bulb),
        detail(seg(14.2, 19.5, 17.8, 19.5)),
    ]


@icon("tripod-head", CAT, "Camera tripod ball head with a quick release plate on top, a round ball, a lock knob and a base",
      tags=["ball head", "pan tilt head", "quick release plate", "camera mount", "tripod", "photography", "support"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 3.5, L(S, 0.5, 1.75))),
        line(seg(12, 6, 12, 8.5)),
        shell(circle(12, 12, 3.5)),
        line(seg(15.5, 12, 18, 12)),
        shell(rect(17.5, 9.5, 3.5, 5, L(S, 0.5, 1.75))),
        shell(rect(9.5, 16, 5, 5.5, L(S, 0.5, 2))),
    ]


@icon("stamp-tongs", CAT, "Long thin stamp tongs with flat spade tips holding a small postage stamp",
      tags=["philately", "tweezers", "stamp collecting", "stamp collector", "stamp tweezers", "postage stamp", "hobby"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 4.5)),
        line("M12 4.5L8 9.5L8.5 12.5"),
        line("M12 4.5L16 9.5L15.5 12.5"),
        shell(rect(6, 12.5, 12, 9, L(S, 0.5, 2))),
        detail(rect(9.5, 15.5, 5, 3, 0)),
    ]


@icon("display-dome", CAT, "Glass bell dome cloche on a round base with a small object inside",
      tags=["cloche", "bell jar", "glass dome", "museum display", "collectible display", "cover", "showcase"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 4.5)),
        shell(L(S, "M4.5 17V13A7.5 8.5 0 0 1 19.5 13V17Z", "M4.5 17V12.5A7.5 8 0 0 1 19.5 12.5V17Z")),
        shell(rect(2.5, 17, 19, 4.5, L(S, 1, 2.25))),
        dot(12, 13, 2.2),
    ]


@icon("trading-card", CAT, "Portrait trading card with a picture panel at the top and two stat lines below",
      tags=["collectible card", "card game", "tcg", "sports card", "baseball card", "rarity", "card collecting"])
def _(S):
    return [
        shell(rect(5, 3, 14, 18, L(S, 1.5, 3))),
        mark(rect(8, 6, 8, 5, L(S, 0, 1))),
        detail(seg(8, 14.5, 16, 14.5)),
        detail(seg(8, 17.5, 13, 17.5)),
    ]


@icon("comic-book", CAT, "Upright comic book with a title bar on the cover and a starburst burst below it",
      tags=["comics", "graphic novel", "manga", "superhero", "issue", "pulp", "collectible comic"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, L(S, 1, 2.5))),
        mark(rect(8, 5.5, 8, 2.5, L(S, 0, 0.8))),
        mark(poly(star(12, 14.5, 4.5, 2.2, 7), closed=True, r=L(S, 0, 0.4))),
    ]


@icon("enamel-pin", CAT, "Rounded enamel pin badge with a bold outline and a star, with its clutch back peeking out behind",
      tags=["lapel pin", "badge", "pin badge", "pin collecting", "merch", "flair", "hard enamel"])
def _(S):
    front = rect(2.5, 2.5, 14, 14, L(S, 3, 7))
    back = minus(circle(17, 17, 4.5), rect(1, 1, 17, 17, L(S, 4, 8)))
    return [
        shell(front),
        shell(back),
        mark(poly(star(9.5, 9.7, 3.6, 1.6, 5), closed=True, r=L(S, 0, 0.3))),
    ]


@icon("souvenir-spoon", CAT, "Small ornate souvenir spoon with a decorative crest shield at the top of its handle",
      tags=["collector spoon", "tourist spoon", "crest", "keepsake", "silverware", "memento", "collectible"])
def _(S):
    deg = 45
    crest = rpoly([(8.5, 2.5), (15.5, 2.5), (15.5, 6), (12, 9), (8.5, 6)], deg, closed=True, r=S.r * 0.6)
    return [
        shell(crest, stroke_miterlimit="3"),
        line(rseg(12, 9, 12, 14, deg)),
        shell(rot(ellipse(12, 18, 3.4, 4.4), deg)),
    ]


@icon("porcelain-doll", CAT, "Porcelain doll with a round face, ringlet curls at each side and a bell shaped dress",
      tags=["antique doll", "bisque doll", "collectible doll", "vintage doll", "toy", "dress", "figurine"])
def _(S):
    return [
        shell(union(circle(12, 6, 3.7), circle(6.8, 9.3, 1.7), circle(17.2, 9.3, 1.7))),
        shell("M9.5 12H14.5L20 21.5H4Z", stroke_miterlimit="3"),
        detail(seg(9, 16, 15, 16)),
    ]


@icon("metal-detector", CAT, "Metal detector with an armrest, a grip, a long slanted shaft and a flat round search coil",
      tags=["treasure hunting", "detectorist", "prospecting", "beach combing", "coin hunting", "search coil", "hobby"])
def _(S):
    return [
        shell(rect(9.5, 2.5, 10, 3.5, L(S, 1, 1.75))),
        line(L(S, "M4 4.5Q3.5 10 9 10", "M4 4.5Q3.5 10 9 10")),
        line(seg(12, 6, 15, 16)),
        shell(ellipse(15.5, 18.5, 6.5, 3)),
    ]


@icon("flower-press", CAT, "Flower press of two wooden boards joined by bolts at each side with a pressed flower between them",
      tags=["pressed flowers", "botanical press", "herbarium", "drying flowers", "plant press", "nature craft", "wing nut"])
def _(S):
    return [
        line(seg(5.5, 2, 5.5, 18)), line(seg(18.5, 2, 18.5, 18)),
        shell(rect(2.5, 4.5, 19, 4, L(S, 1, 2))),
        shell(rect(2.5, 17.5, 19, 4, L(S, 1, 2))),
        line(seg(12, 16, 12, 13)),
        dot(12, 11.8, 1.7),
        line(seg(12, 14.5, 9.8, 13)), line(seg(12, 14.5, 14.2, 13)),
    ]


@icon("rock-painting", CAT, "Smooth oval pebble painted as a ladybug with a dividing line and dots on its back",
      tags=["painted rocks", "stone painting", "kindness rocks", "pebble art", "ladybug", "craft", "kids craft"])
def _(S):
    return [
        shell(rot(ellipse(12, 12, 10, 7.5), -15) if S.name == "line" else "M3 12C3 7 8 4.5 13 4.5C18 4.5 21.5 8 21.5 12.5C21.5 17 17 19.5 11.5 19.5C6 19.5 3 16.5 3 12Z"),
        detail(seg(12.5, 7.5, 12.5, 16.5)),
        dot(10, 10, 1), dot(15, 10, 1), dot(10, 14.5, 1), dot(15, 14.5, 1),
    ]
