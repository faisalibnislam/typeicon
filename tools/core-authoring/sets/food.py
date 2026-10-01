"""TypeIcon Core: food & drink."""
import math
import re

from dsl import arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "food"


# --------------------------------------------------------------------------- local helpers

def xf(d, deg=0.0, cx=12.0, cy=12.0, dx=0.0, dy=0.0):
    """Rotate (clockwise on screen) about (cx, cy), then translate, an absolute d-string made of
    M/L/C/Q/Z and circular A commands."""
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    toks = re.findall(r"[MLCQAZHV]|-?\d*\.?\d+(?:e-?\d+)?", d)

    def tp(x, y):
        x, y = x - cx, y - cy
        return f"{fmt(cx + x * ca - y * sa + dx)} {fmt(cy + x * sa + y * ca + dy)}"

    out, i, cmd = [], 0, None
    while i < len(toks):
        t = toks[i]
        if t in "MLCQAZ":
            cmd = t
            out.append(t)
            i += 1
            continue
        if t in "HV":
            raise ValueError("xf: H/V not supported")
        if cmd == "A":
            rx, ry, rot, la, sw, x, y = toks[i:i + 7]
            rot = fmt(float(rot) + (deg if rx != ry else 0))
            out.append(f"{rx} {ry} {rot} {la} {sw} " + tp(float(x), float(y)))
            i += 7
        else:
            out.append(tp(float(toks[i]), float(toks[i + 1])))
            i += 2
    s = ""
    for t in out:
        s += t if (len(t) == 1 and t in "MLCQAZ") else (t if s and s[-1] in "MLCQAZ" else " " + t)
    return s


def leaf(x1, y1, x2, y2, bulge):
    """Closed pointed leaf from (x1, y1) to (x2, y2); bulge = half width."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    L = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / L, (x2 - x1) / L
    b = bulge * 2
    return (f"M{fmt(x1)} {fmt(y1)}Q{fmt(mx + nx * b)} {fmt(my + ny * b)} {fmt(x2)} {fmt(y2)}"
            f"Q{fmt(mx - nx * b)} {fmt(my - ny * b)} {fmt(x1)} {fmt(y1)}Z")


def layered_discs(discs, gap=1.75):
    """Filled design for overlapping round things: discs (cx, cy, r) back to front; each front disc
    is separated from those behind it by a knocked-out gap."""
    body = None
    for cx, cy, r in discs:
        r_out = r + 1
        if body is not None:
            body = D(body, P(circle(cx, cy, r_out + gap)))
        body = P(circle(cx, cy, r_out)) if body is None else U(body, P(circle(cx, cy, r_out)))
    return body


def ell_chord(cx, cy, rx, ry, c, kind, inset=0.0):
    """Chord of ellipse along x + y = c ('/') or x - y = c ('\\'), shortened by inset at both ends."""
    # parametrise: point = p0 + t * v
    if kind == "/":
        v = (1 / math.sqrt(2), -1 / math.sqrt(2))
        p0 = ((c - cy + cx) / 2, (c + cy - cx) / 2)
    else:
        v = (1 / math.sqrt(2), 1 / math.sqrt(2))
        p0 = ((c + cx + cy) / 2, (cx + cy - c) / 2)
    # solve ((p0x + t vx - cx)/rx)^2 + ((p0y + t vy - cy)/ry)^2 = 1
    ax, ay = (p0[0] - cx) / rx, (p0[1] - cy) / ry
    bx, by = v[0] / rx, v[1] / ry
    A = bx * bx + by * by
    B = 2 * (ax * bx + ay * by)
    C = ax * ax + ay * ay - 1
    disc = math.sqrt(B * B - 4 * A * C)
    t1, t2 = (-B - disc) / (2 * A) + inset, (-B + disc) / (2 * A) - inset
    return seg(p0[0] + t1 * v[0], p0[1] + t1 * v[1], p0[0] + t2 * v[0], p0[1] + t2 * v[1])


def rnd(S, line_val, rounded_val):
    return line_val if S.name == "line" else rounded_val


# =========================================================================== fruit

@icon("apple", CAT, "An apple with a stem and a leaf", tags=["fruit", "healthy", "snack", "produce"])
def _(S):
    body = ("M12 9C10.9 8.3 9.7 8 8.3 8C5.3 8 3.5 10.2 3.5 13.3C3.5 17.3 6.2 21 9 21"
            "C10.3 21 10.8 20.4 12 20.4C13.2 20.4 13.7 21 15 21C17.8 21 20.5 17.3 20.5 13.3"
            "C20.5 10.2 18.7 8 15.7 8C14.3 8 13.1 8.3 12 9Z")
    return [shell(body), line("M12 9C12 7 11.6 5.3 10.5 4"), shell(leaf(13.2, 5, 17.8, 3.2, 1.1))]


@icon("banana", CAT, "A curved banana", tags=["fruit", "yellow", "snack", "produce"])
def _(S):
    body = ("M17.5 5.5C19.5 8 19.8 12.5 17.5 16C15.2 19.5 10.5 21.2 5.5 20.5C4 20.3 3.6 19 5 18.5"
            "C9.5 17 13 14.5 14.5 10.5C15.2 8.6 15.3 7 15 5.5Z")
    return [shell(body), line(poly([(15, 5.5), (15.3, 3), (17.3, 3), (17.5, 5.5)], r=rnd(S, 0, 0.5)))]


@icon("cherry", CAT, "A pair of cherries joined at the stem", tags=["cherries", "fruit", "berry", "produce"])
def _(S):
    return [
        shell(circle(6.5, 17.5, 3)), shell(circle(17, 15.5, 3)),
        line("M6.5 14.5C7 10 9.5 6.5 13 3.5"), line("M17 12.5C16.5 8.5 15 5.5 13 3.5"),
        shell(leaf(12, 4, 5.5, 4.5, 1.3)),
    ]


GRAPES = [(7, 9, 2.5), (12, 9, 2.5), (17, 9, 2.5), (9.5, 13.5, 2.5), (14.5, 13.5, 2.5), (12, 18, 2.5)]


@icon("grapes", CAT, "A bunch of grapes", tags=["grape", "fruit", "vine", "wine", "produce"],
      filled=lambda: U(layered_discs(GRAPES, 1.0), ST("M12 5.5L12.5 3", 2.5)))
def _(S):
    return [*(shell(circle(*g)) for g in GRAPES), line("M12 6.5L12.5 3")]


LEMON = ("M3 12L4.8 10.6C6 7.8 8.8 6.5 12 6.5C15.2 6.5 18 7.8 19.2 10.6L21 12L19.2 13.4"
         "C18 16.2 15.2 17.5 12 17.5C8.8 17.5 6 16.2 4.8 13.4Z")


@icon("lemon", CAT, "A lemon with pointed ends", tags=["citrus", "fruit", "sour", "yellow", "produce"])
def _(S):
    return [shell(xf(LEMON, -35))]


@icon("orange", CAT, "A round orange with a leaf", tags=["citrus", "fruit", "tangerine", "produce"])
def _(S):
    return [shell(circle(12, 13.5, 7.5)), shell(leaf(12, 6, 17.5, 3, 1.3)),
            dot(15, 10.5, 1) if S.name == "line" else dot(15.2, 10.8, 1.1)]


@icon("pear", CAT, "A pear with a stem and a leaf", tags=["fruit", "produce", "healthy", "orchard"])
def _(S):
    body = ("M12 6.5C9.8 6.5 8.8 8.2 8.5 10.3C8.2 12.3 5 13.8 5 16.8C5 19.6 8 21 12 21"
            "C16 21 19 19.6 19 16.8C19 13.8 15.8 12.3 15.5 10.3C15.2 8.2 14.2 6.5 12 6.5Z")
    return [shell(body), line("M12 6.5C12 5 11.7 4 11 3"), shell(leaf(13.5, 5.5, 18, 4.5, 1.2))]


@icon("strawberry", CAT, "A strawberry with its leafy top", tags=["berry", "fruit", "produce"])
def _(S):
    body = "M12 21C7.5 19.5 4 14.5 4 11C4 9.2 5.2 8.5 7 8.5H17C18.8 8.5 20 9.2 20 11C20 14.5 16.5 19.5 12 21Z"
    crown = poly([(7, 8.5), (8.5, 5), (10.5, 6.2), (12, 3), (13.5, 6.2), (15.5, 5), (17, 8.5)], closed=True, r=rnd(S, 0, 0.6))
    return [shell(body), shell(crown), detail(seg(7, 8.5, 17, 8.5)),
            dot(9.5, 12.5, 1), dot(14.5, 12.5, 1), dot(12, 16, 1)]


@icon("watermelon", CAT, "A slice of watermelon", tags=["melon", "fruit", "summer", "slice", "produce"])
def _(S):
    top = 7.5
    return [shell(f"M3 {top}H21A9 9 0 0 1 3 {top}Z" if S.name == "line" else
                  f"M4.5 {top}H19.5A1.5 1.5 0 0 1 21 {top + 1.5}A9 9 0 0 1 3 {top + 1.5}A1.5 1.5 0 0 1 4.5 {top}Z"),
            detail(f"M17.5 {top}A5.5 5.5 0 0 1 6.5 {top}"),
            dot(10.3, 10.2, 0.9), dot(13.7, 10.2, 0.9)]


PINE_BODY = "M9.5 9H14.5C17 9 18 12 18 15C18 18.5 15.5 21 12 21C8.5 21 6 18.5 6 15C6 12 7 9 9.5 9Z"


@icon("pineapple", CAT, "A pineapple with its spiky crown", tags=["fruit", "tropical", "produce"])
def _(S):
    crown = poly([(9.5, 9), (7.5, 4), (10.5, 5.8), (12, 2.5), (13.5, 5.8), (16.5, 4), (14.5, 9)], closed=True, r=rnd(S, 0, 0.6))
    return [shell(PINE_BODY), shell(crown), detail(seg(9, 9, 15, 9)),
            detail(ell_chord(12, 15, 6, 6, 24, "/", 0.6)), detail(ell_chord(12, 15, 6, 6, 30, "/", 0.6)),
            detail(ell_chord(12, 15, 6, 6, -6, "\\", 0.6)), detail(ell_chord(12, 15, 6, 6, 0, "\\", 0.6))]


@icon("avocado", CAT, "Half an avocado with its stone", tags=["fruit", "guacamole", "healthy", "produce"])
def _(S):
    if S.name == "line":  # a slightly pointed stem end
        body = ("M12 3C9.3 3.6 8 5.8 7.4 8.8C7 10.8 4.5 12.6 4.5 15.8C4.5 19 7.5 21 12 21"
                "C16.5 21 19.5 19 19.5 15.8C19.5 12.6 17 10.8 16.6 8.8C16 5.8 14.7 3.6 12 3Z")
    else:
        body = ("M12 3C8.8 3 8 5.8 7.4 8.8C7 10.8 4.5 12.6 4.5 15.8C4.5 19 7.5 21 12 21"
                "C16.5 21 19.5 19 19.5 15.8C19.5 12.6 17 10.8 16.6 8.8C16 5.8 15.2 3 12 3Z")
    return [shell(body), detail(circle(12, 15.5, 3))]


@icon("peach", CAT, "A peach with its crease and a leaf", tags=["fruit", "apricot", "nectarine", "produce"])
def _(S):
    body = "M12 8.5C10 6.8 4 7 4 13.5C4 18 7.5 21 12 21C16.5 21 20 18 20 13.5C20 7 14 6.8 12 8.5Z"
    return [shell(body), detail("M12 8.5C9.6 10.8 9 14.5 10.3 18.5"), shell(leaf(12.5, 6.5, 17.5, 3.5, 1.3))]


@icon("coconut", CAT, "A coconut cracked in half", tags=["fruit", "tropical", "nut", "palm", "produce"])
def _(S):
    zig = [(3, 10), (6, 8), (9, 10.5), (12, 8), (15, 10.5), (18, 8), (21, 10)]
    pts = poly(zig, r=rnd(S, 0, 0.8))
    return [shell(pts + "A9 9 0 0 1 3 10Z"), detail(arc(12, 10, 5.5, 8, 172))]


@icon("kiwi", CAT, "A kiwi fruit cut in half, showing its seeds", tags=["kiwifruit", "fruit", "slice", "produce"])
def _(S):
    seeds = [dot(*pt, 0.9) for pt in (regular(12, 12, 5, 8, -90 + 22.5))]
    return [shell(circle(12, 12, 9)), detail(ellipse(12, 12, 2, 1.25) if S.name == "line" else circle(12, 12, 1.5)), *seeds]


@icon("lime", CAT, "A slice of lime with its segments", tags=["citrus", "fruit", "slice", "lemon", "produce"])
def _(S):
    spokes = []
    for k in range(6):
        a = -90 + k * 60
        x1, y1 = (12 + 1.5 * math.cos(math.radians(a)), 12 + 1.5 * math.sin(math.radians(a)))
        x2, y2 = (12 + 6 * math.cos(math.radians(a)), 12 + 6 * math.sin(math.radians(a)))
        spokes.append(detail(seg(x1, y1, x2, y2)))
    return [shell(circle(12, 12, 9)), *spokes]


MANGO = ("M7.5 20.5C4.2 19.5 3 16 3.8 12.5C4.8 8 8.5 5 13 4.5C17.5 4 20.8 6.5 20.8 10"
         "C20.8 13 18.5 14.5 16 15.5C13.5 16.5 12.5 18 11.2 19.5C10.2 20.6 8.8 20.9 7.5 20.5Z")


@icon("mango", CAT, "A mango with a leaf", tags=["fruit", "tropical", "produce"])
def _(S):
    return [shell(xf(MANGO, 0, dy=1)), line("M12.5 5.6L12 3"), shell(leaf(14.2, 5.2, 20, 2.8, 1.1))]


BERRIES = [(12, 7, 3.5), (6.5, 16.5, 3.5), (17.5, 16.5, 3.5)]


@icon("blueberries", CAT, "Three blueberries with their crowns", tags=["blueberry", "berries", "fruit", "produce"])
def _(S):
    out = []
    for cx, cy, r in BERRIES:
        out.append(shell(circle(cx, cy, r)))
        out.append(detail(f"M{fmt(cx - 0.5)} {fmt(cy - 0.5)}L{fmt(cx + 0.5)} {fmt(cy + 0.5)}"
                          f"M{fmt(cx + 0.5)} {fmt(cy - 0.5)}L{fmt(cx - 0.5)} {fmt(cy + 0.5)}"))
    return out


# =========================================================================== vegetables

def rot_pts(points, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in points]


def bar(x1, y1, x2, y2, w, rc):
    """Rectangle of width w along the axis (x1, y1)-(x2, y2), corners filleted by rc (as poly)."""
    L = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / L * w / 2, (x2 - x1) / L * w / 2
    return poly([(x1 + nx, y1 + ny), (x2 + nx, y2 + ny), (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)], closed=True, r=rc)


CARROT = "M8.5 8.5C8.5 7 9.5 6.5 12 6.5C14.5 6.5 15.5 7 15.5 8.5L12 21.5Z"


@icon("carrot", CAT, "A carrot with its leafy top", tags=["vegetable", "root", "veggie", "produce"])
def _(S):
    return [shell(xf(CARROT, 45)),
            line(xf("M12 6.5L12 2.5", 45)), line(xf("M11 6.5C10.5 4.5 9.5 3.5 8 3", 45)),
            line(xf("M13 6.5C13.5 4.5 14.5 3.5 16 3", 45)),
            detail(xf("M9.3 11L11.5 11", 45)), detail(xf("M14.2 14.5L12.4 14.5", 45))]


@icon("broccoli", CAT, "A head of broccoli", tags=["vegetable", "greens", "veggie", "healthy", "produce"])
def _(S):
    head = ("M7.5 13.5A3.5 3.5 0 0 1 5 7.2A4 4 0 0 1 12 4.2A4 4 0 0 1 19 7.2A3.5 3.5 0 0 1 16.5 13.5Z")
    stem = poly([(9.5, 13.5), (10, 21), (14, 21), (14.5, 13.5)], closed=True, r=S.r)
    return [shell(head), shell(stem), detail(seg(9, 13.5, 15, 13.5))]


@icon("corn", CAT, "An ear of corn in its husk", tags=["maize", "cob", "vegetable", "grain", "produce"])
def _(S):
    edge_l = "C8 12.5 10.8 14.8 12 18"   # from (5, 11.5)
    edge_r = "C16 12.5 13.2 14.8 12 18"  # from (19, 11.5)
    cob = "M8.5 13.2V8.5C8.5 5 10 3 12 3C14 3 15.5 5 15.5 8.5V13.2C14.2 14.4 12.8 15.9 12 18C11.2 15.9 9.8 14.4 8.5 13.2Z"
    return [shell(cob), shell("M12 21C8 20.5 5 17 5 11.5" + edge_l + "Z"), shell("M12 21C16 20.5 19 17 19 11.5" + edge_r + "Z"),
            detail("M5 11.5" + edge_l), detail("M19 11.5" + edge_r),
            detail(seg(12, 5, 12, 13.5)), detail(seg(8.5, 7.5, 15.5, 7.5)), detail(seg(8.5, 11, 15.5, 11))]


@icon("chili-pepper", CAT, "A curved chili pepper", tags=["chilli", "pepper", "spicy", "hot", "vegetable"], aliases=["chili"])
def _(S):
    body = "M14 7.5C17.5 7.5 19.3 9.8 18.3 13.2C17 17.5 11 20.8 4 20.8C8 18.7 10.5 15.5 11.3 11.8C11.8 9.2 12.3 7.5 14 7.5Z"
    return [shell(body), line(poly([(15.5, 7.5), (16, 5), (18.5, 3)], r=S.r))]


@icon("tomato", CAT, "A tomato with its stalk and leaves", tags=["vegetable", "fruit", "salad", "produce"])
def _(S):
    return [shell(ellipse(12, 13.5, 9, 7.5)), line(seg(12, 6, 12, 3)),
            detail(poly([(8, 7.5), (10, 9.5), (12, 8), (14, 9.5), (16, 7.5)], r=S.r))]


EGGPLANT = ("M10.2 5L13.8 5C14.5 7.5 16.3 10 16.3 14.5C16.3 18.3 14.5 20.7 12 20.7C9.5 20.7 7.7 18.3 7.7 14.5"
            "C7.7 10 9.5 7.5 10.2 5Z")


@icon("eggplant", CAT, "An eggplant (aubergine) with its green cap", tags=["aubergine", "brinjal", "vegetable", "produce"],
      aliases=["aubergine"])
def _(S):
    k = dict(deg=40, cx=12, cy=12.5, dx=-0.3, dy=0)
    cap = poly([(8.9, 9.2), (10.5, 8), (12, 10.5), (13.5, 8), (15.1, 9.2)], r=rnd(S, 0, 0.5))
    return [shell(xf(EGGPLANT, **k)), detail(xf(cap, **k)), line(xf("M12 5L12 1.8", **k))]


@icon("potato", CAT, "A potato", tags=["vegetable", "spud", "tuber", "produce"])
def _(S):
    body = ("M6.5 6.5C9 4.5 13.5 4.8 16.8 6.3C20 7.8 21.2 11 20.4 14.2C19.6 17.6 16.2 19.6 12 19.4"
            "C8 19.2 4.8 18 3.9 14.8C3.2 12 4.3 8.3 6.5 6.5Z")
    return [shell(xf(body, 0, dy=0.5)), detail(seg(8, 10, 9.5, 10.5)), detail(seg(15, 9.5, 16.5, 9)), detail(seg(12, 15.5, 13.5, 15))]


@icon("onion", CAT, "An onion bulb with roots", tags=["vegetable", "bulb", "shallot", "produce"])
def _(S):
    body = ("M12 2.5C12.5 5 14 6.5 16.5 8C19.5 9.8 20.5 11.8 20.5 14.2C20.5 17.2 17 19 12 19"
            "C7 19 3.5 17.2 3.5 14.2C3.5 11.8 4.5 9.8 7.5 8C10 6.5 11.5 5 12 2.5Z")
    return [shell(body), detail("M12 7.5C9.5 10 8.7 13.5 9.5 19"), detail("M12 7.5C14.5 10 15.3 13.5 14.5 19"),
            line(seg(10, 19.5, 9.5, 21.5)), line(seg(12, 19.5, 12, 21.5)), line(seg(14, 19.5, 14.5, 21.5))]


@icon("mushroom", CAT, "A mushroom with a domed cap", tags=["fungus", "vegetable", "toadstool", "produce"])
def _(S):
    cap = "M3 12C3 6.8 7 3.5 12 3.5C17 3.5 21 6.8 21 12Z" if S.name == "line" else \
        "M4.5 12C3.7 12 3 11.4 3 10.5C3.4 6.3 7.3 3.5 12 3.5C16.7 3.5 20.6 6.3 21 10.5C21 11.4 20.3 12 19.5 12Z"
    return [shell(cap), shell(rect(9, 12, 6, 9, min(S.R, 2.5))), detail(seg(8.5, 12, 15.5, 12))]


@icon("garlic", CAT, "A bulb of garlic showing its cloves", tags=["vegetable", "clove", "bulb", "spice", "produce"])
def _(S):
    body = ("M12 2.5C12 5.5 13.2 7 15.2 8.5C18.5 11 20.5 13.2 20.5 16.2C20.5 18.8 18.8 20.5 16.8 20.5"
            "C16 20.5 15.5 20 15 19.5C14.2 20.3 13.2 20.7 12 20.7C10.8 20.7 9.8 20.3 9 19.5"
            "C8.5 20 8 20.5 7.2 20.5C5.2 20.5 3.5 18.8 3.5 16.2C3.5 13.2 5.5 11 8.8 8.5C10.8 7 12 5.5 12 2.5Z")
    return [shell(body), detail("M11.5 9.5C9 11.5 8.3 15.5 9 19.5"), detail("M12.5 9.5C15 11.5 15.7 15.5 15 19.5")]


@icon("cucumber", CAT, "A cucumber", tags=["vegetable", "gherkin", "pickle", "salad", "produce"])
def _(S):
    body = bar(5.5, 18.5, 17.5, 6.5, 7, rnd(S, 2.5, 3.5))
    return [shell(body), line(seg(17.5, 6.5, 19.8, 4.2)), dot(9, 15, 1), dot(12.5, 13, 1), dot(14, 9.5, 1)]


@icon("lettuce", CAT, "A crinkly lettuce leaf", tags=["salad", "greens", "romaine", "vegetable", "produce"])
def _(S):
    # left edge contour, bottom to top; the right edge mirrors it. Scallops bulge outwards.
    left = [(12, 21.3), (7.8, 17.3), (6.2, 12), (7.4, 6.8), (12, 2.7)]
    pts = left + [(24 - x, y) for x, y in reversed(left[1:-1])]
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(len(pts)):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % len(pts)]
        r = math.hypot(x1 - x0, y1 - y0) / 2 * 1.15
        d += f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(y1)}"
    d += "Z"
    k = dict(deg=30, cx=12, cy=12)
    return [shell(xf(d, **k)), detail(xf("M12 21.3L12 7", **k)),
            detail(xf(poly([(9.2, 10), (12, 12.5), (14.8, 10)], r=S.r), **k))]


def pt_on_deg(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


@icon("pumpkin", CAT, "A ribbed pumpkin with a stem", tags=["squash", "halloween", "autumn", "vegetable", "produce"])
def _(S):
    body = ("M12 8C10.5 7 8.5 6.8 7 7.1C4 7.8 2.9 10.8 3 14.2C3.2 18 5.5 20.5 8.5 20.5C9.8 20.5 10.8 20 12 20"
            "C13.2 20 14.2 20.5 15.5 20.5C18.5 20.5 20.8 18 21 14.2C21.1 10.8 20 7.8 17 7.1C15.5 6.8 13.5 7 12 8Z")
    return [shell(body), detail("M8.8 7.2C7 10 7 17.5 9 20.4"), detail("M15.2 7.2C17 10 17 17.5 15 20.4"),
            line(poly([(12, 8), (12, 4.5), (14, 3)], r=S.r))]


PEANUT = ("M12 3C15 3 16.5 5 16.5 7.5C16.5 9.5 15.2 10.8 15.2 12C15.2 13.2 17 14.5 17 16.5C17 19.3 14.8 21 12 21"
          "C9.2 21 7 19.3 7 16.5C7 14.5 8.8 13.2 8.8 12C8.8 10.8 7.5 9.5 7.5 7.5C7.5 5 9 3 12 3Z")


@icon("peanut", CAT, "A peanut in its shell", tags=["nut", "groundnut", "allergy", "snack", "legume"])
def _(S):
    return [shell(xf(PEANUT, 45)), detail(xf("M11 7L13 7", 45)), detail(xf("M11 16L13 16", 45)),
            detail(xf("M11 18.5L13 18.5", 45))]


# =========================================================================== dishes

def behind(back_d, fronts, gap=1.75):
    """Outline (d) of the part of back_d not hidden by the front shapes, kept `gap` clear of their strokes.
    gap=None attaches the back shape to the front outline (their strokes merge)."""
    if gap is None:
        cut = U(*[P(f) for f in fronts])
    else:
        cut = U(*[U(P(f), ST(f, 2 * (gap + 2), "round", "round")) for f in fronts])
    return path_to_d(D(P(back_d), cut))


def rotd(d, deg, cx=12.0, cy=12.0, dx=0.0, dy=0.0):
    """Rotate a closed outline via pathops (any SVG commands)."""
    a, b, c, d_, e, f = rotation(deg, cx, cy)
    return path_to_d(transform_path(P(d), (a, b, c, d_, e + dx, f + dy)))


def bone_end(ex, ey, ux, uy, lobe_r=1.6, spread=1.35):
    """Region (pathops) of a bone knob at (ex, ey), axis direction (ux, uy) pointing outwards."""
    nx, ny = -uy, ux
    return U(P(circle(ex + nx * spread, ey + ny * spread, lobe_r)), P(circle(ex - nx * spread, ey - ny * spread, lobe_r)))


def bone_region(x1, y1, x2, y2, w=2.6, knobs=(True, True)):
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    r = P(bar(x1, y1, x2, y2, w, 0))
    if knobs[0]:
        r = U(r, bone_end(x1, y1, -ux, -uy))
    if knobs[1]:
        r = U(r, bone_end(x2, y2, ux, uy))
    return r


BOWL_TOP = 11.5


def bowl(S, top=BOWL_TOP):
    """A round-bottomed bowl with a flat rim at y=top."""
    if S.name == "line":
        return f"M3 {top}L21 {top}C21 {top + 5} 17 {top + 9} 12 {top + 9}C7 {top + 9} 3 {top + 5} 3 {top}Z"
    return (f"M4.5 {top}L19.5 {top}C20.3 {top} 21 {top + 0.7} 20.9 {top + 1.5}C20.3 {top + 5.8} 16.6 {top + 9} 12 {top + 9}"
            f"C7.4 {top + 9} 3.7 {top + 5.8} 3.1 {top + 1.5}C3 {top + 0.7} 3.7 {top} 4.5 {top}Z")


@icon("bread", CAT, "A loaf of bread with scored top", tags=["loaf", "bakery", "baguette", "toast", "wheat"])
def _(S):
    R = rnd(S, 1.5, 3)
    body = (f"M3.5 11.5C3.5 7.5 7.5 5.5 12 5.5C16.5 5.5 20.5 7.5 20.5 11.5V{fmt(19 - R)}A{R} {R} 0 0 1 {fmt(20.5 - R)} 19"
            f"H{fmt(3.5 + R)}A{R} {R} 0 0 1 3.5 {fmt(19 - R)}Z")
    return [shell(body), detail(seg(7, 11.5, 8.5, 8.5)), detail(seg(11.2, 11.5, 12.7, 8.5)), detail(seg(15.4, 11.5, 16.9, 8.5))]


def _croissant():
    cx, cy, R = 12, 15, 8.4
    notches = [-130, -50]
    tipL, tipR = (4.2, 18.8), (19.8, 18.8)
    nL, nR = pt_on_deg(cx, cy, R, notches[0]), pt_on_deg(cx, cy, R, notches[1])
    P2 = lambda p: f"{fmt(p[0])} {fmt(p[1])}"  # noqa: E731
    lob = lambda a, b, k: f"A{fmt(k)} {fmt(k)} 0 0 1 {P2(b)}"  # noqa: E731
    dL = math.hypot(nL[0] - tipL[0], nL[1] - tipL[1]) / 2 * 1.12
    dM = math.hypot(nR[0] - nL[0], nR[1] - nL[1]) / 2 * 1.25
    # inner edge: circle through both tips and (12, 12.8)
    ci = (tipR[0] - 12) ** 2
    c = (ci + tipR[1] ** 2 - 12.8 ** 2) / (2 * (tipR[1] - 12.8))
    ri = c - 12.8
    iL = pt_on_deg(12, c, ri, -122)
    iR = pt_on_deg(12, c, ri, -58)
    d = (f"M{P2(tipL)}{lob(tipL, nL, dL)}{lob(nL, nR, dM)}{lob(nR, tipR, dL)}"
         f"A{fmt(ri)} {fmt(ri)} 0 0 0 {P2(tipL)}Z")
    return d, [seg(*nL, *iL), seg(*nR, *iR)]


@icon("croissant", CAT, "A crescent-shaped croissant", tags=["pastry", "bakery", "breakfast", "french"])
def _(S):
    d, segs = _croissant()
    return [shell(d), *(detail(x) for x in segs)]


@icon("cheese", CAT, "A wedge of cheese with holes", tags=["dairy", "cheddar", "swiss", "wedge"])
def _(S):
    return [shell(poly([(3, 19.5), (3, 12), (21, 5.5), (21, 19.5)], closed=True, r=S.r)),
            dot(7.5, 15.5, 1.6), dot(13, 13.5, 1.3), dot(16.5, 17, 1.1)]


EGG = "M12 3C16 3 19 9.5 19 14C19 18.5 16 21 12 21C8 21 5 18.5 5 14C5 9.5 8 3 12 3Z"


@icon("egg", CAT, "An egg", tags=["eggs", "breakfast", "protein", "easter"])
def _(S):
    return [shell(EGG), detail("M8.5 14.5C8.5 12.5 9.1 10.5 10 9")]


HAM = "M10 9C8.5 11.5 4.5 13.5 4.5 16.8A7.5 3.2 0 0 0 19.5 16.8C19.5 13.5 15.5 11.5 14 9Z"


@icon("meat", CAT, "A leg of ham on the bone", tags=["ham", "beef", "pork", "protein", "roast"])
def _(S):
    k = dict(deg=40, cx=12, cy=12, dx=-0.8, dy=0.6)
    body = xf(HAM, **k)
    bone = path_to_d(transform_path(bone_region(12, 11, 12, 4, knobs=(False, True)), rotation(40, 12, 12)))
    bone = rotd(bone, 0, dx=-0.8, dy=0.6)
    return [shell(body), shell(behind(bone, [body], None)), detail(xf(ellipse(12, 16.8, 7.5, 3.2), **k))]


DRUM = "M12 4.5C15.8 4.5 18.3 7.5 18.3 11C18.3 14.3 15.5 16.3 12 18.5C8.5 16.3 5.7 14.3 5.7 11C5.7 7.5 8.2 4.5 12 4.5Z"


@icon("drumstick", CAT, "A chicken drumstick", tags=["chicken", "leg", "poultry", "fried-chicken", "meat"])
def _(S):
    k = dict(deg=45, dx=3, dy=-3)
    meat_d = xf(DRUM, **k)
    bone_d = path_to_d(bone_region(11, 13, 6, 18, knobs=(False, True)))
    return [shell(meat_d), shell(behind(bone_d, [meat_d], None)), detail(xf("M8.7 10.5C8.7 8.8 9.7 7.3 11.5 6.8", **k))]


@icon("fish-food", CAT, "A whole fish, as food", tags=["fish", "seafood", "salmon", "dinner"])
def _(S):
    body = poly([(18.2, 9.3), (21, 6.5), (21, 17.5), (18.2, 14.7)], r=0)
    body = ("M3 12C5.5 8 9 6.5 12.5 6.5C15.2 6.5 17 7.8 18.2 9.3L21 6.5V17.5L18.2 14.7"
            "C17 16.2 15.2 17.5 12.5 17.5C9 17.5 5.5 16 3 12Z")
    return [shell(body), dot(7.3, 11, 1.1), detail("M10.5 8.2C11.8 10.5 11.8 13.5 10.5 15.8")]


def _shrimp(S):
    """An arched shrimp: head on the right, tail fan on the left."""
    cx, cy, R, r = 12, 15.5, 8.5, 4
    a0, a1 = 175, 15   # tail end (left) ... head end (right), clockwise over the top
    P2 = lambda p: f"{fmt(p[0])} {fmt(p[1])}"  # noqa: E731
    o0, o1 = pt_on_deg(cx, cy, R, a0), pt_on_deg(cx, cy, R, a1)
    i0, i1 = pt_on_deg(cx, cy, r, a0), pt_on_deg(cx, cy, r, a1)
    hr = (R - r) / 2
    # tail fan below the tail end
    t1 = (o0[0] - 1, o0[1] + 4.8)
    nt = ((o0[0] + i0[0]) / 2, o0[1] + 2.6)
    t2 = (i0[0] + 1.2, i0[1] + 4.8)
    d = (f"M{P2(o0)}A{R} {R} 0 1 1 {P2(o1)}A{fmt(hr)} {fmt(hr)} 0 0 1 {P2(i1)}A{r} {r} 0 1 0 {P2(i0)}"
         f"L{P2(t2)}L{P2(nt)}L{P2(t1)}Z")
    segs = [detail(seg(*pt_on_deg(cx, cy, r, a), *pt_on_deg(cx, cy, R, a))) for a in (215, 255, 295)]
    return d, segs, pt_on_deg(cx, cy, (R + r) / 2, a1 - 22)


@icon("shrimp", CAT, "A shrimp with its tail fan", tags=["prawn", "seafood", "shellfish", "scampi"], aliases=["prawn"])
def _(S):
    d, segs, eye = _shrimp(S)
    return [shell(d), *segs, dot(*eye, 1)]


@icon("burger", CAT, "A hamburger with bun and patty", tags=["hamburger", "cheeseburger", "fast-food", "sandwich"])
def _(S):
    bun = "M3.5 10C3.5 5.5 7 3.5 12 3.5C17 3.5 20.5 5.5 20.5 10Z"
    return [shell(bun), line(seg(3, 13.5, 21, 13.5)), shell(rect(3.5, 17, 17, 3.5, rnd(S, 1.5, 1.75))),
            dot(9, 7, 0.9), dot(12, 5.9, 0.9), dot(15, 7, 0.9)]


@icon("pizza", CAT, "A slice of pizza", tags=["slice", "pepperoni", "italian", "fast-food"])
def _(S):
    return [shell("M3 5.5Q12 2.5 21 5.5L12 21.5Z"), detail("M4.6 8.4Q12 5.9 19.4 8.4"),
            dot(9.5, 11.5, 1.4), dot(14.3, 12.3, 1.3), dot(11.8, 15.5, 1.2)]


@icon("hot-dog", CAT, "A sausage in a hot-dog bun", tags=["hotdog", "sausage", "frankfurter", "fast-food"], aliases=["hotdog"])
def _(S):
    k = dict(deg=-40, cx=12, cy=12)
    sausage = rotd(rect(2.5, 9.75, 19, 4.5, rnd(S, 1.2, 2.25)), **k)
    top = "M4.3 9.2C6.3 6.6 9 5.8 12 5.8C15 5.8 17.7 6.6 19.7 9.2"
    bottom = "M4.3 14.8C6.3 17.4 9 18.2 12 18.2C15 18.2 17.7 17.4 19.7 14.8"
    return [shell(sausage), line(xf(top, **k)), line(xf(bottom, **k))]


@icon("taco", CAT, "A folded taco with filling", tags=["mexican", "tortilla", "fast-food", "burrito"])
def _(S):
    cx, cy, R = 12, 17, 9
    shell_d = f"M{cx - R} {cy}A{R} {R} 0 0 1 {cx + R} {cy}Z"
    n, r2 = 5, 5.8
    pts = [pt_on_deg(cx, cy, r2, 180 + i * 180 / n) for i in range(n + 1)]
    frill = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    br = r2 * math.sin(math.radians(90 / n)) * 1.1
    for x, y in pts[1:]:
        frill += f"A{fmt(br)} {fmt(br)} 0 0 1 {fmt(x)} {fmt(y)}"
    return [shell(shell_d), detail(frill)]


@icon("sandwich", CAT, "A sandwich wedge showing its filling", tags=["sub", "toast", "lunch", "club", "snack"])
def _(S):
    body = poly([(3.5, 12), (3.5, 3.5), (20.5, 12), (20.5, 20.5), (3.5, 20.5)], closed=True, r=S.r)
    wave = "M3.5 16.3C5.2 15 6.8 17.6 8.5 16.3C10.2 15 11.8 17.6 13.5 16.3C15.2 15 16.8 17.6 18.5 16.3C19.2 15.8 19.8 15.9 20.5 16.3"
    return [shell(body), detail(seg(3.5, 12, 20.5, 12)), detail(wave)]


@icon("fries", CAT, "French fries in a carton", tags=["chips", "french-fries", "fast-food", "potato"], aliases=["french-fries"])
def _(S):
    box = "M4 10Q12 13.5 20 10L17.8 21H6.2Z"
    return [shell(box if S.name == "line" else "M4 10Q12 13.5 20 10L18 20A1.2 1.2 0 0 1 16.8 21H7.2A1.2 1.2 0 0 1 6 20Z"),
            line(seg(8.3, 9.6, 7.3, 3.8)), line(seg(12, 10, 12, 2.8)), line(seg(15.7, 9.6, 16.7, 3.8))]


@icon("noodles", CAT, "A bowl of noodles with chopsticks", tags=["ramen", "pho", "pasta", "chopsticks", "asian"],
      aliases=["ramen"])
def _(S):
    return [shell(bowl(S)), line(seg(9, 8.5, 20.5, 2.8)), line(seg(12.5, 9.5, 21, 5.8)),
            line("M6.5 10.5C5.5 9 7.5 7.5 6.5 5.5"), line("M9.8 7.5C9 6.5 10.3 5 9.8 3.5")]


@icon("rice-bowl", CAT, "A bowl heaped with rice", tags=["rice", "bowl", "asian", "grain", "meal"])
def _(S):
    top = BOWL_TOP
    n = 5
    pts = [pt_on_deg(12, top + 3.5, 8, 180 + 22 + i * (136 / n)) for i in range(n + 1)]
    mound = f"M4 {top}L{fmt(pts[0][0])} {fmt(pts[0][1])}"
    br = 8 * math.sin(math.radians(136 / n / 2)) * 1.15
    for x, y in pts[1:]:
        mound += f"A{fmt(br)} {fmt(br)} 0 0 1 {fmt(x)} {fmt(y)}"
    mound += f"L20 {top}Z"
    return [shell(bowl(S)), shell(mound), detail(seg(3.5, top, 20.5, top))]


@icon("soup", CAT, "A steaming bowl of soup", tags=["bowl", "broth", "stew", "hot", "meal"])
def _(S):
    return [shell(bowl(S)), line("M8 3.5C7 5 9 6.5 8 8.5"), line("M12 3.5C11 5 13 6.5 12 8.5"), line("M16 3.5C15 5 17 6.5 16 8.5")]


@icon("salad", CAT, "A bowl of salad leaves", tags=["greens", "healthy", "vegetarian", "lettuce", "bowl"])
def _(S):
    return [shell(bowl(S)), shell(leaf(7, 9.5, 4.5, 4.5, 1.5)), shell(leaf(12, 9.5, 12, 3, 1.7)), shell(leaf(17, 9.5, 19.5, 4.5, 1.5))]


@icon("sushi", CAT, "A piece of nigiri sushi", tags=["nigiri", "japanese", "fish", "rice", "seafood"])
def _(S):
    k = dict(deg=-15, cx=12, cy=12.5)
    fish = "M3 11.2C3 8.4 6.5 7 12 7C17.5 7 21 8.4 21 11.2C21 12.3 20.3 13 19 13H5C3.7 13 3 12.3 3 11.2Z"
    rice = rect(5.5, 13, 13, 6.5, 3.25) if S.name == "rounded" else rect(5.5, 13, 13, 6.5, 2.2)
    return [shell(rotd(fish, **k)), shell(rotd(rice, **k)), detail(xf("M4 13L20 13", **k)),
            detail(xf("M8.5 13L10.3 7.4", **k)), detail(xf("M13.5 13L15.3 7.4", **k))]


# =========================================================================== sweets, bakery, extras

def scallop_ring(cx, cy, R, n, bulge=1.1, start=-90):
    pts = [pt_on_deg(cx, cy, R, start + i * 360 / n) for i in range(n)]
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    br = R * math.sin(math.pi / n) * bulge
    for i in range(n):
        x, y = pts[(i + 1) % n]
        d += f"A{fmt(br)} {fmt(br)} 0 0 1 {fmt(x)} {fmt(y)}"
    return d + "Z"


def wave(x0, x1, y, amp, period, phase=0.0, step=0.5):
    n = max(2, int(round((x1 - x0) / step)))
    return [(x0 + (x1 - x0) * i / n, y + amp * math.sin(2 * math.pi * ((x0 + (x1 - x0) * i / n) - x0) / period + phase))
            for i in range(n + 1)]


@icon("cake", CAT, "A birthday cake with candles", tags=["birthday", "party", "celebration", "dessert", "anniversary"])
def _(S):
    body = rect(4, 11, 16, 9.5, rnd(S, 1.5, 3))
    icing = "M4 14C5.3 14 5.7 16 7 16C8.3 16 8.7 14 10 14C11.3 14 11.7 16 13 16C14.3 16 14.7 14 16 14C17.3 14 17.7 16 20 15.5"
    return [shell(body), detail(icing),
            line(seg(8, 10, 8, 7.5)), line(seg(12, 10, 12, 7.5)), line(seg(16, 10, 16, 7.5)),
            dot(8, 4.8, 1.1), dot(12, 4.8, 1.1), dot(16, 4.8, 1.1)]


@icon("cupcake", CAT, "A cupcake with swirled frosting and a cherry", tags=["muffin", "dessert", "sweet", "bakery", "birthday"])
def _(S):
    frosting = ("M5.5 13C4 13 3.3 11.6 4 10.4C4.6 9.4 5.6 9 6.6 9C6.6 7.3 8.3 6 10.3 6H13.7C15.7 6 17.4 7.3 17.4 9"
                "C18.4 9 19.4 9.4 20 10.4C20.7 11.6 20 13 18.5 13Z")
    wrapper = poly([(5.5, 13), (18.5, 13), (17, 21), (7, 21)], closed=True, r=S.r)
    return [shell(frosting), shell(wrapper), detail(seg(4.5, 13, 19.5, 13)), detail(seg(6.6, 9, 17.4, 9)),
            dot(12, 3.3, 1.5), detail(seg(12, 13, 12, 21))]


def _donut_sprinkles():
    return [seg(*pt_on_deg(12, 12, 5.2, a), *pt_on_deg(12, 12, 7.2, a + 10)) for a in (-60, 60, 180)]


def _donut_filled():
    body = D(P(circle(12, 12, 10)), P(circle(12, 12, 2)))
    return D(body, *(ST(sp, 2) for sp in _donut_sprinkles()))


@icon("donut", CAT, "A ring donut with sprinkles", tags=["doughnut", "dessert", "sweet", "bakery", "snack"],
      aliases=["doughnut"], filled=_donut_filled)
def _(S):
    return [shell(circle(12, 12, 9)), line(circle(12, 12, 3)), *(detail(sp) for sp in _donut_sprinkles())]


@icon("ice-cream", CAT, "An ice-cream cone with a scoop", tags=["icecream", "gelato", "dessert", "cone", "summer"],
      aliases=["icecream"])
def _(S):
    scoop = "M6 11C4.6 11 4 9.9 4.5 8.6C5.6 5.2 8.5 3 12 3C15.5 3 18.4 5.2 19.5 8.6C20 9.9 19.4 11 18 11Z"
    cone = poly([(6, 11), (18, 11), (12, 21.2)], closed=True, r=S.r)
    return [shell(scoop), shell(cone), detail(seg(5, 11, 19, 11)),
            detail(seg(9, 11, 14.6, 16.6)), detail(seg(15, 11, 9.4, 16.6))]


@icon("candy", CAT, "A wrapped sweet", tags=["sweet", "bonbon", "toffee", "halloween", "treat"], aliases=["sweet"])
def _(S):
    k = -30
    fans = [rot_pts([(7.6, 12), (3.2, 8.2), (3.2, 15.8)], k), rot_pts([(16.4, 12), (20.8, 8.2), (20.8, 15.8)], k)]
    return [shell(circle(12, 12, 4.6)), *(shell(poly(f, closed=True, r=S.r)) for f in fans),
            detail(xf("M10.2 9C12 10.5 12 13.5 10.2 15", k))]


def _spiral(cx, cy, r0, pitch, turns, start=-90):
    pts = []
    n = int(turns * 48)
    for i in range(n + 1):
        t = i / 48
        a = math.radians(start + 360 * t)
        r = r0 + pitch * t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


@icon("lollipop", CAT, "A swirled lollipop on a stick", tags=["candy", "sweet", "sucker", "treat"])
def _(S):
    return [shell(circle(12, 9, 6.5)), line(seg(12, 15.5, 12, 21.5)),
            detail(poly(_spiral(12, 9, 0.4, 3.9, 1.05), r=0))]


def _choc_outline(S):
    R = rnd(S, 1.5, 3)
    return (f"M{fmt(5 + R)} 3H13.5A2.5 2.5 0 0 0 16.2 5.8A2.5 2.5 0 0 0 19 8.5V{fmt(21 - R)}"
            f"A{R} {R} 0 0 1 {fmt(19 - R)} 21H{fmt(5 + R)}A{R} {R} 0 0 1 5 {fmt(21 - R)}V{fmt(3 + R)}A{R} {R} 0 0 1 {fmt(5 + R)} 3Z")


@icon("chocolate", CAT, "A chocolate bar with a bite taken", tags=["candy", "cocoa", "sweet", "bar", "dessert"])
def _(S):
    return [shell(_choc_outline(S)), detail(seg(12, 3, 12, 21)), detail(seg(5, 9, 19, 9)), detail(seg(5, 15, 19, 15))]


@icon("popcorn", CAT, "A striped bucket of popcorn", tags=["cinema", "movie", "snack", "theater", "corn"])
def _(S):
    top = ("M4.5 10A2.3 2.3 0 0 1 5.3 6A2.5 2.5 0 0 1 9.5 4.6A2.5 2.5 0 0 1 14 3.6A2.5 2.5 0 0 1 17.6 5.6"
           "A2.3 2.3 0 0 1 19.5 10Z")
    bucket = poly([(4.5, 10), (19.5, 10), (17.5, 21), (6.5, 21)], closed=True, r=S.r)
    return [shell(top), shell(bucket), detail(seg(4, 10, 20, 10)),
            detail(seg(9.5, 10, 10.2, 21)), detail(seg(14.5, 10, 13.8, 21))]


@icon("pancakes", CAT, "A stack of pancakes topped with butter", tags=["pancake", "breakfast", "crepe", "syrup", "brunch"],
      aliases=["pancake"])
def _(S):
    return [shell(rect(4.5, 8.5, 15, 4, 2)), shell(rect(3, 12.5, 18, 4, 2)), shell(rect(4, 16.5, 16, 4, 2)),
            detail(seg(5, 12.5, 19, 12.5)), detail(seg(4.5, 16.5, 19.5, 16.5)),
            solid(rect(9.5, 4.3, 5, 3.2, rnd(S, 0.3, 1.2)))]


@icon("waffle", CAT, "A round waffle", tags=["breakfast", "brunch", "belgian", "dessert"])
def _(S):
    edge = scallop_ring(12, 12, 8.6, 12, 1.2, -90 + 15)
    return [shell(edge if S.name == "rounded" else poly(regular(12, 12, 9.2, 12, -90 + 15), closed=True)),
            detail(seg(9, 3.8, 9, 20.2)), detail(seg(15, 3.8, 15, 20.2)),
            detail(seg(3.8, 9, 20.2, 9)), detail(seg(3.8, 15, 20.2, 15))]


@icon("pie", CAT, "A pie with a fluted crust and steam vents", tags=["tart", "dessert", "bakery", "baking", "apple-pie"])
def _(S):
    # crust: dome over a scalloped rim that overhangs the dish
    n, x0, x1, y = 5, 3, 21, 13.2
    w = (x1 - x0) / n
    crust = f"M{x0} {y}C{x0 + 0.5} 9 {6.5} 6.5 12 6.5C17.5 6.5 {x1 - 0.5} 9 {x1} {y}"
    for i in range(n):
        crust += f"A{fmt(w / 2)} {fmt(w / 2 * 1.0)} 0 0 1 {fmt(x1 - w * (i + 1))} {y}"
    crust += "Z"
    dish = poly([(4, 12), (20, 12), (18, 20.5), (6, 20.5)], closed=True, r=S.r)
    return [shell(crust), shell(behind(dish, [crust], 1.0)), detail(seg(8.5, 9.3, 9.5, 11)), detail(seg(12, 8.5, 12, 10.5)),
            detail(seg(15.5, 9.3, 14.5, 11))]


PRETZEL = ("M18.5 7.8L7 18.2C5.5 19.6 3.2 18.5 3.2 14C3.2 8.5 5.5 4.5 8.7 4.5C10.8 4.5 12 6.3 12 8.5"
           "C12 6.3 13.2 4.5 15.3 4.5C18.5 4.5 20.8 8.5 20.8 14C20.8 18.5 18.5 19.6 17 18.2L5.5 7.8")


@icon("pretzel", CAT, "A twisted pretzel", tags=["snack", "bakery", "german", "bread", "oktoberfest"])
def _(S):
    return [line(PRETZEL)]


@icon("honey", CAT, "A honey pot with honey dripping from the rim", tags=["honeypot", "bee", "sweet", "syrup", "jar"])
def _(S):
    body = "M7 9H17C19.5 10.6 20.5 13.2 20.5 15.5C20.5 19 17 21 12 21C7 21 3.5 19 3.5 15.5C3.5 13.2 4.5 10.6 7 9Z"
    lid = rect(5.5, 4, 13, 3, rnd(S, 1, 1.5))
    drip = "M5 12.3H9V15A1.5 1.5 0 0 0 12 15V12.3H19"
    return [shell(body), shell(lid), detail(drip if S.name == "line" else "M5 12.3H8.5C9 12.3 9 12.8 9 13.3V15A1.5 1.5 0 0 0 12 15V13.3C12 12.8 12.2 12.3 12.8 12.3H19")]


@icon("jam", CAT, "A jar of jam with a label", tags=["jelly", "preserve", "marmalade", "jar", "spread"])
def _(S):
    return [shell(rect(5, 3, 14, 4, rnd(S, 1, 1.5))), shell(rect(5.5, 8.5, 13, 12.5, rnd(S, 2, 4))),
            detail(rect(8.5, 12, 7, 5.5, rnd(S, 0.5, 1)))]


@icon("dumpling", CAT, "A pleated steamed dumpling", tags=["bao", "dim-sum", "gyoza", "chinese", "asian"])
def _(S):
    body = "M3.5 17C3.5 11.5 7 7 12 4.5C17 7 20.5 11.5 20.5 17C20.5 19 19 20 17 20H7C5 20 3.5 19 3.5 17Z"
    return [shell(body), detail("M12 4.5C10.3 7.5 9 11 8.6 15"), detail(seg(12, 4.5, 12, 15)),
            detail("M12 4.5C13.7 7.5 15 11 15.4 15")]


@icon("kebab", CAT, "A kebab skewer with chunks of meat", tags=["skewer", "shish", "bbq", "grill", "satay"],
      aliases=["skewer", "shish-kebab"])
def _(S):
    k = dict(deg=-45, cx=12, cy=12)
    out = []
    w, gap = 3.8, 3.2
    x = 12 - (3 * w + 2 * gap) / 2
    for i in range(3):
        out.append(shell(rotd(rect(x, 8.75, w, 6.5, rnd(S, 1, 1.9)), **k)))
        x += w + gap
    x0 = 12 - (3 * w + 2 * gap) / 2
    out += [line(xf(f"M0.8 12L{fmt(x0)} 12", **k)), line(xf(f"M{fmt(24 - x0)} 12L22.5 12", **k))]
    return out


@icon("bento", CAT, "A bento box with compartments", tags=["lunchbox", "japanese", "meal", "box", "lunch"],
      aliases=["lunchbox"])
def _(S):
    return [shell(rect(3, 5, 18, 14, rnd(S, 2, 4))), detail(seg(11, 5, 11, 19)), detail(seg(11, 12, 21, 12)),
            dot(7, 12, 1.8)]


@icon("bacon", CAT, "A wavy strip of bacon", tags=["breakfast", "pork", "rasher", "meat"])
def _(S):
    top = wave(3, 21, 9, 1.4, 9)
    bot = [(x, y + 5.5) for x, y in reversed(top)]
    mid = [(x, y + 2.75) for x, y in top]
    return [shell(poly(top + bot, closed=True)), detail(poly(mid))]


@icon("steak", CAT, "A steak with its bone", tags=["beef", "meat", "t-bone", "grill", "bbq"])
def _(S):
    slab = ("M4 10.5C4 6.5 7.5 4 11 4.5C13.8 4.9 15.2 6.5 17.7 6.6C19.8 6.7 21 8.6 21 11"
            "C21 16.5 17 20 11.8 20C6.8 20 4 15.5 4 10.5Z")
    return [shell(slab), detail("M17.5 9.6C17.8 13.5 15.3 16.6 11.8 16.8"), detail(circle(9.5, 10.5, 2))]


# =========================================================================== drinks

def cup_body(S, y0, y1, x0=4.5, x1=16.5):
    c = rnd(S, 3, 4)
    return (f"M{fmt(x0)} {fmt(y0)}H{fmt(x1)}V{fmt(y1 - c)}C{fmt(x1)} {fmt(y1 - c * 0.35)} {fmt(x1 - c * 0.6)} {fmt(y1)} {fmt(x1 - c)} {fmt(y1)}"
            f"H{fmt(x0 + c)}C{fmt(x0 + c * 0.6)} {fmt(y1)} {fmt(x0)} {fmt(y1 - c * 0.35)} {fmt(x0)} {fmt(y1 - c)}Z")


def cup_handle(y, x=16.5, h=5, w=3):
    r = h / 2
    return f"M{fmt(x)} {fmt(y)}H{fmt(x + w - r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x + w - r)} {fmt(y + h)}H{fmt(x)}"


@icon("coffee", CAT, "A steaming cup of coffee", tags=["cafe", "espresso", "latte", "hot-drink", "caffeine", "cup"])
def _(S):
    return [shell(cup_body(S, 9.5, 20.5)), line(cup_handle(11)),
            line("M8.5 3C7.5 4.3 9.5 5.5 8.5 7"), line("M12.5 3C11.5 4.3 13.5 5.5 12.5 7")]


@icon("tea", CAT, "A cup of tea with a tea bag", tags=["teabag", "hot-drink", "chai", "brew", "cup"])
def _(S):
    tag = rect(4.5, 3, 4, 3.5, rnd(S, 0.5, 1))
    return [shell(cup_body(S, 9.5, 20.5)), line(cup_handle(11)), shell(tag), line("M6.5 6.5C6.5 8 8.5 8.5 10 9.5"),
            ]


@icon("cup", CAT, "A cup on a saucer", tags=["teacup", "saucer", "drink", "hot-drink", "espresso"], aliases=["teacup"])
def _(S):
    return [shell(cup_body(S, 7, 17)), line(cup_handle(8.5)), line(seg(3, 20.5, 21, 20.5))]


@icon("mug", CAT, "A tall mug", tags=["cup", "coffee", "tea", "drink", "hot-drink"])
def _(S):
    return [shell(rect(4, 4.5, 12, 16, rnd(S, 2, 4))), line(cup_handle(8, x=16, h=8, w=4.5))]


@icon("water-glass", CAT, "A tumbler glass of water", tags=["glass", "water", "drink", "tumbler", "hydration"],
      aliases=["glass-water"])
def _(S):
    return [shell(poly([(5, 3.5), (19, 3.5), (17.5, 20.5), (6.5, 20.5)], closed=True, r=S.r)),
            detail("M5.6 10C7.4 8.8 9.2 8.8 11 10C12.8 11.2 14.6 11.2 16.4 10C17.1 9.6 17.7 9.4 18.4 9.4")]


@icon("wine-glass", CAT, "A glass of wine", tags=["wine", "glass", "alcohol", "drink", "bar", "restaurant"])
def _(S):
    bowl_d = "M6.5 3H17.5C17.9 5 18 7 17.6 9C17 12 14.8 13.5 12 13.5C9.2 13.5 7 12 6.4 9C6 7 6.1 5 6.5 3Z"
    return [shell(bowl_d), line(seg(12, 13.5, 12, 20.5)), line(seg(7.5, 20.5, 16.5, 20.5)), detail(seg(6.1, 7.5, 17.9, 7.5))]


@icon("beer", CAT, "A mug of beer with foam", tags=["pint", "ale", "lager", "alcohol", "pub", "drink"])
def _(S):
    foam = "M4 9A2.3 2.3 0 0 1 5.6 4.5A3 3 0 0 1 10.5 3.6A3 3 0 0 1 15 4.2A2.4 2.4 0 0 1 16.5 9Z"
    body = rect(4, 9, 12.5, 12, rnd(S, 1.5, 3))
    return [shell(foam), shell(body), detail(seg(3.5, 9, 17, 9)), line(cup_handle(11, x=16.5, h=6.5, w=4)),
            detail(seg(8.2, 12, 8.2, 18)), detail(seg(12.3, 12, 12.3, 18))]


@icon("cocktail", CAT, "A cocktail glass with an olive", tags=["martini", "drink", "alcohol", "bar", "party"],
      aliases=["martini"])
def _(S):
    return [shell(poly([(3.5, 4.5), (20.5, 4.5), (12, 13)], closed=True, r=S.r)), line(seg(12, 13, 12, 20.5)),
            line(seg(7.5, 20.5, 16.5, 20.5)), dot(10.5, 7.8, 1.6), detail(seg(10.5, 7.8, 13.8, 4.5))]


@icon("bottle", CAT, "A bottle with a label", tags=["wine-bottle", "beverage", "drink", "glass", "alcohol"])
def _(S):
    R = rnd(S, 1.5, 3)
    body = (f"M10 2.5H14V7C14 8.3 17 9 17 11.5V{fmt(21.5 - R)}A{R} {R} 0 0 1 {fmt(17 - R)} 21.5H{fmt(7 + R)}"
            f"A{R} {R} 0 0 1 7 {fmt(21.5 - R)}V11.5C7 9 10 8.3 10 7Z")
    return [shell(body), detail(seg(7, 13.5, 17, 13.5)), detail(seg(7, 18, 17, 18))]


@icon("milk", CAT, "A carton of milk", tags=["carton", "dairy", "drink", "breakfast"])
def _(S):
    body = poly([(5.5, 21.5), (5.5, 9), (8.5, 5.2), (8.5, 2.5), (15.5, 2.5), (15.5, 5.2), (18.5, 9), (18.5, 21.5)], closed=True, r=S.r)
    return [shell(body), detail(seg(5.5, 9, 18.5, 9)), detail(seg(8.5, 5.2, 15.5, 5.2)),
            detail("M12 12.5C13.5 14.5 14.3 15.8 14.3 16.8A2.3 2.3 0 0 1 9.7 16.8C9.7 15.8 10.5 14.5 12 12.5Z")]


@icon("juice", CAT, "A juice box with a straw", tags=["juice-box", "drink", "orange-juice", "kids", "beverage"])
def _(S):
    return [shell(rect(5.5, 8, 13, 13.5, rnd(S, 1.5, 3))), line(poly([(13.5, 8), (13.5, 3.5), (18, 2.5)], r=S.r)),
            detail(circle(12, 15, 2.8))]


@icon("soda", CAT, "A can of soda", tags=["can", "pop", "cola", "soft-drink", "beverage"])
def _(S):
    body = poly([(7.5, 2.5), (16.5, 2.5), (18, 5), (18, 19), (16.5, 21.5), (7.5, 21.5), (6, 19), (6, 5)], closed=True, r=S.r)
    return [shell(body), detail(seg(6, 5, 18, 5)), detail(seg(6, 19, 18, 19)),
            detail("M6 14.5C9 11 13 15.5 18 10.5")]


@icon("teapot", CAT, "A teapot with a spout and handle", tags=["tea", "kettle", "brew", "pot", "hot-drink"])
def _(S):
    body = "M6.8 20.5C5 18.5 4.8 13.5 7.3 11H16.7C19.2 13.5 19 18.5 17.2 20.5Z"
    lid = "M8.5 11C8.5 9 10 8 12 8C14 8 15.5 9 15.5 11Z"
    return [shell(body), shell(lid), detail(seg(8, 11, 16, 11)), dot(12, 5.8, 1.3),
            line("M5.6 15L2.8 10.5"), line("M18.3 12.5C21.5 12.5 21.8 17.5 18.4 18")]


@icon("kettle", CAT, "A stovetop kettle", tags=["boil", "tea", "water", "kitchen", "hot"])
def _(S):
    body = poly([(6.5, 10), (15.5, 10), (18.5, 20.5), (3.5, 20.5)], closed=True, r=S.r)
    return [shell(body), line("M7 10V8.5C7 5.5 15 5.5 15 8.5V10"), line(seg(17.3, 16, 21, 10.5))]


# =========================================================================== kitchen

@icon("fork-knife", CAT, "A fork and a knife", tags=["restaurant", "dining", "cutlery", "meal", "eat", "utensils"],
      aliases=["utensils", "cutlery"])
def _(S):
    fork = "M4.5 3V8C4.5 9.8 5.6 11 7 11C8.4 11 9.5 9.8 9.5 8V3"
    blade = "M16 13V5.2C16 4 16.9 3 18 3C19.6 4 20.5 7.5 20.5 13Z"
    return [line(fork), line(seg(7, 3, 7, 8)), line(seg(7, 11, 7, 21)), shell(blade), line(seg(17.2, 13, 17.2, 21))]


@icon("spoon", CAT, "A spoon", tags=["cutlery", "utensil", "soup", "eat", "teaspoon"])
def _(S):
    bowl_d = ellipse(12, 7.8, 4.2, 5.3) if S.name == "rounded" else \
        "M12 2.5C14.6 2.5 16.2 5 16.2 7.8C16.2 10.8 14.4 13.1 12 13.1C9.6 13.1 7.8 10.8 7.8 7.8C7.8 5 9.4 2.5 12 2.5Z"
    return [shell(bowl_d), line(seg(12, 13.1, 12, 21.5))]


@icon("chef-hat", CAT, "A chef's toque", tags=["chef", "cook", "cooking", "kitchen", "restaurant", "toque"],
      aliases=["toque"])
def _(S):
    top = ("M7 14C4.6 14 3 12.3 3 10.2C3 7.9 4.9 6.2 7.2 6.4C8 4.4 9.8 3 12 3C14.2 3 16 4.4 16.8 6.4"
           "C19.1 6.2 21 7.9 21 10.2C21 12.3 19.4 14 17 14Z")
    band = poly([(7, 14), (17, 14), (17, 20.5), (7, 20.5)], closed=True, r=S.r)
    return [shell(top), shell(band), detail(seg(6.5, 14, 17.5, 14)), detail(seg(7, 17.3, 17, 17.3))]


def _board(S):
    R = rnd(S, 2, 3.5)
    return path_to_d(U(P(rect(3, 5.5, 14, 14, R)), P(rect(15, 9.5, 6, 6, rnd(S, 1.5, 3)))))


@icon("cutting-board", CAT, "A wooden cutting board with a handle", tags=["chopping-board", "kitchen", "prep", "cook", "wood"],
      aliases=["chopping-board"])
def _(S):
    return [shell(_board(S)), dot(18.2, 12.5, 1.3)]


@icon("frying-pan", CAT, "A frying pan", tags=["skillet", "pan", "cook", "kitchen", "fry"], aliases=["skillet"])
def _(S):
    handle = rotd(rect(14.5, 7.4, 9, 3.2, rnd(S, 0.8, 1.6)), -40, 14.5, 9)
    return [shell(circle(9.5, 14, 6.5)), shell(handle)]


@icon("cooking-pot", CAT, "A cooking pot with a lid", tags=["pot", "saucepan", "stew", "cook", "kitchen", "boil"],
      aliases=["saucepan"])
def _(S):
    return [shell(rect(4.5, 10.5, 15, 10, rnd(S, 1.5, 3.5))), line(seg(3, 7.5, 21, 7.5)),
            solid(rect(10, 4, 4, 2.5, rnd(S, 0.3, 1))), line(seg(2.5, 13, 4.5, 13)), line(seg(19.5, 13, 21.5, 13))]


@icon("oven", CAT, "A kitchen oven with a window and knobs", tags=["stove", "range", "bake", "kitchen", "appliance"],
      aliases=["stove"])
def _(S):
    return [shell(rect(3.5, 3, 17, 18, rnd(S, 2, 4))), detail(seg(3.5, 8, 20.5, 8)), dot(7.5, 5.5, 1), dot(11, 5.5, 1),
            detail(rect(7, 11.5, 10, 6, rnd(S, 0.5, 1.5)))]


@icon("microwave", CAT, "A microwave oven", tags=["appliance", "kitchen", "heat", "reheat", "oven"])
def _(S):
    return [shell(rect(2.5, 5, 19, 14, rnd(S, 2, 3.5))), detail(rect(5.5, 8, 9, 8, rnd(S, 0.5, 1.5))),
            detail(seg(17, 5, 17, 19)), dot(19.2, 9, 0.9), dot(19.2, 12.5, 0.9)]


@icon("toaster", CAT, "A toaster with toast popping up", tags=["toast", "breakfast", "appliance", "kitchen", "bread"])
def _(S):
    body = rect(3, 10.5, 18, 10, rnd(S, 2.5, 4))
    slices = [rect(6, 3, 5, 9, rnd(S, 1.5, 2.5)), rect(13, 3, 5, 9, rnd(S, 1.5, 2.5))]
    return [shell(body), *(shell(behind(sl, [body], 1.25)) for sl in slices), dot(17.5, 15.5, 1.2)]


@icon("blender", CAT, "A countertop blender", tags=["mixer", "smoothie", "appliance", "kitchen", "juice"])
def _(S):
    jug = poly([(6, 3.5), (18, 3.5), (16.5, 15), (7.5, 15)], closed=True, r=S.r)
    base = rect(6, 15, 12, 6, rnd(S, 1.5, 2.5))
    return [shell(jug), shell(base), detail(seg(6.5, 15, 17.5, 15)), detail(seg(6.3, 6.5, 17.7, 6.5)), dot(12, 18, 1.2),
            detail(seg(10, 11.5, 14, 9.5))]


@icon("grill", CAT, "A kettle barbecue grill", tags=["bbq", "barbecue", "cookout", "grilling", "outdoor"],
      aliases=["bbq", "barbecue"])
def _(S):
    top = 9
    bowl_d = f"M3 {top}H21A9 8 0 0 1 3 {top}Z"
    return [shell(bowl_d if S.name == "line" else f"M4.5 {top}H19.5A1.5 1.5 0 0 1 21 {top + 1.5}A9 7 0 0 1 3 {top + 1.5}A1.5 1.5 0 0 1 4.5 {top}Z"),
            line(seg(8.5, 16.2, 6.5, 21.5)), line(seg(15.5, 16.2, 17.5, 21.5)),
            line("M8.5 2.5C7.5 3.7 9.5 5 8.5 6.5"), line("M12 2.5C11 3.7 13 5 12 6.5"), line("M15.5 2.5C14.5 3.7 16.5 5 15.5 6.5")]


@icon("salt", CAT, "A salt shaker", tags=["salt-shaker", "seasoning", "spice", "condiment", "table"])
def _(S):
    cap = "M8 9C8 5.5 9.8 3.5 12 3.5C14.2 3.5 16 5.5 16 9Z"
    body = poly([(8, 9), (16, 9), (17.5, 21), (6.5, 21)], closed=True, r=S.r)
    return [shell(cap), shell(body), detail(seg(7.5, 9, 16.5, 9)), dot(10.5, 6.8, 0.8), dot(13.5, 6.8, 0.8),
            detail(seg(7.6, 14, 16.4, 14))]


@icon("pepper-shaker", CAT, "A pepper mill", tags=["pepper", "pepper-mill", "grinder", "seasoning", "spice"],
      aliases=["pepper-mill"])
def _(S):
    body = poly([(8, 9.5), (16, 9.5), (15, 15.5), (17, 21), (7, 21), (9, 15.5)], closed=True, r=S.r)
    cap = "M7.5 9.5C7.5 6.5 9.5 5 12 5C14.5 5 16.5 6.5 16.5 9.5Z"
    return [shell(cap), shell(body), detail(seg(7, 9.5, 17, 9.5)), line(seg(12, 5, 12, 2)), detail(seg(9, 15.5, 15, 15.5))]


@icon("ketchup", CAT, "A squeeze bottle of ketchup", tags=["sauce", "condiment", "tomato", "squeeze-bottle", "mustard"])
def _(S):
    cap = poly([(9, 8.5), (10.5, 5.5), (13.5, 5.5), (15, 8.5)], closed=True, r=rnd(S, 0, 0.5))
    return [shell(rect(7, 8.5, 10, 13, rnd(S, 2, 4))), shell(cap), detail(seg(8, 8.5, 16, 8.5)), line(seg(12, 5.5, 12, 2.5)),
            detail(circle(12, 15, 2.3))]
