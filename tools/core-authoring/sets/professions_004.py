"""TypeIcon Core: professions and roles (batch professions_004).

Creative, science, teaching, faith, historic and everyday-role figures. Each icon is a head-and-shoulders
figure (head r 3, shoulders 9 wide) on the left or centre with one identifying prop, hat or garment mark.
Small solid marks use `dot`/`mark` parts so they are knocked out of the Filled shell.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import I, P, U, fmt, path_to_d, polar  # noqa: F401

CAT = "professions"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def u(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def clip(a, b):
    return path_to_d(I(P(a), P(b)))


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def bust_d(S, cx, top, hw, bottom=21.0):
    r = min(hw - L(S, 2.0, 1.0), bottom - top)
    x0, x1 = cx - hw, cx + hw
    return (f"M{fmt(x0)} {fmt(bottom)}V{fmt(top + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x0 + r)} {fmt(top)}"
            f"H{fmt(x1 - r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(top + r)}V{fmt(bottom)}")


def person(S, cx=12.0, hy=9.0, hr=3.0, top=15.0, hw=4.5, bottom=21.0):
    return [shell(circle(cx, hy, hr)), shell(bust_d(S, cx, top, hw, bottom))]


def lp(S, cx=7.0, hy=9.0):
    """Person on the left, leaving the right side free for a prop."""
    return person(S, cx, hy, 3.0, hy + 6.0, 4.5)


def cp(S, hy=10.0):
    return person(S, 12, hy, 3.0, hy + 6.0, 6.5)


def dome(cx, y, w, h):
    return f"M{fmt(cx - w)} {fmt(y)}A{fmt(w)} {fmt(h)} 0 0 1 {fmt(cx + w)} {fmt(y)}Z"


def star4(cx, cy, r=2.4):
    """Solid four-point sparkle."""
    k = r * 0.3
    return solid(poly([(cx, cy - r), (cx + k, cy - k), (cx + r, cy), (cx + k, cy + k), (cx, cy + r),
                       (cx - k, cy + k), (cx - r, cy), (cx - k, cy - k)], closed=True))


def head(cx, hy, top, hat):
    """Hat shell plus the face below it (no circle strokes inside the hat). `top` is the hat's lower edge."""
    return [shell(hat), shell(clip(circle(cx, hy, 3.0), rect(cx - 3.5, top - 0.4, 7, 8)))]


def cloud(x, y, w):
    """Flat-bottomed cloud with its bottom-left at (x, y+4), width w (>= 8)."""
    b = y + 4
    return (f"M{fmt(x + 2)} {fmt(b)}A2 2 0 0 1 {fmt(x + 2)} {fmt(b - 4)}A3 3 0 0 1 {fmt(x + w - 3.5)} {fmt(b - 5.2)}"
            f"A2.5 2.5 0 0 1 {fmt(x + w - 2)} {fmt(b)}Z")


# ============================================================================ creative and lab roles

@icon("fashion-model", CAT, "Figure in a long coat with lapels and a belt, with camera flash sparkles",
      tags=["model", "runway", "catwalk", "fashion show", "coat", "photoshoot", "style"])
def _(S):
    cx = 8.5
    return (person(S, cx, 8.5, 3.0, 14.5, 5.0)
            + [detail(poly([(cx - 1.8, 14.5), (cx, 18), (cx + 1.8, 14.5)], r=S.r)),
               star4(19, 7, 3), star4(20.5, 15, 1.8)])


@icon("fortune-teller", CAT, "Figure in a headscarf with a crystal ball on a stand",
      tags=["psychic", "clairvoyant", "crystal ball", "medium", "seer", "tarot", "mystic"])
def _(S):
    cx, hy = 7, 10
    scarf = dome(cx, hy - 0.7, 4.0, 4.6)
    return (head(cx, hy, hy - 0.7, scarf) + [solid(poly([(cx + 3.4, hy - 1), (cx + 6.4, hy + 0.8), (cx + 3.4, hy + 1.6)], closed=True)),shell(bust_d(S, cx, 16.0, 4.5)),
            shell(circle(17.5, 11.5, 3.6)), shell(poly([(14.5, 21), (16, 16.6), (19, 16.6), (20.5, 21)], closed=True, r=S.r * 0.4)),
            dot(16.5, 10.5, 0.8), star4(19.5, 4.5, 2)])


@icon("street-artist", CAT, "Figure in a cap with a spray can and paint mist",
      tags=["graffiti", "mural", "spray paint", "urban art", "painter", "wall art", "muralist"])
def _(S):
    cx, hy = 7, 10
    return (head(cx, hy, hy - 1.4, dome(cx, hy - 1.4, 3.3, 3.0) + "M" + fmt(cx + 0.5) + " " + fmt(hy - 1.4) + "H" + fmt(cx + 6.6))
            + [shell(bust_d(S, cx, 16.0, 4.5)),
               shell(rect(14.5, 13, 5, 8, S.R * 0.4)), shell(rect(16, 10, 2, 3)),
               dot(17.2, 7.2, 0.9), dot(20.8, 6.2, 0.9), dot(14.4, 6.4, 0.9), dot(21, 9.8, 0.9)])


@icon("animator", CAT, "Figure beside a film strip with a bouncing ball in each frame",
      tags=["animation", "cartoon", "film strip", "frames", "motion graphics", "keyframe", "storyboard"])
def _(S):
    cx = 6.5
    return (lp(S, cx, 9.0)
            + [shell(rect(14, 3, 7.5, 18, S.R * 0.4)), detail(seg(14, 9, 21.5, 9)), detail(seg(14, 15, 21.5, 15)),
               dot(17.75, 6, 1), dot(17.75, 12, 1), dot(17.75, 18, 1)])


@icon("research-chemist", CAT, "Figure in safety goggles beside a round bottomed flask with liquid",
      tags=["chemist", "chemistry", "lab", "flask", "goggles", "scientist", "experiment"])
def _(S):
    cx = 6.5
    flask = "M16.5 3.5V9.6A4.5 4.5 0 1 0 19.5 9.6V3.5"
    return (lp(S, cx, 9.0)
            + [mark(rect(cx - 3.3, 7.6, 6.6, 2.4, 1.0)), shell(flask), line(seg(15.6, 3.5, 20.4, 3.5)),
               detail(seg(14.2, 15.5, 21.8, 15.5))])


@icon("biologist", CAT, "Figure looking into a microscope",
      tags=["biology", "microscope", "scientist", "lab", "cells", "specimen", "life science"])
def _(S):
    cx = 6.5
    tube = poly([(13.2, 4.2), (15.6, 3), (19.2, 10), (16.8, 11.4)], closed=True, r=S.r * 0.5)
    return (lp(S, cx, 9.0)
            + [shell(tube), line("M19.5 11.5A5 5 0 0 1 17.5 20"), line(seg(13.5, 20.5, 21.5, 20.5)),
               line(seg(13.5, 16.5, 17, 16.5))])


@icon("astronomer", CAT, "Figure beside a long telescope on a tripod pointed at a star",
      tags=["astronomy", "telescope", "stargazer", "stars", "observatory", "space", "tripod"])
def _(S):
    tube = poly([(10.4, 12.4), (12.6, 14.6), (20.6, 6.6), (18.4, 4.4)], closed=True, r=S.r * 0.4)
    return (person(S, 5.5, 9.0, 3.0, 15.0, 4.0)
            + [shell(tube), line(seg(16.4, 11.4, 14, 21)), line(seg(16.4, 11.4, 19.5, 21)),
               star4(20.5, 14, 2.3), star4(21, 2.6, 1.6)])


@icon("archaeologist", CAT, "Figure in a wide brim hat beside a cracked clay pot",
      tags=["archaeology", "dig", "excavation", "artifact", "pottery", "ruins", "expedition"])
def _(S):
    cx, hy = 6.5, 10
    pot = "M15 10.5H20.5C22 13.5 21.8 17.5 20 21H15.5C13.7 17.5 13.5 13.5 15 10.5Z"
    brim = poly([(cx - 5.2, hy - 1.0), (cx + 5.2, hy - 1.0)])
    return (head(cx, hy, hy - 1.4, dome(cx, hy - 1.4, 2.7, 2.6) + "M" + fmt(cx - 5.6) + " " + fmt(hy - 1.4) + "H" + fmt(cx + 5.6))
            + [shell(bust_d(S, cx, 16.0, 4.5)), shell(pot),
               detail(poly([(17.2, 12.8), (18.4, 15), (17.4, 17)]))])


@icon("paleontologist", CAT, "Figure in a bush hat beside a large bone with a small brush",
      tags=["paleontology", "fossil", "dinosaur", "bone", "dig site", "prehistoric", "scientist"])
def _(S):
    cx, hy = 6.5, 9.5
    return (head(cx, hy, hy - 1.4, dome(cx, hy - 1.4, 2.8, 3.2) + "M" + fmt(cx - 4.6) + " " + fmt(hy - 1.4) + "H" + fmt(cx + 4.6))
            + [shell(bust_d(S, cx, 15.5, 4.5)), line(seg(14, 18.5, 21, 18.5)),
               solid(circle(13.8, 17.2, 1.7)), solid(circle(13.8, 19.8, 1.7)),
               solid(circle(21.2, 17.2, 1.7)), solid(circle(21.2, 19.8, 1.7)),
               line(seg(14.5, 12, 17.5, 15)), line(seg(17.5, 15, 19, 13.5))])


@icon("geologist", CAT, "Figure in a hard hat holding a rock hammer with a pointed pick",
      tags=["geology", "rock hammer", "rocks", "minerals", "field work", "hard hat", "earth science"])
def _(S):
    cx, hy = 6.5, 10
    hd = poly([(13, 8.6), (17, 6.4), (21.8, 6.4), (21.8, 9.8), (17, 9.8)], closed=True, r=S.r * 0.4)
    return (head(cx, hy, hy - 1.4, dome(cx, hy - 1.4, 3.3, 3.4) + "M" + fmt(cx - 4.4) + " " + fmt(hy - 1.4) + "H" + fmt(cx + 4.4))
            + [shell(bust_d(S, cx, 16.0, 4.5)), shell(hd), line(seg(18, 10, 15.5, 21))])


@icon("botanist", CAT, "Figure beside a potted plant with a magnifying glass above the leaves",
      tags=["botany", "plants", "magnifier", "greenhouse", "plant scientist", "leaves", "flora"])
def _(S):
    cx = 6
    leaf_l = "M18 16C18 13 16 12.5 14.8 12.5C14.8 14.6 15.8 16 18 16Z"
    leaf_r = "M18 15C18 12.5 19.8 12 21 12C21 14.2 20 15 18 15Z"
    return (lp(S, cx, 9.0)
            + [shell(circle(17.5, 6.4, 2.8)), line(seg(15.6, 8.5, 13.6, 11)),
               shell(poly([(14.5, 17.5), (21.5, 17.5), (20.4, 21), (15.6, 21)], closed=True, r=S.r * 0.5)),
               line(seg(18, 17.5, 18, 15)), shell(leaf_l), shell(leaf_r)])


@icon("marine-biologist", CAT, "Figure in a diving mask and snorkel beside a fish",
      tags=["ocean scientist", "snorkel", "diving", "fish", "sea", "underwater", "marine"])
def _(S):
    cx = 6.5
    return (lp(S, cx, 9.0)
            + [mark(rect(cx - 3.4, 7.4, 6.8, 2.8, 1.2)), line(poly([(cx + 3.2, 9), (cx + 4.6, 9), (cx + 4.6, 3.5)], r=S.r * 0.5)),
               shell(ellipse(16.5, 14.5, 3.6, 2.7)), shell(poly([(19.6, 14.5), (22.2, 12), (22.2, 17)], closed=True, r=S.r * 0.4)),
               dot(15.4, 13.8, 0.7)])


@icon("meteorologist", CAT, "Figure holding a weather balloon on a string above a small cloud",
      tags=["weather forecaster", "forecast", "weather balloon", "climate", "cloud", "atmosphere", "weatherman"])
def _(S):
    return (lp(S, 6, 9.0)
            + [shell(ellipse(17.5, 6, 3.2, 3.6)), line(poly([(17.5, 9.6), (15.2, 12.2), (11.8, 14)], r=S.r * 0.5)),
               shell(cloud(13.5, 16, 8.5))])


@icon("mathematician", CAT, "Figure beside a board showing a pi symbol and an equals sign",
      tags=["math", "maths", "pi", "equation", "blackboard", "algebra", "professor"])
def _(S):
    cx = 6
    return (lp(S, cx, 9.0)
            + [shell(rect(12.5, 2.5, 9.5, 9.5, S.R * 0.4)),
               detail(seg(14.8, 5.8, 19.8, 5.8)), detail(seg(16.2, 5.8, 16.2, 9.5)), detail(seg(18.4, 5.8, 18.4, 9.5)),
               line(seg(14.5, 15.2, 20, 15.2)), line(seg(14.5, 18.5, 20, 18.5))])


@icon("inventor", CAT, "Figure with wild hair holding up a glowing light bulb",
      tags=["invention", "idea", "light bulb", "innovation", "creator", "eureka", "tinkerer"])
def _(S):
    cx = 6.5
    bulb = "M15.4 15.4V12.2A4 4 0 1 1 19.6 12.2V15.4Z"
    return (lp(S, cx, 10.0)
            + [line(seg(cx - 2, 6, cx - 3, 3.6)), line(seg(cx, 5.6, cx, 3)), line(seg(cx + 2, 6, cx + 3, 3.6)),
               shell(bulb), line(seg(15.9, 18.6, 19.1, 18.6)),
               dot(12.2, 6.2, 0.9), dot(22.2, 6.2, 0.9), dot(17.5, 1.8, 0.9)])


def hat(cx, hy, cw, ch, bl, br, y=None):
    """Hat on a head: crown dome (half-width cw, height ch) on a flat brim line from cx-bl to cx+br at y."""
    y = hy - 1.4 if y is None else y
    d = dome(cx, y, cw, ch) + f"M{fmt(cx - bl)} {fmt(y)}H{fmt(cx + br)}"
    return head(cx, hy, y, d)


def wave(x0, x1, y, step=6.0, amp=1.2):
    n = int(round((x1 - x0) / step))
    d = f"M{fmt(x0)} {fmt(y)}q{fmt(step / 4)} {fmt(-amp)} {fmt(step / 2)} 0"
    for _ in range(1, 2 * n):
        d += f"t{fmt(step / 2)} 0"
    return d


def rotpts(pts, deg, cx, cy):
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * sn, cy + (x - cx) * sn + (y - cy) * c) for x, y in pts]


# ============================================================================ field and teaching roles

@icon("entomologist", CAT, "Figure holding a butterfly net with a butterfly below it",
      tags=["insects", "bugs", "butterfly net", "insect scientist", "bug collector", "specimen", "butterfly"])
def _(S):
    return (lp(S, 6.5, 10.0)
            + [shell(ellipse(18, 5, 3.8, 1.6)), line("M14.2 5C14.2 10.5 15.5 13.5 18 13.5C20.5 13.5 21.8 10.5 21.8 5"),
               line(poly([(14.2, 5), (13, 9.5), (11.6, 15.2)])),
               solid(poly([(18, 18.4), (14.6, 15.6), (14.6, 19.4)], closed=True)),
               solid(poly([(18, 18.4), (21.4, 15.6), (21.4, 19.4)], closed=True)), line(seg(18, 15.8, 18, 20.8))])


@icon("birdwatcher", CAT, "Figure holding binoculars to the eyes beside a small bird on a branch",
      tags=["birding", "bird watching", "binoculars", "ornithologist", "nature", "wildlife", "bird"])
def _(S):
    cx, hy = 6.5, 9.5
    return (lp(S, cx, hy)
            + [mark(circle(cx - 2, hy, 2.0)), mark(circle(cx + 2, hy, 2.0)), mark(rect(cx - 2, hy - 1, 4, 1.6)),
               shell(ellipse(18, 10.5, 3, 2.2)), solid(poly([(20.6, 9.9), (22.6, 9.5), (20.8, 11.3)], closed=True)),
               line(seg(14.5, 15.5, 22, 15.5)), line(seg(17, 12.7, 17, 15.5)), line(seg(19, 12.7, 19, 15.5)),
               dot(16.9, 9.9, 0.7)])


@icon("volcanologist", CAT, "Figure in a hooded heat suit with a visor beside an erupting volcano",
      tags=["volcano", "lava", "eruption", "geologist", "heat suit", "magma", "scientist"])
def _(S):
    cx, hy = 6, 10
    cone = poly([(11.5, 21), (15.8, 11.5), (19.2, 11.5), (22, 21)], closed=True, r=S.r * 0.4)
    return ([shell(circle(cx, hy, 4.4)), mark(rect(cx - 3, hy - 1.4, 6, 2.8, 1.2)), shell(bust_d(S, cx, 16.0, 4.5)),
             shell(cone), detail(poly([(17.7, 11.5), (17, 15), (18.5, 17)])),
             line(seg(16.2, 8.7, 15.2, 5.4)), line(seg(18.2, 8.2, 18.2, 3.6)), line(seg(20.2, 8.7, 21.2, 5.4))])


@icon("explorer", CAT, "Figure in a pith helmet beside a compass",
      tags=["adventurer", "expedition", "pith helmet", "compass", "safari", "discovery", "navigator"])
def _(S):
    cx, hy = 6.5, 10
    return (hat(cx, hy, 3.4, 3.0, 5.0, 5.0)
            + [shell(bust_d(S, cx, 16.0, 4.5)), shell(circle(17.5, 13.5, 5)),
               mark(poly([(19.8, 11.2), (18.9, 14.9), (15.2, 15.8), (16.1, 12.1)], closed=True))])


@icon("mountaineer", CAT, "Figure in a helmet with a headlamp and a rope across the chest beside a snowy peak with a flag",
      tags=["climber", "mountain climbing", "summit", "alpine", "helmet", "rope", "peak"])
def _(S):
    cx, hy = 6.5, 10
    return (hat(cx, hy, 3.4, 3.2, 3.9, 3.9)
            + [shell(bust_d(S, cx, 16.0, 4.5)), detail(seg(cx - 3.5, 16.8, cx + 3.0, 21)),
               shell(poly([(12.5, 21), (17.5, 9), (22.5, 21)], closed=True, r=S.r * 0.5)),
               detail(poly([(15.2, 14.6), (17.5, 17), (19.8, 14.6)])),
               line(seg(17.5, 9, 17.5, 3.5)), solid(poly([(17.5, 3.6), (21, 5), (17.5, 6.4)], closed=True))])


@icon("polar-explorer", CAT, "Figure in a fur hood pulling a sled by a rope",
      tags=["arctic", "antarctic", "expedition", "sled", "snow", "fur hood", "ice explorer"])
def _(S):
    cx, hy = 6, 9
    return ([shell(circle(cx, hy, 4.6)), detail(circle(cx, hy, 2.2)), shell(bust_d(S, cx, 15.5, 4.5, 21)),
             line(seg(10.5, 16.4, 13.5, 14.2)),
             shell(rect(13.5, 12.5, 8.5, 3, 1.0)), line("M12.5 20.8H21Q23 20.8 23 18.8"),
             line(seg(15.5, 15.5, 15.5, 20.8)), line(seg(20, 15.5, 20, 20.8))])


@icon("school-principal", CAT, "Figure in a suit and tie in front of a school building with a flag on the roof",
      tags=["headmaster", "headteacher", "school head", "administrator", "school", "education", "dean"])
def _(S):
    cx = 6
    return (lp(S, cx, 9.0)
            + [detail(poly([(cx - 1.5, 15), (cx, 17.5), (cx + 1.5, 15)])), detail(seg(cx, 17.5, cx, 21)),
               shell(poly([(13.5, 21), (13.5, 11), (17.5, 8), (21.5, 11), (21.5, 21)], closed=True, r=S.r * 0.5)),
               mark(rect(16.5, 16, 2, 5)), line(seg(17.5, 8, 17.5, 3.5)),
               solid(poly([(17.5, 3.6), (21, 5), (17.5, 6.4)], closed=True))])


@icon("scout", CAT, "Figure in a campaign hat and neckerchief beside a small tent",
      tags=["boy scout", "girl scout", "camping", "tent", "neckerchief", "troop", "outdoors"])
def _(S):
    cx, hy = 6.5, 10
    return (hat(cx, hy, 3.0, 3.0, 5.4, 5.4)
            + [shell(bust_d(S, cx, 16.0, 4.5)), mark(poly([(cx - 2.6, 16), (cx + 2.6, 16), (cx, 19.4)], closed=True)),
               shell(poly([(12.5, 21), (17.5, 10), (22.5, 21)], closed=True, r=S.r * 0.5)),
               detail(poly([(15.8, 21), (17.5, 16.6), (19.2, 21)]))])


@icon("sports-coach", CAT, "Figure with a whistle on a cord beside a clipboard with an X and an O",
      tags=["coach", "trainer", "clipboard", "whistle", "playbook", "team sports", "tactics"])
def _(S):
    cx = 6
    return (lp(S, cx, 9.0)
            + [detail(poly([(cx - 1.6, 15), (cx, 18), (cx + 1.6, 15)])), mark(circle(cx, 18.6, 1.1)),
               shell(rect(13, 5, 9, 15, S.R * 0.4)),
               detail(seg(15.2, 8.2, 17.6, 10.8)), detail(seg(17.6, 8.2, 15.2, 10.8)), detail(circle(19.2, 15.6, 1.4))])


@icon("yoga-instructor", CAT, "Figure standing in tree pose with palms together above the head on a mat",
      tags=["yoga teacher", "tree pose", "vrksasana", "balance", "stretch", "mat", "wellness"])
def _(S):
    return [solid(circle(12, 8, 1.7)),
            line(poly([(12, 11), (12, 15.5)])),
            line(poly([(12, 11), (7.2, 6.8), (12, 2.6)], r=S.r * 0.4)),
            line(poly([(12, 11), (16.8, 6.8), (12, 2.6)], r=S.r * 0.4)),
            line(poly([(12, 15.5), (12, 21)])),
            line(poly([(12, 15.5), (17.5, 16.8), (12.4, 19)], r=S.r * 0.4)),
            line(seg(5, 21.5, 19, 21.5))]


@icon("ski-instructor", CAT, "Figure in a beanie and goggles with a ski pole and a ski",
      tags=["skiing", "ski teacher", "snowboard instructor", "winter sports", "slope", "pole", "beanie"])
def _(S):
    cx, hy = 7, 8.5
    beanie = dome(cx, hy - 1.2, 3.3, 3.2)
    return (head(cx, hy, hy - 1.2, beanie) + [dot(cx, hy - 5.3, 1.0),
            shell(bust_d(S, cx, 14.5, 4.5, 18.5)), mark(rect(cx - 2.6, hy - 1.0, 5.2, 1.8, 0.9)),
            line(seg(16.5, 7, 15, 17.5)), line(seg(13.6, 15.2, 16.4, 15.2)),
            line("M2.5 21H17.5Q20.5 21 21.5 18.5")])


@icon("swim-instructor", CAT, "Figure in a swim cap standing in waves holding a kickboard",
      tags=["swimming teacher", "lifeguard", "pool", "kickboard", "swim lessons", "water", "coach"])
def _(S):
    cx, hy = 8, 6.5
    cap = dome(cx, hy - 0.4, 3.3, 3.4)
    return (head(cx, hy, hy - 0.4, cap)
            + [shell(bust_d(S, cx, 12.5, 4.5, 16.5)), shell(rect(14.5, 8.5, 7.5, 4.2, 1.8)),
               line(poly([(12.5, 14), (14.8, 12.7)])),
               line(wave(2, 22, 18, 6, 1.2)), line(wave(2, 22, 21.5, 6, 1.2))])


@icon("dance-teacher", CAT, "Figure with a hair bun and a raised arm beside a wall mirror and barre",
      tags=["ballet teacher", "choreographer", "dance class", "studio", "barre", "mirror", "dancer"])
def _(S):
    cx, hy = 6, 9.5
    return (lp(S, cx, hy)
            + [solid(circle(cx, hy - 4.4, 1.5)), line(poly([(10, 16.5), (12.5, 12), (13.2, 7.2)], r=S.r * 0.5)),
               shell(rect(15.5, 3, 6.5, 13, S.R * 0.4)), detail(seg(17.4, 12, 20, 6.5)),
               line(seg(15, 19, 22, 19))])


@icon("golf-caddie", CAT, "Figure in a cap carrying a golf bag with clubs over the shoulder",
      tags=["caddy", "golf bag", "clubs", "golf course", "carrier", "fairway", "sport"])
def _(S):
    cx, hy = 6, 10
    pv, a = (18, 19), -16

    def rp(pts, closed=True, r=0.0):
        return poly(rotpts(pts, a, *pv), closed=closed, r=r)
    bag = rp([(15.5, 12.5), (20.5, 12.5), (20.5, 21), (15.5, 21)], r=S.r)
    clubs = []
    for x, top in ((16.4, 6), (18, 3.8), (19.6, 6)):
        clubs.append(line(rp([(x, 12.5), (x, top)], closed=False)))
        clubs.append(solid(rp([(x - 0.8, top - 0.2), (x + 1.6, top - 0.2), (x + 1.6, top + 1.4), (x - 0.8, top + 1.4)])))
    return (hat(cx, hy, 3.2, 2.8, 2.8, 6.2)
            + [shell(bust_d(S, cx, 16.0, 4.5)), shell(bag), detail(seg(*rotpts([(15.5, 16.5)], a, *pv)[0], *rotpts([(20.5, 16.5)], a, *pv)[0]))]
            + clubs)


@icon("umpire", CAT, "Figure in a cage face mask and chest protector with crossed straps",
      tags=["referee", "baseball umpire", "catcher mask", "official", "sports official", "ref", "judge"])
def _(S):
    cx, hy = 12, 9
    return ([shell(circle(cx, hy, 3.8)), detail(seg(cx - 3.8, hy - 1, cx + 3.8, hy - 1)),
             detail(seg(cx - 3.6, hy + 1.6, cx + 3.6, hy + 1.6)), detail(seg(cx, hy - 3.8, cx, hy + 3.8)),
             shell(bust_d(S, cx, 15.5, 7.5, 21)), detail(seg(cx - 3.5, 15.5, cx - 1.5, 21)), detail(seg(cx + 3.5, 15.5, cx + 1.5, 21))])


@icon("line-judge", CAT, "Figure holding a small flag straight out to the side",
      tags=["linesman", "line referee", "flag", "sports official", "offside", "tennis", "assistant referee"])
def _(S):
    cx = 7
    return (lp(S, cx, 10.0)
            + [line(seg(cx + 3.6, 16.6, 13.5, 14)), line(seg(13.5, 14, 13.5, 3.5)),
               shell(poly([(13.5, 3.5), (20.6, 6.5), (13.5, 9.5)], closed=True, r=S.r * 0.5))])


def beard(cx, hy, w=2.5, d=5.6):
    """Solid beard hanging from the lower half of a head."""
    y0 = hy + 1.3
    return solid(f"M{fmt(cx - w)} {fmt(y0)}C{fmt(cx - w - 0.2)} {fmt(hy + d * 0.85)} {fmt(cx - 1)} {fmt(hy + d)} {fmt(cx)} {fmt(hy + d)}"
                 f"C{fmt(cx + 1)} {fmt(hy + d)} {fmt(cx + w + 0.2)} {fmt(hy + d * 0.85)} {fmt(cx + w)} {fmt(y0)}Z")


def cross_solid(cx, cy, arm=1.7, w=1.4):
    return u(rect(cx - w / 2, cy - arm, w, 2 * arm), rect(cx - arm, cy - w / 2, 2 * arm, w))


def heart(cx, cy, k=1.0):
    """Small heart centred on (cx, cy), about 5k wide."""
    return (f"M{fmt(cx)} {fmt(cy + 2.3 * k)}L{fmt(cx - 2.3 * k)} {fmt(cy - 0.1 * k)}A{fmt(1.35 * k)} {fmt(1.35 * k)} 0 0 1 {fmt(cx)} {fmt(cy - 1.5 * k)}"
            f"A{fmt(1.35 * k)} {fmt(1.35 * k)} 0 0 1 {fmt(cx + 2.3 * k)} {fmt(cy - 0.1 * k)}Z")


def cross_d(cx, cy, r=2.0):
    return f"M{fmt(cx - r)} {fmt(cy)}H{fmt(cx + r)}M{fmt(cx)} {fmt(cy - r)}V{fmt(cy + r)}"


def beads(x, y0, n=4, dy=2.3, dx=0.9):
    """Hanging string of prayer beads."""
    return [dot(x + (dx if i % 2 else 0), y0 + i * dy, 0.95) for i in range(n)]


# ============================================================================ faith roles

@icon("priest", CAT, "Head and shoulders figure in a dark shirt with a white clerical collar tab and a small cross",
      tags=["clergy", "minister", "father", "church", "clerical collar", "pastor", "chaplain"])
def _(S):
    cx = 10.5
    return (person(S, cx, 8.5, 3.0, 14.5, 6.5)
            + [detail(poly([(cx - 1.6, 14.5), (cx, 17.2), (cx + 1.6, 14.5)], r=S.r * 0.5)), mark(rect(cx - 0.9, 14.7, 1.8, 2.3)),
               line(cross_d(20, 5.5, 2.2))])


@icon("nun", CAT, "Figure in a habit and veil with a white band framing the face and a small cross",
      tags=["sister", "habit", "veil", "convent", "religious", "abbey", "wimple"])
def _(S):
    cx, hy = 12, 8.8
    veil = poly([(cx - 7, 21), (cx - 5, hy + 2), (cx - 5, hy - 1), (cx - 2.8, hy - 5), (cx + 2.8, hy - 5), (cx + 5, hy - 1),
                 (cx + 5, hy + 2), (cx + 7, 21)], closed=True, r=L(S, 1.0, 3.2))
    return [shell(veil), detail(circle(cx, hy + 0.3, 2.7)), mark(cross_solid(cx, 17.6))]


@icon("monk", CAT, "Figure in a hooded robe with a rope belt holding prayer beads",
      tags=["friar", "hooded robe", "monastery", "abbey", "rosary", "brother", "cowl"])
def _(S):
    cx, hy = 8.5, 9.5
    robe = (f"M{fmt(cx - 5.5)} 21L{fmt(cx - 4.5)} {fmt(hy + 2.5)}A4.8 6 0 0 1 {fmt(cx + 4.5)} {fmt(hy + 2.5)}L{fmt(cx + 5.5)} 21Z")
    return ([shell(robe), detail(circle(cx, hy + 0.2, 2.3)), detail(seg(cx - 5.2, 17, cx + 5.2, 17))]
            + [line(poly([(16.4, 12.5), (16.4, 14.5)]))] + beads(16.4, 15.4, 4, 2.0, 0.9))


@icon("buddhist-monk", CAT, "Figure with a shaved head in a robe draped over one shoulder with palms together",
      tags=["bhikkhu", "buddhism", "robe", "temple", "meditation", "monastic", "lama"])
def _(S):
    cx, hy = 12, 8.5
    return (person(S, cx, hy, 3.0, 14.5, 6.5)
            + [detail(poly([(cx + 1.5, 14.5), (cx + 3.2, 17.5), (cx + 4.2, 21)])),
               mark(f"M{fmt(cx - 1.2)} 20.6C{fmt(cx - 1.2)} 18.4 {fmt(cx - 0.5)} 17.4 {fmt(cx - 0.4)} 17C{fmt(cx - 0.3)} 17.4 {fmt(cx + 0.4)} 18.4 {fmt(cx + 0.4)} 20.6Z")])


@icon("imam", CAT, "Figure in a round cap with a short beard and a long robe holding a string of prayer beads",
      tags=["muslim cleric", "mosque", "prayer leader", "kufi", "tasbih", "islam", "sheikh"])
def _(S):
    cx, hy = 8, 9.5
    cap = dome(cx, hy - 1.6, 2.9, 2.2)
    return (head(cx, hy, hy - 1.6, cap) + [beard(cx, hy), shell(bust_d(S, cx, 16.0, 5.0, 21))]
            + [line(poly([(16.5, 12.5), (16.5, 14.5)]))] + beads(16.5, 15.4, 4, 2.0, 0.9))


@icon("rabbi", CAT, "Bearded figure in a kippah with a striped prayer shawl on the shoulders",
      tags=["jewish teacher", "kippah", "yarmulke", "tallit", "synagogue", "judaism", "torah"])
def _(S):
    cx, hy = 12, 8.5
    kip = dome(cx, hy - 2.1, 2.6, 1.6)
    return (head(cx, hy, hy - 2.1, kip) + [beard(cx, hy), shell(bust_d(S, cx, 15.0, 6.5, 21)),
            detail(seg(cx - 3.2, 15.4, cx - 3.2, 21)), detail(seg(cx + 3.2, 15.4, cx + 3.2, 21))])


@icon("church-bishop", CAT, "Figure in a tall pointed mitre holding a crozier staff with a curled top",
      tags=["bishop", "mitre", "crozier", "clergy", "cathedral", "pope", "church leader"])
def _(S):
    cx, hy = 7.5, 11
    mitre = poly([(cx - 3.5, hy - 1.6), (cx - 3.5, hy - 4.2), (cx, hy - 9), (cx + 3.5, hy - 4.2), (cx + 3.5, hy - 1.6)], closed=True, r=S.r * 0.4)
    return (head(cx, hy, hy - 1.6, mitre) + [shell(bust_d(S, cx, 16.5, 4.5)), detail(seg(cx, hy - 7, cx, hy - 2.4)),
            line("M19.5 21V8A3 3 0 1 0 16.5 11")])


@icon("pilgrim-walker", CAT, "Figure in a wide brim hat with a walking staff and a scallop shell on the chest",
      tags=["pilgrim", "pilgrimage", "walking staff", "scallop shell", "camino", "wayfarer", "hiker"])
def _(S):
    cx, hy = 7.5, 10
    shell_d = f"M{fmt(cx - 2.6)} 20.6A2.7 2.7 0 0 1 {fmt(cx + 2.6)} 20.6Z"
    return (hat(cx, hy, 3.0, 2.8, 5.4, 5.4)
            + [shell(bust_d(S, cx, 16.0, 4.5)), mark(shell_d),
               line(seg(18, 4.5, 18, 21)), line("M18 4.5A1.8 1.8 0 1 1 20.4 6.2")])


# ============================================================================ historic roles

@icon("armored-knight", CAT, "Figure in plate armor with a visored helmet holding a kite shaped shield",
      tags=["knight", "medieval", "armor", "helmet", "shield", "chivalry", "crusader"])
def _(S):
    cx, hy = 7, 9.5
    helm = (f"M{fmt(cx - 3.8)} {fmt(hy + 3.6)}V{fmt(hy - 0.6)}A3.8 4.4 0 0 1 {fmt(cx + 3.8)} {fmt(hy - 0.6)}V{fmt(hy + 3.6)}Z")
    shield = poly([(14, 8.5), (21, 8.5), (21, 13.5), (17.5, 20.5), (14, 13.5)], closed=True, r=S.r * 0.6)
    return [shell(helm), mark(rect(cx - 3.0, hy - 0.4, 6, 1.5)), line(seg(cx, hy - 4.4, cx, hy - 6.2)),
            shell(bust_d(S, cx, 15.5, 5.0, 21)), shell(shield), detail(seg(17.5, 8.5, 17.5, 17))]


@icon("samurai", CAT, "Figure in a horned kabuto helmet and layered shoulder armor holding a sheathed sword",
      tags=["japanese warrior", "kabuto", "katana", "armor", "bushido", "ronin", "japan"])
def _(S):
    cx, hy = 7.5, 10.5
    helm = dome(cx, hy - 1.2, 3.4, 3.2)
    guard = poly([(cx - 5.6, hy + 1.8), (cx - 3.4, hy - 1.2), (cx + 3.4, hy - 1.2), (cx + 5.6, hy + 1.8)], closed=False)
    return (head(cx, hy, hy - 1.2, helm)
            + [line(guard), line(poly([(cx - 1, hy - 4.4), (cx - 3.4, hy - 6), (cx - 4.4, hy - 8.4)], r=S.r * 0.4)),
               line(poly([(cx + 1, hy - 4.4), (cx + 3.4, hy - 6), (cx + 4.4, hy - 8.4)], r=S.r * 0.4)),
               shell(bust_d(S, cx, 16.0, 5.0, 21)), detail(seg(cx - 5, 18.6, cx + 5, 18.6)),
               line(seg(14, 20.5, 21, 8.5)), solid(poly([(12.6, 16.2), (16.4, 18.4), (15.6, 19.8), (11.8, 17.6)], closed=True))])


@icon("viking-warrior", CAT, "Bearded figure in a round helmet with a nose guard holding a round shield",
      tags=["viking", "norse", "warrior", "helmet", "shield", "raider", "scandinavian"])
def _(S):
    cx, hy = 7, 9.5
    helm = dome(cx, hy - 1.2, 3.3, 3.3)
    return (head(cx, hy, hy - 1.2, helm)
            + [line(seg(cx, hy - 1.2, cx, hy + 1.2)), beard(cx, hy), shell(bust_d(S, cx, 16.0, 4.8, 21)),
               shell(circle(17.5, 14.8, 4.8)), dot(17.5, 14.8, 1.3)])


@icon("gladiator", CAT, "Figure in a crested helmet with a grilled visor holding a round shield",
      tags=["roman fighter", "arena", "colosseum", "helmet", "combat", "warrior", "shield"])
def _(S):
    cx, hy = 7, 9.5
    helm = (f"M{fmt(cx - 3.8)} {fmt(hy + 3.4)}V{fmt(hy - 0.8)}A3.8 4.2 0 0 1 {fmt(cx + 3.8)} {fmt(hy - 0.8)}V{fmt(hy + 3.4)}Z")
    crest = poly([(cx - 2.4, hy - 3.6), (cx - 1.4, hy - 6.4), (cx + 1.4, hy - 6.4), (cx + 2.4, hy - 3.6)], closed=True, r=S.r * 0.4)
    return [shell(helm), shell(crest), detail(seg(cx - 3.8, hy + 0.1, cx + 3.8, hy + 0.1)), detail(seg(cx - 3.8, hy + 2.0, cx + 3.8, hy + 2.0)),
            detail(seg(cx, hy - 0.8, cx, hy + 3.4)),
            shell(bust_d(S, cx, 15.8, 4.8, 21)), shell(circle(17.5, 14.8, 4.8)), detail(circle(17.5, 14.8, 1.8))]


@icon("roman-centurion", CAT, "Figure in a helmet with a sideways brush crest holding a rectangular curved shield",
      tags=["roman soldier", "legionary", "centurion", "helmet", "crest", "scutum", "ancient rome"])
def _(S):
    cx, hy = 7, 10.5
    helm = dome(cx, hy - 1.2, 3.3, 3.0)
    return (head(cx, hy, hy - 1.2, helm)
            + [shell(rect(cx - 4.8, hy - 6.6, 9.6, 2.4, 1.0 if S.name == "line" else 1.2)),
               shell(bust_d(S, cx, 16.0, 4.8, 21)),
               shell(rect(14, 8.5, 8, 12.5, 3.2 if S.name == "line" else 4)), detail(seg(18, 10.5, 18, 19)), detail(seg(15.5, 14.8, 20.5, 14.8))])


@icon("pharaoh", CAT, "Head and shoulders figure in a striped nemes headdress with a braided false beard",
      tags=["egyptian king", "ancient egypt", "nemes", "royal", "headdress", "sphinx", "ruler"])
def _(S):
    cx, hy = 12, 9
    nemes = poly([(cx - 7.4, 17), (cx - 5.4, 6.5), (cx - 3.2, 2.6), (cx + 3.2, 2.6), (cx + 5.4, 6.5), (cx + 7.4, 17)],
                 closed=True, r=L(S, 0.5, 2.5))
    return [shell(nemes), detail(circle(cx, hy + 0.4, 2.7)), detail(seg(cx - 4.6, 5.6, cx + 4.6, 5.6)),
            mark(rect(cx - 1.0, 13.6, 2.0, 5.6, 0.6))]


@icon("musketeer", CAT, "Figure in a wide feathered hat and cape holding a thin rapier",
      tags=["swordsman", "rapier", "feather hat", "cavalier", "swashbuckler", "duelist", "cape"])
def _(S):
    cx, hy = 7, 10
    return (hat(cx, hy, 3.0, 2.8, 5.6, 5.6)
            + [line("M9.5 6.6Q13 2.4 18 4.6"), shell(bust_d(S, cx, 16.0, 4.8, 21)), detail(seg(cx - 4.8, 16.8, cx + 1.5, 21)),
               line(seg(15.5, 20.5, 21, 8.5)), line(seg(13.9, 17.4, 17.1, 19.0))])


@icon("herald", CAT, "Figure blowing a long straight trumpet with a hanging banner",
      tags=["trumpeter", "fanfare", "announcer", "town crier", "medieval", "banner", "proclamation"])
def _(S):
    cx = 6
    bell = poly([(17, 9.5), (21.6, 6.6), (21.6, 12.4)], closed=True, r=S.r * 0.4)
    banner = poly([(12.6, 11.4), (17.8, 11.4), (17.8, 20), (15.2, 17.6), (12.6, 20)], closed=True, r=S.r * 0.4)
    return lp(S, cx, 9.5) + [line(seg(9.8, 9.5, 17.2, 9.5)), shell(bell), shell(banner), mark(circle(15.2, 14.6, 1.1))]


@icon("lamplighter", CAT, "Figure in a cap raising a long pole to a street lamp top",
      tags=["street lamp", "gas lamp", "lantern", "victorian", "night", "pole", "lighting"])
def _(S):
    cx, hy = 6, 10
    lamp = poly([(18.3, 9.6), (22.7, 9.6), (22, 5.6), (19, 5.6)], closed=True, r=S.r * 0.4)
    return (hat(cx, hy, 3.2, 2.4, 3.2, 5.4)
            + [shell(bust_d(S, cx, 16.0, 4.5)), shell(lamp), line(poly([(18.2, 5.2), (20.5, 2.8), (22.8, 5.2)])),
               line(seg(20.5, 9.6, 20.5, 21)), line(seg(10.8, 16.4, 18.8, 8.4)), dot(20.5, 7.6, 0.8)])


@icon("medieval-archer", CAT, "Figure in a hood drawing a longbow with an arrow on the string",
      tags=["bowman", "longbow", "arrow", "archery", "hood", "robin hood", "medieval"])
def _(S):
    cx, hy = 6, 11
    hood = f"M{fmt(cx - 3.8)} {fmt(hy + 1.5)}V{fmt(hy - 0.6)}A3.8 4.2 0 0 1 {fmt(cx + 3.8)} {fmt(hy - 0.6)}V{fmt(hy + 1.5)}"
    return [shell(circle(cx, hy, 3.0)), line(hood), shell(bust_d(S, cx, 17.0, 4.5)),
            line("M17 2.5Q23.5 12.5 17 22.5"), line(poly([(17, 3), (10.4, 12.5), (17, 22)])),
            line(seg(10.4, 12.5, 21, 12.5))]


@icon("cave-dweller", CAT, "Figure in a one shoulder fur garment holding a wooden club",
      tags=["caveman", "cavewoman", "prehistoric", "stone age", "club", "primitive", "fur"])
def _(S):
    cx = 7
    zig = f"M{fmt(cx - 4.5)} 18.5l1.5 1.5l1.5 -1.5l1.5 1.5l1.5 -1.5l1.5 1.5l1.5 -1.5"
    club = poly([(17.2, 4), (21, 4), (21.4, 8.6), (19.8, 10.6), (18.4, 10.6), (16.8, 8.6)], closed=True, r=S.r * 0.6)
    return (lp(S, cx, 9.5)
            + [line(seg(cx - 1.6, 5.4, cx - 2.4, 3.4)), line(seg(cx + 1.6, 5.4, cx + 2.4, 3.4)),
               detail(zig),
               shell(club), line(seg(19, 10.6, 19, 21))])


@icon("milkmaid", CAT, "Figure in a bonnet carrying two pails on a yoke across the shoulders",
      tags=["dairy maid", "farm", "pails", "yoke", "countryside", "bonnet", "milking"])
def _(S):
    cx, hy = 12, 8.2
    bonnet = dome(cx, hy, 3.8, 4.4)
    return (head(cx, hy, hy, bonnet) + [shell(bust_d(S, cx, 14.4, 3.6, 21)),
            line(poly([(3.4, 17), (8.2, 14.4), (15.8, 14.4), (20.6, 17)])),
            line(seg(3.4, 17, 3.4, 18.4)), line(seg(20.6, 17, 20.6, 18.4)),
            shell(poly([(1.8, 18.4), (5, 18.4), (4.6, 21.6), (2.2, 21.6)], closed=True, r=S.r * 0.3)),
            shell(poly([(19, 18.4), (22.2, 18.4), (21.8, 21.6), (19.4, 21.6)], closed=True, r=S.r * 0.3))])


@icon("pioneer-settler", CAT, "Figure in a bonnet beside a covered wagon wheel",
      tags=["frontier", "homesteader", "wagon wheel", "covered wagon", "prairie", "old west", "settler"])
def _(S):
    cx, hy = 6, 10
    bonnet = dome(cx, hy - 0.4, 3.6, 4.0)
    canvas = "M12.7 12.2A4.8 5.7 0 0 1 22.3 12.2Z"
    spokes = [detail(seg(*polar(17.5, 17.4, 3.7, a), *polar(17.5, 17.4, 3.7, a + 180))) for a in (0, 90)]
    return (head(cx, hy, hy - 0.4, bonnet) + [shell(bust_d(S, cx, 16.0, 4.5)), shell(canvas), shell(circle(17.5, 17.4, 3.7)),
            dot(17.5, 17.4, 1.0)] + spokes)


@icon("witch", CAT, "Figure in a tall pointed hat with a crooked tip holding a broom",
      tags=["halloween", "sorceress", "broomstick", "spooky", "pointed hat", "magic", "costume"])
def _(S):
    cx, hy = 6.5, 11
    y = hy - 1.6
    cone = poly([(cx - 3, y), (cx - 1.4, hy - 6.6), (cx + 0.6, hy - 8.4), (cx + 3.6, hy - 7.8), (cx + 1.6, hy - 5.8), (cx + 3, y)],
                closed=True, r=S.r * 0.4)
    return (head(cx, hy, y, cone + f"M{fmt(cx - 5.6)} {fmt(y)}H{fmt(cx + 5.6)}")
            + [shell(bust_d(S, cx, 16.5, 4.5)), line(seg(21, 4.5, 15.5, 16.5)),
               shell(poly([(15.5, 16.5), (18.2, 17.2), (14.2, 21.5), (11.8, 19.6)], closed=True, r=S.r * 0.4))])


@icon("volunteer", CAT, "Figure in a vest with a heart on the chest holding a box of goods",
      tags=["helper", "charity", "community", "donation box", "heart", "service", "giving"])
def _(S):
    cx = 6.5
    return (lp(S, cx, 9.0)
            + [mark(heart(cx, 18.2, 0.9)),
               shell(rect(14, 14, 8, 7, S.R * 0.3)),
               shell(circle(16.8, 10.6, 1.6)), shell(circle(20.2, 10.6, 1.6))])


# ============================================================================ everyday roles and groups

def small_person(cx, hy, hr=1.5, bw=2.2, bottom=21.0):
    """Tiny solid figure for groups."""
    return [solid(circle(cx, hy, hr)), solid(f"M{fmt(cx - bw)} {fmt(bottom)}A{fmt(bw)} {fmt(bw)} 0 0 1 {fmt(cx + bw)} {fmt(bottom)}Z")]


@icon("team-leader", CAT, "Figure in front of a small row of figures holding up a flag",
      tags=["leader", "manager", "flag", "team", "captain", "lead", "group"])
def _(S):
    cx = 6.5
    return (person(S, cx, 10.5, 3.0, 16.5, 4.2)
            + [line(seg(13.5, 20, 13.5, 3)), solid(poly([(13.5, 3.2), (21, 5.6), (13.5, 8)], closed=True))]
            + small_person(17.4, 14.6, 1.4, 1.9) + small_person(21, 14.6, 1.4, 1.9))


@icon("host-with-microphone", CAT, "Figure in a suit holding a handheld microphone with sound arcs",
      tags=["emcee", "presenter", "mc", "microphone", "announcer", "speaker", "show host"])
def _(S):
    cx = 7
    return (lp(S, cx, 10.0)
            + [detail(poly([(cx - 1.6, 16), (cx, 19), (cx + 1.6, 16)], r=S.r * 0.4)),
               shell(circle(16, 11, 2.3)), line(poly([(14.4, 12.7), (13.2, 16.5), (11.6, 17.5)])),
               line(arc(16, 11, 5.8, -50, 50))])


@icon("guest", CAT, "Figure wearing a name tag sticker on the chest waving hello",
      tags=["attendee", "visitor", "name tag", "hello my name is", "wave", "event guest", "invitee"])
def _(S):
    cx = 7
    return (lp(S, cx, 9.5)
            + [mark(rect(cx - 2.4, 16.8, 4.8, 3, 0.8)),
               line(poly([(cx + 3.6, 16.5), (14, 12), (15.5, 7.6)], r=S.r * 0.4)), solid(circle(15.5, 6, 1.8)),
               line(seg(19.2, 5.2, 21, 4)), line(seg(19.6, 8, 21.8, 8))])


@icon("visitor", CAT, "Figure with a lanyard badge standing beside a door",
      tags=["guest pass", "badge", "lanyard", "check in", "front desk", "reception", "visitor pass"])
def _(S):
    cx = 6.5
    return (lp(S, cx, 9.0)
            + [detail(poly([(cx - 3.2, 15), (cx, 18), (cx + 3.2, 15)])), mark(rect(cx - 1.5, 18, 3, 2.6, 0.6)),
               shell(rect(14, 4.5, 8, 16.5, S.R * 0.3)), dot(19.6, 13, 0.9)])


@icon("passenger", CAT, "Figure holding a boarding pass with a rolling suitcase beside",
      tags=["traveler", "traveller", "commuter", "suitcase", "luggage", "boarding pass", "airport"])
def _(S):
    cx = 6
    return (lp(S, cx, 9.0)
            + [shell(rect(14, 11.5, 7, 8, S.R * 0.4)), line(poly([(17.5, 11.5), (17.5, 7.5)])), line(seg(16, 7.5, 19, 7.5)),
               line(seg(15.6, 19.5, 15.6, 21)), line(seg(19.4, 19.5, 19.4, 21)),
               detail(seg(16, 14.6, 19, 14.6))])


@icon("tourist", CAT, "Figure in a sun hat with a camera around the neck beside a folded map",
      tags=["sightseer", "traveler", "traveller", "vacation", "camera", "holiday", "sightseeing"])
def _(S):
    cx, hy = 6.5, 10
    folded = poly([(13.5, 8), (16.2, 10), (18.9, 8), (21.6, 10), (21.6, 19), (18.9, 17), (16.2, 19), (13.5, 17)], closed=True, r=S.r * 0.4)
    return (hat(cx, hy, 3.0, 2.4, 5.8, 5.8)
            + [shell(bust_d(S, cx, 16.0, 4.5)), mark(rect(cx - 2.2, 17.4, 4.4, 3, 0.8)), shell(folded),
               detail(seg(18.9, 8.4, 18.9, 16.6))])


@icon("backpacker", CAT, "Figure with a tall trekking backpack with a rolled mat on top",
      tags=["traveler", "traveller", "trekker", "rucksack", "hostel", "gap year", "budget travel"])
def _(S):
    cx = 6
    return (lp(S, cx, 10.0)
            + [shell(rect(13, 8, 8.5, 13, S.R * 0.5)), detail(seg(13, 15, 21.5, 15)),
               shell(rect(12.4, 3.6, 9.7, 3.2, 1.5)), detail(seg(17.25, 8, 17.25, 15))])


@icon("hiker", CAT, "Figure with daypack straps and trekking poles walking toward a peak",
      tags=["trekker", "walker", "trail", "trekking poles", "mountain walk", "daypack", "outdoors"])
def _(S):
    cx, hy = 7, 9
    return (person(S, cx, hy, 3.0, 15.0, 4.5, 21)
            + [detail(seg(cx - 2.4, 15.4, cx - 2.4, 21)), detail(seg(cx + 2.4, 15.4, cx + 2.4, 21)),
               line(seg(12.5, 15.5, 18.5, 21)), line(seg(14, 12.5, 21, 19)),
               line(poly([(13.5, 9), (17.5, 3.5), (21.5, 9)], r=S.r * 0.4))])


@icon("sports-fan", CAT, "Figure with a scarf around the neck raising a big foam finger",
      tags=["supporter", "fan", "spectator", "foam finger", "scarf", "cheering", "stadium"])
def _(S):
    cx = 6.5
    mitt = poly([(14.5, 21), (14.5, 16.8), (12.6, 16.4), (12.6, 13.8), (14.5, 13.2), (17.2, 13), (17.2, 4.8), (19.8, 4.8),
                 (19.8, 13), (21.8, 13.6), (21.8, 21)], closed=True, r=S.r * 0.8)
    return (lp(S, cx, 9.0)
            + [mark(rect(cx - 3.8, 12.4, 7.6, 2.4, 1.0)), mark(rect(cx + 0.6, 14, 2.2, 5)), shell(mitt),
               detail(seg(17.4, 16, 21.8, 16)), detail(seg(17.4, 18.6, 21.8, 18.6))])


@icon("protester", CAT, "Figure holding a rectangular placard on a stick above the head",
      tags=["demonstrator", "activist", "rally", "march", "sign", "picket", "demonstration"])
def _(S):
    cx = 8
    return (person(S, cx, 14.5, 3.0, 18.5, 4.5, 21)
            + [shell(rect(4, 2.5, 16, 7.5, S.R * 0.3)), detail(seg(7, 6.2, 17, 6.2)),
               line(seg(16.5, 10, 16.5, 17.5)), line(poly([(12.5, 20), (16.5, 17.5)]))])


@icon("charity-donor", CAT, "Figure holding a coin above a donation box with a heart",
      tags=["giver", "donation", "charity", "philanthropy", "fundraising", "heart", "coin slot"])
def _(S):
    cx = 6
    return (lp(S, cx, 9.0)
            + [shell(rect(14, 12, 8, 9, S.R * 0.3)), detail(seg(16, 14.6, 20, 14.6)), mark(heart(18, 18, 0.8)),
               shell(circle(18, 6.4, 2.2)), line(poly([(11.2, 14.5), (14.8, 9)], r=0))])


@icon("winner-on-podium", CAT, "Figure standing on the top step of a three step podium holding a trophy",
      tags=["champion", "first place", "gold medal", "trophy", "victory", "award ceremony", "sports"])
def _(S):
    podium = poly([(2, 21.5), (2, 17), (8, 17), (8, 14), (16, 14), (16, 17.5), (22, 17.5), (22, 21.5)], closed=True, r=S.r * 0.3)
    cup = poly([(16.8, 2.8), (21, 2.8), (20.4, 6.2), (17.4, 6.2)], closed=True, r=S.r * 0.4)
    return [shell(circle(12, 5.2, 2.0)), shell(podium), detail(seg(8, 14, 8, 21.5)), detail(seg(16, 14, 16, 21.5)),
            line(poly([(12, 8.6), (12, 12.5)])), line(poly([(12, 9.4), (15.2, 6.8), (18.6, 6.4)], r=0)), solid(cup)]


@icon("new-hire", CAT, "Figure with a lanyard badge shaking hands with a figure in a tie",
      tags=["onboarding", "new employee", "welcome", "handshake", "recruit", "first day", "team member"])
def _(S):
    return ([shell(circle(6, 8, 2.6)), shell(bust_d(S, 6, 13.2, 4, 21)),
             detail(poly([(4, 13.2), (6, 16), (8, 13.2)])), mark(rect(4.9, 16.4, 2.2, 2.2, 0.5)),
             shell(circle(18, 8, 2.6)), shell(bust_d(S, 18, 13.2, 4, 21)),
             detail(poly([(16.4, 13.2), (18, 15.6), (19.6, 13.2)])), detail(seg(18, 15.6, 18, 19.4)),
             line(seg(10, 17.6, 14, 17.6))])


@icon("neighbors", CAT, "Two figures talking over a low picket fence",
      tags=["neighbours", "neighbor", "neighbour", "fence", "chat", "community", "next door"])
def _(S):
    return ([shell(circle(6, 6.5, 2.4)), shell(bust_d(S, 6, 11.5, 3.8, 16)),
             shell(circle(18, 6.5, 2.4)), shell(bust_d(S, 18, 11.5, 3.8, 16)),
             dot(11, 5.4, 0.8), dot(13, 5.4, 0.8),
             line(seg(2, 19.2, 22, 19.2)), line(seg(4.5, 15.6, 4.5, 21.5)), line(seg(9.5, 15.6, 9.5, 21.5)),
             line(seg(14.5, 15.6, 14.5, 21.5)), line(seg(19.5, 15.6, 19.5, 21.5))])


@icon("best-friends-high-five", CAT, "Two figures slapping raised hands together with a spark",
      tags=["high five", "friends", "buddies", "celebrate", "teamwork", "success", "friendship"])
def _(S):
    return ([shell(circle(5.5, 10.5, 2.5)), shell(bust_d(S, 5.5, 15.4, 3.8, 21)),
             shell(circle(18.5, 10.5, 2.5)), shell(bust_d(S, 18.5, 15.4, 3.8, 21)),
             line(poly([(8.2, 15.8), (10.6, 10.4), (11.4, 8)], r=S.r * 0.4)), line(poly([(15.8, 15.8), (13.4, 10.4), (12.6, 8)], r=S.r * 0.4)),
             star4(12, 4, 2.4)])


@icon("partner-dancers", CAT, "Two figures in a ballroom hold with joined hands raised between them",
      tags=["ballroom", "couple dance", "waltz", "tango", "dance partners", "dancing", "social dance"])
def _(S):
    gown = poly([(13.2, 21), (14.8, 13.6), (19.2, 13.6), (20.8, 21)], closed=True, r=S.r * 0.6)
    return [shell(circle(6.5, 7, 2.4)), shell(circle(17.5, 7, 2.4)),
            shell(bust_d(S, 6.5, 12.4, 3.6, 21)), shell(gown),
            line(poly([(10, 14), (12, 9.2), (14.2, 14)], r=S.r * 0.5))]


@icon("wedding-officiant", CAT, "Figure behind a small lectern holding an open book with two rings above",
      tags=["celebrant", "marriage", "ceremony", "rings", "minister", "wedding", "vows"])
def _(S):
    cx = 6
    return (lp(S, cx, 10.0)
            + [shell(rect(13.5, 15, 8.5, 6, S.R * 0.3)), line(poly([(13.8, 13.2), (17.75, 11.2), (21.7, 13.2)])),
               shell(circle(15.6, 5.2, 2.1)), shell(circle(19.8, 5.2, 2.1))])


def baby(S, cx, hy=11.0):
    return [shell(circle(cx, hy, 1.9)), shell(bust_d(S, cx, hy + 3.6, 2.8, 21))]


def child(S, cx, hy=12.5):
    return [shell(circle(cx, hy, 2.0)), shell(bust_d(S, cx, hy + 3.7, 3.0, 21))]


@icon("mother-and-baby", CAT, "Woman with a hair bun holding a baby against the shoulder with one hand supporting it",
      tags=["mum", "mom", "mother", "newborn", "infant", "motherhood", "parenting"])
def _(S):
    cx = 7.5
    return lp(S, cx, 9.0) + [solid(circle(cx, 4.6, 1.6))] + baby(S, 17, 11.0) + [line(seg(12, 18.5, 14.2, 18.5))]


@icon("father-and-baby", CAT, "Man with a short beard cradling a baby in both arms",
      tags=["dad", "father", "papa", "newborn", "infant", "fatherhood", "parenting"])
def _(S):
    cx = 7
    return (lp(S, cx, 9.0) + [beard(cx, 9.0, 2.3, 5.2)]
            + [shell(rect(12.8, 16.4, 9.4, 4.2, 2.1)), shell(circle(15.4, 13.4, 1.9))])


@icon("mother-and-child", CAT, "Woman holding the hand of a small child standing beside her",
      tags=["mum", "mom", "mother", "kid", "parent and child", "motherhood", "family"])
def _(S):
    cx = 7
    return lp(S, cx, 9.0) + [solid(circle(cx, 4.6, 1.6))] + child(S, 17.5, 12.5) + [line(seg(11.2, 18.6, 14.6, 18.6))]


@icon("father-and-child", CAT, "Man holding the hand of a small child standing beside him",
      tags=["dad", "father", "papa", "kid", "parent and child", "fatherhood", "family"])
def _(S):
    cx = 7
    return lp(S, cx, 9.0) + [beard(cx, 9.0, 2.3, 5.2)] + child(S, 17.5, 12.5) + [line(seg(11.2, 18.6, 14.6, 18.6))]


@icon("parent-and-teen", CAT, "Adult figure with an arm around a slightly shorter teen in a hoodie",
      tags=["parent", "teenager", "adolescent", "family", "support", "hoodie", "mentor"])
def _(S):
    return [shell(circle(7.5, 7.8, 2.9)), shell(bust_d(S, 7.5, 13.8, 4.5, 21)),
            shell(circle(17, 11.2, 2.5)), shell(bust_d(S, 17, 15.6, 3.8, 21)),
            detail(poly([(14.6, 16), (17, 18.6), (19.4, 16)], r=S.r * 0.5)),
            line(seg(12, 15, 14, 15))]


@icon("grandparent-and-grandchild", CAT, "Older figure with glasses and a cane holding the hand of a small child",
      tags=["grandma", "grandpa", "grandmother", "grandfather", "elder", "grandkid", "family"])
def _(S):
    cx = 9.5
    return ([shell(circle(cx, 8.5, 3.0)), shell(bust_d(S, cx, 14.5, 4.2, 21)), mark(rect(cx - 3.2, 7.5, 6.4, 1.3, 0.5)),
             line("M2.4 21V15.8A1.7 1.7 0 0 1 5.8 15.8")]
            + child(S, 19.2, 12.5) + [line(seg(13.7, 18.6, 16.2, 18.6))])


@icon("mountain-guide", CAT, "Figure with a coiled rope over the shoulder pointing up at a peak",
      tags=["alpine guide", "climbing guide", "mountaineering", "rope", "summit", "expedition leader", "trek leader"])
def _(S):
    cx = 7
    return (lp(S, cx, 10.0)
            + [detail(seg(cx - 4.2, 16.2, cx + 1.8, 21)), detail(seg(cx - 2.4, 15.4, cx + 3.6, 20.2)),
               line(poly([(cx + 3.6, 16.6), (13, 12.6)])),
               line(poly([(13.5, 10.5), (17.8, 3.8), (22, 10.5)], r=S.r * 0.4)), line(poly([(15.8, 7.4), (17.8, 9), (19.8, 7.4)]))])


@icon("jester", CAT, "Figure in a three pointed hat with bells on the tips holding a scepter",
      tags=["fool", "court jester", "clown", "medieval", "entertainer", "bells", "scepter"])
def _(S):
    cx, hy = 8, 11.6
    hat_p = poly([(cx - 4, 8.6), (cx - 5, 4.6), (cx - 2.2, 6.2), (cx, 3.8), (cx + 2.2, 6.2), (cx + 5, 4.6), (cx + 4, 8.6)],
                 closed=True, r=S.r * 0.3)
    return (head(cx, hy, 8.6, hat_p)
            + [dot(cx - 5, 3.4, 1.1), dot(cx, 2.6, 1.1), dot(cx + 5, 3.4, 1.1),
               shell(bust_d(S, cx, 17.2, 4.5)),
               line(seg(18, 21, 18, 11)), shell(circle(18, 8.6, 2.4))])

