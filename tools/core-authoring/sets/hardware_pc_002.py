"""TypeIcon Core: computer hardware, peripherals and IT equipment (batch 002)."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "hardware-pc"


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def stand(cx=12, y0=16, y1=20):
    return [line(seg(cx, y0, cx, y1)), line(seg(cx - 4, y1 + 0.5, cx + 4, y1 + 0.5))]


# ============================================================================ chunk 1

@icon("haptic-glove", CAT, "Glove with finger dividers and a small control module on the back of the hand",
      tags=["vr glove", "haptic", "force feedback", "wearable", "virtual reality", "hand tracking"])
def _(S):
    return [
        shell(rect(6, 3, 15, 18, rr(S, 5))),
        detail(seg(9.75, 3, 9.75, 9)), detail(seg(13.5, 3, 13.5, 9)), detail(seg(17.25, 3, 17.25, 9)),
        line(poly([(6, 16), (3, 12.5)], r=0)),
        detail(seg(6, 17.5, 21, 17.5)),
        shell(rect(10.5, 11, 6, 4, rr(S, 1.5))),
    ]


@icon("pointing-stick", CAT, "Four keyboard keys with a small rubber nub in the gap between them",
      tags=["trackpoint", "nub", "laptop", "mouse alternative", "keyboard", "cursor"])
def _(S):
    k = rr(S, 3)
    return [
        shell(rect(3, 3, 6.5, 6.5, k)), shell(rect(14.5, 3, 6.5, 6.5, k)),
        shell(rect(3, 14.5, 6.5, 6.5, k)), shell(rect(14.5, 14.5, 6.5, 6.5, k)),
        dot(12, 12, 1.75),
    ]


@icon("mouse-bungee", CAT, "Weighted base with an arm and clip holding a mouse cable, running to a mouse",
      tags=["cable holder", "cable management", "gaming", "desk", "cord", "mouse"])
def _(S):
    return [
        shell(ellipse(7, 19, 5, 2.5)),
        line(seg(7, 16.5, 7, 7)),
        line(poly([(7, 6), (17.5, 6), (17.5, 10)], r=S.r)),
        shell(rect(14, 10, 7, 11, 2 if S.name == "line" else 3.5)),
        detail(seg(17.5, 12.5, 17.5, 14.5)),
    ]


@icon("vesa-mount", CAT, "Square mounting plate with four screw holes, a center joint and an arm below",
      tags=["monitor mount", "monitor arm", "bracket", "wall mount", "tv mount", "display"])
def _(S):
    return [
        shell(rect(4, 3, 16, 14, rr(S, 3))),
        dot(8, 7, 1), dot(16, 7, 1), dot(8, 13, 1), dot(16, 13, 1),
        dot(12, 10, 1.5),
        line(seg(12, 17, 12, 21)),
    ]


@icon("keyboard-tray", CAT, "Keyboard on a tray hung from the edge of a desk",
      tags=["under desk", "ergonomic", "slide out", "desk", "typing", "workstation"])
def _(S):
    return [
        line(seg(2, 4, 22, 4)),
        line(seg(7, 4, 7, 12)), line(seg(17, 4, 17, 12)),
        shell(rect(3, 12, 18, 9, rr(S, 3))),
        dot(7, 15, 1), dot(10.33, 15, 1), dot(13.67, 15, 1), dot(17, 15, 1),
        detail(seg(8, 18, 16, 18)),
    ]


@icon("digitizer-puck", CAT, "Drafting puck with a round crosshair window, a row of buttons and a cable",
      tags=["cad", "tablet puck", "cursor", "drafting", "digitizing", "graphics tablet"])
def _(S):
    return [
        line(seg(12, 8, 12, 3)),
        shell(rect(4, 8, 16, 13, rr(S, 4))),
        shell(circle(12, 12.5, 2.5)),
        detail(seg(8, 12.5, 16, 12.5)),
        dot(8, 18, 1), dot(12, 18, 1), dot(16, 18, 1),
    ]


@icon("adaptive-switch", CAT, "Large round dome button on a low base",
      tags=["accessibility", "big button", "assistive", "palm switch", "disability", "single switch"])
def _(S):
    return [
        shell("M4 16A8 8 0 0 1 20 16Z"),
        shell(rect(2, 16, 20, 5, rr(S, 2))),
        detail(arc(12, 16, 4.5, 200, 250)),
    ]


@icon("ball-mouse", CAT, "Underside of a mouse showing the rolling ball in its retaining ring",
      tags=["trackball", "mechanical mouse", "retro", "roller ball", "old mouse", "underside"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, 5 if S.name == "line" else 6)),
        shell(circle(12, 12, 5)),
        dot(12, 12, 2.5),
    ]


@icon("microphone-boom-arm", CAT, "Jointed desk-clamped arm holding a microphone at its end",
      tags=["mic arm", "podcast", "streaming", "desk mount", "broadcast", "recording"])
def _(S):
    return [
        shell(rect(3, 16, 6, 5, rr(S, 1.5))),
        line(poly([(6, 16), (6, 9), (15, 9)], r=S.r)),
        shell(rect(15, 4, 6, 10, 3)),
        detail(seg(15, 9, 21, 9)),
    ]


@icon("monitor-hood", CAT, "Monitor screen surrounded by a shading hood on the top and sides",
      tags=["glare shield", "screen shade", "calibration", "photo editing", "visor", "display"])
def _(S):
    return [
        shell(rect(3, 3, 18, 13, rr(S, 2))),
        shell(rect(8, 7, 8, 5)),
        detail(seg(3, 3, 8, 7)), detail(seg(21, 3, 16, 7)),
        *stand(12, 16, 20),
    ]


@icon("monitor-calibrator", CAT, "Round colour sensor hanging by its cable on the middle of a monitor screen",
      tags=["colorimeter", "color calibration", "display profile", "screen color", "photo", "sensor"])
def _(S):
    return [
        shell(rect(3, 3, 18, 13, rr(S, 2))),
        line(seg(12, 3, 12, 6.5)),
        shell(circle(12, 9.5, 3)),
        *stand(12, 16, 20),
    ]


@icon("dead-pixel", CAT, "Blank monitor with one small solid square on the screen",
      tags=["stuck pixel", "screen defect", "display fault", "lcd", "broken pixel", "monitor"])
def _(S):
    return [
        shell(rect(3, 3, 18, 13, rr(S, 2))),
        sq(10.5, 7, 3, 3),
        *stand(12, 16, 20),
    ]


@icon("cracked-screen", CAT, "Laptop screen with crack lines spreading from one impact point",
      tags=["broken screen", "smashed", "damage", "repair", "laptop", "shattered"])
def _(S):
    return [
        shell(rect(3, 3, 18, 14, rr(S, 2))),
        detail(poly([(11, 10), (7.5, 8), (7, 3)])),
        detail(poly([(11, 10), (14.5, 7), (15.5, 3)])),
        detail(poly([(11, 10), (16, 12), (21, 12.5)])),
        detail(poly([(11, 10), (9, 13), (10, 17)])),
        line(seg(2, 20.5, 22, 20.5)),
    ]


@icon("smart-glasses", CAT, "Glasses with a camera at one hinge and a small display in one lens",
      tags=["ar glasses", "augmented reality", "wearable", "heads up display", "eyewear", "smart eyewear"])
def _(S):
    return [
        shell(rect(5, 10, 7, 7, rr(S, 3))),
        shell(rect(14, 10, 7, 7, rr(S, 3))),
        line(seg(12, 12.5, 14, 12.5)),
        line(seg(5, 12, 3, 8.5)),
        dot(3, 7.5, 1.5),
        sq(16.5, 12.5, 2.5, 2.5),
    ]


@icon("vr-base-station", CAT, "Tracking box on a tripod sweeping fan lines from its front face",
      tags=["lighthouse", "vr tracking", "room scale", "virtual reality", "sensor", "tripod"])
def _(S):
    return [
        shell(rect(3, 3, 9, 8, rr(S, 2))),
        line(poly([(3, 21), (7.5, 11), (12, 21)])),
        line(seg(15, 7, 21, 7)), line(seg(15, 4.5, 20, 2.5)), line(seg(15, 9.5, 20, 11.5)),
    ]


# ============================================================================ chunk 2

@icon("video-conference-bar", CAT, "Slim camera and speaker bar mounted above a screen",
      tags=["conference camera", "meeting room", "webcam", "video call", "soundbar", "huddle room"])
def _(S):
    return [
        shell(rect(2, 3, 20, 6, rr(S, 3))),
        dot(12, 6, 1.25), dot(5.5, 6, 1), dot(8.5, 6, 1), dot(15.5, 6, 1), dot(18.5, 6, 1),
        shell(rect(4, 12, 16, 9, rr(S, 2))),
    ]


@icon("keyboard-and-mouse", CAT, "Keyboard with a mouse beside it",
      tags=["desk setup", "peripherals", "input devices", "typing", "combo", "set"])
def _(S):
    return [
        shell(rect(2, 7, 13, 10, rr(S, 3))),
        dot(5.5, 10.5, 0.9), dot(8.5, 10.5, 0.9), dot(11.5, 10.5, 0.9),
        detail(seg(6, 14, 11, 14)),
        shell(rect(17, 6, 5, 11, 2.5)),
    ]


@icon("backlit-keyboard", CAT, "Keyboard with short light rays shining above its keys",
      tags=["illuminated keyboard", "rgb keyboard", "glow", "night typing", "keyboard light", "gaming"])
def _(S):
    return [
        shell(rect(3, 10, 18, 11, rr(S, 3))),
        dot(7, 13.5, 1), dot(10.33, 13.5, 1), dot(13.67, 13.5, 1), dot(17, 13.5, 1),
        detail(seg(8, 17.5, 16, 17.5)),
        line(seg(12, 2.5, 12, 6.5)), line(seg(6.5, 4, 8, 7)), line(seg(17.5, 4, 16, 7)),
    ]


@icon("usb-power-meter", CAT, "Inline USB dongle with a readout window between a plug and a cable",
      tags=["power monitor", "voltage", "amperage", "usb tester", "charging meter", "watts"])
def _(S):
    return [
        shell(rect(2, 9, 4, 6, rr(S, 1.5))),
        line(seg(6, 12, 8, 12)),
        shell(rect(8, 6, 9, 12, rr(S, 2.5))),
        sq(10, 8.5, 5, 3),
        dot(12.5, 15, 1),
        line(seg(17, 12, 22, 12)),
    ]


@icon("roll-up-keyboard", CAT, "Flexible keyboard with one end rolled into a tube",
      tags=["silicone keyboard", "flexible", "portable", "travel keyboard", "foldable", "waterproof"])
def _(S):
    return [
        shell(rect(2, 9, 11, 8, rr(S, 2.5))),
        dot(5, 12, 0.9), dot(8, 12, 0.9), dot(11, 12, 0.9),
        detail(seg(5.5, 14.8, 10.5, 14.8)),
        shell(circle(17.5, 13, 4)),
        dot(17.5, 13, 1.25),
    ]


@icon("laser-projection-keyboard", CAT, "Small projector casting a fan of light onto a desk where a keyboard appears",
      tags=["virtual keyboard", "projected keyboard", "laser keyboard", "bluetooth", "portable", "hologram"])
def _(S):
    return [
        shell(rect(8, 2, 8, 4, rr(S, 1.5))),
        line(seg(10, 6, 6, 13)), line(seg(14, 6, 18, 13)),
        shell(poly([(6, 14), (18, 14), (21, 21), (3, 21)], closed=True, r=S.r)),
        detail(seg(9.5, 14, 8, 21)), detail(seg(14.5, 14, 16, 21)),
    ]


@icon("headphone-amplifier", CAT, "Small amplifier box with a volume knob and a headphone jack with its cable",
      tags=["headphone amp", "dac", "audio", "hi-fi", "volume knob", "audiophile"])
def _(S):
    return [
        shell(rect(2, 7, 20, 12, rr(S, 3))),
        shell(circle(8, 13, 3)),
        detail(seg(8, 13, 8, 11)),
        dot(17, 13, 1.5),
        line(seg(17, 13, 17, 21)),
    ]


@icon("screen-cleaner-spray", CAT, "Spray bottle misting toward a screen",
      tags=["cleaning", "monitor cleaning", "wipe", "dust", "cleaner", "display care"])
def _(S):
    return [
        shell(rect(2, 11, 7, 10, rr(S, 3))),
        line(poly([(5.5, 11), (5.5, 6), (10, 6)], r=S.r)),
        dot(13, 4.5, 1), dot(13.5, 8, 1), dot(12.5, 11.5, 1),
        shell(rect(17, 3, 5, 14, rr(S, 1.5))),
    ]


@icon("brain-computer-interface", CAT, "Head in profile with electrode dots on the scalp and a cable to a small chip",
      tags=["bci", "eeg", "neurotech", "mind control", "brain signals", "neural interface"])
def _(S):
    head = ("M5 21V16C3 14 3 12 3 9A6 6 0 0 1 9 3A6 6 0 0 1 15 9L16.5 12H15V14.5A2 2 0 0 1 13 16.5H11V21Z")
    return [
        shell(head),
        dot(6.5, 8.5, 1), dot(9, 6, 1), dot(11.5, 8.5, 1),
        line(poly([(12, 3.3), (18, 3.3), (18, 7)], r=S.r)),
        shell(rect(16, 7, 5, 5, rr(S, 1.5))),
    ]


@icon("omnidirectional-treadmill", CAT, "Walking figure inside a waist ring on a round platform",
      tags=["vr treadmill", "walk in place", "virtual reality", "locomotion", "gaming", "movement"])
def _(S):
    return [
        shell(ellipse(12, 19, 9, 2.5)),
        shell(circle(12, 4.5, 2)),
        line(seg(12, 7, 12, 12)),
        line(poly([(9, 17), (12, 12), (15, 17)], r=S.r)),
        line(ellipse(12, 10, 5, 1.5)),
    ]


@icon("infrared-blaster", CAT, "Round puck with a dark lens on its edge sending signal waves",
      tags=["ir emitter", "remote control", "ir transmitter", "universal remote", "signal", "smart home"])
def _(S):
    return [
        shell(circle(7, 12, 4.5)),
        sq(10, 10.5, 2.5, 3),
        line(arc(11, 12, 6, -45, 45)),
        line(arc(11, 12, 10, -45, 45)),
    ]


def _keyguard_filled():
    holes = [P(circle(x, y, 1.6)) for x in (6.5, 12, 17.5) for y in (9, 15)]
    return D(P(rect(1, 4, 22, 16, 3)), *holes)


@icon("keyboard-keyguard", CAT, "Keyboard covered by a plate with a round hole over each key",
      tags=["key guard", "accessibility", "typing aid", "tremor", "assistive", "keyboard cover"],
      filled=_keyguard_filled)
def _(S):
    return [
        shell(rect(2, 5, 20, 14, rr(S, 3))),
        *[shell(circle(x, y, 1.5)) for x in (6.5, 12, 17.5) for y in (9, 15)],
    ]


@icon("color-grading-panel", CAT, "Control surface with a row of buttons and three trackball rings",
      tags=["colour grading", "video editing", "colorist", "control surface", "trackballs", "post production"])
def _(S):
    return [
        shell(rect(1.5, 3, 21, 18, rr(S, 3))),
        dot(5, 7, 1), dot(8.5, 7, 1), dot(12, 7, 1), dot(15.5, 7, 1), dot(19, 7, 1),
        detail(circle(5.75, 15, 2)), detail(circle(12, 15, 2)), detail(circle(18.25, 15, 2)),
    ]


@icon("dictation-microphone", CAT, "Slim handheld microphone with a grille and a column of thumb buttons",
      tags=["voice typing", "speech to text", "handheld mic", "transcription", "recorder", "voice"])
def _(S):
    return [
        shell(rect(7, 2, 10, 20, rr(S, 5))),
        dot(10, 5, 0.9), dot(14, 5, 0.9), dot(12, 7.5, 0.9),
        detail(seg(7, 10, 17, 10)),
        dot(12, 13, 1), dot(12, 16, 1), dot(12, 19, 1),
    ]


@icon("cable-raceway", CAT, "Wall channel with its lid lifted open showing cables inside",
      tags=["cable duct", "cable trunking", "wire cover", "conduit", "cable management", "wall"])
def _(S):
    return [
        shell(rect(2, 10, 20, 9, rr(S, 2))),
        dot(6, 14.5, 1.25), dot(10, 14.5, 1.25), dot(14, 14.5, 1.25),
        line(poly([(16, 10), (21, 5)], r=0)),
    ]


# ============================================================================ chunk 3

@icon("ceiling-access-point", CAT, "Flat round wireless access point under a ceiling line with signal arcs below",
      tags=["wifi", "wireless", "ap", "ceiling mount", "network", "office wifi"])
def _(S):
    return [
        line(seg(2, 3, 22, 3)),
        shell(rect(6, 3, 12, 4, rr(S, 2))),
        dot(12, 5, 0.8),
        line(arc(12, 9, 4, 45, 135)), line(arc(12, 9, 8, 45, 135)), line(arc(12, 9, 12, 45, 135)),
    ]


@icon("powerline-adapter", CAT, "Plug-in wall adapter with an ethernet port and a wave along the house wiring",
      tags=["homeplug", "ethernet over power", "network extender", "wall plug", "wired network", "mains"])
def _(S):
    return [
        line(seg(8, 6, 8, 2.5)), line(seg(12, 6, 12, 2.5)),
        shell(rect(4, 6, 12, 15, rr(S, 3))),
        dot(10, 9.5, 1),
        sq(7, 15, 6, 3),
        line("M17.5 12Q18.75 9.5 20 12T22.5 12"),
    ]


@icon("poe-injector", CAT, "Small box with two ethernet ports and a lightning bolt, with a power cord",
      tags=["power over ethernet", "poe", "network power", "injector", "ethernet", "camera power"])
def _(S):
    return [
        shell(rect(2, 5, 16, 14, rr(S, 3))),
        sq(4.5, 7.5, 4, 3), sq(11.5, 7.5, 4, 3),
        solid(poly([(11.5, 11.5), (8, 15), (10.5, 15), (9, 17.5), (13, 13.5), (10.5, 13.5)], closed=True)),
        line(seg(18, 12, 22, 12)),
    ]


@icon("wireless-bridge", CAT, "Two dish antennas on poles facing each other with a dashed beam between them",
      tags=["point to point", "wifi bridge", "radio link", "outdoor antenna", "building to building", "backhaul"])
def _(S):
    return [
        line("M8.5 4.5A5.5 5.5 0 0 0 8.5 15.5"), line("M15.5 4.5A5.5 5.5 0 0 1 15.5 15.5"),
        line(seg(6.5, 13, 6.5, 21)), line(seg(17.5, 13, 17.5, 21)),
        dot(10.2, 10, 0.8), dot(12, 10, 0.8), dot(13.8, 10, 0.8),
    ]


@icon("cable-tone-tracer", CAT, "Pointed probe wand with a speaker grille beside a tone generator with two clip leads",
      tags=["cable tracer", "wire tracer", "toner probe", "cable finder", "network tester", "tone generator"])
def _(S):
    return [
        shell(poly([(2, 8), (5, 5), (18, 5), (18, 11), (5, 11)], closed=True, r=S.r), stroke_miterlimit="3"),
        dot(9, 8, 0.9), dot(12, 8, 0.9), dot(15, 8, 0.9),
        shell(rect(3, 15, 10, 6, rr(S, 2))),
        dot(8, 18, 1),
        line(seg(13, 16.5, 22, 16.5)), line(seg(13, 19.5, 22, 19.5)),
    ]


@icon("network-wall-plate", CAT, "Square wall faceplate with two network jack openings and two screws",
      tags=["ethernet jack", "wall outlet", "rj45", "keystone", "network socket", "faceplate"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        sq(5.5, 9, 5, 6), sq(13.5, 9, 5, 6),
        dot(12, 5.5, 0.9), dot(12, 18.5, 0.9),
    ]


@icon("network-video-recorder", CAT, "Recorder box with a drive slot and camera ports, linked to a small security camera",
      tags=["nvr", "cctv", "security cameras", "surveillance recorder", "video storage", "ip camera"])
def _(S):
    return [
        shell(rect(8, 2, 8, 5, rr(S, 2))),
        dot(12, 4.5, 1),
        line(seg(12, 7, 12, 11)),
        shell(rect(2, 11, 20, 9, rr(S, 2.5))),
        detail(seg(5, 15.5, 10, 15.5)),
        dot(14, 15.5, 1), dot(17, 15.5, 1), dot(19.5, 15.5, 0.9),
    ]


@icon("hot-aisle-containment", CAT, "Two rows of server racks facing away from each other under a roof with a rising heat arrow",
      tags=["data center", "cooling", "airflow", "hot aisle", "server room", "heat"])
def _(S):
    return [
        shell(rect(2, 9, 5, 12, rr(S, 1.5))), shell(rect(17, 9, 5, 12, rr(S, 1.5))),
        detail(seg(2, 15, 7, 15)), detail(seg(17, 15, 22, 15)),
        line(poly([(7, 9), (7, 3.5), (17, 3.5), (17, 9)], r=S.r)),
        line(seg(12, 19, 12, 9.5)),
        line(poly([(9.5, 12), (12, 9.5), (14.5, 12)], r=0)),
    ]


@icon("raised-floor-tile", CAT, "Square perforated floor tile with a grid of round holes",
      tags=["data center floor", "perforated tile", "access floor", "airflow tile", "server room", "vented"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        *[dot(x, y, 1) for x in (8, 12, 16) for y in (8, 12, 16)],
    ]


@icon("computer-room-air-conditioner", CAT, "Tall floor cabinet with a control display and grille and cold air flowing from its base",
      tags=["crac", "data center cooling", "server room cooling", "air handler", "hvac", "cold air"])
def _(S):
    return [
        shell(rect(5, 2, 14, 15, rr(S, 3))),
        sq(8, 5, 8, 3),
        detail(seg(5, 11, 19, 11)), detail(seg(5, 14, 19, 14)),
        line(seg(8, 19.5, 8, 22)), line(seg(12, 19.5, 12, 22)), line(seg(16, 19.5, 16, 22)),
    ]


@icon("rack-power-strip", CAT, "Long vertical power strip with a column of outlets and a cord leaving the top",
      tags=["pdu", "power distribution unit", "outlet strip", "rack mount", "power bar", "server rack"])
def _(S):
    return [
        line(poly([(12, 6), (12, 3.5), (19, 3.5)], r=S.r)),
        shell(rect(8, 6, 8, 16, rr(S, 2.5))),
        sq(10, 8, 4, 3), sq(10, 12.5, 4, 3), sq(10, 17, 4, 3),
    ]


@icon("rack-console-drawer", CAT, "Rack drawer pulled out with a flip-up screen, keyboard keys and a front bar",
      tags=["kvm drawer", "rackmount keyboard", "lcd console", "server console", "crash cart", "data center"])
def _(S):
    return [
        shell(rect(5, 2, 14, 8, rr(S, 2))),
        shell(rect(3, 12, 18, 5, rr(S, 2))),
        dot(6.5, 14.5, 0.8), dot(10, 14.5, 0.8), dot(13.5, 14.5, 0.8), dot(17, 14.5, 0.8),
        line(seg(2, 20.5, 22, 20.5)),
    ]


@icon("cage-nut", CAT, "Square nut held in a spring-steel cage with two flexible wings",
      tags=["rack nut", "square hole", "rack screw", "server rack hardware", "clip nut", "mounting"])
def _(S):
    return [
        shell(rect(4, 4, 16, 15, rr(S, 2.5))),
        shell(rect(8.5, 8, 7, 7, rr(S, 1.5))),
        dot(12, 11.5, 1.1),
        line(seg(4, 15, 2, 20)), line(seg(20, 15, 22, 20)),
    ]


@icon("two-post-rack", CAT, "Open rack of two tall upright rails on a base holding three flat devices",
      tags=["relay rack", "telco rack", "open frame rack", "network rack", "equipment rack", "server"])
def _(S):
    return [
        line(seg(4, 2, 4, 21)), line(seg(20, 2, 20, 21)),
        shell(rect(6, 4, 12, 4, rr(S, 1.5))), shell(rect(6, 10, 12, 4, rr(S, 1.5))), shell(rect(6, 16, 12, 4, rr(S, 1.5))),
    ]


@icon("server-lift", CAT, "Wheeled cart with a tall mast and a raised platform carrying a server",
      tags=["server hoist", "rack lift", "equipment lifter", "data center tool", "cart", "heavy hardware"])
def _(S):
    return [
        line(seg(5, 3, 5, 18)),
        line(seg(3, 18, 21, 18)),
        dot(6, 20.5, 1.25), dot(18, 20.5, 1.25),
        line(seg(5, 14, 21, 14)),
        shell(rect(8, 8, 12, 5, rr(S, 1.5))),
        dot(17, 10.5, 0.9),
    ]


# ============================================================================ chunk 4

@icon("containerized-data-center", CAT, "Shipping container with both doors swung open showing rows of server racks",
      tags=["modular data center", "container", "portable server room", "edge data center", "shipping container", "datacenter"])
def _(S):
    return [
        shell(rect(5, 6, 14, 13, rr(S, 1.5))),
        detail(seg(9.5, 6, 9.5, 19)), detail(seg(14.5, 6, 14.5, 19)),
        line(poly([(5, 6), (2, 9), (2, 16), (5, 19)], r=0)),
        line(poly([(19, 6), (22, 9), (22, 16), (19, 19)], r=0)),
    ]


@icon("server-rail-kit", CAT, "Telescoping slide rail drawn extended in three nested sections",
      tags=["rack rails", "slide rails", "sliding rail", "rack mount kit", "server mounting", "telescoping"])
def _(S):
    return [
        shell(rect(2, 2, 12, 5, rr(S, 3))),
        shell(rect(8, 9, 12, 5, rr(S, 3))),
        shell(rect(12, 16, 10, 5, rr(S, 3))),
    ]


@icon("cable-management-arm", CAT, "Hinged zigzag arm folding between a server back and a rack post",
      tags=["cable arm", "rack cable arm", "server cables", "hinged arm", "data center", "organizer"])
def _(S):
    return [
        shell(rect(2, 3, 3, 18, rr(S, 1.5))),
        line(seg(21, 3, 21, 21)),
        line(poly([(5, 6), (19, 12), (5, 18)], r=S.r)),
        dot(19, 12, 1.4),
    ]


@icon("sim-gear-shifter", CAT, "Gear stick with a round knob rising from a box marked with an H-shaped slot pattern",
      tags=["racing wheel shifter", "driving simulator", "sim racing", "manual gearbox", "gaming", "h pattern"])
def _(S):
    return [
        shell(circle(12, 5, 3)),
        line(seg(12, 8, 12, 13)),
        shell(rect(3, 13, 18, 8, rr(S, 2.5))),
        detail(seg(8, 15, 8, 19)), detail(seg(16, 15, 16, 19)), detail(seg(8, 17, 16, 17)),
    ]


@icon("cellular-router", CAT, "Router box with two paddle antennas and a SIM card inserted at the front",
      tags=["4g router", "5g router", "lte", "mobile hotspot", "sim router", "mobile broadband"])
def _(S):
    return [
        line(seg(7, 11, 7, 3)), line(seg(17, 11, 17, 3)),
        shell(rect(2, 11, 20, 9, rr(S, 2.5))),
        dot(5, 15.5, 0.9), dot(8, 15.5, 0.9),
        solid(poly([(14, 14), (18, 14), (19.5, 15.5), (19.5, 18.5), (14, 18.5)], closed=True)),
    ]


@icon("fusion-splicer", CAT, "Compact splicing machine with a screen on a hinged arm and two fiber clamps on top",
      tags=["fiber splicer", "optical fiber", "fibre optic", "splicing", "fusion splice", "telecom tool"])
def _(S):
    return [
        shell(rect(2, 12, 20, 9, rr(S, 2.5))),
        shell(rect(3, 2, 9, 7, rr(S, 2))),
        line(seg(7.5, 9, 7.5, 12)),
        sq(14.5, 8, 2.5, 4), sq(19, 8, 2.5, 4),
        line(seg(17, 9.5, 19, 9.5)),
    ]


@icon("eprom-chip", CAT, "Dual-row pin chip with a round clear window over the die",
      tags=["uv eprom", "memory chip", "integrated circuit", "rom", "ic", "window chip"])
def _(S):
    pins = []
    for y in (6, 10, 14, 18):
        pins += [line(seg(2, y, 6, y)), line(seg(18, y, 22, y))]
    return [
        shell(rect(6, 3, 12, 18, rr(S, 2.5))),
        *pins,
        shell(circle(12, 12, 3)),
        dot(12, 12, 1),
    ]


@icon("magnetic-drum-memory", CAT, "Horizontal cylinder on two supports with a row of read heads along its top",
      tags=["drum storage", "vintage computer", "retro memory", "legacy storage", "mainframe", "history"])
def _(S):
    return [
        shell("M5 8H19A2 4 0 0 1 19 16H5A2 4 0 0 1 5 8Z"),
        detail(seg(11, 8, 11, 16)),
        line(seg(8, 3, 8, 7)), line(seg(12, 3, 12, 7)), line(seg(16, 3, 16, 7)),
        line(seg(7, 16, 7, 21)), line(seg(17, 16, 17, 21)),
    ]


@icon("dual-screen-laptop", CAT, "Laptop with a second slim screen strip above its keyboard",
      tags=["secondary display", "two screen laptop", "extra screen", "touch bar", "productivity", "portable workstation"])
def _(S):
    return [
        shell(rect(4, 2, 16, 8, rr(S, 2))),
        shell(rect(4, 13.5, 16, 3, rr(S, 1.5))),
        line(seg(2, 21, 22, 21)),
    ]


@icon("retractable-cable", CAT, "Round cable reel with a cable pulled out on both sides, each ending in a small plug",
      tags=["cable reel", "cord reel", "retractable cord", "usb cable", "charging cable", "auto rewind"])
def _(S):
    return [
        shell(circle(12, 12, 5)),
        dot(12, 12, 1.5),
        line(seg(5, 12, 7, 12)), line(seg(17, 12, 19, 12)),
        sq(2, 10, 3, 4, 0 if S.name == 'line' else 1), sq(19, 10, 3, 4, 0 if S.name == 'line' else 1),
    ]


@icon("disk-cloning", CAT, "Two hard drives side by side with an arrow copying from the left to the right",
      tags=["drive clone", "disk copy", "disk imaging", "backup", "duplicate drive", "migrate drive"])
def _(S):
    return [
        shell(rect(2, 4, 7, 16, rr(S, 2))), shell(rect(15, 4, 7, 16, rr(S, 2))),
        dot(5.5, 8, 1.2), dot(18.5, 8, 1.2),
        detail(seg(2, 15, 9, 15)), detail(seg(15, 15, 22, 15)),
        line(seg(10.5, 12, 13.5, 12)),
        line(poly([(12.5, 10), (14.5, 12), (12.5, 14)], r=0)),
    ]


@icon("uv-curing-station", CAT, "Turntable under a clear dome with short light rays shining down on a small object",
      tags=["resin curing", "3d print finishing", "uv light", "post processing", "cure box", "resin printer"])
def _(S):
    return [
        shell("M4 15A8 8 0 0 1 20 15Z"),
        shell(rect(2, 15, 20, 6, rr(S, 2))),
        line(seg(8.5, 8.5, 8.5, 10.5)), line(seg(12, 8, 12, 10.5)), line(seg(15.5, 8.5, 15.5, 10.5)),
        sq(10, 12.5, 4, 2),
    ]


@icon("compressed-air-duster", CAT, "Aerosol can with a thin straw nozzle blowing short air lines",
      tags=["canned air", "air blower", "dust cleaner", "keyboard cleaning", "pc cleaning", "duster"])
def _(S):
    return [
        shell(rect(2.5, 11, 8, 10, rr(S, 3))),
        line(poly([(6.5, 11), (6.5, 5), (15, 5)], r=S.r)),
        line(seg(17.5, 5, 21.5, 5)), line(seg(17, 8, 20.5, 10)), line(seg(17, 2.5, 20.5, 1.5)),
    ]


@icon("usb-microscope", CAT, "Pen-shaped microscope on a stand with a ring light at its lens",
      tags=["digital microscope", "magnifier", "inspection camera", "electronics repair", "close up", "usb camera"])
def _(S):
    return [
        line(seg(3, 22, 21, 22)), line(seg(7, 22, 7, 8)), line(seg(7, 8, 11, 8)),
        shell(rect(11, 3, 6, 11, rr(S, 2.5))),
        sq(12.5, 14, 3, 2.5),
        line(seg(10.5, 18.5, 17.5, 18.5)),
    ]


@icon("cyberdeck", CAT, "Clamshell case with a screen in the lid, keys in the base and a stubby antenna",
      tags=["portable computer", "diy computer", "hacker", "custom laptop", "retro futurism", "handmade pc"])
def _(S):
    return [
        line(seg(18, 6, 20.5, 2)),
        shell(rect(4, 6, 15, 8, rr(S, 2))),
        shell(rect(2, 14, 20, 7, rr(S, 2))),
        dot(6, 17.5, 0.9), dot(9.5, 17.5, 0.9), dot(13, 17.5, 0.9), dot(16.5, 17.5, 0.9),
    ]


# ============================================================================ chunk 5

@icon("bulging-capacitor", CAT, "Cylindrical capacitor with a swollen domed top and a drip leaking down its side, standing on a board",
      tags=["blown capacitor", "swollen capacitor", "failed component", "motherboard repair", "electrolytic", "leaking"])
def _(S):
    return [
        line(seg(2, 21, 22, 21)),
        shell("M6 19V9C6 3.5 16 3.5 16 9V19Z"),
        detail(seg(6, 15, 16, 15)),
        line(seg(19.5, 9, 19.5, 12)),
        dot(19.5, 15.5, 1.3),
    ]


@icon("haptic-vest", CAT, "Sleeveless vest from the front with a grid of small feedback pads on the chest",
      tags=["vr vest", "haptic suit", "force feedback", "wearable", "full body vr", "gaming vest"])
def _(S):
    return [
        shell("M8 3L4 6.5V21H20V6.5L16 3A4 4 0 0 1 8 3Z", stroke_miterlimit="3") if S.name == "line"
        else shell("M8 3L4 6.5V21H20V6.5L16 3A4 4 0 0 1 8 3Z"),
        dot(8.5, 12, 1), dot(12, 12, 1), dot(15.5, 12, 1),
        dot(8.5, 16, 1), dot(12, 16, 1), dot(15.5, 16, 1),
    ]


@icon("bnc-t-connector", CAT, "T-shaped coaxial connector with a round bayonet end on each of its three arms",
      tags=["coax", "coaxial splitter", "bnc tee", "video cable", "network 10base2", "connector"])
def _(S):
    return [
        line(seg(6.5, 10, 17.5, 10)),
        line(seg(12, 10, 12, 15.5)),
        shell(rect(1.5, 6, 5, 8, rr(S, 3))),
        shell(rect(17.5, 6, 5, 8, rr(S, 3))),
        shell(rect(8.5, 15.5, 7, 6, rr(S, 3))),
    ]


@icon("hard-drive-degausser", CAT, "Machine with a wide front slot, a hard drive entering and curved magnetic field lines around it",
      tags=["data destruction", "drive wiper", "erase disk", "magnetic eraser", "secure disposal", "media destruction"])
def _(S):
    return [
        shell(rect(7.5, 2, 9, 7, rr(S, 2))),
        line(arc(12, 5.5, 8.5, 150, 210)), line(arc(12, 5.5, 8.5, -30, 30)),
        shell(rect(2, 11, 20, 10, rr(S, 3))),
        sq(5, 14.5, 14, 2.5),
    ]


@icon("power-supply-tester", CAT, "Handheld tester with a readout at the top and connector sockets of different sizes below",
      tags=["psu tester", "atx tester", "voltage check", "pc repair", "multimeter", "diagnostic tool"])
def _(S):
    return [
        shell(rect(5, 2, 14, 20, rr(S, 3))),
        sq(8, 5, 8, 4),
        sq(8, 12, 3, 3), sq(13, 12, 3, 3), sq(8, 17, 8, 2.5),
    ]


@icon("post-diagnostic-card", CAT, "Expansion card with a two-digit display and gold contacts along the bottom edge",
      tags=["post card", "debug card", "motherboard diagnostics", "boot error code", "pci card", "pc repair"])
def _(S):
    return [
        shell(rect(2, 3, 20, 13, rr(S, 3))),
        detail(rect(6, 7.5, 5, 5)), detail(rect(13, 7.5, 5, 5)),
        sq(4, 18.5, 2, 3), sq(7.5, 18.5, 2, 3), sq(11, 18.5, 2, 3), sq(14.5, 18.5, 2, 3), sq(18, 18.5, 2, 3),
    ]


@icon("delta-3d-printer", CAT, "Tall frame with three arms meeting at one print head above a round bed",
      tags=["delta printer", "3d printing", "rostock", "additive manufacturing", "fdm", "maker"])
def _(S):
    return [
        line(seg(4, 3, 4, 21)), line(seg(20, 3, 20, 21)),
        line(seg(4, 3, 20, 3)), line(seg(2, 21, 22, 21)),
        line(seg(4, 3, 12, 10)), line(seg(20, 3, 12, 10)), line(seg(12, 3, 12, 10)),
        dot(12, 11.5, 1.5),
        line(seg(7, 17, 17, 17)),
    ]


@icon("fanless-industrial-pc", CAT, "Compact box covered in deep parallel cooling fins with a row of ports along the front",
      tags=["passive cooling", "embedded pc", "rugged computer", "heatsink case", "edge computer", "industrial computer"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, rr(S, 3))),
        detail(seg(6, 3, 6, 13)), detail(seg(10, 3, 10, 13)), detail(seg(14, 3, 14, 13)), detail(seg(18, 3, 18, 13)),
        dot(6, 17.5, 1), dot(10, 17.5, 1), dot(14, 17.5, 1), sq(17, 16.5, 3, 2),
    ]


@icon("sata-usb-adapter", CAT, "Short cable with an L-shaped drive connector on one end and a USB plug on the other",
      tags=["drive adapter", "sata to usb", "disk dock cable", "hard drive cable", "external drive", "data recovery"])
def _(S):
    return [
        shell(poly([(2, 6), (9, 6), (9, 11), (6, 11), (6, 16), (2, 16)], closed=True, r=S.r * 0.6)),
        line(poly([(9, 8.5), (12.5, 8.5), (12.5, 13.5), (16, 13.5)], r=S.r)),
        shell(rect(16, 10, 6, 7, rr(S, 1.5))),
    ]


@icon("loopback-plug", CAT, "Small network plug with a short loop of wire running out of its back and returning into it",
      tags=["loopback adapter", "test plug", "network test", "ethernet loop", "port test", "serial loopback"])
def _(S):
    return [
        shell(rect(2, 7, 12, 10, rr(S, 3))),
        dot(5.5, 12, 0.9), dot(8, 12, 0.9), dot(10.5, 12, 0.9),
        line("M14 9.5H18A2.5 2.5 0 0 1 18 14.5H14"),
    ]


@icon("network-operations-center", CAT, "Large wall display showing a graph above two operator monitors seen from behind",
      tags=["noc", "control room", "monitoring wall", "ops center", "dashboard wall", "sysadmin"])
def _(S):
    return [
        shell(rect(2, 2, 20, 9, rr(S, 2))),
        line(poly([(5, 8), (9, 5.5), (13, 7.5), (19, 5)], r=0)),
        shell(rect(4, 15, 6, 4, rr(S, 1.5))), shell(rect(14, 15, 6, 4, rr(S, 1.5))),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("depth-camera", CAT, "Horizontal camera bar with three lenses, the middle one larger, on a small tripod",
      tags=["3d camera", "stereo camera", "lidar camera", "motion sensor", "tof sensor", "kinect style"])
def _(S):
    return [
        shell(rect(2, 4, 20, 8, rr(S, 3))),
        dot(6, 8, 1.2), dot(12, 8, 2), dot(18, 8, 1.2),
        line(seg(12, 12, 12, 16)),
        line(poly([(7, 21), (12, 16), (17, 21)], r=S.r)),
    ]


@icon("laptop-charging-cart", CAT, "Wheeled cabinet with laptops standing upright in a row of slots",
      tags=["laptop cart", "classroom laptops", "charging trolley", "device storage", "school", "sync cart"])
def _(S):
    return [
        shell(rect(3, 2, 18, 15, rr(S, 2.5))),
        detail(seg(7, 2, 7, 12)), detail(seg(10.5, 2, 10.5, 12)), detail(seg(14, 2, 14, 12)), detail(seg(17.5, 2, 17.5, 12)),
        dot(6, 20.5, 1.25), dot(18, 20.5, 1.25),
    ]


@icon("projector-mount", CAT, "Projector hanging from a ceiling pole with a light beam angled forward",
      tags=["ceiling projector", "bracket", "classroom", "presentation", "home theater", "hanging projector"])
def _(S):
    return [
        line(seg(2, 2.5, 22, 2.5)),
        line(seg(9, 2.5, 9, 8)),
        shell(rect(3, 8, 13, 6, rr(S, 2))),
        dot(13, 11, 1.5),
        line(seg(18, 9.5, 22, 6.5)), line(seg(18, 12.5, 22, 16)),
    ]


@icon("mouse-jiggler", CAT, "Mouse resting on a small platform with curved motion lines around it",
      tags=["mouse mover", "keep awake", "idle prevention", "cursor mover", "stay active", "screen lock"])
def _(S):
    return [
        shell(rect(8, 3, 8, 11, rr(S, 4))),
        detail(seg(12, 5.5, 12, 8)),
        line(arc(12, 8.5, 9.5, 155, 205)), line(arc(12, 8.5, 9.5, -25, 25)),
        shell(rect(2, 16, 20, 5, rr(S, 2.5))),
    ]


@icon("wifi-antenna", CAT, "Rubber antenna standing on a threaded base connector with signal arcs beside its tip",
      tags=["wireless antenna", "sma antenna", "external antenna", "router antenna", "aerial", "signal booster"])
def _(S):
    return [
        shell(rect(9.5, 3, 5, 14, rr(S, 2.5))),
        shell(rect(8, 17, 8, 4, rr(S, 1.5))),
        line(arc(12, 7, 6.5, -35, 35)), line(arc(12, 7, 9.5, -35, 35)),
        line(arc(12, 7, 6.5, 145, 215)), line(arc(12, 7, 9.5, 145, 215)),
    ]


@icon("magnetic-core-memory", CAT, "Grid of tiny rings with horizontal and vertical wires crossing through them",
      tags=["core memory", "vintage ram", "retro computing", "ferrite core", "early computer memory", "history"])
def _(S):
    xs = (7, 17)
    return [
        *[line(seg(2.5, y, 21.5, y)) for y in xs],
        *[line(seg(x, 2.5, x, 21.5)) for x in xs],
        *[shell(circle(x, y, 3.5)) for x in xs for y in xs],
    ]


@icon("keypunch-machine", CAT, "Desk-like machine with a card hopper and card stacker on top and a keyboard at the front",
      tags=["punch card", "vintage computer", "data entry", "mainframe era", "card punch", "history"])
def _(S):
    return [
        shell(rect(3, 3, 6, 8, rr(S, 1.5))), shell(rect(15, 3, 6, 8, rr(S, 1.5))),
        shell(rect(2, 12, 20, 9, rr(S, 2.5))),
        dot(6, 16.5, 1), dot(9.5, 16.5, 1), dot(13, 16.5, 1), dot(16.5, 16.5, 1),
    ]


@icon("personal-digital-assistant", CAT, "Handheld organizer with a small screen, a row of round buttons and a stylus beside it",
      tags=["pda", "palm pilot", "handheld", "organiser", "stylus device", "retro gadget"])
def _(S):
    return [
        shell(rect(3, 2, 12, 20, rr(S, 3))),
        detail(rect(5.5, 5, 7, 6, 0)),
        dot(6.5, 16.5, 1), dot(9, 16.5, 1), dot(11.5, 16.5, 1),
        shell(poly([(18, 4), (21, 4), (21, 17), (19.5, 20), (18, 17)], closed=True, r=S.r * 0.4)),
    ]


@icon("analog-computer", CAT, "Upright panel with two round dials, patch sockets and a looped patch cord",
      tags=["patch panel", "vintage computer", "dials", "retro computing", "analogue computer", "plugboard"])
def _(S):
    return [
        shell(rect(3, 2, 18, 20, rr(S, 3))),
        shell(circle(8, 7, 2.5)), shell(circle(16, 7, 2.5)),
        dot(7, 13, 1), dot(12, 13, 1), dot(17, 13, 1),
        line("M7 13V16A5 5 0 0 0 17 16V13"),
    ]
