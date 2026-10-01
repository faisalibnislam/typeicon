"""TypeIcon Core: mythical (batch 1) - dinosaurs, prehistoric life and mythical creatures."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "mythical"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx=12, cy=12):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def flip(d):
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


def thick(d, w, S):
    return path_to_d(ST(d, w, S.cap, S.join))


def pg(pts, S, r=None):
    """Closed polygon, filleted in Rounded."""
    return poly(pts, closed=True, r=S.r if r is None else r)


def mark(d):
    return Part("dot", d)


def rr(S, a=0.5, b=1.2):
    return L(S, a, b)


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def taper(ctrl, w0, w1, n=16, r=0.0):
    """Closed polygon around a cubic centreline whose width goes from w0 to w1 (tails, necks)."""
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        x, y = bez(*ctrl, t)
        x2, y2 = bez(*ctrl, min(1, t + 1e-3))
        x1, y1 = bez(*ctrl, max(0, t - 1e-3))
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy)
        nx, ny = -dy / ln, dx / ln
        w = (w0 + (w1 - w0) * t) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return poly(left + right[::-1], closed=True, r=r)


def rseg(x1, y1, x2, y2, deg, cx=12, cy=12):
    """Rotated line segment as a d-string (open paths cannot go through pathops)."""
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    def r(x, y):
        return (cx + (x - cx) * c - (y - cy) * sn, cy + (x - cx) * sn + (y - cy) * c)
    return seg(*r(x1, y1), *r(x2, y2))


def tilt(d, deg, cx, cy):
    return rot(d, deg, cx, cy)


# --------------------------------------------------------------------------- dinosaurs

@icon("tyrannosaurus", CAT, "Side view of a T. rex with a huge head, open jaw and tiny arms",
      tags=["t-rex", "trex", "dinosaur", "predator", "jurassic", "prehistoric", "carnivore"], aliases=["t-rex"])
def _(S):
    head = pg([(3, 5.5), (9.5, 4.5), (11, 8), (10.5, 11), (4, 11), (3, 9.5)], S)
    body = tilt(ellipse(13.5, 11.5, 5, 3.6), -25, 13.5, 11.5)
    tail = taper(((16, 10.5), (18.5, 11), (20.5, 13), (22, 16)), 5, 1.5)
    leg = pg([(11.5, 12.5), (16, 12.5), (15.5, 17.5), (17, 20), (10.5, 20), (10.5, 18.5), (12, 18)], S)
    arm = pg([(9.5, 12), (7.2, 13.6), (8.2, 14.6), (10.5, 13.6)], S, r=0.4)
    return [shell(union(head, body, tail, leg, arm)), detail(seg(3, 8.2, 7, 8.2)), dot(8.2, 6.6, 0.9)]


@icon("triceratops", CAT, "Side view of a horned dinosaur with a neck frill and brow horns",
      tags=["dinosaur", "horned", "frill", "cretaceous", "prehistoric", "herbivore", "ceratops"])
def _(S):
    body = ellipse(14.5, 13.5, 6, 4)
    head = pg([(2.5, 14.5), (3.5, 12), (8, 10.5), (11, 11.5), (10.5, 16), (5, 16.5)], S)
    frill = pg([(7, 10.5), (8.5, 5), (12.5, 5.5), (14, 9), (12, 12.5)], S)
    horn = pg([(5.5, 11.5), (3, 5.5), (7.8, 10)], S, r=S.r / 2)
    nose = pg([(3, 13), (2.3, 10.5), (5, 12)], S, r=S.r / 2)
    legs = [rect(9, 16, 3.2, 4, rr(S)), rect(16.5, 16, 3.2, 4, rr(S))]
    tail = pg([(19, 11.5), (22, 14.5), (19, 15.5)], S)
    return [shell(union(body, head, frill, horn, nose, tail, *legs)), dot(7.5, 13.5, 0.9)]


@icon("stegosaurus", CAT, "Side view of a dinosaur with tall back plates and tail spikes",
      tags=["dinosaur", "plates", "spikes", "jurassic", "prehistoric", "herbivore"])
def _(S):
    body = ellipse(13, 14.5, 7, 3.5)
    head = ellipse(3.8, 16.5, 2.2, 1.5)
    neck = pg([(4.5, 15.5), (8, 12.5), (8.5, 16.5), (5, 18)], S)
    plates = [pg([(8, 12), (9.3, 6.8), (10.8, 11.8)], S, r=S.r / 2), pg([(11.7, 11.5), (13, 5.5), (14.5, 11.5)], S, r=S.r / 2),
              pg([(15.4, 11.8), (16.7, 7.5), (18, 12.8)], S, r=S.r / 2)]
    tail = taper(((18.5, 14.5), (20.5, 14), (21.5, 13), (22.2, 11)), 3.4, 1.4)
    spike = pg([(20.5, 14), (22.5, 15), (20.5, 17)], S, r=S.r / 2)
    legs = [rect(8.5, 16.5, 2.6, 4, rr(S)), rect(15.5, 16.5, 2.6, 4, rr(S))]
    return [shell(union(body, head, neck, tail, spike, *plates, *legs)), dot(3.4, 16.2, 0.8)]


@icon("velociraptor", CAT, "Side view of a slim running raptor with a stiff tail and raised sickle claw",
      tags=["raptor", "dinosaur", "predator", "claw", "jurassic", "prehistoric", "fast"])
def _(S):
    head = pg([(2.5, 6.5), (8, 6), (9.5, 9), (4, 9.5)], S)
    body = tilt(ellipse(11.5, 11.5, 5.5, 3), 25, 11.5, 11.5)
    neck = thick("M7.5 8.5L10 11", 3.2, S)
    tail = taper(((15, 13), (17.5, 13), (20, 11), (22.5, 9)), 4, 1)
    leg = pg([(10.5, 12.5), (14, 12.5), (14.5, 16.5), (12.5, 19), (13.5, 20.6), (8.5, 20.6), (9, 19.2), (11, 18)], S)
    claw = pg([(10.6, 14.3), (7.6, 15.2), (10.8, 16.6)], S, r=S.r / 2)
    return [shell(union(head, body, neck, tail, leg, claw)), dot(7, 7.3, 0.85)]


@icon("ankylosaurus", CAT, "Side view of a low armored dinosaur with studded back and a club tail",
      tags=["dinosaur", "armored", "armoured", "club tail", "cretaceous", "prehistoric", "herbivore"])
def _(S):
    body = "M4.5 17C4.5 9 18.5 9 18.5 17Z"
    studs = [circle(8, 9.4, 1.2), circle(11.5, 8.2, 1.2), circle(15, 9.4, 1.2)]
    head = pg([(1.8, 15.5), (5, 13), (6, 17), (2, 17)], S)
    legs = [rect(6.5, 16, 3, 4.5, rr(S)), rect(14, 16, 3, 4.5, rr(S))]
    tail = taper(((18, 14.5), (19.5, 14.5), (20, 14.5), (20.5, 14.2)), 2.4, 2)
    club = circle(20.3, 14, 2.3)
    return [shell(union(body, head, tail, club, *studs, *legs)), dot(4, 14.8, 0.8)]


@icon("parasaurolophus", CAT, "Side view of a duck-billed dinosaur with a long tube crest swept back from its head",
      tags=["dinosaur", "hadrosaur", "duck-billed", "crest", "cretaceous", "prehistoric", "herbivore"])
def _(S):
    head = pg([(2, 9.5), (8, 8), (10, 10), (9, 12.5), (3, 12.5)], S)
    crest = thick("M8 8.3C9.5 3.8 14 3.5 16 7.5", 2.6, S)
    body = tilt(ellipse(14, 14, 5.5, 3.6), -15, 14, 14)
    neck = thick("M8 11C10 12.5 10.5 13 11 14", 4, S)
    tail = taper(((18, 14), (20, 15), (21, 17), (22.3, 18.5)), 4, 1.3)
    legs = [rect(10.5, 16, 3, 4.5, rr(S)), rect(16, 16, 3, 4.5, rr(S))]
    return [shell(union(head, crest, body, neck, tail, *legs)), dot(6.3, 10.3, 0.8)]


@icon("corythosaurus", CAT, "Head and neck of a duck-billed dinosaur with a tall rounded helmet crest",
      tags=["dinosaur", "hadrosaur", "duck-billed", "helmet crest", "cretaceous", "prehistoric", "herbivore"])
def _(S):
    snout = pg([(1.8, 10.5), (6, 10.3), (6.5, 14.8), (1.8, 14.3)], S)
    skull = ellipse(9.5, 12.5, 4.5, 3.4)
    crest = "M6.5 10C6 3.5 15.5 3.5 14.5 10Z"
    neck = thick("M11 14C14 15.5 15 17.5 14.5 20", 5, S)
    return [shell(union(snout, skull, crest, neck)), dot(8.8, 12, 0.85)]


@icon("spinosaurus", CAT, "Side view of a long-snouted dinosaur with a tall rounded sail on its back",
      tags=["dinosaur", "sail", "predator", "cretaceous", "prehistoric", "carnivore", "fish eater"])
def _(S):
    sail = poly([(8, 13), (9, 7.2), (10.6, 8.6), (11.8, 4.8), (13.4, 7.4), (14.8, 4.2), (16, 7.4), (17.4, 5.2), (17.8, 9), (19.4, 8.4), (19.4, 13)], closed=True, r=S.r / 2)
    head = pg([(1.5, 12.5), (6.5, 11), (9, 13.5), (7.5, 16), (2, 15)], S)
    body = ellipse(13.5, 14.5, 6, 3.4)
    tail = taper(((18, 14.5), (20, 15), (21, 16.5), (22.3, 18.5)), 4, 1.4)
    legs = [rect(9.5, 16.5, 3, 4, rr(S)), rect(15.5, 16.5, 3, 4, rr(S))]
    return [shell(union(sail, head, body, tail, *legs)), dot(5.3, 13.3, 0.8)]


@icon("baryonyx", CAT, "Side view of a crocodile-snouted predator leaning forward with a huge hooked thumb claw",
      tags=["dinosaur", "predator", "claw", "crocodile snout", "cretaceous", "prehistoric", "carnivore"])
def _(S):
    head = pg([(1.5, 7.5), (9, 6), (10, 9.5), (2, 10)], S)
    body = tilt(ellipse(13, 12, 5.5, 3.6), -8, 13, 12)
    neck = thick("M8 8.8L10.5 11", 4, S)
    tail = taper(((17, 11.5), (19.5, 12), (21, 13.5), (22.3, 16)), 4.4, 1.3)
    leg = pg([(11.5, 13), (16, 13), (15.5, 17.5), (17, 20), (10.5, 20), (10.5, 18.5), (12, 18)], S)
    hook = pg([(10, 13.2), (5.5, 14.2), (4.3, 18.2), (6.6, 16.6), (10.3, 15.8)], S, r=S.r / 2)
    return [shell(union(head, body, neck, tail, leg, hook)), dot(7.5, 8, 0.8)]


@icon("pachycephalosaurus", CAT, "Side view of a dinosaur with a thick bony dome skull ringed by knobs",
      tags=["dinosaur", "dome head", "bone head", "cretaceous", "prehistoric", "herbivore", "headbutt"])
def _(S):
    dome = ellipse(7.3, 7.6, 4.2, 3.6)
    knobs = [circle(3.3, 9, 0.9), circle(4.6, 5.5, 0.9), circle(8.4, 4.1, 0.9)]
    beak = pg([(4, 9.5), (8, 11.2), (3.2, 12.3)], S, r=S.r / 2)
    neck = thick("M8.5 10C10.5 11 11.5 12 12 13", 3.6, S)
    body = tilt(ellipse(14, 14, 5.3, 3.6), -10, 14, 14)
    tail = taper(((18, 13.5), (20, 14), (21, 16), (22.3, 18)), 4, 1.3)
    legs = [rect(10.6, 16, 3, 4.5, rr(S)), rect(16, 16, 3, 4.5, rr(S))]
    return [shell(union(dome, beak, neck, body, tail, *knobs, *legs)), dot(6.2, 8, 0.8)]


@icon("pterodactyl", CAT, "Flying pterosaur seen from below with wide wings, a long beak and a head crest",
      tags=["pterosaur", "flying reptile", "dinosaur", "wings", "prehistoric", "cretaceous", "flyer"])
def _(S):
    wing = pg([(10.4, 9.5), (2, 6), (3.6, 11.5), (6.5, 11), (8, 14.5), (10.4, 13)], S)
    body = ellipse(12, 13, 2.2, 4.2)
    head = pg([(10.6, 7.5), (12, 1.8), (13.4, 7.5)], S, r=S.r / 2)
    crest = pg([(13, 5.8), (15.8, 6.6), (13.3, 8.2)], S, r=S.r / 2)
    tail = pg([(11, 16), (12, 21), (13, 16)], S, r=S.r / 2)
    return [shell(union(wing, flip(wing), body, head, crest, tail))]


@icon("quetzalcoatlus", CAT, "Giant pterosaur standing with folded wings, a very long neck and a spear-like beak",
      tags=["pterosaur", "flying reptile", "giant", "beak", "prehistoric", "cretaceous", "azhdarchid"])
def _(S):
    beak = pg([(1.5, 3.8), (9.5, 3.3), (9.5, 6.2)], S)
    neck = thick("M9 5C12 5 12.5 9 12.8 13", 2.6, S)
    body = ellipse(14, 14, 4, 3)
    wing = pg([(12, 11.5), (19, 6.5), (21.5, 8.5), (17.5, 15.5)], S)
    legs = [rect(12.3, 16, 2, 4.8, rr(S, 0.4, 1)), rect(15.8, 16, 2, 4.8, rr(S, 0.4, 1))]
    return [shell(union(beak, neck, body, wing, *legs)), dot(9.3, 4.8, 0.7)]


@icon("rhamphorhynchus", CAT, "Flying pterosaur in side view with narrow wings, a toothy beak and a long diamond-tipped tail",
      tags=["pterosaur", "flying reptile", "wings", "long tail", "prehistoric", "jurassic", "flyer"])
def _(S):
    body = ellipse(11, 12.5, 4, 2);
    head = pg([(2, 10.5), (6.5, 9.8), (8.5, 12), (3, 12.6)], S)
    wing = pg([(10, 11.5), (12.5, 3.5), (20, 3.8), (14.5, 11.8)], S)
    tail = thick("M14 13.5L19 17.5", 1.6, S)
    vane = pg([(19.5, 16.2), (22.2, 17.4), (20.2, 20.5), (18.6, 18.6)], S, r=S.r / 2)
    return [shell(union(body, head, wing, tail, vane)), dot(5.8, 11, 0.75)]


@icon("plesiosaur", CAT, "Swimming marine reptile with a long neck, small head, broad body and four flippers",
      tags=["marine reptile", "sea monster", "loch ness", "nessie", "prehistoric", "jurassic", "swimming"])
def _(S):
    neck = thick("M8 14.5C4.5 12 4.5 7 8 5.8", 2.8, S)
    head = ellipse(9.5, 5.3, 2.4, 1.5)
    body = ellipse(14, 15.5, 6.5, 3.4)
    fl = [pg([(10, 17), (8.5, 21), (13, 19.3)], S), pg([(16, 17), (16, 21), (19.8, 19.3)], S)]
    tail = pg([(19, 14.5), (22.3, 13.3), (20.5, 17)], S)
    return [shell(union(neck, head, body, tail, *fl)), dot(10.2, 5, 0.6)]


@icon("pliosaur", CAT, "Swimming marine reptile with a short neck and a huge toothy long-jawed head",
      tags=["marine reptile", "sea monster", "predator", "teeth", "prehistoric", "jurassic", "swimming"])
def _(S):
    head = pg([(1.5, 10.5), (10, 9), (11, 14.5), (2, 14.8)], S)
    body = ellipse(15.5, 14, 6, 3.8)
    fl = [pg([(12, 16.5), (10.5, 21), (15, 19.5)], S), pg([(18, 16.5), (18.5, 21), (22, 19)], S)]
    tail = pg([(20, 13), (22.5, 11.3), (22.3, 15.5)], S, r=S.r / 2)
    return [shell(union(head, body, tail, *fl)), detail("M2 12.8L4.3 13.9L6.3 12.8L8.4 13.9L10.5 12.8"), dot(8, 10.8, 0.8)]


@icon("ichthyosaur", CAT, "Dolphin-shaped marine reptile with a long toothy snout, big eye, dorsal fin and crescent tail",
      tags=["marine reptile", "dolphin-like", "jurassic", "prehistoric", "swimming", "sea", "fossil"])
def _(S):
    body = ellipse(12, 12.5, 6.5, 3.8)
    snout = pg([(1.5, 11.6), (7.5, 10.4), (7.5, 14), (1.5, 12.8)], S, r=S.r / 2)
    fin = pg([(10.5, 9.5), (13.5, 4.8), (15.5, 10)], S, r=S.r / 2)
    flip_ = pg([(9.5, 15.3), (8.6, 19.5), (13, 16.3)], S, r=S.r / 2)
    tail = pg([(16.5, 12.5), (20, 7), (22, 8), (20, 12.5), (22, 17), (20, 18)], S, r=S.r)
    return [shell(union(body, snout, fin, flip_, tail)), dot(7.8, 11.4, 1)]


@icon("mosasaur", CAT, "Giant swimming sea lizard with a long crocodile-like head, flippers and a downturned tail fin",
      tags=["marine reptile", "sea lizard", "cretaceous", "prehistoric", "swimming", "sea monster", "fossil"])
def _(S):
    head = pg([(1.5, 10), (9.5, 8.8), (10, 13.2), (2, 12.6)], S)
    body = taper(((9, 11), (13, 13.5), (16.5, 12), (19, 12)), 5.5, 3)
    tail = pg([(17.5, 12), (20.5, 7), (22.2, 8), (20.6, 12.5), (22, 17.5), (20, 18)], S)
    fl = [pg([(11.5, 14), (10.5, 18), (14.5, 16)], S, r=S.r / 2)]
    return [shell(union(head, body, tail, *fl)), dot(7.5, 9.9, 0.7)]


@icon("dimetrodon", CAT, "Side view of a sprawling reptile with a tall fan-shaped sail of spines on its back",
      tags=["sail back", "synapsid", "permian", "prehistoric", "reptile", "fossil", "dinosaur-like"])
def _(S):
    sail = "M6.5 13C7 4.5 16.5 4 17.8 13Z"
    head = pg([(1.6, 12.5), (6.5, 11), (8.5, 14.5), (2, 15)], S)
    body = ellipse(12.5, 14.5, 6, 3)
    tail = taper(((17, 14.5), (19.5, 15.5), (21, 17), (22.3, 19.5)), 3.4, 1.2)
    legs = [pg([(8, 15.5), (11, 15.5), (9.6, 18.2), (10.8, 20.6), (7, 20.6), (7, 18.6)], S, r=S.r / 2),
            pg([(14, 15.5), (17.5, 15.5), (17.5, 18.2), (18.4, 20.6), (14.5, 20.6), (14.2, 18)], S, r=S.r / 2)]
    return [shell(union(sail, head, body, tail, *legs)), detail("M2.2 13.6H5.8"), dot(4.6, 12.6, 0.7)]


@icon("iguanodon", CAT, "Side view of a large plant-eating dinosaur standing half upright with a raised thumb spike",
      tags=["dinosaur", "thumb spike", "cretaceous", "prehistoric", "herbivore", "hadrosaur"])
def _(S):
    head = pg([(3, 5), (8, 4), (9.5, 7), (8, 9), (3.5, 8.5)], S)
    neck = thick("M8 7.5L11.5 11.5", 4, S)
    body = tilt(ellipse(13, 13.5, 5.5, 3.6), -35, 13, 13.5)
    tail = taper(((16, 15), (18.5, 16.5), (20.5, 18), (22.5, 19.5)), 4.6, 1.3)
    leg = pg([(11.5, 14), (16, 14), (15.5, 18.4), (17, 20.6), (10.5, 20.6), (10.5, 19.2), (12, 18.6)], S)
    arm = thick("M10.3 12.2L6.3 12.6", 2.4, S)
    spike = pg([(6.8, 12), (4.6, 9), (5.4, 13.2)], S, r=S.r / 2)
    return [shell(union(head, neck, body, tail, leg, arm, spike)), dot(6.5, 6, 0.8)]


@icon("carnotaurus", CAT, "Side view of a bipedal predator with two short thick horns above the eyes and stubby arms",
      tags=["dinosaur", "horned predator", "bull-like", "cretaceous", "prehistoric", "carnivore", "abelisaur"])
def _(S):
    head = pg([(3, 8.5), (9.5, 7.8), (11, 11), (10, 13.5), (3.6, 13.3)], S)
    horns = [pg([(5.8, 8.4), (5.2, 5), (7.8, 8)], S, r=S.r / 2), pg([(8.6, 8.2), (9, 4.8), (10.8, 8.4)], S, r=S.r / 2)]
    body = tilt(ellipse(14, 13, 5, 3.6), -20, 14, 13)
    tail = taper(((17, 12.5), (19.5, 13), (21, 15), (22.3, 17.5)), 4.4, 1.3)
    leg = pg([(12, 14), (16.5, 14), (16, 18.6), (17.4, 20.8), (11, 20.8), (11, 19.4), (12.4, 18.8)], S)
    return [shell(union(head, body, tail, leg, *horns)), detail(seg(3.2, 11.2, 7.5, 11.2)), dot(8.6, 9.8, 0.8)]


@icon("styracosaurus", CAT, "Side view of a horned dinosaur with a long nose horn and a frill crowned with long spikes",
      tags=["dinosaur", "horned", "spiked frill", "cretaceous", "prehistoric", "herbivore", "ceratops"])
def _(S):
    body = ellipse(14.8, 14.5, 5.8, 3.8)
    head = pg([(3.5, 15), (4.5, 12.6), (8.5, 11.6), (11, 12.6), (10.6, 16.6), (5.5, 17)], S)
    frill = circle(11, 10.6, 3)
    spikes = []
    for a in (-170, -135, -100, -65):
        tipx, tipy = 11 + 6.6 * math.cos(math.radians(a)), 10.6 + 6.6 * math.sin(math.radians(a))
        b1 = (11 + 2.3 * math.cos(math.radians(a - 20)), 10.6 + 2.3 * math.sin(math.radians(a - 20)))
        b2 = (11 + 2.3 * math.cos(math.radians(a + 20)), 10.6 + 2.3 * math.sin(math.radians(a + 20)))
        spikes.append(pg([b1, (tipx, tipy), b2], S, r=S.r / 2))
    nose = pg([(4.3, 13.4), (3, 6.8), (7.3, 12.2)], S, r=S.r / 2)
    legs = [rect(9.8, 17, 3, 3.6, rr(S)), rect(16.5, 17, 3, 3.6, rr(S))]
    tail = pg([(19.5, 13), (22.3, 15.6), (19.3, 16.6)], S)
    return [shell(union(body, head, frill, nose, tail, *spikes, *legs)), dot(7.4, 14.2, 0.8)]


@icon("protoceratops", CAT, "Side view of a small stocky dinosaur with a parrot-like beak and a plain wide neck frill",
      tags=["dinosaur", "frill", "beak", "cretaceous", "prehistoric", "herbivore", "small"])
def _(S):
    body = ellipse(14.5, 14.5, 6, 3.8)
    head = pg([(2, 15.8), (3.6, 12.2), (8, 11.4), (11, 12.6), (10.6, 17), (5, 17.2)], S)
    frill = ellipse(11, 11, 3.3, 4.2)
    beak = pg([(3.5, 12.6), (2, 15.4), (5.2, 14.2)], S, r=S.r / 2)
    legs = [rect(9.6, 17, 3, 3.6, rr(S)), rect(16.6, 17, 3, 3.6, rr(S))]
    tail = pg([(19.5, 13), (22.3, 16), (19.3, 16.8)], S)
    return [shell(union(body, head, frill, beak, tail, *legs)), dot(6.8, 14.3, 0.8)]


@icon("therizinosaurus", CAT, "Side view of a pot-bellied upright dinosaur with a small head and three very long scythe claws",
      tags=["dinosaur", "long claws", "scythe", "feathered", "cretaceous", "prehistoric", "herbivore"])
def _(S):
    head = pg([(3.5, 3.6), (8, 3.2), (8.6, 5.6), (4, 6)], S, r=S.r / 2)
    neck = thick("M7.5 5.2C9 7 10 8 11 9", 2.8, S)
    belly = ellipse(13, 13, 5.5, 5)
    tail = taper(((17, 15), (19, 17), (20.5, 18.5), (22.3, 19.5)), 4, 1.3)
    legs = [rect(10.5, 16.5, 3, 4.2, rr(S)), rect(15, 16.5, 3, 4.2, rr(S))]
    return [shell(union(head, neck, belly, tail, *legs)), line("M8.5 11L3.2 12.6"), line("M8.5 12.2L3.5 15.2"), line("M8.8 13.3L4.6 17.6"), dot(6.2, 4.7, 0.65)]


@icon("dilophosaurus", CAT, "Side view of a slender predator head and neck with two parallel half-moon crests on the skull",
      tags=["dinosaur", "crests", "crested", "jurassic", "prehistoric", "carnivore", "head"])
def _(S):
    head = pg([(1.6, 11), (8, 9.2), (14, 9.6), (15, 13), (8, 14), (2.2, 13.6)], S)
    crests = "M5 9.4C4.6 3.5 10 3 10 9.4Z M10 9.4C10 4 14.6 4.2 14.2 9.6Z"
    neck = pg([(12, 12), (16, 10.5), (21.5, 21), (13.5, 21)], S)
    return [shell(union(head, crests, neck)), detail(seg(2.4, 12.2, 7.5, 12.2)), dot(10, 11, 0.8)]


@icon("oviraptor", CAT, "Feathered beaked dinosaur sitting on a bowl-shaped nest of eggs with its arms spread over them",
      tags=["dinosaur", "nest", "eggs", "feathered", "cretaceous", "prehistoric", "parent"])
def _(S):
    bowl = "M3 14.6C3.5 21 20.5 21 21 14.6Z"
    body = ellipse(12.4, 12, 5, 3.4)
    neck = thick("M8 10.5C6.6 9 6.4 7.5 6.6 5.8", 2.8, S)
    head = pg([(2.8, 4.2), (7.5, 3.4), (8.5, 6), (3.6, 6.4)], S, r=S.r / 2)
    crest = pg([(6.4, 4), (7.3, 2.6), (8.6, 4.2)], S, r=S.r / 2)
    wing = pg([(14, 10), (20, 5.5), (21.4, 8.2), (16, 12.5)], S)
    return [shell(union(bowl, body, neck, head, crest, wing)), dot(9, 17.3, 1), dot(12.6, 18, 1), dot(16.2, 17.3, 1), dot(5.3, 5.1, 0.6)]


@icon("amargasaurus", CAT, "Side view of a small long-necked dinosaur with a double row of tall spines up the back of its neck",
      tags=["dinosaur", "sauropod", "spines", "neck spikes", "cretaceous", "prehistoric", "herbivore"])
def _(S):
    head = ellipse(4.6, 5.2, 2.4, 1.6)
    neck = thick("M6.5 6C9 7 10 9 10.5 12.5", 2.8, S)
    body = ellipse(14.5, 14.5, 6, 3.8)
    tail = taper(((19, 14.5), (20.5, 15.5), (21.5, 17.5), (22.3, 19.5)), 3.6, 1.2)
    legs = [rect(9.8, 16.8, 3, 3.8, rr(S)), rect(16.5, 16.8, 3, 3.8, rr(S))]
    spines = [pg([(7.7, 5.6), (8.8, 3.4), (10.2, 6.8)], S, r=S.r / 2), pg([(9.6, 7.2), (11.8, 4.6), (12.2, 9.2)], S, r=S.r / 2),
              pg([(10.6, 9.8), (13.4, 7.2), (13.6, 11.4)], S, r=S.r / 2)]
    return [shell(union(head, neck, body, tail, *spines, *legs)), dot(4.2, 4.9, 0.65)]


@icon("gallimimus", CAT, "Side view of an ostrich-like running dinosaur with a small beaked head, long neck and legs",
      tags=["dinosaur", "ostrich dinosaur", "running", "fast", "cretaceous", "prehistoric", "theropod"])
def _(S):
    head = pg([(1.8, 4.2), (6.4, 3.4), (6.8, 5.6), (2.4, 5.6)], S, r=S.r / 2)
    neck = thick("M6 5C8 7 7.6 9 9.5 10.6", 2.4, S)
    body = tilt(ellipse(13.5, 11.8, 5, 3), 12, 13.5, 11.8)
    tail = taper(((17.5, 11), (19.5, 10.6), (21, 10.2), (22.4, 10)), 3, 1.2)
    legs = [thick("M12 13.5L10.5 17.2L7.8 20.6", 2.2, S), thick("M15 13.5L17 17L15.2 20.6", 2.2, S)]
    return [shell(union(head, neck, body, tail, *legs)), dot(3.9, 4.4, 0.6)]


@icon("microraptor", CAT, "Small gliding dinosaur seen from above with feathered wings on arms and legs and a fan tail",
      tags=["dinosaur", "four wings", "gliding", "feathered", "cretaceous", "prehistoric", "glider"])
def _(S):
    up = pg([(10.5, 7.5), (2, 5.8), (3.4, 10.4), (10.5, 11)], S)
    lo = pg([(10.6, 13), (3.6, 14.4), (5.2, 19), (10.6, 17.4)], S)
    body = ellipse(12, 11.8, 1.9, 5.2)
    head = pg([(10.8, 7.2), (12, 3.6), (13.2, 7.2)], S, r=S.r / 2)
    fan = pg([(11, 16.5), (9.6, 22), (14.4, 22), (13, 16.5)], S, r=S.r / 2)
    return [shell(union(up, flip(up), lo, flip(lo), body, head, fan))]


@icon("kentrosaurus", CAT, "Side view of a four-legged dinosaur with short shoulder plates turning into long paired spikes down the back and tail",
      tags=["dinosaur", "spikes", "plates", "spiked", "jurassic", "prehistoric", "herbivore"])
def _(S):
    body = ellipse(12.5, 14.8, 6.5, 3.4)
    head = ellipse(3.8, 16.6, 2.2, 1.5)
    neck = pg([(4.5, 15.5), (7.8, 13), (8.3, 16.8), (5, 18)], S)
    plates = [pg([(8.2, 12.4), (9.4, 9.2), (10.9, 12.2)], S, r=S.r / 2), pg([(11.4, 11.8), (12.6, 8.4), (14.2, 12)], S, r=S.r / 2)]
    spikes = [pg([(15.2, 12.6), (16, 6), (17.2, 13)], S, r=S.r / 3), pg([(18, 13.6), (20.4, 8), (20.5, 14.6)], S, r=S.r / 3),
              pg([(19.2, 16), (21.7, 15.2), (20.6, 18.2)], S, r=S.r / 3)]
    tail = taper(((18, 15), (20, 15.4), (21.2, 16.2), (22, 17.2)), 3, 1.4)
    legs = [rect(8.3, 16.8, 2.6, 3.8, rr(S)), rect(15, 16.8, 2.6, 3.8, rr(S))]
    return [shell(union(body, head, neck, tail, *plates, *spikes, *legs)), dot(3.4, 16.3, 0.7)]


@icon("tanystropheus", CAT, "Side view of a small lizard body with a very long stiff neck longer than its body and tail combined",
      tags=["long neck", "reptile", "triassic", "prehistoric", "lizard", "giraffe-necked", "fossil"])
def _(S):
    head = pg([(1.8, 6), (6, 5.4), (6.4, 8.2), (2.4, 8.4)], S, r=S.r / 2)
    neck = thick("M5.8 7.3L14.5 14.4", 2.2, S)
    body = ellipse(17, 15.4, 4, 2.6)
    tail = taper(((20, 16), (21, 17), (21.6, 18.4), (22.3, 19.8)), 2.6, 1)
    legs = [rect(13.8, 16.6, 2.4, 3.8, rr(S, 0.4, 1)), rect(18.4, 16.8, 2.4, 3.6, rr(S, 0.4, 1))]
    return [shell(union(head, neck, body, tail, *legs)), dot(3.6, 6.6, 0.6)]


# --------------------------------------------------------------------------- ice age and ancient sea life

@icon("sabertooth-tiger", CAT, "Side view of a big cat head with an open jaw showing two very long downward saber canines",
      tags=["saber-toothed cat", "smilodon", "ice age", "prehistoric", "big cat", "fangs", "predator"])
def _(S):
    head = pg([(2.5, 10.5), (4, 7), (9, 4.8), (13, 5.5), (13.8, 2.3), (16.8, 6.5), (18, 9), (18, 20), (10.5, 20), (10.2, 17.2),
               (14, 14.6), (9.8, 12.6), (9.3, 16), (7.8, 12.4), (6.4, 17.6), (4.6, 11.8), (2.8, 11.6)], S, r=S.r / 2)
    return [shell(head), dot(12.6, 8.8, 1), dot(4.6, 9, 0.75)]


@icon("aurochs", CAT, "Side view of a wild ox with a heavy shoulder hump and long thick horns curving forward and up",
      tags=["wild ox", "wild cattle", "bull", "ice age", "prehistoric", "extinct", "horns"])
def _(S):
    body = ellipse(14, 13.5, 6.6, 4.2)
    hump = circle(10.5, 9.2, 3.2)
    head = pg([(2.5, 14), (4, 10.6), (8.5, 10.4), (10, 14.6), (5, 16.6)], S)
    horn = taper(((5, 10.6), (2.4, 8), (3, 4.6), (6.6, 3.2)), 2.8, 0.8, r=S.r / 3)
    legs = [rect(9.3, 16.5, 2.6, 4, rr(S)), rect(17, 16.5, 2.6, 4, rr(S))]
    tail = thick("M20 11.5L21.8 16", 1.6, S)
    return [shell(union(body, hump, head, horn, tail, *legs)), dot(6, 12.4, 0.8)]


@icon("terror-bird", CAT, "Side view of a tall flightless bird with tiny wings and an enormous deep hooked beak",
      tags=["phorusrhacid", "giant bird", "flightless", "prehistoric", "predator", "beak", "extinct"])
def _(S):
    head = circle(8.5, 6.5, 3.4)
    beak = pg([(6.6, 3.8), (1.5, 6.4), (2.6, 9.6), (6.6, 9.6)], S)
    neck = thick("M10.5 9C11.5 10.5 12 11 12.5 12", 3, S)
    body = ellipse(14.5, 13.3, 5.4, 3.6)
    tail = pg([(19, 11.5), (21.6, 12.6), (19.4, 15)], S, r=S.r / 2)
    legs = [thick("M13 16L12 20.5", 2.2, S), thick("M17 16L17.8 20.5", 2.2, S)]
    feet = [pg([(9.6, 20.6), (13.4, 20.6), (13.4, 21.6)], S, r=0.3)] if False else []
    return [shell(union(head, beak, neck, body, tail, *legs, *feet)), dot(9.2, 5.6, 0.8), line("M11 14.6L14.4 15.6")]


@icon("moa", CAT, "Side view of a very tall wingless bird with a long upright neck, small head and thick sturdy legs",
      tags=["giant bird", "flightless", "extinct", "new zealand", "prehistoric", "wingless", "ratite"])
def _(S):
    head = pg([(3.6, 2.6), (7.6, 2.4), (7.6, 4.6), (4.2, 4.8)], S, r=S.r / 2)
    neck = thick("M7 3.8C9.8 6 9 9 10.5 11", 2.4, S)
    body = ellipse(13, 14, 5.6, 4.2)
    legs = [rect(9.8, 17, 2.8, 4, rr(S)), rect(14.6, 17, 2.8, 4, rr(S))]
    tail = pg([(17.5, 12.2), (21.6, 13.6), (18.2, 15.6)], S, r=S.r / 2)
    return [shell(union(head, neck, body, tail, *legs)), dot(6, 3.4, 0.6)]


@icon("megalodon-jaw", CAT, "Front view of a giant open shark jaw, an oval ring lined with rows of triangular teeth",
      tags=["shark", "teeth", "jaws", "bite", "prehistoric", "giant shark", "predator"])
def _(S):
    outer = ellipse(12, 12, 9.5, 8.2)
    up = poly([(5.2, 9.2), (6.8, 12.6), (8.6, 9.2), (10.4, 12.6), (12.2, 9.2), (14, 12.6), (15.8, 9.2), (17.4, 12.6), (18.8, 9.2)], r=S.r / 2)
    lo = poly([(5.6, 15.6), (7.4, 12.4), (9.2, 15.6), (11, 12.4), (12.8, 15.6), (14.6, 12.4), (16.4, 15.6), (18.2, 12.4)], r=S.r / 2) if False else poly([(6.6, 15.4), (8.4, 12.6), (10.2, 15.4), (12, 12.6), (13.8, 15.4), (15.6, 12.6), (17.4, 15.4)], r=S.r / 2)
    return [shell(outer), detail(up), detail(lo)]


@icon("megalodon-tooth", CAT, "Single large triangular fossil shark tooth with a notched root at the base",
      tags=["shark tooth", "fossil", "megalodon", "prehistoric", "fang", "relic", "paleontology"])
def _(S):
    d = ("M12 3C13 8 17 12 20.6 16.6Q21.4 19.5 18.4 19.5H14.6Q12 15.8 9.4 19.5H5.6Q2.6 19.5 3.4 16.6C7 12 11 8 12 3Z")
    return [shell(d), detail("M7 14.6H17")]


@icon("dunkleosteus", CAT, "Side view of an armored prehistoric fish with a heavy plated head and sharp bony blade jaws open wide",
      tags=["armored fish", "placoderm", "prehistoric", "devonian", "jaws", "predator", "fossil"])
def _(S):
    head = ellipse(8.5, 12, 6.5, 6.4)
    notch = pg([(0.5, 12.2), (9.5, 9.6), (9.5, 14.6)], S, r=0)
    body = taper(((12, 12), (15.5, 12), (18.5, 12.4), (21, 12.4)), 8, 2.2)
    tail = pg([(19.5, 12.4), (22.4, 7.4), (22.4, 17.4)], S, r=S.r / 2)
    return [shell(union(minus(head, notch), body, tail)), detail("M10.5 6.6C13 9.4 13 14.6 10.5 17.4"), dot(7.6, 8.6, 0.9)]


@icon("stethacanthus", CAT, "Side view of an early shark with a flat brush-topped anvil-shaped fin sticking up from its back",
      tags=["prehistoric shark", "anvil fin", "carboniferous", "fossil", "ancient fish", "shark", "extinct"])
def _(S):
    body = ellipse(11.5, 15, 8.2, 3.3)
    snout = pg([(2, 15), (6, 12.5), (6, 17.5)], S, r=S.r / 2)
    anvil = pg([(7.2, 4.4), (17.2, 4.4), (17.2, 7.6), (13.4, 7.6), (13.4, 12), (10.8, 12), (10.8, 7.6), (7.2, 7.6)], S, r=S.r / 2)
    tail = pg([(17.5, 15), (21.6, 10), (20.6, 15), (21.6, 19.4)], S, r=S.r / 2)
    fin = pg([(9.6, 17.4), (8.8, 21), (13.4, 18.4)], S, r=S.r / 2)
    return [shell(union(body, snout, anvil, tail, fin)), dot(6.2, 14.2, 0.8)]


@icon("helicoprion", CAT, "Spiral whorl of triangular teeth coiled like a buzz saw blade",
      tags=["spiral teeth", "saw", "fossil", "prehistoric shark", "whorl", "paleontology", "buzz saw"])
def _(S):
    pts = []
    for i in range(14):
        r = 10 if i % 2 == 0 else L(S, 7.4, 7.9)
        a = -90 + i * 360 / 14
        pts.append((12 + r * math.cos(math.radians(a)), 12 + r * math.sin(math.radians(a))))
    return [shell(poly(pts, closed=True, r=S.r / 2)), detail("M11 12A1 1 0 0 1 13 12A2.5 2.5 0 0 1 8 12A4 4 0 0 1 16 12")]


@icon("coelacanth", CAT, "Side view of a heavy lobe-finned fish with fleshy limb-like fins and a three-lobed tail",
      tags=["lobe-finned fish", "living fossil", "ancient fish", "prehistoric", "sea", "lobefin", "fossil"])
def _(S):
    body = ellipse(11.5, 12, 8, 4.6)
    tail = pg([(17.5, 12), (21.2, 7.4), (21.2, 11), (22.3, 12), (21.2, 13), (21.2, 16.6)], S, r=S.r / 2)
    fins = [ellipse(9.4, 17.6, 1.6, 2.6), ellipse(15.6, 17.4, 1.5, 2.3), ellipse(13, 6.6, 2, 1.6)]
    return [shell(union(body, tail, *fins)), detail("M6.6 9.2C7.6 11 7.6 13 6.6 14.8"), dot(4.6, 11, 0.8)]


@icon("tiktaalik", CAT, "Side view of a flat-headed fish crawling onto land, propped up on two stubby limb-like front fins",
      tags=["transitional fossil", "fishapod", "evolution", "devonian", "amphibian ancestor", "prehistoric", "sarcopterygian"])
def _(S):
    head = pg([(1.8, 8.4), (9.8, 6.8), (10.8, 11), (2.6, 11.4)], S)
    body = taper(((9, 9.6), (14, 10.6), (18, 12.8), (22, 15.4)), 6, 1.6)
    limbs = [thick("M9.6 12L7.6 16.4L3.4 19.2", 2.4, S), thick("M15 13L15.6 17.6L19.6 20", 2.4, S)]
    return [shell(union(head, body, *limbs)), dot(6.2, 8.8, 0.8)]


@icon("ammonite", CAT, "Coiled spiral fossil shell with evenly spaced ribs around its edge, seen flat from the side",
      tags=["fossil", "shell", "spiral", "cephalopod", "prehistoric", "paleontology", "mollusc"])
def _(S):
    ticks = "".join(seg(12 + 6.3 * math.cos(math.radians(a)), 12 + 6.3 * math.sin(math.radians(a)),
                         12 + 9.6 * math.cos(math.radians(a)), 12 + 9.6 * math.sin(math.radians(a))) for a in range(20, 380, 45))
    return [shell(circle(12, 12, L(S, 9.4, 9.2))), detail(ticks), detail("M11 12A1.2 1.2 0 0 1 13.4 12A2.6 2.6 0 0 1 8.2 12A4 4 0 0 1 16.2 12")]


@icon("belemnite", CAT, "Bullet-shaped pointed fossil guard with a short cone at the wide end, lying at an angle",
      tags=["fossil", "cephalopod", "squid ancestor", "guard", "prehistoric", "paleontology", "thunderbolt"])
def _(S):
    body = "M12 2C15.2 7 15.8 12 14.8 16.6H9.2C8.2 12 8.8 7 12 2Z"
    cone = pg([(9.6, 16.4), (14.4, 16.4), (13.4, 21.4), (10.6, 21.4)], S, r=S.r / 2)
    return [shell(rot(union(body, cone), 40)), detail(rseg(12, 6.4, 12, 13.6, 40))]


@icon("orthoceras", CAT, "Long straight cone-shaped fossil shell with evenly spaced chamber lines across it",
      tags=["fossil", "cephalopod", "cone shell", "chambers", "prehistoric", "paleontology", "ordovician"])
def _(S):
    cone = pg([(7.5, 2), (16.5, 2), (12.9, 22), (11.1, 22)], S, r=S.r / 2)
    def ln(y):
        return rseg(7.5 + 0.18 * (y - 2), y, 16.5 - 0.18 * (y - 2), y, -38)
    return [shell(rot(cone, -38)), detail(ln(7.5) + ln(12.5) + ln(17.5))]


@icon("anomalocaris", CAT, "Top view of a flat swimming predator with side flaps along its body and two curled spiny grasping arms",
      tags=["cambrian", "prehistoric", "arthropod", "predator", "fossil", "ancient sea", "swimmer"])
def _(S):
    body = ellipse(12, 14, 2.6, 6.2)
    flaps = []
    for y in (11, 14.4, 17.6):
        f = pg([(10.2, y - 1.4), (3.6, y - 0.2), (10.2, y + 1.6)], S, r=S.r / 2)
        flaps += [f, flip(f)]
    tail = pg([(10.6, 19.4), (12, 21.6), (13.4, 19.4)], S, r=S.r / 2)
    arms = [thick("M10.8 8.2C9 7 8 5 9.2 3.2", 1.8, S), thick("M13.2 8.2C15 7 16 5 14.8 3.2", 1.8, S)]
    return [shell(union(body, tail, *flaps, *arms)), dot(11, 10.6, 0.6), dot(13, 10.6, 0.6)]


# --------------------------------------------------------------------------- early life, bones and fossils

@icon("opabinia", CAT, "Side view of a small segmented swimmer with stalked eyes on its head and a long flexible clawed nozzle in front",
      tags=["cambrian", "prehistoric", "arthropod", "five eyes", "fossil", "ancient sea", "burgess shale"])
def _(S):
    body = taper(((9, 13.5), (13, 13.5), (17, 13.4), (20, 13.4)), 6.4, 2.4)
    tail = pg([(18.5, 13.4), (22.4, 10.6), (22.4, 16.4)], S, r=S.r / 2)
    eyes = [circle(8.6, 8.4, 1.15), circle(11.4, 7.8, 1.15), circle(14.2, 8.4, 1.15)]
    nozzle = thick("M9.6 13.6C6 14.6 4 13 3.2 10", 2.2, S)
    claw = pg([(1.6, 11), (3.4, 8.4), (4.8, 11.2)], S, r=S.r / 3)
    return [shell(union(body, tail, nozzle, claw, *eyes)), detail("M12.4 10.8V16.2"), detail("M15.8 11.4V15.6")]


@icon("hallucigenia", CAT, "Side view of a tiny worm on paired thin legs with a row of long spikes pointing up from its back",
      tags=["cambrian", "prehistoric", "spiny worm", "fossil", "ancient sea", "burgess shale", "velvet worm"])
def _(S):
    body = thick("M6 13C10 12.2 15 12.2 20.5 13.6", 2.8, S)
    head = circle(5.4, 12.8, 2)
    spikes = seg(9, 11.8, 6.4, 4) + seg(13.4, 11.6, 13.4, 3.2) + seg(17.8, 12, 20.6, 4.8)
    legs = seg(9.6, 14.2, 8, 20.4) + seg(14, 14.4, 14, 20.8) + seg(18.4, 14.6, 20, 20.4)
    return [shell(union(body, head)), line(spikes), line(legs), dot(4.8, 12.4, 0.6)]


@icon("eurypterid", CAT, "Top view of a sea scorpion with a broad head, segmented tapering body, paddle legs and a spiked tail",
      tags=["sea scorpion", "arthropod", "paleozoic", "prehistoric", "fossil", "ancient sea", "predator"])
def _(S):
    head = ellipse(12, 7, 5, 3.4)
    body = pg([(8.4, 9), (15.6, 9), (13.4, 18.4), (10.6, 18.4)], S, r=S.r / 2)
    paddle = rot(ellipse(5.2, 12, 3.4, 1.3), 35, 5.2, 12)
    spike = pg([(11, 18), (12, 22.6), (13, 18)], S, r=S.r / 3)
    return [shell(union(head, body, spike, paddle, flip(paddle))), detail("M10 12.6H14"), detail("M10.6 15.4H13.4")]


@icon("arthropleura", CAT, "Top view of a giant flat millipede with broad segmented body plates and legs along both sides",
      tags=["giant millipede", "arthropod", "carboniferous", "prehistoric", "fossil", "centipede", "insect"])
def _(S):
    body = rect(3.5, 9, 17, 6, S.R / 2 if S.name != "line" else 1.2)
    legs = "".join(seg(x, 9, x - 0.8, 5.6) + seg(x, 15, x - 0.8, 18.4) for x in (7, 11, 15, 19))
    return [shell(body), detail("M8.4 9V15M12.2 9V15M16 9V15"), line(legs), line("M3.6 11C2.4 10 2.2 8 2.6 6.4M3.6 13C2.4 14 2.2 16 2.6 17.6")]


@icon("crinoid-fossil", CAT, "Sea lily fossil with a long beaded stalk topped by a cup and feathery branching arms",
      tags=["sea lily", "fossil", "echinoderm", "prehistoric", "ancient sea", "paleontology", "crinoid"])
def _(S):
    cup = pg([(8.8, 8.4), (15.2, 8.4), (13.4, 13), (10.6, 13)], S, r=S.r)
    arms = "".join(seg(12, 8, x, y) for x, y in ((5, 3.5), (8.6, 2.6), (12, 2.4), (15.4, 2.6), (19, 3.5)))
    beads = [dot(12, 15.8 + 2.7 * i, 1.35) for i in range(3)]
    return [shell(cup), line(arms), *beads, line("M12 13V21")]


@icon("dinosaur-skeleton", CAT, "Side view of a mounted bipedal dinosaur skeleton with a skull, ribcage, bony legs and a tapering tail",
      tags=["bones", "museum", "fossil", "paleontology", "prehistoric", "skeleton", "t-rex"])
def _(S):
    skull = pg([(2.2, 5), (8.6, 4), (9.4, 7.4), (3.2, 8.4)], S, r=S.r / 2)
    spine = line("M9 7.4C13 7.6 16 9.6 22 14.6")
    ribs = "M11.6 8.2C10.4 10.6 11.2 12.6 13 13.4M14.4 9.4C13.4 12 14.2 14 16 14.6"
    legs = "M12.6 13.4L11.6 17.6L8 20.4M16.8 13.4L16.6 17.6L13.6 20.6"
    return [shell(skull), spine, line(ribs), line(legs), line("M10 9.6L7.4 12.4"), dot(6.2, 5.9, 0.7)]


@icon("tyrannosaurus-skull", CAT, "Side view of a large predator skull with big openings, a deep jaw and long pointed teeth",
      tags=["skull", "t-rex skull", "bones", "fossil", "paleontology", "teeth", "dinosaur"])
def _(S):
    upper = pg([(2.5, 9), (5.5, 5.5), (14, 4.4), (20.5, 7), (21, 12.4), (16, 12.4), (15, 14.8), (13.3, 12.4), (8.6, 12.4), (7.6, 14.8),
                (6.2, 12.4), (3.4, 12.4)], S, r=S.r / 3)
    jaw = pg([(4, 17.6), (15.5, 16.8), (20.6, 13.6), (21, 19.2), (6, 20.4)], S, r=S.r / 3)
    return [shell(union(upper, jaw)), detail(ellipse(10.4, 8.6, 2.4, 1.4)), dot(16.4, 8.6, 1.5)]


@icon("triceratops-skull", CAT, "Front view of a horned skull with a broad scalloped frill, two long curving brow horns and a beak",
      tags=["skull", "horned skull", "bones", "fossil", "paleontology", "frill", "dinosaur"])
def _(S):
    frill = ellipse(12, 9, 8.6, 6.4)
    scallops = [circle(12 + 8.8 * math.cos(math.radians(a)), 9 + 6.6 * math.sin(math.radians(a)), L(S, 1.1, 1.4)) for a in range(-170, -5, 24)]
    face = pg([(8.8, 9.4), (15.2, 9.4), (15.6, 16), (13.4, 20.6), (10.6, 20.6), (8.4, 16)], S)
    horns = [taper(((8.8, 11.4), (5.4, 11.2), (2.8, 13.4), (2.2, 18)), 2.8, 0.8, r=S.r / 3),
             taper(((15.2, 11.4), (18.6, 11.2), (21.2, 13.4), (21.8, 18)), 2.8, 0.8, r=S.r / 3)]
    return [shell(union(frill, face, *scallops, *horns)), dot(10.6, 12.6, 0.85), dot(13.4, 12.6, 0.85), dot(12, 17.4, 0.7)]


@icon("dinosaur-eggs-nest", CAT, "Three oval eggs sitting together in a shallow bowl-shaped nest",
      tags=["eggs", "nest", "clutch", "fossil", "prehistoric", "hatching", "dinosaur"])
def _(S):
    bowl = "M2.8 15.4H21.2C20.4 21 15.6 21.6 12 21.6C8.4 21.6 3.6 21 2.8 15.4Z"
    eggs = [ellipse(6.6, 11.4, 2.5, 3.6), ellipse(12, 9.4, 2.5, 3.6), ellipse(17.4, 11.4, 2.5, 3.6)]
    shown = [minus(e, bowl) for e in eggs]
    return [shell(bowl)] + [shell(e) for e in shown] + [dot(12, 18.2, 0.8)]


@icon("dinosaur-hatchling", CAT, "Baby dinosaur head and neck poking out of a cracked egg with a jagged break line",
      tags=["baby dinosaur", "hatching", "egg", "cracked egg", "newborn", "prehistoric", "hatchling"])
def _(S):
    egg = poly([(4.8, 13.4), (8, 16), (10, 13), (14, 16), (16, 13), (19.2, 13.4), (19.6, 17.6), (16.4, 21.2), (7.6, 21.2), (4.4, 17.6)], closed=True, r=S.r)
    neck = thick("M12 14V9.4", 3, S)
    head = union(ellipse(12, 6.4, 3.8, 3.1), pg([(9, 4.8), (4.4, 6.8), (9, 8.8)], S, r=S.r / 2))
    return [shell(union(egg, neck, head)), dot(11.4, 5.6, 0.85)]


@icon("amber-fossil", CAT, "Rounded drop of amber with a small winged insect trapped inside it",
      tags=["amber", "resin", "insect", "trapped", "fossil", "prehistoric", "jurassic park"])
def _(S):
    d = ("M12 3.4C17 8 20.2 11.4 20.2 14.6A8.2 8.2 0 0 1 3.8 14.6C3.8 11.4 7 8 12 3.4Z" if S.name == "line"
         else "M12 4C16.4 8 20.2 11.4 20.2 14.6A8.2 8.2 0 0 1 3.8 14.6C3.8 11.4 7.6 8 12 4Z")
    wing = rot(ellipse(8.8, 11.6, 2.4, 1), -28, 8.8, 11.6)
    return [shell(d), mark(ellipse(12, 14.6, 1.2, 2.8)), mark(wing), mark(flip(wing)), mark(circle(12, 11.2, 1.2))]


@icon("fossil-shell", CAT, "Ribbed fan-shaped clam shell imprint set into a rough rounded rock",
      tags=["fossil", "shell", "scallop", "imprint", "rock", "paleontology", "clam"])
def _(S):
    rock = rect(2.5, 2.8, 19, 18.4, S.R)
    fan = "M12 18.4L6.2 11.2A7.6 5.6 0 0 1 17.8 11.2Z"
    return [shell(rock), shell(fan), detail("M12 18L9.2 10.6"), detail("M12 18L14.8 10.6")]


@icon("dinosaur-tooth", CAT, "Single long curved serrated predator tooth, pointed at the tip and wider at the root",
      tags=["tooth", "fang", "fossil", "predator", "serrated", "paleontology", "t-rex"])
def _(S):
    d = "M12 2.6C15.6 6 16.4 11 14.6 15.6L15.6 20.6H8.4L9.4 15.6C7.6 11 8.4 6 12 2.6Z"
    return [shell(d), detail("M9.2 15.8H14.8")]


@icon("dinosaur-claw", CAT, "Single large curved hooked claw with a bony base, like a raptor killing claw",
      tags=["claw", "talon", "fossil", "raptor", "sickle claw", "predator", "paleontology"])
def _(S):
    d = "M5.2 20.6C3.6 11 9.4 4 19.6 3.4C14.4 6 12.4 10.6 13.6 20.6Z"
    return [shell(d), detail("M4.6 17H13.6")]


@icon("fossil-dig", CAT, "Dinosaur bone lying in layered ground with horizontal strata lines",
      tags=["excavation", "archaeology", "paleontology", "bone", "dig site", "strata", "fossil hunting"])
def _(S):
    ground = rect(2.5, 12.8, 19, 8.8, S.R / 2)
    bone = union(rect(6.5, 5.4, 11, 2.6, 1), circle(6, 4.6, 1.7), circle(6, 8.8, 1.7), circle(18, 4.6, 1.7), circle(18, 8.8, 1.7))
    return [shell(ground), shell(bone), detail("M5 17.2H11M13.4 17.2H19")]


# --------------------------------------------------------------------------- stone age

@icon("mammoth-tusk", CAT, "Single long ivory tusk curving in a wide arc, broad at the base and tapering to a point",
      tags=["ivory", "mammoth", "ice age", "elephant", "prehistoric", "fossil", "tusk"])
def _(S):
    d = taper(((5.6, 20.6), (1.4, 12), (8.6, 3.4), (20.6, 6)), 6.2, 0.6, n=20, r=S.r / 3)
    return [shell(d), detail("M3.6 16.8H8.6")]


@icon("sabertooth-skull", CAT, "Side view of a cat skull with an open jaw and two very long downward saber canines",
      tags=["skull", "smilodon", "bones", "ice age", "fossil", "fangs", "prehistoric"])
def _(S):
    skull = pg([(2.5, 10), (4.5, 6.4), (11, 4.6), (18, 6.4), (21, 10.6), (21, 13), (14.2, 14.4), (10, 12.4), (9.4, 17.4),
                (7.6, 12.2), (5.6, 19.8), (4, 11.6), (2.8, 11.4)], S, r=S.r / 3)
    jaw = pg([(11.4, 18.4), (18, 14.8), (21, 15.6), (20.6, 20.4), (12, 20.6)], S, r=S.r / 3)
    return [shell(union(skull, jaw)), detail(circle(14.4, 9.4, 2.3)), dot(4.4, 9.2, 0.7)]


@icon("flint-hand-axe", CAT, "Teardrop-shaped knapped stone hand axe with chipped facets across its face",
      tags=["stone tool", "flint", "paleolithic", "prehistoric", "biface", "caveman", "knapping"])
def _(S):
    d = ("M12 2.4C17 8 19.8 13 18.4 17.6C17 21.6 7 21.6 5.6 17.6C4.2 13 7 8 12 2.4Z" if S.name == "line"
         else "M12 3C16.6 8.2 19.8 13 18.4 17.6C17 21.6 7 21.6 5.6 17.6C4.2 13 7.4 8.2 12 3Z")
    return [shell(d), detail("M12 6.4L8.8 12.4L11.4 16"), detail("M13 10.6L15.6 15")]


@icon("stone-age-club", CAT, "Wooden club with a rough stone head lashed to the top with crossed cord bindings",
      tags=["caveman", "cave man", "club", "weapon", "prehistoric", "stone age", "primitive"])
def _(S):
    handle = taper(((12, 21.6), (12, 17), (12, 13), (12, 9)), 2.6, 3.4, r=0)
    head = pg([(7.6, 9.8), (7, 5.6), (10, 2.4), (14.6, 2.6), (17, 6), (16.4, 9.8)], S)
    return [shell(rot(union(handle, head), 38)), detail(rseg(9.4, 9.6, 14.6, 12.2, 38) + rseg(14.6, 9.6, 9.4, 12.2, 38))]


@icon("stone-spear", CAT, "Long wooden spear shaft with a chipped stone point bound on with cord",
      tags=["spear", "hunting", "weapon", "caveman", "prehistoric", "stone age", "primitive"])
def _(S):
    point = pg([(12, 1.4), (15.4, 6), (12, 11), (8.6, 6)], S, r=S.r / 2)
    return [shell(rot(point, 45)), line(rseg(12, 10.6, 12, 22.4, 45)), detail(rseg(9.6, 9.6, 14.4, 11.6, 45) + rseg(14.4, 9.6, 9.6, 11.6, 45))]


@icon("dolmen", CAT, "Prehistoric tomb of two upright standing stones supporting a wide flat capstone",
      tags=["megalith", "tomb", "standing stones", "neolithic", "monument", "stone age", "ancient"])
def _(S):
    cap = pg([(2.5, 8.4), (21.5, 6), (21.5, 10.6), (2.5, 12.6)], S, r=S.r / 2)
    legs = [pg([(5, 12), (9.6, 11.4), (9.6, 21), (5, 21)], S, r=S.r / 2), pg([(14.4, 10.8), (19, 10.4), (19, 21), (14.4, 21)], S, r=S.r / 2)]
    return [shell(union(cap, *legs))]


@icon("stone-circle", CAT, "Ring of standing stones in perspective, three large ones in front and two smaller ones behind",
      tags=["megalith", "stonehenge", "standing stones", "neolithic", "monument", "henge", "ancient"])
def _(S):
    front = [rect(2.5, 12.8, 4, 8.6, rr(S, 0.8, 1.6)), rect(10, 13.8, 4, 7.6, rr(S, 0.8, 1.6)), rect(17.5, 12.8, 4, 8.6, rr(S, 0.8, 1.6))]
    back = [rect(6.6, 4.6, 3, 5.4, rr(S, 0.6, 1.2)), rect(14.4, 4.6, 3, 5.4, rr(S, 0.6, 1.2))]
    return [shell(f) for f in front + back]


@icon("petroglyph", CAT, "Rounded boulder with a carved spiral and a small stick figure etched into its face",
      tags=["rock art", "cave art", "carving", "prehistoric", "stone age", "glyph", "ancient"])
def _(S):
    rock = "M3 16.4C2 8.6 7 4 12 4C18 4 22 8 21 15.6C20.6 19 18 20.2 12 20.2C6 20.2 3.4 19.6 3 16.4Z"
    return [shell(rock), detail("M8.6 12.4A1 1 0 0 1 10.6 12.4A2.3 2.3 0 0 1 6 12.4"), dot(16.6, 8.6, 1.1),
            detail("M16.6 9.8V14.2"), detail("M14.4 11.4H18.8"), detail("M16.6 14.2L15.2 17M16.6 14.2L18 17")]


# --------------------------------------------------------------------------- myth and legend

@icon("griffin", CAT, "Side view of a creature with an eagle head, beak and wings on the front and a lion body and tufted tail behind",
      tags=["gryphon", "mythical creature", "eagle", "lion", "legend", "heraldry", "fantasy"], aliases=["gryphon"])
def _(S):
    head = circle(6.4, 6.4, 2.8)
    beak = pg([(4.2, 5), (1.6, 7.6), (4.6, 9)], S, r=S.r / 2)
    neck = thick("M7.6 8.6L10 12", 4, S)
    body = ellipse(14, 15, 6.4, 3.4)
    wing = pg([(10.4, 11.4), (11, 3.4), (16.4, 4.6), (21.4, 2.6), (19.6, 11.6)], S)
    legs = [rect(8.6, 16.8, 2.6, 4, rr(S)), rect(16.8, 16.8, 2.6, 4, rr(S))]
    tail = thick("M20 14.6C22 13.6 22 11.4 21 10.2", 1.6, S)
    tuft = circle(21, 10, 1.3)
    return [shell(union(head, beak, neck, body, wing, tail, tuft, *legs)), dot(6.2, 5.8, 0.7)]


@icon("pegasus", CAT, "Side view of a horse in a gallop with large feathered wings raised from its shoulders",
      tags=["winged horse", "mythical creature", "greek myth", "legend", "flying horse", "fantasy", "gallop"])
def _(S):
    body = ellipse(12.4, 13.6, 5.8, 2.9)
    neck = thick("M8.6 12L6.4 8", 4, S)
    head = pg([(2, 6.4), (5.6, 4.6), (8.4, 7), (7, 9.6), (3, 8.6)], S)
    legs = [thick("M8.4 15L4.4 18.6", 2, S), thick("M10.6 15.6L7.2 20.4", 2, S), thick("M15.6 15.4L19 19", 2, S), thick("M17.6 14.6L21.4 17.4", 2, S)]
    tail = taper(((17.6, 12.6), (20, 12.6), (21.4, 14), (22.2, 16.4)), 2.6, 1, r=0)
    wing = pg([(11.4, 11.4), (11.6, 3.2), (16.6, 4), (20.2, 2.6), (18, 11)], S)
    return [shell(union(body, neck, head, tail, wing, *legs)), dot(5.4, 6.4, 0.7)]


@icon("centaur", CAT, "Side view of a figure with a human torso and arms on a horse body with four legs, holding a bow",
      tags=["half horse", "mythical creature", "greek myth", "archer", "legend", "fantasy", "bow"])
def _(S):
    head = circle(9, 3.8, 1.9)
    torso = pg([(7.6, 6.2), (11, 6.2), (12, 12), (8, 12)], S, r=S.r / 2)
    horse = ellipse(15.2, 14, 5.6, 3)
    legs = [rect(10.8, 15.8, 2.2, 5, rr(S, 0.4, 1)), rect(13.8, 15.8, 2.2, 5, rr(S, 0.4, 1)), rect(17.4, 15.8, 2.2, 5, rr(S, 0.4, 1))]
    tail = taper(((20.2, 12.4), (21.8, 12.6), (22.4, 14), (22, 16.6)), 2.2, 1, r=0)
    return [shell(union(head, torso, horse, tail, *legs)), line("M2.6 3.4C0.8 7 0.8 11 2.6 14.6"), line("M2.8 3.6L2.8 14.4"), line("M10.4 8.4L3 9.2")]


@icon("minotaur", CAT, "Front view of a bull head with long curved horns and a nose ring on a broad human chest and shoulders",
      tags=["bull man", "labyrinth", "mythical creature", "greek myth", "legend", "fantasy", "maze"])
def _(S):
    head = pg([(8.6, 3.6), (15.4, 3.6), (15.8, 9), (14, 12.4), (10, 12.4), (8.2, 9)], S, r=S.r)
    horns = [taper(((8.6, 4.4), (4.4, 5), (2.6, 3), (3.2, 1.2)), 2.4, 0.8, r=0), taper(((15.4, 4.4), (19.6, 5), (21.4, 3), (20.8, 1.2)), 2.4, 0.8, r=0)]
    ears = [pg([(8.4, 6.2), (5.4, 6.8), (8.2, 8.8)], S, r=S.r / 3), pg([(15.6, 6.2), (18.6, 6.8), (15.8, 8.8)], S, r=S.r / 3)]
    chest = pg([(2.5, 21.5), (4, 15.6), (9.6, 13.4), (14.4, 13.4), (20, 15.6), (21.5, 21.5)], S, r=S.r / 2)
    return [shell(union(head, chest, *horns, *ears)), dot(10.4, 7.2, 0.8), dot(13.6, 7.2, 0.8), detail(circle(12, 10.6, 1.0))]


@icon("medusa", CAT, "Front view of a woman's face whose hair is a crown of writhing snakes with small heads",
      tags=["gorgon", "snake hair", "mythical creature", "greek myth", "legend", "fantasy", "snakes"])
def _(S):
    face = ellipse(12, 14, 5, 6)
    snakes = "M8.2 9.4C5.4 8.4 6 5.4 3.8 4.6M10.6 8.2C9 5.8 11 4.4 9.6 2.8M13.4 8.2C15 5.8 13 4.4 14.4 2.8M15.8 9.4C18.6 8.4 18 5.4 20.2 4.6M7.4 14C4.4 14.6 3.6 17.4 2.6 19M16.6 14C19.6 14.6 20.4 17.4 21.4 19"
    heads = [dot(3.6, 4.4, 1.3), dot(9.4, 2.6, 1.3), dot(14.6, 2.6, 1.3), dot(20.4, 4.4, 1.3), dot(2.4, 19.2, 1.3), dot(21.6, 19.2, 1.3)]
    return [shell(face), line(snakes), *heads, dot(10.2, 13, 0.8), dot(13.8, 13, 0.8), detail("M10.4 17.2H13.6")]


@icon("cyclops", CAT, "Front view of a giant head with a single large eye in the middle of the forehead and a heavy brow",
      tags=["one-eyed giant", "monster", "mythical creature", "greek myth", "legend", "fantasy", "giant"])
def _(S):
    head = ellipse(12, 12, 7.6, 9.4)
    ears = [ellipse(4.2, 12.4, 1.6, 2.4), ellipse(19.8, 12.4, 1.6, 2.4)]
    brow = "M6.6 7.4Q12 4.6 17.4 7.4"
    return [shell(union(head, *ears)), detail(ellipse(12, 10.4, 3.4, 2.3)), dot(12, 10.4, 1.1), line(brow), detail("M12 13.6V16.4H13.6"), detail("M8.8 18.8Q12 20 15.2 18.8")]


@icon("cerberus", CAT, "Front view of a dog body with three dog heads side by side on separate necks, wearing a spiked collar",
      tags=["three-headed dog", "hellhound", "underworld", "mythical creature", "greek myth", "legend", "fantasy"])
def _(S):
    def dog(cx, cy):
        return union(ellipse(cx, cy, 2.7, 2.9), pg([(cx - 2.6, cy - 1.4), (cx - 3.2, cy - 3.8), (cx - 0.8, cy - 2.6)], S, r=S.r / 3),
                     pg([(cx + 2.6, cy - 1.4), (cx + 3.2, cy - 3.8), (cx + 0.8, cy - 2.6)], S, r=S.r / 3), ellipse(cx, cy + 2.2, 1.5, 1.2))
    heads = [dog(5.6, 9.8), dog(12, 6.6), dog(18.4, 9.8)]
    body = pg([(2.8, 21.4), (4, 14.6), (8.4, 11), (15.6, 11), (20, 14.6), (21.2, 21.4)], S, r=S.r / 2)
    return [shell(union(*heads, body)), detail(poly([(5.6, 15.4), (7.6, 17.6), (9.6, 15.4), (11.6, 17.6), (13.6, 15.4), (15.6, 17.6), (17.6, 15.4)], r=0)), dot(11, 6, 0.6), dot(13, 6, 0.6)]


@icon("chimera", CAT, "Side view of a lion with a goat head rising from its back and a snake head as its tail",
      tags=["monster", "hybrid", "lion goat snake", "mythical creature", "greek myth", "legend", "fantasy"])
def _(S):
    mane = circle(5.6, 12.6, 3.8)
    body = ellipse(13, 15, 6.6, 3.4)
    legs = [rect(8.6, 17, 2.6, 4, rr(S)), rect(16.6, 17, 2.6, 4, rr(S))]
    neck = thick("M12.4 12.6L12.4 7.4", 2.6, S)
    goat = pg([(9, 3.4), (13.2, 2.4), (14.4, 5), (10.4, 6.6)], S, r=S.r / 2)
    horn = thick("M12.6 2.6C12 1.4 10.6 1.2 10 2", 1.2, S)
    tail = thick("M19 14.2C22 13.6 22.2 10.4 20.4 9", 1.6, S)
    snake = circle(20.2, 8.4, 1.5)
    return [shell(union(mane, body, neck, goat, tail, snake, *legs)), dot(4.6, 12, 0.7), dot(11.6, 4.2, 0.6)]


@icon("harpy", CAT, "Winged bird-woman with large spread wings and taloned feet, topped by a woman's head with long hair",
      tags=["bird woman", "monster", "mythical creature", "greek myth", "legend", "fantasy", "wings"])
def _(S):
    hair = pg([(8.6, 4.8), (12, 1.8), (15.4, 4.8), (16.2, 10), (14.4, 8.6), (9.6, 8.6), (7.8, 10)], S, r=S.r / 2)
    wing = pg([(10, 10.4), (2, 4.6), (2.8, 10.2), (5.6, 11.2), (5.4, 15.4), (10.4, 15)], S)
    body = ellipse(12, 14, 2.6, 5)
    talons = [seg(10.6, 18.6, 9.4, 21.6), seg(13.4, 18.6, 14.6, 21.6)]
    return [shell(union(hair, body, wing, flip(wing))), *[line(t) for t in talons], dot(11, 6.4, 0.6), dot(13, 6.4, 0.6)]


@icon("satyr", CAT, "Figure with small curled horns, a pointed beard and goat legs with hooves, holding pan pipes",
      tags=["faun", "pan", "pan pipes", "mythical creature", "greek myth", "legend", "fantasy"])
def _(S):
    head = pg([(9.2, 4.2), (14.8, 4.2), (14.4, 8), (12, 10.6), (9.6, 8)], S, r=S.r)
    horns = "M9.4 4.4C8 3.6 7.4 2.4 8 1.6M14.6 4.4C16 3.6 16.6 2.4 16 1.6"
    torso = pg([(8, 11), (16, 11), (15, 15.4), (9, 15.4)], S, r=S.r / 2)
    legs = [pg([(9, 15), (12, 15), (10.8, 18.2), (12, 21.4), (8.6, 21.4), (9.2, 18.4)], S, r=S.r / 3), pg([(12, 15), (15, 15), (15, 18.4), (16, 21.4), (12.6, 21.4), (13.4, 18.2)], S, r=S.r / 3)]
    pipes = union(rect(17, 9, 1.8, 6, 0.4), rect(19.5, 9, 1.8, 4.4, 0.4))
    return [shell(union(head, torso, *legs)), line(horns), shell(pipes), dot(10.8, 6.4, 0.6), dot(13.2, 6.4, 0.6), line("M15.6 12.4L17.4 12.6")]


@icon("sphinx", CAT, "Side view of a reclining lion body with a human head wearing a striped headdress",
      tags=["egypt", "egyptian", "riddle", "mythical creature", "legend", "monument", "fantasy"])
def _(S):
    nemes = pg([(3.6, 4.4), (9.4, 4.4), (11.6, 12), (2.8, 12)], S, r=S.r / 2)
    face = ellipse(4.6, 8.4, 2, 3)
    body = pg([(10, 12), (18, 12), (21.6, 15), (21.6, 19.6), (2.4, 19.6), (2.4, 16.6), (10, 16.6)], S, r=S.r / 2)
    return [shell(union(nemes, face, body)), detail("M6.8 6.8L9 9.4"), dot(4.2, 8, 0.6)]


@icon("hippocampus", CAT, "Side view of a sea-horse creature with a horse head, front legs and mane joined to a curling fish tail",
      tags=["sea horse", "seahorse", "mythical creature", "greek myth", "legend", "fantasy", "sea"])
def _(S):
    head = pg([(2, 5), (7.6, 2.8), (10.4, 5.6), (8.2, 8.4), (3, 7)], S)
    body = taper(((8.4, 6), (6.4, 13), (11, 20.6), (18, 19)), 5, 2, n=18, r=0)
    curl = thick("M18 19C21.6 17.6 21 13.6 17.6 14", 2, S)
    mane = [pg([(10.2, 5.2), (13.4, 4.2), (11.6, 8)], S, r=S.r / 3), pg([(9.6, 9.4), (13, 9.2), (10.4, 12.6)], S, r=S.r / 3)]
    legs = thick("M7.4 11.6L3.4 14.6", 1.8, S)
    return [shell(union(head, body, curl, legs, *mane)), dot(6, 5.2, 0.7)]
