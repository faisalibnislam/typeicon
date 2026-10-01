"""TypeIcon Core: faces (batch 002): masks, characters and expressive faces.

Built like the emotions set: one outline (the r 9 face circle unless the icon needs its own head shape) with
features cut out of it in Filled. Line eyes are crisp upright bars and strokes end square; Rounded eyes are soft
ovals and strokes end round. Props that overlap the outline (hats, hands, cones) cut it with a clean gap;
attached parts (ribbons, horns, tongues) join the silhouette.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, Style, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "faces"
FILL = Style("filled", "round", "round", R=4.0, r=1.5)  # pseudo-style: feature geometry for the Filled design
FACE = circle(12, 12, 9)
GAP = 1.75


class Hole(Part):
    """Closed feature (open mouth): outline in Line/Rounded, cut out whole in Filled."""


class Inset(Part):
    """Stroke inside a Hole (teeth): detail in Line/Rounded, kept solid inside the Filled hole."""


class Keep(Part):
    """Solid mark that stays solid in Filled (a pupil inside an eye hole, a dark cap)."""


class Ext(Part):
    """Part attached to the outline (horns, ribbons, tongue): drawn normally, joined to the Filled silhouette."""


def hole(d):
    return Hole("detail", d, {})


def inset(d):
    return Inset("detail", d, {})


def keep(d):
    return Keep("dot", d, {})


def ext_line(d):
    return Ext("line", d, {})


def ext_shell(d):
    return Ext("shell", d, {})


def mark(d):
    """Solid feature (eye, tear): solid in Line/Rounded, cut out of the Filled face."""
    return Part("dot", d)


def L(S, a, b):
    return a if S.name == "line" else b


def eye(S, x, y=10, s=1.0):
    return mark(rect(x - 1.1 * s, y - 1.6 * s, 2.2 * s, 3.2 * s) if S.name == "line" else ellipse(x, y, 1.2 * s, 1.6 * s))


def eyes(S, y=10, dx=3):
    return [eye(S, 12 - dx, y), eye(S, 12 + dx, y)]


def almond(cx, cy, w, h, S):
    """Almond eye shape, pointed corners in Line, soft corners otherwise."""
    x0, x1 = cx - w / 2, cx + w / 2
    if S.name == "line":
        return (f"M{fmt(x0)} {fmt(cy)}Q{fmt(cx)} {fmt(cy - h)} {fmt(x1)} {fmt(cy)}"
                f"Q{fmt(cx)} {fmt(cy + h)} {fmt(x0)} {fmt(cy)}Z")
    k = 2 * h / 3
    return (f"M{fmt(x0)} {fmt(cy)}C{fmt(x0 + w * 0.12)} {fmt(cy - k)} {fmt(x1 - w * 0.12)} {fmt(cy - k)} {fmt(x1)} {fmt(cy)}"
            f"C{fmt(x1 - w * 0.12)} {fmt(cy + k)} {fmt(x0 + w * 0.12)} {fmt(cy + k)} {fmt(x0)} {fmt(cy)}Z")


def flip(d, cx=12):
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 2 * cx, 0)))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def rot(d, deg, cx=12, cy=12):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def _region(p):
    if p.kind == "shell" or isinstance(p, Hole):
        return U(P(p.d), ST(p.d, 2))
    if p.kind in ("line", "detail"):
        return ST(p.d, 2, "round", "round")
    return P(p.d)


def _solid(p):
    if p.kind == "shell":
        return U(P(p.d), ST(p.d, 2, "round", "round"))
    if p.kind == "line":
        return ST(p.d, 2.5, "round", "round")
    return P(p.d)


def _grow(path, g):
    return U(path, ST(path_to_d(path), 2 * g, "round", "round"))


def face(name, description, tags, aliases=(), over=None, outline=None):
    """Register a face. `fn(S)` returns the features; `over(S)` the props overlapping the outline."""
    def deco(fn):
        def draw(S):
            o = outline(S) if outline else FACE
            props = over(S) if over else []
            cutting = [p for p in props if p.kind != "detail"]
            if cutting:
                cutter = _grow(U(*[_region(p) for p in cutting]), GAP)
                ring = solid(path_to_d(D(ST(o, 2, S.cap, S.join), cutter)))
            else:
                ring = shell(o)
            return [ring, *fn(S), *props]

        def filled():
            o = outline(FILL) if outline else FACE
            body = U(P(o), ST(o, 2, "round", "round"))
            feats = fn(FILL)
            exts = [_solid(p) for p in feats if isinstance(p, Ext)]
            if exts:
                body = U(body, *exts)
            keeps = []
            for p in feats:
                if isinstance(p, Ext):
                    continue
                if isinstance(p, Keep):
                    keeps.append(P(p.d))
                elif isinstance(p, Inset):
                    keeps.append(ST(p.d, 2, "butt", "miter"))
                elif isinstance(p, Hole) or p.kind == "shell":
                    body = D(body, U(P(p.d), ST(p.d, 2)))
                elif p.kind in ("detail", "line"):
                    body = D(body, ST(p.d, 2, "round", "round"))
                else:
                    body = D(body, P(p.d))
            props = over(FILL) if over else []
            cutting = [p for p in props if p.kind != "detail"]
            extras = []
            if cutting:
                body = D(body, _grow(U(*[_region(p) for p in cutting]), GAP))
                pr = U(*[_solid(p) for p in cutting])
                knocks = [ST(p.d, 2, "round", "round") for p in props if p.kind == "detail"]
                if knocks:
                    pr = D(pr, *knocks)
                extras.append(pr)
            return U(body, *extras, *keeps)

        return icon(name, CAT, description, tags=tags, aliases=aliases, filled=filled)(draw)
    return deco


def drop(cx, top, r, cy):
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + r * 0.4)} {fmt(top + (cy - top) * 0.4)} {fmt(cx + r)} {fmt(cy - r * 0.5)} {fmt(cx + r)} {fmt(cy)}"
            f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx - r)} {fmt(cy)}"
            f"C{fmt(cx - r)} {fmt(cy - r * 0.5)} {fmt(cx - r * 0.4)} {fmt(top + (cy - top) * 0.4)} {fmt(cx)} {fmt(top)}Z")


def heart(cx, cy, s, S):
    sharp = "M12 20L4.4 12.6A4.6 4.6 0 0 1 11 6.3L12 7.3L13 6.3A4.6 4.6 0 0 1 19.6 12.6Z"
    soft = "M10.6 18.6L4.4 12.6A4.6 4.6 0 0 1 11 6.3L11.3 6.6Q12 7.3 12.7 6.6L13 6.3A4.6 4.6 0 0 1 19.6 12.6L13.4 18.6Q12 20 10.6 18.6Z"
    base = P(sharp if S.name == "line" else soft)
    m = (s, 0, 0, s, cx - 12 * s, cy - 12.6 * s)
    return path_to_d(transform_path(base, m))


def smooth_closed(pts):
    """Closed Catmull-Rom curve through pts as cubic segments."""
    n = len(pts)
    out = [f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"]
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        out.append(f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}")
    return "".join(out) + "Z"


# ============================================================================ masks

def _volto(S):
    if S.name == "line":
        return ("M12 2.5C16 2.5 17.5 5.5 17.5 9.5C17.5 14.5 15.5 19.5 12 21.5"
                "C8.5 19.5 6.5 14.5 6.5 9.5C6.5 5.5 8 2.5 12 2.5Z")
    return ("M12 2.5C16 2.5 17.5 5.5 17.5 9.5C17.5 14.5 15.5 19 13.2 20.9Q12 21.8 10.8 20.9"
            "C8.5 19 6.5 14.5 6.5 9.5C6.5 5.5 8 2.5 12 2.5Z")


@face("volto-mask", "Plain full face carnival mask with ribbon ties at the sides",
      ["mask", "venetian mask", "carnival", "masquerade", "costume", "theatre", "anonymous"], outline=_volto)
def _(S):
    rib = "M6.6 8.5C4 8.5 2.5 10 3 12.5C3.4 14.5 3.8 16.5 2.8 18.5"
    return [mark(almond(9.5, 9.5, 3.8, 2.6, S)), mark(almond(14.5, 9.5, 3.8, 2.6, S)),
            detail(poly([(12, 10.5), (12, 14.5), (11, 14.5)], r=L(S, 0, 0.5))),
            detail("M10.3 17.3Q12 18.2 13.7 17.3"),
            ext_line(rib), ext_line(flip(rib))]


def _bauta(S):
    return poly([(7, 8.5), (17, 8.5), (17, 15.5), (19, 19.5), (18, 21.5), (6, 21.5), (5, 19.5), (7, 15.5)], closed=True, r=S.r)


@face("bauta-mask", "Full face mask with a square jutting chin and no mouth, under a three cornered hat",
      ["mask", "bauta", "venetian mask", "carnival", "tricorn", "disguise", "masquerade"], outline=_bauta,
      over=lambda S: [shell(poly([(2.5, 8), (5.5, 3), (9, 4.5), (12, 5), (15, 4.5), (18.5, 3), (21.5, 8)], closed=True, r=S.r))])
def _(S):
    return [mark(almond(9.5, 12, 3.4, 2.4, S)), mark(almond(14.5, 12, 3.4, 2.4, S)),
            hole(poly([(12, 13), (13.5, 17.5), (10.5, 17.5)], closed=True, r=L(S, 0, 0.5)))]


def _vejigante(S):
    parts = [P(circle(12, 14, 6.5))]
    for a in (-160, -125, -90, -55, -20):
        base_l, base_r = polar(12, 14, 6, a - 15), polar(12, 14, 6, a + 15)
        if S.name == "line":
            tips = [polar(12, 14, 10.1, a - 2.2), polar(12, 14, 10.1, a + 2.2)]
        else:
            tips = [polar(12, 14, 10.4, a)]
        parts.append(P(poly([base_l, *tips, base_r, (12, 14)], closed=True, r=L(S, 0, 0.6))))
    return path_to_d(U(*parts))


@face("vejigante-mask", "Festival mask with cone shaped horns all around the head and a toothy mouth",
      ["vejigante", "mask", "horns", "carnival", "festival", "folk art", "costume"], outline=_vejigante)
def _(S):
    teeth = poly([(8.5, 16.5), (9.9, 18.5), (11.3, 16.5), (12.7, 18.5), (14.1, 16.5), (15.5, 18.5)], r=0)
    return [mark(poly([(8, 11.5), (11, 12.5), (10.5, 14), (8.5, 13.5)], closed=True, r=L(S, 0, 0.4))),
            mark(poly([(16, 11.5), (13, 12.5), (13.5, 14), (15.5, 13.5)], closed=True, r=L(S, 0, 0.4))),
            hole(rect(7.5, 16, 9, 3.5, L(S, 0.5, 1.5))), inset(teeth)]


def _krampus(S):
    pts = [(8, 6), (16, 6), (17.5, 10), (19.5, 13.5), (17.5, 14.2), (18.5, 17.5), (16, 17.2), (15.5, 20.5),
           (12, 19.5), (8.5, 20.5), (8, 17.2), (5.5, 17.5), (6.5, 14.2), (4.5, 13.5), (6.5, 10)]
    return poly(pts, closed=True, r=L(S, 0, 0.8))


@face("krampus-mask", "Horned folk mask with shaggy fur and a long hanging tongue",
      ["krampus", "mask", "horns", "demon", "christmas", "folklore", "alpine"], outline=_krampus,
      over=lambda S: [shell("M10.5 15H13.5V20.5A1.5 1.5 0 0 1 10.5 20.5Z" if S.name != "line" else "M10.5 15H13.5V21.5L12 20.3L10.5 21.5Z")])
def _(S):
    horn = "M8.8 6.5C6.5 5.2 4 6 2.8 4.2C2.1 3.1 2.8 2 4 2.2"
    return [ext_line(horn), ext_line(flip(horn)),
            mark(poly([(8, 9.5), (11, 10.8), (10.5, 12.3), (8.5, 11.8)], closed=True, r=L(S, 0, 0.4))),
            mark(poly([(16, 9.5), (13, 10.8), (13.5, 12.3), (15.5, 11.8)], closed=True, r=L(S, 0, 0.4)))]


# ============================================================================ characters

@face("pierrot-face", "Round clown face with a black skullcap, a painted tear and a ruffled collar",
      ["pierrot", "clown", "mime", "sad clown", "pantomime", "theatre", "circus"], outline=lambda S: circle(12, 10, 7),
      over=lambda S: [shell("M4 17.5H20V19.5A2 2 0 0 1 16 19.5A2 2 0 0 1 12 19.5A2 2 0 0 1 8 19.5A2 2 0 0 1 4 19.5Z"
                            if S.name != "line" else "M4 17.5H20V19.5L18 21.5L16 19.5L14 21.5L12 19.5L10 21.5L8 19.5L6 21.5L4 19.5Z")])
def _(S):
    cap = path_to_d(D(P(circle(12, 10, 8)), P(rect(0, 6.5, 24, 20))))
    sep = [detail(seg(4, 7.5, 20, 7.5))] if S.name == "filled" else []
    return [keep(cap), *sep,
            eye(S, 9.5, 10.5, 0.85), eye(S, 14.5, 10.5, 0.85), mark(drop(15.2, 12.6, 1, 14.3)),
            detail("M9.5 15.1Q10.8 14.3 12.1 15.1")]


def _ogre(S):
    head = rect(5, 3.5, 14, 18, L(S, 4, 5.5))
    ears = [circle(4.5, 11.5, 1.8), circle(19.5, 11.5, 1.8)]
    return union(head, *ears)


@face("ogre-face", "Broad ogre face with a heavy brow, a flat nose and two tusks",
      ["ogre", "troll", "monster", "brute", "fantasy", "orc", "giant"], outline=_ogre)
def _(S):
    tusk_l = poly([(8, 17.5), (9, 14.5), (10, 17.5)], closed=True, r=L(S, 0, 0.3))
    return [detail(poly([(7.5, 7.5), (12, 9), (16.5, 7.5)], r=S.r)),
            eye(S, 9, 11, 0.8), eye(S, 15, 11, 0.8),
            detail("M10.3 14C11 13.2 13 13.2 13.7 14"),
            detail(seg(7.5, 17.5, 16.5, 17.5)), mark(tusk_l), mark(flip(tusk_l))]


@face("pulling-eyelid-face", "Face pulling down one lower eyelid with a fingertip and sticking out its tongue",
      ["akanbe", "teasing", "mocking", "cheeky", "tongue out", "taunt", "emoji"],
      over=lambda S: [shell(rect(14, 13, 3.5, 9, L(S, 1, 1.75)))])
def _(S):
    return [eye(S, 8.5, 10), mark(ellipse(15.5, 9.8, 1.4, 2.1) if S.name != "line" else rect(14.2, 7.7, 2.6, 4.2)),
            detail(seg(6.5, 15, 11.5, 15)), hole("M7.5 15V17A1.5 1.5 0 0 0 10.5 17V15Z")]


@icon("eyes-in-the-dark", CAT, "Two glowing eyes with slit pupils staring out of a dark shape",
      tags=["eyes", "dark", "night", "creepy", "hidden", "watching", "spooky", "lurking"])
def _(S):
    body = rect(2.5, 5, 19, 14, L(S, 3, 6))
    eyes_ = []
    for cx in (8, 16):
        a = almond(cx, 12, 5.5, 4.2, S)
        slit = ellipse(cx, 12, 0.6, 1.4)
        eyes_.append(mark(path_to_d(D(P(a), P(slit)))))
    return [shell(body), *eyes_]


def _eyes_dark_filled():
    body = U(P(rect(2.5, 5, 19, 14, 5)), ST(rect(2.5, 5, 19, 14, 5), 2, "round", "round"))
    out = body
    for cx in (8, 16):
        out = D(out, P(almond(cx, 12, 5.5, 4.2, FILL)))
    for cx in (8, 16):
        out = U(out, P(ellipse(cx, 12, 0.6, 1.4)))
    return out


from dsl import REGISTRY as _REG  # noqa: E402
_REG[-1].filled_override = _eyes_dark_filled


@icon("kilroy-was-here", CAT, "Bald head with a long nose peeking over a wall, fingers gripping the edge",
      tags=["kilroy", "graffiti", "peeking", "peek", "was here", "doodle", "wall", "retro"])
def _(S):
    nose = "M10.5 13V18.5A1.5 1.5 0 0 0 13.5 18.5V13Z" if S.name != "line" else "M10.5 13V20H13.5V13Z"
    bumps = "M2.5 13V14.3A1.1 1.1 0 0 0 4.7 14.3A1.1 1.1 0 0 0 6.9 14.3V13"
    fingers = [line(bumps), line(flip(bumps))]
    return [line(seg(1.5, 13, 22.5, 13)), line(arc(12, 13, 6, 180, 360)),
            dot(10, 10.4, 1.3), dot(14, 10.4, 1.3), shell(nose), *fingers]


@face("face-without-mouth", "Round face with two eyes and no mouth",
      ["no mouth", "speechless", "silent", "mute", "quiet", "blank", "emoji"], aliases=["mouthless-face"])
def _(S):
    return [*eyes(S, 11)]


def _wobble(S):
    pts = []
    for k in range(12):
        a = -90 + k * 30
        r = 9 + (0.9 if k % 2 == 0 else -0.6) + (0.3 if k % 3 == 0 else 0)
        pts.append(polar(12, 12, r, a))
    return smooth_closed(pts)


@face("distorted-face", "Warped face with a wavy outline, mismatched eyes and a skewed mouth",
      ["distorted", "warped", "dizzy", "glitch", "woozy", "twisted", "emoji"], outline=_wobble)
def _(S):
    return [eye(S, 8.5, 10.5, 0.75), detail(circle(15, 9.5, 2)),
            detail("M7.5 16.5C8.5 15 9.5 15.5 10.5 16.2C11.8 17 13 16 13.8 14.8C14.5 14 15.5 14 16.5 14.5")]


@face("side-eye-face", "Face glancing sideways with both pupils shifted and one brow raised",
      ["side eye", "suspicious", "skeptical", "doubt", "sus", "glance", "emoji"], aliases=["side-eye"])
def _(S):
    r = L(S, 1.35, 1.3)
    pupil = (lambda x: mark(rect(x - 1.2, 11.5, 2.4, 2.6))) if S.name == "line" else (lambda x: mark(circle(x, 12.7, r)))
    return [detail(seg(6.5, 9.7, 10.5, 9.7)), detail(seg(13.5, 9.7, 17.5, 9.7)), pupil(9.6), pupil(16.6),
            detail("M13.8 7Q15.5 5.9 17.2 6.7"), detail(seg(10.5, 16.5, 15.5, 16.5))]


@face("thumbing-nose-face", "Face thumbing its nose with fingers spread wide and tongue out",
      ["thumb nose", "mocking", "taunt", "cheeky", "teasing", "nyah", "emoji"], outline=lambda S: circle(9, 12, 7),
      over=lambda S: [shell(circle(14.5, 11.5, 2.2)), line(seg(12.3, 11.5, 10.2, 11.5)),
                      *[line(seg(*polar(14.5, 11.5, 3.2, a), *polar(14.5, 11.5, 7.3, a))) for a in (-60, -22, 16, 54)]])
def _(S):
    return [eye(S, 6.5, 9, 0.8), eye(S, 10.5, 8.5, 0.8), detail(seg(5.5, 15.5, 10.5, 15.5)),
            hole("M6.5 15.5V17.3A1.5 1.5 0 0 0 9.5 17.3V15.5Z")]


# ============================================================================ expressions

@face("disgusted-face", "Disgusted face with lowered brows, squinting eyes and the tongue pushed out",
      ["disgust", "gross", "yuck", "eww", "nauseated", "revolted", "emoji"], aliases=["yuck"])
def _(S):
    return [detail(seg(7, 7, 10.5, 8.2)), detail(seg(17, 7, 13.5, 8.2)),
            detail(seg(7.5, 11, 10.5, 10.8)), detail(seg(16.5, 11, 13.5, 10.8)),
            detail("M7.5 17C9 15.2 10.5 14.8 12 14.8C13.5 14.8 15 15.2 16.5 17"),
            hole("M10.5 15V17.5A1.5 1.5 0 0 0 13.5 17.5V15Z" if S.name != "line" else "M10.5 15V19H13.5V15Z")]


@face("weary-face", "Weary face with eyes squeezed shut, raised brows and a wailing open mouth",
      ["weary", "exhausted", "fed up", "distraught", "wail", "tired", "emoji"], aliases=["exhausted-face"])
def _(S):
    return [detail(seg(7, 7.8, 10.2, 6.6)), detail(seg(17, 7.8, 13.8, 6.6)),
            detail(poly([(7.5, 9.3), (10.2, 10.6), (7.5, 11.9)], r=S.r * 0.3)),
            detail(poly([(16.5, 9.3), (13.8, 10.6), (16.5, 11.9)], r=S.r * 0.3)),
            hole("M8.5 18C8.5 15.4 10 14.2 12 14.2C14 14.2 15.5 15.4 15.5 18Z" if S.name == "line"
                 else "M9.5 18C8.7 18 8.4 17.4 8.6 16.7C9.1 15.1 10.4 14.2 12 14.2C13.6 14.2 14.9 15.1 15.4 16.7C15.6 17.4 15.3 18 14.5 18Z")]


def sparkle(cx, cy, R, S):
    k = R * 0.28
    pts = [(cx, cy - R), (cx + k, cy - k), (cx + R, cy), (cx + k, cy + k), (cx, cy + R), (cx - k, cy + k), (cx - R, cy), (cx - k, cy - k)]
    return poly(pts, closed=True, r=L(S, 0, 0.4))


@face("proud-face", "Proud face with the chin raised, closed eyes, a satisfied smile and a sparkle",
      ["proud", "pride", "smug", "satisfied", "confident", "accomplished", "emoji"], outline=lambda S: circle(11, 13, 8.5),
      over=lambda S: [mark(sparkle(19.5, 4.5, 3, S))])
def _(S):
    return [detail(arc(8, 8.3, 1.6, 0, 180)), detail(arc(14, 8.3, 1.6, 0, 180)),
            detail("M7 12.5C8.5 14.5 10 15 11.5 15C13 15 14.5 14.3 15.5 13")]


_JAW = [(4.5, 6.5), (5, 12), (7.5, 17), (12, 20), (16.5, 17), (19, 12), (19.5, 6.5)]
_LM_LINES = [[(12, 8.5), (12, 13)], [(9, 16.3), (15, 16.3)]]
_LM_DOTS = [(8.5, 9.5), (15.5, 9.5)]


def _lm_points():
    return _JAW + [p for ln in _LM_LINES for p in ln] + _LM_DOTS


def _landmarks_filled():
    out = [ST(poly(_JAW), 2.5, "round", "round")] + [ST(poly(ln), 2.5, "round", "round") for ln in _LM_LINES]
    out += [P(circle(x, y, 1.75)) for x, y in _lm_points()]
    return U(*out)


@icon("facial-landmarks", CAT, "Face mesh of landmark points on the jaw, brows, nose and mouth joined by lines",
      tags=["face landmarks", "face mesh", "face tracking", "computer vision", "keypoints", "biometrics", "ar"],
      filled=_landmarks_filled)
def _(S):
    parts = [line(poly(_JAW, r=S.r))] + [line(poly(ln)) for ln in _LM_LINES]
    if S.name == "line":
        parts += [solid(rect(x - 1.3, y - 1.3, 2.6, 2.6)) for x, y in _lm_points()]
    else:
        parts += [dot(x, y, 1.5) for x, y in _lm_points()]
    return parts


@icon("emotion-recognition", CAT, "Face inside scanning corners with a smile and a frown beside it",
      tags=["emotion detection", "sentiment", "face analysis", "mood", "affective computing", "ai", "scan"])
def _(S):
    c = [((2, 7.5), (2, 4), (5.5, 4)), ((11.5, 4), (15, 4), (15, 7.5)), ((15, 16.5), (15, 20), (11.5, 20)), ((5.5, 20), (2, 20), (2, 16.5))]
    br = [line(poly(list(k), r=S.r)) for k in c]
    return [*br, shell(circle(8.5, 12, 3.8)), dot(7.2, 11.2, 0.8), dot(9.8, 11.2, 0.8),
            line("M18 5.5C18.5 7.8 21 7.8 21.5 5.5"), line("M18 18.5C18.5 16.2 21 16.2 21.5 18.5")]


@icon("face-swap", CAT, "Two small faces with curved arrows swapping them",
      tags=["face swap", "swap", "switch", "exchange", "deepfake", "filter", "photo edit"])
def _(S):
    k = S.r * 0.3
    return [shell(circle(5.8, 12, 3.3)), shell(circle(18.2, 12, 3.3)),
            dot(4.7, 11.4, 0.85), dot(6.9, 11.4, 0.85), dot(17.1, 11.4, 0.85), dot(19.3, 11.4, 0.85),
            line("M5.8 6.2C7 2.8 17 2.8 18.2 6"), line(poly([(15.8, 5), (18.2, 6.3), (19.4, 3.8)], r=k)),
            line("M18.2 17.8C17 21.2 7 21.2 5.8 18"), line(poly([(8.2, 19), (5.8, 17.7), (4.6, 20.2)], r=k))]


# ============================================================================ stone heads

def _moai(S):
    head = poly([(8, 2.5), (16, 2.5), (17, 9), (17.5, 19), (16.5, 21.5), (7.5, 21.5), (6.5, 19), (7, 9)], closed=True, r=S.r)
    ears = [rect(4.5, 7.5, 3, 8, L(S, 0, 1.5)), rect(16.5, 7.5, 3, 8, L(S, 0, 1.5))]
    return union(head, *ears)


@icon("moai-head", CAT, "Tall stone head with a heavy brow, a long nose, long ears and a jutting chin",
      tags=["moai", "stone head", "statue", "easter island", "rapa nui", "monolith", "sculpture"])
def _(S):
    return [shell(_moai(S)), detail(seg(7.5, 7.5, 16.5, 7.5)),
            detail(poly([(11.3, 7.5), (10.3, 14.5), (13.7, 14.5), (12.7, 7.5)], r=S.r * 0.4)),
            detail(seg(9.5, 17.8, 14.5, 17.8))]


def _olmec(S):
    return rect(4, 3, 16, 19, L(S, 5, 7))


@icon("olmec-head", CAT, "Colossal round stone head in a fitted helmet with full lips and a broad nose",
      tags=["olmec", "colossal head", "stone head", "mesoamerica", "sculpture", "archaeology", "ancient"])
def _(S):
    return [shell(_olmec(S)), detail("M4.5 8.5C8 7 16 7 19.5 8.5"), detail(seg(7, 8.5, 7, 16)), detail(seg(17, 8.5, 17, 16)),
            detail(seg(9.2, 11, 11, 11)), detail(seg(13, 11, 14.8, 11)),
            detail(poly([(11.2, 12.5), (10, 15), (14, 15), (12.8, 12.5)], r=S.r * 0.4)),
            detail(ellipse(12, 18.3, 2.8, 1.2))]


# ============================================================================ situations

def _fist(S):
    top = "M5 22V14.5A1.75 1.75 0 0 1 8.5 14.5A1.75 1.75 0 0 1 12 14.5A1.75 1.75 0 0 1 15.5 14.5A1.75 1.75 0 0 1 19 14.5V22Z"
    if S.name == "line":
        return top
    return path_to_d(U(D(P(top), P(rect(0, 19, 24, 5))), P(rect(5, 16, 14, 6, 2.5))))


@face("stress-ball", "Squishy ball with a face squeezed in a fist", ["stress ball", "squeeze", "anxiety", "stress relief", "fidget", "tension", "squishy"],
      outline=lambda S: ellipse(12, 9, 8, 6.2),
      over=lambda S: [shell(_fist(S)), detail(seg(8.5, 14.5, 8.5, 16.5)), detail(seg(12, 14.5, 12, 16.5)), detail(seg(15.5, 14.5, 15.5, 16.5)),
                      detail(seg(5, 19, 13, 19))])
def _(S):
    return [detail(poly([(8, 6), (10, 7.1), (8, 8.2)], r=S.r * 0.3)), detail(poly([(16, 6), (14, 7.1), (16, 8.2)], r=S.r * 0.3))]


@face("hangover-face", "Face with droopy half closed eyes, a wavy mouth and an ice pack on the head",
      ["hangover", "headache", "hungover", "ice pack", "unwell", "morning after", "emoji"], outline=lambda S: circle(12, 13, 8.5),
      over=lambda S: [shell(rect(4.5, 1.5, 12.5, 4.5, L(S, 1.5, 2.25))), shell(rect(17.5, 2, 3.5, 3.5, L(S, 0.5, 1)))])
def _(S):
    lids = [detail(seg(6.5, 11.5, 10.5, 11.5)), detail(seg(13.5, 11.5, 17.5, 11.5))]
    half = [mark(arc(x, 11.5, 1.5, 0, 180) + "Z") for x in (8.5, 15.5)]
    return [*lids, *half, detail("M8 17.3C9 16.3 10 16.3 11 17C12 17.7 13 17.7 14 17C14.7 16.5 15.3 16.4 16 16.8")]


@face("brain-freeze-face", "Face grimacing with eyes squeezed shut next to an ice cream cone",
      ["brain freeze", "ice cream headache", "cold", "ouch", "frozen", "grimace", "emoji"], outline=lambda S: circle(10.5, 10.5, 8.5),
      over=lambda S: [shell(union(arc(18.5, 15.5, 3.3, 180, 360) + "Z", poly([(16, 15.5), (21, 15.5), (18.5, 21.5)], closed=True, r=L(S, 0, 0.6)))),
                      detail(seg(15.2, 15.5, 21.8, 15.5))])
def _(S):
    return [detail(poly([(5.5, 7.5), (8.3, 8.8), (5.5, 10.1)], r=S.r * 0.3)), detail(poly([(15.5, 7.5), (12.7, 8.8), (15.5, 10.1)], r=S.r * 0.3)),
            hole(rect(6, 12.5, 9, 4, L(S, 0.8, 2))), inset(seg(6, 14.5, 15, 14.5))]


@face("bed-head-face", "Sleepy yawning face with one eye half open and messy hair tufts",
      ["bed head", "messy hair", "just woke up", "sleepy", "yawn", "morning", "emoji"], outline=lambda S: circle(12, 13.5, 8),
      over=lambda S: [line("M8.5 6.8C7.5 4.5 5.8 3.8 3.8 4.2"), line("M12 5.5C11.8 3.6 12.8 2.4 14.5 2"),
                      line("M15.5 6.3C16.8 4.5 18.5 4.6 20 5.8")])
def _(S):
    return [detail(seg(7, 11.5, 10.5, 11.5)), detail(seg(13.5, 10.8, 17, 10.8)), mark(arc(15.25, 10.8, 1.4, 0, 180) + "Z"),
            hole(ellipse(12, 17, 1.8, 2.1))]


@face("twitching-eye-face", "Face with a tense forced smile and one eye twitching",
      ["twitch", "stressed", "forced smile", "tense", "nervous", "on edge", "emoji"], outline=lambda S: circle(11, 13, 8.5),
      over=lambda S: [line(poly([(18.5, 2.5), (20.5, 4.5), (19, 5.5), (21.5, 7.5)], r=L(S, 0, 0.4))),
                      line(poly([(15.5, 1.5), (16.5, 3.5)], r=0))])
def _(S):
    return [eye(S, 8, 10.5), eye(S, 14, 10.5), detail(seg(12.3, 8, 15.7, 7.2)),
            hole("M6.5 14.5H15.5C15.5 17 13.5 18.5 11 18.5C8.5 18.5 6.5 17 6.5 14.5Z"), inset(seg(6.5, 16, 15.5, 16))]


@face("mad-scientist-face", "Face with wild frizzy hair, goggles pushed up on the forehead and a manic grin",
      ["mad scientist", "crazy", "genius", "inventor", "evil genius", "wild hair", "lab"], outline=lambda S: circle(12, 14, 7),
      over=lambda S: [line(poly([(4.8, 12.5), (2.5, 11), (4.3, 9.2), (2, 7.2), (5, 6.5), (4, 3.5), (7.2, 4.5), (8.2, 1.8),
                                  (10.2, 3.6), (12, 1.5), (13.8, 3.6), (15.8, 1.8), (16.8, 4.5), (20, 3.5), (19, 6.5),
                                  (22, 7.2), (19.7, 9.2), (21.5, 11), (19.2, 12.5)], r=L(S, 0, 0.4))),
                      shell(circle(9.5, 8, 1.9)), shell(circle(14.5, 8, 1.9))])
def _(S):
    return [eye(S, 9.5, 13, 0.8), eye(S, 14.5, 13, 0.8), hole("M8 16H16C16 18.2 14.3 19.3 12 19.3C9.7 19.3 8 18.2 8 16Z"),
            inset(seg(12, 16, 12, 19.3))]


def _punk(S):
    parts = [P(circle(13, 12.5, 7)), P(poly([(6.4, 10.5), (3.6, 14.6), (6.8, 15.4)], closed=True, r=L(S, 0, 0.6)))]
    for a in (-140, -110, -80, -50):
        parts.append(P(poly([polar(13, 12.5, 6, a - 12), polar(13, 12.5, 10.5, a), polar(13, 12.5, 6, a + 12), (13, 12.5)],
                            closed=True, r=L(S, 0, 0.3))))
    return path_to_d(U(*parts))


@icon("punk-face", CAT, "Head in profile with a tall spiked mohawk and a sneer",
      tags=["punk", "mohawk", "rebel", "rock", "subculture", "spiky hair", "attitude"])
def _(S):
    return [shell(_punk(S), stroke_miterlimit="2"), dot(9, 12, 1.2), detail(arc(14.5, 13.5, 1.6, 270, 450)),
            detail(poly([(8.8, 17.3), (10.8, 17.3), (11.8, 16.3)], r=S.r * 0.3))]
