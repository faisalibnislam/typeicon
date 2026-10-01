"""TypeIcon Core: classroom (batch classroom_003).

Classroom activities, science demonstrations, school events and learning aids, drawn from the objects
themselves. Front or side views; small parts sit inside a clear silhouette so they survive at 16 px.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, rotation, transform_path  # noqa: F401

CAT = "classroom"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx=12.0, cy=12.0):
    """Rotate a closed outline clockwise on screen about (cx, cy)."""
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rot_pts(points, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in points]


def behind(back_d, fronts, gap=1.75):
    """Outline of the part of back_d not hidden by the front shapes, kept `gap` clear of their strokes."""
    cut = U(*[U(P(f), ST(f, 2 * (gap + 2), "round", "round")) for f in fronts])
    return path_to_d(D(P(back_d), cut))


def stroke_cut(d, S, cutters, gap=1.5, w=2.0):
    """A stroke along d drawn as a solid mark, with gaps cut around the cutter strokes (for crossings)."""
    reg = ST(d, w, S.cap, S.join)
    cut = U(*[ST(c, 2 + 2 * gap, "round", "round") for c in cutters])
    return Part("dot", path_to_d(D(reg, cut)))


def pt_on(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def heart(cx, cy, w):
    """Heart outline of width w, centred horizontally on cx; cy is the height of the top notch."""
    r = w / 4
    k = 0.7071
    p1 = (cx - r - k * r, cy + k * r)
    p2 = (cx + r + k * r, cy + k * r)
    b = (cx, cy + 2.35 * r)
    return (f"M{fmt(b[0])} {fmt(b[1])}L{fmt(p1[0])} {fmt(p1[1])}A{fmt(r)} {fmt(r)} 0 1 1 {fmt(cx)} {fmt(cy)}"
            f"A{fmt(r)} {fmt(r)} 0 1 1 {fmt(p2[0])} {fmt(p2[1])}Z")


def drop(cx, cy, r):
    """Teardrop pointing up; round bottom centred on (cx, cy)."""
    top = (cx, cy - 2.4 * r)
    a1 = (cx - r * 0.87, cy - r * 0.5)
    a2 = (cx + r * 0.87, cy - r * 0.5)
    return (f"M{fmt(top[0])} {fmt(top[1])}L{fmt(a1[0])} {fmt(a1[1])}A{fmt(r)} {fmt(r)} 0 1 0 {fmt(a2[0])} {fmt(a2[1])}Z")


def star(cx, cy, ro, ri, rnd=0.0):
    pts = []
    for i in range(10):
        ang = -90 + i * 36
        rad = ro if i % 2 == 0 else ri
        pts.append((cx + rad * math.cos(math.radians(ang)), cy + rad * math.sin(math.radians(ang))))
    return poly(pts, closed=True, r=rnd)


def capsule(x1, y1, x2, y2, w):
    return path_to_d(ST(seg(x1, y1, x2, y2), w, "round", "round"))


def bar(x1, y1, x2, y2, w):
    return path_to_d(ST(seg(x1, y1, x2, y2), w, "butt", "miter"))


def wave(x0, x1, y, amp, n):
    """Smooth wave line from x0 to x1 made of n half waves."""
    step = (x1 - x0) / n
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        xa = x0 + i * step
        sgn = -1 if i % 2 == 0 else 1
        d += f"Q{fmt(xa + step / 2)} {fmt(y + sgn * amp * 2)} {fmt(xa + step)} {fmt(y)}"
    return d


# ============================================================================ rewards, passes and events

def mortarboard(cx, top, w, S):
    """Mortarboard region: flat diamond board (width w) over a skull cap."""
    h = w * 0.36
    board = poly([(cx - w / 2, top + h / 2), (cx, top), (cx + w / 2, top + h / 2), (cx, top + h)], closed=True,
                 r=L(S, 0, 0.6))
    cw = w * 0.5
    skull = poly([(cx - cw / 2, top + h * 0.6), (cx + cw / 2, top + h * 0.6), (cx + cw / 2, top + h * 1.45),
                  (cx - cw / 2, top + h * 1.45)], closed=True, r=L(S, 0, 1))
    return union(board, skull)


@icon("homework-pass", CAT, "Notched ticket with a crossed out pencil for skipping one homework task",
      tags=["homework pass", "reward", "coupon", "no homework", "ticket", "classroom reward"])
def _(S):
    tk = minus(rect(2.5, 5, 19, 14, rr(S, 3)), circle(2.5, 12, 2.3), circle(21.5, 12, 2.3))
    pts = rot_pts([(6, 12), (9, 10.2), (18.2, 10.2), (18.2, 13.8), (9, 13.8)], -38)
    pencil = poly(pts, closed=True, r=L(S, 0, 0.6))
    slash = seg(7.6, 8, 16.4, 16)
    cut = ST(slash, 2 + 2 * 1.0, "round", "round")
    return [shell(tk), mark(path_to_d(D(P(pencil), cut))), detail(slash)]


@icon("buddy-bench", CAT, "Bench with a heart on its backrest where children sit to find a playmate",
      tags=["buddy bench", "friendship bench", "playground", "kindness", "recess", "friends"])
def _(S):
    return [
        shell(rect(3, 3, 18, 9, rr(S, 3))),
        detail(heart(12, 6.2, 6.5)),
        line(seg(2, 15.5, 22, 15.5)),
        line(seg(5.5, 13, 5.5, 21)), line(seg(18.5, 13, 18.5, 21)),
    ]


@icon("brag-tags", CAT, "Ball chain with star, heart and round reward tags",
      tags=["brag tags", "reward tags", "dog tags", "achievement", "charms", "necklace"])
def _(S):
    parts = []
    n = 12
    for i in range(n + 1):
        x = 3 + 18 * i / n
        y = 2 + 5 * (1 - ((x - 12) / 9) ** 2)
        parts.append(dot(x, y, 0.95))
    parts += [
        shell(heart(12, 15.6, 6.6)), line(seg(12, 8.6, 12, 13.4)),
        shell(circle(4.8, 11.2, 2.6)),
        shell(star(18.8, 11.8, 3.1, 1.55, L(S, 0, 0.6))),
    ]
    return parts


@icon("graduation-yard-sign", CAT, "Lawn sign on wire stakes showing a mortarboard and a class year",
      tags=["graduation sign", "yard sign", "lawn sign", "graduate", "class of", "commencement"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 13.5, rr(S, 3))),
        mark(mortarboard(12, 4.8, 10, S)),
        detail(seg(8, 13, 16, 13)),
        line(seg(7, 16, 7, 21.5)), line(seg(17, 16, 17, 21.5)),
    ]


@icon("graduation-bunting", CAT, "String of pennants above a mortarboard for a graduation party",
      tags=["graduation bunting", "banner", "pennants", "party decoration", "graduate", "celebration"])
def _(S):
    def yq(x):
        t = (x - 2) / 20
        return (1 - t) ** 2 * 2.5 + 2 * t * (1 - t) * 6 + t * t * 2.5
    rp = L(S, 0, 0.8)
    parts = []
    xs = [(2.6, 7), (9.8, 14.2), (17, 21.4)]
    for a, b in xs:
        parts.append(shell(poly([(a, yq(a)), (b, yq(b)), ((a + b) / 2, yq((a + b) / 2) + 5)], closed=True, r=rp)))
    parts.append(line(seg(2, yq(2), 2.6, yq(2.6))))
    for (a0, b0), (a1, b1) in zip(xs, xs[1:]):
        parts.append(line(f"M{fmt(b0)} {fmt(yq(b0))}Q{fmt((b0 + a1) / 2)} {fmt(yq((b0 + a1) / 2) + 0.4)} {fmt(a1)} {fmt(yq(a1))}"))
    parts.append(line(seg(21.4, yq(21.4), 22, yq(22))))
    parts.append(shell(mortarboard(12, 12.2, 17, S)))
    parts.append(line("M20.5 15.3V20.5"))
    return parts


@icon("exam-admit-card", CAT, "Exam hall pass card with a header bar, photo box and barcode",
      tags=["admit card", "hall ticket", "exam pass", "admission card", "exam entry", "id card"])
def _(S):
    parts = [
        shell(rect(2.5, 4, 19, 16, rr(S, 3))),
        detail(seg(2.5, 8.5, 21.5, 8.5)),
        detail(rect(5.5, 11.5, 5, 5.5, L(S, 0, 1.2))),
        detail(seg(13.5, 12.2, 18.5, 12.2)),
    ]
    for x0, w in ((13, 1.2), (15.2, 1.2), (17.4, 1.2)):
        parts.append(mark(rect(x0 + 0.2, 14.6, w, 2.8)))
    return parts


# ============================================================================ maths

@icon("coordinate-grid", CAT, "Grid with x and y axes crossing at the centre and one plotted point",
      tags=["coordinate grid", "cartesian plane", "graph", "quadrants", "plot point", "axes"])
def _(S):
    parts = []
    for v in (6.5, 17.5):
        parts.append(detail(seg(3, v, 20, v)))
        parts.append(detail(seg(v, 4, v, 21)))
    ah = L(S, 0, 0.5)
    parts += [
        line(seg(2, 12, 20.5, 12)), line(seg(12, 22, 12, 3.5)),
        solid(poly([(22.5, 12), (19.5, 9.6), (19.5, 14.4)], closed=True, r=ah)),
        solid(poly([(12, 1.5), (9.6, 4.5), (14.4, 4.5)], closed=True, r=ah)),
        dot(17.5, 6.5, 2.4),
    ]
    return parts


# ============================================================================ science demonstrations

@icon("rain-cloud-in-a-jar", CAT, "Jar of water with a foam cloud on top and drops falling through",
      tags=["rain cloud jar", "science experiment", "weather", "shaving cream", "rain", "water cycle"])
def _(S):
    cloud = union(circle(8.3, 7, 2.7), circle(12, 5.2, 3.2), circle(15.7, 7, 2.7), rect(8.3, 6.5, 7.4, 3.2))
    jar = rect(5, 7, 14, 14.5, rr(S, 3))
    return [
        shell(cloud), shell(behind(jar, [cloud], 1.25)),
        mark(drop(9, 15, 1.1)), mark(drop(15, 14, 1.1)), mark(drop(12, 18.5, 1.1)),
    ]


@icon("magic-milk-experiment", CAT, "Plate of milk with colour bursts and a cotton swab touching the centre",
      tags=["magic milk", "science experiment", "food colouring", "dish soap", "surface tension", "milk"])
def _(S):
    plate = ellipse(12, 16, 10, 5.5)
    return [
        shell(plate),
        detail(ellipse(12, 16, 6.5, 3)),
        *[mark(circle(x, y, 1.15) if S.name == "rounded" else rect(x - 1.1, y - 1.1, 2.2, 2.2))
          for x, y in ((8.6, 16.3), (15.4, 16.3), (12, 18.1))],
        line(seg(18.4, 5, 14.4, 10.6)),
        shell(rot(ellipse(13.4, 12.2, 1.2, 1.9), 35, 13.4, 12.2)),
        shell(rot(ellipse(19.4, 3.6, 1.2, 1.9), 35, 19.4, 3.6)),
    ]


@icon("dancing-raisins", CAT, "Tall glass of fizzy water with raisins lifted by bubbles",
      tags=["dancing raisins", "science experiment", "carbonation", "bubbles", "fizzy water", "buoyancy"])
def _(S):
    glass = poly([(5.5, 3), (18.5, 3), (16.8, 21), (7.2, 21)], closed=True, r=S.r)
    return [
        shell(glass),
        detail(seg(6.2, 7, 17.8, 7)),
        mark(rot(ellipse(10, 17.5, 1.9, 1.3), 20, 10, 17.5)), mark(rot(ellipse(14, 12, 1.9, 1.3), -20, 14, 12)),
        mark(rot(ellipse(9.8, 10.5, 1.9, 1.3), 10, 9.8, 10.5)),
        dot(14, 17.5, 0.8), dot(13.4, 15, 0.7), dot(15, 9.2, 0.7), dot(10.5, 14, 0.7),
    ]


@icon("cartesian-diver", CAT, "Squeezed water bottle with a small pipette diver floating inside",
      tags=["cartesian diver", "science experiment", "buoyancy", "pressure", "pipette", "bottle"])
def _(S):
    bottle = poly([(9.5, 5), (14.5, 5), (14.5, 6.5), (17, 9), (17, 21), (7, 21), (7, 9), (9.5, 6.5)], closed=True, r=S.r)
    diver = rot(union(capsule(12, 12, 12, 13.2, 3), rect(11.3, 13.5, 1.4, 4.5)), 20, 12, 14)
    return [
        shell(rect(9, 1.8, 6, 1.6, L(S, 0, 0.8))),
        shell(bottle),
        detail(seg(7, 10, 17, 10)),
        mark(diver),
        line(poly([(2, 12), (4.2, 14.5), (2, 17)])), line(poly([(22, 12), (19.8, 14.5), (22, 17)])),
    ]


@icon("balloon-hovercraft", CAT, "Flat disc with a bottle cap and an inflated balloon on top",
      tags=["balloon hovercraft", "science project", "hovercraft", "air cushion", "friction", "stem"])
def _(S):
    body = union(circle(12, 6.3, 4.6), poly([(12, 10.6), (13.3, 12.1), (10.7, 12.1)], closed=True),
                 rect(10, 11.8, 4, 3, L(S, 0, 0.8)))
    return [
        shell(body), shell(ellipse(12, 16.6, 9.5, 2.2)),
        line(seg(4.5, 21.5, 7.5, 21.5)), line(seg(10.5, 21.5, 13.5, 21.5)), line(seg(16.5, 21.5, 19.5, 21.5)),
    ]


@icon("foil-boat-challenge", CAT, "Foil boat floating on water and loaded with stacks of coins",
      tags=["foil boat", "stem challenge", "buoyancy", "boat", "coins", "sink or float"])
def _(S):
    hull = poly([(2.5, 12.5), (21.5, 12.5), (18.5, 18), (5.5, 18)], closed=True, r=S.r * 0.6)

    def stack(cx, top, rx=3.2, ry=1.3):
        return union(ellipse(cx, top, rx, ry), rect(cx - rx, top, 2 * rx, 12.5 - top))
    s1, s2 = stack(8.8, 5), stack(15.2, 8)
    return [
        shell(hull), shell(behind(s1, [hull], 1.25)), shell(behind(s2, [hull, s1], 1.25)),
        detail(f"M5.6 5A3.2 1.3 0 0 0 12 5"), detail(f"M12 8A3.2 1.3 0 0 0 18.4 8"),
        line(wave(2, 22, 21, 0.6, 4)),
    ]


# ============================================================================ signs and sensory

@icon("school-bus-stop-sign", CAT, "Sign on a pole showing a school bus and a child waiting",
      tags=["school bus stop", "bus stop sign", "school bus", "pickup", "commute", "road sign"])
def _(S):
    bus = union(rect(5.8, 5, 9, 5.6, 1), circle(8, 10.6, 1.25), circle(12.6, 10.6, 1.25))
    bus = minus(bus, rect(7, 6.2, 2.6, 1.8, 0.3), rect(10.6, 6.2, 2.6, 1.8, 0.3))
    child = union(circle(17.3, 6, 1.3), capsule(17.3, 8.6, 17.3, 11, 2.4))
    return [
        shell(rect(3, 2, 18, 11.5, rr(S, 3))),
        mark(bus), mark(child),
        line(seg(12, 13.5, 12, 22)),
    ]


@icon("fiber-optic-lamp", CAT, "Lamp base with a fountain of glowing fibre strands with bright tips",
      tags=["fiber optic lamp", "sensory lamp", "sensory room", "night light", "glow", "fibre optic"])
def _(S):
    parts = [shell(poly([(7, 21.5), (17, 21.5), (15, 16.5), (9, 16.5)], closed=True, r=S.r * 0.6))]
    for ang in (-162, -130, -104, -76, -50, -18):
        tx, ty = pt_on(12, 15, 10, ang)
        sx, sy = pt_on(12, 15, 2.2, ang)
        parts.append(line(f"M{fmt(sx)} {fmt(sy)}L{fmt(tx)} {fmt(ty)}"))
        parts.append(dot(tx, ty, 1.7))
    return parts


# ============================================================================ access and support

@icon("gait-trainer", CAT, "Wheeled walking frame with a chest support and a seat sling for a child",
      tags=["gait trainer", "walker", "mobility aid", "special needs", "physical therapy", "walking frame"])
def _(S):
    frame = poly([(4.5, 18), (7, 8), (17, 8), (19.5, 18)], r=S.r)
    return [
        line(frame),
        shell(rect(8.5, 3, 7, 3.4, L(S, 1, 1.7))),
        line(seg(12, 6.4, 12, 8)),
        line("M8.2 12.5C9 15.2 15 15.2 15.8 12.5"),
        shell(circle(4.5, 20, 1.6)), shell(circle(19.5, 20, 1.6)),
    ]


@icon("classroom-fm-system", CAT, "Teacher lanyard microphone sending signal waves to a listener's ear",
      tags=["fm system", "hearing support", "assistive listening", "microphone", "hearing aid", "classroom audio"])
def _(S):
    return [
        line(poly([(2.5, 2), (5, 7.5), (7.5, 2)], r=S.r)),
        shell(rect(3, 8, 4, 8.5, L(S, 1.2, 2))),
        detail(seg(3, 12.3, 7, 12.3)),
        line(arc(8.5, 12.3, 2.8, -45, 45)), line(arc(8.5, 12.3, 5.6, -45, 45)),
        line("M15.8 10C15.8 7.4 17.6 5.5 19.4 5.5C21.2 5.5 22 7.2 22 9.2C22 11.8 20.4 12.8 19.8 14.8C19.4 16.4 18.8 18.5 16.6 18.5"),
        line("M18 11C18 9.6 18.7 8.9 19.6 9.1"),
    ]


@icon("tray-storage-unit", CAT, "Storage cabinet with shallow pull out trays, one tray slid half open",
      tags=["tray unit", "storage trays", "classroom storage", "drawers", "cabinet", "organizer"])
def _(S):
    cab = union(rect(3, 3, 13, 15.5, rr(S, 3)), rect(14, 9.5, 7.5, 3.5, L(S, 0, 1)))
    return [
        shell(cab),
        detail(seg(3, 7.5, 16, 7.5)), detail(seg(3, 15, 16, 15)),
        detail(seg(3, 11.25, 14, 11.25)),
        shell(circle(6, 20.8, 1.2)), shell(circle(13, 20.8, 1.2)),
    ]


def boot_up(x0, S):
    """Rain boot standing upright in side view, toe to the right."""
    r = L(S, 0.4, 1.4)
    return poly([(x0, 3.5), (x0 + 5, 3.5), (x0 + 5, 12.2), (x0 + 6.9, 13.4), (x0 + 7.9, 15.4), (x0 + 7.9, 18),
                 (x0 + 3.2, 18), (x0 + 3.2, 17.2), (x0 + 1.8, 17.2), (x0 + 1.8, 18), (x0, 18)], closed=True, r=r)


@icon("rain-boot-rack", CAT, "Rack holding a pair of rain boots off the floor to dry",
      tags=["boot rack", "wellies", "rain boots", "cloakroom", "boot drying", "mudroom"])
def _(S):
    return [
        shell(boot_up(2.4, S)), shell(boot_up(13.4, S)),
        detail(seg(2.4, 6.5, 7.4, 6.5)), detail(seg(13.4, 6.5, 18.4, 6.5)),
        line(seg(1.5, 20.5, 22.5, 20.5)),
    ]


@icon("randoseru", CAT, "Boxy stiff school backpack with a rounded flap lid and a buckle clasp",
      tags=["randoseru", "school bag", "backpack", "satchel", "japanese school bag", "rucksack"])
def _(S):
    handle = "M9.5 4V3A1 1 0 0 1 10.5 2H13.5A1 1 0 0 1 14.5 3V4" if S.name == "rounded" else "M9.5 4V2H14.5V4"
    return [
        shell(rect(4.5, 4, 15, 17, L(S, 2, 4))),
        detail("M4.5 12.5C4.5 15.5 6 16.5 8.5 16.5H15.5C18 16.5 19.5 15.5 19.5 12.5"),
        mark(rect(10.4, 15, 3.2, 4.6, L(S, 0.4, 1))),
        line(handle),
    ]


def _jug_parts(S, x0, y0, deg=0.0, mirror=False, piv=None):
    body = [(0, 0), (5, 0), (5.8, 7.5), (-0.8, 7.5)]
    spout = [(4.2, 0), (7, -1.4), (5.3, 2.6)]
    handle = [(0.1, 1.2), (-2.4, 1.6), (-2.4, 5.2), (-0.3, 5.6)]

    def tf(pts):
        out = []
        for x, y in pts:
            if mirror:
                x = 5 - x
            out.append((x + x0, y + y0))
        if deg:
            out = rot_pts(out, deg, *piv)
        return out
    return (union(poly(tf(body), closed=True, r=S.r * 0.5), poly(tf(spout), closed=True)),
            poly(tf(handle), r=S.r * 0.6))


@icon("pouring-practice", CAT, "Tray with two small jugs, one tilted and pouring beads into the other",
      tags=["pouring practice", "montessori", "practical life", "fine motor", "jugs", "pouring"])
def _(S):
    rb, rh = _jug_parts(S, 14, 11.5, mirror=True)
    lb, lh = _jug_parts(S, 4.2, 3, 42, piv=(6.7, 6.8))
    return [
        shell(rb), line(rh), shell(lb), line(lh),
        dot(15.8, 7.4, 1.05), dot(16.2, 10.2, 1.05),
        line(poly([(2, 19.5), (2.8, 21.5), (21.2, 21.5), (22, 19.5)])),
    ]


# ============================================================================ growing, making and eating

@icon("egg-carton-seedlings", CAT, "Egg carton with a seedling sprouting from each soil filled cup",
      tags=["egg carton seedlings", "seed starting", "sprouts", "planting", "recycling craft", "school garden"])
def _(S):
    cups = [ellipse(x, 15.5, 3.1, 4.5) for x in (5.5, 12, 18.5)]
    carton = minus(union(rect(2, 12.5, 20, 3.5, L(S, 0, 1)), *cups), rect(0, 0, 24, 12.5))
    parts = [shell(carton)]
    for x, top in ((5.5, 7.5), (12, 5.5), (18.5, 7.5)):
        parts.append(line(seg(x, 12.5, x, top + 1.5)))
        parts.append(mark(rot(ellipse(x - 1.7, top, 1.8, 1), -35, x - 1.7, top)))
        parts.append(mark(rot(ellipse(x + 1.7, top, 1.8, 1), 35, x + 1.7, top)))
    return parts


@icon("pinecone-bird-feeder", CAT, "Seed coated pinecone hanging from a string with a small bird perched on it",
      tags=["pinecone bird feeder", "bird feeder", "nature craft", "birds", "winter craft", "seeds"])
def _(S):
    cone = "M9.5 5.5C12.5 5.5 14 8.5 14 12C14 16 12 19 9.5 20.5C7 19 5 16 5 12C5 8.5 6.5 5.5 9.5 5.5Z"
    bird = union(ellipse(16.7, 13.5, 3.2, 2.4), circle(18.5, 10.8, 1.9),
                 poly([(20, 10.2), (21.4, 10.9), (20.1, 11.7)], closed=True),
                 poly([(14, 14.2), (13.1, 17.2), (15.8, 15.6)], closed=True))
    return [
        line(seg(9.5, 1.5, 9.5, 5.5)),
        shell(cone), shell(bird),
        detail("M6.5 10L9.5 12L12.5 10"), detail("M6 14L9.5 16.5L13 14"),
        line(seg(14.2, 18.5, 19.7, 18.5)),
    ]


@icon("lunchbox-note", CAT, "Folded note with a heart doodle tucked beside a sandwich",
      tags=["lunchbox note", "lunch note", "love note", "packed lunch", "sandwich", "note from home"])
def _(S):
    note = poly([(2.5, 3), (10, 3), (13, 6), (13, 13.5), (2.5, 13.5)], closed=True, r=S.r * 0.4)
    top = "M8 18.5V17.5C8 15.8 9.5 15 11.5 15H18.5C20.5 15 22 15.8 22 17.5V18.5Z"
    return [
        shell(note), detail("M10 3V6H13"), detail(heart(7.7, 7.4, 5.4)),
        shell(top), line("M8 20.5Q9.75 19.3 11.5 20.5T15 20.5T18.5 20.5T22 20.5"),
    ]


@icon("finger-counting", CAT, "Hand holding up three fingers beside the number 3",
      tags=["finger counting", "count", "three", "numbers", "early maths", "counting on fingers"])
def _(S):
    fw = 3.3
    regs = [P(rect(2.5, 12, 12.6, 9.5, L(S, 0.5, 2.5)))]
    for x, t in ((4.3, 6.2), (7.6, 4.5), (10.9, 5.5)):
        regs.append(ST(seg(x, 13, x, t), fw, "round", "round"))
    regs.append(ST(seg(13.3, 12.8, 13.3, 12.8), fw, "round", "round"))
    regs.append(ST(seg(4, 17.6, 10.8, 16.2), fw, "round", "round"))
    hand = path_to_d(U(*regs))
    return [
        shell(hand),
        detail(seg(5.95, 8, 5.95, 12.5)), detail(seg(9.25, 8, 9.25, 12.5)),
        line("M16.8 3.4C17.3 2.6 18.1 2.2 19 2.2C20.3 2.2 21.2 3 21.2 4.2C21.2 5.4 20.3 6.2 19 6.2"
             "C20.4 6.2 21.4 7 21.4 8.3C21.4 9.6 20.4 10.5 19 10.5C18 10.5 17.2 10 16.7 9.2"),
    ]


# ============================================================================ reading and learning aids

@icon("whisper-phone", CAT, "Child's head in profile with a curved tube running from the ear to the mouth",
      tags=["whisper phone", "phonics phone", "reading phone", "reading aloud", "phonics", "fluency"])
def _(S):
    head = ("M8.5 4C12.4 4 15 6.8 15 10.3L16.8 13.3L15 13.8V15.6C15 17 14 17.8 12.6 17.8H11.5V21H4.5V17.3"
            "C3 16 2 13.8 2 11C2 7 4.8 4 8.5 4Z")
    return [
        shell(head),
        dot(8, 11.3, 1.9),
        line("M9.5 9.5C10 4.5 20.5 3 21.2 11.5C21.8 17.5 18.5 19.5 15.8 17.8"),
    ]


@icon("reading-finger-pointer", CAT, "Wand with a small pointing hand at its tip resting on a line of text",
      tags=["reading pointer", "finger pointer", "guided reading", "tracking text", "pointer", "literacy"])
def _(S):
    fist = union(rect(-3.2, -2.6, 6, 6.2, L(S, 0.8, 2.2)), capsule(2, -1.2, 7.6, -1.2, 2.6),
                 capsule(-0.8, -2.4, 1.6, -3.4, 2.2))
    m = rotation(130, 0, 0)
    tx, ty = 13.2, 8.2
    hand = path_to_d(transform_path(P(fist), (m[0], m[1], m[2], m[3], tx, ty)))
    s0 = pt_on(tx, ty, 3.9, -50)
    s1 = pt_on(tx, ty, 8.6, -50)
    return [
        shell(hand),
        line(seg(s0[0], s0[1], s1[0], s1[1])),
        line(seg(2, 18.5, 22, 18.5)), line(seg(2, 21.5, 14, 21.5)),
    ]


@icon("leveled-reader", CAT, "Thin picture book with a circled letter level badge on the cover corner",
      tags=["leveled reader", "levelled reader", "guided reading", "reading level", "early reader", "picture book"])
def _(S):
    book = rect(3.5, 3, 14, 18.5, rr(S, 3))
    badge = circle(17.5, 7, 4.2)
    letter = "M15.7 10.2L17.5 4.6L19.3 10.2M16.3 8.3H18.7"
    disc = path_to_d(D(P(badge), ST(letter, 1.5, "butt" if S.name == "line" else "round", "miter" if S.name == "line" else "round")))
    return [
        shell(behind(book, [badge], 1.2)),
        detail(seg(6.5, 3, 6.5, 21.5)),
        detail("M9 18L11.5 15L13.5 17L15 15.5"),
        mark(disc),
    ]


@icon("question-parking-lot", CAT, "Board with parking bays holding sticky notes and a question mark",
      tags=["parking lot", "question board", "sticky notes", "questions", "classroom board", "wonder wall"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, rr(S, 3))),
        detail(seg(8.7, 21, 8.7, 13.5)),
        detail(seg(15.3, 21, 15.3, 13.5)),
        detail("M9.8 7.2C9.8 5.8 10.8 5 12 5C13.2 5 14.2 5.8 14.2 7C14.2 8.4 12.2 8.6 12.2 10"),
        mark(rect(3.9, 15.2, 3, 3, 0.4)), mark(rect(17.1, 15.2, 3, 3, 0.4)),
    ]


@icon("brain-break", CAT, "Brain with small running legs for a quick movement break",
      tags=["brain break", "movement break", "energizer", "active break", "classroom routine", "exercise"])
def _(S):
    brain = ("M7.5 13.5C5.6 13.5 4.5 12 4.5 10.3C4.5 9 5.2 8 6.2 7.5C6.2 5 8 3.3 10.4 3.4C11.3 2.6 12.5 2.2 13.8 2.3"
             "C16 2.5 17.6 3.8 18.1 5.6C19.6 6.2 20.5 7.6 20.5 9.3C20.5 11.7 18.8 13.5 16.5 13.5Z")
    return [
        shell(brain),
        detail("M12.5 2.8C11.8 4.5 12.6 6 13.8 6.6"), detail("M8.2 8.4C9.4 7.6 11 7.9 11.8 9"),
        detail("M13.6 10.6C14.6 9.4 16.4 9.2 17.6 10"),
        line(poly([(10, 13.5), (8.4, 17.3), (5.2, 18)], r=S.r)),
        line(poly([(15, 13.5), (15.6, 17.4), (18.6, 20.2)], r=S.r)),
    ]


@icon("wobble-stool", CAT, "Round seat stool on a single post with a rocking base and tilt arcs",
      tags=["wobble stool", "active seating", "flexible seating", "rocking stool", "fidget", "wiggle seat"])
def _(S):
    seat = rect(6.5, 3.5, 11, 3.2, L(S, 0.8, 1.6))
    base = "M7.5 15.5H16.5A4.5 5 0 0 1 7.5 15.5Z"
    post = rect(10.9, 6.7, 2.2, 8.8)
    stool = rot(union(seat, base, post), 10, 12, 20)
    return [
        shell(stool),
        line(arc(12, 14, 9.5, 150, 185)), line(arc(12, 14, 9.5, -5, 30)),
    ]
