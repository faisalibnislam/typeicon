"""TypeIcon Core: retail, part 3 (specialist shop fronts and retail concepts).

Most icons here share one shop front: a striped awning over a shop body (walls x 5-19). The emblem on the
shop is drawn with `em(...)`, a solid silhouette inside a box roughly x 8-16, y 10.5-18.5. It is solid in
Line and Rounded and knocked out of the solid wall in Filled.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path  # noqa: F401

CAT = "retail"


def L(S, a, b):
    return a if S.name == "line" else b


def pu(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def pd(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx, cy):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def thick(d, w):
    return path_to_d(ST(d, w, "butt", "miter"))


def bar(x1, y1, x2, y2, w=1.2):
    """Thin solid bar between two points (for strings, stems, handles)."""
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    nx, ny = -dy / n * w / 2, dx / n * w / 2
    return poly([(x1 + nx, y1 + ny), (x2 + nx, y2 + ny), (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)], closed=True)


def em(d):
    """Solid emblem: solid in Line/Rounded, knocked out of a Filled wall."""
    return Part("dot", d)


def shopfront(S):
    """Striped awning over a shop body."""
    return [
        shell(poly([(3, 8), (5, 3), (19, 3), (21, 8)], closed=True, r=S.r)),
        detail(seg(9.67, 3, 9, 8)), detail(seg(14.33, 3, 15, 8)),
        shell(poly([(5, 8), (5, 21), (19, 21), (19, 8)], closed=True, r=S.r)),
        detail(seg(3, 8, 21, 8)),
    ]


def shop(name, desc, tags, emblem, aliases=()):
    """Register a shop-front icon whose emblem is `emblem(S)` (a list of parts)."""
    @icon(name, CAT, desc, tags=tags, aliases=list(aliases))
    def _(S):
        return shopfront(S) + emblem(S)
    return _


# ============================================================================ shop fronts with an emblem

def _paw(S):
    toes = [pu(circle(8.9, 13.4, 1.15)), pu(circle(11, 11.6, 1.15)), pu(circle(13.2, 11.6, 1.15)), pu(circle(15.2, 13.4, 1.15))]
    pad = poly([(9, 17.6), (10.4, 15), (13.6, 15), (15, 17.6), (13.8, 18.6), (10.2, 18.6)], closed=True, r=1.2)
    return [em(pu(*toes, pad))]


shop("pet-store", "Shop front with an awning and a paw print on the sign",
     ["pet shop", "paw", "animals", "dog", "cat", "pet supplies"], _paw)


def _hardware(S):
    hammer = pu(rot(rect(12.6, 10.4, 1.4, 8.2), 45, 12, 14.5), rot(rect(10.4, 10.4, 5.4, 2.6), 45, 12, 14.5))
    wrench = pu(rot(rect(10.7, 11.4, 1.4, 7.4), -45, 12, 14.5), circle(9.3, 11.9, 1.9))
    wrench = pd(wrench, rot(rect(8.8, 9.8, 1.0, 2.0), -45, 9.3, 11.9))
    return [em(pu(hammer, wrench))]


shop("hardware-store", "Shop front with an awning and a hammer and wrench crossed on the sign",
     ["tools shop", "diy", "builders merchant", "hammer", "wrench", "home improvement"], _hardware)


def _cheese(S):
    wedge = poly([(7.8, 18.4), (7.8, 13.6), (16.2, 11), (16.2, 18.4)], closed=True, r=S.r * 0.5)
    holes = [circle(10.4, 16.2, 0.9), circle(13.6, 14.6, 0.9), circle(14, 17.2, 0.7)]
    return [em(pd(wedge, *holes))]


shop("cheese-shop", "Shop front with an awning and a wedge of cheese with holes on the sign",
     ["cheesemonger", "dairy", "deli", "cheese wedge", "fromagerie"], _cheese)


def _lipstick(S):
    bullet = poly([(10.6, 14.2), (10.6, 12.3), (13.4, 10.4), (13.4, 14.2)], closed=True)
    return [em(pu(bullet, rect(10, 15.1, 4, 3.4, L(S, 0, 0.8))))]


shop("beauty-store", "Shop front with an awning and a lipstick on the sign",
     ["cosmetics shop", "makeup", "lipstick", "perfumery", "beauty supplies"], _lipstick)


def _glasses(S):
    ring = lambda x: pd(circle(x, 14.6, 2.7), circle(x, 14.6, 1.3))
    return [em(pu(ring(9.4), ring(14.6)))]


shop("optical-store", "Shop front with an awning and a large pair of glasses on the sign",
     ["optician", "eyewear", "glasses shop", "spectacles", "eye care"], _glasses)


def _gift(S):
    box = pd(rect(8.2, 14, 7.6, 4.6), rect(11.4, 14, 1.2, 4.6))
    lid = pd(rect(7.6, 12.3, 8.8, 2.1), rect(11.4, 12.3, 1.2, 2.1))
    bow = pu(circle(10.5, 11.4, 1.3), circle(13.5, 11.4, 1.3))
    return [em(pu(box, lid, bow))]


shop("gift-shop", "Shop front with an awning and a wrapped gift box with bow on the sign",
     ["present shop", "souvenir", "gifts", "gift box", "novelty"], _gift)


def _spool(S):
    body = pu(rect(8.6, 10.6, 6.8, 1.6), rect(8.6, 16.9, 6.8, 1.6), rect(9.9, 12, 4.2, 5.2))
    return [em(pd(body, rect(9.9, 13.5, 4.2, 0.9), rect(9.9, 15.1, 4.2, 0.9)))]


shop("fabric-store", "Shop front with an awning and a spool of thread on the sign",
     ["textile shop", "sewing", "haberdashery", "thread", "material shop", "cloth"], _spool)


def _hat(S):
    crown = pd(rect(9.4, 10.8, 5.2, 6.4), rect(9.4, 14.6, 5.2, 1))
    return [em(pu(crown, rect(7.6, 16.9, 8.8, 1.6, 0.6)))]


shop("hat-shop", "Shop front with an awning and a top hat on the sign",
     ["milliner", "hats", "headwear", "top hat", "cap shop"], _hat)


def _balloons(S):
    shapes = [ellipse(9, 12.9, 1.7, 2.1), ellipse(15, 12.9, 1.7, 2.1), ellipse(12, 11.7, 1.7, 2.1)]
    strings = [bar(9.1, 14.8, 11.6, 18.7, 0.8), bar(14.9, 14.8, 12.4, 18.7, 0.8), bar(12, 13.7, 12, 18.7, 0.8)]
    return [em(pu(*shapes, *strings))]


shop("party-store", "Shop front with an awning and a bunch of three balloons on the sign",
     ["party supplies", "balloons", "celebration shop", "birthday", "decorations"], _balloons)


def _pram(S):
    bowl = "M7.6 13.4H15.4A3.9 3.9 0 0 1 11.5 17.3A3.9 3.9 0 0 1 7.6 13.4Z"
    hood = "M7.6 13.4A3.9 3.9 0 0 1 11.5 9.6V13.4Z"
    handle = bar(15.4, 12.6, 16.6, 10.6, 1.2)
    return [em(pu(bowl, hood, handle, circle(9.6, 18, 1.0), circle(14, 18, 1.0)))]


shop("baby-store", "Shop front with an awning and a baby stroller on the sign",
     ["nursery shop", "stroller", "pram", "baby goods", "infant", "buggy"], _pram)


def _washer(S):
    body = pd(rect(8, 10.5, 8, 8, L(S, 0, 1.2)), circle(12, 15.2, 2.5))
    return [em(pu(body, circle(12, 15.2, 1.0)))]


shop("appliance-store", "Shop front with an awning and a front loading washing machine on the sign",
     ["white goods", "washing machine", "electrical shop", "home appliances", "laundry"], _washer)


def _teapot(S):
    body = circle(11.6, 15.2, 3.2)
    lid = rect(10.2, 10.9, 2.8, 1.4, 0.6)
    spout = bar(14, 14.6, 16.4, 12.4, 1.5)
    handle = pd(circle(8.6, 15, 2.1), circle(8.6, 15, 0.9))
    return [em(pu(body, lid, spout, handle))]


shop("tea-shop", "Shop front with an awning and a teapot on the sign",
     ["tea room", "teapot", "tea merchant", "loose leaf", "brew"], _teapot)


def _apple(S):
    body = pu(circle(10.5, 15.2, 3), circle(13.5, 15.2, 3), circle(12, 16, 3.2))
    notch = poly([(12, 12.4), (11, 11.6), (13, 11.6)], closed=True)
    leaf = "M12.4 12.4C12.4 10.6 13.6 10 15.6 10C15.6 11.8 14.4 12.6 12.4 12.4Z"
    return [em(pu(pd(body, notch), leaf))]


shop("health-food-store", "Shop front with an awning and an apple with a leaf on the sign",
     ["organic shop", "natural foods", "wholefoods", "apple", "healthy eating", "grocer"], _apple)


def _pot(S):
    body = rect(8.4, 14, 7.2, 4.6, 1.2)
    lid = rect(7.8, 12.4, 8.4, 1.4, 0.6)
    knob = rect(11, 10.6, 2, 1.6, 0.6)
    handles = pu(rect(6.8, 14.8, 1.8, 1.2), rect(15.4, 14.8, 1.8, 1.2))
    return [em(pu(body, lid, knob, handles))]


shop("kitchenware-store", "Shop front with an awning and a cooking pot with a lid on the sign",
     ["cookware shop", "pots and pans", "kitchen supplies", "cooking", "homeware"], _pot)


def _pendant(S):
    cord = bar(12, 9, 12, 12.6, 1.0)
    shade = "M8.2 16.2A3.8 3.8 0 0 1 15.8 16.2Z"
    return [em(pu(cord, shade, circle(12, 17.7, 1.1)))]


shop("lighting-store", "Shop front with an awning and a hanging pendant lamp on the sign",
     ["lamp shop", "lights", "lighting showroom", "pendant lamp", "fixtures", "chandelier"], _pendant)


def _tent(S):
    return [em(pd(poly([(12, 10.4), (16.8, 18.6), (7.2, 18.6)], closed=True), poly([(12, 14.2), (13.7, 18.7), (10.3, 18.7)], closed=True)))]


shop("outdoor-gear-store", "Shop front with an awning and a small tent on the sign",
     ["camping shop", "tent", "hiking gear", "outdoors", "camping supplies", "adventure"], _tent)


def _mortar(S):
    bowl = "M7.8 14.4H16.2A4.2 4.2 0 0 1 7.8 14.4Z"
    pestle = rot(rect(11.3, 9.6, 2, 6.4, 0.8), 40, 12, 14)
    base = rect(10, 18.2, 4, 0.8)
    return [em(pu(bowl, pestle))]


shop("spice-shop", "Shop front with an awning and a mortar and pestle on the sign",
     ["herbs and spices", "mortar and pestle", "seasoning", "grocer", "condiments", "grind"], _mortar)


def _plane(S):
    pts = [(12, 10.4), (13, 12), (13, 13.4), (16.4, 15.4), (16.4, 16.5), (13, 15.5), (13, 17.3), (14.3, 18.1), (14.3, 18.8),
           (12, 18.2), (9.7, 18.8), (9.7, 18.1), (11, 17.3), (11, 15.5), (7.6, 16.5), (7.6, 15.4), (11, 13.4), (11, 12)]
    return [em(poly(pts, closed=True))]


shop("hobby-shop", "Shop front with an awning and a small model airplane on the sign",
     ["model shop", "hobbies", "model kits", "aeroplane", "toys and models", "rc"], _plane)


def _burst(S):
    pts = []
    for i in range(16):
        r = 4.5 if i % 2 == 0 else 2.9
        pts.append((12 + r * math.cos(math.radians(-90 + i * 22.5)), 14.6 + r * math.sin(math.radians(-90 + i * 22.5))))
    return [em(pd(poly(pts, closed=True), rect(11.1, 12.1, 1.8, 3.2), circle(12, 16.9, 0.9)))]


shop("comic-book-store", "Shop front with an awning and a jagged speech bubble on the sign",
     ["comics", "graphic novels", "manga", "pow", "collectibles", "comic shop"], _burst)


def _percent(S):
    return [em(pu(circle(9.4, 12.4, 1.7), circle(14.6, 16.8, 1.7), bar(15.4, 10.8, 8.6, 18.4, 1.6)))]


shop("discount-store", "Shop front with an awning and a large percent sign on the sign",
     ["bargain shop", "cheap", "percent off", "sale shop", "dollar store", "clearance"], _percent)


def _frame(S):
    return [em(pd(rect(8, 10.4, 8, 8.4, L(S, 0, 0.8)), rect(9.8, 12.2, 4.4, 4.8)))]


shop("frame-shop", "Shop front with an awning and an empty picture frame on the sign",
     ["picture framing", "framer", "frames", "art shop", "photo frame", "gallery"], _frame)


def _tackle(S):
    float_ = ellipse(13, 11.9, 1.4, 1.9)
    return [em(float_), detail("M13 13.8V16.8A2.1 2.1 0 0 1 8.8 16.8V15.2")]


shop("fishing-tackle-shop", "Shop front with an awning and a fishing hook with a small float on the sign",
     ["angling", "bait shop", "fishing gear", "hook", "fisherman", "rods"], _tackle)


def _umbrella(S):
    dome = "M7.4 15A4.6 4.6 0 0 1 16.6 15Z"
    return [em(pu(dome, bar(12, 14.5, 12, 18.4, 1.1))), detail("M12 17.2V18A1.2 1.2 0 0 1 9.6 18")]


shop("umbrella-shop", "Shop front with an awning and an open umbrella on the sign",
     ["brolly", "rain gear", "parasol", "umbrellas", "accessories", "weather"], _umbrella)


def _case(S):
    body = pd(rect(8.4, 12.2, 7.2, 5.8, 1), rect(10.5, 13.2, 0.9, 3.8), rect(12.6, 13.2, 0.9, 3.8))
    handle = pu(rect(10.1, 10.4, 1.1, 2), rect(12.8, 10.4, 1.1, 2), rect(10.1, 10.4, 3.8, 1.1))
    return [em(pu(body, handle, circle(9.8, 18.5, 0.9), circle(14.2, 18.5, 0.9)))]


shop("luggage-store", "Shop front with an awning and a wheeled suitcase on the sign",
     ["suitcases", "travel goods", "bags", "baggage", "trolley case", "holiday"], _case)


def _watch(S):
    face = pd(circle(12, 14.6, 3.2), rect(11.4, 12.3, 1.2, 3), rect(11.4, 14.1, 2.6, 1.2))
    return [em(pu(face, rect(10.4, 9.8, 3.2, 2, 0.4), rect(10.4, 17.4, 3.2, 1.8, 0.4)))]


shop("watch-shop", "Shop front with an awning and a wristwatch on the sign",
     ["watches", "clock shop", "timepiece", "horologist", "wristwatch", "jeweller"], _watch)


def _mattress(S):
    slab = pd(rect(7, 13.4, 10, 4.2, 1.2), rect(11.5, 14.2, 0.9, 2.6))
    pillow = rect(8.2, 11, 4.6, 1.8, 0.8)
    return [em(pu(slab, pillow, rect(7.9, 17.6, 1.2, 1.2), rect(14.9, 17.6, 1.2, 1.2)))]


shop("mattress-store", "Shop front with an awning and a thick mattress with quilted lines on the sign",
     ["bed shop", "mattresses", "sleep store", "bedding", "beds", "furniture"], _mattress)


def _carpet(S):
    roll = pd(circle(10.4, 15.5, 3.1), circle(10.4, 15.5, 1.1))
    sheet = pd(rect(10.4, 16.4, 6.6, 2.2), rect(10.4, 17.2, 6.6, 0.7))
    return [em(pu(roll, sheet))]


shop("carpet-store", "Shop front with an awning and a partly rolled carpet on the sign",
     ["rug shop", "flooring", "carpets", "rugs", "floor coverings", "rolled rug"], _carpet)


def _mask(S):
    shape = "M7.4 12.8Q12 10.6 16.6 12.8L16.6 15.2Q15.2 18.2 13.2 16.2Q12 15.4 10.8 16.2Q8.8 18.2 7.4 15.2Z"
    return [em(pd(shape, ellipse(9.8, 14.1, 1.15, 0.85), ellipse(14.2, 14.1, 1.15, 0.85)))]


shop("costume-shop", "Shop front with an awning and a masquerade mask on the sign",
     ["fancy dress", "masquerade", "halloween", "dress up", "mask", "theatrical"], _mask)


# ============================================================================ distinct building types

def win(x, y, w=2.0, h=2.0):
    return Part("dot", rect(x, y, w, h))


@icon("department-store", CAT, "Wide multi-storey store with a raised sign block, rows of windows and a large entrance",
      tags=["department store", "retail", "shopping", "big store", "mall", "storey building", "shop"])
def _(S):
    return [
        shell(poly([(2, 21), (2, 9), (8, 9), (8, 3), (16, 3), (16, 9), (22, 9), (22, 21)], closed=True, r=S.r)),
        win(10.5, 5.5, 3, 1.5),
        win(5, 11.5), win(9, 11.5), win(13, 11.5), win(17, 11.5),
        win(5, 15.5), win(17, 15.5),
        detail(poly([(10, 21), (10, 16), (14, 16), (14, 21)], r=S.r * 0.5)),
    ]


def _24(S):
    two = thick("M8.2 11.4H10.8V14.3H8.2V17.2H10.8", 1.3)
    four = thick("M13.2 11.2V14.3H16V11.2M16 14.3V17.4", 1.3)
    return [em(pu(two, four))]


shop("convenience-store", "Small shop front with an awning and a 24 hour sign",
     ["corner shop", "24 hour", "mini mart", "open late", "bodega", "all day shop", "c-store"], _24)


def dress_path(cx, top, bottom, hem):
    """Dress silhouette: two straps, a bodice with a V neck, a waist and a flared skirt."""
    w = cx
    return (f"M{fmt(w-1.9)} {fmt(top)}H{fmt(w-0.9)}L{fmt(w)} {fmt(top+1.6)}L{fmt(w+0.9)} {fmt(top)}H{fmt(w+1.9)}"
            f"L{fmt(w+1.5)} {fmt(top+3.4)}L{fmt(w+hem)} {fmt(bottom)}H{fmt(w-hem)}L{fmt(w-1.5)} {fmt(top+3.4)}Z")


@icon("boutique", CAT, "Narrow shop front with a cornice board and an arched window showing a dress",
      tags=["fashion shop", "clothes store", "dress shop", "designer", "small shop", "ladies wear"])
def _(S):
    return [
        shell(poly([(3, 3), (21, 3), (21, 7), (3, 7)], closed=True, r=S.r * 0.5)),
        shell(poly([(5, 7), (5, 21), (19, 21), (19, 7)], closed=True, r=S.r)),
        detail(seg(3, 7, 21, 7)),
        detail("M7.5 21V14A4.5 4.5 0 0 1 16.5 14V21"),
        Part("dot", dress_path(12, 11.4, 19.6, 3.0)),
    ]


@icon("bridal-shop", CAT, "Shop front with an awning and a wedding gown with a small heart on the sign",
      tags=["wedding dress", "bride", "wedding shop", "gown", "bridal wear", "marriage"])
def _(S):
    heart = "M12 18L10.4 16.4A1 1 0 0 1 12 15.2A1 1 0 0 1 13.6 16.4Z"
    return shopfront(S) + [em(pd(dress_path(12, 10.2, 18.8, 4.2), heart))]


@icon("garden-center", CAT, "Greenhouse with a pitched glass roof, pane bars and a sprouting plant inside",
      tags=["garden centre", "nursery", "plants", "greenhouse", "gardening shop", "horticulture"])
def _(S):
    leaf = "M12 17C12 14.6 10.6 13.6 9.4 13.6C9.4 15.6 10.4 17 12 17ZM12 16C12 13.8 13.4 12.8 14.8 12.8C14.8 14.8 13.6 16 12 16Z"
    return [
        shell(poly([(3, 21), (3, 10), (12, 3.5), (21, 10), (21, 21)], closed=True, r=S.r)),
        detail(seg(7.5, 8.5, 7.5, 21)), detail(seg(16.5, 8.5, 16.5, 21)),
        Part("dot", leaf), Part("dot", rect(11.4, 16.6, 1.2, 4.4)),
    ]


@icon("surf-shop", CAT, "Small beach shack with a pitched roof and door and a surfboard standing beside it",
      tags=["surfboard", "beach shop", "surf school", "surfing", "beach hut", "water sports"])
def _(S):
    board = "M18.8 3C21.8 8 22 15 21.2 19.2C20.8 21.2 16.8 21.2 16.4 19.2C15.6 15 15.8 8 18.8 3Z"
    return [
        shell(poly([(3, 21), (3, 10.5), (8, 5.5), (13, 10.5), (13, 21)], closed=True, r=S.r)),
        detail(poly([(6.5, 21), (6.5, 15), (9.5, 15), (9.5, 21)], r=S.r * 0.5)),
        shell(board),
        detail(seg(18.8, 7, 18.8, 15.5)),
    ]


@icon("general-store", CAT, "Old village shop with a pitched false front, a porch roof line, a door and two barrels",
      tags=["village shop", "country store", "old shop", "trading post", "porch", "wooden shop"])
def _(S):
    return [
        shell(poly([(7, 21), (7, 8.5), (12, 3.5), (17, 8.5), (17, 21)], closed=True, r=S.r)),
        detail(seg(3, 12.5, 21, 12.5)),
        detail(poly([(10, 21), (10, 16.5), (14, 16.5), (14, 21)], r=S.r * 0.5)),
        Part("dot", pd(rect(2.2, 15.4, 3.6, 5.6, 1), rect(2.2, 17.6, 3.6, 0.7))),
        Part("dot", pd(rect(18.2, 15.4, 3.6, 5.6, 1), rect(18.2, 17.6, 3.6, 0.7))),
    ]


@icon("pop-up-shop", CAT, "Folding tent canopy over a small table of goods",
      tags=["market stall", "temporary shop", "gazebo", "tent stall", "trade show", "street vendor", "pop up"])
def _(S):
    return [
        shell(poly([(2, 10.5), (12, 5), (22, 10.5)], closed=True, r=S.r)),
        line(seg(4.5, 10, 4.5, 21)), line(seg(19.5, 10, 19.5, 21)),
        line(seg(7, 17, 17, 17)), line(seg(8.5, 17, 8.5, 21)), line(seg(15.5, 17, 15.5, 21)),
        Part("dot", rect(8.8, 13.6, 3, 3.4)), Part("dot", rect(13, 12.6, 2.4, 4.4)),
    ]


@icon("mall-kiosk", CAT, "Island kiosk with a canopy, a central display column and a rounded counter",
      tags=["shopping mall kiosk", "retail island", "booth", "cart", "stall", "island stand"])
def _(S):
    return [
        shell(poly([(3, 8), (5, 3), (19, 3), (21, 8)], closed=True, r=S.r)),
        detail(seg(9.67, 3, 9, 8)), detail(seg(14.33, 3, 15, 8)),
        line(seg(12, 8, 12, 14)),
        shell(rect(3, 14, 18, 7, 3.5)),
    ]


def _star(cx, cy, r, ri):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else ri
        a = math.radians(-90 + i * 36)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return poly(pts, closed=True)


@icon("christmas-market", CAT, "Wooden chalet stall with a pointed roof, a star and string lights along the eaves",
      tags=["xmas market", "winter market", "holiday stall", "chalet", "festive", "advent", "seasonal market"])
def _(S):
    return [
        shell(poly([(3, 13), (12, 6.5), (21, 13)], closed=True, r=S.r)),
        Part("dot", _star(12, 10.6, 2.3, 1.0)),
        line(seg(5, 12.5, 5, 21)), line(seg(19, 12.5, 19, 21)),
        shell(rect(5, 17, 14, 4, min(S.R, 1.5))),
        dot(7.5, 15, 0.9), dot(10.5, 15, 0.9), dot(13.5, 15, 0.9), dot(16.5, 15, 0.9),
    ]


@icon("auction-house", CAT, "Classical building with a sign band holding a gavel above four columns on a base",
      tags=["auctioneer", "gavel", "bidding", "sale room", "classical building", "lots"])
def _(S):
    gavel = pu(rot(rect(9.6, 4.8, 5, 2.4, 0.5), -35, 12, 6.5), rot(rect(11.5, 6.8, 1.2, 2.4), -35, 12, 6.5))
    return [
        shell(poly([(3, 3), (21, 3), (21, 10), (3, 10)], closed=True, r=S.r * 0.5)),
        Part("dot", gavel),
        line(seg(6, 12.5, 6, 18)), line(seg(10, 12.5, 10, 18)), line(seg(14, 12.5, 14, 18)), line(seg(18, 12.5, 18, 18)),
        shell(poly([(3, 19.5), (21, 19.5), (21, 21.5), (3, 21.5)], closed=True, r=S.r * 0.4)),
    ]


# ============================================================================ concepts, services and fixtures

def E(*ds):
    return em(pu(*ds))


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


@icon("waitlist", CAT, "Clipboard with three rows, each a small person head and a line",
      tags=["wait list", "queue", "notify me", "back in stock", "sign up list", "reservation list"])
def _(S):
    rows = []
    for y in (10.2, 14, 17.8):
        rows += [circle(8.6, y, 1.2), bar(11.6, y, 16.4, y, 1.5)]
    return [shell(rect(5, 4.5, 14, 16.5, rr(S, 2.5))), solid(rect(9, 2.5, 6, 3.4, 0.8)), E(*rows)]


@icon("product-configurator", CAT, "Product box beside three slider lines with knobs in different positions",
      tags=["customize", "options", "build your own", "customiser", "personalise", "settings", "variants"])
def _(S):
    parts = [shell(rect(2.5, 8, 8, 9, rr(S, 2))), detail(seg(2.5, 11.5, 10.5, 11.5))]
    for y, kx in ((6, 18), (12, 16), (18, 19.5)):
        parts += [line(seg(13, y, 22, y)), dot(kx, y, 2.0)]
    return parts


@icon("cross-sell", CAT, "Central box with two arrows pointing outward to two smaller boxes either side",
      tags=["upsell", "related products", "add-ons", "recommended items", "bundle", "also bought"])
def _(S):
    return [
        shell(rect(8, 2.5, 8, 7.5, rr(S, 2))), detail(seg(8, 5.5, 16, 5.5)),
        line(poly([(10, 12.5), (6.5, 15)])), line(poly([(14, 12.5), (17.5, 15)])),
        line(poly([(4.8, 12.4), (6.8, 15.2), (3.6, 15.4)])), line(poly([(19.2, 12.4), (17.2, 15.2), (20.4, 15.4)])),
        shell(rect(1.5, 17, 6, 4.5, rr(S, 1.5))), shell(rect(16.5, 17, 6, 4.5, rr(S, 1.5))),
    ]


@icon("omnichannel", CAT, "Shop front, laptop and smartphone arranged in a triangle joined by lines",
      tags=["multichannel", "all channels", "online and in store", "unified commerce", "cross-channel", "connected retail"])
def _(S):
    return [
        shell(poly([(8, 6.5), (9, 2.5), (15, 2.5), (16, 6.5)], closed=True, r=S.r * 0.5)),
        shell(poly([(9, 6.5), (9, 10), (15, 10), (15, 6.5)])),
        shell(rect(1.5, 15, 8, 5, rr(S, 1.5))), line(seg(1.5, 22, 9.5, 22)),
        shell(rect(17, 13.5, 5, 8.5, rr(S, 1.5))),
        line(poly([(10.5, 11.5), (6, 13.5)])), line(poly([(13.5, 11.5), (19, 12)])),
        line(seg(11.5, 18, 15, 18)),
    ]


@icon("price-range-filter", CAT, "Slider track with two tall handles and the section between them filled",
      tags=["price slider", "min max price", "budget filter", "range selector", "filter by price", "price limits"])
def _(S):
    return [
        solid(rect(9, 10.5, 6, 3)),
        shell(rect(5, 6, 5, 12, 2.5)), shell(rect(14, 6, 5, 12, 2.5)),
        line(seg(1.5, 12, 5, 12)), line(seg(19, 12, 22.5, 12)),
    ]


@icon("voice-shopping", CAT, "Cylinder smart speaker with sound waves above and a small shopping cart beside it",
      tags=["smart speaker", "voice order", "assistant", "voice commerce", "talk to buy", "hands free shopping"])
def _(S):
    return [
        shell(rect(2.5, 11, 8, 10, rr(S, 3))),
        detail(seg(2.5, 14.5, 10.5, 14.5)),
        line(arc(6.5, 10, 3.5, -130, -50)), line(arc(6.5, 10, 7, -125, -55)),
        line(poly([(12.5, 10), (14.5, 10), (16, 17.5), (21, 17.5)], r=S.r)),
        shell(poly([(15, 12), (22, 12), (21, 16.5), (16, 16.5)], closed=True, r=S.r * 0.5)),
        dot(16.8, 20.5, 1.2), dot(20.2, 20.5, 1.2),
    ]


@icon("tv-shopping", CAT, "Television showing a product box with a telephone handset beside the set",
      tags=["teleshopping", "home shopping channel", "call to order", "tv sales", "infomercial", "television"])
def _(S):
    handset = pu(thick("M18.5 6.6A7 7 0 0 1 18.5 17.4", 1.8), rect(17.6, 5, 3.4, 3.2, 1), rect(17.6, 15.8, 3.4, 3.2, 1))
    return [
        shell(rect(1.5, 4, 14, 11.5, rr(S, 2.5))),
        E(rect(5.5, 7, 5.5, 5)),
        line(seg(5, 19.5, 12, 19.5)), line(seg(8.5, 15.5, 8.5, 19.5)),
        em(rot(handset, 0, 12, 12)),
    ]


@icon("ship-from-store", CAT, "Small shop front with an awning and a delivery truck driving away from its door",
      tags=["store fulfilment", "local delivery", "dispatch from shop", "same day delivery", "click and deliver", "order shipped"])
def _(S):
    return [
        shell(poly([(1.5, 8.5), (2.5, 3), (9.5, 3), (10.5, 8.5)], closed=True, r=S.r * 0.5)),
        shell(poly([(2.5, 8.5), (2.5, 16), (9.5, 16), (9.5, 8.5)])),
        detail(seg(6, 16, 6, 11.5)),
        shell(rect(11.5, 12.5, 6, 6.5, rr(S, 1.2))),
        shell(poly([(17.5, 14.5), (20.3, 14.5), (22.5, 17), (22.5, 19), (17.5, 19)], closed=True, r=S.r * 0.6)),
        dot(14.5, 20.8, 1.3), dot(20, 20.8, 1.3),
        line(seg(1.5, 19.5, 5, 19.5)), line(seg(1.5, 22, 7.5, 22)),
    ]


@icon("order-pickup-shelf", CAT, "Shelf unit holding bagged orders, each bag with a small name tag",
      tags=["click and collect", "collection point", "pickup rack", "order ready", "bagged orders", "in store pickup"])
def _(S):
    def bag(x, y):
        return pd(rect(x, y, 4.6, 5.4, 0.6), rect(x + 1.4, y + 1.2, 1.8, 1.4))
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 2.5))),
        detail(seg(2.5, 12.5, 21.5, 12.5)),
        E(bag(5.5, 6), bag(13.8, 6), bag(5.5, 16), bag(13.8, 16)),
    ]


@icon("big-box-store", CAT, "Wide low windowless warehouse store with a sign band and a shopping cart by the entrance",
      tags=["superstore", "warehouse store", "hypermarket", "retail park", "megastore", "supercentre", "wholesale club"])
def _(S):
    return [
        shell(poly([(1.5, 21), (1.5, 6), (22.5, 6), (22.5, 21)], closed=True, r=S.r)),
        detail(seg(1.5, 11, 22.5, 11)),
        E(rect(5, 7.8, 9, 1.6)),
        detail(poly([(4.5, 21), (4.5, 15.5), (9.5, 15.5), (9.5, 21)])),
        E(poly([(13, 14), (14.6, 14), (15.4, 17.4), (20, 17.4), (20.6, 14.8), (14.2, 14.8)], closed=True)),
        dot(15.8, 19.6, 0.9), dot(19.4, 19.6, 0.9),
    ]


@icon("strip-mall", CAT, "Row of four connected single storey shop fronts under one flat roof with parking lines in front",
      tags=["shopping strip", "plaza", "retail row", "parade of shops", "small shopping centre", "neighborhood shops"])
def _(S):
    parts = [shell(poly([(1.5, 5), (22.5, 5), (22.5, 17), (1.5, 17)], closed=True, r=S.r)),
             detail(seg(1.5, 9, 22.5, 9))]
    for x in (7, 12, 17):
        parts.append(detail(seg(x, 9, x, 17)))
    for x in (2.6, 8, 13.4, 18.8):
        parts.append(E(rect(x, 11.2, 2.6, 3.2)))
    for x in (3, 8, 13, 18, 21.5):
        parts.append(line(seg(x, 19.5, x, 22)))
    return parts


def _craft(S):
    brush = pu(bar(8.4, 18.6, 10.2, 13.4, 1.6), bar(10.4, 13.8, 11, 11.8, 2.8), poly([(9.6, 11.8), (12.4, 11.8), (11, 9.2)], closed=True))
    scissors = pu(pd(circle(14.4, 18.2, 1.5), circle(14.4, 18.2, 0.6)), pd(circle(17.8, 18.2, 1.5), circle(17.8, 18.2, 0.6)),
                  bar(14.6, 16.8, 17.4, 9.8, 1.2), bar(17.6, 16.8, 14.8, 9.8, 1.2))
    return [em(pu(brush, scissors))]


shop("craft-store", "Shop front with an awning and a paintbrush beside open scissors on the sign",
     ["arts and crafts", "hobby supplies", "paintbrush", "scissors", "diy crafts", "creative shop", "scrapbooking"], _craft)


@icon("bazaar", CAT, "Arcade wall with two pointed archways, each with a hanging lantern",
      tags=["souk", "oriental market", "arcade market", "covered market", "lanterns", "stalls", "marketplace", "arches"])
def _(S):
    parts = [shell(rect(1.5, 3, 21, 18, rr(S, 2)))]
    for x in (4.5, 13.5):
        c = x + 3
        parts.append(detail(poly([(x, 21), (x, 13), (c, 7), (x + 6, 13), (x + 6, 21)], r=S.r)))
        parts.append(E(bar(c, 10.2, c, 13.4, 0.9), circle(c, 15.2, 1.4)))
    return parts


@icon("showroom", CAT, "Sofa and floor lamp standing on a display platform",
      tags=["display room", "furniture showroom", "exhibition", "sofa", "lamp", "furniture store", "display floor"])
def _(S):
    return [
        shell(poly([(1.5, 17.5), (1.5, 10.5), (4.5, 10.5), (4.5, 6.5), (13.5, 6.5), (13.5, 10.5), (16.5, 10.5), (16.5, 17.5)], closed=True, r=S.r)),
        detail(seg(4.5, 11, 4.5, 17.5)), detail(seg(13.5, 11, 13.5, 17.5)),
        shell(poly([(18, 4), (22.5, 4), (21.5, 8.5), (19, 8.5)], closed=True, r=S.r * 0.4)),
        line(seg(20.25, 8.5, 20.25, 17.5)),
        shell(poly([(1.5, 19.5), (22.5, 19.5), (22.5, 21.5), (1.5, 21.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("flea-market", CAT, "Two small canopy tents over folding tables with goods on them",
      tags=["swap meet", "car boot sale", "second hand market", "street market", "market stalls", "bric a brac", "tables"])
def _(S):
    parts = []
    for x in (1.5, 12.5):
        parts += [
            shell(poly([(x, 9.5), (x + 1.2, 3.5), (x + 8.8, 3.5), (x + 10, 9.5)], closed=True, r=S.r * 0.6)),
            line(seg(x + 1.5, 9.5, x + 1.5, 21.5)), line(seg(x + 8.5, 9.5, x + 8.5, 21.5)),
            line(seg(x + 1.5, 17, x + 8.5, 17)),
            E(rect(x + 3.2, 13, 1.8, 2.8), circle(x + 6.4, 14.7, 1.2)),
        ]
    return parts


@icon("food-court", CAT, "Row of three counter bays under an awning with a table and two chairs in front",
      tags=["eating area", "canteen", "mall dining", "street food hall", "fast food court", "table and chairs", "cafeteria"])
def _(S):
    parts = [shell(poly([(1.5, 2.5), (22.5, 2.5), (22.5, 12.5), (1.5, 12.5)], closed=True, r=S.r * 0.6)),
             detail(seg(1.5, 6.5, 22.5, 6.5)), detail(seg(8.5, 2.5, 8.5, 12.5)), detail(seg(15.5, 2.5, 15.5, 12.5))]
    for x in (3.4, 10.4, 17.4):
        parts.append(E(rect(x, 8.8, 3.2, 2.2)))
    parts += [line(seg(8.5, 16.5, 15.5, 16.5)), line(seg(12, 16.5, 12, 21.5)),
              line(poly([(3.5, 14.5), (3.5, 21.5)])), line(seg(3.5, 18.5, 6.5, 18.5)),
              line(poly([(20.5, 14.5), (20.5, 21.5)])), line(seg(20.5, 18.5, 17.5, 18.5))]
    return parts


@icon("assistance-call-button", CAT, "Wall box on a shelf edge with a large round button and a bell above it",
      tags=["call for help", "service bell", "customer service", "staff call", "help button", "ring for service", "call button"])
def _(S):
    bell = "M9 9.2Q9 4 12 4Q15 4 15 9.2L16.2 10.4H7.8Z"
    return [
        E(bell, circle(12, 11.6, 0.001)),
        shell(rect(4.5, 12.5, 15, 7.5, rr(S, 2))),
        dot(12, 16.25, 2.4),
        line(seg(1.5, 21, 22.5, 21)),
    ]


@icon("gift-set", CAT, "Open box holding two small bottles and a jar",
      tags=["gift box", "hamper", "present set", "bath set", "beauty set", "boxed set", "collection box"])
def _(S):
    bottle = lambda x: pu(rect(x + 1.2, 4.2, 1.8, 2.4, 0.3), rect(x, 6.4, 4.2, 6.4, 1))
    jar = pu(rect(15.4, 6.6, 4.8, 1.8, 0.4), rect(15.4, 8.6, 4.8, 4.2, 1))
    return [
        shell(rect(2.5, 12.5, 19, 8.5, rr(S, 4))),
        detail(seg(8.9, 12.5, 8.9, 21)), detail(seg(15, 12.5, 15, 21)),
        E(bottle(3.6), bottle(9.9), jar),
    ]


@icon("coin-counting-tray", CAT, "Triangular tray holding rows of coins lying side by side",
      tags=["coin sorter", "change counter", "cash drawer", "coin tray", "money counting", "coins in rows", "cashier"])
def _(S):
    cs = [(12, 9.4), (9.8, 13.4), (14.2, 13.4), (7.6, 17.4), (12, 17.4), (16.4, 17.4)]
    return [shell(poly([(12, 2.5), (22, 20.5), (2, 20.5)], closed=True, r=S.r)), E(*[circle(x, y, 1.5) for x, y in cs])]


@icon("store-brand", CAT, "Plain box with a label band and a small awning mark on the label",
      tags=["own brand", "private label", "house brand", "generic product", "retailer label", "white label", "packaging"])
def _(S):
    mark = pu(poly([(8.8, 13.4), (9.6, 11.2), (14.4, 11.2), (15.2, 13.4)], closed=True), rect(9.6, 14, 4.8, 2.4))
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))), detail(seg(3, 7, 21, 7)),
        shell(rect(6, 9.5, 12, 8.5, rr(S, 1.5))),
        E(mark),
    ]


@icon("made-to-measure", CAT, "Shirt with a tape measure wrapped around the chest",
      tags=["tailoring", "bespoke", "custom fit", "tailor", "measuring tape", "personalised clothing", "custom clothing"])
def _(S):
    ticks = [rect(8.2 + 1.6 * i, 12.2, 0.7, 1.1 if i % 2 else 1.7) for i in range(5)]
    band = pd(rect(7, 11.5, 10, 3), *ticks)
    return [
        shell(poly([(8, 3), (3, 6), (5, 10), (7, 9), (7, 21), (17, 21), (17, 9), (19, 10), (21, 6), (16, 3)], closed=True, r=S.r)),
        detail("M8 3a4 4 0 0 0 8 0"),
        E(band, rect(14.6, 14, 1.6, 4.6)),
    ]


@icon("engraving-service", CAT, "Ring lying flat with a fine engraving tool touching it and a spark at the point",
      tags=["personalisation", "custom engraving", "jewelry engraving", "inscription", "etching", "ring", "personalise gift"])
def _(S):
    return [
        shell(circle(9.5, 14.5, 6.5)), shell(circle(9.5, 14.5, 3.6)),
        shell(poly([(9.5, 2), (11.4, 4.3), (9.5, 6.6), (7.6, 4.3)], closed=True, r=S.r * 0.4)),
        line(poly([(21.8, 3.5), (16.6, 9)])),
        E(poly([(16.6, 9), (15.2, 10.6), (17.4, 11)], closed=True)),
        E(poly([(19.8, 13.5), (20.6, 15), (22, 15.8), (20.6, 16.6), (19.8, 18.2), (19, 16.6), (17.6, 15.8), (19, 15)], closed=True)),
    ]


@icon("parking-validation", CAT, "Parking ticket with a check mark being stamped by a round stamp",
      tags=["validate parking", "stamp", "ticket validation", "free parking", "car park", "validated ticket", "garage ticket"])
def _(S):
    return [
        E(rect(14, 2, 4, 5, 1.2), rect(12, 7.2, 8, 2, 0.8)),
        shell(rect(2.5, 12, 19, 9, rr(S, 3))),
        detail(seg(8, 12, 8, 21)),
        line(poly([(12.5, 16.8), (14.6, 18.6), (18.2, 14.8)])),
    ]


@icon("order-form", CAT, "Paper form with a small box drawing at the top and three rows of checkbox, line and quantity box",
      tags=["purchase order", "paper order", "request form", "catalogue order", "quantity", "checkbox form", "order sheet"])
def _(S):
    rows = []
    for y in (12.6, 15.8, 19):
        rows += [rect(7, y - 1, 2, 2), bar(10.5, y, 14, y, 1.2), rect(15.2, y - 1.2, 2.6, 2.4)]
    return [shell(rect(4, 2.5, 16, 19.5, rr(S, 2.5))), E(pd(rect(7.5, 5, 5, 4.4), rect(7.5, 7, 5, 0.01)), *rows)]


@icon("coupon-organizer", CAT, "Expanding accordion file with coupon tickets sticking out of its pockets",
      tags=["coupon holder", "voucher wallet", "expanding file", "money saving", "deal folder", "coupon binder", "accordion file"])
def _(S):
    parts = [shell(poly([(2.5, 21), (3.5, 12), (20.5, 12), (21.5, 21)], closed=True, r=S.r)),
             detail(seg(9, 12.5, 8.6, 21)), detail(seg(15, 12.5, 15.4, 21))]
    for x in (4.6, 10.4, 16.2):
        parts.append(E(rot(pd(rect(x - 0.4, 3.5, 4.2, 9, 0.5), circle(x + 1.7, 6.2, 1.0)), (-8, 0, 8)[(4.6, 10.4, 16.2).index(x)], x + 1.7, 12)))
    return parts


@icon("security-label-sticker", CAT, "Square sticker printed with a flat coil pattern above a barcode strip",
      tags=["anti theft tag", "eas label", "rfid sticker", "security tag", "shoplifting prevention", "antenna label", "barcode label"])
def _(S):
    coil = thick("M6.8 11.2V6.8H17.2V11.2H9.4V9H14.8", 1.2)
    bars = [rect(x, 15, w, 3.4) for x, w in ((6.8, 1), (8.6, 2), (11.6, 1), (13.4, 1), (15.2, 2))]
    return [shell(rect(3, 3, 18, 18, rr(S, 3))), E(coil, *bars)]


@icon("bottle-security-cap", CAT, "Bottle neck with a bulky locking cap clamped over the top and a keyhole on its side",
      tags=["bottle lock", "wine security", "anti theft cap", "spirit bottle lock", "liquor security", "locking cap", "keyhole"])
def _(S):
    keyhole = pu(circle(12, 5.2, 1.2), poly([(11.4, 5.6), (12.6, 5.6), (13, 7.4), (11, 7.4)], closed=True))
    return [
        shell(rect(6.5, 2.5, 11, 7, rr(S, 3))), E(keyhole),
        line(poly([(10, 9.5), (10, 13), (6.5, 16), (6.5, 21), (17.5, 21), (17.5, 16), (14, 13), (14, 9.5)], r=S.r)),
    ]


@icon("cart-coin-mechanism", CAT, "Small coin lock box on a shopping cart handle with a coin slot and a short chain ending in a key",
      tags=["coin lock", "trolley lock", "cart release", "deposit coin", "trolley token", "key chain", "shopping trolley"])
def _(S):
    key = pu(pd(circle(9, 19.4, 1.8), circle(9, 19.4, 0.7)), bar(10.6, 19.4, 15, 19.4, 1.2), rect(13, 19.4, 1, 1.6))
    return [
        shell(rect(6.5, 2.5, 11, 9.5, rr(S, 2.5))),
        E(rect(9.5, 6, 5, 1.4)),
        line(seg(1.5, 13.5, 22.5, 13.5)),
        E(bar(9, 14.6, 9, 17.5, 0.9), key),
    ]


@icon("in-counter-scanner", CAT, "Flat scanner window set into a counter top with an upright glass panel and crossing laser lines",
      tags=["bioptic scanner", "checkout scanner", "barcode reader", "pos scanner", "laser scanner", "supermarket till", "scan"])
def _(S):
    return [
        shell(rect(1.5, 15, 21, 6.5, rr(S, 2.5))),
        E(rect(3.8, 16.6, 8, 1.8)),
        shell(rect(14.5, 3, 6.5, 12, rr(S, 1.5))),
        E(thick("M16.2 5.2L19.4 12.6", 1.1), thick("M19.4 5.2L16.2 12.6", 1.1)),
    ]


@icon("tag-fastener", CAT, "Thin plastic filament with a T bar at one end and a flat paddle at the other, holding a small tag",
      tags=["tag gun fastener", "swift tack", "loop fastener", "price tag attachment", "plastic barb", "tagging", "clothing tag fastener"])
def _(S):
    return [
        E(bar(3, 4.5, 3, 11.5, 2.2), rect(17.6, 4.8, 4.4, 5.4, 1)),
        line(seg(3, 8, 17.6, 8)),
        shell(poly([(7.5, 12.5), (12.5, 12.5), (14, 14.5), (14, 21), (6, 21), (6, 14.5)], closed=True, r=S.r * 0.6)),
        line(seg(10, 8, 10, 10.6)),
        dot(10, 15.2, 1.1),
    ]


@icon("group-buying", CAT, "Three person heads side by side above one shared shopping cart",
      tags=["group deal", "bulk buy together", "shared cart", "collective purchase", "team order", "friends shopping", "co-buying"])
def _(S):
    return [
        circle_head(6, 4.5), circle_head(12, 4.5), circle_head(18, 4.5),
        line(poly([(1.5, 9), (4, 9), (6.6, 17.5), (19, 17.5)], r=S.r)),
        shell(poly([(5, 10.8), (22, 10.8), (20.4, 15.6), (6.2, 15.6)], closed=True, r=S.r * 0.5)),
        shell(circle(9, 20.5, 1.2)), shell(circle(17, 20.5, 1.2)),
    ]


def circle_head(cx, cy):
    return dot(cx, cy, 2.3)


@icon("feedback-kiosk", CAT, "Short post carrying a panel with four round buttons, each with a face from frowning to smiling",
      tags=["happy or not", "satisfaction terminal", "rating buttons", "customer survey", "smiley buttons", "mood rating", "review stand"])
def _(S):
    faces = []
    mouths = ["M8.2 8.8Q9.4 7.6 10.6 8.8", "M13.9 8.4H16.3", "M13.9 14.4Q15.1 15.4 16.3 14.4", "M7.8 14.2Q9.4 16.2 11 14.2"]
    return [
        shell(rect(4, 2.5, 16, 15, rr(S, 3))),
        E(pd(circle(9.4, 7.4, 2.6), thick(mouths[0], 0.9)), pd(circle(14.6, 7.4, 2.6), thick(mouths[1], 0.9)),
          pd(circle(9.4, 13, 2.6), thick("M8.2 13.4H10.6", 0.9)), pd(circle(14.6, 13, 2.6), thick("M13.4 12.6Q14.6 14 15.8 12.6", 0.9))),
        line(seg(12, 17.5, 12, 21)), line(seg(7.5, 21.5, 16.5, 21.5)),
    ]


@icon("self-scan-handset-rack", CAT, "Wall charging rack holding a row of handheld scanners, one lifted halfway out",
      tags=["scanner dock", "handheld scanner charger", "scan and go", "self scanning", "charging cradle", "scan as you shop", "docking rack"])
def _(S):
    def scan(x, y):
        return pd(pu(rect(x, y, 4.6, 3.8, 0.8), rect(x + 1.1, y + 3, 2.4, 6.4, 0.8)), rect(x + 1, y + 0.9, 2.6, 1.4))
    return [
        shell(rect(2.5, 11, 19, 10, rr(S, 2.5))),
        detail(seg(8.8, 11, 8.8, 21)), detail(seg(15.2, 11, 15.2, 21)),
        E(scan(2.9, 5), scan(9.7, 1.8), scan(16.5, 5)),
    ]


@icon("tiered-discount", CAT, "Three price tags in a rising staircase row, each with a percent sign and each taller than the one before",
      tags=["volume discount", "bulk pricing", "buy more save more", "discount levels", "savings tiers", "price breaks", "quantity discount"])
def _(S):
    parts = []
    for x, top in ((1.5, 12), (9, 7.5), (16.5, 3)):
        cx = x + 3
        parts.append(shell(poly([(cx, top), (x + 6, top + 2.5), (x + 6, 21.5), (x, 21.5), (x, top + 2.5)], closed=True, r=S.r * 0.5)))
        y = 17.5
        parts.append(E(circle(cx - 1.2, y - 1.3, 1.0), circle(cx + 1.2, y + 1.3, 1.0), bar(cx + 1.7, y - 2, cx - 1.7, y + 2, 0.9)))
    return parts
