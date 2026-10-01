"""TypeIcon Core: mythical creatures, legends and folklore (batch 002)."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "mythical"


# --------------------------------------------------------------------------- local helpers

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


def flip(d):
    """Mirror a d-string across the vertical centre line."""
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


def grow(d, g):
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def mark(d):
    return Part("dot", d)


def _p(p):
    return f"{fmt(p[0])} {fmt(p[1])}"


def tip(a, p, b, r):
    """Corner at p: sharp when r == 0, softened with a quadratic when r > 0."""
    if r <= 0:
        return "L" + _p(p)
    la = math.hypot(a[0] - p[0], a[1] - p[1])
    lb = math.hypot(b[0] - p[0], b[1] - p[1])
    t = min(r, la / 2, lb / 2)
    s = (p[0] + (a[0] - p[0]) * t / la, p[1] + (a[1] - p[1]) * t / la)
    e = (p[0] + (b[0] - p[0]) * t / lb, p[1] + (b[1] - p[1]) * t / lb)
    return "L" + _p(s) + "Q" + _p(p) + " " + _p(e)


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def tube(ctrl, width, n=16):
    """Closed outline around a cubic centreline whose width varies with t."""
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        x, y = bez(*ctrl, t)
        x2, y2 = bez(*ctrl, min(1, t + 1e-3))
        x1, y1 = bez(*ctrl, max(0, t - 1e-3))
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy)
        nx, ny = -dy / ln, dx / ln
        w = width(t) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return left + right[::-1]


def rpts(pts, deg, cx, cy):
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * sn, cy + (x - cx) * sn + (y - cy) * c) for x, y in pts]


def rline(p0, p1, deg, cx, cy):
    a, b = rpts([p0, p1], deg, cx, cy)
    return seg(a[0], a[1], b[0], b[1])


def pt(c, r, deg):
    return (c[0] + r * math.cos(math.radians(deg)), c[1] + r * math.sin(math.radians(deg)))


def star4(cx, cy, r, k=0.3):
    return poly([(cx, cy - r), (cx + r * k, cy - r * k), (cx + r, cy), (cx + r * k, cy + r * k),
                 (cx, cy + r), (cx - r * k, cy + r * k), (cx - r, cy), (cx - r * k, cy - r * k)], closed=True)


# --------------------------------------------------------------------------- objects and relics

@icon("trident", CAT, "Three-pronged spear with barbed tips on a long shaft",
      tags=["poseidon", "neptune", "sea god", "spear", "fork", "myth"])
def _(S):
    r = L(S, 0, 0.5)
    def head(x):
        return solid(poly([(x, 2), (x - 2, 5.5), (x + 2, 5.5)], closed=True, r=r))
    return [line("M6 5V8.5a6 6 0 0 0 12 0V5"), line("M12 4V22"), head(6), head(12), head(18)]


@icon("caduceus", CAT, "Winged staff with two snakes twisting around it",
      tags=["hermes", "mercury", "messenger", "medical", "staff", "snakes"])
def _(S):
    wing = "M11 9.5C8.5 6 5.5 5 2.5 5.5C4 8.5 7 10.5 11 11Z"
    return [line("M12 7V22"), shell(wing), shell(flip(wing)), dot(12, 4.6, 1.6),
            line("M12 20C7 18.5 7 15.5 12 14.5C17 13.5 17 11 12 10"),
            line("M12 20C17 18.5 17 15.5 12 14.5C7 13.5 7 11 12 10")]


@icon("labyrinth", CAT, "Circular maze of nested rings with a gap in each ring",
      tags=["maze", "minotaur", "crete", "puzzle", "path", "meditation"])
def _(S):
    return [line(arc(12, 12, 9, 115, 425)), line(arc(12, 12, 4.8, -55, 235)), dot(12, 12, 1.4)]


@icon("winged-sandal", CAT, "Strapped sandal with a small feathered wing at the ankle",
      tags=["hermes", "talaria", "mercury", "fast", "speed", "greek"])
def _(S):
    r = L(S, 0, 1.2)
    shoe = poly([(9.5, 11), (14, 11), (14.5, 14.5), (19, 15.5), (21, 19), (5, 19), (5, 14)], closed=True, r=r)
    wing = "M9 12C4 13 2 8 3 3.5C7 4 10 7 10.5 10.5Z"
    return [shell(shoe), shell(wing), detail("M14 13.5L9.5 15")]


@icon("mjolnir", CAT, "Short-handled war hammer with a wide head and a wrist loop",
      tags=["thor", "norse", "viking", "hammer", "thunder", "asgard"])
def _(S):
    a, cx, cy = 35, 12, 11
    head = poly(rpts([(6, 4), (18, 4), (18, 10.5), (6, 10.5)], a, cx, cy), closed=True, r=L(S, 0, 2))
    c = rpts([(12, 17.8)], a, cx, cy)[0]
    return [shell(head), detail(rline((10, 5), (10, 9.5), a, cx, cy)), detail(rline((14, 5), (14, 9.5), a, cx, cy)),
            line(rline((12, 10.5), (12, 15.6), a, cx, cy)), shell(circle(c[0], c[1], 2.2))]


@icon("winged-helmet", CAT, "Rounded helmet with a feathered wing on each side",
      tags=["valkyrie", "norse", "viking", "hermes", "wings", "knight"])
def _(S):
    helm = "M8 18V12.5A4 4 0 0 1 16 12.5V18Z"
    wing = "M8 14.5C4 14.5 2 10.5 2.5 5C6 5.5 9.5 8.5 9.5 12Z"
    feather = "M4.8 9.5C6.3 11 7 12 8 13"
    return [shell(helm), shell(wing), shell(flip(wing)), detail(feather), detail(flip(feather)), detail("M8 16H16")]


@icon("rune-stone", CAT, "Tall upright standing stone carved with a rune",
      tags=["runestone", "viking", "norse", "monolith", "menhir", "carved"])
def _(S):
    stone = poly([(6, 21.5), (6.5, 8), (10, 2.5), (16.5, 3.5), (18, 9), (17.5, 21.5)], closed=True, r=L(S, 0, 1.5))
    return [shell(stone), detail("M10.8 8V17"), detail("M10.8 10L14 8"), detail("M10.8 14L14 12")]


@icon("holy-grail", CAT, "Ornate chalice on a tall stem with short rays above the rim",
      tags=["chalice", "cup", "arthurian", "quest", "knights", "legend"])
def _(S):
    cup = "M6.5 8.5H17.5C17.5 13 15.5 15 12 15C8.5 15 6.5 13 6.5 8.5Z"
    return [shell(cup), line("M12 15V20"), line("M8.5 20.5H15.5"),
            line("M12 2.5V4.5"), line("M6.5 3.5L8 5"), line("M17.5 3.5L16 5")]


@icon("magic-lamp", CAT, "Oil lamp with a curved spout and handle and a curl of smoke",
      tags=["genie", "aladdin", "wish", "arabian", "oil lamp", "djinn"])
def _(S):
    r = L(S, 0, 1.5)
    body = "M6 12H19C19 16.2 16 18.5 12.5 18.5C9 18.5 6.3 16.2 6 12Z"
    return [shell(body), line("M6.5 12.5C4.5 12.5 3.3 10.5 3 8.5"), line("M19 12.5C22 12 22 16.5 18 16.5"),
            shell("M9.5 12C9.5 9 15.5 9 15.5 12"), line("M12.5 18.5V21"), line("M9 21.5H16"),
            line("M3 6C2 4.5 4 3.5 3.5 2")]


@icon("dragon-eye", CAT, "Almond reptile eye with a slit pupil and a spiky brow ridge",
      tags=["reptile eye", "serpent", "slit pupil", "fantasy", "fire", "gaze"])
def _(S):
    r = L(S, 0, 1.5)
    eye = "M2.5 14.5C6 9.5 18 9.5 21.5 14.5C18 19.5 6 19.5 2.5 14.5Z"
    return [shell(eye), detail("M12 11.5V17.5"),
            line(poly([(4, 8.5), (6.5, 4), (9, 6.5), (12, 3), (15, 6.5), (17.5, 4), (20, 8.5)], r=r))]


@icon("dragon-egg", CAT, "Egg covered in scales with a small crack near the top",
      tags=["hatch", "hatching", "scales", "fantasy", "wyrm", "nest"])
def _(S):
    egg = ("M12 2.5C16.5 2.5 19 9 19 14C19 18.5 16 21.5 12 21.5C8 21.5 5 18.5 5 14C5 9 7.5 2.5 12 2.5Z")
    return [shell(egg), detail("M8 8.5L10.3 6.8L12 9L13.8 6.8L16 8.5"), detail("M9 13.5a3 3 0 0 0 6 0"),
            detail("M7.5 18a2.5 2.5 0 0 0 4 0"), detail("M12.5 18a2.5 2.5 0 0 0 4 0")]


@icon("unicorn-horn", CAT, "Long spiral horn tapering to a point with a small sparkle",
      tags=["narwhal", "spiral", "magic", "fantasy", "horn", "unicorn"])
def _(S):
    r = L(S, 0, 0.8)
    def edges(y):
        t = (21 - y) / 18
        return 6.5 + t * 4, 14.5 - t * 4
    grooves = []
    for y in (16.5, 12.5, 8.5):
        a, b = edges(y)
        grooves.append(detail(f"M{fmt(a)} {fmt(y + 1.5)}L{fmt(b)} {fmt(y - 1.5)}"))
    return [shell(poly([(6.5, 21), (10.5, 3), (14.5, 21)], closed=True, r=r)), *grooves, solid(star4(19, 7, 3))]


@icon("cauldron", CAT, "Round-bellied pot on small legs over a flame with rising bubbles",
      tags=["witch", "potion", "brew", "halloween", "magic", "pot"])
def _(S):
    body = "M4.5 9.5H19.5C20 14 17 16.5 12 16.5C7 16.5 4 14 4.5 9.5Z"
    return [shell(body), line("M8 16.5L7 19.5"), line("M16 16.5L17 19.5"),
            solid(poly([(12, 17), (10.3, 20.3), (12, 21.5), (13.7, 20.3)], closed=True, r=0.4)),
            dot(9.5, 5.5, 1.3), dot(13.5, 3.8, 1.1), dot(15.5, 6.3, 1)]


@icon("sword-in-stone", CAT, "Sword stuck upright in a rounded boulder",
      tags=["excalibur", "arthur", "king", "legend", "blade", "camelot"])
def _(S):
    a, cx, cy = 14, 12, 16
    stone = poly([(2.5, 21.5), (3.5, 18.5), (8, 17), (16, 17.3), (20.5, 18.8), (21.5, 21.5)], closed=True, r=L(S, 0, 1.5))
    blade = poly(rpts([(9.5, 8), (14.5, 8), (14.5, 18), (9.5, 18)], a, cx, cy), closed=True, r=0)
    guard = "M" + " ".join(f"{fmt(x)} {fmt(y)}" for x, y in rpts([(5, 7.5)], a, cx, cy)) + "Q" + " ".join(
        f"{fmt(x)} {fmt(y)}" for x, y in rpts([(12, 10), (19, 7.5)], a, cx, cy))
    return [shell(minus(blade, stone)), shell(stone), line(guard),
            line(rline((12, 3.5), (12, 8), a, cx, cy)), dot(*rpts([(12, 2.6)], a, cx, cy)[0], 1.4)]


# --------------------------------------------------------------------------- folk and monsters

@icon("elf", CAT, "Elf face with long pointed ears and a fringe of hair",
      tags=["fantasy", "pointed ears", "legolas", "woodland", "fae", "santa helper"])
def _(S):
    r = L(S, 0, 0.8)
    ear = poly([(7, 10.5), (1.8, 5), (6.8, 15.5)], closed=True, r=r)
    body = union(ellipse(12, 12.5, 5.6, 7.5), ear, flip(ear))
    return [shell(body), detail("M6.6 10.5C8 7.2 14 6 17.6 10.5"), dot(9.5, 13.3), dot(14.5, 13.3),
            line("M10.6 17.2Q12 18.2 13.4 17.2")]


@icon("goblin", CAT, "Goblin head with big pointed ears, a hooked nose and a toothy grin",
      tags=["orc", "gremlin", "fantasy", "monster", "green", "creature"])
def _(S):
    r = L(S, 0, 0.8)
    ear = poly([(7, 9.5), (1.5, 8), (2.5, 12.5), (7.2, 14.5)], closed=True, r=r)
    body = union(ellipse(12, 12.5, 5.5, 7), ear, flip(ear))
    return [shell(body), line("M8 9.5L11 11"), line("M16 9.5L13 11"),
            mark(poly([(12, 11.5), (13.6, 15), (10.4, 15)], closed=True, r=0.4)),
            detail("M8.3 17.5L9.6 19L11 17.5L12.4 19L13.8 17.5L15.2 19L16 17.5")]


@icon("gnome", CAT, "Bearded gnome with a tall pointed hat and a round nose",
      tags=["garden gnome", "dwarf", "hat", "beard", "fantasy", "folklore"])
def _(S):
    r = L(S, 0, 1)
    hat = poly([(5.5, 11), (11, 2), (18.5, 11)], closed=True, r=r)
    beard = "M6 10.5H18V14C18 18.5 15 21.5 12 21.5C9 21.5 6 18.5 6 14Z"
    return [shell(union(hat, beard)), detail("M5.5 10.8H18.5"), dot(12, 14, 1.8)]


@icon("dwarf", CAT, "Stocky dwarf face with a round helmet and a long braided beard",
      tags=["fantasy", "miner", "helmet", "beard", "axe", "underground"])
def _(S):
    r = L(S, 0, 1)
    helm = "M5.5 10.5A6.5 6.5 0 0 1 18.5 10.5Z"
    beard = poly([(5.5, 9.5), (18.5, 9.5), (18.5, 15), (15, 21.5), (12, 18.5), (9, 21.5), (5.5, 15)], closed=True, r=r)
    return [shell(union(helm, beard)), detail("M5 10H19"), line("M12 3V5"), dot(9.5, 12.3), dot(14.5, 12.3),
            mark(circle(12, 14.6, 1.3))]


@icon("vampire", CAT, "Pale face with widow's peak hair, two fangs and a high cape collar",
      tags=["dracula", "count", "fangs", "halloween", "undead", "blood"])
def _(S):
    r = L(S, 0, 1)
    collar = poly([(3.2, 3.5), (9, 13), (15, 13), (20.8, 3.5), (20.8, 21), (3.2, 21)], closed=True, r=r)
    face = ellipse(12, 11.5, 5, 6.5)
    return [shell(minus(collar, grow(face, 3.2))), shell(face), mark(poly([(7.3, 9), (12, 11), (16.7, 9), (16.7, 6.5), (7.3, 6.5)], closed=True)),
            solid(poly([(9.5, 14.8), (11, 14.8), (10.3, 17.3)], closed=True)), solid(poly([(13, 14.8), (14.5, 14.8), (13.7, 17.3)], closed=True))]


@icon("mummy", CAT, "Head wrapped in diagonal bandages with one eye peeking through",
      tags=["egypt", "pharaoh", "bandages", "halloween", "undead", "wrapped"])
def _(S):
    return [shell(rect(6, 3, 12, 18, L(S, 4, 6))), detail("M6 8.5L18 5.5"), detail("M6 15.5L18 12.5"),
            detail("M6 20L15 17.5"), dot(10.5, 10.5, 1.3), dot(15, 9.3, 1.3)]


@icon("grim-reaper", CAT, "Hooded cloaked figure with an empty face holding a scythe",
      tags=["death", "scythe", "halloween", "reaper", "hood", "skeleton"])
def _(S):
    cloak = "M9 8C5.8 8 4.3 10.5 4.3 13.5L3 21.5H15L13.7 13.5C13.7 10.5 12.2 8 9 8Z"
    return [shell(cloak), mark(ellipse(9, 12.5, 2.3, 2.8)), line("M19 3.5L18 22"), line("M19 3.5C15 1.8 10 2.3 7 5")]


@icon("zombie", CAT, "Decaying hand reaching up out of the ground beside a tombstone",
      tags=["undead", "graveyard", "halloween", "hand", "grave", "rising"])
def _(S):
    return [line("M2.5 21.5H21.5"), shell(rect(3, 11, 9, 5, L(S, 1.5, 2.5))), line("M4.3 11V5.5"), line("M7.6 11V3.5"),
            line("M10.9 11V5"), line("M7.6 16V21"),
            shell("M14.5 21V11.5A3.5 3.5 0 0 1 21.5 11.5V21Z"), detail("M18 10V15"), detail("M16.3 12H19.7")]


@icon("oni", CAT, "Demon mask with two horns, angry eyes and a fanged grin",
      tags=["demon", "japanese", "ogre", "mask", "horns", "yokai"])
def _(S):
    r = L(S, 0, 0.8)
    horn = poly([(7.5, 6.5), (5.8, 3), (10.5, 5.3)], closed=True, r=r)
    face = "M5 8.5C5 6 19 6 19 8.5V14.5C19 18.8 15.5 21.5 12 21.5C8.5 21.5 5 18.8 5 14.5Z"
    return [shell(union(face, horn, flip(horn))), dot(9, 11, 1.4), dot(15, 11, 1.4),
            detail("M8 15.5L9.5 18L11 15.6L13 15.6L14.5 18L16 15.5")]


@icon("tengu", CAT, "Round mask with a very long nose, bushy brow and a small cap",
      tags=["japanese", "yokai", "long nose", "mask", "goblin", "folklore"])
def _(S):
    r = L(S, 0, 0.8)
    tipx = L(S, 19.5, 21)
    nose = poly([(13, 10), (tipx, 15), (13, 19)], closed=True, r=r)
    head = union(circle(9, 13.5, 7), nose, rect(5.5, 2.5, 7, 5.5, L(S, 0.5, 1.5)))
    return [shell(head), detail("M4.5 9.5L12 11.5"), dot(9, 13.8, 1.3), detail("M5.5 7H12.5")]


@icon("slime-monster", CAT, "Rounded gooey blob with drips at its base and a small smile",
      tags=["slime", "blob", "ooze", "gel", "jelly", "game monster"])
def _(S):
    body = union(ellipse(12, 12.5, 8.5, 7.5), rect(4.5, 16, 3.2, 5.5, 1.6), rect(15.5, 16, 3.2, 4, 1.6), rect(10.3, 17, 2.8, 4.5, 1.4))
    return [shell(body), dot(9, 11.5, 1.3), dot(15, 11.5, 1.3), detail("M10 14.8Q12 16.5 14 14.8")]


@icon("mimic-chest", CAT, "Treasure chest with the lid open like a toothy mouth and a tongue",
      tags=["treasure", "trap", "dungeon", "monster", "rpg", "teeth"])
def _(S):
    return [shell("M4 10V7A3.5 3.5 0 0 1 7.5 3.5H16.5A3.5 3.5 0 0 1 20 7V10Z"),
            shell(rect(3.5, 14.5, 17, 7, L(S, 1.5, 2.5))),
            solid(poly([(6, 10), (9, 10), (7.5, 13.2)], closed=True)), solid(poly([(10.5, 10), (13.5, 10), (12, 13.2)], closed=True)),
            solid(poly([(15, 10), (18, 10), (16.5, 13.2)], closed=True)),
            dot(12, 18, 1.4)]


@icon("dragon-skull", CAT, "Side view of a large reptile skull with swept-back horns and teeth",
      tags=["skull", "bones", "wyrm", "fossil", "fantasy", "horn"])
def _(S):
    r = L(S, 0, 0.6)
    snout = poly([(2.5, 10), (3.2, 8.5), (12, 8), (12, 15.5), (10.5, 15.5), (9.5, 18), (8, 15.5), (6.5, 18), (5, 15.5), (3.2, 15.5)],
                 closed=True, r=r)
    horn = poly([(15.5, 6), (20.8, 3), (19.6, 9.5)], closed=True, r=r)
    return [shell(union(circle(14, 12, 6.2), snout, horn)), dot(14, 11, 1.9), dot(5.2, 11.3, 0.9)]


@icon("lucky-cat", CAT, "Seated cat figurine with a raised paw, a collar bell and a coin on its chest",
      tags=["maneki-neko", "beckoning cat", "fortune", "good luck", "japanese", "wealth"])
def _(S):
    r = L(S, 0, 0.6)
    ear = poly([(6.6, 7), (6.8, 2.8), (10.2, 4.3)], closed=True, r=r)
    ear2 = poly([(12.8, 4.3), (16.2, 2.8), (16.4, 7)], closed=True, r=r)
    body = union(ellipse(11.5, 8.5, 5.5, 4.8), ear, ear2, rect(5.5, 12, 12, 9.5, L(S, 3, 5)), ellipse(19.5, 9, 2.1, 3.8))
    return [shell(body), dot(9.3, 8.5, 1.1), dot(13.7, 8.5, 1.1), dot(11.5, 14.3, 1.3), detail(circle(11.5, 18.3, 2.2))]


@icon("nekomata", CAT, "Sitting cat in side view with two separate tails curling upward",
      tags=["two tails", "cat yokai", "japanese", "folklore", "spirit", "bakeneko"])
def _(S):
    r = L(S, 0, 0.6)
    e1 = poly([(4.6, 6.5), (4.8, 2.5), (8, 4)], closed=True, r=r)
    e2 = poly([(9.3, 4), (12.3, 2.5), (12.5, 6.5)], closed=True, r=r)
    body = union(circle(8.5, 8.5, 4.6), e1, e2, ellipse(10.5, 16.5, 5.3, 5.3))
    return [shell(body), dot(7, 8.6, 1.1), dot(10.3, 8.6, 1.1),
            line("M15 17C19.5 17 20.5 12.5 18.5 9"), line("M15 20.5C21 20.5 22 14.5 21 11")]


@icon("umbrella-yokai", CAT, "Paper umbrella with one big eye, a tongue and a single leg",
      tags=["kasa-obake", "karakasa", "japanese", "yokai", "one eye", "haunted"])
def _(S):
    canopy = "M3 13.5A9 9 0 0 1 21 13.5Q18 11.5 15 13.5Q12 11.5 9 13.5Q6 11.5 3 13.5Z"
    return [shell(canopy), detail(circle(12, 8.3, 2.3)), dot(12, 8.3, 0.9),
            shell(rect(7.6, 13.5, 3.6, 5.5, 1.8)), line("M15.5 13V21"), line("M15.5 21H19.5")]


@icon("lantern-ghost", CAT, "Paper lantern with a split mouth and tongue and a single eye",
      tags=["chochin-obake", "japanese", "yokai", "haunted", "paper lantern", "spooky"])
def _(S):
    body = union(ellipse(12, 12.5, 6.5, 7.5), rect(8.3, 3.3, 7.4, 3, L(S, 0.5, 1.4)), rect(8.3, 18.7, 7.4, 3, L(S, 0.5, 1.4)))
    return [shell(body), dot(12, 9, 2), detail("M8.6 14.5Q12 18 15.4 14.5")]


@icon("baba-yaga-hut", CAT, "Small hut standing on two long scaly chicken legs with clawed feet",
      tags=["witch", "russian", "folklore", "cabin", "fairy tale", "chicken legs"])
def _(S):
    r = L(S, 0, 0.8)
    hut = poly([(4, 10.5), (12, 3), (20, 10.5), (18, 10.5), (18, 15.5), (6, 15.5), (6, 10.5)], closed=True, r=r)
    return [shell(hut), detail(rect(10, 10.5, 4, 5)), line("M8.5 15.5V19.5"), line("M15.5 15.5V19.5"),
            line("M5 21.5L8.5 19.5L11.5 21.5"), line("M12.5 21.5L15.5 19.5L19 21.5")]


@icon("pandora-box", CAT, "Ornate box with its lid lifted and rays of light escaping",
      tags=["pandora", "greek", "myth", "curiosity", "evils", "mystery box"])
def _(S):
    return [shell(rect(4.5, 13.5, 15, 8, L(S, 1.5, 2.5))), shell(poly([(4.5, 10.8), (4.5, 7.8), (19.5, 5.5), (19.5, 9)], closed=True, r=L(S, 0, 1))),
            line("M8 4.8L6.5 2.5"), line("M12 4V2"), dot(12, 17.5, 1.4)]


@icon("pot-of-gold", CAT, "Round pot heaped with gold coins beneath a rainbow arc",
      tags=["leprechaun", "rainbow", "irish", "treasure", "lucky", "saint patrick"])
def _(S):
    pot = "M7 14.5H17C17.5 19 15.5 21.5 12 21.5C8.5 21.5 6.5 19 7 14.5Z"
    coins = union(circle(9.8, 13, 1.9), circle(14.2, 13, 1.9), circle(12, 11.3, 1.8))
    return [line(arc(12, 14.5, 10.5, 180, 360)), line(arc(12, 14.5, 7.4, 180, 360)), shell(union(pot, coins))]


@icon("flying-carpet", CAT, "Patterned carpet floating in a gentle wave with motion lines beneath",
      tags=["aladdin", "magic carpet", "arabian", "rug", "genie", "fantasy"])
def _(S):
    carpet = "M3 8C6 4.5 9 11.5 12 8C15 4.5 18 11.5 21 8V14C18 17.5 15 10.5 12 14C9 17.5 6 10.5 3 14Z"
    return [shell(carpet), dot(8, 10.2, 1), dot(12, 11, 1), dot(16, 10.2, 1), line("M5 20H10"), line("M13 20H19")]


@icon("will-o-wisp", CAT, "Floating teardrop flame hovering over tufts of marsh grass",
      tags=["wisp", "ghost light", "swamp", "marsh", "bog", "spirit flame"])
def _(S):
    r = L(S, 0, 1.6)
    flame = poly([(12, 2), (17.5, 10), (17.5, 13), (15.5, 16), (8.5, 16), (6.5, 13), (6.5, 10)], closed=True, r=L(S, 0, 3))
    if S.name == "line":
        flame = "M12 2.5C14 6.5 17.5 8.8 17.5 12.5C17.5 15.3 15.2 17 12 17C8.8 17 6.5 15.3 6.5 12.5C6.5 8.8 10 6.5 12 2.5Z"
    return [shell(flame), detail("M12 10C13.2 11.3 13.6 12 13.6 12.9C13.6 13.8 12.9 14.4 12 14.4C11.1 14.4 10.4 13.8 10.4 12.9C10.4 12 11 11.3 12 10Z"),
            line("M2.5 21.5H21.5"), line(poly([(4.5, 21.5), (5.5, 19.3), (6.5, 21.5)])), line(poly([(17.5, 21.5), (18.5, 19.3), (19.5, 21.5)]))]


@icon("treant", CAT, "Walking tree with a face in its trunk, branch arms and root feet",
      tags=["ent", "tree spirit", "forest", "living tree", "fantasy", "guardian"])
def _(S):
    canopy = union(circle(8, 7, 3.6), circle(12, 5.2, 3.8), circle(16, 7, 3.6), rect(8, 8, 8, 11, L(S, 1, 2)))
    return [shell(canopy), dot(10.3, 12, 1.1), dot(13.7, 12, 1.1), detail("M10.2 15.6Q12 17 13.8 15.6"),
            line("M8 13.5L4 15.5L2.8 12"), line("M16 13.5L20 15.5L21.2 12"),
            line("M9.5 19L7 21.5"), line("M14.5 19L17 21.5")]


@icon("green-man", CAT, "Face formed from a ring of leaves with a leaf growing from the mouth",
      tags=["foliate head", "woodland", "celtic", "nature spirit", "leaves", "folklore"])
def _(S):
    def leafp(a):
        b = pt((12, 13), 4.5, a)
        t = pt((12, 13), 10.2, a)
        l = pt((12, 13), 7.4, a - 17)
        rr = pt((12, 13), 7.4, a + 17)
        return poly([b, l, t, rr], closed=True, r=L(S, 0, 0.8))
    leaves = [leafp(a) for a in (-180, -150, -120, -90, -60, -30, 0)]
    return [shell(union(circle(12, 13, 5.8), *leaves)), dot(9.7, 12.2, 1.1), dot(14.3, 12.2, 1.1),
            detail("M12 11.5V14.5"), detail("M9.8 17.3H14.2")]


@icon("banshee", CAT, "Floating ghostly woman with long streaming hair and a wailing mouth",
      tags=["wail", "irish", "ghost", "spirit", "scream", "folklore"])
def _(S):
    body = "M12 2.5C7.5 2.5 6.2 6 6.2 9.5L3.8 20.5C5 21.3 6 20.6 7 19.6C8 21.2 9 21.2 10 19.8C11 21.3 13 21.3 14 19.8C15 21.2 16 21.2 17 19.6C18 20.6 19 21.3 20.2 20.5L17.8 9.5C17.8 6 16.5 2.5 12 2.5Z"
    return [shell(body), dot(10, 8.5, 1.1), dot(14, 8.5, 1.1), detail(ellipse(12, 13.2, 1.5, 2.3)),
            detail("M6.6 10C6.2 13 6 15 5.8 17") if False else detail("M8 6.2C9.5 5.2 14.5 5.2 16 6.2")]


@icon("loch-ness-monster", CAT, "Long-necked lake creature with a small head and two humps above waves",
      tags=["nessie", "scottish", "cryptid", "sea monster", "lake", "scotland"])
def _(S):
    neck = poly(tube(((8.5, 18), (8.5, 11.5), (5.5, 11), (5.5, 7)), lambda t: 3.6 - 1.2 * t, 12), closed=True, r=L(S, 0, 1))
    humps = union("M7.5 18.5A4 4.5 0 0 1 15.5 18.5Z", "M14.5 18.5A3.2 3.6 0 0 1 21 18.5Z", neck)
    return [shell(union(humps, ellipse(4.6, 5.9, 3.1, 2.1))), dot(3.9, 5.5, 0.8),
            line("M2.5 21.5Q4.5 20 6.5 21.5T10.5 21.5T14.5 21.5T18.5 21.5T21.5 21.5")]


@icon("golem", CAT, "Blocky stone giant built from heavy slabs with glowing eye slits",
      tags=["clay", "stone giant", "statue", "construct", "fantasy", "rock"])
def _(S):
    body = union(rect(9, 2.5, 6, 5.5, L(S, 0.5, 1.5)), rect(6, 8, 12, 8.5, L(S, 0.5, 1.5)), rect(2.5, 8.5, 3.5, 9.5, L(S, 0.5, 1.5)),
                 rect(18, 8.5, 3.5, 9.5, L(S, 0.5, 1.5)), rect(7, 16, 3.5, 5.5, L(S, 0.5, 1)), rect(13.5, 16, 3.5, 5.5, L(S, 0.5, 1)))
    return [shell(body), dot(10.6, 5.2, 0.9), dot(13.4, 5.2, 0.9), detail("M12 10.5L10.8 13L12.4 14.3")]


def petal(o, ang, r0, r1, w, r=0.0):
    """Pointed leaf from radius r0 to r1 around o at angle ang, width w."""
    b = pt(o, r0, ang)
    t = pt(o, r1, ang)
    m = (r0 + r1) / 2
    a = math.degrees(math.atan2(w / 2, m))
    c1 = pt(o, math.hypot(m, w / 2), ang - a)
    c2 = pt(o, math.hypot(m, w / 2), ang + a)
    return poly([b, c1, t, c2], closed=True, r=r)


@icon("moon-rabbit", CAT, "Full moon with a sitting rabbit silhouette inside",
      tags=["jade rabbit", "mid-autumn", "lunar", "tsukimi", "moon festival", "legend"])
def _(S):
    r = L(S, 0, 0.6)
    ear1 = poly([(13.6, 9.4), (12.6, 4.2), (14.8, 4.2), (15.6, 9.2)], closed=True, r=r)
    ear2 = poly([(15.8, 9.4), (16.4, 4.6), (18.6, 5.2), (17.8, 9.8)], closed=True, r=r)
    rabbit = union(ellipse(10.6, 15.6, 5.2, 4.1), circle(15.6, 11.6, 2.9), ear1, ear2, circle(5.4, 15, 1.6))
    extra = [mark(circle(6.2, 7, 0.9)), mark(circle(8.6, 9.2, 0.7))] if S.name == "rounded" else []
    return [shell(circle(12, 12, 9.5)), mark(rabbit)] + extra


@icon("jackalope", CAT, "Sitting rabbit in side view with branching deer antlers on its head",
      tags=["cryptid", "horned rabbit", "american folklore", "antlers", "hare", "tall tale"])
def _(S):
    r = L(S, 0, 0.6)
    ear = poly([(8.6, 10), (9.6, 5.6), (11.8, 6.4), (11.2, 10.8)], closed=True, r=r)
    body = union(ellipse(14, 16.6, 6.6, 4.6), circle(7.6, 13.2, 3.4), ear, circle(20.6, 15.6, 1.6), rect(3.8, 19, 6, 2.6, L(S, 1, 1.3)))
    return [shell(body), dot(6.6, 12.7, 0.9),
            line("M6.4 10.5L4.6 6.2L3.6 3"), line("M5.3 8L2.8 7"), line("M4.6 6.2L7 4.4")]


@icon("kappa", CAT, "Squat turtle-shelled river creature with a beak and a water dish on its head",
      tags=["japanese", "yokai", "water spirit", "river", "turtle", "cucumber"])
def _(S):
    shellb = poly([(4.5, 21.5), (5.3, 18), (8, 15.8), (16, 15.8), (18.7, 18), (19.5, 21.5)], closed=True, r=L(S, 0, 3))
    return [shell(ellipse(12, 10, 6.3, 5)), shell(ellipse(12, 3.4, 3.2, 1.3)), dot(9.6, 9.3, 1.1), dot(14.4, 9.3, 1.1),
            mark(poly([(10.2, 11.3), (13.8, 11.3), (12, 13.7)], closed=True, r=L(S, 0, 0.4))),
            shell(shellb), detail("M9 21.5L10.2 18.3H13.8L15 21.5")]


@icon("dragon-turtle", CAT, "Turtle with a domed shell and a horned dragon head with whiskers",
      tags=["sea monster", "fantasy", "shell", "black tortoise", "legend", "dragon"])
def _(S):
    r = L(S, 0, 0.8)
    dome = "M2.5 17.5C2.5 10.5 7 7.5 12 7.5C17 7.5 18 10 18 17.5Z"
    head = poly([(17, 13.5), (17.5, 9.5), (21.8, 9), (21.8, 12.6), (20.5, 14.2)], closed=True, r=r)
    return [shell(union(dome, head)), detail("M8.5 17.5L9.5 10.5"), detail("M13.5 17.5L13 10.5"),
            dot(20, 11, 0.8), line("M18.6 9.5L17.8 5.6"), line("M20.4 13.8Q20 16.3 21.6 17.5"),
            shell(rect(4.5, 17.5, 3.4, 3.5, L(S, 0.5, 1.2))), shell(rect(12.3, 17.5, 3.4, 3.5, L(S, 0.5, 1.2)))]


@icon("world-turtle", CAT, "Turtle swimming with a flat world disc and a small hill of land on its shell",
      tags=["great a'tuin", "cosmic", "myth", "creation", "earth", "tortoise"])
def _(S):
    r = L(S, 0, 0.8)
    body = union("M4 20C4 15 7.5 13 12 13C16.5 13 19 15 19 20Z",
                 poly([(17.5, 17), (18.5, 14), (21.6, 14.8), (21.6, 17.4), (20, 18.6)], closed=True, r=r),
                 rect(5.5, 19, 3.6, 2.6, L(S, 0.5, 1.2)), rect(13.5, 19, 3.6, 2.6, L(S, 0.5, 1.2)))
    return [shell(body), shell(ellipse(11.5, 9.5, 9, 1.8)), shell("M7.5 9.3A4.5 4.3 0 0 1 15.5 9.3Z"), dot(20, 15.6, 0.7)]


@icon("mothman", CAT, "Dark humanoid with large moth wings spread and two big glowing eyes",
      tags=["cryptid", "west virginia", "winged", "red eyes", "urban legend", "moth"])
def _(S):
    r = L(S, 0, 0.8)
    wing = poly([(9.5, 10), (2.5, 3.5), (2.6, 13.5), (9.3, 17.5)], closed=True, r=r)
    return [shell(wing), shell(flip(wing)), shell(ellipse(12, 6.6, 3.3, 3.9)), dot(10.6, 6.2, 1.25), dot(13.4, 6.2, 1.25),
            line("M12 10.8V17"), line("M12 17L10 21.5"), line("M12 17L14 21.5"), detail("M9.3 10.2L4.6 7.2") if False else detail("M8.6 11.5L5 8")]


@icon("yeti", CAT, "Shaggy furred creature with raised arms and a pale face",
      tags=["abominable snowman", "himalaya", "cryptid", "snow", "fur", "sasquatch"])
def _(S):
    body = poly([(9, 4.5), (12, 2.5), (15, 4.5), (16.2, 7.5), (19, 5), (21, 3.5), (20.6, 8.5), (19, 12), (21, 15), (18.5, 16.3),
                 (19.5, 20), (16, 19.3), (14.5, 21.5), (12, 19.5), (9.5, 21.5), (8, 19.3), (4.5, 20), (5.5, 16.3), (3, 15),
                 (5, 12), (3.4, 8.5), (3, 3.5), (5, 5), (7.8, 7.5)], closed=True, r=L(S, 0, 0.8))
    return [shell(body), detail(ellipse(12, 9, 3.4, 3.1)), dot(10.8, 8.6, 0.8), dot(13.2, 8.6, 0.8)]


@icon("rokurokubi", CAT, "Woman's head on a very long looping neck that trails back to a small body",
      tags=["stretching neck", "japanese", "yokai", "long neck", "ghost", "folklore"])
def _(S):
    r = L(S, 0, 0.8)
    return [shell(poly([(3, 21.5), (4.2, 17.5), (9.8, 17.5), (11, 21.5)], closed=True, r=r)),
            line("M7 17.5C2.5 12.5 9.5 9.5 12.3 13C15 16.5 19.5 13.5 17 9.5"),
            shell(union(circle(16.6, 6.7, 3.4), circle(16.6, 2.8, 1.6))), dot(15.4, 7, 0.9), dot(17.9, 7, 0.9)]


@icon("amphisbaena", CAT, "Wavy serpent with a head at each end, one facing up and one facing down",
      tags=["two-headed snake", "double head", "greek", "myth", "serpent", "ants"])
def _(S):
    if S.name == "line":
        h1 = poly([(3.8, 15.6), (7, 15.6), (7.4, 19), (5.4, 21), (3.4, 19)], closed=True)
        h2 = poly([(20.2, 8.4), (17, 8.4), (16.6, 5), (18.6, 3), (20.6, 5)], closed=True)
    else:
        h1 = rot(ellipse(5.4, 17.8, 1.9, 2.8), 12, 5.4, 17.8)
        h2 = rot(ellipse(18.6, 6.2, 1.9, 2.8), 12, 18.6, 6.2)
    return [line("M6 14.8C7 7.5 10.5 7 12 12C13.5 17 17 16.5 18 9.2"), shell(h1), shell(h2),
            dot(5.3, 18, 0.6), dot(18.7, 6, 0.6)]


@icon("hydra", CAT, "Serpent body with five long necks fanning upward, each ending in a snake head",
      tags=["many heads", "greek", "heracles", "monster", "serpent", "lernaean"])
def _(S):
    def head(x, y, sgn):
        return shell(ellipse(x + sgn * 1.4, y, 2.3, 1.5))
    return [shell(ellipse(12, 19.6, 7.5, 2.4)),
            line("M8.8 18C7 14 9 12 4.6 12C3.6 12 3.4 11 3.5 10"),
            line("M10.4 17.8C9 13 10.5 10 8 7.5"),
            line("M12 17.6V5"),
            line("M13.6 17.8C15 13 13.5 10 16 7.5"),
            line("M15.2 18C17 14 15 12 19.4 12C20.4 12 20.6 11 20.5 10"),
            shell(ellipse(3.2, 8, 1.6, 2.2)), shell(ellipse(7.2, 5.7, 1.6, 2.2)), shell(ellipse(12, 3.3, 1.8, 2)),
            shell(ellipse(16.8, 5.7, 1.6, 2.2)), shell(ellipse(20.8, 8, 1.6, 2.2))]


@icon("sea-serpent", CAT, "Serpent looping in several arches above wavy water with a dragon-like head",
      tags=["sea monster", "leviathan", "ocean", "sailor legend", "dragon", "nautical"])
def _(S):
    r = L(S, 0, 0.6)
    return [line("M2.5 19A3 5 0 0 1 8.5 19"), line("M8.5 19A3 6.3 0 0 1 14.5 19"),
            line("M14.5 19C14.5 13 18 12 18 8.5"),
            shell(poly([(16.2, 8.6), (16.6, 4.6), (21.6, 6.2), (21.6, 8.8), (19.5, 9.6)], closed=True, r=r)),
            dot(19.4, 6.8, 0.8), line("M17 4.8L16 2.6"),
            line("M2.5 21.5Q4.5 20 6.5 21.5T10.5 21.5T14.5 21.5T18.5 21.5T21.5 21.5")]


@icon("fairy", CAT, "Tiny figure with a star-tipped wand and two pairs of rounded insect wings",
      tags=["pixie", "sprite", "wings", "tinker bell", "magic", "fae"])
def _(S):
    wing_u = rot(ellipse(4.8, 8.4, 2.2, 4.4), 22, 4.8, 8.4)
    wing_l = rot(ellipse(6.2, 16, 1.9, 3), -32, 6.2, 16)
    fig = union(circle(12, 6, 2.6), poly([(12, 9.4), (8.6, 19.5), (15.4, 19.5)], closed=True, r=L(S, 0, 0.8)))
    return [shell(wing_u), shell(wing_l), shell(fig),
            line("M14.6 12L19 8.5"), solid(star4(20.3, 5.4, 2.6))]


@icon("imp", CAT, "Small mischievous devil with little horns, bat wings and a pointed tail",
      tags=["minor demon", "devil", "mischief", "horns", "hell", "gremlin"])
def _(S):
    r = L(S, 0, 0.6)
    wing = poly([(8.5, 11.5), (3.6, 6.5), (4.4, 11), (3.5, 14.5), (6.2, 13.6), (8.5, 16.5)], closed=True, r=r)
    horn = poly([(9.3, 6.2), (8.4, 3), (11, 5)], closed=True, r=r)
    head = union(ellipse(12, 9.3, 4.2, 4), horn, flip(horn))
    return [shell(wing), shell(flip(wing)), shell(head), dot(10.4, 9, 0.9), dot(13.6, 9, 0.9), line("M10.5 11.4H13.5"),
            shell(poly([(9.8, 14.5), (14.2, 14.5), (13.2, 19.5), (10.8, 19.5)], closed=True, r=r)),
            line("M12 19.5C12 21.6 16 21.6 17.5 19"), solid(poly([(16.2, 17.2), (19.5, 18.3), (17.4, 20.3)], closed=True))]


@icon("troll", CAT, "Heavy-browed troll face with a big bulbous nose and two upward tusks",
      tags=["ogre", "monster", "fantasy", "bridge", "tusks", "norse"])
def _(S):
    head = union(circle(12, 11.5, 7.6), ellipse(4.3, 11, 1.8, 2.4), ellipse(19.7, 11, 1.8, 2.4))
    return [shell(head), line("M7.2 8.3L10.8 9.4"), line("M16.8 8.3L13.2 9.4"), dot(9.4, 10.6, 0.9), dot(14.6, 10.6, 0.9),
            mark(ellipse(12, 13.3, 2.2, 1.7)), detail("M8 17H16"),
            solid(poly([(8.3, 17.4), (10.2, 17.4), (9.2, 14.6)], closed=True)), solid(poly([(13.8, 17.4), (15.7, 17.4), (14.8, 14.6)], closed=True))]


@icon("trojan-horse", CAT, "Large wooden horse statue on a wheeled platform with plank lines",
      tags=["greek", "troy", "wooden horse", "war", "ruse", "gift"])
def _(S):
    r = L(S, 0, 0.8)
    head = poly([(12.5, 10), (15, 5), (18, 2.8), (21.6, 7.4), (19.6, 8.6), (18.2, 7), (17, 10.5)], closed=True, r=r)
    body = union(rect(3.5, 9.5, 13.5, 6.5, L(S, 0.5, 1.5)), head, rect(5, 15, 2.6, 4, 0.4), rect(13.6, 15, 2.6, 4, 0.4))
    return [shell(body), detail("M8 10.6V14.8"), detail("M12 10.6V14.8"), dot(17.8, 5.6, 0.8),
            line("M3 20H18"), dot(6.5, 21.2, 0.9), dot(14.5, 21.2, 0.9)]


@icon("werewolf", CAT, "Wolf head howling up at a full moon", 
      tags=["lycanthrope", "wolfman", "full moon", "howl", "halloween", "monster"])
def _(S):
    r = L(S, 0, 0.8)
    wolf = poly([(3.5, 21.5), (4, 15), (6, 11.5), (5.6, 6.8), (9, 9.4), (11.4, 9), (13.4, 12), (16, 10.5), (16.4, 12.5), (12.6, 14.5),
                 (12, 16), (13.6, 21.5)], closed=True, r=r)
    return [shell(wolf), shell(circle(17, 5.3, 3.8)), dot(9.2, 12, 0.9)]


@icon("chinese-dragon", CAT, "Long wingless serpentine dragon with a whiskered horned head, small clawed legs and a wavy body",
      tags=["loong", "oriental", "lunar new year", "asian", "serpent", "auspicious"])
def _(S):
    r = L(S, 0, 0.8)
    ctrl = ((2.8, 18), (8, 6.5), (13, 26), (18, 12))
    body = poly(tube(ctrl, lambda t: 1.4 + 1.8 * math.sin(math.pi * t) + 0.6, 22), closed=True, r=L(S, 0, 1.2))
    head = poly([(15.6, 11.6), (17, 6.8), (21.6, 6.2), (21.8, 9.6), (19.4, 12.4)], closed=True, r=r)
    legs = []
    for t in (0.28, 0.62):
        x, y = bez(*ctrl, t)
        legs.append(line(f"M{fmt(x)} {fmt(y + 1.5)}L{fmt(x + 0.3)} {fmt(y + 4.2)}"))
    return [shell(union(body, head)), dot(19.6, 8.4, 0.8), line("M17.8 6.4L17.2 3.2"), line("M21.4 10.2Q22.2 12 21.4 13.6")] + legs


@icon("guardian-lion", CAT, "Seated lion statue with a curly mane and one paw resting on a ball on a square plinth",
      tags=["foo dog", "shishi", "temple lion", "stone lion", "chinese", "statue"])
def _(S):
    mane = union(circle(12, 7, 3.6), *[circle(*pt((12, 7), 4.8, a), 1.5) for a in range(0, 360, 45)])
    body = union(poly([(8, 11.5), (16, 11.5), (17.2, 18.5), (6.8, 18.5)], closed=True, r=L(S, 0, 1.2)), mane)
    return [shell(body), dot(10.6, 6.6, 0.8), dot(13.4, 6.6, 0.8), mark(poly([(11.2, 8.2), (12.8, 8.2), (12, 9.2)], closed=True)),
            shell(rect(4, 18.5, 16, 3.3, L(S, 0.5, 1.6))), detail("M12 12.6V17.5")]


@icon("tanuki-statue", CAT, "Round-bellied raccoon dog figurine with a wide straw hat and a sake flask",
      tags=["japanese", "raccoon dog", "shigaraki", "lucky", "statue", "restaurant"])
def _(S):
    hat = poly([(3.3, 9), (12, 2.6), (20.7, 9)], closed=True, r=L(S, 0, 1))
    body = union(hat, ellipse(12, 11.6, 4.4, 3.3), ellipse(11, 17.4, 7, 4.6), rect(16.8, 13.2, 3.8, 6.4, 1.6))
    return [shell(body), detail("M3.5 9.2H20.5"), dot(10, 11.2, 0.9), dot(14, 11.2, 0.9), mark(ellipse(12, 12.7, 1.2, 0.8)),
            dot(10, 18, 0.9)]


@icon("kraken", CAT, "Giant tentacles rising from the waves and curling around a small sailing ship",
      tags=["sea monster", "octopus", "giant squid", "ocean", "sailors", "legend"])
def _(S):
    r = L(S, 0, 0.5)
    return [line("M4.5 21.5C2.5 14 3 6.5 8.5 4.8C11.5 4 12.5 6.2 11 7.6"), line("M19.5 21.5C21.5 14 21 6.5 15.5 4.8C12.5 4 11.5 6.2 13 7.6"),
            shell(poly([(9, 15), (15, 15), (13.6, 18), (10.4, 18)], closed=True, r=r)), line("M12 15V9.5"),
            solid(poly([(12.8, 9.8), (15, 13.8), (12.8, 13.8)], closed=True)),
            line("M2.5 21.5Q4.5 20 6.5 21.5T10.5 21.5T14.5 21.5T18.5 21.5T21.5 21.5")]


@icon("atlas-titan", CAT, "Kneeling muscular figure holding up a large globe on his shoulders",
      tags=["greek", "world", "burden", "titan", "globe", "strength"])
def _(S):
    return [shell(circle(12, 6.5, 4.6)), detail("M7.6 6.5H16.4"), detail("M12 2V11") if False else detail("M12 2.8V10.2"),
            shell(poly([(8, 12.8), (16, 12.8), (15, 18), (9, 18)], closed=True, r=L(S, 0, 1))),
            line("M8.6 13.6L5.6 8.4"), line("M15.4 13.6L18.4 8.4"),
            line("M9 18L5.8 21.5H10"), line("M15 18L18.2 21.5")]


@icon("bigfoot", CAT, "Tall hairy ape-like figure striding with one arm swinging back",
      tags=["sasquatch", "cryptid", "forest", "yeti", "monster", "footprint"])
def _(S):
    body = poly([(7, 9), (9, 7.6), (15, 7.6), (16.5, 9.4), (17, 14.5), (15.5, 16.2), (8.2, 16.2), (7.2, 14)], closed=True, r=L(S, 0, 1.5))
    return [shell(union(body, circle(12, 4.7, 2.6))), line("M7.6 10L3.8 15.4"), line("M16.4 10.2L19 15"),
            line("M10 16.2L6 21.5H9"), line("M14 16.2L17.4 21.5H20.4"), dot(11, 4.4, 0.6), dot(13, 4.4, 0.6)]
