"""TypeIcon Core: hobbies, batch 001 (collecting, games, model making, nature study, gardening, puzzles, origami)."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar, rotation, transform_path

CAT = "hobbies"


def L(S, a, b):
    """Value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def mark(d) -> Part:
    """Small solid shape: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx, cy):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def perf(x0, y0, x1, y1, n, br, rx=0.0):
    """Stamp outline: rectangle with n semicircular bites per edge (rx rounds the corners)."""
    body = rect(x0, y0, x1 - x0, y1 - y0, rx)
    bites = []
    for k in range(n):
        fx = x0 + (k + 0.5) / n * (x1 - x0)
        fy = y0 + (k + 0.5) / n * (y1 - y0)
        bites += [circle(fx, y0, br), circle(fx, y1, br), circle(x0, fy, br), circle(x1, fy, br)]
    return minus(body, *bites)


# ============================================================================ collecting

@icon("perforation-gauge", CAT, "Card ruler with rows of dot scales used to count a stamp's perforations",
      tags=["perforation gauge", "stamp gauge", "philately", "stamp collecting", "measure", "tool"])
def _(S):
    ds = []
    for y in (9.5, 14.5):
        for x in (6.5, 10.5, 14.5, 18.5):
            ds.append(dot(x, y, 1.1))
    return [shell(rect(2.5, 5.5, 19, 13, S.R)), *ds]


@icon("stamp-watermark-tray", CAT, "Shallow black tray with a stamp above it and a drop of watermark fluid",
      tags=["watermark tray", "stamp", "philately", "watermark", "fluid", "stamp collecting"])
def _(S):
    return [shell(poly([(2.5, 13.5), (21.5, 13.5), (19.5, 20.5), (4.5, 20.5)], closed=True, r=S.r)),
            shell(perf(4, 3, 14, 10.5, 2, 0.9, L(S, 0, 1.5))),
            mark("M19 2.5C21.5 6 21.5 8.5 19 9.5C16.5 8.5 16.5 6 19 2.5Z")]


@icon("cancelled-stamp", CAT, "Perforated stamp with a round postmark ring and wavy cancellation lines",
      tags=["cancelled stamp", "postmark", "used stamp", "philately", "postage", "franked"])
def _(S):
    return [shell(perf(3.5, 3, 20.5, 21, 4, 1, L(S, 0, 2))),
            detail(circle(9.5, 14.5, 3.5)),
            detail("M12.5 8q1.5-1.5 3 0t3 0")]


@icon("coin-capsule", CAT, "Round clear coin capsule with a coin inside it",
      tags=["coin capsule", "coin holder", "numismatics", "coin collecting", "protect", "case"])
def _(S):
    coin = poly(regular(12, 12, 5, 10), closed=True) if S.name == "line" else circle(12, 12, 5)
    return [shell(circle(12, 12, 9.5)), detail(coin), dot(12, 12, 1.2)]


@icon("coin-flip-holder", CAT, "Square cardboard coin holder with a round window and staples at the corners",
      tags=["coin flip", "cardboard holder", "numismatics", "coin collecting", "window", "stapled"])
def _(S):
    st = [dot(6.5, 6.5, 1), dot(17.5, 6.5, 1), dot(6.5, 17.5, 1), dot(17.5, 17.5, 1)]
    return [shell(rect(3, 3, 18, 18, S.R)), detail(circle(12, 12, 4.5)), *st]


@icon("coin-slab", CAT, "Tall sealed plastic case with a label strip above a round coin window",
      tags=["coin slab", "graded coin", "numismatics", "certified", "coin collecting", "case"])
def _(S):
    return [shell(rect(5, 2.5, 14, 19, S.R)), detail(seg(5, 8, 19, 8)), detail(circle(12, 15, 3.5))]


@icon("coin-tube", CAT, "Clear cylinder with a screw cap on its side showing a stack of coin edges",
      tags=["coin tube", "coin roll", "numismatics", "stack", "storage", "coin collecting"])
def _(S):
    return [shell(rect(2.5, 6.5, 19, 11, S.R)), detail(seg(7, 6.5, 7, 17.5)),
            detail(seg(11, 9.5, 11, 14.5)), detail(seg(15, 9.5, 15, 14.5)), detail(seg(19, 9.5, 19, 14.5))]


@icon("challenge-coin", CAT, "Thick round coin with a raised star in the middle and a notched rim",
      tags=["challenge coin", "medallion", "token", "military coin", "commemorative", "collectible"])
def _(S):
    star = []
    for i in range(10):
        a = -90 + i * 36
        star.append(polar(12, 12.3, 5 if i % 2 == 0 else 2.2, a))
    rim = poly(regular(12, 12, 9.5, 20), closed=True) if S.name == "line" else circle(12, 12, 9.5)
    return [shell(rim), mark(poly(star, closed=True, r=S.r * 0.3))]


@icon("card-toploader", CAT, "Rigid card holder with a trading card sliding in through the top",
      tags=["toploader", "card holder", "trading card", "card sleeve", "protect", "collecting"])
def _(S):
    return [shell(rect(4.5, 8, 15, 13.5, S.R)),
            line(poly([(8, 8), (8, 3.5), (16, 3.5), (16, 8)], r=S.r * 0.6)),
            detail(rect(8, 12, 8, 5, rr(S, 1)))]


@icon("sticker-album", CAT, "Open album with an empty sticker slot on the left page and filled stickers on the right",
      tags=["sticker album", "sticker book", "collection", "swap", "scrapbook", "collecting"])
def _(S):
    return [shell(rect(2.5, 4.5, 19, 15, S.R)), detail(seg(12, 4.5, 12, 19.5)),
            detail(rect(5.5, 8.5, 4, 4, rr(S, 1))),
            mark(rect(14.5, 7.5, 4, 3.5, 0.5)), mark(rect(14.5, 13, 4, 3.5, 0.5))]


@icon("pin-display-board", CAT, "Pennant shaped board holding four enamel pins",
      tags=["pin board", "enamel pins", "pin collecting", "display", "badges", "pennant"])
def _(S):
    return [shell(poly([(3, 3.5), (21, 3.5), (21, 15), (12, 21.5), (3, 15)], closed=True, r=S.r)),
            dot(8, 8.5, 1.5), dot(16, 8.5, 1.5),
            mark(rect(6.8, 11.8, 2.4, 2.4, 0.4)), mark(poly([(16, 11.5), (17.4, 14.2), (14.6, 14.2)], closed=True))]


@icon("autograph-book", CAT, "Small open book with a looping handwritten signature on the right page",
      tags=["autograph book", "signature", "signed", "memorabilia", "collecting", "celebrity"])
def _(S):
    return [shell(rect(2.5, 5, 19, 14, S.R)), detail(seg(12, 5, 12, 19)),
            detail(seg(5.5, 10, 9, 10)), detail(seg(5.5, 14, 9, 14)),
            line("M14.5 15.5C15 11 17 10 16.8 12.5C16.6 15 14.8 13.5 16.5 12.5C18 11.5 18 14 19.5 13")]


@icon("comic-bag-and-board", CAT, "Comic book in a clear bag with a flap, with the backing board showing behind",
      tags=["comic bag", "backing board", "comic book", "storage", "collecting", "protect"])
def _(S):
    return [shell(rect(3.5, 6.5, 14, 15, rr(S, 2))), detail(seg(3.5, 9.5, 17.5, 9.5)),
            detail(rect(6.5, 12.5, 8, 6, rr(S, 1))),
            line(poly([(6.5, 3.5), (20.5, 3.5), (20.5, 17.5)], r=S.r * 0.6))]


def mir(d):
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


# ============================================================================ displays, toys and games

@icon("butterfly-display-case", CAT, "Framed display box with a pinned butterfly in the middle",
      tags=["butterfly case", "entomology", "specimen", "pinned butterfly", "display frame", "collecting"])
def _(S):
    up = "M11 11.2C10.5 8.2 8.2 6.2 6.8 7C5.6 8 6.4 11.2 11 11.2Z"
    lo = "M11 12.6C7.6 12.8 6.6 15 7.6 16C8.6 16.6 10.6 15.6 11 12.6Z"
    return [shell(rect(2.5, 3, 19, 18, S.R)), mark(up), mark(mir(up)), mark(lo), mark(mir(lo)),
            mark(rect(11.2, 8.5, 1.6, 7.5, 0.8))]


@icon("die-cast-car", CAT, "Small toy car in side view on a blister card with a hanging hole",
      tags=["die cast", "toy car", "model car", "collectible", "blister pack", "miniature"])
def _(S):
    car = poly([(6, 16.5), (6, 14), (8.5, 14), (10, 11.5), (14, 11.5), (15.5, 14), (18, 14), (18, 16.5)], closed=True, r=S.r * 0.4)
    return [shell(rect(3, 2.5, 18, 19, rr(S, 2.5))), dot(12, 5.8, 1.3), detail(car),
            mark(circle(9, 17.8, 1.4)), mark(circle(15, 17.8, 1.4))]


@icon("curio-cabinet", CAT, "Tall glass fronted cabinet with three shelves of small collectibles",
      tags=["curio cabinet", "display cabinet", "collection", "shelves", "vitrine", "collectibles"])
def _(S):
    return [shell(rect(4.5, 2, 15, 20, S.R)), detail(seg(4.5, 8.5, 19.5, 8.5)), detail(seg(4.5, 15.2, 19.5, 15.2)),
            mark("M8 7C8 5.5 9.2 5.5 9.2 4.8H10.8C10.8 5.5 12 5.5 12 7Z"), mark(circle(15, 5.8, 1.3)),
            mark(circle(12, 11.2, 1.1)), mark(rect(10.8, 12.4, 2.4, 1.6, 0.3)),
            mark(rect(7.5, 18.4, 9, 1.4, 0.7))]


@icon("tin-toy-robot", CAT, "Boxy retro toy robot with an antenna, round eyes and a wind-up key on its side",
      tags=["tin robot", "wind up toy", "retro toy", "vintage toy", "robot", "collectible"])
def _(S):
    return [shell(rect(8, 5, 8, 5.5, rr(S, 1.5))), line(seg(12, 2.5, 12, 5)),
            dot(10.4, 7.7, 0.9), dot(13.6, 7.7, 0.9),
            shell(rect(7, 12, 10, 6.5, rr(S, 1.5))), dot(12, 15.2, 1.1),
            line(seg(3.5, 12.5, 3.5, 17)), line(seg(9.5, 18.5, 9.5, 21.5)), line(seg(14.5, 18.5, 14.5, 21.5)),
            line(seg(17.5, 14.5, 19.5, 14.5)), dot(20, 14.5, 1.5)]


@icon("blind-box", CAT, "Small cube box with a question mark on the front and its lid slightly raised",
      tags=["blind box", "mystery box", "surprise", "collectible toy", "unboxing", "question mark"])
def _(S):
    return [shell(rect(3, 3, 18, 4, rr(S, 1.5))), shell(rect(4.5, 9, 15, 12.5, S.R)),
            detail("M10.4 13.2a1.7 1.7 0 1 1 2.6 1.4c-.7.4-1 .8-1 1.5"), dot(12, 18.7, 1)]


@icon("polyhedral-dice-set", CAT, "Four gaming dice: a twenty sided, a six sided, a four sided and an eight sided die",
      tags=["dnd dice", "rpg dice", "d20", "tabletop", "role playing", "dice set", "polyhedral"])
def _(S):
    return [shell(poly(regular(7.5, 7.5, 5, 6, start=-90), closed=True, r=S.r * 0.5)), dot(7.5, 7.5, 1.2),
            shell(rect(14.5, 3.5, 7, 7, rr(S, 1.5))), dot(18, 7, 1.1),
            shell(poly([(7.5, 14), (11.5, 21), (3.5, 21)], closed=True, r=S.r * 0.5)),
            shell(poly([(17.5, 13.5), (21.5, 17.5), (17.5, 21.5), (13.5, 17.5)], closed=True, r=S.r * 0.5))]


@icon("deck-box", CAT, "Card deck box with its flip top lid tipped open above the box",
      tags=["deck box", "card box", "trading cards", "card game", "storage", "tcg"])
def _(S):
    return [shell(poly([(7, 2.5), (17, 2.5), (19, 7), (5, 7)], closed=True, r=S.r * 0.6)),
            shell(rect(5, 10, 14, 11.5, S.R)), detail(rect(9, 13.5, 6, 4, rr(S, 1)))]


_HEX_R = 4.0
_HEX_DX = _HEX_R * math.sqrt(3)


def _hex(cx, cy, rad=_HEX_R, rc=0.0):
    return poly(regular(cx, cy, rad, 6, start=-90), closed=True, r=rc)


@icon("hex-map", CAT, "Tabletop game map of interlocking hexagon cells with a tree and a shaded terrain hex",
      tags=["hex map", "hex grid", "wargame", "tabletop", "terrain", "board game", "hexagon"])
def _(S):
    ax, bx, cx_ = 12 - _HEX_DX / 2, 12 + _HEX_DX / 2, 12
    ys, yb = 8.5, 14.5
    outline = union(_hex(ax, ys, rc=L(S, 0, 1.3)), _hex(bx, ys, rc=L(S, 0, 1.3)), _hex(cx_, yb, rc=L(S, 0, 1.3)))
    return [shell(outline),
            detail(poly([(12 - _HEX_DX / 2, yb - 2), (12, yb - 4), (12 + _HEX_DX / 2, yb - 2)])),
            detail(seg(12, ys - 2, 12, yb - 4)),
            mark(poly([(ax, ys - 1.8), (ax + 1.2, ys + 0.6), (ax - 1.2, ys + 0.6)], closed=True)),
            mark(poly(regular(cx_, yb + 0.6, 1.6, 6, start=-90), closed=True))]


@icon("pigeon-loft", CAT, "Small raised loft with a pitched roof, a row of entry holes and a landing board",
      tags=["pigeon loft", "dovecote", "pigeon racing", "bird house", "coop", "racing pigeons"])
def _(S):
    return [shell(poly([(3.5, 9.5), (12, 3), (20.5, 9.5), (20.5, 17), (3.5, 17)], closed=True, r=S.r)),
            dot(8.5, 10.8, 1.2), dot(12, 10.8, 1.2), dot(15.5, 10.8, 1.2),
            detail(seg(3.5, 14, 20.5, 14)),
            line(seg(6.5, 17, 6.5, 21.5)), line(seg(17.5, 17, 17.5, 21.5))]


@icon("model-train-set", CAT, "Oval loop of track above a tiny locomotive and wagon",
      tags=["model train", "train set", "toy train", "railway", "locomotive", "hobby", "oval track"])
def _(S):
    return [line(ellipse(12, 8.5, 9.5, 5)), line(ellipse(12, 8.5, 4.8, 1.8)),
            shell(rect(3, 16.5, 9, 4.5, S.R * 0.5)), shell(rect(14, 17, 7, 4, S.R * 0.5)),
            line(seg(12, 18.7, 14, 18.7))]


@icon("model-railway-track", CAT, "Curved sectional piece of model railway track with sleepers across two rails",
      tags=["model railway", "track piece", "railroad", "sleepers", "ties", "curve", "hobby train"])
def _(S):
    cx = cy = 2.0
    out = []
    for a in (15, 30, 45, 60, 75):
        p1 = polar(cx, cy, 10, a)
        p2 = polar(cx, cy, 18.5, a)
        out.append(detail(seg(*p1, *p2)))
    return [line(arc(cx, cy, 12.3, 8, 82)), line(arc(cx, cy, 16.3, 8, 82)), *out]


@icon("train-set-controller", CAT, "Small boxy speed controller with a round dial, a toggle and a wire trailing out",
      tags=["train controller", "throttle", "model railway", "speed control", "transformer", "dial"])
def _(S):
    return [shell(rect(2.5, 4.5, 16, 14, S.R)), detail(circle(9, 11.5, 3.6)), detail(seg(9, 11.5, 9, 9.2)),
            detail(seg(15, 7.5, 15, 10.5)), dot(15, 14.5, 1),
            line(poly([(18.5, 15), (21.5, 15), (21.5, 21)], r=S.r * 0.6))]


@icon("model-railway-layout", CAT, "Raised baseboard table seen in perspective with a hill, a tree and track across the top",
      tags=["model railway layout", "baseboard", "diorama", "scenery", "train table", "hobby"])
def _(S):
    return [shell(poly([(6, 4.5), (21.5, 4.5), (18, 16), (2.5, 16)], closed=True, r=S.r)),
            detail(seg(5, 13, 19, 13)),
            mark("M7 11 L9.5 7.6 L12 11Z"), dot(16, 8.3, 1.6),
            line(seg(4.5, 16, 4.5, 21.5)), line(seg(16.5, 16, 16.5, 21.5))]


@icon("rc-airplane", CAT, "Small high wing model airplane with a propeller in side view and an antenna wire on the tail",
      tags=["rc plane", "model aircraft", "radio control", "remote control plane", "hobby flying", "propeller"])
def _(S):
    body = "M7 10.5H17L21 7.5V11.5L17.5 14.5H7A2 2 0 0 1 7 10.5Z"
    return [shell(body), line(seg(7, 6.8, 17, 6.8)), line(seg(10, 6.8, 10, 10.5)), line(seg(14.5, 6.8, 14.5, 10.5)),
            line(seg(3.5, 9, 3.5, 16)), line(seg(10, 14.5, 10, 17)), dot(10, 18, 1.6),
            line(seg(19.5, 4, 19.5, 7))]


def lens(x0, y0, x1, y1, w):
    """Leaf shaped lens from (x0,y0) to (x1,y1), w wide in the middle."""
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy)
    nx, ny = -dy / ln * w, dx / ln * w
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    return (f"M{fmt(x0)} {fmt(y0)}Q{fmt(mx + nx)} {fmt(my + ny)} {fmt(x1)} {fmt(y1)}"
            f"Q{fmt(mx - nx)} {fmt(my - ny)} {fmt(x0)} {fmt(y0)}Z")


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def trot(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


# ============================================================================ nature study, gardens

@icon("bird-checklist", CAT, "Clipboard with a small bird at the top and a list of rows, two of them ticked",
      tags=["bird checklist", "life list", "birdwatching", "birding", "sightings", "tally", "bird log"])
def _(S):
    bird = "M6.5 9.2C6.5 7.2 8.5 6.4 10 6.8L12.5 6.4L12.2 8C12 9.4 10.5 10 8.5 10Z"
    return [shell(rect(4.5, 4, 15, 17.5, S.R)), solid(rect(8.5, 2.5, 7, 3.4, 1)),
            mark(bird), mark("M12.2 7.2L15 6.2L14.2 8.6Z"),
            dot(8, 13.2, 1.1), seg_part(11, 13.2, 16, 13.2),
            dot(8, 16.4, 1.1), seg_part(11, 16.4, 16, 16.4),
            seg_part(11, 19.6, 16, 19.6)]


def seg_part(x1, y1, x2, y2):
    return detail(seg(x1, y1, x2, y2))


@icon("digiscoping", CAT, "Spotting scope on a short tripod with a phone clamped to the eyepiece end",
      tags=["digiscoping", "spotting scope", "bird photography", "phone adapter", "tripod", "wildlife photography"])
def _(S):
    return [shell(rect(5.5, 8, 10, 5, S.R * 0.5)), line(seg(3.5, 6.5, 3.5, 14.5)),
            shell(rect(17, 5.5, 4.5, 9.5, rr(S, 1.5))),
            line(poly([(6, 21.5), (10.5, 16), (15, 21.5)], r=S.r * 0.6)), line(seg(10.5, 13, 10.5, 21.5))]


@icon("star-atlas", CAT, "Open book with a constellation of dots joined by lines across its pages",
      tags=["star atlas", "star chart", "constellation", "astronomy", "stargazing", "sky guide"])
def _(S):
    return [shell(poly([(2.5, 5.5), (12, 8), (21.5, 5.5), (21.5, 19), (12, 21), (2.5, 19)], closed=True, r=S.r)),
            detail(poly([(6.5, 15.5), (9, 11.5), (14.5, 14.5), (17.5, 10.5)], r=0)),
            dot(6.5, 15.5, 1.5), dot(9, 11.5, 1.5), dot(14.5, 14.5, 1.5), dot(17.5, 10.5, 1.5)]


@icon("moon-map", CAT, "Round lunar disc with crater marks and two leader lines pointing out to labels",
      tags=["moon map", "lunar map", "crater", "moon atlas", "astronomy", "selenography", "lunar observing"])
def _(S):
    return [shell(circle(9, 12, 7)), dot(6.8, 9.6, 1.3), dot(11.5, 13.5, 1.8), dot(7, 15.2, 1.1),
            line(seg(17, 8.5, 21.5, 8.5)), line(seg(17, 15.5, 21.5, 15.5))]


@icon("solar-filter", CAT, "Telescope tube with a dark filter cap on its front and a sun with rays above",
      tags=["solar filter", "sun observing", "solar telescope", "eclipse", "astronomy", "safe viewing"])
def _(S):
    rays = [line(seg(*polar(17, 7, 3.3, a), *polar(17, 7, 4.9, a))) for a in (0, 45, 90, 180, 225, 270, 315)]
    return [shell(rect(2.5, 13, 9.5, 6.5, S.R * 0.5)), solid(rect(12, 12, 3.2, 8.5, 0.5)),
            dot(17, 7, 1.7), *rays]


@icon("tree-grafting", CAT, "Branch piece joined to a trunk at an angled cut, wrapped with tape and a bud on top",
      tags=["grafting", "scion", "rootstock", "fruit tree", "orchard", "propagation", "grafting tape"])
def _(S):
    scion = path_to_d(transform_path(P(rect(10, 2.5, 4.4, 12)), rotation(22, 12.2, 14)))
    outline = union(rect(7, 13, 10, 9), scion)
    return [shell(outline), detail(seg(7, 16, 17, 16)), detail(seg(7, 19.3, 17, 19.3)),
            mark(lens(15.5, 6, 19.5, 3.4, 1.1))]


@icon("bottle-garden", CAT, "Round bellied glass bottle with soil and small plants growing inside",
      tags=["bottle garden", "terrarium", "carboy", "glass jar garden", "closed terrarium", "indoor plants"])
def _(S):
    body = union(rect(9.6, 3, 4.8, 6.5, L(S, 0, 1.2)), circle(12, 14.2, 7.3))
    return [shell(body), detail("M6.6 18Q12 16.2 17.4 18"),
            line(seg(12, 16.6, 12, 11.2)), mark(lens(12, 14.2, 8.4, 11.6, 1.2)), mark(lens(12, 14.2, 15.6, 11.6, 1.2)),
            mark(lens(12, 11.4, 12, 8, 1.1))]


@icon("fairy-garden", CAT, "Tiny arched door and round window in a tree stump with two mushrooms beside it",
      tags=["fairy garden", "miniature garden", "gnome door", "tree stump", "mushroom", "fantasy garden"])
def _(S):
    stump = poly([(3.5, 21.5), (4.5, 8.5), (9.5, 6.5), (14.5, 8.5), (15.5, 21.5)], closed=True, r=S.r)
    return [shell(stump), detail("M7.5 21.5V16.7a2 2 0 0 1 4 0V21.5"), dot(9.5, 11.5, 1.1),
            mark("M16.8 15a2.7 2.7 0 0 1 5.4 0Z"), mark(rect(18.2, 15, 2.6, 4, 0.4)),
            mark("M17.8 21.8a1.8 1.8 0 0 1 3.6 0Z")]


@icon("alpine-trough", CAT, "Low stone trough holding small rocks and cushion shaped alpine plants",
      tags=["alpine trough", "rock garden", "stone planter", "alpine plants", "cushion plants", "sink garden"])
def _(S):
    return [shell(poly([(2.5, 12), (21.5, 12), (20, 20.5), (4, 20.5)], closed=True, r=S.r)),
            mark("M5.5 12L7.5 7.5L11 8.5L12.2 12Z"), mark("M13.2 12a3.4 3.4 0 0 1 6.8 0Z")]


@icon("plant-label", CAT, "Pointed marker stake with writing lines on its flat top, next to a small seedling",
      tags=["plant label", "plant marker", "garden stake", "seed label", "seedling", "garden tag"])
def _(S):
    return [shell(poly([(3, 3), (11.5, 3), (11.5, 15), (7.25, 21.5), (3, 15)], closed=True, r=S.r * 0.6)),
            mark(rect(5.2, 6.4, 4.1, 1.6, 0.5)), mark(rect(5.2, 10, 4.1, 1.6, 0.5)),
            line(seg(13, 21.5, 22, 21.5)), line(seg(17.5, 21, 17.5, 13.5)),
            mark(lens(17.5, 14.5, 14, 11, 1.4)), mark(lens(17.5, 14.5, 21, 11, 1.4))]


@icon("moss-pole", CAT, "Potted climbing plant with large leaves winding up a fuzzy vertical pole",
      tags=["moss pole", "climbing plant", "monstera", "houseplant", "support", "plant stake", "pothos"])
def _(S):
    return [shell(poly([(6, 16.5), (18, 16.5), (16.5, 21.5), (7.5, 21.5)], closed=True, r=S.r * 0.6)),
            shell(rect(10, 3, 4, 11, rr(S, 1.5))),
            mark(lens(10, 11, 4.5, 7.5, 2)), mark(lens(14, 7.5, 19.5, 4, 2)), mark(lens(14, 13, 20, 12, 2.2))]


@icon("water-propagation", CAT, "Wide mouthed glass jar of water with a stem cutting and white roots growing in it",
      tags=["water propagation", "cutting", "rooting", "stem cutting", "jar", "houseplant", "propagating"])
def _(S):
    return [shell(rect(5.5, 10, 13, 11.5, S.R)), line(seg(12, 4, 12, 10)), detail(seg(12, 10, 12, 13.5)),
            detail(poly([(12, 13.5), (9, 18.2)])), detail(poly([(12, 13.5), (15, 18.2)])), detail(seg(12, 13.5, 12, 18.5)),
            mark(lens(12, 6.8, 7.8, 3.4, 1.3)), mark(lens(12, 6.8, 16.5, 3.4, 1.3))]


@icon("bonsai-wire", CAT, "Small curved tree branch wrapped with wire, with a coil of spare wire beside it",
      tags=["bonsai wire", "training wire", "bonsai", "wiring", "branch shaping", "coil", "aluminum wire"])
def _(S):
    p = [(4.5, 15.5), (8, 17), (11, 6), (19, 6.5)]
    path = f"M{p[0][0]} {p[0][1]}C{p[1][0]} {p[1][1]} {p[2][0]} {p[2][1]} {p[3][0]} {p[3][1]}"
    tube = path_to_d(ST(path, 4.2, S.cap, S.join))
    wraps = []
    for t in (0.2, 0.36, 0.52, 0.7, 0.86):
        x, y = bez(*p, t)
        x2, y2 = bez(*p, t + 0.01)
        dx, dy = x2 - x, y2 - y
        ln = math.hypot(dx, dy)
        tx, ty, nx, ny = dx / ln, dy / ln, -dy / ln, dx / ln
        wraps.append(detail(seg(x - nx * 2.1 - tx * 0.9, y - ny * 2.1 - ty * 0.9, x + nx * 2.1 + tx * 0.9, y + ny * 2.1 + ty * 0.9)))
    return [shell(tube), *wraps, line(circle(17.5, 18, 3.6)), dot(17.5, 18, 1.1)]


@icon("vertical-garden", CAT, "Wall panel with a grid of fabric pockets, each holding a small plant",
      tags=["vertical garden", "living wall", "wall planter", "green wall", "pocket planter", "urban gardening"])
def _(S):
    out = [shell(rect(3, 3, 18, 18, S.R)), detail(seg(3, 12, 21, 12)), detail(seg(12, 3, 12, 21))]
    for cx in (7.5, 16.5):
        for by in (9.7, 19.0):
            out += [mark(lens(cx, by, cx - 2.2, by - 3.4, 1.0)), mark(lens(cx, by, cx + 2.2, by - 3.4, 1.0))]
    return out


@icon("herb-pot", CAT, "Terracotta pot holding three small herb sprigs with different leaf shapes",
      tags=["herb pot", "kitchen herbs", "windowsill garden", "basil", "parsley", "potted herbs"])
def _(S):
    return [shell(poly([(6, 14.5), (18, 14.5), (16.5, 21.5), (7.5, 21.5)], closed=True, r=S.r * 0.6)),
            line(seg(12, 14.5, 12, 6)), mark(lens(12, 12.5, 8.6, 9.8, 1.3)), mark(lens(12, 12.5, 15.4, 9.8, 1.3)),
            mark(lens(12, 8.2, 12, 3.6, 1.4)),
            line(seg(8.5, 14.5, 6, 9)), mark(lens(6, 9.4, 3.6, 5.4, 1.2)),
            line(seg(15.5, 14.5, 18, 9)), mark(circle(18.6, 7.6, 1.6))]


@icon("square-foot-garden", CAT, "Square raised bed divided by slats into nine squares with different small plants",
      tags=["square foot garden", "raised bed", "grid garden", "vegetable garden", "allotment", "planting grid"])
def _(S):
    out = [shell(rect(3, 3, 18, 18, S.R)), detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)),
           detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15))]
    for i, cy in enumerate((6, 12, 18)):
        for j, cx in enumerate((6, 12, 18)):
            k = (i + j) % 3
            if k == 0:
                out.append(mark(circle(cx, cy, 1.1)))
            elif k == 1:
                out.append(mark(poly([(cx, cy - 1.3), (cx + 1.2, cy + 1), (cx - 1.2, cy + 1)], closed=True)))
            else:
                out.append(mark(rect(cx - 1, cy - 1, 2, 2, 0.3)))
    return out


@icon("self-watering-pot", CAT, "Small pot above a water reservoir joined by a wick, with a level mark in the reservoir",
      tags=["self watering pot", "wick", "reservoir", "planter", "water level", "houseplant", "sub irrigation"])
def _(S):
    return [shell(poly([(6.5, 5.5), (17.5, 5.5), (16, 11), (8, 11)], closed=True, r=S.r * 0.5)),
            mark(lens(12, 5.5, 9.5, 2.6, 1.0)), mark(lens(12, 5.5, 14.5, 2.6, 1.0)),
            shell(rect(3, 13.5, 18, 8, S.R)), line(seg(12, 11, 12, 18)),
            detail(seg(5.5, 18, 8.5, 18))]


@icon("honeycomb-frame", CAT, "Rectangular beehive frame holding hexagon comb cells, one of them capped",
      tags=["honeycomb frame", "beehive", "beekeeping", "apiary", "comb", "honey frame", "hive"])
def _(S):
    r = 3.3
    dx = r * math.sqrt(3)
    hexes = [(12 - dx / 2, 9.4), (12 + dx / 2, 9.4), (12, 14.6)]
    cells = union(*[poly(regular(x, y, r, 6, start=-90), closed=True) for x, y in hexes])
    return [shell(rect(3, 3, 18, 18, S.R * 0.5)), detail(cells),
            detail(poly([(12 - dx / 2 - 0.0, 14.6 - r / 2 - 0.0), (12, 14.6 - r), (12 + dx / 2, 14.6 - r / 2)])),
            mark(poly(regular(12, 14.6, 1.2, 6, start=-90), closed=True))]


@icon("dish-garden", CAT, "Shallow wide bowl holding three different small cacti and succulents",
      tags=["dish garden", "succulents", "cactus bowl", "miniature desert", "houseplant", "succulent planter"])
def _(S):
    bowl = poly([(2.5, 14.5), (21.5, 14.5), (19, 20), (5, 20)], closed=True, r=S.r) if S.name == "line" else "M2.5 14.5H21.5C21.5 19 17.5 21 12 21S2.5 19 2.5 14.5Z"
    return [shell(bowl),
            mark(rect(10.8, 5, 2.6, 9.5, 1.3)), mark(rect(8.4, 8.2, 2.4, 1.6, 0.8)), mark(rect(13.4, 6.8, 2.4, 1.6, 0.8)),
            mark(lens(6.6, 14.5, 3.8, 9.6, 1.1)), mark(lens(6.6, 14.5, 6.6, 8.6, 1.1)), mark(lens(6.6, 14.5, 9.4, 9.8, 1.1)),
            mark(circle(17.8, 12.2, 2.2))]


# ============================================================================ puzzles and paper

@icon("chess-problem", CAT, "Corner of a chessboard with a king and a curved arrow showing the mating move",
      tags=["chess problem", "chess puzzle", "mate in one", "king", "chessboard", "endgame study"])
def _(S):
    return [shell(rect(3, 12, 9.5, 9.5, rr(S, 1.5))), mark(rect(3.8, 12.8, 4, 4)), mark(rect(7.8, 16.8, 4, 4)),
            line(seg(17.5, 3, 17.5, 6)), line(seg(16, 4.5, 19, 4.5)),
            shell(poly([(15, 12), (16, 7.5), (19, 7.5), (20, 12)], closed=True, r=S.r * 0.4)),
            line(seg(14.5, 14.8, 20.5, 14.8)),
            line("M14 20.5Q20.5 20.5 20.5 17.6"), line(poly([(18.7, 18.4), (20.5, 16.4), (22.2, 18.4)]))]


@icon("soma-cube", CAT, "Cube made of irregular pieces with seams, and a small L shaped piece lifted away beside it",
      tags=["soma cube", "cube puzzle", "packing puzzle", "polycube", "brain teaser", "3d puzzle"])
def _(S):
    c = (9, 15)
    return [shell(poly([(9, 8.5), (14.6, 11.75), (14.6, 18.25), (9, 21.5), (3.4, 18.25), (3.4, 11.75)], closed=True, r=S.r * 0.4)),
            detail(poly([(3.4, 11.75), (9, 15), (14.6, 11.75)])), detail(seg(9, 15, 9, 21.5)),
            shell(poly([(15.5, 3), (21.5, 3), (21.5, 6.2), (18.7, 6.2), (18.7, 9), (15.5, 9)], closed=True, r=S.r * 0.4))]


@icon("sliding-block-puzzle", CAT, "Square tray with blocks of different sizes and a gap in the right wall as the exit",
      tags=["sliding block puzzle", "klotski", "unblock", "escape puzzle", "brain teaser", "logic puzzle"])
def _(S):
    return [line(poly([(21.5, 8.5), (21.5, 2.5), (2.5, 2.5), (2.5, 21.5), (21.5, 21.5), (21.5, 15.5)], r=S.r * 0.6)),
            mark(rect(5.5, 5.5, 7, 7, 0.8)), mark(rect(14.5, 5.5, 4, 7, 0.8)),
            mark(rect(5.5, 15, 4, 3.5, 0.8)), mark(rect(11.5, 15, 7, 3.5, 0.8))]


@icon("megaminx", CAT, "Twisty puzzle face: a central pentagon with five surrounding sections inside a pentagon outline",
      tags=["megaminx", "dodecahedron puzzle", "twisty puzzle", "speedcubing", "pentagon", "cube puzzle"])
def _(S):
    outer = regular(12, 12.8, 9.7, 5)
    inner = regular(12, 12.8, 4, 5)
    return [shell(poly(outer, closed=True, r=S.r * 1.6)), detail(poly(inner, closed=True, r=S.r * 0.8)),
            *[detail(seg(*inner[i], *outer[i])) for i in range(5)]]


@icon("twisty-snake-puzzle", CAT, "Two strips of triangular segments folded into a zigzag, like a snake puzzle",
      tags=["twisty snake", "snake cube", "rubiks snake", "folding puzzle", "twist puzzle", "triangle prisms"])
def _(S):
    def strip(y0, y1, x0):
        top = [(x0 + 6 * i, y0) for i in range(3)]
        bot = [(x0 + 3 + 6 * i, y1) for i in range(2)]
        pts = [top[0], top[1], top[2], bot[1], bot[0]]
        return pts
    a = strip(3.5, 10.5, 3)
    b = strip(13.5, 20.5, 9)
    return [shell(poly(a, closed=True, r=S.r * 0.4)), detail(seg(*a[1], *a[4])), detail(seg(*a[1], *a[3])),
            shell(poly(b, closed=True, r=S.r * 0.4)), detail(seg(*b[1], *b[4])), detail(seg(*b[1], *b[3]))]


@icon("puzzle-globe", CAT, "Sphere made of curved interlocking jigsaw pieces with one piece lifted away from it",
      tags=["puzzle globe", "3d puzzle", "sphere puzzle", "jigsaw ball", "world puzzle", "earth puzzle"])
def _(S):
    return [shell(circle(9.5, 14.5, 7.5)), detail("M2.5 14.5Q9.5 17.5 16.5 14.5"), detail("M9.5 7Q6.8 14.5 9.5 22"),
            shell(union(rect(16.5, 4, 5, 5, S.R * 0.5), circle(19, 4, 1.5)))]


@icon("cryptogram", CAT, "Row of letter boxes with numbers beneath, two of the boxes filled in with letters",
      tags=["cryptogram", "cipher puzzle", "code puzzle", "substitution cipher", "word puzzle", "decode"])
def _(S):
    out = []
    for i, x in enumerate((2.5, 9, 15.5)):
        out.append(shell(rect(x, 4.5, 6, 7, S.R * 0.5)))
        for k in range(i + 1):
            out.append(mark(rect(x + 0.9 + k * 1.9, 14.5, 1.2, 4.5, 0.4)))
    return [*out, mark(circle(5.5, 8, 1.4)), mark(circle(18.5, 8, 1.4))]


@icon("rebus", CAT, "An eye, a plus sign and a letter in a row, a picture word puzzle",
      tags=["rebus", "picture puzzle", "word puzzle", "riddle", "eye plus letter", "brain teaser"])
def _(S):
    return [shell("M2.5 12Q6.7 6.2 10.9 12Q6.7 17.8 2.5 12Z", stroke_miterlimit="3"), dot(6.7, 12, 1.5),
            line(seg(13.2, 12, 16.6, 12)), line(seg(14.9, 10.3, 14.9, 13.7)),
            line(seg(18, 8, 22, 8)), line(seg(20, 8, 20, 17))]


@icon("cube-timer", CAT, "Flat timer mat with a palm pad on each side of a small digital time display",
      tags=["cube timer", "speedcubing", "stackmat", "solve timer", "stopwatch", "timer mat"])
def _(S):
    return [shell(rect(2.5, 6.5, 19, 11, S.R)), dot(6.2, 12, 2.4), dot(17.8, 12, 2.4),
            mark(rect(9.5, 9.5, 5, 5, 0.8))]


@icon("jigsaw-box", CAT, "Puzzle box lid showing a mountain picture, with two loose jigsaw pieces in front",
      tags=["jigsaw box", "jigsaw puzzle", "puzzle box", "pieces", "mountain scene", "puzzling"])
def _(S):
    p1 = union(rect(4.5, 18, 4.5, 3.5, 0.6), circle(6.75, 18, 1.2))
    p2 = union(rect(13, 18, 4.5, 3.5, 0.6), circle(15.25, 18, 1.2))
    return [shell(rect(2.5, 2.5, 19, 12.5, S.R * 0.5)),
            detail(poly([(5, 13), (9.5, 7), (12.5, 10.5), (14.5, 8.5), (19, 13)])), dot(8, 6.2, 1),
            mark(p1), mark(p2)]


def _pl(pts, S, k=0.5):
    return poly(pts, closed=True, r=S.r * k)


@icon("origami-frog", CAT, "Faceted folded paper frog in side view with crouched back legs and an angular body",
      tags=["origami frog", "paper frog", "paper folding", "jumping frog", "folded paper", "animal origami"])
def _(S):
    body = [(2.5, 15.5), (6.5, 9), (13, 8), (17.5, 11.5), (21.5, 19.5), (14.5, 19.5), (10, 16.5), (7.5, 19.5), (4, 17.5)]
    return [shell(_pl(body, S)), detail(seg(6.5, 9, 10, 16.5)), detail(seg(13, 8, 10, 16.5)),
            detail(seg(17.5, 11.5, 14.5, 19.5)), dot(6.3, 12.8, 0.9)]


@icon("origami-fox", CAT, "Folded paper fox face seen from the front with two pointed ears and a creased snout",
      tags=["origami fox", "paper fox", "paper folding", "fox face", "folded paper", "animal origami"])
def _(S):
    head = [(3, 3), (9, 7.5), (15, 7.5), (21, 3), (21, 13), (12, 21.5), (3, 13)]
    return [shell(_pl(head, S)), detail(poly([(9, 7.5), (12, 14.5), (15, 7.5)])),
            dot(7.5, 11.5, 1), dot(16.5, 11.5, 1), mark(poly([(11, 19), (13, 19), (12, 20.4)], closed=True))]


@icon("origami-lily", CAT, "Folded paper lily with four pointed petals curling outward around a narrow centre",
      tags=["origami lily", "paper flower", "paper folding", "folded flower", "petals", "flower origami"])
def _(S):
    petal = [(12, 12), (8.6, 7.2), (12, 2.5), (15.4, 7.2)]
    pets = []
    for k in range(4):
        pts = trot(petal, 90 * k)
        pets.append(poly(pts, closed=True))
    return [shell(union(*pets)), dot(12, 12, 1.3)]


@icon("origami-masu-box", CAT, "Square folded paper box seen from above with diagonal creases on the inside walls",
      tags=["masu box", "origami box", "paper box", "paper folding", "folded box", "square box"])
def _(S):
    return [shell(poly([(3, 4), (21, 4), (21, 20), (3, 20)], closed=True, r=S.r * 0.6)),
            detail(poly([(8.8, 9), (15.2, 9), (15.2, 15), (8.8, 15)], closed=True)),
            detail(seg(4, 5, 8.8, 9)), detail(seg(20, 5, 15.2, 9)), detail(seg(4, 19, 8.8, 15)), detail(seg(20, 19, 15.2, 15))]


@icon("origami-butterfly", CAT, "Folded paper butterfly with triangular wings, a creased centre line and a folded body",
      tags=["origami butterfly", "paper butterfly", "paper folding", "folded paper", "insect origami", "wings"])
def _(S):
    body = [(12, 10), (3, 4.5), (3.5, 12.5), (7, 20), (12, 14.5), (17, 20), (20.5, 12.5), (21, 4.5)]
    return [shell(_pl(body, S)), detail(seg(12, 10.5, 12, 14)), detail(seg(12, 12, 5.8, 7.4)), detail(seg(12, 12, 18.2, 7.4))]


@icon("origami-water-bomb", CAT, "Inflated paper cube with diagonal fold lines on its faces and a small blow hole at the top",
      tags=["water bomb", "paper balloon", "origami balloon", "inflatable", "paper folding", "paper cube"])
def _(S):
    hexa = [(12, 2.5), (19.8, 7), (19.8, 17), (12, 21.5), (4.2, 17), (4.2, 7)]
    return [shell(_pl(hexa, S, 0.4)), detail(poly([(4.2, 7), (12, 12), (19.8, 7)])), detail(seg(12, 12, 12, 21.5)),
            dot(12, 7, 1.3)]


@icon("origami-swan", CAT, "Folded paper swan with a long upright neck, a sharp beak and flat angled wing folds",
      tags=["origami swan", "paper swan", "paper folding", "folded bird", "swan", "bird origami"])
def _(S):
    body = [(2.5, 6.5), (6.5, 3), (10, 5), (9.5, 13.5), (21.5, 9.5), (17, 20), (7.5, 20), (5.5, 14), (6, 8.5)]
    return [shell(_pl(body, S, 0.4)), detail(seg(9.5, 13.5, 16, 19)), detail(seg(9.5, 13.5, 13, 20)), dot(7.6, 6, 0.8)]


@icon("origami-rabbit", CAT, "Faceted paper rabbit sitting upright with two long pointed ears and a round tail",
      tags=["origami rabbit", "paper rabbit", "paper bunny", "paper folding", "folded paper", "animal origami"])
def _(S):
    body = [(8, 2.5), (10.5, 9.5), (13.5, 9.5), (16, 2.5), (17, 10.5), (18.5, 15), (20.5, 21.5), (4.5, 21.5), (6.5, 15), (7, 10.5)]
    return [shell(_pl(body, S, 0.4)), detail(poly([(7, 10.5), (12, 16), (17, 10.5)])), dot(16.5, 19.2, 1.2)]


@icon("origami-shirt", CAT, "Folded paper shirt with a pointed collar, short folded sleeves and a straight hem",
      tags=["origami shirt", "paper shirt", "paper folding", "folded shirt", "collar", "dollar shirt"])
def _(S):
    body = [(8, 3), (3, 6.5), (5.5, 11), (7.5, 9.5), (7.5, 21), (16.5, 21), (16.5, 9.5), (18.5, 11), (21, 6.5), (16, 3)]
    return [shell(_pl(body, S, 0.4)), detail(poly([(8.8, 3), (12, 8.5), (15.2, 3)])), detail(seg(7.5, 9.5, 4.8, 7.6)), detail(seg(16.5, 9.5, 19.2, 7.6))]


@icon("origami-whale", CAT, "Angular folded paper whale with a flat belly, a raised split tail and a crease along the body",
      tags=["origami whale", "paper whale", "paper folding", "folded paper", "sea animal origami", "tail"])
def _(S):
    body = [(2.5, 15), (5.5, 10), (12, 9), (17, 10.5), (17.5, 4.5), (19.5, 8), (22, 5.5), (18, 14), (14, 18.5), (6, 18.5)]
    return [shell(_pl(body, S, 0.4)), detail(seg(5.5, 10, 10, 18.5)), detail(seg(12, 9, 14, 18.5)), dot(6.8, 13.2, 0.9)]


@icon("origami-cup", CAT, "Folded paper cup shaped like a trapezoid with a folded down triangular flap on the front",
      tags=["origami cup", "paper cup", "paper folding", "folded cup", "drinking cup", "traditional origami"])
def _(S):
    return [shell(_pl([(4, 5), (20, 5), (17, 20), (7, 20)], S)), detail(poly([(4.8, 5.5), (12, 13), (19.2, 5.5)]))]


@icon("origami-cat", CAT, "Folded paper cat face with a wide head, two triangular ears and a flat creased chin",
      tags=["origami cat", "paper cat", "paper folding", "folded paper", "cat face", "animal origami"])
def _(S):
    head = [(3.5, 3), (9, 6.5), (15, 6.5), (20.5, 3), (20.5, 17), (14, 21), (10, 21), (3.5, 17)]
    return [shell(_pl(head, S)), dot(8.2, 12, 1), dot(15.8, 12, 1), mark(poly([(10.8, 14.6), (13.2, 14.6), (12, 16.2)], closed=True)),
            detail(seg(12, 16.5, 12, 21))]


@icon("origami-dog", CAT, "Folded paper dog face with a pointed head, two drooping folded ears and a small nose tip",
      tags=["origami dog", "paper dog", "paper folding", "folded paper", "puppy face", "animal origami"])
def _(S):
    head = poly([(6.5, 4), (17.5, 4), (17.5, 13), (12, 21.5), (6.5, 13)], closed=True)
    el = poly([(6.5, 4), (2.5, 6.5), (2.5, 15), (6.5, 12)], closed=True)
    er = poly([(17.5, 4), (21.5, 6.5), (21.5, 15), (17.5, 12)], closed=True)
    return [shell(union(head, el, er)), detail(seg(6.5, 4, 6.5, 12.5)), detail(seg(17.5, 4, 17.5, 12.5)),
            dot(9.8, 9.5, 1), dot(14.2, 9.5, 1), mark(circle(12, 18.2, 1.1))]


@icon("origami-penguin", CAT, "Folded paper penguin in front view with a dark back, a pale triangular belly and a pointed head",
      tags=["origami penguin", "paper penguin", "paper folding", "folded paper", "bird origami", "antarctic"])
def _(S):
    body = [(12, 2.5), (16, 7), (19.5, 19), (17, 21.5), (7, 21.5), (4.5, 19), (8, 7)]
    return [shell(_pl(body, S)), detail(poly([(12, 11), (15.5, 19), (8.5, 19)], closed=True)),
            dot(10.4, 6.4, 0.8), dot(13.6, 6.4, 0.8), mark(poly([(11, 8.2), (13, 8.2), (12, 9.8)], closed=True))]


@icon("origami-elephant", CAT, "Faceted paper elephant face with two large ear flaps and a long angular trunk",
      tags=["origami elephant", "paper elephant", "paper folding", "folded paper", "trunk", "animal origami"])
def _(S):
    face = [(12, 3), (15.5, 5.5), (21.5, 4), (21.5, 13), (16.5, 16), (14.5, 21.5), (9.5, 21.5), (7.5, 16), (2.5, 13), (2.5, 4), (8.5, 5.5)]
    return [shell(_pl(face, S, 0.4)), detail(seg(8.5, 5.5, 7.5, 16)), detail(seg(15.5, 5.5, 16.5, 16)),
            dot(10.5, 9.5, 0.9), dot(13.5, 9.5, 0.9)]


@icon("origami-tulip", CAT, "Folded paper tulip with a cup shaped bloom of angled petals on a straight stem with one leaf",
      tags=["origami tulip", "paper tulip", "paper flower", "paper folding", "folded flower", "spring flower"])
def _(S):
    bloom = [(6.5, 4), (9.2, 7.5), (12, 4), (14.8, 7.5), (17.5, 4), (17.5, 10), (12, 13.5), (6.5, 10)]
    return [shell(_pl(bloom, S, 0.4)), detail(seg(9.2, 7.5, 12, 13.2)), detail(seg(14.8, 7.5, 12, 13.2)),
            line(seg(12, 13.5, 12, 21.5)), mark(poly([(12, 20.5), (12, 17), (18, 14), (16.5, 19)], closed=True))]


@icon("origami-fish", CAT, "Angular folded paper fish with a diamond body, a forked tail and a creased fin",
      tags=["origami fish", "paper fish", "paper folding", "folded paper", "sea animal origami", "forked tail"])
def _(S):
    body = [(2.5, 12), (8, 6.5), (14, 7), (16.5, 10.5), (21.5, 6.5), (19.5, 12), (21.5, 17.5), (16.5, 13.5), (14, 17), (8, 17.5)]
    return [shell(_pl(body, S, 0.4)), detail(seg(7.8, 7, 7.8, 17)), detail(seg(11, 9.5, 14.5, 14.5)), dot(5, 11.2, 0.8)]


@icon("origami-paper", CAT, "Square sheet of folding paper with a corner folded over and dashed diagonal crease lines",
      tags=["origami paper", "folding paper", "kami", "paper sheet", "paper folding", "square paper"])
def _(S):
    dashes = [detail(seg(5.2, 18.8, 7.8, 16.2)), detail(seg(10, 14, 12.6, 11.4))]
    return [shell(poly([(3, 3), (15, 3), (21, 9), (21, 21), (3, 21)], closed=True, r=S.r * 0.5)),
            detail(poly([(15, 3), (15, 9), (21, 9)])), *dashes]


@icon("crease-pattern", CAT, "Square with solid and dashed fold lines forming triangles, like an origami diagram",
      tags=["crease pattern", "fold lines", "origami diagram", "mountain valley", "paper folding", "origami design"])
def _(S):
    dashes = [detail(seg(12, 3.5, 12, 7)), detail(seg(12, 17, 12, 20.5))]
    return [shell(poly([(3, 3), (21, 3), (21, 21), (3, 21)], closed=True, r=S.r * 0.6)),
            detail(seg(3, 3, 21, 21)), detail(seg(21, 3, 3, 21)), *dashes,
            detail(seg(3.5, 12, 7, 12)), detail(seg(17, 12, 20.5, 12))]


@icon("delta-kite", CAT, "Wide triangular delta kite flying at an angle with a central spine and a line trailing below",
      tags=["delta kite", "kite flying", "kite", "wind toy", "triangle kite", "sport kite"])
def _(S):
    tri = trot([(12, 2), (20.5, 13), (3.5, 13)], 28, 12, 9)
    spine = trot([(12, 5.5), (12, 13)], 28, 12, 9)
    tail = trot([(12, 13)], 28, 12, 9)[0]
    return [shell(poly(tri, closed=True, r=S.r * 0.6)), detail(seg(*spine[0], *spine[1])),
            line(f"M{fmt(tail[0])} {fmt(tail[1])}C{fmt(tail[0] - 4)} {fmt(tail[1] + 2)} {fmt(tail[0] + 1)} {fmt(tail[1] + 5)} {fmt(tail[0] - 3)} {fmt(tail[1] + 8)}")]
