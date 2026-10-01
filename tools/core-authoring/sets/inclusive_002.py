"""TypeIcon Core: inclusive (batch 002): accessible places, adaptive play and assistive devices."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import P, path_to_d, rotation, transform_path, fmt

CAT = "inclusive"


def rot(d, deg, cx, cy):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def union(*ds):
    from geometry import U
    return path_to_d(U(*[P(d) for d in ds]))


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def head(x, y, deg, n=3.2, spread=145):
    """Open arrowhead whose tip is (x, y) and which travels toward deg (0 = right, 90 = down)."""
    a = (x + n * math.cos(math.radians(deg + spread)), y + n * math.sin(math.radians(deg + spread)))
    b = (x + n * math.cos(math.radians(deg - spread)), y + n * math.sin(math.radians(deg - spread)))
    return poly([a, (x, y), b])


def wave(x, y, n, w=3.0, h=1.5):
    d = f"M{fmt(x)} {fmt(y)}"
    for i in range(n):
        d += f"q{fmt(w / 2)} {fmt(-h if i % 2 == 0 else h)} {fmt(w)} 0" if i == 0 else f"t{fmt(w)} 0"
    return d


# ============================================================================ places and transport

@icon("swivel-car-seat", CAT, "A car seat with a curved arrow under it showing it turning out of the car",
      tags=["swivel seat", "car transfer", "turning seat", "mobility", "vehicle", "accessible car", "rotate seat"])
def _(S):
    return [
        shell(poly([(7, 3), (11, 3), (11, 9), (17, 9), (17, 13), (7, 13)], closed=True, r=S.r)),
        line(arc(12, 12, 8, 25, 155)),
        line(head(*pt(12, 12, 8, 155), 245)),
        line(head(*pt(12, 12, 8, 25), -65)),
    ]


def pt(cx, cy, r, deg):
    return (cx + r * math.cos(math.radians(deg)), cy + r * math.sin(math.radians(deg)))


@icon("car-transfer-handle", CAT, "A T-shaped grab handle whose hooked tip sits in a car door latch bracket",
      tags=["transfer handle", "car handle", "grab handle", "door latch", "getting out of car", "support", "mobility aid"])
def _(S):
    return [
        shell(rect(4, 3, 16, 5, min(S.R, 2.5))),
        line(poly([(12, 8), (12, 17), (15.5, 17)], r=S.r)),
        line(poly([(8, 13), (8, 21), (19, 21), (19, 13)], r=S.r)),
    ]


@icon("step-free-access", CAT, "A door frame with a level floor running straight through and a small wheelchair user outside",
      tags=["no steps", "level entry", "flat entrance", "wheelchair access", "accessible entrance", "ramp free", "barrier free"])
def _(S):
    return [
        line(poly([(3, 21), (3, 3), (11, 3), (11, 21)], r=S.r)),
        line(seg(2, 21, 22, 21)),
        dot(8, 12.5, 1.1),
        dot(17, 7.5, 1.6),
        line(poly([(17, 10.5), (17, 14), (21, 14)], r=S.r)),
        shell(circle(17, 17.5, 3.5)),
    ]


@icon("accessible-pedestrian-button", CAT, "A pole-mounted crossing push button box with a large arrow and a speaker grille",
      tags=["crossing button", "pedestrian signal", "push button", "tactile arrow", "audible signal", "street crossing", "walk signal"])
def _(S):
    return [
        shell(rect(5, 2, 14, 16, S.R)),
        detail(poly([(12, 11), (12, 5.5)])),
        detail(poly([(9, 8), (12, 5), (15, 8)], r=S.r)),
        dot(9, 14.5, 1), dot(12, 14.5, 1), dot(15, 14.5, 1),
        line(seg(12, 18, 12, 22)),
    ]


@icon("wayfinding-audio-beacon", CAT, "A small wall box sending out sound waves with a map pin below it",
      tags=["audio beacon", "talking sign", "navigation aid", "blind navigation", "sound guidance", "location marker", "indoor wayfinding"])
def _(S):
    return [
        shell(rect(3, 3, 9, 6, min(S.R, 2))),
        line(arc(12, 6, 4.5, -45, 45)),
        line(arc(12, 6, 7.5, -40, 40)),
        shell("M12 21C9.5 19 8 17.5 8 15.5A4 4 0 0 1 16 15.5C16 17.5 14.5 19 12 21Z"),
        dot(12, 15.5, 1.3),
    ]


@icon("passenger-assistance-point", CAT, "A help panel on a post beside a person reaching out a hand to offer assistance",
      tags=["help point", "assistance", "station help", "call for help", "passenger support", "customer service", "assisted travel"])
def _(S):
    return [
        shell(rect(2, 2, 9, 10, min(S.R, 2.5))),
        detail(poly([(4.5, 9), (8.5, 9)])),
        dot(6.5, 5.5, 1.6),
        line(seg(6.5, 12, 6.5, 22)),
        shell(circle(17.5, 5.5, 2.5)),
        line(poly([(15.5, 22), (17.5, 15), (19.5, 22)], r=S.r)),
        line(seg(17.5, 9.5, 17.5, 15)),
        line(seg(17.5, 11, 13.5, 13.5)),
    ]


@icon("accessible-sink", CAT, "A wall-mounted basin with a lever tap and clear open space underneath for knees",
      tags=["washbasin", "wheelchair sink", "bathroom", "knee clearance", "lever tap", "wall hung basin", "accessible bathroom"])
def _(S):
    return [
        line(seg(21, 3, 21, 21)),
        line(seg(3, 21, 21, 21)),
        shell(poly([(21, 9), (7, 9), (9.5, 15), (21, 15)], closed=True, r=S.r)),
        line(poly([(21, 5), (12, 5), (12, 7)], r=S.r)),
        line(seg(16, 5, 16, 2.5)),
    ]


@icon("accessible-toilet-key", CAT, "A large key with a round bow carrying a small person symbol, for locked accessible toilets",
      tags=["radar key", "disabled toilet key", "restroom key", "toilet access", "locked washroom", "key", "access key"])
def _(S):
    return [
        shell(circle(8, 12, 6.5)),
        dot(8, 9.2, 1.2),
        detail(poly([(5.5, 12), (10.5, 12)])),
        detail(poly([(8, 12), (8, 15)])),
        line(seg(14.5, 12, 21.5, 12)),
        line(seg(18.5, 12, 18.5, 15.5)),
        line(seg(21.5, 12, 21.5, 14.5)),
    ]


@icon("accessible-picnic-table", CAT, "A picnic table with a bench on one side only, leaving an open end where a wheelchair fits",
      tags=["picnic table", "wheelchair table", "outdoor seating", "park", "open end table", "accessible park", "garden table"])
def _(S):
    return [
        line(seg(3, 8, 21, 8)),
        line(seg(7, 8, 5, 21)),
        line(seg(17, 8, 19, 21)),
        line(seg(2, 14.5, 9.5, 14.5)),
        line(seg(14.5, 14.5, 17.5, 14.5)),
        dot(21, 14.5, 1),
    ]


@icon("audio-ballot", CAT, "A voting booth with a ballot slot and headphones plugged into its side",
      tags=["accessible voting", "audio voting", "headphones", "ballot", "voting booth", "blind voter", "election"])
def _(S):
    return [
        shell(poly([(5, 11), (5, 4), (10, 4), (10, 11)], r=S.r)),
        shell(rect(2, 11, 12, 10, min(S.R, 2.5))),
        detail(poly([(5, 14.5), (11, 14.5)])),
        line(poly([(14, 18), (18, 18), (18, 13.5)], r=S.r)),
        line(arc(17.5, 8, 3.5, 180, 360)),
        shell(rect(13, 8, 2, 4.5, 1)),
        shell(rect(20, 8, 2, 4.5, 1)),
    ]


@icon("talking-atm", CAT, "A cash machine with a headphone jack and an earphone plugged in by a cord",
      tags=["accessible atm", "audio banking", "cash machine", "earphone", "blind banking", "speaking machine", "bank"])
def _(S):
    return [
        shell(rect(3, 2, 13, 19, min(S.R, 2.5))),
        detail(rect(6, 5, 7, 5, 0)),
        detail(poly([(6, 14), (13, 14)])),
        dot(9.5, 17.5, 1),
        line(poly([(16, 17), (20, 17), (20, 13)], r=S.r)),
        shell(ellipse(20, 10.5, 1.6, 2.4)),
    ]


@icon("adaptive-swing-seat", CAT, "A playground swing with a high backrest bucket seat and a front safety bar",
      tags=["swing", "playground", "supportive swing", "bucket seat", "adaptive play", "inclusive playground", "harness swing"])
def _(S):
    return [
        line(seg(3, 3, 21, 3)),
        line(seg(8, 3, 8, 6)),
        line(seg(16, 3, 16, 6)),
        shell(poly([(7, 6), (17, 6), (17, 13), (20, 13), (20, 20), (4, 20), (4, 13), (7, 13)], closed=True, r=S.r)),
        detail(poly([(4, 16.5), (20, 16.5)])),
    ]


@icon("sensory-pod-swing", CAT, "A hanging teardrop-shaped cocoon swing with an oval opening",
      tags=["cocoon swing", "hanging pod", "calming swing", "sensory room", "pod chair", "hanging nest", "retreat space"])
def _(S):
    return [
        line(seg(8, 2.5, 16, 2.5)),
        line(seg(12, 2.5, 12, 6)),
        shell("M12 6C16 8 19 11 19 15A7 6.5 0 0 1 5 15C5 11 8 8 12 6Z"),
        detail(ellipse(12, 15, 3, 3.8)),
    ]


@icon("adaptive-tricycle", CAT, "A tricycle with a high back support seat, pedals and a rear push handle",
      tags=["trike", "therapy tricycle", "adaptive bike", "push handle", "disability bike", "supportive seat", "three wheel bike"])
def _(S):
    return [
        shell(circle(5.5, 17, 3.5)),
        shell(circle(18, 17, 3.5)),
        line(poly([(5.5, 17), (8, 9), (6, 8)], r=S.r)),
        line(poly([(8, 9), (12, 16), (18, 17)], r=S.r)),
        line(seg(11, 12, 16, 12)),
        line(poly([(16, 12), (16, 5), (20, 3)], r=S.r)),
    ]


@icon("ski-outrigger", CAT, "A forearm crutch with a short ski attached at its base",
      tags=["adaptive skiing", "crutch ski", "outrigger", "disabled skiing", "winter sport", "mobility", "ski crutch"])
def _(S):
    return [
        line(seg(14, 3, 10, 19)),
        line(arc(15.5, 6.5, 2.7, 270, 450)),
        line(seg(11.8, 11.5, 16, 11.5)),
        line(poly([(3, 21), (19, 21), (22, 18.5)], r=S.r)),
    ]


@icon("beep-ball", CAT, "A ball with a speaker grille giving off sound waves, used in blind baseball",
      tags=["beeping ball", "blind baseball", "audible ball", "sound ball", "adaptive sport", "speaker", "softball"])
def _(S):
    return [
        shell(circle(8, 12, 5.5)),
        detail(poly([(5.5, 10), (10.5, 10)])),
        detail(poly([(5.5, 14), (10.5, 14)])),
        line(arc(8, 12, 9, -35, 35)),
        line(arc(8, 12, 12.5, -30, 30)),
    ]


@icon("swim-tapper", CAT, "A pole with a soft ball on its tip tapping a swimmer's head above the water",
      tags=["tapping stick", "blind swimming", "turn warning", "swim coach", "tapper", "pool safety", "adaptive swimming"])
def _(S):
    return [
        line(seg(3, 3, 9.5, 7.5)),
        shell(circle(11.5, 9, 2.2)),
        shell(circle(17, 14, 3.5)),
        line(wave(2, 20.5, 6, 3.3, 1.6)),
    ]


@icon("showdown-table", CAT, "A long table with raised rims, a centre screen and a goal pocket at each end, seen from above",
      tags=["table game", "blind table tennis", "table sport", "paralympic", "adaptive sport", "goal pocket", "showdown"])
def _(S):
    return [
        shell(rect(2, 5, 20, 14, S.R)),
        detail(poly([(12, 5), (12, 19)])),
        sq(3.5, 10.5, 2.5, 3),
        sq(18, 10.5, 2.5, 3),
        dot(8, 8, 1.1),
    ]


@icon("boccia-ramp", CAT, "A tilted chute on a stand with a ball rolling down it",
      tags=["boccia", "ramp", "ball chute", "adaptive sport", "paralympic", "assistive ramp", "ball sport"])
def _(S):
    return [
        shell(poly([(4.9, 3.5), (17.9, 11.5), (16.1, 14.5), (3.1, 6.5)], closed=True, r=S.r * 0.6)),
        line(seg(8, 8.5, 6, 21)),
        line(seg(14.2, 12.5, 16.5, 21)),
        shell(circle(20, 17, 2.3)),
    ]


@icon("tactile-chess-board", CAT, "A chessboard with dark squares and small pegs in the light squares so it can be felt by touch",
      tags=["chess", "touch board", "blind chess", "tactile game", "raised squares", "pegged pieces", "board game"])
def _(S):
    c = 16 / 3
    parts = [shell(rect(3, 3, 18, 18, min(S.R, 2.5)))]
    for i in range(3):
        for j in range(3):
            x, y = 4 + c * i, 4 + c * j
            if (i + j) % 2 == 0:
                parts.append(sq(x, y, c, c))
            else:
                parts.append(dot(x + c / 2, y + c / 2, 1.1))
    return parts


@icon("adaptive-game-controller", CAT, "A wide flat controller board with two large round buttons and a row of small sockets along the top",
      tags=["accessible gaming", "switch controller", "big buttons", "game pad", "one handed gaming", "assistive gaming", "socket board"])
def _(S):
    return [
        shell(rect(2, 8, 20, 13, S.R)),
        detail(circle(7.5, 15, 3.5)),
        detail(circle(16.5, 15, 3.5)),
        line(seg(6, 4, 6, 8)),
        line(seg(10, 4, 10, 8)),
        line(seg(14, 4, 14, 8)),
        line(seg(18, 4, 18, 8)),
    ]


@icon("switch-adapted-toy", CAT, "A toy car joined by a cord to a large round push button switch",
      tags=["adapted toy", "switch toy", "big button", "assistive switch", "cause and effect", "special needs play", "toy car"])
def _(S):
    return [
        shell(poly([(2, 11), (2, 7.5), (5, 7.5), (6.5, 4), (10.5, 4), (12, 7.5), (14, 7.5), (14, 11)], closed=True, r=S.r)),
        dot(5.5, 11.5, 1.8),
        dot(10.5, 11.5, 1.8),
        line(poly([(14, 9), (17, 9), (17, 13)], r=S.r)),
        shell(circle(17, 18, 4)),
        detail(circle(17, 18, 1.4)),
    ]


@icon("head-pointer", CAT, "A head with a band across the forehead and a long pointer stick aimed at a key",
      tags=["head wand", "headstick", "typing aid", "assistive typing", "pointer", "mobility aid", "hands free input"])
def _(S):
    nose = poly([(15.2, 12.5), (18.2, 15.5), (14.8, 16)], closed=True, r=S.r * 0.5)
    return [
        shell(union(circle(9, 11, 6.5), nose)),
        detail(poly([(3, 8), (15, 8)])),
        line(seg(15, 8, 22, 10.5)),
        line(poly([(5, 17.5), (5, 21), (13, 21), (13, 17.5)], r=S.r)),
    ]


@icon("mouth-stick", CAT, "A slim stick with a mouthpiece at one end and a rubber tip pressing a key at the other",
      tags=["mouthstick", "typing stick", "hands free", "quadriplegic aid", "assistive tool", "stylus", "key press"])
def _(S):
    return [
        shell(rect(2, 3, 5, 4, 1.5)),
        line(seg(6, 6, 16, 15)),
        dot(17, 16, 1.9),
        shell(rect(11, 18, 11, 3.5, 1)),
    ]


@icon("sip-and-puff-switch", CAT, "A bendable gooseneck arm holding a mouth tube above a small switch box on a base",
      tags=["sip puff", "breath switch", "straw switch", "gooseneck", "assistive switch", "breath control", "wheelchair control"])
def _(S):
    return [
        shell(rect(3, 16, 18, 5, min(S.R, 2.4))),
        dot(7, 18.5, 1),
        line("M12 16C12 11 17 12 17 8" if S.name == "line" else "M12 16C12 11.5 17 11.5 17 8"),
        shell(rect(14.5, 2.5, 5, 5.5, min(S.R, 2.4))),
    ]


@icon("keyguard", CAT, "A plate with holes laid over a keyboard so each key can be pressed on its own",
      tags=["keyboard guard", "key plate", "typing aid", "tremor", "motor impairment", "keyboard cover", "accessibility"])
def _(S):
    parts = [shell(rect(3, 4, 18, 16, min(S.R, 3)))]
    for y in (6, 10.5):
        for x in (5.5, 10.5, 15.5):
            parts.append(sq(x, y, 3, 2.5))
    parts.append(sq(5.5, 15, 13, 2.5))
    return parts


@icon("dwell-click", CAT, "A mouse pointer arrow with a ring partly filling around its tip",
      tags=["hover click", "auto click", "eye tracking", "head tracking", "timed click", "progress ring", "hands free"])
def _(S):
    return [
        shell(poly([(9, 9), (9, 20), (11.8, 17.2), (14, 21.5), (16, 20.5), (13.8, 16.3), (17.5, 16)], closed=True, r=S.r * 0.5)),
        line(arc(9, 9, 6, 130, 340)),
    ]


@icon("large-cursor", CAT, "A big mouse pointer arrow next to a small standard one for scale",
      tags=["big pointer", "enlarged cursor", "low vision", "cursor size", "mouse pointer", "visibility", "accessibility setting"])
def _(S):
    return [
        shell(poly([(3, 3), (3, 18), (7, 14), (10, 21), (13, 19.5), (10, 13), (15.5, 12.5)], closed=True, r=S.r * 0.6)),
        solid(poly([(17.5, 3), (17.5, 9.5), (19, 8.2), (20.2, 11), (21.3, 10.5), (20.1, 7.7), (22, 7.5)], closed=True)),
    ]


@icon("accessibility-tree", CAT, "A tree of connected nodes where each node holds a small person mark",
      tags=["a11y tree", "dom tree", "screen reader", "semantic structure", "node hierarchy", "assistive technology", "web accessibility"])
def _(S):
    parts = []
    for cx, cy in ((12, 5), (5, 17.5), (19, 17.5)):
        parts += [shell(circle(cx, cy, 3.5)), dot(cx, cy, 1.2)]
    parts += [line(seg(12, 8.5, 12, 10.5)), line(poly([(5, 14), (5, 10.5), (19, 10.5), (19, 14)], r=S.r))]
    return parts


@icon("emotion-flashcards", CAT, "Two fanned cards, one showing a smiling face and one a sad face",
      tags=["feelings cards", "emotion cards", "autism support", "social skills", "communication cards", "mood", "visual aid"])
def _(S):
    def card(cx, deg, smile):
        face = [dot(cx - 1.6, 9.2, 0.9), dot(cx + 1.6, 9.2, 0.9)]
        mouth = f"M{fmt(cx - 2.2)} 13.7Q{fmt(cx)} {fmt(16.2 if smile else 11.7)} {fmt(cx + 2.2)} 13.7"
        out = [shell(rot(rect(cx - 3.75, 5, 7.5, 13, min(S.R, 2)), deg, cx, 11.5))]
        for p_ in face:
            p_.d = rot(p_.d, deg, cx, 11.5)
        out += face
        out.append(Part("detail", rot(mouth, deg, cx, 11.5)))
        return out
    return card(7, -8, True) + card(17, 8, False)


@icon("relaxed-performance", CAT, "Theatre curtains drawn open with a soft wave line on the stage between them",
      tags=["sensory friendly show", "relaxed theatre", "autism friendly", "quiet show", "calm performance", "inclusive event", "curtain"])
def _(S):
    return [
        line(seg(2, 3, 22, 3)),
        shell("M3 3V20H8C8 14 7 8 10 3Z" if S.name == "line" else "M3 3V20H8C8 14 7 8 10 3Z"),
        shell("M21 3V20H16C16 14 17 8 14 3Z"),
        line(wave(9.5, 13, 3, 2.0, 1.6)),
    ]


@icon("sensory-bag", CAT, "A drawstring bag with headphones and a round fidget toy peeking out of the top",
      tags=["sensory kit", "calm kit", "headphones", "fidget toy", "autism support", "comfort bag", "sensory tools"])
def _(S):
    return [
        line(arc(8, 9, 4.5, 180, 360)),
        shell(circle(17, 6.5, 2.8)),
        shell(poly([(5, 10), (19, 10), (20, 21), (4, 21)], closed=True, r=S.r)),
        detail("M5.5 13Q12 15.5 18.5 13"),
    ]


@icon("zero-entry-pool", CAT, "A pool side view where the floor slopes gently down from the deck into the water with no steps",
      tags=["beach entry", "gradual entry", "pool access", "accessible pool", "ramped pool", "wheelchair pool", "swimming"])
def _(S):
    return [
        shell(poly([(2, 7), (7, 7), (17, 18), (22, 18), (22, 21), (2, 21)], closed=True, r=S.r)),
        line(wave(11, 11.5, 4, 2.75, 1.4)),
    ]


@icon("pivot-transfer-disc", CAT, "A thick round turntable disc with two footprints on top and a curved arrow showing it turn",
      tags=["transfer turntable", "turning disc", "pivot disc", "patient transfer", "stand and turn", "carer aid", "mobility"])
def _(S):
    return [
        shell("M3 12.5V18.5A9 3.5 0 0 0 21 18.5V12.5A9 3.5 0 0 0 3 12.5Z"),
        detail("M3 15.5A9 3.5 0 0 0 21 15.5"),
        Part("dot", rot(ellipse(9.5, 12.5, 1.1, 2.1), 22, 9.5, 12.5)),
        Part("dot", rot(ellipse(14.5, 12.5, 1.1, 2.1), -22, 14.5, 12.5)),
        line(arc(12, 6.5, 5, 205, 335)),
        line(head(*pt(12, 6.5, 5, 335), 65)),
    ]


@icon("pronoun-badge", CAT, "A round name badge with two lines of text and a small speech bubble above it",
      tags=["pronouns", "name tag", "pin badge", "inclusive introduction", "gender identity", "she he they", "lapel pin"])
def _(S):
    return [
        shell(circle(9.5, 15.5, 6.5)),
        detail(poly([(6.5, 14.5), (12.5, 14.5)])),
        detail(poly([(7.5, 18), (11.5, 18)])),
        shell(poly([(14, 2.5), (21.5, 2.5), (21.5, 7.5), (18, 7.5), (15.5, 9.5), (15.5, 7.5), (14, 7.5)], closed=True, r=S.r)),
    ]
