"""TypeIcon Core: festivities (holiday, ritual and cultural celebration objects), batch 4."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "festivities"


def L(S, a, b):
    return a if S.name == "line" else b


def flame(x, y, h=4.0, w=1.7):
    """Small solid flame with its base centre at (x, y)."""
    return solid(f"M{fmt(x)} {fmt(y - h)}C{fmt(x + w)} {fmt(y - h * 0.4)} {fmt(x + w)} {fmt(y)} {fmt(x)} {fmt(y)}"
                 f"C{fmt(x - w)} {fmt(y)} {fmt(x - w)} {fmt(y - h * 0.4)} {fmt(x)} {fmt(y - h)}Z")


def star(cx, cy, ro, ri, n=5, rot=-90.0):
    pts = []
    for i in range(n):
        pts.append(polar(cx, cy, ro, rot + 360 / n * i))
        pts.append(polar(cx, cy, ri, rot + 360 / n * i + 180 / n))
    return pts


def P_(p):
    return f"{fmt(p[0])} {fmt(p[1])}"


def rot(pts, deg, cx=12.0, cy=12.0):
    """Rotate points clockwise on screen about (cx, cy)."""
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * sn, cy + (x - cx) * sn + (y - cy) * c) for x, y in pts]


def almond(cx, cy, length, width, ang):
    """Solid leaf shape centred at (cx, cy), long axis at ang degrees."""
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    h, w = length / 2, width / 2

    def pt(u, v):
        return f"{fmt(cx + u * ca - v * sa)} {fmt(cy + u * sa + v * ca)}"
    return f"M{pt(-h, 0)}Q{pt(0, w * 2)} {pt(h, 0)}Q{pt(0, -w * 2)} {pt(-h, 0)}Z"


def band(centre, w):
    """Closed outline polygon (points) around a centre-line polyline with half-width w and round ends."""
    n = len(centre)
    left, right = [], []
    for i, p in enumerate(centre):
        a = centre[max(i - 1, 0)]
        b = centre[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy) or 1
        nx, ny = -dy / d, dx / d
        left.append((p[0] + nx * w, p[1] + ny * w))
        right.append((p[0] - nx * w, p[1] - ny * w))

    def cap(p, q, sign):
        dx, dy = p[0] - q[0], p[1] - q[1]
        d = math.hypot(dx, dy) or 1
        dx, dy = dx / d, dy / d
        out = []
        for k in range(1, 6):
            phi = math.pi * k / 6
            nx, ny = -dy, dx
            out.append((p[0] + sign * w * (math.cos(phi) * nx) + w * math.sin(phi) * dx,
                        p[1] + sign * w * (math.cos(phi) * ny) + w * math.sin(phi) * dy))
        return out
    end = cap(centre[-1], centre[-2], 1)
    start = cap(centre[0], centre[1], -1)
    return left + end + right[::-1] + start


# ============================================================================ chunk 1

@icon("rugelach", CAT, "Crescent-shaped rolled pastry with ridges across its curve",
      tags=["rugelach", "pastry", "hanukkah", "jewish", "cookie", "crescent", "baking", "dessert"])
def _(S):
    parts = [shell("M5 18.5A8.5 8.5 0 1 1 19 18.5A7 7 0 0 0 5 18.5Z")]
    for a in (-128, -90, -52):
        o = polar(12, 13.7, 8.5, a)
        t = (12, 17.5)
        dx, dy = t[0] - o[0], t[1] - o[1]
        n = math.hypot(dx, dy)
        dx, dy = dx / n, dy / n
        # find intersection with inner circle centre (12,18.5) r 7 going from o along (dx,dy)
        best = None
        for k in range(1, 200):
            s = k * 0.05
            x, y = o[0] + dx * s, o[1] + dy * s
            if math.hypot(x - 12, y - 18.5) <= 7.0:
                best = (x, y)
                break
        parts.append(detail(seg(o[0], o[1], best[0], best[1])))
    return parts


@icon("marzipan-pig", CAT, "Front view of a round pig face with pointed ears, a snout and two eyes",
      tags=["marzipan", "pig", "lucky", "new year", "candy", "german", "sweet", "piglet"])
def _(S):
    return [
        shell(circle(12, 13.5, 8)),
        line(poly([(5.8, 9.2), (4.5, 3.8), (10, 6.2)], r=S.r)),
        line(poly([(18.2, 9.2), (19.5, 3.8), (14, 6.2)], r=S.r)),
        detail(ellipse(12, 16.2, 3.3, 2.1)),
        dot(8.6, 12, 1.0), dot(15.4, 12, 1.0),
    ]


@icon("nougat-bar", CAT, "Slab of nougat seen from the corner with wafer layers top and bottom and whole almonds between",
      tags=["nougat", "torrone", "candy", "almond", "bar", "sweet", "christmas", "confection"])
def _(S):
    return [
        shell(poly([(3, 10), (7, 5.5), (21, 5.5), (21, 15.5), (17.5, 19.5), (3, 19.5)], closed=True, r=S.r)),
        detail(poly([(3, 10), (17.5, 10), (21, 5.5)])),
        detail(seg(17.5, 10, 17.5, 19.5)),
        detail(seg(3, 16.8, 17.5, 16.8)),
        dot(7, 13.4, 1.0), dot(10.5, 13.4, 1.0), dot(14, 13.4, 1.0),
    ]


@icon("honeycomb-paper-ball", CAT, "Hanging tissue paper ball with a hexagon cell pattern and a string loop on top",
      tags=["honeycomb", "paper ball", "party", "decoration", "hanging", "tissue", "pom", "baby shower"])
def _(S):
    parts = [
        line(seg(12, 2.5, 12, 6)),
        shell(circle(12, 14, 8)),
        detail(poly(regular(12, 14, 3.6, 6), closed=True, r=0)),
    ]
    for a in (-90, -30, 30, 90, 150, 210):
        p = polar(12, 14, 3.6, a)
        q = polar(12, 14, 8, a)
        parts.append(detail(seg(p[0], p[1], q[0], q[1])))
    return parts


@icon("paper-rosette", CAT, "Round pleated paper fan decoration with folded ridges around a solid centre",
      tags=["rosette", "paper fan", "pleated", "decoration", "party", "pinwheel", "backdrop", "garland"])
def _(S):
    pts = []
    n = 12
    for i in range(n):
        pts.append(polar(12, 12, 9.5, -90 + 360 / n * i))
        pts.append(polar(12, 12, 7.3, -90 + 360 / n * i + 180 / n))
    parts = [shell(poly(pts, closed=True, r=S.r * 0.5))]
    for k in range(6):
        a = -90 + 30 + 60 * k
        p = polar(12, 12, 4.2, a)
        q = polar(12, 12, 7.3, a)
        parts.append(detail(seg(p[0], p[1], q[0], q[1])))
    parts.append(dot(12, 12, 2.0))
    return parts


@icon("table-centerpiece", CAT, "Low flower bowl on a table line with a tall candle standing on each side",
      tags=["centerpiece", "table", "flowers", "candles", "dinner", "wedding", "thanksgiving", "decor"])
def _(S):
    return [
        line(seg(2.5, 21, 21.5, 21)),
        line(seg(4.5, 10.5, 4.5, 21)),
        line(seg(19.5, 10.5, 19.5, 21)),
        flame(4.5, 8.5, 3.2, 1.3),
        flame(19.5, 8.5, 3.2, 1.3),
        shell(poly([(8, 16), (16, 16), (14.5, 21), (9.5, 21)], closed=True, r=S.r * 0.6)),
        shell(circle(12, 11.5, 3.5)),
        dot(12, 11.5, 1.0),
    ]


@icon("evergreen-garland", CAT, "Leafy swag with a pointed leaf edge hanging in a curve between two hooks",
      tags=["garland", "evergreen", "christmas", "swag", "pine", "holiday", "decoration", "mantel"])
def _(S):
    n = 14
    up, dn = [], []
    for i in range(n + 1):
        t = i / n
        x, y = 3.5 + 17 * t, 4.5 + 24 * t * (1 - t)
        up.append((x, y))
        off = 3.4 if i in (0, n) else (3.6 if i % 2 else 5.0)
        dn.append((x, y + off))
    return [
        shell(poly(up + dn[::-1], closed=True, r=S.r * 0.9)),
        dot(3.5, 2.6, 0.9), dot(20.5, 2.6, 0.9),
        dot(12, 11, 1.0),
    ]


@icon("moravian-star-lantern", CAT, "Star lantern with long spikes at the four sides and shorter spikes on the diagonals",
      tags=["moravian star", "advent star", "lantern", "christmas", "star", "froebel", "hanging", "polar"])
def _(S):
    pts = []
    for i in range(8):
        a = -90 + 45 * i
        pts.append(polar(12, 12, 10 if i % 2 == 0 else 8, a))
        pts.append(polar(12, 12, 4.5, a + 22.5))
    return [
        shell(poly(pts, closed=True, r=S.r * 0.5), stroke_miterlimit="3"),
        dot(12, 12, 1.4),
    ]


@icon("eye-of-providence", CAT, "Single eye inside an upright triangle with short rays of light above it",
      tags=["eye of providence", "all seeing eye", "triangle", "symbol", "divine", "masonic", "trinity", "rays"])
def _(S):
    return [
        shell(poly([(12, 8.5), (21, 21), (3, 21)], closed=True, r=S.r)),
        detail("M9 16.5Q12 13.5 15 16.5Q12 19.5 9 16.5"),
        dot(12, 16.5, 1.0),
        line(seg(12, 2, 12, 5)),
        line(seg(6, 4, 8, 6.3)),
        line(seg(18, 4, 16, 6.3)),
    ]


def _tomoe(a, tip):
    rad = (math.cos(math.radians(a)), math.sin(math.radians(a)))
    tan = (-rad[1], rad[0])
    c = (12 + 4.3 * rad[0], 12 + 4.3 * rad[1])
    pts = []
    for i in range(9):
        phi = math.pi * i / 8
        pts.append((c[0] + 2.1 * (math.cos(phi) * rad[0] - math.sin(phi) * tan[0]),
                    c[1] + 2.1 * (math.cos(phi) * rad[1] - math.sin(phi) * tan[1])))
    n = 10
    inner = []
    for i in range(n + 1):
        s = i / n
        w = 4.2 * (1 - s) ** 0.85 + tip * s
        inner.append(polar(12, 12, 6.4 - w, a + 135 * s))
    outer = [polar(12, 12, 6.4, a + 135 * i / n) for i in range(n + 1)]
    return pts + inner + outer[::-1]


def _mitsudomoe_filled():
    from dsl import P, ST, U
    body = [ST(circle(12, 12, 9.5), 2.5)]
    for a in (-90, 30, 150):
        body.append(P(poly(_tomoe(a, 0.0), closed=True)))
    return U(*body)


@icon("mitsudomoe", CAT, "Circle holding three comma shapes that chase each other around the centre",
      tags=["mitsudomoe", "tomoe", "japanese", "shrine", "taiko", "swirl", "symbol", "crest"],
      filled=_mitsudomoe_filled)
def _(S):
    parts = [line(circle(12, 12, 9.5))]
    for a in (-90, 30, 150):
        parts.append(shell(poly(_tomoe(a, 0.0 if S.name == "line" else 0.7), closed=True, r=0)))
    return parts


@icon("table-number-stand", CAT, "Numbered card standing in a low slotted base",
      tags=["table number", "place card", "wedding", "reception", "banquet", "stand", "sign", "seating"])
def _(S):
    return [
        line(poly([(6.5, 15), (6.5, 3), (17.5, 3), (17.5, 15)], r=S.r)),
        detail(poly([(9.5, 6.5), (14.5, 6.5), (11.5, 12)])),
        shell(rect(3, 15, 18, 6, min(S.R, 2.5))),
    ]


def _scallop(hx, hy, r, a0, a1, n):
    """Scallop shell outline with its hinge at (hx, hy) and a scalloped rim from angle a0 to a1."""
    pts = [polar(hx, hy, r, a0 + (a1 - a0) * i / n) for i in range(n + 1)]
    d = f"M{P_((hx, hy))}L{P_(pts[0])}"
    chord = 2 * r * math.sin(math.radians((a1 - a0) / n / 2))
    for p in pts[1:]:
        d += f"A{fmt(chord * 0.62)} {fmt(chord * 0.62)} 0 0 1 {P_(p)}"
    return d + "Z", pts


@icon("baptism-shell", CAT, "Scallop shell tipped to the side with a few water drops falling from its rim",
      tags=["baptism", "christening", "shell", "scallop", "water", "blessing", "church", "drops"])
def _(S):
    d, pts = _scallop(9, 15, 9, -125, -5, 5)
    parts = [shell(d), shell(poly([(6.8, 15.5), (11.2, 15.5), (10.3, 18.5), (7.7, 18.5)], closed=True, r=S.r * 0.4))]
    for p in pts[1:-1]:
        ang = math.degrees(math.atan2(p[1] - 15, p[0] - 9))
        q = polar(9, 15, 3.5, ang)
        r = polar(9, 15, 6.3, ang)
        parts.append(detail(seg(q[0], q[1], r[0], r[1])))
    parts.append(solid("M19.5 16.5C20.8 18.3 20.8 19.5 19.5 20C18.2 19.5 18.2 18.3 19.5 16.5Z"))
    parts.append(solid("M15.3 18.5C16.3 19.8 16.3 20.8 15.3 21.2C14.3 20.8 14.3 19.8 15.3 18.5Z"))
    return parts


@icon("fan-bunting", CAT, "Half-circle pleated bunting with stripes fanning out from a round rosette at the top",
      tags=["bunting", "fan", "semicircle", "party", "decoration", "fourth of july", "parade", "pleated"])
def _(S):
    parts = [shell("M2 7H22A10 10 0 0 1 2 7Z" if S.name == "line" else
                   "M4 7H20Q22.5 7 21.9 9.2A10 10 0 0 1 2.1 9.2Q1.5 7 4 7Z")]
    for a in (45, 77, 103, 135):
        p = polar(12, 7, 10, a)
        parts.append(detail(seg(12, 7, p[0], p[1])))
    parts.append(dot(12, 7, 2.0))
    return parts


@icon("christmas-light-bulb", CAT, "Upright flame-shaped holiday bulb with a screw base, wire either side and glow rays",
      tags=["christmas lights", "bulb", "fairy lights", "string lights", "holiday", "lamp", "glow", "decoration"])
def _(S):
    return [
        shell(poly([(12, 2.5), (16, 8), (17, 12.5), (14.5, 16.5), (9.5, 16.5), (7, 12.5), (8, 8)], closed=True, r=S.r + 2)),
        shell(rect(9, 16.5, 6, 3.5, min(S.R, 1.2))),
        line(seg(2.5, 18.3, 9, 18.3)),
        line(seg(15, 18.3, 21.5, 18.3)),
        line(seg(3.8, 5, 5.5, 6.6)),
        line(seg(20.2, 5, 18.5, 6.6)),
    ]


@icon("elf-shoes", CAT, "Side view of an elf boot with a cuffed shaft and a long toe curling up to a small bell",
      tags=["elf", "shoe", "boot", "curled toe", "jester", "christmas", "costume", "bell"])
def _(S):
    return [
        shell(poly([(4, 6.5), (11, 6.5), (11, 12), (13.5, 13), (17, 13.3), (20, 12), (20, 15), (18, 18.5), (14, 20), (4, 20)],
                   closed=True, r=S.r)),
        detail(seg(4, 9.8, 11, 9.8)),
        detail(seg(4, 17, 14, 17)),
        line(seg(20, 12, 20.6, 9.5)),
        shell(circle(20.6, 7.5, 1.8)),
    ]

# ============================================================================ chunk 2

@icon("christmas-list", CAT, "Paper list with a star on top and check marks beside three short lines",
      tags=["christmas list", "wish list", "santa", "checklist", "naughty or nice", "scroll", "letter", "holiday"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, min(S.R, 3))),
        solid(poly(star(12, 6.4, 2.3, 1.0), closed=True)),
        detail(poly([(7.6, 11), (8.6, 12), (10.2, 10)])),
        detail(seg(12.3, 11, 16.2, 11)),
        detail(poly([(7.6, 15), (8.6, 16), (10.2, 14)])),
        detail(seg(12.3, 15, 16.2, 15)),
        detail(poly([(7.6, 19), (8.6, 20), (10.2, 18)])) if False else detail(seg(7.8, 18.8, 16.2, 18.8)),
    ]


@icon("pomander", CAT, "Round orange studded with cloves and tied with a crossing ribbon and a hanging loop",
      tags=["pomander", "orange", "cloves", "christmas", "ribbon", "scent", "tudor", "spice"])
def _(S):
    return [
        line(poly([(12, 7), (9.6, 4.6), (12, 2.2), (14.4, 4.6)], closed=True, r=S.r * 1.2)),
        shell(circle(12, 14.2, 7.6)),
        detail(seg(12, 6.6, 12, 21.8)),
        detail("M4.4 14.2H19.6"),
        dot(8.2, 10.4, 0.9), dot(15.8, 10.4, 0.9), dot(8.2, 18, 0.9), dot(15.8, 18, 0.9),
    ]


@icon("kissing-ball", CAT, "Round ball of leaves hanging from a ribbon bow with berries tucked in",
      tags=["kissing ball", "mistletoe", "greenery", "christmas", "hanging", "wreath", "bow", "holiday"])
def _(S):
    n = 9
    pts = [polar(12, 14, 6.3, -90 + 360 / n * i) for i in range(n + 1)]
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for p in pts[1:]:
        d += f"A2.6 2.6 0 0 1 {fmt(p[0])} {fmt(p[1])}"
    return [
        line(seg(12, 1.8, 12, 4.2)),
        shell(poly([(12, 5), (7.8, 2.8), (7.8, 7.2)], closed=True, r=S.r * 0.6)),
        shell(poly([(12, 5), (16.2, 2.8), (16.2, 7.2)], closed=True, r=S.r * 0.6)),
        shell(d + "Z"),
        dot(9.8, 14.6, 1.0), dot(14.4, 12.6, 1.0), dot(13.6, 17.4, 0.9),
    ]


@icon("st-nicholas-shoe", CAT, "Wooden clog with an orange and a candy cane poking out of its opening",
      tags=["st nicholas", "shoe", "clog", "candy cane", "orange", "december 6", "gifts", "sinterklaas"])
def _(S):
    return [
        shell(poly([(3, 12.5), (13.5, 12.5), (14.5, 15), (19.5, 15.8), (21.5, 18.5), (21.5, 20.5), (3, 20.5)], closed=True, r=S.r)),
        detail(seg(3, 17.3, 17.5, 17.3)),
        shell(circle(6.6, 8.6, 2.5)),
        line("M11.8 12.5V5a2.3 2.3 0 0 1 4.6 0"),
    ]


@icon("woven-heart-basket", CAT, "Heart-shaped paper basket with a crisscross woven pattern and a wide arched handle",
      tags=["woven heart", "basket", "danish", "paper heart", "christmas", "julehjerter", "weaving", "ornament"])
def _(S):
    return [
        line("M3.6 12C2 1 22 1 20.4 12"),
        shell("M12 21.5C3 16.3 3.6 10.8 7.6 10.6C10 10.5 11.6 11.8 12 12.8C12.4 11.8 14 10.5 16.4 10.6C20.4 10.8 21 16.3 12 21.5Z"),
        detail(seg(8, 13.2, 14, 18.6)),
        detail(seg(16, 13.2, 10, 18.6)),
    ]


@icon("lucia-bun", CAT, "S-shaped curled sweet bun with a raisin pressed into each coiled end",
      tags=["lucia bun", "saffron bun", "lussekatter", "swedish", "st lucia", "sweet roll", "baking", "raisin"])
def _(S):
    c = []
    for i in range(0, 17):
        th = math.radians(-10 - (i / 16) * 260)
        c.append((12 + 3.6 * math.cos(th), 8.8 + 3.6 * math.sin(th)))
    for i in range(1, 17):
        th = math.radians(-90 + (i / 16) * 260)
        c.append((12 + 3.6 * math.cos(th), 15.6 + 3.6 * math.sin(th)))
    e1, e2 = c[0], c[-1]
    return [
        shell(poly(band(c, 2.5), closed=True, r=0)),
        dot(e1[0] - 0.2, e1[1] + 0.2, 0.0001) if False else dot(c[2][0] - 0.5, c[2][1], 0.8),
        dot(c[-3][0] + 0.5, c[-3][1], 0.8),
    ]


@icon("snowball-lantern", CAT, "Mound of packed snowballs with an arched opening and a candle flame glowing inside",
      tags=["snowball lantern", "snow", "candle", "winter", "luminary", "glow", "swedish", "snow lantern"])
def _(S):
    return [
        shell("M3 20.5C5 12 9 7 12 3.5C15 7 19 12 21 20.5Z" if S.name == "line" else
              "M3 20.5C3 12 7.5 3.5 12 3.5C16.5 3.5 21 12 21 20.5Z"),
        detail("M6 10.8Q12 13.6 18 10.8"),
        detail("M9 20.5V17.3a3 3 0 0 1 6 0V20.5"),
        flame(12, 19, 3.4, 1.4),
    ]


@icon("hanukkah-oil-jug", CAT, "Round-bellied oil jug with a narrow neck, a flared rim and one handle",
      tags=["hanukkah", "oil jug", "cruse", "menorah", "miracle", "olive oil", "pitcher", "jewish"])
def _(S):
    return [
        shell(poly([(8.6, 2.6), (15.4, 2.6), (13.6, 5.6), (13.6, 8.6), (10.4, 8.6), (10.4, 5.6)], closed=True, r=S.r * 0.6)),
        shell(ellipse(12, 15.2, 6.2, 6.6)),
        line("M14 5.4C21 5.4 21.5 12 18 13.6"),
    ]


@icon("rose-water-sprinkler", CAT, "Bottle with a flat base, round belly and very long neck, its perforated cap sprinkling drops",
      tags=["rose water", "sprinkler", "gulabdani", "perfume", "bottle", "guest", "drops", "eid"])
def _(S):
    return [
        shell(poly([(10.5, 5.5), (13.5, 5.5), (13.5, 11), (17, 14), (17.5, 19), (16, 21.5), (8, 21.5), (6.5, 19), (7, 14), (10.5, 11)],
                   closed=True, r=S.r + 1)),
        shell(rect(9, 2.5, 6, 3, min(S.R, 1.2))),
        dot(6.4, 3.4, 0.9), dot(17.6, 3.4, 0.9), dot(4.4, 7, 0.9), dot(19.6, 7, 0.9),
    ]


@icon("lamp-pillar", CAT, "Tall column topped by a lamp bowl and flame, with small lamps on alternating sides",
      tags=["lamp pillar", "deepstambh", "diya", "temple", "diwali", "lights", "column", "festival"])
def _(S):
    parts = [
        flame(12, 5.6, 3.6, 1.5),
        shell(poly([(7, 6.2), (17, 6.2), (14.6, 10.3), (9.4, 10.3)], closed=True, r=S.r)),
        shell(rect(10.6, 10.3, 2.8, 9.7, 0)),
        shell(rect(7, 19.5, 10, 2.5, min(S.R, 1))),
    ]
    for y, side in ((13, -1), (16.5, 1)):
        x0 = 10.6 if side < 0 else 13.4
        x1 = x0 + side * 3.8
        parts.append(line(seg(x0, y, x1, y)))
        parts.append(dot(x1, y, 1.5))
    return parts


@icon("victory-banner", CAT, "Pole topped with a small round finial and a pleated fabric banner hanging from it",
      tags=["victory banner", "dhvaja", "gyaltsen", "flag", "pennant", "buddhist", "pole", "standard"])
def _(S):
    return [
        line(seg(5, 5, 5, 21.5)),
        dot(5, 3, 1.4),
        shell(poly([(5, 6), (19.5, 6), (19.5, 18), (16.4, 15.3), (12.7, 18), (9.2, 15.3), (5, 18)], closed=True, r=S.r * 0.5)),
        detail(seg(9.2, 6, 9.2, 12)),
        detail(seg(14.2, 6, 14.2, 12)),
    ]


@icon("chinese-papercut", CAT, "Round paper cutting with a scalloped edge, four cut-out petals and a centre hole",
      tags=["papercut", "paper cutting", "jianzhi", "window flower", "lunar new year", "craft", "chinese", "cut paper"])
def _(S):
    n = 12
    d = ""
    pts = [polar(12, 12, 9.4, 360 / n * i) for i in range(n + 1)]
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for p in pts[1:]:
        d += f"A2.4 2.4 0 0 1 {fmt(p[0])} {fmt(p[1])}"
    parts = [shell(d + "Z")]
    for a in (-90, 0, 90, 180):
        c = polar(12, 12, 4.8, a)
        rad = polar(0, 0, 1, a)
        tan = (-rad[1], rad[0])
        pts4 = [(c[0] + rad[0] * 2.3, c[1] + rad[1] * 2.3), (c[0] + tan[0] * 1.7, c[1] + tan[1] * 1.7),
                (c[0] - rad[0] * 2.3, c[1] - rad[1] * 2.3), (c[0] - tan[0] * 1.7, c[1] - tan[1] * 1.7)]
        parts.append(detail(poly(pts4, closed=True, r=0)))
    parts.append(dot(12, 12, 1.0))
    return parts


def _hole(cx, cy, r):
    """Circle drawn the opposite way round so it cuts a hole in a compound path."""
    return (f"M{fmt(cx - r)} {fmt(cy)}A{fmt(r)} {fmt(r)} 0 1 1 {fmt(cx + r)} {fmt(cy)}"
            f"A{fmt(r)} {fmt(r)} 0 1 1 {fmt(cx - r)} {fmt(cy)}Z")


@icon("jade-bi-disc", CAT, "Flat jade disc with a round hole in the centre and a ring of small raised dots",
      tags=["jade", "bi disc", "chinese", "ceremonial", "amulet", "ring stone", "heaven", "ancient"])
def _(S):
    hr = 2.8 if S.name == "line" else 3.4
    dr = 0.8 if S.name == "line" else 1.1
    parts = [shell(circle(12, 12, 9.6) + _hole(12, 12, hr))]
    for i in range(9):
        p = polar(12, 12, 6.6, -90 + 40 * i)
        parts.append(dot(p[0], p[1], dr))
    return parts


@icon("longevity-peach-bun", CAT, "Peach-shaped steamed bun with a pointed tip, a crease line and two leaves on top",
      tags=["longevity peach", "shoutao", "peach bun", "birthday", "chinese", "steamed bun", "dim sum", "auspicious"])
def _(S):
    return [
        shell("M12 7C15.5 9 20.5 10.5 20 15.3C19.6 19.5 16 21.5 12 21.5C8 21.5 4.4 19.5 4 15.3C3.5 10.5 8.5 9 12 7Z" if S.name == "line" else
              "M12 7.6C15.5 8.6 20.5 10.5 20 15.3C19.6 19.5 16 21.5 12 21.5C8 21.5 4.4 19.5 4 15.3C3.5 10.5 8.5 8.6 12 7.6Z"),
        detail("M12 8.5C10 12.5 10.3 17 12.5 21"),
        solid(almond(16.5, 4.6, 6, 1.5, -25)),
        solid(almond(7.6, 5, 5, 1.3, 30)),
    ]

# ============================================================================ chunk 3

@icon("lucky-arrow", CAT, "Diagonal ceremonial arrow with fletching at the tail and a small bell tied near the tip",
      tags=["lucky arrow", "hamaya", "new year", "shrine", "charm", "bell", "good luck", "japanese"])
def _(S):
    def rp(pts, closed=False, r=0.0):
        return poly(rot(pts, 45), closed=closed, r=r)
    cx, cy = rot([(15.6, 9.6)], 45)[0]
    return [
        line(rp([(12, 6), (12, 21)])),
        shell(rp([(12, 2), (9.4, 7.2), (14.6, 7.2)], closed=True, r=S.r * 0.6)),
        shell(rp([(12, 14.5), (9, 16.5), (9, 21.5), (12, 19.5)], closed=True, r=S.r * 0.4)),
        shell(rp([(12, 14.5), (15, 16.5), (15, 21.5), (12, 19.5)], closed=True, r=S.r * 0.4)),
        shell(circle(cx, cy, 1.9)),
        line(rp([(12, 10), (13.9, 9.9)])),
    ]


@icon("lucky-rake-charm", CAT, "Bamboo rake charm with curved tines fanning up from a bound handle and a small mask in the middle",
      tags=["kumade", "rake", "lucky charm", "tori no ichi", "japanese", "fortune", "okame", "market"])
def _(S):
    return [
        line(seg(12, 15.5, 12, 21.5)),
        line("M6.2 16.3Q12 19 17.8 16.3"),
        line("M6.5 16.5C4 13 3.5 8.5 5 5"),
        line("M9.7 17C8.5 12.5 8.5 8 9 4.2"),
        line("M14.3 17C15.5 12.5 15.5 8 15 4.2"),
        line("M17.5 16.5C20 13 20.5 8.5 19 5"),
        shell(circle(12, 10.5, 2.2)),
    ]


@icon("bean-throwing-box", CAT, "Square wooden measuring box heaped with roasted beans and a few beans scattered beside it",
      tags=["masu", "setsubun", "beans", "soybeans", "box", "japanese", "mamemaki", "winter"])
def _(S):
    parts = [
        shell(rect(2.8, 13.5, 14.4, 8, min(S.R, 3.4))),
    ]
    for (x, y, a) in ((6.2, 10, 20), (9.8, 8.6, -25), (13.6, 10, 35), (8, 12, -40), (11.8, 12, 10)):
        parts.append(solid(almond(x, y, 3.6, 2.0, a)))
    for (x, y, a) in ((20, 11.5, 30), (20.8, 16, -30), (20.2, 20, 70)):
        parts.append(solid(almond(x, y, 3.6, 2.0, a)))
    return parts


@icon("festival-tower", CAT, "Wooden festival tower with a roof, a drum on top, cross braces and lanterns hanging either side",
      tags=["yagura", "tower", "obon", "matsuri", "drum tower", "lanterns", "scaffold", "summer festival"])
def _(S):
    return [
        line(poly([(4, 9), (12, 3), (20, 9)], r=S.r)),
        shell(rect(9.4, 6.2, 5.2, 3.4, min(S.R, 1))),
        line(seg(6.5, 10.5, 17.5, 10.5)),
        line(seg(7.5, 10.5, 6, 21.5)),
        line(seg(16.5, 10.5, 18, 21.5)),
        line(seg(7.3, 12, 16.7, 20)),
        line(seg(16.7, 12, 7.3, 20)),
        line(seg(4, 9, 3.2, 12)),
        line(seg(20, 9, 20.8, 12)),
        dot(3.2, 13.6, 1.4), dot(20.8, 13.6, 1.4),
    ]


@icon("goldfish-scoop", CAT, "Round paper scoop with a short handle lifting a small goldfish with water drops",
      tags=["goldfish scooping", "kingyo sukui", "festival game", "poi", "carnival", "fish", "japanese", "summer"])
def _(S):
    return [
        shell(circle(14.2, 13.8, 5.2)),
        line(seg(17.9, 17.5, 21.5, 21)),
        shell(ellipse(7.6, 7, 3.8, 2.3)),
        shell(poly([(4, 7), (2.2, 5), (2.2, 9)], closed=True, r=S.r * 0.4)),
        dot(9, 6.4, 0.8),
        dot(13, 5, 0.9), dot(17, 4, 0.9), dot(5, 15, 0.9), dot(7.5, 19, 0.9),
    ]


@icon("lucky-pouch", CAT, "Small round drawstring pouch with gathered neck, a tied cord with loose ends and a ring emblem",
      tags=["lucky bag", "omamori", "fukubukuro", "pouch", "drawstring", "charm", "sachet", "new year"])
def _(S):
    return [
        shell("M8 10.5C3.5 12.5 3 18 6.5 20.5C9 22 15 22 17.5 20.5C21 18 20.5 12.5 16 10.5Z"),
        shell(poly([(8, 10.5), (6.6, 3.5), (17.4, 3.5), (16, 10.5)], closed=True, r=S.r * 0.6)),
        detail(seg(10.6, 3.5, 10.2, 8)),
        detail(seg(13.4, 3.5, 13.8, 8)),
        line(seg(7.5, 10.5, 16.5, 10.5)),
        line("M16.5 10.5C19.5 10.5 20 13 19.8 14.5"),
        line("M7.5 10.5C4.5 10.5 4 13 4.2 14.5"),
        detail(circle(12, 16, 2.4)),
    ]


@icon("flower-offering-tray", CAT, "Shallow square palm-leaf tray holding heaped flower petals and a lit incense stick",
      tags=["canang sari", "offering", "bali", "flowers", "tray", "incense", "palm leaf", "temple"])
def _(S):
    return [
        shell(poly([(2.5, 15.5), (21.5, 15.5), (20, 20.5), (4, 20.5)], closed=True, r=S.r * 0.6)),
        dot(6.6, 12.6, 2.0), dot(11.2, 11.4, 2.0), dot(15.8, 12.6, 2.0),
        line(seg(18, 12.4, 20.8, 3.6)),
        dot(21, 3, 1.0),
    ]


@icon("confetti-egg", CAT, "Egg with a jagged crack across its upper part and confetti bursting out above it",
      tags=["cascaron", "confetti egg", "easter", "egg", "party", "confetti", "tissue", "celebration"])
def _(S):
    return [
        shell("M12 6C15 8 19 11.5 19 15.5C19 19.3 15.9 21.6 12 21.6C8.1 21.6 5 19.3 5 15.5C5 11.5 9 8 12 6Z" if S.name == "line" else
              "M12 6.4C15.5 6.4 19 11.5 19 15.5C19 19.3 15.9 21.6 12 21.6C8.1 21.6 5 19.3 5 15.5C5 11.5 8.5 6.4 12 6.4Z"),
        detail(poly([(6.2, 12.6), (8.8, 10.8), (11, 13.2), (13.4, 10.8), (15.4, 13.2), (17.8, 11.6)])),
        dot(7.2, 3.4, 0.9), dot(12, 2.6, 0.9), dot(16.8, 3.4, 0.9), dot(20, 6.6, 0.9), dot(4, 6.6, 0.9),
    ]


@icon("fly-whisk", CAT, "Ceremonial whisk with a short handle and a long plume of hair strands streaming from its tip",
      tags=["fly whisk", "chowry", "chamara", "ceremonial", "plume", "yak hair", "temple", "whisk"])
def _(S):
    return [
        line(seg(4.6, 21, 9.2, 13.6)),
        dot(9.4, 13.3, 1.7),
        line("M9.4 13.3C8.5 8.5 13 4.5 20.5 3.6"),
        line("M9.4 13.3C11 9.6 16 8.3 21.5 8.6"),
        line("M9.4 13.3C12.5 12.3 17.5 13 21.5 14.2"),
        line("M9.4 13.3C12 15.6 16 18.4 20 19"),
    ]


@icon("processional-cross", CAT, "Ornate cross with round ends and a medallion at the centre mounted on a tall staff",
      tags=["processional cross", "church", "crucifer", "staff", "procession", "easter", "religious", "lent"])
def _(S):
    return [
        line(seg(12, 4, 12, 15)),
        line(seg(6.6, 8.6, 17.4, 8.6)),
        dot(12, 2.8, 1.6), dot(6, 8.6, 1.6), dot(18, 8.6, 1.6),
        shell(circle(12, 8.6, 2.3)),
        shell(circle(12, 16.3, 1.4)),
        line(seg(12, 17.7, 12, 21.6)),
    ]


# ============================================================================ chunk 4

@icon("akuaba-doll", CAT, "Carved standing figure with a large flat disc head, ringed neck, short arms and a column body",
      tags=["akuaba", "fertility doll", "ghana", "african", "carved figure", "wooden doll", "ritual", "asante"])
def _(S):
    return [
        shell(circle(12, 6.6, 4.6)),
        dot(10.2, 6, 0.9), dot(13.8, 6, 0.9),
        detail(seg(10.6, 8.6, 13.4, 8.6)),
        shell(rect(9.8, 12.4, 4.4, 8.4, min(S.R, 1.5))),
        detail(seg(9.8, 14.2, 14.2, 14.2)),
        line(poly([(9.8, 14.6), (6.4, 15.4), (6.4, 19)], r=S.r)),
        line(poly([(14.2, 14.6), (17.6, 15.4), (17.6, 19)], r=S.r)),
    ]


@icon("sweetgrass-braid", CAT, "Twisted braid of grass strands tied with a band at the top and loose ends at the bottom",
      tags=["sweetgrass", "braid", "smudge", "indigenous", "ceremony", "grass", "herb", "plait"])
def _(S):
    n = 24
    a, b = [], []
    for i in range(n + 1):
        y = 5 + 11.5 * i / n
        ph = math.pi * 2 * i / n * 2.0
        a.append((12 + 3.4 * math.sin(ph), y))
        b.append((12 - 3.4 * math.sin(ph), y))
    return [
        line(poly(a, r=0)),
        line(poly(b, r=0)),
        line(seg(8, 3.6, 16, 3.6)),
        line(seg(8, 17.8, 16, 17.8)),
        line("M9.4 18C8.8 19.6 7.8 20.8 6.6 21.6"),
        line(seg(12, 18, 12, 21.8)),
        line("M14.6 18C15.2 19.6 16.2 20.8 17.4 21.6"),
    ]


@icon("confetti-balloon", CAT, "Clear round balloon filled with small confetti pieces on a curly string",
      tags=["confetti balloon", "party", "birthday", "clear balloon", "celebration", "helium", "decoration", "latex"])
def _(S):
    return [
        shell(poly([(12, 2.5), (17, 4.5), (18.6, 9.5), (16.6, 14.2), (12, 17), (7.4, 14.2), (5.4, 9.5), (7, 4.5)], closed=True, r=S.r + 3)),
        solid(poly([(12, 17), (10.4, 19), (13.6, 19)], closed=True)),
        line("M12 19Q9.5 20.4 12 21.4"),
        dot(9.4, 8, 0.85), dot(13.6, 6.4, 0.85), dot(14.6, 10.6, 0.85), dot(10.8, 11.6, 0.85), dot(8.6, 12.4, 0.0001) if False else dot(12.4, 8.8, 0.7),
    ]


@icon("lipstick-kiss", CAT, "Pair of lips imprint with a centre line and short marks around it",
      tags=["lipstick kiss", "kiss mark", "lips", "kiss print", "romance", "valentine", "cosmetics", "xoxo"])
def _(S):
    return [
        shell("M2.8 13C6 7 9 7 12 9.5C15 7 18 7 21.2 13C18 19 6 19 2.8 13Z"),
        detail("M3.2 13.2Q12 15 20.8 13.2"),
        line(seg(4, 4.2, 5.6, 6)),
        line(seg(20, 4.2, 18.4, 6)),
        line(seg(12, 2.4, 12, 4.6)),
    ]


@icon("tree-heart-carving", CAT, "Tree trunk with a round cut top and roots, a heart and two marks carved into its bark",
      tags=["tree carving", "heart", "initials", "lovers", "love", "bark", "romance", "carved heart"])
def _(S):
    return [
        shell("M6.5 4.5A5.5 2 0 0 0 17.5 4.5L16.6 17L20.5 21.5H3.5L7.4 17Z"),
        line("M6.5 4.5A5.5 2 0 0 1 17.5 4.5"),
        detail("M12 14.4C9 12.2 9 9 10.6 8.6C11.4 8.4 11.9 9 12 9.6C12.1 9 12.6 8.4 13.4 8.6C15 9 15 12.2 12 14.4Z"),
        detail(seg(10, 16.8, 10, 18.8)),
        detail(seg(14, 16.8, 14, 18.8)),
    ]


@icon("draped-cross", CAT, "Wooden cross with a cloth draped over the crossbar and hanging down both sides",
      tags=["draped cross", "good friday", "lent", "easter", "church", "cross", "cloth", "holy week"])
def _(S):
    return [
        line(seg(12, 2.3, 12, 21.7)),
        line(seg(2.6, 6.8, 21.4, 6.8)),
        shell(poly([(4.6, 8.2), (9.4, 8.2), (9.4, 18.4), (7, 16.6), (4.6, 18.4)], closed=True, r=S.r * 0.6)),
        shell(poly([(14.6, 8.2), (19.4, 8.2), (19.4, 18.4), (17, 16.6), (14.6, 18.4)], closed=True, r=S.r * 0.6)),
    ]


@icon("hymn-number-board", CAT, "Wooden board with an arched top holding rows of slotted number cards",
      tags=["hymn board", "hymn numbers", "church", "chapel", "sign board", "service", "number board", "worship"])
def _(S):
    parts = [shell("M4.5 21.5V10A7.5 7.5 0 0 1 19.5 10V21.5Z" if S.name == "line" else
                   "M4.5 20Q4.5 21.5 6 21.5H18Q19.5 21.5 19.5 20V10A7.5 7.5 0 0 0 4.5 10Z")]
    for y in (9.6, 15.4):
        parts.append(detail(rect(7.6, y, 3.6, 3.6, 0)))
        parts.append(detail(rect(12.8, y, 3.6, 3.6, 0)))
    return parts


@icon("offering-plate", CAT, "Shallow round collection plate on a short foot holding coins and an envelope",
      tags=["offering plate", "collection plate", "church", "donation", "tithe", "alms", "coins", "envelope"])
def _(S):
    return [
        shell("M2.8 12.5H21.2C21.2 17 17.4 19.6 12 19.6C6.6 19.6 2.8 17 2.8 12.5Z"),
        line(seg(12, 19.6, 12, 21.6)),
        dot(6.6, 9.4, 1.8), dot(10.6, 8.4, 1.5),
        shell(rect(13.6, 5.4, 6, 4.6, min(S.R, 1))),
        detail(poly([(13.6, 5.4), (16.6, 8), (19.6, 5.4)])),
    ]


@icon("ahimsa-hand", CAT, "Raised open palm with four fingers, a thumb and a small wheel drawn in the centre of the palm",
      tags=["ahimsa", "jain", "palm", "non-violence", "hand", "wheel", "chakra", "symbol"])
def _(S):
    return [
        shell(rect(6.5, 12.5, 11, 9, min(S.R, 3))),
        line(seg(8.4, 12.5, 8.4, 6)),
        line(seg(11.5, 12.5, 11.5, 3.6)),
        line(seg(14.6, 12.5, 14.6, 3.6)),
        line(seg(17.5, 12.5, 17.5, 6.2)) if False else line(seg(17.4, 13.5, 17.4, 7)),
        line(poly([(6.5, 16.5), (3.6, 14.6), (3, 12)], r=S.r)),
        detail(circle(12, 17, 2.2)),
    ]


@icon("sacred-fire-urn", CAT, "Stemmed metal urn with a wide mouth holding a tall flame",
      tags=["sacred fire", "urn", "zoroastrian", "fire temple", "atash", "flame", "altar", "vessel"])
def _(S):
    return [
        flame(12, 10, 8, 3.2),
        shell("M5.8 10.4H18.2C18.2 14.6 15.6 16.6 12 16.6C8.4 16.6 5.8 14.6 5.8 10.4Z"),
        line(seg(12, 16.6, 12, 19.4)),
        shell(poly([(7.4, 21.6), (9.8, 19.4), (14.2, 19.4), (16.6, 21.6)], closed=True, r=S.r * 0.5)),
    ]


@icon("groundbreaking-shovel", CAT, "Shovel with a bow tied on its handle pushed into a small mound of earth",
      tags=["groundbreaking", "shovel", "ceremony", "construction", "ribbon", "spade", "dedication", "first dig"])
def _(S):
    return [
        line(seg(9, 2.8, 15, 2.8)),
        line(seg(12, 2.8, 12, 12)),
        solid(poly([(12, 7), (8, 5), (8, 9)], closed=True)),
        solid(poly([(12, 7), (16, 5), (16, 9)], closed=True)),
        line(poly([(8.4, 17), (8.4, 12), (15.6, 12), (15.6, 17)], r=S.r)),
        line("M2.5 21.6C5 17.6 9 16.8 12 16.8C15 16.8 19 17.6 21.5 21.6"),
    ]


@icon("ship-christening", CAT, "Ship hull with a bottle on a rope swinging in to smash against it in a splash",
      tags=["ship christening", "ship launch", "champagne", "bottle", "naming ceremony", "shipyard", "boat", "launch"])
def _(S):
    cx, cy = 15.6, 9.6
    body = rot([(cx - 1.6, cy - 2.6), (cx + 1.6, cy - 2.6), (cx + 1.6, cy + 2.6), (cx - 1.6, cy + 2.6)], -45, cx, cy)
    n0 = rot([(cx, cy - 2.6)], -45, cx, cy)[0]
    n1 = rot([(cx, cy - 6.4)], -45, cx, cy)[0]
    return [
        shell(poly([(2.5, 15.5), (21.5, 15.5), (18, 21), (6, 21)], closed=True, r=S.r)),
        shell(poly(body, closed=True, r=S.r * 0.4)),
        line(poly([n0, n1, (3.5, 3)])),
        line(seg(19.8, 12.6, 21.4, 11)),
        line(seg(20.6, 13.6, 22, 13.6)) if False else line(seg(21.4, 13.6, 22.4, 13.6)),
    ]


@icon("statue-unveiling", CAT, "Tall statue shape under a draped cloth on a pedestal with a pull cord and tassel",
      tags=["unveiling", "statue", "monument", "memorial", "dedication", "cloth", "ceremony", "reveal"])
def _(S):
    return [
        shell("M12 3C15 3 16 6 16 8.4C16 11.5 18.6 13 18.6 18H5.4C5.4 13 8 11.5 8 8.4C8 6 9 3 12 3Z"),
        detail("M10.4 9.5C10 12.5 9.6 14.5 9.4 18"),
        detail("M14 9.5C14.3 12 14.6 14.5 14.8 18"),
        shell(rect(3.5, 18, 17, 3.6, min(S.R, 1.2))),
        line("M16 5C19 3.4 20.6 6 20.5 10"),
        dot(20.5, 11.8, 1.1),
    ]


@icon("raffle-drum", CAT, "Wire mesh barrel drum on a stand with a crank handle at one end",
      tags=["raffle drum", "tombola", "lottery", "draw", "tickets", "bingo", "prize draw", "crank"])
def _(S):
    return [
        shell(rect(3, 4.5, 14.5, 11, min(S.R, 4))),
        detail(seg(8, 4.5, 8, 15.5)),
        detail(seg(12.4, 4.5, 12.4, 15.5)),
        line(seg(17.5, 10, 20.5, 10)),
        line(seg(20.5, 7, 20.5, 13)),
        line(seg(6, 15.5, 4.2, 21.5)),
        line(seg(14.5, 15.5, 16.3, 21.5)),
        line(seg(3, 21.5, 17.5, 21.5)),
    ]


@icon("prize-wheel", CAT, "Upright spinning wheel cut into wedge segments on a base with a pointer flag at the top",
      tags=["prize wheel", "spin the wheel", "wheel of fortune", "game", "carnival", "raffle", "segments", "pointer"])
def _(S):
    parts = [
        solid(poly([(10.4, 1.8), (13.6, 1.8), (12, 5.6)], closed=True)),
        shell(circle(12, 12.2, 7.4)),
        dot(12, 12.2, 1.2),
        line(seg(12, 19.6, 12, 21.6)),
        line(seg(7, 21.6, 17, 21.6)),
    ]
    for a in (-90, -30, 30, 90, 150, 210):
        p = polar(12, 12.2, 2.2, a)
        q = polar(12, 12.2, 7.4, a)
        parts.append(detail(seg(p[0], p[1], q[0], q[1])))
    return parts


# ============================================================================ chunk 5

@icon("fortune-sticks", CAT, "Tall bamboo cup full of thin sticks with one stick sliding out of the top",
      tags=["fortune sticks", "kau cim", "chien tung", "divination", "temple", "oracle", "lots", "bamboo"])
def _(S):
    return [
        shell(rect(6.5, 12, 11, 9.5, min(S.R, 2.6))),
        detail(seg(6.5, 16, 17.5, 16)),
        line(seg(9, 12, 8.4, 5)),
        line(seg(12, 12, 12, 4)),
        line(seg(15, 12, 15.6, 5)),
        line(seg(10.5, 9.5, 12.8, 1.8)) if False else line(seg(17.4, 12, 19.6, 2.4)),
    ]


@icon("ribbon-wand", CAT, "Short stick with long ribbons streaming from its tip in curls",
      tags=["ribbon wand", "rhythmic gymnastics", "streamer", "dance", "twirl", "festival", "ribbon stick", "performance"])
def _(S):
    return [
        line(seg(4.2, 21.6, 10.6, 13.6)),
        dot(4.4, 21.3, 1.3),
        line("M10.6 13.6C9.6 8 12 4 16.4 4.6C19.8 5.2 19.6 9 16.8 9.4"),
        line("M10.6 13.6C13.4 11.4 17.4 13.2 19.2 16.8C20.4 19.6 17.8 21.2 16.2 19.8"),
        line("M10.6 13.6C7.2 10.6 7.4 6.4 10 3.8"),
    ]


@icon("pumpkin-pie", CAT, "Pie in a fluted tin with a dollop of whipped cream piled on top",
      tags=["pumpkin pie", "thanksgiving", "pie", "dessert", "autumn", "whipped cream", "baking", "fall"])
def _(S):
    parts = [
        shell(poly([(3, 13), (21, 13), (18.6, 20.6), (5.4, 20.6)], closed=True, r=S.r * 0.6)),
        line("M3 13a1.5 1.5 0 0 1 3 0a1.5 1.5 0 0 1 3 0a1.5 1.5 0 0 1 3 0a1.5 1.5 0 0 1 3 0a1.5 1.5 0 0 1 3 0a1.5 1.5 0 0 1 3 0"),
        solid(poly([(12, 3.2), (14.6, 6.6), (13.4, 6.6), (15.8, 9.6), (8.2, 9.6), (10.6, 6.6), (9.4, 6.6)], closed=True)),
        detail(seg(7.4, 16.8, 16.6, 16.8)),
    ]
    return parts


@icon("shrine-offering-box", CAT, "Wooden donation box with a slatted top made of angled bars and a coin dropping in",
      tags=["saisen box", "offering box", "shrine", "donation", "temple", "coin", "slatted", "prayer"])
def _(S):
    return [
        shell(poly([(3, 12.4), (6.4, 8), (21, 8), (21, 17), (18, 21.6), (3, 21.6)], closed=True, r=S.r * 0.6)),
        detail(poly([(3, 12.4), (18, 12.4), (21, 8)])),
        detail(seg(18, 12.4, 18, 21.6)),
        detail(seg(8.6, 12.4, 11.4, 8.4)) if False else detail(seg(9, 12.4, 11.8, 8.4)),
        detail(seg(13.6, 12.4, 16.4, 8.4)),
        shell(circle(11.5, 3.9, 1.8)),
    ]


@icon("havan-fire-pit", CAT, "Square stepped fire pit narrowing like an upside-down pyramid with flames rising from the top",
      tags=["havan kund", "fire pit", "hindu", "ritual fire", "yajna", "puja", "homa", "copper"])
def _(S):
    return [
        flame(7.6, 13, 6.2, 2.2),
        flame(12, 13, 9, 2.8),
        flame(16.4, 13, 6.2, 2.2),
        shell(poly([(3, 13.6), (21, 13.6), (21, 16), (18.2, 16), (18.2, 18.6), (15.6, 18.6), (15.6, 21.6), (8.4, 21.6),
                    (8.4, 18.6), (5.8, 18.6), (5.8, 16), (3, 16)], closed=True, r=S.r * 0.5)),
    ]


def _cob(cx, cy, ang, r):
    pts = [(0, -6.6), (2.3, -3.2), (2.7, 1.6), (1.7, 5.4), (0, 6.6), (-1.7, 5.4), (-2.7, 1.6), (-2.3, -3.2)]
    return poly([(x, y) for x, y in rot([(cx + px, cy + py) for px, py in pts], ang, cx, cy)], closed=True, r=r)


@icon("decorative-corn", CAT, "Three dried corn cobs fanned out and tied together at the base with loose husk strands",
      tags=["indian corn", "decorative corn", "harvest", "autumn", "thanksgiving", "fall", "maize", "dried corn"])
def _(S):
    rr = S.r + 1.2
    return [
        shell(_cob(12, 8.6, 0, rr)),
        shell(_cob(7, 10.6, -24, rr)),
        shell(_cob(17, 10.6, 24, rr)),
        line(seg(9, 17.4, 15, 17.4)),
        line("M10 17.6L8 21.6"),
        line(seg(12, 17.6, 12, 21.8)),
        line("M14 17.6L16 21.6"),
    ]


@icon("advent-candlestick", CAT, "Low wooden holder with four candles in a row, the first two lit",
      tags=["advent", "advent candles", "christmas", "candle holder", "four candles", "wreath", "sundays", "countdown"])
def _(S):
    return [
        shell(rect(2.5, 16.6, 19, 4.4, min(S.R, 1.6))),
        line(seg(5, 9.4, 5, 16.6)),
        line(seg(9.7, 9.4, 9.7, 16.6)),
        line(seg(14.3, 9.4, 14.3, 16.6)),
        line(seg(19, 9.4, 19, 16.6)),
        flame(5, 8, 4.6, 1.6),
        flame(9.7, 8, 4.6, 1.6),
    ]


@icon("incense-smoker", CAT, "Small turned wooden figure with a round hat and an open mouth puffing a curl of smoke",
      tags=["incense smoker", "raucherman", "german", "christmas", "wooden figure", "smoke", "incense cone", "folk art"])
def _(S):
    return [
        shell("M8 8.2C8 3.4 16 3.4 16 8.2Z"),
        line(seg(6, 8.4, 18, 8.4)),
        shell(poly([(8.2, 10.2), (15.8, 10.2), (18, 21.6), (6, 21.6)], closed=True, r=S.r)),
        dot(10.6, 11.9, 0.7), dot(13.4, 11.9, 0.7),
        dot(12, 14.6, 1.5),
        detail(seg(7.2, 18.4, 16.8, 18.4)),
        line("M14.4 13.6C17.2 13.4 20.4 11.6 20.2 8.4C20 6.4 17.8 6.6 18 8.2"),
    ]


@icon("lantern-on-stick", CAT, "Round paper lantern with a warm glow hanging from the end of a short carrying stick",
      tags=["lantern stick", "paper lantern", "lantern parade", "st martin", "martinmas", "carrying lantern", "glow", "children"])
def _(S):
    return [
        line(seg(2.5, 3.6, 14.5, 3.6)),
        line(seg(12, 3.6, 12, 6)),
        shell(rect(10.4, 6, 3.2, 1.8, 0.3)),
        shell(poly([(12, 8), (16.6, 10), (18.4, 14.2), (16.6, 18.6), (12, 20.4), (7.4, 18.6), (5.6, 14.2), (7.4, 10)], closed=True, r=S.r + 3)),
        detail(seg(12, 8, 12, 20.4)),
        line(seg(2.4, 12.6, 3.8, 12.6)),
        line(seg(20.2, 12.6, 21.6, 12.6)),
        line(seg(12, 21.6, 12, 22.2)) if False else dot(12, 21.6, 0.6),
    ]


@icon("lovespoon", CAT, "Carved wooden spoon with a wide handle panel holding a heart cut-out above the bowl",
      tags=["lovespoon", "welsh", "wedding", "carved spoon", "love token", "heart", "wooden", "craft"])
def _(S):
    return [
        shell(rect(7.4, 2.4, 9.2, 9.4, min(S.R, 3))),
        detail("M12 10.2C9.4 8.4 9.4 6 10.8 5.6C11.5 5.4 11.9 6 12 6.5C12.1 6 12.5 5.4 13.2 5.6C14.6 6 14.6 8.4 12 10.2Z"),
        line(seg(12, 11.8, 12, 14.4)),
        shell(poly([(6.6, 18.2), (8.6, 14.4), (15.4, 14.4), (17.4, 18.2), (15.4, 21.8), (8.6, 21.8)], closed=True, r=S.r + 1.5)),
    ]


@icon("brigids-cross", CAT, "Four-armed cross woven from rushes around a square centre with bound tips on each arm",
      tags=["brigid's cross", "st brigid", "imbolc", "irish", "rushes", "woven cross", "celtic", "protection"])
def _(S):
    parts = [shell(rect(9, 9, 6, 6, min(S.R, 1.2)))]
    for (x0, y0, x1, y1) in ((12, 9, 12, 2.6), (15, 12, 21.4, 12), (12, 15, 12, 21.4), (9, 12, 2.6, 12)):
        parts.append(line(seg(x0, y0, x1, y1)))
    for (a, b, c, d) in ((10.2, 4.8, 13.8, 4.8), (19.2, 10.2, 19.2, 13.8), (10.2, 19.2, 13.8, 19.2), (4.8, 10.2, 4.8, 13.8)):
        parts.append(line(seg(a, b, c, d)))
    return parts


@icon("april-fool-fish", CAT, "Paper cutout fish with a strip of tape stuck across its back",
      tags=["april fool", "paper fish", "poisson d'avril", "prank", "joke", "tape", "cutout", "april 1"])
def _(S):
    return [
        shell("M3 12.6C6 7 13 7 16.4 12.6C13 18.2 6 18.2 3 12.6Z"),
        shell(poly([(16, 12.6), (21.4, 7.8), (21.4, 17.4)], closed=True, r=S.r * 0.6)),
        dot(7, 11.8, 0.9),
        shell(poly([(8.6, 4.4), (13.4, 4.4), (14.4, 9.6), (9.6, 9.6)], closed=True, r=0)),
    ]


@icon("christmas-boat", CAT, "Small sailing ship ornament with one mast and strings of lights running down to the hull",
      tags=["christmas boat", "lighted boat", "ship", "christmas lights", "harbor", "ornament", "holiday", "sailing"])
def _(S):
    return [
        shell(poly([(3, 15.8), (21, 15.8), (18, 21.2), (6, 21.2)], closed=True, r=S.r)),
        line(seg(12, 3.4, 12, 15.8)),
        solid(poly(star(12, 2.9, 1.9, 0.8), closed=True)),
        line(seg(12, 4.6, 4.4, 15)),
        line(seg(12, 4.6, 19.6, 15)),
        dot(9.3, 8.3, 1.9), dot(6.5, 12, 1.9),
        dot(14.7, 8.3, 1.9), dot(17.5, 12, 1.9),
    ]

# ============================================================================ chunk 6

@icon("caroling-star-pole", CAT, "Large eight-pointed star with a small lantern glowing at its centre mounted on a carrying pole",
      tags=["star singers", "caroling star", "epiphany", "kolyada", "christmas", "lantern", "procession", "pole"])
def _(S):
    pts = star(12, 9.6, 7.4, 4.2, n=8)
    return [
        shell(poly(pts, closed=True, r=S.r * 0.4), stroke_miterlimit="3"),
        dot(12, 9.6, 1.9),
        line(seg(12, 17, 12, 21.8)),
    ]


@icon("groom-flower-veil", CAT, "Front view of a turban with strands of flower beads falling like a curtain over the face",
      tags=["sehra", "flower veil", "groom", "turban", "wedding", "indian wedding", "garland curtain", "marigold"])
def _(S):
    parts = [
        shell("M5.5 9.6C5.5 2.4 18.5 2.4 18.5 9.6Z"),
        detail("M7.4 7.4Q12 5 16.6 7.4"),
    ]
    for x in (6.5, 10, 14, 17.5):
        parts.append(line(seg(x, 9.6, x, 20.4)))
        parts.append(dot(x, 13, 1.5))
        parts.append(dot(x, 17.4, 1.5))
        parts.append(dot(x, 21, 1.0)) if False else None
    return [p for p in parts if p is not None]


@icon("moon-kite", CAT, "Diamond kite with a cross frame and a wide crescent-shaped tail below it",
      tags=["moon kite", "kite", "crescent", "festival kite", "flying", "wind", "sky", "traditional kite"])
def _(S):
    return [
        shell(poly([(12, 2.4), (19.6, 8.2), (12, 15.6), (4.4, 8.2)], closed=True, r=S.r * 0.6)),
        detail(seg(12, 2.4, 12, 15.6)),
        detail(seg(4.4, 8.2, 19.6, 8.2)),
        shell("M4.8 17.4C5.6 22 18.4 22 19.2 17.4C16.6 19.8 7.4 19.8 4.8 17.4Z"),
    ]


@icon("shield-kite", CAT, "Rectangular kite with a round hole in its centre and a wavy tail string hanging below",
      tags=["shield kite", "kite", "rectangular kite", "round hole", "flying", "festival", "wind", "tail"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 13, 13.5, min(S.R, 2.5)) + circle(12, 9.2, 2.7)),
        line("M12 16C9 17.4 15 19 12 20.4C11 21 11.4 21.4 12 21.8"),
    ]


@icon("weather-charm-doll", CAT, "Hanging cloth doll with a round head and simple face, tied at the neck over a flared skirt",
      tags=["teru teru bozu", "weather doll", "sunshine charm", "rain charm", "japanese", "hanging doll", "cloth", "wish"])
def _(S):
    return [
        line(seg(12, 2.2, 12, 5.6)),
        shell(circle(12, 9.2, 3.7)),
        dot(10.6, 8.7, 0.7), dot(13.4, 8.7, 0.7),
        line(seg(9.3, 13.4, 14.7, 13.4)),
        shell(poly([(9.4, 13.4), (5.5, 21), (8.6, 20), (12, 21.4), (15.4, 20), (18.5, 21), (14.6, 13.4)], closed=True, r=S.r * 0.6)),
    ]


@icon("household-shrine-shelf", CAT, "Small wall shelf holding a miniature shrine with a pitched roof, a door and a rope across the front",
      tags=["kamidana", "household shrine", "shinto", "shelf", "altar", "miniature shrine", "home altar", "shimenawa"])
def _(S):
    return [
        line(poly([(3, 10), (12, 3.5), (21, 10)], r=S.r)),
        shell(rect(6, 10, 12, 7, min(S.R, 1))),
        detail(seg(12, 12.4, 12, 17)),
        line(seg(2.5, 18.8, 21.5, 18.8)) if False else shell(rect(3, 17.6, 18, 3, min(S.R, 1))),
        line(seg(5, 13.4, 7.2, 13.4)) if False else dot(9.2, 13.6, 0.9),
    ]


@icon("cucumber-spirit-horse", CAT, "Side view of a cucumber standing on four stick legs like a small horse with a head and tail",
      tags=["shoryo uma", "spirit horse", "obon", "cucumber horse", "japanese", "ancestors", "vegetable animal", "offering"])
def _(S):
    return [
        shell(poly([(3.4, 12), (6, 9.2), (17, 9.2), (20, 12), (17, 14.8), (6, 14.8)], closed=True, r=S.r + 1.5)),
        line(poly([(6, 9.4), (4.6, 4.6), (8, 3.4)], r=S.r)),
        line(seg(7, 14.8, 6, 21)),
        line(seg(10, 14.8, 9.6, 21)),
        line(seg(14, 14.8, 14.4, 21)),
        line(seg(17, 14.8, 18, 21)),
        line("M20 12C21.8 12.4 22 15 21 17"),
    ]


def _chakana_outline():
    pts = [(9, 3), (15, 3), (15, 6), (18, 6), (18, 9), (21, 9), (21, 15), (18, 15), (18, 18), (15, 18), (15, 21), (9, 21),
           (9, 18), (6, 18), (6, 15), (3, 15), (3, 9), (6, 9), (6, 6), (9, 6)]
    return pts


@icon("chakana", CAT, "Stepped Andean cross with three steps on every side and a round hole at the centre",
      tags=["chakana", "andean cross", "inca", "stepped cross", "peru", "quechua", "sacred symbol", "southern cross"])
def _(S):
    return [shell(poly(_chakana_outline(), closed=True, r=S.r * 0.5) + circle(12, 12, 2.7))]


@icon("wish-ribbon-bracelet", CAT, "Wrist with a narrow ribbon tied in a bow, its two loose ends hanging down",
      tags=["wish bracelet", "ribbon bracelet", "friendship bracelet", "wrist", "knot", "tied ribbon", "charm", "fiesta"])
def _(S):
    return [
        shell(rect(5, 2.4, 14, 19.2, min(S.R, 4))),
        detail(poly([(12, 9), (8, 6.4), (8, 11.6)], closed=True)),
        detail(poly([(12, 9), (16, 6.4), (16, 11.6)], closed=True)),
        detail("M12 10.2L9.8 18"),
        detail("M12 10.2L14.2 18"),
    ]


@icon("fish-hook-pendant", CAT, "Carved hook-shaped pendant with a curved shank and barb hanging from a cord",
      tags=["fish hook", "pendant", "hei matau", "maori", "pacific", "necklace", "carved", "cord"])
def _(S):
    c = [(11, 7.4), (11, 10), (11, 13.4)]
    for i in range(0, 13):
        th = math.radians(180 - 180 * i / 12)
        c.append((14.6 + 3.6 * math.cos(th), 13.4 + 3.9 * math.sin(th)))
    c += [(18.2, 11.4), (18.2, 9.6)]
    return [
        line(poly([(3.4, 2.4), (11, 7.4), (18.6, 2.4)], r=S.r)),
        shell(poly(band(c, 1.5), closed=True, r=0)),
        line(seg(18.2, 10.8, 15.6, 12.2)),
    ]


@icon("kava-bowl", CAT, "Wide round wooden bowl resting on many short legs with a half coconut cup above it",
      tags=["kava", "kava bowl", "tanoa", "pacific", "fiji", "samoa", "ceremony", "coconut cup"])
def _(S):
    parts = [
        shell("M3 11.6H21C21 16.4 17.4 18.6 12 18.6C6.6 18.6 3 16.4 3 11.6Z"),
        shell("M14.4 4.6H20.4C20.4 7.6 18.6 9 17.4 9C16.2 9 14.4 7.6 14.4 4.6Z"),
    ]
    for x0, x1 in ((6, 5), (9, 8.4), (12, 12), (15, 15.6), (18, 19)):
        parts.append(line(seg(x0, 18, x1, 21.6)))
    return parts


@icon("pilgrim-staff", CAT, "Tall walking staff with a scallop shell at the top and a water gourd hanging below it",
      tags=["pilgrim staff", "camino", "santiago", "scallop shell", "gourd", "pilgrimage", "walking stick", "saint james"])
def _(S):
    d, pts = _scallop(9.4, 9.6, 8.4, -58, 58, 4)
    parts = [line(seg(7.4, 2.2, 7.4, 21.8)), shell(d)]
    for p in pts[1:-1]:
        ang = math.degrees(math.atan2(p[1] - 9.6, p[0] - 9.4))
        q = polar(9.4, 9.6, 3.8, ang)
        r = polar(9.4, 9.6, 6.2, ang)
        parts.append(detail(seg(q[0], q[1], r[0], r[1])))
    parts += [line(seg(7.4, 16.2, 14.8, 16.6)), shell(circle(15, 19, 2.6)), line(seg(15, 16.6, 15, 16.4))]
    return parts