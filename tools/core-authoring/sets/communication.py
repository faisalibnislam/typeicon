"""TypeIcon Core: communication."""
import math
import re

from dsl import arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, polar

CAT = "communication"


# --------------------------------------------------------------------------- local helpers

def tx(d, s=1.0, ox=0.0, oy=0.0, ax=0.0, ay=0.0):
    """Scale a d-string (absolute M/L/H/V/A/C/Q/Z only) by s about (ax, ay), then translate by (ox, oy)."""
    toks = re.findall(r"[MLHVACQZ]|-?\d*\.?\d+", d)
    out, i, cmd = [], 0, None

    def X(v):
        return fmt(ax + (float(v) - ax) * s + ox)

    def Y(v):
        return fmt(ay + (float(v) - ay) * s + oy)

    while i < len(toks):
        t = toks[i]
        if t in "MLHVACQZ":
            cmd = t
            out.append(t)
            i += 1
            continue
        if cmd in "ML":
            out.append(f"{X(toks[i])} {Y(toks[i + 1])}")
            i += 2
        elif cmd == "H":
            out.append(X(t))
            i += 1
        elif cmd == "V":
            out.append(Y(t))
            i += 1
        elif cmd == "A":
            rx, ry, rot, la, sw, x, y = toks[i:i + 7]
            out.append(f"{fmt(float(rx) * s)} {fmt(float(ry) * s)} {rot} {la} {sw} {X(x)} {Y(y)}")
            i += 7
        elif cmd == "C":
            out.append(" ".join(f"{X(toks[i + k])} {Y(toks[i + k + 1])}" for k in (0, 2, 4)))
            i += 6
        elif cmd == "Q":
            out.append(" ".join(f"{X(toks[i + k])} {Y(toks[i + k + 1])}" for k in (0, 2)))
            i += 4
        else:
            raise ValueError(f"tx: unsupported {cmd}")
    s_out = ""
    for t in out:
        s_out += t if (t in "MLHVACQZ" or not s_out or s_out[-1] in "MLHVACQZ") else " " + t
    return s_out


def flatten(d, step=0.2):
    """Sample a d-string into subpaths of points: [(points, closed), ...]."""
    from fontTools.pens.recordingPen import RecordingPen
    from fontTools.svgLib.path import parse_path
    rec = RecordingPen()
    parse_path(d, rec)
    subs, cur, closed = [], [], False

    def add_line(a, b):
        n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / step))
        for k in range(1, n + 1):
            cur.append((a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n))

    for op, args in rec.value:
        if op == "moveTo":
            if cur:
                subs.append((cur, closed))
            cur, closed = [args[0]], False
        elif op == "lineTo":
            add_line(cur[-1], args[0])
        elif op == "curveTo":
            p0 = cur[-1]
            for i in range(0, len(args), 3):
                c1, c2, p3 = args[i:i + 3]
                for k in range(1, 41):
                    t = k / 40
                    mt = 1 - t
                    cur.append((mt ** 3 * p0[0] + 3 * mt * mt * t * c1[0] + 3 * mt * t * t * c2[0] + t ** 3 * p3[0],
                                mt ** 3 * p0[1] + 3 * mt * mt * t * c1[1] + 3 * mt * t * t * c2[1] + t ** 3 * p3[1]))
                p0 = p3
        elif op == "qCurveTo":
            p0 = cur[-1]
            c1, p2 = args[0], args[-1]
            for k in range(1, 31):
                t = k / 30
                mt = 1 - t
                cur.append((mt * mt * p0[0] + 2 * mt * t * c1[0] + t * t * p2[0], mt * mt * p0[1] + 2 * mt * t * c1[1] + t * t * p2[1]))
        elif op in ("closePath", "endPath"):
            if op == "closePath" and cur:
                add_line(cur[-1], cur[0])
                closed = True
            subs.append((cur, closed))
            cur, closed = [], False
    if cur:
        subs.append((cur, closed))
    return subs


def outside(d, hidden):
    """Open path(s) tracing the parts of outline d where hidden(x, y) is False (for partly covered back shapes)."""
    out = []
    for pts, closed in flatten(d):
        keep = [not hidden(x, y) for x, y in pts]
        if all(keep):
            out.append("M" + "L".join(P2(*p) for p in pts) + ("Z" if closed else ""))
            continue
        n = len(pts)
        start = keep.index(False) if closed else 0
        order = [(start + k) % n for k in range(n)] if closed else list(range(n))
        run = []
        for i in order + ([] if not closed else []):
            if keep[i]:
                run.append(pts[i])
            elif run:
                if len(run) > 1:
                    out.append("M" + "L".join(P2(*p) for p in run))
                run = []
        if len(run) > 1:
            out.append("M" + "L".join(P2(*p) for p in run))
    return "".join(out)


def P2(x, y):
    return f"{fmt(x)} {fmt(y)}"


# Telephone handset (the v0.1 "phone" drawing), top-left earpiece to bottom-right mouthpiece.
_HANDSET_R = ("M5.2 3.5H8.6L10.4 8L8.1 9.5A11 11 0 0 0 14.5 15.9L16 13.6L20.5 15.4V18.8"
              "A1.7 1.7 0 0 1 18.8 20.5A15.5 15.5 0 0 1 3.5 5.2A1.7 1.7 0 0 1 5.2 3.5Z")
_HANDSET_L = "M3.5 3.5H8.6L10.4 8L8.1 9.5A11 11 0 0 0 14.5 15.9L16 13.6L20.5 15.4V20.5H19A15.5 15.5 0 0 1 3.5 5Z"


def handset(S, s=0.82, ox=0.0, oy=0.0):
    """Handset scaled about the bottom-left corner so the top-right stays free for signals."""
    d = _HANDSET_L if S.name == "line" else _HANDSET_R
    return tx(d, s, ox, oy, ax=3.0, ay=21.0)


def round_bubble(S, cx, cy, r, a1, a2, tip):
    """Circle bubble with a pointed tail between angles a2 (start of gap) and a1; tip = tail point.
    Arc runs clockwise from a1 round to a2."""
    p1, p2 = polar(cx, cy, r, a1), polar(cx, cy, r, a2)
    sweep = (a2 - a1) % 360
    arc_cmd = f"A{fmt(r)} {fmt(r)} 0 {1 if sweep > 180 else 0} 1 {P2(*p2)}"
    if S.name == "line":
        return f"M{P2(*p1)}{arc_cmd}L{P2(*tip)}Z"
    # Rounded: soften the tail tip.
    k = 0.28
    a = (tip[0] + (p2[0] - tip[0]) * k, tip[1] + (p2[1] - tip[1]) * k)
    b = (tip[0] + (p1[0] - tip[0]) * k, tip[1] + (p1[1] - tip[1]) * k)
    return f"M{P2(*p1)}{arc_cmd}L{P2(*a)}Q{P2(*tip)} {P2(*b)}Z"


def msg_circle(S):
    return round_bubble(S, 12.5, 11.5, 8.5, 160, 118, (4, 20))


# Rectangular chat bubble with a tail hanging from the bottom edge.
_CHAT = [(3, 4), (21, 4), (21, 17), (11.5, 17), (7, 21), (7, 17), (3, 17)]


def chat_bubble(S, pts=None):
    return poly(pts or _CHAT, closed=True, r=S.r * 1.3)


def envelope(S, x, y, w, h):
    """Closed envelope: body + V flap."""
    return [shell(rect(x, y, w, h, S.R * 0.5)),
            detail(poly([(x + 0.5, y + 1.5), (x + w / 2, y + h * 0.55), (x + w - 0.5, y + 1.5)], r=S.r))]


# ============================================================================ messages & chat

@icon("message-circle", CAT, "Round speech bubble with a pointed tail; a message.",
      tags=["message", "chat", "comment", "bubble", "talk", "reply"])
def _(S):
    return [shell(msg_circle(S))]


@icon("message-square", CAT, "Square speech bubble whose corner forms the tail; a message.",
      tags=["message", "chat", "comment", "bubble", "sms", "text"])
def _(S):
    return [shell(poly([(3, 3.5), (21, 3.5), (21, 17), (8.5, 17), (3, 21)], closed=True, r=S.r * 1.3),
                  stroke_miterlimit="2")]


@icon("messages", CAT, "Two overlapping rectangular speech bubbles; a message thread.",
      tags=["messages", "thread", "chat", "conversation", "inbox", "dm"], aliases=["message-thread"])
def _(S):
    front = [(2.5, 9), (15.5, 9), (15.5, 17.5), (9, 17.5), (5.5, 21), (5.5, 17.5), (2.5, 17.5)]
    back = [(8, 6.5), (8, 3), (21.5, 3), (21.5, 14), (17.5, 14)]
    return [shell(poly(front, closed=True, r=S.r * 1.1)), line(poly(back, r=S.r * 1.1))]


@icon("chat-dots", CAT, "Rectangular speech bubble with three dots; chat or more to say.",
      tags=["chat", "message", "typing", "ellipsis", "comment", "sms"])
def _(S):
    return [shell(chat_bubble(S)), dot(7.5, 10.5, 1.3), dot(12, 10.5, 1.3), dot(16.5, 10.5, 1.3)]


@icon("chat-bubbles", CAT, "Two round speech bubbles facing each other; a chat.",
      tags=["chat", "conversation", "talk", "discussion", "messages", "bubbles"])
def _(S):
    # Back bubble (upper left) shows only where the front bubble (lower right) does not cover it.
    back = round_bubble(S, 9, 9, 6.5, 165, 118, (3, 17.5))
    fc, fr = (16.25, 16), 5.25
    front = round_bubble(S, *fc, fr, 70, 20, (21.5, 21.5))
    return [line(outside(back, lambda x, y: math.hypot(x - fc[0], y - fc[1]) < fr + 3.25)), shell(front)]


@icon("comment-dots", CAT, "Round speech bubble with three dots; a comment in progress.",
      tags=["comment", "chat", "typing", "ellipsis", "reply", "message"])
def _(S):
    return [shell(msg_circle(S)), dot(8.5, 11.5, 1.3), dot(12.5, 11.5, 1.3), dot(16.5, 11.5, 1.3)]


@icon("send", CAT, "Notched arrowhead pointing right; send a message.",
      tags=["send", "submit", "message", "deliver", "post", "arrow"])
def _(S):
    return [shell(poly([(3, 3.5), (20.5, 12), (3, 20.5), (6.5, 12)], closed=True, r=S.r * 0.6), stroke_miterlimit="2")]


@icon("paper-plane", CAT, "Folded paper plane flying up and to the right; send or share.",
      tags=["send", "paper plane", "message", "deliver", "share", "fly"])
def _(S):
    body = [(21, 3), (14.5, 21), (10.5, 13.5), (3, 10)]
    return [shell(poly(body, closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
            detail(seg(10.5, 13.5, 21, 3))]


# ============================================================================ mail

@icon("mail-open", CAT, "Opened envelope with the flap raised; a read email.",
      tags=["email", "read", "opened", "envelope", "inbox", "message"], aliases=["envelope-open"])
def _(S):
    return [shell(poly([(3, 10), (12, 3.5), (21, 10), (21, 20.5), (3, 20.5)], closed=True, r=S.r)),
            detail(poly([(3.5, 10.5), (12, 16), (20.5, 10.5)], r=S.r))]


@icon("mailbox", CAT, "Curbside mailbox on a post with its flag raised.",
      tags=["mailbox", "postbox", "letterbox", "post", "delivery", "mail"], aliases=["postbox"])
def _(S):
    body = "M2.5 16.5V12.5A3.75 3.75 0 0 1 6.25 8.75H13.75A3.75 3.75 0 0 1 17.5 12.5V16.5Z"
    return [shell(body),
            detail("M10 16.5V12.5A3.75 3.75 0 0 0 6.25 8.75"),
            line(seg(13.5, 16.5, 13.5, 21.5)),
            line(seg(20.5, 15.5, 20.5, 2.5)),
            solid(rect(15, 2.5, 5.5, 4, min(S.R * 0.25, 0.75)) if S.name == "line" else rect(15, 2.5, 5.5, 4, 1)),
            ]


@icon("mail-stack", CAT, "Two stacked envelopes; several emails.",
      tags=["emails", "mail", "envelopes", "bulk", "inbox", "messages"], aliases=["mails"])
def _(S):
    return [*envelope(S, 2.5, 8.5, 15.5, 12),
            line(poly([(6.5, 6), (6.5, 3.5), (21.5, 3.5), (21.5, 15.5), (20, 15.5)], r=S.r))]


# ============================================================================ phone

@icon("phone-call", CAT, "Telephone handset with sound waves; an active call.",
      tags=["call", "calling", "telephone", "phone", "ring", "talk"])
def _(S):
    return [shell(handset(S)), line(arc(13, 11, 4, 270, 360)), line(arc(13, 11, 8, 270, 360))]


@icon("phone-incoming", CAT, "Telephone handset with an arrow coming in; an incoming call.",
      tags=["incoming call", "receive", "call", "telephone", "inbound"])
def _(S):
    return [shell(handset(S)), line(seg(20.5, 3.5, 15, 9)), line(poly([(14.5, 4.5), (14.5, 9.5), (19.5, 9.5)], r=S.r))]


@icon("phone-outgoing", CAT, "Telephone handset with an arrow going out; an outgoing call.",
      tags=["outgoing call", "dial", "call", "telephone", "outbound"])
def _(S):
    return [shell(handset(S)), line(seg(14, 10, 19.5, 4.5)), line(poly([(15, 3.5), (20.5, 3.5), (20.5, 9)], r=S.r))]


@icon("phone-missed", CAT, "Telephone handset with a bounced arrow; a missed call.",
      tags=["missed call", "call", "telephone", "unanswered", "notification"])
def _(S):
    return [shell(handset(S)), line(poly([(12.5, 4.5), (16, 8), (20.5, 3.5)], r=S.r)),
            line(poly([(16.5, 3.5), (20.5, 3.5), (20.5, 7.5)], r=S.r))]


@icon("phone-ringing", CAT, "Telephone handset with ringing marks; the phone is ringing.",
      tags=["ringing", "ring", "call", "telephone", "incoming", "vibrate"])
def _(S):
    rays = [line(seg(*polar(12.5, 11.5, 4.5, a), *polar(12.5, 11.5, 8.5, a))) for a in (-80, -45, -10)]
    return [shell(handset(S)), *rays]


@icon("voicemail", CAT, "Two reels joined by tape; a voicemail message.",
      tags=["voicemail", "voice message", "answering machine", "tape", "recording"])
def _(S):
    rx = 3 if S.name == "line" else 4
    return [shell(rect(2.5, 8.5, 8, 8, rx)), shell(rect(13.5, 8.5, 8, 8, rx)), line(seg(6.5, 16.5, 17.5, 16.5))]


@icon("video-call", CAT, "Video camera with a person inside; a video call.",
      tags=["video call", "video chat", "meeting", "webcam", "facetime", "conference"])
def _(S):
    return [shell(rect(2, 5, 14, 14, S.R * 0.75)),
            shell(poly([(16, 10), (21.5, 7), (21.5, 17), (16, 14)], closed=True, r=S.r * 0.5)),
            detail(circle(9, 10, 1.75)),
            detail("M5 19V17.5A2.5 2.5 0 0 1 7.5 15H10.5A2.5 2.5 0 0 1 13 17.5V19")]


@icon("contact", CAT, "Person with a telephone handset beside them; a contact to call.",
      tags=["contact", "person", "call", "reach", "get in touch", "phone"], aliases=["contact-person"])
def _(S):
    return [shell(circle(8.5, 9, 3.5)),
            line("M2.5 21V20A5.5 5.5 0 0 1 8 14.5H9A5.5 5.5 0 0 1 14.5 20V21"),
            shell(handset(S, 0.4, 12.2, -9.6))]


@icon("address-book", CAT, "Ring-bound address book with a person on the cover.",
      tags=["contacts", "address book", "directory", "phonebook", "people"], aliases=["phonebook"])
def _(S):
    return [shell(rect(6, 2.5, 14, 19, S.R * 0.75)),
            detail(circle(13, 9.5, 2.25)),
            detail("M9 17.5V17A3 3 0 0 1 12 14H14A3 3 0 0 1 17 17V17.5"),
            line(seg(3.5, 7, 8, 7)), line(seg(3.5, 12, 8, 12)), line(seg(3.5, 17, 8, 17))]


def _rot(pts, deg, c=(12, 12)):
    a = math.radians(deg)
    return [(c[0] + (x - c[0]) * math.cos(a) - (y - c[1]) * math.sin(a),
             c[1] + (x - c[0]) * math.sin(a) + (y - c[1]) * math.cos(a)) for x, y in pts]


@icon("megaphone", CAT, "Hand-held megaphone with a handle; loudhailer.",
      tags=["megaphone", "bullhorn", "loudhailer", "shout", "marketing", "campaign"], aliases=["bullhorn"])
def _(S):
    rot = -18
    cone = _rot([(3, 9.5), (6.5, 9.5), (18.5, 4), (18.5, 20), (6.5, 14.5), (3, 14.5)], rot, (12, 13))
    handle = _rot([(8.5, 15.5), (9.5, 20.5), (12.5, 20.5), (12, 17.2)], rot, (12, 13))
    lip = _rot([(15.5, 5.4), (15.5, 18.6)], rot, (12, 13))
    return [shell(poly(cone, closed=True, r=S.r * 0.6)), line(poly(handle, r=S.r * 0.6)),
            detail(seg(*lip[0], *lip[1]))]


@icon("broadcast", CAT, "Point with signal waves on both sides; broadcast or live signal.",
      tags=["broadcast", "signal", "live", "radio", "transmit", "on air", "podcast"])
def _(S):
    return [dot(12, 12, 2.25),
            line(arc(12, 12, 5, 135, 225)), line(arc(12, 12, 5, 315, 45)),
            line(arc(12, 12, 9, 140, 220)), line(arc(12, 12, 9, 320, 40))]


@icon("rss", CAT, "Dot with two quarter arcs; web feed.",
      tags=["rss", "feed", "subscribe", "atom", "blog", "news feed"], aliases=["feed"])
def _(S):
    return [dot(6, 18, 2), line(arc(5, 19, 7.5, 270, 360)), line(arc(5, 19, 14, 270, 360))]


@icon("podcast", CAT, "Microphone with waves on both sides; a podcast.",
      tags=["podcast", "audio show", "episode", "microphone", "listen", "broadcast"])
def _(S):
    return [shell(rect(9.5, 3, 5, 10, 2.5)),
            line("M8 11.5A4 4 0 0 0 16 11.5"),
            line(seg(12, 15.5, 12, 21)),
            line(arc(12, 8, 7.5, 145, 215)), line(arc(12, 8, 7.5, 325, 35))]


@icon("antenna", CAT, "Radio mast with a transmitter emitting waves.",
      tags=["antenna", "radio tower", "transmitter", "signal", "broadcast", "mast"], aliases=["radio-tower"])
def _(S):
    return [dot(12, 7, 2),
            line(poly([(7, 21.5), (12, 10.5), (17, 21.5)], r=S.r)), line(seg(9.3, 16.5, 14.7, 16.5)),
            line(arc(12, 7, 4.5, 145, 215)), line(arc(12, 7, 4.5, 325, 35)),
            line(arc(12, 7, 8.5, 150, 210)), line(arc(12, 7, 8.5, 330, 30))]


@icon("satellite-dish", CAT, "Satellite dish on a stand, aimed up and to the right.",
      tags=["satellite", "dish", "receiver", "tv", "signal", "parabolic"])
def _(S):
    dish = "M4.5 7.5A10 10 0 0 0 16.5 19.5Z"
    return [shell(dish),
            line(poly([(10.5, 13.5), (15.5, 8.5)], r=S.r)), dot(16.5, 7.5, 1.75),
            line(poly([(7.5, 17), (5, 21.5)], r=S.r)), line(seg(3, 21.5, 11, 21.5)),
            line(arc(16.5, 7.5, 4.5, 270, 360))]


@icon("walkie-talkie", CAT, "Hand-held two-way radio with an antenna.",
      tags=["walkie talkie", "two-way radio", "radio", "transceiver", "push to talk"], aliases=["two-way-radio"])
def _(S):
    return [shell(rect(6, 7.5, 12, 14, S.R * 0.75)),
            line(seg(9, 7.5, 9, 2.5)),
            detail(seg(9, 11.5, 15, 11.5)), detail(seg(9, 14.5, 15, 14.5)),
            dot(12, 18.25, 1.2)]


@icon("fax", CAT, "Fax machine with a page coming out of the top.",
      tags=["fax", "facsimile", "machine", "office", "document", "print"])
def _(S):
    return [line(poly([(7, 10), (7, 3), (17, 3), (17, 10)], r=S.r * 0.6)),
            detail(seg(9.5, 6.5, 14.5, 6.5)),
            shell(rect(3, 10, 18, 11, S.R * 0.75)),
            detail(seg(6.5, 14, 11.5, 14)),
            dot(15, 14, 1.1), dot(18, 14, 1.1), dot(15, 17.5, 1.1), dot(18, 17.5, 1.1)]


@icon("pager", CAT, "Pager with a text display and a button; beeper.",
      tags=["pager", "beeper", "bleeper", "on call", "notification", "device"], aliases=["beeper"])
def _(S):
    return [shell(rect(2.5, 5, 19, 14, S.R * 0.75)),
            detail(rect(6, 8.5, 12, 4, min(S.R * 0.25, 1))),
            dot(9, 15.5, 1.1), dot(15, 15.5, 1.1)]


@icon("speech-bubble", CAT, "Oval speech bubble with a curved tail; someone speaking.",
      tags=["speech", "talk", "say", "dialogue", "comic", "bubble"])
def _(S):
    cx, cy, rx, ry = 12, 10.5, 9, 7
    a1, a2 = math.radians(158), math.radians(112)
    p1 = (cx + rx * math.cos(a1), cy + ry * math.sin(a1))
    p2 = (cx + rx * math.cos(a2), cy + ry * math.sin(a2))
    tip = (4, 21) if S.name == "line" else (4.3, 20.6)
    tail = (f"C{P2(8, 19)} {P2(6.5, 20.5)} {P2(*tip)}" + ("" if S.name == "line" else f"Q{P2(3.6, 21.2)} {P2(3.9, 20.3)}")
            + f"C{P2(5, 18.5)} {P2(5.2, 16.5)} {P2(*p1)}")
    return [shell(f"M{P2(*p1)}A{rx} {ry} 0 1 1 {P2(*p2)}" + tail + "Z")]


@icon("thought-bubble", CAT, "Cloud-shaped bubble with a trail of small circles; a thought.",
      tags=["thought", "think", "idea", "dream", "thinking", "cloud"])
def _(S):
    cloud = ("M7.5 15A3.25 3.25 0 0 1 5 9.2A3.5 3.5 0 0 1 10 5A4 4 0 0 1 17 5.4"
             "A3.5 3.5 0 0 1 19.5 11.5A3.25 3.25 0 0 1 15.5 15" + ("Z" if S.name == "line" else "Q11.5 16.2 7.5 15Z"))
    return [shell(cloud), shell(circle(6.5, 18.5, 1.5)), dot(3.5, 21, 1.1)]


@icon("quote-bubble", CAT, "Speech bubble containing quotation marks; a quote or testimonial.",
      tags=["quote", "quotation", "testimonial", "cite", "said", "comment"])
def _(S):
    def mark(x):
        return [dot(x, 9.5, 1.75), detail(f"M{fmt(x + 1.6)} 9.8C{fmt(x + 1.6)} 11.8 {fmt(x + 0.5)} 13 {fmt(x - 1.2)} 13.5")]
    return [shell(chat_bubble(S)), *mark(9), *mark(14.5)]


@icon("conversation", CAT, "Two speech bubbles from opposite sides; a back-and-forth dialogue.",
      tags=["conversation", "dialogue", "discussion", "reply", "talk", "exchange"], aliases=["dialogue"])
def _(S):
    a = [(2.5, 3), (15, 3), (15, 9.5), (8, 9.5), (4.5, 12.5), (4.5, 9.5), (2.5, 9.5)]
    b = [(9, 13), (21.5, 13), (21.5, 19.5), (19.5, 19.5), (19.5, 22), (16, 19.5), (9, 19.5)]
    return [shell(poly(a, closed=True, r=S.r)), shell(poly(b, closed=True, r=S.r))]


@icon("announcement", CAT, "Speech bubble with an exclamation mark; an announcement.",
      tags=["announcement", "notice", "news", "important", "alert", "broadcast"])
def _(S):
    return [shell(chat_bubble(S)), detail(seg(12, 7, 12, 11)), dot(12, 13.75, 1.3)]


@icon("inbox-full", CAT, "Inbox tray holding a stack of papers; unread items waiting.",
      tags=["inbox", "tray", "full", "unread", "pending", "messages"], aliases=["tray-full"])
def _(S):
    tray = [(3, 13), (8, 13), (9.5, 16), (14.5, 16), (16, 13), (21, 13), (21, 21), (3, 21)]
    return [shell(poly(tray, closed=True, r=S.r)), line(seg(6, 9.5, 18, 9.5)), line(seg(8, 5.5, 16, 5.5))]


@icon("newsletter", CAT, "Page with a masthead rising out of an envelope; an email newsletter.",
      tags=["newsletter", "subscribe", "bulletin", "digest", "email", "news"])
def _(S):
    pocket = [(3, 11), (12, 16.5), (21, 11), (21, 21), (3, 21)]
    return [shell(poly(pocket, closed=True, r=S.r)),
            line(poly([(6.5, 11.5), (6.5, 3), (17.5, 3), (17.5, 11.5)], r=S.r)),
            solid(rect(9, 5.5, 6, 2.5, 0 if S.name == "line" else 0.6)), line(seg(9, 10.5, 15, 10.5))]


@icon("email-at", CAT, "Envelope with an at sign; an email address.",
      tags=["email", "address", "at", "contact", "mail", "e-mail"], aliases=["email-address"])
def _(S):
    c, r_in, r_out = (16.5, 8.25), 2, 5.25
    at = [shell(circle(*c, r_in)),
          line(f"M{P2(c[0] + r_in, c[1] - 1.5)}V{fmt(c[1] + 1)}A1.5 1.5 0 0 0 {P2(c[0] + r_out, c[1] + 1)}V{fmt(c[1])}"
               f"A{r_out} {r_out} 0 1 0 {P2(*polar(*c, r_out, 62))}")]
    body = rect(2.5, 9.5, 13.5, 11, S.R * 0.5)
    flap = poly([(3, 11), (9.25, 15.5), (15.5, 11)], r=S.r)
    hidden = lambda x, y: math.hypot(x - c[0], y - c[1]) < r_out + 3  # noqa: E731
    return [*at, line(outside(body, hidden)), line(outside(flap, hidden))]


@icon("letter", CAT, "Envelope sealed with a wax seal; a letter.",
      tags=["letter", "envelope", "post", "mail", "correspondence", "sealed"])
def _(S):
    return [shell(rect(2.5, 5, 19, 14, S.R * 0.5)),
            detail(poly([(3, 6), (9.8, 12)], r=S.r)), detail(poly([(14.2, 12), (21, 6)], r=S.r)),
            dot(12, 12.5, 2.25)]


@icon("postcard", CAT, "Postcard with a stamp, message lines and address lines.",
      tags=["postcard", "travel", "greeting", "mail", "card", "holiday"])
def _(S):
    return [shell(rect(2, 4.5, 20, 15, S.R * 0.5)),
            detail(seg(12, 8, 12, 16)),
            detail(rect(15.5, 7.5, 3.5, 3.5, min(S.R * 0.25, 0.75))),
            detail(seg(5, 9, 9, 9)), detail(seg(5, 12.5, 9, 12.5)),
            detail(seg(14.5, 15, 19, 15))]


def _perforated(x0, y0, x1, y1, n, br):
    """Closed outline of a stamp: rectangle with n semicircular bites per edge."""
    def edge(ax, ay, bx, by):
        L = math.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / L, (by - ay) / L
        out = ""
        for k in range(n):
            t = (k + 0.5) / n * L
            cx, cy = ax + ux * t, ay + uy * t
            p1 = (cx - ux * br, cy - uy * br)
            p2 = (cx + ux * br, cy + uy * br)
            out += f"L{P2(*p1)}A{br} {br} 0 0 0 {P2(*p2)}"
        return out + f"L{P2(bx, by)}"
    return (f"M{P2(x0, y0)}" + edge(x0, y0, x1, y0) + edge(x1, y0, x1, y1) + edge(x1, y1, x0, y1)
            + edge(x0, y1, x0, y0) + "Z")


_STAMP = (3.5, 3, 20.5, 21, 4, 1)
_STAMP_PIC = [(7.5, 16.5), (10.5, 12), (12.5, 14), (14, 12.5), (16.5, 16.5)]


def _stamp_filled():
    x0, y0, x1, y1, n, br = _STAMP
    body = P(rect(x0 - 1, y0 - 1, x1 - x0 + 2, y1 - y0 + 2))
    bites = []
    for k in range(n):
        fx = x0 + (k + 0.5) / n * (x1 - x0)
        fy = y0 + (k + 0.5) / n * (y1 - y0)
        bites += [P(circle(fx, y0 - 1, br + 0.9)), P(circle(fx, y1 + 1, br + 0.9)),
                  P(circle(x0 - 1, fy, br + 0.9)), P(circle(x1 + 1, fy, br + 0.9))]
    pic = ST(poly(_STAMP_PIC), 2.0)
    return D(body, *bites, pic, P(circle(14.5, 8.5, 1.5)))


@icon("stamp-postage", CAT, "Postage stamp with perforated edges.",
      tags=["stamp", "postage", "post", "mail", "philately", "letter"], aliases=["postage-stamp"], filled=_stamp_filled)
def _(S):
    return [shell(_perforated(*_STAMP)),
            detail(poly(_STAMP_PIC, r=S.r * 0.5)),
            dot(14.5, 8.5, 1.4)]


@icon("telegram-message", CAT, "Strip of telegraph tape printed with Morse code; a telegram.",
      tags=["telegram", "telegraph", "morse", "wire", "cable", "message"], aliases=["telegraph"])
def _(S):
    ribbon = [(2.5, 7.5), (21.5, 7.5), (19.5, 12), (21.5, 16.5), (2.5, 16.5), (4.5, 12)]
    return [shell(poly(ribbon, closed=True, r=S.r * 0.5), stroke_miterlimit="2.5"),
            detail(seg(7, 12, 10, 12)), dot(12.25, 12, 1.1), detail(seg(14.5, 12, 17.5, 12))]


@icon("signal-bars", CAT, "Four ascending bars; signal strength.",
      tags=["signal", "reception", "cellular", "strength", "bars", "network"], aliases=["signal-strength"])
def _(S):
    return [line(seg(4.5, 21, 4.5, 17)), line(seg(9.5, 21, 9.5, 13)), line(seg(14.5, 21, 14.5, 8.5)),
            line(seg(19.5, 21, 19.5, 3.5))]


@icon("chat-typing", CAT, "Pill-shaped bubble with three dots; someone is typing.",
      tags=["typing", "typing indicator", "chat", "writing", "ellipsis", "pending"])
def _(S):
    return [shell(rect(3, 4, 18, 10, S.R * 1.25)),
            dot(8, 9, 1.3), dot(12, 9, 1.3), dot(16, 9, 1.3),
            dot(6, 17.5, 1.6), dot(3.5, 20.5, 1.1)]


@icon("mail-flag", CAT, "Envelope beside a raised flag; a flagged email.",
      tags=["flagged", "important", "follow up", "email", "mail", "mark"])
def _(S):
    return [*envelope(S, 2.5, 9, 12.5, 11.5),
            line(seg(18, 21, 18, 3)),
            shell(poly([(18, 3), (21.5, 3), (20, 6), (21.5, 9), (18, 9)], closed=True, r=S.r * 0.4))]


@icon("intercom", CAT, "Wall intercom with a speaker grille and a call button.",
      tags=["intercom", "door phone", "entry phone", "buzzer", "doorbell", "speaker"], aliases=["door-phone"])
def _(S):
    return [shell(rect(5.5, 2.5, 13, 19, S.R * 0.75)),
            detail(circle(12, 8.5, 3)), dot(12, 8.5, 1),
            detail(seg(9.5, 16.5, 14.5, 16.5))]


@icon("speakerphone", CAT, "Mobile phone emitting sound waves; call on speaker.",
      tags=["speakerphone", "speaker", "loudspeaker", "hands-free", "call", "phone"], aliases=["hands-free"])
def _(S):
    return [shell(rect(3, 2.5, 10.5, 19, S.R * 0.75)), detail(seg(7.25, 18, 9.25, 18)),
            line(arc(12.5, 12, 4.5, -40, 40)), line(arc(12.5, 12, 8.5, -40, 40))]


@icon("headset-support", CAT, "Head wearing a headset with a microphone; customer support.",
      tags=["support", "customer service", "help desk", "call center", "agent", "headset"],
      aliases=["customer-support", "call-center"])
def _(S):
    return [shell(circle(12, 11, 4.5)),
            line(arc(12, 11, 8, 190, 350)),
            shell(rect(2.5, 10, 3, 6, min(S.R * 0.5, 1.5))), shell(rect(18.5, 10, 3, 6, min(S.R * 0.5, 1.5))),
            line("M20 16V17.5A3 3 0 0 1 17 20.5H14"), dot(13, 20.5, 1.5)]
