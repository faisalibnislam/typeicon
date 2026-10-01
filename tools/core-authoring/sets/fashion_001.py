"""TypeIcon Core: fashion (batch fashion_001).

Garments drawn front-on in the same proportions as sets/clothing.py: tops sit on a 3-21 frame with sleeves
beside a 7-17 body, bottoms hang from a waistband at y 3-4. Patterned garments (stripes, plaid) use solid
bands in Line/Rounded and knocked-out bands in Filled.
"""
from dsl import D, I, P, Part, ST, U, arc, circle, detail, dot, ellipse, icon, line, poly, rect, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar  # noqa: F401

CAT = "fashion"


# --------------------------------------------------------------------------- helpers

def _tee(top=3.5, hem=20.5, body=(7, 17)):
    """Short-sleeved top outline (same shape as clothing/t-shirt)."""
    bl, br = body
    return [(8.5, top), (3, top + 3), (4.5, top + 7.5), (bl, top + 6.5), (bl, hem),
            (br, hem), (br, top + 6.5), (19.5, top + 7.5), (21, top + 3), (15.5, top)]


def _ls(cuff=19.0, hem=21.0, neck=(9, 15), top=3.0, shoulder=5.0, body=(7, 17), outer=(3, 21)):
    """Long-sleeved top outline: sleeves hang beside the body (seams added as details)."""
    (nl, nr), (bl, br), (ol, orr) = neck, body, outer
    return [(nl, top), (ol + 1.5, shoulder), (ol, cuff), (bl, cuff), (bl, hem),
            (br, hem), (br, cuff), (orr, cuff), (orr - 1.5, shoulder), (nr, top)]


def _seams(y0=10.0, y1=19.0, body=(7, 17)):
    return [detail(seg(body[0], y0, body[0], y1)), detail(seg(body[1], y0, body[1], y1))]


def _mirror(pts):
    return [(24 - x, y) for x, y in pts]


def _crew(top=3.5, l=8.5, r=15.5, depth=2.5):
    mid = top + depth
    return (f"M{fmt(l)} {fmt(top)}C{fmt(l + 0.7)} {fmt(top + 1.7)} {fmt(l + 1.9)} {fmt(mid)} 12 {fmt(mid)}"
            f"C{fmt(r - 1.9)} {fmt(mid)} {fmt(r - 0.7)} {fmt(top + 1.7)} {fmt(r)} {fmt(top)}")


def _solid_body(*ds):
    """Filled silhouette of closed outlines (fill plus the 2 px stroke)."""
    return U(*[U(P(d), ST(d, 2)) for d in ds])


def _band(outline_d, x, y, w, h):
    """Part of a closed outline inside a rectangle, as a solid region (stripes, shaded panels)."""
    return path_to_d(I(P(outline_d), P(rect(x, y, w, h))))


def _tail(pts, r=0.0):
    """Open polyline without its leading move-to, to continue a path that already ends at pts[0]."""
    d = poly(pts, r=r)
    return d[min(i for i in (d.find("L", 1), d.find("A", 1)) if i > 0):]


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


def _flower(cx, cy, k=1.05, r=0.95):
    return [Part("dot", circle(*polar(cx, cy, k, a), r)) for a in (-90, -18, 54, 126, 198)]


# ============================================================================ tops

@icon("crop-top", CAT, "Short-sleeved top cut off above the waist, with a bare gap above the waistband below.",
      tags=["crop", "cropped", "top", "midriff", "summer", "tee"], aliases=["cropped-top"])
def _(S):
    return [
        shell(poly(_tee(top=3, hem=13), closed=True, r=S.r)),
        detail(_crew(top=3)),
        shell(rect(6.5, 17.5, 11, 4, min(S.R, 1.5))),
    ]


@icon("turtleneck", CAT, "Long-sleeved sweater with a tall collar rolled up around the neck.",
      tags=["polo neck", "roll neck", "sweater", "jumper", "knitwear", "winter"], aliases=["polo-neck", "roll-neck"])
def _(S):
    pts = [(9, 2), (15, 2), (15, 6.5), (19.5, 7.5), (21, 19), (17, 19), (17, 21), (7, 21), (7, 19), (3, 19), (4.5, 7.5), (9, 6.5)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(9, 6.5, 15, 6.5)),
        *_seams(y0=11),
    ]


@icon("henley-shirt", CAT, "Long-sleeved shirt with a round collarless neck and a short row of buttons.",
      tags=["henley", "top", "buttons", "casual", "shirt", "long sleeve"])
def _(S):
    return [
        shell(poly(_ls(), closed=True, r=S.r)),
        *_seams(),
        detail(_crew(top=3, l=9, r=15, depth=2.5)),
        dot(12, 8.5, 1), dot(12, 12, 1), dot(12, 15.5, 1),
    ]


@icon("hawaiian-shirt", CAT, "Short-sleeved shirt with an open camp collar and flowers printed on the front.",
      tags=["aloha shirt", "floral", "tropical", "summer", "vacation", "camp collar"], aliases=["aloha-shirt"])
def _(S):
    return [
        shell(poly(_tee(hem=21), closed=True, r=S.r)),
        detail(poly([(8.5, 3.5), (10, 8), (12, 9.5), (14, 8), (15.5, 3.5)], r=S.r)),
        *_flower(10.4, 13.6), *_flower(13.8, 17.2),
    ]


@icon("flannel-shirt", CAT, "Long-sleeved collared shirt with a plaid grid of crossing lines.",
      tags=["plaid", "checked shirt", "lumberjack", "tartan", "flannel", "shirt"], aliases=["plaid-shirt"])
def _(S):
    return [
        shell(poly(_ls(), closed=True, r=S.r)),
        *_seams(),
        detail(poly([(9, 3), (10, 7), (12, 5), (14, 7), (15, 3)], r=S.r)),
        detail(seg(12, 5, 12, 21)),
        detail(seg(3.8, 11.5, 20.2, 11.5)), detail(seg(3.35, 16, 20.65, 16)),
    ]


@icon("long-sleeve-shirt", CAT, "Plain crew-neck shirt with full-length sleeves held out from the body.",
      tags=["long sleeve", "tee", "top", "shirt", "basic", "casual"], aliases=["long-sleeve-tee"])
def _(S):
    pts = [(9, 3), (5, 4), (2, 14), (4.5, 15.5), (7.5, 9.5), (7.5, 21), (16.5, 21), (16.5, 9.5), (19.5, 15.5), (22, 14), (19, 4), (15, 3)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(_crew(top=3, l=9, r=15)),
    ]


@icon("v-neck-shirt", CAT, "Short-sleeved T-shirt with a deep V-shaped neckline.",
      tags=["v-neck", "tee", "t-shirt", "top", "neckline", "casual"], aliases=["v-neck-tee"])
def _(S):
    return [
        shell(poly(_tee(), closed=True, r=S.r)),
        detail(poly([(8.5, 3.5), (12, 10), (15.5, 3.5)], r=S.r)),
    ]


_TEE = _tee()


@icon("raglan-shirt", CAT, "T-shirt with shaded sleeves joined by diagonal seams from the underarm to the collar.",
      tags=["raglan", "baseball tee", "tee", "top", "sleeves", "two tone"], aliases=["baseball-tee"])
def _(S):
    sl = [(8.5, 3.5), (3, 6.5), (4.5, 11), (7, 10)]
    return [
        shell(poly(_TEE, closed=True, r=S.r)),
        solid(poly(sl, closed=True, r=S.r)), solid(poly(_mirror(sl), closed=True, r=S.r)),
        detail(seg(7, 10, 8.5, 3.5)), detail(seg(17, 10, 15.5, 3.5)),
        detail(_crew()),
    ]


_RUGBY = poly(_ls(), closed=True)
_RUGBY_BANDS = [(11, 2.5), (16, 2.5)]
_RUGBY_COLLAR = poly([(9, 3), (10, 7), (12, 5), (14, 7), (15, 3)])


def _rugby_filled():
    body = D(_solid_body(_RUGBY), *[P(rect(0, y, 24, h)) for y, h in _RUGBY_BANDS])
    return D(body, ST(_RUGBY_COLLAR, 2), ST(seg(12, 5, 12, 9), 2))


@icon("rugby-shirt", CAT, "Long-sleeved shirt with wide horizontal stripes, a pointed collar and a short button placket.",
      tags=["rugby jersey", "striped", "hooped shirt", "sport", "polo", "stripes"], aliases=["rugby-jersey"],
      filled=_rugby_filled)
def _(S):
    outline = poly(_ls(), closed=True, r=S.r)
    return [
        shell(outline),
        *[Part("dot", _band(outline, 0, y, 24, h)) for y, h in _RUGBY_BANDS],
        detail(poly([(9, 3), (10, 7), (12, 5), (14, 7), (15, 3)], r=S.r)),
        detail(seg(12, 5, 12, 9)),
    ]


@icon("breton-shirt", CAT, "Long-sleeved boat-neck top with thin, evenly spaced horizontal stripes.",
      tags=["breton", "striped shirt", "sailor stripes", "mariniere", "boat neck", "stripes"], aliases=["striped-top"])
def _(S):
    pts = [(8, 3), (4.5, 4.5), (3, 19), (7, 19), (7, 21), (17, 21), (17, 19), (21, 19), (19.5, 4.5), (16, 3)]
    d = poly(pts, r=S.r) + "C14.5 4.4 9.5 4.4 8 3Z"
    xl = lambda y: 4.5 - 1.5 * (y - 4.5) / 14.5  # noqa: E731
    return [shell(d)] + [detail(seg(xl(y), y, 24 - xl(y), y)) for y in (8.5, 12.5, 16.5)]


@icon("halter-top", CAT, "Sleeveless top held up by straps that meet behind the neck, leaving the shoulders bare.",
      tags=["halter", "halterneck", "sleeveless", "summer", "top", "backless"], aliases=["halterneck"])
def _(S):
    pts = [(5.5, 10), (9, 8.5), (12, 11.5), (15, 8.5), (18.5, 10), (17, 15), (18, 21), (6, 21), (7, 15)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        line(poly([(8.6, 8.7), (10.8, 3), (13.2, 3), (15.4, 8.7)], r=S.r)),
    ]


@icon("off-shoulder-top", CAT, "Top with a wide straight neckline below the shoulders and short puffed sleeves.",
      tags=["off the shoulder", "bardot", "top", "blouse", "summer", "neckline"], aliases=["bardot-top"])
def _(S):
    d = ("M4 7.5H20C21.5 7.5 22 9.5 21.5 11.5C21.2 12.8 20 13.5 18.5 13.5L17.5 13.5"
         + _tail([(17.5, 13.5), (18, 20.5), (6, 20.5), (6.5, 13.5)], r=S.r)
         + "L5.5 13.5C4 13.5 2.8 12.8 2.5 11.5C2 9.5 2.5 7.5 4 7.5Z")
    return [
        shell(d),
        detail(seg(6.8, 7.5, 6.5, 13.5)), detail(seg(17.2, 7.5, 17.5, 13.5)),
    ]


@icon("one-shoulder-top", CAT, "Top with a single strap and a diagonal neckline down to the opposite underarm.",
      tags=["asymmetric", "one shoulder", "top", "evening", "neckline", "strap"], aliases=["asymmetric-top"])
def _(S):
    pts = [(6, 8), (9, 7), (18, 11), (17, 15), (18, 21), (6, 21), (7, 15)]
    return [shell(poly(pts, closed=True, r=S.r)), line(poly([(7.3, 7.6), (8.5, 3), (11, 3), (12.2, 8.7)], r=S.r))]


@icon("peplum-top", CAT, "Fitted sleeveless top with a short flared ruffle below the waist seam.",
      tags=["peplum", "flared top", "ruffle", "blouse", "top", "fitted"])
def _(S):
    top = "M8 3.5H10C10 6 10.8 7.5 12 7.5C13.2 7.5 14 6 14 3.5H16C16 6.5 16.5 8 17 10L16 14"
    hem = ("L20.5 19.5A2.83 1.5 0 0 1 14.83 19.5A2.83 1.5 0 0 1 9.17 19.5A2.83 1.5 0 0 1 3.5 19.5L8 14L7 10"
           "C7.5 8 8 6.5 8 3.5Z")
    if S.name == "rounded":
        hem = ("L20.2 18.5Q20.8 19.5 20 19.8A2.7 1.5 0 0 1 14.83 19.5A2.83 1.5 0 0 1 9.17 19.5A2.7 1.5 0 0 1 4 19.8"
               "Q3.2 19.5 3.8 18.5L8 14L7 10C7.5 8 8 6.5 8 3.5Z")
    return [shell(top + hem), detail(seg(8, 14, 16, 14))]


@icon("corset", CAT, "Hourglass bodice with a curved top edge and criss-cross lacing down the centre.",
      tags=["bustier", "bodice", "lacing", "lingerie", "victorian", "waist"], aliases=["bustier"])
def _(S):
    body = poly([(18.5, 5), (16.5, 12), (18.5, 19), (12, 21), (5.5, 19), (7.5, 12), (5.5, 5)], r=S.r) + \
        "C8 4 10.5 4.5 12 6.5C13.5 4.5 16 4 18.5 5Z"
    lace = [(10.7, 9), (13.3, 11.5), (10.7, 14), (13.3, 16.5), (10.7, 19)]
    return [shell(body), detail(poly(lace, r=S.r * 0.5)), detail(poly(_mirror(lace), r=S.r * 0.5))]


@icon("bodysuit", CAT, "One-piece long-sleeved top that ends in a high-cut brief at the hips.",
      tags=["body", "leotard", "one piece", "top", "long sleeve", "fitted"], aliases=["leotard"])
def _(S):
    pts = [(9, 3), (4.5, 4.5), (3, 14.5), (7, 14.5), (7, 15.5), (10.5, 21), (13.5, 21), (17, 15.5), (17, 14.5), (21, 14.5), (19.5, 4.5), (15, 3)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        *_seams(y0=9.5, y1=14.5),
        detail(_crew(top=3, l=9, r=15)),
    ]


_HOOD = _arc_pts(12, 7.5, 5, 180, 360, n=10)


@icon("zip-hoodie", CAT, "Hooded jacket with a full-length centre zipper and two front pockets.",
      tags=["zip up", "hooded jacket", "sweatshirt", "hoodie", "zipper", "casual"], aliases=["zip-up-hoodie"])
def _(S):
    pts = _HOOD + [(19.5, 8), (21, 19), (17, 19), (17, 21), (7, 21), (7, 19), (3, 19), (4.5, 8)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        *_seams(y0=12),
        detail(poly([(7, 8), (12, 12.5), (17, 8)], r=S.r)),
        detail(seg(12, 12.5, 12, 21)),
        detail(seg(8.6, 15, 9.6, 18.5)), detail(seg(15.4, 15, 14.4, 18.5)),
    ]


@icon("quarter-zip-pullover", CAT, "Long-sleeved pullover with a stand collar and a short zipper from the collar to mid chest.",
      tags=["quarter zip", "half zip", "pullover", "sweater", "fleece", "zip neck"], aliases=["half-zip-pullover"])
def _(S):
    pts = [(9, 2.5), (15, 2.5), (15, 5.5), (19.5, 6.5), (21, 19), (17, 19), (17, 21), (7, 21), (7, 19), (3, 19), (4.5, 6.5), (9, 5.5)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        *_seams(y0=10.5),
        detail(seg(9, 5.5, 15, 5.5)),
        detail(seg(12, 2.5, 12, 11)),
        Part("dot", rect(10.75, 10.5, 2.5, 3.5, 0 if S.name == "line" else 1.2)),
    ]


@icon("sweater-vest", CAT, "Sleeveless knit vest with a V-neck and a diamond argyle pattern.",
      tags=["argyle", "tank top", "slipover", "knitwear", "preppy", "sleeveless"], aliases=["slipover"])
def _(S):
    pts = [(8.5, 3), (6, 3.5), (5.5, 6.5), (4, 9.5), (4, 19), (5.5, 21), (18.5, 21), (20, 19), (20, 9.5), (18.5, 6.5), (18, 3.5), (15.5, 3)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(poly([(8.5, 3), (12, 9.5), (15.5, 3)], r=S.r)),
        detail(poly([(12, 12), (15, 15.5), (12, 19), (9, 15.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("tie-dye-shirt", CAT, "T-shirt with a swirl pattern spiralling out from the centre of the chest.",
      tags=["tie dye", "swirl", "hippie", "psychedelic", "tee", "dyed"], aliases=["tie-dye"])
def _(S):
    c = (12, 14)
    arms = []
    for a in (-90, 30, 150):
        e = polar(*c, 3.3, a)
        k = polar(*c, 3.0, a - 55)
        arms.append(detail(f"M{fmt(c[0])} {fmt(c[1])}Q{fmt(k[0])} {fmt(k[1])} {fmt(e[0])} {fmt(e[1])}"))
    return [shell(poly(_tee(hem=21), closed=True, r=S.r)), detail(_crew()), *arms]


_REF = poly(_tee(hem=21), closed=True)
_REF_BANDS = [(9, 9, 2, 10.5), (13, 9, 2, 10.5)]
_REF_COLLAR = poly([(8.5, 3.5), (10, 7.5), (12, 5.5), (14, 7.5), (15.5, 3.5)])


def _ref_filled():
    return D(_solid_body(_REF), *[P(rect(*b)) for b in _REF_BANDS], ST(_REF_COLLAR, 2))


@icon("referee-shirt", CAT, "Short-sleeved collared shirt with bold vertical stripes.",
      tags=["referee", "umpire", "official", "striped shirt", "sport", "match"], aliases=["umpire-shirt"],
      filled=_ref_filled)
def _(S):
    outline = poly(_tee(hem=21), closed=True, r=S.r)
    return [
        shell(outline),
        *[Part("dot", rect(x, y, w, h + 1)) for x, y, w, h in _REF_BANDS],
        detail(poly([(8.5, 3.5), (10, 7.5), (12, 5.5), (14, 7.5), (15.5, 3.5)], r=S.r)),
    ]


@icon("sailor-suit", CAT, "Top with a deep sailor collar and a neckerchief knotted at the point of the V.",
      tags=["sailor", "navy", "middy", "marine", "costume", "neckerchief"], aliases=["sailor-top"])
def _(S):
    return [
        shell(poly(_tee(hem=21), closed=True, r=S.r)),
        detail(poly([(8.5, 3.5), (12, 11), (15.5, 3.5)], r=S.r)),
        detail(poly([(6.5, 4.6), (7.5, 8), (10.5, 9.5)], r=S.r)), detail(poly([(17.5, 4.6), (16.5, 8), (13.5, 9.5)], r=S.r)),
        Part("dot", poly([(10.3, 11.5), (13.7, 11.5), (12, 14)], closed=True, r=S.r * 0.4)),
        detail(seg(11.3, 13.5, 10.3, 18)), detail(seg(12.7, 13.5, 13.7, 18)),
    ]


_CLER = poly(_ls(), closed=True)


def _cler_filled():
    body = _solid_body(_CLER)
    return D(body, P(rect(10.8, 3, 2.4, 3)), ST(seg(7, 10, 7, 19), 2), ST(seg(17, 10, 17, 19), 2))


@icon("clerical-collar-shirt", CAT, "Long-sleeved shirt with a dark band collar and a small white tab at the throat.",
      tags=["clergy", "priest", "dog collar", "minister", "church", "pastor"], aliases=["clergy-shirt"],
      filled=_cler_filled)
def _(S):
    return [
        shell(poly(_ls(), closed=True, r=S.r)),
        *_seams(),
        Part("dot", rect(9, 2.5, 1.8, 4)), Part("dot", rect(13.2, 2.5, 1.8, 4)),
        detail(seg(9, 6, 15, 6)),
        detail(seg(12, 6, 12, 21)),
    ]


@icon("tailcoat", CAT, "Formal coat cut short at the waist in front, with two long pointed tails hanging behind.",
      tags=["tails", "white tie", "formal", "evening wear", "conductor", "tuxedo"], aliases=["tails"])
def _(S):
    pts = [(9, 3), (4.5, 4.5), (3, 15.5), (6.5, 15.5), (8, 21), (9.5, 21), (10.5, 12.5), (13.5, 12.5), (14.5, 21), (16, 21),
           (17.5, 15.5), (21, 15.5), (19.5, 4.5), (15, 3)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(7, 9.5, 6.6, 15.5)), detail(seg(17, 9.5, 17.4, 15.5)),
        detail(poly([(9, 3), (12, 9.5), (15, 3)], r=S.r)),
    ]


@icon("double-breasted-jacket", CAT, "Suit jacket with wide lapels and two vertical rows of buttons.",
      tags=["double breasted", "blazer", "suit", "formal", "jacket", "buttons"], aliases=["double-breasted-blazer"])
def _(S):
    pts = [(6, 3.5), (12, 11.5), (18, 3.5), (20, 4.5), (21, 8), (21, 21), (3, 21), (3, 8), (4, 4.5)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(poly([(4.8, 4.2), (7, 9.5), (9.5, 10)], r=S.r)), detail(poly([(19.2, 4.2), (17, 9.5), (14.5, 10)], r=S.r)),
        dot(9, 14.5, 1.2), dot(15, 14.5, 1.2), dot(9, 18, 1.2), dot(15, 18, 1.2),
    ]


def _puffer_pts():
    left = [(9, 2.5), (9, 5), (5, 5.5), (3, 7.5), (3.8, 9), (2.6, 11), (3.4, 13), (2.4, 15), (3.2, 17), (2.3, 19), (3, 21)]
    return left + [(21, 21)] + [(24 - x, y) for x, y in reversed(left[1:-1])] + [(15, 2.5)]


@icon("puffer-jacket", CAT, "Quilted jacket made of stacked puffy baffles with a high zipped collar.",
      tags=["puffer", "down jacket", "quilted", "padded", "winter coat", "puffy"], aliases=["down-jacket"])
def _(S):
    return [
        shell(poly(_puffer_pts(), closed=True, r=S.r)),
        detail(seg(3.8, 9, 20.2, 9)), detail(seg(3.4, 13, 20.6, 13)), detail(seg(3.2, 17, 20.8, 17)),
        detail(seg(12, 2.5, 12, 21)),
    ]


@icon("parka", CAT, "Long winter coat with a fur-trimmed hood and big flap pockets.",
      tags=["winter coat", "anorak", "fur hood", "arctic", "cold", "outerwear"], aliases=["fur-hood-coat"])
def _(S):
    hood = [polar(12, 8.5, 6.3 if i % 2 else 5.4, 180 + i * 15) for i in range(13)]
    pts = hood + [(19.5, 9.5), (21, 18), (17.5, 18), (18, 21.5), (6, 21.5), (6.5, 18), (3, 18), (4.5, 9.5)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.4)),
        detail(poly([(7.3, 9.5), (12, 13), (16.7, 9.5)], r=S.r)),
        detail(seg(6.9, 13.5, 6.6, 18)), detail(seg(17.1, 13.5, 17.4, 18)),
        detail(poly([(8.3, 16), (11, 16), (11, 18.5)], r=S.r * 0.5)), detail(poly([(15.7, 16), (13, 16), (13, 18.5)], r=S.r * 0.5)),
    ]


@icon("denim-jacket", CAT, "Button jacket with a pointed collar, two flap chest pockets and a waistband.",
      tags=["jean jacket", "denim", "trucker jacket", "casual", "jacket", "western"], aliases=["jean-jacket"])
def _(S):
    flap = [(8.2, 9.5), (10.8, 9.5), (10.8, 11.2), (9.5, 12.5), (8.2, 11.2)]
    return [
        shell(poly(_ls(), closed=True, r=S.r)),
        *_seams(),
        detail(poly([(9, 3), (10, 7.5), (12, 5.5), (14, 7.5), (15, 3)], r=S.r)),
        detail(seg(12, 5.5, 12, 21)),
        Part("dot", poly(flap, closed=True, r=S.r * 0.3)), Part("dot", poly(_mirror(flap), closed=True, r=S.r * 0.3)),
        detail(seg(7, 17.5, 17, 17.5)),
    ]


# ============================================================================ outerwear, robes and one-pieces

@icon("cape", CAT, "Short cloak hanging from the shoulders in a wide bell, tied with a bow at the neck.",
      tags=["cloak", "mantle", "superhero", "costume", "cape", "shoulders"], aliases=["mantle"])
def _(S):
    return [
        shell(poly([(9, 5.5), (15, 5.5), (17.5, 7.5), (21, 20), (3, 20), (6.5, 7.5)], closed=True, r=S.r)),
        line(poly([(8.5, 2.5), (15.5, 7.5), (15.5, 2.5), (8.5, 7.5)], closed=True, r=S.r * 0.3)),
        detail(seg(9.5, 11, 8.5, 20)), detail(seg(14.5, 11, 15.5, 20)),
    ]


@icon("cloak", CAT, "Long hooded cloak falling to the ground in folds, with a round clasp at the throat.",
      tags=["hooded cloak", "robe", "mantle", "wizard", "fantasy", "medieval"], aliases=["hooded-cloak"])
def _(S):
    top = "M12 2C15.5 2 17.5 4.5 17.5 8"
    d = top + _tail([(17.5, 8), (20.5, 21.5), (3.5, 21.5), (6.5, 8)], r=S.r) + "C6.5 4.5 8.5 2 12 2Z"
    return [
        shell(d),
        Part("dot", ellipse(12, 7.5, 2.8, 3.2)),
        Part("dot", circle(12, 13, 1.4)),
        detail(seg(9.5, 15.5, 8.5, 21.5)), detail(seg(14.5, 15.5, 15.5, 21.5)),
    ]


@icon("poncho", CAT, "Poncho with a neck opening, a woven stripe and fringe along the lower edges.",
      tags=["cape", "serape", "blanket", "mexican", "andean", "rain poncho"], aliases=["serape"])
def _(S):
    edge = lambda x: 14 + abs(x - 12) * -5 / 9.5 + 5  # noqa: E731  (y of the lower edge at x)
    fringe = [detail(seg(x, edge(x) + 0.5, x, edge(x) + 2.5)) for x in (5.5, 8.8, 12, 15.2, 18.5)]
    return [
        shell(poly([(9, 3.5), (15, 3.5), (21.5, 14), (12, 19), (2.5, 14)], closed=True, r=S.r)),
        detail(_crew(top=3.5, l=9, r=15, depth=2.3)),
        detail(seg(4.4, 11, 19.6, 11)),
        *fringe,
    ]


@icon("scrubs", CAT, "Short-sleeved V-neck medical top with a chest pocket holding a pen.",
      tags=["medical", "nurse", "doctor", "hospital", "uniform", "healthcare"], aliases=["scrub-top"])
def _(S):
    return [
        shell(poly(_tee(hem=21), closed=True, r=S.r)),
        detail(poly([(8.5, 3.5), (12, 9.5), (15.5, 3.5)], r=S.r)),
        Part("dot", rect(12.5, 13.5, 3, 3.5, 0 if S.name == "line" else 0.8)),
        detail(seg(14, 10, 14, 13.5)),
    ]


@icon("high-visibility-vest", CAT, "Sleeveless safety vest with horizontal reflective stripes and stripes over the shoulders.",
      tags=["hi-vis", "safety vest", "reflective", "construction", "workwear", "high vis"], aliases=["hi-vis-vest", "safety-vest"])
def _(S):
    pts = [(8.5, 3), (6, 3.5), (5.5, 7), (4, 9.5), (4, 21), (20, 21), (20, 9.5), (18.5, 7), (18, 3.5), (15.5, 3)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(poly([(8.5, 3), (12, 10), (15.5, 3)], r=S.r)),
        detail(seg(12, 10, 12, 21)),
        detail(seg(4, 14, 20, 14)), detail(seg(4, 18, 20, 18)),
        detail(seg(7.4, 3.5, 7.4, 14)), detail(seg(16.6, 3.5, 16.6, 14)),
    ]


@icon("hazmat-suit", CAT, "Full-body protective suit with an attached hood, a clear face visor and sealed gloves and boots.",
      tags=["hazmat", "protective suit", "biohazard", "chemical", "decontamination", "ppe"], aliases=["protective-suit"])
def _(S):
    hood = _arc_pts(12, 6, 4.5, 180, 360, n=8)
    pts = [(7.5, 9.5)] + hood + [(16.5, 9.5), (19.5, 10.5), (21, 17), (17, 17), (17.5, 21.5), (13, 21.5), (12, 17.5),
                                 (11, 21.5), (6.5, 21.5), (7, 17), (3, 17), (4.5, 10.5)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(rect(9.5, 4.5, 5, 3.5, min(S.R, 1.5))),
        detail(seg(7, 13, 7, 17)), detail(seg(17, 13, 17, 17)),
        detail(seg(3.3, 15, 6.9, 15)), detail(seg(17.1, 15, 20.7, 15)),
        detail(seg(6.7, 19.5, 11.4, 19.5)), detail(seg(12.6, 19.5, 17.3, 19.5)),
    ]


@icon("graduation-gown", CAT, "Academic gown with wide bell sleeves and a front opening.",
      tags=["academic gown", "graduation", "commencement", "robe", "graduate", "ceremony"], aliases=["academic-gown"])
def _(S):
    pts = [(9, 3), (4.5, 4.5), (2, 15), (7, 15), (6.5, 21), (17.5, 21), (17, 15), (22, 15), (19.5, 4.5), (15, 3)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(7.2, 9.5, 7, 15)), detail(seg(16.8, 9.5, 17, 15)),
        detail(poly([(9, 3), (12, 8), (15, 3)], r=S.r)),
        detail(seg(12, 8, 12, 21)),
    ]


def _onepiece(cuff=13.5):
    return [(9, 3), (4.5, 4.5), (3, cuff), (7, cuff), (6, 21), (10, 21), (12, 15), (14, 21), (18, 21), (17, cuff),
            (21, cuff), (19.5, 4.5), (15, 3)]


@icon("wetsuit", CAT, "Full-body neoprene suit with long arms and legs, a chest panel seam and a zip pull.",
      tags=["diving suit", "surfing", "neoprene", "scuba", "swimming", "watersports"], aliases=["diving-suit"])
def _(S):
    pts = [(10, 3), (4.5, 4.5), (3, 13.5), (7, 13.5), (6, 21), (10, 21), (12, 15), (14, 21), (18, 21), (17, 13.5),
           (21, 13.5), (19.5, 4.5), (14, 3)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(7, 9, 7, 13.5)), detail(seg(17, 9, 17, 13.5)),
        detail("M4.2 7.5C8 10.5 16 10.5 19.8 7.5"),
        detail(seg(12, 3, 12, 6.5)),
    ]


@icon("jumpsuit", CAT, "One-piece garment with long sleeves and long legs, a collar and a belted waist.",
      tags=["boiler suit", "coveralls", "one piece", "overall", "flight suit", "romper"], aliases=["boiler-suit"])
def _(S):
    return [
        shell(poly(_onepiece(), closed=True, r=S.r)),
        detail(seg(7, 9, 7, 13.5)), detail(seg(17, 9, 17, 13.5)),
        detail(poly([(9, 3), (10, 7), (12, 5), (14, 7), (15, 3)], r=S.r)),
        detail(seg(12, 5, 12, 9)),
        detail(seg(7, 11.5, 17, 11.5)),
    ]


@icon("romper", CAT, "One-piece short-sleeved top joined to short shorts, with a tie belt at the waist.",
      tags=["playsuit", "one piece", "shorts", "summer", "jumpsuit", "outfit"], aliases=["playsuit"])
def _(S):
    pts = [(8.5, 4), (3, 7), (4.5, 11.5), (7, 10.5), (7, 13.5), (6, 20), (11, 20), (12, 17), (13, 20), (18, 20),
           (17, 13.5), (17, 10.5), (19.5, 11.5), (21, 7), (15.5, 4)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(_crew(top=4)),
        detail(seg(7, 13.5, 17, 13.5)),
        line(poly([(10.5, 13.5), (9, 16.5)], r=S.r)),
    ]


@icon("baby-onesie", CAT, "Small short-sleeved baby bodysuit with an envelope neckline and snaps at the crotch.",
      tags=["onesie", "babygrow", "baby", "infant", "bodysuit", "newborn"], aliases=["babygrow"])
def _(S):
    pts = [(9, 4), (4, 6.5), (5, 10.5), (7.5, 10), (7.5, 14.5), (9.5, 20), (14.5, 20), (16.5, 14.5), (16.5, 10), (19, 10.5), (20, 6.5), (15, 4)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(_crew(top=4, l=9, r=15, depth=2.2)),
        dot(10.1, 17.6, 0.8), dot(12, 17.6, 0.8), dot(13.9, 17.6, 0.8),
    ]


@icon("nightgown", CAT, "Long loose sleeveless nightdress reaching the ankles, with a gathered yoke at the neckline.",
      tags=["nightdress", "nightie", "sleepwear", "nightwear", "bedtime", "chemise"], aliases=["nightdress", "nightie"])
def _(S):
    return [
        shell(poly([(8, 6), (16, 6), (17, 9.5), (20, 21), (4, 21), (7, 9.5)], closed=True, r=S.r)),
        line(seg(8.7, 6, 8.7, 2.5)), line(seg(15.3, 6, 15.3, 2.5)),
        detail(seg(7, 9.5, 17, 9.5)),
        detail(seg(10, 9.5, 9, 21)), detail(seg(14, 9.5, 15, 21)),
    ]


@icon("long-johns", CAT, "One-piece thermal underwear with long sleeves, long legs and a button placket down the chest.",
      tags=["union suit", "thermal underwear", "base layer", "winter", "underwear", "one piece"], aliases=["union-suit"])
def _(S):
    return [
        shell(poly(_onepiece(), closed=True, r=S.r)),
        detail(seg(7, 9, 7, 13.5)), detail(seg(17, 9, 17, 13.5)),
        detail(_crew(top=3, l=9, r=15, depth=2.3)),
        dot(12, 8, 1), dot(12, 11.2, 1), dot(12, 14.4, 1),
        detail(seg(3.3, 11.3, 7, 11.3)), detail(seg(17, 11.3, 20.7, 11.3)),
    ]


# ============================================================================ trousers, shorts and skirts

_PANTS = [(6, 3), (18, 3), (19.5, 21), (14, 21), (12, 11.5), (10, 21), (4.5, 21)]


@icon("waders", CAT, "Chest-high waterproof trousers with attached boots and shoulder straps.",
      tags=["fishing waders", "chest waders", "angling", "waterproof", "boots", "fly fishing"], aliases=["chest-waders"])
def _(S):
    pts = [(8, 7), (16, 7), (16, 10.5), (18, 10.5), (18.5, 17.5), (21, 19), (21, 21.5), (13.5, 21.5), (13.5, 17.5), (12, 14),
           (10.5, 17.5), (10.5, 21.5), (3, 21.5), (3, 19), (5.5, 17.5), (6, 10.5), (8, 10.5)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        line(seg(8.5, 7, 7, 2.5)), line(seg(15.5, 7, 17, 2.5)),
        detail(seg(6, 10.5, 18, 10.5)),
        detail(seg(5.6, 17.5, 10.5, 17.5)), detail(seg(13.5, 17.5, 18.4, 17.5)),
    ]


@icon("cargo-pants", CAT, "Trousers with a large flap pocket on the side of each thigh.",
      tags=["cargo trousers", "combat trousers", "utility pants", "pockets", "outdoor", "workwear"], aliases=["cargo-trousers"])
def _(S):
    rr = 0 if S.name == "line" else 0.8
    return [
        shell(poly(_PANTS, closed=True, r=S.r)),
        detail(seg(5.67, 7, 18.33, 7)),
        Part("dot", rect(6.3, 11.5, 3, 4, rr)), Part("dot", rect(14.7, 11.5, 3, 4, rr)),
    ]


@icon("sweatpants", CAT, "Loose trousers with a drawstring waistband and elastic cuffs gathered at the ankles.",
      tags=["joggers", "tracksuit bottoms", "track pants", "sweats", "loungewear", "gym"], aliases=["joggers"])
def _(S):
    pts = [(6, 3), (18, 3), (19.5, 15.5), (17.5, 18), (17.5, 21), (13.5, 21), (13.5, 18), (12, 11.5), (10.5, 18),
           (10.5, 21), (6.5, 21), (6.5, 18), (4.5, 15.5)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(5.6, 6.5, 18.4, 6.5)),
        line(seg(11, 6.5, 10.3, 10)), line(seg(13, 6.5, 13.7, 10)),
        detail(seg(6.5, 18, 10.5, 18)), detail(seg(13.5, 18, 17.5, 18)),
    ]


@icon("bell-bottoms", CAT, "Trousers fitted at the thigh that flare out wide from the knee to the hem.",
      tags=["flares", "flared trousers", "70s", "retro", "disco", "hippie"], aliases=["flares"])
def _(S):
    pts = [(6.5, 3), (17.5, 3), (16.5, 13), (20.5, 21), (13.5, 21), (12, 11), (10.5, 21), (3.5, 21), (7.5, 13)]
    return [shell(poly(pts, closed=True, r=S.r)), detail(seg(6.2, 6.5, 17.8, 6.5))]


@icon("ripped-jeans", CAT, "Jeans with jagged tears across both knees.",
      tags=["distressed jeans", "torn jeans", "denim", "destroyed", "grunge", "trousers"], aliases=["distressed-jeans"])
def _(S):
    tear = [(5.4, 14.5), (6.6, 13), (7.8, 14.5), (9, 13), (10, 14)]
    return [
        shell(poly(_PANTS, closed=True, r=S.r)),
        detail(seg(5.67, 7, 18.33, 7)),
        detail(poly(tear, r=S.r * 0.3)), detail(poly(_mirror(tear), r=S.r * 0.3)),
    ]


@icon("harem-pants", CAT, "Very baggy trousers with a low drop crotch and legs gathered tightly at the ankles.",
      tags=["harem trousers", "baggy", "aladdin pants", "drop crotch", "yoga", "loose"], aliases=["harem-trousers"])
def _(S):
    pts = [(7, 3), (17, 3), (20, 8), (21, 13), (18.5, 17.5), (16.5, 19), (16.5, 21.5), (13.5, 21.5), (13.5, 19), (12, 17),
           (10.5, 19), (10.5, 21.5), (7.5, 21.5), (7.5, 19), (5.5, 17.5), (3, 13), (4, 8)]
    return [
        shell(poly(pts, closed=True, r=S.r * 1.5)),
        detail(seg(6, 6.5, 18, 6.5)),
        detail(seg(7.5, 19, 10.5, 19)), detail(seg(13.5, 19, 16.5, 19)),
    ]


@icon("jodhpurs", CAT, "Riding breeches that balloon out wide at the thighs and fit tightly from the knee down.",
      tags=["riding breeches", "equestrian", "horse riding", "breeches", "jodhpur", "riding"], aliases=["riding-breeches"])
def _(S):
    pts = [(7, 3), (17, 3), (20.5, 8), (19.5, 11.5), (16.5, 14), (16.5, 21), (13, 21), (12, 11.5), (11, 21), (7.5, 21),
           (7.5, 14), (4.5, 11.5), (3.5, 8)]
    return [
        shell(poly(pts, closed=True, r=S.r * 1.5)),
        detail(seg(5.6, 6.5, 18.4, 6.5)),
        detail(seg(7.5, 15.5, 11, 15.5)), detail(seg(13, 15.5, 16.5, 15.5)),
    ]


@icon("lederhosen", CAT, "Leather shorts with an H-shaped pair of braces joined by a chest strap.",
      tags=["bavarian", "oktoberfest", "german", "traditional", "shorts", "braces"], aliases=["bavarian-shorts"])
def _(S):
    return [
        shell(poly([(6, 11.5), (18, 11.5), (19, 20), (13.5, 20.5), (12, 16.5), (10.5, 20.5), (5, 20)], closed=True, r=S.r)),
        line(seg(8.5, 11.5, 8.5, 3)), line(seg(15.5, 11.5, 15.5, 3)),
        line(seg(8.5, 7, 15.5, 7)),
        detail(seg(5.8, 14, 18.2, 14)),
    ]


_KILT = poly([(6, 4), (18, 4), (19.5, 19), (4.5, 19)], closed=True)


@icon("kilt", CAT, "Knee-length tartan kilt with a waistband and a sporran pouch hanging at the front.",
      tags=["scottish", "tartan", "highland", "plaid", "sporran", "skirt"], aliases=["highland-kilt"])
def _(S):
    pouch = "M10 11.5H14V15.5C14 16.9 13.1 17.5 12 17.5C10.9 17.5 10 16.9 10 15.5Z" if S.name == "rounded" else \
        poly([(10, 11.5), (14, 11.5), (14, 16), (12, 17.5), (10, 16)], closed=True)
    return [
        shell(poly([(6, 4), (18, 4), (19.5, 19), (4.5, 19)], closed=True, r=S.r)),
        detail(seg(5.7, 7, 18.3, 7)),
        detail(seg(8, 7, 7.3, 19)), detail(seg(16, 7, 16.7, 19)),
        detail(seg(5.2, 14, 8, 14)), detail(seg(16, 14, 18.8, 14)),
        Part("dot", pouch),
        detail(seg(12, 7, 12, 11.5)),
    ]


@icon("chaps", CAT, "Pair of leather leg coverings on a belt, open at the seat, with fringed outer edges.",
      tags=["cowboy", "western", "leather", "rodeo", "riding", "motorcycle"], aliases=["leather-chaps"])
def _(S):
    leg = [(4.5, 9), (10, 9), (9.5, 21), (5.5, 21)]
    ex = lambda y: 4.5 + (y - 9) / 12  # noqa: E731
    fr = [detail(seg(ex(y), y, ex(y) - 2.2, y)) for y in (12.5, 16.5)]
    fr += [detail(seg(24 - ex(y), y, 26.2 - ex(y), y)) for y in (12.5, 16.5)]
    return [
        shell(rect(3.5, 3, 17, 3.5, min(S.R, 1.5))),
        dot(12, 4.75, 1),
        shell(poly(leg, closed=True, r=S.r)), shell(poly(_mirror(leg), closed=True, r=S.r)),
        *fr,
    ]


@icon("sarong", CAT, "Length of cloth wrapped around the hips and knotted at one side, falling to the ankle.",
      tags=["pareo", "wrap skirt", "lungi", "beach", "sarong", "wrap"], aliases=["pareo"])
def _(S):
    return [
        shell(poly([(6.5, 4), (17.5, 4), (18.5, 21), (5.5, 21)], closed=True, r=S.r)),
        detail(seg(6.3, 7, 17.7, 7)),
        Part("dot", circle(15, 9.5, 1.7)),
        detail(seg(14, 11, 10, 21)),
        detail(poly([(15.8, 11), (16.3, 16)], r=S.r)),
    ]


@icon("hakama", CAT, "Wide pleated trousers that look like a long skirt, tied around the waist.",
      tags=["japanese", "martial arts", "kendo", "aikido", "traditional", "trousers"], aliases=["japanese-trousers"])
def _(S):
    pts = [(7, 4), (17, 4), (21, 21), (14, 21), (12, 15), (10, 21), (3, 21)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(6.6, 7, 17.4, 7)),
        detail(seg(9.5, 7, 7.5, 21)), detail(seg(14.5, 7, 16.5, 21)),
        line(poly([(10.5, 7), (9, 10.5)], r=S.r)), line(poly([(13.5, 7), (15, 10.5)], r=S.r)),
    ]


@icon("suspenders", CAT, "Two braces crossing in an X at the back and clipped to the waistband of a pair of trousers.",
      tags=["braces", "suspender", "clips", "trousers", "menswear", "straps"], aliases=["trouser-braces"])
def _(S):
    rr = 0 if S.name == "line" else 0.8
    return [
        line(seg(7, 2.5, 16.2, 15.5)), line(seg(17, 2.5, 7.8, 15.5)),
        shell(rect(3.5, 15.5, 17, 5, min(S.R, 2))),
        Part("dot", rect(6.3, 13.5, 3, 4, rr)), Part("dot", rect(14.7, 13.5, 3, 4, rr)),
        Part("dot", poly([(12, 6.3), (14, 9.1), (12, 11.9), (10, 9.1)], closed=True, r=S.r * 0.3)),
    ]


_GAR_IN = ellipse(12, 11, 6, 2.5)


def _garter_outer():
    pts = []
    for i in range(24):
        a = i * 15
        rx, ry = (9, 5.2) if i % 2 == 0 else (8.2, 4.4)
        x, _ = polar(0, 0, rx, a)
        _, y = polar(0, 0, ry, a)
        pts.append((12 + x, 12 + y))
    return pts


def _garter_filled():
    outer = poly(_garter_outer(), closed=True)
    bow = poly([(8.5, 14.5), (12, 16.5), (15.5, 14.5), (15.5, 19.5), (12, 17.5), (8.5, 19.5)], closed=True)
    return U(D(_solid_body(outer), P(_GAR_IN), ST(_GAR_IN, 2)), _solid_body(bow))


@icon("garter", CAT, "Lace-edged elastic leg band with a ruffled edge and a small bow.",
      tags=["wedding garter", "lingerie", "bridal", "lace", "leg band", "hosiery"], aliases=["leg-garter"],
      filled=_garter_filled)
def _(S):
    return [
        shell(poly(_garter_outer(), closed=True, r=S.r * 0.4)),
        detail(_GAR_IN),
        shell(poly([(8.5, 14.5), (12, 16.5), (15.5, 14.5), (15.5, 19.5), (12, 17.5), (8.5, 19.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("pencil-skirt", CAT, "Straight narrow skirt reaching the knee, with a short slit at the hem.",
      tags=["office skirt", "straight skirt", "fitted", "workwear", "business", "skirt"], aliases=["straight-skirt"])
def _(S):
    return [
        shell(poly([(7.5, 3.5), (16.5, 3.5), (18, 10), (16, 20.5), (8, 20.5), (6, 10)], closed=True, r=S.r * 1.5)),
        detail(seg(7.1, 6.5, 16.9, 6.5)),
        detail(seg(12, 20.5, 12, 16.5)),
    ]


@icon("tutu", CAT, "Ballet bodice above a skirt of stiff layered tulle sticking straight out around the waist.",
      tags=["ballet", "ballerina", "dance", "tulle", "costume", "skirt"], aliases=["ballet-tutu"])
def _(S):
    bodice = "M9 3H10.3C10.5 4.6 11.2 5.5 12 5.5C12.8 5.5 13.5 4.6 13.7 3H15" + _tail([(15, 3), (15.5, 11), (8.5, 11), (9, 3)], r=S.r) + "Z"
    tut = [(8.5, 11), (15.5, 11), (21.5, 13.5), (20, 15.5), (18.5, 14.5), (17, 16.5), (15.5, 15), (13.75, 17), (12, 15.3),
           (10.25, 17), (8.5, 15), (7, 16.5), (5.5, 14.5), (4, 15.5), (2.5, 13.5)]
    return [shell(bodice), shell(poly(tut, closed=True, r=S.r * 0.3)), detail(seg(4.5, 13.5, 19.5, 13.5))]


@icon("hoop-skirt", CAT, "Bell-shaped skirt with horizontal hoop rings showing through it.",
      tags=["crinoline", "petticoat", "victorian", "bell skirt", "hoops", "costume"], aliases=["crinoline"])
def _(S):
    left = [(9, 3.5), (7.8, 7.5), (5.8, 12), (4.3, 16), (3.5, 20.5)]
    pts = left + [(24 - x, y) for x, y in reversed(left)]
    hoops = []
    for (xl, y) in [(7.5, 8.5), (5.6, 12.5), (4.2, 16.5)]:
        hoops.append(detail(f"M{fmt(xl)} {fmt(y)}Q12 {fmt(y + 2)} {fmt(24 - xl)} {fmt(y)}"))
    return [shell(poly(pts, closed=True, r=S.r * 1.5)), *hoops]


@icon("grass-skirt", CAT, "Waistband with long strands of grass hanging down from it.",
      tags=["hula skirt", "hawaiian", "luau", "tropical", "polynesian", "costume"], aliases=["hula-skirt"])
def _(S):
    tops = [6.5, 9.25, 12, 14.75, 17.5]
    bots = [3.5, 7.75, 12, 16.25, 20.5]
    return [
        shell(rect(4.5, 3, 15, 4, min(S.R, 1.5))),
        *[line(seg(t, 8, b, 21)) for t, b in zip(tops, bots)],
    ]


# ============================================================================ dresses and gowns

@icon("ball-gown", CAT, "Gown with a fitted strapless bodice and a huge full skirt spreading to the floor.",
      tags=["ball dress", "formal", "princess", "prom", "gala", "gown"], aliases=["ball-dress"])
def _(S):
    pts = [(8.5, 4), (10.5, 3.5), (12, 4.5), (13.5, 3.5), (15.5, 4), (15, 10), (19, 13), (21.5, 21), (2.5, 21), (5, 13), (9, 10)]
    return [
        shell(poly(pts, closed=True, r=S.r * 1.3)),
        detail(seg(9, 10, 15, 10)),
        detail(seg(10.3, 12.5, 8.5, 21)), detail(seg(13.7, 12.5, 15.5, 21)),
    ]


@icon("evening-gown", CAT, "Slim floor-length gown with thin straps and a high slit up one leg.",
      tags=["evening dress", "formal", "red carpet", "cocktail", "gala", "gown"], aliases=["evening-dress"])
def _(S):
    pts = [(9, 6.5), (15, 6.5), (16, 11), (15.5, 15), (17.5, 21), (6.5, 21), (8.5, 15), (8, 11)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        line(seg(9.5, 6.5, 9, 2.5)), line(seg(14.5, 6.5, 15, 2.5)),
        detail(seg(14.2, 21, 13.2, 14)),
    ]


@icon("mermaid-gown", CAT, "Floor-length gown fitted closely down to the knee, then flaring out wide like a fish tail.",
      tags=["mermaid dress", "trumpet dress", "fishtail", "formal", "bridal", "gown"], aliases=["mermaid-dress"])
def _(S):
    pts = [(8.5, 4), (10.5, 3.5), (12, 4.5), (13.5, 3.5), (15.5, 4), (15.5, 10), (15, 15), (20.5, 21), (3.5, 21), (9, 15), (8.5, 10)]
    return [shell(poly(pts, closed=True, r=S.r)), detail(seg(9, 15, 15, 15))]


@icon("wedding-gown", CAT, "Long gown with a sweetheart bodice, a full skirt and a long train trailing behind.",
      tags=["wedding dress", "bridal", "bride", "marriage", "train", "gown"], aliases=["wedding-dress", "bridal-gown"])
def _(S):
    top = "M7.5 4.5C9 3 11 3 12 5C13 3 15 3 16.5 4.5"
    rest = _tail([(16.5, 4.5), (15.5, 10.5), (18, 14.5), (21.5, 21.5)], r=S.r * 1.3) + "Q11 21.5 4.5 19.5" + \
        _tail([(4.5, 19.5), (6.5, 14.5), (8.5, 10.5), (7.5, 4.5)], r=S.r * 1.3)
    return [
        shell(top + rest + "Z"),
        detail(seg(8.5, 10.5, 15.5, 10.5)),
        detail("M12 10.5Q13.5 15.5 16.5 20.8"),
    ]


@icon("wrap-dress", CAT, "Dress with a crossover V neckline and a tie bow at the side of the waist.",
      tags=["wrap", "crossover", "day dress", "v-neck", "tie waist", "dress"], aliases=["crossover-dress"])
def _(S):
    pts = [(9, 3.5), (4.5, 6), (5.5, 10), (7.5, 9.5), (8, 12), (5, 21), (19, 21), (16, 12), (16.5, 9.5), (18.5, 10), (19.5, 6), (15, 3.5)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(9, 3.5, 15.5, 12)), detail(seg(15, 3.5, 12.4, 7.9)),
        detail(seg(8, 12, 16, 12)),
        detail(seg(15.2, 12, 13.2, 21)),
        line(poly([(16.5, 12), (19.5, 16)], r=S.r)),
    ]


@icon("flapper-dress", CAT, "Straight drop-waist sleeveless dress with rows of hanging fringe.",
      tags=["1920s", "roaring twenties", "charleston", "gatsby", "fringe", "dress"], aliases=["twenties-dress"])
def _(S):
    teeth = []
    for i in range(7):
        x = 18.5 - i * 13 / 6
        teeth.append((x, 20))
        if i < 6:
            teeth.append((x - 13 / 12, 21.5))
    top = "M8 3H10C10 5.5 10.8 7 12 7C13.2 7 14 5.5 14 3H16C16 6 17 8.5 18.5 9.5"
    zz = [(5.8, 16.5)] + [(5.8 + (i + 1) * 12.4 / 8, 15 if i % 2 == 0 else 16.5) for i in range(8)]
    return [
        shell(top + _tail([(18.5, 9.5)] + teeth + [(5.5, 9.5)], r=S.r * 0.3) + "C7 8.5 8 6 8 3Z"),
        detail(seg(5.5, 12.5, 18.5, 12.5)),
        detail(poly(zz, r=S.r * 0.3)),
    ]


@icon("flamenco-dress", CAT, "Fitted dress that bursts into tiers of ruffles from the knee down to the floor.",
      tags=["flamenco", "spanish", "sevillana", "ruffles", "dance", "dress"], aliases=["ruffle-dress"])
def _(S):
    def scallop(x0, x1, y, n):
        w = (x1 - x0) / n
        return "".join(f"A{fmt(w / 2)} 1.3 0 0 1 {fmt(x1 - (i + 1) * w)} {fmt(y)}" for i in range(n))
    top = poly([(9, 3), (15, 3), (16, 8), (15, 12), (18.5, 15.5)], r=S.r)
    d = top + "L17.5 16L21 20.5" + scallop(3, 21, 20.5, 5) + "L6.5 16L5.5 15.5" + \
        _tail([(5.5, 15.5), (9, 12), (8, 8), (9, 3)], r=S.r) + "Z"
    return [
        shell(d),
        detail(_crew(top=3, l=9, r=15, depth=2.2)),
        detail("M18.5 15.5" + scallop(5.5, 18.5, 15.5, 4)),
    ]


# ============================================================================ dress from around the world

@icon("qipao", CAT, "Fitted dress with a mandarin collar, a curved closure across the chest and a side slit.",
      tags=["cheongsam", "chinese dress", "mandarin collar", "traditional", "silk", "dress"], aliases=["cheongsam"])
def _(S):
    pts = [(10.5, 2.5), (13.5, 2.5), (13.5, 4.5), (16, 5), (18.5, 6), (18, 9), (16, 8.5), (15.5, 12), (16.5, 21),
           (7.5, 21), (8.5, 12), (8, 8.5), (6, 9), (5.5, 6), (8, 5), (10.5, 4.5)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(10.5, 4.5, 13.5, 4.5)),
        detail("M12 4.5C12.5 7 14 8.3 16.2 8.8"),
        dot(13.5, 11, 1.1),
        detail(seg(9.2, 21, 9.6, 16.5)),
    ]


@icon("ao-dai", CAT, "Long fitted tunic with a stand collar and side slits from the waist, worn over loose trousers.",
      tags=["vietnamese", "tunic", "traditional", "silk", "long dress", "national dress"], aliases=["vietnamese-tunic"])
def _(S):
    tunic = [(10.5, 2.5), (13.5, 2.5), (13.5, 4), (17, 5), (20.5, 14), (18, 14.5), (15.5, 9), (15, 11.5), (14.5, 21.5),
             (9.5, 21.5), (9, 11.5), (8.5, 9), (6, 14.5), (3.5, 14), (7, 5), (10.5, 4)]
    leg = [(8, 14), (6.5, 21.5), (4, 21.5), (6.2, 14)]
    return [
        shell(poly(tunic, closed=True, r=S.r)),
        detail(seg(10.5, 4, 13.5, 4)),
        detail("M12 4C12.3 5.8 13.5 7 15.2 7.5"),
        line(poly([(7.5, 15.5), (6, 21.5)], r=S.r)), line(poly([(16.5, 15.5), (18, 21.5)], r=S.r)),
    ]


@icon("hanbok", CAT, "Very short jacket tied with a long ribbon bow over a full, high-waisted bell skirt.",
      tags=["korean", "traditional", "jeogori", "chima", "national dress", "dress"], aliases=["korean-dress"])
def _(S):
    pts = [(10, 3), (4, 4.5), (2.5, 7), (2.5, 10), (5, 11), (7.5, 10), (4.5, 21), (19.5, 21), (16.5, 10), (19, 11),
           (21.5, 10), (21.5, 7), (20, 4.5), (14, 3)]
    return [
        shell(poly(pts, closed=True, r=S.r * 1.3)),
        detail(poly([(7.3, 5), (7.5, 10), (16.5, 10), (16.7, 5)], r=S.r)),
        detail(poly([(10, 3), (12.5, 7.5), (14, 3)], r=S.r)),
        line(seg(12.5, 8, 11, 16)), line(seg(13, 8, 15, 15)),
        dot(12.7, 7.8, 1.4),
    ]


@icon("dirndl", CAT, "Laced bodice over a puff-sleeved blouse, with a full skirt and a front apron.",
      tags=["bavarian", "oktoberfest", "alpine", "traditional", "apron", "dress"], aliases=["alpine-dress"])
def _(S):
    pts = [(9, 4), (6, 3.5), (3.5, 5.5), (4, 8.5), (7.5, 8.5), (8.5, 11), (4, 21), (20, 21), (15.5, 11), (16.5, 8.5),
           (20, 8.5), (20.5, 5.5), (18, 3.5), (15, 4)]
    return [
        shell(poly(pts, closed=True, r=S.r * 1.3)),
        detail(_crew(top=4, l=9, r=15, depth=2.2)),
        detail(seg(8.3, 4.5, 7.5, 8.5)), detail(seg(15.7, 4.5, 16.5, 8.5)),
        detail(seg(8.5, 11, 15.5, 11)),
        detail(poly([(9.5, 11), (9, 18.5), (15, 18.5), (14.5, 11)], r=S.r)),
    ]


@icon("kaftan", CAT, "Long loose robe with very wide sleeves and an embroidered band around a V neckline.",
      tags=["caftan", "robe", "tunic", "boho", "beach", "loungewear"], aliases=["caftan"])
def _(S):
    pts = [(9, 3), (2.5, 4.5), (2.5, 11), (7, 11), (7, 21), (17, 21), (17, 11), (21.5, 11), (21.5, 4.5), (15, 3)]
    band = [(9, 3), (12, 10.5), (15, 3), (13.2, 3), (12, 6.5), (10.8, 3)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        Part("dot", poly(band, closed=True, r=S.r * 0.3)),
        detail(seg(7, 7.5, 7, 11)), detail(seg(17, 7.5, 17, 11)),
    ]


@icon("abaya", CAT, "Long loose ankle-length robe with long sleeves, an open front and a plain collarless neck.",
      tags=["robe", "modest", "cloak", "arabic", "gulf", "dress"], aliases=["abaya-robe"])
def _(S):
    pts = [(9.5, 3), (5, 4.5), (3, 15), (6.5, 15), (5.5, 21.5), (18.5, 21.5), (17.5, 15), (21, 15), (19, 4.5), (14.5, 3)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(7, 9.5, 6.6, 15)), detail(seg(17, 9.5, 17.4, 15)),
        detail(_crew(top=3, l=9.5, r=14.5, depth=2.3)),
        detail(seg(12, 5.3, 12, 21.5)),
    ]


@icon("thobe", CAT, "Ankle-length long-sleeved robe with a small stand collar and a short button placket.",
      tags=["thawb", "dishdasha", "kandura", "robe", "arabic", "menswear"], aliases=["thawb", "dishdasha"])
def _(S):
    pts = [(10, 2.5), (14, 2.5), (14, 4.5), (18, 5.5), (20.5, 14), (17, 14), (17.5, 21.5), (6.5, 21.5), (7, 14), (3.5, 14), (6, 5.5), (10, 4.5)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(10, 4.5, 14, 4.5)),
        detail(seg(12, 4.5, 12, 11)),
        detail(seg(7.4, 9.5, 7, 14)), detail(seg(16.6, 9.5, 17, 14)),
    ]
