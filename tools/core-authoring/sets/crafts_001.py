"""TypeIcon Core: crafts (batch crafts_001): painting and drawing supplies, printmaking, bookbinding,
sculpture, pottery and knitting tools.

Long hand tools (brushes, markers, carving tools) are drawn upright and turned 45 degrees clockwise so the
handle points to the bottom-left and the working end to the top-right, matching the tools set. Pens that
are shown drawing point to the bottom-left instead, with the line they drew. Containers and pottery are
drawn in side view.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path.parser import parse_path
from geometry import SCALE, D, I, P, ST, U, fmt, path_to_d, rotation

CAT = "crafts"
TILT = 45


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


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


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def grow(d, g):
    """Region d expanded by g px (to cut clean gaps where one part passes behind another)."""
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def thick(d, w, cap="butt", join="miter"):
    """Closed outline of a stroke of width w along d."""
    return path_to_d(ST(d, w, cap, join))


def hole(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def bounds(parts):
    regions = []
    for p in parts:
        regions.append(P(p.d) if p.kind in ("shell", "dot", "solid") else ST(p.d, 2.0))
    x0, y0, x1, y1 = U(*regions).bounds
    return x0 / SCALE, y0 / SCALE, x1 / SCALE, y1 / SCALE


def fit(parts, cx=12.0, cy=12.0):
    """Translate parts so their drawn bounds are centred on (cx, cy), snapped to half pixels."""
    x0, y0, x1, y1 = bounds(parts)
    dx = round((cx - (x0 + x1) / 2) * 2) / 2
    dy = round((cy - (y0 + y1) / 2) * 2) / 2
    if dx == 0 and dy == 0:
        return parts
    return [Part(p.kind, mv(p.d, dx, dy), p.attrs) for p in parts]


def turn(parts, deg=TILT, cx=12.0, cy=12.0):
    return [Part(p.kind, rot(p.d, deg, cx, cy), p.attrs) for p in parts]


def tilt(parts, deg=TILT):
    """Turn an upright tool (handle down) so the handle points to the bottom-left, then centre it."""
    return fit(turn(parts, deg))


def rbox(S, x, y, w, h, cap=None):
    return rect(x, y, w, h, rr(S, cap))


def leaf_at(base, ang, length, w):
    """Pointed leaf (brush tip, flame) starting at base and pointing along ang (degrees, 0 = right, -90 = up)."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    bx, by = base
    tx, ty = bx + ux * length, by + uy * length
    k = w * 0.75
    c1 = (bx + ux * length * 0.3 + nx * k, by + uy * length * 0.3 + ny * k)
    c2 = (bx + ux * length * 0.75 + nx * k * 0.6, by + uy * length * 0.75 + ny * k * 0.6)
    c3 = (bx + ux * length * 0.75 - nx * k * 0.6, by + uy * length * 0.75 - ny * k * 0.6)
    c4 = (bx + ux * length * 0.3 - nx * k, by + uy * length * 0.3 - ny * k)

    def p(q):
        return f"{fmt(q[0])} {fmt(q[1])}"
    return f"M{p(base)}C{p(c1)} {p(c2)} {p((tx, ty))}C{p(c3)} {p(c4)} {p(base)}Z"


def along(p, ang, dist):
    a = math.radians(ang)
    return (p[0] + math.cos(a) * dist, p[1] + math.sin(a) * dist)


def rot_pt(p, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    x, y = p[0] - cx, p[1] - cy
    return cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)


def shift_to(parts, src, dst):
    """Translate parts so the point src lands on dst."""
    return [Part(p.kind, mv(p.d, dst[0] - src[0], dst[1] - src[1]), p.attrs) for p in parts]


def smooth(pts, t=0.5):
    """Closed Catmull-Rom curve through pts."""
    n = len(pts)
    out = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        out += f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}"
    return out + "Z"


def drop_d(cx, top, bottom, w):
    """Water-drop shape: pointed top, round bottom."""
    r = w / 2
    cy = bottom - r
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx)} {fmt(top)} {fmt(cx + r)} {fmt(cy - r * 0.9)} {fmt(cx + r)} {fmt(cy)}"
            f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx - r)} {fmt(cy)}C{fmt(cx - r)} {fmt(cy - r * 0.9)} {fmt(cx)} {fmt(top)} {fmt(cx)} {fmt(top)}Z")

# ============================================================================ paints, brushes and canvases

@icon("paint-tube", CAT, "Paint tube with a crimped flat end and a blob of paint squeezed from the nozzle",
      tags=["oil paint", "acrylic paint", "gouache", "artist paint", "tube", "painting"])
def _(S):
    body = poly([(8, 18), (16, 18), (16, 10.5), (13.5, 8), (10.5, 8), (8, 10.5)], closed=True, r=S.r)
    crimp = rect(7, 18, 10, 3, rr(S, 0.5))
    neck = rect(10.5, 5.5, 3, 2.5)
    blob = "M12 1.3C13.8 1.3 14.6 2.6 14.2 3.8C14 4.6 13.2 5.2 12 5.2C10.8 5.2 10 4.6 9.8 3.8C9.4 2.6 10.2 1.3 12 1.3Z"
    return tilt([shell(union(body, crimp, neck)), detail(seg(8, 18, 16, 18)), detail(seg(10.5, 8, 13.5, 8)),
                 solid(blob)])


@icon("acrylic-paint-bottle", CAT, "Short squeeze bottle of craft paint with a pointed flip-top spout and a label band",
      tags=["acrylic paint", "craft paint", "squeeze bottle", "paint bottle", "poster paint", "painting"])
def _(S):
    body = rbox(S, 6, 10.5, 12, 10.5, 3)
    cap = rect(8.5, 6.5, 7, 4)
    spout = poly([(11, 6.5), (13, 6.5), (12.5, 3), (11.5, 3)], closed=True)
    return [shell(union(body, cap, spout)), detail(seg(8.5, 10.5, 15.5, 10.5)),
            detail(seg(6, 14, 18, 14)), detail(seg(6, 18, 18, 18))]


@icon("watercolor-palette", CAT, "Open watercolour tin with two rows of paint pans and a brush lying above it",
      tags=["watercolour", "paint set", "paint pans", "paint box", "painting", "art supplies"],
      aliases=["watercolour-palette"])
def _(S):
    tin = rbox(S, 2.5, 9.5, 19, 11.5, 2)
    k = L(S, 0, 0.8)
    pans = [hole(rect(x, y, 3, 2.25, k)) for y in (12, 16.25) for x in (5.5, 10.5, 15.5)]
    brush = [line(seg(2.5, 5, 12, 5)), solid(rect(11.5, 3.5, 3, 3, L(S, 0, 0.5))), solid(leaf_at((14.2, 5), 0, 7, 3.2))]
    return [shell(tin)] + pans + brush


@icon("palette-knife", CAT, "Painting knife with a cranked neck and a flat rounded blade",
      tags=["painting knife", "spatula", "impasto", "oil painting", "mixing paint", "art tool"])
def _(S):
    if S.name == "line":
        blade = "M9 10.5C5.3 9.3 5 5.2 9 1.8C13 5.2 12.7 9.3 9 10.5Z"
    else:
        blade = "M9 10.5C5.5 9.5 5 6.5 6.4 4.3C7.3 2.9 8.2 2.2 9 2.2C9.8 2.2 10.7 2.9 11.6 4.3C13 6.5 12.5 9.5 9 10.5Z"
    return tilt([shell(blade), line(poly([(9, 10.5), (9, 12), (12, 14), (12, 15.5)], r=S.r * 0.8)),
                 shell(rect(10.25, 15.5, 3.5, 6.5, rr(S, 1.75)))])


@icon("flat-brush", CAT, "Flat paintbrush with a wide metal ferrule and square-cut bristles",
      tags=["paintbrush", "flat paintbrush", "shader brush", "painting", "artist brush", "brush"])
def _(S):
    bristles = poly([(9, 9), (7.5, 4), (8.5, 2.5), (15.5, 2.5), (16.5, 4), (15, 9)], closed=True, r=S.r * 0.5)
    ferrule = rect(9, 9, 6, 4.5)
    return tilt([shell(union(bristles, ferrule)), detail(seg(9, 9, 15, 9)), line(seg(12, 13.5, 12, 22))])


def _brush(base, ang, handle, S):
    end = along(base, ang, handle)
    return [line(seg(base[0], base[1], end[0], end[1])), solid(leaf_at(along(end, ang, -0.3), ang, L(S, 4.2, 4), 3))]


@icon("brush-jar", CAT, "Straight-sided glass jar holding three paintbrushes standing at different heights",
      tags=["brush holder", "brush pot", "rinse jar", "paintbrushes", "painting", "art studio"])
def _(S):
    jar = rbox(S, 5, 11, 14, 10, 3)
    return ([shell(jar), detail(seg(5, 15, 19, 15))] + _brush((9.5, 10), -118, 3.5, S)
            + _brush((12, 10), -90, 4, S) + _brush((14.5, 10), -62, 2.5, S))


@icon("stretched-canvas", CAT, "Blank stretched canvas seen at an angle, showing the depth of its frame",
      tags=["canvas", "painting canvas", "blank canvas", "stretcher frame", "artist canvas", "painting"])
def _(S):
    face = poly([(8, 3), (21, 5.5), (21, 18.5), (8, 21)], closed=True, r=S.r * 0.6)
    side = poly([(3.5, 5.5), (8, 3), (8, 21), (3.5, 18.5)], closed=True, r=S.r * 0.6)
    return [shell(union(face, side)), detail(seg(8, 3, 8, 21)), dot(5.75, 8, 0.9), dot(5.75, 12, 0.9),
            dot(5.75, 16, 0.9)]


@icon("drawing-board", CAT, "Drawing board tilted on a stand with a clip holding the paper at the top",
      tags=["drafting board", "sketch board", "drawing table", "clip", "sketching", "art"])
def _(S):
    board = poly([(6, 4), (18, 4), (20.5, 16.5), (3.5, 16.5)], closed=True, r=S.r)
    return [shell(board), solid(rect(9, 2.5, 6, 3, L(S, 0, 1))), detail("M8.5 12.5C10 9.5 12 13.5 15.5 9.5"),
            line(seg(8, 16.5, 6.5, 21.5)), line(seg(16, 16.5, 17.5, 21.5))]


def _stick(p0, p1, w):
    a = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    nx, ny = -math.sin(a) * w / 2, math.cos(a) * w / 2
    ux, uy = math.cos(a) * 0.8, math.sin(a) * 0.8
    return [(p0[0] + nx, p0[1] + ny), (p1[0] + nx - ux, p1[1] + ny - uy), (p1[0] - nx + ux, p1[1] - ny + uy),
            (p0[0] - nx + ux * 0.6, p0[1] - ny + uy * 0.6)]


@icon("charcoal-stick", CAT, "Two sticks of willow charcoal lying side by side above a smudged mark",
      tags=["charcoal", "willow charcoal", "vine charcoal", "sketching", "drawing", "art supplies"])
def _(S):
    a = poly(_stick((3.5, 11), (13.5, 3), 3.2), closed=True, r=S.r * 0.5)
    b = poly(_stick((8.5, 15), (19, 6.5), 3.2), closed=True, r=S.r * 0.5)
    return fit([shell(b, stroke_miterlimit="2"), shell(a, stroke_miterlimit="2"),
                line("M4 20C7 18.5 9 21.5 12 20S17 18.5 20 20")])


@icon("chalk-pastels", CAT, "Open tray of chalk pastel sticks of different lengths",
      tags=["soft pastels", "chalk pastels", "pastel sticks", "drawing", "art supplies", "colours"])
def _(S):
    tray = rbox(S, 3, 13.5, 18, 7.5, 2)
    sticks = []
    for x, top, ang in ((6.5, 4.5, -12), (12, 3, 0), (17.5, 5.5, 12)):
        st = rot(rect(x - 1.75, top, 3.5, 14 - top, L(S, 0, 1)), ang, x, 14)
        sticks.append(solid(minus(st, grow(tray, 1.5))))
    return [shell(tray), detail(seg(3, 17, 21, 17))] + sticks


@icon("blending-stump", CAT, "Paper blending stump tapered to a point at both ends with a spiral seam",
      tags=["tortillon", "stump", "blender", "smudge tool", "shading", "drawing"], aliases=["tortillon"])
def _(S):
    body = poly([(12, 2), (14.5, 7.5), (14.5, 16.5), (12, 22), (9.5, 16.5), (9.5, 7.5)], closed=True, r=S.r)
    return tilt([shell(body), detail(seg(9.5, 11, 14.5, 8.5)), detail(seg(9.5, 15.5, 14.5, 13))])


@icon("kneaded-eraser", CAT, "Soft squashed lump of kneaded eraser with a thumb dent and a stretched corner",
      tags=["putty eraser", "art eraser", "rubber", "erase", "charcoal", "drawing"], aliases=["putty-eraser"])
def _(S):
    pts = [(3.5, 15.5), (5, 10.5), (9, 9), (12, 11.5), (15, 9), (18, 7.5), (21.5, 5.5), (21, 11), (19, 17), (13, 19.5), (7.5, 19)]
    return [shell(smooth(pts, L(S, 0.45, 1))), detail("M7 14.5C8.2 15.8 9.5 16.2 10.8 16")]


@icon("art-marker", CAT, "Chunky art marker with a slanted chisel nib and a capped end",
      tags=["alcohol marker", "chisel marker", "felt pen", "illustration", "colouring", "drawing"])
def _(S):
    nib = poly([(10.5, 7), (13.5, 7), (13.5, 3), (10.5, 5)], closed=True, r=S.r * 0.4)
    body = rect(8.5, 7, 7, 9.5, rr(S, 1))
    cap = rect(8, 16.5, 8, 5, rr(S, 1.5))
    return tilt([shell(union(nib, body, cap)), detail(seg(8.5, 16.5, 15.5, 16.5)), detail(seg(10.5, 7, 13.5, 7))])


@icon("fineliner", CAT, "Slim fineliner pen with a needle-point tip drawing a thin straight line",
      tags=["fine liner", "drawing pen", "ink pen", "fine tip pen", "line art", "drawing"],
      aliases=["fine-liner"])
def _(S):
    body = rect(10, 9, 4, 12.5, rr(S, 1.5))
    parts = [shell(body), solid(poly([(10.6, 9), (13.4, 9), (12, 2.5)], closed=True)), detail(seg(10, 12.5, 14, 12.5))]
    parts = [Part(p.kind, rot(p.d, 225), p.attrs) for p in parts]
    tipp = rot_pt((12, 2.5), 225)
    parts = shift_to(parts, tipp, (7, 19))
    return parts + [line(seg(2.5, 19, 7, 19))]


@icon("technical-pen", CAT, "Technical drafting pen with a knurled grip and a tube nib resting on a ruled line",
      tags=["drafting pen", "ink drafting", "technical drawing", "draughting", "ink pen", "precision"])
def _(S):
    return [shell(rect(8.5, 2, 7, 12, rr(S, 1.5))), detail(seg(8.5, 7, 15.5, 7)), detail(seg(8.5, 10, 15.5, 10)),
            shell(rect(10.5, 14, 3, 3.5)), line(seg(12, 17.5, 12, 20.5)), line(seg(2.5, 21.5, 21.5, 21.5))]


@icon("airbrush", CAT, "Pen-shaped airbrush with a paint cup on top, a trigger button, a hose and a fine spray",
      tags=["spray gun", "air brush", "compressor", "spray paint", "illustration", "model painting"])
def _(S):
    body = poly([(6, 11), (14, 11), (17, 12), (17, 14), (14, 15), (6, 15)], closed=True, r=S.r)
    cup = poly([(8, 6), (12, 6), (11, 11), (9, 11)], closed=True, r=S.r * 0.4)
    return [shell(body), shell(cup), line(seg(14.5, 8, 14.5, 11)), solid(rect(13.3, 6.5, 2.4, 1.6, L(S, 0, 0.6))),
            line(seg(17, 13, 19, 13)), dot(21, 11, 0.9), dot(21.5, 13.5, 0.9), dot(20.5, 16, 0.9),
            line("M6 13H4.5C2.5 13 2.5 17 4 20")]


# ============================================================================ studio, drawing and painting techniques

@icon("artist-mannequin", CAT, "Jointed wooden drawing mannequin standing on a base",
      tags=["drawing mannequin", "lay figure", "art model", "wooden figure", "pose reference", "figure drawing"],
      aliases=["lay-figure"])
def _(S):
    torso = poly([(9.5, 8), (14.5, 8), (13.5, 14), (10.5, 14)], closed=True, r=S.r * 0.6)
    return [shell(ellipse(12, 4.3, 1.9, 2.3)), shell(torso),
            line(poly([(9, 9), (6, 12.5), (5.5, 16.5)], r=S.r)), line(poly([(15, 9), (18, 12.5), (18.5, 16.5)], r=S.r)),
            line(poly([(11, 14.5), (10.5, 18), (10, 21)], r=S.r)), line(poly([(13, 14.5), (13.5, 18), (14, 21)], r=S.r)),
            line(seg(7, 21.5, 17, 21.5)),
            dot(6, 12.5, 1.5), dot(18, 12.5, 1.5)]


@icon("hand-model", CAT, "Wooden jointed model hand with segmented fingers standing on a small square base",
      tags=["artist hand", "wooden hand", "drawing hand", "hand reference", "pose model", "figure drawing"],
      aliases=["wooden-hand"])
def _(S):
    palm = poly([(5.5, 11.5), (18.5, 11.5), (17, 17.5), (7, 17.5)], closed=True, r=S.r * 0.6)
    parts = [shell(palm), line(seg(12, 17.5, 12, 19.5)), shell(rect(8, 19.5, 8, 2, L(S, 0, 0.8)))]
    for x, top in ((7.3, 6.5), (10.4, 4.5), (13.6, 5), (16.7, 7)):
        parts += [line(seg(x, 11.5, x, top)), dot(x, (11.5 + top) / 2 + 0.5, 1.3)]
    parts += [line(seg(5.5, 14, 2.5, 10.5))]
    return parts


@icon("still-life", CAT, "Still life arrangement of a bottle, an apple and a pear on a table",
      tags=["still life", "art class", "arrangement", "fruit", "bottle", "drawing subject", "painting"])
def _(S):
    bottle = poly([(5.5, 3), (8, 3), (8, 7), (10.5, 9.5), (10.5, 19.5), (3, 19.5), (3, 9.5), (5.5, 7)],
                  closed=True, r=S.r)
    apple = ("M11 13.3C9 12.5 7.5 14 7.5 16.3C7.5 18.5 9 19.5 10.3 19.5C10.8 19.5 11 19.3 11 19.3"
             "C11 19.3 11.2 19.5 11.7 19.5C13 19.5 14.5 18.5 14.5 16.3C14.5 14 13 12.5 11 13.3Z")
    pear = ("M19 10.5C17.8 10.5 17.5 12 17.3 13.3C17.1 14.8 16 15.5 16 17.3C16 19 17 19.5 19 19.5"
            "C21 19.5 22 19 22 17.3C22 15.5 20.9 14.8 20.7 13.3C20.5 12 20.2 10.5 19 10.5Z")
    bottle = minus(bottle, grow(apple, 3))
    return [shell(bottle), shell(apple), shell(pear), line(seg(11, 13.3, 12, 11.3)), line(seg(2, 21.5, 22, 21.5))]


@icon("paint-splatter", CAT, "Irregular splash of paint with droplets flung around it",
      tags=["splash", "splat", "paint splash", "ink blot", "spill", "mess", "art"], aliases=["paint-splash"])
def _(S):
    spec = [(-100, 7.5), (-75, 4.2), (-45, 5.8), (-20, 4), (5, 7.8), (30, 4.3), (60, 5.5), (95, 4.2), (125, 7),
            (150, 4), (180, 5.2), (210, 4.4), (235, 6.8), (255, 4.2)]
    pts = [pt_on(11.5, 12, r, a) for a, r in spec]
    return [shell(smooth(pts, L(S, 0.6, 1.0))), dot(20.5, 3.5, 1.3), dot(3, 20.5, 1.2), dot(21, 18, 1), dot(2.8, 7, 0.9)]


@icon("paint-drip", CAT, "Band of wet paint running down in rounded drips of different lengths",
      tags=["dripping paint", "wet paint", "drip", "runny paint", "paint run", "melting"])
def _(S):
    band = rect(3, 3, 18, 5, rr(S, 1.5))
    drips = [rect(x - 1.75, 5, 3.5, bottom - 5, 1.75) for x, bottom in ((6.5, 16.5), (12, 12), (17.5, 20.5))]
    return [shell(union(band, *drips))]


def _bez(p, t):
    u = 1 - t
    return (u ** 3 * p[0][0] + 3 * u * u * t * p[1][0] + 3 * u * t * t * p[2][0] + t ** 3 * p[3][0],
            u ** 3 * p[0][1] + 3 * u * u * t * p[1][1] + 3 * u * t * t * p[2][1] + t ** 3 * p[3][1])


def _offset(p, t, off):
    x, y = _bez(p, t)
    x2, y2 = _bez(p, min(1, t + 1e-3))
    x1, y1 = _bez(p, max(0, t - 1e-3))
    dx, dy = x2 - x1, y2 - y1
    ln = math.hypot(dx, dy)
    return x - dy / ln * off, y + dx / ln * off


@icon("brush-stroke", CAT, "Single sweeping paint stroke that is thick at one end and breaks into dry bristle streaks at the other",
      tags=["paint stroke", "dry brush", "brushstroke", "swoosh", "texture", "painting"], aliases=["brushstroke"])
def _(S):
    c = [(3.5, 16.5), (6, 8), (12, 19), (20.5, 8)]
    cut = 0.5
    n = 14
    left = [_offset(c, cut * i / n, -3.3 + 0.3 * i / n) for i in range(n + 1)]
    right = [_offset(c, cut * i / n, 3.3 - 0.3 * i / n) for i in range(n + 1)]
    body = poly(left + right[::-1], closed=True, r=S.r * 0.8)
    parts = [shell(body)]
    for off, end in ((-2.9, 0.95), (0, 1.0), (2.9, 0.82)):
        pts = [_offset(c, cut + (end - cut) * i / 8, off) for i in range(9)]
        parts.append(line(poly(pts)))
    return fit(parts)


@icon("color-mixing", CAT, "Two overlapping blobs of paint with the blended colour where they meet",
      tags=["colour mixing", "blend", "mix paint", "colour theory", "painting", "palette"],
      aliases=["colour-mixing"])
def _(S):
    if S.name == "line":
        a, b = circle(8.5, 12, 6.5), circle(15.5, 12, 6.5)
    else:
        a = rot(ellipse(9, 12, 5.8, 7), 25, 9, 12)
        b = rot(ellipse(15, 12, 5.8, 7), -25, 15, 12)
    lens = path_to_d(I(P(a), P(b)))
    return [shell(a), shell(b), solid(lens)]


@icon("art-portfolio", CAT, "Large flat zip-around art portfolio case with a carry handle",
      tags=["portfolio case", "artwork folder", "art case", "drawing folder", "carry case", "art school"])
def _(S):
    return [line(poly([(9, 7), (9, 3.5), (15, 3.5), (15, 7)], r=S.r)), shell(rbox(S, 2.5, 7, 19, 14, 2)),
            detail(rect(6.5, 11, 11, 6, L(S, 0, 1.5)))]


@icon("proportional-divider", CAT, "Proportional divider: two long arms crossing at a sliding pivot screw",
      tags=["proportional dividers", "scaling tool", "reduction compass", "drafting", "measure", "enlarge"])
def _(S):
    pv = (12, 9.5)
    ux, uy = 3 / 7.1, 6.5 / 7.1  # direction of arm A (down-right)
    def end(dx, dy, t):
        return pv[0] + dx * t, pv[1] + dy * t
    ta = (9, 3)
    ba = (17.5, 21.5)
    tb = (15, 3)
    bb = (6.5, 21.5)
    parts = [line(seg(*ta, *end(-ux, -uy, 2.6))), line(seg(*end(ux, uy, 2.6), *ba)),
             line(seg(*tb, *end(ux, -uy, 2.6))), line(seg(*end(-ux, uy, 2.6), *bb)),
             shell(circle(pv[0], pv[1], 2.2)), dot(pv[0], pv[1], 0.6)]
    return parts


@icon("maulstick", CAT, "Maulstick with a padded ball end resting against the edge of a canvas",
      tags=["mahlstick", "mahl stick", "hand rest", "painting support", "sign painting", "artist tool"],
      aliases=["mahlstick"])
def _(S):
    canvas = rbox(S, 3, 6, 11, 15, 1.5)
    ball = circle(16.5, 5.5, 2.5)
    return [shell(canvas), shell(ball), line(seg(17.8, 7.8, 21.5, 21.5))]


@icon("gold-leaf", CAT, "Open booklet of gold leaf with a crinkled sheet and a soft brush lifting its corner",
      tags=["gilding", "leaf booklet", "metal leaf", "gilder's brush", "decorating", "craft"],
      aliases=["gilding"])
def _(S):
    return [shell(rbox(S, 2.5, 9, 19, 12, 2)), detail(seg(12, 9, 12, 21)),
            hole(poly([(14.5, 12.5), (17, 12.5), (19, 14.5), (19, 18), (14.5, 18)], closed=True)),
            line(seg(21.5, 2.5, 18.7, 6.2)), solid(leaf_at((18.9, 6), 130, 4, 3))]


@icon("perspective-drawing", CAT, "Box drawn in two-point perspective below a horizon line with a vanishing point at each end",
      tags=["two point perspective", "vanishing point", "horizon line", "drawing technique", "3d drawing", "sketching"])
def _(S):
    box = poly([(6, 10.5), (12, 8.5), (18, 10.5), (18, 18), (12, 21), (6, 18)], closed=True, r=S.r * 0.5)
    return [shell(box), detail(poly([(6, 10.5), (12, 12.5), (18, 10.5)])), detail(seg(12, 12.5, 12, 21)),
            line(seg(4.5, 3.5, 19.5, 3.5)), dot(3, 3.5, 1.6), dot(21, 3.5, 1.6)]


@icon("cameo-portrait", CAT, "Oval cameo brooch framing a woman's profile with her hair in a bun",
      tags=["cameo", "brooch", "profile portrait", "silhouette", "jewellery", "victorian"], aliases=["cameo"])
def _(S):
    head = poly([(10.5, 15), (9.8, 11.5), (10.3, 8), (12.3, 6.6), (14.3, 7.6), (14.9, 9.4), (16, 11), (15, 11.5),
                 (15.2, 12.3), (14.6, 13.4), (13.6, 13.6), (13.6, 15), (15, 17.3), (9.5, 17.3)], closed=True, r=S.r * 0.5)
    bun = circle(9.4, 8.2, 1.7)
    return [shell(ellipse(12, 12, 7.5, 9)), hole(union(head, bun))]


@icon("graffiti-wall", CAT, "Brick wall with a bold sprayed graffiti tag and a paint drip",
      tags=["graffiti", "street art", "tag", "spray paint", "mural", "brick wall"])
def _(S):
    tag = thick("M5.5 8C7 5 9 5.5 9.5 7.5C10 9.5 12 10 13 7.5C14 5 16.5 5.3 18.5 7.5", 3, "round", "round")
    drip = rect(11.3, 7.5, 2.4, 5, 1.2)
    return [shell(rect(2.5, 3, 19, 18, L(S, 2, 4))), hole(union(tag, drip)),
            detail(seg(2.5, 14.5, 21.5, 14.5)), detail(seg(2.5, 18.5, 21.5, 18.5)),
            detail(seg(12, 14.5, 12, 18.5)), detail(seg(7.5, 18.5, 7.5, 21)), detail(seg(16.5, 18.5, 16.5, 21))]


@icon("art-supplies", CAT, "Pencil and paintbrush crossed over each other",
      tags=["art materials", "drawing and painting", "art class", "creative", "stationery", "crafts"],
      aliases=["art-materials"])
def _(S):
    pencil = union(rect(10.5, 7, 3, 13, rr(S, 0.5)), poly([(10.5, 7), (13.5, 7), (12, 3)], closed=True))
    pencil_parts = turn([shell(pencil), detail(seg(10.5, 7, 13.5, 7)), detail(seg(10.5, 17.5, 13.5, 17.5))], 45)
    brush = turn([solid(leaf_at((12, 11.3), -90, 8.3, 3.4)), solid(rect(10.8, 9, 2.4, 3, 0.3))], -45)
    cut = grow(pencil_parts[0].d, 3)
    back = [Part(p.kind, minus(p.d, cut), p.attrs) for p in brush]
    back.append(line(seg(*rot_pt((12, 21.5), -45), *rot_pt((12, 17.3), -45))))
    return back + pencil_parts


# ============================================================================ ink, calligraphy and printmaking

@icon("ink-stick", CAT, "Block of solid ink with a raised panel, its worn end resting on an inkstone",
      tags=["sumi ink", "inkstick", "ink block", "inkstone", "calligraphy", "ink painting"],
      aliases=["inkstick"])
def _(S):
    block = poly([(9.5, 3), (14.5, 3), (14.5, 14), (9.5, 15.5)], closed=True, r=S.r * 0.6)
    stick = turn([shell(block), hole(rect(11, 6, 2, 5.5, L(S, 0, 1)))], 30, 12, 15)
    stone = rbox(S, 2.5, 16.5, 19, 5, 1.5)
    return [Part(p.kind, mv(p.d, 1, -1), p.attrs) for p in stick] + [shell(stone), detail(seg(6, 19, 10, 19))]


@icon("brush-rest", CAT, "Low three-peaked brush rest with a paintbrush lying across its tops",
      tags=["brush holder", "pen rest", "calligraphy", "ink painting", "desk", "painting"])
def _(S):
    rest = poly([(2.5, 20), (2.5, 17.5), (5.5, 11.5), (8.75, 16), (12, 11.5), (15.25, 16), (18.5, 11.5), (21.5, 17.5),
                 (21.5, 20)], closed=True, r=S.r)
    return [shell(rest), line(seg(2.5, 9.5, 13, 9.5)), solid(rect(12.5, 8, 2.5, 3, L(S, 0, 0.5))),
            solid(leaf_at((14.8, 9.5), 0, 6.8, 3))]


@icon("oblique-pen-holder", CAT, "Oblique calligraphy pen holder with a side flange holding the nib off centre",
      tags=["oblique holder", "calligraphy pen", "copperplate", "dip pen", "nib holder", "lettering"])
def _(S):
    handle = rect(10.5, 10, 3, 11.5, L(S, 0.5, 1.5))
    return tilt([shell(handle), line(poly([(12, 10), (12, 8.5), (15.5, 6.3)], r=S.r * 0.6)),
                 solid(poly([(14.4, 7.2), (16.6, 7.2), (16.6, 4), (15.5, 1.3), (14.4, 4)], closed=True))])


@icon("ink-bottle", CAT, "Small square ink bottle with a round screw cap, the ink level showing, and a drop beside it",
      tags=["inkwell", "ink pot", "fountain pen ink", "calligraphy ink", "drawing ink", "writing"],
      aliases=["ink-pot"])
def _(S):
    bottle = union(rbox(S, 3, 10, 12.5, 11, 2), rect(6, 8, 6.5, 2.5))
    cap = rect(5.5, 3.5, 7.5, 4.5, rr(S, 1))
    drop = "M19 11C19 11 21.8 14.6 21.8 16.5C21.8 18.1 20.5 19.3 19 19.3C17.5 19.3 16.2 18.1 16.2 16.5C16.2 14.6 19 11 19 11Z"
    return [shell(bottle), shell(cap), detail(seg(3, 14.5, 15.5, 14.5)), shell(drop)]


@icon("sealing-wax", CAT, "Stick of sealing wax melting a drip of wax onto a round wax seal",
      tags=["wax seal", "sealing stick", "letter seal", "envelope", "stationery", "calligraphy"])
def _(S):
    stick = thick(seg(21, 3.5, 12, 8), 4)
    seal = poly([pt_on(10, 18.8, 3.9 if i % 2 == 0 else 3.4, i * 25.714) for i in range(14)], closed=True, r=L(S, 0.3, 1.1))
    return [shell(stick), solid(drop_d(10.5, 10.5, 14, 2.6)), shell(seal)]


@icon("illuminated-letter", CAT, "Square panel with a large decorated capital A and leafy flourishes",
      tags=["drop cap", "illuminated manuscript", "initial", "decorated letter", "calligraphy", "medieval"],
      aliases=["drop-cap"])
def _(S):
    return [shell(rbox(S, 3, 3, 18, 18, 2)), detail(poly([(7.5, 17.5), (12, 6.5), (16.5, 17.5)], r=S.r * 0.5)),
            detail(seg(9.3, 13.5, 14.7, 13.5)), hole(leaf_at((5.5, 7.5), -60, 3, 2)), hole(leaf_at((18.5, 16.5), 120, 3, 2)),
            hole(leaf_at((18.5, 7.5), -120, 3, 2)), hole(leaf_at((5.5, 16.5), 60, 3, 2))]


@icon("calligraphy-flourish", CAT, "Looping calligraphic pen flourish with two ovals and a trailing tail",
      tags=["flourish", "swash", "lettering", "penmanship", "ornament", "calligraphy"], aliases=["swash"])
def _(S):
    d = ("M3 18.5C7 18.5 10 14 9.5 9C9.1 5 5 5 5.2 8.5C5.5 13 11 15 13.5 12C15.5 9.5 16.5 5 19 5"
         "C21.5 5 21 9.5 18 12C15.5 14 13.5 17.5 16 19C17.5 20 19.5 19.5 21.5 18")
    end = circle(3, 18.5, 1.6) if S.name == "rounded" else rect(1.6, 17.1, 2.8, 2.8)
    return [line(d), solid(end)]


@icon("linocut", CAT, "Square lino block with a carved wave pattern and a cutting gouge at its corner",
      tags=["lino print", "linoleum block", "relief print", "printmaking", "carving", "block print"],
      aliases=["lino-print"])
def _(S):
    return [shell(rect(3, 3, 18, 18, L(S, 2, 4))), detail("M6.5 9C8.3 6.5 9.8 11.5 12 9S15.7 6.5 17.5 9"),
            detail("M6.5 15C8.3 12.5 9.8 17.5 12 15S15.7 12.5 17.5 15")]


@icon("lino-cutter", CAT, "Lino cutter with a round mushroom handle and a short U-shaped gouge blade",
      tags=["lino tool", "gouge", "v tool", "linocut", "carving tool", "printmaking"], aliases=["lino-tool"])
def _(S):
    handle = "M5.5 13H18.5C18.5 18.5 15.5 21.5 12 21.5C8.5 21.5 5.5 18.5 5.5 13Z"
    cup = "M9.3 2.5C9.3 5.2 10.8 6 12 6C13.2 6 14.7 5.2 14.7 2.5Z"
    return tilt([shell(handle), shell(rect(10.5, 9.5, 3, 3.5)), line(seg(12, 9.5, 12, 5)), solid(cup)])


@icon("baren", CAT, "Baren: a flat round printing pad with a knotted cord handle, pressing on a sheet",
      tags=["printing pad", "burnisher", "woodblock printing", "relief print", "printmaking", "hand press"])
def _(S):
    pad = rect(3, 12, 18, 5, 2.5 if S.name == "rounded" else 1.5)
    handle = "M8.5 12C8.5 6.5 15.5 6.5 15.5 12"
    return [shell(pad), line(handle), solid(circle(12, 6.3, 2)), line(seg(2, 20.5, 22, 20.5))]


@icon("movable-type", CAT, "Single metal type sort: a short block with a raised reversed letter F on its face",
      tags=["letterpress", "type sort", "printing type", "metal type", "typography", "printing press"],
      aliases=["type-sort"])
def _(S):
    # reversed F: stem on the right, arms pointing left
    face = poly([(17, 2), (7.5, 2), (7.5, 4.8), (14, 4.8), (14, 6.3), (9.5, 6.3), (9.5, 9), (14, 9), (14, 12.5),
                 (17, 12.5)], closed=True)
    return [solid(face), shell(rect(4, 12, 16, 9.5, L(S, 1.5, 3.5))), detail(seg(7.5, 15, 16.5, 15))]


# ============================================================================ printing, papermaking and bookbinding

@icon("composing-stick", CAT, "Composing stick: a long metal tray with a sliding knee clamp holding a row of type blocks",
      tags=["typesetting", "letterpress", "type tray", "hand setting", "printing press", "compositor"],
      aliases=["typesetting-stick"])
def _(S):
    parts = [shell(poly([(2.5, 13), (2.5, 20), (21.5, 20), (21.5, 13)], r=S.r), stroke_miterlimit="2"),
             solid(rect(17.5, 4.5, 4, 9, L(S, 0, 1)))]
    for x in (5.5, 9.5, 13.5):
        parts.append(solid(rect(x - 1.25, 6.5, 2.5, 6.5, L(S, 0, 0.6))))
    return parts


@icon("type-case", CAT, "Shallow wooden type case divided into many small compartments of different sizes",
      tags=["letterpress", "typesetting", "type drawer", "printing", "compartments", "print shop"],
      aliases=["type-drawer"])
def _(S):
    return [shell(rect(2.5, 4.5, 19, 15, L(S, 1.5, 3.5))), detail(seg(9, 4.5, 9, 19.5)), detail(seg(15, 4.5, 15, 19.5)),
            detail(seg(2.5, 12, 9, 12)), detail(seg(15, 9.5, 21.5, 9.5)), detail(seg(15, 14.5, 21.5, 14.5))]


@icon("screen-printing", CAT, "Mesh screen frame with a printed star in the centre and a squeegee pulled across the top",
      tags=["silk screen", "screenprint", "serigraphy", "squeegee", "t-shirt printing", "printmaking"],
      aliases=["silk-screen"])
def _(S):
    star = poly([pt_on(12, 15.5, 4 if i % 2 == 0 else 1.8, -90 + i * 36) for i in range(10)], closed=True)
    return [shell(rect(2.5, 9.5, 19, 12, L(S, 1.5, 3.5))), hole(star), shell(rect(2.5, 2.5, 19, 4, L(S, 1, 2)))]


@icon("block-print-stamp", CAT, "Carved wooden printing block with a round knob handle and a flower pattern printed below it",
      tags=["block printing", "hand stamp", "rubber stamp", "textile printing", "relief print", "craft"],
      aliases=["printing-block"])
def _(S):
    flower = union(*[circle(12 + dx, 18.6 + dy, 1.7) for dx, dy in ((0, -1.7), (1.7, 0), (0, 1.7), (-1.7, 0))])
    stamp = union(circle(12, 4.8, 2.6), rect(10.5, 6.5, 3, 3), rect(4.5, 9, 15, 5, L(S, 1, 2.5)))
    return [shell(stamp), solid(flower)]


@icon("embossing-stylus", CAT, "Embossing stylus with a ball tip at each end pressing a raised line into paper",
      tags=["ball stylus", "embossing tool", "paper craft", "card making", "stencil embossing", "scrapbooking"],
      aliases=["emboss-stylus"])
def _(S):
    tool = turn([shell(rect(11, 6, 2, 12, 1)), solid(circle(12, 4.3, 2.3)), solid(circle(12, 19.7, 2.3))], 40)
    tool = shift_to(tool, rot_pt((12, 19.7), 40), (8, 15.5))
    bump = "M2.5 21.5H6.5C7 19 9 19 9.5 21.5H21.5"
    return tool + [line(bump)]


@icon("paper-marbling", CAT, "Shallow tray of liquid with swirling feathered marbling patterns across its surface",
      tags=["marbled paper", "suminagashi", "ebru", "swirl", "bookbinding", "endpaper"],
      aliases=["marbled-paper"])
def _(S):
    tray = rect(2.5, 4.5, 19, 15, L(S, 1.5, 3.5))
    sp = []
    for k in range(0, 41):
        th = k / 40 * 2.6 * math.pi
        r = 0.6 + 0.55 * th
        sp.append(pt_on(12, 12, r, th * 180 / math.pi))
    return [shell(tray), detail(poly(sp))]


@icon("papermaking-frame", CAT, "Wooden mould and deckle frame with a mesh screen lifted above a vat, water dripping from it",
      tags=["handmade paper", "mould and deckle", "paper vat", "pulp", "paper craft", "recycling paper"],
      aliases=["mould-and-deckle"])
def _(S):
    vat = poly([(3, 16), (21, 16), (19.5, 21.5), (4.5, 21.5)], closed=True, r=S.r)
    return [shell(rect(4.5, 2, 15, 8, L(S, 1, 2.5))), detail(seg(12, 2, 12, 10)), detail(seg(4.5, 6, 19.5, 6)),
            solid(drop_d(8.5, 11.5, 14.3, 2.2)), solid(drop_d(15.5, 12, 14.8, 2.2)), shell(vat)]


@icon("bookbinding", CAT, "Stack of folded paper sections sewn along the spine with thread, and a needle hanging beside it",
      tags=["book sewing", "signatures", "spine stitching", "handmade book", "bindery", "book craft"],
      aliases=["book-sewing"])
def _(S):
    return [shell(rect(4, 3.5, 11, 17, L(S, 1.5, 3))), line(seg(2.5, 7.5, 8, 7.5)), line(seg(2.5, 12, 8, 12)),
            line(seg(2.5, 16.5, 8, 16.5)), line("M20 6.5V20.5"), hole(rect(19.3, 8.5, 1.4, 2.6)),
            line("M20 6.5C20 3.5 17 3 15 4.5")]


@icon("bone-folder", CAT, "Bone folder with one rounded and one pointed end creasing the fold of a sheet of paper",
      tags=["paper creaser", "folding tool", "scoring", "origami", "bookbinding", "card making"],
      aliases=["paper-creaser"])
def _(S):
    tool = "M12 2C13.5 6 16 9 16 14.5C16 19.5 14 22 12 22C10 22 8 19.5 8 14.5C8 9 10.5 6 12 2Z"
    if S.name == "line":
        tool = "M12 2L16 11V19C16 21 14 22 12 22C10 22 8 21 8 19V11Z"
    return tilt([shell(tool)])


@icon("book-press", CAT, "Book press: a book squeezed between two flat boards by a central screw with a cross handle",
      tags=["bookbinding", "standing press", "screw press", "flattening books", "bindery", "pressing"],
      aliases=["standing-press"])
def _(S):
    body = union(rect(4, 9, 16, 3), rect(6, 12, 12, 6), rect(3, 18, 18, 3))
    return [line(seg(7, 2.5, 17, 2.5)), line(seg(12, 2.5, 12, 9)), shell(body, stroke_miterlimit="2"),
            detail(seg(6, 12, 18, 12)), detail(seg(6, 18, 18, 18))]


@icon("halftone-dots", CAT, "Square grid of printing dots that shrink from large at one corner to tiny at the other",
      tags=["halftone", "dot pattern", "print screen", "comic dots", "gradient", "newspaper print"],
      aliases=["halftone"])
def _(S):
    parts = [shell(rect(2.5, 2.5, 19, 19, L(S, 2, 4)))]
    for i in range(3):
        for j in range(3):
            r = 1.9 - 0.3 * (i + j)
            x, y = 7.5 + 4.5 * j, 7.5 + 4.5 * i
            parts.append(Part("dot", circle(x, y, r) if S.name == "rounded" else rect(x - r, y - r, 2 * r, 2 * r)))
    return parts


# ============================================================================ sculpture

@icon("marble-block", CAT, "Rough rectangular block of marble with chipped corners and a vein running across its face",
      tags=["stone block", "sculpting stone", "quarry", "raw stone", "statue material", "carving"],
      aliases=["stone-block"])
def _(S):
    block = poly([(3, 10), (7, 5.5), (21, 5.5), (21, 16.5), (17, 21), (3, 21)], closed=True, r=S.r * 0.6)
    return [shell(block), detail(poly([(3, 10), (17, 10), (21, 5.5)])), detail(seg(17, 10, 17, 21)),
            detail(poly([(6.5, 17), (8, 14), (10.5, 16), (12.5, 13.5)], r=S.r * 0.4))]


@icon("stone-carving", CAT, "Pointed chisel held against a rough stone block with small chips flying off",
      tags=["chisel", "sculpting", "masonry", "statue", "stonemason", "carving"], aliases=["stonemasonry"])
def _(S):
    stone = poly([(2.5, 15), (5, 13), (10, 13.5), (13, 12), (21.5, 15), (21.5, 21.5), (2.5, 21.5)], closed=True, r=S.r * 0.8)
    chisel = [Part(p.kind, rot(p.d, -28, 11, 13), p.attrs) for p in [
        shell(poly([(9.8, 2), (14.2, 2), (14.2, 9), (12, 12.5), (9.8, 9)], closed=True, r=S.r * 0.4)),
        detail(seg(9.8, 5, 14.2, 5))]]
    chips = [solid(poly([(16, 9.5), (18.3, 8.2), (18.3, 10.8)], closed=True)), solid(poly([(19, 5.5), (21, 4.5), (21, 7)], closed=True))]
    return [shell(stone)] + chisel + chips


@icon("clay-loop-tool", CAT, "Wooden sculpting tool with a round wire loop at one end and a square wire loop at the other",
      tags=["loop tool", "ribbon tool", "wire tool", "modelling tool", "ceramics", "clay"],
      aliases=["ribbon-tool"])
def _(S):
    return tilt([line(circle(12, 5.3, 3.2)), shell(rect(10.5, 9.5, 3, 6, L(S, 1, 1.5))),
                 line(rect(8.8, 15.7, 6.4, 6, L(S, 0, 1.5)))])


@icon("banding-wheel", CAT, "Heavy round banding wheel turntable on a short central pedestal, with a ring on its top",
      tags=["turntable", "ceramics wheel", "decorating wheel", "pottery", "slow wheel", "studio"],
      aliases=["pottery-turntable"])
def _(S):
    disc = "M3 8A9 3.5 0 0 1 21 8V10.5A9 3.5 0 0 1 3 10.5Z"
    body = union(disc, rect(10, 12, 4, 7), ellipse(12, 19, 7, 2.3))
    return [shell(body), detail("M3 8A9 3.5 0 0 0 21 8"), hole(ellipse(12, 8, 3.8, 1.2))]


@icon("wire-armature", CAT, "Stick figure built from bent twisted wire standing on a small wooden base",
      tags=["sculpture frame", "figure armature", "modelling", "skeleton", "clay figure", "maquette"],
      aliases=["armature"])
def _(S):
    return [line(circle(12, 4.3, 2.5)), line(seg(12, 6.8, 12, 14)),
            line(poly([(6, 12), (9, 8.5), (12, 8.8), (15, 8.5), (18, 12)], r=S.r * 0.6)),
            line(poly([(12, 14), (9.5, 17), (9.5, 19.5)], r=S.r * 0.6)), line(poly([(12, 14), (14.5, 17), (14.5, 19.5)], r=S.r * 0.6)),
            shell(rect(5, 19.5, 14, 2.3, L(S, 0.5, 1.1)))]


@icon("hanging-mobile", CAT, "Hanging mobile: a bar on a string with a smaller bar and shapes balanced beneath it",
      tags=["kinetic sculpture", "kinetic art", "balance", "nursery mobile", "baby mobile", "suspended"],
      aliases=["mobile-sculpture"])
def _(S):
    return [line(seg(12, 2.5, 12, 6)), line(seg(5.5, 6, 18.5, 6)), line(seg(5.5, 6, 5.5, 10.5)), shell(circle(5.5, 13, 2.4)),
            line(seg(16.5, 6, 16.5, 11)), line(seg(12.5, 11, 20.5, 11)), line(seg(12.5, 11, 12.5, 14.5)),
            solid(poly([(12.5, 14.5), (15, 19), (10, 19)], closed=True)),
            line(seg(20.5, 11, 20.5, 14.5)), solid(circle(20.5, 17.3, 2.3))]


@icon("wood-carving", CAT, "Small carved bird figure with curled wood shavings beside it",
      tags=["woodcarving", "whittled bird", "folk art", "wood sculpture", "shavings", "carving"])
def _(S):
    bird = union(ellipse(9.5, 14, 6, 4.3), circle(14, 8.3, 3), poly([(16.4, 7.3), (20.5, 9), (16.6, 10.3)], closed=True),
                 poly([(4.5, 12.5), (2.5, 9), (6, 11)], closed=True))
    return [shell(bird), dot(14.4, 7.7, 1.0), line(seg(6, 20, 14, 20)),
            line("M17 17.5C17 15.5 20 15.5 20 17.5C20 19.3 17.7 19.5 17.3 18"), line("M17 21C18 20 20.5 20 21.5 21")]


@icon("display-plinth", CAT, "Square display plinth with a thin top slab and a base, holding a small sphere",
      tags=["pedestal", "gallery stand", "sculpture stand", "museum display", "exhibit", "podium"],
      aliases=["pedestal"])
def _(S):
    body = union(rect(6, 8.5, 12, 2.5, L(S, 0.5, 1)), rect(8.5, 11, 7, 8), rect(6, 19, 12, 2.5, L(S, 0.5, 1)))
    return [shell(circle(12, 4.6, 2.6)), shell(body), detail(seg(8.5, 11, 15.5, 11)), detail(seg(8.5, 19, 15.5, 19))]


@icon("ice-sculpture", CAT, "Swan carved from a block of ice, with sparkle marks beside it",
      tags=["ice carving", "swan", "frozen art", "wedding centrepiece", "buffet", "winter"],
      aliases=["ice-swan"])
def _(S):
    pts = [(4.6, 5.2), (6.3, 3.2), (8.7, 3.3), (9.9, 5.4), (9.6, 8.2), (10.6, 10.5), (15, 9.5), (19.5, 6.5), (20, 12.5),
           (16, 16.8), (9, 17), (5.3, 14.7), (7.6, 12.8), (7, 9.8), (6.8, 7.3), (6.6, 5.8)]
    swan = smooth(pts, L(S, 0.35, 0.8))
    return [shell(swan), dot(7.9, 4.9, 0.8), shell(rect(3, 18.5, 18, 3, L(S, 0.5, 1.2))),
            solid(poly([(19.5, 2.5), (20.3, 4.7), (22.5, 5.5), (20.3, 6.3), (19.5, 8.5), (18.7, 6.3), (16.5, 5.5), (18.7, 4.7)], closed=True))]


# ============================================================================ pottery and ceramics

@icon("pottery-wheel", CAT, "Potter's wheel with a dome of clay on the wheel head inside a wide splash pan",
      tags=["throwing", "potter", "ceramics", "wheel thrown", "clay", "studio"],
      aliases=["potters-wheel"])
def _(S):
    clay = "M8 12.5C8 7.5 10.5 4.5 12 4.5S16 7.5 16 12.5A4 1.6 0 0 1 8 12.5Z"
    base = poly([(7, 18.5), (17, 18.5), (18.5, 21.5), (5.5, 21.5)], closed=True, r=S.r)
    return [shell(ellipse(12, 13, 10, 4)), shell(clay), shell(base)]


@icon("pinch-pot", CAT, "Small lopsided round pinch pot with an uneven rim and fingertip dents on its side",
      tags=["handbuilt", "clay bowl", "hand built pottery", "beginner ceramics", "kids craft", "fingerprints"])
def _(S):
    bowl = "M3.5 9.5C3.5 16.5 7.5 20.5 12 20.5C16.5 20.5 20.5 16.5 20.5 9.5C17.5 11 15 8.5 12 9.8C9 11 6.5 8.5 3.5 9.5Z"
    if S.name == "rounded":
        bowl = "M3.5 10C3.5 16.5 7.5 20.5 12 20.5C16.5 20.5 20.5 16.5 20.5 10C17.5 11 15 8.8 12 10C9 11 6.5 8.8 3.5 10Z"
    return [shell(bowl), hole(circle(8, 14.2, 1.15)), hole(circle(15.2, 16.2, 1.15))]


@icon("coil-pot", CAT, "Round pot built up from stacked horizontal coils of clay with a ridge between each row",
      tags=["coiled pottery", "hand building", "clay coils", "ceramics", "traditional pottery", "craft"])
def _(S):
    if S.name == "line":
        pot = "M8 4H16C16 6.5 20 8.5 20 14C20 18 18 21 15.5 21H8.5C6 21 4 18 4 14C4 8.5 8 6.5 8 4Z"
    else:
        pot = "M8 4H16C16 6.5 20 8.5 20 14C20 18.5 16.5 21 12 21C7.5 21 4 18.5 4 14C4 8.5 8 6.5 8 4Z"
    return [shell(pot), detail("M4.6 11Q12 13.6 19.4 11"), detail("M4.3 15.5Q12 18.2 19.7 15.5")]


@icon("pottery-rib", CAT, "Flat kidney-shaped pottery rib with a smooth curved outline",
      tags=["kidney scraper", "clay rib", "smoothing tool", "ceramics tool", "wood rib", "throwing tool"],
      aliases=["kidney-rib"])
def _(S):
    pts = [(3.5, 11.5), (5.5, 7), (11, 4.8), (17, 5.8), (20.5, 9.5), (19, 13.5), (14.5, 14), (12.5, 17.5), (8.5, 20), (4.8, 18)]
    return [shell(rot(smooth(pts, L(S, 0.45, 0.9)), 25, 12, 12))]


@icon("kintsugi", CAT, "Round bowl with a jagged crack line across it, drawn as a bold repaired seam",
      tags=["kintsugi bowl", "golden repair", "japanese repair", "mended pottery", "broken bowl", "wabi sabi"],
      aliases=["kintsugi-bowl"])
def _(S):
    body = "M2.5 8.5H21.5C21.5 15 17.5 20 12 20C6.5 20 2.5 15 2.5 8.5Z"
    return [shell(body), line(seg(8.5, 21.5, 15.5, 21.5)),
            detail(poly([(11, 8.5), (13.5, 11.5), (10.5, 14), (13.5, 16.5), (12, 20)], r=S.r * 0.3))]


@icon("porcelain-vase", CAT, "Round-bellied vase with a short narrow neck and a painted wavy band around the middle",
      tags=["ceramic vase", "china", "ming style", "pottery", "decorative ware", "antique"])
def _(S):
    n = L(S, 2.4, 3)
    vase = (f"M{12 - n - 1.2} 2.5H{12 + n + 1.2}C{12 + n + 0.5} 4 {12 + n} 5 {12 + n} 6.5C18.5 8 20 11 20 14C20 17.5 17.5 19.5 16 21.5H8"
            f"C6.5 19.5 4 17.5 4 14C4 11 5.5 8 {12 - n} 6.5C{12 - n} 5 {12 - n - 0.5} 4 {12 - n - 1.2} 2.5Z")
    return [shell(vase), detail("M4.2 13.5C6.6 11.5 9 15.5 12 13.5S17.4 11.5 19.8 13.5"), dot(12, 17.8, 1.0)]


@icon("glaze-dipping", CAT, "Bowl gripped by tongs being dipped into a bucket of glaze with drips falling back in",
      tags=["glazing", "dip glaze", "tongs", "ceramics", "kiln prep", "pottery finishing"],
      aliases=["glazing-bowl"])
def _(S):
    bowl = "M6.5 5.5H17.5C17.5 9 15.5 10.5 12 10.5C8.5 10.5 6.5 9 6.5 5.5Z"
    bucket = poly([(3, 16.5), (21, 16.5), (19.5, 21.5), (4.5, 21.5)], closed=True, r=S.r)
    return [shell(bowl), line(poly([(6, 5.5), (9.5, 2.5), (12, 2.5)])), line(poly([(18, 5.5), (14.5, 2.5), (12, 2.5)])),
            solid(drop_d(9.5, 11.6, 14.4, 2)), solid(drop_d(14.5, 12, 14.8, 2)), shell(bucket)]


@icon("slip-casting-mold", CAT, "Two-part plaster mold bound with a strap, liquid clay being poured into the gap on top",
      tags=["slip casting", "plaster mould", "casting clay", "ceramics mould", "pouring slip", "pottery"],
      aliases=["slip-mold"])
def _(S):
    return [shell(rect(3, 10, 7.5, 11.5, L(S, 1.5, 3))), shell(rect(13.5, 10, 7.5, 11.5, L(S, 1.5, 3))),
            hole(rect(3, 14.8, 18, 3)), solid(rect(11, 2.5, 2, 6.5, 1))]


# ============================================================================ knitting and yarn tools

@icon("circular-knitting-needle", CAT, "Circular knitting needle: two short pointed tips joined by a long flexible cable forming a loop",
      tags=["knitting needles", "circular needle", "cable needle", "yarn", "knitting in the round", "hat knitting"],
      aliases=["circular-needle"])
def _(S):
    top = L(S, 2.5, 3.2)
    k = L(S, 0, 0.6)
    left = poly([(4.3, 11.5), (7.7, 11.5), (7.7, 7), (6, top), (4.3, 7)], closed=True, r=k)
    right = poly([(16.3, 11.5), (19.7, 11.5), (19.7, 7), (18, top), (16.3, 7)], closed=True, r=k)
    return [solid(left), solid(right), line("M6 11.5C6 20 9.5 21 11.3 18.3C12 17.2 12.6 17.2 13.3 18.3C14.5 21 18 20 18 11.5")]


@icon("row-counter", CAT, "Knitting row counter: a barrel with a number window threaded on a pointed needle",
      tags=["stitch counter", "knitting counter", "tally", "count rows", "knitting tool", "yarn craft"],
      aliases=["knitting-counter"])
def _(S):
    return [line(seg(12, 6, 12, 8.5)), solid(poly([(10.8, 6), (13.2, 6), (12, 2.3)], closed=True)),
            shell(rect(5.5, 8.5, 13, 9, L(S, 2, 4))), hole(rect(8.5, 11, 7, 4, L(S, 0, 1))), line(seg(12, 17.5, 12, 19.5)),
            solid(circle(12, 20.6, 1.4))]


@icon("stitch-marker", CAT, "Small open locking ring stitch marker with a clasp, hanging on a strand of yarn",
      tags=["knitting marker", "locking marker", "ring marker", "crochet marker", "knitting notion", "yarn"],
      aliases=["knitting-marker"])
def _(S):
    return [line(arc(12, 10.5, 5, 20, 340)), line(poly([(16.7, 8.8), (20.5, 8.3)])) if False else solid(rect(16.4, 10.6, 4.2, 2.6, L(S, 0, 1))),
            line("M2.5 19C6 19 8 15 12 15.5C15 16 17 19.5 21.5 18.5")]


@icon("yarn-swift", CAT, "Collapsible yarn swift: a spoked wheel frame on a clamp with a skein of yarn stretched around it",
      tags=["skein holder", "yarn winder", "wool winding", "umbrella swift", "knitting tool", "yarn craft"],
      aliases=["skein-winder"])
def _(S):
    ring = circle(12, 9.5, 7.3) if S.name == "rounded" else poly(regular(12, 9.5, 8, 6), closed=True)
    spokes = [detail(seg(12, 9.5, *pt_on(12, 9.5, 7, -90 + k * 60))) for k in range(6)]
    return [shell(ring)] + spokes + [line(seg(12, 17.5, 12, 19.5)), shell(rect(7.5, 19.5, 9, 2.2, L(S, 0.5, 1.1)))]


@icon("ball-winder", CAT, "Tabletop yarn ball winder with a side crank handle and a flat-topped cake of yarn on its spindle",
      tags=["yarn winder", "center pull ball", "yarn cake", "wool winder", "knitting tool", "yarn craft"],
      aliases=["yarn-winder"])
def _(S):
    cake = poly([(4.5, 17), (15.5, 17), (14, 7.5), (6, 7.5)], closed=True, r=S.r * 0.6)
    return [shell(cake), detail(seg(5.5, 12.3, 14.9, 12.3)), line(seg(10, 7.5, 10, 4)),
            shell(rect(3, 17, 18, 4, L(S, 0.8, 2))), line(seg(19, 17, 19, 10.5)), solid(circle(19, 8.5, 2))]


@icon("wool-carders", CAT, "Pair of wool carders with wire-toothed paddles and straight handles, a puff of wool between them",
      tags=["hand carders", "carding wool", "fibre prep", "spinning", "fleece", "yarn craft"],
      aliases=["hand-carders"])
def _(S):
    top = union(rect(2.5, 3, 12, 5.5, L(S, 1, 2.5)), rect(14, 4.25, 7.5, 3, L(S, 0.5, 1.5)))
    bottom = union(rect(9.5, 15, 12, 5.5, L(S, 1, 2.5)), rect(2.5, 16.25, 7.5, 3, L(S, 0.5, 1.5)))
    wool = union(circle(8.5, 12, 1.9), circle(12, 11.5, 2.3), circle(15.5, 12, 1.9))
    return [shell(top), shell(bottom), solid(wool)]


@icon("spool-knitter", CAT, "Spool knitter doll: a small cylinder with pegs on top and a knitted cord growing from the bottom",
      tags=["knitting nancy", "french knitting", "i-cord", "corking", "kids knitting", "yarn craft"],
      aliases=["knitting-nancy"])
def _(S):
    parts = [shell(rect(5, 7, 14, 8.5, L(S, 1.5, 3.5))), dot(9.5, 11.2, 1.1), dot(14.5, 11.2, 1.1)]
    for x in (7.5, 10.5, 13.5, 16.5):
        parts.append(line(seg(x, 3.5, x, 7)))
        parts.append(dot(x, 3.2, 1.3))
    parts.append(shell(rect(9.3, 15.5, 5.4, 6, L(S, 0, 1.5))))
    parts.append(detail(seg(9.3, 18.5, 14.7, 18.5)))
    return parts
