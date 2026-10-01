"""TypeIcon Core: household (batch household_005): hair care, makeup, nails, skin care, laundry care and bath items.

Original drawings of everyday beauty, grooming and laundry objects. Bodies are shells; labels, folds and texture
marks are details so the Filled style knocks them out. Laundry care symbols are plain geometry.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import LINE, I, fmt, path_to_d, polar, rotation, transform_path

CAT = "household"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def mark(d) -> Part:
    return Part("dot", d)


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(pts, deg, cx=12.0, cy=12.0):
    """Rotate points clockwise on screen about (cx, cy)."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rotd(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rp(pts, deg, closed=True, r=0.0, cx=12.0, cy=12.0):
    return poly(rot(pts, deg, cx, cy), closed=closed, r=r)


# ============================================================================ hair care

@icon("hair-net", CAT, "Dome-shaped hair net with a mesh of lines and an elastic rim",
      tags=["hairnet", "mesh", "cap", "kitchen", "hygiene", "food safety", "bun"])
def _(S):
    return [
        shell("M4.5 14A7.5 7.5 0 0 1 19.5 14Z"),
        detail("M12 6.5V14"),
        detail("M8.3 14Q8.3 9.5 12 6.5"),
        detail("M15.7 14Q15.7 9.5 12 6.5"),
        shell(rect(3, 14, 18, 4, L(S, 1, 2))),
    ]


@icon("shampoo", CAT, "Tall shampoo bottle with a flip cap and a hair strand on the label",
      tags=["shampoo bottle", "hair wash", "bathroom", "toiletries", "conditioner", "hair care"])
def _(S):
    return [
        shell(rect(6.5, 9, 11, 13, rr(S, 3))),
        shell(rect(9.5, 6, 5, 3, 0.5)),
        shell(rect(8.5, 2.5, 7, 3.5, L(S, 0.5, 1.5))),
        detail("M11 12.5C13.5 14 9.5 17 12.5 19"),
    ]


@icon("hairspray", CAT, "Aerosol can with a round cap, a hair strand on the label and a fan of fine spray",
      tags=["hair spray", "aerosol", "styling", "hold", "hair product", "salon", "mist"])
def _(S):
    return [
        shell(rect(4.5, 9.5, 9.5, 12.5, rr(S, 2.5))),
        shell(rect(6, 5, 6.5, 4.5, L(S, 1, 2))),
        detail("M8.5 13C11 14.5 7 17 10 19"),
        line(seg(16.5, 5, 20, 3)),
        line(seg(17, 8, 21.5, 8)),
        line(seg(16.5, 11, 20, 13)),
    ]


@icon("hair-wax", CAT, "Short round pot of hair wax with a finger swipe across the surface",
      tags=["pomade", "clay", "styling", "hair product", "tub", "hair gel", "jar", "barber"])
def _(S):
    body = "M3.5 10.5V17.5A8.5 4 0 0 0 20.5 17.5V10.5A8.5 4 0 0 0 3.5 10.5Z"
    return [
        shell(body),
        detail(ellipse(12, 10.5, 8.5, 4)),
        line("M8.5 10.5Q12 12.5 15.5 9.5"),
    ]


@icon("hair-dye", CAT, "Mixing bowl of hair color with a tint brush resting across it",
      tags=["hair color", "tint", "bleach", "colouring", "salon", "bowl", "brush", "highlights"])
def _(S):
    return [
        shell("M3.5 12H20.5C20.5 17 17 21 12 21C7 21 3.5 17 3.5 12Z"),
        line(seg(3, 4.5, 11, 8.5)),
        shell(poly([(11, 8.5), (13, 4.5), (18, 6.5), (16, 10.5)], closed=True, r=S.r * 0.6)),
    ]


@icon("salon-hood-dryer", CAT, "Seated salon hair dryer with a large dome hood on an arm and pole",
      tags=["hood dryer", "salon", "hair dryer", "hairdresser", "perm", "setting", "beauty parlour"])
def _(S):
    return [
        shell("M3 12A7.5 7.5 0 0 1 18 12Z"),
        dot(8.5, 9, 1), dot(12.5, 9, 1),
        line(poly([(18, 8.5), (20, 8.5), (20, 21)], r=S.r)),
        line(seg(16, 21, 22, 21)),
        line(poly([(4, 17), (4, 21)])),
    ]


@icon("shampoo-basin", CAT, "Salon backwash basin with a curved neck rest, faucet and a reclining chair back",
      tags=["backwash", "salon sink", "hairdresser", "hair washing", "basin", "salon chair", "rinse"])
def _(S):
    return [
        shell("M10 9H21V12.5C21 16 18.5 18 15.5 18H10Q12.5 13.5 10 9Z"),
        line(poly([(19, 9), (19, 5), (16, 5)], r=S.r)),
        line(seg(15.5, 18, 15.5, 21)),
        line(seg(12, 21, 19, 21)),
        line(poly([(2.5, 5.5), (6.5, 14), (6.5, 21)], r=S.r)),
    ]


@icon("wig", CAT, "Wig of long wavy hair with a side part and an open cap at the face",
      tags=["hairpiece", "toupee", "fake hair", "costume", "hair loss", "synthetic", "drag"])
def _(S):
    return [
        shell("M12 3C7.5 3 4.5 6.5 4.5 11C4.5 15 6 17 5 20C5 21 7 21.5 8.5 20.5C9.7 19.5 9.5 17 9.5 14.5C9.5 12 10.5 10.5 12 9C13.5 10.5 14.5 12 14.5 14.5C14.5 17 14.3 19.5 15.5 20.5C17 21.5 19 21 19 20C18 17 19.5 15 19.5 11C19.5 6.5 16.5 3 12 3Z"),
        detail("M10 4C10 6.5 8.5 8.5 7 9.5"),
    ]


@icon("hair-extension", CAT, "Clip-in hair extension weft with small clips on its top edge and long strands below",
      tags=["weft", "clip-in", "hair piece", "add length", "volume", "salon", "hair accessory"])
def _(S):
    return [
        shell(rect(3.5, 6.5, 17, 3.5, L(S, 0.5, 1.7))),
        sq(4.5, 3, 3, 3.5), sq(10.5, 3, 3, 3.5), sq(16.5, 3, 3, 3.5),
        line("M6.5 10C5.5 13 7.5 16 6.5 21"),
        line("M11 10C10 13 12 16 11 21"),
        line("M15.5 10C14.5 13 16.5 16 15.5 21"),
        line("M19.5 10V17"),
    ]


@icon("hair-bun", CAT, "Back of a head with hair gathered into a round bun on top and shoulders below",
      tags=["updo", "topknot", "hairstyle", "ballerina bun", "hair tie", "chignon", "messy bun"])
def _(S):
    head = union(circle(12, 11.5, 5.5), circle(12, 4.5, 3.2))
    return [
        shell(head),
        line(poly([(4, 21), (4.5, 20), (8, 19.3), (16, 19.3), (19.5, 20), (20, 21)], r=S.r)),
        detail("M8.5 8.5C10.5 10.5 13.5 10.5 15.5 8.5"),
    ]


@icon("braid", CAT, "Single plaited braid of stacked interlocking segments with a hair tie at the end",
      tags=["plait", "hairstyle", "pigtail", "three strand", "hair tie", "french braid", "hair"])
def _(S):
    links = union(rotd(ellipse(12, 5.5, 5, 2.8), 30, 12, 5.5), rotd(ellipse(12, 10.5, 5, 2.8), -30, 12, 10.5),
                  rotd(ellipse(12, 15.5, 5, 2.8), 30, 12, 15.5))
    return [
        shell(links),
        detail("M8 8.2L16 7.8"),
        detail("M8 13.2L16 12.8"),
        shell(rect(9, 19, 6, 2.5, L(S, 0.5, 1.2))),
    ]


@icon("ponytail", CAT, "Head in side view with hair pulled back into a swinging ponytail",
      tags=["hairstyle", "hair tie", "scrunchie", "pony tail", "pulled back", "sporty", "hair"])
def _(S):
    head = union(circle(9.5, 12.5, 6.5), "M15 9.5C19.5 6.5 22 10 21 14C20.3 17 18.5 19 16.5 19.5C18.5 16 17.5 13 15.5 12Z")
    return [
        shell(head),
        dot(6.5, 12, 1),
        detail("M5 9C8 6.5 11 7 13 9"),
    ]


@icon("hair-loss", CAT, "Head with a bare crown and loose curling strands falling away beside it",
      tags=["balding", "alopecia", "thinning", "receding", "shedding", "hair fall", "bald spot"])
def _(S):
    return [
        shell(circle(8, 11.5, 5.5)),
        line("M16.5 3.5C19 5.5 15 7.5 17.5 10"),
        line("M20.5 11C22 13 19 15 20.5 17.5"),
        line("M15 15.5C17 17 14 19 16 21.5"),
    ]


@icon("dandruff", CAT, "Hair strands hanging from the scalp with small white flakes falling from them",
      tags=["flakes", "itchy scalp", "dry scalp", "anti-dandruff", "scalp care", "seborrheic", "hair"])
def _(S):
    return [
        line(seg(3.5, 3.5, 20.5, 3.5)),
        line("M6.5 3.5C4.5 7 8.5 9 6.5 13"),
        line("M12 3.5C10 7 14 9 12 13"),
        line("M17.5 3.5C15.5 7 19.5 9 17.5 13"),
        dot(5, 17.5, 1.5), dot(10, 20, 1.5), dot(14.5, 17, 1.5), dot(19, 20, 1.5),
    ]


@icon("hair-wash", CAT, "Head covered with a cap of foam on top and water drops falling around it",
      tags=["washing hair", "shampooing", "lather", "bubbles", "rinse", "suds", "bath"])
def _(S):
    foam = union(circle(8.5, 9.5, 3.3), circle(12.5, 7.5, 3.8), circle(16, 10, 3))
    return [
        shell(foam),
        line(arc(12, 14, 7.5, 0, 180)),
        dot(3, 15, 1.2), dot(21, 15, 1.2), dot(6, 20, 1.2),
    ]


# ============================================================================ makeup

@icon("mascara", CAT, "Mascara tube with its spiky bristle wand pulled out above it",
      tags=["lashes", "eye makeup", "wand", "volumizing", "cosmetics", "beauty", "eyelash"])
def _(S):
    return [
        shell(rect(7, 15, 10, 7, rr(S, 2.5))),
        line(seg(12, 11, 12, 15)),
        shell(ellipse(12, 6.5, 2.3, 4.5)),
        line(seg(6.5, 3.5, 9.7, 3.5)), line(seg(6.5, 6.5, 9.7, 6.5)), line(seg(6.5, 9.5, 9.7, 9.5)),
        line(seg(14.3, 3.5, 17.5, 3.5)), line(seg(14.3, 6.5, 17.5, 6.5)), line(seg(14.3, 9.5, 17.5, 9.5)),
    ]


@icon("eyeliner", CAT, "Slim eyeliner pencil with a fine sharpened tip and a band near the end",
      tags=["liner", "kohl pencil", "eye makeup", "cosmetics", "wing", "waterline", "beauty"])
def _(S):
    return [
        shell(rp([(12, 2), (14.2, 7.5), (14.2, 21.5), (9.8, 21.5), (9.8, 7.5)], 45, r=S.r * 0.5)),
        detail(rp([(9.8, 7.5), (14.2, 7.5)], 45, closed=False)),
        detail(rp([(9.8, 17), (14.2, 17)], 45, closed=False)),
    ]


@icon("eyebrow-pencil", CAT, "Eyebrow pencil with a spoolie brush at the other end and a brow arch beside it",
      tags=["brow", "brow pencil", "spoolie", "eyebrow brush", "makeup", "cosmetics", "arched brow"])
def _(S):
    return [
        shell(rp([(12, 1.5), (14, 6), (14, 15.5), (10, 15.5), (10, 6)], 45, r=S.r * 0.5)),
        detail(rp([(10, 6), (14, 6)], 45, closed=False)),
        shell(rp([(10.5, 15.5), (13.5, 15.5), (13.5, 21.5), (10.5, 21.5)], 45, r=S.r * 0.5)),
        line("M12.5 21C15 17.5 18.5 17 21.5 19"),
    ]


@icon("eyeshadow-palette", CAT, "Open eyeshadow palette with a mirror in the lid and a row of round shadow pans",
      tags=["eye shadow", "makeup palette", "cosmetics", "pans", "blush", "contour", "beauty"])
def _(S):
    return [
        shell(rect(3, 3, 18, 7, rr(S, 2.5))),
        detail(seg(8, 8, 11, 5)),
        shell(rect(3, 13, 18, 8, rr(S, 2.5))),
        dot(7.5, 17, 1.5), dot(12, 17, 1.5), dot(16.5, 17, 1.5),
    ]


@icon("powder-compact", CAT, "Round powder compact seen from above with a pressed powder cake and a puff resting on it",
      tags=["pressed powder", "makeup", "puff", "face powder", "mirror compact", "cosmetics", "beauty"])
def _(S):
    return [
        shell(union(rect(4, 2.5, 16, 11.5, 5.5), rect(3, 13.5, 18, 8, L(S, 2, 4)))),
        detail(seg(3, 13.5, 21, 13.5)),
        detail(seg(8.5, 8, 11.5, 5.5)),
        mark(circle(12, 17.5, 1.6)),
    ]


@icon("makeup-brush", CAT, "Makeup brush with a fluffy domed head, a metal ferrule and a long tapered handle",
      tags=["blush brush", "powder brush", "cosmetics", "beauty", "bristles", "applicator", "face"])
def _(S):
    return [
        shell(rotd("M8.5 9.5C8.5 4.5 10 2.5 12 2.5C14 2.5 15.5 4.5 15.5 9.5Z", 45)),
        shell(rp([(9, 9.5), (15, 9.5), (15, 13.5), (9, 13.5)], 45, r=S.r * 0.4)),
        shell(rp([(10.3, 13.5), (13.7, 13.5), (12.8, 22), (11.2, 22)], 45, r=S.r * 0.3)),
    ]


@icon("fan-brush", CAT, "Makeup brush with a flat fan-shaped bristle head, a ferrule and a handle",
      tags=["highlighter brush", "fan", "cosmetics", "beauty", "bristles", "sweep", "applicator"])
def _(S):
    p1, p2 = polar(12, 13.5, 11, -130), polar(12, 13.5, 11, -50)
    fan = f"M12 13.5L{fmt(p1[0])} {fmt(p1[1])}A11 11 0 0 1 {fmt(p2[0])} {fmt(p2[1])}Z"
    return [
        shell(rotd(fan, 45)),
        detail(rp([(12, 13.5), (12, 6)], 45, closed=False)),
        shell(rp([(10, 13.5), (14, 13.5), (14, 16.5), (10, 16.5)], 45, r=S.r * 0.4)),
        shell(rp([(10.6, 16.5), (13.4, 16.5), (12.8, 22), (11.2, 22)], 45, r=S.r * 0.3)),
    ]


@icon("foundation", CAT, "Square glass foundation bottle with a pump top and a drop of liquid beside it",
      tags=["makeup", "base", "liquid foundation", "pump bottle", "cosmetics", "complexion", "beauty"])
def _(S):
    drop = "M19 10.5C19 10.5 16.6 13.6 16.6 15.3A2.4 2.4 0 0 0 21.4 15.3C21.4 13.6 19 10.5 19 10.5Z"
    return [
        shell(rect(3.5, 11, 10.5, 11, rr(S, 2.5))),
        shell(rect(7, 8, 3.5, 3, 0.3)),
        line(poly([(8.75, 8), (8.75, 4), (13, 4)], r=S.r)),
        detail(seg(3.5, 15.5, 14, 15.5)),
        solid(drop),
    ]


@icon("lip-gloss", CAT, "Tube of lip gloss with an angled doe-foot tip and a sparkle of shine",
      tags=["gloss", "lip shine", "lips", "makeup", "cosmetics", "wand", "beauty"])
def _(S):
    return [
        shell(rect(5.5, 10, 9, 12, rr(S, 2.5))),
        shell(poly([(7.5, 10), (7.5, 6), (11, 2.5), (13, 6), (13, 10)], closed=True, r=S.r)),
        solid(poly([(19, 3.5), (19.9, 5.6), (22, 6.5), (19.9, 7.4), (19, 9.5), (18.1, 7.4), (16, 6.5), (18.1, 5.6)], closed=True)),
        detail(seg(5.5, 15, 14.5, 15)),
    ]


@icon("lip-balm", CAT, "Round flat tin of lip balm seen from above with a pair of lips on the lid",
      tags=["chapstick", "lip care", "tin", "moisturizer", "lips", "cosmetics", "salve"])
def _(S):
    lips = poly([(6.5, 12), (9, 9.3), (12, 10.5), (15, 9.3), (17.5, 12), (15, 14.8), (9, 14.8)], closed=True, r=S.r)
    return [
        shell(circle(12, 12, 9)),
        detail(lips),
        detail(seg(6.5, 12, 17.5, 12)),
    ]


@icon("makeup-sponge", CAT, "Egg-shaped makeup blending sponge with a flat cut side and a few pores",
      tags=["beauty blender", "blending sponge", "foundation", "concealer", "cosmetics", "applicator", "dab"])
def _(S):
    if S.name == "line":
        body = "M12 2C8 2 5 8 5 13C5 16.5 6 18.5 7 20.5H17C18 18.5 19 16.5 19 13C19 8 16 2 12 2Z"
    else:
        body = "M12 2.5C7.5 2.5 5 8 5 13C5 16 5.8 18 7 19.3Q8 20.5 9.5 20.5H14.5Q16 20.5 17 19.3C18.2 18 19 16 19 13C19 8 16.5 2.5 12 2.5Z"
    return [
        shell(body),
        dot(10.5, 9, 1), dot(14, 11.5, 1), dot(10.5, 14.5, 1),
    ]


@icon("eyelash-curler", CAT, "Eyelash curler with a curved clamp at the top and scissor handles with finger loops",
      tags=["lash curler", "eyelashes", "curl", "eye makeup", "beauty tool", "cosmetics", "clamp"])
def _(S):
    return [
        line("M4 7C8 3.5 16 3.5 20 7"),
        line("M6.5 10.5C9.5 8.5 14.5 8.5 17.5 10.5"),
        line(seg(17.5, 10.5, 8.8, 17.3)),
        line(seg(6.5, 10.5, 15.2, 17.3)),
        shell(circle(7, 19.2, 2.2)),
        shell(circle(17, 19.2, 2.2)),
    ]


@icon("false-eyelashes", CAT, "Strip of false eyelashes with long curved lashes rising from a thin band",
      tags=["fake lashes", "lash strip", "eye makeup", "extensions", "cosmetics", "glam", "beauty"])
def _(S):
    out = [line("M3 16Q12 20 21 16")]
    tips = [(2.5, 8.5), (6.5, 5), (12, 3.5), (17.5, 5), (21.5, 8.5)]
    bases = [(4.2, 16.4), (8, 17.7), (12, 18), (16, 17.7), (19.8, 16.4)]
    for (bx, by), (tx, ty) in zip(bases, tips):
        cx = bx + (tx - bx) * 0.15
        cy = (by + ty) / 2
        out.append(line(f"M{fmt(bx)} {fmt(by)}Q{fmt(cx)} {fmt(cy)} {fmt(tx)} {fmt(ty)}"))
    return out


@icon("nail-lamp", CAT, "Dome-shaped nail curing lamp with a hand resting inside and light rays above it",
      tags=["uv lamp", "led lamp", "gel nails", "manicure", "curing", "nail salon", "dryer"])
def _(S):
    return [
        shell("M3 21V16A9 9 0 0 1 21 16V21Z"),
        detail(rect(8.5, 15, 7, 6, rr(S, 2))),
        detail(seg(12, 9.5, 12, 11.5)),
        detail(seg(8, 10.5, 9.2, 12)),
        detail(seg(16, 10.5, 14.8, 12)),
    ]


@icon("nail-polish-remover", CAT, "Round remover bottle with a pump dish on top and a cotton pad beside it",
      tags=["acetone", "manicure", "cotton pad", "nail care", "cleanser", "pump bottle", "beauty"])
def _(S):
    return [
        shell(rect(3.5, 12, 11, 9.5, rr(S, 3))),
        line(seg(9, 8, 9, 12)),
        shell(poly([(3.5, 4.5), (5, 8), (13, 8), (14.5, 4.5)], closed=True, r=S.r * 0.6)),
        shell(circle(19, 17, 3)),
    ]


@icon("makeup-bag", CAT, "Soft zippered pouch with a lipstick sticking out of the top",
      tags=["cosmetic bag", "toiletry pouch", "zip", "travel", "purse", "beauty", "lipstick"])
def _(S):
    body = union(rect(3, 9, 18, 12, rr(S, 4)), poly([(12.5, 10), (12.5, 5.5), (17.5, 2.5), (17.5, 10)], closed=True))
    return [
        shell(body),
        detail(seg(3, 13.5, 21, 13.5)),
        detail(seg(12.5, 6.5, 17.5, 6.5)),
        mark(circle(8, 17.5, 1.2)),
    ]


@icon("makeup-organizer", CAT, "Stepped makeup organizer with lipsticks standing in a tray and a drawer below",
      tags=["cosmetic organizer", "vanity", "storage", "lipstick holder", "acrylic", "drawers", "dresser"])
def _(S):
    return [
        line(seg(7, 9, 7, 3)),
        line(seg(12, 9, 12, 3)),
        line(seg(17, 9, 17, 3)),
        shell(rect(3.5, 9, 17, 4.5, L(S, 0.5, 2))),
        shell(rect(3.5, 13.5, 17, 8, rr(S, 2.5))),
        mark(circle(12, 17.5, 1.3)),
    ]


@icon("vanity-case", CAT, "Boxy hard-sided train case with a top handle, a center latch and a mirror band",
      tags=["train case", "cosmetic case", "beauty box", "travel makeup", "suitcase", "toiletry", "salon kit"])
def _(S):
    return [
        line(poly([(8.5, 8), (8.5, 4.5), (15.5, 4.5), (15.5, 8)], r=S.r)),
        shell(rect(3, 8, 18, 13, rr(S, 3))),
        detail(seg(3, 13, 21, 13)),
        detail(ellipse(12, 17, 2.5, 1.6)),
    ]


@icon("serum", CAT, "Slim bottle with a squeeze dropper on top and a single drop beside it",
      tags=["skin care", "dropper bottle", "facial oil", "essence", "vitamin c", "beauty", "pipette"])
def _(S):
    drop = "M19 6.5C19 6.5 16.6 9.6 16.6 11.3A2.4 2.4 0 0 0 21.4 11.3C21.4 9.6 19 6.5 19 6.5Z"
    return [
        shell(rect(4.5, 11, 10, 11, rr(S, 3))),
        shell(rect(7, 8, 5, 3, 0.3)),
        shell(rect(7.5, 2, 4, 6, L(S, 1, 2))),
        detail(seg(4.5, 16, 14.5, 16)),
        solid(drop),
    ]


@icon("sheet-mask", CAT, "Face-shaped sheet mask with cut-outs for the eyes and mouth",
      tags=["face mask", "facial", "skin care", "spa", "self care", "hydrating", "beauty"])
def _(S):
    eye = lambda cx: poly([(cx - 2.2, 10), (cx, 8.9), (cx + 2.2, 10), (cx, 11.1)], closed=True, r=S.r * 0.5)
    return [
        shell("M12 2.5C7 2.5 4.5 6 4.5 11.5C4.5 17 8 21.5 12 21.5C16 21.5 19.5 17 19.5 11.5C19.5 6 17 2.5 12 2.5Z"),
        mark(eye(8.5)), mark(eye(15.5)),
        mark(poly([(9.8, 16), (12, 15), (14.2, 16), (12, 17.5)], closed=True, r=S.r * 0.6)),
    ]


@icon("cleansing-brush", CAT, "Electric facial cleansing brush with a fan of bristles on a round plate and a handle",
      tags=["face brush", "skin care", "sonic", "exfoliating", "facial cleanser", "spa", "pore"])
def _(S):
    return [
        line(seg(6.5, 6, 7.5, 10.5)), line(seg(10.5, 3.5, 10.5, 10.5)), line(seg(14, 3.5, 14, 10.5)), line(seg(17.5, 6, 16.5, 10.5)),
        shell(rect(4, 10.5, 16, 3, L(S, 0.5, 1.5))),
        shell(rect(9, 13.5, 6, 8.5, rr(S, 3))),
        mark(circle(12, 17.5, 1)),
    ]


@icon("perfume-atomizer", CAT, "Vintage perfume bottle with a tube running to a squeeze bulb and a fine mist at the collar",
      tags=["perfume bottle", "spray bulb", "fragrance", "scent", "cologne", "vintage", "vanity"])
def _(S):
    return [
        shell(rect(3.5, 12.5, 12, 9.5, rr(S, 4))),
        shell(rect(7, 9.5, 5, 3, 0.3)),
        line(poly([(9.5, 9.5), (9.5, 5), (14, 5)], r=S.r)),
        shell(ellipse(17.5, 5, 3, 2.4)),
        dot(4.2, 8.5, 1), dot(2.8, 11, 0.9),
    ]


@icon("wax-warmer", CAT, "Small round wax pot heater with a wooden spatula dipped into the melted wax",
      tags=["waxing", "hair removal", "depilatory", "spa", "wax heater", "melting pot", "salon"])
def _(S):
    return [
        shell("M3.5 10H19.5V13A6.5 6.5 0 0 1 13 19.5H10A6.5 6.5 0 0 1 3.5 13Z"),
        line(seg(21, 2.5, 11, 12.5)),
        detail(seg(3.5, 10, 19.5, 10)),
    ]


@icon("wax-strip", CAT, "Rectangular wax strip with its lower corner peeled back and a few hairs caught in it",
      tags=["waxing", "hair removal", "depilatory", "peel", "strip", "spa", "smooth skin"])
def _(S):
    return [
        shell("M6 3H18V13L11 20H6Z"),
        detail(poly([(11, 13), (11, 20), (18, 13), (11, 13)], closed=False)),
        detail("M9.5 7C10 6 10.5 7 11 6"),
    ]


@icon("epilator", CAT, "Handheld epilator with a wide rounded head of tweezer discs and a slim handle",
      tags=["hair removal", "tweezer", "depilator", "shaver", "grooming", "legs", "electric"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 7, rr(S, 3))),
        dot(8.5, 6, 1.1), dot(12, 6, 1.1), dot(15.5, 6, 1.1),
        shell(rect(8.5, 9.5, 7, 12.5, rr(S, 3))),
        sq(11, 13, 2, 3.5, 1),
    ]


@icon("henna-cone", CAT, "Henna applicator cone with a rolled top edge and a floral swirl piped from its tip",
      tags=["mehndi", "mehendi", "paste cone", "body art", "wedding", "temporary tattoo", "design"])
def _(S):
    return [
        shell(poly([(9, 20), (4, 3.5), (14.5, 3.5)], closed=True, r=S.r)),
        detail(seg(5.5, 8, 13, 8)),
        line("M9.5 21.5C13 21.5 13 18.5 16 18.5C19 18.5 19 21.5 17 21.5C15.5 21.5 15.5 20 16.5 20"),
    ]


@icon("kohl-pot", CAT, "Small round kohl pot with a narrow neck and a thin applicator stick resting in it",
      tags=["kajal", "surma", "eyeliner", "eye makeup", "traditional cosmetics", "applicator", "kohl"])
def _(S):
    return [
        shell("M9 9.5C5 10.5 3.5 13 3.5 15.8C3.5 19.5 7.5 21.5 12 21.5C16.5 21.5 20.5 19.5 20.5 15.8C20.5 13 19 10.5 15 9.5Z"),
        shell(rect(9, 6.5, 6, 3.3, L(S, 0.3, 1.2))),
        line(seg(11.5, 7.5, 18.5, 1.8)),
    ]


# ============================================================================ laundry care and garment care

@icon("care-permanent-press-wash", CAT, "Laundry care symbol: a washtub with a wave of water and one bar underneath",
      tags=["laundry symbol", "care label", "permanent press", "wash", "washing instructions", "machine wash", "textile care"])
def _(S):
    return [
        shell(poly([(3, 4.5), (21, 4.5), (18, 16), (6, 16)], closed=True, r=S.r)),
        detail("M6.5 10C8.5 8.2 10 11.8 12 10C14 8.2 15.5 11.8 17.5 10"),
        line(seg(5, 20, 19, 20)),
    ]


@icon("care-tumble-dry-medium", CAT, "Laundry care symbol: a square holding a circle with two dots for medium heat tumble drying",
      tags=["laundry symbol", "care label", "tumble dry", "dryer", "medium heat", "drying instructions", "textile care"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        detail(circle(12, 12, 5.8)),
        dot(9.6, 12, 1.2), dot(14.4, 12, 1.2),
    ]


@icon("care-dry-clean-gentle", CAT, "Laundry care symbol: an open circle with one bar underneath for gentle dry cleaning",
      tags=["laundry symbol", "care label", "dry clean", "gentle", "professional cleaning", "delicate", "textile care"])
def _(S):
    return [
        shell(circle(12, 10, 7.5)),
        line(seg(6, 20, 18, 20)),
    ]


@icon("dishwasher-tablet", CAT, "Block-shaped two-layer dishwasher tablet seen in perspective with a small ball pressed into its top",
      tags=["dishwasher pod", "detergent", "dish soap", "cleaning", "kitchen", "capsule", "tab"])
def _(S):
    body = union(poly([(6, 6.5), (21, 6.5), (18, 10.5), (3, 10.5)], closed=True), rect(3, 10.5, 15, 10.5, rr(S, 1.5)),
                 poly([(18, 10.5), (21, 6.5), (21, 17), (18, 21)], closed=True))
    return [
        shell(body),
        detail(poly([(3, 15.8), (18, 15.8), (21, 11.8)])),
        mark(circle(11.5, 8.5, 1.4)),
    ]


@icon("stained-shirt", CAT, "T-shirt with a round splotch stain and a drip running down its front",
      tags=["stain", "dirty clothes", "spill", "laundry", "stain remover", "spot", "soiled"])
def _(S):
    return [
        shell(poly([(8, 3), (3, 6), (5, 10), (7, 9), (7, 21), (17, 21), (17, 9), (19, 10), (21, 6), (16, 3)], closed=True, r=S.r)),
        detail("M8 3a4 4 0 0 0 8 0"),
        mark("M10.5 10C12 9 14.5 9.5 15 11.5C16 12.5 15.5 14.5 13.8 14.8C12.5 15.5 10.5 15 10 13.3C9 12.5 9.3 10.8 10.5 10Z"),
        mark(circle(12.4, 17.6, 1.1)),
    ]


@icon("trouser-press", CAT, "Upright trouser press panel with a pair of pants hanging flat inside it",
      tags=["pants press", "trousers", "creases", "wrinkles", "garment care", "hotel", "ironing"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 3))),
        detail(poly([(8, 6), (16, 6), (16, 19), (12.8, 19), (12, 11), (11.2, 19), (8, 19)], closed=True)),
    ]


@icon("clip-drying-hanger", CAT, "Round drying hanger with a hook on top and pegs dangling from its ring",
      tags=["sock dryer", "laundry", "clothes pegs", "clips", "air dry", "circular hanger", "clothesline"])
def _(S):
    out = [
        line("M12 5V3.8A1.9 1.9 0 1 1 13.9 5.7"),
        shell(circle(12, 9.5, 4.5)),
    ]
    for a in (30, 70, 110, 150):
        x, y = polar(12, 9.5, 5.5, a)
        out.append(line(seg(x, y, x, y + 4.5)))
        out.append(sq(x - 1.3, y + 4.6, 2.6, 2.6, 0.6))
    return out


@icon("garment-bag", CAT, "Long zippered garment bag with a hanger hook poking out of the top",
      tags=["suit bag", "dress cover", "clothes cover", "travel", "hanging bag", "wardrobe", "storage"])
def _(S):
    return [
        line("M12 7V4.2A2 2 0 1 1 14 6.2"),
        shell(rect(6, 7, 12, 15, rr(S, 3))),
        detail(seg(12, 11, 12, 20)),
        sq(10.8, 8.8, 2.4, 2.4, 0.5),
    ]


# ============================================================================ grooming tools and bathing

@icon("nit-comb", CAT, "Metal lice comb with a short handle and a row of long, fine teeth",
      tags=["lice comb", "head lice", "nits", "fine tooth comb", "pest", "school", "hair check"])
def _(S):
    out = [
        shell(rect(2.5, 9.5, 6.5, 5, rr(S, 2.5))),
        shell(rect(9, 3, 3, 18, L(S, 0.8, 1.5))),
    ]
    for y in (4.5, 8, 11.5, 15, 18.5):
        out.append(line(seg(12, y, 21.5, y)))
    return out


@icon("ear-pick", CAT, "Slim ear pick stick with a tiny scoop at one end and a soft cotton tuft at the other",
      tags=["earwax", "ear cleaner", "ear spoon", "grooming", "hygiene", "cotton tuft", "ear care"])
def _(S):
    return [
        line(seg(6.8, 17.2, 14.5, 9.5)),
        shell(rotd(ellipse(4.6, 19.4, L(S, 3.6, 3.3), L(S, 1.6, 2)), -45, 4.6, 19.4)),
        shell(circle(17.5, 6.5, L(S, 3, 3.3))),
    ]


@icon("henna-hand", CAT, "Open hand with a floral henna pattern of a flower and dots across the palm",
      tags=["mehndi", "mehendi", "hand art", "body art", "wedding", "bridal", "temporary tattoo"])
def _(S):
    return [
        shell(rect(6, 11, 12.5, 10.5, rr(S, 3.5))),
        line(seg(7.6, 11, 7.6, 5)),
        line(seg(11, 11, 11, 3)),
        line(seg(14.4, 11, 14.4, 3.8)),
        line(seg(17.4, 11, 17.4, 6.5)),
        line(seg(6, 15, 3, 10.5)),
        detail(circle(12.2, 16, 1.6)),
        mark(circle(8.6, 14, 0.9)), mark(circle(15.8, 14, 0.9)), mark(circle(8.6, 18.4, 0.9)), mark(circle(15.8, 18.4, 0.9)),
    ]


@icon("hammam-bowl", CAT, "Shallow metal bath bowl with a pouring lip and an embossed zigzag band",
      tags=["hammam", "turkish bath", "bath bowl", "tas", "water scoop", "spa", "rinse bowl"])
def _(S):
    return [
        shell("M3 8.5H19L22 6L21 10C20 15.5 16.5 18.5 11.5 18.5C6.5 18.5 3 15 3 8.5Z"),
        detail(poly([(7.5, 11.5), (9.5, 14), (11.5, 11.5), (13.5, 14), (15.5, 11.5)], r=S.r * 0.4)),
        line(seg(8, 21.5, 15, 21.5)),
    ]


@icon("wooden-soaking-tub", CAT, "Deep square wooden tub of vertical planks with steam rising above the water",
      tags=["ofuro", "hot tub", "japanese bath", "hinoki", "onsen", "spa", "barrel bath"])
def _(S):
    return [
        shell(rect(3.5, 10, 17, 11.5, rr(S, 2.5))),
        detail(seg(8, 10, 8, 21.5)), detail(seg(12, 10, 12, 21.5)), detail(seg(16, 10, 16, 21.5)),
        line("M8 7C6.8 5.5 9.2 4.5 8 2.5"),
        line("M12 7C10.8 5.5 13.2 4.5 12 2.5"),
        line("M16 7C14.8 5.5 17.2 4.5 16 2.5"),
    ]


@icon("bath-bucket-and-mug", CAT, "Bathing bucket full of water with a plastic mug with a handle resting at its rim",
      tags=["bathroom", "water bucket", "dipper", "scoop", "traditional bathing", "wash", "splash"])
def _(S):
    body = union(poly([(4, 11), (20, 11), (18, 21.5), (6, 21.5)], closed=True), rect(7.5, 3.5, 7, 7.5, rr(S, 1.5)))
    return [
        shell(body),
        line("M14.5 5.5H16.5A1.9 1.9 0 0 1 16.5 9.3H14.5"),
        detail("M6.5 16C8.5 14.5 10.5 17.5 12.5 16C14.5 14.5 16 17 17.5 16"),
    ]


@icon("toothbrush-case", CAT, "Pill-shaped travel case lying flat with a toothbrush showing through its clear lid",
      tags=["travel toothbrush", "oral care", "hygiene", "holder", "cover", "dental", "trip"])
def _(S):
    return [
        shell(rect(2.5, 7.5, 19, 9, 4.5)),
        detail(seg(14.5, 7.5, 14.5, 16.5)),
        detail(seg(6.5, 12, 17, 12)),
        mark(rect(16, 10.5, 3.2, 3, 0.5)),
    ]


@icon("sanitizer-stand", CAT, "Freestanding pole with a hand sanitizer dispenser on top and a drip tray below",
      tags=["hand sanitizer", "dispenser", "hygiene station", "gel pump", "covid", "clinic", "entrance"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 8, 6.5, rr(S, 2))),
        line(poly([(13.5, 5), (17.5, 5), (17.5, 7.5)], r=S.r)),
        line(seg(9.5, 9, 9.5, 21)),
        line(seg(5, 21.5, 14, 21.5)),
        shell(rect(14, 14, 7.5, 2.5, L(S, 0.5, 1.2))),
        line(seg(9.5, 15.3, 14, 15.3)),
        dot(17.5, 10.8, 1),
    ]


@icon("soap-bubbles", CAT, "Cluster of three round soap bubbles of different sizes, each with a shine mark",
      tags=["suds", "foam", "bubble", "bath", "lather", "washing", "cleaning"])
def _(S):
    return [
        shell(circle(9, 14.5, 6.5)),
        shell(circle(18, 8, 3.5)),
        shell(circle(18.5, 17.5, 2.5)),
        line(arc(9, 14.5, 3.6, 195, 255)),
        line(seg(17, 7, 17.4, 6.6)),
    ]


@icon("curly-hair", CAT, "A single lock of hair hanging from the scalp and winding down into tight springy spiral curls",
      tags=["curls", "ringlets", "coily", "spiral", "hair type", "texture", "hairstyle"])
def _(S):
    return [
        line(seg(6, 2.5, 18, 2.5)),
        line("M12 2.5V4C17.5 4 17.5 8.5 12 8.5C6.5 8.5 6.5 13 12 13C17.5 13 17.5 17.5 12 17.5C8.5 17.5 8 20.5 10.5 21.5"),
    ]
