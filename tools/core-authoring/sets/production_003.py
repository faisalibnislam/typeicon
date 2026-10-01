"""TypeIcon Core: production (photo and video capture, exposure, darkroom and film stock), batch 3.

Photo frames are the only shell where possible; the picture inside is a detail or a knocked-out dot so the
Filled style reads as a solid frame with the drawing cut out of it.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar

CAT = "production"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def ko(d) -> Part:
    """Solid region: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def frame(S, x=2, y=4, w=20, h=16):
    return shell(rect(x, y, w, h, S.R))


def rotp(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def behind(S, back, front, w=2.0):
    """Stroke of `back` with the area covered by `front` (plus a 1 px gap) removed: a card tucked behind another."""
    stroke = ST(back, w, S.cap, S.join)
    mask = U(P(front), ST(front, 4.0, S.cap, S.join))
    return solid(path_to_d(D(stroke, mask)))


def head(S, cx, cy, tip, rad):
    """Helper for arrow heads: two short strokes at the end of a curve, `tip` point with direction deg."""
    return None


def arrow_arc(cx, cy, r, a0, a1, hl=2.4):
    """Clockwise arc from a0 to a1 (degrees) with an open arrow head at the end."""
    tx, ty = polar(cx, cy, r, a1)
    d = arc(cx, cy, r, a0, a1)
    th = math.radians(a1)
    dx, dy = -math.sin(th), math.cos(th)  # travel direction
    out = d
    for sgn in (1, -1):
        ang = math.radians(150) * sgn
        ca, sa = math.cos(ang), math.sin(ang)
        hx = dx * ca - dy * sa
        hy = dx * sa + dy * ca
        out += seg(tx, ty, tx + hx * hl, ty + hy * hl)
    return out


# ============================================================================ capture and stage

@icon("motion-capture-suit", CAT, "Standing figure in a body suit with marker dots on its joints",
      tags=["mocap", "motion capture", "performance capture", "suit", "animation", "vfx", "tracking markers"])
def _(S):
    return [
        shell(rect(9, 7.5, 6, 7.5, L(S, 1, 2.5))),
        shell(circle(12, 3.8, 1.9)),
        line("M9 9L4.5 13M15 9L19.5 13"),
        line("M10.5 15L9.5 21M13.5 15L14.5 21"),
        dot(6.6, 11.2, 1.5), dot(17.4, 11.2, 1.5), dot(10, 18.2, 1.5), dot(14, 18.2, 1.5),
    ]

@icon("facial-capture-helmet", CAT, "Head in profile with a helmet and a thin boom arm holding a small camera before the face",
      tags=["facial capture", "face tracking", "helmet camera", "performance capture", "head rig", "mocap", "animation"])
def _(S):
    head = poly([(2.5, 13.5), (3, 8.5), (7, 6), (11.5, 7), (13.5, 11.5), (14.5, 15), (13, 15.5), (13, 20), (6, 20), (6, 16.5), (3.5, 16.5)],
                closed=True, r=S.r * 1.6)
    return [
        shell(head),
        detail(seg(2.5, 12, 13.2, 12)),
        line(poly([(9, 6.5), (9, 2.8), (18.5, 2.8), (18.5, 9.5)], r=S.r)),
        shell(rect(16.5, 10, 4.5, 4.5, L(S, 1, 1.5))),
    ]

@icon("led-volume-stage", CAT, "Curved wall of screens showing mountains with a small camera on a tripod before it",
      tags=["virtual production", "led wall", "volume", "screen wall", "film set", "backdrop", "vfx"])
def _(S):
    wall = "M3 4Q12 2 21 4V12.5Q12 15 3 12.5Z" if S.name == "line" else "M4.5 4.4Q12 2.2 19.5 4.4Q21 4.8 21 6.3V11.7Q21 12.7 19.5 13Q12 14.8 4.5 13Q3 12.7 3 11.7V6.3Q3 4.8 4.5 4.4Z"
    return [
        shell(wall),
        detail(poly([(5.5, 11), (9, 7), (11.5, 9.5), (14.5, 6.5), (18.5, 11)], r=S.r * 0.6)),
        shell(rect(9, 16, 6, 3, 1)),
        line("M10.5 19L8 22M13.5 19L16 22"),
    ]

@icon("photogrammetry-scan", CAT, "Small object at the centre with a ring of cameras around it pointing inward",
      tags=["3d scan", "photogrammetry", "scanning", "capture rig", "cameras", "reconstruction", "model"])
def _(S):
    parts = [line(circle(12, 12, 8.8))]
    for k in range(4):
        pts = rotp([(9.6, 2.4), (14.4, 2.4), (12, 6.8)], k * 90)
        parts.append(shell(poly(pts, closed=True, r=S.r * 0.4)))
    parts.append(shell(poly(regular(12, 12, 3.4, 6), closed=True, r=S.r * 0.6)))
    return parts


@icon("exposure-triangle", CAT, "Triangle joining an aperture, a shutter dial and a sensitivity badge at its corners",
      tags=["exposure", "aperture", "shutter speed", "iso", "photography basics", "manual mode", "camera settings"])
def _(S):
    tp, bl, br = (12, 5.2), (5, 18), (19, 18)

    def trim(a, b, ra, rb):
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy)
        ux, uy = dx / n, dy / n
        return seg(a[0] + ux * ra, a[1] + uy * ra, b[0] - ux * rb, b[1] - uy * rb)
    r = 3.3
    return [
        line(trim(tp, bl, r + 1, r + 1) + trim(tp, br, r + 1, r + 1) + trim(bl, br, r + 1, r + 1)),
        shell(circle(tp[0], tp[1], r)), ko(circle(tp[0], tp[1], 1.0)),
        shell(circle(bl[0], bl[1], r)), detail(seg(bl[0], bl[1] - r + 0.5, bl[0], bl[1])),
        shell(rect(br[0] - r, br[1] - r, 2 * r, 2 * r, L(S, 0.8, 1.6))), ko(circle(br[0], br[1], 1.0)),
    ]


@icon("iso-sensitivity", CAT, "Rounded badge with the letters ISO above a row of grain dots",
      tags=["iso", "sensitivity", "light sensitivity", "camera settings", "grain", "noise", "exposure"])
def _(S):
    return [
        frame(S, 2, 3, 20, 13),
        detail("M6.5 7V12"),
        detail(poly([(12, 7), (9.5, 7), (9.5, 9.5), (12, 9.5), (12, 12), (9.5, 12)], r=S.r * 0.3)),
        detail(rect(14.5, 7, 3, 5, L(S, 0.3, 1.5))),
        dot(5.5, 19.5, 1.0), dot(10, 20, 1.0), dot(14.5, 19.5, 1.0), dot(18.5, 20, 1.0),
    ]


@icon("exposure-bracketing", CAT, "Three photo frames fanned out with minus, zero and plus marks beneath",
      tags=["bracketing", "hdr", "exposure", "auto bracket", "multiple exposures", "camera settings", "photography"])
def _(S):
    def card(dx, deg):
        pts = [(7.5, 3), (16.5, 3), (16.5, 15), (7.5, 15)]
        pts = [(x + dx, y) for x, y in pts]
        return rotp(pts, deg, 12, 20)
    front = poly(card(0, 0), closed=True, r=S.r * 0.6)
    lf = poly(card(0, -17), closed=True, r=S.r * 0.6)
    rt = poly(card(0, 17), closed=True, r=S.r * 0.6)
    return [
        behind(S, lf, front), behind(S, rt, front), shell(front),
        line(seg(3, 20.5, 6, 20.5)), dot(12, 20.5, 1.2), line(seg(18, 20.5, 21, 20.5) + seg(19.5, 19, 19.5, 22)),
    ]


@icon("burst-mode", CAT, "Row of overlapping photo frames offset to the right with short speed lines",
      tags=["burst", "continuous shooting", "sequence", "multiple shots", "rapid fire", "camera mode", "photography"])
def _(S):
    f0 = rect(7, 5, 8, 13, S.R * 0.4)
    f1 = rect(11, 5, 8, 13, S.R * 0.4)
    f2 = rect(15, 5, 7, 13, S.R * 0.4)
    return [behind(S, f0, f1), behind(S, f1, f2), shell(f2),
            line("M2 9H4.5M2 12H4.5M2 15H4.5"), dot(18.5, 14, 1.0)]


@icon("high-speed-photography", CAT, "Milk drop crown splash with droplets above it over a flat surface",
      tags=["milk drop", "splash", "crown", "freeze motion", "high speed", "liquid", "macro photography"])
def _(S):
    crown = poly([(5.5, 18), (6.5, 13), (9.3, 15.5), (12, 11.5), (14.7, 15.5), (17.5, 13), (18.5, 18)], closed=True, r=S.r * 0.8)
    return [
        shell(crown),
        dot(6.5, 9.2, 1.3), dot(12, 6, 1.3), dot(17.5, 9.2, 1.3), dot(9.5, 3.8, 0.01) if False else dot(15, 4, 1.0),
        line("M2.5 21.5H21.5"),
    ]

@icon("light-leak", CAT, "Photo frame with a glow spilling in from the top right corner",
      tags=["light leak", "film effect", "vintage", "glow", "flare", "overexposed", "photo effect"])
def _(S):
    return [frame(S, 3, 4, 18, 16), ko("M21 4V9A5 5 0 0 1 16 4Z"), detail(arc(21, 4, 9, 90, 180)),
            ko(circle(7, 16, 1.1))]

@icon("film-grain", CAT, "Photo frame filled with an even speckle of small dots of different sizes",
      tags=["grain", "noise", "film effect", "texture", "speckle", "analog", "photo effect"])
def _(S):
    return [frame(S, 3, 4, 18, 16),
            ko(circle(7.5, 8.5, 1.1)), ko(circle(12.5, 8, 0.9)), ko(circle(17, 9, 1.2)),
            ko(circle(9.5, 12.5, 1.3)), ko(circle(15, 13, 1.0)),
            ko(circle(7, 16, 0.9)), ko(circle(12, 16.5, 1.2)), ko(circle(17, 16.3, 1.0))]


@icon("sepia-tone", CAT, "Photo frame with mountains and a sun beside a single tint drop",
      tags=["sepia", "vintage", "brown tint", "old photo", "color grade", "photo filter", "antique"])
def _(S):
    drop = "M19.3 6.5C19.3 6.5 16.8 9.6 16.8 11.6A2.5 2.5 0 0 0 21.8 11.6C21.8 9.6 19.3 6.5 19.3 6.5Z"
    return [frame(S, 2, 5, 12, 14),
            detail(poly([(3, 17), (6.5, 12.5), (9, 15), (11, 13), (13, 17)], r=S.r * 0.5)),
            ko(circle(10.5, 8.6, 1.1)),
            shell(drop)]


@icon("moire-pattern", CAT, "Two sets of concentric rings offset against each other forming an interference lattice",
      tags=["moire", "interference", "pattern", "overlap", "screen artifact", "banding", "optics"])
def _(S):
    gap = L(S, 36, 50)
    return [line(arc(9.5, 12, 3, gap, 360 - gap)), line(arc(14.5, 12, 3, gap + 180, 180 + 360 - gap)),
            line(arc(9.5, 12, 7.5, gap, 360 - gap)), line(arc(14.5, 12, 7.5, gap + 180, 180 + 360 - gap))]

@icon("rolling-shutter-distortion", CAT, "Propeller with bent curved blades inside a camera frame",
      tags=["rolling shutter", "skew", "distortion", "propeller", "artifact", "cmos", "jello effect"])
def _(S):
    from geometry import rotation, transform_path
    blade = P("M12 11C10.5 8.5 11 6.5 14.5 5.8")
    parts = [frame(S, 2, 3, 20, 18)]
    for k in range(3):
        parts.append(detail(path_to_d(transform_path(blade, rotation(k * 120, 12, 12)))))
    parts.append(ko(circle(12, 12, 1.3)))
    return parts

@icon("motion-photo", CAT, "Photo frame with a small play circle and wave arcs on both sides",
      tags=["live photo", "motion photo", "moving picture", "animated photo", "short clip", "photo video", "play"])
def _(S):
    return [frame(S, 2, 4, 20, 16), detail(circle(12, 12, 3.5)),
            detail(arc(12, 12, 7.5, -40, 40) + arc(12, 12, 7.5, 140, 220)),
            ko(poly([(11, 10.6), (11, 13.4), (13.4, 12)], closed=True))]


@icon("switch-camera", CAT, "Camera outline with two curved arrows chasing each other in a circle inside its body",
      tags=["flip camera", "selfie camera", "front back camera", "rotate camera", "reverse camera", "camera toggle", "swap"])
def _(S):
    body = poly([(2.5, 8), (7.5, 8), (9, 5), (15, 5), (16.5, 8), (21.5, 8), (21.5, 20), (2.5, 20)], closed=True, r=S.r * 0.8)
    return [
        shell(body),
        detail(arrow_arc(12, 14, 3.6, 190, 315, 2.2)), detail(arrow_arc(12, 14, 3.6, 10, 135, 2.2)),
    ]


@icon("photo-collage", CAT, "Square frame divided into several photo panels of different sizes",
      tags=["collage", "photo grid", "layout", "multiple photos", "mosaic", "photo montage", "scrapbook"])
def _(S):
    return [frame(S, 3, 3, 18, 18), detail("M11 3V21M3 12H11M11 9H21")]


@icon("eye-autofocus", CAT, "Eye outline with a pupil inside four corner focus brackets",
      tags=["eye af", "eye detection", "autofocus", "face focus", "focus brackets", "tracking focus", "portrait"])
def _(S):
    eye = "M6 12Q12 7 18 12Q12 17 6 12Z" if S.name == "line" else "M6.2 12Q12 7 17.8 12Q12 17 6.2 12Z"
    return [
        line(poly([(3, 8), (3, 3), (8, 3)], r=S.r)), line(poly([(16, 3), (21, 3), (21, 8)], r=S.r)),
        line(poly([(3, 16), (3, 21), (8, 21)], r=S.r)), line(poly([(16, 21), (21, 21), (21, 16)], r=S.r)),
        shell(eye), dot(12, 12, 1.5),
    ]


@icon("red-eye-reduction", CAT, "Eye with a solid pupil beside a small lightning flash",
      tags=["red eye", "flash", "pre flash", "eye fix", "photo correction", "portrait", "camera flash"])
def _(S):
    eye = "M2.5 14Q8.5 6.5 14.5 14Q8.5 21.5 2.5 14Z"
    bolt = poly([(20.5, 3), (16.5, 9), (19.5, 9), (17.5, 14.5), (22, 7.5), (19, 7.5)], closed=True, r=S.r * 0.3)
    return [shell(eye), dot(8.5, 14, 1.7), shell(bolt)]


# ============================================================================ editing tools

@icon("dodge-and-burn", CAT, "Round paddle on a stick beside a hand shaped card with a hole in the palm",
      tags=["dodge", "burn", "lighten darken", "retouching", "darkroom", "photo editing", "exposure tool"])
def _(S):
    hand = poly([(11.5, 21), (11.5, 16.5), (10, 14), (11.5, 13), (13.5, 15), (13.5, 8), (21.5, 8), (21.5, 21)], closed=True, r=S.r * 0.8)
    return [shell(circle(5.5, 6.5, 3.5)), line("M5.5 10V21"), shell(hand), ko(circle(17.5, 15, 1.8))]

@icon("clone-stamp-tool", CAT, "Rubber stamp tool beside a small crosshair target",
      tags=["clone stamp", "stamp", "retouch", "copy pixels", "photo editing", "healing", "duplicate area"])
def _(S):
    stamp = poly([(5, 3), (9, 3), (9, 10), (12, 10), (12, 16), (2, 16), (2, 10), (5, 10)], closed=True, r=S.r * 0.6)
    return [shell(stamp), line("M2 20H12"),
            line(circle(18.5, 16, 3)), line("M18.5 10.5V12.5M18.5 19.5V21.5M13.5 16H15.5M21.5 16H22.5")]


@icon("curves-adjustment", CAT, "Square graph with a centre cross and an S shaped curve from bottom left to top right",
      tags=["curves", "tone curve", "contrast", "photo editing", "levels", "color grading", "adjustment"])
def _(S):
    return [frame(S, 3, 3, 18, 18), detail("M12 3V21M3 12H21"),
            ko("M5.5 18.5C10.5 18.5 9 5.5 18.5 5.5L18.5 4.4C8 4.4 10 17.4 5.5 17.4Z") if False else detail("M6 18C11 18 9.5 6 18 6")]


@icon("levels-adjustment", CAT, "Histogram hill above a slider row with three triangle handles",
      tags=["levels", "histogram", "tonal range", "black point", "white point", "photo editing", "adjustment"])
def _(S):
    hill = "M3 11.5C6 11.5 7.5 4 12 4S18 11.5 21 11.5Z"
    parts = [shell(hill), line("M2.5 15.5H21.5")]
    for x in (4, 12, 20):
        parts.append(solid(poly([(x, 17), (x - 2.4, 21.5), (x + 2.4, 21.5)], closed=True)))
    return parts


@icon("noise-reduction", CAT, "Photo frame with speckle dots on the left and a smooth side on the right divided by a sweeping line",
      tags=["denoise", "noise", "grain removal", "smooth", "clean image", "photo editing", "high iso"])
def _(S):
    return [frame(S, 3, 4, 18, 16), detail("M12.5 4C14.5 9 10.5 15 12.5 20"),
            ko(circle(6.8, 8.2, 1.0)), ko(circle(8.8, 12, 1.0)), ko(circle(6.5, 15.8, 1.0)),
            detail("M15.5 10H18.5M15.5 14H18.5")]


# ============================================================================ darkroom and film stock

@icon("darkroom-tray", CAT, "Shallow developing tray seen at an angle holding a photo print with tongs on the rim",
      tags=["developing tray", "darkroom", "chemicals", "print developing", "film photography", "tongs", "analog"])
def _(S):
    top = poly([(2, 18), (6, 11), (22, 11), (18, 18)], closed=True, r=S.r * 0.6)
    return [
        shell(top),
        line("M2 18V21H18V18"),
        detail(poly([(7, 16), (9.3, 13), (15.7, 13), (13.4, 16)], closed=True)),
        line(poly([(19.5, 2.5), (16.5, 9)], r=0) + seg(17.5, 3, 21, 8)),
    ]


@icon("film-changing-bag", CAT, "Flat lightproof bag with a zipper across the top and two sleeve openings on the sides",
      tags=["changing bag", "darkroom bag", "light tight", "film loading", "film photography", "sleeves", "analog"])
def _(S):
    return [
        shell(rect(6.5, 4.5, 11, 16, L(S, 2, 3))),
        detail("M9 8.5H15"),
        line("M6.5 12H4Q2 15 4 18H6.5"), line("M17.5 12H20Q22 15 20 18H17.5"),
    ]

@icon("slide-loupe", CAT, "Cone shaped magnifier with a wide eyepiece rim standing on a small square slide",
      tags=["loupe", "light table", "slide viewer", "transparency", "film review", "magnifier", "photography"])
def _(S):
    cone = poly([(7, 2.5), (17, 2.5), (17, 5.5), (15.5, 5.5), (17.5, 15), (6.5, 15), (8.5, 5.5), (7, 5.5)], closed=True, r=S.r * 0.5)
    return [shell(cone), shell(rect(3, 17, 18, 4.5, L(S, 0.5, 2))), ko(poly([(6, 19.9), (8.5, 18.4), (11, 19.9)], closed=True))]

@icon("medium-format-film-roll", CAT, "Short spool of film wrapped in backing paper with a tape tab on a wide spool",
      tags=["120 film", "medium format", "film roll", "spool", "backing paper", "film photography", "analog"])
def _(S):
    spool = poly([(2.5, 3), (21.5, 3), (21.5, 7), (18, 7), (18, 17), (21.5, 17), (21.5, 21), (2.5, 21), (2.5, 17), (6, 17), (6, 7), (2.5, 7)],
                 closed=True, r=S.r * 0.6)
    return [shell(spool), detail("M8 10.5H16"), ko(rect(11, 13, 5, 2.5, 0))]


@icon("110-film-cartridge", CAT, "Flat film cartridge with two chambers joined by a narrow bridge with a small window",
      tags=["110 film", "pocket film", "film cartridge", "subminiature", "film photography", "analog", "vintage camera film"])
def _(S):
    body = poly([(2.5, 5), (9, 5), (9, 8), (15, 8), (15, 5), (21.5, 5), (21.5, 19), (15, 19), (15, 16), (9, 16), (9, 19), (2.5, 19)],
                closed=True, r=S.r * 0.6)
    return [shell(body), ko(rect(10.7, 10.5, 2.6, 3, 0.4)), dot(5.8, 12, 1.2), dot(18.2, 12, 1.2)]


@icon("sheet-film-holder", CAT, "Flat holder for sheet film with a dark slide pulled half out of one end",
      tags=["large format", "film holder", "dark slide", "sheet film", "4x5", "film photography", "view camera"])
def _(S):
    return [shell(rect(3, 4, 12, 16, L(S, 1, 2))), detail(rect(6.2, 7.2, 5.6, 9.6, 0)),
            line(poly([(15, 8), (21.5, 8), (21.5, 16), (15, 16)], r=S.r * 0.4))]


@icon("instant-film-pack", CAT, "Box pack of instant photo prints with the top print leaning out of it showing its picture window",
      tags=["instant film", "film pack", "instant photo", "print", "photo paper", "instant camera"])
def _(S):
    box = rect(3, 12.5, 18, 8.5, L(S, 1.5, 3))
    back = poly(rotp([(6, 2.5), (18, 2.5), (18, 17), (6, 17)], 9, 12, 17), closed=True, r=S.r * 0.4)
    win = poly(rotp([(8.5, 5), (15.5, 5), (15.5, 10.5), (8.5, 10.5)], 9, 12, 17), closed=True)
    return [behind(S, back, box), shell(box), ko(win), ko(circle(17.5, 17, 1.0))]

@icon("daguerreotype", CAT, "Small hinged case opened like a book with an oval frame holding a portrait on one side",
      tags=["daguerreotype", "early photograph", "antique photo", "portrait case", "history of photography", "vintage", "tintype"])
def _(S):
    return [frame(S, 2.5, 4, 19, 16), detail("M12 4V20"), detail(ellipse(17.2, 12, 2.6, 4.2)),
            ko(circle(17.2, 10.8, 0.9)), ko(rect(4.8, 10.5, 2.2, 3, 0.8))]


@icon("iris-transition", CAT, "Dark frame with a small circular opening in the centre showing a figure like a closing iris wipe",
      tags=["iris wipe", "iris out", "closing circle", "film transition", "silent film", "video transition", "cartoon ending"],
      filled=lambda: U(D(P(rect(2, 3.5, 20, 17, 3)), P(circle(12, 12, 5.6))),
                       P(circle(12, 10.3, 1.7)), P("M9 16Q9.4 12.9 12 12.9Q14.6 12.9 15 16Z")))
def _(S):
    return [shell(rect(2.5, 4, 19, 16, S.R)), detail(circle(12, 12, 5.2)), ko(circle(12, 10.3, 1.4)),
            ko("M9.6 15.2Q10 12.9 12 12.9Q14 12.9 14.4 15.2Z")]

# ============================================================================ stage and rigs

@icon("rain-machine", CAT, "Tall stand holding a horizontal pipe bar that sprays rows of rain lines down to the ground",
      tags=["rain tower", "rain effect", "film set", "special effects", "sfx", "water rig", "weather effect"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 18, 3, L(S, 0.8, 1.5))),
        line("M5.5 5.5V21M3 21H8"),
        line("M10.5 9L9.5 13M14.5 9L13.5 13M18.5 9L17.5 13M12.5 16L11.5 20M16.5 16L15.5 20M20.5 16L19.5 20"),
    ]


@icon("stunt-airbag", CAT, "Large puffy cushion on the ground with a figure falling toward it",
      tags=["airbag", "stunt", "fall", "landing cushion", "safety", "stunt work", "film set"])
def _(S):
    return [
        shell(rect(2.5, 15.5, 19, 6, L(S, 2, 3))),
        shell(circle(12, 3.8, 1.8)),
        line("M12 6.5V10.5M7.5 4.5L12 8L16.5 4.5M12 10.5L9 14M12 10.5L15 14"),
    ]


@icon("ptz-camera-controller", CAT, "Desk control panel with a tall joystick on the right and buttons and a small screen on the left",
      tags=["ptz", "camera control", "joystick", "remote camera", "broadcast", "control surface", "pan tilt zoom"])
def _(S):
    return [
        shell(rect(2, 14, 20, 7, L(S, 1.5, 3))),
        shell(rect(3.5, 4.5, 9, 5.5, L(S, 1, 1.5))),
        line("M17.5 14V8"), dot(17.5, 6.2, 2.3),
        dot(6, 17.5, 1.0), dot(10, 17.5, 1.0), dot(14, 17.5, 1.0),
    ]


@icon("sound-stage", CAT, "Large arched hangar studio building with a big sliding door and a number above it",
      tags=["soundstage", "film studio", "studio lot", "hangar", "production stage", "movie set", "building"])
def _(S):
    hall = "M2.5 21V10L12 3.5L21.5 10V21Z" if S.name == "line" else "M2.5 21V10.5Q2.5 9.5 3.3 9L11.2 3.6Q12 3.1 12.8 3.6L20.7 9Q21.5 9.5 21.5 10.5V21Z"
    return [shell(hall), detail(rect(6, 12.5, 12, 8.5, 0)), detail("M12 12.5V21"),
            ko(rect(11.3, 6.5, 1.4, 3.3, 0.3))]


@icon("probe-lens", CAT, "Small camera body with a very long thin tube lens that bends to an angled tip",
      tags=["periscope lens", "snorkel lens", "macro probe", "tube lens", "insect lens", "food photography", "specialty lens"])
def _(S):
    body = U(P(rect(2.5, 8, 8, 10, L(S, 1, 2))), P(rect(3.5, 5, 4.5, 4, L(S, 0.5, 1))))
    tube = ST("M10 13H16.5L20.5 19", 4.0, S.cap, S.join)
    return [shell(path_to_d(U(body, tube))), dot(5.5, 12, 1.0)]


@icon("night-mode-photo", CAT, "Camera outline with a crescent moon and a small star inside",
      tags=["night mode", "low light", "night photography", "moon", "dark scene", "camera mode", "long exposure"])
def _(S):
    body = poly([(2.5, 8), (7.5, 8), (9, 5), (15, 5), (16.5, 8), (21.5, 8), (21.5, 20), (2.5, 20)], closed=True, r=S.r * 0.8)
    moon = path_to_d(D(P(circle(11, 14, 4.2)), P(circle(13.2, 12.7, 3.6))))
    star = poly([(16.8, 10.6), (17.4, 12.2), (19, 12.8), (17.4, 13.4), (16.8, 15), (16.2, 13.4), (14.6, 12.8), (16.2, 12.2)], closed=True)
    return [shell(body), ko(moon), ko(star)]


@icon("photo-filters", CAT, "Photo frame holding three overlapping circles in a Venn arrangement",
      tags=["filters", "effects", "photo effects", "color overlay", "venn", "image editing", "presets"])
def _(S):
    return [frame(S, 2.5, 3, 19, 18), detail(circle(12, 10, 3.4)), detail(circle(8.8, 15, 3.4)), detail(circle(15.2, 15, 3.4))]
