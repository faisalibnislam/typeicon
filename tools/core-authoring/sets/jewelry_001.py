"""TypeIcon Core: jewelry (batch jewelry_001).

Rings, bracelets, necklaces, earrings, piercings, gem cuts and settings, findings, chains and watch parts.
Round gems are drawn as faceted polygons in Line and smooth circles in Rounded (see rd). Small stones are
`dot` parts, which are solid in Line/Rounded and knocked out in Filled.
"""
import math

from dsl import D, I, P, Part, ST, U, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar  # noqa: F401

CAT = "jewelry"


def rd(S, cx, cy, r, n=8):
    """Round outline: n-gon in Line, circle in Rounded."""
    if S.name == "line":
        return poly(regular(cx, cy, r, n, start=-90 + 180 / n), closed=True)
    return circle(cx, cy, r)


def ov(S, cx, cy, rx, ry, n=12):
    """Oval outline: polygon in Line, ellipse in Rounded."""
    if S.name == "line":
        pts = [(cx + rx * math.cos(math.radians(i * 360 / n)), cy + ry * math.sin(math.radians(i * 360 / n))) for i in range(n)]
        return poly(pts, closed=True)
    return ellipse(cx, cy, rx, ry)


def ring_dots(cx, cy, r, n, rr=1.0, start=-90.0, skip=()):
    return [dot(*polar(cx, cy, r, start + i * 360 / n), rr) for i in range(n) if i not in skip]


def sq(x, y, w, h, rx=0.0) -> Part:
    return Part("dot", rect(x, y, w, h, rx))


# ============================================================================ rings

@icon("eternity-band", CAT, "Ring band seen face on with a continuous row of small round stones set all the way around.",
      tags=["eternity ring", "wedding band", "anniversary ring", "stone ring", "diamond band", "jewelry"])
def _(S):
    return [shell(rd(S, 12, 12, 9, 12)), shell(rd(S, 12, 12, 4.2, 8))] + ring_dots(12, 12, 6.6, 8, 1.05, start=-90 + 22.5)


@icon("cocktail-ring", CAT, "Ring with an oversized oval stone sitting on a raised mount above a round band.",
      tags=["statement ring", "big ring", "gemstone ring", "dome ring", "jewelry", "party ring"])
def _(S):
    return [
        line(arc(12, 16.5, 5.5, 340, 200)),
        shell(poly([(8.5, 11), (15.5, 11), (14, 14.5), (10, 14.5)], closed=True, r=S.r * 0.5)),
        shell(ov(S, 12, 7, 8.5, 4.2, 10)),
    ]


@icon("poison-ring", CAT, "Ring with a small square box on top and its lid flipped open above it.",
      tags=["secret ring", "compartment ring", "locket ring", "pillbox ring", "hidden", "jewelry"])
def _(S):
    return [
        line(arc(12, 17, 5.5, 335, 205)),
        shell(rect(5.5, 10, 13, 5.5, min(S.R, 2))),
        shell(poly([(8.5, 3), (15.5, 3), (18.5, 7), (5.5, 7)], closed=True, r=S.r)),
    ]


@icon("spinner-ring", CAT, "Wide ring band with a loose middle band between two arrows that show it spins.",
      tags=["fidget ring", "meditation ring", "worry ring", "anxiety ring", "rotating band", "jewelry"])
def _(S):
    return [
        shell(rect(3, 8, 18, 8, S.R * 0.6)),
        detail(seg(9, 8, 9, 16)), detail(seg(15, 8, 15, 16)),
        line(poly([(6, 4.5), (18, 4.5)])), line(poly([(15.5, 2.5), (18, 4.5), (15.5, 6.5)], r=S.r * 0.4)),
        line(poly([(18, 19.5), (6, 19.5)])), line(poly([(8.5, 17.5), (6, 19.5), (8.5, 21.5)], r=S.r * 0.4)),
    ]


@icon("three-stone-ring", CAT, "Ring front view with a large round stone flanked by two smaller stones above the band.",
      tags=["trilogy ring", "past present future", "engagement ring", "gemstone ring", "jewelry", "triple stone"])
def _(S):
    return [
        line(arc(12, 17, 6, 330, 210)),
        shell(rd(S, 12, 8.2, 3.4, 8)),
        dot(4.6, 10.5, 2.1), dot(19.4, 10.5, 2.1),
    ]


@icon("halo-ring", CAT, "Top view of a ring with a round centre stone surrounded by a circle of tiny stones.",
      tags=["halo setting", "engagement ring", "cluster", "diamond ring", "jewelry", "gemstone"])
def _(S):
    outer = circle(12, 12, 9.3) if S.name == "rounded" else poly(regular(12, 12, 9.3, 12), closed=True)
    return [shell(rd(S, 12, 12, 3.4, 8)), line(outer)] + ring_dots(12, 12, 6.6, 8, 1.2, start=-67.5)


@icon("tension-ring", CAT, "Open ring band whose two ends pinch a single stone held between them.",
      tags=["tension setting", "floating stone", "engagement ring", "gemstone ring", "jewelry", "suspended"])
def _(S):
    return [
        line(arc(12, 14.5, 7.5, 305, 235)),
        shell(poly([(12, 2.5), (16, 7), (12, 11.5), (8, 7)], closed=True, r=S.r * 0.7)),
    ]


@icon("tennis-bracelet", CAT, "Oval bracelet made of a continuous line of small round stones with a box clasp.",
      tags=["diamond bracelet", "line bracelet", "stone bracelet", "wrist", "jewelry", "riviere"])
def _(S):
    stones = [dot(12 + 9 * math.cos(math.radians(a)), 11.5 + 6.5 * math.sin(math.radians(a)), 1.6) for a in range(0, 360, 30) if a != 90]
    return stones + [shell(rect(8.5, 16, 7, 5, S.R))]


@icon("id-bracelet", CAT, "Chain bracelet laid flat with a rectangular name plate in the middle carrying an engraved line.",
      tags=["name bracelet", "identity bracelet", "medical id", "engraved plate", "chain bracelet", "jewelry"])
def _(S):
    return [
        shell(rect(7, 7.5, 10, 9, min(S.R, 2.5))),
        detail(seg(9.5, 12, 14.5, 12)),
        shell(ov(S, 3.6, 12, 2.4, 2.2, 8)), shell(ov(S, 20.4, 12, 2.4, 2.2, 8)),
    ]


# ============================================================================ necklaces and earrings

def ear_d(S, dx=0.0, dy=0.0):
    """Closed ear outline (right ear, front view), shifted by (dx, dy)."""
    def f(*v):
        return " ".join(fmt(x + (dx if i % 2 == 0 else dy)) for i, x in enumerate(v))
    if S.name == "line":
        return ("M" + f(6, 6) + "C" + f(11, 2.5, 17.5, 4, 18, 10) + "C" + f(18.3, 14.5, 14.5, 15, 14.5, 18.5)
                + "C" + f(14.5, 21, 12.5, 22, 10.5, 21.5) + "C" + f(8.5, 21, 6, 19.5, 6, 18) + "Z")
    return ("M" + f(7.5, 6) + "C" + f(11, 2.5, 17.5, 4, 18, 10) + "C" + f(18.3, 14.5, 14.5, 15, 14.5, 18.5)
            + "C" + f(14.5, 21, 12.5, 22, 10.5, 21.5) + "C" + f(8.5, 21, 6, 19.5, 6, 18) + "L" + f(6, 8) + "Q" + f(6, 6.8, 7.5, 6) + "Z")


@icon("lariat-necklace", CAT, "Long open necklace chain looped round the neck with two strands hanging down to small tassel drops.",
      tags=["y necklace", "drop necklace", "long chain", "chain necklace", "tassel", "jewelry"])
def _(S):
    return [
        line("M4 3C4 11 8 14 12 14C16 14 20 11 20 3"),
        line(poly([(10.2, 19.5), (12, 14), (13.8, 19.5)])),
        dot(10, 20.5, 1.6), dot(14, 20.5, 1.6),
    ]


@icon("bib-necklace", CAT, "Wide crescent collar necklace with a band of stones graded in size across the front.",
      tags=["statement necklace", "collar necklace", "choker", "jeweled collar", "gem necklace", "jewelry"])
def _(S):
    body = ("M3 3C3 13 8 20 12 20C16 20 21 13 21 3L17.5 3C17.5 9 15 14.5 12 14.5C9 14.5 6.5 9 6.5 3Z" if S.name == "rounded"
            else "M3 3L5 12L12 20L19 12L21 3L17.5 3L16 9L12 14.5L8 9L6.5 3Z")
    return [shell(body), dot(12, 17.2, 1.3), dot(7.3, 11.6, 1.0), dot(16.7, 11.6, 1.0)]


@icon("nameplate-necklace", CAT, "Fine chain holding a horizontal plate that carries a wavy cursive script word.",
      tags=["name necklace", "custom necklace", "personalised jewelry", "script plate", "chain", "jewelry"])
def _(S):
    return [
        line("M3 3C3 9 6 12.5 8.5 13.5"), line("M21 3C21 9 18 12.5 15.5 13.5"),
        shell(rect(4.5, 13.5, 15, 7.5, min(S.R, 2.5))),
        detail("M8 17.3Q9.5 14.8 11 17.3T14 17.3T17 17.3"),
    ]


@icon("initial-pendant", CAT, "Chain with a round disc pendant showing a single bold capital letter.",
      tags=["letter necklace", "monogram", "alphabet pendant", "disc pendant", "custom jewelry", "necklace"])
def _(S):
    return [
        line(poly([(4, 3), (12, 10.5), (20, 3)])),
        shell(rd(S, 12, 16, 5, 10)),
        detail(seg(9.5, 14.2, 14.5, 14.2)), detail(seg(12, 14.2, 12, 19)),
    ]


@icon("solitaire-pendant", CAT, "Thin chain with a single faceted stone hanging from it at its lowest point.",
      tags=["diamond pendant", "single stone", "necklace", "gem", "chain", "jewelry"])
def _(S):
    return [
        line(poly([(3, 3), (12, 11.5), (21, 3)])),
        shell(poly([(8, 12), (16, 12), (19, 15.5), (12, 22), (5, 15.5)], closed=True, r=S.r * 0.6)),
        detail(seg(5.5, 15.5, 18.5, 15.5)),
    ]


@icon("multi-strand-necklace", CAT, "Three chain necklaces of different lengths layered below one another.",
      tags=["layered necklaces", "layering", "stacked chains", "chains", "necklace set", "jewelry"])
def _(S):
    return [
        line("M7 3C7 6 9 7.5 12 7.5C15 7.5 17 6 17 3"),
        line("M5 3C5 9 8 12.5 12 12.5C16 12.5 19 9 19 3"),
        line("M3 3C3 12 7 18 12 18C17 18 21 12 21 3"),
    ]


@icon("tassel-earring", CAT, "Ear hook with a small metal cap from which a bundle of long fringe threads hangs.",
      tags=["fringe earring", "drop earring", "boho", "festival earring", "dangle", "jewelry"])
def _(S):
    return [
        line("M12 2.5V6"),
        shell(poly([(9.5, 6), (14.5, 6), (14, 9.5), (10, 9.5)], closed=True, r=S.r * 0.4)),
        line("M10.5 10L8 21.5"), line("M12 10V21.5"), line("M13.5 10L16 21.5"),
    ]


@icon("ear-climber", CAT, "Ear outline with a curved row of small stones climbing along its outer edge.",
      tags=["ear crawler", "ear cuff", "earring", "ear jewelry", "stones", "jewelry"])
def _(S):
    return [shell(ear_d(S, -2.5, 1.5))] + [dot(*p, 1.4) for p in [(19.8, 13.8), (20.6, 9.4), (18.6, 5.2), (14.6, 2.8)]]


@icon("clip-on-earring", CAT, "Round button earring with a spring clip behind it instead of a post.",
      tags=["clip earring", "non pierced", "screw back", "button earring", "ear", "jewelry"])
def _(S):
    return [
        line(poly([(12, 7.5), (19.5, 7.5), (19.5, 17.5), (12, 17.5)], r=S.r * 0.6)),
        shell(rd(S, 9.5, 12.5, 6, 10)),
    ]


@icon("jhumka-earring", CAT, "Earring with a round stud on top and a dome shaped bell hanging below, edged with bead drops.",
      tags=["jhumki", "bell earring", "indian earring", "south asian jewelry", "dome earring", "jewelry"])
def _(S):
    bell = ("M5.5 15.5C5.5 10 8.5 7.8 12 7.8C15.5 7.8 18.5 10 18.5 15.5Z" if S.name == "rounded"
            else "M5.5 15.5L7 10L12 7.8L17 10L18.5 15.5Z")
    return [dot(12, 4, 2.0), shell(bell), dot(7.8, 20, 1.5), dot(12, 20.4, 1.5), dot(16.2, 20, 1.5)]


@icon("chandbali-earring", CAT, "Crescent moon shaped earring hanging from a stud, its lower curve lined with small bead drops.",
      tags=["chand bali", "moon earring", "crescent earring", "indian earring", "south asian jewelry", "jewelry"])
def _(S):
    cres = ("M3.5 8C4 13.5 8 16.5 12 16.5C16 16.5 20 13.5 20.5 8C18 11.5 15 12.5 12 12.5C9 12.5 6 11.5 3.5 8Z" if S.name == "rounded"
            else "M3.5 8L7 14L12 16.5L17 14L20.5 8L17 11L12 12.5L7 11Z")
    return [line(poly([(4, 7.5), (12, 2.8), (20, 7.5)])), dot(12, 3.2, 1.8), shell(cres),
            dot(7.5, 20.3, 1.2), dot(12, 21, 1.2), dot(16.5, 20.3, 1.2)]


@icon("ear-gauge", CAT, "Ear outline with a large round hollow tunnel plug stretching the piercing in the lobe.",
      tags=["ear tunnel", "flesh tunnel", "stretched lobe", "plug", "body modification", "piercing"])
def _(S):
    ear = "M6 18V8Q6 6.8 7.5 6C11 2.5 17.5 4 18 10C18.2 12.5 17 13.8 16 15" if S.name == "rounded" else \
        "M6 18V6C11 2.5 17.5 4 18 10C18.2 12.5 17 13.8 16 15"
    return [line(ear), shell(rd(S, 11.2, 18, 3.6, 10)), dot(11.2, 18, 1.0)]


@icon("nose-stud", CAT, "Side view of a nose with a tiny round gem stud on the side of the nostril.",
      tags=["nose piercing", "nostril stud", "nose screw", "nose pin", "face jewelry", "piercing"])
def _(S):
    nose = ("M11 3C11 8 9.5 11.5 6.5 15C5.5 16.5 6.5 18.5 8.5 18.5H13C15.5 18.5 16.3 15.6 14 14" if S.name == "rounded"
            else "M11 3L11 8L6.5 15L7 18.5L13 18.5L15.5 16L14 14")
    return [line(nose), dot(14.9, 16, 1.9)]


@icon("barbell-piercing", CAT, "Short straight bar with a small ball on each end, the standard piercing barbell shown alone.",
      tags=["body jewelry", "tongue bar", "ear bar", "straight barbell", "piercing", "industrial"])
def _(S):
    return [line(seg(7.5, 16.5, 16.5, 7.5)), shell(rd(S, 5.2, 18.8, 2.6, 8)), shell(rd(S, 18.8, 5.2, 2.6, 8))]


@icon("stickpin", CAT, "Long straight pin with a small jewel on the head and a tiny guard cap on the point.",
      tags=["tie pin", "lapel pin", "hat pin", "jeweled pin", "cravat pin", "jewelry"])
def _(S):
    return [line(seg(14.5, 9.5, 6.5, 17.5)), shell(rd(S, 17.5, 6.5, 3.4, 6)), dot(5.2, 18.8, 1.7)]


@icon("sovereign-orb", CAT, "Royal orb: a sphere with two jewelled bands around it and a small cross on top.",
      tags=["globus cruciger", "royal orb", "regalia", "crown jewels", "monarch", "cross orb"])
def _(S):
    return [
        shell(rd(S, 12, 14, 6.8, 12)),
        detail("M5.4 11.8C9 13.6 15 13.6 18.6 11.8"), detail("M5.4 16.6C9 18.4 15 18.4 18.6 16.6"),
        line(seg(12, 2, 12, 6.5)), line(seg(9.8, 3.8, 14.2, 3.8)),
    ]


# ============================================================================ settings and gem cuts

def half_round(S, cx, cy, r, n=8):
    """Upper half disc (flat edge at the bottom) as a closed outline."""
    if S.name == "line":
        pts = [polar(cx, cy, r, 180 + i * 180 / n) for i in range(n + 1)]
        return poly(pts, closed=True)
    return f"M{fmt(cx - r)} {fmt(cy)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx + r)} {fmt(cy)}Z"


def blob(S, pts, k=2.2):
    return poly(pts, closed=True, r=S.r * k)


def scaled(pts, f, cx=12.0, cy=12.0, rot=0.0):
    a = math.radians(rot)
    out = []
    for x, y in pts:
        dx, dy = (x - cx) * f, (y - cy) * f
        out.append((cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a)))
    return out


@icon("prong-setting", CAT, "Top view of a round stone gripped by four small metal claws at its edge.",
      tags=["claw setting", "four prong", "stone mount", "gem setting", "jewelry", "engagement ring"])
def _(S):
    return [shell(rd(S, 12, 12, 5, 8))] + [dot(*polar(12, 12, 7.6, a), 2.0) for a in (45, 135, 225, 315)]


@icon("bezel-setting", CAT, "Round stone surrounded by a smooth raised metal rim, on a ring band.",
      tags=["bezel", "rim setting", "collet", "stone mount", "gem setting", "jewelry"])
def _(S):
    return [line(arc(12, 14.5, 6.6, 350, 190)), shell(rd(S, 12, 8, 6.2, 12)), detail(rd(S, 12, 8, 2.6, 8))]


@icon("channel-setting", CAT, "Ring band section with a row of square stones sitting in a groove between two metal walls.",
      tags=["channel set", "baguette stones", "square stones", "gem setting", "band", "jewelry"])
def _(S):
    return [shell(rect(2, 6, 20, 12, S.R)), sq(4.5, 10, 4, 4), sq(10, 10, 4, 4), sq(15.5, 10, 4, 4)]


@icon("pave-setting", CAT, "Ring band covered with many tiny round stones set close together with beads of metal between them.",
      tags=["pave", "diamond band", "sparkle", "tiny stones", "gem setting", "jewelry"])
def _(S):
    ds = []
    for i, y in enumerate((8.6, 12, 15.4)):
        xs = (5.2, 8.7, 12.2, 15.7, 19.2) if i % 2 == 0 else (6.9, 10.4, 13.9, 17.4)
        ds += [dot(x, y, 0.95) for x in xs]
    return [shell(rect(2, 4.5, 20, 15, S.R))] + ds


@icon("flush-setting", CAT, "Plain wide band with a stone sunk level with the metal and a small star engraved around it.",
      tags=["gypsy setting", "burnish setting", "star engraving", "flush set", "band", "jewelry"])
def _(S):
    cx, cy = 12, 12
    rays = [detail(seg(*polar(cx, cy, 4.6, a), *polar(cx, cy, 4.6, a + 180))) for a in (0, 45, 90, 135)]
    return [shell(rect(2, 5, 20, 14, S.R))] + rays + [dot(12, 12, 1.8)]


@icon("rose-cut", CAT, "Top view of a round gem with a domed centre divided into a star of small triangular facets.",
      tags=["rose cut diamond", "dome gem", "antique cut", "facets", "diamond", "gemstone"])
def _(S):
    star = []
    for i in range(12):
        star.append(polar(12, 12, 6.2 if i % 2 == 0 else 3.4, -90 + i * 30))
    return [shell(rd(S, 12, 12, 9.5, 12)), detail(poly(star, closed=True))]


@icon("asscher-cut", CAT, "Top view of a square gem with clipped corners and stepped square rings forming a tunnel effect.",
      tags=["step cut", "square emerald cut", "art deco gem", "diamond", "gemstone", "facets"])
def _(S):
    return [
        shell(poly([(8, 3), (16, 3), (21, 8), (21, 16), (16, 21), (8, 21), (3, 16), (3, 8)], closed=True, r=S.r * 1.6)),
        detail(poly([(10, 8), (14, 8), (16, 10), (16, 14), (14, 16), (10, 16), (8, 14), (8, 10)], closed=True)),
    ]


@icon("radiant-cut", CAT, "Top view of a rectangular gem with clipped corners and criss-crossing brilliant facet lines.",
      tags=["radiant diamond", "rectangular gem", "brilliant cut", "facets", "diamond", "gemstone"])
def _(S):
    return [
        shell(poly([(8, 2.5), (16, 2.5), (19.5, 6), (19.5, 18), (16, 21.5), (8, 21.5), (4.5, 18), (4.5, 6)], closed=True, r=S.r * 1.6)),
        detail(poly([(12, 7.5), (15.5, 12), (12, 16.5), (8.5, 12)], closed=True)),
        detail(seg(12, 3.5, 12, 7.5)), detail(seg(12, 16.5, 12, 20.5)), detail(seg(15.5, 12, 18.5, 12)), detail(seg(5.5, 12, 8.5, 12)),
    ]


@icon("briolette", CAT, "Teardrop shaped gem covered all over in small triangular facets with a drilled hole near the tip.",
      tags=["drop gem", "faceted teardrop", "bead", "gem drop", "facets", "gemstone"])
def _(S):
    tear = ("M12 2.5C13.5 6 19 9.5 19 15A7 7 0 0 1 5 15C5 9.5 10.5 6 12 2.5Z" if S.name == "rounded"
            else "M12 2.5L19 12L19 16L15 21L9 21L5 16L5 12Z")
    return [shell(tear), detail(poly([(5.5, 14), (9, 10.5), (12, 14), (15, 10.5), (18.5, 14)])), detail(poly([(8.5, 19.5), (12, 14), (15.5, 19.5)])), dot(12, 6, 1.0)]


@icon("half-moon-cut", CAT, "Top view of a half circle gem with a straight edge and curved step lines of facets.",
      tags=["half moon gem", "semicircle gem", "demi lune", "side stone", "facets", "gemstone"])
def _(S):
    return [shell(half_round(S, 12, 18, 9.5)), detail(half_round(S, 12, 18, 4.2, 6)), detail(seg(*polar(12, 18, 4.5, 225), *polar(12, 18, 8.2, 225))), detail(seg(12, 13.5, 12, 9.8)), detail(seg(*polar(12, 18, 4.5, 315), *polar(12, 18, 8.2, 315)))]


@icon("shield-cut", CAT, "Top view of a gem in a heraldic shield outline with a flat top and pointed bottom and inner facets.",
      tags=["shield gem", "heraldic cut", "fancy cut", "diamond", "gemstone", "facets"])
def _(S):
    outer = ("M4 3H20V11C20 16.5 16.5 19.5 12 22C7.5 19.5 4 16.5 4 11Z" if S.name == "rounded"
             else "M4 3L20 3L20 12L12 22L4 12Z")
    inner = ("M8.5 8H15.5V11.5C15.5 13.5 14 15.5 12 17C10 15.5 8.5 13.5 8.5 11.5Z" if S.name == "rounded"
             else "M8.5 8L15.5 8L15.5 12L12 17L8.5 12Z")
    return [shell(outer), detail(inner)]


@icon("kite-cut", CAT, "Top view of a kite shaped gem with a long pointed bottom, a short pointed top and facet lines.",
      tags=["kite gem", "kite diamond", "fancy cut", "facets", "diamond", "gemstone"])
def _(S):
    return [
        shell(poly([(12, 2), (19.5, 9), (12, 22), (4.5, 9)], closed=True, r=S.r * 0.6)),
        detail(poly([(12, 6.5), (15, 9.5), (12, 16), (9, 9.5)], closed=True)),
    ]


@icon("hexagon-cut", CAT, "Top view of a six sided gem with a smaller hexagon table and facet lines running to the corners.",
      tags=["hexagonal gem", "hex cut", "six sided gem", "facets", "diamond", "gemstone"])
def _(S):
    outer = regular(12, 12, 10, 6)
    inner = regular(12, 12, 4.6, 6)
    return [shell(poly(outer, closed=True, r=S.r * 1.5)), detail(poly(inner, closed=True))] + [detail(seg(*polar(12, 12, 4.8, -90 + i * 60), *polar(12, 12, 8.4, -90 + i * 60))) for i in range(6)]


@icon("bullet-cut", CAT, "Top view of a long narrow gem with a flat base and a pointed arched top like a bullet.",
      tags=["bullet gem", "arch cut", "tapered baguette", "fancy cut", "diamond", "gemstone"])
def _(S):
    outer = ("M5 21.5V10C5 6 8 3 12 2.5C16 3 19 6 19 10V21.5Z" if S.name == "rounded" else "M5 21.5L5 9.5L12 2.5L19 9.5L19 21.5Z")
    return [shell(outer), detail(poly([(9, 18), (9, 11), (12, 8), (15, 11), (15, 18)]))]


@icon("star-sapphire", CAT, "Domed oval cabochon with a six rayed star of light crossing its surface.",
      tags=["asterism", "star stone", "sapphire", "ruby", "cabochon", "gemstone"])
def _(S):
    return [shell(ov(S, 12, 12, 9.5, 8.8, 12))] + [detail(seg(*polar(12, 12, 4.7, a), *polar(12, 12, 4.7, a + 180))) for a in (90, 30, 150)]


@icon("cats-eye-gem", CAT, "Oval polished cabochon with a single bright slit of light down the centre.",
      tags=["chrysoberyl", "cat's eye", "chatoyancy", "cabochon", "tiger eye", "gemstone"])
def _(S):
    return [shell(ov(S, 12, 12, 8, 9.5, 12)), detail(seg(12, 5.5, 12, 18.5))]


@icon("watermelon-tourmaline", CAT, "Triangular crystal slice with a solid inner core and a distinct outer rind band.",
      tags=["tourmaline slice", "bicolor crystal", "pink green stone", "crystal slice", "gemstone", "mineral"])
def _(S):
    return [shell(poly([(12, 2.5), (21.5, 19.5), (2.5, 19.5)], closed=True, r=S.r * 0.8)),
            Part("dot", poly([(12, 8.8), (16.7, 16.8), (7.3, 16.8)], closed=True, r=S.r * 0.4))]


AGATE = [(5, 9), (8, 4.2), (14.5, 3.6), (19.5, 7.5), (20.5, 14), (16.5, 19.8), (9.5, 20.4), (4, 16)]


@icon("agate-slice", CAT, "Irregular oval stone slab with wavy concentric bands and a small crystal hollow at the centre.",
      tags=["agate", "banded stone", "geode slice", "mineral slab", "coaster", "gemstone"])
def _(S):
    return [shell(blob(S, AGATE)), detail(blob(S, scaled(AGATE, 0.5, rot=20), 1.6)), dot(12, 12, 1.5)]


BAROQUE = [(7, 5), (13, 3), (18.5, 5.8), (20.8, 11.5), (18.2, 17.5), (12.5, 21.5), (6.5, 20), (3.2, 14.5), (5, 9)]


@icon("baroque-pearl", CAT, "Irregular lumpy pearl shape with a soft highlight, clearly not round.",
      tags=["freeform pearl", "lumpy pearl", "irregular pearl", "pearl", "gemstone", "organic gem"])
def _(S):
    pts = [(6, 6), (11.5, 3), (17, 4.5), (20.5, 9.5), (18.5, 14), (21, 18.5), (15, 21.5), (8.5, 20), (3.5, 15), (4.5, 10)]
    return [shell(blob(S, pts, 2.6)), detail("M8 10C8.4 8.2 9.6 7.2 11.2 7")]


NUGGET = [(6, 5.5), (12, 3.5), (18.5, 6), (21, 12), (18.5, 18), (12, 21), (6, 19.5), (3, 13), (3.8, 8.5)]


@icon("turquoise-nugget", CAT, "Rounded rough stone with a web of thin dark matrix veins running across its surface.",
      tags=["turquoise", "matrix stone", "veined stone", "raw gem", "southwestern jewelry", "gemstone"])
def _(S):
    return [shell(blob(S, NUGGET, 2.6)), detail(poly([(6, 10), (9.5, 12.5), (8.5, 17)])), detail(poly([(11.5, 6), (13.5, 10), (18, 11.5)])),
            detail(poly([(12.5, 15.5), (16, 17)]))]


@icon("trapiche-emerald", CAT, "Hexagonal gem slice with six dark spokes radiating from a small solid hexagon in the centre.",
      tags=["trapiche", "spoked emerald", "wheel gem", "emerald slice", "hexagon crystal", "gemstone"])
def _(S):
    return [shell(poly(regular(12, 12, 10, 6, start=0), closed=True, r=S.r * 0.5)),
            Part("dot", poly(regular(12, 12, 2.6, 6, start=0), closed=True))] + [
        line(seg(*polar(12, 12, 2.6, a), *polar(12, 12, 8.6, a))) for a in range(0, 360, 60)]


# ============================================================================ findings and chains

def tilt(pts, deg, cx, cy):
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * sn, cy + (x - cx) * sn + (y - cy) * c) for x, y in pts]


def oval_pts(cx, cy, rx, ry, n=14, deg=0.0):
    pts = [(cx + rx * math.cos(math.radians(i * 360 / n)), cy + ry * math.sin(math.radians(i * 360 / n))) for i in range(n)]
    return tilt(pts, deg, cx, cy)


def spiral(cx, cy, r0, r1, turns, n=28, start=0.0):
    return [polar(cx, cy, r0 + (r1 - r0) * i / n, start + 360 * turns * i / n) for i in range(n + 1)]


def toothed(cx, cy, r_out, r_in, n, start=-90.0):
    """Gear outline points: n square-ish teeth."""
    pts = []
    step = 360 / n
    for i in range(n):
        a = start + i * step
        pts += [polar(cx, cy, r_in, a), polar(cx, cy, r_out, a + step * 0.18), polar(cx, cy, r_out, a + step * 0.5), polar(cx, cy, r_in, a + step * 0.68)]
    return pts


@icon("pendant-bail", CAT, "Small folded metal loop hanging a teardrop pendant, with a chain passing through the loop.",
      tags=["bail", "pendant loop", "chain loop", "jewelry finding", "necklace", "teardrop pendant"])
def _(S):
    drop = ("M12 10C13.5 12.5 17.5 14 17.5 17.2A5.5 5.5 0 0 1 6.5 17.2C6.5 14 10.5 12.5 12 10Z" if S.name == "rounded"
            else "M12 10L17.5 15.5L15.5 21L8.5 21L6.5 15.5Z")
    return [line(seg(2, 5, 9.5, 5)), line(seg(14.5, 5, 22, 5)), shell(rect(9.5, 2.5, 5, 7, min(S.R, 2))), shell(drop)]


@icon("ear-wire", CAT, "Single fishhook earring wire curving up and over, ending in a small open loop at the bottom.",
      tags=["fish hook", "earring hook", "earring finding", "jewelry making", "hook wire", "dangle"])
def _(S):
    hook = ("M12 14V9C12 4.2 16.5 2.5 19 5C20.6 6.8 20 9.5 19 11" if S.name == "rounded"
            else "M12 14L12 8L15 3.5L19.5 5L20 11")
    return [line(hook), shell(rd(S, 12, 17.7, 3.4, 8))]


@icon("earring-back", CAT, "Butterfly shaped earring back clutch with two wings and a hole in the middle for the post.",
      tags=["butterfly clutch", "earring clutch", "earring stopper", "post back", "jewelry finding", "backing"])
def _(S):
    from geometry import P as _P, U as _U
    k = S.r * 2.6
    wl = _P(poly(oval_pts(6.8, 12, 4.8, 6.6, 14, -20), closed=True, r=k))
    wr = _P(poly(oval_pts(17.2, 12, 4.8, 6.6, 14, 20), closed=True, r=k))
    return [shell(path_to_d(_U(wl, wr, _P(circle(12, 12, 3.6))))), dot(12, 12, 1.5)]


@icon("head-pin", CAT, "Straight thin wire pin with a flat disc head at the bottom and a bead threaded on it.",
      tags=["jewelry wire", "beading pin", "bead pin", "findings", "jewelry making", "headpin"])
def _(S):
    return [line(seg(12, 2, 12, 7)), shell(rd(S, 12, 11.5, 3.7, 8)), line(seg(12, 15.2, 12, 19.5)), solid(rect(8, 19.5, 8, 2.5, 0.6))]


@icon("eye-pin", CAT, "Straight thin wire pin with a small round loop at one end and a bead threaded on it.",
      tags=["jewelry wire", "beading pin", "loop pin", "findings", "jewelry making", "eyepin"])
def _(S):
    return [shell(rd(S, 12, 4.8, 2.6, 8)), line(seg(12, 7.4, 12, 10.5)), shell(rd(S, 12, 14.5, 3.8, 8)), line(seg(12, 18.3, 12, 22))]


@icon("rope-chain", CAT, "Short length of chain made of twisted links forming a diagonal spiral rope pattern.",
      tags=["twisted chain", "rope necklace", "gold chain", "twist links", "chain", "jewelry"])
def _(S):
    return [shell(rect(2, 7, 20, 10, S.R * 1.6)), detail(seg(6.5, 7, 9, 17)), detail(seg(11.5, 7, 14, 17)), detail(seg(16.5, 7, 19, 17))]


@icon("box-chain", CAT, "Short length of chain made of small square box links joined in a straight line.",
      tags=["venetian chain", "square link chain", "box link", "gold chain", "chain", "jewelry"])
def _(S):
    return [shell(rect(2, 7.5, 20, 9, S.R * 0.5)), detail(seg(8.7, 7.5, 8.7, 16.5)), detail(seg(15.3, 7.5, 15.3, 16.5))]


@icon("curb-chain", CAT, "Short length of flat oval links that lie interlocked and slanted against each other.",
      tags=["curb link", "cuban chain", "flat chain", "gold chain", "chain", "jewelry"])
def _(S):
    return [shell(poly(oval_pts(x, 12, 5, 3.4, 12, 35), closed=True, r=S.r * 2)) for x in (6, 12, 18)]


@icon("figaro-chain", CAT, "Short length of chain with a pattern of small round links followed by one long oval link.",
      tags=["figaro link", "mariner chain", "three one chain", "gold chain", "chain", "jewelry"])
def _(S):
    return [shell(rd(S, 3.8, 12, 2.2, 8)), shell(rd(S, 9.2, 12, 2.2, 8)), shell(poly(oval_pts(17, 12, 5, 2.8, 12), closed=True, r=S.r * 2))]


@icon("snake-chain", CAT, "Short smooth flexible tube of chain with fine scale ridges along it, curving in an S.",
      tags=["snake necklace", "flat snake", "herringbone", "gold chain", "chain", "jewelry"])
def _(S):
    pts = [(3.5 + 17 * t, 12 - 4.6 * math.sin(2 * math.pi * t)) for t in [i / 24 for i in range(25)]]
    ridges = []
    for t in (0.2, 0.38, 0.56, 0.74):
        x = 3.5 + 17 * t
        y = 12 - 4.6 * math.sin(2 * math.pi * t)
        dy = -4.6 * 2 * math.pi * math.cos(2 * math.pi * t) / 17
        n = math.hypot(1, dy)
        nx, ny = -dy / n, 1 / n
        ridges.append(detail(seg(x - nx * 2.4, y - ny * 2.4, x + nx * 2.4, y + ny * 2.4)))
    tube = path_to_d(ST(poly(pts), 4.6, "butt" if S.name == "line" else "round", "miter" if S.name == "line" else "round"))
    return [shell(tube)] + ridges


@icon("rectangular-watch", CAT, "Wristwatch with a tall rectangular case, two hands, and short straps above and below.",
      tags=["tank watch", "square watch", "dress watch", "wrist watch", "timepiece", "jewelry"])
def _(S):
    return [
        shell(rect(6.5, 6.5, 11, 11, S.R)),
        detail(poly([(12, 9.5), (12, 12), (14.5, 13)])),
        line(poly([(9, 6.5), (9, 2.5), (15, 2.5), (15, 6.5)])), line(poly([(9, 17.5), (9, 21.5), (15, 21.5), (15, 17.5)])),
    ]


@icon("watch-caseback", CAT, "Round watch back with a notched screw ring around its edge and an engraved line in the centre.",
      tags=["case back", "screw back", "back cover", "watch repair", "watchmaker", "watch"])
def _(S):
    return [shell(rd(S, 12, 12, 9.5, 12)), detail(circle(12, 12, 4.8) if S.name == "rounded" else poly(regular(12, 12, 4.8, 8), closed=True)),
            detail(seg(9.8, 12, 14.2, 12))] + ring_dots(12, 12, 7.15, 8, 0.9, start=-67.5)


@icon("balance-wheel", CAT, "Round watch balance wheel with a spoke across it and a fine spiral hairspring coiled at the centre.",
      tags=["hairspring", "oscillator", "watch movement", "watchmaker", "clockwork", "mechanical watch"])
def _(S):
    return [line(rd(S, 12, 12, 9.2, 14)), line(seg(3.2, 12, 7.2, 12)), line(seg(16.8, 12, 20.8, 12)),
            line(poly(spiral(12, 12, 1.0, 5.0, 1.25, 24), r=S.r * 0.4))]


@icon("escapement", CAT, "Toothed escape wheel with an anchor shaped pallet fork resting on its top teeth.",
      tags=["escape wheel", "pallet fork", "anchor escapement", "watch movement", "clockwork", "mechanical watch"])
def _(S):
    return [
        shell(poly(toothed(12, 15.6, 5.8, 3.8, 8), closed=True, r=S.r * 0.3)),
        line(poly([(4.5, 9), (8, 4.5), (16, 4.5), (19.5, 9)], r=S.r * 0.6)),
        dot(4.5, 9.5, 1.7), dot(19.5, 9.5, 1.7), dot(12, 4.5, 1.6),
    ]


@icon("mainspring-barrel", CAT, "Round drum with gear teeth on its rim and an open face showing a tightly coiled flat spring.",
      tags=["spring barrel", "mainspring", "watch movement", "winding", "clockwork", "mechanical watch"])
def _(S):
    return [shell(poly(toothed(12, 12, 10, 8.6, 12), closed=True, r=S.r * 0.3)),
            detail(poly(spiral(12, 12, 1.2, 5.8, 1.4, 26), r=S.r * 0.4)), dot(12, 12, 1.3)]


@icon("watch-rotor", CAT, "Half moon shaped oscillating weight pivoting at the centre of a round watch movement.",
      tags=["automatic winding", "oscillating weight", "self winding", "watch movement", "watchmaker", "mechanical watch"])
def _(S):
    return [line(rd(S, 12, 12, 9.5, 12)), shell(half_round(S, 12, 13, 6.2, 6)), dot(12, 13, 1.2)]


@icon("spring-bar", CAT, "Short thin tube with spring loaded pins at both ends, shown between two watch lugs.",
      tags=["strap bar", "watch strap", "lug bar", "watch repair", "watchmaker", "spring loaded pin"])
def _(S):
    return [line(seg(2.5, 5, 2.5, 19)), line(seg(21.5, 5, 21.5, 19)), line(seg(2.5, 12, 6.5, 12)), line(seg(17.5, 12, 21.5, 12)),
            shell(rect(6.5, 9.5, 11, 5, min(S.R, 2.4)))]


@icon("metal-watch-band", CAT, "Wristwatch strap of short rows of three linked metal segments, shown straight.",
      tags=["bracelet strap", "link bracelet", "steel strap", "watch strap", "watch band", "watch"])
def _(S):
    return [shell(rect(6, 2, 12, 20, S.R * 0.5)), detail(seg(10, 2, 10, 22)), detail(seg(14, 2, 14, 22)),
            detail(seg(10, 7.5, 14, 7.5)), detail(seg(10, 12, 14, 12)), detail(seg(10, 16.5, 14, 16.5)),
            detail(seg(6, 10, 10, 10)), detail(seg(14, 10, 18, 10)), detail(seg(6, 14.5, 10, 14.5)), detail(seg(14, 14.5, 18, 14.5))]


@icon("tourbillon", CAT, "Round cage with a crossbar frame holding a small balance wheel, with a curved arrow showing it rotates.",
      tags=["rotating cage", "watch complication", "haute horlogerie", "watch movement", "watchmaker", "mechanical watch"])
def _(S):
    a_end = 340
    tip = polar(12, 12, 9.4, a_end)
    ux, uy = -math.sin(math.radians(a_end)), math.cos(math.radians(a_end))
    nx, ny = math.cos(math.radians(a_end)), math.sin(math.radians(a_end))
    b1 = (tip[0] - ux * 3 + nx * 2.2, tip[1] - uy * 3 + ny * 2.2)
    b2 = (tip[0] - ux * 3 - nx * 2.2, tip[1] - uy * 3 - ny * 2.2)
    return [
        shell(rd(S, 12, 12, 5.6, 10)),
        detail(rd(S, 12, 12, 2.2, 6)),
        line(arc(12, 12, 9.4, 200, a_end)), line(poly([b1, tip, b2], r=S.r * 0.3)),
    ]


@icon("watchmaker-screwdriver", CAT, "Very slim screwdriver with a ridged shaft and a small swiveling cap on top of the handle.",
      tags=["jeweler screwdriver", "precision screwdriver", "watch repair", "eyeglass screwdriver", "micro tool", "watchmaker"])
def _(S):
    def R(pts):
        return tilt(pts, 45, 12, 12)
    return [
        line(poly(R([(12, 2), (12, 8.5)]))),
        shell(poly(R([(9.5, 8.5), (14.5, 8.5), (14.5, 17.5), (9.5, 17.5)]), closed=True, r=S.r * 0.4)),
        detail(poly(R([(9.5, 11.5), (14.5, 11.5)]))), detail(poly(R([(9.5, 14.5), (14.5, 14.5)]))),
        solid(poly(R([(10.5, 19.5), (13.5, 19.5), (13.5, 21.5), (10.5, 21.5)]), closed=True)),
    ]
