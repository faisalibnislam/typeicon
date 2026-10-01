"""TypeIcon Core: business (batch 002).

Business frameworks, workplace life, marketing and retail. People follow `sets/people.py`: a round head over
open shoulders, or a stick figure with a dot head. Overlapping objects are drawn in layers (front first):
back layers are cut away around the front silhouette with a gap, so they stay readable at 16 px.
"""
import math

from dsl import LINE, Part, arc, circle, detail, dot, ellipse, filled_region, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "business"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def block(x, y, w, h, rx=0.0):
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def zig(x_from, x_to, y_hi, y_lo, n):
    """Zigzag points from x_from to x_to: n teeth, starting and ending on y_hi."""
    pts = []
    for i in range(2 * n + 1):
        x = x_from + (x_to - x_from) * i / (2 * n)
        pts.append((x, y_hi if i % 2 == 0 else y_lo))
    return pts


def head_arrow(tip, deg, size=2.5, spread=45):
    """Open arrowhead (two strokes meeting at tip) pointing in direction deg (0 = right, 90 = down)."""
    a = polar(tip[0], tip[1], size, deg + 180 - spread)
    b = polar(tip[0], tip[1], size, deg + 180 + spread)
    return [a, tip, b]


def bust(S, cx, top, hw, bottom):
    """Open-bottom shoulders (people.py proportions). Line has squarer shoulders than Rounded."""
    r = hw - (1.0 if S.name != "line" else 2.0)
    r = max(0.5, min(r, bottom - top))
    x0, x1 = cx - hw, cx + hw
    return (f"M{fmt(x0)} {fmt(bottom)}V{fmt(top + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x0 + r)} {fmt(top)}"
            f"H{fmt(x1 - r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(top + r)}V{fmt(bottom)}")


# --------------------------------------------------------------------------- layering (as in people.py)

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


# ============================================================================ accounting and frameworks

@icon("t-account", CAT, "T-account ledger: a heading bar over a centre line with entries on each side",
      tags=["t account", "ledger", "debit", "credit", "bookkeeping", "accounting"])
def _(S):
    return [shell(rect(3, 3, 18, 4.5, L(S, 0.5, 2.25))),
            line(seg(12, 7.5, 12, 21)),
            line(seg(4, 12, 9, 12)), line(seg(4, 16, 8, 16)),
            line(seg(15, 12, 20, 12)), line(seg(15, 16, 20, 16)), line(seg(15, 20, 18, 20))]


@layered("expense-report", "Clipboard form with a receipt clipped over its corner",
         tags=["expenses", "expense claim", "reimbursement", "receipt", "report", "spending"])
def _(S):
    teeth = zig(21, 11.5, 18.5, 16.75, 3)
    receipt = [shell(poly([(11.5, 7), (21, 7), *teeth], closed=True, r=S.r * 0.4)),
               detail(seg(14.25, 10.5, 18.25, 10.5)), detail(seg(14.25, 13.75, 18.25, 13.75))]
    board = [shell(rect(3, 4, 12, 17, L(S, 1.5, 3))), shell(rect(6, 2.5, 6, 3, L(S, 0.5, 1))),
             detail(seg(6, 10, 8.5, 10)), detail(seg(6, 14, 8.5, 14)), detail(seg(6, 18, 8.5, 18))]
    return [receipt, board]


@icon("scan-receipt", CAT, "Receipt framed by four scanning corner brackets",
      tags=["scan receipt", "receipt scanner", "capture", "expense", "ocr", "camera"])
def _(S):
    teeth = zig(16, 8, 17.5, 16, 3)
    return [line(poly([(3, 8), (3, 3), (8, 3)], r=S.r)), line(poly([(16, 3), (21, 3), (21, 8)], r=S.r)),
            line(poly([(21, 16), (21, 21), (16, 21)], r=S.r)), line(poly([(8, 21), (3, 21), (3, 16)], r=S.r)),
            shell(poly([(8, 6.5), (16, 6.5), *teeth], closed=True, r=S.r * 0.4)),
            detail(seg(10.5, 10, 13.5, 10)), detail(seg(10.5, 13, 13.5, 13))]


@icon("e-receipt", CAT, "Smartphone showing a receipt with a zigzag bottom edge",
      tags=["digital receipt", "electronic receipt", "mobile receipt", "purchase", "proof of payment", "phone"])
def _(S):
    teeth = zig(15.5, 8.5, 16, 14.5, 3)
    return [shell(rect(5, 2, 14, 20, L(S, 2, 3.5))),
            detail(poly([(8.5, 5.5), (15.5, 5.5), *teeth], closed=True, r=S.r * 0.4)),
            detail(seg(L(S, 10.5, 11), 19, L(S, 13.5, 13), 19))]


@icon("five-forces-diagram", CAT, "Central box with four arrow blocks pointing in from every side",
      tags=["five forces", "porter", "competition", "strategy", "industry analysis", "framework"])
def _(S):
    k = L(S, 0, 0.6)
    top = [(9.5, 2.5), (14.5, 2.5), (14.5, 4.5), (12, 6.75), (9.5, 4.5)]
    parts = [shell(rect(9, 9, 6, 6, L(S, 0.5, 2)))]
    for deg in (0, 90, 180, 270):
        m = rotation(deg, 12, 12)
        pts = [(m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5]) for x, y in top]
        parts.append(mark(poly(pts, closed=True, r=k)))
    return parts


@icon("value-proposition-canvas", CAT, "Square and circle side by side, each split into three sections",
      tags=["value proposition", "canvas", "customer profile", "value map", "product fit", "strategy"])
def _(S):
    cx, cy, r = 17.5, 12, 4
    spokes = [detail(seg(cx, cy, *polar(cx, cy, r, a))) for a in (-90, 30, 150)]
    return [shell(rect(2, 8, 8, 8, L(S, 0.5, 2.5))), detail(seg(6, 8, 6, 16)), detail(seg(6, 12, 10, 12)),
            shell(circle(cx, cy, r)), *spokes]


@icon("nine-box-grid", CAT, "Three by three grid with one marked cell in the top right corner",
      tags=["9 box", "talent grid", "performance", "potential", "succession", "hr"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)),
            detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)),
            detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15)),
            dot(18, 6, 1.25)]


@icon("value-chain", CAT, "Arrow-shaped band divided into three chevron segments",
      tags=["value chain", "process", "activities", "stages", "supply chain", "strategy"])
def _(S):
    return [shell(poly([(2, 6), (17, 6), (21.5, 12), (17, 18), (2, 18), (4.5, 12)], closed=True, r=S.r * 0.5)),
            detail(poly([(7, 6), (9.5, 12), (7, 18)], r=S.r * 0.5)),
            detail(poly([(12, 6), (14.5, 12), (12, 18)], r=S.r * 0.5))]


@icon("business-model-canvas", CAT, "Wide board divided into five tall blocks above two wide ones",
      tags=["business model", "canvas", "lean canvas", "strategy", "startup", "planning"])
def _(S):
    return [shell(rect(2, 4, 20, 16, L(S, 1, 3))),
            detail(seg(2, 15, 22, 15)), detail(seg(12, 15, 12, 20)),
            detail(seg(6, 4, 6, 15)), detail(seg(10, 4, 10, 15)), detail(seg(14, 4, 14, 15)), detail(seg(18, 4, 18, 15)),
            detail(seg(6, 9.5, 10, 9.5)), detail(seg(14, 9.5, 18, 9.5))]


@icon("stakeholder-map", CAT, "Central circle linked by spokes to six people around it",
      tags=["stakeholders", "stakeholder analysis", "network", "relationships", "influence", "people"])
def _(S):
    parts = [shell(circle(12, 12, 3))]
    for a in range(-90, 270, 60):
        x, y = polar(12, 12, 8.75, a)
        parts.append(dot(x, y, 2))
        parts.append(line(seg(*polar(12, 12, 5, a), *polar(12, 12, 6.25, a))))
    return parts


@icon("game-plan", CAT, "Play board with an X, an O and a curved arrow for the planned move",
      tags=["game plan", "strategy", "playbook", "tactics", "plan", "coach"])
def _(S):
    tip = (13, 7.5)
    return [shell(rect(3, 3, 18, 18, S.R)),
            detail(seg(6, 15, 9, 18)), detail(seg(9, 15, 6, 18)),
            detail(circle(16.75, 16.5, 1.75)),
            detail("M7.5 12C7.5 9 9.5 7.5 13 7.5"),
            detail(poly(head_arrow(tip, 0, 2.25), r=S.r * 0.3))]


@icon("bottleneck", CAT, "Bottle on its side with three items queued inside and one leaving through the neck",
      tags=["bottleneck", "constraint", "congestion", "throughput", "flow", "slowdown"])
def _(S):
    body = [(2, 6), (10, 6), (14, 10), (17, 10), (17, 14), (14, 14), (10, 18), (2, 18)]
    return [shell(poly(body, closed=True, r=S.r * 0.6)),
            dot(5.5, 9.5, 1.25), dot(5.5, 14.5, 1.25), dot(9.5, 12, 1.25),
            dot(20.5, 12, 1.5)]


@icon("360-degree-feedback", CAT, "Person inside a circular arrow that goes all the way round",
      tags=["360 feedback", "performance review", "peer review", "appraisal", "evaluation", "hr"])
def _(S):
    cx, cy, r = 12, 12, 9
    end = polar(cx, cy, r, 235)
    ang = 235 + 90
    return [line(arc(cx, cy, r, -55, 235)),
            line(poly(head_arrow(end, ang, 3), r=S.r * 0.3)),
            dot(12, 8.75, 2.25),
            line(bust(S, 12, 13.25, 4.25, 17))]


# ============================================================================ corporate structure

def star_pts(cx, cy, ro, ri, n=5, start=-90.0):
    pts = []
    for i in range(2 * n):
        pts.append(polar(cx, cy, ro if i % 2 == 0 else ri, start + i * 180 / n))
    return pts


_MG = (9.75, 14.25, 4.25)  # circle centres x and radius


def _merger_arrows(S):
    return [line(poly(head_arrow((2.75, 12), 0, 2.25), r=S.r * 0.3)),
            line(poly(head_arrow((21.25, 12), 180, 2.25), r=S.r * 0.3))]


def _merger_filled():
    xa, xb, r = _MG
    body = U(P(circle(xa, 12, r)), P(circle(xb, 12, r)), ST(circle(xa, 12, r), 2.0), ST(circle(xb, 12, r), 2.0))
    h = math.degrees(math.acos((xb - xa) / 2 / r))
    body = D(body, ST(arc(xb, 12, r, 180 - h, 180 + h), 1.75, "round", "round"))
    arrows = [ST(poly(head_arrow((2.75, 12), 0, 2.25)), 2.5), ST(poly(head_arrow((21.25, 12), 180, 2.25)), 2.5)]
    return U(body, *arrows)


@icon("business-merger", CAT, "Two overlapping circles pushed together by arrows from each side",
      tags=["merger", "merge", "consolidation", "combine", "join", "m&a"], filled=_merger_filled)
def _(S):
    xa, xb, r = _MG
    return [line(circle(xa, 12, r)), line(circle(xb, 12, r)), *_merger_arrows(S)]


@icon("acquisition", CAT, "Big fish with its mouth open about to swallow a small fish",
      tags=["takeover", "acquire", "buyout", "big fish", "m&a", "purchase"])
def _(S):
    if S.name == "line":
        tail = "L22 6.5V17.5L18.5 14"
    else:
        tail = "L20.6 7.9Q22 7 22 8.6V15.4Q22 17 20.6 16.1L18.5 14"
    big = ("M9 8.5C11.5 5 16.5 5 18.5 10" + tail +
           "C16.5 19 11.5 19 9 15.5L12.5 12Z")
    small = ("M1.5 12C2.2 9.8 5 9.5 6.4 11L8.5 9.3V14.7L6.4 13C5 14.5 2.2 14.2 1.5 12Z")
    return [shell(big, stroke_miterlimit="2"), dot(14.25, 9.75, 1.1), solid(small)]


@icon("franchise", CAT, "Three identical small shop fronts with awnings in a row",
      tags=["franchise", "chain store", "branches", "retail chain", "outlets", "licensing"])
def _(S):
    k = L(S, 0, 0.6)
    parts = []
    for x in (4.5, 12, 19.5):
        parts.append(mark(poly([(x - 2.5, 5), (x + 2.5, 5), (x + 3.25, 9.5), (x - 3.25, 9.5)], closed=True, r=k)))
        parts.append(line(poly([(x - 2.25, 11.5), (x - 2.25, 20), (x + 2.25, 20), (x + 2.25, 11.5)], r=S.r)))
    return parts


@icon("branch-offices", CAT, "Tall head office linked by lines to a small branch building on each side",
      tags=["branches", "branch office", "headquarters", "subsidiary", "offices", "locations"])
def _(S):
    return [shell(rect(9.5, 2.5, 5, 18.5, L(S, 0.5, 1.5))),
            dot(12, 6.5, 1), dot(12, 10.5, 1), dot(12, 14.5, 1),
            shell(rect(2, 14, 4, 7, L(S, 0.5, 1.5))), shell(rect(18, 14, 4, 7, L(S, 0.5, 1.5))),
            line(poly([(4, 13), (4, 9), (8.5, 9)], r=S.r)), line(poly([(20, 13), (20, 9), (15.5, 9)], r=S.r))]


@layered("global-business", "Globe with a briefcase in front of its lower right side",
         tags=["international business", "global", "worldwide", "export", "multinational", "trade"])
def _(S):
    case = [line(poly([(15.25, 14), (15.25, 12), (19.25, 12), (19.25, 14)], r=S.r * 0.5)),
            shell(rect(12.5, 14, 9.5, 7, L(S, 1, 2))), detail(seg(12.5, 17, 22, 17))]
    globe = [shell(circle(10, 10, 8)), detail(ellipse(10, 10, 3.5, 8)), detail(seg(2, 10, 18, 10))]
    return [case, globe]


@layered("leadership", "Person in front with a small flag above, two smaller people behind",
         tags=["leader", "lead", "team leader", "manager", "guide", "vision"])
def _(S):
    front = [shell(circle(12, 11, 2.75)), shell(bust(S, 12, 16.5, 5.5, 21)),
             line(seg(12, 2.5, 12, 6.5)), solid(poly([(12, 2), (16, 3.5), (12, 5.25)], closed=True))]
    back = [shell(circle(5.5, 10, 2)), shell(bust(S, 5.5, 14.5, 3.5, 21)),
            shell(circle(18.5, 10, 2)), shell(bust(S, 18.5, 14.5, 3.5, 21))]
    return [front, back]


@icon("glass-ceiling", CAT, "Person reaching up to a horizontal pane that is cracked above their hands",
      tags=["glass ceiling", "barrier", "equality", "promotion", "breakthrough", "women in business"])
def _(S):
    k = S.r * 0.4
    left = [(2, 2.5), (10.5, 2.5), (12, 4.5), (10.5, 6.5), (2, 6.5)]
    right = [(13.5, 2.5), (22, 2.5), (22, 6.5), (13.5, 6.5), (15, 4.5)]
    return [shell(poly(left, closed=True, r=k)), shell(poly(right, closed=True, r=k)),
            dot(12, 11.5, 2),
            line(poly([(8, 9.5), (9.5, 15.5), (14.5, 15.5), (16, 9.5)], r=S.r)),
            line(seg(12, 15.5, 12, 18)),
            line(poly([(9.5, 22), (12, 18), (14.5, 22)], r=S.r))]


@layered("elevator-pitch", "Elevator doors with a speech bubble between them",
         tags=["elevator pitch", "pitch", "sales pitch", "short speech", "startup", "introduction"])
def _(S):
    bubble = [shell(poly([(8, 10), (16, 10), (16, 14.5), (13.5, 14.5), (12, 16.5), (10.5, 14.5), (8, 14.5)],
                         closed=True, r=S.r * 0.6))]
    doors = [shell(rect(3.5, 7, 7.5, 14, L(S, 0.5, 1.5))), shell(rect(13, 7, 7.5, 14, L(S, 0.5, 1.5))),
             mark(poly([(8, 4.5), (9.75, 2), (11.5, 4.5)], closed=True, r=L(S, 0, 0.4))),
             mark(poly([(12.5, 2), (16, 2), (14.25, 4.5)], closed=True, r=L(S, 0, 0.4)))]
    return [bubble, doors]


def mini_person(S, cx, cy):
    """Tiny person: a round head over solid shoulders (squarer in Line)."""
    if S.name == "line":
        body = poly([(cx - 3.5, cy + 7), (cx - 3.5, cy + 4.5), (cx - 2, cy + 3), (cx + 2, cy + 3), (cx + 3.5, cy + 4.5),
                     (cx + 3.5, cy + 7)], closed=True)
    else:
        body = f"M{fmt(cx - 3.5)} {fmt(cy + 7)}V{fmt(cy + 6.5)}A3.5 3.5 0 0 1 {fmt(cx + 3.5)} {fmt(cy + 6.5)}V{fmt(cy + 7)}Z"
    return [dot(cx, cy, 2), solid(body)]


@icon("business-networking", CAT, "Three small people at the corners of a triangle joined by lines",
      tags=["networking", "connections", "contacts", "business contacts", "relationships", "community"])
def _(S):
    return [*mini_person(S, 12, 3.5), *mini_person(S, 5.5, 13.5), *mini_person(S, 18.5, 13.5),
            line(seg(11, 19, 13, 19)), line(seg(8, 10, 9.5, 8)), line(seg(16, 10, 14.5, 8))]


@icon("hybrid-work", CAT, "House and office building with two arrows cycling between them",
      tags=["hybrid work", "remote work", "work from home", "office", "commute", "flexible working"])
def _(S):
    tip1, tip2 = (12, 4.5), (12, 19.5)
    return [shell(poly([(2.5, 16.5), (6.5, 13), (10.5, 16.5), (10.5, 21), (2.5, 21)], closed=True, r=S.r * 0.6)),
            shell(rect(14.5, 3, 7, 8.5, L(S, 0.5, 1.5))), dot(18, 7.25, 1),
            line("M6 10V7.5A3 3 0 0 1 9 4.5H12"), line(poly(head_arrow(tip1, 0, 2.25), r=S.r * 0.3)),
            line("M18 14V16.5A3 3 0 0 1 15 19.5H12"), line(poly(head_arrow(tip2, 180, 2.25), r=S.r * 0.3))]


@icon("digital-nomad", CAT, "Open laptop on a small table under a leaning palm tree",
      tags=["digital nomad", "remote work", "work from anywhere", "travel", "freelancer", "laptop"])
def _(S):
    return [line("M4 21.5Q4.5 12.5 8.5 6.5"),
            line("M8.5 6.5Q5 3.5 2 6.5"), line("M8.5 6.5Q12.5 3.5 15.5 6.5"), line("M8.5 6.5Q8 3 10.5 2"),
            line("M8.5 6.5Q4 7 3 11"), line("M8.5 6.5Q13 7 14 11"),
            shell(rect(13, 12, 7.5, 5.5, L(S, 0.5, 1.5))),
            line(seg(10.5, 20, 22.5, 20))]


@layered("employee-of-the-month", "Framed portrait of a person with a star rosette on the frame corner",
         tags=["employee of the month", "award", "recognition", "top performer", "staff award", "achievement"])
def _(S):
    star = [shell(poly(star_pts(17.5, 7, 4.5, 2.1), closed=True, r=S.r * 0.3), stroke_miterlimit="2")]
    frame = [shell(rect(2.5, 4, 14, 17, L(S, 1, 2.5))), detail(circle(9.5, 10.5, 2.25)),
             detail(bust(S, 9.5, 15, 4, 21))]
    return [star, frame]


@icon("career-ladder", CAT, "Ladder rising towards a briefcase at the top right",
      tags=["career ladder", "promotion", "career growth", "advancement", "climb", "job"])
def _(S):
    return [line(seg(3.5, 22, 3.5, 5)), line(seg(10.5, 22, 10.5, 5)),
            line(seg(3.5, 9, 10.5, 9)), line(seg(3.5, 13.5, 10.5, 13.5)), line(seg(3.5, 18, 10.5, 18)),
            line(poly([(16, 5), (16, 3), (19, 3), (19, 5)], r=S.r * 0.5)),
            shell(rect(13.5, 5, 8, 6, L(S, 0.5, 1.5)))]


@icon("mentorship", CAT, "Tall person with a hand resting on the shoulder of a smaller person",
      tags=["mentor", "mentoring", "coaching", "guidance", "support", "apprentice"])
def _(S):
    return [dot(7, 4.5, 2.25),
            line(poly([(3, 14.5), (4.5, 9.5), (10, 9.5), (14, 13)], r=S.r)),
            line(seg(7, 9.5, 7, 15)), line(poly([(4.5, 21.5), (7, 15), (9.5, 21.5)], r=S.r)),
            dot(17.5, 9.5, 1.75),
            line(poly([(14, 13), (21, 13), (21.5, 16.5)], r=S.r)),
            line(seg(17.5, 13, 17.5, 17)), line(poly([(15.5, 21.5), (17.5, 17), (19.5, 21.5)], r=S.r))]


@layered("leaving-job-box", "Cardboard box with a small plant and a picture frame sticking out of the top",
         tags=["leaving job", "resignation", "fired", "last day", "quit", "moving desk"])
def _(S):
    box = [shell(poly([(3, 12), (21, 12), (19.5, 21), (4.5, 21)], closed=True, r=S.r * 0.5)),
           detail(seg(L(S, 10, 10.5), 15.5, L(S, 14, 13.5), 15.5))]
    plant = [line(seg(8, 13, 8, 7)),
             shell("M8 8C7.5 5 5.5 4 3 4C3 6.5 5 8.5 8 8Z"), shell("M8 7C8.5 4.5 10 3 12.5 3C12.5 5.5 11 7 8 7Z")]
    frame_pts = [(13.5, 5.5), (19.5, 4.5), (20.5, 12.5), (14.5, 13.5)]
    frame = [shell(poly(frame_pts, closed=True, r=S.r * 0.5))]
    return [box, plant + frame]


# ============================================================================ workplace

@icon("coworking-table", CAT, "Long shared table with three open laptops along it",
      tags=["coworking", "shared desk", "hot desk", "open office", "workspace", "team table"])
def _(S):
    parts = [line(seg(2, 15.5, 22, 15.5)), line(seg(4.5, 15.5, 4.5, 21.5)), line(seg(19.5, 15.5, 19.5, 21.5))]
    for x in (3, 9.75, 16.5):
        parts.append(shell(rect(x, 8, 4.5, 5, L(S, 0.5, 1.25))))
    return parts


@layered("welcome-kit", "Open box holding a mug, a notebook and a pen for a new starter",
         tags=["welcome kit", "onboarding", "new hire", "welcome pack", "swag", "starter kit"])
def _(S):
    box = [shell(rect(3, 13, 18, 8.5, L(S, 1, 2))),
           line(seg(3, 13, 1.5, 10)), line(seg(21, 13, 22.5, 10))]
    mug = [shell(rect(5, 7.5, 4.5, 5.5, L(S, 0.5, 1.5))), line("M9.5 9H9.75A1.5 1.5 0 0 1 9.75 12H9.5")]
    book = [shell(rect(14, 3.5, 5, 9.5, L(S, 0.5, 1.25))), detail(seg(16.5, 3.5, 16.5, 13))]
    return [box, mug + book]


@icon("workload", CAT, "Person holding a tall, teetering stack of files above their head",
      tags=["workload", "overworked", "busy", "too much work", "burnout", "paperwork"])
def _(S):
    rx = L(S, 0, 0.75)
    return [block(2.5, 2, 8, 3, rx), block(3.5, 7, 8, 3, rx), block(2, 12, 8.5, 3, rx), block(3, 17, 8.5, 3.5, rx),
            shell(circle(17.5, 10, 2.75)), shell(bust(S, 17.5, 15.5, 4, 21))]


@icon("award-plaque", CAT, "Shield-shaped plaque with a small engraved plate in the centre",
      tags=["plaque", "award", "trophy plaque", "honour", "recognition", "commemorative"])
def _(S):
    body = "M4 3H20V11C20 16 16.5 19.5 12 21.5C7.5 19.5 4 16 4 11Z"
    if S.name == "rounded":
        body = "M6.5 3H17.5A2.5 2.5 0 0 1 20 5.5V11C20 16 16.5 19.5 12 21.5C7.5 19.5 4 16 4 11V5.5A2.5 2.5 0 0 1 6.5 3Z"
    return [shell(body), detail(rect(8, 7.5, 8, 5, L(S, 0, 1))), detail(seg(L(S, 10, 10.5), 16, L(S, 14, 13.5), 16))]


@icon("word-of-mouth", CAT, "One person speaking, with sound waves travelling to a second person",
      tags=["word of mouth", "recommendation", "buzz", "referral", "conversation", "gossip"])
def _(S):
    return [*mini_person(S, 4.5, 10), *mini_person(S, 19.5, 10),
            line(arc(8, 11, 2.5, -45, 45)), line(arc(8, 11, 5.5, -35, 35))]


@icon("referral", CAT, "Two people with a curved arrow passing from one to the other",
      tags=["referral", "refer a friend", "recommend", "invite", "referral program", "introduction"])
def _(S):
    tip = (18.75, 9)
    return [*mini_person(S, 5.5, 13.5), *mini_person(S, 18.5, 13.5),
            line("M5.5 9C7.5 3.5 16 3 18.75 9"), line(poly(head_arrow(tip, 70, 2.5), r=S.r * 0.3))]


@icon("target-audience", CAT, "Target of concentric rings with a small person at the centre",
      tags=["target audience", "target market", "audience", "demographic", "customer", "marketing"])
def _(S):
    body = (f"M8.75 15.25V14.5A3.25 3 0 0 1 15.25 14.5V15.25Z" if S.name != "line" else
            "M8.75 15.25V13.5L10.25 12.25H13.75L15.25 13.5V15.25Z")
    return [shell(circle(12, 12, 9)), detail(circle(12, 12, 5.25)), dot(12, 9.75, 1.5), mark(body)]


@icon("buyer-persona", CAT, "Profile card with an avatar on the left and a bulleted list on the right",
      tags=["buyer persona", "customer profile", "persona", "user profile", "ideal customer", "marketing"])
def _(S):
    parts = [shell(rect(2, 4, 20, 16, L(S, 1.5, 3))), detail(circle(7.5, 9.5, 2.25)), detail(bust(S, 7.5, 14, 3.5, 20))]
    for y in (9, 12.5, 16):
        parts += [dot(13.75, y, 1), detail(seg(L(S, 16, 16.5), y, L(S, 19.5, 19), y))]
    return parts


def _bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def dashed_bez(ctrl, spans, n=6):
    """Short polylines along a cubic between parameter spans [(t0, t1), ...]."""
    out = []
    for t0, t1 in spans:
        out.append(poly([_bez(*ctrl, t0 + (t1 - t0) * i / n) for i in range(n + 1)]))
    return out


@icon("customer-journey", CAT, "Winding dashed path from a person to a shopping bag",
      tags=["customer journey", "user journey", "journey map", "path to purchase", "funnel", "touchpoints"])
def _(S):
    ctrl = [(5, 12.5), (5, 20), (19, 4.5), (18.5, 12)]
    k = L(S, 0, 0.05)
    spans = [(0.02 + k, 0.2 - k), (0.33 + k, 0.53 - k), (0.66 + k, 0.86 - k)]
    return [*mini_person(S, 5, 2.5),
            *[line(d) for d in dashed_bez(ctrl, spans)],
            line("M16.25 15.5V15A2.25 2.25 0 0 1 20.75 15V15.5"),
            shell(rect(14, 15.5, 9, 6.5, L(S, 0.5, 1.5)))]


def _tiny_person(S, cx, cy):
    head = circle(cx, cy - 1.5, 1.25)
    if S.name == "line":
        body = poly([(cx - 2, cy + 2.25), (cx - 2, cy + 1), (cx - 1, cy + 0.25), (cx + 1, cy + 0.25), (cx + 2, cy + 1),
                     (cx + 2, cy + 2.25)], closed=True)
    else:
        body = f"M{fmt(cx - 2)} {fmt(cy + 2.25)}A2 2 0 0 1 {fmt(cx + 2)} {fmt(cy + 2.25)}Z"
    return [mark(head), mark(body)]


@icon("customer-segments", CAT, "Pie chart split into three slices with a small person in each",
      tags=["customer segments", "segmentation", "market segments", "audience groups", "demographics", "cohorts"])
def _(S):
    parts = [shell(circle(12, 12, 9.5))]
    parts += [detail(seg(12, 12, *polar(12, 12, 9.5, a))) for a in (-90, 30, 150)]
    for a in (-30, 90, 210):
        parts += _tiny_person(S, *polar(12, 12, 5.25, a))
    return parts


@icon("ab-test", CAT, "Two panels side by side marked with the letters A and B",
      tags=["a/b test", "split test", "experiment", "variant", "compare", "optimisation"])
def _(S):
    k = S.r * 0.3
    a = poly([(3.75, 16.5), (6.25, 7), (8.75, 16.5)], r=k)
    b = "M15.5 16.5V7H17.5A2.25 2.25 0 0 1 17.5 11.5H15.5M17.5 11.5H18A2.5 2.5 0 0 1 18 16.5H15.5"
    return [shell(rect(1.5, 3, 10, 18, L(S, 1.5, 3))), shell(rect(12.5, 3, 10, 18, L(S, 1.5, 3))),
            detail(a), detail(seg(5, 13.25, 7.5, 13.25)), detail(b)]


_AD_A = poly([(7.25, 15.5), (9.25, 9), (11.25, 15.5)])
_AD_D = "M13.75 15.5V9H15A3.25 3.25 0 0 1 15 15.5Z"


def _ad_letters():
    return U(ST(_AD_A, 2.0, "butt", "miter"), ST(seg(8, 13.5, 10.5, 13.5), 1.75), ST(_AD_D, 2.0, "butt", "miter"))


def _banner_filled():
    win = U(P(rect(2, 3, 20, 18, 2)), ST(rect(2, 3, 20, 18, 2), 2.0))
    win = D(win, ST(seg(2, 6.5, 22, 6.5), 2.0))
    win = D(win, P(rect(4.5, 7.5, 15, 10, 0.5)))
    return U(win, _ad_letters())


@icon("banner-ad", CAT, "Browser window with a wide banner marked AD across the page",
      tags=["banner ad", "display ad", "advert", "advertisement", "web ad", "ad placement"], filled=_banner_filled)
def _(S):
    banner = D(P(rect(5, 8, 14, 9, L(S, 0, 1.5))), _ad_letters())
    return [shell(rect(2, 3, 20, 18, L(S, 2, 3))), detail(seg(2, 6.5, 22, 6.5)), solid(path_to_d(banner))]


@icon("inflatable-tube-man", CAT, "Tall wavy inflatable figure with flailing arms rising from a fan base",
      tags=["tube man", "air dancer", "sky dancer", "inflatable", "car lot", "promotion"])
def _(S):
    spine = "M12 17.5C9.5 14.5 14.5 11 12 5"
    body = path_to_d(ST(spine, 4, "round", "round"))
    return [shell(body),
            line("M10.5 10.5C8 10.5 7 5.5 3.5 4.5"), line("M13.75 9.5C16 9.5 16.5 6.5 20.5 7"),
            shell(rect(7.5, 19.5, 9, 2.5, L(S, 0.25, 1.25)))]


@icon("cardboard-display-stand", CAT, "Stepped display stand with product boxes on three shelves and a header card",
      tags=["display stand", "point of sale", "pos display", "merchandising", "retail display", "shelf"])
def _(S):
    rx = L(S, 0, 0.5)
    parts = [shell(rect(6, 2, 12, 4.5, L(S, 0.5, 1.5))),
             line(seg(4, 11, 20, 11)), line(seg(3, 16, 21, 16)), line(seg(2, 21, 22, 21))]
    for x in (5.5, 9.5, 13.5):
        parts.append(block(x + 0.25, 7.5, 2.5, 2.5, rx))
    for x in (4.5, 8.5, 12.5, 16.5):
        parts.append(block(x + 0.25, 12.5, 2.5, 2.5, rx))
    for x in (3.5, 7.5, 11.5, 15.5, 19.5):
        parts.append(block(x - 0.75, 17.5, 2.5, 2.5, rx))
    parts[-1] = block(18.25, 17.5, 2.5, 2.5, rx)
    return parts


@icon("step-and-repeat-banner", CAT, "Wide backdrop covered in a repeating pattern of small squares, on two feet",
      tags=["step and repeat", "press wall", "media wall", "backdrop", "red carpet", "sponsor wall"])
def _(S):
    rx = L(S, 0, 0.5)
    parts = [shell(rect(2, 2.5, 20, 14.5, L(S, 1, 2.5))),
             line(seg(5, 17, 5, 21.5)), line(seg(19, 17, 19, 21.5)),
             line(seg(2.5, 21.5, 7.5, 21.5)), line(seg(16.5, 21.5, 21.5, 21.5))]
    for row, y in enumerate((5.25, 9.5, 13.75)):
        xs = (6, 12, 18) if row % 2 == 0 else (9, 15)
        parts += [block(x - 1, y - 1, 2, 2, rx) for x in xs]
    return parts


# ============================================================================ selling and shopping online

def pin_d(cx, cy, r, tip_y):
    """Map pin outline: a circle of radius r at (cx, cy) tapering to a point at (cx, tip_y)."""
    d = tip_y - cy
    a = math.degrees(math.acos(r / d))
    p1 = polar(cx, cy, r, 90 + a)
    p2 = polar(cx, cy, r, 90 - a)
    return (f"M{fmt(cx)} {fmt(tip_y)}L{fmt(p1[0])} {fmt(p1[1])}A{fmt(r)} {fmt(r)} 0 1 1 {fmt(p2[0])} {fmt(p2[1])}Z")


def price_tag(S, cx, top, w=6, h=8.5):
    """Hanging price tag: pointed top with a punched hole."""
    x0, x1 = cx - w / 2, cx + w / 2
    pts = [(cx, top), (x1, top + 2.75), (x1, top + h), (x0, top + h), (x0, top + 2.75)]
    return [shell(poly(pts, closed=True, r=S.r * 0.5)), dot(cx, top + 4, 1.1)]


@icon("price-comparison", CAT, "Balance scale with a price tag hanging from each end of the beam",
      tags=["price comparison", "compare prices", "best price", "cost comparison", "shopping", "value"])
def _(S):
    return [line(seg(12, 3.5, 12, 20.5)), line(seg(8, 21, 16, 21)), line(seg(3.5, 5, 20.5, 5)),
            line(seg(5, 5, 5, 8)), line(seg(19, 5, 19, 8)),
            *price_tag(S, 5, 8), *price_tag(S, 19, 8)]


@icon("auction-paddle", CAT, "Round bidding paddle on a short handle with the number 1 on its face",
      tags=["auction", "bid", "bidding paddle", "bidder", "paddle", "sale"])
def _(S):
    hr = L(S, 0.25, 1.25)
    body = path_to_d(U(P(circle(12, 9, 7)), P(rect(10.25, 14, 3.5, 8, hr))))
    return [shell(body), detail(poly([(10.5, 7), (12.5, 5.5), (12.5, 12.5)], r=S.r * 0.3))]


@icon("upsell", CAT, "Small parcel with an arrow leading up to a larger parcel beside it",
      tags=["upsell", "upgrade", "upselling", "bigger plan", "cross sell", "sales"])
def _(S):
    tip = (10, 5)
    return [shell(rect(2, 14, 6.5, 7, L(S, 0.5, 1.5))), detail(seg(5.25, 14, 5.25, 16.5)),
            shell(rect(12.5, 8, 9.5, 13, L(S, 1, 2.5))), detail(seg(17.25, 8, 17.25, 12)),
            line(poly([(5.25, 11.5), (5.25, 5), tip], r=S.r)), line(poly(head_arrow(tip, 0, 2.5), r=S.r * 0.3))]


@icon("sales-territory", CAT, "Map area divided into regions with a pin marking one of them",
      tags=["sales territory", "sales region", "territory", "area", "district", "coverage map"])
def _(S):
    k = S.r * 0.4
    outline = [(2.5, 5), (10, 2.5), (21.5, 4), (20.5, 19.5), (12, 21.5), (3, 18.5)]
    return [shell(poly(outline, closed=True, r=k)),
            detail(poly([(10, 2.5), (10.5, 14.5), (3, 18.5)], r=k)), detail(seg(10.5, 14.5, 20.75, 15.25)),
            mark(pin_d(15.75, 8.25, 2.5, 12.75))]


@icon("online-store", CAT, "Browser window with a shop awning drawn across the page",
      tags=["online store", "online shop", "e-commerce", "web shop", "storefront", "website"])
def _(S):
    n, x0, x1, y0, y1 = 3, 5, 19, 11, 13.5
    w = (x1 - x0) / n
    scallops = "".join(f"A{fmt(w / 2)} {fmt(w / 2 * 0.6)} 0 0 1 {fmt(x1 - w * (i + 1))} {fmt(y1)}" for i in range(n))
    awning = f"M{fmt(x0)} {fmt(y0)}H{fmt(x1)}V{fmt(y1)}{scallops}Z"
    return [shell(rect(2, 3, 20, 18, L(S, 2, 3))), detail(seg(2, 7, 22, 7)), detail(awning),
            detail(seg(6.5, 17.5, 6.5, 21)), detail(seg(17.5, 17.5, 17.5, 21))]


@icon("mobile-shopping", CAT, "Smartphone with a shopping bag on its screen",
      tags=["mobile shopping", "shopping app", "m-commerce", "buy on phone", "online shopping", "app"])
def _(S):
    return [shell(rect(4.5, 2, 15, 20, L(S, 2, 3.5))),
            detail(rect(7.5, 10, 9, 7.5, L(S, 0.5, 1.5))), detail("M10 13V9A2 2 0 0 1 14 9V13")]


@icon("product-card", CAT, "Card with an image area on top, a title, a price and a small button",
      tags=["product card", "product tile", "listing", "catalog item", "shop item", "ui card"])
def _(S):
    return [shell(rect(4, 2, 16, 20, L(S, 1.5, 3))), detail(seg(4, 10, 20, 10)),
            detail(poly([(7.5, 10), (10.5, 6.5), (13, 9)], r=S.r * 0.3)), dot(15.5, 6, 1.25),
            detail(seg(7.5, 13.5, 16.5, 13.5)), detail(seg(7.5, 18, 10, 18)),
            block(12.5, 16.5, 4.5, 3, L(S, 0, 1))]


@layered("curbside-pickup", "Car with a shopping bag being loaded into its boot",
         tags=["curbside pickup", "kerbside collection", "click and collect", "drive up", "pickup", "car boot"])
def _(S):
    wheels = [shell(circle(6.5, 18, 2.25)), shell(circle(17, 18, 2.25))]
    body = [shell(poly([(2, 18), (2, 13.5), (4.5, 12.5), (7.5, 8.5), (13.5, 8.5), (16, 12.5), (22, 13), (22, 18)],
                       closed=True, r=S.r * 0.5))]
    bag = [shell(rect(15.5, 4, 6, 5, L(S, 0.5, 1.25))), line("M17 4V3.25A1.5 1.5 0 0 1 20 3.25V4")]
    return [wheels, bag, body]


@layered("in-store-pickup", "Shop front with an awning and a parcel waiting in front of its door",
         tags=["in-store pickup", "click and collect", "collect in store", "pickup point", "parcel collection", "shop"])
def _(S):
    box = [shell(rect(13, 14, 9, 7.5, L(S, 0.5, 1.5))), detail(seg(17.5, 14, 17.5, 16.5))]
    shop = [shell(poly([(2, 8), (4, 3), (18, 3), (20, 8)], closed=True, r=S.r)),
            line(poly([(4, 8), (4, 21), (18, 21), (18, 8)], r=S.r)),
            line(poly([(7.5, 21), (7.5, 13.5), (11.5, 13.5), (11.5, 21)], r=S.r * 0.5))]
    return [box, shop]


@icon("order-tracking", CAT, "Dashed route from a parcel to a pin just below a house",
      tags=["order tracking", "track order", "parcel tracking", "delivery status", "shipment", "where is my order"])
def _(S):
    return [shell(rect(2, 14.5, 7, 6.5, L(S, 0.5, 1.5))), detail(seg(5.5, 14.5, 5.5, 17)),
            shell(poly([(15, 9), (15, 5.5), (18.5, 2.5), (22, 5.5), (22, 9)], closed=True, r=S.r * 0.5)),
            line(seg(11, 17.75, 13, 17.75)), line(seg(15, 17.75, 16.5, 17.75)),
            mark(pin_d(18.5, 13.25, 2.25, 18.25))]


@icon("missed-delivery-card", CAT, "Front door with a card pushed halfway through its letter slot",
      tags=["missed delivery", "delivery card", "sorry we missed you", "notice", "letterbox", "redelivery"])
def _(S):
    return [shell(rect(5, 2, 14, 20, L(S, 1, 2.5))),
            detail(rect(7.5, 8, 9, 2.5, L(S, 0, 1.25))),
            detail(poly([(9, 10.5), (9, 17), (15, 17), (15, 10.5)], r=S.r * 0.5)),
            detail(seg(11, 13.75, 13, 13.75)),
            dot(16, 19.5, 1)]


@icon("product-exchange", CAT, "Two parcels with curved arrows swapping them",
      tags=["exchange", "swap item", "product exchange", "replacement", "return and replace", "trade"])
def _(S):
    tip1, tip2 = (11.75, 4.5), (12.25, 19.5)
    return [shell(rect(2, 13, 8, 8, L(S, 0.5, 2))), detail(seg(6, 13, 6, 16)),
            shell(rect(14, 3, 8, 8, L(S, 0.5, 2))), detail(seg(18, 3, 18, 6)),
            line("M6 10V7.5A3 3 0 0 1 9 4.5H11.75"), line(poly(head_arrow(tip1, 0, 2.25), r=S.r * 0.3)),
            line("M18 14V16.5A3 3 0 0 1 15 19.5H12.25"), line(poly(head_arrow(tip2, 180, 2.25), r=S.r * 0.3))]


@icon("subscription-box", CAT, "Lidded box with a bow on top and a circular repeat arrow on its front",
      tags=["subscription box", "monthly box", "recurring delivery", "subscription", "gift box", "repeat order"])
def _(S):
    cx, cy, r = 12, 15.75, 2.75
    end = polar(cx, cy, r, 200)
    return [shell(rect(2, 6.5, 20, 4, L(S, 0.5, 1.5))), shell(rect(3.5, 10.5, 17, 10.5, L(S, 1, 2))),
            line("M12 6.5C10.5 3 7 3 7.5 5.5"), line("M12 6.5C13.5 3 17 3 16.5 5.5"),
            detail(arc(cx, cy, r, -70, 200)), detail(poly(head_arrow(end, 290, 2), r=S.r * 0.3))]


@icon("product-bundle", CAT, "Small box stacked on a larger box, tied together with a ribbon and bow",
      tags=["bundle", "product bundle", "package deal", "combo", "multipack", "bundle offer"])
def _(S):
    return [shell(rect(7, 7, 10, 6, L(S, 0.5, 1.5))), shell(rect(3, 13, 18, 8.5, L(S, 1, 2))),
            detail(seg(12, 7, 12, 21.5)),
            line("M12 7C10.5 3 7 3 8 6"), line("M12 7C13.5 3 17 3 16 6")]


# ============================================================================ in the shop

@icon("vip-pass", CAT, "Tall pass card on a lanyard clip with a crown printed on its face",
      tags=["vip", "vip pass", "all access", "backstage", "guest pass", "exclusive"])
def _(S):
    crown = [(8.75, 18.5), (8.75, 13.5), (10.4, 15.5), (12, 13), (13.6, 15.5), (15.25, 13.5), (15.25, 18.5)]
    return [line(seg(10.75, 6, 9, 1.5)), line(seg(13.25, 6, 15, 1.5)),
            shell(rect(10, 6, 4, 2.5, L(S, 0, 1))),
            shell(rect(6, 8.5, 12, 14, L(S, 1.5, 3))),
            detail(poly(crown, closed=True, r=S.r * 0.3))]


@icon("shop-mannequin", CAT, "Display mannequin with a smooth head and arms, standing on a pole and base",
      tags=["mannequin", "shop dummy", "display", "fashion", "clothing store", "window display"])
def _(S):
    torso = [(8.5, 8), (15.5, 8), (14.5, 12), (15.5, 16.5), (8.5, 16.5), (9.5, 12)]
    return [shell(circle(12, 4, 2.25)),
            shell(poly(torso, closed=True, r=S.r * 0.6)),
            line(seg(6.5, 9.5, 5, 15)), line(seg(17.5, 9.5, 19, 15)),
            line(seg(12, 16.5, 12, 21)), line(seg(8, 21.5, 16, 21.5))]


def _shirt(S, cx, top):
    pts = [(cx - 1.25, top), (cx - 3.5, top + 1.25), (cx - 3.5, top + 4), (cx - 2.5, top + 4), (cx - 2.5, top + 9.5),
           (cx + 2.5, top + 9.5), (cx + 2.5, top + 4), (cx + 3.5, top + 4), (cx + 3.5, top + 1.25), (cx + 1.25, top)]
    return mark(poly(pts, closed=True, r=L(S, 0, 0.5)))


@icon("garment-rack", CAT, "Rolling clothes rail with two shirts hanging from it",
      tags=["clothes rail", "garment rack", "clothing rack", "hangers", "wardrobe", "boutique"])
def _(S):
    return [line(poly([(2, 19), (2, 3), (22, 3), (22, 19)], r=S.r)), line(seg(1.5, 19, 22.5, 19)),
            dot(3.5, 21.5, 1.25), dot(20.5, 21.5, 1.25),
            line(seg(8, 3, 8, 5.5)), line(seg(16, 3, 16, 5.5)),
            _shirt(S, 8, 6.5), _shirt(S, 16, 6.5)]


@icon("store-aisle", CAT, "Two rows of shelves receding towards the end of a shop aisle",
      tags=["aisle", "store aisle", "supermarket", "shelves", "grocery store", "shopping"])
def _(S):
    k = S.r * 0.3
    return [shell(poly([(2, 2.5), (8.5, 7.5), (8.5, 16.5), (2, 21.5)], closed=True, r=k)),
            detail(seg(2, 9, 8.5, 10.5)), detail(seg(2, 15, 8.5, 13.5)),
            shell(poly([(22, 2.5), (15.5, 7.5), (15.5, 16.5), (22, 21.5)], closed=True, r=k)),
            detail(seg(22, 9, 15.5, 10.5)), detail(seg(22, 15, 15.5, 13.5))]


@icon("self-checkout", CAT, "Self-service checkout kiosk with a screen, a scanning counter and a bagging stand",
      tags=["self checkout", "self service", "self scan", "kiosk", "supermarket", "till"])
def _(S):
    return [shell(rect(3, 2.5, 9, 6, L(S, 0.5, 1.5))), line(seg(7.5, 8.5, 7.5, 11)),
            shell(rect(2, 11, 13, 3.5, L(S, 0.5, 1.25))),
            line(poly([(3.5, 14.5), (3.5, 21.5), (13.5, 21.5), (13.5, 14.5)], r=S.r)),
            shell(rect(17, 10, 5, 5.5, L(S, 0.5, 1.25))), line("M18.25 10V9A1.25 1.25 0 0 1 20.75 9V10"),
            line(seg(19.5, 15.5, 19.5, 21.5))]


@icon("checkout-conveyor", CAT, "Checkout conveyor belt carrying two items with a divider bar between them",
      tags=["conveyor belt", "checkout belt", "checkout", "till", "supermarket", "groceries"])
def _(S):
    return [shell(rect(2, 13, 20, 4.5, 2.25 if S.name != "line" else 0.5)),
            dot(6, 15.25, 1), dot(18, 15.25, 1),
            line(seg(5, 17.5, 5, 21.5)), line(seg(19, 17.5, 19, 21.5)),
            shell(rect(3, 4.5, 5, 6.5, L(S, 0.5, 1.25))),
            mark(poly([(10.5, 11), (12.25, 8), (14, 11)], closed=True, r=L(S, 0, 0.4))),
            shell(rect(16.5, 6.5, 4.5, 4.5, L(S, 0.5, 2.25)))]


@icon("anti-theft-tag", CAT, "Round plastic security tag with a pin standing up through its centre",
      tags=["security tag", "anti theft", "clothing tag", "shoplifting", "eas tag", "alarm tag"])
def _(S):
    cap = rect(9, 3, 6, 2.5, 0) if S.name == "line" else ellipse(12, 4.25, 3, 1.5)
    return [shell(ellipse(12, 15.5, 9.5, 5)), dot(12, 15.5, 1.5),
            line(seg(12, 5.5, 12, 12.5)), mark(cap)]


@icon("empty-shelf", CAT, "Two-tier shop shelf that is empty apart from one box at the end",
      tags=["empty shelf", "out of stock", "sold out", "stockout", "shortage", "supply"])
def _(S):
    return [line(poly([(3, 21.5), (3, 3), (21, 3), (21, 21.5)], r=S.r)),
            line(seg(3, 11.5, 21, 11.5)), line(seg(3, 19.5, 21, 19.5)),
            block(15.5, 13.5, 4, 5.5, L(S, 0, 1))]


@icon("barcode-scanner", CAT, "Handheld barcode scanner gun with a trigger and a beam fanning out",
      tags=["barcode scanner", "scanner gun", "scan", "checkout", "inventory", "point of sale"])
def _(S):
    body = [(8, 4.5), (20.5, 4.5), (21.5, 6), (21.5, 9.5), (17.5, 10.5), (19, 20.5), (14.5, 21), (12.5, 10.5), (8, 10.5)]
    return [shell(poly(body, closed=True, r=S.r * 0.5)),
            line(seg(5.5, 6.5, 2, 4.5)), line(seg(5.5, 8.5, 2, 10.5)),
            line(poly([(11.5, 12.5), (11, 15), (13, 15.5)], r=S.r * 0.4))]


def nine(x):
    """Digit 9, 3.5 wide, between y 10.5 and 15.5, left edge at x."""
    return (f"M{fmt(x)} 15.5H{fmt(x + 1.75)}A1.75 1.75 0 0 0 {fmt(x + 3.5)} 13.75V12.25"
            f"A1.75 1.75 0 1 0 {fmt(x + 1.75)} 14H{fmt(x + 3.5)}")


@icon("shelf-price-label", CAT, "Price label strip on a shelf edge with a barcode on the left and a big price",
      tags=["shelf label", "price label", "shelf edge label", "price tag", "unit price", "supermarket"])
def _(S):
    return [line(seg(2, 4.5, 22, 4.5)),
            shell(rect(2.5, 7.5, 19, 11, L(S, 1, 2.5))),
            block(5, 10.5, 1, 5), block(7, 10.5, 2, 5), block(10, 10.5, 1, 5),
            detail(nine(12.5)), detail(nine(17))]


@icon("display-counter", CAT, "Shop counter with a sloping glass front and items on a shelf inside",
      tags=["display counter", "glass counter", "showcase", "display case", "deli counter", "shop counter"])
def _(S):
    return [shell(poly([(2, 21), (2, 12), (6.5, 4), (22, 4), (22, 21)], closed=True, r=S.r * 0.6)),
            detail(seg(2, 15, 22, 15)),
            block(8, 9, 3, 3, L(S, 0, 1.5)), block(13, 9, 3, 3, L(S, 0, 0.5)), block(17.5, 9, 2.5, 3, L(S, 0, 0.5))]


@icon("roll-cage-trolley", CAT, "Tall mesh roll cage on wheels with boxes inside",
      tags=["roll cage", "cage trolley", "roll container", "warehouse", "logistics", "stock delivery"])
def _(S):
    rx = L(S, 0, 0.5)
    return [line(rect(4, 2.5, 16, 17, L(S, 0, 1.5))), line(seg(4, 11, 20, 11)),
            line(seg(9.5, 2.5, 9.5, 11)), line(seg(14.5, 2.5, 14.5, 11)),
            block(7, 14, 4.5, 3.5, rx), block(12.5, 14, 4.5, 3.5, rx),
            dot(6, 21.5, 1.25), dot(18, 21.5, 1.25)]


@icon("platform-trolley", CAT, "Flat low platform trolley on wheels with one upright push handle",
      tags=["platform trolley", "flatbed trolley", "push cart", "dolly", "moving", "warehouse"])
def _(S):
    return [shell(rect(2, 14.5, 17.5, 3, L(S, 0.25, 1.5))),
            line(poly([(19.5, 14.5), (19.5, 3.5), (22, 3.5)], r=S.r)),
            shell(circle(5.5, 20.5, 1.75)), shell(circle(15.5, 20.5, 1.75))]


@icon("bargain-bin", CAT, "Open bin piled with a jumble of items and a price tag on its side",
      tags=["bargain bin", "clearance", "discount bin", "sale items", "cheap", "markdown"])
def _(S):
    tag = [(13, 15.5), (15, 13.5), (18.5, 13.5), (18.5, 17.5), (15, 17.5)]
    return [shell(poly([(2.5, 11), (21.5, 11), (19.5, 21.5), (4.5, 21.5)], closed=True, r=S.r * 0.6)),
            detail(poly(tag, closed=True, r=S.r * 0.3)),
            mark(circle(7, 7.5, 2.5)), mark(poly([(12, 3), (15, 6), (12, 9), (9, 6)], closed=True, r=L(S, 0, 0.5))),
            mark(rect(16, 4, 3.5, 5.5, L(S, 0, 1)))]


@icon("rolling-basket", CAT, "Shopping basket on two small wheels with a long pull handle",
      tags=["rolling basket", "wheeled basket", "shopping basket", "pull basket", "supermarket", "trolley basket"])
def _(S):
    return [shell(poly([(2, 10), (16, 10), (15, 18), (3, 18)], closed=True, r=S.r * 0.6)),
            detail(seg(6.5, 12.5, 6.5, 15.5)), detail(seg(11, 12.5, 11, 15.5)),
            line(seg(15.5, 11, 19.5, 3)), line(seg(18, 2.5, 21.5, 4)),
            shell(circle(5.5, 20.5, 1.5)), shell(circle(12.5, 20.5, 1.5))]


@icon("shopping-trolley-bag", CAT, "Tall fabric shopping bag on a two-wheeled frame with a curved handle",
      tags=["shopping trolley", "granny cart", "trolley bag", "wheeled bag", "shopping cart bag", "market bag"])
def _(S):
    return [shell(rect(4, 7, 10, 12.5, L(S, 1, 2.5))), detail(seg(4, 10.5, 14, 10.5)),
            line("M17 18.5V5A2.5 2.5 0 0 0 12 5"),
            shell(circle(16, 20, 2))]


@layered("cash-on-delivery", "Parcel with a banknote leaning against its front",
         tags=["cash on delivery", "cod", "pay on delivery", "pay cash", "delivery payment", "parcel"])
def _(S):
    note = [shell(rect(8, 12.5, 14, 8.5, L(S, 0.5, 1.5))), detail(circle(15, 16.75, 1.75))]
    box = [shell(rect(2, 3, 15, 13, L(S, 1, 2))), detail(seg(9.5, 3, 9.5, 7))]
    return [note, box]


@icon("store-locator", CAT, "Map pin with a small shop awning inside its round head",
      tags=["store locator", "find a store", "shop finder", "nearest store", "location", "branch finder"])
def _(S):
    return [shell(pin_d(12, 9.5, 7.5, 22)),
            detail(poly([(7.75, 9.5), (9.25, 5.5), (14.75, 5.5), (16.25, 9.5)], closed=True, r=S.r * 0.3)),
            detail(poly([(9, 9.5), (9, 13), (15, 13), (15, 9.5)], r=S.r * 0.3))]


# ============================================================================ chunk 6: remaining concepts

def _letter_r(x, y):
    return f"M{fmt(x)} {fmt(y + 5)}V{fmt(y)}H{fmt(x + 2)}A1.25 1.25 0 0 1 {fmt(x + 2)} {fmt(y + 2.5)}H{fmt(x)}M{fmt(x + 2)} {fmt(y + 2.5)}L{fmt(x + 3.25)} {fmt(y + 5)}"


@icon("raci-matrix", CAT, "Table grid with the letters R, A, C and I in separate cells",
      tags=["raci", "responsibility matrix", "roles", "accountable", "consulted", "informed", "project management"])
def _(S):
    def thin(d, w=1.5):
        return mark(path_to_d(ST(d, w, "butt", "miter")))
    return [shell(rect(2.5, 2.5, 19, 19, L(S, 1, 3))), detail(seg(12, 2.5, 12, 21.5)), detail(seg(2.5, 12, 21.5, 12)),
            thin(_letter_r(5.5, 4.5)),
            thin("M14.25 10V6.5L15.75 4.5L17.25 6.5V10M14.25 8.5H17.25"),
            thin("M9.5 15.25V14.25H6.5V17.25H9.5V16.25", 1.5),
            thin("M15.75 14V19M14.25 14H17.25M14.25 19H17.25")]


@icon("delivery-backpack", CAT, "Boxy insulated delivery backpack seen from behind with a zip lid and two curved shoulder straps",
      tags=["delivery backpack", "courier bag", "food delivery", "thermal bag", "insulated bag", "rider"])
def _(S):
    return [shell(rect(4, 3, 16, 18.5, L(S, 1.5, 3))),
            detail(seg(4, 8, 20, 8)), block(11, 4.5, 2, 1.5, 0),
            detail("M8.5 8C9.5 13 9.5 17 7.5 21.5"), detail("M15.5 8C14.5 13 14.5 17 16.5 21.5")]


@layered("price-labeler", "Handheld price label gun with a roll of labels on top and a label sticking out of the nozzle",
         tags=["price gun", "label gun", "price labeler", "retail", "stock marking", "labelling"])
def _(S):
    gun = [(6, 11.5), (17, 11.5), (21.5, 13.5), (21.5, 16.5), (18.5, 16.5), (19, 21.5), (14.5, 21.5), (13.5, 16.5), (6, 16.5)]
    body = [shell(poly(gun, closed=True, r=S.r * 0.5)), block(1.5, 12.5, 4, 3, L(S, 0, 0.75))]
    roll = [shell(circle(10.5, 6.5, 4.5)), dot(10.5, 6.5, 1.25)]
    return [body, roll]


@icon("tagging-gun", CAT, "Pistol-grip tagging gun with a long hollow needle and a clip of plastic fasteners",
      tags=["tagging gun", "tag gun", "fastener gun", "clothing tag", "retail", "price tag attacher"])
def _(S):
    gun = [(9, 4.5), (20, 4.5), (22, 6.5), (22, 10.5), (18.5, 10.5), (19, 20.5), (13.5, 20.5), (12.5, 10.5), (9, 10.5)]
    return [shell(poly(gun, closed=True, r=S.r * 0.5)),
            line(seg(1.5, 7.5, 9, 7.5)),
            mark(circle(3.5, 12.5, 1.25)), mark(circle(7, 12.5, 1.25)), mark(circle(10.5, 14.5, 1.25))]
