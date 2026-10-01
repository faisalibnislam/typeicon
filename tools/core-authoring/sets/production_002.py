"""TypeIcon Core: production (theatre, film and video), batch 2.

Viewfinder icons keep the frame as the only shell; everything inside it is a detail or a knocked-out dot so the
Filled style reads as a solid frame with the drawing cut out of it.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "production"


def ko(d) -> Part:
    """Solid region: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def frame(S, x=2, y=4, w=20, h=16):
    return shell(rect(x, y, w, h, S.R))


def rotp(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


# ============================================================================ shot types

@icon("close-up-shot", CAT, "Viewfinder frame filled by a large head and shoulders",
      tags=["close-up", "closeup", "camera shot", "framing", "film", "face", "cinematography"])
def _(S):
    return [frame(S), detail(circle(12, 10.5, 4)), detail("M6 20a6 5 0 0 1 12 0")]


@icon("extreme-close-up-shot", CAT, "Viewfinder frame filled edge to edge by a single eye",
      tags=["extreme close-up", "eye", "camera shot", "framing", "film", "detail shot", "cinematography"])
def _(S):
    return [frame(S, 2, 4, 20, 16),
            detail("M6 12Q12 6.5 18 12Q12 17.5 6 12Z"), ko(circle(12, 12, 2))]


@icon("wide-shot", CAT, "Viewfinder frame with a small full body figure standing on a ground line",
      tags=["wide shot", "long shot", "full body", "camera shot", "framing", "film", "cinematography"])
def _(S):
    return [frame(S), detail("M5 16.5H19"), ko(circle(12, 7.5, 1.6)),
            detail("M12 9.5V13M12 13L10.5 16M12 13L13.5 16")]


@icon("medium-shot", CAT, "Viewfinder frame showing a figure from the waist up",
      tags=["medium shot", "waist up", "camera shot", "framing", "film", "cinematography", "torso"])
def _(S):
    return [frame(S), detail(circle(12, 9.5, 2.5)), detail("M7 20v-2a5 4 0 0 1 10 0v2")]


@icon("two-shot", CAT, "Viewfinder frame with two figures side by side from the waist up",
      tags=["two shot", "two people", "camera shot", "framing", "film", "conversation", "cinematography"])
def _(S):
    return [frame(S), ko(circle(8, 10, 2)), ko(circle(16, 10, 2)),
            detail("M4.5 20v-2a3.5 3.5 0 0 1 7 0v2"), detail("M12.5 20v-2a3.5 3.5 0 0 1 7 0v2")]


@icon("over-the-shoulder-shot", CAT, "Viewfinder frame with the back of a large head in the corner facing a smaller figure",
      tags=["over the shoulder", "ots", "camera shot", "framing", "film", "dialogue", "cinematography"])
def _(S):
    return [frame(S), ko(circle(8, 11, 3.5)), ko("M3.5 20a4.5 4.5 0 0 1 9 -0.5V20Z"),
            ko(circle(17, 9, 1.75)), detail("M14 16a3 3 0 0 1 6 0")]


@icon("point-of-view-shot", CAT, "Eye beside a viewfinder frame showing two arms reaching forward",
      tags=["pov", "first person", "camera shot", "framing", "film", "subjective", "cinematography"])
def _(S):
    return [shell(rect(9, 4, 13, 16, S.R)), detail("M13 19.5V13M18 19.5V13"),
            ko(rect(11.5, 8.5, 3, 4.5, 1)), ko(rect(16.5, 8.5, 3, 4.5, 1)),
            line("M1 12Q4.25 7.5 7.5 12Q4.25 16.5 1 12"), dot(4.25, 12, 1.4)]


@icon("dutch-angle", CAT, "Viewfinder frame with a building and horizon tilted on a strong diagonal",
      tags=["dutch tilt", "canted angle", "tilted", "camera shot", "framing", "film", "cinematography"])
def _(S):
    b = rotp([(8, 14), (8, 8), (13, 8), (13, 14)], -20, 12, 13)
    return [frame(S), detail(poly(b, closed=True)), detail(seg(4.5, 16.5, 19.5, 11.5))]


@icon("overhead-shot", CAT, "Viewfinder frame looking straight down on a head and shoulders from above",
      tags=["overhead", "top down", "birds eye", "camera shot", "framing", "film", "cinematography"])
def _(S):
    return [frame(S), detail(rect(6, 8.5, 12, 7, 3.5)), ko(circle(12, 12, 2.25))]


@icon("dolly-zoom", CAT, "Nested viewfinder frames joined by diagonals like a zoom tunnel",
      tags=["vertigo effect", "zoom", "perspective", "camera move", "film", "contra zoom", "cinematography"])
def _(S):
    return [frame(S), detail(rect(8, 9, 8, 6, 0)),
            detail(seg(5, 7, 8, 9) + seg(19, 7, 16, 9) + seg(5, 17, 8, 15) + seg(19, 17, 16, 15))]


@icon("tracking-shot", CAT, "Camera on a wheeled dolly following behind a walking figure",
      tags=["follow shot", "dolly", "camera move", "film", "track", "moving camera", "cinematography"])
def _(S):
    return [shell(rect(2, 6, 8, 6, min(S.R, 1.5))), shell(poly([(10, 8), (13, 6.5), (13, 11.5), (10, 10)], closed=True, r=S.r * 0.3)),
            shell(rect(2, 14, 11, 2, 0)), dot(5, 19, 1.75), dot(10, 19, 1.75),
            dot(19, 5, 1.75), line(poly([(19, 7.5), (18, 13)], r=0) + "M18 13L15.5 18M18 13L20.5 15.5L20 19")]


@icon("establishing-shot", CAT, "Wide viewfinder frame showing a city skyline with a small title bar in the corner",
      tags=["skyline", "city", "scene opener", "camera shot", "framing", "film", "location shot"])
def _(S):
    return [frame(S), ko(rect(5, 13, 3, 6)), ko(rect(9.5, 8.5, 4, 10.5)), ko(rect(15, 12, 3.5, 7)),
            detail("M15 8H19")]


@icon("panning-shot", CAT, "Sharp car in the centre of a frame with speed streaks behind it",
      tags=["pan", "motion blur", "following", "camera move", "film", "speed", "cinematography"])
def _(S):
    car = poly([(10, 16), (10, 13), (12, 10.5), (16, 10.5), (18, 13), (19, 13), (19, 16)], closed=True)
    return [frame(S), detail(car), ko(circle(12.5, 16.5, 1.5)), ko(circle(16.5, 16.5, 1.5)),
            detail("M5 10H8M5 13H8M5 16H8")]


# ============================================================================ editing and video tools

@icon("razor-edit-tool", CAT, "Razor blade hovering above a timeline clip that has a cut line through it",
      tags=["razor", "blade", "cut", "split clip", "video editing", "timeline", "slice"])
def _(S):
    return [shell(poly([(5, 2.5), (19, 2.5), (21.5, 5.75), (19, 9), (5, 9), (2.5, 5.75)], closed=True, r=S.r * 0.5)),
            detail("M9.5 5.75H14.5"), shell(rect(2, 13, 20, 8, S.R)), detail("M12 13V21")]


@icon("trim-clip", CAT, "Timeline clip with a square bracket handle gripping its start",
      tags=["trim", "clip edge", "ripple trim", "video editing", "timeline", "shorten", "in point"])
def _(S):
    return [shell(rect(8, 9, 14, 6, min(S.R, 2))), line(poly([(6, 4.5), (3, 4.5), (3, 19.5), (6, 19.5)], r=S.r * 0.5))]


@icon("dissolve-transition", CAT, "Two overlapping clip rectangles with crossing fade lines where they overlap",
      tags=["cross dissolve", "crossfade", "video transition", "video editing", "blend", "fade between clips", "timeline"])
def _(S):
    return [shell(rect(2, 4, 13, 10, S.R)), shell(rect(9, 10, 13, 10, S.R)),
            detail(seg(10, 11, 14, 13) + seg(10, 13, 14, 11))]


@icon("wipe-transition", CAT, "Frame split by a diagonal edge with one side solid and an arrow moving across",
      tags=["wipe", "video transition", "video editing", "reveal", "slide transition", "diagonal wipe", "scene change"])
def _(S):
    return [frame(S, 2, 4, 20, 16), ko(poly([(3.5, 5.5), (13, 5.5), (9, 18.5), (3.5, 18.5)], closed=True)),
            detail("M15 12H19.5"), detail("M17.5 10L19.5 12L17.5 14")]


def _fade_filled():
    ring1 = D(P(rect(1, 6, 7, 12)), P(rect(3, 8, 3, 8)))
    half = D(P(rect(8.5, 6, 7, 12)), P(rect(10.5, 8, 3, 3)))
    return U(ring1, half, P(rect(16, 6, 7, 12)))


@icon("fade-to-black", CAT, "Row of three frames going from empty to half filled to solid",
      tags=["fade out", "fade in", "video transition", "video editing", "dip to black", "darken", "ending"],
      filled=_fade_filled)
def _(S):
    rr = 1 if S.name == 'line' else 2
    return [shell(rect(2, 7, 5, 10, rr)), shell(rect(9.5, 7, 5, 10, rr)), shell(rect(17, 7, 5, 10, rr)),
            solid(rect(9.5, 12, 5, 5)), solid(rect(17, 7, 5, 10))]


@icon("render-queue", CAT, "Stack of three video frames with a progress bar running beneath them",
      tags=["export", "rendering", "batch render", "video editing", "queue", "progress", "encode"])
def _(S):
    return [line("M6 3.5H18"), line("M4 7H20"),
            shell(rect(2, 10, 20, 7, min(S.R, 2))),
            ko(poly([(10.5, 11.5), (10.5, 15.5), (14, 13.5)], closed=True)),
            line("M2 21H13"), line("M16 21H22")]


@icon("timeline-marker", CAT, "Timeline ruler with a pentagon marker hanging from it and a thin line dropping down",
      tags=["playhead", "marker", "flag", "video editing", "cue point", "ruler", "chapter"])
def _(S):
    return [line("M2 3.5H22"), line("M4.5 3.5V7M19.5 3.5V7"),
            shell(poly([(8.5, 5), (15.5, 5), (15.5, 10), (12, 13.5), (8.5, 10)], closed=True, r=S.r * 0.6)),
            line("M12 13.5V21")]


@icon("motion-tracking", CAT, "Corner bracket target around a dot with a trail of smaller dots behind it",
      tags=["track point", "tracker", "video effects", "follow object", "post production", "target", "visual effects"])
def _(S):
    t = []
    x0, y0, x1, y1 = 11, 2.5, 21, 12.5
    t.append(line(poly([(x0, y0 + 3), (x0, y0), (x0 + 3, y0)], r=S.r * 0.4)))
    t.append(line(poly([(x1 - 3, y0), (x1, y0), (x1, y0 + 3)], r=S.r * 0.4)))
    t.append(line(poly([(x0, y1 - 3), (x0, y1), (x0 + 3, y1)], r=S.r * 0.4)))
    t.append(line(poly([(x1 - 3, y1), (x1, y1), (x1, y1 - 3)], r=S.r * 0.4)))
    return t + [dot(16, 7.5, 1.75), dot(10, 13, 1.5), dot(6.5, 16, 1.25), dot(3.5, 19, 1.1)]


@icon("lut-cube", CAT, "Isometric cube with one face shaded, for a colour lookup table",
      tags=["lut", "color grading", "colour grade", "look up table", "3d lut", "video color", "color correction"])
def _(S):
    hexa = regular(12, 12, 9.5, 6)
    return [shell(poly(hexa, closed=True, r=S.r)),
            detail(poly([hexa[5], (12, 12), hexa[1]]) + poly([(12, 12), hexa[3]])),
            ko(poly([(6, 9.8), (10.4, 12.4), (10.4, 17.6), (6, 15)], closed=True))]


@icon("vectorscope", CAT, "Round scope with six small target boxes around its ring and a trace in the centre",
      tags=["scope", "color scope", "chroma", "video monitoring", "waveform", "color correction", "saturation"])
def _(S):
    parts = [shell(circle(12, 12, 9.5))]
    for k in range(6):
        x, y = polar(12, 12, 6, -75 + 60 * k)
        parts.append(ko(rect(x - 1.25, y - 1.25, 2.5, 2.5)))
    parts.append(detail("M12 12L15 8"))
    return parts


@icon("title-safe-area", CAT, "Screen with corner guides set inside its edge and two short text lines in the middle",
      tags=["safe area", "safe zone", "overscan", "broadcast", "video editing", "caption safe", "guides"])
def _(S):
    return [frame(S, 2, 3, 20, 18),
            detail("M5.5 9V6.5H8M16 6.5H18.5V9M5.5 15V17.5H8M16 17.5H18.5V15"),
            detail("M9 10.5H15M9 13.5H13")]


@icon("letterboxed-video", CAT, "Screen with solid bars across the top and bottom and a play mark in the middle",
      tags=["letterbox", "widescreen", "cinemascope", "aspect ratio", "black bars", "cinema", "video"])
def _(S):
    return [frame(S, 2, 4, 20, 16), ko(rect(3, 5, 18, 3)), ko(rect(3, 16, 18, 3)),
            ko(poly([(10, 9.75), (10, 14.25), (14, 12)], closed=True))]


@icon("zebra-stripes-warning", CAT, "Viewfinder frame with diagonal stripes over an overexposed patch and a bright dot",
      tags=["zebra", "overexposure", "exposure warning", "camera", "clipping", "highlights", "video monitor"])
def _(S):
    return [frame(S, 2, 4, 20, 16), dot(7, 9, 1.75),
            detail("M8 17L18 7M13.5 18.5L19 13")]


@icon("4k-video", CAT, "Screen outline with the characters 4K inside it",
      tags=["4k", "uhd", "ultra hd", "resolution", "high definition", "video quality", "2160p"])
def _(S):
    return [frame(S, 2, 4, 20, 16), detail("M10 8V16M10 8L6 13.5H11.5"),
            detail("M14.5 8V16M19 8L14.5 12L19 16")]


@icon("auto-reframe", CAT, "Wide frame with a tall crop frame inside it centred on a person",
      tags=["reframe", "crop", "vertical video", "aspect ratio", "subject tracking", "video editing", "smart crop"])
def _(S):
    return [frame(S, 2, 4, 20, 16), detail(rect(8.5, 7.5, 7, 9, 0)),
            ko(circle(12, 10.5, 1.4)), ko(rect(10.25, 12.75, 3.5, 2, 1))]


@icon("scene-detection", CAT, "Film strip with a cut line down its middle and a sparkle above the cut",
      tags=["scene cut", "auto cut", "split scenes", "video analysis", "film", "shot boundary", "smart edit"])
def _(S):
    return [shell(rect(2, 12, 20, 9, S.R)), detail("M12 12V21"),
            ko(poly([(12, 2), (13.2, 5.3), (16.5, 6.5), (13.2, 7.7), (12, 11), (10.8, 7.7), (7.5, 6.5), (10.8, 5.3)], closed=True))]


# ============================================================================ theatre and stagecraft

def union_d(*ds):
    from dsl import path_to_d
    return path_to_d(U(*[P(d) for d in ds]))


@icon("theater-box-seat", CAT, "Balcony box with a draped swag above and two people leaning over its rail",
      tags=["opera box", "balcony", "theatre seating", "private box", "performance", "audience", "royal box"])
def _(S):
    return [line("M3 3Q7.5 8.5 12 3Q16.5 8.5 21 3"),
            ko(circle(8, 10, 2)), ko(circle(16, 10, 2)),
            ko("M5 15a3 3.5 0 0 1 6 0Z"), ko("M13 15a3 3.5 0 0 1 6 0Z"),
            shell(rect(2.5, 15, 19, 6, S.R))]


@icon("ghost-light", CAT, "Bare light bulb in a cage on a tall stand, left burning on an empty stage",
      tags=["theatre tradition", "stage light", "bulb", "lamp", "superstition", "empty stage", "work light"])
def _(S):
    return [shell(circle(12, 6.5, 4)), detail("M12 2.5V10.5"), line("M12 10.5V19"),
            line("M7.5 21.5L12 18.5L16.5 21.5"), line("M2.5 6.5H5M19 6.5H21.5")]


@icon("stage-flat", CAT, "Back of a scenery panel showing its wooden frame rails and a diagonal brace",
      tags=["scenery", "set piece", "backdrop panel", "theatre set", "set building", "stagecraft", "wall flat"])
def _(S):
    return [shell(rect(5, 3, 14, 18, S.R * 0.5)), detail("M5 12H19"), detail("M5 12L19 21")]


@icon("stage-fly-system", CAT, "Pulley with a rope running down to a hanging scenery batten and a counterweight",
      tags=["fly loft", "rigging", "batten", "counterweight", "scenery lift", "theatre rigging", "flies"])
def _(S):
    return [shell(circle(12, 5, 3)), line("M9 5V14M15 5V11.5"), line("M3 14H11"),
            shell(rect(4, 16, 6, 5, min(S.R, 1.5))), shell(rect(13, 11.5, 4, 7, min(S.R, 1.5)))]


@icon("revolving-stage", CAT, "Round turntable stage platform with a curved rotation arrow above it",
      tags=["turntable stage", "rotating stage", "scene change", "theatre machinery", "spin", "platform", "rotate"])
def _(S):
    return [shell("M3 15A9 4 0 0 1 21 15V18A9 4 0 0 1 3 18Z"), detail("M3 15A9 4 0 0 0 21 15"),
            line("M5 10A8 6.5 0 0 1 19 7.5"), line(poly([(19.5, 3.5), (19.5, 8), (15, 8)], r=S.r * 0.5))]


@icon("theater-in-the-round", CAT, "Top down round stage ringed by curved seat rows broken by aisles",
      tags=["arena stage", "central staging", "circular theatre", "seating plan", "audience", "theatre layout", "in the round"])
def _(S):
    parts = [shell(circle(12, 12, 2.75))]
    for k in range(4):
        parts.append(line(arc(12, 12, 6.25, 50 + 90 * k, 130 + 90 * k)))
        parts.append(line(arc(12, 12, 9.5, 20 + 90 * k, 70 + 90 * k)))
    return parts


@icon("wig-head", CAT, "Mannequin head on a short stand wearing a full curly wig",
      tags=["wig", "hairpiece", "hair stand", "costume", "theatre hair", "mannequin", "curls"])
def _(S):
    wig = union_d(circle(12, 11.5, 6), circle(7.5, 7.5, 3), circle(12, 5.5, 3), circle(16.5, 7.5, 3),
                  circle(6, 13, 2.75), circle(18, 13, 2.75))
    return [shell(wig), ko(circle(9.75, 12.5, 1)), ko(circle(14.25, 12.5, 1)), line("M12 18V21"), line("M8.5 21.5H15.5")]


@icon("costume-rack", CAT, "Rolling clothes rail on wheels with two costumes hanging from it",
      tags=["wardrobe", "garment rail", "clothes rack", "theatre costumes", "dress rail", "backstage", "hanging clothes"])
def _(S):
    return [line("M3 4.5H21"), line("M3.5 4.5V19M20.5 4.5V19"), line("M3.5 19H20.5"),
            shell(poly([(9, 6), (7, 15.5), (11.5, 15.5)], closed=True, r=S.r * 0.4)),
            shell(poly([(15, 6), (13, 15.5), (17.5, 15.5)], closed=True, r=S.r * 0.4)),
            dot(3.5, 21, 1.25), dot(20.5, 21, 1.25)]


@icon("spike-mark", CAT, "Stage floor seen from above with a T shaped tape mark and a footprint beside it",
      tags=["floor tape", "blocking", "position mark", "stage mark", "actor position", "theatre", "footprint"])
def _(S):
    return [line("M3 7H12"), line("M7.5 7V19"), ko(ellipse(18, 9.5, 2.25, 3.5)), ko(circle(18, 16, 1.75))]


@icon("surtitle-screen", CAT, "Wide narrow text screen hung on two cables above a stage opening",
      tags=["surtitles", "supertitles", "captions", "opera", "translation display", "theatre captions", "subtitle board"])
def _(S):
    return [line("M6 2.5V8M18 2.5V8"), shell(rect(2, 8, 20, 10, min(S.R, 2))), detail("M6 12H18M8 15H16")]


@icon("thunder-sheet", CAT, "Large thin metal sheet hanging from a bar with wobble lines and a bolt beside it",
      tags=["sound effect", "foley", "theatre effects", "thunder", "metal sheet", "storm", "backstage"])
def _(S):
    return [line("M3 3.5H15"), line("M6 3.5V6M13 3.5V6"), shell(rect(4.5, 6, 10, 14, min(S.R, 1.5))),
            detail("M8 9.5Q10 11.5 8 13.5Q6 15.5 8 17.5"),
            solid(poly([(20, 3), (16.5, 12), (19.5, 12), (18, 21), (22.5, 10), (19.5, 10), (22, 3)], closed=True))]


@icon("wind-machine", CAT, "Slatted drum on a stand with a crank handle at its side",
      tags=["sound effect", "foley", "theatre effects", "wind", "crank", "storm sound", "backstage"])
def _(S):
    return [shell(circle(10, 10, 7)), detail("M6.5 6V14M10 3V17M13.5 6V14"), line("M17 10H21V16"),
            line("M6 16L4 21M14 16L16 21")]


@icon("vaudeville-hook", CAT, "Long cane with a large curved hook reaching out from the edge of a curtain",
      tags=["shepherds crook", "stage hook", "comedy", "vaudeville", "variety act", "pull off stage", "gag prop"])
def _(S):
    return [shell(poly([(2, 3), (8, 3), (6.5, 21), (2, 21)], closed=True, r=S.r * 0.5)), detail("M5 3L4.5 21"),
            line("M8.5 15H16.5A3.75 3.75 0 1 0 12.75 11.25")]


# ============================================================================ sound, light and broadcast

@icon("stagebox", CAT, "Metal box with a grid of round connector sockets on its face and a thick cable leaving one side",
      tags=["stage box", "snake", "audio patch", "xlr", "connector panel", "sound desk", "live sound"])
def _(S):
    sockets = [ko(circle(x, y, 1.4)) for y in (9.5, 14.5) for x in (6.5, 10.5, 14.5)]
    return [shell(rect(2.5, 5, 15, 14, S.R)), *sockets, line("M17.5 12H19A2.5 2.5 0 0 1 21.5 14.5V21")]


@icon("in-ear-monitor", CAT, "Ear outline with a moulded earpiece in it and a thin cable trailing away",
      tags=["iem", "ear monitor", "earpiece", "stage monitoring", "earphone", "musician", "wireless pack"])
def _(S):
    return [line("M10.5 17.5C8 12 8 4.5 14.5 3.5C19.5 3 21 9 18 12C16.5 14 17 17 15 19C13 21 10.5 20 10.5 17.5"),
            ko(ellipse(13.5, 11, 2, 3)), line("M12 14.5C10 17 7 18.5 2.5 17")]


@icon("line-array-speaker", CAT, "Fan shaped stack of speaker boxes hanging from a rigging bar",
      tags=["pa system", "loudspeaker", "concert sound", "flown speakers", "sound reinforcement", "rigging", "speaker cluster"])
def _(S):
    return [line("M5 2.5H19"), line("M12 2.5V4.5"),
            shell(poly([(6.5, 5), (17.5, 5), (21, 21), (3, 21)], closed=True, r=S.r * 0.4)),
            detail("M5.4 10.3H18.6M4.3 15.7H19.7")]


@icon("confetti-cannon", CAT, "Handheld tube cannon angled upward bursting a spray of small confetti pieces",
      tags=["party popper", "celebration", "launcher", "wedding", "stage effect", "streamers", "burst"])
def _(S):
    tube = rotp([(3, 15), (3, 20), (13, 20), (9, 15)], 0)
    body = poly([(3, 21), (6.5, 11), (12.5, 13.5), (9.5, 21)], closed=True, r=S.r * 0.4)
    return [shell(body), ko(rect(14, 4, 2.5, 2.5)), ko(rect(19, 8, 2.5, 2.5)), ko(rect(11, 5, 2, 2)),
            dot(17, 12, 1.2), dot(14, 9, 1.1), dot(21, 4.5, 1.2),
            line("M9 10Q10 6 14 2")]


@icon("stage-pyrotechnics", CAT, "Row of floor boxes along a stage edge each shooting a tall column of flame",
      tags=["fire effect", "flame", "stage fire", "concert effects", "special effects", "flame projector", "pyro"])
def _(S):
    parts = []
    for x in (4.5, 12, 19.5):
        parts.append(shell(rect(x - 2.5, 18.5, 5, 3, 0.5)))
        parts.append(shell(f"M{fmt(x)} 16C{fmt(x - 3.5)} 13 {fmt(x - 2)} 9.5 {fmt(x)} 4C{fmt(x + 2)} 9.5 {fmt(x + 3.5)} 13 {fmt(x)} 16Z"))
    return parts


@icon("projection-mapping", CAT, "Building facade with a projector beam from the side and a pattern painted across it",
      tags=["video mapping", "building projection", "light show", "projector", "facade", "visual art", "spatial augmented reality"])
def _(S):
    parts = [shell(rect(12, 3, 10, 18, S.R)), shell(rect(2, 10.5, 5, 4, S.R * 0.5)),
             line("M7 11.5L12 6M7 13.5L12 19")]
    for y in (6.5, 11, 15.5):
        for x in (14.5, 18.5):
            parts.append(ko(rect(x, y, 2, 2)))
    return parts

@icon("hologram-display", CAT, "Round base sending light up around a small figure floating above it",
      tags=["hologram", "holographic", "3d projection", "futuristic", "projection", "virtual display", "sci-fi"])
def _(S):
    return [shell(poly([(5, 21), (8, 17), (16, 17), (19, 21)], closed=True, r=S.r * 0.4)),
            line("M7.5 14.5L4.5 4.5M16.5 14.5L19.5 4.5"), ko(circle(12, 7.5, 2)), ko("M8.5 14a3.5 3.5 0 0 1 7 0Z")]


@icon("mic-flag", CAT, "Handheld microphone with a square flag fitted around its shaft below the grille",
      tags=["mic cube", "station flag", "microphone branding", "broadcast", "interview", "news", "logo cube"])
def _(S):
    return [shell(circle(12, 5.5, 3.5)), shell(rect(5.5, 10.5, 13, 6, min(S.R, 2))), detail("M9 13.5H15"),
            shell(rect(10.5, 16.5, 3, 5, min(S.R, 1.5)))]


@icon("cue-light", CAT, "Small box on a stand with one lamp lit above a push button",
      tags=["cue lamp", "stage manager", "go light", "backstage", "signal light", "theatre", "show control"])
def _(S):
    return [shell(rect(6, 2.5, 12, 13, S.R)), ko(circle(12, 7, 2.5)), ko(circle(12, 12.5, 1.25)),
            line("M12 15.5V21"), line("M8 21H16"), line("M2.5 5L4 6M2.5 9L4 8.5M21.5 5L20 6M21.5 9L20 8.5")]


@icon("news-helicopter", CAT, "Helicopter side view with a round camera ball hung under its nose",
      tags=["traffic helicopter", "aerial camera", "broadcast", "gimbal", "live coverage", "news chopper", "sky camera"])
def _(S):
    return [shell(ellipse(11, 11.5, 6.5, 4.5)), line("M17 10.5H22M22 10.5V7"), line("M3 5.5H19M11 5.5V7"),
            line("M9 20H18M13 16V20"), ko(circle(5.5, 16, 2.25))]


@icon("telestrator", CAT, "Television screen showing a ringed player with a hand drawn curved arrow",
      tags=["sports analysis", "screen drawing", "broadcast", "touchscreen annotation", "replay", "pundit", "tv graphics"])
def _(S):
    return [shell(rect(2, 3.5, 20, 14, S.R)), detail(circle(8, 10.5, 2.5)), detail("M12 12C13.5 7.5 16.5 7.5 18 9.5"),
            detail("M18.5 6.5L18.5 10.5L14.5 10.5"), line("M9 21H15M12 17.5V21")]


@icon("field-reporter", CAT, "Person holding a handheld microphone, framed by a camera viewfinder",
      tags=["news reporter", "journalist", "live report", "tv interview", "correspondent", "broadcast", "on location"])
def _(S):
    return [frame(S, 2, 3, 20, 18), ko(circle(10.5, 10, 2.25)), detail("M5.5 21a5 5 0 0 1 10 0"),
            ko(rect(16, 9.5, 2.5, 4.5, 1.2)), detail("M15 17L17 14.5")]


# ============================================================================ film gear and animation

@icon("film-can", CAT, "Round flat film tin seen from above at an angle, with its lid ring and a strip of film curling out",
      tags=["film tin", "reel can", "movie canister", "film storage", "archive", "cinema", "celluloid"])
def _(S):
    return [shell("M3 11A9 6 0 0 1 21 11V15A9 6 0 0 1 3 15Z"), detail("M3 11A9 6 0 0 0 21 11"),
            ko(ellipse(12, 10, 3.5, 1.75)), line(poly([(18, 6.5), (21, 3.5), (17, 2.5)], r=S.r * 1.5))]

@icon("jog-shuttle-wheel", CAT, "Round editing controller with an outer ring around an inner dimpled jog wheel",
      tags=["jog wheel", "shuttle", "scrub", "video editing", "edit controller", "playback control", "dial"])
def _(S):
    parts = [shell(circle(12, 12, 9.5)), detail(circle(12, 12, 6))]
    rad = 0 if S.name == "line" else 0.9
    for k in range(6):
        x, y = polar(12, 12, 3, 60 * k)
        parts.append(ko(rect(x - 0.9, y - 0.9, 1.8, 1.8, rad)))
    return parts

@icon("intertitle-card", CAT, "Ornate rectangular frame with decorative corners and two centred lines of text",
      tags=["title card", "silent film", "caption card", "dialogue card", "old cinema", "movie text", "frame"])
def _(S):
    return [shell(rect(2, 4, 20, 16, S.R)), ko(rect(4.5, 6.5, 2, 2)), ko(rect(17.5, 6.5, 2, 2)),
            ko(rect(4.5, 15.5, 2, 2)), ko(rect(17.5, 15.5, 2, 2)), detail("M8.5 10.5H15.5M10 13.5H14")]


@icon("director-viewfinder", CAT, "Handheld viewfinder tube with a small eyepiece and a neck cord looping above it",
      tags=["directors finder", "framing tool", "lens viewer", "cinematography", "location scout", "film", "shot framing"])
def _(S):
    return [shell(rect(2.5, 5, 14, 9, S.R * 0.5)), shell(rect(16.5, 3.5, 5, 12, S.R * 0.5)), detail("M6 5V14"),
            line("M6 14C6 22 15 22 15 14")]

@icon("shot-list", CAT, "Clipboard with three rows, each starting with a small camera mark",
      tags=["shooting schedule", "storyboard list", "film planning", "call sheet", "production", "checklist", "camera setups"])
def _(S):
    return [shell(rect(4, 4, 16, 17, S.R)), shell(rect(9, 2, 6, 4, min(S.R, 1.5))),
            ko(rect(7, 9.5, 3, 2.5)), ko(rect(7, 13, 3, 2.5)), ko(rect(7, 16.5, 3, 2.5)),
            detail("M12.5 10.75H17M12.5 14.25H17M12.5 17.75H17")]


@icon("animation-cel", CAT, "Clear sheet with peg holes along the top edge and a painted character on it",
      tags=["cel", "cell animation", "traditional animation", "hand drawn", "acetate", "peg bar", "animator"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), ko(rect(6, 5, 3, 1.5)), ko(rect(10.5, 5, 3, 1.5)), ko(rect(15, 5, 3, 1.5)),
            detail(circle(12, 11.5, 2.5)), detail("M7.5 20a4.5 4.5 0 0 1 9 0")]


@icon("kinetoscope", CAT, "Tall cabinet with a peephole viewer on top and a hand crank on its side",
      tags=["peep show", "early cinema", "film viewer", "vintage movies", "edison", "nickelodeon", "movie history"])
def _(S):
    return [shell(rect(6, 8, 10, 13, S.R * 0.5)), shell(rect(7.5, 3, 7, 5, S.R * 0.5)), ko(circle(11, 5.5, 1)),
            detail("M6 13H16"), line("M16 14H19.5V18")]


@icon("onion-skinning", CAT, "Solid ball with two faded dashed copies trailing behind it",
      tags=["ghost frames", "previous frame", "animation guide", "frame overlay", "traditional animation", "flipbook", "echo"])
def _(S):
    parts = [shell(circle(17, 12, 4))]
    for cx in (11, 5):
        for k in range(3):
            parts.append(line(arc(cx, 12, 3.5, 10 + 120 * k, 90 + 120 * k)))
    return parts

@icon("tweening", CAT, "Two solid key poses of a ball at the ends with smaller in-between balls along the arc",
      tags=["in-betweening", "keyframes", "interpolation", "animation", "motion path", "inbetweens", "easing"])
def _(S):
    rad = 0.3 if S.name == "line" else 1.5
    return [shell(circle(5, 17, 3)), shell(circle(19, 17, 3)),
            ko(rect(7.5, 9, 3, 3, rad)), ko(rect(10.5, 6.5, 3, 3, rad)), ko(rect(13.5, 9, 3, 3, rad))]

@icon("bouncing-ball-animation", CAT, "Squashed ball flat on a ground line with a trail of balls rising away from it",
      tags=["squash and stretch", "animation principle", "bounce", "motion arc", "ball drop", "keyframe", "animator"])
def _(S):
    return [line("M2 20.5H22"), ko(ellipse(6, 18, 4, 2)), dot(10.5, 13.5, 1), dot(13, 9.5, 1.4), dot(16, 6.5, 1.8),
            dot(20, 5.5, 1.1)]


@icon("character-rig", CAT, "Stick figure skeleton of straight bones joined by round joint dots",
      tags=["skeleton", "armature", "bones", "joints", "3d animation", "ik", "puppet"])
def _(S):
    return [shell(circle(12, 4.5, 2.5)), line("M12 8.5V14M7.5 10.5H16.5M7.5 10.5L5 15.5M16.5 10.5L19 15.5"),
            line("M12 14L8.5 21M12 14L15.5 21"), dot(7.5, 10.5, 1.5), dot(16.5, 10.5, 1.5), dot(12, 14, 1.5),
            dot(5, 15.5, 1.5), dot(19, 15.5, 1.5)]


@icon("lip-sync-chart", CAT, "Grid of six small mouth shapes, each open a different amount",
      tags=["phonemes", "mouth shapes", "visemes", "animation chart", "dialogue animation", "speech", "exposure sheet"])
def _(S):
    return [frame(S, 2, 3, 20, 18), detail("M9 3.5V20.5M15 3.5V20.5M2.5 12H21.5"),
            ko(circle(5.5, 7.5, 1.4)), ko(ellipse(12, 7.5, 2, 1.1)), ko(rect(15.5, 7, 3, 1)),
            ko("M10 15.5Q12 18.5 14 15.5Z"), ko(rect(4.25, 15, 2.5, 3, 1)), ko("M15.5 17.5Q18.5 14.5 21 17.5Z")]


@icon("phenakistoscope", CAT, "Slotted disc with a ring of slots near its rim and a short handle below it",
      tags=["animation disc", "optical toy", "victorian toy", "persistence of vision", "proto cinema", "spinning disc", "zoetrope"])
def _(S):
    parts = [shell(circle(12, 10.5, 8.5)), ko(circle(12, 10.5, 1.5)), line("M12 19V22")]
    for k in range(8):
        x, y = polar(12, 10.5, 5.2, 45 * k)
        parts.append(ko(rect(x - 0.9, y - 0.9, 1.8, 1.8, 0 if S.name == "line" else 0.9)))
    return parts

@icon("walk-cycle", CAT, "Row of three small figures showing the stages of a walking step",
      tags=["walking animation", "gait", "character animation", "key poses", "animation cycle", "frame sequence", "stride"])
def _(S):
    parts = []
    poses = [("M4 12.5L1.5 20M4 12.5L6.5 20", "M4 9L2 12M4 9L6 12"),
             ("M12 12.5L11 20M12 12.5L13.5 18.5", "M12 9L12 13"),
             ("M20 12.5L17.5 20M20 12.5L22.5 20", "M20 9L18 12M20 9L22 12")]
    for (lg, ar), x in zip(poses, (4, 12, 20)):
        parts += [dot(x, 4.75, 1.75), line(seg(x, 7.5, x, 12.5)), line(lg)]
    return parts

@icon("rotoscoping", CAT, "Dashed outline traced around a head and shoulders with square anchor points on it",
      tags=["rotoscope", "roto", "trace footage", "mask animation", "visual effects", "frame by frame", "cutout"])
def _(S):
    parts = [ko(circle(12, 9, 2.25)), ko("M8.5 18a3.5 3.5 0 0 1 7 0Z")]
    for k in range(5):
        parts.append(line(arc(12, 9, 5.5, -90 + 72 * k + 10, -90 + 72 * k + 50)))
    parts.append(line("M4 20V16.5A5 4.5 0 0 1 7.5 14M20 20V16.5A5 4.5 0 0 0 16.5 14"))
    parts += [ko(rect(10.75, 2.25, 2.5, 2.5)), ko(rect(15, 6.75, 2.5, 2.5)), ko(rect(6.5, 6.75, 2.5, 2.5)),
              ko(rect(2.75, 19, 2.5, 2.5)), ko(rect(18.75, 19, 2.5, 2.5))]
    return parts


@icon("dubbing", CAT, "Studio microphone on a stand facing a screen that shows a speaking face",
      tags=["voice over", "voice recording", "adr", "lip sync", "translation audio", "post production", "narration"])
def _(S):
    return [shell(rect(3, 3.5, 5, 9, 2.5)), line("M1.5 9.5A6.5 6.5 0 0 0 9.5 15.5"), line("M5.5 16V21"),
            shell(rect(12, 5, 10, 11, S.R)), ko(circle(15.5, 9, 1)), ko(circle(18.5, 9, 1)), ko(ellipse(17, 12.75, 1.75, 1))]


@icon("talk-show-set", CAT, "Host desk on the left and a two seat sofa on the right in front of a city skyline backdrop",
      tags=["chat show", "late night", "tv studio", "interview set", "host desk", "couch", "television"])
def _(S):
    return [line("M2 9V5.5H7V9M9.5 9V3.5H14.5V9M17 9V6H22V9"), shell(rect(2, 13, 9, 7, min(S.R, 1.5))),
            shell(poly([(13, 20), (13, 15), (14.5, 15), (14.5, 12), (20.5, 12), (20.5, 15), (22, 15), (22, 20)], closed=True, r=S.r * 0.5))]


@icon("film-rewinder", CAT, "Film reel on a spindle with a hand crank and a curved arrow showing the winding direction",
      tags=["rewind", "film winding", "reel crank", "editing bench", "cinema", "projectionist", "film handling"])
def _(S):
    parts = [shell(circle(10, 11, 7)), dot(10, 11, 1.25), line("M2 21H18")]
    for k in range(3):
        x, y = polar(10, 11, 4, -90 + 120 * k)
        parts.append(ko(circle(x, y, 1.4)))
    parts += [line("M17.5 3.5A10 10 0 0 1 21.5 11"), line(poly([(21.5, 7), (21.5, 11.5), (17, 11.5)], r=S.r * 0.5))]
    return parts


@icon("film-trim-bin", CAT, "Canvas bin below a pin rack with strips of film hanging down into it",
      tags=["trim bin", "film editing", "cutting room", "off cuts", "film strips", "editor", "celluloid"])
def _(S):
    return [line("M2 3H22"), line("M7 3V13M12 3V11M17 3V13"),
            shell(poly([(3, 13), (21, 13), (19, 21), (5, 21)], closed=True, r=S.r * 0.5))]
