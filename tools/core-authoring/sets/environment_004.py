"""TypeIcon Core: environment (batch 004).

Restoration and ecology, field sites and monitoring, weather and season marks, calendar marks, urban climate
and resilience, and clean-energy and water systems. The cloud is the shared Core cloud (see sets/nature.py).
"""
import math
import re

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, LINE, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "environment"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


_NUM = re.compile(r"[A-Za-z]|-?\d*\.?\d+(?:e-?\d+)?")


def _tx(d, s=1.0, dx=0.0, dy=0.0, cx=12.0, cy=12.0, mirror=False):
    """Uniformly scale a d-string about (cx, cy), optionally mirror it, then translate (absolute M L H V C Q A Z)."""
    toks = _NUM.findall(d)
    out, i, cmd = [], 0, None
    sx = -s if mirror else s

    def X(v):
        return fmt(cx + (float(v) - cx) * sx + dx)

    def Y(v):
        return fmt(cy + (float(v) - cy) * s + dy)

    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t
            out.append(t)
            i += 1
            if cmd in "Zz":
                continue
        if cmd in "MLT":
            out.append(f"{X(toks[i])} {Y(toks[i + 1])}")
            i += 2
        elif cmd == "H":
            out.append(X(toks[i]))
            i += 1
        elif cmd == "V":
            out.append(Y(toks[i]))
            i += 1
        elif cmd in "CSQ":
            n = {"C": 3, "S": 2, "Q": 2}[cmd]
            out.append(" ".join(f"{X(toks[i + 2 * k])} {Y(toks[i + 2 * k + 1])}" for k in range(n)))
            i += 2 * n
        elif cmd == "A":
            rx, ry, rt, la, sw, x, y = toks[i:i + 7]
            if mirror:
                sw = "1" if sw == "0" else "0"
            out.append(f"{fmt(float(rx) * s)} {fmt(float(ry) * s)} {rt} {la} {sw} {X(x)} {Y(y)}")
            i += 7
        else:
            raise ValueError(f"unsupported command {cmd}")
    return "".join(out)


_CLOUD_LINE = "M4.5 19H19.5A3.8 3.8 0 0 0 18 11.7A6 6 0 0 0 6.5 10A4.7 4.7 0 0 0 4.5 19Z"
_CLOUD_ROUND = "M7 19H17.5A4.5 4.5 0 0 0 18 10.03A6 6 0 0 0 6.34 9.1A5 5 0 0 0 7 19Z"


def cloud(S, s=1.0, dx=0.0, dy=0.0, mirror=False):
    """The shared Core cloud, scaled about (12, 12) then moved."""
    return _tx(_CLOUD_LINE if S.name == "line" else _CLOUD_ROUND, s, dx, dy, mirror=mirror)


def region(d):
    return U(P(d), ST(d, 2))


def grow(p, g):
    return U(p, ST(path_to_d(p), 2 * g, "round", "round"))


def cut_strokes(S, ds, cutter, gap=2.0, w=2.0):
    """Stroke outlines of ds (in style S) minus grow(cutter, gap): for things seen behind another."""
    body = U(*[ST(d, w, S.cap, S.join) for d in ds])
    return solid(path_to_d(D(body, grow(cutter, gap))))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx, cy):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled body."""
    return Part("dot", d)


def sun_rays(cx, cy, r0, r1, n=8, start=0.0):
    return [seg(*polar(cx, cy, r0, start + k * 360 / n), *polar(cx, cy, r1, start + k * 360 / n)) for k in range(n)]


def slant(x, y0, y1, k=0.35):
    """A falling streak from (x, y0) to y1, leaning left as it falls."""
    return seg(x + (y1 - y0) * k / 2, y0, x - (y1 - y0) * k / 2, y1)


def wave(x0, x1, y, amp=1.5, n=3, up_first=True):
    w = (x1 - x0) / n
    s = -1 if up_first else 1
    d = f"M{fmt(x0)} {fmt(y)}"
    for k in range(n):
        a = x0 + k * w
        d += (f"Q{fmt(a + w / 4)} {fmt(y + s * amp * 2)} {fmt(a + w / 2)} {fmt(y)}"
              f"Q{fmt(a + 3 * w / 4)} {fmt(y - s * amp * 2)} {fmt(a + w)} {fmt(y)}")
    return d


def vwave(x, y0, y1, amp=1.5, n=2):
    """Smooth vertical wave from (x, y0) to (x, y1) with n full periods."""
    h = (y1 - y0) / n
    d = f"M{fmt(x)} {fmt(y0)}"
    for k in range(n):
        a = y0 + k * h
        d += (f"Q{fmt(x + amp * 2)} {fmt(a + h / 4)} {fmt(x)} {fmt(a + h / 2)}"
              f"Q{fmt(x - amp * 2)} {fmt(a + 3 * h / 4)} {fmt(x)} {fmt(a + h)}")
    return d


def leaf(x0, y0, x1, y1, bulge):
    """Leaf outline from base (x0, y0) to tip (x1, y1); bulge is the half width (sign picks the side first)."""
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy)
    nx, ny = -dy / ln * bulge * 2, dx / ln * bulge * 2
    return (f"M{fmt(x0)} {fmt(y0)}Q{fmt(mx + nx)} {fmt(my + ny)} {fmt(x1)} {fmt(y1)}"
            f"Q{fmt(mx - nx)} {fmt(my - ny)} {fmt(x0)} {fmt(y0)}Z")


def flake(S, cx, cy, R, branch=False, start=-90):
    parts = []
    for k in range(3):
        a = start + k * 60
        parts.append(line(seg(*polar(cx, cy, R, a), *polar(cx, cy, R, a + 180))))
    if branch:
        for k in range(6):
            a = start + k * 60
            ax, ay = polar(cx, cy, R * 0.6, a)
            parts.append(line(poly([polar(ax, ay, R * 0.36, a - 50), (ax, ay), polar(ax, ay, R * 0.36, a + 50)], r=S.r * 0.5)))
    return parts


def head(S, tip, deg, size=3.0, spread=45):
    a = polar(*tip, size, deg + 180 - spread)
    b = polar(*tip, size, deg + 180 + spread)
    return poly([a, tip, b], r=S.r * 0.6)


def arrow_head(x, y, deg, size=2.5):
    """Open chevron arrowhead with its tip at (x, y) pointing along deg."""
    a = polar(x, y, size * math.sqrt(2), deg + 135)
    b = polar(x, y, size * math.sqrt(2), deg - 135)
    return [a, (x, y), b]


def arc_arrow(S, cx, cy, r, a0, a1, size=2.25):
    """Clockwise arc from a0 to a1 (degrees) with an open arrowhead at the a1 end."""
    tip = polar(cx, cy, r, a1)
    return [line(arc(cx, cy, r, a0, a1)), line(poly(arrow_head(*tip, a1 + 90, size), r=S.r * 0.5))]


def drop_d(S, cx, cy, s=1.0):
    """Water drop with its point at (cx, cy - 7.5 s) and body centred on (cx, cy)."""
    d = L(S, "M12 2.5C12 2.5 16.5 7.5 16.5 10.5A4.5 4.5 0 0 1 7.5 10.5C7.5 7.5 12 2.5 12 2.5Z",
          "M11.3 3.3Q12 2.5 12.7 3.3C13.9 4.8 16.5 8 16.5 10.5A4.5 4.5 0 0 1 7.5 10.5C7.5 8 10.1 4.8 11.3 3.3Z")
    return _tx(d, s, cx - 12, cy - 10.5, 12, 10.5)


def calendar(S, x=3, y=4.5, w=18, h=16.5):
    """Calendar page with a header rule and two binder rings."""
    return [shell(rect(x, y, w, h, min(S.R, 2.5))), detail(seg(x, y + 4.5, x + w, y + 4.5)),
            line(seg(x + 4.5, y - 2, x + 4.5, y + 1.5)), line(seg(x + w - 4.5, y - 2, x + w - 4.5, y + 1.5))]


def thermo(S, x, top, bulb_y, level, w=4.0, br=3.5):
    """Thermometer: tube of width w from top to the bulb (centre bulb_y, radius br), column from level."""
    h = w / 2
    yj = bulb_y - math.sqrt(br * br - h * h)
    if S.name == "line":
        d = f"M{fmt(x - h)} {fmt(yj)}V{fmt(top)}H{fmt(x + h)}V{fmt(yj)}A{fmt(br)} {fmt(br)} 0 1 1 {fmt(x - h)} {fmt(yj)}Z"
    else:
        d = (f"M{fmt(x - h)} {fmt(yj)}V{fmt(top + h)}A{fmt(h)} {fmt(h)} 0 0 1 {fmt(x + h)} {fmt(top + h)}"
             f"V{fmt(yj)}A{fmt(br)} {fmt(br)} 0 1 1 {fmt(x - h)} {fmt(yj)}Z")
    parts = [shell(d)]
    if level is not None:
        parts.append(detail(seg(x, level, x, bulb_y - 1)))
    parts.append(dot(x, bulb_y, br / 2))
    return parts


def reed(x, y0, y1, hh=3.0):
    """Cattail: a stem from y0 up to y1 with a solid seed head on top."""
    return [line(seg(x, y0, x, y1 + hh)), mark(ellipse(x, y1 + hh / 2 + 0.3, 1.4, hh / 2 + 0.3))]


def sprout(S, x, y, h=6, s=1.0):
    """Seedling rising from (x, y): a stem and two leaves."""
    return [line(seg(x, y, x, y - h)), line(leaf(x, y - h * 0.55, x - 4 * s, y - h * 0.55 - 2.4 * s, -1.0 * s)),
            line(leaf(x, y - h * 0.8, x + 4 * s, y - h * 0.8 - 2.4 * s, 1.0 * s))]


def tree(S, cx, top, bot, r):
    """Round tree: canopy circle of radius r with its top at `top`, and a trunk down to `bot`."""
    cy = top + r
    return [shell(circle(cx, cy, r)), line(seg(cx, cy + r, cx, bot))]


def house_body(S, x0, x1, eave, base, peak):
    """Gabled house outline as a single polygon."""
    xm = (x0 + x1) / 2
    return poly([(x0, eave), (xm, peak), (x1, eave), (x1, base), (x0, base)], closed=True, r=S.r)


def person(S, cx, head_y=5.5, body_top=10.5, base=21, hw=7.5):
    """Bust of a person: a head and rounded shoulders."""
    r = L(S, 1.5, 4)
    d = (f"M{fmt(cx - hw)} {fmt(base)}V{fmt(body_top + r)}A{r} {r} 0 0 1 {fmt(cx - hw + r)} {fmt(body_top)}"
         f"H{fmt(cx + hw - r)}A{r} {r} 0 0 1 {fmt(cx + hw)} {fmt(body_top + r)}V{fmt(base)}Z")
    return [shell(circle(cx, head_y, 3.2)), shell(d)]


def bolt(S, pts):
    return line(poly(pts, r=S.r), stroke_miterlimit="8")


# ============================================================================ restoration and ecology

@icon("wetland-restoration", CAT, "Two reeds and a young sprout rising from water.",
      tags=["wetland", "restoration", "reeds", "marsh", "rewetting", "conservation", "habitat"])
def _(S):
    return [*reed(6.5, 16, 4), *reed(11.5, 16, 7.5), *sprout(S, 17.5, 16, 6), line(wave(2, 22, 19.5, 1.2, 3))]


@icon("coral-restoration", CAT, "Branching coral growing out of a small mounting frame.",
      tags=["coral", "reef", "restoration", "coral nursery", "marine", "conservation", "frag"])
def _(S):
    return [shell(rect(3, 16, 18, 5.5, L(S, 0.5, 2.5))), detail(seg(9, 16.5, 9, 21)), detail(seg(15, 16.5, 15, 21)),
            line(seg(12, 16.5, 12, 5.5)), line(seg(12, 13, 7.5, 9)), line(seg(12, 11.5, 16.5, 7.5)),
            dot(12, 4.5, 1.6), dot(6.8, 8.3, 1.6), dot(17.2, 6.8, 1.6)]


@icon("biodiversity", CAT, "Circle split in three, holding a leaf, a fish and a bird.",
      tags=["biodiversity", "species", "life", "nature", "variety", "ecology", "wildlife"])
def _(S):
    cx, cy, R = 12, 12, 9.5
    return [shell(circle(cx, cy, R)),
            *[detail(seg(*polar(cx, cy, L(S, 0, 2.5), a), *polar(cx, cy, R, a))) for a in (-90, 30, 150)],
            mark(leaf(14.2, 10, 17.5, 5.8, 1.0)),
            mark(ellipse(10.8, 17.3, 2.2, 1.3)), mark(poly([(13, 17.3), (14.5, 16.2), (14.5, 18.4)], closed=True)),
            mark("M5.8 8.6Q7 6.2 8.2 8.2Q9.4 6.2 10.6 8.6L10 8.9Q9.4 7.8 8.2 9.6Q7 7.8 6.4 8.9Z")]


@icon("ecosystem", CAT, "Small tree inside two curved arrows chasing each other in a cycle.",
      tags=["ecosystem", "cycle", "balance", "nature", "environment", "circular", "ecology"])
def _(S):
    return [*arc_arrow(S, 12, 12, 9, 200, 340, 2.25), *arc_arrow(S, 12, 12, 9, 20, 160, 2.25),
            shell(poly([(12, 6), (15.5, 12.5), (8.5, 12.5)], closed=True, r=S.r)), line(seg(12, 12.5, 12, 16))]


@icon("hedgerow", CAT, "Long low bushy hedge with a scalloped top above two rows of field furrows.",
      tags=["hedgerow", "hedge", "field boundary", "countryside", "bushes", "wildlife corridor", "farmland"])
def _(S):
    body = union(rect(2.5, 11, 19, 5.5, 0), circle(7, 11, 3), circle(12.5, 9.5, 4), circle(17.5, 11.5, 3))
    return [shell(body), detail(seg(8, 13.5, 8.3, 13.5)), detail(seg(14, 13.5, 14.3, 13.5)),
            line(seg(2.5, 20, 21.5, 20)), line(seg(5, 23, 19, 23))][:-1]


@icon("wildlife-pond", CAT, "Oval pond with two reeds and a lily pad floating on the water.",
      tags=["pond", "wildlife pond", "garden pond", "water habitat", "reeds", "lily pad", "frog"])
def _(S):
    return [shell(ellipse(12, 17, 9.5, 4)), *reed(7.5, 16, 3.5, 3.5), *reed(11.5, 15.5, 5.5, 3.5),
            mark(ellipse(16.5, 17, 2.2, 1.0))]


@icon("peat-bog", CAT, "Stepped block of peat with grass tufts on top, brick-like cuts and a wavy puddle.",
      tags=["peat", "bog", "peatland", "moss", "wetland", "carbon store", "moor"])
def _(S):
    prof = poly([(3, 12.5), (13, 12.5), (13, 16.5), (21, 16.5), (21, 21), (3, 21)], closed=True, r=S.r * 0.5)
    tufts = []
    for x in (6, 10):
        tufts += [line(seg(x, 12.5, x - 1.6, 8.5)), line(seg(x, 12.5, x + 1.6, 8.5))]
    return [shell(prof), detail(seg(3, 16.5, 13, 16.5)), detail(seg(8, 16.5, 8, 21)), *tufts,
            line(wave(15, 21, 13, 0.7, 1))]


@icon("save-the-planet", CAT, "Globe with meridians held above a cupped open hand.",
      tags=["save the planet", "protect earth", "care", "environment", "globe", "hand", "sustainability"])
def _(S):
    hand = poly([(2, 14.5), (7, 14.5), (9.5, 17), (15.5, 17), (19.5, 14)], r=S.r)
    return [shell(circle(12, 8, 5.5)), detail(ellipse(12, 8, 2.3, 5.5)), detail(seg(6.5, 8, 17.5, 8)),
            line(hand), line(seg(4, 21, 14, 21))]


@icon("earth-hour", CAT, "Globe next to a wall light switch with its lever in the down position.",
      tags=["earth hour", "lights out", "switch off", "energy saving", "globe", "light switch", "climate action"])
def _(S):
    return [shell(circle(9, 12, 6.5)), detail(ellipse(9, 12, 2.6, 6.5)), detail(seg(2.5, 12, 15.5, 12)),
            shell(rect(17, 6.5, 5, 11, L(S, 0.5, 2.2))), dot(19.5, 14.5, 1.2)]


@icon("eco-warrior", CAT, "Person with a leaf on their chest.",
      tags=["eco warrior", "environmentalist", "activist", "green", "volunteer", "climate activist", "nature"])
def _(S):
    return [*person(S, 12), mark(leaf(10, 18.3, 14.5, 13.3, 1.5))]


def test_tube(S, x, top, bot, w):
    """Open-topped test tube: square bottom (Line) or round bottom (Rounded), plus its rim."""
    h = w / 2
    d = L(S, f"M{fmt(x - h)} {fmt(top)}V{fmt(bot)}H{fmt(x + h)}V{fmt(top)}",
          f"M{fmt(x - h)} {fmt(top)}V{fmt(bot - h)}A{fmt(h)} {fmt(h)} 0 0 0 {fmt(x + h)} {fmt(bot - h)}V{fmt(top)}")
    return [line(d), line(seg(x - h - 1.5, top, x + h + 1.5, top))]


@icon("environmental-scientist-kit", CAT, "Test tube holding a green leaf.",
      tags=["environmental science", "lab", "test tube", "leaf", "research", "sampling", "ecology"])
def _(S):
    return [*test_tube(S, 12, 3.5, 21, 8), mark(leaf(12, 18.3, 12, 11, 2.2))]


@icon("water-testing", CAT, "Test tube dipped into wavy water with a water drop beside it.",
      tags=["water testing", "water quality", "sample", "test tube", "lab", "purity", "river"])
def _(S):
    return [*test_tube(S, 11, 3.5, 21, 6), line(wave(2, 8, 13.5, 0.9, 1)), line(wave(14, 22, 13.5, 0.9, 1)),
            line(wave(2, 8, 18.5, 0.9, 1)), line(wave(14, 22, 18.5, 0.9, 1)),
            shell(drop_d(S, 18.5, 7, 0.5))]


@icon("air-monitoring-station", CAT, "Louvred instrument shelter with a peaked roof standing on two splayed legs.",
      tags=["air quality", "monitoring station", "sensor", "pollution monitor", "weather station", "measurement", "environment"])
def _(S):
    box = poly([(3.5, 8), (12, 3.5), (20.5, 8), (20.5, 16), (3.5, 16)], closed=True, r=S.r)
    return [shell(box), detail(seg(7, 11, 17, 11)), detail(seg(7, 13.5, 17, 13.5)),
            line(seg(7, 16, 5.5, 21.5)), line(seg(17, 16, 18.5, 21.5))]


@icon("nature-trail-sign", CAT, "Arrow-shaped wooden signpost on a post with a leaf on the sign.",
      tags=["nature trail", "trail sign", "signpost", "hiking", "footpath", "leaf", "waymarker"])
def _(S):
    sign = poly([(3, 5.5), (17, 5.5), (21.5, 10), (17, 14.5), (3, 14.5)], closed=True, r=S.r)
    return [shell(sign), mark(leaf(7, 12, 13, 8, 1.4)), line(seg(8, 14.5, 8, 21.5)), line(seg(5, 21.5, 11, 21.5))]


@icon("thundersnow", CAT, "Cloud with a lightning bolt on one side and a snowflake on the other beneath it.",
      tags=["thundersnow", "snow storm", "thunder", "lightning", "snow", "winter storm", "weather"])
def _(S):
    return [shell(cloud(S, 0.72, 0, -3.5)), bolt(S, [(9.8, 14.5), (7.2, 18), (10.2, 18), (8, 21.5)]),
            *flake(S, 16, 18, 3)]


@icon("breezy-day", CAT, "Small sun in the upper corner with a curling wind line and two short gusts beneath it.",
      tags=["breezy", "windy day", "light wind", "breeze", "sun", "wind", "weather"])
def _(S):
    rays = sun_rays(8, 7, 4.6, 5.8)
    return [shell(circle(8, 7, 2.6)), *[line(r) for r in rays],
            line("M4 14.5H15.5A2.5 2.5 0 1 0 13 12"), line(seg(3, 19.5, 12, 19.5)), line(seg(15.5, 19.5, 20, 19.5))]


@icon("tornado-siren", CAT, "Megaphone-style horn siren on a tall pole with sound arcs radiating out.",
      tags=["tornado siren", "warning siren", "alert", "emergency", "horn", "civil defense", "storm warning"])
def _(S):
    horn = poly([(4, 5.5), (9, 5.5), (14, 3), (14, 13), (9, 10.5), (4, 10.5)], closed=True, r=S.r)
    return [shell(horn), line(arc(14, 8, 4, -50, 50)), line(arc(14, 8, 8, -45, 45)),
            line(seg(7, 10.5, 7, 21.5)), line(seg(4, 21.5, 10, 21.5))]


@icon("hurricane-shutters", CAT, "Window covered by a corrugated storm panel with a bolt in each corner.",
      tags=["hurricane shutters", "storm shutters", "window protection", "storm panel", "hurricane prep", "bolts", "corrugated"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(wave(3, 21, 9.5, 1.1, 3)), detail(wave(3, 21, 14.5, 1.1, 3)),
            dot(6.5, 6, 1), dot(17.5, 6, 1), dot(6.5, 18, 1), dot(17.5, 18, 1)]


@icon("snow-fence", CAT, "Slatted fence with a sloping snow drift piled against one side.",
      tags=["snow fence", "snowdrift", "windbreak", "winter", "barrier", "slats", "blizzard"])
def _(S):
    drift = "M2.5 21C6.5 21 8.5 14 13 14V21Z"
    return [shell(drift), line(seg(13, 4, 13, 14)), line(seg(18, 4, 18, 21)), line(seg(13, 7.5, 21.5, 7.5)),
            line(seg(13, 12, 21.5, 12)), line(seg(13, 21.5, 21.5, 21.5))]


@icon("hand-crank-radio", CAT, "Small radio with an antenna, a speaker circle, dial bars and a crank arm on top.",
      tags=["hand crank radio", "emergency radio", "wind-up radio", "survival", "weather radio", "preparedness", "off grid"])
def _(S):
    return [shell(rect(3, 9, 18, 12, min(S.R, 2.5))), detail(circle(8.5, 15, 2.6)), detail(seg(14, 13.5, 17.5, 13.5)),
            detail(seg(14, 16.5, 17.5, 16.5)), line(seg(17, 9, 20, 3)),
            line(poly([(7, 9), (7, 4.5), (3.5, 4.5)], r=S.r * 0.6)), dot(3.5, 4.5, 1.3)]


@icon("snow-day", CAT, "Calendar page with a large snowflake in place of the date.",
      tags=["snow day", "school closure", "closed", "winter", "snowflake", "calendar", "cancelled"])
def _(S):
    cx, cy, R = 12, 15.2, 3.7
    return [*calendar(S), *[detail(seg(*polar(cx, cy, R, a), *polar(cx, cy, R, a + 180))) for a in (-90, -30, 30)]]


@icon("sun-path", CAT, "Dotted arc over a horizon line with three sun positions along it.",
      tags=["sun path", "solar path", "sun position", "sunrise sunset", "solar noon", "daylight", "horizon"])
def _(S):
    cx, cy, R = 12, 19, 9.5
    suns = [205, 270, 335]
    dots = [232, 251, 289, 308]
    return [line(seg(2, 19, 22, 19)), *[solid(circle(*polar(cx, cy, R, a), 2)) for a in suns],
            *[dot(*polar(cx, cy, R, a), 0.9) for a in dots]]


@icon("window-thermometer", CAT, "Round dial thermometer with a needle, held to the glass by a suction cup below.",
      tags=["window thermometer", "outdoor thermometer", "dial thermometer", "suction cup", "temperature", "weather", "gauge"])
def _(S):
    return [shell(circle(12, 9, 6.5)), detail(seg(12, 9, 15.2, 5.8)), dot(12, 9, 1.3),
            line(seg(12, 15.5, 12, 17.5)), shell("M7 21.5A5 4.3 0 0 1 17 21.5Z")]


@icon("soil-thermometer", CAT, "Round dial gauge on top of a long probe pushed into a line of soil.",
      tags=["soil thermometer", "ground temperature", "probe", "gardening", "compost", "soil temperature", "agriculture"])
def _(S):
    return [shell(circle(12, 6, 4.5)), detail(seg(12, 6, 14.2, 3.8)), dot(12, 6, 1),
            line(seg(12, 10.5, 12, 21.5)), line(seg(2.5, 14.5, 9, 14.5)), line(seg(15, 14.5, 21.5, 14.5)),
            dot(5.5, 19, 1), dot(18.5, 18.5, 1)]


@icon("payday", CAT, "Calendar page with a coin on it.",
      tags=["payday", "salary", "pay date", "wages", "income", "calendar", "coin"])
def _(S):
    return [*calendar(S), detail(circle(12, 15.2, 3.5)), dot(12, 15.2, 1)]


@icon("work-week", CAT, "Calendar page with a row of seven dots, the first five solid.",
      tags=["work week", "weekdays", "five days", "monday to friday", "schedule", "business days", "calendar"])
def _(S):
    cal = calendar(S, 2, 4.5, 20, 16.5)
    return [*cal, *[dot(4.9 + k * 2.4, 14.5, 0.95) for k in range(5)], *[dot(4.9 + k * 2.4, 14.5, 0.5) for k in (5, 6)]]


@icon("timestamp", CAT, "Rubber stamp with a small clock face on its knob and a printed line below.",
      tags=["timestamp", "time stamp", "date stamp", "log time", "rubber stamp", "clock", "record"])
def _(S):
    return [shell(circle(12, 6, 4)), detail(seg(12, 6, 12, 4)), detail(seg(12, 6, 13.6, 6)),
            line(seg(12, 10, 12, 13)), shell(rect(4.5, 13, 15, 4.5, min(S.R, 2))), line(seg(5, 21, 19, 21))]


@icon("siesta", CAT, "Hammock slung between two posts with a sun above it.",
      tags=["siesta", "afternoon nap", "rest", "hammock", "sun", "relax", "midday"])
def _(S):
    rays = sun_rays(12, 6, 3.3, 4.4)
    return [shell(circle(12, 6, 2)), *[line(r) for r in rays], line(seg(3.5, 10.5, 3.5, 21.5)),
            line(seg(20.5, 10.5, 20.5, 21.5)), shell("M3.5 12.5Q12 24 20.5 12.5Q12 16.5 3.5 12.5Z")]


@icon("rain-garden", CAT, "Downspout pouring a drop into a bowl-shaped planted bed with two reeds.",
      tags=["rain garden", "bioswale", "stormwater", "downspout", "planted basin", "runoff", "sustainable drainage"])
def _(S):
    return [line(poly([(5, 3), (5, 10.5), (8.4, 10.5)], r=S.r)), mark(drop_d(S, 8.4, 15, 0.45)),
            line("M2.5 15.5Q12 25 21.5 15.5"), *reed(13.5, 19, 8, 3), *reed(17.5, 18, 10, 3)]


@icon("permeable-paving", CAT, "Paving slab split into blocks by joints, with drops falling through the joints into waves below.",
      tags=["permeable paving", "porous paving", "pavers", "drainage", "stormwater", "infiltration", "sustainable urban drainage"])
def _(S):
    return [shell(rect(2.5, 3.5, 19, 7, min(S.R, 2))), detail(seg(9, 3.5, 9, 10.5)), detail(seg(15, 3.5, 15, 10.5)),
            dot(9, 14.3, 1), dot(15, 14.3, 1), line(wave(2.5, 21.5, 19.5, 1.2, 3))]


@icon("urban-heat-island", CAT, "City skyline of three buildings with a thermometer rising beside it.",
      tags=["urban heat island", "city heat", "heat", "thermometer", "skyline", "climate", "hot city"])
def _(S):
    sky = poly([(2, 21), (2, 13), (5.5, 13), (5.5, 5.5), (10.5, 5.5), (10.5, 11), (13.5, 11), (13.5, 21)], closed=True,
               r=S.r * 0.5)
    return [shell(sky), mark(rect(7, 8.5, 1.6, 1.6)), mark(rect(7, 12.5, 1.6, 1.6)), *thermo(S, 18.5, 3, 18.5, 9.5, w=3, br=2.5)]


def _bounce(S, x, y, deg, length=6.5, size=2.0):
    tip = polar(x, y, length, deg)
    return [line(seg(x, y, *tip)), line(poly(arrow_head(*tip, deg, size), r=S.r * 0.5))]


@icon("cool-roof", CAT, "House with two arrows bouncing away from its roof slopes.",
      tags=["cool roof", "reflective roof", "heat reflection", "solar reflectance", "roof", "energy saving", "white roof"])
def _(S):
    house = poly([(3, 21.5), (3, 15.5), (12, 10), (21, 15.5), (21, 21.5)], closed=True, r=S.r)
    return [shell(house), detail(seg(9.5, 21.5, 9.5, 18)), detail(seg(14.5, 21.5, 14.5, 18)),
            *_bounce(S, 7, 11.5, -115), *_bounce(S, 17, 11.5, -65)]


@icon("shade-tree", CAT, "Leafy tree beside a small house, with diagonal shade lines across the house wall.",
      tags=["shade tree", "tree shade", "cooling", "shadow", "house", "energy saving", "canopy"])
def _(S):
    house = poly([(12.5, 21), (12.5, 12.5), (17, 8.5), (21.5, 12.5), (21.5, 21)], closed=True, r=S.r * 0.6)
    canopy = union(circle(4.8, 9, 2.8), circle(8.3, 7, 3.6), circle(9.2, 10.5, 2.8), circle(5.8, 5.8, 2.6))
    return [shell(canopy), line(seg(7, 13, 7, 21.5)), shell(house), detail(seg(15.5, 21, 21.5, 15)),
            detail(seg(15.5, 17, 18.5, 14))]


@icon("water-footprint", CAT, "Large water drop holding a footprint inside it.",
      tags=["water footprint", "water use", "virtual water", "consumption", "drop", "footprint", "sustainability"])
def _(S):
    return [shell(drop_d(S, 12, 14.5, 1.6)), mark(ellipse(12.3, 17.4, 2.2, 3.1)),
            *[mark(circle(x, y, 0.9)) for x, y in ((9.3, 13.2), (11.2, 12.2), (13.3, 12.2), (15, 13.2))]]


@icon("peak-demand", CAT, "Round dial with a sharp spike line crossing it and a bolt mark in the corner.",
      tags=["peak demand", "peak load", "electricity", "spike", "grid", "energy demand", "power usage"])
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(poly([(5.5, 14.5), (9, 14.5), (12, 6.5), (15, 17), (18.5, 17)], r=S.r * 0.6))]


@icon("power-outage", CAT, "House with dark windows and a broken lightning bolt beside it.",
      tags=["power outage", "blackout", "power cut", "electricity", "no power", "lightning", "grid failure"])
def _(S):
    house = poly([(2.5, 21), (2.5, 12), (8.5, 7), (14.5, 12), (14.5, 21)], closed=True, r=S.r)
    return [shell(house), mark(rect(5.5, 13.5, 3, 3.5)), mark(rect(9.5, 13.5, 3, 3.5)),
            line(poly([(20, 2.5), (17.5, 8), (20.5, 8)], r=S.r * 0.5)), line(poly([(18.5, 12.5), (21, 12.5), (18.5, 18)], r=S.r * 0.5))]


def turtle_d():
    """Top view of a sea turtle (for a solid mark) centred on (12, 12)."""
    body = ellipse(12, 12.5, 3.4, 4.2)
    head = circle(12, 7.1, 1.5)
    fl = [rot(ellipse(7.6, 9.6, 2.3, 1.0), 35, 7.6, 9.6), rot(ellipse(16.4, 9.6, 2.3, 1.0), -35, 16.4, 9.6),
          rot(ellipse(8.4, 15.6, 1.6, 0.9), -35, 8.4, 15.6), rot(ellipse(15.6, 15.6, 1.6, 0.9), 35, 15.6, 15.6)]
    return union(body, head, *fl)


@icon("bycatch", CAT, "Fishing net bag holding a sea turtle and a small fish.",
      tags=["bycatch", "fishing net", "sea turtle", "incidental catch", "overfishing", "marine conservation", "trawl"])
def _(S):
    bag = L(S, "M3 4.5H21C21 13 17 21.5 12 21.5C7 21.5 3 13 3 4.5Z",
            "M5 4.5H19Q21 4.5 21 6.5C21 14 17 21.5 12 21.5C7 21.5 3 14 3 6.5Q3 4.5 5 4.5Z")
    return [shell(bag), mark(_tx(turtle_d(), 0.8, 0, -1.6)), mark(ellipse(10.6, 18, 1.5, 0.9)),
            mark(poly([(12, 18), (13.4, 17), (13.4, 19)], closed=True))]


@icon("monoculture", CAT, "Two neat rows of identical pine trees planted in a rigid grid.",
      tags=["monoculture", "single crop", "plantation", "uniform", "forestry", "farming", "biodiversity loss"])
def _(S):
    parts = []
    for y in (3.5, 13.5):
        for x in (5.5, 12, 18.5):
            parts.append(solid(poly([(x, y), (x + 3.6, y + 5.2), (x - 3.6, y + 5.2)], closed=True, r=S.r * 0.7)))
            parts.append(line(seg(x, y + 5.2, x, y + 6.6)))
    return parts


@icon("green-data-center", CAT, "Server rack of three units with status lights, a leaf in the bottom unit.",
      tags=["green data center", "sustainable computing", "server", "eco hosting", "renewable", "low carbon", "cloud"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 19, min(S.R, 2))), detail(seg(4.5, 8.5, 19.5, 8.5)), detail(seg(4.5, 14.5, 19.5, 14.5)),
            mark(circle(8, 5.5, 1)), mark(circle(8, 11.5, 1)), detail(seg(11.5, 5.5, 16, 5.5)), detail(seg(11.5, 11.5, 16, 11.5)),
            mark(leaf(9.3, 19.6, 14.7, 16.0, 1.3))]


def chord(cx, cy, r, dy):
    h = math.sqrt(max(r * r - dy * dy, 0))
    return seg(cx - h, cy + dy, cx + h, cy + dy)


def vchord(cx, cy, r, dx):
    h = math.sqrt(max(r * r - dx * dx, 0))
    return seg(cx + dx, cy - h, cx + dx, cy + h)


@icon("climate-model", CAT, "Globe covered in a square grid mesh with a thermometer beside it.",
      tags=["climate model", "simulation", "global warming", "forecast", "grid", "thermometer", "climate science"])
def _(S):
    cx, cy, r = 8.5, 12, 6.5
    return [shell(circle(cx, cy, r)), *[detail(chord(cx, cy, r, dy)) for dy in (-3.3, 0, 3.3)],
            *[detail(vchord(cx, cy, r, dx)) for dx in (-3.3, 0, 3.3)], *thermo(S, 19.5, 3, 18, 8.5, w=3, br=2.5)]


@icon("water-scarcity", CAT, "Tap with a single cracked drop falling from its spout.",
      tags=["water scarcity", "drought", "water shortage", "dry tap", "no water", "conservation", "last drop"])
def _(S):
    return [line(poly([(2, 6), (15, 6), (15, 8.5)], r=S.r)), line(seg(8.5, 6, 8.5, 3)), line(seg(6, 3, 11, 3)),
            shell(drop_d(S, 15, 17, 0.9)), detail(poly([(14.3, 14.5), (15.8, 16.5), (14.6, 18.3)], r=0))]


@icon("desalination-plant", CAT, "Waves flowing into a tank with an outlet pipe on the right ending in a drop.",
      tags=["desalination", "desalination plant", "seawater", "fresh water", "reverse osmosis", "water treatment", "drinking water"])
def _(S):
    return [line(wave(2, 7, 13, 0.9, 1)), line(wave(2, 7, 18, 0.9, 1)), shell(rect(9, 5, 7, 15, min(S.R, 2))),
            detail(wave(9, 16, 13, 0.8, 1)), line(poly([(16, 8.5), (20, 8.5), (20, 12)], r=S.r)),
            mark(drop_d(S, 20, 17.5, 0.5))]


@icon("agrivoltaics", CAT, "Raised solar panel on two posts above a young crop plant.",
      tags=["agrivoltaics", "agrovoltaics", "solar farming", "dual use", "solar panel", "crops", "renewable energy"])
def _(S):
    panel = poly([(2.5, 9), (5.5, 3), (21.5, 3), (18.5, 9)], closed=True, r=S.r * 0.6)
    return [shell(panel), detail(seg(12, 3, 9.5, 9)), line(seg(6, 9, 6, 21.5)), line(seg(18, 9, 18, 21.5)),
            *sprout(S, 12, 21.5, 6.5, 0.9)]


@icon("floating-solar", CAT, "Tilted solar panel resting on two floats above wavy water.",
      tags=["floating solar", "floatovoltaics", "solar panel", "reservoir", "lake", "renewable energy", "water"])
def _(S):
    panel = poly([(3, 12), (7, 4), (21, 4), (17, 12)], closed=True, r=S.r * 0.6)
    return [shell(panel), detail(seg(14, 4, 10, 12)), line(seg(8, 12, 8, 15.5)), line(seg(15, 12, 15, 15.5)),
            line(wave(2, 22, 18.5, 1.1, 3))]


@icon("ground-source-heat-pump", CAT, "House with a U-shaped buried pipe loop running down into the ground beneath it.",
      tags=["ground source heat pump", "geothermal", "heat pump", "ground loop", "heating", "renewable energy", "pipe"])
def _(S):
    house = poly([(3.5, 8), (12, 2.5), (20.5, 8), (20.5, 12), (3.5, 12)], closed=True, r=S.r)
    return [shell(house), line("M8 12V19A2 2 0 0 0 12 19V15A2 2 0 0 1 16 15V12")]


@icon("clothing-swap", CAT, "Two shirts with a pair of curved arrows exchanging between them.",
      tags=["clothing swap", "clothes swap", "swap shop", "secondhand", "clothing exchange", "reuse", "circular fashion"])
def _(S):
    def tee(x, y):
        pts = [(0, 2), (3, 0), (4.3, 1.2), (7.7, 1.2), (9, 0), (12, 2), (10.5, 5), (9, 4.3), (9, 10.5), (3, 10.5), (3, 4.3), (1.5, 5)]
        return poly([(x - 1 + px * 0.9, y + py * 0.9) for px, py in pts], closed=True, r=S.r * 0.4)
    return [shell(tee(2, 2.5)), shell(tee(11.5, 12.5)),
            line("M13 5Q19 5 19 10"), line(poly(arrow_head(19, 10.5, 90, 1.8), r=S.r * 0.4)),
            line("M11 19Q5 19 5 14"), line(poly(arrow_head(5, 13.5, -90, 1.8), r=S.r * 0.4))]


@icon("bokashi-bin", CAT, "Lidded bucket with a small tap near its base and a leaf on its side.",
      tags=["bokashi", "bokashi bin", "composting", "fermentation", "food waste", "kitchen compost", "bucket"])
def _(S):
    body = poly([(5, 8.5), (19, 8.5), (17.5, 21), (6.5, 21)], closed=True, r=S.r * 0.6)
    return [shell(body), shell(rect(4, 4.5, 16, 4, min(S.R, 1.5))), mark(leaf(9.5, 18, 14.5, 12.2, 1.7)),
            line(poly([(18, 18), (21.5, 18), (21.5, 20.5)], r=S.r * 0.5))]


def _p(p):
    return f"{fmt(p[0])} {fmt(p[1])}"


def _tip(a, p, b, r):
    """Corner at p (from a towards b): sharp when r == 0, softened with a quadratic when r > 0."""
    if r <= 0:
        return "L" + _p(p)
    def toward(q, t):
        dx, dy = q[0] - p[0], q[1] - p[1]
        n = math.hypot(dx, dy)
        return (p[0] + dx / n * t, p[1] + dy / n * t)
    a1, b1 = toward(a, r), toward(b, r)
    return f"L{_p(a1)}Q{_p(p)} {_p(b1)}"


@icon("wildlife-rescue", CAT, "Small songbird with a bandage band around its body, resting in a cupped hand.",
      tags=["wildlife rescue", "animal rescue", "injured bird", "rehabilitation", "care", "bandage", "sanctuary"])
def _(S):
    r = L(S, 0, 1.2)
    d = ("M15 4.5C17 4.5 18.5 5.8 18.8 7.4" + _tip((18.8, 7.4), (21.5, 8.6), (18.7, 9.9), r)
         + "L18.7 9.9C18.5 14.5 15.5 18 11 18.3" + _tip((11, 18.3), (3.5, 19.5), (7.8, 14.3), r)
         + "L7.8 14.3C10 12.5 11 10.5 11.3 8.5C11.6 6 13 4.5 15 4.5Z")
    k = dict(s=0.72, dx=0, dy=-3.5)
    band = "M10.6 10.4L13.6 9.8L14.8 16.6L11.6 17.4Z"
    return [shell(_tx(d, **k)), mark(_tx(band, **k)), line("M3 15C3 19 7 21.5 12 21.5C17 21.5 21 19 21 15")]


@icon("solar-pump", CAT, "Small solar panel wired to a pump whose spout pours water into a trough.",
      tags=["solar pump", "solar water pump", "irrigation", "livestock water", "trough", "renewable energy", "off grid"])
def _(S):
    panel = poly([(2.5, 8), (5.5, 2.5), (14, 2.5), (11, 8)], closed=True, r=S.r * 0.6)
    return [shell(panel), line(seg(6.5, 8, 6.5, 12)), shell(rect(2.5, 12, 8, 8, min(S.R, 2))),
            line(poly([(10.5, 14), (17, 14), (17, 15.5)], r=S.r)), mark(drop_d(S, 17, 17, 0.32)),
            line(poly([(13, 18.5), (13, 21.5), (22, 21.5), (22, 18.5)], r=S.r * 0.5))]


@icon("drip-torch", CAT, "Fuel canister with a handle and a long curved spout ending in a small flame.",
      tags=["drip torch", "prescribed burn", "controlled burn", "wildfire", "fire management", "fuel", "forestry"])
def _(S):
    flame = "M19.5 1.8C21 3.8 22 5 22 6.3A2.5 2.5 0 0 1 17 6.3C17 5 18.3 3.8 19.5 1.8Z"
    return [shell(rect(3.5, 10, 10, 11.5, min(S.R, 2))), line(poly([(6, 10), (6, 6), (11, 6), (11, 10)], r=S.r * 0.6)),
            line(poly([(13.5, 13), (19.5, 13), (19.5, 9)], r=S.r)), mark(flame)]


@icon("energy-consumption", CAT, "Electric plug beside three rising bars of a chart.",
      tags=["energy consumption", "power usage", "electricity use", "plug", "bar chart", "meter", "kwh"])
def _(S):
    return [line(seg(4.5, 2.5, 4.5, 6.5)), line(seg(8.5, 2.5, 8.5, 6.5)), shell(rect(2.5, 6.5, 8, 6.5, min(S.R, 2))),
            line(seg(6.5, 13, 6.5, 21.5)), line(seg(14, 21.5, 14, 16.5)), line(seg(17.5, 21.5, 17.5, 12.5)),
            line(seg(21, 21.5, 21, 8))]


@icon("birthday-calendar", CAT, "Calendar page with a small cake and a lit candle on it.",
      tags=["birthday calendar", "birthday date", "anniversary", "celebration", "cake", "reminder", "calendar"])
def _(S):
    return [*calendar(S), detail(rect(7, 15, 10, 3.5, 0.8 if S.name == "rounded" else 0)), detail(seg(12, 12.3, 12, 15)),
            dot(12, 11.3, 0.8)]


@icon("hurricane-track", CAT, "Hurricane swirl at the narrow end of a dotted path inside a widening cone outline.",
      tags=["hurricane track", "storm track", "forecast cone", "cyclone", "path", "tropical storm", "landfall"])
def _(S):
    h = (6, 17.5)
    def at(rr, a):
        return polar(*h, rr, a)
    return [shell(circle(*h, 2.6)), dot(*h, 0.8),
            line(arc(*h, 4.8, 20, 80)), line(arc(*h, 4.8, 200, 260)),
            line(seg(*at(4.9, -62), *at(17, -62))), line(seg(*at(4.9, -22), *at(17, -22))),
            *[dot(*at(r, -42), 0.9) for r in (9, 12.5, 16)]]


@icon("fog-harvesting", CAT, "Diamond mesh net stretched between two poles with a drop collecting into a trough below.",
      tags=["fog harvesting", "fog catcher", "water collection", "mesh net", "cloud forest", "drinking water", "fog net"])
def _(S):
    return [shell(rect(5, 2.5, 14, 9, 0)), detail(seg(5, 11.5, 14, 2.5)), detail(seg(10, 11.5, 19, 2.5)),
            detail(seg(5, 2.5, 14, 11.5)), detail(seg(10, 2.5, 19, 11.5)),
            line(seg(5, 11.5, 5, 18)), line(seg(19, 11.5, 19, 18)),
            mark(drop_d(S, 12, 15.2, 0.38)), shell(poly([(5, 18), (19, 18), (17.5, 21.5), (6.5, 21.5)], closed=True, r=S.r * 0.5))]


@icon("eco-mode", CAT, "Half-circle gauge with its needle at the low end and a leaf above the hub.",
      tags=["eco mode", "economy mode", "eco driving", "low power", "energy saving", "green", "gauge"])
def _(S):
    return [line(arc(12, 17.5, 9, 180, 360)), line(seg(12, 17.5, 6.2, 15)), dot(12, 17.5, 1.6),
            mark(leaf(12, 14, 12, 10, 1.5))]


@icon("tree-hug", CAT, "Person with their head to one side and both arms wrapped around a tree trunk.",
      tags=["tree hug", "tree hugger", "nature lover", "forest", "environmentalist", "embrace", "conservation"])
def _(S):
    canopy = union(circle(14.5, 6, 3.8), circle(18, 7.5, 3), circle(11.5, 7.5, 3))
    return [shell(canopy), line(seg(13, 11, 13, 21.5)), line(seg(17, 11, 17, 21.5)),
            shell(circle(5.5, 7.5, 2.4)), line(seg(5.5, 10.5, 5.5, 21.5)), line(seg(5.5, 14, 19.5, 14)), dot(19.5, 14, 1.3)]


@icon("snowmelt", CAT, "Snow mound with drips falling from its edge into a wavy stream below.",
      tags=["snowmelt", "thaw", "melting snow", "spring runoff", "meltwater", "stream", "warming"])
def _(S):
    mound = "M3 14.5C3 9.5 7 6.5 11 6.5C15 6.5 19 9.5 19 14.5Z"
    return [shell(mound), dot(6.5, 17.5, 1), dot(11, 17.5, 1), dot(15.5, 17.5, 1), line(wave(2, 22, 21, 0.8, 3))]


def ban(S, cx=12, cy=12, r=9.5):
    """Prohibition ring with a diagonal slash."""
    a, b = polar(cx, cy, r, 135), polar(cx, cy, r, -45)
    return [shell(circle(cx, cy, r)), detail(seg(*a, *b))]


@icon("anti-poaching", CAT, "Shield holding an elephant head seen from the front with big ears and a trunk.",
      tags=["anti poaching", "wildlife protection", "ranger", "ivory", "elephant", "conservation", "shield"])
def _(S):
    shield = L(S, "M12 2.5L20 5.5V12C20 17 16 20.5 12 21.5C8 20.5 4 17 4 12V5.5Z",
               "M11.2 2.8Q12 2.5 12.8 2.8L19.3 5.2Q20 5.5 20 6.2V12C20 17 16 20.5 12.4 21.4Q12 21.5 11.6 21.4C8 20.5 4 17 4 12V6.2Q4 5.5 4.7 5.2Z")
    ele = union(circle(12, 10, 2.5), ellipse(7.9, 9.6, 1.9, 2.6), ellipse(16.1, 9.6, 1.9, 2.6),
                "M10.8 11H13.2L13 16.3A1 1 0 0 1 11 16.3Z")
    return [shell(shield), mark(ele)]


@icon("leave-no-trace", CAT, "Ring holding a footprint beside a leaf.",
      tags=["leave no trace", "outdoor ethics", "hiking", "low impact", "footprint", "leave nothing", "camping"])
def _(S):
    return [shell(circle(12, 12, 9.5)), mark(ellipse(9, 14.5, 1.9, 3)),
            *[mark(circle(x, y, 0.9)) for x, y in ((7.4, 9.6), (9.1, 8.8), (10.9, 9.2))],
            mark(L(S, leaf(13.2, 16.2, 17.6, 8.8, 1.6), rot(ellipse(15.4, 12.5, 1.9, 4.6), 30, 15.4, 12.5)))]


@icon("no-littering", CAT, "Prohibition sign over a discarded drink cup with a lid and straw.",
      tags=["no littering", "no dumping", "keep clean", "do not litter", "trash", "rubbish", "prohibition"])
def _(S):
    cup = "M8.8 9.2H15.2L14.2 17.5H9.8Z"
    return [shell(circle(12, 12, 9.5)), mark(cup), mark(rect(8.2, 7.6, 7.6, 1.3, 0.4)), line(seg(12.5, 7.6, 13.6, 5)),
            detail(seg(*polar(12, 12, 9.5, 135), *polar(12, 12, 9.5, -45)))]


@icon("do-not-feed-wildlife", CAT, "Prohibition sign over a duck and a slice of bread.",
      tags=["do not feed wildlife", "no feeding", "feed ducks", "bread", "nature reserve", "park sign", "prohibition"])
def _(S):
    duck = union(ellipse(10.8, 12.8, 4.8, 2.9), circle(14.6, 8.6, 2.1),
                 L(S, "M16.4 8.2L19 9.1L16.4 9.9Z", ellipse(17.9, 9, 1.4, 0.8)))
    bread = L(S, "M14 17.6V13.2H18.2V17.6Z", "M14 17.6V15.4A1.3 1.3 0 0 1 14.6 13.1H17.6A1.3 1.3 0 0 1 18.2 15.4V17.6Z")
    return [shell(circle(12, 12, 9.5)), mark(duck), mark(bread), detail(seg(*polar(12, 12, 9.5, 135), *polar(12, 12, 9.5, -45)))]


@icon("hybrid-car", CAT, "Car side view with a leaf and a fuel drop above its roof.",
      tags=["hybrid car", "hybrid vehicle", "low emission", "eco car", "electric and petrol", "green transport", "fuel"])
def _(S):
    body = ("M2.5 19.5V16.5L6 15.3L8.6 11.5H15.4L18.2 15.3L21.5 16.5V19.5H19.7A2.6 2.6 0 0 0 14.5 19.5H9.5"
            "A2.6 2.6 0 0 0 4.3 19.5Z")
    body = L(S, body, body)
    return [shell(body), detail(seg(12, 11.5, 12, 15.3)), dot(7, 19.6, 1.5), dot(17, 19.6, 1.5),
            mark(leaf(6.5, 8.3, 10.8, 3, 1.6)), mark(drop_d(S, 16.5, 5.8, 0.42))]


@icon("snow-blower", CAT, "Walk-behind snow blower with an auger housing in front, a chute and thrown snow.",
      tags=["snow blower", "snow thrower", "snow removal", "winter", "driveway", "machine", "clearing snow"])
def _(S):
    return [shell(rect(2.5, 11.5, 4.5, 8.5, min(S.R, 1.5))), detail(seg(2.5, 15.75, 7, 15.75)),
            shell(rect(8, 9, 9, 6.5, min(S.R, 2))), line(poly([(11.5, 9), (11.5, 5), (16.5, 5)], r=S.r)),
            dot(19.5, 4, 0.9), dot(21, 6.5, 0.9), dot(19, 7.5, 0.9),
            line(poly([(17, 13.5), (21.5, 10.5)], r=0)), dot(12.5, 19.3, 1.9)]
