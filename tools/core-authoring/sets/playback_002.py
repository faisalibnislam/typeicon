"""TypeIcon Core: playback, media controls and audio/video gear (batch 2)."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from dsl import D, I, P, ST, U
from geometry import fmt, path_to_d, polar

CAT = "playback"


# --------------------------------------------------------------------------- helpers

def pick(S, a, b):
    """Line value, Rounded value."""
    return a if S.name == "line" else b


def sdot(d) -> Part:
    """Solid region: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def sq(x, y, w, h, rx=0.0) -> Part:
    return Part("dot", rect(x, y, w, h, rx))


def tri(cx, cy, h, S=None, r=0.0):
    """Right-pointing play triangle centred on (cx, cy), height h."""
    w = h * 0.85
    return poly([(cx - w / 3, cy - h / 2), (cx + 2 * w / 3, cy), (cx - w / 3, cy + h / 2)], closed=True, r=r)


def arc_arrow(cx, cy, r, a0, a1, head=2.2, ccw=False):
    """Arc from a0 to a1 (clockwise unless ccw) with an open arrow head at the end."""
    d = arc(cx, cy, r, a0, a1) if not ccw else arc(cx, cy, r, a1, a0)
    end = a1 if not ccw else a0
    x, y = polar(cx, cy, r, end)
    sgn = -1 if ccw else 1
    tx, ty = -math.sin(math.radians(end)) * sgn, math.cos(math.radians(end)) * sgn
    nx, ny = math.cos(math.radians(end)), math.sin(math.radians(end))
    p1 = (x - tx * head + nx * head * 0.9, y - ty * head + ny * head * 0.9)
    p2 = (x - tx * head - nx * head * 0.9, y - ty * head - ny * head * 0.9)
    return d + f"M{fmt(p1[0])} {fmt(p1[1])}L{fmt(x)} {fmt(y)}L{fmt(p2[0])} {fmt(p2[1])}"


def head(x, y, dx, dy, s=2.2):
    """Open arrow head chevron with tip at (x, y) pointing along (dx, dy)."""
    n = math.hypot(dx, dy)
    dx, dy = dx / n, dy / n
    px, py = -dy, dx
    a = (x - dx * s + px * s, y - dy * s + py * s)
    b = (x - dx * s - px * s, y - dy * s - py * s)
    return f"M{fmt(a[0])} {fmt(a[1])}L{fmt(x)} {fmt(y)}L{fmt(b[0])} {fmt(b[1])}"


def wave_arc(x, cy, h, bulge):
    """Sound wave arc bulging right."""
    s = bulge
    R = (h * h + s * s) / (2 * s)
    return f"M{fmt(x)} {fmt(cy - h)}A{fmt(R)} {fmt(R)} 0 0 1 {fmt(x)} {fmt(cy + h)}"


def brackets(x0, y0, x1, y1, n, S=None):
    """Four corner brackets of a frame, arm length n."""
    return [
        line(f"M{fmt(x0)} {fmt(y0 + n)}V{fmt(y0)}H{fmt(x0 + n)}"),
        line(f"M{fmt(x1 - n)} {fmt(y0)}H{fmt(x1)}V{fmt(y0 + n)}"),
        line(f"M{fmt(x1)} {fmt(y1 - n)}V{fmt(y1)}H{fmt(x1 - n)}"),
        line(f"M{fmt(x0 + n)} {fmt(y1)}H{fmt(x0)}V{fmt(y1 - n)}"),
    ]


def earbud_icon_parts(S):
    return []


# =========================================================================== chunk 1

@icon("speed-ramp", CAT, "Video clip with a smooth S curve rising across it from slow to fast",
      tags=["slow motion", "time remap", "video editing", "speed curve", "acceleration", "timeline"])
def _(S):
    return [shell(rect(3, 4, 18, 16, S.R)), detail("M6.5 16C12 16 12 8 17.5 8")]


@icon("video-stabilization", CAT, "Steady video frame with wobble lines along both sides",
      tags=["stabilize", "shake", "steady", "video editing", "camera", "smooth"])
def _(S):
    return [shell(rect(7.5, 7.5, 9, 9, S.R * 0.5)), dot(12, 12, 1.25),
            line("M3.5 6.5C2 8.5 5 9.5 3.5 12C2 14.5 5 15.5 3.5 17.5"),
            line("M20.5 6.5C19 8.5 22 9.5 20.5 12C19 14.5 22 15.5 20.5 17.5")]


@icon("earbud-case", CAT, "Pill shaped charging case with its lid open above two earbuds",
      tags=["earbuds", "charging case", "wireless earphones", "earphones", "charger", "audio"])
def _(S):
    return [shell(rect(3, 12, 18, 9, S.R * 1.1)),
            line(poly([(3, 12), (3, 8), (6, 3.5), (18, 3.5), (21, 8), (21, 12)], r=S.r * 2)),
            dot(8.5, 16.5, 1.6), dot(15.5, 16.5, 1.6)]


@icon("neckband-earphones", CAT, "U shaped neckband with an earbud at each end",
      tags=["neckband", "wireless earphones", "bluetooth", "earphones", "sport", "audio"])
def _(S):
    band = ("M5.5 8.5V13L9 18.5H15L18.5 13V8.5" if S.name == "line"
            else "M5.5 8.5V12.5A6.5 6.5 0 0 0 18.5 12.5V8.5")
    return [line(band),
            shell(circle(5.5, 5.5, 2.5)), shell(circle(18.5, 5.5, 2.5))]


@icon("headphone-stand", CAT, "Upright stand with a crossbar holding a pair of over ear headphones",
      tags=["headphones", "stand", "holder", "hook", "desk", "audio"])
def _(S):
    return [line("M5 14V12.5A7 7 0 0 1 19 12.5V14"),
            shell(rect(3.5, 14, 4, 6, S.R * 0.5)), shell(rect(16.5, 14, 4, 6, S.R * 0.5)),
            line(seg(9.5, 9, 14.5, 9)), line(seg(12, 9, 12, 21)), line(seg(9, 21, 15, 21))]


@icon("simulcast", CAT, "Play button circle with branches fanning out to three small screens",
      tags=["multi stream", "broadcast", "multistream", "live", "stream to many", "streaming"])
def _(S):
    return [shell(circle(7, 12, 5)), sdot(tri(7.4, 12, 4.5)),
            line("M12 12H14M14 5V19M14 5H16M14 12H16M14 19H16"),
            solid(rect(16, 3, 5, 4, 0.5)), solid(rect(16, 10, 5, 4, 0.5)), solid(rect(16, 17, 5, 4, 0.5))]


@icon("intermission", CAT, "Closed stage curtains with a small hourglass in the middle",
      tags=["interval", "break", "theatre", "curtains", "pause", "show", "stage"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R * 0.5)), detail(seg(3, 7, 21, 7)),
            detail(seg(6.5, 7, 6.5, 21)), detail(seg(17.5, 7, 17.5, 21)),
            sdot(poly([(10, 10), (14, 10), (10, 17), (14, 17)], closed=True))]


@icon("vintage-movie-camera", CAT, "Old fashioned film camera on a tripod with two reels on top and a crank",
      tags=["film camera", "cinema", "retro", "director", "silent film", "tripod", "reels"])
def _(S):
    return [shell(rect(5, 10.5, 11, 6.5, S.R * 0.5)), shell(circle(7.75, 6.5, 2.75)), shell(circle(13.25, 6.5, 2.75)),
            shell(poly([(16, 11.5), (20, 10), (20, 17.5), (16, 16)], closed=True, r=S.r * 0.5)),
            line(seg(5, 13.5, 2.5, 13.5)),
            line(seg(10.5, 17, 7, 21.5)), line(seg(10.5, 17, 14, 21.5)), line(seg(10.5, 17, 10.5, 21.5))]


@icon("audio-only", CAT, "Dashed video frame with a pair of headphones in the middle",
      tags=["no video", "podcast", "listen", "audio mode", "background play", "headphones"])
def _(S):
    d = []
    for (x, y, dx, dy) in [(3, 4, 1, 0), (3, 20, 1, 0)]:
        for a, b in [(0, 4), (7, 11), (14, 18)]:
            d.append(line(seg(x + a, y, x + b, y)))
    for x in (3, 21):
        for a, b in [(4, 7.5), (10.25, 13.75), (16.5, 20)]:
            d.append(line(seg(x, a, x, b)))
    return d + [line("M8.5 13.5V12.5A3.5 3.5 0 0 1 15.5 12.5V13.5"),
                shell(rect(7.5, 13, 2.5, 4, 1)), shell(rect(14, 13, 2.5, 4, 1))]


@icon("video-loop", CAT, "Video frame with a looping arrow circling a small play triangle",
      tags=["repeat video", "loop", "replay", "repeat", "gif", "looping clip"])
def _(S):
    return [shell(rect(2.5, 3.5, 19, 17, S.R)), detail(arc_arrow(12, 12, 4.25, -60, 240, 2)),
            sdot(tri(12.3, 12, 3))]


@icon("frame-capture", CAT, "Shutter aperture inside corner brackets; grab a still frame from video",
      tags=["screenshot", "still frame", "snapshot", "grab frame", "capture", "freeze frame"])
def _(S):
    return brackets(3, 3, 21, 21, 4.5) + [shell(circle(12, 12, 4.5)), sdot(poly(regular(12, 12, 2, 6), closed=True))]


@icon("dvr", CAT, "Flat set top recorder box with a record dot and a clock display",
      tags=["digital video recorder", "set top box", "recorder", "tv recording", "schedule recording", "cable box"])
def _(S):
    return [shell(rect(2.5, 7.5, 19, 10, S.R * 0.75)), dot(7, 12.5, 1.75),
            detail(circle(15.5, 12.5, 2.5)), line(seg(6, 17.5, 6, 19.5)), line(seg(18, 17.5, 18, 19.5))]


@icon("tv-input-source", CAT, "Television with an arrow pointing into its left side; choose the input",
      tags=["input", "source", "hdmi", "external input", "switch input", "tv settings"])
def _(S):
    return [shell(rect(9, 4, 12, 13, S.R)), line(seg(12, 20.5, 18, 20.5)),
            line(seg(2.5, 10.5, 8, 10.5)), line(head(8, 10.5, 1, 0, 2.5))]


@icon("party-speaker", CAT, "Tall floor speaker with two woofers and light rays over the top",
      tags=["pa speaker", "big speaker", "dj", "party", "loudspeaker", "sound system", "disco"])
def _(S):
    return [shell(rect(5, 6, 12, 15, S.R)), detail(circle(11, 11, 2.5)), detail(circle(11, 17, 2)),
            line(seg(19.5, 6.5, 21.5, 4.5)), line(seg(20, 10, 22, 10)), line(seg(17, 3.5, 17, 1.5))]


# =========================================================================== chunk 2

@icon("suitcase-record-player", CAT, "Portable suitcase record player with a turntable platter and tone arm",
      tags=["portable turntable", "vinyl", "record player", "retro", "briefcase", "music", "gramophone"])
def _(S):
    return [shell(rect(2.5, 8, 19, 12.5, S.R)), line(poly([(5, 8), (5, 3.5), (19, 3.5), (19, 8)], r=S.r)),
            detail(circle(10, 14.25, 3.75)), dot(10, 14.25, 1.1), dot(17.5, 11.5, 1.1),
            detail(poly([(17.5, 11.5), (17.5, 16.5), (15.5, 18)], r=S.r))]


@icon("cassette-adapter", CAT, "Cassette tape with a cable leaving its edge that ends in a jack plug",
      tags=["tape adapter", "car stereo", "aux", "audio cable", "mp3 adapter", "jack", "retro"])
def _(S):
    return [shell(rect(2, 3.5, 16, 14, S.R)), detail(circle(7, 9, 1.75)), detail(circle(13, 9, 1.75)),
            detail(poly([(5, 17.5), (6.75, 13), (13.25, 13), (15, 17.5)], r=S.r * 0.5)),
            line("M18 8H18.5A2 2 0 0 1 20.5 10V14"), sq(19, 14, 3, 5, 0.5), line(seg(20.5, 19, 20.5, 21.5))]


@icon("radio-presets", CAT, "Radio with a tuning display above six preset buttons",
      tags=["station presets", "favorite stations", "car radio", "tuner", "memory buttons", "fm", "am"])
def _(S):
    parts = [shell(rect(2.5, 3, 19, 18, S.R)), detail(rect(5.5, 6, 13, 3.5, S.R * 0.25))]
    for r in (13, 17):
        for x in (5.5, 10.25, 15):
            parts.append(sq(x, r, 3.5, 2.25, 0.5))
    return parts


@icon("movie-poster", CAT, "Tall movie poster with a film strip across the top and title lines below",
      tags=["film poster", "cinema", "one sheet", "promo", "movie", "advert", "billboard"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 19, S.R * 0.5)), detail(seg(4.5, 8, 19.5, 8)),
            sq(7, 4.5, 2, 1.75), sq(11, 4.5, 2, 1.75), sq(15, 4.5, 2, 1.75),
            detail(seg(8, 13.5, 16, 13.5)), detail(seg(8, 17, 13.5, 17))]


@icon("age-rating", CAT, "Rounded badge with a big number seven and a plus sign; minimum age label",
      tags=["parental guidance", "content rating", "pg", "minimum age", "certificate", "rated", "kids"])
def _(S):
    return [shell(rect(2.5, 4.5, 19, 15, S.R)),
            detail(poly([(6.5, 8.75), (12, 8.75), (9, 15.5)], r=S.r * 0.3)),
            detail(seg(17, 9.25, 17, 14.75)), detail(seg(14.25, 12, 19.75, 12))]


@icon("outdoor-cinema", CAT, "Large screen on two poles standing on grass, showing a play triangle",
      tags=["open air cinema", "drive in", "movie night", "screen", "garden cinema", "projection", "summer"])
def _(S):
    return [shell(rect(4, 2.5, 16, 10.5, S.R * 0.5)), sdot(tri(12.4, 7.75, 4.5)),
            line(seg(8, 13, 8, 19)), line(seg(16, 13, 16, 19)),
            line("M2.5 19.5C5 18 7 21 9.5 19.5S14 21 16.5 19.5S19.5 18 21.5 19.5")]


@icon("capture-card", CAT, "Small box with an HDMI style port on the left and a cable plugged into the right",
      tags=["game capture", "hdmi capture", "streaming gear", "video input", "recorder", "usb", "streamer"])
def _(S):
    return [shell(rect(6.5, 6.5, 11, 11, S.R * 0.6)), dot(12, 12, 1.5),
            shell(poly([(2.5, 10), (6.5, 10), (6.5, 14), (4, 14), (2.5, 12.5)], closed=True)),
            line(seg(17.5, 12, 21.5, 12))]


@icon("reaction-video", CAT, "Video frame with a play triangle and a small face bubble in the corner",
      tags=["react", "picture in picture", "commentary", "streamer", "facecam", "response video", "video creator"])
def _(S):
    return [shell(rect(2.5, 3.5, 19, 17, S.R)), sdot(tri(8.5, 10.5, 5.5)),
            detail(circle(15.75, 13.25, 3.25)), dot(14.6, 12.75, 0.75), dot(16.9, 12.75, 0.75)]


@icon("dolly-track", CAT, "Camera on a wheeled cart rolling along a straight rail",
      tags=["camera dolly", "tracking shot", "film set", "crew", "cinematography", "rail", "movie"])
def _(S):
    return [shell(rect(5.5, 2.5, 8, 6, S.R * 0.5)),
            shell(poly([(13.5, 4.5), (18, 3), (18, 8), (13.5, 6.5)], closed=True, r=S.r * 0.4)),
            line(seg(9.5, 8.5, 9.5, 11.5)), line(seg(3.5, 11.5, 15.5, 11.5)),
            detail(circle(6.5, 15.5, 1.75)), detail(circle(13, 15.5, 1.75)),
            line(seg(2.5, 20.5, 21.5, 20.5))]


@icon("loop-recording", CAT, "Record dot inside a circular loop arrow; recording that overwrites itself",
      tags=["dash cam", "overwrite", "continuous recording", "cctv", "record loop", "rolling recording"])
def _(S):
    return [line(arc_arrow(12, 12, 8.5, -60, 240, 2.6)), dot(12, 12, 3.75)]


@icon("voice-changer", CAT, "Small microphone with a jagged wave that becomes a smooth wave",
      tags=["pitch shifter", "voice effect", "robot voice", "vocoder", "voice modulator", "audio effect"])
def _(S):
    return [shell(rect(4, 3, 4, 8.5, 2)), line(arc(6, 10, 4.5, 0, 180)),
            line(seg(6, 14.5, 6, 19)), line(seg(3.5, 19, 8.5, 19)),
            line(poly([(11, 12), (12.25, 8), (13.75, 16), (15, 12)], r=S.r * 0.3)),
            line("M15 12H16.5C17.5 7 20.5 7 21.5 12")]


@icon("parametric-equalizer", CAT, "Smooth EQ curve with one bell peak and one dip, each marked with a dot",
      tags=["eq", "audio mixing", "frequency", "filter", "bell curve", "sound settings", "mastering"])
def _(S):
    return [shell(rect(2.5, 3, 19, 18, S.R)),
            detail("M5.5 12C7 12 7 8 9 8S11 12 12 12S14 16 15.5 16S17 12 18.5 12"),
            dot(9, 8, 2.25), dot(15.5, 16, 2.25)]


@icon("car-infotainment", CAT, "Car dashboard screen with an album square and a play triangle between two vents",
      tags=["dashboard", "car audio", "head unit", "phone mirroring", "car stereo", "touchscreen"])
def _(S):
    return [shell(rect(7, 3.5, 10, 9, S.R * 0.6)), sq(9, 6, 3, 3), sdot(tri(14.25, 7.5, 3.5)),
            line(seg(2.5, 6.5, 5, 6.5)), line(seg(2.5, 10, 5, 10)), line(seg(19, 6.5, 21.5, 6.5)), line(seg(19, 10, 21.5, 10)),
            line(pick(S, "M2.5 17.5L9 15.5H15L21.5 17.5", "M2.5 17.5C6 15.5 9 15.5 12 15.5S18 15.5 21.5 17.5"))]


@icon("stadium-screen", CAT, "Large scoreboard screen on two legs above curved rows of stadium seats",
      tags=["jumbotron", "big screen", "scoreboard", "arena", "giant screen", "sports venue", "replay"])
def _(S):
    return [shell(rect(4, 2.5, 16, 8, S.R * 0.5)), line(seg(9, 10.5, 9, 16.3)), line(seg(15, 10.5, 15, 16.3)),
            line("M2.5 21.5A9.5 5.5 0 0 1 21.5 21.5"), line("M7 21.5A5 3 0 0 1 17 21.5")]


@icon("music-charts", CAT, "Ranked list of three songs with a note on top and trend arrows beside the rows",
      tags=["top songs", "hit parade", "top 40", "chart position", "ranking", "leaderboard", "popular tracks"])
def _(S):
    return [shell(circle(9, 6, 2)), line(seg(11, 6, 11, 2.5)), line(pick(S, "M11 2.5L15.5 4.5", "M11 2.5C12 4 14 4 15.5 4.5")),
            dot(4.5, 11.5, 1.1), line(seg(8, 11.5, 15, 11.5)), line(poly([(17.5, 12.75), (19, 11.25), (20.5, 12.75)], r=S.r * 0.3)),
            dot(4.5, 15.5, 1.1), line(seg(8, 15.5, 15, 15.5)), line(poly([(17.5, 14.75), (19, 16.25), (20.5, 14.75)], r=S.r * 0.3)),
            dot(4.5, 19.5, 1.1), line(seg(8, 19.5, 15, 19.5)), line(seg(17.5, 19.5, 20.5, 19.5))]


# =========================================================================== chunk 3

@icon("concert-ticket", CAT, "Ticket with notched sides, a perforation line and a music note on the main part",
      tags=["gig", "live music", "admission", "event ticket", "show", "festival", "pass"])
def _(S):
    body = "M2.5 6H21.5V10.5A1.5 1.5 0 0 0 21.5 13.5V18H2.5V13.5A1.5 1.5 0 0 0 2.5 10.5Z"
    return [shell(body), dot(17, 9, 0.9), dot(17, 12, 0.9), dot(17, 15, 0.9),
            dot(7.5, 14, 1.75), detail(seg(9.25, 14, 9.25, 8.5)), detail(pick(S, "M9.25 8.5L12.5 10", "M9.25 8.5C10.5 9 11.5 9.5 12.5 10"))]


@icon("portable-dvd-player", CAT, "Clamshell DVD player with a play triangle on the screen and a disc on the base",
      tags=["dvd", "travel video", "car dvd", "laptop style", "movie player", "disc player", "portable"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 10, S.R * 0.6)), sdot(tri(12.4, 7.5, 4.5)),
            shell(rect(2.5, 14.5, 19, 6, S.R * 0.6)), dot(7.5, 17.5, 1.5), detail(seg(12, 17.5, 18, 17.5))]


@icon("cinema-camera", CAT, "Boxy digital cinema camera with a large lens, a matte box in front and a top handle",
      tags=["movie camera", "film camera", "production", "digital cinema", "cinematography", "shoot", "video camera"])
def _(S):
    return [shell(rect(2.5, 9, 11, 9.5, S.R * 0.5)), line(poly([(5.5, 9), (5.5, 5.5), (11, 5.5), (11, 9)], r=S.r)),
            shell(rect(13.5, 11, 3.5, 5.5, S.R * 0.25)), shell(rect(17, 9, 4.5, 9.5, S.R * 0.5)), dot(6.5, 14, 1.25)]


@icon("burn-disc", CAT, "Compact disc with a small flame rising from its upper right edge",
      tags=["write cd", "burn cd", "copy to disc", "cd burner", "dvd burn", "optical", "record disc"])
def _(S):
    tip = pick(S, "M17.75 2C17.75 5 21.5 6.5 21.5 10", "M17.75 2.25C17.75 5 21.5 6.5 21.5 10")
    return [shell(circle(8, 15.5, 6.25)), dot(8, 15.5, 1.3),
            shell(tip + "A3.75 3.75 0 0 1 14 10C14 8.25 15 7 16 6C16.25 7.5 17 8 17.5 7.25C18 6 17.75 4 17.75 2Z")]


@icon("optical-drive", CAT, "Slim disc drive with its tray slid out holding a disc",
      tags=["cd drive", "dvd drive", "disc tray", "eject", "cd rom", "blu-ray", "computer drive"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 6, S.R * 0.5)), dot(17.5, 5.5, 0.9), detail(seg(5.5, 5.5, 12, 5.5)),
            shell(circle(12, 15, 4)), dot(12, 15, 1), line(seg(4, 20.75, 20, 20.75))]


@icon("merge-clips", CAT, "Two short timeline clips with an arrow pointing down into one longer clip",
      tags=["join clips", "combine video", "concatenate", "video editing", "timeline", "splice", "edit"])
def _(S):
    return [shell(rect(2.5, 2.5, 8.5, 5, S.R * 0.4)), shell(rect(13, 2.5, 8.5, 5, S.R * 0.4)),
            line(seg(12, 10, 12, 14)), line(head(12, 14, 0, 1, 2.25)),
            shell(rect(2.5, 16.5, 19, 5, S.R * 0.4))]


@icon("lower-third", CAT, "Video frame with a thick name bar and a thinner title bar across its lower left",
      tags=["caption bar", "name tag", "tv graphic", "news ticker", "title overlay", "broadcast graphics", "chyron"])
def _(S):
    return [shell(rect(2.5, 3.5, 19, 17, S.R)), sq(5.5, 10.5, 11, 3.75, 0.5), sq(5.5, 15.5, 7, 2, 0.5)]


@icon("cable-tv", CAT, "Television set with a thick coaxial cable leaving its back and ending in a screw plug",
      tags=["coax", "coaxial cable", "television", "antenna cable", "tv service", "satellite", "broadcast"])
def _(S):
    return [shell(rect(2.5, 4.5, 13, 11, S.R)), line(seg(6, 19, 12, 19)),
            line("M15.5 8.5H17.5C20 8.5 20 13 19 14.5"), sq(17, 14.5, 4, 3.25, 0.5), line(seg(19, 17.75, 19, 21))]


@icon("cd-wallet", CAT, "Zippered disc wallet opened flat with one disc on each page",
      tags=["cd case", "dvd holder", "disc folder", "disc storage", "media wallet", "sleeve", "album holder"])
def _(S):
    return [shell(rect(2, 4.5, 20, 15, S.R)), detail(seg(12, 4.5, 12, 19.5)),
            detail(circle(7, 12, 2)), detail(circle(17, 12, 2))]


@icon("cd-spindle", CAT, "Tall stack of discs on a central post with a domed lid lifted above",
      tags=["cd stack", "blank discs", "disc tub", "dvd pack", "cake box", "storage", "media"])
def _(S):
    return [shell("M6 7.5A6 4.5 0 0 1 18 7.5Z"), line(seg(12, 13, 12, 7.5)),
            shell(ellipse(12, 13, 7.5, 2.5)),
            line("M4.5 13V16.5A7.5 2.5 0 0 0 19.5 16.5V13"), line("M4.5 16.5V20A7.5 2.5 0 0 0 19.5 20V16.5")]


@icon("sleep-sounds", CAT, "Crescent moon with a music note and two gentle wave lines below",
      tags=["lullaby", "white noise", "night music", "relaxing sounds", "bedtime", "calm audio", "sleep music"])
def _(S):
    return [shell("M10 2.75A5.75 5.75 0 1 0 14.75 10.5A4.5 4.5 0 0 1 10 2.75Z"),
            dot(17.75, 9, 1.6), line(seg(19.35, 9, 19.35, 4)), line(pick(S, "M19.35 4L21.5 5.25", "M19.35 4C20 4.75 20.75 5 21.5 5.25")),
            line("M3 18.25C5 16.75 7 16.75 9 18.25S13 19.75 15 18.25S19 16.75 21 18.25"),
            line("M3 21.5C5 20 7 20 9 21.5S13 23 15 21.5S19 20 21 21.5")]


@icon("album-carousel", CAT, "Row of three album covers with the centre one facing forward and the sides angled away",
      tags=["cover flow", "album browser", "music library", "gallery", "swipe albums", "collection", "record sleeves"])
def _(S):
    return [solid("M2.5 8L5.5 6.75V15.25L2.5 14Z"), solid("M21.5 8L18.5 6.75V15.25L21.5 14Z"),
            shell(rect(7.5, 4.5, 9, 11, S.R * 0.25)), sdot(circle(12, 10, 2)),
            dot(9.5, 19.5, 1), dot(12, 19.5, 1), dot(14.5, 19.5, 1)]


@icon("computer-speakers", CAT, "Monitor on a desk flanked by two small upright speakers",
      tags=["pc speakers", "desktop audio", "stereo", "desk setup", "monitor", "multimedia", "sound"])
def _(S):
    return [shell(rect(8, 4, 8, 8, S.R * 0.4)), line(seg(12, 12, 12, 18)), line(seg(2.5, 20.5, 21.5, 20.5)),
            shell(rect(2, 9, 4.5, 11, S.R * 0.4)), dot(4.25, 11.75, 0.8), dot(4.25, 16.25, 1.2),
            shell(rect(17.5, 9, 4.5, 11, S.R * 0.4)), dot(19.75, 11.75, 0.8), dot(19.75, 16.25, 1.2)]


@icon("shower-speaker", CAT, "Round waterproof speaker hanging from a suction cup with water droplets beside it",
      tags=["waterproof speaker", "bluetooth speaker", "bathroom", "suction cup", "splash proof", "portable speaker", "shower music"])
def _(S):
    return [shell(circle(9.5, 14.5, 6.25)), detail(circle(9.5, 14.5, 2.5)),
            solid(pick(S, "M5.5 5.5L7.5 2.5H11.5L13.5 5.5Z", "M5.5 5.5A4 3.5 0 0 1 13.5 5.5Z")), line(seg(9.5, 5.5, 9.5, 8)),
            solid("M19 3C17.5 5 17 6 17 7A2 2 0 0 0 21 7C21 6 20.5 5 19 3Z"),
            solid("M19 13C17.75 14.75 17.25 15.5 17.25 16.5A1.75 1.75 0 0 0 20.75 16.5C20.75 15.5 20.25 14.75 19 13Z")]


# =========================================================================== chunk 4

@icon("bone-conduction-headphones", CAT, "Head in side view with a band curving behind it and a pad resting in front of the ear",
      tags=["open ear", "sport headphones", "bone conduction", "wraparound", "running headset", "bluetooth", "audio"])
def _(S):
    head = poly([(7, 21.5), (7, 18), (4.5, 13.5), (4.5, 9), (8, 4), (14, 3), (18.5, 6), (19.5, 10.5), (21.5, 14), (19, 15),
                 (19, 18), (16, 18.5), (16, 21.5)], closed=True, r=S.r * 2)
    return [shell(head), detail("M15.5 9.5V13A3.5 3.5 0 0 1 8.5 13V11"), sq(14.25, 9, 2.5, 4.5, 1)]


@icon("pay-per-view", CAT, "Television screen with a coin dropping into its top edge",
      tags=["ppv", "paid stream", "premium event", "rent movie", "buy to watch", "purchase", "boxing match"])
def _(S):
    return [shell(rect(3, 8.5, 18, 12, S.R)), sdot(tri(12.4, 14.5, 5)), shell(circle(12, 4.25, 2.75))]


@icon("motion-capture", CAT, "Standing figure with marker dots on its joints and a camera pointed at it",
      tags=["mocap", "animation", "tracking suit", "performance capture", "3d animation", "markers", "vfx"])
def _(S):
    return [shell(circle(8, 4.5, 2.25)), line(seg(8, 7.5, 8, 14)),
            line(poly([(3.5, 12.5), (8, 9), (12.5, 12.5)], r=S.r)), line(poly([(4.5, 21), (8, 14), (11.5, 21)], r=S.r)),
            dot(3.5, 12.5, 1.25), dot(12.5, 12.5, 1.25), dot(8, 14, 1.25),
            shell(rect(15.5, 8, 5.5, 5, S.R * 0.3)), line(seg(18.25, 13, 18.25, 16)), line(seg(15.5, 19.5, 21, 19.5))]


@icon("photosensitivity-warning", CAT, "Screen with a lightning bolt and a small eye below it; flashing lights warning",
      tags=["seizure warning", "flashing lights", "strobe", "epilepsy", "content warning", "flicker", "safety"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 12.5, S.R)),
            detail(poly([(13, 5), (8.5, 9.5), (12.5, 9.5), (10.5, 12.5)], r=S.r * 0.3)),
            line("M3 19.5C6 15.75 18 15.75 21 19.5C18 23.25 6 23.25 3 19.5Z"), dot(12, 19.5, 1.5)]


@icon("silent-disco", CAT, "Dancing figure wearing large headphones, one arm raised",
      tags=["headphone party", "dance", "wireless headphones", "club", "festival", "dancing", "rave"])
def _(S):
    return [shell(circle(12, 7.5, 2.5)), line("M6.5 9V7.5A5.5 5.5 0 0 1 17.5 7.5V9"),
            solid(rect(5.25, 8, 2.5, 4, 0.8)), solid(rect(16.25, 8, 2.5, 4, 0.8)),
            line(seg(12, 11, 12, 16)), line(poly([(7, 14.5), (12, 12.5), (17, 14), (19.5, 11)], r=S.r)),
            line(poly([(7.5, 21.5), (12, 16), (16, 21.5)], r=S.r))]


@icon("teletext", CAT, "Television screen filled with blocky text rows and a three digit page number on top",
      tags=["tv text news", "tv text", "page numbers", "videotext", "old tv news", "retro tv", "text service"])
def _(S):
    return [shell(rect(2.5, 3, 19, 15, S.R)), sq(5.5, 6, 5, 2.5), sq(13, 6, 1.5, 2.5), sq(15.75, 6, 1.5, 2.5),
            sq(5.5, 10.5, 6, 1.75), sq(13, 10.5, 5.5, 1.75), sq(5.5, 13.75, 8, 1.75), line(seg(8, 21, 16, 21))]


@icon("console-radiogram", CAT, "Long low wooden cabinet on tapered legs, one half a speaker and the other a lift up lid",
      tags=["radiogram", "hi-fi cabinet", "record cabinet", "vintage stereo", "mid century", "retro audio", "sideboard"])
def _(S):
    return [shell(rect(2.5, 8.5, 19, 8, S.R * 0.5)), detail(seg(12, 8.5, 12, 16.5)), detail(circle(7.25, 12.5, 2.25)),
            line(poly([(13.5, 8.5), (15, 4), (21, 4)], r=S.r)), dot(17, 12.5, 1.25),
            line(seg(5, 16.5, 3.5, 21)), line(seg(19, 16.5, 20.5, 21))]


@icon("dialogue-enhancement", CAT, "Speech bubble holding a tall sound wave above a flat background line",
      tags=["clear speech", "voice boost", "speech clarity", "dialogue boost", "tv audio", "subtitle audio", "hearing aid"])
def _(S):
    body = poly([(2.5, 2.5), (21.5, 2.5), (21.5, 16.5), (10, 16.5), (6, 21), (6, 16.5), (2.5, 16.5)], closed=True, r=S.r * 1.5)
    return [shell(body), detail(seg(6.5, 7.5, 6.5, 9.25)), detail(seg(10, 5.5, 10, 11)), detail(seg(13.5, 6.5, 13.5, 10.25)),
            detail(seg(17, 7.5, 17, 9)), detail(seg(6, 13, 18, 13))]


@icon("sports-broadcast", CAT, "Television showing a ball with a small live dot in the corner",
      tags=["live sport", "match", "game on tv", "football", "soccer", "live event", "sports channel"])
def _(S):
    return [shell(rect(2.5, 7.5, 19, 13.5, S.R)), line(poly([(8, 2.5), (12, 7.5), (16, 2.5)], r=S.r)),
            detail(circle(10, 14.5, 4)), sdot(poly(regular(10, 14.5, 1.7, 5), closed=True)), dot(18, 11.5, 1.25)]


@icon("video-rental-store", CAT, "Small shop front with a striped awning and a film strip sign above the door",
      tags=["movie rental", "dvd shop", "video shop", "retro store", "rent films", "cinema shop"])
def _(S):
    return [shell(poly([(2.5, 7.5), (4.5, 2.5), (19.5, 2.5), (21.5, 7.5)], closed=True, r=S.r * 0.5)),
            detail(seg(9.5, 2.5, 8.5, 7.5)), detail(seg(14.5, 2.5, 15.5, 7.5)),
            shell(rect(3.5, 7.5, 17, 13.5, S.R * 0.3)),
            sq(5.5, 10, 2, 2.5), sq(9, 10, 2, 2.5), sq(12.5, 10, 2, 2.5), sq(16, 10, 2, 2.5),
            detail(rect(9.5, 15.5, 5, 5.5, 0))]


@icon("play-selection", CAT, "Pair of square brackets enclosing a play triangle",
      tags=["play range", "loop region", "selected clip", "in and out points", "play section", "range", "bracket"])
def _(S):
    return [line(poly([(8, 4), (3.5, 4), (3.5, 20), (8, 20)], r=S.r)), line(poly([(16, 4), (20.5, 4), (20.5, 20), (16, 20)], r=S.r)),
            shell(tri(11.5, 12, 8, r=S.r * 0.5))]


@icon("karaoke-microphone", CAT, "Handheld microphone with a wide round speaker body and buttons on its handle",
      tags=["singing", "sing along", "party mic", "wireless mic", "singer", "karaoke machine", "microphone"])
def _(S):
    return [shell(circle(11.5, 8, 6)), detail(circle(11.5, 8, 2.5)),
            shell(poly([(9, 14.5), (14, 14.5), (13, 21.5), (10, 21.5)], closed=True, r=S.r * 0.5)),
            dot(11.5, 17, 0.8), dot(11.5, 19.5, 0.8), line(wave_arc(20, 8, 3, 1.25))]


@icon("drive-in-speaker", CAT, "Metal box speaker with a grille hooked over the top edge of a car window glass",
      tags=["drive in cinema", "car window speaker", "outdoor movie", "retro cinema", "window mount", "old speaker", "drive-in"])
def _(S):
    return [shell(rect(2.5, 9.5, 7.5, 11.5, S.R * 0.4)), detail(seg(4.75, 14, 7.75, 14)), detail(seg(4.75, 17.5, 7.75, 17.5)),
            line(poly([(6.25, 9.5), (6.25, 3.5), (19.5, 3.5), (19.5, 9.5)], r=S.r)),
            shell(rect(13.5, 6.5, 3, 14.5, S.R * 0.2))]


@icon("surtitles", CAT, "Theatre stage with open curtains and a long text bar above the stage opening",
      tags=["supertitles", "opera captions", "theatre subtitles", "stage text", "translation", "live captions", "playhouse"],
      filled=lambda: U(P(rect(3, 3, 18, 3, 0.5)),
                       D(P(rect(2, 8, 20, 14, 2)), P("M9.25 10.5C9.25 14.5 7 17 7 20H17C17 17 14.75 14.5 14.75 10.5Z"))))
def _(S):
    return [sq(3, 3, 18, 3, 0.5), shell(rect(3, 9, 18, 12, S.R * 0.4)),
            solid("M3 9H9C9 14 6.5 17 6.5 21H3Z"), solid("M21 9H15C15 14 17.5 17 17.5 21H21Z")]


@icon("score-overlay", CAT, "Video frame with a small two column score box in its top left corner",
      tags=["scoreboard", "sports graphic", "live score", "match overlay", "broadcast graphic", "scorebug", "hud"])
def _(S):
    return [shell(rect(2.5, 3.5, 19, 17, S.R)), sq(5.5, 6.5, 3.5, 4, 0.5), sq(10.5, 6.5, 3.5, 4, 0.5),
            sdot(tri(13, 15, 4))]


# =========================================================================== chunk 5

def tri_left(cx, cy, h):
    w = h * 0.85
    return poly([(cx + w / 3, cy - h / 2), (cx - 2 * w / 3, cy), (cx + w / 3, cy + h / 2)], closed=True)


def slice_tri(y0, y1, dx):
    """Part of the play triangle (8,6.5)-(16.5,12)-(8,17.5) between y0 and y1, shifted by dx."""
    k = 8.5 / 5.5

    def xr(y):
        return 8 + (y - 6.5) * k if y <= 12 else 16.5 - (y - 12) * k
    pts = [(8 + dx, y0), (xr(y0) + dx, y0), (xr(y1) + dx, y1), (8 + dx, y1)]
    if y0 < 12 < y1:
        pts.insert(2, (16.5 + dx, 12))
    return poly(pts, closed=True)


@icon("lock-screen-player", CAT, "Phone with a large clock bar on top and a media control row with play and skip below",
      tags=["now playing", "lock screen", "media widget", "phone music controls", "notification player", "smartphone", "controls"])
def _(S):
    return [shell(rect(4.5, 1.5, 15, 21, S.R)), sq(8, 5.5, 8, 3.5, 0.5),
            sdot(tri(12.4, 15.5, 4.5)), sdot(tri_left(7.6, 15.5, 3)), sdot(tri(16.4, 15.5, 3)), line(seg(7.5, 19.25, 16.5, 19.25))]


@icon("volume-mixer", CAT, "Three horizontal slider tracks, each with a small speaker on the left and a knob at a different position",
      tags=["app volume", "sound mixer", "per app volume", "audio levels", "sliders", "channels", "volume control"])
def _(S):
    parts = []
    for y, kx in ((5.5, 15), (12, 11.5), (18.5, 18)):
        parts.append(solid(poly([(2.5, y - 1), (4.25, y - 1), (6.5, y - 2.75), (6.5, y + 2.75), (4.25, y + 1), (2.5, y + 1)], closed=True)))
        parts.append(line(seg(9, y, 21.5, y)))
        parts.append(dot(kx, y, 2.25))
    return parts


@icon("next-episode", CAT, "Small thumbnail beside a countdown ring with a play triangle in it",
      tags=["up next", "autoplay", "binge", "series", "auto play countdown", "streaming", "skip to next"])
def _(S):
    return [shell(rect(2, 8, 7, 8, S.R * 0.3)), line(arc(17, 12, 4.75, -90, 210)), sdot(tri(17.3, 12, 4))]


@icon("audio-feedback", CAT, "Microphone and a loudspeaker with a jagged squeal line running between them",
      tags=["howl", "mic squeal", "feedback loop", "pa system", "screech", "larsen effect", "sound check"])
def _(S):
    return [shell(rect(2.5, 8.5, 5, 7.5, 2.5)), line(seg(5, 16, 5, 21)),
            shell(rect(14.5, 12.5, 7, 9, S.R * 0.4)), dot(18, 17, 1.5),
            line(poly([(5, 6), (6.5, 2.5), (8, 5), (9.5, 2.5), (11, 5), (12.5, 2.5), (14, 5), (15.5, 2.5), (18, 5), (18, 10)])),
            line(head(18, 10.5, 0, 1, 2))]


@icon("group-listening", CAT, "Two pairs of headphones side by side joined by a short link, a music note above",
      tags=["shared listening", "listen together", "friends", "duet", "sync music", "social audio", "share headphones"])
def _(S):
    parts = [shell(circle(10.25, 5.5, 1.75)), line(seg(12, 5.5, 12, 2)), line(pick(S, "M12 2L15 3.25", "M12 2C12.75 2.75 13.75 3 15 3.25")),
             line(seg(10.75, 17.5, 13.25, 17.5))]
    for cx in (6.25, 17.75):
        parts.append(line(f"M{fmt(cx - 3.5)} 14.5V13.5A3.5 3.5 0 0 1 {fmt(cx + 3.5)} 13.5V14.5"))
        parts.append(solid(rect(cx - 4.5, 14.5, 2, 6, 0.8)))
        parts.append(solid(rect(cx + 2.5, 14.5, 2, 6, 0.8)))
    return parts


@icon("thaumatrope", CAT, "Round disc on a short axis with twisted strings at both sides and a bird drawn on its face",
      tags=["optical toy", "persistence of vision", "victorian toy", "spinning card", "early animation", "illusion", "cage and bird"])
def _(S):
    bird = poly([(15.75, 11), (14.25, 10), (12.75, 10.75), (9, 9.25), (9.5, 11.75), (10.75, 12.5), (11.25, 14.25), (13.75, 13.75), (14.75, 12.5)], closed=True)
    return [shell(circle(12, 12, 5.75)), sdot(bird),
            line("M6.25 12L2.5 10"), line("M6.25 12L2.5 14"), line("M17.75 12L21.5 10"), line("M17.75 12L21.5 14")]


@icon("headphone-splitter", CAT, "Y shaped adapter with a jack plug at the base and two round sockets at the forked ends",
      tags=["audio splitter", "share audio", "aux splitter", "y cable", "3.5mm", "jack adapter", "two headphones"])
def _(S):
    return [solid(rect(10, 16, 4, 5.5, 0.8)), line(seg(12, 16, 12, 12)),
            line(poly([(6.25, 6.5), (12, 12), (17.75, 6.5)], r=S.r)),
            shell(circle(6, 4.75, 2.75)), shell(circle(18, 4.75, 2.75))]


@icon("timeline-snap", CAT, "Horseshoe magnet above the edge of a clip with a thin guide line where it snaps",
      tags=["magnetic timeline", "snapping", "snap to clip", "video editing", "align clips", "magnet", "guide"])
def _(S):
    return [line("M7 4V7.5A5 5 0 0 0 17 7.5V4"), solid(rect(5.75, 1.5, 2.5, 3.5, 0.3)), solid(rect(15.75, 1.5, 2.5, 3.5, 0.3)),
            line(seg(12, 14.5, 12, 21.75)),
            shell(rect(12, 16.5, 9.5, 5, S.R * 0.3)), shell(rect(2.5, 16.5, 5.5, 5, S.R * 0.3))]


@icon("tangled-tape", CAT, "Cassette with a loose loop of tape spilling out in tangled curls",
      tags=["cassette jam", "tape mess", "eaten tape", "broken cassette", "retro audio", "unspool", "magnetic tape"])
def _(S):
    return [shell(rect(2.5, 2.5, 15, 10, S.R)), detail(circle(7, 7.5, 1.6)), detail(circle(13, 7.5, 1.6)),
            line("M9.5 12.5C9.5 16.5 5 16 5 19.25C5 22 10.5 21.25 10.75 18.25C11 15.25 15.5 15.5 15.5 19C15.5 22 20.5 21.5 20.75 18.25C21 16 18.5 15 16.75 16.5")]


@icon("video-glitch", CAT, "Video frame with a play triangle whose horizontal slices are shifted sideways",
      tags=["glitch effect", "corrupted video", "digital error", "distortion", "vhs", "video artifact", "broken stream"])
def _(S):
    return [shell(rect(2.5, 3.5, 19, 17, S.R)),
            sdot(slice_tri(6.5, 9.5, -1.5)), sdot(slice_tri(10.5, 13.5, 1.5)), sdot(slice_tri(14.5, 17.5, -1))]


@icon("hdmi-switch", CAT, "Small box with three ports on the left, one on the right and an arrow across it",
      tags=["hdmi selector", "input switch", "av switch", "source selector", "tv inputs", "hdmi hub", "video switcher"])
def _(S):
    return [shell(rect(6.5, 3.5, 11, 17, S.R * 0.6)),
            sq(2, 5.5, 4, 3, 0.5), sq(2, 10.5, 4, 3, 0.5), sq(2, 15.5, 4, 3, 0.5), sq(18, 10.5, 4, 3, 0.5),
            detail(seg(9.5, 12, 14.5, 12)), detail(head(14.5, 12, 1, 0, 2))]


@icon("volume-buttons", CAT, "Edge of a phone with two raised buttons and a plus and minus sign beside them",
      tags=["volume up", "volume down", "phone buttons", "side buttons", "hardware keys", "rocker", "device"])
def _(S):
    return [shell(rect(15, 2.5, 6.5, 19, S.R * 0.6)), shell(rect(12.5, 6.5, 2.5, 5, S.R * 0.3)), shell(rect(12.5, 13.5, 2.5, 5, S.R * 0.3)),
            line(seg(3, 9, 9, 9)), line(seg(6, 6, 6, 12)), line(seg(3, 16, 9, 16))]


@icon("earbud-tap-control", CAT, "Single earbud seen from the side with a fingertip touching it and ripple arcs",
      tags=["touch controls", "tap earbud", "gesture", "wireless earbuds", "double tap", "touch sensor", "earphone controls"])
def _(S):
    return [shell(circle(7.5, 7.5, 3.75)), line(poly([(10.25, 10.25), (10.75, 14), (9.5, 19.5)], r=S.r)),
            shell(rect(15.5, 13, 4.5, 9, 2.25)), line(arc(17.75, 13, 4.25, -140, -40)), line(arc(17.75, 13, 7.5, -130, -50))]


@icon("inline-remote", CAT, "Earphone cable with a small oblong remote in the middle carrying three buttons",
      tags=["cable remote", "earphone controls", "in-line mic", "headset remote", "wired earbuds", "play pause button", "mic button"])
def _(S):
    return [line(seg(12, 2.5, 12, 6)), shell(rect(8, 6, 8, 12, S.R * 0.6)),
            dot(12, 9.5, 1.1), dot(12, 12, 1.1), dot(12, 14.5, 1.1), line(seg(12, 18, 12, 21.5))]
