"""TypeIcon Core: pets (batch 003).

Pet, horse and livestock gear, care and behaviour, drawn from the objects themselves.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "pets"


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


def rseg(x1, y1, x2, y2, deg, cx=12.0, cy=12.0):
    """Open segment rotated clockwise by deg about (cx, cy)."""
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)

    def q(x, y):
        return cx + (x - cx) * c - (y - cy) * sn, cy + (x - cx) * sn + (y - cy) * c
    p1, p2 = q(x1, y1), q(x2, y2)
    return seg(p1[0], p1[1], p2[0], p2[1])


def grow(d, g):
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def mark(d):
    """Solid silhouette: solid in Line and Rounded, knocked out of a Filled body."""
    return Part("dot", d)


def paw_d(cx, cy, s=1.0):
    """Small solid paw print centred on (cx, cy); s = 1 is about 6.5 px wide."""
    pad = ellipse(cx, cy + 1.3 * s, 2.3 * s, 1.75 * s)
    toes = [circle(cx - 2.6 * s, cy - 0.5 * s, 0.95 * s), circle(cx - 0.95 * s, cy - 2.5 * s, 0.95 * s),
            circle(cx + 0.95 * s, cy - 2.5 * s, 0.95 * s), circle(cx + 2.6 * s, cy - 0.5 * s, 0.95 * s)]
    return union(pad, *toes)


# ============================================================================ feeding and care

@icon("sheep-pen", CAT, "Barred hurdle pen with a woolly sheep standing behind the top rail",
      tags=["sheep", "fold", "enclosure", "hurdle", "livestock", "farm", "paddock"])
def _(S):
    k = L(S, 0.3, 0.8)
    wool = union(ellipse(12.5, 7.6, 5.2, 2.3), circle(9.6, 6.3, 2.2 + k), circle(12.6, 5, 2.3 + k), circle(15.6, 6.3, 2.2 + k))
    head = ellipse(6.2, 8.2, 1.5, 1.9)
    pen = rect(2.5, 13, 19, 8, min(S.R, 2))
    return [shell(wool), mark(head), shell(pen), detail(seg(8.5, 13, 8.5, 21)), detail(seg(12, 13, 12, 21)), detail(seg(15.5, 13, 15.5, 21))]


@icon("ox-yoke", CAT, "Wooden yoke beam with two U-shaped bows hanging below it",
      tags=["ox", "oxen", "harness", "draught", "plough", "farm", "bullock", "cattle"])
def _(S):
    beam = rect(2.5, 4.5, 19, 4, L(S, 0.6, 2))
    return [shell(beam), line("M5.5 8.5V15a2.5 2.5 0 0 0 5 0V8.5"), line("M13.5 8.5V15a2.5 2.5 0 0 0 5 0V8.5")]


@icon("lamb-bottle-feeding", CAT, "Small lamb standing and drinking from a tilted bottle with a teat",
      tags=["lamb", "bottle feeding", "orphan", "sheep", "milk", "farm", "baby animal"])
def _(S):
    k = L(S, 0.3, 0.8)
    wool = union(ellipse(16.8, 13, 4.8, 3.6), circle(14.6, 12.2, 2.4 + k), circle(17.6, 10.4, 2.5 + k), circle(20, 12.2, 2.2 + k))
    head = union(rot(ellipse(11.8, 14.8, 1.9, 2.6), 30, 11.8, 14.8), rot(ellipse(13, 12.6, 1, 1.8), -40, 13, 12.6))
    tx, ty = 8.4, 14
    b = union(rect(tx - 2, ty - 9.2, 4, 6.4, min(S.R, 1.4)), poly([(tx - 1.2, ty - 2.8), (tx + 1.2, ty - 2.8), (tx, ty)], closed=True, r=0))
    return [shell(wool), mark(head), shell(rot(b, -40, tx, ty)), detail(rot(seg(tx - 2, ty - 4.8, tx + 2, ty - 4.8), -40, tx, ty)),
            line(seg(14.6, 16.5, 14.6, 21)), line(seg(19.4, 16.5, 19.4, 21))]


@icon("pet-sling", CAT, "Fabric pouch with a strap loop and a small dog head peeking out of the top",
      tags=["pet carrier", "sling bag", "dog carrier", "puppy", "small dog", "crossbody", "bag"])
def _(S):
    pouch = poly([(3.5, 14.5), (20.5, 14.5), (18.5, 21.5), (5.5, 21.5)], closed=True, r=L(S, 0, 1.4))
    head = minus(circle(12, 11, 3.3), rect(0, 13, 24, 12))
    ears = [rot(ellipse(8.2, 11.2, 1.1, 2.3), 15, 8.2, 11.2), rot(ellipse(15.8, 11.2, 1.1, 2.3), -15, 15.8, 11.2)]
    return [shell(pouch), line("M4.5 14.5C3.5 3 20.5 3 19.5 14.5"), shell(head), mark(ears[0]), mark(ears[1]), dot(10.8, 10.4, 0.8), dot(13.2, 10.4, 0.8)]


@icon("dog-backpack", CAT, "Dog in side view wearing a saddlebag pack on its back",
      tags=["dog pack", "hiking dog", "saddlebag", "harness", "trail", "travel", "canine"])
def _(S):
    pack = rect(11, 10.5, 7, 7.5, L(S, 0.6, 1.4))
    body = union(rect(8, 6.5, 12.5, 6.5, L(S, 2, 2.9)), circle(5.4, 7.6, 3.3), ellipse(2.6, 9.3, 1.7, 1.3),
                 poly([(3.6, 6), (4.6, 2.6), (7.2, 5.6)], closed=True, r=L(S, 0, 0.5)))
    body = minus(body, grow(pack, 1.3))
    return [shell(body), shell(pack), line(seg(9.5, 12.5, 9.5, 20.5)), line(seg(19, 12.5, 19, 20.5)),
            line("M20.5 7.5C22 7 22.3 5.4 22 3.6"), dot(5, 7.6, 0.8)]


@icon("pet-seat-belt", CAT, "Short tether strap with a belt buckle tongue at one end and a snap clip at the other",
      tags=["car safety", "dog seat belt", "restraint", "tether", "harness", "travel", "buckle", "clip"])
def _(S):
    tongue = poly([(8, 7.5), (3.5, 9.5), (3.5, 14.5), (8, 16.5)], closed=True, r=L(S, 0, 1))
    strap = rect(8, 9.5, 8.5, 5, L(S, 0, 1.2))
    return [shell(tongue), detail(seg(5.5, 10.6, 5.5, 13.4)), shell(strap), detail(seg(10, 12, 14.5, 12)),
            shell(rect(16.5, 8, 5, 8, L(S, 1.5, 2.5)))]


@icon("pet-food-bin", CAT, "Upright storage bin with a hinged lid, small wheels and a paw print on the front",
      tags=["pet food storage", "kibble bin", "dog food", "cat food", "container", "airtight", "feed bin"])
def _(S):
    lid = rect(4.5, 3.5, 15, 4.5, L(S, 0.8, 2))
    body = rect(5.5, 8, 13, 10, L(S, 0.8, 2))
    return [shell(union(lid, body)), detail(seg(5.5, 8, 18.5, 8)), mark(paw_d(12, 12.6, 0.95)),
            mark(circle(8, 20.6, 1.4)), mark(circle(16, 20.6, 1.4))]


@icon("wet-food-pouch", CAT, "Flat food pouch with a cut corner at the top and a fish outline on the front",
      tags=["wet food", "cat food", "dog food", "sachet", "pouch", "fish", "tear notch", "meal"])
def _(S):
    d = poly([(6, 3.5), (15.5, 3.5), (18, 6), (18, 20.5), (6, 20.5)], closed=True, r=L(S, 0, 1.2))
    fish = union(ellipse(11.2, 14.4, 3.2, 2.2), poly([(13.6, 14.4), (16.2, 12.4), (16.2, 16.4)], closed=True, r=0))
    return [shell(d), detail(seg(6, 7.5, 18, 7.5)), mark(fish)]


@icon("treat-ball", CAT, "Ball with a round opening and kibble pieces tumbling out of the hole",
      tags=["treat dispenser", "puzzle toy", "dog toy", "kibble", "snack ball", "enrichment", "feeding toy"])
def _(S):
    k = L(S, 0, 0.5)
    bits = [rot(rect(16.3, 13, 2.6, 2.6, k), 20, 17.6, 14.3), rot(rect(14.6, 18.2, 2.6, 2.6, k), -15, 15.9, 19.5),
            rot(rect(19.4, 18, 2.6, 2.6, k), 30, 20.7, 19.3)]
    return [shell(circle(9.5, 9.5, 6.5)), dot(11.3, 11.3, 2), *[mark(b) for b in bits]]


@icon("agility-a-frame", CAT, "Tall A-shaped ramp with slat rungs and a paw print beside it",
      tags=["dog agility", "a-frame", "obstacle course", "training", "ramp", "dog sport", "climb"])
def _(S):
    tri = poly([(6, 20.5), (14, 4.5), (22, 20.5)], closed=True, r=L(S, 0, 1.2))
    return [shell(tri), detail(seg(9.3, 13.6, 18.7, 13.6)), detail(seg(7.7, 17, 20.3, 17)), mark(paw_d(5.6, 7.6, 0.85))]


@icon("bark-collar", CAT, "Dog collar strap with a small box unit at the front and sound wave arcs above it",
      tags=["training collar", "anti-bark", "dog collar", "sound waves", "barking", "device", "behaviour"])
def _(S):
    box = rect(9, 11.5, 6, 7.5, L(S, 0.8, 1.6))
    strap = minus(rect(2.5, 14, 19, 4.5, L(S, 0.6, 2)), grow(box, 1.3))
    return [shell(strap), shell(box), line(arc(12, 10.5, 3.6, -145, -35)), line(arc(12, 10.5, 7, -145, -35))]


@icon("paw-balm", CAT, "Round balm tin with its lid set beside it, a paw print on the lid",
      tags=["paw wax", "paw butter", "dog care", "moisturiser", "salve", "tin", "pad protection", "winter"])
def _(S):
    tin = union(rect(2.5, 14, 13, 6.5, L(S, 1, 2.6)), ellipse(9, 14, 6.5, 2))
    return [shell(tin), detail("M2.5 14A6.5 2 0 0 0 15.5 14"), shell(circle(17, 6.8, 4.4)), mark(paw_d(17, 7, 0.62))]


@icon("paw-washer", CAT, "Tall cup with bristles lining the inside and a paw dipping towards the top",
      tags=["paw cleaner", "muddy paws", "dog paw wash", "bristles", "cup", "hygiene", "after walk"])
def _(S):
    cup = poly([(5, 9.5), (19, 9.5), (17, 21), (7, 21)], closed=True, r=L(S, 0, 1.2))
    return [shell(cup), detail(seg(9.5, 13.5, 9.5, 17.5)), detail(seg(12, 13.5, 12, 17.5)), detail(seg(14.5, 13.5, 14.5, 17.5)),
            mark(paw_d(12, 4.6, 0.8))]


@icon("grooming-glove", CAT, "Mitt-shaped grooming glove seen palm up, the palm covered with rubber nubs",
      tags=["pet brush glove", "deshedding glove", "fur removal", "massage", "mitt", "cat", "dog", "brush"])
def _(S):
    mitt = union("M6.5 21V10C6.5 4.8 9 3 12 3C15 3 17.5 4.8 17.5 10V21Z", thick("M6.5 15.5L3.8 11.2", 3.4, S))
    return [shell(mitt), detail(seg(6.5, 18.5, 17.5, 18.5)), dot(9.6, 7.3, 1), dot(14.4, 7.3, 1), dot(12, 11, 1), dot(9.6, 14.7, 1), dot(14.4, 14.7, 1)]


@icon("pet-nail-grinder", CAT, "Handheld rotary tool with a round sanding drum at the tip and a guard cap",
      tags=["nail trimmer", "claw grinder", "dog nails", "cat nails", "electric file", "pedicure", "grooming tool"])
def _(S):
    k = L(S, 1, 2.4)
    body = rect(2.5, 9.5, 11, 5.5, k)
    neck = rect(13.5, 10.5, 3, 3.5, 0)
    drum = rect(16.5, 8.5, 5, 7, L(S, 0.6, 1.4))
    d = lambda x: rot(x, -25, 12, 12)
    return [shell(d(union(body, neck, drum))), detail(d(seg(16.5, 12, 21.5, 12))), mark(d(circle(7, 12.2, 1.1)))]


@icon("dog-diaper", CAT, "Diaper for a dog with side tabs and a round hole for the tail at the top",
      tags=["pet nappy", "incontinence", "heat diaper", "dog pants", "belly band", "puppy", "hygiene"])
def _(S):
    body = "M4.5 4.5H19.5V9.5C19.5 14 15.5 14.5 15.5 20H8.5C8.5 14.5 4.5 14 4.5 9.5Z"
    tabs = union(rect(1.5, 7, 4, 4.5, L(S, 0.6, 1.4)), rect(18.5, 7, 4, 4.5, L(S, 0.6, 1.4)))
    return [shell(union(body, tabs)), detail(circle(12, 8.2, 2.2)), detail(seg(8.5, 17.5, 15.5, 17.5))]


@icon("potty-training-bells", CAT, "Strap hanging from a door handle with a column of small bells along it",
      tags=["dog bells", "door bells", "house training", "toilet training", "puppy", "go outside", "strap"])
def _(S):
    handle = rect(6, 2.5, 12, 3.6, L(S, 0.8, 1.8))
    def bell(cx, cy):
        pts = [(cx - 2.6, cy + 2.2), (cx - 1.4, cy + 1.6), (cx - 1.6, cy - 0.2), (cx - 1.7, cy - 0.8)]
        return (f"M{fmt(cx - 2.6)} {fmt(cy + 2.2)}C{fmt(cx - 1.4)} {fmt(cy + 1.6)} {fmt(cx - 1.6)} {fmt(cy - 0.2)} {fmt(cx - 1.7)} {fmt(cy - 0.8)}"
                f"C{fmt(cx - 1.5)} {fmt(cy - 3)} {fmt(cx + 1.5)} {fmt(cy - 3)} {fmt(cx + 1.7)} {fmt(cy - 0.8)}"
                f"C{fmt(cx + 1.6)} {fmt(cy - 0.2)} {fmt(cx + 1.4)} {fmt(cy + 1.6)} {fmt(cx + 2.6)} {fmt(cy + 2.2)}Z")
    return [shell(handle), line(seg(12, 6.1, 12, 21)), mark(bell(8.6, 10.6)), mark(bell(15.4, 14.6)), mark(bell(8.6, 18.6))]


@icon("dog-grass-pad", CAT, "Shallow square tray filled with upright blades of turf",
      tags=["pee pad", "indoor potty", "artificial grass", "puppy training", "turf", "litter tray", "apartment dog"])
def _(S):
    tray = rect(2.5, 15, 19, 5.5, L(S, 0.8, 2))
    blades = [poly([(x - 1.4, 14.5), (x + 1.4, 14.5), (tx, ty)], closed=True) for x, tx, ty in
              [(5.6, 4.2, 7), (10, 10.6, 4.5), (14.4, 13.6, 6.5), (18.6, 20, 8)]]
    return [shell(tray), *[solid(b) for b in blades]]


@icon("fire-hydrant", CAT, "Street fire hydrant with a domed cap, a side outlet on each side and a flanged base",
      tags=["hydrant", "dog toilet", "street", "water supply", "firefighting", "sidewalk", "curb"])
def _(S):
    cap = minus(circle(12, 8.6, 4.6), rect(0, 8.6, 24, 6))
    body = union(rect(8.5, 8.4, 7, 9.6, 0), rect(3.5, 10.6, 5.5, 4.2, L(S, 0.5, 1.4)), rect(15, 10.6, 5.5, 4.2, L(S, 0.5, 1.4)),
                 rect(6, 18, 12, 3.5, L(S, 0.5, 1.4)), rect(11, 2.4, 2, 2, 0))
    return [shell(union(cap, body)), detail(seg(7.4, 8.6, 16.6, 8.6)), detail(seg(8.5, 18, 15.5, 18))]


@icon("bird-ladder", CAT, "Short wooden ladder with round rungs and a hook at the top for hanging in a cage",
      tags=["cage ladder", "parrot", "budgie", "perch", "climbing toy", "bird toy", "pet bird"])
def _(S):
    return [line(seg(7, 6.5, 7, 21.5)), line(seg(17, 6.5, 17, 21.5)), line(seg(7, 6.5, 17, 6.5)), line(seg(7, 11.5, 17, 11.5)),
            line(seg(7, 16.5, 17, 16.5)), line(seg(7, 21, 17, 21)), line("M12 6.5V3.8a2.4 2.4 0 0 1 4.8 0")]


# ============================================================================ farm and stable

@icon("hay-ring-feeder", CAT, "Round metal ring feeder with vertical bars standing around a mound of hay",
      tags=["hay feeder", "bale feeder", "horse feeder", "cattle feeder", "round bale", "livestock", "paddock"])
def _(S):
    h = L(S, 3.2, 2.4)
    top = union(ellipse(12, 9.5, 8.5, 2.8), f"M5 9.5C5.5 {fmt(h)} 18.5 {fmt(h)} 19 9.5Z")
    bars = []
    for x in (3.5, 7.75, 12, 16.25, 20.5):
        u = (x - 12) / 8.5
        r = math.sqrt(max(0, 1 - u * u))
        bars.append(line(seg(x, 9.5 + 2.8 * r, x, 18 + 2.8 * r)))
    return [shell(top), *bars, line("M3.5 18A8.5 2.8 0 0 0 20.5 18")]


@icon("calf-hutch", CAT, "Igloo-shaped plastic hutch with an arched doorway and a small wire pen beside it",
      tags=["calf house", "dairy", "cattle", "young stock", "shelter", "igloo hutch", "farm", "pen"])
def _(S):
    dome = minus(ellipse(8.2, 17.6, 6.9, 10), rect(0, 17.6, 24, 14))
    base = rect(1, 17.6, 14.4, 3.4, L(S, 0.5, 1.3))
    pen = rect(16.8, 11.5, 5.2, 9.5, L(S, 0.4, 1.4))
    return [shell(union(dome, base)), detail("M5.7 17.6V14.6A2.5 2.5 0 0 1 10.7 14.6V17.6"), shell(pen), detail(seg(19.4, 11.5, 19.4, 21))]


@icon("ear-tag-pliers", CAT, "Plier-style applicator with long handles and an ear tag loaded in the jaw",
      tags=["ear tagging", "livestock id", "applicator", "cattle tag", "sheep tag", "farm tool", "identification"])
def _(S):
    tag = rect(9, 2, 6, 4.4, L(S, 0.6, 1.6))
    arms = union(thick("M5 20.5L11.6 12.2L9.8 8.6", 3.4, S), thick("M19 20.5L12.4 12.2L14.2 8.6", 3.4, S))
    return [shell(tag), shell(arms), dot(12, 13.4, 0.9)]


@icon("hay-hook", CAT, "Large curved steel hook with a wooden T handle",
      tags=["bale hook", "hay bale", "farm tool", "lifting", "barn", "t handle", "baling"])
def _(S):
    handle = rect(6, 2.5, 12, 3.6, L(S, 0.8, 1.8))
    return [shell(handle), line("M12 6.1V13C12 17 14 20.5 17.5 20.5C20.5 20.5 21.5 18 21.5 15.5")]


@icon("hitching-post", CAT, "Wooden post with a metal ring on its side and a lead rope tied to it",
      tags=["horse tie", "tether", "tie ring", "rope", "stable", "yard", "rail", "ranch"])
def _(S):
    post = rect(5, 3, 7, 18.5, L(S, 0.5, 1.6))
    return [shell(post), detail(seg(5, 6.5, 12, 6.5)), line(circle(15.6, 10.6, 2.6)),
            line("M15.6 13.2C15.6 17.5 19.5 17 19.5 20.5")]


@icon("riding-spur", CAT, "Riding spur with a U-shaped heel band, a short neck and a spiked rowel wheel",
      tags=["horse riding", "equestrian", "boot spur", "rowel", "cowboy", "rider", "heel"])
def _(S):
    n = 12
    star = poly([(5.6 + (3.1 if i % 2 == 0 else 1.5) * math.cos(math.radians(i * 30)),
                  12 + (3.1 if i % 2 == 0 else 1.5) * math.sin(math.radians(i * 30))) for i in range(n)], closed=True, r=0)
    band = "M21.5 5.5H16.5a6.5 6.5 0 0 0 0 13H21.5"
    return [line(band), line(seg(10, 12, 8.6, 12)), shell(star)]


@icon("riding-crop", CAT, "Short thin riding whip with a wrapped grip at the top and a flat leather keeper at the tip",
      tags=["horse whip", "jockey", "equestrian", "crop", "training aid", "show jumping", "riding"])
def _(S):
    d = lambda x: rot(x, 45, 12, 12)
    g = lambda x1, y1, x2, y2: rseg(x1, y1, x2, y2, 45)
    grip = rect(10.3, 2.5, 3.4, 7, L(S, 0.8, 1.7))
    keeper = rect(9.6, 17.6, 4.8, 4.2, L(S, 0.5, 1.3))
    return [shell(d(grip)), detail(g(10.3, 5, 13.7, 5)), detail(g(10.3, 7.3, 13.7, 7.3)), line(g(12, 9.5, 12, 17.6)), shell(d(keeper))]


@icon("snaffle-bit", CAT, "Horse bit with a jointed mouthpiece bar and a large round ring at each end",
      tags=["horse bit", "bridle", "mouthpiece", "tack", "equestrian", "rein ring", "saddlery"])
def _(S):
    bar = thick(poly([(7, 12), (12, 16.5), (17, 12)], r=S.r * 0.6), 3.2, S)
    return [line(circle(5.4, 9.8, 3.8)), line(circle(18.6, 9.8, 3.8)), shell(bar)]


@icon("horse-blinkers", CAT, "Horse head in profile wearing a bridle with a square blinker cup beside the eye",
      tags=["blinders", "winkers", "carriage horse", "harness racing", "bridle", "tack", "equestrian"])
def _(S):
    r = L(S, 0, 1.2)
    head = ("M13 6.5L15.5 2.8L16.8 6.3L16.8 6.3C19.3 9 20.5 14 20.5 21L10.5 21C10.5 18.5 11 16.8 12 15.2"
            "C10.5 16.8 8.8 17.8 6.8 17.8C5 17.8 3.8 16.8 3.8 15.3C3.8 14 4.3 13.2 5.2 12.3Z")
    blinker = rect(14.4, 7.4, 4.2, 5.6, L(S, 0.4, 1.2))
    return [shell(head), mark(blinker), dot(11.6, 9.6, 1.1), detail("M14.4 13.4C12.2 15 10 15.4 7.6 15")]


@icon("mounting-block", CAT, "Sturdy block of three stacked steps seen from the side, used to climb onto a horse",
      tags=["mounting steps", "horse riding", "stable yard", "step block", "riding aid", "stairs", "equestrian"])
def _(S):
    steps = poly([(2.5, 21), (2.5, 16.5), (8, 16.5), (8, 12), (13.5, 12), (13.5, 7.5), (21.5, 7.5), (21.5, 21)], closed=True, r=L(S, 0, 1))
    return [shell(steps), detail(seg(8, 16.5, 8, 21)), detail(seg(13.5, 12, 13.5, 21))]


@icon("hoof-rasp", CAT, "Long flat rasp with a crosshatched surface and a handle at one end, used by farriers",
      tags=["farrier", "horse hoof", "file", "hoof trimming", "hoof care", "stable", "tool"])
def _(S):
    d = lambda x: rot(x, 45, 12, 12)
    g = lambda x1, y1, x2, y2: rseg(x1, y1, x2, y2, 45)
    blade = rect(7.8, 2, 8.4, 12.5, L(S, 0.6, 1.6))
    hatch = [(7.8, 5.6, 16.2, 9.4), (7.8, 10.2, 16.2, 14), (16.2, 5.6, 7.8, 9.4), (16.2, 10.2, 7.8, 14)]
    return [shell(d(blade)), *[detail(g(*h)) for h in hatch], shell(d(rect(9.8, 15.5, 4.4, 6.5, L(S, 0.8, 2))))]


@icon("rabies-tag", CAT, "Round metal tag on a split ring with a small syringe stamped on it",
      tags=["vaccination tag", "dog licence", "id tag", "pet tag", "collar tag", "vet", "vaccine"])
def _(S):
    barrel = thick(seg(9.6, 17, 14.4, 12.2), 2.8, S)
    needle = thick(seg(9.6, 17, 7.8, 18.8), 1.2, S)
    flange = thick(seg(13.6, 10.8, 15.8, 13), 1.6, S)
    plunger = thick(seg(14.4, 12.2, 16.6, 10), 1.2, S)
    return [line(circle(12, 4.4, 2.4)), shell(circle(12, 14.6, 6.6)), mark(union(barrel, needle, flange, plunger))]


@icon("animal-catch-pole", CAT, "Long pole with a handle at one end and an adjustable cable noose loop at the other",
      tags=["animal control", "snare pole", "rescue", "dog catcher", "capture", "noose", "wildlife handling"])
def _(S):
    return [shell(thick(seg(3.8, 20.2, 7.6, 16.4), 3.6, S)), line(seg(7.6, 16.4, 13.4, 10.6)), line(arc(17.8, 6.2, 3.8, 170, 460)),
            shell(thick(seg(12.4, 11.6, 14.2, 9.8), 3.2, S))]


@icon("live-animal-trap", CAT, "Rectangular wire mesh cage trap with a raised drop door at one end",
      tags=["humane trap", "cage trap", "catch and release", "raccoon", "feral cat", "wildlife", "pest control"])
def _(S):
    cage = rect(2.5, 9.5, 15.5, 9.5, L(S, 0.8, 2))
    door = rect(19.6, 4.5, 2.2, 10.5, L(S, 0.3, 1))
    return [shell(cage), detail(seg(7.4, 9.5, 7.4, 19)), detail(seg(12.6, 9.5, 12.6, 19)), detail(seg(2.5, 14.25, 18, 14.25)), shell(door), line("M7.5 9.5V6.3H13V9.5")]


@icon("pet-urn", CAT, "Small rounded urn with a lid and a paw print on its front",
      tags=["pet memorial", "cremation", "ashes", "pet loss", "remembrance", "rainbow bridge", "keepsake"])
def _(S):
    lid = rect(8, 3, 8, 3, L(S, 0.6, 1.5))
    neck = rect(9.6, 6, 4.8, 2.2, 0)
    belly = "M9.4 8.2C3.5 9.5 3.5 20.5 12 20.5C20.5 20.5 20.5 9.5 14.6 8.2Z"
    foot = rect(8.5, 19.5, 7, 2.3, L(S, 0.4, 1.1))
    return [shell(union(lid, neck, belly, foot)), mark(paw_d(12, 13.6, 0.85)), line("M8.6 9.6C5.4 8 3.6 10.8 5.6 12.8"), line("M15.4 9.6C18.6 8 20.4 10.8 18.4 12.8")]


# ============================================================================ transport and behaviour

@icon("pet-taxi", CAT, "Car in side view with a paw print on a sign above the roof",
      tags=["pet transport", "animal taxi", "vet ride", "dog cab", "travel with pets", "car", "paw sign"])
def _(S):
    cabin = poly([(5.5, 13.5), (8.5, 9), (15.5, 9), (18.5, 13.5)], closed=True, r=L(S, 0, 1))
    body = rect(2.5, 13.5, 19, 5.5, L(S, 0.8, 2.4))
    return [shell(union(cabin, body)), detail(seg(12, 9, 12, 13.5)), mark(circle(7, 19.2, 2.1)), mark(circle(17, 19.2, 2.1)), mark(paw_d(12, 4.6, 0.72))]


@icon("mobile-pet-groomer", CAT, "Van in side view with a paw print and a pair of scissors on its side panel",
      tags=["grooming van", "mobile grooming", "pet salon", "dog groomer", "house call", "scissors", "vehicle"])
def _(S):
    box = rect(2.5, 5.5, 13.5, 12.5, L(S, 0.8, 2))
    cab = poly([(15, 10), (19, 10), (21.5, 13.5), (21.5, 18), (15, 18)], closed=True, r=L(S, 0, 1))
    return [shell(union(box, cab)), detail(seg(15.5, 10, 15.5, 18)),
            mark(circle(7, 19, 2.1)), mark(circle(18, 19, 2.1)), mark(paw_d(6.8, 11, 0.7)), detail(seg(10.4, 8.2, 13.2, 12.4)), detail(seg(13.2, 8.2, 10.4, 12.4)),
            dot(10.6, 14.3, 1.1), dot(13, 14.3, 1.1)]


@icon("cat-in-box", CAT, "Cat head with pointed ears peeking out of an open cardboard box with folded flaps",
      tags=["cat", "box", "peeking", "kitten", "hiding", "cardboard", "curious cat", "delivery box"])
def _(S):
    r = L(S, 0, 0.6)
    ears = union(poly([(8, 9), (8.2, 2.8), (12, 6)], closed=True, r=r), poly([(16, 9), (15.8, 2.8), (12, 6)], closed=True, r=r))
    head = union(circle(12, 9.4, 4.2), ears)
    box = rect(3.5, 12.5, 17, 8.2, L(S, 0.6, 1.5))
    flaps = union(poly([(3.5, 12.5), (2, 9), (5.4, 9.6), (5.6, 12.5)], closed=True, r=r),
                  poly([(20.5, 12.5), (22, 9), (18.6, 9.6), (18.4, 12.5)], closed=True, r=r))
    return [shell(union(head, box, flaps)), dot(10.2, 9.2, 0.95), dot(13.8, 9.2, 0.95)]


@icon("dog-begging", CAT, "Dog sitting up on its hind legs with both front paws raised",
      tags=["sit up", "beg", "treat", "trick", "puppy", "dog training", "please", "pet"])
def _(S):
    r = L(S, 0, 1.2)
    head = union(circle(11, 6.4, 3.3), ellipse(7.4, 7.6, 2.2, 1.6))
    ear = rot(ellipse(14.2, 6.6, 1.3, 2.6), -12, 14.2, 6.6)
    body = union(ellipse(13, 14.4, 4.6, 5.6), rect(8.6, 18.5, 9, 3, L(S, 1, 1.5)))
    return [shell(union(head, ear, body)), line("M9.6 12L7 9.8"), line("M8.8 15L5.4 12.6"), dot(9.6, 5.6, 0.85), line("M17.4 17C19.6 17 21 15.6 21 13.5")]


@icon("dog-digging", CAT, "Dog in side view with its front paws in a hole and dirt clumps flying out behind it",
      tags=["digging", "hole", "garden", "dirt", "burying", "behaviour", "puppy", "yard"])
def _(S):
    body = rot(rect(8.5, 8, 11.5, 6.4, L(S, 2.6, 3.2)), -14, 14, 11)
    head = union(circle(6.6, 13.4, 3.1), ellipse(3.8, 15.6, 1.9, 1.4), poly([(7.4, 11.2), (9.8, 10.6), (9, 14)], closed=True, r=0))
    return [shell(union(body, head)), line(seg(7.6, 16, 7.6, 20)), line(seg(10.8, 15.2, 10.8, 20)), line(seg(18.6, 13.6, 18.6, 20)),
            line("M20.4 9.4L21.6 6.6"), line(seg(2, 21, 22, 21)), dot(5.6, 12.6, 0.8), mark(circle(22, 12.2, 1)), mark(circle(21.2, 16, 1.1))]


@icon("tail-wagging", CAT, "Rear view of a sitting dog with its tail raised and curved motion lines on both sides",
      tags=["happy dog", "wag", "tail", "excited", "friendly", "dog behaviour", "greeting", "pet"])
def _(S):
    head = circle(10, 7.2, 3.1)
    ears = [rot(ellipse(6.6, 7.4, 1.3, 2.4), 12, 6.6, 7.4), rot(ellipse(13.4, 7.4, 1.3, 2.4), -12, 13.4, 7.4)]
    body = ellipse(10, 15.6, 4.4, 5.2)
    return [shell(union(head, *ears, body)), line("M11.5 20.2C16.5 20.2 18 16.6 17.4 12.8"),
            line("M20.4 10C21.6 12.4 21.6 15 20.6 17.4"), line("M3 9C1.8 11.4 1.8 14 2.8 16.4")]


@icon("pet-shedding", CAT, "Cat sitting in side view with loose tufts of fur drifting off around it",
      tags=["fur", "hair", "moulting", "molting", "cat hair", "deshedding", "pet hair", "grooming"])
def _(S):
    r = L(S, 0, 0.6)
    head = union(circle(8.2, 8.4, 3.4), poly([(5.4, 7.4), (5.8, 3.6), (8.4, 5.6)], closed=True, r=r), poly([(11, 7.4), (10.6, 3.6), (8, 5.6)], closed=True, r=r))
    body = union(ellipse(10.6, 16.4, 5.2, 4.8), thick("M15.4 19C18 19.5 19.6 17.8 18.8 15.4", 2.4, S))
    tufts = [rot(ellipse(18.4, 5.4, 2.2, 1.1), -30, 18.4, 5.4), rot(ellipse(20.4, 10.2, 2, 1), 20, 20.4, 10.2), rot(ellipse(15.6, 11.2, 1.7, 0.9), -40, 15.6, 11.2)]
    return [shell(union(head, body)), dot(7.2, 8.2, 0.8), dot(9.6, 8.2, 0.8), *[mark(t) for t in tufts]]


@icon("dog-and-cat", CAT, "Dog head and cat head side by side, the smaller cat slightly in front",
      tags=["pets", "dog", "cat", "cats and dogs", "animals", "friends", "household pets", "pet shop"])
def _(S):
    r = L(S, 0, 0.6)
    dog = union(circle(8.4, 9.4, 5), rot(ellipse(3.4, 9.6, 1.7, 3.4), 8, 3.4, 9.6), rot(ellipse(13.4, 9.2, 1.5, 3), -8, 13.4, 9.2))
    cat = union(circle(16.4, 14.6, 4.4), poly([(12.4, 13), (12.8, 8.4), (16, 11)], closed=True, r=r), poly([(20.4, 13), (20, 8.4), (16.8, 11)], closed=True, r=r))
    dog = minus(dog, grow(cat, 1.3))
    return [shell(dog), shell(cat), dot(6.6, 8.6, 0.85), mark(ellipse(8.4, 11.6, 1.5, 1)), dot(14.8, 14.2, 0.8), dot(18, 14.2, 0.8)]


@icon("hamster-tubes", CAT, "Connected clear tubes forming an elbow and a T junction with round ends",
      tags=["hamster cage", "tunnel", "habitat", "rodent", "gerbil", "play tubes", "crittertrail", "small pet"])
def _(S):
    tubes = union(thick("M4.5 6.5H19", 4.6, S), thick("M11.75 6.5V19", 4.6, S), thick("M4.5 6.5V13", 4.6, S))
    return [shell(tubes), mark(circle(19, 6.5, 1.3)), mark(circle(11.75, 19, 1.3)), mark(circle(4.5, 13, 1.3))]


@icon("rabbit-run", CAT, "Triangular A-frame run of wire mesh on a wooden frame with a small hatch at one end",
      tags=["bunny run", "rabbit hutch", "guinea pig", "outdoor pen", "mesh cage", "a-frame", "small animal"])
def _(S):
    front = poly([(2.5, 20.5), (8.5, 7), (14.5, 20.5)], closed=True, r=L(S, 0, 1))
    return [shell(front), detail("M6.1 20.5V16.4H10.9V20.5"), line(seg(8.5, 7, 15.5, 4)), line(seg(15.5, 4, 21.5, 17.5)), line(seg(14.5, 20.5, 21.5, 17.5)),
            line(seg(11.5, 13.8, 18.5, 10.8))]


@icon("dog-sled", CAT, "Low wooden sled with an upright handlebar at the back and a gangline leading to a running dog",
      tags=["sledding", "mushing", "husky", "snow", "winter", "iditarod", "sled dog", "arctic"])
def _(S):
    basket = rect(10, 11.2, 10.5, 4.3, L(S, 0.8, 1.8))
    dog = union(ellipse(4.6, 12.6, 2.6, 1.4), circle(2, 11.4, 1.2), thick("M3.2 13.8L1.8 15.8", 1.2, S), thick("M6.4 13.8L7.6 15.8", 1.2, S))
    return [shell(basket), line("M21.5 19.5H11.5C9.2 19.5 8.6 18 8.8 16.6"), line(seg(12.5, 15.5, 12.5, 19.5)), line(seg(18.5, 15.5, 18.5, 19.5)),
            line(seg(20.5, 11.2, 21.6, 4.6)), line(seg(19.6, 4.6, 22.6, 4.6)), line(seg(7.4, 12.8, 10, 12.8)), mark(dog)]


@icon("saddle-rack", CAT, "Wall bracket arm jutting out with a saddle resting on top of it",
      tags=["saddle bracket", "tack room", "horse gear", "wall mount", "stable", "equestrian", "saddle stand"])
def _(S):
    saddle = "M7 14.6C6.4 11 6.6 8.6 8.2 8C10 7.4 10.6 10.2 12.8 10.6C15 11 16 8.6 17.6 7.2C19.4 5.8 21.4 7.4 21.2 10.4L20.6 14.6Z"
    return [shell(saddle), detail("M9.2 12C10.6 13.2 13 13.6 16 12.8"), line(seg(3, 3, 3, 21.5)), line(seg(3, 18.5, 21.5, 18.5)), line(seg(3, 13.5, 9, 18.5))]


@icon("heated-pet-pad", CAT, "Flat rounded pad with three wavy heat lines rising above it and a power cord out one side",
      tags=["warming mat", "pet heater", "electric mat", "cat bed", "dog bed", "winter", "cosy", "warmth"])
def _(S):
    pad = rect(2.5, 14.5, 16, 5.5, L(S, 1, 2.6))
    waves = [line(f"M{x} 12C{x - 2} 10 {x + 2} 8 {x} 6") for x in (6.2, 10.5, 14.8)]
    return [shell(pad), *waves, line("M18.5 17.2C21.5 17.2 20.5 21 22.6 21"), ]


@icon("raised-dog-cot", CAT, "Elevated mesh cot bed stretched on a frame with short legs at the corners and a dog lying on it",
      tags=["elevated bed", "outdoor dog bed", "cooling cot", "trampoline bed", "dog furniture", "camping", "porch"])
def _(S):
    sling = poly([(5, 10), (21.5, 10), (19.5, 15), (2.5, 15)], closed=True, r=L(S, 0, 1.4))
    dog = union(ellipse(10.6, 6.6, 4.4, 2), circle(15.8, 5.6, 1.8), poly([(15.6, 4.2), (16.6, 2.4), (17.6, 4.6)], closed=True))
    return [shell(sling), line(seg(4.5, 15, 4.5, 21)), line(seg(17.5, 15, 17.5, 21)), line(seg(3, 21, 6, 21)), line(seg(16, 21, 19, 21)), mark(dog)]


@icon("cat-wall-shelves", CAT, "Three staggered floating shelves climbing the wall diagonally with a cat sitting on the top one",
      tags=["cat climbing", "cat furniture", "wall perch", "cat tree", "floating shelf", "indoor cat", "enrichment"])
def _(S):
    cat = union(circle(17.4, 4.6, 2.2), poly([(15.6, 3.4), (15.8, 1.2), (17.4, 2.6)], closed=True), poly([(19.2, 3.4), (19, 1.2), (17.4, 2.6)], closed=True),
                ellipse(18.4, 7.6, 2.8, 2.2))
    return [line(seg(2.5, 20.5, 9.5, 20.5)), line(seg(8.5, 15.5, 15.5, 15.5)), line(seg(14.5, 10.5, 21.5, 10.5)), mark(cat)]


@icon("livestock-marker", CAT, "Chunky marking crayon stick pushed up out of a twist-up holder",
      tags=["raddle", "sheep marker", "paint stick", "cattle marking", "crayon", "farm", "breeding mark"])
def _(S):
    crayon = poly([(9.5, 10), (9.5, 5.6), (12, 2.6), (14.5, 5.6), (14.5, 10)], closed=True, r=L(S, 0, 0.6))
    holder = rect(8, 9.5, 8, 12, L(S, 0.6, 1.6))
    return [shell(union(crayon, holder)), detail(seg(8, 9.5, 16, 9.5)), detail(seg(8, 14.2, 16, 15.6)), detail(seg(8, 18, 16, 19.4))]


@icon("hoof-stand", CAT, "Short pedestal stand with a wide base and a cradle top holding a horse hoof",
      tags=["farrier stand", "hoof trimming", "horse", "shoeing", "hoof jack", "stable", "equine care"])
def _(S):
    hoof = union(rect(9.6, 2, 4.8, 4.4, 0), poly([(9.3, 6), (14.7, 6), (17.6, 10), (6.4, 10)], closed=True, r=L(S, 0, 0.8)))
    return [shell(hoof), detail(seg(9.3, 6.4, 14.7, 6.4)), line(seg(5.5, 13, 18.5, 13)), shell(rect(10.3, 13, 3.4, 5.5, 0)), shell(rect(4.5, 18.5, 15, 3, L(S, 0.6, 1.4)))]


@icon("pet-ear-drops", CAT, "Dropper bottle releasing a drop beside a floppy dog ear",
      tags=["ear cleaner", "ear infection", "vet medicine", "dropper", "ear care", "dog health", "treatment", "mites"])
def _(S):
    ear = "M5.6 3.6C3 8.6 3.6 15.6 8 20.4C12.4 17.4 13 10.4 11 5.2C9.6 2.6 7 2.4 5.6 3.6Z"
    dropper = union(rect(15.4, 1.8, 3.2, 3.2, L(S, 0.6, 1.4)), rect(14.6, 5, 4.8, 2, 0), rect(15.4, 7, 3.2, 4.6, 0),
                    poly([(15.4, 11.6), (18.6, 11.6), (17, 14.4)], closed=True))
    drop = "M17 16.2C15.4 18.4 15.2 19.4 15.3 20C15.4 21 16.2 21.6 17 21.6C17.8 21.6 18.6 21 18.7 20C18.8 19.4 18.6 18.4 17 16.2Z"
    return [shell(ear), detail("M7 8.2C6.8 11 7.6 13.8 9 16"), shell(dropper), mark(drop)]


@icon("pet-toy-basket", CAT, "Open basket with a ball, a bone and a rope toy sticking out of the top",
      tags=["toy box", "dog toys", "cat toys", "tidy up", "storage", "play", "chew toys", "bin"])
def _(S):
    basket = poly([(3.5, 11.5), (20.5, 11.5), (18.6, 21), (5.4, 21)], closed=True, r=L(S, 0, 1.4))
    bone = union(thick(seg(11.6, 9.8, 15, 6.4), 2.2, S), circle(11, 10, 1.4), circle(12.6, 8.4, 1.3), circle(14.6, 5.9, 1.3), circle(16, 7.6, 1.4))
    return [shell(basket), detail(seg(4.5, 16.2, 19.5, 16.2)), shell(circle(7, 7.6, 2.8)), mark(bone), line(seg(19.6, 11.5, 19.6, 6)), dot(19.6, 4.6, 1.5)]


@icon("catio", CAT, "Mesh box enclosure attached to a house wall with a cat sitting inside",
      tags=["cat patio", "outdoor cat enclosure", "cat run", "window box", "screened porch", "safe outdoors", "cat"])
def _(S):
    box = rect(7.5, 7, 14, 13.5, L(S, 0.8, 2))
    cat = union(circle(14.5, 13.4, 1.9), poly([(12.9, 12.6), (13.1, 10.4), (14.5, 11.6)], closed=True), poly([(16.1, 12.6), (15.9, 10.4), (14.5, 11.6)], closed=True),
                ellipse(14.5, 17, 2.5, 2.6))
    return [line(seg(3.5, 3, 3.5, 21.5)), line(seg(3.5, 11, 7.5, 11)), line(seg(3.5, 17.5, 7.5, 17.5)), shell(box), detail(seg(12.2, 7, 12.2, 9.6)),
            detail(seg(16.8, 7, 16.8, 9.6)), mark(cat)]


@icon("pet-ramp", CAT, "Sloped ramp with a side rail leading up to the open back of a car",
      tags=["dog ramp", "car ramp", "suv", "senior dog", "vehicle access", "mobility", "boot ramp", "loading"])
def _(S):
    car = poly([(11.5, 19), (11.5, 7.5), (17, 7.5), (19.5, 11), (21.5, 11), (21.5, 19)], closed=True, r=L(S, 0, 1))
    ramp = poly([(2.5, 20), (11.5, 14), (11.5, 17)], closed=True, r=L(S, 0, 0.6))
    return [shell(car), mark(circle(17, 19.6, 1.9)), shell(ramp), line(seg(3.6, 14.4, 9.4, 10.2)), line(seg(4.4, 14.4, 4.4, 17.4)), line(seg(8.8, 10.8, 8.8, 14.6))]


@icon("pet-sitter", CAT, "Person seated in an armchair with a cat curled up on their lap",
      tags=["pet sitting", "cat lap", "house sitter", "cuddle", "companion", "caretaker", "cat owner", "armchair"])
def _(S):
    person = union(circle(9.6, 4.8, 2.5), thick("M10.2 8.2L12.2 14", 4.2, S), thick("M12.4 14.4H5.6", 3.8, S), thick("M5.6 14.4V20.6", 3.2, S))
    cat = union(ellipse(9.4, 11.2, 3, 1.6), circle(6.4, 10.2, 1.4), poly([(5.6, 9.2), (5.8, 7.8), (6.8, 8.8)], closed=True), poly([(7.2, 9.2), (7.4, 7.8), (6.6, 8.6)], closed=True))
    chair = union(rect(14.6, 3, 6.4, 16.4, L(S, 1, 2.8)), rect(10, 16, 11, 3.4, L(S, 0.6, 1.4)))
    chair = minus(chair, grow(person, 1.5))
    person = minus(person, grow(cat, 0.9))
    return [shell(chair), mark(person), mark(cat)]
