"""TypeIcon Core: sea life (batch sea_life_001).

Fish, eels, sharks, rays and other sea creatures, drawn from the animals themselves. Side views face left
(head on the left, tail on the right), matching the fish and shark in animals.py.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, solid  # noqa: F401
from dsl import shell as _shell
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "sea-life"


# --------------------------------------------------------------------------- local helpers

def shell(d, **attrs):
    """Shell with a low miter limit, so the acute fin and tail tips bevel instead of spiking out in Line."""
    attrs.setdefault("stroke_miterlimit", "2.5")
    return _shell(d, **attrs)


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx, cy):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def thick(d, w, S):
    """Outline of a stroke of width w along d."""
    return path_to_d(ST(d, w, S.cap, S.join))


def f(v):
    return fmt(round(v, 2))


def _p(p):
    return f"{f(p[0])} {f(p[1])}"


def tip(a, p, b, r):
    """Corner at p (coming from a, leaving towards b): sharp when r == 0, softened with a quadratic when r > 0."""
    if r <= 0:
        return "L" + _p(p)
    la = math.hypot(a[0] - p[0], a[1] - p[1])
    lb = math.hypot(b[0] - p[0], b[1] - p[1])
    t = min(r, la / 2, lb / 2)
    s = (p[0] + (a[0] - p[0]) * t / la, p[1] + (a[1] - p[1]) * t / la)
    e = (p[0] + (b[0] - p[0]) * t / lb, p[1] + (b[1] - p[1]) * t / lb)
    return "L" + _p(s) + "Q" + _p(p) + " " + _p(e)


def pt(c, r, deg):
    return (c[0] + r * math.cos(math.radians(deg)), c[1] + r * math.sin(math.radians(deg)))


def mark(d):
    """Small solid mark: solid in stroke styles, knocked out of a Filled body."""
    return Part("dot", d)


def body(x0, x1, cy, up, dn, j=1.3, peak=0.42, blunt=0.6, lean=0.15):
    """Fish body from the nose (x0, cy) to the tail joint at x1 (half height j), top at cy - up, belly at cy + dn."""
    xm = x0 + (x1 - x0) * peak
    a = (xm - x0) * (1 - lean)
    b = (x1 - xm) * 0.5
    c0 = x0 + (xm - x0) * lean
    return (f"M{f(x0)} {f(cy)}C{f(c0)} {f(cy - up * blunt)} {f(xm - a * 0.45)} {f(cy - up)} {f(xm)} {f(cy - up)}"
            f"C{f(xm + b)} {f(cy - up)} {f(x1 - b * 0.4)} {f(cy - j - (up - j) * 0.35)} {f(x1)} {f(cy - j)}"
            f"L{f(x1)} {f(cy + j)}"
            f"C{f(x1 - b * 0.4)} {f(cy + j + (dn - j) * 0.35)} {f(xm + b)} {f(cy + dn)} {f(xm)} {f(cy + dn)}"
            f"C{f(xm - a * 0.45)} {f(cy + dn)} {f(c0)} {f(cy + dn * blunt)} {f(x0)} {f(cy)}Z")


def fork(S, x, cy, j, ln, s, notch=0.55, r=None):
    """Forked tail: joint at x (half height j), lobes reach x + ln at cy -/+ s, notch at x + ln * notch."""
    r = L(S, 0, 1) if r is None else r
    return poly([(x - 1.5, cy - j), (x + ln, cy - s), (x + ln * notch, cy), (x + ln, cy + s), (x - 1.5, cy + j)], closed=True, r=r)


def fan(S, x, cy, j, ln, s):
    """Rounded fan tail."""
    r = L(S, 0, 1)
    a, b = (x - 1.5, cy - j), (x + ln - 0.8, cy - s)
    c, d = (x + ln - 0.8, cy + s), (x - 1.5, cy + j)
    return (f"M{_p(a)}" + tip(a, b, c, r) + f"C{f(x + ln + 0.7)} {f(cy - s * 0.5)} {f(x + ln + 0.7)} {f(cy + s * 0.5)} {_p(c)}"
            + tip(b, c, d, r) + f"L{_p(d)}Z")


def fin(S, pts, r=None):
    return poly(pts, closed=True, r=L(S, 0, 0.8) if r is None else r)


def tube(fn, width, n=28):
    """Closed outline around a centreline fn(t) -> (x, y), width(t) in px."""
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        x, y = fn(t)
        x2, y2 = fn(min(1, t + 1e-3))
        x1, y1 = fn(max(0, t - 1e-3))
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy)
        nx, ny = -dy / ln, dx / ln
        w = width(t) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return left + right[::-1]


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def bolt(x, y, s=1.0):
    """Small lightning bolt with its top at (x, y)."""
    pts = [(0, 0), (-3.2, 5), (-0.6, 5), (-2, 9), (2.6, 3.4), (0, 3.4), (1.6, 0)]
    return [(x + px * s, y + py * s) for px, py in pts]


def water(x0, x1, y, a=1.2, waves=3):
    """Wavy water line."""
    w = (x1 - x0) / waves
    d = f"M{f(x0)} {f(y)}"
    for i in range(waves):
        xa = x0 + i * w
        d += f"C{f(xa + w * 0.25)} {f(y - a)} {f(xa + w * 0.25)} {f(y - a)} {f(xa + w * 0.5)} {f(y)}"
        d += f"C{f(xa + w * 0.75)} {f(y + a)} {f(xa + w * 0.75)} {f(y + a)} {f(xa + w)} {f(y)}"
    return d


# --------------------------------------------------------------------------- reef and bony fish

@icon("clownfish", CAT, "Plump fish with three bold bands across its head, middle and tail",
      tags=["anemonefish", "reef fish", "tropical fish", "aquarium", "coral reef", "ocean"])
def _(S):
    b = body(2.5, 17, 12, 6, 6, j=2, peak=0.45, blunt=0.75)
    t = fan(S, 17, 12, 2, 4.5, 4.8)
    return [shell(union(b, t)), detail("M8.2 6.9C7 10 7 14 8.2 17.1"), detail("M13 6.4C12 10 12 14 13 17.6"),
            detail("M17 9.8V14.2"), dot(5.2, 10.6, 1.1)]


@icon("angelfish", CAT, "Tall triangular fish with long swept back fins above and below",
      tags=["freshwater angelfish", "aquarium", "tropical fish", "cichlid", "reef fish"])
def _(S):
    r = L(S, 0, 1.2)
    pts = [(3, 12), (8.5, 7.3), (15.5, 2.5), (14.5, 9.3), (17.2, 11), (21, 8.3), (21, 15.7), (17.2, 13), (14.5, 14.7),
           (15.5, 21.5), (8.5, 16.7)]
    return [shell(poly(pts, closed=True, r=r)), detail("M10.5 6.7V17.3"), dot(6.3, 11.3, 1.1)]


@icon("pufferfish", CAT, "Round inflated fish covered in short spikes with pouting lips",
      tags=["blowfish", "puffer", "fugu", "globefish", "spiky fish", "ocean"])
def _(S):
    c = (11.5, 12.5)
    parts = [circle(c[0], c[1], 6.5), circle(4.8, 13.3, 1.5)]
    rr = L(S, 0, 0.3)
    for a in (-150, -118, -86, -54, -22, 34, 66, 98, 130):
        parts.append(poly([pt(c, 6, a - 12), pt(c, 8.8, a), pt(c, 6, a + 12)], closed=True, r=rr))
    parts.append(fin(S, [(17, 11.2), (21.3, 9), (21.3, 16), (17, 13.8)]))
    return [shell(union(*parts)), dot(9, 10.8, 1.2), detail("M12.5 13.5C14 14 14.8 15.2 14.8 16.5")]


@icon("swordfish", CAT, "Sleek fish with a long flat sword bill and a crescent tail",
      tags=["broadbill", "billfish", "marlin", "game fish", "deep sea fishing", "ocean"])
def _(S):
    b = body(6.5, 16.5, 12.5, 4, 3.6, j=1.1, peak=0.33, blunt=0.55, lean=0.1)
    d = fin(S, [(9, 9.2), (10.6, 4.6), (13, 9)])
    t = poly([(15.5, 11.4), (20.8, 6.2), (19.5, 12.5), (20.8, 18.8), (15.5, 13.6)], closed=True, r=L(S, 0, 1))
    return [shell(union(b, d, t)), line(seg(2, 11.9, 7, 11.9)), dot(9, 11.4, 1), detail("M10.5 14.2C11.8 15.2 13 15.5 14.2 15.4")]


@icon("sailfish", CAT, "Billed fish with a huge sail shaped fin along its back",
      tags=["billfish", "sail", "marlin", "game fish", "fast fish", "ocean"])
def _(S):
    r = L(S, 0, 1)
    b = body(6.5, 16.5, 16, 3, 2.8, j=1, peak=0.33, blunt=0.55, lean=0.1)
    sail = "M8.3 14C8.3 8.5 9.3 4 11 2.8C13.5 5 16 9.5 16.8 14.6Z"
    t = poly([(15.5, 15), (20.8, 11.2), (19.6, 16), (20.8, 20.8), (15.5, 17)], closed=True, r=r)
    return [shell(union(b, sail, t)), line(seg(2, 15.5, 7, 15.5)), detail("M11.2 13.6L11.2 7"), dot(8.9, 15.3, 0.95)]


@icon("seahorse", CAT, "Upright seahorse with a tube snout and a tail curled into a spiral",
      tags=["sea horse", "hippocampus", "marine", "ocean", "aquarium", "coral reef"])
def _(S):
    head = ellipse(12.5, 5.6, 3.2, 2.7)
    crown = fin(S, [(12, 3.4), (13.3, 1.8), (14.4, 3.4)], r=L(S, 0, 0.4))
    trunk = "M11 7.5C8.3 9.5 8.2 14.5 11.5 16.8L14.8 16.3C17 13.5 17 9.5 15 7.2Z"
    dfin = fin(S, [(16, 9.8), (18.8, 11.4), (16, 13.5)])
    return [shell(union(head, crown, trunk, dfin)), line("M10.2 6.3L5 7.5"),
            line("M13.3 16.3C13.8 19.3 13 21 11 21C9.2 21 8.5 19.2 10 18.5"), dot(13, 5.4, 0.95)]


@icon("moray-eel", CAT, "Eel head with an open jaw leaning out of a hole in a rock",
      tags=["moray", "eel", "reef", "rock", "ocean", "marine"])
def _(S):
    rock = "M8.5 21.5C8.5 17 10.8 13.5 15 13.5C19 13.5 21.5 17 21.5 21.5Z"
    neck = thick("M14.6 17.5C14 12.5 11.5 8.5 7.5 8", 4.4, S)
    head = ellipse(6.8, 8, 3.8, 3.2)
    jaw = poly([(2, 6.4), (7.2, 8.4), (2, 10.8)], closed=True)
    return [shell(minus(union(rock, neck, head), jaw)), detail("M12 19.6C13.5 18.2 15.8 18.2 17.2 19.6"), dot(7.6, 6.4, 0.95)]


@icon("electric-eel", CAT, "Long wavy eel with a small lightning bolt above it",
      tags=["eel", "electricity", "shock", "voltage", "river fish", "amazon"])
def _(S):
    def c(t):
        return (4.2 + 16.3 * t, 16.8 - 2.6 * math.sin(t * 2 * math.pi))

    def w(t):
        return 4 - 3.2 * t
    b = poly(tube(c, w, 36), closed=True, r=0)
    head = ellipse(4.3, 16.8, 2.5, 2.1)
    snout = fin(S, [(1.9, 17.2), (4, 15), (4, 18.6)], r=0) if S.name == "line" else circle(3, 16.8, 1)
    return [shell(union(b, head, snout)), shell(poly(bolt(14.5, 2.5, 0.95), closed=True, r=L(S, 0, 0.5))), dot(4.6, 16.1, 0.8)]


@icon("garden-eel", CAT, "Three thin eels poking up out of the sandy seabed",
      tags=["eels", "seabed", "sand", "burrow", "reef", "ocean"])
def _(S):
    parts = [line(water(2, 22, 20, 0.8, 2))]
    for x, top, s in ((5.5, 9, 1), (12, 5.5, 1), (18.5, 10, -1)):
        parts.append(line(f"M{f(x)} 19V{f(top + 2.5)}C{f(x)} {f(top)} {f(x + 0.8 * s)} {f(top - 0.5)} {f(x + 2.6 * s)} {f(top - 0.5)}"))
        parts.append(dot(x + 2.6 * s, top - 0.5, 1.4))
    return parts


@icon("gulper-eel", CAT, "Deep sea eel with an enormous pouch mouth and a thin whip tail",
      tags=["pelican eel", "deep sea", "abyss", "eel", "ocean"])
def _(S):
    pouch = "M3 9C3 15 6 18.5 10 16.5L13.5 13C14.5 11.5 14 10 12.5 9.8Z"
    return [shell(pouch), line(poly([(13, 8.5), (3, 4)], r=S.r)), line("M13.8 12.3C17 13.5 18 17 20.5 20.5"), dot(12, 11.8, 0.9)]


@icon("eel", CAT, "Long snake like fish in a gentle S curve with a small fin behind its head",
      tags=["freshwater eel", "conger", "unagi", "slippery", "fish", "ocean"])
def _(S):
    def c(t):
        return (4 + 16.8 * t, 12 + 3.8 * math.sin(t * 2 * math.pi))

    def w(t):
        return 4.4 - 3.6 * t
    b = poly(tube(c, w, 40), closed=True, r=0)
    head = ellipse(4, 12, 2.6, 2.3)
    snout = fin(S, [(1.8, 12.4), (4, 9.9), (4, 14)], r=0) if S.name == "line" else circle(2.6, 12.1, 1.2)
    pec = fin(S, [(7.2, 14.6), (8, 18.6), (9.6, 15.2)])
    return [shell(union(b, head, snout, pec)), dot(4.3, 11.2, 0.85), detail("M6.8 10L6.8 14")]


@icon("anglerfish", CAT, "Round deep sea fish with a toothy mouth and a glowing lure on a stalk",
      tags=["angler", "monkfish", "deep sea", "lure", "abyss", "ocean"])
def _(S):
    b = circle(12.5, 14, 6.8)
    t = fin(S, [(18, 12.3), (21.5, 9.8), (21.5, 18.2), (18, 15.7)])
    return [shell(union(b, t)), detail("M5.8 13.2L7.5 15.7L9.2 13.2L10.9 15.7L12.6 13.2"),
            line("M11.5 7.3C11 4 8.5 2.7 5.8 3.8"), dot(4.8, 5, 1.6), dot(13.4, 10.6, 1.1)]


@icon("viperfish", CAT, "Slender deep sea fish with an open jaw and long needle fangs",
      tags=["deep sea", "fangs", "abyss", "predator", "ocean"])
def _(S):
    b = body(3, 16.5, 11.5, 3.6, 3.6, j=1, peak=0.35, blunt=0.7)
    t = fork(S, 16.5, 11.5, 1, 4.5, 4)
    mouth = poly([(1, 9.2), (8, 11.5), (1, 13.8)], closed=True)
    r = L(S, 0, 0.4)
    fangs = [fin(S, [(3.2, 9.5), (5.4, 16.8), (5.3, 9.6)], r=r), fin(S, [(3.4, 13.4), (6.8, 6), (5.6, 13.2)], r=r)]
    return [shell(union(minus(union(b, t), mouth), *fangs)), dot(7.4, 9.3, 1.1)]


@icon("barracuda", CAT, "Long torpedo shaped fish with a pointed jutting lower jaw and a forked tail",
      tags=["predator", "game fish", "teeth", "reef", "ocean"])
def _(S):
    r = L(S, 0, 0.8)
    b = ("M3.6 11.8C6 10.2 8.5 9.3 11 9.3C13.5 9.3 15.5 10 17 11L17 13C15.5 14 13.5 14.8 11 14.8C8 14.8 5.8 14.4 4.2 13.9"
         + tip((4.2, 13.9), (2.6, 13), (3.6, 11.8), r) + "Z")
    d1 = fin(S, [(8.5, 9.8), (9.8, 7.2), (11.2, 9.4)])
    d2 = fin(S, [(13, 10), (14, 8.2), (15, 10.4)])
    t = fork(S, 16.8, 12, 1, 4.8, 4.2, notch=0.45)
    return [shell(union(b, d1, d2, t)), detail("M4.2 12.8L7.8 12.6"), dot(6.4, 11.1, 0.9)]


@icon("tuna", CAT, "Thick torpedo shaped fish with small finlets and a sickle tail",
      tags=["bluefin", "tuna fish", "seafood", "sushi", "fishing", "ocean"])
def _(S):
    b = body(2.5, 16, 12, 4.5, 4, j=1.2, peak=0.4, blunt=0.55)
    d = fin(S, [(7.8, 8.2), (9.5, 4.6), (11.5, 7.8)])
    t = poly([(15.5, 11), (20.3, 4.2), (19, 12), (20.3, 19.8), (15.5, 13)], closed=True, r=L(S, 0, 1))
    lets = []
    for x in (12.2, 14.2):
        lets.append(fin(S, [(x - 0.9, 9.4), (x + 0.8, 7.6), (x + 0.9, 9.6)], r=L(S, 0, 0.3)))
        lets.append(fin(S, [(x - 0.9, 14.8), (x + 0.8, 16.4), (x + 0.9, 14.4)], r=L(S, 0, 0.3)))
    return [shell(union(b, d, t, *lets)), dot(5.5, 11, 1.1), detail("M8.5 13.3C9.8 14.3 11 14.5 12.3 14.2")]


@icon("salmon", CAT, "Fish leaping in an arc above a wavy water line",
      tags=["leaping fish", "river", "spawning", "seafood", "fishing", "wild salmon"])
def _(S):
    ctrl = ((3.5, 13.5), (5.5, 5.5), (13.5, 3.8), (17.5, 11))

    def w(t):
        if t < 0.1:
            return 2.6 + t * 20
        if t < 0.45:
            return 4.6
        return 4.6 - (t - 0.45) / 0.55 * 3.4
    b = poly(tube(lambda t: bez(*ctrl, t), w, 30), closed=True, r=0)
    head = circle(4.3, 12.2, 2.2)
    e = bez(*ctrl, 1)
    tl = fin(S, [(e[0] - 1.2, e[1] - 0.6), (e[0] - 1.3, e[1] + 4.6), (e[0] + 0.6, e[1] + 2.4), (e[0] + 3.4, e[1] + 3.2), (e[0] + 0.8, e[1] - 1.4)])
    df = fin(S, [(9.5, 5.3), (11.5, 2.4), (12.8, 5)])
    return [shell(union(b, head, tl, df)), line(water(2, 22, 20, 1, 3)), dot(5.6, 10.2, 0.9)]


@icon("mackerel", CAT, "Streamlined fish with wavy stripes along its back and a deeply forked tail",
      tags=["fish", "seafood", "oily fish", "fishing", "atlantic mackerel", "ocean"])
def _(S):
    b = body(2.5, 16, 12.5, 4, 3.4, j=1, peak=0.42, blunt=0.5)
    d = fin(S, [(8, 9), (9.5, 6.3), (11, 8.6)])
    t = fork(S, 16, 12.5, 1, 5.5, 5, notch=0.35)
    return [shell(union(b, d, t)), detail("M10.2 9.1C11.2 10 10.2 11 11.3 12"), detail("M13.3 9.8C14.3 10.6 13.4 11.4 14.2 12.2"),
            dot(5.5, 11.5, 1)]


@icon("cod-fish", CAT, "Heavy fish with three dorsal fins, a lateral line and a chin barbel",
      tags=["cod", "atlantic cod", "whitefish", "fish and chips", "seafood", "fishing"])
def _(S):
    r = L(S, 0, 1)
    b = body(3, 16.5, 12, 4.2, 3.8, j=1.5, peak=0.4, blunt=0.6)
    fins = [fin(S, [(5.2, 9), (6.6, 5.6), (8.2, 8.3)], r=r), fin(S, [(9.4, 7.9), (10.9, 4.8), (12.4, 8)], r=r),
            fin(S, [(13.3, 8.8), (14.6, 6.4), (15.8, 10)], r=r)]
    t = poly([(15.5, 10.5), (21, 7.5), (21, 16.5), (15.5, 13.5)], closed=True, r=r)
    return [shell(union(b, *fins, t)), line("M4.5 15.2L4 18.8"), detail("M8 12.8C11 11.5 13 11.5 15.5 12.2"), dot(6, 10.8, 1)]


@icon("catfish", CAT, "Flat headed fish with long whiskers drooping from its wide mouth",
      tags=["fish", "whiskers", "barbels", "river", "freshwater", "fishing"])
def _(S):
    b = body(6.5, 17.5, 13, 3.8, 3, j=1.3, peak=0.3, blunt=0.9, lean=0)
    d = fin(S, [(10, 10), (11.5, 7.2), (12.8, 9.8)])
    t = fan(S, 17.5, 13, 1.3, 4, 3.8)
    return [shell(union(b, d, t)), line("M6.8 11.8C4.5 11.2 3 9.5 2.7 6.5"), line("M6.8 14.2C4.5 15 3.2 17 3 20"),
            dot(8.8, 11.6, 1)]


@icon("koi", CAT, "Carp seen from above with swept back fins, a flowing tail and a spot on its head",
      tags=["koi carp", "carp", "pond fish", "japanese", "garden pond", "luck"])
def _(S):
    ctrl = ((12, 3.5), (12.5, 9), (10.5, 13), (12.5, 17.5))

    def w(t):
        if t < 0.1:
            return 5 + t * 14
        if t < 0.3:
            return 6.4
        return 6.4 - (t - 0.3) / 0.7 * 4.6
    b = poly(tube(lambda t: bez(*ctrl, t), w, 30), closed=True, r=0)
    head = ellipse(12, 5.3, 3.3, 3)
    rr = L(S, 0, 1)
    fins = [fin(S, [(9.6, 7.8), (6, 12.2), (9.2, 11.6)], r=rr), fin(S, [(14.4, 8), (18, 12.4), (14.6, 11.4)], r=rr)]
    tl = fin(S, [(13.3, 16.8), (16.4, 21.6), (12.6, 19.8), (8.8, 21.4), (11.6, 16.8)], r=L(S, 0, 1))
    return [shell(union(b, head, *fins, tl)), dot(12, 5.6, 1.5)]


@icon("betta-fish", CAT, "Small fish trailing huge flowing veil fins and tail",
      tags=["betta", "siamese fighting fish", "fighting fish", "aquarium", "pet fish", "veil tail"])
def _(S):
    r = L(S, 0, 1.2)
    bd = ellipse(7, 10, 4.3, 2.8)
    a, b_, c, d = (10, 8.2), (20.8, 4), (19, 20.5), (9.5, 12)
    tail = (f"M{_p(a)}C13 5.5 17 3.8 {_p((20.3, 4))}" + tip((17, 3.8), b_, (21.3, 9), r)
            + f"C21.5 10 21 16 {_p((19.3, 20))}" + tip((21, 16), c, (15, 21), r) + f"C15 21.5 11.5 18 8 14"
            + tip((11.5, 18), (6, 18.5), (7, 13), r) + f"L7.5 12.4L{_p(d)}Z")
    return [shell(union(bd, tail)), detail("M12.5 10L18 7.5"), detail("M12.5 12.5L18 15.5"), dot(5, 9.5, 1)]


@icon("piranha", CAT, "Deep bodied fish with a jutting lower jaw full of triangular teeth",
      tags=["predator", "teeth", "amazon", "river", "bite", "dangerous"])
def _(S):
    b = ellipse(11, 12, 7, 6.5)
    jaw = fin(S, [(5.2, 13.2), (2.6, 14), (5.5, 17.5)])
    t = fork(S, 17.5, 12, 1.5, 4, 4.5, notch=0.4)
    return [shell(union(b, jaw, t)), detail("M4 13L5.5 11.5L7 13L8.5 11.5L10 13"), dot(7.8, 8.8, 1.1)]


@icon("flounder", CAT, "Flatfish lying on the seabed with both eyes bulging from its upper side",
      tags=["flatfish", "plaice", "sole", "halibut", "seabed", "seafood"])
def _(S):
    b = "M2.5 15.8C4.5 12.8 8.5 11.8 11.5 11.8C14.5 11.8 16.5 13 17.8 14.3L17.8 16.8C14 18.3 6 18.3 2.5 15.8Z"
    eyes = [circle(6.2, 11.6, 1.8), circle(9.8, 10.9, 1.8)]
    t = fan(S, 17.8, 15.5, 1.2, 3.8, 3)
    return [shell(union(b, *eyes, t)), line(seg(2, 20.5, 22, 20.5)), dot(6.2, 11.6, 0.8), dot(9.8, 10.9, 0.8)]


@icon("ocean-sunfish", CAT, "Huge round fish with tall fins above and below and a clipped stubby rear",
      tags=["mola", "mola mola", "sunfish", "giant fish", "ocean"])
def _(S):
    r = L(S, 0, 1)
    b = circle(10, 12, 7)
    top = fin(S, [(12, 6), (15.6, 2.6), (16.8, 8.8)], r=r)
    bot = fin(S, [(12, 18), (15.6, 21.4), (16.8, 15.2)], r=r)
    rear = "M15 7.5C17.5 9 17.8 10.5 17 12C17.8 13.5 17.5 15 15 16.5Z"
    return [shell(union(b, top, bot, rear)), dot(6.5, 10.2, 1.1), detail("M3.8 13.8L5.4 13.4")]


@icon("flying-fish", CAT, "Small fish gliding above a wave with long wing like fins spread wide",
      tags=["gliding fish", "wings", "tropical", "ocean", "sea", "flight"])
def _(S):
    b = body(3, 15.5, 12.5, 2.4, 2.2, j=0.9, peak=0.4, blunt=0.6)
    wing = fin(S, [(7.5, 11), (16.5, 3), (18, 5.3), (11.5, 11.3)], r=L(S, 0, 1.2))
    t = fork(S, 15.5, 12.5, 0.9, 5, 3.6, notch=0.4)
    return [shell(union(b, wing, t)), line(water(2, 22, 19.5, 1, 3)), dot(5.5, 12, 0.9)]


@icon("lionfish", CAT, "Fish with long spiky fins radiating from its back like a mane",
      tags=["venomous", "spines", "reef fish", "invasive", "tropical fish", "ocean"])
def _(S):
    b = body(3, 15.5, 15, 3.2, 3, j=1.2, peak=0.4, blunt=0.6)
    t = fan(S, 15.5, 15, 1.2, 4.8, 3.6)
    c = (10.5, 16)
    spines = [line(poly([pt(c, 4.5, a), pt(c, ln, a)])) for a, ln in ((-150, 9.4), (-123, 11.5), (-96, 12.2), (-69, 11.5), (-42, 9))]
    return [shell(union(b, t)), *spines, line(poly([(8.5, 18), (6.2, 21.5)])), line(poly([(11.3, 18), (12, 21.5)])),
            detail("M10.5 12.3V17.7"), dot(5.6, 14.3, 1)]


@icon("butterflyfish", CAT, "Flat disc shaped fish with a pointed snout, an eye stripe and an eye spot near the tail",
      tags=["reef fish", "tropical fish", "coral reef", "aquarium", "ocean"])
def _(S):
    b = circle(11.5, 12, 6.8)
    sn = fin(S, [(5.5, 10.4), (2.3, 12.5), (5.5, 14)])
    t = fan(S, 18, 12, 1.5, 3.6, 3.4)
    return [shell(union(b, sn, t)), detail("M8.5 5.9C7.3 9.5 7.3 14.5 8.5 18.1"), dot(14.3, 10, 1.4)]


@icon("surgeonfish", CAT, "Oval fish with a long dorsal fin and a sharp spine at the base of its tail",
      tags=["tang", "blue tang", "reef fish", "tropical fish", "aquarium", "doctorfish"])
def _(S):
    b = body(3, 16, 12, 6, 5.5, j=1.3, peak=0.45, blunt=0.55)
    t = poly([(15, 10.8), (21, 6.8), (19.3, 12), (21, 17.2), (15, 13.2)], closed=True, r=L(S, 0, 1))
    return [shell(union(b, t)), detail("M5.5 9C8 6.8 11.5 6.5 14.5 8.3"), mark(fin(S, [(13, 13.4), (16.5, 11.7), (14.4, 14.9)], r=L(S, 0, 0.3))),
            dot(6.3, 11, 1)]


@icon("parrotfish", CAT, "Chunky fish with a fused parrot like beak and large scales",
      tags=["reef fish", "beak", "tropical fish", "coral reef", "scales", "ocean"])
def _(S):
    b = body(4, 16, 12.5, 5.5, 5, j=1.5, peak=0.38, blunt=0.9, lean=0.05)
    beak = ellipse(3.8, 13.2, 2, 2.1)
    t = poly([(15, 10.8), (21, 7.2), (20, 12.5), (21, 17.8), (15, 14.2)], closed=True, r=L(S, 0, 1))
    return [shell(union(b, beak, t)), detail("M2 13.2H5"), detail("M8.3 10.5C9.3 11.8 10.9 11.8 11.9 10.5C12.9 11.8 14.5 11.8 15.3 11"),
            detail("M8.3 14.8C9.3 16.1 10.9 16.1 11.9 14.8C12.9 16.1 14.5 16.1 15.3 15.3"), dot(7, 9.8, 1)]


@icon("boxfish", CAT, "Cube shaped fish with a boxy body, spots, tiny fins and a small tail",
      tags=["cowfish", "trunkfish", "reef fish", "tropical fish", "spotted", "aquarium"])
def _(S):
    bx = rect(3, 6.5, 13.5, 11.5, L(S, 2.5, 4))
    t = fan(S, 16.5, 12.2, 1.5, 4.5, 3.5)
    lips = circle(3, 14.5, 1.3)
    return [shell(union(bx, t, lips)), dot(6.5, 10, 1.1), dot(10.5, 10.5, 0.95), dot(13.3, 13, 0.95), dot(9.6, 14.6, 0.95)]


@icon("triggerfish", CAT, "Diamond shaped fish with a raised spike dorsal fin and a small mouth at its front point",
      tags=["reef fish", "tropical fish", "picasso fish", "coral reef", "aquarium", "ocean"])
def _(S):
    r = L(S, 0, 1.5)
    b = poly([(2.8, 12.5), (10, 6.5), (16, 10.8), (16, 13.4), (10, 18.8)], closed=True, r=r)
    t = poly([(15, 10.6), (21, 7.5), (19.8, 12.1), (21, 16.7), (15, 13.6)], closed=True, r=L(S, 0, 1))
    return [shell(union(b, t)), line(poly([(10.3, 7.2), (11.8, 2.6)], r=S.r)), dot(7.2, 10.6, 1)]


@icon("moorish-idol", CAT, "Disc shaped fish with bold vertical bands and a very long streamer trailing from its back",
      tags=["reef fish", "tropical fish", "coral reef", "aquarium", "banner fish", "ocean"])
def _(S):
    b = circle(11, 14, 5.8)
    sn = fin(S, [(6, 12.2), (2.5, 14.6), (6, 16.2)], r=L(S, 0, 0.5))
    t = fan(S, 16.5, 14, 1.3, 3.8, 3)
    return [shell(union(b, sn, t)), line("M9.8 8.4C10.8 4.8 14 3 20.8 3.5"), detail("M8.8 8.6C7.8 11.5 7.8 16.5 8.8 19.4"),
            detail("M13.2 8.6C12.2 11.5 12.2 16.5 13.2 19.4"), dot(6.2, 13.2, 0.9)]


@icon("unicornfish", CAT, "Oval fish with a long straight horn projecting forward from its forehead",
      tags=["reef fish", "horn", "tang", "tropical fish", "coral reef", "ocean"])
def _(S):
    b = body(4, 16.5, 13.5, 5, 4.5, j=1.2, peak=0.42, blunt=0.75)
    t = poly([(15.5, 12.3), (21, 8.8), (19.6, 13.5), (21, 18.2), (15.5, 14.7)], closed=True, r=L(S, 0, 1))
    horn = fin(S, [(4.8, 11.4), (2, 7.6), (7.4, 9.4)], r=L(S, 0, 0.5))
    return [shell(union(b, t, horn)), dot(8, 12, 1)]


@icon("grouper", CAT, "Large heavy bodied fish with thick lips, a wide mouth and a rounded tail",
      tags=["sea bass", "reef fish", "big fish", "fishing", "seafood", "ocean"])
def _(S):
    b = body(3, 16.5, 12.5, 6, 5.5, j=1.8, peak=0.4, blunt=0.85, lean=0.05)
    lips = [ellipse(3.2, 11.8, 1.7, 1.3), ellipse(3.4, 14.4, 1.8, 1.3)]
    t = fan(S, 16.5, 12.5, 1.8, 4.8, 4.2)
    return [shell(union(b, *lips, t)), detail("M3.5 13.1L8.4 13.8"), dot(7.4, 10, 1.1), detail("M11.8 7.2C13.5 7.6 14.8 8.6 15.6 9.8")]


@icon("mudskipper", CAT, "Fish propped up on its front fins on a mud line with bulging eyes on top of its head",
      tags=["amphibious fish", "mudflat", "mangrove", "goby", "walking fish", "tidal"])
def _(S):
    b = body(3, 16.5, 12.5, 3.3, 3, j=1, peak=0.35, blunt=0.75)
    t = fork(S, 16.5, 12.5, 1, 4.5, 3.4, notch=0.5)
    fish = rot(union(b, t), 12, 3, 12.5)
    eyes = [circle(4.6, 8.2, 1.9), circle(7.6, 8.6, 1.9)]
    return [shell(union(fish, *eyes)), line(poly([(8.5, 15.3), (7.8, 19.2), (10.3, 19.2)], r=S.r)), line(seg(2, 21, 22, 21)),
            dot(4.6, 8, 0.8), dot(7.6, 8.4, 0.8)]


@icon("remora", CAT, "Slim fish with a flat oval ridged sucker disc on top of its head",
      tags=["suckerfish", "sharksucker", "hitchhiker", "ocean", "marine", "fish"])
def _(S):
    b = body(2.5, 16.5, 14.5, 3, 2.8, j=1, peak=0.35, blunt=0.55)
    t = fork(S, 16.5, 14.5, 1, 4.8, 3.8, notch=0.45)
    disc = ellipse(7.8, 9.6, 4.8, 2.2)
    return [shell(union(b, t)), shell(disc), detail("M6.3 8.6V10.6"), detail("M9.3 8.6V10.6"), dot(4.8, 14, 0.9)]


@icon("sturgeon", CAT, "Long prehistoric fish with bony plates, whisker barbels and a shark like tail",
      tags=["caviar", "ancient fish", "river", "bony plates", "freshwater", "roe"])
def _(S):
    r = L(S, 0, 1)
    b = body(2.5, 16.5, 11.5, 3.6, 3.2, j=1.1, peak=0.45, blunt=0.3, lean=0.05)
    t = poly([(15.8, 10.4), (21.5, 5.5), (20, 11.5), (19.8, 15.2), (15.8, 12.6)], closed=True, r=r)
    d = fin(S, [(12.5, 8.6), (14.2, 6.2), (15, 9.8)], r=r)
    plates = [mark(poly(regular(x, 10.4, 1.15, 4, 0), closed=True, r=L(S, 0, 0.3))) for x in (7.8, 10.4, 13)]
    return [shell(union(b, t, d)), *plates, line(seg(4.3, 13, 4, 16.5)), line(seg(6.5, 14, 6.3, 17.2)), dot(5, 10.6, 0.8)]


@icon("paddlefish", CAT, "Fish with a long flat paddle shaped snout far in front of its mouth",
      tags=["spoonbill", "spoonbill fish", "river", "freshwater", "ancient fish"])
def _(S):
    b = body(8.5, 17, 13, 3.4, 3.2, j=1, peak=0.35, blunt=0.65)
    t = poly([(16.2, 11.9), (21.2, 8), (20, 13.2), (21.2, 18.2), (16.2, 14.1)], closed=True, r=L(S, 0, 1))
    paddle = poly(tube(lambda t: (9.5 - 6 * t, 12.3 - 1 * t), lambda t: 1.6 + 1.6 * t ** 2, 12), closed=True, r=0)
    end = ellipse(3.8, 11.3, 2, 1.8)
    return [shell(union(b, t, paddle, end)), dot(10.8, 12, 0.9), detail("M9 14.3L12 14.6")]


@icon("largemouth-bass", CAT, "Stocky fish with an oversized open mouth and a spiny dorsal fin",
      tags=["bass", "black bass", "freshwater", "sport fishing", "angling", "lake"])
def _(S):
    r = L(S, 0, 0.8)
    b = body(3, 16.5, 13, 5, 4.6, j=1.4, peak=0.42, blunt=0.7)
    spines = [fin(S, [(6.5, 9.2), (7.5, 5.2), (9, 8.6)], r=r), fin(S, [(8.6, 8.6), (9.8, 5), (11.2, 8.4)], r=r),
              fin(S, [(11, 8.6), (13.6, 6.6), (14.6, 10.4)], r=r)]
    t = fan(S, 16.5, 13, 1.4, 4.6, 4)
    mouth = poly([(0.5, 9.8), (9, 13), (0.5, 17)], closed=True)
    return [shell(minus(union(b, *spines, t), mouth)), dot(7.2, 10.3, 1)]


@icon("mahi-mahi", CAT, "Fish with a tall blunt forehead, a dorsal fin along its whole back and a forked tail",
      tags=["dorado", "dolphinfish", "game fish", "tropical", "seafood", "sport fishing"])
def _(S):
    r = L(S, 0, 1)
    b = ("M3.5 14.5L3.5 8" + tip((3.5, 14.5), (3.5, 5.5), (7, 5.5), L(S, 0, 1.8)) + "L7 5.5C10.5 5.8 14 7.8 16.8 10.8L16.8 13.2"
         "C13.5 15.5 9.5 16.8 6.5 16.8C4.8 16.8 3.5 16 3.5 14.5Z")
    t = fork(S, 16.8, 12, 1.2, 4.6, 5, notch=0.4)
    return [shell(union(b, t)), detail("M5.8 7.8C9.5 8 12.8 9.5 15.5 12"), dot(6.2, 11, 1.05)]


@icon("oarfish", CAT, "Very long ribbon shaped fish in waves with a tall crest of spines on its head",
      tags=["king of herrings", "sea serpent", "deep sea", "ribbon fish", "giant fish", "ocean"])
def _(S):
    def c(t):
        return (4.5 + 16.5 * t, 16 + 2.6 * math.sin(t * 2.2 * math.pi))

    def w(t):
        return 3.4 - 2.2 * t
    b = poly(tube(c, w, 40), closed=True, r=0)
    head = ellipse(4.5, 16, 2.5, 2.1)
    o = (6, 14.5)
    crest = poly([o, pt(o, 9, -122), pt(o, 9, -96), pt(o, 9, -70)], closed=True, r=L(S, 0, 1))
    return [shell(union(b, head, crest)), detail(seg(*pt(o, 2.5, -96), *pt(o, 7, -96))), dot(3.9, 15.7, 0.75)]


@icon("hatchetfish", CAT, "Tiny deep sea fish with a deep hatchet shaped belly, a thin tail and upturned eyes",
      tags=["marine hatchetfish", "deep sea", "glowing", "abyss", "tiny fish"])
def _(S):
    r = L(S, 0, 1.5)
    b = ("M3.5 9" + tip((3.5, 11), (3.5, 7.5), (14, 8.8), r) + "L14 8.8L16.5 10.5L16.5 12.5L14.2 13.5"
         "C12 17.5 9 19.5 6.5 19.5C4.5 19.5 3.5 16 3.5 11Z")
    t = fork(S, 16.5, 11.5, 1, 4.5, 3.6, notch=0.45)
    return [shell(union(b, t)), dot(5.8, 10.2, 1.3), dot(7, 16.5, 0.8), dot(9.5, 15.8, 0.8), dot(11.7, 14.2, 0.8)]


@icon("blobfish", CAT, "Droopy gelatinous blob face with a sagging nose and a downturned mouth",
      tags=["blob", "deep sea", "ugly", "sad", "meme", "gloomy"])
def _(S):
    r = L(S, 0, 2)
    d = ("M12 3.5C17.5 3.5 20.5 7.5 20 13C19.8 16 20.8 18 20.8 20.5" + tip((20.8, 18), (20.8, 20.5), (3.2, 20.5), r)
         + tip((20.8, 20.5), (3.2, 20.5), (3.2, 18), r) + "L3.2 18C3.2 18 4.2 16 4 13C3.5 7.5 6.5 3.5 12 3.5Z")
    return [shell(d), detail("M10.2 9.8C10.2 12.5 9.5 14.5 12 14.5C14.5 14.5 13.8 12.5 13.8 9.8"),
            detail("M8.2 18.2C10.2 16.8 13.8 16.8 15.8 18.2"), dot(7.8, 9.5, 1.1), dot(16.2, 9.5, 1.1)]


@icon("barreleye", CAT, "Fish whose head is a clear dome with two tube eyes inside pointing up",
      tags=["spookfish", "transparent head", "deep sea", "abyss", "strange fish"])
def _(S):
    b = body(3, 16.5, 15.5, 3, 3, j=1, peak=0.4, blunt=0.7)
    t = fan(S, 16.5, 15.5, 1, 4.5, 3.4)
    return [shell(union(b, t)), line("M3.5 13.5C3.5 7.5 5.5 4.5 8.5 4.5C11.5 4.5 13.5 7.5 13.5 12.5"),
            line(seg(7, 12.2, 7, 9.5)), line(seg(10.2, 12.2, 10.2, 9.5)), dot(7, 8.8, 1.3), dot(10.2, 8.8, 1.3)]


@icon("tripod-fish", CAT, "Fish standing on the seabed on three long stilt like fin rays",
      tags=["deep sea", "stilts", "seabed", "abyss", "strange fish", "tripod"])
def _(S):
    b = body(3, 16.5, 9, 2.8, 2.6, j=1, peak=0.4, blunt=0.6)
    t = fork(S, 16.5, 9, 1, 4.5, 3.4, notch=0.45)
    return [shell(union(b, t)), line(seg(7, 11, 5, 20)), line(seg(9.2, 11.2, 10.5, 20)), line(seg(19.5, 11.5, 20.5, 20)),
            line(seg(2, 21, 22, 21)), dot(5.5, 8.4, 0.95)]


@icon("stonefish", CAT, "Lumpy rock like fish with warty skin, an upturned mouth and eyes on top",
      tags=["venomous fish", "camouflage", "reef", "rock", "dangerous", "ocean"])
def _(S):
    r = L(S, 0, 1)
    top = union(circle(6.5, 11, 3.2), circle(10.5, 9.6, 3.4), circle(14.5, 10.8, 3), ellipse(11, 14, 8.5, 4.5))
    t = fan(S, 18.5, 14.5, 1.5, 3.2, 3)
    return [shell(union(top, t)), detail("M3 14C4.5 15.2 6.5 15.2 8 13.6"), dot(6.8, 10.4, 1.1), dot(12, 13, 0.8),
            dot(15, 14.8, 0.8), dot(10.5, 16.5, 0.8)]


@icon("frogfish", CAT, "Round lumpy fish sitting on leg like fins with a small lure above its wide mouth",
      tags=["anglerfish", "walking fish", "camouflage", "reef", "lure", "ocean"])
def _(S):
    b = circle(12, 11.5, 6.5)
    t = fan(S, 18, 11, 1.5, 3.4, 3.2)
    return [shell(union(b, t)), line(poly([(9.5, 17.2), (8.2, 20.5), (5.5, 20.5)], r=S.r)), line(poly([(14.5, 17.4), (15.2, 20.5), (18, 20.5)], r=S.r)),
            detail("M5.8 12.2C7.5 13.8 10 14 12 13"), line("M8.2 6.2C7 4.6 5.5 4.2 4.2 4.6"), dot(3.9, 4.8, 1.3), dot(10.8, 9.5, 1.1)]


@icon("discus-fish", CAT, "Round flat disc shaped fish with thin wavy bands and small fins",
      tags=["discus", "cichlid", "aquarium", "amazon", "tropical fish", "freshwater"])
def _(S):
    b = circle(11, 12, 7.4)
    t = fan(S, 18, 12, 1.4, 3.6, 3)
    sn = fin(S, [(4.2, 10.8), (2.5, 12.6), (4.5, 13.8)], r=L(S, 0, 0.4))
    return [shell(union(b, t, sn)), detail("M9.2 5.2C8.2 7.5 10.2 9.5 9.2 12C8.2 14.5 10.2 16.5 9.2 18.8"),
            detail("M13.2 5.4C12.2 7.7 14.2 9.7 13.2 12.2C12.2 14.7 14.2 16.7 13.2 18.6"), dot(6.3, 10.6, 1)]


@icon("lanternfish", CAT, "Small fish with a big eye and a row of glowing lights along its belly",
      tags=["myctophid", "deep sea", "bioluminescent", "glowing", "light", "abyss"])
def _(S):
    b = body(2.5, 16.5, 11.5, 5, 4.6, j=1.3, peak=0.35, blunt=0.75)
    t = fork(S, 16.5, 11.5, 1.3, 4.5, 4, notch=0.45)
    return [shell(union(b, t)), dot(6, 9.8, 1.8), dot(6.4, 13.8, 1), dot(9.4, 14, 1), dot(12.4, 13.2, 1)]


@icon("fish-school", CAT, "Three small identical fish swimming in a staggered group",
      tags=["shoal", "school of fish", "fishes", "group", "swarm", "aquarium", "ocean"])
def _(S):
    def small(x, y):
        b = f"M{f(x)} {f(y)}C{f(x + 1.5)} {f(y - 2.6)} {f(x + 5)} {f(y - 2.6)} {f(x + 6.2)} {f(y - 0.6)}L{f(x + 6.2)} {f(y + 0.6)}C{f(x + 5)} {f(y + 2.6)} {f(x + 1.5)} {f(y + 2.6)} {f(x)} {f(y)}Z"
        tl = fin(S, [(x + 5.5, y), (x + 8.6, y - 2.4), (x + 8.6, y + 2.4)], r=L(S, 0, 0.6))
        return union(b, tl)
    return [shell(small(2.5, 6.5)), shell(small(12.5, 12)), shell(small(2.5, 17.5)),
            dot(4.8, 6, 0.8), dot(14.8, 11.5, 0.8), dot(4.8, 17, 0.8)]


# --------------------------------------------------------------------------- sharks and rays

@icon("hammerhead-shark", CAT, "Shark seen from above with a wide flat hammer shaped head and eyes at each end",
      tags=["hammerhead", "shark", "predator", "ocean", "marine", "top view"])
def _(S):
    r = L(S, 0, 1)
    head = poly([(2.5, 4.2), (21.5, 4.2), (21.5, 7.2), (14.2, 7.8), (9.8, 7.8), (2.5, 7.2)], closed=True, r=L(S, 0, 1.5))
    bd = "M10 7.5C9.3 11 9.6 15 10.8 18.3L13.2 18.3C14.4 15 14.7 11 14 7.5Z"
    fl = fin(S, [(10, 10.2), (5.5, 14.8), (10.2, 13.3)], r=r)
    fr = fin(S, [(14, 10.2), (18.5, 14.8), (13.8, 13.3)], r=r)
    tl = fin(S, [(11, 17.4), (8.8, 21.6), (12, 20.2), (15.2, 21.6), (13, 17.4)], r=r)
    return [shell(union(head, bd, fl, fr, tl)), dot(4.4, 5.7, 0.9), dot(19.6, 5.7, 0.9)]


@icon("whale-shark", CAT, "Huge shark with a wide flat mouth at the front and spots on its back",
      tags=["gentle giant", "shark", "biggest fish", "filter feeder", "ocean", "diving"])
def _(S):
    r = L(S, 0, 1)
    b = ("M2.5 10" + tip((2.5, 15.5), (2.5, 9.5), (6, 8.3), L(S, 0, 1.5)) + "C8 7.6 9.5 7.5 10.5 7.5" + tip((10.5, 7.5), (12.2, 3.8), (13.8, 7.8), r)
         + "L13.8 7.8C15.5 8.2 17 9 18 10" + tip((18, 10), (21.5, 5.5), (20.2, 11.8), r) + tip((21.5, 5.5), (20.2, 11.8), (21.5, 17.5), r)
         + tip((20.2, 11.8), (21.5, 17.5), (18, 13.8), r) + "L18 13.8C15 15.8 12 16.3 9.5 16.3" + tip((9.5, 16.3), (8.3, 19.8), (6.8, 16.2), r)
         + "L6.8 16.2C4.8 16.1 2.5 15.8 2.5 15.5Z")
    return [shell(b), detail("M2.5 13.2H6"), dot(5.2, 11, 0.85), dot(9, 10.3, 0.9), dot(12, 10.8, 0.9), dot(10.5, 13.4, 0.9),
            dot(14.2, 12.4, 0.9)]


@icon("thresher-shark", CAT, "Shark with an extremely long curved upper tail lobe as long as its body",
      tags=["thresher", "shark", "long tail", "predator", "ocean", "marine"])
def _(S):
    r = L(S, 0, 1)
    b = ("M2.5 15.5C4 13.6 6 12.6 7.6 12.3" + tip((7.6, 12.3), (8.8, 9), (10.2, 12.4), r)
         + "L10.2 12.4C11.2 12.7 12.2 13.1 13 13.6C15.5 10 18.5 6 21.5 3C19.8 7.2 17.3 11.4 14.6 15.3"
         + tip((14.6, 15.3), (15.8, 18.3), (13, 16.4), r) + "L13 16.4C11 17.6 8.8 18 7.2 18"
         + tip((7.2, 18), (6.3, 20.6), (5, 17.6), r) + "L5 17.6C4 17.2 3 16.5 2.5 15.5Z")
    return [shell(b), dot(5.2, 15, 0.85)]


@icon("goblin-shark", CAT, "Shark with a long flat blade like snout overhanging protruding jaws",
      tags=["goblin", "deep sea", "shark", "strange", "abyss", "ocean"])
def _(S):
    r = L(S, 0, 1)
    b = ("M2.3 9.8C5 9.6 7 9.4 9 9.4C10.5 9.3 12 9.3 13.3 9.5" + tip((13.3, 9.5), (14.6, 6.4), (16, 9.9), r)
         + "L16 9.9C17.5 10.3 19 11 20 11.8" + tip((20, 11.8), (21.8, 8.5), (21.2, 13.8), r) + tip((21.8, 8.5), (21.2, 13.8), (18.5, 14.2), r)
         + "L18.5 14.2C15 15.6 12 15.6 10 15.2" + tip((10, 15.2), (6.8, 16.8), (7.8, 14.4), r) + "L7.8 14.4C7 12.6 5 11.3 2.3 9.8Z")
    return [shell(b), dot(9.4, 11.2, 0.85)]


@icon("tiger-shark", CAT, "Shark with a blunt square snout and dark stripes along its back",
      tags=["tiger", "shark", "stripes", "predator", "ocean", "marine"])
def _(S):
    r = L(S, 0, 1)
    b = ("M2.8 10.6" + tip((2.8, 14), (2.8, 10), (6, 9.5), L(S, 0, 1.2)) + "C8 9.2 9.5 9 10.5 9" + tip((10.5, 9), (12.6, 4.2), (14, 9.3), r)
         + "L14 9.3C16 9.6 17.5 10.3 18.4 11" + tip((18.4, 11), (21.5, 6.6), (20.4, 12.5), r) + tip((21.5, 6.6), (20.4, 12.5), (21.5, 17), r)
         + tip((20.4, 12.5), (21.5, 17), (18.2, 14), r) + "L18.2 14C15.5 15.5 12.5 16 10 16" + tip((10, 16), (8.8, 19.8), (7.2, 15.8), r)
         + "L7.2 15.8C5 15.5 2.8 15 2.8 14Z")
    return [shell(b), detail("M9 9.2L8 13.2"), detail("M12.5 9.2L11.5 13.4"), detail("M16 9.8L15.2 13.2"), dot(5.3, 11.8, 0.9)]


@icon("sawfish", CAT, "Flat ray like fish seen from above with a long saw shaped snout edged with teeth",
      tags=["carpenter shark", "saw", "ray", "endangered", "ocean", "top view"])
def _(S):
    r = L(S, 0, 1)
    head = "M9.5 9.2C11 9.2 12.5 9.5 13.5 10L13.5 14C12.5 14.5 11 14.8 9.5 14.8C8.7 13.5 8.7 10.5 9.5 9.2Z"
    fl = fin(S, [(11, 10), (14.5, 5.5), (15.5, 11)], r=r)
    fr = fin(S, [(11, 14), (14.5, 18.5), (15.5, 13)], r=r)
    tail = "M13 10.2C16 10.8 18.5 11.4 20.8 12C18.5 12.6 16 13.2 13 13.8Z"
    tf = fin(S, [(18.5, 12), (21.8, 9.4), (21.8, 14.6)], r=r)
    return [shell(union(head, fl, fr, tail, tf)), line(seg(2.5, 12, 9, 12)), line(seg(3.8, 10, 3.8, 14)), line(seg(6.6, 10, 6.6, 14))]


@icon("manta-ray", CAT, "Wide diamond shaped ray seen from above with pointed wings and two curled horn lobes",
      tags=["manta", "devil ray", "ray", "ocean", "diving", "marine"])
def _(S):
    r = L(S, 0, 1.5)
    a, lw, rear, rw, b = (10, 7), (2, 12), (12, 17.5), (22, 12), (14, 7)
    d = (f"M{_p(a)}C7.5 7.3 4.5 9 3 10.8" + tip((3, 10.8), lw, (5, 13), r) + "L5 13C7.5 14 10 15.5 12 17.5"
         + "C14 15.5 16.5 14 19 13" + tip((19, 13), rw, (21, 10.8), r) + f"L21 10.8C19.5 9 16.5 7.3 {_p(b)}Z")
    return [shell(d), line("M10.3 7.2C9 6 8.8 4.2 10 3.4"), line("M13.7 7.2C15 6 15.2 4.2 14 3.4"), line(seg(12, 17.5, 12, 21.8)),
            dot(10.3, 10, 0.85), dot(13.7, 10, 0.85)]


@icon("stingray", CAT, "Rounded flat ray seen from above with a long thin whip tail and a small barb",
      tags=["ray", "sting", "barb", "seabed", "ocean", "marine"])
def _(S):
    r = L(S, 0, 2)
    d = ("M12 4C15.5 4 18.5 6.5 20.5 9.3" + tip((18.5, 6.5), (21.8, 11), (19, 13.5), r)
         + "L19 13.5C17 15.5 14.5 16.8 12 16.8C9.5 16.8 7 15.5 5 13.5" + tip((5, 13.5), (2.2, 11), (5.5, 6.5), r)
         + "L3.5 9.3C5.5 6.5 8.5 4 12 4Z")
    return [shell(d), line(seg(12, 16.8, 12, 22)), line(poly([(12, 19.5), (14, 18.3)], r=S.r)), dot(10.2, 8, 0.85), dot(13.8, 8, 0.85)]


@icon("eagle-ray", CAT, "Ray seen from above with pointed swept back wings, a rounded snout, spots and a long tail",
      tags=["spotted eagle ray", "ray", "ocean", "diving", "marine", "reef"])
def _(S):
    r = L(S, 0, 1.2)
    d = ("M10.5 6.5C8 7.5 5 10.5 2.5 15" + tip((5, 11), (2.5, 15), (7.5, 13), r) + "L7.5 13C9.5 13 11 14 12 15.5"
         "C13 14 14.5 13 16.5 13" + tip((16.5, 13), (21.5, 15), (19, 11), r) + "L19 11C18 9 16 7.5 13.5 6.5Z")
    return [shell(union(d, ellipse(12, 5.8, 2.2, 2.4))), line(seg(12, 15.5, 12, 21.8)), dot(8.5, 10.2, 0.9), dot(15.5, 10.2, 0.9),
            dot(12, 9.5, 0.9)]


@icon("electric-ray", CAT, "Nearly round flat ray seen from above with a short thick tail and a lightning bolt on its disc",
      tags=["torpedo ray", "numbfish", "ray", "electricity", "shock", "ocean"])
def _(S):
    r = L(S, 0, 1)
    disc = ellipse(12, 9.5, 8.5, 6.8)
    tail = poly([(10.5, 14.5), (10.8, 17.5), (13.2, 17.5), (13.5, 14.5)], closed=True)
    tf = fin(S, [(12, 16.5), (8, 21.5), (16, 21.5)], r=r)
    pel = [fin(S, [(8.5, 14.5), (6.5, 16.8), (10.5, 16)], r=r), fin(S, [(15.5, 14.5), (17.5, 16.8), (13.5, 16)], r=r)]
    return [shell(union(disc, tail, tf, *pel)), mark(poly(bolt(12.8, 4.8, 0.95), closed=True, r=L(S, 0, 0.4)))]


@icon("guitarfish", CAT, "Fish seen from above with a flat triangular ray front tapering into a thick shark like tail",
      tags=["shovelnose ray", "ray", "shark", "sand", "seabed", "ocean"])
def _(S):
    r = L(S, 0, 1.5)
    front = ("M12 2.5C14.5 2.5 16.5 6 17.8 10" + tip((16.5, 6), (18, 11), (13.8, 12.5), r)
             + "L13.8 12.5L13.2 18.5L10.8 18.5L10.2 12.5" + tip((10.2, 12.5), (6, 11), (7.5, 6), r) + "L6.2 10C7.5 6 9.5 2.5 12 2.5Z")
    fins = [fin(S, [(13.3, 14), (15.5, 15.3), (13.2, 16.4)], r=L(S, 0, 0.5)), fin(S, [(10.7, 14), (8.5, 15.3), (10.8, 16.4)], r=L(S, 0, 0.5))]
    tl = fin(S, [(11, 18), (9.2, 21.6), (12.2, 20.6), (15, 21.6), (13, 18)], r=L(S, 0, 1))
    return [shell(union(front, *fins, tl)), dot(10.5, 6.8, 0.85), dot(13.5, 6.8, 0.85)]


# --------------------------------------------------------------------------- shark things

@icon("shark-fin", CAT, "Single triangular dorsal fin cutting above a wavy water line",
      tags=["shark", "fin", "danger", "swimming", "beach", "warning", "ocean"])
def _(S):
    r = L(S, 0, 1.5)
    d = "M4.5 16C8 14 11.5 9 15.5 3.2" + tip((11.5, 9), (15.5, 3.2), (15.2, 10), r) + "L15.2 10C15.2 12.5 16.3 14.5 18.5 16Z"
    return [shell(d), line(water(2, 22, 19, 1.2, 3))]


@icon("shark-tooth", CAT, "Single large triangular shark tooth with a curved root",
      tags=["tooth", "fossil", "megalodon", "fang", "necklace", "beach find"])
def _(S):
    d = ("M12 2.5" + tip((6, 13), (12, 2.5), (18, 13), L(S, 0, 1)) + "C12.8 7 15.5 11.5 19 14.5C20.3 16.5 19.8 19 17.8 19.8"
         "C16 19.9 14 19.2 12 18.8C10 19.2 8 19.9 6.2 19.8C4.2 19 3.7 16.5 5 14.5C8.5 11.5 11.2 7 12 2.5Z")
    return [shell(d), detail("M5.6 15.4C9.5 16.8 14.5 16.8 18.4 15.4")]


def _jaw_filled():
    ring = D(P(ellipse(12, 12, 11, 9.8)), P(ellipse(12, 12, 6.8, 5.6)))
    teeth = []
    for x in (9, 12, 15):
        teeth.append(poly([(x - 1.6, 7.5), (x, 10.5), (x + 1.6, 7.5)], closed=True))
        teeth.append(poly([(x - 1.6, 16.5), (x, 13.5), (x + 1.6, 16.5)], closed=True))
    return U(ring, *[P(t) for t in teeth])


@icon("shark-jaw", CAT, "Front view of open shark jaws with rows of triangular teeth around the opening",
      tags=["jaws", "teeth", "bite", "shark", "danger", "predator"], filled=_jaw_filled)
def _(S):
    r = L(S, 0, 0.3)
    ring = minus(ellipse(12, 12, 10, 8.8), ellipse(12, 12, 6.2, 5))
    teeth = []
    for x in (9, 12, 15):
        teeth.append(poly([(x - 1.3, 7.8), (x, 10.2), (x + 1.3, 7.8)], closed=True, r=r))
        teeth.append(poly([(x - 1.3, 16.2), (x, 13.8), (x + 1.3, 16.2)], closed=True, r=r))
    return [shell(union(ring, *teeth))]


@icon("shark-cage", CAT, "Barred diving cage hanging below the water line with a shark fin nearby",
      tags=["cage diving", "diving", "shark", "adventure", "tourism", "ocean"])
def _(S):
    r = L(S, 0, 1.2)
    fin_d = "M12.5 9C15.5 7.5 18 5 20.2 2" + tip((18, 5), (20.2, 2), (19.8, 6), r) + "L19.8 6C19.8 7.3 20.5 8.3 21.8 9Z"
    return [shell(rect(2.5, 12.5, 11, 9, min(S.R, 2))), detail(seg(6.2, 12.5, 6.2, 21.5)), detail(seg(9.8, 12.5, 9.8, 21.5)),
            line(seg(8, 12.5, 8, 2.5)), line(seg(2, 9, 22, 9)), shell(fin_d)]


@icon("mermaids-purse", CAT, "Shark egg case pouch with a curly tendril at each corner",
      tags=["egg case", "shark egg", "skate egg", "beachcombing", "beach find", "ocean"])
def _(S):
    d = "M7 6.5C9.5 7.5 14.5 7.5 17 6.5C16 10 16 14 17 17.5C14.5 16.5 9.5 16.5 7 17.5C8 14 8 10 7 6.5Z"
    if S.name == "rounded":
        d = rect(7, 6.5, 10, 11, 3)
    return [shell(d), line("M7.5 7C5.5 5 3 5 3 3.2C3 2.4 3.8 2 4.5 2.4"), line("M16.5 7C18.5 5 21 5 21 3.2C21 2.4 20.2 2 19.5 2.4"),
            line("M7.5 17C5.5 19 3 19 3 20.8C3 21.6 3.8 22 4.5 21.6"), line("M16.5 17C18.5 19 21 19 21 20.8C21 21.6 20.2 22 19.5 21.6")]


# --------------------------------------------------------------------------- marine mammals, reptiles and molluscs

@icon("humpback-whale", CAT, "Whale with extra long wing like flippers and grooves along its throat",
      tags=["humpback", "whale", "whale watching", "marine mammal", "ocean", "migration"])
def _(S):
    r = L(S, 0, 1)
    b = ("M2.5 12C2.8 8.8 6.5 7.8 10.5 8.2C14 8.6 15.5 9.8 17.2 8.8L19.8 9.4C19.2 13 15.5 15.8 10.5 15.8C5.5 15.8 2.3 14.8 2.5 12Z")
    fl = fin(S, [(17.3, 9.6), (14.8, 5.6), (18.4, 6.4), (21.5, 3.8), (20.8, 8), (19.6, 9.8)], r=r)
    flip = fin(S, [(7, 14.8), (11.8, 21.4), (10.5, 15.2)], r=r)
    return [shell(union(b, fl, flip)), detail("M3.2 12.8C5 13.6 7 13.7 9 13.3"), dot(6.4, 10.9, 0.9)]


@icon("dugong", CAT, "Sea cow in side view with a downturned snout and a fluked tail",
      tags=["sea cow", "manatee", "marine mammal", "seagrass", "ocean", "gentle"])
def _(S):
    r = L(S, 0, 1)
    b = "M5 9.5C8 8.2 12 8.5 15 9.5C16.5 10 17.5 10.3 18.5 9.8L19.5 11C18.5 13.5 16 15.5 12 15.5C9 15.5 6.5 15 5 14Z"
    head = union(circle(5.5, 11.8, 3.2), ellipse(3.8, 14, 2, 2.3))
    fl = fin(S, [(18.2, 10.6), (16.8, 6.4), (19.6, 7.8), (21.6, 5), (21.4, 9.6), (19.7, 11.2)], r=r)
    flip = fin(S, [(8, 14.8), (8.8, 19), (11.2, 15.3)], r=r)
    return [shell(union(b, head, fl, flip)), dot(5.8, 10.6, 0.9), detail("M2.6 14.2H4.8")]


@icon("marine-iguana", CAT, "Stocky lizard with a spiky crest along its back lying on a rock at the water line",
      tags=["iguana", "galapagos", "lizard", "reptile", "rock", "sea lizard"])
def _(S):
    r = L(S, 0, 0.4)
    rock = "M4.5 21.5C5 18.5 8 17 12 17C16 17 19 18.5 19.5 21.5Z"
    bd = "M2.5 11.5C2.5 9.6 4 8.6 6 8.6C9 8.6 12 10 15.5 11.5L15.5 13.8C12 14.2 9 14 6 13.6C4 13.3 2.5 13 2.5 11.5Z"
    crest = [poly([(x - 1, y + 0.8), (x, y - 1.7), (x + 1, y + 0.8)], closed=True, r=r) for x, y in ((7, 8.6), (10, 9.3), (13, 10.6))]
    tail = thick("M15 12.6C17.5 12.6 20 13.5 21.2 16.5", 2.2, S)
    legs = [thick(poly([(7.5, 13.5), (7, 17.5)]), 2.2, S), thick(poly([(13, 13.8), (13.5, 17.5)]), 2.2, S)]
    return [shell(union(rock, bd, *crest, tail, *legs)), line(seg(2, 21.5, 22, 21.5)), dot(5, 10.9, 0.85)]


@icon("nautilus", CAT, "Coiled striped spiral shell with a cluster of short tentacles and an eye at its opening",
      tags=["chambered nautilus", "mollusc", "mollusk", "cephalopod", "spiral", "fossil"])
def _(S):
    shl = circle(13.5, 10.5, 7.8)
    head = ellipse(7.2, 15, 3.4, 2.8)
    return [shell(union(shl, head)), detail("M10.2 14C9 10.5 11 7.5 14 7.5C16.5 7.5 17.5 9.5 17 11.5"),
            detail("M19.5 5.2L17.2 7.2"), detail("M21.2 11L18.2 11"), line(seg(4.6, 13.8, 2.2, 12.8)), line(seg(4.5, 16.3, 2.2, 17.5)),
            line(seg(6.8, 17.7, 5.8, 20.5)), dot(8, 14.2, 0.9)]


@icon("dumbo-octopus", CAT, "Round octopus with two ear like fins on top and short webbed arms like a skirt",
      tags=["dumbo", "deep sea", "octopus", "cute", "cephalopod", "abyss"])
def _(S):
    r = L(S, 0, 1.5)
    head = ellipse(12, 9.5, 6, 6)
    if S.name == "line":
        skirt = "M6.2 11L4 19.5L8 17.8L10 20.5L12 18L14 20.5L16 17.8L20 19.5L17.8 11Z"
    else:
        skirt = "M6.2 11L4.3 18.3Q4 19.5 5.3 19.2L8 18Q8.7 17.8 9.3 19.3Q10 21 11 19.5L12 18.2L13 19.5Q14 21 14.7 19.3Q15.3 17.8 16 18L18.7 19.2Q20 19.5 19.7 18.3L17.8 11Z"
    ears = [fin(S, [(7.2, 6.5), (3, 3.5), (3.3, 8), (6.5, 9)], r=r), fin(S, [(16.8, 6.5), (21, 3.5), (20.7, 8), (17.5, 9)], r=r)]
    return [shell(union(head, skirt, *ears)), dot(9.5, 10, 1.1), dot(14.5, 10, 1.1)]
