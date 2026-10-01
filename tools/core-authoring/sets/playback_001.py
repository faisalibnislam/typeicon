"""TypeIcon Core: playback (batch 001) - player controls, audio effects, broadcast and editing marks."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar

CAT = "playback"


def pick(S, a, b):
    """Line value, Rounded value."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def sdot(S, x, y, r=1.25):
    """Small solid dot: square in Line, round in Rounded."""
    if S.name == "rounded":
        return dot(x, y, r)
    return Part("dot", rect(x - r, y - r, 2 * r, 2 * r))


def ptri(S, x, y, h, w=None, k=0.4):
    """Small solid right-pointing triangle with left edge at x and vertical centre y (for marks)."""
    w = h * 0.85 if w is None else w
    return mark(poly([(x, y - h / 2), (x + w, y), (x, y + h / 2)], closed=True, r=S.r * k))


def tri(S, x, y, h, w=None, k=0.5):
    """Right-pointing triangle outline points (closed) with its left edge at x, centred on y."""
    w = h * 0.85 if w is None else w
    return poly([(x, y - h / 2), (x + w, y), (x, y + h / 2)], closed=True, r=S.r * k)


def ahead(cx, cy, r, deg, size=2.2, cw=True, S=None):
    """Open arrowhead (chevron) at angle deg on a circle, pointing along the travel direction."""
    px, py = polar(cx, cy, r, deg)
    a = math.radians(deg)
    tx, ty = (-math.sin(a), math.cos(a)) if cw else (math.sin(a), -math.cos(a))
    nx, ny = math.cos(a), math.sin(a)
    b1 = (px - tx * size + nx * size, py - ty * size + ny * size)
    b2 = (px - tx * size - nx * size, py - ty * size - ny * size)
    return poly([b1, (px, py), b2], r=(S.r * 0.6 if S else 0))


def head(S, tip, dirdeg, size=2.4):
    """Open arrowhead chevron with its tip at `tip`, pointing toward dirdeg (0 = right, 90 = down)."""
    a = math.radians(dirdeg)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    b1 = (tip[0] - ux * size + nx * size, tip[1] - uy * size + ny * size)
    b2 = (tip[0] - ux * size - nx * size, tip[1] - uy * size - ny * size)
    return poly([b1, tip, b2], r=S.r * 0.6)


# --------------------------------------------------------------------------- tiny text marks (solid, 1.4 px strokes)

_G = {
    "0": [["M", .5, 0, "C", 1.15, 0, 1.15, 1, .5, 1, "C", -.15, 1, -.15, 0, .5, 0, "Z"]],
    "1": [["M", .05, .22, "L", .6, 0, "L", .6, 1]],
    "2": [["M", 0, .26, "C", 0, -.08, 1, -.1, 1, .3, "C", 1, .6, 0, .7, 0, 1, "L", 1, 1]],
    "4": [["M", 0, 0, "L", 0, .65, "L", 1, .65], ["M", .72, 0, "L", .72, 1]],
    "3": [["M", 0, .08, "C", .3, -.06, 1, -.02, 1, .26, "C", 1, .46, .6, .5, .4, .5],
          ["M", .4, .5, "C", .9, .5, 1.05, .7, 1, .8, "C", .95, 1.05, .3, 1.08, 0, .9]],
    "6": [["M", .9, .08, "C", .5, -.05, 0, .2, 0, .65, "C", 0, 1.1, 1, 1.1, 1, .68, "C", 1, .3, .3, .3, .05, .6]],
    "8": [["M", .5, .5, "C", -.1, .4, 0, 0, .5, 0, "C", 1, 0, 1.1, .4, .5, .5],
          ["M", .5, .5, "C", -.15, .6, -.1, 1, .5, 1, "C", 1.1, 1, 1.15, .6, .5, .5]],
    "A": [["M", 0, 1, "L", .5, 0, "L", 1, 1], ["M", .2, .68, "L", .8, .68]],
    "B": [["M", 0, 0, "L", 0, 1], ["M", 0, 0, "L", .55, 0, "C", 1.02, 0, 1.02, .5, .55, .5, "L", 0, .5],
          ["M", .55, .5, "C", 1.1, .5, 1.1, 1, .55, 1, "L", 0, 1]],
    "D": [["M", 0, 0, "L", 0, 1, "L", .45, 1, "C", 1.1, 1, 1.1, 0, .45, 0, "Z"]],
    "H": [["M", 0, 0, "L", 0, 1], ["M", 1, 0, "L", 1, 1], ["M", 0, .5, "L", 1, .5]],
    "R": [["M", 0, 1, "L", 0, 0, "L", .55, 0, "C", 1.02, 0, 1.02, .52, .55, .52, "L", 0, .52], ["M", .5, .52, "L", 1, 1]],
    "S": [["M", 1, .12, "C", .6, -.08, 0, .02, 0, .26, "C", 0, .52, 1, .48, 1, .76, "C", 1, 1.05, .4, 1.1, 0, .88]],
    "K": [["M", 0, 0, "L", 0, 1], ["M", 1, 0, "L", 0, .62], ["M", .3, .45, "L", 1, 1]],
    "M": [["M", 0, 1, "L", 0, 0, "L", .5, .6, "L", 1, 0, "L", 1, 1]],
    "L": [["M", 0, 0, "L", 0, 1, "L", 1, 1]],
    "C": [["M", 1, .15, "C", .6, -.05, 0, 0, 0, .5, "C", 0, 1, .6, 1.05, 1, .85]],
    "E": [["M", 1, 0, "L", 0, 0, "L", 0, 1, "L", 1, 1], ["M", 0, .5, "L", .75, .5]],
    "P": [["M", 0, 1, "L", 0, 0, "L", .55, 0, "C", 1.05, 0, 1.05, .55, .55, .55, "L", 0, .55]],
}
_GW = {"1": 0.6, "M": 1.15, "A": 1.05}


def txt_d(s, cx, cy, h, cw, gap, S, sw=1.4):
    """Solid region d-string for the text s, centred on (cx, cy); cw = width of a normal character."""
    ws = [cw * _GW.get(c, 1.0) for c in s]
    total = sum(ws) + gap * (len(s) - 1)
    x = cx - total / 2
    y0 = cy - h / 2
    strokes = []
    for c, w in zip(s, ws):
        for st in _G[c]:
            cmds = []
            i = 0
            while i < len(st):
                op = st[i]
                i += 1
                if op == "Z":
                    cmds.append("Z")
                    continue
                n = {"M": 2, "L": 2, "C": 6}[op]
                vals = st[i:i + n]
                i += n
                pts = [f"{fmt(x + vals[j] * w)} {fmt(y0 + vals[j + 1] * h)}" for j in range(0, n, 2)]
                cmds.append(op + " ".join(pts))
            strokes.append(ST("".join(cmds), sw, "round" if S.name == "rounded" else "butt", "round" if S.name == "rounded" else "miter"))
        x += w + gap
    return path_to_d(U(*strokes))


def txt(S, s, cx, cy, h=6.0, cw=3.4, gap=1.4, sw=1.4):
    return mark(txt_d(s, cx, cy, h, cw, gap, S, sw))


# ============================================================================ chunk 1: transport and player chrome

@icon("replay-10-seconds", CAT, "Counterclockwise circular arrow with the number 10 inside",
      tags=["rewind 10", "back 10 seconds", "skip back", "replay", "jump back", "podcast", "video player"])
def _(S):
    return [line(arc(12, 12, 9, -68, 248)), line(ahead(12, 12, 9, -68, 2.4, False, S)), txt(S, "10", 12, 12.5, 6.4, 3.4, 1.6)]


@icon("forward-30-seconds", CAT, "Clockwise circular arrow with the number 30 inside",
      tags=["forward 30", "skip ahead 30 seconds", "jump forward", "fast forward", "podcast", "video player"])
def _(S):
    return [line(arc(12, 12, 9, -68, 248)), line(ahead(12, 12, 9, 248, 2.4, True, S)), txt(S, "30", 12, 12.5, 6.4, 3.4, 1.6)]


@icon("start-over", CAT, "Play triangle beside a bar with a curved arrow arching back to the bar",
      tags=["restart", "from the beginning", "replay from start", "back to start", "rewind", "play again"])
def _(S):
    return [line(seg(4.5, 13, 4.5, 21)), shell(tri(S, 9, 17, 9, 10.5)),
            line("M20 10C20 3 4.5 3 4.5 8"), line(head(S, (4.5, 9.8), 90, 2.3))]


@icon("playback-speed", CAT, "Speedometer arc with a needle and a small play triangle at the pivot",
      tags=["speed", "tempo", "faster", "slower", "1.5x", "rate", "gauge"])
def _(S):
    return [line(arc(12, 14, 9, 150, 30)), line(seg(13.5, 12.5, 18, 7.5)), ptri(S, 8.5, 15, 5.5, 4.6)]


@icon("ab-repeat", CAT, "Letters A and B over a progress track with a loop arrow above the span between them",
      tags=["loop section", "repeat segment", "section repeat", "a to b", "practice loop", "loop a b"])
def _(S):
    return [line(poly([(6.5, 8.5), (6.5, 4.5), (17.5, 4.5), (17.5, 7)], r=S.r * 0.6)), line(head(S, (17.5, 8.8), 90, 2.3)),
            txt(S, "A", 6.5, 14.2, 6, 3.6), txt(S, "B", 17.5, 14.2, 6, 3.6),
            line(seg(2, 20.5, 22, 20.5))]


@icon("gapless-playback", CAT, "Five waveform bars in an unbroken row with a link bracket underneath",
      tags=["seamless", "no gap", "continuous", "crossfade off", "album playback", "live album"])
def _(S):
    bars = [(4, 8, 14), (8, 5, 17), (12, 7, 15), (16, 4, 18), (20, 8, 14)]
    return [*[line(seg(x, a, x, b)) for x, a, b in bars], line(poly([(8, 19), (8, 21.5), (16, 21.5), (16, 19)], r=S.r * 0.4))]


@icon("autoplay", CAT, "Pill-shaped switch whose round knob holds a play triangle",
      tags=["auto play", "auto-play next", "toggle", "switch", "continuous play", "next episode"])
def _(S):
    return [shell(rect(1.5, 5.5, 21, 13, 6.5)), detail(circle(16, 12, 3.6)), ptri(S, 14.8, 12, 3.4, 3)]


@icon("play-next", CAT, "Play triangle and a down arrow feeding into a list of lines",
      tags=["up next", "queue next", "add to queue", "play after this", "insert in queue", "playlist"])
def _(S):
    return [shell(tri(S, 3.5, 6.5, 8, 7)), line(seg(17, 3, 17, 9.5)), line(head(S, (17, 10.5), 90, 2.3)),
            line(seg(3, 13.5, 21, 13.5)), line(seg(3, 17.5, 21, 17.5)), line(seg(3, 21, 14, 21))]


@icon("now-playing", CAT, "Square album cover beside three equaliser bars of different heights",
      tags=["currently playing", "track playing", "equalizer", "music player", "audio bars", "live track"])
def _(S):
    return [shell(rect(2.5, 7.5, 9, 9.5, rr(S, 2))), line(seg(14.5, 17, 14.5, 11)), line(seg(17.75, 17, 17.75, 5.5)), line(seg(21, 17, 21, 13))]


@icon("mini-player", CAT, "Phone outline with a slim player bar near the bottom holding a thumbnail and play triangle",
      tags=["picture in picture", "minimised player", "compact player", "bottom player", "floating player", "now playing bar"])
def _(S):
    return [shell(rect(5, 2, 14, 20, rr(S, 3))), detail(seg(5, 14.5, 19, 14.5)),
            mark(rect(7.5, 16.2, 3.6, 3.6, S.R * 0.2)), ptri(S, 14, 18, 3.8, 3.2)]


@icon("sleep-timer", CAT, "Crescent moon with a small clock face in its hollow",
      tags=["sleep", "auto stop", "bedtime", "countdown", "stop after", "night timer"])
def _(S):
    moon = D(P(circle(10.5, 10.5, 8.5)), P(circle(15, 15, 6.6)), P(circle(17, 17, 8.2)))
    return [shell(path_to_d(moon)), shell(circle(17, 17, 4.4)),
            detail(poly([(17, 14.8), (17, 17), (18.6, 18)], r=S.r * 0.3))]


# ============================================================================ chunk 2: video and library views

def globe_d(cx, cy, r, w=1.1):
    disc = P(circle(cx, cy, r))
    cuts = [ST(ellipse(cx, cy, r * 0.42, r), w, "butt", "miter"), ST(seg(cx - r, cy, cx + r, cy), w, "butt", "miter")]
    return path_to_d(D(disc, *cuts))


@icon("skip-silence", CAT, "Waveform bars at each side with two chevrons squeezing a flat gap shut",
      tags=["trim silence", "remove pauses", "voice boost", "smart speed", "shorten gaps", "podcast"])
def _(S):
    return [line(seg(3.5, 7.5, 3.5, 16.5)), line(seg(20.5, 7.5, 20.5, 16.5)),
            line(poly([(7.6, 8.5), (10.6, 12), (7.6, 15.5)], r=S.r * 0.5)), line(poly([(16.4, 8.5), (13.4, 12), (16.4, 15.5)], r=S.r * 0.5))]


@icon("seek-bar", CAT, "Progress track filled on the left with a round knob and a time label above",
      tags=["scrubber", "progress bar", "timeline slider", "scrub", "video progress", "position"])
def _(S):
    return [txt(S, "30", 12, 6.2, 6, 3.3, 1.4), solid(rect(3, 14.6, 6.5, 3.2, 1.6 if S.name == "rounded" else 0)),
            shell(circle(12, 16.2, 3)), line(seg(15, 16.2, 21, 16.2))]


@icon("seek-preview", CAT, "Thumbnail frame with a pointer tail above a progress bar and knob",
      tags=["scrub preview", "hover preview", "thumbnail preview", "timeline thumbnail", "video scrubbing", "frame preview"])
def _(S):
    return [shell(poly([(3, 3), (21, 3), (21, 13), (14, 13), (12, 15.5), (10, 13), (3, 13)], closed=True, r=S.r * 0.5)),
            ptri(S, 10.4, 8, 5, 4.4), line(seg(3, 20, 9.5, 20)), line(seg(14.5, 20, 21, 20)), dot(12, 20, 2)]


@icon("playhead", CAT, "Vertical line topped with a downward pentagon marker crossing a row of timeline clips",
      tags=["timeline marker", "scrub head", "current time", "editing", "video editor", "cursor"])
def _(S):
    return [shell(rect(2, 14.5, 20, 6.5, rr(S, 1.5))), detail(seg(7, 14.5, 7, 21)), detail(seg(17, 14.5, 17, 21)),
            shell(poly([(8, 3), (16, 3), (16, 7), (12, 10.5), (8, 7)], closed=True, r=S.r * 0.4)), line(seg(12, 10.5, 12, 22.5))]


@icon("video-buffering", CAT, "Video frame with a ring of short spinner dashes, one longer than the rest",
      tags=["loading video", "spinner", "waiting", "stalled", "streaming", "wait"])
def _(S):
    out = [shell(rect(2, 4.5, 20, 15, rr(S, 3)))]
    for i in range(8):
        a = -90 + 45 * i
        r0, r1 = (2.2, 5.6) if i == 0 else (3.3, 5.4)
        out.append(detail(seg(*polar(12, 12, r0, a), *polar(12, 12, r1, a))))
    return out


@icon("transport-controls", CAT, "Rounded bar holding skip back, a larger play triangle and skip forward",
      tags=["media controls", "player buttons", "previous play next", "control bar", "remote", "player bar"])
def _(S):
    return [shell(rect(1.5, 6, 21, 12, rr(S, 4))),
            mark(rect(4, 9.2, 1.4, 5.6)), mark(poly([(8, 9.2), (5.6, 12), (8, 14.8)], closed=True)),
            ptri(S, 10.2, 12, 7.2, 4.6),
            mark(poly([(16, 9.2), (18.4, 12), (16, 14.8)], closed=True)), mark(rect(18.6, 9.2, 1.4, 5.6))]


@icon("jog-wheel", CAT, "Large round jog dial with an inner platter ring and a finger dimple near its edge",
      tags=["shuttle", "dj wheel", "scrub wheel", "turntable platter", "editing controller", "frame stepping"])
def _(S):
    return [shell(circle(12, 12, 10)), detail(circle(12, 12, 6)), sdot(S, *polar(12, 12, 3.2, 135), 1.3)]


@icon("cue-point", CAT, "Waveform bars with a vertical marker line carrying a small flag",
      tags=["marker", "audio cue", "hot cue", "flag", "dj cue", "position marker"])
def _(S):
    bars = [(3.5, 13, 19), (7.5, 10, 22), (16.5, 12, 20), (20.5, 14, 18)]
    return [*[line(seg(x, a, x, b)) for x, a, b in bars], line(seg(12, 3, 12, 22)), shell(poly([(12, 3), (19, 5.5), (12, 8)], closed=True, r=S.r * 0.4))]


@icon("tap-tempo", CAT, "Fingertip pressing down on a pad with impact marks either side",
      tags=["bpm", "beat tap", "tempo tap", "metronome", "rhythm", "find tempo"])
def _(S):
    return [shell(rect(9, 2, 6, 9.5, 3)), shell(rect(3, 15.5, 18, 5.5, rr(S, 2.5))),
            line(seg(4.5, 7, 6.5, 8.5)), line(seg(4, 11.5, 6.5, 11.8)), line(seg(19.5, 7, 17.5, 8.5)), line(seg(20, 11.5, 17.5, 11.8))]


@icon("frame-by-frame", CAT, "Film frame with sprocket holes and a step-forward triangle with a bar beside it",
      tags=["step frame", "next frame", "frame advance", "single frame", "animation", "stepping"])
def _(S):
    return [shell(rect(2, 3.5, 12, 17, rr(S, 2))), mark(rect(3.7, 6.3, 1.4, 1.8)), mark(rect(3.7, 11.1, 1.4, 1.8)), mark(rect(3.7, 15.9, 1.4, 1.8)),
            mark(rect(10.9, 6.3, 1.4, 1.8)), mark(rect(10.9, 11.1, 1.4, 1.8)), mark(rect(10.9, 15.9, 1.4, 1.8)),
            shell(poly([(16.4, 8.5), (20, 12), (16.4, 15.5)], closed=True, r=S.r * 0.3)), line(seg(21.8, 8, 21.8, 16))]


@icon("frame-rate", CAT, "Film frame with the number 60 inside and three speed lines trailing behind",
      tags=["fps", "60fps", "frames per second", "refresh rate", "video speed", "smooth motion"])
def _(S):
    return [shell(rect(8, 5, 14, 14, rr(S, 3))), txt(S, "60", 15, 12.2, 6, 3.2, 1.3),
            line(seg(2, 8.5, 5, 8.5)), line(seg(2, 12, 5, 12)), line(seg(2, 15.5, 5, 15.5))]


@icon("resume-playback", CAT, "Video thumbnail with a play triangle and a part-filled progress bar along the bottom",
      tags=["continue watching", "pick up where you left off", "resume video", "keep watching", "saved position", "unfinished"])
def _(S):
    return [shell(rect(2, 4, 20, 16, rr(S, 3))), ptri(S, 10.2, 10, 6, 5.2),
            mark(rect(3.6, 15.2, 9, 1.8)), mark(circle(12.6, 16.1, 1.6))]


@icon("episode-list", CAT, "Three rows each with a small play disc on the left and two text lines",
      tags=["episodes", "season list", "tv episodes", "series", "playlist rows", "chapters list"])
def _(S):
    out = []
    for y in (4.5, 12, 19.5):
        tri_pts = [(4.3, y - 1.4), (6.4, y), (4.3, y + 1.4)]
        out.append(solid(path_to_d(D(P(circle(5, y, 2.8)), P(poly(tri_pts, closed=True))))))
        out.append(line(seg(10, y - 1.5, 21, y - 1.5)))
        out.append(line(seg(10, y + 1.7, 17, y + 1.7)))
    return out


@icon("scene-selection", CAT, "Two by two grid of numbered thumbnails",
      tags=["scenes", "chapters", "chapter menu", "dvd menu", "jump to scene", "thumbnails grid"])
def _(S):
    out = []
    for n, (x, y) in enumerate([(2, 2.5), (12.5, 2.5), (2, 12.5), (12.5, 12.5)]):
        out.append(shell(rect(x, y, 9.5, 9, rr(S, 1.8))))
        out.append(txt(S, str(n + 1), x + 4.75, y + 4.5, 3.8, 2.4, 1, 1.1))
    return out


@icon("commentary-track", CAT, "Director's chair below a speech bubble holding sound bars",
      tags=["director commentary", "audio commentary", "behind the scenes", "director", "dvd extra", "voice track"])
def _(S):
    return [shell(poly([(4, 2), (20, 2), (20, 9), (14.5, 9), (12, 11.5), (9.5, 9), (4, 9)], closed=True, r=S.r * 0.8)),
            mark(rect(8.4, 4.4, 1.3, 2.6)), mark(rect(11.35, 3.8, 1.3, 3.8)), mark(rect(14.3, 4.6, 1.3, 2.2)),
            line(seg(6.5, 14, 17.5, 14)), line(seg(6.5, 18, 17.5, 18)), line(seg(6.5, 14, 6.5, 22)), line(seg(17.5, 14, 17.5, 22))]


@icon("audio-language", CAT, "Speech bubble holding a waveform beside the letter A and a foreign-style glyph",
      tags=["dub", "dubbed audio", "audio track language", "voice language", "multilingual audio", "language track"])
def _(S):
    return [shell(poly([(2, 4), (14, 4), (14, 14), (8.5, 14), (6, 17), (6, 14), (2, 14)], closed=True, r=S.r * 0.8)),
            mark(rect(4.6, 7.8, 1.3, 2.4)), mark(rect(7.2, 6.6, 1.3, 4.8)), mark(rect(9.8, 7.4, 1.3, 3.2)),
            txt(S, "A", 19, 6, 5, 3.2, 1, 1.3),
            mark(path_to_d(U(ST("M16.6 13H21.4", 1.3, "butt", "miter"), ST("M19 11.6V13", 1.3, "butt", "miter"),
                             ST("M17 19L21.2 13.4", 1.3, "butt", "miter"), ST("M21 19L16.8 13.4", 1.3, "butt", "miter"))))]


@icon("translated-subtitles", CAT, "Screen with two subtitle bars at the bottom and a small globe in the top corner",
      tags=["subtitles translation", "caption language", "foreign subtitles", "closed captions language", "translate captions", "cc language"])
def _(S):
    return [shell(rect(2, 4, 20, 15, rr(S, 3))), mark(globe_d(16.6, 8.6, 3.2)),
            mark(rect(5, 12.2, 14, 1.6, 0.8)), mark(rect(7.5, 15.1, 9, 1.6, 0.8))]


@icon("skip-ad", CAT, "Rounded button holding the letters AD and a skip-forward symbol",
      tags=["skip advert", "skip advertisement", "skip commercial", "ad break", "skip sponsor", "advert"])
def _(S):
    return [shell(rect(1.5, 6, 21, 12, rr(S, 4))), txt(S, "AD", 8.4, 12, 5.8, 3.2, 1.4),
            mark(poly([(14.6, 8.8), (18.8, 12), (14.6, 15.2)], closed=True)), mark(rect(19.2, 8.8, 1.4, 6.4))]


@icon("media-library", CAT, "Stack of cards with the front one showing a play triangle",
      tags=["video library", "collection", "my library", "media collection", "saved videos", "stack"])
def _(S):
    return [line(seg(7, 3.5, 17, 3.5)), line(seg(5, 6.5, 19, 6.5)), shell(rect(3, 9.5, 18, 11.5, rr(S, 2.5))), ptri(S, 10.3, 15.2, 6, 5.2)]


# ============================================================================ chunk 3: screens, devices and tape formats

def rot_pts(pts, deg, ox=0.0, oy=0.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(ox + x * c - y * s, oy + x * s + y * c) for x, y in pts]


@icon("video-playlist", CAT, "Video frame with a play triangle on the left and three list lines on the right",
      tags=["playlist", "video queue", "up next list", "watch list", "series list", "queue"])
def _(S):
    return [shell(rect(2, 4, 20, 16, rr(S, 3))), ptri(S, 5.2, 12, 6.4, 5.4),
            detail(seg(12.5, 8.5, 18.5, 8.5)), detail(seg(12.5, 12, 18.5, 12)), detail(seg(12.5, 15.5, 18.5, 15.5))]


@icon("video-wall", CAT, "Three by three grid of touching screens forming one large display with a play triangle in the middle",
      tags=["display wall", "tiled screens", "monitor wall", "signage wall", "control room", "multi screen"])
def _(S):
    return [shell(rect(2, 3, 20, 18, S.R)), detail(seg(8.67, 3, 8.67, 21)), detail(seg(15.33, 3, 15.33, 21)),
            detail(seg(2, 9, 22, 9)), detail(seg(2, 15, 22, 15)), ptri(S, 10.6, 12, 3.4, 3)]


@icon("multi-view", CAT, "Two by two grid of rounded rectangles each holding a small play triangle",
      tags=["split screen", "quad view", "multiple streams", "four videos", "grid view", "watch multiple"])
def _(S):
    out = []
    for x, y in [(2, 3), (12.5, 3), (2, 12.5), (12.5, 12.5)]:
        out.append(shell(rect(x, y, 9.5, 8.5, rr(S, 2))))
        out.append(ptri(S, x + 3.6, y + 4.25, 3.6, 3))
    return out


@icon("instant-replay", CAT, "Television with a circular replay arrow around a play triangle on its screen",
      tags=["replay", "rewatch", "action replay", "sports replay", "slow motion replay", "tv replay"])
def _(S):
    return [shell(rect(2, 3, 20, 15, rr(S, 2.5))), line(seg(8, 21, 16, 21)),
            detail(arc(12, 10.5, 4.3, -70, 250)), detail(ahead(12, 10.5, 4.3, -70, 1.8, False, S)), ptri(S, 10.6, 10.5, 3.6, 3)]


@icon("highlight-reel", CAT, "Film strip with a four-point sparkle star on its centre frame",
      tags=["highlights", "best moments", "sizzle reel", "montage", "recap", "top clips"])
def _(S):
    star = poly([(12, 7.8), (13.2, 10.8), (16.2, 12), (13.2, 13.2), (12, 16.2), (10.8, 13.2), (7.8, 12), (10.8, 10.8)], closed=True)
    return [shell(rect(2, 5.5, 20, 13, rr(S, 2))), detail(seg(7.5, 5.5, 7.5, 18.5)), detail(seg(16.5, 5.5, 16.5, 18.5)),
            mark(star), line(seg(3.5, 21.5, 20.5, 21.5))] if False else [
            shell(rect(2, 5, 20, 14, S.R)), detail(seg(7, 5, 7, 19)), detail(seg(17, 5, 17, 19)), mark(star)]


@icon("screen-mirroring", CAT, "Television with a play triangle and a small phone below with an arrow up to the screen",
      tags=["mirror phone", "cast screen", "screen cast", "display on tv", "share to tv", "wireless display"])
def _(S):
    return [shell(rect(2, 2.5, 20, 11, rr(S, 2.5))), ptri(S, 10.4, 8, 5, 4.4),
            shell(rect(3.5, 15.5, 5.5, 7, rr(S, 1.5))), line(seg(15, 22, 15, 17.5)), line(head(S, (15, 16.2), -90, 2.4))]


@icon("multiroom-audio", CAT, "House outline split into two rooms with a small speaker in each",
      tags=["whole home audio", "multi room speakers", "home sound", "house music", "speaker group", "zones"])
def _(S):
    spk = [(5.3, 15), (6.6, 15), (8.6, 13.3), (8.6, 18.7), (6.6, 17), (5.3, 17)]
    return [shell(poly([(2, 10.5), (12, 2.5), (22, 10.5), (22, 21), (2, 21)], closed=True, r=S.r * 0.5)), detail(seg(12, 11, 12, 21)),
            mark(poly(spk, closed=True)), mark(poly([(24 - x, y) for x, y in spk], closed=True))]


@icon("smartphone-remote", CAT, "Phone showing a round directional pad with a play button, with signal arcs above",
      tags=["phone as remote", "remote control app", "tv remote app", "controller app", "second screen", "wireless control"])
def _(S):
    return [line(arc(12, 9, 2.6, 215, 325)), line(arc(12, 9, 5.6, 225, 315)), shell(rect(5, 10.5, 14, 11.5, rr(S, 3))),
            detail(circle(12, 16.2, 3.4)), ptri(S, 10.8, 16.2, 3, 2.6)]


@icon("curved-tv", CAT, "Wide television seen from the front with gently curved top and bottom edges on a short stand",
      tags=["curved screen", "curved monitor", "ultrawide", "television", "home theatre", "display"])
def _(S):
    if S.name == "line":
        body = "M2 5Q12 8 22 5V15Q12 18 2 15Z"
    else:
        body = "M3.8 5.6Q12 8 20.2 5.6Q22 5.1 22 6.9V13.6Q22 15.3 20.2 14.9Q12 17.3 3.8 14.9Q2 15.3 2 13.6V6.9Q2 5.1 3.8 5.6Z"
    return [shell(body), line(seg(12, 16.5, 12, 20)), line(seg(7.5, 21, 16.5, 21))]


@icon("eject", CAT, "Upward pointing triangle above a flat horizontal bar",
      tags=["eject disc", "remove media", "unmount", "release", "open tray", "safely remove"])
def _(S):
    return [shell(poly([(12, 4), (21, 14), (3, 14)], closed=True, r=S.r * 0.6)), line(seg(3.5, 19, 20.5, 19))]


@icon("eight-track-cartridge", CAT, "Rectangular tape cartridge with a rounded back corner, a label area and an exposed tape slot",
      tags=["8-track", "8 track tape", "tape cartridge", "retro audio", "vintage music", "cartridge tape"])
def _(S):
    if S.name == "line":
        body = "M2 5H16A6 6 0 0 1 22 11V19H2Z"
    else:
        body = "M3.5 5H16A6 6 0 0 1 22 11V17.5A1.5 1.5 0 0 1 20.5 19H3.5A1.5 1.5 0 0 1 2 17.5V6.5A1.5 1.5 0 0 1 3.5 5Z"
    return [shell(body), detail(rect(6, 8.5, 9.5, 4, rr(S, 1))), mark(rect(5, 15.4, 9, 1.4))]


@icon("in-flight-entertainment", CAT, "Back of an airplane seat with a small screen showing a play triangle and a headphone jack below it",
      tags=["airplane screen", "seatback screen", "plane movies", "flight movies", "ife", "inflight"])
def _(S):
    return [shell(rect(4, 2.5, 16, 19, rr(S, 3))), detail(rect(7.5, 6, 9, 7, rr(S, 1))), ptri(S, 10.6, 9.5, 3.2, 2.8), dot(12, 17.5, 1.5)]


# ============================================================================ chunk 4: audio routing, formats and effects

def wv(xe, h, xp, cy=12.0):
    """Sound-wave arc: ends at (xe, cy +- h), bulging right to x = xp."""
    s = xp - xe
    R = (h * h + s * s) / (2 * s)
    return f"M{fmt(xe)} {fmt(cy - h)}A{fmt(R)} {fmt(R)} 0 0 1 {fmt(xe)} {fmt(cy + h)}"


@icon("rec-indicator", CAT, "Camera viewfinder corner brackets with a large filled dot and the letters REC at the top",
      tags=["recording", "record light", "on air", "rec", "viewfinder", "camera recording"])
def _(S):
    k = S.r * 0.3
    return [line(poly([(2.5, 7), (2.5, 2.5), (7, 2.5)], r=k)), line(poly([(17, 2.5), (21.5, 2.5), (21.5, 7)], r=k)),
            line(poly([(2.5, 17), (2.5, 21.5), (7, 21.5)], r=k)), line(poly([(17, 21.5), (21.5, 21.5), (21.5, 17)], r=k)),
            txt(S, "REC", 12, 7.2, 4.4, 2.6, 1.1, 1.2), solid(circle(12, 15, 3.4))]


@icon("tally-light", CAT, "Small box camera with a round lamp on top and short rays around the lamp showing it is live",
      tags=["on air light", "live indicator", "red light", "camera lamp", "studio light", "broadcast live"])
def _(S):
    out = [shell(rect(3, 13, 18, 8, rr(S, 2.5))), detail(circle(12, 17, 1.6)), shell(circle(12, 8.3, 2.5))]
    for a in (-90, -40, -140, 0, 180):
        out.append(line(seg(*polar(12, 8.3, 4.6, a), *polar(12, 8.3, 6.4, a))))
    return out


@icon("bass-boost", CAT, "Speaker with a large low sound wave and a small up arrow beside it",
      tags=["bass", "low end", "subwoofer", "bass enhance", "deep sound", "eq bass"])
def _(S):
    spk = [(2, 9), (5.5, 9), (10, 4.5), (10, 19.5), (5.5, 15), (2, 15)]
    return [shell(poly(spk, closed=True, r=S.r * 0.66)), line(wv(13.2, 3.7, 15.6)), line(seg(20.5, 20, 20.5, 8)), line(head(S, (20.5, 6.6), -90, 2.4))]


@icon("noise-cancellation", CAT, "Headphones with a wave entering one cup and flattening to a straight line",
      tags=["anc", "noise canceling", "noise cancelling", "quiet mode", "silence noise", "active noise"])
def _(S):
    return [line("M3.5 13.5V12A8.5 8.5 0 0 1 20.5 12V13.5"), shell(rect(2.5, 13.5, 4.5, 8, rr(S, 2))), shell(rect(17, 13.5, 4.5, 8, rr(S, 2))),
            line("M8.6 17.5Q9.6 14 10.8 17.5T13 17.5H15.4")]


@icon("transparency-mode", CAT, "Headphones with sound arcs passing between the ear cups toward the centre",
      tags=["ambient sound", "hear through", "awareness mode", "pass through", "listen around", "outside sound"])
def _(S):
    return [line("M3.5 13.5V12A8.5 8.5 0 0 1 20.5 12V13.5"), shell(rect(2.5, 13.5, 4.5, 8, rr(S, 2))), shell(rect(17, 13.5, 4.5, 8, rr(S, 2))),
            line(arc(8.6, 17.5, 1.9, -60, 60)), line(arc(15.4, 17.5, 1.9, 120, 240))]


@icon("mono-audio", CAT, "Single speaker cabinet with a woofer and tweeter above the letter M",
      tags=["mono", "single channel", "one speaker", "mono sound", "mono mix", "accessibility audio"])
def _(S):
    return [shell(rect(6.5, 2.5, 11, 13.5, rr(S, 2.5))), detail(circle(12, 11, 2.2)), sdot(S, 12, 6, 1.2), txt(S, "M", 12, 19.6, 4.4, 3.2, 1, 1.3)]


@icon("stereo-audio", CAT, "Two speaker cabinets side by side above the letters L and R",
      tags=["stereo", "left right", "two channel", "stereo sound", "stereo mix", "speakers pair"])
def _(S):
    out = []
    for x, ch in ((2, "L"), (13, "R")):
        out += [shell(rect(x, 2.5, 9, 13.5, rr(S, 2.5))), detail(circle(x + 4.5, 11, 2.0)), sdot(S, x + 4.5, 6, 1.1), txt(S, ch, x + 4.5, 19.6, 4.2, 3, 1, 1.3)]
    return out


@icon("audio-output", CAT, "Speaker and headphones side by side with a curved arrow arching from one to the other",
      tags=["output device", "switch speaker", "audio device", "sound output", "headphones or speakers", "playback device"])
def _(S):
    spk = [(2.5, 16), (4.8, 16), (8, 13), (8, 21.5), (4.8, 18.5), (2.5, 18.5)]
    return [shell(poly(spk, closed=True, r=S.r * 0.5)),
            line("M14.2 18V17.3A3.8 3.8 0 0 1 21.8 17.3V18"), shell(rect(13.2, 18, 2.6, 3.6, rr(S, 1))), shell(rect(20.2, 18, 2.6, 3.6, rr(S, 1))),
            line("M5.5 10.5C5.5 3.5 18 3.5 18 10"), line(head(S, (18, 11.5), 90, 2.3))]


@icon("lossless-audio", CAT, "Smooth unbroken waveform curve inside a diamond outline",
      tags=["hi-res audio", "flac", "cd quality", "high fidelity", "uncompressed", "hifi"])
def _(S):
    return [shell(poly([(12, 2), (22, 12), (12, 22), (2, 12)], closed=True, r=S.r * 1.2)), detail("M6.6 12C8.2 6.6 10 6.6 12 12C14 17.4 15.8 17.4 17.4 12")]


@icon("hdr-video", CAT, "Rounded badge with a half-filled sun above the letters HDR",
      tags=["high dynamic range", "hdr", "hdr10", "wide contrast", "bright video", "video quality"])
def _(S):
    ring = D(P(circle(12, 8.8, 2.8)), P(circle(12, 8.8, 1.7)))
    half = D(P(circle(12, 8.8, 1.7)), P(rect(9, 6, 3, 6)))
    return [shell(rect(2, 3.5, 20, 17, rr(S, 4))), mark(path_to_d(U(ring, half))), txt(S, "HDR", 12, 15.6, 4.6, 3, 1.1, 1.3)]


@icon("8k-resolution", CAT, "Rounded badge containing the bold characters 8K",
      tags=["8k", "ultra hd 8k", "4320p", "video quality", "resolution", "high resolution"])
def _(S):
    return [shell(rect(2, 4.5, 20, 15, rr(S, 4))), txt(S, "8K", 12, 12, 7, 4.4, 1.6, 1.8)]


@icon("sd-video", CAT, "Rounded badge containing the bold characters SD",
      tags=["sd", "standard definition", "480p", "low resolution", "video quality", "resolution"])
def _(S):
    return [shell(rect(2, 4.5, 20, 15, rr(S, 4))), txt(S, "SD", 12, 12, 7, 4.4, 1.6, 1.8)]


@icon("audio-visualizer", CAT, "Small circle ringed by short radiating bars of varying length like a radial spectrum",
      tags=["spectrum", "radial equalizer", "music visualizer", "sound bars", "audio reactive", "eq circle"])
def _(S):
    lens = [4, 3.2, 2.2, 3.4, 1.6, 2.6, 1.4, 2.6, 1.6, 3.4, 2.2, 3.2]
    out = [shell(circle(12, 12, 3.4))]
    for i, ln in enumerate(lens):
        a = -90 + 30 * i
        out.append(line(seg(*polar(12, 12, 6.6, a), *polar(12, 12, 6.6 + ln, a))))
    return out


@icon("echo-effect", CAT, "Sound wave arc followed by two smaller fading copies stepping away to the right",
      tags=["delay", "repeat sound", "echo", "audio delay", "fx", "bounce"])
def _(S):
    return [line(wv(4.5, 7.5, 8.3)), line(wv(11.3, 5.2, 14.2)), line(wv(17.2, 3, 19.4))]


@icon("reverb-effect", CAT, "Speaker inside a room outline with sound waves bouncing off the walls",
      tags=["room sound", "hall reverb", "ambience", "echo chamber", "acoustic space", "fx"])
def _(S):
    return [shell(rect(2, 3, 20, 18, rr(S, 3))), mark(poly([(5.5, 10), (8, 10), (11, 7.3), (11, 16.7), (8, 14), (5.5, 14)], closed=True)),
            detail(wv(13.8, 2.6, 15.6)), detail(wv(16.6, 5.2, 18.4))]


@icon("distortion-effect", CAT, "Waveform whose peaks are sliced flat at a top and bottom line like a clipped signal",
      tags=["clipping", "overdrive", "fuzz", "clipped wave", "guitar pedal", "fx"])
def _(S):
    pts = []
    n = 32
    for i in range(n + 1):
        x = 2.5 + 19 * i / n
        v = max(-1, min(1, 1.9 * math.sin(2 * math.pi * 2 * i / n)))
        pts.append((x, 12 - 5.5 * v))
    return [line(poly(pts, r=S.r * 0.4))]


@icon("pitch-shift", CAT, "Music note with a small up arrow and a small down arrow stacked beside it",
      tags=["transpose", "key change", "pitch up", "pitch down", "tuning", "voice changer"])
def _(S):
    return [shell(circle(6.5, 17, 3.2)), line(seg(9.7, 17, 9.7, 4.5)), line(pick(S, "M9.7 4.5C10.7 8 14.5 8 14.5 11", "M9.7 4.5C10.7 8 14.5 8 14.5 10.6")),
            line(seg(19.5, 10, 19.5, 4)), line(head(S, (19.5, 2.8), -90, 2.4)), line(seg(19.5, 14, 19.5, 20)), line(head(S, (19.5, 21.2), 90, 2.4))]


@icon("time-stretch", CAT, "Waveform block with outward pointing arrows at both ends pulling it longer",
      tags=["stretch audio", "tempo change", "lengthen clip", "speed without pitch", "warp", "resize clip"])
def _(S):
    return [shell(rect(8, 6.5, 8, 11, rr(S, 2))), mark(rect(10, 10, 1.2, 4)), mark(rect(11.4, 8.8, 1.2, 6.4)), mark(rect(12.8, 10.4, 1.2, 3.2)),
            line(seg(5.6, 12, 2.6, 12)), line(head(S, (2.3, 12), 180, 2.4)), line(seg(18.4, 12, 21.4, 12)), line(head(S, (21.7, 12), 0, 2.4))]


@icon("audio-compressor", CAT, "Tall waveform squeezed between two horizontal bars with inward arrows",
      tags=["dynamic range", "compression", "limiter squeeze", "loudness", "squash", "mastering"])
def _(S):
    return [line(seg(2, 3, 22, 3)), line(seg(2, 21, 22, 21)),
            line(seg(9, 9, 9, 15)), line(seg(12, 7, 12, 17)), line(seg(15, 9, 15, 15)),
            line(seg(4, 4, 4, 8.2)), line(head(S, (4, 9.4), 90, 2.3)), line(seg(20, 4, 20, 8.2)), line(head(S, (20, 9.4), 90, 2.3)),
            line(seg(4, 20, 4, 15.8)), line(head(S, (4, 14.6), -90, 2.3)), line(seg(20, 20, 20, 15.8)), line(head(S, (20, 14.6), -90, 2.3))]


# ============================================================================ chunk 5: mixing, radio and editing

@icon("audio-fade", CAT, "Trapezoid volume envelope rising from zero, holding level, then sloping back down, with waveform bars inside",
      tags=["fade in", "fade out", "volume envelope", "crossfade", "ramp", "audio editing"])
def _(S):
    return [shell(poly([(2, 20), (8, 5), (16, 5), (22, 20)], closed=True, r=S.r * 0.6)),
            mark(rect(9.4, 10, 1.3, 6)), mark(rect(11.35, 8.5, 1.3, 9)), mark(rect(13.3, 10.5, 1.3, 5))]


@icon("audio-stems", CAT, "Song waveform on the left branching into three separate lanes of waveform",
      tags=["stem separation", "split tracks", "isolate vocals", "instrument tracks", "multitrack", "stems"])
def _(S):
    out = [line(seg(3, 9.5, 3, 14.5)), line(seg(6, 7.5, 6, 16.5)), line(seg(8.5, 12, 11, 12)), line(seg(11, 5, 11, 19))]
    for y in (5, 12, 19):
        out += [line(seg(11, y, 13.5, y)), line(seg(15, y - 1.2, 15, y + 1.2)), line(seg(18, y - 2.4, 18, y + 2.4)), line(seg(21, y - 1.6, 21, y + 1.6))]
    return out


@icon("sound-effects", CAT, "Jagged starburst shape with a small waveform in its centre",
      tags=["sfx", "foley", "sound fx", "audio effects", "bang", "effects library"])
def _(S):
    pts = []
    for i in range(16):
        r = 10 if i % 2 == 0 else 6.6
        pts.append(polar(12, 12, r, -90 + i * 22.5))
    return [shell(poly(pts, closed=True, r=S.r * 0.4)), detail(poly([(7.6, 12), (9.2, 12), (10.4, 9.2), (12, 14.8), (13.6, 9.2), (14.8, 12), (16.4, 12)], r=S.r * 0.3))]


@icon("lip-sync", CAT, "Open mouth beside a waveform with a bracket underneath linking the two",
      tags=["lipsync", "mouth sync", "dubbing", "audio video sync", "speech timing", "voice match"])
def _(S):
    return [shell("M2 10.5C4 5.5 10 5.5 12 10.5C10 15.5 4 15.5 2 10.5Z"), detail(seg(2.6, 10.6, 11.4, 10.6)),
            line(seg(16, 8.5, 16, 12.5)), line(seg(18.8, 6, 18.8, 15)), line(seg(21.6, 8, 21.6, 13)),
            line(poly([(7, 16.5), (7, 20), (19, 20), (19, 17)], r=S.r * 0.4))]


@icon("volume-limiter", CAT, "Speaker with sound waves that stop at a solid vertical ceiling line",
      tags=["peak limiter", "max volume", "loudness cap", "safe volume", "volume ceiling", "clipping guard"])
def _(S):
    spk = [(2, 9), (5.5, 9), (10, 4.5), (10, 19.5), (5.5, 15), (2, 15)]
    return [shell(poly(spk, closed=True, r=S.r * 0.66)), line(wv(13, 3.6, 15.2)), line(wv(16, 6, 17.8)), line(seg(21.3, 3, 21.3, 21))]


@icon("show-notes", CAT, "Document page with text lines and a small microphone in its top corner",
      tags=["podcast notes", "episode notes", "transcript", "episode description", "podcast page", "show page"])
def _(S):
    return [shell(rect(4, 2.5, 16, 19, rr(S, 3))), detail(seg(7.5, 8, 12, 8)), detail(seg(7.5, 11.5, 12, 11.5)),
            detail(seg(7.5, 15.5, 16.5, 15.5)), detail(seg(7.5, 19, 13.5, 19)),
            mark(rect(14.9, 5, 2.2, 4.4, 1.1)), mark(path_to_d(ST("M14 8.4A3 3 0 0 0 18 8.4", 1.1, "butt", "miter"))), mark(rect(15.45, 11.3, 1.1, 1.2))]


@icon("call-in-show", CAT, "Studio microphone on a stand beside a telephone handset",
      tags=["phone in", "talk radio", "caller", "listener call", "live call", "radio phone"])
def _(S):
    hs = [(-3, -7), (3, -7), (3, -3.4), (0.2, -2.8), (0.2, 2.8), (3, 3.4), (3, 7), (-3, 7)]
    hs = [(x * 1.02, y * 1.02) for x, y in hs]
    return [shell(rect(3.5, 2.5, 6, 10, 3)), line("M2 10.5A5.5 5.5 0 0 0 11 10.5"), line(seg(6.5, 16, 6.5, 20)), line(seg(3.5, 20.5, 9.5, 20.5)),
            shell(poly(rot_pts(hs, 28, 16.8, 12), closed=True, r=S.r * 0.5))]


@icon("digital-radio", CAT, "Compact portable radio with a small text display, speaker holes and a short antenna",
      tags=["dab", "dab radio", "digital tuner", "portable radio", "radio receiver", "fm dab"])
def _(S):
    return [line(seg(16.5, 8, 20, 2.5)), shell(rect(2.5, 8, 19, 13, rr(S, 3))), detail(rect(5.5, 11, 8, 3.6, 0.6)),
            sdot(S, 17.5, 11.6, 1), sdot(S, 17.5, 14.6, 1), sdot(S, 17.5, 17.6, 1), mark(rect(5.5, 17.2, 7, 1.4))]


@icon("radio-scanner", CAT, "Handheld receiver with a long rubber antenna, a small frequency screen and a grid of keys",
      tags=["police scanner", "scanner radio", "handheld receiver", "frequency scanner", "walkie", "monitor radio"])
def _(S):
    out = [line(seg(9.5, 9, 9.5, 2.3)), shell(rect(6.5, 9, 11, 13, rr(S, 3))), detail(rect(9, 11.6, 6, 3, 0.4))]
    for x in (9.2, 11.4, 13.6):
        out += [mark(rect(x, 17.3, 1.5, 1.4)), mark(rect(x, 19.4, 1.5, 1.4))]
    return out


@icon("fm-transmitter", CAT, "Car socket plug with a round display head and radio waves rising from its top",
      tags=["car fm transmitter", "bluetooth car adapter", "cigarette lighter adapter", "car audio adapter", "fm adapter", "wireless car audio"])
def _(S):
    return [shell(circle(12, 14, 4.6)), mark(rect(9.7, 13, 4.6, 2)), shell(rect(10.2, 18.6, 3.6, 3.4, rr(S, 1))),
            line(arc(12, 14, 8, -135, -45)), line(arc(12, 14, 11.2, -125, -55))]


@icon("broadcast-van", CAT, "Van seen from the side with a satellite dish raised on its roof",
      tags=["news van", "satellite truck", "outside broadcast", "ob van", "live truck", "sng"])
def _(S):
    return [shell(poly([(2, 17.5), (2, 11.5), (15.5, 11.5), (21.5, 15), (21.5, 17.5)], closed=True, r=S.r * 0.6)),
            shell(circle(7, 18.5, 2.3)), shell(circle(16.5, 18.5, 2.3)),
            shell("M4 3.5A6 6 0 0 0 10 9.6L4 3.5Z"), line(seg(7, 6.6, 10.6, 3.2)), line(seg(10, 9.6, 10, 11.5))]


@icon("razor-tool", CAT, "Blade pointing down at the gap where a timeline clip has been cut in two",
      tags=["cut tool", "blade tool", "split clip", "slice", "video editing", "cut clip"])
def _(S):
    return [shell(poly([(5, 3), (19, 3), (19, 8), (12, 10.5), (5, 8)], closed=True, r=S.r * 0.5)), detail(seg(8.5, 5.5, 15.5, 5.5)),
            shell(rect(2, 14, 8, 6, rr(S, 1.5))), shell(rect(14, 14, 8, 6, rr(S, 1.5))), line(seg(12, 12.5, 12, 21.5))]


@icon("in-out-points", CAT, "Opening and closing brackets around a highlighted span on a timeline",
      tags=["mark in", "mark out", "trim range", "selection range", "range marker", "edit points"])
def _(S):
    k = S.r * 0.3
    return [line(poly([(9, 4.5), (5, 4.5), (5, 19.5), (9, 19.5)], r=k)), line(poly([(15, 4.5), (19, 4.5), (19, 19.5), (15, 19.5)], r=k)),
            solid(rect(9.6, 10, 4.8, 4, 0.8 if S.name == "rounded" else 0)), line(seg(2, 12, 3.4, 12)), line(seg(20.6, 12, 22, 12))]


@icon("clip-trim", CAT, "Film clip block with thick handles at each end and a small arrow pushing one end inward",
      tags=["trim clip", "shorten clip", "edit handles", "trim handle", "video timeline", "ripple trim"])
def _(S):
    return [shell(rect(6.5, 9, 11, 8, rr(S, 2))), solid(rect(2.6, 6.5, 2.6, 13, 1.2 if S.name == "rounded" else 0)),
            solid(rect(18.8, 6.5, 2.6, 13, 1.2 if S.name == "rounded" else 0)), line(seg(22, 3.5, 17, 3.5)), line(head(S, (15.8, 3.5), 180, 2.2))]


@icon("freeze-frame", CAT, "Film frame with a snowflake in its centre",
      tags=["freeze", "still frame", "pause frame", "hold frame", "video still", "snapshot frame"])
def _(S):
    out = [shell(rect(2, 4, 20, 16, rr(S, 3)))]
    for a in (-90, -30, 30):
        out.append(detail(seg(*polar(12, 12, 5.4, a), *polar(12, 12, 5.4, a + 180))))
    return out
