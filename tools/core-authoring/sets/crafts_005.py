"""TypeIcon Core: crafts (batch crafts_005): photography and film gear, drawing and painting techniques,
pottery and fibre tools, hobby builds and wooden keepsakes.

Objects are drawn front-on or from the side. Small marks inside a shell are knocked out of the Filled style
(hole) or left solid (solid). Line and Rounded differ by corner radius, caps and explicit per-style choices.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path.parser import parse_path
from geometry import SCALE, D, P, ST, U, fmt, path_to_d, poly_d, rotation

CAT = "crafts"
TILT = 45


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    """Container corner radius: small in Line, full in Rounded (capped for small shapes)."""
    if cap is None:
        return S.R
    return min(1.0, cap / 2) if S.name == "line" else cap


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


def flipx(d):
    """Mirror a d-string left to right about x = 12."""
    return tf(d, (-1, 0, 0, 1, 24, 0))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def grow(d, g):
    """Region d expanded by g px (cuts a clean gap where one part passes behind another)."""
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def band(d, w=2.0, S=None):
    """Closed region of a w px wide stroke along the open path d."""
    cap = "round" if S is not None and S.name == "rounded" else "butt"
    return path_to_d(ST(d, w, cap, "round" if cap == "round" else "miter"))


def hole(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def tilt(parts, deg=TILT, cx=12.0, cy=12.0):
    return [Part(p.kind, rot(p.d, deg, cx, cy), p.attrs) for p in parts]


def shift(parts, dx, dy):
    return [Part(p.kind, mv(p.d, dx, dy), p.attrs) for p in parts]


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
    return shift(parts, dx, dy)


def heart_d(cx, cy, w):
    """Heart of width w centred on (cx, cy)."""
    k = w / 16.0
    return tf("M12 20L4.4 12.6A4.6 4.6 0 0 1 11 6.3L12 7.3L13 6.3A4.6 4.6 0 0 1 19.6 12.6Z",
              (k, 0, 0, k, cx - 12 * k, cy - 13 * k))


def star_d(cx, cy, ro, ri=None, r=0.0):
    ri = ro * 0.45 if ri is None else ri
    pts = [pt_on(cx, cy, ro if i % 2 == 0 else ri, -90 + i * 36) for i in range(10)]
    return poly(pts, closed=True, r=r)


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    x = u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0]
    y = u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]
    dx = 3 * u * u * (p1[0] - p0[0]) + 6 * u * t * (p2[0] - p1[0]) + 3 * t * t * (p3[0] - p2[0])
    dy = 3 * u * u * (p1[1] - p0[1]) + 6 * u * t * (p2[1] - p1[1]) + 3 * t * t * (p3[1] - p2[1])
    n = math.hypot(dx, dy) or 1
    return (x, y), (-dy / n, dx / n)


# ============================================================================ machines, books and photo gear

@icon("treadle-sewing-machine", CAT, "Vintage sewing machine on an iron table with a wide foot pedal below",
      tags=["treadle", "vintage sewing machine", "antique sewing", "foot pedal", "sewing", "tailor"])
def _(S):
    body = union(rect(3, 3, 18, 6.5, rr(S, 2)), rect(15.5, 3, 5.5, 11, rr(S, 1)))
    return [
        shell(body),
        line(seg(6.5, 9.5, 6.5, 12.5)),
        line(seg(2.5, 14.5, 21.5, 14.5)),
        line(seg(6, 14.5, 6, 21)),
        line(seg(18, 14.5, 18, 21)),
        shell(rect(8.5, 17.5, 7, 3.5, rr(S, 1.75))),
    ]


@icon("accordion-book", CAT, "Book with a hard cover whose pages fold in a zigzag concertina",
      tags=["concertina book", "folded book", "leporello", "zigzag book", "artist book", "paper craft"])
def _(S):
    pages = poly([(7, 6), (11.5, 4), (16, 6), (20.5, 4), (20.5, 20), (16, 18), (11.5, 20), (7, 18)], closed=True, r=S.r * 0.6)
    return [
        shell(rect(3, 5, 4, 14, rr(S, 1.5))),
        shell(pages),
        detail(seg(11.5, 4, 11.5, 20)),
        detail(seg(16, 6, 16, 18)),
    ]


@icon("macro-photography", CAT, "Camera lens ring framing a single flower in close-up",
      tags=["macro", "close-up", "flower photo", "macro lens", "camera", "nature photography"])
def _(S):
    flower = union(circle(12, 9.6, 2.4), circle(14.4, 12, 2.4), circle(12, 14.4, 2.4), circle(9.6, 12, 2.4))
    ring = poly(regular(12, 12, 9.6, 8, -67.5), closed=True) if S.name == "line" else circle(12, 12, 9)
    return [shell(ring), detail(flower), hole(circle(12, 12, 1.1))]


@icon("photo-corners", CAT, "Print held on a page by a small triangular mount at each corner",
      tags=["photo mounts", "album corners", "scrapbook", "photo album", "snapshot", "picture"])
def _(S):
    parts = [shell(rect(5, 5, 14, 14, rr(S, 1.5)))]
    for sx, sy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        cx, cy = 12 + sx * 9, 12 + sy * 9
        parts.append(solid(poly([(cx, cy), (cx - sx * 6.5, cy), (cx, cy - sy * 6.5)], closed=True, r=L(S, 0, 0.5))))
    parts.append(detail(poly([(8.5, 15), (11, 11.5), (13, 14), (14, 13), (15.5, 15)], r=S.r * 0.5)))
    return parts


@icon("barn-doors", CAT, "Round studio light with four hinged flaps around its front opening",
      tags=["light shaper", "studio light", "flags", "lighting", "film set", "photography"])
def _(S):
    k = S.r * 0.5
    top = poly([(8.5, 6), (15.5, 6), (18, 2.5), (6, 2.5)], closed=True, r=k)
    parts = [shell(circle(12, 12, 3.5)), shell(top)]
    for deg in (90, 180, 270):
        parts.append(shell(rot(top, deg)))
    return parts


@icon("underwater-camera-housing", CAT, "Boxy waterproof housing around a camera with a round lens port and two side handles",
      tags=["dive camera", "waterproof case", "scuba", "diving", "underwater photography", "camera"])
def _(S):
    handle = poly([(7, 7.5), (3.5, 7.5), (3.5, 13.5), (7, 13.5)], r=S.r)
    return [
        shell(rect(7, 4.5, 10, 11, rr(S, 3))),
        shell(circle(12, 10, 2.6)),
        line(handle),
        line(flipx(handle)),
        line("M3 20.5Q5.25 18.7 7.5 20.5T12 20.5T16.5 20.5T21 20.5"),
    ]


@icon("color-calibration-card", CAT, "Square reference card printed with a grid of small colour patches",
      tags=["test chart", "colour chart", "white balance", "calibration", "gray card", "photography"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, rr(S, 3)))]
    for i in range(3):
        for j in range(3):
            parts.append(hole(rect(5.75 + i * 4.75, 5.75 + j * 4.75, 2.5, 2.5, L(S, 0, 0.6))))
    return parts


_VASE_L = [(8, 3), (8.6, 5.2), (9.5, 7.2), (9.3, 8.6), (9.6, 10.4), (9.2, 12), (10, 13.4), (9.3, 15), (9.4, 16.8), (8.6, 18.4), (7, 21)]


def _vase_pts():
    return _VASE_L + [(24 - x, y) for x, y in reversed(_VASE_L)]


@icon("face-vase-illusion", CAT, "Square picture of a vase whose sides are two faces in profile looking at each other",
      tags=["rubin vase", "optical illusion", "two faces", "figure ground", "perception", "psychology"],
      filled=lambda: D(U(P(rect(3, 3, 18, 18, 2)), ST(rect(3, 3, 18, 18, 2), 2)), P(poly(_vase_pts(), closed=True))))
def _(S):
    return [shell(rect(3, 3, 18, 18, rr(S, 3))), detail(poly(_vase_pts(), closed=True, r=S.r * 0.8))]


@icon("flexible-curve", CAT, "Bendable drafting ruler curved into a gentle S shape with cross ticks along it",
      tags=["french curve", "drafting", "flex curve", "ruler", "design", "measuring"])
def _(S):
    p0, p1, p2, p3 = (3.5, 17), (11, 17), (13, 7), (20.5, 7)
    d = f"M{fmt(p0[0])} {fmt(p0[1])}C{fmt(p1[0])} {fmt(p1[1])} {fmt(p2[0])} {fmt(p2[1])} {fmt(p3[0])} {fmt(p3[1])}"
    parts = [shell(band(d, 4, S))]
    for t in (0.2, 0.4, 0.6, 0.8):
        (x, y), (nx, ny) = bez(p0, p1, p2, p3, t)
        parts.append(detail(seg(x - nx * 2, y - ny * 2, x + nx * 2, y + ny * 2)))
    return parts


@icon("pour-painting", CAT, "Cup tipped over a square canvas with swirling cells of paint spreading out",
      tags=["fluid art", "acrylic pour", "flow painting", "paint", "abstract art", "canvas"])
def _(S):
    cup = poly([(12.5, 2), (20.5, 2), (19, 9.5), (14, 9.5)], closed=True, r=S.r * 0.6)
    cup = tf(cup, rotation(-112, 16, 6))
    cup = mv(cup, 1, -0.5)
    return [
        shell(cup),
        line("M9.5 9.5C9.5 11 8.5 11.5 8.5 13"),
        shell(rect(3, 13, 18, 8, rr(S, 2))),
        hole(circle(9, 17.2, 1.5)), hole(circle(14, 16.6, 1)), hole(circle(17.5, 18, 1.2)),
    ]


def _club_parts(S, deg):
    head = union(ellipse(12, 6, 3.6, 4), poly([(9.2, 8), (14.8, 8), (13, 13.2), (11, 13.2)], closed=True))
    parts = [Part("shell", head), Part("line", seg(12, 13, 12, 19.5)), Part("solid", circle(12, 20, 1.7) if S.name == "rounded"
                                                                          else rect(10.4, 18.6, 3.2, 2.6))]
    return [Part(p.kind, rot(p.d, deg, 12, 16), p.attrs) for p in parts]


@icon("juggling-clubs", CAT, "Two bowling pin shaped juggling clubs crossed in an X",
      tags=["juggling", "circus", "clubs", "performer", "street performer", "skills"])
def _(S):
    return _club_parts(S, -38) + _club_parts(S, 38)


@icon("tattoo-flash", CAT, "Sheet of paper printed with a small set of simple tattoo designs: a heart, a star and an anchor",
      tags=["tattoo design", "tattoo sheet", "flash art", "tattoo parlour", "ink", "body art"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 2.5))),
        hole(heart_d(8.3, 8.3, 5.6)),
        hole(star_d(15.7, 8, 3.2, 1.5)),
        hole(circle(12, 13.6, 1.2)),
        detail(seg(12, 14.8, 12, 19)),
        detail(arc(12, 16.6, 3.2, 15, 165)),
    ]


@icon("comic-strip", CAT, "Horizontal strip of three comic panels with a speech bubble in the middle panel",
      tags=["comic", "cartoon", "panels", "graphic novel", "manga", "speech bubble"])
def _(S):
    bubble = union(ellipse(12, 10.6, 2.3, 1.6), poly([(11, 11.6), (11, 13.8), (13.2, 12)], closed=True))
    return [
        shell(rect(2.5, 5, 19, 14, rr(S, 2.5))),
        detail(seg(8.5, 5, 8.5, 19)),
        detail(seg(15.5, 5, 15.5, 19)),
        hole(circle(5.5, 11, 1.2)),
        hole(bubble),
        hole(star_d(18.5, 12, 1.9, 0.9)),
    ]


@icon("storyboard", CAT, "Grid of six small film frames with rough sketches, used to plan a scene shot by shot",
      tags=["shot list", "frames", "film planning", "animation", "scenes", "pre-production"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, rr(S, 3))), detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)), detail(seg(3, 12, 21, 12))]
    parts += [hole(circle(6, 7.5, 1.1)), hole(poly([(10.8, 9.5), (12, 6), (13.2, 9.5)], closed=True)),
              hole(rect(16.8, 6, 2.4, 2.4, L(S, 0, 0.6))), hole(seg(5, 17.5, 7, 15.5) and poly([(5, 17.8), (6, 14.6), (7, 17.8)], closed=True)),
              hole(circle(12, 16, 1.1)), hole(circle(18, 16, 1.1))]
    return parts


@icon("lucet", CAT, "Lyre shaped two pronged fork with a braided square cord hanging from beneath it",
      tags=["cordmaking", "braiding", "cord making", "lyre", "craft tool", "string"])
def _(S):
    return [
        line("M5.5 3.5C4 10 7.5 13.5 12 13.5S20 10 18.5 3.5"),
        dot(5.5, 3.5, 1.6), dot(18.5, 3.5, 1.6),
        shell(rect(10, 15, 4, 6.5, L(S, 0, 1.5))),
        hole(rect(11.3, 17.5, 1.4, 2.5)),
    ]


# ============================================================================ machines, prints and paint

@icon("embroidery-machine", CAT, "Sewing machine head with a round hoop of stretched fabric under the needle",
      tags=["machine embroidery", "embroidery hoop", "sewing machine", "monogram", "stitching", "needlework"])
def _(S):
    body = union(rect(3, 3, 18, 4.5, rr(S, 2)), rect(3, 3, 4.5, 18, rr(S, 2)))
    return [
        shell(body),
        line(seg(15, 7.5, 15, 10.5)),
        shell(circle(15, 15.8, 4.7)),
        hole(star_d(15, 16, 2.4, 1.1)),
    ]


def _head_pts():
    """Side view of a head facing right: rounded skull, nose, lips, chin and neck as polygon points."""
    pts = [(9.5, 21), (9.5, 17)]
    for a in range(125, 361, 12):
        pts.append(pt_on(11.5, 9.6, 7.6, a))
    pts += [(19.1, 11.6), (21, 13.2), (19.3, 14.2), (19.4, 15.6), (18.4, 16.4), (18.4, 18), (16, 18.6), (16, 21)]
    return pts


@icon("double-exposure", CAT, "Head in profile with a tree blended into the silhouette",
      tags=["photo effect", "overlay", "profile", "nature portrait", "blend", "photography"])
def _(S):
    return [
        shell(poly(_head_pts(), closed=True, r=S.r * 0.6)),
        hole(poly([(11.5, 4.8), (14.6, 9.5), (8.4, 9.5)], closed=True, r=L(S, 0, 0.5))),
        hole(poly([(11.5, 8), (15.4, 14.5), (7.6, 14.5)], closed=True, r=L(S, 0, 0.5))),
        hole(rect(10.7, 14, 1.6, 6)),
    ]


def _vignette_corners():
    return D(P(rect(4, 5, 16, 14)), P(ellipse(12, 12, 7.8, 5.6)))


@icon("vignette-photo", CAT, "Photo frame with darkened corners fading toward a light oval centre",
      tags=["vignette", "photo effect", "edit photo", "dark corners", "filter", "photography"],
      filled=lambda: D(U(P(rect(3, 4, 18, 16, 2)), ST(rect(3, 4, 18, 16, 2), 2)), P(ellipse(12, 12, 7.2, 5)))) 
def _(S):
    return [shell(rect(3, 4, 18, 16, rr(S, 3))), solid(path_to_d(_vignette_corners()))]


@icon("sign-painting", CAT, "Long thin lettering brush painting a bold letter H on a flat sign board",
      tags=["lettering", "signwriting", "hand lettering", "brush", "signwriter", "typography"])
def _(S):
    brush = [line(seg(12, 1, 12, 7)), solid(poly([(10.6, 7), (13.4, 7), (12, 11.5)], closed=True))]
    brush = [Part(p.kind, rot(p.d, -40, 12, 11), p.attrs) for p in brush]
    brush = shift(brush, -3, 0)
    return brush + [
        shell(rect(3, 12, 18, 9, rr(S, 2))),
        detail(seg(9.5, 14.5, 9.5, 18.5)),
        detail(seg(14.5, 14.5, 14.5, 18.5)),
        detail(seg(9.5, 16.5, 14.5, 16.5)),
    ]


@icon("fabric-painting", CAT, "Tote bag with a painted flower on its front",
      tags=["textile paint", "tote bag", "fabric art", "painted bag", "flower design", "craft"])
def _(S):
    bag = poly([(5, 9), (19, 9), (20.5, 21), (3.5, 21)], closed=True, r=S.r * 0.6)
    flower = union(circle(12, 13.6, 1.7), circle(14.1, 15.7, 1.7), circle(12, 17.8, 1.7), circle(9.9, 15.7, 1.7))
    return [
        line("M8.5 9V6.5A3.5 3.5 0 0 1 15.5 6.5V9") if S.name == "rounded" else line("M8.5 9V6.5L10 3.5H14L15.5 6.5V9"),
        shell(bag),
        hole(flower),
    ]


@icon("glass-painting", CAT, "Wine glass decorated with painted dots",
      tags=["stained glass paint", "painted glass", "wine glass", "glassware", "decorating", "craft"])
def _(S):
    bowl = "M7 3H17C17.3 9 15.5 12.8 12 13C8.5 12.8 6.7 9 7 3Z"
    return [
        shell(bowl) if S.name == "rounded" else shell(poly([(7, 3), (17, 3), (16.5, 9), (12, 13), (7.5, 9)], closed=True)),
        line(seg(12, 13, 12, 20)),
        line(seg(8, 20.5, 16, 20.5)),
        hole(circle(9.8, 6, 0.9)), hole(circle(14.2, 6, 0.9)), hole(circle(12, 8.8, 0.9)),
    ]


@icon("bamboo-ink-painting", CAT, "Bamboo stalk with joints and a few long pointed leaves in brush stroke style",
      tags=["sumi-e", "ink wash", "chinese painting", "bamboo", "brush painting", "calligraphy"])
def _(S):
    stalk = rect(9.5, 2.5, 5, 19, rr(S, 2))
    leaf_r1 = "M14.5 8.5C16 4.5 19 3 21.5 3C20.5 6 18 8.5 14.5 8.5Z"
    leaf_r2 = "M14.5 14C17 11.5 20 11.5 22 12.5C20.5 15 17.5 15.5 14.5 14Z"
    leaf_l = "M9.5 12.5C8 9.5 5.5 8 2.5 8C3.5 11 6 13 9.5 12.5Z"
    return [
        shell(stalk),
        detail(seg(9.5, 8.5, 14.5, 8.5)),
        detail(seg(9.5, 15.5, 14.5, 15.5)),
        solid(leaf_r1), solid(leaf_r2), solid(leaf_l),
    ]


@icon("canvas-roll", CAT, "Roll of raw canvas partly unrolled into a flat sheet",
      tags=["canvas", "raw canvas", "artist canvas", "painting surface", "fabric roll", "art supplies"])
def _(S):
    return [
        shell(circle(8, 9.5, 6)),
        detail(arc(8, 9.5, 2.4, 180, 450)),
        shell(rect(8, 15.5, 13.5, 4.5, rr(S, 2.25))),
    ]


@icon("ruling-pen", CAT, "Drafting pen with two pointed steel blades held apart by an adjusting screw",
      tags=["drafting pen", "technical pen", "ink line", "draughtsman", "drawing instrument", "calligraphy"])
def _(S):
    parts = [
        shell(rect(9.5, 12.5, 5, 10, rr(S, 2.5))),
        line(poly([(9.8, 12.5), (9.8, 8), (12, 1.5)])),
        line(poly([(14.2, 12.5), (14.2, 8), (12, 1.5)])),
        line(seg(14.2, 8.5, 17.5, 8.5)),
        solid(circle(18, 8.5, 1.8)) if S.name == "rounded" else solid(rect(16.7, 7.2, 2.6, 2.6)),
    ]
    return fit(tilt(parts, 45))


@icon("tripod-dolly", CAT, "Tripod with a camera head standing on a three armed wheeled base",
      tags=["camera dolly", "film gear", "tripod wheels", "camera support", "film set", "video"])
def _(S):
    return [
        shell(rect(8.5, 2.5, 7, 4, rr(S, 2))),
        line(poly([(5.5, 17), (12, 6.5), (18.5, 17)])),
        line(seg(12, 6.5, 12, 17)),
        line(seg(3.5, 17, 20.5, 17)),
        solid(circle(4.5, 20, 1.8)), solid(circle(12, 20, 1.8)), solid(circle(19.5, 20, 1.8)),
    ]


@icon("camera-jib", CAT, "Long counterweighted arm on a tripod with a camera at its tip",
      tags=["jib arm", "camera crane", "film crane", "boom", "cinematography", "video"])
def _(S):
    return [
        line(seg(5, 16, 14.5, 9.5)),
        shell(rect(2.5, 14.5, 4, 5, rr(S, 1.5))),
        shell(rect(13.5, 3, 6, 6.5, rr(S, 2))),
        solid(rect(19.5, 4.5, 2, 3.5)),
        line(seg(11.5, 11.6, 9, 21.5)),
        line(seg(11.5, 11.6, 16, 21.5)),
    ]


@icon("v-flat", CAT, "Two tall white boards hinged together and standing in a V shape",
      tags=["reflector board", "bounce board", "studio lighting", "photo studio", "light modifier", "photography"])
def _(S):
    return [
        shell(poly([(3, 3), (12, 6), (21, 3), (21, 21), (12, 18), (3, 21)], closed=True, r=S.r * 0.7)),
        detail(seg(12, 6, 12, 18)),
    ]


@icon("framed-jersey", CAT, "Sports shirt spread flat inside a rectangular frame with a number on it",
      tags=["sports memorabilia", "shirt frame", "collectible", "football shirt", "wall display", "fan"])
def _(S):
    shirt = poly([(9.5, 5.5), (12, 8), (14.5, 5.5), (17.5, 7.5), (16.5, 10.5), (15.5, 9.8), (15.5, 18.5), (8.5, 18.5), (8.5, 9.8),
                  (7.5, 10.5), (6.5, 7.5)], closed=True, r=S.r * 0.4)
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 2.5))),
        detail(shirt),
        hole(poly([(10.3, 13.4), (12, 11.6), (13.7, 11.6), (13.7, 16.6), (11.9, 16.6), (11.9, 13.4)], closed=True)),
    ]


@icon("pressed-penny", CAT, "Elongated oval souvenir coin flattened and stamped with a star",
      tags=["souvenir coin", "elongated coin", "penny press", "tourist keepsake", "coin", "collectible"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, L(S, 5.5, 7))),
        hole(star_d(12, 12, 4.6, 2.0, r=L(S, 0, 0.4))),
    ]


def _rock(cx, cy, sx, sy, k):
    """Small lumpy stone as a rounded polygon around (cx, cy)."""
    pts = [(-2.4, -0.6), (-1.2, -2.0), (1.0, -2.3), (2.4, -0.8), (2.1, 1.3), (0.2, 2.3), (-1.8, 1.6)]
    pts = [(cx + x * sx, cy + y * sy) for x, y in pts]
    return poly(pts, closed=True, r=k)


@icon("rock-collection", CAT, "Box divided into compartments, each holding a small stone",
      tags=["rocks", "minerals", "geology", "stone samples", "rockhound", "specimens"])
def _(S):
    k = 1.2
    return [
        shell(rect(3, 4, 18, 16, rr(S, 3))),
        detail(seg(12, 4, 12, 20)),
        detail(seg(3, 12, 21, 12)),
        hole(_rock(7.5, 8, 0.95, 0.95, k)),
        hole(_rock(16.5, 8, 0.85, 0.9, k)),
        hole(_rock(7.5, 16, 0.9, 0.85, k)),
        hole(_rock(16.5, 16, 0.95, 1.0, k)),
    ]


# ============================================================================ hobby builds, clay and fibre

@icon("slot-car", CAT, "Low race car on a short stretch of track with a guide slot down the middle",
      tags=["slot racing", "toy car", "model racing", "race track", "hobby", "slot track"])
def _(S):
    body = poly([(3, 14.5), (3, 12), (9, 11), (11.5, 7.5), (16, 7.5), (18.5, 11), (21, 12), (21, 14.5)], closed=True, r=S.r * 0.7)
    return [
        shell(body),
        solid(circle(7, 15, 2.3)), solid(circle(17, 15, 2.3)),
        shell(rect(2.5, 18.5, 19, 3.5, rr(S, 1.75))),
        hole(rect(6, 19.65, 12, 1.2)),
    ]


@icon("tin-can-lantern", CAT, "Tin can with a wire handle and a pattern of punched holes letting out points of light",
      tags=["punched tin", "candle holder", "upcycled", "camping light", "luminary", "recycled craft"])
def _(S):
    return [
        line(arc(12, 9, 6, 180, 360)),
        shell(rect(6, 9, 12, 12, rr(S, 2))),
        detail(seg(6, 11.5, 18, 11.5)),
        detail(seg(6, 18.5, 18, 18.5)),
        hole(circle(8.6, 13.9, 0.8)), hole(circle(12, 13.9, 0.8)), hole(circle(15.4, 13.9, 0.8)),
        hole(circle(10.3, 16.4, 0.8)), hole(circle(13.7, 16.4, 0.8)),
    ]


@icon("sgraffito", CAT, "Round plate with a dark glaze layer and a leaf pattern scratched through it with a pointed tool",
      tags=["scratched design", "pottery decoration", "ceramics", "glaze", "plate", "scratch art"])
def _(S):
    leaf = "M11 19C7 16 7 10 11 6.5C15 10 15 16 11 19Z" if S.name == "rounded" else "M11 19L7.5 13L11 6.5L14.5 13Z"
    return [
        shell(circle(11, 12.5, 8.5)),
        detail(leaf),
        detail(seg(11, 19, 11, 12)),
        line(seg(21, 3, 17, 7)),
        solid(poly([(17, 7), (16.8, 9.2), (14.8, 7.2)], closed=True)),
    ]


@icon("encaustic-painting", CAT, "Small flat iron gliding over a panel and leaving smooth melted wax streaks behind it",
      tags=["wax painting", "hot wax", "beeswax", "fine art", "wax iron", "painting technique"])
def _(S):
    return [
        line(poly([(12.5, 9), (12.5, 4.5), (17, 4.5), (17, 9)], r=S.r)),
        shell(poly([(9.5, 16), (9.5, 11.5), (13, 9), (18, 9), (21, 16)], closed=True, r=S.r * 0.6)),
        line("M3 15.5Q4.75 13.5 6.5 15.5T9.5 15.5"),
        line(seg(3, 20, 21, 20)),
    ]


@icon("silk-painting", CAT, "Square frame of stretched silk showing an outlined flower with a brush touching one petal",
      tags=["silk art", "gutta", "textile painting", "scarf", "fabric art", "brush"])
def _(S):
    flower = union(circle(9, 7.8, 2.3), circle(11.3, 10.1, 2.3), circle(9, 12.4, 2.3), circle(6.7, 10.1, 2.3))
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        detail(flower),
        line(seg(20, 20, 14.5, 14.5)),
        solid(poly([(14.5, 14.5), (13, 12.5), (12.5, 13.3), (13.3, 14.3)], closed=True)) if False else solid(poly([(14.6, 14.6), (12.6, 12.9), (13.0, 12.4), (15.1, 14.1)], closed=True)),
    ]


@icon("needle-book", CAT, "Small fabric booklet opened to show felt pages with needles pinned through them",
      tags=["needle case", "felt pages", "sewing notions", "hand sewing", "needles", "sewing kit"])
def _(S):
    book = "M12 6C9.5 4.3 6 4 3 5V19C6 18 9.5 18.3 12 20C14.5 18.3 18 18 21 19V5C18 4 14.5 4.3 12 6Z"
    return [
        shell(book) if S.name == "rounded" else shell(poly([(12, 6), (3, 5), (3, 19), (12, 20), (21, 19), (21, 5)], closed=True)),
        detail(seg(12, 6, 12, 20)),
        hole(circle(5.6, 10, 0.9)), detail(seg(7.5, 10, 10, 10)),
        hole(circle(5.6, 14, 0.9)), detail(seg(7.5, 14, 10, 14)),
        hole(circle(14.4, 9.5, 0.9)), detail(seg(16.3, 9.5, 19, 9.5)),
        hole(circle(14.4, 13.5, 0.9)), detail(seg(16.3, 13.5, 19, 13.5)),
    ]


@icon("drum-carder", CAT, "Wool carding machine with a large and a small spiked drum on a frame and a side crank handle",
      tags=["carding", "wool prep", "fibre prep", "batts", "spinning", "fleece"])
def _(S):
    return [
        shell(circle(9.5, 10.5, 6.5)),
        hole(circle(9.5, 10.5, 1.3)),
        shell(circle(18.5, 16, 3)),
        line(seg(2.5, 21.5, 21.5, 21.5)),
        line(seg(9.5, 17, 9.5, 21.5)),
        line(seg(18.5, 19, 18.5, 21.5)),
        line(seg(9.5, 10.5, 4, 4.5)),
        solid(circle(3.5, 4, 1.8)),
    ]


@icon("warping-board", CAT, "Rectangular board with pegs along its top and bottom edges and warp thread zigzagging between them",
      tags=["weaving", "warp", "loom prep", "pegs", "thread", "textile"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, rr(S, 3)))]
    parts += [detail(poly([(7, 6.5), (12, 17.5), (17, 6.5)], r=S.r * 0.5)), detail(poly([(7, 17.5), (12, 6.5), (17, 17.5)], r=S.r * 0.5))]
    for x in (7, 12, 17):
        parts += [dot(x, 6.5, 1.4), dot(x, 17.5, 1.4)]
    return parts


@icon("water-brush", CAT, "Brush pen with a clear barrel showing water inside, a drop and a soft pointed brush tip",
      tags=["water brush pen", "watercolor", "travel brush", "refillable brush", "painting", "sketching"])
def _(S):
    parts = [
        solid(poly([(10.4, 8.5), (13.6, 8.5), (12, 1.5)], closed=True, r=L(S, 0, 0.3))),
        shell(rect(10, 8.5, 4, 2.5, rr(S, 1))),
        shell(rect(9, 11, 6, 10.5, rr(S, 3))),
        hole(circle(12, 17.6, 1.4)) if S.name == "rounded" else hole(poly([(12, 15.6), (13.4, 18), (10.6, 18)], closed=True)),
    ]
    return fit(tilt(parts, 45))


@icon("dodging-tool", CAT, "Thin wire wand with a small round card disc on its end held over a print",
      tags=["darkroom", "photo printing", "enlarger", "burning and dodging", "shading", "analog photography"])
def _(S):
    return [
        line(seg(11.5, 8.5, 21, 3)),
        shell(circle(9, 10, 3)),
        shell(rect(3, 16, 18, 5.5, rr(S, 2))),
    ]


@icon("rc-helicopter", CAT, "Small helicopter with a top rotor and tail rotor above a handheld radio controller with an antenna",
      tags=["radio control", "remote control", "toy helicopter", "hobby", "model aircraft", "transmitter"])
def _(S):
    return [
        line(seg(9, 3, 21, 3)),
        line(seg(15, 3, 15, 5.5)),
        shell(ellipse(15, 8.5, 4.2, 2.8)),
        line(seg(10.8, 8.5, 4, 6.5)),
        line(seg(3.5, 4, 3.5, 8.5)),
        shell(rect(3, 14.5, 13, 7, rr(S, 2.5))),
        line(seg(6, 14.5, 6, 11.5)),
        solid(circle(6, 11, 1.2)),
        hole(circle(7.5, 18, 1.4)), hole(rect(11, 17.2, 3.2, 1.6, L(S, 0, 0.8))),
    ]


@icon("river-table", CAT, "Wooden slab table with two live edges framing a wavy resin river down the middle",
      tags=["epoxy table", "resin table", "live edge", "wood slab", "furniture", "woodworking"])
def _(S):
    river = "M9.5 5C13.5 7.2 8.5 9.4 10.8 12H14.2C12 9.4 17 7.2 13 5Z"
    return [
        shell(poly([(5, 5), (21, 5), (19, 12), (3, 12)], closed=True, r=S.r * 0.6)),
        hole(river),
        line(seg(5.5, 12.5, 5.5, 21)),
        line(seg(17.5, 12.5, 17.5, 21)),
    ]


@icon("macrame-plant-hanger", CAT, "Knotted cords hanging from a ring and gathering around a round plant pot",
      tags=["macrame", "hanging planter", "plant holder", "knotted cord", "boho", "houseplant"])
def _(S):
    return [
        shell(circle(12, 3.8, 1.8)),
        line(seg(12, 5.6, 12, 8)),
        solid(circle(12, 8.6, 1.5)),
        line(poly([(12, 8.6), (6, 15)])),
        line(poly([(12, 8.6), (18, 15)])),
        line(seg(12, 8.6, 12, 15)),
        shell(poly([(5.5, 14.5), (18.5, 14.5), (16.5, 21.5), (7.5, 21.5)], closed=True, r=S.r * 0.7)),
    ]


@icon("hand-cast", CAT, "Plaster cast of an upright hand with open fingers standing on a small square base",
      tags=["plaster hand", "life cast", "hand mold", "sculpture", "keepsake", "mould"])
def _(S):
    return [
        shell(rect(5.5, 12, 13, 6.5, rr(S, 2))),
        line(seg(7.3, 12, 7.3, 6)),
        line(seg(10.4, 12, 10.4, 3.5)),
        line(seg(13.6, 12, 13.6, 4)),
        line(seg(16.7, 12, 16.7, 7)),
        line(seg(18.5, 15, 21, 10.5)),
        shell(rect(6, 18.5, 12, 3, rr(S, 1.5))),
    ]


@icon("slip-trailer", CAT, "Squeeze bottle with a thin nozzle drawing a raised dotted line of clay slip",
      tags=["slip decoration", "pottery", "ceramics", "clay", "squeeze bottle", "trailing"])
def _(S):
    return [
        shell(poly([(8, 2.5), (16, 2.5), (16, 9), (13, 11.5), (11, 11.5), (8, 9)], closed=True, r=S.r * 0.8)),
        detail(seg(8, 6, 16, 6)),
        line(seg(12, 11.5, 12, 15.5)),
        solid(circle(4.5, 19.5, 1.4)), solid(circle(8.5, 19.5, 1.4)), solid(circle(12.5, 19.5, 1.4)),
        solid(circle(16.5, 19.5, 1.4)), solid(circle(20.5, 19.5, 1.4)),
    ]


@icon("bead-design-board", CAT, "Curved U shaped board with a groove channel and a few beads laid out in a necklace line",
      tags=["bead board", "necklace layout", "jewellery design", "beading", "bead tray", "jewelry making"])
def _(S):
    cx, cy, r = 12, 8.5, 6.8
    parts = [shell(band(arc(cx, cy, r, 0, 180), 4.5, S))]
    for a in (30, 60, 90, 120, 150):
        x, y = pt_on(cx, cy, r, a)
        parts.append(hole(circle(x, y, 1.05)))
    return parts


@icon("clay-cane", CAT, "Short log of polymer clay with a flower pattern on its cut end and one thin slice beside it",
      tags=["polymer clay", "millefiori", "cane", "clay slice", "clay cane", "jewellery making"])
def _(S):
    log = union(ellipse(8, 8.5, 4, 5.5), rect(8, 3, 8, 11), ellipse(16, 8.5, 4, 5.5))
    flower = union(circle(8, 7.2, 1.2), circle(9.3, 8.5, 1.2), circle(8, 9.8, 1.2), circle(6.7, 8.5, 1.2))
    return [
        shell(log),
        detail("M8 3A4 5.5 0 0 0 8 14"),
        hole(flower),
        shell(circle(17, 19, 2.6) if S.name == "rounded" else poly(regular(17, 19, 2.9, 8, -22.5), closed=True)),
        hole(circle(17, 19, 0.9)),
    ]


@icon("origami-ball", CAT, "Ball made of many folded paper units with pointed petal tips all around its surface",
      tags=["kusudama", "paper ball", "modular origami", "folded paper", "paper craft", "decoration"])
def _(S):
    star = poly([pt_on(12, 12, 9.6 if i % 2 == 0 else 6.6, -90 + i * 15) for i in range(24)], closed=True, r=S.r * 0.12)
    return [shell(star), detail(circle(12, 12, 3)) if S.name == "rounded" else detail(poly(regular(12, 12, 3.3, 8, -22.5), closed=True))]


@icon("light-trails", CAT, "Curving road at night with long streaking parallel light lines following the bend",
      tags=["long exposure", "night photography", "car lights", "traffic streaks", "slow shutter", "highway"])
def _(S):
    parts = [line("M6 21C6 9 12 4 21 4"), line("M11 21C11 13 14 9 21 9"), line("M16 21C16 16 18 14 21 14")]
    return parts + [solid(rect(2.5, 19.5, 2, 2)) if S.name == "line" else solid(circle(3.5, 20.5, 1.2))]


@icon("shaker-box", CAT, "Oval wooden box with a lid and pointed swallowtail fingers joining its side band",
      tags=["shaker oval box", "wooden box", "bentwood", "swallowtail joint", "woodworking", "storage box"])
def _(S):
    body = "M3 7C3 4.8 7 3.5 12 3.5S21 4.8 21 7V16C21 19 17 20.5 12 20.5S3 19 3 16Z"
    return [
        shell(body),
        detail("M3 7C3 9.2 7 10.5 12 10.5S21 9.2 21 7"),
        detail(poly([(14, 12.5), (18.5, 14.5), (14, 16.5), (18.5, 18.5)], r=S.r)),
    ]


@icon("carved-wooden-chain", CAT, "Three linked chain loops carved from a single piece of wood, still attached to a small block",
      tags=["love spoon chain", "whittling", "wood carving", "chain links", "carved chain", "woodcraft"])
def _(S):
    return [
        line(rect(8.5, 2.5, 7, 7, 3.5)),
        line(seg(12, 5, 12, 14)),
        line(rect(8.5, 10.5, 7, 7, 3.5)),
        shell(rect(6, 17.5, 12, 4, rr(S, 2))),
    ]
