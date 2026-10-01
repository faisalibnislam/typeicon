"""TypeIcon Core: home maintenance (plumbing, damp, pests, electrics, roofing), batch 001."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar

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


# ============================================================================ plumbing and leaks

@icon("roof-leak-bucket", CAT, "A drop falling from a sloped roof into a bucket on the floor",
      tags=["roof leak", "leaking roof", "bucket", "drip", "water damage", "ceiling leak", "repair"])
def _(S):
    return [
        line(poly([(2.5, 9), (12, 3.5), (21.5, 9)], r=S.r)),
        drop(12, 8, 4.4, 1.5),
        shell(poly([(6.5, 14.5), (17.5, 14.5), (16, 21), (8, 21)], closed=True, r=S.r)),
        detail(seg(8, 17.5, 16, 17.5)),
    ]


@icon("ceiling-water-stain", CAT, "A ceiling panel with a ring-shaped water stain and a drop hanging from it",
      tags=["ceiling stain", "water stain", "leak", "water damage", "drip", "plumbing leak", "damp"])
def _(S):
    return [
        shell(poly([(5.5, 3), (18.5, 3), (22, 11), (2, 11)], closed=True, r=S.r)),
        detail(ellipse(12, 7, 4, 1.8)) if S.name == "rounded" else detail(poly([(8, 7), (12, 5), (16, 7), (12, 9)], closed=True)),
        drop(12, 14, 6, 2),
    ]


@icon("pipe-repair-clamp", CAT, "A pipe wrapped by a band clamp with a bolt tab, drops stopped beneath it",
      tags=["pipe clamp", "pipe repair", "leak fix", "band clamp", "plumbing repair", "burst pipe", "seal"])
def _(S):
    return [
        line(seg(2, 7, 8, 7)), line(seg(2, 14, 8, 14)),
        line(seg(16, 7, 22, 7)), line(seg(16, 14, 22, 14)),
        shell(rect(8, 5, 8, 11, rr(S, 3))),
        line(poly([(10, 5), (10, 2.5), (14, 2.5), (14, 5)], r=S.r * 0.5)),
        drop(12, 17.5, 5, 1.7),
    ]


@icon("toilet-flapper", CAT, "A round rubber flapper disc with a hinge arm and a short chain",
      tags=["flapper", "toilet repair", "tank flapper", "flush valve", "rubber seal", "cistern", "plumbing part"])
def _(S):
    return [
        shell(circle(13, 15, 6.5)),
        detail(circle(13, 15, 2)),
        line(poly([(7.5, 12), (3.5, 9.5), (3.5, 5)], r=S.r)),
        line(seg(13, 8.5, 13, 6)),
        line(circle(13, 4, 2)) if S.name == "rounded" else line(rect(11.5, 2.5, 3, 3)),
    ]


@icon("toilet-fill-valve", CAT, "A tall fill valve tube with a float cup and a curled refill hose",
      tags=["fill valve", "ballcock", "toilet repair", "cistern valve", "float cup", "tank refill", "plumbing part"])
def _(S):
    return [
        line(poly([(9.5, 11), (9.5, 6), (14.5, 6), (14.5, 11)], r=S.r)),
        line(seg(9.5, 18, 9.5, 21.5)), line(seg(14.5, 18, 14.5, 21.5)),
        shell(rect(4.5, 11, 15, 7, rr(S, 3))),
        line(poly([(12, 6), (12, 3), (19.5, 3), (19.5, 8)], r=S.r)),
    ]


@icon("toilet-wax-ring", CAT, "A thick wax ring seal with a plastic horn funnel at its center",
      tags=["wax ring", "toilet seal", "toilet installation", "closet flange", "plumbing seal", "bowl gasket", "toilet repair"])
def _(S):
    return [
        shell(ellipse(12, 16, 9.5, 5)),
        detail(ellipse(12, 16, 4.6, 1.8)),
        line(poly([(9.6, 15), (10.8, 7.5), (13.2, 7.5), (14.4, 15)], r=S.r)),
    ]

@icon("running-toilet", CAT, "A toilet with flow lines in the bowl and a circular arrow beside the tank",
      tags=["running toilet", "toilet keeps running", "water waste", "continuous flush", "leaking toilet", "cistern", "plumbing"])
def _(S):
    return [
        shell(rect(3, 3, 7, 8, rr(S, 3))),
        shell(poly([(3, 13), (21, 13), (20, 17), (16, 19), (16, 21.5), (6.5, 21.5), (6.5, 13)], closed=True, r=S.r)),
        line(wave(8.5, 16.5, 2, 3.5, 1.2)),
        line(arc(16, 6.5, 3.5, 40, 330)),
        line(poly([(20, 3), (20, 5.5), (17.5, 5.5)], r=S.r * 0.5)),
    ]


@icon("clogged-toilet", CAT, "A toilet bowl filled to the rim with a plunger standing in it",
      tags=["clogged toilet", "blocked toilet", "overflow", "plunger", "toilet blockage", "plumbing problem", "bathroom"])
def _(S):
    return [
        shell(rect(3, 3, 6, 8, rr(S, 3))),
        shell(poly([(3, 13), (21, 13), (20, 17), (16, 19), (16, 21.5), (6.5, 21.5), (6.5, 13)], closed=True, r=S.r)),
        line(seg(16, 3, 16, 12)),
        line(poly([(13, 17), (13.5, 14), (18.5, 14), (19, 17)], r=S.r * 0.5)),
    ]


@icon("clogged-drain", CAT, "A sink drain with water pooled above it and a hair clump blocking the pipe",
      tags=["clogged drain", "blocked drain", "hair clog", "slow drain", "sink blockage", "plumbing problem", "plug hole"])
def _(S):
    return [
        line(poly([(2.5, 3), (2.5, 9.5), (8, 9.5)], r=S.r)),
        line(poly([(21.5, 3), (21.5, 9.5), (16, 9.5)], r=S.r)),
        line(wave(4.5, 6, 4, 3.8, 1.3)),
        line(seg(8, 9.5, 8, 21)),
        line(seg(16, 9.5, 16, 21)),
        solid(ellipse(12, 16.5, 3, 2.2)),
        line(seg(9, 15, 7.5, 13.5)), line(seg(15, 15, 16.5, 13.5)),
    ]


@icon("accordion-plunger", CAT, "A plunger with a ribbed bellows body on a straight handle",
      tags=["accordion plunger", "bellows plunger", "toilet plunger", "drain plunger", "unblock", "clog", "plumbing tool"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 7)),
        shell(poly([(9, 7), (15, 7), (14, 11), (16, 15), (19, 20.5), (5, 20.5), (8, 15), (10, 11)], closed=True, r=S.r)),
        detail(seg(9.8, 11, 14.2, 11)),
        detail(seg(8.5, 15, 15.5, 15)),
    ]


@icon("drain-hair-remover", CAT, "A thin barbed plastic strip with a ring pull for lifting hair out of drains",
      tags=["drain snake", "hair catcher", "drain cleaner", "zip strip", "hair removal tool", "unclog", "sink"])
def _(S):
    pts = [(10.5, 8), (13.5, 8)]
    for y in (10, 14.5, 19):
        pts += [(13.5, y), (16, y + 1.5), (13.5, y + 3)]
    pts += [(13.5, 22), (10.5, 22)]
    for y in (19, 14.5, 10):
        pts += [(10.5, y + 3), (8, y + 1.5), (10.5, y)]
    return [
        line(circle(12, 4.5, 2.5)) if S.name == "rounded" else line(rect(9.5, 2, 5, 5)),
        shell(poly(pts, closed=True), stroke_miterlimit="2"),
    ]

@icon("faucet-cartridge", CAT, "An upright valve cartridge with a splined stem and two o-ring bands",
      tags=["cartridge", "tap cartridge", "faucet repair", "mixer valve", "o-ring", "replacement part", "plumbing part"])
def _(S):
    return [
        shell(rect(9.5, 2.5, 5, 3.5, 1 if S.name == "rounded" else 0)),
        shell(rect(6.5, 6, 11, 15.5, rr(S, 3))),
        detail(seg(6.5, 11, 17.5, 11)),
        detail(seg(6.5, 16, 17.5, 16)),
    ]


@icon("faucet-aerator", CAT, "A small round threaded aerator cap showing its mesh screen",
      tags=["aerator", "tap aerator", "faucet filter", "water saver", "mesh screen", "faucet repair", "spout cap"])
def _(S):
    return [
        shell(ellipse(12, 8, 9, 4.5)),
        line(seg(3, 8, 3, 15.5)),
        line(seg(21, 8, 21, 15.5)),
        line("M3 15.5A9 4.5 0 0 0 21 15.5"),
        detail(seg(8, 8, 16, 8)),
        detail(seg(12, 6, 12, 10)),
    ]


@icon("compression-fitting", CAT, "A pipe end with a ferrule ring and a hex nut shown apart, ready to slide on",
      tags=["compression nut", "ferrule", "olive ring", "pipe fitting", "plumbing joint", "exploded view", "pipe connector"])
def _(S):
    return [
        line(seg(2, 8.5, 6.5, 8.5)), line(seg(2, 15.5, 6.5, 15.5)),
        shell(rect(9, 7.5, 3, 9, rr(S, 1))),
        shell(rect(15, 5.5, 7, 13, rr(S, 3))),
        detail(seg(18.5, 5.5, 18.5, 18.5)),
    ]


@icon("soldering-copper-pipe", CAT, "A copper pipe joint with a torch flame below and a solder wire touching the seam",
      tags=["soldering", "sweating pipe", "copper pipe", "torch", "plumbing joint", "solder wire", "brazing"])
def _(S):
    return [
        line(seg(2, 8.5, 8.5, 8.5)), line(seg(2, 14.5, 8.5, 14.5)),
        line(seg(15.5, 8.5, 22, 8.5)), line(seg(15.5, 14.5, 22, 14.5)),
        shell(rect(8.5, 6.5, 7, 10, rr(S, 1.5))),
        line(poly([(21.5, 2.5), (17, 5.5)], r=0)),
        solid("M12 17.5C12 19 9.8 19.8 9.8 21A2.2 2.2 0 0 0 14.2 21C14.2 19.8 12 19 12 17.5Z"),
    ]


@icon("pipe-flaring-tool", CAT, "A clamp bar holding a tube end with a screw yoke and cone pressing into it",
      tags=["flaring tool", "flare tool", "tube flaring", "copper tube", "brake line", "hvac tool", "pipe tool"])
def _(S):
    return [
        line(poly([(5, 15), (5, 6.5), (19, 6.5), (19, 15)], r=S.r)),
        line(seg(12, 2.5, 12, 6.5)),
        line(seg(9, 2.5, 15, 2.5)),
        solid(poly([(9.5, 10), (14.5, 10), (12, 15)], closed=True)),
        shell(rect(2.5, 15, 19, 6, rr(S, 3))),
        dot(8, 18, 1), dot(16, 18, 1),
    ]


@icon("pex-tubing-coil", CAT, "A flat coil of flexible tubing with its loose end trailing off to one side",
      tags=["pex", "pex pipe", "tubing coil", "flexible pipe", "water line", "plumbing supply", "hose coil"])
def _(S):
    return [
        line(circle(10.5, 11, 8)),
        line(circle(10.5, 11, 3.5)),
        line("M10.5 19C14 20.5 18 21.5 22 19.5"),
    ]


@icon("pvc-cement-can", CAT, "A small can of pipe cement with its lid lifted on a dauber stem",
      tags=["pvc cement", "solvent cement", "pipe glue", "primer", "dauber", "plumbing adhesive", "glue can"])
def _(S):
    return [
        shell(rect(3, 4, 13, 3.5, rr(S, 1.5))),
        line(seg(9.5, 7.5, 9.5, 12)),
        shell(rect(3, 12, 13, 9.5, rr(S, 3))),
        detail(seg(3, 16.5, 16, 16.5)),
    ]


@icon("sewer-backup", CAT, "A floor drain grate with water bubbling up around it and an arrow rising above",
      tags=["sewer backup", "drain overflow", "backed up drain", "floor drain", "sewage", "flood", "plumbing emergency"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 9)),
        line(poly([(8.5, 5.5), (12, 2.5), (15.5, 5.5)], r=S.r)),
        shell(ellipse(12, 17, 9.5, 4.5)),
        detail(seg(7.5, 17, 16.5, 17)),
        dot(5.5, 11, 1.3), dot(18.5, 11, 1.3),
    ]


@icon("septic-tank-pumping", CAT, "A buried tank under the ground line with a thick suction hose reaching into it",
      tags=["septic tank", "septic pumping", "pump out", "suction hose", "underground tank", "sewage", "wastewater"])
def _(S):
    return [
        shell(rect(10, 2.5, 4, 7, rr(S, 1.5))),
        line(seg(2, 10, 10, 10)), line(seg(14, 10, 22, 10)),
        shell(rect(3, 13, 18, 8.5, rr(S, 3))),
        line(seg(12, 10, 12, 18)),
    ]


@icon("sewer-cleanout", CAT, "A short pipe stub rising from the ground line capped by a square-headed plug",
      tags=["cleanout", "sewer cleanout", "drain access", "cleanout plug", "sewer line", "pipe cap", "plumbing access"])
def _(S):
    return [
        shell(rect(10, 2.5, 4, 4, 0)),
        shell(rect(8, 6.5, 8, 9.5, rr(S, 1.5))),
        detail(seg(8, 10, 16, 10)),
        line(seg(2, 16, 8, 16)), line(seg(16, 16, 22, 16)),
        line(seg(8, 16, 8, 21.5)), line(seg(16, 16, 16, 21.5)),
    ]


@icon("drain-inspection-camera", CAT, "A cable reel with a small monitor on top and a camera head at the end of the cable",
      tags=["drain camera", "sewer camera", "pipe inspection", "borescope", "push cable", "plumbing inspection", "cctv drain"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 11, 7, rr(S, 3))),
        line(seg(9, 9.5, 9, 12)),
        shell(circle(9, 17, 5.5)),
        dot(9, 17, 1.5),
        line(seg(14.5, 17, 17, 17)),
        shell(poly([(17, 14), (20.5, 14), (22, 17), (20.5, 20), (17, 20)], closed=True, r=S.r)),
    ]


@icon("drain-jetting", CAT, "A pipe cross-section with a bullet-shaped nozzle spraying water jets backward",
      tags=["drain jetting", "hydro jetting", "water jet", "pipe cleaning", "sewer cleaning", "high pressure", "nozzle"])
def _(S):
    return [
        line(seg(2, 4.5, 22, 4.5)), line(seg(2, 19.5, 22, 19.5)),
        shell("M10 9.5H16Q20.5 9.5 20.5 12Q20.5 14.5 16 14.5H10Z"),
        line(seg(8, 9.5, 3, 7.5)), line(seg(8, 12, 3, 12)), line(seg(8, 14.5, 3, 16.5)),
    ]


@icon("leaking-water-heater", CAT, "A tall water heater tank with a flue on top and a puddle with drops at its base",
      tags=["water heater leak", "leaking tank", "hot water tank", "boiler leak", "water damage", "puddle", "plumbing problem"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 4)),
        shell(rect(6, 4, 12, 10.5, rr(S, 4))),
        detail(seg(6, 8.5, 18, 8.5)),
        drop(9, 16.5, 3.4, 1.2), drop(15, 16.5, 3.4, 1.2),
        line(seg(3, 22, 21, 22)),
    ]


@icon("water-heater-blanket", CAT, "A tall water heater tank wrapped in a quilted insulation jacket with two straps",
      tags=["tank insulation", "heater jacket", "insulation blanket", "energy saving", "hot water tank", "quilted wrap", "heat loss"])
def _(S):
    return [
        shell(rect(5.5, 3, 13, 18.5, rr(S, 4))),
        detail(seg(5.5, 8.5, 18.5, 8.5)),
        detail(seg(5.5, 15.5, 18.5, 15.5)),
        dot(12, 12, 1.2),
    ]


@icon("water-heater-anode-rod", CAT, "A long rod with a hex head at the top and a pitted, corroded lower half",
      tags=["anode rod", "sacrificial anode", "magnesium rod", "tank corrosion", "water heater part", "rust", "maintenance"])
def _(S):
    return [
        shell(rect(8.5, 2.5, 7, 4, rr(S, 1))),
        shell(poly([(10.5, 6.5), (13.5, 6.5), (13.5, 12), (15.5, 13.5), (13.5, 15), (15.5, 16.5), (13.5, 18), (13.5, 21.5),
                    (10.5, 21.5), (10.5, 18), (8.5, 16.5), (10.5, 15), (8.5, 13.5), (10.5, 12)], closed=True, r=S.r * 0.3)),
    ]


@icon("clogged-showerhead", CAT, "A showerhead with blocked nozzles marked by scale dots and a single thin jet",
      tags=["showerhead", "limescale", "blocked nozzle", "weak shower", "scale buildup", "descale", "bathroom"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 5)),
        shell("M3 12A9 7 0 0 1 21 12Z"),
        dot(6.5, 15, 1.5), dot(17.5, 15, 1.5),
        line(seg(12, 15, 12, 21.5)),
    ]


@icon("pipe-heat-cable", CAT, "A pipe with a heating cable wound around it in a spiral, ending in a plug",
      tags=["heat tape", "pipe heating", "freeze protection", "frozen pipes", "winterize", "heating cable", "insulation"])
def _(S):
    return [
        shell(rect(2.5, 7, 15, 8, rr(S, 3))),
        line(seg(5.5, 5, 8, 17)), line(seg(11, 5, 13.5, 17)),
        line("M13.5 17C14 20.5 16 20.5 17.5 20.5"),
        shell(rect(17.5, 18.5, 4.5, 4, rr(S, 1.5))),
    ]


@icon("outdoor-faucet-cover", CAT, "A dome-shaped foam cover strapped over an outdoor spigot on a wall",
      tags=["faucet cover", "spigot cover", "hose bib cover", "winterize", "freeze protection", "outdoor tap", "insulation"])
def _(S):
    return [
        line(seg(3, 2.5, 3, 21.5)),
        shell("M4.5 6H12A7 7 0 0 1 19 13V19H4.5Z"),
        detail(seg(11, 6, 11, 19)),
    ]


@icon("washing-machine-leak", CAT, "A front-loading washing machine with water and drops spreading out from under its front",
      tags=["washer leak", "washing machine leak", "laundry flood", "appliance leak", "puddle", "water damage", "drain hose"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 13, rr(S, 3))),
        detail(circle(12, 9.5, 3)),
        drop(9, 17, 3.4, 1.2), drop(15, 17, 3.4, 1.2),
        line(seg(2.5, 22, 21.5, 22)),
    ]


@icon("mold-remediation", CAT, "A person in a respirator mask spraying a patch of speckled mould on a wall",
      tags=["mould removal", "mold removal", "respirator", "mold cleanup", "spray cleaner", "wall mold", "hazmat"])
def _(S):
    return [
        shell(circle(7.5, 6.5, 3.8)),
        solid(poly([(4.5, 7.5), (10.5, 7.5), (9.5, 10.5), (5.5, 10.5)], closed=True)),
        line(poly([(2.5, 22), (2.5, 17), (7.5, 13.5), (12.5, 17), (12.5, 22)], r=S.r)),
        line(seg(12, 15, 15, 12.5)),
        line(seg(21.5, 2.5, 21.5, 21.5)),
        dot(18.5, 8, 1.2), dot(19, 12, 1.2), dot(18, 16, 1.2), dot(16.5, 5.5, 1),
    ]


@icon("mold-test-kit", CAT, "A petri dish with fuzzy colony spots next to a sampling swab",
      tags=["mold test", "mould test", "petri dish", "swab", "air quality sample", "spore test", "home inspection"])
def _(S):
    return [
        shell(ellipse(9.5, 13, 8, 4.5)),
        line(seg(1.5, 13, 1.5, 18)), line(seg(17.5, 13, 17.5, 18)),
        line("M1.5 18A8 4.5 0 0 0 17.5 18"),
        dot(7, 12.5, 1.2), dot(11.5, 12.5, 1.2),
        line(seg(21.5, 3, 17.5, 7)),
        dot(17, 7.5, 1.6),
    ]


@icon("rising-damp", CAT, "A wall with a wavy tide mark near the bottom and arrows rising from the floor",
      tags=["rising damp", "damp wall", "tide mark", "moisture", "damp course", "wall damp", "water damage"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 3))),
        detail(wave(5.5, 9.5, 4, 3.25, 1.2)),
        detail(poly([(8, 18), (8, 14)], r=0)), detail(poly([(5.5, 15.5), (8, 13), (10.5, 15.5)], r=0)),
        detail(poly([(16, 18), (16, 14)], r=0)), detail(poly([(13.5, 15.5), (16, 13), (18.5, 15.5)], r=0)),
    ]


@icon("peeling-paint", CAT, "A wall surface with paint flakes curling away from it, one large curl in the center",
      tags=["peeling paint", "flaking paint", "paint failure", "blistering", "wall repair", "repaint", "scraping"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 3))),
        detail("M6.5 9H14.5A3 3 0 0 1 14.5 15H11"),
        detail(seg(6.5, 17.5, 9.5, 17.5)),
        detail(seg(16.5, 18, 18.5, 18)),
    ]


@icon("brick-efflorescence", CAT, "A small brick wall panel with white crystalline bloom spreading over the lower bricks",
      tags=["efflorescence", "salt bloom", "white deposit", "brickwork", "masonry damp", "salt staining", "brick repair"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 18, rr(S, 3))),
        detail(seg(2.5, 9, 21.5, 9)), detail(seg(2.5, 15, 21.5, 15)),
        detail(seg(12, 3, 12, 9)), detail(seg(7, 9, 7, 15)), detail(seg(17, 9, 17, 15)),
        dot(5, 18.2, 1), dot(9, 18.2, 1), dot(15, 18.2, 1), dot(19, 18.2, 1),
    ]


@icon("damp-proof-injection", CAT, "A wall base with a row of drilled holes and an injection gun filling one of them",
      tags=["damp proof course", "dpc injection", "damp proofing", "injection gun", "cream injection", "rising damp treatment", "wall treatment"])
def _(S):
    return [
        shell(rect(15, 2.5, 7, 6, rr(S, 3))),
        line(seg(18.5, 8.5, 18.5, 16.5)),
        shell(rect(2.5, 12, 19, 9.5, rr(S, 3))),
        dot(6, 17, 1.3), dot(12, 17, 1.3),
    ]


@icon("flooded-basement", CAT, "A house cross-section with water filling the basement level and waves on its surface",
      tags=["flooded basement", "basement flood", "water damage", "sump pump failure", "flood", "wet cellar", "house flooding"])
def _(S):
    return [
        shell(poly([(4, 10), (12, 3), (20, 10), (20, 21.5), (4, 21.5)], closed=True, r=S.r)),
        detail(wave(5.5, 15.5, 4, 3.25, 1.2)),
    ]


def capsule(x1, y1, x2, y2, w=3.0):
    """Solid rounded pellet along a short segment."""
    return solid(path_to_d(ST(seg(x1, y1, x2, y2), w, "round", "round")))


@icon("dry-rot", CAT, "A wooden beam end split into cube-shaped cracks with fungal strands growing from it",
      tags=["dry rot", "wood rot", "fungus", "rotten timber", "cubical cracking", "timber decay", "structural damage"])
def _(S):
    return [
        shell(rect(2.5, 4, 15, 15, rr(S, 3))),
        detail(poly([(8, 4), (8, 10), (13, 10), (13, 14)], r=S.r * 0.5)),
        detail(poly([(2.5, 14), (8, 14), (8, 19)], r=S.r * 0.5)),
        line("M17.5 9.5Q20.5 9.5 21.5 6"),
        line("M17.5 14.5Q20.5 14.5 21.5 18"),
    ]


@icon("rotten-window-sill", CAT, "A window frame corner with a crumbling, chunked-out sill and a screwdriver probing it",
      tags=["rotten sill", "window rot", "wood rot", "window repair", "crumbling wood", "carpentry repair", "probe"])
def _(S):
    return [
        line(seg(5, 2.5, 5, 12.5)),
        shell(poly([(2.5, 13), (21.5, 13), (21.5, 16.5), (18.5, 16.5), (17, 19.5), (14, 17.5), (12, 20.5), (9, 18), (6.5, 20), (2.5, 16.5)],
                   closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
        line(seg(20.5, 4.5, 15, 11.5)),
        solid(poly([(17.8, 3.2), (20, 1.8), (22, 4.2), (19.8, 5.6)], closed=True)),
    ]


@icon("broken-floorboard", CAT, "A row of floorboards seen from above with one board cracked through to a jagged hole",
      tags=["broken floorboard", "floor repair", "cracked board", "hole in floor", "rotten floor", "wood floor", "subfloor"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 3))),
        detail(seg(2.5, 8.5, 21.5, 8.5)), detail(seg(2.5, 15.5, 21.5, 15.5)),
        detail(seg(15, 2.5, 15, 8.5)), detail(seg(8, 15.5, 8, 21.5)),
        Part("dot", poly([(6, 11), (10, 10.2), (11.2, 12), (14, 10.4), (17, 11.3), (15.4, 13.4), (11, 14), (8, 13.4)], closed=True)),
    ]


@icon("window-trickle-vent", CAT, "The top of a window frame with a slotted vent strip and airflow lines passing through",
      tags=["trickle vent", "window vent", "ventilation", "airflow", "condensation", "slot vent", "window frame"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 9, rr(S, 3))),
        detail(seg(6, 7, 10.5, 7)), detail(seg(13.5, 7, 18, 7)),
        line("M8 14q-1.6 2.3 0 4.5t0 3"),
        line("M16 14q-1.6 2.3 0 4.5t0 3"),
    ]


@icon("termite-damage", CAT, "A cut wooden beam end with a maze of hollow galleries eaten through the grain",
      tags=["termite damage", "wood eaten", "hollow wood", "insect damage", "timber damage", "pest damage", "galleries"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 18, rr(S, 3))),
        detail(poly([(7, 3), (7, 12), (13, 12), (13, 7), (17.5, 7), (17.5, 14)], r=S.r * 0.5)),
        detail(poly([(2.5, 17), (9, 17), (9, 21)], r=S.r * 0.5)),
        detail(poly([(13, 21), (13, 17), (21.5, 17)], r=S.r * 0.5)),
    ]


@icon("termite-bait-station", CAT, "A round stake pushed into the ground with a flat cap and a slot on its side",
      tags=["bait station", "termite bait", "termite stake", "ground stake", "pest control", "monitoring station", "termite treatment"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 13, 3.5, rr(S, 1.5))),
        shell(rect(8, 6, 8, 15.5, rr(S, 1))),
        detail(seg(12, 8.5, 12, 12)),
        line(seg(2, 14.5, 8, 14.5)), line(seg(16, 14.5, 22, 14.5)),
    ]


@icon("termite-mud-tubes", CAT, "A foundation wall with thin branching earthen tubes climbing up from the ground",
      tags=["mud tubes", "termite tubes", "shelter tubes", "termite signs", "foundation pest", "termite inspection", "earthen tunnels"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 17, rr(S, 3))),
        detail(poly([(8, 20), (8, 14), (13, 9), (13, 3)], r=S.r * 0.5)),
        detail(poly([(8, 14), (5, 10.5)], r=0)),
        detail(poly([(18, 20), (18, 14)], r=0)),
    ]


@icon("mouse-droppings", CAT, "A small cluster of elongated pellets scattered on a floor line",
      tags=["mouse droppings", "rodent droppings", "pest signs", "rat poop", "pellets", "infestation sign", "rodent control"])
def _(S):
    return [
        line(seg(2, 21, 22, 21)),
        capsule(5, 17, 8.5, 16, 3),
        capsule(11, 17.5, 14.5, 17.5, 3),
        capsule(16.5, 16, 19.5, 17, 3),
        capsule(7.5, 11.5, 10.5, 10.5, 3),
        capsule(13.5, 12, 16.5, 11, 3),
    ]


@icon("gnawed-cable", CAT, "An electric cable with bite notches in the insulation and bare copper strands showing",
      tags=["gnawed cable", "chewed wire", "rodent damage", "exposed wire", "damaged cable", "electrical hazard", "mouse chewed"])
def _(S):
    body = path_to_d(D(P(rect(2, 8, 13, 8, 0)), P(circle(6, 8, 2.2)), P(circle(11.5, 8, 2.2)), P(circle(8.5, 16, 2.2))))
    return [
        shell(body, stroke_miterlimit="2"),
        line("M15 10.5Q18 8 22 7.5"),
        line(seg(15, 12, 22, 12)),
        line("M15 13.5Q18 16 22 16.5"),
    ]


@icon("mouse-hole", CAT, "A baseboard with a small arched hole gnawed at the bottom, dark inside",
      tags=["mouse hole", "rodent entry", "baseboard gap", "rat hole", "pest entry point", "gap in wall", "skirting board"])
def _(S):
    return [
        shell(rect(2.5, 7, 19, 14, rr(S, 3))),
        Part("dot", "M8.5 21V16.5A3.5 3.5 0 0 1 15.5 16.5V21Z"),
    ]


@icon("rat-bait-station", CAT, "A low rectangular bait box with two round entry holes and a keyhole on the lid",
      tags=["bait box", "rat bait", "rodent station", "tamper resistant", "pest control", "rodenticide", "bait trap"])
def _(S):
    return [
        shell(rect(2.5, 5, 19, 15.5, rr(S, 3))),
        detail(seg(2.5, 10, 21.5, 10)),
        dot(12, 7.5, 1.1),
        dot(7.5, 15.5, 2), dot(16.5, 15.5, 2),
    ]


@icon("ultrasonic-pest-repeller", CAT, "A small plug-in device on a wall with curved sound waves radiating from its front",
      tags=["pest repeller", "ultrasonic repeller", "plug-in repeller", "rodent repellent", "sound waves", "pest deterrent", "electronic repellent"])
def _(S):
    return [
        line(seg(2.5, 2.5, 2.5, 21.5)),
        shell(rect(4, 6, 8, 12, rr(S, 3))),
        detail(seg(8, 9.5, 8, 14.5)),
        line(arc(12.5, 12, 5.5, -45, 45)),
        line(arc(12.5, 12, 9.5, -45, 45)),
    ]


@icon("bird-netting", CAT, "A building ledge with a taut square-mesh net stretched across the opening",
      tags=["bird netting", "bird control", "pigeon proofing", "anti-bird net", "eave protection", "bird deterrent", "mesh"])
def _(S):
    return [
        shell(rect(2.5, 4, 19, 14, rr(S, 1.5))),
        detail(seg(8, 4, 8, 18)), detail(seg(12, 4, 12, 18)), detail(seg(16, 4, 16, 18)),
        detail(seg(2.5, 9, 21.5, 9)), detail(seg(2.5, 13, 21.5, 13)),
        line(seg(1.5, 21.5, 22.5, 21.5)),
    ]


@icon("squirrel-in-attic", CAT, "An attic under a pitched roof with a squirrel sitting inside",
      tags=["squirrel", "attic pest", "roof rodent", "wildlife in attic", "animal removal", "roof space", "nuisance wildlife"])
def _(S):
    return [
        shell(poly([(3.5, 21), (3.5, 12), (12, 3.5), (20.5, 12), (20.5, 21)], closed=True, r=S.r)),
        Part("dot", ellipse(10, 16.5, 2.4, 3.2)),
        Part("dot", circle(10.8, 11.8, 1.8)),
        detail("M11.8 19C17.5 19 17 12.5 14.2 13"),
    ]


def bug(x, y):
    """A tiny insect: a body dot with crossed legs (knocked out of shells in Filled)."""
    return [dot(x, y, 1.5), detail(seg(x - 2.6, y - 1.8, x + 2.6, y + 1.8)), detail(seg(x - 2.6, y + 1.8, x + 2.6, y - 1.8))]


@icon("bedbug-mattress-cover", CAT, "A mattress fully enclosed in a protective cover with a zipper running around its edge",
      tags=["mattress encasement", "bed bug cover", "mattress protector", "zippered cover", "allergen cover", "bedroom", "pest proof"])
def _(S):
    return [
        shell(rect(2, 5, 20, 14, rr(S, 4))),
        detail(rect(6, 9, 12, 6, rr(S, 2))),
        dot(18, 15, 1.2),
    ]


@icon("roach-gel-bait", CAT, "A syringe-style bait applicator with a long thin tip and a row of gel dots below it",
      tags=["gel bait", "cockroach bait", "roach control", "bait syringe", "pest treatment", "applicator", "insecticide gel"])
def _(S):
    return [
        line(seg(2, 5, 2, 11)), line(seg(2, 8, 5, 8)),
        shell(rect(5, 5, 9, 6, rr(S, 3))),
        line(poly([(14, 8), (19, 8), (20.5, 12)], r=S.r)),
        dot(5, 19, 1.4), dot(10, 19, 1.4), dot(15, 19, 1.4), dot(20, 19, 1.4),
    ]


def _flash(pts, deg=40, tx=7.5, ty=6.5):
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    return [(tx + x * c - y * sn, ty + x * sn + y * c) for x, y in pts]


@icon("pest-inspection", CAT, "A flashlight beam shining along a baseboard and revealing a small insect",
      tags=["pest inspection", "flashlight", "insect check", "bug search", "pest survey", "torch", "infestation check"])
def _(S):
    handle = _flash([(-6, -1.8), (2, -1.8), (2, 1.8), (-6, 1.8)])
    head = _flash([(2, -1.8), (5, -3.4), (5, 3.4), (2, 1.8)])
    b1 = _flash([(7, -3.4), (14, -6)])
    b2 = _flash([(7, 3.4), (14, 6)])
    return [
        shell(poly(handle, closed=True, r=S.r * 0.5)),
        shell(poly(head, closed=True, r=S.r * 0.3)),
        line(poly(b1, r=0)), line(poly(b2, r=0)),
        line(seg(11, 21.5, 22, 21.5)),
        *bug(18, 17),
    ]


def rot(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * sn, cy + (x - cx) * sn + (y - cy) * c) for x, y in pts]


@icon("mole-trap", CAT, "A scissor-jaw trap with two looped handles and crossing jaws pointing into a soil mound",
      tags=["mole trap", "scissor trap", "garden pest", "gopher trap", "lawn pest", "soil mound", "animal trap"])
def _(S):
    return [
        line(circle(7.5, 5.5, 3)), line(circle(16.5, 5.5, 3)),
        line(seg(9.5, 8.5, 15.5, 17.5)), line(seg(14.5, 8.5, 8.5, 17.5)),
        line("M2.5 21.5C6.5 16 17.5 16 21.5 21.5"),
    ]


@icon("door-sweep", CAT, "The bottom edge of a door with a brush strip along it, bristles touching the floor",
      tags=["door sweep", "draught excluder", "door brush", "weatherstrip", "door seal", "draft stopper", "gap seal"])
def _(S):
    return [
        line(poly([(7, 15), (7, 2.5), (17, 2.5), (17, 15)], r=S.r)),
        dot(14, 9, 1.2),
        shell(rect(5.5, 15, 13, 3, rr(S, 1))),
        line(seg(7.5, 18, 7.5, 20.5)), line(seg(10.5, 18, 10.5, 20.5)), line(seg(13.5, 18, 13.5, 20.5)), line(seg(16.5, 18, 16.5, 20.5)),
        line(seg(2, 21.5, 22, 21.5)),
    ]

@icon("bug-fogger", CAT, "An upright aerosol can with a cloud of fog billowing from its top nozzle",
      tags=["bug bomb", "fogger", "insecticide fog", "pest treatment", "aerosol can", "fumigation", "pest spray"])
def _(S):
    cloud = path_to_d(U(P(circle(8, 5.5, 2.5)), P(circle(12, 4.5, 3)), P(circle(16, 5.5, 2.5)), P(rect(8, 5.5, 8, 2.5))))
    return [
        shell(cloud),
        solid(rect(10.5, 10, 3, 1.5)),
        shell(rect(7.5, 11.5, 9, 10, rr(S, 3))),
        detail(seg(7.5, 16, 16.5, 16)),
    ]


@icon("house-infestation", CAT, "A simple house outline with small insects crawling over its walls",
      tags=["infestation", "pest infestation", "bugs in house", "insects", "home pests", "cockroaches", "exterminator"])
def _(S):
    return [
        shell(poly([(3.5, 21), (3.5, 11), (12, 3), (20.5, 11), (20.5, 21)], closed=True, r=S.r)),
        *bug(8.5, 15), *bug(15.5, 17.5), *bug(12, 10.5),
    ]


@icon("bulb-duster", CAT, "A squeeze bulb with a long thin nozzle puffing out a small cloud of powder",
      tags=["duster", "puffer", "powder applicator", "insecticide dust", "diatomaceous earth", "bellows duster", "pest control"])
def _(S):
    bulb = shell(circle(8.5, 15, 6)) if S.name == "rounded" else shell(poly(regular(8.5, 15, 6.4, 8, start=22.5), closed=True))
    return [
        bulb,
        solid(poly([(15.83, 10.33), (13.25, 7.51), (11.77, 8.87), (14.35, 11.69)], closed=True)),
        line(seg(14.5, 8.6, 19, 4.6)),
        dot(20.8, 2.8, 1.2), dot(21.4, 6.5, 1.2), dot(17.5, 2.5, 1),
    ]

@icon("bucket-mouse-trap", CAT, "A bucket with a ramp against its rim and a spinning bottle on a wire across the top",
      tags=["bucket trap", "rolling log trap", "diy mouse trap", "humane trap", "rodent trap", "spinner", "pest control"])
def _(S):
    return [
        line(seg(1.5, 21.5, 5.5, 12.5)),
        line(seg(3.5, 6.75, 7, 6.75)), line(seg(17, 6.75, 20.5, 6.75)),
        shell(rect(7, 4.5, 10, 4.5, rr(S, 2))),
        shell(poly([(6, 12), (18, 12), (17, 21.5), (7, 21.5)], closed=True, r=S.r)),
    ]


@icon("decoy-owl", CAT, "An upright plastic owl with big eyes standing on a roof ridge line",
      tags=["fake owl", "owl decoy", "bird deterrent", "scarecrow", "pest bird control", "roof ridge", "garden owl"])
def _(S):
    return [
        shell(poly([(4.5, 18.5), (4.5, 5), (8, 7.5), (16, 7.5), (19.5, 5), (19.5, 18.5)], closed=True, r=S.r * 1.5)),
        detail(circle(8.8, 11.5, 2)), detail(circle(15.2, 11.5, 2)),
        dot(8.8, 11.5, 0.9), dot(15.2, 11.5, 0.9),
        Part("dot", poly([(12, 12.5), (10.8, 15), (13.2, 15)], closed=True)),
        line(seg(2, 21.5, 22, 21.5)),
    ]

@icon("air-brick", CAT, "A single brick face with a grid of rectangular ventilation holes",
      tags=["air brick", "vent brick", "airbrick", "ventilation", "underfloor vent", "wall vent", "masonry vent"])
def _(S):
    holes = [Part("dot", rect(x, y, 3, 3, 0)) for x in (5, 10.5, 16) for y in (8, 13)]
    return [shell(rect(2, 5, 20, 14, rr(S, 3))), *holes]


@icon("raccoon-raiding-trash", CAT, "A raccoon head peeking out of a trash can with litter scattered around it",
      tags=["raccoon", "trash raider", "garbage can", "wildlife pest", "bin raiding", "animal proof bin", "nuisance animal"])
def _(S):
    return [
        line(poly([(7.5, 12), (7, 5.5), (9.5, 7.5), (14.5, 7.5), (17, 5.5), (16.5, 12)], r=S.r)),
        dot(10, 10, 1.1), dot(14, 10, 1.1),
        shell(poly([(5, 12.5), (19, 12.5), (17.5, 21.5), (6.5, 21.5)], closed=True, r=S.r)),
        dot(2.5, 19.5, 1.2), dot(21.5, 19, 1.2),
    ]


@icon("bed-leg-interceptor", CAT, "A bed leg standing in a round double-walled cup with a small bug trapped in the outer ring",
      tags=["bed bug interceptor", "climb-up trap", "bed bug trap", "bed leg cup", "bed bug monitor", "pest trap", "bedroom pests"])
def _(S):
    return [
        shell(poly([(9.5, 2.5), (14.5, 2.5), (14.5, 14.5), (9.5, 14.5)], closed=True, r=S.r)),
        shell(ellipse(12, 17.5, 9.5, 4.5)),
        detail(ellipse(12, 17.5, 5.2, 2)),
        dot(4.6, 17.5, 0.9),
    ]

@icon("magnetic-screen-door", CAT, "A doorway with a mesh curtain split down the middle and magnets along the seam",
      tags=["screen door", "magnetic curtain", "insect screen", "fly screen", "bug curtain", "door mesh", "pest barrier"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 3))),
        detail(seg(12, 2.5, 12, 21.5)),
        detail(seg(8, 6.5, 8, 17.5)), detail(seg(16, 6.5, 16, 17.5)),
        Part("dot", rect(10.25, 7.5, 3.5, 2.5, 0)), Part("dot", rect(10.25, 14, 3.5, 2.5, 0)),
    ]


@icon("tripped-breaker", CAT, "A circuit breaker module with its toggle stuck in the middle position and a lightning bolt beside it",
      tags=["tripped breaker", "circuit breaker", "breaker trip", "power cut", "fuse box", "electrical fault", "reset breaker"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 9.5, 19, rr(S, 3))),
        detail(seg(7.25, 6, 7.25, 18)),
        Part("dot", rect(5.25, 10, 4, 4, 0)),
        solid(poly([(19.5, 3), (15.5, 12.5), (19, 12.5), (17, 21), (22, 10), (18.5, 10)], closed=True)),
    ]


@icon("blown-fuse", CAT, "A glass cartridge fuse with a broken filament inside and a scorch mark in the middle",
      tags=["blown fuse", "burnt fuse", "cartridge fuse", "broken filament", "electrical repair", "fuse replacement", "power failure"])
def _(S):
    return [
        shell(rect(2, 6.5, 4, 11, rr(S, 1.5))),
        shell(rect(18, 6.5, 4, 11, rr(S, 1.5))),
        line(seg(6, 8, 18, 8)), line(seg(6, 16, 18, 16)),
        line(seg(6, 12, 9.5, 12)), line(seg(14.5, 12, 18, 12)),
        dot(12, 12, 1.5),
    ]


@icon("flickering-light", CAT, "A light bulb with short broken rays and a jagged zigzag line beside it",
      tags=["flickering light", "flicker", "faulty bulb", "unstable power", "loose wiring", "dimming", "electrical fault"])
def _(S):
    return [
        shell("M8 15.5V14.3A5.5 5.5 0 1 1 14 14.3V15.5Z"),
        line(seg(8.5, 18.5, 13.5, 18.5)),
        line(seg(9.5, 21, 12.5, 21)),
        line(arc(11, 9.5, 8, 190, 225)),
        line(arc(11, 9.5, 8, -75, -40)),
        line(poly([(21, 3), (19.5, 8), (22, 11), (20.5, 17)], r=S.r * 0.5)),
    ]


@icon("sparking-outlet", CAT, "A wall outlet plate with a flash of sparks bursting near one socket",
      tags=["sparking outlet", "electrical spark", "faulty socket", "arcing", "short circuit", "fire hazard", "outlet repair"])
def _(S):
    star = []
    for i in range(16):
        r = 4.4 if i % 2 == 0 else 1.9
        star.append(polar(18, 6, r, -90 + i * 22.5))
    return [
        shell(rect(2, 9, 12, 12, rr(S, 3))),
        Part("dot", rect(5, 12, 2, 3.5, 0)), Part("dot", rect(9, 12, 2, 3.5, 0)),
        dot(8, 18, 1.1),
        solid(poly(star, closed=True)),
    ]


@icon("circuit-tracer", CAT, "A plug-in transmitter unit and a handheld receiver wand with a pointed tip and signal arcs",
      tags=["circuit tracer", "wire tracer", "breaker finder", "cable locator", "electrician tool", "tone generator", "receiver"])
def _(S):
    wand = rot([(10.5, 2), (13.5, 2), (13.5, 11.5), (12, 15), (10.5, 11.5)], -45, 12, 9)
    return [
        shell(rect(2.5, 14, 8, 7.5, rr(S, 3))),
        dot(6.5, 17.75, 1.2),
        shell(poly(wand, closed=True, r=S.r * 0.4)),
        line(arc(16.3, 13.7, 3.5, 0, 75)),
        line(arc(16.3, 13.7, 6.5, 0, 75)),
    ]


@icon("screw-in-fuse", CAT, "A round plug fuse with a threaded screw base and a small window on top",
      tags=["plug fuse", "edison fuse", "screw fuse", "old fuse box", "fuse replacement", "household fuse", "electrical"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 9.5, rr(S, 4))),
        Part("dot", rect(8.5, 5.5, 7, 3.5, 0)),
        shell(poly([(7, 12), (17, 12), (17, 18), (15.5, 19.5), (8.5, 19.5), (7, 18)], closed=True, r=S.r * 0.5)),
        detail(seg(7, 15, 17, 15)),
        solid(rect(10.5, 20, 3, 2, 0)),
    ]


@icon("sheathed-cable", CAT, "A flat cable end with its outer sheath stripped back showing two insulated wires and one bare wire",
      tags=["sheathed cable", "twin and earth", "stripped cable", "cable stripping", "bare earth wire", "wiring", "electrical cable"])
def _(S):
    return [
        shell(rect(2, 4, 8, 16, rr(S, 3))),
        shell(rect(11, 4.5, 9, 3.5, rr(S, 1.5))),
        line(seg(10, 12, 22, 12)),
        shell(rect(11, 16, 9, 3.5, rr(S, 1.5))),
    ]


@icon("knob-and-tube-wiring", CAT, "A wooden joist with porcelain knobs holding a wire and a porcelain tube passing through the joist",
      tags=["knob and tube", "old wiring", "porcelain knob", "vintage wiring", "ceramic insulator", "wiring inspection", "joist"])
def _(S):
    return [
        line(seg(2, 5.5, 22, 5.5)),
        shell(rect(5, 8, 4, 6, rr(S, 1.5))),
        shell(rect(15, 8, 4, 6, rr(S, 1.5))),
        shell(rect(2.5, 15, 19, 6.5, rr(S, 2))),
        Part("dot", rect(10.5, 16.5, 3, 3.5, 0)),
    ]


@icon("wall-chase", CAT, "A wall section with a straight vertical groove cut into it holding a cable that runs down to a box",
      tags=["wall chase", "cable channel", "chasing wall", "groove", "buried cable", "wiring channel", "plastering"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 3))),
        detail(seg(8.5, 2.5, 8.5, 12)), detail(seg(15.5, 2.5, 15.5, 12)),
        line(seg(12, 2.5, 12, 12.5)),
        shell(rect(7, 12.5, 10, 5.5, rr(S, 1.5))),
    ]


@icon("missing-shingles", CAT, "A roof section of overlapping shingle rows with a gap where shingles are missing",
      tags=["missing shingles", "roof damage", "storm damage", "roof repair", "bare roof deck", "shingle loss", "roofing"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 18, rr(S, 3))),
        detail(seg(2.5, 9, 21.5, 9)), detail(seg(2.5, 15, 21.5, 15)),
        detail(seg(9, 3, 9, 9)), detail(seg(16, 3, 16, 9)),
        detail(seg(12, 15, 12, 21)),
        Part("dot", rect(8, 10.5, 8, 3.5, 0)),
    ]


@icon("roof-inspection", CAT, "A person kneeling on a roof slope holding a clipboard",
      tags=["roof inspection", "roof survey", "roofer", "roof check", "clipboard", "property inspection", "roof condition"])
def _(S):
    return [
        line(seg(2, 21, 22, 14)),
        dot(7, 5.5, 2.2),
        line(poly([(7, 8.5), (8.5, 14), (13, 16)], r=S.r)),
        line(seg(8, 11, 13, 10)),
        shell(rect(13, 6.5, 6, 7.5, rr(S, 1.5))),
    ]


@icon("roofing-hatchet", CAT, "A hatchet with a flat hammer face, a blade on the back, a gauge pin and a short handle",
      tags=["roofing hatchet", "shingler hatchet", "roofer tool", "hatchet", "shingle tool", "hammer axe", "roofing tools"])
def _(S):
    return [
        shell(poly([(2.5, 4.5), (8, 4.5), (21.5, 2.5), (21.5, 10.5), (8, 9), (2.5, 9)], closed=True, r=S.r * 0.4), stroke_miterlimit="2"),
        line(seg(16.5, 10.5, 16.5, 13.5)),
        shell(rect(8.5, 9, 4, 12.5, rr(S, 1.5))),
    ]


@icon("shingle-removal-shovel", CAT, "A long-handled shovel with a flat blade whose front edge has saw-tooth notches",
      tags=["shingle shovel", "roof tear-off", "roofing shovel", "shingle ripper", "re-roofing", "roof stripping", "tear off tool"])
def _(S):
    return [
        line(seg(9, 2.5, 15, 2.5)),
        line(seg(12, 2.5, 12, 12.5)),
        shell(poly([(6.5, 12.5), (17.5, 12.5), (17.5, 18.5), (15.7, 21), (13.8, 18.5), (12, 21), (10.2, 18.5), (8.3, 21), (6.5, 18.5)],
                   closed=True, r=0), stroke_miterlimit="2"),
    ]


def _step(x0, y0, w=7.0, h=6.0, t=3.0):
    return [(x0, y0), (x0 + w, y0), (x0 + w, y0 - h), (x0 + w - t, y0 - h), (x0 + w - t, y0 - t), (x0, y0 - t)]


@icon("roof-flashing", CAT, "Stepped L-shaped metal pieces tucked under shingles where a roof slope meets a wall",
      tags=["step flashing", "roof flashing", "wall flashing", "roof leak seal", "sheet metal", "roofing detail", "waterproofing"])
def _(S):
    return [shell(poly(_step(x, y), closed=True, r=S.r * 0.4)) for x, y in ((2.5, 21), (8.5, 16), (14.5, 11))]


@icon("gutter-cleaning", CAT, "A gloved hand scooping a clump of leaves out of a gutter channel",
      tags=["gutter cleaning", "clean gutters", "leaves", "gutter maintenance", "gloved hand", "debris removal", "rain gutter"])
def _(S):
    return [
        shell(rect(7.5, 2.5, 7.5, 8, rr(S, 3))),
        line(poly([(15, 6), (18.5, 6), (18.5, 9.5)], r=S.r * 0.5)),
        solid("M6.5 16Q8.5 11.5 14.5 12.5Q13.5 17 6.5 16Z"),
        solid("M11 17Q14 13 19 14.5Q17.5 18 11 17Z"),
        line("M2.5 12V15A3 3 0 0 0 5.5 18H18.5A3 3 0 0 0 21.5 15V12"),
    ]
