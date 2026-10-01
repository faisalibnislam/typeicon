"""TypeIcon Core: clothing."""
from dsl import arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from dsl import D, P, Part, ST, U
from geometry import fmt, polar


def _pts_d(pts):
    return "".join(("M" if i == 0 else "L") + f"{fmt(x)} {fmt(y)}" for i, (x, y) in enumerate(pts))


def _arc_pts(cx, cy, r, a0, a1, n=8, ry=None):
    """Points along an ellipse arc (degrees, 0 = right, 90 = down) for use inside poly()."""
    ry = r if ry is None else ry
    out = []
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        x, _ = polar(0, 0, r, a)
        _, y = polar(0, 0, ry, a)
        out.append((cx + x, cy + y))
    return out


def _long_sleeves(cuff=19.0, hem=21.0, neck=(9, 15), top=3.0, shoulder=5.0, body=(7, 17), outer=(3, 21)):
    """Front silhouette of a long-sleeved top: sleeves hang beside the body (seams added as details)."""
    (nl, nr), (bl, br), (ol, orr) = neck, body, outer
    return [(nl, top), (ol + 1.5, shoulder), (ol, cuff), (bl, cuff), (bl, hem),
            (br, hem), (br, cuff), (orr, cuff), (orr - 1.5, shoulder), (nr, top)]


def _seams(S, y0=10.0, cuff=19.0, body=(7, 17)):
    return [detail(seg(body[0], y0, body[0], cuff)), detail(seg(body[1], y0, body[1], cuff))]


# ============================================================================ tops

@icon("t-shirt", "clothing", "T-shirt with short sleeves", tags=["tee", "shirt", "clothes", "apparel", "top"], aliases=["tee"])
def _(S):
    return [
        shell(poly([(8.5, 3.5), (3, 6.5), (4.5, 11), (7, 10), (7, 20.5), (17, 20.5), (17, 10), (19.5, 11), (21, 6.5), (15.5, 3.5)], closed=True, r=S.r)),
        detail("M8.5 3.5C9.2 5.2 10.4 6 12 6C13.6 6 14.8 5.2 15.5 3.5"),
    ]


@icon("shirt", "clothing", "Long-sleeved button-up shirt with a collar",
      tags=["dress shirt", "button-up", "collar", "formal", "clothes", "top"], aliases=["button-up-shirt"])
def _(S):
    return [
        shell(poly(_long_sleeves(), closed=True, r=S.r)),
        *_seams(S),
        detail(poly([(9, 3), (10, 7), (12, 5), (14, 7), (15, 3)], r=S.r)),
        dot(12, 10.5, 1.1), dot(12, 14.5, 1.1), dot(12, 18.5, 1.1),
    ]


@icon("polo", "clothing", "Polo shirt with a collar and short button placket",
      tags=["polo shirt", "golf", "collar", "clothes", "top", "sport"], aliases=["polo-shirt"])
def _(S):
    return [
        shell(poly([(8.5, 3.5), (3, 6.5), (4.5, 11), (7, 10), (7, 20.5), (17, 20.5), (17, 10), (19.5, 11), (21, 6.5), (15.5, 3.5)], closed=True, r=S.r)),
        detail(poly([(8.5, 3.5), (10, 7.5), (12, 5.5), (14, 7.5), (15.5, 3.5)], r=S.r)),
        detail(seg(12, 5.5, 12, 11)),
    ]


@icon("jacket", "clothing", "Zip-up jacket with long sleeves",
      tags=["zip", "outerwear", "bomber", "windbreaker", "clothes"])
def _(S):
    return [
        shell(poly(_long_sleeves(cuff=19, hem=21), closed=True, r=S.r)),
        *_seams(S),
        detail("M9 3C9.4 4.6 10.5 5.5 12 5.5C13.5 5.5 14.6 4.6 15 3"),
        detail(seg(12, 5.5, 12, 21)),
    ]


@icon("coat", "clothing", "Long overcoat with lapels",
      tags=["overcoat", "trench coat", "outerwear", "winter", "clothes"])
def _(S):
    return [
        shell(poly([(9, 3), (5, 4.5), (3.5, 16), (7, 16), (6, 21), (18, 21), (17, 16), (20.5, 16), (19, 4.5), (15, 3)], closed=True, r=S.r)),
        detail(seg(7, 9.5, 7, 16)), detail(seg(17, 9.5, 17, 16)),
        detail(poly([(9, 3), (12, 11), (15, 3)], r=S.r)),
        detail(seg(12, 11, 12, 21)),
    ]


@icon("hoodie", "clothing", "Hooded sweatshirt with drawstrings",
      tags=["hooded", "sweatshirt", "hood", "casual", "clothes"], aliases=["hooded-sweatshirt"])
def _(S):
    hood = _arc_pts(12, 7.5, 5, 180, 360, n=10)
    pts = hood + [(19.5, 8), (21, 19), (17, 19), (17, 21), (7, 21), (7, 19), (3, 19), (4.5, 8)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        *_seams(S, y0=12, cuff=19),
        detail(poly([(7, 8), (12, 12.5), (17, 8)], r=S.r)),
        line(seg(10.2, 11.1, 10.2, 15.5)), line(seg(13.8, 11.1, 13.8, 15.5)),
    ]


@icon("sweater", "clothing", "Knit sweater with ribbed cuffs and hem",
      tags=["jumper", "pullover", "knitwear", "winter", "clothes"], aliases=["jumper", "pullover"])
def _(S):
    return [
        shell(poly(_long_sleeves(cuff=19, hem=21), closed=True, r=S.r)),
        *_seams(S),
        detail("M9 3C9.4 4.6 10.5 5.5 12 5.5C13.5 5.5 14.6 4.6 15 3"),
        detail(seg(3.2, 15.5, 7, 15.5)), detail(seg(17, 15.5, 20.8, 15.5)),
        detail(seg(7, 17, 17, 17)),
    ]


@icon("vest", "clothing", "Sleeveless waistcoat with buttons",
      tags=["waistcoat", "gilet", "sleeveless", "formal", "clothes"], aliases=["waistcoat", "gilet"])
def _(S):
    pts = [(9, 3), (6.5, 3), (6, 6.5), (4, 9), (4, 19), (12, 21), (20, 19), (20, 9), (18, 6.5), (17.5, 3), (15, 3)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(poly([(9, 3), (12, 11), (15, 3)], r=S.r)),
        dot(12, 14.5, 1.1), dot(12, 18, 1.1),
    ]


@icon("suit", "clothing", "Suit jacket with lapels and a tie",
      tags=["business", "formal", "tie", "blazer", "office", "clothes"], aliases=["business-suit"])
def _(S):
    pts = [(6, 3.5), (12, 18), (18, 3.5), (20, 4.5), (21, 8), (21, 21), (3, 21), (3, 8), (4, 4.5)]
    tie = poly([(10.8, 4.5), (13.2, 4.5), (12.7, 6.8), (13.3, 10.8), (12, 12.5), (10.7, 10.8), (11.3, 6.8)], closed=True)
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(poly([(4.8, 4.2), (6.8, 11), (10.5, 14)], r=S.r)),
        detail(poly([(19.2, 4.2), (17.2, 11), (13.5, 14)], r=S.r)),
        solid(tie),
    ]


@icon("tie", "clothing", "Necktie", tags=["necktie", "formal", "business", "office", "clothes"], aliases=["necktie"])
def _(S):
    return [
        shell(poly([(10, 3), (14, 3), (13, 6.5), (15, 17), (12, 21), (9, 17), (11, 6.5)], closed=True, r=S.r)),
        detail(seg(11, 6.5, 13, 6.5)),
    ]


@icon("bow-tie", "clothing", "Bow tie", tags=["bowtie", "formal", "tuxedo", "party", "clothes"], aliases=["bowtie"])
def _(S):
    return [
        shell(poly([(3, 6.5), (9.5, 9.5), (14.5, 9.5), (21, 6.5), (21, 17.5), (14.5, 14.5), (9.5, 14.5), (3, 17.5)], closed=True, r=S.r)),
        detail(seg(9.5, 9.5, 9.5, 14.5)), detail(seg(14.5, 9.5, 14.5, 14.5)),
    ]


@icon("scarf", "clothing", "Scarf wrapped around the neck with hanging ends",
      tags=["muffler", "winter", "wrap", "neck", "clothes"], aliases=["muffler"])
def _(S):
    wrap = "M4 3.5C4 8.5 7.5 11 12 11C16.5 11 20 8.5 20 3.5H16C16 5.8 14.3 7.3 12 7.3C9.7 7.3 8 5.8 8 3.5Z"
    return [
        shell(wrap),
        shell(poly([(7.5, 13), (11, 13), (10.5, 20), (6, 19.5)], closed=True, r=S.r)),
        shell(poly([(13, 13), (16.5, 13), (18, 21), (13.5, 21)], closed=True, r=S.r)),
    ]


# ============================================================================ bottoms

@icon("skirt", "clothing", "A-line skirt with a waistband", tags=["mini skirt", "a-line", "women", "fashion", "clothes"])
def _(S):
    return [
        shell(poly([(7, 4), (17, 4), (17, 8), (20.5, 20), (3.5, 20), (7, 8)], closed=True, r=S.r)),
        detail(seg(7, 8, 17, 8)),
    ]


@icon("pants", "clothing", "Trousers with a waistband",
      tags=["trousers", "slacks", "legs", "bottoms", "clothes"], aliases=["trousers"])
def _(S):
    return [
        shell(poly([(6, 3), (18, 3), (19.5, 21), (14, 21), (12, 11.5), (10, 21), (4.5, 21)], closed=True, r=S.r)),
        detail(seg(5.67, 7, 18.33, 7)),
    ]


@icon("jeans", "clothing", "Jeans with front pockets and rolled cuffs",
      tags=["denim", "trousers", "pants", "casual", "clothes"], aliases=["denim"])
def _(S):
    return [
        shell(poly([(6, 3), (18, 3), (19.5, 21), (14, 21), (12, 11.5), (10, 21), (4.5, 21)], closed=True, r=S.r)),
        detail(seg(5.67, 7, 18.33, 7)),
        detail("M5.9 10.5C8.3 10.5 9.5 9 9.5 7"), detail("M18.1 10.5C15.7 10.5 14.5 9 14.5 7"),
        detail(seg(4.83, 17, 10.84, 17)), detail(seg(13.16, 17, 19.17, 17)),
    ]


@icon("shorts", "clothing", "Pair of shorts", tags=["short pants", "summer", "bottoms", "clothes", "gym"])
def _(S):
    return [
        shell(poly([(5, 4), (19, 4), (20.5, 17.5), (14, 18.5), (12, 12), (10, 18.5), (3.5, 17.5)], closed=True, r=S.r)),
        detail(seg(4.56, 8, 19.44, 8)),
    ]


# ============================================================================ headwear

@icon("hat", "clothing", "Brimmed hat with a band", tags=["fedora", "trilby", "headwear", "clothes", "gentleman"])
def _(S):
    crown = poly([(7, 14), (7.5, 6.5), (9, 5), (12, 6.3), (15, 5), (16.5, 6.5), (17, 14)], r=S.r)
    d = crown + "C19.5 14 21 14.8 21 16C21 17.5 17 18.5 12 18.5C7 18.5 3 17.5 3 16C3 14.8 4.5 14 7 14Z"
    return [shell(d), detail(seg(7.17, 11.5, 16.83, 11.5))]


@icon("cap", "clothing", "Baseball cap with a peak", tags=["baseball cap", "peak", "visor", "headwear", "sport"],
      aliases=["baseball-cap"])
def _(S):
    tip = "L21 14.5C21.6 15.1 21.4 16.5 20.3 16.5Z" if S.name == "rounded" else "L21.5 14.5L21.5 16.5Z"
    return [
        shell("M3 16.5C3 9.5 7 5 12 5C16.5 5 19.5 8.5 19.5 13" + tip),
        detail("M10.5 16.5C11.5 14.2 14.5 13 19.5 13"),
    ]


@icon("beanie", "clothing", "Knitted beanie with a pompom",
      tags=["knit hat", "winter hat", "toque", "headwear", "winter"], aliases=["knit-hat"])
def _(S):
    rr = 0.01 if S.name == "line" else 2
    cuff = f"H20V{fmt(19.5 - rr)}" + (f"A{rr} {rr} 0 0 1 {fmt(20 - rr)} 19.5" if rr > 0.1 else "") + \
        f"H{fmt(4 + rr)}" + (f"A{rr} {rr} 0 0 1 4 {fmt(19.5 - rr)}" if rr > 0.1 else "") + "V13.5Z"
    return [
        shell("M5.5 13.5C5.5 9.5 8.5 7 12 7C15.5 7 18.5 9.5 18.5 13.5" + cuff),
        detail(seg(5.5, 13.5, 18.5, 13.5)),
        detail(seg(8, 13.5, 8, 19.5)), detail(seg(12, 13.5, 12, 19.5)), detail(seg(16, 13.5, 16, 19.5)),
        dot(12, 4.5, 2),
    ]


# ============================================================================ legwear

@icon("dress", "clothing", "Dress with fitted top and flared skirt", tags=["gown", "frock", "clothes", "fashion", "women"])
def _(S):
    return [
        shell(poly([(9, 3), (9, 5.5), (7.5, 10), (9.5, 11), (5, 21), (19, 21), (14.5, 11), (16.5, 10), (15, 5.5), (15, 3)], closed=True, r=S.r)),
        detail(seg(9.5, 11, 14.5, 11)),
    ]


@icon("sock", "clothing", "A single sock", tags=["socks", "hosiery", "clothes", "foot"])
def _(S):
    return [
        shell(poly([(9, 3), (16, 3), (16, 13), (11, 19.5), (7, 20.5), (4, 17.5), (5, 14.5), (9, 11)], closed=True, r=S.r)),
        detail(seg(9, 7, 16, 7)),
    ]


# ============================================================================ footwear

@icon("shoe", "clothing", "Leather dress shoe with a heel",
      tags=["oxford", "footwear", "formal", "leather", "loafer"], aliases=["dress-shoe"])
def _(S):
    return [
        shell(poly([(3, 7.5), (8, 7.5), (13.5, 11.5), (19, 12.5), (21, 14.5), (21, 17), (9.5, 17), (8.5, 20), (3, 20)], closed=True, r=S.r)),
        detail(seg(3, 17, 9.5, 17)),
    ]


@icon("sneaker", "clothing", "Laced sneaker with a thick sole",
      tags=["trainer", "running shoe", "footwear", "sport", "gym"], aliases=["trainer", "running-shoe"])
def _(S):
    return [
        shell(poly([(3, 19.5), (3, 7.5), (7.5, 7.5), (14, 12), (19, 13), (21, 15), (21, 19.5)], closed=True, r=S.r)),
        detail(seg(3, 15.5, 21, 15.5)),
        detail(seg(9.8, 9.09, 8.3, 11.2)), detail(seg(12.68, 11.08, 11.4, 12.9)),
    ]


@icon("boot", "clothing", "Ankle-high boot with a heel", tags=["boots", "footwear", "winter", "hiking", "leather"])
def _(S):
    return [
        shell(poly([(5, 3), (12, 3), (12, 11.5), (18.5, 13), (21, 15.5), (21, 17.5), (10.5, 17.5), (9.5, 20.5), (5, 20.5)], closed=True, r=S.r)),
        detail(seg(5, 17.5, 10.5, 17.5)),
        detail(seg(5, 7, 12, 7)),
    ]


@icon("high-heel", "clothing", "High-heeled shoe", tags=["stiletto", "pump", "heels", "footwear", "women", "fashion"],
      aliases=["stiletto", "heels"])
def _(S):
    return [
        shell("M4 6.5C6 9 9 12.5 13.5 13.5L18.5 14.5C20.5 15 21 16.5 21 18.5L15 18.5C11 18.5 8 15 5.5 11.5L4 9.5Z"),
        line(seg(4.9, 11, 5.4, 20.5)),
    ]


@icon("sandal", "clothing", "Flip-flop sandal seen from above",
      tags=["flip-flop", "thong", "beach", "summer", "footwear"], aliases=["flip-flop"])
def _(S):
    return [
        shell("M12 2.5C15.5 2.5 17 5 17 8.5C17 11.5 15.5 13 15.5 16C15.5 19 16 21.5 12 21.5C8 21.5 8.5 19 8.5 16C8.5 13 7 11.5 7 8.5C7 5 8.5 2.5 12 2.5Z"),
        detail(poly([(7.6, 11.5), (12, 6.5), (16.4, 11.5)], r=S.r)),
    ]


@icon("slipper", "clothing", "House slipper (mule) with a toe cover",
      tags=["house shoe", "mule", "home", "footwear", "cozy"], aliases=["house-shoe"])
def _(S):
    return [
        shell("M3 15.5H9.5C9.5 10.5 12.5 7.5 16.5 7.5C19.5 7.5 21 10 21 13.5"
              + ("V19.5H3Z" if S.name == "line" else "V18A1.5 1.5 0 0 1 19.5 19.5H4.5A1.5 1.5 0 0 1 3 18V15.5Z")),
        detail(seg(9.5, 15.5, 21, 15.5)),
    ]


# ============================================================================ hands, belts, bags

@icon("glove", "clothing", "Five-fingered glove", tags=["gloves", "winter", "hand", "work glove", "clothes"])
def _(S):
    thumb = "L3.6 13.8Q2.5 12.2 4 11.2Q5 10.6 6 11.8" if S.name == "rounded" else "L3 13L4.5 10.5L6 11.8"
    d = ("M7.5 21V17.5" + thumb + "V7.625A1.625 1.625 0 0 1 9.25 7.625V5.625A1.625 1.625 0 0 1 12.5 5.625"
         "V6.625A1.625 1.625 0 0 1 15.75 6.625V9.125A1.625 1.625 0 0 1 19 9.125V21Z")
    return [
        shell(d),
        detail(seg(9.25, 7.625, 9.25, 12)), detail(seg(12.5, 6.625, 12.5, 12)), detail(seg(15.75, 9.125, 15.75, 12)),
        detail(seg(7.5, 17.5, 19, 17.5)),
    ]


@icon("mitten", "clothing", "Mitten with a separate thumb", tags=["mittens", "winter", "hand", "warm", "clothes"])
def _(S):
    thumb = "L3.8 13.2Q3 11.8 4.2 10.9Q5.6 10 7 11.5" if S.name == "rounded" else "L3.2 12.5L4.8 10L7 11.5"
    return [
        shell("M7 21V16.5" + thumb + "V8.5A5.5 5.5 0 0 1 18 8.5V21Z"),
        detail(seg(7, 16.5, 18, 16.5)),
    ]


@icon("belt", "clothing", "Belt with a buckle", tags=["buckle", "waist", "leather", "accessory", "clothes"])
def _(S):
    return [
        shell(rect(3, 5.5, 9, 13, min(S.R, 2))),
        shell(poly([(12, 9.5), (19, 9.5), (21, 12), (19, 14.5), (12, 14.5)], r=S.r) + "Z"),
        detail(seg(3, 12, 9.5, 12)),
        dot(15.5, 12, 1.1),
    ]


@icon("handbag", "clothing", "Handbag with a top handle",
      tags=["bag", "tote", "purse", "fashion", "accessory"], aliases=["tote-bag"])
def _(S):
    return [
        shell(poly([(5.5, 9.5), (18.5, 9.5), (20.5, 20.5), (3.5, 20.5)], closed=True, r=S.r)),
        line("M8.5 9.5V7.5C8.5 5.1 10 3.5 12 3.5C14 3.5 15.5 5.1 15.5 7.5V9.5"),
        dot(12, 13.5, 1.2),
    ]


@icon("purse", "clothing", "Coin purse with a kiss-lock clasp",
      tags=["coin purse", "clutch", "money", "change", "accessory"], aliases=["coin-purse"])
def _(S):
    return [
        shell("M5 9.5H19C20.5 11.5 21 13.5 21 15.5C21 19 17 20.5 12 20.5C7 20.5 3 19 3 15.5C3 13.5 3.5 11.5 5 9.5Z" if S.name == "line" else
              "M6.3 9.5H17.7C18.5 9.5 19 9.8 19.4 10.4C20.5 12.1 21 13.8 21 15.5C21 19 17 20.5 12 20.5C7 20.5 3 19 3 15.5"
              "C3 13.8 3.5 12.1 4.6 10.4C5 9.8 5.5 9.5 6.3 9.5Z"),
        dot(10.6, 7.4, 1.4), dot(13.4, 7.4, 1.4),
    ]


@icon("wallet", "clothing", "Billfold wallet with a clasp tab",
      tags=["billfold", "money", "cards", "cash", "accessory"], aliases=["billfold"])
def _(S):
    return [
        shell(rect(3, 5.5, 18, 14, S.R)),
        detail(poly([(21, 9.5), (15.5, 9.5), (15.5, 15.5), (21, 15.5)], r=S.r)),
        dot(18.3, 12.5, 1.1),
    ]


@icon("backpack", "clothing", "Backpack with a front pocket",
      tags=["rucksack", "school bag", "bag", "travel", "hiking"], aliases=["rucksack"])
def _(S):
    return [
        shell(rect(5, 5.5, 14, 16, S.R)),
        line("M9 5.5V4.5C9 3.4 9.9 2.5 11 2.5H13C14.1 2.5 15 3.4 15 4.5V5.5" if S.name == "rounded" else poly([(9, 5.5), (9, 2.5), (15, 2.5), (15, 5.5)])),
        detail(poly([(8, 21.5), (8, 14), (16, 14), (16, 21.5)], r=S.r)),
        detail(seg(5, 10, 19, 10)),
    ]


# ============================================================================ jewellery & accessories

@icon("wristwatch", "clothing", "Analogue wristwatch with a strap",
      tags=["watch", "time", "clock", "accessory", "wrist"], aliases=["watch"])
def _(S):
    return [
        shell(circle(12, 12, 5.5)),
        shell(poly([(9.1, 6.6), (9.6, 3), (14.4, 3), (14.9, 6.6)], closed=True, r=S.r)),
        shell(poly([(9.1, 17.4), (9.6, 21), (14.4, 21), (14.9, 17.4)], closed=True, r=S.r)),
        detail(poly([(12, 9.5), (12, 12), (14, 13.5)], r=S.r)),
        dot(18.4, 12, 1),
    ]


@icon("ring", "clothing", "Ring with a gemstone", tags=["engagement", "jewelry", "diamond", "wedding", "jewellery"])
def _(S):
    return [
        line(circle(12, 15, 5.5)),
        shell(poly([(9.5, 3), (14.5, 3), (16.5, 5.5), (12, 9.5), (7.5, 5.5)], closed=True, r=S.r * 1.5)),
        detail(seg(7.5, 5.5, 16.5, 5.5)),
    ]


@icon("necklace", "clothing", "Necklace with a pendant", tags=["pendant", "jewelry", "chain", "jewellery", "gift"])
def _(S):
    return [
        line("M4.5 3C4.5 9.5 8 13 12 13C16 13 19.5 9.5 19.5 3"),
        shell(poly([(12, 13), (15, 16.8), (12, 21), (9, 16.8)], closed=True, r=S.r)),
    ]


@icon("earring", "clothing", "Drop earring on a hook", tags=["jewelry", "jewellery", "ear", "drop", "accessory"])
def _(S):
    return [
        line("M12 10V5.5C12 3.8 10.9 3 9.7 3C8.5 3 7.7 3.8 7.7 5"),
        shell("M12 10C14.5 13 16 15 16 17A4 4 0 0 1 8 17C8 15 9.5 13 12 10Z"),
    ]


_BR_OUT = ellipse(12, 10.5, 9, 6)
_BR_IN = ellipse(12, 9.5, 5.5, 3.2)
_BR_GEM = poly([(12, 16.5), (14.5, 19), (12, 21.5), (9.5, 19)], closed=True)


def _bracelet_filled():
    body = U(P(_BR_OUT), ST(_BR_OUT, 2), P(_BR_GEM), ST(_BR_GEM, 2))
    return D(body, D(P(_BR_IN), ST(_BR_IN, 2)))


@icon("bracelet", "clothing", "Bangle bracelet with a charm",
      tags=["bangle", "jewelry", "jewellery", "wrist", "charm"], aliases=["bangle"], filled=_bracelet_filled)
def _(S):
    return [
        shell(_BR_OUT), detail(_BR_IN),
        shell(poly([(12, 16.5), (14.5, 19), (12, 21.5), (9.5, 19)], closed=True, r=S.r)),
    ]


@icon("sunglasses", "clothing", "Sunglasses with dark lenses", tags=["shades", "summer", "sun", "eyewear", "glasses"],
      aliases=["shades"])
def _(S):
    lens = [(3, 9), (10.5, 9), (10.5, 13), (8.5, 16), (5, 16), (3, 13.5)]
    return [
        shell(poly(lens, closed=True, r=S.r)),
        shell(poly([(24 - x, y) for x, y in lens], closed=True, r=S.r)),
        line("M10.5 10.5C11 9.5 13 9.5 13.5 10.5"),
        detail(seg(5.2, 13, 7, 11.2)), detail(seg(16.8, 11.2, 18.8, 13)),
    ]


# ============================================================================ swim & underwear

@icon("swimsuit", "clothing", "One-piece swimsuit", tags=["swimwear", "bathing suit", "beach", "swim", "summer"],
      aliases=["bathing-suit"])
def _(S):
    pts = [(7.5, 3), (9.5, 3), (12, 8), (14.5, 3), (16.5, 3), (17, 10), (16, 13), (18, 15.5), (13.5, 20.5), (10.5, 20.5), (6, 15.5), (8, 13), (7, 10)]
    return [shell(poly(pts, closed=True, r=S.r))]


@icon("bikini", "clothing", "Two-piece bikini", tags=["swimwear", "two-piece", "beach", "swim", "summer"])
def _(S):
    return [
        shell(poly([(4, 11), (10.5, 11), (8, 4.5)], closed=True, r=S.r)),
        shell(poly([(13.5, 11), (20, 11), (16, 4.5)], closed=True, r=S.r)),
        line(seg(10.5, 10, 13.5, 10)),
        shell(poly([(4.5, 14), (19.5, 14), (13.5, 21), (10.5, 21)], closed=True, r=S.r)),
    ]


@icon("underwear", "clothing", "Briefs with an elastic waistband",
      tags=["briefs", "underpants", "pants", "lingerie", "undies"], aliases=["briefs", "underpants"])
def _(S):
    pts = [(3.5, 5.5), (20.5, 5.5), (20.5, 11.5), (17, 14), (14.5, 18.5), (9.5, 18.5), (7, 14), (3.5, 11.5)]
    return [shell(poly(pts, closed=True, r=S.r)), detail(seg(3.5, 9.5, 20.5, 9.5))]


@icon("bra", "clothing", "Bra with two cups and straps", tags=["brassiere", "lingerie", "underwear", "women"],
      aliases=["brassiere"])
def _(S):
    d = "M3 16.5C3 12 5.5 9 9 9C10.3 9 11.3 9.7 12 10.5C12.7 9.7 13.7 9 15 9C18.5 9 21 12 21 16.5Z"
    return [
        shell(d if S.name == "rounded" else d.replace("C3 12", "L3 13.5C3 12")),
        detail(seg(12, 10.5, 12, 16.5)),
        line(seg(6, 9.8, 7, 3.5)), line(seg(18, 9.8, 17, 3.5)),
    ]


@icon("pajamas", "clothing", "Pajama top and trousers",
      tags=["pyjamas", "sleepwear", "nightwear", "bedtime", "sleep"], aliases=["pyjamas", "pjs"])
def _(S):
    return [
        shell(poly([(9, 3), (4.5, 4.5), (3, 10), (7, 10.5), (7, 12), (17, 12), (17, 10.5), (21, 10), (19.5, 4.5), (15, 3)], closed=True, r=S.r)),
        detail(poly([(9, 3), (12, 6.5), (15, 3)], r=S.r)),
        shell(poly([(7, 15), (17, 15), (18, 21), (13.5, 21), (12, 18), (10.5, 21), (6, 21)], closed=True, r=S.r)),
    ]


# ============================================================================ work & utility

@icon("uniform", "clothing", "Uniform tunic with two rows of buttons",
      tags=["military", "police", "officer", "work", "clothes"])
def _(S):
    return [
        shell(poly(_long_sleeves(), closed=True, r=S.r)),
        *_seams(S),
        detail(seg(9, 5.5, 15, 5.5)),
        dot(10, 9.5, 1.1), dot(14, 9.5, 1.1), dot(10, 13.5, 1.1), dot(14, 13.5, 1.1), dot(10, 17.5, 1.1), dot(14, 17.5, 1.1),
    ]


@icon("apron", "clothing", "Bib apron with waist ties and a pocket",
      tags=["kitchen", "cooking", "chef", "baking", "work"])
def _(S):
    return [
        shell(poly([(8.5, 6), (15.5, 6), (15.5, 11), (18, 11), (18.5, 21), (5.5, 21), (6, 11), (8.5, 11)], closed=True, r=S.r)),
        line("M8.5 6C8.5 3.8 9.8 2.8 12 2.8C14.2 2.8 15.5 3.8 15.5 6"),
        line(seg(6, 11, 3, 13.5)), line(seg(18, 11, 21, 13.5)),
        detail(poly([(9, 14.5), (9, 17.5), (15, 17.5), (15, 14.5)], r=S.r)),
    ]


@icon("hanger", "clothing", "Clothes hanger", tags=["coat hanger", "wardrobe", "closet", "cloakroom", "clothes"],
      aliases=["coat-hanger"])
def _(S):
    return [
        line(arc(12, 5.5, 2.2, 180, 90) + "V9"),
        line(poly([(12, 9), (21, 15.5), (21, 18), (3, 18), (3, 15.5)], closed=True, r=S.r)),
    ]


@icon("sewing-machine", "clothing", "Sewing machine", tags=["sewing", "tailor", "stitch", "craft", "fabric"])
def _(S):
    pts = [(4, 4.5), (20, 4.5), (20, 17), (21, 17), (21, 20.5), (3, 20.5), (3, 17), (15.5, 17), (15.5, 9), (9, 9), (9, 12), (4, 12)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        line(seg(6.5, 12, 6.5, 15.5)),
        line(seg(12, 4.5, 12, 2)),
    ]


def _stadium(ax, ay, bx, by, r):
    import math
    L = math.hypot(bx - ax, by - ay)
    nx, ny = -(by - ay) / L * r, (bx - ax) / L * r
    return (f"M{fmt(ax + nx)} {fmt(ay + ny)}L{fmt(bx + nx)} {fmt(by + ny)}A{fmt(r)} {fmt(r)} 0 0 0 {fmt(bx - nx)} {fmt(by - ny)}"
            f"L{fmt(ax - nx)} {fmt(ay - ny)}A{fmt(r)} {fmt(r)} 0 0 0 {fmt(ax + nx)} {fmt(ay + ny)}Z")


@icon("needle-thread", "clothing", "Sewing needle with thread", tags=["sewing", "needle", "thread", "stitch", "tailor"],
      aliases=["needle", "sewing-needle"])
def _(S):
    return [
        line(seg(3.5, 20.5, 14.6, 9.4)),
        line(_stadium(15, 9, 18.5, 5.5, 1.9)),
        line("M16.8 7.2C19.5 4.5 22.8 8 20.5 11.5C18.5 14.5 15 14 13.5 17C12.8 18.5 12 20 10.5 21"),
    ]


_BTN_OUT = circle(12, 12, 8.5)
_BTN_RIM = circle(12, 12, 5.5)
_BTN_HOLES = [(10.1, 10.1), (13.9, 10.1), (10.1, 13.9), (13.9, 13.9)]


def _button_filled():
    body = U(P(_BTN_OUT), ST(_BTN_OUT, 2))
    return D(body, ST(_BTN_RIM, 2), *[P(circle(x, y, 1.1)) for x, y in _BTN_HOLES])


@icon("sewing-button", "clothing", "Sewing button with four holes",
      tags=["button", "sewing", "haberdashery", "craft", "tailor"], filled=_button_filled)
def _(S):
    if S.name == "line":
        holes = [Part("dot", rect(x - 1.05, y - 1.05, 2.1, 2.1)) for x, y in _BTN_HOLES]
    else:
        holes = [dot(x, y, 1.1) for x, y in _BTN_HOLES]
    return [shell(_BTN_OUT), detail(_BTN_RIM), *holes]


# ============================================================================ more tops

@icon("tank-top", "clothing", "Sleeveless tank top", tags=["singlet", "vest top", "sleeveless", "gym", "summer"],
      aliases=["singlet"])
def _(S):
    bottom = "V21H5.5" if S.name == "line" else "V19A2 2 0 0 1 16.5 21H7.5A2 2 0 0 1 5.5 19"
    return [shell("M8 3H10C10 5.5 10.8 7 12 7C13.2 7 14 5.5 14 3H16C16 6 17 8.5 18.5 9.5" + bottom + "V9.5C7 8.5 8 6 8 3Z")]


@icon("blouse", "clothing", "Blouse with puffed sleeves and a peplum",
      tags=["top", "women", "shirt", "fashion", "clothes"])
def _(S):
    d = ("M9 3.5L6.5 4.5C3.5 5 2.5 8 4 11L7.5 10L8 14.5L6.5 20.5H17.5L16 14.5L16.5 10L20 11"
         "C21.5 8 20.5 5 17.5 4.5L15 3.5Z")
    return [
        shell(d),
        detail(poly([(9, 3.5), (12, 7), (15, 3.5)], r=S.r)),
        detail(seg(8, 14.5, 16, 14.5)),
    ]


@icon("cardigan", "clothing", "Button-front cardigan with a V-neck",
      tags=["knitwear", "sweater", "jumper", "button", "clothes"])
def _(S):
    return [
        shell(poly(_long_sleeves(), closed=True, r=S.r)),
        *_seams(S),
        detail(poly([(9, 3), (12, 10), (15, 3)], r=S.r)),
        detail(seg(12, 10, 12, 21)),
        dot(12, 13.5, 1.5), dot(12, 17.5, 1.5),
    ]


@icon("kimono", "clothing", "Kimono with wide sleeves and an obi sash",
      tags=["japanese", "robe", "yukata", "traditional", "clothes"], aliases=["yukata"])
def _(S):
    return [
        shell(poly([(9, 3), (3, 5), (3, 12), (7, 12), (7, 21), (17, 21), (17, 12), (21, 12), (21, 5), (15, 3)], closed=True, r=S.r)),
        detail(seg(15, 3, 10.5, 12.5)), detail(seg(9, 3, 11.8, 8)),
        detail(seg(7, 12.5, 17, 12.5)), detail(seg(7, 16, 17, 16)),
        detail(seg(10.3, 16, 10, 21)),
    ]


@icon("sari", "clothing", "Woman wearing a sari draped over one shoulder",
      tags=["saree", "indian", "traditional", "drape", "women"], aliases=["saree"])
def _(S):
    pts = [(9, 9.5), (15, 9.5), (17, 12), (15.5, 13.5), (18.5, 21), (5.5, 21), (7.5, 14.5), (4.5, 18), (3, 16.5), (7.5, 10.5)]
    return [
        shell(circle(12, 4.5, 2.5)),
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(9, 9.5, 15.9, 14.5)),
        detail(seg(11, 17, 10.7, 21)), detail(seg(14, 17, 14.3, 21)),
    ]


@icon("raincoat", "clothing", "Hooded raincoat with buttons", tags=["rain", "mac", "waterproof", "anorak", "weather"],
      aliases=["anorak"])
def _(S):
    hood = _arc_pts(12, 7.5, 5, 180, 360, n=10)
    pts = hood + [(19.5, 8), (21, 16), (17.5, 16), (18, 21), (6, 21), (6.5, 16), (3, 16), (4.5, 8)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(6.7, 12, 6.6, 16)), detail(seg(17.3, 12, 17.4, 16)),
        detail(poly([(7, 8), (12, 12.5), (17, 8)], r=S.r)),
        detail(seg(12, 12.5, 12, 21)),
        dot(14.2, 15.5, 1.1), dot(14.2, 19, 1.1),
    ]


@icon("overalls", "clothing", "Bib overalls (dungarees)", tags=["dungarees", "denim", "farmer", "workwear", "clothes"],
      aliases=["dungarees"])
def _(S):
    pts = [(8, 7), (16, 7), (16, 10.5), (18.5, 10.5), (19.5, 21), (14, 21), (12, 14.5), (10, 21), (4.5, 21), (5.5, 10.5), (8, 10.5)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        line(seg(8.5, 7, 7, 2.5)), line(seg(15.5, 7, 17, 2.5)),
        detail(seg(5.5, 10.5, 18.5, 10.5)),
    ]


@icon("leggings", "clothing", "Slim-fitting leggings", tags=["tights", "yoga pants", "activewear", "gym", "women"],
      aliases=["tights", "yoga-pants"])
def _(S):
    return [
        shell(poly([(6.5, 3), (17.5, 3), (16.5, 21), (13.5, 21), (12, 10), (10.5, 21), (7.5, 21)], closed=True, r=S.r)),
        detail(seg(6.3, 6.5, 17.3, 6.5)),
    ]


# ============================================================================ more headwear

@icon("cowboy-hat", "clothing", "Cowboy hat with an upturned brim",
      tags=["western", "stetson", "rodeo", "ranch", "headwear"], aliases=["stetson"])
def _(S):
    return [
        shell("M7 13.5L7.8 7C8 5.5 10 5 12 6.5C14 5 16 5.5 16.2 7L17 13.5C18.5 13.5 19.8 12.6 21 10.5"
              "C21 15 17.5 17.5 12 17.5C6.5 17.5 3 15 3 10.5C4.2 12.6 5.5 13.5 7 13.5Z"),
        detail(seg(7.3, 11, 16.7, 11)),
    ]


@icon("top-hat", "clothing", "Tall top hat", tags=["magician", "gentleman", "formal", "tuxedo", "headwear"])
def _(S):
    return [
        shell(poly([(7, 16), (6.5, 3), (17.5, 3), (17, 16), (21, 16), (21, 19.5), (3, 19.5), (3, 16)], closed=True, r=S.r)),
        detail(seg(6.85, 12, 17.15, 12)),
    ]


@icon("helmet", "clothing", "Motorcycle helmet with a visor",
      tags=["motorcycle", "crash helmet", "biker", "safety", "headwear"], aliases=["crash-helmet"])
def _(S):
    body = "M3.5 15.5C3.5 8.5 7.5 4 13 4C18 4 21 8 21 13V17" + ("L19.5 19H7" if S.name == "line" else "C21 18.2 20.2 19 19 19H7") + \
        "C5 19 3.5 17.5 3.5 15.5Z"
    return [
        shell(body),
        detail("M21 10.5H15.5C14 10.5 13 11.5 13 13C13 14.5 14 15 15.5 15H21"),
    ]


@icon("crown", "clothing", "Royal crown", tags=["king", "queen", "royal", "monarch", "winner"])
def _(S):
    return [
        shell(poly([(3.5, 7), (8, 12), (12, 5), (16, 12), (20.5, 7), (19, 19), (5, 19)], closed=True, r=S.r)),
        detail(seg(4.5, 15, 19.5, 15)),
    ]


@icon("tiara", "clothing", "Jewelled tiara", tags=["princess", "diadem", "bride", "jewelry", "royal"],
      aliases=["diadem"])
def _(S):
    top = poly([(3, 17), (4.5, 10), (8, 12), (12, 4.5), (16, 12), (19.5, 10), (21, 17)], r=S.r)
    return [
        shell(top + "C18 15.5 15 15 12 15C9 15 6 15.5 3 17Z"),
        dot(12, 11, 1.4),
    ]


# ============================================================================ beauty & grooming

@icon("lipstick", "clothing", "Lipstick tube", tags=["makeup", "cosmetics", "beauty", "lips", "rouge"])
def _(S):
    return [
        shell(poly([(9.5, 11), (9.5, 6), (14.5, 3), (14.5, 11), (17, 11), (17, 21), (7, 21), (7, 11)], closed=True, r=S.r)),
        detail(seg(7, 15, 17, 15)),
    ]


@icon("perfume", "clothing", "Perfume bottle", tags=["fragrance", "scent", "cologne", "beauty", "spray"],
      aliases=["fragrance", "cologne"])
def _(S):
    pts = [(9, 3), (15, 3), (15, 7.5), (13.5, 7.5), (13.5, 10), (19, 10), (19, 21), (5, 21), (5, 10), (10.5, 10), (10.5, 7.5), (9, 7.5)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(10.5, 7.5, 13.5, 7.5)),
        detail(rect(8.5, 13.5, 7, 4, min(S.R, 1.5))),
    ]


@icon("nail-polish", "clothing", "Nail polish bottle", tags=["manicure", "nails", "varnish", "beauty", "cosmetics"],
      aliases=["nail-varnish"])
def _(S):
    return [
        shell(poly([(10, 3), (14, 3), (14, 11), (17, 11), (18, 21), (6, 21), (7, 11), (10, 11)], closed=True, r=S.r)),
        detail(seg(10, 11, 14, 11)),
        detail(seg(9.8, 14.5, 9.6, 17.5)),
    ]


@icon("comb", "clothing", "Hair comb", tags=["hair", "grooming", "barber", "beauty", "hairdresser"])
def _(S):
    return [
        shell(rect(3, 5.5, 18, 4.5, min(S.R, 2))),
        *[line(seg(x, 10, x, 18.5)) for x in (4.5, 8.25, 12, 15.75, 19.5)],
    ]


@icon("hairbrush", "clothing", "Paddle hairbrush", tags=["hair", "brush", "grooming", "beauty", "salon"])
def _(S):
    end = "V21H10.5Z" if S.name == "line" else "V19.5A1.5 1.5 0 0 1 12 21A1.5 1.5 0 0 1 10.5 19.5Z"
    return [
        shell("M10.5 14.81A6 6 0 1 1 13.5 14.81" + end),
        dot(9.75, 7.25, 1.1), dot(14.25, 7.25, 1.1), dot(9.75, 11.25, 1.1), dot(14.25, 11.25, 1.1),
    ]


@icon("razor", "clothing", "Safety razor", tags=["shave", "shaving", "grooming", "barber", "blade"])
def _(S):
    return [
        shell(poly([(3.5, 3), (20.5, 3), (20.5, 9), (14, 9), (14, 21), (10, 21), (10, 9), (3.5, 9)], closed=True, r=S.r)),
        detail(seg(3.5, 6, 20.5, 6)),
        detail(seg(10, 17, 14, 17)),
    ]


# ============================================================================ haberdashery & laundry

@icon("zipper", "clothing", "Zipper with interlocking teeth and a slider",
      tags=["zip", "fastener", "sewing", "clothes", "close"], aliases=["zip-fastener"])
def _(S):
    rr = 0 if S.name == "line" else 0.9
    teeth = [(9, 10.5), (12, 12.5), (9, 14.5), (12, 16.5), (9, 18.5), (12, 20)]
    return [
        shell(poly([(8, 3), (16, 3), (14.5, 8), (9.5, 8)], closed=True, r=S.r)),
        *[Part("dot", rect(x, y, 3, 2, rr)) for x, y in teeth],
    ]


def _pin_pt(u, v):
    import math
    c = math.sqrt(0.5)
    return (12 + (u + v) * c, 12 + (v - u) * c)


@icon("safety-pin", "clothing", "Safety pin", tags=["pin", "fastener", "sewing", "nappy pin", "clip"])
def _(S):
    P0 = _pin_pt
    pts = lambda *uv: " ".join(f"{fmt(x)} {fmt(y)}" for x, y in (P0(u, v) for u, v in uv))  # noqa: E731
    c = P0(-7, 0)
    return [
        line(circle(c[0], c[1], 2.6)),
        line("M" + pts((-4.6, -1)) + "L" + pts((4.5, -2.2))),
        line("M" + pts((-4.6, 1)) + "L" + pts((4.5, 2.2))),
        shell(poly([P0(4.5, -3), P0(9, -3), P0(9, 3), P0(4.5, 3)], closed=True, r=S.r)),
    ]


@icon("clothes-iron", "clothing", "Clothes iron", tags=["iron", "ironing", "laundry", "press", "steam"],
      aliases=["flat-iron"])
def _(S):
    return [
        shell("M3.5 18C4.5 12 7 8.5 11 8.5H18C19.9 8.5 21 9.6 21 11.5V18Z"),
        line(poly([(9, 8.5), (10, 4.5), (18.5, 4.5), (18.5, 8.5)], r=S.r)),
        detail(seg(4.3, 14.5, 21, 14.5)),
    ]


@icon("laundry-basket", "clothing", "Laundry basket with clothes", tags=["laundry", "hamper", "washing", "clothes", "basket"],
      aliases=["hamper"])
def _(S):
    return [
        shell(poly([(3, 9), (21, 9), (19, 21), (5, 21)], closed=True, r=S.r)),
        detail(seg(3.6, 13, 20.4, 13)), detail(seg(4.3, 17, 19.7, 17)),
        line("M6 9C6 6 9 4.5 11 6.5C13 3.8 17.5 4.5 18 9"),
    ]


@icon("fabric", "clothing", "Bolt of fabric unrolling", tags=["cloth", "textile", "material", "sewing", "roll"],
      aliases=["cloth", "textile"])
def _(S):
    zig = [(21, 9), (21, 19.5), (19, 21), (17, 19.5), (15, 21), (13, 19.5), (11, 21), (9, 19.5), (9, 9)]
    return [
        shell(rect(3, 3, 18, 6, 3 if S.name == "rounded" else 1)),
        shell(poly(zig, closed=True, r=S.r * 0.5)),
        detail("M6 3A2 3 0 0 1 6 9"),
    ]
