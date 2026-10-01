"""TypeIcon Core: nautical (batch 002): ship parts, anchors, sails, sailing kit, navigation, flags and diving."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "nautical"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def rot(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def flip(d):
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


def wave(y, x0=2.0, x1=22.0, a=1.5, w=4.0):
    """Sea line: alternating half-waves from x0 to x1."""
    n = int(round((x1 - x0) / w))
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        d += f"q{fmt(w / 2)} {fmt(-a if i % 2 == 0 else a)} {fmt(w)} 0" if i == 0 else f"t{fmt(w)} 0"
    return d


# ============================================================================ ship parts

@icon("deck-swab", CAT, "Long-handled swab with a thick bundle of rope strands",
      tags=["swab", "mop", "deck", "clean", "ship", "rope", "sailor"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 12)),
        shell(poly([(9.5, 12), (14.5, 12), (19, 21), (5, 21)], closed=True, r=S.r)),
        detail(seg(10.5, 15.5, 9.5, 19.5)),
        detail(seg(13.5, 15.5, 14.5, 19.5)),
    ]


@icon("bulbous-bow", CAT, "Side view of a ship bow with a rounded bulb below the waterline",
      tags=["ship", "bow", "hull", "bulb", "vessel", "naval architecture", "waterline"])
def _(S):
    hull = "M2.5 4.5H19L18 10.5C22 10.5 22.5 16.5 17.5 16.5H2.5Z"
    if S.name == "line":
        hull = "M2.5 4.5H19.5L18 10.5C22.5 10.5 22.5 16.5 17.5 16.5H2.5Z"
    return [shell(hull), line(wave(20.5, 2.5, 22.5, 1.25, 4))]


@icon("yardarm", CAT, "Top of a ship mast with a horizontal yard and lift lines from its tips",
      tags=["mast", "yard", "rigging", "sailing ship", "spar", "lifts", "ship"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 21.5)),
        line(seg(2.5, 9, 21.5, 9)),
        line(poly([(3, 9), (12, 3.5), (21, 9)])),
    ]


@icon("bowsprit", CAT, "Front of a sailing ship with a long spar angling forward and a stay running to it",
      tags=["ship", "spar", "jib stay", "bow", "sailing ship", "rigging", "prow"])
def _(S):
    return [
        shell(poly([(2, 15), (11, 15), (14, 15), (11, 21), (2, 21)], closed=True, r=S.r)),
        line(seg(11, 15, 22, 9)),
        line(seg(7, 3, 7, 15)),
        line(seg(7, 3.5, 22, 9)),
    ]


@icon("anchor-chain", CAT, "Heavy chain of oval stud links running diagonally",
      tags=["chain", "anchor", "link", "stud link", "ship", "mooring", "heavy"])
def _(S):
    parts = []
    for (x, y) in [(6.5, 17.5), (12, 12), (17.5, 6.5)]:
        if S.name == "line":
            link = poly([(x - 5, y), (x - 3, y - 3), (x + 3, y - 3), (x + 5, y), (x + 3, y + 3), (x - 3, y + 3)], closed=True)
        else:
            link = ellipse(x, y, 5, 3)
        parts.append(line(rot(link, -45, x, y)))
        parts.append(line(rot(seg(x, y - 3, x, y + 3), -45, x, y)))
    return parts


@icon("anchor-windlass", CAT, "Deck winch with a drum and a notched chain wheel feeding anchor chain",
      tags=["windlass", "capstan", "winch", "chain", "anchor", "deck", "ship"])
def _(S):
    return [
        shell(rect(2.5, 6, 7, 9, min(S.R, 2))),
        line(seg(9.5, 10.5, 11.5, 10.5)),
        shell(poly([(16.5 + 5 * math.cos(math.radians(a)), 10.5 + 5 * math.sin(math.radians(a))) for a in range(22, 382, 45)], closed=True, r=S.r)),
        dot(16.5, 10.5, 1.5),
        line(seg(6, 15, 6, 21)),
        line(seg(16.5, 15.5, 16.5, 21)),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("watertight-door", CAT, "Oval ship door with a hand wheel and lever dogs around its edge",
      tags=["bulkhead", "door", "hatch", "ship", "naval", "sealed", "compartment"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 13, 19, L(S, 4.5, 6))),
        detail(circle(12, 12, 3)),
        line(seg(2.5, 7, 5.5, 7)), line(seg(2.5, 17, 5.5, 17)),
        line(seg(18.5, 7, 21.5, 7)), line(seg(18.5, 17, 21.5, 17)),
    ]


@icon("wheelhouse", CAT, "Small boxy cabin on a boat deck with a wide front window and a mast on its roof",
      tags=["pilothouse", "bridge", "cabin", "boat", "helm", "ship", "captain"])
def _(S):
    body = poly([(2, 7), (22, 7), (22, 10), (19.5, 10), (19.5, 21), (4.5, 21), (4.5, 10), (2, 10)], closed=True, r=S.r * 0.5)
    return [
        shell(body),
        detail(rect(7.5, 13, 9, 4, 0)),
        line(seg(12, 2, 12, 7)),
    ]


@icon("bow-thruster", CAT, "Ship bow with a round tunnel through the hull and a small propeller inside",
      tags=["thruster", "ship", "maneuvering", "hull", "tunnel", "propeller", "bow"])
def _(S):
    return [
        shell(poly([(2.5, 4.5), (20, 4.5), (19.5, 10), (15.5, 20), (2.5, 20)], closed=True, r=S.r)),
        detail(circle(9.5, 12.5, 4)),
        dot(9.5, 12.5, 1.25),
    ]


@icon("ducted-propeller", CAT, "Propeller enclosed in a short round nozzle ring beside a rudder",
      tags=["nozzle", "propeller", "thruster", "ship", "rudder", "screw", "duct"])
def _(S):
    return [
        line(ellipse(9.5, 12, 5.5, 8.5)), dot(9.5, 12, 1.5),
        line(seg(9.5, 12, 9.5, 8)), line(seg(9.5, 12, 6.3, 14.5)), line(seg(9.5, 12, 12.7, 14.5)),
        shell(rect(17.5, 4, 4, 16, min(S.R, 1.5))),
    ]


@icon("azimuth-thruster", CAT, "Pod drive hanging below a hull on a strut with a propeller at its front",
      tags=["pod drive", "thruster", "propulsion", "ship", "propeller", "steerable"])
def _(S):
    pod = union(rect(6.5, 14.5, 13, 5.5, 2.75), rect(10.5, 3.5, 4, 12, 0))
    return [line(seg(2, 3.5, 22, 3.5)), shell(pod), line(seg(3, 11.5, 3, 22))]


@icon("deadeye", CAT, "Round wooden block with three holes in a triangle and a rope lashed below it",
      tags=["block", "rigging", "wooden", "lanyard", "sailing ship", "shroud", "rope"])
def _(S):
    return [
        shell(circle(12, 10, 8)),
        dot(12, 6.75, 1.5), dot(8.9, 12.2, 1.5), dot(15.1, 12.2, 1.5),
        line("M12 18V22"),
    ]


@icon("belaying-pin", CAT, "Wooden pin shaped like a small club standing in a rail",
      tags=["pin", "rail", "rigging", "rope", "cleat", "sailing ship", "wooden"])
def _(S):
    pin = "M10.5 3.5C10.5 2 13.5 2 13.5 3.5L13 6.5C15 8 15 11 14 14.5V21H10V14.5C9 11 9 8 11 6.5Z"
    return [
        shell(pin),
        line(seg(2, 16, 10, 16)), line(seg(14, 16, 22, 16)),
    ]


@icon("ratlines", CAT, "Two slanting shroud ropes joined by short horizontal rungs like a rope ladder",
      tags=["shrouds", "rope ladder", "rigging", "mast", "climb", "sailing ship", "ratline"])
def _(S):
    xl = lambda y: 3 + (21 - y) / 18 * 6
    parts = [line(poly([(3, 21), (9, 3), (15, 3), (21, 21)], r=S.r * 0.5))]
    for y in (8, 12.5, 17):
        parts.append(line(seg(xl(y), y, 24 - xl(y), y)))
    return parts


@icon("draft-marks", CAT, "Ship hull side with a vertical scale of marks above the waterline",
      tags=["draught", "draft", "hull", "waterline", "load line", "scale", "ship", "depth"])
def _(S):
    return [
        shell(poly([(3, 3.5), (20, 3.5), (17.5, 16.5), (3, 16.5)], closed=True, r=S.r)),
        detail(seg(8, 6.5, 8, 13.5)),
        detail(seg(8, 6.5, 11.5, 6.5)),
        detail(seg(8, 10, 11.5, 10)),
        detail(seg(8, 13.5, 11.5, 13.5)),
        line(wave(20.5, 2.5, 22.5, 1.25, 4)),
    ]


@icon("companionway", CAT, "Steep narrow ladder with handrails leading down through an open deck hatch",
      tags=["ladder", "stairs", "hatch", "below deck", "boat", "cabin", "steps"])
def _(S):
    xl = lambda y: 8 - 3 * (y - 6) / 15
    parts = [line(seg(2, 5.5, 8, 5.5)), line(seg(16, 5.5, 22, 5.5)),
             line(seg(8, 5.5, 5, 21)), line(seg(16, 5.5, 19, 21))]
    for y in (10, 14.5, 19):
        parts.append(line(seg(xl(y), y, 24 - xl(y), y)))
    return parts


@icon("gimbal-lamp", CAT, "Lantern hung inside a swinging ring so it stays upright when the boat tilts",
      tags=["lantern", "oil lamp", "gimbal", "boat", "cabin", "light", "ship"])
def _(S):
    return [
        line(seg(12, 2, 12, 4.5)),
        line(circle(12, 13, 8.5)),
        shell(poly([(10, 9), (14, 9), (15, 17), (9, 17)], closed=True, r=S.r * 0.5)),
        dot(12, 13.5, 1.0),
    ]


@icon("sailboat-keel", CAT, "Sailboat hull with a sail, a deep narrow fin keel and a heavy bulb at its tip",
      tags=["keel", "sailboat", "ballast", "hull", "fin keel", "bulb", "yacht"])
def _(S):
    hull = poly([(2, 10), (22, 10), (19, 14), (5, 14)], closed=True, r=S.r)
    keel = rect(10.5, 13, 3, 6.5, 0)
    bulb = ellipse(12, 19.5, 3.5, 1.75)
    return [line(seg(11.5, 2, 11.5, 10)), solid(poly([(12, 2), (12, 8), (4.5, 8)], closed=True)), shell(union(hull, keel, bulb))]


@icon("stern-gallery", CAT, "Back of an old sailing ship with rows of windows under a lantern on top",
      tags=["stern", "galleon", "sailing ship", "windows", "transom", "captain cabin", "old ship"])
def _(S):
    body = poly([(3, 8), (21, 8), (20, 16), (17, 21), (7, 21), (4, 16)], closed=True) if S.name == "line" else "M3 8H21L20 15C19.5 18 17 21 12 21C7 21 4.5 18 4 15Z"
    parts = [solid(poly([(10, 7), (10.5, 3), (13.5, 3), (14, 7)], closed=True)), shell(body)]
    for x in (6, 10.5, 15):
        parts.append(Part("dot", rect(x, 11, 3, 2.5, 0)))
    for x in (7.5, 13.5):
        parts.append(Part("dot", rect(x, 16, 3, 2.5, 0)))
    return parts


@icon("boat-steering-console", CAT, "Center console of a small boat with a wheel, a throttle lever and a windscreen",
      tags=["helm", "steering wheel", "console", "boat", "throttle", "dashboard", "windscreen"])
def _(S):
    return [
        line(poly([(5, 12), (6.5, 4), (17.5, 4), (19, 12)], r=S.r * 0.5)),
        shell(rect(3, 12, 18, 9, min(S.R, 2))),
        detail(circle(8.5, 16.5, 2.5)),
        detail(seg(16, 18.5, 17.5, 15.5)),
    ]


@icon("marine-throttle", CAT, "Boat throttle control box with a single lever angled forward",
      tags=["throttle", "gear shift", "lever", "boat", "engine control", "remote control", "marine"])
def _(S):
    return [
        shell(rect(4, 12, 16, 9, min(S.R, 2.5))),
        line(seg(10, 12, 16.5, 4.5)),
        dot(17.5, 3.5, 2.0),
        detail(seg(8, 16.5, 16, 16.5)),
    ]


@icon("grapnel-anchor", CAT, "Small anchor with a straight shank and four curved tines spread like a claw",
      tags=["grapnel", "grappling hook", "anchor", "claw", "boat", "dinghy", "hook"])
def _(S):
    return [
        line(circle(12, 4.25, 2)),
        line(seg(12, 6.25, 12, 16)),
        line("M12 16C9 16.5 5.5 15 4 9"),
        line("M12 16C15 16.5 18.5 15 20 9"),
        line("M12 16C11.5 18 10 19.5 8 19.5"),
        line("M12 16C12.5 18 14 19.5 16 19.5"),
    ]

@icon("fluke-anchor", CAT, "Flat anchor with two wide triangular flukes on a crossbar at the bottom of the shank",
      tags=["anchor", "fluke", "boat", "mooring", "flat anchor", "hook"])
def _(S):
    return [
        line(circle(12, 3.75, 1.75)),
        line(seg(12, 5.5, 12, 15)),
        line(seg(8, 7.5, 16, 7.5)),
        shell(poly([(10.5, 13), (10.5, 20), (3, 20)], closed=True, r=S.r * 0.5)),
        shell(poly([(13.5, 13), (13.5, 20), (21, 20)], closed=True, r=S.r * 0.5)),
    ]


@icon("plow-anchor", CAT, "Anchor with a pointed plowshare blade hinged at the end of a long shank",
      tags=["plough anchor", "anchor", "plowshare", "boat", "mooring", "blade"])
def _(S):
    return [
        line(circle(12, 3.75, 1.75)),
        line(seg(12, 5.5, 12, 12)),
        shell(poly([(12, 21.5), (3, 13.5), (12, 11.5), (21, 13.5)], closed=True, r=S.r * 0.6)),
        detail(seg(12, 12.5, 12, 19)),
    ]


@icon("mushroom-anchor", CAT, "Anchor with a straight shank ending in an upside-down bowl like a mushroom cap",
      tags=["mooring", "anchor", "dome", "mushroom", "buoy", "permanent mooring", "bowl"])
def _(S):
    cap = L(S, "M3 21C3 13 7 10.5 12 10.5C17 10.5 21 13 21 21Z", "M3 21C3 14 7 10.5 12 10.5C17 10.5 21 14 21 21Z")
    return [line(circle(12, 4.25, 2)), line(seg(12, 6.25, 12, 10.5)), shell(cap)]


@icon("sea-anchor", CAT, "Cone-shaped fabric drogue on bridle lines trailing behind a boat",
      tags=["drogue", "sea anchor", "parachute anchor", "storm", "boat", "heave to", "bridle"])
def _(S):
    return [
        shell(poly([(14, 6), (21.5, 10), (21.5, 14), (14, 18)], closed=True, r=S.r)),
        line("M14 18A2.5 6 0 0 1 14 6"),
        line(seg(3.5, 12, 14, 6)),
        line(seg(3.5, 12, 14, 18)),
        dot(3.5, 12, 1.5),
    ]


@icon("lateen-sail", CAT, "Mast with a long diagonal yard carrying a large triangular sail",
      tags=["sail", "dhow", "felucca", "triangular sail", "mast", "sailing", "yard"])
def _(S):
    return [
        shell(poly([(3.5, 16), (20.5, 3.5), (20.5, 19)], closed=True, r=S.r * 0.6)),
        detail(seg(11, 9, 11, 21.5)),
    ]


@icon("gaff-sail", CAT, "Four-sided sail on a mast with a slanting spar along its top edge and a boom below",
      tags=["sail", "gaff", "mainsail", "mast", "boom", "sailing", "schooner"])
def _(S):
    return [
        line(seg(4, 3, 4, 21.5)),
        shell(poly([(8, 7), (19, 3.5), (21, 19), (8, 19)], closed=True, r=S.r * 0.6)),
    ]


@icon("square-sail", CAT, "Rectangular sail hanging from a horizontal yard, billowing outward",
      tags=["sail", "yard", "square rigger", "viking", "tall ship", "sailing", "canvas"])
def _(S):
    k = L(S, 0.0, 1.2)
    sail = f"M6 5.5H18C{fmt(19.5 + k)} 10 {fmt(20.5 + k)} 15 20 19.5Q12 17.5 4 19.5C{fmt(3.5 - k)} 15 {fmt(4.5 - k)} 10 6 5.5Z"
    return [line(seg(2.5, 3.5, 21.5, 3.5)), shell(sail)]


@icon("jib-sail", CAT, "Small triangular headsail on a forestay running down to the bow of a boat",
      tags=["jib", "headsail", "sail", "forestay", "sailboat", "bow", "genoa"])
def _(S):
    return [
        shell(poly([(14.5, 3.5), (5, 17.5), (14.5, 17.5)], closed=True, r=S.r * 0.6)),
        line(seg(19, 2.5, 19, 21.5)),
        line(seg(2, 21, 16, 21)),
    ]


@icon("reefed-sail", CAT, "Mainsail partly lowered with its bottom bundled along the boom and tied with reef ties",
      tags=["reef", "reefing", "mainsail", "sail", "storm", "boom", "sailing"])
def _(S):
    return [
        line(seg(4, 3, 4, 21.5)),
        shell(poly([(8, 3.5), (17, 13.5), (8, 13.5)], closed=True, r=S.r * 0.6)),
        shell(rect(8, 16, 13, 4.5, min(S.R, 2))),
        detail(seg(12, 16, 12, 20.5)), detail(seg(17, 16, 17, 20.5)),
    ]


@icon("roller-furling-jib", CAT, "Headsail rolled around a forestay into a tube, with a drum at the bottom",
      tags=["furling", "headsail", "jib", "roller furler", "forestay", "sail", "sailboat"])
def _(S):
    return [
        shell(union(rect(8, 2.5, 3.5, 13, min(S.R, 1.75)), rect(6, 15, 7.5, 5.5, min(S.R, 2.5)))),
        shell(poly([(15.5, 4), (21, 19), (15.5, 19)], closed=True, r=S.r * 0.6)),
    ]


@icon("winch-handle", CAT, "L-shaped winch handle with a square drive plug at one end and a round grip at the other",
      tags=["winch", "handle", "crank", "sailing", "grinder", "sheet", "tool"])
def _(S):
    return [
        shell(rect(2.5, 7.5, 5, 5, L(S, 0.3, 1.5))),
        line(seg(7.5, 10, 16.5, 10)),
        shell(rect(16.5, 4, 5, 14, L(S, 1.5, 2.5))),
    ]


@icon("cam-cleat", CAT, "Two toothed cams side by side on a base gripping a rope between them",
      tags=["cleat", "rope", "sheet", "sailing", "cam", "clamp", "dinghy"])
def _(S):
    return [
        shell(poly([(4, 3.5), (8, 3.5), (10, 14), (5, 14)], closed=True, r=S.r * 0.6)),
        shell(poly([(20, 3.5), (16, 3.5), (14, 14), (19, 14)], closed=True, r=S.r * 0.6)),
        shell(rect(3, 16, 18, 5, min(S.R, 2))),
    ]


@icon("masthead-wind-vane", CAT, "Top of a mast with a swinging arrow vane and two small reference tabs",
      tags=["wind vane", "wind direction", "mast", "sailing", "weather vane", "arrow", "masthead"])
def _(S):
    return [
        line(seg(12, 6, 12, 21.5)),
        line(seg(3.5, 4.5, 17, 4.5)),
        solid(poly([(22, 4.5), (16.5, 1.5), (16.5, 7.5)], closed=True)),
        solid(poly([(2.5, 4.5), (2.5, 1.5), (6.5, 4.5)], closed=True)),
        line(poly([(7, 11), (7, 14), (17, 14), (17, 11)], r=S.r * 0.5)),
    ]


@icon("bosuns-chair", CAT, "Seat sling hanging from rope bridle lines and a ring, used to hoist a sailor up a mast",
      tags=["bosun chair", "boatswain", "mast climb", "rigging", "sling seat", "sailing", "hoist"])
def _(S):
    seat = poly([(4, 15), (20, 15), (18, 21), (6, 21)], closed=True) if S.name == "line" else "M4 15H20C20 19 18 21 12 21C6 21 4 19 4 15Z"
    return [
        line(circle(12, 4.5, 2)),
        line(seg(11, 6.3, 4.5, 14.5)),
        line(seg(13, 6.3, 19.5, 14.5)),
        shell(seat),
    ]


@icon("boat-shoes", CAT, "Low moccasin-style shoe seen from the side with a lace running around its top edge",
      tags=["deck shoes", "loafer", "moccasin", "footwear", "sailing", "shoe", "casual"])
def _(S):
    return [
        shell(poly([(2.5, 8), (9, 8), (12, 12), (18, 13), (21.5, 15), (21.5, 18), (2.5, 18)], closed=True, r=S.r)),
        detail(poly([(5.5, 11), (9, 11.5), (11.5, 14.5), (16, 15.5)], r=S.r * 0.5)),
        line(seg(2.5, 20.5, 21.5, 20.5)),
    ]


@icon("boat-bailer", CAT, "Scoop cut from a plastic jug with its handle, used to bail water out of a boat",
      tags=["bailer", "bail", "scoop", "bilge", "water", "dinghy", "jug"])
def _(S):
    return [
        shell(poly([(3, 5), (10, 5), (16, 11), (16, 21), (3, 21)], closed=True, r=S.r)),
        line("M16 12.5C21.5 12.5 21.5 19 16 19"),
    ]


@icon("oarlock", CAT, "U-shaped metal fork on a pin mounted on a boat gunwale with an oar resting in it",
      tags=["rowlock", "oar", "rowing", "boat", "gunwale", "fork", "row"])
def _(S):
    return [
        line("M5.5 3.5V8.5A6.5 6.5 0 0 0 18.5 8.5V3.5"),
        dot(12, 8.5, 2.25),
        line(seg(12, 15, 12, 17)),
        shell(rect(2.5, 17, 19, 4.5, min(S.R, 2))),
    ]


@icon("windvane-steering-gear", CAT, "Upright wind vane on a boat's stern linked to a small rudder blade in the water",
      tags=["self steering", "wind vane", "rudder", "stern", "offshore sailing", "vane gear", "sailboat"])
def _(S):
    return [
        shell(rect(9, 2.5, 6, 8, min(S.R, 2))),
        line(seg(12, 10.5, 12, 14.5)),
        shell(rect(10.5, 14.5, 3, 7, min(S.R, 1.5))),
        line("M2 14q1.5 -1.5 3 0t3 0"),
        line("M16 14q1.5 -1.5 3 0t3 0"),
    ]


@icon("sailing-trapeze", CAT, "Sailor standing straight out from the side of a small dinghy, hung from a wire on the mast",
      tags=["trapeze", "dinghy", "hiking", "sailing", "racing", "wire", "sailor"])
def _(S):
    return [
        line(seg(4, 2.5, 4, 16)),
        line(seg(4, 4, 16, 12.5)),
        shell(poly([(2, 16.5), (13, 16.5), (10.5, 21), (4.5, 21)], closed=True, r=S.r)),
        line(seg(12.5, 12.5, 18.5, 12.5)),
        line(seg(12.5, 12.5, 12.5, 16.5)),
        shell(circle(20.25, 12.5, 1.75)) if False else dot(20.25, 12.5, 1.9),
    ]


@icon("tacking-maneuver", CAT, "Zigzag course up toward the wind arrow, turning at each tack",
      tags=["tacking", "zigzag", "upwind", "sailing", "beating", "course", "wind"])
def _(S):
    return [
        line(poly([(3, 21), (14, 14), (5, 8.5), (13, 3.5)], r=S.r)),
        line(seg(20, 2.5, 20, 15)),
        solid(poly([(20, 21), (17, 14), (23, 14)], closed=True)),
        dot(3, 21, 1.6),
    ]


@icon("kamal", CAT, "Small rectangular board with a knotted string through its center, an old star altitude tool",
      tags=["navigation", "latitude", "celestial", "star altitude", "arab navigation", "string", "knots"])
def _(S):
    return [
        shell(rect(3, 4, 18, 7, L(S, 0.5, 2.5))),
        line(seg(12, 11, 12, 21.5)),
        dot(12, 14.75, 1.5), dot(12, 19.25, 1.5),
    ]


@icon("hand-bearing-compass", CAT, "Handheld compass with a round card window on top of a pistol-style grip",
      tags=["compass", "bearing", "hand compass", "sighting", "navigation", "boat", "heading"])
def _(S):
    return [
        shell(circle(12, 7.5, 5.5)),
        dot(12, 7.5, 1.4),
        line(seg(12, 13, 12, 16)),
        shell(poly([(8.5, 16), (15.5, 16), (16, 22), (8, 22)], closed=True, r=S.r * 0.6)),
    ]


def _star(cx, cy, ro, ri, n=4):
    pts = []
    for i in range(n * 2):
        a = math.radians(-90 + i * 180 / n)
        r = ro if i % 2 == 0 else ri
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return poly(pts, closed=True)


@icon("navigation-plotter", CAT, "Clear square plotting tool with a rotating compass rose disc in the middle",
      tags=["chart plotter", "parallel rules", "chart work", "course plotter", "navigation", "protractor", "ruler"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 17, L(S, 1, 4))),
        detail(circle(12, 12, 5.5)),
        Part("dot", _star(12, 12, 3.6, 1.0)),
    ]


@icon("distress-flare", CAT, "Handheld cylindrical flare with a grip band and bright sparks bursting from its top",
      tags=["flare", "signal", "emergency", "rescue", "sos", "pyrotechnic", "safety"])
def _(S):
    return [
        shell(rect(8.5, 9.5, 7, 12, min(S.R, 2.5))),
        detail(seg(8.5, 17, 15.5, 17)),
        line(seg(12, 6, 12, 2.5)),
        line(seg(8, 7.5, 5.5, 5)),
        line(seg(16, 7.5, 18.5, 5)),
        line(seg(5.5, 10.5, 3, 10.5)) if False else dot(4.5, 10.5, 1.0),
        dot(19.5, 10.5, 1.0),
    ]


@icon("ships-logbook", CAT, "Thick bound book with an anchor on its cover",
      tags=["log", "logbook", "journal", "captain", "voyage", "record", "ship"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, L(S, 1, 3))),
        detail(seg(12, 6.5, 12, 16)),
        detail(seg(9.5, 9, 14.5, 9)),
        detail("M8 13.5A4 4 0 0 0 16 13.5"),
    ]


@icon("ship-inclinometer", CAT, "Curved scale gauge with a hanging pointer showing how far a ship is heeling",
      tags=["clinometer", "heel", "list", "tilt", "roll", "gauge", "ship", "angle"])
def _(S):
    pts = []
    parts = [line("M3 9A9 9 0 0 0 21 9"), line(seg(12, 9, 13.9, 16.2)), dot(12, 9, 1.75)]
    for ang in (45, 90, 135):
        a = math.radians(ang)
        parts.append(line(seg(12 + 9 * math.cos(a), 9 + 9 * math.sin(a), 12 + 11.8 * math.cos(a), 9 + 11.8 * math.sin(a))))
    return parts


@icon("taffrail-log", CAT, "Dial gauge on a stern rail with a line trailing into the water to a small spinning rotor",
      tags=["log", "speed", "distance", "ship log", "rotator", "dial", "navigation"])
def _(S):
    return [
        shell(circle(8, 8, 5.5)),
        detail(seg(8, 8, 10.5, 5.5)),
        line("M11 13.5C14 16 13 19.5 17 19.5"),
        shell(ellipse(19.75, 19.5, 2.25, 1.5)) if S.name == "rounded" else shell(poly([(17.5, 19.5), (19.75, 18), (22, 19.5), (19.75, 21)], closed=True)),
    ]


# ============================================================================ flags and day shapes

@icon("burgee", CAT, "Triangular pennant on a short staff at the top of a mast, flying out to the side",
      tags=["pennant", "flag", "yacht club", "mast", "triangle flag", "sailing", "club flag"])
def _(S):
    return [
        line(seg(4.5, 2.5, 4.5, 21.5)),
        shell(poly([(8, 5), (19.5, 9.5), (8, 14)], closed=True, r=S.r), stroke_miterlimit="2"),
    ]


@icon("swallowtail-burgee", CAT, "Flag with a deep V-shaped notch at its fly end forming two tails, on a short staff",
      tags=["swallow tail", "flag", "pennant", "yacht club", "mast", "sailing", "forked flag"])
def _(S):
    return [
        line(seg(4.5, 2.5, 4.5, 21.5)),
        shell(poly([(8, 4.5), (21.5, 4.5), (15.5, 9.5), (21.5, 14.5), (8, 14.5)], closed=True, r=S.r * 0.6)),
    ]


@icon("commissioning-pennant", CAT, "Very long narrow tapering streamer flying from the top of a mast",
      tags=["pennant", "streamer", "naval", "warship", "flag", "commissioned", "mast"])
def _(S):
    return [
        line(seg(4, 2.5, 4, 21.5)),
        shell("M7 5C10 3.5 12 6.5 15 5.5S19 5 22 6.5C19 8 16.5 8 15 8.5C12 9.5 10 7 7 8.5Z") if S.name == "rounded"
        else shell("M7 4.5L14 6L22 6.5L14 8.5L7 9Z"),
    ]


@icon("dressed-ship", CAT, "Side view of a ship with a line of small signal flags running over the mast from bow to stern",
      tags=["dressing ship", "bunting", "flags", "celebration", "ship", "regatta", "signal flags"])
def _(S):
    parts = [
        shell(poly([(3, 16), (21, 16), (18, 20.5), (6, 20.5)], closed=True, r=S.r)),
        line(seg(12, 4, 12, 16)),
        line(poly([(3, 14), (12, 4), (21, 14)])),
    ]
    for (x, y) in ((5.7, 11), (8.8, 7.6), (15.2, 7.6), (18.3, 11)):
        parts.append(Part("dot", rect(x - 1.2, y + 1.4, 2.4, 2.4, 0)))
    return parts


@icon("anchor-ball", CAT, "Front of a boat with a single round black ball hoisted above the bow",
      tags=["day shape", "anchored", "black ball", "colregs", "ship", "signal", "anchorage"])
def _(S):
    return [
        line(seg(12, 2, 12, 16)),
        solid(circle(12, 8.5, 3.25)),
        shell(poly([(3, 16), (21, 16), (18, 21), (6, 21)], closed=True, r=S.r)),
    ]


@icon("motor-sailing-cone", CAT, "Sailboat mast with a single cone shape hoisted point down in the rigging",
      tags=["day shape", "cone", "motorsailing", "colregs", "sailboat", "signal", "under power"])
def _(S):
    return [
        line(seg(12, 2, 12, 6)),
        shell(poly([(6.5, 6), (17.5, 6), (12, 15)], closed=True, r=S.r * 0.6)),
        line(seg(12, 15, 12, 21.5)),
    ]


@icon("restricted-maneuverability-shapes", CAT, "Vertical line of three day shapes on a mast: a ball, a diamond and a ball",
      tags=["day shapes", "restricted", "colregs", "signal", "ball diamond ball", "ship", "rules of the road"])
def _(S):
    return [
        line(seg(12, 2, 12, 22)),
        solid(circle(12, 4.75, 2.75)),
        solid(poly([(12, 8.5), (15.5, 12), (12, 15.5), (8.5, 12)], closed=True)),
        solid(circle(12, 19.25, 2.75)),
    ]


@icon("not-under-command-shapes", CAT, "Two round black balls hoisted one above the other on a mast line",
      tags=["day shapes", "not under command", "two balls", "colregs", "signal", "ship", "disabled"])
def _(S):
    return [
        line(seg(12, 2, 12, 22)),
        solid(circle(12, 6.75, 3.5)),
        solid(circle(12, 17, 3.5)),
    ]


# ============================================================================ diving

@icon("buoyancy-compensator", CAT, "Inflatable diving vest with shoulder straps, a waist strap and a hose at the left shoulder",
      tags=["bcd", "dive vest", "scuba", "diving", "inflator", "jacket", "buoyancy"])
def _(S):
    return [
        shell(poly([(6.5, 3), (10, 3), (12, 6.5), (14, 3), (17.5, 3), (20, 8), (19, 21), (5, 21), (4, 8)], closed=True, r=S.r * 0.6)),
        detail(seg(5, 15, 19, 15)),
        Part("dot", rect(10.5, 13.5, 3, 3, 0)),
        line("M6.5 3.5C2 2.5 1.5 8.5 3 10"),
    ]


@icon("dive-knife", CAT, "Dive knife with a sheath strapped around a lower leg by two straps",
      tags=["diving knife", "scuba", "blade", "sheath", "leg strap", "underwater", "cutting tool"])
def _(S):
    return [
        shell(rect(10, 2, 4, 5.5, min(S.R, 1.5))),
        line(seg(8, 9, 16, 9)),
        shell(poly([(8, 12), (16, 12), (15, 21.5), (9, 21.5)], closed=True, r=S.r * 0.6)),
        line(seg(3.5, 14.5, 8, 14.5)), line(seg(16, 14.5, 20.5, 14.5)),
        line(seg(3.5, 19, 8.5, 19)), line(seg(15.5, 19, 20.5, 19)),
    ]


@icon("dive-light", CAT, "Chunky underwater torch with a wide lens head, a thick body and a wrist lanyard",
      tags=["torch", "flashlight", "underwater light", "scuba", "diving", "lamp", "night dive"])
def _(S):
    return [
        shell(poly([(3.5, 6.5), (10, 9), (10, 15), (3.5, 17.5)], closed=True, r=S.r)),
        shell(rect(10, 9, 10, 6, min(S.R, 2))),
        dot(15, 12, 1.0),
        line("M20 12C22.5 12 22.5 19 17 19.5"),
    ]


@icon("dive-slate", CAT, "Small writing board with a clip at the top and a pencil hanging beside it",
      tags=["underwater slate", "notes", "scuba", "diving", "writing board", "communication", "pencil"])
def _(S):
    return [
        shell(rect(3.5, 4, 13, 17, min(S.R, 2.5))),
        Part("solid", rect(7.5, 2, 5, 3, 0)),
        detail(seg(7, 10, 13, 10)), detail(seg(7, 14, 13, 14)),
        line(seg(20, 9, 20, 19)),
        line(seg(16.5, 6.5, 20, 9)),
    ]


@icon("submersible-pressure-gauge", CAT, "Round dial gauge in a rubber boot at the end of a high-pressure hose",
      tags=["spg", "air gauge", "tank pressure", "scuba", "diving", "dial", "hose"])
def _(S):
    return [
        shell(circle(9, 14.5, 7)),
        detail(seg(9, 14.5, 12.5, 10.5)),
        dot(9, 14.5, 1.3),
        line("M13.5 9C16.5 6 14.5 3 21.5 3"),
    ]


@icon("rebreather", CAT, "Backpack unit with two looped breathing hoses running to a single mouthpiece",
      tags=["closed circuit", "diving", "scuba", "breathing", "loop", "technical diving", "hoses"])
def _(S):
    return [
        shell(rect(2.5, 4, 8, 16, min(S.R, 3))),
        line("M10.5 7C16 7 15 10.5 18.5 10.5"),
        line("M10.5 15C16 15 15 12.5 18.5 12.5"),
        shell(rect(17.5, 8.5, 4, 6, min(S.R, 1.5))),
    ]


@icon("dive-reel", CAT, "Spool of guideline on a frame with a pistol grip handle and a winding crank",
      tags=["cave diving", "guideline", "spool", "scuba", "diving", "line reel", "technical"])
def _(S):
    return [
        shell(circle(9.5, 9.5, 7)),
        detail(circle(9.5, 9.5, 2.5)),
        shell(rect(13.5, 14, 5, 8, L(S, 0.5, 2.5))),
    ]


@icon("full-face-dive-mask", CAT, "Diving mask covering the whole face in one piece, with a regulator bump at the mouth",
      tags=["scuba", "diving", "face mask", "regulator", "underwater", "full face", "visor"])
def _(S):
    return [
        shell(union(poly([(5, 3), (19, 3), (21.5, 10), (18, 19), (6, 19), (2.5, 10)], closed=True, r=S.r), circle(12, 19, 3))),
        detail(rect(6.5, 7, 11, 5, L(S, 1, 2.5))),
    ]


@icon("atmospheric-diving-suit", CAT, "Bulky hard-shell diving suit with a domed viewport head, jointed limbs and pincer hands",
      tags=["hard suit", "deep sea", "diving", "pressure suit", "underwater", "robot suit", "exosuit"])
def _(S):
    return [
        shell(circle(12, 5.5, 3.5)),
        dot(12, 5.5, 1.3),
        shell(rect(7.5, 10.5, 9, 6.5, min(S.R, 2.5))),
        line("M7.5 12L4 15L4 18"),
        line("M16.5 12L20 15L20 18"),
        line("M2.5 21L4 18L5.5 21"),
        line("M18.5 21L20 18L21.5 21"),
        line(seg(10, 17, 10, 21.5)),
        line(seg(14, 17, 14, 21.5)),
    ]


@icon("monofin", CAT, "Single wide tail-shaped fin with two foot pockets side by side",
      tags=["fin", "freediving", "swimming", "mermaid", "flipper", "monofin", "underwater"])
def _(S):
    body = ("M8 2.5H16V9C19.5 11 22 15 21.5 21C18 19 15 19.5 12 21C9 19.5 6 19 2.5 21C2 15 4.5 11 8 9Z" if S.name == "rounded"
            else "M8 2.5H16V9L21.5 13L21.5 21L12 19.5L2.5 21L2.5 13L8 9Z")
    return [shell(body), detail(seg(12, 3.5, 12, 8.5))]


@icon("hookah-dive-compressor", CAT, "Small compressor on a floating ring with a long air hose running down to a diver",
      tags=["surface supplied", "hookah", "air compressor", "diving", "snorkel", "hose", "float"])
def _(S):
    return [
        shell(rect(9, 1.5, 6, 4, L(S, 0.3, 1.5))),
        line(ellipse(12, 9, 9, 3)),
        line("M12 12V15C12 17 15 16.5 15 19"),
        dot(15, 20, 1.6),
    ]


@icon("underwater-habitat", CAT, "Cylindrical seafloor laboratory on legs with round portholes and an entry shaft below",
      tags=["seafloor", "lab", "aquanaut", "saturation", "research", "ocean", "porthole"])
def _(S):
    return [
        shell(rect(3, 4, 18, 11, L(S, 3, 5.5))),
        dot(7.5, 9.5, 1.4), dot(12, 9.5, 1.4), dot(16.5, 9.5, 1.4),
        line(seg(12, 15, 12, 21.5)),
        line(seg(6, 15, 4, 21)),
        line(seg(18, 15, 20, 21)),
    ]


@icon("diver-ok-signal", CAT, "Diver figure with one arm curved over the top of the head, the OK signal",
      tags=["scuba", "diving", "hand signal", "ok", "all good", "underwater", "communication"])
def _(S):
    return [
        shell(circle(10, 8.5, 2.25)),
        line("M11 12.5C17.5 12 18 4.5 10 4"),
        line(seg(10, 10.75, 10, 15.5)),
        line(seg(10, 12.5, 5, 15.5)),
        line(seg(10, 15.5, 7, 21.5)),
        line(seg(10, 15.5, 13, 21.5)),
    ]


@icon("longline-fishing", CAT, "Horizontal fishing line held up by floats with short lines hanging down, each ending in a hook",
      tags=["fishing", "longline", "hooks", "floats", "commercial fishing", "line", "tuna"])
def _(S):
    return [
        line(seg(2, 6, 22, 6)),
        dot(8, 3.4, 1.75), dot(16, 3.4, 1.75),
        line("M4.5 6V17A1.5 1.5 0 0 0 7.5 17"),
        line("M11.5 6V17A1.5 1.5 0 0 0 14.5 17"),
        line("M18.5 6V17A1.5 1.5 0 0 0 21.5 17"),
    ]

@icon("jackline-tether", CAT, "Safety strap with a clip at each end, one on a harness ring and one hooked to a deck line",
      tags=["safety line", "harness", "lifeline", "man overboard", "sailing", "clip", "strap"])
def _(S):
    return [
        line(circle(5.5, 5.5, 2.75)),
        line("M8 7C13 8 9 13 15 13.5"),
        line(rect(14, 12, 6, 8, L(S, 1.5, 3))),
        line(seg(2, 19, 22, 19)),
    ]
