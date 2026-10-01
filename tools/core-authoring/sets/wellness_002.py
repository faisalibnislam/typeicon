"""TypeIcon Core: wellness (batch 002): exercise moves, yoga poses, yoga props and heat/cold therapy.

Figures follow the people and sports sets: a solid head (r 2.25) over 2 px limbs, faceted in Line and filleted in
Rounded (poly with r=S.r). Each pose is a small stick figure, with the floor, bar, bench or box drawn only where
the move needs it to be recognised.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401

CAT = "wellness"


def pl(S, pts):
    return line(poly(pts, r=S.r))


def hd(x, y):
    return dot(x, y, 2.25)


def figure(S, h, *limbs):
    return [hd(*h)] + [pl(S, p) for p in limbs]


def sq(x, y, w, h):
    return Part("dot", rect(x, y, w, h))


# =========================================================================== exercise moves

@icon("lunge", CAT, "Side view of a figure with the front knee bent at a right angle and the back knee near the floor.",
      tags=["lunge", "leg day", "workout", "exercise", "legs", "fitness"], aliases=["lunges"])
def _(S):
    return figure(S, (10, 4.5), [(10, 9), (10, 14)], [(10, 14), (15, 14), (15, 21.5)],
                  [(10, 14), (7, 20), (3, 18)], [(10, 10), (6, 12)])


@icon("mountain-climbers", CAT, "Side view of a figure in a plank driving one knee toward the chest.",
      tags=["mountain climber", "plank", "core", "cardio", "workout", "hiit"], aliases=["mountain-climber"])
def _(S):
    return figure(S, (19, 6), [(17, 10.5), (7, 14.5), (3, 21.5)], [(17, 10.5), (18.5, 21)],
                  [(7, 14.5), (13, 17), (9, 19.5)])


@icon("pull-up", CAT, "Front view of a figure hanging from a bar with the chin above it and the elbows bent.",
      tags=["pull-up", "chin-up", "bar", "calisthenics", "upper body", "workout"], aliases=["chin-up"])
def _(S):
    return [hd(12, 4.5), line(seg(3, 9, 21, 9)), pl(S, [(5.5, 9), (7, 14), (10.5, 12)]), pl(S, [(18.5, 9), (17, 14), (13.5, 12)]),
            line(seg(12, 12, 12, 16.5)), pl(S, [(9.5, 21.5), (12, 16.5), (14.5, 21.5)])]


@icon("tricep-dips", CAT, "Side view of a figure with the hands on a bench behind, lowering the hips with the legs out in front.",
      tags=["tricep dips", "bench dips", "triceps", "arms", "workout", "calisthenics"], aliases=["bench-dips"])
def _(S):
    return [line(seg(2, 12, 9, 12)), line(seg(4, 12, 4, 21.5)),
            hd(13, 5.5), pl(S, [(12.5, 9.5), (11.5, 16.5), (21, 19)]), pl(S, [(12.5, 9.5), (8, 12)])]


@icon("deadlift", CAT, "Side view of a figure bent at the hips gripping a loaded barbell near the shins.",
      tags=["deadlift", "barbell", "powerlifting", "weights", "strength", "gym"], aliases=["deadlifts"])
def _(S):
    return [hd(16.5, 5.5), pl(S, [(4, 12), (13, 9)]), pl(S, [(4, 12), (8.5, 16.5), (8, 21.5)]),
            pl(S, [(13, 9.5), (15.5, 14.5)]), shell(circle(15.5, 18.5, 4))]


@icon("bench-press", CAT, "Side view of a figure lying on a bench pressing a barbell up above the chest.",
      tags=["bench press", "chest", "barbell", "weights", "strength", "gym"], aliases=["bench-presses"])
def _(S):
    return [hd(4.5, 12), pl(S, [(8, 14), (15, 14), (19.5, 16.5), (19, 21.5)]), line(seg(3, 17, 16, 17)),
            line(seg(5, 17, 5, 21.5)), line(seg(14, 17, 14, 21.5)),
            pl(S, [(9, 14), (9, 9.5)]), shell(circle(9, 6, 3.5))]


@icon("bicep-curl", CAT, "Front view of a standing figure curling a dumbbell up toward the shoulder.",
      tags=["bicep curl", "biceps", "dumbbell", "arms", "weights", "gym"], aliases=["biceps-curl"])
def _(S):
    return [hd(10, 4.5), line(seg(10, 8.5, 10, 14.5)), pl(S, [(7, 21.5), (10, 14.5), (13, 21.5)]),
            pl(S, [(10, 9.5), (6, 15)]), pl(S, [(10, 9.5), (14.5, 14), (16.5, 9.5)]),
            line(seg(14.5, 8, 20.5, 8)), sq(13.5, 6, 2, 4), sq(19.5, 6, 2, 4)]


@icon("kettlebell-swing", CAT, "Side view of a figure with the hips forward swinging a kettlebell out at chest height.",
      tags=["kettlebell swing", "kettlebell", "hips", "cardio", "strength", "workout"], aliases=["kb-swing"])
def _(S):
    return [hd(7.5, 4.5), pl(S, [(8, 9), (10, 14.5), (10.5, 18), (9.5, 21.5)]), pl(S, [(8, 10), (16.5, 10.5)]),
            shell(circle(19, 14, 3)), line(arc(19, 11.5, 2.5, 180, 360))]


@icon("box-jump", CAT, "Side view of a figure tucking the knees in mid-air above a plyo box.",
      tags=["box jump", "plyometric", "plyo box", "jump", "leg power", "crossfit"], aliases=["box-jumps"])
def _(S):
    return [hd(9, 3.5), pl(S, [(9, 8), (10, 13), (16, 11.5), (12.5, 14.5)]), pl(S, [(9, 9), (14, 6.5)]),
            shell(rect(4, 18, 16, 4, min(S.R, 1)))]


@icon("high-knees", CAT, "Front view of a figure running in place with one knee raised to hip height.",
      tags=["high knees", "run in place", "cardio", "warm-up", "hiit", "workout"], aliases=["high-knee"])
def _(S):
    return [hd(12, 4.5), line(seg(12, 8.5, 12, 14.5)), pl(S, [(12, 14.5), (9, 21.5)]),
            pl(S, [(12, 14.5), (16.5, 12.5), (16, 18)]), pl(S, [(12, 9.5), (7.5, 12), (6, 7.5)]),
            pl(S, [(12, 9.5), (16, 8), (18.5, 11.5)])]


@icon("glute-bridge", CAT, "Side view of a figure lying on the back with the knees bent and the hips lifted into a straight line.",
      tags=["glute bridge", "hip raise", "glutes", "core", "floor exercise", "pilates"], aliases=["hip-bridge"])
def _(S):
    return [hd(3.5, 16.5), pl(S, [(7, 18), (17, 10), (19, 12), (18.5, 19.5)]),
            line(seg(7, 18, 11, 19.5)), line(seg(2, 21.5, 22, 21.5))]


@icon("superman-exercise", CAT, "Side view of a figure lying face down with the arms and legs lifted off the floor.",
      tags=["superman", "back extension", "lower back", "core", "floor exercise", "workout"], aliases=["superman-hold"])
def _(S):
    return [hd(15.5, 13), pl(S, [(2.5, 14.5), (7, 18), (14, 18), (20.5, 14.5)]), line(seg(2, 21.5, 22, 21.5))]


@icon("bicycle-crunch", CAT, "Side view of a figure lying with the shoulders lifted, one knee tucked in and the other leg extended.",
      tags=["bicycle crunch", "abs", "core", "crunch", "floor exercise", "workout"], aliases=["bicycle-crunches"])
def _(S):
    return [hd(5, 9), pl(S, [(7, 13), (11.5, 18), (21, 15.5)]), pl(S, [(11.5, 18), (15.5, 13), (18.5, 16.5)]),
            line(seg(2, 21.5, 22, 21.5))]


@icon("wall-sit", CAT, "Side view of a figure seated against a wall line with the knees at a right angle and no chair.",
      tags=["wall sit", "wall squat", "isometric", "legs", "endurance", "workout"], aliases=["wall-squat"])
def _(S):
    return [hd(7, 4.5), line(seg(3, 2, 3, 22)), pl(S, [(7, 9), (7, 15), (14, 15), (14, 21.5)]),
            pl(S, [(7, 10), (11, 13)])]


@icon("leg-raises", CAT, "Side view of a figure lying flat with the straight legs lifted up to vertical.",
      tags=["leg raises", "abs", "lower abs", "core", "floor exercise", "workout"], aliases=["leg-raise"])
def _(S):
    return [hd(3.5, 17), pl(S, [(7, 18.5), (14, 18.5), (14, 4)]), line(seg(2, 21.5, 22, 21.5))]


@icon("calf-raises", CAT, "Side view of a figure up on tiptoes on a step with an arrow showing the lift.",
      tags=["calf raises", "calves", "tiptoe", "heel raise", "legs", "workout"], aliases=["heel-raises"])
def _(S):
    return [hd(9, 3.5), line(seg(9, 8, 9, 13)), pl(S, [(9, 13), (9, 16.5), (12.5, 18)]),
            pl(S, [(9, 9), (6, 12)]),
            shell(rect(3, 19, 12, 3, 0)), line(seg(19, 16, 19, 8)), pl(S, [(16.5, 10.5), (19, 8), (21.5, 10.5)])]


@icon("handstand", CAT, "Front view of a figure balanced upside down on both hands with the legs straight up.",
      tags=["handstand", "inversion", "balance", "gymnastics", "calisthenics", "yoga"], aliases=["hand-stand"])
def _(S):
    return [hd(12, 19), line(seg(6.5, 21.5, 9.5, 13)), line(seg(17.5, 21.5, 14.5, 13)), line(seg(9.5, 13, 14.5, 13)),
            line(seg(12, 13, 12, 8)), pl(S, [(10, 2.5), (12, 8), (14, 2.5)])]


@icon("farmers-walk", CAT, "Front view of a walking figure carrying a heavy kettlebell hanging from each hand.",
      tags=["farmers walk", "farmer carry", "kettlebell", "grip", "strength", "carry"], aliases=["farmers-carry"])
def _(S):
    return [hd(12, 4.5), line(seg(12, 8.5, 12, 14)), pl(S, [(9.5, 21.5), (12, 14), (14.5, 21.5)]),
            pl(S, [(12, 9.5), (6, 14)]), pl(S, [(12, 9.5), (18, 14)]),
            dot(4.5, 18, 2.75), dot(19.5, 18, 2.75)]


@icon("nordic-walking", CAT, "Side view of a walking figure with a long pole planted on the ground ahead.",
      tags=["nordic walking", "pole walking", "walking poles", "hiking", "outdoor fitness", "senior fitness"], aliases=["pole-walking"])
def _(S):
    return [hd(10, 4.5), line(seg(10, 9, 10, 15)), pl(S, [(6, 21.5), (10, 15), (14, 21.5)]),
            pl(S, [(10, 10), (14.5, 11)]), line(seg(17, 6.5, 21, 21.5))]


@icon("step-aerobics", CAT, "Side view of a figure stepping one foot up onto a low aerobic step with the arms swinging.",
      tags=["step aerobics", "step class", "aerobic step", "cardio", "dance fitness", "workout"], aliases=["step-class"])
def _(S):
    return [hd(14, 4.5), line(seg(14, 9, 14, 14)), pl(S, [(14, 14), (9, 15.5), (8, 18)]), pl(S, [(14, 14), (16, 18), (17, 21.5)]),
            pl(S, [(14, 10), (10, 12)]), pl(S, [(14, 10), (18.5, 11.5)]), shell(rect(3, 18.5, 9, 3, 0))]


@icon("tai-chi", CAT, "Front view of a figure in a wide low stance with the arms flowing out in a slow curve.",
      tags=["tai chi", "qigong", "martial arts", "slow movement", "balance", "mindfulness"], aliases=["taichi"])
def _(S):
    return [hd(11, 4.5), line(seg(11, 9, 11, 13.5)), pl(S, [(18, 21.5), (16.5, 16.5), (11, 13.5), (6, 16.5), (4.5, 21.5)]),
            line("M11 10C14 8.5 17.5 8.5 21 10"), line("M11 10C8 11 5.5 12 3 11.5")]


@icon("pilates-exercise", CAT, "Side view of a figure on a mat rolling up from the floor with a round back and the arms reaching forward.",
      tags=["pilates", "roll up", "core", "mat pilates", "abs", "mat exercise"], aliases=["mat-pilates"])
def _(S):
    return [hd(9, 6.5), line("M9.5 19C3.5 17.5 3.5 12.5 7.5 10"), line(seg(9.5, 19, 21.5, 19)), line(seg(2, 21.5, 22, 21.5)),
            line(seg(8, 11, 16, 11))]


@icon("stretching", CAT, "Front view of a standing figure reaching both arms overhead and joining them above the head.",
      tags=["stretching", "reach", "warm-up", "flexibility", "cool down", "mobility"], aliases=["stretch"])
def _(S):
    return [hd(12, 9.5), pl(S, [(8.5, 14.5), (6.5, 7), (12, 2.5), (17.5, 7), (15.5, 14.5)]), line(seg(12, 14, 12, 16)),
            pl(S, [(8, 21.5), (12, 16), (16, 21.5)])]

# =========================================================================== stretches

FLOOR = lambda: line(seg(2, 21.5, 22, 21.5))  # noqa: E731


def mir(pts):
    return [(24 - x, y) for x, y in pts]


@icon("hamstring-stretch", CAT, "Side view of a figure seated with the legs straight out and the feet flexed, reaching forward toward the toes.",
      tags=["hamstring stretch", "toe touch", "seated stretch", "flexibility", "legs", "warm-up"], aliases=["toe-touch"])
def _(S):
    return [hd(15, 9.5), pl(S, [(5.5, 19), (12, 12.5)]), pl(S, [(5.5, 19), (19.5, 19), (20.5, 15)]), pl(S, [(12.5, 13), (18, 16.5)])]


@icon("quad-stretch", CAT, "Side view of a standing figure holding one foot behind against the buttock.",
      tags=["quad stretch", "quadriceps", "standing stretch", "thigh", "warm-up", "flexibility"], aliases=["quadriceps-stretch"])
def _(S):
    return [hd(12, 4.5), line(seg(12, 9, 12, 14.5)), pl(S, [(12, 14.5), (12.5, 21.5)]),
            pl(S, [(12, 14.5), (11, 19.5), (5.5, 15.5)]), pl(S, [(12, 10), (8, 13), (5.5, 15.5)])]


@icon("neck-stretch", CAT, "Front view of the head and shoulders with a hand over the head gently pulling it to the side.",
      tags=["neck stretch", "neck", "shoulders", "desk stretch", "tension relief", "head tilt"], aliases=["neck-tilt"])
def _(S):
    return [shell(circle(10, 8.5, 3.5)),
            line(poly([(3, 21.5), (4, 17.5), (12, 15.5), (20, 17.5), (21, 21.5)], r=S.r * 2)),
            pl(S, [(20, 17.5), (21, 8.5), (15.5, 4.5)])]


@icon("butterfly-stretch", CAT, "Front view of a figure seated upright with the soles of the feet together and the knees out to the sides.",
      tags=["butterfly stretch", "bound angle", "hip opener", "seated stretch", "groin", "flexibility"], aliases=["cobbler-pose"])
def _(S):
    return [hd(12, 4.5), line(seg(12, 9, 12, 14.5)), line(poly([(12, 14.5), (3.5, 16.5), (12, 20.5), (20.5, 16.5)], closed=True, r=S.r))]


# =========================================================================== yoga poses

@icon("tree-pose", CAT, "Front view of a figure standing on one leg with the other foot on the inner thigh and the arms raised in a Y.",
      tags=["tree pose", "vrksasana", "yoga", "balance", "standing pose", "one leg"], aliases=["vrksasana"])
def _(S):
    return [hd(12, 7.5), pl(S, [(5.5, 3), (9.5, 12), (14.5, 12), (18.5, 3)]), line(seg(12, 12, 12, 16.5)),
            line(seg(12, 16.5, 12.5, 21.5)), pl(S, [(12, 16.5), (6.5, 19), (11.5, 19.5)])]


@icon("warrior-three-pose", CAT, "Side view of a figure balanced on one leg with the torso, arms and back leg in one horizontal line.",
      tags=["warrior three", "warrior 3", "virabhadrasana", "yoga", "balance", "standing pose"], aliases=["warrior-iii"])
def _(S):
    return [hd(17, 6.5), pl(S, [(2.5, 11), (14, 11)]), line(seg(14, 11, 22, 11)), pl(S, [(14, 11), (14, 21.5)])]


@icon("downward-dog", CAT, "Side view of a figure in an inverted V with the hands and feet on the floor and the hips high.",
      tags=["downward dog", "downward facing dog", "adho mukha svanasana", "yoga", "inversion", "vinyasa"], aliases=["downward-facing-dog"])
def _(S):
    return [hd(12.5, 15), pl(S, [(3, 21.5), (13, 5.5), (21, 21.5)])]


@icon("cobra-pose", CAT, "Side view of a figure lying face down with the legs flat and the chest lifted on straight arms.",
      tags=["cobra pose", "bhujangasana", "yoga", "backbend", "spine", "floor pose"], aliases=["bhujangasana"])
def _(S):
    return [hd(19.5, 7.5), pl(S, [(2.5, 18.5), (10, 18.5), (16, 11)]), pl(S, [(16, 11), (16.5, 20)]), FLOOR()]


@icon("childs-pose", CAT, "Side view of a figure kneeling and folded forward in a low curve with the head down and the arms stretched ahead.",
      tags=["child's pose", "balasana", "yoga", "rest pose", "restorative", "kneeling"], aliases=["balasana"])
def _(S):
    return [hd(16.5, 17.5), line("M4.5 19.5C4 9.5 14 9 14.5 15.5"), line(seg(18, 21.5, 22, 21.5)), FLOOR()]


@icon("triangle-pose", CAT, "Front view of a figure with the legs wide, one hand down to the shin and the other arm pointing straight up.",
      tags=["triangle pose", "trikonasana", "yoga", "side stretch", "standing pose", "wide legs"], aliases=["trikonasana"])
def _(S):
    return [hd(4.5, 8.5), pl(S, [(9, 10), (14, 12)]), pl(S, [(4.5, 21.5), (14, 12), (21, 21.5)]), line(seg(9, 2.5, 9, 17))]


@icon("boat-pose", CAT, "Side view of a figure balanced on the sit bones with straight legs and torso raised in a V, arms forward.",
      tags=["boat pose", "navasana", "yoga", "core", "abs", "balance"], aliases=["navasana"])
def _(S):
    return [hd(3.5, 6.5), pl(S, [(4.5, 11), (9, 18), (21, 11)]), pl(S, [(6, 12), (13.5, 11)])]


@icon("cat-cow-pose", CAT, "Side view of a figure on hands and knees with the back rounded up in an arch.",
      tags=["cat cow", "cat pose", "marjaryasana", "yoga", "spine mobility", "all fours"], aliases=["cat-pose"])
def _(S):
    return [hd(20.5, 15), line("M7 13C8 5 16 5 17 12.5"), pl(S, [(7, 13), (7, 20.5), (3, 20.5)]), pl(S, [(17, 12.5), (17, 20.5)]), FLOOR()]


@icon("headstand", CAT, "Side view of a figure upside down on the head and forearms with the legs straight up.",
      tags=["headstand", "sirsasana", "yoga", "inversion", "balance", "tripod"], aliases=["sirsasana"])
def _(S):
    return [hd(13, 18.5), line(seg(13, 15.5, 13, 2)), line(seg(4, 21.5, 20, 21.5)),
            line(seg(6, 21.5, 11.5, 13))]


@icon("shoulder-stand", CAT, "Side view of a figure on the shoulders with the hands supporting the lower back and the legs straight up.",
      tags=["shoulder stand", "sarvangasana", "yoga", "inversion", "legs up", "floor pose"], aliases=["sarvangasana"])
def _(S):
    return [hd(3.5, 17.5), line(seg(7.5, 19, 12.5, 2.5)), line(seg(11, 19, 9.5, 12.5)), FLOOR()]


@icon("wheel-pose", CAT, "Side view of a figure in a full backbend arch on hands and feet with the belly facing up.",
      tags=["wheel pose", "urdhva dhanurasana", "yoga", "backbend", "full wheel", "arch"], aliases=["urdhva-dhanurasana"])
def _(S):
    return [hd(13, 17), line("M4 21C4 5 15 4 17.5 14"), pl(S, [(17.5, 14), (19, 21)]), FLOOR()]


@icon("bow-pose", CAT, "Side view of a figure lying on the belly holding the ankles behind, the body curved like a bow.",
      tags=["bow pose", "dhanurasana", "yoga", "backbend", "belly down", "floor pose"], aliases=["dhanurasana"])
def _(S):
    return [hd(19.5, 9.5), line("M4.5 8.5C4 17 9 20.5 16.5 14"), line(seg(16.5, 14, 4.5, 8.5)), line(seg(7, 21.5, 15, 21.5))]


@icon("pigeon-pose", CAT, "Side view of a figure with the front leg folded under the torso, the back leg stretched long and the chest upright.",
      tags=["pigeon pose", "eka pada rajakapotasana", "yoga", "hip opener", "floor pose", "stretch"], aliases=["eka-pada-rajakapotasana"])
def _(S):
    return [hd(14, 5), pl(S, [(10.5, 17), (12.5, 10)]), pl(S, [(10.5, 17), (18.5, 17.5), (11.5, 20.5)]), pl(S, [(10.5, 17), (2.5, 20)]),
            pl(S, [(12.5, 10.5), (16.5, 15)])]


@icon("dancer-pose", CAT, "Side view of a figure on one leg holding the other foot up behind with one hand, the other arm reaching forward.",
      tags=["dancer pose", "natarajasana", "yoga", "balance", "standing pose", "backbend"], aliases=["natarajasana"])
def _(S):
    return [hd(12, 4.5), line(seg(12, 9, 12, 14)), pl(S, [(12, 14), (12, 21.5)]), pl(S, [(12, 14), (6, 15), (4.5, 8.5)]),
            pl(S, [(12, 10), (8, 6), (4.5, 8.5)]), pl(S, [(12, 10), (19, 8)])]


@icon("chair-pose", CAT, "Side view of a figure with the knees bent as if sitting on an invisible chair and the arms raised overhead.",
      tags=["chair pose", "utkatasana", "yoga", "squat", "standing pose", "legs"], aliases=["utkatasana"])
def _(S):
    return [hd(7.5, 5.5), pl(S, [(9, 10), (7, 15), (14.5, 15.5), (14, 21.5)]), pl(S, [(9, 10), (15.5, 4.5)])]


@icon("fish-pose", CAT, "Side view of a figure lying on the back with the chest arched up and the crown of the head on the floor.",
      tags=["fish pose", "matsyasana", "yoga", "backbend", "chest opener", "floor pose"], aliases=["matsyasana"])
def _(S):
    return [hd(4, 17), pl(S, [(7.5, 19.5), (11, 12.5), (14.5, 19), (21.5, 19)]), FLOOR()]


@icon("plow-pose", CAT, "Side view of a figure lying on the shoulders with the legs folded back over the head, toes touching the floor.",
      tags=["plow pose", "halasana", "yoga", "inversion", "forward fold", "floor pose"], aliases=["halasana"])
def _(S):
    return [hd(16, 18), pl(S, [(10, 20), (10, 8), (21, 20)]), FLOOR()]


@icon("corpse-pose", CAT, "Top view of a figure lying flat on a mat with the arms slightly out and the legs apart.",
      tags=["corpse pose", "savasana", "yoga", "relaxation", "rest", "lying down"], aliases=["savasana"])
def _(S):
    return [shell(rect(1.5, 4.5, 21, 15, S.R)), hd(6.5, 12), line(seg(10, 12, 14.5, 12)), pl(S, [(19, 9.5), (14.5, 12), (19, 14.5)]),
            pl(S, [(12.5, 8), (10, 12), (12.5, 16)])]


@icon("happy-baby-pose", CAT, "Side view of a figure lying on the back holding the feet with the knees bent toward the armpits.",
      tags=["happy baby", "ananda balasana", "yoga", "hip opener", "floor pose", "relaxation"], aliases=["ananda-balasana"])
def _(S):
    return [hd(3.5, 17), pl(S, [(7, 19), (14, 19)]), pl(S, [(14, 19), (10, 13), (15, 8.5)]), pl(S, [(7.5, 18), (15, 8.5)]), FLOOR()]


@icon("seated-forward-bend", CAT, "Side view of a figure seated with the legs straight and the torso folded flat over them.",
      tags=["seated forward bend", "paschimottanasana", "yoga", "forward fold", "hamstrings", "floor pose"], aliases=["paschimottanasana"])
def _(S):
    return [hd(18.5, 13.5), pl(S, [(5, 19.5), (21, 19.5)]), pl(S, [(5.5, 19), (7, 13.5), (14, 13.5)])]


@icon("standing-forward-bend", CAT, "Side view of a figure standing with the torso folded down over straight legs and the hands to the floor.",
      tags=["standing forward bend", "uttanasana", "yoga", "forward fold", "hamstrings", "standing pose"], aliases=["uttanasana"])
def _(S):
    return [hd(13, 17.5), line(seg(7, 6.5, 7, 21.5)), pl(S, [(7, 6.5), (12.5, 8.5), (13, 14)]), pl(S, [(12.8, 10), (17.5, 21)])]


@icon("garland-pose", CAT, "Front view of a figure in a deep squat with the heels down and the palms together at the chest.",
      tags=["garland pose", "malasana", "yoga", "squat", "hip opener", "deep squat"], aliases=["malasana", "yogi-squat"])
def _(S):
    return [hd(12, 4.5), line(seg(12, 9, 12, 14.5)), pl(S, [(8.5, 21.5), (5, 15), (12, 14.5), (19, 15), (15.5, 21.5)]),
            pl(S, [(9.5, 13.5), (12, 10), (14.5, 13.5)])]


@icon("goddess-pose", CAT, "Front view of a figure in a wide squat with the knees out and the arms bent up like goalposts.",
      tags=["goddess pose", "utkata konasana", "yoga", "wide squat", "standing pose", "legs"], aliases=["utkata-konasana"])
def _(S):
    return [hd(12, 4.5), line(seg(12, 9, 12, 13.5)), pl(S, [(6, 21.5), (6, 16.5), (12, 13.5), (18, 16.5), (18, 21.5)]),
            pl(S, [(12, 9.5), (6, 9.5), (6, 4.5)]), pl(S, [(12, 9.5), (18, 9.5), (18, 4.5)])]


@icon("splits-pose", CAT, "Side view of a figure sitting on the floor with the legs split front and back and the arms raised.",
      tags=["splits", "hanumanasana", "yoga", "flexibility", "gymnastics", "floor pose"], aliases=["hanumanasana", "the-splits"])
def _(S):
    return [hd(12, 5), pl(S, [(2.5, 19.5), (21.5, 19.5)]), line(seg(12, 10, 12, 19.5)), pl(S, [(7.5, 3), (12, 10), (16.5, 3)])]


@icon("legs-up-the-wall", CAT, "Side view of a figure lying on the back with the straight legs resting up against a wall line.",
      tags=["legs up the wall", "viparita karani", "yoga", "restorative", "relaxation", "recovery"], aliases=["viparita-karani"])
def _(S):
    return [line(seg(21.5, 2, 21.5, 22)), hd(4, 16.5), pl(S, [(8, 18.5), (17.5, 18.5), (17.5, 4)]), line(seg(2, 21.5, 21.5, 21.5))]


@icon("partner-yoga", CAT, "Two figures standing back to back, leaning apart with their hands joined to balance each other.",
      tags=["partner yoga", "couples yoga", "acro yoga", "balance", "pair", "trust"], aliases=["couples-yoga"])
def _(S):
    return [hd(5, 5), hd(19, 5), pl(S, [(5.5, 9.5), (7.5, 15), (10, 21.5)]), pl(S, mir([(5.5, 9.5), (7.5, 15), (10, 21.5)])),
            pl(S, [(5.5, 10), (12, 14.5)]), pl(S, mir([(5.5, 10), (12, 14.5)]))]


# =========================================================================== props and gear

def leaf(bx, by, ang, length, width):
    tip = pt_on(bx, by, length, ang)
    mid = pt_on(bx, by, length * 0.5, ang)
    c1 = pt_on(*mid, width, ang + 90)
    c2 = pt_on(*mid, width, ang - 90)
    f = lambda p: f"{p[0]:.2f} {p[1]:.2f}"  # noqa: E731
    return f"M{bx:.2f} {by:.2f}Q{f(c1)} {f(tip)}Q{f(c2)} {bx:.2f} {by:.2f}Z"


from dsl import pt_on  # noqa: E402


@icon("yoga-block", CAT, "Three-quarter view of a rectangular foam yoga block with its top and side faces.",
      tags=["yoga block", "foam block", "yoga brick", "prop", "yoga gear", "support"], aliases=["yoga-brick"])
def _(S):
    return [shell(poly([(3, 10), (7, 5.5), (21, 5.5), (21, 14), (17, 18.5), (3, 18.5)], closed=True, r=S.r)),
            detail(seg(3.5, 10, 17, 10)), detail(seg(17, 10, 20.5, 6)), detail(seg(17, 10, 17, 18))]


@icon("yoga-strap", CAT, "A yoga strap curled into a loop with a metal D ring buckle.",
      tags=["yoga strap", "stretching strap", "belt", "prop", "yoga gear", "flexibility"], aliases=["yoga-belt"])
def _(S):
    return [shell(ellipse(10.5, 13, 8, 6.5)), shell(ellipse(10.5, 13, 3.5, 2.5)),
            shell(rect(16, 4, 6, 7, min(S.R, 2))), line(seg(18, 14, 21.5, 21))]


@icon("yoga-wheel", CAT, "Three-quarter view of a wide hoop yoga wheel, a hollow padded ring seen at an angle.",
      tags=["yoga wheel", "dharma wheel", "backbend wheel", "prop", "yoga gear", "stretching"], aliases=["dharma-yoga-wheel"])
def _(S):
    return [shell(ellipse(8, 12, 5, 7.5)), shell(ellipse(8, 12, 1.75, 3) if S.name == "rounded" else poly([(8, 8.5), (9.75, 10.25), (9.75, 13.75), (8, 15.5), (6.25, 13.75), (6.25, 10.25)], closed=True)),
            line(seg(8, 4.5, 16.5, 4.5)), line(seg(8, 19.5, 16.5, 19.5)),
            line("M16.5 4.5A5 7.5 0 0 1 16.5 19.5")]


@icon("yoga-bolster", CAT, "Side view of a long cylindrical yoga bolster cushion with a handle loop on one end.",
      tags=["yoga bolster", "cushion", "restorative yoga", "prop", "yoga gear", "pillow"], aliases=["bolster"])
def _(S):
    return [shell(rect(5, 9, 17, 9.5, min(S.R, 4))), detail("M17.5 9.5C19.5 11.5 19.5 16 17.5 18"),
            line(poly([(5, 11), (2.5, 11), (2.5, 16.5), (5, 16.5)], r=S.r * 0.5))]


@icon("meditation-cushion", CAT, "Side view of a round plump floor cushion with pleats and a button, resting on a flat mat.",
      tags=["meditation cushion", "zafu", "floor cushion", "mindfulness", "sitting", "meditation"], aliases=["zafu"])
def _(S):
    return [shell(poly([(2.5, 14.5), (4, 10.5), (8, 8), (16, 8), (20, 10.5), (21.5, 14.5), (18, 18.5), (6, 18.5)], closed=True, r=S.r * 2)),
            detail(seg(8.5, 9, 7, 17.5)), detail(seg(15.5, 9, 17, 17.5)), detail(seg(12, 12.5, 12, 18)), line(seg(2, 21.5, 22, 21.5))]


@icon("meditation-bench", CAT, "Side view of a low slanted kneeling bench with a sloped seat on two short angled legs.",
      tags=["meditation bench", "seiza bench", "kneeling bench", "prayer bench", "mindfulness", "seat"], aliases=["seiza-bench"])
def _(S):
    return [shell(poly([(2.5, 9), (21.5, 13), (21.5, 15.5), (2.5, 12)], closed=True, r=S.r * 0.5)),
            pl(S, [(6, 13), (3.5, 21.5)]), pl(S, [(18, 15), (20.5, 21.5)])]


# =========================================================================== heat, cold and bodywork

@icon("sauna", CAT, "Front view of a wooden sauna room with two stepped benches, a stove and rising steam.",
      tags=["sauna", "steam", "heat therapy", "spa", "wellness", "wooden room"], aliases=["finnish-sauna"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, min(S.R, 3))), detail(seg(12, 9, 21, 9)), detail(seg(12, 15, 21, 15)),
            sq(4.5, 16, 4, 4), detail("M6.5 13.5C5.5 12 7.5 10.5 6.5 8.5")]


@icon("steam-room", CAT, "Front view of a tiled bench with thick clouds of steam rising in front of it.",
      tags=["steam room", "steam bath", "hammam", "spa", "wellness", "vapor"])
def _(S):
    return [shell(rect(2.5, 15, 19, 3, min(S.R, 1.5))), line(seg(5, 18, 5, 21.5)), line(seg(19, 18, 19, 21.5)),
            shell("M7 12C4 12 3 8.5 6 7.5C6.5 4 11 3.5 12 6C14 4 18.5 5 18 8.5C21 9 20.5 12 17.5 12Z")]


@icon("cold-plunge", CAT, "Side view of a round tub of water with floating ice cubes and a snowflake above.",
      tags=["cold plunge", "ice bath", "cold therapy", "recovery", "cold water", "wellness"])
def _(S):
    return [shell(poly([(3, 12), (21, 12), (19.5, 20.5), (4.5, 20.5)], closed=True, r=S.r)),
            detail(poly([(5, 15.5), (8, 14), (11, 15.5), (14, 14), (17, 15.5), (19, 14.5)], r=S.r)),
            sq(7, 16.5, 3, 3), sq(13, 17, 3, 3),
            line(seg(12, 2, 12, 8)), line(seg(9, 3.6, 15, 6.4)), line(seg(9, 6.4, 15, 3.6))]


@icon("float-tank", CAT, "Side view of an egg-shaped floatation pod with the lid raised and water inside.",
      tags=["float tank", "sensory deprivation", "isolation tank", "flotation therapy", "relaxation", "spa"], aliases=["flotation-tank"])
def _(S):
    return [shell(poly([(2.5, 13), (21.5, 13), (20, 20.5), (4, 20.5)], closed=True, r=S.r * 1.5)),
            detail(poly([(5, 16.5), (8, 15.5), (11, 16.5), (14, 15.5), (17, 16.5), (19, 16)], r=S.r)),
            line("M4 11C4 6 9 3 15 3.5"), line(seg(3, 13, 3, 11.5))]


@icon("cryotherapy-chamber", CAT, "Front view of a tall cylinder cabin with a head showing at the top and a frost sparkle beside it.",
      tags=["cryotherapy", "cryo chamber", "cold therapy", "recovery", "frost", "wellness"], aliases=["cryo-chamber"])
def _(S):
    return [hd(10, 4), shell(rect(4.5, 8, 11, 13.5, min(S.R, 3))), detail(seg(6.5, 10.5, 13.5, 10.5)),
            line(seg(19.5, 11.5, 19.5, 16.5)), line(seg(17.4, 12.75, 21.6, 15.25)), line(seg(17.4, 15.25, 21.6, 12.75))]


@icon("sauna-whisk", CAT, "A bundle of leafy birch twigs tied together at a short handle.",
      tags=["sauna whisk", "birch whisk", "vihta", "venik", "sauna", "leaves"], aliases=["vihta", "birch-whisk"])
def _(S):
    return [shell(leaf(12, 14.5, -90, 12.5, 5)), shell(leaf(12, 14.5, -125, 11, 5)), shell(leaf(12, 14.5, -55, 11, 5)),
            shell(leaf(12, 14.5, -158, 8.5, 4.5)), shell(leaf(12, 14.5, -22, 8.5, 4.5)),
            line(seg(12, 14.5, 12, 21.5)), line(seg(9.5, 16.5, 14.5, 16.5))]


@icon("back-massage", CAT, "Side view of a figure lying face down on a table with two hands pressing on the back.",
      tags=["back massage", "massage therapy", "spa", "bodywork", "relaxation", "masseur"])
def _(S):
    return [hd(4.5, 10.5), line(seg(8, 12, 21, 12)), line(seg(2, 15.5, 22, 15.5)), line(seg(4, 15.5, 4, 21.5)), line(seg(20, 15.5, 20, 21.5)),
            pl(S, [(8, 2.5), (10, 8.5)]), pl(S, [(15, 2.5), (13.5, 8.5)])]
