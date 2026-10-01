"""TypeIcon Core: audio & video (media).

Media icons receive the full variant-badge set in the bottom-right corner (box 13–23), so identifying
details sit in the top half or on the left wherever the object allows.

The speaker used by the volume family is the exact v0.1 `volume` speaker, so volume-off / -low / -mute
line up with `volume` when a player swaps between them.
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, P, ST, U, arc, circle, detail, dot, ellipse, filled_region, icon, line, path_to_d, poly, pt_on, rect, regular, rotation,
    seg, shell, solid, transform_path,
)
from geometry import LINE, fmt

CAT = "media"


# --------------------------------------------------------------------------- helpers

def rnd(S, line_val, rounded_val):
    return line_val if S.name == "line" else rounded_val


def pts_d(pts):
    return "".join(("M" if i == 0 else "L") + f"{fmt(x)} {fmt(y)}" for i, (x, y) in enumerate(pts))


def arc_pts(cx, cy, r, a0, a1, n=24, ry=None):
    ry = r if ry is None else ry
    out = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        out.append((cx + r * math.cos(a), cy + ry * math.sin(a)))
    return out


def wave(xe, h, xp, cy=12.0):
    """Sound-wave arc: ends at (xe, cy ± h), bulging right to x = xp."""
    s = xp - xe
    R = (h * h + s * s) / (2 * s)
    return f"M{fmt(xe)} {fmt(cy - h)}A{fmt(R)} {fmt(R)} 0 0 1 {fmt(xe)} {fmt(cy + h)}"


def wave_pts(xe, h, xp, cy=12.0, n=16):
    s = xp - xe
    R = (h * h + s * s) / (2 * s)
    cx = xp - R
    a = math.degrees(math.asin(h / R))
    return arc_pts(cx, cy, R, -a, a, n)


def outside_band(points, closed, f, lo, hi):
    """Split a polyline into the runs where f(p) <= lo or f(p) >= hi (f linear): cut a gap along a slash."""
    pts = list(points) + ([points[0]] if closed else [])
    runs, cur = [], []
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        fa, fb = f(a), f(b)
        # parameter values where |f| crosses k
        ts = [0.0]
        for c in (lo, hi):
            if (fa - c) * (fb - c) < 0:
                ts.append((c - fa) / (fb - fa))
        ts = sorted(ts) + [1.0]
        for t0, t1 in zip(ts, ts[1:]):
            tm = (t0 + t1) / 2
            pm = (a[0] + (b[0] - a[0]) * tm, a[1] + (b[1] - a[1]) * tm)
            p0 = (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0)
            p1 = (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)
            if not (lo < f(pm) < hi):
                if not cur:
                    cur = [p0]
                cur.append(p1)
            elif cur:
                runs.append(cur)
                cur = []
    if cur:
        runs.append(cur)
    if closed and len(runs) > 1 and runs[0][0] == pts[0] and runs[-1][-1] == pts[-1]:
        runs[0] = runs[-1][:-1] + runs[0]
        runs.pop()
    return [r for r in runs if len(r) > 1]


def disc(cx, cy, r):
    return P(circle(cx, cy, r))


def solid_outline(d, miter=4.0):
    return U(P(d), ST(d, 2.0, "butt", "miter", miter))


SPK = [(4, 9), (8, 9), (13, 4.5), (13, 19.5), (8, 15), (4, 15)]  # v0.1 volume speaker
W1 = "M16.5 8.5A5 5 0 0 1 16.5 15.5"                            # v0.1 volume waves
W2 = "M19 6A8.5 8.5 0 0 1 19 18"


def speaker(S):
    return shell(poly(SPK, closed=True, r=S.r * 0.66))


# =========================================================================== music

@icon("music-note", CAT, "A single eighth note (quaver)", tags=["note", "quaver", "song", "sound", "melody", "audio"])
def _(S):
    return [shell(circle(8, 17.5, 3)), line(seg(11, 17.5, 11, 3.5)),
            line(rnd(S, "M11 3.5C12 6.8 17.5 6.8 17.5 11.5", "M11 3.5C12 6.8 17.5 6.8 17.5 11"))]


@icon("music", CAT, "Two beamed eighth notes; music or a song", tags=["song", "melody", "audio", "notes", "tune", "track"])
def _(S):
    return [shell(circle(6.5, 17.5, 2.5)), shell(circle(17.5, 15.5, 2.5)),
            line(poly([(9, 17.5), (9, 5.5), (20, 3.5), (20, 15.5)], r=S.r))]


@icon("music-notes", CAT, "Two sixteenth notes joined by a double beam", tags=["notes", "semiquaver", "melody", "song", "tune", "audio"])
def _(S):
    return [shell(circle(6.5, 17.5, 2.5)), shell(circle(17.5, 15.5, 2.5)),
            line(poly([(9, 17.5), (9, 5.5), (20, 3.5), (20, 15.5)], r=S.r)), line(seg(9, 9.5, 20, 7.5))]


@icon("headphones", CAT, "Over-ear headphones", tags=["headset", "listen", "audio", "earphones", "music", "cans"])
def _(S):
    return [line("M4 13.5V12A8 8 0 0 1 20 12V13.5"),
            shell(rect(4, 13.5, 4.5, 7.5, S.R * 0.5)), shell(rect(15.5, 13.5, 4.5, 7.5, S.R * 0.5))]


# =========================================================================== volume

@icon("volume-low", CAT, "Speaker with a single small sound wave; low volume", tags=["sound", "quiet", "audio", "speaker", "soft"])
def _(S):
    return [speaker(S), line(W1)]


@icon("volume-high", CAT, "Speaker with three sound waves; full volume", tags=["sound", "loud", "audio", "speaker", "max"], aliases=["volume-up"])
def _(S):
    spk = [(3, 9.5), (6, 9.5), (10, 6), (10, 18), (6, 14.5), (3, 14.5)]
    return [shell(poly(spk, closed=True, r=S.r * 0.66)),
            line(wave(12.5, 2.5, 13.75)), line(wave(15, 5, 17.25)), line(wave(17.5, 7.5, 21))]


@icon("volume-mute", CAT, "Speaker with a cross; sound muted", tags=["mute", "silent", "sound", "audio", "speaker", "quiet"], aliases=["volume-x"])
def _(S):
    return [speaker(S), line(seg(16, 9.5, 21, 14.5)), line(seg(21, 9.5, 16, 14.5))]


_OFF_F = lambda p: (p[1] - p[0]) / math.sqrt(2)  # noqa: E731  signed distance from the slash y = x (< 0: upper right)
_OFF_BAND = (-3.5, 0.5)  # gap only on the upper-right side of the slash, as the badge "off" reads
_SLASH = seg(3, 3, 21, 21)


def _volume_off_parts(S):
    parts = []
    for run in outside_band(SPK, True, _OFF_F, *_OFF_BAND):
        parts.append(line(poly(run, r=S.r * 0.66)))
    for run in outside_band(wave_pts(16.5, 3.5, 17.93), False, _OFF_F, *_OFF_BAND):
        parts.append(line(pts_d(run)))
    return parts + [line(_SLASH)]


def _volume_off_filled():
    body = filled_region([shell(poly(SPK, closed=True)), line(W1)])
    o = 1.375 / math.sqrt(2)  # strip on the upper-right side: slash half-width 1.25 + gap 1.5
    strip = ST(seg(3 + o, 3 - o, 21 + o, 21 - o), 2.75, "butt")
    return U(D(body, strip), ST(_SLASH, 2.5, "butt"))


@icon("volume-off", CAT, "Speaker struck through; sound off", tags=["sound off", "mute", "silent", "audio", "disabled", "speaker"],
      filled=_volume_off_filled)
def _(S):
    return _volume_off_parts(S)


@icon("radio", CAT, "Portable radio with an antenna, speaker and tuning dial", tags=["fm", "am", "broadcast", "tuner", "transistor", "audio"])
def _(S):
    return [shell(rect(3, 9, 18, 11, S.R)), line(seg(6.5, 9, 17, 3.5)),
            detail(circle(8.5, 14.5, 2.5)), detail(seg(14, 12.5, 18, 12.5)), detail(seg(14, 16.5, 18, 16.5))]


# =========================================================================== transport controls

def _record_filled():
    return U(D(disc(12, 12, 10), disc(12, 12, 7)), disc(12, 12, 5))


@icon("record", CAT, "Record button: a solid dot inside a ring", tags=["rec", "recording", "capture", "live", "button"],
      filled=_record_filled)
def _(S):
    return [shell(circle(12, 12, 9)), dot(12, 12, rnd(S, 4, 4.75))]


def _stop_sq(S):
    return rect(8.5, 8.5, 7, 7, S.R * 0.375)


@icon("stop-circle", CAT, "Stop square inside a circle", tags=["stop", "end", "halt", "media", "button"],
      filled=lambda: D(disc(12, 12, 10), P(rect(8, 8, 8, 8, 1))))
def _(S):
    return [shell(circle(12, 12, 9)), shell(_stop_sq(S))]


_PLAY_TRI = [(9.5, 7.5), (16.5, 12), (9.5, 16.5)]


@icon("play-circle", CAT, "Play triangle inside a circle", tags=["play", "start", "video", "media", "button", "resume"],
      filled=lambda: D(disc(12, 12, 10), P(poly([(9, 6.8), (17.3, 12), (9, 17.2)], closed=True))))
def _(S):
    return [shell(circle(12, 12, 9)), shell(poly(_PLAY_TRI, closed=True, r=S.r * 0.5))]


@icon("pause-circle", CAT, "Pause bars inside a circle", tags=["pause", "hold", "media", "button", "break"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(seg(10, 8.5, 10, 15.5)), detail(seg(14, 8.5, 14, 15.5))]


_SKIP_TRI = [(5, 5), (15.5, 12), (5, 19)]


def _mirror(pts):
    return [(24 - x, y) for x, y in pts]


@icon("skip-forward", CAT, "Play triangle against a bar; next track", tags=["next", "skip", "track", "forward", "media"], aliases=["next-track"])
def _(S):
    return [shell(poly(_SKIP_TRI, closed=True, r=S.r * 0.5)), line(seg(19.5, 5, 19.5, 19))]


@icon("skip-back", CAT, "Bar with a backward triangle; previous track", tags=["previous", "back", "skip", "track", "media"], aliases=["previous-track"])
def _(S):
    return [shell(poly(_mirror(_SKIP_TRI), closed=True, r=S.r * 0.5)), line(seg(4.5, 5, 4.5, 19))]


_FF = ([(3, 6), (12, 12), (3, 18)], [(12, 6), (21, 12), (12, 18)])


@icon("fast-forward", CAT, "Two forward triangles; fast forward", tags=["forward", "skip", "speed", "media", "ahead"])
def _(S):
    return [shell(poly(t, closed=True, r=S.r * 0.5)) for t in _FF]


@icon("rewind", CAT, "Two backward triangles; rewind", tags=["back", "reverse", "media", "fast backward", "backward"])
def _(S):
    return [shell(poly(_mirror(t), closed=True, r=S.r * 0.5)) for t in _FF]


@icon("playlist", CAT, "Lines of a list beside a music note; playlist or queue", tags=["queue", "tracks", "list", "songs", "music", "album"])
def _(S):
    return [line(seg(3, 6, 14, 6)), line(seg(3, 11, 13.5, 11)), line(seg(3, 16, 10, 16)),
            shell(circle(15, 17.5, 2.5)), line(poly([(17.5, 17.5), (17.5, 5.5), (21, 7)], r=S.r))]


@icon("album", CAT, "Square album sleeve holding a record", tags=["record", "lp", "cover", "music", "collection", "disc"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(circle(12, 12, 5)), dot(12, 12, 1.5)]


# =========================================================================== recorded media

@icon("vinyl", CAT, "Vinyl record with grooves and a centre label", tags=["record", "lp", "disc", "turntable", "dj", "music"], aliases=["vinyl-record"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(circle(12, 12, 2.5)),
            detail(arc(12, 12, 5.75, 195, 255)), detail(arc(12, 12, 5.75, 15, 75))]


@icon("cassette", CAT, "Audio cassette tape with two reels", tags=["tape", "mixtape", "retro", "audio", "cassette tape", "music"], aliases=["cassette-tape"])
def _(S):
    return [shell(rect(3, 5, 18, 14, S.R)), detail(circle(8.5, 10.5, 1.75)), detail(circle(15.5, 10.5, 1.75)),
            detail(poly([(7, 19), (8.5, 15.5), (15.5, 15.5), (17, 19)], r=S.r * 0.5))]


@icon("film", CAT, "Strip of film with sprocket lanes", tags=["movie", "cinema", "video", "reel", "frames", "footage"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)),
            detail(seg(7.5, 3, 7.5, 21)), detail(seg(16.5, 3, 16.5, 21)), detail(seg(7.5, 12, 16.5, 12)),
            detail(seg(3, 7.5, 7.5, 7.5)), detail(seg(3, 12, 7.5, 12)), detail(seg(3, 16.5, 7.5, 16.5)),
            detail(seg(16.5, 7.5, 21, 7.5)), detail(seg(16.5, 12, 21, 12)), detail(seg(16.5, 16.5, 21, 16.5))]


def _clapper_arm():
    a = math.radians(-12)
    u, n = (math.cos(a), math.sin(a)), (math.sin(a), -math.cos(a))
    A = (4.0, 11.0)
    L, T = 16.5, 3.75

    def at(t, h):
        return (A[0] + u[0] * t + n[0] * h, A[1] + u[1] * t + n[1] * h)
    arm = [at(0, 0), at(L, 0), at(L, T), at(0, T)]
    stripes = [seg(*at(t, 0), *at(t + 2.2, T)) for t in (4.5, 10)]
    return arm, stripes


@icon("clapperboard", CAT, "Film clapperboard with its striped arm open", tags=["clapper", "movie", "film", "director", "scene", "cinema", "take"])
def _(S):
    arm, stripes = _clapper_arm()
    return [shell(rect(3, 11, 18, 10, S.R)), shell(poly(arm, closed=True, r=S.r * 0.5)),
            *[detail(s) for s in stripes], detail(seg(3, 15, 21, 15))]


# =========================================================================== video

@icon("video", CAT, "Video camera shape: body with a lens cone; video or a recording", tags=["movie", "record", "clip", "camera", "footage", "stream"])
def _(S):
    return [shell(rect(3, 6, 12, 12, S.R)), shell(poly([(15, 10), (21, 6.5), (21, 17.5), (15, 14)], closed=True, r=S.r * 0.5))]


@icon("video-camera", CAT, "Classic movie camera with two film reels on top", tags=["movie camera", "film", "cinema", "camcorder", "shoot", "reels"])
def _(S):
    return [shell(rect(3, 12, 12, 8, S.R * 0.75)), shell(circle(6.5, 7.25, 2.75)), shell(circle(13, 7.25, 2.75)),
            shell(poly([(15, 14.5), (20.5, 12), (20.5, 20), (15, 17.5)], closed=True, r=S.r * 0.5))]


@icon("webcam", CAT, "Round webcam on a small stand", tags=["camera", "video call", "stream", "conference", "computer", "cam"])
def _(S):
    return [shell(circle(12, 10, 7)), detail(circle(12, 10, 2.5)), line(seg(12, 17, 12, 20.5)), line(seg(7, 20.5, 17, 20.5))]


@icon("tv", CAT, "Television screen with an antenna", tags=["television", "screen", "watch", "broadcast", "show", "channel"], aliases=["television"])
def _(S):
    return [shell(rect(3, 7.5, 18, 13, S.R)), line(poly([(8, 3), (12, 7.5), (16, 3)], r=S.r))]


@icon("projector", CAT, "Video projector with a large lens and feet", tags=["beamer", "presentation", "cinema", "slides", "screening"])
def _(S):
    return [shell(rect(3, 7, 18, 11, S.R)), detail(circle(8.5, 12.5, 3)), detail(seg(14.5, 10.5, 18, 10.5)), dot(16.25, 14.5, 1.1),
            line(seg(6.5, 18, 6.5, 20.5)), line(seg(17.5, 18, 17.5, 20.5))]


@icon("screen-share", CAT, "Monitor with an upward arrow; share your screen", tags=["share screen", "present", "screencast", "display", "meeting"])
def _(S):
    return [shell(rect(3, 4, 18, 13, S.R)), line(seg(12, 17, 12, 20.5)), line(seg(8, 20.5, 16, 20.5)),
            detail(seg(12, 14, 12, 8)), detail(poly([(9, 10.5), (12, 7.5), (15, 10.5)], r=S.r))]


@icon("cast", CAT, "Screen corner with broadcast arcs; cast to a device", tags=["chromecast", "stream", "airplay", "mirror", "tv", "wireless"])
def _(S):
    return [line(poly([(3, 8.5), (3, 4), (21, 4), (21, 20), (15.5, 20)], r=S.r)),
            dot(4.25, 19.75, 1.5), line(arc(4, 20, 4.75, 270, 360)), line(arc(4, 20, 9, 270, 360))]


@icon("subtitles", CAT, "Screen with lines of caption text", tags=["captions", "transcript", "text", "srt", "translation", "video"])
def _(S):
    return [shell(rect(3, 5, 18, 14, S.R)),
            detail(seg(6.5, 11, 13, 11)), detail(seg(15.5, 11, 17.5, 11)),
            detail(seg(6.5, 15, 8.5, 15)), detail(seg(11, 15, 17.5, 15))]


@icon("closed-captions", CAT, "Box with the letters CC; closed captions", tags=["cc", "captions", "subtitles", "accessibility", "deaf", "text"], aliases=["cc"])
def _(S):
    return [shell(rect(3, 5, 18, 14, S.R)), detail(arc(8.75, 12, 2.5, 45, 315)), detail(arc(15.25, 12, 2.5, 45, 315))]


# =========================================================================== audio tools

@icon("equalizer", CAT, "Three slider tracks at different levels; audio equalizer", tags=["eq", "levels", "sliders", "audio", "sound", "bass", "treble"])
def _(S):
    parts = []
    for x, y in ((5.5, 15), (12, 8), (18.5, 13)):
        parts += [line(seg(x, 3, x, y - 2.25)), line(seg(x, y + 2.25, x, 21)), shell(circle(x, y, 2.25))]
    return parts


@icon("waveform", CAT, "Audio waveform as bars of varying height", tags=["audio", "sound wave", "voice", "recording", "podcast", "signal"], aliases=["sound-wave"])
def _(S):
    return [line(seg(x, 12 - h / 2, x, 12 + h / 2)) for x, h in ((4, 4), (8, 10), (12, 17), (16, 12), (20, 5))]


@icon("metronome", CAT, "Pyramid metronome with a swinging pendulum", tags=["tempo", "beat", "rhythm", "bpm", "practice", "music"])
def _(S):
    body = [(9.5, 3), (14.5, 3), (19.5, 21), (4.5, 21)]
    return [shell(poly(body, closed=True, r=S.r * 0.66)), detail(seg(5.6, 17, 18.4, 17)),
            detail(seg(12, 17, 16.17, 8.99)), line(seg(16.17, 8.99, 18.5, 4.5))]


@icon("microphone-stand", CAT, "Stage microphone on a tripod stand", tags=["mic stand", "stage", "karaoke", "singer", "concert", "performance"])
def _(S):
    head = circle(12, 6, 3.25)
    grip = poly([(10.25, 9.75), (13.75, 9.75), (13, 13), (11, 13)], closed=True, r=S.r * 0.4)
    return [shell(head), detail(seg(8.75, 6, 15.25, 6)), shell(grip), line(seg(12, 13, 12, 18)),
            line(poly([(6.5, 21), (12, 18), (17.5, 21)], r=S.r))]


@icon("microphone-vintage", CAT, "Retro broadcast microphone in a yoke with grille bars", tags=["retro mic", "radio", "podcast", "broadcast", "studio", "old"])
def _(S):
    return [shell(rect(7.5, 3, 9, 11.5, rnd(S, 2.5, 4.5))), detail(seg(7.5, 7, 16.5, 7)), detail(seg(7.5, 10.5, 16.5, 10.5)),
            line("M4.5 8.5A7.5 7.5 0 0 0 19.5 8.5"), line(seg(12, 16, 12, 20.5)), line(seg(8, 20.5, 16, 20.5))]


@icon("loudspeaker", CAT, "Loudspeaker cabinet with a tweeter and a woofer", tags=["speaker", "hi-fi", "stereo", "sound system", "audio", "woofer"])
def _(S):
    return [shell(rect(5, 3, 14, 18, S.R)), dot(12, 7, 1.25), detail(circle(12, 14.75, 3.25))]


# =========================================================================== instruments

def rot(pts, deg, cx=12.0, cy=12.0):
    """Rotate points clockwise on screen by deg about (cx, cy)."""
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in pts]


def box(cx, cy, hl, hw, deg):
    """Rectangle centred at (cx, cy): half-length hl along the axis at deg (0 = up), half-width hw."""
    return rot([(cx - hw, cy - hl), (cx + hw, cy - hl), (cx + hw, cy + hl), (cx - hw, cy + hl)], deg, cx, cy)


def outline(path):
    return path_to_d(path)


_AX = (math.sqrt(0.5), -math.sqrt(0.5))   # guitar axis, pointing up-right
_PX = (math.sqrt(0.5), math.sqrt(0.5))    # perpendicular


def _along(c, t, p=0.0):
    return (c[0] + _AX[0] * t + _PX[0] * p, c[1] + _AX[1] * t + _PX[1] * p)


def _perp_seg(c, h):
    a, b = _along(c, 0, -h), _along(c, 0, h)
    return seg(*a, *b)


@icon("guitar", CAT, "Acoustic guitar with a round sound hole", tags=["acoustic", "strings", "instrument", "folk", "music", "band"], aliases=["acoustic-guitar"])
def _(S):
    body = outline(U(P(circle(8, 16, 4.5)), P(circle(11.75, 12.25, 3))))
    return [shell(body), detail(circle(8.75, 15.25, 1.25)),
            line(seg(13.8, 10.2, 17.3, 6.7)), shell(poly(box(18.6, 5.4, 1.9, 1.25, 45), closed=True, r=S.r * 0.4))]


@icon("electric-guitar", CAT, "Electric guitar with a cutaway body and two pickups", tags=["rock", "strings", "instrument", "band", "amp", "music"])
def _(S):
    horn = transform_path(P(ellipse(12.2, 11.2, 1.6, 3.4)), rotation(45))
    horn2 = transform_path(P(ellipse(8.4, 11.4, 1.5, 2.6)), rotation(20, 8.4, 11.4))
    body = outline(U(P(circle(8, 16, 4.5)), horn, horn2))
    return [shell(body), detail(_perp_seg((9.4, 14.6), 1.6)), detail(_perp_seg((6.9, 17.1), 1.6)),
            line(seg(12.6, 11.4, 17.3, 6.7)),
            shell(poly(rot([(17.4, 7.2), (17.4, 3.2), (19.8, 2.6), (19.8, 7.2)], 45, 18.6, 5.2), closed=True, r=S.r * 0.4))]


def _piano_filled():
    body = P(rect(2, 4, 20, 16, 2))
    cuts = []
    for x in (7.5, 12, 16.5):
        cuts.append(ST(poly([(x - 2, 5.5), (x - 2, 13.25), (x + 2, 13.25), (x + 2, 5.5)]), 1.5))
        cuts.append(ST(seg(x, 13.25, x, 18.5), 1.5))
    return D(body, *cuts)


@icon("piano", CAT, "Piano keyboard with black and white keys", tags=["keyboard", "keys", "instrument", "classical", "synth", "music"],
      filled=_piano_filled)
def _(S):
    parts = [shell(rect(3, 5, 18, 14, S.R))]
    for x in (7.5, 12, 16.5):
        parts += [solid(rect(x - 1.25, 5, 2.5, 7.5, rnd(S, 0, 0.6))), detail(seg(x, 12.5, x, 19))]
    return parts


@icon("drum", CAT, "Snare drum with crossed drumsticks", tags=["percussion", "snare", "beat", "drummer", "instrument", "rhythm"])
def _(S):
    return [shell("M4 10A8 3 0 0 1 20 10V17A8 3 0 0 1 4 17Z"), detail("M4 10A8 3 0 0 0 20 10"),
            detail(poly([(8, 12.6), (12, 20), (16, 12.6)], r=S.r)),
            line(seg(9.5, 8, 4.5, 3)), line(seg(14.5, 8, 19.5, 3))]


@icon("trumpet", CAT, "Trumpet with three valves and a flared bell", tags=["brass", "horn", "jazz", "fanfare", "instrument", "band"])
def _(S):
    return [line(seg(3, 10, 16, 10)), line(seg(3, 8, 3, 12)),
            shell(poly([(16, 9), (21, 5.5), (21, 14.5), (16, 11)], closed=True, r=S.r * 0.5)),
            line(poly([(7, 10), (7, 15), (14, 15), (14, 10)], r=S.r)),
            *[line(seg(x, 5, x, 10)) for x in (7, 10.5, 14)]]


@icon("violin", CAT, "Violin with f-holes, neck and scroll", tags=["fiddle", "strings", "classical", "orchestra", "instrument", "bow"], aliases=["fiddle"])
def _(S):
    body = ("M12 8.5C9.5 8.5 8 9.5 8 11.5C8 12.8 9.3 13.2 9.3 14.2C9.3 15.2 7 15.8 7 18C7 20 9.3 21 12 21"
            "C14.7 21 17 20 17 18C17 15.8 14.7 15.2 14.7 14.2C14.7 13.2 16 12.8 16 11.5C16 9.5 14.5 8.5 12 8.5Z")
    return [shell(body), detail(seg(10, 15.75, 10, 18.5)), detail(seg(14, 15.75, 14, 18.5)), detail(seg(12, 8.5, 12, 13)),
            line("M12 8.5V4.5C12 3.3 13 2.7 14 3.2" if S.name == "rounded" else "M12 8.5V3H14"),
            line(seg(10.25, 5.75, 13.75, 5.75))]


@icon("saxophone", CAT, "Saxophone: curved body, flared bell and angled mouthpiece", tags=["sax", "jazz", "woodwind", "brass", "instrument", "blues"], aliases=["sax"])
def _(S):
    tube = ST("M9.5 6.5V15.5A3.75 3.75 0 0 0 17 15.5V13.5", 4.5, "butt", "miter")
    bell = P(poly([(14.75, 14), (14, 9.5), (21, 7.5), (19.25, 14)], closed=True))
    return [shell(outline(U(tube, bell))), line("M9.5 6.5C9.5 4.5 8.2 3.5 5 3.5"),
            dot(9.5, 10, 1), dot(9.5, 13.5, 1)]


@icon("flute", CAT, "Transverse flute with finger holes", tags=["woodwind", "orchestra", "classical", "pipe", "instrument", "wind"])
def _(S):
    tube = box(12, 12, 10.5, 2, 45)
    parts = [shell(poly(tube, closed=True, r=S.r * 0.5))]
    for t in (-6, -3, 0, 3):
        parts.append(dot(12 + _AX[0] * t, 12 + _AX[1] * t, 0.9))
    parts.append(detail(_perp_seg(_along((12, 12), 6.5), 2)))
    return parts


def _harp_parts(S):
    frame = "M5 4V20.5H9L19.5 8C18.5 5.5 16 4.5 13.5 5.5C11 6.5 8 6.5 5 4Z"
    strings = [(9.5, 6.3, 19.9), (13, 5.3, 15.7), (16.5, 4.9, 11.6)]
    return [shell(frame, stroke_miterlimit="2"), *[detail(seg(x, a, x, b)) for x, a, b in strings]]


@icon("harp", CAT, "Concert harp: frame with vertical strings", tags=["strings", "orchestra", "angel", "classical", "instrument", "celtic"])
def _(S):
    return _harp_parts(S)


@icon("tambourine", CAT, "Tambourine: round frame with metal jingles", tags=["percussion", "jingle", "shake", "instrument", "rhythm", "folk"])
def _(S):
    R, r, n = 7.75, 1.75, 5
    parts = []
    gap = math.degrees(2 * math.asin(r / (2 * R)))
    for i in range(n):
        a = -90 + i * 360 / n
        x, y = pt_on(12, 12, R, a)
        parts.append(shell(circle(x, y, r)))
        if S.name == "rounded":  # jingles sit in gaps of the frame
            parts.append(line(arc(12, 12, R, a + gap, a + 360 / n - gap)))
    if S.name == "line":  # crisp: the frame runs through each jingle
        parts.append(line(circle(12, 12, R)))
    return parts


@icon("xylophone", CAT, "Xylophone bars with a mallet", tags=["glockenspiel", "percussion", "mallet", "bars", "instrument", "kids"])
def _(S):
    bars = [line(seg(x, 13 - h / 2, x, 13 + h / 2)) for x, h in ((3.5, 16), (7.5, 13), (11.5, 10), (15.5, 7))]
    return bars + [line(seg(21, 3, 19.6, 4.9)), shell(circle(18.5, 6.5, 1.75))]


@icon("accordion-instrument", CAT, "Accordion with pleated bellows between two keyboards", tags=["accordion", "squeezebox", "bellows", "folk", "instrument", "polka"], aliases=["squeezebox"])
def _(S):
    top = [(7.5, 5.5), (9.75, 3.5), (12, 5.5), (14.25, 3.5), (16.5, 5.5)]
    bot = [(x, 24 - y) for x, y in top]
    return [shell(rect(3, 5, 4.5, 14, S.R * 0.5)), shell(rect(16.5, 5, 4.5, 14, S.R * 0.5)),
            line(poly(top, r=S.r * 0.5)), line(poly(bot, r=S.r * 0.5)),
            line(seg(9.75, 3.5, 9.75, 20.5)), line(seg(14.25, 3.5, 14.25, 20.5)), line(seg(12, 5.5, 12, 18.5)),
            dot(5.25, 9, 1), dot(5.25, 12, 1), dot(5.25, 15, 1)]


@icon("bell-music", CAT, "Hand bell with a wooden handle", tags=["handbell", "chime", "ring", "instrument", "choir", "bell"], aliases=["handbell"])
def _(S):
    bell = "M5 17.5C7 16.5 7 14.5 7.3 12.5C7.8 9.8 9.5 8.5 12 8.5C14.5 8.5 16.2 9.8 16.7 12.5C17 14.5 17 16.5 19 17.5Z"
    return [shell(bell, stroke_miterlimit="2"), shell(rect(10.5, 2.5, 3, 4, rnd(S, 0.5, 1.5))), dot(12, 20.5, 1.5)]


# =========================================================================== audio gear

_MIX = ((7.5, 15), (12, 12.5), (16.5, 14))


def _mixer_filled():
    body = P(rect(2, 2, 20, 20, 2))
    cuts = []
    for x, y in _MIX:
        cuts += [P(circle(x, 7, 1.5)), ST(seg(x, 10.5, x, 18), 1.5), P(rect(x - 2, y - 1, 4, 2))]
    return D(body, *cuts)


@icon("mixer", CAT, "Mixing desk with knobs and faders", tags=["mixing console", "dj", "audio", "studio", "faders", "sound desk"],
      aliases=["mixing-console"], filled=_mixer_filled)
def _(S):
    parts = [shell(rect(3, 3, 18, 18, S.R))]
    for x, y in _MIX:
        parts += [dot(x, 7, 1.25), detail(seg(x, 10.5, x, 18)), detail(seg(x - 1.75, y, x + 1.75, y))]
    return parts


@icon("turntable", CAT, "Record turntable with platter and tone arm", tags=["record player", "dj", "vinyl", "deck", "phonograph", "music"], aliases=["record-player"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(circle(10, 12, 4.5)), dot(10, 12, 1.1),
            dot(17.5, 6.5, 1.25), detail(poly([(17.5, 6.5), (17.5, 14.5), (15.25, 16.75)], r=S.r))]


@icon("boombox", CAT, "Portable stereo boombox with two speakers and a handle", tags=["ghetto blaster", "stereo", "radio", "cassette", "retro", "music"])
def _(S):
    return [shell(rect(3, 8.5, 18, 11, S.R)), line(poly([(6.5, 8.5), (6.5, 4.5), (17.5, 4.5), (17.5, 8.5)], r=S.r)),
            detail(circle(8, 14.25, 2.25)), detail(circle(16, 14.25, 2.25)), detail(seg(10.75, 10.75, 13.25, 10.75))]


@icon("mp3-player", CAT, "Portable music player with a screen and click wheel", tags=["ipod", "music player", "walkman", "portable", "audio"], aliases=["music-player"])
def _(S):
    return [shell(rect(6, 3, 12, 18, S.R)), detail(rect(9, 6, 6, 4, S.R * 0.25)), detail(circle(12, 16, 2.5))]


# =========================================================================== cinema

@icon("movie-reel", CAT, "Film reel with spoke holes and a loose tail of film", tags=["film reel", "cinema", "movie", "footage", "projector", "reel"])
def _(S):
    parts = [shell(circle(11, 11, 8)), dot(11, 11, 1.1)]
    for i in range(5):
        parts.append(detail(circle(*pt_on(11, 11, 4.4, -90 + 72 * i), 1.4)))
    parts.append(line(seg(11, 19, 21, 19)))
    return parts


@icon("popcorn-movie", CAT, "Striped popcorn bucket for the cinema", tags=["popcorn", "cinema", "snack", "movie night", "theatre"])
def _(S):
    puffs = U(P(circle(7.5, 8.5, 2.75)), P(circle(12, 6.5, 3.25)), P(circle(16.5, 8.5, 2.75)), P(rect(5, 8.5, 14, 2)))
    bucket = P(poly([(5, 10), (19, 10), (17, 21), (7, 21)], closed=True))
    return [shell(outline(U(puffs, bucket))), detail(seg(4.9, 10, 19.1, 10)),
            detail(seg(10.25, 10, 10.75, 21)), detail(seg(13.75, 10, 13.25, 21))]


_TKT_TRI = [(8, 9.5), (12, 12), (8, 14.5)]


def _ticket_parts(S):
    body = D(P(rect(3, 6, 18, 12, S.R * 0.5)), P(circle(3, 12, 2)), P(circle(21, 12, 2)))
    return [shell(outline(body)), detail(seg(15.5, 6, 15.5, 8.5)), detail(seg(15.5, 10.75, 15.5, 13.25)), detail(seg(15.5, 15.5, 15.5, 18))]


@icon("ticket-movie", CAT, "Cinema ticket with a play symbol and a tear-off stub",
      tags=["cinema ticket", "admission", "movie", "admit one", "film", "show"],
      filled=lambda: D(filled_region(_ticket_parts(LINE)), P(poly([(7.5, 8.6), (13, 12), (7.5, 15.4)], closed=True))))
def _(S):
    return _ticket_parts(S) + [shell(poly(_TKT_TRI, closed=True, r=S.r * 0.4))]
