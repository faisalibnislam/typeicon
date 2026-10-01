"""TypeIcon Core: privacy 002 (surveillance, locks and keys, physical security, forensics, identity documents)."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "privacy"


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def star(cx, cy, ro, ri, n=5):
    pts = []
    for i in range(n * 2):
        a = -90 + i * 180 / n
        pts.append(polar(cx, cy, ro if i % 2 == 0 else ri, a))
    return pts


def head_shoulders(cx, cy, hr=3.0, w=6.5):
    """Head circle centre (cx, cy) and shoulders arc path below it."""
    return circle(cx, cy, hr), f"M{fmt(cx - w)} {fmt(cy + hr + 7)}V{fmt(cy + hr + 5)}a{fmt(w)} {fmt(w * 0.8)} 0 0 1 {fmt(2 * w)} 0V{fmt(cy + hr + 7)}"


# ============================================================================ seals and marks

@icon("security-hologram", CAT, "Oval holographic sticker with a small star and diagonal shimmer lines",
      tags=["hologram", "authenticity", "sticker", "anti-counterfeit", "genuine", "security label"])
def _(S):
    return [
        shell(ellipse(12, 12, 9.5, 7.5)),
        Part("dot", poly(star(8.5, 10.5, 3.2, 1.4), closed=True)),
        detail(seg(13.5, 16.5, 17.5, 9)),
        detail(seg(16.5, 16, 19, 11.5)),
    ]


@icon("document-watermark", CAT, "Document page with a faint emblem circle and a line of text",
      tags=["watermark", "document", "authentic", "paper", "stamp", "confidential", "draft"])
def _(S):
    return [
        shell(poly([(5, 2.5), (14, 2.5), (19, 7.5), (19, 21.5), (5, 21.5)], closed=True, r=S.r)),
        detail("M14 2.5V7.5H19"),
        detail(arc(12, 14.5, 3.8, 30, 150)),
        detail(arc(12, 14.5, 3.8, 210, 330)),
        detail(seg(8.5, 7, 11, 7)),
    ]


@icon("tamper-seal", CAT, "Box with a tape strip across its lid seam showing a void mark",
      tags=["tamper evident", "seal", "void", "sticker", "package", "sealed", "tape"])
def _(S):
    return [
        shell(poly([(3, 6), (21, 6), (21, 12), (17, 18), (3, 18)], closed=True, r=S.r)),
        detail(poly([(21, 12), (17, 12), (17, 18)])),
        sq(6, 10.5, 3, 3),
        sq(11, 10.5, 3, 3),
    ]


@icon("pull-tight-seal", CAT, "Plastic security seal with a loop tail locked into a flat tag",
      tags=["cable tie", "security seal", "tag", "container seal", "freight", "tamper"])
def _(S):
    return [
        shell(rect(6, 2.5, 12, 7, rr(S, 3))),
        detail(seg(9, 5, 15, 5)),
        detail(seg(9, 7.3, 12.5, 7.3)),
        line(arc(12, 16, 5.5, -65, 245)),
    ]


@icon("chained-briefcase", CAT, "Briefcase with a chain running from the handle to a cuff ring",
      tags=["briefcase", "courier", "secure transport", "chained", "handcuff", "diplomatic case"])
def _(S):
    return [
        shell(rect(2.5, 9, 14, 11.5, rr(S, 2))),
        line(poly([(6.5, 9), (6.5, 6), (12.5, 6), (12.5, 9)], r=S.r)),
        detail(seg(2.5, 14, 16.5, 14)),
        line(seg(12.5, 7, 16, 5.5)),
        shell(circle(19, 5.5, 2.5)),
    ]


# ============================================================================ surveillance cameras

@icon("dome-camera", CAT, "Ceiling dome camera with a flat mount and a lens inside the dome",
      tags=["cctv", "surveillance", "security camera", "ceiling", "dome", "monitoring"])
def _(S):
    return [
        shell(poly([(3, 3), (21, 3), (21, 6.5), (3, 6.5)], closed=True, r=S.r)),
        shell("M4.5 6.5a7.5 7.5 0 0 0 15 0Z"),
        dot(12, 10.5, 2),
    ]


@icon("ptz-camera", CAT, "Pan tilt zoom camera ball hanging from a wall arm with a rotation arrow",
      tags=["ptz", "pan tilt zoom", "cctv", "surveillance", "camera", "rotating camera"])
def _(S):
    return [
        line(seg(3, 3, 3, 12)),
        line(poly([(3, 6), (9, 6), (9, 9)], r=S.r)),
        shell(circle(13, 13.5, 5)),
        dot(13, 13.5, 1.8),
        line(arc(13, 13.5, 8.5, -60, 5)),
        line(poly([(19, 8.5), (20.6, 11.2), (17.5, 11.5)], r=S.r * 0.3)),
    ]


@icon("body-camera", CAT, "Small camera on a chest strap with a round lens and a record dot",
      tags=["bodycam", "body worn camera", "police", "security guard", "recording", "chest camera"])
def _(S):
    return [
        line(seg(2, 9, 7, 9)),
        line(seg(17, 9, 22, 9)),
        line(seg(2, 16, 7, 16)),
        line(seg(17, 16, 22, 16)),
        shell(rect(7, 4.5, 10, 15, rr(S, 3))),
        detail(circle(12, 10, 2.2)),
        dot(12, 16, 1),
    ]


@icon("cctv-monitor-wall", CAT, "Two by two grid of monitors on a stand, each showing a camera view",
      tags=["video wall", "cctv", "control room", "monitors", "surveillance", "security operations"])
def _(S):
    parts = []
    for x in (2.5, 12.5):
        for y in (2.5, 11):
            parts.append(shell(rect(x, y, 9, 7, rr(S, 1.5))))
            parts.append(dot(x + 4.5, y + 3.5, 1.1))
    parts.append(line(seg(12, 18, 12, 21.5)))
    parts.append(line(seg(8, 21.5, 16, 21.5)))
    return parts


@icon("cctv-recorder", CAT, "Flat recorder box with status lights and a cable running to a small camera",
      tags=["dvr", "nvr", "cctv", "video recorder", "surveillance", "storage"])
def _(S):
    return [
        shell(rect(2.5, 12.5, 14, 7.5, rr(S, 2))),
        dot(6, 16.3, 1),
        dot(9, 16.3, 1),
        sq(11.5, 15.5, 3, 1.6),
        line(poly([(6.5, 12.5), (6.5, 6), (13, 6)], r=S.r)),
        shell(rect(13, 3, 8.5, 6, rr(S, 1.5))),
        dot(17.3, 6, 1.2),
    ]


@icon("cctv-warning-sign", CAT, "Square sign with a camera silhouette and a small warning triangle",
      tags=["cctv sign", "camera in use", "surveillance notice", "warning", "monitored area", "video surveillance"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(rect(6, 12, 7, 4.5, rr(S, 1))),
        Part("dot", poly([(13, 13), (17, 11), (17, 17.5), (13, 15.5)], closed=True)),
        Part("dot", poly([(10, 6), (12, 9.5), (8, 9.5)], closed=True)),
    ]


@icon("license-plate-recognition", CAT, "Number plate with character blocks inside four corner scan brackets",
      tags=["anpr", "alpr", "number plate", "licence plate", "car park", "traffic camera", "scan"])
def _(S):
    parts = []
    a, b, arm = 2, 22, 4.5
    for pts in ([(a, a + arm), (a, a), (a + arm, a)], [(b - arm, a), (b, a), (b, a + arm)],
                [(a, b - arm), (a, b), (a + arm, b)], [(b - arm, b), (b, b), (b, b - arm)]):
        parts.append(line(poly(pts, r=S.r)))
    parts.append(shell(rect(6, 8.5, 12, 7, rr(S, 1.5))))
    for x in (8, 11, 14):
        parts.append(sq(x, 10.5, 2, 3))
    return parts


# ============================================================================ listening gear

@icon("wiretap", CAT, "Old telephone handset with a clip on its cord and a wire to an earphone",
      tags=["phone tap", "eavesdrop", "listening", "bug", "spy", "intercept call", "telephone"])
def _(S):
    return [
        shell("M3.5 10.5V9C3.5 7 5.5 5.5 8 5.5H16C18.5 5.5 20.5 7 20.5 9V10.5H17.5V9H6.5V10.5Z"),
        line(seg(12, 9, 12, 13)),
        shell(rect(10, 13, 4, 3.5, rr(S, 1))),
        line(poly([(12, 16.5), (12, 19.5), (15, 19.5)], r=S.r)),
        shell(circle(17.7, 19.5, 2.2)),
    ]


@icon("listening-bug", CAT, "Button-sized round microphone device with an antenna and sound arcs",
      tags=["hidden microphone", "bug", "eavesdropping", "spy", "covert", "audio surveillance"])
def _(S):
    return [
        shell(circle(8, 15, 5)),
        dot(8, 15, 1.5),
        line(seg(8, 10, 8, 4.5)),
        dot(8, 3.8, 1.2),
        line(arc(8, 15, 8, -38, 38)),
        line(arc(8, 15, 11.5, -32, 32)),
    ]


@icon("night-vision-goggles", CAT, "Front view of goggles with two tube eyepieces and a strap over the top",
      tags=["nvg", "night vision", "military", "dark", "infrared", "goggles", "spy gear"])
def _(S):
    return [
        shell(rect(2.5, 11, 8, 10, S.R)),
        shell(rect(13.5, 11, 8, 10, S.R)),
        detail(circle(6.5, 16, 1.6)),
        detail(circle(17.5, 16, 1.6)),
        line(seg(10.5, 14, 13.5, 14)),
        line(poly([(6.5, 11), (6.5, 8), (9, 4.5), (15, 4.5), (17.5, 8), (17.5, 11)], r=S.r)),
    ]

def rot(pts, deg=45, cx=12.0, cy=12.0):
    """Rotate points clockwise on screen about (cx, cy)."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rbox(x, y, w, h, deg=45):
    return rot([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], deg)


# ============================================================================ more surveillance

@icon("surveillance-earpiece", CAT, "In-ear bud with a coiled cable running down to a clip",
      tags=["security earpiece", "covert earpiece", "coiled cable", "bodyguard", "radio", "secret service"])
def _(S):
    return [
        shell(circle(8, 5.5, 3.3)),
        line("M8 8.8C8 10 8 10 8 10.5C14 10.5 14 14.5 8 14.5S2 18.5 8 18.5"),
        shell(rect(6, 18.5, 4, 3, rr(S, 1))),
    ]


@icon("surveillance-van", CAT, "Windowless panel van with a satellite dish and antenna on its roof",
      tags=["spy van", "surveillance vehicle", "stakeout", "undercover", "monitoring", "police van"])
def _(S):
    return [
        shell(poly([(2.5, 8), (15, 8), (18.5, 11.5), (21.5, 12.5), (21.5, 17), (2.5, 17)], closed=True, r=S.r)),
        shell(circle(7, 18, 2.5)),
        shell(circle(17, 18, 2.5)),
        detail(poly([(15.5, 8.5), (15.5, 12.5), (21.5, 12.5)])),
        line("M5 4.5a3 3 0 0 0 6 0"),
        line(seg(11, 2.5, 11, 5)),
        line(seg(16.5, 3, 16.5, 8)),
    ]


def _eye(S, cx, cy, rx, ry):
    if S.name == "line":
        return f"M{fmt(cx - rx)} {fmt(cy)}Q{fmt(cx)} {fmt(cy - 2 * ry)} {fmt(cx + rx)} {fmt(cy)}Q{fmt(cx)} {fmt(cy + 2 * ry)} {fmt(cx - rx)} {fmt(cy)}Z"
    return ellipse(cx, cy, rx, ry)


@icon("fake-cell-tower", CAT, "Small lattice tower topped with an open eye instead of an antenna",
      tags=["imsi catcher", "stingray", "cell site simulator", "phone tracking", "surveillance", "rogue tower"])
def _(S):
    return [
        shell(_eye(S, 12, 5, 5, 2.4)),
        dot(12, 5, 1),
        line(seg(11, 9.5, 7, 21.5)),
        line(seg(13, 9.5, 17, 21.5)),
        line(seg(9.7, 14, 14.3, 14)),
        line(seg(8.3, 18, 15.7, 18)),
        line(seg(9.7, 14, 15.7, 18)),
        line(seg(14.3, 14, 8.3, 18)),
    ]


@icon("mobile-surveillance-tower", CAT, "Trailer with a tall mast carrying a camera head and a small solar panel",
      tags=["mobile tower", "camera trailer", "portable surveillance", "cctv trailer", "site security", "solar"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 8, 4.5, rr(S, 2))),
        dot(11.6, 4.8, 1),
        line(seg(9.5, 7, 9.5, 15)),
        shell(poly([(13.5, 10), (21, 8.5), (21, 13), (13.5, 14.5)], closed=True, r=S.r * 0.5)),
        shell(rect(3, 15, 15, 3, rr(S, 1))),
        line("M7.5 18a2.6 2.6 0 0 0 5.2 0"),
        line(seg(18, 16.5, 21.5, 16.5)),
    ]


@icon("spy-pen-camera", CAT, "Ballpoint pen with a tiny round camera lens set into its barrel",
      tags=["hidden camera", "spy pen", "covert recording", "pen camera", "undercover", "secret"])
def _(S):
    lens = rot([(14.5, 8)])[0]
    return [
        shell(poly(rbox(9.5, 3.5, 5, 12), closed=True, r=S.r * 0.6)),
        shell(poly(rot([(9.5, 15.5), (14.5, 15.5), (12, 21)]), closed=True, r=S.r * 0.4)),
        shell(circle(lens[0], lens[1], 2.6)),
        dot(lens[0], lens[1], 0.9),
    ]


@icon("neighborhood-watch-sign", CAT, "Sign on a post showing a house roof above an open eye",
      tags=["neighbourhood watch", "community watch", "crime prevention", "vigilant", "sign", "look out"])
def _(S):
    return [
        shell(rect(3, 2, 18, 17, rr(S, 3))),
        detail(poly([(7, 8.2), (12, 4.8), (17, 8.2)], r=S.r * 0.4)),
        detail("M6.5 13.5Q12 8.5 17.5 13.5Q12 18.5 6.5 13.5Z"),
        dot(12, 13.5, 1),
        line(seg(12, 19, 12, 22)),
    ]


# ============================================================================ safes

@icon("safe-deposit-box", CAT, "Long narrow metal box with a hinged lid and two keyholes on its front",
      tags=["bank vault", "deposit box", "strongbox", "valuables", "storage", "bank"])
def _(S):
    return [
        shell(poly([(4, 10), (6, 4), (18, 4), (20, 10)], closed=True, r=S.r * 0.6)),
        shell(rect(2.5, 10, 19, 10, rr(S, 2))),
        dot(8, 14, 1.3),
        dot(16, 14, 1.3),
        sq(7.2, 15.5, 1.6, 2),
        sq(15.2, 15.5, 1.6, 2),
    ]


@icon("hidden-wall-safe", CAT, "Picture frame swung open on a hinge to show a wall safe with a dial behind it",
      tags=["wall safe", "hidden safe", "secret compartment", "behind painting", "valuables", "vault"])
def _(S):
    return [
        shell(poly([(2.5, 4), (8, 6.5), (8, 17.5), (2.5, 20)], closed=True, r=S.r * 0.5)),
        detail(poly([(4.5, 7.5), (6, 8.3), (6, 15.7), (4.5, 16.5)])),
        shell(rect(10, 4, 11.5, 16, S.R)),
        detail(circle(15.7, 12, 3)),
        dot(15.7, 12, 1),
    ]


@icon("floor-safe", CAT, "Floor hatch in perspective with a round combination dial set into its lid",
      tags=["underfloor safe", "in-floor safe", "hidden safe", "vault", "dial", "valuables"])
def _(S):
    return [
        shell(poly([(6, 5), (18, 5), (22, 19), (2, 19)], closed=True, r=S.r)),
        detail(ellipse(12, 12, 5.2, 3.6)),
        dot(12, 12, 1),
        detail(seg(12, 12, 15, 10.2)),
    ]


@icon("keypad-safe", CAT, "Small cube safe with a numeric keypad and a round handle on its door",
      tags=["digital safe", "electronic safe", "pin code", "hotel safe", "keypad", "strongbox"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, S.R))]
    for x in (7, 10.5):
        for y in (8, 12, 16):
            parts.append(dot(x, y, 1.1))
    parts.append(detail(circle(16.3, 12, 2.8)))
    parts.append(dot(16.3, 12, 0.9))
    return parts


@icon("deposit-safe", CAT, "Safe with a pull-out drop drawer on its top and a dial below",
      tags=["drop safe", "cash drop", "night deposit", "till safe", "retail", "cash handling"])
def _(S):
    return [
        shell(rect(7, 3, 10, 4.5, rr(S, 2))),
        sq(8.5, 4.6, 7, 1.4),
        shell(rect(3, 7.5, 18, 13.5, S.R)),
        detail(circle(12, 14.3, 3.2)),
        dot(12, 14.3, 1),
    ]


@icon("key-drop-box", CAT, "Wall box with a letterbox style slot and a small key above it",
      tags=["key safe", "key return", "after hours drop", "key box", "rental", "dealership"])
def _(S):
    return [
        shell(rect(4, 3, 16, 18, S.R)),
        dot(8.5, 8, 2),
        detail(seg(10.5, 8, 16.5, 8)),
        detail(seg(14.5, 8, 14.5, 10.5)),
        sq(7, 14.5, 10, 2.6),
    ]


@icon("chain-and-padlock", CAT, "Two interlocked chain links with a padlock hanging from them",
      tags=["chain lock", "bike lock", "secured", "gate lock", "heavy duty", "chained"])
def _(S):
    return [
        shell(rect(2, 2.5, 11, 5.5, 2.75)),
        shell(rect(11, 2.5, 11, 5.5, 2.75)),
        line("M9.5 14V12a2.5 2.5 0 0 1 5 0V14"),
        shell(rect(7, 13.5, 10, 8, rr(S, 3))),
        dot(12, 16.8, 1.1),
    ]


@icon("disc-padlock", CAT, "Round disc padlock with a short shackle tucked into a notch at the top",
      tags=["puck lock", "round padlock", "shackleless", "storage unit", "heavy duty", "security lock"])
def _(S):
    return [
        line("M9.5 9V7a2.5 2.5 0 0 1 5 0V9"),
        shell(circle(12, 14.5, 7.5)),
        dot(12, 14, 1.4),
        sq(11.2, 14, 1.6, 3),
    ]


@icon("skeleton-key", CAT, "Old-fashioned key with a looped bow, a long shank and a single square bit",
      tags=["old key", "antique key", "vintage key", "master key", "door key", "mystery"])
def _(S):
    return [
        shell(circle(12, 6.5, 4)),
        line(seg(9.5, 12, 14.5, 12)),
        line(seg(12, 10.5, 12, 21.5)),
        shell(poly([(12, 16), (17, 16), (17, 20), (12, 20)], closed=True, r=S.r)),
    ]


# ============================================================================ more keys and locks

@icon("tubular-key", CAT, "Key with a round bow and a short hollow barrel notched around its tip",
      tags=["tubular lock key", "barrel key", "vending machine key", "cylinder key", "round key", "bike lock key"])
def _(S):
    return [
        shell(circle(12, 5.5, 3.5)),
        shell(poly([(9, 10), (15, 10), (15, 21.5), (13.5, 21.5), (13.5, 19), (10.5, 19), (10.5, 21.5), (9, 21.5)], closed=True, r=S.r * 0.5)),
        dot(12, 14.5, 1.1),
    ]


@icon("cross-key", CAT, "Key with a round bow and a four-winged cross-shaped blade",
      tags=["cross blade key", "four way key", "plus key", "dimple key", "door key", "security key"])
def _(S):
    return [
        shell(circle(12, 4.8, 3)),
        line(seg(12, 8, 12, 11.5)),
        shell(poly([(10, 11.5), (14, 11.5), (14, 14.5), (17, 14.5), (17, 18.5), (14, 18.5), (14, 21.5), (10, 21.5),
                    (10, 18.5), (7, 18.5), (7, 14.5), (10, 14.5)], closed=True, r=S.r * 0.6)),
    ]


@icon("broken-key", CAT, "Key snapped in two with a jagged break and the tip piece set slightly apart",
      tags=["snapped key", "stuck key", "lockout", "key stuck in lock", "damaged key", "locksmith"])
def _(S):
    return [
        shell(circle(12, 5, 3.5)),
        shell(poly([(10, 8.5), (14, 8.5), (14, 13), (12, 11), (10, 13)], closed=True, r=S.r * 0.3)),
        shell(poly([(11, 17), (13, 15.5), (15, 17), (15, 21.5), (11, 21.5)], closed=True, r=S.r * 0.3)),
    ]


@icon("locker-key-band", CAT, "Coiled wrist band with a small tag and a key hanging from it",
      tags=["wristband key", "gym locker key", "pool key", "spiral wrist coil", "changing room", "locker"])
def _(S):
    return [
        line(ellipse(10, 8, 7, 5)),
        line(ellipse(10, 11.5, 7, 5)),
        shell(rect(15, 15.5, 6.5, 5.5, rr(S, 2))),
        dot(4.5, 19, 2),
        line(seg(6.5, 19, 12, 19)),
        line(seg(10.5, 19, 10.5, 21.5)),
    ]


@icon("key-ring", CAT, "Split ring with three keys hanging from it at different angles",
      tags=["keychain", "keys", "bunch of keys", "key holder", "house keys", "car keys"])
def _(S):
    return [
        line(circle(12, 6.5, 4.5)),
        dot(9, 13.5, 1.7),
        dot(12, 13.5, 1.7),
        dot(15, 13.5, 1.7),
        line(seg(9, 13.5, 6, 21.5)),
        line(seg(12, 13.5, 12, 21.5)),
        line(seg(15, 13.5, 18, 21.5)),
        line(seg(6.8, 19.3, 4.3, 18.6)),
        line(seg(17.2, 19.3, 19.7, 18.6)),
    ]


@icon("lock-cylinder", CAT, "Side view of a cylinder lock with a round barrel on a narrower stem and a keyway",
      tags=["lock barrel", "euro cylinder", "profile cylinder", "locksmith", "lock core", "keyway"])
def _(S):
    if S.name == "line":
        body = "M8.5 21.5V14.48A6.5 6.5 0 1 1 15.5 14.48V21.5Z"
    else:
        body = "M8.5 20V14.48A6.5 6.5 0 1 1 15.5 14.48V20A1.5 1.5 0 0 1 14 21.5H10A1.5 1.5 0 0 1 8.5 20Z"
    return [
        shell(body),
        dot(12, 8.5, 1.5),
        sq(11.2, 8.5, 1.6, 3.5),
        dot(12, 18, 1),
    ]


# ============================================================================ doors, fences and gates

@icon("security-door", CAT, "Reinforced door in a heavy frame with four bolt bars extending into the frame",
      tags=["steel door", "reinforced door", "deadbolt", "bolt bars", "secure entry", "vault door"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, S.R)),
        detail(rect(6, 5.5, 10.5, 14)),
        detail(seg(16.5, 8, 21, 8)),
        detail(seg(16.5, 11.5, 21, 11.5)),
        detail(seg(16.5, 15, 21, 15)),
        detail(seg(16.5, 18.5, 21, 18.5)),
        dot(13.2, 13, 1),
    ]


@icon("scissor-gate", CAT, "Collapsible folding gate with a lattice of crossing diagonal bars between posts",
      tags=["folding gate", "security gate", "lattice gate", "accordion gate", "shutter", "shop front"])
def _(S):
    parts = [line(seg(3, 2.5, 3, 21.5)), line(seg(21, 2.5, 21, 21.5))]
    for x0 in (3, 12):
        for y0 in (3, 12):
            parts.append(line(seg(x0, y0, x0 + 9, y0 + 9)))
            parts.append(line(seg(x0 + 9, y0, x0, y0 + 9)))
    return parts


def _star4(cx, cy, ro, ri):
    return poly(star(cx, cy, ro, ri, 4), closed=True)


@icon("razor-wire", CAT, "Coiled loops of wire running sideways with small blade barbs along them",
      tags=["barbed wire", "concertina wire", "fence", "prison", "perimeter", "boundary", "no entry"])
def _(S):
    parts = [line(circle(6, 12, 5)), line(circle(12, 12, 5)), line(circle(18, 12, 5))]
    for x, y in ((6, 4.3), (18, 4.3), (12, 19.7)):
        if S.name == "line":
            parts.append(line(seg(x - 2, y - 2, x + 2, y + 2)))
            parts.append(line(seg(x + 2, y - 2, x - 2, y + 2)))
        else:
            parts.append(dot(x, y, 1.6))
    return parts


@icon("anti-climb-spikes", CAT, "Wall top with a row of sharp upward spikes mounted along it",
      tags=["wall spikes", "anti intruder", "fence spikes", "perimeter", "deterrent", "rooftop protection"])
def _(S):
    parts = [shell(rect(2, 14, 20, 7.5, rr(S, 3.5))), detail(seg(2, 17.8, 22, 17.8))]
    for cx in (4, 8, 12, 16, 20):
        parts.append(solid(poly([(cx - 1.5, 14), (cx, 4.5), (cx + 1.5, 14)], closed=True)))
    return parts


@icon("glass-break-detector", CAT, "Window pane with a crack star, a small sensor above and sound arcs",
      tags=["window alarm", "break-in sensor", "acoustic sensor", "burglar alarm", "intrusion", "glass sensor"])
def _(S):
    return [
        shell(rect(3, 9.5, 18, 12, S.R)),
        detail(seg(11, 15, 6.5, 11.8)),
        detail(seg(11, 15, 16, 12.2)),
        detail(seg(11, 15, 8, 19.5)),
        detail(seg(11, 15, 17.5, 18.5)),
        shell(circle(12, 4.5, 2.2)),
        line(arc(12, 4.5, 5.5, 160, 200)),
        line(arc(12, 4.5, 5.5, -20, 20)),
    ]


@icon("laser-tripwire", CAT, "Two posts with three dotted laser beams running between them",
      tags=["laser alarm", "beam sensor", "infrared beam", "intruder detection", "perimeter alarm", "trip beam"])
def _(S):
    rx = 0 if S.name == "line" else 1.8
    parts = [shell(rect(2, 4, 4, 17, rx)), shell(rect(18, 4, 4, 17, rx))]
    for y in (8, 12.5, 17):
        for x in (8.7, 12, 15.3):
            parts.append(dot(x, y, 0.9))
    return parts


@icon("anti-theft-gate", CAT, "Pair of upright pedestal panels at a shop exit with signal arcs between them",
      tags=["eas gate", "shop alarm", "security gate", "store exit", "shoplifting", "tag detector"])
def _(S):
    return [
        shell(rect(2, 3, 5, 18, S.R)),
        shell(rect(17, 3, 5, 18, S.R)),
        line(arc(7, 12, 3.5, -40, 40)),
        line(arc(7, 12, 6.3, -40, 40)),
        dot(4.5, 7, 0.9),
    ]


# ============================================================================ alarms and emergency

@icon("panic-button", CAT, "Large round push button on a square base with a raised hand on it",
      tags=["alarm button", "emergency button", "duress", "help button", "sos", "safety button"])
def _(S):
    hand = ("M8.8 10V5.8H10.3V10Z M10.9 10V4.8H12.4V10Z M13 10V5.2H14.5V10Z M15.1 10V6.6H16.6V10Z"
            "M8.8 9H16.6V13.2H8.8Z M6.8 10.6H8.8V12.2H6.8Z")
    return [
        shell(circle(12, 9.3, 7.3)),
        shell(rect(3, 15.5, 18, 6, rr(S, 3))),
        Part("dot", hand),
    ]


@icon("break-glass-call-point", CAT, "Square wall box with a glass front panel showing a crack mark",
      tags=["fire alarm", "manual call point", "emergency alarm", "break glass", "alarm pull", "fire safety"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(rect(6, 6, 12, 12, rr(S, 1))),
        detail(poly([(8.5, 7.5), (11.5, 11), (10, 12.5), (14, 16.5)])),
        detail(poly([(11.5, 11), (15.5, 9.5)])),
    ]

@icon("emergency-call-tower", CAT, "Tall pillar with a beacon light on top, a speaker panel and a call button",
      tags=["help point", "blue light phone", "emergency phone", "campus safety", "call box", "sos pillar"])
def _(S):
    return [
        shell("M9 7a3 3 0 0 1 6 0Z"),
        line(seg(4.5, 4.5, 6.8, 5.6)),
        line(seg(19.5, 4.5, 17.2, 5.6)),
        shell(rect(7, 7, 10, 15, rr(S, 3))),
        detail(seg(9.8, 11, 14.2, 11)),
        detail(seg(9.8, 13.8, 14.2, 13.8)),
        dot(12, 18, 1.6),
    ]


@icon("door-stop-alarm", CAT, "Rubber door wedge with a speaker grille on its sloped face and sound arcs",
      tags=["door wedge alarm", "travel alarm", "door jammer", "hotel safety", "siren", "intruder alert"])
def _(S):
    return [
        shell(poly([(2.5, 21), (20.5, 21), (20.5, 7.5)], closed=True, r=S.r), stroke_miterlimit="2"),
        dot(11.5, 17.5, 1.1),
        dot(15, 17.5, 1.1),
        dot(18.3, 17.5, 1.1),
        line(arc(12, 13.5, 4, 205, 250)),
        line(arc(12, 13.5, 7.5, 205, 250)),
    ]


@icon("personal-alarm", CAT, "Small keychain siren with a pull pin on a cord and sound arcs",
      tags=["rape alarm", "safety alarm", "keyring alarm", "panic alarm", "siren", "self defense"])
def _(S):
    return [
        line(circle(6.5, 5, 2.3)),
        shell(rect(3, 9, 10, 12.5, S.R)),
        dot(6.3, 14, 0.9),
        dot(9.7, 14, 0.9),
        dot(6.3, 17.5, 0.9),
        dot(9.7, 17.5, 0.9),
        line(poly([(10.5, 9), (10.5, 5), (14, 5)], r=S.r * 0.5)),
        dot(16, 5, 1.3),
        line(arc(13, 15, 4.2, -40, 40)),
        line(arc(13, 15, 7.4, -40, 40)),
    ]


@icon("panic-exit-bar", CAT, "Door with a long horizontal push bar across it and a small arrow along it",
      tags=["push bar", "crash bar", "fire exit", "emergency exit door", "egress", "exit device"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, S.R)),
        detail(rect(6.5, 7.5, 11, 4, rr(S, 2))),
        detail(seg(8, 16.5, 16, 16.5)),
        detail(poly([(13.6, 14.3), (16, 16.5), (13.6, 18.7)])),
    ]


@icon("security-mirror-dome", CAT, "Half sphere convex mirror in a ceiling corner with a curved highlight",
      tags=["convex mirror", "shop mirror", "anti shoplifting mirror", "blind spot mirror", "corner mirror", "retail security"])
def _(S):
    return [
        shell("M3 3H21A18 18 0 0 1 3 21Z"),
        detail(arc(3, 3, 9, 12, 78)),
        dot(14.5, 14.5, 1.2),
    ]


@icon("liquids-bag", CAT, "Clear resealable bag with a zip line at the top holding three small bottles",
      tags=["airport liquids", "100ml", "travel size bottles", "clear bag", "carry on", "toiletries"])
def _(S):
    return [
        shell(rect(3.5, 3.5, 17, 18, S.R)),
        detail(seg(3.5, 8, 20.5, 8)),
        sq(6, 13, 3.5, 6, 0.6),
        sq(10.25, 13, 3.5, 6, 0.6),
        sq(14.5, 13, 3.5, 6, 0.6),
        sq(7, 10.8, 1.5, 2),
        sq(11.25, 10.8, 1.5, 2),
        sq(15.5, 10.8, 1.5, 2),
    ]


@icon("body-armor", CAT, "Front view of a sleeveless protective vest with shoulder straps and a front plate",
      tags=["bulletproof vest", "ballistic vest", "flak jacket", "protective vest", "armour", "police gear"])
def _(S):
    return [
        shell(poly([(7, 3), (10, 3), (12, 5.5), (14, 3), (17, 3), (17, 9), (19.5, 10.5), (19.5, 21.5), (4.5, 21.5),
                    (4.5, 10.5), (7, 9)], closed=True, r=S.r)),
        detail(rect(8.5, 11, 7, 7, rr(S, 1.5))),
    ]


@icon("riot-shield", CAT, "Tall rounded shield with a viewing slot and the handle showing through",
      tags=["police shield", "riot gear", "protective shield", "crowd control", "transparent shield", "tactical"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 13, 19, S.R)),
        detail(rect(8.5, 5.5, 7, 3.5, rr(S, 1.5))),
        detail(rect(10, 12.5, 4, 5, rr(S, 1.5))),
    ]


@icon("handcuffs", CAT, "Pair of round cuffs joined by a short chain, one with a keyhole",
      tags=["restraints", "arrest", "police", "custody", "cuffs", "law enforcement"])
def _(S):
    rx = 0 if S.name == "line" else 2.6
    return [
        shell(circle(6.5, 14.5, 4.5)),
        shell(circle(17.5, 14.5, 4.5)),
        shell(rect(3.5, 3.5, 6, 5.5, rx)),
        shell(rect(14.5, 3.5, 6, 5.5, rx)),
        dot(6.5, 6.25, 0.9),
        line(seg(11, 14.5, 13, 14.5)),
    ]


@icon("spike-strip", CAT, "Folding road strip lying across the road with rows of upward spikes",
      tags=["tire spikes", "stinger", "road spikes", "police barrier", "vehicle stopper", "traffic control"])
def _(S):
    parts = [shell(poly([(3, 19), (7, 11.5), (21, 11.5), (17, 19)], closed=True, r=S.r * 0.6)),
             detail(seg(7.8, 18.5, 11.3, 12)), detail(seg(12.6, 18.5, 16.2, 12))]
    for cx in (10, 13.5, 17, 20.5):
        parts.append(solid(poly([(cx - 1.3, 11.5), (cx, 4.5), (cx + 1.3, 11.5)], closed=True)))
    return parts


@icon("gas-mask", CAT, "Front view of a full face mask with two round eye lenses and a round filter below",
      tags=["respirator", "chemical protection", "hazmat", "cbrn", "face mask", "protective gear"])
def _(S):
    return [
        shell(poly([(5, 4), (19, 4), (20, 11), (16, 16.5), (8, 16.5), (4, 11)], closed=True, r=S.r * 2.2)),
        detail(circle(8.6, 9.5, 2.3)),
        detail(circle(15.4, 9.5, 2.3)),
        shell(circle(12, 19.2, 2.8)),
    ]


@icon("bag-inspection", CAT, "Handbag with a magnifying glass held above its opening",
      tags=["bag check", "search bag", "baggage screening", "customs", "security check", "inspect"])
def _(S):
    return [
        line("M5.5 12V9.5a2.5 2.5 0 0 1 5 0V12"),
        shell(poly([(3, 12), (17, 12), (19, 21.5), (2, 21.5)], closed=True, r=S.r)),
        shell(circle(16.5, 6.5, 3.5)),
        line(seg(19, 9, 21.7, 11.7)),
    ]


@icon("robber", CAT, "Figure in a striped shirt and eye mask carrying a sack over one shoulder",
      tags=["burglar", "thief", "criminal", "masked bandit", "crime", "loot"])
def _(S):
    return [
        shell(circle(8.5, 6, 3.2)),
        detail(seg(5.8, 6, 11.2, 6)),
        shell(poly([(3.5, 21.5), (3.5, 13), (5.5, 10), (11.5, 10), (13.5, 13), (13.5, 21.5)], closed=True, r=S.r)),
        detail(seg(3.5, 14.5, 13.5, 14.5)),
        detail(seg(3.5, 18, 13.5, 18)),
        shell(circle(17.5, 14, 4.5)),
        line(poly([(16, 9.8), (17.5, 6.8), (19, 9.8)], r=S.r * 0.3)),
    ]



@icon("safecracker", CAT, "Round safe dial with a stethoscope chest piece against it and the tubing curling away",
      tags=["safe cracking", "locksmith", "heist", "vault breaker", "stethoscope", "combination lock"])
def _(S):
    return [
        shell(rect(2.5, 7, 14, 14, S.R)),
        detail(circle(9.5, 14, 3.6)),
        dot(9.5, 14, 1),
        shell(circle(15.5, 9, 2.4)),
        line("M17.2 7.4C20 4 22 8 21.5 12S19.5 20 16.5 21"),
    ]

# ============================================================================ fraud and forensics

@icon("identity-theft", CAT, "ID card with a photo being pulled away by a gloved hand gripping its corner",
      tags=["id theft", "stolen identity", "impersonation", "fraud", "identity fraud", "personal data stolen"])
def _(S):
    return [
        shell(rect(2.5, 10, 14.5, 11, rr(S, 2))),
        dot(7, 13.5, 1.5),
        sq(5, 16, 4, 2, 0.8),
        detail(seg(11, 14, 14, 14)),
        shell(rect(13.5, 2.5, 8, 6.5, rr(S, 3))),
        shell(rect(10.5, 6, 5.5, 2.4, 1.2)),
    ]


@icon("card-skimmer", CAT, "Card machine slot hidden under a bulky fake overlay with a card half inserted",
      tags=["atm skimmer", "card reader fraud", "payment fraud", "fake reader", "credit card theft", "skimming"])
def _(S):
    return [
        line(poly([(8, 11), (8, 2.5), (16, 2.5), (16, 11)], r=S.r * 0.5)),
        detail(seg(8, 5.5, 16, 5.5)),
        shell(rect(2.5, 11, 19, 10.5, S.R)),
        detail(seg(6.5, 16.3, 17.5, 16.3)),
    ]


@icon("evidence-bag", CAT, "Clear sealed bag with a striped label area at the top and a small item inside",
      tags=["forensic bag", "crime scene", "evidence", "sample bag", "police", "exhibit"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, S.R)),
        sq(7.5, 5, 9, 1.6),
        detail(seg(5, 9, 19, 9)),
        sq(10.5, 12.5, 3, 6, 1.5),
    ]


@icon("evidence-marker", CAT, "Folded A-shaped tent card standing on the ground with a number on its face",
      tags=["crime scene marker", "evidence number", "evidence tent", "forensics", "numbered marker", "investigation"])
def _(S):
    return [
        shell(poly([(9, 3.5), (15, 3.5), (20, 20.5), (4, 20.5)], closed=True, r=S.r)),
        detail(poly([(10.5, 10.5), (12.5, 8.5), (12.5, 16.5)])),
        detail(seg(10.5, 16.5, 14.5, 16.5)),
    ]


@icon("fingerprint-dusting", CAT, "Fluffy round brush dusting a partial fingerprint with a few powder dots",
      tags=["latent prints", "forensics", "crime scene", "print powder", "fingerprint lifting", "csi"])
def _(S):
    return [
        shell(circle(11, 6.5, 3.2)),
        line(seg(13.3, 4.3, 19, 1.8)),
        dot(17, 9, 0.9),
        dot(19.5, 6.5, 0.9),
        dot(5.5, 10, 0.9),
        line(arc(11, 22, 3, 210, 330)),
        line(arc(11, 22, 6.2, 210, 330)),
        line(arc(11, 22, 9.4, 210, 330)),
    ]


@icon("ten-print-card", CAT, "Fingerprint card with two rows of five small boxes",
      tags=["fingerprint card", "booking", "ten print", "police record", "identification", "biometrics"])
def _(S):
    parts = [shell(rect(2.5, 3.5, 19, 17, S.R))]
    for i in range(5):
        x = 5.3 + i * 3.1
        parts.append(sq(x, 8, 2.2, 2.6, 0.5))
        parts.append(sq(x, 13, 2.2, 2.6, 0.5))
    return parts


@icon("dna-profiling", CAT, "Electrophoresis gel with four lanes of short horizontal bands at different heights",
      tags=["dna fingerprint", "gel electrophoresis", "genetic test", "forensic dna", "lab", "paternity"])
def _(S):
    bands = {6.5: (7, 11, 16), 10.1: (8.5, 13.5), 13.7: (7, 10, 15), 17.3: (9, 12.5, 17)}
    parts = [shell(rect(3, 3, 18, 18, S.R))]
    for x, ys in bands.items():
        for y in ys:
            parts.append(sq(x - 1.2, y, 2.4, 1.5))
    return parts


@icon("mugshot", CAT, "Head and shoulders in front of height marks, holding a placard at chest level",
      tags=["booking photo", "police photo", "arrest", "criminal record", "suspect", "lineup"])
def _(S):
    parts = [shell(circle(12, 7, 3.2)),
             shell(poly([(6.5, 21.5), (6.5, 15.5), (9, 12.5), (15, 12.5), (17.5, 15.5), (17.5, 21.5)], closed=True, r=S.r)),
             sq(9.5, 16.5, 5, 3.2, 0.6)]
    for y in (5, 9, 13, 17, 21):
        parts.append(line(seg(2, y, 4.5, y)))
        parts.append(line(seg(19.5, y, 22, y)))
    return parts


@icon("police-lineup", CAT, "Three standing figures of different heights in a row",
      tags=["identity parade", "suspects", "police", "witness", "criminal investigation", "height chart"])
def _(S):
    parts = []
    rx = 0.6 if S.name == "line" else 1.7
    for cx, hy, top in ((5, 7, 10.5), (12, 4.5, 8), (19, 8.5, 12)):
        parts.append(shell(circle(cx, hy, 2.0)))
        parts.append(shell(rect(cx - 1.7, top, 3.4, 21.5 - top, rx)))
    return parts


@icon("lie-detector", CAT, "Paper strip with a jagged scribbled line and a thin needle arm drawing on it",
      tags=["polygraph", "truth test", "interrogation", "investigation", "test", "deception"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 13, 17, rr(S, 2))),
        detail(poly([(5, 12), (7, 7.5), (9.5, 16), (11.5, 8.5), (13, 13)])),
        line(seg(20.5, 20.5, 14.8, 13.5)),
        dot(20.5, 20.5, 1.4),
    ]


@icon("ankle-monitor", CAT, "Lower leg and foot with a chunky strap device on the ankle and a signal arc",
      tags=["electronic tag", "house arrest", "gps tracker", "probation", "parole", "offender monitoring"])
def _(S):
    return [
        line(poly([(7, 2.5), (7, 17), (5.5, 20), (5.5, 21.5), (20.5, 21.5), (20.5, 19.5), (17, 17.5), (17, 2.5)], r=S.r)),
        shell(rect(5, 11, 14, 5, rr(S, 2))),
        dot(12, 13.5, 1),
        line(arc(12, 9.5, 3.2, -125, -55)),
        line(arc(12, 9.5, 6, -125, -55)),
    ]


@icon("wanted-poster", CAT, "Pinned poster with a framed face silhouette and two lines of bold text beneath",
      tags=["wanted", "fugitive", "criminal", "reward", "notice", "most wanted"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 2.5))),
        detail(rect(7, 6, 10, 6.5)),
        dot(12, 8.6, 1.2),
        sq(9.8, 10.5, 4.4, 1, 0.5),
        detail(seg(7.5, 16, 16.5, 16)),
        detail(seg(9.5, 18.8, 14.5, 18.8)),
    ]


@icon("counterfeit-detector-pen", CAT, "Marker pen drawing a short stroke across the corner of a banknote",
      tags=["fake money", "forged note", "banknote check", "cash handling", "fraud check", "currency"])
def _(S):
    return [
        shell(poly(rot([(10.5, 1.5), (13.5, 1.5), (13.5, 10.5), (10.5, 10.5)], 45), closed=True, r=S.r * 0.6)),
        shell(poly(rot([(10.5, 10.5), (13.5, 10.5), (12, 14.5)], 45), closed=True, r=S.r * 0.4)),
        shell(rect(2.5, 15, 15, 6.5, rr(S, 2))),
        dot(10, 18.2, 1.3),
        sq(4.5, 17.5, 2, 1.4),
    ]


@icon("security-guard-shield-badge", CAT, "Shoulder patch shield with a banner across the top and a star in the centre",
      tags=["guard badge", "security patch", "uniform badge", "officer", "insignia", "patrol"])
def _(S):
    body = ("M4 3.5H20V13C20 17.5 16 20.5 12 21.5C8 20.5 4 17.5 4 13Z" if S.name == "line" else
            "M6.5 3.5H17.5Q20 3.5 20 6V13C20 17.5 16 20.5 12 21.5C8 20.5 4 17.5 4 13V6Q4 3.5 6.5 3.5Z")
    return [
        shell(body),
        detail(seg(4, 8, 20, 8)),
        Part("dot", poly(star(12, 14.3, 3.6, 1.6), closed=True)),
    ]


# ============================================================================ identity documents

@icon("biometric-passport", CAT, "Passport booklet cover with a small emblem ring and a chip symbol near the bottom",
      tags=["e-passport", "epassport", "travel document", "chip passport", "border control", "rfid passport"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 2.5))),
        detail(circle(12, 8, 2.8)),
        detail(rect(8.3, 14, 7.4, 5, rr(S, 1))),
        dot(12, 16.5, 1.1),
    ]


@icon("passport-photo", CAT, "Small photo with a head and shoulders and a guide outline around the head",
      tags=["id photo", "visa photo", "headshot", "photo booth", "biometric photo", "portrait"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, rr(S, 2))),
        detail(ellipse(12, 9.5, 4.6, 5.8)),
        dot(12, 9, 2.2),
        line(poly([(7.3, 21.5), (7.3, 19.3), (9.3, 17.5), (14.7, 17.5), (16.7, 19.3), (16.7, 21.5)], r=S.r * 0.5)),
    ]


@icon("birth-certificate", CAT, "Document with a baby footprint at the top and a ribbon seal in the bottom corner",
      tags=["birth record", "newborn", "registry", "official document", "vital records", "baby"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 2.5))),
        Part("dot", ellipse(10, 9, 1.4, 2.2)),
        dot(7.6, 5.8, 0.7),
        dot(9.4, 5, 0.7),
        dot(11.3, 5.2, 0.7),
        detail(seg(14, 7, 16.5, 7)),
        detail(seg(7.5, 13, 12, 13)),
        shell(circle(15.5, 16.8, 2.4)),
    ]


@icon("digital-id", CAT, "Smartphone showing an ID card layout with a photo square and lines of text",
      tags=["mobile id", "digital identity", "wallet id", "e-id", "phone credential", "verified"])
def _(S):
    return [
        shell(rect(5.5, 2, 13, 20, S.R)),
        sq(8.3, 7.3, 3.4, 3.6, 0.6),
        detail(seg(13.2, 8, 15.7, 8)),
        detail(seg(13.2, 10.8, 15.7, 10.8)),
        detail(seg(8.3, 14.5, 15.7, 14.5)),
    ]


@icon("proof-of-address", CAT, "Utility bill page with a small house at the top and lines of text beneath",
      tags=["utility bill", "address verification", "residence proof", "kyc", "bank statement", "household bill"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rr(S, 2.5))),
        Part("dot", poly([(8.5, 9.2), (8.5, 7.2), (12, 4.6), (15.5, 7.2), (15.5, 9.2)], closed=True)),
        detail(seg(8, 12.5, 16, 12.5)),
        detail(seg(8, 15.5, 16, 15.5)),
        detail(seg(8, 18.5, 13, 18.5)),
    ]


@icon("passport-reader", CAT, "Flat desktop reader with an open passport lying on its glass window",
      tags=["document scanner", "mrz reader", "border control", "id scanner", "check in desk", "travel document"])
def _(S):
    return [
        shell("M3 4.5C6 3.5 9 4 12 6C15 4 18 3.5 21 4.5V12C18 11 15 11.5 12 13.5C9 11.5 6 11 3 12Z"),
        detail(seg(12, 6.5, 12, 13)),
        shell(rect(2.5, 15.5, 19, 6, S.R)),
        dot(6, 18.5, 0.9),
        sq(12, 17.7, 7, 1.6, 0.8),
    ]
