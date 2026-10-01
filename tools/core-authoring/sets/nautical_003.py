"""TypeIcon Core: nautical (batch nautical_003).

Fishing craft and gear, pirate-age relics, rope hitches, old navigation instruments and harbor structures.
Boats are drawn from the side, nets and weirs from the front or above, long tools turned on a diagonal.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, polar

CAT = "nautical"


def water(y=20.5, x0=2, x1=22, w=4, c=1.6):
    """Wave line from x0 to x1 (x1 - x0 must be a multiple of w)."""
    n = int(round((x1 - x0) / w))
    return f"M{fmt(x0)} {fmt(y)}q{fmt(w / 2)} {fmt(-c)} {fmt(w)} 0" + f"t{fmt(w)} 0" * (n - 1)


def rr(S, cap):
    return min(S.R, cap)


def rot(pts, deg=45, cx=12.0, cy=12.0):
    """Rotate points clockwise on screen about (cx, cy)."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rpath(cmds, deg=45):
    """Path from commands with rotated points: M L A(r,large,sweep,p) Q C Z."""
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


def rseg(x1, y1, x2, y2, deg=45):
    (a, b), (c, d) = rot([(x1, y1), (x2, y2)], deg)
    return seg(a, b, c, d)


def rp(pts, closed=True, r=0.0, deg=45):
    return poly(rot(pts, deg), closed=closed, r=r)


def fish(x, y, s=1.0, flip=False):
    """Small solid fish (body lens plus forked tail) centred near (x, y), facing left unless flipped."""
    k = -1 if flip else 1

    def X(v):
        return fmt(x + k * v * s)

    def Y(v):
        return fmt(y + v * s)
    return (f"M{X(-2.2)} {Y(0)}Q{X(-0.4)} {Y(-2.3)} {X(1.4)} {Y(0)}Q{X(-0.4)} {Y(2.3)} {X(-2.2)} {Y(0)}Z"
            f"M{X(1.0)} {Y(0)}L{X(3.0)} {Y(-1.7)}L{X(3.0)} {Y(1.7)}Z")


# ============================================================================ nets and fishing boats

@icon("gillnet", CAT, "Wall of net hanging in the water with floats along the top edge and weights along the bottom.",
      tags=["gill net", "fishing net", "net wall", "floats", "commercial fishing", "mesh", "fishery"])
def _(S):
    return [
        shell(rect(3, 7.5, 18, 10, S.R * 0.75)),
        detail(seg(9, 7.5, 9, 17.5)), detail(seg(15, 7.5, 15, 17.5)), detail(seg(3, 12.5, 21, 12.5)),
        dot(6, 4.2, 1.4), dot(12, 4.2, 1.4), dot(18, 4.2, 1.4),
        solid(rect(5, 20, 2, 2)), solid(rect(11, 20, 2, 2)), solid(rect(17, 20, 2, 2)),
    ]


@icon("purse-seine", CAT, "Circle of net seen from above around a few fish, with a boat beside it drawing the net closed.",
      tags=["purse seine net", "net circle", "fish school", "tuna fishing", "commercial fishing", "top view", "netting"])
def _(S):
    ring = circle(9.5, 9.5, 7.5) if S.name == "rounded" else poly([polar(9.5, 9.5, 7.5, -90 + i * 30) for i in range(12)], closed=True)
    return [
        shell(ring),
        Part("dot", fish(7.6, 8.4, 1.1)), Part("dot", fish(12.2, 11.8, 1.1, flip=True)),
        shell(poly([(15, 18.5), (19.5, 18.5), (21.5, 20.5), (19.5, 22.5), (15, 22.5)], closed=True, r=S.r * 0.6)),
    ]


@icon("purse-seiner", CAT, "Fishing boat with a tall mast, a slanted boom and a hanging pulley block over the deck.",
      tags=["purse seine boat", "fishing boat", "tuna boat", "trawler", "mast", "boom", "commercial fishing", "vessel"])
def _(S):
    return [
        shell(poly([(2, 15), (4.5, 15), (4.5, 10.5), (10, 10.5), (10, 15), (22, 15), (19.5, 20), (4.5, 20)], closed=True, r=S.r * 0.6)),
        line(seg(14.5, 3, 14.5, 15)),
        line(seg(14.5, 5, 21, 10)),
        solid(circle(21, 12.2, 1.3)),
    ]


@icon("crab-boat", CAT, "Fishing boat with a wheelhouse at the front and a stack of square crab pots on the back deck.",
      tags=["crab fishing", "crab pots", "fishing boat", "cage traps", "king crab", "commercial fishing", "vessel"])
def _(S):
    return [
        shell(poly([(2, 15.5), (4.5, 15.5), (4.5, 9.5), (10.5, 9.5), (10.5, 15.5), (22, 15.5), (19.5, 20.5), (4.5, 20.5)], closed=True, r=S.r * 0.6)),
        shell(rect(13, 4.5, 6.5, 10, rr(S, 1.5))),
        detail(seg(13, 9.5, 19.5, 9.5)), detail(seg(16.25, 4.5, 16.25, 9.5)),
    ]


@icon("dory", CAT, "Small flat bottomed rowing boat with high flared sides, seen from the side on the water.",
      tags=["rowboat", "fishing dinghy", "small boat", "flat bottom boat", "row boat", "skiff", "oars"])
def _(S):
    body = "M2 7.5Q12 12 22 9.5L19 17H5Z" if S.name == "line" else "M2.5 7.5Q12 12 21.5 9.5L18.5 16.5Q18.2 17 17.5 17H6.5Q5.8 17 5.5 16.5Z"
    return [
        shell(body),
        detail(seg(7, 13, 17.5, 13)),
        line(water(20.5)),
    ]


@icon("glass-fishing-float", CAT, "Round glass ball wrapped in a diamond mesh of rope with a hanging loop on top.",
      tags=["glass float", "fishing float", "net float", "buoy ball", "beach find", "net", "rope", "japanese float"])
def _(S):
    loop = circle(12, 3.6, 1.6) if S.name == "rounded" else poly([(12, 1.8), (13.8, 3.6), (12, 5.4), (10.2, 3.6)], closed=True)
    return [
        shell(circle(12, 14, 7.5)),
        detail(seg(6.7, 8.7, 17.3, 19.3)), detail(seg(17.3, 8.7, 6.7, 19.3)),
        line(loop),
    ]


@icon("fish-box", CAT, "Open crate packed with ice and fish, forked tails sticking up over its rim.",
      tags=["fish crate", "catch", "ice box", "seafood", "market", "fish market", "tray", "fishmonger"])
def _(S):
    return [
        solid("M7 12.5V8.5L4.5 3L8.2 5.2L11.5 3L9 8.5V12.5Z"),
        solid("M15 12.5V8.5L12.5 3L16.2 5.2L19.5 3L17 8.5V12.5Z"),
        shell(rect(3, 12, 18, 9, S.R * 0.75)),
        detail(seg(3, 16.5, 21, 16.5)),
    ]


@icon("gaff-hook", CAT, "Long pole ending in a large curved hook with a sharp point, used to land big fish.",
      tags=["fishing gaff", "boat hook", "landing hook", "big game fishing", "pole", "angling", "catch"])
def _(S):
    cmds = [("M", (12, 22)), ("L", (12, 7.5)), ("Q", (12, 3), (16, 3)), ("Q", (19.5, 3), (19.5, 7)), ("L", (17.5, 11))]
    if S.name == "line":
        cmds = [("M", (12, 22)), ("L", (12, 6)), ("L", (14, 3)), ("L", (18, 3)), ("L", (19.5, 7)), ("L", (17.5, 11))]
    return [line(rpath(cmds, 45))]


@icon("harpoon", CAT, "Long shaft with a barbed arrow head at one end and a coil of rope tied near the other.",
      tags=["whaling", "spear", "fishing spear", "hunting", "barbed", "rope", "whaler", "weapon"])
def _(S):
    return [
        line(rseg(12, 22, 12, 9)),
        solid(rp([(12, 0.8), (16.8, 9.5), (12.9, 7.6), (11.1, 7.6), (7.2, 9.5)])),
        line(circle(*rot([(7.8, 17)])[0], 3)),
    ]


@icon("netting-needle", CAT, "Flat shuttle with a pointed tip, a slot with a center tongue, and a notched tail, used to tie nets.",
      tags=["net needle", "net making", "shuttle", "net mending", "twine", "fishing net", "craft", "mesh"])
def _(S):
    return [
        shell(rp([(12, 1), (15.8, 6), (15.8, 22), (13.5, 22), (12, 19), (10.5, 22), (8.2, 22), (8.2, 6)], r=S.r * 0.6)),
        detail(rseg(12, 7, 12, 14.5)),
    ]


@icon("trawl-door", CAT, "Heavy curved steel plate towed on a two legged chain and a wire, used to spread a trawl net.",
      tags=["otter board", "trawl board", "trawling", "fishing gear", "steel plate", "bridle", "net spreader"])
def _(S):
    return [
        shell("M10 4H6.5Q2 12 6.5 20H10Z" if S.name == "line" else "M9.5 4H6.5Q2 12 6.5 20H9.5Q11 20 11 18.5V5.5Q11 4 9.5 4Z"),
        detail(seg(3.6, 12, 11, 12)),
        line(seg(11, 6, 17.5, 12)), line(seg(11, 18, 17.5, 12)),
        line(seg(17.5, 12, 22, 12)),
        solid(circle(17.5, 12, 1.6)),
    ]


@icon("squid-jig", CAT, "Slim torpedo shaped lure with an eye, and a crown of fine curved hooks around its lower end.",
      tags=["squid lure", "jig", "squid fishing", "cuttlefish", "fishing lure", "hooks", "bait", "angling"])
def _(S):
    return [
        shell("M12 2.5Q15.5 5 15.5 9.5V15H8.5V9.5Q8.5 5 12 2.5Z" if S.name == "line" else "M12 2.5Q15.5 5 15.5 9.5V14.5Q15.5 15 15 15H9Q8.5 15 8.5 14.5V9.5Q8.5 5 12 2.5Z"),
        dot(12, 8, 1.2),
        detail(seg(8.5, 12, 15.5, 12)),
        line(seg(12, 15, 12, 21)),
        line("M9.5 15V18.5Q9.5 21 6.5 20.5"), line("M14.5 15V18.5Q14.5 21 17.5 20.5"),
    ]


@icon("fighting-chair", CAT, "Swiveling boat chair with a tall back, a footrest bar, and a rod socket at the front of the seat.",
      tags=["big game chair", "sport fishing", "fishing chair", "deck chair", "rod holder", "marlin", "boat seat"])
def _(S):
    return [
        shell(poly([(14, 3), (19.5, 3), (19.5, 14), (4, 14), (4, 11), (14, 11)], closed=True, r=S.r * 0.6)),
        shell(rect(4.5, 6, 3, 5, rr(S, 1))),
        line(seg(11.5, 14, 11.5, 20.5)),
        line(seg(7, 20.5, 16.5, 20.5)),
        line(seg(11.5, 17, 4, 17)),
    ]


def _weir_points():
    base = [(12, 21), (3.5, 12), (3.5, 8), (6, 4.5), (9.5, 4.5), (12, 7.5), (14.5, 4.5), (18, 4.5), (20.5, 8), (20.5, 12), (12, 21)]
    out, acc = [base[0]], 0.0
    step = 3.6
    for a, b in zip(base, base[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        t = step - acc
        while t <= L:
            out.append((a[0] + (b[0] - a[0]) * t / L, a[1] + (b[1] - a[1]) * t / L))
            t += step
        acc = L - (t - step)
    return out


def _weir_filled():
    pts = _weir_points()[1:-1]
    parts = [P(circle(x, y, 1.5)) for x, y in pts] + [P(fish(11, 11.5, 1.3))]
    return U(*parts)


@icon("fish-weir", CAT, "Top view of a heart shaped fence of stakes standing in the water with a fish trapped inside.",
      tags=["fish trap", "stake fence", "fish corral", "traditional fishing", "pound net", "tidal trap", "stakes"],
      filled=_weir_filled)
def _(S):
    pts = _weir_points()[1:-1]
    if S.name == "line":
        parts = [solid(rect(x - 1, y - 1, 2, 2)) for x, y in pts]
    else:
        parts = [dot(x, y, 1.15) for x, y in pts]
    parts.append(solid(fish(11, 11.5, 1.3)))
    return parts


@icon("net-drum", CAT, "Large horizontal reel with a wide flange at each end, wound with a mesh of fishing net, on a deck.",
      tags=["net reel", "net winch", "trawl winch", "fishing boat gear", "drum", "reel", "net hauler"])
def _(S):
    return [
        shell(rect(3, 4, 3.5, 14, rr(S, 1.75))),
        shell(rect(17.5, 4, 3.5, 14, rr(S, 1.75))),
        shell(rect(6.5, 7.5, 11, 7, 0)),
        detail(seg(9, 7.5, 15, 14.5)), detail(seg(15, 7.5, 9, 14.5)),
        line(seg(2, 21, 22, 21)),
    ]


@icon("cantilever-fishing-net", CAT, "Square net lowered on four ropes from a long wooden boom that leans out over the water from a shore post.",
      tags=["chinese fishing net", "lift net", "shore net", "kerala fishing", "boom net", "traditional fishing", "counterweight"])
def _(S):
    return [
        line(seg(5, 8, 5, 22)),
        line(seg(3.5, 9, 19, 4)),
        solid(rect(3, 4, 3.5, 3.5)),
        line(seg(19, 4.5, 12.5, 14)), line(seg(19, 4.5, 21, 14)),
        shell(rect(10.5, 14, 11, 7, rr(S, 1.5))),
        detail(seg(16, 14, 16, 21)),
    ]


@icon("stilt-fishing", CAT, "Fisher sitting on a crossbar atop a single pole planted in the sea, holding a rod with a line in the water.",
      tags=["stilt fisherman", "sri lanka fishing", "pole fishing", "angler", "traditional fishing", "fishing rod", "sea"])
def _(S):
    return [
        solid(circle(9, 4.5, 2.1)),
        line(seg(9, 8, 9, 13)),
        line(seg(9, 10, 20.5, 4.5)),
        line(seg(20.5, 4.5, 20.5, 18)),
        line(seg(5.5, 14.5, 12.5, 14.5)),
        line(seg(9, 14.5, 9, 22)),
        line(water(19, 2, 6, 4)), line(water(19, 12, 22, 5) if False else water(19, 12, 20, 4)),
    ]


@icon("cormorant-fishing", CAT, "Narrow boat with a lantern on a pole at the bow and a cormorant perched on its side.",
      tags=["cormorant fisherman", "trained bird fishing", "river fishing", "lantern boat", "li river", "bird", "traditional fishing"])
def _(S):
    return [
        shell(poly([(2, 15.5), (22, 15.5), (19.5, 20), (4.5, 20)], closed=True, r=S.r * 0.6)),
        line(seg(5.5, 15.5, 5.5, 4)),
        shell(rect(3.5, 4, 4, 5, rr(S, 1))),
        shell(rect(11, 10.3, 6.5, 4.2, 2.1)),
        line(seg(17, 11.5, 19, 7)),
        solid(circle(19.6, 5.6, 1.5)),
        solid("M20.4 5.2L22.8 6.2L20.4 6.8Z"),
    ]


@icon("fish-drying-rack", CAT, "Wooden A frame with two crossbars and split fish hanging from them to dry.",
      tags=["drying rack", "stockfish", "dried fish", "preserving", "smoking fish", "fish curing", "salted fish"])
def _(S):
    def hang(x, y, h=4.6):
        return solid(f"M{fmt(x)} {fmt(y)}Q{fmt(x + 1.7)} {fmt(y + h * 0.5)} {fmt(x)} {fmt(y + h)}Q{fmt(x - 1.7)} {fmt(y + h * 0.5)} {fmt(x)} {fmt(y)}Z")
    return [
        line(poly([(3.5, 21), (12, 3), (20.5, 21)], r=S.r)),
        line(seg(8.8, 9, 15.2, 9)),
        line(seg(6, 15, 18, 15)),
        hang(12, 10, 3.6),
        hang(9, 16, 4.8), hang(15, 16, 4.8),
    ]


@icon("squid-fishing-boat", CAT, "Fishing boat with a row of large round lamps hanging from a wire strung above the deck to lure squid.",
      tags=["squid boat", "light fishing", "night fishing", "lamps", "jigging boat", "fishing vessel", "lure lights"])
def _(S):
    return [
        line(seg(2.5, 4.5, 21.5, 4.5)),
        solid(circle(4.5, 7.2, 1.5)), solid(circle(8.5, 7.2, 1.5)), solid(circle(15.5, 7.2, 1.5)), solid(circle(19.5, 7.2, 1.5)),
        line(seg(12, 4.5, 12, 15)),
        shell(poly([(2, 15.5), (4.5, 15.5), (4.5, 12), (8.5, 12), (8.5, 15.5), (22, 15.5), (19.5, 20.5), (4.5, 20.5)], closed=True, r=S.r * 0.6)),
    ]


@icon("handline-frame", CAT, "H shaped wooden winder wrapped with fishing line, with a sinker and a hook hanging from its lower ends.",
      tags=["hand line", "line winder", "fishing line", "hook and sinker", "handline", "traditional fishing", "reel"])
def _(S):
    return [
        shell(poly([(3.5, 3), (8.5, 3), (8.5, 6.5), (15.5, 6.5), (15.5, 3), (20.5, 3), (20.5, 15), (15.5, 15), (15.5, 12), (8.5, 12),
                    (8.5, 15), (3.5, 15)], closed=True, r=S.r * 0.6)),
        solid(rect(8.5, 7.5, 7, 4)),
        line(seg(6, 15, 6, 19)),
        solid(circle(6, 20.8, 1.4)),
        line("M18 15V19.5Q18 21.5 15.8 21.5"),
    ]


@icon("cutlass", CAT, "Short curved sword with a wide single edged blade, a bowl shaped hand guard and a round pommel.",
      tags=["pirate sword", "sabre", "saber", "blade", "weapon", "buccaneer", "naval sword", "swashbuckler"])
def _(S):
    blade = rpath([("M", (11, 13)), ("Q", (10.3, 6), (14, 1.8)), ("Q", (13.2, 7), (13.2, 13)), ("Z",)])
    bowl = rpath([("M", (8, 13.5)), ("L", (16, 13.5)), ("A", 4, 0, 1, (8, 13.5)), ("Z",)])
    return [
        shell(blade),
        shell(bowl),
        line(rseg(12, 17.5, 12, 21)),
        solid(circle(*rot([(12, 22)])[0], 1.3)),
    ]


_DOUBLOON_R = [9.0, 8.2, 8.8, 9.0, 8.0, 8.7, 9.0, 8.3, 8.9, 8.1, 8.8, 9.0]


@icon("doubloon", CAT, "Old gold coin with a slightly uneven edge and a cross stamped in the center.",
      tags=["pirate coin", "gold coin", "spanish gold", "treasure", "piece of eight", "buccaneer", "loot"])
def _(S):
    pts = [polar(12, 12, _DOUBLOON_R[i], -90 + i * 30) for i in range(12)]
    return [
        shell(poly(pts, closed=True, r=S.r * 1.3)),
        detail(seg(12, 6.5, 12, 17.5)), detail(seg(6.5, 12, 17.5, 12)),
    ]


@icon("scrimshaw", CAT, "Curved whale tooth with a tiny sailing ship engraved on its face.",
      tags=["whale tooth", "engraving", "sailor art", "carved tooth", "whaling craft", "bone carving", "souvenir"])
def _(S):
    tooth = "M7 21Q4 12 9.5 5Q12 2 14.5 4Q20 10 17 21Z" if S.name == "line" else "M8 21Q4.5 12 9.5 5Q12 2 14.5 4Q20 10 16.5 20Q16.3 21 15.5 21Z"
    return [
        shell(tooth),
        detail(seg(11.5, 8.5, 11.5, 14.5)),
        detail("M11.5 9.5L14.5 14H11.5"),
        detail(seg(8.8, 17, 15, 17)),
    ]


@icon("sailors-valentine", CAT, "Octagonal wooden box with a heart made of tiny seashells in the middle.",
      tags=["shell box", "shellwork", "seashell heart", "souvenir", "barbados shells", "keepsake", "sailor gift"])
def _(S):
    return [
        shell(poly(regular(12, 12, 9.6, 8, -67.5), closed=True, r=S.r)),
        detail("M12 17.2Q6.3 13.3 7 10.3Q7.6 7.8 10 8.2Q11.6 8.5 12 10Q12.4 8.5 14 8.2Q16.4 7.8 17 10.3Q17.7 13.3 12 17.2Z"),
    ]


@icon("caulking-iron", CAT, "Wide flat chisel with a flared cutting edge standing beside a round headed wooden mallet.",
      tags=["caulking mallet", "shipwright tool", "boat building", "hull sealing", "oakum", "wood boat repair", "calking"])
def _(S):
    return [
        shell(rect(2.5, 3, 8.5, 6.5, rr(S, 2))),
        shell(rect(5.3, 9.5, 2.9, 11.5, rr(S, 1))),
        shell(poly([(13, 3), (21.5, 3), (19.5, 11), (15, 11)], closed=True, r=S.r * 0.6)),
        shell(rect(15.5, 11, 3.5, 10, rr(S, 1.5))),
    ]


@icon("hardtack", CAT, "Square ship's biscuit with a neat grid of small holes pricked across it.",
      tags=["ship biscuit", "sea biscuit", "cracker", "sailor food", "navy bread", "provisions", "rations"])
def _(S):
    parts = [shell(rect(3.5, 3.5, 17, 17, S.R * 0.75))]
    for x in (8.5, 12, 15.5):
        for y in (8.5, 12, 15.5):
            parts.append(dot(x, y, 1.15))
    return parts


@icon("widows-walk", CAT, "House with a small railed platform on top of its roof for watching the sea.",
      tags=["roof walk", "rooftop lookout", "captain's house", "coastal home", "railing", "new england", "sea view"])
def _(S):
    return [
        line(poly([(8.5, 7.5), (8.5, 3.5), (15.5, 3.5), (15.5, 7.5)], r=S.r * 0.5)),
        line(seg(12, 3.5, 12, 7.5)),
        shell(poly([(3, 13.5), (8.5, 7.5), (15.5, 7.5), (21, 13.5)], closed=True, r=S.r * 0.6)),
        line(poly([(5, 13.5), (5, 21), (19, 21), (19, 13.5)], r=S.r)),
        line(poly([(10, 21), (10, 16.5), (14, 16.5), (14, 21)], r=S.r * 0.5)),
    ]


# ============================================================================ emblems, rope work and small craft

def _anchor_parts(S, deg, k=1.0, shift=(0.0, 0.0)):
    """A ship's anchor (ring, shank, stock, curved arms with flukes) scaled by k and turned by deg about the centre."""
    def T(p):
        x, y = 12 + (p[0] - 12) * k, 12 + (p[1] - 12) * k
        (qx, qy), = rot([(x, y)], deg)
        return (qx + shift[0], qy + shift[1])

    def pth(cmds):
        out = []
        for c in cmds:
            if c[0] in ("M", "L"):
                q = T(c[1])
                out.append(f"{c[0]}{fmt(q[0])} {fmt(q[1])}")
            elif c[0] == "C":
                q = [T(p) for p in c[1:]]
                out.append("C" + " ".join(f"{fmt(a)} {fmt(b)}" for a, b in q))
        return "".join(out)
    ring = T((12, 5))
    return [
        line(circle(ring[0], ring[1], 2 * k)),
        line(pth([("M", (12, 7)), ("L", (12, 21))])),
        line(pth([("M", (8, 9.5)), ("L", (16, 9.5))])),
        line(pth([("M", (5, 14.5)), ("C", (5, 18.5), (8, 21), (12, 21)), ("C", (16, 21), (19, 18.5), (19, 14.5))])),
        line(poly([T((3, 16.5)), T((5, 14)), T((7, 16.5))], r=S.r * 0.5)),
        line(poly([T((17, 16.5)), T((19, 14)), T((21, 16.5))], r=S.r * 0.5)),
    ]


@icon("crossed-anchors", CAT, "Two anchors crossed diagonally over each other in an X, a naval emblem.",
      tags=["anchors crossed", "naval emblem", "navy badge", "maritime crest", "sailor insignia", "harbor", "marine"])
def _(S):
    def small(deg):
        def T(p):
            (q,) = rot([p], deg)
            return q
        ring = T((12, 4.5))
        arms = rpath([("M", (9, 15)), ("C", (9.2, 18.5), (10, 19.5), (12, 19.5)), ("C", (14, 19.5), (14.8, 18.5), (15, 15))], deg)
        return [
            line(circle(ring[0], ring[1], 1.5)),
            line(rseg(12, 6, 12, 19.5, deg)),
            line(rseg(9.8, 9, 14.2, 9, deg)),
            line(arms),
        ]
    return small(42) + small(-42)


@icon("fouled-anchor", CAT, "Anchor with a rope wound loosely around its shank, a classic maritime emblem.",
      tags=["anchor and rope", "navy emblem", "sailor tattoo", "anchor rope", "maritime badge", "nautical", "mooring"])
def _(S):
    a = _anchor_parts(S, 0, 1.0)
    rope = line("M7.5 10.5C11 11.5 17 10.5 16.5 13C16 15.5 8 14 7.5 16.5C7.2 18.5 12 19 16 17")
    return a + [rope]


@icon("powder-keg", CAT, "Small barrel with metal bands and a lit fuse sticking out of the top.",
      tags=["gunpowder", "barrel bomb", "explosive", "pirate barrel", "fuse", "cask", "dynamite keg"])
def _(S):
    body = "M6.5 8Q4 14 6.5 20H17.5Q20 14 17.5 8Z" if S.name == "line" else "M7 8Q4.3 14 6.8 19.3Q7 20 7.8 20H16.2Q17 20 17.2 19.3Q19.7 14 17 8Q16.8 7.5 16 7.5H8Q7.2 7.5 7 8Z"
    return [
        shell(body),
        detail(seg(5.2, 11.5, 18.8, 11.5)), detail(seg(5.2, 16.5, 18.8, 16.5)),
        line("M12 7.5V4.5Q12 3 14.5 3"),
        solid(circle(17, 2.8, 1.6)),
    ]


@icon("rolling-hitch", CAT, "Vertical pole with rope wrapped diagonally around it several times and a tail leaving at the top.",
      tags=["rope knot", "hitch", "pole", "knotting", "scouting", "sailing knot", "tie", "lashing"])
def _(S):
    return [
        shell(rect(9, 2, 6, 20, rr(S, 1.5))),
        line(seg(5.5, 19, 18.5, 15)), line(seg(5.5, 14.5, 18.5, 10.5)),
        line("M5.5 10L18.5 6.5Q20.5 6 20.5 4"),
    ]


@icon("ghost-ship", CAT, "Old sailing ship with torn, ragged sails and a jagged hull, mist drifting beneath it.",
      tags=["haunted ship", "phantom ship", "flying dutchman", "pirate", "spooky", "wreck", "halloween", "sailing ship"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 13)),
        shell(poly([(11, 4.5), (5.5, 6), (5.5, 11), (7.5, 9.5), (9, 11.5), (11, 9.5)], closed=True, r=S.r * 0.4)),
        shell(poly([(13, 4.5), (18.5, 6), (18.5, 11), (16.5, 9.5), (15, 11.5), (13, 9.5)], closed=True, r=S.r * 0.4)),
        shell(poly([(2.5, 13.5), (21.5, 13.5), (19.5, 17.5), (17, 16), (14.5, 18), (12, 16), (9.5, 18), (7, 16), (4.8, 17.5)], closed=True, r=S.r * 0.4)),
        line(water(21.5)),
    ]


@icon("dive-lift-bag", CAT, "Open bottomed bag of air rising underwater, lifting a small box on two straps below it.",
      tags=["lift bag", "salvage bag", "diver", "underwater recovery", "buoyancy bag", "diving", "raise object"])
def _(S):
    bag = "M4.5 12Q3 2.5 12 2.5Q21 2.5 19.5 12Z" if S.name == "line" else "M5.8 12Q3 2.5 12 2.5Q21 2.5 18.2 12Q18 12.6 17.4 12.6H6.6Q6 12.6 5.8 12Z"
    return [
        shell(bag),
        detail("M6.6 9Q9.3 7.5 12 9T17.4 9"),
        line(seg(7, 12.6, 12, 17)), line(seg(17, 12.6, 12, 17)),
        shell(rect(8.5, 17, 7, 5, rr(S, 1.25))),
    ]


@icon("oyster-tongs", CAT, "Two long handles crossed at a pivot with open toothed baskets at their lower ends, used to gather oysters.",
      tags=["oystering", "shellfish rake", "bed tongs", "harvesting", "chesapeake", "seafood", "rake tongs"])
def _(S):
    return [
        line(seg(16.5, 2.5, 6.8, 15)), line(seg(7.5, 2.5, 17.2, 15)),
        solid(circle(12, 8.6, 1.5)),
        line(poly([(3.5, 20), (3.5, 15.5), (10, 15.5), (10, 20)], r=S.r * 0.6)),
        line(poly([(14, 20), (14, 15.5), (20.5, 15.5), (20.5, 20)], r=S.r * 0.6)),
    ]


@icon("push-net", CAT, "Triangular net on two poles pushed through shallow water by a wading figure.",
      tags=["shrimp net", "shrimping", "wading", "scoop net", "traditional fishing", "shallow water", "fisher"])
def _(S):
    return [
        shell(poly([(2.5, 20), (11.5, 20), (2.5, 12)], closed=True, r=S.r * 0.5)),
        detail(seg(2.5, 16, 6.5, 20)),
        line(seg(2.5, 12, 15, 9.5)), line(seg(11.5, 20, 15, 9.5)),
        line(seg(15, 9.5, 18.5, 9.5)),
        solid(circle(19, 4.6, 2.1)),
        line(seg(19, 8, 19, 15)),
        line("M19 15L17 21.5"),
    ]


# ============================================================================ instruments, structures and workboats

@icon("leeboard", CAT, "Flat hulled barge seen from the side with a large fan shaped board hinged to its flank and dipping below.",
      tags=["lee board", "sailing barge", "dutch boat", "side board", "keel board", "centreboard", "sailing"])
def _(S):
    fan = "M12 10.5H16.5L19.5 18.5Q14 21.5 9 18.5Z" if S.name == "line" else "M12.5 10.5H16L19 18Q14 21 9.5 18Z"
    return [
        shell(poly([(2, 4), (22, 4), (20, 10.5), (4, 10.5)], closed=True, r=S.r * 0.6)),
        shell(fan),
        dot(14.2, 12.6, 1.1),
    ]


@icon("backstaff", CAT, "Old navigation instrument with a long staff and two nested arcs of different sizes, with small sighting vanes.",
      tags=["davis quadrant", "sea quadrant", "sextant ancestor", "old navigation", "sun sight", "navigator", "measure altitude"])
def _(S):
    return [
        line(seg(3, 19, 22, 19)),
        line(arc(19, 19, 14.5, 180, 270)),
        line(arc(19, 19, 7.5, 180, 270)),
        line(seg(3.5, 16, 3.5, 22)),
        line(seg(19, 3.5, 19, 6.5)),
    ]


@icon("nocturnal-star-dial", CAT, "Round dial on a short grip with a sighting hole at its center and a long pointer arm pivoting across it.",
      tags=["nocturnal", "night clock", "star clock", "polaris dial", "old navigation", "tell time by stars", "astrolabe"])
def _(S):
    return [
        shell(circle(11, 10, 6.8)),
        dot(11, 10, 1.6),
        line(seg(12.6, 8.6, 21.5, 2.5)),
        shell(rect(9.5, 16.8, 3, 5.2, rr(S, 1.2))),
    ]


@icon("marine-loading-arm", CAT, "Jointed pipe arm on a jetty folded like an elbow, reaching over to connect to a tanker's deck.",
      tags=["loading arm", "oil jetty", "tanker transfer", "fuel loading", "port terminal", "marine terminal", "pipeline"])
def _(S):
    return [
        shell(rect(2, 13, 5.5, 9, rr(S, 1.5))),
        line("M4.75 13V5H15V10.5"),
        solid(circle(4.75, 5, 1.9)), solid(circle(15, 5, 1.9)),
        shell(rect(13.3, 10.5, 3.4, 3, rr(S, 1))),
        shell(poly([(10, 16.5), (22, 16.5), (20, 21), (12, 21)], closed=True, r=S.r * 0.5)),
    ]


@icon("vessel-traffic-tower", CAT, "Tall harbor control tower with a wide glass walled room at the top and a radar bar turning above it.",
      tags=["harbor control", "port control tower", "vts", "ship traffic", "radar tower", "harbour master", "coastal watch"])
def _(S):
    return [
        line(seg(7, 3.6, 17, 3.6)),
        line(seg(12, 3.6, 12, 8)),
        shell(poly([(4.5, 8), (19.5, 8), (17, 12.5), (7, 12.5)], closed=True, r=S.r * 0.5)),
        detail(seg(9.5, 8, 10.5, 12.5)), detail(seg(14.5, 8, 13.5, 12.5)),
        shell(rect(10, 12.5, 4, 9.5, 0)),
        line(seg(6.5, 22, 17.5, 22)) if False else line(seg(7, 22, 17, 22)),
    ]


@icon("faith-hope-charity-symbol", CAT, "Emblem of a cross at the top, a heart in the middle and an anchor below, all on one vertical shaft.",
      tags=["cross heart anchor", "three virtues", "faith hope love", "mariner emblem", "christian symbol", "pendant", "sailor charm"])
def _(S):
    heart = "M12 13.8Q7.4 11 8 8.9Q8.4 7.3 10 7.5Q11.4 7.7 12 9Q12.6 7.7 14 7.5Q15.6 7.3 16 8.9Q16.6 11 12 13.8Z"
    return [
        line(seg(12, 2.5, 12, 7.5)),
        line(seg(8.5, 5, 15.5, 5)),
        solid(heart),
        line(seg(12, 13, 12, 20.5)),
        line("M6 14.8C6.3 18.5 8.6 20.5 12 20.5C15.4 20.5 17.7 18.5 18 14.8"),
        line(poly([(4.5, 16.5), (6, 14.5), (7.5, 16.5)], r=S.r * 0.5)),
        line(poly([(16.5, 16.5), (18, 14.5), (19.5, 16.5)], r=S.r * 0.5)),
    ]


@icon("rope-frame", CAT, "Round frame made of thick twisted rope, its ends tied in a small knot at the bottom.",
      tags=["rope circle", "rope ring", "rope wreath", "nautical frame", "twisted rope", "knot", "decor", "border"])
def _(S):
    parts = [line(circle(12, 10.5, 7.5))]
    for i in range(10):
        a = math.radians(i * 36)
        x0, y0 = 12 + math.cos(a) * 6.4 - math.sin(a) * 0.9, 10.5 + math.sin(a) * 6.4 + math.cos(a) * 0.9
        x1, y1 = 12 + math.cos(a) * 8.6 + math.sin(a) * 0.9, 10.5 + math.sin(a) * 8.6 - math.cos(a) * 0.9
        parts.append(detail(seg(x0, y0, x1, y1)))
    parts.append(solid(circle(12, 19.2, 2.2)))
    parts.append(line(seg(12, 20, 9.6, 22.5)))
    parts.append(line(seg(12, 20, 14.4, 22.5)))
    return parts


@icon("rigid-inflatable-boat", CAT, "Side view of a boat with a thick inflatable tube around a hard hull, a small console and an outboard motor.",
      tags=["rib", "inflatable boat", "rescue boat", "dinghy", "tender", "speedboat", "sea rescue"])
def _(S):
    return [
        shell(poly([(4, 14.5), (17, 14.5), (15.5, 20), (6, 20)], closed=True, r=S.r * 0.5)),
        shell(rect(2, 9.5, 17, 6, S.R * 1.4 if S.name == "rounded" else 2)),
        shell(rect(7.5, 3.8, 4.5, 5.7, rr(S, 1))),
        shell(rect(19.6, 8.5, 2.8, 7, rr(S, 1))),
        line(seg(21, 15.5, 21, 21)),
    ]


@icon("sterndrive", CAT, "Boat stern in side view with an engine hatch on deck and a drive leg with a propeller bolted to the transom.",
      tags=["stern drive", "inboard outboard", "io drive", "boat engine", "outdrive", "propulsion", "power boat", "marine engine"])
def _(S):
    return [
        shell(poly([(2, 10.5), (15, 10.5), (15, 18), (5.5, 18)], closed=True, r=S.r * 0.5)),
        shell(rect(4.5, 5.5, 7, 5, rr(S, 1.25))),
        shell(rect(15.8, 11, 3, 8, rr(S, 1.25))),
        shell(rect(14.5, 18.5, 7.5, 3.5, rr(S, 1.75))),
        line(seg(22.6, 18.6, 22.6, 22)),
    ]


@icon("ship-gunport", CAT, "Square hatch in the side of a wooden ship's hull, its lid propped open and a cannon muzzle poking out.",
      tags=["cannon port", "gun port", "hull hatch", "warship", "pirate ship", "galleon", "cannon", "man o war"])
def _(S):
    return [
        shell(rect(2, 4, 20, 17, rr(S, 2))),
        detail("M7 9.5L5.5 7H18.5L17 9.5"),
        detail(rect(7, 9.5, 10, 8.5, 0)),
        solid(circle(12, 14, 2.6)),
    ]


@icon("deck-prism", CAT, "Glass prism set flush in a ship's deck, flat on top and tapering to a point below, with light rays under it.",
      tags=["deck light", "deck glass", "sailing ship light", "skylight lens", "below decks", "glass", "illumination"])
def _(S):
    return [
        line(seg(2, 6.5, 7, 6.5)), line(seg(17, 6.5, 22, 6.5)),
        shell(poly([(7, 6.5), (17, 6.5), (17, 11), (12, 17), (7, 11)], closed=True, r=S.r * 0.5)),
        detail(seg(7, 11, 17, 11)),
        line(seg(12, 19.5, 12, 22.5)), line(seg(7.5, 19, 6, 21.8)), line(seg(16.5, 19, 18, 21.8)),
    ]


@icon("quay-steps", CAT, "Stone steps cut into a harbor wall running down into the water, with a small boat tied at the bottom.",
      tags=["harbour steps", "landing steps", "jetty stairs", "dock stairs", "waterfront", "mooring", "tender landing"])
def _(S):
    return [
        shell(poly([(2, 3), (8, 3), (8, 7.5), (12, 7.5), (12, 12), (15.5, 12), (15.5, 16), (2, 16)], closed=True, r=S.r * 0.4)),
        shell(poly([(17.5, 14.5), (22, 14.5), (20.5, 18.5), (19, 18.5)], closed=True, r=S.r * 0.3)),
        line(water(21.5, 2, 22, 4)),
    ]


def _seine_pts():
    def y(x):
        t = (x - 3) / 18.0
        return (1 - t) ** 2 * 7 + 2 * (1 - t) * t * -1 + t * t * 7
    return y


@icon("beach-seine", CAT, "Curved wall of net in the shallows with a rope running from each end to figures hauling on the beach.",
      tags=["seine net", "hauling net", "shore fishing", "net fishing", "beach fishing", "drag net", "shallows"])
def _(S):
    y = _seine_pts()
    parts = [shell("M3 7Q12 -1 21 7V12Q12 4 3 12Z")]
    for x in (8, 12, 16):
        parts.append(detail(seg(x, y(x) + 0.2, x, y(x) + 5)))
    parts += [line(seg(3, 12, 6.5, 18.5)), line(seg(21, 12, 17.5, 18.5)),
              solid(circle(6.5, 20.4, 1.6)), solid(circle(17.5, 20.4, 1.6))]
    return parts
