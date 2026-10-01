"""TypeIcon Core: beauty (batch 002): nail, makeup, skin care, tattoo and piercing tools and treatments.

Objects use simple front or side views. Long tools are drawn upright and turned 45 degrees so the handle
points to the bottom-left. Faces share one head oval with the features kept to a few marks.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar, rotation, transform_path

CAT = "beauty"
TILT = 45


def L(S, a, b):
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


def rrect(x, y, w, h, rx=0.0, deg=TILT):
    """Rotated rounded rectangle approximated by a filleted polygon (rx is the fillet)."""
    return rp([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], r=rx, deg=deg)


def rdot(x, y, r=1.25, deg=TILT):
    (a, b), = rot([(x, y)], deg)
    return dot(a, b, r)


def drop(cx, cy, s=1.0):
    """Small droplet outline with its tip up."""
    return (f"M{fmt(cx)} {fmt(cy - 3.5 * s)}C{fmt(cx)} {fmt(cy - 3.5 * s)} {fmt(cx - 2.6 * s)} {fmt(cy)} "
            f"{fmt(cx - 2.6 * s)} {fmt(cy + 1.2 * s)}A{fmt(2.6 * s)} {fmt(2.6 * s)} 0 0 0 {fmt(cx + 2.6 * s)} {fmt(cy + 1.2 * s)}"
            f"C{fmt(cx + 2.6 * s)} {fmt(cy)} {fmt(cx)} {fmt(cy - 3.5 * s)} {fmt(cx)} {fmt(cy - 3.5 * s)}Z")


def rotd(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def bar(p, q, w, tip=0.0, r=0.0):
    """Closed polygon for a bar from p (back) to q (tip end), tapering over the last `tip` px to a point."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    nx, ny = -uy * w / 2, ux * w / 2
    a = (q[0] - ux * tip, q[1] - uy * tip)
    pts = [(p[0] + nx, p[1] + ny), (a[0] + nx, a[1] + ny), q, (a[0] - nx, a[1] - ny), (p[0] - nx, p[1] - ny)]
    if tip == 0:
        pts = [(p[0] + nx, p[1] + ny), (q[0] + nx, q[1] + ny), (q[0] - nx, q[1] - ny), (p[0] - nx, p[1] - ny)]
    return poly(pts, closed=True, r=r)


def solidpart(d):
    return Part("dot", d)


def scallop(cx, cy, R, n, ar, S):
    """Closed outline of n small arcs around a circle (a soft puff edge); Line has crisp joins, Rounded the same arcs."""
    pts = [polar(cx, cy, R, i * 360 / n - 90) for i in range(n)]
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(n):
        q = pts[(i + 1) % n]
        d += f"A{fmt(ar)} {fmt(ar)} 0 0 1 {fmt(q[0])} {fmt(q[1])}"
    return d + "Z"


def star(cx, cy, R, r, n=5):
    pts = []
    for i in range(2 * n):
        pts.append(polar(cx, cy, R if i % 2 == 0 else r, -90 + i * 180 / n))
    return pts


def head(S, cx=12, cy=12, rx=7, ry=9):
    return shell(ellipse(cx, cy, rx, ry))


def cap(S, v):
    return min(S.R, v)


# ============================================================================ nails and manicure

@icon("nail-stamper", CAT, "A square silicone stamper on a short handle beside a small metal plate with a dot pattern.",
      tags=["nail art", "stamping", "manicure", "stamper", "nail plate", "design transfer"])
def _(S):
    return [shell(rect(3, 3, 8, 8, S.R)), line(seg(7, 11, 7, 21)),
            shell(rect(15, 5, 6, 15, cap(S, 2.5))), dot(18, 10, 1.1), dot(18, 15, 1.1)]


@icon("cuticle-oil-pen", CAT, "A slim twist pen with a small brush tip and a droplet of oil beside it.",
      tags=["cuticle", "oil", "nail care", "pen", "manicure", "twist pen"])
def _(S):
    return [shell(rrect(9, 10, 6, 11, S.r * 0.6)), shell(rp([(10, 10), (14, 10), (13, 5), (11, 5)], r=S.r * 0.4)),
            detail(rseg(9, 17, 15, 17)), shell(drop(18, 18, 0.9))]


@icon("manicure-cushion", CAT, "A hand lying flat on a padded cushion with its fingers spread.",
      tags=["manicure", "hand rest", "pillow", "nail salon", "arm rest", "hand"])
def _(S):
    return [shell(rect(6, 3, 12, 10, L(S, 2, 4))), detail(seg(9, 3, 9, 7)), detail(seg(12, 3, 12, 7)),
            detail(seg(15, 3, 15, 7)), shell(rect(3, 17, 18, 4, 2))]


@icon("manicure-set", CAT, "An open zip case holding a nail file, scissors and clippers.",
      tags=["manicure", "kit", "nail care", "grooming", "case", "pedicure set"])
def _(S):
    return [shell(rect(3, 4, 18, 16, S.R)), detail(seg(7, 9, 7, 16)), detail(seg(10.5, 9, 13.5, 16)),
            detail(seg(13.5, 9, 10.5, 16)), detail(seg(17, 9, 17, 16))]


@icon("orange-wood-stick", CAT, "A slim wooden stick with a slanted chisel end and a tapered point.",
      tags=["cuticle pusher", "manicure", "nail care", "stick", "wood", "orangewood"])
def _(S):
    return [shell(rp([(10, 6), (14, 3), (14, 17), (12, 21), (10, 17)], r=S.r)), detail(rseg(12, 9, 12, 15))]


@icon("broken-nail", CAT, "A fingertip whose nail has a jagged crack across it.",
      tags=["nail damage", "cracked nail", "split nail", "manicure repair", "fingernail", "injury"])
def _(S):
    return [shell("M4 21V11a8 8 0 0 1 16 0V21"), detail(rect(8, 5.5, 8, 9, cap(S, 2.5))),
            detail(poly([(8, 11.5), (10.5, 9), (13, 12.5), (16, 9.5)], r=S.r * 0.4))]


@icon("nail-brush", CAT, "A small scrubbing brush with stiff bristles along both long sides.",
      tags=["nail care", "scrubbing", "hygiene", "hand wash", "bristles", "cleaning"])
def _(S):
    out = [shell(rect(3, 9, 18, 6, 3))]
    for x in (6, 10, 14, 18):
        out += [line(seg(x, 4, x, 9)), line(seg(x, 15, x, 20))]
    return out


@icon("paraffin-wax-bath", CAT, "A warm wax tub with a hand dipped into it up to the wrist.",
      tags=["paraffin", "hand treatment", "spa", "warm wax", "dip", "moisturizing"])
def _(S):
    return [shell(rect(3, 11, 18, 10, cap(S, 3))), shell(rect(8, 2, 8, 13, 4)), detail("M4 18Q7 16 10 18T16 18T20 18")]


# ============================================================================ makeup

LIPS = "M3 17L6.5 14.5L9.5 15.8L12.5 14.5L16 17L9.5 21Z"


@icon("lip-liner", CAT, "A slim cosmetic pencil with its sharpened tip pointing at a pair of lips.",
      tags=["lip pencil", "makeup", "lips", "cosmetics", "contour", "pencil"])
def _(S):
    lips = L(S, "M3 17L5.5 14.5L8 15.5L10.5 14.5L13 17L8 21Z", "M3 17Q5.5 14.5 8 15.5Q10.5 14.5 13 17Q8 22 3 17Z")
    return [shell(bar((21, 3), (12, 12), 4, 3.5, S.r * 0.5)), shell(lips), detail(seg(3.8, 17, 12.2, 17))]


@icon("liquid-lipstick", CAT, "A slim lip colour tube standing beside its wand with a slanted flat applicator tip.",
      tags=["lip gloss", "lip colour", "makeup", "cosmetics", "wand", "applicator", "lip stain"])
def _(S):
    return [shell(poly([(5, 3.5), (8.5, 2.5), (9.5, 6.5), (6.5, 8)], closed=True, r=S.r * 0.4)),
            line(seg(7.5, 8, 7.5, 12)), shell(rect(5, 12, 5, 9, cap(S, 2))),
            shell(rect(14, 7, 7, 14, cap(S, 2.5))), detail(seg(14, 11, 21, 11))]


@icon("face-contouring", CAT, "A face with short shading strokes under the cheekbones, along the jaw and at the temples.",
      tags=["contour", "makeup", "cheekbones", "bronzer", "sculpt", "shading", "highlight"])
def _(S):
    return [head(S), dot(9.5, 9, 1.1), dot(14.5, 9, 1.1),
            detail(seg(8.5, 12.5, 10.5, 15)), detail(seg(15.5, 12.5, 13.5, 15)),
            detail(seg(8.5, 16, 10.5, 18.5)), detail(seg(15.5, 16, 13.5, 18.5))]


@icon("setting-spray", CAT, "A slim pump mist bottle spraying a fan of fine dots to the right.",
      tags=["makeup", "mist", "fixing spray", "face spray", "finishing spray", "spritz", "cosmetics"])
def _(S):
    return [shell(rect(3, 11, 7, 10, cap(S, 2.5))), shell(rect(5, 6, 3, 5)), line(seg(8, 5, 11, 5)),
            dot(14.5, 5, 1.1), dot(18, 3.5, 1.1), dot(17, 8, 1.1), dot(21, 7, 1.1), dot(14.5, 9, 1.1)]


@icon("loose-powder", CAT, "A round powder jar with a perforated sifter lid sitting on top.",
      tags=["face powder", "makeup", "setting powder", "sifter", "translucent powder", "cosmetics"])
def _(S):
    return [shell(rect(5, 4, 14, 5, cap(S, 2))), dot(9, 6.5, 0.9), dot(12, 6.5, 0.9), dot(15, 6.5, 0.9),
            shell(rect(4, 13, 16, 8, cap(S, 3)))]


@icon("powder-puff", CAT, "A soft round makeup puff with a ribbon strap arched across its back.",
      tags=["makeup", "puff", "powder", "cosmetics", "applicator", "velour", "face powder"])
def _(S):
    return [shell(scallop(12, 12, 8.2, 8, 3.4, S)), detail("M8 13.5Q12 9 16 13.5")]


@icon("kabuki-brush", CAT, "A short makeup brush with a dense dome of bristles on a stubby handle.",
      tags=["makeup brush", "foundation brush", "buffing brush", "bristles", "cosmetics", "blush"])
def _(S):
    return [shell("M5 12C5 2 19 2 19 12Z"), detail(seg(9, 6, 9, 9)), detail(seg(12, 5, 12, 9)), detail(seg(15, 6, 15, 9)),
            shell(poly([(10, 15), (14, 15), (14.5, 21), (9.5, 21)], closed=True, r=S.r * 0.5))]


@icon("angled-brow-brush", CAT, "A thin makeup brush with a slanted bristle tip beside an eyebrow stroke.",
      tags=["eyebrow", "brow", "makeup brush", "cosmetics", "brow brush", "liner brush", "grooming"])
def _(S):
    body = rp([(10, 3), (14, 5), (14, 10), (13, 12), (13, 21), (11, 21), (11, 12), (10, 10)], r=S.r * 0.4)
    return [shell(body), line("M13 20.5C16 17 19 17 21.5 18")]


@icon("brow-stencil", CAT, "A small plastic card with an eyebrow shaped cutout in the middle.",
      tags=["eyebrow", "brow", "template", "shaping", "makeup", "grooming", "guide"])
def _(S):
    return [shell(rect(3, 5, 18, 14, S.R)),
            solidpart("M6 14.5C8 11 13 9 18 10C14 11 10 12.5 8 15.5Z")]


@icon("face-chart", CAT, "A sheet of paper with a blank face outline and colour swatches below.",
      tags=["makeup", "template", "planning", "makeup artist", "worksheet", "look", "cosmetics"])
def _(S):
    return [shell(rect(4, 2, 16, 20, cap(S, 2.5))), detail(ellipse(12, 9.5, 3.5, 4.5)),
            dot(8, 18, 1.2), dot(12, 18, 1.2), dot(16, 18, 1.2)]


@icon("brush-cleaning-mat", CAT, "A rounded silicone pad covered in rows of ridges for scrubbing makeup brushes.",
      tags=["makeup brush", "cleaning", "silicone", "mat", "washing", "brush care", "hygiene"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R + 1)), detail("M6 8Q8 6 10 8T14 8T18 8"), detail("M6 12Q8 10 10 12T14 12T18 12"),
            detail("M6 16Q8 14 10 16T14 16T18 16")]


@icon("makeup-brush-holder", CAT, "A cup holding three makeup brushes of different sizes standing upright.",
      tags=["makeup brushes", "organizer", "cup", "vanity", "cosmetics", "storage", "brush holder"])
def _(S):
    return [shell(poly([(4, 13), (20, 13), (18, 21), (6, 21)], closed=True, r=S.r)),
            line(seg(6, 13, 6, 9)), shell(ellipse(6, 6, 1.5, 3)),
            line(seg(12, 13, 12, 7)), shell(ellipse(12, 4, 1.5, 2.5)),
            line(seg(18, 13, 18, 9)), shell(ellipse(18, 6, 1.5, 3))]


@icon("winged-eyeliner", CAT, "An open eye with a bold liner line along the upper lid that flicks up past the outer corner.",
      tags=["eyeliner", "cat eye", "makeup", "eye", "flick", "liner", "cosmetics"])
def _(S):
    eye = L(S, "M3 14Q11 6 19 12Q11 19 3 14Z", "M3 14Q11 6 19 12Q11 19 3 14Z")
    return [shell(eye), dot(11, 12.5, 2), line("M3 14Q11 6 19 12L21.5 8.5")]


@icon("beauty-mark", CAT, "A face with a single small dark dot above one corner of the mouth.",
      tags=["mole", "birthmark", "skin", "face", "cosmetic", "freckle", "beauty spot"])
def _(S):
    return [head(S), dot(9.5, 9.5, 1.1), dot(14.5, 9.5, 1.1), detail(seg(10, 17, 13, 17)), dot(16.5, 14.5, 1.3)]


@icon("eyeshadow-applicator", CAT, "A short double ended stick with an oval sponge tip at each end.",
      tags=["eyeshadow", "makeup", "sponge", "applicator", "eye makeup", "cosmetics", "blending"])
def _(S):
    t1 = L(S, rect(9.5, 1.5, 5, 7, 0.8), ellipse(12, 5, 2.5, 3.5))
    t2 = L(S, rect(9.5, 15.5, 5, 7, 0.8), ellipse(12, 19, 2.5, 3.5))
    return [shell(rotd(t1, 45)), line(rseg(12, 8.5, 12, 15.5)), shell(rotd(t2, 45))]


@icon("foundation-shade-swatches", CAT, "Three stripes of makeup from light to deep, with a droplet beside them.",
      tags=["foundation", "shade match", "skin tone", "swatch", "makeup", "complexion", "colour match"])
def _(S):
    k = L(S, 0.5, 1.5)
    return [shell(rect(3, 3, 12, 3, k)), shell(rect(3, 10, 12, 3, k)), solidpart(rect(2, 16, 14, 5, k + 1)),
            shell(drop(19, 12, 0.8))]


# ============================================================================ skin care

@icon("toner-bottle", CAT, "A tall slim cosmetic bottle with a screw cap beside a cotton pad catching a drop.",
      tags=["toner", "skin care", "cleansing", "astringent", "cotton pad", "face", "lotion"])
def _(S):
    return [shell(rect(4, 8, 6, 13, cap(S, 2.5))), shell(rect(5, 3, 4, 3)),
            shell(drop(17, 8.5, 0.8)), shell(circle(17, 17, 4))]


@icon("facial-cleanser", CAT, "A squeeze tube with a flip cap beside a mound of foam bubbles.",
      tags=["face wash", "cleanser", "foam", "skin care", "soap", "tube", "bubbles"])
def _(S):
    return [shell(poly([(3, 8), (11, 8), (10, 21), (4, 21)], closed=True, r=S.r)), shell(rect(5, 3, 4, 3)),
            shell(circle(16, 16, 4)), shell(circle(19.5, 9.5, 2.2)), shell(circle(14, 9, 1.4))]


@icon("clay-mask", CAT, "A face with a thick mask coating the forehead and chin, leaving the eyes and lips clear.",
      tags=["face mask", "mud mask", "skin care", "spa", "facial", "clay", "beauty treatment"])
def _(S):
    return [head(S), solidpart(ellipse(12, 6.2, 3.8, 1.5)), dot(9.5, 11, 1), dot(14.5, 11, 1),
            solidpart(ellipse(8.2, 15.5, 1.5, 2)), solidpart(ellipse(15.8, 15.5, 1.5, 2)),
            detail(seg(10.5, 15.5, 13.5, 15.5)), solidpart(ellipse(12, 19.2, 2.6, 1))]


@icon("peel-off-mask", CAT, "A face with a smooth mask coating and one cheek corner curling away as it is peeled.",
      tags=["face mask", "peel off", "skin care", "facial", "peeling", "beauty treatment", "gel mask"])
def _(S):
    return [head(S), dot(9, 9.5, 1), dot(14, 9.5, 1), detail(seg(9, 16, 13, 16)),
            shell(poly([(14, 13), (21, 9), (21.5, 16)], closed=True, r=S.r))]


@icon("eye-cream", CAT, "A small eye with an arc of cream below it and a tube with a ball tip pointing at it.",
      tags=["eye care", "under eye", "skin care", "dark circles", "roller ball", "serum", "anti aging"])
def _(S):
    return [shell("M3 7Q8 2 13 7Q8 12 3 7Z"), dot(8, 7, 1.4), line("M4 14.5Q7.5 16.5 11 14.5"),
            shell(bar((21, 21), (16, 16), 4, 0, S.r * 0.5)), shell(circle(14, 14, 1.6))]


@icon("pimple-patch", CAT, "A small sheet of round dot stickers with one peeled and lifted at an angle.",
      tags=["acne", "blemish", "spot", "zit", "hydrocolloid", "skin care", "sticker"])
def _(S):
    return [shell(rect(3, 4, 18, 16, S.R)), detail(circle(8, 9, 2)), detail(circle(16, 9, 2)),
            detail(circle(8, 15.5, 2)), detail(rotd(ellipse(16, 15.5, 2.4, 1.6), -30, 16, 15.5))]


@icon("ice-roller", CAT, "A handheld facial roller with a wide cylinder head on a short handle and frost sparkles.",
      tags=["face roller", "cold therapy", "puffiness", "skin care", "cooling", "facial massage", "cryo"])
def _(S):
    return [shell(rect(3, 3, 18, 7, cap(S, 3.5))), line(seg(12, 10, 12, 13)), shell(rect(9.5, 13, 5, 8, cap(S, 2))),
            line(seg(5.5, 14, 5.5, 18)), line(seg(3.5, 16, 7.5, 16)),
            line(seg(18.5, 14, 18.5, 18)), line(seg(16.5, 16, 20.5, 16))]


@icon("led-face-mask", CAT, "A rigid full face mask with eye openings and a grid of small lights across its surface.",
      tags=["light therapy", "led", "skin care", "red light", "beauty device", "facial", "anti aging"])
def _(S):
    return [head(S), detail(L(S, rect(7, 9.7, 3.6, 1.6), ellipse(8.8, 10.5, 1.8, 1.1))), detail(L(S, rect(13.4, 9.7, 3.6, 1.6), ellipse(15.2, 10.5, 1.8, 1.1))),
            dot(9, 5.5, 0.9), dot(15, 5.5, 0.9), dot(12, 6.5, 0.9), dot(8.5, 15, 0.9), dot(15.5, 15, 0.9),
            dot(12, 15.5, 0.9), dot(12, 19, 0.9)]


@icon("comedone-extractor", CAT, "A slim metal tool with a small loop at one end and a pointed lancet at the other.",
      tags=["blackhead remover", "pore", "skin care", "extractor", "acne tool", "esthetician", "lancet"])
def _(S):
    (cx, cy), = rot([(12, 5.5)])
    return [shell(circle(cx, cy, 3.2)), line(rseg(12, 8.7, 12, 16)),
            shell(rp([(10.3, 16), (13.7, 16), (12, 21)], r=S.r * 0.5))]


@icon("dermaplaning-blade", CAT, "A slim facial razor with a small flat blade head on a long thin handle.",
      tags=["dermaplaning", "facial razor", "peach fuzz", "exfoliation", "skin care", "shaving", "face shaver"])
def _(S):
    (a, b), = rot([(12, 9)])
    head_ = rotd(poly([(7.5, 3), (16.5, 3), (16.5, 9), (7.5, 9)], closed=True, r=S.r * 0.6), 30, 12, 9)
    slit = rotd(seg(9.5, 6, 14.5, 6), 30, 12, 9)
    return [shell(rotd(head_, TILT)), detail(rotd(slit, TILT)), line(rseg(12, 9, 12, 21))]


@icon("sample-sachet", CAT, "A small flat foil sachet with crimped edges and a droplet printed on its front.",
      tags=["sample", "foil packet", "single use", "skin care", "travel size", "trial", "cosmetic packet"])
def _(S):
    return [shell(rect(5, 2, 14, 20, L(S, 1, 3))), detail(poly([(5, 6), (7, 5), (9, 6), (11, 5), (13, 6), (15, 5), (17, 6), (19, 5)])),
            detail(drop(12, 13, 0.9))]


@icon("beauty-fridge", CAT, "A small fridge with its door open showing jars and a bottle on its shelves.",
      tags=["skin care fridge", "cosmetics", "cold storage", "mini fridge", "vanity", "serum storage", "cooling"])
def _(S):
    return [shell(rect(3, 4, 10, 16, cap(S, 2))), detail(seg(3, 11, 13, 11)),
            solidpart(rect(5.5, 6.5, 3, 2.5)), solidpart(rect(9.5, 5.5, 2, 3.5)), solidpart(rect(5.5, 13.5, 5, 3.5)),
            shell(poly([(16, 6), (21, 4), (21, 20), (16, 18)], closed=True, r=S.r * 0.5))]


@icon("hand-mask", CAT, "A hand wearing a moisture glove with a sealed wrist cuff.",
      tags=["glove mask", "hand care", "moisturizing", "skin care", "spa", "hydration", "hand treatment"])
def _(S):
    return [shell(rect(6, 3, 12, 10, L(S, 2, 4))), detail(seg(9, 3, 9, 7)), detail(seg(12, 3, 12, 7)), detail(seg(15, 3, 15, 7)),
            shell(rect(8, 16, 8, 4, 1.5)), line(seg(16, 18, 21, 18))]


@icon("foot-peel-mask", CAT, "A foot wearing a plastic bootie sealed at the ankle, with a peeled flake beside it.",
      tags=["foot mask", "exfoliating", "heel", "skin care", "pedicure", "bootie", "foot care"])
def _(S):
    return [shell(poly([(5, 3), (12, 3), (12, 12), (19, 14), (19, 21), (5, 21)], closed=True, r=S.r)),
            detail(seg(5, 8, 12, 8)), shell(poly([(16, 4), (21, 5), (18.5, 9)], closed=True, r=S.r * 0.4))]


# ============================================================================ skin concerns and treatments

@icon("double-chin", CAT, "A head in side profile with a soft extra fold of skin bulging under the jaw.",
      tags=["chin", "jaw", "profile", "fat", "face", "skin concern", "neck"])
def _(S):
    return [shell("M9 3C14 2.5 17.5 5.5 17.5 9.5L19.5 13L17.5 14V16C17.5 18.5 14.5 19.5 11.5 18.5L10 21H6V12C6 6 7 3.5 9 3Z"),
            dot(13.5, 8.5, 1.1), detail("M11.5 14.5Q14 14.5 15.5 16")]


@icon("cellulite", CAT, "A thigh and hip outline covered with small dimples.",
      tags=["dimples", "skin texture", "thigh", "body care", "skin concern", "orange peel", "body contouring"])
def _(S):
    return [shell(poly([(6, 3), (17, 3), (18, 11), (16, 21), (8, 21), (8, 12)], closed=True, r=S.r * 1.5)),
            dot(11, 7, 1), dot(14, 8, 1), dot(11.5, 11.5, 1), dot(14.5, 13, 1), dot(11.5, 16.5, 1)]


@icon("ingrown-hair", CAT, "A cross section of skin with a hair curling back down into the skin under a small bump.",
      tags=["hair", "skin", "razor bump", "shaving", "follicle", "skin concern", "waxing"])
def _(S):
    return [line("M2 10H8Q12 4 16 10H22"), line("M8 21C8 13 16 13 16 17C16 20 12 19.5 12 17")]


@icon("blackheads", CAT, "A nose in front view with several small dark dots across its tip and sides.",
      tags=["pores", "acne", "nose", "skin concern", "comedones", "clogged pores", "skin care"])
def _(S):
    return [shell(poly([(10, 3), (7.5, 14), (6, 17), (8, 20), (12, 18.5), (16, 20), (18, 17), (16.5, 14), (14, 3)],
                       closed=True, r=S.r * 1.2)),
            dot(10.5, 11, 1), dot(13.5, 11, 1), dot(12, 14.5, 1), dot(9.2, 16.5, 1), dot(14.8, 16.5, 1)]


@icon("chemical-peel", CAT, "A face with a flat fan brush painting a smooth layer across one cheek.",
      tags=["peel", "exfoliation", "acid", "facial", "skin care", "dermatology", "spa treatment"])
def _(S):
    return [head(S, 9, 12, 6.5, 8.5), dot(7, 10, 1), detail(seg(6.5, 17, 9.5, 17)),
            line(seg(21, 3, 18, 6)), shell(poly([(17, 6), (20, 9), (16, 13), (12.5, 9.5)], closed=True, r=S.r * 0.6))]


@icon("cosmetic-injection", CAT, "A face with a small syringe held at the forehead between the brows.",
      tags=["botox", "filler", "injection", "aesthetic", "wrinkle treatment", "syringe", "dermatology"])
def _(S):
    return [head(S, 10, 13, 6.5, 8.5), dot(7.5, 13, 1), dot(12.5, 13, 1),
            shell(bar((21, 3), (16, 8), 4, 0, S.r * 0.4)), line(seg(16, 8, 11.5, 10.5)),
            line(seg(19, 1.5, 22, 4.5))]


@icon("spray-tan", CAT, "A standing body silhouette beside a spray gun sending a fan of fine mist dots.",
      tags=["tanning", "bronzing", "sunless tan", "booth", "body care", "airbrush", "salon"])
def _(S):
    return [shell(circle(6.5, 5, 2.5)), shell(rect(3.5, 9, 6, 12, cap(S, 3))),
            shell(rect(17, 3, 5, 4, 1.5)), dot(14.5, 6.5, 1), dot(13.5, 10, 1), dot(16.5, 10.5, 1),
            dot(14.5, 14, 1), dot(18, 14, 1)]


@icon("mud-bath", CAT, "A tub of thick mud with a few bubbles and a head and shoulders resting above the surface.",
      tags=["spa", "mud", "treatment", "wellness", "relax", "soak", "body treatment"])
def _(S):
    return [shell(rect(3, 14, 18, 7, cap(S, 3))), shell(circle(12, 5.5, 2.5)), line("M6.5 13C6.5 8 17.5 8 17.5 13"),
            dot(8, 17.5, 1), dot(12, 18, 1), dot(16, 17.5, 1)]


@icon("body-wrap-treatment", CAT, "A person lying down with the body wrapped in bands from chest to ankles and the head free.",
      tags=["spa", "wrap", "body treatment", "detox", "slimming", "wellness", "massage"])
def _(S):
    return [shell(circle(5, 12, 2.5)), shell(rect(10, 9, 11, 6, L(S, 1.5, 3))), detail(seg(13.5, 9, 13.5, 15)), detail(seg(17.5, 9, 17.5, 15))]


@icon("ear-candling", CAT, "An ear with a tall thin hollow candle standing in it and a small flame on top.",
      tags=["ear", "hopi", "wellness", "alternative", "candle", "therapy", "ear care"])
def _(S):
    return [line("M3 10C3 3 12 3 12 9C12 12 9 13 9 16C9 20 5 20 5 16"), shell(poly([(13, 20), (13, 10), (20, 10), (20, 20)], closed=True, r=S.r * 0.5)),
            shell(drop(16.5, 5.5, 0.5))]


@icon("facial-massage", CAT, "A face with a hand pressing on each cheek.",
      tags=["massage", "spa", "facial", "skin care", "gua sha", "cheeks", "relaxation"])
def _(S):
    return [head(S, 12, 12, 4.5, 8), shell(rect(1.5, 10, 3, 7, 1.5)), shell(rect(19.5, 10, 3, 7, 1.5)),
            dot(10.5, 10, 0.9), dot(13.5, 10, 0.9), detail(seg(11, 15, 13, 15))]


@icon("tattoo-removal", CAT, "A forearm with a faded star tattoo and a laser handpiece above it firing short rays.",
      tags=["laser", "removal", "skin", "ink", "dermatology", "fade", "clinic"])
def _(S):
    return [shell(rect(2.5, 13, 19, 7, 3.5)), solidpart(poly(star(12, 16.5, 2.8, 1.2), closed=True)),
            shell(rect(9, 2, 6, 4, 1.5)), line(seg(12, 6, 12, 8)), dot(12, 10.5, 0.8), line(seg(8, 8, 9, 9)), line(seg(16, 8, 15, 9))]


# ============================================================================ tattoo

@icon("rotary-tattoo-pen", CAT, "A slim pen style tattoo machine with a tapered needle tip, a grip band and a cord at the back.",
      tags=["tattoo machine", "ink", "tattoo artist", "studio", "pen", "needle", "body art"])
def _(S):
    return [shell(rp([(10.5, 8), (13.5, 8), (12.7, 3.5), (11.3, 3.5)], r=S.r * 0.3)), shell(rrect(8.5, 8, 7, 9, S.r * 0.6)),
            detail(rseg(8.5, 12, 15.5, 12)), line(rotd("M12 17V18.5Q12 20 14 20", TILT))]


@icon("tattoo-needle-cartridge", CAT, "A short clear cylinder with a membrane band and a needle poking out of its tapered tip.",
      tags=["needle", "cartridge", "tattoo machine", "ink", "tattoo supplies", "studio", "disposable"])
def _(S):
    return [shell(poly([(8, 2.5), (16, 2.5), (16, 12), (13.5, 17), (10.5, 17), (8, 12)], closed=True, r=S.r)),
            detail(seg(8, 7, 16, 7)), line(seg(12, 17, 12, 22))]


@icon("tattoo-ink-caps", CAT, "A row of three small cone shaped ink cups on a tray.",
      tags=["ink cups", "pigment", "tattoo artist", "supplies", "studio", "paint", "caps"])
def _(S):
    cups = [shell(poly([(c - 2, 5), (c + 2, 5), (c + 1.2, 14.5), (c - 1.2, 14.5)], closed=True)) for c in (5, 12, 19)]
    return cups + [shell(rect(2, 16.5, 20, 4, L(S, 1, 2)))]


@icon("tattoo-ink-bottle", CAT, "A small bottle with a pointed dispensing cap and a drop of ink falling beside it.",
      tags=["ink", "pigment", "tattoo", "bottle", "supplies", "studio", "body art"])
def _(S):
    return [shell(rect(3, 11, 11, 10, cap(S, 2.5))), shell(poly([(6.5, 11), (6.5, 7), (8.5, 3), (10.5, 7), (10.5, 11)], closed=True, r=S.r * 0.4)),
            shell(drop(18.5, 14, 1.0))]


@icon("tattoo-stencil", CAT, "A sheet of transfer paper with a simple line design and its corner lifting to show the skin.",
      tags=["transfer", "stencil", "tattoo design", "thermal paper", "outline", "template", "tracing"])
def _(S):
    return [shell(poly([(3, 3), (21, 3), (21, 13), (13, 21), (3, 21)], closed=True, r=S.r)),
            detail("M6 10Q8.5 6 11 10T16 10"), detail("M6 15Q8 12.5 10 15"), line(poly([(13, 21), (13, 13), (21, 13)], r=S.r))]


@icon("sleeve-tattoo", CAT, "An arm from shoulder to wrist filled with a continuous pattern of waves and swirls.",
      tags=["full sleeve", "arm", "tattoo design", "body art", "ink", "pattern", "half sleeve"])
def _(S):
    return [shell(poly([(2, 5), (22, 9), (22, 15), (2, 19)], closed=True, r=S.r * 2)), detail("M6 10Q8 8 10 10T14 10"),
            detail("M6 14.5Q8 12.5 10 14.5T14 14.5"), dot(18, 12, 1.2)]


@icon("tattoo-aftercare-wrap", CAT, "A forearm with a star tattoo covered by a clear wrap sheet taped at both ends.",
      tags=["aftercare", "healing", "bandage", "film", "wrap", "tattoo care", "cover"])
def _(S):
    return [shell(rect(2.5, 7, 19, 10, L(S, 2, 5))), detail(seg(6, 7, 6, 17)), detail(seg(18, 7, 18, 17)),
            solidpart(poly(star(12, 12, 3.4, 1.5), closed=True))]


@icon("temporary-tattoo", CAT, "A square transfer sheet with a star design and one corner peeling back.",
      tags=["transfer", "fake tattoo", "kids", "decal", "sticker", "water transfer", "body art"])
def _(S):
    return [shell(poly([(3, 3), (21, 3), (21, 14), (14, 21), (3, 21)], closed=True, r=S.r)),
            solidpart(poly(star(10.5, 11, 5, 2.3), closed=True)),
            line(poly([(14, 21), (14, 14), (21, 14)], r=S.r))]


@icon("hand-poke-tattoo", CAT, "A slim stick with a needle tip held at an angle over skin with a short line of dots.",
      tags=["stick and poke", "diy", "needle", "tattoo", "ink", "dotwork", "manual tattoo"])
def _(S):
    return [shell(bar((21, 3), (12, 12), 3, 0, S.r * 0.5)), line(seg(12, 12, 9.5, 15)), line(seg(2, 21, 22, 21)),
            dot(4, 18, 1), dot(8, 18, 1), dot(12, 18, 1)]


# ============================================================================ piercing

@icon("piercing-needle", CAT, "A long hollow piercing needle with a bevelled tip and a short hub at the back.",
      tags=["needle", "body piercing", "hollow needle", "jewelry", "studio", "sterile", "piercer"])
def _(S):
    return [shell(bar((21, 3), (15.5, 8.5), 4.5, 0, S.r * 0.5)), shell(poly([(13, 10), (15, 12), (4, 21)], closed=True, r=S.r * 0.3))]


@icon("piercing-clamp", CAT, "Forceps with two finger rings and a pair of flat triangular jaws.",
      tags=["forceps", "body piercing", "clamp", "tool", "studio", "piercer", "pliers"])
def _(S):
    return [shell(circle(7, 18.5, 2.5)), shell(circle(17, 18.5, 2.5)), line(seg(8.5, 16.5, 15, 9)), line(seg(15.5, 16.5, 9, 9)),
            shell(poly([(7, 3), (10.5, 3), (9, 8.5)], closed=True, r=S.r * 0.5)),
            shell(poly([(17, 3), (13.5, 3), (15, 8.5)], closed=True, r=S.r * 0.5))]


@icon("piercing-gun", CAT, "A small handgun shaped ear piercing tool with a stud earring loaded at its nose.",
      tags=["ear piercing", "earring", "stud", "jewelry", "tool", "piercing", "mall kiosk"])
def _(S):
    return [shell(poly([(3, 5), (16, 5), (16, 10), (12.5, 10), (11, 20), (5.5, 20), (7, 10), (3, 10)], closed=True, r=S.r)),
            line(seg(16, 8, 19, 8)), dot(20.5, 8, 1.4)]


@icon("septum-ring", CAT, "A nose in front view with a horseshoe ring hanging below the tip, a ball on each end.",
      tags=["nose ring", "septum", "horseshoe", "jewelry", "body piercing", "nose", "circular barbell"])
def _(S):
    return [shell(poly([(10, 3), (7.5, 11), (6, 14), (8, 17), (12, 16), (16, 17), (18, 14), (16.5, 11), (14, 3)],
                       closed=True, r=S.r * 1.2)),
            line("M9.8 17A2.2 2.2 0 1 0 14.2 17"), dot(9.8, 17, 1.1), dot(14.2, 17, 1.1)]


@icon("lip-ring", CAT, "Closed lips with a small hoop ring through the lower lip near one corner.",
      tags=["lip piercing", "labret", "jewelry", "hoop", "body piercing", "mouth", "lips"])
def _(S):
    lips = L(S, "M3 9L8 6L12 7.5L16 6L21 9L16 14H8Z", "M3 9Q7.5 5.5 12 7.5Q16.5 5.5 21 9Q16.5 15 12 15Q7.5 15 3 9Z")
    return [shell(lips), detail(seg(3.8, 9, 20.2, 9)), line("M15.5 13.5A3 3 0 1 0 19.5 16")]


@icon("eyebrow-piercing", CAT, "An eye under an eyebrow with a small curved barbell through the outer end of the brow.",
      tags=["brow piercing", "jewelry", "barbell", "body piercing", "face", "eyebrow", "curved barbell"])
def _(S):
    return [line("M3 10Q9 5 17 8"), shell("M3 18Q9 13 15 18Q9 23 3 18Z"), dot(9, 18, 1.4),
            line("M14.5 4Q18 8 14.5 12.5"), dot(14.5, 4, 1.4), dot(14.5, 12.5, 1.4)]


@icon("industrial-piercing", CAT, "An ear outline with a long straight bar running diagonally across the upper cartilage.",
      tags=["ear", "scaffold", "barbell", "body piercing", "jewelry", "cartilage", "bar"])
def _(S):
    return [line("M6 20C6 6 12 3 16 6C20 9 16 14 15 17C14 20 9 22 8 18"), line(seg(4, 6, 20, 10)), dot(4, 6, 1.5), dot(20, 10, 1.5)]


@icon("tongue-piercing", CAT, "An open mouth with the tongue out and a ball stud through its centre.",
      tags=["tongue", "barbell", "jewelry", "body piercing", "mouth", "stud", "oral"])
def _(S):
    return [shell("M3 5C3 5 12 3 21 5C21 11 17 13 12 13C7 13 3 11 3 5Z"), line("M8.5 11V17.5A3.5 3.5 0 0 0 15.5 17.5V11"),
            dot(12, 16, 1.4)]


@icon("captive-bead-ring", CAT, "A round hoop ring with a small gap closed by a single bead held between the ends.",
      tags=["ring", "hoop", "jewelry", "body piercing", "cbr", "bead", "nose ring"])
def _(S):
    return [line(arc(12, 13, 8, 300, 600)), dot(12, 5.5, 2.3)]


@icon("labret-stud", CAT, "A short straight post with a flat round disc at one end and a ball at the other, in side view.",
      tags=["lip stud", "flat back", "jewelry", "body piercing", "monroe", "post", "stud"])
def _(S):
    return [shell(rect(3, 7, 3, 10, L(S, 0.5, 1.5))), line(seg(6, 12, 16.5, 12)), shell(circle(19, 12, 2.5))]


@icon("ear-tunnel", CAT, "An earlobe in side view with a large round hollow tunnel set through it.",
      tags=["gauge", "stretched ear", "plug", "flesh tunnel", "jewelry", "body modification", "ear"])
def _(S):
    lobe = poly([(9, 3), (15, 4), (17, 10), (15, 17), (13, 21), (9, 21), (7, 17), (7, 8)], closed=True, r=S.r * 2.5)
    return [shell(lobe), detail(circle(11, 16, 2.5))]
