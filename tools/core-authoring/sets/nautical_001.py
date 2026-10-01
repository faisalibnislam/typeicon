"""TypeIcon Core: nautical (batch nautical_001).

Buoys, navigation marks, lights, dock and deck hardware, and rope work. Objects are drawn upright or from the
side; water is a gentle wave line.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, polar

CAT = "nautical"


def water(y=20.5, x0=2, x1=22, w=4, c=1.6):
    """Wave line from x0 to x1 (x1 - x0 must be a multiple of w)."""
    n = int(round((x1 - x0) / w))
    return f"M{fmt(x0)} {fmt(y)}q{fmt(w / 2)} {fmt(-c)} {fmt(w)} 0" + f"t{fmt(w)} 0" * (n - 1)


def rr(S, cap):
    return min(S.R, cap)


# ============================================================================ buoys

@icon("can-buoy", CAT, "Flat topped cylindrical buoy floating upright on the water.",
      tags=["can buoy", "channel marker", "lateral mark", "buoy", "navigation", "harbor"])
def _(S):
    return [
        shell(rect(8, 4, 8, 11, rr(S, 1.5))),
        detail(seg(8, 9.5, 16, 9.5)),
        line(water(19.5)),
    ]


@icon("nun-buoy", CAT, "Cone topped buoy with a pointed top floating on the water.",
      tags=["nun buoy", "conical buoy", "channel marker", "lateral mark", "buoy", "navigation"])
def _(S):
    return [
        shell(poly([(12, 3), (17, 15), (7, 15)], closed=True, r=S.r * 0.6)),
        detail(seg(9.6, 10, 14.4, 10)),
        line(water(19.5)),
    ]


@icon("spar-buoy", CAT, "Long thin pole shaped buoy standing upright in the water.",
      tags=["spar buoy", "pole buoy", "channel marker", "navigation", "buoy", "marker"])
def _(S):
    return [
        shell(rect(10, 2.5, 4, 14, rr(S, 1.5))),
        detail(seg(10, 8, 14, 8)),
        line(water(19.5, 2, 10, 4)), line(water(19.5, 14, 22, 4)),
        line(seg(12, 19.5, 12, 22)),
    ]


@icon("bell-buoy", CAT, "Buoy with an open frame tower holding a hanging bell.",
      tags=["bell buoy", "sound buoy", "channel marker", "navigation", "bell", "warning"])
def _(S):
    return [
        shell(poly([(5, 18), (7, 14.5), (17, 14.5), (19, 18)], closed=True, r=S.r * 0.6)),
        line(poly([(7.5, 14.5), (10, 3.5), (14, 3.5), (16.5, 14.5)], r=S.r * 0.6)),
        solid("M11.5 5v3.2q-1.3.7-1.3 3.8h3.6q0-3.1-1.3-3.8V5z"),
        line(water(21.2)),
    ]


@icon("whistle-buoy", CAT, "Buoy with a short whistle pipe on top and sound lines beside it.",
      tags=["whistle buoy", "sound buoy", "channel marker", "navigation", "warning", "buoy"])
def _(S):
    return [
        shell(rect(10.5, 8, 3, 6, rr(S, 1.2))),
        shell(rect(6.5, 14, 11, 5, rr(S, 1.5))),
        line(seg(12, 2.5, 12, 5)), line(seg(8, 3.5, 9.3, 5.5)), line(seg(16, 3.5, 14.7, 5.5)),
        line(water(21.6, 2, 22, 4, 1.2)),
    ]


@icon("mooring-buoy", CAT, "Round ball buoy on the water with a ring on top and a chain below.",
      tags=["mooring ball", "mooring buoy", "anchorage", "boat", "chain", "ring"])
def _(S):
    return [
        shell(circle(12, 10.5, 5)),
        line(seg(12, 5.5, 12, 3)),
        line(water(17.5, 2, 6, 4)), line(water(17.5, 18, 22, 4)),
        line(seg(12, 15.5, 12, 17.5)), line(seg(12, 19.5, 12, 22)),
    ]


@icon("isolated-danger-mark", CAT, "Pillar buoy with a central band and two stacked spheres on top.",
      tags=["isolated danger", "danger mark", "cardinal", "navigation", "warning", "buoy", "hazard"])
def _(S):
    return [
        solid(circle(12, 3.6, 1.5)), solid(circle(12, 7.4, 1.5)),
        shell(rect(8, 11, 8, 7, rr(S, 1.5))),
        detail(seg(8, 14.5, 16, 14.5)),
        line(water(21.2)),
    ]


@icon("safe-water-mark", CAT, "Round striped buoy with a single sphere on a short pole.",
      tags=["safe water", "fairway mark", "mid channel", "navigation", "buoy", "sphere"])
def _(S):
    return [
        solid(circle(12, 3.6, 1.5)),
        line(seg(12, 5, 12, 6.5)),
        shell(circle(12, 11.5, 5)),
        detail(ellipse(12, 11.5, 2, 5)),
        line(water(20.5)),
    ]


@icon("cardinal-mark", CAT, "Pillar buoy with two cones stacked on top, one pointing up and one down.",
      tags=["cardinal buoy", "north mark", "navigation", "topmark", "buoy", "compass"])
def _(S):
    return [
        solid(poly([(12, 2), (14.6, 5.4), (9.4, 5.4)], closed=True)),
        solid(poly([(9.4, 6.6), (14.6, 6.6), (12, 10)], closed=True)),
        shell(rect(8, 12, 8, 6, rr(S, 1.5))),
        line(water(21.2)),
    ]


@icon("special-mark-buoy", CAT, "Pillar buoy topped with a single cross shaped mark.",
      tags=["special mark", "cross topmark", "navigation", "buoy", "yellow buoy", "marker"])
def _(S):
    return [
        line(seg(9.6, 2.8, 14.4, 7.6)), line(seg(14.4, 2.8, 9.6, 7.6)),
        shell(rect(8, 11, 8, 7, rr(S, 1.5))),
        detail(seg(8, 14.5, 16, 14.5)),
        line(water(21.2)),
    ]


@icon("lobster-buoy", CAT, "Small bullet shaped float with a spindle stick through it and a rope trailing down.",
      tags=["pot buoy", "trap float", "crab pot", "fishing", "float", "rope"])
def _(S):
    body = "M8 14V9.5Q8 5 12 5Q16 5 16 9.5V14Z" if S.name == "line" else "M8 14V9.5Q8 5 12 5Q16 5 16 9.5V14Q16 15 15 15H9Q8 15 8 14Z"
    return [
        shell(body),
        line(seg(12, 2.2, 12, 5)),
        detail(seg(8, 10, 16, 10)),
        line("M12 15q-2 2 0 3.5t0 3.5"),
    ]


@icon("surface-marker-buoy", CAT, "Tall narrow inflatable tube floating upright with a thin line going down.",
      tags=["smb", "dive float", "safety sausage", "diving", "marker buoy", "signal tube"])
def _(S):
    return [
        shell(rect(10, 3, 4, 12, 2)),
        line(water(17.5, 2, 10, 4)), line(water(17.5, 14, 22, 4)),
        line(seg(12, 15, 12, 22)),
    ]


@icon("racing-mark-buoy", CAT, "Inflatable pyramid shaped racing mark floating on the water with an anchor line below.",
      tags=["race buoy", "regatta", "sailing race", "course mark", "inflatable", "marker"])
def _(S):
    return [
        shell(poly([(12, 3.5), (19, 15), (5, 15)], closed=True, r=S.r * 0.6)),
        detail(seg(12, 4.5, 12, 15)),
        line(water(18.5, 2, 10, 4)), line(water(18.5, 14, 22, 4)),
        line(seg(12, 20.5, 12, 22)),
    ]


@icon("daybeacon", CAT, "Single post standing in the water carrying a flat triangular sign board on top.",
      tags=["day beacon", "day marker", "channel marker", "navigation", "piling", "sign"])
def _(S):
    return [
        shell(poly([(12, 3), (17, 10), (7, 10)], closed=True, r=S.r * 0.6)),
        line(seg(12, 10, 12, 19)),
        line(water(20.5)),
    ]


# ============================================================================ lights

@icon("boat-navigation-lights", CAT, "Top view of a boat bow with a lamp on each side, each casting a wedge of light outward.",
      tags=["nav lights", "port and starboard", "running lights", "boat lights", "night sailing", "bow"])
def _(S):
    return [
        shell(poly([(12, 5), (16, 10), (16, 21), (8, 21), (8, 10)], closed=True, r=S.r * 0.7)),
        shell(poly([(7, 11.5), (2.5, 6.5), (2.5, 16.5)], closed=True, r=S.r * 0.4)),
        shell(poly([(17, 11.5), (21.5, 6.5), (21.5, 16.5)], closed=True, r=S.r * 0.4)),
        dot(8, 11.5, 1.2), dot(16, 11.5, 1.2),
    ]


@icon("ship-lantern", CAT, "Metal ship's lantern with a domed cap, a glass globe inside a guard and a carrying ring.",
      tags=["lantern", "oil lamp", "storm lantern", "hurricane lamp", "ship light", "lamp"])
def _(S):
    return [
        line("M10 5.5V4.3a2 2 0 0 1 4 0V5.5"),
        shell(poly([(6.5, 9), (9, 5.5), (15, 5.5), (17.5, 9)], closed=True, r=S.r * 0.6)),
        line(seg(8, 9, 8, 18)), line(seg(16, 9, 16, 18)),
        shell(rect(6.5, 18, 11, 3, rr(S, 1.2))),
        solid(circle(12, 13.5, 2.4)),
    ]


@icon("range-lights", CAT, "Two lights on posts, a short one in front and a tall one behind, used to line up a channel.",
      tags=["leading lights", "transit lights", "channel lights", "harbor entrance", "navigation", "posts"])
def _(S):
    return [
        solid(circle(17, 5, 2.2)), line(seg(17, 7, 17, 19)),
        solid(circle(8, 11, 2.2)), line(seg(8, 13, 8, 19)),
        line(water(21.2)),
    ]


@icon("sector-light", CAT, "Small light tower casting three fan shaped beams in different directions over the water.",
      tags=["sector lighthouse", "colored sectors", "beacon", "coastal light", "navigation", "beam"])
def _(S):
    cx, cy = 12, 11.5
    out = [
        shell(poly([(9.5, 21), (10.5, 14), (13.5, 14), (14.5, 21)], closed=True, r=S.r * 0.5)),
        solid(circle(cx, cy, 1.8)),
    ]
    for a in (-160, -90, -20):
        p = polar(cx, cy, 4.5, a)
        q = polar(cx, cy, 9, a)
        out.append(line(seg(p[0], p[1], q[0], q[1])))
    return out


@icon("screw-pile-lighthouse", CAT, "Small cottage with a lantern on its roof, standing on thin iron legs above the water.",
      tags=["stilt lighthouse", "offshore light", "iron legs", "lighthouse", "navigation", "beacon"])
def _(S):
    return [
        solid(rect(10.5, 2.5, 3, 3.5)),
        shell(poly([(5.5, 10), (9.5, 6), (14.5, 6), (18.5, 10)], closed=True, r=S.r * 0.5)),
        shell(rect(7.5, 10, 9, 5, rr(S, 1.2))),
        line(seg(9, 15, 8, 19)), line(seg(15, 15, 16, 19)),
        line(water(21.3)),
    ]


def _lattice(y):
    """x of the left leg of the skeleton tower at height y."""
    return 8 + 2.5 * (21 - y) / 14


@icon("skeleton-tower-lighthouse", CAT, "Tall open steel lattice tower tapering upward with a small lantern room at the top.",
      tags=["lattice lighthouse", "steel tower", "open frame", "lighthouse", "navigation", "beacon"])
def _(S):
    zig = [(_lattice(20.5), 20.5), (24 - _lattice(16.5), 16.5), (_lattice(12.5), 12.5), (24 - _lattice(9), 9)]
    return [
        shell(poly([(10.5, 7.5), (10.5, 5), (12, 3), (13.5, 5), (13.5, 7.5)], closed=True, r=S.r * 0.4)),
        line(seg(_lattice(21), 21, 10.5, 7.5)), line(seg(24 - _lattice(21), 21, 13.5, 7.5)),
        line(poly(zig)),
    ]


@icon("caisson-lighthouse", CAT, "Squat round iron base rising from the water like a spark plug, topped by a small tower and lantern.",
      tags=["spark plug lighthouse", "offshore lighthouse", "iron base", "lighthouse", "navigation", "sea light"])
def _(S):
    return [
        shell(poly([(12, 2.5), (15, 6.5), (9, 6.5)], closed=True, r=S.r * 0.4)),
        shell(rect(10, 6.5, 4, 4, 0)),
        shell(poly([(7, 10.5), (17, 10.5), (19, 18), (5, 18)], closed=True, r=S.r * 0.5)),
        line(water(21.2)),
    ]


@icon("pierhead-light", CAT, "Short tapered light tower with a pointed lamp room at the end of a harbor pier standing on posts.",
      tags=["harbor light", "breakwater light", "jetty light", "pier", "navigation", "beacon"])
def _(S):
    return [
        shell(poly([(12, 17.5), (13.5, 9.5), (18.5, 9.5), (20, 17.5)], closed=True, r=S.r * 0.5)),
        shell(poly([(13, 9.5), (16, 3.5), (19, 9.5)], closed=True, r=S.r * 0.4)),
        line(seg(2.5, 17.5, 21, 17.5)),
        line(seg(5, 17.5, 5, 21)), line(seg(9.5, 17.5, 9.5, 21)), line(seg(16, 17.5, 16, 21)),
    ]


@icon("fresnel-lens", CAT, "Beehive shaped lighthouse lens of stacked glass rings around a central lamp, on a base.",
      tags=["lighthouse lens", "beacon lens", "glass rings", "lamp", "optics", "lighthouse"])
def _(S):
    return [
        shell(poly([(7, 18), (7, 10), (9.5, 4.5), (14.5, 4.5), (17, 10), (17, 18)], closed=True, r=S.r * 1.6 + 1)),
        detail(seg(7, 8.5, 17, 8.5)), detail(seg(7, 13.5, 17, 13.5)),
        shell(rect(5, 18, 14, 3, rr(S, 1.2))),
    ]


# ============================================================================ dock and deck hardware

def rotd(d, deg, cx=12.0, cy=12.0):
    from geometry import rotation, transform_path
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


@icon("mooring-bitts", CAT, "Pair of short thick iron posts on a shared base plate with a rope wound around them in a figure eight.",
      tags=["bitts", "bollards", "deck fitting", "mooring post", "rope", "dock"])
def _(S):
    return [
        shell(rect(4, 6, 5, 12, S.R)), shell(rect(15, 6, 5, 12, S.R)),
        shell(rect(2.5, 18, 19, 3, rr(S, 1.2))),
        line(seg(9, 10, 15, 15)), line(seg(9, 15, 15, 10)),
    ]


@icon("fairlead-chock", CAT, "Deck fitting with two curved horns facing each other, forming a slot that guides a rope.",
      tags=["chock", "panama chock", "fairlead", "deck fitting", "rope guide", "mooring"])
def _(S):
    if S.name == "line":
        horn = "M3 19.5V12Q3 6 10 6V9Q7.5 9 7.5 12.5V19.5Z"
        horn2 = "M21 19.5V12Q21 6 14 6V9Q16.5 9 16.5 12.5V19.5Z"
    else:
        horn = "M3 18.5Q3 19.5 4 19.5H6.5Q7.5 19.5 7.5 18.5V12.5Q7.5 9 9.5 9Q10.5 9 10.5 7.5Q10.5 6 9.5 6Q3 6 3 12Z"
        horn2 = "M21 18.5Q21 19.5 20 19.5H17.5Q16.5 19.5 16.5 18.5V12.5Q16.5 9 14.5 9Q13.5 9 13.5 7.5Q13.5 6 14.5 6Q21 6 21 12Z"
    return [shell(horn), shell(horn2)]


@icon("hawsepipe", CAT, "Ship bow seen from the side with an anchor pulled up snug into a round opening in the hull.",
      tags=["hawse pipe", "anchor pocket", "anchor", "bow", "hull", "ship"])
def _(S):
    return [
        shell(poly([(3, 3.5), (11, 3.5), (21.5, 9), (18, 18), (3, 18)], closed=True, r=S.r * 0.7)),
        detail(circle(10.5, 11.5, 4.5)),
        solid(rect(9.5, 9, 2, 6)),
        solid(rect(8, 9.6, 5, 1.6)),
        line(water(21.3)),
    ]


@icon("concrete-tetrapod", CAT, "Chunky concrete block with four stubby legs pointing out in different directions.",
      tags=["tetrapod", "breakwater", "armor unit", "coastal defense", "concrete", "sea defense"])
def _(S):
    return [
        shell(poly([(10, 3), (14, 3), (14, 9.5), (20, 13.5), (19, 20), (13.5, 16.5), (10.5, 16.5), (5, 20), (4, 13.5), (10, 9.5)],
                   closed=True, r=S.r * 0.8)),
        detail(circle(12, 13, 2)),
    ]


@icon("groyne", CAT, "Row of wooden posts and planks running out from the beach into the waves.",
      tags=["groin", "sea defense", "beach", "erosion", "breakwater", "coast"])
def _(S):
    return [
        shell(rect(4, 6, 16, 3.5, rr(S, 1.2))),
        line(seg(7, 9.5, 7, 17)), line(seg(12, 9.5, 12, 17)), line(seg(17, 9.5, 17, 17)),
        line(water(20.5)),
    ]


@icon("sea-wall", CAT, "Curved concrete wall at the shoreline with a big wave curling back off its face.",
      tags=["seawall", "flood defense", "coastal protection", "embankment", "breakwater", "wave"])
def _(S):
    return [
        shell("M15 3H21V21H8Q15 17 15 3Z" if S.name == "line" else "M16 3H20Q21 3 21 4V20Q21 21 20 21H9Q15.5 17 15.5 4.5Q15.5 3 16 3Z"),
        line("M2.5 19C2.5 13 6 10 9.5 10.5S13 14 10.5 14.5"),
    ]


@icon("floating-dry-dock", CAT, "U shaped floating pontoon with high side walls and a ship lifted out of the water inside it.",
      tags=["dry dock", "drydock", "shipyard", "ship repair", "pontoon", "dock"])
def _(S):
    return [
        shell(poly([(3, 6), (7, 6), (7, 14.5), (17, 14.5), (17, 6), (21, 6), (21, 18), (3, 18)], closed=True, r=S.r * 0.5)),
        line(water(21.3)),
        solid(poly([(9.5, 9), (14.5, 9), (13.5, 12), (10.5, 12)], closed=True)),
    ]


@icon("marine-fuel-dock", CAT, "Fuel pump with a hose standing on a wooden pier beside the water.",
      tags=["fuel dock", "gas dock", "boat fuel", "marina", "pump", "diesel"])
def _(S):
    return [
        shell(rect(4, 3.5, 8, 14, rr(S, 1.5))),
        detail(seg(4, 8, 12, 8)),
        line("M12 11H15q2 0 2 2v3.5"),
        line(seg(15.5, 16.5, 18.5, 16.5)),
        line(seg(2.5, 18, 21.5, 18)),
        line(seg(6, 18, 6, 21.5)), line(seg(18, 18, 18, 21.5)),
    ]


@icon("shore-power-pedestal", CAT, "Short post on a marina dock with a power socket, a light on top and a cable running away.",
      tags=["power pedestal", "dock power", "shore power", "marina", "electric hookup", "plug"])
def _(S):
    return [
        dot(12, 3.8, 1.4),
        shell(rect(8, 6.5, 8, 12, rr(S, 1.5))),
        detail(seg(8, 10, 16, 10)),
        dot(12, 14, 1.3),
        line("M16 14.5H19q2 0 2 2v3"),
        line(seg(2.5, 19.5, 21.5, 19.5)),
    ]


@icon("mooring-dolphin", CAT, "Cluster of wooden piles bound together at the top with rope, standing in the water.",
      tags=["dolphin", "piles", "pilings", "mooring post", "harbor", "pier"])
def _(S):
    return [
        line(seg(8, 19.5, 10.5, 3.5)), line(seg(12, 19.5, 12, 3)), line(seg(16, 19.5, 13.5, 3.5)),
        line(seg(9.5, 8, 14.5, 8)),
        line(water(20.5)),
    ]


def _rot(pts, deg=45, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def _rot(pts, deg=45, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


@icon("boat-hook", CAT, "Long pole with a metal tip that has one straight point and one curved hook.",
      tags=["boathook", "docking pole", "pole", "mooring", "rope", "fending"])
def _(S):
    a, b, c, d, f = _rot([(12, 24.5), (12, 6), (12, -0.5), (12, 6), (16.5, 3)])
    cp = _rot([(17, 8)])[0]
    hook = f"M{fmt(d[0])} {fmt(d[1])}Q{fmt(cp[0])} {fmt(cp[1])} {fmt(f[0])} {fmt(f[1])}"
    return [
        line(seg(a[0], a[1], b[0], b[1])),
        line(seg(c[0], c[1], d[0], d[1])),
        line(hook),
    ]


@icon("boat-cradle", CAT, "Boat hull resting out of the water on a frame of padded supports and legs.",
      tags=["boat stand", "boat support", "dry storage", "hull", "shipyard", "boatyard"])
def _(S):
    return [
        line(seg(12, 7, 12, 3)),
        solid(poly([(12, 3), (16, 4.5), (12, 6)], closed=True)),
        shell(poly([(3, 7), (21, 7), (17.5, 13), (6.5, 13)], closed=True, r=S.r * 0.6)),
        line(seg(8, 13, 6, 20.5)), line(seg(16, 13, 18, 20.5)),
        line(seg(2.5, 20.5, 21.5, 20.5)),
    ]


@icon("mooring-ring", CAT, "Heavy iron ring hanging from a bolted plate set into the top of a stone quay wall.",
      tags=["quay ring", "iron ring", "dock ring", "tie up", "harbor", "rope"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 5, S.R)),
        shell(rect(9, 7.5, 6, 3, 0)),
        line(circle(12, 15.5, 5)),
    ]


@icon("liferaft-canister", CAT, "Capsule shaped container split along the middle, held in a cradle on a ship rail.",
      tags=["life raft", "liferaft", "survival", "safety", "emergency", "capsule"])
def _(S):
    rx = 3 if S.name == "line" else 4
    return [
        shell(rect(3, 6.5, 18, 8.5, rx)),
        detail(seg(12, 6.5, 12, 15)),
        line(seg(7, 15, 7, 19)), line(seg(17, 15, 17, 19)),
        line(seg(2.5, 19.5, 21.5, 19.5)),
    ]


@icon("horseshoe-buoy", CAT, "U shaped horseshoe lifebuoy with two bands across its sides.",
      tags=["horseshoe lifebuoy", "life ring", "rescue", "man overboard", "safety", "flotation"])
def _(S):
    cx, cy, R, r = 12, 13, 8.5, 4.3
    a1, a2 = 205, 335
    o1, o2 = polar(cx, cy, R, a1), polar(cx, cy, R, a2)
    i1, i2 = polar(cx, cy, r, a1), polar(cx, cy, r, a2)
    d = (f"M{fmt(o1[0])} {fmt(o1[1])}A{R} {R} 0 1 0 {fmt(o2[0])} {fmt(o2[1])}"
         f"L{fmt(i2[0])} {fmt(i2[1])}A{r} {r} 0 1 1 {fmt(i1[0])} {fmt(i1[1])}Z")
    p, q = polar(cx, cy, r, 135), polar(cx, cy, R, 135)
    p2, q2 = polar(cx, cy, r, 45), polar(cx, cy, R, 45)
    return [
        shell(d),
        detail(seg(p[0], p[1], q[0], q[1])), detail(seg(p2[0], p2[1], q2[0], q2[1])),
    ]


@icon("boat-storage-rack", CAT, "Tall steel rack with three levels, each holding a small boat on its shelf.",
      tags=["dry stack", "boat rack", "marina storage", "boat storage", "shelving", "boatyard"])
def _(S):
    out = [line(seg(3.5, 3, 3.5, 21)), line(seg(20.5, 3, 20.5, 21))]
    for y in (8.5, 14.5, 20.5):
        out.append(line(seg(3.5, y, 20.5, y)))
        out.append(solid(poly([(7.5, y - 3.5), (16.5, y - 3.5), (15, y - 1.2), (9, y - 1.2)], closed=True)))
    return out


@icon("dock-cart", CAT, "Deep tub barrow on a large wheel with a long handle, used to move gear along a marina dock.",
      tags=["dock trolley", "marina cart", "wheelbarrow", "gear cart", "luggage", "trolley"])
def _(S):
    return [
        shell(poly([(8, 8), (20, 8), (18, 14), (10, 14)], closed=True, r=S.r * 0.6)),
        line(seg(8, 8.5, 2.5, 3.5)),
        line(seg(9, 14.5, 6.5, 20.5)),
        shell(circle(15, 17.5, 3)),
    ]


@icon("cargo-hand-hook", CAT, "Short curved steel hook with a T shaped handle, a dockworker's cargo hook.",
      tags=["baling hook", "hay hook", "longshoreman", "docker", "cargo", "hook"])
def _(S):
    return [
        shell(rect(4.5, 17, 15, 4, rr(S, 1.5))),
        line(seg(12, 17, 12, 10)),
        line("M12 10V8Q12 4 16 4Q20 4 20 8V9.5"),
    ]


@icon("mooring-reel", CAT, "Deck mounted spool on a stand with a thick mooring rope wound around its core.",
      tags=["rope reel", "winch", "line drum", "deck equipment", "mooring winch", "ship"])
def _(S):
    return [
        shell(rect(3.5, 3.5, 3.5, 13, rr(S, 1.2))), shell(rect(17, 3.5, 3.5, 13, rr(S, 1.2))),
        shell(rect(7, 6.5, 10, 7, 0)),
        detail(seg(9.5, 6.5, 11, 13.5)), detail(seg(13, 6.5, 14.5, 13.5)),
        line(seg(5, 16.5, 5, 21)), line(seg(19, 16.5, 19, 21)),
        line(seg(2.5, 21, 21.5, 21)),
    ]


@icon("ship-cargo-derrick", CAT, "Ship mast with a long angled boom and a cable from its tip lifting a crate.",
      tags=["cargo boom", "crane", "derrick", "hoist", "loading", "freighter"])
def _(S):
    return [
        line(seg(5.5, 21, 5.5, 3)),
        line(seg(5.5, 17, 17, 6)),
        line(seg(5.5, 3, 17, 6)),
        line(seg(17, 6, 17, 11)),
        shell(rect(13.5, 11, 7, 6, rr(S, 1.2))),
        line(seg(2.5, 21, 21.5, 21)),
    ]


@icon("container-twistlock", CAT, "Metal cone shaped connector with a twist handle, used to lock shipping containers together.",
      tags=["twist lock", "container lock", "corner casting", "lashing", "shipping container", "connector"])
def _(S):
    return [
        shell(poly([(8.5, 9), (10.5, 3), (13.5, 3), (15.5, 9)], closed=True, r=S.r * 0.5)),
        shell(rect(4.5, 9, 15, 4, rr(S, 1.5))),
        shell(rect(9, 13, 6, 5, 0)),
        line(seg(15, 16, 19, 16)),
        solid(circle(20, 16, 1.6)),
    ]


@icon("boat-wake", CAT, "Top view of a small boat moving forward, leaving a V shaped trail of wake lines behind it.",
      tags=["wake", "wash", "speedboat", "boat trail", "water", "motorboat"])
def _(S):
    return [
        shell(poly([(12, 2.5), (15.5, 8), (15.5, 13), (8.5, 13), (8.5, 8)], closed=True, r=S.r * 0.7)),
        detail(seg(8.5, 9, 15.5, 9)),
        line(seg(8.5, 15.5, 3, 21.5)), line(seg(15.5, 15.5, 21, 21.5)),
        line(seg(12, 17, 12, 21.5)),
    ]


@icon("no-wake-zone", CAT, "Round sign with a small boat crossed through by a diagonal bar.",
      tags=["slow zone", "idle speed", "speed limit", "harbor rules", "prohibited", "no wash"])
def _(S):
    return [
        shell(circle(12, 12, 9.5)),
        detail(poly([(6.5, 12.5), (17.5, 12.5), (15.5, 16), (8.5, 16)], closed=True, r=S.r * 0.4)),
        detail(poly([(9.5, 12.5), (10.5, 9), (14, 9), (15, 12.5)])),
        detail(seg(5.5, 5.5, 18.5, 18.5)),
    ]




# ============================================================================ rope work and tools

def _rp(cmds, deg=45):
    """Path from commands with rotated points: ("M", p) ("L", p) ("Q", c, p) ("Z",)."""
    def pt(p):
        q = _rot([p], deg)[0]
        return f"{fmt(q[0])} {fmt(q[1])}"
    out = []
    for c in cmds:
        if c[0] in ("M", "L"):
            out.append(c[0] + pt(c[1]))
        elif c[0] == "Q":
            out.append("Q" + pt(c[1]) + " " + pt(c[2]))
        else:
            out.append("Z")
    return "".join(out)


@icon("marlinspike", CAT, "Long tapered steel spike with a rounded head end, used for opening rope strands.",
      tags=["marlin spike", "splicing tool", "rope tool", "sailor", "knot tool", "spike"])
def _(S):
    return [
        shell(_rp([("M", (9.8, 0)), ("L", (14.2, 0)), ("L", (13, 8)), ("L", (12, 24.5)), ("L", (11, 8)), ("Z",)])) if S.name == "line" else
        shell(_rp([("M", (10.5, 0)), ("Q", (9.8, 0), (9.8, 1)), ("L", (11, 8)), ("L", (12, 24.5)), ("L", (13, 8)),
                   ("L", (14.2, 1)), ("Q", (14.2, 0), (13.5, 0)), ("Z",)])),
        dot(*_rot([(12, 2.8)])[0], 1.0),
    ]


@icon("splicing-fid", CAT, "Smooth tapered wooden cone with a pointed tip and a rounded base, used for opening rope strands.",
      tags=["fid", "rope tool", "splicing", "sailor", "knot tool", "cone"])
def _(S):
    if S.name == "line":
        body = _rp([("M", (8.5, 3.5)), ("L", (15.5, 3.5)), ("L", (12.8, 21)), ("L", (11.2, 21)), ("Z",)])
    else:
        body = _rp([("M", (10, 3)), ("L", (14, 3)), ("Q", (15.8, 3), (15.5, 5)), ("L", (12.8, 20)), ("Q", (12, 22), (11.2, 20)),
                    ("L", (8.5, 5)), ("Q", (8.2, 3), (10, 3)), ("Z",)])
    return [
        shell(body),
        detail(_rp([("M", (9.3, 7.5)), ("L", (14.7, 7.5))])),
    ]


@icon("knot-board", CAT, "Framed board displaying rows of small rope knots on cords.",
      tags=["knot display", "rope knots", "sailor", "scouting", "macrame", "decor"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(6, 9, 18, 9)), detail(seg(6, 15.5, 18, 15.5)),
        dot(9.5, 9, 1.6), dot(14.5, 9, 1.6), dot(9.5, 15.5, 1.6), dot(14.5, 15.5, 1.6),
    ]


@icon("rope-fender", CAT, "Pear shaped fender made of braided rope, hanging from a short rope loop.",
      tags=["boat fender", "bumper", "rope ball", "marina", "dock", "protection"])
def _(S):
    if S.name == "line":
        body = "M9.5 6.5Q9.5 9.5 6.5 11.5Q5 13 5 15.5A7 7 0 0 0 19 15.5Q19 13 17.5 11.5Q14.5 9.5 14.5 6.5Z"
    else:
        body = "M10.5 6.5Q10.5 9.5 7 11.5Q5 13 5 15.5A7 7 0 0 0 19 15.5Q19 13 17 11.5Q13.5 9.5 13.5 6.5Z"
    return [
        line("M10 6.5V4a2 2 0 0 1 4 0V6.5"),
        shell(body),
        detail(seg(8, 12.5, 16, 20)), detail(seg(16, 12.5, 8, 20)),
    ]


@icon("rat-guard", CAT, "Round metal disc clamped around a diagonal mooring line running from a ship to the quay.",
      tags=["rat shield", "rodent guard", "mooring line", "ship", "quay", "port"])
def _(S):
    th = math.radians(127.7)
    ex, ey = 6.6 * math.cos(th), 6.6 * math.sin(th)
    e1, e2 = (12 + ex, 12 + ey), (12 - ex, 12 - ey)
    ry = 2.4 if S.name == "line" else 2.8
    disc = (f"M{fmt(e1[0])} {fmt(e1[1])}A6.6 {ry} 127.7 1 0 {fmt(e2[0])} {fmt(e2[1])}"
            f"A6.6 {ry} 127.7 1 0 {fmt(e1[0])} {fmt(e1[1])}Z")
    return [
        line(seg(2.5, 4.4, 9.6, 9.9)), line(seg(14.4, 14.1, 21.5, 19.6)),
        shell(disc),
    ]


@icon("cargo-net", CAT, "Square net of thick rope mesh gathered at the corners onto a single lifting ring, holding a load.",
      tags=["lifting net", "sling net", "rope net", "loading", "dockside", "hoist"])
def _(S):
    return [
        line(circle(12, 4.2, 2)),
        line(seg(11, 5.8, 4.5, 12.5)), line(seg(13, 5.8, 19.5, 12.5)),
        shell(rect(4, 12.5, 16, 8.5, S.R)),
        detail(poly([(4.5, 13), (12, 20.5), (19.5, 13)])), detail(poly([(4.5, 20.5), (12, 13), (19.5, 20.5)])),
    ]


@icon("flemish-coil", CAT, "Rope laid flat on a deck in a tight flat spiral, seen from above.",
      tags=["coiled rope", "rope coil", "deck", "spiral", "sailing", "line"])
def _(S):
    tail = "V17" if S.name == "line" else "Q4.5 17 6.5 19"
    return [line("M12.5 11A1.5 1.5 0 0 1 15.5 11A3.5 3.5 0 0 1 8.5 11A5.5 5.5 0 0 1 19.5 11A7.5 7.5 0 0 1 4.5 11" + tail)]


@icon("clove-hitch", CAT, "Rope wrapped twice around a horizontal pole with the two turns crossing in an X over the front.",
      tags=["hitch", "knot", "pole", "rope", "tie", "scouting"])
def _(S):
    return [
        shell(rect(2.5, 9, 19, 6, rr(S, 2))),
        line(seg(8.5, 3, 8.5, 6)), line(seg(15.5, 3, 15.5, 6)),
        line(seg(8.5, 6, 15.5, 18)), line(seg(15.5, 6, 8.5, 18)),
        line(seg(8.5, 18, 8.5, 21.5)), line(seg(15.5, 18, 15.5, 21.5)),
    ]


@icon("overhand-knot", CAT, "Single rope with one simple overhand loop tied in the middle, the two ends leaving in opposite directions.",
      tags=["simple knot", "stopper", "rope", "tie", "loop", "basic knot"])
def _(S):
    return [line("M2.5 17C8 17 15 15 16.5 10C18 4 10 3 8.5 8C7 13 13 17 21.5 17")]


@icon("monkey-fist-knot", CAT, "Round ball of woven rope turns with a single rope tail coming out, a weighted throwing knot.",
      tags=["monkey fist", "heaving line", "rope ball", "throwing weight", "sailor", "knot"])
def _(S):
    body = poly(regular(12, 9.5, 6.3, 10, start=-72), closed=True, r=S.r * 2.2)
    return [
        shell(body),
        detail(rotd(ellipse(12, 9.5, 6.3, 2.4), 45, 12, 9.5)), detail(rotd(ellipse(12, 9.5, 6.3, 2.4), -45, 12, 9.5)),
        line("M12 16Q12 19 15.5 21.5"),
    ]


@icon("turks-head-knot", CAT, "Braided rope band woven around a cylinder in a repeating over and under pattern, like a ring.",
      tags=["turk's head", "braid", "decorative knot", "rope ring", "woven band", "bracelet"])
def _(S):
    return [
        shell(rect(2.5, 6.5, 19, 11, rr(S, 2))),
        detail(poly([(4.5, 7), (9, 17), (13.5, 7), (18, 17)])),
        detail(poly([(4.5, 17), (9, 7), (13.5, 17), (18, 7)])),
    ]


@icon("eye-splice", CAT, "Rope end bent back into a fixed eye loop, with its strands woven into the standing part.",
      tags=["splice", "rope eye", "loop", "rope end", "sailor", "thimble"])
def _(S):
    return [
        line(circle(6.5, 12, 4)),
        shell(rect(11, 9, 10.5, 6, S.R)),
        detail(seg(14.5, 9, 16, 15)), detail(seg(18, 9, 19.5, 15)),
    ]


@icon("ocean-plait-mat", CAT, "Oval flat mat woven from one rope in a tight over and under lattice of diamonds.",
      tags=["ocean mat", "rope mat", "woven mat", "plaited", "decorative", "deck mat"])
def _(S):
    return [
        shell(poly([(6.5, 5.5), (17.5, 5.5), (21.5, 12), (17.5, 18.5), (6.5, 18.5), (2.5, 12)], closed=True, r=S.r * 2.5 + 1)),
        detail(poly([(5.5, 12), (9, 7), (12, 12), (15, 7), (18.5, 12)])),
        detail(poly([(5.5, 12), (9, 17), (12, 12), (15, 17), (18.5, 12)])),
    ]


@icon("rope-whipping", CAT, "Rope end with bands of tight twine wrapped near the tip to stop the strands fraying.",
      tags=["whipped rope", "rope end", "twine", "fraying", "sailor", "rope care"])
def _(S):
    return [
        shell(rect(8, 2.5, 8, 14, S.R)),
        detail(seg(8, 9.5, 16, 9.5)), detail(seg(8, 13, 16, 13)),
        line(seg(9.2, 16.5, 8, 21.5)), line(seg(12, 16.5, 12, 21.5)), line(seg(14.8, 16.5, 16, 21.5)),
    ]
