"""TypeIcon Core: messaging, broadcast and media (batch 2)."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "messaging"


def rr(S, cap):
    return min(S.R, cap)


def sdot(S, x, y, r=1.25):
    """Small solid mark: square in Line, round in Rounded."""
    if S.name == "rounded":
        return dot(x, y, r)
    return Part("dot", rect(x - r, y - r, 2 * r, 2 * r))


def ahead(cx, cy, r, deg, size=2.0, cw=True, S=None):
    """Open arrowhead (chevron) at angle deg on a circle, pointing along the travel direction."""
    px, py = polar(cx, cy, r, deg)
    a = math.radians(deg)
    tx, ty = (-math.sin(a), math.cos(a)) if cw else (math.sin(a), -math.cos(a))
    nx, ny = math.cos(a), math.sin(a)
    b1 = (px - tx * size + nx * size, py - ty * size + ny * size)
    b2 = (px - tx * size - nx * size, py - ty * size - ny * size)
    return poly([b1, (px, py), b2], r=(S.r * 0.6 if S else 0))


# ============================================================================ chunk 1

@icon("screen-recording", CAT, "Monitor with a record dot inside a ring on its screen",
      tags=["record screen", "screen capture", "capture", "screencast", "monitor", "rec"])
def _(S):
    return [
        shell(rect(2, 3.5, 20, 13.5, rr(S, 2.5))),
        line(seg(12, 17, 12, 20.5)),
        line(seg(8, 20.5, 16, 20.5)),
        detail(circle(12, 10.25, 3.5)),
        sdot(S, 12, 10.25, 1.25),
    ]


@icon("flip-camera", CAT, "Camera body with two curved arrows circling its lens",
      tags=["switch camera", "selfie", "rotate camera", "front camera", "rear camera", "swap"])
def _(S):
    body = poly([(2, 8), (7, 8), (8.5, 5.5), (15.5, 5.5), (17, 8), (22, 8), (22, 21), (2, 21)], closed=True, r=S.r)
    return [
        shell(body),
        detail(arc(12, 14.5, 3.5, 200, 330)),
        detail(ahead(12, 14.5, 3.5, 330, 1.8, True, S)),
        detail(arc(12, 14.5, 3.5, 20, 150)),
        detail(ahead(12, 14.5, 3.5, 150, 1.8, True, S)),
    ]


@icon("virtual-background", CAT, "Person in front of a scenic backdrop with a mountain and sun",
      tags=["background blur", "video call", "backdrop", "meeting", "green screen", "scene"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, rr(S, 3))),
        detail(poly([(2, 15), (6.5, 9.5), (10, 14)], r=S.r * 0.5)),
        sdot(S, 18, 7.5, 1.25),
        detail(circle(13.5, 10.5, 2.5)),
        detail("M8.5 21a5 5 0 0 1 10 0"),
    ]


@icon("hybrid-meeting", CAT, "Wall screen with two faces above two people seated at a table",
      tags=["remote meeting", "conference", "video call", "office", "in person", "screen share"])
def _(S):
    return [
        shell(rect(5, 2, 14, 8, rr(S, 2))),
        sdot(S, 9.5, 6, 1.25),
        sdot(S, 14.5, 6, 1.25),
        shell(circle(7, 14.5, 2)),
        shell(circle(17, 14.5, 2)),
        line(poly([(2, 19), (22, 19)])),
        line(seg(5, 19, 5, 22)),
        line(seg(19, 19, 19, 22)),
    ]


@icon("video-bar", CAT, "Slim camera bar with a central lens resting on the top edge of a screen",
      tags=["conference camera", "webcam", "meeting room", "all in one", "speaker bar", "camera bar"])
def _(S):
    return [
        shell(rect(2, 10.5, 20, 8, rr(S, 2.5))),
        line(seg(12, 18.5, 12, 21.5)),
        line(seg(8, 21.5, 16, 21.5)),
        shell(rect(3, 3, 18, 5.5, rr(S, 2.5))),
        sdot(S, 12, 5.75, 1.0),
    ]


@icon("watch-party", CAT, "Two viewers side by side under a screen with a play triangle",
      tags=["watch together", "shared viewing", "group watch", "movie night", "stream together", "friends"])
def _(S):
    return [
        shell(rect(3, 2, 18, 9, rr(S, 2))),
        detail(poly([(10, 4), (10, 9), (15, 6.5)], closed=True, r=S.r * 0.4)),
        shell(circle(7, 14.5, 2)),
        shell(circle(17, 14.5, 2)),
        line(poly([(3.5, 22), (3.5, 21), (10.5, 21), (10.5, 22)])) if False else line("M3 22a4 4 0 0 1 8 0"),
        line("M13 22a4 4 0 0 1 8 0"),
    ]


@icon("camcorder", CAT, "Handheld video camera with a front lens barrel and a viewfinder",
      tags=["video camera", "handycam", "recorder", "filming", "home video", "camera"])
def _(S):
    body = poly([(2, 9), (14, 9), (14, 10.5), (22, 10.5), (22, 17), (14, 17), (14, 19), (2, 19)], closed=True, r=S.r)
    return [
        shell(body),
        line(poly([(4, 9), (4, 5), (9, 5), (9, 9)], r=S.r * 0.6)),
        detail(rect(5, 12, 6, 4, 1)) if S.name == "rounded" else detail(rect(5, 12, 6, 4)),
        detail(seg(18, 10.5, 18, 17)),
    ]


@icon("broadcast-camera", CAT, "Studio television camera with a hood and a viewfinder on a wheeled pedestal",
      tags=["tv camera", "studio", "television", "news", "production", "pedestal"])
def _(S):
    body = poly([(3, 5.5), (8, 8), (11, 8), (11, 3.5), (21, 3.5), (21, 13), (8, 13), (3, 15.5)], closed=True, r=S.r * 0.6)
    return [
        shell(body),
        detail(seg(8, 8, 8, 13)),
        line(seg(14, 13, 14, 17)),
        line(seg(5, 17.5, 21, 17.5)),
        sdot(S, 7, 21, 1.5),
        sdot(S, 19, 21, 1.5),
    ]


@icon("film-cartridge", CAT, "Small film canister with a spool knob and a tongue of film",
      tags=["film roll", "35mm", "analog", "photography", "canister", "negative"])
def _(S):
    return [
        shell(rect(5, 6.5, 12, 15, rr(S, 3))),
        detail(seg(5, 10, 17, 10)),
        detail(seg(5, 18, 17, 18)),
        line(seg(11, 2.5, 11, 6.5)),
        line(poly([(17, 13), (22, 13), (22, 16), (17, 16)], r=S.r * 0.4)),
    ]


@icon("video-timeline", CAT, "Two clip tracks with a vertical playhead line",
      tags=["video editor", "editing", "clips", "tracks", "playhead", "nle", "cut"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 7, 5, rr(S, 1.5))),
        shell(rect(15.5, 4.5, 6, 5, rr(S, 1.5))),
        shell(rect(2.5, 14.5, 4, 5, rr(S, 1.5))),
        shell(rect(15.5, 14.5, 6, 5, rr(S, 1.5))),
        line(seg(12.5, 2, 12.5, 22)),
    ]


@icon("screenplay", CAT, "Stack of script pages held by two round brass fasteners on the left",
      tags=["script", "screenwriting", "film script", "manuscript", "movie", "drama", "pages"])
def _(S):
    return [
        line(poly([(3, 6), (3, 21), (18, 21)], r=S.r * 0.6)),
        shell(rect(7, 2, 14, 16, rr(S, 2))),
        sdot(S, 10.5, 6, 1.25),
        sdot(S, 10.5, 14, 1.25),
        detail(seg(14, 7, 18, 7)),
        detail(seg(14, 11, 18, 11)),
    ]


@icon("color-grading", CAT, "Three colour wheels each with a small off-centre marker dot",
      tags=["colour grading", "color correction", "color wheels", "video editing", "grade", "lift gamma gain"])
def _(S):
    parts = []
    for cx, cy, ox, oy in ((7, 8, 0.9, -0.7), (17, 8, -0.8, 0.9), (12, 17, 0.6, 0.9)):
        parts.append(shell(circle(cx, cy, 3.5)))
        parts.append(sdot(S, cx + ox, cy + oy, 0.9))
    return parts


@icon("cue-card", CAT, "Large card with bold text lines held up by a hand",
      tags=["idiot board", "prompt card", "teleprompter", "script card", "speech", "television", "prompt"])
def _(S):
    return [
        shell(rect(3, 2, 18, 11.5, rr(S, 2))),
        detail(seg(7, 5.75, 17, 5.75)),
        detail(seg(7, 9.5, 14, 9.5)),
        shell(rect(7.5, 14.5, 9, 7, rr(S, 3))),
        detail(seg(10.5, 14.5, 10.5, 17.5)),
        detail(seg(13.5, 14.5, 13.5, 17.5)),
    ]


@icon("video-switcher", CAT, "Production switcher panel with rows of square buttons and a fader lever",
      tags=["vision mixer", "live production", "broadcast", "mixer", "t-bar", "switching", "studio"])
def _(S):
    parts = [shell(rect(2, 5, 20, 14, rr(S, 3)))]
    for x in (5, 10):
        for y in (8, 13):
            parts.append(Part("dot", rect(x, y, 3, 3)))
    parts.append(detail(seg(18, 8, 18, 16)))
    parts.append(Part("dot", rect(16.25, 11, 3.5, 2.5)) if False else sdot(S, 18, 12, 1.0))
    return parts


@icon("field-monitor", CAT, "Small monitor with a folding sunshade hood flaring around the screen",
      tags=["camera monitor", "on-camera monitor", "sun hood", "director monitor", "preview screen", "filming"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 14, rr(S, 2.5))),
        detail(rect(8, 7.5, 8, 6, rr(S, 1))),
        detail(seg(7.5, 7, 4.5, 4.5)),
        detail(seg(16.5, 7, 19.5, 4.5)),
        detail(seg(7.5, 14, 4.5, 16.5)),
        detail(seg(16.5, 14, 19.5, 16.5)),
        line(seg(12, 17.5, 12, 21)),
        line(seg(8, 21, 16, 21)),
    ]


@icon("film-projector", CAT, "Vintage movie projector with two film reels on top and a lens at the front",
      tags=["cinema", "reel to reel", "movie projector", "old movie", "8mm", "screening", "film reel"])
def _(S):
    return [
        shell(circle(6.5, 6.5, 3.5)),
        shell(circle(15.5, 6.5, 3.5)),
        sdot(S, 6.5, 6.5, 0.9),
        sdot(S, 15.5, 6.5, 0.9),
        shell(rect(2, 12.5, 15, 8.5, rr(S, 2))),
        line(poly([(17, 14), (21.5, 12.5), (21.5, 19), (17, 18)], r=S.r * 0.5)),
    ]


@icon("magic-lantern", CAT, "Old lantern-style projector with a chimney on top and a lens tube at the front",
      tags=["lantern slide", "slide projector", "antique", "projection", "victorian", "optical toy"])
def _(S):
    return [
        shell(rect(7, 9.5, 11, 10.5, rr(S, 2))),
        line(poly([(10, 9.5), (10, 4), (14.5, 4), (14.5, 9.5)], r=S.r * 0.6)),
        line(poly([(7, 12.5), (2.5, 12.5), (2.5, 17), (7, 17)], r=S.r * 0.6)),
        detail(circle(12.5, 14.75, 2.25)) if S.name == "rounded" else detail(rect(10.25, 12.5, 4.5, 4.5)),
        line(seg(9, 20, 9, 22)) if False else line(seg(21, 11, 21, 18)) if False else line(seg(9, 20, 9, 22)),
        line(seg(16, 20, 16, 22)),
    ]


@icon("box-office", CAT, "Ticket booth with an awning, a service window and a speaking hole",
      tags=["ticket booth", "ticket office", "cinema", "theatre", "kiosk", "tickets", "counter"])
def _(S):
    return [
        shell(poly([(2.5, 9), (5.5, 3.5), (18.5, 3.5), (21.5, 9)], closed=True, r=S.r * 0.6)),
        shell(rect(5, 9.5, 14, 11.5, rr(S, 1.5))),
        detail(rect(8, 12.5, 8, 4, rr(S, 1))),
        sdot(S, 12, 14.5, 0.8),
        detail(seg(8, 19, 16, 19)) if False else detail(seg(10, 19, 14, 19)),
    ]


@icon("video-cassette-recorder", CAT, "Low video recorder box with a wide tape slot and a clock display",
      tags=["vcr", "videotape", "vhs", "retro", "tape deck", "video player", "cassette"])
def _(S):
    return [
        shell(rect(2, 7, 20, 11, rr(S, 2.5))),
        Part("dot", rect(4.5, 10, 10, 2.5)),
        Part("dot", rect(17, 10, 2.5, 2.5)) if False else sdot(S, 17.5, 11.25, 1.25),
        detail(seg(5, 15.5, 11, 15.5)) if False else detail(seg(12, 15, 19, 15)),
        line(seg(5, 18, 5, 20.5)),
        line(seg(19, 18, 19, 20.5)),
    ]


@icon("microfiche", CAT, "Card with a cut corner, a header strip and a grid of tiny film frames",
      tags=["microform", "archive", "library", "records", "micro film", "reader", "document archive"])
def _(S):
    card = poly([(3, 3.5), (17, 3.5), (21, 7.5), (21, 20.5), (3, 20.5)], closed=True, r=S.r)
    return [
        shell(card),
        detail(seg(3, 9, 21, 9)),
        detail(seg(9, 9, 9, 20.5)),
        detail(seg(15, 9, 15, 20.5)),
        detail(seg(3, 14.75, 21, 14.75)),
    ]


@icon("tv-guide", CAT, "Schedule grid with a time bar on top and rows of programme blocks",
      tags=["tv listings", "program guide", "epg", "channel schedule", "television schedule", "what's on", "listings"])
def _(S):
    parts = [shell(rect(2, 3, 20, 18, rr(S, 2.5))), detail(seg(2, 7.5, 22, 7.5))]
    for x, y, w in ((5, 10, 6), (13, 10, 6), (5, 13.5, 3.5), (10.5, 13.5, 8.5), (5, 17, 8), (15.5, 17, 3.5)):
        parts.append(Part("dot", rect(x, y, w, 2)))
    return parts


@icon("slow-motion", CAT, "Play triangle followed by three shortening trail lines",
      tags=["slow mo", "slomo", "playback speed", "slow down", "video speed", "replay", "half speed"])
def _(S):
    return [
        shell(poly([(13, 5), (13, 19), (22, 12)], closed=True, r=S.r)),
        line(seg(9, 8, 9, 16)),
        line(seg(5.5, 10, 5.5, 14)),
        sdot(S, 2.75, 12, 0.9),
    ]


def _ell(cx, cy, rx, ry, deg):
    a = math.radians(deg)
    return cx + rx * math.cos(a), cy + ry * math.sin(a)


@icon("360-video", CAT, "Play triangle inside an elliptical ring with an arrowhead for a surround view",
      tags=["360", "panorama video", "immersive", "vr video", "spherical video", "surround", "360 degree"])
def _(S):
    cx, cy, rx, ry = 12, 12, 8.75, 6
    x1, y1 = _ell(cx, cy, rx, ry, 75)
    x2, y2 = _ell(cx, cy, rx, ry, 25)
    a = math.radians(25)
    tx, ty = -rx * math.sin(a), ry * math.cos(a)
    n = math.hypot(tx, ty)
    tx, ty = tx / n, ty / n
    nx, ny = -ty, tx
    h = 2.2
    head = [(x2 - tx * h + nx * h, y2 - ty * h + ny * h), (x2, y2), (x2 - tx * h - nx * h, y2 - ty * h - ny * h)]
    return [
        line(f"M{fmt(x1)} {fmt(y1)}A{rx} {ry} 0 1 1 {fmt(x2)} {fmt(y2)}"),
        line(poly(head, r=S.r * 0.6)),
        shell(poly([(10, 9), (10, 15), (15, 12)], closed=True, r=S.r * 0.5)),
    ]


@icon("hd-video", CAT, "Rounded rectangle containing the letters HD",
      tags=["high definition", "hd", "720p", "1080p", "video quality", "resolution", "hi-def"])
def _(S):
    return [
        shell(rect(1.5, 4.5, 21, 15, rr(S, 3))),
        detail(seg(5.5, 8.75, 5.5, 15.25)),
        detail(seg(9.5, 8.75, 9.5, 15.25)),
        detail(seg(5.5, 12, 9.5, 12)),
        detail(seg(13.5, 8.75, 13.5, 15.25)),
        detail("M13.5 8.75h1.5a3.25 3.25 0 0 1 0 6.5h-1.5"),
    ]


@icon("4k-resolution", CAT, "Rounded rectangle containing the characters 4K",
      tags=["4k", "uhd", "ultra hd", "2160p", "video quality", "high resolution", "resolution"])
def _(S):
    return [
        shell(rect(1.5, 4.5, 21, 15, rr(S, 3))),
        detail(poly([(9.5, 8.5), (5, 13.5), (11, 13.5)], r=S.r * 0.3)),
        detail(seg(9.5, 8.5, 9.5, 16)),
        detail(seg(14.5, 8.5, 14.5, 15.5)),
        detail(poly([(19.5, 8.5), (14.5, 12), (19.5, 15.5)], r=S.r * 0.3)),
    ]


@icon("test-card", CAT, "Screen showing a circle drawn over vertical bars",
      tags=["test pattern", "colour bars", "color bars", "tv test", "calibration", "no signal", "broadcast"])
def _(S):
    return [
        shell(rect(2, 4, 20, 16, rr(S, 2.5))),
        detail(seg(6, 4, 6, 20)),
        detail(seg(18, 4, 18, 20)),
        detail(circle(12, 12, 3)),
        sdot(S, 12, 12, 0.9),
    ]


@icon("static-noise", CAT, "Television screen with antenna ears filled with scattered dots",
      tags=["tv static", "white noise", "snow", "no signal", "interference", "glitch", "television"])
def _(S):
    parts = [shell(rect(2, 8, 20, 13, rr(S, 2.5))), line(seg(12, 8, 8, 3.5)), line(seg(12, 8, 16, 3.5))]
    for x, y in ((6, 12), (11, 11.5), (17, 12), (8.5, 15.5), (14.5, 15.5), (19, 16.5), (5.5, 18), (11.5, 18.5)):
        parts.append(sdot(S, x, y, 0.85))
    return parts


@icon("news-desk", CAT, "Newsreader seated behind a curved desk with a screen on the wall behind",
      tags=["anchor desk", "newsroom", "television news", "presenter", "studio", "broadcast", "anchor"])
def _(S):
    return [
        shell(rect(14.5, 2.5, 7.5, 6.5, rr(S, 1.5))),
        shell(circle(8.5, 6.5, 2)),
        line("M4.5 15.5a4 4 0 0 1 8 0"),
        shell("M2.5 15.5H21.5V19Q12 23.5 2.5 19Z"),
    ]


@icon("voice-over", CAT, "Microphone beside a video frame with a play triangle, for narration recorded over video",
      tags=["narration", "dubbing", "voiceover", "audio recording", "commentary", "microphone", "film"])
def _(S):
    return [
        shell(rect(4, 2.5, 5, 8.5, 2.5)),
        line("M2 9.5a4.5 4.5 0 0 0 9 0"),
        line(seg(6.5, 14, 6.5, 21)),
        line(seg(3.5, 21, 9.5, 21)),
        shell(rect(14, 6, 8, 12, rr(S, 2))),
        detail(poly([(16.5, 9.5), (16.5, 14.5), (20, 12)], closed=True, r=S.r * 0.4)),
    ]


@icon("transcript", CAT, "Document with lines of text, each starting with a small speaker marker",
      tags=["speaker labels", "captions", "text of speech", "dialogue", "interview transcript", "minutes", "notes"])
def _(S):
    parts = [shell(rect(4, 2, 16, 20, rr(S, 2.5)))]
    for y in (7, 12, 17):
        parts.append(sdot(S, 8.5, y, 1.25))
        parts.append(detail(seg(12, y, 16, y)))
    return parts


@icon("ham-radio", CAT, "Amateur radio transceiver with a tuning knob, display and a hand microphone on a cord",
      tags=["amateur radio", "transceiver", "cb radio", "shortwave", "two way radio", "walkie", "radio operator"])
def _(S):
    return [
        shell(rect(2, 10, 13, 11, rr(S, 2.5))),
        detail(circle(6.5, 15.5, 2.25)),
        sdot(S, 11.5, 13, 0.9) if False else Part("dot", rect(10, 12.5, 3, 1.75)),
        line(seg(5, 10, 5, 3.5)),
        shell(rect(18, 2.5, 4, 8, rr(S, 2))),
        line(poly([(20, 10.5), (20, 13.5), (18, 14.5), (20, 15.5), (18, 16.5), (15, 17.5)], r=S.r * 0.4)),
    ]


@icon("radio-tuner-dial", CAT, "Radio tuning window with frequency tick marks and a pointer rising above it",
      tags=["frequency dial", "tuner", "fm am", "tuning", "radio scale", "analog radio", "frequency"])
def _(S):
    return [
        shell(rect(2, 7.5, 20, 13, rr(S, 3))),
        detail(seg(5, 13.5, 5, 17)),
        detail(seg(8.25, 13.5, 8.25, 17)),
        detail(seg(16, 13.5, 16, 17)),
        detail(seg(19.25, 13.5, 19.25, 17)),
        line(seg(12, 3, 12, 7.5)),
        detail(seg(12, 8.5, 12, 17)),
    ]


@icon("signal-booster", CAT, "Small box with two upright antennas and signal arcs between them",
      tags=["repeater", "range extender", "cell booster", "amplifier", "reception", "wifi extender", "signal"])
def _(S):
    return [
        shell(rect(3, 14, 18, 7, rr(S, 2))),
        line(seg(5.5, 14, 5.5, 6)),
        line(seg(18.5, 14, 18.5, 6)),
        line(f"M9.4 10.4a3.5 3.5 0 0 1 5.2 0"),
        line(f"M8.6 6.6a6 6 0 0 1 6.8 0") if False else line("M8.3 7.7a6 6 0 0 1 7.4 0"),
        sdot(S, 12, 17.5, 1.0),
    ]


@icon("cell-tower", CAT, "Tall lattice mast with panel antennas mounted near the top",
      tags=["mobile mast", "phone tower", "cellular", "base station", "network tower", "coverage", "telecom"])
def _(S):
    return [
        line(poly([(6.5, 21.5), (12, 4.5), (17.5, 21.5)]), stroke_miterlimit="1.5"),
        line(seg(8.5, 15, 15.5, 15)),
        line(seg(7.5, 19, 16.5, 19)),
        shell(rect(3.5, 5, 3, 6, rr(S, 1))),
        shell(rect(17.5, 5, 3, 6, rr(S, 1))),
    ]


@icon("mobile-hotspot", CAT, "Smartphone sending out wifi arcs from its top edge",
      tags=["tethering", "personal hotspot", "share internet", "wifi sharing", "portable wifi", "phone wifi", "internet sharing"])
def _(S):
    return [
        shell(rect(7, 12, 10, 10, rr(S, 2))),
        detail(seg(10.5, 18.5, 13.5, 18.5)),
        sdot(S, 12, 8.75, 1.25),
        line("M9.6 6a3.5 3.5 0 0 1 4.8 0") if False else line(arc(12, 8.75, 3.25, 228, 312)),
        line(arc(12, 8.75, 6.5, 228, 312)),
    ]


@icon("airplane-mode", CAT, "Small airplane silhouette inside a rounded square",
      tags=["flight mode", "aeroplane mode", "offline", "wireless off", "travel", "in flight", "disable radios"])
def _(S):
    plane = poly([(12, 5), (13.3, 8), (13.3, 10.5), (19, 14), (19, 15.6), (13.3, 13.8), (13.3, 17.2), (15.5, 18.6), (15.5, 19.5),
                  (12, 18.6), (8.5, 19.5), (8.5, 18.6), (10.7, 17.2), (10.7, 13.8), (5, 15.6), (5, 14), (10.7, 10.5), (10.7, 8)],
                 closed=True, r=0.0 if S.name == "line" else 0.7)
    return [
        shell(rect(2, 2, 20, 20, rr(S, 5) if S.name == "rounded" else 2)),
        Part("dot", plane),
    ]


@icon("submarine-cable", CAT, "Cable cross-section with a ring of strands around a central core",
      tags=["undersea cable", "fibre optic cable", "fiber optic", "internet cable", "transoceanic", "cable layers", "subsea"])
def _(S):
    parts = [shell(circle(12, 12, 9)), sdot(S, 12, 12, 1.75)]
    for k in range(6):
        x, y = polar(12, 12, 5.2, -90 + 60 * k)
        parts.append(sdot(S, x, y, 1.1))
    return parts


# ============================================================================ chunk 4: lines, relays and signals

@icon("telephone-pole", CAT, "Utility pole with a crossarm, insulators and drooping wires",
      tags=["utility pole", "power pole", "phone line", "telegraph pole", "overhead wires", "cable", "lineman"])
def _(S):
    return [
        line(seg(12, 3.5, 12, 22)),
        line(seg(4.5, 8, 19.5, 8)),
        sdot(S, 6, 4.75, 1.0),
        sdot(S, 18, 4.75, 1.0),
        line("M3 8.5Q2 13 2.5 17"),
        line("M21 8.5Q22 13 21.5 17"),
    ]


@icon("microwave-relay-tower", CAT, "Lattice tower with two bowl dish antennas pointing in opposite directions",
      tags=["microwave link", "relay station", "point to point", "backhaul", "radio link", "dish tower", "telecom"])
def _(S):
    return [
        line(poly([(7.5, 21.5), (12, 4.5), (16.5, 21.5)]), stroke_miterlimit="1.5"),
        line(seg(8.5, 17.5, 15.5, 17.5)),
        shell("M4.5 5Q11 9.75 4.5 14.5Z"),
        shell("M19.5 5Q13 9.75 19.5 14.5Z"),
    ]


@icon("satellite-uplink", CAT, "Ground dish aimed upward with a dotted beam reaching a small satellite",
      tags=["uplink", "ground station", "earth station", "transmit", "space link", "satcom", "dish antenna"])
def _(S):
    return [
        shell(arc(8, 16, 7, 45, 225) + "Z"),
        line(seg(8, 16, 12, 12)),
        sdot(S, 14, 10, 0.9),
        sdot(S, 16, 8, 0.9),
        shell(rect(17.5, 2.5, 4, 4, rr(S, 1))),
    ]


@icon("signal-interference", CAT, "Signal bars with a jagged zigzag line cutting through",
      tags=["jamming", "weak signal", "noisy signal", "bad reception", "network interference", "disruption", "static"])
def _(S):
    return [
        line(seg(4, 20, 4, 15)),
        line(seg(8.5, 20, 8.5, 11)),
        line(seg(13, 20, 13, 7)),
        line(poly([(21, 3), (16.5, 10.5), (21, 13), (16.5, 21)], r=S.r * 0.4)),
    ]


@icon("telegraph-key", CAT, "Morse key with a flat base, a pivoting lever and a round finger knob",
      tags=["morse code", "morse key", "telegraph", "wireless key", "straight key", "dot dash", "cw"])
def _(S):
    return [
        shell(rect(2, 17.5, 20, 4, rr(S, 1.5))),
        line(seg(4.5, 14, 19.5, 14)),
        line(seg(15, 14, 15, 17.5)),
        line(seg(7.5, 11, 7.5, 14)),
        shell(circle(7.5, 8, 3)),
    ]


@icon("ticker-tape-machine", CAT, "Glass dome on a small stand with a paper tape curling out of it",
      tags=["stock ticker", "ticker tape", "paper tape", "stock exchange", "telegraph printer", "vintage finance", "dome"])
def _(S):
    return [
        shell("M3.5 15a8.5 8.5 0 0 1 17 0Z"),
        detail(circle(12, 11.25, 2.25)),
        line(seg(12, 15, 12, 21)),
        line(seg(7, 21, 17, 21)),
        line("M20.5 15.5c2 .5 2 4.5 0 5H16"),
    ]


@icon("teletype", CAT, "Boxy teleprinter with a paper sheet feeding out of the top and a keyboard at the front",
      tags=["teleprinter", "teletypewriter", "telex", "tty", "old terminal", "printer", "vintage"])
def _(S):
    return [
        line(poly([(8.5, 9), (8.5, 2.5), (15.5, 2.5), (15.5, 9)], r=S.r * 0.5)),
        shell(rect(2, 9, 20, 7, rr(S, 2))),
        detail(seg(6, 12.5, 14, 12.5)),
        shell(rect(4, 17.5, 16, 4, rr(S, 1.5))),
    ]


@icon("speaking-tube", CAT, "Curved voice pipe with a hinged whistle cap and a flared bell mouth",
      tags=["voice pipe", "ship communication", "bridge tube", "whistle", "intercom", "old speaking horn", "voice tube"])
def _(S):
    return [
        shell(rect(3, 1.75, 4, 3, rr(S, 1))),
        line("M5 4.75V12a6 6 0 0 0 6 6h3"),
        shell(poly([(14, 14.5), (21.5, 10.5), (21.5, 21.5), (14, 17.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("signal-fire", CAT, "Tall flame rising above crossed logs",
      tags=["beacon", "bonfire", "smoke signal fire", "warning fire", "lookout", "flame", "fire signal"])
def _(S):
    return [
        shell("M12 2.5C13 5 16.5 6.5 16.5 10.25a4.5 4.5 0 0 1-9 0C7.5 8 9 6.5 10 5.5c.4 1.5 1 2 1.6 2 .8-1.4.8-3.2.4-5Z"),
        line(seg(4.5, 17, 19.5, 21.5)),
        line(seg(19.5, 17, 4.5, 21.5)),
    ]


@icon("heliograph", CAT, "Round signalling mirror on a tripod with a sighting rod beside it",
      tags=["signal mirror", "sun telegraph", "mirror signal", "flash signal", "morse mirror", "survey", "tripod mirror"])
def _(S):
    return [
        shell(circle(8.5, 8, 5)),
        line(seg(8.5, 13, 8.5, 15.5)),
        line(poly([(4, 22), (8.5, 15.5), (13, 22)], r=S.r * 0.5)),
        line(poly([(15, 8), (21, 8)])),
        line(seg(21, 5.5, 21, 10.5)),
    ]


@icon("signal-lamp", CAT, "Round lamp with horizontal shutter slats across its lens and a carrying handle",
      tags=["aldis lamp", "morse lamp", "shutter lamp", "signalling light", "ship lamp", "naval", "flash lamp"])
def _(S):
    return [
        shell(circle(12, 14, 8)),
        detail(seg(4.5, 11, 19.5, 11)),
        detail(seg(4, 14, 20, 14)),
        detail(seg(4.5, 17, 19.5, 17)),
        line(poly([(8.5, 7), (8.5, 2.5), (15.5, 2.5), (15.5, 7)], r=S.r * 0.6)),
    ]


@icon("semaphore-telegraph", CAT, "Tall post with a crossbeam and two pivoting arms, an optical telegraph",
      tags=["chappe telegraph", "optical telegraph", "signal tower", "semaphore tower", "visual signalling", "history", "mast"])
def _(S):
    return [
        line(seg(12, 8, 12, 22)),
        line(seg(6, 8, 18, 8)),
        line(seg(6, 8, 3, 3)),
        line(seg(18, 8, 21, 13)),
        line(seg(8.5, 22, 15.5, 22)),
    ]


@icon("alarm-bell", CAT, "Flared bell with a clapper below and ring marks at its sides",
      tags=["fire bell", "warning bell", "school bell", "alert", "siren", "emergency", "ringing"])
def _(S):
    return [
        shell("M3.5 18c2.5-1.5 3-4.5 3-7.5a5.5 5.5 0 0 1 11 0c0 3 .5 6 3 7.5Z"),
        sdot(S, 12, 21, 1.25),
        line(seg(12, 2.5, 12, 4.75)),
        line(seg(3.5, 6, 1.5, 4)) if False else line(seg(3, 7, 2, 4.5)) if False else line(seg(3.5, 6.5, 2.5, 4.5)),
        line(seg(20.5, 6.5, 21.5, 4.5)),
    ]


@icon("fire-alarm-pull", CAT, "Wall box with a flame symbol above a downward pull handle",
      tags=["pull station", "manual call point", "fire alarm", "emergency", "break glass", "alarm box", "evacuation"])
def _(S):
    return [
        shell(rect(4.5, 2, 15, 20, rr(S, 3))),
        detail("M12 4.5C10.4 6.3 9.25 7.2 9.25 8.7a2.75 2.75 0 0 0 5.5 0C14.75 7.2 13.6 6.3 12 4.5Z"),
        detail(seg(4.5, 12.5, 19.5, 12.5)),
        detail(rect(8, 15, 8, 4, rr(S, 1.5))),
    ]


@icon("buzzer-button", CAT, "Square buzzer box with a large round push pad and a cable trailing away",
      tags=["quiz buzzer", "game show buzzer", "push button", "answer button", "doorbell", "press", "contestant"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 15, rr(S, 3))),
        detail(circle(12, 10, 4.5)),
        line("M12 17.5V19a2.5 2.5 0 0 0 2.5 2.5H20"),
    ]


@icon("cipher-disk", CAT, "Two concentric lettered rings divided into cells with a centre pin",
      tags=["cipher wheel", "secret code", "decoder ring", "cryptography", "enigma", "encryption", "code wheel"])
def _(S):
    parts = [shell(circle(12, 12, 9.5)), detail(circle(12, 12, 4.5))]
    for k in range(12):
        a = math.radians(k * 30 + 15)
        parts.append(detail(seg(12 + 4.5 * math.cos(a), 12 + 4.5 * math.sin(a), 12 + 9.5 * math.cos(a), 12 + 9.5 * math.sin(a))))
    parts.append(sdot(S, 12, 12, 1.25))
    return parts


# ============================================================================ chunk 5: devices and press

@icon("app-badge-count", CAT, "Rounded app tile with a small circular badge at its top-right corner",
      tags=["notification badge", "unread count", "app icon badge", "notification count", "alert bubble", "red dot", "home screen"])
def _(S):
    r = 5 if S.name == "rounded" else 2.5
    d = (f"M12.5 7.5H{fmt(3 + r)}a{r} {r} 0 0 0-{r} {r}v{fmt(14 - 2 * r)}a{r} {r} 0 0 0 {r} {r}h{fmt(15 - 2 * r)}"
         f"a{r} {r} 0 0 0 {r}-{r}V12")
    return [
        line(d),
        shell(circle(18, 6, 3.5)),
        sdot(S, 18, 6, 1.0),
    ]


@icon("ringtone", CAT, "Smartphone with a music note beside it",
      tags=["phone sound", "call tone", "ring sound", "notification sound", "music note", "custom ringtone", "alert tone"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 10, 19, rr(S, 2.5))),
        detail(seg(6, 18, 9, 18)),
        line(seg(19.5, 16, 19.5, 4.5)),
        line(poly([(19.5, 4.5), (22, 7.5)], r=0)),
        shell(circle(17, 17, 2.25)) if False else Part("dot", ellipse(17.25, 17, 2.75, 2.25)),
    ]


@icon("digital-signage", CAT, "Tall vertical screen on a floor stand showing a picture block and a line of text",
      tags=["display board", "kiosk screen", "advertising display", "information screen", "menu board", "totem", "digital display"])
def _(S):
    return [
        shell(rect(5.5, 1.75, 13, 16.5, rr(S, 2.5))),
        Part("dot", rect(8, 4.5, 8, 5)),
        detail(seg(8.5, 13.5, 15.5, 13.5)),
        line(seg(12, 18.25, 12, 21.5)),
        line(seg(8, 21.5, 16, 21.5)),
    ]


@icon("press-camera", CAT, "Vintage press camera with a viewfinder on top and a round flash reflector at the side",
      tags=["photojournalist", "newspaper photographer", "flashbulb", "vintage camera", "reporter camera", "flash", "photography"])
def _(S):
    return [
        shell(rect(2, 11, 15, 10, rr(S, 2))),
        detail(circle(9.5, 16, 2.75)),
        line(poly([(4.5, 11), (4.5, 8), (9, 8), (9, 11)], r=S.r * 0.6)),
        shell(circle(18.5, 6.5, 3.5)),
        sdot(S, 18.5, 6.5, 1.0),
        line(seg(18.5, 10, 18.5, 14.5)),
    ]


@icon("press-hat", CAT, "Brimmed hat with a card tucked into its band",
      tags=["fedora", "reporter", "journalist", "trilby", "old time reporter", "press card", "headwear"])
def _(S):
    return [
        shell(ellipse(12, 16.5, 10, 3.5)),
        shell("M6.5 15.5L7 9.5Q12 5 17 9.5L17.5 15.5"),
        detail(seg(6.8, 13, 17.2, 13)),
        Part("dot", rect(13.5, 8.75, 3, 3.25)),
    ]


@icon("rolled-newspaper", CAT, "Newspaper rolled into a tube with two bands around it",
      tags=["delivery", "morning paper", "paperboy", "daily paper", "newsprint", "rolled paper", "press"])
def _(S):
    return [
        shell(rect(2.5, 6.5, 19, 11, rr(S, 4))),
        detail("M7.5 9a2.5 3 0 0 0 0 6"),
        detail(seg(12.5, 6.5, 12.5, 17.5)),
        detail(seg(16.5, 6.5, 16.5, 17.5)),
    ]


@icon("digital-newspaper", CAT, "Tablet showing a newspaper page with a headline bar and columns",
      tags=["e-paper", "online news", "news app", "e-newspaper", "digital edition", "news reader", "tablet news"])
def _(S):
    return [
        shell(rect(3, 2, 18, 20, rr(S, 3))),
        Part("dot", rect(6, 5, 12, 2)),
        detail(seg(6, 11, 10, 11)),
        detail(seg(6, 14.75, 10, 14.75)),
        detail(seg(6, 18.5, 10, 18.5)),
        Part("dot", rect(13, 10, 5, 4)),
        detail(seg(13, 18.5, 18, 18.5)),
    ]


@icon("newspaper-clipping", CAT, "Torn-out article with a jagged top edge, a headline, a picture block and text",
      tags=["cutting", "press cutting", "article", "clip", "news story", "scrapbook", "excerpt"])
def _(S):
    clip = poly([(5, 4.5), (7.5, 2.5), (10, 4.5), (12.5, 2.5), (15, 4.5), (17.5, 2.5), (19, 4), (19, 21.5), (5, 21.5)],
                closed=True, r=S.r * 0.4)
    return [
        shell(clip),
        detail(seg(8.5, 8.5, 15.5, 8.5)),
        Part("dot", rect(8.5, 11.5, 4, 3.5)),
        detail(seg(15, 12.5, 15.5, 12.5)) if False else detail(seg(8.5, 18.5, 15.5, 18.5)),
    ]


@icon("breaking-news", CAT, "Television banner with a lightning bolt at its left end and text lines",
      tags=["news flash", "live news", "urgent news", "headline", "lower third", "news alert", "bulletin"])
def _(S):
    bolt = poly([(7.5, 8), (4.5, 12.5), (6.5, 12.5), (5.5, 16), (8.5, 11), (6.5, 11)], closed=True)
    return [
        shell(rect(2, 6, 20, 12, rr(S, 2.5))),
        Part("dot", bolt),
        detail(seg(10.5, 6, 10.5, 18)),
        detail(seg(13, 10.25, 19, 10.25)),
        detail(seg(13, 13.75, 17, 13.75)),
    ]


@icon("news-ticker", CAT, "Long strip with scrolling text blocks and a small arrow at its right end",
      tags=["scrolling headlines", "crawl", "news crawl", "stock ticker", "marquee", "headline strip", "lower thirds"])
def _(S):
    return [
        shell(rect(2, 7.5, 20, 9, rr(S, 2.5))),
        Part("dot", rect(5, 11, 4, 2)),
        Part("dot", rect(10.5, 11, 3, 2)),
        detail(poly([(17, 10), (19.25, 12), (17, 14)], r=S.r * 0.3)),
    ]


@icon("press-pass", CAT, "Badge on a lanyard with a photo circle and a heavy title bar",
      tags=["media badge", "press badge", "accreditation", "journalist pass", "lanyard", "credentials", "reporter id"])
def _(S):
    return [
        line(poly([(9.5, 1.75), (12, 8)], r=0)),
        line(poly([(14.5, 1.75), (12, 8)], r=0)),
        shell(rect(5.5, 8, 13, 14, rr(S, 2.5))),
        detail(seg(10.5, 11, 13.5, 11)),
        Part("dot", rect(8.5, 14, 7, 2)),
        sdot(S, 12, 19, 0.7) if False else detail(seg(8.5, 19, 12.5, 19)) if False else Part("dot", rect(8.5, 18, 4, 1.5)),
    ]


@icon("press-conference", CAT, "Podium with a cluster of microphones on its top edge",
      tags=["media briefing", "lectern", "announcement", "statement", "news conference", "speech", "microphones"])
def _(S):
    parts = [shell(poly([(5.5, 21.5), (7, 11.5), (17, 11.5), (18.5, 21.5)], closed=True, r=S.r * 0.6))]
    for hx, hy, bx in ((7.5, 6.5, 9.5), (12, 4, 12), (16.5, 6.5, 14.5)):
        parts.append(sdot(S, hx, hy, 1.5))
        parts.append(line(seg(hx, hy + 1.5, bx, 11.5)))
    return parts


@icon("interview-microphone", CAT, "Handheld reporter microphone with a square station cube around its neck",
      tags=["reporter microphone", "news microphone", "tv mic", "vox pop", "street interview", "press", "broadcast mic"])
def _(S):
    return [
        shell(circle(12, 5.5, 3.5)),
        line(seg(12, 9, 12, 12)),
        shell(rect(7.5, 12, 9, 7, rr(S, 1.5))),
        line(seg(12, 19, 12, 22)),
    ]


@icon("reporter-notebook", CAT, "Tall narrow spiral pad bound at the top with lines of notes",
      tags=["steno pad", "notepad", "journalist notes", "notes", "spiral notebook", "shorthand", "memo pad"])
def _(S):
    return [
        shell(rect(5.5, 4, 13, 18, rr(S, 2))),
        line(seg(8.5, 1.75, 8.5, 5.5)),
        line(seg(12, 1.75, 12, 5.5)),
        line(seg(15.5, 1.75, 15.5, 5.5)),
        detail(seg(8.5, 11, 15.5, 11)),
        detail(seg(8.5, 15, 15.5, 15)),
        detail(seg(8.5, 19, 12.5, 19)) if False else detail(seg(8.5, 19, 15.5, 19)) if False else detail(seg(8.5, 18.5, 12.5, 18.5)),
    ]


@icon("classified-ads", CAT, "Newspaper page divided into many small boxed ad blocks in columns",
      tags=["small ads", "want ads", "listings", "classifieds", "newspaper ads", "notices", "personals"])
def _(S):
    return [
        shell(rect(3, 2, 18, 20, rr(S, 4))),
        detail(seg(12, 2, 12, 22)),
        detail(seg(3, 9.5, 12, 9.5)),
        detail(seg(3, 16, 12, 16)),
        detail(seg(12, 7, 21, 7)),
        detail(seg(12, 13, 21, 13)),
        detail(seg(12, 18, 21, 18)),
        Part("dot", rect(5.5, 4.75, 4, 2)),
        Part("dot", rect(14.5, 9.25, 4, 2)),
        Part("dot", rect(5.5, 18, 4, 2)),
    ]


def _star(cx, cy, ro, ri, n=5):
    pts = []
    for k in range(2 * n):
        r = ro if k % 2 == 0 else ri
        a = math.radians(-90 + k * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


@icon("zine", CAT, "Small stapled booklet with a hand-drawn star on its cover",
      tags=["booklet", "diy magazine", "fanzine", "pamphlet", "self published", "chapbook", "small press"])
def _(S):
    return [
        shell(rect(4.5, 2, 15, 20, rr(S, 2))),
        sdot(S, 7.5, 6, 0.9),
        sdot(S, 7.5, 18, 0.9),
        Part("dot", poly(_star(13.25, 12, 4, 1.8), closed=True)),
    ]


@icon("tear-off-flyer", CAT, "Sheet pinned at the top with a row of vertical tear-off tabs along its bottom edge",
      tags=["notice board flyer", "tear off tabs", "pull tab poster", "lost and found", "advert", "community notice", "poster"])
def _(S):
    return [
        shell(rect(4, 2, 16, 20, rr(S, 2))),
        sdot(S, 12, 5.5, 1.0),
        detail(seg(8, 9.5, 16, 9.5)),
        detail(seg(4, 15, 20, 15)),
        detail(seg(8, 15, 8, 22)),
        detail(seg(12, 15, 12, 22)),
        detail(seg(16, 15, 16, 22)),
    ]


@icon("protest-sign", CAT, "Rectangular placard on a wooden stick with bold lines of text",
      tags=["picket", "demonstration", "placard", "rally", "march", "activism", "banner sign"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 12, rr(S, 2))),
        detail(seg(6.5, 6.5, 17.5, 6.5)),
        detail(seg(6.5, 10.5, 14, 10.5)),
        line(seg(12, 14.5, 12, 22)),
    ]


# ============================================================================ chunk 6: aircraft and web

def _plane_top(cx, cy, k=1.0):
    """Small aeroplane seen from above, pointing right."""
    pts = [(22, 0), (17, -2), (14, -8), (11, -8), (12.5, -2), (7, -2), (5.5, -4.5), (3.5, -4.5), (4.5, 0),
           (3.5, 4.5), (5.5, 4.5), (7, 2), (12.5, 2), (11, 8), (14, 8), (17, 2)]
    return [(cx + (x - 12) * k, cy + y * k) for x, y in pts]


@icon("skywriting", CAT, "Small plane trailing a looping smoke line behind it",
      tags=["sky message", "smoke trail", "aerial advertising", "stunt plane", "airshow", "loop", "vapour trail"])
def _(S):
    return [
        Part("dot", poly(_plane_top(17.5, 7, 0.55), closed=True)),
        line("M13 7.5H8.5C4.5 7.5 3 11 5 13.5S10 14 9.5 11 4 8.5 2.5 12.5s.5 7 4 7.5"),
    ]


@icon("aerial-banner", CAT, "Small plane towing a long rectangular banner on a line",
      tags=["banner plane", "towed banner", "beach advert", "aerial advertising", "sky banner", "promotion", "tow line"])
def _(S):
    return [
        Part("dot", poly(_plane_top(17.5, 6.5, 0.55), closed=True)),
        line(poly([(13.5, 7), (10, 11.5)])),
        shell("M2.5 12.5Q5.5 10.5 8.5 12.5T14.5 12.5V19.5Q11.5 21.5 8.5 19.5T2.5 19.5Z") if False else shell("M2.5 12.5Q5.5 11 8.5 12.5T14.5 12.5V19Q11.5 20.5 8.5 19T2.5 19Z"),
    ]


@icon("blog-post", CAT, "Browser window with a heading bar and text lines, a pen nib overlapping the corner",
      tags=["article", "web post", "writing", "blogging", "cms", "publish", "web page"])
def _(S):
    nib = poly([(14, 22), (14.6, 17.5), (19.5, 12.5), (22, 15), (17, 20)], closed=True, r=S.r * 0.3)
    return [
        line(poly([(12.5, 17.5), (2, 17.5), (2, 3), (18, 3), (18, 11)], r=S.r)),
        detail(seg(2, 7.5, 18, 7.5)),
        detail(seg(5, 11.5, 12, 11.5)),
        detail(seg(5, 15, 9, 15)),
        shell(nib),
    ]
