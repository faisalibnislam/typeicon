"""TypeIcon Core: wellness (batch 003): bodywork and spa, mindful rituals, nutrition and supplements, sleep, mental health and calm spaces.

Figures follow the wellness and people sets: a solid head (r 2.25) over 2 px limbs, faceted in Line and filleted in
Rounded (poly with r=S.r). Heads in profile face right and share the outline used by the anatomy set.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar, transform_path

CAT = "wellness"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def pl(S, pts):
    return line(poly(pts, r=S.r))


def hd(x, y, r=2.25):
    return dot(x, y, r)


def sq(x, y, w, h):
    return Part("dot", rect(x, y, w, h))


def xf(d, m):
    return path_to_d(transform_path(P(d), m))


def tf(d, k=1.0, dx=0.0, dy=0.0, sx=1.0):
    return xf(d, (k * sx, 0, 0, k, dx, dy))


def star4(cx, cy, r, k=0.3):
    return poly([polar(cx, cy, r if i % 2 == 0 else r * k, -90 + i * 45) for i in range(8)], closed=True)


HEAD = "M8 21V17.2C5.6 15.8 4 13.3 4 10.5C4 6.4 7.6 3 12 3C16.1 3 19 5.9 19 9.5L20.5 12.8L19 13.3V15.5C19 16.6 18.1 17.5 17 17.5H14V21Z"
HEAD_R = ("M8 20V17.2C5.6 15.8 4 13.3 4 10.5C4 6.4 7.6 3 12 3C16.1 3 19 5.9 19 9.5L20.2 12Q20.6 12.9 19.7 13.1L19 13.3V15.5"
          "C19 16.6 18.1 17.5 17 17.5H14V20C14 20.6 13.6 21 13 21H9C8.4 21 8 20.6 8 20Z")


def head(S, k=1.0, dx=0.0, dy=0.0):
    """Profile head facing right (same outline as the anatomy set), scaled by k and moved."""
    return tf(L(S, HEAD, HEAD_R), k, dx, dy)


def zzz(x, y, k=1.0):
    """A small Z drawn as a line (x, y is its top-left corner)."""
    return line(poly([(x, y), (x + 4 * k, y), (x, y + 4 * k), (x + 4 * k, y + 4 * k)], r=0))


# =========================================================================== bodywork and spa

@icon("foot-massage", CAT, "Side view of a bare foot with two arrows pressing up into the sole from below.",
      tags=["foot rub", "sole massage", "reflexology", "spa", "pedicure", "relaxation"], aliases=["foot-rub"])
def _(S):
    foot = poly([(6, 2.5), (12, 2.5), (12, 8), (19, 10.5), (21.5, 13), (21.5, 15.5), (4, 15.5), (4, 12.5), (6, 9)], closed=True, r=S.r)
    return [shell(foot), pl(S, [(6, 20), (8.5, 17.5), (11, 20)]), pl(S, [(13, 20), (15.5, 17.5), (18, 20)])]


@icon("reflexology-chart", CAT, "The sole of a foot with five toes and two zone lines dividing it into regions.",
      tags=["reflexology", "foot map", "pressure points", "foot chart", "zones", "alternative medicine"])
def _(S):
    sole = poly([(7, 10), (9.5, 7.5), (15, 7.5), (17.5, 10.5), (16, 15), (15.5, 19), (13, 21.5), (10, 21.5), (8, 19), (8.5, 14.5)], closed=True, r=S.r + 1.2)
    return [shell(sole), detail(seg(8.5, 12.5, 16.5, 12.5)), detail(seg(9, 17, 15.5, 17)),
            dot(7.2, 5.2, 1.3), dot(10.2, 3.7, 1.3), dot(13.4, 3.5, 1.3), dot(16.3, 4.4, 1.3), dot(18.6, 6.4, 1.3)]


@icon("acupuncture", CAT, "A rounded back or shoulder outline with three fine needles standing in the skin.",
      tags=["needles", "traditional chinese medicine", "tcm", "pain relief", "meridian", "alternative medicine"])
def _(S):
    body = L(S, "M3 21L3.5 17L8 13.5H16L20.5 17L21 21Z", "M3 21C3 15 7 13 12 13S21 15 21 21Z")
    out = [shell(body)]
    for x in (7.5, 12, 16.5):
        out += [dot(x, 3.8, 1.5), line(seg(x, 5, x, 12)), detail(seg(x, 13, x, 17))]
    return out


@icon("acupressure-mat", CAT, "A flat slanted mat dotted with rows of tiny spikes.",
      tags=["spike mat", "shakti mat", "pressure mat", "back pain", "relaxation", "massage"], aliases=["spike-mat"])
def _(S):
    mat = poly([(7, 5), (22, 5), (17, 19), (2, 19)], closed=True, r=S.r)
    out = [shell(mat)]
    for (x, y) in [(9, 9), (14, 9), (18, 9), (7.5, 14), (12, 14), (16, 14)]:
        out.append(dot(x, y, 1.1))
    return out


@icon("scalp-massager", CAT, "A short handle with a spray of curved wire prongs that end in small balls.",
      tags=["head scratcher", "head massager", "tingles", "relaxation", "wire massager", "scalp"], aliases=["head-scratcher"])
def _(S):
    out = [shell(poly([(9.5, 15), (14.5, 15), (14.5, 22), (9.5, 22)], closed=True, r=S.r))]
    for (ex, ey, cx, cy) in [(4, 8, 6, 13), (7.5, 4.5, 8, 11), (12, 3.5, 12, 11), (16.5, 4.5, 16, 11), (20, 8, 18, 13)]:
        out += [line(f"M12 15Q{cx} {cy} {ex} {ey + 1.2}"), dot(ex, ey, 1.3)]
    return out


@icon("foot-roller", CAT, "A ridged wooden roller resting on a flat base with two end supports.",
      tags=["foot massager", "roller", "plantar fasciitis", "sole", "wooden roller", "relaxation"], aliases=["foot-massage-roller"])
def _(S):
    return [shell(rect(3, 8, 18, 7, min(S.R, 3.5))), detail(seg(8, 8, 8, 15)), detail(seg(12, 8, 12, 15)), detail(seg(16, 8, 16, 15)),
            line(seg(2, 21, 22, 21)), line(seg(6, 15, 6, 21)), line(seg(18, 15, 18, 21))]


@icon("herbal-compress", CAT, "A round cloth bundle of herbs gathered and tied tight around a short handle.",
      tags=["herbal ball", "thai massage", "luk pra kob", "spa", "poultice", "herbs"], aliases=["herbal-ball"])
def _(S):
    bundle = poly([(12, 2.5), (17.5, 5), (19.5, 10), (17, 14), (14.5, 16), (9.5, 16), (7, 14), (4.5, 10), (6.5, 5)], closed=True, r=S.r + 1.2)
    return [shell(bundle), detail(seg(12, 15, 12, 8)), detail(seg(9.5, 14, 7.5, 9)), detail(seg(14.5, 14, 16.5, 9)),
            shell(rect(10, 16, 4, 6, 0))]


@icon("chiropractic-adjustment", CAT, "A column of three vertebrae with an arrow pushing in from each side.",
      tags=["chiropractor", "spine adjustment", "back crack", "spinal manipulation", "back pain", "osteopathy"])
def _(S):
    out = []
    for y in (2.5, 9.5, 16.5):
        out.append(shell(rect(9, y, 6, 4.5, min(S.R, 2))))
    out += [line(poly([(2.5, 9), (6, 12), (2.5, 15)], r=S.r)), line(poly([(21.5, 4), (18, 7), (21.5, 10)], r=S.r)),
            line(seg(2.5, 12, 6, 12)), line(seg(21.5, 7, 18, 7))]
    return out


# =========================================================================== rituals and calm objects

@icon("singing-bowl", CAT, "A wide metal bowl on a round cushion with a wooden striker standing beside it.",
      tags=["tibetan bowl", "sound healing", "meditation", "resonance", "himalayan bowl", "gong"], aliases=["tibetan-bowl"])
def _(S):
    bowl = L(S, "M2 6H16C16 11 13 14 9 14C5 14 2 11 2 6Z", "M3 6H15Q16 6 16 7C15.5 11 12.8 14 9 14S2.5 11 2 7Q2 6 3 6Z")
    return [shell(bowl), shell(rect(4, 17, 10, 4.5, min(S.R, 1.5))), line(seg(20, 8, 20, 21)), dot(20, 5.5, 2.25)]


@icon("incense-stick", CAT, "A thin incense stick leaning in a low holder with a curl of smoke rising from the lit tip.",
      tags=["agarbatti", "joss stick", "aromatherapy", "smoke", "meditation", "fragrance"], aliases=["joss-stick"])
def _(S):
    return [solid(rect(4, 19, 16, 3, 1)), line(seg(9, 19, 14, 9)), line("M14 9C11.5 7 16.5 5.5 13.5 2.5")]


@icon("smudge-stick", CAT, "A tied bundle of dried sage with leafy tips and a ribbon of smoke rising from the top.",
      tags=["sage bundle", "smudging", "cleansing", "ritual", "white sage", "smoke"], aliases=["sage-bundle"])
def _(S):
    body = poly([(9.5, 21.5), (14.5, 21.5), (15.5, 14), (17, 9), (14.5, 6.5), (12, 8.5), (9.5, 6.5), (7, 9), (8.5, 14)], closed=True, r=S.r)
    return [shell(body), detail(seg(8, 15.5, 16, 15.5)), detail(seg(12, 11, 12, 13)),
            line("M12 6C10.5 4.8 13.5 3.8 12 2")]


@icon("zen-stones", CAT, "Four smooth flat stones balanced in a stack, each smaller than the one below.",
      tags=["cairn", "balanced stones", "rock stack", "spa", "mindfulness", "balance"], aliases=["stacked-stones"])
def _(S):
    out = []
    for (w, y) in [(6, 4.2), (10, 8.4), (14, 12.6), (18, 16.8)]:
        x0, x1 = 12 - w / 2, 12 + w / 2
        out.append(shell(poly([(x0, y + 2.2), (x0 + 1.5, y), (x1 - 1.5, y), (x1, y + 2.2), (x1 - 1.5, y + 4.2), (x0 + 1.5, y + 4.2)], closed=True, r=S.r)))
        if w < 18:
            out.append(detail(seg(x0 + 2.2, y + 4.2, x1 - 2.2, y + 4.2)))
    return out


@icon("zen-garden", CAT, "Top view of a tray of raked sand with a loop of rake lines circling two small rocks.",
      tags=["rock garden", "karesansui", "japanese garden", "raked sand", "minimalism", "calm"])
def _(S):
    ring = "M9 7.5H15A4.5 4.5 0 0 1 15 16.5H9A4.5 4.5 0 0 1 9 7.5Z"
    return [shell(rect(2, 3, 20, 18, S.R)), detail(ring), solid(circle(9, 12, 1.6)), solid(circle(15, 12, 1.6))]


@icon("tabletop-fountain", CAT, "Three stacked stone bowls, each wider than the one above, with water dripping down between them.",
      tags=["water feature", "indoor fountain", "zen", "spa", "relaxation", "feng shui"], aliases=["zen-fountain"])
def _(S):
    out = []
    for (w, y, h) in [(8, 2.5, 3.5), (13, 9, 4), (20, 16.5, 5)]:
        x0, x1 = 12 - w / 2, 12 + w / 2
        out.append(shell(poly([(x0, y), (x1, y), (x1 - 1.5, y + h), (x0 + 1.5, y + h)], closed=True, r=S.r)))
    out += [line(seg(9, 6.3, 9, 8.5)), line(seg(15, 6.3, 15, 8.5)), line(seg(6.5, 13.3, 6.5, 15.5)), line(seg(17.5, 13.3, 17.5, 15.5))]
    return out


@icon("spa-towels", CAT, "Five rolled towels stacked in a pyramid, seen from the ends, with a small flower on top.",
      tags=["rolled towels", "spa", "bath towels", "hotel", "massage", "relaxation"], aliases=["rolled-towels"])
def _(S):
    out = []
    for (x, y) in [(5.5, 18.2), (12, 18.2), (18.5, 18.2), (8.8, 11.6), (15.2, 11.6)]:
        out += [shell(poly(regular(x, y, 3.3, 8, start=-67.5), closed=True, r=S.r)), dot(x, y, 0.9)]
    out.append(solid(star4(12, 4.2, 2.6, 0.45)))
    return out


@icon("spa-slippers", CAT, "Top view of a pair of open-toe spa slippers, each with a wide strap across the front.",
      tags=["slippers", "spa", "hotel", "open toe", "sandals", "footwear", "relaxation"], aliases=["open-toe-slippers"])
def _(S):
    out = []
    for x in (3.5, 14.5):
        out.append(shell(poly([(x, 8), (x + 1.2, 4), (x + 5.8, 4), (x + 7, 8), (x + 7, 17), (x + 5.8, 21), (x + 1.2, 21), (x, 17)], closed=True, r=S.r + 0.6)))
        out.append(detail(poly([(x, 11), (x + 3.5, 8.5), (x + 7, 11)], r=0)))
    return out


@icon("facial-treatment", CAT, "Front view of a face with a headband and a cucumber slice over each eye.",
      tags=["facial", "face mask", "cucumber eyes", "skincare", "spa", "beauty treatment"], aliases=["spa-facial"])
def _(S):
    face = poly([(6.5, 5), (17.5, 5), (18.5, 13), (15.5, 19), (12, 21), (8.5, 19), (5.5, 13)], closed=True, r=S.r + 1.5)
    return [shell(face), detail(seg(6, 8, 18, 8)), detail(circle(9, 12.5, 2.3)), detail(circle(15, 12.5, 2.3)),
            detail(seg(10.5, 17.2, 13.5, 17.2))]


@icon("food-pyramid", CAT, "A triangle split into three horizontal food groups with small food dots in each band.",
      tags=["nutrition pyramid", "food groups", "healthy eating", "diet", "dietitian", "balanced diet"], aliases=["nutrition-pyramid"])
def _(S):
    tri = poly([(12, 2.5), (22, 20.5), (2, 20.5)], closed=True, r=S.r)
    return [shell(tri), detail(seg(8.3, 9.5, 15.7, 9.5)), detail(seg(5.2, 15, 18.8, 15)),
            dot(12, 6.8, 0.8), dot(9.6, 12.4, 0.9), dot(14.4, 12.4, 0.9), dot(7.2, 18.1, 0.9), dot(12, 18.1, 0.9), dot(16.8, 18.1, 0.9)]


@icon("macronutrients", CAT, "A round chart pulled apart into three sectors for protein, carbohydrate and fat.",
      tags=["macros", "protein carbs fat", "diet", "calories", "nutrition", "pie chart"], aliases=["macros"])
def _(S):
    out = []
    for a0, a1 in [(-90, 40), (40, 160), (160, 270)]:
        mid = (a0 + a1) / 2
        ox, oy = polar(0, 0, 2.2, mid)
        cx, cy = 12 + ox, 12 + oy
        sx, sy = polar(cx, cy, 7.3, a0)
        ex, ey = polar(cx, cy, 7.3, a1)
        large = 1 if a1 - a0 > 180 else 0
        out.append(shell(f"M{fmt(cx)} {fmt(cy)}L{fmt(sx)} {fmt(sy)}A7.3 7.3 0 {large} 1 {fmt(ex)} {fmt(ey)}Z"))
    return out


@icon("nutrition-label", CAT, "A tall food panel with a bold heading bar and three rows of values.",
      tags=["nutrition facts", "food label", "ingredients", "calories", "diet", "packaging"], aliases=["nutrition-facts-label"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 19, L(S, 1, 3))), sq(7.5, 5.2, 9, 3), detail(seg(8, 12, 16, 12)), detail(seg(8, 15.2, 16, 15.2)),
            detail(seg(8, 18.4, 13, 18.4))]


@icon("protein-powder", CAT, "A tub with a screw lid and a measuring scoop standing beside it.",
      tags=["whey", "supplement tub", "protein shake", "gym", "bodybuilding", "powder"], aliases=["whey-protein"])
def _(S):
    return [shell(rect(2.5, 3.5, 12, 4, L(S, 0.8, 2))), shell(rect(3.5, 9.5, 10, 12, L(S, 0.8, 2.4))), detail(seg(6, 14.5, 11, 14.5)),
            shell(poly([(16.5, 15), (22, 15), (21, 20), (17.5, 20)], closed=True, r=S.r)), line(seg(19.25, 15, 19.25, 8))]


@icon("protein-bar", CAT, "A wrapped snack bar with crimped fins at both ends and a stripe across the wrapper.",
      tags=["energy bar", "snack bar", "granola bar", "gym snack", "wrapper", "nutrition"], aliases=["snack-bar"])
def _(S):
    return [shell(rect(6.5, 6.5, 11, 11, L(S, 0.8, 2.4))),
            shell(poly([(6.5, 9), (2.5, 7), (2.5, 17), (6.5, 15)], closed=True, r=S.r)),
            shell(poly([(17.5, 9), (21.5, 7), (21.5, 17), (17.5, 15)], closed=True, r=S.r)),
            detail(seg(9.5, 10.5, 14.5, 10.5)), detail(seg(9.5, 13.5, 14.5, 13.5))]


@icon("energy-gel", CAT, "A small gel sachet with a serrated tear-off top and a drop mark on the front.",
      tags=["gel pack", "sports nutrition", "runner fuel", "endurance", "sachet", "carb gel"], aliases=["gel-sachet"])
def _(S):
    body = poly([(6.5, 3), (8.5, 5), (10.5, 3), (12.5, 5), (14.5, 3), (16.5, 5), (17.5, 3), (17.5, 21), (6.5, 21)], closed=True, r=S.r * 0.5)
    drop = "M12 10L8.8 14.6A3.6 3.6 0 1 0 15.2 14.6Z"
    return [shell(body), Part("dot", drop)]


@icon("fish-oil-capsule", CAT, "A clear oval softgel capsule with a small fish silhouette inside.",
      tags=["omega 3", "softgel", "supplement", "cod liver oil", "dha", "fish oil"], aliases=["omega-3"])
def _(S):
    fish = path_to_d(U(P(ellipse(10.8, 12, 3.8, 2.4)), P(poly([(14, 12), (17.5, 9.5), (17.5, 14.5)], closed=True))))
    return [shell(rect(2, 5.5, 20, 13, L(S, 2.5, 6.5))), Part("dot", fish)]


@icon("vitamins", CAT, "A round vitamin tablet marked with a letter C beside a slanted capsule.",
      tags=["supplements", "multivitamin", "vitamin c", "pills", "nutrition", "health"], aliases=["vitamin-pills"])
def _(S):
    m = (0.7071, 0.7071, -0.7071, 0.7071, 17, 7)
    return [shell(rect(2.5, 11.5, 10, 10, L(S, 2, 5))), line(arc(7.5, 16.5, 2, 45, 315)),
            shell(xf(rect(-3, -6.2, 6, 12.4, L(S, 2, 3)), m)), detail(xf(seg(-3, 0, 3, 0), m))]


@icon("probiotic", CAT, "A capsule pulled open into two halves with small rod-shaped bacteria spilling upward.",
      tags=["gut health", "good bacteria", "lactobacillus", "supplement", "digestive", "microbiome"], aliases=["probiotics"])
def _(S):
    out = [shell(L(S, "M10 13.5H5Q2.5 13.5 2.5 16.2V17.8Q2.5 20.5 5 20.5H10Z", "M10 13.5H5.5C3.7 13.5 2.5 14.6 2.5 16.2V17.8C2.5 19.4 3.7 20.5 5.5 20.5H10Z")),
           shell(L(S, "M14 13.5H19Q21.5 13.5 21.5 16.2V17.8Q21.5 20.5 19 20.5H14Z", "M14 13.5H18.5C20.3 13.5 21.5 14.6 21.5 16.2V17.8C21.5 19.4 20.3 20.5 18.5 20.5H14Z"))]
    for (cx, cy, a) in [(12, 6.5, 90), (7.5, 8.5, 35), (16.5, 8.5, -35)]:
        out.append(solid(xf(rect(-2.5, -1, 5, 2, 1), (math.cos(math.radians(a)), math.sin(math.radians(a)), -math.sin(math.radians(a)), math.cos(math.radians(a)), cx, cy))))
    return out


@icon("meal-prep", CAT, "Three stacked food containers with lids, each divided into compartments.",
      tags=["lunch boxes", "bento", "food containers", "batch cooking", "diet planning", "tupperware"], aliases=["meal-prep-containers"])
def _(S):
    out = []
    for y in (2.5, 9.2, 15.9):
        out += [shell(rect(3, y, 18, 5.6, L(S, 0.8, 2.6))), detail(seg(9.5, y + 0.8, 9.5, y + 4.8))]
    return out


@icon("food-diary", CAT, "An open notebook with an apple on the left page and lines of writing on the right page.",
      tags=["food journal", "meal log", "calorie tracking", "diet", "nutrition notebook", "eating habits"], aliases=["food-journal"])
def _(S):
    return [shell(rect(2.5, 3.5, 19, 17, L(S, 1, 3))), detail(seg(12, 3.5, 12, 20.5)),
            dot(7.2, 13, 2.4), line(seg(7.2, 8.7, 7.2, 10.6)), detail(seg(14.8, 8, 18.8, 8)), detail(seg(14.8, 11.5, 18.8, 11.5)), detail(seg(14.8, 15, 18.8, 15))]


@icon("water-intake", CAT, "A tall glass partly filled with water, with level marks on the side and a water drop beside it.",
      tags=["hydration", "drink water", "water tracker", "glass of water", "daily water", "healthy habits"], aliases=["hydration-tracker"])
def _(S):
    drop = "M19 8.5L16.3 12.6A3.2 3.2 0 1 0 21.7 12.6Z"
    return [shell(poly([(2.5, 3), (14.5, 3), (13.2, 21), (3.8, 21)], closed=True, r=S.r)), detail(seg(4, 9.5, 13.2, 9.5)),
            detail(seg(5.8, 13.5, 8.2, 13.5)), detail(seg(5.8, 17.2, 8.2, 17.2)), solid(drop)]


@icon("smoothie", CAT, "A tall glass of thick smoothie with a domed lid and a straw sticking out.",
      tags=["shake", "juice", "blended drink", "fruit drink", "healthy", "takeaway drink"], aliases=["smoothie-cup"])
def _(S):
    return [shell(poly([(6, 9), (18, 9), (16.6, 21.5), (7.4, 21.5)], closed=True, r=S.r)),
            shell(L(S, "M5.5 9C5.5 5.5 8 4 12 4S18.5 5.5 18.5 9Z", "M5.5 9C5.5 5.5 8 4 12 4S18.5 5.5 18.5 9Z")),
            line(poly([(13.5, 4.5), (16, 2.2), (19.5, 2.2)], r=0)), detail(seg(8, 14, 16, 14))]


@icon("acai-bowl", CAT, "A bowl heaped with round berries and fruit toppings on top.",
      tags=["smoothie bowl", "breakfast bowl", "granola", "fruit bowl", "superfood", "berries"], aliases=["smoothie-bowl"])
def _(S):
    bowl = L(S, "M3 11.5H21C21 17 17 21 12 21S3 17 3 11.5Z", "M4 11.5H20Q21 11.5 21 12.5C20.5 17.5 17 21 12 21S3.5 17.5 3 12.5Q3 11.5 4 11.5Z")
    return [shell(bowl), dot(7.5, 8.4, 2.1), dot(12, 7.4, 2.1), dot(16.5, 8.4, 2.1), dot(9.8, 4, 1.6), dot(14.5, 3.7, 1.6)]


@icon("overnight-oats", CAT, "A glass jar of layered oats and fruit with a spoon sticking out of the top.",
      tags=["oatmeal", "mason jar", "breakfast", "meal prep", "layered jar", "healthy breakfast"], aliases=["oats-jar"])
def _(S):
    return [shell(poly([(7, 8), (17, 8), (18, 10), (18, 21.5), (6, 21.5), (6, 10)], closed=True, r=S.r)),
            detail(seg(6.5, 14, 17.5, 14)), detail(seg(6.5, 18, 17.5, 18)), line(seg(11, 12, 16.5, 3.5)), dot(17.2, 3, 2)]


@icon("intermittent-fasting", CAT, "An empty plate with clock hands in the middle and a fork beside it.",
      tags=["fasting", "eating window", "16 8 diet", "meal timing", "time restricted eating", "diet"], aliases=["fasting-clock"])
def _(S):
    return [shell(circle(14.5, 12, 7.8)), detail(poly([(14.5, 7.5), (14.5, 12), (17.5, 12)], r=S.r)),
            line("M2.5 3V7A1.5 1.5 0 0 0 5.5 7V3"), line(seg(4, 8.5, 4, 21.5))]


@icon("vegetarian-symbol", CAT, "A square outline with a solid circle in the middle, the mark used on vegetarian food.",
      tags=["veg", "vegetarian", "food label", "plant based", "diet", "meat free"], aliases=["veg-mark"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), dot(12, 12, 5.2)]


@icon("bmi-chart", CAT, "A horizontal bar split into four segments with a pointer above one of them.",
      tags=["body mass index", "weight range", "healthy weight", "obesity scale", "gauge", "bmi"], aliases=["bmi-scale"])
def _(S):
    return [shell(rect(2, 14.5, 20, 6, L(S, 1, 3))), detail(seg(7, 15.5, 7, 19.5)), detail(seg(12, 15.5, 12, 19.5)), detail(seg(17, 15.5, 17, 19.5)),
            solid(poly([(14.5, 11.5), (11.5, 6), (17.5, 6)], closed=True, r=S.r * 0.4))]


@icon("glucose-meter", CAT, "A handheld blood sugar meter with a screen, a button and a test strip sticking out of the top.",
      tags=["blood sugar", "diabetes", "glucometer", "blood test", "finger prick", "monitor"], aliases=["glucometer"])
def _(S):
    drop = "M18.5 1.8L16.8 4.4A2 2 0 1 0 20.2 4.4Z"
    return [shell(rect(4.5, 8, 15, 14, L(S, 1.5, 4))), detail(rect(8, 11, 8, 4.5, 0)), dot(12, 19, 1.2), line(seg(12, 8, 12, 3)), solid(drop)]


@icon("counting-sheep", CAT, "A fluffy sheep leaping over a low fence with a small Z above it.",
      tags=["insomnia", "can't sleep", "bedtime", "fall asleep", "sleep aid", "sheep"], aliases=["sheep-jump"])
def _(S):
    wool = path_to_d(U(*[P(circle(x, y, 3.2)) for x, y in [(7.5, 10.5), (11, 8.5), (14.5, 10.5), (11, 12.8)]]))
    headp = L(S, poly([(17, 8.5), (20.5, 9), (21, 12), (18.5, 13.5), (16.5, 12)], closed=True), "M17 8.8C19 7.8 21.5 9.5 21 11.8C20.7 13 19 14 17.5 13C16.5 12 16.2 9.8 17 8.8Z")
    return [shell(wool), shell(headp), line(seg(8, 14, 6.5, 17)), line(seg(13.5, 15, 15, 17.5)),
            line(seg(2, 21.5, 22, 21.5)), line(seg(6, 18.5, 6, 21.5)), line(seg(18, 18.5, 18, 21.5)), zzz(3, 3, 0.9)]


@icon("sleeping-person", CAT, "A person asleep in bed under a blanket with the head on a pillow and a Z rising.",
      tags=["sleep", "bedtime", "resting", "nap", "bed", "asleep"], aliases=["asleep"])
def _(S):
    return [shell(rect(2, 15, 20, 4.5, L(S, 0.8, 2))), line(seg(2, 10, 2, 21.5)), line(seg(22, 13, 22, 21.5)),
            hd(6.2, 11.8, 2.2), shell(poly([(9.5, 15), (10.5, 10.5), (21, 10.5), (21, 15)], closed=True, r=S.r)), zzz(12, 2.5, 0.9)]


@icon("snoring", CAT, "Side view of a head with a closed eye and open mouth, with sound waves coming out.",
      tags=["snore", "loud breathing", "sleep apnea", "noisy sleep", "sleeping noise", "zzz"], aliases=["snorer"])
def _(S):
    return [shell(head(S, 0.8, 0.5, 2.5)), detail(seg(10.3, 8, 12.8, 8)), dot(14.8, 12.3, 0.9),
            line(arc(16.8, 11.5, 3.2, -45, 45)), line(arc(16.8, 11.5, 5.8, -42, 42))]


def bolt(x, y, k=1.0):
    pts = [(1.5, 0), (-2, 5), (0.3, 5), (-1.3, 9.5), (3, 3.5), (0.7, 3.5), (2.8, 0)]
    return poly([(x + k * px, y + k * py) for px, py in pts], closed=True)


def cloud(x, y, k=1.0):
    """A small cloud whose bottom-left corner sits at (x, y)."""
    return tf("M0 0H9A2.6 2.6 0 0 0 9.3 -5.2A3.8 3.8 0 0 0 2.2 -6A2.7 2.7 0 0 0 0 0Z", k, x, y)


# =========================================================================== sleep

@icon("weighted-blanket", CAT, "A quilted blanket with a grid of stitched pockets and one corner folded over.",
      tags=["gravity blanket", "anxiety blanket", "heavy blanket", "sleep aid", "quilt", "bedding"], aliases=["gravity-blanket"])
def _(S):
    return [shell(rect(2.5, 4.5, 19, 15, L(S, 1, 3))), detail(seg(8.8, 4.5, 8.8, 19.5)), detail(seg(15.2, 4.5, 15.2, 19.5)),
            detail(seg(2.5, 9.5, 21.5, 9.5)), detail(seg(2.5, 14.5, 21.5, 14.5))]


@icon("sleep-stages", CAT, "A stepped line graph dropping through three sleep depths with a crescent moon above.",
      tags=["sleep cycle", "rem sleep", "deep sleep", "sleep tracking", "hypnogram", "sleep tracker"], aliases=["hypnogram"])
def _(S):
    moon = path_to_d(D(P(circle(18.5, 5.3, 3.4)), P(circle(20.2, 4.2, 2.9))))
    return [line(poly([(2, 10.5), (6, 10.5), (6, 15), (10, 15), (10, 20), (14.5, 20), (14.5, 15), (18.5, 15), (18.5, 11.5), (22, 11.5)], r=S.r)), solid(moon)]


@icon("circadian-rhythm", CAT, "A sun and a crescent moon inside a ring of two arrows chasing each other around.",
      tags=["body clock", "sleep wake cycle", "day and night", "24 hour cycle", "chronobiology", "jet lag"], aliases=["body-clock"])
def _(S):
    def head(deg, rr=9):
        return polar(12, 12, rr, deg)
    out = [line(arc(12, 12, 9, -160, -20)), line(arc(12, 12, 9, 20, 160))]
    # arrow heads at the arc ends (clockwise on the top arc, clockwise on the bottom arc)
    for a, sgn in [(-20, 1), (160, 1)]:
        tx, ty = head(a)
        tan = math.radians(a + 90)
        bx, by = math.cos(tan), math.sin(tan)
        nx, ny = math.cos(math.radians(a)), math.sin(math.radians(a))
        out.append(line(poly([(tx - bx * 2.6 + nx * 2.4, ty - by * 2.6 + ny * 2.4), (tx + bx * 0.6, ty + by * 0.6), (tx - bx * 2.6 - nx * 2.4, ty - by * 2.6 - ny * 2.4)], r=0)))
    moon = path_to_d(D(P(circle(15.8, 12, 2.9)), P(circle(17.2, 11.2, 2.5))))
    out += [dot(8.2, 12, 1.7), solid(moon)]
    return out


@icon("cpap-mask", CAT, "Front view of a face wearing a nose mask with straps to the sides and a breathing hose running down.",
      tags=["sleep apnea", "cpap", "breathing machine", "nasal mask", "sleep therapy", "respiratory"], aliases=["sleep-apnea-mask"])
def _(S):
    face = poly([(5.5, 8), (7, 3.5), (17, 3.5), (18.5, 8), (17.5, 14), (14, 18), (10, 18), (6.5, 14)], closed=True, r=S.r + 1.5)
    return [shell(face), Part("dot", poly([(12, 7.5), (16, 14.5), (8, 14.5)], closed=True, r=S.r * 0.5)), detail(seg(5.5, 11.5, 9, 11.5)), detail(seg(18.5, 11.5, 15, 11.5)),
            line(seg(12, 14.5, 12, 21.5))]


@icon("sleepwalking", CAT, "Side view of a figure walking with both arms stretched out in front and a Z above.",
      tags=["somnambulism", "night walking", "parasomnia", "sleep disorder", "zombie walk", "sleep"], aliases=["somnambulism"])
def _(S):
    return [hd(8.5, 5.5), line(poly([(8.5, 9.5), (9.5, 15)], r=0)), pl(S, [(9.5, 15), (7, 21.5)]), pl(S, [(9.5, 15), (13.5, 21.5)]),
            line(seg(8.8, 10.5, 17.5, 9)), line(seg(9, 12.7, 17, 13.2)), zzz(15, 1.8, 0.8)]


@icon("yawning-face", CAT, "A round sleepy face with closed eyes and a wide open oval mouth.",
      tags=["yawn", "tired", "sleepy", "bored", "drowsy", "fatigue"], aliases=["yawn"])
def _(S):
    return [shell(rect(3, 5, 17, 17, L(S, 5, 8.5))), detail(arc(8.2, 11.5, 1.9, 20, 160)), detail(arc(15, 11.5, 1.9, 20, 160)),
            Part("dot", ellipse(11.5, 17, 2.4, 2.6)), zzz(18, 1.5, 0.8)]


# =========================================================================== mind

@icon("stress", CAT, "Side view of a head with a lightning bolt inside and short tension lines around the crown.",
      tags=["tension", "anxiety", "pressure", "overwhelmed", "mental health", "headache"], aliases=["stressed"])
def _(S):
    return [shell(head(S, 0.82, 3.4, 2.8)), Part("dot", bolt(10.9, 7.3, 0.8)),
            line(seg(4, 3, 6.2, 5.2)), line(seg(9, 1.5, 9.6, 4.2)), line(seg(14.5, 1.8, 13.5, 4.2))]


@icon("burnout", CAT, "Side view of a head with a nearly empty battery inside it.",
      tags=["exhaustion", "drained", "work fatigue", "low energy", "mental health", "tired"], aliases=["exhausted"])
def _(S):
    return [shell(head(S)), detail(rect(6.8, 7.5, 8, 5.5, 0)), line(seg(15.8, 9, 15.8, 11.5)), Part("dot", rect(8, 8.8, 1.8, 2.9))]


@icon("depression", CAT, "Side view of a head with a small rain cloud beside it and drops falling.",
      tags=["low mood", "sadness", "mental health", "gloomy", "blues", "mood disorder"], aliases=["low-mood"])
def _(S):
    return [shell(head(S, 0.78, 0, 4)), shell(cloud(13, 8.6, 0.85)), line(seg(15.5, 10.8, 15.5, 12.4)), line(seg(18.5, 10.8, 18.5, 12.4)),
            line(seg(21, 10.8, 21, 12.4))]


@icon("brain-fog", CAT, "Side view of a head with a hazy cloud sitting in the brain area.",
      tags=["cloudy thinking", "forgetful", "unclear mind", "long covid", "cognitive", "mental fatigue"], aliases=["mental-fog"])
def _(S):
    return [shell(head(S)), detail(cloud(6.3, 14, 1.0))]


@icon("overthinking", CAT, "Side view of a head with a tight spiral of looping thought rising out of the top.",
      tags=["racing thoughts", "rumination", "anxiety", "mental loop", "worry", "mind"], aliases=["rumination"])
def _(S):
    pts = []
    for i in range(0, 41):
        t = i / 40
        pts.append(polar(16.5, 7, 0.9 + 4.3 * t, -90 + t * 720))
    return [shell(head(S, 0.8, 0.2, 4.6)), line(poly(pts, r=0))]


@icon("calm-mind", CAT, "Side view of a head with three gentle wave lines inside it.",
      tags=["peace", "tranquil", "relaxed", "serenity", "mindfulness", "meditation"], aliases=["peaceful-mind"])
def _(S):
    out = [shell(head(S))]
    for y in (6.5, 10, 13.5):
        out.append(detail(f"M6.5 {y}C8 {y - 1.6} 9.5 {y - 1.6} 11 {y}S14 {y + 1.6} 15.5 {y}"))
    return out


@icon("focus-mind", CAT, "Side view of a head with a bullseye target inside it.",
      tags=["concentration", "attention", "target", "goal", "mindfulness", "productivity"], aliases=["concentration"])
def _(S):
    return [shell(head(S)), detail(circle(11, 9.6, 3.4)), dot(11, 9.6, 1)]


@icon("growth-mindset", CAT, "Side view of a head with a young sprout with two leaves growing from the crown.",
      tags=["learning", "personal growth", "development", "potential", "positive thinking", "plant"], aliases=["sprout-mind"])
def _(S):
    leaf_l = "M12 5.8C12 3.2 9.8 2.2 7.8 2.6C7.8 4.8 9.4 6 12 5.8Z"
    leaf_r = "M12 5.8C12 3.2 14.2 2.2 16.2 2.6C16.2 4.8 14.6 6 12 5.8Z"
    return [shell(head(S, 0.8, 2.8, 5.2)), line(seg(12, 5, 12, 8.8)), solid(leaf_l), solid(leaf_r)]


@icon("self-hug", CAT, "Front view of a person with both arms crossed over the chest and a small heart beside them.",
      tags=["self care", "self love", "comfort", "self compassion", "embrace", "wellbeing"], aliases=["self-love"])
def _(S):
    body = poly([(5.5, 21), (6, 12.5), (8.5, 10), (15.5, 10), (18, 12.5), (18.5, 21)], closed=True, r=S.r + 1)
    return [hd(11, 5.5, 2.5), shell(body), detail(seg(7.5, 13.5, 16.5, 17.5)), detail(seg(16.5, 13.5, 7.5, 17.5)),
            solid("M19.5 9C19.5 9 16.4 7 16.4 5C16.4 3.3 18.5 2.7 19.5 4.2C20.5 2.7 22.6 3.3 22.6 5C22.6 7 19.5 9 19.5 9Z")]


@icon("therapy-couch", CAT, "A long couch with a raised head end and a simple chair beside it.",
      tags=["psychotherapy", "counselling", "psychiatrist", "lie down", "mental health", "session"], aliases=["psychiatrist-couch"])
def _(S):
    return [shell(poly([(2, 13), (2, 8), (5.5, 8), (5.5, 11), (14.5, 11), (14.5, 17), (2, 17)], closed=True, r=S.r)),
            line(seg(3, 17, 3, 21)), line(seg(13.5, 17, 13.5, 21)),
            line(poly([(20.5, 7), (20.5, 15), (17.5, 15)], r=S.r)), line(seg(17.5, 15, 17.5, 21)), line(seg(20.5, 15, 20.5, 21))]


@icon("therapy-session", CAT, "Two seated people facing each other with a speech bubble between them.",
      tags=["counselling", "talk therapy", "psychologist", "conversation", "mental health", "appointment"], aliases=["counselling-session"])
def _(S):
    out = [hd(5, 10.5), line(seg(5, 14, 5, 18)), pl(S, [(5, 18), (9.5, 18), (9.5, 21.5)]), line(seg(3, 21.5, 3, 18.5)),
           hd(19, 10.5), line(seg(19, 14, 19, 18)), pl(S, [(19, 18), (14.5, 18), (14.5, 21.5)]), line(seg(21, 21.5, 21, 18.5))]
    out.append(solid(poly([(8.5, 2.5), (15.5, 2.5), (15.5, 8), (12.5, 8), (10, 10), (10, 8), (8.5, 8)], closed=True, r=0)))
    return out


@icon("support-group", CAT, "Top view of a ring of six people around a small heart in the middle.",
      tags=["group therapy", "community", "circle", "peer support", "mental health", "meeting"], aliases=["group-therapy"])
def _(S):
    ringpts = regular(12, 12, 8.4, 6)
    out = [line(poly(regular(12, 12, 8.4, 6, start=-60), closed=True, r=S.r))]
    for (x, y) in ringpts:
        out.append(Part("dot", circle(x, y, 2.3)))
    out.append(solid("M12 15C12 15 8.6 12.7 8.6 10.6C8.6 8.9 10.7 8.4 12 9.8C13.3 8.4 15.4 8.9 15.4 10.6C15.4 12.7 12 15 12 15Z"))
    return out


@icon("crisis-helpline", CAT, "A telephone handset with a heart rising beside it.",
      tags=["hotline", "emergency call", "suicide prevention", "mental health support", "lifeline", "call for help"], aliases=["hotline"])
def _(S):
    curve = "M5 8.5C5 15 9.5 19 16 19"
    hand = path_to_d(U(ST(curve, 4.2, S.cap, S.join), P(rect(2.1, 4.1, 5.8, 5.8, L(S, 0.8, 2.9))), P(rect(14.1, 16.1, 5.8, 5.8, L(S, 0.8, 2.9)))))
    return [shell(hand), solid("M17.5 10C17.5 10 13.8 7.6 13.8 5.2C13.8 3.2 16.3 2.6 17.5 4.4C18.7 2.6 21.2 3.2 21.2 5.2C21.2 7.6 17.5 10 17.5 10Z")]


@icon("mood-tracker", CAT, "A row of three faces going from sad to neutral to happy with a check mark under the last one.",
      tags=["mood log", "feelings", "emotion diary", "daily check in", "mental health", "mood journal"], aliases=["mood-log"])
def _(S):
    out = []
    for x in (4.5, 12, 19.5):
        out.append(shell(rect(x - 3.5, 4, 7, 7, L(S, 2, 3.5))))
    out += [detail("M2.8 9.2Q4.5 7.8 6.2 9.2"), detail(seg(10.3, 8.5, 13.7, 8.5)), detail("M17.8 7.5Q19.5 9.2 21.2 7.5"),
            line(poly([(17, 17), (19, 19.5), (22, 15.5)], r=S.r))]
    return out


@icon("gratitude-journal", CAT, "A closed notebook with a heart on the cover and a stitched spine.",
      tags=["thankful", "diary", "appreciation", "writing", "self care", "notebook"], aliases=["thankfulness-journal"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 19, L(S, 1, 3))), detail(seg(8.5, 2.5, 8.5, 21.5)),
            Part("dot", "M14 17C14 17 10.8 14.8 10.8 12.6C10.8 10.9 13 10.3 14 11.8C15 10.3 17.2 10.9 17.2 12.6C17.2 14.8 14 17 14 17Z")]


@icon("breathwork", CAT, "A pair of lungs with the windpipe on top and curved lines of air flowing in from above.",
      tags=["breathing exercise", "deep breath", "pranayama", "inhale", "lungs", "mindful breathing"], aliases=["breathing-exercise"])
def _(S):
    lung = L(S, "M10 10C7 10 4 13.5 3.5 17C3.2 19.5 4.8 21 7 20.6L9.5 20.2C10.3 20 10.6 19.5 10.6 18.8V10.8Z",
             "M10 10C7 10 4 13.5 3.5 17C3.2 19.5 4.8 21 7 20.6L9.5 20.2C10.3 20 10.6 19.5 10.6 18.8V11C10.6 10.4 10.4 10 10 10Z")
    mir = xf(lung, (-1, 0, 0, 1, 24, 0))
    return [shell(lung), shell(mir), line(seg(12, 6, 12, 12)), line(poly([(9.8, 8.4), (12, 10.6), (14.2, 8.4)], r=S.r)),
            line("M2.5 6.5Q5 3.5 8.5 4.5"), line("M21.5 6.5Q19 3.5 15.5 4.5")]


@icon("box-breathing", CAT, "A square path with an arrow on each side going around and a dot at the starting corner.",
      tags=["square breathing", "4 4 4 4", "breath counting", "calming", "anxiety relief", "breathwork"], aliases=["square-breathing"])
def _(S):
    return [line(rect(5, 5, 14, 14, S.R)),
            solid("M10.8 2.8L14.6 5L10.8 7.2Z"), solid("M16.8 10.4L19 14.2L21.2 10.4Z"),
            solid("M13.2 16.8L9.4 19L13.2 21.2Z"), solid("M7.2 13.6L5 9.8L2.8 13.6Z"), dot(5, 5, 2)]


def scale(S, left, right):
    """Balance scale frame; left/right are lists of parts drawn above each pan."""
    out = [line(seg(12, 3, 12, 20)), line(seg(8, 21, 16, 21)), line(seg(3.5, 4.5, 20.5, 4.5)),
           line(poly([(3.5, 4.5), (1.8, 12.5)], r=0)), line(poly([(3.5, 4.5), (8.5, 12.5)], r=0)),
           line(poly([(20.5, 4.5), (15.5, 12.5)], r=0)), line(poly([(20.5, 4.5), (22.2, 12.5)], r=0)),
           line(poly([(1.5, 12.5), (4, 15.5), (6, 15.5), (8.8, 12.5)], r=S.r)),
           line(poly([(15.2, 12.5), (18, 15.5), (20, 15.5), (22.5, 12.5)], r=S.r))]
    return out + left + right


@icon("emotional-balance", CAT, "A balance scale with a heart on one pan and a cluster-shaped brain on the other.",
      tags=["heart and mind", "feelings and logic", "emotional intelligence", "mental health", "equilibrium", "wellbeing"], aliases=["heart-mind-balance"])
def _(S):
    heart = solid("M5.2 12C5.2 12 2.8 10.3 2.8 8.7C2.8 7.5 4.3 7 5.2 8.2C6.1 7 7.6 7.5 7.6 8.7C7.6 10.3 5.2 12 5.2 12Z")
    brain = solid(path_to_d(U(*[P(circle(x, y, 1.45)) for x, y in [(17.6, 10.6), (20.2, 10.6), (18.9, 8.6), (18.9, 11)]])))
    return scale(S, [heart], [brain])


@icon("work-life-balance", CAT, "A balance scale with a briefcase on one pan and a house on the other.",
      tags=["work and home", "burnout prevention", "career and family", "equilibrium", "wellbeing", "lifestyle"], aliases=["life-balance"])
def _(S):
    case = solid(rect(3, 8.3, 5.4, 3.6, 0.5))
    handle = line(poly([(4.7, 8.3), (4.7, 7), (6.7, 7), (6.7, 8.3)], r=0))
    house = solid(poly([(15.2, 12), (15.2, 9.5), (18.8, 6.8), (22.4, 9.5), (22.4, 12)], closed=True))
    return scale(S, [case, handle], [house])


@icon("social-battery", CAT, "A battery with two small people inside and the left part filled to show remaining energy.",
      tags=["introvert", "energy level", "socializing", "recharge", "people drain", "social fatigue"], aliases=["social-energy"])
def _(S):
    return [shell(rect(2, 6.5, 18, 11, L(S, 1.5, 3.5))), solid(rect(20.8, 10, 1.4, 4, 0.4)), Part("dot", rect(4.5, 9, 3.5, 6, 0.6)),
            dot(12.6, 10, 1.1), dot(16.6, 10, 1.1), Part("dot", rect(11.4, 11.8, 2.4, 3, 1)), Part("dot", rect(15.4, 11.8, 2.4, 3, 1))]


@icon("hand-on-shoulder", CAT, "Two people standing side by side, one resting a hand on the other's shoulder.",
      tags=["comfort", "support", "empathy", "reassurance", "consoling", "friendship"], aliases=["comforting-touch"])
def _(S):
    return [hd(6.5, 5.5), line(seg(6.5, 9, 6.5, 15)), pl(S, [(6.5, 15), (4, 21.5)]), pl(S, [(6.5, 15), (9, 21.5)]),
            pl(S, [(6.5, 10.5), (12, 13), (16.5, 10)]),
            hd(17.5, 7), line(seg(17.5, 10.5, 17.5, 15.5)), pl(S, [(17.5, 15.5), (15, 21.5)]), pl(S, [(17.5, 15.5), (20, 21.5)])]


@icon("safe-space", CAT, "A simple house outline with a heart in the middle.",
      tags=["sanctuary", "refuge", "home", "comfort", "shelter", "mental health"], aliases=["safe-haven"])
def _(S):
    return [shell(poly([(3, 11), (12, 3), (21, 11), (21, 21), (3, 21)], closed=True, r=S.r)),
            Part("dot", "M12 19C12 19 7.6 16.2 7.6 13.6C7.6 11.6 10.4 11 12 12.8C13.6 11 16.4 11.6 16.4 13.6C16.4 16.2 12 19 12 19Z")]


@icon("enso-circle", CAT, "A single brush-stroke circle left open, thick where the brush lands and tapering to a thin tail.",
      tags=["zen circle", "japanese calligraphy", "zen buddhism", "brush stroke", "minimalism", "mindfulness"], aliases=["zen-circle"])
def _(S):
    outer, inner = [], []
    n = 36
    for i in range(n + 1):
        t = i / n
        a = -60 + t * 300
        w = 4.4 - 3.2 * t ** 0.8
        outer.append(polar(12, 12, 8.4 + w / 2, a))
        inner.append(polar(12, 12, 8.4 - w / 2, a))
    return [shell(poly(outer + inner[::-1], closed=True, r=S.r * 0.4))]


@icon("mandala", CAT, "A round flower-like pattern: a ring of eight petals with a smaller ring and a dot at the centre.",
      tags=["sacred geometry", "buddhist art", "colouring", "circular pattern", "meditation", "hindu art"], aliases=["mandala-pattern"])
def _(S):
    pts = []
    for i in range(16):
        pts.append(polar(12, 12, 9.2 if i % 2 == 0 else 6.2, -90 + i * 22.5))
    inner = [polar(12, 12, 3.6 if i % 2 == 0 else 2.4, -67.5 + i * 45) for i in range(8)]
    return [line(poly(pts, closed=True, r=S.r)), line(poly(regular(12, 12, 3.6, 8, start=-67.5), closed=True, r=S.r * 0.5)), dot(12, 12, 1.1)]


@icon("chakras", CAT, "A seated meditating figure with seven small dots running down the centre line from head to base.",
      tags=["energy centers", "yoga", "spiritual", "kundalini", "aura", "meditation"], aliases=["seven-chakras"])
def _(S):
    out = [shell(poly(regular(12, 5, 3, 8), closed=True, r=S.r)), dot(12, 5, 0.8)]
    for y in (9.3, 11.5, 13.7, 15.9, 18.1, 20.3):
        out.append(dot(12, y, 0.85))
    out += [line(poly([(8.2, 9), (6.8, 14), (3, 19.5)], r=S.r)), line(poly([(15.8, 9), (17.2, 14), (21, 19.5)], r=S.r))]
    return out


def pine(x, top, bottom):
    h = bottom - top
    return poly([(x, top), (x + 2.6, top + h * 0.45), (x + 1.4, top + h * 0.45), (x + 3.3, bottom), (x - 3.3, bottom), (x - 1.4, top + h * 0.45), (x - 2.6, top + h * 0.45)], closed=True)


@icon("forest-bathing", CAT, "A person standing with arms open between two tall pine trees.",
      tags=["shinrin yoku", "nature therapy", "woods", "outdoors", "walk in nature", "tree hugging"], aliases=["shinrin-yoku"])
def _(S):
    return [shell(pine(4.6, 3, 17)), shell(pine(19.4, 3, 17)), line(seg(4.6, 17, 4.6, 21)), line(seg(19.4, 17, 19.4, 21)),
            hd(12, 6), line(seg(12, 9.5, 12, 15)), pl(S, [(12, 15), (10, 21.5)]), pl(S, [(12, 15), (14, 21.5)]),
            pl(S, [(8.8, 8), (12, 11), (15.2, 8)])]


@icon("sound-bath", CAT, "A person lying on the floor with stacked curved sound waves rippling over them.",
      tags=["sound healing", "gong bath", "relaxation", "vibration", "meditation", "restorative"], aliases=["gong-bath"])
def _(S):
    return [hd(4.5, 16.5), pl(S, [(8, 17.5), (21, 17.5)]), line(seg(2, 21.5, 22, 21.5)),
            line("M3 5.5Q12 1.5 21 5.5"), line("M5.5 10.5Q12 7.5 18.5 10.5")]


@icon("guided-meditation", CAT, "A cross-legged figure wearing headphones, with the hands resting on the knees.",
      tags=["meditation app", "audio meditation", "headphones", "mindfulness", "calm", "listening"], aliases=["meditation-audio"])
def _(S):
    return [hd(12, 7), line(arc(12, 7, 4.4, 180, 360)), sq(6.6, 6, 1.8, 3.6), sq(15.6, 6, 1.8, 3.6),
            line(seg(12, 10.5, 12, 16)), pl(S, [(12, 11.5), (7.5, 14.5), (7, 17)]), pl(S, [(12, 11.5), (16.5, 14.5), (17, 17)]),
            pl(S, [(3, 20), (9, 17.5), (15, 17.5), (21, 20)])]


@icon("relaxing-bath", CAT, "A bathtub on small feet with a head resting above the bubbles and a lit candle on the rim.",
      tags=["bubble bath", "spa", "soak", "self care", "unwind", "bathtub"])
def _(S):
    return [shell(poly([(2, 12.5), (22, 12.5), (20.5, 19), (3.5, 19)], closed=True, r=S.r)), line(seg(6, 19, 6, 21.5)), line(seg(18, 19, 18, 21.5)),
            hd(14.5, 8.2, 2.1), dot(7, 9.4, 1.2), dot(9.8, 7.4, 1.2), dot(10.2, 10.4, 0.9),
            sq(19.5, 8, 2.2, 4), solid("M20.6 3.6C20.6 3.6 19.7 4.8 19.7 5.5A0.9 0.9 0 0 0 21.5 5.5C21.5 4.8 20.6 3.6 20.6 3.6Z")]


@icon("scented-candle", CAT, "A candle in a round glass jar with a lid lying beside it and a curl of scent above the flame.",
      tags=["aromatherapy", "fragrance", "home fragrance", "relaxation", "wax", "cozy"])
def _(S):
    return [shell(rect(3, 11, 12, 10, L(S, 1.5, 4))), detail(seg(5.5, 16, 12.5, 16)),
            shell(rect(17, 17, 5, 4, L(S, 0.8, 1.8))),
            solid("M9 4.8C9 4.8 7.4 6.6 7.4 7.8A1.6 1.6 0 0 0 10.6 7.8C10.6 6.6 9 4.8 9 4.8Z"),
            line("M14 9C12.6 7.6 15.4 6.2 14 3.4")]


@icon("cozy-blanket", CAT, "A person wrapped in a thick blanket holding a steaming mug.",
      tags=["hygge", "warm", "winter", "comfort", "hot drink", "relaxing at home"], aliases=["hygge"])
def _(S):
    body = poly([(4, 21), (3.5, 14), (6, 9.5), (12, 9.5), (14.5, 14), (14, 21)], closed=True, r=S.r + 1.5)
    return [hd(9, 5.5, 2.4), shell(body), shell(rect(15.5, 14.5, 4.5, 6, L(S, 0.8, 1.6))), line("M20 16H21.5V19H20"),
            line("M17 12C16 11 18.5 10 17.5 8.5"), line("M19.5 12C18.5 11 21 10 20 8.5")]


@icon("digital-detox", CAT, "A smartphone lying face down with a small leafy sprout growing beside it.",
      tags=["screen time", "unplug", "phone free", "tech break", "offline", "social media break"], aliases=["unplug-phone"])
def _(S):
    leaf_l = "M18.4 13.8C18.4 11.4 16.6 10.4 15.1 10.8C15.1 12.9 16.3 14 18.4 13.8Z"
    leaf_r = "M18.4 10.8C18.4 8.4 20.2 7.4 21.7 7.8C21.7 9.9 20.5 11 18.4 10.8Z"
    return [shell(rect(3, 3, 9.5, 18, L(S, 1.5, 3.5))), Part("dot", rect(5, 5, 3.4, 3.4, L(S, 0.5, 1.4))),
            line(seg(18.4, 21, 18.4, 8)), solid(leaf_l), solid(leaf_r)]
