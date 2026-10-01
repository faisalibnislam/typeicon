"""TypeIcon Core: household cleaning, laundry and pest control (batch 002).

Household cleaning tools, machines, supplies, laundry gear and pest control, drawn from the objects themselves.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar

CAT = "household"


def rot(pts, deg=45, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rp(pts, closed=True, r=0.0, deg=45):
    return poly(rot(pts, deg), closed=closed, r=r)


def rseg(x1, y1, x2, y2, deg=45):
    (a, b), (c, d) = rot([(x1, y1), (x2, y2)], deg)
    return seg(a, b, c, d)


def rrect(x, y, w, h, rx=0.0, deg=45):
    """Rotated rounded rectangle."""
    rx = max(0.0, min(rx, w / 2, h / 2))
    def pt(p):
        q = rot([p], deg)[0]
        return f"{fmt(q[0])} {fmt(q[1])}"
    if rx == 0:
        return rp([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], deg=deg)
    return ("M" + pt((x + rx, y)) + "L" + pt((x + w - rx, y)) + f"A{fmt(rx)} {fmt(rx)} 0 0 1 " + pt((x + w, y + rx))
            + "L" + pt((x + w, y + h - rx)) + f"A{fmt(rx)} {fmt(rx)} 0 0 1 " + pt((x + w - rx, y + h))
            + "L" + pt((x + rx, y + h)) + f"A{fmt(rx)} {fmt(rx)} 0 0 1 " + pt((x, y + h - rx))
            + "L" + pt((x, y + rx)) + f"A{fmt(rx)} {fmt(rx)} 0 0 1 " + pt((x + rx, y)) + "Z")


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    return Part("dot", rect(x, y, w, h, rx))


def union_d(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


# ============================================================================ cleaning tools

@icon("window-cleaning", CAT, "Window pane with a squeegee blade and two sparkles",
      tags=["squeegee", "window cleaner", "glass", "streak free", "cleaning", "shine", "housework"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        detail(seg(6.5, 17, 14.5, 17)),
        detail(seg(10.5, 17, 10.5, 11)),
        detail(seg(16.5, 5.5, 16.5, 9.5)),
        detail(seg(14.5, 7.5, 18.5, 7.5)),
    ]


@icon("extension-pole", CAT, "Telescopic pole with two sections and a clip head on top",
      tags=["telescopic pole", "reach pole", "long handle", "cleaning", "duster pole", "ceiling", "housework"])
def _(S):
    return [
        shell(rrect(9.5, 12, 5, 9.5, rr(S, 2))),
        detail(rseg(9.5, 15.5, 14.5, 15.5)),
        line(rseg(12, 12, 12, 6)),
        shell(rrect(8.5, 2, 7, 4, rr(S, 1.5))),
    ]


@icon("scraper-blade", CAT, "Flat razor scraper with a wide blade and a short handle",
      tags=["razor scraper", "paint scraper", "putty knife", "glass scraper", "remove", "cleaning", "tool"])
def _(S):
    return [
        shell(poly([(3.5, 3), (20.5, 3), (18, 11), (6, 11)], closed=True, r=S.r * 0.6)),
        detail(seg(5.5, 6.5, 18.5, 6.5)),
        shell(rect(9.75, 11, 4.5, 10.5, rr(S, 2.25))),
    ]


@icon("mop-bucket", CAT, "Wheeled mop bucket with a wringer press and a mop handle",
      tags=["bucket", "wringer", "janitor", "floor cleaning", "mopping", "cleaner", "housework"])
def _(S):
    return [
        line(seg(12, 8, 18, 2)),
        shell(rect(3.5, 8, 17, 3.5, rr(S, 1.75))),
        shell(poly([(5, 11.5), (19, 11.5), (17.5, 21.5), (6.5, 21.5)], closed=True, r=S.r)),
    ]


@icon("spin-mop", CAT, "Round spin mop head with long microfiber strands",
      tags=["microfiber mop", "string mop", "round mop", "floor cleaning", "mopping", "spinning", "housework"])
def _(S):
    return [
        line(seg(12, 2, 12, 6.5)),
        shell(rect(6, 6.5, 12, 4, rr(S, 2))),
        shell("M7.5 10.5C6.5 14 5 18 3.5 21.5L8 19.5L12 21.5L16 19.5L20.5 21.5C19 18 17.5 14 16.5 10.5Z" if S.name == "line"
              else "M7.5 10.5C6.5 14 5 18 3.5 21.5Q8 19 12 21.5Q16 19 20.5 21.5C19 18 17.5 14 16.5 10.5Z"),
        detail(seg(10.5, 12.5, 9.5, 18)),
        detail(seg(13.5, 12.5, 14.5, 18)),
    ]


@icon("flat-mop", CAT, "Flat rectangular mop pad on a swivel joint with a long handle",
      tags=["microfiber mop", "floor mop", "mop pad", "floor cleaning", "mopping", "swivel", "housework"])
def _(S):
    return [
        line(seg(17, 2.5, 12.5, 12)),
        shell(rect(3, 15, 18, 5.5, rr(S, 2.5))),
        dot(12, 13, 1.25),
    ]


@icon("steam-mop", CAT, "Upright steam mop with a triangular pad and wisps of steam",
      tags=["steam cleaner", "floor steamer", "floor cleaning", "hygiene", "sanitize floor", "mopping", "housework"])
def _(S):
    return [
        line(seg(9, 2.5, 15, 2.5)),
        line(seg(12, 2.5, 12, 6.5)),
        shell(rect(9, 6.5, 6, 9.5, rr(S, 3))),
        shell(poly([(3.5, 21.5), (20.5, 21.5), (16.5, 16), (7.5, 16)], closed=True, r=S.r * 0.6)),
        line("M19.5 6.5C18 8 21 9.5 19.5 11C19 11.5 18.8 12 18.9 12.5"),
    ]


@icon("push-broom", CAT, "Wide push broom with a long bristle head on a straight pole",
      tags=["shop broom", "garage broom", "sweeping", "sweep floor", "yard", "cleaning", "housework"])
def _(S):
    return [
        line(seg(12, 13.5, 16.5, 2.5)),
        shell(rect(3, 13.5, 18, 3, rr(S, 1.5))),
        shell(rect(3, 16.5, 18, 5, rr(S, 1.5) if S.name == "rounded" else 0)),
        detail(seg(8, 16.5, 8, 21.5)),
        detail(seg(16, 16.5, 16, 21.5)),
    ]


@icon("whisk-broom", CAT, "Short hand broom with fanned bristles bound near the top",
      tags=["hand broom", "counter brush", "crumb brush", "sweeping", "straw broom", "cleaning", "housework"])
def _(S):
    return [
        shell(rect(10, 2, 4, 6, rr(S, 2))),
        shell(rect(9, 8, 6, 3, rr(S, 1.5))),
        shell(poly([(9.5, 11), (14.5, 11), (20, 21.5), (4, 21.5)], closed=True, r=S.r * 0.6)),
        detail(seg(11, 12.5, 9, 21)),
        detail(seg(13, 12.5, 15, 21)),
    ]


@icon("cobweb-duster", CAT, "Round bristle duster on a long pole reaching a cobweb in the corner",
      tags=["spider web", "cobweb brush", "ceiling duster", "dusting", "corner", "cleaning", "housework"])
def _(S):
    star = []
    for i in range(12):
        star.append(polar(11, 13, 5.25 if i % 2 == 0 else 3.75, -90 + i * 30))
    return [
        line(arc(22, 2, 4.5, 90, 180)),
        line(arc(22, 2, 9, 90, 180)),
        line(seg(22, 2, 22, 11.5)),
        line(seg(22, 2, 15.6, 8.4)),
        line(seg(22, 2, 12.5, 2)),
        shell(poly(star, closed=True, r=S.r * 0.4), stroke_miterlimit="2"),
        line(seg(7.5, 16.5, 3, 21.5)),
    ]


@icon("lint-roller", CAT, "Lint roller with a sticky cylinder and a handle",
      tags=["sticky roller", "pet hair", "fluff remover", "clothes cleaning", "lint remover", "tape roller", "housework"])
def _(S):
    return [
        shell(rect(3, 2.5, 15, 8, rr(S, 4))),
        detail(seg(9, 2.5, 7, 10.5)),
        line(poly([(18, 6.5), (20.5, 6.5), (20.5, 14), (12, 14)], r=S.r * 0.6)),
        shell(rect(9.75, 14, 4.5, 7.5, rr(S, 2.25))),
    ]


@icon("clothes-brush", CAT, "Oval clothes brush with a dense pad of bristles",
      tags=["garment brush", "suit brush", "lint brush", "coat brush", "dust off", "clothing care", "housework"])
def _(S):
    return [
        shell(rect(3, 3.5, 18, 8, rr(S, 4))),
        shell(rect(5, 11.5, 14, 7, rr(S, 1.5) if S.name == "rounded" else 0)),
        detail(seg(9, 11.5, 9, 18.5)),
        detail(seg(12, 11.5, 12, 18.5)),
        detail(seg(15, 11.5, 15, 18.5)),
    ]

@icon("rubber-gloves", CAT, "Long rubber cleaning glove with a rolled cuff",
      tags=["cleaning gloves", "dish gloves", "washing up gloves", "latex gloves", "hand protection", "chores", "housework"])
def _(S):
    hand = [(8, 17), (8, 14), (4.5, 11.5), (6, 9.5), (8, 11.5), (8, 6), (11, 6), (11, 3.5), (14, 3.5), (14, 5), (17, 5), (17, 17)]
    return [
        shell(poly(hand, closed=True, r=S.r * 0.7)),
        detail(seg(11, 8.5, 11, 13)),
        detail(seg(14, 8.5, 14, 13)),
        shell(rect(6.5, 17, 11, 4.5, rr(S, 2))),
    ]


@icon("carpet-beater", CAT, "Rattan carpet beater with a three-lobed loop head on a handle",
      tags=["rug beater", "carpet whacker", "dust", "beating", "spring cleaning", "traditional", "housework"])
def _(S):
    centres = rot([(12, 5.3), (15.4, 11), (8.6, 11)], 45, 12, 12)
    lobes = union_d(*[circle(x, y, 3.4) for x, y in centres])
    hub = rot([(12, 8.9)], 45, 12, 12)[0]
    return [
        shell(lobes),
        dot(hub[0], hub[1], 1.25),
        line(rseg(12, 13.5, 12, 21.5)),
    ]


@icon("carpet-cleaner", CAT, "Upright carpet cleaning machine with a clear water tank and a wide nozzle",
      tags=["carpet shampooer", "rug cleaner", "deep clean", "extractor", "upholstery", "floor care", "housework"])
def _(S):
    return [
        line(poly([(12, 8), (12, 3), (17, 3)], r=S.r * 0.6)),
        shell(rect(7, 8, 10, 9, rr(S, 2.5))),
        detail("M7 12.5Q9.5 10.5 12 12.5T17 12.5"),
        shell(rect(3, 17, 18, 4.5, rr(S, 2.25))),
    ]


@icon("steam-cleaner", CAT, "Handheld steam cleaner with a nozzle releasing puffs of steam",
      tags=["steamer", "sanitizer", "grout cleaner", "hygiene", "deep clean", "hand steamer", "housework"])
def _(S):
    return [
        shell(rect(2.5, 8.5, 10, 6.5, rr(S, 3))),
        shell(rect(4.5, 15, 5, 6.5, rr(S, 2))),
        line(seg(12.5, 12, 15, 12)),
        shell(union_d(circle(17.5, 12, 2.5), circle(20, 9, 2.5), circle(20, 13.5, 2))),
    ]


@icon("pressure-washer", CAT, "Pressure washer gun with a trigger and a long lance spraying a jet",
      tags=["power washer", "jet wash", "spray gun", "patio cleaning", "driveway", "car wash", "outdoor cleaning"])
def _(S):
    return [
        shell(rect(2.5, 7, 8, 6, rr(S, 2.5))),
        shell(rect(4, 13, 4.5, 7.5, rr(S, 2))),
        line(seg(10.5, 10, 16, 10)),
        line(seg(18, 10, 21.5, 6)),
        line(seg(18.5, 10, 21.5, 10)),
        line(seg(18, 10, 21.5, 14)),
    ]


@icon("floor-scrubber", CAT, "Walk-behind floor scrubbing machine with a round brush deck and a handlebar",
      tags=["floor polisher", "auto scrubber", "commercial cleaning", "janitor", "floor machine", "buffer", "cleaning equipment"])
def _(S):
    return [
        line(poly([(13, 12), (17, 4), (21.5, 4)], r=S.r * 0.6)),
        shell(rect(5, 9.5, 9, 6.5, rr(S, 3))),
        shell(rect(3, 16, 18, 4.5, rr(S, 2.25))),
    ]


@icon("robot-vacuum", CAT, "Top view of a round robot vacuum with a bumper arc and a sensor",
      tags=["robotic vacuum", "robot cleaner", "auto vacuum", "smart home", "floor cleaning", "autonomous", "housework"])
def _(S):
    return [
        shell(circle(12, 12, 9.25)),
        detail(arc(12, 12, 5.5, 200, 340)),
        dot(12, 13.5, 1.5) if S.name == "rounded" else sq(10.5, 12, 3, 3),
    ]


@icon("handheld-vacuum", CAT, "Small cordless handheld vacuum with a pistol grip and a flared nozzle",
      tags=["cordless vacuum", "hand vac", "car vacuum", "crumbs", "portable vacuum", "mini vacuum", "housework"])
def _(S):
    return [
        shell(poly([(7.5, 7), (3, 4.5), (3, 12.5), (7.5, 10)], closed=True, r=S.r * 0.6)),
        shell(rect(7.5, 5, 13.5, 6.5, rr(S, 3))),
        shell(rect(13.5, 11.5, 5, 9.5, rr(S, 2.5))),
        detail(seg(12, 8.25, 17.5, 8.25)),
    ]


@icon("stick-vacuum", CAT, "Cordless stick vacuum with a motor body at the top and a floor head",
      tags=["cordless vacuum", "lightweight vacuum", "slim vacuum", "floor cleaning", "stick vac", "battery vacuum", "housework"])
def _(S):
    return [
        line(poly([(9, 4.5), (6, 4.5), (6, 10)], r=S.r * 0.6)),
        shell(rect(9, 2.5, 7, 9, rr(S, 3))),
        detail(seg(11, 6, 14, 6)),
        line(seg(12.5, 11.5, 12.5, 17.5)),
        shell(poly([(4, 21.5), (5.5, 17.5), (21, 17.5), (21, 21.5)], closed=True, r=S.r * 0.6)),
    ]


@icon("upright-vacuum", CAT, "Upright vacuum cleaner with a tall dust bag body and a wide floor head",
      tags=["vacuum cleaner", "bagged vacuum", "carpet cleaning", "floor care", "sweeper", "housework"])
def _(S):
    return [
        line(poly([(9, 2.5), (14, 2.5), (14, 7)], r=S.r * 0.6)),
        shell("M8 17V12A4 4 0 0 1 16 12V17Z" if S.name == "rounded" else "M8 17V11L11 7H13L16 11V17Z"),
        detail(seg(8, 13, 16, 13)),
        shell(rect(3, 17, 18, 4.5, rr(S, 2.25))),
    ]


@icon("wet-dry-vacuum", CAT, "Drum-shaped shop vacuum on casters with a flexible hose over the lid",
      tags=["shop vac", "workshop vacuum", "garage vacuum", "wet vac", "canister vacuum", "drum vacuum", "cleaning equipment"])
def _(S):
    return [
        line("M8 6.5C8 2 16 2 16 6.5"),
        shell(rect(3.5, 6.5, 17, 4, S.R / 2)),
        shell(poly([(5, 10.5), (19, 10.5), (18, 18.5), (6, 18.5)], closed=True, r=S.r)),
        dot(7.5, 21, 1.25),
        dot(16.5, 21, 1.25),
    ]


@icon("cleaning-caddy", CAT, "Open plastic tote with a centre handle holding a spray bottle and a brush",
      tags=["cleaning bucket", "supplies tote", "cleaning kit", "cleaner's basket", "housekeeping", "storage", "housework"])
def _(S):
    return [
        line(poly([(9, 13), (9, 8.5), (15, 8.5), (15, 13)], r=S.r * 0.6)),
        line(poly([(4.5, 13), (4.5, 5.5), (7, 5.5)], r=S.r * 0.4)),
        line(seg(18.5, 13, 18.5, 5)),
        shell(poly([(3, 13), (21, 13), (19, 21.5), (5, 21.5)], closed=True, r=S.r)),
    ]


@icon("janitor-cart", CAT, "Cleaning trolley with a hanging bag, a shelf and a mop bucket at the side",
      tags=["housekeeping cart", "cleaning trolley", "hotel cleaning", "maid cart", "custodian", "service cart", "commercial cleaning"])
def _(S):
    return [
        shell(rect(3, 2.5, 9, 7, rr(S, 2.5))),
        shell(rect(3, 12, 12, 6, rr(S, 1.5))),
        shell(poly([(16.5, 8), (21.5, 8), (20.5, 18), (17.5, 18)], closed=True, r=S.r * 0.6)),
        dot(6, 21, 1.25),
        dot(12, 21, 1.25),
        dot(19, 21, 1.25),
    ]


@icon("wet-floor-sign", CAT, "A-frame caution sign with a slipping person figure",
      tags=["caution sign", "slippery floor", "hazard sign", "warning sign", "slip hazard", "safety", "janitor"])
def _(S):
    return [
        shell(poly([(9, 2.5), (15, 2.5), (20, 21.5), (4, 21.5)], closed=True, r=S.r)),
        dot(13.5, 8, 1.25),
        detail(poly([(15, 11), (12, 12.5), (10, 16)])),
        detail(seg(12, 12.5, 15, 16)),
    ]


@icon("chore-chart", CAT, "Clipboard with a checklist of ticked rows and a small spray bottle",
      tags=["chore list", "cleaning schedule", "housework checklist", "household tasks", "rota", "to-do", "family chores"])
def _(S):
    return [
        shell(rect(3, 4.5, 13, 17, rr(S, 2))),
        shell(rect(6.5, 2.5, 6, 4, rr(S, 1.5))),
        detail(poly([(6, 10.5), (7.5, 12), (10, 9.5)])),
        detail(seg(11.5, 10.5, 13.5, 10.5)),
        detail(poly([(6, 16), (7.5, 17.5), (10, 15)])),
        detail(seg(11.5, 16, 13.5, 16)),
        shell(rect(18, 13, 4, 8, rr(S, 1.5))),
        line(poly([(19, 13), (19, 10.5), (22, 10.5)])),
    ]


# ============================================================================ waste and supplies

DROP = "M{x} {y}L{a} {b}A{r} {r} 0 1 0 {c} {b}Z"


def drop_d(cx, cy, r=1.6):
    """Teardrop centred near (cx, cy): pointed top, round belly (for label marks)."""
    return (f"M{fmt(cx)} {fmt(cy - r * 1.9)}L{fmt(cx - r * 0.95)} {fmt(cy - r * 0.35)}"
            f"A{fmt(r)} {fmt(r)} 0 1 0 {fmt(cx + r * 0.95)} {fmt(cy - r * 0.35)}Z")


@icon("trash-bag", CAT, "Full garbage bag with a twisted neck tied at the top",
      tags=["garbage bag", "bin bag", "rubbish bag", "refuse sack", "waste", "litter", "take out trash"])
def _(S):
    return [
        line(seg(10.5, 7, 7, 3.5)),
        line(seg(13.5, 7, 17, 3.5)),
        shell(poly([(9.5, 10), (10.5, 7), (13.5, 7), (14.5, 10)], closed=True, r=S.r * 0.4)),
        shell("M9.5 10C4.5 11.5 3.5 17 6 20C8 22 16 22 18 20C20.5 17 19.5 11.5 14.5 10Z"),
    ]


@icon("bin-bag-roll", CAT, "Roll of garbage bags with a bag sheet unrolling along the bottom",
      tags=["bin liners", "garbage bags", "refuse sacks", "trash bags", "perforated roll", "waste", "supplies"])
def _(S):
    return [
        shell(circle(10, 11.5, 8)),
        detail(circle(10, 11.5, 2.75)),
        line(poly([(10, 19.5), (21.5, 19.5), (21.5, 13)], r=S.r)),
    ]


@icon("wheelie-bin", CAT, "Tall wheeled waste bin with a lid and a large wheel at the back",
      tags=["wheeled bin", "garbage bin", "trash can", "refuse bin", "dustbin", "curbside", "waste"])
def _(S):
    return [
        shell(rect(3.5, 3, 15, 4.5, rr(S, 2.25))),
        shell(poly([(5, 7.5), (17, 7.5), (16, 20), (6, 20)], closed=True, r=S.r * 0.6)),
        detail(seg(8.5, 11.5, 13.5, 11.5)),
        dot(19, 19, 2.25),
    ]


@icon("bleach-bottle", CAT, "Chunky jug with a handle and a screw cap, marked with a drop",
      tags=["cleaning jug", "laundry bleach", "disinfectant", "chlorine", "whitener", "cleaning supply", "household chemical"])
def _(S):
    return [
        shell(rect(7.5, 3.5, 5, 3.5, rr(S, 1.5))),
        shell(rect(4, 7, 12, 14.5, rr(S, 3.5))),
        line(poly([(16, 10), (19.5, 10), (19.5, 17), (16, 17)], r=S.r * 0.8)),
        Part("dot", drop_d(10, 15, 2.1)),
    ]


@icon("dish-soap", CAT, "Tall squeeze bottle with a flip-top cap and a plate with a bubble",
      tags=["washing up liquid", "dish detergent", "dish washing", "kitchen soap", "dishwashing liquid", "cleaning supply", "sink"])
def _(S):
    return [
        shell(poly([(7.5, 21.5), (7.5, 12.5), (10.5, 9.5), (10.5, 5.5), (9.5, 5.5), (9.5, 3), (14.5, 3), (14.5, 5.5), (13.5, 5.5), (13.5, 9.5), (16.5, 12.5), (16.5, 21.5)],
                   closed=True, r=S.r * 0.6)),
        detail(circle(12, 17, 2.5)),
    ]


@icon("toilet-cleaner", CAT, "Cleaner bottle with a bent angled neck pointing forward",
      tags=["toilet bowl cleaner", "loo cleaner", "lavatory", "bathroom cleaning", "bent neck bottle", "disinfectant", "household chemical"])
def _(S):
    return [
        line(poly([(9, 11), (9, 5), (3.5, 5), (3.5, 8)], r=S.r * 0.6)),
        shell(rect(4.5, 11, 13, 10.5, rr(S, 3.5))),
        detail(seg(8, 15, 14, 15)),
        detail(seg(8, 18, 12, 18)),
    ]


@icon("drain-cleaner", CAT, "Heavy bottle with a wide child-safe cap and a curved pipe on the label",
      tags=["drain unblocker", "pipe cleaner", "clog remover", "plumbing", "sink blockage", "caustic", "household chemical"])
def _(S):
    return [
        shell(rect(7.5, 3, 9, 5, rr(S, 2))),
        shell(rect(5.5, 8, 13, 13.5, rr(S, 3.5))),
        detail("M9.5 12.5V16.5A2.5 2.5 0 0 0 14.5 16.5V12.5"),
    ]


@icon("disinfectant-wipes", CAT, "Round wipes canister with one wipe pulled up through the lid",
      tags=["cleaning wipes", "sanitizing wipes", "antibacterial wipes", "surface wipes", "germ kill", "hygiene", "canister"])
def _(S):
    return [
        line("M10 8.5C10 4.5 11.5 5 12 3C12.5 5 14 4.5 14 8.5"),
        shell(rect(4.5, 8.5, 15, 3, rr(S, 1.5))),
        shell(rect(5.5, 11.5, 13, 10, rr(S, 2.5))),
        Part("dot", drop_d(12, 17.5, 1.9)),
    ]


@icon("wet-wipes", CAT, "Soft wet wipes pack with a resealable flap and a wipe peeking out",
      tags=["baby wipes", "moist towelettes", "hand wipes", "refill pack", "diaper changing", "hygiene", "cleaning"])
def _(S):
    return [
        line("M8.5 8.5C8.5 5 10.5 5.5 12 3C13.5 5.5 15.5 5 15.5 8.5"),
        shell(rect(3, 8.5, 18, 13, rr(S, 3.5))),
        detail(rect(7.5, 11.5, 9, 4.5, 0) if S.name == "line" else rect(7.5, 11.5, 9, 4.5, 2.25)),
    ]


@icon("paper-towel-roll", CAT, "Paper towel roll standing on a vertical holder",
      tags=["kitchen roll", "kitchen towel", "paper towel holder", "paper towels", "spill cleanup", "wipe", "kitchen"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 6)),
        shell(ellipse(12, 7, 5, 2)),
        line("M7 7V16.5A5 2 0 0 0 17 16.5V7"),
        line(seg(6.5, 21, 17.5, 21)),
    ]


@icon("tissue-box", CAT, "Square tissue box with a tissue fluffed up out of the top",
      tags=["facial tissues", "tissue dispenser", "handkerchief", "cold and flu", "bathroom", "paper tissue"])
def _(S):
    return [
        line("M8.5 10C7 6 9.5 3 12 6C14.5 3 17 6 15.5 10"),
        shell(rect(3, 10, 18, 11.5, rr(S, 3))),
        detail(seg(8, 15.75, 16, 15.75)),
    ]


@icon("pocket-tissues", CAT, "Small flat packet of tissues with a tissue poking out of the top",
      tags=["travel tissues", "handkerchiefs", "tissue pack", "pocket pack", "paper hankies", "cold", "on the go"])
def _(S):
    return [
        line("M8.5 9.5C8 4.5 11.5 4 12 7C12.5 4 16 4.5 15.5 9.5"),
        shell(poly([(6, 9.5), (18, 9.5), (18, 21.5), (6, 21.5)], closed=True, r=S.r)),
        detail(seg(6, 14, 18, 14)),
    ]


@icon("furniture-polish", CAT, "Round tin of wax polish with its lid off and a cloth beside it",
      tags=["wood polish", "wax tin", "furniture wax", "dusting", "shine", "wood care", "cleaning supply"])
def _(S):
    return [
        shell(ellipse(8.5, 11, 5.5, 2.25)),
        line("M3 11V18.5A5.5 2.25 0 0 0 14 18.5V11"),
        shell(poly([(16, 20.5), (16.5, 12.5), (19, 14), (21, 12.5), (21.5, 20.5)], closed=True, r=S.r)),
    ]


@icon("air-freshener-spray", CAT, "Aerosol can with a round cap spraying a mist, with a small flower beside it",
      tags=["room spray", "deodorizer", "aerosol", "odor eliminator", "fragrance", "scent", "freshen air"])
def _(S):
    return [
        shell(rect(4, 11, 8, 10.5, rr(S, 3))),
        shell(rect(5.5, 6, 5, 5, rr(S, 2))),
        dot(14.5, 6.5, 1.1), dot(18, 4.5, 1.1), dot(18.5, 8.5, 1.1),
        dot(18, 15.5, 1.3),
        dot(18, 12.5, 1.6), dot(21, 15.5, 1.6), dot(18, 18.5, 1.6), dot(15, 15.5, 1.6),
    ]


@icon("plug-in-air-freshener", CAT, "Wall plug-in scent unit with a small scent bottle and rising scent waves",
      tags=["electric air freshener", "wall plug freshener", "scented oil", "fragrance plug", "room scent", "home fragrance", "odor control"])
def _(S):
    return [
        line("M8.5 7C7 5.5 10 4.5 8.5 3"),
        line("M12 7C10.5 5.5 13.5 4.5 12 3"),
        line("M15.5 7C14 5.5 17 4.5 15.5 3"),
        shell(rect(4, 8.5, 16, 9, rr(S, 3))),
        Part("dot", drop_d(12, 14, 1.7)),
        line(seg(9, 17.5, 9, 21.5)),
        line(seg(15, 17.5, 15, 21.5)),
    ]


@icon("reed-diffuser", CAT, "Small bottle with thin reeds fanning out from its neck",
      tags=["scent sticks", "fragrance diffuser", "aroma reeds", "home fragrance", "room scent", "rattan sticks", "essential oil"])
def _(S):
    return [
        line(seg(11.25, 10, 6.5, 2.5)),
        line(seg(12, 10, 12, 2.5)),
        line(seg(12.75, 10, 17.5, 2.5)),
        shell(poly([(6.5, 21.5), (6.5, 14.5), (10, 11.5), (10, 10), (14, 10), (14, 11.5), (17.5, 14.5), (17.5, 21.5)], closed=True, r=S.r)),
    ]


@icon("aroma-diffuser", CAT, "Dome-shaped ultrasonic diffuser releasing a curl of mist",
      tags=["essential oil diffuser", "ultrasonic diffuser", "aromatherapy", "mist maker", "scent diffuser", "relaxation", "spa"])
def _(S):
    return [
        line("M12 9.5C9.5 7.5 14.5 6.5 12 4.5C11 3.7 11 3 11.5 2.5"),
        shell("M5.5 17A6.5 6.5 0 0 1 18.5 17Z"),
        shell(rect(3.5, 17, 17, 4.5, rr(S, 2.25))),
    ]


# ============================================================================ pest control and dirt

@icon("drain-snake", CAT, "Coiled drain auger drum with a crank handle and a cable trailing out",
      tags=["plumber's snake", "drain auger", "pipe snake", "clogged drain", "plumbing", "unblock", "sink repair"])
def _(S):
    return [
        shell(circle(9.5, 11, 7)),
        detail(circle(9.5, 11, 3)),
        line(poly([(16.5, 11), (21.5, 11), (21.5, 6)], r=S.r)),
        line("M6 17.5C6 21.5 13 21.5 15 19.5"),
    ]


@icon("fly-swatter", CAT, "Fly swatter with a square mesh paddle on a long thin handle",
      tags=["fly killer", "bug swatter", "insect swat", "pest control", "mosquito swatter", "flies", "household pest"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 13, 11, rr(S, 3))),
        detail(seg(12, 2.5, 12, 13.5)),
        detail(seg(5.5, 8, 18.5, 8)),
        line(seg(12, 13.5, 12, 15.5)),
        shell(rect(10.5, 15.5, 3, 6, rr(S, 1.5))),
    ]


@icon("mousetrap", CAT, "Wooden spring mousetrap with a snap bar and a wedge of cheese on the trigger",
      tags=["rat trap", "snap trap", "pest control", "rodent", "mice", "spring trap", "vermin"])
def _(S):
    return [
        shell(rect(3, 5, 18, 14, rr(S, 3))),
        detail(poly([(6.5, 16), (6.5, 8.5), (13, 8.5), (13, 16)], r=S.r * 0.5)),
        Part("dot", poly([(15.5, 16.5), (19, 16.5), (19, 10)], closed=True, r=S.r * 0.4)),
    ]


@icon("insect-spray", CAT, "Aerosol can with a round cap spraying a mist toward a small bug",
      tags=["bug spray", "pesticide", "insecticide", "bug killer", "pest control", "ant killer", "roach spray"])
def _(S):
    return [
        shell(rect(3, 11, 7.5, 10.5, rr(S, 3))),
        shell(rect(4.5, 6, 4.5, 5, rr(S, 2))),
        dot(13, 7, 1.1), dot(16, 4.5, 1.1), dot(17.5, 8, 1.1),
        solid(ellipse(18, 16.5, 2.25, 3)),
        line(seg(15.75, 15, 13.75, 14)),
        line(seg(20.25, 15, 22, 14)),
        line(seg(15.75, 18, 13.75, 19)),
        line(seg(20.25, 18, 22, 19)),
    ]


def _coil_d(cx, cy):
    # spiral of alternating semicircles (radius grows 1.5 per half turn), drawn from the centre outward
    d = f"M{fmt(cx - 1.5)} {fmt(cy)}"
    x0 = cx - 1.5
    for i, r in enumerate([1.5, 3, 4.5, 6, 7.5]):
        x1 = x0 + 2 * r if i % 2 == 0 else x0 - 2 * r
        d += f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(cy)}"
        x0 = x1
    return d


@icon("mosquito-coil", CAT, "Spiral mosquito coil with a thin line of smoke rising from its end",
      tags=["mosquito repellent", "insect coil", "incense coil", "bug repellent", "outdoor", "camping", "pest control"])
def _(S):
    return [
        line(_coil_d(11.5, 13.5)),
        line("M19 13.5C19 10 21.5 10 21.5 7C21.5 5 20 4.5 20 2.5"),
    ]


@icon("sticky-fly-trap", CAT, "Hanging strip of fly paper with a few small dots stuck on it",
      tags=["fly paper", "flypaper", "fly strip", "insect trap", "hanging trap", "pest control", "flies"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 5)),
        shell("M8 5H16V19.5Q14 22 12 19.5Q10 17 8 19.5Z" if S.name == "line" else "M8 5H16V19.5Q14 22 12 19.5Q10 17 8 19.5Z"),
        dot(10.5, 9, 1.1), dot(13.5, 11.5, 1.1), dot(10.5, 14, 1.1),
    ]


@icon("dust-cloud", CAT, "Puff of dust with small particles floating around it",
      tags=["dusty", "dust particles", "allergens", "airborne dust", "dirt", "debris", "cleaning"])
def _(S):
    pts = [(4, 9), (8, 4.5), (18, 6), (21, 11)]
    big = 3.5 if S.name == "rounded" else 3
    marks = [sq(x - 1.1, y - 1.1, 2.2, 2.2) if S.name == "line" else dot(x, y, 1.25) for x, y in pts]
    return [
        shell(union_d(circle(7.5, 16, 3), circle(12, 16.5, big), circle(16.5, 16, 3), circle(9.5, 12, 3.5), circle(14.5, 11.5, 3.5))),
        *marks,
    ]


@icon("dust-mite", CAT, "Tiny rounded mite with eight short legs and a segmented back",
      tags=["house mite", "allergen", "bed mite", "microscopic pest", "allergy", "bedding", "mattress"])
def _(S):
    legs = []
    for a in (135, 165, 195, 225, -45, -15, 15, 45):
        x0, y0 = polar(12, 12, 4.5, a)
        x1, y1 = polar(12, 12, 9.25, a)
        legs.append(line(seg(x0, y0, x1, y1)))
    return [
        *legs,
        shell(ellipse(12, 12, 5, 5.5)),
        detail(poly([(9, 10.5), (12, 12), (15, 10.5)], r=S.r * 0.5) if S.name == "rounded" else seg(9, 11.5, 15, 11.5)),
    ]


@icon("wall-mold", CAT, "Wall panel with clusters of round fuzzy spots spreading across it",
      tags=["mildew", "black mold", "damp wall", "fungus", "spores", "moisture", "home inspection"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        dot(8.5, 14.5, 2.4), dot(13.5, 16.5, 1.4), dot(12.5, 11, 1.6), dot(16.5, 13, 1.2), dot(9, 8.5, 1.2),
    ]



@icon("disinfecting", CAT, "Spray bottle misting onto a small germ",
      tags=["sanitizing", "disinfect", "germs", "bacteria", "surface cleaning", "hygiene", "antibacterial spray"])
def _(S):
    germ = [line(seg(*polar(18, 16, 3, a), *polar(18, 16, 5.25, a))) for a in (0, 60, 120, 180, 240, 300)]
    return [
        shell(rect(2.5, 12, 8, 9.5, rr(S, 3))),
        shell(poly([(4, 12), (4, 8), (10.5, 8), (10.5, 10)], closed=True, r=S.r * 0.6)),
        dot(13.5, 9.5, 1.1), dot(16, 7.5, 1.1),
        solid(circle(18, 16, 2.75)),
        *germ,
    ]


@icon("chimney-brush", CAT, "Round spiky wire chimney brush on a flexible rod with a handle",
      tags=["chimney sweep", "flue brush", "sweeping chimney", "fireplace cleaning", "wire brush", "soot", "stove cleaning"])
def _(S):
    star = []
    for i in range(16):
        star.append(polar(12, 9, 6 if i % 2 == 0 else 4, -90 + i * 22.5))
    return [
        shell(poly(star, closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
        line("M12 13C12 15 13.5 16 13.5 17"),
        shell(rect(10.5, 17, 6, 4.5, rr(S, 2))),
    ]


@icon("pool-skimmer", CAT, "Flat mesh skimmer net on a long pole",
      tags=["pool net", "leaf skimmer", "swimming pool cleaning", "leaf net", "pool maintenance", "net", "pond"])
def _(S):
    return [
        line(seg(13.5, 12, 21, 3)),
        shell(rect(2.5, 11.5, 12, 9.5, rr(S, 3))),
        detail(seg(8.5, 11.5, 8.5, 21)),
        detail(seg(2.5, 16.25, 14.5, 16.25)),
    ]


@icon("boot-scraper", CAT, "Metal boot scraper with a blade between two short posts and brushes beneath",
      tags=["shoe scraper", "mud scraper", "boot cleaner", "doorstep", "entryway", "dirt removal", "mud room"])
def _(S):
    return [
        shell(rect(3, 6, 18, 3.5, rr(S, 1.75))),
        line(seg(5.5, 9.5, 5.5, 20.5)),
        line(seg(18.5, 9.5, 18.5, 20.5)),
        shell(rect(8.5, 13.5, 7, 7, rr(S, 1.5) if S.name == "rounded" else 0)),
        detail(seg(12, 13.5, 12, 20.5)),
    ]


@icon("doormat", CAT, "Rectangular coir doormat with a coarse texture and a thin border",
      tags=["welcome mat", "door mat", "entrance mat", "floor mat", "coir mat", "entryway", "rug"])
def _(S):
    return [
        shell(rect(2.5, 6, 19, 12, rr(S, 3))),
        detail(rect(6, 9.5, 12, 5, 0) if S.name == "line" else rect(6, 9.5, 12, 5, 1.5)),
    ]



# ============================================================================ air care

@icon("dehumidifier", CAT, "Upright box with a vent grille on top and a water drop on its front tank",
      tags=["moisture remover", "damp control", "humidity", "dry air", "basement", "mold prevention", "appliance"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, rr(S, 3))),
        detail(seg(8, 6.5, 16, 6.5)),
        detail(seg(8, 9.5, 16, 9.5)),
        Part("dot", drop_d(12, 16.25, 2.6)),
    ]


@icon("air-purifier", CAT, "Tall rounded air purifier with a grille band and air flow lines at the top",
      tags=["air cleaner", "hepa filter", "clean air", "allergens", "pollution", "purify air", "appliance"])
def _(S):
    return [
        line(seg(12, 6.5, 12, 2.5)),
        line(seg(8.5, 6.5, 6, 3.5)),
        line(seg(15.5, 6.5, 18, 3.5)),
        shell(rect(6, 8.5, 12, 13, rr(S, 4))),
        detail(seg(6, 13.5, 18, 13.5)),
        detail(seg(6, 17, 18, 17)),
    ]


@icon("humidifier", CAT, "Teardrop-shaped humidifier with a curl of mist rising from its top",
      tags=["mist maker", "moisture", "dry air", "cool mist", "bedroom", "baby room", "appliance"])
def _(S):
    body = ("M12 7C8.5 9.5 5.5 13 5.5 17Q5.5 21.5 12 21.5Q18.5 21.5 18.5 17C18.5 13 15.5 9.5 12 7Z" if S.name == "line"
            else "M12 7C9 9.5 5.5 13 5.5 17Q5.5 21.5 12 21.5Q18.5 21.5 18.5 17C18.5 13 15 9.5 12 7Z")
    return [
        line("M12 4.5C10.5 3.5 13.5 2.5 12 1.75"),
        shell(body),
        detail(seg(6, 17.5, 18, 17.5)),
    ]


# ============================================================================ laundry

@icon("laundry-detergent", CAT, "Detergent bottle with a finger hole handle and a measuring cap on top",
      tags=["washing liquid", "laundry liquid", "washing detergent", "clothes washing", "cleaner", "wash day", "laundry"])
def _(S):
    return [
        shell(rect(9, 2.5, 6, 3.5, rr(S, 1.5))),
        shell(poly([(4.5, 21.5), (4.5, 10), (9, 6), (16, 6), (19.5, 9.5), (19.5, 21.5)], closed=True, r=S.r)),
        detail(rect(13.5, 9.5, 3.5, 4.5, 0) if S.name == "line" else rect(13.5, 9.5, 3.5, 4.5, 1.75)),
        Part("dot", drop_d(10, 18, 2)),
    ]


@icon("detergent-powder", CAT, "Box of washing powder with a scoop resting on its open top",
      tags=["washing powder", "laundry powder", "soap powder", "scoop", "clothes washing", "cleaner", "laundry"])
def _(S):
    return [
        shell(rect(7, 3.5, 8, 4.5, rr(S, 2))),
        line(seg(15, 5.5, 20, 2.5)),
        shell(rect(4.5, 9, 15, 12.5, rr(S, 1.5) if S.name == "rounded" else 0)),
        Part("dot", drop_d(12, 17, 2.2)),
    ]


@icon("laundry-pod", CAT, "Soft pillow-shaped detergent pod with two swirled compartments",
      tags=["detergent pod", "washing capsule", "laundry capsule", "detergent tablet", "single dose", "cleaner", "laundry"])
def _(S):
    return [
        shell(rect(2.5, 5.5, 19, 13, 4.5 if S.name == "line" else 6.5)),
        detail("M12 5.5C8.5 9.5 15.5 14.5 12 18.5"),
    ]


@icon("fabric-softener", CAT, "Rounded bottle with a cap and a fluffy cloud mark on the label",
      tags=["fabric conditioner", "softener", "laundry scent", "soft clothes", "rinse aid", "cleaner", "laundry"])
def _(S):
    cloud = union_d(circle(9.75, 16.25, 1.9), circle(12.25, 14.75, 2.4), circle(14.75, 16.25, 1.9), rect(9.75, 16.25, 5, 1.9))
    return [
        shell(rect(9, 2.5, 6, 3.5, rr(S, 1.5))),
        shell(rect(4.5, 6, 15, 15.5, rr(S, 5))),
        Part("dot", cloud),
    ]


@icon("dryer-sheet", CAT, "Thin rectangular sheet with a crinkled edge and small wavy scent lines",
      tags=["tumble dryer sheet", "anti static sheet", "laundry sheet", "fresh scent", "softener sheet", "clothes dryer", "laundry"])
def _(S):
    return [
        shell(poly([(3.5, 3), (15.5, 3), (17.5, 7), (15.5, 11), (17.5, 15), (15.5, 21), (3.5, 21)], closed=True, r=S.r * 0.4)),
        detail("M6.5 8.5Q8.25 6.5 10 8.5T13.5 8.5"),
        detail("M6.5 14.5Q8.25 12.5 10 14.5T13.5 14.5"),
        line("M20.5 7C19 8.5 22 10 20.5 11.5"),
        line("M20.5 13.5C19 15 22 16.5 20.5 18"),
    ]


@icon("dryer-ball", CAT, "Round wool dryer ball with a stitched seam",
      tags=["wool dryer ball", "felted ball", "tumble dryer", "softener alternative", "eco laundry", "reusable", "laundry"])
def _(S):
    return [
        shell(circle(12, 12, 9.25)),
        detail(poly([(5.5, 10.5), (8.5, 13.5), (12, 10.5), (15.5, 13.5), (18.5, 10.5)], r=S.r)),
    ]


@icon("lint-trap", CAT, "Dryer lint screen, a mesh frame with a layer of fluff on top",
      tags=["lint filter", "dryer lint", "lint screen", "fluff", "dryer maintenance", "fire safety", "laundry"])
def _(S):
    return [
        line("M6 8Q5 4.5 8.5 5Q10 3 12.5 4.5Q15.5 3.5 16 6Q19.5 6 18 8"),
        shell(rect(3.5, 8, 17, 13.5, rr(S, 2.5))),
        detail(seg(9.5, 8, 9.5, 21.5)),
        detail(seg(14.5, 8, 14.5, 21.5)),
        detail(seg(3.5, 14.75, 20.5, 14.75)),
    ]


@icon("clothespin", CAT, "Wooden clothespin with two legs joined by a spring",
      tags=["peg", "clothes peg", "clip", "washing line", "hang laundry", "pin", "laundry"])
def _(S):
    return [
        shell(poly([(8, 2.5), (16, 2.5), (16, 11), (14.5, 21.5), (9.5, 21.5), (8, 11)], closed=True, r=S.r)),
        detail(seg(12, 12, 12, 21.5)),
        dot(12, 7, 1.5) if S.name == "rounded" else sq(10.5, 5.5, 3, 3),
    ]


@icon("peg-bag", CAT, "Fabric peg bag on a hanger with a round opening for clothespins",
      tags=["clothespin bag", "peg holder", "pin bag", "washing line", "hanger bag", "outdoor laundry", "laundry"])
def _(S):
    return [
        line("M7.5 8.5Q12 0.5 16.5 8.5"),
        shell(poly([(6, 8.5), (18, 8.5), (19.5, 21.5), (4.5, 21.5)], closed=True, r=S.r)),
        detail(ellipse(12, 14.5, 4.25, 3.25)),
    ]


@icon("clothesline", CAT, "Line strung between two posts with a shirt and a sock pegged on it",
      tags=["washing line", "drying laundry", "hang clothes", "outdoor drying", "airing clothes", "garden", "laundry"])
def _(S):
    shirt = [(4.5 + 0.5 * x, 6 + 0.5 * y) for x, y in [(8, 3), (3, 6), (5, 10), (7, 9), (7, 21), (17, 21), (17, 9), (19, 10), (21, 6), (16, 3)]]
    shirt = [(x + 1, y + 1.5) for x, y in shirt]
    return [
        line(seg(2.5, 2.5, 2.5, 21.5)),
        line(seg(21.5, 2.5, 21.5, 21.5)),
        line("M2.5 5Q12 8 21.5 5"),
        shell(poly(shirt, closed=True, r=S.r * 0.4)),
        shell(poly([(16.5, 8), (19, 8), (19, 15.5), (15, 15.5), (15, 13), (16.5, 13)], closed=True, r=S.r * 0.5)),
    ]


@icon("clothes-drying-rack", CAT, "Folding clothes airer with rails and a towel draped over the top rail",
      tags=["airer", "drying rack", "indoor drying", "laundry rack", "horse", "towel rail", "laundry"])
def _(S):
    return [
        line(seg(4, 21.5, 5.5, 3.5)),
        line(seg(20, 21.5, 18.5, 3.5)),
        line(seg(5.5, 3.5, 18.5, 3.5)),
        line(seg(5, 9.5, 19, 9.5)),
        line(seg(4.5, 15.5, 19.5, 15.5)),
        shell(rect(8.5, 9.5, 7, 9, rr(S, 1.5))),
    ]


@icon("rotary-clothesline", CAT, "Umbrella-shaped rotary washing line on a central pole with radiating lines",
      tags=["rotary dryer", "whirligig", "washing line", "umbrella clothes line", "garden drying", "outdoor", "laundry"])
def _(S):
    return [
        line(seg(12, 5, 12, 21.5)),
        line(seg(12, 5, 3, 12.5)),
        line(seg(12, 5, 21, 12.5)),
        line(seg(3, 12.5, 21, 12.5)),
        line(seg(7.25, 8.75, 16.75, 8.75)),
    ]


@icon("ironing-board", CAT, "Side view of an ironing board with a pointed end on crossed folding legs",
      tags=["iron board", "pressing", "folding board", "garment care", "wrinkles", "ironing", "laundry"])
def _(S):
    return [
        shell(poly([(2.5, 6.5), (17, 6.5), (21.5, 9), (17, 11.5), (2.5, 11.5)], closed=True, r=S.r * 0.6)),
        line(seg(6.5, 11.5, 15.5, 21.5)),
        line(seg(15.5, 11.5, 6.5, 21.5)),
    ]


@icon("garment-steamer", CAT, "Handheld garment steamer with a flat head releasing steam",
      tags=["clothes steamer", "travel steamer", "wrinkle remover", "steam iron alternative", "garment care", "fabric steam", "laundry"])
def _(S):
    return [
        shell(rect(2.5, 9.5, 8, 12, rr(S, 3))),
        line(seg(10.5, 14, 13.5, 14)),
        shell(poly([(13.5, 10.5), (18.5, 10.5), (21.5, 14), (18.5, 17.5), (13.5, 17.5)], closed=True, r=S.r * 0.6)),
        line("M15 7.5C13.5 6 16.5 5 15 3.5"),
        line("M19 7.5C17.5 6 20.5 5 19 3.5"),
    ]


@icon("laundry-bag", CAT, "Drawstring laundry bag stuffed with clothes and a cord looped at the top",
      tags=["dirty clothes bag", "laundry sack", "drawstring bag", "wash bag", "hamper bag", "dirty washing", "laundry"])
def _(S):
    return [
        line(seg(10.5, 7.5, 8, 4)),
        line(seg(12, 7.5, 12, 3.5)),
        line(seg(13.5, 7.5, 16, 4)),
        shell(poly([(9.5, 11), (10.5, 7.5), (13.5, 7.5), (14.5, 11)], closed=True, r=S.r * 0.4)),
        shell("M9.5 11C3.5 12.5 3 18 5.5 20.5C8 22.5 16 22.5 18.5 20.5C21 18 20.5 12.5 14.5 11Z"),
        detail("M10.5 13C10.5 16 8.5 16 8.5 19"),
        detail("M13.5 13C13.5 16 15.5 16 15.5 19"),
    ]


@icon("mesh-laundry-bag", CAT, "Zippered mesh wash bag with a diamond net pattern",
      tags=["delicates bag", "wash bag", "lingerie bag", "net bag", "washing machine bag", "zip bag", "laundry"])
def _(S):
    return [
        shell(rect(3.5, 4, 17, 17.5, rr(S, 3))),
        detail(seg(3.5, 8, 20.5, 8)),
        detail(poly([(3.5, 14.5), (8, 10.75), (12, 14.5), (16, 10.75), (20.5, 14.5)])),
        detail(poly([(3.5, 14.5), (8, 18.25), (12, 14.5), (16, 18.25), (20.5, 14.5)])),
    ]


@icon("washboard", CAT, "Wooden washboard with a ridged panel in a frame",
      tags=["scrub board", "hand washing", "old fashioned laundry", "rub board", "traditional", "wash day", "laundry"])
def _(S):
    def ridge(y):
        pts = [(4 + 2 * i, y + (0.8 if i % 2 else -0.8)) for i in range(9)]
        return detail(poly(pts, r=S.r * 0.4))
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 3))),
        detail(seg(4, 6.5, 20, 6.5)),
        ridge(10.5), ridge(14), ridge(17.5),
    ]


@icon("washtub", CAT, "Round metal washtub with two side handles and bubbles above the water",
      tags=["laundry tub", "wash basin", "zinc tub", "hand washing", "old fashioned laundry", "bucket", "suds"])
def _(S):
    return [
        dot(9, 4.5, 1.4), dot(13.5, 3.5, 1.1), dot(16, 6.5, 1.25),
        shell(rect(4, 8.5, 16, 3.5, rr(S, 1.75))),
        shell(poly([(5.5, 12), (18.5, 12), (17, 21), (7, 21)], closed=True, r=S.r * 0.6)),
        line(poly([(4.5, 14), (2.5, 14), (2.5, 17)], r=S.r * 0.5)),
        line(poly([(19.5, 14), (21.5, 14), (21.5, 17)], r=S.r * 0.5)),
    ]
