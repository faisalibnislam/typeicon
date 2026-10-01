"""TypeIcon Core: messaging (batch 003). Press, post, phones, broadcast and event signage."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, polar

CAT = "messaging"


# --------------------------------------------------------------------------- local helpers

def P2(x, y):
    return f"{fmt(x)} {fmt(y)}"


def kd(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def star_pts(cx, cy, R, r, n, start=-90.0):
    return [polar(cx, cy, R if i % 2 == 0 else r, start + i * 180 / n) for i in range(2 * n)]


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def crescent(cx, cy, r, off=1.3, r2=None):
    return minus(circle(cx, cy, r), circle(cx + off, cy - off * 0.6, r2 or r * 0.85))


def bub(S, x0=2.5, y0=2.5, x1=21.5, y1=18.0, tip=(7.0, 22.0), tx0=7.0, tx1=11.5):
    return poly([(x0, y0), (x1, y0), (x1, y1), (tx1, y1), tip, (tx0, y1), (x0, y1)], closed=True, r=S.r * 1.3)


# ============================================================================ chunk 1

@icon("press-release", CAT, "Document with a small megaphone in its upper corner.",
      tags=["press", "announcement", "media statement", "news release", "pr", "publicity"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 19, S.R)),
            kd(poly([(8, 7.5), (10.5, 7.5), (15, 5), (15, 12), (10.5, 9.5), (8, 9.5)], closed=True, r=S.r * 0.3)),
            detail(seg(8, 15.5, 16, 15.5)), detail(seg(8, 18.5, 13, 18.5))]


@icon("almanac", CAT, "Thick book with a sun and a crescent moon on its cover.",
      tags=["yearbook", "annual", "calendar book", "weather almanac", "sun moon", "reference"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 19, S.R)), detail(seg(8.5, 3, 8.5, 21)),
            kd(circle(14.2, 8, 2.2)), kd(crescent(14.2, 16, 2.8, 1.5, 2.4))]


@icon("bookplate", CAT, "Rectangular label with a decorative border, a small open book and a name line.",
      tags=["ex libris", "book label", "library label", "owner label", "bookmark", "name plate"])
def _(S):
    return [shell(rect(3, 4, 18, 16, min(S.R, 2))),
            detail("M12 8.5C10.5 7.2 8.8 7.2 7.3 7.7V12.3C8.8 11.8 10.5 11.8 12 13.1C13.5 11.8 15.2 11.8 16.7 12.3V7.7C15.2 7.2 13.5 7.2 12 8.5Z"),
            detail(seg(8, 16.5, 16, 16.5))]


@icon("clay-tablet", CAT, "Rounded rectangle tablet covered in rows of small wedge-shaped marks.",
      tags=["cuneiform", "ancient writing", "stone tablet", "sumerian", "archaeology", "early writing"])
def _(S):
    parts = [shell(rect(4, 3, 16, 18, 4 if S.name == "rounded" else 3))]
    for y in (7.5, 12, 16.5):
        for x in (8.5, 14.5):
            if y == 12:
                parts.append(kd(poly([(x - 1.6, y - 1.6), (x + 1.6, y - 1.6), (x, y + 1.6)], closed=True)))
            else:
                parts.append(kd(poly([(x - 1.6, y - 1.6), (x + 1.6, y), (x - 1.6, y + 1.6)], closed=True)))
    return parts


@icon("panel-discussion", CAT, "Three head figures behind a long table with a microphone in front of each.",
      tags=["panel", "speakers", "conference", "roundtable", "forum", "talk show", "discussion table"])
def _(S):
    parts = [shell(rect(2.5, 12.5, 19, 8, S.R))]
    for x in (6, 12, 18):
        parts.append(dot(x, 5.8, 2.0))
        parts.append(line(f"M{fmt(x - 2.4)} 12.5A2.4 2.4 0 0 1 {fmt(x + 2.4)} 12.5"))
        parts.append(kd(rect(x - 0.6, 14.3, 1.2, 3.2, 0.5)))
    return parts


@icon("broadcast-interview", CAT, "Two chairs facing each other with a microphone on a stand between them.",
      tags=["interview", "talk show", "guest seat", "podcast", "press interview", "tv studio"])
def _(S):
    return [shell(poly([(2.5, 5), (5, 5), (5, 11.5), (8, 11.5), (8, 15), (2.5, 15)], closed=True, r=S.r * 0.6)),
            line(seg(3.5, 15, 3.5, 20.5)), line(seg(7, 15, 7, 20.5)),
            shell(poly([(21.5, 5), (19, 5), (19, 11.5), (16, 11.5), (16, 15), (21.5, 15)], closed=True, r=S.r * 0.6)),
            line(seg(20.5, 15, 20.5, 20.5)), line(seg(17, 15, 17, 20.5)),
            kd(rect(10.75, 3.5, 2.5, 6, 1.25)), line(seg(12, 10, 12, 19.5)), line(seg(10.5, 20.5, 13.5, 20.5))]


@icon("debate", CAT, "Two podiums facing each other with a speech bubble above each one.",
      tags=["argument", "podium", "public speaking", "face off", "election debate", "rebuttal"])
def _(S):
    return [kd(poly([(3, 3), (10, 3), (10, 8), (6.5, 8), (4.5, 10), (4.5, 8), (3, 8)], closed=True, r=S.r * 0.5)),
            kd(poly([(14, 3), (21, 3), (21, 8), (19.5, 8), (19.5, 10), (17.5, 8), (14, 8)], closed=True, r=S.r * 0.5)),
            shell(poly([(4.5, 12.5), (9, 12.5), (10, 21), (3.5, 21)], closed=True, r=S.r * 0.6)),
            shell(poly([(15, 12.5), (19.5, 12.5), (20.5, 21), (14, 21)], closed=True, r=S.r * 0.6))]


@icon("petition", CAT, "Clipboard with several signature lines filled with scribbles.",
      tags=["sign", "signatures", "campaign", "collect signatures", "sign up", "cause", "activism"])
def _(S):
    parts = [shell(rect(4.5, 4, 15, 17.5, S.R)), kd(rect(9, 2, 6, 3.5, 1))]
    for y in (10, 14, 18):
        parts.append(detail(f"M8 {y}Q9.5 {y - 2.2} 11 {y}T14 {y}T16.5 {y}"))
    return parts


@icon("voice-command", CAT, "Head profile facing right with sound waves coming out of the mouth.",
      tags=["voice control", "speech recognition", "say", "dictation", "hands free", "spoken input", "assistant"])
def _(S):
    head = ("M6 21V16.6C3.6 15 2.8 12.2 3 9.6C3.3 5.6 6.4 3 9.6 3C12.8 3 15 5 15 7.8L16.4 11L14.8 11.8V14"
            "Q14.8 15.8 13 15.8H11V21Z")
    return [shell(head, stroke_miterlimit="2"), line(arc(15.8, 12.5, 4.4, -38, 38)), line(arc(15.8, 12.5, 7.2, -38, 38))]


@icon("name-tag", CAT, "Rectangular sticker with a solid top band and a blank line for a written name.",
      tags=["hello my name is", "badge", "nametag", "introduction", "conference badge", "sticker label"])
def _(S):
    return [shell(rect(3, 4.5, 18, 15, min(S.R, 3))), kd(rect(5.5, 7, 13, 3.5)), detail(seg(7, 15.5, 17, 15.5))]


@icon("tag-person", CAT, "Price tag shape with a small head-and-shoulders figure inside.",
      tags=["tag someone", "mention", "tag friend", "photo tag", "label person", "people tag"])
def _(S):
    return [shell(poly([(2.5, 5), (15, 5), (21.5, 12), (15, 19), (2.5, 19)], closed=True, r=S.r)),
            kd(circle(8.5, 9.6, 1.9)), kd("M5 16.3Q5 12.3 8.5 12.3Q12 12.3 12 16.3Z"), kd(circle(17, 12, 1.1))]


@icon("viral-spread", CAT, "Central dot linked to several nodes which each branch out to more nodes.",
      tags=["viral", "go viral", "spread", "network effect", "share chain", "contagion", "trending"])
def _(S):
    parts = [dot(12, 12, 2.2) if S.name == "rounded" else kd(rect(10, 10, 4, 4))]
    for a in (-90, 30, 150):
        n = polar(12, 12, 5.6, a)
        parts.append(line(seg(12, 12, *n)))
        parts.append(dot(n[0], n[1], 1.6) if S.name == "rounded" else kd(rect(n[0] - 1.4, n[1] - 1.4, 2.8, 2.8)))
        for da in (-28, 28):
            q = polar(12, 12, 10, a + da)
            parts.append(line(seg(*n, *q)))
            parts.append(dot(q[0], q[1], 1.2) if S.name == "rounded" else kd(rect(q[0] - 1.1, q[1] - 1.1, 2.2, 2.2)))
    return parts


@icon("fan-mail", CAT, "Pile of envelopes with a small star on the top one.",
      tags=["fan letter", "admirer", "celebrity mail", "letters", "star", "appreciation", "post"])
def _(S):
    return [line(poly([(6, 9), (6, 4.5), (21, 4.5), (21, 15.5), (18, 15.5)], r=S.r)),
            shell(rect(3, 9, 15, 11.5, min(S.R, 2))),
            kd(poly(star_pts(10.5, 14.9, 3.5, 1.5, 5), closed=True))]


# ============================================================================ chunk 2

@icon("online-dating", CAT, "Two phone screens facing each other with a heart between them.",
      tags=["dating app", "match", "romance", "swipe", "love", "couple", "relationship", "chat"])
def _(S):
    return [shell(rect(2.5, 5, 5.5, 14, min(S.R, 2.5))), shell(rect(16, 5, 5.5, 14, min(S.R, 2.5))),
            kd("M12 15.2C9.6 13.3 9.6 10.3 11 10.3C11.6 10.3 12 10.8 12 11.3C12 10.8 12.4 10.3 13 10.3C14.4 10.3 14.4 13.3 12 15.2Z")]


@icon("slash-command", CAT, "Speech bubble with a single forward slash inside it.",
      tags=["slash", "chat command", "bot command", "shortcut", "command menu", "forward slash"])
def _(S):
    return [shell(bub(S)), detail(seg(13.6, 5.8, 10.4, 14.7))]


@icon("voice-channel", CAT, "Speaker cone with a hash sign beside it.",
      tags=["voice room", "audio channel", "voice chat", "hash", "channel", "speaker", "live audio"])
def _(S):
    return [shell(poly([(2.5, 9), (5.5, 9), (9.5, 5.5), (9.5, 18.5), (5.5, 15), (2.5, 15)], closed=True, r=S.r * 0.5)),
            line(seg(15.5, 6.5, 15.5, 17.5)), line(seg(20, 6.5, 20, 17.5)),
            line(seg(13.5, 9.5, 22, 9.5)), line(seg(13.5, 14.5, 22, 14.5))]


@icon("quoted-reply", CAT, "Speech bubble with a small nested block at its top made of a vertical bar and a short line.",
      tags=["reply to message", "quote", "reply thread", "respond", "chat", "inline reply"])
def _(S):
    return [shell(bub(S)), detail(seg(7, 6, 7, 9.5)), detail(seg(10, 7.75, 17, 7.75)), detail(seg(7, 13.5, 14, 13.5))]


@icon("e-card", CAT, "Screen showing a folded greeting card with a heart on its front.",
      tags=["digital card", "ecard", "online greeting", "greeting card", "electronic card", "wishes", "heart"])
def _(S):
    return [shell(rect(2, 3, 20, 14, S.R)),
            detail(poly([(7, 13.5), (7, 6), (14, 6), (17, 9), (17, 13.5)], closed=True, r=S.r * 0.4)),
            kd("M12 12.6C10.3 11.4 10.3 9.2 11.4 9.2C11.8 9.2 12 9.5 12 9.8C12 9.5 12.2 9.2 12.6 9.2C13.7 9.2 13.7 11.4 12 12.6Z"),
            line(seg(12, 17, 12, 20.5)), line(seg(8, 20.5, 16, 20.5))]


@icon("mail-chute", CAT, "Tall narrow glass-fronted wall chute with a slot box at its base.",
      tags=["letter chute", "mail drop", "building mail", "postal chute", "apartment mail", "drop slot"])
def _(S):
    return [shell(rect(9, 2.5, 6, 12.5, min(S.R, 2))), kd(rect(10.5, 5, 3, 2)), kd(rect(10.5, 9, 3, 2)),
            shell(rect(6, 15, 12, 6.5, min(S.R, 2))), detail(seg(9, 18.2, 15, 18.2))]


@icon("mail-tray", CAT, "Rectangular postal tray with hand holes at each end, filled with upright letters.",
      tags=["letter tray", "sorting tray", "postal", "mail crate", "outbox", "sorting office", "letters"])
def _(S):
    return [line(seg(6, 10.5, 7.2, 3.5)), line(seg(10, 10.5, 10.6, 3)), line(seg(14, 10.5, 13.4, 3)), line(seg(18, 10.5, 16.8, 3.5)),
            shell(poly([(2.5, 10.5), (21.5, 10.5), (20, 20.5), (4, 20.5)], closed=True, r=S.r * 0.6)),
            kd(rect(5.5, 14, 3.5, 2, 1)), kd(rect(15, 14, 3.5, 2, 1))]


@icon("stamp-vending-machine", CAT, "Upright box machine with a small display, a coin slot and a stamp dispensing slot.",
      tags=["postage machine", "stamp dispenser", "post office kiosk", "buy stamps", "postage vending", "kiosk"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 19, S.R)), kd(rect(7.5, 5.5, 9, 3.5)), kd(rect(9.5, 11.2, 5, 1.4, 0.6)),
            detail(rect(7.5, 14.5, 9, 4))]


@icon("slider-phone", CAT, "Mobile phone with its screen half slid upward revealing a keypad beneath.",
      tags=["slide phone", "keypad phone", "retro mobile", "feature phone", "sliding keyboard", "qwerty slider"])
def _(S):
    return [line(poly([(6.5, 14.5), (6.5, 21.5), (17.5, 21.5), (17.5, 14.5)], r=S.r)),
            shell(rect(6.5, 2.5, 11, 12.5, S.R)), kd(rect(9, 5.5, 6, 6)),
            dot(9.5, 18.2, 1), dot(12, 18.2, 1), dot(14.5, 18.2, 1)]


@icon("car-telephone", CAT, "Corded handset resting in a console cradle with a coiled cord.",
      tags=["car phone", "mobile phone 1980s", "vehicle phone", "corded handset", "retro phone", "cradle"])
def _(S):
    return [shell(poly([(3, 2.5), (10.5, 2.5), (10.5, 7), (9, 7), (9, 10), (10.5, 10), (10.5, 14), (3, 14),
                        (3, 10), (4.5, 10), (4.5, 7), (3, 7)], closed=True, r=S.r * 0.5)),
            shell(rect(3, 15.5, 18, 6, min(S.R, 2))), kd(circle(8, 18.5, 1)), kd(circle(12, 18.5, 1)), kd(circle(16, 18.5, 1)),
            line(poly([(10.5, 8.5), (18.5, 8.5), (18.5, 15.5)], r=S.r))]


@icon("sim-eject-tool", CAT, "Small flat metal pin with a round loop at one end.",
      tags=["sim pin", "sim tray tool", "eject pin", "phone pin", "paperclip", "card tray opener"])
def _(S):
    tip = (20.5, 20.5)
    a, b = (8.3, 10.7), (10.7, 8.3)
    return [shell(circle(7, 7, 3.6)), shell(poly([a, b, tip], closed=True, r=S.r * 0.3), stroke_miterlimit="6")]


@icon("dual-sim", CAT, "Two SIM cards with clipped corners overlapping each other.",
      tags=["two sims", "double sim", "sim cards", "two numbers", "sim slots", "mobile line"])
def _(S):
    return [line(poly([(8, 8), (8, 2.5), (16.5, 2.5), (19.5, 5.5), (19.5, 16), (14, 16)], r=S.r * 0.5)),
            shell(poly([(3, 8), (10, 8), (13, 11), (13, 21.5), (3, 21.5)], closed=True, r=S.r * 0.5)),
            kd(rect(5.5, 13.5, 5, 5, 1))]


@icon("5g-network", CAT, "Signal bars beside the characters 5G.",
      tags=["5g", "fifth generation", "mobile network", "cellular", "wireless speed", "signal strength"])
def _(S):
    return [line(poly([(7.6, 6.5), (3.4, 6.5), (3.4, 11.5)])), line("M3.4 11.5H5.3A3 3 0 0 1 5.3 17.5H3"),
            line("M13.6 8.8A3.4 4.8 0 1 0 13.6 15.2V12H11"),
            kd(rect(16.4, 13.5, 1.8, 5)), kd(rect(19, 9.5, 1.8, 9)), kd(rect(21.6, 5.5, 1.8, 13))]


@icon("satellite-texting", CAT, "Smartphone with a dotted arc reaching up to a small satellite.",
      tags=["emergency sms", "satellite messaging", "off grid", "sos text", "no signal", "satellite phone"])
def _(S):
    return [shell(rect(2.5, 12.5, 6.5, 9, min(S.R, 2))),
            shell(poly([(16.5, 5), (20, 8.5), (16.5, 12), (13, 8.5)], closed=True)),
            line(seg(14.2, 10.8, 11.6, 13.4)), line(seg(18.8, 6.2, 21.4, 3.6)),
            dot(5.3, 8.6, 1), dot(7.4, 5.4, 1), dot(10.4, 3.8, 1)]


@icon("push-to-talk", CAT, "Round button marked with a microphone and sound arcs, pressed by a finger.",
      tags=["ptt", "walkie talkie", "hold to talk", "talk button", "radio", "voice button", "press and speak"])
def _(S):
    return [shell(circle(12, 12, 9.5)), kd(rect(10.25, 6, 3.5, 6.5, 1.75)),
            detail("M8 11A4 4 0 0 0 16 11"), detail(seg(12, 15, 12, 17))]


# ============================================================================ chunk 3

@icon("telephone-plug", CAT, "Small square modular plug with a latch clip and a flat cable.",
      tags=["rj11", "phone jack plug", "landline cable", "modular connector", "ethernet plug", "phone cord"])
def _(S):
    return [shell(poly([(5.5, 3.5), (18.5, 3.5), (18.5, 13), (15.5, 13), (15.5, 21.5), (8.5, 21.5), (8.5, 13), (5.5, 13)],
                       closed=True, r=S.r * 0.6)),
            kd(rect(8.5, 6, 1.4, 4.5)), kd(rect(11.3, 6, 1.4, 4.5)), kd(rect(14.1, 6, 1.4, 4.5))]


@icon("room-booking-panel", CAT, "Small tablet mounted on a wall beside a door edge showing a status bar.",
      tags=["meeting room display", "room scheduler", "conference room sign", "availability panel", "reservation screen", "door tablet"])
def _(S):
    return [line(seg(3.5, 2.5, 3.5, 21.5)),
            shell(rect(8, 4.5, 13, 15, S.R)), kd(rect(10.5, 7, 8, 3)), detail(seg(10.5, 14, 18.5, 14))]


@icon("interactive-whiteboard", CAT, "Large wall screen on a rolling stand with a stylus stroke on it.",
      tags=["smart board", "digital whiteboard", "classroom display", "touch screen board", "presentation board", "teaching screen"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 12.5, S.R)), detail(poly([(6, 10.5), (9.5, 6.5), (12.5, 10.5), (17, 6.5)], r=S.r)),
            line(seg(12, 15, 12, 20)), line(seg(6.5, 20.5, 17.5, 20.5)), dot(6.5, 20.5, 1.2), dot(17.5, 20.5, 1.2)]


@icon("background-blur", CAT, "Head-and-shoulders figure in front of a background of soft scattered dots.",
      tags=["blur background", "video call effect", "privacy backdrop", "bokeh", "webcam", "virtual background"])
def _(S):
    return [shell(circle(12, 9, 3.3)),
            shell("M6 21.5V19.5Q6 14.5 12 14.5Q18 14.5 18 19.5V21.5Z"),
            *[dot(x, y, 1.15) if S.name == "rounded" else kd(rect(x - 1, y - 1, 2, 2))
              for x, y in ((4, 4.5), (20, 4.5), (3.6, 10.5), (20.4, 10.5), (3, 17), (21, 17))]]


@icon("viewer-count", CAT, "Eye symbol beside a small number on a rounded tag.",
      tags=["views", "live viewers", "audience size", "watching now", "view counter", "stream views", "eye"])
def _(S):
    lens = "M4 12Q7.8 7 11.6 12Q7.8 17 4 12Z"
    return [shell(rect(2, 5, 20, 14, 7 if S.name == "rounded" else 4)),
            kd(minus(lens, circle(7.8, 12, 1.4))),
            detail("M14.6 10A2.3 2.3 0 0 1 19.4 10C19.4 12.3 14.6 13.8 14.6 15.5H19.4")]


@icon("film-countdown", CAT, "Circle with crosshair ticks and a large number 3 in its centre, the film leader countdown.",
      tags=["film leader", "countdown", "movie start", "3 2 1", "cinema", "reel leader", "count in"])
def _(S):
    return [shell(circle(12, 12, 8)), line(seg(12, 1.5, 12, 4)), line(seg(12, 20, 12, 22.5)),
            line(seg(1.5, 12, 4, 12)), line(seg(20, 12, 22.5, 12)),
            detail("M9.8 9A2.3 2.2 0 0 1 14.2 9C14.2 10.6 12.8 11.5 11.8 11.5C13 11.5 14.4 12.4 14.4 14.2A2.4 2.2 0 0 1 9.6 14.6")]


@icon("red-carpet", CAT, "Long carpet runner in perspective with a rope stanchion on each side.",
      tags=["premiere", "vip entrance", "gala", "celebrity arrival", "awards night", "roped walkway", "runner"])
def _(S):
    return [shell(poly([(10, 4), (14, 4), (19, 21), (5, 21)], closed=True, r=S.r * 0.5)),
            dot(3.6, 8, 1.6), line(seg(3.6, 9.5, 3.6, 15.5)), line(seg(2, 16.5, 5.2, 16.5)),
            dot(20.4, 8, 1.6), line(seg(20.4, 9.5, 20.4, 15.5)), line(seg(18.8, 16.5, 22, 16.5))]


@icon("velvet-rope", CAT, "Two posts with round tops joined by a drooping rope.",
      tags=["rope barrier", "stanchion", "queue line", "exclusive entry", "vip", "crowd control", "club door"])
def _(S):
    return [dot(5, 6, 2), line(seg(5, 8, 5, 20)), line(seg(2.5, 20.5, 7.5, 20.5)),
            dot(19, 6, 2), line(seg(19, 8, 19, 20)), line(seg(16.5, 20.5, 21.5, 20.5)),
            line("M5 9Q12 19 19 9")]


@icon("home-movie-camera", CAT, "Small handheld film camera with a pistol grip and a short lens.",
      tags=["cine camera", "film camera", "vintage camcorder", "8mm film", "family video", "handheld camera"])
def _(S):
    return [shell(rect(3, 6.5, 12, 8.5, min(S.R, 2))), shell(poly([(15, 8.5), (21, 6), (21, 15.5), (15, 13)], closed=True, r=S.r * 0.4)),
            shell(rect(6, 15, 5, 6.5, min(S.R, 1.5))), kd(circle(6.5, 9.7, 1))]


@icon("portable-tv", CAT, "Small handheld television with a tiny screen and a telescopic antenna.",
      tags=["pocket tv", "mini television", "battery tv", "rabbit ears", "camping tv", "retro tv", "antenna"])
def _(S):
    return [line(seg(12, 9, 7, 3)), line(seg(12, 9, 17, 3)), dot(7, 3, 1.2), dot(17, 3, 1.2),
            shell(rect(3, 9, 18, 12, S.R)), detail(rect(5.5, 11.5, 9, 7, 1)), kd(circle(18, 13, 1)), kd(circle(18, 17, 1))]


@icon("signal-splitter", CAT, "Small box with one cable coming in on one side and two cables leaving the other.",
      tags=["cable splitter", "coax splitter", "tv splitter", "antenna splitter", "signal divider", "coaxial", "y cable"])
def _(S):
    return [shell(rect(8, 7.5, 8, 9, min(S.R, 2))),
            line(seg(2.5, 12, 8, 12)), line(seg(16, 10, 21.5, 10)), line(seg(16, 14, 21.5, 14)),
            *[dot(x, y, 1.4) if S.name == "rounded" else kd(rect(x - 1.3, y - 1.3, 2.6, 2.6)) for x, y in ((3, 12), (21, 10), (21, 14))]]


@icon("hand-crank-siren", CAT, "Round siren housing with a side crank handle and a grip underneath.",
      tags=["air raid siren", "emergency alarm", "manual siren", "crank alarm", "warning horn", "civil defense"])
def _(S):
    return [shell(circle(10, 8.5, 6)), detail(circle(10, 8.5, 2)),
            line(seg(16, 8.5, 21, 8.5)), line(seg(21, 8.5, 21, 13.5)),
            line(poly([(7, 14.5), (7, 21.5), (13, 21.5), (13, 14.5)], r=S.r))]


@icon("bell-pull", CAT, "Rope hanging from a ceiling bracket ending in a tassel.",
      tags=["servant bell", "rope bell", "pull cord", "butler call", "summon", "doorbell rope", "tassel"])
def _(S):
    return [line(seg(6, 3.5, 18, 3.5)), line("M12 3.5C10.3 6 13.7 8.5 12 11"), dot(12, 13, 2.2),
            line(seg(12, 15.5, 9, 21.5)), line(seg(12, 15.5, 12, 21.5)), line(seg(12, 15.5, 15, 21.5))]


@icon("now-serving-display", CAT, "Wall screen showing a large ticket number with a small arrow beside it.",
      tags=["queue display", "ticket number", "next in line", "waiting room screen", "counter number", "take a number"])
def _(S):
    return [shell(rect(2, 5, 20, 14, S.R)), detail(poly([(5.5, 9, ), (11, 9), (8, 15.5)], r=S.r * 0.3)),
            kd(poly([(14.5, 9.5), (19, 12), (14.5, 14.5)], closed=True))]


@icon("research-paper", CAT, "Document with a title bar, a boxed abstract and two columns of text lines.",
      tags=["journal article", "academic paper", "study", "manuscript", "abstract", "publication", "scholarly"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 19, S.R)), detail(seg(8, 6, 16, 6)), kd(rect(7.5, 9, 9, 3.4)),
            detail(seg(9.5, 15, 9.5, 18.5)), detail(seg(14.5, 15, 14.5, 18.5))]


# ============================================================================ chunk 4

def tube(d, w, S):
    return path_to_d(ST(d, w, S.cap, S.join))


@icon("yard-sign", CAT, "Small rectangular sign on a two-pronged wire stake stuck into grass.",
      tags=["lawn sign", "campaign sign", "for sale sign", "election sign", "garden sign", "real estate sign", "stake"])
def _(S):
    return [shell(rect(3.5, 2.5, 17, 10, S.R)), detail(seg(7, 6.3, 17, 6.3)), detail(seg(7, 9.2, 13, 9.2)),
            line(seg(9, 12.5, 9, 21)), line(seg(15, 12.5, 15, 21)),
            line(poly([(2.5, 21), (4, 18.3), (5.5, 21)], r=S.r * 0.5)), line(poly([(18.5, 21), (20, 18.3), (21.5, 21)], r=S.r * 0.5)),
            line(seg(2.5, 21, 21.5, 21))]


@icon("unsend-message", CAT, "Speech bubble with a curved arrow inside it looping back to the left.",
      tags=["undo send", "retract message", "delete for everyone", "recall", "take back", "chat", "unsent"])
def _(S):
    return [shell(bub(S)), detail("M16.5 14V12.5A3.5 3.5 0 0 0 13 9H8.5"), detail(poly([(11, 6.5), (8.5, 9), (11, 11.5)], r=S.r * 0.5))]


@icon("cold-email", CAT, "Envelope with a small snowflake on its front.",
      tags=["cold outreach", "unsolicited email", "sales email", "prospecting", "outbound email", "frozen", "snowflake"])
def _(S):
    c = (18, 16.5)
    parts = [shell(minus(rect(2.5, 4.5, 17, 13, min(S.R, 3)), circle(*c, 6.4))),
             detail(poly([(3.5, 5.5), (10.5, 11), (14.5, 7.7)]))]
    for a in (90, 150, 210):
        p1, p2 = polar(*c, 3.6, a), polar(*c, 3.6, a + 180)
        parts.append(line(seg(*p1, *p2)))
    return parts


@icon("courier-envelope", CAT, "Large stiff cardboard envelope with a pull-tab strip across its top.",
      tags=["express mail", "mailer", "overnight envelope", "tear strip", "cardboard mailer", "parcel envelope", "shipping"])
def _(S):
    return [shell(rect(4, 3, 16, 18, S.R)), detail(seg(4.5, 7.5, 10, 7.5)), detail(seg(12.5, 7.5, 15, 7.5)),
            kd(rect(16.5, 5.3, 2.2, 4.4, 1)), detail(rect(7.5, 12, 9, 5.5, 1))]


@icon("phone-off-hook", CAT, "Desk telephone base with its handset lying on its side next to it.",
      tags=["busy line", "handset off", "landline", "receiver down", "unavailable", "retro telephone", "engaged"])
def _(S):
    return [shell(rect(2.5, 9, 10, 12, S.R)), detail(circle(7.5, 14.5, 2)), kd(circle(7.5, 14.5, 0.7)),
            shell(poly([(15, 3.5), (21.5, 3.5), (21.5, 8.5), (20, 8.5), (20, 15.5), (21.5, 15.5), (21.5, 20.5), (15, 20.5),
                        (15, 15.5), (16.5, 15.5), (16.5, 8.5), (15, 8.5)], closed=True, r=S.r * 0.5))]


@icon("cinema-seats", CAT, "Row of three folding theatre seats with armrests, seen from the front.",
      tags=["movie theater", "theatre seating", "auditorium", "cinema chairs", "screening", "row of seats", "tip-up seat"])
def _(S):
    r = 1.5 if S.name == "line" else 2.4
    parts = []
    for x in (2, 9.5, 17):
        parts.append(solid(rect(x, 3, 5, 9, r)))
        parts.append(solid(rect(x, 13.5, 5, 4, min(r, 1.5))))
        parts.append(line(seg(x + 2.5, 17.5, x + 2.5, 21)))
    for x in (7, 14.5):
        parts.append(solid(rect(x, 10, 2.5, 2.2, 0.5)))
    return parts


@icon("end-credits", CAT, "Screen with centred text lines of different lengths and a small upward arrow at the side.",
      tags=["closing credits", "roll credits", "film credits", "scrolling text", "the end", "movie ending", "cast list"])
def _(S):
    return [shell(rect(2.5, 3, 14.5, 18, S.R)), detail(seg(7.5, 7.5, 12, 7.5)), detail(seg(6, 12, 13.5, 12)), detail(seg(7.5, 16.5, 12, 16.5)),
            line(seg(20.5, 19, 20.5, 8)), line(poly([(18.6, 10.5), (20.5, 7.6), (22.4, 10.5)], r=S.r * 0.5))]


@icon("aviation-headset", CAT, "Headset with thick padded ear cups, a padded headband and a boom microphone.",
      tags=["pilot headset", "aircraft headset", "noise cancelling", "flight radio", "boom mic", "cockpit", "atc"])
def _(S):
    return [line("M4.5 12.5A7.5 8.5 0 0 1 19.5 12.5"), kd(rect(9.3, 2.6, 5.4, 2.4, 1)),
            shell(rect(2.5, 11.5, 5, 7.5, 2 if S.name == "line" else 2.6)), shell(rect(16.5, 11.5, 5, 7.5, 2 if S.name == "line" else 2.6)),
            line("M5 19Q5 21.6 9.5 21.6H11.5"), dot(12.8, 21.6, 1.5)]


@icon("newspaper-bundle", CAT, "Stack of folded newspapers tied together with a crossed string.",
      tags=["papers", "paper delivery", "stacked newspapers", "tied bundle", "press run", "circulation", "news bale"])
def _(S):
    return [shell(rect(3, 8.5, 18, 11.5, min(S.R, 2))), line(poly([(5, 8.5), (5, 5), (19, 5), (19, 8.5)], r=S.r)),
            line(seg(12, 5, 12, 20)), line(seg(3, 14.3, 21, 14.3))]


@icon("social-listening", CAT, "Ear with a small hash sign and sound arcs beside it.",
      tags=["brand monitoring", "social media monitoring", "mentions", "hashtag tracking", "sentiment", "listening tool", "ear"])
def _(S):
    return [line("M10.5 9.5A5 5.2 0 1 1 18.5 13C18.5 15.5 15.6 16.5 15.4 18.6C15.2 20.3 14 21 12.6 21C11.4 21 10.4 20.5 9.8 19.5"),
            line("M12.6 11C12.6 9.8 13.3 9 14.2 9C15.2 9 15.8 9.9 15.8 11"),
            solid(rect(3, 3.3, 1.4, 6.6)), solid(rect(6.2, 3.3, 1.4, 6.6)), solid(rect(2.2, 4.9, 6.2, 1.4)), solid(rect(2.2, 7.4, 6.2, 1.4))]


@icon("guest-list", CAT, "Clipboard with a column of name lines and small tick boxes.",
      tags=["attendees", "rsvp", "invite list", "door list", "checklist names", "event check in", "roster"])
def _(S):
    parts = [shell(rect(4.5, 4, 15, 17.5, S.R)), kd(rect(9, 2, 6, 3.5, 1))]
    for y in (10, 14, 18):
        parts.append(kd(rect(7.4, y - 1.2, 2.4, 2.4, 0.4)))
        parts.append(detail(seg(12, y, 16.5, y)))
    return parts


@icon("alphabet-board", CAT, "Board with a grid of letters and two larger boxes marked yes and no across the top.",
      tags=["spirit board", "talking board", "planchette", "letter board", "yes no board", "seance", "spelling board"])
def _(S):
    parts = [shell(rect(2.5, 3.5, 19, 17, S.R)), kd(rect(5, 6, 5.5, 2.6, 0.8)), kd(rect(13.5, 6, 5.5, 2.6, 0.8))]
    for y in (12.5, 16.5):
        for x in (6, 9.4, 12.8, 16.2):
            parts.append(dot(x + 0.2, y, 0.95))
    return parts


@icon("face-filter", CAT, "Face outline with pointed animal ears and a small animal nose drawn over it.",
      tags=["selfie filter", "camera effect", "cat ears", "ar filter", "video lens", "photo effect", "animal face"])
def _(S):
    face = path_to_d(U(P(circle(12, 13.5, 7.5)),
                       P(poly([(5.3, 10), (5.3, 2.5), (11, 6.8)], closed=True)),
                       P(poly([(18.7, 10), (18.7, 2.5), (13, 6.8)], closed=True))))
    return [shell(face), dot(9, 12.5, 1.1), dot(15, 12.5, 1.1), kd(poly([(10.4, 15.2), (13.6, 15.2), (12, 17)], closed=True))]


@icon("save-the-date-card", CAT, "Card with a small calendar page and a heart in its centre.",
      tags=["wedding invitation", "date announcement", "save the date", "event card", "wedding card", "calendar heart", "invite"])
def _(S):
    return [shell(rect(2.5, 4, 19, 16, S.R)), detail(rect(7, 7, 10, 10, 1)), detail(seg(7, 10.3, 17, 10.3)),
            kd("M12 15.8C10.2 14.6 10.2 12.5 11.3 12.5C11.7 12.5 12 12.8 12 13.1C12 12.8 12.3 12.5 12.7 12.5C13.8 12.5 13.8 14.6 12 15.8Z")]


@icon("place-card", CAT, "Small folded tent card standing on a table with a name line on its front.",
      tags=["name card", "table card", "seating card", "wedding seating", "tent card", "dinner party", "escort card"])
def _(S):
    return [shell(poly([(5, 18), (7, 6.5), (17, 6.5), (19, 18)], closed=True, r=S.r)), detail(seg(8.5, 12.5, 15.5, 12.5)),
            line(seg(2.5, 21, 21.5, 21))]
