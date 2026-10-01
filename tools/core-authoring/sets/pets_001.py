"""TypeIcon Core: pets (batch 1). Leashes, collars, beds, housing, feeding, toys, grooming, travel and litter."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
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


def rot(d, deg, cx=12, cy=12):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rp(pts, deg, cx=12, cy=12):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def mark(d):
    """Small solid mark: solid in stroke styles, knocked out of a Filled body."""
    return Part("dot", d)


def bone(cx, cy, length, deg=0, r=1.9, w=3.0):
    h = length / 2 - r * 0.7
    b = union(rect(cx - h, cy - w / 2, 2 * h, w), *[circle(cx + sx * h, cy + sy * (w / 2 + 0.1), r)
                                                      for sx in (-1, 1) for sy in (-1, 1)])
    return rot(b, deg, cx, cy) if deg else b


def pawprint(cx, cy, s=1.0):
    """Tiny paw: pad + four toes as one solid path (for marks on a 5-7 px area)."""
    parts = [ellipse(cx, cy + 1.3 * s, 1.9 * s, 1.4 * s)]
    for dx, dy in ((-2.3, -0.4), (-0.8, -1.9), (0.8, -1.9), (2.3, -0.4)):
        parts.append(circle(cx + dx * s, cy + dy * s, 0.75 * s))
    return union(*parts)


# ============================================================================ leashes and collars

@icon("dog-leash", CAT, "Dog leash with a loop handle, a wavy strap and a snap clip",
      tags=["lead", "leash", "dog walking", "walk", "pet", "strap"])
def _(S):
    return [
        shell(rect(3, 3, 7, 7, L(S, 3, 3.5))),
        line("M8.5 10C9.5 15 4 15 8 18C10.5 20 14 16 15.5 17"),
        shell(rect(15.5, 15.5, 5.5, 4, L(S, 1, 2))),
        detail(seg(18.3, 15.5, 18.3, 19.5)),
    ]


@icon("retractable-leash", CAT, "Retractable leash with a chunky handle, a thumb button and a cord out to a clip",
      tags=["reel leash", "extendable lead", "leash", "dog walking", "reel", "cord", "pet"])
def _(S):
    return [
        shell(rect(3, 3, 13, 13, L(S, 3, 5))),
        detail(rect(6, 7, 3, 6, L(S, 0.5, 1.5))),
        sq(11.5, 5.5, 2.5, 3, L(S, 0, 0.8)),
        line("M14 15C17 16 18 17 18.5 18"),
        shell(rect(16.5, 18, 5, 3.5, L(S, 0.5, 1.5))),
    ]


def sq(x, y, w, h, rx=0.0):
    return Part("dot", rect(x, y, w, h, rx))


@icon("slip-lead", CAT, "Rope slip lead with a handle loop at the top and a sliding ring forming a noose",
      tags=["rope leash", "training lead", "show lead", "kennel lead", "leash", "dog", "vet"])
def _(S):
    return [
        shell(ellipse(12, 5, 4, 3)) if S.name == "rounded" else shell(rect(8, 2.5, 8, 5.5, 2)),
        line(seg(12, 8, 12, 11)),
        shell(circle(12, 13, 2.2)),
        line("M10.5 14.8C5 16.5 6 22 12 22C18 22 19 16.5 13.5 14.8"),
    ]


@icon("dog-collar", CAT, "Buckle dog collar seen at an angle with punched holes and a hanging ring",
      tags=["collar", "dog", "neck strap", "buckle", "pet", "puppy", "id ring"])
def _(S):
    band = "M3 8.5A9 4 0 0 1 21 8.5V14.5A9 4 0 0 1 3 14.5Z"
    return [
        shell(band),
        detail("M3 8.5A9 4 0 0 0 21 8.5"),
        sq(10.5, 12.3, 3, 2, L(S, 0, 0.6)),
        dot(6.5, 13, 0.9),
        dot(17.5, 13, 0.9),
        shell(circle(12, 19.5, 1.9)) if S.name == "rounded" else shell(rect(10.2, 17.7, 3.6, 3.6)),
    ]


@icon("bell-collar", CAT, "Thin cat collar loop with a small jingle bell hanging from the front",
      tags=["cat collar", "jingle bell", "kitten", "safety collar", "breakaway", "pet", "bell"])
def _(S):
    return [
        line(ellipse(12, 7, 9, 4)),
        shell(circle(12, 16, 4.2)) if S.name == "rounded" else shell(poly(regular(12, 16, 4.6, 8, -67.5), closed=True)),
        detail(seg(8.6, 14.6, 15.4, 14.6)),
        dot(12, 17.8, 0.9),
    ]


@icon("pet-id-tag", CAT, "Bone-shaped name tag with a punched hole hanging from a split ring",
      tags=["dog tag", "name tag", "id tag", "collar tag", "microchip tag", "pet", "bone"])
def _(S):
    b = union(rect(5, 12.5, 14, 6.5), circle(5.3, 12.7, 3.2), circle(5.3, 18.8, 3.2),
              circle(18.7, 12.7, 3.2), circle(18.7, 18.8, 3.2))
    return [
        line(circle(12, 5, 2.6)),
        shell(b),
        dot(12, 15.75, 1.3),
    ]


@icon("dog-harness", CAT, "Front view of a padded dog harness with a neck opening, chest strap and buckle",
      tags=["harness", "no pull harness", "dog vest", "walking harness", "pet gear", "leash", "strap"])
def _(S):
    body = poly([(7, 3), (17, 3), (20, 9), (18, 21), (6, 21), (4, 9)], closed=True, r=S.r)
    return [
        shell(body),
        detail("M8.5 3.5Q12 11 15.5 3.5"),
        detail(seg(5, 15.5, 19, 15.5)),
        sq(10.5, 12.5, 3, 3.5, L(S, 0, 0.7)),
    ]


@icon("dog-muzzle", CAT, "Side view of a basket muzzle made of vertical bars with a head strap looping over the top",
      tags=["muzzle", "basket muzzle", "dog safety", "bite", "snout", "vet", "pet gear"])
def _(S):
    return [
        shell(poly([(2.5, 11), (16, 9.5), (16, 20), (2.5, 18.5)], closed=True, r=S.r)),
        detail(seg(7, 10.5, 7, 19.2)),
        detail(seg(11.5, 10, 11.5, 19.7)),
        line("M10 9.8C10 2.5 21.5 2.5 21.5 15L16 15"),
    ]


@icon("leash-hook", CAT, "Wall plate with a paw print above a peg and a leash loop hanging from a hook",
      tags=["leash holder", "wall hook", "entryway", "dog leash hanger", "pet storage", "paw", "hook"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 11, L(S, 2, 3.5))),
        mark(pawprint(12, 8.2, 1.0)),
        line(seg(7, 13.5, 7, 17)),
        dot(7, 18, 1.1),
        line(seg(16.5, 13.5, 16.5, 16)),
        shell(ellipse(16.5, 18.6, 3, 2.6)),
    ]


# ============================================================================ beds and housing

@icon("dog-bed", CAT, "Oval bolster pet bed seen at an angle with a raised rim and a sunken cushion",
      tags=["pet bed", "dog cushion", "bolster bed", "sleeping", "basket", "pet furniture", "nap"])
def _(S):
    ry = L(S, 4.6, 5.2)
    body = union(ellipse(12, 12.5, 10, ry), ellipse(12, 15.5, 10, ry), rect(2, 12.5, 20, 3))
    return [shell(body), detail(ellipse(12, 12.4, 5.8, 2))]


@icon("cat-cave-bed", CAT, "Domed cat bed with a round entrance hole at the front and two ear points on top",
      tags=["cat cave", "cat bed", "felt cave", "pet hideout", "kitten", "cosy", "pet bed"])
def _(S):
    dome = "M3 20V14C3 9 7 6.5 12 6.5C17 6.5 21 9 21 14V20Z"
    ears = union(poly([(5.5, 9), (6, 3.5), (10, 6.7)], closed=True), poly([(18.5, 9), (18, 3.5), (14, 6.7)], closed=True))
    return [shell(union(dome, ears)), detail(circle(12, 16, 3.2))]


@icon("dog-house", CAT, "Small wooden kennel with a pitched roof and an arched doorway",
      tags=["kennel", "doghouse", "dog shelter", "outdoor pet home", "pet house", "yard", "puppy"])
def _(S):
    return [
        shell(poly([(2.5, 11.5), (12, 4), (21.5, 11.5)], closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
        shell(rect(4.5, 11.5, 15, 9.5, 0)),
        detail("M9 21V17.5A3 3 0 0 1 15 17.5V21"),
    ]


@icon("dog-crate", CAT, "Rectangular wire crate with vertical bars and a carry handle on top",
      tags=["kennel crate", "wire crate", "dog cage", "training crate", "puppy crate", "pet", "cage"])
def _(S):
    return [
        line(poly([(9, 7), (9, 4), (15, 4), (15, 7)], r=S.r)),
        shell(rect(3, 7, 18, 13, L(S, 2, 3.5))),
        detail(seg(8, 7, 8, 20)),
        detail(seg(12, 7, 12, 20)),
        detail(seg(16, 7, 16, 20)),
    ]


@icon("pet-carrier", CAT, "Hard pet carrier with a top handle, vent slots on the side and a barred door at the front",
      tags=["cat carrier", "dog carrier", "travel crate", "vet visit", "kennel", "transport", "pet travel"])
def _(S):
    return [
        line(poly([(8, 8), (8, 4), (16, 4), (16, 8)], r=S.r)),
        shell(rect(2.5, 8, 19, 12.5, L(S, 2, 4))),
        detail(seg(6, 12.5, 9, 12.5)),
        detail(seg(6, 16, 9, 16)),
        detail(seg(13, 10.5, 13, 18)),
        detail(seg(17, 10.5, 17, 18)),
    ]


@icon("pet-door", CAT, "Door with a small flap near the bottom and a paw print above it",
      tags=["cat flap", "dog door", "pet flap", "doggy door", "cat door", "entry", "home"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, L(S, 1.5, 3.5))),
        mark(pawprint(12, 8, 1.15)),
        detail(poly([(8.5, 14), (15.5, 14), (17, 19.5), (10, 19.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("pet-gate", CAT, "Freestanding gate of vertical bars with a small swing door in the lower middle",
      tags=["baby gate", "dog gate", "safety gate", "barrier", "stair gate", "fence", "pet proofing"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 18, L(S, 1.5, 3.5))),
        detail(seg(6.5, 3, 6.5, 21)),
        detail(seg(17.5, 3, 17.5, 21)),
        detail(rect(9.5, 11.5, 5, 9.5, L(S, 0, 1))),
        dot(13, 16.5, 0.0 + 0.9),
    ]


@icon("pet-playpen", CAT, "Octagonal fold-out exercise pen of mesh panels seen at an angle",
      tags=["exercise pen", "x-pen", "puppy pen", "play pen", "fence", "enclosure", "run"])
def _(S):
    n = 8
    top = [(12 + 9.5 * math.cos(math.radians(-22.5 + i * 45)), 8 + 4.2 * math.sin(math.radians(-22.5 + i * 45))) for i in range(n)]
    bot = [(x, y + 9) for x, y in top]
    return [
        shell(union(ellipse(12, 8, 9.5, 4.2), ellipse(12, 17, 9.5, 4.2), rect(2.5, 8, 19, 9))),
        detail(ellipse(12, 8, 9.5, 4.2)) if S.name == "rounded" else detail(poly(top, closed=True)),
        detail(seg(8, 12.5, 8, 20)),
        detail(seg(12, 12.5, 12, 21.2)),
        detail(seg(16, 12.5, 16, 20)),
    ]


@icon("pet-stairs", CAT, "Three carpeted steps in side view with a paw print on the body of the stairs",
      tags=["dog stairs", "pet steps", "cat steps", "ramp", "sofa steps", "bed steps", "senior pet"])
def _(S):
    return [
        shell(poly([(2.5, 21), (2.5, 17), (8, 17), (8, 13), (13.5, 13), (13.5, 9), (21.5, 9), (21.5, 21)], closed=True, r=S.r * 0.5)),
        mark(pawprint(17.6, 15.4, 0.8)),
    ]


@icon("cat-tree", CAT, "Tall cat tower with a post, two platforms, a cube hideout with a round hole and a base",
      tags=["cat tower", "cat condo", "climbing tower", "kitten furniture", "perch", "cat furniture", "scratcher"])
def _(S):
    return [
        shell(rect(3, 18.5, 18, 3, L(S, 0.5, 1.5))),
        line(seg(7, 6.5, 7, 18.5)),
        shell(rect(2.5, 3.5, 10, 3, L(S, 0.5, 1.5))),
        shell(rect(8, 10.5, 12.5, 8, L(S, 1, 2.5))),
        dot(14.5, 14.5, 1.6),
        line(seg(13.5, 10.5, 13.5, 8)),
    ]


@icon("scratching-post", CAT, "Upright post wrapped in rope on a square base with a small ball hanging from the top",
      tags=["cat scratcher", "sisal post", "claw post", "cat furniture", "scratch", "kitten", "toy ball"])
def _(S):
    return [
        shell(rect(3, 18.5, 14, 3, L(S, 0.5, 1.5))),
        shell(rect(6.5, 4.5, 7, 14, L(S, 1, 2))),
        detail(seg(6.5, 9, 13.5, 9)),
        detail(seg(6.5, 14, 13.5, 14)),
        line("M13.5 6.5H19V10"),
        shell(circle(19, 13, 2.4)),
    ]


@icon("cat-window-perch", CAT, "Window frame with a hammock shelf held by suction cups on the lower pane",
      tags=["window seat", "cat hammock", "window bed", "suction cup perch", "cat shelf", "sunbathing", "window"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, L(S, 1.5, 3.5))),
        detail(seg(12, 2.5, 12, 12)),
        detail(seg(3, 7, 21, 7)),
        shell(rect(1.5, 12, 21, 3.5, L(S, 1, 1.75))),
    ]


@icon("cat-scratcher-lounge", CAT, "Curved cardboard cat lounger seen from the side with its layered corrugated edge",
      tags=["cardboard scratcher", "cat lounge", "cat bed", "corrugated", "scratch pad", "curved scratcher", "kitten"])
def _(S):
    outer = ellipse(12, 7, 9.2, 13)
    inner = ellipse(12, 5.6, 6.6, 9.2)
    crescent = minus(minus(outer, inner), rect(-5, -20, 34, 29.5))
    mid = "M6.5 11.5C8 14.5 9.8 16 12 16C14.2 16 16 14.5 17.5 11.5"
    return [shell(crescent), detail(mid)]


# ============================================================================ cages and feeding

@icon("hamster-cage", CAT, "Wire-top cage on a deep plastic base with a running wheel inside",
      tags=["small pet cage", "rodent cage", "gerbil", "hamster home", "habitat", "exercise wheel", "pet"])
def _(S):
    return [
        line(poly([(5, 12), (5, 4.5), (19, 4.5), (19, 12)], r=S.r)),
        line(seg(9.5, 4.5, 9.5, 12)),
        line(seg(14.5, 4.5, 14.5, 12)),
        shell(rect(2.5, 12, 19, 9.5, L(S, 1.5, 3.5))),
        detail(circle(9, 16.75, 2.9)),
        dot(9, 16.75, 0.0 + 0.8),
    ]


@icon("rabbit-hutch", CAT, "Wooden hutch on legs with a pitched roof, a mesh door and a solid door",
      tags=["rabbit house", "bunny hutch", "guinea pig home", "outdoor cage", "small animal", "backyard", "pet"])
def _(S):
    return [
        shell(poly([(2, 9), (12, 3), (22, 9)], closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
        shell(rect(3.5, 9, 17, 8.5, 0)),
        detail(seg(12, 9, 12, 17.5)),
        detail(seg(8, 10, 8, 16.5)),
        dot(16, 13.3, 1.0),
        line(seg(6, 17.5, 6, 21.5)),
        line(seg(18, 17.5, 18, 21.5)),
    ]


@icon("dog-kennel-run", CAT, "Chain link fence pen with a small kennel roof peeking above the top rail",
      tags=["dog run", "chain link", "outdoor pen", "fenced yard", "kennel", "enclosure", "boarding"])
def _(S):
    return [
        line(poly([(7.5, 6), (12, 2.8), (16.5, 6)], r=S.r)),
        shell(rect(2.5, 6, 19, 14.5, L(S, 1.5, 3))),
        detail(poly([(3.5, 8.5), (9.5, 18), (15.5, 8.5), (20.5, 16)])),
        detail(poly([(3.5, 18), (9.5, 8.5), (15.5, 18), (20.5, 10.5)])),
    ]


@icon("raised-pet-feeder", CAT, "Low stand holding two bowls side by side at the top",
      tags=["elevated feeder", "double bowl", "dog diner", "cat feeder", "bowl stand", "food and water", "feeding station"])
def _(S):
    return [
        shell(poly([(4, 8), (10.5, 8), (9.5, 13.5), (5, 13.5)], closed=True, r=S.r)),
        shell(poly([(13.5, 8), (20, 8), (19, 13.5), (14.5, 13.5)], closed=True, r=S.r)),
        shell(rect(2.5, 13.5, 19, 3.5, L(S, 0.5, 1.75))),
        line(seg(5.5, 17, 5.5, 21.5)),
        line(seg(18.5, 17, 18.5, 21.5)),
    ]


@icon("slow-feeder-bowl", CAT, "Top view of a round bowl whose floor is a maze of curved ridges",
      tags=["slow feeder", "puzzle bowl", "anti gulp", "maze bowl", "dog bowl", "healthy eating", "pet dish"])
def _(S):
    rim = circle(12, 12, 9.5) if S.name == "rounded" else poly(regular(12, 12, 10, 8, -22.5), closed=True)
    return [
        shell(rim),
        detail(arc(12, 12, 5.6, -20, 250)),
        dot(12, 12, 1.4),
    ]


@icon("small-pet-water-bottle", CAT, "Upside-down water bottle clipped to cage bars with a metal sipper tube and a drip",
      tags=["hamster bottle", "rabbit water bottle", "cage bottle", "sipper", "drinker", "guinea pig", "gravity feeder"])
def _(S):
    return [
        line(seg(3, 2.5, 3, 21.5)),
        line(seg(21, 2.5, 21, 21.5)),
        line(seg(3, 7, 7.5, 7)),
        line(seg(21, 7, 16.5, 7)),
        shell(rect(7.5, 3, 9, 10.5, L(S, 3, 4.5))),
        shell(rect(10, 13.5, 4, 2.5, 0)),
        line(poly([(12, 16), (12, 18.5), (14.5, 20.5)])),
    ]


@icon("collapsible-pet-bowl", CAT, "Flat folding silicone bowl with ridged sides and a small clip on its rim",
      tags=["travel bowl", "foldable bowl", "portable bowl", "silicone dish", "hiking dog", "camping", "pet dish"])
def _(S):
    return [
        shell(poly([(2.5, 10.5), (21.5, 10.5), (18.5, 20), (5.5, 20)], closed=True, r=S.r)),
        detail(seg(4.3, 14, 19.7, 14)),
        shell(rect(15.5, 2.5, 5, 6.5, L(S, 1, 2.5))),
    ]


def fish_mark(cx, cy, s=1.0, S=None):
    body = ellipse(cx - 0.8 * s, cy, 3.2 * s, 2.0 * s)
    tail = poly([(cx + 1.6 * s, cy), (cx + 4.0 * s, cy - 1.9 * s), (cx + 4.0 * s, cy + 1.9 * s)], closed=True)
    return union(body, tail)


@icon("pet-travel-water-bottle", CAT, "Slim water bottle with a flip-out trough cup attached to the top",
      tags=["portable water bottle", "dog water bottle", "walk bottle", "hydration", "travel drinker", "hiking", "pet"])
def _(S):
    trough = "M11.5 10.5C12.5 6 18 4.5 21 8.5C19.5 12.5 15 14 11.5 13.5Z"
    return [
        shell(rect(3.5, 9, 8, 12.5, L(S, 2, 3.5))),
        shell(rect(5.5, 4.5, 4, 4.5, L(S, 0.5, 1.2))),
        shell(trough),
        detail(seg(3.5, 14, 11.5, 14)),
    ]


def piece(S, x, y, r):
    if S.name == "rounded":
        return circle(x, y, r)
    return rect(x - r * 0.85, y - r * 0.85, r * 1.7, r * 1.7, 0.3)


@icon("kibble", CAT, "Small heap of rounded dry food pieces with a bone-shaped biscuit on top",
      tags=["dry food", "dog food", "cat food", "pellets", "biscuits", "pet food", "feeding"])
def _(S):
    parts = [shell(piece(S, x, y, 2.4)) for x, y in ((5.5, 18.2), (12, 18.2), (18.5, 18.2), (8.75, 12.4), (15.25, 12.4))]
    parts.append(solid(bone(12, 6.3, 8.0, 0, 1.3, 1.7)))
    return parts


@icon("pet-food-bag", CAT, "Tall stand-up bag of pet food with a folded top and a large paw print on the front",
      tags=["dog food bag", "cat food sack", "kibble bag", "pet store", "pantry", "feeding", "pet supplies"])
def _(S):
    body = poly([(5.5, 7), (18.5, 7), (19.5, 21), (4.5, 21)], closed=True, r=S.r * 0.6)
    return [
        shell(body),
        shell(rect(6.5, 3, 11, 4, L(S, 0.5, 1.5))),
        mark(pawprint(12, 14.6, 1.75)),
    ]


@icon("pet-food-can", CAT, "Short wide can with a pull-tab lid and a fish on the label",
      tags=["wet food", "canned food", "tin", "cat food can", "dog food can", "pet food", "pate"])
def _(S):
    can = union(ellipse(12, 7.5, 9, 3), ellipse(12, 18, 9, 3), rect(3, 7.5, 18, 10.5))
    return [
        shell(can),
        mark(rect(10.4, 6.6, 3.2, 1.8, L(S, 0, 0.8))),
        mark(fish_mark(11, 14, 0.8)),
    ]


@icon("pet-food-scoop", CAT, "Deep measuring scoop with a long handle and kibble piled above its rim",
      tags=["measuring scoop", "food scoop", "portion", "feeding", "kibble", "dog food", "serving"])
def _(S):
    bowl = "M3.5 12.5H16.5C16.5 17.5 14 20.5 10 20.5C6 20.5 3.5 17.5 3.5 12.5Z"
    return [
        shell(bowl) if S.name == "rounded" else shell(poly([(3.5, 12.5), (16.5, 12.5), (14.5, 20), (5.5, 20)], closed=True)),
        line(seg(15.5, 14, 21.5, 8)),
        solid(piece(S, 6.5, 9.6, 1.6)),
        solid(piece(S, 10, 9.6, 1.6)),
        solid(piece(S, 13.5, 9.6, 1.6)),
        solid(piece(S, 8.3, 6.2, 1.6)),
        solid(piece(S, 11.8, 6.2, 1.6)),
    ]


@icon("treat-jar", CAT, "Glass jar with a lid knob and a bone shape on the front",
      tags=["treat container", "biscuit jar", "dog treats", "cookie jar", "canister", "pet snacks", "reward"])
def _(S):
    return [
        shell(rect(10, 2.5, 4, 2.5, L(S, 0.5, 1))),
        shell(rect(6, 5, 12, 3, L(S, 0.5, 1.2))),
        shell(rect(4.5, 8, 15, 13.5, L(S, 2, 4))),
        mark(bone(12, 14.7, 9, 0, 1.5, 2.3)),
    ]


@icon("treat-pouch", CAT, "Rounded drawstring pouch with a belt clip and a bone-shaped treat poking out",
      tags=["treat bag", "training pouch", "belt pouch", "dog training", "reward bag", "walking", "snack bag"])
def _(S):
    pouch = "M6.5 10.5C3.5 14 3.5 21 11.5 21C19.5 21 19.5 14 16.5 10.5Z"
    return [
        shell(pouch),
        detail("M5.6 12.6Q11.5 14.6 17.4 12.6"),
        solid(bone(11.5, 6, 9, 90, 1.6, 2.2)),
        line("M19 14H22V18.5"),
    ]


@icon("lick-mat", CAT, "Square rubber mat with rows of bumps and a wavy tongue smear across the middle",
      tags=["licking mat", "slow feeding mat", "peanut butter mat", "anxiety relief", "enrichment", "grooming distraction", "pet"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, L(S, 2.5, 5))),
        detail("M6.5 12C8.5 9.3 10.3 9.3 12 12S15.5 14.7 17.5 12"),
        dot(7.5, 7, 1.0), dot(12, 7, 1.0), dot(16.5, 7, 1.0),
        dot(7.5, 17, 1.0), dot(12, 17, 1.0), dot(16.5, 17, 1.0),
    ]


@icon("fish-food-flakes", CAT, "Small shaker tub tilted over the water, sprinkling flakes down",
      tags=["fish food", "aquarium feeding", "flakes", "goldfish food", "fish tank", "sprinkle", "pet fish"])
def _(S):
    tub = union(rect(3, 7, 8, 8, L(S, 1, 2)), rect(2.5, 4.5, 9, 3, L(S, 0.5, 1.2)))
    return [
        shell(rot(tub, 130, 7, 10)),
        dot(15, 10.5, 0.9), dot(18, 7.5, 0.9), dot(18.5, 12, 0.9), dot(14.5, 14, 0.9),
        line("M2 20.5Q4.75 18 7.5 20.5T13 20.5T18.5 20.5T22 20.5"),
    ]


@icon("catnip", CAT, "Catnip sprig with kite-shaped leaves and a flower spike on top",
      tags=["cat herb", "nepeta", "cat treat", "herb", "plant", "kitty", "euphoria"])
def _(S):
    r = S.r * 0.8
    return [
        line(seg(12, 21.5, 12, 9.5)),
        shell(poly([(12, 9.5), (14.4, 6), (12, 2.5), (9.6, 6)], closed=True, r=r)),
        shell(poly([(11.3, 18), (5.5, 19.5), (2.8, 13.2), (8.3, 12.7)], closed=True, r=r)),
        shell(poly([(12.7, 14.5), (18.5, 15.5), (21.2, 9.6), (15.7, 9.2)], closed=True, r=r)),
    ]


@icon("cat-grass", CAT, "Small pot filled with tall straight blades of grass",
      tags=["cat grass pot", "wheatgrass", "oat grass", "hairball help", "indoor plant", "pet safe plant", "greens"])
def _(S):
    return [
        shell(poly([(4.5, 13.5), (19.5, 13.5), (17.5, 21.5), (6.5, 21.5)], closed=True, r=S.r * 0.6)),
        line("M8.5 13.5C8.5 9 6.5 7 6 3.5"),
        line("M12 13.5V3"),
        line("M15.5 13.5C15.5 9 17.5 7 18 3.5"),
    ]


@icon("hay-rack", CAT, "Small V-shaped wire rack stuffed with hay stalks poking out of the top",
      tags=["hay feeder", "rabbit hay", "guinea pig", "cage accessory", "forage", "small animal", "manger"])
def _(S):
    return [
        shell(poly([(3.5, 10), (20.5, 10), (15.5, 20.5), (8.5, 20.5)], closed=True, r=S.r * 0.7)),
        detail(seg(6, 13.5, 18, 13.5)),
        detail(seg(8, 17, 16, 17)),
        line(seg(7, 10, 5.5, 3.5)),
        line(seg(11, 10, 10.5, 3)),
        line(seg(14, 10, 15.5, 3.5)),
        line(seg(17.5, 10, 19.5, 5)),
    ]


# ============================================================================ toys

@icon("rope-toy", CAT, "Knotted rope in a gentle S curve with a large knot at each end",
      tags=["tug toy", "chew toy", "dog toy", "knotted rope", "tug of war", "fetch", "play"])
def _(S):
    return [
        line("M6.5 17.5C12 16.5 10.5 12.5 12 12C13.5 11.5 12 7.5 17.5 6.5"),
        shell(circle(5, 18.8, 3)) if S.name == "rounded" else shell(rect(2.2, 16, 5.6, 5.6)),
        shell(circle(19, 5.2, 3)) if S.name == "rounded" else shell(rect(16.2, 2.4, 5.6, 5.6)),
    ]


@icon("ball-launcher", CAT, "Long curved plastic arm with a handle at one end and a ball held in a cup at the other",
      tags=["ball thrower", "fetch", "ball chucker", "dog toy", "throwing stick", "tennis ball", "play outside"])
def _(S):
    return [
        shell(rect(3.5, 15.5, 4.5, 6, L(S, 1.5, 2.2))),
        line("M5.8 15.5C6.5 11.5 9 8.5 13.5 7"),
        line(arc(17, 7, 3.8, 10, 300)),
        dot(18.4, 6, 1.6),
    ]


@icon("treat-puzzle-toy", CAT, "Flat puzzle board with two round lids and a sliding cover over treat hollows",
      tags=["puzzle feeder", "enrichment toy", "brain game", "interactive toy", "hide treats", "dog puzzle", "mental stimulation"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 17, L(S, 2, 4))),
        detail(circle(8, 9, 2.2)),
        detail(circle(16, 9, 2.2)),
        detail(circle(8, 16, 2.2)),
        dot(16, 16, 1.5),
    ]


@icon("cat-wand-toy", CAT, "Thin stick with a string hanging from its tip down to a feather",
      tags=["teaser wand", "feather toy", "interactive cat toy", "fishing pole toy", "kitten play", "dangle", "pounce"])
def _(S):
    return [
        line(seg(3, 21, 13.5, 4.5)),
        line("M13.5 4.5C18 5 18.5 8 18.5 11"),
        shell(poly([(18.5, 11), (21.3, 15.5), (18.5, 21.5), (15.7, 15.5)], closed=True, r=S.r * 0.7)),
        detail(seg(18.5, 13.5, 18.5, 18.5)),
    ]


@icon("toy-mouse", CAT, "Stuffed toy mouse with a stitched seam along its back and a long curving tail",
      tags=["cat toy", "catnip mouse", "plush mouse", "kitten toy", "chase", "fake mouse", "pet play"])
def _(S):
    body = poly([(2.5, 17.5), (4.5, 12), (12, 8.5), (19, 12), (19.5, 17.5)], closed=True, r=S.r * 1.6 + 1.2)
    return [
        shell(union(body, circle(12.5, 8.8, 2.8))),
        detail("M6.5 13.5C9 11.6 12.5 11.5 15.5 13"),
        dot(6.5, 15.6, 0.9),
        line("M19.5 16.5C23 16.5 23 11 20.5 9.5"),
    ]


@icon("cat-tunnel", CAT, "Crinkle play tunnel in perspective: a ribbed tube with a round opening at the front",
      tags=["play tunnel", "crinkle tunnel", "collapsible tunnel", "cat toy", "rabbit tunnel", "kitten", "hide and seek"])
def _(S):
    tube = union(ellipse(7, 12, 3.6, 8), poly([(7, 4), (19, 6), (19, 18), (7, 20)], closed=True),
                 ellipse(19, 12, 2, 6) if S.name == "rounded" else rect(19, 6, 0.1, 12))
    return [
        shell(tube),
        detail("M7 4A3.6 8 0 0 1 7 20"),
        detail("M14.3 5.2Q16.3 12 14.3 18.8"),
    ]


@icon("laser-toy", CAT, "Pen-shaped laser pointer sending a dashed beam to a small bright dot",
      tags=["laser pointer", "red dot", "cat toy", "chase", "light toy", "interactive play", "pet exercise"])
def _(S):
    def r(pts):
        return rp(pts, -38, 7, 17)
    return [
        shell(rot(rect(2.5, 14.5, 10, 5, L(S, 1.5, 2.5)), -38, 7.5, 17)),
        line(poly(r([(14, 17), (15.8, 17)]))),
        line(poly(r([(18, 17), (19.8, 17)]))),
        dot(20, 5.2, 1.9),
    ]


@icon("cat-ball-track", CAT, "Circular ring track seen at an angle with a ball rolling in the channel",
      tags=["cat circuit", "ball tower", "rolling ball toy", "kitten play", "track toy", "swat", "interactive toy"])
def _(S):
    ry = L(S, 7.2, 7.8)
    return [
        shell(ellipse(12, 12.5, 10, ry)),
        detail(ellipse(12, 11.6, 5.8, 3.3)),
        dot(12, 17.9, 1.3),
    ]


@icon("squeaky-toy", CAT, "Rubber chicken toy with an open beak and a comb, small squeak lines beside it",
      tags=["rubber chicken", "chew toy", "dog toy", "squeaker", "noise toy", "play", "puppy"])
def _(S):
    body = union(circle(12, 15, 6.4), circle(8, 8.3, 3.2), rect(6.6, 8.5, 4.2, 6.5))
    return [
        shell(body),
        line(poly([(5, 7), (2.3, 6.3)])),
        line(poly([(5, 9.6), (2.3, 10.4)])),
        line(poly([(6.4, 5.2), (7.4, 3.6), (9, 5), (10.2, 3.6), (10.6, 5.4)], r=S.r * 0.6), stroke_miterlimit="1.5"),
        dot(8.6, 8, 0.9),
        line(seg(19.5, 8, 21.5, 6.3)),
        line(seg(20.3, 11.5, 22, 11.5)),
    ]


@icon("hamster-ball", CAT, "Clear exercise ball with vent slots and a hamster silhouette inside",
      tags=["exercise ball", "rodent ball", "hamster run", "gerbil ball", "small pet play", "roll", "clear ball"])
def _(S):
    tiny = union(ellipse(13, 15.5, 4.6, 3.3), circle(8.8, 14.2, 2.4), circle(9.6, 11.6, 1.0))
    slot = detail(seg(9, 6.2, 15, 6.2)) if S.name == "line" else detail(seg(10, 6.2, 14, 6.2))
    return [
        shell(circle(12, 12, 9.5)),
        slot,
        mark(tiny),
    ]


@icon("bird-mirror-toy", CAT, "Small round mirror hanging on a chain with a tiny bell below",
      tags=["parrot toy", "budgie mirror", "cage toy", "bird cage accessory", "bell", "perch toy", "pet bird"])
def _(S):
    mirror = circle(12, 10, 5.5) if S.name == "rounded" else poly(regular(12, 10, 6, 8, -22.5), closed=True)
    return [
        line(seg(12, 2, 12, 4.5)),
        shell(mirror),
        detail(seg(9.2, 11.5, 11.4, 8.4)),
        line(seg(12, 15.5, 12, 17)),
        shell(circle(12, 19.4, 2.3)),
    ]


# ============================================================================ grooming

@icon("slicker-brush", CAT, "Rectangular brush head of dense bent wire pins on a long handle",
      tags=["grooming brush", "pin brush", "dog brush", "cat brush", "detangle", "coat care", "fur"])
def _(S):
    def R(d):
        return rot(d, 38, 12, 13)

    def Rp(pts):
        return rp(pts, 38, 12, 13)
    parts = [
        shell(R(rect(4.5, 9, 15, 5, L(S, 1, 2)))),
        shell(R(poly([(10, 14), (14, 14), (13.5, 21.5), (10.5, 21.5)], closed=True, r=S.r * 0.6))),
    ]
    for x in (8, 12, 16):
        parts.append(line(poly(Rp([(x, 9), (x, 4.6)]))))
        c = Rp([(x, 3.6)])[0]
        parts.append(solid(circle(c[0], c[1], 1.2)))
    return parts


@icon("deshedding-tool", CAT, "Handle with a wide flat comb blade of fine teeth held at a right angle",
      tags=["undercoat rake", "shedding comb", "fur remover", "coat comb", "dog grooming", "cat grooming", "hair"])
def _(S):
    return [
        shell(rect(8.5, 2.5, 7, 8, L(S, 2, 3))),
        shell(rect(3, 10.5, 18, 4.5, L(S, 0.5, 1.5))),
        line(seg(5, 15, 5, 20)),
        line(seg(8.5, 15, 8.5, 20)),
        line(seg(12, 15, 12, 20)),
        line(seg(15.5, 15, 15.5, 20)),
        line(seg(19, 15, 19, 20)),
    ]


@icon("pet-nail-clipper", CAT, "Scissor-style nail clippers with two handle loops and a notched cutting tip",
      tags=["claw clipper", "nail trimmer", "dog nails", "cat claws", "paw care", "grooming tool", "trim"])
def _(S):
    return [
        shell(circle(7, 18, 3) if S.name == "rounded" else rect(4.2, 15.2, 5.6, 5.6)),
        shell(circle(17, 18, 3) if S.name == "rounded" else rect(14.2, 15.2, 5.6, 5.6)),
        line("M8.6 15.4L14.5 7"),
        line("M15.4 15.4L9.5 7"),
        line(arc(12, 6.4, 2.5, 180, 360)),
    ]


@icon("pet-shampoo", CAT, "Squeeze bottle with a flip cap and a paw print on the label, bubbles beside it",
      tags=["dog shampoo", "pet wash", "bath time", "conditioner", "grooming product", "suds", "hypoallergenic"])
def _(S):
    return [
        shell(rect(3.5, 8.5, 11, 13, L(S, 2, 4))),
        shell(rect(6.5, 5.5, 5, 3, L(S, 0.5, 1))),
        shell(rect(5.5, 2.5, 7, 3, L(S, 0.5, 1.5))),
        mark(pawprint(9, 15.2, 1.15)),
        line(circle(19.3, 8, 2.3)),
        dot(19, 15, 1.2),
    ]


@icon("dog-bath", CAT, "Dog with floppy ears sitting in a tub with soap bubbles above its head",
      tags=["dog wash", "bathing", "pet bath", "tub", "shower", "grooming", "suds"])
def _(S):
    tub = "M2.5 14.5H21.5V16C21.5 19.5 19 21.5 15.5 21.5H8.5C5 21.5 2.5 19.5 2.5 16Z"
    head = union(circle(12, 9.6, 3.8), rot(ellipse(7.3, 9.6, 1.5, 3.4), 12, 7.3, 9.6), rot(ellipse(16.7, 9.6, 1.5, 3.4), -12, 16.7, 9.6))
    return [
        shell(tub) if S.name == "rounded" else shell(poly([(2.5, 14.5), (21.5, 14.5), (20, 21.5), (4, 21.5)], closed=True)),
        shell(head),
        dot(10.6, 9.2, 0.8), dot(13.4, 9.2, 0.8),
        dot(12, 11.6, 0.0 + 0.9),
        line(circle(18.5, 4.6, 1.8)),
        dot(14.5, 3.4, 0.9),
        dot(21, 8.5, 0.9),
    ]


@icon("pet-dryer", CAT, "Upright blaster dryer on a wheeled pole with a long hose and nozzle pointing out",
      tags=["blow dryer", "force dryer", "grooming dryer", "fur dryer", "pet salon", "hose", "blower"])
def _(S):
    return [
        shell(rect(3, 2.5, 10, 9, L(S, 2, 4))),
        detail(seg(5.5, 5.5, 10.5, 5.5)),
        detail(seg(5.5, 8.5, 10.5, 8.5)),
        line(seg(8, 11.5, 8, 18.5)),
        line(seg(3.5, 18.5, 12.5, 18.5)),
        dot(4.5, 21, 1.2), dot(11.5, 21, 1.2),
        line("M13 6C17 6 15 12.5 18 12.5"),
        shell(poly([(18, 10), (22, 8.6), (22, 16.4), (18, 15)], closed=True, r=S.r * 0.5)),
    ]


@icon("grooming-shears", CAT, "Pair of long curved shears with a small finger rest on one handle",
      tags=["pet scissors", "curved shears", "fur trimming", "haircut", "groomer", "trimming", "salon tools"])
def _(S):
    return [
        shell(circle(7, 18.5, 2.8) if S.name == "rounded" else rect(4.4, 15.9, 5.4, 5.4)),
        shell(circle(17, 18.5, 2.8) if S.name == "rounded" else rect(14.4, 15.9, 5.4, 5.4)),
        line("M8.4 16C11 11.5 13.5 8 14 2.8"),
        line("M15.6 16C13 11.5 10.5 8 10 2.8"),
        line(seg(20.4, 17.5, 22, 19.5)),
    ]


@icon("pet-clippers", CAT, "Electric clippers with a comb guard on the blade and a cord from the side",
      tags=["hair clippers", "fur clippers", "pet trimmer", "shaver", "groomer", "haircut", "electric"])
def _(S):
    return [
        line(seg(8.5, 2.5, 8.5, 5.5)),
        line(seg(12, 2.5, 12, 5.5)),
        line(seg(15.5, 2.5, 15.5, 5.5)),
        shell(poly([(7, 9), (17, 9), (16, 5.5), (8, 5.5)], closed=True, r=S.r * 0.5)),
        shell(rect(7.5, 9, 9, 12.5, L(S, 2, 4))),
        dot(12, 14, 1.1),
        line(poly([(16.5, 18), (19.5, 18), (21.2, 16), (21.2, 12)], r=S.r)),
    ]


@icon("pet-toothbrush", CAT, "Rubber finger brush sleeve with bristle nubs beside a tooth outline",
      tags=["dog dental", "finger toothbrush", "teeth cleaning", "oral care", "tartar", "dog teeth", "pet hygiene"])
def _(S):
    tooth = ("M13 8C13 5 14 3.5 15.5 3.5C16.5 3.5 16.7 4.5 17 4.5C17.3 4.5 17.5 3.5 18.5 3.5C20 3.5 21 5 21 8"
             "C21 11 19.8 13 19.5 16.5C19.3 18.5 17.8 18.5 17.4 16.5L17 13.5L16.6 16.5C16.2 18.5 14.7 18.5 14.5 16.5C14.2 13 13 11 13 8Z")
    return [
        shell(rect(2.5, 7, 7.5, 14.5, L(S, 3, 3.75))),
        dot(5.3, 11.5, 0.75), dot(7.5, 11.5, 0.75), dot(5.3, 14.8, 0.75), dot(7.5, 14.8, 0.75),
        shell(tooth),
    ]


@icon("pet-grooming", CAT, "Poodle head with a pom-pom topknot and a pair of scissors beside it",
      tags=["pet salon", "dog groomer", "poodle cut", "haircut", "spa", "trim", "fluff"])
def _(S):
    head = union(circle(8.5, 5.8, 3.4), ellipse(8.5, 14.3, 4.4, 5.6), ellipse(4.1, 14.6, 1.8, 4), ellipse(12.9, 14.6, 1.8, 4))
    return [
        shell(head),
        dot(7, 13.3, 0.85), dot(10, 13.3, 0.85),
        dot(8.5, 16.6, 1.0),
        line(seg(16, 3.5, 21, 13)),
        line(seg(21, 3.5, 16, 13)),
        line(circle(16, 16.8, 1.7)) if S.name == "rounded" else line(rect(14.4, 15.2, 3.2, 3.2)),
        line(circle(21, 16.8, 1.7)) if S.name == "rounded" else line(rect(19.4, 15.2, 3.2, 3.2)),
    ]


@icon("pet-wipes", CAT, "Soft pack of wipes with one wipe pulled up out of the lid, a paw print on the pack",
      tags=["pet wipes", "paw cleaner", "grooming wipes", "hygiene", "clean up", "wet wipes", "tissue"])
def _(S):
    return [
        shell(poly([(9, 10.5), (9, 6.5), (13, 3.2), (16.5, 6), (15.5, 10.5)], closed=True, r=S.r)),
        shell(rect(3, 10.5, 18, 10.5, L(S, 2, 3.5))),
        detail(seg(3, 13.5, 21, 13.5)),
        mark(pawprint(12, 17.5, 0.85)),
    ]


# ============================================================================ clothing, travel and tech

@icon("dog-coat", CAT, "Side view of a dog wearing a quilted coat that covers its back",
      tags=["dog jacket", "winter coat", "pet sweater", "cold weather", "dog clothes", "raincoat", "puppy wear"])
def _(S):
    head = union(poly([(2.5, 10), (5.5, 7.5), (9, 7.5), (9, 13), (2.5, 13)], closed=True), poly([(5.6, 7.8), (6.2, 4), (8.6, 7.6)], closed=True))
    return [
        shell(rect(8.5, 7.5, 12.5, 8, L(S, 2, 3.5))),
        detail(seg(13, 7.5, 13, 15.5)),
        detail(seg(16.8, 7.5, 16.8, 15.5)),
        shell(head),
        line(seg(10.5, 15.5, 10.5, 21)),
        line(seg(18.5, 15.5, 18.5, 21)),
        line(seg(21, 8.5, 22, 5)),
    ]


@icon("dog-boots", CAT, "Pair of small paw booties with a strap and thick soles",
      tags=["dog shoes", "paw protectors", "booties", "snow boots", "hot pavement", "paw care", "winter gear"])
def _(S):
    def boot(x):
        return [
            shell(union(rect(x, 3.5, 7.5, 13.5, L(S, 1.5, 3)), rect(x - 0.5, 16.5, 8.5, 4, L(S, 1, 1.75)))),
            detail(seg(x, 8.5, x + 7.5, 8.5)),
        ]
    return boot(3) + boot(13.5)


@icon("pet-bandana", CAT, "Triangular bandana tied around a collar with a small paw pattern on the fabric",
      tags=["dog scarf", "neckerchief", "pet accessory", "costume", "fashion", "collar wear", "kerchief"])
def _(S):
    tri = poly([(3, 6), (21, 6), (12, 21)], closed=True, r=S.r * 0.7)
    return [
        shell(union(tri, rect(2, 3, 20, 3.5, L(S, 0.5, 1.5)))),
        mark(pawprint(12, 11.6, 1.05)),
    ]


@icon("pet-life-jacket", CAT, "Dog life vest with a grab handle on top and a buoyancy collar under the chin",
      tags=["dog lifejacket", "swim vest", "flotation", "boating", "water safety", "pool", "beach"])
def _(S):
    vest = poly([(8, 5.5), (10.5, 5.5), (12, 8), (13.5, 5.5), (16, 5.5), (20, 8), (19.5, 12), (17.5, 14.5), (17.5, 21), (6.5, 21),
                 (6.5, 14.5), (4.5, 12), (4, 8)], closed=True, r=S.r * 0.8)
    return [
        line(poly([(9.8, 6), (9.8, 2.8), (14.2, 2.8), (14.2, 6)], r=S.r * 0.6)),
        shell(vest),
        detail(seg(6.5, 17, 17.5, 17)),
        sq(10.5, 14.2, 3, 3.6, L(S, 0, 0.7)),
    ]


@icon("pet-stroller", CAT, "Pet stroller with a mesh domed canopy on a four-wheel frame and a push handle",
      tags=["dog stroller", "pram", "pet buggy", "pet transport", "walk", "senior dog", "cat stroller"])
def _(S):
    dome = "M3.5 13.5C3.5 8 7 4.5 11.5 4.5C16 4.5 18.5 8 18.5 13.5Z"
    return [
        shell(dome),
        detail("M11.5 4.5Q8.5 9 8.8 13.5"),
        detail("M11.5 4.5Q14.5 9 14.2 13.5"),
        shell(rect(3, 13.5, 16, 3, L(S, 0.5, 1.5))),
        line(seg(18.8, 12, 21.5, 8)),
        line(seg(6.5, 16.5, 6.5, 18)),
        line(seg(15.5, 16.5, 15.5, 18)),
        shell(circle(6.5, 19.7, 1.9)),
        shell(circle(15.5, 19.7, 1.9)),
    ]


@icon("dog-car-seat", CAT, "Booster basket seat hanging from a car headrest with a dog head peeking out",
      tags=["pet car seat", "booster seat", "car travel", "dog safety", "headrest hanger", "road trip", "vehicle"])
def _(S):
    head = union(circle(12, 10, 3.2), poly([(9.5, 8.3), (8.2, 5.8), (10.8, 6.8)], closed=True), poly([(14.5, 8.3), (15.8, 5.8), (13.2, 6.8)], closed=True))
    return [
        line(poly([(6, 12), (6, 3), (18, 3), (18, 12)], r=S.r)),
        shell(union(rect(3.5, 12, 17, 9, L(S, 2, 4)), head)),
        dot(10.9, 9.8, 0.75), dot(13.1, 9.8, 0.75),
    ]


@icon("pet-tracker", CAT, "Small tracker tag on a collar strap with a location pin above it",
      tags=["gps tracker", "pet locator", "lost pet", "smart tag", "collar tag", "find my pet", "location"])
def _(S):
    pin = "M12 11.5C9.3 8.8 8 7.3 8 5.7A4 4 0 0 1 16 5.7C16 7.3 14.7 8.8 12 11.5Z"
    return [
        shell(pin),
        dot(12, 5.7, 1.3),
        line(seg(2, 18.5, 7.8, 18.5)),
        line(seg(16.2, 18.5, 22, 18.5)),
        shell(circle(12, 18.5, 4)) if S.name == "rounded" else shell(rect(8, 14.5, 8, 8)),
        dot(12, 18.5, 1.1),
    ]


@icon("pet-camera", CAT, "Round home camera on a base with a lens and a treat slot below it",
      tags=["pet cam", "treat dispenser camera", "home monitoring", "remote viewing", "security cam", "watch pet", "two way"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 12.5, L(S, 3, 6.25))),
        dot(12, 8.7, 2.2),
        shell(rect(6, 15, 12, 6.5, L(S, 1.5, 2.5))),
        detail(seg(9, 18.3, 15, 18.3)),
    ]


# ============================================================================ litter and waste

@icon("litter-box", CAT, "Low open tray filled with litter granules and a raised heap of litter in the middle",
      tags=["cat litter tray", "litter pan", "kitty litter", "toilet", "sand box", "cat hygiene", "scoop"])
def _(S):
    tray = poly([(2.5, 11.5), (21.5, 11.5), (19.5, 20.5), (4.5, 20.5)], closed=True, r=S.r)
    heap = "M5.5 11.5C7 7.5 9.5 5.5 12 5.5C14.5 5.5 17 7.5 18.5 11.5Z"
    return [
        shell(union(tray, heap)),
        detail(seg(3, 11.5, 21, 11.5)),
        dot(8, 15.6, 0.95), dot(12, 16.8, 0.95), dot(16, 15.6, 0.95),
    ]


@icon("covered-litter-box", CAT, "Hooded litter box with a swinging flap door at the front and a handle on top",
      tags=["hooded litter box", "cat toilet", "enclosed litter pan", "privacy litter", "flap door", "kitty", "cat hygiene"])
def _(S):
    return [
        line(poly([(9, 5.5), (9, 3), (15, 3), (15, 5.5)], r=S.r)),
        shell("M3 21V13.5C3 8.5 7 5.5 12 5.5C17 5.5 21 8.5 21 13.5V21Z") if S.name == "rounded" else shell(poly([(3, 21), (3, 11), (7, 5.5), (17, 5.5), (21, 11), (21, 21)], closed=True)),
        detail(poly([(8, 21), (8, 13.5), (16, 13.5), (16, 21)], r=S.r * 0.5)),
        detail(seg(8, 17, 16, 17)),
    ]


@icon("litter-scoop", CAT, "Slotted scoop with a grid of holes and a straight handle",
      tags=["litter shovel", "cat litter", "clump scoop", "sifter", "waste", "kitty", "clean"])
def _(S):
    def R(d):
        return rot(d, 30, 12, 12)

    def Rp(pts):
        return rp(pts, 30, 12, 12)
    parts = [shell(R(poly([(6, 4.5), (18, 4.5), (17, 13), (7, 13)], closed=True, r=S.r * 0.8)))]
    for x, y in ((9.8, 7.6), (14.2, 7.6), (12, 10.6)):
        c = Rp([(x, y)])[0]
        parts.append(dot(c[0], c[1], 1.0))
    parts.append(line(poly(Rp([(12, 13), (12, 21)]))))
    return parts


@icon("poop-bag-dispenser", CAT, "Small bone-shaped dispenser with a bag roll peeking out and a clip on top",
      tags=["waste bag holder", "dog waste bags", "leash accessory", "walk", "clean up", "poo bags", "pickup"])
def _(S):
    b = union(rect(6, 10, 12, 9.5), circle(5.3, 11.2, 3.2), circle(5.3, 18.3, 3.2), circle(18.7, 11.2, 3.2), circle(18.7, 18.3, 3.2))
    return [
        shell(rect(10, 2.5, 4, 4.5, L(S, 0.5, 1.5))),
        line(seg(12, 7, 12, 10)),
        shell(b),
        detail(circle(12, 14.7, 2.6)),
    ]


@icon("pooper-scooper", CAT, "Long-handled jaw scoop with a grip at the top and a clamshell mouth at the bottom",
      tags=["poop scoop", "dog waste", "yard cleanup", "pickup tool", "jaw scoop", "grabber", "backyard"])
def _(S):
    return [
        shell(rect(9, 2.5, 6, 4, L(S, 1, 2))),
        line(seg(12, 6.5, 12, 9.5)),
        line("M4 14C4 11 7.5 9.5 12 9.5C16.5 9.5 20 11 20 14"),
        shell(poly([(3.5, 17), (20.5, 17), (18.5, 21.5), (5.5, 21.5)], closed=True, r=S.r * 0.6)),
    ]


@icon("cat-backpack", CAT, "Pet backpack with shoulder straps and a large round bubble window showing a cat face",
      tags=["pet backpack", "bubble backpack", "cat carrier bag", "astronaut backpack", "travel bag", "walk with cat", "pet transport"])
def _(S):
    ear = lambda sx: poly([(12 + sx * 3.6, 10.1), (12 + sx * 3.4, 7.2), (12 + sx * 1.6, 9.0)], closed=True)
    return [
        shell(rect(5, 3.5, 14, 18, L(S, 3, 6))),
        detail(circle(12, 11.5, 5.4)),
        mark(ear(-1)), mark(ear(1)),
        dot(10.4, 12, 0.8), dot(13.6, 12, 0.8),
        line("M4 8C2.4 11 2.4 15 4 18"),
        line("M20 8C21.6 11 21.6 15 20 18"),
    ]


@icon("snuffle-mat", CAT, "Square mat covered in rows of dense fleece loops for hiding treats",
      tags=["snuffle mat", "sniffing mat", "foraging mat", "treat hiding", "enrichment", "fleece", "nose work"])
def _(S):
    def row(y):
        d = f"M5.5 {y}"
        for _ in range(4):
            d += "a1.5 1.5 0 0 1 3 0"
        return d
    return [
        shell(rect(3, 3, 18, 18, L(S, 2.5, 5))),
        detail(row(8.5)),
        detail(row(13)),
        detail(row(17.5)),
    ]
