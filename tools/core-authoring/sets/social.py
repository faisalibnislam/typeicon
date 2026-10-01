"""TypeIcon Core: social."""
import math

from dsl import (  # noqa: F401
    LINE, arc, circle, detail, dot, ellipse, filled_region, icon, line, poly, pt_on, rect, regular, seg, shell, solid,
)
from geometry import D, P, ST, U, fmt, polar

CAT = "social"


# --------------------------------------------------------------------------- local helpers

def P2(x, y):
    return f"{fmt(x)} {fmt(y)}"


def star_pts(cx, cy, r_out, r_in=None, n=5):
    r_in = r_out * 0.43 if r_in is None else r_in
    return [polar(cx, cy, r_out if i % 2 == 0 else r_in, -90 + i * 180 / n) for i in range(2 * n)]


def heart_d(cx, cy, s, rounded=False):
    """Heart (the v0.1 design) scaled by s about its centre (12, 13)."""
    base = ("M12 20L4.4 12.6A4.6 4.6 0 0 1 11 6.3L12 7.3L13 6.3A4.6 4.6 0 0 1 19.6 12.6Z" if not rounded else
            "M10.6 18.6L4.4 12.6A4.6 4.6 0 0 1 11 6.3L11.3 6.6Q12 7.3 12.7 6.6L13 6.3A4.6 4.6 0 0 1 19.6 12.6L13.4 18.6Q12 20 10.6 18.6Z")
    import re
    toks = re.findall(r"[MLAQZ]|-?\d*\.?\d+", base)
    out, i, cmd = [], 0, None

    def X(v):
        return fmt(cx + (float(v) - 12) * s)

    def Y(v):
        return fmt(cy + (float(v) - 13) * s)
    while i < len(toks):
        t = toks[i]
        if t in "MLAQZ":
            cmd = t
            out.append(t)
            i += 1
        elif cmd in "ML":
            out.append(f"{X(toks[i])} {Y(toks[i + 1])}")
            i += 2
        elif cmd == "Q":
            out.append(f"{X(toks[i])} {Y(toks[i + 1])} {X(toks[i + 2])} {Y(toks[i + 3])}")
            i += 4
        elif cmd == "A":
            rx, ry, rot, la, sw, x, y = toks[i:i + 7]
            out.append(f"{fmt(float(rx) * s)} {fmt(float(ry) * s)} {rot} {la} {sw} {X(x)} {Y(y)}")
            i += 7
    return "".join(out)


def round_bubble(S, cx, cy, r, a1, a2, tip):
    """Circle bubble with a pointed tail between angles a2 and a1 (arc runs clockwise from a1 to a2)."""
    p1, p2 = polar(cx, cy, r, a1), polar(cx, cy, r, a2)
    sweep = (a2 - a1) % 360
    arc_cmd = f"A{fmt(r)} {fmt(r)} 0 {1 if sweep > 180 else 0} 1 {P2(*p2)}"
    if S.name == "line":
        return f"M{P2(*p1)}{arc_cmd}L{P2(*tip)}Z"
    k = 0.28
    a = (tip[0] + (p2[0] - tip[0]) * k, tip[1] + (p2[1] - tip[1]) * k)
    b = (tip[0] + (p1[0] - tip[0]) * k, tip[1] + (p1[1] - tip[1]) * k)
    return f"M{P2(*p1)}{arc_cmd}L{P2(*a)}Q{P2(*tip)} {P2(*b)}Z"


def msg_circle(S):
    return round_bubble(S, 12.5, 11.5, 8.5, 160, 118, (4, 20))


_CHAT = [(3, 4), (21, 4), (21, 17), (11.5, 17), (7, 21), (7, 17), (3, 17)]


def chat_bubble(S):
    return poly(_CHAT, closed=True, r=S.r * 1.3)


def person(S, hx, hy, hr, x0, x1, top, bottom=21):
    """Head-and-shoulders (matches the v0.1 user icon)."""
    w = x1 - x0
    rr = min(w / 2 - 0.5, 5.5)
    body = (f"M{P2(x0, bottom)}V{fmt(top + rr)}A{fmt(rr)} {fmt(rr)} 0 0 1 {P2(x0 + rr, top)}"
            f"H{fmt(x1 - rr)}A{fmt(rr)} {fmt(rr)} 0 0 1 {P2(x1, top + rr)}V{fmt(bottom)}")
    return [shell(circle(hx, hy, hr)), line(body)]


def knock(draw, glyph):
    """Filled design: the derived Filled of the non-solid parts with a solid glyph knocked out."""
    def f():
        parts = [p for p in draw(LINE) if p.kind != "solid"]
        return D(filled_region(parts), P(glyph))
    return f


def bell_body(cx=12.0, top=4.5, w=6.0, bottom=16.5, flare=1.5):
    return (f"M{P2(cx - w, bottom)}V{fmt(top + w)}A{fmt(w)} {fmt(w)} 0 0 1 {P2(cx + w, top + w)}V{fmt(bottom)}"
            f"L{P2(cx + w + flare, bottom + 2)}H{fmt(cx - w - flare)}Z")


# ============================================================================ reactions

@icon("dislike", CAT, "Heart split by a crack; dislike or unlike.",
      tags=["dislike", "unlike", "broken heart", "unfavourite", "heartbreak", "remove like"],
      aliases=["broken-heart"])
def _(S):
    crack = [(12, 7.3), (10.2, 11), (13.2, 13.5), (11.3, 16.5), (12, 19.5)]
    return [shell(heart_d(12, 13, 1.05, S.name == "rounded")), detail(poly(crack, r=S.r * 0.4))]


@icon("repost", CAT, "Post card with an arrow curving out of it; share someone's post to your feed.",
      tags=["repost", "reshare", "retweet", "boost", "share", "quote post"], aliases=["reshare"])
def _(S):
    return [shell(rect(3, 11, 11.5, 10.5, S.R * 0.75)),
            line("M8.75 8.5A3.5 3.5 0 0 1 12.25 5H19.5"),
            line(poly([(17, 2.5), (19.5, 5), (17, 7.5)], r=S.r * 0.6)),
            detail(seg(6, 14.75, 11.5, 14.75)), detail(seg(6, 18, 9.5, 18))]


@icon("follow", CAT, "Person with a plus sign; follow someone.",
      tags=["follow", "subscribe", "add friend", "connect", "user", "join"])
def _(S):
    return [*person(S, 9, 8.5, 3.5, 2.5, 15.5, 14.5), line(seg(19, 3, 19, 10)), line(seg(15.5, 6.5, 22, 6.5))]


@icon("unfollow", CAT, "Person with a minus sign; unfollow someone.",
      tags=["unfollow", "unsubscribe", "remove friend", "disconnect", "user", "leave"])
def _(S):
    return [*person(S, 9, 8.5, 3.5, 2.5, 15.5, 14.5), line(seg(15.5, 6.5, 22, 6.5))]


def _notif_draw(S):
    body = bell_body(11, 5, 5.75, 16.5, 1.5)
    c, r = (18.25, 5.25), 3
    hide = lambda x, y: math.hypot(x - c[0], y - c[1]) < r + 2.5  # noqa: E731
    vis = _outside(body, hide)
    return [line(vis), line(seg(9, 21, 13, 21)), dot(*c, r)]


def _notif_filled():
    body = bell_body(11, 5, 5.75, 16.5, 1.5)
    c, r = (18.25, 5.25), 3
    solid_bell = U(P(body), ST(body, 2.0))
    clapper = P("M8.75 20.25H13.25A2.25 2.25 0 0 1 8.75 20.25Z")
    return U(D(U(solid_bell, clapper), P(circle(*c, r + 1.75))), P(circle(*c, r)))


def _outside(d, hidden):
    import re  # noqa: F401
    from fontTools.pens.recordingPen import RecordingPen
    from fontTools.svgLib.path import parse_path
    rec = RecordingPen()
    parse_path(d, rec)
    pts, subs = [], []
    for op, args in rec.value:
        if op == "moveTo":
            if pts:
                subs.append(pts)
            pts = [args[0]]
        elif op == "lineTo":
            a, b = pts[-1], args[0]
            n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / 0.2))
            pts += [(a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n) for k in range(1, n + 1)]
        elif op == "curveTo":
            p0 = pts[-1]
            for j in range(0, len(args), 3):
                c1, c2, p3 = args[j:j + 3]
                for k in range(1, 41):
                    t = k / 40
                    mt = 1 - t
                    pts.append((mt ** 3 * p0[0] + 3 * mt * mt * t * c1[0] + 3 * mt * t * t * c2[0] + t ** 3 * p3[0],
                                mt ** 3 * p0[1] + 3 * mt * mt * t * c1[1] + 3 * mt * t * t * c2[1] + t ** 3 * p3[1]))
                p0 = p3
        elif op == "closePath":
            a, b = pts[-1], pts[0]
            n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / 0.2))
            pts += [(a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n) for k in range(1, n + 1)]
            subs.append(pts)
            pts = []
    if pts:
        subs.append(pts)
    out = []
    for sp in subs:
        keep = [not hidden(*p) for p in sp]
        if all(keep):
            out.append("M" + "L".join(P2(*p) for p in sp) + "Z")
            continue
        start = keep.index(False)
        n = len(sp)
        run = []
        for k in range(n):
            i = (start + k) % n
            if keep[i]:
                run.append(sp[i])
            elif run:
                if len(run) > 1:
                    out.append("M" + "L".join(P2(*p) for p in run))
                run = []
        if len(run) > 1:
            out.append("M" + "L".join(P2(*p) for p in run))
    return "".join(out)


@icon("notification-bell", CAT, "Bell with a dot; new notifications.",
      tags=["notifications", "unread", "alert", "new", "bell", "badge"], filled=_notif_filled)
def _(S):
    return _notif_draw(S)


# ============================================================================ opinions

@icon("poll", CAT, "Horizontal result bars of different lengths; a poll and its results.",
      tags=["poll", "vote results", "survey", "options", "question", "results"])
def _(S):
    rr = 0.01 if S.name == "line" else 0.75
    return [line(seg(3, 2.5, 3, 21.5)),
            shell(rect(6.5, 5, 14.5, 1.5, rr)), shell(rect(6.5, 11.25, 8.5, 1.5, rr)), shell(rect(6.5, 17.5, 11.5, 1.5, rr))]


@icon("vote", CAT, "Ballot paper with a check mark going into a ballot box.",
      tags=["vote", "ballot", "election", "ballot box", "poll", "democracy"], aliases=["ballot"])
def _(S):
    return [line(poly([(7, 12), (7, 2.5), (17, 2.5), (17, 12)], r=S.r * 0.6)),
            line(poly([(9.5, 7.5), (11.5, 9.5), (14.5, 5.5)], r=S.r * 0.5)),
            shell(rect(3, 14, 18, 7.5, S.R * 0.5))]


@icon("survey", CAT, "Form page with checked answers; a survey or questionnaire.",
      tags=["survey", "questionnaire", "form", "quiz", "checklist", "research"], aliases=["questionnaire"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 19, S.R * 0.75)),
            detail(poly([(7.5, 8), (9, 9.5), (11.5, 6.5)], r=S.r * 0.4)), detail(seg(13.5, 8, 16.5, 8)),
            detail(poly([(7.5, 15), (9, 16.5), (11.5, 13.5)], r=S.r * 0.4)), detail(seg(13.5, 15, 16.5, 15))]


@icon("feedback", CAT, "Speech bubble with a smiling face; feedback or sentiment.",
      tags=["feedback", "opinion", "sentiment", "satisfaction", "reaction", "comment"])
def _(S):
    return [shell(chat_bubble(S)), dot(9, 8.5, 1.25), dot(15, 8.5, 1.25), detail("M8.5 11.5A3.5 3.5 0 0 0 15.5 11.5")]


def _rating_stars():
    return [star_pts(12, 8.5, 6, 2.6), star_pts(5.25, 16.25, 3.6, 1.6), star_pts(18.75, 16.25, 3.6, 1.6)]


@icon("rating", CAT, "Three stars, the middle one raised; a rating or score.",
      tags=["rating", "stars", "score", "rank", "reviews", "evaluate"], aliases=["stars"])
def _(S):
    big, a, b = _rating_stars()
    return [shell(poly(big, closed=True, r=S.r * 0.2)),
            solid(poly(a, closed=True)), solid(poly(b, closed=True))]


_REVIEW_STAR = star_pts(12, 10.8, 4.6, 2)


def _review_draw(S):
    return [shell(chat_bubble(S)), solid(poly(_REVIEW_STAR, closed=True))]


@icon("review", CAT, "Speech bubble with a star; a written review.",
      tags=["review", "testimonial", "rating", "opinion", "feedback", "comment"],
      filled=knock(_review_draw, poly(_REVIEW_STAR, closed=True)))
def _(S):
    return _review_draw(S)


@icon("trending", CAT, "Flame with an upward arrow; trending or hot right now.",
      tags=["trending", "hot", "popular", "viral", "fire", "top"], aliases=["hot"])
def _(S):
    flame = ("M12 21.5C8 21.5 5 18.8 5 15C5 11 8.5 9 8.5 4.5C11.5 6 13 8.5 13 10.5"
             "C14.3 9.8 15 8.5 15 7C17.5 9 19 12 19 15C19 18.8 16 21.5 12 21.5Z")
    return [shell(flame), detail(seg(12, 19, 12, 13.5)), detail(poly([(9.5, 16), (12, 13.5), (14.5, 16)], r=S.r * 0.5))]


@icon("hashtag-social", CAT, "Round speech bubble with a hash sign; a hashtag or topic.",
      tags=["hashtag", "topic", "tag", "trend", "channel", "social"])
def _(S):
    return [shell(msg_circle(S)),
            detail(seg(11, 7, 10, 16)), detail(seg(15, 7, 14, 16)),
            detail(seg(8, 9.75, 17, 9.75)), detail(seg(8, 13.25, 17, 13.25))]


@icon("share-alt", CAT, "Three connected nodes; share with others.",
      tags=["share", "network", "connect", "send", "distribute", "nodes"], aliases=["share-nodes"])
def _(S):
    a, b, c = (17.5, 5.5), (6, 12), (17.5, 18.5)
    r = 2.75

    def link(p, q):
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = math.hypot(dx, dy)
        k = (r + 1.75) / L
        return seg(p[0] + dx * k, p[1] + dy * k, q[0] - dx * k, q[1] - dy * k)
    return [shell(circle(*a, r)), shell(circle(*b, r)), shell(circle(*c, r)), line(link(b, a)), line(link(b, c))]


_CH_HEART = heart_d(12.5, 12.5, 0.62)


def _comment_heart_draw(S):
    return [shell(msg_circle(S)), solid(heart_d(12.5, 12.5, 0.62, S.name == "rounded"))]


@icon("comment-heart", CAT, "Round speech bubble with a heart; a loving comment or reaction.",
      tags=["comment", "love", "reaction", "like", "reply", "message"],
      filled=knock(_comment_heart_draw, _CH_HEART))
def _(S):
    return _comment_heart_draw(S)


# ============================================================================ content

@icon("live-stream", CAT, "Screen showing a live broadcast signal; streaming live.",
      tags=["live", "livestream", "streaming", "broadcast", "on air", "go live"], aliases=["livestream"])
def _(S):
    return [shell(rect(2, 3.5, 20, 13.5, S.R * 0.75)),
            dot(12, 10.25, 1.6),
            detail(arc(12, 10.25, 4.25, 140, 220)), detail(arc(12, 10.25, 4.25, 320, 40)),
            line(seg(12, 17, 12, 20.5)), line(seg(8, 20.5, 16, 20.5))]


@icon("story", CAT, "Person inside a segmented ring; a social story.",
      tags=["story", "stories", "status update", "moment", "avatar ring", "24 hours"], aliases=["stories"])
def _(S):
    segs = [line(arc(12, 12, 9, a + 9, a + 81)) for a in (-90, 0, 90, 180)]
    return [*segs, shell(circle(12, 9.25, 2.25)), line("M8.25 16.5A3.75 3.75 0 0 1 15.75 16.5")]


@icon("reel", CAT, "Clapper-topped frame with a play button; a short video reel.",
      tags=["reel", "short video", "clip", "shorts", "video", "play"], aliases=["short-video"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)),
            detail(seg(3, 8.5, 21, 8.5)),
            detail(seg(8, 3.5, 10, 8)), detail(seg(13.5, 3.5, 15.5, 8)),
            detail(poly([(10, 11.5), (15.5, 14.75), (10, 18)], closed=True, r=S.r * 0.4))]


# ============================================================================ people

@icon("followers", CAT, "Person with another person behind; your followers.",
      tags=["followers", "audience", "fans", "subscribers", "people", "community"])
def _(S):
    front_head, fr = (9, 9.5), 3.5
    back = [shell(circle(16.5, 7.5, 3))]
    back_body = "M15.5 13H17A5 5 0 0 1 22 18V19.5"
    return [*person(S, *front_head, fr, 2.5, 15.5, 15.5, 21.5)[:1],
            line("M2.5 21.5V21A5.5 5.5 0 0 1 8 15.5H10A5.5 5.5 0 0 1 15.5 21V21.5"),
            *back, line(back_body)]


@icon("verified-badge", CAT, "Scalloped badge with a check mark; a verified account.",
      tags=["verified", "badge", "authentic", "official", "approved", "checkmark"])
def _(S):
    n, rr, bump = 9, 8, 3.2
    pts = [polar(12, 12, rr, -90 + i * 360 / n) for i in range(n)]
    d = f"M{P2(*pts[0])}" + "".join(f"A{bump} {bump} 0 0 1 {P2(*pts[(i + 1) % n])}" for i in range(n)) + "Z"
    return [shell(d), detail(poly([(8.5, 12), (11, 14.5), (15.5, 9.5)], r=S.r * 0.5))]


@icon("influencer", CAT, "Person with a star beside them; an influencer or featured creator.",
      tags=["influencer", "creator", "celebrity", "featured", "star", "popular"], aliases=["creator"])
def _(S):
    return [*person(S, 9, 8.5, 3.5, 2.5, 15.5, 14.5),
            solid(poly(star_pts(18.25, 6.75, 4.75, 2), closed=True))]


@icon("community-group", CAT, "Three people side by side, the centre one in front; a community.",
      tags=["community", "group", "team", "members", "people", "club"], aliases=["community"])
def _(S):
    return [shell(circle(12, 8, 3.25)),
            line("M6 21.5V20A5 5 0 0 1 11 15H13A5 5 0 0 1 18 20V21.5"),
            shell(circle(5, 9.5, 2.25)), shell(circle(19, 9.5, 2.25)),
            line("M2 18.5V17.5A3.5 3.5 0 0 1 5.5 14"), line("M22 18.5V17.5A3.5 3.5 0 0 0 18.5 14")]
