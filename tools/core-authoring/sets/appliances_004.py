"""TypeIcon Core: appliances (batch appliances_004).

Original drawings of small home appliances, lamps, connectors, batteries and household fittings, mostly in
front or side view. Bodies are shells; seams, dials and grilles are details; cords, stems and rays are lines.
Long hand-held devices are drawn upright and turned 45 degrees clockwise (handle to the bottom-left), matching
the tools and kitchen sets.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path.parser import parse_path
from geometry import SCALE, D, P, ST, U, fmt, path_to_d, rotation

CAT = "appliances"
TILT = 45


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    """Container corner radius for the style, optionally capped for small shapes (Line keeps it tighter)."""
    if cap is None:
        return S.R
    return min(S.R, cap) if S.name == "rounded" else min(S.R, cap) * 0.4


def tf(d, m):
    """Apply an affine matrix (a, b, c, d, e, f) to a d-string, keeping open paths open."""
    pen = SVGPathPen(None, ntos=fmt)
    parse_path(d, TransformPen(pen, m))
    return pen.getCommands()


def rot(d, deg=TILT, cx=12.0, cy=12.0):
    """Rotate a d-string clockwise on screen about (cx, cy)."""
    return tf(d, rotation(deg, cx, cy))


def mv(d, dx, dy):
    return tf(d, (1, 0, 0, 1, dx, dy))


def flip(d):
    """Mirror across the vertical centre line."""
    return tf(d, (-1, 0, 0, 1, 24, 0))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def hole(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def fit(parts, cx=12.0, cy=12.0):
    """Translate parts so their drawn bounds are centred on (cx, cy), snapped to half pixels."""
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
    """Turn an upright device (handle down) so the handle points to the bottom-left, then centre it."""
    return fit([Part(p.kind, rot(p.d, deg), p.attrs) for p in parts])


def top_round(x, y, w, h, rt, rb=0.0):
    """Rectangle with top corners of radius rt and bottom corners of radius rb."""
    return (f"M{fmt(x)} {fmt(y + h - rb)}V{fmt(y + rt)}A{fmt(rt)} {fmt(rt)} 0 0 1 {fmt(x + rt)} {fmt(y)}"
            f"H{fmt(x + w - rt)}A{fmt(rt)} {fmt(rt)} 0 0 1 {fmt(x + w)} {fmt(y + rt)}V{fmt(y + h - rb)}"
            + (f"A{fmt(rb)} {fmt(rb)} 0 0 1 {fmt(x + w - rb)} {fmt(y + h)}" if rb else "")
            + f"H{fmt(x + rb)}"
            + (f"A{fmt(rb)} {fmt(rb)} 0 0 1 {fmt(x)} {fmt(y + h - rb)}" if rb else "") + "Z")


def bolt(cx, cy, s=1.0):
    """Small lightning bolt polygon centred on (cx, cy), about 3.5 x 6 at s = 1."""
    pts = [(0.6, -3), (-1.8, 0.4), (-0.1, 0.4), (-0.6, 3), (1.8, -0.4), (0.1, -0.4)]
    return poly([(cx + x * s, cy + y * s) for x, y in pts], closed=True)


def plus(cx, cy, a=1.5):
    return f"M{fmt(cx - a)} {fmt(cy)}H{fmt(cx + a)}M{fmt(cx)} {fmt(cy - a)}V{fmt(cy + a)}"


def drop(cx, cy, h=5.0):
    """Water drop: pointed top at cy - h/2, round bottom."""
    r = h * 0.36
    by = cy + h / 2 - r
    ty = cy - h / 2
    return (f"M{fmt(cx)} {fmt(ty)}C{fmt(cx + r * 0.6)} {fmt(ty + h * 0.3)} {fmt(cx + r)} {fmt(by - r * 0.4)} "
            f"{fmt(cx + r)} {fmt(by)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx - r)} {fmt(by)}"
            f"C{fmt(cx - r)} {fmt(by - r * 0.4)} {fmt(cx - r * 0.6)} {fmt(ty + h * 0.3)} {fmt(cx)} {fmt(ty)}Z")


# ============================================================================ chargers and devices

@icon("wireless-charger", CAT, "Phone standing over a flat charging pad with wireless waves and a bolt",
      tags=["wireless charging", "charging pad", "cordless charger", "phone charger", "inductive", "charge"])
def _(S):
    return [
        shell(rect(8, 2.5, 8, 12.5, rr(S, 2))),
        hole(bolt(12, 8.75, 0.85)),
        line(arc(12, 8.75, 7.5, 135, 225)),
        line(arc(12, 8.75, 7.5, -45, 45)),
        shell(rect(3, 18, 18, 3.5, rr(S, 1.75))),
    ]


@icon("3d-printer", CAT, "3D printer: a cube frame with a print head on a gantry above a printed part",
      tags=["3d printing", "additive manufacturing", "fdm", "printer", "maker", "prototype"])
def _(S):
    return [
        line(rect(3, 2.5, 18, 19, rr(S))),
        line(seg(3, 8, 21, 8)),
        shell(rect(9.5, 6, 5, 4.5, rr(S, 1))),
        solid(poly([(10.75, 10.5), (13.25, 10.5), (12, 12.5)], closed=True)),
        shell(poly([(8.5, 21.5), (10.5, 15.5), (13.5, 15.5), (15.5, 21.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("irrigation-controller", CAT, "Wall-mounted sprinkler timer box with a water drop and a big dial",
      tags=["sprinkler timer", "irrigation timer", "watering", "garden", "controller", "schedule"])
def _(S):
    return [
        shell(rect(3, 3.5, 18, 17, rr(S))),
        detail(circle(9.5, 12, 3.5)),
        detail(seg(9.5, 12, 9.5, 10)),
        hole(drop(16.5, 8.5, 4.5)),
        dot(16.5, 14, 1),
        dot(16.5, 17, 1),
    ]


@icon("bidet-seat", CAT, "Toilet seat seen from above with a control panel arm on one side",
      tags=["bidet", "electronic bidet", "smart toilet", "toilet seat", "bathroom", "hygiene"])
def _(S):
    seat = ellipse(10.5, 14, 6.5, 7.5)
    back = rect(3, 2.5, 15, 5, rr(S, 2))
    arm = rect(16, 2.5, 6, 12, rr(S, 2))
    return [
        shell(union(seat, back, arm)),
        detail(seg(4.5, 7.5, 16, 7.5)),
        detail(ellipse(10.5, 14.5, 2.75, 3.75)),
        dot(19, 7, 1),
        dot(19, 10.5, 1),
    ]


@icon("floodlight-camera", CAT, "Security camera with two angled flood lamps on a wall mount",
      tags=["security light", "floodlight", "camera", "motion light", "outdoor", "surveillance"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 6.5, rr(S))),
        detail(seg(8.5, 3, 8.5, 9.5)),
        detail(seg(15.5, 3, 15.5, 9.5)),
        line(seg(12, 9.5, 12, 11.5)),
        shell(circle(12, 16, 4.5)),
        dot(12, 16, 1.75) if S.name == "rounded" else hole(rect(10.25, 14.25, 3.5, 3.5)),
        line(seg(4.5, 13, 3, 17)),
        line(seg(19.5, 13, 21, 17)),
    ]


@icon("self-cleaning-litter-box", CAT, "Round domed automatic litter box with an entry hole and a waste drawer",
      tags=["litter box", "cat litter", "automatic", "pet", "cat", "self cleaning"])
def _(S):
    dx = math.sqrt(8.5 ** 2 - 4.5 ** 2)
    drum = f"M{fmt(12 - dx)} 16.5A8.5 8.5 0 1 1 {fmt(12 + dx)} 16.5Z"
    base = rect(3, 16.5, 18, 5, rr(S, 1.5))
    return [
        shell(union(drum, base)),
        detail(seg(3, 16.5, 21, 16.5)),
        detail(circle(12, 10, 3)),
    ]


@icon("nose-trimmer", CAT, "Pen-shaped nose hair trimmer with a small rounded head and a button",
      tags=["nose hair", "ear hair", "trimmer", "grooming", "shaver", "personal care"])
def _(S):
    body = union(top_round(9.75, 2.5, 4.5, 6.5, 2.25), rect(8.5, 8.5, 7, 13, rr(S, 2.5)))
    return tilt([
        shell(body),
        detail(seg(8.5, 8.5, 15.5, 8.5)),
        dot(12, 13, 1.25),
    ])


@icon("uv-nail-lamp", CAT, "Low domed nail dryer lamp with a wide front opening and light rays inside",
      tags=["nail lamp", "uv lamp", "led nail dryer", "gel nails", "manicure", "salon"])
def _(S):
    dome = "M2 19.5V14Q2 5 12 5Q22 5 22 14V19.5Z"
    mouth = "M5.5 20V15A6.5 4.5 0 0 1 18.5 15V20Z"
    return [
        shell(minus(dome, mouth)),
        line(seg(12, 14, 12, 18)),
        line(seg(8.75, 15, 8.25, 18)),
        line(seg(15.25, 15, 15.75, 18)),
    ]


@icon("massage-chair", CAT, "Reclining massage chair with a padded back, armrest, footrest and a corded remote",
      tags=["massage", "recliner", "shiatsu", "relax", "spa", "chair"])
def _(S):
    back = poly([(3, 5), (7, 3), (10, 13), (6, 14.5)], closed=True, r=S.r)
    seat = rect(6, 12, 10.5, 5, rr(S, 2))
    rest = poly([(14.5, 12.5), (21.5, 18), (19.5, 20.5), (13, 16)], closed=True, r=S.r)
    return [
        shell(union(back, seat, rest)),
        detail(seg(9.5, 12, 14, 12)),
        line(seg(10, 17, 10, 21)),
        line(seg(6.5, 21, 13.5, 21)),
        shell(rect(17.5, 3, 3, 5, rr(S, 1))),
        line("M14.5 12Q16 10 19 8"),
    ]


# ============================================================================ bulbs and lamps

@icon("candle-bulb", CAT, "Candle-shaped light bulb with a pointed flame tip and a narrow screw base",
      tags=["candle bulb", "chandelier bulb", "light bulb", "e14", "flame bulb", "lighting"])
def _(S):
    glass = "M12 2.5C15 6.5 16.5 9.5 16.5 12.5A4.5 4.5 0 0 1 7.5 12.5C7.5 9.5 9 6.5 12 2.5Z"
    base = rect(9.5, 16, 5, 5.5, rr(S, 1))
    return [
        shell(union(glass, base)),
        detail(seg(9.5, 18.75, 14.5, 18.75)),
        detail(seg(12, 9.5, 12, 13)),
    ]


@icon("bollard-light", CAT, "Short post light with a glowing band near the top standing on a path",
      tags=["path light", "garden light", "bollard", "outdoor lighting", "landscape light", "post light"])
def _(S):
    return [
        shell(top_round(8.5, 3, 7, 17.5, 3.5, 0)),
        detail(seg(8.5, 7.5, 15.5, 7.5)),
        detail(seg(8.5, 11.5, 15.5, 11.5)),
        line(seg(2, 20.5, 8.5, 20.5)),
        line(seg(15.5, 20.5, 22, 20.5)),
        line(seg(3, 9.5, 5.5, 9.5)),
        line(seg(18.5, 9.5, 21, 9.5)),
    ]


@icon("tiffany-lamp", CAT, "Table lamp with a wide domed stained glass shade on a slender base",
      tags=["stained glass lamp", "mosaic lamp", "table lamp", "vintage lamp", "lighting", "decor"])
def _(S):
    return [
        shell(L(S, "M2.5 12Q2.5 3.5 12 3.5Q21.5 3.5 21.5 12Z", "M2.5 11A1 1 0 0 0 3.5 12H20.5A1 1 0 0 0 21.5 11Q21.5 3.5 12 3.5Q2.5 3.5 2.5 11Z")),
        detail("M4.5 8Q12 6 19.5 8"),
        detail(seg(8, 7.25, 8, 12)),
        detail(seg(12, 7, 12, 12)),
        detail(seg(16, 7.25, 16, 12)),
        line(seg(12, 12, 12, 19)),
        shell(rect(7.5, 19, 9, 2.5, rr(S, 1.25))),
    ]


@icon("bankers-lamp", CAT, "Desk lamp with a long half-cylinder shade, a curved stem and a pull chain",
      tags=["bankers lamp", "library lamp", "desk lamp", "green lamp", "office", "lighting"])
def _(S):
    return [
        shell("M2.5 12V10.5A4.5 4.5 0 0 1 7 6H17A4.5 4.5 0 0 1 21.5 10.5V12Z"),
        line(seg(12, 12, 12, 19.5)),
        shell(rect(4, 19.5, 16, 2, rr(S, 1))),
        line(seg(17.5, 12, 17.5, 15)),
        dot(17.5, 16.25, 1.25),
    ]


@icon("work-light", CAT, "Portable work lamp: a caged bulb with a hanging hook and a handle",
      tags=["work lamp", "trouble light", "shop light", "inspection lamp", "garage", "hanging light"])
def _(S):
    cage = rect(7, 5.5, 10, 10.5, L(S, 3, 5))
    grip = rect(9.5, 15, 5, 6.5, rr(S, 1.5))
    return [
        shell(union(cage, grip)),
        detail(seg(12, 5.5, 12, 16)),
        detail(seg(7, 10.75, 17, 10.75)),
        line("M12 5.5V4A1.75 1.75 0 0 0 8.5 4"),
    ]


@icon("battery-charger", CAT, "Charger base with two AA batteries standing in slots and a bolt",
      tags=["battery charger", "rechargeable", "aa charger", "nimh", "charging", "batteries"])
def _(S):
    body = union(rect(3, 13, 18, 8.5, rr(S, 2)), rect(4.5, 5.5, 5, 9, rr(S, 1)), rect(14.5, 5.5, 5, 9, rr(S, 1)))
    return [
        shell(body),
        solid(rect(6, 3, 2, 2)),
        solid(rect(16, 3, 2, 2)),
        hole(bolt(12, 17.25, 0.75)),
    ]


# ============================================================================ kitchen

@icon("slow-juicer", CAT, "Upright slow juicer with a feed hopper and auger chamber pouring into a cup",
      tags=["masticating juicer", "cold press", "juicer", "juice", "auger", "kitchen"])
def _(S):
    hopper = poly([(4.5, 2.5), (14.5, 2.5), (12.5, 6), (6.5, 6)], closed=True, r=S.r * 0.6)
    body = union(hopper, rect(4.5, 5.5, 10, 9.5, L(S, 1, 3)), rect(3, 15, 13, 6.5, rr(S)))
    return [
        shell(body),
        detail(seg(7, 9.25, 12, 7.75)),
        detail(seg(7, 12.75, 12, 11.25)),
        line(poly([(14.5, 11.5), (19.5, 11.5), (19.5, 14)], r=S.r)),
        shell(poly([(18, 16), (21.5, 16), (21, 21.5), (18.5, 21.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("yogurt-maker", CAT, "Round appliance base with a clear dome lid over three small jars",
      tags=["yoghurt maker", "yogurt", "fermenting", "incubator", "jars", "kitchen"], aliases=["yoghurt-maker"])
def _(S):
    return [
        line("M3.5 16V13A8.5 8 0 0 1 20.5 13V16"),
        solid(rect(10.75, 3, 2.5, 2, L(S, 0, 0.75))),
        hole(rect(5.75, 10.5, 3.5, 4, L(S, 0.3, 1))),
        hole(rect(10.25, 10.5, 3.5, 4, L(S, 0.3, 1))),
        hole(rect(14.75, 10.5, 3.5, 4, L(S, 0.3, 1))),
        shell(rect(2.5, 16.5, 19, 5, rr(S, 2))),
    ]


@icon("donut-maker", CAT, "Donut maker with its lid hinged open above a plate of ring-shaped moulds",
      tags=["doughnut maker", "donut", "mini donuts", "baking", "snack maker", "kitchen"], aliases=["doughnut-maker"])
def _(S):
    return [
        shell(poly([(5, 2.5), (19, 2.5), (20.5, 9), (3.5, 9)], closed=True, r=S.r)),
        shell(rect(2.5, 11.5, 19, 10, rr(S))),
        detail(circle(8, 16.5, 2.25)),
        detail(circle(16, 16.5, 2.25)),
    ]


@icon("electric-wine-opener", CAT, "Slim electric corkscrew standing on the neck of a wine bottle",
      tags=["wine opener", "electric corkscrew", "cork remover", "wine", "bottle opener", "bar"])
def _(S):
    bottle = "M10.25 13V15.5Q10.25 17 7.5 18.25Q6 19 6 21.5H18Q18 19 16.5 18.25Q13.75 17 13.75 15.5V13Z"
    return [
        shell(union(rect(8.75, 2.5, 6.5, 12, rr(S, 3)), bottle)),
        detail(seg(8.75, 14.5, 15.25, 14.5)),
        dot(12, 6.5, 1.25),
    ]


# ============================================================================ climate

@icon("cassette-air-conditioner", CAT, "Square ceiling air conditioner panel with a central grille and a vent on each side",
      tags=["ceiling ac", "cassette ac", "air conditioning", "hvac", "cooling", "ceiling unit"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S))),
        detail(rect(9.5, 9.5, 5, 5, L(S, 0, 1))),
        detail(seg(9, 6, 15, 6)),
        detail(seg(9, 18, 15, 18)),
        detail(seg(6, 9, 6, 15)),
        detail(seg(18, 9, 18, 15)),
    ]


# ============================================================================ cords and connectors

@icon("extension-cord", CAT, "Extension lead with a plug on one end and a socket block on the other",
      tags=["extension lead", "extension cable", "power cord", "plug", "socket", "electrical"])
def _(S):
    return [
        line(seg(4.5, 2.5, 4.5, 4.5)),
        line(seg(7.5, 2.5, 7.5, 4.5)),
        shell(rect(3, 4.5, 6, 5, rr(S, 1.5))),
        line("M6 9.5V13Q6 18 11 18H13"),
        shell(rect(13, 13, 8.5, 8.5, rr(S, 2.5))),
        dot(15.75, 17.25, 1),
        dot(18.75, 17.25, 1),
    ]


@icon("iec-connector", CAT, "Face of an IEC power cord connector: a flat-topped shape with three slots",
      tags=["iec", "c13", "kettle plug", "power cord", "computer cable", "connector"], aliases=["c13-connector"])
def _(S):
    return [
        shell(poly([(3, 5), (21, 5), (21, 13), (16.5, 19), (7.5, 19), (3, 13)], closed=True, r=S.r)),
        hole(rect(11, 8, 2, 4, L(S, 0, 0.8))),
        hole(rect(6.5, 11, 2, 4, L(S, 0, 0.8))),
        hole(rect(15.5, 11, 2, 4, L(S, 0, 0.8))),
    ]


@icon("dc-barrel-plug", CAT, "Round DC barrel power plug with a hollow metal tip on a thin cable",
      tags=["barrel jack", "dc plug", "power adapter", "coaxial power", "charger plug", "connector"],
      aliases=["barrel-jack"])
def _(S):
    return tilt([
        shell(union(rect(10, 2.5, 4, 6, rr(S, 1)), rect(8.5, 8, 7, 8.5, rr(S, 2.5)))),
        detail(seg(8.5, 8, 15.5, 8)),
        line(seg(12, 16.5, 12, 21.5)),
    ])


@icon("xlr-connector", CAT, "Round XLR audio connector face with three pin holes and a latch tab",
      tags=["xlr", "microphone cable", "audio connector", "balanced audio", "mic plug", "pro audio"],
      aliases=["xlr-plug"])
def _(S):
    pin = (lambda x, y: dot(x, y, 1.3)) if S.name == "rounded" else (lambda x, y: hole(rect(x - 1.1, y - 1.1, 2.2, 2.2)))
    return [
        shell(union(circle(12, 13, 8.5), rect(9.5, 2.5, 5, 4, rr(S, 1.5)))),
        pin(8.5, 11.5),
        pin(15.5, 11.5),
        pin(12, 16.5),
    ]


@icon("speaker-terminals", CAT, "Plate with two binding posts marked plus and minus and wires below",
      tags=["binding posts", "speaker wire", "amplifier", "audio terminals", "hifi", "polarity"])
def _(S):
    return [
        line(plus(7.5, 4.5, 1.75)),
        line(seg(14.75, 4.5, 18.25, 4.5)),
        shell(rect(2.5, 8, 19, 9, rr(S, 2.5))),
        detail(circle(7.5, 12.5, 1.75)),
        detail(circle(16.5, 12.5, 1.75)),
        line(seg(7.5, 17, 7.5, 21.5)),
        line(seg(16.5, 17, 16.5, 21.5)),
    ]


@icon("scart-connector", CAT, "Wide SCART plug face with one cut corner and two rows of pins",
      tags=["scart", "euroconnector", "av cable", "tv connector", "video cable", "retro"])
def _(S):
    pin = (lambda x, y: dot(x, y, 1)) if S.name == "rounded" else (lambda x, y: hole(rect(x - 0.9, y - 0.9, 1.8, 1.8)))
    return [
        shell(poly([(2, 6.5), (22, 6.5), (22, 13.5), (18.5, 17.5), (2, 17.5)], closed=True, r=S.r)),
        *[pin(x, 10.25) for x in (5.5, 9, 12.5, 16, 19.5)],
        *[pin(x, 14) for x in (7.25, 10.75, 14.25)],
    ]


# ============================================================================ beauty and wellness

@icon("hood-dryer", CAT, "Salon hood hair dryer on a stand arm above a chair",
      tags=["salon dryer", "hair dryer", "bonnet dryer", "hood", "hair salon", "beauty"], aliases=["bonnet-dryer"])
def _(S):
    return [
        shell("M3.5 9.5A7 7 0 0 1 17.5 9.5Z" if S.name == "line" else
              "M3.5 8.5A7 7 0 0 1 17.5 8.5V9A0.5 0.5 0 0 1 17 9.5H4A0.5 0.5 0 0 1 3.5 9Z"),
        line(poly([(17.5, 6.5), (20.5, 6.5), (20.5, 21.5)], r=S.r)),
        shell(union(rect(3.5, 12.5, 4.5, 6.5, rr(S, 2)), rect(3.5, 15.5, 12, 3.5, rr(S, 1.5)))),
        line(seg(9.5, 19, 9.5, 21.5)),
        line(seg(6, 21.5, 13, 21.5)),
    ]


@icon("light-therapy-lamp", CAT, "Upright light therapy panel on a small stand with a sun symbol",
      tags=["sad lamp", "light box", "daylight lamp", "bright light therapy", "seasonal", "wellness"],
      aliases=["sad-lamp"])
def _(S):
    rays = [seg(*pt_on(12, 9.5, 4, a), *pt_on(12, 9.5, 5.25, a)) for a in range(0, 360, 45)]
    return [
        shell(rect(3.5, 2.5, 17, 14.5, rr(S))),
        hole(circle(12, 9.5, 2.25)),
        *[detail(r) for r in rays],
        shell(poly([(10.5, 17), (13.5, 17), (15.5, 21.5), (8.5, 21.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("sauna-stove", CAT, "Sauna heater box with a pile of stones on top and heat waves rising",
      tags=["sauna heater", "kiuas", "sauna", "hot stones", "steam", "spa"])
def _(S):
    stones = union(circle(7.5, 11, 2.5), circle(12, 10.5, 2.75), circle(16.5, 11, 2.5))
    return [
        shell(union(stones, rect(4, 12, 16, 9.5, rr(S, 2)))),
        detail(seg(4, 12.5, 20, 12.5)),
        detail(seg(8, 16.75, 16, 16.75)),
        *[line(f"M{x} 6.5Q{x - 1.25} 5.25 {x} 4Q{x + 1.25} 2.75 {x} 1.5") for x in (8, 12, 16)],
    ]


@icon("stove-knob", CAT, "Round cooker control knob with a pointer and tick marks around it",
      tags=["cooker knob", "oven knob", "burner control", "dial", "temperature", "kitchen"])
def _(S):
    ticks = [line(seg(*pt_on(12, 13, 8.25, a), *pt_on(12, 13, 9.75, a))) for a in (180, 225, 270, 315, 0)]
    return [
        shell(circle(12, 13, 6)),
        detail(rect(10.75, 9, 2.5, 8, L(S, 0, 1.25))),
        *ticks,
    ]


# ============================================================================ plumbing and fittings

def _pipe(d, w=5.0):
    """Closed outline of a pipe of width w following the centreline d."""
    return path_to_d(ST(d, w, "butt", "round"))


@icon("sink-trap", CAT, "P-trap under a sink: a drain pipe dropping into a U bend and turning to the wall",
      tags=["p trap", "u bend", "drain", "plumbing", "sink", "waste pipe"], aliases=["p-trap"])
def _(S):
    return [
        shell(union(_pipe("M8 5V13A4 4 0 0 0 16 13V11.5Q16 9 18.5 9H21.5"), rect(4, 2.5, 8, 2.5, rr(S, 1)))),
        line(seg(22, 5, 22, 13)),
    ]


# ============================================================================ lamps

@icon("picture-light", CAT, "Slim tube lamp on a short arm above a framed picture, light falling onto it",
      tags=["picture lamp", "art light", "gallery light", "frame light", "wall light", "painting"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 3, rr(S, 1.5))),
        line(seg(12, 5.5, 12, 9.5)),
        line(seg(5.5, 7.5, 4, 9)),
        line(seg(18.5, 7.5, 20, 9)),
        shell(rect(3, 11.5, 18, 10, rr(S, 2))),
        detail(poly([(6.5, 18.5), (10, 14.5), (12.5, 17), (14, 15.5), (17.5, 18.5)], r=S.r * 0.5)),
    ]


@icon("monitor-light-bar", CAT, "Long lamp bar clipped on top of a monitor, lighting the desk below",
      tags=["screen bar", "monitor lamp", "desk light", "screen light", "workspace", "home office"],
      aliases=["screen-bar"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 3, rr(S, 1.5))),
        shell(rect(5.5, 7.5, 13, 9, rr(S, 2))),
        line(seg(12, 16.5, 12, 19.5)),
        line(seg(2, 21, 22, 21)),
        line(seg(3.5, 8, 2.5, 13)),
        line(seg(20.5, 8, 21.5, 13)),
    ]


@icon("moon-lamp", CAT, "Round moon-shaped lamp with craters resting in a low stand",
      tags=["moon light", "night light", "lunar lamp", "moon", "bedroom", "decor"])
def _(S):
    return [
        shell(union(circle(12, 10.5, 8.5), poly([(8.5, 21.5), (9.5, 18), (14.5, 18), (15.5, 21.5)], closed=True, r=S.r * 0.5))),
        detail(circle(8.5, 8, 2)),
        detail(circle(15, 12, 1.5)),
        dot(14.5, 6, 1),
        dot(9.5, 13.5, 0.9),
    ]


@icon("torchiere-lamp", CAT, "Tall floor lamp with a slim pole and an upturned bowl shade casting light upward",
      tags=["torchiere", "uplighter", "floor lamp", "uplight", "standing lamp", "lighting"], aliases=["uplighter"])
def _(S):
    return [
        line(seg(8.5, 5.5, 6.5, 2.5)),
        line(seg(12, 5.5, 12, 2.5)),
        line(seg(15.5, 5.5, 17.5, 2.5)),
        shell("M6.5 7.5H17.5A5.5 3.5 0 0 1 6.5 7.5Z" if S.name == "line" else
              "M7.5 7.5H16.5A1 1 0 0 1 17.4 8.9A5.5 3.5 0 0 1 6.6 8.9A1 1 0 0 1 7.5 7.5Z"),
        line(seg(12, 11, 12, 20)),
        shell(rect(7.5, 20, 9, 1.5, L(S, 0.3, 0.75))),
    ]


@icon("slide-projector", CAT, "Boxy slide projector with a round carousel tray on top and a front lens",
      tags=["carousel projector", "slides", "35mm", "projector", "presentation", "retro"])
def _(S):
    return [
        shell(ellipse(12, 7, 8, 3.5)),
        dot(12, 7, 1.25),
        shell(rect(2.5, 11.5, 19, 9.5, rr(S))),
        detail(circle(8, 16.25, 2.25)),
        detail(seg(14, 16.25, 18, 16.25)),
    ]


# ============================================================================ audio and controls

@icon("ceiling-speaker", CAT, "Flush speaker set into a ceiling line with sound waves spreading down",
      tags=["in ceiling speaker", "ceiling speaker", "recessed speaker", "pa system", "background music", "audio"])
def _(S):
    return [
        line(seg(2, 3, 5.5, 3)),
        line(seg(18.5, 3, 22, 3)),
        shell("M5.5 3H18.5A6.5 4.5 0 0 1 5.5 3Z" if S.name == "line" else
              "M6.5 2H17.5A1 1 0 0 1 18.5 3A6.5 4.5 0 0 1 5.5 3A1 1 0 0 1 6.5 2Z"),
        line(arc(12, 4, 8, 60, 120)),
        line(arc(12, 4, 12.5, 62, 118)),
        line(arc(12, 4, 17, 64, 116)),
    ]


@icon("motorized-valve", CAT, "Pipe valve with a boxy electric motor actuator mounted on top",
      tags=["motorised valve", "zone valve", "actuator", "heating", "hvac", "plumbing"],
      aliases=["motorised-valve", "zone-valve"])
def _(S):
    return [
        shell(rect(6, 2.5, 12, 7.5, rr(S, 2))),
        dot(9.5, 6.25, 1.25),
        line(seg(12, 10, 12, 12)),
        shell(union(rect(2, 14, 20, 5.5, rr(S, 1)), circle(12, 16.75, 4.75))),
        detail(seg(5, 14, 5, 19.5)),
        detail(seg(19, 14, 19, 19.5)),
    ]


# ============================================================================ home care and mobility

@icon("adjustable-bed", CAT, "Side view of a bed with the head section raised and a remote control",
      tags=["adjustable bed", "electric bed", "power base", "recline", "sleep", "bedroom"])
def _(S):
    return [
        shell(poly([(2.5, 8), (5.5, 6.5), (9.5, 12.5), (21.5, 12.5), (21.5, 16), (8, 16)], closed=True, r=S.r)),
        line(seg(2.5, 19.5, 21.5, 19.5)),
        line(seg(4.5, 19.5, 4.5, 21.5)),
        line(seg(19.5, 19.5, 19.5, 21.5)),
        shell(rect(15.5, 2.5, 4, 6.5, rr(S, 1.5))),
        dot(17.5, 5, 0.9),
    ]


@icon("pour-over-coffee", CAT, "Cone coffee dripper with ribs sitting on top of a carafe with a handle",
      tags=["pour over", "drip coffee", "coffee dripper", "hand brew", "filter coffee", "barista"],
      aliases=["pour-over"])
def _(S):
    cone = poly([(4, 2.5), (18, 2.5), (13.5, 8.5), (8.5, 8.5)], closed=True, r=S.r * 0.6)
    return [
        shell(union(cone, rect(9, 8, 4, 3.5, 0), rect(4.5, 11, 13, 10.5, L(S, 2.5, 4.5)))),
        detail(seg(8.5, 5, 9.75, 8.5)),
        detail(seg(13.5, 5, 12.25, 8.5)),
        detail(seg(9, 8.5, 13, 8.5)),
        line(poly([(17.5, 13), (20.5, 13), (20.5, 18.5), (17.5, 18.5)], r=S.r)),
    ]


@icon("can-crusher", CAT, "Wall-mounted can crusher with a long lever and a flattened can inside",
      tags=["can crusher", "recycling", "aluminium cans", "soda can", "compactor", "garage"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 4, 19, rr(S, 1.5))),
        line(poly([(6.5, 9.5), (17, 9.5), (17, 21.5), (6.5, 21.5)], r=S.r)),
        shell(rect(9, 17, 5.5, 2.5, L(S, 0.3, 1))),
        line(seg(6.5, 5, 21.5, 2.5)),
        line(seg(11.75, 4.2, 11.75, 13)),
        line(seg(9, 13, 14.5, 13)),
    ]


@icon("carpet-sweeper", CAT, "Low flat carpet sweeper on small wheels with a long push handle",
      tags=["carpet sweeper", "floor sweeper", "manual sweeper", "cleaning", "rug", "housework"])
def _(S):
    return [
        shell(union(rect(2.5, 13, 14, 5.5, rr(S, 2)), circle(6, 19.5, 2), circle(13, 19.5, 2))),
        detail(seg(2.5, 18.5, 16.5, 18.5)),
        line(seg(12, 13, 20.5, 3.5)),
        line(seg(18.5, 2, 22, 5)),
    ]


# ============================================================================ batteries

@icon("aa-battery", CAT, "Single upright AA battery with a small top nub and a plus sign",
      tags=["aa", "double a", "battery", "cell", "alkaline", "power"], aliases=["double-a-battery"])
def _(S):
    return [
        solid(rect(10.5, 2, 3, 2.5, L(S, 0, 0.75))),
        shell(rect(7.5, 4.5, 9, 17, rr(S, 2.5))),
        detail(plus(12, 10, 1.75)),
        detail(seg(7.5, 16, 16.5, 16)),
    ]


@icon("nine-volt-battery", CAT, "Rectangular 9 volt battery with a round and a hexagonal snap terminal",
      tags=["9v battery", "9 volt", "pp3", "smoke alarm battery", "battery", "power"], aliases=["9v-battery"])
def _(S):
    return [
        shell(union(rect(4.5, 7.5, 15, 14, rr(S)), circle(8.5, 5.5, 2.5),
                    poly(regular(15.5, 5.5, 2.75, 6, 0), closed=True, r=S.r * 0.3))),
        detail(seg(4.5, 7.5, 19.5, 7.5)),
        detail(plus(12, 14.5, 2)),
    ]


@icon("coin-cell-battery", CAT, "Flat round button cell battery seen at an angle with a plus sign",
      tags=["button cell", "coin battery", "cr2032", "watch battery", "lithium cell", "battery"],
      aliases=["button-cell"])
def _(S):
    rx, ry = 9, 5
    side = (f"M3 10A{rx} {ry} 0 0 1 21 10V13.5A{rx} {ry} 0 0 1 3 13.5Z" if S.name == "line" else
            f"M3 10A{rx} {ry} 0 0 1 21 10V13A1 1 0 0 1 20.8 13.6A{rx} {ry} 0 0 1 3.2 13.6A1 1 0 0 1 3 13Z")
    return [
        shell(side),
        detail(f"M3 10A{rx} {ry} 0 0 0 21 10"),
        detail(plus(12, 9.25, 1.75)),
    ]


# ============================================================================ heaters

@icon("bar-heater", CAT, "Electric bar fire: two glowing heating bars across an arched reflector on feet",
      tags=["electric fire", "bar fire", "radiant heater", "two bar heater", "heating", "warmth"],
      aliases=["electric-fire"])
def _(S):
    return [
        shell("M4 19V10.5A8 7.5 0 0 1 20 10.5V19Z" if S.name == "line" else
              "M4 17V10.5A8 7.5 0 0 1 20 10.5V17A2 2 0 0 1 18 19H6A2 2 0 0 1 4 17Z"),
        detail(seg(4, 11.5, 20, 11.5)),
        detail(seg(4, 15.5, 20, 15.5)),
        line(seg(6.5, 19, 6.5, 21.5)),
        line(seg(17.5, 19, 17.5, 21.5)),
        dot(12, 7, 1.1),
    ]


@icon("parabolic-heater", CAT, "Round dish heater with a central heating element on a tilting stand",
      tags=["dish heater", "radiant heater", "reflector heater", "patio heater", "heating", "infrared"])
def _(S):
    return [
        shell(circle(12, 9, 6)),
        detail(circle(12, 9, 2.25)),
        line(arc(12, 9, 8.75, 0, 180)),
        dot(3.25, 9, 1.25),
        dot(20.75, 9, 1.25),
        line(seg(12, 17.75, 12, 20)),
        shell(rect(7, 20, 10, 1.75, L(S, 0.3, 0.875))),
    ]


# ============================================================================ food service

@icon("meat-slicer", CAT, "Deli meat slicer with a large round blade, a food carriage and a falling slice",
      tags=["deli slicer", "food slicer", "meat slicer", "butcher", "charcuterie", "kitchen"])
def _(S):
    return [
        shell(circle(9.5, 9.5, 7)),
        detail(circle(9.5, 9.5, 2.25)),
        shell(poly([(18.5, 4), (21.5, 4), (21.5, 17), (18.5, 17)], closed=True, r=S.r * 0.6)),
        shell(rect(2.5, 18.5, 19, 3, rr(S, 1.5))),
        line("M3.5 16.5Q5.5 14.5 7.5 16.5" if S.name == "rounded" else "M3.5 16.5L5.5 14.5L7.5 16.5"),
    ]


@icon("hot-dog-roller", CAT, "Hot dog roller grill: sausages resting on a row of rollers under a sneeze guard",
      tags=["roller grill", "hot dog grill", "sausage roller", "concession", "snack bar", "fast food"])
def _(S):
    return [
        line(poly([(2.5, 7), (2.5, 3.5), (21.5, 3.5)], r=S.r)),
        shell(rect(3.5, 8.5, 7.5, 3.5, 1.75)),
        shell(rect(13, 8.5, 7.5, 3.5, 1.75)),
        *[dot(x, 14, 1.1) for x in (4.5, 8.25, 12, 15.75, 19.5)],
        shell(rect(2.5, 16.5, 19, 5, rr(S, 2))),
    ]


@icon("ice-shaver", CAT, "Shaved ice machine with an ice block on top, a side crank and a cup of shaved ice below",
      tags=["shaved ice", "snow cone", "ice crusher", "kakigori", "slush", "dessert"], aliases=["snow-cone-machine"])
def _(S):
    body = union(rect(4, 2.5, 13, 8, rr(S, 2)), rect(4, 2.5, 3.5, 19, rr(S, 1.5)), rect(4, 18, 13, 3.5, rr(S, 1.5)))
    return [
        shell(body),
        detail(rect(9.5, 5, 4.5, 3, L(S, 0, 0.75))),
        shell("M10 18L9 14H16L15 18Z" if S.name == "line" else "M10.2 18L9.2 14.4A0.4 0.4 0 0 1 9.6 14H15.4A0.4 0.4 0 0 1 15.8 14.4L14.8 18Z"),
        line(poly([(17, 6.5), (20.5, 6.5), (20.5, 10)], r=S.r)),
    ]


@icon("baby-bottle-sterilizer", CAT, "Round base with a tall clear dome over two upright baby bottles",
      tags=["bottle steriliser", "sterilizer", "baby bottles", "steam steriliser", "nursery", "feeding"],
      aliases=["bottle-sterilizer", "bottle-steriliser"])
def _(S):
    bottle = lambda x: [hole(rect(x - 1.75, 9.5, 3.5, 6.5, L(S, 0.3, 1))), hole("M%s 9.5L%s 7.5A1.25 1.25 0 0 1 %s 7.5L%s 9.5Z" % (fmt(x - 1.25), fmt(x - 1), fmt(x + 1), fmt(x + 1.25)))]
    return [
        line("M4.5 17V9A7.5 6.5 0 0 1 19.5 9V17"),
        *bottle(9),
        *bottle(15),
        shell(rect(2.5, 17.5, 19, 4, rr(S, 2))),
    ]


# ============================================================================ switches and electrical

@icon("slide-dimmer", CAT, "Wall plate with a vertical slider track and a knob for dimming lights",
      tags=["dimmer", "slide dimmer", "light dimmer", "wall switch", "brightness", "lighting control"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 13, 19, rr(S))),
        detail(seg(12, 6, 12, 18)),
        hole(rect(9.5, 10, 5, 3, L(S, 0.3, 1.5))),
    ]


@icon("outlet-tester", CAT, "Plug-in socket tester in a wall outlet with three indicator lights",
      tags=["socket tester", "receptacle tester", "outlet checker", "wiring test", "electrician", "electrical"],
      aliases=["socket-tester"])
def _(S):
    light = (lambda x: dot(x, 12, 1.1)) if S.name == "rounded" else (lambda x: hole(rect(x - 1, 11, 2, 2)))
    return [
        line(rect(2.5, 2.5, 19, 19, rr(S))),
        shell(rect(5.5, 7.5, 13, 9, rr(S, 2))),
        light(8.75),
        light(12),
        light(15.25),
    ]


@icon("dryer-vent", CAT, "Outside wall vent hood with its flap swung open and air blowing out",
      tags=["dryer vent", "exhaust vent", "wall vent", "tumble dryer", "vent hood", "laundry"])
def _(S):
    return [
        shell(rect(3, 2.5, 3.5, 19, rr(S, 1))),
        shell(poly([(6.5, 5.5), (13.5, 8.5), (13.5, 16), (6.5, 16)], closed=True, r=S.r * 0.6)),
        line(seg(13.5, 8.5, 19, 14)),
        line("M9 19.5Q12.5 17.5 16 19.5Q18.5 21 21.5 19.5"),
    ]


@icon("home-control-panel", CAT, "Wall-mounted touchscreen home control panel with four room tiles",
      tags=["smart home panel", "home hub", "control panel", "touchscreen", "home automation", "wall tablet"],
      aliases=["smart-home-panel"])
def _(S):
    tile = lambda x, y: hole(rect(x, y, 4.5, 4, L(S, 0.3, 1.25)))
    return [
        shell(rect(3, 3, 18, 18, rr(S))),
        detail(seg(6.5, 6.5, 11, 6.5)),
        tile(6.5, 9.5), tile(13, 9.5), tile(6.5, 15), tile(13, 15),
    ]


# ============================================================================ household

@icon("shoe-polisher", CAT, "Shoe shine machine: a low box with two round brushes and a shoe above",
      tags=["shoe shine", "shoe polisher", "shoe buffer", "brush", "footwear care", "hotel"],
      aliases=["shoe-shine-machine"])
def _(S):
    return [
        shell(poly([(4, 9.5), (4, 4.5), (8.5, 4.5), (11, 7), (18, 7.5), (20, 9.5)], closed=True, r=S.r)),
        shell(rect(2.5, 12.5, 19, 9, rr(S))),
        detail(circle(7.5, 17, 2.25)),
        detail(circle(16.5, 17, 2.25)),
    ]


@icon("faucet-water-filter", CAT, "Kitchen tap with a small cylindrical water filter clipped onto the spout",
      tags=["tap filter", "faucet filter", "water filter", "drinking water", "purifier", "kitchen"],
      aliases=["tap-water-filter"])
def _(S):
    return [
        shell(union(_pipe("M6.5 19V8.5Q6.5 5 10 5H14", 3.5), rect(2.5, 19, 8, 2.5, rr(S, 1)))),
        shell(rect(14, 2.5, 6.5, 9.5, rr(S, 2))),
        detail(seg(14, 6.5, 20.5, 6.5)),
        solid(drop(17.25, 17.25, 5)),
    ]


@icon("pellet-stove", CAT, "Pellet stove with a hopper lid on top, a flame window and a flue pipe",
      tags=["pellet stove", "wood pellet", "biomass stove", "heating", "fireplace", "stove"])
def _(S):
    flame = "M10 16.75C8.5 16.75 8.3 15 9.25 13.75C9.4 14.6 9.9 14.8 10.2 14.6C10 13.5 10.4 12.8 11 12.25C11 13.5 12 14 12 15.25C12 16.25 11.2 16.75 10 16.75Z"
    return [
        shell(rot(rect(3.5, 3.5, 12, 2, L(S, 0.3, 1)), -8, 3.5, 5.5)),
        shell(rect(3.5, 7.5, 13, 14, rr(S))),
        detail(rect(6.5, 10.5, 7, 7.5, L(S, 0, 1.5))),
        hole(mv(flame, 0, 0)),
        line(poly([(16.5, 17), (20, 17), (20, 2.5)], r=S.r)),
    ]


@icon("window-fan", CAT, "Twin window fan: two round fans in a slim frame set into a window",
      tags=["window fan", "twin fan", "box fan", "ventilation", "cooling", "exhaust fan"])
def _(S):
    return [
        line(poly([(2.5, 10), (2.5, 2.5), (21.5, 2.5), (21.5, 10)], r=S.r)),
        line(seg(2.5, 6.5, 21.5, 6.5)),
        shell(rect(2, 10.5, 20, 10, rr(S, 2))),
        detail(circle(7.25, 15.5, 2.75)),
        detail(circle(16.75, 15.5, 2.75)),
    ]
