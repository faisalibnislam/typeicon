"""TypeIcon Core: appliances (batch 003): home audio and video, smart home devices and small household machines.

Drawn from the objects themselves, front or side views, simple boxes with one or two telling features.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar  # noqa: F401


def pt_on(cx, cy, r, deg):
    return polar(cx, cy, r, deg)

CAT = "appliances"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def waves(cx, cy, radii, a0, a1):
    return [line(arc(cx, cy, r, a0, a1)) for r in radii]


# ============================================================================ home audio

@icon("soundbar", CAT, "Long slim soundbar speaker under a TV screen",
      tags=["sound bar", "tv speaker", "home audio", "speaker", "home cinema", "audio"])
def _(S):
    return [
        shell(rect(4, 3, 16, 7, rr(S, 2.5))),
        shell(rect(2, 13, 20, 7, rr(S, 3))),
        dot(6, 16.5, 1), dot(10, 16.5, 1), dot(14, 16.5, 1), dot(18, 16.5, 1),
    ]


@icon("subwoofer", CAT, "Cube subwoofer box with one large woofer cone",
      tags=["sub", "bass speaker", "woofer", "bass", "home audio", "speaker"])
def _(S):
    return [
        shell(rect(3, 3, 18, 16, rr(S, 3))),
        detail(circle(12, 11, 4.5)),
        dot(12, 11, 1.4),
        line(seg(6.5, 19, 6.5, 21.5)), line(seg(17.5, 19, 17.5, 21.5)),
    ]


@icon("av-receiver", CAT, "Wide AV receiver with a display and a large volume knob",
      tags=["receiver", "amplifier", "home theater", "hi-fi", "surround", "audio video"])
def _(S):
    return [
        shell(rect(2, 6, 20, 12, rr(S, 2.5))),
        detail(seg(5.5, 10, 11.5, 10)),
        dot(6, 14, 1), dot(9.5, 14, 1),
        detail(circle(16.5, 12, 2.25)),
    ]


@icon("stereo-amplifier", CAT, "Low stereo amplifier with two knobs and a VU meter window",
      tags=["amplifier", "amp", "hi-fi", "stereo", "integrated amplifier", "audio"])
def _(S):
    return [
        shell(rect(2, 5, 20, 14, rr(S, 2.5))),
        detail(arc(12, 13.5, 4.5, 205, 335)),
        detail(seg(12, 13.5, 14, 10)),
        dot(5.75, 15.5, 1.6), dot(18.25, 15.5, 1.6),
    ]


@icon("hifi-system", CAT, "Mini hi-fi system: a centre unit with a display between two speakers",
      tags=["hi-fi", "stereo system", "music system", "micro system", "speakers", "audio"], aliases=["stereo-system"])
def _(S):
    return [
        shell(rect(8.5, 3, 7, 18, rr(S, 2))),
        detail(seg(10.5, 7, 13.5, 7)),
        detail(seg(8.5, 11, 15.5, 11)),
        dot(12, 15.5, 1.1),
        shell(rect(2, 9, 4.5, 12, rr(S, 1.5))),
        shell(rect(17.5, 9, 4.5, 12, rr(S, 1.5))),
    ]


@icon("tower-speaker", CAT, "Tall floor-standing speaker with a tweeter and two woofers",
      tags=["floorstanding speaker", "floor speaker", "column speaker", "hi-fi", "loudspeaker", "audio"], aliases=["floorstanding-speaker"])
def _(S):
    return [
        shell(rect(7, 2, 10, 19, rr(S, 3))),
        dot(12, 5.5, 1),
        detail(circle(12, 10.25, 1.75)),
        detail(circle(12, 16.25, 1.75)),
    ]


@icon("portable-speaker", CAT, "Portable wireless speaker lying on its side with a carry strap",
      tags=["bluetooth speaker", "wireless speaker", "outdoor speaker", "travel speaker", "audio", "music"])
def _(S):
    return [
        shell(rect(2, 8.5, 14, 11, L(S, 3, 5.5))),
        detail(seg(5.5, 8.5, 5.5, 19.5)), detail(seg(12.5, 8.5, 12.5, 19.5)),
        dot(9, 14, 1),
        line(arc(16, 14, 3.5, -40, 40)), line(arc(16, 14, 7, -40, 40)),
    ]


@icon("surround-sound", CAT, "Listener in the middle with four speakers sending sound inward",
      tags=["surround", "5.1", "home theater", "spatial audio", "speakers", "sound"])
def _(S):
    k = L(S, 0, 0.75)
    return [
        shell(circle(12, 12, 2)),
        sq(2.5, 2.5, 4, 4, k), sq(17.5, 2.5, 4, 4, k), sq(2.5, 17.5, 4, 4, k), sq(17.5, 17.5, 4, 4, k),
        line(arc(4.5, 4.5, 5, 25, 65)), line(arc(19.5, 4.5, 5, 115, 155)),
        line(arc(4.5, 19.5, 5, 295, 335)), line(arc(19.5, 19.5, 5, 205, 245)),
    ]


# ============================================================================ players and recorders

@icon("cd-player", CAT, "CD player with its disc tray slid out holding a disc",
      tags=["compact disc player", "disc player", "hi-fi", "cd", "music", "audio"])
def _(S):
    return [
        shell(rect(2, 3, 20, 7, rr(S, 2))),
        detail(seg(5.5, 6.5, 9.5, 6.5)),
        dot(18, 6.5, 1),
        shell(poly([(5, 13), (19, 13), (21.5, 20.5), (2.5, 20.5)], closed=True, r=S.r * 0.5)),
        detail(ellipse(12, 16.75, 4.5, 1.75)),
    ]


@icon("cassette-deck", CAT, "Hi-fi cassette deck with a tape window and transport buttons",
      tags=["tape deck", "cassette player", "tape recorder", "hi-fi", "cassette", "audio"], aliases=["tape-deck"])
def _(S):
    return [
        shell(rect(2, 5, 20, 14, rr(S, 2.5))),
        detail(rect(5, 8, 9, 8, L(S, 0.5, 1.5))),
        dot(7.75, 12, 1), dot(11.25, 12, 1),
        detail(seg(16.5, 9, 18.5, 9)),
        dot(17.5, 12.5, 0.9), dot(17.5, 15.5, 0.9),
    ]


@icon("reel-to-reel", CAT, "Reel-to-reel tape recorder with two large reels and tape between them",
      tags=["tape recorder", "open reel", "magnetic tape", "studio", "vintage audio", "recording"])
def _(S):
    return [
        shell(circle(6.5, 7, 3.5)), dot(6.5, 7, 1.1),
        shell(circle(17.5, 7, 3.5)), dot(17.5, 7, 1.1),
        line(poly([(9, 10.5), (12, 13.5), (15, 10.5)], r=S.r)),
        shell(rect(2, 15, 20, 6, rr(S, 3))),
        dot(9, 18, 0.9), dot(15, 18, 0.9),
    ]


@icon("gramophone", CAT, "Wind-up gramophone with a flared horn over its box and a crank",
      tags=["phonograph", "wind up record player", "record player", "vintage", "antique", "music"], aliases=["phonograph"])
def _(S):
    horn = "M8.4 13.4Q12 9 12.3 3.3A5.2 2.4 45 0 1 20.7 11.7Q15 12 9.6 14.6Z"
    return [
        shell(horn),
        line(seg(9, 13.5, 9, 16)),
        shell(rect(3, 16, 12, 5, rr(S, 1.5))),
        line(poly([(15, 18.5), (18.5, 18.5), (18.5, 21)], r=S.r * 0.6)),
    ]


@icon("jukebox", CAT, "Arched jukebox cabinet with a curved window, buttons and a grille",
      tags=["juke box", "diner", "retro", "coin operated", "music machine", "records"])
def _(S):
    top = "A7.5 7.5 0 0 1 19.5 10.5"
    body = ("M4.5 21V10.5" + top + "V21Z") if S.name == "line" else ("M6.5 21A2 2 0 0 1 4.5 19V10.5" + top + "V19A2 2 0 0 1 17.5 21Z")
    return [
        shell(body),
        detail("M8 11A4 4 0 0 1 16 11Z"),
        dot(9, 14.5, 0.9), dot(12, 14.5, 0.9), dot(15, 14.5, 0.9),
        detail(seg(8, 18, 16, 18)),
    ]


@icon("karaoke-machine", CAT, "Karaoke speaker box with a screen and a corded microphone",
      tags=["karaoke", "sing along", "microphone", "party", "singing", "speaker"])
def _(S):
    return [
        shell(rect(2.5, 3, 11, 18, rr(S, 2))),
        detail(rect(5, 5.5, 6, 3.5, L(S, 0, 1))),
        detail(circle(8, 15, 2.75)),
        shell(circle(19, 5, 2.25)),
        line(seg(19, 7.5, 19, 12)),
        line("M19 12C19 17.5 17.5 18 13.5 18"),
    ]


# ============================================================================ video

@icon("vcr", CAT, "Video cassette recorder with a tape flap and a clock display",
      tags=["video recorder", "vhs player", "video cassette recorder", "vintage", "tape", "retro"], aliases=["video-recorder"])
def _(S):
    return [
        shell(rect(2, 7, 20, 10, rr(S, 2.5))),
        detail(rect(5, 10, 8, 2.5, L(S, 0, 1))),
        detail(seg(15.5, 10.5, 18.5, 10.5)),
        dot(16, 14, 0.9), dot(18.5, 14, 0.9),
    ]


@icon("videotape", CAT, "VHS video cassette with a reel window and a label strip",
      tags=["vhs", "video cassette", "tape", "vhs tape", "home video", "retro"], aliases=["video-cassette"])
def _(S):
    return [
        shell(rect(2, 5, 20, 14, rr(S, 2))),
        detail(rect(5.5, 8, 13, 5.5, L(S, 0, 1.5))),
        dot(9, 10.75, 1.25), dot(15, 10.75, 1.25),
        detail(seg(6, 16, 18, 16)),
    ]


@icon("dvd-player", CAT, "Slim DVD player with a disc going into its slot and a display",
      tags=["dvd", "blu ray", "disc player", "video player", "home cinema", "movie"])
def _(S):
    return [
        line(arc(8, 13, 5, 180, 360)),
        line(arc(8, 13, 1.5, 180, 360)),
        shell(rect(2, 13, 20, 6, rr(S, 2.5))),
        detail(seg(14.5, 16, 18.5, 16)),
    ]


@icon("set-top-box", CAT, "Set-top box with a channel display beside its remote control",
      tags=["cable box", "tv box", "satellite receiver", "decoder", "digital tv", "television"], aliases=["cable-box"])
def _(S):
    return [
        shell(rect(2, 9, 12, 8, rr(S, 2.5))),
        detail(rect(5, 11.5, 5.5, 3, L(S, 0, 1))),
        shell(rect(17, 5, 5, 16, rr(S, 2))),
        dot(19.5, 8.5, 1), dot(19.5, 12.25, 0.8), dot(19.5, 15.25, 0.8),
    ]


def _stick(S):
    body = rect(9, 7, 12.5, 10, rr(S, 3))
    plug = poly([(2.5, 9.5), (9.5, 9.5), (9.5, 14.5), (4, 14.5), (2.5, 13)], closed=True)
    return path_to_d(U(P(body), P(plug)))


@icon("streaming-stick", CAT, "HDMI streaming stick with its plug and a play symbol",
      tags=["media stick", "tv stick", "dongle", "hdmi dongle", "streaming device", "smart tv"])
def _(S):
    return [
        shell(_stick(S)),
        detail(poly([(13.5, 9.5), (17.5, 12), (13.5, 14.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("tv-antenna", CAT, "Indoor rabbit-ear TV antenna with two rods in a V on a base",
      tags=["rabbit ears", "indoor antenna", "tv aerial", "dipole", "reception", "broadcast"], aliases=["rabbit-ears"])
def _(S):
    base = ("M5 20.5A7 5.5 0 0 1 19 20.5Z" if S.name == "line" else "M6 20.5A1 1 0 0 1 5 19.5A7 5 0 0 1 19 19.5A1 1 0 0 1 18 20.5Z")
    return [
        shell(base),
        line(seg(10, 14.5, 5, 4)), line(seg(14, 14.5, 19, 4)),
        dot(5, 3.5, 1.5), dot(19, 3.5, 1.5),
    ]


@icon("roof-aerial", CAT, "Rooftop Yagi TV aerial: a boom with crosswise elements on a mast",
      tags=["tv aerial", "yagi antenna", "rooftop antenna", "outdoor antenna", "reception", "broadcast"], aliases=["yagi-antenna"])
def _(S):
    return [
        line(seg(2.5, 8, 21.5, 8)),
        line(seg(4, 3, 4, 13)), line(seg(8.5, 4, 8.5, 12)), line(seg(15.5, 5, 15.5, 11)), line(seg(20, 5.5, 20, 10.5)),
        line(seg(12, 8, 12, 21.5)),
        line(poly([(7, 21.5), (12, 18), (17, 21.5)], r=S.r)),
    ]


@icon("home-theater", CAT, "Home cinema: a wide screen with speakers and a sofa in front",
      tags=["home cinema", "movie room", "media room", "tv room", "surround sound", "entertainment"], aliases=["home-cinema"])
def _(S):
    sofa = [(3.5, 21), (3.5, 15.5), (7, 15.5), (7, 13.5), (17, 13.5), (17, 15.5), (20.5, 15.5), (20.5, 21)]
    return [
        shell(rect(6, 3, 12, 8, rr(S, 1.5))),
        sq(2, 4, 2.5, 7, L(S, 0, 1)), sq(19.5, 4, 2.5, 7, L(S, 0, 1)),
        shell(poly(sofa, closed=True, r=S.r * 0.6)),
        detail(seg(7, 15.5, 7, 21)), detail(seg(17, 15.5, 17, 21)), detail(seg(7, 18, 17, 18)),
    ]


@icon("tv-wall-mount", CAT, "Flat TV seen from the side on a folding wall-mount arm",
      tags=["tv bracket", "wall bracket", "articulating mount", "swivel mount", "tv mount", "installation"], aliases=["tv-bracket"])
def _(S):
    return [
        line(seg(3, 2, 3, 22)),
        line(poly([(4, 15), (9, 10), (13, 14.5)], r=S.r)),
        dot(9, 10, 1.5),
        shell(rect(15, 3, 4, 18, rr(S, 1.5))),
    ]


@icon("digital-photo-frame", CAT, "Digital photo frame on a stand showing a mountain and sun",
      tags=["photo frame", "picture frame", "digital frame", "slideshow", "photos", "display"], aliases=["digital-picture-frame"])
def _(S):
    return [
        shell(rect(2, 3, 20, 15, rr(S, 2.5))),
        detail(poly([(5, 15), (10, 9.5), (13.5, 13), (15.5, 11), (19, 15)], r=S.r * 0.6)),
        dot(16, 7, 1.5),
        line(seg(8, 18, 6.5, 21.5)), line(seg(16, 18, 17.5, 21.5)),
    ]


def _discman(S):
    return path_to_d(U(P(circle(11, 10, 8)), P(rect(3, 10, 16, 9, rr(S, 3)))))


@icon("portable-cd-player", CAT, "Round portable CD player with a disc window and a headphone cord",
      tags=["portable cd", "personal cd player", "walkman", "cd", "music", "retro"], aliases=["personal-cd-player"])
def _(S):
    return [
        shell(_discman(S)),
        detail(circle(11, 10, 3.5)),
        dot(11, 10, 1),
        dot(8, 16, 0.9), dot(11, 16, 0.9), dot(14, 16, 0.9),
        line("M19 14C21.5 14 21.5 17 21.5 21.5"),
    ]


@icon("portable-cassette-player", CAT, "Pocket cassette player with a tape window and a headphone cord",
      tags=["personal stereo", "pocket tape player", "tape player", "cassette", "music", "retro"], aliases=["personal-stereo"])
def _(S):
    return [
        shell(rect(3, 7, 13, 14, rr(S, 2.5))),
        detail(rect(5.5, 10, 8, 5, L(S, 0, 1.5))),
        dot(8, 12.5, 1), dot(11, 12.5, 1),
        sq(5, 4, 2.5, 2, L(S, 0, 0.75)), sq(9, 4, 2.5, 2, L(S, 0, 0.75)),
        line("M14 7C14 3 20 2.5 20 7V21.5"),
    ]


@icon("cordless-phone", CAT, "Cordless phone handset with a keypad standing in its charging cradle",
      tags=["home phone", "landline", "dect phone", "handset", "telephone", "base station"], aliases=["dect-phone"])
def _(S):
    return [
        line(seg(15, 4, 15, 1.75)),
        shell(rect(8, 4, 8, 13.5, rr(S, 2.5))),
        detail(seg(10.5, 6.75, 13.5, 6.75)),
        dot(10.5, 10, 0.85), dot(13.5, 10, 0.85), dot(10.5, 12.5, 0.85), dot(13.5, 12.5, 0.85),
        dot(10.5, 15, 0.85), dot(13.5, 15, 0.85),
        line(poly([(5, 14.5), (5, 20.5), (19, 20.5), (19, 14.5)], r=S.r)),
    ]


@icon("baby-monitor", CAT, "Baby monitor: a parent unit with a screen next to a round camera",
      tags=["baby camera", "nursery monitor", "baby cam", "child monitor", "parenting", "nursery"])
def _(S):
    return [
        line(seg(4.5, 8, 4.5, 3.5)),
        shell(rect(3, 8, 9, 13, rr(S, 2))),
        detail(rect(5.5, 10.5, 4, 4, L(S, 0, 1))),
        dot(7.5, 18, 0.9),
        shell(circle(17.5, 10, 3.75)),
        dot(17.5, 10, 1.3),
        line(seg(17.5, 14.75, 17.5, 20.5)),
        line(seg(14.5, 20.5, 20.5, 20.5) if S.name == "line" else seg(15, 20.5, 20, 20.5)),
    ]


@icon("weather-station", CAT, "Home weather station display with a sun and cloud beside an outdoor sensor",
      tags=["weather", "forecast", "thermometer", "barometer", "outdoor sensor", "climate"])
def _(S):
    cloud = "M6.25 14.5H11.25A2 2 0 0 0 11.25 10.5A3 3 0 0 0 5.6 11.6A1.5 1.5 0 0 0 6.25 14.5Z"
    return [
        shell(rect(2, 3, 13, 18, rr(S, 2.5))),
        Part("dot", cloud),
        dot(11.5, 7, 1.25),
        detail(seg(5, 18, 11.5, 18)),
        shell(rect(18, 8, 4, 10, rr(S, 1.5))),
        line(seg(20, 8, 20, 4.5)),
    ]


def _drop(cx, top, h, S):
    """Water drop: pointed tip (Line) or softened tip (Rounded), round bottom."""
    r = h * 0.38
    cy = top + h - r
    a = math.asin(r / (h - r))
    rx, ry = cx + r * math.cos(a), cy - r * math.sin(a)
    lx = cx - r * math.cos(a)
    arc_ = f"A{fmt(r)} {fmt(r)} 0 1 1 {fmt(lx)} {fmt(ry)}"
    if S.name == "line":
        return f"M{fmt(cx)} {fmt(top)}L{fmt(rx)} {fmt(ry)}" + arc_ + "Z"
    t = 0.3
    ax, ay = cx + t * (lx - cx), top + t * (ry - top)
    bx, by = cx + t * (rx - cx), top + t * (ry - top)
    return f"M{fmt(ax)} {fmt(ay)}Q{fmt(cx)} {fmt(top)} {fmt(bx)} {fmt(by)}L{fmt(rx)} {fmt(ry)}" + arc_ + "Z"


@icon("hygrometer", CAT, "Round humidity gauge with a needle and a water drop",
      tags=["humidity meter", "humidity", "moisture", "gauge", "damp", "indoor climate"], aliases=["humidity-gauge"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(seg(12, 11, L(S, 7.5, 8), 7)),
        dot(12, 11, 1.5),
        Part("dot", _drop(12, 13.5, 5, S)),
    ]


# ============================================================================ networking and smart home

@icon("air-quality-monitor", CAT, "Air quality monitor with a wavy air line and a level bar on its display",
      tags=["air quality", "air monitor", "co2 monitor", "pollution", "indoor air", "sensor"])
def _(S):
    return [
        shell(rect(3, 4, 18, 16, rr(S, 4))),
        detail("M6.5 10.5C8 8.5 9.5 8.5 10.75 10.5S13.5 12.5 14.75 10.5S16.5 8.5 17.5 9.5"),
        detail(seg(6.5, 15.5, 12.5, 15.5)),
        dot(16.5, 15.5, 1.1),
    ]


@icon("mesh-wifi", CAT, "Three mesh Wi-Fi units linked by dotted lines with a signal arc",
      tags=["mesh network", "mesh router", "whole home wifi", "wifi system", "wireless", "network"])
def _(S):
    k = L(S, 1.5, 2.5)
    return [
        line(arc(12, 9.5, 5.5, 225, 315)),
        shell(rect(9.5, 7.5, 5, 5, k)),
        shell(rect(2.5, 16, 5, 5, k)), shell(rect(16.5, 16, 5, 5, k)),
        dot(9, 15, 0.9), dot(15, 15, 0.9), dot(12, 18.5, 0.9),
    ]


@icon("wifi-extender", CAT, "Plug-in Wi-Fi extender with two antennas and signal arcs",
      tags=["wifi repeater", "range extender", "wifi booster", "signal booster", "wireless", "network"], aliases=["wifi-repeater", "range-extender"])
def _(S):
    return [
        line(arc(12, 11, 4, 225, 315)), line(arc(12, 11, 7.5, 225, 315)),
        shell(rect(6.5, 11.5, 11, 8, rr(S, 3))),
        dot(12, 15.5, 1.1),
        line(seg(10, 19.5, 10, 22)), line(seg(14, 19.5, 14, 22)),
    ]


def _port(x, y):
    return Part("dot", poly([(x, y), (x + 3, y), (x + 3, y + 2.5), (x + 2.2, y + 2.5), (x + 2.2, y + 3.2),
                             (x + 0.8, y + 3.2), (x + 0.8, y + 2.5), (x, y + 2.5)], closed=True))


@icon("network-switch", CAT, "Network switch: a flat box with a row of Ethernet ports and lights",
      tags=["ethernet switch", "lan switch", "switch", "networking", "hub", "ports"], aliases=["ethernet-switch"])
def _(S):
    xs = (4.75, 8.75, 12.75, 16.75)
    return [
        shell(rect(2, 6.5, 20, 11, rr(S, 3))),
        *[dot(x + 1.5, 9.5, 0.7) for x in xs],
        *[_port(x, 12) for x in xs],
    ]


@icon("nas-drive", CAT, "Small NAS tower with two drive bays and status lights",
      tags=["nas", "network storage", "file server", "home server", "backup", "storage"], aliases=["network-attached-storage"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 3))),
        detail(rect(6.5, 5, 4, 10.5, L(S, 0, 1))), detail(rect(13.5, 5, 4, 10.5, L(S, 0, 1))),
        dot(8.5, 18.5, 1), dot(15.5, 18.5, 1),
    ]


@icon("smart-hub", CAT, "Smart home hub with a central light ring and signal arcs",
      tags=["home hub", "iot hub", "bridge", "smart home", "home automation", "controller"], aliases=["home-hub"])
def _(S):
    return [
        shell(rect(6.5, 6.5, 11, 11, L(S, 2.5, 4.5))),
        detail(circle(12, 12, 2.25)),
        line(arc(12, 12, 9, -35, 35)), line(arc(12, 12, 9, 145, 215)),
    ]


@icon("smart-display", CAT, "Smart display: a tabletop screen with a weather widget on a speaker base",
      tags=["smart screen", "home display", "voice assistant", "smart home", "screen", "kitchen display"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 11.5, rr(S, 2.5))),
        dot(7.5, 8.75, 2),
        detail(seg(12, 7.5, 18, 7.5)), detail(seg(12, 11, 16, 11)),
        shell(rect(6, 17.5, 12, 3.5, rr(S, 1.75))),
    ]


def _bulb(S):
    top = "C9.5 12.8 6.5 11.5 6.5 8.5A5.5 5.5 0 0 1 17.5 8.5C17.5 11.5 14.5 12.8 14.5 13.8"
    if S.name == "line":
        return "M9.5 20.5V13.8" + top + "V20.5Z"
    return "M11 20.5A1.5 1.5 0 0 1 9.5 19V13.8" + top + "V19A1.5 1.5 0 0 1 13 20.5Z"


@icon("smart-bulb", CAT, "Light bulb with a Wi-Fi signal inside the glass",
      tags=["smart light", "wifi bulb", "connected bulb", "smart lighting", "led bulb", "smart home"])
def _(S):
    return [
        shell(_bulb(S)),
        detail(arc(12, 11, 3.25, 220, 320)),
        dot(12, 11, 1.1),
        detail(seg(9.5, 17, 14.5, 17)),
    ]


@icon("smart-deadbolt", CAT, "Smart deadbolt with a keypad above a lever handle",
      tags=["smart lock", "keypad lock", "keyless entry", "door lock", "digital lock", "security"])
def _(S):
    return [
        shell(rect(7, 2, 10, 11.5, rr(S, 2.5))),
        dot(10, 5.25, 0.9), dot(14, 5.25, 0.9), dot(10, 8, 0.9), dot(14, 8, 0.9), dot(10, 10.75, 0.9), dot(14, 10.75, 0.9),
        dot(9.5, 18.5, 2.25),
        line(seg(9.5, 18.5, 19.5, 18.5)),
    ]


@icon("video-doorbell", CAT, "Video doorbell with a camera lens above a ring button",
      tags=["smart doorbell", "doorbell camera", "door camera", "front door", "security"], aliases=["doorbell-camera"])
def _(S):
    return [
        shell(rect(7.5, 2, 9, 20, L(S, 3, 4.5))),
        detail(circle(12, 7, 2.25)),
        dot(12, 7, 0.9),
        detail(seg(10.5, 11.5, 13.5, 11.5)),
        dot(12, 16.5, 2.25),
    ]


@icon("motion-sensor", CAT, "Wall-mounted motion sensor dome sending detection waves",
      tags=["pir sensor", "motion detector", "occupancy sensor", "movement", "security", "smart home"], aliases=["motion-detector", "pir-sensor"])
def _(S):
    dome = (poly([(6, 3), (18, 3), (18, 7)], r=0) + "L16 7A4 4 0 0 1 8 7L6 7Z") if S.name == "line" else \
        "M7.5 3H16.5A1.5 1.5 0 0 1 18 4.5V7H16A4 4 0 0 1 8 7H6V4.5A1.5 1.5 0 0 1 7.5 3Z"
    return [
        shell(dome),
        detail(seg(12, 7, 12, 11)),
        line(arc(12, 7, 8, 45, 135)),
        line(arc(12, 7, 12.5, 50, 130)),
    ]


@icon("contact-sensor", CAT, "Door contact sensor: a sensor and a magnet side by side with a gap",
      tags=["door sensor", "window sensor", "magnetic sensor", "entry sensor", "reed switch", "security"], aliases=["door-sensor"])
def _(S):
    return [
        line(arc(7, 8, 3.5, 230, 310)), line(arc(7, 8, 7, 235, 305)),
        shell(rect(3, 9, 8, 12, rr(S, 2.5))),
        dot(7, 13, 1.1),
        shell(rect(15, 12, 5, 9, rr(S, 2))),
    ]


@icon("water-leak-sensor", CAT, "Water leak sensor puck on the floor under a falling drop",
      tags=["leak detector", "flood sensor", "water sensor", "leak alarm", "plumbing", "smart home"], aliases=["leak-detector", "flood-sensor"])
def _(S):
    return [
        Part("dot", _drop(12, 2.5, 7, S)),
        shell(rect(5, 12, 14, 5.5, rr(S, 2.75))),
        line(seg(2.5, 21, 21.5, 21)),
        line(arc(12, 6.5, 5.5, -45, -5)), line(arc(12, 6.5, 5.5, 185, 225)),
    ]


def _flame(cx, cy, h):
    w = h * 0.36
    b = cy + h / 2
    t = cy - h / 2
    return (f"M{fmt(cx)} {fmt(t)}C{fmt(cx + w * 1.2)} {fmt(t + h * 0.35)} {fmt(cx + w * 1.1)} {fmt(b)} {fmt(cx)} {fmt(b)}"
            f"C{fmt(cx - w * 1.1)} {fmt(b)} {fmt(cx - w * 1.2)} {fmt(t + h * 0.35)} {fmt(cx)} {fmt(t)}Z")


@icon("gas-detector", CAT, "Plug-in gas detector with a vent grille and a flame warning mark",
      tags=["gas alarm", "gas leak detector", "carbon monoxide", "natural gas", "safety", "alarm"], aliases=["gas-alarm"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 15.5, rr(S, 3))),
        detail(seg(7.5, 6, 16.5, 6)), detail(seg(7.5, 9, 16.5, 9)),
        Part("dot", _flame(12, 13.5, 4.5)),
        line(seg(9, 18, 9, 21.5)), line(seg(15, 18, 15, 21.5)),
    ]


@icon("smart-blinds", CAT, "Motorised window blinds with a headrail motor and a Wi-Fi signal",
      tags=["motorized blinds", "smart shades", "window blinds", "roller blind", "smart home", "automation"], aliases=["motorized-blinds"])
def _(S):
    return [
        shell(rect(2, 3, 20, 3.5, rr(S, 1.5))),
        line(seg(3.5, 10, 20.5, 10)), line(seg(3.5, 13.5, 13, 13.5)), line(seg(3.5, 17, 11, 17)), line(seg(3.5, 20.5, 10.5, 20.5)),
        dot(17.5, 19.5, 1.1),
        line(arc(17.5, 19.5, 3, 225, 315)),
        line(arc(17.5, 19.5, 5.5, 230, 310)),
    ]


@icon("garage-door-opener", CAT, "Garage door opener: a ceiling motor on a rail running to a sectional door",
      tags=["garage opener", "door opener", "garage motor", "automatic garage door", "garage", "remote opener"], aliases=["garage-opener"])
def _(S):
    return [
        shell(rect(2, 3, 7, 5, rr(S, 1.5))),
        line(poly([(9, 5.5), (16.5, 5.5), (16.5, 8.5)], r=S.r * 0.6)),
        shell(rect(12, 10, 9, 11, rr(S, 1.5))),
        detail(seg(12, 13.75, 21, 13.75)), detail(seg(12, 17.25, 21, 17.25)),
    ]


@icon("smart-fridge", CAT, "Tall fridge with a touch screen panel on its door",
      tags=["smart refrigerator", "connected fridge", "touch screen fridge", "fridge", "refrigerator", "smart kitchen"], aliases=["smart-refrigerator"])
def _(S):
    return [
        shell(rect(5, 2, 14, 20, rr(S, 3))),
        detail(seg(5, 8, 19, 8)),
        detail(seg(16, 4.5, 16, 5.5)),
        detail(rect(8, 11, 5.5, 5.5, L(S, 0, 1))),
        detail(seg(16, 11, 16, 16.5)),
    ]


@icon("smart-home", CAT, "House outline with a Wi-Fi signal inside",
      tags=["connected home", "home automation", "iot", "smart house", "wifi", "domotics"], aliases=["connected-home"])
def _(S):
    return [
        shell(poly([(4, 21), (4, 10.5), (12, 3.5), (20, 10.5), (20, 21)], closed=True, r=S.r)),
        detail(arc(12, 17.5, 5.5, 225, 315)),
        detail(arc(12, 17.5, 2.75, 225, 315)),
        dot(12, 17.5, 1.1),
    ]


@icon("smart-button", CAT, "Small round wireless push button sending a signal",
      tags=["wireless button", "smart switch", "scene button", "push button", "iot", "smart home"])
def _(S):
    base = circle(12, 15.5, 5.5) if S.name == "rounded" else rect(6.5, 10, 11, 11, 2.5)
    return [
        line(arc(12, 15.5, 8.5, 235, 305)),
        line(arc(12, 15.5, 12, 240, 300)),
        shell(base),
        detail(circle(12, 15.5, 2.25)),
    ]


@icon("smart-mirror", CAT, "Mirror showing a clock and weather widget on the glass",
      tags=["magic mirror", "display mirror", "connected mirror", "bathroom mirror", "mirror", "smart home"])
def _(S):
    return [
        shell(rect(5, 2, 14, 20, rr(S, 3))),
        detail(seg(8, 6, 13, 6)),
        dot(15.5, 6, 1.25),
        detail(seg(8, 9, 11, 9)),
        detail(seg(11.5, 18, 15.5, 14)),
    ]


@icon("alarm-keypad", CAT, "Wall-mounted alarm keypad with a small screen and a grid of keys",
      tags=["security keypad", "alarm panel", "burglar alarm", "security system", "keypad", "arm disarm"], aliases=["alarm-panel"])
def _(S):
    keys = [dot(x, y, 0.8) for y in (7.5, 10.5, 13.5, 16.5) for x in (13, 16, 19)]
    return [
        shell(rect(2, 4, 20, 16, rr(S, 2.5))),
        detail(rect(4.5, 7, 5.5, 4, L(S, 0, 1))),
        dot(5.5, 15.5, 0.9), dot(8.5, 15.5, 0.9),
        *keys,
    ]


@icon("pet-feeder", CAT, "Automatic pet feeder: a food hopper with a screen above a bowl",
      tags=["automatic feeder", "cat feeder", "dog feeder", "pet food", "timed feeder", "pets"], aliases=["automatic-pet-feeder"])
def _(S):
    return [
        shell(rect(6, 2, 12, 12.5, rr(S, 2.5))),
        detail(rect(8.5, 4.5, 7, 3.5, L(S, 0, 1))),
        dot(12, 11, 1),
        shell(poly([(3, 17.5), (21, 17.5), (19, 21.5), (5, 21.5)], closed=True, r=S.r * 0.6)),
    ]


@icon("pet-water-fountain", CAT, "Pet water fountain: a round bowl with water arcing from a spout",
      tags=["cat fountain", "pet fountain", "drinking fountain", "water bowl", "pets", "hydration"])
def _(S):
    bowl = "M3 14H21A9 7 0 0 1 3 14Z" if S.name == "line" else "M4 14H20A1 1 0 0 1 21 15A9 6.5 0 0 1 3 15A1 1 0 0 1 4 14Z"
    return [
        line(seg(12, 14, 12, 9)),
        line("M12 8C12 4 17.5 4 18 11"),
        line("M12 8C12 4 6.5 4 6 11"),
        shell(bowl),
    ]


@icon("paper-shredder", CAT, "Paper shredder: a sheet going into the top and strips coming out below",
      tags=["shredder", "document shredder", "shred", "office", "confidential", "privacy"], aliases=["shredder"])
def _(S):
    return [
        line(poly([(7, 8), (7, 2.5), (17, 2.5), (17, 8)], r=S.r)),
        shell(rect(3, 9, 18, 5, rr(S, 2))),
        *[line(seg(x, 16, x, 21.5)) for x in (7, 10.33, 13.67, 17)],
    ]


@icon("laminator", CAT, "Laminator with a front slot and a glossy laminated sheet coming out",
      tags=["laminating machine", "laminate", "pouch laminator", "office", "sealing", "document"], aliases=["laminating-machine"])
def _(S):
    return [
        shell(rect(2, 4, 20, 7, rr(S, 2.5))),
        detail(seg(5, 7.5, 13, 7.5)),
        dot(18, 7.5, 1),
        line(poly([(6, 12), (6, 21), (18, 21), (18, 12)], r=S.r)),
        line(seg(9.5, 17.5, 12.5, 14.5)),
    ]


@icon("label-maker", CAT, "Handheld label maker with a screen, keys and a label strip coming out the top",
      tags=["label printer", "labeller", "labeler", "tape labeler", "organising", "office"], aliases=["label-printer"])
def _(S):
    return [
        line(poly([(9.5, 7.5), (9.5, 2.5), (14.5, 2.5), (14.5, 7.5)], r=S.r * 0.6)),
        shell(rect(4.5, 8, 15, 13, rr(S, 3))),
        detail(rect(7.5, 10.5, 9, 3, L(S, 0, 1))),
        dot(7.5, 17.5, 0.9), dot(10.5, 17.5, 0.9), dot(13.5, 17.5, 0.9), dot(16.5, 17.5, 0.9),
    ]


@icon("photocopier", CAT, "Office photocopier with a lid, a control panel and paper trays",
      tags=["copier", "copy machine", "office printer", "photocopy", "multifunction printer"], aliases=["copier", "copy-machine"])
def _(S):
    return [
        shell(rect(3, 3.5, 12, 2.5, rr(S, 1))),
        sq(17, 3.5, 4, 2.5, L(S, 0, 1)),
        shell(rect(3, 9, 18, 12, rr(S, 3))),
        detail(seg(3, 13, 21, 13)), detail(seg(3, 17, 21, 17)),
        dot(12, 15, 0.8), dot(12, 19, 0.8),
    ]


# ============================================================================ kitchen and household

@icon("rotisserie-oven", CAT, "Countertop rotisserie oven with a chicken turning on a spit behind the glass",
      tags=["rotisserie", "roast chicken", "spit roast", "countertop oven", "grill", "kitchen"])
def _(S):
    return [
        shell(rect(2, 4, 20, 14, rr(S, 2.5))),
        detail(rect(4.5, 6.5, 11, 9, L(S, 0, 1))),
        Part("dot", ellipse(10, 11, 3, 2)),
        detail(seg(6, 11, 14, 11)),
        dot(18.5, 8.5, 1), dot(18.5, 12.5, 1),
        line(seg(5, 18, 5, 20.5)), line(seg(19, 18, 19, 20.5)),
    ]


def _knife_blade():
    pts = [(12, 9.5), (4, 9.5), (2.5, 12)]
    x = 3.5
    while x < 11.5:
        pts += [(x, 14.5), (x + 1, 13.6)]
        x += 2
    pts += [(12, 14.5)]
    return pts


@icon("electric-knife", CAT, "Electric carving knife with twin serrated blades, a chunky handle and a cord",
      tags=["carving knife", "electric carving knife", "slicer", "carving", "roast", "kitchen"], aliases=["electric-carving-knife"])
def _(S):
    return [
        shell(poly(_knife_blade(), closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
        detail(seg(4, 12, 12, 12)),
        shell(rect(12, 8, 7, 8, rr(S, 3))),
        line("M19 12C21.5 12 21.5 16 21.5 20"),
    ]


def _waves3(y0, y1, xs):
    out = []
    for x in xs:
        m = (y0 + y1) / 2
        out.append(line(f"M{fmt(x)} {fmt(y1)}C{fmt(x - 1.2)} {fmt(m + 0.9)} {fmt(x + 1.2)} {fmt(m - 0.9)} {fmt(x)} {fmt(y0)}"))
    return out


@icon("warming-drawer", CAT, "Built-in warming drawer with a handle and gentle heat rising",
      tags=["warmer drawer", "plate warmer", "food warmer", "built in oven", "kitchen", "keep warm"])
def _(S):
    return [
        *_waves3(3, 7, (8, 12, 16)),
        shell(rect(2, 10, 20, 11, rr(S, 2.5))),
        detail(seg(2, 13, 22, 13)),
        detail(seg(9, 16.75, 15, 16.75)),
    ]


def _mixer_head(S):
    head = rect(3, 3, 17, 5, rr(S, 2))
    col = rect(4, 5, 4, 16, rr(S, 1))
    return path_to_d(U(P(head), P(col)))


@icon("milkshake-maker", CAT, "Spindle drink mixer: a column with a motor head and a cup hooked under the spindle",
      tags=["drink mixer", "spindle mixer", "milkshake mixer", "malt mixer", "diner", "smoothie"], aliases=["spindle-mixer"])
def _(S):
    return [
        shell(_mixer_head(S)),
        line(seg(16, 8, 16, 11)),
        shell(poly([(12, 11), (20, 11), (19, 21), (13, 21)], closed=True, r=S.r * 0.5)),
        detail(seg(16, 11, 16, 16.5)),
    ]


@icon("baseboard-heater", CAT, "Long low baseboard heater along the floor with fins and rising heat",
      tags=["skirting heater", "baseboard heating", "electric heater", "convector", "heating", "wall heater"], aliases=["skirting-heater"])
def _(S):
    return [
        *_waves3(4, 9, (7, 12, 17)),
        shell(rect(2, 12.5, 20, 6.5, rr(S, 2))),
        *[detail(seg(x, 14.75, x, 16.75)) for x in (5.5, 9, 12.5, 16)],
        dot(19, 15.75, 1),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("hand-warmer", CAT, "Pocket hand warmer with a glowing centre and heat waves",
      tags=["pocket warmer", "rechargeable hand warmer", "heat pack", "winter", "warm hands", "camping"])
def _(S):
    return [
        shell(rect(7.5, 3.5, 9, 17, L(S, 3, 4.5))),
        detail(circle(12, 12, 2.25)),
        dot(12, 12, 0.8),
        line("M3.5 7.5C2.3 9 4.7 10.5 3.5 12S2.3 15 3.5 16.5"),
        line("M20.5 7.5C19.3 9 21.7 10.5 20.5 12S19.3 15 20.5 16.5"),
    ]


@icon("steam-station-iron", CAT, "Steam generator iron resting on its water tank base, joined by a hose",
      tags=["steam generator", "steam iron", "ironing station", "steam station", "laundry", "ironing"], aliases=["steam-generator-iron"])
def _(S):
    iron = ("M7.5 14.5V11.5C7.5 10.4 8.4 9.5 9.5 9.5H15C17.8 9.5 19.8 11.3 20.5 14.5Z" if S.name == "line" else
            "M9 14.5A1.5 1.5 0 0 1 7.5 13V11.5C7.5 10.4 8.4 9.5 9.5 9.5H15C17.8 9.5 19.8 11.3 20.3 13.3A1 1 0 0 1 19.3 14.5Z")
    return [
        shell(iron),
        line(poly([(10, 9.5), (10, 5.5), (16, 5.5), (16.5, 9.5)], r=S.r)),
        line("M10 5.5C4 5.5 2 8 3 11C3.6 12.8 5.5 13 5 15"),
        shell(rect(2.5, 15.5, 19, 5.5, rr(S, 2))),
    ]


@icon("window-cleaning-robot", CAT, "Square window cleaning robot on a pane with its safety cord and cleaning path",
      tags=["window robot", "glass cleaning robot", "robot cleaner", "window cleaner", "cleaning", "housework"])
def _(S):
    return [
        shell(rect(2, 2, 20, 20, rr(S, 2))),
        detail(rect(7.5, 10, 9, 9, L(S, 1, 2.5))),
        dot(12, 14.5, 1.3),
        detail(seg(12, 10, 12, 2)),
        detail(seg(16, 7, 18.5, 4.5)),
    ]


@icon("robot-lawn-mower", CAT, "Robot lawn mower: a low sloped shell on wheels on the grass",
      tags=["robotic mower", "robot mower", "automatic mower", "lawn robot", "garden", "grass"], aliases=["robotic-mower"])
def _(S):
    return [
        dot(15, 4.5, 1.25),
        line(seg(15, 5.5, 15, 9)),
        shell("M2.5 16.5L4.5 12.5C5.5 10.5 7 9.5 9.5 9.5H15C18 9.5 20.5 12 21 16.5Z" if S.name == "line" else
              "M3.5 16.5A1 1 0 0 1 2.6 15L4.5 12.5C5.5 10.5 7 9.5 9.5 9.5H15C18 9.5 20.5 12 21 15.5A1 1 0 0 1 20 16.5Z"),
        dot(6.5, 18.5, 1.5), dot(16.5, 18.5, 2.25),
        line(seg(2, 21.75, 22, 21.75)),
    ]


@icon("ultrasonic-cleaner", CAT, "Ultrasonic cleaner tank with a ring in rippling water",
      tags=["ultrasonic bath", "jewellery cleaner", "jewelry cleaner", "sonic cleaner", "glasses cleaner", "cleaning"], aliases=["ultrasonic-bath"])
def _(S):
    return [
        line(seg(4, 4.5, 20, 4.5) if S.name == "line" else seg(4.5, 4.5, 19.5, 4.5)),
        shell(rect(3, 7.5, 18, 13.5, rr(S, 2.5))),
        detail("M6 11C7.5 9.8 9 9.8 10.5 11S13.5 12.2 15 11S16.5 9.8 18 11"),
        detail(circle(12, 16.5, 2)),
    ]


@icon("sensor-trash-can", CAT, "Touchless trash can with its lid lifting and a sensor on the front",
      tags=["sensor bin", "touchless bin", "automatic trash can", "motion bin", "garbage can", "rubbish bin"], aliases=["sensor-bin"])
def _(S):
    body = poly([(5, 9), (19, 9), (18, 21), (6, 21)], closed=True, r=S.r)
    return [
        line(seg(4, 6.5, 19.5, 3.5)),
        shell(body),
        dot(12, 12.5, 1.2),
    ]


def _cover_cap():
    return path_to_d(D(P(circle(12, 12, 5)), P(rect(9, 11.25, 6, 1.5))))


@icon("outlet-safety-cover", CAT, "Child safety cap plugged into a wall outlet",
      tags=["outlet cover", "socket cover", "outlet plug", "childproof", "baby proofing", "child safety"], aliases=["outlet-cover", "socket-cover"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S))),
        Part("dot", _cover_cap()),
    ]


@icon("key-card-switch", CAT, "Hotel key card switch: a wall plate with a card half inserted in its slot",
      tags=["card switch", "hotel key card", "energy saver switch", "card holder", "hotel room", "power switch"])
def _(S):
    return [
        line(poly([(8.5, 12), (8.5, 2.5), (15.5, 2.5), (15.5, 12)], r=S.r * 0.6)),
        shell(rect(4, 8, 16, 13, rr(S, 2.5))),
        detail(seg(7, 12, 17, 12)),
        dot(12, 17, 1.1),
    ]


@icon("septic-tank", CAT, "Cross-section of an underground septic tank with inlet and outlet pipes",
      tags=["septic system", "sewage tank", "wastewater", "drainage", "plumbing", "cesspool"])
def _(S):
    return [
        line(seg(2, 4.5, 22, 4.5)),
        shell(rect(6, 9, 12, 11.5, rr(S, 2))),
        detail(seg(12, 9, 12, 16)),
        line(seg(2, 11.5, 6, 11.5)), line(seg(18, 13, 22, 13)),
    ]


def _radkey_grip(S):
    wings = U(P(circle(7, 7, 3.5)), P(circle(17, 7, 3.5)), P(rect(7, 5.25, 10, 3.5)))
    return path_to_d(wings)


@icon("radiator-key", CAT, "Radiator bleed key with a butterfly grip, short shaft and square socket end",
      tags=["bleed key", "radiator bleed key", "bleeding radiator", "plumbing", "heating", "key"], aliases=["bleed-key"])
def _(S):
    return [
        shell(_radkey_grip(S)),
        line(seg(12, 10.5, 12, 15)),
        shell(rect(9, 15, 6, 6, L(S, 0.5, 1.5))),
        dot(12, 18, 1),
    ]


@icon("immersion-heater", CAT, "Immersion heater: a screw cap head with a long looped heating element",
      tags=["immersion element", "water heater element", "boiler element", "hot water", "heating element", "plumbing"])
def _(S):
    return [
        shell(rect(6.5, 2, 11, 4.5, L(S, 0.5, 2))),
        shell(rect(8.5, 8.5, 7, 2.5, L(S, 0, 1.25))),
        line("M10 11V18.5A2 2 0 0 0 14 18.5V11"),
    ]


@icon("tube-amplifier", CAT, "Valve amplifier with a row of vacuum tubes on top and two knobs",
      tags=["valve amplifier", "vacuum tube amp", "tube amp", "hi-fi", "vintage audio", "amplifier"], aliases=["valve-amplifier"])
def _(S):
    return [
        *[shell(rect(x - 1.5, 4, 3, 6.5, 1.5)) for x in (6, 12, 18)],
        shell(rect(2, 12.5, 20, 8.5, rr(S, 2.5))),
        detail(circle(6.5, 16.75, 1.75)),
        detail(circle(17.5, 16.75, 1.75)),
    ]


def _crescent(cx, cy, r):
    return path_to_d(D(P(circle(cx, cy, r)), P(circle(cx + r * 0.6, cy - r * 0.45, r * 0.85))))


@icon("white-noise-machine", CAT, "White noise sound machine with a moon on the front and sound waves above",
      tags=["sound machine", "sleep machine", "noise machine", "sleep aid", "baby sleep", "white noise"], aliases=["sound-machine"])
def _(S):
    return [
        line("M4.5 5.5C6 4 7.5 4 9 5.5S12 7 13.5 5.5S16.5 4 18 5.5"),
        line("M6 9.5C7.5 8 9 8 10.5 9.5S13.5 11 15 9.5S16.5 8 18 9.5"),
        shell(rect(3, 13, 18, 8, rr(S, 4))),
        Part("dot", _crescent(12, 17, 2.5)),
    ]


@icon("wake-up-light", CAT, "Wake-up light: a round lamp glowing like a rising sun above a clock base",
      tags=["sunrise alarm", "sunrise lamp", "light alarm clock", "dawn simulator", "sleep", "morning"], aliases=["sunrise-alarm"])
def _(S):
    return [
        shell(circle(12, 9.5, 4.5)),
        *[line(seg(*pt_on(12, 9.5, 6.5, a), *pt_on(12, 9.5, 8.5, a))) for a in (0, 45, 135, 180, 225, 270, 315)],
        shell(rect(5.5, 17.5, 13, 4, rr(S, 2))),
        detail(seg(10, 19.5, 14, 19.5)),
    ]


@icon("usb-hub", CAT, "USB hub: a small bar with three ports and a short cable with a plug",
      tags=["usb splitter", "port hub", "usb adapter", "dongle", "connector", "computer accessory"])
def _(S):
    return [
        shell(rect(2, 11, 14, 7, rr(S, 3))),
        sq(4, 13.75, 2.5, 1.5), sq(7.75, 13.75, 2.5, 1.5), sq(11.5, 13.75, 2.5, 1.5),
        line("M16 14.5C19.5 14.5 19.5 12 19.5 9"),
        shell(rect(17.5, 3, 4, 6, rr(S, 1))),
    ]
