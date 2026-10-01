"""TypeIcon Core: farm (batch 003). Farm machinery, garden structures and crop tools."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar, rotation, transform_path

CAT = "farm"


def L(S, a, b):
    """Value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def mark(d) -> Part:
    return Part("dot", d)


def rot(d, deg, cx, cy):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def chord(cx, cy, r, dir_deg, off):
    """Chord of a circle perpendicular offset `off` from centre, running along direction dir_deg."""
    d = math.radians(dir_deg)
    ux, uy = math.cos(d), math.sin(d)
    nx, ny = -uy, ux
    h = math.sqrt(max(r * r - off * off, 0))
    px, py = cx + nx * off, cy + ny * off
    return seg(px - ux * h, py - uy * h, px + ux * h, py + uy * h)


# ============================================================================ chunk 1

@icon("bale-wrapper", CAT, "Round hay bale on a turntable with a film roll arm beside it",
      tags=["bale wrapping", "silage", "hay bale", "wrap", "plastic film", "haylage", "baler"])
def _(S):
    return [
        shell(circle(9, 10.5, 6.5)),
        detail(arc(9, 10.5, 3, 200, 110)),
        line(seg(2.5, 20, 15.5, 20)),
        line(seg(21, 11.5, 21, 21)),
        shell(rect(19, 3.5, 4, 7, min(S.R, 1.5))),
    ]


@icon("rain-gun", CAT, "Irrigation sprinkler cannon on a small cart throwing an arc of water",
      tags=["big gun", "sprinkler", "irrigation", "water cannon", "field watering", "spray", "reel"])
def _(S):
    return [
        shell(rect(2.5, 13, 12, 3.5, min(S.R, 1.5))),
        dot(6, 20, 1.75),
        dot(11.5, 20, 1.75),
        line(seg(8.5, 13, 14.5, 8.5)),
        line("M16.5 8C19 4 22 6.5 22 12"),
        dot(19.5, 12, 1),
    ]


@icon("flax-plant", CAT, "Slender flax plant with narrow leaves, a flower and a round seed boll",
      tags=["flax", "linen", "linseed", "fibre crop", "flower", "crop", "plant"])
def _(S):
    flower = poly(regular(12, 5.5, 3.4, 5), closed=True, r=S.r * 0.5) if S.name == "line" else circle(12, 5.5, 3)
    return [
        shell(flower),
        line(seg(12, 9, 12, 21.5)),
        line(seg(12, 19, 7, 15.5)),
        line(seg(12, 15, 16.5, 11.5)),
        dot(18.5, 9.5, 2),
    ]


@icon("corn-shock", CAT, "Teepee-shaped bundle of dried corn stalks tied with a band near the top",
      tags=["corn shock", "corn stalks", "autumn", "fall decoration", "harvest", "fodder", "stooks"])
def _(S):
    return [
        shell(poly([(12, 6), (19, 21), (5, 21)], closed=True, r=S.r)),
        detail(seg(9, 11.5, 15, 11.5)),
        detail(seg(10.5, 14.5, 9.5, 21)),
        detail(seg(13.5, 14.5, 14.5, 21)),
        line(seg(12, 6.5, 8, 2.5)),
        line(seg(12, 6.5, 16, 2.5)),
    ]


@icon("pumpkin-patch", CAT, "Two ribbed pumpkins with stems, sitting on the ground",
      tags=["pumpkin", "patch", "halloween", "autumn", "harvest", "vine", "pick your own"])
def _(S):
    big = union(ellipse(9, 14, 3.4, 5.2), ellipse(5.6, 14.5, 2.6, 4.6), ellipse(12.4, 14.5, 2.6, 4.6))
    return [
        shell(big),
        line(seg(9, 9, 9, 4.5)),
        shell(ellipse(19.3, 17.5, 2.7, 2.7)),
        line(seg(19.3, 14.8, 19.3, 12.5)),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("irrigation-valve", CAT, "Pipe with a handwheel valve on top and a water drop at the outlet",
      tags=["valve", "water pipe", "irrigation", "handwheel", "tap", "pipeline", "water control"])
def _(S):
    return [
        shell(rect(2.5, 12.5, 14.5, 5, min(S.R, 2))),
        detail(seg(5.5, 12.5, 5.5, 17.5)),
        detail(seg(14, 12.5, 14, 17.5)),
        line(seg(9.75, 12.5, 9.75, 7)),
        line(seg(5, 6, 14.5, 6)),
        shell("M20 15C20 15 17.5 18 17.5 19.5a2.5 2.5 0 0 0 5 0C22.5 18 20 15 20 15Z"),
    ]


@icon("woven-wire-fence", CAT, "Field fence of square wire mesh stretched between two posts",
      tags=["field fence", "wire fence", "livestock fence", "mesh", "fencing", "pasture", "boundary"])
def _(S):
    return [
        shell(rect(3, 5, 18, 13, 0)),
        detail(seg(3, 9.5, 21, 9.5)),
        detail(seg(3, 13.5, 21, 13.5)),
        detail(seg(9, 5, 9, 18)),
        detail(seg(15, 5, 15, 18)),
        line(seg(3, 2.5, 3, 21.5)),
        line(seg(21, 2.5, 21, 21.5)),
    ]


def _zig_mesh(s, x0, y0, nx, rows):
    """Hexagonal mesh as zigzag rows joined by short verticals; returns list of path strings."""
    w = math.sqrt(3) * s
    out, nodes = [], []
    for k in range(rows):
        base = y0 + k * 1.5 * s
        pts = []
        for i in range(nx + 1):
            valley = (i + k) % 2 == 1
            pts.append((x0 + i * w / 2, base + (s / 2 if valley else 0)))
        nodes.append(pts)
        out.append(pts)
    return out, w


@icon("chicken-wire", CAT, "Patch of hexagonal wire mesh showing the honeycomb pattern",
      tags=["poultry netting", "wire mesh", "hexagonal mesh", "chicken coop", "netting", "enclosure", "fencing"])
def _(S):
    s = 3.6
    rowsp, w = _zig_mesh(s, 3, 3.2, 6, 3)
    parts = [line(poly(p, r=S.r * 0.4)) for p in rowsp]
    for k in range(2):
        for i in range(7):
            if (i + k) % 2 == 1:
                x = rowsp[k][i][0]
                parts.append(line(seg(x, rowsp[k][i][1], x, rowsp[k + 1][i][1])))
    return parts


@icon("corn-sheller", CAT, "Hand-cranked corn sheller box with a cob fed in at the top and a crank at the side",
      tags=["corn", "sheller", "maize", "kernels", "crank", "hand tool", "threshing"])
def _(S):
    return [
        shell(ellipse(9.5, 5.5, 2.8, 4)),
        detail(seg(7.5, 4.5, 11.5, 4.5)),
        detail(seg(7.5, 7, 11.5, 7)),
        shell(rect(3.5, 11, 12, 9.5, rr(S, 2.5))),
        detail(circle(9.5, 15.75, 2.5)),
        line(poly([(15.5, 15.75), (20.5, 15.75), (20.5, 20.5)], r=S.r * 0.5)),
    ]


@icon("airblast-sprayer", CAT, "Tank trailer with a round fan at the back blowing a mist up and out",
      tags=["orchard sprayer", "mist blower", "pesticide", "fan sprayer", "crop protection", "spraying", "vineyard"])
def _(S):
    cx, cy = 17, 13.5
    blades = "".join(seg(cx, cy, *polar(cx, cy, 3.3, a)) for a in (90, 210, 330))
    return [
        shell(rect(2.5, 10, 9, 6.5, rr(S, 3))),
        dot(6.5, 19.5, 1.75),
        shell(circle(cx, cy, 4.5)),
        detail(blades),
        line("M14 7C16 3.5 19.5 3.5 21.5 6"),
    ]


@icon("frost-fan", CAT, "Tall orchard pole topped with a two-bladed propeller fan",
      tags=["wind machine", "frost protection", "orchard", "propeller", "fan", "cold air", "blossom"])
def _(S):
    return [
        shell(poly([(11, 7), (3, 3), (3, 8)], closed=True, r=S.r * 0.6)),
        shell(poly([(13, 7), (21, 4), (21, 9)], closed=True, r=S.r * 0.6)),
        dot(12, 7, 1.6),
        line(seg(12, 9, 12, 21.5)),
        line(seg(8, 21.5, 16, 21.5)),
    ]


@icon("farm-bell", CAT, "Bell hung in a U-shaped yoke on top of a post",
      tags=["dinner bell", "ranch bell", "call bell", "yoke", "alarm", "homestead", "rope bell"])
def _(S):
    bell = "M6.5 13.5Q9.5 12.5 9.5 9A2.5 5.5 0 0 1 14.5 9Q14.5 12.5 17.5 13.5Z"
    return [
        line(poly([(3.5, 6), (3.5, 15.5), (20.5, 15.5), (20.5, 6)], r=S.r * 0.7)),
        shell(bell),
        shell(rect(10, 15.5, 4, 6, 0)),
    ]


@icon("wagon-wheel", CAT, "Wooden wagon wheel with a thick rim, round hub and straight spokes",
      tags=["cart wheel", "wheel", "wagon", "western", "pioneer", "spokes", "old farm"])
def _(S):
    spokes = "".join(seg(*polar(12, 12, 2.5, a), *polar(12, 12, 7.5, a)) for a in range(0, 360, 45))
    hub = circle(12, 12, 2.6) if S.name == "rounded" else rect(9.4, 9.4, 5.2, 5.2)
    return [
        line(circle(12, 12, 9)),
        line(circle(12, 12, 7)),
        line(spokes),
        shell(hub),
    ]


@icon("lawn-sweeper", CAT, "Push lawn sweeper with a brush roller under a low body and a collection bag",
      tags=["leaf sweeper", "grass sweeper", "lawn", "yard work", "push sweeper", "garden cleanup", "brush"])
def _(S):
    return [
        shell(rect(8, 9, 9, 5.5, rr(S, 2))),
        shell(poly([(17, 9.5), (22, 11.5), (22, 17), (17, 14)], closed=True, r=S.r * 0.5)),
        shell(circle(12.5, 18.5, 2.8)),
        dot(12.5, 18.5, 0.9),
        line(poly([(9, 9), (5, 3)])),
        line(seg(2.5, 3, 7, 3)),
    ]


def _leaf(cx, top, bottom, w):
    my = (top + bottom) / 2
    k = w * 0.66
    a = 0.35
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + k)} {fmt(top + (my - top) * a)} {fmt(cx + k)} {fmt(bottom - (bottom - my) * a)} {fmt(cx)} {fmt(bottom)}"
            f"C{fmt(cx - k)} {fmt(bottom - (bottom - my) * a)} {fmt(cx - k)} {fmt(top + (my - top) * a)} {fmt(cx)} {fmt(top)}Z")


def leaf_at(base, tip, w):
    bx, by = base
    tx, ty = tip
    ln = math.hypot(tx - bx, ty - by)
    deg = math.degrees(math.atan2(tx - bx, -(ty - by)))
    return rot(_leaf(bx, by - ln, by, w), deg, bx, by)


# ============================================================================ chunk 2

@icon("grow-bag", CAT, "Soft fabric grow bag with two side handles and a leafy plant growing from the top",
      tags=["fabric pot", "planter bag", "container garden", "potato bag", "plant pot", "gardening", "patio"])
def _(S):
    return [
        shell(poly([(5, 11.5), (19, 11.5), (20.5, 19), (19, 21.5), (5, 21.5), (3.5, 19)], closed=True, r=S.r)),
        line(poly([(5, 13.5), (2.5, 13.5), (2.5, 16.5)], r=S.r * 0.5)),
        line(poly([(19, 13.5), (21.5, 13.5), (21.5, 16.5)], r=S.r * 0.5)),
        line(seg(12, 11.5, 12, 7)),
        shell(leaf_at((12, 8), (6, 4), 4.5)),
        shell(leaf_at((12, 8), (18, 4), 4.5)),
    ]


@icon("hydroponic-tower", CAT, "Tall vertical growing tower with plants in its sides and a water tank at the base",
      tags=["vertical farm", "hydroponics", "tower garden", "aeroponics", "indoor farming", "soilless", "grow tower"])
def _(S):
    return [
        shell(rect(8, 2.5, 8, 14.5, rr(S, 2))),
        detail(seg(10.5, 7, 13.5, 7)),
        detail(seg(10.5, 12, 13.5, 12)),
        line(seg(8, 5, 4.5, 3.5)),
        line(seg(16, 9.5, 19.5, 8)),
        line(seg(8, 14.5, 4.5, 13)),
        shell(rect(4, 17, 16, 4.5, rr(S, 2))),
    ]


@icon("farm-fuel-tank", CAT, "Horizontal fuel tank raised on a stand with a hose and nozzle hanging down",
      tags=["diesel tank", "fuel storage", "petrol", "gas tank", "refuelling", "farm diesel", "bowser"])
def _(S):
    return [
        shell(rect(2.5, 4, 15, 8, min(S.R, 4) if S.name == "rounded" else 2)),
        line(seg(6, 12, 6, 21.5)),
        line(seg(14, 12, 14, 21.5)),
        line(seg(3.5, 21.5, 16.5, 21.5)),
        line(poly([(17.5, 8), (20.5, 8), (20.5, 15)], r=S.r * 0.5)),
        shell(rect(19, 15, 3, 4.5, min(S.R, 1))),
    ]


@icon("bat-box", CAT, "Tall narrow wooden bat box with a sloped roof and a slot entrance at the bottom",
      tags=["bat house", "bat roost", "wildlife", "nest box", "conservation", "garden wildlife", "habitat"])
def _(S):
    return [
        shell(rect(7, 8, 10, 13.5, 0)),
        shell(poly([(4.5, 9), (4.5, 6.5), (19.5, 3), (19.5, 5.5)], closed=True, r=S.r * 0.3)),
        detail(seg(10, 18, 14, 18)),
    ]


@icon("hedgehog-house", CAT, "Low domed wooden shelter with a small arched entrance tunnel",
      tags=["hedgehog", "wildlife shelter", "hibernation", "garden wildlife", "hog house", "nest", "habitat"])
def _(S):
    return [
        shell("M3 20V15Q3 6 12 6Q21 6 21 15V20Z" if S.name == "line" else "M3 20V15C3 8 7 6 12 6S21 8 21 15V20Z"),
        detail("M9 20V17.5A3 3 0 0 1 15 17.5V20"),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("tobacco-plant", CAT, "Tall tobacco plant with large broad leaves up the stalk and flowers on top",
      tags=["tobacco", "leaf crop", "nicotiana", "cash crop", "curing", "smoking", "cigar"])
def _(S):
    return [
        line(seg(12, 21.5, 12, 7.5)),
        shell(leaf_at((12, 21), (3, 16), 5)),
        shell(leaf_at((12, 16.5), (21, 11.5), 5)),
        shell(leaf_at((12, 12), (4, 7.5), 4.5)),
        dot(12, 4, 1.4),
        dot(9, 6, 1.25),
        dot(15, 6, 1.25),
    ]


@icon("corn-dolly", CAT, "Small woven straw figure with a loop at the top, a braided body and ears of grain at the base",
      tags=["harvest charm", "straw figure", "straw craft", "folk art", "harvest festival", "wheat weaving", "tradition"])
def _(S):
    return [
        line("M12 7.5C9.5 4.5 9.5 2.5 12 2.5C14.5 2.5 14.5 4.5 12 7.5"),
        shell(poly([(12, 7.5), (16.5, 13), (12, 18.5), (7.5, 13)], closed=True, r=S.r)),
        detail(seg(9.5, 10.5, 14.5, 15.5)),
        line(seg(12, 18.5, 7, 22)),
        line(seg(12, 18.5, 17, 22)),
        line(seg(12, 18.5, 12, 22)),
    ]


@icon("garden-bridge", CAT, "Small arched footbridge with railings curving over water",
      tags=["footbridge", "pond bridge", "arched bridge", "landscaping", "japanese garden", "crossing", "water feature"])
def _(S):
    return [
        line("M2.5 16Q12 8 21.5 16"),
        line("M2.5 10.5Q12 2.5 21.5 10.5"),
        line(seg(2.5, 10.5, 2.5, 16)),
        line(seg(21.5, 10.5, 21.5, 16)),
        line(seg(7.25, 7.5, 7.25, 13)),
        line(seg(12, 6.5, 12, 12)),
        line(seg(16.75, 7.5, 16.75, 13)),
        line("M2 20.5q2.5-1.5 5 0t5 0t5 0t5 0"),
    ]


@icon("grape-harvester", CAT, "Tall harvester straddling a row of vines on high wheels",
      tags=["vineyard", "wine harvest", "vintage", "grape picking", "viticulture", "machine harvester", "vines"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 7, rr(S, 2.5))),
        line(seg(5.5, 9.5, 5.5, 16.5)),
        line(seg(18.5, 9.5, 18.5, 16.5)),
        shell(circle(5.5, 19, 2.5)) if False else dot(5.5, 19.5, 2.25),
        dot(18.5, 19.5, 2.25),
        dot(10.5, 15, 1.3),
        dot(13.5, 15, 1.3),
        dot(12, 18, 1.3),
        line(seg(12, 13, 12, 11)),
    ]


@icon("tree-shaker", CAT, "Machine with a clamp gripping a tree trunk while fruit falls from the branches",
      tags=["trunk shaker", "orchard harvest", "nut harvest", "fruit falling", "olive harvest", "almond", "harvesting"])
def _(S):
    return [
        shell(rect(2.5, 14.5, 6, 6, rr(S, 2))),
        line(seg(8.5, 17, 11.5, 17)),
        solid(rect(11.5, 14, 2, 6)),
        shell(poly(regular(17, 7, 4.8, 8, -22.5), closed=True, r=0) if S.name == "line" else circle(17, 7, 4.5)),
        shell(rect(15, 11.5, 4, 9.5, 0)),
        dot(4, 7, 1.3),
        dot(8, 4.5, 1.3),
        dot(8.5, 10, 1.3),
    ]


@icon("hay-tedder", CAT, "Two spinning star-shaped tine rotors on a frame flicking hay into the air",
      tags=["hay turner", "haymaking", "tines", "rotary tedder", "drying hay", "forage", "meadow"])
def _(S):
    def star(cx, cy, r):
        return "".join(seg(cx, cy, *polar(cx, cy, r, a)) for a in range(-90, 270, 60))
    return [
        line(seg(6.5, 16, 17.5, 16)),
        line(star(6.5, 16, 4.8)),
        line(star(17.5, 16, 4.8)),
        line(seg(12, 16, 12, 9)),
        dot(8, 5.5, 1.1),
        dot(12, 4, 1.1),
        dot(16, 5.5, 1.1),
    ]


@icon("land-roller", CAT, "Wide set of ridged rollers on a frame with a hitch drawbar",
      tags=["field roller", "cultivator roller", "soil roller", "flattening", "seedbed", "ring roller", "tillage"])
def _(S):
    return [
        line(seg(3, 8, 21, 8)),
        line(seg(12, 8, 12, 2.5)),
        shell(rect(3, 11, 4.5, 10, rr(S, 1.5))),
        shell(rect(9.75, 11, 4.5, 10, rr(S, 1.5))),
        shell(rect(16.5, 11, 4.5, 10, rr(S, 1.5))),
        detail(seg(3, 16, 7.5, 16)),
        detail(seg(9.75, 16, 14.25, 16)),
        detail(seg(16.5, 16, 21, 16)),
    ]


@icon("grain-cart", CAT, "Hopper wagon on two big tires with an auger arm raised over one side",
      tags=["chaser bin", "grain wagon", "harvest logistics", "auger", "combine", "hopper", "unloading"])
def _(S):
    return [
        shell(poly([(2.5, 6), (17.5, 6), (14.5, 14), (5.5, 14)], closed=True, r=S.r)),
        shell(circle(7.5, 18.5, 3.2)),
        shell(circle(14.5, 18.5, 3.2)),
        line(seg(15, 8.5, 21.5, 3)),
        line(seg(21.5, 3, 21.5, 6.5)),
    ]


@icon("feed-mixer", CAT, "Wagon with a tall tapered tub and a spiral auger visible inside",
      tags=["tmr mixer", "livestock feed", "feed wagon", "total mixed ration", "cattle feed", "auger", "dairy"])
def _(S):
    return [
        shell(poly([(4.5, 3.5), (19.5, 3.5), (17.5, 17), (6.5, 17)], closed=True, r=S.r)),
        detail(seg(12, 5.5, 12, 15)),
        detail(seg(8.5, 9, 12, 7.5)),
        detail(seg(12, 12, 15.5, 10.5)),
        dot(8, 20.5, 1.6),
        dot(16, 20.5, 1.6),
    ]


# ============================================================================ chunk 3

@icon("bulk-milk-tank", CAT, "Horizontal milk tank on legs with a hatch, an agitator motor on top and an outlet valve",
      tags=["milk cooler", "dairy", "cold storage", "milk vat", "stainless tank", "milking parlour", "farm dairy"])
def _(S):
    return [
        shell(rect(2.5, 9, 19, 8, min(S.R, 3.5) if S.name == "rounded" else 2)),
        shell(rect(6, 5, 4, 4, 0)),
        shell(rect(13.5, 3, 4, 6, 0)),
        line(seg(6, 17, 4.5, 21.5)),
        line(seg(18, 17, 19.5, 21.5)),
        dot(18, 13, 1.3),
    ]


@icon("hand-spreader", CAT, "Seed hopper with a side crank and a spinner plate scattering seeds below",
      tags=["seed broadcaster", "seeder", "fertilizer spreader", "hand crank", "sowing", "broadcast seeding", "cover crop"])
def _(S):
    return [
        shell(poly([(4, 3.5), (16, 3.5), (12.5, 13), (7.5, 13)], closed=True, r=S.r * 0.6)),
        line(poly([(16, 7.5), (20.5, 7.5), (20.5, 11.5)], r=S.r * 0.5)),
        line(seg(5.5, 16.5, 14.5, 16.5)),
        dot(3.5, 20, 0.9),
        dot(10, 21, 0.9),
        dot(16.5, 20, 0.9),
    ]


@icon("cream-separator", CAT, "Tall cream separator with a top bowl, two spouts and a side crank",
      tags=["milk separator", "dairy", "centrifuge", "cream", "skim milk", "hand crank", "homestead"])
def _(S):
    return [
        shell(poly([(5.5, 2.5), (16.5, 2.5), (14, 8), (8, 8)], closed=True, r=S.r * 0.5)),
        shell(rect(8, 8, 6, 9, 0)),
        shell(rect(5.5, 17, 11, 4.5, rr(S, 1.5))),
        line(seg(8, 11, 3.5, 11)),
        line(seg(8, 14, 3.5, 14)),
        line(poly([(14, 12.5), (19, 12.5), (19, 17)], r=S.r * 0.5)),
    ]


@icon("mobile-chicken-coop", CAT, "A-frame chicken coop on wheels with a wire run underneath and a pull handle",
      tags=["chicken tractor", "hen house", "poultry", "portable coop", "pasture poultry", "henhouse", "backyard chickens"])
def _(S):
    return [
        shell(poly([(3, 16), (10, 4.5), (17, 16)], closed=True, r=S.r)),
        detail(seg(10, 9, 10, 16)),
        shell(rect(3, 16, 14, 4, 0)),
        detail(seg(7.5, 16, 7.5, 20)),
        detail(seg(12.5, 16, 12.5, 20)),
        dot(19.5, 20.5, 1.7),
        line(seg(17, 13, 21.5, 9)),
    ]


@icon("geodesic-greenhouse", CAT, "Dome greenhouse built from triangular panels with a small door",
      tags=["geodesic dome", "dome greenhouse", "glasshouse", "garden dome", "growing dome", "polyhedron", "plants"])
def _(S):
    return [
        shell("M3 20A9 9 0 0 1 21 20Z"),
        detail(poly([(4.9, 14.5), (8.5, 20), (12, 14.5), (15.5, 20), (19.1, 14.5)])),
        detail(seg(12, 11, 12, 14.5)),
    ]


@icon("container-farm", CAT, "Ribbed shipping container with a sprouting plant growing inside",
      tags=["vertical farm", "urban farming", "indoor grow", "hydroponic container", "freight farm", "grow pod", "sprout"])
def _(S):
    return [
        shell(rect(2.5, 6.5, 19, 12, rr(S, 2))),
        detail(seg(6.5, 6.5, 6.5, 18.5)),
        detail(seg(9.5, 6.5, 9.5, 18.5)),
        line(seg(16, 15.5, 16, 11.5)),
        shell(leaf_at((16, 13), (12.5, 9.5), 2.2)) if False else line(seg(16, 13, 13.5, 10.5)),
        line(seg(16, 13, 18.5, 10.5)),
    ]


@icon("manure-pile", CAT, "Steaming rounded heap of manure with a muck fork stuck in the top",
      tags=["dung heap", "muck heap", "compost", "fertilizer", "muck fork", "farmyard", "steam"])
def _(S):
    return [
        shell("M2.5 21Q3 13 9 11Q12 9.5 15 11Q21 13 21.5 21Z"),
        line("M7 7Q6 5.5 7.5 4Q8.5 2.5 7.5 1.5"),
        line(seg(19.5, 2, 15.5, 12)),
        line(poly([(13.5, 13), (16, 10.5)])) if False else line(seg(13.5, 12, 18, 14)),
    ]


@icon("oil-palm-bunch", CAT, "Dense oval cluster of small palm fruits with spiky tips at the top",
      tags=["palm fruit", "palm oil", "fruit bunch", "plantation", "ffb", "tropical crop", "harvest"])
def _(S):
    return [
        shell(ellipse(12, 14, 7.5, 7.5)),
        dot(9.5, 10.5, 1.2), dot(14.5, 10.5, 1.2),
        dot(8, 14, 1.2), dot(12, 14, 1.2), dot(16, 14, 1.2),
        dot(9.5, 17.5, 1.2), dot(14.5, 17.5, 1.2),
        line(seg(12, 6.5, 12, 2)),
        line(seg(8.5, 7.8, 6, 3.5)),
        line(seg(15.5, 7.8, 18, 3.5)),
    ]


@icon("hanging-scale", CAT, "Hook scale with a round dial hanging from a ring and a sack hooked below",
      tags=["spring scale", "weighing", "produce scale", "weight", "market", "sack", "hanging balance"])
def _(S):
    return [
        shell(circle(12, 3.6, 1.8)),
        shell(circle(12, 10.5, 5.5)),
        detail(seg(12, 10.5, 14.5, 8)),
        line(seg(12, 16, 12, 18)),
        shell("M8 22Q8 18 12 18Q16 18 16 22Z"),
    ]


@icon("gazing-ball", CAT, "Reflective glass sphere with a highlight sitting on a short pedestal",
      tags=["garden ornament", "mirror ball", "globe", "yard decoration", "reflective", "garden globe", "lawn art"])
def _(S):
    return [
        shell(circle(12, 9.5, 6.5)),
        detail(arc(12, 9.5, 3.3, 195, 265)),
        shell(poly([(9.5, 16.5), (14.5, 16.5), (15.5, 21.5), (8.5, 21.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("garden-urn", CAT, "Classical urn planter on a pedestal with a wide rim and trailing plants",
      tags=["urn planter", "garden ornament", "classical", "planter", "pedestal pot", "patio", "landscaping"])
def _(S):
    return [
        shell("M6.5 4.5H17.5L16 7C16 8 15 8.5 15 9.5C19 11 18.5 16 14 17H10C5.5 16 5 11 9 9.5C9 8.5 8 8 8 7Z"),
        shell(poly([(10, 17), (14, 17), (15.5, 21.5), (8.5, 21.5)], closed=True, r=S.r * 0.5)),
        line("M6.5 4.5Q3 6 3.5 10"),
        line("M17.5 4.5Q21 6 20.5 10"),
    ]


@icon("rain-chain", CAT, "Chain of small linked cups hanging from a gutter with water dripping down it",
      tags=["gutter chain", "downspout", "rain catcher", "roof drainage", "japanese garden", "kusari doi", "water feature"])
def _(S):
    return [
        line(seg(4, 3, 20, 3)),
        line(seg(12, 3, 12, 6)),
        shell(poly([(8.5, 6), (15.5, 6), (14, 9.5), (10, 9.5)], closed=True, r=S.r * 0.5)),
        line(seg(12, 9.5, 12, 11.5)),
        shell(poly([(8.5, 11.5), (15.5, 11.5), (14, 15), (10, 15)], closed=True, r=S.r * 0.5)),
        line(seg(12, 15, 12, 17)),
        shell(poly([(8.5, 17), (15.5, 17), (14, 20.5), (10, 20.5)], closed=True, r=S.r * 0.5)),
        dot(18, 10, 1),
        dot(18, 16, 1),
    ]


def _spiral(cx, cy, r0, r1, turns, n=36):
    pts = []
    for i in range(n + 1):
        t = i / n
        a = math.radians(-90 + 360 * turns * t)
        r = r0 + (r1 - r0) * t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


@icon("herb-spiral", CAT, "Spiral stone wall seen from above with small herbs planted along it",
      tags=["herb garden", "permaculture", "spiral garden", "raised bed", "garden design", "herbs", "top view"])
def _(S):
    return [
        line(poly(_spiral(12, 12, 1.5, 9, 1.75), r=0)),
        dot(12, 15, 0.9), dot(7.5, 9, 0.9), dot(17, 14, 0.9),
    ]


@icon("keyhole-garden", CAT, "Round raised bed from above with a notch path leading to a central compost basket",
      tags=["raised bed", "garden design", "compost basket", "african garden", "top view", "permaculture", "circular bed"])
def _(S):
    return [
        shell(arc(12, 11.5, 9.5, 112, 68) + "L12 11.5Z"),
        detail(circle(12, 11.5, 2.2)),
    ]


@icon("green-roof", CAT, "House with a pitched roof covered in grass and small plants",
      tags=["living roof", "sod roof", "eco house", "sustainable building", "roof garden", "grass roof", "insulation"])
def _(S):
    return [
        shell(poly([(4, 21.5), (4, 12.5), (12, 6.5), (20, 12.5), (20, 21.5)], closed=True, r=S.r)),
        detail("M10 21.5V17.5A2 2 0 0 1 14 17.5V21.5"),
        line(seg(6, 11.35, 6, 8.5)),
        line(seg(9, 9.1, 9, 6.3)),
        line(seg(12, 6.5, 12, 3.5)),
        line(seg(15, 9.1, 15, 6.3)),
        line(seg(18, 11.35, 18, 8.5)),
    ]


# ============================================================================ chunk 4

@icon("archimedes-screw", CAT, "Inclined tube with a spiral screw inside lifting water from a low pool to a higher channel",
      tags=["screw pump", "water lifting", "irrigation pump", "ancient pump", "auger pump", "water screw", "drainage"])
def _(S):
    tube = rect(9, 3, 6, 18, 0)
    flights = seg(9, 8, 15, 6) + seg(9, 13, 15, 11) + seg(9, 18, 15, 16)
    return [
        shell(rot(tube, 40, 12, 12)),
        detail(rot(flights, 40, 12, 12)),
        line("M2 21.5q2.5-1.5 5 0t5 0"),
        dot(21, 3.5, 1.1),
        dot(21.5, 8, 1.1),
    ]


@icon("watering-globe", CAT, "Round glass watering bulb with a long stem pushed into the soil of a potted plant",
      tags=["plant watering bulb", "self watering", "aqua globe", "houseplant", "vacation watering", "glass bulb", "drip feeder"])
def _(S):
    return [
        shell(circle(6.5, 6, 3.8)),
        line(seg(8.5, 9.3, 11, 17)),
        shell(poly([(7, 14.5), (19, 14.5), (17.5, 21.5), (8.5, 21.5)], closed=True, r=S.r * 0.5)),
        line(seg(16, 14.5, 16, 9.5)),
        line(seg(16, 11.5, 19, 8.5)),
        line(seg(16, 12.5, 13.5, 10)),
    ]


@icon("duck-house", CAT, "Small wooden hut with a ramp floating on a raft in a pond",
      tags=["duck hut", "pond shelter", "floating coop", "waterfowl", "duck pond", "poultry house", "raft"])
def _(S):
    return [
        shell(poly([(5, 14.5), (5, 10.5), (11, 4.5), (17, 10.5), (17, 14.5)], closed=True, r=S.r)),
        detail("M9.5 14.5V13A1.5 1.5 0 0 1 12.5 13V14.5"),
        line(seg(3, 17.5, 19.5, 17.5)),
        line(seg(19.5, 17.5, 22, 20)),
        line("M2 21.5q2.5-1.5 5 0t5 0t5 0"),
    ]


@icon("pond-aerator", CAT, "Floating paddlewheel aerator on two pontoons splashing water in a pond",
      tags=["paddle wheel", "fish pond", "aquaculture", "oxygenation", "pond pump", "water circulation", "fish farm"])
def _(S):
    blades = "".join(seg(*polar(12, 8.5, 1.5, a), *polar(12, 8.5, 5, a)) for a in range(0, 360, 60))
    return [
        line(blades),
        shell(rect(2, 14.5, 6, 3, rr(S, 1))),
        shell(rect(16, 14.5, 6, 3, rr(S, 1))),
        line(seg(7, 16, 17, 16)),
        line(seg(12, 10, 12, 16)),
        line("M2 21.5q2.5-1.5 5 0t5 0t5 0t5 0"),
    ]


@icon("orchard-heater", CAT, "Squat round heater pot with a tall narrow chimney and a flame at the top",
      tags=["smudge pot", "frost protection", "orchard", "groundhog heater", "warming", "cold nights", "citrus grove"])
def _(S):
    return [
        shell(rect(4, 14, 16, 7.5, min(S.R, 3.5) if S.name == "rounded" else 2)),
        shell(rect(10.5, 7, 3, 7, 0)),
        shell("M12 1.5C14 3 14.5 4.5 13.2 6H10.8C9.5 4.5 10 3 12 1.5Z"),
    ]


@icon("frost-cover", CAT, "Plant under a fabric frost hood tied at the base with a snowflake above",
      tags=["frost protection", "plant cover", "winter garden", "fleece", "cloche", "frost blanket", "cold snap"])
def _(S):
    flake = "".join(seg(*polar(12, 3.8, 2.6, a), *polar(12, 3.8, 2.6, a + 180)) for a in (0, 60, 120))
    return [
        line(flake),
        shell("M5 21.5V16A7 7 0 0 1 19 16V21.5Z"),
        detail(seg(5, 19, 19, 19)),
    ]


@icon("crop-yield", CAT, "Ear of wheat beside three rising bars and an upward arrow",
      tags=["harvest results", "production", "yield growth", "agronomy", "crop output", "wheat", "farm analytics"])
def _(S):
    return [
        line(seg(6, 21.5, 6, 9)),
        shell(leaf_at((6, 14.5), (3, 11), 2.6)),
        shell(leaf_at((6, 14.5), (9, 11), 2.6)),
        line(seg(6, 9, 6, 4)),
        solid(rect(11, 17, 2.5, 4.5)),
        solid(rect(15, 14, 2.5, 7.5)),
        solid(rect(19, 11, 2.5, 10.5)),
        line(poly([(12, 9), (20, 4)])),
        line(poly([(16.5, 3.5), (20.5, 3.5), (20.5, 7)], r=S.r * 0.3)),
    ]


@icon("soil-test", CAT, "Test tube holding layered soil and liquid beside a small color chart",
      tags=["soil sample", "soil analysis", "ph test", "agronomy lab", "nutrient test", "testing kit", "soil health"])
def _(S):
    return [
        line(seg(4, 3.5, 12, 3.5)),
        shell("M5.5 3.5V17A2.5 2.5 0 0 0 10.5 17V3.5" if False else "M5.5 3.5H10.5V17A2.5 2.5 0 0 1 5.5 17Z"),
        detail(seg(5.5, 11, 10.5, 11)),
        detail("M5.5 15Q8 13.5 10.5 15"),
        shell(rect(14, 5, 7, 15, rr(S, 1.5))),
        detail(seg(14, 10, 21, 10)),
        detail(seg(14, 14.5, 21, 14.5)),
    ]


@icon("queen-excluder", CAT, "Flat rectangular hive panel of closely spaced slots with a thin rim",
      tags=["beekeeping", "hive part", "apiary", "bee queen", "honey super", "grid", "excluder screen"])
def _(S):
    return [
        shell(rect(3, 5, 18, 14, S.R)),
        detail(seg(7.5, 5, 7.5, 19)),
        detail(seg(11.5, 5, 11.5, 19)),
        detail(seg(15.5, 5, 15.5, 19)),
    ]


# ============================================================================ chunk 5

@icon("grain-dryer", CAT, "Tall dryer tower with grain chutes on top and a burner box and fan at its base",
      tags=["grain bin", "crop drying", "harvest storage", "burner", "drying tower", "moisture", "elevator"])
def _(S):
    return [
        line(seg(9, 4, 9, 1.5)),
        line(seg(15, 4, 15, 1.5)),
        shell(rect(6, 4, 12, 11, rr(S, 1.5))),
        detail(seg(6, 8, 18, 8)),
        detail(seg(6, 11.5, 18, 11.5)),
        shell(rect(2.5, 15, 8, 6.5, rr(S, 1.5))),
        shell(circle(16.5, 18.5, 3)),
    ]


@icon("round-barn", CAT, "Circular barn with a conical roof, a small cupola and a wide arched door",
      tags=["circular barn", "farm building", "dairy barn", "roundhouse", "rural architecture", "farmstead", "heritage"])
def _(S):
    return [
        shell("M4.5 12.5V19Q12 22.5 19.5 19V12.5Z"),
        shell(poly([(3.5, 12.5), (12, 6.5), (20.5, 12.5)], closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
        line(seg(12, 6.5, 12, 3)),
        detail("M9 20.6V17A3 3 0 0 1 15 17V20.6"),
    ]


@icon("barn-cupola", CAT, "Small roof cupola with louvered sides, a pyramid cap and a weather vane arrow on top",
      tags=["roof vent", "weather vane", "barn roof", "louvers", "ventilation", "rural architecture", "weathervane"])
def _(S):
    return [
        line(seg(12, 5.5, 12, 1.5)),
        line(poly([(9, 2.5), (15, 2.5)])),
        shell(poly([(4.5, 11.5), (12, 5.5), (19.5, 11.5)], closed=True, r=S.r * 0.6)),
        shell(rect(6, 11.5, 12, 9, 0)),
        detail(seg(6, 14.5, 18, 14.5)),
        detail(seg(6, 17.5, 18, 17.5)),
    ]


@icon("pig-ark", CAT, "Low half-round corrugated metal hut with an open doorway, standing on grass",
      tags=["pig shelter", "pig house", "corrugated hut", "outdoor pigs", "swine", "livestock shelter", "field shelter"])
def _(S):
    return [
        shell("M2.5 20V16Q2.5 7.5 12 7.5T21.5 16V20Z"),
        detail("M8.5 20V16.5A3.5 3.5 0 0 1 15.5 16.5V20"),
        line(seg(2, 21.5, 22, 21.5)),
        detail(seg(5.5, 12.5, 5.5, 16)),
        detail(seg(18.5, 12.5, 18.5, 16)),
    ]


@icon("horse-walker", CAT, "Round exercise pen from above with a central pole and four radial arms",
      tags=["hot walker", "horse exerciser", "stable", "equestrian", "training", "round pen", "top view"])
def _(S):
    hub = shell(circle(12, 12, 2.2)) if S.name == "rounded" else shell(rect(9.8, 9.8, 4.4, 4.4))
    parts = [line(circle(12, 12, 9.5)), hub]
    for a in (45, 135, 225, 315):
        x1, y1 = polar(12, 12, 2.2, a)
        x2, y2 = polar(12, 12, 6.2, a)
        parts.append(line(seg(x1, y1, x2, y2)))
        x3, y3 = polar(12, 12, 6.8, a)
        parts.append(dot(x3, y3, 1.3) if S.name == "rounded" else Part("dot", rect(x3 - 1.2, y3 - 1.2, 2.4, 2.4)))
    return parts


@icon("furrow-irrigation", CAT, "Raised crop ridges receding toward the horizon with water in the furrows between them",
      tags=["flood irrigation", "row crops", "ditch", "field water", "ridge and furrow", "surface irrigation", "rows"])
def _(S):
    return [
        line(seg(2.5, 21.5, 7.9, 11.5)),
        line(seg(8.5, 21.5, 10.5, 11.5)),
        line(seg(15.5, 21.5, 13.5, 11.5)),
        line(seg(21.5, 21.5, 16.1, 11.5)),
        line(seg(4, 7, 20, 7)),
        dot(5.5, 18.5, 1),
        dot(12, 18.5, 1),
        dot(18.5, 18.5, 1),
    ]
