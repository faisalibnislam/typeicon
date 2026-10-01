"""TypeIcon Core: farm (batch 002): buildings, tractors, harvesters, implements, hand tools, fields, fences."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, polar

CAT = "farm"


def hub(x, y, r, hr=None):
    """Side-view wheel: a ring with a hub dot."""
    return [shell(circle(x, y, r)), dot(x, y, hr if hr else (1.0 if r >= 2.5 else 0.8))]


# ============================================================================ buildings and places

@icon("oast-house", CAT, "Round kiln tower with a conical roof and a tilted cowl on top",
      tags=["oast", "hop kiln", "hops", "kiln", "brewing", "farm building", "kent"])
def _(S):
    return [
        shell(poly([(7, 21), (7, 11), (5, 11), (12, 5), (19, 11), (17, 11), (17, 21)], closed=True, r=S.r * 0.6)),
        detail(seg(7, 11, 17, 11)),
        line(poly([(12, 5), (12, 3.5), (16, 2.5)])),
        detail("M10 21v-3a2 2 0 0 1 4 0v3"),
    ]


@icon("pole-barn", CAT, "Open-sided barn with a gable roof on tall poles sheltering stacked hay bales",
      tags=["hay barn", "open barn", "hay shed", "farm building", "storage", "bales", "shelter"])
def _(S):
    return [
        line(poly([(3, 9), (12, 4), (21, 9)], r=S.r * 0.6)),
        line(seg(5, 9, 5, 21)), line(seg(19, 9, 19, 21)),
        shell(poly([(8, 21), (8, 17), (9.5, 17), (9.5, 13), (14.5, 13), (14.5, 17), (16, 17), (16, 21)], closed=True, r=S.r * 0.4)),
        detail(seg(12, 17, 12, 21)),
    ]


@icon("milking-parlor", CAT, "Cow seen from behind standing in a stall with milking cups under the udder",
      tags=["milking parlour", "dairy", "milking", "cow", "stall", "dairy farm", "udder"])
def _(S):
    return [
        line(seg(3, 3, 3, 21)), line(seg(21, 3, 21, 21)),
        shell(rect(7.5, 4, 9, 9, S.R)),
        line(seg(5.5, 5, 7.5, 6.5)), line(seg(18.5, 5, 16.5, 6.5)),
        detail(seg(12, 6, 12, 11)),
        line("M9.5 13v1.5a2.5 2.5 0 0 0 5 0V13"),
        line(seg(10.5, 17, 10.5, 20)), line(seg(13.5, 17, 13.5, 20)),
    ]


@icon("shepherd-hut", CAT, "Small hut with a curved roof and chimney pipe on iron wheels",
      tags=["shepherds hut", "wagon", "lambing hut", "caravan", "glamping", "cabin on wheels", "rural retreat"])
def _(S):
    return [
        shell("M4 15V12A8 7 0 0 1 20 12V15Z"),
        detail(poly([(10, 15), (10, 11), (14, 11), (14, 15)])),
        line(seg(15.5, 6.5, 15.5, 3.5)),
        *hub(8, 18.5, 2.5), *hub(16, 18.5, 2.5),
    ]


@icon("farm-stand", CAT, "Roadside produce stand with an awning and vegetables on the counter",
      tags=["produce stand", "roadside stand", "farmers market", "market stall", "fresh produce", "vegetable stand", "farm shop"])
def _(S):
    return [
        shell(poly([(3, 7), (5, 3), (19, 3), (21, 7)], closed=True, r=S.r * 0.5)),
        line(seg(5, 7, 5, 21)), line(seg(19, 7, 19, 21)),
        shell(rect(3, 16, 18, 5, S.R * 0.5)),
        shell(circle(9, 13, 2)), shell(circle(15, 13, 2)),
    ]


@icon("biogas-digester", CAT, "Domed tank with a gas pipe and valve and an inlet pipe on one side",
      tags=["biogas", "anaerobic digester", "methane", "manure", "renewable energy", "bioenergy", "gas holder"])
def _(S):
    return [
        shell("M6 21V14A7 7 0 0 1 20 14V21Z"),
        detail(seg(6, 14, 20, 14)),
        line("M13 7V4.5h5"), line(seg(15.5, 3, 15.5, 6)),
        line(poly([(6, 18), (3, 18), (3, 13)])),
    ]


@icon("ranch-gate", CAT, "Two tall posts with a crossbeam overhead and a blank sign hanging below",
      tags=["ranch entrance", "farm entrance", "entry gate", "ranch sign", "western", "homestead", "driveway"])
def _(S):
    return [
        shell(rect(2, 3, 20, 4, S.R * 0.5)),
        line(seg(5, 7, 5, 21)), line(seg(19, 7, 19, 21)),
        line(seg(10, 7, 10, 10)), line(seg(14, 7, 14, 10)),
        shell(rect(8, 10, 8, 5, S.R * 0.5)),
    ]


@icon("weather-vane", CAT, "Rooster on a rod above crossed compass arms",
      tags=["weathercock", "wind direction", "rooster vane", "wind vane", "barn roof", "compass", "weather"])
def _(S):
    return [
        shell(poly([(4, 4.5), (5.5, 2.5), (8, 5.5), (13, 6), (14.5, 3.5), (17, 3), (19.5, 5), (16.5, 6.5), (15.5, 8.5),
                    (13, 10), (8.5, 10), (6, 7.5)], closed=True, r=S.r * 0.7)),
        line(seg(11, 10, 11, 21)),
        line(seg(4, 16, 18, 16)),
        dot(4, 16, 1.25), dot(18, 16, 1.25),
    ]


@icon("vineyard", CAT, "Grape bunch hanging from a wire between two posts above a rolling hill",
      tags=["grapes", "grapevine", "winery", "wine", "viticulture", "wine country", "vines"])
def _(S):
    return [
        line(seg(4, 3, 4, 16)), line(seg(20, 3, 20, 16)),
        line(seg(4, 5, 20, 5)),
        line(seg(12, 5, 12, 7)),
        dot(9.75, 9, 1.15), dot(12, 9, 1.15), dot(14.25, 9, 1.15),
        dot(10.9, 11.5, 1.15), dot(13.1, 11.5, 1.15), dot(12, 14, 1.15),
        line("M2 21Q12 14 22 21"),
    ]


@icon("tea-plantation", CAT, "Rows of rounded tea bushes stepping up a hillside",
      tags=["tea garden", "tea estate", "tea bushes", "camellia sinensis", "tea farm", "terraced rows", "hillside crop"])
def _(S):
    return [
        line("M3 20a3 3 0 0 1 6 0a3 3 0 0 1 6 0a3 3 0 0 1 6 0"),
        line("M6 14a3 3 0 0 1 6 0a3 3 0 0 1 6 0"),
        line("M9 8a3 3 0 0 1 6 0"),
    ]


# ============================================================================ tractors

@icon("crawler-tractor", CAT, "Tractor with a cab running on rubber crawler tracks instead of wheels",
      tags=["track tractor", "tracked tractor", "caterpillar tractor", "crawler", "heavy farm machine", "tracks", "rubber tracks"])
def _(S):
    return [
        shell(poly([(5, 15), (5, 4), (11, 4), (11, 9), (20, 9), (20, 15)], closed=True, r=S.r * 0.6)),
        detail(seg(8, 6.5, 8, 11)),
        line(seg(17, 9, 17, 5)),
        shell(rect(3, 16, 18, 5, 2.5)),
        dot(7.5, 18.5, 0.9), dot(16.5, 18.5, 0.9),
    ]


@icon("vintage-tractor", CAT, "Old open tractor with a large spoked rear wheel, tall exhaust stack and pan seat",
      tags=["antique tractor", "old tractor", "classic tractor", "heritage", "steel wheel tractor", "retro farm", "tractor"])
def _(S):
    return [
        shell(rect(11, 10, 9, 5, S.R * 0.5)),
        line(seg(18, 10, 18, 4)),
        line(seg(5.5, 6, 9.5, 6)), line(seg(7.5, 6, 7.5, 11)),
        shell(circle(8, 16, 5)),
        detail(seg(8, 12, 8, 20)), detail(seg(4, 16, 12, 16)),
        dot(8, 16, 1.5),
        *hub(19, 18.5, 2.5),
    ]


@icon("walking-tractor", CAT, "Two-wheeled walk-behind tractor with an engine, long handlebars and a tiller behind",
      tags=["hand tractor", "power tiller", "walk-behind", "garden tractor", "two-wheel tractor", "rototiller", "small farm"])
def _(S):
    return [
        shell(rect(4, 6, 9, 5, S.R * 0.5)),
        *hub(8.5, 16.5, 4.5, 1.2),
        line(seg(13, 9, 20, 4)), line(seg(20, 4, 22, 5.5)),
        line(seg(13, 16.5, 15.5, 18.5)),
        shell(circle(18, 18.5, 2.5)),
        dot(18, 18.5, 0.8),
    ]


@icon("autonomous-tractor", CAT, "Driverless tractor with no cab and signal waves above its hood",
      tags=["driverless tractor", "self-driving tractor", "robotic tractor", "smart farming", "precision agriculture", "gps tractor", "unmanned"])
def _(S):
    return [
        shell(rect(10, 13, 11, 4, S.R * 0.5)),
        *hub(7.5, 17, 4, 1.1), *hub(18.5, 19, 2.5),
        dot(13, 9.5, 1.15),
        line(arc(13, 9.5, 3.5, -135, -45)),
        line(arc(13, 9.5, 6.75, -135, -45)),
    ]


@icon("combine-harvester", CAT, "Combine harvester from the side with a front header and reel, cab and unloading auger",
      tags=["combine", "grain harvest", "wheat harvest", "harvesting", "reaper", "farm machine", "crop harvest"])
def _(S):
    return [
        line("M2.5 12a3 3 0 0 1 6 0"),
        shell(rect(2, 14, 8, 4, S.R * 0.4)),
        shell(poly([(11, 18), (11, 3), (17, 3), (17, 8), (21, 8), (21, 18)], closed=True, r=S.r * 0.6)),
        detail(seg(13.5, 5.5, 14.5, 5.5)),
        line(seg(19, 8, 19, 5)), line(seg(19, 5, 22, 3)),
        *hub(14.5, 19, 2.5), *hub(19.5, 19.5, 1.8, 0.6),
    ]


@icon("forage-harvester", CAT, "Harvester with a tall curved spout blowing chopped crop into a trailer beside it",
      tags=["silage harvester", "chopper", "forage chopper", "silage", "maize harvest", "corn silage", "self-propelled"])
def _(S):
    return [
        shell(poly([(2, 17), (2, 6), (6, 6), (6, 11), (10, 11), (10, 17)], closed=True, r=S.r * 0.6)),
        line("M8 11V6.5a2.5 2.5 0 0 1 2.5-2.5H15l1.5 3"),
        line(poly([(13, 11), (13, 17), (22, 17), (22, 11)], r=S.r * 0.5)),
        dot(17, 13.5, 1.1), dot(19.75, 15, 1.1),
        *hub(6, 19, 2.5), *hub(18, 19.5, 2, 0.7),
    ]


@icon("cotton-picker", CAT, "Harvester with a boxy mesh basket on top and row units reaching forward at the front",
      tags=["cotton harvester", "cotton harvest", "cotton farming", "picker", "basket", "boll", "crop machine"])
def _(S):
    return [
        shell(rect(5, 3, 13, 7, S.R * 0.5)),
        detail(seg(9.5, 3, 9.5, 10)), detail(seg(13.5, 3, 13.5, 10)),
        shell(rect(3, 11, 14, 7, S.R * 0.5)),
        line(poly([(17, 13.5), (19.5, 13.5), (22, 18)], r=S.r * 0.5)),
        line(poly([(17, 16), (18.5, 16), (20, 19)], r=S.r * 0.3)),
        *hub(7.5, 19.5, 2), *hub(13.5, 19.5, 2),
    ]


@icon("square-baler", CAT, "Baler towed from the side pushing a rectangular bale out of its chute",
      tags=["hay baler", "straw baler", "bale", "hay", "rectangular bale", "baling", "tractor implement"])
def _(S):
    return [
        shell(rect(2, 7, 12, 10, S.R * 0.5)),
        detail(seg(5, 10, 11, 10)),
        shell(rect(15, 12, 7, 6, S.R * 0.4)),
        detail(seg(18.5, 12, 18.5, 18)),
        *hub(8, 19.5, 2, 0.6),
    ]


@icon("round-baler", CAT, "Baler with a rounded chamber and door ejecting a round bale onto the ground",
      tags=["round bale", "hay roll", "big bale", "silage bale", "roll baler", "hay", "straw"])
def _(S):
    return [
        shell(circle(8.5, 9.5, 6.5)),
        detail(arc(8.5, 9.5, 3, 200, 120)),
        shell(circle(18.5, 17.5, 3.5)),
        dot(18.5, 17.5, 0.9),
        *hub(8.5, 19, 2, 0.6),
    ]


@icon("moldboard-plow", CAT, "Plow frame with three curved moldboards in a diagonal row turning soil",
      tags=["plough", "mouldboard plough", "turn soil", "tillage", "ploughing", "tractor implement", "furrow"])
def _(S):
    parts = [line(seg(2, 3, 22, 9))]
    for x, y0, y1 in ((4, 3.6, 10), (10.5, 5.5, 12), (17, 7.5, 14)):
        parts.append(line(seg(x, y0, x, y1)))
        parts.append(shell(poly([(x, y1), (x + 4.5, y1 + 5), (x, y1 + 5)], closed=True, r=S.r * 0.5)))
    return parts


@icon("disc-harrow", CAT, "Two gangs of round discs set at an angle forming a V on a frame",
      tags=["harrow", "disk harrow", "tillage", "soil preparation", "disc gang", "tractor implement", "cultivation"])
def _(S):
    parts = [line(seg(4.5, 3.5, 8.5, 21)), line(seg(19.5, 3.5, 15.5, 21))]
    for t in (0.1, 0.5, 0.9):
        x = 4.5 + 4 * t
        y = 3.5 + 17.5 * t
        for cx in (x, 24 - x):
            if S.name == "line":
                parts.append(shell(poly(regular(cx, y, 2.6, 6, start=0), closed=True)))
            else:
                parts.append(shell(circle(cx, y, 2.25)))
                parts.append(dot(cx, y, 0.8))
    return parts


@icon("field-cultivator", CAT, "Wide toolbar with a row of curved spring tines raking the soil",
      tags=["cultivator", "tine cultivator", "tillage", "soil prep", "spring tines", "seedbed", "tractor implement"])
def _(S):
    parts = [line(seg(2, 6, 22, 6)), line(seg(12, 6, 12, 2.5))]
    for x in (3.5, 8.5, 13.5, 18.5):
        parts.append(line(f"M{fmt(x)} 6V12c0 3 2 5 4.5 6.5"))
    return parts


@icon("seed-drill", CAT, "Long tapered seed hopper with a row of tubes dropping seed into the soil",
      tags=["seeder", "drill", "sowing", "seeding", "planting", "grain drill", "tractor implement"])
def _(S):
    parts = [shell(poly([(3, 3), (21, 3), (19, 10), (5, 10)], closed=True, r=S.r * 0.5))]
    for x in (7, 12, 17):
        parts.append(line(seg(x, 10, x, 15)))
        parts.append(dot(x, 18, 1.25))
    parts.append(line(seg(2, 21, 22, 21)))
    return parts


@icon("row-planter", CAT, "Toolbar with three planter units, each with a small hopper and a wheel",
      tags=["planter", "corn planter", "precision planter", "sowing", "seed", "row crop", "tractor implement"])
def _(S):
    parts = [line(seg(2, 10, 22, 10))]
    for x in (4.5, 12, 19.5):
        parts.append(shell(poly([(x - 2.5, 3), (x + 2.5, 3), (x + 1.5, 7.5), (x - 1.5, 7.5)], closed=True, r=S.r * 0.4)))
        parts.append(line(seg(x, 10, x, 15)))
        parts.append(shell(circle(x, 18.5, 2.5)))
    return parts


@icon("fertilizer-spreader", CAT, "Cone hopper with a spinning disc below throwing granules out in an arc",
      tags=["broadcast spreader", "fertiliser spreader", "granules", "lime spreader", "feeding crops", "tractor implement", "spreading"])
def _(S):
    return [
        shell(poly([(4, 3), (20, 3), (14.5, 12), (9.5, 12)], closed=True, r=S.r * 0.5)),
        line(seg(6.5, 14.5, 17.5, 14.5)),
        dot(4, 17.5, 1.1), dot(8.5, 18.5, 1.1), dot(12, 19, 1.1), dot(15.5, 18.5, 1.1), dot(20, 17.5, 1.1),
        dot(2.75, 13.5, 1.0), dot(21.25, 13.5, 1.0),
    ]


@icon("manure-spreader", CAT, "Box trailer with spiked vertical beater rollers at the back throwing clumps",
      tags=["muck spreader", "dung spreader", "slurry", "compost", "fertilizer", "farmyard manure", "trailer"])
def _(S):
    return [
        shell(rect(2.5, 6, 12, 10, S.R * 0.5)),
        detail(seg(6, 9.5, 11, 9.5)),
        line(seg(17, 5, 17, 15)),
        line(seg(17, 8, 19.5, 8)), line(seg(17, 12, 19.5, 12)),
        dot(21, 5.5, 1.0), dot(21, 16, 1.0),
        *hub(8.5, 19, 2.5, 0.8),
    ]


@icon("crop-sprayer", CAT, "Tank above a long wide boom with nozzles spraying downward",
      tags=["field sprayer", "pesticide", "herbicide", "spray boom", "crop protection", "agrochemical", "spraying"])
def _(S):
    parts = [shell(rect(7, 2.5, 10, 5, 2.5)), line(seg(2, 10, 22, 10))]
    for x in (4, 9.3, 14.7, 20):
        parts.append(line(seg(x, 12.5, x - 1.5, 17.5)))
        parts.append(line(seg(x, 12.5, x + 1.5, 17.5)))
    return parts


@icon("crop-duster", CAT, "Single-engine farm plane with a tall tail releasing a cloud of spray below",
      tags=["agricultural aircraft", "aerial spraying", "crop dusting", "airplane", "biplane", "aerial application", "farm plane"])
def _(S):
    return [
        shell(poly([(3, 5), (7, 8.5), (17, 8.5), (20.5, 10.5), (17, 13), (7, 13), (3, 10)], closed=True, r=S.r * 0.6)),
        line(seg(10.5, 10.5, 13.5, 13.5)),
        line(seg(22, 7.5, 22, 13.5)),
        dot(5, 17, 1.1), dot(9, 18.5, 1.1), dot(13, 17, 1.1), dot(7, 21, 1.1), dot(11, 21, 1.1), dot(15, 19.5, 1.1),
    ]


@icon("spraying-drone", CAT, "Multirotor drone with a tank underneath spraying mist downward in a fan",
      tags=["agricultural drone", "crop drone", "uav", "spray drone", "precision agriculture", "aerial spraying", "quadcopter"])
def _(S):
    return [
        shell(rect(8.5, 7, 7, 4, S.R * 0.5)),
        line(seg(8.5, 8, 5.5, 5.5)), line(seg(15.5, 8, 18.5, 5.5)),
        line(seg(2.5, 4.5, 8, 4.5)), line(seg(16, 4.5, 21.5, 4.5)),
        shell(rect(10, 12.5, 4, 2.5, 1.2)),
        line(seg(10.5, 17.5, 7.5, 21)), line(seg(12, 17.5, 12, 21)), line(seg(13.5, 17.5, 16.5, 21)),
    ]


@icon("hay-rake", CAT, "Two large tine wheels on a frame raking hay into a windrow",
      tags=["windrower", "tedder", "hay making", "haymaking", "rake", "tractor implement", "windrow"])
def _(S):
    parts = [line(seg(7, 7, 17, 12))]
    for cx, cy in ((7, 7), (17, 12)):
        for a in range(0, 360, 60):
            x1, y1 = polar(cx, cy, 1.5, a)
            x2, y2 = polar(cx, cy, 5, a + 35)
            c = polar(cx, cy, 3.6, a)
            parts.append(line(f"M{fmt(x1)} {fmt(y1)}Q{fmt(c[0])} {fmt(c[1])} {fmt(x2)} {fmt(y2)}"))
        parts.append(dot(cx, cy, 1.3))
    parts.append(line("M3 21q9-5 18 0"))
    return parts


def rot(pts, deg, cx, cy):
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * sn, cy + (x - cx) * sn + (y - cy) * c) for x, y in pts]


# ============================================================================ trailers, carts and old machines

@icon("tractor-loader", CAT, "Tractor with front loader arms raising a bucket",
      tags=["front loader", "bucket", "farm loader", "frontloader tractor", "lifting", "muck", "tractor"])
def _(S):
    return [
        shell(poly([(12, 11), (12, 3.5), (20, 3.5), (20, 11)], closed=True, r=S.r * 0.5)),
        detail(seg(14.5, 6, 17.5, 6)),
        shell(rect(5.5, 10, 9, 4.5, S.R * 0.5)),
        line(seg(10, 10, 5.5, 6)),
        line(poly([(3, 3.5), (3, 8.5), (7.5, 8.5)], r=S.r * 0.5)),
        *hub(16.5, 16.5, 5, 1.4), *hub(8, 19, 2.5),
    ]


@icon("farm-trailer", CAT, "Two-wheel tipping trailer with high sides raised at an angle, dumping grain",
      tags=["tipping trailer", "dump trailer", "grain trailer", "tipper", "dumping", "trailer", "agriculture"])
def _(S):
    box = rot([(3, 6), (19, 6), (19, 14), (3, 14)], 18, 19, 14)
    return [
        shell(poly(box, closed=True, r=S.r * 0.4)),
        *hub(15.5, 17.5, 3, 0.9),
        dot(21, 17.5, 0.9), dot(19.5, 20.5, 0.9),
    ]


@icon("slurry-tanker", CAT, "Round tank trailer with a spreader plate spraying a wide fan at the rear",
      tags=["slurry spreader", "liquid manure", "vacuum tanker", "muck spreader", "tank trailer", "fertilizer", "farmyard"])
def _(S):
    return [
        shell(rect(2.5, 5, 14, 9, 4)),
        line(seg(8, 5, 8, 3.5)),
        *hub(9, 18, 3, 0.9),
        line(poly([(16, 10), (19.5, 10), (19.5, 14)])),
        line(seg(17, 14.5, 22, 14.5)),
        line(seg(18.5, 17, 17.5, 21)), line(seg(19.75, 17, 19.75, 21)), line(seg(21, 17, 22, 21)),
    ]


@icon("grain-auger", CAT, "Long inclined tube on wheels with grain pouring from its top end",
      tags=["auger", "grain elevator", "screw conveyor", "grain handling", "silo loading", "bin filler", "grain"])
def _(S):
    pv = (5, 18.5)
    tube = rot([(5, 14), (19, 14), (19, 18.5), (5, 18.5)], -32, *pv)
    sp = lambda x: seg(*rot([(x, 14.5)], -32, *pv)[0], *rot([(x, 18)], -32, *pv)[0])
    return [
        shell(poly(tube, closed=True, r=S.r * 0.4)),
        detail(sp(8)), detail(sp(12)),
        line(seg(12, 13.5, 12, 17.5)),
        *hub(12, 19.5, 2.2, 0.7),
        dot(21, 9.5, 1.0), dot(21, 13.5, 1.0), dot(21, 17.5, 1.0),
    ]


@icon("hay-wagon", CAT, "Flat wagon piled high with square hay bales",
      tags=["bale wagon", "hay bales", "hay cart", "haul", "harvest", "straw", "trailer"])
def _(S):
    return [
        shell(poly([(3, 18), (3, 12), (6, 12), (6, 5), (18, 5), (18, 12), (21, 12), (21, 18)], closed=True, r=S.r * 0.4)),
        detail(seg(6, 12, 18, 12)), detail(seg(9.5, 12, 9.5, 18)), detail(seg(14.5, 12, 14.5, 18)), detail(seg(12, 5, 12, 12)),
        *hub(6.5, 19.5, 2, 0.6), *hub(17.5, 19.5, 2, 0.6),
    ]


@icon("ox-cart", CAT, "Two-wheel wooden cart with a large spoked wheel and a shaft reaching to an ox yoke",
      tags=["bullock cart", "oxcart", "wagon", "rural transport", "animal cart", "traditional farming", "bullock"])
def _(S):
    return [
        shell(poly([(3, 5), (17, 5), (15, 11), (5, 11)], closed=True, r=S.r * 0.5)),
        shell(circle(10, 16, 5)),
        detail(seg(10, 12, 10, 20)), detail(seg(6, 16, 14, 16)),
        dot(10, 16, 1.4),
        line(seg(16, 8, 21.5, 11.5)),
        line(seg(21.5, 8.5, 21.5, 14)),
    ]


@icon("ox-plow", CAT, "Ox pulling a simple wooden plow with a handle held behind",
      tags=["ox plough", "bullock", "oxen", "traditional plowing", "animal traction", "cattle", "heritage farming"])
def _(S):
    return [
        shell(rect(7, 8, 11, 6, S.R * 0.6)),
        shell(poly([(17.5, 8), (21, 10), (21, 14), (17.5, 14)], r=S.r * 0.3, closed=True)),
        line("M18.5 8c-.5-2.5 1-4 3-3.5"),
        line(seg(8.5, 14, 8.5, 19)), line(seg(16, 14, 16, 19)),
        line(seg(7, 11, 4.5, 15.5)),
        line(seg(4.5, 15.5, 2.5, 8)),
        line(seg(2.5, 20.5, 22, 20.5)),
    ]


@icon("threshing-machine", CAT, "Old stationary thresher on wheels with a belt pulley and straw blowing from a chute",
      tags=["thresher", "threshing", "grain separator", "steam era", "harvest", "vintage farm machine", "straw"])
def _(S):
    return [
        shell(circle(5.5, 13.5, 3)),
        detail(seg(5.5, 10.5, 5.5, 16.5)), detail(seg(2.5, 13.5, 8.5, 13.5)),
        shell(rect(9, 8, 11, 8, S.R * 0.5)),
        line(poly([(14, 8), (16, 3.5), (21, 3.5)])),
        dot(20.5, 6.5, 0.9), dot(18.5, 5.5, 0.9),
        *hub(12.5, 19, 2.5, 0.8), *hub(18, 19, 2.5, 0.8),
    ]


@icon("steam-traction-engine", CAT, "Steam traction engine with a tall chimney, a boiler and a huge rear wheel",
      tags=["steam engine", "steam tractor", "traction engine", "steam power", "vintage", "heritage", "showman"])
def _(S):
    return [
        shell(rect(3, 9, 14, 6, S.R * 0.7)),
        line(seg(6, 9, 6, 5)), line(seg(4, 4, 8, 4)),
        line(seg(14, 5, 21, 5)),
        shell(circle(16.5, 15.5, 5)),
        detail(seg(16.5, 11, 16.5, 20)), detail(seg(12, 15.5, 21, 15.5)),
        dot(16.5, 15.5, 1.3),
        *hub(6.5, 18.5, 2.5, 0.8),
    ]


@icon("tractor-tire", CAT, "Large tractor tire seen from the side with deep angled tread lugs",
      tags=["tractor tyre", "wheel", "agricultural tire", "tread", "lugs", "rubber", "farm machinery"])
def _(S):
    parts = [shell(circle(12, 12, 9)), shell(circle(12, 12, 3))]
    for k in range(10):
        a = k * 36
        x1, y1 = polar(12, 12, 5.6, a)
        x2, y2 = polar(12, 12, 8, a + 20)
        parts.append(detail(seg(x1, y1, x2, y2)))
    return parts


@icon("tractor-seat", CAT, "Perforated metal pan seat on a curved spring stem",
      tags=["pan seat", "spring seat", "tractor", "driver seat", "sit", "vintage tractor", "seat"])
def _(S):
    return [
        shell("M3.5 8.5Q12 3 20.5 8.5Q12 13.5 3.5 8.5Z"),
        Part("dot", circle(8.5, 8.2, 0.9)), Part("dot", circle(12, 8.4, 0.9)), Part("dot", circle(15.5, 8.2, 0.9)),
        line(poly([(12, 12), (9.5, 14), (14.5, 16.5), (9.5, 18.5), (12, 20)], r=S.r * 0.5)),
        line(seg(7.5, 21, 16.5, 21)),
    ]


@icon("agricultural-robot", CAT, "Small wheeled field robot with a flat body, a camera on a mast and a weeding arm",
      tags=["farm robot", "weeding robot", "field robot", "agtech", "autonomous", "crop monitoring", "robotics"])
def _(S):
    return [
        shell(rect(9, 3, 6, 4, S.R * 0.5)),
        line(seg(12, 7, 12, 10)),
        shell(rect(4, 10, 16, 5, S.R * 0.5)),
        *hub(7, 18.5, 2.5, 0.8), *hub(17, 18.5, 2.5, 0.8),
        line(seg(12, 15, 12, 21)),
    ]


@icon("threshing-flail", CAT, "Two wooden sticks joined by a short link, the striking swipple hanging at an angle",
      tags=["flail", "thresh by hand", "grain beating", "traditional harvest", "hand threshing", "medieval farm", "swipple"])
def _(S):
    return [
        line(seg(3.5, 21, 14, 8)),
        shell(circle(15.5, 6.3, 1.7)),
        line(seg(17, 8, 21, 18)),
    ]


@icon("winnowing-basket", CAT, "Wide shallow basket tossing grain upward while chaff drifts off to the side",
      tags=["winnowing", "tray", "sifting", "separating chaff", "grain cleaning", "flat basket", "traditional harvest"])
def _(S):
    return [
        shell("M3 14h18l-2.5 4.5a2 2 0 0 1-1.8 1.2H7.3a2 2 0 0 1-1.8-1.2Z"),
        detail(seg(7, 17, 17, 17)),
        dot(8, 7.5, 1.1), dot(12, 5, 1.1), dot(16, 7.5, 1.1), dot(10, 10.5, 1.1), dot(14, 10.5, 1.1),
        line(seg(18.5, 4.5, 22, 3.5)), line(seg(19.5, 8, 22, 7)),
    ]


@icon("millstone", CAT, "Large round grinding stone with radiating grooves and a square hole in the center",
      tags=["grindstone", "mill", "flour mill", "grain grinding", "gristmill", "stone", "milling"])
def _(S):
    parts = [shell(circle(12, 12, 9))]
    for k in range(8):
        a = k * 45 + 22.5
        x1, y1 = polar(12, 12, 5.6, a)
        x2, y2 = polar(12, 12, 8, a)
        parts.append(detail(seg(x1, y1, x2, y2)))
    parts.append(Part("dot", rect(10, 10, 4, 4, 0 if S.name == "line" else 1.2)))
    return parts


# ============================================================================ hand tools, containers and crops

def union_d(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def lens(p, q, w):
    """Pointed leaf shape from p to q with half-width w."""
    (x1, y1), (x2, y2) = p, q
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    ln = math.hypot(dx, dy)
    nx, ny = -dy / ln, dx / ln
    c1 = (mx + nx * w * 2, my + ny * w * 2)
    c2 = (mx - nx * w * 2, my - ny * w * 2)
    return (f"M{fmt(x1)} {fmt(y1)}Q{fmt(c1[0])} {fmt(c1[1])} {fmt(x2)} {fmt(y2)}"
            f"Q{fmt(c2[0])} {fmt(c2[1])} {fmt(x1)} {fmt(y1)}Z")


@icon("orchard-ladder", CAT, "Tall tripod ladder with two rungs-and-rails sides and a single back pole, tapering to the top",
      tags=["fruit picking ladder", "tripod ladder", "three-legged ladder", "harvest", "apple picking", "orchard", "climb"])
def _(S):
    def lx(y):
        return 6 + (21 - y) / 18 * 4.5

    def rx(y):
        return 16 - (21 - y) / 18 * 3.5
    parts = [line(seg(6, 21, 10.5, 3)), line(seg(16, 21, 12.5, 3))]
    for y in (9, 14, 18.5):
        parts.append(line(seg(lx(y), y, rx(y), y)))
    parts.append(line(seg(12, 5, 21, 21)))
    return parts


@icon("bushel-basket", CAT, "Round tapered basket with two bands and two side handles, heaped with apples",
      tags=["apple basket", "harvest basket", "produce basket", "fruit basket", "picking", "orchard", "peck"])
def _(S):
    return [
        shell(poly([(5.5, 12), (18.5, 12), (16.5, 21), (7.5, 21)], closed=True, r=S.r * 0.5)),
        detail(seg(6.5, 15, 17.5, 15)), detail(seg(7, 18.2, 17, 18.2)),
        line(poly([(5.5, 13), (3, 13), (3, 16.5), (6, 16.5)], r=S.r * 0.4)),
        line(poly([(18.5, 13), (21, 13), (21, 16.5), (18, 16.5)], r=S.r * 0.4)),
        line("M7 12C7 7 9.5 5 12 5S17 7 17 12"),
        dot(10, 9.5, 1.1), dot(14, 9, 1.1), dot(12, 7.5, 1.0),
    ]


@icon("grain-scoop", CAT, "Wide deep scoop shovel with raised sides and a D-grip handle, heaped with grain",
      tags=["grain shovel", "scoop shovel", "feed scoop", "silage fork", "barn tool", "hand tool", "granary"])
def _(S):
    def R(pts):
        return rot(pts, 45, 12, 12)
    hd = R([(12, 12), (12, 18)])
    dots = R([(10, 3.5), (14, 3.5), (12, 4.5)])
    return [
        shell(poly(R([(7, 6), (17, 6), (15.5, 12), (8.5, 12)]), closed=True, r=S.r * 0.5)),
        line(seg(*hd[0], *hd[1])),
        shell(poly(R([(9.5, 18), (14.5, 18), (14.5, 21.5), (9.5, 21.5)]), closed=True, r=S.r * 0.6)),
        dot(*dots[0], 0.9), dot(*dots[1], 0.9), dot(*dots[2], 0.9),
    ]


@icon("haystack", CAT, "Tall rounded haystack with a pole sticking out of the top",
      tags=["hay rick", "hayrick", "hay", "straw stack", "hay bale stack", "harvest", "rural"])
def _(S):
    body = "M12 6C8 7 4 12 4 18Q4 20.5 6.5 20.5H17.5Q20 20.5 20 18C20 12 16 7 12 6Z"
    return [
        shell(body),
        line(seg(12, 7, 12, 3)),
        detail("M7.5 16q4.5-2.5 9 0"),
        detail("M9.5 11.5q2.5-1.5 5 0"),
    ]


@icon("shoulder-pole", CAT, "Carrying pole across a person's shoulders with a basket hanging from each end",
      tags=["yoke", "carrying pole", "bamboo pole", "water carrier", "porter", "baskets", "traditional carrying"])
def _(S):
    return [
        shell(circle(12, 6.5, 2.5)),
        shell("M9 21v-5a3 3 0 0 1 6 0v5Z"),
        line(seg(2.5, 12.5, 21.5, 12.5)),
        line(seg(5, 12.5, 5, 16)), line(seg(19, 12.5, 19, 16)),
        shell("M2 16H8A3 3 0 0 1 2 16Z"), shell("M16 16H22A3 3 0 0 1 16 16Z"),
    ]


@icon("egg-tray", CAT, "Square cardboard egg flat with four cups, two of them holding eggs",
      tags=["egg carton", "egg flat", "eggs", "egg box", "poultry", "collecting eggs", "dozen"])
def _(S):
    return [
        shell(ellipse(6.5, 10.3, 1.7, 2.2)), shell(ellipse(12, 10.3, 1.7, 2.2)), shell(ellipse(17.5, 10.3, 1.7, 2.2)),
        shell(poly([(2.5, 13), (21.5, 13), (19.5, 20.5), (4.5, 20.5)], closed=True, r=S.r * 0.5)),
        detail(seg(9.25, 14.5, 9.25, 19)), detail(seg(14.75, 14.5, 14.75, 19)),
    ]


@icon("calf-bottle", CAT, "Large bottle with measurement marks, a long rubber teat and a hanging handle",
      tags=["feeding bottle", "calf milk", "lamb feeding", "teat", "newborn calf", "dairy", "milk bottle"])
def _(S):
    return [
        shell(poly([(11, 7.5), (11, 4.5), (12, 3), (13, 4.5), (13, 7.5)], closed=True, r=S.r * 0.4)),
        shell(poly([(9, 10), (15, 10), (17, 13), (17, 20), (7, 20), (7, 13)], closed=True, r=S.r * 0.6)),
        shell(rect(8.5, 7.5, 7, 2.5, 1)),
        detail(seg(9.5, 14, 13, 14)), detail(seg(9.5, 17.5, 13, 17.5)),
    ]


@icon("poultry-drinker", CAT, "Bell-shaped water dome sitting in a shallow ring of water with a handle on top",
      tags=["chicken waterer", "hen drinker", "chick waterer", "water dispenser", "coop", "poultry water", "bell drinker"])
def _(S):
    return [
        line(poly([(10, 7.5), (10, 4), (14, 4), (14, 7.5)], r=S.r * 0.4)),
        shell("M6 16V13a6 5.5 0 0 1 12 0v3Z"),
        shell(rect(3, 17.5, 18, 3.5, 1.75)),
    ]


@icon("horse-collar", CAT, "Padded oval horse collar with metal hames on each side",
      tags=["draft horse", "harness", "hames", "collar", "workhorse", "tack", "plough horse"],
      filled=lambda: D(U(P(ellipse(12, 12, 8.5, 9.5)), ST(ellipse(12, 12, 8.5, 9.5), 2.0, "butt", "miter")),
                       P(ellipse(12, 13, 3.5, 5)), ST(seg(6, 8, 6, 16), 2.0, "butt", "miter"), ST(seg(18, 8, 18, 16), 2.0, "butt", "miter")))
def _(S):
    return [
        shell(ellipse(12, 12, 8.5, 9.5)),
        shell(ellipse(12, 13, 3.5, 5)),
        detail(seg(6, 8, 6, 16)), detail(seg(18, 8, 18, 16)),
    ]


@icon("fleece", CAT, "Shorn sheep fleece laid flat, a cloud-like outline with curly wool marks",
      tags=["wool", "sheep wool", "shearing", "raw wool", "lamb", "fibre", "sheep"])
def _(S):
    body = union_d(circle(7, 14.5, 4), circle(12, 9.5, 4.8), circle(17, 14.5, 4), circle(12, 15, 5))
    return [
        shell(body),
        detail("M9 13.5a1.5 1.5 0 0 1 3 0"),
        detail("M13.5 16.5a1.5 1.5 0 0 1 3 0"),
    ]


@icon("plowed-field", CAT, "Curved parallel furrows running toward a horizon line",
      tags=["ploughed field", "furrows", "tilled soil", "farmland", "cropland", "arable", "field"])
def _(S):
    return [
        line(seg(2, 7, 22, 7)),
        line("M9 9Q6.5 14 3 21"), line("M11.5 9Q10 14 8.5 21"), line("M13.5 9Q14.5 14 16 21"), line("M16 9Q18 14 21 21"),
    ]


@icon("soybean", CAT, "Soybean pod with three bumps beside a leaf made of three leaflets",
      tags=["soy", "soya bean", "edamame", "legume", "pulse", "oilseed crop", "pod"])
def _(S):
    pod = union_d(circle(4.8, 18.5, 2.3), circle(8.3, 15.5, 2.3), circle(11.8, 12.5, 2.3))
    return [
        shell(pod),
        line(seg(17.5, 12.5, 17.5, 18)),
        shell(lens((17.5, 12.5), (17.5, 4), 1.4)),
        shell(lens((17.5, 12.5), (21.5, 7.5), 1.3)),
        shell(lens((17.5, 12.5), (13.5, 7.5), 1.3)),
    ]


@icon("fertilizer-bag", CAT, "Sack of fertilizer with a sprout on its front and granules spilled at the base",
      tags=["fertiliser", "plant food", "nutrients", "soil amendment", "compost bag", "agrochemical", "feed bag"])
def _(S):
    return [
        shell(poly([(6, 3), (18, 3), (19.5, 7), (19.5, 17.5), (4.5, 17.5), (4.5, 7)], closed=True, r=S.r * 0.6)),
        detail(seg(5, 7, 19, 7)),
        detail(poly([(9, 10.5), (12, 13), (15, 10.5)])),
        detail(seg(12, 13, 12, 15.5)),
        dot(4.5, 20.5, 0.9), dot(8.5, 21, 0.9), dot(12, 20.5, 0.9), dot(15.5, 21, 0.9), dot(19.5, 20.5, 0.9),
    ]


@icon("crop-rotation", CAT, "Four circular arrows chasing each other around a central sprout",
      tags=["crop cycle", "rotating crops", "field rotation", "sustainable farming", "soil health", "cycle", "agronomy"])
def _(S):
    parts = []
    r = 8.3
    for k in range(4):
        a0, a1 = k * 90 + 8, k * 90 + 58
        parts.append(line(arc(12, 12, r, a0, a1)))
        px, py = polar(12, 12, r, a1)
        tx, ty = -math.sin(math.radians(a1)), math.cos(math.radians(a1))
        rx_, ry_ = math.cos(math.radians(a1)), math.sin(math.radians(a1))
        tip = (px + tx * 1.6, py + ty * 1.6)
        b1 = (px - tx * 1.8 + rx_ * 2.0, py - ty * 1.8 + ry_ * 2.0)
        b2 = (px - tx * 1.8 - rx_ * 2.0, py - ty * 1.8 - ry_ * 2.0)
        parts.append(line(poly([b1, tip, b2], r=S.r * 0.3)))
    parts.append(line(poly([(9.5, 9.5), (12, 12), (14.5, 9.5)])))
    parts.append(line(seg(12, 12, 12, 15.5)))
    return parts


@icon("cracked-soil", CAT, "Dry ground broken into cracked plates with a drooping sprout above",
      tags=["drought", "dry earth", "parched", "arid", "dry land", "crop failure", "dehydrated soil"])
def _(S):
    return [
        shell(rect(2.5, 12, 19, 9.5, S.R * 0.4)),
        detail(poly([(8, 12), (10, 16), (7.5, 21.5)])),
        detail(poly([(10, 16), (16, 15), (15, 21.5)])),
        detail(poly([(16, 15), (21.5, 13)])),
        line("M12 12V8a3 3 0 0 1 3-3"),
        line("M12 9.5Q9.5 9.5 8.5 11.5"),
    ]


# ============================================================================ fences, gates, people and garden

@icon("diseased-leaf", CAT, "Leaf with a vein and scattered round dark spots of blight",
      tags=["leaf blight", "plant disease", "blight", "leaf spot", "fungus", "crop disease", "sick plant"])
def _(S):
    return [
        shell(lens((4.5, 19.5), (19.5, 4.5), 4.2)),
        detail(seg(7.5, 16.5, 15, 9)),
        line(seg(4.5, 19.5, 2.5, 21.5)),
        dot(13.6, 14, 1.15), dot(9.5, 9.3, 1.15), dot(15.2, 8.2, 0.9),
    ]


@icon("land-parcel", CAT, "Plot of farmland divided into field rectangles with a map pin on one",
      tags=["field plot", "farm plot", "cadastral", "land lot", "acreage", "property", "field map"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 18, S.R * 0.4)),
        detail(seg(8.5, 3, 8.5, 21)), detail(seg(8.5, 14.5, 21.5, 14.5)),
        detail("M15 12.5C12.5 10.3 12 9.3 12 8.3a3 3 0 0 1 6 0c0 1-.5 2-3 4.2Z"),
        dot(15, 8.3, 1.0),
    ]


@icon("wattle-fence", CAT, "Low panel of woven horizontal branches weaving between upright stakes",
      tags=["woven fence", "hurdle", "willow fence", "hazel hurdle", "basketry fence", "garden edging", "rustic"])
def _(S):
    parts = [line(seg(x, 4, x, 21)) for x in (5, 9.7, 14.4, 19.1)]
    for y in (8.5, 13, 17.5):
        parts.append(line(f"M2.5 {fmt(y)}q2.3-2 4.7 0t4.7 0t4.7 0t4.7 0"))
    return parts


@icon("bamboo-fence", CAT, "Fence of tied vertical bamboo poles with nodes and a horizontal binding rail",
      tags=["bamboo screen", "bamboo poles", "garden screen", "privacy fence", "asian garden", "cane fence", "bamboo"])
def _(S):
    parts = []
    for n, x in enumerate((4.5, 9.5, 14.5, 19.5)):
        parts.append(line(seg(x, 3, x, 21)))
        y = 7 if n % 2 == 0 else 17
        parts.append(line(seg(x - 1.75, y, x + 1.75, y)))
    parts.append(line(seg(2, 12, 22, 12)))
    return parts


@icon("dry-stone-wall", CAT, "Low wall of irregular stones fitted without mortar, capped with upright stones",
      tags=["drystone", "stone wall", "field wall", "rock wall", "boundary wall", "cotswold", "rural wall"])
def _(S):
    return [
        shell(rect(2.5, 12.5, 19, 9, S.R * 0.3)),
        detail(poly([(2.5, 17), (9, 17), (9, 21.5)])),
        detail(seg(9, 17, 15.5, 17)),
        detail(poly([(15.5, 17), (15.5, 21.5)])),
        detail(seg(6.5, 12.5, 6.5, 17)), detail(seg(13, 12.5, 13, 17)),
        shell(poly([(3.5, 12.5), (4.5, 7.5), (8, 7), (9, 12.5)], closed=True, r=S.r * 0.6)),
        shell(poly([(10, 12.5), (10.5, 8), (14, 8.5), (15, 12.5)], closed=True, r=S.r * 0.6)),
        shell(poly([(16, 12.5), (16.5, 8), (20, 7.5), (20.5, 12.5)], closed=True, r=S.r * 0.6)),
    ]


@icon("farm-gate", CAT, "Five-bar metal field gate with a diagonal brace, hinged on a post",
      tags=["field gate", "five bar gate", "pasture gate", "paddock gate", "livestock gate", "hinge", "entrance"])
def _(S):
    return [
        line(seg(2.5, 3, 2.5, 21)),
        line(seg(2.5, 7.5, 6, 7.5)), line(seg(2.5, 16.5, 6, 16.5)),
        shell(rect(6, 4, 16, 16, S.R * 0.3)),
        detail(seg(6, 8.6, 22, 8.6)), detail(seg(6, 12, 22, 12)), detail(seg(6, 15.4, 22, 15.4)),
        detail(seg(6, 20, 22, 4)),
    ]


@icon("garden-gate", CAT, "Small wooden gate with an arched top and pickets set between two posts",
      tags=["picket gate", "wicket gate", "cottage gate", "arched gate", "yard gate", "garden entrance", "wooden gate"])
def _(S):
    return [
        line(seg(3, 5, 3, 21)), line(seg(21, 5, 21, 21)),
        dot(3, 3.5, 1.3), dot(21, 3.5, 1.3),
        shell("M6.5 21V11a5.5 5.5 0 0 1 11 0v10Z"),
        detail(seg(9.6, 8, 9.6, 21)), detail(seg(14.4, 8, 14.4, 21)), detail(seg(6.5, 16, 17.5, 16)),
    ]


@icon("stile", CAT, "Wooden step stile over a fence with two steps up and down and a post to hold",
      tags=["fence stile", "footpath", "hiking", "public right of way", "countryside walk", "step over", "rural crossing"])
def _(S):
    return [
        line(seg(2, 6, 22, 6)), line(seg(2, 9, 22, 9)),
        line(seg(12, 4, 12, 12)),
        shell(poly([(5, 21), (5, 16.5), (9, 16.5), (9, 12.5), (15, 12.5), (15, 16.5), (19, 16.5), (19, 21)], closed=True, r=S.r * 0.4)),
    ]


@icon("fence-post", CAT, "Single square wooden post with wire strands stapled to it, driven into the ground",
      tags=["post", "wire fence", "barbed wire", "fencing", "paddock", "livestock fence", "boundary"])
def _(S):
    return [
        shell(rect(9, 3, 6, 18, S.R * 0.3)),
        line(seg(2, 7, 9, 7)), line(seg(15, 7, 22, 7)),
        line(seg(2, 12, 9, 12)), line(seg(15, 12, 22, 12)),
        line(seg(2.5, 18.5, 9, 18.5)), line(seg(15, 18.5, 21.5, 18.5)),
    ]


@icon("gardener", CAT, "Person in a wide sun hat and long apron holding a watering can",
      tags=["gardening", "horticulture", "watering can", "sun hat", "allotment", "plant care", "garden worker"])
def _(S):
    return [
        shell("M5.5 6.3a2.5 2.5 0 0 1 5 0Z"),
        line(seg(2.5, 6.3, 13.5, 6.3)),
        shell(circle(8, 10, 1.9)),
        shell("M4.5 21V16a3.5 3.5 0 0 1 7 0v5Z"),
        line(seg(11, 15.5, 14.5, 16)),
        shell(rect(14.5, 13.5, 5.5, 5, S.R * 0.4)),
        line(seg(20, 14.5, 22, 11.5)),
        dot(21, 18.5, 0.8), dot(19, 21, 0.8),
    ]


@icon("shepherd", CAT, "Person in a long coat holding a tall crook with a sheep beside them",
      tags=["sheep herder", "crook", "flock", "pastoral", "stockman", "shepherd staff", "herding"])
def _(S):
    sheep = union_d(circle(17.5, 16.5, 2.3), circle(20, 15.8, 2.0), circle(19.5, 18.2, 2.0))
    return [
        shell(circle(7.5, 5.5, 2.3)),
        shell(poly([(4, 21), (5.5, 10), (9.5, 10), (11, 21)], closed=True, r=S.r * 0.6)),
        line("M13 21V6a2.5 2.5 0 0 1 5 0v1"),
        shell(sheep),
        line(seg(16.8, 19, 16.8, 21)), line(seg(20.2, 20, 20.2, 21.5)),
    ]


@icon("slow-moving-vehicle-sign", CAT, "Triangular emblem with a bold border and clipped top as mounted on the back of tractors",
      tags=["smv sign", "slow vehicle", "tractor sign", "road safety", "farm vehicle warning", "hazard triangle", "rural road"])
def _(S):
    return [
        shell(poly([(3, 20), (9.5, 6), (14.5, 6), (21, 20)], closed=True, r=S.r * 0.5)),
        detail(poly([(7.3, 17.5), (12, 9.5), (16.7, 17.5)], closed=True)),
    ]


@icon("seed-packet", CAT, "Paper seed envelope with a folded top flap and a flower on its face, seeds beside it",
      tags=["seeds", "seed envelope", "planting", "sowing", "garden seeds", "flower seeds", "gardening"])
def _(S):
    return [
        shell(rect(3.5, 3, 13.5, 18, S.R * 0.3)),
        detail(seg(3.5, 7.5, 17, 7.5)),
        detail(circle(10.25, 12.5, 2.4)), dot(10.25, 12.5, 0.9),
        detail(seg(10.25, 15, 10.25, 19)),
        dot(20.5, 13, 1.0), dot(19.6, 16.6, 1.0), dot(21, 19.8, 1.0),
    ]


@icon("garden-obelisk", CAT, "Tall four-sided pyramid frame of thin slats with a ball finial on top",
      tags=["plant support", "trellis", "climbing frame", "garden structure", "climber support", "tuteur", "garden"])
def _(S):
    return [
        shell(circle(12, 4.5, 1.25)),
        line(seg(6, 21, 10.8, 7)), line(seg(18, 21, 13.2, 7)),
        line(seg(8.4, 14, 15.6, 14)), line(seg(7.2, 17.6, 16.8, 17.6)), line(seg(9.6, 10.5, 14.4, 10.5)),
    ]


@icon("rock-garden", CAT, "Mound of rounded boulders with small tufted plants growing between them",
      tags=["alpine garden", "rockery", "boulders", "stones", "landscaping", "succulents", "garden feature"])
def _(S):
    rocks = union_d(
        poly([(3, 20.5), (3, 16), (6, 12.5), (10.5, 13), (13, 16), (13, 20.5)], closed=True, r=2),
        poly([(12, 20.5), (12.5, 17), (16, 15), (20.5, 16.5), (21, 20.5)], closed=True, r=2),
        poly([(6.5, 13.5), (8, 9.5), (12, 8.5), (14.5, 11.5), (13, 14.5)], closed=True, r=2))
    return [
        shell(rocks),
        line(seg(17.5, 15, 16.8, 11.5)), line(seg(17.5, 15, 18.4, 11.3)), line(seg(17.5, 15, 19.6, 12.3)),
        line(seg(4.5, 12.3, 3.6, 9)), line(seg(4.5, 12.3, 5.3, 8.8)),
    ]


@icon("hedge-shears", CAT, "Manual shears with two long straight blades and two short handles, blades open",
      tags=["hedge clippers", "trimmer", "garden shears", "topiary", "pruning", "hedge cutting", "clippers"])
def _(S):
    return [
        shell(lens((12, 12), (4, 3.5), 1.6)), shell(lens((12, 12), (20, 3.5), 1.6)),
        line(seg(12, 12, 16, 21)), line(seg(12, 12, 8, 21)),
        dot(12, 12, 0.9),
    ]


@icon("nesting-box", CAT, "Row of three open cubby boxes with an egg resting in the middle one",
      tags=["hen nest", "laying box", "chicken coop", "egg laying", "nest box", "henhouse", "poultry house"])
def _(S):
    return [
        shell(rect(2.5, 6, 19, 14, S.R * 0.4)),
        detail(seg(8.8, 6, 8.8, 20)), detail(seg(15.2, 6, 15.2, 20)),
        Part("dot", ellipse(12, 15.3, 1.5, 2)),
    ]


@icon("livestock-scale", CAT, "Platform scale with low side rails and a dial display on a post at one end",
      tags=["animal scale", "weighing", "cattle scale", "weigh platform", "sheep scale", "weight", "farm equipment"])
def _(S):
    return [
        shell(rect(2.5, 15.5, 19, 4.5, S.R * 0.4)),
        line(poly([(5, 15.5), (5, 10), (13, 10), (13, 15.5)], r=S.r * 0.4)),
        line(seg(18, 10, 18, 15.5)),
        shell(circle(18, 6.5, 3)),
        detail(seg(18, 6.5, 19.3, 5.2)),
    ]


@icon("cheese-press", CAT, "Wooden frame with a round cheese mold at the bottom and a long weighted lever pressing on it",
      tags=["cheesemaking", "curd press", "dairy", "farmhouse cheese", "lever press", "cheese mould", "artisan cheese"])
def _(S):
    return [
        line(seg(4, 3, 4, 21)), line(seg(2, 21, 17, 21)),
        shell(rect(7, 14, 7, 6, S.R * 0.3)),
        line(seg(10.5, 10, 10.5, 14)),
        line(seg(4, 10, 21, 10)),
        line(seg(19, 10, 19, 13)),
        shell(rect(17, 13, 4, 4, S.R * 0.3)),
    ]


@icon("disc-mower", CAT, "Mower bar with a row of small round cutting discs lowered to the grass",
      tags=["drum mower", "hay mower", "grass cutting", "mowing", "haymaking", "tractor implement", "cutter bar"])
def _(S):
    parts = [shell(rect(2, 9, 20, 3.5, S.R * 0.3)), line(seg(16, 9, 16, 3.5))]
    for x in (4.5, 10, 15.5, 20.5):
        parts.append(shell(circle(x, 16, 1.75)))
    parts += [line(seg(3, 21.5, 3, 20)), line(seg(12.5, 21.5, 12.5, 20)), line(seg(21, 21.5, 21, 20))]
    return parts
