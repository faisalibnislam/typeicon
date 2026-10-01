"""TypeIcon Core: sports gear and sporting scenes, batch 005.

Athletes follow the sports module: head dot r 2.25, 2 px limbs drawn as open lines.
"""
import math

from dsl import D, I, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "sports-gear"


def pick(S, a, b):
    """Line value, Rounded value."""
    return a if S.name == "line" else b


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def sp(d) -> Part:
    """Small solid shape from a path."""
    return Part("dot", d)


def wave(S, y, x0=3, x1=21, step=3, amp=1):
    pts = []
    x = x0
    k = 0
    while x <= x1 + 0.01:
        pts.append((x, y + (amp if k % 2 else -amp)))
        x += step
        k += 1
    return poly(pts, r=S.r)


@icon("diving-tower", CAT, "Tall diving tower with platforms at three heights above a pool",
      tags=["diving", "platform", "high dive", "pool", "springboard", "aquatics"], aliases=["high-dive"])
def _(S):
    return [
        line(seg(6, 3, 6, 17)),
        line(seg(6, 4.5, 11, 4.5)),
        line(seg(6, 9, 14, 9)),
        line(seg(6, 13.5, 17, 13.5)),
        line(wave(S, 20, 3, 21, 3, 1)),
    ]


@icon("trophy-cabinet", CAT, "Glass-fronted cabinet with small trophies on its shelves",
      tags=["trophy case", "display cabinet", "awards", "shelf", "winners", "club room"], aliases=["trophy-case"])
def _(S):
    cup = lambda x, y: sp(poly([(x - 2.5, y), (x + 2.5, y), (x + 2, y + 2.5), (x + .75, y + 3.5), (x + .75, y + 4.5), (x + 2, y + 4.5), (x + 2, y + 5.5), (x - 2, y + 5.5), (x - 2, y + 4.5), (x - .75, y + 4.5), (x - .75, y + 3.5), (x - 2, y + 2.5)], closed=True))
    return [
        shell(rect(3.5, 2.5, 17, 18, S.R)),
        detail(seg(3.5, 11, 20.5, 11)),
        detail(seg(3.5, 16.5, 20.5, 16.5)),
        cup(8.5, 4.5), cup(15.5, 4.5),
        sp(circle(8.5, 13.7, 1.5)), sp(circle(15.5, 13.7, 1.5)),
        line(seg(6, 20.5, 6, 22)), line(seg(18, 20.5, 18, 22)),
    ]


@icon("medal-hanger", CAT, "Wall bar with three medals hanging from ribbons",
      tags=["medal rack", "medal display", "awards", "ribbons", "wall mount", "trophies"], aliases=["medal-rack"])
def _(S):
    parts = [line(seg(2.5, 3.5, 21.5, 3.5))]
    for x in (4.5, 12, 19.5):
        parts.append(line(poly([(x - 1.5, 3.5), (x, 8.5), (x + 1.5, 3.5)], r=S.r)))
        parts.append(shell(circle(x, 14, 2.5)))
    return parts


@icon("umpire-chair", CAT, "Tall umpire chair with a ladder frame beside a net post",
      tags=["referee chair", "high chair", "tennis", "volleyball", "official", "stand"], aliases=["referee-chair"])
def _(S):
    return [
        line(poly([(5.5, 2.5), (5.5, 9), (13, 9)], r=S.r)),
        line(seg(6.5, 9, 4.5, 21.5)),
        line(seg(12, 9, 14, 21.5)),
        line(seg(5.6, 14, 13, 14)),
        line(seg(5, 18, 13.4, 18)),
        line(seg(20.5, 7, 20.5, 21.5)),
    ]


@icon("running-singlet", CAT, "Sleeveless running top with a diagonal sash across the front",
      tags=["singlet", "tank top", "athletics", "track", "vest", "race wear"], aliases=["track-singlet"])
def _(S):
    body = [(7, 3), (9, 3), (10.5, 6.5), (13.5, 6.5), (15, 3), (17, 3), (16.5, 9), (17.5, 21), (6.5, 21), (7.5, 9)]
    return [
        shell(poly(body, closed=True, r=S.r)),
        detail(seg(8, 11, 16.8, 17)),
    ]


@icon("slam-dunk", CAT, "Player hanging from the hoop rim after a dunk",
      tags=["basketball", "dunk", "hoop", "rim", "jump", "backboard"], aliases=["dunk"])
def _(S):
    return [
        line(seg(21.5, 2.5, 21.5, 9)),
        line(seg(15, 7, 21.5, 7)),
        dot(8.5, 9, 2.25),
        line(poly([(15, 7), (12.5, 12.5)], r=S.r)),
        line(poly([(12.5, 12.5), (11, 17), (8.5, 21.5)], r=S.r)),
        line(poly([(11, 17), (14, 21.5)], r=S.r)),
        line(poly([(12.5, 12.5), (8.5, 14.5)], r=S.r)),
    ]


@icon("basketball-dribble", CAT, "Player bent low bouncing a ball beside the knee",
      tags=["basketball", "dribbling", "ball handling", "court", "bounce", "guard"], aliases=["dribble"])
def _(S):
    return [
        dot(8.5, 4.5, 2.25),
        line(poly([(9.5, 8), (11, 14)], r=S.r)),
        line(poly([(9.5, 9), (14, 12), (17, 14.5)], r=S.r)),
        line(poly([(11, 14), (7, 17), (5, 21.5)], r=S.r)),
        line(poly([(11, 14), (13, 18), (11.5, 21.5)], r=S.r)),
        shell(circle(19, 18.5, 2.5)),
    ]


@icon("field-goal-kick", CAT, "Player kicking an oval ball toward the goal posts",
      tags=["american football", "kicker", "kick", "gridiron", "uprights", "punt"], aliases=["place-kick"])
def _(S):
    return [
        dot(6, 5, 2.25),
        line(poly([(6, 8.5), (7, 14)], r=S.r)),
        line(poly([(6.5, 10), (10, 12)], r=S.r)),
        line(poly([(7, 14), (5, 21.5)], r=S.r)),
        line(poly([(7, 14), (10.5, 17.5), (13, 17.5)], r=S.r)),
        shell("M15 17.2A6 6 0 0 0 21 11.3A6 6 0 0 0 15 17.2Z"),
        detail(seg(16.8, 14.8, 19.2, 13.7)),
    ]


@icon("cricket-wicketkeeper", CAT, "Crouched wicketkeeper with large gloves behind the stumps",
      tags=["cricket", "keeper", "gloves", "stumps", "wicket", "catch"], aliases=["wicket-keeper"])
def _(S):
    return [
        dot(6.5, 6, 2.25),
        line(poly([(7.5, 9), (9, 14)], r=S.r)),
        line(poly([(7.5, 10), (11, 12.5)], r=S.r)),
        line(poly([(9, 14), (5.5, 17), (5.5, 21.5)], r=S.r)),
        line(poly([(9, 14), (11.5, 17.5), (10.5, 21.5)], r=S.r)),
        shell(circle(12, 12.5, 1.5)),
        line(seg(15, 8, 15, 21.5)), line(seg(18.5, 8, 18.5, 21.5)), line(seg(22, 8, 22, 21.5)),
    ]


@icon("golf-putting", CAT, "Golfer bent over a putter lining up a ball near the hole",
      tags=["golf", "putt", "putter", "green", "ball", "hole"], aliases=["putt"])
def _(S):
    return [
        dot(6.5, 4.5, 2.25),
        line(poly([(7, 8), (9, 14)], r=S.r)),
        line(poly([(7.5, 9), (12, 11.5)], r=S.r)),
        line(seg(12, 11.5, 14, 19.5)),
        line(seg(13, 19.5, 16, 19.5)),
        line(poly([(9, 14), (7.5, 21.5)], r=S.r)),
        line(poly([(9, 14), (11.5, 21.5)], r=S.r)),
        dot(18.5, 19.5, 1.2),
        line(seg(21.5, 11, 21.5, 21)),
    ]


@icon("grind-rail", CAT, "Low metal rail on two legs with a skateboard grinding on top",
      tags=["skateboard", "rail", "street skating", "trick", "skatepark", "grind"], aliases=["skate-rail"])
def _(S):
    return [
        line(poly([(4.5, 5), (6.5, 8.5), (17.5, 8.5), (19.5, 5)], r=S.r)),
        dot(8.5, 11, 1.2), dot(15.5, 11, 1.2),
        line(seg(2.5, 15, 21.5, 15)),
        line(seg(5.5, 15, 4.5, 21.5)),
        line(seg(18.5, 15, 19.5, 21.5)),
    ]


@icon("trophy-lift", CAT, "Figure lifting a large cup trophy high overhead",
      tags=["winner", "champion", "celebration", "cup", "victory", "title"], aliases=["lift-trophy"])
def _(S):
    return [
        shell(poly([(7.5, 2.5), (16.5, 2.5), (15.5, 6), (12, 7.5), (8.5, 6)], closed=True, r=S.r)),
        line(seg(12, 7.5, 12, 9.5)),
        line(seg(9.5, 9.5, 14.5, 9.5)),
        line(poly([(9.5, 9.5), (6.5, 13), (9, 17.5)], r=S.r)),
        line(poly([(14.5, 9.5), (17.5, 13), (15, 17.5)], r=S.r)),
        dot(12, 14, 2.0),
        line(poly([(8, 21.5), (9, 17.5), (15, 17.5), (16, 21.5)], r=S.r)),
    ]


@icon("darts-player", CAT, "Player with a dart cocked at eye level facing a dartboard",
      tags=["darts", "dart throw", "pub game", "dartboard", "aim", "throw"], aliases=["dart-thrower"])
def _(S):
    return [
        dot(5.5, 5, 2.25),
        line(poly([(5.5, 8.5), (6.5, 14)], r=S.r)),
        line(poly([(6, 9.5), (9.5, 9), (11.5, 7)], r=S.r)),
        line(seg(11.5, 7, 14, 7)),
        line(poly([(6.5, 14), (4, 21.5)], r=S.r)),
        line(poly([(6.5, 14), (10, 21.5)], r=S.r)),
        shell(circle(19, 8, 3.5)),
        dot(19, 8, 1),
    ]


@icon("strike-zone", CAT, "Three by three strike zone grid floating above home plate",
      tags=["baseball", "softball", "pitch", "umpire", "plate", "batter"], aliases=["pitch-zone"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 12, pick(S, 0.5, 2))),
        detail(seg(9.5, 2.5, 9.5, 14.5)), detail(seg(14.5, 2.5, 14.5, 14.5)),
        detail(seg(4.5, 6.5, 19.5, 6.5)), detail(seg(4.5, 10.5, 19.5, 10.5)),
        shell(poly([(7.5, 17.5), (16.5, 17.5), (16.5, 19.5), (12, 21.5), (7.5, 19.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("handball-court", CAT, "Top view of a handball court with a D-shaped goal area at each end",
      tags=["handball", "court", "pitch", "goal area", "top view", "indoor sport"])
def _(S):
    return [
        shell(rect(2.5, 5, 19, 14, pick(S, 0.5, 2))),
        detail(seg(12, 5, 12, 19)),
        detail(arc(2.5, 12, 5.5, -90, 90)),
        detail(arc(21.5, 12, 5.5, 90, 270)),
    ]


@icon("volleyball-court", CAT, "Top view of a volleyball court with a centre net line and an attack line on each side",
      tags=["volleyball", "court", "net", "attack line", "top view", "beach volleyball"])
def _(S):
    return [
        shell(rect(2.5, 5, 19, 14, pick(S, 0.5, 2))),
        detail(seg(12, 5, 12, 19)),
        detail(seg(7.5, 5, 7.5, 19)), detail(seg(16.5, 5, 16.5, 19)),
        line(seg(12, 2, 12, 5)), line(seg(12, 19, 12, 22)),
    ]


@icon("rugby-pitch", CAT, "Top view of a rugby pitch with H-shaped posts at each end and a halfway line",
      tags=["rugby", "pitch", "field", "goal posts", "try line", "top view"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 19, 15, pick(S, 0.5, 2))),
        detail(seg(12, 4.5, 12, 19.5)),
        detail(poly([(5.5, 9.5), (9, 9.5)])), detail(poly([(5.5, 14.5), (9, 14.5)])), detail(seg(7.2, 9.5, 7.2, 14.5)),
        detail(poly([(15, 9.5), (18.5, 9.5)])), detail(poly([(15, 14.5), (18.5, 14.5)])), detail(seg(16.8, 9.5, 16.8, 14.5)),
    ]


@icon("wall-bars", CAT, "Tall wooden ladder of horizontal rungs fixed flat against a wall",
      tags=["gymnastics", "stall bars", "swedish ladder", "exercise", "stretching", "gym"], aliases=["stall-bars"])
def _(S):
    parts = [line(seg(5, 2.5, 5, 21.5)), line(seg(19, 2.5, 19, 21.5))]
    for y in (4.5, 8.5, 12.5, 16.5, 20.5):
        parts.append(line(seg(5, y, 19, y)))
    return parts


@icon("vaulting-box", CAT, "Stacked wooden box sections topped with a padded cushion",
      tags=["gymnastics", "vault", "plinth", "box jump", "pommel", "school gym"], aliases=["plinth-box"])
def _(S):
    return [
        shell(rect(3, 3, 18, 4, pick(S, 0.5, 2))),
        shell(poly([(5, 9.5), (19, 9.5), (20, 14.5), (4, 14.5)], closed=True, r=S.r * 0.5)),
        shell(poly([(4, 16.5), (20, 16.5), (21, 21.5), (3, 21.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("backstroke-flags", CAT, "Line of small pennant flags strung across above a pool",
      tags=["swimming", "backstroke", "pool", "pennants", "lane", "warning flags"], aliases=["pool-flags"])
def _(S):
    tri = lambda x: sp(poly([(x - 2, 6), (x + 2, 6), (x, 11)], closed=True, r=S.r * 0.3))
    return [
        line(seg(2.5, 3, 2.5, 21.5)), line(seg(21.5, 3, 21.5, 21.5)),
        line(seg(2.5, 5, 21.5, 5)),
        tri(7), tri(12), tri(17),
        line(wave(S, 17.5, 5, 19, 3.5, 1)),
    ]


@icon("signed-ball", CAT, "Ball with a curved seam and a scribbled signature across its surface",
      tags=["autograph", "memorabilia", "souvenir", "signature", "fan", "collectible"], aliases=["autographed-ball"])
def _(S):
    sig = pick(S, "M10 17L11.5 13L13 17.5L14.5 13.5L16 16L18.5 13.5",
               "M10 16.5C11 12.5 12 12.5 12.5 15C13 17.5 13.7 14 14.8 14.3C16 14.6 16 16.5 18.5 13.5")
    return [
        shell(circle(12, 12, 9)),
        detail(pick(S, "M6 6L8 12L6 18", "M6 6C9 9.5 9 14.5 6 18")),
        detail(sig),
    ]


@icon("live-match", CAT, "Screen showing a ball with a live broadcast dot in the corner",
      tags=["broadcast", "streaming", "tv", "game on", "watch", "sports coverage"], aliases=["live-game"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 13, pick(S, 0.5, 2.5))),
        shell(circle(9.5, 10, 3)),
        dot(17, 7, 1.3),
        line(seg(8, 20.5, 16, 20.5)), line(seg(12, 16.5, 12, 20.5)),
    ]


@icon("championship-ring", CAT, "Chunky ring with a large raised gem on its top",
      tags=["jewelry", "title", "winner", "champion", "gem", "award"], aliases=["champion-ring"])
def _(S):
    return [
        shell(poly([(7, 2.5), (17, 2.5), (19.5, 7), (12, 12.5), (4.5, 7)], closed=True, r=S.r)),
        shell(circle(12, 16, 5.5)),
        detail(seg(7, 7, 17, 7)),
    ]


@icon("stadium-seat", CAT, "Folding stadium seat with a numbered back and a flip-up bottom",
      tags=["bleacher", "grandstand", "chair", "arena", "seating", "folding seat"], aliases=["bleacher-seat"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 13, 11, pick(S, 1, 3))),
        detail(poly([(10.5, 6.5), (12.5, 5), (12.5, 11)])),
        shell(poly([(5.5, 16), (18.5, 16), (18.5, 19), (5.5, 19)], closed=True, r=S.r * 0.6)),
        line(seg(8, 19, 8, 21.5)), line(seg(16, 19, 16, 21.5)),
    ]


@icon("line-marker-cart", CAT, "Small wheeled cart painting a white line on the grass",
      tags=["field marking", "groundskeeper", "pitch lines", "turf", "paint", "grounds"], aliases=["field-marker"])
def _(S):
    return [
        shell(rect(4.5, 4, 11, 8, pick(S, 0.5, 2))),
        line(poly([(15.5, 6), (20, 3.5)], r=S.r)),
        shell(circle(7, 15, 1.75)), shell(circle(13, 15, 1.75)),
        line(seg(2.5, 20.5, 21.5, 20.5)),
    ]


@icon("timing-chip", CAT, "Small plastic timing tag laced onto the top of a running shoe",
      tags=["race timing", "marathon", "shoe tag", "runner", "lap", "bib chip"], aliases=["shoe-chip"])
def _(S):
    shoe = [(3, 19), (3, 12), (8, 10.5), (11, 14), (18, 15), (21, 17.5), (21, 19)]
    return [
        shell(poly(shoe, closed=True, r=S.r)),
        detail(seg(8.5, 14, 10, 12.5)),
        line(seg(3, 21.5, 21, 21.5)),
        sp(rect(8, 3.5, 7, 5, pick(S, 0.3, 1))),
        line(seg(11.5, 8.5, 11.5, 10.5)),
    ]


@icon("skateboard-truck", CAT, "Skateboard truck with a baseplate, hanger and a wheel at each end of the axle",
      tags=["skateboard", "axle", "wheels", "hanger", "baseplate", "parts"], aliases=["skate-truck"])
def _(S):
    return [
        shell(rect(6, 3, 12, 4, pick(S, 0.5, 2))),
        shell(poly([(9, 9), (15, 9), (17, 14), (7, 14)], closed=True, r=S.r * 0.6)),
        line(seg(5, 17, 19, 17)),
        sp(rect(2.5, 12.5, 3.5, 9, pick(S, 0.5, 1.6))), sp(rect(18, 12.5, 3.5, 9, pick(S, 0.5, 1.6))),
    ]


@icon("footgolf", CAT, "Player kicking a soccer ball toward a flag in a large hole",
      tags=["soccer golf", "kick", "flag", "hole", "course", "ball"], aliases=["foot-golf"])
def _(S):
    return [
        dot(5, 5, 2.25),
        line(poly([(5, 8.5), (6, 14)], r=S.r)),
        line(poly([(5.5, 10), (9, 12)], r=S.r)),
        line(poly([(6, 14), (4, 21.5)], r=S.r)),
        line(poly([(6, 14), (9.5, 17.5), (10.5, 17.5)], r=S.r)),
        shell(circle(14, 18, 2)),
        line(seg(20.5, 4, 20.5, 21)),
        sp(poly([(20.5, 4), (20.5, 10), (15.5, 7)], closed=True)),
    ]


@icon("recurve-bow", CAT, "Recurve bow with flicked limb tips and a long stabilizer rod",
      tags=["archery", "bow", "olympic", "stabilizer", "string", "target shooting"], aliases=["olympic-bow"])
def _(S):
    bow = pick(S, "M3.5 3L10 5L15 8.5L16.5 12L15 15.5L10 19L3.5 21",
               "M3.5 3C10 4 16.5 7 16.5 12C16.5 17 10 20 3.5 21")
    return [
        line(bow),
        line(seg(3.5, 3, 3.5, 21)),
        sq(15, 10, 3.5, 4, pick(S, 0, 1)),
        line(seg(18, 12, 21.5, 12)),
        dot(21.5, 12, 1.25),
    ]


@icon("victory-lap", CAT, "Runner jogging with a large flag held up behind the shoulders",
      tags=["celebration", "winner", "jog", "flag", "stadium", "champion"], aliases=["lap-of-honour"])
def _(S):
    return [
        shell(poly([(2.5, 5.5), (6, 6.5), (10, 7), (10, 13), (6, 12.5), (2.5, 11.5)], closed=True, r=S.r)),
        dot(16.5, 5, 2.25),
        line(poly([(15, 8.5), (13, 14)], r=S.r)),
        line(poly([(14.8, 9.5), (19, 11.5)], r=S.r)),
        line(poly([(13, 14), (17, 16.5), (15.5, 21.5)], r=S.r)),
        line(poly([(13, 14), (9.5, 18), (7, 20.5)], r=S.r)),
    ]


@icon("stick-fighting", CAT, "Figure in a wide stance holding two short sticks crossed above the head",
      tags=["martial arts", "escrima", "arnis", "kali", "combat sport", "baton"], aliases=["escrima"])
def _(S):
    return [
        dot(12, 9.5, 2.25),
        line(seg(12, 13, 12, 17)),
        line(poly([(12, 13.5), (8.5, 14.5), (6.5, 10.5)], r=S.r)),
        line(poly([(12, 13.5), (15.5, 14.5), (17.5, 10.5)], r=S.r)),
        line(seg(5, 11.5, 16, 2.5)),
        line(seg(19, 11.5, 8, 2.5)),
        line(poly([(8, 21.5), (12, 17), (16, 21.5)], r=S.r)),
    ]


@icon("human-flag", CAT, "Figure gripping a vertical pole with the body held straight out sideways",
      tags=["calisthenics", "street workout", "strength", "pole", "bodyweight", "gymnastics"], aliases=["pole-flag"])
def _(S):
    return [
        line(seg(4.5, 2.5, 4.5, 21.5)),
        dot(11, 6.5, 2.25),
        line(poly([(4.5, 14), (8, 11)], r=S.r)),
        line(poly([(4.5, 9), (8, 11)], r=S.r)),
        line(seg(8, 11, 15, 11)),
        line(poly([(15, 11), (21.5, 8.5)], r=S.r)),
        line(poly([(15, 11), (21.5, 14.5)], r=S.r)),
    ]


@icon("aerial-hoop", CAT, "Performer posed inside a large ring hanging from a single rope",
      tags=["lyra", "aerial arts", "circus", "acrobat", "silks", "performer"], aliases=["lyra-hoop"])
def _(S):
    return [
        line(seg(12, 2, 12, 6)),
        line(circle(12, 14.5, 8)),
        dot(12, 9.5, 2),
        line(seg(12, 12, 12, 16.5)),
        line(seg(8.5, 12, 15.5, 12)),
        line(poly([(8.5, 20), (12, 16.5), (15.5, 20)], r=S.r)),
    ]


@icon("outfielder-catch", CAT, "Fielder leaping with a gloved hand raised to catch a high ball",
      tags=["baseball", "softball", "fly ball", "glove", "diving catch", "fielding"], aliases=["fly-ball-catch"])
def _(S):
    return [
        dot(8.5, 8, 2.25),
        line(poly([(9.5, 11), (10.5, 16.5)], r=S.r)),
        line(poly([(9.8, 12), (14.5, 8)], r=S.r)),
        shell(circle(16, 6, 2)),
        dot(21, 3.5, 1.3),
        line(poly([(9.8, 12.5), (6, 13.5)], r=S.r)),
        line(poly([(10.5, 16.5), (14.5, 18.5), (13.5, 21.5)], r=S.r)),
        line(poly([(10.5, 16.5), (7, 18.5), (5.5, 21.5)], r=S.r)),
    ]


@icon("netball-player", CAT, "Player holding a ball high with both hands beside a goal ring",
      tags=["netball", "shooter", "goal ring", "pivot", "ball", "court"], aliases=["netball-shooter"])
def _(S):
    return [
        line(seg(21.5, 2.5, 21.5, 21.5)),
        line(seg(17, 7, 21.5, 7)),
        shell(circle(11, 4.5, 2.25)),
        line(poly([(9, 14.5), (6, 10), (8.8, 6.5)], r=S.r)),
        line(poly([(13, 14.5), (16, 10), (13.2, 6.5)], r=S.r)),
        dot(11, 11, 2),
        line(poly([(9, 14.5), (11, 15.5), (13, 14.5)], r=S.r)),
        line(seg(11, 15.5, 11, 18.5)),
        line(poly([(7.5, 21.5), (11, 18.5), (14.5, 21.5)], r=S.r)),
    ]


@icon("squash-player", CAT, "Player lunging low with a racket toward a ball near the front wall",
      tags=["squash", "racquet", "lunge", "court", "wall", "rally"], aliases=["squash-lunge"])
def _(S):
    return [
        line(seg(21.5, 2.5, 21.5, 21.5)),
        dot(7, 5.5, 2.25),
        line(poly([(7.5, 9), (9.5, 14)], r=S.r)),
        line(poly([(8, 10), (12, 10.5), (13.5, 8.5)], r=S.r)),
        shell(circle(16, 6, 2.2)),
        line(poly([(9.5, 14), (14, 16), (14.5, 21.5)], r=S.r)),
        line(poly([(9.5, 14), (5.5, 18), (3.5, 21.5)], r=S.r)),
        dot(18, 17.5, 1.2),
    ]


@icon("ultimate-disc", CAT, "Player leaping sideways to catch a flying disc",
      tags=["ultimate", "flying disc", "disc golf", "catch", "leap", "team sport"], aliases=["disc-catch"])
def _(S):
    return [
        shell(ellipse(18.5, 4.5, 3.2, 1.2)),
        dot(7, 8, 2.25),
        line(poly([(8.5, 11), (12.5, 16)], r=S.r)),
        line(poly([(9, 11.5), (13.5, 8), (16, 6.5)], r=S.r)),
        line(poly([(9, 11.5), (5, 13.5)], r=S.r)),
        line(poly([(12.5, 16), (17.5, 17.5), (20, 21)], r=S.r)),
        line(poly([(12.5, 16), (10, 20), (6.5, 21.5)], r=S.r)),
    ]


@icon("hockey-goalie", CAT, "Crouched goalie in a mask and large leg pads holding a stick",
      tags=["ice hockey", "goalkeeper", "pads", "mask", "save", "netminder"], aliases=["goaltender"])
def _(S):
    return [
        shell(circle(12, 5.5, 2.75)),
        detail(seg(9.8, 5.5, 14.2, 5.5)),
        shell(rect(8.5, 10, 7, 6, pick(S, 0.5, 2))),
        line(poly([(8.5, 11), (5, 12.5)], r=S.r)),
        sq(2.5, 11.5, 3, 3, pick(S, 0.3, 1)),
        shell(rect(7, 16.5, 4, 5, pick(S, 0.3, 1.2))), shell(rect(13, 16.5, 4, 5, pick(S, 0.3, 1.2))),
        line(poly([(20.5, 8), (20.5, 21), (18, 21)], r=S.r)),
    ]


@icon("guide-runner", CAT, "Two runners side by side joined at the hands by a short tether",
      tags=["blind running", "para athletics", "visually impaired", "partner", "tether", "inclusive sport"], aliases=["running-guide"])
def _(S):
    def runner(x):
        return [
            dot(x + 1.5, 5, 2.0),
            line(poly([(x + 0.5, 8.5), (x - 1, 14)], r=S.r)),
            line(poly([(x + 0.5, 9.5), (x + 3.5, 11.5)], r=S.r)),
            line(poly([(x - 1, 14), (x + 2.5, 17), (x + 1.5, 21.5)], r=S.r)),
            line(poly([(x - 1, 14), (x - 3.5, 18), (x - 5, 21)], r=S.r)),
        ]
    return runner(7.5) + runner(17.5) + [line(seg(11, 11.5, 14.5, 11.5))]


@icon("aid-station", CAT, "Table lined with cups and a runner reaching to grab one",
      tags=["marathon", "water stop", "hydration", "race support", "cups", "refreshments"], aliases=["water-station"])
def _(S):
    cup = lambda x: sp(poly([(x - 1.4, 11.5), (x + 1.4, 11.5), (x + 1, 15), (x - 1, 15)], closed=True))
    return [
        line(seg(2.5, 16, 13.5, 16)),
        line(seg(4, 16, 4, 21.5)), line(seg(12, 16, 12, 21.5)),
        cup(4.5), cup(8), cup(11.5),
        dot(19, 5.5, 2.25),
        line(poly([(18.5, 9), (18, 14)], r=S.r)),
        line(poly([(18.5, 10), (15.5, 11)], r=S.r)),
        line(poly([(18, 14), (21, 17.5), (20, 21.5)], r=S.r)),
        line(poly([(18, 14), (16.5, 18), (17, 21.5)], r=S.r)),
    ]


@icon("coxswain", CAT, "Small figure seated at the stern of a rowing boat calling through a megaphone",
      tags=["rowing", "crew", "boat", "megaphone", "steer", "regatta"], aliases=["cox"])
def _(S):
    return [
        shell(poly([(2.5, 15.5), (21.5, 15.5), (18.5, 20), (5.5, 20)], closed=True, r=S.r)),
        dot(17.5, 8, 2.25),
        line(seg(17.5, 11, 17.5, 15.5)),
        line(poly([(17.5, 12), (14.5, 11)], r=S.r)),
        sp(poly([(14.5, 8.5), (9.5, 6), (9.5, 12.5), (14.5, 10.5)], closed=True)),
    ]


@icon("climbing-wall", CAT, "Tall wall panel covered with scattered holds of different shapes",
      tags=["bouldering", "indoor climbing", "holds", "gym", "wall", "route"], aliases=["boulder-wall"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, pick(S, 0.5, 2.5))),
        dot(8.5, 7, 1.5), sq(14, 5.5, 3, 2.5, pick(S, 0, 0.8)),
        sp(poly([(10.5, 14), (13.5, 14), (12, 11)], closed=True)),
        dot(16, 13.5, 1.2), sq(7, 15.5, 2.5, 3, pick(S, 0, 0.8)), dot(13.5, 18.5, 1.5),
    ]


@icon("wrestling-mask", CAT, "Full head mask with almond eye cutouts, a zigzag crest and an open mouth",
      tags=["lucha libre", "luchador", "wrestler", "face mask", "costume", "ring"])
def _(S):
    head = pick(S, "M12 2.5L17.5 4.5L20 10L19 16L15.5 21.5H8.5L5 16L4 10L6.5 4.5Z",
                "M12 2.5C7.5 2.5 4 5.5 4 10.5V15L8 21.5H16L20 15V10.5C20 5.5 16.5 2.5 12 2.5Z")
    return [
        shell(head),
        detail(poly([(8, 5.5), (10, 8), (12, 5.5), (14, 8), (16, 5.5)], r=S.r * 0.5)),
        sp("M6.5 12.5C8 10 10.5 10.5 11 12.5C9.5 14.5 7.5 14.5 6.5 12.5Z"),
        sp("M17.5 12.5C16 10 13.5 10.5 13 12.5C14.5 14.5 16.5 14.5 17.5 12.5Z"),
        sp(pick(S, "M10 17L14 17L13 19.5L11 19.5Z", "M10 17.2C11.5 16.6 12.5 16.6 14 17.2L13 19.3H11Z")),
    ]


@icon("rebounder-net", CAT, "Angled square frame with a taut net returning a ball",
      tags=["rebound net", "training", "practice", "football", "tennis", "return wall"], aliases=["rebound-net"])
def _(S):
    A, B, D = (3, 9), (15, 5), (6, 20)
    C = (B[0] + D[0] - A[0], B[1] + D[1] - A[1])
    pt = lambda u, v: (A[0] + u * (B[0] - A[0]) + v * (D[0] - A[0]), A[1] + u * (B[1] - A[1]) + v * (D[1] - A[1]))
    parts = [shell(poly([A, B, C, D], closed=True, r=S.r))]
    for t in (1 / 3, 2 / 3):
        parts.append(detail(seg(*pt(t, 0), *pt(t, 1))))
        parts.append(detail(seg(*pt(0, t), *pt(1, t))))
    parts.append(shell(circle(19.5, 5, 2)))
    return parts


@icon("golf-hole-map", CAT, "Top view of a leaf-shaped fairway running from the tee to a round green with a flag",
      tags=["golf course", "hole layout", "fairway", "green", "tee", "yardage"], aliases=["hole-layout"])
def _(S):
    fw = pick(S, "M3 21L3.5 14.5L7.5 11L14.5 9L14 14L10 18.5Z",
              "M3 21C2 15 7 10 14.5 9C15 15 10.5 21 3 21Z")
    return [
        shell(fw),
        dot(6.5, 17, 1.2),
        shell(circle(18.5, 7, 3.2)),
        line(seg(18.5, 7, 18.5, 2.5)) if False else dot(18.5, 7, 1),
    ]


@icon("golf-rangefinder", CAT, "Compact handheld rangefinder with a lens at one end and a small flag above",
      tags=["golf", "distance", "laser", "range finder", "yardage", "scope"], aliases=["laser-rangefinder"])
def _(S):
    return [
        shell(circle(6.5, 14, 4)),
        shell(rect(11, 11, 10, 6, pick(S, 0.5, 2.5))),
        dot(6.5, 14, 1.2),
        line(seg(16, 11, 16, 4)),
        sp(poly([(16, 3.5), (20, 5), (16, 6.5)], closed=True)),
    ]


@icon("wing-chun-dummy", CAT, "Upright wooden post with three short arms and a leg sticking out",
      tags=["martial arts", "training dummy", "kung fu", "mook jong", "wooden dummy", "dojo"], aliases=["wooden-dummy"])
def _(S):
    return [
        shell(rect(10, 2.5, 4, 19, pick(S, 0.5, 2))),
        line(seg(3.5, 6.5, 10, 6.5)), line(seg(14, 6.5, 20.5, 6.5)),
        line(seg(3.5, 11.5, 10, 11.5)),
        line(poly([(14, 15.5), (19.5, 15.5), (19.5, 20)], r=S.r)),
    ]


@icon("bowling-strike", CAT, "Ball crashing into a group of pins that fly apart",
      tags=["bowling", "strike", "pins", "alley", "lane", "knock down"], aliases=["strike-pins"])
def _(S):
    def pin(x, y, deg):
        a = math.radians(deg)
        pts = [(-1.2, -3.5), (1.2, -3.5), (1.2, -1.5), (2.2, 1.5), (2.2, 3.5), (-2.2, 3.5), (-2.2, 1.5), (-1.2, -1.5)]
        rp = [(x + px * math.cos(a) - py * math.sin(a), y + px * math.sin(a) + py * math.cos(a)) for px, py in pts]
        return sp(poly(rp, closed=True, r=pick(S, 0, 1.0)))
    return [
        shell(circle(6.5, 17, 4)),
        dot(5.5, 15.5, 0.8), dot(7.8, 15.8, 0.8),
        pin(16, 5, -25), pin(20, 12, 35), pin(15, 17.5, 80),
    ]
