"""TypeIcon Core: family (batch family_002): baby milestones, parenting moments, family routines and outings.

People are stick figures (a solid head over 2 px limbs, polylines filleted with S.r). Objects they use are
shells so Filled turns them solid while limbs get heavier. Layered scenes cut back layers away around the
front silhouette with a gap.
"""
import math

from dsl import LINE, D, P, ST, U, Part, arc, circle, detail, dot, ellipse, filled_region, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar  # noqa: F401

CAT = "family"
HR = 2.25


def pick(S, a, b):
    return a if S.name == "line" else b


def limb(S, *pts):
    return line(poly(list(pts), r=S.r * 0.5))


def mark(d):
    return Part("dot", d)


def ahead(S, x, y, deg, n=2.2):
    """Open arrowhead at (x, y) pointing along deg (0 = right, 90 = down)."""
    a1, a2 = math.radians(deg + 150), math.radians(deg - 150)
    return line(poly([(x + n * math.cos(a1), y + n * math.sin(a1)), (x, y), (x + n * math.cos(a2), y + n * math.sin(a2))], r=S.r * 0.3))


def wheel(cx, cy, r=2):
    return shell(circle(cx, cy, r))


def star(cx, cy, ro, ri=None):
    ri = ri or ro * 0.45
    pts = []
    for i in range(10):
        pts.append(polar(cx, cy, ro if i % 2 == 0 else ri, -90 + i * 36))
    return poly(pts, closed=True)


# =========================================================================== gear

@icon("stroller-rain-cover", CAT, "Side view of a stroller under a clear dome cover with raindrops falling on it",
      tags=["stroller", "rain", "weather cover", "pram", "baby", "buggy", "wet weather"])
def _(S):
    dome = "M3 14A7 8 0 0 1 17 14Z" if S.name == "line" else "M3 14A7 8 0 0 1 17 14Z"
    return [
        shell(dome),
        limb(S, (17, 14), (21, 10)),
        line(seg(6, 14, 6, 17)), line(seg(14, 14, 14, 17)),
        wheel(6, 19.5, 2.25), wheel(14, 19.5, 2.25),
        line(seg(7, 2.5, 5.5, 5)), line(seg(12, 2.5, 10.5, 5)), line(seg(17, 2.5, 15.5, 5)),
    ]


@icon("daycare-buggy", CAT, "Large wagon stroller seen from the side with four children in a row under a canopy",
      tags=["daycare", "stroller", "multi seat stroller", "crew buggy", "nursery", "kids", "wagon"])
def _(S):
    return [
        shell(rect(2.5, 11.5, 17, 4.5, min(S.R, 2))),
        line(seg(3, 4.5, 20, 4.5)), line(seg(4, 4.5, 4, 11)), line(seg(19, 4.5, 19, 11)),
        dot(7, 8.5, 1.5), dot(10.5, 8.5, 1.5), dot(14, 8.5, 1.5), dot(17.5, 8.5, 1.5),
        wheel(6.5, 19.5, 2), wheel(16.5, 19.5, 2),
        limb(S, (19.5, 14), (22, 10)),
    ]


@icon("trailer-bike", CAT, "Adult bicycle with a child's one-wheel bike hitched behind it",
      tags=["bicycle", "tag along", "child bike", "cycling", "family ride", "attachment", "trailer cycle"])
def _(S):
    return [
        wheel(3.5, 18, 1.75), wheel(10.5, 17.5, 2.75), wheel(19.5, 17.5, 2.75),
        limb(S, (3.5, 18), (5, 11)), line(seg(2.5, 11, 7, 11)),
        line(seg(5.2, 12, 11.5, 12)),
        limb(S, (10.5, 17.5), (12.5, 11.5), (17, 11.5), (19.5, 17.5)),
        line(seg(10.5, 8.5, 14, 8.5)), line(seg(12.5, 8.5, 12.5, 11.5)),
        limb(S, (17, 11.5), (17, 6.5), (19.5, 6.5)),
    ]


@icon("kids-kick-scooter", CAT, "Small kick scooter with a deck, two wheels and a tall T handle",
      tags=["scooter", "kick scooter", "toddler scooter", "ride on", "push scooter", "toy", "kids"])
def _(S):
    return [
        shell(rect(5.5, 14.5, 12, 3, min(S.R, 1.5))),
        wheel(4.5, 19.5, 2), wheel(19, 19.5, 2),
        limb(S, (17, 14.5), (15.5, 4)),
        line(seg(12.5, 4, 19.5, 4)),
        line(seg(17.5, 17.5, 19, 17.5)),
    ]


@icon("stick-family-decal", CAT, "Rear car window with a row of stick figure family decals of decreasing height",
      tags=["car decal", "family sticker", "stick figures", "window sticker", "minivan", "family car", "sticker"])
def _(S):
    return [
        shell(poly([(2.5, 20), (5, 5), (19, 5), (21.5, 20)], closed=True, r=S.r * 0.5)),
        dot(8, 9.5, 1.5), detail(seg(8, 11.5, 8, 17)),
        dot(12.5, 11.5, 1.4), detail(seg(12.5, 13.5, 12.5, 17)),
        dot(16.5, 13, 1.25), detail(seg(16.5, 14.8, 16.5, 17)),
    ]


# =========================================================================== baby milestones

@icon("baby-first-word", CAT, "Baby face with a speech bubble holding two sound dots",
      tags=["first word", "baby talk", "speech", "milestone", "babbling", "mama", "dada"])
def _(S):
    return [
        shell(circle(8, 15.5, 5.5)),
        dot(6, 14.5, 0.9), dot(10, 14.5, 0.9),
        detail("M6 17.5Q8 19.2 10 17.5"),
        shell(poly([(12.5, 2.5), (21.5, 2.5), (21.5, 9.5), (15.5, 9.5), (13, 12), (13, 9.5), (12.5, 9.5)], closed=True, r=S.r * 0.4)),
        dot(16, 6, 0.95), dot(19, 6, 0.95),
    ]


@icon("baby-milestone-card", CAT, "Milestone card with a large number one, a star above and a small baby face in the corner",
      tags=["milestone card", "baby photo", "monthly card", "first year", "keepsake", "baby", "photo prop"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 19, min(S.R, 3))),
        mark(star(12, 7.5, 3)),
        detail(poly([(7.5, 13.5), (9.5, 11.5), (9.5, 18)], r=S.r * 0.4)),
        dot(15.5, 16, 2.2),
    ]


@icon("baby-memory-book", CAT, "Closed baby keepsake book with tiny footprints on the cover and a ribbon bookmark",
      tags=["memory book", "baby book", "keepsake", "scrapbook", "journal", "footprints", "baby album"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 16, min(S.R, 2))),
        detail(seg(8, 2.5, 8, 18.5)),
        mark("M11.5 14a1.3 2 0 1 0 0.01 0Z"), mark("M15.8 8.5a1.3 2 0 1 0 0.01 0Z"),
        line(poly([(15, 18.5), (15, 21), (16.5, 19.5), (18, 21), (18, 18.5)])),
    ]


@icon("baby-sitting-up", CAT, "Baby sitting upright on the floor with legs out in front and arms raised for balance",
      tags=["sitting up", "baby milestone", "sit", "infant", "six months", "tummy time", "development"])
def _(S):
    return [
        dot(10.5, 5, 2.75),
        shell(rect(7, 8.5, 7, 10, 3.5)),
        limb(S, (14, 17), (21, 17)),
        limb(S, (7.5, 10.5), (4, 9), (3, 5.5)),
        limb(S, (13.5, 10.5), (17, 9), (18, 5.5)),
    ]


@icon("baby-rolling-over", CAT, "Baby rolling over onto its side with a curved arrow above showing the turn",
      tags=["rolling over", "roll", "baby milestone", "tummy time", "infant movement", "development", "turn"])
def _(S):
    return [
        shell(rect(4, 12.5, 11, 7, 3.5)),
        dot(18.5, 16, 3),
        line(arc(12, 16, 10, 215, 325)),
        ahead(S, *polar(12, 16, 10, 325), 55),
    ]


@icon("toddler-walking", CAT, "Small toddler walking with a wide stance and arms held up and out for balance",
      tags=["toddler", "first steps", "walking", "baby steps", "milestone", "child", "learning to walk"])
def _(S):
    return [
        dot(12, 5.5, 2.75),
        limb(S, (12, 9), (12, 15)),
        limb(S, (12, 10.5), (7, 7.5)), limb(S, (12, 10.5), (17, 7.5)),
        limb(S, (12, 15), (8, 21)), limb(S, (12, 15), (16, 21)),
    ]


@icon("baby-pulling-to-stand", CAT, "Baby standing and gripping the edge of a low table with both hands",
      tags=["pulling up", "standing", "cruising", "baby milestone", "furniture walking", "infant", "table"])
def _(S):
    return [
        dot(7, 6, 2.5),
        limb(S, (7, 9.5), (7, 15)),
        limb(S, (7, 11), (12, 12.5)),
        limb(S, (7, 15), (5, 21)), limb(S, (7, 15), (9, 21)),
        shell(rect(12, 12.5, 10, 2.5, 1)),
        line(seg(20.5, 15, 20.5, 21)), line(seg(14, 15, 14, 21)),
    ]


@icon("pat-a-cake", CAT, "Adult hand and baby hand meeting palm to palm in a clap with short impact lines",
      tags=["clapping", "baby games", "high five", "play", "nursery rhyme", "hands", "bonding"])
def _(S):
    return [
        shell(rect(5, 8, 5, 9, 2.5)),
        shell(rect(14, 10, 4, 7, 2)),
        limb(S, (7.5, 17), (5, 21)), limb(S, (16, 17), (18.5, 21)),
        line(seg(12, 2.5, 12, 5.5)), line(seg(7.5, 3.5, 9, 5.5)), line(seg(16.5, 3.5, 15, 5.5)),
    ]


@icon("first-birthday-cake", CAT, "Small round cake with one tall candle shaped like the number one",
      tags=["first birthday", "one year", "birthday cake", "candle", "baby party", "celebration", "milestone"])
def _(S):
    return [
        shell(rect(4.5, 13, 15, 8, min(S.R, 3))),
        detail(pick(S, poly([(4.5, 16.5), (8, 18), (12, 16), (16, 18), (19.5, 16.5)]), "M4.5 16.5Q8 19 12 16.5T19.5 16.5")),
        line(poly([(9.5, 8), (12.5, 5.5), (12.5, 13)], r=S.r * 0.4)),
        dot(12.5, 2.8, 1.3),
    ]


@icon("tooth-fairy", CAT, "Small molar tooth with a wing on one side and a star tipped wand on the other",
      tags=["tooth fairy", "lost tooth", "baby tooth", "dental", "wand", "wings", "children"])
def _(S):
    tooth = ("M7.5 8C7.5 5.5 10 5 12 6.5C14 5 16.5 5.5 16.5 8C16.5 11 15 12.5 15 15.5L14.5 20C14.3 21 12.7 21 12.5 19.5"
             "L12 16.5L11.5 19.5C11.3 21 9.7 21 9.5 20L9 15.5C9 12.5 7.5 11 7.5 8Z")
    return [
        shell(tooth),
        shell("M7.5 11C4 11 2.5 8 2.5 4.5C6 5 7.5 7 7.5 11Z"),
        limb(S, (16.5, 13), (20, 9.5)),
        mark(star(20.5, 5.5, 2.7)),
    ]


@icon("baby-swimming", CAT, "Baby underwater in profile with arms and legs spread and bubbles rising above",
      tags=["baby swim", "infant swimming", "swim lessons", "water", "pool", "bubbles", "aquatic"])
def _(S):
    return [
        line("M2 4.5q2.5-2 5 0t5 0t5 0t5 0"),
        dot(17, 13, 2.5),
        limb(S, (14.5, 13), (8, 13)),
        limb(S, (14, 13), (16, 18.5)),
        limb(S, (8, 13), (4.5, 9.5)), limb(S, (8, 13), (4.5, 17)),
        dot(20.5, 9.5, 0.9), dot(20, 7, 0.9),
    ]


def cres(cx, cy, r, dx, dy, r2):
    """Crescent: circle (cx,cy,r) minus a circle offset by (dx,dy) with radius r2."""
    return path_to_d(D(P(circle(cx, cy, r)), P(circle(cx + dx, cy + dy, r2))))


# =========================================================================== roles and households

@icon("toddler", CAT, "Small figure with a large round head, short body and stubby legs standing with arms out",
      tags=["toddler", "small child", "preschooler", "kid", "little one", "child", "two year old"])
def _(S):
    return [
        dot(12, 6.5, 3.5),
        limb(S, (12, 11), (12, 16)),
        limb(S, (12, 12.5), (7, 14)), limb(S, (12, 12.5), (17, 14)),
        limb(S, (12, 16), (9.5, 21)), limb(S, (12, 16), (14.5, 21)),
    ]


@icon("co-parenting", CAT, "Two small houses side by side with a child between them and a double headed arrow below",
      tags=["co parenting", "shared custody", "two homes", "divorce", "joint parenting", "separated parents", "child"])
def _(S):
    return [
        shell(poly([(2.5, 13.5), (2.5, 9), (5.5, 6), (8.5, 9), (8.5, 13.5)], closed=True, r=S.r * 0.5)),
        shell(poly([(21.5, 13.5), (21.5, 9), (18.5, 6), (15.5, 9), (15.5, 13.5)], closed=True, r=S.r * 0.5)),
        dot(12, 9, 1.6), limb(S, (12, 12), (12, 14.5)),
        line(seg(4.5, 19.5, 19.5, 19.5)), ahead(S, 4, 19.5, 180), ahead(S, 20, 19.5, 0),
    ]


@icon("working-parent", CAT, "Adult carrying a briefcase in one hand and holding a small child's hand with the other",
      tags=["working parent", "commute", "briefcase", "work life balance", "career parent", "mum", "dad"])
def _(S):
    return [
        dot(9, 4.5, HR),
        limb(S, (9, 8), (9, 14)),
        limb(S, (9, 14), (7, 21)), limb(S, (9, 14), (11, 21)),
        limb(S, (9, 9.5), (5, 13.5)),
        shell(rect(2.5, 14.5, 5, 4, 1)),
        limb(S, (9, 9.5), (14, 12)),
        dot(19, 9.5, 1.75), limb(S, (19, 12.5), (19, 17)),
        limb(S, (19, 17), (17.5, 21)), limb(S, (19, 17), (20.5, 21)),
        limb(S, (19, 13.5), (14, 12)),
    ]


@icon("stay-at-home-parent", CAT, "House outline with an adult and a small child standing inside",
      tags=["stay at home parent", "homemaker", "home parent", "childcare at home", "household", "caregiver", "family home"])
def _(S):
    return [
        shell(poly([(3, 11), (12, 3), (21, 11), (21, 21), (3, 21)], closed=True, r=S.r * 0.5)),
        dot(9.5, 12.5, 1.5), detail(seg(9.5, 14.8, 9.5, 21)),
        dot(15, 15, 1.25), detail(seg(15, 16.8, 15, 21)),
    ]


@icon("parental-leave", CAT, "Calendar page with a baby carriage in place of the date grid",
      tags=["parental leave", "maternity leave", "paternity leave", "time off", "new baby", "baby carriage", "calendar"])
def _(S):
    return [
        shell(rect(3, 4.5, 18, 16.5, min(S.R, 3))),
        detail(seg(3, 9.5, 21, 9.5)),
        line(seg(8, 2.5, 8, 6)), line(seg(16, 2.5, 16, 6)),
        mark("M7.5 16A4.5 4.5 0 0 1 16.5 16Z"), mark("M17.5 12.5L16.5 16L15.5 16Z"),
        mark(circle(9.5, 18, 1)), mark(circle(14.5, 18, 1)),
    ]


@icon("playdate", CAT, "Two small children sitting on the floor facing each other with a toy block between them",
      tags=["playdate", "play date", "toddlers playing", "friends", "playing together", "toy block", "kids"])
def _(S):
    return [
        dot(5, 7, 2), limb(S, (5, 10), (5, 15.5)), limb(S, (5, 15.5), (8.5, 15.5)),
        dot(19, 7, 2), limb(S, (19, 10), (19, 15.5)), limb(S, (19, 15.5), (15.5, 15.5)),
        shell(rect(10, 12.5, 4.5, 4.5, 0 if S.name == "line" else 1)),
    ]


@icon("bedtime-routine", CAT, "Crescent moon, a toothbrush and a small closed book in a row",
      tags=["bedtime routine", "night routine", "brush teeth", "bedtime story", "going to bed", "sleep", "toothbrush"])
def _(S):
    return [
        solid(cres(6.5, 12, 5, 2.6, -2, 4.2)),
        line(seg(12.5, 21, 12.5, 11)), solid(rect(11, 3.5, 3, 7)),
        shell(rect(16.5, 10, 5, 10.5, 1)),
        mark(rect(18.25, 12, 1.5, 2)),
    ]


@icon("curfew", CAT, "Clock face with hands showing ten, a small house below right and a crescent moon above",
      tags=["curfew", "home by", "late night", "bedtime limit", "time to be home", "teen rules", "night"])
def _(S):
    return [
        shell(circle(9, 9, 6.25)),
        detail(poly([(9, 5.5), (9, 9), (6.5, 10.5)])),
        shell(poly([(13.5, 21), (13.5, 17.5), (17.5, 14), (21.5, 17.5), (21.5, 21)], closed=True, r=S.r * 0.5)),
        solid(cres(19.5, 5.5, 3, 1.6, -1.2, 2.6)),
    ]


@icon("time-out-chair", CAT, "Small child's chair seen from the side with a sand timer standing on the seat",
      tags=["time out", "naughty chair", "discipline", "timer", "consequence", "calm down", "chair"])
def _(S):
    return [
        line(poly([(6, 3.5), (6, 16), (18, 16)], r=S.r * 0.4)),
        line(seg(6, 16, 6, 21)), line(seg(18, 16, 18, 21)),
        shell(poly([(9.5, 4), (14.5, 4), (12, 8.5), (14.5, 13), (9.5, 13), (12, 8.5)], closed=True, r=S.r * 0.3)),
    ]


@icon("family-rules-poster", CAT, "Poster pinned at the top with a small house symbol as the header and two lines of text below",
      tags=["house rules", "family rules", "poster", "rule chart", "family values", "expectations", "home rules"])
def _(S):
    return [
        shell(rect(4.5, 4.5, 15, 17, min(S.R, 2))),
        mark(poly([(8.5, 12), (8.5, 9.5), (12, 6.5), (15.5, 9.5), (15.5, 12)], closed=True)),
        detail(seg(8, 15, 16, 15)), detail(seg(8, 18.5, 13.5, 18.5)),
        dot(12, 3.5, 1.3),
    ]


@icon("family-meeting", CAT, "Three people of different heights around a round table with a speech bubble above",
      tags=["family meeting", "family discussion", "round table", "talk together", "family council", "conversation", "household"])
def _(S):
    return [
        shell(rect(8, 2.5, 8, 4.5, 0 if S.name == 'line' else 2)),
        dot(12, 11, 1.75), dot(5, 12, 1.75), dot(19, 12, 1.75),
        line(seg(5, 13.5, 5, 16)), line(seg(12, 12.5, 12, 16)), line(seg(19, 13.5, 19, 16)),
        shell(rect(2.5, 16.5, 19, 4.5, 0 if S.name == 'line' else 2.25)),
    ]


@icon("family-calendar", CAT, "Calendar page with a row of three heads of different sizes above small date dots",
      tags=["family calendar", "shared schedule", "household planner", "family planner", "events", "organizer", "family"])
def _(S):
    return [
        shell(rect(3, 3.5, 18, 17.5, min(S.R, 3))),
        line(seg(8, 2, 8, 5)), line(seg(16, 2, 16, 5)),
        dot(7.5, 10.5, 1.6), dot(12, 10, 2.1), dot(16.5, 10.75, 1.3),
        dot(6.75, 16.5, 0.85), dot(9.5, 16.5, 0.85), dot(12.25, 16.5, 0.85), dot(15, 16.5, 0.85), dot(17.75, 16.5, 0.85),
    ]


@icon("chore-wheel", CAT, "Round spinner wheel divided into six segments with a pointer at the top",
      tags=["chore wheel", "chore chart", "spinner", "jobs", "household tasks", "rota", "kids chores"])
def _(S):
    cx, cy, r = 12, 13.5, 8
    spokes = [seg(*polar(cx, cy, r, a), *polar(cx, cy, r, a + 180)) for a in (0, 60, 120)]
    return [
        shell(circle(cx, cy, r)),
        *[detail(d) for d in spokes],
        solid(poly([(9.5, 1.8), (14.5, 1.8), (12, 6)], closed=True, r=S.r)),
        dot(cx, cy, 1.5),
    ]


@icon("parent-and-child-parking", CAT, "Square parking sign with a letter P and an adult holding a child's hand beside it",
      tags=["parent child parking", "family parking", "reserved parking", "parking sign", "mom and baby", "car park", "priority"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 10, 10, min(S.R, 2))),
        detail("M5.75 10V5H8.25A1.75 1.75 0 0 1 8.25 8.5H5.75"),
        line(seg(7.5, 12.5, 7.5, 21)),
        dot(16.5, 5.5, 1.75), limb(S, (16.5, 8.5), (16.5, 14.5)),
        limb(S, (16.5, 14.5), (15, 21)), limb(S, (16.5, 14.5), (18, 21)),
        limb(S, (16.5, 10), (20, 14)),
        dot(20.5, 11, 1.2),
    ]


@icon("child-protection", CAT, "Small child figure resting in an open cupped hand with a curved shield arc above",
      tags=["child protection", "safeguarding", "child safety", "care", "protect children", "welfare", "cupped hand"])
def _(S):
    return [
        line(arc(12, 12, 10, 205, 335)),
        dot(12, 8.5, 2), limb(S, (12, 11.5), (12, 16)),
        limb(S, (12, 12.5), (9.5, 15)), limb(S, (12, 12.5), (14.5, 15)),
        line("M3.5 15.5Q4 21 12 21Q20 21 20.5 15.5"),
    ]


@icon("parenting-book", CAT, "Closed book with an adult and a child holding hands on the cover",
      tags=["parenting book", "parenting guide", "advice book", "child rearing", "family guide", "reading", "manual"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, min(S.R, 2))),
        detail(seg(7.5, 2.5, 7.5, 21.5)),
        dot(12, 8, 1.5), detail(seg(12, 10, 12, 17)),
        dot(16.5, 11.5, 1.2), detail(seg(16.5, 13.2, 16.5, 17)),
        detail(seg(12, 13, 16.5, 14.5)),
    ]


# =========================================================================== keepsakes and outings

@icon("baby-registry", CAT, "Clipboard with a checklist beside a small baby bottle and a gift box",
      tags=["baby registry", "baby shower", "wish list", "gift list", "newborn gifts", "checklist", "shower gifts"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 12, 17, min(S.R, 2))),
        line(seg(6.5, 3, 10.5, 3)),
        dot(6, 10.5, 1), detail(seg(8.5, 10.5, 11.5, 10.5)),
        dot(6, 15.5, 1), detail(seg(8.5, 15.5, 11.5, 15.5)),
        solid(rect(18, 3.5, 2.5, 2)),
        shell(rect(17, 7, 4.5, 5.5, min(S.R, 1.5))),
        shell(rect(17, 15.5, 4.5, 5.5, min(S.R, 1))),
        mark(rect(18.75, 15.5, 1, 5.5)),
    ]


@icon("college-savings-jar", CAT, "Glass jar holding coins with a graduation cap sitting on the lid",
      tags=["college fund", "education savings", "tuition", "savings jar", "piggy bank", "graduation", "coins"])
def _(S):
    return [
        shell(poly([(11, 2.5), (18.5, 5.5), (11, 8.5), (3.5, 5.5)], closed=True, r=S.r * 0.6)),
        line(poly([(18.5, 6), (18.5, 9)])),
        shell(rect(5.5, 11.5, 13, 9.5, 3)),
        mark(circle(9.5, 17.5, 1.5)), mark(circle(14.5, 17.5, 1.5)), mark(circle(12, 14.5, 1.2)),
    ]


@icon("family-location", CAT, "Map pin whose round head holds two adult figures and a child figure",
      tags=["family location", "find family", "location sharing", "map pin", "family tracker", "where are you", "gps"])
def _(S):
    return [
        shell("M12 21.5C12 21.5 4.5 15 4.5 9.5A7.5 7.5 0 0 1 19.5 9.5C19.5 15 12 21.5 12 21.5Z"),
        dot(9, 7.5, 1.3), detail(seg(9, 9.5, 9, 12.5)),
        dot(15, 7.5, 1.3), detail(seg(15, 9.5, 15, 12.5)),
        dot(12, 10, 1.1), detail(seg(12, 11.7, 12, 13.2)),
    ]


@icon("family-video-call", CAT, "Phone screen showing a grandparent's face with a small child waving in front of the camera",
      tags=["video call", "grandparents", "facetime", "remote family", "long distance", "phone call", "family chat"])
def _(S):
    return [
        shell(rect(5.5, 2, 13, 20, min(S.R, 3))),
        dot(12, 7, 2.2), detail("M8.5 13.5Q8.5 10.5 12 10.5Q15.5 10.5 15.5 13.5"),
        dot(9.5, 17, 1.3), detail(seg(9.5, 18.7, 9.5, 20)), detail(poly([(10.5, 18), (14.5, 15)])),
    ]


@icon("sleep-deprived-parent", CAT, "Tired face with slanted half closed eyes and a coffee mug",
      tags=["tired parent", "exhausted", "no sleep", "newborn", "coffee", "sleepless", "fatigue"])
def _(S):
    return [
        shell(circle(8.5, 10, 6.5)),
        detail(seg(5, 8.5, 7.5, 8.5)), detail(seg(9.5, 8.5, 12, 8.5)),
        detail(seg(6.5, 13, 10.5, 13)),
        shell(rect(15.5, 14.5, 5, 5.5, min(S.R, 1.5))),
        line("M20.5 16a1.7 1.7 0 0 1 0 3"),
    ]


@icon("family-therapy", CAT, "Three figures on a sofa facing one figure in an armchair",
      tags=["family therapy", "counselling", "counseling", "therapist", "couples therapy", "mental health", "session"])
def _(S):
    return [
        dot(4.5, 7.5, 1.3), dot(7.5, 7.5, 1.3), dot(10.5, 7.5, 1.3),
        shell(rect(2.5, 10.5, 10.5, 6, min(S.R, 2))),
        line(seg(4, 16.5, 4, 20)), line(seg(11.5, 16.5, 11.5, 20)),
        dot(18.5, 6.5, 1.7),
        shell(rect(15.5, 10, 6, 6.5, min(S.R, 2))),
        line(seg(16.5, 16.5, 16.5, 20)), line(seg(20.5, 16.5, 20.5, 20)),
    ]


@icon("fridge-art", CAT, "Refrigerator door with a child's drawing of a sun held on by a round magnet",
      tags=["fridge art", "kids drawing", "refrigerator", "magnet", "child artwork", "crayon art", "display"])
def _(S):
    return [
        shell(rect(4.5, 2, 15, 20, min(S.R, 3))),
        detail(seg(4.5, 8.5, 19.5, 8.5)),
        detail(seg(16.5, 4.5, 16.5, 6.5)), detail(seg(16.5, 10.5, 16.5, 13)),
        detail(rect(8, 13, 5, 5)),
        dot(10.5, 13, 1.3),
    ]


@icon("family-movie-night", CAT, "Sofa seen from behind with three heads of different sizes facing a screen with a play triangle",
      tags=["movie night", "family film", "home cinema", "living room", "tv time", "popcorn night", "streaming"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 8, 0 if S.name == "line" else 2)),
        mark(poly([(10.5, 4.5), (10.5, 8.5), (14, 6.5)], closed=True)),
        dot(7.5, 14.5, 1.6), dot(12, 14, 2), dot(16.5, 14.8, 1.3),
        shell(rect(3.5, 16.5, 17, 5, 0 if S.name == "line" else 2)),
    ]


@icon("family-hike", CAT, "Adult with a backpack and walking stick followed by a child, with a mountain peak above",
      tags=["family hike", "hiking", "trail", "walking stick", "backpack", "outdoors", "nature walk"])
def _(S):
    return [
        line(poly([(12.5, 9), (17, 3.5), (21.5, 9)], r=S.r * 0.5)),
        dot(7.5, 8, 1.75), limb(S, (7.5, 10.5), (7.5, 16)),
        limb(S, (7.5, 16), (5.5, 21.5)), limb(S, (7.5, 16), (9.5, 21.5)),
        limb(S, (7.5, 12), (11.5, 14)), line(seg(11.5, 11, 13, 21.5)),
        shell(rect(3, 10.5, 3, 4.5, 1)),
        dot(18, 14, 1.4), limb(S, (18, 16), (18, 18.5)),
        limb(S, (18, 18.5), (16.7, 21.5)), limb(S, (18, 18.5), (19.3, 21.5)),
    ]


@icon("family-bike-ride", CAT, "A large bicycle and a small bicycle riding side by side, each with a rider",
      tags=["family bike ride", "cycling", "bicycle", "kids bike", "cycle together", "outdoor activity", "weekend ride"])
def _(S):
    return [
        wheel(3.5, 18, 2), wheel(10, 18, 2),
        limb(S, (3.5, 18), (6, 13), (10, 18)), line(seg(6, 13, 9, 12.5)),
        dot(6.5, 5.5, 1.6), limb(S, (6.5, 7.5), (6, 12)), limb(S, (6.5, 8.5), (9.5, 12.5)),
        wheel(16, 19.5, 1.5), wheel(21, 19.5, 1.5),
        limb(S, (16, 19.5), (17.5, 15), (21, 19.5)), line(seg(17.5, 15, 20.5, 14.5)),
        dot(18, 10.5, 1.3), limb(S, (18, 12), (17.5, 15)), limb(S, (18, 12.5), (20.5, 14.5)),
    ]


@icon("family-camping", CAT, "Triangle tent with a campfire beside it and three heads of different sizes around the fire",
      tags=["family camping", "tent", "campfire", "outdoors", "campsite", "holiday", "camp out"])
def _(S):
    return [
        shell(poly([(2.5, 20), (8, 7), (13.5, 20)], closed=True, r=S.r * 0.6)),
        detail(seg(8, 12, 8, 20)),
        dot(16, 10.5, 1.4), dot(19, 8, 1.1), dot(21.5, 10.5, 1.4),
        solid("M18.75 12.5C20.5 14.5 21 16 21 17.5A2.25 2.25 0 0 1 16.5 17.5C16.5 16 17.5 15 17.5 14C18 14.5 18.5 14 18.75 12.5Z"),
        line(seg(16, 21, 21.5, 21)),
    ]


@icon("baking-with-kids", CAT, "Child on a small stool stirring a mixing bowl beside an adult holding a rolling pin",
      tags=["baking with kids", "cooking together", "kitchen", "mixing bowl", "rolling pin", "family cooking", "bake"])
def _(S):
    return [
        dot(3.5, 7, 1.75), limb(S, (3.5, 9.5), (3.5, 15)),
        limb(S, (3.5, 15), (2.5, 21.5)), limb(S, (3.5, 15), (5.5, 21.5)),
        limb(S, (3.5, 11), (7.5, 13)),
        shell("M7.5 13.5H14A3.25 3.25 0 0 1 7.5 13.5Z"),
        dot(21, 5, 2), limb(S, (21, 8), (21, 15)),
        limb(S, (21, 15), (19.5, 21.5)), limb(S, (21, 15), (22, 21.5)),
        limb(S, (21, 10), (20, 12.5)),
        shell(rect(14.5, 11.5, 5.5, 2.5, 1.25)),
    ]


@icon("kite-flying-with-child", CAT, "Adult and child standing together holding one string that rises to a diamond kite",
      tags=["kite flying", "kite", "windy day", "park", "play outdoors", "string", "family fun"])
def _(S):
    return [
        shell(poly([(17, 2.5), (20.5, 6.5), (17, 10.5), (13.5, 6.5)], closed=True, r=S.r * 0.4)),
        line("M17 11Q15 14.5 10.5 15"),
        dot(5, 8, 1.75), limb(S, (5, 10.5), (5, 16)),
        limb(S, (5, 16), (3.5, 21.5)), limb(S, (5, 16), (6.5, 21.5)),
        limb(S, (5, 12), (10.5, 15)),
        dot(15.5, 14.5, 1.4), limb(S, (15.5, 16.5), (15.5, 18.5)),
        limb(S, (15.5, 18.5), (14.3, 21.5)), limb(S, (15.5, 18.5), (16.7, 21.5)),
        limb(S, (15.5, 17), (12.5, 15)),
    ]


@icon("family-portrait", CAT, "Picture frame holding two tall adult figures and two shorter child figures side by side",
      tags=["family portrait", "family photo", "picture frame", "group photo", "wall photo", "photograph", "memories"])
def _(S):
    def bust(cx, hw, top):
        return mark(f"M{fmt(cx - hw)} 18V{fmt(top + hw)}A{fmt(hw)} {fmt(hw)} 0 0 1 {fmt(cx + hw)} {fmt(top + hw)}V18Z")
    return [
        shell(rect(2.5, 3.5, 19, 17.5, 0 if S.name == 'line' else 3)),
        dot(6, 8.5, 1.6), bust(6, 2.2, 11.5),
        dot(10.3, 11.5, 1.3), bust(10.3, 1.7, 13.5),
        dot(13.7, 11.5, 1.3), bust(13.7, 1.7, 13.5),
        dot(18, 8.5, 1.6), bust(18, 2.2, 11.5),
    ]


@icon("family-reunion", CAT, "Two rows of many figures of different heights standing under a draped banner",
      tags=["family reunion", "gathering", "get together", "big family", "relatives", "party", "group"])
def _(S):
    return [
        line("M2.5 3.5Q12 7 21.5 3.5"),
        dot(5, 10, 1.4), dot(10, 9.5, 1.4), dot(14.5, 9.5, 1.4), dot(19, 10, 1.4),
        line(seg(5, 11.8, 5, 14)), line(seg(10, 11.3, 10, 14)), line(seg(14.5, 11.3, 14.5, 14)), line(seg(19, 11.8, 19, 14)),
        dot(7.5, 15, 1.5), dot(12, 14.5, 1.5), dot(16.5, 15, 1.5),
        line(seg(7.5, 17, 7.5, 21)), line(seg(12, 16.5, 12, 21)), line(seg(16.5, 17, 16.5, 21)),
    ]


@icon("family-stroll", CAT, "Row of four figures of decreasing height walking to the right holding hands in a chain",
      tags=["family walk", "stroll", "holding hands", "walking together", "park walk", "evening walk", "parents and children"])
def _(S):
    return [
        dot(4.5, 7.5, 1.8), limb(S, (4.5, 10), (4.5, 16.5)),
        limb(S, (4.5, 16.5), (3, 21.5)), limb(S, (4.5, 16.5), (6, 21.5)),
        dot(10.5, 10, 1.6), limb(S, (10.5, 12.2), (10.5, 17)),
        limb(S, (10.5, 17), (9.2, 21.5)), limb(S, (10.5, 17), (11.8, 21.5)),
        dot(15.8, 12.5, 1.4), limb(S, (15.8, 14.4), (15.8, 18)),
        limb(S, (15.8, 18), (14.7, 21.5)), limb(S, (15.8, 18), (16.9, 21.5)),
        dot(20.5, 15, 1.2), limb(S, (20.5, 16.7), (20.5, 19)),
        limb(S, (20.5, 19), (19.7, 21.5)), limb(S, (20.5, 19), (21.3, 21.5)),
        limb(S, (4.5, 12), (10.5, 14), (15.8, 15.5), (20.5, 17.5)),
    ]


@icon("parent-helping-homework", CAT, "Child at a desk with an open notebook while an adult leans in and points to the page",
      tags=["homework help", "studying", "school work", "tutoring", "help with homework", "parent teacher", "desk"])
def _(S):
    return [
        dot(5.5, 7.5, 2), limb(S, (5.5, 10.5), (5.5, 14)),
        limb(S, (5.5, 12), (9, 13.5)),
        line(seg(2.5, 15, 15, 15)), line(seg(4, 15, 4, 21.5)), line(seg(13.5, 15, 13.5, 21.5)),
        solid(rect(7, 12, 5.5, 2.5)),
        dot(19.5, 5, 2), limb(S, (19.5, 8), (19.5, 15)),
        limb(S, (19.5, 15), (18, 21.5)), limb(S, (19.5, 15), (21, 21.5)),
        limb(S, (19.5, 10), (15, 12.5), (11, 13)),
    ]


@icon("swing-between-parents", CAT, "Two adults holding the hands of a child lifted in the air between them with a motion arc below",
      tags=["swinging child", "lift", "playing with child", "one two three", "hand in hand", "parents and child", "fun"])
def _(S):
    return [
        dot(3.5, 7, 1.8), limb(S, (3.5, 9.5), (3.5, 15.5)),
        limb(S, (3.5, 15.5), (2.5, 21)), limb(S, (3.5, 15.5), (5, 21)),
        limb(S, (3.5, 10.5), (8.5, 10)),
        dot(20.5, 7, 1.8), limb(S, (20.5, 9.5), (20.5, 15.5)),
        limb(S, (20.5, 15.5), (19, 21)), limb(S, (20.5, 15.5), (21.5, 21)),
        limb(S, (20.5, 10.5), (15.5, 10)),
        dot(12, 6, 1.7), limb(S, (12, 8.3), (12, 13)),
        limb(S, (12, 13), (10.5, 16)), limb(S, (12, 13), (13.5, 16)),
        limb(S, (8.5, 10), (12, 10.5), (15.5, 10)),
        line("M6.5 19Q12 22 17.5 19"),
    ]


@icon("fishing-with-child", CAT, "Adult and child sitting side by side on a dock each holding a fishing rod over water",
      tags=["fishing", "fishing with kids", "dock", "lake", "angler", "rod", "family outing"])
def _(S):
    return [
        dot(5, 7.5, 1.75), limb(S, (5, 10), (5, 14.5)),
        limb(S, (5, 14.5), (10, 14.5)),
        dot(10.5, 9.5, 1.4), limb(S, (10.5, 11.5), (10.5, 14.5)),
        line(seg(2.5, 16.5, 13.5, 16.5)),
        limb(S, (5, 11), (7, 10)), line(seg(7, 10, 21, 2.5)), line(seg(21, 2.5, 21, 15.5)),
        limb(S, (10.5, 12.5), (12, 11.5)), line(seg(12, 11.5, 15.5, 9)), line(seg(15.5, 9, 15.5, 15.5)),
        line("M2.5 19.5q2.5-2 5 0t5 0t5 0t5 0"),
    ]


@icon("family-with-pet", CAT, "Two adults and a child standing together with a dog sitting at their feet",
      tags=["family with dog", "pet", "dog", "family pet", "household", "puppy", "pets and kids"])
def _(S):
    return [
        dot(3.5, 6.5, 1.5), limb(S, (3.5, 8.7), (3.5, 15)),
        limb(S, (3.5, 15), (2.5, 21.5)), limb(S, (3.5, 15), (4.8, 21.5)),
        dot(8.5, 6.5, 1.5), limb(S, (8.5, 8.7), (8.5, 15)),
        limb(S, (8.5, 15), (7.5, 21.5)), limb(S, (8.5, 15), (9.8, 21.5)),
        dot(13, 11.5, 1.3), limb(S, (13, 13.3), (13, 17.5)),
        limb(S, (13, 17.5), (12, 21.5)), limb(S, (13, 17.5), (14.2, 21.5)),
        shell(poly([(17.5, 21.5), (17.5, 17), (19.5, 14), (22, 14), (22, 16), (21, 17), (21, 21.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("sleepover", CAT, "Two sleeping bags side by side with heads poking out and a flashlight beam between them",
      tags=["sleepover", "slumber party", "sleeping bag", "flashlight", "pajama party", "camp indoors", "kids party"])
def _(S):
    return [
        shell(rect(2.5, 11.5, 6.5, 10, 3.25)), dot(5.75, 8.5, 1.8),
        shell(rect(15, 11.5, 6.5, 10, 3.25)), dot(18.25, 8.5, 1.8),
        solid(rect(11, 14.5, 2, 5)),
        line(seg(12, 13, 10, 3)), line(seg(12, 13, 14, 3)),
    ]


@icon("new-parents", CAT, "Two adults standing close together looking down at a swaddled baby held between them",
      tags=["new parents", "newborn", "first baby", "swaddled baby", "couple", "welcome baby", "family of three"])
def _(S):
    return [
        dot(4, 5.5, 2), limb(S, (4, 8.5), (4, 14.5)),
        limb(S, (4, 14.5), (2.5, 21.5)), limb(S, (4, 14.5), (6, 21.5)),
        dot(20, 5.5, 2), limb(S, (20, 8.5), (20, 14.5)),
        limb(S, (20, 14.5), (18, 21.5)), limb(S, (20, 14.5), (21.5, 21.5)),
        limb(S, (4, 10), (8.5, 15)), limb(S, (20, 10), (15.5, 15)),
        dot(12, 10, 1.6),
        shell(rect(8.5, 12.5, 7, 6, 3)),
    ]


@icon("carrying-child-on-hip", CAT, "Adult standing with a toddler sitting on one hip and the adult's arm wrapped around the child",
      tags=["carrying child", "hip carry", "toddler", "holding child", "parent and toddler", "picking up", "lift"])
def _(S):
    return [
        dot(8, 4.5, 2.25), limb(S, (8, 7.5), (8, 14.5)),
        limb(S, (8, 14.5), (6, 21.5)), limb(S, (8, 14.5), (10, 21.5)),
        dot(16.5, 8, 1.75), limb(S, (16.5, 10.5), (14.5, 14.5)),
        limb(S, (14.5, 14.5), (17, 17)), limb(S, (14.5, 14.5), (12, 18)),
        limb(S, (8, 9.5), (11.5, 13.5), (15.5, 12.5)),
    ]


@icon("family-circle", CAT, "Ring of five figures of different sizes holding hands in a circle seen from above",
      tags=["family circle", "holding hands", "unity", "togetherness", "group hug", "circle of care", "community"])
def _(S):
    cx, cy, R = 12, 12, 7.5
    heads = [(-90, 2.4), (-18, 2.0), (54, 2.3), (126, 1.7), (198, 2.1)]
    out = [dot(*polar(cx, cy, R, a), r) for a, r in heads]
    for i, (a, r) in enumerate(heads):
        b, rb = heads[(i + 1) % 5]
        a0 = a + math.degrees(math.asin((r + 0.5) / R))
        b0 = (b if b > a else b + 360) - math.degrees(math.asin((rb + 0.5) / R))
        out.append(line(arc(cx, cy, R, a0, b0)))
    return out


@icon("sibling-rivalry", CAT, "Two children pulling opposite arms of the same teddy bear with tension marks above",
      tags=["sibling rivalry", "fighting over toy", "tug of war", "sharing", "argument", "brothers sisters", "teddy bear"])
def _(S):
    return [
        shell(circle(12, 9.5, 2.5)), dot(9.6, 6.7, 1), dot(14.4, 6.7, 1),
        shell(rect(9.5, 13, 5, 6, 2)),
        dot(3.5, 10, 1.6), limb(S, (3.5, 12), (3.5, 17)),
        limb(S, (3.5, 17), (2.5, 21.5)), limb(S, (3.5, 17), (5, 21.5)),
        limb(S, (3.5, 13.5), (9.5, 14.5)),
        dot(20.5, 10, 1.6), limb(S, (20.5, 12), (20.5, 17)),
        limb(S, (20.5, 17), (19, 21.5)), limb(S, (20.5, 17), (21.5, 21.5)),
        limb(S, (20.5, 13.5), (14.5, 14.5)),
        line(seg(7, 5, 5.5, 3.5)), line(seg(17, 5, 18.5, 3.5)),
    ]


@icon("empty-nest", CAT, "Open twig nest with no eggs inside and a single bird flying away above it",
      tags=["empty nest", "kids left home", "grown children", "bird nest", "moving out", "retirement of parenting", "nest"])
def _(S):
    return [
        shell("M3 12.5H21C21 18 17 21 12 21S3 18 3 12.5Z"),
        detail(poly([(6.5, 15.5), (12, 17.5), (17.5, 15.5)])),
        line(seg(6, 11.5, 4, 8.5)), line(seg(18, 11.5, 20, 8.5)),
        line("M12.5 7Q14.5 3.5 16.5 6.5Q18.5 3.5 20.5 7"),
    ]


@icon("parent-child-talk", CAT, "Adult kneeling to eye level with a small child with a speech bubble between their heads",
      tags=["talking with child", "heart to heart", "kneeling", "listening", "communication", "parenting talk", "conversation"])
def _(S):
    return [
        shell(poly([(8.5, 2.5), (15.5, 2.5), (15.5, 7), (12.5, 7), (11, 9), (11, 7), (8.5, 7)], closed=True, r=S.r * 0.3)),
        dot(5, 8, 2), limb(S, (5, 10.5), (5, 15.5)),
        limb(S, (5, 15.5), (9.5, 16.5), (9.5, 21.5)), limb(S, (5, 15.5), (3, 21.5)),
        limb(S, (5, 11.5), (9, 13)),
        dot(18.5, 10, 1.6), limb(S, (18.5, 12), (18.5, 17)),
        limb(S, (18.5, 17), (17.2, 21.5)), limb(S, (18.5, 17), (19.8, 21.5)),
    ]


@icon("family-home", CAT, "House outline with a chimney and two adult figures and a child figure inside the walls",
      tags=["family home", "household", "house", "residence", "living together", "homeowners", "parents and child"])
def _(S):
    return [
        shell(poly([(2.5, 11), (12, 3), (21.5, 11), (21.5, 21.5), (2.5, 21.5)], closed=True, r=S.r * 0.5)),
        line(seg(17, 5.5, 17, 8)),
        dot(8, 12.5, 1.3), detail(seg(8, 14.5, 8, 21.5)),
        dot(16, 12.5, 1.3), detail(seg(16, 14.5, 16, 21.5)),
        dot(12, 15.5, 1.1), detail(seg(12, 17.2, 12, 21.5)),
    ]
