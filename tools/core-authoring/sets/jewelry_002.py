"""TypeIcon Core: jewelry bench tools, trade items and finished-piece packaging (batch 002)."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "jewelry"


def rot(pts, deg=45, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rp(pts, closed=True, r=0.0, deg=45):
    return poly(rot(pts, deg), closed=closed, r=r)


def rseg(x1, y1, x2, y2, deg=45):
    (a, b), (c, d) = rot([(x1, y1), (x2, y2)], deg)
    return seg(a, b, c, d)


def rpath(cmds, deg=45):
    out = []

    def pt(p):
        q = rot([p], deg)[0]
        return f"{fmt(q[0])} {fmt(q[1])}"
    for c in cmds:
        op = c[0]
        if op in ("M", "L"):
            out.append(op + pt(c[1]))
        elif op == "A":
            out.append(f"A{fmt(c[1])} {fmt(c[1])} 0 {c[2]} {c[3]} " + pt(c[4]))
        elif op == "Q":
            out.append("Q" + pt(c[1]) + " " + pt(c[2]))
        elif op == "C":
            out.append("C" + pt(c[1]) + " " + pt(c[2]) + " " + pt(c[3]))
        elif op == "Z":
            out.append("Z")
    return "".join(out)


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    return Part("dot", rect(x, y, w, h, rx))


def gem_pts(cx, cy, w, h):
    """Brilliant-cut gem seen from the side: flat table, wide girdle, pointed pavilion."""
    return [(cx - w * 0.5, cy - h * 0.5), (cx + w * 0.5, cy - h * 0.5), (cx + w, cy - h * 0.5 + h * 0.4), (cx, cy + h * 0.5),
            (cx - w, cy - h * 0.5 + h * 0.4)]


# ============================================================================ small bench items

@icon("watch-key", CAT, "Small winding key with a rounded bow and a short square barrel",
      tags=["winding key", "clock key", "pocket watch", "wind", "antique", "horology"])
def _(S):
    return [
        shell(rect(7, 2.5, 10, 5, rr(S, 2.5))),
        line(seg(12, 7.5, 12, 10.5)),
        shell(rect(8.5, 10.5, 7, 10, rr(S, 2))),
        sq(10.5, 15.5, 3, 3),
    ]


@icon("watch-chain", CAT, "Pocket watch chain with a clip ring, a T bar and a hanging fob",
      tags=["pocket watch", "albert chain", "fob chain", "t bar", "waistcoat", "antique", "chain"])
def _(S):
    return [
        shell(circle(12, 5, 2.5)),
        line(seg(12, 7.5, 12, 11)),
        line(seg(7, 11, 17, 11)),
        line(seg(12, 11, 12, 13.5)),
        shell(poly([(12, 13.5), (16, 17.5), (12, 21.5), (8, 17.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("draw-plate", CAT, "Flat steel plate with a row of holes shrinking in size",
      tags=["wire drawing", "drawplate", "wire", "gauge", "goldsmith", "tapered holes", "metalwork"])
def _(S):
    return [
        shell(rect(2.5, 6.5, 19, 11, rr(S, 2.5))),
        dot(7.5, 12, 2.2),
        dot(13, 12, 1.6),
        dot(17.5, 12, 1.1),
    ]


@icon("dapping-block", CAT, "Metal block with round cavities and a ball ended punch beside it",
      tags=["dapping", "doming", "punch", "dome", "cavity", "metal forming", "goldsmith"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 12, 16, rr(S, 2))),
        dot(8.5, 9.5, 3),
        dot(8.5, 16, 1.7),
        line(seg(19.5, 2.5, 19.5, 14.5)),
        shell(circle(19.5, 17.5, 2.5)),
    ]


@icon("diamond-tester", CAT, "Pen shaped tester with a metal probe tip and indicator lights",
      tags=["diamond test", "gem tester", "moissanite", "thermal probe", "authenticity", "gemology", "pen"])
def _(S):
    return [
        line(rseg(12, 2.5, 12, 8.5)),
        shell(poly(rot([(9.5, 8.5), (14.5, 8.5), (14.5, 21.5), (9.5, 21.5)]), closed=True, r=S.r * 0.6)),
        Part("dot", circle(*rot([(12, 12.5)])[0], 1.0)),
        Part("dot", circle(*rot([(12, 15.5)])[0], 1.0)),
        Part("dot", circle(*rot([(12, 18.5)])[0], 1.0)),
    ]


@icon("carat-scale", CAT, "Small digital scale with a weighing pan holding a gem",
      tags=["gem scale", "weighing", "carat", "pocket scale", "balance", "diamond weight", "gemology"])
def _(S):
    return [
        shell(poly(gem_pts(12, 5.6, 2.8, 4.2), closed=True, r=S.r * 0.4)),
        line(seg(6, 10, 18, 10)),
        line(seg(12, 10, 12, 14)),
        shell(rect(3, 14, 18, 7.5, rr(S, 2.5))),
        sq(13, 16.5, 5, 2.5),
    ]


@icon("ingot-mold", CAT, "Steel ingot mold with a long trough and short feet",
      tags=["ingot", "casting", "pouring", "gold bar", "smelting", "metal", "mould"])
def _(S):
    return [
        shell(poly([(4, 6.5), (20, 6.5), (18.5, 16), (5.5, 16)], closed=True, r=S.r)),
        Part("dot", poly([(7.5, 9), (16.5, 9), (16, 12.5), (8, 12.5)], closed=True)),
        line(seg(7, 16, 7, 20.5)),
        line(seg(17, 16, 17, 20.5)),
    ]


@icon("casting-flask", CAT, "Short metal flask holding a wax tree with ring shapes on a central sprue",
      tags=["lost wax", "investment casting", "wax tree", "sprue", "flask", "foundry", "goldsmith"])
def _(S):
    return [
        shell("M4 6A8 3 0 0 1 20 6V18A8 3 0 0 1 4 18Z"),
        detail("M4 6A8 3 0 0 0 20 6"),
        detail(poly([(8.5, 11), (12, 14.5), (15.5, 11)])),
        detail(seg(12, 14.5, 12, 19)),
    ]


@icon("chasing-hammer", CAT, "Hammer with a flat round face, a ball peen and a slim handle",
      tags=["ball peen", "repousse", "chasing", "metalsmith", "hammer", "goldsmith", "tool"])
def _(S):
    head = rpath([("M", (5.5, 4.5)), ("L", (8.5, 4.5)), ("L", (8.5, 6)), ("L", (13.5, 6)), ("A", 2.5, 0, 1, (13.5, 11)),
                  ("L", (8.5, 11)), ("L", (8.5, 12.5)), ("L", (5.5, 12.5)), ("Z",)])
    return [
        shell(head, stroke_miterlimit="2"),
        shell(poly(rot([(9.5, 10), (12.5, 10), (12.5, 20), (9.5, 20)]), closed=True, r=S.r * 0.6)),
    ]


@icon("graver", CAT, "Engraving tool with a bulb shaped handle and a short angled steel blade",
      tags=["burin", "engraving", "hand engraving", "chisel", "metal engraving", "goldsmith", "tool"])
def _(S):
    handle = rpath([("M", (9.5, 14)), ("L", (14.5, 14)), ("C", (17.5, 15.5), (18, 20), (14.5, 21.5)), ("L", (9.5, 21.5)),
                    ("C", (6, 20), (6.5, 15.5), (9.5, 14)), ("Z",)])
    return [
        shell(handle),
        shell(poly(rot([(10.5, 14), (10.5, 7), (14, 2.5), (14, 14)]), closed=True, r=S.r * 0.9), stroke_miterlimit="2"),
    ]


@icon("jewelers-bench", CAT, "Workbench top seen from above with a half moon cutout and a catch tray",
      tags=["jewellers bench", "goldsmith bench", "workbench", "catch tray", "studio", "workshop", "half moon"])
def _(S):
    return [
        shell("M2.5 2.5H21.5V10.5H16.5A4.5 4.5 0 0 1 7.5 10.5H2.5Z"),
        shell(rect(8, 18, 8, 3.5, rr(S, 1.5))),
    ]


@icon("wire-jig", CAT, "Square pegboard with pegs and a wire bent around them",
      tags=["jig", "peg board", "wire bending", "wire work", "pegs", "craft", "pattern"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 2.5))),
        detail(poly([(7.5, 7.5), (16.5, 7.5), (7.5, 16.5), (16.5, 16.5)])),
        dot(7.5, 7.5, 1.6),
        dot(16.5, 7.5, 1.6),
        dot(7.5, 16.5, 1.6),
        dot(16.5, 16.5, 1.6),
    ]


@icon("gem-scoop", CAT, "Small scoop with a short handle holding a few loose cut stones",
      tags=["gem tray", "loose stones", "gemstones", "scoop", "sorting", "stone dealer", "diamonds"])
def _(S):
    return [
        solid(poly([(5.5, 6.5), (8, 4), (10.5, 6.5), (8, 9)], closed=True)),
        solid(poly([(11.5, 7), (13.5, 5), (15.5, 7), (13.5, 9)], closed=True)),
        shell("M3 11.5H16Q15.5 18.5 9.5 19.5Q3.5 18.5 3 11.5Z"),
        line(seg(15.5, 14, 21.5, 9.5)),
    ]


@icon("lunula-collar", CAT, "Flat crescent shaped collar necklace with small paddle ends",
      tags=["lunula", "torc", "ancient jewelry", "gorget", "collar necklace", "crescent", "bronze age"])
def _(S):
    return [
        shell("M2 6.5C3 14 7.5 17.5 12 17.5C16.5 17.5 21 14 22 6.5L18 6.5C17 10.5 15 12.5 12 12.5C9 12.5 7 10.5 6 6.5Z"),
        dot(12, 15, 1.0),
    ]


@icon("touchstone", CAT, "Dark stone tablet with bright streaks rubbed across it and a gold bar touching it",
      tags=["assay", "gold test", "purity", "streak test", "karat test", "metal testing", "stone"])
def _(S):
    return [
        shell(poly([(2.5, 21), (5, 10), (21.5, 10), (19, 21)], closed=True, r=S.r)),
        detail(seg(8, 14, 12.5, 14)),
        detail(seg(7.5, 17, 16, 17)),
        shell(rect(14, 2.5, 7, 4, rr(S, 1.5))),
        line(seg(17.5, 6.5, 17.5, 10)),
    ]




@icon("gem-certificate", CAT, "Certificate sheet with a cut gem at the top, text lines and a round seal",
      tags=["gem report", "grading report", "diamond certificate", "appraisal", "authenticity", "gemology", "document"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 2.5))),
        detail(poly(gem_pts(12, 7.5, 2.6, 3.4), closed=True, r=S.r * 0.4)),
        detail(seg(8, 13, 16, 13)),
        detail(seg(8, 17.5, 12, 17.5)),
        dot(16, 17.5, 1.6),
    ]


@icon("diamond-parcel", CAT, "Folded paper packet laid flat along its creases with a diamond in the centre",
      tags=["diamond paper", "parcel paper", "gem packet", "stone packet", "dealer", "loose diamonds", "folded paper"])
def _(S):
    return [
        shell(rect(3, 4.5, 18, 15, rr(S, 2.5))),
        detail(seg(3, 9, 21, 9)),
        detail(seg(3, 15, 21, 15)),
        Part("dot", poly([(12, 10.2), (15, 12), (12, 13.8), (9, 12)], closed=True)),
    ]


@icon("jewelry-pouch", CAT, "Soft drawstring pouch with a ring peeking out of the opening",
      tags=["gift pouch", "drawstring bag", "jewellery bag", "velvet pouch", "packaging", "ring", "gift"])
def _(S):
    return [
        shell(circle(12, 5.5, 2)),
        line(poly([(6.5, 4), (9.5, 9.5)])),
        line(poly([(17.5, 4), (14.5, 9.5)])),
        shell("M9.5 9.5C4 12 3.5 18 6.5 20.5H17.5C20.5 18 20 12 14.5 9.5Z"),
        detail(seg(9, 13.5, 15, 13.5)),
    ]


@icon("jewelry-tag", CAT, "Small price tag on a string loop with a punched hole",
      tags=["price tag", "jewellery label", "label", "retail", "hang tag", "string tag", "price"])
def _(S):
    return [
        line("M10.5 10.5C7 6.5 8.5 2.5 12 2.5C15.5 2.5 17 6.5 13.5 10.5"),
        shell(poly([(7.5, 13.5), (12, 9.5), (16.5, 13.5), (16.5, 21.5), (7.5, 21.5)], closed=True, r=S.r * 0.8)),
        dot(12, 14, 1.2),
    ]


@icon("ring-resizing", CAT, "Ring band with a cut gap at the bottom and two arrows pointing outward",
      tags=["resize ring", "ring size", "stretch ring", "cut and solder", "sizing", "ring repair", "adjust ring"])
def _(S):
    return [
        line(arc(12, 9.5, 7, 110, 430)),
        line(poly([(10.5, 20.5), (4.5, 20.5)])),
        line(poly([(7, 18), (4.5, 20.5), (7, 23)], r=S.r * 0.5)),
        line(poly([(13.5, 20.5), (19.5, 20.5)])),
        line(poly([(17, 18), (19.5, 20.5), (17, 23)], r=S.r * 0.5)),
    ]


@icon("cloisonne-enamel", CAT, "Round plaque divided by raised wire outlines into petal shaped cells",
      tags=["cloisonne", "enamel", "enameling", "wire cells", "enamelware", "petals", "decorative"])
def _(S):
    tip = 4.5 if S.name == "line" else 6.5
    parts = [shell(circle(12, 12, 9.5))]
    for deg in (0, 90, 180, 270):
        parts.append(detail(rpath([("M", (12, 12)), ("C", (9, 10), (9, tip + 1.5), (12, tip)), ("C", (15, tip + 1.5), (15, 10), (12, 12)), ("Z",)], deg)))
    return parts


@icon("filigree", CAT, "Round openwork pendant made of fine curling wire scrolls",
      tags=["filigree work", "wire scrolls", "openwork", "pendant", "lacework", "scrollwork", "decorative metal"])
def _(S):
    parts = [shell(circle(12, 12, 9.5))]
    for cx, cy, th in ((8, 8, 225), (16, 8, 315), (8, 16, 135), (16, 16, 45)):
        parts.append(detail(arc(cx, cy, 2, th + 45, th + 315)))
    return parts + [dot(12, 12, 1.0)]


@icon("casting-grain", CAT, "Small heap of round metal shot grains",
      tags=["shot", "grain", "pellets", "metal beads", "alloy", "melting", "casting"])
def _(S):
    parts = []
    for r, y, xs in ((18.5, 0, (6, 10.2, 14.4, 18.6)), (14.5, 0, (8.1, 12.3, 16.5)), (10.5, 0, (10.2, 14.4)), (6.5, 0, (12.3,))):
        for x in xs:
            parts.append(dot(x, r, 1.6))
    return parts + [line(seg(3, 21.5, 21, 21.5))]
