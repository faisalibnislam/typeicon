"""TypeIcon Core: wellness (batch 004): exercise moves, body and mind concepts, support gear.

Figures follow wellness_002: a solid head (r 2.25) over 2 px limbs, faceted in Line and filleted in Rounded
(poly with r=S.r). Small marks (weights, drops, hearts) are solid parts so Filled knocks them out or keeps them.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import P, fmt, path_to_d, transform_path

CAT = "wellness"


def pl(S, pts):
    return line(poly(pts, r=S.r))


def hd(x, y):
    return dot(x, y, 2.25)


def figure(S, h, *limbs):
    return [hd(*h)] + [pl(S, p) for p in limbs]


def sq(x, y, w, h):
    return Part("dot", rect(x, y, w, h))


def xf(d, k, dx, dy):
    return path_to_d(transform_path(P(d), (k, 0, 0, k, dx, dy)))


HEART = "M12 20L4.4 12.6A4.6 4.6 0 0 1 11 6.3L12 7.3L13 6.3A4.6 4.6 0 0 1 19.6 12.6Z"


def heart_d(cx, cy, w):
    k = w / 16.0
    return xf(HEART, k, cx - 12 * k, cy - 13 * k)


def drop_d(cx, cy, r):
    """Teardrop whose round belly is centred on (cx, cy) with radius r and whose tip is 2.2 r above."""
    t = cy - 2.3 * r
    dx = r * 0.85
    return (f"M{fmt(cx)} {fmt(t)}L{fmt(cx + dx)} {fmt(cy - r * 0.5)}A{fmt(r)} {fmt(r)} 0 1 1 {fmt(cx - dx)} {fmt(cy - r * 0.5)}Z")


def star_d(cx, cy, r):
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return poly(pts, closed=True)


# =========================================================================== chunk 1

@icon("vision-board", CAT, "A pinboard with pinned photos, a star and a heart arranged in a collage.",
      tags=["vision board", "goals", "manifest", "collage", "dream board", "inspiration"])
def _(S):
    return [shell(rect(3, 4, 18, 17, S.R)),
            Part("dot", rect(6.5, 7.5, 5.5, 4.5)),
            Part("dot", star_d(16.5, 10.2, 3.3)),
            Part("dot", heart_d(9.5, 16.8, 6)),
            Part("dot", rect(14, 15, 4.5, 3.5)),
            line(seg(12, 2, 12, 4))]


@icon("good-posture", CAT, "Side view of an upright figure standing straight beside a vertical alignment line.",
      tags=["posture", "spine", "straight back", "alignment", "ergonomics", "back health"])
def _(S):
    return [hd(9.5, 4.5), line(seg(9.5, 8.5, 9.5, 15)), pl(S, [(9.5, 15), (9.5, 21.5)]),
            pl(S, [(9.5, 10), (13, 14.5)]),
            line(seg(18, 3, 18, 21.5)), line(seg(16, 3, 20, 3)), line(seg(16, 21.5, 20, 21.5))]


@icon("six-pack-abs", CAT, "Front view of a bare torso with six blocks of abdominal muscle.",
      tags=["abs", "abdominals", "core", "six pack", "stomach muscles", "fitness", "torso"])
def _(S):
    blocks = [Part("dot", rect(x, y, 4.5, 4, 0.8)) for y in (5.5, 11, 16.5) for x in (6.5, 13)]
    return [shell(poly([(7.5, 2.5), (16.5, 2.5), (20, 6), (17.5, 21.5), (6.5, 21.5), (4, 6)], closed=True, r=S.r))] + blocks


@icon("sweat-drops", CAT, "A forehead with a brow and three sweat drops falling from it.",
      tags=["sweat", "perspiration", "workout", "hot", "effort", "forehead", "sweating"])
def _(S):
    return [shell(circle(10, 13.5, 7.5)), dot(7, 12.5, 1.1), dot(13, 12.5, 1.1), line(seg(7.5, 17, 12.5, 17)),
            solid(drop_d(19.5, 7, 1.8)), solid(drop_d(21, 12.5, 1.5)), solid(drop_d(19, 18, 1.8))]


@icon("weight-loss", CAT, "A figure pulling out the waistband of trousers that have become too large.",
      tags=["weight loss", "slimming", "diet", "baggy trousers", "lose weight", "waist", "progress"])
def _(S):
    return [hd(12, 4.5), line(seg(12, 8.5, 12, 13)), pl(S, [(12, 9.5), (6, 9.5), (3.5, 13.5)]),
            pl(S, [(12, 9.5), (18, 9.5), (20.5, 13.5)]),
            shell(poly([(6.5, 13), (17.5, 13), (21, 21.5), (13, 21.5), (12, 17.5), (11, 21.5), (3, 21.5)], closed=True, r=S.r))]


@icon("heart-rate-zone", CAT, "A five-segment gauge with a needle and a heart underneath, showing training intensity zones.",
      tags=["heart rate", "zones", "cardio", "intensity", "bpm", "training zone", "pulse"])
def _(S):
    parts = [line(arc(12, 16, 9.5, 180 + i * 36 + 7, 180 + (i + 1) * 36 - 7)) for i in range(5)]
    parts.append(pl(S, [(12, 14), (16.5, 8.5)]))
    parts.append(solid(heart_d(12, 20, 6)))
    return parts


@icon("rest-day", CAT, "A calendar page with a small bed drawn on it.",
      tags=["rest day", "recovery", "day off", "sleep", "schedule", "training plan", "calendar"])
def _(S):
    return [shell(rect(3, 4, 18, 17, S.R)), detail(seg(3, 9, 21, 9)),
            line(seg(8, 2, 8, 6)), line(seg(16, 2, 16, 6)),
            pl(S, [(7, 12.5), (7, 18)]), pl(S, [(7, 16), (17, 16), (17, 18)]), dot(9.5, 13.8, 1.1)]


@icon("yoga-mat", CAT, "A yoga mat with one end rolled into a thick spiral and the rest laid flat.",
      tags=["yoga mat", "exercise mat", "pilates", "stretching", "floor", "rolled mat"])
def _(S):
    return [shell(circle(16.5, 13.5, 5.5)), detail(arc(16.5, 13.5, 2, 0, 270)),
            pl(S, [(11.4, 15.5), (2.5, 15.5), (2.5, 19), (16.5, 19)])]


@icon("bird-dog", CAT, "Side view of a figure on hands and knees with one arm and the opposite leg stretched out.",
      tags=["bird dog", "quadruped", "core stability", "back exercise", "balance", "workout"])
def _(S):
    return figure(S, (19.5, 13.5), [(7.5, 12), (14.5, 12)], [(14.5, 12), (22, 7.5)], [(14.5, 12), (14.5, 21.5)],
                  [(7.5, 12), (2, 8.5)], [(7.5, 12), (7.5, 19.5), (4, 21.5)])


@icon("donkey-kick", CAT, "Side view of a figure on hands and knees kicking one bent leg up with the sole facing the ceiling.",
      tags=["donkey kick", "glutes", "quadruped", "booty workout", "leg raise", "floor exercise"])
def _(S):
    return figure(S, (19.5, 10.5), [(8, 11), (15, 10)], [(15, 10), (15, 21.5)],
                  [(8, 11), (3, 8.5), (7, 3.5)], [(8, 11), (9, 18.5), (5, 21)]) + [line(seg(2, 21.5, 22, 21.5))]


@icon("lateral-raise", CAT, "Front view of a standing figure holding a dumbbell in each hand with the arms out to shoulder height.",
      tags=["lateral raise", "side raise", "shoulders", "dumbbell", "delts", "weights", "gym"])
def _(S):
    return [hd(12, 4.5), line(seg(12, 8.5, 12, 15)), pl(S, [(9, 21.5), (12, 15), (15, 21.5)]),
            line(seg(3.5, 9.5, 20.5, 9.5)), sq(2, 7, 2.5, 5), sq(19.5, 7, 2.5, 5)]


@icon("dumbbell-row", CAT, "Side view of a figure with one hand and knee on a bench pulling a dumbbell up toward the hip.",
      tags=["dumbbell row", "one arm row", "back workout", "bench", "lats", "weights", "gym"])
def _(S):
    return [hd(4.5, 6.5), pl(S, [(7, 9), (16.5, 10.5)]), pl(S, [(8.5, 9.2), (7, 19)]),
            pl(S, [(11, 9.5), (14, 12.5), (14, 16)]), sq(12, 15.5, 4, 2),
            line(seg(3, 19, 17, 19)),
            pl(S, [(16.5, 10.5), (20.5, 15), (20.5, 21.5)]), pl(S, [(16.5, 10.5), (14.8, 19)])]

# =========================================================================== chunk 2

@icon("shadow-boxing", CAT, "Side view of a figure in a fighting stance throwing a straight punch with the other fist at the chin.",
      tags=["shadow boxing", "boxing", "punch", "martial arts", "cardio", "fight stance", "workout"])
def _(S):
    return [hd(9.5, 4.5), line(seg(9, 8.5, 9, 14)), pl(S, [(9, 14), (13.5, 17.5), (15, 21.5)]),
            pl(S, [(9, 14), (5, 17.5), (3.5, 21.5)]),
            pl(S, [(10, 10), (19, 9.5)]), solid(circle(20, 9.5, 2)),
            pl(S, [(9, 10.5), (6.5, 13.5), (10.5, 8.5)])]


@icon("chair-yoga", CAT, "Side view of a figure seated on a chair leaning into a side stretch with one arm arched overhead.",
      tags=["chair yoga", "seated yoga", "desk stretch", "gentle yoga", "side stretch", "mobility", "seniors"])
def _(S):
    return [hd(14, 9), pl(S, [(9, 14.5), (10.5, 10)]), pl(S, [(10.5, 10.5), (10.5, 2.5), (19, 4.5)]),
            pl(S, [(9, 14.5), (16, 14.5), (17, 21.5)]),
            pl(S, [(3.5, 8), (3.5, 16.5), (15, 16.5)]), line(seg(3.5, 16.5, 3.5, 21.5)), line(seg(14, 16.5, 14, 21.5))]


@icon("knee-sleeve", CAT, "A leg from thigh to shin with a ribbed support sleeve fitted over the knee.",
      tags=["knee sleeve", "knee brace", "support", "compression", "joint support", "injury", "squat"])
def _(S):
    return [line(poly([(7, 2.5), (7.5, 9)])), line(poly([(17, 2.5), (16.5, 9)])),
            line(poly([(8, 15), (9, 21.5)])), line(poly([(16, 15), (15, 21.5)])),
            shell(rect(5.5, 9, 13, 6, min(S.R, 2))), detail(seg(9.5, 9, 9.5, 15)), detail(seg(14.5, 9, 14.5, 15))]


@icon("hand-wraps", CAT, "A hand with a strip of cloth wound around the knuckles and palm and the loose end trailing.",
      tags=["hand wraps", "boxing wraps", "knuckle protection", "mma", "wrist support", "training gear"])
def _(S):
    return [shell(rect(4, 3, 13, 18, S.R)), detail(seg(8.3, 3, 8.3, 8)), detail(seg(12.7, 3, 12.7, 8)),
            detail(seg(4, 15, 17, 11.5)), detail(seg(4, 19.5, 17, 16)),
            line(poly([(17, 17.5), (21, 17.5), (20.5, 21.5)], r=S.r))]


@icon("effervescent-tablet", CAT, "A glass of water with a round tablet sinking in it and bubbles rising.",
      tags=["effervescent tablet", "fizzy", "vitamin tablet", "dissolve", "supplement", "electrolytes", "glass of water"])
def _(S):
    return [shell(poly([(5, 4.5), (19, 4.5), (17.5, 21.5), (6.5, 21.5)], closed=True, r=S.r)),
            Part("dot", circle(12, 17, 2.2)), dot(9.2, 12.5, 1.1), dot(14.5, 11.5, 1.1), dot(12, 8, 1)]


@icon("loneliness", CAT, "A single small figure sitting alone on a bench under a crescent moon.",
      tags=["loneliness", "lonely", "alone", "isolation", "solitude", "sad", "mental health"])
def _(S):
    moon = path_to_d(__import__("geometry").D(P(circle(18, 6.5, 4.2)), P(circle(20, 5.3, 3.5))))
    return [solid(moon), hd(8.5, 8), line(seg(8.5, 11.5, 8.5, 16.5)), pl(S, [(8.5, 16.5), (13, 16.5), (13, 21.5)]),
            line(seg(2.5, 18, 17, 18)), line(seg(4, 18, 4, 21.5)), line(seg(15.5, 18, 15.5, 21.5))]


@icon("resilience", CAT, "A small plant with two leaves growing up through a crack in a paving slab.",
      tags=["resilience", "perseverance", "grit", "growth", "bounce back", "strength", "sprout"])
def _(S):
    leaf_l = "M12 12C7 12 5 9.5 5 6.5C9 6.5 12 8 12 12Z"
    leaf_r = "M12 12C17 12 19 9.5 19 6.5C15 6.5 12 8 12 12Z"
    return [shell(leaf_l), shell(leaf_r), line(seg(12, 12, 12, 17.5)),
            pl(S, [(2, 17), (8, 17), (9.5, 19.5), (8, 21.5)]), pl(S, [(22, 17), (16, 17), (14.5, 19.5), (16, 21.5)])]


def head_d(S, k=1.0, dx=0.0, dy=0.0):
    d = ("M8 21V17.2C5.6 15.8 4 13.3 4 10.5C4 6.4 7.6 3 12 3C16.1 3 19 5.9 19 9.5L20.5 12.8L19 13.3V15.5C19 16.6 18.1 17.5 17 17.5H14V21Z"
         if S.name == "line" else
         "M8 20V17.2C5.6 15.8 4 13.3 4 10.5C4 6.4 7.6 3 12 3C16.1 3 19 5.9 19 9.5L20.2 12Q20.6 12.9 19.7 13.1L19 13.3V15.5C19 16.6 18.1 17.5 17 17.5H14V20C14 20.6 13.6 21 13 21H9C8.4 21 8 20.6 8 20Z")
    return xf(d, k, dx, dy) if k != 1.0 or dx or dy else d


@icon("positive-thinking", CAT, "A head in profile with a small sun with rays glowing inside it.",
      tags=["positive thinking", "optimism", "good vibes", "mindset", "happy thoughts", "bright side", "mental health"])
def _(S):
    rays = [detail(seg(11.5 + 3.3 * math.cos(math.radians(a)), 10.2 + 3.3 * math.sin(math.radians(a)),
                       11.5 + 4.7 * math.cos(math.radians(a)), 10.2 + 4.7 * math.sin(math.radians(a)))) for a in range(0, 360, 45)]
    return [shell(head_d(S)), dot(11.5, 10.2, 1.7)] + rays


@icon("mental-load", CAT, "A head in profile balancing a stack of boxes on top.",
      tags=["mental load", "overwhelmed", "burden", "stress", "workload", "overthinking", "burnout"])
def _(S):
    return [shell(head_d(S, 0.55, 5.8, 9.75)),
            Part("dot", rect(8, 7.2, 8, 3.2, 0.6)), Part("dot", rect(6.5, 3.6, 5, 3, 0.6)), Part("dot", rect(12.2, 3.6, 5.3, 3, 0.6)),
            Part("dot", rect(8.5, 0.3, 7, 2.6, 0.6))]


@icon("personal-boundaries", CAT, "A figure standing inside a circle with one palm raised outward at its edge.",
      tags=["personal boundaries", "personal space", "say no", "limits", "consent", "self care", "stop"])
def _(S):
    return [line(circle(9, 12, 8)), hd(9, 8.3), line(seg(9, 11, 9, 15.5)),
            pl(S, [(9, 15.5), (7, 19)]), pl(S, [(9, 15.5), (11, 19)]),
            pl(S, [(9, 11.5), (19.5, 11.5)]), line(seg(20.5, 7.5, 20.5, 14.5))]


@icon("mudra-hand", CAT, "A hand held palm up with the thumb and index finger touching in a ring and the other fingers extended.",
      tags=["mudra", "gyan mudra", "meditation hand", "hand gesture", "yoga", "chin mudra", "zen"])
def _(S):
    return [shell(circle(6.3, 12.3, 2.7)), shell(rect(9, 14, 12, 7.5, min(S.R, 2))),
            line(seg(12, 14, 12, 5)), line(seg(15.5, 14, 15.5, 3.5)), line(seg(19, 14, 19, 6))]


@icon("meditation-labyrinth", CAT, "A round labyrinth of concentric paths winding in toward a centre point.",
      tags=["labyrinth", "maze walk", "walking meditation", "mindfulness", "path", "journey inward", "spiritual"])
def _(S):
    return [line(arc(12, 12, 9, 25, 335)), line(arc(12, 12, 5.5, 205, 515)), dot(12, 12, 1.5)]


@icon("skincare-routine", CAT, "Three skincare containers side by side: a dropper bottle, a pump bottle and a short jar.",
      tags=["skincare", "routine", "serum", "moisturizer", "beauty", "self care", "lotion"])
def _(S):
    return [shell(rect(3, 10, 3.6, 11.5, min(S.R, 1.5))), line(seg(4.8, 3.5, 4.8, 7.5)),
            shell(rect(10, 11, 3.6, 10.5, min(S.R, 1.5))), pl(S, [(11.8, 11), (11.8, 5), (9.5, 5)]),
            shell(rect(17, 13.5, 4.5, 8, min(S.R, 1.5))), line(seg(17, 11.5, 21.5, 11.5))]