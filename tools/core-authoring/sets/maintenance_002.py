"""TypeIcon Core: home maintenance (roofing, insulation, walls, paint, wallpaper, floors, doors and windows), batch 002."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "maintenance"


def drop(x, y, h=4.2, w=1.5):
    """Solid water drop with its tip at (x, y)."""
    yb = y + h * 0.68
    return solid(f"M{fmt(x)} {fmt(y)}C{fmt(x)} {fmt(y + h * 0.3)} {fmt(x - w)} {fmt(y + h * 0.45)} {fmt(x - w)} {fmt(yb)}"
                 f"A{fmt(w)} {fmt(w)} 0 0 0 {fmt(x + w)} {fmt(yb)}C{fmt(x + w)} {fmt(y + h * 0.45)} {fmt(x)} {fmt(y + h * 0.3)} {fmt(x)} {fmt(y)}Z")


def rr(S, cap):
    return min(S.R, cap)


def wave(x0, y, n, w=3.0, a=1.2):
    """Open wavy line starting at (x0, y) with n half waves of width w."""
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        d += f"q{fmt(w / 2)} {fmt(-a if i % 2 == 0 else a)} {fmt(w)} 0" if i == 0 else f"t{fmt(w)} 0"
    return d


def xf(x, y, deg):
    """Local frame: origin (x, y), u axis along deg (0 = right, 90 = down), v perpendicular (clockwise)."""
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return lambda u, v: (x + u * c - v * s, y + u * s + v * c)


def bar(x1, y1, x2, y2, w=1.6):
    """Closed rectangle d-string along a segment (for knocked-out tool marks)."""
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    ox, oy = -dy / n * w / 2, dx / n * w / 2
    return poly([(x1 + ox, y1 + oy), (x2 + ox, y2 + oy), (x2 - ox, y2 - oy), (x1 - ox, y1 - oy)], closed=True)


def knock(d):
    """Solid mark that is knocked out of a Filled shell."""
    return Part("dot", d)


def flame(x, y, w=2.2, h=5):
    """Solid flame teardrop centred at x with its point at (x, y+h) pointing down."""
    return solid(f"M{fmt(x)} {fmt(y + h)}C{fmt(x - w)} {fmt(y + h * 0.7)} {fmt(x - w)} {fmt(y + h * 0.3)} {fmt(x)} {fmt(y)}"
                 f"C{fmt(x + w)} {fmt(y + h * 0.3)} {fmt(x + w)} {fmt(y + h * 0.7)} {fmt(x)} {fmt(y + h)}Z")


def pointed_trowel(S, x, y, deg, L=6.0, W=4.6, hl=5.0):
    """Pointed trowel: triangular blade with tip at (x, y), handle extending back along deg."""
    f = xf(x, y, deg)
    return [shell(poly([f(0, 0), f(L, W / 2), f(L, -W / 2)], closed=True, r=S.r * 0.6)),
            line(poly([f(L, 0), f(L + hl, 0)]))]


def knife(S, x, y, deg, L=6.0, W=4.0, hl=5.0):
    """Flat blade knife: rectangular blade, tip edge at (x, y), handle back along deg."""
    f = xf(x, y, deg)
    return [shell(poly([f(0, -W / 2), f(0, W / 2), f(L, W / 2), f(L, -W / 2)], closed=True, r=S.r * 0.6)),
            line(poly([f(L, 0), f(L + hl, 0)]))]


# ============================================================================ roof, gutters, chimney

@icon("clogged-gutter", CAT, "A gutter trough heaped with leaves and water spilling over its front edge",
      tags=["clogged gutter", "blocked gutter", "leaves", "overflow", "rain gutter", "cleaning", "eavestrough"])
def _(S):
    return [
        shell(poly([(3, 10), (21, 10), (18.5, 16), (5.5, 16)], closed=True, r=S.r)),
        line("M5 10C5.5 5 9 4.5 10 7.5C11 3.5 14.5 3.5 15 7C16 5.5 18.5 6 19 10"),
        drop(8.5, 18.5, 3.3, 1.2),
        drop(15.5, 18.5, 3.3, 1.2),
    ]


@icon("gutter-guard", CAT, "A gutter trough covered by a perforated mesh strip with a leaf resting on top",
      tags=["gutter guard", "gutter cover", "leaf guard", "mesh", "gutter screen", "rain gutter", "leaf filter"])
def _(S):
    return [
        shell(poly([(4, 10), (20, 10), (22, 14), (2, 14)], closed=True, r=S.r * 0.6)),
        dot(8, 12, 0.8), dot(12, 12, 0.8), dot(16, 12, 0.8),
        shell(poly([(2, 16), (22, 16), (19.5, 21.5), (4.5, 21.5)], closed=True, r=S.r)),
        line("M8 7C8 4.5 11 3.5 14 4C14 6.5 11 7.5 8 7Z") if S.name == "rounded" else line("M8 7C8 4 12 3.5 14 4C14 6.5 11 7.5 8 7Z"),
    ]


@icon("downspout-splash-block", CAT, "A downspout elbow above a sloped concrete block with water running along it",
      tags=["splash block", "downspout", "drainage", "rain water", "gutter outlet", "downspout extension", "runoff"])
def _(S):
    return [
        line(poly([(6, 2.5), (6, 8), (10, 10.5)], r=S.r)),
        drop(12, 12, 3.2, 1.2),
        shell(poly([(3, 16.5), (21, 19.5), (21, 21.5), (3, 21.5)], closed=True, r=S.r * 0.6)),
    ]


@icon("ice-dam", CAT, "A roof edge with a ridge of ice, icicles hanging below and water pooled behind it",
      tags=["ice dam", "icicles", "roof ice", "winter roof", "eave", "frozen gutter", "snow melt"])
def _(S):
    return [
        shell(poly([(2, 3), (13, 7.5), (13, 11.5), (2, 7)], closed=True, r=S.r * 0.5)),
        shell(rect(13, 7, 8, 7, rr(S, 2))),
        solid("M14 14L16 21L18 14Z"),
        solid("M18.5 14L20 19L21.5 14Z"),
    ]


@icon("roof-moss", CAT, "Rows of roof shingles with round clumps of moss growing along the joints",
      tags=["roof moss", "moss", "algae", "shingles", "roof cleaning", "growth", "damp roof"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        detail(seg(3, 9, 21, 9)),
        detail(seg(3, 15, 21, 15)),
        detail(seg(12, 3, 12, 9)),
        detail(seg(7.5, 9, 7.5, 15)),
        detail(seg(16.5, 9, 16.5, 15)),
        dot(8, 9, 1.4), dot(10.6, 9.6, 1.1),
        dot(15, 15, 1.4), dot(17.7, 15.6, 1.1),
    ]


@icon("turbine-roof-vent", CAT, "A domed spinning turbine vent with curved vanes on a short base on a roof ridge",
      tags=["turbine vent", "whirlybird", "roof vent", "attic ventilation", "wind turbine vent", "ventilator", "attic fan"])
def _(S):
    return [
        line(seg(2, 21, 22, 21)),
        shell(rect(7, 14.5, 10, 4.5, rr(S, 1.2))),
        shell("M5 14.5A7 7 0 0 1 19 14.5Z"),
        detail("M9.5 14.5C8.5 11.5 9 9.5 11 8.5"),
        detail("M14.5 14.5C15.5 11.5 15 9.5 13 8.5"),
        line(seg(12, 3, 12, 7.5)),
    ]


@icon("soffit-vent", CAT, "The underside of a roof eave seen from below with a slotted rectangular vent panel",
      tags=["soffit", "soffit vent", "eave vent", "attic ventilation", "roof eave", "air intake", "underside of roof"])
def _(S):
    return [
        line(seg(2, 4, 22, 4)),
        shell(poly([(6, 8), (18, 8), (22, 20), (2, 20)], closed=True, r=S.r)),
        detail(rect(8, 12, 8, 4.5)),
        detail(seg(12, 12, 12, 16.5)),
    ]


@icon("torch-on-roofing", CAT, "A rolled roofing membrane being unrolled while a torch flame heats its underside",
      tags=["torch on roofing", "torch down", "flat roof", "membrane", "roofing felt", "bitumen", "propane torch"])
def _(S):
    return [
        shell(circle(6.5, 12, 4.5)),
        dot(6.5, 12, 1.2),
        line("M6.5 16.5H22"),
        line(seg(2, 21.5, 22, 21.5)),
        line(seg(21, 3, 15.5, 8.5)),
        flame(14, 9.5, 2, 5),
    ]


@icon("ladder-stabilizer", CAT, "The top of a ladder fitted with a wide U-shaped standoff arm",
      tags=["ladder stabilizer", "ladder standoff", "ladder safety", "wall standoff", "ladder accessory", "gutter work", "roof access"])
def _(S):
    return [
        line(poly([(4, 3), (4, 8), (20, 8), (20, 3)], r=S.r)),
        line(seg(8.5, 8, 8.5, 22)),
        line(seg(15.5, 8, 15.5, 22)),
        line(seg(8.5, 13.5, 15.5, 13.5)),
        line(seg(8.5, 19, 15.5, 19)),
    ]


@icon("sagging-roof", CAT, "A house whose roof line dips down in the middle with a downward arrow above it",
      tags=["sagging roof", "roof sag", "roof damage", "structural", "drooping ridge", "roof problem", "deflection"])
def _(S):
    return [
        line("M2.5 12L7.5 6Q12 12 16.5 6L21.5 12"),
        line(poly([(5, 13), (5, 21.5), (19, 21.5), (19, 13)], r=S.r)),
        line(poly([(10, 2.5), (12, 4.5), (14, 2.5)], r=S.r)),
    ]


@icon("tarped-roof", CAT, "A pitched roof covered by a tarp held down with sandbags along its edges",
      tags=["tarped roof", "roof tarp", "storm damage", "temporary roof", "sandbags", "emergency repair", "blue tarp"])
def _(S):
    return [
        shell(poly([(3, 14.5), (12, 5.5), (21, 14.5)], closed=True, r=S.r)),
        dot(6.5, 12, 1.3), dot(17.5, 12, 1.3), dot(9.5, 9, 1.1), dot(14.5, 9, 1.1),
        line(poly([(5, 17.5), (5, 21.5), (19, 21.5), (19, 17.5)], r=S.r)),
    ]


@icon("brick-repointing", CAT, "A brick wall section with a pointing trowel pressing mortar into a horizontal joint",
      tags=["repointing", "pointing", "mortar", "brick repair", "bricklaying", "trowel", "masonry"])
def _(S):
    return [
        shell(rect(2.5, 3, 12, 17, rr(S, 2))),
        detail(seg(2.5, 8.5, 14.5, 8.5)),
        detail(seg(2.5, 14, 14.5, 14)),
        detail(seg(8.5, 3, 8.5, 8.5)),
        detail(seg(11.5, 8.5, 11.5, 14)),
        *pointed_trowel(S, 14, 12.5, 40, 6.5, 5, 3),
    ]


@icon("spalling-brick", CAT, "A brick wall section with one crumbled brick face and fragments falling below",
      tags=["spalling", "crumbling brick", "brick damage", "frost damage", "masonry repair", "flaking", "decay"])
def _(S):
    return [
        shell(poly([(3, 3), (21, 3), (21, 15), (16.5, 15), (14.5, 13), (12, 15.5), (9.5, 13), (7.5, 15), (3, 15)], closed=True, r=S.r * 0.4)),
        detail(seg(3, 9, 21, 9)),
        detail(seg(12, 3, 12, 9)),
        solid("M8 18L10.5 18L9 21Z"),
        solid("M13 18.5L15.5 18.5L14.5 21.5Z"),
        solid("M18 18L20 19.5L17.5 20.5Z"),
    ]


@icon("chimney-damper", CAT, "A chimney flue with a hinged plate inside and a pull chain hanging below",
      tags=["damper", "chimney damper", "flue", "fireplace", "chimney", "pull chain", "draft control"])
def _(S):
    return [
        line(seg(4.5, 2, 4.5, 22)),
        line(seg(19.5, 2, 19.5, 22)),
        line(seg(4.5, 9, 18, 13)),
        line(seg(16, 14, 16, 17.5)),
        line(circle(16, 19.5, 1.5)),
    ]


@icon("chimney-balloon", CAT, "A chimney flue plugged by an inflated balloon with an air tube below",
      tags=["chimney balloon", "flue plug", "draft stopper", "fireplace", "chimney seal", "inflatable", "heat loss"])
def _(S):
    return [
        line(seg(4, 2, 4, 22)),
        line(seg(20, 2, 20, 22)),
        shell(ellipse(12, 11, 5.5, 6.5)),
        line(seg(12, 17.5, 12, 22)),
    ]


# ============================================================================ outdoors, foundation, insulation, draughts

@icon("window-well", CAT, "A corrugated half-round metal well dug below ground level around a basement window",
      tags=["window well", "basement window", "egress", "light well", "ground level", "foundation", "drainage"])
def _(S):
    return [
        line(seg(2, 5, 22, 5)),
        shell("M4 5A8 15 0 0 0 20 5Z"),
        detail(rect(8.5, 7.5, 7, 6.5)),
        detail(seg(12, 7.5, 12, 14)),
    ]


@icon("leaning-fence", CAT, "Two fence pickets leaning to one side with a diagonal brace propping them up",
      tags=["leaning fence", "fence repair", "tilted post", "fence brace", "storm damage", "wobbly fence", "post support"])
def _(S):
    def pk(cx, w=4):
        sh = lambda y: (21.5 - y) * 0.14
        return shell(poly([(cx - w / 2 + sh(21.5), 21.5), (cx - w / 2 + sh(7), 7), (cx + sh(3), 3), (cx + w / 2 + sh(7), 7), (cx + w / 2 + sh(21.5), 21.5)], closed=True, r=S.r * 0.5))
    return [pk(10), pk(17), line(seg(2.5, 21.5, 6.5, 12))]


@icon("driveway-sealing", CAT, "A driveway in perspective with a long-handled squeegee spreading a dark sealer layer",
      tags=["driveway sealing", "sealcoat", "asphalt", "tarmac", "squeegee", "paving", "sealer"])
def _(S):
    return [
        shell(poly([(8, 8), (16, 8), (22, 21.5), (2, 21.5)], closed=True, r=S.r * 0.6)),
        line(seg(6, 14, 15, 14)),
        solid(rect(5, 17, 15, 2)),
        line(seg(10.5, 14, 18, 2.5)),
    ]


@icon("crack-monitor-gauge", CAT, "Two overlapping plastic plates with a crosshair grid fixed across a wall crack",
      tags=["crack monitor", "crack gauge", "tell tale", "wall crack", "movement monitor", "subsidence", "structural survey"])
def _(S):
    return [
        line(poly([(13, 1.5), (11, 3.5), (12.5, 5)])),
        shell(rect(2.5, 6, 12, 9, rr(S, 2))),
        shell(rect(9.5, 10, 12, 9, rr(S, 2))),
        detail(seg(15.5, 12, 15.5, 17.5)),
        detail(seg(11.5, 14.5, 19.5, 14.5)),
    ]


@icon("foundation-underpinning", CAT, "A house footing supported by steel piers and jacks driven in below it",
      tags=["underpinning", "foundation repair", "piers", "jacks", "house lifting", "settlement", "structural support"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 6, rr(S, 1.5))),
        line(seg(7, 9, 7, 22)),
        line(seg(17, 9, 17, 22)),
        line(seg(3.5, 14, 10.5, 14)),
        line(seg(13.5, 14, 20.5, 14)),
    ]


@icon("blown-in-insulation", CAT, "An attic roof with a hose blowing a cloud of loose-fill insulation onto the floor",
      tags=["blown in insulation", "loose fill", "attic insulation", "cellulose", "insulation hose", "energy saving", "loft"])
def _(S):
    return [
        line(poly([(2, 12), (12, 3.5), (22, 12)], r=S.r)),
        shell("M6 21C3.5 21 3.5 17 6.5 17C7 14 11 14 12 16.5C14 15 18 16 17.5 19C19.5 19.5 19 21 17 21Z"),
        line(poly([(22, 15), (19, 15), (15.5, 11)], r=S.r)),
    ]


@icon("spray-foam-insulation", CAT, "A spray gun filling the space between two wall studs with a bumpy layer of foam",
      tags=["spray foam", "foam insulation", "stud wall", "expanding foam", "insulation gun", "energy saving", "wall cavity"])
def _(S):
    return [
        line(seg(4, 2.5, 4, 21.5)),
        line(seg(20, 2.5, 20, 21.5)),
        shell(rect(7, 2.5, 10, 4, rr(S, 1.5))),
        shell("M8 21.5V13.5C6.5 12 9 10 10.5 11.5C11 9 14 9 14.5 11.5C16 10 18 12 16 13.5V21.5Z"),
    ]


@icon("rigid-insulation-board", CAT, "A short stack of thick foam boards with one foil-faced board leaning in front",
      tags=["rigid insulation", "foam board", "xps", "eps", "polyiso", "foil faced", "insulation panel"])
def _(S):
    return [
        shell(rect(2.5, 13, 12, 8.5, rr(S, 1.5))),
        detail(seg(2.5, 17.2, 14.5, 17.2)),
        shell(poly([(14, 3), (19, 3), (21.5, 21.5), (15.5, 21.5)], closed=True, r=S.r * 0.6)),
        detail(seg(16.8, 8, 17.7, 15)),
    ]


@icon("cavity-wall-insulation", CAT, "A wall cross-section with two brick leaves and dotted insulation filling the gap between them",
      tags=["cavity wall", "wall insulation", "injected insulation", "brick wall", "beads", "retrofit", "energy saving"])
def _(S):
    return [
        shell(rect(2.5, 3, 6, 18, rr(S, 3))),
        shell(rect(15.5, 3, 6, 18, rr(S, 3))),
        detail(seg(2.5, 12, 8.5, 12)),
        detail(seg(15.5, 12, 21.5, 12)),
        dot(10.8, 5.5, 0.9), dot(13.2, 8, 0.9), dot(10.8, 10.5, 0.9), dot(13.2, 13, 0.9), dot(10.8, 15.5, 0.9), dot(13.2, 18, 0.9),
    ]


@icon("weatherstripping", CAT, "A roll of foam strip tape with a length stuck down along a door frame edge",
      tags=["weatherstrip", "door seal", "draught excluder", "draft stopper", "foam tape", "door frame", "energy saving"])
def _(S):
    return [
        line(seg(20.5, 2, 20.5, 22)),
        shell(rect(15.5, 8, 3, 13.5, rr(S, 1))),
        shell(circle(7.5, 8, 5)),
        dot(7.5, 8, 1.2),
        line(seg(12.5, 8, 15.5, 8)),
    ]


@icon("window-shrink-film", CAT, "A window covered by clear film with a hair dryer blowing warm air at it",
      tags=["shrink film", "window insulation kit", "plastic film", "hair dryer", "draft proofing", "winterize", "window cover"])
def _(S):
    return [
        shell(rect(2.5, 3, 12, 12, rr(S, 2))),
        detail(seg(8.5, 3, 8.5, 15)),
        detail(seg(2.5, 9, 14.5, 9)),
        shell(rect(14, 16.5, 7.5, 4.5, rr(S, 1.5))),
        line(wave(5.5, 19, 2, 3, 1)),
    ]


@icon("house-heat-loss", CAT, "A house outline with wavy heat lines rising inside it and escaping through the roof",
      tags=["heat loss", "energy waste", "poor insulation", "thermal leak", "energy audit", "heating bill", "warm air"])
def _(S):
    return [
        shell(poly([(3.5, 21.5), (3.5, 10.5), (12, 3.5), (20.5, 10.5), (20.5, 21.5)], closed=True, r=S.r)),
        detail("M8.5 19C7 17.5 10 16 8.5 14.5C7 13 10 12 8.5 10.5"),
        detail("M15.5 19C14 17.5 17 16 15.5 14.5C14 13 17 12 15.5 10.5"),
    ]


@icon("radiant-barrier-foil", CAT, "Attic rafters lined with a shiny foil sheet while sun rays bounce away from it",
      tags=["radiant barrier", "attic foil", "reflective insulation", "heat reflection", "sun rays", "cooling", "attic"])
def _(S):
    return [
        line(poly([(2, 21.5), (12, 10), (22, 21.5)], r=S.r)),
        line(poly([(6, 21.5), (12, 14.5), (18, 21.5)], r=S.r)),
        line(circle(5, 5, 2.2)),
        line(seg(8.5, 7.5, 10.5, 9.5)),
        line(poly([(15, 5), (18, 5)])),
        line(seg(18.5, 7.5, 21, 7.5)),
    ]


@icon("caulking-window", CAT, "A caulking gun nozzle laying a bead of sealant along the edge of a window frame",
      tags=["caulking", "sealant", "caulk gun", "window frame", "weatherproofing", "silicone", "draught sealing"])
def _(S):
    f = xf(10, 10, 225)
    return [
        shell(rect(11, 11, 11, 10.5, rr(S, 1.5))),
        detail(seg(16.5, 11, 16.5, 21.5)),
        shell(poly([f(0, 0), f(3, 1.3), f(3, -1.3)], closed=True)),
        shell(poly([f(3, -2.3), f(8.5, -2.3), f(8.5, 2.3), f(3, 2.3)], closed=True, r=S.r * 0.5)),
        line(poly([f(8.5, 0), f(10.5, 0)])),
    ]


@icon("blower-door-test", CAT, "A door frame fitted with a tight panel holding a large round fan in its centre",
      tags=["blower door", "air tightness test", "energy audit", "pressure test", "fan door", "infiltration", "home energy"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, S.R)),
        detail(circle(12, 12, 6)),
        detail(seg(12, 12, 12, 7)),
        detail(seg(12, 12, 16.3, 14.5)),
        detail(seg(12, 12, 7.7, 14.5)),
    ]


@icon("drafty-window", CAT, "A window with curved wind lines blowing in around its frame",
      tags=["drafty window", "draught", "air leak", "cold air", "wind", "leaky window", "heat loss"])
def _(S):
    return [
        shell(rect(11, 3, 10.5, 18, rr(S, 2))),
        detail(seg(11, 12, 21.5, 12)),
        line(wave(1.5, 9, 2, 3.5, 1.3)),
        line(wave(1.5, 16, 2, 3.5, 1.3)),
    ]


# ============================================================================ heating, paint and wallpaper

@icon("bleeding-radiator", CAT, "A radiator with a key turning its bleed valve and a drop falling onto a cloth",
      tags=["bleed radiator", "radiator key", "trapped air", "heating repair", "cold radiator", "bleed valve", "central heating"])
def _(S):
    return [
        shell(rect(2.5, 3, 12, 18.5, rr(S, 3))),
        detail(seg(6.5, 3, 6.5, 21.5)),
        detail(seg(10.5, 3, 10.5, 21.5)),
        shell(rect(14.5, 4, 4, 4, rr(S, 1))),
        line(seg(18.5, 6, 21.5, 6)),
        drop(16.5, 10.5, 4, 1.4),
        line(wave(14.5, 20, 2, 3.5, 1)),
    ]


@icon("air-duct-cleaning", CAT, "A rectangular air duct in cross-section with a rotating brush head on a flexible shaft",
      tags=["duct cleaning", "air duct", "hvac cleaning", "brush", "ventilation", "ductwork", "dust removal"])
def _(S):
    spokes = [detail(seg(16, 12, *polar(16, 12, 4, a))) for a in (0, 60, 120, 180, 240, 300)]
    return [
        shell(rect(2.5, 4.5, 19, 15, rr(S, 3))),
        detail(wave(3, 12, 2, 3.5, 1.3)),
        dot(16, 12, 1.4),
        *spokes,
    ]


@icon("hvac-manifold-gauge", CAT, "Two round pressure gauges on a manifold bar with three hoses hanging below",
      tags=["manifold gauge", "hvac gauges", "refrigerant", "pressure gauge", "air conditioning service", "hoses", "technician"])
def _(S):
    return [
        shell(circle(7, 7.5, 4.5)),
        shell(circle(17, 7.5, 4.5)),
        detail(seg(7, 7.5, 8.5, 5.5)),
        detail(seg(17, 7.5, 18.5, 5.5)),
        shell(rect(2.5, 13.5, 19, 3, rr(S, 1.5))),
        line(seg(6, 16.5, 6, 22)),
        line(seg(12, 16.5, 12, 22)),
        line(seg(18, 16.5, 18, 22)),
    ]


@icon("painters-tape", CAT, "A roll of masking tape with a strip pulled out and stuck along a straight wall edge",
      tags=["painter's tape", "masking tape", "painting prep", "clean edge", "tape roll", "decorating", "masking"])
def _(S):
    return [
        shell(circle(8, 14, 6.5)),
        dot(8, 14, 2),
        line("M14.5 14C17.5 14 18.5 12 18.5 8V2.5"),
        line(seg(21.5, 2.5, 21.5, 21.5)),
    ]


@icon("paint-edger", CAT, "A flat rectangular paint pad on a handle with small guide wheels along one edge",
      tags=["paint edger", "edging pad", "cutting in", "paint pad", "ceiling edge", "painting tool", "trim painting"])
def _(S):
    return [
        line(seg(11.5, 12, 11.5, 3)),
        shell(rect(3, 12, 17, 5, rr(S, 2))),
        dot(6, 19.8, 1.5),
        dot(17, 19.8, 1.5),
    ]


@icon("paint-stir-stick", CAT, "A flat wooden paddle stick with holes near its end, dipped into an open paint can",
      tags=["paint stirrer", "stir stick", "paddle", "mixing paint", "paint can", "open can", "decorating"])
def _(S):
    return [
        line(poly([(3.5, 14.5), (3.5, 21.5), (20.5, 21.5), (20.5, 14.5)], r=S.r)),
        shell(rect(9.5, 2.5, 5, 15.5, rr(S, 1.5))),
        dot(12, 6.5, 0.9), dot(12, 9.5, 0.9), dot(12, 12.5, 0.9),
    ]


@icon("paint-can-opener", CAT, "A small flat key-shaped lever with a hooked tip prying up the lid rim of a paint can",
      tags=["paint can opener", "lid lever", "can key", "pry tool", "paint tin", "decorating", "tin opener"])
def _(S):
    return [
        line("M3 11V19C3 21.5 21 21.5 21 19V11"),
        shell(ellipse(12, 11, 9, 3.5)),
        line(circle(19.5, 4, 2.3)),
        line(seg(18, 5.8, 12.5, 10)),
        line(poly([(12.5, 10), (10.5, 8.2)])),
    ]


@icon("wallpaper-pasting-table", CAT, "A long folding trestle table with wallpaper unrolled across it and a paste brush on top",
      tags=["pasting table", "wallpaper table", "trestle table", "paste brush", "wallpapering", "decorating", "folding table"])
def _(S):
    return [
        shell(rect(2, 13, 20, 2.5, rr(S, 1))),
        line(poly([(5, 15.5), (3, 21.5)])), line(poly([(5, 15.5), (7, 21.5)])),
        line(poly([(19, 15.5), (17, 21.5)])), line(poly([(19, 15.5), (21, 21.5)])),
        shell(circle(5.5, 7.5, 3.5)),
        line("M5.5 11H22"),
        shell(rect(14, 6, 5.5, 3, rr(S, 1))),
        line(seg(16.8, 6, 16.8, 3)),
    ]


@icon("wallpaper-seam-roller", CAT, "A small narrow roller wheel on a bent handle pressing along a wallpaper seam",
      tags=["seam roller", "wallpaper roller", "wallpapering", "seam press", "paper joint", "decorating tool", "smoothing"])
def _(S):
    return [
        line(seg(8, 2.5, 8, 13)),
        shell(circle(8, 17, 4)),
        dot(8, 17, 1.1),
        line(poly([(12, 17), (17.5, 17), (17.5, 4)], r=S.r)),
    ]


@icon("wallpaper-steamer", CAT, "A flat steam plate on a hose connected to a small water tank with steam rising",
      tags=["wallpaper steamer", "steam stripper", "wallpaper removal", "steam plate", "hose", "water tank", "stripping"])
def _(S):
    return [
        line(wave(5, 6.5, 2, 3, 1.1)),
        shell(rect(2.5, 9, 11, 12.5, rr(S, 3))),
        dot(6, 13, 1), dot(10, 13, 1), dot(6, 17, 1), dot(10, 17, 1),
        line("M13.5 17C15 17 15 18 16.5 18"),
        shell(rect(16.5, 12, 5.5, 9.5, rr(S, 2))),
    ]


@icon("peeling-wallpaper", CAT, "A strip of patterned wallpaper curling away from the wall at its top",
      tags=["peeling wallpaper", "loose wallpaper", "curling paper", "wall covering", "damp damage", "wallpaper repair", "lifting seam"])
def _(S):
    return [
        line(seg(2.5, 2.5, 2.5, 21.5)),
        shell(rect(7, 9, 10, 12.5, rr(S, 1.5))),
        shell(poly([(7, 9), (17, 9), (21.5, 3.5), (11.5, 3.5)], closed=True, r=S.r * 0.5)),
        dot(12, 14, 1.1), dot(10, 18, 1.1), dot(14.5, 18, 1.1),
    ]


@icon("hanging-wallpaper", CAT, "A wallpaper strip unrolled down a wall beside a hanging plumb line",
      tags=["hanging wallpaper", "wallpapering", "plumb line", "plumb bob", "wall covering", "decorating", "paper hanging"])
def _(S):
    return [
        line(seg(4, 2.5, 4, 15)),
        solid("M4 15.5L6.2 18.5L4 21.5L1.8 18.5Z"),
        shell(rect(9, 2.5, 11.5, 15, rr(S, 2))),
        dot(14.8, 7, 1.1), dot(12.5, 11.5, 1.1), dot(17.2, 11.5, 1.1),
        line(seg(9, 21.5, 20.5, 21.5)),
    ]


@icon("spackle-tub", CAT, "A round tub of wall filler with a mound inside and a small putty knife leaning on the rim",
      tags=["spackle", "filler", "joint compound", "putty", "wall repair", "tub", "plaster filler"])
def _(S):
    return [
        shell(poly([(3, 13), (17, 13), (16, 21.5), (4, 21.5)], closed=True, r=S.r)),
        line("M5.5 13C5.5 9 14.5 9 14.5 13"),
        *knife(S, 19.5, 4.5, 120, 5, 3.5, 4),
    ]


@icon("drywall-patch", CAT, "A wall section with a square mesh patch stuck over a hole",
      tags=["drywall patch", "wall patch", "mesh patch", "hole repair", "plasterboard", "wall repair", "gypsum"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 4))),
        detail(rect(6.5, 6.5, 11, 11)),
        detail(seg(12, 6.5, 12, 17.5)),
        detail(seg(6.5, 12, 17.5, 12)),
    ]


@icon("hole-in-drywall", CAT, "A wall section with a jagged hole and short cracks radiating from it",
      tags=["hole in wall", "drywall hole", "wall damage", "plasterboard", "punched wall", "repair needed", "cracks"])
def _(S):
    pts = [polar(12, 12, 5 if i % 2 else 3.1, -90 + i * 45) for i in range(8)]
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 4))),
        detail(poly(pts, closed=True)),
        detail(seg(*polar(12, 12, 6.6, 22), *polar(12, 12, 8.8, 22))),
        detail(seg(*polar(12, 12, 6.6, 202), *polar(12, 12, 8.8, 202))),
    ]


# ============================================================================ wall finishing tools

@icon("filling-wall-crack", CAT, "A wall with a zigzag crack and a filling knife pressing filler into it",
      tags=["fill crack", "wall crack", "filler", "filling knife", "plaster repair", "decorating prep", "spackling"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 10, 19, rr(S, 2))),
        detail(poly([(9, 2.5), (6, 8), (10, 13), (6.5, 21.5)])),
        *knife(S, 10.5, 13, 20, 6, 4, 3.5),
    ]


@icon("drywall-nail-pop", CAT, "A wall surface with a small raised nail head and a circular crack around it",
      tags=["nail pop", "drywall nail", "wall bump", "screw pop", "plasterboard", "wall repair", "ring crack"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 4))),
        detail(circle(12, 12, 5.5)),
        dot(12, 12, 1.6),
    ]


@icon("inside-corner-trowel", CAT, "A trowel whose blade is folded to a right angle along its middle, with a short handle on its back",
      tags=["corner trowel", "inside corner", "plastering", "drywall finishing", "bent trowel", "joint compound", "finishing tool"])
def _(S):
    return [
        shell(poly([(3, 12), (12, 9), (21, 12), (21, 20), (12, 17), (3, 20)], closed=True, r=S.r * 0.6)),
        detail(seg(12, 9, 12, 17)),
        line(seg(12, 9, 12, 5.5)),
        shell(rect(9.5, 2, 5, 4, rr(S, 1.5))),
    ]


@icon("pole-sander", CAT, "A rectangular sanding pad on a swivel joint attached to a long pole",
      tags=["pole sander", "drywall sander", "ceiling sander", "sanding pad", "extension pole", "finishing", "sandpaper"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 5.5, rr(S, 2))),
        shell(circle(12, 11.5, 2)),
        line(seg(12.8, 13.5, 17.5, 22)),
    ]


@icon("hopper-texture-gun", CAT, "A spray gun with a wide open funnel hopper on top and a pistol grip",
      tags=["texture gun", "hopper gun", "drywall texture", "ceiling texture", "popcorn ceiling", "spray gun", "plaster spray"])
def _(S):
    return [
        shell(poly([(4.5, 2.5), (17.5, 2.5), (14, 9.5), (8, 9.5)], closed=True, r=S.r * 0.6)),
        shell(rect(2.5, 10, 15, 5, rr(S, 2))),
        line(seg(17.5, 12.5, 21.5, 12.5)),
        shell(poly([(6, 15), (11.5, 15), (10.5, 21.5), (5.5, 21.5)], closed=True, r=S.r * 0.6)),
    ]


@icon("paint-mixer-paddle", CAT, "A drill shaft ending in a spiral mixing paddle dipped in a paint bucket",
      tags=["paint mixer", "mixing paddle", "drill attachment", "stirrer", "paint bucket", "mixing paint", "thinset mixer"])
def _(S):
    return [
        shell(rect(10, 2, 4, 3.5, rr(S, 1.2))),
        line(seg(12, 5.5, 12, 11)),
        line("M12 11C6.5 12 8 15 12 15.5C16 16 17.5 19 12 20"),
        line(poly([(3.5, 13), (4.5, 21.5), (19.5, 21.5), (20.5, 13)])),
    ]


@icon("hand-masker", CAT, "A handheld tool carrying a paper roll and a tape roll, with a masking strip running out",
      tags=["hand masker", "masking film", "masking paper", "masking tool", "paint prep", "tape and paper", "dispenser"])
def _(S):
    return [
        shell(circle(7.5, 7.5, 4.5)),
        dot(7.5, 7.5, 1.2),
        shell(circle(17.5, 7.5, 3.2)),
        line(seg(12, 7.5, 14.3, 7.5)),
        shell(poly([(4, 14), (13, 14), (13, 19.5), (11.2, 21.5), (9.2, 19.5), (7.5, 21.5), (5.7, 19.5), (4, 19.5)], closed=True, r=0)),
        line(seg(17.5, 10.7, 17.5, 17)),
    ]


@icon("plastering-trowel", CAT, "A wide flat steel blade with a handle mounted on top along its length",
      tags=["plastering trowel", "finishing trowel", "skim coat", "plaster", "float", "wall finishing", "render"])
def _(S):
    return [
        shell(poly([(2, 15.5), (22, 15.5), (20.5, 19.5), (3.5, 19.5)], closed=True, r=S.r * 0.5)),
        line(seg(8, 15.5, 8, 11)),
        line(seg(16, 15.5, 16, 11)),
        shell(rect(6, 5.5, 12, 5.5, rr(S, 2.5))),
    ]


@icon("grout-saw", CAT, "A short handle with a narrow serrated blade at one end, beside rows of tile grout lines",
      tags=["grout saw", "grout removal", "grout rake", "tile repair", "regrouting", "serrated blade", "tile tool"])
def _(S):
    f = xf(21, 3, 135)
    teeth = poly([f(0, 0), f(1, 1.4), f(2, 0), f(3, 1.4), f(4, 0), f(5, 1.4), f(6, 0)])
    return [
        line(teeth),
        shell(poly([f(6, -2), f(14, -2), f(14, 2), f(6, 2)], closed=True, r=S.r * 0.5)),
        line(seg(2, 17, 22, 17)),
        line(seg(8, 17, 8, 22)),
        line(seg(16, 17, 16, 22)),
    ]


@icon("caulk-smoothing-tool", CAT, "A small flat plastic spatula with angled corners smoothing a sealant bead in a corner",
      tags=["caulk tool", "sealant smoother", "bead finishing", "silicone tool", "spatula", "corner seal", "caulking"])
def _(S):
    return [
        shell(poly([(5, 2.5), (19, 2.5), (19, 8), (12, 14), (5, 8)], closed=True, r=S.r * 0.6)),
        dot(12, 6.5, 1.3),
        line(poly([(3, 16.5), (12, 21.5), (21, 16.5)])),
    ]


@icon("resealing-bathtub", CAT, "A bathtub rim meeting a tiled wall with a fresh sealant bead laid along the joint",
      tags=["reseal bath", "bath sealant", "silicone bead", "bathroom", "tub caulk", "tiles", "waterproofing"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 6.5, rr(S, 2))),
        detail(seg(9, 2.5, 9, 9)),
        detail(seg(15.5, 2.5, 15.5, 9)),
        solid(rect(2.5, 10.8, 19, 2)),
        shell(poly([(2.5, 15), (21.5, 15), (21.5, 17), (18, 21.5), (6, 21.5), (2.5, 17)], closed=True, r=S.r)),
    ]


@icon("deck-staining", CAT, "Wooden deck boards with a wide brush applying a darker stain stripe along one board",
      tags=["deck stain", "staining", "decking", "wood stain", "brush", "outdoor wood", "deck care"])
def _(S):
    return [
        line(seg(12.5, 2.5, 12.5, 6)),
        shell(poly([(8, 6), (17, 6), (16.5, 11), (8.5, 11)], closed=True, r=S.r * 0.5)),
        shell(rect(2.5, 13, 19, 8.5, rr(S, 2))),
        detail(seg(2.5, 17.2, 21.5, 17.2)),
    ]


@icon("floor-drum-sander", CAT, "An upright walk-behind floor sanding machine with a dust bag and a drum at the bottom",
      tags=["floor sander", "drum sander", "sanding floors", "hardwood floor", "refinishing", "dust bag", "floor restoration"])
def _(S):
    return [
        shell(rect(3, 16, 13, 5.5, rr(S, 2.5))),
        line(poly([(8, 16), (9, 8), (4, 2.5)], r=S.r)),
        shell(rect(14.5, 6.5, 7, 8, rr(S, 3))),
        line(poly([(11, 11), (14.5, 11)])),
        dot(19, 19, 1.5),
    ]


@icon("squeaky-floorboard", CAT, "A row of floorboards with the middle one bowed upward and sound lines above it",
      tags=["squeaky floor", "creaky floorboard", "loose board", "floor noise", "floor repair", "carpentry", "joist"])
def _(S):
    return [
        line(arc(12, 11, 3, 215, 325)),
        line(arc(12, 11, 6, 215, 325)),
        shell(rect(2.5, 15, 6, 6.5, rr(S, 1.5))),
        shell("M9.5 21.5V16C10.5 12.5 13.5 12.5 14.5 16V21.5Z"),
        shell(rect(15.5, 15, 6, 6.5, rr(S, 1.5))),
    ]


@icon("cracked-tile", CAT, "A square floor tile with a zigzag crack running across it",
      tags=["cracked tile", "broken tile", "tile repair", "floor tile", "ceramic", "damaged tile", "replace tile"])
def _(S):
    return [
        shell(rect(3.5, 3.5, 17, 17, rr(S, 3))),
        detail(poly([(13.5, 3.5), (10, 9), (14.5, 13), (10.5, 20.5)])),
    ]


@icon("carpet-knee-kicker", CAT, "A short carpet stretching tool with a toothed head at one end and a padded cushion at the other",
      tags=["knee kicker", "carpet stretcher", "carpet fitting", "carpet tool", "flooring", "gripper teeth", "installation"])
def _(S):
    return [
        solid("M6 6.5L2.5 8L6 9.5Z"),
        solid("M6 10.5L2.5 12L6 13.5Z"),
        solid("M6 14.5L2.5 16L6 17.5Z"),
        shell(rect(6, 6, 4, 12, rr(S, 1))),
        shell(rect(10, 10.5, 6, 3, rr(S, 1))),
        shell(rect(16, 5.5, 5.5, 13, rr(S, 3))),
    ]


@icon("cutting-in-paint", CAT, "An angled brush painting a clean line where a wall meets the ceiling",
      tags=["cutting in", "edging", "angled brush", "ceiling line", "wall paint", "painting technique", "trim brush"])
def _(S):
    f = xf(12, 9.5, 45)
    return [
        line(seg(2.5, 5, 21.5, 5)),
        solid(rect(2.5, 7, 9.5, 2.5)),
        shell(poly([f(0, -1.5), f(4, -3), f(4, 3), f(0, 1.5)], closed=True, r=0)),
        shell(poly([f(4, -3), f(7, -3), f(7, 3), f(4, 3)], closed=True, r=S.r * 0.5)),
        line(poly([f(7, 0), f(11, 0)])),
    ]


# ============================================================================ floors, doors, windows, records

@icon("lead-paint-test", CAT, "A test swab with a coloured tip pressed against a flake of paint",
      tags=["lead paint test", "lead test kit", "swab", "paint chip", "old paint", "safety test", "renovation hazard"])
def _(S):
    return [
        shell(poly([(4, 17), (12, 15.5), (15, 19.5), (7, 21.5)], closed=True, r=S.r * 0.5)),
        line(seg(20.5, 3, 11.5, 12.5)),
        shell(circle(10, 14, 2.4)),
    ]


@icon("tile-leveling-clip", CAT, "Two tile edges with a clip rising between them and a wedge pushed through its slot",
      tags=["tile spacer", "leveling clip", "lippage", "tile installation", "wedge", "tiling", "floor tiles"])
def _(S):
    return [
        shell(rect(2.5, 12, 8, 9.5, rr(S, 2))),
        shell(rect(13.5, 12, 8, 9.5, rr(S, 2))),
        line(seg(12, 7, 12, 21.5)),
        shell(rect(8, 2.5, 8, 4.5, rr(S, 1.5))),
        solid("M15 4L21.5 3.6L21.5 6Z"),
    ]


@icon("squeaky-door-hinge", CAT, "A door hinge with an oil can nozzle dripping onto its pin",
      tags=["squeaky hinge", "oil hinge", "lubricate", "door noise", "oil can", "door repair", "creaky door"])
def _(S):
    return [
        line(poly([(21, 2.5), (15.5, 2.5), (12, 5.5)], r=S.r)),
        drop(12, 7, 3, 1.1),
        shell(rect(2.5, 12, 8, 9.5, rr(S, 2))),
        shell(rect(13.5, 12, 8, 9.5, rr(S, 2))),
        shell(rect(10, 11, 4, 11, rr(S, 1.5))),
        dot(6, 16.7, 1.1), dot(18, 16.7, 1.1),
    ]


@icon("sticking-door", CAT, "A door in its frame rubbing at the top corner with a small friction burst",
      tags=["sticking door", "jammed door", "door rubbing", "door won't close", "swollen door", "planing", "door repair"])
def _(S):
    star = [polar(19.5, 6, 2.6 if i % 2 == 0 else 1.2, -90 + i * 45) for i in range(8)]
    return [
        line(poly([(3, 22), (3, 3), (21, 3), (21, 22)], r=S.r)),
        shell(rect(6, 6.5, 12.5, 15, rr(S, 2))),
        dot(9.5, 14, 1.1),
        solid(poly(star, closed=True)),
    ]


@icon("broken-window-pane", CAT, "A window pane shattered into cracks radiating from an impact point",
      tags=["broken window", "shattered glass", "cracked pane", "glass repair", "window damage", "impact", "glazing"])
def _(S):
    spokes = []
    for a in (10, 80, 150, 225, 295):
        spokes.append(detail(poly([(12, 12), polar(12, 12, 4.2, a + 12), polar(12, 12, 8.8, a)])))
    return [shell(rect(2.5, 2.5, 19, 19, rr(S, 3))), *spokes]


@icon("window-glazing-putty", CAT, "A window pane corner with a putty knife smoothing a putty bead along the glass edge",
      tags=["glazing putty", "window putty", "putty knife", "glass fitting", "sash repair", "bead", "window repair"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 12, 12, rr(S, 2))),
        solid(rect(2.5, 16.5, 12, 2)),
        *knife(S, 14, 17.5, -30, 5, 4, 3),
    ]


@icon("screen-spline-roller", CAT, "A tool with a wheel at each end of a handle pressing spline cord into a screen frame groove",
      tags=["spline roller", "screen repair", "window screen", "screen tool", "rescreening", "spline", "mesh"])
def _(S):
    return [
        shell(rect(9.5, 2.5, 5, 10, rr(S, 2.5))),
        line(seg(12, 12.5, 12, 17)),
        line(seg(8.3, 17, 15.7, 17)),
        shell(circle(5.5, 17, 2.8)),
        shell(circle(18.5, 17, 2.8)),
        line(seg(2.5, 22, 21.5, 22)),
    ]


@icon("torn-window-screen", CAT, "A window screen frame with mesh lines and a ragged tear across its middle",
      tags=["torn screen", "ripped mesh", "screen repair", "insect screen", "fly screen", "hole in screen", "window screen"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 3))),
        detail(seg(8.5, 2.5, 8.5, 7)),
        detail(seg(15.5, 17, 15.5, 21.5)),
        detail(poly([(5, 15), (9, 11), (11.5, 14), (14.5, 9), (19, 12)])),
    ]


@icon("garage-door-torsion-spring", CAT, "The top of a garage door with a long coiled spring on a shaft running across above it",
      tags=["torsion spring", "garage door spring", "coil spring", "garage repair", "overhead door", "shaft", "spring replacement"])
def _(S):
    return [
        line(seg(2.5, 8, 21.5, 8)),
        line(seg(5, 4.5, 7.5, 11.5)),
        line(seg(8.5, 4.5, 11, 11.5)),
        line(seg(12, 4.5, 14.5, 11.5)),
        line(seg(15.5, 4.5, 18, 11.5)),
        shell(rect(2.5, 14.5, 19, 7, rr(S, 2))),
        detail(seg(12, 14.5, 12, 21.5)),
    ]


@icon("lock-rekeying", CAT, "A lock cylinder cut open to show pins of different heights with a new key entering",
      tags=["rekey", "lock cylinder", "pin tumbler", "locksmith", "new key", "lock change", "security"])
def _(S):
    return [
        shell(rect(2.5, 4, 13.5, 14, rr(S, 3))),
        detail(seg(6, 4, 6, 9)),
        detail(seg(9.5, 4, 9.5, 12)),
        detail(seg(13, 4, 13, 7.5)),
        detail(seg(5.5, 14.5, 15, 14.5)),
        line(seg(16, 14.5, 18.2, 14.5)),
        dot(20, 14.5, 1.6),
    ]


@icon("shelf-mounting", CAT, "A wall shelf with a spirit level resting on top and support brackets beneath it",
      tags=["mount shelf", "spirit level", "shelf bracket", "wall mounting", "diy", "level shelf", "hanging shelf"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 5, rr(S, 2))),
        dot(12, 6, 1.1),
        shell(rect(2.5, 10.5, 19, 3, rr(S, 1.5))),
        line(poly([(6, 13.5), (6, 20), (11, 13.5)], r=S.r)),
        line(poly([(18, 13.5), (18, 20), (13, 13.5)], r=S.r)),
    ]


@icon("maintenance-request", CAT, "A form sheet with a small house at the top, lines of text and a wrench in the corner",
      tags=["maintenance request", "repair request", "work order", "landlord form", "service ticket", "fault report", "form"])
def _(S):
    return [
        shell(poly([(3, 2.5), (11, 2.5), (16, 7.5), (16, 21.5), (3, 21.5)], closed=True, r=S.r * 0.6)),
        detail(poly([(5.5, 11.5), (9.5, 8), (13.5, 11.5)])),
        detail(seg(5.5, 15, 13.5, 15)),
        detail(seg(5.5, 18.2, 11, 18.2)),
        line(arc(19.5, 14, 2.5, -50, 230)),
        line(seg(19.5, 16.5, 19.5, 22)),
    ]


@icon("home-maintenance-calendar", CAT, "A calendar page with a small house and a wrench marked on its days",
      tags=["maintenance calendar", "home schedule", "seasonal tasks", "upkeep planner", "service dates", "reminders", "home care"])
def _(S):
    return [
        shell(rect(3, 4.5, 18, 17, rr(S, 3))),
        detail(seg(3, 9.5, 21, 9.5)),
        line(seg(8, 2, 8, 6.5)),
        line(seg(16, 2, 16, 6.5)),
        knock(poly([(5.5, 18.5), (5.5, 15.5), (8, 13), (10.5, 15.5), (10.5, 18.5)], closed=True)),
        knock(bar(14, 18.5, 18.5, 14, 1.6)),
        dot(19, 13.8, 1.4),
    ]


@icon("repair-estimate", CAT, "A document with a wrench and screwdriver crossed at the top and itemised lines ending in a total",
      tags=["repair estimate", "quote", "repair quote", "cost estimate", "invoice", "tradesman quote", "price list"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 19, rr(S, 3))),
        knock(bar(7.5, 5.5, 16, 11, 1.6)),
        knock(bar(16.5, 5.5, 8, 11, 1.6)),
        dot(16.5, 5.5, 1.6), dot(7.5, 5.5, 1.6),
        detail(seg(7, 14.5, 17, 14.5)),
        detail(seg(11, 18.2, 17, 18.2)),
    ]


@icon("before-after-renovation", CAT, "A house outline split down the middle, the left half cracked and the right half clean",
      tags=["before and after", "renovation", "makeover", "house restoration", "home improvement", "refurbishment", "transformation"])
def _(S):
    return [
        shell(poly([(3, 21.5), (3, 10.5), (12, 3), (21, 10.5), (21, 21.5)], closed=True, r=S.r)),
        detail(seg(12, 8, 12, 21.5)),
        detail(poly([(5.5, 12), (8.5, 15), (6, 17.5), (8.5, 21.5)])),
        detail(rect(15, 13, 3.5, 3.5)),
    ]


@icon("sash-cord-weight", CAT, "A sash window side with a cord running over a pulley to a hanging cylindrical weight",
      tags=["sash cord", "sash weight", "pulley", "sash window", "window repair", "counterweight", "box sash"])
def _(S):
    return [
        shell(circle(12, 6, 3.2)),
        dot(12, 6, 1.1),
        line(seg(8.8, 6, 8.8, 11)),
        shell(rect(2.5, 11, 7, 10.5, rr(S, 4))),
        line(seg(15.2, 6, 15.2, 13)),
        shell(rect(12.7, 13, 5, 8.5, rr(S, 4))),
    ]


@icon("pop-up-drain-stopper", CAT, "A sink drain in cross-section with a round plug on a stem linked to a horizontal pivot rod",
      tags=["pop up drain", "sink stopper", "pivot rod", "drain plug", "basin waste", "plumbing repair", "clevis"])
def _(S):
    return [
        line(seg(2.5, 6.5, 7, 6.5)),
        line(seg(17, 6.5, 21.5, 6.5)),
        line(seg(7, 6.5, 7, 21.5)),
        line(seg(17, 6.5, 17, 21.5)),
        shell(rect(8.5, 3, 7, 3, rr(S, 1))),
        line(seg(12, 6, 12, 15)),
        line(seg(12, 15, 21.5, 15)),
        dot(17, 15, 1.5),
    ]
