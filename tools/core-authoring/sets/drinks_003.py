"""TypeIcon Core: drinks (batch drinks_003): bar tools, cocktails, barware and drink vessels.

Glassware and bar gear are drawn in front or side view. Long hand tools (bar spoon, muddler) are drawn
upright and turned 45 degrees clockwise so the handle points to the bottom-left.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, seg, shell, solid  # noqa: F401
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path.parser import parse_path
from geometry import SCALE, D, P, ST, U, fmt, path_to_d, rotation

CAT = "drinks"
TILT = 45


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def tf(d, m):
    pen = SVGPathPen(None, ntos=fmt)
    parse_path(d, TransformPen(pen, m))
    return pen.getCommands()


def rot(d, deg=TILT, cx=12.0, cy=12.0):
    return tf(d, rotation(deg, cx, cy))


def mv(d, dx, dy):
    return tf(d, (1, 0, 0, 1, dx, dy))


def flip(d):
    return tf(d, (-1, 0, 0, 1, 24, 0))


def fit(parts, cx=12.0, cy=12.0):
    regions = []
    for p in parts:
        regions.append(P(p.d) if p.kind in ("shell", "dot", "solid") else ST(p.d, 2.0))
    x0, y0, x1, y1 = U(*regions).bounds
    dx = round((cx - (x0 + x1) / 2 / SCALE) * 2) / 2
    dy = round((cy - (y0 + y1) / 2 / SCALE) * 2) / 2
    if dx == 0 and dy == 0:
        return parts
    return [Part(p.kind, mv(p.d, dx, dy), p.attrs) for p in parts]


def tilt(parts, deg=TILT):
    return fit([Part(p.kind, rot(p.d, deg), p.attrs) for p in parts])


def hole(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


# ============================================================================ cocktails and vessels

@icon("copper-mug", CAT, "Straight-sided copper mug with a side handle and a lime wedge on the rim",
      tags=["moscow mule", "copper cup", "metal mug", "cocktail", "hammered", "lime"])
def _(S):
    body = rect(4.5, 8, 11.5, 12.5, rr(S, 2.5))
    handle = poly([(16, 11), (19.5, 11), (19.5, 16.5), (16, 16.5)], r=L(S, 0, 1.5))
    return [shell(body), line(handle), line("M7.5 8a3 3 0 0 1 6 0"),
            dot(8.5, 13.5, 0.9), dot(12, 16.5, 0.9)]


@icon("julep-cup", CAT, "Metal julep cup with a frosted side, a mound of crushed ice and a mint sprig",
      tags=["mint julep", "frosted cup", "silver cup", "bourbon", "kentucky derby", "crushed ice", "cocktail"])
def _(S):
    cup = poly([(6, 12), (18, 12), (17.5, 21), (6.5, 21)], closed=True, r=S.r)
    mound = "M6.5 12C6 9.5 8 8.5 9.5 9C10.5 7 13.5 7 14.5 9C16 8.5 18 9.5 17.5 12"
    return [shell(cup), line(mound), line("M12 8.5V5.5"),
            shell("M12 5.5C12 3.5 14 2.5 16.5 2.5C16.5 4.5 15 5.5 12 5.5Z"),
            shell("M12 6.5C12 5 10.5 4.2 8 4.2C8 6 9.5 6.5 12 6.5Z"),
            dot(9, 15.5, 1), dot(14, 14.5, 1), dot(12, 19, 1)]


@icon("mojito", CAT, "Tall glass with mint leaves, ice and a straw",
      tags=["cocktail", "mint", "highball", "rum", "lime", "summer drink", "straw"])
def _(S):
    glass = poly([(6, 8), (18, 8), (16.5, 21), (7.5, 21)], closed=True, r=S.r)
    return [shell(glass), line("M14.5 3L12.5 15"),
            shell("M6.5 8C6 5.5 8 4 10.5 4C10.5 6.5 9 8 6.5 8Z"),
            dot(9.5, 13, 1.1), dot(9.5, 17.5, 1.1), dot(13.5, 18, 1.1)]


@icon("bloody-mary", CAT, "Tall tapered glass with a celery stalk and a lemon wedge on the rim",
      tags=["cocktail", "celery", "tomato juice", "brunch", "vodka", "garnish"])
def _(S):
    glass = poly([(5.5, 8), (18.5, 8), (16.5, 21), (7.5, 21)], closed=True, r=S.r)
    return [shell(glass), detail(seg(7, 12.5, 17, 12.5)),
            line("M14.5 13L16.5 3"),
            line("M16.5 3L14.5 1.5M16.5 3L18.5 2")]


@icon("fishbowl-cocktail", CAT, "Large round bowl glass with several straws sticking out",
      tags=["party drink", "sharing cocktail", "big drink", "bowl", "straws", "fishbowl"])
def _(S):
    cx, cy, r = 12, 14, 7.5
    dy = math.sqrt(r * r - 3.5 * 3.5)
    y = cy - dy
    bowl = f"M{fmt(cx - 3.5)} {fmt(y)}A{r} {r} 0 1 0 {fmt(cx + 3.5)} {fmt(y)}Z"
    return [shell(bowl), line("M9.5 2.5L11 14"), line("M14.5 2.5L13 14"),
            detail("M5 14.5q1.75 -1.5 3.5 0t3.5 0t3.5 0t3.5 0")]


@icon("flaming-cocktail", CAT, "Short glass with a flame burning on top of the drink",
      tags=["flambe", "on fire", "flame", "lit drink", "shot", "cocktail", "bar show"])
def _(S):
    glass = poly([(5, 14), (19, 14), (17.5, 21), (6.5, 21)], closed=True, r=S.r)
    flame = "M12 3C12.5 5 15.8 6.3 15.8 8.8A3.8 3.8 0 0 1 8.2 8.8C8.2 7.2 9 6.2 10 5.2C10 6.6 10.6 7.2 11.2 7.2C11.6 5.5 11 4.3 12 3Z"
    return [shell(glass), shell(flame)]


@icon("punch-bowl", CAT, "Wide footed bowl with a ladle resting in it",
      tags=["party", "punch", "fruit punch", "ladle", "serving bowl", "event"])
def _(S):
    bowl = "M3 10H21A9 8 0 0 1 3 10Z"
    return [shell(bowl), line("M12 18V21M8 21H16"), detail("M20 3L15.5 11"), detail(circle(14.5, 13, 2))]


@icon("hip-flask", CAT, "Flat pocket flask with sloped shoulders, a screw cap and a curved band across the body",
      tags=["flask", "pocket flask", "whiskey", "liquor", "spirits", "camping"])
def _(S):
    body = poly([(7, 9), (17, 9), (19.5, 11.5), (19.5, 21), (4.5, 21), (4.5, 11.5)], closed=True, r=L(S, 0, 2))
    return [shell(body), shell(rect(9.5, 3, 5, 6.5, rr(S, 1.5))), detail("M5 15.5Q12 18.5 19 15.5")]


@icon("absinthe-glass", CAT, "Stemmed glass with a slotted spoon across the rim holding a sugar cube",
      tags=["absinthe", "sugar cube", "green fairy", "spirit", "spoon", "louche"])
def _(S):
    bowl = "M6 9H18C18 13.5 15.5 16 12 16C8.5 16 6 13.5 6 9Z"
    return [shell(bowl), line("M12 16V20M8 21H16"), line("M2.5 8.5H21.5"),
            solid(rect(9.5, 3.5, 5, 4, L(S, 0.3, 1.2))), detail(seg(8, 12.5, 16, 12.5))]


@icon("bitters-bottle", CAT, "Small round bottle with a dasher top and a wide paper label",
      tags=["cocktail bitters", "dasher bottle", "bar", "flavoring", "dropper"])
def _(S):
    body = rect(5.5, 9.5, 13, 11.5, L(S, 2.5, 5))
    return [shell(body), shell(rect(10, 5.5, 4, 4)), shell(rect(9, 2.5, 6, 3.5, rr(S, 1))),
            detail(seg(5.5, 13.5, 18.5, 13.5)), detail(seg(5.5, 18, 18.5, 18))]


@icon("bottle-optic", CAT, "Upside-down spirit bottle held in a wall bracket above a measuring chamber",
      tags=["optic", "spirit dispenser", "pub", "bar measure", "shot measure", "liquor"])
def _(S):
    bottle = poly([(7, 2.5), (17, 2.5), (17, 9), (13.5, 11.5), (13.5, 14), (10.5, 14), (10.5, 11.5), (7, 9)],
                  closed=True, r=S.r)
    return [shell(bottle), line("M3 3V12"), line("M3 7.5H7"),
            shell(rect(9, 14, 6, 7.5, rr(S, 1.5))), detail(seg(9, 18, 15, 18))]


@icon("cocktail-shaker", CAT, "Three-piece cocktail shaker with a tapered body, strainer top and small cap",
      tags=["shaker", "bartender", "mixing", "bar tool", "cocktail", "boston shaker"])
def _(S):
    body = poly([(6, 10), (18, 10), (16, 21), (8, 21)], closed=True, r=S.r)
    strainer = poly([(8.5, 10), (10, 6), (14, 6), (15.5, 10)], r=S.r)
    return [shell(body), line(strainer), shell(rect(10, 2.5, 4, 3.5, rr(S, 1))),
            detail(seg(7, 14.5, 17, 14.5))]


@icon("jigger", CAT, "Double-ended hourglass measuring cup with a large and a small cone",
      tags=["bar measure", "shot measure", "cocktail", "bartender", "measuring cup", "ounce"])
def _(S):
    j = poly([(5.5, 3), (18.5, 3), (13, 11.5), (15.5, 21), (8.5, 21), (11, 11.5)], closed=True, r=S.r)
    return [shell(j), detail(seg(8, 7, 16, 7)), detail(seg(9.5, 17, 14.5, 17))]


@icon("bar-spoon", CAT, "Long bar spoon with a twisted stem, an oval bowl and a disc end",
      tags=["cocktail spoon", "stirring", "bartender", "twisted spoon", "mixing", "stirrer"])
def _(S):
    stem = ("M12 9.5V12L13.2 13.2L10.8 15.6L13.2 18L12 19.2" if S.name == "line"
            else "M12 9.5V11.5q1.6 1.2 0 2.4t0 2.4t0 2.4")
    parts = [shell(ellipse(12, 5.8, 2.8, 4)), line(stem), shell(circle(12, 21, 1.5))]
    return tilt(parts)


@icon("muddler", CAT, "Short bar muddler: a tapered wooden baton with ridges around its wide end",
      tags=["cocktail", "crush mint", "bartender", "pestle", "mojito", "bar tool"])
def _(S):
    m = poly([(10, 2), (14, 2), (15.5, 22), (8.5, 22)], closed=True, r=S.r)
    return tilt([shell(m), detail(seg(9, 15.5, 15, 15.5)), detail(seg(8.8, 19, 15.2, 19))])


@icon("cocktail-strainer", CAT, "Round perforated strainer plate with finger rests and a long handle",
      tags=["hawthorne strainer", "bar tool", "bartender", "strain", "cocktail", "perforated"])
def _(S):
    cx, cy, r = 9.5, 14.5, 7
    grip = rot(rect(cx + r - 1, cy - 1.1, 7.5, 2.2, L(S, 0.3, 1.1)), -45, cx, cy)
    return [shell(circle(cx, cy, r)), shell(grip),
            dot(cx, cy, 1), dot(cx - 3.2, cy, 0.9), dot(cx + 3.2, cy, 0.9), dot(cx, cy - 3.2, 0.9), dot(cx, cy + 3.2, 0.9)]


@icon("mixing-glass", CAT, "Wide mixing glass with a pouring lip and a bar spoon standing in it",
      tags=["bar glass", "stirred cocktail", "martini", "bartender", "pitcher", "stirring glass"])
def _(S):
    glass = poly([(4, 7), (18, 7), (16, 21), (6, 21)], closed=True, r=S.r)
    return [shell(glass), line("M15 2L11 15"), shell(circle(15.6, 2.8, 1.6)),
            detail(seg(6, 17.5, 16, 17.5))]


@icon("ice-tongs", CAT, "Crossed scissor-style tongs with inward claws gripping a cube of ice",
      tags=["ice tongs", "bar tool", "ice bucket", "tongs", "pinch", "serving ice"])
def _(S):
    a = poly([(5.5, 2.5), (16.5, 13.5), (16.5, 18)], r=S.r)
    b = poly([(18.5, 2.5), (7.5, 13.5), (7.5, 18)], r=S.r)
    return [line(a), line(b), shell(rect(9.5, 15.5, 5, 5.5, rr(S, 1)))]


@icon("ice-cube", CAT, "Single cube of ice in perspective with a small highlight corner",
      tags=["ice", "frozen", "cold", "cube", "freezer", "chilled", "drink"])
def _(S):
    cube = poly([(4, 8), (8, 4), (20, 4), (20, 16), (16, 20), (4, 20)], closed=True, r=S.r)
    return [shell(cube), detail("M4 8H16V20"), detail(seg(16, 8, 20, 4)), detail("M7.5 16.5V13H11")]


@icon("ice-scoop", CAT, "Deep scoop with a flat front, a rounded bottom, an angled handle and ice on top",
      tags=["ice", "bar tool", "scoop", "bucket", "serving", "ice bin"])
def _(S):
    body = "M3 9H16V14C16 18 13.5 21 9.5 21C5.5 21 3 18.5 3 15Z"
    grip = rot(rect(15, 7.3, 6.5, 2.6, L(S, 0.3, 1.2)), -35, 15, 8.6)
    return [shell(body, stroke_miterlimit="2"), shell(grip), detail(seg(3, 12.5, 16, 12.5)),
            solid(rect(3.5, 3.5, 4, 4, L(S, 0.2, 0.8))), solid(rect(9, 4.5, 4, 3.5, L(S, 0.2, 0.8)))]


@icon("ice-cube-tray", CAT, "Rectangular tray divided into wells with two ice cubes popped out above it",
      tags=["freezer", "ice maker", "ice tray", "silicone tray", "frozen", "cubes"])
def _(S):
    return [shell(rect(2.5, 10, 19, 11, rr(S, 3))), detail(seg(12, 10, 12, 21)), detail(seg(2.5, 15.5, 21.5, 15.5)),
            solid(rect(4.5, 2.5, 4.5, 4.5, L(S, 0.3, 1))), solid(rect(12.5, 3.5, 4.5, 4.5, L(S, 0.3, 1)))]


@icon("pour-spout", CAT, "Speed pourer with a ribbed rubber stopper, a flange and an angled metal spout",
      tags=["speed pourer", "bottle pourer", "bar tool", "liquor pourer", "spirits", "bartender"])
def _(S):
    tube = rot(rect(9.3, 1.5, 3.6, 10.5, L(S, 0.3, 1.5)), 40, 11, 12)
    return [shell(rect(7, 12, 8, 3, rr(S, 1.2))), shell(tube),
            shell(poly([(8, 15), (14, 15), (13, 21.5), (9, 21.5)], closed=True, r=S.r)), detail(seg(8.5, 18.3, 13.5, 18.3))]


@icon("bottle-opener", CAT, "Flat bottle opener with a round head, an oblong opening and a handle",
      tags=["cap remover", "beer", "bar tool", "crown cap", "opener", "kitchen"])
def _(S):
    from geometry import P as _P, U as _U, path_to_d as _d
    body = _d(_U(_P(circle(12, 7.5, 6.5)), _P(rect(9.5, 10, 5, 12, L(S, 0.5, 2.5)))))
    return tilt([shell(body), detail(circle(12, 7.5, 2.2)), dot(12, 18.5, 0.9)])


@icon("cocktail-pick", CAT, "Short cocktail pick skewering two olives, with a bead at the top",
      tags=["olives", "martini", "garnish", "skewer", "toothpick", "appetizer"])
def _(S):
    def olive(cy):
        pts = [(8, cy), (8.8, cy - 2.2), (10.8, cy - 3), (13.2, cy - 3), (15.2, cy - 2.2), (16, cy),
               (15.2, cy + 2.2), (13.2, cy + 3), (10.8, cy + 3), (8.8, cy + 2.2)]
        return solid(poly(pts, closed=True, r=L(S, 0, 1.2)))
    return tilt([line("M12 4V24"), olive(9.5), olive(16.5), shell(poly([(12, 0.5), (14.2, 2.5), (12, 4.5), (9.8, 2.5)], closed=True, r=S.r))])


@icon("cocktail-umbrella", CAT, "Small open paper umbrella with scalloped edge and a thin stick through the centre",
      tags=["drink umbrella", "paper parasol", "tiki", "tropical", "garnish", "summer drink"])
def _(S):
    if S.name == "line":
        canopy = "M4 12A8 8 0 0 1 20 12L16 16L12 12L8 16Z"
    else:
        canopy = "M4 12A8 8 0 0 1 20 12A4 4 0 0 1 12 12A4 4 0 0 1 4 12Z"
    return tilt([shell(canopy), line("M12 2V23"), detail(seg(12, 4, 7.5, 11.5)), detail(seg(12, 4, 16.5, 11.5))], 25)


@icon("drinking-straw", CAT, "Bendy straw with an accordion joint near the top",
      tags=["straw", "bendy straw", "sip", "sipping", "plastic straw", "flexible straw"])
def _(S):
    from geometry import P as _P, U as _U, path_to_d as _d
    low = rect(9.5, 10, 5, 12, L(S, 0, 1.5))
    up = rot(rect(9.5, 1.5, 5, 10, L(S, 0, 1.5)), 35, 12, 10)
    body = _d(_U(_P(low), _P(up)))
    return fit([shell(body), detail(seg(9.5, 13, 14.5, 13)), detail(seg(9.5, 16.5, 14.5, 16.5))])


@icon("swizzle-stick", CAT, "Thin drink stirrer with a disc ornament on top and crossed spokes near the tip",
      tags=["stirrer", "drink stirrer", "cocktail stick", "bar", "stir stick", "muddle"])
def _(S):
    return tilt([shell(circle(12, 4.5, 3)), line("M12 7.5V21.5"), line("M9 16.5H15"), line("M9.5 19.5H14.5")])


@icon("drink-coaster", CAT, "Round coaster seen at an angle with a ring left by a glass",
      tags=["beer mat", "table protector", "bar", "glass ring", "mat", "drinkware"])
def _(S):
    stain = circle(12, 9.5, 0.1)
    out = [shell("M3 9.5A9 5 0 0 1 21 9.5A9 5 0 0 1 3 9.5Z"),
           line(f"M3 9.5V{L(S, 12.5, 13.5)}A9 5 0 0 0 21 {L(S, 12.5, 13.5)}V9.5")]
    if S.name == "line":
        out.append(detail("M7.5 9.5A4.5 2 0 0 1 16.5 9.5A4.5 2 0 0 1 7.5 9.5Z"))
    else:
        out.append(detail("M7.5 9.5A4.5 2 0 0 1 16.5 9.5"))
    return out


@icon("drinks-tray", CAT, "Round serving tray held up on one open hand with a tumbler and a wine glass on it",
      tags=["waiter", "server", "waitress", "serving tray", "hospitality", "restaurant", "glasses"])
def _(S):
    return [line("M2.5 13.5H21.5"), shell(rect(4.5, 4.5, 5, 8, rr(S, 1))),
            shell("M13.5 3.5H19.5C19.5 7.5 18 9.5 16.5 9.5C15 9.5 13.5 7.5 13.5 3.5Z"), line("M16.5 9.5V12.5"),
            shell(rect(8.5, 16.5, 7, 5, rr(S, 2.5)))]


@icon("bar-cart", CAT, "Two-tier wheeled cart with a bottle and cup on top and glasses below",
      tags=["drinks trolley", "home bar", "serving cart", "liquor cart", "cocktail hour", "trolley"])
def _(S):
    def bottle(cx, top):
        return solid(poly([(cx - 0.8, top), (cx + 0.8, top), (cx + 0.8, top + 2), (cx + 2, top + 3.2), (cx + 2, 8),
                           (cx - 2, 8), (cx - 2, top + 3.2), (cx - 0.8, top + 2)], closed=True))
    return [line("M3.5 9H18.5"), line("M3.5 16H18.5"), line("M5 9V18.5"), line("M17.5 9V3.5H21.5"),
            dot(5, 20.5, 1.6), dot(17.5, 20.5, 1.6), bottle(7.5, 3), solid(poly([(11.5, 5), (15.5, 5), (14.5, 8), (12.5, 8)], closed=True)),
            solid(poly([(6, 12), (9.5, 12), (9, 15), (6.5, 15)], closed=True)), solid(poly([(12, 12), (15.5, 12), (15, 15), (12.5, 15)], closed=True))]


@icon("bar-counter", CAT, "Bar counter with a shelf of bottles behind it and two stools in front",
      tags=["pub", "tavern", "lounge", "bar stool", "nightlife", "counter"])
def _(S):
    def bottle(cx, top):
        return solid(poly([(cx - 0.8, top), (cx + 0.8, top), (cx + 0.8, top + 2), (cx + 2, top + 3.2), (cx + 2, 8),
                           (cx - 2, 8), (cx - 2, top + 3.2), (cx - 0.8, top + 2)], closed=True))
    return [line("M3.5 8.5H20.5"), bottle(6.5, 2.5), bottle(12, 3.5), bottle(17.5, 2.5),
            line("M2.5 13.5H21.5"), line("M4.5 18H9.5"), line("M7 18V21.5"), line("M14.5 18H19.5"), line("M17 18V21.5"),
            line("M5.5 21.5H8.5"), line("M15.5 21.5H18.5")]


# ============================================================================ pots, jugs and containers

def _union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


@icon("bottle-stopper", CAT, "Tapered cork stopper with a domed metal top",
      tags=["cork", "wine stopper", "bottle cap", "seal", "plug", "reusable stopper"])
def _(S):
    dome = "M5.5 12.5A6.5 6.5 0 0 1 18.5 12.5Z"
    body = poly([(8, 12.5), (16, 12.5), (14.5, 21.5), (9.5, 21.5)], closed=True, r=S.r)
    return [shell(dome), shell(body), detail(seg(9, 17, 15, 17))]


@icon("cloth-coffee-filter", CAT, "Cone-shaped cloth filter on a wire ring with a long handle and a drip below",
      tags=["sock filter", "cloth filter", "coffee sock", "brewing", "tea strainer", "drip"])
def _(S):
    return [shell(ellipse(10.5, 5.5, 5.5, 2.2)), line(poly([(5.2, 6.5), (10.5, 17), (15.8, 6.5)], r=S.r)),
            line("M16 5.5H22"), dot(10.5, 20.5, 1.3)]


@icon("airpot", CAT, "Tall thermal pot with a wide push-button pump on top and a spout at the front",
      tags=["pump pot", "coffee dispenser", "thermal carafe", "hot beverage", "catering", "insulated pot"])
def _(S):
    return [shell(rect(5.5, 2.5, 11, 3.5, rr(S, 1.5))), line("M11 6V8.5"),
            shell(rect(6, 8.5, 10, 13, rr(S, 2.5))), line(poly([(16, 12), (20, 12), (20, 9)], r=S.r)),
            detail(seg(6, 13, 16, 13))]


@icon("teapot-warmer", CAT, "Teapot sitting on a round stand with a small tealight flame underneath",
      tags=["tealight", "keep warm", "candle warmer", "tea", "stand", "flame"])
def _(S):
    flame = "M11 16.5C12 17.5 13.4 18.4 13.4 19.8A2.4 2.4 0 0 1 8.6 19.8C8.6 18.4 10 17.5 11 16.5Z"
    return [shell(rect(5.5, 4, 10, 8, rr(S, 4))), dot(10.5, 2.3, 1.1), line(poly([(15.5, 7.5), (18.5, 7.5), (21, 4.5)], r=S.r)),
            line(poly([(5.5, 6), (3, 6), (3, 10), (5.5, 10)], r=S.r)),
            line("M4 14.5H18"), line("M5.5 14.5V21.5"), line("M16.5 14.5V21.5"), shell(flame)]


@icon("thermo-pot", CAT, "Electric hot water pot with a push button on the lid, a short spout and a handle",
      tags=["electric kettle", "water boiler", "hot water dispenser", "airpot", "instant hot water", "kettle"])
def _(S):
    return [shell(rect(4.5, 8, 13, 13.5, rr(S, 3))), shell(rect(6, 5, 10, 3.5, rr(S, 1))), solid(rect(9, 2, 4, 3.2)),
            line(poly([(17.5, 11), (21, 11), (21, 17.5), (17.5, 17.5)], r=S.r)), line("M4.5 10.5L2 8.5"),
            detail(seg(8, 14, 14, 14))]


@icon("hydration-bladder", CAT, "Soft water reservoir bag with a long drinking hose ending in a bite valve",
      tags=["water bladder", "hydration pack", "hiking", "cycling", "drinking tube"])
def _(S):
    return [shell(rect(3.5, 6.5, 11, 15, rr(S, 3.5))), shell(rect(7, 3, 4, 3.5, rr(S, 1))),
            line("M11 4.2H16Q20.5 4.2 20.5 9V15.5"), solid(rect(19, 15.5, 3, 4.5)),
            detail(seg(3.5, 11.5, 14.5, 11.5))]


@icon("milk-jug", CAT, "Plastic gallon jug with a built-in handle, a small screw cap and a label",
      tags=["gallon", "dairy", "milk carton", "plastic jug", "water jug", "container"])
def _(S):
    body = poly([(4.5, 21.5), (4.5, 10.5), (8.5, 6.5), (19.5, 6.5), (19.5, 21.5)], closed=True, r=S.r)
    return [shell(body), shell(rect(5.5, 2.5, 4.5, 4, rr(S, 1))), detail(rect(13.5, 9.5, 3.5, 4, rr(S, 1.2))),
            detail(seg(4.5, 17, 19.5, 17))]


@icon("hydrometer", CAT, "Weighted glass float with a thin stem floating inside a tall test cylinder",
      tags=["brewing", "specific gravity", "wine making", "beer making", "measurement", "test jar"])
def _(S):
    return [shell(rect(5.5, 2.5, 13, 19, rr(S, 2.5))), line("M12 6V13"), shell(circle(12, 16.5, 2.5)),
            detail(seg(5.5, 9, 9.5, 9)), detail(seg(14.5, 9, 18.5, 9))]


@icon("tastevin", CAT, "Shallow round tasting cup with dimples in its side and a ring handle",
      tags=["wine tasting", "sommelier", "tasting cup", "wine cup", "silver cup", "burgundy"])
def _(S):
    cup = poly([(3, 9), (17, 9), (15.5, 15), (12.5, 18.5), (7.5, 18.5), (4.5, 15)], closed=True, r=L(S, 0, 3.5))
    return [shell(cup), shell(circle(20, 9.5, 2.3)), dot(7.5, 13, 1), dot(12.5, 13, 1), dot(10, 16, 0.9)]


@icon("citrus-twist", CAT, "Spiral curl of citrus peel with a short straight end",
      tags=["lemon twist", "orange peel", "garnish", "zest", "curl", "cocktail garnish"])
def _(S):
    d = ("M3 20.5H8C15 20.5 20.5 15.5 20.5 10.5C20.5 6 17 3.5 13.5 3.5C10 3.5 7.5 6 7.5 9C7.5 11.5 9.5 13 11.5 13"
         + ("C13.5 13 14.5 11.5 14.5 10.3" if S.name == "line" else ""))
    return [line(d)]


@icon("stemware-rack", CAT, "Overhead rail with two wine glasses hanging upside down by their stems",
      tags=["wine glass rack", "glass holder", "bar", "hanging glasses", "stemware", "storage"])
def _(S):
    bowl = lambda x: f"M{x - 3.5} 20.5C{x - 3.5} 16.5 {x - 2} 13 {x} 13C{x + 2} 13 {x + 3.5} 16.5 {x + 3.5} 20.5Z"
    return [line("M2.5 3.5H21.5"), line("M7 3.5V13"), line("M17 3.5V13"), shell(bowl(7)), shell(bowl(17))]


@icon("stacked-cups", CAT, "Stack of nested disposable cups with lips showing at each level",
      tags=["paper cups", "plastic cups", "party cups", "disposable", "stack", "takeaway"])
def _(S):
    body = poly([(7.5, 21), (16.5, 21), (19, 4), (5, 4)], closed=True, r=S.r)
    return fit([Part(p.kind, rot(p.d, 8), p.attrs) for p in
                [shell(body), line("M3.8 9H20.2"), line("M4.4 14H19.6")]])


@icon("carved-wooden-cup", CAT, "Rounded carved wooden cup with a thick handle lump with a hole through it",
      tags=["kuksa", "wood cup", "camping cup", "handmade", "nordic", "drinking cup"])
def _(S):
    cup = "M3 7.5H15.5V12C15.5 16.5 13 19.5 9.25 19.5C5.5 19.5 3 16.5 3 12Z"
    lump = rect(14.5, 9, 6.5, 7, L(S, 2, 3.2))
    return [shell(_union(cup, lump)), detail("M3 12.5H15.5"), dot(18.25, 12.5, 1.3)]


@icon("mason-jar-mug", CAT, "Screw-top glass jar with a side handle and a straw through the lid",
      tags=["jar cup", "smoothie jar", "iced coffee", "drinking jar", "canning jar", "lid"])
def _(S):
    return [shell(rect(4.5, 8, 11.5, 13.5, rr(S, 3))), shell(rect(4, 4.5, 12.5, 4, rr(S, 1.2))),
            line("M14 1.5L12 15"), line(poly([(16, 11.5), (19.5, 11.5), (19.5, 17), (16, 17)], r=S.r))]


@icon("ice-machine", CAT, "Boxy ice maker with a power light on top and a bin door showing cubes of ice",
      tags=["ice maker", "ice dispenser", "freezer", "restaurant", "hotel", "commercial"])
def _(S):
    return [shell(rect(3, 2.5, 18, 19, rr(S, 2.5))), dot(17, 5.5, 1.1), detail(seg(6, 5.5, 12, 5.5)),
            detail(rect(6.5, 9.5, 11, 9, rr(S, 1))),
            solid(rect(8.5, 13.5, 3.2, 3.2)), solid(rect(12.6, 13.5, 3.2, 3.2))]


@icon("kegerator", CAT, "Small fridge with a tap tower, spout and tap handle mounted on top",
      tags=["beer tap", "draft beer", "keg fridge", "home bar", "beer dispenser", "tap tower"])
def _(S):
    return [shell(rect(4, 11.5, 16, 10, rr(S, 2.5))), shell(rect(9.5, 6.5, 5, 5, rr(S, 1))), line("M12 6.5V3.5"),
            solid(rect(10.5, 1.5, 3, 3.5)), line("M9.5 9H7V11"), detail(seg(16, 14.5, 16, 19))]


@icon("pulled-tea", CAT, "Two cups with tea poured in a long arc from a high cup into a low one",
      tags=["pouring tea", "tea pulling", "teh tarik", "pull tea", "stream", "beverage"])
def _(S):
    low = "M3.5 16H12.5C12.5 19.5 10.5 21.5 8 21.5C5.5 21.5 3.5 19.5 3.5 16Z"
    high = mv(rot("M13 3.5H21C21 8.5 19 11 17 11C15 11 13 8.5 13 3.5Z", -45, 17, 7.5), -0.5, 1.5)
    return [shell(low), shell(high), line("M13 8.5C10.5 10.5 8 11.5 8 14")]


@icon("absinthe-fountain", CAT, "Glass water globe on a stand with taps dripping into glasses below",
      tags=["absinthe", "water dispenser", "drip", "glass globe", "spirit service", "drip fountain"])
def _(S):
    glass = lambda x: solid(poly([(x - 3, 19), (x + 3, 19), (x + 2.4, 22), (x - 2.4, 22)], closed=True))
    return [shell(circle(12, 6, 4.2)), line("M12 10.2V13"), line("M4 13H20"), line("M6 13V15.3"), line("M18 13V15.3"),
            dot(6, 17.3, 0.9), dot(18, 17.3, 0.9), glass(6), glass(18)]


@icon("gourd-bottle", CAT, "Double-bulb gourd bottle with a stopper and a cord tied at the waist",
      tags=["calabash", "water gourd", "wine gourd", "hulu", "traditional bottle", "flask"])
def _(S):
    from dsl import regular
    top = poly(regular(12, 8.2, 3.7, 12), closed=True, r=S.r)
    bot = poly(regular(12, 16, 6.3, 12), closed=True, r=S.r)
    return [shell(_union(top, bot)), solid(rect(10.5, 1.5, 3, 3)), detail(seg(9.3, 12.2, 14.7, 12.2)), line("M14.5 12.2L17.5 14.5")]


@icon("water-sachet", CAT, "Pillow-shaped plastic water bag with a torn corner, crimped ends and a drip",
      tags=["pure water", "sachet water", "water pouch", "plastic bag", "drinking water", "pouch"])
def _(S):
    bag = poly([(3.5, 7.5), (15, 7.5), (16, 10), (18, 8.5), (20.5, 11), (20.5, 18.5), (3.5, 18.5)], closed=True, r=L(S, 0, 1.4))
    return [shell(bag), detail(seg(7, 11.5, 7, 15)), dot(13, 14, 1.3)]


@icon("bagged-drink", CAT, "Clear plastic bag of iced drink tied with a ruffled top and a straw",
      tags=["bubble tea bag", "takeaway drink", "iced drink", "plastic bag drink", "street drink", "juice bag"])
def _(S):
    body = poly([(7.5, 10), (16.5, 10), (19, 21), (5, 21)], closed=True, r=L(S, 0, 2.5))
    return [shell(body), line(poly([(8, 7.5), (10, 10), (12, 7.5), (14, 10), (16, 7.5)], r=S.r * 0.5)),
            line("M17.5 2L13.5 15"), dot(9.5, 15.5, 1.1), dot(14.5, 18, 1.1)]


@icon("beverage-trolley", CAT, "Tall service trolley with two drawers, a pot and a cup on top and small wheels",
      tags=["service cart", "hospitality", "tea trolley", "coffee cart", "hotel", "catering"])
def _(S):
    pot = solid("M5.5 8.2V5.2Q5.5 4 6.7 4H10.8Q12 4 12 5.2V8.2Z")
    return [shell(rect(5, 9, 14, 10.5, L(S, 0.5, 3))), detail(seg(5, 14.2, 19, 14.2)), dot(12, 11.6, 0.9), dot(12, 16.9, 0.9),
            dot(7, 21, 1.2), dot(17, 21, 1.2), pot, solid(poly([(12, 5.2), (14.5, 3.5), (14.5, 5), (12, 7)], closed=True)),
            solid(poly([(15.5, 4.5), (19.5, 4.5), (18.8, 8.2), (16.2, 8.2)], closed=True))]


@icon("pull-tab", CAT, "Flat can pull tab with a round finger ring and a rivet hole",
      tags=["can tab", "soda can", "ring pull", "beverage can", "aluminum", "opener"])
def _(S):
    body = _union(circle(8.5, 12, 7), rect(11, 8.5, 11, 7, L(S, 1, 3.5)))
    return tilt([shell(body), detail(circle(8.5, 12, 3.2)), dot(17.5, 12, 1.2)], -30)


@icon("pouring-drink", CAT, "Bottle tilted down pouring a stream into a glass",
      tags=["pour", "serve", "bartender", "refill", "pouring", "bottle and glass"])
def _(S):
    b = poly([(3, 14.5), (3, 7), (5, 5), (5, 1.5), (7, 1.5), (7, 5), (9, 7), (9, 14.5)], closed=True, r=S.r)
    return [shell(mv(rot(b, 125, 6, 8), 2.5, 1.5)), line("M13.5 15V18.5"),
            shell(poly([(11.5, 16.5), (20.5, 16.5), (19.5, 21.5), (12.5, 21.5)], closed=True, r=S.r))]


@icon("spilled-drink", CAT, "Glass tipped on its side with liquid running out and pooling on the table",
      tags=["spill", "accident", "knocked over", "mess", "tipped glass", "liquid"])
def _(S):
    glass = poly([(13, 3.5), (3, 5.5), (3, 11.5), (13, 13.5)], r=S.r)
    puddle = "M9 19C9 17.5 12 17 14.5 17.5C17 16.5 21 17.5 21 19.8C21 21.8 17 21.8 14.5 21.8C11 21.8 9 21 9 19Z"
    return [line(glass), line("M13 11.5Q15.5 12 15.5 15.5"), shell(puddle)]


