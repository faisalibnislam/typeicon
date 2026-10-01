"""TypeIcon Core: professions (batch 002).

Every profession is a simple head-and-shoulders figure with one or two identifying props. The figure is a
round head over open-bottom shoulders; props (hats, headsets, tools) carry the meaning.
"""
from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "professions"


def bust(S, cx=8.0, top=12.5, hw=5.0, bottom=21.0):
    """Open-bottom shoulders. Line has squarer shoulders than Rounded."""
    r = min(hw - (1.0 if S.name != "line" else 2.0), bottom - top)
    x0, x1 = cx - hw, cx + hw
    return (f"M{fmt(x0)} {fmt(bottom)}V{fmt(top + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x0 + r)} {fmt(top)}"
            f"H{fmt(x1 - r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(top + r)}V{fmt(bottom)}")


def fig(S, cx=8.0, hy=6.5, hr=2.25, top=12.5, hw=5.0, bottom=21.0):
    return [shell(circle(cx, hy, hr)), shell(bust(S, cx, top, hw, bottom))]


def phones(cx, hy, rr=5.0):
    """Headphone band over the head with two ear pads."""
    return [line(arc(cx, hy, rr, 180, 360)), line(seg(cx - rr, hy, cx - rr, hy + 3)), line(seg(cx + rr, hy, cx + rr, hy + 3))]


def rrot(cx, cy, w, h, deg, r=0.0):
    """Closed polygon: a w x h rectangle centred on (cx, cy) turned clockwise by deg."""
    import math
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    pts = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
    return poly([(cx + x * c - y * sn, cy + x * sn + y * c) for x, y in pts], closed=True, r=r)


def rr_(S, cap):
    return min(S.R, cap)


# ============================================================================ tech and media

@icon("data-scientist", CAT, "Person beside a scatter plot with a trend line.",
      tags=["data analyst", "statistics", "analytics", "machine learning", "researcher", "scientist"])
def _(S):
    return fig(S, 7.5) + [line(poly([(14, 4), (14, 20), (21.5, 20)], r=S.r)), dot(17, 16, 1.25), dot(19.5, 12, 1.25), dot(21.5, 7.5, 1.25)]


@icon("robotics-engineer", CAT, "Person beside a small jointed robot arm.",
      tags=["robot", "automation", "engineer", "mechatronics", "robot arm", "technician"])
def _(S):
    return fig(S, 7.5) + [line(seg(14, 20.5, 21.5, 20.5)), line(poly([(17.5, 20.5), (17.5, 13), (21, 8)], r=S.r)),
                          shell(circle(17.5, 13, 1.5)), line(poly([(19, 5.5), (21.5, 7), (22, 10)], r=S.r))]


@icon("drone-pilot", CAT, "Person with a remote controller and a quadcopter hovering above.",
      tags=["drone operator", "uav", "quadcopter", "remote control", "aerial", "flying"])
def _(S):
    return fig(S, 7, hy=9.5, top=15, hw=4.5) + [
        line(seg(14, 3.5, 21, 10.5)), line(seg(21, 3.5, 14, 10.5)), dot(14, 3.5, 1.6), dot(21, 3.5, 1.6),
        dot(14, 10.5, 1.6), dot(21, 10.5, 1.6)] + [
        shell(rect(13.5, 15, 8, 5, rr_(S, 2))), dot(16, 17.5, 1), dot(19, 17.5, 1)]


@icon("gamer", CAT, "Person in a headset holding a game controller.",
      tags=["video games", "esports", "player", "headset", "controller", "gaming"])
def _(S):
    pad = [(6, 14), (18, 14), (21.5, 20), (19.5, 21.5), (16.5, 18.5), (7.5, 18.5), (4.5, 21.5), (2.5, 20)]
    return [shell(circle(12, 8, 2)), line(arc(12, 8, 5, 180, 360)), line(seg(7, 8, 7, 11)), line(seg(17, 8, 17, 11)),
            shell(poly(pad, closed=True, r=max(S.r, 1.0))), dot(7.5, 16.25, 1), dot(16, 16.25, 1), dot(18.5, 16.25, 1)]


@icon("streamer", CAT, "Person in a headset beside a webcam on a stand.",
      tags=["live stream", "content creator", "webcam", "broadcast", "headset", "twitch"])
def _(S):
    return fig(S, 7, hy=8, hr=2, top=14.5, hw=5) + phones(7, 8) + [
        shell(circle(18, 7.5, 3)), dot(18, 7.5, 1), line(seg(18, 10.5, 18, 16)), line(seg(15.5, 16, 20.5, 16))]


@icon("podcaster", CAT, "Person in headphones beside a large studio microphone on a stand.",
      tags=["podcast", "host", "audio", "microphone", "headphones", "recording"])
def _(S):
    return fig(S, 7, hy=8, hr=2, top=14.5, hw=5) + phones(7, 8) + [
        shell(rect(15.75, 3, 4.5, 9, 2.25)), line(seg(18, 12, 18, 18.5)), line(seg(15, 19, 21, 19))]


@icon("video-creator", CAT, "Person beside a ring light on a tripod.",
      tags=["vlogger", "youtuber", "content creator", "ring light", "tripod", "filming"])
def _(S):
    return fig(S, 6.5, hw=4.5) + [shell(circle(17.5, 7.5, 4.5)), solid(rect(16.25, 5.75, 2.5, 3.5, 0.6)), line(seg(17.5, 12, 17.5, 21)),
                                  line(seg(17.5, 16, 14.5, 21)), line(seg(17.5, 16, 20.5, 21))]


@icon("news-anchor", CAT, "Person behind a desk with a screen beside.",
      tags=["newsreader", "broadcast", "tv", "journalist", "presenter", "desk"])
def _(S):
    return [shell(circle(8, 7, 2.25)), shell(bust(S, 8, 12, 4.5, 16)), shell(rect(3, 16, 18, 5, rr_(S, 1.5))),
            shell(rect(14, 3, 8, 6, rr_(S, 2)))]


@icon("weather-presenter", CAT, "Person pointing to a weather map board with a sun and a cloud.",
      tags=["meteorologist", "forecast", "weather report", "tv", "sun", "cloud"])
def _(S):
    return fig(S, 6, hw=4) + [shell(rect(13, 3, 9, 13, rr_(S, 2))), dot(16.5, 7, 1.5),
                              solid("M15.5 13.5a1.6 1.6 0 0 1 0-3.2a2.4 2.4 0 0 1 4.5-.3A1.75 1.75 0 0 1 19.6 13.5Z")]


@icon("radio-host", CAT, "Person in headphones with a microphone and an on air sign.",
      tags=["radio", "dj", "broadcast", "on air", "presenter", "microphone"])
def _(S):
    return fig(S, 7, hy=8, hr=2, top=14.5, hw=5) + phones(7, 8) + [
        shell(rect(14, 3, 8, 5, rr_(S, 2))), dot(18, 5.5, 1), shell(rect(16, 12, 4, 6, 2)), line(seg(18, 18, 18, 21))]


@icon("camera-operator", CAT, "Person with a video camera resting on the shoulder.",
      tags=["cameraman", "film crew", "videographer", "cinematographer", "camcorder", "shooting"])
def _(S):
    return fig(S, 6, hy=8, top=14, hw=4.5) + [shell(rect(11, 6, 6.5, 6.5, rr_(S, 2))),
                                              shell(poly([(17.5, 7.5), (22, 5.5), (22, 13), (17.5, 11)], closed=True, r=S.r))]


@icon("film-director", CAT, "Person calling action through a megaphone.",
      tags=["movie", "filmmaker", "megaphone", "action", "cinema", "set"])
def _(S):
    return fig(S, 6, hy=8, top=14, hw=4.5) + [shell(poly([(11, 7.5), (21, 3.5), (21, 13.5), (11, 9.5)], closed=True, r=S.r)),
                                              line(seg(14.5, 11.5, 14.5, 15))]


@icon("boom-operator", CAT, "Person holding a long pole with a furry microphone overhead.",
      tags=["boom mic", "film crew", "sound", "set", "recordist", "microphone pole"])
def _(S):
    return fig(S, 7, hy=9.5, top=15, hw=4.5) + [line(seg(10, 16.5, 16, 10)), shell(rrot(18, 7, 8, 4.5, -45, r=1.2 if S.name == "line" else 2.2))]


@icon("sound-engineer", CAT, "Person in headphones with a mixing desk of sliders in front.",
      tags=["audio engineer", "mixing", "studio", "producer", "mixer", "recording"])
def _(S):
    return [shell(circle(12, 7, 2)), line(arc(12, 7, 5, 180, 360)), line(seg(7, 7, 7, 10)), line(seg(17, 7, 17, 10)),
            shell(rect(2.5, 14, 19, 7, rr_(S, 3))), detail(seg(7.5, 16, 7.5, 17.5)), detail(seg(12, 17.5, 12, 19)),
            detail(seg(16.5, 16, 16.5, 17.5))]


@icon("editor", CAT, "Person beside a page with a wavy correction mark on the text.",
      tags=["proofreader", "copy editor", "manuscript", "revise", "publishing", "correction"])
def _(S):
    return fig(S, 6.5, hw=4.5) + [shell(rect(13.5, 3, 8.5, 14, rr_(S, 2))), detail(seg(15.5, 7, 20, 7)),
                                  detail("M15.5 11.5q1.25-2 2.5 0t2.5 0"), line(seg(14, 20.5, 21.5, 20.5))]


# ============================================================================ hats

def hat_hard(S, cx, hy, w=4.75):
    """Hard hat: dome with a brim."""
    return [shell(f"M{fmt(cx - 3.25)} {fmt(hy - 1)}A3.25 3.25 0 0 1 {fmt(cx + 3.25)} {fmt(hy - 1)}Z"),
            line(seg(cx - w, hy - 1, cx + w, hy - 1))]


def hat_cap(S, cx, hy, visor=True, top=3.75):
    """Peaked cap: flat-topped crown with a visor."""
    parts = [shell(poly([(cx - 3.25, hy - 1), (cx - 2.75, hy - top), (cx + 2.75, hy - top), (cx + 3.25, hy - 1)], closed=True, r=S.r * 0.7))]
    if visor:
        parts.append(line(seg(cx - 4.5, hy - 1, cx + 4.5, hy - 1)))
    return parts


def hat_top(S, cx, hy):
    """Top hat."""
    return [shell(rect(cx - 2.5, hy - 6.5, 5, 5.5, S.r * 0.5)), line(seg(cx - 4.5, hy - 1, cx + 4.5, hy - 1))]


def hat_bucket(S, cx, hy):
    """Bucket hat: sloped crown with a drooping brim."""
    return [shell(poly([(cx - 2.75, hy - 1.25), (cx - 2.25, hy - 4.5), (cx + 2.25, hy - 4.5), (cx + 2.75, hy - 1.25)], closed=True, r=S.r * 0.7)),
            line(poly([(cx - 5, hy), (cx - 2.5, hy - 1.25), (cx + 2.5, hy - 1.25), (cx + 5, hy)], r=S.r))]


# ============================================================================ writing and travel

@icon("author", CAT, "Person with a quill pen beside an open book.",
      tags=["writer", "novelist", "book", "quill", "literature", "writing"])
def _(S):
    return fig(S, 6.5, hw=4.5) + [
        shell("M21.5 3C16.5 3.5 14 6.5 13 11C15 10.5 16.5 9.5 17.5 8.5C19.5 7 21 5.5 21.5 3Z"),
        line(seg(13, 11, 11.5, 13)),
        shell(poly([(12.5, 15.5), (17, 16.5), (21.5, 15.5), (21.5, 21), (17, 22), (12.5, 21)], closed=True, r=S.r * 0.5))]


@icon("screenwriter", CAT, "Person beside a typewriter with a sheet of paper sticking up.",
      tags=["scriptwriter", "script", "typewriter", "film", "writing", "screenplay"])
def _(S):
    return fig(S, 6, hw=4) + [shell(rect(14, 3, 6.5, 11, rr_(S, 1))), detail(seg(16.25, 6.5, 18.25, 6.5)),
                              shell(rect(11, 13.5, 11, 7, rr_(S, 2.5))), dot(14.75, 17, 1), dot(18.25, 17, 1)]


@icon("cartoonist", CAT, "Person with a pencil beside a comic speech bubble.",
      tags=["comics", "illustrator", "drawing", "speech bubble", "animation", "sketch"])
def _(S):
    return fig(S, 6.5, hw=4.5) + [
        shell(poly([(13, 3.5), (22, 3.5), (22, 10), (17, 10), (14.5, 12.5), (14.5, 10), (13, 10)], closed=True, r=S.r * 0.6)),
        shell(rrot(18, 17.5, 8, 3, -45, r=0.6 if S.name == "line" else 1.2))]


@icon("translator", CAT, "Person between two speech bubbles holding different letters.",
      tags=["interpreter", "languages", "translate", "multilingual", "speech", "linguist"])
def _(S):
    return fig(S, 6, hw=4) + [
        shell(poly([(12, 3), (21, 3), (21, 9.5), (14.5, 9.5), (12, 12), (12, 9.5)], closed=True, r=S.r * 0.6)),
        detail("M14.5 7.5L16.5 4.5L18.5 7.5") if False else dot(16.5, 6.25, 1.2),
        shell(poly([(14, 12.5), (22, 12.5), (22, 18.5), (19.5, 18.5), (19.5, 21), (17, 18.5), (14, 18.5)], closed=True, r=S.r * 0.6)),
        dot(18, 15.5, 1.2)]


@icon("sign-language-interpreter", CAT, "Person beside a raised hand with fingers up.",
      tags=["sign language", "deaf", "hearing impaired", "interpreter", "accessibility", "hand signs"])
def _(S):
    return fig(S, 6, hw=4) + [line(seg(15.5, 4, 15.5, 12)), line(seg(18.5, 3, 18.5, 12)), line(seg(21.5, 4, 21.5, 12)),
                              shell(rect(14.5, 12, 8, 8, rr_(S, 3.5)))]


@icon("librarian", CAT, "Person beside a tall stack of books.",
      tags=["library", "books", "reading", "bookkeeper", "stack of books", "literature"])
def _(S):
    return fig(S, 6.5, hw=4.5) + [shell(rect(13.5, 4, 8, 3, rr_(S, 1.5))), shell(rect(11.5, 10, 10, 3, rr_(S, 1.5))),
                                  shell(rect(14, 16, 8, 3, rr_(S, 1.5)))]


@icon("museum-curator", CAT, "Person beside a framed picture hung on the wall.",
      tags=["museum", "gallery", "exhibition", "art", "frame", "painting"])
def _(S):
    return fig(S, 6, hw=4) + [shell(rect(12.5, 3.5, 9.5, 9, rr_(S, 1.5))), dot(18.75, 7, 1),
                              solid("M14.5 11.5L16.75 8L19 11.5Z")]


@icon("tour-guide", CAT, "Person holding up a small flag with two followers behind.",
      tags=["travel guide", "tourism", "flag", "sightseeing", "group tour", "excursion"])
def _(S):
    return fig(S, 7, hy=9.5, top=15, hw=4.5) + [line(seg(14, 3.5, 14, 14)), shell(poly([(14, 3.5), (20.5, 5.75), (14, 8)], closed=True, r=S.r * 0.5))]


@icon("flight-attendant", CAT, "Person in a small cap beside a narrow drinks trolley.",
      tags=["air hostess", "cabin crew", "steward", "airline", "trolley", "in-flight service"])
def _(S):
    return fig(S, 6.5, hy=9.5, top=15, hw=4.5) + hat_cap(S, 6.5, 9.5, visor=False, top=3.25) + [
        shell(rect(13.5, 6, 8, 13, rr_(S, 1.5))), detail(seg(13.5, 12.5, 21.5, 12.5)),
        dot(15.5, 21, 1), dot(19.5, 21, 1)]


@icon("air-traffic-controller", CAT, "Person in a headset beside a round radar screen with a sweep line.",
      tags=["atc", "control tower", "radar", "airport", "aviation", "headset"])
def _(S):
    return fig(S, 6, hy=8, hr=2, top=14.5, hw=4.5) + phones(6, 8, 4.5) + [
        shell(circle(17.5, 11, 5)), detail(seg(17.5, 11, 20.5, 8)), dot(15.5, 14, 0.9)]


@icon("ship-captain", CAT, "Person in a captain's cap beside a ship's wheel.",
      tags=["skipper", "sea captain", "mariner", "ship wheel", "helm", "nautical"])
def _(S):
    spokes = [dot(*polar(17.5, 15, 5.6, a), 1) for a in range(0, 360, 45)]
    return fig(S, 6.5, hy=9.5, top=15, hw=4.5) + hat_cap(S, 6.5, 9.5) + [shell(circle(17.5, 15, 3)), dot(17.5, 15, 0.8)] + spokes


@icon("sailor", CAT, "Person in a round sailor cap with a V-neck collar.",
      tags=["seaman", "navy", "sea", "deckhand", "mariner", "crew"])
def _(S):
    return fig(S, 12, hy=9.5, hr=2.5, top=15, hw=7) + hat_cap(S, 12, 9.5, visor=False, top=3.5) + [detail(poly([(8.5, 15.5), (12, 19.5), (15.5, 15.5)], r=S.r * 0.5))]


@icon("navy-officer", CAT, "Person in a peaked cap with an anchor badge and shoulder boards.",
      tags=["naval officer", "admiral", "uniform", "military", "peaked cap", "anchor"])
def _(S):
    return fig(S, 12, hy=9.5, hr=2.5, top=15, hw=7) + hat_cap(S, 12, 9.5) + [solid(rect(4.5, 16.5, 4, 2)), solid(rect(15.5, 16.5, 4, 2))]


@icon("fisherman", CAT, "Person in a bucket hat holding a fishing rod with the line hanging down.",
      tags=["angler", "fishing", "fish", "rod", "hobby", "bucket hat"])
def _(S):
    return fig(S, 6.5, hy=9.5, top=15, hw=4.5) + hat_bucket(S, 6.5, 9.5) + [
        line(seg(11.5, 16, 20, 4)), line("M20 4V15"), line("M20 15a1.5 1.5 0 0 1-3 0")]


def hat_paper(S, cx, hy):
    """Folded paper hat, as worn by painters."""
    return [shell(poly([(cx - 2.75, hy - 1.25), (cx - 2, hy - 4.75), (cx + 2, hy - 4.75), (cx + 2.75, hy - 1.25)], closed=True, r=S.r * 0.5))]


# ============================================================================ trades

@icon("lumberjack", CAT, "Person in a plaid shirt holding an axe.",
      tags=["logger", "woodcutter", "axe", "forestry", "timber", "plaid shirt"])
def _(S):
    import math
    a = math.radians(25)

    def tr(pts):
        return [(14.5 + x * math.cos(a) - y * math.sin(a), 11.5 + x * math.sin(a) + y * math.cos(a)) for x, y in pts]
    h0, h1 = tr([(0, -3), (0, 7)])
    head = poly(tr([(-1.5, -7), (1, -7), (4.5, -8.5), (5, -1.5), (1, -3), (-1.5, -3)]), closed=True, r=S.r * 0.4)
    return fig(S, 6.5, top=13.5, hw=4.5) + [line(seg(*h0, *h1)), shell(head)]


@icon("miner", CAT, "Person in a helmet with a headlamp holding a pickaxe.",
      tags=["mining", "pickaxe", "quarry", "helmet", "headlamp", "underground"])
def _(S):
    return fig(S, 6.5, hy=9.5, top=15, hw=4.5) + hat_hard(S, 6.5, 9.5) + [
        dot(6.5, 6.9, 0.7), line(seg(17.5, 7, 17.5, 21)), line("M12.5 9.5C13.5 5 21.5 5 22.5 9.5")]


@icon("oil-rig-worker", CAT, "Person in a hard hat beside an oil derrick tower.",
      tags=["oil and gas", "drilling", "derrick", "rig", "roughneck", "petroleum"])
def _(S):
    return fig(S, 6.5, hy=9.5, top=15, hw=4.5) + hat_hard(S, 6.5, 9.5) + [
        line(seg(14.5, 21, 16.5, 4)), line(seg(21.5, 21, 19.5, 4)), line(seg(16.5, 4, 19.5, 4)),
        line(seg(15.6, 17, 20.4, 9)), line(seg(20.4, 17, 15.6, 9))]


@icon("electrician", CAT, "Person in a hard hat beside a lightning bolt.",
      tags=["electrical", "wiring", "power", "lightning", "voltage", "lineman"])
def _(S):
    bolt = [(19.5, 3), (14, 12), (18, 12), (16.5, 21), (22, 10.5), (18, 10.5)]
    return fig(S, 6.5, hy=9.5, top=15, hw=4.5) + hat_hard(S, 6.5, 9.5) + [shell(poly(bolt, closed=True, r=S.r * 0.5))]


@icon("plumber", CAT, "Person in a cap beside a bent pipe with a drip.",
      tags=["plumbing", "pipes", "water", "leak", "repair", "pipe wrench"])
def _(S):
    return fig(S, 6.5, hy=9.5, top=15, hw=4.5) + hat_cap(S, 6.5, 9.5) + [
        line(poly([(14, 21), (14, 12), (22, 12)], r=S.r)), solid("M18.5 14.5C19.75 16.25 20.5 17.25 20.5 18.25A2 2 0 0 1 16.5 18.25C16.5 17.25 17.25 16.25 18.5 14.5Z")]


@icon("carpenter", CAT, "Person with a hand saw above a wooden plank.",
      tags=["woodworker", "joiner", "saw", "wood", "plank", "woodwork"])
def _(S):
    import math
    a = math.radians(30)

    def tr(pts):
        return [(16 + x * math.cos(a) - y * math.sin(a), 11.5 + x * math.sin(a) + y * math.cos(a)) for x, y in pts]
    handle = poly(tr([(-7.5, -3), (-4, -3), (-4, 3), (-7.5, 3)]), closed=True, r=S.r)
    blade = poly(tr([(-4, -2), (5.5, -0.5), (5.5, 2), (-4, 3)]), closed=True, r=S.r * 0.5)
    return fig(S, 5.5, hy=9.5, top=15, hw=3.5) + [shell(handle), shell(blade)]


@icon("bricklayer", CAT, "Person with a trowel beside a short brick wall.",
      tags=["mason", "bricks", "wall", "trowel", "construction", "masonry"])
def _(S):
    return fig(S, 6.5, hw=4.5) + [
        shell(rect(12, 11, 10, 9, rr_(S, 1))), detail(seg(12, 15.5, 22, 15.5)), detail(seg(17, 11, 17, 15.5)),
        detail(seg(14.5, 15.5, 14.5, 20)), detail(seg(19.5, 15.5, 19.5, 20)),
        line(seg(12.5, 6, 15.5, 6)), shell(poly([(15.5, 6), (18.5, 3.5), (22, 6), (18.5, 8.5)], closed=True, r=S.r * 0.5))]


@icon("roofer", CAT, "Person with a hammer above a sloped shingled roof.",
      tags=["roofing", "roof", "shingles", "hammer", "builder", "construction"])
def _(S):
    return fig(S, 6, hy=7.5, top=13.5, hw=4, bottom=21) + hat_hard(S, 6, 7.5) + [
        line(poly([(11.5, 21), (17, 14.5), (22.5, 21)], r=S.r)), shell(rect(14, 3, 6, 3.5, rr_(S, 1))), line(seg(17, 6.5, 17, 11))]


@icon("house-painter", CAT, "Person in a paper hat holding a long paint roller.",
      tags=["painter and decorator", "paint roller", "decorating", "wall painting", "renovation", "diy"])
def _(S):
    return fig(S, 6.5, hy=9.5, top=15, hw=4.5) + hat_paper(S, 6.5, 9.5) + [
        shell(rect(12, 3.5, 9, 4.5, rr_(S, 1.5))), line(poly([(21, 5.75), (22.5, 5.75), (22.5, 11), (16.5, 11), (16.5, 13)], r=S.r)),
        line(seg(16.5, 13, 16.5, 21))]


@icon("locksmith", CAT, "Person beside a padlock with a keyhole.",
      tags=["lock", "key", "padlock", "security", "lockout", "keys"])
def _(S):
    return fig(S, 6, hw=4) + [line("M14.5 11.5V8.5a3 3 0 0 1 6 0V11.5"), shell(rect(12.5, 11.5, 10, 9, rr_(S, 2))), dot(17.5, 15, 1)]


@icon("blacksmith", CAT, "Person with a hammer raised above an anvil.",
      tags=["smith", "forge", "anvil", "hammer", "metalwork", "ironwork"])
def _(S):
    anvil = [(11.5, 12.5), (22, 12.5), (22, 15), (19.5, 15), (18.5, 17.5), (21, 20.5), (12.5, 20.5), (15, 17.5), (15, 15), (11.5, 15)]
    return fig(S, 5.5, hw=3.5) + [shell(poly(anvil, closed=True, r=S.r * 0.4)), shell(rrot(19, 5, 6, 3.5, 45, r=S.r * 0.6)), line(seg(17, 7, 13.5, 10.5))]


@icon("tailor", CAT, "Person with a tape measure around the neck beside a needle and thread.",
      tags=["seamstress", "sewing", "needle", "tape measure", "dressmaker", "alterations"])
def _(S):
    return fig(S, 6.5, hw=4.5) + [detail(seg(5.25, 13.5, 5.25, 18.5)), detail(seg(7.75, 13.5, 7.75, 18.5)),
                                  line(seg(14, 21, 20.5, 6)), line("M20.5 6C23 3 18.5 2.5 18.5 5.5C18.5 8 22.5 8 22.5 11")]


@icon("cobbler", CAT, "Person with a hammer above a shoe.",
      tags=["shoemaker", "shoe repair", "cobbling", "shoes", "hammer", "footwear"])
def _(S):
    shoe = [(12, 11.5), (15.5, 11.5), (16, 15), (21.5, 16.5), (22, 20.5), (12, 20.5)]
    return fig(S, 6, hy=8, top=14, hw=4) + [shell(poly(shoe, closed=True, r=S.r * 0.6)), shell(rect(12.5, 3, 6, 3, rr_(S, 1))), line(seg(15.5, 6, 15.5, 8.5))]


@icon("watchmaker", CAT, "Person with tweezers above an open watch.",
      tags=["horologist", "watch repair", "clockmaker", "tweezers", "watch", "timepiece"])
def _(S):
    return fig(S, 6, hw=4) + [line(poly([(14, 3), (17.5, 9)], r=S.r)), line(poly([(21, 3), (17.5, 9)], r=S.r)),
                              shell(circle(17.5, 15, 5)), detail(poly([(17.5, 12.75), (17.5, 15), (19.5, 15)], r=S.r))]


# ============================================================================ personal care, food and service

@icon("barber", CAT, "Person beside a striped barber pole.",
      tags=["barbershop", "haircut", "hair salon", "barber pole", "grooming", "clippers"])
def _(S):
    return fig(S, 6.5, hw=4.5) + [shell(rect(15, 6, 5.5, 11, rr_(S, 1.5))), detail(seg(15.5, 13.5, 20, 9.5)),
                                  line(seg(14, 3.5, 21.5, 3.5)), line(seg(14, 19.5, 21.5, 19.5))]


@icon("hairdresser", CAT, "Person beside a pair of scissors.",
      tags=["hair stylist", "salon", "haircut", "scissors", "hairstyle", "beauty"])
def _(S):
    return fig(S, 6.5, hw=4.5) + [line(seg(15.5, 17, 20.5, 3.5)), line(seg(20.5, 17, 15.5, 3.5)),
                                  shell(circle(15.25, 18.25, 2)), shell(circle(20.75, 18.25, 2))][:4]


@icon("makeup-artist", CAT, "Person beside a large fluffy makeup brush.",
      tags=["make-up", "cosmetics", "beauty", "brush", "stylist", "face"])
def _(S):
    return fig(S, 6.5, hw=4.5) + [line(seg(13, 21, 17.5, 12)), shell("M17.5 12C14.5 9.5 15 4 20 3C22.5 5.5 21.5 9.5 17.5 12Z")]


@icon("tattoo-artist", CAT, "Person with a tattoo machine over a forearm marked with a dot.",
      tags=["tattoo", "ink", "body art", "tattoo machine", "needle", "studio"])
def _(S):
    return fig(S, 6, hw=4) + [shell(rect(16, 3, 4.5, 7, rr_(S, 1.5))), line(seg(18.25, 10, 18.25, 14.5)),
                              shell(rect(11, 14.5, 11, 6.5, rr_(S, 2.5))), solid(poly([polar(16.5, 17.75, 2.4 if i % 2 == 0 else 1.0, -90 + i * 36) for i in range(10)], closed=True))]


@icon("nail-technician", CAT, "Person beside a bottle of nail polish.",
      tags=["manicurist", "nails", "manicure", "nail polish", "beauty", "salon"])
def _(S):
    return fig(S, 6, hw=4) + [shell(rect(15.5, 2.5, 4, 5.5, rr_(S, 1.5))), shell(circle(17.5, 15, 5)), dot(17.5, 15, 1)]


@icon("florist", CAT, "Person holding a wrapped bouquet of flowers.",
      tags=["flowers", "bouquet", "flower shop", "floral", "blooms", "arrangement"])
def _(S):
    return fig(S, 6, hw=4) + [shell("M13.5 3.5V8C13.5 10.75 15.5 12 17.75 12C20 12 22 10.75 22 8V3.5L19.75 5.75L17.75 3.5L15.75 5.75Z" if S.name != "line" else "M13.5 3.5V8C13.5 10.75 15.5 12 17.75 12C20 12 22 10.75 22 8V3.5L19.75 5.75L17.75 3.5L15.75 5.75Z"),
                              line(seg(17.75, 12, 17.75, 21)), line(poly([(17.75, 19), (14, 16.5)], r=S.r))]


@icon("arborist", CAT, "Person in a helmet with a rope harness beside a tree.",
      tags=["tree surgeon", "tree climber", "tree care", "rope", "helmet", "pruning"])
def _(S):
    return fig(S, 6, hy=9.5, top=15, hw=4) + hat_hard(S, 6, 9.5) + [
        shell(poly([(17.5, 3), (22.5, 12), (12.5, 12)], closed=True, r=S.r * 0.6)), line(seg(17.5, 12, 17.5, 21)),
        line(poly([(10.5, 17), (14, 15.5), (17.5, 17)], r=S.r))]


@icon("cowboy", CAT, "Person in a cowboy hat with a neckerchief.",
      tags=["cowgirl", "rancher", "wild west", "western", "cowboy hat", "ranch"])
def _(S):
    return fig(S, 12, hy=10, hr=2.5, top=15.5, hw=7) + [
        shell(poly([(8.75, 8.5), (9, 4.5), (12, 5.75), (15, 4.5), (15.25, 8.5)], closed=True, r=S.r * 0.6)), line("M5 7C6.5 9.5 9 8.5 12 8.5C15 8.5 17.5 9.5 19 7"),
        solid("M9.5 16L14.5 16L12 19.5Z")]


@icon("jockey", CAT, "Person in a peaked riding cap and diamond silks holding a crop.",
      tags=["horse racing", "rider", "racing silks", "derby", "equestrian", "riding crop"])
def _(S):
    return fig(S, 9, hy=9.5, hr=2.5, top=15, hw=6) + hat_cap(S, 9, 9.5) + [
        detail(poly([(9, 15.5), (11.5, 18.5), (9, 21.5), (6.5, 18.5)], closed=True)) if False else detail(poly([(9, 15.5), (11, 18.25), (9, 21), (7, 18.25)], closed=True)),
        line(seg(16, 21, 21, 6)), line("M21 6l1.5-2")]


@icon("butcher", CAT, "Person in a striped apron holding a meat cleaver.",
      tags=["meat", "cleaver", "butchery", "meat cutter", "deli", "chopping"])
def _(S):
    return fig(S, 6.5, hw=4.5) + [detail(seg(4.75, 14, 4.75, 21)), detail(seg(8.25, 14, 8.25, 21)),
                                  shell(rect(12.5, 3.5, 9.5, 8, rr_(S, 1.5))), dot(15.5, 7.5, 1), shell(rect(16, 13.5, 3.5, 7, rr_(S, 1.5)))]


@icon("pizza-maker", CAT, "Person tossing a round pizza dough into the air.",
      tags=["pizzaiolo", "pizza", "dough", "pizzeria", "italian", "baker"])
def _(S):
    return fig(S, 6.5, hy=9.5, top=15, hw=4.5) + [shell(circle(17.5, 8, 4.75)), dot(16, 6.5, 0.9), dot(19, 7, 0.9), dot(17, 10, 0.9), line(seg(13.5, 12, 11.5, 17.5))]


@icon("sushi-chef", CAT, "Person in a headband holding a long knife over a sushi roll.",
      tags=["sushi", "japanese cuisine", "itamae", "knife", "sushi roll", "chef"])
def _(S):
    return fig(S, 6.5, hy=9.5, top=15, hw=4.5) + [line(seg(3.5, 8.5, 9.5, 8.5)), shell(poly([(11, 6.5), (21.5, 4.5), (21.5, 8), (11, 8)], closed=True, r=S.r * 0.4)),
                                                  shell(circle(17, 16.5, 4)), dot(17, 16.5, 1)]


@icon("grill-master", CAT, "Person in an apron beside a barbecue grill with flames.",
      tags=["barbecue", "bbq", "grilling", "cookout", "flames", "grill"])
def _(S):
    return fig(S, 6, hy=9.5, top=15, hw=4) + [shell("M12.5 14H22.5A5 5 0 0 1 12.5 14Z"),
                                               solid("M17.5 3C19.5 6 21 7 21 9.5A3.5 3.5 0 0 1 14 9.5C14 7.5 15.5 6.5 15.5 5C16.5 6 16.75 6.25 17.5 6.25C17.25 5 17 4 17.5 3Z")]


@icon("barista", CAT, "Person in an apron holding a coffee cup with steam.",
      tags=["coffee", "cafe", "espresso", "coffee shop", "latte", "cup"])
def _(S):
    return fig(S, 6, hw=4) + [shell(poly([(12.5, 11), (19.5, 11), (19.5, 15), (17, 19), (15, 19), (12.5, 15)], closed=True, r=S.r * 0.6)),
                              line("M19.5 12.5H20.5a1.5 1.5 0 0 1 0 3.5H19.5"), line(seg(14.5, 4, 14.5, 8)), line(seg(17.5, 3, 17.5, 8))]


@icon("bartender", CAT, "Person with a cocktail shaker above a shallow glass.",
      tags=["barman", "bar", "cocktail", "shaker", "mixologist", "drinks"])
def _(S):
    return fig(S, 6, hw=4) + [shell(poly([(12.5, 3.5), (17.5, 3.5), (17, 11), (13, 11)], closed=True, r=S.r * 0.5)),
                              shell(poly([(14.5, 14), (22, 14), (18.25, 18.5)], closed=True, r=S.r * 0.5)), line(seg(18.25, 18.5, 18.25, 21))][:3]


@icon("sommelier", CAT, "Person in a vest swirling a glass of wine.",
      tags=["wine steward", "wine", "wine glass", "vineyard", "tasting", "restaurant"])
def _(S):
    return fig(S, 6, hw=4) + [detail(poly([(3.5, 13.5), (6, 18), (8.5, 13.5)], r=S.r * 0.5)),
                              shell("M14 4H22C22 9 20.5 11.5 18 11.5S14 9 14 4Z"), line(seg(18, 11.5, 18, 18.5)), line(seg(15.5, 19.5, 20.5, 19.5))]


def sq(d) -> Part:
    """Small solid region: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


# ============================================================================ hotels, cleaning and street work

@icon("doorman", CAT, "Person in a peaked cap beside an open door.",
      tags=["door attendant", "hotel", "entrance", "porter", "greeter", "uniform"])
def _(S):
    return fig(S, 6.5, hy=9.5, top=15, hw=4.5) + hat_cap(S, 6.5, 9.5) + [shell(rect(14, 3, 8, 18, rr_(S, 1.5))), dot(16.5, 12.5, 1)]


@icon("concierge", CAT, "Person behind a desk with a service bell.",
      tags=["hotel", "front desk", "reception", "service bell", "guest services", "hospitality"])
def _(S):
    return [shell(circle(7, 7, 2.25)), shell(bust(S, 7, 12, 4.5, 16)), shell(rect(2.5, 16, 19, 5, rr_(S, 1.5))),
            shell("M15.25 14A3.25 3.25 0 0 1 21.75 14Z"), dot(18.5, 7.5, 1)]


@icon("bellhop", CAT, "Person in a pillbox cap pushing a suitcase on a luggage cart.",
      tags=["porter", "luggage", "hotel", "baggage", "suitcase", "cart"])
def _(S):
    return fig(S, 6, hy=9.5, top=15, hw=4) + hat_cap(S, 6, 9.5, visor=False, top=3.25) + [
        shell(rect(12.5, 10, 9.5, 8, rr_(S, 2))), line("M15.5 10V7.5h3.5V10"), dot(14.5, 20.5, 0.9), dot(20, 20.5, 0.9)]


@icon("valet-attendant", CAT, "Person in a vest holding up a car key beside the front of a car.",
      tags=["valet parking", "car park", "parking attendant", "car key", "hotel", "restaurant"])
def _(S):
    return fig(S, 6, hy=9.5, top=15, hw=4) + [
        shell(circle(19.5, 5, 2.25)), line(seg(17.25, 5, 13, 5)), line(seg(14.75, 5, 14.75, 7.5)),
        shell(rect(12.5, 13.5, 10, 6.5, rr_(S, 2.5))), line("M14.5 13.5L15.75 10.5H19.25L20.5 13.5"), dot(15, 16.75, 0.9), dot(20, 16.75, 0.9)]


@icon("housekeeper", CAT, "Person in a small cap holding a spray bottle.",
      tags=["maid", "cleaner", "hotel cleaning", "spray bottle", "domestic", "housekeeping"])
def _(S):
    return fig(S, 6, hy=9.5, top=15, hw=4) + hat_cap(S, 6, 9.5, visor=False, top=3) + [
        shell(rect(13, 11, 7, 9.5, rr_(S, 2))), line(poly([(15, 11), (15, 7.5), (22, 7.5)], r=S.r)), line(seg(18.5, 11, 18.5, 9))][:4]


@icon("janitor", CAT, "Person with a mop beside a bucket on wheels.",
      tags=["cleaner", "custodian", "mop", "bucket", "cleaning", "maintenance"])
def _(S):
    return fig(S, 6, hw=4) + [line(seg(13, 3, 17, 14)), shell(poly([(12, 13.5), (22.5, 13.5), (21, 20), (13.5, 20)], closed=True, r=S.r * 0.6)),
                              dot(14, 21, 0.9), dot(20, 21, 0.9)][:3]


@icon("window-cleaner", CAT, "Person beside a window pane with a squeegee wiping it.",
      tags=["glass cleaner", "squeegee", "windows", "high rise", "cleaning", "washing"])
def _(S):
    return fig(S, 6, hw=4) + [shell(rect(12.5, 3, 9.5, 12, rr_(S, 1.5))), detail(seg(17.25, 3, 17.25, 15)), detail(seg(12.5, 9, 22, 9)),
                              line(seg(12.5, 19.5, 22, 19.5))][:5]


@icon("chimney-sweep", CAT, "Person in a top hat holding a round chimney brush on a rod.",
      tags=["chimney", "soot", "brush", "top hat", "fireplace", "sweeping"])
def _(S):
    spokes = [line(seg(*polar(17.5, 8, 3, a), *polar(17.5, 8, 5.25, a))) for a in range(0, 360, 45)]
    return fig(S, 6, hy=10.5, top=16, hw=4) + hat_top(S, 6, 10.5) + [shell(circle(17.5, 8, 2.5)), line(seg(17.5, 10.5, 17.5, 21))] + spokes


@icon("pest-control-technician", CAT, "Person in a respirator mask holding a spray can with a bug in the mist.",
      tags=["exterminator", "pest control", "insects", "spray", "bug", "fumigation"])
def _(S):
    return fig(S, 6, hw=4) + [sq(rect(3.9, 7.2, 4.2, 2, 1)), shell(rect(12, 9, 5, 11, rr_(S, 1.5))), shell(rect(13.25, 5.5, 2.5, 3.5, rr_(S, 1))),
                              dot(19.5, 6.5, 0.9), dot(21.5, 9, 0.9), dot(19.5, 11.5, 0.9), solid(ellipse(20.25, 16.5, 1.7, 2.5))][:7]


@icon("garbage-collector", CAT, "Person in a safety vest lifting a wheeled bin.",
      tags=["waste collector", "refuse", "bin man", "trash", "sanitation", "rubbish"])
def _(S):
    return fig(S, 6, hw=4) + [shell(poly([(13, 8.5), (22, 8.5), (21, 20), (14, 20)], closed=True, r=S.r * 0.6)), line(seg(12.5, 6, 22.5, 6)),
                              line(seg(17.5, 11.5, 17.5, 17))]


@icon("street-sweeper", CAT, "Person in a vest holding a wide broom.",
      tags=["road sweeper", "broom", "sweeping", "street cleaner", "city", "litter"])
def _(S):
    return fig(S, 6, hw=4) + [line(seg(17.5, 3, 17.5, 15)), shell(poly([(13, 15), (22, 15), (23, 20.5), (12, 20.5)], closed=True, r=S.r * 0.4))]


@icon("road-worker", CAT, "Person in a hard hat and striped vest holding a stop sign paddle.",
      tags=["flagger", "traffic control", "roadwork", "stop sign", "highway", "construction"])
def _(S):
    return fig(S, 6, hy=9.5, top=15, hw=4) + hat_hard(S, 6, 9.5) + [
        detail(seg(4.5, 15.5, 4.5, 21)) if False else detail(seg(4.75, 15.5, 4.75, 21)), detail(seg(7.25, 15.5, 7.25, 21)),
        shell(poly(regular(17.5, 8, 5, 8, -67.5), closed=True, r=S.r * 0.5)), detail(seg(15, 8, 20, 8)), line(seg(17.5, 13, 17.5, 21))]


@icon("jackhammer-operator", CAT, "Person in ear defenders gripping a jackhammer with dust at the base.",
      tags=["pneumatic drill", "demolition", "breaker", "construction", "ear defenders", "roadwork"])
def _(S):
    return fig(S, 6, hy=8.5, hr=2, top=14.5, hw=4) + phones(6, 8.5, 4.25) + [
        line(seg(14, 4.5, 21, 4.5)), shell(rect(15.75, 4.5, 4.5, 8, rr_(S, 1.5))), line(seg(18, 12.5, 18, 19)),
        dot(14, 20.5, 0.9), dot(22, 20.5, 0.9)]


@icon("crane-operator", CAT, "Person in a cab under the jib of a tower crane with a hook.",
      tags=["construction crane", "tower crane", "hoist", "hook", "builder", "lifting"])
def _(S):
    return fig(S, 6, hy=9.5, top=15, hw=4) + [
        line(seg(12.5, 4, 22.5, 4)), line(seg(19.5, 4, 19.5, 21)), line(seg(15.25, 4, 15.25, 12)), shell(rect(13, 12, 4.5, 3.5, rr_(S, 1)))]


@icon("forklift-operator", CAT, "Person seated in a forklift with raised forks carrying a pallet.",
      tags=["lift truck", "warehouse", "pallet", "forks", "logistics", "loading"])
def _(S):
    return [shell(circle(8, 7, 2)), line(seg(8, 9.5, 8, 12.5)), line(poly([(4.5, 12.5), (4.5, 3), (11.5, 3)], r=S.r)),
            shell(rect(3, 12.5, 12, 5.5, rr_(S, 2.5))), dot(6.5, 20.25, 1.1), dot(12, 20.25, 1.1),
            line(seg(17.5, 4, 17.5, 20)), line(seg(17.5, 17.5, 22.5, 17.5)), shell(rect(18.75, 11.5, 3.5, 4, rr_(S, 1)))]


@icon("warehouse-worker", CAT, "Person in a vest pushing a hand truck stacked with two boxes.",
      tags=["stockroom", "logistics", "hand truck", "boxes", "packing", "loader"])
def _(S):
    return fig(S, 6, hw=4) + [line(seg(13, 3, 13, 19.5)), line(seg(13, 19.5, 22, 19.5)), shell(rect(15, 4.5, 6.5, 4, rr_(S, 1))),
                              shell(rect(15, 11.5, 6.5, 4, rr_(S, 1)))]


@icon("factory-worker", CAT, "Person in a hard hat beside a conveyor belt carrying a box.",
      tags=["manufacturing", "assembly line", "production", "conveyor", "plant worker", "industrial"])
def _(S):
    return fig(S, 6, hy=9.5, top=15, hw=4) + hat_hard(S, 6, 9.5) + [
        shell(rect(12, 15.5, 10.5, 4.5, rr_(S, 2.25))), shell(rect(14.5, 8.5, 5.5, 4.5, rr_(S, 1)))]


@icon("deep-sea-diver", CAT, "Diver in a round helmet with a front window and an air hose.",
      tags=["diving suit", "helmet diver", "underwater", "salvage", "ocean", "air hose"])
def _(S):
    return [shell(circle(11, 8, 4.75)), dot(11, 8, 1.9), line(seg(6.5, 13.5, 15.5, 13.5)), shell(bust(S, 11, 16, 6, 21)),
            line("M16 8C20 8 21 12 21 20")]


@icon("scuba-diver", CAT, "Diver in a mask and snorkel with an air tank on the back.",
      tags=["scuba", "snorkel", "diving mask", "air tank", "underwater", "dive"])
def _(S):
    return fig(S, 9, hy=8.5, hr=2.5, top=14.5, hw=5) + [shell(rect(5.75, 6.5, 6.5, 4, rr_(S, 2))), line(poly([(13.25, 8.5), (15.5, 8.5), (15.5, 3.5)], r=S.r)),
                                                          shell(rect(15.5, 13, 4.5, 8, rr_(S, 2.25)))]
