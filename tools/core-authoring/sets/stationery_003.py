"""TypeIcon Core: stationery, batch 003 (presentation, printing, mail, packing and writing-tool curiosities)."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "stationery"
TILT = 45


def rot(pts, deg=TILT, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rp(pts, closed=True, r=0.0, deg=TILT):
    return poly(rot(pts, deg), closed=closed, r=r)


def rrect(x, y, w, h, rx=0.0, deg=TILT):
    """Rotated rounded rectangle (via poly with fillet)."""
    return poly(rot([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], deg), closed=True, r=rx)


def rseg(x1, y1, x2, y2, deg=TILT):
    (a, b), (c, d) = rot([(x1, y1), (x2, y2)], deg)
    return seg(a, b, c, d)


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    return Part("dot", rect(x, y, w, h, rx))


@icon("letterpress-type", CAT, "Metal type block with a raised mirrored letter on its top face",
      tags=["letterpress", "movable type", "printing", "typography", "typeface", "slug", "print shop"])
def _(S):
    return [
        line("M15 12V2.5H11.5A3 3 0 0 0 11.5 8.5H15"),
        shell(rect(5, 12, 14, 9, rr(S, 2))),
        detail(seg(9, 18, 15, 18)),
    ]


@icon("queue-ticket-dispenser", CAT, "Wall dispenser showing a large number with a paper ticket sticking out of its slot",
      tags=["take a number", "ticket", "queue", "waiting line", "turn", "service desk"])
def _(S):
    return [
        shell(rect(5, 2, 14, 14, rr(S, 3))),
        detail(poly([(10, 7), (12.5, 5), (12.5, 11.5)], r=S.r * 0.3)),
        detail(seg(8, 14, 16, 14)),
        line(poly([(9.5, 16), (9.5, 21.5), (14.5, 21.5), (14.5, 16)], r=S.r * 0.4)),
    ]


@icon("collate", CAT, "Three stacked offset pages fanned out in order",
      tags=["collating", "sort pages", "page order", "copy", "stack", "print job", "sets"])
def _(S):
    return [
        line(poly([(7, 12), (3, 12), (3, 2), (13, 2), (13, 6)], r=S.r * 0.5)),
        line(poly([(11, 16), (7, 16), (7, 6), (17, 6), (17, 10)], r=S.r * 0.5)),
        shell(rect(11, 10, 10, 11, rr(S, 2))),
        detail(seg(14, 14, 18, 14)),
        detail(seg(14, 17.5, 18, 17.5)),
    ]


@icon("teleprompter", CAT, "Camera lens behind an angled glass pane that reflects text from a screen below",
      tags=["autocue", "presenter", "script", "broadcast", "video shoot", "speech", "reading aid"])
def _(S):
    return [
        shell(rect(15, 3, 6, 9, rr(S, 2))),
        line(seg(15, 7.5, 11.5, 7.5)),
        line(seg(4, 3, 12, 11)),
        shell(rect(3, 15, 13, 6, rr(S, 2))),
        detail(seg(6, 18, 13, 18)),
    ]


@icon("gavel", CAT, "Wooden mallet with a barrel head beside its round sound block",
      tags=["judge", "court", "auction", "law", "hammer", "verdict", "order"])
def _(S):
    return [
        shell(rrect(6, 3, 12, 6.5, rr(S, 3))),
        shell(rrect(10.5, 9.5, 3, 11, rr(S, 1.5))),
        shell(rect(11.5, 19, 10, 3, rr(S, 1.5))),
    ]


@icon("laser-pointer", CAT, "Slim pen shaped pointer sending a straight beam that ends in a dot",
      tags=["presentation", "pointer", "slides", "beam", "red dot", "lecture", "highlight"])
def _(S):
    return [
        shell(rrect(10, 12, 4, 10, rr(S, 2))),
        line(rseg(12, 9.5, 12, 5)),
        dot(*rot([(12, 1.8)])[0], 1.6),
    ]


@icon("presentation-clicker", CAT, "Small handheld remote with two arrow buttons and a pointer lens at its tip",
      tags=["slide remote", "next slide", "presenter", "wireless clicker", "page turner", "slides"])
def _(S):
    return [
        shell(rect(8, 2, 8, 20, rr(S, 3))),
        dot(12, 5, 1),
        Part("dot", poly([(12, 8.5), (14.2, 11.5), (9.8, 11.5)], closed=True)),
        Part("dot", poly([(9.8, 14.5), (14.2, 14.5), (12, 17.5)], closed=True)),
    ]


@icon("conference-microphone", CAT, "Desk microphone on a round base with a long flexible gooseneck",
      tags=["gooseneck", "meeting", "speech", "podium", "boardroom", "audio", "speaker"])
def _(S):
    return [
        shell(rect(11, 2, 7, 9, rr(S, 3.5))),
        detail(seg(11, 6.5, 18, 6.5)),
        line("M14.5 11C14.5 14 10 14 10 17V19"),
        shell(rect(4, 19, 14, 3, rr(S, 1.5))),
    ]


@icon("roll-up-banner", CAT, "Tall vertical banner on a stand with a cassette base and a top rail",
      tags=["pull up banner", "retractable banner", "trade show", "display stand", "signage", "advertising"])
def _(S):
    return [
        line(poly([(7, 17), (7, 4), (17, 4), (17, 17)])),
        line(seg(5, 2, 19, 2)),
        detail(seg(10, 8, 14, 8)),
        detail(seg(10, 11.5, 14, 11.5)),
        shell(rect(4, 17.5, 16, 4, rr(S, 2))),
    ]


@icon("exhibition-booth", CAT, "Trade show booth with a curved back wall, a header sign and a front counter",
      tags=["trade show", "expo", "stand", "fair", "exhibitor", "convention", "display"])
def _(S):
    return [
        shell(rect(6, 2.5, 12, 4, rr(S, 1.5))),
        line("M4 21V12Q12 7.5 20 12V21"),
        shell(rect(8, 14.5, 8, 6.5, rr(S, 2))),
    ]


@icon("brochure-rack", CAT, "Wall rack with two tiers of pockets holding folded leaflets",
      tags=["leaflet holder", "flyer stand", "pamphlet", "literature rack", "display", "lobby", "tourist info"])
def _(S):
    return [
        line(poly([(7, 7), (7, 2.5), (17, 2.5), (17, 7)], r=S.r * 0.5)),
        shell(rect(4, 7, 16, 4, rr(S, 1.5))),
        line(poly([(7, 18), (7, 13.5), (17, 13.5), (17, 18)], r=S.r * 0.5)),
        shell(rect(4, 18, 16, 4, rr(S, 1.5))),
    ]


@icon("page-orientation", CAT, "Portrait sheet and landscape sheet joined by a curved arrow",
      tags=["portrait", "landscape", "rotate page", "layout", "print setup", "page setup", "paper direction"])
def _(S):
    return [
        shell(rect(3, 2, 8, 11, rr(S, 2))),
        shell(rect(11, 15, 10, 7, rr(S, 2))),
        line(poly([(14, 5), (17, 5), (20, 8), (20, 11)], r=S.r + 1)),
        line(poly([(18, 9.5), (20, 12), (22, 9.5)])),
    ]


@icon("duplex-printing", CAT, "Sheet of paper with a curved arrow wrapping around its edge to the other side",
      tags=["double sided", "two sided", "print both sides", "flip", "back to back", "printer settings", "2 sided"])
def _(S):
    return [
        shell(rect(3, 3, 11, 16, rr(S, 2))),
        detail(seg(6.5, 8, 10.5, 8)),
        detail(seg(6.5, 12, 10.5, 12)),
        line(poly([(17, 5), (20, 5), (20, 19), (17, 19)], r=S.r + 1.5)),
        line(poly([(19, 16.5), (16.5, 19), (19, 21.5)])),
    ]


@icon("paper-sizes", CAT, "Three nested sheets of shrinking size sharing their bottom left corner",
      tags=["a4", "a3", "a5", "paper format", "page size", "letter size", "print dimensions"])
def _(S):
    return [
        shell(rect(3, 3, 17, 18, rr(S, 2))),
        detail(poly([(3, 9), (13.5, 9), (13.5, 21)], r=S.r)),
        detail(poly([(3, 15), (8, 15), (8, 21)], r=S.r * 0.6)),
    ]


@icon("pages-per-sheet", CAT, "Single sheet divided into four small page thumbnails with text lines",
      tags=["n-up", "multiple pages per sheet", "thumbnails", "handout", "print layout", "save paper", "4 up"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        detail(seg(12, 3, 12, 21)),
        detail(seg(3, 12, 21, 12)),
        Part("dot", rect(5.5, 6.5, 4, 1.5)),
        Part("dot", rect(14.5, 6.5, 4, 1.5)),
        Part("dot", rect(5.5, 15.5, 4, 1.5)),
        Part("dot", rect(14.5, 15.5, 4, 1.5)),
    ]


@icon("ink-level", CAT, "Three printer ink tanks side by side, each filled to a different height",
      tags=["ink cartridge", "toner level", "printer ink", "low ink", "supplies", "refill", "ink status"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        detail(seg(9, 3, 9, 21)),
        detail(seg(15, 3, 15, 21)),
        Part("dot", rect(5.5, 8, 2, 11)),
        Part("dot", rect(11, 12, 2, 7)),
        Part("dot", rect(17, 15.5, 2, 3.5)),
    ]


@icon("collection-mailbox", CAT, "Street mailbox with a rounded top, a pull down flap handle and short legs",
      tags=["post box", "drop box", "mail drop", "street mailbox", "send letters", "postal", "collection box"])
def _(S):
    rb = 0 if S.name == "line" else 2
    body = "M5 17V9A7 7 0 0 1 19 9V17Z" if rb == 0 else "M5 15V9A7 7 0 0 1 19 9V15A2 2 0 0 1 17 17H7A2 2 0 0 1 5 15Z"
    return [
        shell(body),
        detail(seg(8.5, 9, 15.5, 9)),
        dot(12, 13.2, 1.2),
        line(seg(7.5, 17, 7.5, 22)),
        line(seg(16.5, 17, 16.5, 22)),
    ]


@icon("pillar-postbox", CAT, "Cylindrical freestanding post box with a domed cap and a horizontal letter slot",
      tags=["pillar box", "post box", "red postbox", "mail slot", "postal", "uk mail"])
def _(S):
    return [
        shell("M8 21V10H6.5A5.5 5.5 0 0 1 17.5 10H16V21Z"),
        detail(seg(10, 14.5, 14, 14.5)),
    ]


@icon("wall-mounted-letterbox", CAT, "Box fixed to a wall with a sloping hinged lid over the slot and a small lock",
      tags=["letterbox", "mail box", "wall box", "mailbox", "post box", "front door", "letter slot", "lockable"])
def _(S):
    return [
        shell(poly([(3, 20), (3, 9), (6, 3.5), (18, 3.5), (21, 9), (21, 20)], closed=True, r=S.r)),
        detail(seg(7, 9, 17, 9)),
        dot(12, 15, 1.4),
    ]


@icon("letter-rack", CAT, "Desk rack with upright ends holding envelopes on edge",
      tags=["mail sorter", "desk organizer", "envelope holder", "correspondence", "inbox tray", "office", "letters"])
def _(S):
    return [
        line(poly([(3, 8), (3, 20.5), (21, 20.5), (21, 8)], r=S.r)),
        line(seg(8, 4, 16, 4)),
        shell(rect(6, 7, 12, 10, rr(S, 2))),
        detail(poly([(6, 7), (12, 12.5), (18, 7)])),
    ]


@icon("telephone-switchboard", CAT, "Panel with rows of jacks and patch cords plugged in",
      tags=["operator", "patch panel", "manual exchange", "retro phone", "call routing", "cord board", "vintage telephone"])
def _(S):
    return [
        shell(rect(3, 3, 18, 13, rr(S, 2))),
        dot(7.5, 7, 1.2), dot(12, 7, 1.2), dot(16.5, 7, 1.2),
        dot(7.5, 12, 1.2), dot(12, 12, 1.2), dot(16.5, 12, 1.2),
        line(poly([(7.5, 16), (7.5, 21), (12, 21), (12, 16)], r=S.r + 1)),
        line(seg(16.5, 16, 16.5, 21)),
    ]


@icon("dictation-recorder", CAT, "Slim handheld recorder with a speaker grille, a small screen and a slide switch on its side",
      tags=["voice recorder", "dictaphone", "audio notes", "memo", "transcription", "interview", "handheld recorder"])
def _(S):
    return [
        shell(rect(6, 2, 10, 20, rr(S, 3))),
        detail(seg(9.5, 5.5, 12.5, 5.5)),
        detail(rect(9, 8.5, 4, 4)),
        dot(11, 18, 1.4),
        line(seg(19.5, 8, 19.5, 13)),
    ]


@icon("conveyor-belt", CAT, "Belt running over rollers on two legs with two boxes riding on top",
      tags=["assembly line", "production line", "factory", "warehouse", "packing line", "logistics", "automation"])
def _(S):
    return [
        shell(rect(3, 4, 7, 7, rr(S, 1.5))),
        shell(rect(14, 7, 6, 4, rr(S, 1.5))),
        shell(rect(2, 13, 20, 6, 3)),
        dot(6, 16, 1.2), dot(12, 16, 1.2), dot(18, 16, 1.2),
        line(seg(6, 19, 6, 22)),
        line(seg(18, 19, 18, 22)),
    ]


@icon("strapped-box", CAT, "Closed box seen from the corner with two strapping bands, each joined by a small seal clip",
      tags=["packaging", "banded box", "pallet", "shipping", "strapping", "secured parcel", "freight"])
def _(S):
    return [
        shell(poly([(3, 9), (8, 4), (21, 4), (21, 16), (16, 21), (3, 21)], closed=True, r=S.r)),
        detail(poly([(3, 9), (16, 9), (21, 4)])),
        detail(seg(16, 9, 16, 21)),
        detail(poly([(7, 21), (7, 9), (12, 4)])),
        Part("dot", rect(5.5, 13.5, 3, 3.5)),
    ]


@icon("air-pillows", CAT, "Row of three connected inflated plastic cushions joined at pinched, perforated seams",
      tags=["bubble packaging", "void fill", "inflatable cushion", "protective packaging", "shipping", "air cushion", "packing"])
def _(S):
    n = 2.5 if S.name == "line" else 1.8  # seam pinch depth
    t, b = 6 + n, 18 - n
    path = (f"M2 12Q2 6 5.3 6Q8.5 6 8.7 {fmt(t)}Q9 6 12 6Q15 6 15.3 {fmt(t)}Q15.5 6 18.7 6Q22 6 22 12"
            f"Q22 18 18.7 18Q15.5 18 15.3 {fmt(b)}Q15 18 12 18Q9 18 8.7 {fmt(b)}Q8.5 18 5.3 18Q2 18 2 12Z")
    return [
        shell(path),
        detail(seg(8.7, 11, 8.7, 13)),
        detail(seg(15.3, 11, 15.3, 13)),
    ]


def _pie(S, cx, cy, sx, sy, r):
    """Quarter disc in the quadrant (sx, sy) of the centre, inset from the cross by 1."""
    pts = [(cx + sx * 1, cy + sy * 1)]
    a0 = math.degrees(math.asin(1 / r))
    for i in range(6):
        a = a0 + (90 - 2 * a0) * i / 5
        pts.append((cx + sx * r * math.sin(math.radians(a)), cy + sy * r * math.cos(math.radians(a))))
    return pts


@icon("center-of-gravity-mark", CAT, "Circle divided into four quarters with two opposite quarters solid, the handling mark for center of gravity",
      tags=["centre of gravity", "balance point", "handling symbol", "cargo marking", "lifting", "packaging symbol", "freight mark"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(seg(12, 3, 12, 21)),
        detail(seg(3, 12, 21, 12)),
        Part("dot", poly(_pie(S, 12, 12, 1, -1, 7.6), closed=True, r=S.r * 0.5)),
        Part("dot", poly(_pie(S, 12, 12, -1, 1, 7.6), closed=True, r=S.r * 0.5)),
    ]


@icon("shredded-paper", CAT, "Loose pile of thin vertical paper strips curling at their ends",
      tags=["paper shredder", "confidential", "destroy documents", "waste paper", "strips", "recycling", "cut paper"])
def _(S):
    return [
        line("M5 3V15Q5 19 2.8 20"),
        line("M9.7 5V17Q9.7 20 12.2 21"),
        line("M14.3 3V16Q14.3 19.5 17 20.5"),
        line("M19 5V15Q19 19 21 20"),
    ]


@icon("brush-pen", CAT, "Slim pen with a long pointed brush tip",
      tags=["calligraphy pen", "ink brush", "lettering", "drawing", "manga", "illustration", "art supplies"])
def _(S):
    tip = [(10.2, 9), (10.3, 6.5), (11.2, 4.2), (12, 1.8), (12.8, 4.2), (13.7, 6.5), (13.8, 9)]
    return [
        shell(rp(tip, closed=True, r=S.r * 0.4)),
        shell(rrect(9.5, 9.5, 5, 12, rr(S, 2))),
        detail(rseg(9.5, 13, 14.5, 13)),
    ]


@icon("isometric-paper", CAT, "Sheet of paper printed with isometric axes, one upright line and two lines at thirty degrees",
      tags=["isometric grid", "triangle grid", "drafting paper", "3d drawing", "technical drawing", "engineering paper", "graph paper"])
def _(S):
    return [
        shell(rect(4, 2, 16, 20, rr(S, 2))),
        detail(seg(12, 6, 12, 18)),
        detail(seg(6.8, 9, 17.2, 15)),
        detail(seg(6.8, 15, 17.2, 9)),
    ]


@icon("carbon-paper", CAT, "Sheet of paper with its corner peeled back to show a dark carbon layer beneath",
      tags=["carbon copy", "duplicate", "copy sheet", "triplicate", "receipt book", "transfer paper", "cc"])
def _(S):
    return [
        shell(poly([(4, 2), (20, 2), (20, 13), (13, 20), (4, 20)], closed=True, r=S.r * 0.6)),
        detail(poly([(20, 13), (13, 13), (13, 20)])),
        detail(seg(7.5, 7, 15, 7)),
        solid(poly([(21.5, 14.5), (21.5, 21.5), (14.5, 21.5)], closed=True)),
    ]


@icon("electric-pencil-sharpener", CAT, "Desktop pencil sharpener with a round pencil hole, a shavings drawer and a power button",
      tags=["pencil sharpener", "electric sharpener", "classroom", "desk", "shavings", "office supplies", "motorized"])
def _(S):
    return [
        shell(rect(3, 4, 18, 17, rr(S, 3))),
        detail(circle(10.5, 9.5, 2.8)),
        dot(17.5, 9.5, 1.3),
        detail(seg(3, 15.5, 21, 15.5)),
        detail(seg(10, 18.5, 14, 18.5)),
    ]


@icon("typewriter-ribbon", CAT, "Two spools joined by a band of ink ribbon stretched between them",
      tags=["ink ribbon", "typewriter", "spool", "reel", "vintage", "printer ribbon", "typing"])
def _(S):
    return [
        shell(circle(6, 12, 4)),
        shell(circle(18, 12, 4)),
        dot(6, 12, 1.3) if S.name == "rounded" else Part("dot", rect(4.8, 10.8, 2.4, 2.4)),
        dot(18, 12, 1.3) if S.name == "rounded" else Part("dot", rect(16.8, 10.8, 2.4, 2.4)),
        line(seg(6, 8, 18, 8)),
        line(seg(6, 16, 18, 16)),
    ]


@icon("av-cart", CAT, "Rolling cart with two shelves on casters and a projector on the top shelf",
      tags=["projector cart", "media cart", "audiovisual", "classroom", "trolley", "equipment", "presentation"])
def _(S):
    return [
        shell(rect(6, 5, 12, 6, rr(S, 2))),
        dot(14.5, 8, 1.2),
        line(seg(3, 12.5, 21, 12.5)),
        line(seg(4.5, 17.5, 19.5, 17.5)),
        line(seg(4.5, 12.5, 4.5, 20)),
        line(seg(19.5, 12.5, 19.5, 20)),
        dot(4.5, 21, 1.1),
        dot(19.5, 21, 1.1),
    ]


@icon("telescopic-pointer", CAT, "Long extendable pointer made of joined segments with a small ball at its tip",
      tags=["teacher pointer", "pointing stick", "extendable wand", "lecture", "classroom", "presenter", "baton"])
def _(S):
    return [
        shell(rrect(10, 13, 4, 9, rr(S, 2))),
        line(rseg(12, 13, 12, 4)),
        line(rseg(10.5, 9, 13.5, 9)),
        dot(*rot([(12, 2)])[0], 1.7),
    ]


@icon("one-on-one-meeting", CAT, "Two chairs facing each other across a small round table",
      tags=["one to one", "1:1", "interview", "chat", "catch up", "coaching", "private meeting", "discussion"])
def _(S):
    return [
        line(seg(3.5, 4, 3.5, 12)),
        shell(rect(3.5, 12, 5, 3, rr(S, 1.5))),
        line(seg(4.5, 15, 4.5, 20.5)),
        line(seg(8, 15, 8, 20.5)),
        line(seg(20.5, 4, 20.5, 12)),
        shell(rect(15.5, 12, 5, 3, rr(S, 1.5))),
        line(seg(19.5, 15, 19.5, 20.5)),
        line(seg(16, 15, 16, 20.5)),
        shell(rect(10.5, 11, 3, 1.5, 0.75)),
        line(seg(12, 12.5, 12, 20.5)),
    ]


@icon("greeting-card", CAT, "Folded card standing partly open with a small flower on its front panel",
      tags=["card", "birthday card", "congratulations", "wishes", "occasion", "stationery", "send love"])
def _(S):
    return [
        shell(rect(4, 3, 11, 18, rr(S, 2))),
        line(poly([(15, 6), (20, 4.5), (20, 18.5), (15, 20)], r=S.r * 0.5)),
        dot(9.5, 8.2, 1.4), dot(9.5, 11.8, 1.4), dot(7.7, 10, 1.4), dot(11.3, 10, 1.4),
        detail(seg(9.5, 13.5, 9.5, 17.5)),
    ]


@icon("rubber-stamp-rack", CAT, "Rotating tray holding three upright rubber stamps",
      tags=["stamp holder", "stamp stand", "office stamps", "carousel", "rubber stamps", "desk organizer", "stamp organizer"])
def _(S):
    out = []
    for x in (5, 12, 19):
        out.append(line(seg(x, 3.5, x, 9)))
        out.append(shell(rect(x - 2, 9, 4, 5, rr(S, 1.2))))
    out.append(line(ellipse(12, 19, 9.5, 2.5)) if S.name == "rounded" else
               line(poly([(2.5, 19), (5, 16.5), (19, 16.5), (21.5, 19), (19, 21.5), (5, 21.5)], closed=True)))
    return out


@icon("paperclip-chain", CAT, "Chain of four linked paperclip loops hanging in a gentle curve",
      tags=["clips", "linked clips", "office supplies", "connected", "chain", "attach", "binder clips"])
def _(S):
    ys = (7.5, 11.5, 11.5, 7.5)
    return [line(rect(2 + 4.5 * i, y, 6.5, 5, 1.5 if S.name == "line" else 2.5)) for i, y in enumerate(ys)]


@icon("rolling-file-cart", CAT, "Open wheeled frame cart with hanging file folders standing inside it",
      tags=["file trolley", "hanging files", "mobile filing", "records cart", "office", "folders", "document cart"])
def _(S):
    return [
        line(poly([(3, 6), (3, 17.5), (21, 17.5), (21, 6)], r=S.r)),
        line(poly([(8, 15), (8, 6), (10.5, 6)], r=S.r * 0.4)),
        line(poly([(13, 15), (13, 6), (15.5, 6)], r=S.r * 0.4)),
        line(poly([(18, 15), (18, 6), (20.5, 6)], r=S.r * 0.4)),
        dot(6, 20.8, 1.2),
        dot(18, 20.8, 1.2),
    ]


@icon("archive-shelving", CAT, "Tall shelving unit with archive boxes sitting on three shelves",
      tags=["records storage", "filing", "warehouse shelf", "storage boxes", "document archive", "rack", "stockroom"])
def _(S):
    out = [shell(rect(3, 2.5, 18, 19, rr(S, 4))), detail(seg(3, 8.5, 21, 8.5)), detail(seg(3, 15, 21, 15))]
    for top in (4, 10.5, 16.5):
        out.append(Part("dot", rect(5.5, top, 5, 3.5)))
        out.append(Part("dot", rect(13.5, top, 5, 3.5)))
    return out


@icon("plan-chest", CAT, "Wide low cabinet with a stack of shallow drawers for storing large drawings",
      tags=["flat file", "blueprint storage", "map drawers", "architect", "drawing cabinet", "document drawers", "filing cabinet"])
def _(S):
    return [
        shell(rect(2, 4, 20, 17, rr(S, 4))),
        detail(seg(2, 9.7, 22, 9.7)),
        detail(seg(2, 15.3, 22, 15.3)),
        Part("dot", rect(9.5, 6.5, 5, 1.4)),
        Part("dot", rect(9.5, 12.2, 5, 1.4)),
        Part("dot", rect(9.5, 17.8, 5, 1.4)),
    ]


@icon("pencil-extender", CAT, "Metal tube holder gripping a short pencil stub with a sliding ring",
      tags=["pencil holder", "stub holder", "lengthener", "pencil saver", "drafting", "art supplies", "short pencil"])
def _(S):
    return [
        shell(rp([(10, 13), (10, 7), (12, 3), (14, 7), (14, 13)], r=S.r * 0.4)),
        shell(rrect(9, 12, 6, 10, rr(S, 1.5))),
        detail(rseg(9, 16, 15, 16)),
    ]


@icon("dot-matrix-printer", CAT, "Wide low printer with sprocket edged fan fold paper feeding up through its top",
      tags=["impact printer", "tractor feed", "continuous paper", "retro printer", "invoice printer", "legacy", "line printer"])
def _(S):
    return [
        line(poly([(5.5, 12), (5.5, 3), (18.5, 3), (18.5, 12)], r=S.r * 0.5)),
        dot(8.2, 6, 0.8), dot(8.2, 9, 0.8), dot(15.8, 6, 0.8), dot(15.8, 9, 0.8),
        shell(rect(2, 12, 20, 9, rr(S, 2))),
        detail(seg(7, 16.5, 17, 16.5)),
    ]


@icon("answering-machine", CAT, "Desk unit with a tape window, a speaker grille and a row of play buttons",
      tags=["voicemail", "message recorder", "telephone", "retro", "tape", "landline", "leave a message"])
def _(S):
    return [
        shell(rect(2, 6, 20, 15, rr(S, 3))),
        detail(rect(5, 9, 7, 4, rr(S, 1.5))),
        dot(16, 10, 1), dot(19, 10, 1), dot(16, 13, 1), dot(19, 13, 1),
        dot(5.5, 17.5, 1.2), dot(9, 17.5, 1.2), dot(12.5, 17.5, 1.2),
    ]


@icon("corrugated-cardboard", CAT, "Cross section of cardboard with a fluted layer between two flat liners",
      tags=["cardboard", "packaging material", "flute", "box material", "carton", "recycling", "layers"])
def _(S):
    if S.name == "line":
        wave = poly([(3, 12), (6, 8.5), (9, 15.5), (12, 8.5), (15, 15.5), (18, 8.5), (21, 12)], r=0)
    else:
        wave = "M3 12Q4.5 6 7.5 12T13.5 12T19.5 12L21 12"
    return [
        line(seg(3, 5, 21, 5)),
        line(seg(3, 19, 21, 19)),
        line(wave),
    ]


@icon("kraft-paper-dispenser", CAT, "Paper roll on a floor stand with a sheet pulled down to a cutting bar",
      tags=["wrapping paper", "packing paper", "paper roll", "shipping station", "packing bench", "roll holder", "gift wrap"])
def _(S):
    return [
        shell(circle(11, 7, 5.5)) if S.name == "rounded" else shell(poly(regular(11, 7, 5.8, 8, -22.5), closed=True)),
        dot(11, 7, 1.3),
        line(seg(11, 12.5, 11, 21)),
        line(seg(5.5, 21, 16.5, 21)),
        line(seg(16.5, 7, 16.5, 16)),
        line(seg(14, 17, 21, 17)),
    ]


@icon("copy-holder", CAT, "Upright stand holding a sheet of paper with a horizontal line guide bar across it",
      tags=["document holder", "typist", "data entry", "reading guide", "desk stand", "copy stand", "paper easel"])
def _(S):
    return [
        shell(rect(6, 2, 12, 15, rr(S, 2))),
        detail(seg(9, 5.5, 15, 5.5)),
        detail(seg(9, 8.5, 15, 8.5)),
        line(seg(3.5, 12, 20.5, 12)),
        line(seg(12, 17, 12, 21)),
        line(seg(7.5, 21, 16.5, 21)),
    ]


@icon("desk-footrest", CAT, "Angled platform with a textured top resting on a curved rocking base",
      tags=["foot rest", "ergonomic", "under desk", "rocker", "office comfort", "posture", "foot stool"])
def _(S):
    dots = rot([(7.5, 10), (12, 10), (16.5, 10)], -14)
    return [
        shell(rrect(3, 7, 18, 6, rr(S, 2), deg=-14)),
        dot(*dots[0], 0.9), dot(*dots[1], 0.9), dot(*dots[2], 0.9),
        line("M5 16Q12 24 19 16"),
    ]


@icon("chair-mat", CAT, "Top view of a floor mat with a tongue shaped lip and an office chair base on it",
      tags=["floor protector", "desk chair mat", "carpet protector", "office floor", "casters", "workspace", "rolling chair"])
def _(S):
    spokes = []
    for i in range(5):
        a = -90 + 72 * i
        x, y = polar(12, 9, 3.4, a)
        spokes.append(detail(seg(12, 9, x, y)))
        spokes.append(dot(x, y, 1.0))
    return [
        shell(poly([(3, 3), (21, 3), (21, 14), (16, 14), (16, 21), (8, 21), (8, 14), (3, 14)], closed=True, r=S.r)),
        *spokes,
    ]


@icon("in-out-board", CAT, "Wall board with rows of name lines and two columns where round magnets show who is in or out",
      tags=["attendance board", "whereabouts", "staff board", "office status", "magnet board", "who is in", "sign out"])
def _(S):
    return [
        shell(rect(3, 2, 18, 20, rr(S, 2))),
        detail(seg(5.5, 6.5, 11, 6.5)),
        detail(seg(5.5, 12, 11, 12)),
        detail(seg(5.5, 17.5, 11, 17.5)),
        dot(14.5, 6.5, 1.4),
        dot(18, 12, 1.4),
        dot(14.5, 17.5, 1.4),
    ]


@icon("inkstone", CAT, "Rectangular stone slab with a round well of ink and an ink stick lying beside it",
      tags=["ink slab", "calligraphy", "sumi", "chinese writing", "ink grinding", "brush painting", "scholar tools"])
def _(S):
    stick = poly(rot([(12.5, 10.5), (20, 10.5), (20, 13.5), (12.5, 13.5)], -20, 16.2, 12), closed=True)
    return [
        shell(rect(2, 5, 20, 16, rr(S, 3))),
        detail(ellipse(8.5, 14, 3.5, 3)),
        detail(stick),
    ]


@icon("calligraphy-brush", CAT, "Brush with a bamboo handle, a hanging loop at the top and a tapered hair tip",
      tags=["chinese brush", "ink brush", "sumi brush", "painting", "lettering", "writing brush", "handwriting"])
def _(S):
    return [
        shell(circle(12, 3.8, 1.8)) if S.name == "rounded" else shell(rect(10.2, 2, 3.6, 3.6)),
        line(seg(12, 5.6, 12, 7)),
        shell(rect(10, 7, 4, 8, rr(S, 1.5))),
        detail(seg(10, 10, 14, 10)),
        shell(poly([(9.5, 15), (14.5, 15), (14.5, 17), (12, 22), (9.5, 17)], closed=True, r=S.r * 0.4)),
    ]


@icon("chop-seal", CAT, "Small upright seal stamp beside its square printed impression",
      tags=["name seal", "hanko", "stamp", "signature stamp", "red seal", "asian seal", "signet"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 5, 8, rr(S, 2))),
        shell(rect(2.5, 10.5, 9, 5, rr(S, 1.5))),
        shell(rect(14, 12.5, 8, 8, rr(S, 1.5))),
        dot(18, 16.5, 1.4) if S.name == "rounded" else Part("dot", rect(16.6, 15.1, 2.8, 2.8)),
    ]


@icon("reed-pen", CAT, "Cut reed stem with an angled chisel tip and a small slit at the point",
      tags=["quill", "bamboo pen", "calligraphy pen", "dip pen", "ancient writing", "scribe", "ink pen"])
def _(S):
    return [
        shell(rp([(9.5, 21), (9.5, 8.5), (14.5, 3.5), (14.5, 21)], r=S.r * 0.5)),
        detail(rseg(12, 6, 12, 12)),
        detail(rseg(9.5, 17, 14.5, 17)),
    ]


@icon("wax-tablet", CAT, "Two hinged tablets opened like a book with scratched lines and a pointed stylus below",
      tags=["writing tablet", "ancient", "roman", "stylus", "diptych", "history", "scratch writing"])
def _(S):
    return [
        shell(rect(2, 3, 20, 14, rr(S, 2))),
        detail(seg(12, 3, 12, 17)),
        detail(seg(5, 7, 9, 7)), detail(seg(5, 11, 8, 11)),
        detail(seg(15, 7, 19, 7)), detail(seg(15, 11, 18, 11)),
        line(seg(3.5, 20.5, 16.5, 20.5)),
        solid(poly([(16, 19.5), (21.5, 20.5), (16, 21.5)], closed=True)),
    ]


@icon("stamp-album", CAT, "Open album with postage stamps mounted on both pages",
      tags=["philately", "stamp collecting", "collection", "postage stamps", "hobby", "collector", "stock book"])
def _(S):
    return [
        shell(rect(2, 4, 20, 16, rr(S, 4))),
        detail(seg(12, 4, 12, 20)),
        Part("dot", rect(5, 7, 4.5, 4)), Part("dot", rect(5, 13, 4.5, 4)),
        Part("dot", rect(14.5, 7, 4.5, 4)), Part("dot", rect(14.5, 13, 4.5, 4)),
    ]


@icon("registration-mark", CAT, "Circle with a crosshair whose lines extend past its edge, the printer registration target",
      tags=["crosshair", "print alignment", "crop marks", "prepress", "target", "color registration", "press check"])
def _(S):
    return [
        line(circle(12, 12, 5.5)),
        line(seg(12, 2.5, 12, 21.5)),
        line(seg(2.5, 12, 21.5, 12)),
        dot(12, 12, 1.3),
    ]


@icon("ink-brayer", CAT, "Small rubber roller on a frame with a handle, resting over a patch of ink",
      tags=["roller", "printmaking", "linocut", "relief printing", "ink roller", "block printing", "studio"])
def _(S):
    return [
        line(poly([(3, 15), (3, 8), (21, 8), (21, 15)], r=S.r)),
        line(seg(12, 8, 12, 3)),
        shell(rect(4, 11.5, 16, 6, 3)),
        solid(rect(4, 20, 16, 2)),
    ]


@icon("badge-reel", CAT, "Round retractable reel with its cord pulled out to a card clip below",
      tags=["id badge", "lanyard", "retractable", "name tag holder", "yo-yo", "access card", "clip"])
def _(S):
    return [
        shell(circle(12, 9, 6.5)),
        dot(12, 9, 1.8) if S.name == "rounded" else Part("dot", rect(10.2, 7.2, 3.6, 3.6)),
        line(seg(12, 15.5, 12, 17.5)),
        shell(rect(7.5, 17.5, 9, 4.5, rr(S, 3))),
    ]
