"""TypeIcon Core: classroom (batch 002).

Classroom life, special-education supports, school events and hands-on activities, drawn from the objects
themselves. Overlapping objects are drawn in layers (front first): back layers are cut away around the front
silhouette with a small gap in every style so they stay readable at 16 px.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, filled_region, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import LINE, fmt, path_to_d, polar, rotation, transform_path

CAT = "classroom"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def star(cx, cy, r, ri=None, n=5, start=-90.0):
    ri = r * 0.45 if ri is None else ri
    pts = []
    for i in range(2 * n):
        pts.append(polar(cx, cy, r if i % 2 == 0 else ri, start + i * 180 / n))
    return pts


def rotd(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rotp(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def cloud(circles, base_y=None, x0=None, x1=None):
    parts = [P(circle(*c)) for c in circles]
    if base_y is not None:
        parts.append(P(rect(x0, base_y - 3, x1 - x0, 3)))
    return path_to_d(U(*parts))


# --------------------------------------------------------------------------- layering (front layer first)

def _paint(parts, S):
    regs = []
    for p in parts:
        if p.kind in ("dot", "solid"):
            regs.append(P(p.d))
        else:
            regs.append(ST(p.d, 2.0, S.cap, S.join, float(p.attrs.get("stroke_miterlimit", 4))))
    return U(*regs)


def _sil(parts, S):
    regs = []
    for p in parts:
        if p.kind in ("dot", "solid"):
            regs.append(P(p.d))
        elif p.kind == "shell":
            regs.append(U(P(p.d), ST(p.d, 2.0, S.cap, S.join, float(p.attrs.get("stroke_miterlimit", 4)))))
        else:
            regs.append(ST(p.d, 2.0, S.cap, S.join))
    return U(*regs)


def _grow(region, g):
    if g <= 0:
        return region
    return U(region, ST(path_to_d(region), 2 * g, "round", "round"))


def _stroke_layers(S, layers, gap):
    out = list(layers[0])
    cover = _grow(_sil(layers[0], S), gap)
    for parts in layers[1:]:
        if not parts:
            continue
        vis = D(_paint(parts, S), cover)
        if abs(vis.area) > 0.01:
            out.append(solid(path_to_d(vis)))
        cover = U(cover, _grow(_sil(parts, S), gap))
    return out


def _filled_layers(layers, gap):
    result = filled_region(layers[0])
    cover = _grow(result, gap)
    for parts in layers[1:]:
        if not parts:
            continue
        f = filled_region(parts)
        result = U(result, D(f, cover))
        cover = U(cover, _grow(f, gap))
    return result


def layered(name, desc, tags, aliases=(), gap=1.5):
    """Register an icon drawn as layers: fn(S) -> [front parts, parts behind, ...]."""
    def deco(fn):
        icon(name, CAT, desc, tags=tags, aliases=aliases,
             filled=lambda: _filled_layers(fn(LINE), gap))(lambda S: _stroke_layers(S, fn(S), gap))
        return fn
    return deco


def spiral(cx, cy, r0, r1, turns, a0=-90.0, n=36):
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append(polar(cx, cy, r0 + (r1 - r0) * t, a0 + 360 * turns * t))
    return pts


# ============================================================================ in class

@icon("doodling", CAT, "Notebook page with a spiral and a star doodled beside the margin",
      tags=["doodle", "scribble", "sketch", "notebook", "bored", "drawing"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 2.5))),
        detail(seg(8.5, 2.5, 8.5, 21.5)),
        detail(poly(spiral(14.25, 8.25, 0.6, 3.6, 1.15))),
        mark(poly(star(14.25, 16.25, 3.4, 1.5), closed=True, r=L(S, 0, 0.4))),
    ]


@icon("daydreaming", CAT, "Person gazing up at a thought cloud with a star in it",
      tags=["daydream", "dreaming", "distracted", "imagination", "mind wandering", "wishing"])
def _(S):
    cl = cloud([(14, 7, 2.75), (17.5, 5.25, 3.25), (20, 8, 2)], 10, 14, 20)
    bust = ("M2.5 21.5V19A3 3 0 0 1 5.5 16H9.5A3 3 0 0 1 12.5 19V21.5" if S.name == "rounded" else
            "M2.5 21.5V18L4.5 16H10.5L12.5 18V21.5")
    return [
        shell(circle(7.5, 10.5, 3)), line(bust),
        dot(12.25, 12.75, 1.1),
        shell(cl),
        mark(poly(star(17, 7.5, 2.1, 0.95), closed=True, r=L(S, 0, 0.3))),
    ]


@layered("sleeping-in-class", "Head resting on folded arms on a desk with a Z above",
         tags=["asleep", "tired", "napping", "snooze", "bored", "student"])
def _(S):
    return [
        [shell(circle(9, 9, 3.5))],
        [shell(rect(3.5, 12.5, 14, 4, L(S, 1, 2)))],
        [line(seg(2, 18.5, 22, 18.5)), line(seg(4, 18.5, 4, 21.5)), line(seg(20, 18.5, 20, 21.5)),
         line(poly([(15, 3), (19.5, 3), (15, 8), (19.5, 8)], r=S.r * 0.4))],
    ]


def _bitten_page():
    page = rect(3.5, 2.5, 15, 19, 0)
    bites = [circle(18.5, 3, 2.6), circle(19.3, 7.2, 2.1), circle(14.6, 2.3, 2.1)]
    return minus(page, *bites)


@icon("dog-ate-homework", CAT, "Homework sheet with bites taken out of its corner and a paw print",
      tags=["homework", "excuse", "dog", "bitten", "chewed", "late work"])
def _(S):
    return [
        shell(_bitten_page(), stroke_miterlimit="2"),
        detail(seg(6.5, 6.5, 11, 6.5)),
        detail(seg(6.5, 10, 14.5, 10)),
        mark(ellipse(11, 16.75, 2.6, 2.1)),
        dot(7.9, 13.6, 1.15), dot(11, 12.5, 1.15), dot(14.1, 13.6, 1.15),
    ]


@layered("sensory-bubble-tube", "Tall clear column of rising bubbles on a round base",
         tags=["bubble tube", "sensory", "calming", "sensory room", "autism", "light"])
def _(S):
    return [
        [shell(rect(5, 18, 14, 3.5, rr(S, 1.5)))],
        [shell(rect(7.5, 2.5, 9, 17, rr(S, 3))), dot(10.5, 14.5, 1.3), dot(13.5, 11, 1.3), dot(10.5, 7.5, 1.3),
         dot(13.25, 4.9 if S.name == "line" else 5.3, 0.9)],
    ]


@icon("speech-generating-device", CAT, "Tablet with a grid of symbol buttons and sound waves",
      tags=["aac device", "communication device", "talker", "speech", "voice output", "assistive technology"])
def _(S):
    k = L(S, 0, 0.6)
    keys = [mark(rect(x, y, 2.75, 2.75, k)) for x in (4.75, 9.25) for y in (5.5, 10.5, 15.5)]
    return [
        shell(rect(2.5, 2.5, 12, 19, rr(S, 2.5))),
        *keys,
        line(arc(14.5, 12, 4, -35, 35)),
        line(arc(14.5, 12, 7, -35, 35)),
    ]


@layered("slant-board", "Angled writing board seen from the side with a clip holding paper at the top",
         tags=["writing slope", "slope board", "handwriting", "occupational therapy", "posture", "desk"])
def _(S):
    return [
        [shell(rotd(rect(16, 5.5, 3, 5, L(S, 0, 1)), -28, 17.5, 8))],
        [shell(poly([(2.5, 20), (21.5, 20), (21.5, 10)], closed=True, r=S.r), stroke_miterlimit="2"),
         line(seg(4.5, 16, 15, 10.45))],
    ]


@icon("wobble-cushion", CAT, "Round inflated disc cushion with a bumpy top",
      tags=["wobble cushion", "balance disc", "sensory seat", "fidget", "wiggle seat", "active sitting"])
def _(S):
    body = "M3 10A9 4.5 0 0 1 21 10V14A9 4.5 0 0 1 3 14Z" if S.name == "rounded" else \
        "M3 10A9 4.5 0 0 1 21 10V14.5A9 4 0 0 1 3 14.5Z"
    return [
        shell(body),
        detail("M3 10A9 4.5 0 0 0 21 10"),
        dot(8, 9.75, 1.1), dot(12, 8.5, 1.1), dot(16, 9.75, 1.1),
    ]


@icon("chew-necklace", CAT, "Cord necklace with a chunky ring-shaped chewable pendant",
      tags=["chewelry", "chew toy", "sensory", "oral motor", "chewing", "fidget"])
def _(S):
    return [
        line(arc(12, 2.5, 7.5, 0, 180) if S.name == "rounded" else poly([(4.5, 2.5), (4.5, 4.5), (12, 10.5), (19.5, 4.5), (19.5, 2.5)])),
        shell(circle(12, 16, 5.5) if S.name == "rounded" else poly(regular(12, 16, 5.8, 6, start=-90), closed=True)),
        detail(circle(12, 16, 1.75)),
    ]


@icon("first-then-board", CAT, "Board with two picture cards and an arrow from first to then",
      tags=["first then", "visual schedule", "routine", "autism", "sequence", "visual support"])
def _(S):
    k = L(S, 0, 1)
    return [
        shell(rect(2, 3.5, 20, 17, rr(S, 2.5))),
        detail(seg(5, 7, 9.5, 7)), detail(seg(14.5, 7, 19, 7)),
        detail(rect(4.75, 10, 5, 7, k)),
        detail(rect(14.25, 10, 5, 7, k)),
        mark(poly([(11, 11.25), (13, 13.5), (11, 15.75)], closed=True, r=S.r * 0.3)),
    ]


@icon("token-board", CAT, "Reward board with a star picture above a row of earned tokens",
      tags=["token economy", "reward chart", "behaviour", "behavior", "tokens", "motivation"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 2.5))),
        mark(poly(star(12, 8.25, 3.75, 1.7), closed=True, r=L(S, 0, 0.4))),
        detail(seg(2.5, 13, 21.5, 13)),
        dot(7, 17.25, 1.6), dot(12, 17.25, 1.6),
        detail(circle(17, 17.25, 1.1)),
    ]


@icon("social-story", CAT, "Open booklet with a person on one page and a speech bubble on the other",
      tags=["social story", "social narrative", "autism", "booklet", "behaviour", "communication"])
def _(S):
    book = poly([(2, 4.5), (12, 6), (22, 4.5), (22, 19.5), (12, 21), (2, 19.5)], closed=True, r=S.r * 0.66)
    bub = ("M14.5 9H19.5V13.5H16.5L15 15V13.5H14.5Z" if S.name == "line" else
           "M15.5 9H18.5A1 1 0 0 1 19.5 10V12.5A1 1 0 0 1 18.5 13.5H16.5L15 15V13.5A1 1 0 0 1 14.5 12.5V10A1 1 0 0 1 15.5 9Z")
    return [
        shell(book),
        detail(seg(12, 6, 12, 21)),
        dot(7, 9.75, 1.6),
        detail("M4.5 17V15.5A1.5 1.5 0 0 1 6 14H8A1.5 1.5 0 0 1 9.5 15.5V17" if S.name == "rounded" else "M4.5 17V14H9.5V17"),
        detail(bub),
    ]


@icon("feelings-chart", CAT, "Chart of four faces: happy, sad, angry and worried",
      tags=["emotions chart", "feelings", "emotions", "zones", "check in", "wellbeing"])
def _(S):
    cells = [(7.25, 7.25), (16.75, 7.25), (7.25, 16.75), (16.75, 16.75)]
    mouths = [
        lambda x, y: f"M{fmt(x - 2)} {fmt(y + 1)}Q{fmt(x)} {fmt(y + 3)} {fmt(x + 2)} {fmt(y + 1)}",
        lambda x, y: f"M{fmt(x - 2)} {fmt(y + 2.5)}Q{fmt(x)} {fmt(y + 0.5)} {fmt(x + 2)} {fmt(y + 2.5)}",
        lambda x, y: seg(x - 2, y + 1.75, x + 2, y + 1.75),
        lambda x, y: f"M{fmt(x - 2)} {fmt(y + 2)}Q{fmt(x - 1)} {fmt(y + 0.75)} {fmt(x)} {fmt(y + 2)}Q{fmt(x + 1)} {fmt(y + 3.25)} {fmt(x + 2)} {fmt(y + 2)}",
    ]
    parts = [shell(rect(2.5, 2.5, 19, 19, rr(S, 2.5))), detail(seg(12, 2.5, 12, 21.5)), detail(seg(2.5, 12, 21.5, 12))]
    for (x, y), m in zip(cells, mouths):
        parts += [dot(x - 1.4, y - 1.4, 0.85), dot(x + 1.4, y - 1.4, 0.85), detail(m(x, y))]
    return parts


@icon("calm-down-corner", CAT, "Small play tent with a floor cushion and a star beside it",
      tags=["calm corner", "calming corner", "quiet space", "safe space", "self regulation", "cozy corner"])
def _(S):
    return [
        shell(poly([(2, 21), (8.5, 7), (15, 21)], closed=True, r=S.r * 0.66)),
        detail(poly([(6.5, 21), (8.5, 15.5), (10.5, 21)], r=S.r * 0.3)),
        shell(rect(15.5, 17, 6.5, 4, rr(S, 2))),
        mark(poly(star(18.5, 7.5, 3.5, 1.6), closed=True, r=L(S, 0, 0.4))),
    ]


@layered("individual-education-plan", "Document with a person at the top and a target beside it",
         tags=["iep", "education plan", "learning plan", "sen", "special needs", "goals"])
def _(S):
    return [
        [shell(circle(16.5, 16.5, 5)), dot(16.5, 16.5, 1.4)],
        [shell(rect(3, 2.5, 14, 17, rr(S, 2.5))), dot(8, 6.75, 1.5),
         detail("M5.75 11.5A2.25 2.25 0 0 1 10.25 11.5"),
         detail(seg(12, 7, 14, 7)), detail(seg(12, 10.5, 14, 10.5))],
    ]


@layered("teaching-assistant", "Adult beside a smaller seated child, pointing at a page on the desk",
         tags=["teaching assistant", "classroom aide", "support staff", "tutor", "one to one", "helper"])
def _(S):
    return [
        [line(seg(2, 15.5, 14, 15.5)), line(seg(4, 15.5, 4, 21.5))],
        [shell(circle(17.5, 6, 2.75)),
         line(poly([(21.5, 21.5), (21.5, 13.5), (19.5, 11.5), (15.5, 11.5), (11.5, 13.5)], r=S.r))],
        [shell(circle(7.5, 8, 2.25)), line(poly([(4, 15.5), (4, 13.5), (5.5, 12), (9.5, 12), (11, 13.5)], r=S.r))],
    ]


# ============================================================================ reading, timing and supports

@layered("colored-reading-overlay", "Tinted sheet laid over the lower lines of a text page",
         tags=["reading overlay", "coloured overlay", "dyslexia", "visual stress", "reading aid", "tinted"])
def _(S):
    return [
        [shell(rect(8.5, 10, 13, 10, rr(S, 2))), detail(seg(11, 13.5, 18.5, 13.5)), detail(seg(11, 16.75, 16, 16.75))],
        [shell(rect(2.5, 2.5, 14, 19, rr(S, 2.5))), detail(seg(5.5, 6.5, 13.5, 6.5)), detail(seg(5.5, 10, 7, 10)),
         detail(seg(5.5, 13.5, 7, 13.5))],
    ]


@icon("visual-timer", CAT, "Round timer with a shaded sector showing the time left",
      tags=["visual timer", "countdown", "time left", "time timer", "transition", "minutes"])
def _(S):
    a = 125
    ex, ey = polar(12, 13, 6, -90 + a)
    sector = f"M12 13V7A6 6 0 0 1 {fmt(ex)} {fmt(ey)}Z"
    return [
        shell(circle(12, 13, 8.5)),
        shell(rect(10, 2, 4, 2.5, L(S, 0, 1))),
        mark(sector),
    ]


@icon("break-card", CAT, "Card with a pause symbol and a line of text",
      tags=["break card", "ask for a break", "pause", "rest", "self regulation", "visual support"])
def _(S):
    k = L(S, 0, 0.75)
    return [
        shell(rect(2.5, 5, 19, 14, rr(S, 2.5))),
        mark(rect(5.5, 8.5, 2.5, 7, k)), mark(rect(9.5, 8.5, 2.5, 7, k)),
        detail(seg(14.5, 10, 18, 10)), detail(seg(14.5, 14, 17, 14)),
    ]


def _foot(cx, cy, deg):
    sole = f"M{fmt(cx)} {fmt(cy - 3.2)}C{fmt(cx + 2.3)} {fmt(cy - 3.2)} {fmt(cx + 1.9)} {fmt(cy + 3.4)} {fmt(cx)} {fmt(cy + 3.4)}C{fmt(cx - 1.9)} {fmt(cy + 3.4)} {fmt(cx - 2.3)} {fmt(cy - 3.2)} {fmt(cx)} {fmt(cy - 3.2)}Z"
    return rotd(sole, deg, cx, cy)


@icon("sensory-path", CAT, "Floor trail of footprints following a zigzag line",
      tags=["sensory path", "sensory walk", "movement break", "hallway", "footprints", "active learning"])
def _(S):
    return [
        line(poly([(3, 6), (7, 2.5), (11, 6), (15, 2.5), (19, 6)], r=S.r * 0.5)),
        mark(_foot(8, 15.5, -12)), dot(8.9, 10.2, 1),
        mark(_foot(16, 17.5, 12)), dot(15.1, 12.2, 1),
    ]


@icon("reading-pen", CAT, "Scanning pen passing over text with sound waves",
      tags=["reading pen", "scanning pen", "text to speech", "dyslexia", "assistive technology", "read aloud"])
def _(S):
    body = rotd(rect(9.5, 1, 5, 16, rr(S, 2.5)), 45, 12, 12)
    return [
        shell(body),
        solid(poly(rotp([(11, 17), (13, 17), (12, 19.5)], 45, 12, 12), closed=True)),
        detail(rotd(seg(12, 4, 12, 8), 45, 12, 12)),
        line(seg(2.5, 21.5, 9, 21.5)),
        line(arc(10, 10, 5, 180, 250)),
        line(arc(10, 10, 8, 185, 245)),
    ]


@icon("tablet-arm-desk", CAT, "Student chair with a writing tablet arm in front of the seat",
      tags=["tablet arm chair", "desk chair", "lecture chair", "school desk", "writing arm", "seat"])
def _(S):
    return [
        shell(rect(3, 3, 3.5, 12, rr(S, 1.5))),
        shell(rect(3, 12.5, 12, 3, rr(S, 1.5))),
        line(seg(4.75, 15.5, 4.75, 21.5)), line(seg(13, 15.5, 13, 21.5)),
        shell(rect(11, 6.5, 10.5, 3, rr(S, 1.5))),
        line(seg(6.5, 8, 11, 8)),
    ]


@layered("pull-down-map", "Wall map hanging from a roller case with a pull ring",
         tags=["wall map", "roller map", "geography", "classroom map", "pull down", "chart"])
def _(S):
    return [
        [shell(rect(2, 2.5, 20, 3.5, rr(S, 1.75)))],
        [shell(rect(4, 5, 16, 11.5, L(S, 0, 1.5))),
         detail("M7 9.5C8.5 8 10 10.5 11.5 9.5S14 11.5 13 13" if S.name == "rounded" else poly([(7, 9.5), (9, 8.5), (11.5, 10), (13.5, 9.5), (13, 13)])),
         dot(16.5, 12.25, 1.1),
         line(seg(12, 16.5, 12, 18)), line(circle(12, 20, 1.75))],
    ]


@icon("bulletin-board", CAT, "Framed corkboard with pinned notes",
      tags=["corkboard", "notice board", "noticeboard", "pinboard", "announcements", "classroom display"])
def _(S):
    k = L(S, 0, 0.75)
    return [
        shell(rect(2, 3, 20, 18, rr(S, 2.5))),
        detail(rect(5, 7, 5.5, 5.5, k)),
        detail(rect(13.5, 8.5, 5.5, 8.5, k)),
        detail(rect(5, 15.5, 5, 2.5, k)),
        dot(16.25, 6.5, 1.3),
    ]


@icon("weather-chart", CAT, "Classroom board with sun and rain cloud symbols and an arrow under the sun",
      tags=["weather chart", "weather board", "circle time", "forecast", "calendar time", "early years"])
def _(S):
    cl = cloud([(14, 9.25, 2.25), (17.25, 7.75, 2.75), (19, 9.75, 1.75)], 11.5, 14, 19.5)
    return [
        shell(rect(2, 3, 20, 18, rr(S, 2.5))),
        dot(7.5, 8.75, 2.5),
        mark(cl),
        detail(seg(15, 14.5, 14.25, 17)), detail(seg(18.5, 14.5, 17.75, 17)),
        mark(poly([(7.5, 13.5), (9.75, 17.5), (5.25, 17.5)], closed=True, r=S.r * 0.3)),
    ]


@icon("marble-reward-jar", CAT, "Glass jar partly filled with marbles",
      tags=["marble jar", "reward jar", "class reward", "behaviour", "behavior", "incentive"])
def _(S):
    return [
        shell(rect(7, 2, 10, 3, rr(S, 1))),
        shell("M7.5 5V6.5C5.5 7.5 4.5 9 4.5 11V19A2.5 2.5 0 0 0 7 21.5H17A2.5 2.5 0 0 0 19.5 19V11C19.5 9 18.5 7.5 16.5 6.5V5"
              if S.name == "rounded" else poly([(7.5, 5), (7.5, 6.5), (4.5, 9), (4.5, 21.5), (19.5, 21.5), (19.5, 9), (16.5, 6.5), (16.5, 5)], closed=True)),
        detail(seg(4.5, 11.5, 19.5, 11.5)),
        dot(8.5, 18, 1.6), dot(12, 18, 1.6), dot(15.5, 18, 1.6), dot(10.25, 14.75, 1.6), dot(13.75, 14.75, 1.6),
    ]


@icon("school-gate", CAT, "Gate with two posts, vertical bars and an arched sign across the top",
      tags=["school gate", "gates", "entrance", "school entrance", "drop off", "pick up"])
def _(S):
    band = "M2.5 8Q12 -1 21.5 8V10.5Q12 1.5 2.5 10.5Z"
    return [
        shell(band, stroke_miterlimit="2"),
        shell(rect(2.5, 12.5, 3, 9, L(S, 0, 1))),
        shell(rect(18.5, 12.5, 3, 9, L(S, 0, 1))),
        line(seg(9, 10, 9, 21.5)), line(seg(15, 10, 15, 21.5)),
        line(seg(5.5, 15.5, 18.5, 15.5)),
    ]


@icon("detention", CAT, "Clock above a chalkboard of repeated written lines",
      tags=["detention", "punishment", "writing lines", "after school", "discipline", "consequence"])
def _(S):
    def wave(y):
        return f"M5.5 {fmt(y)}Q7 {fmt(y - 1.5)} 8.5 {fmt(y)}T11.5 {fmt(y)}T14.5 {fmt(y)}T17.5 {fmt(y)}"
    return [
        shell(circle(12, 5.5, 3.5)),
        detail(poly([(12, 3.75), (12, 5.5), (13.5, 6.5)], r=S.r * 0.3)),
        shell(rect(2.5, 11.5, 19, 10, rr(S, 2))),
        detail(wave(15)), detail(wave(18.25)),
    ]


def _shield(cx, cy, w, h):
    return (f"M{fmt(cx - w / 2)} {fmt(cy - h / 2)}H{fmt(cx + w / 2)}V{fmt(cy)}"
            f"Q{fmt(cx + w / 2)} {fmt(cy + h / 2 * 0.8)} {fmt(cx)} {fmt(cy + h / 2)}"
            f"Q{fmt(cx - w / 2)} {fmt(cy + h / 2 * 0.8)} {fmt(cx - w / 2)} {fmt(cy)}Z")


@icon("school-blazer", CAT, "School blazer with lapels and a crest on the breast pocket",
      tags=["blazer", "school uniform", "jacket", "crest", "uniform", "private school"])
def _(S):
    return [
        shell(poly([(8, 2.5), (3, 5), (3, 21.5), (21, 21.5), (21, 5), (16, 2.5)], closed=True, r=S.r)),
        detail(poly([(8, 2.5), (9.5, 8), (8, 9.5), (12, 16)], r=S.r * 0.4)),
        detail(poly([(16, 2.5), (14.5, 8), (16, 9.5), (12, 16)], r=S.r * 0.4)),
        mark(_shield(17.25, 13.5, 3.25, 4)),
        dot(12, 19, 1),
    ]


@layered("show-and-tell", "Child holding up a star toy in front of two seated classmates",
         tags=["show and tell", "presentation", "sharing time", "circle time", "public speaking", "kids"])
def _(S):
    def bust(cx):
        return (f"M{fmt(cx - 3.5)} 22V21A2.5 2.5 0 0 1 {fmt(cx - 1)} 18.5H{fmt(cx + 1)}A2.5 2.5 0 0 1 {fmt(cx + 3.5)} 21V22"
                if S.name == "rounded" else f"M{fmt(cx - 3.5)} 22V20L{fmt(cx - 2)} 18.5H{fmt(cx + 2)}L{fmt(cx + 3.5)} 20V22")
    return [
        [shell(circle(5.5, 14.5, 2)), shell(circle(18.5, 14.5, 2)), line(bust(5.5)), line(bust(18.5))],
        [shell(circle(10.5, 4.5, 2.25)),
         line(poly([(7.5, 14.5), (7.5, 10), (8.5, 9), (12.5, 9), (16, 5.5)], r=S.r)),
         line(seg(12, 9, 13.5, 14.5)),
         mark(poly(star(18.5, 4, 3, 1.35), closed=True, r=L(S, 0, 0.35)))],
    ]


@layered("bake-sale", "Table with a frosted cupcake and a price sign on a stand",
         tags=["bake sale", "fundraiser", "cake stall", "fete", "charity", "school fair"])
def _(S):
    top = cloud([(5.75, 9, 2.25), (8.5, 7, 2.75), (11.25, 9, 2.25)], 11, 5.75, 11.25)
    return [
        [shell(top),
         shell(poly([(4.5, 11), (12.5, 11), (11.5, 15), (5.5, 15)], closed=True, r=S.r * 0.4)),
         shell(rect(15, 4, 6.5, 5.5, rr(S, 1.5))), line(seg(18.25, 9.5, 18.25, 15))],
        [line(seg(2, 16.5, 22, 16.5)), line(seg(4, 16.5, 4, 21.5)), line(seg(20, 16.5, 20, 21.5))],
    ]


@layered("first-day-of-school", "Child with a backpack holding a sign with the number 1",
         tags=["first day of school", "back to school", "new school year", "first day", "starting school", "milestone"])
def _(S):
    body = ("M6 21.5V14A3.5 3.5 0 0 1 9.5 10.5H14.5A3.5 3.5 0 0 1 18 14V21.5" if S.name == "rounded" else
            "M6 21.5V13L8.5 10.5H15.5L18 13V21.5")
    return [
        [shell(rect(4, 13.5, 10, 8, rr(S, 2))),
         detail(poly([(7.75, 16.25), (9.25, 15.5), (9.25, 19.5)], r=S.r * 0.3))],
        [shell(circle(12, 5, 3)), line(body)],
        [shell(rect(15.5, 8, 6, 9, rr(S, 2)))],
    ]




# ============================================================================ events and school life

@icon("book-fair", CAT, "Bookcase stall of books under a string of bunting",
      tags=["book fair", "book sale", "reading", "library", "school event", "books"])
def _(S):
    k = L(S, 0, 0.5)
    flags = [mark(poly([(x - 1.75, 3.5 + 0.2 * abs(x - 12) * 0), (x + 1.75, 3.5), (x, 7)], closed=True, r=S.r * 0.2)) for x in (6, 12, 18)]
    return [
        line(seg(2, 3, 22, 3)),
        *flags,
        shell(rect(3, 10, 18, 11.5, rr(S, 2))),
        detail(seg(3, 15.75, 21, 15.75)),
        mark(rect(6, 11.5, 2, 3, k)), mark(rect(9, 11.5, 2, 3, k)), mark(poly([(13, 14.5), (14.9, 11.8), (16.5, 12.9), (14.6, 14.5)], closed=True)),
        mark(rect(6, 17.25, 2, 3, k)), mark(rect(12, 17.25, 2, 3, k)), mark(rect(15, 17.25, 2, 3, k)),
    ]


def _leaf(x0, y0, x1, y1, bulge):
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    nx, ny = -dy * bulge, dx * bulge
    return (f"M{fmt(x0)} {fmt(y0)}Q{fmt(mx + nx)} {fmt(my + ny)} {fmt(x1)} {fmt(y1)}"
            f"Q{fmt(mx - nx)} {fmt(my - ny)} {fmt(x0)} {fmt(y0)}Z")


@icon("school-garden", CAT, "Raised garden bed with sprouts and a small sign stake",
      tags=["school garden", "raised bed", "planting", "gardening", "outdoor learning", "vegetable patch"])
def _(S):
    parts = [
        shell(rect(2, 15, 20, 6.5, rr(S, 1.5))),
        detail(seg(2, 18.25, 22, 18.25)),
        shell(rect(15, 3, 6.5, 4.5, rr(S, 1.25))), line(seg(18.25, 7.5, 18.25, 15)),
    ]
    mir = lambda d, x: path_to_d(transform_path(P(d), (-1, 0, 0, 1, 2 * x, 0)))
    for x in (5.5, 11):
        lf = (poly([(x - 0.25, 11), (x - 1.5, 7.5), (x - 4, 6.5), (x - 3, 9.5)], closed=True) if S.name == "line"
              else _leaf(x - 0.25, 11, x - 4, 6.75, 0.3))
        parts += [line(seg(x, 15, x, 11)), mark(lf), mark(mir(lf, x))]
    return parts


@layered("rhythm-sticks", "Pair of ridged wooden rhythm sticks crossed in an X",
         tags=["rhythm sticks", "lummi sticks", "percussion", "music class", "beat", "instrument"])
def _(S):
    def stick(deg):
        body = rotd(rect(10, 1.5, 4, 21, L(S, 0.5, 2)), deg)
        ridges = [detail(rotd(seg(10, y, 14, y), deg)) for y in (4.5, 7.5, 16.5, 19.5)]
        return [shell(body), *ridges]
    return [stick(45), stick(-45)]





@icon("talent-show", CAT, "Stage between curtains with a microphone on a stand and a star above",
      tags=["talent show", "school concert", "performance", "stage", "open mic", "show"])
def _(S):
    curtain = "M2 2.5H7.5Q7.5 10 4.5 13V21.5H2Z" if S.name == "line" else "M2 2.5H7.5Q7.5 10 4.5 13V21.5H3.5A1.5 1.5 0 0 1 2 20Z"
    return [
        shell(curtain),
        shell(path_to_d(transform_path(P(curtain), (-1, 0, 0, 1, 24, 0)))),
        mark(poly(star(12, 4.25, 2.6, 1.15), closed=True, r=L(S, 0, 0.3))),
        shell(rect(10.5, 8.5, 3, 5, 1.5)),
        line(seg(12, 13.5, 12, 20.5)),
        line(seg(9.5, 21, 14.5, 21)),
    ]


@layered("yearbook-signing", "Open yearbook of photos with a pen writing a looped signature",
         tags=["yearbook", "signing", "autograph", "graduation", "end of year", "memories"])
def _(S):
    book = poly([(2, 8), (11, 9.5), (20, 8), (20, 20.5), (11, 22), (2, 20.5)], closed=True, r=S.r * 0.6)
    pen = rotd(rect(16.5, 0.5, 3, 11, L(S, 0.5, 1.5)), 35, 18, 6)
    return [
        [shell(pen)],
        [shell(book), detail(seg(11, 9.5, 11, 22)),
         mark(rect(4, 12, 2.75, 2.75)), mark(rect(4, 16.5, 2.75, 2.75)), mark(rect(7.5, 12.5, 1.5, 2.25)),
         detail("M12.5 17.5C13.5 14.5 15 14 15 15.5S13.5 18.5 15 18S17 15.5 18 16" if S.name == "rounded" else
                poly([(12.5, 17.5), (14, 14.5), (15, 15.5), (14, 18.25), (16, 17), (18, 15.75)]))],
    ]


@layered("fossil-dig-kit", "Plaster block with a half exposed spiral shell fossil and a brush on top",
         tags=["fossil dig", "excavation kit", "paleontology", "palaeontology", "ammonite", "science kit"])
def _(S):
    return [
        [shell(rect(12, 2.5, 8, 4.5, rr(S, 1.5))), detail(seg(14.75, 2.5, 14.75, 7)), detail(seg(17.25, 2.5, 17.25, 7)),
         line(seg(3, 4.75, 12, 4.75))],
        [shell(rect(2.5, 9.5, 19, 12, rr(S, 2))),
         detail(poly(spiral(11, 15.75, 0.5, 3.75, 1.2, a0=0))),
         detail(seg(17, 13, 18.5, 12)), detail(seg(16.5, 17.5, 18.5, 18.5))],
    ]


@icon("straw-rocket", CAT, "Paper rocket with fins slid onto a bendy drinking straw",
      tags=["straw rocket", "paper rocket", "stem", "science project", "launch", "air pressure"])
def _(S):
    deg = 45
    up = [(12, 2), (14.5, 5.5), (14.5, 10), (16.5, 12.5), (16.5, 13.5), (7.5, 13.5), (7.5, 12.5), (9.5, 10), (9.5, 5.5)]
    return [
        shell(poly(rotp(up, deg, 13.5, 10.5), closed=True, r=S.r * 0.4), stroke_miterlimit="2"),
        line(poly([rotp([(12, 13.5)], deg, 13.5, 10.5)[0], (7, 17.5), (7, 21.5)], r=S.r * 1.3)),
    ]


@icon("greater-than-alligator", CAT, "Alligator head with open jaws making a greater than sign",
      tags=["greater than", "alligator math", "crocodile", "comparing numbers", "inequality", "math"])
def _(S):
    upper = poly([(3, 3), (20.5, 9.5), (20.5, 11.5), (3.5, 6)], closed=True, r=S.r * 0.3)
    lower = poly([(3, 21), (20.5, 14.5), (20.5, 12.5), (3.5, 18)], closed=True, r=S.r * 0.3)
    head = union(upper, lower, rect(15.5, 8.5, 6, 7, 0), circle(17.5, 8, 2.75))
    return [
        shell(head, stroke_miterlimit="2"),
        dot(17.5, 8.25, 1.1),
        mark(poly([(7, 7.2), (9, 7.9), (7.9, 9.4)], closed=True)),
        mark(poly([(11, 8.7), (13, 9.4), (11.9, 10.9)], closed=True)),
        mark(poly([(7, 16.8), (9, 16.1), (7.9, 14.6)], closed=True)),
        mark(poly([(11, 15.3), (13, 14.6), (11.9, 13.1)], closed=True)),
    ]


@icon("marble-painting", CAT, "Shallow tray with a marble rolling looping paint trails",
      tags=["marble painting", "process art", "painting", "art class", "early years", "craft"])
def _(S):
    trail = "M5.5 16C4.5 11 9 7.5 11 10.5S9 16.5 12.5 16S16 8 18.5 9.5"
    return [
        shell(rect(2.5, 3.5, 19, 17, rr(S, 2.5))),
        detail(trail if S.name == "rounded" else poly([(5.5, 16), (6, 10), (10.5, 8.5), (10.5, 13.5), (12.5, 16), (15, 10), (17.5, 9)])),
        dot(17.75, 15, 2),
    ]


@layered("clothespin-butterfly", "Wooden clothespin clipped through the middle of paper butterfly wings",
         tags=["clothespin butterfly", "craft", "paper butterfly", "art and craft", "kids craft", "clothes peg"])
def _(S):
    up = poly([(10, 11), (5, 4), (2.5, 5), (2.5, 10.5), (4, 12)], closed=True, r=S.r * 0.6)
    lo = poly([(10, 14), (4.5, 15), (4, 19), (6, 20.5), (10, 17)], closed=True, r=S.r * 0.6)
    mir = (-1, 0, 0, 1, 24, 0)
    return [
        [shell(rect(10.25, 4.5, 3.5, 17, rr(S, 1.75))), detail(seg(10.25, 10, 13.75, 10)),
         line(poly([(11, 4.5), (9, 2)], r=0)), line(poly([(13, 4.5), (15, 2)], r=0))],
        [shell(up), shell(lo), shell(path_to_d(transform_path(P(up), mir))), shell(path_to_d(transform_path(P(lo), mir)))],
    ]


@layered("worry-box", "Box with a folded note with a squiggle going into the slot in its lid",
         tags=["worry box", "worries", "anxiety", "wellbeing", "feelings", "mental health"])
def _(S):
    return [
        [shell(rect(3, 11, 18, 10.5, rr(S, 2))), detail(seg(8.5, 14.5, 15.5, 14.5))],
        [shell(rotd(rect(8.5, 2.5, 7, 10, L(S, 0, 1)), -10, 12, 8)),
         detail(rotd("M10.5 6Q11.5 4.5 12.5 6T14 6", -10, 12, 8))],
    ]


@layered("breathing-ball", "Expanding ball of linked segments held between two hands",
         tags=["breathing ball", "hoberman sphere", "mindfulness", "breathing exercise", "calm", "expanding ball"])
def _(S):
    hex_pts = regular(12, 12, 3.25, 6, start=-90)
    spokes = [detail(seg(*hex_pts[i], *polar(12, 12, 7, -90 + i * 60))) for i in range(6)]
    hand_l = "M2 18V9A1.5 1.5 0 0 1 5 9V18Z" if S.name == "rounded" else rect(2, 7.5, 3, 10.5)
    hand_r = path_to_d(transform_path(P(hand_l), (-1, 0, 0, 1, 24, 0)))
    return [
        [shell(circle(12, 12, 7)), detail(poly(hex_pts, closed=True, r=S.r * 0.3)), *spokes],
        [shell(hand_l), shell(hand_r)],
    ]


@layered("pinafore-dress", "Sleeveless pinafore dress with a square neckline over a collared blouse",
         tags=["pinafore", "school dress", "school uniform", "jumper dress", "gymslip", "tunic"])
def _(S):
    dress = poly([(7.5, 4.5), (9.5, 4.5), (9.5, 9), (14.5, 9), (14.5, 4.5), (16.5, 4.5), (16.5, 11), (19.5, 21.5), (4.5, 21.5), (7.5, 11)], closed=True, r=S.r * 0.6)
    blouse = poly([(8, 2.5), (3, 5.5), (4.5, 10), (7.5, 9), (16.5, 9), (19.5, 10), (21, 5.5), (16, 2.5)], closed=True, r=S.r * 0.6)
    return [
        [shell(dress)],
        [shell(blouse), detail(poly([(9.5, 2.5), (12, 5.5), (14.5, 2.5)], r=S.r * 0.3))],
    ]


@layered("quoits", "Peg on a small base with one rubber ring around it and one beside it",
         tags=["quoits", "ring toss", "hoopla", "sports day", "throwing game", "playground game"])
def _(S):
    return [
        [line(arc(15.5, 14.5, 4.5, 20, 160))],
        [shell(rect(14.25, 3, 2.5, 16, 1.25)), shell(rect(10.5, 18.5, 10, 3, rr(S, 1.5))),
         line(arc(15.5, 14.5, 4.5, 160, 380))],
        [line(circle(5.5, 16.5, 3.25))],
    ]


# ============================================================================ milestones, results and lessons

@icon("hundredth-day-of-school", CAT, "Number 100 with a party hat on the 1 and confetti",
      tags=["100th day", "hundredth day", "100 days of school", "celebration", "milestone", "party"])
def _(S):
    zero = (lambda cx: ellipse(cx, 15.5, 2.75, 4.5)) if S.name == "rounded" else (lambda cx: rect(cx - 2.75, 11, 5.5, 9, 1.5))
    return [
        shell(poly([(2.5, 9), (4.5, 3), (6.5, 9)], closed=True, r=S.r * 0.4), stroke_miterlimit="2"),
        line(poly([(2.5, 12.5), (4.5, 11.25), (4.5, 20)], r=S.r * 0.3)),
        shell(zero(10.75)), shell(zero(18.5)),
        dot(10, 4.5, 1), dot(14.5, 6.5, 1), dot(17.5, 3, 1), dot(21, 6.5, 1),
    ]





@layered("results-envelope", "Opened envelope with a results sheet showing a grade A",
         tags=["exam results", "results day", "grades", "report", "envelope", "letter"])
def _(S):
    return [
        [shell(rect(2.5, 12, 19, 9.5, rr(S, 2))), detail(poly([(2.5, 12.5), (12, 17.5), (21.5, 12.5)], r=S.r * 0.4))],
        [shell(rect(6, 2.5, 12, 12, L(S, 0, 1.5))),
         detail(poly([(9.75, 11), (12, 5.5), (14.25, 11)], r=S.r * 0.3)), detail(seg(10.75, 9, 13.25, 9))],
    ]


@layered("nature-scavenger-hunt", "Checklist of ticked items with a leaf beside it",
         tags=["scavenger hunt", "nature walk", "checklist", "outdoor learning", "forest school", "treasure hunt"])
def _(S):
    leaf = _leaf(12.5, 21.5, 21.5, 11, 0.32)
    return [
        [shell(leaf), detail(seg(14.5, 19.5, 18.5, 14.5))],
        [shell(rect(2.5, 2.5, 13, 17, rr(S, 2.5))),
         *[detail(poly([(5, y), (6.25, y + 1.25), (8.25, y - 1.25)], r=S.r * 0.3)) for y in (6.5, 11)],
         detail(seg(10, 6.5, 13, 6.5)), detail(seg(10, 11, 13, 11)), detail(rect(5, 14.25, 2.5, 2.5, 0))],
    ]


@icon("video-magnifier", CAT, "Screen on a stand showing an enlarged letter above a reading tray",
      tags=["video magnifier", "cctv magnifier", "low vision", "magnifier", "visual impairment", "reading aid"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 16, 11, rr(S, 2))),
        detail(poly([(10.5, 11), (13.5, 5), (16.5, 11)], r=S.r * 0.3)), detail(seg(11.75, 9, 15.25, 9)),
        line(seg(8, 13.5, 8, 18.5)),
        shell(rect(2.5, 18.5, 19, 3, rr(S, 1.5))),
        mark(rect(14.5, 13.5, 3, 2, 0)),
    ]


@icon("economics-class", CAT, "Chalkboard graph with a rising and a falling line crossing at a point",
      tags=["economics", "supply and demand", "market", "equilibrium", "graph", "business studies"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 15.5, rr(S, 2))),
        detail(poly([(6, 6), (6, 15), (18.5, 15)], r=S.r * 0.3)),
        detail(seg(9, 12.5, 18, 6)), detail(seg(9, 6, 18, 12.5)),
        line(seg(5, 21, 19, 21)),
    ]


@icon("solar-system-mobile", CAT, "Hanging ring with a sun and planets dangling on strings",
      tags=["solar system", "planet mobile", "space project", "planets", "science project", "astronomy"])
def _(S):
    return [
        line(seg(12, 2, 12, 4)),
        line(ellipse(12, 6, 9, 2)),
        line(seg(12, 8, 12, 10.5)), shell(circle(12, 14, 3.5)),
        line(seg(4.5, 8, 4.5, 13)), dot(4.5, 15, 2),
        line(seg(19.5, 8, 19.5, 15.5)), shell(circle(19.5, 18.5, 2.5)),
    ]


@icon("star-jump", CAT, "Figure jumping with arms and legs spread wide in an X",
      tags=["star jump", "jumping jack", "exercise", "pe", "warm up", "fitness"], aliases=["jumping-jack"])
def _(S):
    return [
        dot(12, 4, 2.25),
        line(poly([(4, 3.5), (12, 10), (20, 3.5)], r=S.r)),
        line(seg(12, 10, 12, 14)),
        line(poly([(5, 21.5), (12, 14), (19, 21.5)], r=S.r)),
    ]


@icon("shuttle-run", CAT, "Runner between two cones with a double headed arrow",
      tags=["shuttle run", "beep test", "sprint", "pe", "agility", "fitness test"])
def _(S):
    return [
        dot(14, 3.5, 2),
        line(poly([(8.5, 8.5), (11, 7), (15, 8.5), (16.5, 11)], r=S.r * 0.6)),
        line(poly([(12.5, 7.5), (10.5, 12.5), (8, 15)], r=S.r * 0.6)),
        line(poly([(10.5, 12.5), (14, 13.5), (14.5, 15.5)], r=S.r * 0.6)),
        shell(poly([(2, 21.5), (3.75, 16.5), (5.5, 21.5)], closed=True, r=S.r * 0.3)),
        shell(poly([(18.5, 21.5), (20.25, 16.5), (22, 21.5)], closed=True, r=S.r * 0.3)),
        line(seg(8.5, 19.5, 15.5, 19.5)),
        solid(poly([(7, 19.5), (9.5, 17.75), (9.5, 21.25)], closed=True)),
        solid(poly([(17, 19.5), (14.5, 17.75), (14.5, 21.25)], closed=True)),
    ]


@icon("sit-and-reach", CAT, "Seated figure reaching over straight legs toward a box with a ruler",
      tags=["sit and reach", "flexibility test", "hamstring stretch", "pe", "fitness test", "stretching"])
def _(S):
    return [
        dot(10.5, 9, 2.25),
        line(poly([(3, 20), (7.5, 14), (13, 12.5)], r=S.r)),
        line(seg(3, 20, 14, 20)),
        shell(rect(16, 15, 5.5, 6.5, rr(S, 1.5))),
        shell(rect(14.5, 11.5, 7.5, 1.5, 0) if S.name == "line" else rect(14.5, 11.5, 7.5, 1.5, 0.75)),
    ]


@icon("hole-reinforcement", CAT, "Punched ruled sheet with a ring sticker around one hole",
      tags=["hole reinforcement", "reinforcement ring", "binder paper", "punched holes", "stationery", "ring binder"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 2))),
        dot(7, 6, 1.25), dot(7, 18, 1.25),
        dot(7, 12, 1.25), detail(circle(7, 12, 2.75)),
        detail(seg(12, 6, 21.5, 6)), detail(seg(12, 12, 21.5, 12)), detail(seg(12, 18, 21.5, 18)),
    ]


@icon("school-sign", CAT, "Sign board on two posts with a school building symbol and text",
      tags=["school sign", "school entrance", "signage", "campus", "welcome sign", "school name"])
def _(S):
    return [
        shell(rect(2, 4.5, 20, 11, rr(S, 2))),
        mark(poly([(4.5, 13), (4.5, 9.5), (7.5, 7), (10.5, 9.5), (10.5, 13)], closed=True, r=S.r * 0.3)),
        detail(seg(13, 8.5, 19, 8.5)), detail(seg(13, 11.5, 17, 11.5)),
        line(seg(6, 15.5, 6, 21.5)), line(seg(18, 15.5, 18, 21.5)),
    ]


# ============================================================================ uniforms, calm and study




@icon("star-breathing", CAT, "Star outline with arrows showing breath traced up and down its edges",
      tags=["star breathing", "breathing exercise", "mindfulness", "calm down", "self regulation", "relaxation"])
def _(S):
    pts = star(12, 13, 9, 3.9)
    return [
        shell(poly(pts, closed=True, r=S.r * 0.4), stroke_miterlimit="2"),
        solid(poly(rotp([(6.8, 5.6), (9.3, 5.6), (8.05, 3.4)], -25, 8.05, 4.8), closed=True)),
        solid(poly(rotp([(14.7, 3.4), (17.2, 3.4), (15.95, 5.6)], 25, 15.95, 4.5), closed=True)),
    ]


@layered("touch-and-feel-book", "Board book with a fuzzy patch on its cover and a hand touching it",
         tags=["touch and feel", "sensory book", "board book", "baby book", "tactile", "texture"])
def _(S):
    fuzz = poly(star(11.5, 9.5, 3.75, 2.6, n=10), closed=True, r=L(S, 0, 0.3))
    finger = rotd(rect(14, 9.5, 3, 8, 1.5), -35, 15.5, 13)
    palm = rotd(rect(13.5, 15, 6.5, 6, L(S, 1.5, 3)), -35, 15.5, 13)
    return [
        [shell(union(finger, palm))],
        [shell(rect(2.5, 2.5, 16, 18, rr(S, 2.5))), detail(seg(6, 2.5, 6, 20.5)), detail(fuzz)],
    ]


@layered("past-papers", "Stack of three offset exam papers with a year label on the front sheet",
         tags=["past papers", "exam practice", "revision", "past exams", "test prep", "worksheets"])
def _(S):
    return [
        [shell(rect(2.5, 9, 12, 12.5, rr(S, 2))), mark(rect(9, 11.5, 3.5, 2.5, L(S, 0, 0.75))),
         detail(seg(5, 16, 12, 16)), detail(seg(5, 19, 10, 19))],
        [shell(rect(6, 5.75, 12, 12.5, rr(S, 2)))],
        [shell(rect(9.5, 2.5, 12, 12.5, rr(S, 2)))],
    ]


@icon("brain-dump", CAT, "Head in profile with an arrow flowing from the top onto a page of scribbles",
      tags=["brain dump", "mind dump", "journaling", "unload thoughts", "note taking", "revision"])
def _(S):
    head = poly([(4.5, 21.5), (3.5, 16.5), (2.5, 12), (4, 8), (8, 7), (11, 8.5), (12, 11.5), (13, 13.5), (11.5, 14.5), (11.5, 16.5), (8.5, 17), (8.5, 21.5)],
                r=S.r * 0.9)
    return [
        line(head),
        line("M7 4.5C9.5 2 15 2 17.5 6" if S.name == "rounded" else poly([(7, 4.5), (11, 2.5), (15, 3), (17.5, 6)])),
        solid(poly(rotp([(17.5, 8.5), (15.4, 5.6), (19.6, 5.6)], -30, 17.5, 7), closed=True)),
        shell(rect(15, 10, 7, 11.5, rr(S, 1.5))),
        detail(seg(17, 13.5, 20, 13.5)), detail(seg(17, 17, 19, 17)),
    ]


@icon("fraction-pizza", CAT, "Pizza cut into eight slices with one slice pulled out and shaded",
      tags=["fraction pizza", "fractions", "one eighth", "math", "equal parts", "pizza"])
def _(S):
    c, r = (11, 13), 8
    a0, a1 = -90, -45
    p0, p1 = polar(*c, r, a0), polar(*c, r, a1)
    body = f"M{fmt(c[0])} {fmt(c[1])}L{fmt(p1[0])} {fmt(p1[1])}A{r} {r} 0 1 1 {fmt(p0[0])} {fmt(p0[1])}Z"
    off = polar(0, 0, 3, -67.5)
    q0, q1 = polar(c[0] + off[0], c[1] + off[1], r - 0.5, a0), polar(c[0] + off[0], c[1] + off[1], r - 0.5, a1)
    sl = f"M{fmt(c[0] + off[0])} {fmt(c[1] + off[1])}L{fmt(q0[0])} {fmt(q0[1])}A{r - 0.5} {r - 0.5} 0 0 1 {fmt(q1[0])} {fmt(q1[1])}Z"
    return [
        shell(body, stroke_miterlimit="2"),
        *[detail(seg(*c, *polar(*c, r, a))) for a in (0, 45, 90, 135, 180, 225)],
        solid(sl) if S.name == "line" else solid(path_to_d(U(P(sl), ST(sl, 1.0, "round", "round")))),
    ]


@layered("balloon-car", "Toy car with an inflated balloon on top, its neck pointing backward",
         tags=["balloon car", "balloon powered car", "stem", "science project", "newton's third law", "toy car"])
def _(S):
    return [
        [shell(circle(6.5, 19, 2.5)), shell(circle(16.5, 19, 2.5))],
        [shell(rect(2.5, 13, 18, 5, rr(S, 2)))],
        [shell(ellipse(14.5, 7, 6, 4.25)), shell(poly([(8.75, 6), (5.5, 7), (8.75, 8.5)], closed=True, r=S.r * 0.3)),
         line(seg(12, 11, 12, 13))],
    ]


@icon("dressing-frame", CAT, "Square wooden frame holding two fabric flaps fastened with buttons",
      tags=["dressing frame", "button frame", "montessori", "fine motor", "self care", "buttoning"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 2.5))),
        detail(rect(6, 6, 12, 12, L(S, 0, 1))),
        detail(seg(11, 6, 11, 18)),
        dot(14.25, 9, 1.25), dot(14.25, 12, 1.25), dot(14.25, 15, 1.25),
    ]


@layered("knobbed-cylinders", "Wooden block holding a row of shrinking cylinders with knobs",
         tags=["knobbed cylinders", "montessori", "cylinder block", "size sorting", "fine motor", "sensorial"])
def _(S):
    k = L(S, 0, 0.75)
    cyl = []
    x = 3.25
    b = 17.5
    for w, h in ((4, 11), (3.25, 9.5), (2.5, 8), (2, 6.5)):
        cx = x + w / 2
        knob = circle(cx, b - h - 1.6, 1.2) if S.name == "rounded" else rect(cx - 1.1, b - h - 2.8, 2.2, 2.2)
        cyl.append(mark(union(rect(x, b - h, w, h + 1, k), knob, rect(cx - 0.5, b - h - 1.6, 1, 1.8))))
        x += w + 2
    return [
        [shell(rect(2, 17, 20, 4.5, rr(S, 1.5)))],
        cyl,
    ]


@icon("insulated-lunch-bag", CAT, "Soft zippered lunch bag with a quilted front and a carry handle",
      tags=["lunch bag", "cool bag", "insulated bag", "packed lunch", "lunch box", "school lunch"])
def _(S):
    return [
        line(poly([(8.5, 8), (8.5, 3.5), (15.5, 3.5), (15.5, 8)], r=S.r)),
        shell(rect(3, 8, 18, 13.5, rr(S, 3))),
        detail(seg(3, 11.5, 21, 11.5)),
        detail(seg(7, 11.5, 15, 21.5)), detail(seg(17, 11.5, 9, 21.5)),
    ]


@icon("big-key-keyboard", CAT, "Chunky keyboard with a few oversized keys",
      tags=["big keys", "large key keyboard", "accessible keyboard", "assistive technology", "early learning", "keyboard"])
def _(S):
    k = L(S, 0, 0.75)
    return [
        shell(rect(2, 5.5, 20, 13, rr(S, 2.5))),
        *[mark(rect(x, y, 4, 3.5, k)) for x in (4.5, 10, 15.5) for y in (8, 13)],
    ]





@layered("chair-kick-band", "Chair with a stretchy band between its front legs and a foot pushing it",
         tags=["chair band", "kick band", "fidget band", "bouncy band", "sensory", "adhd"])
def _(S):
    return [
        [shell(ellipse(12, 19, 2.75, 2) if S.name == "rounded" else rect(9.25, 17, 5.5, 4, 0.5))],
        [line(poly([(5.5, 15), (12, 17), (18.5, 15)], r=S.r))],
        [shell(rect(6, 2.5, 12, 6, rr(S, 2))), shell(rect(3.5, 9.5, 17, 3, rr(S, 1.5))),
         line(seg(5.5, 12.5, 5.5, 21.5)), line(seg(18.5, 12.5, 18.5, 21.5))],
    ]


@icon("fine-motor-tongs", CAT, "Small tongs picking up a pom pom above a tray of sorting cups",
      tags=["tongs", "fine motor", "sorting", "pom poms", "occupational therapy", "early years"])
def _(S):
    return [
        line(poly([(21.5, 3), (12.5, 8.5)], r=0)),
        line(poly([(21.5, 3), (14.5, 12.5)], r=0)),
        shell(circle(10.5, 11.5, 2.25)),
        shell(rect(2.5, 16.5, 19, 5, rr(S, 1.5))),
        detail(seg(9, 16.5, 9, 21.5)), detail(seg(15, 16.5, 15, 21.5)),
    ]


@layered("lacing-beads", "Cube, ball and cylinder beads threaded on a lace with a stiff tip",
         tags=["lacing beads", "threading beads", "fine motor", "stringing beads", "toddler toy", "early years"])
def _(S):
    return [
        [shell(rotd(rect(3, 14.5, 5, 5, rr(S, 1)), -40, 5.5, 17)),
         shell(circle(11.5, 11.5, 3)),
         shell(rotd(rect(15, 5, 5, 4, rr(S, 1)), -40, 17.5, 7))],
        [line("M2 21.5Q6 20 8.5 15.5T20.5 3.5" if S.name == "rounded" else poly([(2, 21.5), (21, 3)])),
         solid(path_to_d(ST(seg(20, 4.5, 21.75, 2.25), 3, "butt" if S.name == "line" else "round", "round")))],
    ]


@layered("cutting-practice", "Worksheet with dashed zigzag and straight lines and child scissors cutting along one",
         tags=["cutting practice", "scissor skills", "fine motor", "worksheet", "preschool", "cutting lines"])
def _(S):
    zig = [seg(5, 8, 6.5, 6), seg(8.5, 6, 10, 8), seg(12, 8, 13.5, 6)]
    wav = [seg(5, 13, 6.75, 13), seg(8.75, 13, 10.5, 13)]
    return [
        [line(circle(14.5, 19, 2.25)), line(circle(19.5, 15, 2.25)),
         line(poly([(16, 17.25), (10, 12)], r=0)), line(poly([(17.5, 14.25), (11.5, 10.75)], r=0))],
        [shell(rect(2.5, 2.5, 14, 18, rr(S, 2))), *[detail(z) for z in zig], *[detail(w) for w in wav]],
    ]


@layered("dress-up-trunk", "Open trunk with a crown sitting on its edge",
         tags=["dress up", "dressing up box", "costume trunk", "pretend play", "role play", "costumes"])
def _(S):
    crown = poly([(6, 12.5), (5.5, 7.5), (8.25, 9.75), (10.5, 6.5), (12.75, 9.75), (15.5, 7.5), (15, 12.5)], closed=True, r=S.r * 0.3)
    return [
        [shell(crown, stroke_miterlimit="2")],
        [shell(rect(2.5, 12.5, 19, 9, rr(S, 2))), detail(seg(2.5, 16, 21.5, 16)), dot(12, 16, 1.5)],
        [shell(poly([(3.5, 12.5), (5, 3), (19, 3), (20.5, 12.5)], closed=True, r=S.r * 0.6))],
    ]
