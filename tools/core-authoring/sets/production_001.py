"""TypeIcon Core: production (cameras, lenses, filters, rigs, stage and studio lighting), batch 001."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d

CAT = "production"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap):
    return min(S.R, cap)


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def rot(pts, deg, cx, cy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def sq(x, y, w, h, rx=0.0) -> Part:
    return Part("dot", rect(x, y, w, h, rx))


# ============================================================================ camera bodies

@icon("dslr-camera", CAT, "Side view of a digital SLR camera with a prism hump, a grip and a lens barrel",
      tags=["dslr", "camera", "photography", "slr", "photo", "digital camera"])
def _(S):
    body = poly([(2, 10), (9, 10), (9, 8), (11, 8), (12, 5.5), (17, 5.5), (18, 8), (22, 8), (22, 19), (2, 19)],
                closed=True, r=S.r * 0.6)
    return [shell(body), detail(seg(9, 10.5, 9, 18.5)), detail(seg(17, 11.5, 17, 18.5)), sq(19, 10.5, 1.5, 1.5)]


@icon("medium-format-camera", CAT, "Boxy medium format camera with a square lens and a folded up waist level finder hood",
      tags=["medium format", "camera", "film camera", "waist level", "photography", "studio camera"])
def _(S):
    return [
        line(poly([(6, 10), (7.5, 4.5), (16.5, 4.5), (18, 10)], r=S.r * 0.6)),
        shell(rect(3, 10, 18, 11, rr(S, 3))),
        detail(rect(8.5, 13, 7, 5, rr(S, 1))),
    ]


@icon("point-and-shoot-camera", CAT, "Slim compact camera with an off center lens, a flash window and a shutter button",
      tags=["compact camera", "point and shoot", "camera", "photography", "snapshot", "digital camera"])
def _(S):
    return [
        shell(rect(2, 7, 20, 13, rr(S, 3))),
        detail(circle(9, 14, 3)),
        sq(15.5, 10, 3.5, 2, L(S, 0, 0.8)),
        line(seg(15, 4, 19, 4)),
    ]


@icon("disposable-camera", CAT, "Single use film camera with a wrap band, a small lens, a flash window and a film wheel",
      tags=["single use camera", "film camera", "cheap camera", "camera", "photography", "vacation"])
def _(S):
    return [
        line(poly([(15, 7), (15, 4), (20, 4), (20, 7)], r=S.r * 0.5)),
        shell(rect(3, 7, 18, 13, rr(S, 2.5))),
        detail(seg(3, 10.5, 21, 10.5)),
        dot(12, 15, 2),
        sq(5.5, 12.5, 3, 2),
    ]


@icon("box-camera", CAT, "Old fashioned upright box camera with a carrying handle and a winding key",
      tags=["vintage camera", "box", "camera", "retro", "film camera"])
def _(S):
    return [
        line(poly([(9, 6), (9, 3), (15, 3), (15, 6)], r=S.r * 0.6)),
        shell(rect(5, 6, 14, 15, rr(S, 3))),
        detail(circle(12, 15, 3)),
        line(seg(19.5, 11, 22, 11)),
        line(seg(22, 9, 22, 13)),
    ]


@icon("hand-crank-film-camera", CAT, "Early cine camera with a hand crank and a round lens on a tall tripod",
      tags=["movie camera", "silent film", "cine camera", "tripod", "vintage", "film"])
def _(S):
    return [
        line(poly([(9, 4), (9, 1.5), (12, 1.5)], r=S.r * 0.6)),
        shell(rect(3, 4, 13, 8, rr(S, 2))),
        shell(rect(16, 6, 5, 4, rr(S, 1.5))),
        line(seg(9.5, 12, 9.5, 14.5)),
        line(seg(9.5, 14.5, 5, 22)),
        line(seg(9.5, 14.5, 14, 22)),
        line(seg(9.5, 14.5, 9.5, 22)),
    ]


@icon("camera-film-magazine", CAT, "Film camera with two round film magazine lobes seated on top",
      tags=["film magazine", "cine camera", "film reels", "motion picture", "movie camera", "camera"])
def _(S):
    top = union(circle(8, 7.5, 4), circle(16, 7.5, 4), rect(3, 10, 18, 11, rr(S, 3)))
    return [shell(top), detail(circle(12, 16, 2.5))]


# ============================================================================ lenses

@icon("wide-angle-lens", CAT, "Short lens barrel seen from the side with a large bulging front element",
      tags=["wide angle", "lens", "camera lens", "photography", "landscape", "fisheye"])
def _(S):
    body = "M21 8L13 8L13 5C5 6 5 18 13 19L13 16L21 16Z"
    return [shell(body), detail(seg(17, 8.5, 17, 15.5))]


@icon("zoom-lens", CAT, "Long lens barrel with a wide ribbed zoom ring and focal length tick marks",
      tags=["telephoto", "lens", "camera lens", "zoom", "photography", "focal length"])
def _(S):
    body = poly([(2, 8), (11, 8), (11, 5.5), (22, 5.5), (22, 18.5), (11, 18.5), (11, 16), (2, 16)], closed=True, r=S.r * 0.4)
    return [shell(body), detail(seg(14.5, 6, 14.5, 18)), detail(seg(18.5, 6, 18.5, 18)),
            sq(4.5, 10, 1, 4), sq(7.5, 10, 1, 4)]


@icon("tilt-shift-lens", CAT, "Lens barrel whose front half is tilted on a hinge with a small adjustment knob",
      tags=["tilt shift", "lens", "camera lens", "miniature", "architecture photography", "perspective control"])
def _(S):
    front = rot([(14, 7), (21, 7), (21, 17), (14, 17)], 14, 12, 12)
    return [
        shell(rect(2, 8, 9, 8, rr(S, 2))),
        shell(poly(front, closed=True, r=S.r * 0.5)),
        line(seg(11.5, 12, 14, 12)),
        dot(6.5, 4.75, 1.4), line(seg(6.5, 6, 6.5, 8)),
    ]


@icon("anamorphic-lens", CAT, "Front view of a lens with a stretched oval glass element and a horizontal light streak",
      tags=["anamorphic", "widescreen", "cinema lens", "lens", "flare", "film"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(ellipse(12, 12, 5.5, 3.4)),
        line(seg(5.5, 12, 18.5, 12)),
    ]


@icon("pancake-lens", CAT, "Very thin flat lens mounted on the front of a small camera body",
      tags=["pancake", "thin lens", "prime lens", "lens", "compact camera", "mirrorless"])
def _(S):
    return [
        shell(poly([(2, 8), (6, 8), (7, 5.5), (11, 5.5), (12, 8), (15, 8), (15, 19), (2, 19)], closed=True, r=S.r * 0.5)),
        shell(rect(17, 7, 4, 14, rr(S, 2))),
        sq(4.5, 12, 3, 3),
    ]


@icon("cine-lens", CAT, "Cylindrical cinema lens with two raised gear rings around the barrel",
      tags=["cinema lens", "film lens", "prime lens", "gear ring", "movie", "lens"])
def _(S):
    body = union(rect(2, 8, 20, 8, rr(S, 2)), rect(5, 4, 5, 16, rr(S, 2)), rect(13, 4, 5, 16, rr(S, 2)))
    return [shell(body), detail(seg(20, 8.5, 20, 15.5)), sq(7, 9.5, 1, 5), sq(15, 9.5, 1, 5)]


@icon("lens-mount", CAT, "Front view of a round camera mount opening with bayonet tabs and a locking pin",
      tags=["bayonet", "mount", "camera body", "lens mount", "interchangeable lens", "camera"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(arc(12, 12, 5.5, 215, 305)),
        detail(arc(12, 12, 5.5, 335, 65)),
        detail(arc(12, 12, 5.5, 95, 185)),
        sq(11, 7.5, 2, 1.5) if False else dot(12, 12, 1.25),
    ]


@icon("extension-tube", CAT, "Hollow tube with a wide mounting flange at each end that sits between a camera and a lens",
      tags=["macro", "extension tube", "close up", "lens spacer", "camera accessory", "photography"])
def _(S):
    tube = poly([(3, 4), (8, 4), (8, 7), (16, 7), (16, 4), (21, 4), (21, 20), (16, 20), (16, 17), (8, 17), (8, 20), (3, 20)],
                closed=True, r=S.r * 0.4)
    return [shell(tube), detail(seg(8.5, 12, 15.5, 12))]


@icon("lens-adapter", CAT, "Stepped ring adapter with a wide flange on one end and a narrower mount on the other",
      tags=["adapter", "mount adapter", "lens ring", "converter", "camera accessory", "bayonet"])
def _(S):
    body = poly([(3, 4), (10, 4), (10, 7), (21, 7), (21, 17), (10, 17), (10, 20), (3, 20)], closed=True, r=S.r * 0.4)
    return [shell(body), detail(seg(15.5, 7.5, 15.5, 16.5))]


@icon("teleconverter", CAT, "Short stubby cylinder with a glass element in its middle, fitted between lens and camera",
      tags=["teleconverter", "extender", "lens", "telephoto", "magnifier", "camera accessory"])
def _(S):
    body = poly([(2, 9), (5, 9), (5, 5), (19, 5), (19, 9), (22, 9), (22, 15), (19, 15), (19, 19), (5, 19), (5, 15), (2, 15)],
                closed=True, r=S.r * 0.4)
    return [shell(body), detail("M12 8C15 10 15 14 12 16C9 14 9 10 12 8Z")]


def _chords(cx, cy, r, offs, deg=-45):
    a = math.radians(deg)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    out = []
    for d in offs:
        h = math.sqrt(max(r * r - d * d, 0))
        x, y = cx + nx * d, cy + ny * d
        out.append(seg(x - ux * h, y - uy * h, x + ux * h, y + uy * h))
    return out


@icon("polarizing-filter", CAT, "Round screw on filter with an outer ring and parallel diagonal lines across the glass",
      tags=["polarizer", "cpl", "filter", "lens filter", "glare", "photography"])
def _(S):
    parts = [shell(circle(12, 12, 9))]
    parts += [detail(c) for c in _chords(12, 12, 6.2, [-4, 0, 4])]
    return parts


def _graduated_filled():
    plate = P(rect(2, 2, 20, 20, 2))
    return D(plate, P(rect(4, 12, 16, 8, 1)))


def _graduated_filled():
    return D(P(rect(2, 2, 20, 20, 3)), P(rect(4, 12, 16, 8, 1)))


@icon("graduated-filter", CAT, "Square filter plate that is dark across the top half and clear across the bottom half",
      tags=["graduated nd", "grad filter", "filter", "sky", "landscape photography", "lens filter"],
      filled=_graduated_filled)
def _(S):
    r = rr(S, 4)
    top = path_to_d(I(P(rect(3, 3, 18, 18, r)), P(rect(0, 0, 24, 11))))
    return [shell(rect(3, 3, 18, 18, r)), solid(top)]


def _nd_glass():
    return path_to_d(D(P(circle(12, 12, 5.5)), ST(seg(8.6, 9.6, 10.6, 7.6), 1.4, "round", "round")))


def _nd_filled():
    ring = D(P(circle(12, 12, 10)), P(circle(12, 12, 7.5)))
    return U(ring, P(_nd_glass()))


def _nd_glass(S=None):
    g = seg(8.6, 9.6, 10.6, 7.6) if S is None or S.name == "rounded" else poly([(8, 11), (8, 8), (11, 8)])
    if S is None or S.name == "rounded":
        g = arc(12, 12, 3.8, 200, 265)
    return path_to_d(D(P(circle(12, 12, 5.5)), ST(g, 1.4, "round" if S is None or S.name == "rounded" else "butt", "round" if S is None or S.name == "rounded" else "miter")))


def _nd_filled():
    ring = D(P(circle(12, 12, 10)), P(circle(12, 12, 7.5)))
    return U(ring, P(_nd_glass()))


@icon("nd-filter", CAT, "Round screw on filter with a solid dark glass and a small glint of light",
      tags=["neutral density", "nd filter", "filter", "long exposure", "dark glass", "lens filter"],
      filled=_nd_filled)
def _(S):
    return [shell(circle(12, 12, 9)), solid(_nd_glass(S))]


@icon("matte-box", CAT, "Bellows and hood with a tilted flap mounted in front of a camera lens",
      tags=["matte box", "lens hood", "flag", "film camera", "cinema", "shade"])
def _(S):
    return [
        shell(rect(2, 9, 4, 6, rr(S, 1.5))),
        shell(poly([(7, 9.5), (12, 7.5), (12, 16.5), (7, 14.5)], closed=True, r=S.r * 0.4)),
        shell(rect(12.5, 6.5, 9, 11, rr(S, 2))),
        line(poly([(12.5, 6.5), (14, 3), (21, 3)], r=S.r * 0.5)),
    ]


@icon("follow-focus", CAT, "Large round focus knob with a small gear meshing with a toothed lens ring",
      tags=["follow focus", "focus puller", "gear", "knob", "cine lens", "film camera"])
def _(S):
    return [
        shell(circle(8, 12, 6)),
        sq(6.5, 10.5, 3, 3) if S.name == "line" else dot(8, 12, 1.6),
        sq(14.5, 8, 2, 2, L(S, 0, 0.6)), sq(14.5, 14, 2, 2, L(S, 0, 0.6)),
        shell(rect(17, 3, 5, 18, rr(S, 2.5))),
    ]

# ============================================================================ optics, effects and accessories

@icon("lens-flare", CAT, "Bright four point star in the corner with a diagonal line of smaller circles trailing away from it",
      tags=["flare", "sun flare", "light streak", "glare", "lens effect", "photography"])
def _(S):
    star = []
    for i in range(8):
        r = 5.5 if i % 2 == 0 else 1.7
        a = math.radians(-90 + i * 45)
        star.append((8 + r * math.cos(a), 8 + r * math.sin(a)))
    return [
        shell(poly(star, closed=True, r=S.r * 0.3), stroke_miterlimit="1.5"),
        dot(14, 14, 1.4),
        shell(circle(18.5, 18.5, 2.5)),
    ]


@icon("lens-cleaning-pen", CAT, "Pen shaped cleaning tool with a soft brush at one end and a round felt tip at the other",
      tags=["lens pen", "cleaning", "brush", "camera care", "dust", "lens cleaner"])
def _(S):
    def R(pts, closed=True, r=0.0):
        return poly(rot(pts, 45, 12, 12), closed=closed, r=r)

    def RS(a, b):
        (x1, y1), (x2, y2) = rot([a, b], 45, 12, 12)
        return seg(x1, y1, x2, y2)
    return [
        line(RS((12, 6.5), (9, 2))), line(RS((12, 6.5), (12, 1.5))), line(RS((12, 6.5), (15, 2))),
        shell(R([(9.5, 7), (14.5, 7), (14.5, 16), (9.5, 16)], r=S.r * 0.5)),
        shell(R([(10.5, 16), (13.5, 16), (13.5, 19), (12, 21.5), (10.5, 19)], r=S.r * 0.3)),
    ]


def _ring(cx, cy, r, w=2.0):
    return D(P(circle(cx, cy, r + w / 2)), P(circle(cx, cy, r - w / 2)))


def _chroma_filled():
    return U(_ring(10.5, 12, 8), _ring(13.5, 12, 8))


@icon("chromatic-aberration", CAT, "Circle outline drawn twice slightly offset so a thin double edge fringe shows on one side",
      tags=["fringing", "color fringe", "lens defect", "optics", "aberration", "purple fringing"],
      filled=_chroma_filled)
def _(S):
    return [shell(circle(10.5, 12, 8)), line(arc(13.5, 12, 8, -55, 55))]


@icon("barrel-distortion", CAT, "Square grid whose lines bulge outward toward the edges like the side of a barrel",
      tags=["distortion", "lens distortion", "fisheye", "grid", "optics", "wide angle"])
def _(S):
    frame = "M4 4Q12 2 20 4Q22 12 20 20Q12 22 4 20Q2 12 4 4Z"
    return [
        shell(frame),
        detail("M9.3 3.3Q7.3 12 9.3 20.7"),
        detail("M14.7 3.3Q16.7 12 14.7 20.7"),
        detail("M3.3 9.3Q12 7.3 20.7 9.3"),
        detail("M3.3 14.7Q12 16.7 20.7 14.7"),
    ]


@icon("field-of-view", CAT, "Small camera on the left with two lines opening into a wide cone and an arc marking the angle",
      tags=["fov", "angle of view", "coverage", "camera angle", "view cone", "optics"])
def _(S):
    return [
        shell(rect(2, 9, 6, 6, rr(S, 1.5))),
        line(poly([(21, 4), (9.5, 12), (21, 20)], r=S.r * 0.3)),
        line(arc(9.5, 12, 7, -40, 40)),
    ]


@icon("rack-focus", CAT, "A solid sharp shape in front of a dashed soft shape behind it, marking a shift of focus",
      tags=["focus pull", "pull focus", "depth of field", "cinematography", "sharp and blurry", "film"])
def _(S):
    far = [line(arc(17, 7.5, 4.25, a, a + 45)) for a in (0, 90, 180, 270)]
    return far + [solid(circle(7.5, 16, 4.5))]


@icon("focus-peaking", CAT, "Flower in a viewfinder frame with its edge traced by a ring of small bright dots",
      tags=["peaking", "manual focus", "viewfinder", "sharpness", "focus assist", "camera"])
def _(S):
    parts = [
        line(poly([(2, 7), (2, 2.5), (6.5, 2.5)])), line(poly([(17.5, 2.5), (22, 2.5), (22, 7)])),
        line(poly([(2, 17), (2, 21.5), (6.5, 21.5)])), line(poly([(17.5, 21.5), (22, 21.5), (22, 17)])),
        dot(12, 10, 1.6),
    ]
    for k in range(6):
        a = math.radians(60 * k)
        parts.append(dot(12 + 5 * math.cos(a), 10 + 5 * math.sin(a), 1.15))
    parts.append(line(seg(12, 15.5, 12, 19.5)))
    return parts


@icon("focus-stacking", CAT, "Stack of offset image layers with a small flower on the front layer",
      tags=["focus stack", "macro", "layers", "depth of field", "merge", "photography"])
def _(S):
    return [
        line(poly([(6, 6), (6, 3.5), (20, 3.5), (20, 15)], r=S.r * 0.3)),
        shell(rect(3, 8, 15, 13, rr(S, 2))),
        dot(10.5, 14.5, 1.3), dot(10.5, 11.5, 1.1), dot(13.5, 14.5, 1.1), dot(10.5, 17.5, 1.1), dot(7.5, 14.5, 1.1),
    ]


@icon("camera-strap", CAT, "Camera body with a wide padded strap rising from both ends and meeting above it",
      tags=["neck strap", "shoulder strap", "camera", "carry", "accessory", "photography"])
def _(S):
    return [
        shell(poly([(4, 13), (10.5, 3), (13.5, 3), (20, 13), (16, 13), (12, 7.5), (8, 13)], closed=True, r=S.r * 0.5)),
        shell(rect(2, 15, 20, 7, rr(S, 3))),
        dot(12, 18.5, 1.4),
    ]


@icon("hot-shoe", CAT, "Close view of a camera top with a flat accessory slot rail and a center contact dot",
      tags=["flash mount", "accessory shoe", "camera top", "flash", "mount", "camera"])
def _(S):
    return [
        shell(rect(3, 4, 18, 16, rr(S, 3))),
        detail(poly([(7.5, 16), (7.5, 8.5), (16.5, 8.5), (16.5, 16)], r=S.r * 0.4)),
        dot(12, 12.5, 1.25),
    ]


@icon("camera-mode-dial", CAT, "Round ridged dial seen from above with small marks around it and a pointer line",
      tags=["mode dial", "dial", "camera settings", "program dial", "knob", "camera"])
def _(S):
    pts = []
    for i in range(32):
        r = 9.5 if i % 2 == 0 else 8.6
        a = math.radians(-90 + i * 360 / 32)
        pts.append((12 + r * math.cos(a), 12 + r * math.sin(a)))
    parts = [shell(poly(pts, closed=True, r=S.r * 0.3)), line(seg(12, 12, 12, 8))]
    for k in range(1, 8):
        a = math.radians(-90 + 45 * k)
        parts.append(dot(12 + 5.6 * math.cos(a), 12 + 5.6 * math.sin(a), 0.95))
    return parts


@icon("articulating-screen", CAT, "Camera back with its screen swung out to the side on a hinge and tilted",
      tags=["flip screen", "vari-angle screen", "selfie screen", "lcd", "vlog camera", "camera"])
def _(S):
    screen = rot([(16, 6), (22, 6), (22, 16), (16, 16)], 14, 15, 11)
    return [
        shell(rect(2, 5, 11, 15, rr(S, 2.5))),
        dot(7.5, 9, 1.2), dot(7.5, 12.5, 1.2), dot(7.5, 16, 1.2),
        shell(poly(screen, closed=True, r=S.r * 0.4)),
    ]


@icon("camera-rain-cover", CAT, "Camera wrapped in a loose hooded sleeve with rain falling on top",
      tags=["rain sleeve", "weather protection", "waterproof", "camera cover", "rain", "outdoor photography"])
def _(S):
    return [
        shell("M3 21V14C3 10 7 8.5 12 8.5C17 8.5 21 10 21 14V21Z"),
        detail(circle(12, 15, 2.5)),
        line(seg(6, 2, 5, 5)), line(seg(12, 2, 11, 5)), line(seg(18, 2, 17, 5)),
    ]


def _cage_filled():
    frame = D(P(rect(2, 7, 20, 14, 2)), P(rect(5, 10, 14, 8, 1)))
    cam = D(P(rect(7.5, 11.5, 9, 5, 1)), P(circle(12, 14, 1.2)))
    handle = ST("M8 7V3.5H16V7", 2.5, "butt", "miter")
    return U(frame, cam, handle)


@icon("camera-cage", CAT, "Camera body enclosed by a rectangular metal frame with a handle across the top",
      tags=["cage", "camera rig", "filmmaking", "video rig", "frame", "mounting"], filled=_cage_filled)
def _(S):
    return [
        line(poly([(8, 7), (8, 3.5), (16, 3.5), (16, 7)], r=S.r * 0.4)),
        shell(rect(3, 7, 18, 14, rr(S, 2.5))),
        shell(rect(7.5, 11, 9, 6, rr(S, 1.5))),
        dot(12, 14, 1.2),
    ]


@icon("quick-release-plate", CAT, "Flat mounting plate with a captive screw near the top and slanted dovetail edges at the sides",
      tags=["tripod plate", "camera plate", "dovetail", "mount", "tripod head"])
def _(S):
    return [
        shell(rect(6, 3, 12, 18, rr(S, 2.5))),
        line(poly([(6, 7), (3, 10), (3, 14), (6, 17)], r=S.r * 0.3)),
        line(poly([(18, 7), (21, 10), (21, 14), (18, 17)], r=S.r * 0.3)),
        dot(12, 8, 2),
        detail(seg(9.5, 15, 14.5, 15)),
    ]


# ============================================================================ power, charts and rigs

@icon("camera-brick-battery", CAT, "Large brick battery with a stack of level bars and a tapered mounting plate on its base",
      tags=["battery pack", "power", "cinema camera", "charge level", "film set"])
def _(S):
    body = union(rect(4, 2.5, 16, 15, rr(S, 3)), poly([(6, 17), (18, 17), (16, 21.5), (8, 21.5)], closed=True))
    return [
        shell(body),
        detail(seg(5.5, 17.5, 18.5, 17.5)),
        sq(8, 6, 8, 2), sq(8, 9.5, 8, 2), sq(8, 13, 8, 2),
    ]


def _wedge(cx, cy, r, a0, a1):
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    return f"M{fmt(cx)} {fmt(cy)}L{fmt(x0)} {fmt(y0)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(y1)}Z"


@icon("star-test-chart", CAT, "Square focus chart with a round star of alternating dark and light wedges meeting in the center",
      tags=["star chart", "focus chart", "resolution chart", "test pattern", "calibration", "lens test"])
def _(S):
    parts = [shell(rect(2, 2, 20, 20, rr(S, 3)))]
    for k in range(4):
        parts.append(Part("dot", _wedge(12, 12, 7.5, 90 * k, 90 * k + 45)))
    return parts


@icon("crop-factor", CAT, "A large outer frame with a smaller inner frame in its corner and a small diagonal arrow between their corners",
      tags=["sensor size", "crop sensor", "full frame", "aps-c", "focal length equivalent", "camera sensor"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, rr(S, 3))),
        detail(rect(11.5, 11, 7.5, 6.5, rr(S, 1))),
        line(seg(5, 6, 8.5, 9.5)),
        line(poly([(5.5, 9.5), (8.5, 9.5), (8.5, 6.5)])),
    ]


@icon("slr-cross-section", CAT, "Cut away of an SLR camera showing the lens, an angled mirror and the prism leading to the eyepiece",
      tags=["mirror", "pentaprism", "viewfinder", "how a camera works", "optics", "cutaway"])
def _(S):
    body = union(rect(8, 10, 14, 10, rr(S, 2)), poly([(10.5, 10), (14, 4.5), (20, 4.5), (20, 10)], closed=True))
    return [
        shell(rect(2, 9, 5, 12, rr(S, 1.5))),
        shell(body),
        detail(seg(10.5, 18, 15, 13.5)),
        detail(seg(20, 12.5, 20, 18)),
    ]


@icon("smartphone-video-rig", CAT, "Phone held sideways in a handled frame with a microphone and a light mounted on top",
      tags=["phone rig", "vlogging", "mobile filmmaking", "video", "smartphone", "creator"])
def _(S):
    return [
        solid(rect(5, 3, 3.5, 5)),
        solid(rect(14, 3, 6, 5, L(S, 0, 1))),
        shell(rect(3, 8, 18, 11, rr(S, 2.5))),
        detail(rect(6.5, 11.5, 11, 4, rr(S, 1))),
        line(seg(6, 19, 6, 22)), line(seg(18, 19, 18, 22)),
    ]


@icon("phone-clip-lens", CAT, "Phone with a clip on lens sitting over its camera at one corner",
      tags=["phone lens", "macro lens", "wide lens", "mobile photography", "clip lens", "smartphone camera"])
def _(S):
    body = union(rect(9, 2, 13, 20, rr(S, 3)), circle(9.5, 8.5, 4.5))
    return [shell(body), detail(circle(9.5, 8.5, 1.8)), sq(15.5, 18, 3, 1.5)]


@icon("shoulder-rig", CAT, "Camera on a rail over a curved shoulder pad with two hand grips below",
      tags=["shoulder mount", "documentary", "camera support", "filmmaking", "handheld rig", "video"])
def _(S):
    return [
        shell(rect(9, 3, 9, 7, rr(S, 2))),
        shell(rect(18, 5, 3.5, 3.5, rr(S, 1))),
        line(seg(12, 10, 12, 14)), line(seg(16, 10, 16, 14)),
        line(seg(6, 14, 22, 14)),
        shell("M6 10.5C1.5 10.5 1.5 21 6 21Z"),
        shell(rect(11, 16.5, 3, 5.5, rr(S, 1.5))), shell(rect(17, 16.5, 3, 5.5, rr(S, 1.5))),
    ]


@icon("camera-stabilizer-vest", CAT, "Body vest with a spring arm holding a camera on a vertical post with a weight at the bottom",
      tags=["stabilizer", "body mount", "smooth shot", "camera operator", "film"])
def _(S):
    return [
        shell(poly([(2, 7), (4, 3.5), (8, 3.5), (10, 7), (10, 21), (2, 21)], closed=True, r=S.r * 0.6)),
        line(poly([(10, 12), (17, 12)])),
        line(seg(17, 9, 17, 18)),
        shell(rect(13.5, 3, 8, 5.5, rr(S, 1.5))),
        dot(17, 19.5, 2.2),
    ]


@icon("suction-cup-mount", CAT, "Large round suction cup pad with a short jointed arm holding a small camera",
      tags=["car mount", "suction mount", "window mount", "action camera", "vehicle camera", "mount"])
def _(S):
    return [
        shell(poly([(3, 21), (6, 16.5), (18, 16.5), (21, 21)], closed=True, r=S.r)),
        line(seg(12, 16.5, 12, 12)),
        dot(12, 11.5, 1.5),
        line(seg(12, 11.5, 16, 8.5)),
        shell(rect(13, 2.5, 8.5, 6, rr(S, 1.5))),
    ]


@icon("cable-cam", CAT, "Camera hanging from a small carriage on cables stretched from tall corner posts",
      tags=["wire camera", "aerial camera", "stadium camera", "suspended camera", "sports broadcast"])
def _(S):
    return [
        line(seg(3, 2.5, 3, 22)), line(seg(21, 2.5, 21, 22)),
        line(seg(3, 4, 10, 8.5)), line(seg(21, 4, 14, 8.5)),
        shell(rect(9, 8.5, 6, 3, rr(S, 1))),
        line(seg(12, 11.5, 12, 14)),
        shell(rect(8.5, 14, 7, 6, rr(S, 2))),
    ]


@icon("camera-car", CAT, "Car side view with a long arm reaching out from its roof and holding a camera ahead of it",
      tags=["tracking vehicle", "crane car", "car shot", "film", "camera arm", "chase scene"])
def _(S):
    return [
        shell(poly([(2, 19), (2, 15), (5, 15), (7.5, 11.5), (12, 11.5), (14.5, 15), (16, 15), (16, 19)], closed=True, r=S.r * 0.5)),
        dot(5.5, 19.5, 2.2), dot(12.5, 19.5, 2.2),
        line(poly([(9.5, 11.5), (9.5, 6), (18, 6)])),
        shell(rect(17, 8, 5, 5, rr(S, 1.2))),
    ]


@icon("robotic-camera-arm", CAT, "Industrial robot arm on a round base with jointed segments holding a camera at its tip",
      tags=["motion control", "robot arm", "automated camera", "industrial", "film", "camera rig"])
def _(S):
    return [
        shell(rect(2, 18, 10, 4, L(S, 0.5, 2))),
        line(seg(7, 18, 7, 14.5)),
        shell(circle(7, 13, 1.75)),
        line(seg(8.2, 11.7, 11.5, 7.3)),
        shell(circle(12.5, 6, 1.75)),
        line(seg(14.25, 6, 17, 6)),
        shell(rect(17, 3, 5, 6, L(S, 0.5, 2.5))),
    ]


@icon("apple-box", CAT, "Wooden box seen at an angle with a hand hole cut into its end",
      tags=["film set", "grip equipment", "crate", "riser", "step", "prop"])
def _(S):
    body = union(rect(2, 9.5, 14, 10.5, rr(S, 1.5)), poly([(2, 9.5), (6, 5.5), (20, 5.5), (16, 9.5)], closed=True),
                 poly([(16, 9.5), (20, 5.5), (20, 16), (16, 20)], closed=True))
    return [shell(body, stroke_miterlimit="2"), detail(seg(16, 10, 16, 19.5)), detail(seg(2.5, 9.5, 16, 9.5)),
            Part("dot", rect(6, 12.5, 6, 3, 1.5))]


@icon("c-stand", CAT, "Stand with three spread legs, a tall column and a side arm with a clamp at the top",
      tags=["century stand", "grip stand", "light stand", "film set", "gobo arm", "support"])
def _(S):
    return [
        line(seg(12, 18, 12, 4)),
        line(seg(12, 18, 3, 21.5)), line(seg(12, 18, 21, 21.5)), line(seg(12, 18, 12, 22)),
        shell(rect(10, 4, 4, 4, rr(S, 1))),
        line(seg(14, 6, 22, 6)),
    ]


@icon("copy-stand", CAT, "Flat baseboard with an upright column holding a camera that points straight down at the board",
      tags=["reproduction stand", "document camera", "overhead camera", "digitising", "flat lay", "scanner"])
def _(S):
    return [
        shell(rect(2, 19, 20, 3, rr(S, 1))),
        line(seg(5, 19, 5, 3.5)),
        line(seg(5, 3.5, 13, 3.5)),
        shell(rect(9.5, 6, 7, 5, rr(S, 1.5))),
        line(seg(11, 13, 8.5, 17)), line(seg(15, 13, 17.5, 17)),
    ]


@icon("photo-turntable", CAT, "Low round rotating platform with a small product box on top and a curved arrow beneath",
      tags=["360 photography", "product photography", "spin", "rotating stand", "lazy susan", "display"])
def _(S):
    return [
        shell(rect(9, 4, 6, 6, rr(S, 1.5))),
        shell(rect(3, 11, 18, 4, rr(S, 2))),
        line("M4 18.5Q12 22.5 20 18.5"),
        line(poly([(17, 17), (20.3, 18.3), (19.5, 21.5)])),
    ]


# ============================================================================ stage and studio lighting

def _star4(cx, cy, ro, ri):
    pts = []
    for i in range(8):
        r = ro if i % 2 == 0 else ri
        a = math.radians(-90 + i * 45)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


@icon("star-tracker-mount", CAT, "Tripod top with a tilted wedge mount holding a camera, aimed toward a small star",
      tags=["astrophotography", "night sky", "equatorial mount", "tripod", "milky way", "astronomy camera"])
def _(S):
    return [
        solid(poly(_star4(19, 5.5, 3.5, 1.1), closed=True)),
        shell(rect(3, 3.5, 9, 5.5, rr(S, 1.5))),
        line(seg(7.5, 9, 7.5, 11.5)),
        shell(poly([(4, 17), (12, 17), (12, 12)], closed=True, r=S.r * 0.4)),
        line(seg(8, 17, 4, 22)), line(seg(8, 17, 12, 22)), line(seg(8, 17, 8, 22)),
    ]


@icon("fresnel-light", CAT, "Stage light seen from the front with concentric stepped lens rings and two tilted barn door flaps",
      tags=["fresnel", "stage lamp", "barn doors", "studio light", "theatre lighting", "spotlight"])
def _(S):
    return [
        line(poly([(5, 5), (3.5, 2.5), (20.5, 2.5), (19, 5)])),
        line(poly([(5, 19), (3.5, 21.5), (20.5, 21.5), (19, 19)])),
        shell(rect(5, 5, 14, 14, rr(S, 3))),
        detail(circle(12, 12, 4)),
        dot(12, 12, 1.4),
    ]


@icon("ellipsoidal-spotlight", CAT, "Long narrow spotlight barrel with a lens tube in front, shutter handles on top and a yoke below",
      tags=["profile spot", "stage spotlight", "theatre lighting", "shutter", "gobo projector"])
def _(S):
    return [
        shell(rect(2, 8, 13, 8, rr(S, 2.5))),
        shell(rect(16, 9, 5, 6, rr(S, 1.5))),
        line(seg(7, 8, 7, 4.5)), line(seg(11, 8, 11, 5.5)),
        line(poly([(5, 16), (7, 20.5), (13, 20.5), (15, 16)], r=S.r * 0.4)),
    ]


@icon("moving-head-light", CAT, "Round light head resting in a U shaped yoke above a square base with a narrow beam rising from it",
      tags=["intelligent light", "dmx", "concert lighting", "stage light", "robotic light", "dj light"])
def _(S):
    return [
        solid(poly([(10.8, 7), (13.2, 7), (15.5, 2), (8.5, 2)], closed=True)),
        line("M5.5 11.5V13Q5.5 16.5 12 16.5Q18.5 16.5 18.5 13V11.5"),
        shell(circle(12, 11.5, 3)),
        shell(rect(8, 17.5, 8, 4.5, rr(S, 1.5))),
    ]


@icon("follow-spot", CAT, "Long cylindrical spotlight on a tall stand with a rear handle and a single narrow beam",
      tags=["spot operator", "theatre", "stage spotlight", "concert", "limelight", "beam"])
def _(S):
    return [
        shell(rect(4, 7, 12, 6, rr(S, 2))),
        line(poly([(4, 10), (1.5, 10)])), line(seg(1.5, 8, 1.5, 12)),
        solid(poly([(17.5, 9.5), (22, 8), (22, 12)], closed=True)),
        line(seg(9, 13, 9, 21.5)),
        line(seg(5, 21.5, 13, 21.5)),
    ]


@icon("footlights", CAT, "Row of small hooded lamps along the front edge of a stage floor shining upward",
      tags=["stage lights", "floor lights", "theatre", "footlight", "stage edge", "lamps"])
def _(S):
    parts = [line(seg(2, 20.5, 22, 20.5))]
    for x in (5, 12, 19):
        parts.append(solid(f"M{x - 3} 19.5A3 3.5 0 0 1 {x + 3} 19.5Z"))
        parts.append(line(seg(x, 13.5, x, 9)))
    return parts


@icon("lighting-console", CAT, "Sloped control desk with a row of vertical fader sliders and a small screen above them",
      tags=["lighting desk", "light board", "dimmer", "faders", "stage control", "dmx controller"])
def _(S):
    return [
        shell(rect(7, 2.5, 10, 5, rr(S, 1))),
        shell(poly([(2, 21), (5, 11), (19, 11), (22, 21)], closed=True, r=S.r * 0.5)),
        detail(seg(8.5, 13.5, 8.5, 18.5)), detail(seg(12, 13.5, 12, 18.5)), detail(seg(15.5, 13.5, 15.5, 18.5)),
        sq(7, 14, 3, 1.5), sq(10.5, 16.5, 3, 1.5), sq(14, 15, 3, 1.5),
    ]


@icon("lighting-plot", CAT, "Top down stage outline with small light symbols arranged along a bar above it",
      tags=["light plot", "lighting design", "stage plan", "rigging plan", "theatre", "diagram"])
def _(S):
    parts = [
        line(seg(3, 4, 21, 4)),
        shell(rect(3, 12, 18, 9, rr(S, 2.5))),
        dot(12, 16.5, 1.4),
    ]
    for x in (6.5, 12, 17.5):
        parts.append(solid(poly([(x - 1.8, 6), (x + 1.8, 6), (x + 1.2, 9.5), (x - 1.2, 9.5)], closed=True)))
    return parts


_LEAF = "M12 3.8C15 5.5 15 9 12 12C9 9 9 5.5 12 3.8Z"
_LEAF_S = "M12 17C14.2 18 14.2 20.2 12 21.5C9.8 20.2 9.8 18 12 17Z"


_LEAF_S = "M12 17C14.2 18 14.2 20.2 12 21.5C9.8 20.2 9.8 18 12 17Z"


@icon("gobo", CAT, "Round metal disc with a leaf shaped cut out and the same leaf shape projected as light below",
      tags=["light template", "pattern projection", "stencil", "breakup", "stage lighting", "leaf shadow"])
def _(S):
    if S.name == "line":
        leaf = "M12 3.8L15 7.2L12 12L9 7.2Z"
    else:
        leaf = path_to_d(P(ellipse(12, 8, 2.6, 3.8)))
    return [shell(circle(12, 8, 6.5)), Part("dot", leaf), solid(_LEAF_S)]


@icon("lighting-gel", CAT, "Stage lamp with a colored square filter sheet held in a frame at its front",
      tags=["color filter", "colour gel", "stage lamp", "theatre lighting", "tint", "filter sheet"])
def _(S):
    return [
        shell(poly([(2, 10), (9, 8), (9, 16), (2, 14)], closed=True, r=S.r * 0.4)),
        shell(rect(12, 5, 9, 14, rr(S, 1.5))),
        Part("dot", rect(15, 8, 3, 8)),
    ]


@icon("snoot", CAT, "Light head with a long narrowing tube on its front that makes a small round spot",
      tags=["light modifier", "spot", "narrow beam", "studio lighting", "tube", "photography light"])
def _(S):
    return [
        shell(rect(2, 6, 8, 12, rr(S, 2.5))),
        shell(poly([(10, 8), (16, 10.5), (16, 13.5), (10, 16)], closed=True, r=S.r * 0.3)),
        dot(20.5, 12, 1.5),
    ]


@icon("honeycomb-grid", CAT, "Round disc filled with a hexagonal honeycomb pattern that fits over a light reflector",
      tags=["grid", "light grid", "honeycomb", "beam control", "reflector", "studio lighting"])
def _(S):
    hexp = [(12 + 3.6 * math.cos(math.radians(-90 + 60 * k)), 12 + 3.6 * math.sin(math.radians(-90 + 60 * k))) for k in range(6)]
    parts = [shell(circle(12, 12, 9)), detail(poly(hexp, closed=True, r=S.r * 0.8))]
    for k in range(6):
        a = math.radians(-90 + 60 * k)
        parts.append(detail(seg(12 + 3.6 * math.cos(a), 12 + 3.6 * math.sin(a), 12 + 8 * math.cos(a), 12 + 8 * math.sin(a))))
    return parts


@icon("lantern-softbox", CAT, "Round paper lantern shaped ball light hanging from the end of a long boom pole",
      tags=["chinese lantern", "ball light", "soft light", "boom pole", "film lighting", "diffuser"])
def _(S):
    return [
        line(poly([(3.5, 22), (3.5, 3.5), (15.5, 3.5), (15.5, 7)])),
        shell(ellipse(15.5, 13.5, 5.5, 6.5)),
        detail(ellipse(15.5, 13.5, 1.6, 4.6)),
    ]


@icon("lighting-flag", CAT, "Black rectangular panel on an arm clamped to a stand, used to block part of a light",
      tags=["flag", "cutter", "negative fill", "shade", "film lighting", "grip"])
def _(S):
    return [
        solid(rect(11, 4, 10, 12, L(S, 0, 1.5))),
        line(seg(5, 10, 11, 10)),
        dot(5, 10, 1.7),
        line(seg(5, 10, 5, 21.5)),
        line(seg(2, 21.5, 8, 21.5)),
    ]


@icon("butterfly-frame", CAT, "Large square fabric frame held overhead on two tall stands with the sun and its rays above it",
      tags=["silk", "overhead", "diffusion frame", "sun diffuser", "outdoor lighting", "film set"])
def _(S):
    return [
        dot(12, 4, 2),
        line(seg(4.5, 4, 8, 4)), line(seg(16, 4, 19.5, 4)),
        shell(rect(2.5, 9, 19, 6.5, rr(S, 2.5))),
        detail(seg(12, 9.5, 12, 15)),
        line(seg(6, 16, 6, 22)), line(seg(18, 16, 18, 22)),
    ]

@icon("cucoloris", CAT, "Board with irregular cut out holes held in front of a light, casting a dappled pattern below",
      tags=["cookie", "kukaloris", "dappled light", "shadow pattern", "film lighting", "breakup"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 10, rr(S, 2.5))),
        Part("dot", circle(8, 7, 1.8)),
        Part("dot", ellipse(14.5, 8.5, 2.5, 1.7)),
        Part("dot", circle(16.5, 5, 1.2)),
        dot(5.5, 18, 1.3), dot(11, 17, 1.6), dot(16, 19, 1.2), dot(19.5, 16.5, 1),
    ]


@icon("studio-strobe", CAT, "Studio flash head with a flared reflector bowl and a vented back, standing on a stand",
      tags=["monolight", "flash head", "studio flash", "strobe", "photography light", "reflector"])
def _(S):
    return [
        shell(rect(2, 7, 8, 9, rr(S, 2))),
        detail(seg(4.5, 10, 7.5, 10)), detail(seg(4.5, 13, 7.5, 13)),
        shell(poly([(10, 9), (16, 4.5), (16, 18.5), (10, 14)], closed=True, r=S.r * 0.4)),
        dot(13, 11.5, 1.3),
        line(seg(6, 16, 6, 21.5)), line(seg(2, 21.5, 10, 21.5)),
    ]


@icon("flash-diffuser", CAT, "Hot shoe flash unit with a rounded translucent dome cap over its head",
      tags=["flash", "soft light", "dome diffuser", "bounce", "photography accessory"])
def _(S):
    body = union("M6 8C6 2.5 18 2.5 18 8Z", rect(6, 8, 12, 6, rr(S, 1.5)), rect(9, 13, 6, 8, rr(S, 1)))
    return [shell(body), detail(seg(6.5, 8, 17.5, 8)), line(seg(8, 22, 16, 22))]


@icon("led-light-tube", CAT, "Slim handheld light wand held upright with a glowing tube and rays at both sides",
      tags=["light wand", "tube light", "led", "video light", "creative lighting"])
def _(S):
    parts = [
        shell(rect(9.5, 2.5, 5, 13.5, rr(S, 2.5))),
        shell(rect(10.5, 17, 3, 5, rr(S, 1.5))),
        detail(seg(12, 5.5, 12, 13)),
    ]
    for y in (6, 10, 14):
        parts += [line(seg(3, y, 6, y)), line(seg(18, y, 21, y))]
    return parts


@icon("audience-blinder", CAT, "Rectangular panel with a two by two grid of round bright lamps and rays shining out of the top",
      tags=["blinder", "stage light", "concert lighting", "crowd light", "par bank", "theatre lighting"])
def _(S):
    parts = [shell(rect(4, 8, 16, 13, rr(S, 3))),
             line(seg(6.5, 5, 5, 2)), line(seg(12, 5, 12, 2)), line(seg(17.5, 5, 19, 2))]
    for x in (9, 15):
        for y in (12.5, 17):
            parts.append(dot(x, y, 1.6))
    return parts


@icon("blacklight", CAT, "Long fluorescent tube in a fixture with short wavy lines radiating downward from it",
      tags=["uv light", "black light", "ultraviolet", "glow", "neon", "party light"])
def _(S):
    parts = [shell(rect(2, 3, 20, 8, rr(S, 3))), sq(5.5, 6, 13, 2, L(S, 0, 1))]
    for x in (6, 12, 18):
        parts.append(line(poly([(x, 14), (x + 1.6, 16.5), (x, 19), (x + 1.6, 21.5)], r=S.r * 0.8)))
    return parts


@icon("three-point-lighting", CAT, "Top down diagram with a subject circle in the middle and three lamps placed around it",
      tags=["key light", "fill light", "back light", "lighting setup", "portrait lighting", "studio diagram"])
def _(S):
    def lamp(cx, cy, deg):
        return solid(poly(rot([(cx - 2.5, cy - 1.75), (cx + 2.5, cy - 1.75), (cx + 2.5, cy + 1.75), (cx - 2.5, cy + 1.75)], deg, cx, cy), closed=True))
    return [
        shell(circle(12, 12, 3.2)),
        lamp(4.5, 4.5, 45), lamp(19.5, 4.5, 135), lamp(12, 20.5, -90),
        line(seg(7.3, 7.3, 8.8, 8.8)), line(seg(16.7, 7.3, 15.2, 8.8)), line(seg(12, 17.3, 12, 16)),
    ]


_FACE_O = lambda: P(ellipse(12, 12, 8, 10))
_NOSE = "M15 10.5L16.7 14L14.5 14.5"


def _split_filled():
    left = I(_FACE_O(), P(rect(0, 0, 12, 24)))
    ring = D(_FACE_O(), P(ellipse(12, 12, 6, 8)))
    return U(left, ring, ST(_NOSE, 2.5, "butt", "miter"))


@icon("split-lighting", CAT, "Face outline split down the middle with one half filled solid and the other half left open",
      tags=["portrait lighting", "dramatic light", "half face", "shadow", "chiaroscuro", "studio lighting"], filled=_split_filled)
def _(S):
    left = path_to_d(I(_FACE_O(), P(rect(0, 0, 12, 24))))
    return [shell(ellipse(12, 12, 7, 9)), solid(left), line(poly([(15, 10.5), (16.7, 14), (14.5, 14.5)], r=S.r * 0.5))]


def _eye_almond():
    return "M2 12C5 6.5 8.5 5 12 5C15.5 5 19 6.5 22 12C19 17.5 15.5 19 12 19C8.5 19 5 17.5 2 12Z"


def _catch_pupil(S=None):
    win = P(rect(11, 9.8, 2.4, 2.4, 0.7 if (S is None or S.name == "rounded") else 0))
    return path_to_d(D(P(circle(12, 12, 3.8)), win))


def _catch_filled():
    return U(D(P(_eye_almond()), P(circle(12, 12, 5.8))), P(_catch_pupil()))


@icon("catchlight", CAT, "Eye with a small square window shaped highlight reflected in its pupil",
      tags=["eye light", "portrait", "reflection", "softbox", "eye highlight", "photography"], filled=_catch_filled)
def _(S):
    return [shell(_eye_almond()), solid(_catch_pupil(S))]


@icon("color-temperature", CAT, "Horizontal scale with a flame at the warm end, a snowflake at the cool end and a pointer under it",
      tags=["white balance", "kelvin", "warm cool", "light colour", "tungsten daylight", "temperature scale"])
def _(S):
    return [
        solid("M5.5 10C2.5 10 2.5 6.5 4.2 4.8C4.8 6.5 5.6 6.2 5.2 2.8C8.5 4.5 8.8 10 5.5 10Z"),
        line(seg(19, 3.5, 19, 9.5)), line(seg(16.4, 5, 21.6, 8)), line(seg(16.4, 8, 21.6, 5)),
        shell(rect(2, 12, 20, 5, rr(S, 2))),
        detail(seg(8, 12.5, 8, 16.5)), detail(seg(14, 12.5, 14, 16.5)),
        solid(poly([(9.5, 22), (11, 19), (12.5, 22)], closed=True)),
    ]


@icon("flash-powder-lamp", CAT, "Old handheld flash pan on a stick with a bright burst and small puffs of smoke above it",
      tags=["magnesium flash", "vintage flash", "early photography", "flash pan", "smoke", "history"])
def _(S):
    return [
        solid(poly(_star4(12, 6.5, 5.5, 2.2) + [], closed=True)),
        shell(poly([(5, 13.5), (19, 13.5), (17, 16), (7, 16)], closed=True, r=S.r * 0.4)),
        line(seg(12, 16, 12, 22)),
        dot(4.5, 8, 1.5), dot(19.5, 8, 1.5),
    ]


@icon("orchestra-pit", CAT, "Stage floor with a sunken pit between its edges holding a conductor with a raised baton",
      tags=["theatre", "opera", "musicians", "conductor", "stage", "performance"])
def _(S):
    return [
        line(poly([(2, 8), (6, 8), (6, 21), (18, 21), (18, 8), (22, 8)])),
        dot(11, 13, 1.8),
        line(seg(11, 15.5, 11, 19)),
        line(poly([(11, 16.5), (14, 14), (16, 10.5)])),
    ]
