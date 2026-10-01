"""TypeIcon Core: historic (batch 003).

Medieval dress and early instruments, ancient objects and symbols, historic figures and early vehicles.
Figures use a round head over open shoulders; scenes where one thing stands in front of another are drawn
in layers so the front part cuts a clean gap into what lies behind it.
"""
import math

from dsl import LINE, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from dsl import D, P, ST, U, filled_region
from geometry import fmt, path_to_d, polar, rotation, transform_path

CAT = "historic"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rpts(pts, deg, cx=12.0, cy=12.0):
    """Rotate points clockwise on screen about (cx, cy)."""
    a = math.radians(deg)
    c, s_ = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s_, cy + (x - cx) * s_ + (y - cy) * c) for x, y in pts]


def mark(d):
    """Small solid mark: solid in stroke styles, knocked out of a Filled shell."""
    return Part("dot", d)


def rr(S, cap):
    return min(S.R, cap)


def flame(x, top, bottom, w=1.4):
    """Small teardrop flame with its point up."""
    r = w
    my = bottom - r
    return (f"M{fmt(x)} {fmt(top)}Q{fmt(x + w * 1.2)} {fmt((top + my) / 2 + 0.5)} {fmt(x + r)} {fmt(my)}"
            f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x - r)} {fmt(my)}Q{fmt(x - w * 1.2)} {fmt((top + my) / 2 + 0.5)} {fmt(x)} {fmt(top)}Z")


def leaf(cx, cy, h, w, deg=0.0):
    """Pointed leaf of height h and width w, turned by deg about its centre."""
    k = w * 0.66
    t, b = cy - h / 2, cy + h / 2
    d = (f"M{fmt(cx)} {fmt(t)}C{fmt(cx + k)} {fmt(t + h * 0.2)} {fmt(cx + k)} {fmt(b - h * 0.2)} {fmt(cx)} {fmt(b)}"
         f"C{fmt(cx - k)} {fmt(b - h * 0.2)} {fmt(cx - k)} {fmt(t + h * 0.2)} {fmt(cx)} {fmt(t)}Z")
    return rot(d, deg, cx, cy) if deg else d


# --------------------------------------------------------------------------- layered drawings

def _paint(parts, S):
    regs = []
    for p in parts:
        if p.kind in ("dot", "solid"):
            regs.append(P(p.d))
        else:
            regs.append(ST(p.d, 2.0, S.cap, S.join, float(p.attrs.get("stroke_miterlimit", 4))))
    return U(*regs)


def _sil(parts, S):
    regs = []
    for p in parts:
        if p.kind in ("dot", "solid"):
            regs.append(P(p.d))
        elif p.kind == "shell":
            regs.append(U(P(p.d), ST(p.d, 2.0, S.cap, S.join, float(p.attrs.get("stroke_miterlimit", 4)))))
        else:
            regs.append(ST(p.d, 2.0, S.cap, S.join))
    return U(*regs)


def _grow(region, g):
    if g <= 0:
        return region
    return U(region, ST(path_to_d(region), 2 * g, "round", "round"))


def _stroke_layers(S, layers, gap):
    out = list(layers[0])
    cover = _grow(_sil(layers[0], S), gap)
    for parts in layers[1:]:
        if not parts:
            continue
        vis = D(_paint(parts, S), cover)
        if abs(vis.area) > 0.01:
            out.append(solid(path_to_d(vis)))
        cover = U(cover, _grow(_sil(parts, S), gap))
    return out


def _filled_layers(layers, gap):
    result = filled_region(layers[0])
    cover = _grow(result, gap)
    for parts in layers[1:]:
        if not parts:
            continue
        f = filled_region(parts)
        result = U(result, D(f, cover))
        cover = U(cover, _grow(f, gap))
    return result


def layered(name, desc, tags, aliases=(), gap=1.5):
    """Register an icon drawn as layers: fn(S) -> [front layer, layer behind, ...]."""
    def deco(fn):
        icon(name, CAT, desc, tags=tags, aliases=aliases,
             filled=lambda: _filled_layers(fn(LINE), gap))(lambda S: _stroke_layers(S, fn(S), gap))
        return fn
    return deco


# ============================================================================ dress and adornment

@icon("tudor-bonnet", CAT, "Flat wide-brimmed Tudor cap with a puffed crown and a feather at one side",
      tags=["tudor", "cap", "hat", "renaissance", "beret", "feather"])
def _(S):
    crown = "M6 14C5.5 10 8 8.5 12 8.5C16 8.5 18.5 10 18 14Z"
    brim = "M2.5 15.5Q12 10.5 21.5 15.5Q12 20.5 2.5 15.5Z" if S.name == "line" else ellipse(12, 15.5, 9.5, 2.75)
    plume = "M14.5 9.5C15 6 17.5 3.5 21 3C21 6.5 18.5 9 15.5 10.5Z"
    return [shell(union(crown, brim, plume)), detail("M6.5 14Q12 12.3 17.5 14")]


@icon("poulaine-shoe", CAT, "Medieval shoe with a very long pointed toe curving upward",
      tags=["medieval shoe", "crakow", "pointed shoe", "footwear", "middle ages", "costume"])
def _(S):
    heel = L(S, "M3 20V12H8", "M4.5 20Q3 20 3 18.5V13.5Q3 12 4.5 12H8")
    body = (heel + "C9 14.5 11 15.5 14 15.5C17 15.5 19.5 13.5 21.5 8.5"
            "C21.5 14.5 19 19 14 20Z")
    return [shell(body, stroke_miterlimit="10")]


@icon("liripipe-hood", CAT, "Medieval hood with a shoulder cape and a long narrow tail hanging from its peak",
      tags=["hood", "chaperon", "medieval", "cowl", "cape", "costume"])
def _(S):
    hood = ("M3.5 20.5C3.5 16.5 5.5 15 5.5 12.5V9C5.5 5.5 8 3 11.5 2.5C14 3.5 15 6 15 9V12.5"
            "C15 15 17 16.5 17 20.5Z")
    if S.name != "line":
        hood = ("M5 20.5Q3.5 20.5 3.5 19C3.5 16 5.5 15 5.5 12.5V9C5.5 5.5 8 3 11.5 2.5C14 3.5 15 6 15 9V12.5"
                "C15 15 17 16 17 19Q17 20.5 15.5 20.5Z")
    return [shell(hood), detail(ellipse(10.25, 10, 2.25, 3)),
            line("M12 2.5C16.5 1.8 20 3.5 20.5 7.5V17.5"), dot(20.5, 19.5, 1.5)]


@icon("pickelhaube", CAT, "Spiked leather helmet with a front plate and a short visor",
      tags=["spiked helmet", "prussian", "helmet", "military", "19th century", "soldier"])
def _(S):
    dome = "M2.5 17.5L3.5 16C3.5 10.5 7 7.5 11.5 7.5C16 7.5 19 10.5 19 16L21.5 18.5H17.5L17 17.5Z"
    spike = poly([(9.5, 8), (10.5, 6.5), (11.5, 3.5), (12.5, 6.5), (13.5, 8)], closed=True, r=S.r * 0.3)
    plate = poly([(13, 10.5), (17, 10.5), (17, 13), (15, 15), (13, 13)], closed=True, r=S.r * 0.4)
    return [shell(union(dome, spike), stroke_miterlimit="2"), mark(plate)]


# ============================================================================ early instruments

@icon("sackbut", CAT, "Early trombone with a narrow slide, a small flared bell and a looped tube",
      tags=["sackbut", "trombone", "renaissance", "brass", "early music", "instrument"])
def _(S):
    bell = poly([(2.5, 2.5), (8, 5), (8, 8), (2.5, 10.5)], closed=True, r=S.r * 0.5)
    return [shell(bell), line("M8 6.5H18.5A2.75 2.75 0 0 1 18.5 12H5.5A2.75 2.75 0 0 0 5.5 17.5H17"), dot(19.5, 17.5, 1.6)]


@icon("rebec", CAT, "Narrow pear-shaped bowed string instrument beside a small curved bow",
      tags=["rebec", "fiddle", "medieval", "bowed", "strings", "instrument"])
def _(S):
    body = union(circle(9, 15, 5.5), rect(7.25, 4.5, 3.5, 9, rr(S, 1)))
    return [shell(body), detail(seg(9, 9, 9, 16)), detail(seg(7, 17.5, 11, 17.5)), dot(5, 4.5, 1.25), dot(13, 4.5, 1.25),
            line("M17.5 3.5Q23.5 12 17.5 20.5"), line(seg(17.5, 3.5, 17.5, 20.5))]


@icon("psaltery", CAT, "Flat trapezoid board strung with parallel strings and a round rose sound hole",
      tags=["psaltery", "zither", "medieval", "strings", "plucked", "instrument"])
def _(S):
    board = poly([(8, 3), (16, 3), (21.5, 21), (2.5, 21)], closed=True, r=S.r)
    return [shell(board), detail(seg(7.5, 7, 16.5, 7)), detail(seg(6.3, 11, 17.7, 11)),
            detail(circle(12, 16, 2))]


@icon("portative-organ", CAT, "Small carried organ with a row of pipes of rising heights above a short keyboard",
      tags=["organ", "portative", "medieval", "pipes", "keyboard", "instrument"])
def _(S):
    keys = rect(2.5, 15, 19, 6, rr(S, 1.5))
    parts = [shell(keys)]
    for x in (7.25, 12, 16.75):
        parts.append(detail(seg(x, 18.5, x, 21)))
        parts.append(mark(rect(x - 1, 15, 2, 3.5)))
    for x, top in ((4, 10), (8, 6.5), (12, 3), (16, 6.5), (20, 10)):
        parts.append(line(seg(x, 15, x, top)))
    return parts


# ============================================================================ ancient objects and symbols

@icon("oxhide-ingot", CAT, "Flat bronze age metal ingot shaped like a stretched hide with four long curved corners",
      tags=["oxhide ingot", "copper ingot", "bronze age", "trade", "metal", "archaeology"])
def _(S):
    ends = []
    for a, b in (((2.5, 5.5), (4.5, 3.5)), ((19.5, 3.5), (21.5, 5.5)), ((21.5, 18.5), (19.5, 20.5)),
                 ((4.5, 20.5), (2.5, 18.5))):
        ends.append((a, b))
    d = f"M{fmt(ends[0][0][0])} {fmt(ends[0][0][1])}"
    ctrl = [(12, 10), (16, 12), (12, 14), (8, 12)]
    for i, (a, b) in enumerate(ends):
        if S.name == "line":
            d += f"L{fmt(b[0])} {fmt(b[1])}"
        else:
            d += f"A1.5 1.5 0 0 1 {fmt(b[0])} {fmt(b[1])}"
        n = ends[(i + 1) % 4][0]
        c = ctrl[i]
        d += f"Q{fmt(c[0])} {fmt(c[1])} {fmt(n[0])} {fmt(n[1])}"
    return [shell(d + "Z")]


def _cross_ends(S, tipfn):
    """Four copies of an arm tip drawn upward; tipfn(S, m) builds parts with the point mapper m."""
    parts = []
    for k in range(4):
        def m(x, y, k=k):
            q = rpts([(x, y)], 90 * k)[0]
            return f"{fmt(q[0])} {fmt(q[1])}"
        parts += tipfn(S, m)
    return parts


@icon("cross-fleury", CAT, "Heraldic cross whose four arms each end in a small fleur-de-lis tip",
      tags=["cross flory", "heraldry", "fleur-de-lis", "christian", "coat of arms", "medieval"])
def _(S):
    def tip(S, m):
        petal = (f"M{m(12, 2.5)}C{m(13.3, 3.8)} {m(13.3, 5.2)} {m(12, 6.5)}C{m(10.7, 5.2)} {m(10.7, 3.8)} {m(12, 2.5)}Z"
                 if S.name == "line" else f"M{m(12, 2.8)}C{m(13.8, 3.8)} {m(13.4, 5.6)} {m(12, 6.5)}C{m(10.6, 5.6)} {m(10.2, 3.8)} {m(12, 2.8)}Z")
        return [line(f"M{m(12, 12)}L{m(12, 6.5)}"),
                line(f"M{m(12, 7.5)}C{m(10.2, 7.5)} {m(9.5, 6)} {m(9.5, 4)}"),
                line(f"M{m(12, 7.5)}C{m(13.8, 7.5)} {m(14.5, 6)} {m(14.5, 4)}"),
                shell(petal)]
    return _cross_ends(S, tip)


@icon("cross-crosslet", CAT, "Heraldic cross whose four arms are each crossed by a short bar near the end",
      tags=["crosslet", "heraldry", "christian", "coat of arms", "medieval", "cross"])
def _(S):
    def tip(S, m):
        return [line(f"M{m(12, 12)}L{m(12, 2.5)}"), line(f"M{m(9, 6)}L{m(15, 6)}")]
    return _cross_ends(S, tip)


@icon("pithos", CAT, "Very large rounded storage jar with a wide mouth and raised rope bands around its body",
      tags=["pithos", "storage jar", "greek", "minoan", "pottery", "archaeology", "olive oil"])
def _(S):
    body = "M8 6C4.5 7 3.5 9.5 3.5 12C3.5 16 6.5 19.5 9 21H15C17.5 19.5 20.5 16 20.5 12C20.5 9.5 19.5 7 16 6Z"
    rim = rect(6.5, 3, 11, 3, rr(S, 1))

    def rope(y, x0, x1):
        n = 6
        w = (x1 - x0) / n
        d = f"M{fmt(x0)} {fmt(y)}"
        for i in range(n):
            d += f"Q{fmt(x0 + w * (i + 0.5))} {fmt(y + (1.3 if i % 2 else -1.3))} {fmt(x0 + w * (i + 1))} {fmt(y)}"
        return d
    return [shell(union(body, rim)), detail(rope(11, 3.6, 20.4)), detail(rope(15.5, 4.7, 19.3))]


@icon("qulliq", CAT, "Half-moon shaped stone oil lamp with a row of small flames along its straight edge",
      tags=["qulliq", "kudlik", "inuit", "oil lamp", "seal oil", "arctic", "stone lamp"])
def _(S):
    r = L(S, 0, 1.5)
    lamp = (f"M{fmt(2.5 + r)} 12H{fmt(21.5 - r)}" + (f"Q21.5 12 21.5 {fmt(12 + r)}" if r else "") +
            "C21.5 17.5 17.5 21 12 21C6.5 21 2.5 17.5 2.5 " + fmt(12 + r) + (f"Q2.5 12 {fmt(2.5 + r)} 12" if r else "") + "Z")
    parts = [shell(lamp), detail("M6 15.5H18")]
    for x in (5.5, 10, 14, 18.5):
        parts.append(solid(flame(x, 5, 10.5)))
    return parts


@icon("stirrup-spout-vessel", CAT, "Round clay pot with a hollow stirrup-shaped handle joining into one upright spout",
      tags=["stirrup spout", "moche", "andean pottery", "peru", "vessel", "ceramic", "archaeology"])
def _(S):
    spout = poly([(10.5, 2.5), (13.5, 2.5), (13, 6.5), (11, 6.5)], closed=True, r=S.r * 0.3)
    return [shell(ellipse(12, 16.5, 8, 4.5)),
            line("M7.5 13.2C7.5 4.8 16.5 4.8 16.5 13.2"), shell(spout)]


@icon("tsuba", CAT, "Round Japanese sword guard plate with a narrow central slot and a small hole on each side",
      tags=["tsuba", "sword guard", "katana", "samurai", "japanese", "metalwork"])
def _(S):
    plate = circle(12, 12, 9) if S.name != "line" else poly(regular(12, 12, 9.5, 8, -67.5), closed=True)
    slot = rect(10.75, 7, 2.5, 10, 1.25)
    return [shell(plate), mark(slot), mark(ellipse(6.5, 12, 1.1, 2.3)), mark(ellipse(17.5, 12, 1.1, 2.3))]


# ============================================================================ historic figures

def bust(S, cx=12.0, top=14.0, hw=7.0, bottom=21.0):
    """Open-bottom shoulders. Line has squarer shoulders than Rounded."""
    r = hw - (1.0 if S.name != "line" else 2.5)
    r = min(r, bottom - top)
    x0, x1 = cx - hw, cx + hw
    return (f"M{fmt(x0)} {fmt(bottom)}V{fmt(top + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x0 + r)} {fmt(top)}"
            f"H{fmt(x1 - r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(top + r)}V{fmt(bottom)}")


def head(x, y, r=2.25):
    return dot(x, y, r)


def limb(S, *pts):
    return line(poly(list(pts), r=S.r))


@layered("alchemist", "Robed alchemist in a pointed cap holding up a round flask with bubbles rising from it",
         tags=["alchemist", "alchemy", "wizard", "potion", "experiment", "medieval", "chemist"])
def _(S):
    cap = poly([(3.5, 7.5), (7.5, 3), (11.5, 7.5)], closed=True, r=S.r * 0.6)
    flask = union(circle(17, 16, 3.75), rect(15.75, 8.5, 2.5, 6))
    return [[shell(flask), dot(17, 16.5, 1)], [dot(15.5, 4.5, 1.1), dot(19.25, 3, 1.1)],
            [shell(cap)], [shell(circle(7.5, 11.5, 2.5)), line(bust(S, 7.5, 17, 5.5, 21.5))]]


@layered("druid", "Hooded bearded druid holding a tall staff topped with a sprig of mistletoe",
         tags=["druid", "celtic", "wizard", "sage", "hood", "staff", "mistletoe"])
def _(S):
    robe = ("M2.5 21V13C2.5 7 5.5 3 9.5 2.5C13.5 3 16.5 7 16.5 13V21" if S.name == "line" else
            "M2.5 21V13C2.5 7 5.5 3 9.5 2.5C13.5 3 16.5 7 16.5 13V21")
    beard = poly([(7, 12.5), (12, 12.5), (9.5, 18.5)], closed=True, r=S.r * 0.5)
    return [[shell(robe), detail(ellipse(9.5, 8.5, 2.25, 2.25)), mark(beard)],
            [line(seg(20, 7, 20, 21.5)), shell(leaf(18.25, 4.75, 4, 2, -45)), shell(leaf(21.25, 4.25, 3.5, 1.8, 40)),
             dot(20, 6.5, 1)]]


@layered("ancient-philosopher", "Bearded philosopher in a draped robe holding a scroll with one finger raised",
         tags=["philosopher", "greek", "sage", "thinker", "scholar", "antiquity", "teacher"])
def _(S):
    beard = "M5.6 7Q9 11.5 12.4 7L11.3 12.5Q9 14 6.7 12.5Z"
    scroll = [shell(union(rect(17, 12, 4, 8), ellipse(19, 12, 2.75, 1.5), ellipse(19, 20, 2.75, 1.5)))]
    return [scroll, [shell(circle(9, 5.5, 3.25)), solid(beard)],
            [line(bust(S, 9, 15.5, 6.5, 21.5)), line(seg(3.5, 16, 12, 21.5))]]


def _emperor(S):
    leaves = []
    for a in (-165, -135, -105, -75, -45, -15):
        x, y = polar(12, 8.5, 5, a)
        leaves.append(solid(rot(ellipse(x, y, 1.6, 0.9), a + 90, x, y)))
    return [leaves, [shell(circle(12, 8.5, 3.5))], [line(bust(S, 12, 15, 7.5, 21)), line(seg(6.5, 16, 16.5, 21))]]


icon("roman-emperor", CAT, "Bust of a Roman emperor wearing a laurel wreath with a toga over one shoulder",
     tags=["roman", "emperor", "caesar", "laurel", "toga", "antiquity", "rome"],
     filled=lambda: _filled_layers(_emperor(LINE), 0.75))(lambda S: _stroke_layers(S, _emperor(S), 0.75))


@layered("minstrel", "Minstrel in a feathered cap playing a lute held across the chest",
         tags=["minstrel", "bard", "troubadour", "lute", "musician", "medieval", "jester"])
def _(S):
    lute = [shell(rot(ellipse(13.5, 16.5, 5.25, 4.25), -40, 13.5, 16.5)), line(poly([(16.5, 13.5), (20, 9.5), (22, 10.5)], r=0)),
            dot(13.5, 16.5, 1.2)]
    figure = [shell(circle(7, 7.5, 2.75)), line("M4.25 6.25C4.25 3.5 6 2.5 7.5 2.5C9 2.5 10.5 3 11.5 5"),
              line(bust(S, 7, 13.5, 4.5, 21.5))]
    return [lute, figure]


@layered("knighting-ceremony", "Crowned figure touching a sword blade to the shoulder of a kneeling figure",
         tags=["knighting", "dubbing", "accolade", "knight", "king", "queen", "ceremony", "honour"], gap=1.25)
def _(S):
    crown = poly([(15, 4), (15, 1.8), (16.5, 3), (17.5, 1.5), (18.5, 3), (20, 1.8), (20, 4)], closed=True, r=S.r * 0.2)
    king = [head(17.5, 7), limb(S, (17.5, 10.5), (17.5, 15.5)), limb(S, (15.5, 21.5), (17.5, 15.5), (19.5, 21.5)),
            limb(S, (17.5, 11), (14, 12.5))]
    sword = [line(seg(6.5, 12.5, 13, 12.5)), line(seg(13, 10.5, 13, 14.5))]
    kneeler = [head(5, 8.5), limb(S, (4.5, 12), (4.5, 16), (9, 16), (9, 21.5)), line(seg(4.5, 16, 3, 21.5))]
    return [[solid(crown)] + sword, king, kneeler]


@layered("suffragette", "Woman in a wide hat and long skirt with a sash across the body holding up a placard",
         tags=["suffragette", "suffrage", "votes for women", "protest", "feminism", "equality", "history"])
def _(S):
    hat = "M3.5 7.5H16.5M6.5 7.5C6.5 4.5 8 3 10 3C12 3 13.5 4.5 13.5 7.5"
    dress = poly([(7, 13.5), (13, 13.5), (15.5, 21), (4.5, 21)], closed=True, r=S.r)
    placard = rect(15.5, 2.5, 6.5, 5, rr(S, 1.5))
    return [[shell(placard)], [line(seg(18.75, 7.5, 18.75, 16))], [line(hat)], [shell(circle(10, 10, 2))],
            [shell(dress), detail(seg(8, 14, 12.5, 19))]]


@layered("prospector", "Bearded prospector in a wide-brimmed hat with a pickaxe over one shoulder",
         tags=["prospector", "gold rush", "miner", "pioneer", "pickaxe", "panning", "wild west"])
def _(S):
    hat = [line(seg(2.5, 7, 14.5, 7)), shell(poly([(5, 7), (5.5, 3), (11.5, 3), (12, 7)], closed=True, r=S.r * 0.5))]
    face = shell(union(circle(8.5, 10, 2.5), poly([(6.2, 11), (10.8, 11), (8.5, 15.5)], closed=True, r=S.r * 0.4)))
    body = line(bust(S, 8.5, 17, 6, 21.5))
    pick = [line("M14 6Q18.5 2.5 22 7"), line(seg(18.5, 4.5, 18.5, 21.5))]
    return [hat, [face], [body], pick]


@layered("knocker-upper", "Figure in the street holding a very long pole up to tap on an upper floor window",
         tags=["knocker-upper", "alarm", "wake up", "industrial revolution", "victorian", "job", "street"], gap=1.25)
def _(S):
    win = rect(14.5, 2.5, 7, 8, rr(S, 1))
    return [[shell(win), detail(seg(18, 2.5, 18, 10.5))],
            [line(seg(5.5, 17.5, 13.5, 9.5))],
            [head(4.5, 11.5, 2), limb(S, (4.5, 14.5), (4.5, 18)), limb(S, (2.8, 21.5), (4.5, 18), (6.2, 21.5)),
             limb(S, (4.5, 15), (7, 15))]]


@layered("south-pointing-chariot", "Two-wheeled cart with a small figure standing on top, one arm pointing ahead",
         tags=["south-pointing chariot", "compass", "ancient china", "direction", "invention", "navigation"], gap=1.25)
def _(S):
    cart = rect(3, 12.5, 14, 3.5, rr(S, 1))
    return [[shell(circle(10, 18, 3.25)), dot(10, 18, 1)],
            [shell(cart), line(seg(17, 14.25, 21.5, 14.25))],
            [head(8, 3.5, 2), limb(S, (8, 6.5), (8, 10)), limb(S, (6.5, 12.5), (8, 10), (9.5, 12.5)), limb(S, (8, 7), (15, 7))]]


# ============================================================================ early vehicles

def horse(S):
    """Small horse in profile facing right, legs to the ground (same build as the transport set)."""
    body = poly([(14.5, 14.5), (14.5, 10.5), (18, 10.5), (19, 5.5), (21, 7.5), (21, 9.5), (20.5, 9.5), (20.5, 14.5)],
                closed=True, r=S.r * 0.5)
    return [shell(body), line(seg(15.5, 14.5, 15.5, 21)), line(seg(19.5, 14.5, 19.5, 21))]


def wheel(cx, cy, r, hub=1.0):
    return [shell(circle(cx, cy, r)), dot(cx, cy, hub)]


@layered("hansom-cab", "Two-wheeled closed cab with the driver perched high at the back, pulled by one horse",
         tags=["hansom", "cab", "carriage", "victorian", "horse-drawn", "taxi"], gap=1)
def _(S):
    cab = poly([(3.5, 8.5), (10, 8.5), (12, 14), (3.5, 14)], closed=True, r=S.r)
    return [wheel(7.5, 17.5, 3.5),
            [shell(cab), detail(seg(6, 11, 9, 11)), line(seg(12, 12, 14.5, 12))] + horse(S),
            [head(4, 3.5, 1.5), line(seg(3, 6, 6, 6))]]


@icon("dandy-horse", CAT, "Early running machine with two equal wheels, a padded seat and no pedals",
      tags=["draisine", "running machine", "velocipede", "hobby horse", "bicycle", "history"])
def _(S):
    return [shell(circle(5.5, 17, 4)), shell(circle(18.5, 17, 4)), dot(5.5, 17, 1), dot(18.5, 17, 1),
            line(poly([(5.5, 17), (5.5, 11), (17.5, 11)], r=S.r)), line(seg(18.5, 17, 17, 6.5)),
            line(seg(15, 6.5, 19.5, 6.5)), shell(rect(7.5, 8, 5, 3, rr(S, 1.5)))]


@icon("boneshaker-bicycle", CAT, "Early iron bicycle with pedals on a slightly larger front wheel and a curved frame",
      tags=["boneshaker", "velocipede", "vintage bicycle", "bike", "pedals", "history"])
def _(S):
    return [shell(circle(16.5, 16, 5)), shell(circle(5, 18, 3)), dot(5, 18, 1),
            line("M5 18C6 11 10 9 15 7.5"), line(seg(15, 7.5, 16.5, 16)), line(seg(13, 6, 17.5, 6)),
            shell(rect(7.5, 9.5, 4.5, 2.5, rr(S, 1.25))),
            line(seg(16.5, 16, 19.5, 19)), dot(16.5, 16, 1.25)]


@icon("steam-carriage", CAT, "Early open horseless coach with large spoked wheels and a tall smoking boiler chimney",
      tags=["steam carriage", "steam car", "horseless carriage", "locomobile", "vintage car", "history"])
def _(S):
    seat = poly([(2.5, 4), (2.5, 11.5), (10.5, 11.5)], r=S.r * 0.5)
    boiler = rect(12.5, 7, 9, 5, rr(S, 2.5))
    return [line(seat), shell(boiler), line(seg(16, 7, 16, 4)), line("M12.5 2.5Q14 1 15.5 2.5T18.5 2.5"),
            shell(circle(7, 17.5, 3.75)), dot(7, 17.5, 1), shell(circle(17.5, 17.5, 3.75)), dot(17.5, 17.5, 1)]


@icon("steam-roller", CAT, "Vintage steam road roller with a huge front roller, a tall chimney and a canopy over the driver",
      tags=["steamroller", "road roller", "traction engine", "roadworks", "vintage", "history"])
def _(S):
    boiler = rect(2.5, 7.5, 12, 4.5, rr(S, 2.25))
    return [shell(boiler), line(seg(5.5, 7.5, 5.5, 2.5)), line(seg(3.5, 2.5, 7.5, 2.5)),
            line(seg(16.5, 3, 22, 3)), line(seg(21, 3, 21, 11)), line(seg(14.5, 11, 14.5, 12)),
            shell(circle(6.5, 16.5, 4.5)), detail(circle(6.5, 16.5, 1.25)), shell(circle(18, 17, 4)), dot(18, 17, 1.1)]


def _windows(xs, y):
    return [mark(rect(x - 1, y - 1, 2, 2)) for x in xs]


@layered("horse-drawn-omnibus", "Horse-drawn double-deck coach with a row of passengers seated on the roof",
         tags=["omnibus", "horse bus", "double decker", "victorian", "public transport", "history"], gap=1)
def _(S):
    body = rect(2.5, 8, 11, 6.5, rr(S, 1.5))
    return [wheel(5.5, 18, 3) + wheel(11.5, 19, 2, 0.75),
            [shell(body), line(seg(13.5, 12.5, 14.5, 12.5))] + _windows((5.5, 8.5, 11.5), 11) + horse(S),
            [line(seg(2.5, 5.5, 13.5, 5.5)), dot(5, 3, 1.2), dot(8, 3, 1.2), dot(11, 3, 1.2)]]


@layered("horse-drawn-caravan", "Barrel-roofed wooden wagon home with a small chimney and spoked wheels, pulled by a horse",
         tags=["vardo", "caravan", "wagon", "bow top", "travelling", "horse-drawn", "history"], gap=1)
def _(S):
    wagon = "M2.5 14.5V9.5C2.5 6.5 5 5 8 5C11 5 13.5 6.5 13.5 9.5V14.5Z"
    return [wheel(5.5, 18, 3) + wheel(11.5, 19, 2, 0.75),
            [shell(wagon), line(seg(10.5, 5.5, 10.5, 2.5)), line(seg(13.5, 12.5, 14.5, 12.5))] + _windows((7,), 10) + horse(S)]


@layered("bath-chair", "Three-wheeled invalid chair with a folding hood and a long steering handle at the front",
         tags=["bath chair", "invalid carriage", "wheelchair", "victorian", "mobility", "history"], gap=1)
def _(S):
    hood = "M3 13V9.5A6.5 6.5 0 0 1 9.5 3V13Z" if S.name == "line" else "M3 13V9.5A6.5 6.5 0 0 1 9.5 3V11.5Q9.5 13 8 13Z"
    return [wheel(6.5, 17.5, 3.5),
            [shell(hood), detail(seg(5, 6.5, 9.5, 11))],
            [line(poly([(9.5, 13), (14, 13), (14, 17.5)], r=S.r))] + wheel(14, 19.5, 2, 0.75) +
            [line(seg(15, 18, 21.5, 11.5))]]


@icon("cog-ship", CAT, "Medieval single-mast ship with a high rounded hull, a square sail and a boxy stern castle",
      tags=["cog", "medieval ship", "hanseatic", "sailing ship", "merchant ship", "history"])
def _(S):
    sail = rect(8.5, 4.5, 10, 6.5, rr(S, 1.5))
    hull = poly([(2.5, 9), (7, 9), (7, 13), (22, 13), (19.5, 19), (5, 19.5), (2.5, 13)], closed=True, r=S.r)
    return [shell(sail), shell(hull), line(seg(13.5, 13, 13.5, 2))]


@icon("early-monoplane", CAT, "Early single-wing aircraft with a slim fuselage, a high wing on struts, a front propeller and a wheel",
      tags=["monoplane", "early aircraft", "vintage plane", "aviation", "pioneer", "history"])
def _(S):
    fus = poly([(2.5, 11.25), (14, 10.5), (18.5, 11.5), (19.5, 13), (18.5, 14.5), (14, 15.5), (2.5, 13.75)], closed=True, r=S.r * 0.6)
    wing = poly([(4, 4.5), (18, 4.5), (18, 7), (4, 7)], closed=True, r=S.r * 0.6)
    fin = poly([(2.5, 11.25), (2.5, 7), (6, 11)], closed=True, r=S.r * 0.3)
    return [solid(fus), solid(wing), solid(fin), line(seg(8, 7, 9, 11)), line(seg(15, 7, 14, 11)),
            line(seg(21.75, 8, 21.75, 18)), line(seg(10, 15, 10, 18.5)), dot(10, 19.75, 1.75)]


@icon("early-submarine", CAT, "Upright egg-shaped one-person wooden submarine with a domed hatch on top and a hand-cranked propeller",
      tags=["turtle submarine", "early submarine", "submersible", "naval history", "invention", "history"])
def _(S):
    hull = ellipse(10.5, 14, 6.5, 7)
    hatch = "M8 8A2.5 2.5 0 0 1 13 8" if S.name != "line" else "M8 8V5.5H13V8"
    return [shell(hull), line(hatch), line(seg(10.5, 5.5, 10.5, 3)), line(seg(8, 2.5, 13, 2.5)),
            mark(circle(10.5, 13, 1.5)), mark(circle(10.5, 17, 1.25)), line("M17 13H19.5"), line(seg(20, 8.5, 20, 17.5))]


# ============================================================================ more figures and scenes

@layered("medieval-scribe", "Hooded scribe beside a large open book, writing with a long quill",
         tags=["scribe", "monk", "manuscript", "illuminated", "medieval", "copyist", "writing"], gap=1.25)
def _(S):
    book = poly([(11.5, 10), (16.5, 8.5), (21.5, 10), (21.5, 20), (16.5, 18.5), (11.5, 20)], closed=True, r=S.r * 0.4)
    quill = [line(seg(14.5, 13.5, 20.5, 3.5)), shell(leaf(19.3, 5.5, 6, 2.4, 30))]
    return [quill, [shell(circle(6, 7.25, 2.75)), line(bust(S, 6, 13.5, 4, 21))],
            [shell(book), detail(seg(16.5, 8.5, 16.5, 18.5))]]


@icon("troika", CAT, "Three horses abreast seen from the front with a tall painted arch over the middle one",
      tags=["troika", "russian", "sleigh", "three horses", "winter", "harness", "arch", "tradition"])
def _(S):
    def face(x, top):
        return solid(f"M{fmt(x - 1.5)} {fmt(top + 2.5)}V{fmt(top)}L{fmt(x - 0.5)} {fmt(top + 1.8)}H{fmt(x + 0.5)}"
                     f"L{fmt(x + 1.5)} {fmt(top)}V{fmt(top + 2.5)}L{fmt(x + 2.2)} {fmt(top + 6)}L{fmt(x + 1.3)} {fmt(top + 12)}"
                     f"H{fmt(x - 1.3)}L{fmt(x - 2.2)} {fmt(top + 6)}Z")
    arch = "M8.25 9V8A3.75 3.75 0 0 1 15.75 8V9"
    runner = "M2.5 17C2.5 19.5 4.5 21 7 21H17C19.5 21 21.5 19.5 21.5 17"
    return [face(4.5, 6), face(12, 7), face(19.5, 6), line(arch), line(runner)]


@icon("jade-cong", CAT, "Square ritual jade tube seen from above with a round bore and a mark at each corner",
      tags=["cong", "jade", "liangzhu", "neolithic", "china", "ritual", "archaeology", "square tube"])
def _(S):
    body = rect(3, 3, 18, 18, rr(S, 3))
    parts = [shell(body), detail(circle(12, 12, 4))]
    for x, y in ((6.75, 6.75), (17.25, 6.75), (6.75, 17.25), (17.25, 17.25)):
        parts.append(dot(x, y, 1.25))
    return parts


@icon("dotaku-bell", CAT, "Tall flattened bronze bell with a thin flat loop on top, side flanges and a panelled surface",
      tags=["dotaku", "bronze bell", "yayoi", "japan", "ancient", "ritual", "archaeology"])
def _(S):
    body = poly([(8, 8.5), (16, 8.5), (19, 21), (5, 21)], closed=True, r=S.r)
    fl = [poly([(7.5, 10.5), (3, 14), (3, 18), (6, 19)], closed=True, r=S.r * 0.4),
          poly([(16.5, 10.5), (21, 14), (21, 18), (18, 19)], closed=True, r=S.r * 0.4)]
    return [shell(union(body, *fl)), line("M9.75 8.5V5.25A2.25 2.25 0 0 1 14.25 5.25V8.5"),
            detail(seg(9.25, 8.5, 8.25, 21)), detail(seg(14.75, 8.5, 15.75, 21)), detail(seg(7, 15, 17, 15))]


def _peak(x, top, w, lean, base=11.0):
    """Curled flame-like horn rising from the rim: base from x-w to x+w, tip leaning by `lean`."""
    return (f"M{fmt(x - w)} {fmt(base)}C{fmt(x - w)} {fmt(base - (base - top) * 0.45)} {fmt(x + lean * 0.3)} {fmt(top + 3)} {fmt(x + lean)} {fmt(top)}"
            f"C{fmt(x + w * 0.9 + lean * 0.4)} {fmt(top + 2.5)} {fmt(x + w)} {fmt(base - 2)} {fmt(x + w)} {fmt(base)}Z")


@icon("jomon-flame-pot", CAT, "Tall clay cooking pot whose rim rises into swirling flame-like peaks, with cord patterns on the body",
      tags=["jomon", "flame pot", "japan", "pottery", "neolithic", "ceramic", "archaeology", "cord marked"])
def _(S):
    pot = poly([(7.5, 21), (16.5, 21), (19, 11), (5, 11)], closed=True, r=S.r * 0.6)
    peaks = [_peak(7, 4.5, 2.2, -1.5), _peak(12, 2.5, 2.2, 1.0), _peak(17, 4.5, 2.2, 1.5)]
    return [shell(union(pot, *peaks)), detail("M7 15Q9.5 13 12 15T17 15"), detail("M8 19Q10 17.5 12 19T16 19")]


@layered("chacmool", "Reclining stone figure with bent knees and raised torso, head turned outward, holding a flat dish on its stomach",
         tags=["chacmool", "chac mool", "maya", "aztec", "toltec", "mesoamerica", "sculpture", "offering"], gap=1.25)
def _(S):
    dish = poly([(9.5, 10.5), (16.5, 10.5), (15.5, 13.5), (10.5, 13.5)], closed=True, r=S.r * 0.4)
    head = [shell(circle(19, 6, 2.75))]
    body = [line(poly([(2.5, 20.5), (7, 11), (11, 20), (18, 14)], r=S.r)), line(seg(11, 20, 20, 20)),
            line(seg(18, 14, 19, 9.5))]
    return [[shell(dish)], head, body]


@layered("ballcourt-ring", "Carved stone ring mounted high on a sloping stone wall with a ball beside it",
         tags=["ball court", "ballcourt", "mesoamerica", "maya", "aztec", "ring", "ullamaliztli", "archaeology"], gap=1.25)
def _(S):
    wall = poly([(9.5, 21), (14.5, 3.5), (21.5, 3.5), (21.5, 21)], closed=True, r=S.r)
    return [[line(circle(17.5, 10.5, 3))], [shell(wall)], [dot(5, 17.5, 3)]]


@icon("trapezoid-doorway", CAT, "Doorway narrower at the top set in a wall of tightly fitted polygonal stone blocks",
      tags=["inca", "trapezoidal door", "stonework", "masonry", "machu picchu", "ancient wall", "archaeology"])
def _(S):
    wall = rect(2.5, 2.5, 19, 19, rr(S, 2))
    door = poly([(7.5, 21), (9.5, 8.5), (14.5, 8.5), (16.5, 21)], r=S.r * 0.5)
    return [shell(wall), line(door), detail("M2.5 9L5.5 11.5"), detail("M2.5 15.5L4.5 14.5"), detail("M21.5 10L18.5 12.5"),
            detail("M21.5 16L19.5 15")]


# ============================================================================ daily life, places and objects

@icon("warp-weighted-loom", CAT, "Upright wooden loom frame with vertical threads held taut by a row of hanging weights",
      tags=["loom", "warp-weighted loom", "weaving", "textile", "neolithic", "viking", "ancient craft"])
def _(S):
    parts = [line(seg(2.5, 3.5, 21.5, 3.5)), line(seg(4, 3.5, 4, 21.5)), line(seg(20, 3.5, 20, 21.5))]
    for x in (8.5, 12, 15.5):
        parts.append(detail(seg(x, 3.5, x, 15.5)))
        parts.append(dot(x, 18, 1.75))
    return parts


@icon("distaff", CAT, "Tall staff with a bundle of loose fiber on top and a thread running down to a small hanging spindle",
      tags=["distaff", "spindle", "spinning", "wool", "flax", "thread", "textile", "ancient craft"])
def _(S):
    bundle = "M4.75 11.5C3.75 7 5.5 4 8 2.5C10.5 4 12.25 7 11.25 11.5Z"
    spindle = poly([(17, 14), (18.5, 18), (17, 21.5), (15.5, 18)], closed=True, r=S.r * 0.3)
    return [line(seg(8, 11, 8, 21.5)), shell(bundle), detail("M6.75 5.5L7.25 9"), detail("M9.5 5.5L9.25 9"),
            line("M11.5 8.5C15 9 17 10.5 17 14"), shell(spindle, stroke_miterlimit="2")]


@icon("fireplace-crane", CAT, "Iron arm swung out from the side of a hearth with a cooking pot hanging from a hook above the flames",
      tags=["hearth", "crane", "cauldron", "pot hook", "fireplace", "cooking", "medieval kitchen"])
def _(S):
    pot = poly([(11, 8), (20, 8), (20, 11.5), (18, 14.5), (13, 14.5), (11, 11.5)], closed=True, r=S.r * 0.6)
    return [line(seg(3.5, 2.5, 3.5, 21.5)), line(seg(3.5, 4, 19.5, 4)), line(seg(3.5, 12.5, 11, 4)),
            line(seg(15.5, 4, 15.5, 8)), shell(pot), solid(flame(12, 17, 21.5, 1.5)), solid(flame(16, 16.5, 21.5, 1.6)),
            solid(flame(20, 17, 21.5, 1.5))]


@icon("roman-fort", CAT, "Top view of a square walled Roman camp with corner towers, four gates and two crossing roads",
      tags=["castra", "roman camp", "legion", "fort", "walls", "top view", "military", "archaeology"])
def _(S):
    wall = rect(5, 5, 14, 14, rr(S, 1))
    towers = [rect(2.5, 2.5, 5.5, 5.5, rr(S, 1.25)), rect(16, 2.5, 5.5, 5.5, rr(S, 1.25)),
              rect(2.5, 16, 5.5, 5.5, rr(S, 1.25)), rect(16, 16, 5.5, 5.5, rr(S, 1.25))]
    return [shell(union(wall, *towers)), detail(seg(12, 5, 12, 19)), detail(seg(5, 12, 19, 12))]


@icon("knot-garden", CAT, "Top view of a square garden bed edged with hedges, a central diamond hedge, a round bed and four corner beds",
      tags=["knot garden", "parterre", "hedge", "tudor garden", "topiary", "formal garden", "top view"])
def _(S):
    parts = [shell(rect(2.5, 2.5, 19, 19, S.R)), detail(poly([(12, 6.25), (17.75, 12), (12, 17.75), (6.25, 12)], closed=True, r=S.r * 0.5)),
             dot(12, 12, 1.6)]
    for x, y in ((6, 6), (18, 6), (6, 18), (18, 18)):
        parts.append(dot(x, y, 1.1))
    return parts


@icon("inhabited-bridge", CAT, "Multi-arched stone bridge with a row of tall narrow gabled houses built along its top",
      tags=["inhabited bridge", "ponte vecchio", "medieval bridge", "arches", "houses on bridge", "stone bridge", "river"])
def _(S):
    houses = poly([(3, 15), (3, 9.5), (6, 5.5), (9, 9.5), (12, 5.5), (15, 9.5), (18, 5.5), (21, 9.5), (21, 15)],
                  closed=True, r=S.r * 0.4)
    deck = rect(2.5, 14, 19, 7.5, rr(S, 1))
    return [shell(union(houses, deck)), detail(seg(2.5, 14.5, 21.5, 14.5)), detail("M5 21.5V19.5A2.5 2.5 0 0 1 10 19.5V21.5"),
            detail("M14 21.5V19.5A2.5 2.5 0 0 1 19 19.5V21.5"), detail(seg(9, 9.5, 9, 14)), detail(seg(15, 9.5, 15, 14))]


@icon("cabinet-of-curiosities", CAT, "Open wooden cabinet with a shelf holding a globe, a jar, a skull and a seashell",
      tags=["wunderkammer", "curiosity cabinet", "collection", "natural history", "specimens", "renaissance", "museum"])
def _(S):
    jar = poly([(14.5, 4.5), (17.5, 4.5), (17.5, 6), (18.75, 7.25), (18.75, 11), (13.25, 11), (13.25, 7.25), (14.5, 6)],
               closed=True, r=S.r * 0.3)
    skull = union(circle(7.5, 16.5, 2.6), rect(6.25, 18, 2.5, 2.5))
    shellp = "M13 20.5Q12.5 16 16 14.75Q19.5 16 19 20.5Z"
    return [shell(rect(2.5, 2.5, 19, 19, S.R)), detail(seg(2.5, 12.5, 21.5, 12.5)),
            mark(circle(7.5, 8.5, 2.5)), mark(jar), mark(skull), mark(shellp)]


@icon("toby-jug", CAT, "Pottery jug shaped like a seated stout man in a three-cornered hat holding a mug, with a handle at the back",
      tags=["toby jug", "character jug", "pottery", "pub", "tankard", "english", "antique", "ceramic"])
def _(S):
    hat = poly([(3, 7.5), (5.5, 2.5), (12, 5), (18.5, 2.5), (21, 7.5)], closed=True, r=S.r * 0.4)
    body = ellipse(12, 17.5, 6.5, 4)
    face = circle(12, 10, 3.25)
    return [shell(union(hat, face, body)), line("M18 14.5C22.5 14 22.5 20.5 18 20"), mark(circle(10.75, 9.5, 0.8)),
            mark(circle(13.25, 9.5, 0.8)), mark(rect(9.5, 15.5, 5, 3.5, rr(S, 0.75)))]


@icon("solar-barque", CAT, "Long crescent-shaped ancient boat with upturned papyrus-bundle ends and a small shrine holding the sun disc",
      tags=["solar barque", "egyptian boat", "ra", "sun boat", "papyrus", "ancient egypt", "sacred boat", "mythology"])
def _(S):
    hull = ("M2.5 9C3.5 15 7.5 18.5 12 18.5C16.5 18.5 20.5 15 21.5 9C18.5 12.5 15.5 13.5 12 13.5C8.5 13.5 5.5 12.5 2.5 9Z")
    shrine = rect(9.5, 7.5, 5, 7, rr(S, 1))
    return [shell(union(hull, shrine)), line(seg(8.5, 7.5, 15.5, 7.5)), dot(12, 3.5, 1.75),
            dot(2.5, 6, 1.4), dot(21.5, 6, 1.4)]


@icon("lamellar-armor", CAT, "Torso armor made of rows of small vertical plates laced together in horizontal bands",
      tags=["lamellar", "cuirass", "samurai", "scale armor", "byzantine", "steppe", "plate armor", "warrior"])
def _(S):
    torso = poly([(3.5, 6), (8, 3), (12, 6.5), (16, 3), (20.5, 6), (18, 10), (18.5, 21.5), (5.5, 21.5), (6, 10)],
                 closed=True, r=S.r * 0.6)
    parts = [shell(torso), detail(seg(6, 13, 18, 13)), detail(seg(5.8, 17.5, 18.2, 17.5))]
    for x in (10, 14):
        parts.append(detail(seg(x, 14, x, 16.5)))
    for x in (8.5, 12, 15.5):
        parts.append(detail(seg(x, 18.5, x, 21)))
    parts.append(detail(seg(12, 9.5, 12, 12)))
    return parts


@icon("roman-dodecahedron", CAT, "Small hollow twelve-sided bronze object with a round hole in each face and a knob at every corner",
      tags=["dodecahedron", "gallo-roman", "bronze", "puzzling object", "artifact", "archaeology", "mystery"])
def _(S):
    outer = regular(12, 12, 8, 10)
    inner = regular(12, 12, 4.25, 5)
    parts = [shell(poly(outer, closed=True) if S.name == "line" else circle(12, 12, 8)), detail(poly(inner, closed=True, r=S.r * 0.4))]
    for k in range(5):
        a = -90 + 72 * k
        parts.append(detail(seg(*polar(12, 12, 4.25, a), *polar(12, 12, 8, a))))
    parts.append(dot(12, 12, 1.25))
    for x, y in outer:
        parts.append(dot(x, y, 1.4))
    return parts


@icon("ceremonial-feather-fan", CAT, "Long pole topped with a half-circle fan of tall ostrich feathers",
      tags=["feather fan", "flabellum", "ostrich feather", "pharaoh", "ceremonial", "ancient egypt", "regalia", "royal"])
def _(S):
    feathers = []
    for a in (-150, -120, -90, -60, -30):
        x, y = polar(12, 14, 5.6, a)
        feathers.append(leaf(x, y, 11, 4.6, a + 90) if S.name == "line" else rot(ellipse(x, y, 2.3, 5.5), a + 90, x, y))
    parts = [shell(union(*feathers)), line(seg(12, 14, 12, 22))]
    for a in (-135, -105, -75, -45):
        parts.append(detail(seg(*polar(12, 14, 3, a), *polar(12, 14, 8.5, a))))
    return parts


@icon("pictish-stone", CAT, "Upright carved stone slab marked with a crescent crossed by a rod above a pair of joined discs",
      tags=["pictish stone", "symbol stone", "picts", "scotland", "carved stone", "crescent and v-rod", "archaeology"])
def _(S):
    slab = poly([(5.5, 21.5), (5.5, 4.5), (8, 2.5), (16, 2.5), (18.5, 4.5), (18.5, 21.5)], closed=True, r=S.r * 0.8)
    return [shell(slab), detail("M8.5 6A3.5 3.5 0 0 0 15.5 6"), detail(poly([(9.5, 4), (12, 10), (14.5, 4)])),
            detail(seg(9.5, 16, 14.5, 16)), dot(9.25, 16, 1.75), dot(14.75, 16, 1.75)]
