"""TypeIcon Core: cosmetics (batch 001): fragrance, makeup, brushes, nails and skincare.

Objects are drawn upright from the front. Outlines are shells, internal marks are details (knocked out in
Filled), small products and sparkles are dots or solids.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "cosmetics"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


_PRE: set = set()


def rl(kind, x1, y1, x2, y2, deg=45):
    """Open straight stroke whose end points are already rotated (turn() leaves it alone)."""
    a = math.radians(deg)
    c, s_ = math.cos(a), math.sin(a)

    def r(x, y):
        return 12 + (x - 12) * c - (y - 12) * s_, 12 + (x - 12) * s_ + (y - 12) * c
    (ax, ay), (bx, by) = r(x1, y1), r(x2, y2)
    part = Part(kind, seg(ax, ay, bx, by))
    _PRE.add(id(part))
    return part


def turn(parts, deg, cx=12.0, cy=12.0):
    """Rotate every closed part about (cx, cy) (open strokes: build them with rl)."""
    return [p if id(p) in _PRE else Part(p.kind, rot(p.d, deg, cx, cy), p.attrs) for p in parts]


def rp(x, y, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s_ = math.cos(a), math.sin(a)
    return cx + (x - cx) * c - (y - cy) * s_, cy + (x - cx) * s_ + (y - cy) * c


def heart(x, y, w=2.6):
    """Small solid heart centred on (x, y)."""
    h = w * 0.55
    return (f"M{fmt(x)} {fmt(y + w * 0.8)}L{fmt(x - w)} {fmt(y - h * 0.1)}A{fmt(w / 2)} {fmt(w / 2)} 0 0 1 {fmt(x)} {fmt(y - h * 0.9)}"
            f"A{fmt(w / 2)} {fmt(w / 2)} 0 0 1 {fmt(x + w)} {fmt(y - h * 0.1)}Z")


def star(cx, cy, r, ri=None, n=5):
    ri = ri or r * 0.45
    pts = []
    for i in range(n * 2):
        pts.append(polar(cx, cy, r if i % 2 == 0 else ri, -90 + i * 180 / n))
    return poly(pts, closed=True)


def face(S):
    """Egg shaped front face outline on the left half of the grid."""
    return poly([(3.5, 5), (13.5, 5), (14, 13), (8.5, 21), (3, 13)], closed=True, r=L(S, 4, 7))


def kn(d):
    """Small solid mark: solid in Line and Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def tapered(x1, y1, x2, y2, w1, w2):
    """Closed point list for a tapered handle from (x1, y1) to (x2, y2)."""
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    nx, ny = -dy / n, dx / n
    return [(x1 + nx * w1 / 2, y1 + ny * w1 / 2), (x2 + nx * w2 / 2, y2 + ny * w2 / 2),
            (x2 - nx * w2 / 2, y2 - ny * w2 / 2), (x1 - nx * w1 / 2, y1 - ny * w1 / 2)]


def sq(x, y, w, h, rx=0.0):
    return Part("dot", rect(x, y, w, h, rx))


def spark(x, y, r=2.0):
    """Four point sparkle (solid)."""
    k = r * 0.3
    return solid(poly([(x, y - r), (x + k, y - k), (x + r, y), (x + k, y + k), (x, y + r), (x - k, y + k),
                       (x - r, y), (x - k, y - k)], closed=True))


def tear(cx, cy, r):
    """Teardrop pointing up (d-string)."""
    return union(circle(cx, cy, r), poly([(cx - r * 0.75, cy - r * 0.6), (cx, cy - r * 2.0), (cx + r * 0.75, cy - r * 0.6)], closed=True))


def lips(cx, cy, w, h):
    return (f"M{fmt(cx - w / 2)} {fmt(cy)}C{fmt(cx - w / 4)} {fmt(cy - h * .9)} {fmt(cx - w * .08)} {fmt(cy - h * .9)} {fmt(cx)} {fmt(cy - h * .4)}"
            f"C{fmt(cx + w * .08)} {fmt(cy - h * .9)} {fmt(cx + w / 4)} {fmt(cy - h * .9)} {fmt(cx + w / 2)} {fmt(cy)}"
            f"C{fmt(cx + w / 4)} {fmt(cy + h * .9)} {fmt(cx - w / 4)} {fmt(cy + h * .9)} {fmt(cx - w / 2)} {fmt(cy)}Z")


def wave(x, y0, y1, a=1.5):
    """Vertical wavy scent line from y0 down to y1 (two bumps)."""
    m = (y0 + y1) / 2
    return f"M{fmt(x)} {fmt(y1)}Q{fmt(x - a)} {fmt((y1 + m) / 2)} {fmt(x)} {fmt(m)}T{fmt(x)} {fmt(y0)}"


# ============================================================================ fragrance bottles

@icon("round-perfume-bottle", CAT, "Spherical perfume bottle with a short neck, a spray cap and a liquid line",
      tags=["perfume", "fragrance", "cologne", "scent", "bottle", "spray", "glass"])
def _(S):
    body = union(circle(12, 15, 6.5), rect(10.5, 6, 3, 4))
    return [shell(body), shell(rect(9, 2.5, 6, 3.5, L(S, 0, 1.2))),
            detail("M8 15Q10 13.5 12 15T16 15")]


@icon("heart-perfume-bottle", CAT, "Heart shaped perfume bottle with a short neck and a square stopper",
      tags=["perfume", "fragrance", "love", "valentine", "gift", "bottle", "scent"])
def _(S):
    heart = "M12 21Q3.5 15.5 3.5 11.5Q3.5 8.5 6.5 8.5Q10 8.5 12 11.5Q14 8.5 17.5 8.5Q20.5 8.5 20.5 11.5Q20.5 15.5 12 21Z"
    return [shell(union(heart, rect(10.5, 6, 3, 4))), shell(rect(9.5, 2.5, 5, 3.5, L(S, 0, 1.2)))]


@icon("faceted-perfume-bottle", CAT, "Perfume bottle with an angular cut body and a faceted crystal stopper",
      tags=["perfume", "crystal", "cut glass", "luxury", "fragrance", "bottle", "diamond"])
def _(S):
    k = S.r
    body = poly([(12, 21.5), (4, 13.5), (7, 9), (17, 9), (20, 13.5)], closed=True, r=k)
    return [shell(body), shell(poly([(10, 2.5), (14, 2.5), (15.5, 5.5), (8.5, 5.5)], closed=True, r=k * 0.6)),
            shell(rect(10.5, 5.5, 3, 3.5)),
            detail(seg(4, 13.5, 20, 13.5)), detail(seg(12, 13.5, 12, 20))]


@icon("art-deco-perfume-bottle", CAT, "Squat rectangular perfume bottle with stepped shoulders and a fan shaped stopper",
      tags=["perfume", "vintage", "deco", "fragrance", "bottle", "antique", "scent"])
def _(S):
    body = poly([(4, 21.5), (4, 14), (6.5, 14), (6.5, 11), (17.5, 11), (17.5, 14), (20, 14), (20, 21.5)],
                closed=True, r=S.r * 0.6)
    fan = "M12 11L7 5A7 7 0 0 1 17 5Z"
    return [shell(body), shell(fan), detail(seg(12, 11, 12, 3.5))]


@icon("perfume-dauber-bottle", CAT, "Small perfume bottle with its round stopper lifted out on a long dauber rod",
      tags=["perfume", "attar", "oud", "fragrance oil", "dipper", "bottle", "scent"])
def _(S):
    return [shell(union(rect(5, 14.5, 14, 7, L(S, 1.5, 3.5)), rect(9, 12, 6, 3))),
            shell(circle(12, 5, 3)), line(seg(12, 8, 12, 18))]


@icon("rollerball-perfume", CAT, "Slim rollerball perfume tube with a ball tip beside its screw cap",
      tags=["roll on", "perfume", "fragrance", "oil", "travel", "scent", "cap"])
def _(S):
    return [shell(rect(3.5, 9.5, 6.5, 12, L(S, 1, 3))), shell(rect(5.5, 6.5, 2.5, 3)), shell(circle(6.75, 4.5, 2)),
            shell(rect(14, 5.5, 6.5, 16, L(S, 1, 3))), detail(seg(14, 9.5, 20.5, 9.5))]


@icon("solid-perfume-tin", CAT, "Round balm tin with its lid open and a fingertip swipe across the solid perfume",
      tags=["solid perfume", "balm", "tin", "fragrance", "compact", "wax", "scent"])
def _(S):
    tin = "M3 12.5V17.5A9 3.5 0 0 0 21 17.5V12.5"
    return [shell(rect(6, 2.5, 12, 7, L(S, 1.5, 3))), line(tin), shell(ellipse(12, 12.5, 9, 3.5)),
            detail("M8.5 13Q11.5 11.5 15.5 13")]


@icon("travel-perfume-spray", CAT, "Slim refillable atomizer with a nozzle cap and a puff of mist above",
      tags=["atomizer", "perfume", "travel", "refill", "spray", "mist", "fragrance"])
def _(S):
    return [shell(rect(8, 10.5, 8, 11, L(S, 1, 3))), shell(rect(10, 7, 4, 3.5)),
            dot(8.5, 3.5, 1), dot(12, 2.5, 1), dot(15.5, 3.5, 1)]


@icon("fragrance-wheel", CAT, "Circle split into four wedges with a flower, a leaf, a wood grain and a citrus mark",
      tags=["scent wheel", "fragrance families", "floral", "woody", "citrus", "perfume", "chart"])
def _(S):
    leaf = poly([(7.5, 4.5), (9.5, 7.5), (7.5, 10.5), (5.5, 7.5)], closed=True, r=S.r * 1.3)
    return [shell(circle(12, 12, 9.5)), detail(seg(12, 2.5, 12, 21.5)), detail(seg(2.5, 12, 21.5, 12)),
            kn(leaf), dot(16.5, 7.5, 1.6), kn(rect(5.5, 16, 4, 1.4) + rect(5.5, 18.5, 4, 1.4)),
            kn(L(S, "M14.5 17.5A2.2 2.2 0 0 1 18.5 17.5Z", "M14.5 17.2A2.2 2.2 0 0 1 18.5 17.2Q16.5 18.4 14.5 17.2Z"))]


@icon("perfume-gift-set", CAT, "Open gift box holding a tall perfume bottle and a mini bottle with a ribbon",
      tags=["gift", "perfume", "set", "present", "fragrance", "box", "boxed"])
def _(S):
    return [shell(rect(3, 13.5, 18, 8, L(S, 0.5, 2))), detail(seg(17, 13.5, 17, 21.5)),
            shell(rect(5.5, 6.5, 6, 7)), shell(rect(7, 3, 3, 3.5)),
            shell(rect(13.5, 9.5, 4, 4))]


@icon("perfume-organ", CAT, "Tiered shelf unit holding rows of small perfume vials, a perfumer's workstation",
      tags=["perfumer", "fragrance lab", "vials", "shelf", "scent", "workstation", "blending"])
def _(S):
    return [shell(rect(3, 3, 18, 18, L(S, 0.5, 3))), detail(seg(3, 12, 21, 12)),
            sq(6.5, 6.5, 2.5, 3.5), sq(10.75, 6.5, 2.5, 3.5), sq(15, 6.5, 2.5, 3.5),
            sq(6.5, 15.5, 2.5, 3), sq(10.75, 15.5, 2.5, 3), sq(15, 15.5, 2.5, 3)]


@icon("spraying-perfume", CAT, "Perfume bottle spraying a fine mist toward a forearm",
      tags=["perfume", "apply", "fragrance", "spritz", "wrist", "scent", "mist"])
def _(S):
    return [shell(rect(2.5, 9, 6, 12.5, L(S, 0.5, 2.5))), shell(rect(4, 5.5, 3, 3.5)),
            dot(11, 6, 1), dot(13.5, 7.5, 1), dot(16, 9, 1),
            shell(rect(11.5, 13, 10.5, 7, 3.5))]


@icon("car-vent-air-freshener", CAT, "Round clip on air freshener attached to the slats of a car vent",
      tags=["car", "freshener", "vent clip", "scent", "automotive", "air", "fragrance"])
def _(S):
    return [shell(rect(2.5, 12, 19, 9.5, L(S, 1, 3))), detail(seg(2.5, 16.75, 21.5, 16.75)),
            shell(circle(12, 7.5, 3.5)),
            line(wave(5, 3, 9)), line(wave(19, 3, 9))]


@icon("air-freshener-dispenser", CAT, "Wall box dispenser showing a spray can through a window with a puff of mist below",
      tags=["air freshener", "aerosol", "dispenser", "room spray", "automatic", "scent", "bathroom"])
def _(S):
    return [shell(rect(3, 2.5, 18, 13, L(S, 1, 3))), detail(rect(7, 5.5, 10, 6.5)), sq(10.5, 7.5, 3, 3),
            line(seg(12, 15.5, 12, 18)), dot(8, 20.5, 1), dot(12, 21, 1), dot(16, 20.5, 1)]


# ============================================================================ resins, flasks and makeup

@icon("frankincense-resin", CAT, "Cluster of teardrop shaped resin lumps with a thin smoke curl rising above",
      tags=["incense", "resin", "aromatic", "smoke", "fragrance", "raw material", "burning"])
def _(S):
    k = S.r * 0.6
    return [shell(poly(regular(7, 17.5, 4.3, 5, -80), closed=True, r=k)),
            shell(poly(regular(16, 18, 4.8, 6, -60), closed=True, r=k)),
            shell(poly(regular(11.5, 12, 3, 5, -100), closed=True, r=k)),
            line("M11.5 8Q9 6 11.5 4.5T11.5 2.5")]


@icon("agarwood-chips", CAT, "Splintered wood chips with grain lying in a shallow dish, the raw material of oud",
      tags=["oud", "agarwood", "incense", "wood chips", "fragrance", "bakhoor", "raw material"])
def _(S):
    bowl = "M3 14H21A9 7 0 0 1 3 14Z"
    return [shell(bowl), shell(poly([(6.5, 12), (5.5, 7.5), (8, 6), (9.5, 12)], closed=True, r=S.r * 0.5)),
            shell(poly([(11, 12), (11, 4.5), (13.5, 4.5), (13.5, 12)], closed=True, r=S.r * 0.5)),
            shell(poly([(15, 12), (16.5, 6), (18.5, 7.5), (18, 12)], closed=True, r=S.r * 0.5))]


@icon("aryballos", CAT, "Ancient round bodied flask with a narrow neck, a flat disc lip and a loop handle",
      tags=["ancient", "greek", "oil flask", "perfume", "amphora", "pottery", "historic"])
def _(S):
    return [shell(union(circle(10.5, 15.5, 6), rect(9, 8, 3, 3))), shell(rect(6.5, 4, 8, 3, L(S, 0, 1.4))),
            line("M12.5 10C21 6 22 15 16 15")]


@icon("perfumer", CAT, "Person in a lab coat holding a paper blotter strip up to the nose and a small bottle",
      tags=["nose", "fragrance expert", "scent designer", "lab", "profession", "perfume", "blotter"])
def _(S):
    return [shell(circle(9.5, 7, 3.5)),
            shell(f"M2.5 21.5V17Q2.5 12 9.5 12Q16.5 12 16.5 17V21.5Z"),
            detail("M7 12.5L9.5 17L12 12.5"),
            line(seg(13.5, 6.5, 21, 3.5)), shell(rect(18.5, 16.5, 3.5, 5, L(S, 0, 1)))]


@icon("perfume-vanity-tray", CAT, "Oval tray holding three perfume bottles of different heights and shapes",
      tags=["vanity", "dresser", "perfume", "collection", "display", "fragrance", "tray"])
def _(S):
    k = L(S, 0, 1.2)
    return [shell(ellipse(12, 17.5, 10, 3.5)),
            solid(rect(4, 9, 4, 8, k)), solid(rect(5, 6.5, 2, 2.5)),
            solid(union(circle(12, 13, 3.2), rect(11, 7.5, 2, 3))),
            solid(rect(16, 5, 4, 12, k)), solid(rect(17, 2.5, 2, 2.5))]


@icon("perfume-pendant", CAT, "Tiny stoppered perfume bottle hanging from a thin chain necklace",
      tags=["locket", "necklace", "jewelry", "perfume", "chain", "wearable", "fragrance"])
def _(S):
    return [line("M3.5 3Q4.5 8 12 8Q19.5 8 20.5 3"), shell(rect(10, 8.5, 4, 2.5)),
            shell(union(circle(12, 16.5, 5), rect(10.5, 11, 3, 3)))]


@icon("fragrance-lamp", CAT, "Rounded glass bottle topped with a burner head and heat lines rising above",
      tags=["catalytic lamp", "fragrance", "diffuser", "home", "scent", "burner", "air"])
def _(S):
    return [shell(union(circle(12, 17, 5), rect(10, 10, 4, 4))), shell(rect(8, 6.5, 8, 3.5, L(S, 0, 1.2))),
            line(wave(9.5, 1.5, 4.5, 1)), line(wave(14.5, 1.5, 4.5, 1))]


@icon("lip-brush", CAT, "Slim lip brush with a tapered tip and a protective sleeve pulled halfway over the handle",
      tags=["lipstick", "makeup brush", "lips", "applicator", "cosmetic", "beauty", "gloss"])
def _(S):
    k = S.r * 0.5
    return turn([shell(poly([(12, 2), (14.5, 8), (9.5, 8)], closed=True, r=k)),
                 shell(rect(10, 8.5, 4, 3)),
                 rl("line", 12, 11.5, 12, 14),
                 shell(rect(9, 14, 6, 7.5, L(S, 0, 2)))], 45)


@icon("lipstick-swatch", CAT, "Three color test streaks of different lengths beside a lipstick tip",
      tags=["lip color", "shade", "swatch", "test", "makeup", "lipstick", "smear"])
def _(S):
    return [line(seg(3.5, 11, 12, 8)), line(seg(3.5, 16, 15, 12)), line(seg(3.5, 21, 10, 18.5)),
            shell(poly([(15.5, 6.5), (20, 3), (20, 9), (15.5, 9)], closed=False, r=S.r * 0.5) + "Z")]


@icon("applying-lipstick", CAT, "Lips seen from the front with a lipstick bullet touching the lower lip",
      tags=["lipstick", "makeup", "lips", "apply", "cosmetic", "beauty", "mouth"])
def _(S):
    k = S.r * 0.5
    stick = [shell(rect(15, 14, 4, 7.5, L(S, 0, 1))),
             shell(poly([(15, 14), (15, 10), (19, 8), (19, 14)], closed=True, r=k))]
    return [shell(lips(9, 8, 13, 5.5))] + [Part(p.kind, rot(p.d, -35, 17, 17), p.attrs) for p in stick] + \
        [detail("M2.5 8Q9 10 15.5 8")]


@icon("concealer-pen", CAT, "Slim click pen with a small brush tip, a collar and a push button at the end",
      tags=["concealer", "click pen", "brush pen", "makeup", "cosmetic", "highlighter pen", "touch up"])
def _(S):
    return turn([dot(12, 2.8, 1.2),
                 shell(poly([(10.5, 9), (12, 5.5), (13.5, 9)], closed=True)),
                 shell(rect(9.5, 9, 5, 2.5)), shell(rect(9, 11.5, 6, 7.5, L(S, 0, 2))),
                 shell(rect(10.5, 19, 3, 2.5))], 45)


@icon("cushion-compact", CAT, "Open round compact with a mirror lid, a dotted cushion and a round puff",
      tags=["cushion", "foundation", "compact", "makeup", "puff", "mirror", "bb cushion"])
def _(S):
    return [shell(rect(5, 2.5, 14, 7.5, L(S, 1, 3.5))), kn(spark(12, 6.2, 1.6).d),
            shell(ellipse(12, 16.5, 9.5, 5)), shell(circle(12, 16, 2.2)),
            dot(6.5, 16.5, 1), dot(17.5, 16.5, 1)]


@icon("bronzer-compact", CAT, "Square compact with the lid open and a round pan holding a small sun mark",
      tags=["bronzer", "powder", "compact", "sun", "makeup", "contour", "tan"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 6.5, L(S, 1, 3))), shell(rect(3, 11, 18, 10.5, L(S, 1, 3.5))),
            detail(circle(12, 16.25, 3.6)), dot(12, 16.25, 1.1)]


@icon("makeup-highlighter", CAT, "Round pressed powder pan with a diagonal shimmer streak and sparkles at the edge",
      tags=["highlighter", "shimmer", "glow", "illuminator", "makeup", "powder", "sparkle"])
def _(S):
    return [shell(circle(10.5, 13.5, 7.5)), detail(seg(7, 17, 14, 10)), spark(19, 5, 2.6), spark(20, 12, 1.5)]


# ============================================================================ base makeup and brushes

@icon("contour-stick", CAT, "Twist up contour stick with an angled two tone tip and its cap standing beside it",
      tags=["contour", "cream stick", "sculpt", "makeup", "foundation stick", "highlight", "cosmetic"])
def _(S):
    k = S.r * 0.5
    return [shell(rect(3.5, 13, 8, 8.5, L(S, 0, 2))),
            shell(poly([(3.5, 13), (3.5, 8.5), (11.5, 4), (11.5, 13)], closed=True, r=k)),
            detail(seg(3.5, 10.5, 11.5, 7)),
            shell(rect(15, 6.5, 6, 15, L(S, 0, 2.5))), detail(seg(15, 10, 21, 10))]


@icon("loose-powder-jar", CAT, "Short round jar with a sifter disc full of small holes and a puff of powder above",
      tags=["loose powder", "setting powder", "sifter", "makeup", "jar", "face powder", "translucent"])
def _(S):
    return [shell(rect(4, 14.5, 16, 7, L(S, 1, 3))), shell(rect(5, 8.5, 14, 6, L(S, 1, 3))),
            dot(8.5, 11.5, 0.9), dot(12, 11.5, 0.9), dot(15.5, 11.5, 0.9),
            dot(8, 4.5, 1), dot(12, 3, 1), dot(16, 4.5, 1)]


@icon("color-corrector-palette", CAT, "Square palette with four round pans in a two by two grid, each filled differently",
      tags=["corrector", "concealer palette", "makeup", "color correcting", "pans", "cosmetic", "compact"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, L(S, 1.5, 4))),
            detail(circle(8, 8, 2.2)), dot(8, 8, 0.8),
            detail(circle(16, 8, 2.2)),
            detail(circle(8, 16, 2.2)), detail(seg(6.5, 16, 9.5, 16)),
            dot(16, 16, 2.4)]


@icon("blotting-papers", CAT, "Small booklet of oil blotting sheets with one thin sheet pulled halfway out showing a drop mark",
      tags=["oil control", "blotting sheets", "shine", "skincare", "makeup", "booklet", "face papers"])
def _(S):
    return [shell(rect(3.5, 9.5, 14, 12, L(S, 0.5, 2.5))),
            shell(poly([(8, 9.5), (8, 3), (20.5, 3), (20.5, 9.5)], closed=False, r=S.r * 0.5)),
            kn(tear(14.5, 7, 1.1))]


@icon("micellar-water", CAT, "Clear bottle with a pump top and a round cotton pad pressed onto it",
      tags=["cleanser", "makeup remover", "cotton pad", "skincare", "pump bottle", "toner", "face"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 3.5, L(S, 0.5, 1.75))), shell(rect(9.5, 6, 5, 2)),
            shell(rect(10.5, 8, 3, 2.5)),
            shell(rect(6.5, 10.5, 11, 11, L(S, 1, 3.5))), detail("M6.5 16Q9.25 14.5 12 16T17.5 16")]


@icon("makeup-wedge-sponge", CAT, "Triangular foam makeup wedge with small pores on its surface",
      tags=["sponge", "foundation", "blending", "wedge", "makeup", "applicator", "latex free"])
def _(S):
    return [shell(poly([(12, 3), (21.5, 20.5), (2.5, 20.5)], closed=True, r=S.r * 1.6)),
            dot(12, 12.5, 1), dot(9, 17, 1), dot(15, 17, 1)]


@icon("removing-makeup", CAT, "Face outline with a round cotton pad swept across one cheek and motion strokes",
      tags=["makeup remover", "cleanse", "cotton pad", "skincare", "wipe", "face", "cleansing"])
def _(S):
    return [shell(face(S)),
            dot(6.5, 10, 1), dot(10.5, 10, 1),
            shell(circle(18, 15.5, 3.5))]


@icon("powder-brush", CAT, "Large round fluffy brush head on a long slim tapered handle",
      tags=["makeup brush", "face powder", "bronzer", "blush", "fluffy", "cosmetic", "kabuki"])
def _(S):
    return turn([shell("M7.5 11Q4 7 7.5 4Q12 0.5 16.5 4Q20 7 16.5 11Z"),
                 shell(rect(10, 11.5, 4, 3)),
                 shell(poly([(10.8, 15), (13.2, 15), (12.6, 21.5), (11.4, 21.5)], closed=True))], 45)


@icon("angled-blush-brush", CAT, "Medium brush whose bristles are cut on a slanted edge, on a slim handle",
      tags=["blush brush", "contour brush", "makeup brush", "cheek", "angled", "cosmetic", "bronzer"])
def _(S):
    return turn([shell(poly([(8, 11), (8, 6.5), (16, 3), (16, 11)], closed=True, r=S.r * 0.7)),
                 shell(rect(10, 11.5, 4, 3)),
                 shell(poly([(10.8, 15), (13.2, 15), (12.6, 21.5), (11.4, 21.5)], closed=True))], 45)


@icon("flat-foundation-brush", CAT, "Flat paddle shaped brush head with a rounded tip, seen face on, on a slim handle",
      tags=["foundation brush", "makeup brush", "paddle", "flat", "liquid foundation", "cosmetic", "applicator"])
def _(S):
    return turn([shell(rect(8, 2.5, 8, 10, L(S, 2, 4))), rl("detail", 12, 5.5, 12, 9),
                 shell(rect(10, 12.5, 4, 2.5)),
                 shell(poly([(10.8, 15.5), (13.2, 15.5), (12.6, 21.5), (11.4, 21.5)], closed=True))], 45)


@icon("eyeshadow-blending-brush", CAT, "Slim handle with a small tapered fluffy brush head shaped like a flame",
      tags=["blending brush", "eyeshadow", "eye makeup", "makeup brush", "crease brush", "cosmetic", "fluffy"])
def _(S):
    return turn([shell("M12 2Q17 7 15.5 11H8.5Q7 7 12 2Z"), shell(rect(10, 11.5, 4, 2.5)),
                 shell(poly([(10.8, 14.5), (13.2, 14.5), (12.6, 21.5), (11.4, 21.5)], closed=True))], 45)


@icon("brush-drying-rack", CAT, "Small rack holding three makeup brushes upside down so the heads point to the floor",
      tags=["brush holder", "drying", "makeup brushes", "brush care", "stand", "hang", "storage"])
def _(S):
    return [line(seg(2.5, 3, 21.5, 3)),
            line(seg(7, 3, 7, 12)), line(seg(12, 3, 12, 12)), line(seg(17, 3, 17, 12)),
            solid(ellipse(7, 16.5, 2.2, 4.2)), solid(ellipse(12, 16.5, 2.2, 4.2)), solid(ellipse(17, 16.5, 2.2, 4.2))]


@icon("sponge-tip-applicator", CAT, "Double ended stick with a small teardrop shaped foam tip at each end",
      tags=["eyeshadow applicator", "sponge tip", "eye makeup", "cosmetic", "tool", "dual ended", "blending"])
def _(S):
    k = L(S, 0, 2.6)
    return turn([shell(poly([(1.5, 12), (5.5, 8.5), (9, 12), (5.5, 15.5)], closed=True, r=k)),
                 rl("line", 9, 12, 15, 12, -45),
                 shell(poly([(22.5, 12), (18.5, 8.5), (15, 12), (18.5, 15.5)], closed=True, r=k))], -45)


# ============================================================================ eyes, brows and lashes

@icon("liquid-eyeliner", CAT, "Felt tip liner pen with a fine pointed tip beside a thin winged stroke",
      tags=["eyeliner", "winged liner", "cat eye", "eye makeup", "pen", "felt tip", "cosmetic"])
def _(S):
    return [shell(rect(3.5, 10.5, 6.5, 11, L(S, 0, 2.5))), shell(poly([(4.5, 10.5), (6.75, 4.5), (9, 10.5)], closed=True, r=S.r * 0.4)),
            detail(seg(3.5, 14.5, 10, 14.5)),
            line("M13.5 19Q18.5 18.5 21 12")]


@icon("gel-eyeliner", CAT, "Small squat pot of gel liner with an angled brush resting across the open top",
      tags=["gel liner", "eyeliner pot", "eye makeup", "brush", "cosmetic", "jar", "precision"])
def _(S):
    return [shell(rect(4, 13.5, 16, 8, L(S, 1, 3))), line(seg(21, 3.5, 12.5, 9)),
            solid(rot(ellipse(9.5, 10.8, 3.4, 1.8), -31, 9.5, 10.8))]


@icon("eyebrow-stencil", CAT, "Card with a brow shaped cutout and a pencil tip filling in the opening",
      tags=["brow", "stencil", "template", "eyebrow pencil", "makeup", "shape", "guide"])
def _(S):
    pencil = turn([shell(rect(10.5, 9, 3, 12.5)), shell(poly([(10.5, 9), (12, 5), (13.5, 9)], closed=True))], 225)
    return [shell(rect(2.5, 9, 12, 12.5, L(S, 1, 3.5))), detail("M5 18Q8 13.5 12 15.5")] + pencil


@icon("lash-glue", CAT, "Tiny squeeze tube with a very fine needle nozzle and a small drop at the tip",
      tags=["eyelash glue", "adhesive", "false lashes", "lashes", "makeup", "tube", "cosmetic"])
def _(S):
    return [shell(poly([(6.5, 21.5), (6.5, 13), (10, 11), (14, 11), (17.5, 13), (17.5, 21.5)], closed=True, r=S.r * 0.6)),
            detail(seg(6.5, 19, 17.5, 19)), line(seg(12, 11, 12, 6)), solid(tear(12, 3.6, 1.1))]


@icon("eyelash-extensions", CAT, "Closed eye with a row of long lashes and fine tweezers placing a single lash",
      tags=["lash extensions", "eyelashes", "tweezers", "salon", "lash artist", "beauty", "volume lashes"])
def _(S):
    lashes = [line(seg(5.5, 13, 3.5, 18)), line(seg(8.5, 14.8, 7.5, 20)), line(seg(12, 15.5, 12, 21)),
              line(seg(15.5, 14.8, 16.5, 20))]
    return [line("M3 11.5Q12 18 21 11.5")] + lashes + [line(seg(21.5, 2.5, 19, 8)), line(seg(17.5, 2.5, 19, 8))]


@icon("applying-mascara", CAT, "Open eye with a mascara wand brushing up through the upper lashes",
      tags=["mascara", "eye makeup", "lashes", "wand", "apply", "cosmetic", "volumizing"])
def _(S):
    return [shell(poly([(2.5, 16), (12, 11), (21.5, 16), (12, 21.5)], closed=True, r=L(S, 4, 9))),
            dot(12, 16.3, 1.9), line(seg(5.5, 13.5, 3.5, 9.5)), line(seg(9, 12, 8, 7.5)),
            solid(rot(ellipse(15, 6.5, 1.7, 3.6), 40, 15, 6.5)), line(seg(17.5, 4.5, 21.5, 2.5))]


@icon("brow-mapping", CAT, "Eyebrow and eye with three straight guide lines fanning toward the start, arch and tail of the brow",
      tags=["eyebrow shaping", "brow design", "microblading", "measure", "guide lines", "symmetry", "beauty"])
def _(S):
    return [line("M5 9.5Q12.5 3 20.5 8"), line(seg(2.5, 21.5, 5, 11)), line(seg(2.5, 21.5, 13, 5.8)),
            line(seg(2.5, 21.5, 20, 9)), dot(17, 18, 2)]


# ============================================================================ nails and skincare

@icon("nail-stickers", CAT, "Small sheet of nail decals with hearts and flowers and one decal peeling up at the corner",
      tags=["nail art", "decals", "manicure", "stickers", "press on", "design", "nail wraps"])
def _(S):
    sheet = poly([(3, 2.5), (21, 2.5), (21, 15), (14.5, 21.5), (3, 21.5)], closed=True, r=L(S, 0, 2.5))
    return [shell(sheet), detail(poly([(14.5, 21.5), (14.5, 15), (21, 15)])),
            kn(heart(8, 8.5, 2.6)), dot(15.5, 8, 1.7), kn(heart(8, 16, 2.6))]


@icon("nail-color-wheel", CAT, "Ring of nail tips fanned around a center circle like a polish swatch wheel",
      tags=["polish colors", "swatch", "nail salon", "manicure", "shade chart", "nail tips", "palette"])
def _(S):
    petal = rect(10, 2, 4, 6.5, L(S, 0.5, 2))
    return [shell(circle(12, 12, 2.4))] + [solid(rot(petal, i * 60)) for i in range(6)]

@icon("nail-shapes", CAT, "Four nail outlines in a grid: square, round, almond and stiletto",
      tags=["manicure", "nail salon", "nail tips", "square nails", "almond nails", "stiletto", "shapes"])
def _(S):
    k = S.r * 0.5
    return [shell(poly([(4.5, 10.5), (4.5, 3.5), (9.5, 3.5), (9.5, 10.5)], closed=True, r=k)),
            shell("M14.5 10.5V6A2.5 2.5 0 0 1 19.5 6V10.5Z"),
            shell("M4.5 21V17.5Q4.5 14.5 7 13Q9.5 14.5 9.5 17.5V21Z"),
            shell(poly([(14.5, 21), (14.5, 17), (17, 12.5), (19.5, 17), (19.5, 21)], closed=True, r=k))]

@icon("nail-dryer", CAT, "Small box dryer with a hand opening at the front and airflow lines above",
      tags=["uv lamp", "led lamp", "gel nails", "manicure", "dryer", "nail salon", "cure"])
def _(S):
    return [shell(rect(2.5, 8, 19, 13.5, L(S, 1.5, 4))), detail("M7 21.5V16.5A5 5 0 0 1 17 16.5V21.5"),
            line(seg(7, 2.5, 7, 5)), line(seg(12, 2.5, 12, 5)), line(seg(17, 2.5, 17, 5))]


@icon("painting-nails", CAT, "Fingertip with a polish brush touching the nail",
      tags=["nail polish", "manicure", "paint", "nails", "brush", "salon", "varnish"])
def _(S):
    return [shell("M6.5 21.5V9.5Q6.5 3.5 12 3.5Q17.5 3.5 17.5 9.5V21.5Z"),
            detail("M9.5 11V8.5Q9.5 6.5 12 6.5Q14.5 6.5 14.5 8.5V11Z"),
            line(seg(21.5, 3.5, 17, 9)), solid(rot(ellipse(15, 11.5, 1.3, 2.6), 50, 15, 11.5))]


@icon("clay-face-mask", CAT, "Face outline covered in speckles with the eyes clear, and a small bowl and brush beside it",
      tags=["face mask", "clay", "mud mask", "skincare", "spa", "bowl", "facial"])
def _(S):
    return [shell(face(S)),
            detail(seg(5.5, 9.5, 7, 9.5)), detail(seg(9, 9.5, 10.5, 9.5)),
            dot(5.5, 7, 0.8), dot(10.5, 7, 0.8), dot(5.5, 13, 0.8), dot(10.5, 13, 0.8),
            shell("M15.5 15.5H22A3.25 3.25 0 0 1 15.5 15.5Z"), line(seg(19, 13, 21.5, 5))]


@icon("ipl-hair-removal", CAT, "Handheld device with a wide flash window at the head and short light rays above it",
      tags=["laser", "hair removal", "light therapy", "epilator", "device", "skincare", "flash"])
def _(S):
    return [shell(rect(5, 8.5, 14, 5.5, L(S, 1, 2.75))), shell(rect(9, 14, 6, 7.5, L(S, 0, 2))),
            line(seg(12, 2.5, 12, 5.5)), line(seg(6.5, 3.5, 8, 5.5)), line(seg(17.5, 3.5, 16, 5.5))]


@icon("eyebrow-threading", CAT, "Eyebrow arc with a twisted loop of thread pulled taut across it",
      tags=["threading", "brow", "hair removal", "salon", "thread", "shaping", "beauty"])
def _(S):
    return [line("M3.5 9.5Q12 3 20.5 8.5"), line(seg(4, 14.5, 20, 21)), line(seg(4, 21, 20, 14.5)),
            dot(3.5, 14.5, 1.3), dot(3.5, 21, 1.3), dot(20.5, 14.5, 1.3), dot(20.5, 21, 1.3)]


@icon("dermaplaning-razor", CAT, "Slim handled razor with a small flat blade head, used to exfoliate the face",
      tags=["dermaplane", "facial razor", "exfoliate", "peach fuzz", "skincare", "blade", "shave"])
def _(S):
    return turn([shell(rect(9, 6.5, 6, 4.5, L(S, 0, 1.5))), solid(rect(8, 3.5, 8, 2)),
                 shell(poly([(10.5, 11), (13.5, 11), (13, 21.5), (11, 21.5)], closed=True))], 35)

@icon("cosmetic-spatula", CAT, "Tiny flat scoop resting against an open cream jar",
      tags=["spatula", "cream jar", "scoop", "skincare", "hygienic", "applicator", "cosmetic"])
def _(S):
    sp = turn([shell(ellipse(12, 5.5, 2.4, 3.2))], 40)
    return [shell(rect(2.5, 13, 12, 8.5, L(S, 1, 3))), line(seg(*rp(12, 8.5, 40), *rp(12, 21, 40)))] + sp


@icon("skin-hydration", CAT, "Wavy skin layers with a water droplet sinking into the top layer",
      tags=["moisturizer", "water", "dermis", "epidermis", "skincare", "hydrate", "droplet"])
def _(S):
    return [shell(tear(12, 8, 3)), line("M3 13.5Q7.5 11.5 12 13.5T21 13.5"), line("M3 17.5Q7.5 15.5 12 17.5T21 17.5"),
            line("M3 21Q7.5 19.5 12 21T21 21")]

@icon("glowing-skin", CAT, "Face outline with sparkles along the cheek to show a healthy glow",
      tags=["radiant", "glow", "shine", "skincare", "complexion", "beauty", "sparkle"])
def _(S):
    return [shell(face(S)),
            dot(6, 10, 1), dot(10, 10, 1), spark(18.5, 5, 2.8), spark(19.5, 12.5, 2), spark(16.5, 19, 1.8)]


@icon("face-wash", CAT, "Squeeze tube with a cluster of foam bubbles pushed out of the nozzle",
      tags=["cleanser", "foam", "face wash", "skincare", "tube", "bubbles", "cleansing"])
def _(S):
    return [shell(poly([(6.5, 21.5), (6.5, 13.5), (10, 11.5), (14, 11.5), (17.5, 13.5), (17.5, 21.5)], closed=True, r=S.r * 0.6)),
            detail(seg(6.5, 19, 17.5, 19)), shell(rect(10.5, 9.5, 3, 2)),
            dot(8.5, 6, 1.8), dot(13, 4.2, 2), dot(16.5, 7, 1.5)]


# ============================================================================ spa and salon

@icon("ultrasonic-skin-scrubber", CAT, "Handheld device with a flat angled metal spatula head and short vibration lines",
      tags=["skin spatula", "pore cleaning", "facial", "exfoliation", "esthetician", "device", "ultrasonic"])
def _(S):
    return [shell(rect(9, 12, 6, 9.5, L(S, 1, 3))),
            shell("M9.5 12V8.5Q11 4 17 3Q18 8 15 12Z"),
            line("M5.5 6.5Q4 9 5.5 11.5")]


@icon("toner-pads", CAT, "Round jar of soaked pads with a stack of pads above the rim and tweezers beside it",
      tags=["cotton pads", "toner", "exfoliating pads", "skincare", "jar", "tweezers", "cleansing"])
def _(S):
    return [shell(rect(3, 13, 14, 8.5, L(S, 1, 3.5))),
            shell(rect(4.5, 9, 11, 3.5, L(S, 0.5, 1.75))), shell(rect(5.5, 5, 9, 3.5, L(S, 0.5, 1.75))),
            line(seg(19, 3.5, 20.5, 12)), line(seg(21.5, 3.5, 20.5, 12))]


@icon("kansa-wand", CAT, "Short handle topped with a shallow metal bowl, used for soothing face massage",
      tags=["kansa", "face massage", "ayurveda", "bronze", "wand", "skincare", "spa"])
def _(S):
    return [shell(rect(9.5, 2.5, 5, 9.5, L(S, 0, 2))), shell("M3 12H21A9 8 0 0 1 3 12Z")]


@icon("shea-butter", CAT, "Split shea nut beside a small jar of butter with a scoop mark in the surface",
      tags=["shea", "nut", "butter", "moisturizer", "skincare", "natural", "african"])
def _(S):
    return [shell(ellipse(7, 9, 4.5, 6)), detail(seg(7, 4, 7, 14)),
            shell(rect(12.5, 12, 9, 9.5, L(S, 1, 3))), detail("M14.5 16Q17 13.5 19.5 16")]


@icon("face-gems", CAT, "Sticker sheet of rhinestones in star, heart and teardrop shapes",
      tags=["rhinestones", "face jewels", "festival", "glitter", "stick on", "sparkle", "makeup"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, L(S, 1.5, 4))),
            kn(heart(8, 8.5, 2.7)), kn(star(16, 8, 3.4, 1.6)), kn(tear(8, 16.5, 2.2)),
            kn(poly([(16, 13.5), (18.5, 16.5), (16, 19.5), (13.5, 16.5)], closed=True, r=S.r * 0.4))]


@icon("esthetician", CAT, "Person in a tunic holding a round facial brush, with a small cream jar at the side",
      tags=["skin therapist", "facial", "spa", "beautician", "profession", "skincare", "salon"])
def _(S):
    return [shell(circle(9.5, 7, 3.5)),
            shell("M2.5 21.5V17Q2.5 12 9.5 12Q16.5 12 16.5 17V21.5Z"), detail(seg(9.5, 13, 9.5, 21)),
            line(seg(14, 12.5, 19.5, 6.5)), solid(circle(20, 5.5, 2)),
            shell(rect(18.5, 17, 3.5, 4.5, L(S, 0, 1)))]


@icon("massage-oil", CAT, "Rounded oil bottle tipped over an open palm with a drop of oil falling",
      tags=["body oil", "massage", "spa", "aromatherapy", "pour", "oil bottle", "hand"])
def _(S):
    bottle = turn([shell(rect(9, 8, 6, 9, L(S, 1, 2.5))), shell(rect(10.5, 6, 3, 2)), shell(rect(10, 4, 4, 2))], 150, 12, 11)
    dx, dy = rp(12, 3, 150, 12, 11)
    return bottle + [solid(tear(dx, dy + 3.6, 1.1)), shell(rect(3, 18.5, 18, 3, L(S, 0, 1.5)))]


@icon("spa-headband", CAT, "Terry cloth headband with a large bow knot on top",
      tags=["headband", "towel", "face wash", "skincare", "bow", "spa", "makeup"])
def _(S):
    return [shell("M2.5 21Q2.5 8 12 8Q21.5 8 21.5 21L18 21Q18 11.5 12 11.5Q6 11.5 6 21Z"),
            shell(poly([(12, 5.5), (6.5, 2.5), (6.5, 8.5)], closed=True, r=S.r * 0.6)),
            shell(poly([(12, 5.5), (17.5, 2.5), (17.5, 8.5)], closed=True, r=S.r * 0.6))]


@icon("sauna-hat", CAT, "Felt bell shaped hat with a short rolled brim worn in the sauna to protect the head",
      tags=["felt hat", "sauna", "heat", "spa", "head protection", "wool", "bathhouse"])
def _(S):
    return [shell("M6.5 16Q6.5 4 12 4Q17.5 4 17.5 16Z"), shell(rect(3, 16, 18, 4.5, L(S, 1, 2.25)))]


@icon("vichy-shower", CAT, "Horizontal bar of downward water jets above a person lying on a treatment table",
      tags=["spa", "hydrotherapy", "shower", "massage", "treatment table", "water jets", "wellness"])
def _(S):
    return [line(seg(3, 3.5, 21, 3.5)), line(seg(7, 6.5, 7, 9.5)), line(seg(12, 6.5, 12, 9.5)), line(seg(17, 6.5, 17, 9.5)),
            shell(circle(5.5, 14.5, 2.3)), shell(rect(9.5, 12.5, 12, 4, L(S, 0, 2))),
            line(seg(2.5, 20.5, 21.5, 20.5))]


@icon("hair-color-swatch", CAT, "Metal ring holding a fan of hair locks used to choose a hair color",
      tags=["hair dye", "color chart", "salon", "shade", "colorist", "swatch ring", "hair"])
def _(S):
    lock = poly([(12, 7.5), (9.3, 21), (14.7, 21)], closed=True, r=S.r * 0.4)
    return [turn([shell(lock)], a, 12, 5)[0] for a in (-30, 0, 30)] + [shell(circle(12, 4.5, 2))]


@icon("duckbill-clip", CAT, "Long straight sectioning clip with two narrow jaws and a hinge near the back",
      tags=["hair clip", "sectioning", "salon", "styling", "hairdresser", "clamp", "beak clip"])
def _(S):
    k = S.r * 0.5
    return turn([shell(poly([(2, 10.5), (17, 7), (21.5, 8.5), (21.5, 11), (2, 11.5)], closed=True, r=k)),
                 shell(poly([(2, 13.5), (21.5, 13), (21.5, 16.5), (17, 18), (2, 14.5)], closed=True, r=k)),
                 dot(18.5, 12, 1)], -25)


@icon("satin-hair-bonnet", CAT, "Puffy round sleep bonnet with a gathered elastic band around the rim",
      tags=["hair bonnet", "sleep cap", "satin", "hair care", "night", "curls", "protective"])
def _(S):
    return [shell("M3.5 16C2 5.5 7 3.5 12 3.5C17 3.5 22 5.5 20.5 16Z"), shell(rect(2.5, 15.5, 19, 5, L(S, 1.5, 2.5))),
            detail(seg(7.5, 15.5, 7.5, 20.5)), detail(seg(12, 15.5, 12, 20.5)), detail(seg(16.5, 15.5, 16.5, 20.5))]
