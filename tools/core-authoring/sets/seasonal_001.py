"""TypeIcon Core: seasonal (batch 001), winter gear and chores, autumn harvest, spring."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d

CAT = "seasonal"


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def sq(x, y, w, h, rx=0.0) -> Part:
    return Part("dot", rect(x, y, w, h, rx))


def tri(a, b, c) -> Part:
    return Part("dot", poly([a, b, c], closed=True))


def rot(pts, deg=45, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * sn, cy + (x - cx) * sn + (y - cy) * c) for x, y in pts]


def rrect(x, y, w, h, r=0.0, deg=45):
    return poly(rot([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], deg), closed=True, r=r)


def rseg(x1, y1, x2, y2, deg=45):
    (a, b), (c, d) = rot([(x1, y1), (x2, y2)], deg)
    return seg(a, b, c, d)


# =========================================================================== chunk 1

@icon("snowboard-binding", CAT, "Side view of a snowboard binding with a highback and ankle strap on a base plate",
      tags=["snowboard", "binding", "winter sports", "highback", "strap", "board", "gear"])
def _(S):
    return [shell(rect(3, 16, 18, 3, S.R if S.name == "line" else 1.5)),
            shell(poly([(4, 16), (6, 3), (11, 3), (10, 16)], closed=True, r=S.r)),
            line("M12 16C12 8 19 8 19 16"),
            line("M2 22H22")]


@icon("ice-cleats", CAT, "Boot sole with a rubber harness and metal spikes underneath",
      tags=["traction", "spikes", "ice grips", "winter", "boot", "walking", "slip"])
def _(S):
    return [shell(rect(3, 11, 18, 5, S.R if S.name == "line" else 2.5)),
            line("M8 11C8 6 16 6 16 11"),
            solid(poly([(5, 16), (8, 16), (6.5, 20)], closed=True)),
            solid(poly([(10.5, 16), (13.5, 16), (12, 20)], closed=True)),
            solid(poly([(16, 16), (19, 16), (17.5, 20)], closed=True))]


@icon("puffer-vest", CAT, "Sleeveless quilted vest with puffy bands and a centre zip",
      tags=["vest", "gilet", "quilted", "padded", "winter", "clothing", "warm"])
def _(S):
    return [shell(poly([(9, 3), (15, 3), (18, 4), (18, 8), (19.5, 12), (19.5, 21), (4.5, 21), (4.5, 12), (6, 8), (6, 4)],
                       closed=True, r=S.r)),
            detail("M12 5V21"), detail("M5 11H11"), detail("M13 11H19"), detail("M5 16H11"), detail("M13 16H19")]


@icon("neck-gaiter", CAT, "Soft fabric tube worn around the neck with a fold line",
      tags=["neck warmer", "buff", "scarf", "face cover", "winter", "cold", "fleece"])
def _(S):
    if S.name == "line":
        body = "M5 5.5C9 6.5 15 6.5 19 5.5C16 9 16 14 17.5 19C14 20 10 20 6.5 19C8 14 8 9 5 5.5Z"
    else:
        body = "M5 6C5 4.5 19 4.5 19 6C16 9 16 14 17.5 18C17.5 20 6.5 20 6.5 18C8 14 8 9 5 6Z"
    return [shell(body),
            detail("M5.5 6.5C8 8.5 16 8.5 18.5 6.5"), detail("M7.5 14C10.5 16 13.5 16 16.5 14")]


@icon("car-snow-brush", CAT, "Snow brush with an ice scraper blade on the other end of the handle",
      tags=["snow brush", "ice scraper", "windshield", "car", "winter", "frost", "clean"])
def _(S):
    r = 0 if S.name == "line" else 1.5
    return [shell(rrect(7, 3, 10, 5, r)),
            detail(rseg(10.5, 3, 10.5, 8)), detail(rseg(13.5, 3, 13.5, 8)),
            line(rseg(12, 8, 12, 16)),
            shell(rrect(8, 16, 8, 4.5, r))]


@icon("snow-pusher", CAT, "Wide shovel blade on a long handle pushing a heap of snow",
      tags=["snow shovel", "plow", "push shovel", "driveway", "winter", "clear snow", "chores"])
def _(S):
    return [shell("M2 20C2 14 6 13 9 14.5L9 20Z"),
            shell(rect(10.5, 11, 4, 9, S.R if S.name == "line" else 2)),
            line("M14 13L20 3"),
            line("M2 22H22")]


@icon("driveway-snow-stake", CAT, "Tall reflective marker pole standing in a snowbank",
      tags=["snow pole", "marker", "reflector", "driveway", "winter", "plow", "stake"])
def _(S):
    body = union(rect(10, 2, 4, 14), "M3 21C3 15 8 14 12 14C16 14 21 15 21 21Z")
    return [shell(body), detail("M10 6H14"), detail("M10 10H14")]


@icon("snow-fort", CAT, "Wall of stacked snow blocks with battlements and a small flag",
      tags=["fort", "snow wall", "snowball fight", "winter", "kids", "play", "blocks"])
def _(S):
    body = union(rect(3, 12, 18, 9), rect(3, 9, 4, 4), rect(10, 9, 4, 4), rect(17, 9, 4, 4))
    return [shell(body), detail("M3 16.5H21"), detail("M8 12V16.5"), detail("M16 12V16.5"), detail("M12 16.5V21"),
            line("M19 9V3"), tri((19, 3), (19, 6.5), (15.5, 4.75))]


@icon("skate-guards", CAT, "Ice skate boot with a hard guard covering the blade",
      tags=["skate", "blade guards", "ice skating", "soakers", "winter", "protect", "hockey"])
def _(S):
    return [shell(poly([(6, 2), (12, 2), (12, 7), (20, 9.5), (20, 12), (6, 12)], closed=True, r=S.r)),
            shell(rect(3, 16, 18, 5, S.R if S.name == "line" else 2.5)),
            dot(8, 18.5, 1), dot(16, 18.5, 1)]


@icon("windshield-snow-cover", CAT, "Fabric sheet over a car windshield marked with a snowflake",
      tags=["windshield cover", "frost cover", "car", "winter", "snow", "protect", "ice"])
def _(S):
    return [shell(poly([(6, 3), (18, 3), (22, 16), (2, 16)], closed=True, r=S.r)),
            line("M4.5 16V21"), line("M19.5 16V21"),
            line("M12 5V12"), line("M8.9 6.6L15.1 10.4"), line("M15.1 6.6L8.9 10.4")]


@icon("ice-stock", CAT, "Curling-style stock with a tall handle sliding along an ice line",
      tags=["ice stock", "eisstock", "curling", "winter sport", "slide", "bavarian", "puck"])
def _(S):
    return [shell(rect(5, 13, 14, 5, S.R if S.name == "line" else 2.5)),
            line("M8.5 13C8.5 4 15.5 4 15.5 13"),
            line("M3 21H21")]


@icon("skibob", CAT, "Bicycle-like frame with a seat and handlebar riding on two short skis",
      tags=["ski bike", "snow bike", "winter sport", "snow", "ride", "mountain", "skis"])
def _(S):
    return [line("M2.5 20H10"), line("M14 20H21.5"),
            line("M7 20L9.5 11"), line("M18 20L15.5 7"), line("M9.5 11H15.5"),
            line("M13 6H18"), sq(6.5, 8.5, 5, 2)]


@icon("steering-snow-sled", CAT, "Low sled with a small steering wheel on skis",
      tags=["sled", "steering sled", "snow", "kids", "winter", "toboggan", "ride"])
def _(S):
    return [shell(rect(3, 12, 18, 5, S.R if S.name == "line" else 2.5)),
            line("M7 17V20"), line("M17 17V20"), line("M2.5 20.5H21.5"),
            shell(circle(16, 6, 3)), line("M16 9V12")]


@icon("inflatable-snow-sled", CAT, "Puffy air-pillow sled with chambers and carry handles",
      tags=["snow tube", "inflatable sled", "air sled", "winter", "kids", "slide", "snow"])
def _(S):
    return [shell(rect(5, 6, 14, 12, S.R if S.name == "line" else 4)),
            detail("M9.5 6V18"), detail("M14.5 6V18"),
            line(poly([(5, 9), (2.5, 9), (2.5, 15), (5, 15)], r=S.r)),
            line(poly([(19, 9), (21.5, 9), (21.5, 15), (19, 15)], r=S.r))]


@icon("ice-lantern", CAT, "Block of ice shaped like a bucket with a candle flame glowing inside",
      tags=["ice candle", "luminary", "lantern", "winter", "candle", "glow", "decoration"])
def _(S):
    return [shell(poly([(5, 5), (19, 5), (17, 20), (7, 20)], closed=True, r=S.r)),
            detail("M12 9C14.5 12 15 13 15 14.5A3 3 0 0 1 9 14.5C9 13 9.5 12 12 9Z")]


# =========================================================================== chunk 2

@icon("hot-toddy", CAT, "Mug of hot drink with a cinnamon stick and rising steam",
      tags=["hot drink", "toddy", "mug", "cinnamon", "winter", "warm", "cider", "steam"])
def _(S):
    return [shell(rect(4, 10, 12, 11, S.R if S.name == "line" else 4)),
            line("M16 12H18A3 3 0 0 1 18 18H16"),
            line("M14.5 3L11.5 12"),
            line("M7 2C6 3.5 8 5 7 6.5")]


@icon("mukluks", CAT, "Tall soft winter boot with a fur cuff and a dangling pompom tie",
      tags=["winter boot", "fur boot", "arctic", "snow boot", "footwear", "pompom", "warm"])
def _(S):
    body = union(rect(5, 2, 9, 5, S.R if S.name == "line" else 2),
                 poly([(6, 6), (13, 6), (13, 14), (20, 16.5), (20, 21), (6, 21)], closed=True, r=S.r))
    return [shell(body), detail("M5 7H14"), detail("M9.5 7V11"), dot(9.5, 12.5, 1.5)]


@icon("ice-spud", CAT, "Heavy bar with a chisel blade breaking a hole in the ice with chips flying",
      tags=["ice chisel", "ice fishing", "spud bar", "hole", "frozen lake", "winter", "tool"])
def _(S):
    return [line("M12 2V13"),
            shell(poly([(9.5, 13), (14.5, 13), (13, 19), (11, 19)], closed=True, r=S.r)),
            line("M2 21H7"), line("M17 21H22"),
            dot(6.5, 14, 1.1), dot(17.5, 14, 1.1), dot(20, 9.5, 1.1), dot(4, 9.5, 1.1)]


@icon("ice-road", CAT, "Straight road across a frozen lake with marker poles and cracks",
      tags=["ice road", "frozen lake", "winter road", "route", "travel", "arctic", "highway"])
def _(S):
    return [shell(poly([(10, 4), (14, 4), (21, 20), (3, 20)], closed=True, r=S.r)),
            detail("M12 7V9"), detail("M12 12V15"),
            line("M2.5 8L5 10L3.5 12.5"), line("M21.5 8L19 10L20.5 12.5")]


@icon("ice-hotel", CAT, "Domed building built from ice blocks with an arched entrance",
      tags=["ice hotel", "igloo", "ice building", "winter", "lodging", "arctic", "blocks"])
def _(S):
    return [shell("M2 21V14C2 8 7 4 12 4C17 4 22 8 22 14V21Z"),
            detail("M9 21V17A3 3 0 0 1 15 17V21"),
            detail("M3 12H8"), detail("M16 12H21"), detail("M12 4V9")]


@icon("ski-chalet", CAT, "Steep-roofed mountain cabin with a window, balcony rail and door",
      tags=["chalet", "a-frame", "cabin", "ski lodge", "mountain", "winter", "holiday"])
def _(S):
    return [shell(poly([(3, 21), (3, 14), (12, 3), (21, 14), (21, 21)], closed=True, r=S.r)),
            detail("M3 14.5H21"), detail("M10.5 21V17.5H13.5V21"), dot(12, 9.5, 1.3)]


@icon("snowboard-halfpipe", CAT, "U-shaped snow halfpipe with a rider jumping above it",
      tags=["halfpipe", "snowboard", "freestyle", "winter sports", "jump", "trick", "snow park"])
def _(S):
    return [line("M3 10C3 17 7 20 12 20C17 20 21 17 21 10"),
            dot(12, 3.8, 1.6), line("M12 6.5V10"), line("M9 5.5L12 7.5L15 5.5"),
            line("M9.5 13H14.5")]


@icon("fireplace-screen", CAT, "Three-panel folding mesh screen with an arched centre panel",
      tags=["fireplace", "fire screen", "hearth", "mesh", "winter", "cozy", "spark guard"])
def _(S):
    body = union(poly([(2.5, 20), (2.5, 11), (8, 9), (8, 21)], closed=True),
                 poly([(16, 9), (21.5, 11), (21.5, 20), (16, 21)], closed=True),
                 "M8 21V9C8 4 16 4 16 9V21Z")
    return [shell(body), detail("M8 9V21"), detail("M16 9V21"), detail("M12 6.5V21"), detail("M8 14.5H16")]


# =========================================================================== chunk 3

@icon("winter-car-kit", CAT, "Duffel bag marked with a snowflake for winter car emergencies",
      tags=["emergency kit", "winter", "car", "roadside", "snowflake", "bag", "survival"])
def _(S):
    return [shell(rect(3, 10, 18, 11, S.R if S.name == "line" else 4)),
            line("M8 10C8 4 16 4 16 10"),
            detail("M12 12.5V18.5"), detail("M9.4 14L14.6 17"), detail("M14.6 14L9.4 17")]


@icon("snow-scoop", CAT, "Deep box-shaped scoop shovel with a long handle and a grip",
      tags=["snow shovel", "scoop", "shovel", "driveway", "winter", "chores", "clear snow"])
def _(S):
    return [shell(poly([(2, 13), (12, 13), (15, 20), (5, 20)], closed=True, r=S.r)),
            line("M3 13C4 9 9 9 11 13"),
            line("M12 14L19 5"), line("M17 3.5H21.5")]


@icon("heated-jacket", CAT, "Zipped jacket with a battery pack at the hip and wavy heat lines on the chest",
      tags=["heated clothing", "battery", "warm", "winter", "coat", "heating", "jacket"])
def _(S):
    return [shell(poly([(9, 3), (15, 3), (21, 8), (21, 18), (17, 18), (17, 21), (7, 21), (7, 18), (3, 18), (3, 8)],
                       closed=True, r=S.r)),
            detail("M12 4V21"), Part("dot", poly([(9.5, 7), (6.5, 12.5), (8.8, 12.5), (8, 16.5), (11, 10.5), (8.8, 10.5)], closed=True)),
            sq(13.8, 14, 2.4, 2.4)]


@icon("rolling-snowball", CAT, "Figure leaning forward pushing a large snowball along the ground",
      tags=["snowball", "snowman", "winter", "play", "push", "kids", "snow"])
def _(S):
    return [shell(circle(16.5, 15, 5)),
            dot(5, 6.5, 1.8), line("M6 9L8 15L6 20"), line("M8 15L10.5 20"), line("M6.5 11.5L11 13"),
            line("M2 21.5H8")]


@icon("sidewalk-ice-chopper", CAT, "Long handle with a flat steel blade for chopping ice off paving",
      tags=["ice chopper", "ice breaker", "sidewalk", "winter", "tool", "scraper", "chisel"])
def _(S):
    r = 0 if S.name == "line" else 1
    return [line(rseg(12, 2, 12, 16, 30)), shell(rrect(7, 16, 10, 4, r, 30)),
            dot(4.5, 17, 1.1), dot(6, 12.5, 1.1), dot(19.5, 19, 1.1)]


@icon("yard-waste-bag", CAT, "Tall paper lawn bag with a folded top and leaves poking out",
      tags=["leaf bag", "yard waste", "garden waste", "autumn", "compost", "raking", "paper bag"])
def _(S):
    return [shell(poly([(6, 8), (18, 8), (19, 21), (5, 21)], closed=True, r=S.r)),
            detail("M6 12H18"),
            solid("M9 8C6.5 6 7.5 3 10.5 2.5C11.5 5 11 6.5 9 8Z"),
            solid("M14 8C12.5 5.5 14 3 17 3C17.5 5.5 16.5 7 14 8Z")]


@icon("cider-press", CAT, "Slatted basket press with a central screw, crank handle and juice spout",
      tags=["cider", "press", "apple", "juice", "autumn", "harvest", "crank"])
def _(S):
    return [line("M3 3H21"), line("M4 3V21"), line("M20 3V21"),
            line("M12 3V10"), line("M8.5 6.5H15.5"),
            shell(rect(7, 10, 10, 8, S.R if S.name == "line" else 2)),
            detail("M10.5 10V18"), detail("M13.5 10V18")]


@icon("pumpkin-spice-latte", CAT, "Takeaway coffee cup with a lid and a pumpkin on its sleeve",
      tags=["latte", "coffee", "pumpkin", "autumn", "fall", "takeaway", "spice"])
def _(S):
    return [shell(poly([(6, 8), (18, 8), (16.5, 21), (7.5, 21)], closed=True, r=S.r)),
            shell(rect(5, 5, 14, 3, S.R if S.name == "line" else 1.5)),
            detail("M6.8 12H17.2"), detail("M7.2 18H16.8"),
            Part("dot", ellipse(12, 15, 2.4, 1.7)),
            line("M13 5L15 2")]


@icon("storm-window", CAT, "Window frame with an extra outer pane and wind blowing against it",
      tags=["storm window", "window", "insulation", "wind", "winter", "weatherproof", "draft"])
def _(S):
    return [shell(rect(8, 3, 14, 18, S.R if S.name == "line" else 3)),
            detail("M15 3V21"), detail("M8 12H22"),
            line("M2 8H5.5"), line("M2 13H5.5"), line("M2 18H5.5")]


@icon("furnace-filter", CAT, "Flat pleated air filter panel in a frame",
      tags=["air filter", "furnace", "hvac", "pleated", "home maintenance", "heating", "airflow"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R if S.name == "line" else 3)),
            detail("M8 3V21"), detail("M12 3V21"), detail("M16 3V21")]

# =========================================================================== chunk 4

def scallop(cx, cy, r, n, rs):
    return union(circle(cx, cy, r), *[circle(*polar_pt(cx, cy, r, i * 360 / n), rs) for i in range(n)])


def polar_pt(cx, cy, r, deg):
    a = math.radians(deg)
    return (cx + r * math.cos(a), cy + r * math.sin(a))


@icon("pecan-pie", CAT, "Round pie with a fluted crust and pecan halves on top",
      tags=["pecan", "pie", "dessert", "thanksgiving", "autumn", "baking", "nuts"])
def _(S):
    body = scallop(12, 12, 8, 12, 1.6) if S.name == "line" else scallop(12, 12, 8.2, 10, 1.9)
    pecans = [Part("dot", circle(*polar_pt(12, 12, 3.6, a), 1.1)) for a in (90, 162, 234, 306, 18)]
    return [shell(body), *pecans, dot(12, 12, 1.1)]


@icon("geese-v-formation", CAT, "Flock of birds flying in a V formation",
      tags=["geese", "birds", "migration", "autumn", "flying", "flock", "formation", "sky"])
def _(S):
    def bird(x, y):
        return line(f"M{fmt(x - 2.5)} {fmt(y + 0.5)}Q{fmt(x - 1.2)} {fmt(y - 1.5)} {fmt(x)} {fmt(y + 0.5)}"
                    f"Q{fmt(x + 1.2)} {fmt(y - 1.5)} {fmt(x + 2.5)} {fmt(y + 0.5)}")
    return [bird(12, 4), bird(8, 9), bird(16, 9), bird(4.5, 14), bird(19.5, 14)]


@icon("apple-crate", CAT, "Slatted wooden crate with a handhold, filled with apples",
      tags=["apples", "crate", "harvest", "orchard", "autumn", "box", "fruit"])
def _(S):
    body = union(rect(3, 11, 18, 10, S.R if S.name == "line" else 2),
                 circle(7, 8.5, 3.2), circle(12, 7.5, 3.2), circle(17, 8.5, 3.2))
    return [shell(body), detail("M3 15.5H21"), Part("dot", rect(9.5, 17.2, 5, 1.6, 0.8))]


@icon("wool-socks", CAT, "Thick knitted sock with a ribbed cuff and bands",
      tags=["socks", "wool", "knit", "winter", "warm", "clothing", "cozy"])
def _(S):
    d = ("M5 3H13V12C13 14 14 15 16 15.5C19 16 20.5 17.5 20.5 19.5C20.5 20.5 20 21 19 21H8C6 21 5 20 5 18Z"
         if S.name == "rounded" else "M5 3H13V12L18 15.5L20.5 17.5V21H5Z")
    return [shell(d), detail("M5 6.5H13"), detail("M5 10H13"), detail("M9 3V6.5")]


@icon("trench-coat", CAT, "Long belted double-breasted coat with wide lapels",
      tags=["coat", "raincoat", "overcoat", "belt", "clothing", "autumn", "fashion"])
def _(S):
    return [shell(poly([(9, 3), (12, 6.5), (15, 3), (20, 6), (21, 21), (3, 21), (4, 6)], closed=True, r=S.r)),
            detail("M9 4L12 10.5L15 4"), detail("M3.8 14H20.2"),
            dot(9.5, 18, 1), dot(14.5, 18, 1)]


@icon("flint-corn", CAT, "Ear of dried corn with husks peeled back and mottled kernels",
      tags=["corn", "maize", "indian corn", "harvest", "autumn", "kernels", "husk", "thanksgiving"])
def _(S):
    return [shell(ellipse(12, 8.5, 4, 6.5)),
            *[dot(x, y, 0.9) for x in (10.5, 13.5) for y in (5, 8, 11)],
            shell("M12 21C7 21 4 16 4.5 11C8 12.5 10.5 15 12 21Z"),
            shell("M12 21C17 21 20 16 19.5 11C16 12.5 13.5 15 12 21Z")]


@icon("canning-jar", CAT, "Preserving jar with a lid and band, filled with fruit pieces",
      tags=["mason jar", "preserves", "canning", "jam", "pickling", "autumn", "pantry", "harvest"])
def _(S):
    body = union(rect(6, 8, 12, 13, S.R if S.name == "line" else 4), rect(7, 6, 10, 4))
    return [shell(body), shell(rect(7, 2.5, 10, 3, 1 if S.name == "line" else 1.5)),
            detail("M7 9.5H17"), dot(10, 14.5, 1.5), dot(14, 13.5, 1.5), dot(12, 18, 1.5)]


@icon("storm-door", CAT, "Exterior door with a full glass panel and a closer bar",
      tags=["door", "storm door", "glass door", "entry", "home", "winter", "weatherproof"])
def _(S):
    return [shell(rect(5, 2, 14, 20, S.R if S.name == "line" else 3)),
            detail("M8 4.5H16"), detail(rect(8, 8, 8, 8, 0)), dot(16.3, 19.2, 0.9)]


@icon("baked-apple", CAT, "Baked apple in a dish, stuffed with oats and raisins",
      tags=["apple", "baked", "dessert", "autumn", "oats", "cinnamon", "fall recipe"])
def _(S):
    return [shell("M12 9C9 7 5 9 6 12.5C6.5 15.5 9 16.5 12 15.5C15 16.5 17.5 15.5 18 12.5C19 9 15 7 12 9Z"),
            line("M12 8.5C12 7 12.5 6 13.5 5"),
            line("M17 5C16 3.5 18 2.5 17 1.5") if False else line("M18.5 6.5C17.5 5 19.5 4 18.5 2.5"),
            line("M5.5 6.5C4.5 5 6.5 4 5.5 2.5"),
            shell("M3 17.5H21C21 20.5 18 22 12 22C6 22 3 20.5 3 17.5Z")]


@icon("baby-chick", CAT, "Small round chick with a beak and thin legs",
      tags=["chick", "easter", "spring", "bird", "baby", "chicken", "hatch"])
def _(S):
    return [shell(circle(12, 11, 6.5)), dot(10, 9, 1.1),
            solid(poly([(5.8, 10), (2, 11.5), (5.8, 13)], closed=True)),
            line("M10 17.5V21"), line("M14 17.5V21"),
            line("M12 4.5V2.5") if S.name == "line" else line("M12 4.5C12 3.5 13 3 13.5 2.5")]


@icon("spring-lamb", CAT, "Young woolly lamb standing on thin legs",
      tags=["lamb", "sheep", "spring", "easter", "farm", "baby animal", "wool"])
def _(S):
    body = union(circle(11, 10.5, 4.5), circle(16, 10.5, 4.5), circle(13.5, 13.5, 4.5), ellipse(5, 11.5, 2.3, 3))
    return [shell(body), dot(4.5, 10.5, 0.9),
            line("M11 17.5V21"), line("M17 17.5V21")]


# =========================================================================== chunk 5

@icon("kettle-corn", CAT, "Round kettle pot with popped corn heaped above the rim and a paddle",
      tags=["popcorn", "kettle", "fair food", "snack", "autumn", "carnival", "stirring"])
def _(S):
    pot = "M3 13H21C21 18.5 17 21.5 12 21.5C7 21.5 3 18.5 3 13Z"
    corn = union(circle(8, 10.5, 3), circle(12.5, 9, 3), circle(16.5, 10.5, 3), rect(5, 10, 14, 3))
    return [shell(union(pot, corn)), detail("M3.5 13.5H20.5"), line("M20 3L14 11")]


@icon("maple-sap-bucket", CAT, "Tree trunk with a metal spout and a lidded bucket hanging from it",
      tags=["maple", "syrup", "sap", "tapping", "bucket", "spring", "sugaring", "tree"])
def _(S):
    bucket = union(poly([(11.5, 10), (20.5, 10), (19.5, 20), (12.5, 20)], closed=True), rect(10.5, 8, 11, 2.5))
    return [shell(rect(2, 2, 6, 20, S.R if S.name == "line" else 2)),
            line("M8 10H11"), shell(bucket),
            line("M13.5 8C13.5 3.5 18.5 3.5 18.5 8"), detail("M5 6V9"), detail("M5 14V17")]


@icon("sap-evaporator", CAT, "Long pan over a firebox with flames, rising steam and a chimney",
      tags=["maple syrup", "evaporator", "boiling sap", "sugarhouse", "steam", "spring", "fire"])
def _(S):
    body = union(rect(2, 12, 17, 9), rect(1.5, 10, 18, 3), rect(19, 3, 3, 18))
    return [shell(body),
            detail("M10.5 19.5C8 18 8.5 16 10.5 14.5C11 16 13 16.5 12.5 19.5Z"),
            line("M6 7.5C5 6 7 5 6 3.5"), line("M12 7.5C11 6 13 5 12 3.5")]


@icon("gardening-gloves", CAT, "Cuffed work glove with spread fingers and a leaf mark",
      tags=["garden", "work gloves", "spring", "planting", "hands", "protection", "yard work"])
def _(S):
    body = union(rect(6, 9, 12, 8, 1 if S.name == "line" else 3),
                 rect(6, 3, 3, 7, 1.5), rect(9, 2, 3, 8, 1.5), rect(12, 3, 3, 7, 1.5), rect(15, 4, 3, 6, 1.5),
                 poly([(2.5, 12), (5.5, 10.5), (7.5, 15), (4.5, 16)], closed=True))
    return [shell(body), shell(rect(6, 17.5, 12, 3.5, 1 if S.name == "line" else 1.5)),
            detail("M9 4V9"), detail("M12 4V9"), detail("M15 5V9"),
            dot(12, 13.2, 1.1)]


@icon("seed-bomb", CAT, "Lumpy ball of clay and soil with seeds and a small sprout on top",
      tags=["seed ball", "seed bomb", "guerrilla gardening", "spring", "wildflower", "planting", "sprout"])
def _(S):
    return [shell(circle(12, 15, 6.5) if S.name == "rounded" else poly(regular(12, 15, 7, 8, -67.5), closed=True)), dot(10, 14, 1), dot(14.5, 13.5, 1), dot(12, 18, 1),
            line("M12 8.5V5.5"),
            shell("M12 6C9.5 6.5 8 5 7.5 3C10 2.5 11.8 3.5 12 6Z"),
            shell("M12 6C14.5 6.5 16 5 16.5 3C14 2.5 12.2 3.5 12 6Z")]


@icon("spring-cleaning", CAT, "Cleaning bucket with a handle and sparkles",
      tags=["cleaning", "spring", "bucket", "chores", "tidy", "household", "sparkle", "fresh"])
def _(S):
    def star(cx, cy, r):
        k = r * 0.28
        return solid(poly([(cx, cy - r), (cx + k, cy - k), (cx + r, cy), (cx + k, cy + k), (cx, cy + r), (cx - k, cy + k),
                           (cx - r, cy), (cx - k, cy - k)], closed=True))
    return [shell(poly([(4, 11), (20, 11), (17.5, 21), (6.5, 21)], closed=True, r=S.r)),
            line("M7 11C7 6 17 6 17 11"),
            star(19, 4.5, 3), star(4.5, 5, 2.2), detail("M5.5 15H18.5")]


@icon("sakura-mochi", CAT, "Oval rice cake wrapped in a cherry leaf with a small blossom on top",
      tags=["mochi", "sakura", "cherry blossom", "wagashi", "japanese sweet", "spring", "rice cake"])
def _(S):
    return [shell(ellipse(12, 13, 9.5, 6.5)),
            detail("M12 13.5V19"), detail("M12 16L8 13.5"), detail("M12 16L16 13.5"),
            *[dot(*polar_pt(12, 9.3, 1.9, a), 1.0) for a in (90, 162, 234, 306, 18)]]