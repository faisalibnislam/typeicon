"""TypeIcon Core: stationery (pens, paper, desk supplies, mail and packing)."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar

CAT = "stationery"
TILT = 45


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rot(pts, deg=TILT, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rp(pts, closed=True, r=0.0, deg=TILT):
    return poly(rot(pts, deg), closed=closed, r=r)


def rseg(x1, y1, x2, y2, deg=TILT):
    (a, b), (c, d) = rot([(x1, y1), (x2, y2)], deg)
    return seg(a, b, c, d)


def rpath(cmds, deg=TILT) -> str:
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


def rrect(x, y, w, h, rx=0.0, deg=TILT) -> str:
    rx = max(0.0, min(rx, w / 2, h / 2))
    if rx == 0:
        return rp([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], deg=deg)
    return rpath([("M", (x + rx, y)), ("L", (x + w - rx, y)), ("A", rx, 0, 1, (x + w, y + rx)),
                  ("L", (x + w, y + h - rx)), ("A", rx, 0, 1, (x + w - rx, y + h)), ("L", (x + rx, y + h)),
                  ("A", rx, 0, 1, (x, y + h - rx)), ("L", (x, y + rx)), ("A", rx, 0, 1, (x + rx, y)), ("Z",)], deg)


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    return Part("dot", rect(x, y, w, h, rx))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def spline(pts):
    """Smooth closed curve through points (Catmull-Rom as cubic Beziers)."""
    n = len(pts)
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}"
    return d + "Z"


def blob(S, cx, cy, radii, start=-90.0, line_r=0.0):
    """Irregular closed outline: faceted in Line, smooth in Rounded."""
    n = len(radii)
    pts = [polar(cx, cy, r, start + i * 360 / n) for i, r in enumerate(radii)]
    return poly(pts, closed=True, r=line_r) if S.name == "line" else spline(pts)


def star_pts(cx, cy, ro, ri, n=5):
    out = []
    for i in range(n * 2):
        out.append(polar(cx, cy, ro if i % 2 == 0 else ri, -90 + i * 180 / n))
    return out


# ============================================================================ writing instruments (chunk 1)

@icon("mechanical-pencil", CAT, "Slim mechanical pencil with a pocket clip and a thin lead at the tip",
      tags=["propelling pencil", "drafting", "writing", "school", "office", "lead", "stationery"])
def _(S):
    return [
        shell(rrect(10, 1, 4, 2.5, rr(S, 1)), stroke_miterlimit="2"),
        shell(rrect(9.5, 3.5, 5, 11, rr(S, 1.5))),
        line(rpath([("M", (14.5, 5)), ("L", (16.5, 5)), ("L", (16.5, 9.5))])),
        shell(rp([(10, 14.5), (14, 14.5), (12.8, 18), (11.2, 18)], r=S.r * 0.3)),
        line(rseg(12, 18, 12, 22.5)),
    ]


@icon("click-pen", CAT, "Retractable ballpoint pen with a plunger button, side clip and small tip",
      tags=["ballpoint", "retractable pen", "writing", "office", "signing", "stationery"])
def _(S):
    return [
        shell(rrect(10.5, 1, 3, 2.5, rr(S, 1))),
        shell(rrect(9, 3.5, 6, 12, rr(S, 2))),
        line(rpath([("M", (15, 5.5)), ("L", (17.5, 5.5)), ("L", (17.5, 12))])),
        shell(rp([(9.5, 15.5), (14.5, 15.5), (12.8, 19.5), (11.2, 19.5)], r=S.r * 0.4)),
        line(rseg(12, 19.5, 12, 22)),
    ]


@icon("multicolor-pen", CAT, "Chunky multi-ink pen with sliding colour tabs on its side and one tip",
      tags=["four colour pen", "multi pen", "ballpoint", "writing", "office", "school", "stationery"])
def _(S):
    return [
        shell(rrect(8.5, 1.5, 7, 13, rr(S, 2.5))),
        line(rseg(15.5, 4, 18.5, 4)), line(rseg(15.5, 7.5, 18.5, 7.5)), line(rseg(15.5, 11, 18, 11)),
        shell(rp([(9, 14.5), (15, 14.5), (13, 19), (11, 19)], r=S.r * 0.4)),
        line(rseg(12, 19, 12, 22)),
    ]


@icon("dip-pen", CAT, "Dip pen with a tapered holder and a split metal nib",
      tags=["nib pen", "calligraphy", "quill", "fountain", "ink", "writing", "lettering"])
def _(S):
    return [
        shell(rp([(10.5, 1.5), (13.5, 1.5), (14, 11.5), (10, 11.5)], r=S.r * 0.4)),
        shell(rp([(9.5, 11.5), (14.5, 11.5), (13.5, 17), (12, 22), (10.5, 17)], r=S.r * 0.6), stroke_miterlimit="3"),
        dot(*rot([(12, 15.5)])[0], 1.0),
    ]


@icon("inkwell", CAT, "Squat square ink bottle with a short neck, a cap and a visible ink level",
      tags=["ink bottle", "ink pot", "calligraphy", "writing", "pen", "fountain pen", "stationery"])
def _(S):
    return [
        shell(rect(3.5, 10.5, 17, 11, rr(S, 3))),
        shell(rect(8, 7, 8, 3.5, rr(S, 1))),
        detail(seg(7, 16, 17, 16)),
        line(seg(13, 7, 19, 2.5)),
    ]


@icon("ink-blot", CAT, "Irregular ink splash with a round centre and droplets around it",
      tags=["ink splash", "stain", "spill", "blotch", "splatter", "writing", "mess"])
def _(S):
    radii = [6.5, 7.6, 5.4, 6.8, 8.4, 6.0, 5.2, 7.4, 8.2, 6.2, 5.6, 7.0, 6.2, 8.0]
    return [
        shell(blob(S, 11, 12.5, radii, start=-100, line_r=0.8), stroke_miterlimit="3"),
        dot(19.5, 4.5, 1.6), dot(4, 4, 1.3), dot(20, 20, 1.4),
    ]


@icon("pencil-box", CAT, "Open hard pencil case with its lid raised at the back and two pencils inside",
      tags=["pencil case", "school", "supplies", "stationery", "pencils", "student", "desk"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 4.5, rr(S, 1.5))),
        shell(rect(3, 9.5, 18, 12, rr(S, 3))),
        detail(seg(6, 14.25, 16, 14.25)),
        detail(seg(8, 17.75, 18, 17.75)),
    ]


@icon("pencil-roll", CAT, "Fabric pencil wrap with slots holding three pencils and a tie cord",
      tags=["pencil wrap", "pencil holder", "art supplies", "drawing", "artist", "stationery", "roll"])
def _(S):
    return [
        shell(rect(2.5, 10, 19, 11, rr(S, 2.5))),
        line(seg(6.5, 3.5, 6.5, 14)), line(seg(12, 3.5, 12, 14)), line(seg(17.5, 3.5, 17.5, 14)),
        detail(seg(9.25, 15, 9.25, 21)), detail(seg(14.75, 15, 14.75, 21)),
    ]


@icon("pencil-cup", CAT, "Desk cup holding three pens and pencils at different angles",
      tags=["pen holder", "pen pot", "desk organizer", "office", "pencils", "stationery", "desk"])
def _(S):
    return [
        shell(rect(5.5, 11, 13, 10, rr(S, 3))),
        line(seg(9, 11, 6.5, 3)), line(seg(12.5, 11, 12.5, 2.5)), line(seg(16, 11, 18.5, 3.5)),
        solid(poly([(5.5, 3.5), (7.5, 3.5), (6.5, 1.8)], closed=True)) if False else dot(12.5, 2.8, 0.1) if False else detail(seg(9, 16, 15, 16)),
    ]


@icon("desk-pen-set", CAT, "Rectangular desk base with a small holder and a slim pen angled upward",
      tags=["desk set", "pen stand", "executive", "office", "gift", "pen", "writing", "stationery"])
def _(S):
    pen = rot([(10.5, 11), (13.5, 11), (13.5, 5), (12, 1.5), (10.5, 5)], 22, 12, 11)
    return [
        shell(rect(2.5, 16.5, 19, 5, rr(S, 2))),
        shell(poly(pen, closed=True, r=S.r * 0.4)),
        shell(rect(8.5, 11, 7, 5.5, rr(S, 1.5))),
    ]


@icon("crank-pencil-sharpener", CAT, "Desk sharpener with a round body, side crank and a pencil hole",
      tags=["manual sharpener", "classroom sharpener", "school", "pencil", "crank", "stationery", "office"])
def _(S):
    return [
        shell(rect(3.5, 3.5, 13, 13, L(S, 4, 6.5))),
        detail(circle(10, 10, 0.1)) if False else dot(10, 10, 2.5),
        line(rpath([("M", (16.5, 10)), ("L", (20.5, 10)), ("L", (20.5, 15.5))], deg=0)),
        dot(20.5, 17.5, 1.7),
        line(seg(5, 21, 15, 21)),
    ]


@icon("correction-tape", CAT, "Handheld correction tape dispenser with an applicator tip laying a strip",
      tags=["white out", "tape runner", "erase", "mistake", "fix", "office", "stationery", "writing"])
def _(S):
    return [
        shell(rect(2.5, 5.5, 13, 13, L(S, 3, 6.5))),
        detail(circle(9, 12, 3.2)),
        shell(poly([(15.5, 9), (20, 10.2), (20, 13.8), (15.5, 15)], closed=True, r=S.r * 0.4)),
        line(seg(21.5, 17, 22, 17)) if False else line(seg(13, 21.5, 21.5, 21.5)),
    ]


@icon("correction-fluid", CAT, "Small correction bottle with its brush cap lifted above the neck",
      tags=["white out", "typo fix", "paint", "erase", "mistake", "fix", "office", "stationery"])
def _(S):
    return [
        shell(rect(8.5, 2.5, 7, 4, rr(S, 1.5))),
        line(seg(12, 6.5, 12, 9.5)),
        shell(rect(9, 9.5, 6, 3, rr(S, 1))),
        shell(rect(5.5, 12.5, 13, 9, rr(S, 3))),
        detail(seg(8.5, 17, 15.5, 17)),
    ]


@icon("whiteboard-eraser", CAT, "Whiteboard eraser block with a curved grip on top and a felt pad below",
      tags=["board eraser", "dry erase", "classroom", "wipe", "marker", "teaching", "office", "stationery"])
def _(S):
    return [
        shell(rect(3, 11, 18, 10, rr(S, 2.5))),
        detail(seg(3, 17, 21, 17)),
        line(poly([(7.5, 11), (7.5, 5), (16.5, 5), (16.5, 11)], r=S.r * 1.4)),
    ]


@icon("pen-refill", CAT, "Ballpoint ink refill with a small spring slipped over the tip end",
      tags=["ink cartridge", "ink tube", "ballpoint", "replace", "spring", "pen", "stationery"])
def _(S):
    return [
        shell(rrect(9.5, 1.5, 5, 10, rr(S, 1.5))),
        line(rseg(8.5, 14.5, 15.5, 14.5)), line(rseg(8.5, 17.5, 15.5, 17.5)),
        line(rseg(12, 11.5, 12, 22)),
    ]


# ============================================================================ stamps, seals, pads and paper (chunk 2)

@icon("pencil-lead-refill", CAT, "Slim lead tube with a sliding cap and two thin lead sticks inside",
      tags=["lead refill", "mechanical pencil", "spare leads", "drafting", "pencil", "supplies", "stationery"])
def _(S):
    return [
        shell(rect(8, 2.5, 8, 3.5, rr(S, 1))),
        shell(rect(7, 6, 10, 15, rr(S, 2))),
        detail(seg(10.25, 10, 10.25, 17)), detail(seg(13.75, 10, 13.75, 17)),
    ]


@icon("rocker-blotter", CAT, "Curved rocker blotter with a round knob handle on top",
      tags=["ink blotter", "desk blotter", "blotting paper", "ink", "calligraphy", "vintage", "stationery"])
def _(S):
    return [
        shell(rect(9, 3, 6, 4, L(S, 1.5, 2))),
        shell("M3 10.5H21C20.5 14.5 17 18.5 12 18.5C7 18.5 3.5 14.5 3 10.5Z", stroke_miterlimit="3"),
        detail(seg(7.5, 14, 16.5, 14)),
    ]


@icon("wax-seal", CAT, "Round wax seal with irregular melted edges and a star pressed in the middle",
      tags=["sealing wax", "stamp", "letter seal", "official", "certified", "royal", "approved", "stationery"])
def _(S):
    radii = [9, 8, 9.3, 8.1, 9, 7.9, 9.4, 8.2, 9, 8, 9.2, 8.3, 9.3, 8, 9, 8.2]
    return [
        shell(blob(S, 12, 12, radii, line_r=0.6), stroke_miterlimit="3"),
        Part("dot", poly(star_pts(12, 12.3, 5, 2.2), closed=True, r=S.r * 0.3)),
    ]


@icon("wax-seal-stamp", CAT, "Turned wooden seal handle with a round metal head beside a small wax puddle",
      tags=["sealing stamp", "signet", "letter seal", "wax", "invitation", "calligraphy", "vintage", "stationery"])
def _(S):
    puddle = (poly([(3.5, 20.2), (7, 18.5), (17, 18.5), (20.5, 20.2), (17, 21.9), (7, 21.9)], closed=True)
              if S.name == "line" else ellipse(12, 20.2, 8.5, 1.7))
    return [
        shell(rect(9, 2.5, 6, 3.5, L(S, 1, 2.5))),
        shell(poly([(10.5, 6), (13.5, 6), (13.5, 10.5), (15, 12), (15, 13.5), (9, 13.5), (9, 12), (10.5, 10.5)], closed=True, r=S.r * 0.3)),
        shell(rect(6.5, 13.5, 11, 3, L(S, 0.5, 1.5))),
        shell(puddle),
    ]


@icon("ink-pad", CAT, "Flat ink pad tin with its lid open and a soaked pad inside",
      tags=["stamp pad", "inkpad", "rubber stamp", "ink", "office", "crafts", "stationery"])
def _(S):
    return [
        shell(poly([(4.5, 7.5), (6, 2.5), (18, 2.5), (19.5, 7.5)], closed=True, r=S.r * 0.5)),
        shell(rect(2.5, 10, 19, 11, rr(S, 2.5))),
        sq(6, 13, 12, 5, rr(S, 1)),
    ]


@icon("date-stamp", CAT, "Rubber date stamp with a loop handle and a number band around its body",
      tags=["dater", "rubber stamp", "office", "received", "paperwork", "mail room", "stationery"])
def _(S):
    return [
        line(poly([(8.5, 9.5), (8.5, 3), (15.5, 3), (15.5, 9.5)], r=S.r * 1.5)),
        shell(rect(6, 9.5, 12, 7, rr(S, 1.5))),
        detail(seg(8.5, 13, 15.5, 13)),
        shell(rect(3, 16.5, 18, 4.5, rr(S, 1.5))),
    ]


@icon("seal-embosser", CAT, "Hand press with a C-shaped frame whose jaws clamp a round die over the edge of a sheet",
      tags=["notary", "embossing seal", "official seal", "document", "certificate", "stamp press", "stationery"])
def _(S):
    return [
        shell(poly([(3, 6), (21, 6), (21, 21), (3, 21), (3, 16.5), (15.5, 16.5), (15.5, 10.5), (3, 10.5)], closed=True, r=S.r * 0.4)),
        dot(9, 13.5, 1.2),
    ]


@icon("padfolio", CAT, "Open writing folio with a notepad on the right and card pockets on the left",
      tags=["portfolio", "folder", "notepad holder", "business", "conference", "meeting", "stationery"])
def _(S):
    return [
        shell(rect(2.5, 4, 19, 16, rr(S, 2.5))),
        detail(seg(12, 4, 12, 20)),
        detail(seg(5, 9, 9.5, 9)), detail(seg(5, 14, 9.5, 14)),
        detail(seg(14.5, 9, 19, 9)), detail(seg(14.5, 13, 19, 13)), detail(seg(14.5, 17, 19, 17)),
    ]


@icon("legal-pad", CAT, "Tall writing pad with a binding strip across the top, a margin line and ruled lines",
      tags=["yellow pad", "notepad", "writing pad", "notes", "lawyer", "office", "paper", "stationery"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rr(S, 2))),
        sq(5, 2.5, 14, 4),
        detail(seg(8.5, 6.5, 8.5, 21)),
        detail(seg(11.5, 10.5, 19, 10.5)), detail(seg(11.5, 14.5, 19, 14.5)), detail(seg(11.5, 18, 19, 18)),
    ]


@icon("steno-pad", CAT, "Narrow pad with spiral rings along the top and a line dividing the page into two columns",
      tags=["reporter notebook", "shorthand", "spiral pad", "notes", "secretary", "journalist", "stationery"])
def _(S):
    return [
        shell(rect(5.5, 5, 13, 16, rr(S, 2))),
        line(seg(9, 2.5, 9, 7.5)), line(seg(12, 2.5, 12, 7.5)), line(seg(15, 2.5, 15, 7.5)),
        detail(seg(12, 10, 12, 21)),
    ]


@icon("composition-notebook", CAT, "Marbled-cover notebook with a dark spine and a small blank label",
      tags=["composition book", "marble notebook", "school", "journal", "notes", "student", "stationery"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, L(S, 2, 3.5))),
        detail(seg(8.5, 2.5, 8.5, 21.5)),
        detail(rect(11, 6.5, 6, 4, 0.5)),
        dot(11.5, 15, 1), dot(15, 17, 1), dot(16, 14, 0.9),
    ]


@icon("index-card", CAT, "Horizontal record card with a heading line near the top and ruled lines below",
      tags=["note card", "flash card", "cue card", "recipe card", "study", "library", "stationery"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 19, 15, rr(S, 2.5))),
        detail(seg(6, 8.5, 13, 8.5)),
        detail(seg(6, 12.5, 18, 12.5)), detail(seg(6, 16.5, 18, 16.5)),
    ]


@icon("index-card-box", CAT, "Small open box of upright index cards with a tabbed divider sticking up",
      tags=["card file", "recipe box", "card catalog", "flash cards", "filing", "library", "stationery"])
def _(S):
    return [
        line(poly([(5, 12), (5, 6.5), (13, 6.5), (13, 3), (19, 3), (19, 12)], r=S.r * 0.6)),
        shell(rect(3, 12, 18, 9, rr(S, 2.5))),
        detail(seg(8, 16.5, 16, 16.5)),
    ]


@icon("graph-paper", CAT, "Sheet covered in a square grid with the top right corner folded down",
      tags=["grid paper", "squared paper", "math paper", "drafting", "engineering", "plotting", "stationery"])
def _(S):
    return [
        shell(poly([(5, 3), (14, 3), (19, 8), (19, 21), (5, 21)], closed=True, r=S.r * 0.5)),
        detail(poly([(14, 3), (14, 8), (19, 8)], r=0)),
        detail(seg(5, 12.5, 19, 12.5)), detail(seg(5, 16.5, 19, 16.5)),
        detail(seg(9.5, 8, 9.5, 21)), detail(seg(14.5, 8, 14.5, 21)),
    ]


@icon("loose-leaf-paper", CAT, "Ruled sheet with three punched holes and a margin line on the left",
      tags=["notebook paper", "binder paper", "lined paper", "school", "homework", "notes", "stationery"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, L(S, 1, 3.5))),
        dot(7.5, 7, 1.2), dot(7.5, 12, 1.2), dot(7.5, 17, 1.2),
        detail(seg(11, 2.5, 11, 21.5)),
        detail(seg(11, 8, 20, 8)), detail(seg(11, 12.5, 20, 12.5)), detail(seg(11, 17, 20, 17)),
    ]


@icon("dot-grid-paper", CAT, "Sheet with evenly spaced dots in rows and columns and a folded corner",
      tags=["dotted paper", "bullet journal", "dot grid", "planner page", "sketching", "lettering", "stationery"])
def _(S):
    dots = [dot(x, y, 1.1) for x, y in [(9, 11.5), (14, 11.5), (9, 15.5), (14, 15.5), (9, 19), (14, 19)]]
    return [
        shell(poly([(5, 3), (14, 3), (19, 8), (19, 21), (5, 21)], closed=True, r=S.r * 0.5)),
        detail(poly([(14, 3), (14, 8), (19, 8)], r=0)),
    ] + dots


@icon("tractor-feed-paper", CAT, "Continuous computer paper with sprocket holes along both edges and a fold below",
      tags=["fanfold paper", "continuous form", "dot matrix", "printer paper", "retro computing", "perforated", "stationery"])
def _(S):
    return [
        shell(rect(3, 3, 18, 13, rr(S, 1.5))),
        dot(5.5, 6.5, 1), dot(5.5, 12.5, 1), dot(18.5, 6.5, 1), dot(18.5, 12.5, 1),
        detail(seg(8.5, 3, 8.5, 16)), detail(seg(15.5, 3, 15.5, 16)),
        line(poly([(3, 19), (21, 19)])),
    ]


@icon("paper-ream", CAT, "Wrapped pack of paper with a label on the middle and a sheet edge showing on top",
      tags=["paper stack", "copy paper", "printer paper", "a4", "office supplies", "bulk", "stationery"])
def _(S):
    return [
        line(seg(5.5, 4.5, 18.5, 4.5)),
        shell(rect(3, 7.5, 18, 13.5, rr(S, 2))),
        detail(rect(7, 11, 10, 6, 0.5)),
    ]


# ============================================================================ paper products and calendars (chunk 3)

@icon("thermal-paper-roll", CAT, "Small paper roll with a hollow core and its loose end hanging down",
      tags=["receipt paper", "till roll", "pos", "register", "printer paper", "checkout", "stationery"])
def _(S):
    return [
        shell(poly([(8, 11), (16, 11), (16, 21.5), (14, 20), (12, 21.5), (10, 20), (8, 21.5)], closed=True, r=S.r * 0.3)),
        shell(rect(3.5, 2.5, 17, 8.5, L(S, 2, 4))),
        detail(seg(7.5, 2.5, 7.5, 11)), detail(seg(16.5, 2.5, 16.5, 11)),
        detail(seg(10.5, 15.5, 13.5, 15.5)),
    ]


@icon("letterhead", CAT, "Sheet of paper with a header band holding a small emblem and lines of text below",
      tags=["company letter", "stationery sheet", "business letter", "branding", "correspondence", "paper", "official"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, rr(S, 2))),
        dot(8.5, 5.5, 1.5),
        detail(seg(11.5, 5.5, 16, 5.5)),
        detail(seg(4.5, 9, 19.5, 9)),
        detail(seg(8, 13, 16, 13)), detail(seg(8, 17, 13, 17)),
    ]


@icon("folded-letter", CAT, "Letter folded in three with two fold creases and a line of handwriting",
      tags=["tri fold", "business letter", "mail", "correspondence", "note", "paper", "post"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rr(S, 2))),
        detail(seg(5, 8.75, 19, 8.75)), detail(seg(5, 15.25, 19, 15.25)),
        detail(seg(8.5, 12, 15.5, 12)),
    ]


@icon("crumpled-paper", CAT, "Ball of crushed paper with jagged creases and folded facets",
      tags=["scrunched paper", "waste", "trash", "draft", "discard", "rubbish", "mistake", "paper ball"])
def _(S):
    radii = [8.6, 7.6, 9, 7.4, 8.8, 7.8, 9.1, 7.5, 8.6, 7.7]
    return [
        shell(blob(S, 12, 12, radii, start=-80, line_r=0.5), stroke_miterlimit="3"),
        detail(poly([(7, 8.5), (11, 10), (10.5, 14), (14.5, 16)], r=S.r * 0.2)),
        detail(poly([(13.5, 6), (16, 9.5), (18, 9)], r=S.r * 0.2)),
    ]


@icon("memo-cube", CAT, "Thick cube of loose note sheets seen from a corner with sheet edges on its sides",
      tags=["note cube", "paper cube", "desk memo", "notes", "message pad", "reminder", "stationery"])
def _(S):
    return [
        shell(poly([(4, 8.5), (8, 4), (20, 4), (20, 15.5), (16, 20), (4, 20)], closed=True, r=S.r * 0.4)),
        detail(poly([(4, 8.5), (16, 8.5), (20, 4)], r=0)),
        detail(seg(16, 8.5, 16, 20)),
        detail(seg(4, 14, 16, 14)),
    ]


@icon("page-flags", CAT, "Edge of a page with a row of narrow index flags sticking out of its side",
      tags=["sticky flags", "page markers", "bookmarks", "tabs", "highlight", "index tabs", "review", "stationery"])
def _(S):
    return [
        shell(rect(3, 3, 13, 18, rr(S, 2))),
        line(seg(16, 6.5, 21.5, 6.5)), line(seg(16, 11.5, 21.5, 11.5)), line(seg(16, 16.5, 21.5, 16.5)),
        detail(seg(6.5, 9, 12.5, 9)), detail(seg(6.5, 14, 11, 14)),
    ]


@icon("label-sheet", CAT, "Sheet with a grid of rounded labels, the last one peeling at the corner",
      tags=["sticker sheet", "address labels", "adhesive labels", "peel", "stickers", "printing", "stationery"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, L(S, 1.5, 3.5))),
        sq(6, 6, 5.5, 5.5, L(S, 0.5, 1.5)), sq(12.5, 6, 5.5, 5.5, L(S, 0.5, 1.5)), sq(6, 12.5, 5.5, 5.5, L(S, 0.5, 1.5)),
        Part("dot", poly([(12.5, 18), (12.5, 12.5), (18, 12.5), (18, 15), (15, 18)], closed=True, r=L(S, 0, 0.8))),
    ]


@icon("shipping-label", CAT, "Rectangular label with address lines at the top and a barcode strip at the bottom",
      tags=["parcel label", "postage label", "address label", "barcode", "courier", "dispatch", "mail", "package"])
def _(S):
    return [
        shell(rect(3, 4, 18, 16, rr(S, 2))),
        detail(seg(6.5, 8, 15, 8)), detail(seg(6.5, 11.5, 12, 11.5)),
        sq(6, 14.5, 1.5, 3.5), sq(8.5, 14.5, 1, 3.5), sq(10.5, 14.5, 2, 3.5), sq(14, 14.5, 1, 3.5), sq(16, 14.5, 1.5, 3.5),
    ]


@icon("planner", CAT, "Open spiral-bound planner with two facing pages split into small day boxes",
      tags=["diary", "agenda", "organizer", "schedule", "weekly planner", "datebook", "appointments", "stationery"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 17, rr(S, 2.5))),
        line(seg(10, 7, 14, 7)), line(seg(10, 12, 14, 12)), line(seg(10, 17, 14, 17)),
        sq(5, 7, 3, 3), sq(5, 13.5, 3, 3), sq(16, 7, 3, 3), sq(16, 13.5, 3, 3),
    ]


@icon("desk-calendar", CAT, "Tent-shaped standing calendar with rings across the top and a date grid on its front",
      tags=["standing calendar", "flip calendar", "table calendar", "dates", "schedule", "office", "stationery"])
def _(S):
    return [
        shell(poly([(5, 6), (19, 6), (21, 20.5), (3, 20.5)], closed=True, r=S.r * 0.5)),
        line(seg(8.5, 3, 8.5, 8)), line(seg(15.5, 3, 15.5, 8)),
        dot(8, 12.5, 1.1), dot(12, 12.5, 1.1), dot(16, 12.5, 1.1), dot(8, 16.5, 1.1), dot(12, 16.5, 1.1), dot(16, 16.5, 1.1),
    ]


@icon("tear-off-calendar", CAT, "Calendar pad with a large day number on the top sheet and a torn strip above it",
      tags=["day calendar", "daily pad", "page a day", "date", "kitchen calendar", "wall calendar", "stationery"])
def _(S):
    return [
        line(poly([(4, 5.5), (6.5, 3), (9, 5.5), (11.5, 3), (14, 5.5), (16.5, 3), (19, 5.5)], r=0)),
        shell(rect(4, 8.5, 16, 12.5, rr(S, 2))),
        line(poly([(10, 14), (13, 12), (13, 18.5)], r=S.r * 0.3)),
    ]


@icon("perpetual-calendar", CAT, "Two small number cubes on a stand above a block that shows the month",
      tags=["dice calendar", "cube calendar", "desk date", "block calendar", "date display", "office", "stationery"])
def _(S):
    return [
        shell(rect(3.5, 3, 8, 9, rr(S, 1.5))),
        shell(rect(12.5, 3, 8, 9, rr(S, 1.5))),
        sq(7.3, 5.8, 1.5, 4.2), sq(6.2, 5.8, 1.2, 1.4),
        sq(14.8, 5.8, 3.4, 1.4), sq(16.8, 7.2, 1.4, 3),
        shell(rect(3, 14.5, 18, 6.5, rr(S, 2))),
        detail(seg(7, 17.75, 17, 17.75)),
    ]


@icon("timesheet", CAT, "Grid form for logging hours with a small clock face drawn in the header corner",
      tags=["time log", "hours", "work hours", "attendance", "payroll", "time tracking", "form", "stationery"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 2.5))),
        detail(circle(16.5, 6.8, 2)),
        detail(seg(6, 6.8, 11, 6.8)),
        detail(seg(2.5, 11.5, 21.5, 11.5)), detail(seg(2.5, 16.5, 21.5, 16.5)),
        detail(seg(9.5, 11.5, 9.5, 21.5)),
    ]


@icon("time-card", CAT, "Tall narrow punch card with a notch at the top, a name line and two columns of time stamps",
      tags=["punch card", "clock in", "attendance", "payroll", "work shift", "factory", "time clock", "stationery"])
def _(S):
    rx = L(S, 2, 3.5)
    d = (f"M{fmt(6 + rx)} 2.5H10.5a1.5 1.5 0 0 0 3 0H{fmt(18 - rx)}a{rx} {rx} 0 0 1 {rx} {rx}V{fmt(21.5 - rx)}"
         f"a{rx} {rx} 0 0 1 -{rx} {rx}H{fmt(6 + rx)}a{rx} {rx} 0 0 1 -{rx} -{rx}V{fmt(2.5 + rx)}a{rx} {rx} 0 0 1 {rx} -{rx}Z")
    return [
        shell(d),
        detail(seg(9, 8, 15, 8)),
        detail(seg(12, 11, 12, 21.5)),
        sq(8, 13.5, 2, 1.6), sq(8, 17.5, 2, 1.6), sq(14, 13.5, 2, 1.6), sq(14, 17.5, 2, 1.6),
    ]


@icon("punched-card", CAT, "Card with one clipped corner and rows of small rectangular holes punched across it",
      tags=["punch card", "computer history", "retro computing", "data card", "vintage", "stationery"])
def _(S):
    return [
        shell(poly([(2.5, 5.5), (17.5, 5.5), (21.5, 9), (21.5, 19), (2.5, 19)], closed=True, r=S.r * 0.4)),
        sq(5.8, 8.8, 1.6, 3), sq(9, 8.8, 1.6, 3), sq(12.2, 8.8, 1.6, 3), sq(15.4, 8.8, 1.6, 3),
        sq(5.8, 13.2, 1.6, 3), sq(9, 13.2, 1.6, 3), sq(12.2, 13.2, 1.6, 3), sq(15.4, 13.2, 1.6, 3), sq(18.4, 13.2, 1.6, 3),
    ]


@icon("brochure", CAT, "Tri-fold leaflet opened into three panels, with an image block and text marks",
      tags=["leaflet", "pamphlet", "tri fold", "flyer", "handout", "marketing", "print", "stationery"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 19, 15, rr(S, 2))),
        detail(seg(8.75, 4.5, 8.75, 19.5)), detail(seg(15.25, 4.5, 15.25, 19.5)),
        sq(10.9, 8, 2.2, 4), detail(seg(10.5, 15.5, 13.5, 15.5)),
        dot(5.6, 9, 0.9), dot(5.6, 14, 0.9), dot(18.4, 9, 0.9), dot(18.4, 14, 0.9),
    ]


@icon("flyer", CAT, "Portrait sheet with a large picture block, a bold title bar and short text lines",
      tags=["poster", "handbill", "advert", "leaflet", "announcement", "marketing", "print", "stationery"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rr(S, 2))),
        sq(8, 5.5, 8, 5),
        sq(8, 12.5, 8, 2),
        detail(seg(8, 18, 14, 18)),
    ]


@icon("resume", CAT, "Portrait document with a round portrait at the top left, a name line and sections of text lines",
      tags=["cv", "curriculum vitae", "job application", "career", "hiring", "profile", "document", "stationery"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rr(S, 2))),
        dot(9.5, 7, 2),
        detail(seg(13.5, 7, 16, 7)),
        detail(seg(8, 12.5, 16, 12.5)), detail(seg(8, 17, 13, 17)),
    ]


@icon("sketchbook", CAT, "Book with a spiral along the top edge and a simple mountain doodle on the page",
      tags=["drawing pad", "art book", "artist", "doodle", "spiral", "sketch", "drawing", "stationery"])
def _(S):
    return [
        shell(rect(4.5, 5.5, 15, 15.5, rr(S, 2))),
        line(seg(8.5, 2.5, 8.5, 7.5)), line(seg(12, 2.5, 12, 7.5)), line(seg(15.5, 2.5, 15.5, 7.5)),
        detail(poly([(7.5, 17.5), (11, 12), (13.5, 15), (15, 13.5), (17, 17.5)], r=0)),
    ]


@icon("elastic-band-notebook", CAT, "Hardcover notebook held shut by a vertical elastic strap with a ribbon hanging below",
      tags=["journal", "diary", "notes", "ribbon bookmark", "planner", "stationery", "hardcover"])
def _(S):
    return [
        shell(rect(5, 2, 14, 17.5, L(S, 1.5, 3.5))),
        detail(seg(15.25, 2, 15.25, 19.5)),
        solid(poly([(8.5, 19.5), (11.5, 19.5), (11.5, 22.3), (10, 21), (8.5, 22.3)], closed=True)),
    ]


@icon("paper-spike", CAT, "Upright metal spike on a weighted base with several receipts pierced on it",
      tags=["receipt spike", "bill spike", "note spike", "spindle", "diner", "restaurant", "orders", "stationery"])
def _(S):
    return [
        solid(poly([(10.6, 5), (13.4, 5), (12, 1.8)], closed=True)),
        line(seg(12, 5, 12, 18)),
        line(seg(6.5, 9.5, 17.5, 9.5)), line(seg(7.5, 13.5, 16.5, 13.5)),
        shell(poly([(4.5, 21.5), (7, 18), (17, 18), (19.5, 21.5)], closed=True, r=S.r * 0.5)),
    ]


# ============================================================================ envelopes, post and parcels (chunk 4)

@icon("padded-envelope", CAT, "Envelope lined with small bubbles below a flap with a peel strip",
      tags=["bubble mailer", "shipping envelope", "cushioned", "mail", "post", "protective", "packaging"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 19, 15, rr(S, 2.5))),
        detail(seg(2.5, 9, 21.5, 9)),
        dot(7, 13, 1.2), dot(12, 13, 1.2), dot(17, 13, 1.2), dot(9.5, 16.3, 1.2), dot(14.5, 16.3, 1.2),
    ]


@icon("window-envelope", CAT, "Long envelope with a clear address window on the left and a stamp square on the right",
      tags=["business envelope", "address window", "billing", "invoice", "letter", "mail", "post", "statement"])
def _(S):
    return [
        shell(rect(2, 5.5, 20, 13, rr(S, 2.5))),
        detail(rect(5, 9, 8, 6, 0.5)),
        sq(16.5, 8.5, 2.8, 3.2),
    ]


@icon("clasp-envelope", CAT, "Large portrait envelope whose flap is held down by a round metal clasp",
      tags=["manila envelope", "document envelope", "catalog envelope", "string tie", "office", "mail", "folder"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rr(S, 2.5))),
        detail(poly([(5, 3), (12, 9.5), (19, 3)], r=0)),
        dot(12, 13.2, 1.4),
    ]


@icon("interoffice-envelope", CAT, "Portrait envelope with two button discs joined by string and a ruled routing grid",
      tags=["inter office", "internal mail", "reusable envelope", "memo", "routing slip", "office mail", "post room"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rr(S, 2.5))),
        dot(12, 5.8, 1.3), dot(12, 9.8, 1.3), detail(seg(12, 5.8, 12, 9.8)),
        detail(seg(5, 14.5, 19, 14.5)), detail(seg(5, 18.3, 19, 18.3)), detail(seg(12, 14.5, 12, 21.5)),
    ]


@icon("airmail-envelope", CAT, "Envelope with a border of diagonal stripes along the bottom and a stamp in the top corner",
      tags=["air mail", "par avion", "international mail", "overseas post", "letter", "stamp", "correspondence"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 19, 15, rr(S, 2.5))),
        detail(seg(5.5, 8.5, 11, 8.5)),
        sq(15.5, 7.5, 3.5, 4),
        detail(seg(5.5, 17.5, 8, 14.3)), detail(seg(9, 17.5, 11.5, 14.3)), detail(seg(12.5, 17.5, 15, 14.3)), detail(seg(16, 17.5, 18.5, 14.3)),
    ]


@icon("letter-opener", CAT, "Slim pointed blade with a rounded handle, its tip slid under the top edge of an envelope",
      tags=["paper knife", "envelope opener", "desk tool", "mail", "slit", "office", "vintage", "stationery"])
def _(S):
    def o(pts):
        return rot(pts, 225, 14, 8)
    blade = o([(14, 0), (17, 5), (17, 9), (11, 9), (11, 5)])
    handle = o([(12.3, 9), (15.7, 9), (16.4, 12), (15.4, 15), (12.6, 15), (11.6, 12)])
    return [
        shell(rect(2.5, 12.5, 19, 9, rr(S, 2.5))),
        shell(poly(blade, closed=True, r=S.r * 0.4), stroke_miterlimit="4"),
        shell(poly(handle, closed=True, r=S.r * 0.6)),
    ]


@icon("postmark", CAT, "Circular cancellation ring with a date line inside and wavy lines trailing to the right",
      tags=["cancellation mark", "post office stamp", "franking", "date stamp", "mail", "stamped", "postal", "letter"])
def _(S):
    return [
        shell(rect(2.5, 5.5, 12.5, 12.5, L(S, 5, 6.25))),
        detail(seg(6, 11.75, 11.5, 11.75)),
        line("M16.5 8q1.5-1.6 3 0t3 0"), line("M16.5 11.75q1.5-1.6 3 0t3 0"), line("M16.5 15.5q1.5-1.6 3 0t3 0"),
    ]


@icon("post-horn", CAT, "Coiled horn with a flared bell and a small mouthpiece, the old postal service sign",
      tags=["postal horn", "mail coach", "posthorn", "post office", "courier", "bugle", "brass", "mail"])
def _(S):
    return [
        line(circle(9.5, 14, 5)),
        line(seg(9.5, 9, 9.5, 4)), line(seg(7.5, 3.5, 11.5, 3.5)),
        shell("M14.5 12.3C17.5 12.3 19.2 10 21 7.5V20.5C19.2 18 17.5 15.7 14.5 15.7Z", stroke_miterlimit="4"),
    ]


@icon("stamp-sheet", CAT, "Sheet of postage stamps in a three by three grid with perforated gaps between them",
      tags=["postage stamps", "stamp collecting", "philately", "mail", "perforation", "post office", "stamps"])
def _(S):
    ds = [dot(x, y, 1.1) for y in (5.6, 12, 18.4) for x in (5.6, 12, 18.4)]
    return [
        shell(rect(2.5, 2.5, 19, 19, L(S, 1, 3))),
        detail(seg(8.75, 2.5, 8.75, 21.5)), detail(seg(15.25, 2.5, 15.25, 21.5)),
        detail(seg(2.5, 8.75, 21.5, 8.75)), detail(seg(2.5, 15.25, 21.5, 15.25)),
    ] + ds


@icon("po-box", CAT, "Wall of small post office box doors, two across and three down, each with a tiny knob",
      tags=["post office box", "mailbox wall", "private mail", "pigeonholes", "pobox", "postal", "mail", "lockbox"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, L(S, 2, 3.5))),
        detail(seg(12, 2.5, 12, 21.5)), detail(seg(4, 8.8, 20, 8.8)), detail(seg(4, 15.2, 20, 15.2)),
        dot(10, 6.2, 0.9), dot(18, 12.2, 0.9), dot(10, 18.6, 0.9),
    ]


@icon("parcel-locker", CAT, "Wall unit of lockers in several sizes with a small screen and keypad panel on the left",
      tags=["package locker", "pickup locker", "click and collect", "smart locker", "delivery", "courier", "self service"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, L(S, 2, 3.5))),
        detail(seg(9, 2.5, 9, 21.5)),
        detail(seg(9, 8.2, 21.5, 8.2)), detail(seg(9, 14, 21.5, 14)),
        sq(4.7, 5, 2.4, 3),
        dot(5.3, 12.5, 0.75), dot(7.2, 12.5, 0.75), dot(5.3, 15.5, 0.75), dot(7.2, 15.5, 0.75),
    ]


@icon("mail-sack", CAT, "Canvas mail sack cinched at the neck with a ruffled top and an envelope on its front",
      tags=["mailbag", "post bag", "postal sack", "courier", "mail delivery", "post office", "letters", "bag"])
def _(S):
    return [
        line(poly([(7.5, 6), (9.75, 3.5), (12, 6), (14.25, 3.5), (16.5, 6)], r=0)),
        shell(poly([(8.5, 9), (15.5, 9), (19.5, 12.5), (21, 19), (19, 21.5), (5, 21.5), (3, 19), (4.5, 12.5)], closed=True, r=S.r)),
        detail(rect(8, 13.5, 8, 5.5, 0.5)),
    ]


@icon("mail-cart", CAT, "Wheeled mail cart with a deep bin, a push handle on one side and letters stacked inside",
      tags=["mailroom trolley", "post trolley", "office delivery", "mail room", "courier cart", "bin on wheels"])
def _(S):
    return [
        line(poly([(3.5, 3), (3.5, 14), (7, 14)], r=S.r * 0.6)),
        line(poly([(10, 9), (10, 5), (18, 5), (18, 9)], r=S.r * 0.4)),
        shell(rect(7, 9, 14, 8.5, rr(S, 2.5))),
        dot(10.5, 20.3, 1.6), dot(17.5, 20.3, 1.6),
    ]


# ============================================================================ mail room, weighing and packing (chunk 5)

@icon("mail-sorting-rack", CAT, "Grid of open pigeonhole slots with envelopes tucked into some of the compartments",
      tags=["pigeonholes", "mail room", "post sorting", "letter rack", "office mail", "cubbies", "mail slots"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 17, L(S, 1.5, 3.5))),
        detail(seg(2.5, 12, 21.5, 12)),
        detail(seg(8.75, 3.5, 8.75, 12)), detail(seg(15.25, 12, 15.25, 20.5)),
        Part("dot", poly([(11.5, 10.5), (12.2, 6.2), (17, 6.6), (16.3, 10.5)], closed=True)),
        Part("dot", poly([(5.5, 18.8), (6.2, 14.6), (11, 15), (10.3, 18.8)], closed=True)),
    ]


@icon("postage-meter", CAT, "Desk postage machine with a display and a slot, an envelope sliding out below with a printed mark",
      tags=["franking machine", "mail machine", "postage printer", "mailroom", "office", "stamps", "mail"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 10.5, L(S, 2, 3.5))),
        sq(5.5, 5, 7, 3.5, L(S, 0, 1)), dot(17, 7.5, 1.4),
        shell(rect(5, 15, 14, 6.5, L(S, 1, 2.5))),
        sq(15, 16.8, 2.5, 2.2),
    ]


@icon("letter-scale", CAT, "Small desk scale with a curved dial and an envelope resting on its plate",
      tags=["postal scale", "mail scale", "weigh letter", "postage weight", "post office", "dial scale", "balance"])
def _(S):
    return [
        shell(rect(8, 2.5, 8, 5, rr(S, 1))),
        line(seg(5.5, 9, 18.5, 9)),
        shell(poly([(4, 21.5), (6, 12), (18, 12), (20, 21.5)], closed=True, r=S.r * 0.6)),
        detail(arc(12, 19, 4.3, 180, 360)),
        detail(seg(12, 19, 13.6, 15.6)),
    ]


@icon("parcel-scale", CAT, "Flat weighing platform with a box on it and a separate display unit joined by a cord",
      tags=["package scale", "shipping scale", "weigh parcel", "postage weight", "courier", "platform scale", "post office"])
def _(S):
    return [
        shell(rect(5, 7, 9, 8.5, rr(S, 1.5))),
        detail(seg(9.5, 7, 9.5, 11)),
        shell(rect(2.5, 15.5, 14, 5, rr(S, 1.5))),
        shell(rect(17.5, 7.5, 4, 7, rr(S, 1))),
        line(poly([(16.5, 18), (19.5, 18), (19.5, 14.5)], r=S.r * 0.4)),
    ]


@icon("suggestion-box", CAT, "Closed box with a slot in its lid and a folded note being dropped into the slot",
      tags=["feedback box", "comment box", "ideas", "ballot box", "complaints", "idea box", "survey", "drop box"])
def _(S):
    note = rot([(9.5, 2.5), (14.5, 2.5), (14.5, 9.5), (9.5, 9.5)], 18, 12, 9.5)
    return [
        shell(rect(3.5, 9.5, 17, 12, rr(S, 2.5))),
        shell(poly(note, closed=True, r=S.r * 0.3)),
        sq(8, 13, 8, 2),
    ]


@icon("mailing-tube", CAT, "Long cardboard mailing tube with round end caps and a label band around the middle",
      tags=["postal tube", "poster tube", "shipping tube", "cylinder", "rolled print", "blueprint", "package"])
def _(S):
    return [
        shell(rrect(7.5, 5.5, 9, 12, L(S, 0.5, 1.5))),
        shell(rrect(6.5, 3.5, 11, 2.5, L(S, 0.3, 1.2))),
        shell(rrect(6.5, 17, 11, 2.5, L(S, 0.3, 1.2))),
        detail(rseg(7.5, 11.5, 16.5, 11.5)),
    ]


@icon("bubble-wrap", CAT, "Sheet of plastic covered in round air bubbles with a big curled corner",
      tags=["air cushion", "packing", "protective wrap", "fragile", "popping", "packaging", "shipping", "padding"])
def _(S):
    return [
        shell(poly([(3, 3), (21, 3), (21, 13.5), (13.5, 21), (3, 21)], closed=True, r=S.r * 0.5)),
        detail(poly([(21, 13.5), (13.5, 13.5), (13.5, 21)], r=0)),
        dot(6.8, 6.8, 1.4), dot(12, 6.8, 1.4), dot(17.2, 6.8, 1.4), dot(6.8, 12, 1.4), dot(9.4, 17.2, 1.4),
    ]


def _s_piece(cx, cy, deg, k=1.0):
    pts = [(0, -4 * k), (-3.8 * k, -4 * k), (-3.8 * k, 0), (0, 0), (3.8 * k, 0), (3.8 * k, 4 * k), (0, 4 * k)]
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)

    def t(p):
        return (cx + p[0] * c - p[1] * s, cy + p[0] * s + p[1] * c)
    q = [t(p) for p in pts]
    return (f"M{fmt(q[0][0])} {fmt(q[0][1])}C{fmt(q[1][0])} {fmt(q[1][1])} {fmt(q[2][0])} {fmt(q[2][1])} {fmt(q[3][0])} {fmt(q[3][1])}"
            f"C{fmt(q[4][0])} {fmt(q[4][1])} {fmt(q[5][0])} {fmt(q[5][1])} {fmt(q[6][0])} {fmt(q[6][1])}")


@icon("packing-peanuts", CAT, "Small pile of curved S-shaped foam packing pieces",
      tags=["foam peanuts", "loose fill", "void fill", "packaging", "shipping", "cushioning", "box filler"])
def _(S):
    return [
        line(_s_piece(7, 7.5, 40)), line(_s_piece(16.5, 8.5, -30)), line(_s_piece(11.5, 17, 80)),
    ]


@icon("tape-gun", CAT, "Packing tape dispenser with a pistol grip, a tape roll on top and a toothed cutter at the front",
      tags=["tape dispenser", "box sealer", "packing tape", "shipping", "sealing", "warehouse", "packaging"])
def _(S):
    return [
        shell(rect(3, 2.5, 13, 13, L(S, 4, 6.5))),
        dot(9.5, 9, 2.4),
        shell(poly([(5.5, 15.5), (12.5, 15.5), (11.5, 21.5), (4.5, 21.5)], closed=True, r=S.r * 0.6)),
        line(poly([(14, 17.5), (15.5, 15.5), (17, 17.5), (18.5, 15.5), (20, 17.5), (21.5, 15.5)], r=0)),
    ]


@icon("stretch-film", CAT, "Roll of plastic wrap on a hand core with a wide sheet unrolling from it",
      tags=["pallet wrap", "shrink wrap", "cling film", "plastic wrap", "packaging", "warehouse", "shipping", "roll"])
def _(S):
    return [
        shell(rect(3, 4, 7, 14, L(S, 2, 3.5))),
        line(seg(6.5, 2, 6.5, 4)), line(seg(6.5, 18, 6.5, 20.5)),
        shell("M10 7C14 7 17 9 21 9V21C17 21 14 19 10 18Z", stroke_miterlimit="4"),
        detail("M10 12.5C14 12.5 17 14.5 21 14.5"),
    ]


@icon("string-tied-parcel", CAT, "Paper wrapped parcel tied with twine crossing both ways and knotted at the middle",
      tags=["brown paper package", "wrapped parcel", "twine", "string", "mail", "post", "knot", "package"])
def _(S):
    return [
        shell(rect(3, 4.5, 18, 15, L(S, 1.5, 3.5))),
        detail(seg(12, 4.5, 12, 19.5)), detail(seg(3, 12, 21, 12)),
        dot(12, 12, 2.2),
        line(seg(12, 12, 9, 16.5)), line(seg(12, 12, 15, 16.5)),
    ]


@icon("doorstep-parcel", CAT, "Taped box sitting on a doormat in front of the bottom of a closed door",
      tags=["delivered package", "front door delivery", "porch parcel", "drop off", "courier", "delivery", "doormat"])
def _(S):
    return [
        line(poly([(5.5, 19.5), (5.5, 3), (18.5, 3), (18.5, 19.5)], r=S.r * 0.4)),
        dot(16, 10, 1.1),
        shell(rect(8, 12.5, 8, 6, rr(S, 1))),
        line(seg(2.5, 20.5, 21.5, 20.5)),
    ]


@icon("parcel-handover", CAT, "Open hand held out from below carrying a small taped box, as in a delivery handover",
      tags=["delivery", "hand over package", "courier", "receive parcel", "give", "dispatch", "recipient"])
def _(S):
    return [
        shell(rect(7, 2.5, 10, 8.5, rr(S, 1.5))),
        detail(seg(12, 2.5, 12, 7)),
        shell(poly([(2.5, 21.5), (2.5, 16), (6.5, 14), (17, 14), (20, 15.5), (20, 17.5), (17, 18.5), (10.5, 18.5)], closed=True, r=S.r * 0.6)),
    ]
