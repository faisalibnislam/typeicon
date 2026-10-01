"""TypeIcon Core: signage (batch 2): prohibition, warning, mandatory and information signs, drawn as small pictograms."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "signage"


# --------------------------------------------------------------------------- helpers (local coordinates, centre 0,0)

def stroke(pts, w=1.6, closed=False):
    return ST(poly(pts, closed=closed), w, "round", "round")


def pth(d, w=1.6):
    return ST(d, w, "round", "round")


def ell(cx, cy, rx, ry):
    return P(ellipse(cx, cy, rx, ry))


def cir(cx, cy, r):
    return P(circle(cx, cy, r))


def pg(pts, r=0.0):
    return P(poly(pts, closed=True, r=r))


def rc(x, y, w, h, r=0.0):
    return P(rect(x, y, w, h, r))


def uu(*ps):
    return U(*ps)


def put(p, cx=12.0, cy=12.0, s=1.0, fx=False):
    return path_to_d(transform_path(p, (-s if fx else s, 0, 0, s, cx, cy)))


def mark(d):
    """Solid pictogram part: solid in Line/Rounded, knocked out of a solid frame in Filled."""
    return Part("dot", d)


def soften(p, g=0.45):
    """Round the convex corners of a region (shrink, then grow) for the Rounded style."""
    try:
        sh = D(p, ST(path_to_d(p), 2 * g, "butt", "miter"))
        return U(sh, ST(path_to_d(sh), 2 * g, "round", "round"))
    except Exception:
        return p


def fin(S, p, g=0.45):
    return p if S.name == "line" else soften(p, g)


def person(x=0, y=0, s=1.0, w=1.7):
    """Standing figure about 10 tall, head top at y-5."""
    h = cir(x, y - 4.1 * s, 1.25 * s)
    b = stroke([(x, y - 2.3 * s), (x, y + 0.8 * s)], 2.0 * s)
    lg = stroke([(x - 1.3 * s, y + 4.8 * s), (x, y + 0.8 * s), (x + 1.3 * s, y + 4.8 * s)], 1.6 * s)
    ar = stroke([(x - 2 * s, y + 0.8 * s), (x, y - 1.6 * s), (x + 2 * s, y + 0.8 * s)], 1.4 * s)
    return uu(h, b, lg, ar)


DIAG = "M5.8 5.8L18.2 18.2"


def prohibit(S, pic, gap=0.55):
    """Prohibition sign: ring, diagonal bar, pictogram (local coords, centred) cut clear of the bar."""
    cut = ST(DIAG, 2 + 2 * gap, "butt", "miter")
    diag = DIAG if S.name == "line" else "M7.6 7.6L16.4 16.4"
    return [shell(circle(12, 12, 9)), detail(diag),
            mark(path_to_d(D(transform_path(fin(S, pic), (1, 0, 0, 1, 12, 12)), cut)))]


T3 = [(12, 3.5), (21.5, 20.5), (2.5, 20.5)]


def tri(S):
    return shell(poly(T3, closed=True, r=S.r * 1.0), stroke_miterlimit="4")


def warn(S, pic, cy=16.3, s=1.0, fx=False):
    return [tri(S), mark(put(pic, 12, cy, s, fx))]


def dia(S):
    c = 9.5
    return shell(poly([(12, 12 - c), (12 + c, 12), (12, 12 + c), (12 - c, 12)], closed=True, r=S.r * 1.2))


def dsign(S, pic, cy=12.0, s=1.0, fx=False):
    return [dia(S), mark(put(pic, 12, cy, s, fx))]


def msign(S, pic, s=1.0):
    return [shell(circle(12, 12, 9)), mark(put(pic, 12, 12, s))]


# --------------------------------------------------------------------------- prohibition signs

@icon("no-tattoos-sign", CAT, "Prohibition circle over a forearm carrying a star tattoo.",
      tags=["no tattoos", "tattoo ban", "prohibited", "body art", "skin", "forbidden"])
def _(S):
    arm = uu(stroke([(-5.0, 5.0), (1.2, -1.2)], 4.6), ell(3.6, -3.6, 2.6, 3.4))
    arm = transform_path(arm, (1, 0, 0, 1, 0, 0))
    star = pg([p for i in range(5) for p in (
        (-2.6 + 2.0 * math.cos(math.radians(-90 + i * 72)), 2.6 + 2.0 * math.sin(math.radians(-90 + i * 72))),
        (-2.6 + 0.9 * math.cos(math.radians(-54 + i * 72)), 2.6 + 0.9 * math.sin(math.radians(-54 + i * 72))))])
    return prohibit(S, D(arm, star))


@icon("no-crossing-tracks-sign", CAT, "Prohibition circle over a person stepping across railway tracks.",
      tags=["no crossing", "railway", "tracks", "train", "trespass", "level crossing"])
def _(S):
    fig = person(2.8, -1.2, 0.95)
    rails = uu(rc(-6.0, 3.4, 12.0, 1.2), rc(-6.0, 5.6, 12.0, 1.2),
               rc(-5.2, 3.4, 1.3, 3.4), rc(-1.8, 3.4, 1.3, 3.4), rc(1.6, 3.4, 1.3, 3.4), rc(5.0, 3.4, 1.3, 3.4))
    return prohibit(S, uu(fig, rails))


@icon("no-crowd-surfing-sign", CAT, "Prohibition circle over a person carried flat on raised hands above a crowd.",
      tags=["no crowd surfing", "concert", "mosh pit", "crowd", "prohibited", "festival"])
def _(S):
    body = uu(ell(2.4, -3.0, 3.8, 1.4), cir(-2.0, -3.4, 1.4))
    heads = uu(*[cir(x, 4.2, 1.3) for x in (-4.6, -1.6, 1.4)])
    hands = uu(*[stroke([(x, 2.4), (x + 0.6, -0.4)], 1.1) for x in (-4.6, -1.6, 1.4)])
    return prohibit(S, uu(body, heads, hands))


@icon("no-standing-on-toilet-sign", CAT, "Prohibition circle over a person crouching with both feet on a toilet seat.",
      tags=["no standing", "toilet", "squat", "restroom", "bathroom", "prohibited", "feet on seat"])
def _(S):
    toilet = uu(rc(-6.0, -1.0, 3.0, 5.0), P("M-3.4 2.6H5.8V4.4Q5.8 6.2 3.8 6.2H-0.6Q-3.4 6.2 -3.4 4Z"))
    fig = uu(cir(3.4, -5.2, 1.4), stroke([(3.2, -3.4), (2.2, -0.6)], 2.2),
             stroke([(2.2, -0.6), (4.8, 0.2), (4.6, 2.2)], 1.7), stroke([(2.8, -2.8), (5.4, -1.8)], 1.4))
    return prohibit(S, uu(toilet, fig))


@icon("no-stepping-on-surface-sign", CAT, "Prohibition circle over a shoe sole above a hatched flat panel.",
      tags=["no stepping", "do not step", "fragile surface", "keep off", "skylight", "panel", "prohibited"])
def _(S):
    sole = uu(ell(3.6, -4.6, 2.2, 2.0), P("M2.0 -3.2L5.6 -3.4Q5.2 -1.6 4.8 -0.6Q4.4 1.0 3.0 1.0Q1.4 1.0 1.4 -0.4Z"))
    panel = uu(rc(-6.0, 3.0, 12.0, 1.2), rc(-6.0, 5.6, 12.0, 1.2),
               rc(-5.2, 3.0, 1.3, 3.8), rc(-1.8, 3.0, 1.3, 3.8), rc(1.6, 3.0, 1.3, 3.8), rc(5.0, 3.0, 1.3, 3.8))
    return prohibit(S, uu(sole, panel))


@icon("no-reaching-in-sign", CAT, "Prohibition circle over a hand reaching into the opening of a machine guard.",
      tags=["no reaching in", "machine guard", "keep hands out", "danger", "moving parts", "prohibited"])
def _(S):
    guard = uu(rc(0.8, -6.0, 1.6, 4.8), rc(0.8, 1.6, 1.6, 4.8), rc(0.8, -6.0, 5.2, 1.6), rc(0.8, 4.8, 5.2, 1.6), rc(4.8, -6.0, 1.6, 12.0))
    hand = uu(rc(-6.2, -0.9, 5.2, 2.4), rc(-1.4, -2.2, 3.6, 4.6, 1.0))
    return prohibit(S, uu(guard, hand))


@icon("no-heavy-load-sign", CAT, "Prohibition circle over a heavy block with a downward arrow above a flat surface.",
      tags=["no heavy loads", "weight limit", "do not overload", "load limit", "prohibited", "heavy", "floor load"])
def _(S):
    block = rc(-3.8, -0.6, 7.6, 4.6, 0.6)
    arrow = uu(rc(-0.8, -6.4, 1.6, 3.4), pg([(-2.8, -3.2), (2.8, -3.2), (0, -0.6)]))
    floor = rc(-6.2, 4.6, 12.4, 1.4)
    return prohibit(S, uu(block, arrow, floor))


# --------------------------------------------------------------------------- information and warning signs

@icon("automatic-door-sign", CAT, "Sliding door panels with outward chevrons and a sensor under the header.",
      tags=["automatic door", "sliding door", "sensor", "auto door", "entrance", "shop door"])
def _(S):
    return [shell(rect(3.5, 3.5, 17, 17, S.R)), detail("M3.5 9H20.5"), detail("M12 9V20.5"),
            dot(12, 6.25, 1.1),
            line(poly([(9, 12.5), (6.5, 15), (9, 17.5)], r=S.r)), line(poly([(15, 12.5), (17.5, 15), (15, 17.5)], r=S.r))]


@icon("glass-door-sign", CAT, "Glass door with glare lines beside a person about to walk into it.",
      tags=["glass door", "clear glass", "walk into", "collision", "transparent", "caution glass", "patio door"])
def _(S):
    return [shell(rect(3.5, 3.5, 10, 17, min(S.R, 2))), dot(11, 12.5, 0.9),
            line(poly([(6, 12), (11, 7)])), line(poly([(6, 17), (11, 12)])),
            mark(put(fin(S, person(0, 0, 1.0)), 18.2, 12.5, 1.0))]


@icon("doors-closing-sign", CAT, "Two train door leaves closing in on a hand caught between them.",
      tags=["doors closing", "train doors", "mind the doors", "hand caught", "trapped", "metro", "caution doors"])
def _(S):
    hand = uu(rc(-2.2, 1.6, 4.4, 4.2, 1.0), rc(-2.2, -2.8, 1.0, 5.0, 0.5), rc(-0.5, -3.6, 1.0, 5.8, 0.5), rc(1.2, -2.8, 1.0, 5.0, 0.5))
    arr = uu(pg([(-3.6, -5.2), (-1.4, -3.6), (-3.6, -2.0)]), pg([(3.6, -5.2), (1.4, -3.6), (3.6, -2.0)]))
    return [shell(rect(3.5, 3.5, 4.5, 17, 0.4 if S.name == 'line' else 2.2)), shell(rect(16, 3.5, 4.5, 17, 0.4 if S.name == 'line' else 2.2)),
            mark(put(hand, 12, 15.0, 1.0)), mark(put(arr, 12, 8.4, 1.0))]


@icon("stray-golf-balls-sign", CAT, "Warning triangle with a golf ball flying along a dotted arc toward a person.",
      tags=["stray golf balls", "golf course", "flying ball", "caution", "fairway", "warning"])
def _(S):
    ball = cir(-4.2, -0.6, 1.5)
    dots = uu(*[cir(x, y, 0.5) for x, y in ((-2.2, -1.6), (-0.4, -2.0), (1.2, -1.5))])
    return warn(S, uu(ball, dots, person(4.2, -0.3, 0.5)), cy=16.4)


@icon("flashing-lights-sign", CAT, "Warning triangle with a spotlight sending out alternating long and short rays.",
      tags=["flashing lights", "strobe", "photosensitive", "epilepsy", "strobe lights", "warning"])
def _(S):
    rays = uu(*[stroke([(2.5 * math.cos(math.radians(a)), 1.2 + 2.5 * math.sin(math.radians(a))),
                         ((2.5 + L) * math.cos(math.radians(a)), 1.2 + (2.5 + L) * math.sin(math.radians(a)))], 1.0)
                for a, L in ((-90, 2.0), (-50, 1.1), (-130, 1.1), (-15, 1.9), (-165, 1.9))])
    return warn(S, uu(cir(0, 1.2, 1.5), rays), cy=16.4)


@icon("smoke-effects-sign", CAT, "Warning triangle with a haze machine blowing out a billowing cloud.",
      tags=["smoke effects", "haze machine", "fog machine", "theatre smoke", "stage smoke", "warning"])
def _(S):
    box = rc(-6.0, 0.4, 3.6, 2.8, 0.5)
    cloud = uu(cir(0.2, 1.2, 1.7), cir(2.4, 0.0, 2.0), cir(4.4, 1.4, 1.5), cir(2.3, 2.2, 1.6), rc(-2.6, 1.0, 1.2, 1.2))
    return warn(S, uu(box, cloud), cy=16.6)


@icon("passing-trains-sign", CAT, "Warning triangle with a train front and speed lines racing past.",
      tags=["passing trains", "fast trains", "platform edge", "stand back", "railway", "warning"])
def _(S):
    body = D(rc(-2.6, -3.2, 5.2, 6.4, 1.6), rc(-1.6, -2.3, 3.2, 1.9), cir(-1.3, 1.6, 0.6), cir(1.3, 1.6, 0.6))
    spd = uu(rc(-6.0, 0.0, 2.2, 0.8), rc(3.8, 0.0, 2.2, 0.8), rc(-5.4, 1.8, 1.8, 0.8), rc(3.6, 1.8, 1.8, 0.8))
    return warn(S, uu(body, spd), cy=16.2)


@icon("ticks-warning-sign", CAT, "Warning triangle with an eight-legged tick seen from above.",
      tags=["ticks", "tick warning", "lyme", "bug", "parasite", "tall grass", "warning"])
def _(S):
    legs = uu(*[stroke([(sx * 1.8, y), (sx * 4.8, y2)], 0.9) for sx in (-1, 1)
                for y, y2 in ((-1.6, -2.8), (-0.4, -0.8), (0.8, 1.6), (1.8, 3.2))])
    return warn(S, uu(ell(0, 0.4, 2.3, 2.7), cir(0, -2.4, 1.0), legs), cy=16.2)


@icon("swim-between-flags-sign", CAT, "Swimmer in the waves between two upright beach flags.",
      tags=["swim between the flags", "beach", "lifeguard", "patrolled area", "surf", "safe swimming", "flags"])
def _(S):
    return [line("M4.5 3V13.5"), line("M19.5 3V13.5"),
            solid(poly([(5.5, 3), (10, 5.25), (5.5, 7.5)], closed=True)), solid(poly([(18.5, 3), (14, 5.25), (18.5, 7.5)], closed=True)),
            shell(circle(10.5, 11, 1.7)), line("M12.5 12.5Q14.8 9.5 17 11.5"),
            line("M3 16Q5.2 14 7.5 16T12 16T16.5 16T21 16"), line("M3 20.5Q5.2 18.5 7.5 20.5T12 20.5T16.5 20.5T21 20.5")]


@icon("unattended-baggage-sign", CAT, "Lone suitcase with an exclamation mark beside it.",
      tags=["unattended baggage", "lost luggage", "suspicious bag", "security", "abandoned bag", "report bag"])
def _(S):
    return [shell(rect(3, 10.5, 14, 10.5, min(S.R, 2))), line(poly([(7, 10.5), (7, 7.5), (13, 7.5), (13, 10.5)], r=S.r * 0.5)),
            detail("M3 15.5H17") if False else dot(10, 15.7, 1.1), line("M20 3.5V10"), dot(20, 14.2, 1.15)]


@icon("cyclists-dismount-sign", CAT, "Person walking beside a bicycle with a hand on the handlebar.",
      tags=["cyclists dismount", "push bike", "walk your bike", "dismount", "pedestrian zone", "bicycle"])
def _(S):
    return [shell(circle(9.5, 18.5, 2.4)), shell(circle(19, 18.5, 2.4)),
            line(poly([(9.5, 18.5), (12.5, 14), (19, 14), (19, 18.5)])), line("M19 14V11"), line("M17.5 11H21"),
            shell(circle(4.2, 4.8, 1.6)), line("M4.2 8V14"), line(poly([(2.6, 21), (4.2, 14), (6.2, 21)], r=S.r)),
            line("M4.2 9.5L18 11")]


@icon("falling-coconuts-sign", CAT, "Warning triangle with a palm crown dropping a coconut toward a person below.",
      tags=["falling coconuts", "palm tree", "beach", "tropical", "danger from above", "warning"])
def _(S):
    palm = uu(stroke([(-4.2, 3.2), (-3.8, -0.6)], 1.2),
              *[pth(f"M-3.8 -0.8Q{a} {b} {c} {d}", 1.0) for a, b, c, d in ((-5.4, -2.6, -6.4, -0.4), (-2.4, -3.0, -0.8, -0.6), (-4.8, -2.8, -4.6, -3.6), (-3.0, -2.6, -2.2, -3.4))])
    return warn(S, uu(palm, cir(-0.4, 1.4, 0.95), cir(-0.4, -0.6, 0.35), person(4.2, 0.0, 0.5)), cy=16.2)


@icon("shooting-range-sign", CAT, "Warning triangle with a bullseye target and a dotted line of fire toward it.",
      tags=["shooting range", "firing range", "gun range", "target", "bullseye", "live fire", "warning"])
def _(S):
    tgt = uu(D(cir(2.4, 0, 3.3), cir(2.4, 0, 2.2)), cir(2.4, 0, 1.0))
    return warn(S, uu(tgt, *[cir(x, 0, 0.5) for x in (-5.4, -3.8, -2.2)]), cy=16.4)


@icon("roof-snow-slide-sign", CAT, "Warning triangle with a slab of snow sliding off a roof onto a person.",
      tags=["roof snow", "snow slide", "falling snow", "avalanche roof", "ice", "winter hazard", "warning"])
def _(S):
    roof = stroke([(-6.0, -3.6), (-0.4, -0.2)], 1.3)
    slab = stroke([(-4.8, -4.2), (-1.6, -2.4)], 1.9)
    return warn(S, uu(roof, slab, cir(0.8, 0.6, 0.55), person(4.2, 0.0, 0.5)), cy=16.4)


# --------------------------------------------------------------------------- animal crossing signs (silhouettes facing right)

def _legs(*xs, y=1.4, h=2.2, w=0.95):
    return uu(*[rc(x, y, w, h, 0.3) for x in xs])


def p_moose():
    body = ell(-0.8, 0.4, 3.0, 1.7)
    neck = stroke([(1.4, -0.2), (3.2, -1.4)], 2.2)
    head = ell(4.5, -0.6, 1.5, 0.95)
    ant = pg([(2.8, -2.2), (2.0, -3.4), (3.2, -3.1), (3.6, -4.0), (4.4, -3.2), (5.2, -3.6), (5.2, -2.4), (4.2, -1.9)])
    dew = cir(3.3, 0.5, 0.6)
    return uu(body, neck, head, ant, dew, _legs(-3.5, -2.4, 0.5, 1.6, y=1.5, h=2.3))


def p_elephant():
    body = ell(-0.8, 0.0, 3.3, 2.2)
    head = cir(3.0, -0.5, 1.9)
    trunk = pth("M4.2 0.6Q5.7 1.2 5.0 3.4", 1.4)
    legs = _legs(-3.6, -2.0, 0.2, 1.6, y=1.2, h=2.5, w=1.3)
    ear = stroke([(2.0, -1.6), (1.3, 0.0), (2.4, 1.2)], 0.6)
    return D(uu(body, head, trunk, legs, stroke([(-4.0, -0.8), (-4.8, 1.6)], 0.7)), ear)


def p_penguin():
    body = uu(ell(0, 0.8, 2.4, 3.0), cir(0.3, -2.7, 1.4))
    belly = ell(0.9, 1.1, 1.1, 2.0)
    beak = pg([(1.4, -3.1), (3.0, -2.3), (1.4, -2.0)])
    feet = uu(ell(-0.8, 3.9, 1.1, 0.5), ell(1.2, 3.9, 1.1, 0.5))
    flip = stroke([(-1.8, -0.4), (-3.1, 1.8)], 1.1)
    return uu(D(body, belly), beak, feet, flip)


def p_koala():
    body = ell(-0.4, 1.0, 3.0, 1.8)
    head = cir(3.0, -0.2, 1.9)
    ears = uu(cir(1.4, -2.2, 1.35), cir(4.4, -2.4, 1.35))
    nose = ell(4.6, 0.1, 0.75, 0.9)
    return D(uu(body, head, ears, _legs(-3.0, 1.4, y=2.0, h=1.9, w=1.3)), nose)


def p_wombat():
    body = ell(-0.6, 0.6, 3.8, 2.3)
    head = uu(cir(3.4, 0.6, 1.8), rc(3.6, 0.6, 2.0, 1.5, 0.7))
    ear = cir(2.5, -1.2, 0.6)
    return uu(body, head, ear, _legs(-3.4, -1.9, 1.6, 2.7, y=2.2, h=1.5, w=1.1))


def p_hedgehog():
    cx, cy, rx, ry = -0.8, 1.2, 4.0, 3.0
    pts = [(cx - rx, cy + 1.0)]
    n = 11
    for i in range(n + 1):
        a = math.radians(180 + 14 + i * (152 / n))
        rr = 1.0 if i % 2 == 0 else 0.76
        pts.append((cx + rx * 1.12 * rr * math.cos(a), cy + ry * 1.2 * rr * math.sin(a)))
    pts.append((cx + rx, cy + 1.0))
    back = pg(pts)
    face = pg([(2.4, 0.4), (5.8, 2.4), (5.6, 3.0), (2.4, 3.2)])
    nose = cir(5.8, 2.6, 0.55)
    return uu(back, face, nose, rc(-2.8, 3.0, 1.0, 1.0), rc(1.0, 3.0, 1.0, 1.0), ell(-0.4, 2.6, 3.3, 1.2))


def p_squirrel():
    tail = pth("M-2.0 3.0Q-5.6 1.6 -4.2 -2.0Q-3.4 -3.6 -2.0 -3.4", 2.4)
    body = ell(0.0, 1.4, 1.7, 2.2)
    head = cir(1.7, -1.1, 1.15)
    ear = pg([(1.4, -2.0), (1.5, -3.0), (2.4, -2.0)])
    leg = ell(-0.6, 3.0, 1.6, 0.7)
    nose = cir(2.9, -0.7, 0.5)
    return uu(tail, body, head, ear, leg, nose, stroke([(1.4, 0.8), (2.6, 1.8)], 0.9))


def p_otter():
    body = stroke([(-3.2, 1.1), (2.2, 0.6)], 3.4)
    tail = stroke([(-3.2, 1.3), (-6.0, 2.8)], 1.5)
    head = cir(3.5, -0.1, 1.55)
    snout = ell(4.9, 0.5, 0.85, 0.65)
    legs = _legs(-2.4, 1.4, y=1.8, h=1.9, w=1.1)
    return uu(body, tail, head, snout, legs)


def p_crab():
    body = ell(0, 1.2, 3.3, 2.1)
    claws = []
    for sx in (-1, 1):
        arm = stroke([(sx * 2.4, 0.2), (sx * 4.0, -2.4)], 0.95)
        c = D(cir(sx * 4.2, -3.0, 1.35), pg([(sx * 4.2, -3.0), (sx * 3.4, -4.6), (sx * 5.2, -4.6)]))
        legs = uu(*[stroke([(sx * 2.6, 1.2 + k * 0.5), (sx * 5.4, 1.0 + k * 1.5 + 0.4)], 0.85) for k in range(3)])
        claws += [arm, c, legs]
    return uu(body, *claws)


def p_bison():
    body = uu(ell(1.0, 0.4, 3.0, 2.0), ell(-2.2, 0.9, 2.2, 1.6), cir(1.6, -1.2, 2.0))
    head = uu(ell(4.6, 1.4, 1.35, 1.6), pg([(4.6, -0.2), (5.4, -1.6), (5.9, -0.9), (5.5, 0.4)]))
    beard = pg([(3.8, 2.6), (4.8, 2.6), (4.2, 3.8)])
    return uu(body, head, beard, _legs(-3.6, -2.4, 0.3, 1.6, y=1.8, h=2.0, w=0.95), stroke([(-4.2, 0.2), (-5.2, 2.0)], 0.7))


def p_monkey():
    body = ell(0, 0.0, 2.9, 1.5)
    head = cir(3.3, -1.0, 1.3)
    ear = cir(2.5, -2.0, 0.65)
    muzzle = ell(4.4, -0.7, 0.8, 0.7)
    legs = uu(stroke([(1.8, 0.8), (2.6, 3.4)], 1.0), stroke([(-2.0, 0.6), (-2.8, 3.4)], 1.1),
              stroke([(1.0, 1.0), (0.4, 3.4)], 0.9), stroke([(-1.0, 0.9), (-1.6, 3.4)], 0.9))
    tail = pth("M-2.7 -0.5Q-5.8 -0.6 -5.4 -3.0Q-5.1 -4.2 -3.9 -3.6", 0.9)
    return uu(body, head, ear, muzzle, legs, tail)


def p_sheep():
    fleece = uu(cir(-2.4, 0.0, 1.8), cir(-0.6, -1.0, 2.0), cir(1.4, -0.8, 1.9), cir(2.4, 0.6, 1.5),
                cir(-1.0, 1.0, 1.9), cir(1.0, 1.2, 1.8))
    head = ell(4.5, 0.3, 1.0, 1.5)
    ear = ell(3.5, -0.8, 0.8, 0.45)
    return uu(fleece, head, ear, _legs(-2.4, 1.3, y=1.9, h=2.0, w=0.95))


def p_badger():
    body = ell(-0.6, 0.9, 3.5, 1.9)
    head = pg([(2.4, -0.6), (4.0, -0.9), (6.0, 1.3), (4.4, 2.2), (2.4, 2.2)], r=0.5)
    stripe = uu(stroke([(3.0, -0.4), (5.1, 1.1)], 0.45), stroke([(3.7, 0.2), (5.7, 1.6)], 0.45))
    return D(uu(body, head, _legs(-3.0, -1.6, 1.0, 2.2, y=2.2, h=1.5, w=1.1)), stripe)


def p_kiwi():
    body = ell(-0.6, 0.2, 3.5, 2.6)
    head = cir(2.8, -1.2, 1.1)
    beak = stroke([(3.6, -0.7), (6.0, 2.2)], 0.75)
    legs = uu(stroke([(-1.4, 2.4), (-1.4, 4.0)], 0.9), stroke([(0.4, 2.4), (0.5, 4.0)], 0.9))
    return uu(body, head, beak, legs)


def p_emu():
    body = ell(-0.6, 0.6, 3.2, 2.0)
    neck = stroke([(1.6, -0.2), (3.2, -3.4)], 1.2)
    head = ell(3.9, -3.9, 1.35, 0.8)
    legs = uu(stroke([(-1.0, 2.2), (-1.2, 5.0)], 0.95), stroke([(0.6, 2.2), (1.3, 5.0)], 0.95))
    fur = pg([(-3.8, 0.0), (-4.8, 2.2), (-3.0, 2.0), (-2.4, 3.2), (-1.6, 2.4), (-3.0, 0.8)])
    return uu(body, neck, head, legs, fur)


def p_armadillo():
    shell_ = ell(-0.3, 0.6, 3.7, 2.5)
    shell_ = D(shell_, rc(-5, 2.6, 10, 3))
    bands = uu(*[stroke([(x, -2.6), (x - 0.5, 2.4)], 0.45) for x in (-2.3, -0.9, 0.5, 1.9)])
    head = pg([(3.0, -0.4), (6.0, 1.6), (3.0, 2.6)], r=0.4)
    ear = pg([(3.0, -0.3), (3.4, -1.8), (4.2, -0.5)])
    tail = stroke([(-3.6, 1.6), (-6.0, 2.6)], 0.9)
    legs = _legs(-2.6, 1.4, y=2.0, h=1.6, w=1.1)
    return uu(D(shell_, bands), head, ear, tail, legs)


def p_boar():
    body = ell(-0.6, 0.5, 3.4, 2.0)
    head = uu(cir(3.3, 0.7, 1.7), rc(4.0, 0.9, 2.0, 1.5, 0.6))
    ear = pg([(2.7, -0.6), (2.8, -2.2), (4.0, -0.8)])
    bristles = pg([(-3.6, -0.6), (-3.0, -2.2), (-2.2, -1.2), (-1.4, -2.6), (-0.6, -1.4), (0.2, -2.6), (0.8, -1.2), (1.8, -1.0)])
    tusk = pg([(5.0, 2.1), (5.4, 3.2), (4.4, 2.4)])
    return uu(body, head, ear, bristles, tusk, _legs(-3.3, -1.9, 0.4, 1.8, y=1.8, h=1.9, w=1.0), stroke([(-3.8, 0.0), (-4.8, 1.4)], 0.7))


def _animal(name, desc, tags, frame, pic, s=1.0, cy=None, fx=False):
    cy = cy if cy is not None else (12.0 if frame == "dia" else 16.5)

    @icon(name, CAT, desc, tags=tags)
    def _(S):
        return (dsign if frame == "dia" else warn)(S, pic(), cy=cy, s=s, fx=fx)
    return _


_animal("moose-crossing-sign", "Diamond sign with a moose in profile showing broad antlers.",
        ["moose crossing", "elk", "deer", "wildlife crossing", "road sign", "antlers", "animal crossing"], "dia", p_moose, 0.95, 12.6)
_animal("elephant-crossing-sign", "Diamond sign with a walking elephant, trunk curved down.",
        ["elephant crossing", "wildlife crossing", "road sign", "safari", "animal crossing", "trunk"], "dia", p_elephant, 0.95, 11.6)
_animal("penguin-crossing-sign", "Triangle sign with an upright penguin waddling.",
        ["penguin crossing", "wildlife crossing", "road sign", "antarctic", "animal crossing", "waddle"], "tri", p_penguin, 0.8, 16.3)
_animal("koala-crossing-sign", "Diamond sign with a koala on all fours showing round ears.",
        ["koala crossing", "wildlife crossing", "road sign", "australia", "marsupial", "animal crossing"], "dia", p_koala, 1.0, 12.0)
_animal("wombat-crossing-sign", "Diamond sign with a stocky wombat in profile.",
        ["wombat crossing", "wildlife crossing", "road sign", "australia", "marsupial", "animal crossing"], "dia", p_wombat, 1.0, 11.6)
_animal("hedgehog-crossing-sign", "Triangle sign with a spiky hedgehog in profile.",
        ["hedgehog crossing", "wildlife crossing", "road sign", "spines", "garden animal", "animal crossing"], "tri", p_hedgehog, 0.85, 15.3)
_animal("squirrel-crossing-sign", "Triangle sign with a squirrel in profile and a bushy tail.",
        ["squirrel crossing", "wildlife crossing", "road sign", "rodent", "bushy tail", "animal crossing"], "tri", p_squirrel, 0.85, 16.0)
_animal("otter-crossing-sign", "Triangle sign with a long low otter walking.",
        ["otter crossing", "wildlife crossing", "road sign", "river animal", "animal crossing", "waterway"], "tri", p_otter, 0.9, 16.4)
_animal("crab-crossing-sign", "Diamond sign with a crab from above, claws raised.",
        ["crab crossing", "wildlife crossing", "road sign", "migration", "beach", "claws", "animal crossing"], "dia", p_crab, 0.95, 12.2)
_animal("bison-crossing-sign", "Diamond sign with a bison in profile showing a shoulder hump.",
        ["bison crossing", "buffalo", "wildlife crossing", "road sign", "prairie", "animal crossing"], "dia", p_bison, 0.95, 11.8)
_animal("wild-boar-crossing-sign", "Triangle sign with a bristly wild boar in profile.",
        ["wild boar crossing", "pig", "hog", "wildlife crossing", "road sign", "tusks", "animal crossing"], "tri", p_boar, 0.85, 16.0)
_animal("monkey-crossing-sign", "Diamond sign with a monkey walking on all fours.",
        ["monkey crossing", "primate", "wildlife crossing", "road sign", "animal crossing", "curled tail"], "dia", p_monkey, 1.0, 12.4)
_animal("sheep-crossing-sign", "Triangle sign with a woolly sheep in profile.",
        ["sheep crossing", "flock", "livestock", "road sign", "wool", "lamb", "animal crossing"], "tri", p_sheep, 0.9, 16.2)
_animal("badger-crossing-sign", "Triangle sign with a low badger in profile.",
        ["badger crossing", "wildlife crossing", "road sign", "striped face", "animal crossing", "setts"], "tri", p_badger, 0.9, 16.2)
_animal("kiwi-bird-crossing-sign", "Diamond sign with a round kiwi bird showing a long thin beak.",
        ["kiwi crossing", "bird crossing", "new zealand", "flightless bird", "wildlife crossing", "road sign"], "dia", p_kiwi, 1.0, 11.4)
_animal("emu-crossing-sign", "Diamond sign with a tall emu on long legs.",
        ["emu crossing", "flightless bird", "australia", "wildlife crossing", "road sign", "animal crossing"], "dia", p_emu, 0.85, 12.0)
_animal("armadillo-crossing-sign", "Diamond sign with an armadillo showing banded shell segments.",
        ["armadillo crossing", "wildlife crossing", "road sign", "armored animal", "animal crossing", "banded shell"], "dia", p_armadillo, 1.0, 11.8)


def rot(p, deg, cx=0.0, cy=0.0):
    return transform_path(p, rotation(deg, cx, cy))


# --------------------------------------------------------------------------- warning triangles and diamonds

def p_lion():
    body = ell(-0.6, 0.8, 3.4, 1.4)
    haunch = cir(-2.8, 1.0, 1.5)
    head = cir(3.6, -0.2, 1.3)
    ears = uu(pg([(3.0, -1.0), (3.2, -2.3), (4.0, -1.2)]), pg([(4.2, -1.1), (4.7, -2.2), (5.0, -0.7)]))
    legs = uu(stroke([(2.0, 1.2), (2.6, 3.2)], 1.1), stroke([(0.2, 1.4), (0.2, 3.2)], 1.0), stroke([(-2.6, 1.6), (-2.8, 3.2)], 1.2))
    tail = pth("M-3.8 0.6Q-6.2 0.8 -5.8 3.0Q-5.6 3.7 -4.8 3.5", 1.0)
    return uu(body, haunch, head, ears, legs, tail)


def p_stingray():
    wing = pg([(0, -3.0), (2.4, -2.2), (5.6, 0.2), (2.2, 1.0), (0, 2.2), (-2.2, 1.0), (-5.6, 0.2), (-2.4, -2.2)], r=0.8)
    tail = pth("M0 1.6Q-0.6 3.2 1.6 3.6", 0.8)
    return D(uu(wing, tail), uu(cir(-1.0, -1.0, 0.4), cir(1.0, -1.0, 0.4)))


def p_cassowary():
    body = ell(-0.6, 0.7, 2.9, 2.0)
    neck = stroke([(1.2, -0.2), (2.4, -3.0)], 1.5)
    head = cir(2.8, -3.4, 1.0)
    beak = pg([(3.6, -3.6), (4.8, -3.0), (3.6, -2.8)])
    casque = pg([(1.8, -3.9), (2.3, -5.8), (3.8, -4.4), (3.4, -3.8)])
    legs = uu(stroke([(-1.0, 2.3), (-1.1, 4.0)], 1.0), stroke([(0.6, 2.3), (1.1, 4.0)], 1.0))
    return uu(body, neck, head, beak, casque, legs)


def p_scorpion():
    body = uu(ell(-0.8, 1.6, 3.0, 1.1), cir(2.4, 1.4, 1.1))
    arm = stroke([(2.8, 1.0), (4.6, 0.2)], 0.9)
    claw = D(cir(5.0, -0.4, 1.35), pg([(5.0, -0.4), (6.6, -1.6), (6.6, 0.6)]))
    tail = pth("M-3.6 1.4Q-6.2 0.2 -4.8 -2.4Q-3.4 -4.0 -1.2 -2.8", 1.2)
    sting = pg([(-2.0, -3.9), (0.0, -2.1), (-1.8, -1.6)])
    legs = uu(*[stroke([(x, 2.4), (x - 0.6, 3.9)], 0.8) for x in (-3.0, -1.6, -0.2, 1.2)])
    return uu(body, arm, claw, tail, sting, legs)


def p_bomb():
    body = uu(ell(0.6, 0, 4.0, 1.8), pg([(-3.0, -1.2), (-5.9, -3.0), (-5.9, 3.0), (-3.0, 1.2)]))
    bands = uu(stroke([(-2.2, -2.2), (-2.2, 2.2)], 0.5), stroke([(0.2, -2.4), (0.2, 2.4)], 0.5))
    body = D(rot(D(body, bands), -16, 0, 0), rc(-9, 1.0, 18, 8))
    ground = pg([(-5.8, 1.9), (-3.6, 1.5), (-1.4, 2.0), (1.0, 1.5), (3.2, 2.0), (5.8, 1.6), (5.8, 3.4), (-5.8, 3.4)])
    return uu(body, ground)


def p_jet():
    nozzle = D(cir(-3.9, -0.2, 2.0), cir(-3.9, -0.2, 0.95))
    winds = uu(*[stroke([(-1.0, y), (x2, y)], 0.8) for y, x2 in ((-1.4, 1.4), (0.2, 2.2), (1.8, 1.4))])
    fig = rot(person(4.2, 0.2, 0.5), 22, 4.2, 2.6)
    return uu(nozzle, winds, fig)


def p_prop():
    blade = ell(0, -2.0, 0.85, 1.7)
    props = uu(*[rot(blade, a) for a in (0, 120, 240)], cir(0, 0, 0.95))
    arcs = uu(*[pth(arc(0, 0, 3.5, a, a + 28), 0.6) for a in (-70, 50, 170)])
    return uu(props, arcs)


def p_rollers():
    rings = uu(D(cir(-2.1, 1.3, 2.0), cir(-2.1, 1.3, 0.8)), D(cir(2.1, 1.3, 2.0), cir(2.1, 1.3, 0.8)))
    hand = uu(rc(-0.55, -3.4, 1.1, 3.6, 0.4))
    return uu(rings, hand, pg([(-1.4, -3.2), (1.4, -3.2), (0, -2.0)]))


def p_tipping():
    cab = D(rc(-4.6, -4.2, 3.8, 7.4, 0.2), rc(-3.9, -3.5, 2.4, 2.6), rc(-3.9, -0.5, 2.4, 2.6))
    cab = rot(cab, 20, -4.6, 3.2)
    return uu(cab, person(4.2, 0.3, 0.45))


@icon("mountain-lion-warning-sign", CAT, "Warning triangle with a crouching big cat in profile.",
      tags=["mountain lion", "cougar", "puma", "big cat", "wildlife warning", "predator", "trail warning"])
def _(S):
    return warn(S, p_lion(), cy=16.4, s=0.9)


@icon("stingray-warning-sign", CAT, "Warning triangle with a flat stingray seen from above, whip tail trailing.",
      tags=["stingray", "ray", "shuffle your feet", "beach warning", "sea animal", "sting", "shallow water"])
def _(S):
    return warn(S, p_stingray(), cy=16.0, s=0.92)


@icon("cassowary-warning-sign", CAT, "Warning triangle with a tall flightless bird showing a helmet-like crest.",
      tags=["cassowary", "dangerous bird", "flightless bird", "rainforest", "queensland", "wildlife warning"])
def _(S):
    return warn(S, p_cassowary(), cy=16.6, s=0.78)


@icon("scorpion-warning-sign", CAT, "Warning triangle with a scorpion from above, pincers raised and tail curled.",
      tags=["scorpion", "sting", "desert", "venomous", "arachnid", "wildlife warning"])
def _(S):
    return warn(S, p_scorpion(), cy=16.5, s=0.95)


@icon("unexploded-ordnance-sign", CAT, "Warning triangle with a finned shell half buried in the ground.",
      tags=["unexploded ordnance", "uxo", "bomb", "munitions", "do not touch", "minefield", "military hazard"])
def _(S):
    return warn(S, p_bomb(), cy=16.0, s=0.95)


@icon("jet-blast-sign", CAT, "Warning triangle with a jet engine nozzle blowing wind lines at a toppling person.",
      tags=["jet blast", "jet exhaust", "engine blast", "airport", "wind", "danger zone", "aircraft"])
def _(S):
    return warn(S, p_jet(), cy=16.2, s=0.92)


@icon("propeller-hazard-sign", CAT, "Warning triangle with a three-bladed propeller and motion arcs.",
      tags=["propeller", "spinning blades", "rotor", "aircraft hazard", "boat propeller", "danger", "keep clear"])
def _(S):
    return warn(S, p_prop(), cy=15.6, s=0.95)


@icon("counter-rotating-rollers-hazard", CAT, "Warning triangle with two rollers meeting and a finger drawn toward the gap.",
      tags=["rollers", "nip point", "pinch point", "machine hazard", "entanglement", "crush hazard", "in-running"])
def _(S):
    return warn(S, p_rollers(), cy=16.3, s=1.0)


@icon("tipping-hazard", CAT, "Warning triangle with a tall cabinet tipping forward over a small person.",
      tags=["tipping hazard", "tip over", "falling furniture", "unstable", "anchor furniture", "crush hazard"])
def _(S):
    return warn(S, p_tipping(), cy=16.2, s=0.82)


def p_cart():
    roof = rc(-3.4, -3.8, 6.8, 1.0, 0.4)
    posts = uu(stroke([(-2.6, -3.0), (-2.6, -0.4)], 0.8), stroke([(2.6, -3.0), (2.6, -0.4)], 0.8))
    body = rc(-4.8, -0.4, 9.6, 2.6, 0.9)
    seat = rc(-3.4, -1.8, 2.4, 1.6, 0.4)
    wheels = uu(cir(-2.8, 2.4, 1.35), cir(2.8, 2.4, 1.35))
    return uu(roof, posts, D(uu(body, seat), ST("M-2.8 2.4", 1, "round", "round") if False else cir(-2.8, 2.4, 1.9), cir(2.8, 2.4, 1.9)), wheels)


def p_skier():
    head = cir(0.8, -3.6, 1.0)
    body = stroke([(0.8, -2.2), (-0.2, 0.6)], 1.6)
    legs = stroke([(2.6, 1.2), (-0.2, 0.6), (-2.6, 2.0)], 1.3)
    skis = uu(stroke([(-5.4, 3.4), (-0.8, 3.4)], 0.9), stroke([(0.6, 2.6), (5.4, 2.6)], 0.9))
    poles = uu(stroke([(0.8, -1.6), (4.2, 2.4)], 0.6), stroke([(0.4, -1.4), (-3.2, 1.8)], 0.6), stroke([(0.8, -1.6), (-0.4, -0.4)], 1.2))
    return uu(head, body, legs, skis, poles)


@icon("golf-cart-crossing-sign", CAT, "Diamond sign with a side-view golf cart under a canopy roof.",
      tags=["golf cart crossing", "golf course", "buggy", "cart path", "road sign", "crossing"])
def _(S):
    return dsign(S, p_cart(), cy=12.2, s=1.0)


@icon("skier-crossing-sign", CAT, "Diamond sign with a cross-country skier striding with poles.",
      tags=["skier crossing", "ski trail", "cross-country skiing", "nordic", "winter", "road sign", "crossing"])
def _(S):
    return dsign(S, p_skier(), cy=11.6, s=1.0)


@icon("mandatory-action-sign", CAT, "Solid circle with a bold exclamation mark, the generic must-do sign.",
      tags=["mandatory", "must do", "required action", "instruction", "notice", "important", "compulsory"])
def _(S):
    if S.name == "line":
        return msign(S, uu(pg([(-1.5, -5.6), (1.5, -5.6), (0.9, 1.6), (-0.9, 1.6)]), pg([(-1.4, 3.0), (1.4, 3.0), (1.4, 5.6), (-1.4, 5.6)])), 1.0)
    return msign(S, uu(stroke([(0, -4.6), (0, 0.8)], 3.0), cir(0, 4.4, 1.55)), 1.0)


@icon("wide-load-sign", CAT, "Long banner board on a truck bumper with arrows pointing out at both ends.",
      tags=["wide load", "oversize load", "abnormal load", "truck sign", "banner board", "escort vehicle", "heavy haulage"])
def _(S):
    return [shell(rect(2.5, 4.5, 19, 8.5, min(S.R, 2))),
            detail("M6 8.75H18"), detail(poly([(8.5, 6.5), (6, 8.75), (8.5, 11)], r=S.r * 0.5)), detail(poly([(15.5, 6.5), (18, 8.75), (15.5, 11)], r=S.r * 0.5)),
            line("M7 13V17M17 13V17"), shell(rect(3.5, 17, 17, 3.5, min(S.R, 1.5)))]


@icon("cleaning-in-progress-sign", CAT, "A-frame floor stand showing a mop leaning in a bucket.",
      tags=["wet floor", "cleaning in progress", "caution", "mop", "bucket", "a-frame", "slippery"])
def _(S):
    bucket = pg([(-2.6, 0.0), (2.6, 0.0), (1.9, 4.6), (-1.9, 4.6)], r=0.3)
    mop = uu(stroke([(0.6, 0.0), (-1.2, -4.8)], 1.0), pg([(-2.6, -6.0), (-0.2, -5.0), (-0.9, -4.0), (-3.2, -4.8)]))
    return [shell(poly([(5.5, 21), (8.8, 3.5), (15.2, 3.5), (18.5, 21)], closed=True, r=S.r * 0.8)),
            mark(put(fin(S, uu(bucket, mop)), 12, 14.6, 0.95))]


@icon("event-steward", CAT, "Standing person in a loose tabard vest with a reflective band and a radio on the shoulder.",
      tags=["steward", "marshal", "event staff", "usher", "crowd control", "high visibility", "volunteer", "security"])
def _(S):
    return [shell(circle(12, 5.2, 2.3)),
            shell(poly([(7.3, 10), (10, 8.8), (14, 8.8), (16.7, 10), (15.8, 21), (8.2, 21)], closed=True, r=S.r * 0.7)),
            detail("M8 15.5H16"), detail("M10 8.8L12 11.2L14 8.8"),
            line("M7.3 10L4.8 15.5"), line("M16.7 10L19.2 15.5"),
            solid(rect(17.4, 5.2, 2.2, 3.6, 0.4)) ]


# --------------------------------------------------------------------------- instruction signs

def hand_up():
    palm = rc(-2.0, 0.0, 4.0, 3.6, 0.9)
    fingers = uu(*[rc(-2.0 + i * 1.07, -h, 0.9, h + 0.6, 0.4) for i, h in enumerate((3.2, 4.2, 3.9, 3.0))])
    thumb = stroke([(-1.6, 2.4), (-3.2, 0.6)], 0.95)
    return uu(palm, fingers, thumb)


def head_prof():
    """Head in profile facing right, centred near 0,0 (about 9 wide, 12 tall with neck)."""
    return uu(ell(-0.4, -0.8, 3.4, 3.9), rc(-2.4, 1.6, 3.0, 3.6, 0.4), pg([(2.6, -1.0), (4.3, 0.9), (2.6, 1.4)], r=0.3), ell(2.0, 2.0, 1.3, 1.0))


@icon("remove-shoes-sign", CAT, "Shoe in side view with an arrow lifting upward away from it.",
      tags=["remove shoes", "take off shoes", "shoes off", "no shoes", "entry rule", "temple", "home entrance"])
def _(S):
    return [shell(poly([(3, 20), (3, 13), (4.5, 12), (8.5, 12), (10.5, 14.5), (16, 15.5), (20, 17.5), (21, 20)], closed=True, r=S.r * 0.8)),
            detail("M3 17.5H20.5"), detail("M9 14.5L10.5 16.5"),
            line("M7 3V9"), line(poly([(4.2, 5.8), (7, 3), (9.8, 5.8)], r=S.r * 0.6))]


@icon("shower-before-swimming-sign", CAT, "Shower head spraying water beside an arrow pointing on to pool waves.",
      tags=["shower before swimming", "pool rule", "rinse off", "hygiene", "swimming pool", "wash first", "pool entry"])
def _(S):
    return [shell("M3.5 9Q3.5 3.5 8.5 3.5T13.5 9Z"), line("M8.5 3.5V2"), line("M5 12V14.5"), line("M8.5 12V15.5"), line("M12 12V14.5"),
            line("M16.5 9H21"), line(poly([(19, 6.8), (21.2, 9), (19, 11.2)], r=S.r * 0.6)),
            line("M2.5 19Q4.7 17 7 19T11.5 19T16 19T20.5 19")]


@icon("wait-behind-line-sign", CAT, "Standing person behind a dashed floor line with a raised halt hand in front.",
      tags=["wait behind line", "queue", "stand back", "privacy line", "line up", "stop here", "waiting line"])
def _(S):
    return [shell(circle(7, 4.8, 1.8)), line("M7 8V14"), line(poly([(5, 19), (7, 14), (9, 19)], r=S.r)), line("M7 9.5L10.5 12"),
            mark(put(fin(S, hand_up()), 17.2, 11.5, 1.05)),
            line("M2.5 21.2H7"), line("M10 21.2H14"), line("M17 21.2H21.5")]


@icon("keep-distance-sign", CAT, "Two standing people apart with a double-headed arrow between them at head height.",
      tags=["keep distance", "social distancing", "stay apart", "personal space", "spacing", "two metres", "queue spacing"])
def _(S):
    def fig(x):
        return [shell(circle(x, 5.5, 1.8)), line(poly([(x, 9), (x, 15)])), line(poly([(x - 1.8, 21), (x, 15), (x + 1.8, 21)], r=S.r))]
    return fig(4.5) + fig(19.5) + [line("M8.5 5.5H15.5"), line(poly([(10.5, 3.3), (8.2, 5.5), (10.5, 7.7)], r=S.r * 0.6)),
                                   line(poly([(13.5, 3.3), (15.8, 5.5), (13.5, 7.7)], r=S.r * 0.6))]


@icon("close-the-gate-sign", CAT, "Field gate with rails swinging shut beside an arrow toward the latch post.",
      tags=["close the gate", "shut gate", "livestock", "farm gate", "countryside", "keep closed", "fence gate"])
def _(S):
    return [line("M4 3V21"), line("M20.5 3V21"),
            shell(rect(7, 5.5, 10, 9, min(S.R, 1.5))), detail("M7 10H17"),
            line("M8 18.5H16.5"), line(poly([(14.2, 16.3), (16.5, 18.5), (14.2, 20.7)], r=S.r * 0.6))]


@icon("apply-sunscreen-sign", CAT, "Squeeze bottle dispensing a dollop of cream onto an open palm under a small sun.",
      tags=["apply sunscreen", "sun cream", "sunblock", "spf", "skin protection", "uv protection", "lotion"])
def _(S):
    return [shell(rect(3.5, 3, 7, 9, min(S.R, 2))), shell(rect(5.7, 12, 2.6, 3, 0.4)), dot(7, 18, 1.5),
            line("M2.5 21H13"),
            shell(circle(18, 6.5, 2.2)), line("M18 1.8V2.8"), line("M18 10.2V11.2"), line("M13.3 6.5H14.3"), line("M21.7 6.5H22.7")]


@icon("take-a-number", CAT, "Wall ticket dispenser with a numbered paper ticket sticking out of its slot.",
      tags=["take a number", "ticket dispenser", "queue ticket", "deli counter", "waiting line", "number system", "turn"])
def _(S):
    return [shell(rect(4, 3, 16, 8, min(S.R, 2.5))), dot(12, 6.6, 1.2), detail("M7 9H17"),
            shell(rect(8.5, 12.5, 7, 8.5, 0.6 if S.name == "line" else 1.5)), detail("M12 15V19"), detail("M10.6 16.2L12 15")]


@icon("hold-childs-hand-sign", CAT, "Adult holding a small child's hand while both stand on escalator steps.",
      tags=["hold child's hand", "escalator safety", "supervise children", "parent and child", "keep hold", "kids", "stairs"])
def _(S):
    return [shell(circle(6, 4.6, 1.8)), line("M6 8V13.5"), line(poly([(4.2, 20), (6, 13.5), (8, 20)], r=S.r)),
            line(poly([(6, 9.5), (11, 12), (15.5, 12)], r=S.r * 0.6)),
            shell(circle(16.5, 8.8, 1.3)), line("M16.5 11V15.5"), line(poly([(15.3, 18), (16.5, 15.5), (18, 18)], r=S.r * 0.4)),
            line(poly([(2, 21.5), (9.8, 21.5), (9.8, 19.2), (22, 19.2)], r=S.r * 0.3))]


@icon("fold-stroller-sign", CAT, "Stroller collapsed into a narrow shape with a curved folding arrow beside it.",
      tags=["fold stroller", "collapse pushchair", "buggy", "pram", "escalator rule", "bus rule", "folded"])
def _(S):
    return [line("M4 4H9.5"), shell(rect(6.5, 6, 5, 10, min(S.R, 2.2))), dot(7.5, 19.2, 1.5), dot(12, 19.2, 1.5),
            line("M15.5 7.5Q20.5 9.5 18.5 15"), line(poly([(16.8, 14.5), (18.7, 15.8), (19.8, 13.6)], r=S.r * 0.5))]


@icon("stay-on-trail-sign", CAT, "Walking figure on a path between two border lines with tufts of vegetation either side.",
      tags=["stay on trail", "stay on path", "keep to the path", "hiking", "protect habitat", "nature reserve", "footpath"])
def _(S):
    return [line("M6 21.5L10.5 3"), line("M18 21.5L13.5 3"),
            mark(put(fin(S, person(0, 0, 0.62)), 12, 12.8, 1.0)),
            line(poly([(2, 18), (3, 14.5), (4, 18)])), line("M3 18V14"), line(poly([(20, 14), (21, 10.5), (22, 14)])), line("M21 14V10")]


@icon("extinguish-campfire-sign", CAT, "Bucket tipping water over a small campfire with steam rising.",
      tags=["extinguish campfire", "put out fire", "douse fire", "camping", "fire safety", "water bucket", "bonfire"])
def _(S):
    def rpts(pts, deg, cx, cy):
        a = math.radians(deg)
        return [(cx + (x - cx) * math.cos(a) - (y - cy) * math.sin(a), cy + (x - cx) * math.sin(a) + (y - cy) * math.cos(a)) for x, y in pts]
    bucket = rpts([(3.5, 3), (10.5, 3), (9.5, 10), (4.5, 10)], -38, 7, 6.5)
    return [shell(poly(bucket, closed=True, r=S.r * 0.6)),
            line("M14 7.5V9.5"), line("M17 6.5V9.5") if False else line("M12.5 11V13"),
            shell("M15.5 21.5Q10.5 21.5 10.5 17.5Q10.5 14.5 13.5 12.5Q14 15 15.5 15Q16 12.5 18 10.5Q21.5 13.5 21.5 17.5Q21.5 21.5 15.5 21.5Z"),
            line("M4 20Q5.5 18.5 4.5 17")]


def cap_head(mod):
    h = head_prof()
    return mod(h)


@icon("wear-swim-cap-sign", CAT, "Solid circle with a head in profile covered by a smooth swim cap.",
      tags=["wear swim cap", "swimming cap", "pool rule", "hair cover", "hygiene", "mandatory", "bathing cap"])
def _(S):
    h = fin(S, head_prof(), 1.0)
    edge = pth("M3.4 -2.2Q-0.6 -0.2 -3.8 1.6", 0.6)
    return msign(S, D(h, edge), 0.82)


@icon("wear-hairnet-sign", CAT, "Solid circle with a head in profile whose hair is gathered under a mesh net.",
      tags=["wear hairnet", "hair net", "food hygiene", "kitchen rule", "factory rule", "mandatory", "hair cover"])
def _(S):
    h = fin(S, head_prof(), 1.0)
    holes = [cir(x, y, 0.5) for x, y in ((-3.0, -2.0), (-1.6, -3.0), (0.0, -3.4), (1.4, -2.9), (-2.4, -0.6), (-0.9, -1.4), (0.6, -1.6), (-3.0, 0.4), (-1.5, 0.2))]
    return msign(S, D(h, *holes), 0.82)


@icon("wear-shoe-covers-sign", CAT, "Solid circle with a shoe wrapped in a baggy disposable cover.",
      tags=["wear shoe covers", "overshoes", "booties", "clean room", "hygiene", "mandatory", "shoe protectors"])
def _(S):
    sh = pg([(-5.2, 3.6), (-5.2, -0.6), (-3.8, -4.4), (-1.0, -4.4), (-0.4, -1.4), (1.8, -0.2), (4.2, 0.8), (5.6, 2.2), (5.6, 3.6)])
    band = pth("M-4.6 -1.9Q-2.6 -2.9 -0.4 -2.5", 0.55)
    sole = stroke([(-5.0, 2.5), (5.0, 2.5)], 0.55)
    return msign(S, D(fin(S, sh, 1.1), band, sole), 0.95)


@icon("wear-apron-sign", CAT, "Solid circle with a torso wearing a full-length bib apron on a neck strap.",
      tags=["wear apron", "protective apron", "kitchen rule", "lab safety", "workshop", "mandatory", "bib apron"])
def _(S):
    ap = pg([(-2.6, -3.4), (2.6, -3.4), (2.6, -1.0), (4.4, -0.4), (4.0, 5.6), (-4.0, 5.6), (-4.4, -0.4), (-2.6, -1.0)])
    strap = D(cir(0, -4.4, 2.8), cir(0, -4.4, 1.9), rc(-4, -4.4, 8, 6))
    pocket = ST(poly([(-2.2, 1.8), (-2.2, 4.0), (2.2, 4.0), (2.2, 1.8)]), 0.5, "butt", "miter")
    return msign(S, uu(D(fin(S, ap, 1.2), pocket), strap), 0.95)


@icon("wear-bike-helmet-sign", CAT, "Solid circle with a head in profile wearing a vented bicycle helmet with a chin strap.",
      tags=["wear bike helmet", "cycle helmet", "bicycle safety", "head protection", "mandatory", "cycling", "helmet required"])
def _(S):
    h = fin(S, head_prof(), 1.0)
    vents = uu(*[pth(f"M{x} -3.6L{x - 1.2} -1.6", 0.55) for x in (-2.0, -0.6, 0.8, 2.0)])
    rim = pth("M-3.8 -0.4Q0 -0.9 3.5 -1.6", 0.55)
    strap = pth("M0.6 -0.9L0.8 2.6", 0.5)
    return msign(S, D(h, vents, rim, strap), 0.82)


@icon("use-barrier-cream-sign", CAT, "Solid circle with a tube squeezing cream onto the back of a hand.",
      tags=["barrier cream", "hand cream", "skin protection", "workplace", "dermatitis", "mandatory", "apply cream"])
def _(S):
    tube = rot(uu(pg([(-1.6, -6.0), (1.6, -6.0), (1.1, -1.0), (-1.1, -1.0)], r=0.3), rc(-0.7, -1.0, 1.4, 1.2)), 28, 0, 0)
    tube = transform_path(tube, (1, 0, 0, 1, -2.4, 0.2))
    cream = uu(pth("M-3.0 3.0Q-1.6 2.0 -0.4 3.0T2.2 3.0", 1.0), cir(-3.0, 3.0, 0.6))
    hand = uu(rc(-5.0, 4.0, 8.0, 3.2, 1.2), rc(2.2, 4.4, 3.0, 2.4, 1.0))
    return msign(S, uu(fin(S, tube, 0.6), cream, fin(S, hand, 0.9)), 0.85)


@icon("modest-dress-sign", CAT, "Standing person in a long-sleeved top and ankle-length skirt with shoulders and knees covered.",
      tags=["modest dress", "dress code", "cover shoulders", "cover knees", "temple dress", "respectful clothing", "long skirt"])
def _(S):
    return [shell(circle(12, 4.5, 2.2)),
            shell(poly([(9.2, 8.5), (11, 7.5), (13, 7.5), (14.8, 8.5), (17.5, 15.5), (15.6, 16), (14.2, 12.5), (16.5, 21), (7.5, 21), (9.8, 12.5), (8.4, 16), (6.5, 15.5)], closed=True, r=S.r * 0.6)),
            detail("M10 12.5H14")]


@icon("head-covering-sign", CAT, "Head in profile with a scarf draped over the hair and falling past the neck.",
      tags=["head covering", "headscarf", "hijab", "head scarf", "dress code", "religious site", "scarf"])
def _(S):
    return [shell("M5 21Q3.5 9 11 4.5Q18.5 3 19.5 10Q19.8 14 17.5 17L19 21Z"),
            detail("M13 9Q16.5 9.5 16.5 12.5L15.2 14Q16 15.2 14.4 16"), detail("M5.5 17Q10 19 15 18")]


@icon("knock-before-entering-sign", CAT, "Closed fist knocking on a door panel with small impact marks.",
      tags=["knock before entering", "knock first", "please knock", "door", "privacy", "office rule", "enter"])
def _(S):
    return [shell(rect(12, 3, 9, 18, min(S.R, 1.5))), detail("M14.5 7H18.5"), detail("M14.5 11H18.5"), dot(14.2, 15.5, 0.9),
            shell(rect(2.5, 9.5, 5.5, 6, 2 if S.name == "line" else 2.6)), detail("M2.5 12.5H8"),
            line("M9.4 8.6L10.4 7.2"), line("M9.8 12.6H10.9"), line("M9.4 16.5L10.4 17.9")]


@icon("return-trays-sign", CAT, "Food tray with a plate being slid toward the shelves of a rack, arrow showing the direction.",
      tags=["return trays", "clear your tray", "tray return", "cafeteria", "canteen", "food court", "tidy up"])
def _(S):
    return [line("M20.5 3V21"), line("M14.5 7H20.5"), line("M14.5 13H20.5"), line("M14.5 19H20.5"),
            shell(rect(3, 13, 9.5, 2.4, 0.6)), shell("M5.5 13Q7.75 8.5 10 13"),
            line("M3 19.5H11"), line(poly([(9, 17.5), (11.2, 19.5), (9, 21.5)], r=S.r * 0.5))]


@icon("carry-dog-on-escalator-sign", CAT, "Person on escalator steps holding a small dog in their arms.",
      tags=["carry dogs", "pets on escalator", "escalator safety", "dog rule", "animal rule", "mall", "station"])
def _(S):
    dog = uu(ell(0, 0.4, 3.0, 1.6), cir(3.2, -1.4, 1.35), pg([(3.6, -2.4), (3.9, -3.6), (4.7, -2.3)]), rc(-2.3, 1.4, 1.0, 2.0, 0.3), rc(1.6, 1.4, 1.0, 2.0, 0.3),
             stroke([(-2.8, -0.2), (-4.0, -1.8)], 0.9))
    return [shell(circle(6, 4.6, 1.8)), line("M6 8V14"), line(poly([(4.2, 20), (6, 14), (8, 20)], r=S.r)),
            line(poly([(6, 9.5), (9, 12.5), (12, 12.5)], r=S.r * 0.6)),
            mark(put(fin(S, dog), 16.2, 11.4, 1.0)),
            line(poly([(2, 21.5), (9.8, 21.5), (9.8, 19.2), (22, 19.2)], r=S.r * 0.3))]


@icon("let-passengers-off-sign", CAT, "Train doorway with one arrow leaving it first and a second arrow waiting to enter from the side.",
      tags=["let passengers off", "let people off first", "boarding", "train etiquette", "alight first", "platform", "doorway"])
def _(S):
    return [line("M7.5 3V16.5"), line("M16.5 3V16.5"),
            line("M12 4.5V15.5"), line(poly([(9.2, 12.8), (12, 15.6), (14.8, 12.8)], r=S.r * 0.6)),
            line("M2.5 20.5H9"), line(poly([(7, 18.5), (9.2, 20.5), (7, 22.5)], r=S.r * 0.5))]


@icon("remove-laptop-sign", CAT, "Open laptop lifted above a shallow screening tray.",
      tags=["remove laptop", "security screening", "airport security", "take out laptop", "tray", "x-ray", "checkpoint"])
def _(S):
    return [shell(rect(6.5, 2.5, 11, 7.5, min(S.R, 1.5))), line("M4 12.5H20"),
            shell(poly([(3, 15.5), (21, 15.5), (19.5, 21), (4.5, 21)], closed=True, r=S.r * 0.6))]


@icon("empty-pockets-sign", CAT, "Trouser pocket tipping coins and keys down into a small tray.",
      tags=["empty pockets", "security screening", "coins", "keys", "metal detector", "checkpoint", "tray"])
def _(S):
    return [shell(poly([(3, 3), (14, 3), (14, 11), (8.5, 14), (3, 11)], closed=True, r=S.r * 0.7)), detail("M3 6.5H14"),
            shell(circle(18, 5.5, 1.7)), shell(circle(19.5, 10.7, 1.7)), dot(15.2, 8.5, 1.0),
            shell(poly([(4, 17), (20, 17), (18.5, 21.5), (5.5, 21.5)], closed=True, r=S.r * 0.5))]


@icon("cigarette-bin", CAT, "Slim post bin with a perforated top plate and a stubbed cigarette resting on it.",
      tags=["cigarette bin", "butt bin", "smoking area", "stub out", "ashtray post", "litter", "outdoor ashtray"])
def _(S):
    return [shell(poly([(5.5, 9), (18.5, 9), (18.5, 13), (15, 13), (15, 21), (9, 21), (9, 13), (5.5, 13)], closed=True, r=S.r * 0.6)),
            dot(9, 11, 0.6), dot(12, 11, 0.6), dot(15, 11, 0.6),
            line("M5 5.5H13.5"), dot(16.2, 5.5, 1.1)]


@icon("baggage-drop", CAT, "Suitcase riding a short conveyor belt toward a hatch in a counter.",
      tags=["baggage drop", "bag drop", "luggage check-in", "airport", "check in baggage", "conveyor", "counter"])
def _(S):
    return [shell(rect(14.5, 3.5, 6.5, 13.5, min(S.R, 3))), detail("M14.5 9.5H21"),
            shell(rect(3, 10.5, 9, 6.5, min(S.R, 3))), line(poly([(6, 10.5), (6, 8.3), (9, 8.3), (9, 10.5)], r=S.r * 0.4)),
            shell(rect(2, 17, 18, 3.5, min(S.R, 1.75))), dot(6, 18.75, 0.6), dot(11, 18.75, 0.6), dot(16, 18.75, 0.6)]
