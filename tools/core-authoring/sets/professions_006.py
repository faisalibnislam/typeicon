"""TypeIcon Core: professions and roles (batch professions_006).

Trades, service jobs, accessibility roles and street trades. Most are a head-and-shoulders figure on the left
with one identifying prop on the right; a few are full scenes where the prop is the point.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, U, fmt, path_to_d, polar  # noqa: F401

CAT = "professions"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def mark(d):
    return Part("dot", d)


def bust_d(S, cx, top, hw, bottom=21.0):
    r = min(hw - L(S, 2.0, 1.0), bottom - top)
    x0, x1 = cx - hw, cx + hw
    return (f"M{fmt(x0)} {fmt(bottom)}V{fmt(top + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x0 + r)} {fmt(top)}"
            f"H{fmt(x1 - r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(top + r)}V{fmt(bottom)}")


def person(S, cx=12.0, hy=9.0, hr=3.0, top=15.0, hw=4.5, bottom=21.0):
    return [shell(circle(cx, hy, hr)), shell(bust_d(S, cx, top, hw, bottom))]


def lp(S, cx=6.0, hy=9.0, hw=4.0):
    return person(S, cx, hy, 3.0, hy + 6.0, hw)


def cap_d(cx, y, w, h):
    """Dome (flat cap crown) sitting on y."""
    return f"M{fmt(cx - w)} {fmt(y)}A{fmt(w)} {fmt(h)} 0 0 1 {fmt(cx + w)} {fmt(y)}Z"


# ============================================================================ trades

@icon("glazier", CAT, "Figure carrying a large glass pane using two suction cup handles",
      tags=["glass fitter", "window installer", "glass pane", "suction cup", "glazing", "windows", "tradesperson"])
def _(S):
    return (lp(S, 6.0, 9.0, 4.0)
            + [shell(rect(13, 4, 8, 15, L(S, 0, 1.5))),
               detail(seg(15.5, 12, 18.5, 8)),
               line(seg(10, 17, 13, 14))])


@icon("hvac-technician", CAT, "Figure holding a pressure gauge beside an outdoor air unit with a round fan grille",
      tags=["hvac", "air conditioning", "heating", "cooling", "ac repair", "gauge", "technician", "outdoor unit"])
def _(S):
    return (lp(S, 6.0, 8.5, 4.0)
            + [shell(rect(13, 8, 9, 13, min(S.R, 2.5))),
               detail(circle(17.5, 14.5, 2.4))])


@icon("cctv-operator", CAT, "Figure seated before a wall of four small monitor screens",
      tags=["security guard", "surveillance", "monitoring", "control room", "camera operator", "monitors", "watch"])
def _(S):
    return ([shell(rect(3, 2.5, 18, 8, min(S.R, 2))),
             detail(seg(12, 2.5, 12, 10.5)),
             detail(seg(3, 6.5, 21, 6.5))]
            + person(S, 12, 15.2, 2.3, 18.5, 5.0, 21.5))


@icon("shoe-shiner", CAT, "Figure brushing a shoe resting on a small wooden box stand",
      tags=["bootblack", "shoe shine", "shoe polish", "brush", "street trade", "shoe care", "cobbler"])
def _(S):
    shoe = [(13, 8.5), (16, 8.5), (16, 11.5), (21, 13), (21, 14.5), (13, 14.5)]
    return (lp(S, 6.0, 9.0, 4.0)
            + [shell(poly(shoe, closed=True, r=0)),
               shell(rect(12, 17, 10, 4, L(S, 0, 1.2)))])


@icon("ice-sculptor", CAT, "Figure with a chisel carving a swan shape from a block of ice",
      tags=["ice carving", "swan", "ice block", "chisel", "sculpting", "banquet", "ice art"])
def _(S):
    return (lp(S, 6.0, 9.0, 4.0)
            + [shell(rect(11.5, 17, 10.5, 4, L(S, 0, 1.2))),
               shell(ellipse(16, 14, 3.6, 1.8)),
               line("M19 13.2Q22 10.5 19.5 7.5L17.5 8"),
               line(seg(10, 12, 12.5, 14.5))])


@icon("pool-cleaner", CAT, "Figure holding a long pole with a skimmer net over wavy water",
      tags=["pool boy", "pool service", "skimmer", "swimming pool", "net", "maintenance", "water"])
def _(S):
    return (lp(S, 6.0, 8.0, 4.0)
            + [line(seg(9.5, 12, 16, 14.5)),
               shell(circle(18.5, 15.5, 2.8)),
               line("M12.5 21.5q1.5-1.5 3 0t3 0t3 0")])


@icon("tea-picker", CAT, "Figure with a basket on the back plucking leaves from a low bush",
      tags=["tea harvest", "plantation", "tea leaves", "farmer", "basket", "picking", "tea garden"])
def _(S):
    bush = path_to_d(U(P(circle(17, 18, 2.6)), P(circle(20, 17.3, 2.3)), P(rect(14.5, 18, 7.5, 3))))
    return (person(S, 10.5, 8.5, 3.0, 14.5, 3.0)
            + [shell(rect(2.5, 10.5, 3, 7.5, L(S, 0, 1.2))),
               shell(bush),
               line(seg(13.5, 15, 16.5, 13))])


@icon("furniture-movers", CAT, "Two figures carrying a sofa between them",
      tags=["removals", "moving house", "movers", "sofa", "couch", "relocation", "heavy lifting"])
def _(S):
    parts = []
    for x, d in ((4, 1), (20, -1)):
        parts += [shell(circle(x, 6, 2.1)),
                  line(poly([(x, 9), (x, 14.5)], r=0)),
                  line(poly([(x + d * 1.5, 20.5), (x, 14.5), (x - d * 1.5, 20.5)], r=S.r)),
                  line(seg(x, 11, x + d * 4, 13.5))]
    return parts + [shell(rect(8, 10, 8, 7, min(S.R, 2))), detail(seg(8, 14, 16, 14))]


@icon("balloon-artist", CAT, "Figure twisting long balloons into a small balloon dog",
      tags=["balloon twister", "balloon animal", "balloon dog", "party", "entertainer", "clown", "kids party"])
def _(S):
    return (lp(S, 6.0, 9.0, 4.0)
            + [shell(ellipse(15.5, 16.5, 4.5, 2.4)),
               shell(circle(19.8, 11.8, 2)),
               line(seg(19.6, 13.8, 19, 14.7)),
               line(seg(12.8, 18.8, 12.8, 21)), line(seg(18.2, 18.8, 18.2, 21))])


@icon("hot-air-balloon-pilot", CAT, "Figure in a wicker basket reaching up to a burner with a flame under the balloon",
      tags=["balloonist", "ballooning", "aeronaut", "basket", "burner", "flight", "sightseeing"])
def _(S):
    return [shell(ellipse(12, 6, 5.2, 4)),
            line(seg(7.2, 9, 9, 18)), line(seg(16.8, 9, 15, 18)),
            shell("M12 12.8Q10.8 11.8 12 10.2Q13.2 11.8 12 12.8Z"),
            shell(circle(12, 15.3, 1.4)),
            shell(rect(8, 18, 8, 3.5, L(S, 0, 1.2)))]


@icon("rideshare-driver", CAT, "Figure in a car window with a phone showing a map pin",
      tags=["ride hailing", "taxi driver", "car service", "chauffeur", "gig driver", "app driver", "map pin"])
def _(S):
    car = "M2.5 20V16Q2.5 14.5 4 14.5H7L9 11.5H16L18 14.5H20Q21.5 14.5 21.5 16V20Z"
    return [shell(car),
            shell(circle(7, 20, 1.8)), shell(circle(17, 20, 1.8)),
            mark(circle(12.5, 13.6, 1.3)),
            shell(rect(14, 2, 6, 7, L(S, 0.5, 1.5))),
            mark(circle(17, 5, 1.1))]


@icon("milk-delivery-person", CAT, "Figure in a cap carrying a wire crate of glass milk bottles",
      tags=["milkman", "dairy delivery", "bottles", "crate", "doorstep delivery", "milk round", "cap"])
def _(S):
    def bottle(x):
        return f"M{x} 15V11.5L{x + 1} 10V8.5H{x + 2.5}V10L{x + 3.5} 11.5V15"
    return (person(S, 6, 9.5, 3.0, 15.5, 4.0)
            + [shell(cap_d(6, 7.2, 3.4, 2.2)), line(seg(9.5, 7.2, 11.5, 7.2)),
               line(bottle(13)), line(bottle(17.5)),
               shell(rect(12.5, 15, 9.5, 5.5, L(S, 0, 1.5))),
               detail(seg(17.25, 15, 17.25, 20.5))])


@icon("night-watchman", CAT, "Figure in a cap and long coat holding up a lantern with a crescent moon above",
      tags=["night guard", "lamplighter", "watch", "lantern", "patrol", "historic", "town crier"])
def _(S):
    moon = path_to_d(D(P(circle(18.5, 5.8, 3.3)), P(circle(20.2, 4.6, 2.7))))
    return (person(S, 6, 9.5, 3.0, 15.5, 4.0)
            + [shell(cap_d(6, 7.2, 3.4, 2.2)),
               shell(rect(14.5, 13, 5, 6.5, L(S, 0, 1.2))), line("M15.5 13V11.5Q17 10 18.5 11.5V13"),
               mark(circle(17, 16.3, 1.1)),
               shell(moon),
               line(seg(10, 17.5, 14.5, 16.5))])


@icon("toymaker", CAT, "Figure in an apron holding a wooden toy train with a small hammer",
      tags=["toy maker", "toy workshop", "wooden toys", "craftsman", "train", "hammer", "apron", "santa's workshop"])
def _(S):
    return (lp(S, 6.0, 9.0, 4.0)
            + [detail(seg(6, 15.5, 6, 21)),
               shell(rect(12.5, 2.5, 5, 3.5, 0)), line(seg(15, 6, 15, 11)),
               shell(rect(12.5, 13, 5.5, 4.5, L(S, 0, 1.2))), shell(rect(18, 11, 4, 6.5, L(S, 0, 1.2))),
               shell(circle(14.5, 19.3, 1.5)), shell(circle(20, 19.3, 1.5))])


@icon("bell-ringer", CAT, "Figure pulling a rope with a fluffy grip hanging from a bell above",
      tags=["church bells", "campanologist", "bell tower", "rope", "ringing", "belfry", "chime"])
def _(S):
    bell = "M13.5 8Q13.5 3.5 17 3.5Q20.5 3.5 20.5 8L21.5 9H12.5Z"
    return (lp(S, 6.0, 10.0, 4.0)
            + [shell(bell),
               line(seg(17, 9.5, 17, 13)),
               shell(ellipse(17, 15.5, 1.3, 2.3)),
               line(seg(10, 17, 15.7, 15.5))])


@icon("organist", CAT, "Figure seated at a keyboard beneath a row of tall organ pipes",
      tags=["pipe organ", "church musician", "keyboard", "recital", "organ pipes", "musician", "church"])
def _(S):
    pipes = [shell(rect(x, y, 3, 8 - (y - 2) + 1, 0)) for x, y in [(3, 2), (8, 4), (13, 4), (18, 2)]]
    return (pipes + person(S, 12, 13.5, 2.3, 17.2, 4.0, 18)
            + [shell(rect(3, 18, 18, 3.5, L(S, 0, 1.2))), detail(seg(9, 18, 9, 21.5)), detail(seg(15, 18, 15, 21.5))])


@icon("parent-teaching-bike", CAT, "Adult running behind a child on a small bicycle holding the back of the seat",
      tags=["learning to ride", "bike lesson", "training", "childhood", "parent and child", "cycling", "balance"])
def _(S):
    return [shell(circle(5, 6, 2.2)),
            line(poly([(5, 8.5), (4.5, 14.5)], r=S.r)),
            line(poly([(4.5, 14.5), (2.5, 21)], r=S.r)), line(poly([(4.5, 14.5), (8, 20)], r=S.r)),
            line(poly([(5, 10), (10.5, 12.5)], r=S.r)),
            shell(circle(12.5, 18.5, 2.5)), shell(circle(20, 18.5, 2.5)),
            line(poly([(12.5, 18.5), (15, 13.5), (20, 18.5)], r=S.r)),
            line(seg(10.5, 12.5, 16, 12.5)), line(seg(15, 13.5, 19, 12)),
            shell(circle(17.5, 6, 2)), line(seg(17, 8.5, 15.5, 12.5))]


@icon("person-with-reacher-grabber", CAT, "Figure using a long pole grabber tool to pick up a small object from the floor",
      tags=["reacher", "grabber", "pick up tool", "mobility aid", "assistive tool", "disability", "dressing aid"])
def _(S):
    return (lp(S, 6.0, 8.0, 4.0)
            + [line(seg(10, 12, 18, 18.5)),
               line(poly([(16, 20), (18, 18.5), (20.5, 19.5)], r=S.r)),
               shell(rect(19.5, 20.5, 2.5, 1.5, 0))])


@icon("person-with-communication-board", CAT, "Figure holding a tablet showing a grid of picture symbol squares",
      tags=["aac", "speech aid", "symbols", "nonverbal", "tablet", "communication aid", "accessibility", "speech disability"])
def _(S):
    return (lp(S, 6.0, 9.0, 4.0)
            + [shell(rect(12, 8, 10, 12, L(S, 0.5, 2))),
               detail(seg(17, 8, 17, 20)), detail(seg(12, 14, 22, 14))])


@icon("screen-reader-user", CAT, "Figure in headphones at a laptop with sound waves coming from the screen",
      tags=["blind user", "visually impaired", "headphones", "assistive technology", "accessibility", "laptop", "audio"])
def _(S):
    return (person(S, 6.5, 10, 2.6, 16, 3.8)
            + [line(arc(6.5, 10, 3.9, 180, 360)),
               line(seg(2.6, 10, 2.6, 12)), line(seg(10.4, 10, 10.4, 12)),
               shell(rect(13, 12, 8.5, 6, L(S, 0.5, 1.5))), line(seg(11.5, 20, 23, 20)),
               line(arc(17.25, 12, 3, 215, 325)), line(arc(17.25, 12, 6, 225, 315))])


@icon("person-with-back-brace", CAT, "Figure wearing a wide back support brace wrapped around the torso",
      tags=["back support", "lumbar", "orthopedic", "injury", "posture", "medical brace", "back pain", "recovery"])
def _(S):
    return (person(S, 12, 6.5, 2.7, 10.5, 5.0, 21.5)
            + [shell(rect(7, 14, 10, 5, L(S, 0, 1.2))),
               detail(seg(12, 14, 12, 19))])
