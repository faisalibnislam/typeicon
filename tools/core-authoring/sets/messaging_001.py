"""TypeIcon Core: messaging (batch 001). Chat bubbles, mail, phones and calls."""
import math
import re

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, polar

CAT = "messaging"


# --------------------------------------------------------------------------- local helpers

def P2(x, y):
    return f"{fmt(x)} {fmt(y)}"


def kd(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


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
    """Open path(s) tracing the parts of outline d where hidden(x, y) is False."""
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
        for i in order:
            if keep[i]:
                run.append(pts[i])
            elif run:
                if len(run) > 1:
                    out.append("M" + "L".join(P2(*p) for p in run))
                run = []
        if len(run) > 1:
            out.append("M" + "L".join(P2(*p) for p in run))
    return "".join(out)


def clip_y(pts, ymax, closed=True):
    """Open polyline(s) along the polygon edges, keeping only the part with y <= ymax."""
    n = len(pts)
    runs, cur = [], []
    edges = [(pts[i], pts[(i + 1) % n]) for i in range(n if closed else n - 1)]
    for (x1, y1), (x2, y2) in edges:
        in1, in2 = y1 <= ymax, y2 <= ymax
        if in1 and not cur:
            cur = [(x1, y1)]
        if in1 and in2:
            cur.append((x2, y2))
        elif in1 != in2:
            t = (ymax - y1) / (y2 - y1)
            xi = x1 + (x2 - x1) * t
            if in1:
                cur.append((xi, ymax))
                runs.append(cur)
                cur = []
            else:
                cur = [(xi, ymax), (x2, y2)]
    if cur:
        runs.append(cur)
    if len(runs) > 1 and closed and runs[0][0] == runs[-1][-1]:
        runs[0] = runs.pop()[:-1] + runs[0]
    return runs


def rot_pts(pts, deg, c):
    a = math.radians(deg)
    return [(c[0] + (x - c[0]) * math.cos(a) - (y - c[1]) * math.sin(a),
             c[1] + (x - c[0]) * math.sin(a) + (y - c[1]) * math.cos(a)) for x, y in pts]


_HANDSET_R = ("M5.2 3.5H8.6L10.4 8L8.1 9.5A11 11 0 0 0 14.5 15.9L16 13.6L20.5 15.4V18.8"
              "A1.7 1.7 0 0 1 18.8 20.5A15.5 15.5 0 0 1 3.5 5.2A1.7 1.7 0 0 1 5.2 3.5Z")
_HANDSET_L = "M3.5 3.5H8.6L10.4 8L8.1 9.5A11 11 0 0 0 14.5 15.9L16 13.6L20.5 15.4V20.5H19A15.5 15.5 0 0 1 3.5 5Z"


def handset(S, s=0.82, ox=0.0, oy=0.0):
    """Telephone handset (earpiece top-left, mouthpiece bottom-right), scaled about its bottom-left."""
    d = _HANDSET_L if S.name == "line" else _HANDSET_R
    return tx(d, s, ox, oy, ax=3.0, ay=21.0)


def bub(S, x0=2.5, y0=2.5, x1=21.5, y1=18.0, tip=(7.0, 22.0), tx0=7.0, tx1=11.5):
    """Rectangular chat bubble with a tail hanging below the bottom-left."""
    return poly([(x0, y0), (x1, y0), (x1, y1), (tx1, y1), tip, (tx0, y1), (x0, y1)], closed=True, r=S.r * 1.3)


def person(cx, cy, s=1.0):
    """Head-and-shoulders (inner details): head centre (cx, cy), shoulders below."""
    return [detail(circle(cx, cy, 1.6 * s)),
            detail(f"M{P2(cx - 3.5 * s, cy + 6.4 * s)}A{fmt(3.5 * s)} {fmt(3.2 * s)} 0 0 1 {P2(cx + 3.5 * s, cy + 6.4 * s)}")]


def heart_d(S, cx, cy, u):
    """Heart about (cx, cy), half-width u (pointed tip in Line, softened tip in Rounded)."""
    def q(x, y):
        return P2(cx + x * u, cy + y * u)
    tip = (f"L{q(0.12, 0.92)}Q{q(0, 1.05)} {q(-0.12, 0.92)}" if S.name == "rounded" else f"L{q(0, 1)}")
    if S.name == "rounded":
        head = f"M{q(0.12, 0.92)}"
        tail = f"C{q(-0.5, 0.6)} {q(-1, 0.25)} {q(-1, -0.35)}"
    else:
        head = f"M{q(0, 1)}"
        tail = f"C{q(-0.5, 0.65)} {q(-1, 0.25)} {q(-1, -0.35)}"
    left = (f"C{q(-1, -0.95)} {q(-0.6, -1.25)} {q(-0.3, -1.25)}C{q(-0.1, -1.25)} {q(0, -1.05)} {q(0, -0.8)}")
    right = (f"C{q(0, -1.05)} {q(0.1, -1.25)} {q(0.3, -1.25)}C{q(0.6, -1.25)} {q(1, -0.95)} {q(1, -0.35)}"
             f"C{q(1, 0.25)} {q(0.5, 0.65)} " + (q(0.12, 0.92) if S.name == "rounded" else q(0, 1)))
    if S.name == "rounded":
        return head + tail + left + right + f"Q{q(0, 1.05)} {q(-0.12, 0.92)}Z"
    return head + tail + left + right + "Z"


def env(S, x, y, w, h, flap=True):
    """Closed envelope: body + V flap."""
    out = [shell(rect(x, y, w, h, S.R * 0.5))]
    if flap:
        out.append(detail(poly([(x + 0.8, y + 1.6), (x + w / 2, y + h * 0.55), (x + w - 0.8, y + 1.6)], r=S.r)))
    return out


def star_pts(cx, cy, R, r, n, start=-90.0):
    out = []
    for i in range(2 * n):
        out.append(polar(cx, cy, R if i % 2 == 0 else r, start + i * 180 / n))
    return out


# ============================================================================ chat bubbles

@icon("voice-message", CAT, "Speech bubble holding three audio waveform bars.",
      tags=["voice note", "audio message", "waveform", "voice", "record", "chat", "sound"])
def _(S):
    return [shell(bub(S)), detail(seg(8, 8.5, 8, 12)), detail(seg(12, 6, 12, 14.5)), detail(seg(16, 8, 16, 12.5))]


@icon("video-message", CAT, "Speech bubble with a play triangle inside.",
      tags=["video note", "video chat", "clip", "play", "recorded video", "chat"])
def _(S):
    return [shell(bub(S)), kd(poly([(9.5, 6), (9.5, 14.5), (16, 10.25)], closed=True, r=S.r * 0.6))]


@icon("photo-message", CAT, "Speech bubble with a tiny picture of a mountain and a sun.",
      tags=["picture message", "image", "photo", "attachment", "chat", "mms"])
def _(S):
    return [shell(bub(S)), detail(poly([(6, 14.5), (10, 8.5), (13, 12.5), (14.5, 11), (18, 14.5)], r=S.r * 0.8)),
            dot(15.5, 7, 1.3)]


@icon("shared-contact", CAT, "Speech bubble with a head-and-shoulders silhouette inside.",
      tags=["contact card", "share contact", "person", "profile", "chat", "vcard"])
def _(S):
    return [shell(bub(S)), detail(circle(12, 7.6, 1.7)),
            detail("M8 15A4 3.4 0 0 1 16 15")]


@icon("group-chat", CAT, "Speech bubble with three heads in a row inside it.",
      tags=["group message", "team chat", "people", "members", "community", "conversation"])
def _(S):
    return [shell(bub(S, 2.0, 2.0, 22.0, 18.0, (6.5, 22.0), 6.5, 11.0)),
            dot(6.5, 9.2, 1.45), dot(17.5, 9.2, 1.45), dot(12, 7.4, 1.8),
            detail("M8.3 15A3.7 3.4 0 0 1 15.7 15")]


@icon("direct-message", CAT, "Speech bubble with a small paper plane inside.",
      tags=["dm", "private message", "send", "inbox", "chat", "paper plane"])
def _(S):
    return [shell(bub(S)), kd(poly([(6.5, 9), (17.5, 5.5), (13.5, 14.5), (11, 10.5)], closed=True, r=S.r * 0.4))]


@icon("quick-reply", CAT, "Speech bubble with a lightning bolt inside.",
      tags=["fast reply", "instant answer", "lightning", "auto reply", "canned response", "chat"])
def _(S):
    return [shell(bub(S)), kd(poly([(13.3, 4.8), (7.8, 10.6), (11.2, 10.6), (10.2, 15.6), (16.2, 9.4), (12.8, 9.4)], closed=True, r=S.r * 0.3))]


@icon("emoji-reaction", CAT, "Speech bubble with a smiley face overlapping its lower corner.",
      tags=["react", "emoji", "smiley", "reaction", "like", "chat", "sticker"])
def _(S):
    b = poly([(17, 8.5), (17, 2.5), (2.5, 2.5), (2.5, 13.5), (4.5, 13.5), (4.5, 17.5), (8.3, 13.5), (8.8, 13.5)], r=S.r * 1.1)
    c, r = (16.5, 16.5), 5.5
    return [line(b), shell(circle(*c, r)), dot(14.6, 15.2, 0.95), dot(18.4, 15.2, 0.95),
            detail("M14 17.6A3 2.6 0 0 0 19 17.6")]


@icon("chatbot", CAT, "Speech bubble showing a robot face with an antenna and square eyes.",
      tags=["bot", "assistant", "robot", "automation", "support bot", "chat", "virtual agent"])
def _(S):
    return [shell(bub(S, 2.5, 6.5, 21.5, 18.5, (7, 22.0), 7.0, 11.5)), line(seg(12, 6.5, 12, 3.5)), dot(12, 2.8, 1.2),
            kd(rect(7.5, 9.5, 2.5, 2.5)), kd(rect(14, 9.5, 2.5, 2.5)), detail(seg(9, 15, 15, 15))]


@icon("ai-chat", CAT, "Speech bubble with a four-point sparkle inside.",
      tags=["ai", "assistant", "sparkle", "generative", "copilot", "chat", "smart reply"])
def _(S):
    sp = "M12 4.2Q12.9 9.3 18 10.3Q12.9 11.3 12 16.4Q11.1 11.3 6 10.3Q11.1 9.3 12 4.2Z"
    return [shell(bub(S)), kd(sp)]


@icon("shout-bubble", CAT, "Jagged starburst speech balloon with a pointed tail.",
      tags=["shout", "yell", "exclaim", "comic", "burst", "loud", "angry"])
def _(S):
    pts = star_pts(12, 10.8, 8.4, 5.8, 9)
    tail = polar(12, 10.8, 12.0, 130)
    pts = pts[:11] + [tail] + pts[12:]
    return [shell(poly(pts, closed=True, r=S.r * 0.5), stroke_miterlimit="3")]


@icon("whisper-bubble", CAT, "Speech balloon drawn with a dashed outline and a small tail.",
      tags=["whisper", "quiet", "private", "low voice", "dashed bubble", "secret", "hush"])
def _(S):
    c, r = (12.5, 10.5), 8.5
    parts = [line(arc(*c, r, a, a + 28)) for a in (-84, -38, 8, 54, 100)]
    parts += [line(arc(*c, r, a, a + 28)) for a in (192, 238)]
    p1, p2, tip = polar(*c, r, 152), polar(*c, r, 118), (4.5, 20)
    parts += [line(f"M{P2(*p1)}L{P2(*tip)}L{P2(*p2)}")]
    return parts


@icon("forwarded-message", CAT, "Speech bubble with a double right-pointing chevron inside.",
      tags=["forward", "pass on", "share message", "resend", "chat", "fast forward"])
def _(S):
    return [shell(bub(S)), detail(poly([(7, 6.5), (10.8, 10.25), (7, 14)], r=S.r)),
            detail(poly([(12.5, 6.5), (16.3, 10.25), (12.5, 14)], r=S.r))]


@icon("text-emoticon", CAT, "Speech bubble holding a sideways smiley made of a colon and a bracket.",
      tags=["emoticon", "smiley", "colon bracket", "text face", "happy", "chat", "ascii"])
def _(S):
    return [shell(bub(S)), dot(7.5, 7.8, 1.3), dot(7.5, 12.7, 1.3), detail("M12.5 6.3Q18.5 10.25 12.5 14.2")]


@icon("meme-image", CAT, "Picture frame with a text bar across its top and bottom and a simple face between them.",
      tags=["meme", "caption", "funny picture", "image macro", "joke", "viral", "social"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, S.R * 0.75)), kd(rect(6, 5.5, 12, 2)), kd(rect(6, 16.5, 12, 2)),
            dot(9.8, 10.6, 1.0), dot(14.2, 10.6, 1.0), detail("M9.6 13.4Q12 15.2 14.4 13.4")]


@icon("audio-room", CAT, "Four small avatar heads around a central microphone.",
      tags=["voice room", "live audio", "speakers", "listeners", "podcast chat", "social audio"])
def _(S):
    return [dot(12, 3.9, 2.0), dot(20.1, 12, 2.0), dot(12, 20.1, 2.0), dot(3.9, 12, 2.0),
            shell(rect(9.6, 7.2, 4.8, 7.6, 1.4 if S.name == "line" else 2.4))]


@icon("live-reactions", CAT, "Three hearts floating upward in a staggered trail.",
      tags=["hearts", "live stream", "reactions", "love", "floating hearts", "like", "broadcast"])
def _(S):
    return [shell(heart_d(S, 8, 17.2, 3.3)), shell(heart_d(S, 16.5, 11, 3.3)), shell(heart_d(S, 8.5, 6.5, 2.7))]


@icon("link-in-bio", CAT, "Phone screen with a round avatar at the top and three stacked link buttons below.",
      tags=["bio link", "profile links", "landing page", "creator", "social profile", "smartphone"])
def _(S):
    return [shell(rect(5, 2, 14, 20, S.R * 0.9)), dot(12, 6.6, 1.8),
            detail(seg(8.5, 11.5, 15.5, 11.5)), detail(seg(8.5, 14.8, 15.5, 14.8)), detail(seg(8.5, 18.1, 15.5, 18.1))]


def _banner_filled():
    banner = D(P(rect(2, 4, 20, 12)), P(circle(12, 15.5, 6.4)))
    return U(banner, P(circle(12, 15.5, 4.6)))


@icon("profile-banner", CAT, "Wide cover rectangle with a round avatar overlapping its bottom edge.",
      tags=["cover photo", "header image", "profile", "avatar", "social profile", "banner"], filled=_banner_filled)
def _(S):
    return [line(poly([(5, 15.5), (2.5, 15.5), (2.5, 4.5), (21.5, 4.5), (21.5, 15.5), (19, 15.5)], r=S.r * 0.8)),
            shell(circle(12, 15.5, 3.6))]


@icon("q-and-a", CAT, "Speech bubble with a question mark and a round bubble with a check mark overlapping its corner.",
      tags=["question", "answer", "faq", "ask", "help", "forum", "interview"])
def _(S):
    back = poly([(16.5, 7.7), (16.5, 2.5), (2.5, 2.5), (2.5, 15), (4.8, 15), (4.8, 18.5), (8.4, 15)], r=S.r * 0.9)
    return [line(back), shell(circle(16.8, 16.5, 5.3)),
            detail("M7.6 7.1A1.9 1.9 0 1 1 10.3 8.8Q9.5 9.4 9.5 10.4"), dot(9.5, 12.7, 0.9),
            detail(poly([(14.4, 16.6), (16.1, 18.3), (19.3, 14.9)], r=S.r * 0.4))]

@icon("love-letter", CAT, "Closed envelope with a heart sealing the point of its flap.",
      tags=["valentine", "romance", "heart", "letter", "card", "affection", "envelope"])
def _(S):
    return [shell(rect(2.5, 4.5, 19, 15, S.R * 0.5)),
            detail(poly([(3.5, 6), (9.3, 11)], r=S.r)), detail(poly([(14.7, 11), (20.5, 6)], r=S.r)),
            Part("dot", heart_d(S, 12, 12.2, 2.4))]


@icon("red-envelope", CAT, "Tall narrow envelope with a pointed flap and a round emblem in the centre, used for gifting money.",
      tags=["hongbao", "lucky money", "gift money", "lunar new year", "festive", "eid", "angpao", "money envelope"])
def _(S):
    return [shell(rect(5.5, 2.5, 13, 19, S.R * 0.75)), detail(seg(5.5, 7, 18.5, 7)), dot(12, 14, 2.8)]

@icon("stamped-envelope", CAT, "Envelope front with a small stamp in the top-right corner and address lines.",
      tags=["postage", "stamp", "mail", "post", "letter", "address", "envelope"])
def _(S):
    return [shell(rect(2.5, 4.5, 19, 15, S.R * 0.5)), detail(rect(15.2, 7.5, 3.6, 3.6)),
            detail(seg(5.8, 12.6, 11.5, 12.6)), detail(seg(5.8, 16, 10.5, 16))]


@icon("registered-mail", CAT, "Envelope with a large letter R on its front.",
      tags=["certified mail", "tracked post", "recorded delivery", "proof of delivery", "letter", "r mark"])
def _(S):
    return [shell(rect(2.5, 4.5, 19, 15, S.R * 0.5)),
            detail("M9.8 15.5V8.5H12.6A2.2 2.2 0 0 1 12.6 12.9H9.8M12.6 12.9L14.8 15.5")]

@icon("return-to-sender", CAT, "Envelope with a curved U-turn arrow looping back over it.",
      tags=["return mail", "undeliverable", "bounce", "send back", "u-turn", "post", "reply"])
def _(S):
    return [*env(S, 2.5, 12.5, 19, 9), line("M18 11V8.5A6 6 0 0 0 6 8.5V10"), line(poly([(3.5, 7.8), (6, 10.6), (8.5, 7.8)], r=S.r * 0.5))]


@icon("email-signature", CAT, "Envelope with a handwritten signature scribble along its lower half.",
      tags=["signature", "sign off", "autograph", "handwriting", "email footer", "letter", "sign"])
def _(S):
    return [shell(rect(2.5, 4.5, 19, 15, S.R * 0.5)),
            detail(poly([(3.5, 6), (12, 10.6), (20.5, 6)], r=S.r)),
            detail("M6.2 16.4C7.3 13 8.6 13 8.6 15.2C8.6 17 9.8 16.8 10.3 15.3C10.9 13.6 12.4 13.5 12.6 15.2L17.5 15.2")]


@icon("out-of-office", CAT, "Envelope with a small palm tree standing beside it.",
      tags=["away", "vacation", "holiday", "auto reply", "palm tree", "leave", "ooo", "email"])
def _(S):
    return [*env(S, 2, 12, 10.5, 9), line("M17.5 21.5C17.2 18 17.5 14 18 11"),
            line("M18 11C15.5 6 11.5 7 10.5 9.8"), line("M18 11C20.5 6 22 7.5 22.5 10.2"), line(seg(18, 11, 18, 4.5))]



@icon("mailing-list", CAT, "Envelope on the left with three bulleted list lines beside it.",
      tags=["subscribers", "distribution list", "newsletter list", "recipients", "email list", "audience"])
def _(S):
    return [*env(S, 2.5, 8, 9.5, 9.5), dot(15, 7.5, 1.2), dot(15, 12.75, 1.2), dot(15, 18, 1.2),
            line(seg(17.5, 7.5, 21.5, 7.5)), line(seg(17.5, 12.75, 21.5, 12.75)), line(seg(17.5, 18, 21.5, 18))]


@icon("junk-mail", CAT, "Tilted envelope drooping over the rim of a small wastebasket.",
      tags=["spam", "trash mail", "unwanted mail", "flyer", "circular", "discard", "bin"])
def _(S):
    body = [(4.5, 5.5), (16.5, 2.5), (18.5, 10), (6.5, 13)]
    c = (11.5, 7.75)
    env_pts = rot_pts([(3.5, 4.5), (17.5, 4.5), (17.5, 13.5), (3.5, 13.5)], 18, c)
    runs = clip_y(env_pts, 12.0)
    parts = [line(poly(r, r=S.r * 0.8)) for r in runs if len(r) > 1]
    bin_ = poly([(5.5, 13.5), (7, 21.5), (17, 21.5), (18.5, 13.5)], closed=True, r=S.r * 0.6)
    return parts + [shell(bin_), line(seg(4, 13.5, 20, 13.5)), detail(seg(12, 16.5, 12, 19))]


@icon("cluster-mailbox", CAT, "Pedestal cabinet with a grid of small mail doors standing on a short post.",
      tags=["mail cluster", "apartment mailboxes", "post boxes", "letterboxes", "neighborhood mail", "delivery"])
def _(S):
    return [shell(rect(3, 2.5, 18, 13.5, S.R * 0.6)), detail(seg(9, 3.5, 9, 15)), detail(seg(15, 3.5, 15, 15)),
            detail(seg(3.5, 9.25, 20.5, 9.25)), dot(6, 6, 0.9), dot(12, 6, 0.9), dot(18, 6, 0.9),
            dot(6, 12.6, 0.9), dot(12, 12.6, 0.9), dot(18, 12.6, 0.9),
            line(seg(12, 16, 12, 21.5)), line(seg(7.5, 21.5, 16.5, 21.5))]


@icon("stamp-coil", CAT, "Roll of postage stamps with a strip of stamps unwinding from it.",
      tags=["stamps", "postage roll", "stamp strip", "post office", "perforated", "mail supplies"])
def _(S):
    return [shell(circle(8, 9, 5.5)), dot(8, 9, 1.4),
            shell(rect(8, 15, 13.5, 6.5, S.R * 0.3)), detail(seg(14.75, 16, 14.75, 20.5))]


@icon("pen-pal", CAT, "Envelope in front of a small globe.",
      tags=["penfriend", "international mail", "world", "correspondence", "airmail", "letter abroad", "global"])
def _(S):
    c, r = (9.5, 9.5), 6.5
    def hid(x, y):
        return x > 11.5 and y > 12.2 or (x > 13.2 and y > 9.6) or (y > 13.2 and x > 9.6)
    globe = outside(circle(*c, r), hid)
    mer = outside(f"M{P2(9.5, 3)}A2.8 6.5 0 0 0 {P2(9.5, 16)}A2.8 6.5 0 0 0 {P2(9.5, 3)}Z", hid)
    return [line(globe), line(mer), *env(S, 10.5, 12, 11.5, 9)]


@icon("delivery-door-tag", CAT, "Door hanger card with a round hole at the top and a small parcel symbol below.",
      tags=["door hanger", "missed delivery", "parcel notice", "sorry we missed you", "courier card", "package", "note"])
def _(S):
    return [shell(rect(5.5, 2.5, 13, 19, S.R * 0.75)), detail(circle(12, 7, 1.8)),
            detail(rect(8.7, 12.7, 6.6, 5.3)), detail(seg(8.7, 15.2, 15.3, 15.2))]


@icon("customs-form", CAT, "Form sheet with a small globe at the top and rows of checkboxes below.",
      tags=["customs declaration", "shipping form", "international parcel", "export", "border", "paperwork"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 19, S.R * 0.6)), detail(circle(12, 7.2, 2.4)), detail(seg(8.8, 7.2, 15.2, 7.2)),
            kd(rect(7, 12.2, 2.2, 2.2)), detail(seg(11.5, 13.3, 16.5, 13.3)),
            kd(rect(7, 16.6, 2.2, 2.2)), detail(seg(11.5, 17.7, 16.5, 17.7))]


@icon("signature-pad", CAT, "Handheld tablet with a stylus signing a squiggle on its screen.",
      tags=["e-signature", "sign here", "delivery signature", "proof of delivery", "stylus", "pos terminal", "autograph"])
def _(S):
    return [shell(rect(2.5, 5, 19, 15, S.R * 0.75)),
            detail("M5.6 16C6.6 12.6 8 12.6 8 15C8 16.8 9.2 16.4 9.8 14.6C10.3 13.2 11.7 13.4 12 15"),
            detail(seg(13.2, 14.2, 18.2, 9))]


@icon("parcel-tracking", CAT, "Parcel box with a map pin above it and a dotted route line leading away.",
      tags=["track package", "shipment location", "delivery status", "where is my order", "gps", "courier", "route"])
def _(S):
    pin = "M18 15.3C15 12.2 13.3 10.3 13.3 8A4.7 4.7 0 0 1 22.7 8C22.7 10.3 21 12.2 18 15.3Z"
    return [shell(rect(2.5, 11, 10, 10, S.R * 0.5)), detail(seg(7.5, 11.5, 7.5, 15.5)),
            shell(pin), dot(18, 8, 1.4), dot(16, 19.5, 1.0), dot(19.5, 19.5, 1.0)]


@icon("mail-bicycle", CAT, "Bicycle with a large front basket full of envelopes.",
      tags=["courier bike", "postman", "letter carrier", "delivery bike", "cycle post", "messenger", "bicycle"])
def _(S):
    return [shell(circle(5.2, 17.3, 3.6)), shell(circle(18.8, 17.3, 3.6)),
            line("M5.2 17.3L9.2 10.8H14.6L11.4 17.3Z"), line(seg(14.6, 10.8, 18.8, 17.3)),
            line(seg(7.6, 9, 10.8, 9)),
            shell(rect(14.2, 3, 8, 5.5, S.R * 0.3)), detail(poly([(14.8, 4), (18.2, 6.3), (21.6, 4)], r=S.r * 0.5))]


@icon("invitation-card", CAT, "Envelope with a card sticking out that carries a ribbon bow.",
      tags=["invite", "party", "wedding", "event", "save the date", "celebration", "rsvp"])
def _(S):
    bow = [kd(poly([(8.2, 4.9), (11.3, 6.9), (8.2, 8.9)], closed=True)), kd(poly([(15.8, 4.9), (12.7, 6.9), (15.8, 8.9)], closed=True)),
           dot(12, 6.9, 1.1)]
    return [shell(poly([(3, 11), (12, 16.5), (21, 11), (21, 21), (3, 21)], closed=True, r=S.r)),
            line(poly([(6.5, 11.5), (6.5, 3), (17.5, 3), (17.5, 11.5)], r=S.r)), *bow]


@icon("rsvp-card", CAT, "Small reply card with a ticked box and a crossed box, each beside a line.",
      tags=["reply card", "attending", "yes or no", "accept decline", "event response", "wedding reply", "respond"])
def _(S):
    return [shell(rect(3, 3.5, 18, 17, S.R * 0.6)),
            detail(poly([(6, 8.4), (7.8, 10.2), (10.6, 6.8)], r=S.r * 0.4)), detail(seg(13.5, 8.6, 18, 8.6)),
            detail(seg(6.4, 13.4, 9.8, 16.8)), detail(seg(9.8, 13.4, 6.4, 16.8)), detail(seg(13.5, 15.1, 18, 15.1))]


@icon("guestbook", CAT, "Open book with a pen lying across its pages.",
      tags=["visitor book", "sign in book", "register", "wedding book", "memories", "signatures", "log book"])
def _(S):
    book = poly([(2.5, 6.5), (12, 8.5), (21.5, 6.5), (21.5, 18.5), (12, 20.5), (2.5, 18.5)], closed=True, r=S.r * 0.6)
    return [shell(book), detail(seg(12, 9.5, 12, 20)), detail(seg(14.5, 16, 18.5, 9.2)),
            detail(seg(5.5, 10.5, 9, 11.2)), detail(seg(5.5, 14.5, 9, 15.2))]


# ============================================================================ phones and handsets

@icon("payphone", CAT, "Wall-mounted box phone with a handset on its side, a keypad and a coin slot.",
      tags=["pay phone", "public phone", "phone booth", "coin phone", "telephone box", "street phone", "call box"])
def _(S):
    dots = [dot(x, y, 0.9) for y in (11.5, 15, 18.5) for x in (11.2, 14.5, 17.8)]
    return [shell(rect(2.5, 5.5, 3.6, 11, S.R * 0.5 + 0.6)), shell(rect(8, 2.5, 13.5, 19, S.R * 0.75)),
            detail(seg(11, 6.5, 18.5, 6.5)), *dots]


@icon("candlestick-phone", CAT, "Upright stick telephone with a flat mouthpiece on top and a separate earpiece hanging on a hook.",
      tags=["antique phone", "vintage telephone", "old phone", "stick phone", "retro", "early telephone", "1920s"])
def _(S):
    return [shell(poly([(3.5, 21.5), (4.8, 18.5), (15.2, 18.5), (16.5, 21.5)], closed=True, r=S.r * 0.6)),
            line(seg(10, 18.5, 10, 6)),
            shell(poly([(5.8, 2.8), (14.2, 2.8), (14.2, 5.8), (5.8, 5.8)], closed=True, r=S.r * 0.8)),
            line(seg(10, 11, 15.6, 11)), shell(rect(15.6, 8.5, 4, 8, S.R * 0.5 + 0.6)),
            line("M17.6 16.5Q17.6 20 14.8 20.4")]


@icon("flip-phone", CAT, "Clamshell mobile phone opened, with a small screen on the upper half and a keypad on the lower half.",
      tags=["clamshell phone", "cell phone", "old mobile", "folding phone", "y2k", "retro mobile"])
def _(S):
    dots = [dot(x, y, 0.8) for y in (17, 19.4) for x in (9.2, 12, 14.8)]
    return [shell(rect(6, 2, 12, 9.5, S.R * 0.6)), kd(rect(8.8, 4.3, 6.4, 4.2)),
            shell(rect(6, 14, 12, 8, S.R * 0.6)), *dots]


@icon("feature-phone", CAT, "Candy-bar mobile phone with a small screen above a grid of number keys.",
      tags=["basic phone", "keypad phone", "dumb phone", "old mobile", "cell phone", "button phone", "t9"])
def _(S):
    dots = [dot(x, y, 0.8) for y in (13.5, 16.3, 19.1) for x in (9, 12, 15)]
    return [shell(rect(5.5, 2, 13, 20, S.R * 0.8)), detail(rect(8.2, 5, 7.6, 4.4)), *dots]


@icon("brick-phone", CAT, "Large brick-shaped early mobile phone with a stubby antenna.",
      tags=["90s phone", "retro mobile", "early cell phone", "car phone", "vintage", "antenna phone", "old school"])
def _(S):
    dots = [dot(x, y, 0.85) for y in (14.2, 16.9, 19.6) for x in (8.6, 12, 15.4)]
    return [shell(rect(5, 6.5, 14, 15.5, S.R * 0.75)), shell(rect(14.2, 2.2, 2.6, 4.3, S.R * 0.25)),
            kd(rect(8, 9, 8, 2.4)), *dots]


@icon("satellite-phone", CAT, "Chunky rugged handset with a thick fold-up antenna and a small screen.",
      tags=["sat phone", "remote communication", "expedition", "rugged phone", "off grid", "emergency phone", "antenna"])
def _(S):
    ant = rot_pts([(14.2, 1.8), (17.2, 1.8), (17.2, 9), (14.2, 9)], 25, (15.7, 9))
    dots = [dot(x, y, 0.8) for y in (16.4, 19.2) for x in (8.2, 11, 13.8)]
    return [shell(poly(ant, closed=True, r=S.r * 0.6)), shell(rect(4.5, 8.5, 12.5, 13.5, S.R * 0.75)),
            kd(rect(7, 10.8, 7.5, 2.8)), *dots]


@icon("foldable-phone", CAT, "Book-style folding smartphone shown half open with a hinge down the middle.",
      tags=["folding phone", "flip screen", "fold", "bendable display", "flexible screen", "dual screen", "smartphone"])
def _(S):
    body = poly([(2.5, 4), (12, 4), (21.5, 6.2), (21.5, 17.8), (12, 20), (2.5, 20)], closed=True, r=S.r * 0.6)
    return [shell(body), detail(seg(12, 4.5, 12, 19.5)), detail(rect(5, 7, 4, 10)), dot(16.5, 8.5, 0.9)]


@icon("wall-phone", CAT, "Wall-mounted phone with a dial and a handset on its side with a long coiled cord.",
      tags=["wall telephone", "landline", "kitchen phone", "wired phone", "coiled cord", "vintage home phone", "retro"])
def _(S):
    return [shell(rect(2.5, 4, 3.6, 9.5, S.R * 0.5 + 0.6)), shell(rect(8.5, 2.5, 13, 13.5, S.R * 0.75)),
            detail(circle(15, 9.25, 2.6)),
            line("M4.3 13.5Q1.8 15.2 4.3 16.9Q6.8 18.6 4.3 20.3Q2.6 21.4 4.8 21.8")]


@icon("bluetooth-earpiece", CAT, "Single ear-hook earpiece with a short boom microphone.",
      tags=["headset", "hands-free", "wireless earpiece", "ear hook", "mobile accessory", "bluetooth", "mic boom"])
def _(S):
    return [line("M13.5 6.2C9.5 2.4 4.3 5 4.3 10.4C4.3 14 6.3 16.4 9 17.4"),
            shell(rect(12.6, 5.5, 5.6, 10.5, 2.8 if S.name == "rounded" else 1.2)),
            line(seg(15.4, 16, 12.8, 20.6)), dot(12, 21, 1.1)]


@icon("rotary-dial", CAT, "Round dial disc with a ring of finger holes and a curved finger stop.",
      tags=["rotary phone", "old telephone dial", "dialer", "finger wheel", "retro phone", "pulse dial", "vintage"])
def _(S):
    c = (10.5, 12)
    holes = [dot(*polar(*c, 4.6, 100 + 36 * k), 1.15) for k in range(7)]
    return [shell(circle(*c, 7.8)), *holes, line(arc(*c, 10.3, 335, 35))]


@icon("phone-card", CAT, "Prepaid card with a chip on the left and a small telephone handset on the right.",
      tags=["calling card", "prepaid phone card", "sim card", "top up", "phone credit", "smart card", "chip card"])
def _(S):
    return [shell(rect(2.5, 5.5, 19, 13, S.R * 0.75)), kd(rect(5, 9.6, 4.6, 4.8, 1)),
            kd(handset(S, 0.42, 10.2, -6.0))]


@icon("caller-id", CAT, "Telephone handset next to a small id card with a person silhouette.",
      tags=["who is calling", "incoming caller", "contact name", "call display", "identify caller", "phone number lookup"])
def _(S):
    return [shell(handset(S, 0.7, -0.5, 0)), shell(rect(11.5, 2.5, 10.5, 9.5, S.R * 0.5)),
            dot(16.75, 6, 1.3), detail(seg(14.5, 9.4, 19, 9.4))]


@icon("call-transfer", CAT, "Telephone handset with two opposing horizontal arrows above it.",
      tags=["forward call", "redirect call", "switch", "hand off", "transfer", "reroute", "swap"])
def _(S):
    return [shell(handset(S, 0.56, 5.6, 0.3)),
            line(seg(4, 3.8, 19.5, 3.8)), line(poly([(16.5, 1.3), (19.5, 3.8), (16.5, 6.3)], r=S.r * 0.4)),
            line(seg(20, 8.2, 4.5, 8.2)), line(poly([(7.5, 5.7), (4.5, 8.2), (7.5, 10.7)], r=S.r * 0.4))]


@icon("conference-call", CAT, "Telephone handset with three small head figures above it.",
      tags=["group call", "multi party call", "audio conference", "meeting call", "dial in", "team call", "participants"])
def _(S):
    return [shell(handset(S, 0.62, 4.7, 0.2)), dot(6.5, 5.3, 1.7), dot(12, 4.3, 1.9), dot(17.5, 5.3, 1.7)]


@icon("call-merge", CAT, "Two lines converging into one arrow above a telephone handset.",
      tags=["join calls", "combine calls", "three way call", "merge", "link calls", "bridge", "unite"])
def _(S):
    return [shell(handset(S, 0.5, 6.0, 0.9)), line(seg(4.5, 2.6, 12, 6)), line(seg(19.5, 2.6, 12, 6)),
            line(seg(12, 6, 12, 10.2)), line(poly([(9.7, 8.3), (12, 10.6), (14.3, 8.3)], r=S.r * 0.4))]


@icon("hang-up", CAT, "Telephone handset lying horizontally with both ends pointing down.",
      tags=["end call", "disconnect", "decline", "cancel call", "terminate call", "phone down", "reject"])
def _(S):
    if S.name == "line":
        d = "M2.5 17.5V14.5C2.5 10 6.5 8 12 8C17.5 8 21.5 10 21.5 14.5V17.5H16V14.6C13.5 13.2 10.5 13.2 8 14.6V17.5Z"
    else:
        d = ("M2.5 16V14.5C2.5 10 6.5 8 12 8C17.5 8 21.5 10 21.5 14.5V16Q21.5 17.5 20 17.5H17.5Q16 17.5 16 16V14.6"
             "C13.5 13.2 10.5 13.2 8 14.6V16Q8 17.5 6.5 17.5H4Q2.5 17.5 2.5 16Z")
    return [shell(d)]


@icon("call-log", CAT, "Telephone handset beside three short horizontal list lines.",
      tags=["call history", "recent calls", "calls list", "phone records", "dialed numbers", "missed calls", "register"])
def _(S):
    return [shell(handset(S, 0.68, -0.5, 0)), line(seg(14.5, 4.5, 21.5, 4.5)), line(seg(14.5, 8.5, 21.5, 8.5)),
            line(seg(14.5, 12.5, 21.5, 12.5))]


@icon("phone-speed-dial", CAT, "Telephone handset with a small lightning bolt beside it.",
      tags=["quick dial", "favorite number", "shortcut call", "one touch dial", "fast call", "lightning", "hotkey"])
def _(S):
    return [shell(handset(S, 0.7, -0.5, 0)),
            solid(poly([(18, 2.5), (12.8, 9.6), (16.3, 9.6), (15, 15), (20.8, 7.8), (17.3, 7.8)], closed=True, r=S.r * 0.3))]


@icon("call-on-hold", CAT, "Telephone handset with two vertical pause bars beside it.",
      tags=["pause call", "hold music", "wait", "paused call", "standby", "suspend call", "on hold"])
def _(S):
    return [shell(handset(S, 0.7, -0.5, 0)), line(seg(16, 3.5, 16, 11.5)), line(seg(20, 3.5, 20, 11.5))]


@icon("call-waiting", CAT, "Telephone handset with three dots in a row beside it.",
      tags=["second call", "incoming while busy", "please wait", "queue", "ellipsis", "pending call", "waiting"])
def _(S):
    return [shell(handset(S, 0.7, -0.5, 0)), dot(13.6, 5, 1.3), dot(17.4, 5, 1.3), dot(21.2, 5, 1.3)]


@icon("call-recording", CAT, "Telephone handset with a filled record dot inside a ring.",
      tags=["record call", "call capture", "voice log", "recorded line", "audio record", "monitor", "rec"])
def _(S):
    return [shell(handset(S, 0.7, -0.5, 0)), shell(circle(16.8, 7.2, 4.2)), dot(16.8, 7.2, 1.7)]


@icon("emergency-call", CAT, "Telephone handset with a bold medical cross beside it.",
      tags=["sos", "urgent call", "911", "112", "999", "help line", "ambulance", "first aid"])
def _(S):
    cross = [(16, 2.5), (19, 2.5), (19, 6), (22, 6), (22, 9), (19, 9), (19, 12.5), (16, 12.5), (16, 9), (13, 9), (13, 6), (16, 6)]
    return [shell(handset(S, 0.7, -0.5, 0)), solid(poly(cross, closed=True, r=S.r * 0.3))]


@icon("international-call", CAT, "Telephone handset beside a small globe.",
      tags=["overseas call", "long distance", "world call", "global", "roaming", "abroad", "country code"])
def _(S):
    return [shell(handset(S, 0.64, -0.5, 0)), shell(circle(16.2, 7.3, 5.3)),
            detail("M12 7.3H20.4")]


@icon("robocall", CAT, "Telephone handset beside a simple robot head with an antenna.",
      tags=["automated call", "spam call", "ai caller", "recorded message", "telemarketing", "bot call", "auto dialer"])
def _(S):
    return [shell(handset(S, 0.68, -0.5, 0)), shell(rect(12.5, 8, 9, 7, S.R * 0.5)),
            dot(15.4, 11.5, 0.95), dot(18.6, 11.5, 0.95), line(seg(17, 8, 17, 5.3)), dot(17, 4.3, 1.2)]


@icon("phone-tree", CAT, "Telephone handset at the top with lines branching down to three boxes.",
      tags=["ivr", "menu options", "press 1", "call routing", "auto attendant", "branching", "hierarchy"])
def _(S):
    return [solid(handset(S, 0.42, 5.3, -11.3)), line(seg(12, 9.7, 12, 13.3)), line(seg(4.5, 13.3, 19.5, 13.3)),
            line(seg(4.5, 13.3, 4.5, 16.5)), line(seg(19.5, 13.3, 19.5, 16.5)),
            solid(rect(2.5, 16.5, 4, 5, 0.6)), solid(rect(10, 16.5, 4, 5, 0.6)), solid(rect(17.5, 16.5, 4, 5, 0.6))]


@icon("phone-number", CAT, "Telephone handset above a short row of dots and a dash standing for digits.",
      tags=["dial", "digits", "contact number", "mobile number", "landline", "telephone number", "call us"])
def _(S):
    return [shell(handset(S, 0.66, 5.2, -2.5)), dot(3.6, 20, 1.0), dot(6.7, 20, 1.0), dot(9.8, 20, 1.0),
            line(seg(11.4, 20, 12.8, 20)), dot(14.4, 20, 1.0), dot(17.5, 20, 1.0), dot(20.6, 20, 1.0)]


@icon("field-telephone", CAT, "Boxy portable telephone with a hand crank on its side and a handset on top.",
      tags=["military phone", "army telephone", "hand crank phone", "portable phone", "wartime", "vintage field phone", "crank"])
def _(S):
    return [line(poly([(4, 8.5), (4, 4.5), (15, 4.5), (15, 8.5)], r=S.r * 0.8)),
            shell(rect(2.5, 8.5, 15, 13, S.R * 0.6)), detail(seg(3.5, 12, 16.5, 12)), detail(circle(7.6, 16.8, 2)),
            dot(13, 16.8, 1.0), line(poly([(17.5, 17), (21.5, 17), (21.5, 12.5)], r=S.r * 0.6)), dot(21.5, 11.6, 1.2)]


@icon("captioned-telephone", CAT, "Desk phone with a large screen showing text lines beside the handset.",
      tags=["captioned calls", "hard of hearing", "deaf phone", "live captions", "accessible phone", "subtitles"])
def _(S):
    dots = [dot(x, y, 0.85) for y in (16.4, 19.2) for x in (5.6, 8.8, 12)]
    return [line(poly([(3, 12), (3, 8.3), (9.5, 8.3), (9.5, 12)], r=S.r * 0.8)),
            shell(rect(12.3, 2.5, 9.2, 9, S.R * 0.5)), detail(seg(14.6, 5.4, 19.2, 5.4)), detail(seg(14.6, 8.2, 17.6, 8.2)),
            shell(rect(2.5, 13, 19, 8.5, S.R * 0.6)), *dots, detail(seg(15.5, 17.2, 19, 17.2))]


@icon("tty-device", CAT, "Keyboard unit with a small text display and a telephone handset resting on top.",
      tags=["tdd", "text telephone", "deaf communication", "teletypewriter", "typed calls", "relay service", "text phone"])
def _(S):
    dots = [dot(x, y, 0.85) for y in (15.3, 18.6) for x in (6.2, 9.4, 12.6, 15.8, 19)]
    return [line(poly([(4, 6.5), (4, 3.5), (20, 3.5), (20, 6.5)], r=S.r * 0.8)),
            shell(rect(5.5, 7, 13, 4, S.R * 0.3)), kd(rect(7.5, 8.2, 6, 1.6)),
            shell(rect(2.5, 12.5, 19, 9, S.R * 0.6)), *dots]


@icon("video-phone", CAT, "Desk phone with a small screen showing a face above its keypad.",
      tags=["videophone", "picture phone", "face to face call", "video call phone", "screen phone", "desk video"])
def _(S):
    dots = [dot(x, y, 0.85) for y in (16.5, 19.3) for x in (8, 12, 16)]
    return [shell(rect(4, 2, 16, 10, S.R * 0.6)), dot(10.4, 6, 0.9), dot(13.6, 6, 0.9), detail("M9.8 8.6Q12 10.2 14.2 8.6"),
            shell(rect(3, 14, 18, 8, S.R * 0.6)), *dots]


@icon("acoustic-coupler", CAT, "Modem box with two round rubber cups holding a telephone handset on top.",
      tags=["modem", "dial up", "old internet", "retro computing", "data over phone", "bbs", "300 baud"])
def _(S):
    return [line("M6.2 8.3C6.2 2 17.8 2 17.8 8.3"), shell(rect(2.8, 8.3, 6.8, 5.4, 2.4 if S.name == "rounded" else 1.2)),
            shell(rect(14.4, 8.3, 6.8, 5.4, 2.4 if S.name == "rounded" else 1.2)),
            shell(rect(2.5, 15.5, 19, 6, S.R * 0.5)), dot(16.6, 18.5, 0.85), dot(19, 18.5, 0.85), detail(seg(5.5, 18.5, 12, 18.5))]


@icon("video-conference", CAT, "Screen divided into a two by two grid with a head in each cell, on a stand.",
      tags=["video meeting", "team call", "remote meeting", "gallery view", "virtual meeting", "group video"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 15, S.R * 0.6)), detail(seg(12, 3.5, 12, 16.5)), detail(seg(3.5, 10, 20.5, 10)),
            dot(7.2, 6.4, 1.2), dot(16.8, 6.4, 1.2), dot(7.2, 13.6, 1.2), dot(16.8, 13.6, 1.2),
            line(seg(12, 17.5, 12, 21)), line(seg(7.5, 21.3, 16.5, 21.3))]


@icon("webinar", CAT, "Screen showing a presenter at the top and a row of small audience heads below.",
      tags=["online seminar", "virtual lecture", "live presentation", "online class", "training session", "speaker", "audience"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 12.5, S.R * 0.6)), dot(12, 6.4, 1.6),
            detail("M8.6 13A3.4 3 0 0 1 15.4 13"),
            dot(5.5, 19.6, 1.5), dot(10, 19.6, 1.5), dot(14, 19.6, 1.5), dot(18.5, 19.6, 1.5)]


@icon("breakout-rooms", CAT, "Large rectangle split into four rooms with openings, each with a small person dot.",
      tags=["breakout groups", "sub rooms", "small groups", "meeting rooms", "workshop", "split session", "teams"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, S.R * 0.75)),
            detail(seg(12, 3.5, 12, 8.3)), detail(seg(12, 15.7, 12, 20.5)),
            detail(seg(3.5, 12, 8.3, 12)), detail(seg(15.7, 12, 20.5, 12)),
            dot(7.2, 7.2, 1.3), dot(16.8, 7.2, 1.3), dot(7.2, 16.8, 1.3), dot(16.8, 16.8, 1.3)]
