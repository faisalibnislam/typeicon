"""TypeIcon Core: sports gear, batch 002 (athletes, track and field, gymnastics, combat sports)."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import polar

CAT = "sports-gear"


def L(S, a, b):
    """Line value, Rounded value."""
    return a if S.name == "line" else b


def sq(x, y, w, h, rx=0.0) -> Part:
    return Part("dot", rect(x, y, w, h, rx))


def rrect(cx, cy, w, h, deg, r=0.0):
    """Rotated rectangle polygon points (deg rotates the long axis h from vertical, clockwise)."""
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    pts = []
    for x, y in [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]:
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return pts


# ============================================================================ team sports

@icon("volleyball-player", CAT, "Player jumping with one arm raised to spike a ball",
      tags=["volleyball", "spike", "jump", "player", "athlete", "net sports"], aliases=[])
def _(S):
    return [
        dot(9, 8, 2.25),
        line(poly([(9.5, 11), (10.5, 16)], r=S.r)),
        line(poly([(9.8, 11.5), (14, 6.5)], r=S.r)),
        line(poly([(9.8, 11.5), (5, 10)], r=S.r)),
        line(poly([(10.5, 16), (7.5, 18.5), (8.5, 21.5)], r=S.r)),
        line(poly([(10.5, 16), (14, 18), (12.5, 21.5)], r=S.r)),
        line(circle(18, 5.5, 3)),
    ]


@icon("volleyball-dig", CAT, "Crouched player bumping a ball upward with joined forearms",
      tags=["volleyball", "dig", "bump", "forearm pass", "defense", "player"], aliases=[])
def _(S):
    return [
        dot(7.5, 6.5, 2.25),
        line(poly([(8.5, 9.5), (7, 15)], r=S.r)),
        line(poly([(8.5, 10), (15, 14)], r=S.r)),
        line(poly([(7, 15), (11, 17.5), (10, 21.5)], r=S.r)),
        line(poly([(7, 15), (4.5, 18), (5, 21.5)], r=S.r)),
        line(circle(17, 6.5, 3)),
    ]


@icon("ice-hockey-player", CAT, "Skater bent forward with a stick driving a puck across the ice",
      tags=["ice hockey", "skater", "stick", "puck", "player", "winter sports"], aliases=[])
def _(S):
    return [
        dot(7.5, 5, 2.25),
        line(poly([(8.5, 8), (11, 13)], r=S.r)),
        line(poly([(9, 8.8), (13, 11.5), (19, 17)], r=S.r)),
        line(poly([(19, 17), (21.5, 19)], r=S.r)),
        line(poly([(11, 13), (7.5, 16.5), (4, 16.5)], r=S.r)),
        line(poly([(11, 13), (13, 17), (10.5, 20)], r=S.r)),
        sq(14, 19.5, 4, 2),
    ]


@icon("field-hockey-player", CAT, "Running player bent low with a hooked stick pushing a ball",
      tags=["field hockey", "hockey", "player", "hooked stick", "ball", "running"], aliases=[])
def _(S):
    return [
        dot(8, 5, 2.25),
        line(poly([(9, 8), (8, 14)], r=S.r)),
        line(poly([(9, 9), (14, 11), (18, 17.5)], r=S.r)),
        line(poly([(18, 17.5), (17.5, 20.5), (14.5, 20.5)], r=S.r)),
        line(poly([(8, 14), (12, 16), (10.5, 21)], r=S.r)),
        line(poly([(8, 14), (4.5, 17), (3.5, 21)], r=S.r)),
        dot(20.5, 20, 1.5),
    ]


@icon("lacrosse-player", CAT, "Running player holding a netted stick high with a ball cradled in it",
      tags=["lacrosse", "stick", "net", "player", "cradle", "team sport"], aliases=[])
def _(S):
    return [
        dot(7, 7, 2.25),
        line(poly([(8, 10), (8.5, 15)], r=S.r)),
        line(poly([(8, 10.5), (12, 13.5), (15, 9)], r=S.r)),
        line(seg(12.5, 12.5, 15.5, 8)),
        line(poly([(15.5, 8), (14.5, 4.5), (17.5, 2.5), (20.5, 4.5), (19.5, 8.5), (15.5, 8)], r=S.r)),
        line(poly([(8.5, 15), (12.5, 18), (11, 21.5)], r=S.r)),
        line(poly([(8.5, 15), (5, 17.5), (3.5, 21)], r=S.r)),
    ]


@icon("cricket-batter", CAT, "Batter in a ready stance with a flat bat about to meet a ball",
      tags=["cricket", "batter", "batsman", "bat", "strike", "wicket"], aliases=["batsman"])
def _(S):
    return [
        dot(7.5, 4.5, 2.25),
        line(poly([(7.5, 8), (7.5, 14)], r=S.r)),
        line(poly([(7.5, 9), (11.5, 12)], r=S.r)),
        line(seg(11.5, 12, 14.8, 14.6)),
        shell(poly(rrect(17.3, 18, 3.2, 8, -38), closed=True, r=L(S, 0, 1))),
        line(poly([(7.5, 14), (6, 21.5)], r=S.r)),
        line(poly([(7.5, 14), (10, 21.5)], r=S.r)),
        dot(20.5, 7, 1.5),
    ]


@icon("cricket-bowler", CAT, "Bowler in delivery stride with the bowling arm straight overhead",
      tags=["cricket", "bowler", "bowling", "delivery", "overarm", "pitch"], aliases=[])
def _(S):
    return [
        dot(8.5, 6.5, 2.25),
        line(poly([(9.5, 9.5), (9.5, 15)], r=S.r)),
        line(poly([(9.8, 9.8), (14, 2.5)], r=S.r)),
        line(poly([(9.5, 10.5), (5, 12.5)], r=S.r)),
        line(poly([(9.5, 15), (5, 21.5)], r=S.r)),
        line(poly([(9.5, 15), (15.5, 17), (18.5, 21.5)], r=S.r)),
        dot(17.5, 3, 1.5),
    ]


@icon("golfer", CAT, "Golfer bent over in the stance with the club resting behind a ball",
      tags=["golf", "golfer", "swing", "address", "club", "course"], aliases=[])
def _(S):
    return [
        dot(7, 4.5, 2.25),
        line(poly([(8, 7.5), (7.5, 14)], r=S.r)),
        line(poly([(8.2, 8.5), (11.5, 13)], r=S.r)),
        line(poly([(11.5, 13), (15, 20.5), (17.5, 20.5)], r=S.r)),
        line(poly([(7.5, 14), (5, 21.5)], r=S.r)),
        line(poly([(7.5, 14), (10, 21.5)], r=S.r)),
        dot(21, 19.5, 1.5),
    ]


@icon("hurling-player", CAT, "Running player balancing a small ball on a flat-bladed stick",
      tags=["hurling", "camogie", "hurley", "stick", "ball", "gaelic"], aliases=["hurley"])
def _(S):
    return [
        dot(7, 7, 2.25),
        line(poly([(7.5, 10), (7, 15.5)], r=S.r)),
        line(poly([(7.5, 11), (12, 13.5), (14.5, 11)], r=S.r)),
        line(seg(14, 11.5, 17.5, 8.5)),
        shell(poly(rrect(19, 7, 3, 5.5, 40), closed=True, r=L(S, 0, 0.8))),
        line(poly([(7, 15.5), (11, 18), (9.5, 21.5)], r=S.r)),
        line(poly([(7, 15.5), (4, 17.5), (3, 21)], r=S.r)),
        dot(15.5, 3.5, 1.5),
    ]

@icon("kabaddi", CAT, "Raider lunging forward with one hand stretched out to tag a defender",
      tags=["kabaddi", "raider", "tag", "contact sport", "lunge", "south asian sport"], aliases=[])
def _(S):
    return [
        dot(9, 6, 2.25),
        line(poly([(9.5, 9), (9, 14)], r=S.r)),
        line(poly([(9.5, 10), (15, 9), (21, 8)], r=S.r)),
        line(poly([(9.5, 10), (5, 12.5), (3, 11)], r=S.r)),
        line(poly([(9, 14), (14.5, 14), (15.5, 21.5)], r=S.r)),
        line(poly([(9, 14), (6, 17.5), (3.5, 21.5)], r=S.r)),
    ]


@icon("bowling-player", CAT, "Bowler crouched forward releasing a ball down the lane",
      tags=["bowling", "tenpin", "bowler", "release", "lane", "strike"], aliases=[])
def _(S):
    return [
        dot(8, 5, 2.25),
        line(poly([(9, 8), (10, 13.5)], r=S.r)),
        line(poly([(9.2, 9), (6, 12), (7.5, 16)], r=S.r)),
        line(poly([(9.2, 9), (12.5, 10.5), (13.5, 14)], r=S.r)),
        line(poly([(10, 13.5), (14.5, 17), (13, 21.5)], r=S.r)),
        line(poly([(10, 13.5), (6, 17.5), (3, 21)], r=S.r)),
        shell(circle(18.5, 19, 3)),
    ]


@icon("billiards-player", CAT, "Player leaning over a table to line up a shot with a long cue",
      tags=["billiards", "pool", "snooker", "cue", "player", "table"], aliases=[])
def _(S):
    return [
        dot(5, 5.5, 2.25),
        line(poly([(5.5, 8.5), (5, 15)], r=S.r)),
        line(poly([(5.5, 10), (9.5, 12.5)], r=S.r)),
        line(seg(6.5, 10.8, 17, 13.8)),
        dot(20, 14.5, 1.5),
        line(seg(9, 18, 22.5, 18)),
        line(seg(11, 18, 11, 21.5)), line(seg(21, 18, 21, 21.5)),
        line(poly([(5, 15), (3, 21.5)], r=S.r)),
        line(poly([(5, 15), (7.5, 21.5)], r=S.r)),
    ]


@icon("referee", CAT, "Official with a whistle in the mouth and one arm pointing out",
      tags=["referee", "umpire", "official", "whistle", "foul", "judge"], aliases=[])
def _(S):
    return [
        dot(9, 5.5, 2.25),
        line(seg(11, 5.5, 13.5, 5.5)),
        dot(14.5, 7, 1.8),
        line(poly([(9, 8.5), (9, 15)], r=S.r)),
        line(poly([(9, 9.5), (15.5, 12), (21.5, 10.5)], r=S.r)),
        line(poly([(9, 9.5), (4.5, 12)], r=S.r)),
        line(poly([(9, 15), (6, 21.5)], r=S.r)),
        line(poly([(9, 15), (12.5, 21.5)], r=S.r)),
    ]


@icon("foam-finger", CAT, "Oversized foam hand with the index finger pointing up",
      tags=["foam finger", "number one", "fan", "supporter", "cheer", "spectator", "mitt"], aliases=[])
def _(S):
    return [
        shell(poly([(9, 3), (14, 3), (14, 10.5), (19, 10.5), (19, 18), (6, 18), (6, 15), (3, 12.5), (4.5, 10), (9, 12.5)], closed=True, r=S.r)),
        shell(rect(7.5, 18, 10, 3.5, L(S, 0, 1))),
        detail(seg(11.5, 10.5, 11.5, 14.5)),
    ]


@icon("bleachers", CAT, "Stepped rows of bench seating with spectators sitting on them",
      tags=["bleachers", "stands", "grandstand", "seating", "spectators", "stadium", "crowd"], aliases=["grandstand"])
def _(S):
    return [
        shell(poly([(2, 21.5), (2, 17), (8, 17), (8, 12.5), (14, 12.5), (14, 8), (21, 8), (21, 21.5)], closed=True, r=S.r)),
        detail(seg(8, 17.5, 8, 21.5)), detail(seg(14, 13, 14, 21.5)),
        dot(5, 14, 1.5), dot(11, 9.5, 1.5), dot(17.5, 5, 1.5),
    ]


@icon("stadium-floodlight", CAT, "Tall mast topped by a rectangular bank of lamps",
      tags=["floodlight", "stadium lights", "lamp", "mast", "night game", "pitch lighting"], aliases=[])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 7, L(S, 0, 2))),
        dot(8.5, 6, 1.1), dot(12, 6, 1.1), dot(15.5, 6, 1.1),
        line(seg(12, 9.5, 12, 21.5)),
        line(seg(8, 21.5, 16, 21.5)),
    ]


@icon("championship-belt", CAT, "Wide belt with a large ornate central plate between two straps",
      tags=["championship belt", "title belt", "champion", "boxing", "wrestling", "prize"], aliases=[])
def _(S):
    return [
        shell(poly(regular(12, 12, 6.5, 8, -67.5), closed=True, r=S.r)),
        dot(12, 12, 1.8),
        line(seg(2, 9.5, 5.7, 9.5)), line(seg(2, 14.5, 5.7, 14.5)),
        line(seg(18.3, 9.5, 22, 9.5)), line(seg(18.3, 14.5, 22, 14.5)),
    ]


@icon("award-rosette", CAT, "Pleated round rosette with two ribbon tails hanging below",
      tags=["rosette", "ribbon", "prize", "award", "first place", "show winner", "badge"], aliases=[])
def _(S):
    pts = []
    for i in range(24):
        pts.append(polar(12, 9, 7 if i % 2 == 0 else 5.6, -90 + i * 15))
    return [
        shell(poly(pts, closed=True, r=S.r * 0.6)),
        detail(circle(12, 9, 2)),
        shell(poly([(8, 15), (5.5, 22), (8.5, 20.5), (10.5, 22), (11.5, 16)], closed=True, r=S.r * 0.4)),
        shell(poly([(16, 15), (18.5, 22), (15.5, 20.5), (13.5, 22), (12.5, 16)], closed=True, r=S.r * 0.4)),
    ]


@icon("trophy-shield", CAT, "Shield-shaped plaque with name plates standing on a base",
      tags=["shield", "plaque", "trophy", "award", "crest", "commemorative", "prize"], aliases=[])
def _(S):
    return [
        shell(poly([(5, 2.5), (19, 2.5), (19, 10), (12, 17.5), (5, 10)], closed=True, r=S.r)),
        detail(seg(9, 7, 15, 7)),
        detail(seg(9.5, 10.5, 14.5, 10.5)),
        shell(rect(6, 17.5, 12, 4, L(S, 0, 1))),
    ]


@icon("race-bib", CAT, "Rectangular race number bib with a safety pin in each corner",
      tags=["bib", "race number", "marathon", "runner", "entry number", "competitor", "event"], aliases=[])
def _(S):
    return [
        shell(rect(3.5, 4, 17, 16, S.R)),
        detail(poly([(9, 9), (15, 9), (11.5, 16.5)], r=S.r)),
        dot(6.8, 7.3, 1), dot(17.2, 7.3, 1), dot(6.8, 16.7, 1), dot(17.2, 16.7, 1),
    ]


@icon("sports-water-bottle", CAT, "Squeeze bottle with a pull-up nozzle cap and grip ridges",
      tags=["water bottle", "squeeze bottle", "hydration", "drink", "gym", "cycling bottle", "refill"], aliases=[])
def _(S):
    return [
        line(seg(12, 2, 12, 4.5)),
        shell(rect(8.5, 5.5, 7, 3.5, L(S, 0, 1))),
        shell(poly([(9.5, 12), (14.5, 12), (17, 14), (17, 21), (7, 21), (7, 14)], closed=True, r=S.r)),
        detail(seg(10, 17, 14, 17)),
    ]


@icon("ball-bag", CAT, "Mesh drawstring bag with a ball peeking out of the gathered top",
      tags=["ball bag", "mesh bag", "equipment bag", "drawstring", "balls", "team kit", "training"], aliases=[])
def _(S):
    return [
        line(circle(12, 4.8, 2.8)),
        shell(poly([(9, 10), (15, 10), (20, 21.5), (4, 21.5)], closed=True, r=S.r)),
        dot(9.5, 15.5, 1), dot(14.5, 15.5, 1), dot(7.5, 19, 1), dot(12, 19, 1), dot(16.5, 19, 1),
    ]


@icon("finish-arch", CAT, "Inflatable arch over a road with a banner across the top",
      tags=["finish arch", "inflatable arch", "race finish", "marathon", "banner", "gate", "event"], aliases=[])
def _(S):
    if S.name == "line":
        d = "M3 21.5V11a9 9 0 0 1 18 0V21.5H16.5V11a4.5 4.5 0 0 0-9 0V21.5Z"
    else:
        d = ("M3 11a9 9 0 0 1 18 0V20a1.5 1.5 0 0 1-1.5 1.5H18a1.5 1.5 0 0 1-1.5-1.5V11a4.5 4.5 0 0 0-9 0V20"
             "a1.5 1.5 0 0 1-1.5 1.5H4.5A1.5 1.5 0 0 1 3 20Z")
    return [
        shell(d),
        detail(seg(8, 10.5, 16, 10.5)),
    ]


@icon("team-huddle", CAT, "Ring of players seen from above with arms linked around each other",
      tags=["huddle", "team", "teamwork", "players", "circle", "pep talk", "group"], aliases=[])
def _(S):
    parts = []
    for i in range(5):
        a = -90 + i * 72
        x, y = polar(12, 12, 4.3, a)
        parts.append(dot(x, y, 1.9))
        parts.append(line(arc(12, 12, 8.5, a - 25, a + 25)))
    return parts


# ============================================================================ track and field

@icon("sprint-start", CAT, "Sprinter crouched in the set position with hands on the ground and hips raised",
      tags=["sprint", "start", "set position", "crouch", "sprinter", "100m", "track"], aliases=[])
def _(S):
    return [
        dot(16, 7.5, 2.25),
        line(poly([(13.5, 10), (14.5, 19)], r=S.r)),
        line(poly([(13.5, 10), (7, 10.5)], r=S.r)),
        line(poly([(7, 10.5), (10.5, 15), (8, 19.5)], r=S.r)),
        line(poly([(7, 10.5), (4, 16), (2.5, 19)], r=S.r)),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("starting-blocks", CAT, "Pair of angled foot pedals on a rail, side view",
      tags=["starting blocks", "sprint start", "foot pedals", "track", "sprint", "race start"], aliases=[])
def _(S):
    return [
        shell(poly(rrect(9, 14.5, 3.5, 9, -28), closed=True, r=L(S, 0, 1))),
        shell(poly(rrect(16, 14.5, 3.5, 9, -28), closed=True, r=L(S, 0, 1))),
        line(seg(3, 21, 21, 21)),
    ]


@icon("hurdling", CAT, "Athlete in full stride with the lead leg stretched out over a hurdle",
      tags=["hurdles", "hurdling", "hurdler", "track", "obstacle", "110m hurdles"], aliases=["hurdler"])
def _(S):
    return [
        dot(8, 4.5, 2.25),
        line(poly([(8.5, 7.5), (7, 12.5)], r=S.r)),
        line(poly([(8.5, 8.5), (12, 6)], r=S.r)),
        line(poly([(8.5, 8.5), (4, 9)], r=S.r)),
        line(poly([(7, 12.5), (13, 11), (18.5, 10.5)], r=S.r)),
        line(poly([(7, 12.5), (3.5, 15.5), (6.5, 18.5)], r=S.r)),
        line(seg(13, 15.5, 21, 15.5)),
        line(seg(14, 15.5, 14, 21.5)), line(seg(20, 15.5, 20, 21.5)),
    ]


@icon("relay-baton", CAT, "Hollow tube baton with curved motion marks showing it being passed on",
      tags=["baton", "relay", "handoff", "pass", "4x100", "team race", "track"], aliases=[])
def _(S):
    return [
        shell(poly(rrect(12, 12, 4.5, 14, 45), closed=True, r=L(S, 0, 1))),
        line(arc(12, 12, 10, 200, 250)),
        line(arc(12, 12, 10, 20, 70)),
    ]


@icon("finish-line-tape", CAT, "Runner with both arms raised breaking a tape stretched across the track",
      tags=["finish line", "finish tape", "winner", "victory", "race", "runner", "first place"], aliases=[])
def _(S):
    return [
        dot(12, 5, 2.25),
        line(poly([(6, 3.5), (12, 8.5), (18, 3.5)], r=S.r)),
        line(poly([(12, 8.5), (12, 15)], r=S.r)),
        line(poly([(12, 15), (8.5, 21.5)], r=S.r)),
        line(poly([(12, 15), (15.5, 21.5)], r=S.r)),
        line(poly([(2, 9.5), (7, 11.5), (12, 11.5), (17, 11.5), (22, 9.5)], r=0)),
    ]


@icon("long-jump", CAT, "Jumper flying forward with legs extended toward a sand pit",
      tags=["long jump", "jumper", "sand pit", "leap", "track and field", "distance"], aliases=[])
def _(S):
    return [
        dot(9, 4.5, 2.25),
        line(poly([(9, 7.5), (8, 12.5)], r=S.r)),
        line(poly([(8.8, 8.5), (5, 5), (3, 6)], r=S.r)),
        line(poly([(8.8, 8.5), (13, 6)], r=S.r)),
        line(poly([(8, 12.5), (14, 13), (18.5, 11)], r=S.r)),
        line(poly([(8, 12.5), (12, 16), (15.5, 15)], r=S.r)),
        line(seg(2, 21.5, 8, 21.5)),
        shell(rect(11.5, 18.5, 10.5, 3.5, 0)),
    ]


@icon("triple-jump", CAT, "Jumper bounding through the air with three landing marks on the ground",
      tags=["triple jump", "hop step jump", "bound", "jumper", "track and field", "footprints"], aliases=[])
def _(S):
    return [
        dot(12, 4.5, 2.25),
        line(poly([(12, 7.5), (11.5, 12.5)], r=S.r)),
        line(poly([(12, 8.5), (8, 6), (5.5, 8)], r=S.r)),
        line(poly([(12, 8.5), (16, 6.5), (19, 8.5)], r=S.r)),
        line(poly([(11.5, 12.5), (15, 15), (14, 17)], r=S.r)),
        line(poly([(11.5, 12.5), (8, 14.5), (6.5, 17.5)], r=S.r)),
        dot(4.5, 20.5, 1.5), dot(12, 20.5, 1.5), dot(19.5, 20.5, 1.5),
    ]


@icon("javelin-throw", CAT, "Thrower leaning back with the arm drawn behind to launch a long javelin",
      tags=["javelin", "throw", "thrower", "spear", "track and field", "field event"], aliases=[])
def _(S):
    return [
        dot(11, 6.5, 2.25),
        line(poly([(11.5, 9.5), (11, 15)], r=S.r)),
        line(poly([(11.5, 10.5), (8, 12.5)], r=S.r)),
        line(poly([(11.5, 10.5), (15, 12)], r=S.r)),
        line(poly([(11, 15), (7.5, 21.5)], r=S.r)),
        line(poly([(11, 15), (16, 18), (16.5, 21.5)], r=S.r)),
        line(seg(2.5, 15, 20, 7)),
        solid(poly([(19, 5.5), (22.5, 6.5), (20.5, 9)], closed=True)),
    ]


@icon("discus-throw", CAT, "Thrower twisting with one arm swung out holding a flat disc",
      tags=["discus", "throw", "thrower", "disc", "track and field", "field event"], aliases=[])
def _(S):
    return [
        dot(9, 5.5, 2.25),
        line(poly([(9.5, 8.5), (10, 14.5)], r=S.r)),
        line(poly([(9.7, 9.5), (16, 10.5)], r=S.r)),
        line(poly([(9.7, 9.5), (4.5, 12)], r=S.r)),
        line(poly([(10, 14.5), (6, 21.5)], r=S.r)),
        line(poly([(10, 14.5), (15, 17.5), (15.5, 21.5)], r=S.r)),
        solid(ellipse(19.5, 10.5, 2.8, 1.6)),
    ]


@icon("shot-put", CAT, "Thrower crouched with a heavy ball pressed against the neck",
      tags=["shot put", "shot", "throw", "heavy ball", "track and field", "field event"], aliases=[])
def _(S):
    return [
        dot(7, 6, 2.25),
        line(poly([(8, 9), (9, 15)], r=S.r)),
        line(poly([(8.2, 10), (13, 12.5), (14.5, 9)], r=S.r)),
        dot(14, 6, 2.5),
        line(poly([(9, 15), (13.5, 17.5), (12, 21.5)], r=S.r)),
        line(poly([(9, 15), (5, 17.5), (4.5, 21.5)], r=S.r)),
    ]


@icon("hammer-throw", CAT, "Thrower spinning with a heavy ball on a wire swinging around",
      tags=["hammer throw", "hammer", "spin", "throw", "track and field", "field event"], aliases=[])
def _(S):
    return [
        dot(11, 6.5, 2.25),
        line(poly([(11, 9.5), (11, 15.5)], r=S.r)),
        line(poly([(11, 10.5), (14.5, 12.5)], r=S.r)),
        line(seg(14.5, 12.5, 18.5, 8)),
        dot(20, 5.5, 2.2),
        line(poly([(11, 15.5), (8, 21.5)], r=S.r)),
        line(poly([(11, 15.5), (14.5, 21.5)], r=S.r)),
        line(arc(11, 13, 9, 150, 250)),
    ]


@icon("steeplechase", CAT, "Runner clearing a barrier above a water pit",
      tags=["steeplechase", "water jump", "barrier", "hurdle", "track and field", "obstacle"], aliases=[])
def _(S):
    return [
        dot(7, 4, 2.25),
        line(poly([(7.5, 7), (6.5, 12)], r=S.r)),
        line(poly([(7.5, 8), (11, 5.5)], r=S.r)),
        line(poly([(7.5, 8), (3.5, 8.5)], r=S.r)),
        line(poly([(6.5, 12), (11.5, 10.5), (15, 10)], r=S.r)),
        line(poly([(6.5, 12), (3, 15), (5.5, 17.5)], r=S.r)),
        shell(rect(11.5, 13, 9.5, 2.5, 0)),
        line("M10 20q2-2.5 4 0t4 0t4 0"),
    ]


@icon("running-track", CAT, "Top view of an oval running track with parallel lanes",
      tags=["running track", "athletics track", "oval", "lanes", "stadium", "400m", "track and field"], aliases=[])
def _(S):
    return [
        shell(rect(2.5, 4.5, 19, 15, L(S, 5, 7.5))),
        shell(rect(7, 9, 10, 6, L(S, 1.5, 3))),
        detail(seg(12, 4.5, 12, 9)),
    ]


@icon("track-spikes", CAT, "Low running shoe with a stiff sole and small spikes under the toe",
      tags=["spikes", "running shoe", "track shoe", "cleats", "sprint", "athletics footwear"], aliases=[])
def _(S):
    return [
        shell(poly([(2.5, 17), (2.5, 7.5), (7, 7.5), (10, 11), (15, 12.5), (21.5, 15), (21.5, 17)], closed=True, r=S.r)),
        detail(seg(8, 12.5, 10.5, 15)),
        solid(poly([(12.5, 18), (15.5, 18), (14, 21.5)], closed=True)),
        solid(poly([(17.5, 18), (20.5, 18), (19, 21.5)], closed=True)),
        solid(poly([(3.5, 18), (6.5, 18), (5, 21.5)], closed=True)),
    ]


# ============================================================================ gymnastics

@icon("pommel-horse", CAT, "Padded body on legs with two raised handles on top",
      tags=["pommel horse", "gymnastics", "apparatus", "handles", "artistic gymnastics", "gym equipment"], aliases=[])
def _(S):
    return [
        shell(rect(2.5, 10, 19, 5, L(S, 1.5, 2.5))),
        line(poly([(6.5, 10), (6.5, 5), (10.5, 5), (10.5, 10)], r=S.r)),
        line(poly([(13.5, 10), (13.5, 5), (17.5, 5), (17.5, 10)], r=S.r)),
        line(seg(7, 15, 6, 21.5)), line(seg(17, 15, 18, 21.5)),
    ]


@icon("balance-beam", CAT, "Long narrow beam on two sturdy legs, side view",
      tags=["balance beam", "gymnastics", "beam", "apparatus", "artistic gymnastics", "gym equipment"], aliases=[])
def _(S):
    return [
        shell(rect(2, 7, 20, 4.5, L(S, 1.5, 2.2))),
        line(poly([(6, 11.5), (6, 21.5)], r=S.r)),
        line(poly([(18, 11.5), (18, 21.5)], r=S.r)),
        line(seg(3.5, 21.5, 8.5, 21.5)), line(seg(15.5, 21.5, 20.5, 21.5)),
    ]


@icon("uneven-bars", CAT, "Two horizontal bars at different heights on posts",
      tags=["uneven bars", "asymmetric bars", "gymnastics", "bars", "apparatus", "artistic gymnastics"], aliases=["asymmetric-bars"])
def _(S):
    return [
        line(seg(2.5, 5, 10.5, 5)), line(seg(6.5, 5, 6.5, 21.5)),
        line(seg(13.5, 11, 21.5, 11)), line(seg(17.5, 11, 17.5, 21.5)),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("vaulting-table", CAT, "Padded vault top on a pedestal with a springboard in front",
      tags=["vault", "vaulting table", "gymnastics", "springboard", "apparatus", "gym equipment"], aliases=[])
def _(S):
    return [
        shell(rect(10.5, 4.5, 11, 5, L(S, 1.5, 2.5))),
        line(poly([(13, 9.5), (12, 21.5)], r=S.r)),
        line(poly([(19, 9.5), (20, 21.5)], r=S.r)),
        shell(poly([(2.5, 21.5), (2.5, 17.5), (8, 16), (8, 21.5)], closed=True, r=S.r)),
    ]


@icon("rhythmic-ribbon", CAT, "Gymnast on tiptoe twirling a long ribbon on a stick",
      tags=["rhythmic gymnastics", "ribbon", "twirl", "dance", "gymnast", "wand"], aliases=[])
def _(S):
    return [
        dot(8, 6, 2.25),
        line(poly([(8, 9), (8, 15)], r=S.r)),
        line(poly([(8, 10), (11.5, 7)], r=S.r)),
        line(seg(11.5, 7, 14.5, 4.5)),
        line("M14.5 4.5C16 1.5 18.5 1.5 19 5S21.5 10 22 6"),
        line(seg(8, 15, 8, 21.5)),
        line(poly([(8, 15), (12.5, 17), (11, 20.5)], r=S.r)),
        line(poly([(8, 10), (4, 12.5)], r=S.r)),
    ]


@icon("horizontal-bar", CAT, "Gymnast hanging from a high single bar between two posts",
      tags=["horizontal bar", "high bar", "gymnastics", "swing", "apparatus", "artistic gymnastics"], aliases=["high-bar"])
def _(S):
    return [
        line(seg(2.5, 3.5, 21.5, 3.5)),
        line(seg(2.5, 3.5, 2.5, 21.5)), line(seg(21.5, 3.5, 21.5, 21.5)),
        line(poly([(9, 3.5), (12, 8), (15, 3.5)], r=S.r)),
        dot(12, 11, 2),
        line(poly([(12, 13), (12, 17)], r=S.r)),
        line(poly([(12, 17), (10.5, 21.5)], r=S.r)),
        line(poly([(12, 17), (13.5, 21.5)], r=S.r)),
    ]


@icon("springboard", CAT, "Wedge-shaped sprung board with a slanted top",
      tags=["springboard", "board", "gymnastics", "vault", "diving board", "launch"], aliases=[])
def _(S):
    return [
        shell(poly([(2.5, 20.5), (2.5, 17), (21.5, 11.5), (21.5, 20.5)], closed=True, r=S.r)),
        detail(poly([(8, 20.5), (10.5, 17), (13, 20.5)], r=0)),
    ]


@icon("gym-mat", CAT, "Thick folding mat with three panels, seen from the front corner",
      tags=["gym mat", "exercise mat", "tumbling mat", "folding mat", "gymnastics", "floor mat"], aliases=[])
def _(S):
    return [
        shell(poly([(2.5, 12), (7, 6.5), (21.5, 6.5), (21.5, 14.5), (18, 20), (2.5, 20)], closed=True, r=S.r)),
        detail(seg(2.5, 12, 18, 12)), detail(seg(18, 12, 18, 20)), detail(seg(18, 12, 21.5, 6.5)),
        detail(seg(8.2, 12, 8.2, 20)), detail(seg(13.2, 12, 13.2, 20)),
    ]


@icon("human-pyramid", CAT, "Six figures stacked in a triangle with three at the base, two in the middle, one on top",
      tags=["human pyramid", "cheerleading", "stack", "acrobatics", "teamwork", "formation"], aliases=[])
def _(S):
    parts = []
    rows = [(3.5, [12]), (10, [8.5, 15.5]), (16.5, [5, 12, 19])]
    for y, xs in rows:
        for x in xs:
            parts.append(dot(x, y, 1.5))
            parts.append(line(seg(x - 2.5, y + 3.8, x + 2.5, y + 3.8)))
    return parts


# ============================================================================ combat sports

@icon("fencing", CAT, "Two fencers lunging at each other with thin swords crossing in the middle",
      tags=["fencing", "fencer", "duel", "sword fight", "epee", "foil", "sabre"], aliases=[])
def _(S):
    def one(m):
        def X(x):
            return x if m == 1 else 24 - x
        return [
            dot(X(4.5), 6.5, 2),
            line(poly([(X(5), 9), (X(6), 14)], r=S.r)),
            line(poly([(X(5.5), 10.5), (X(8), 10.5), (X(16), 9)], r=0)),
            line(poly([(X(6), 14), (X(9.5), 17.5), (X(9.5), 21.5)], r=S.r)),
            line(poly([(X(6), 14), (X(2.5), 21.5)], r=S.r)),
        ]
    return one(1) + one(-1)


@icon("fencing-mask", CAT, "Rounded mesh face mask with a bib covering the neck",
      tags=["fencing mask", "fencer", "face guard", "mask", "mesh", "protective gear", "helmet"], aliases=[])
def _(S):
    return [
        shell("M5.5 15V9.5a6.5 6.5 0 0 1 13 0V15Z"),
        detail(seg(9.5, 5, 9.5, 15)), detail(seg(14.5, 5, 14.5, 15)),
        shell(poly([(5.5, 17), (18.5, 17), (20.5, 21.5), (3.5, 21.5)], closed=True, r=S.r)),
    ]


@icon("fencing-foil", CAT, "Thin flexible sword with a round bell guard over the grip",
      tags=["foil", "fencing sword", "blade", "epee", "weapon", "fencing", "guard"], aliases=[])
def _(S):
    return [
        line(seg(12, 2, 12, 11)),
        shell(poly([(6.5, 17), (8, 13), (12, 11.5), (16, 13), (17.5, 17)], closed=True, r=S.r)),
        line(seg(12, 17, 12, 20.5)),
        Part("dot", rect(10.5, 20, 3, 2, 0)) if S.name == "line" else dot(12, 21, 1.5),
    ]


@icon("judo", CAT, "Judoka throwing an opponent over the hip, both in loose jackets",
      tags=["judo", "throw", "martial arts", "hip throw", "grappling", "dojo", "ippon"], aliases=[])
def _(S):
    return [
        dot(8, 8, 2),
        line(poly([(9, 10.5), (11, 15)], r=S.r)),
        line(poly([(11, 15), (8, 21.5)], r=S.r)),
        line(poly([(11, 15), (15, 21.5)], r=S.r)),
        line(poly([(9.5, 11), (14, 10)], r=S.r)),
        dot(20, 14, 2),
        line(poly([(17.5, 12.5), (13, 8.5), (7, 3.5)], r=S.r)),
        line(poly([(7, 3.5), (3.5, 5)], r=S.r)),
        line(poly([(14, 10), (16.5, 14)], r=S.r)),
    ]


@icon("wrestling", CAT, "Two wrestlers leaning into each other with arms locked around one another",
      tags=["wrestling", "grapple", "hold", "wrestlers", "combat sport", "mat", "tie-up"], aliases=[])
def _(S):
    def one(m):
        def X(x):
            return x if m == 1 else 24 - x
        return [
            dot(X(7.5), 6, 2),
            line(poly([(X(8.5), 9), (X(6), 15)], r=S.r)),
            line(poly([(X(6), 15), (X(3.5), 21.5)], r=S.r)),
            line(poly([(X(6), 15), (X(9.5), 21.5)], r=S.r)),
            line(poly([(X(8.2), 10), (X(12.5), 12.5)], r=S.r)),
        ]
    return one(1) + one(-1)


@icon("sumo", CAT, "Heavy wrestler in a crouch with one leg raised and a belt around the waist",
      tags=["sumo", "rikishi", "wrestler", "stomp", "shiko", "japanese wrestling", "belt"], aliases=["rikishi"])
def _(S):
    return [
        dot(12, 4, 2),
        shell(ellipse(12, 11.5, 5.5, 4.5)),
        detail(seg(6.5, 14, 17.5, 14)),
        line(poly([(7, 9.5), (3.5, 12), (4.5, 14.5)], r=S.r)),
        line(poly([(17, 9), (20.5, 9.5)], r=S.r)),
        line(poly([(14.5, 16), (19.5, 15), (21.5, 18.5)], r=S.r)),
        line(poly([(9.5, 16), (8.5, 21.5)], r=S.r)),
    ]


@icon("sumo-ring", CAT, "Top view of a circular ring with two short start lines inside",
      tags=["sumo ring", "dohyo", "ring", "circle", "arena", "wrestling ring", "start lines"], aliases=["dohyo"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(seg(9.5, 8.5, 9.5, 15.5)), detail(seg(14.5, 8.5, 14.5, 15.5)),
        sq(1.5, 10.5, 3, 3) if S.name == "line" else dot(3, 12, 1.2),
        sq(19.5, 10.5, 3, 3) if S.name == "line" else dot(21, 12, 1.2),
    ]


@icon("kendo", CAT, "Fencer in armor and a grilled helmet raising a bamboo sword overhead",
      tags=["kendo", "shinai", "bamboo sword", "men", "armor", "japanese fencing", "martial arts"], aliases=["shinai"])
def _(S):
    return [
        shell(circle(11, 9.5, 4)),
        detail(seg(7.5, 9.5, 14.5, 9.5)),
        shell(poly([(7, 15), (15, 15), (17, 21.5), (5, 21.5)], closed=True, r=S.r)),
        line(poly([(15.5, 16), (18, 12)], r=S.r)),
        line(seg(18, 12, 21, 2.5)),
    ]


@icon("kyudo", CAT, "Archer in wide trousers drawing a very tall asymmetric bow",
      tags=["kyudo", "japanese archery", "yumi", "bow", "archer", "martial arts", "arrow"], aliases=["yumi"])
def _(S):
    return [
        dot(7, 5.5, 2.25),
        line(poly([(7.5, 8.5), (7.5, 15)], r=S.r)),
        line(seg(7.5, 11, 20, 11)),
        line("M17 2Q23.5 11.5 17 21.5"),
        line(poly([(17, 2), (8.5, 10.5), (17, 21.5)], r=0)),
        line(poly([(7.5, 15), (4.5, 21.5)], r=S.r)),
        line(poly([(7.5, 15), (10.5, 21.5)], r=S.r)),
    ]


@icon("muay-thai", CAT, "Fighter with a headband driving a knee strike upward",
      tags=["muay thai", "thai boxing", "knee strike", "kickboxing", "fighter", "martial arts", "headband"], aliases=[])
def _(S):
    return [
        dot(9, 5.5, 2.25),
        line(poly([(6.8, 5.2), (3.5, 4), (3, 6.5)], r=0)),
        line(poly([(9.5, 8.5), (9.5, 14.5)], r=S.r)),
        line(poly([(9.5, 9.5), (14.5, 9), (14.5, 5)], r=S.r)),
        line(poly([(9.5, 9.5), (6, 12.5)], r=S.r)),
        line(poly([(9.5, 14.5), (16, 12.5), (15.5, 17.5)], r=S.r)),
        line(poly([(9.5, 14.5), (7.5, 21.5)], r=S.r)),
    ]


@icon("kung-fu", CAT, "Fighter in a low wide horse stance with one palm pushed forward",
      tags=["kung fu", "horse stance", "palm strike", "wushu", "martial arts", "chinese martial arts", "stance"], aliases=["wushu"])
def _(S):
    return [
        dot(11, 5, 2.25),
        line(poly([(11, 8), (11, 14)], r=S.r)),
        line(poly([(11, 9.5), (20, 9.5)], r=S.r)),
        line(seg(20.5, 6.5, 20.5, 12.5)),
        line(poly([(11, 9.5), (7.5, 12), (9, 14)], r=S.r)),
        line(poly([(11, 14), (5.5, 16.5), (5.5, 21.5)], r=S.r)),
        line(poly([(11, 14), (16.5, 16.5), (16.5, 21.5)], r=S.r)),
    ]


@icon("boxer", CAT, "Boxer in a guard stance with gloves raised in front of the face",
      tags=["boxer", "boxing", "guard", "gloves", "fighter", "pugilist", "stance"], aliases=[])
def _(S):
    return [
        dot(9, 5.5, 2.25),
        line(poly([(9.5, 8.5), (9, 15)], r=S.r)),
        line(poly([(9.5, 10), (13.5, 12), (14.5, 8)], r=S.r)),
        dot(15.5, 6.2, 2.6),
        line(poly([(9.5, 10), (12.5, 14), (17, 12)], r=S.r)),
        dot(19, 11.2, 2.4),
        line(poly([(9, 15), (13, 17.5), (12, 21.5)], r=S.r)),
        line(poly([(9, 15), (5, 17.5), (4.5, 21.5)], r=S.r)),
    ]


@icon("capoeira", CAT, "Dancer in a low cartwheel with the legs swinging overhead",
      tags=["capoeira", "cartwheel", "brazilian martial art", "acrobatics", "dance fight", "handstand", "roda"], aliases=[])
def _(S):
    return [
        line(poly([(6, 21.5), (10.5, 15.5)], r=S.r)),
        line(poly([(16, 21.5), (11.5, 15.5)], r=S.r)),
        dot(11, 12.5, 2),
        line(poly([(11, 10.5), (11.5, 8)], r=S.r)),
        line(poly([(11.5, 8), (6, 2.5)], r=S.r)),
        line(poly([(11.5, 8), (18, 3.5)], r=S.r)),
    ]


@icon("mma-cage", CAT, "Top view of an eight-sided fenced ring with the fence line inside",
      tags=["mma", "cage", "octagon", "mixed martial arts", "fight arena", "ring"], aliases=["octagon-ring"])
def _(S):
    return [
        shell(poly(regular(12, 12, 10, 8, -67.5), closed=True, r=S.r)),
        detail(poly(regular(12, 12, 5.8, 8, -67.5), closed=True, r=S.r)),
    ]


@icon("boxing-ring", CAT, "Square ring platform with corner posts and three rows of ropes",
      tags=["boxing ring", "ring", "ropes", "corner posts", "arena", "fight night", "canvas"], aliases=[])
def _(S):
    return [
        shell(poly([(2.5, 18), (12, 13.5), (21.5, 18), (12, 22)], closed=True, r=S.r)),
        line(seg(3.5, 5, 3.5, 18)), line(seg(20.5, 5, 20.5, 18)), line(seg(12, 2.5, 12, 13.5)),
        line(poly([(3.5, 7.5), (12, 3.5), (20.5, 7.5)], r=0)),
        line(poly([(3.5, 12), (12, 8), (20.5, 12)], r=0)),
    ]


@icon("boxing-headgear", CAT, "Padded headguard with an open face and cheek protectors",
      tags=["headgear", "head guard", "boxing", "sparring", "protective gear", "helmet", "padded"], aliases=[])
def _(S):
    return [
        shell(poly([(5, 12), (5.5, 7), (8.5, 3.5), (15.5, 3.5), (18.5, 7), (19, 12), (17, 19), (14, 21), (10, 21), (7, 19)], closed=True, r=L(S, 0, 3))),
        detail(ellipse(12, 12.5, 3.2, 5.2)),
    ]


@icon("boxing-bell", CAT, "Round dome bell on a mounting plate with a striker",
      tags=["boxing bell", "round bell", "ring the bell", "start of round", "gong", "timer", "dome bell"], aliases=[])
def _(S):
    return [
        shell("M4.5 17a7.5 7.5 0 0 1 15 0Z"),
        shell(rect(3, 18.5, 18, 3, L(S, 0, 1.2))),
        Part("dot", rect(10.5, 2.5, 3, 3, 0)) if S.name == "line" else dot(12, 4, 1.7),
    ]


@icon("martial-arts-belt", CAT, "Cloth belt tied in a knot with two ends hanging down",
      tags=["belt", "black belt", "obi", "karate belt", "rank", "dojo", "martial arts"], aliases=["obi"])
def _(S):
    return [
        line(seg(2, 8, 9.5, 8)), line(seg(14.5, 8, 22, 8)),
        shell(rect(9.5, 5, 5, 6, L(S, 0, 1.5))),
        line(poly([(10.8, 11), (8.5, 21)], r=S.r)),
        line(poly([(13.2, 11), (15.5, 21)], r=S.r)),
    ]


@icon("martial-arts-uniform", CAT, "Wrap-over jacket with wide sleeves and a tied belt",
      tags=["gi", "karate gi", "dogi", "uniform", "judo gi", "dojo", "martial arts jacket"], aliases=["gi"])
def _(S):
    return [
        shell(poly([(9, 3.5), (2.5, 7.5), (2.5, 15.5), (6.5, 15.5), (6.5, 21.5), (17.5, 21.5), (17.5, 15.5), (21.5, 15.5), (21.5, 7.5), (15, 3.5)], closed=True, r=S.r)),
        detail(poly([(9, 3.5), (13, 12.5)], r=0)),
        detail(seg(6.5, 17.5, 17.5, 17.5)),
    ]


@icon("nunchaku", CAT, "Two short sticks joined end to end by a short chain",
      tags=["nunchaku", "nunchucks", "chain weapon", "martial arts", "kung fu", "okinawan weapon", "sticks"], aliases=["nunchucks"])
def _(S):
    return [
        shell(poly(rrect(6.2, 15.2, 3.4, 13, 13), closed=True, r=L(S, 0, 1.2))),
        shell(poly(rrect(17.8, 15.2, 3.4, 13, -13), closed=True, r=L(S, 0, 1.2))),
        line("M7.5 8.5C8.5 3 15.5 3 16.5 8.5"),
    ]


@icon("bo-staff", CAT, "Long straight wooden staff held diagonally in two hands",
      tags=["bo staff", "staff", "quarterstaff", "martial arts weapon", "kobudo", "pole", "stick"], aliases=["quarterstaff"])
def _(S):
    return [
        line(seg(3, 21, 21, 3)),
        dot(8.2, 15.8, 2.5), dot(15.8, 8.2, 2.5),
    ]


@icon("board-breaking", CAT, "Hand chopping down through a wooden board that is splitting in two",
      tags=["board breaking", "karate chop", "break", "taekwondo", "power", "martial arts", "split"], aliases=[])
def _(S):
    return [
        shell(rect(9.5, 2.5, 5, 9, L(S, 0, 2.2))),
        shell(poly([(2.5, 15.5), (10.5, 15.5), (9.5, 20.5), (2.5, 20.5)], closed=True, r=S.r)),
        shell(poly([(13.5, 15.5), (21.5, 15.5), (21.5, 20.5), (14.5, 20.5)], closed=True, r=S.r)),
        line(seg(7, 12, 5.5, 9.5)), line(seg(17, 12, 18.5, 9.5)),
    ]


# ============================================================================ sailing

@icon("sailing-dinghy", CAT, "Small dinghy with a triangular sail and a sailor leaning out over the side",
      tags=["dinghy", "sailing", "hiking out", "small boat", "sailor", "regatta", "sail"], aliases=[])
def _(S):
    return [
        line(seg(11, 2.5, 11, 15)),
        shell(poly([(11, 3.5), (11, 12.5), (4, 12.5)], closed=True, r=S.r)),
        shell(poly([(2.5, 15.5), (18, 15.5), (15.5, 20.5), (5.5, 20.5)], closed=True, r=S.r)),
        dot(20, 9.5, 2),
        line(poly([(15, 14.5), (19, 11.5)], r=S.r)),
    ]


@icon("sailing-regatta", CAT, "Three small sailboats racing past a triangular marker buoy",
      tags=["regatta", "sailing race", "yacht race", "boats", "buoy", "sailboats", "fleet"], aliases=[])
def _(S):
    def boat(x, y):
        return [
            solid(poly([(x, y - 6), (x, y), (x + 5, y)], closed=True)),
            line(seg(x - 1, y + 2.5, x + 6.5, y + 2.5)),
        ]
    return boat(3.5, 8) + boat(14.5, 8) + boat(7.5, 19) + [
        solid(poly([(19.5, 14.5), (22, 21), (17, 21)], closed=True)),
    ]