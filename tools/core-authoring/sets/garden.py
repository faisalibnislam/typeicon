"""TypeIcon Core: garden & farming.

Original drawings of generic garden tools, plants and farm objects (front or side views).
The category takes the `minimal` variant badges in the bottom-right box (13–23), so identifying
details sit top/left where the object allows.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar, rotation, transform_path

CAT = "garden"


def L(S, a, b):
    """Value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def mark(d) -> Part:
    """Small solid shape: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def rot(d, deg, cx, cy):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def leaf(cx, top, bottom, w, S=None):
    """Vertical leaf from top to bottom, width w. Line: pointed tips; Rounded: softer tips."""
    my = (top + bottom) / 2
    k = w * (0.66 if S is None or S.name == "line" else 0.72)
    a = 0.35 if S is None or S.name == "line" else 0.2
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + k)} {fmt(top + (my - top) * a)} {fmt(cx + k)} {fmt(bottom - (bottom - my) * a)} {fmt(cx)} {fmt(bottom)}"
            f"C{fmt(cx - k)} {fmt(bottom - (bottom - my) * a)} {fmt(cx - k)} {fmt(top + (my - top) * a)} {fmt(cx)} {fmt(top)}Z")


def leaf_at(base, tip, w, S=None):
    """Leaf from base point to tip point."""
    bx, by = base
    tx, ty = tip
    ln = math.hypot(tx - bx, ty - by)
    deg = math.degrees(math.atan2(tx - bx, -(ty - by)))
    return rot(leaf(bx, by - ln, by, w, S), deg, bx, by)


# ============================================================================ tools

@icon("watering-can", CAT, "Watering can with a rear handle, long spout and a sprinkler rose",
      tags=["watering", "garden", "plants", "water", "gardening", "irrigation"])
def _(S):
    body = ("M3 20V12.5C3 10.6 5.5 9.5 8.5 9.5C11.5 9.5 14 10.6 14 12.5V20Z" if S.name == "line" else
            "M4.5 20A1.5 1.5 0 0 1 3 18.5V12.5C3 10.6 5.5 9.5 8.5 9.5C11.5 9.5 14 10.6 14 12.5V18.5A1.5 1.5 0 0 1 12.5 20Z")
    rose = rot(rect(17.25, 6.5, 4.5, 2.5, L(S, 0, 1)), 35, 19.5, 7.75)
    return [
        shell(body),
        line("M4 12.5C2.5 8.5 4.5 4.5 8.5 4.5C11 4.5 12.7 6.5 13 10.3"),
        line(seg(14, 17, 18.3, 9.5)),
        shell(rose),
    ]


@icon("garden-rake", CAT, "Garden rake with a long handle and four tines",
      tags=["rake", "leaves", "gardening", "lawn", "tool", "yard work"], aliases=["leaf-rake"])
def _(S):
    return [
        line(seg(12, 2, 12, 14)),
        line(seg(4, 14, 20, 14) if S.name == "line" else seg(4.5, 14, 19.5, 14)),
        *[line(seg(x, 14, x, 20.5 if S.name == "line" else 20)) for x in (5.5, 9.83, 14.17, 18.5)],
    ]


@icon("wheelbarrow", CAT, "Wheelbarrow with a tray, front wheel and handles",
      tags=["barrow", "garden cart", "construction", "gardening", "haul", "farm"], aliases=["barrow"])
def _(S):
    return [
        shell(poly([(3, 7.5), (16, 7.5), (14, 14), (7, 14)], closed=True, r=S.r)),
        line(seg(15, 11, 21, 11) if S.name == "line" else seg(15, 11, 20.5, 11)),
        shell(circle(7, 18, 2.75)),
        line(seg(13, 14, 14.5, 21)),
    ]


@icon("hedge-trimmer", CAT, "Powered hedge trimmer with a toothed blade",
      tags=["hedge cutter", "trimmer", "garden tool", "pruning", "bush", "gardening"], aliases=["hedge-cutter"])
def _(S):
    parts = [
        shell(rect(3, 11, 8, 5, rr(S, 1.5))),
        line("M4.5 11V9A1.5 1.5 0 0 1 6 7.5H8A1.5 1.5 0 0 1 9.5 9V11" if S.name != "line" else "M4.5 11V7.5H9.5V11"),
        line(seg(11, 13.5, 21, 13.5 if S.name == "line" else 13.5)),
    ]
    for x in (13, 16, 19):
        parts.append(mark(poly([(x - 1, 12.6), (x, 10.2), (x + 1, 12.6)], closed=True)))
        parts.append(mark(poly([(x + 0.5, 14.4), (x + 1.5, 16.8), (x + 2.5, 14.4)], closed=True)))
    return [rot_part(p, -25) for p in parts]


def rot_part(p, deg, cx=12, cy=12):
    return Part(p.kind, rot(p.d, deg, cx, cy) if p.kind != "line" else _rot_open(p.d, deg, cx, cy), p.attrs)


def _rot_open(d, deg, cx, cy):
    """Rotate an open path d-string (keeps it open) by transforming its numbers."""
    import re
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    toks = re.findall(r"[A-Za-z]|-?\d*\.?\d+(?:e-?\d+)?", d)
    out, i, cmd = [], 0, None
    nums = {"M": 2, "L": 2, "C": 6, "Q": 4, "A": 7, "H": 1, "V": 1}
    cur = (0.0, 0.0)
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t
            i += 1
            if cmd in "Zz":
                out.append("Z")
            continue
        n = nums[cmd]
        vals = [float(v) for v in toks[i:i + n]]
        i += n

        def R(x, y):
            return (cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca)
        if cmd == "H":
            p = R(vals[0], cur[1]); cur = (vals[0], cur[1]); out.append("L" + f"{fmt(p[0])} {fmt(p[1])}")
        elif cmd == "V":
            p = R(cur[0], vals[0]); cur = (cur[0], vals[0]); out.append("L" + f"{fmt(p[0])} {fmt(p[1])}")
        elif cmd == "A":
            p = R(vals[5], vals[6]); cur = (vals[5], vals[6])
            out.append(f"A{fmt(vals[0])} {fmt(vals[1])} {fmt(vals[2] + deg)} {int(vals[3])} {int(vals[4])} {fmt(p[0])} {fmt(p[1])}")
        else:
            pts = [R(vals[j], vals[j + 1]) for j in range(0, n, 2)]
            cur = (vals[-2], vals[-1])
            out.append(cmd + " ".join(f"{fmt(x)} {fmt(y)}" for x, y in pts))
    return "".join(out)


@icon("lawn-mower", CAT, "Push lawn mower with a long handle",
      tags=["mower", "lawnmower", "grass", "lawn", "garden", "cutting"], aliases=["lawnmower", "mower"])
def _(S):
    deck = ("M3 15V13C3 11.9 3.9 11 5 11H12.5L14.5 15Z" if S.name == "line" else
            "M4.5 15A1.5 1.5 0 0 1 3 13.5V13C3 11.9 3.9 11 5 11H12.5L13.8 13.6A1 1 0 0 1 12.9 15Z")
    return [
        shell(deck),
        line(seg(12, 11, 18, 4)),
        line(seg(16, 3.5, 21, 3.5) if S.name == "line" else seg(16.5, 3.5, 20.5, 3.5)),
        shell(circle(6, 18.5, 2.5)), shell(circle(12.5, 18.5, 2.5)),
    ]


def _spiral(cx, cy, r0, r1, turns, start=0.0, n=60):
    pts = []
    for i in range(n + 1):
        t = i / n
        a = math.radians(start + 360 * turns * t)
        r = r0 + (r1 - r0) * t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


@icon("garden-hose", CAT, "Coiled garden hose with a spray nozzle",
      tags=["hose", "hosepipe", "watering", "garden", "water", "irrigation"], aliases=["hosepipe"])
def _(S):
    coil = _spiral(9.5, 13, 2.25, 7.5, 1.6, start=90)
    d = "M" + "L".join(f"{fmt(x)} {fmt(y)}" for x, y in coil)
    ex, ey = coil[-1]
    return [
        line(d),
        line(f"M{fmt(ex)} {fmt(ey)}C{fmt(ex + 3)} {fmt(ey - 3)} 14 4.5 16.5 4.5"),
        shell(rect(16.5, 3, 4.5, 3, rr(S, 1))),
        line(seg(18, 6, 18, 9)),
    ]


# ============================================================================ planting

@icon("seed-bag", CAT, "Tied sack of seeds with a sprout on the front",
      tags=["seeds", "sack", "sowing", "planting", "gardening", "farm"], aliases=["seed-sack"])
def _(S):
    sack = ("M9 3H15L14 6.5C17.8 8.3 19.5 12 19.5 16C19.5 19.5 17 21 12 21C7 21 4.5 19.5 4.5 16C4.5 12 6.2 8.3 10 6.5Z"
            if S.name == "line" else
            "M9.5 3H14.5A0.6 0.6 0 0 1 15 3.7L14 6.5C17.8 8.3 19.5 12 19.5 16C19.5 19.5 17 21 12 21C7 21 4.5 19.5 4.5 16C4.5 12 6.2 8.3 10 6.5L9 3.7A0.6 0.6 0 0 1 9.5 3Z")
    return [
        shell(sack),
        detail(seg(10, 6.5, 14, 6.5)),
        detail(seg(12, 18, 12, 13)),
        detail("M12 14.5C12 12.5 10.8 11.5 8.8 11.5C8.8 13.5 10 14.5 12 14.5"),
        detail("M12 13.5C12 11.5 13.2 10.5 15.2 10.5C15.2 12.5 14 13.5 12 13.5"),
    ]


@icon("potted-plant", CAT, "Tulip growing in a flower pot",
      tags=["flower pot", "plant", "flower", "planter", "gardening", "grow"], aliases=["flower-pot", "flowerpot"])
def _(S):
    tulip = ("M8.5 3.5L10.3 5.5L12 3L13.7 5.5L15.5 3.5V7C15.5 9 14 10.5 12 10.5C10 10.5 8.5 9 8.5 7Z" if S.name == "line" else
             "M8.5 4.2C8.5 3.7 9 3.5 9.4 3.9L10.3 5.1L11.4 3.4C11.7 3 12.3 3 12.6 3.4L13.7 5.1L14.6 3.9C15 3.5 15.5 3.7 15.5 4.2V7C15.5 9 14 10.5 12 10.5C10 10.5 8.5 9 8.5 7Z")
    return [
        shell(tulip),
        line(seg(12, 10.5, 12, 14.5)),
        shell(leaf_at((11, 14.5), (6, 11.5), 2.2, S)),
        shell(leaf_at((13, 14.5), (18, 11.5), 2.2, S)),
        shell(rect(6, 14.5, 12, 3, rr(S, 1))),
        shell(poly([(7, 17.5), (17, 17.5), (16, 21), (8, 21)], closed=True, r=S.r * 0.5)),
    ]


@icon("fruit-tree", CAT, "Tree with a round crown bearing fruit",
      tags=["apple tree", "orchard", "fruit", "tree", "garden", "harvest"], aliases=["apple-tree"])
def _(S):
    return [
        shell(circle(12, 9.5, 7.5)),
        line(seg(12, 17, 12, 21.5) if S.name == "line" else seg(12, 17, 12, 21)),
        detail(poly([(12, 17), (12, 13.5), (15, 10.5)], r=S.r)),
        dot(8.5, 8, 1.4), dot(13, 5.5, 1.4), dot(8.5, 12.5, 1.4), dot(16.5, 6.5, 1.2),
    ]


# ============================================================================ crops and farm

@icon("wheat", CAT, "Ear of wheat with grains along the stalk",
      tags=["grain", "cereal", "crop", "farm", "harvest", "bread"], aliases=["wheat-ear"])
def _(S):
    parts = [line(seg(12, 8, 12, 21.5) if S.name == "line" else seg(12, 8, 12, 21))]
    parts.append(shell(leaf(12, 2.5, 7.5, 2.6, S)))
    for y in (11, 15):
        parts.append(shell(leaf_at((11.2, y), (7, y - 4.5), 2.6, S)))
        parts.append(shell(leaf_at((12.8, y), (17, y - 4.5), 2.6, S)))
    return parts


@icon("crop-corn", CAT, "Corn plant with a stalk, long leaves and a cob",
      tags=["corn", "maize", "crop", "farm", "field", "agriculture"], aliases=["corn-plant", "corn-stalk"])
def _(S):
    return [
        line(seg(14, 3, 14, 21.5) if S.name == "line" else seg(14, 3, 14, 21)),
        shell(rot(ellipse(9, 9.5, 2.5, 5), -15, 9, 9.5)),
        detail(rot(seg(9, 6.5, 9, 12.5), -15, 9, 9.5)),
        line("M14 14C10.5 13.5 7 15.5 4.5 19"),
        line("M14 10C17 9.5 19.5 10.5 21 13"),
        line("M14 6C15.5 4.5 17.5 4 19.5 4.5"),
    ]


@icon("farm-fence", CAT, "Post-and-rail farm fence with a diagonal brace",
      tags=["ranch fence", "paddock", "rail fence", "farm", "field", "boundary"], aliases=["ranch-fence", "rail-fence"])
def _(S):
    posts = [shell(rect(4, 4, 4, 17, L(S, 0.5, 2))), shell(rect(16, 4, 4, 17, L(S, 0.5, 2)))]
    rails = [line(seg(8, 8.5, 16, 8.5)), line(seg(8, 15.5, 16, 15.5)),
             line(seg(8, 15.5, 16, 8.5))]
    return [*posts, *rails]


@icon("scarecrow", CAT, "Scarecrow with a straw hat and outstretched arms",
      tags=["farm", "field", "crows", "harvest", "autumn", "halloween"])
def _(S):
    shirt = [(3.5, 11), (20.5, 11), (20.5, 14.5), (15, 14.5), (15, 18.5), (9, 18.5), (9, 14.5), (3.5, 14.5)]
    return [
        shell(poly([(12, 1.8), (14.6, 4.8), (9.4, 4.8)], closed=True, r=S.r * 0.5)),
        line(seg(7.5, 5, 16.5, 5) if S.name == "line" else seg(8, 5, 16, 5)),
        shell(circle(12, 7.75, 2)),
        shell(poly(shirt, closed=True, r=S.r * 0.66)),
        detail(seg(10.5, 11, 13.5, 11)),
        line(seg(12, 18.5, 12, 21.5) if S.name == "line" else seg(12, 18.5, 12, 21)),
    ]


def _skep():
    tiers = [(4, 16.5, 16, 4.5), (5.5, 12.5, 13, 4), (7.5, 8.5, 9, 4), (10, 5, 4, 3.5)]
    return tiers


@icon("beehive", CAT, "Traditional woven beehive with an entrance",
      tags=["bee", "hive", "honey", "apiary", "skep", "beekeeping"], aliases=["skep", "hive"])
def _(S):
    r = L(S, 1.5, 2)
    tiers = _skep()
    body = union(*[rect(x, y, w, h, min(r, h / 2)) for x, y, w, h in tiers])
    parts = [shell(body)]
    for x, y, w, h in tiers[1:]:
        parts.append(detail(seg(x + 0.5, y + h, x + w - 0.5, y + h)))
    parts.append(detail("M10 21V19.5A2 2 0 0 1 14 19.5V21"))
    return parts


@icon("greenhouse", CAT, "Glass greenhouse with a pitched roof and glazing bars",
      tags=["glasshouse", "hothouse", "nursery", "plants", "gardening", "grow"], aliases=["glasshouse"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 10), (12, 3), (21, 10), (21, 21)], closed=True, r=S.r)),
        detail(seg(3, 10, 21, 10)),
        detail(seg(8.5, 10, 8.5, 21)), detail(seg(15.5, 10, 15.5, 21)),
        detail(seg(12, 3, 12, 10)),
        detail(seg(3, 15.5, 8.5, 15.5)), detail(seg(15.5, 15.5, 21, 15.5)),
    ]


@icon("harvest", CAT, "Sheaf of grain tied with a band",
      tags=["crop", "sheaf", "harvest festival", "farm", "autumn", "grain"], aliases=["sheaf"])
def _(S):
    pv, ang = (12, 15), 40
    head = leaf(12, 2.5, 9, 2.6, S)
    heads = [shell(head), shell(rot(head, -ang, *pv)), shell(rot(head, ang, *pv))]
    bl, br = polar(12, 15, 6, -90 - ang), polar(12, 15, 6, -90 + ang)
    end = 21.5 if S.name == "line" else 21
    stalks = [line(seg(12, 9, 12, 13.5)), line(seg(12, 16.5, 12, end)),
              line(seg(bl[0], bl[1], 10.74, 13.5)), line(seg(br[0], br[1], 13.26, 13.5)),
              line(seg(10.75, 16.5, 7, end - 0.5)), line(seg(13.25, 16.5, 17, end - 0.5))]
    return [*heads, *stalks, shell(rect(9, 13.5, 6, 3, rr(S, 1)))]


@icon("vegetable-basket", CAT, "Basket of vegetables with leafy tops and a tomato",
      tags=["vegetables", "produce", "basket", "groceries", "farm", "harvest"], aliases=["veggie-basket"])
def _(S):
    return [
        line(seg(8, 11, 5, 5)), line(seg(8, 11, 8.5, 4)), line(seg(8, 11, 11.5, 5.5)),
        shell("M12.5 11A3.5 3.5 0 0 1 19.5 11Z"),
        shell(poly([(3, 11), (21, 11), (19, 21), (5, 21)], closed=True, r=S.r)),
        detail(seg(3.7, 14.5, 20.3, 14.5)), detail(seg(9, 11, 9.8, 21)), detail(seg(15, 11, 14.2, 21)),
    ]


@icon("compost", CAT, "Slatted compost bin with a leaf sprouting from the heap",
      tags=["composting", "compost bin", "organic", "waste", "soil", "eco"], aliases=["compost-bin"])
def _(S):
    return [
        shell(leaf_at((12, 9), (15, 2.5), 3, S)),
        line("M5 11C6 9.3 8.5 8.5 12 8.5C15.5 8.5 18 9.3 19 11"),
        shell(poly([(3, 11), (21, 11), (21, 21), (3, 21)], closed=True, r=S.r)),
        detail(seg(7.5, 11, 7.5, 21)), detail(seg(12, 11, 12, 21)), detail(seg(16.5, 11, 16.5, 21)),
    ]


@icon("sprinkler", CAT, "Lawn sprinkler throwing a fan of water drops",
      tags=["lawn sprinkler", "watering", "irrigation", "garden", "water", "grass"], aliases=["lawn-sprinkler"])
def _(S):
    drops = [dot(*polar(12, 13, 5.5, a), 1.2) for a in (-160, -125, -90, -55, -20)]
    drops += [dot(*polar(12, 13, 9.5, a), 1.2) for a in (-145, -108, -72, -35)]
    return [
        *drops,
        shell(rect(9.5, 13, 5, 3.5, rr(S, 1.5))),
        line(seg(12, 16.5, 12, 21)),
        line(seg(8, 21, 16, 21) if S.name == "line" else seg(8.5, 21, 15.5, 21)),
    ]
