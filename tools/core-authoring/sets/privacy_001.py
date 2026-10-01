"""TypeIcon Core: privacy, cyber attacks, authentication and cryptography (batch 001)."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "privacy"


def _pick(S, sharp, soft):
    return sharp if S.name == "line" else soft


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def rot(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rrect(x, y, w, h, deg, cx=12.0, cy=12.0, r=0.0):
    return poly(rot([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], deg, cx, cy), closed=True, r=r)


def rcen(cx, cy, w, h, deg, r=0.0):
    """Closed rectangle w x h centred on (cx, cy), turned clockwise by deg."""
    return poly(rot([(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)],
                    deg, cx, cy), closed=True, r=r)


def rseg(x1, y1, x2, y2, deg, cx=12.0, cy=12.0):
    (a, b), (c, d) = rot([(x1, y1), (x2, y2)], deg, cx, cy)
    return seg(a, b, c, d)


def brackets(S, x0, y0, x1, y1, arm=3.5):
    """Four corner brackets of a scanning frame."""
    return [line(poly(pts, r=S.r)) for pts in (
        [(x0, y0 + arm), (x0, y0), (x0 + arm, y0)], [(x1 - arm, y0), (x1, y0), (x1, y0 + arm)],
        [(x0, y1 - arm), (x0, y1), (x0 + arm, y1)], [(x1 - arm, y1), (x1, y1), (x1, y1 - arm)])]


def padlock(S, x, y, w, h, sh=None, keyhole=True):
    """Padlock body with its top-left corner at (x, y); shackle rises from the body."""
    sh = sh or w * 0.5
    cx = x + w / 2
    r = sh / 2
    top = y - r - 1.5
    parts = [line(f"M{fmt(cx - r)} {fmt(y)}V{fmt(y - 1.5)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx + r)} {fmt(y - 1.5)}V{fmt(y)}"),
             shell(rect(x, y, w, h, _pick(S, 0.5, min(1.5, w / 4))))]
    if keyhole:
        parts.append(dot(cx, y + h / 2, 1.1))
    return parts


_SHIELD = "M12 2.5L20 5.5V11C20 16 16.6 19.8 12 21.5C7.4 19.8 4 16 4 11V5.5Z"
_SHIELD_ROUND = ("M10.95 2.9L5.05 5.1Q4 5.5 4 6.6V11C4 16 7.4 19.8 12 21.5C16.6 19.8 20 16 20 11V6.6"
                 "Q20 5.5 18.95 5.1L13.05 2.9Q12 2.5 10.95 2.9Z")


def shield(S):
    return shell(_pick(S, _SHIELD, _SHIELD_ROUND))


def envelope(S, x, y, w, h):
    return [shell(rect(x, y, w, h, _pick(S, 1, 2.5))),
            detail(poly([(x + 0.5, y + 0.5), (x + w / 2, y + h * 0.55), (x + w - 0.5, y + 0.5)], r=S.r * 0.5))]


def bug(S, cx, cy, s=1.0):
    """Small beetle seen from above: body oval, head and two legs per side."""
    parts = [shell(ellipse(cx, cy + 0.5 * s, 3.5 * s, 4.5 * s)),
             line(seg(cx - 3.5 * s, cy - 0.5 * s, cx - 6 * s, cy - 2 * s)),
             line(seg(cx + 3.5 * s, cy - 0.5 * s, cx + 6 * s, cy - 2 * s)),
             line(seg(cx - 3.5 * s, cy + 2.5 * s, cx - 6 * s, cy + 4 * s)),
             line(seg(cx + 3.5 * s, cy + 2.5 * s, cx + 6 * s, cy + 4 * s))]
    return parts


# =========================================================================== attacks

@icon("ransomware", CAT, "Document beside a padlock: files locked until payment",
      tags=["ransom", "malware", "encrypted files", "extortion", "cyber attack", "locked files"])
def _(S):
    return [
        shell(poly([(3, 3), (9, 3), (12, 6), (12, 20), (3, 20)], closed=True, r=S.r)),
        detail(seg(6, 10, 9, 10)),
        detail(seg(6, 14, 9, 14)),
        *padlock(S, 14.5, 13, 8, 8, 4.5),
    ]


@icon("phishing", CAT, "Fishing hook dangling over an envelope",
      tags=["scam", "fraud email", "fake email", "hook", "social engineering", "spam"])
def _(S):
    return [
        line(f"M16 2V6.5A3 3 0 0 1 10 6.5"),
        line(seg(10, 6.5, 8.5, 5)),
        *envelope(S, 3, 12, 18, 9),
    ]


@icon("computer-worm", CAT, "Monitor with a segmented worm arching over its top edge",
      tags=["worm", "malware", "virus", "infection", "self replicating", "computer"])
def _(S):
    return [
        shell(rect(3, 11, 18, 9, _pick(S, 1, 2.5))),
        line(seg(9, 22, 15, 22)),
        dot(4.5, 7.5, 1.6), dot(8.5, 5, 1.6), dot(13, 4.5, 1.6), dot(17, 6, 1.6),
        shell(circle(20, 8.5, 1.6)) if S.name == "rounded" else dot(20, 8.5, 1.9),
    ]


@icon("keylogger", CAT, "Keyboard watched by an open eye",
      tags=["spyware", "keystroke", "monitoring", "surveillance", "key logging", "spy"])
def _(S):
    return [
        shell(rect(2, 11, 20, 10, _pick(S, 1.5, 3.5))),
        dot(6.5, 14.5, 1), dot(10.5, 14.5, 1), dot(14.5, 14.5, 1), dot(18.5, 14.5, 1),
        detail(seg(8, 18, 16, 18)),
        shell(_pick(S, "M13 5.5C15 2.5 20 2.5 22 5.5C20 8.5 15 8.5 13 5.5Z",
                    "M13.4 5.0C15.4 2.4 19.6 2.4 21.6 5.0Q22 5.5 21.6 6.0C19.6 8.6 15.4 8.6 13.4 6.0Q13 5.5 13.4 5.0Z")),
    ]


@icon("botnet", CAT, "Four bot heads around a central computer, linked in a hub network",
      tags=["zombie network", "ddos", "hacked computers", "malware network", "command and control", "robots"])
def _(S):
    def head(x, y, up):
        ax = (x + 2.5, y, x + 2.5, y - 2) if up else (x + 2.5, y + 5, x + 2.5, y + 7)
        return [shell(rect(x, y, 5, 5, _pick(S, 0.5, 1.5))), line(seg(*ax))]
    return [
        *head(2, 4.5, True), *head(17, 4.5, True), *head(2, 15.5, False), *head(17, 15.5, False),
        shell(rect(9, 9.5, 6, 5, _pick(S, 0.5, 1.5))),
        line(seg(7, 9.5, 9.5, 11)), line(seg(17, 9.5, 14.5, 11)),
        line(seg(7, 15.5, 9.5, 13.5)), line(seg(17, 15.5, 14.5, 13.5)),
    ]


@icon("brute-force-attack", CAT, "Sledgehammer swinging down onto a padlock",
      tags=["password cracking", "hammer", "guessing", "break in", "attack", "force"])
def _(S):
    return [
        line(seg(2.5, 2.5, 7, 7)),
        shell(rcen(9.5, 9.5, 9, 5, -45, r=S.r * 0.5)),
        *padlock(S, 12.5, 15, 9, 7, 5),
    ]


@icon("sql-injection", CAT, "Database cylinder with a syringe pushed into its side",
      tags=["database attack", "injection", "query", "hack", "sql", "syringe"])
def _(S):
    return [
        shell("M2.5 6A5.5 2.5 0 0 1 13.5 6V17A5.5 2.5 0 0 1 2.5 17Z"),
        detail("M2.5 11.5A5.5 2.5 0 0 0 13.5 11.5"),
        line(rseg(16, 15, 16, 20.5, 45, 16, 12)),
        shell(rrect(14, 7.5, 4, 7.5, 45, 16, 12, r=S.r * 0.3)),
        line(rseg(16, 7.5, 16, 4.5, 45, 16, 12)),
        line(rseg(14, 4.5, 18, 4.5, 45, 16, 12)),
    ]


@icon("zero-day", CAT, "Calendar page with a large zero and a bug at its corner",
      tags=["zero day exploit", "unpatched", "vulnerability", "day zero", "0-day", "bug"])
def _(S):
    return [
        shell(rect(3, 3, 15, 17, _pick(S, 1, 3))),
        detail(seg(3, 8, 18, 8)),
        detail(ellipse(10.5, 14.25, 2.25, 3)),
        shell(ellipse(19, 18.5, 2, 2.75)),
        line(seg(17.3, 15.5, 16, 14)),
        line(seg(20.7, 15.5, 22, 14)),
    ]


@icon("backdoor", CAT, "Server tower with a swung-open door beside it",
      tags=["hidden access", "trojan", "secret entrance", "server", "exploit", "remote access"])
def _(S):
    return [
        shell(rect(3, 2.5, 11, 19, _pick(S, 1, 3))),
        detail(seg(3, 9, 14, 9)),
        detail(seg(3, 15, 14, 15)),
        dot(6.5, 5.75, 1), dot(6.5, 12, 1),
        shell(poly([(18, 11), (22, 9.5), (22, 20), (18, 21.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("honeypot-trap", CAT, "Honey pot with a drip, fed by a network line with two nodes",
      tags=["decoy", "bait", "trap", "deception", "lure attackers", "honeynet"])
def _(S):
    return [
        shell(rect(7, 2.5, 10, 3, _pick(S, 0.5, 1.5))),
        shell("M8 5.5C3 7 2.5 14 7.5 16.5H16.5C21.5 14 21 7 16 5.5"),
        detail("M9.5 5.5V10.5A1.5 1.5 0 0 0 12.5 10.5V5.5"),
        line(seg(6, 20.5, 18, 20.5)),
        dot(3.5, 20.5, 1.5), dot(20.5, 20.5, 1.5),
    ]


@icon("air-gap", CAT, "Two monitors linked by a cable with a gap in the middle",
      tags=["isolated network", "offline", "disconnected", "secure computer", "no network", "separation"])
def _(S):
    return [
        shell(rect(1.5, 3.5, 9, 8, _pick(S, 1, 2))),
        shell(rect(13.5, 3.5, 9, 8, _pick(S, 1, 2))),
        line("M6 11.5V18H9"),
        line("M18 11.5V18H15"),
        line(seg(9, 15.5, 9, 20.5)),
        line(seg(15, 15.5, 15, 20.5)),
    ]


@icon("vulnerability", CAT, "Shield with a jagged crack running down through it",
      tags=["weakness", "flaw", "exposed", "security hole", "broken shield", "risk"])
def _(S):
    return [shield(S), detail(poly([(12, 2.5), (13.5, 7), (10.5, 10.5), (13, 14), (11, 18)]))]


@icon("security-patch", CAT, "Shield with an adhesive bandage stuck diagonally across it",
      tags=["fix", "hotfix", "update", "bandage", "repair", "security update"])
def _(S):
    return [shield(S), detail(rrect(6.5, 9.25, 11, 5.5, -45, 12, 12, r=S.r * 0.3))]


@icon("penetration-test", CAT, "Shield with an arrow piercing through it",
      tags=["pentest", "ethical hacking", "red team", "arrow", "security test", "breach test"])
def _(S):
    return [
        shield(S),
        detail(seg(6, 6, 18, 18)),
        line(seg(2.5, 2.5, 6, 6)),
        line(seg(2, 5, 5, 2)),
        line(poly([(22, 17), (22, 22), (17, 22)], r=S.r)),
        line(seg(18, 18, 22, 22)),
    ]


@icon("threat-radar", CAT, "Round radar screen with a sweep line and a blip on the ring",
      tags=["threat detection", "monitoring", "scanner", "radar", "intrusion detection", "sweep"])
def _(S):
    return [
        shell(circle(12, 12, 9.5)),
        detail(circle(12, 12, 4.5)),
        detail(seg(12, 12, 18, 6)),
        dot(16.5, 14.5, 1.5),
    ]


@icon("threat-hunting", CAT, "Magnifying glass with a crosshair on its lens",
      tags=["hunt", "search for threats", "investigation", "target", "detect", "security analyst"])
def _(S):
    return [
        shell(circle(10, 10, 7.5)),
        line(seg(15.5, 15.5, 21.5, 21.5)),
        dot(10, 10, 1.25),
        detail(seg(10, 5.5, 10, 7.5)), detail(seg(10, 12.5, 10, 14.5)),
        detail(seg(5.5, 10, 7.5, 10)), detail(seg(12.5, 10, 14.5, 10)),
    ]


@icon("bug-bounty", CAT, "Beetle on top of a stack of coins",
      tags=["reward", "vulnerability reward", "coins", "payout", "bug", "hacker program"])
def _(S):
    return [
        shell(ellipse(12, 7, 3, 4)),
        line(seg(9, 6, 6, 4.5)), line(seg(15, 6, 18, 4.5)),
        line(seg(9, 9, 6, 10.5)), line(seg(15, 9, 18, 10.5)),
        shell("M4 16A8 2.5 0 0 1 20 16V20A8 2.5 0 0 1 4 20Z"),
        detail("M4 18A8 2.5 0 0 0 20 18"),
    ]


@icon("man-in-the-middle", CAT, "Two computers linked through a hooded figure in the middle",
      tags=["mitm", "interception", "eavesdropping", "hacker", "hooded", "wiretap"])
def _(S):
    return [
        shell(_pick(S, "M7.5 12V7.5A4.5 4.5 0 0 1 16.5 7.5V12Z", "M7.5 11.5V7.5A4.5 4.5 0 0 1 16.5 7.5V11.5Q16.5 12 16 12H8Q7.5 12 7.5 11.5Z")),
        dot(10.5, 8.5, 1), dot(13.5, 8.5, 1),
        shell(rect(1.5, 16, 7.5, 5.5, _pick(S, 0.5, 1.5))),
        shell(rect(15, 16, 7.5, 5.5, _pick(S, 0.5, 1.5))),
        line(seg(5.5, 16, 8.5, 12.5)), line(seg(18.5, 16, 15.5, 12.5)),
    ]


@icon("email-spoofing", CAT, "Envelope above a half face mask",
      tags=["fake sender", "impersonation", "forged email", "mask", "disguise", "fraud"])
def _(S):
    return [
        *envelope(S, 3, 2.5, 18, 9),
        shell("M3 15.5Q12 12.5 21 15.5V16.5Q21 20.5 17.5 20.5Q14.5 20.5 13.5 18.5Q12 17.5 10.5 18.5Q9.5 20.5 6.5 20.5Q3 20.5 3 16.5Z"),
        dot(7.5, 17.5, 1), dot(16.5, 17.5, 1),
    ]


@icon("malicious-usb", CAT, "USB flash drive with a skull on its body",
      tags=["infected usb", "flash drive", "skull", "malware", "badusb", "thumb drive"])
def _(S):
    return [
        shell(rect(8, 2, 8, 5.5, _pick(S, 0.5, 1.5))),
        shell(rect(5, 7.5, 14, 14.5, _pick(S, 1, 3))),
        detail("M8.5 18.5V14A3.5 3.5 0 0 1 15.5 14V18.5Z"),
        dot(10.5, 14, 1), dot(13.5, 14, 1),
    ]


@icon("juice-jacking", CAT, "Public charging port on a wall box with a cable plugged in and two dark eyes above",
      tags=["charging station", "usb charger hack", "public charger", "data theft", "airport charger", "cable"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 11, _pick(S, 1, 3))),
        detail(rect(8, 7.5, 8, 3, _pick(S, 0, 1))),
        dot(8.5, 5, 1), dot(15.5, 5, 1),
        line("M12 13.5V17Q12 20 15 20H17"),
        line(seg(17, 17.5, 17, 22)),
    ]


@icon("data-breach", CAT, "Database cylinder split by a jagged crack with bits spilling out",
      tags=["leak", "stolen data", "hacked database", "exposure", "binary", "security incident"])
def _(S):
    return [
        shell("M2 6A6.5 2.5 0 0 1 15 6V18A6.5 2.5 0 0 1 2 18Z"),
        detail(poly([(8.5, 3.5), (10, 9), (7, 13), (9.5, 17), (8, 20.5)], r=S.r)),
        dot(19, 7, 1.25), dot(20, 12, 1.25), dot(18.5, 17, 1.25),
    ]


@icon("data-exfiltration", CAT, "Database behind a wall with an arrow carrying data up and over it",
      tags=["data theft", "stolen data", "leak", "sneak out", "transfer", "wall"])
def _(S):
    return [
        shell("M1.5 11A3.5 1.5 0 0 1 8.5 11V19A3.5 1.5 0 0 1 1.5 19Z"),
        shell(rect(11, 10, 4, 11.5, _pick(S, 0, 1.5))),
        line("M5 8C5 2 19.5 2 19.5 12"),
        line(poly([(17, 10), (19.5, 12.5), (22, 10)], r=S.r * 0.3)),
    ]


@icon("privilege-escalation", CAT, "Figure on the top step of a staircase holding a key up",
      tags=["admin rights", "root access", "elevation", "permissions", "stairs", "promote"])
def _(S):
    return [
        shell(poly([(2, 21.5), (2, 18), (7, 18), (7, 14.5), (12, 14.5), (12, 11), (22, 11), (22, 21.5)], closed=True, r=S.r * 0.3)),
        shell(circle(17, 4.5, 2)) if S.name == "rounded" else shell(circle(17, 4.5, 2)),
        line(seg(17, 7, 17, 11)),
        line(seg(17, 8, 13.5, 5)),
        dot(12.5, 4, 1.25),
    ]


@icon("packet-sniffer", CAT, "Network line carrying packets with a magnifier over them",
      tags=["network analyzer", "traffic capture", "inspect packets", "eavesdrop", "monitor traffic"])
def _(S):
    return [
        line(seg(1.5, 20.5, 22.5, 20.5)),
        sq(2.5, 14.5, 4.5, 4.5, 0.5 if S.name == "rounded" else 0),
        sq(9.75, 14.5, 4.5, 4.5, 0.5 if S.name == "rounded" else 0),
        sq(17, 14.5, 4.5, 4.5, 0.5 if S.name == "rounded" else 0),
        shell(circle(11, 6.5, 4.25)),
        line(seg(14.2, 9.7, 17.5, 13)),
    ]


@icon("session-hijacking", CAT, "Cookie gripped from above by a clawed grabber",
      tags=["cookie theft", "account takeover", "stolen session", "claw", "grab", "web attack"])
def _(S):
    return [
        line(seg(4, 2.5, 20, 2.5)),
        line("M5 2.5V6.5C5 8.5 6.5 9.5 8.5 10"),
        line("M12 2.5V8.5"),
        line("M19 2.5V6.5C19 8.5 17.5 9.5 15.5 10"),
        shell(circle(12, 18, 4.5)),
        dot(10.5, 17, 0.9), dot(13.5, 17, 0.9), dot(12, 20, 0.9),
    ]


@icon("blocklist", CAT, "A banned symbol beside a list of entries",
      tags=["deny list", "blacklist", "banned", "blocked", "forbidden", "filter"], aliases=["deny-list"])
def _(S):
    return [
        shell(circle(7, 12, 5)),
        detail(seg(3.5, 15.5, 10.5, 8.5)),
        line(seg(15, 6, 22, 6)), line(seg(15, 12, 22, 12)), line(seg(15, 18, 22, 18)),
    ]


@icon("ad-blocker", CAT, "Browser window with an ad banner struck through",
      tags=["block ads", "advert", "popup blocker", "banner", "no ads", "browser extension"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, _pick(S, 1, 3))),
        detail(seg(2, 8, 22, 8)),
        detail(rect(5.5, 11, 13, 6, 0)),
        detail(seg(7, 17, 17, 11)),
    ]


@icon("onion-routing", CAT, "Onion bulb with layered rings and a route line through it",
      tags=["anonymous network", "layers", "anonymity", "relay", "private browsing"])
def _(S):
    return [
        shell("M12 2.5Q12.5 5.5 10 7C6 9 3.5 12 3.5 14.5C3.5 19 8 21.5 12 21.5C16 21.5 20.5 19 20.5 14.5C20.5 12 18 9 14 7Q11.5 5.5 12 2.5Z"),
        detail("M12 8C8 11 8 17 12 21"),
        detail("M12 8C16 11 16 17 12 21"),
    ]


@icon("dictionary-attack", CAT, "Open book with a key rising from its pages and speed lines",
      tags=["password guessing", "wordlist", "cracking", "book", "key", "hacking"])
def _(S):
    return [
        shell("M12 15C9 13.5 5.5 13.5 2.5 14.5V21C5.5 20 9 20 12 21.5C15 20 18.5 20 21.5 21V14.5C18.5 13.5 15 13.5 12 15Z"),
        detail(seg(12, 15, 12, 21.5)),
        shell(circle(12, 5.5, 3)),
        line(seg(12, 8.5, 12, 13)),
        line(seg(5.5, 4, 5.5, 8)), line(seg(18.5, 4, 18.5, 8)),
    ]


@icon("hardware-security-module", CAT, "Flat rack-mounted box with status lights and a key on its front",
      tags=["hsm", "key storage", "crypto appliance", "rack server", "secure vault", "encryption hardware"])
def _(S):
    return [
        shell(rect(2, 5.5, 20, 13, _pick(S, 1, 3))),
        dot(5.75, 10, 1), dot(5.75, 14, 1),
        detail(circle(11.5, 12, 2.25)),
        detail(seg(13.75, 12, 19, 12)),
        detail(seg(17, 12, 17, 14.5)),
    ]


@icon("passkey", CAT, "Person silhouette with a key at its lower right",
      tags=["passwordless", "webauthn", "sign in", "login key", "fido", "credential"])
def _(S):
    return [
        shell(circle(9, 7, 3.5)),
        line(poly([(2.5, 20.5), (2.5, 18), (5, 14.5), (9, 13.75), (11, 14.25)], r=S.r)),
        shell(circle(17.5, 13.5, 2.75)),
        line(seg(17.5, 16.25, 17.5, 22)),
        line(seg(17.5, 18.5, 20.5, 18.5)), line(seg(17.5, 21, 20, 21)),
    ]


@icon("magic-link", CAT, "Envelope with a chain link on its front and a sparkle at the corner",
      tags=["passwordless login", "email link", "sign in link", "one click", "url", "chain"])
def _(S):
    return [
        shell(rect(2, 7, 15, 13, _pick(S, 1, 3))),
        detail("M9 11.5H7.5A2.25 2.25 0 0 0 7.5 16H9"),
        detail("M10 11.5H11.5A2.25 2.25 0 0 1 11.5 16H10"),
        solid(poly([(19.5, 1.8), (20.6, 4.4), (23.2, 5.5), (20.6, 6.6), (19.5, 9.2), (18.4, 6.6), (15.8, 5.5), (18.4, 4.4)], closed=True)),
    ]


@icon("password-generator", CAT, "Six-sided die with a pip on its top face and a curved arrow beside it",
      tags=["random password", "dice", "randomizer", "generate", "secret", "strong password"])
def _(S):
    cx, cy, r = 10.5, 12.5, 8.5
    v = [polar(cx, cy, r, -90 + 60 * i) for i in range(6)]
    return [
        shell(poly(v, closed=True, r=S.r)),
        detail(poly([v[5], (cx, cy), v[1]], r=S.r * 0.3)),
        detail(seg(cx, cy, *v[3])),
        dot(cx, cy - 4.25, 1.1),
        line("M20 8.5Q23 12.5 20 16.5"),
        line(poly([(22, 15.5), (20, 16.8), (18.5, 14.8)], r=S.r * 0.3)),
    ]


@icon("voice-id", CAT, "Sound waveform of vertical bars inside four corner scan brackets",
      tags=["voiceprint", "speaker recognition", "voice recognition", "biometric", "audio", "speech"])
def _(S):
    return [
        *brackets(S, 2.5, 2.5, 21.5, 21.5, 4),
        line(seg(7, 10.5, 7, 13.5)), line(seg(10.3, 8, 10.3, 16)), line(seg(13.7, 6.5, 13.7, 17.5)), line(seg(17, 9.5, 17, 14.5)),
    ]


@icon("palm-scan", CAT, "Open palm with a scan line across it inside corner brackets",
      tags=["palm vein", "hand biometric", "hand recognition", "palm reader", "biometric", "hand"])
def _(S):
    return [
        *brackets(S, 1.5, 1.5, 22.5, 22.5, 3.5),
        shell(rect(6.5, 11.5, 11, 8, _pick(S, 1, 3))),
        line(seg(7.5, 5.5, 7.5, 11.5)), line(seg(10.5, 4.5, 10.5, 11.5)), line(seg(13.5, 4.5, 13.5, 11.5)), line(seg(16.5, 5.5, 16.5, 11.5)),
        detail(seg(6.5, 15.5, 17.5, 15.5)),
    ]


@icon("hardware-security-key", CAT, "USB security key from above: connector, round touch button and keyring hole",
      tags=["security key", "usb key", "fido2", "usb token", "u2f", "two factor"])
def _(S):
    return [
        line(poly([(7, 9), (2.5, 9), (2.5, 15), (7, 15)])),
        shell(rect(7, 6, 15, 12, _pick(S, 1, 4))),
        detail(circle(12.5, 12, 2)),
        dot(18.5, 12, 1.25),
    ]


@icon("backup-codes", CAT, "Sheet with two columns of short dashed codes and a small key at its top",
      tags=["recovery codes", "one time codes", "2fa backup", "emergency access", "printout", "codes list"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, _pick(S, 1, 3))),
        detail(circle(7, 6.5, 1.25)),
        detail(seg(8.5, 6.5, 13, 6.5)),
        detail(seg(6.5, 11, 10, 11)), detail(seg(14, 11, 17.5, 11)),
        detail(seg(6.5, 14.5, 10, 14.5)), detail(seg(14, 14.5, 17.5, 14.5)),
        detail(seg(6.5, 18, 10, 18)), detail(seg(14, 18, 17.5, 18)),
    ]


@icon("security-token-fob", CAT, "Keychain token with a small display window, button and key ring loop",
      tags=["otp token", "token", "hardware token", "keychain", "one time password", "authenticator"])
def _(S):
    return [
        line("M9.5 7.5V5.5A2.5 2.5 0 0 1 14.5 5.5V7.5"),
        shell(rect(5.5, 7.5, 13, 14.5, _pick(S, 1, 4))),
        detail(rect(8.5, 10.5, 7, 4, 0)),
        dot(12, 18.5, 1.25),
    ]


@icon("push-authentication", CAT, "Smartphone with a notification card above a check button and a cross button",
      tags=["approve login", "mfa prompt", "approve deny", "phone approval", "two factor", "notification"])
def _(S):
    return [
        shell(rect(5.5, 2, 13, 20, _pick(S, 1.5, 3.5))),
        detail(seg(8.5, 6, 15.5, 6)), detail(seg(8.5, 9.5, 13.5, 9.5)),
        detail(poly([(8.3, 16.8), (9.6, 18.1), (11.6, 15.5)])),
        detail(seg(13.3, 15.6, 15.7, 18.2)), detail(seg(15.7, 15.6, 13.3, 18.2)),
    ]


@icon("access-key-fob", CAT, "Teardrop key fob with a ring hole and three contactless wave arcs",
      tags=["proximity fob", "rfid fob", "keyless entry", "tap to enter", "nfc", "door fob"])
def _(S):
    return [
        shell(_pick(S, "M12 2.5L9 7L4.8 14C3.8 17.5 7 21.5 12 21.5C17 21.5 20.2 17.5 19.2 14L15 7Z",
                    "M12 2.5C10.3 2.5 9.3 3.6 8.7 5L4.8 14C3.8 17.5 7 21.5 12 21.5C17 21.5 20.2 17.5 19.2 14L15.3 5C14.7 3.6 13.7 2.5 12 2.5Z")),
        dot(12, 5.75, 1.1),
        detail(arc(8, 15.5, 3, -50, 50)),
        detail(arc(8, 15.5, 6.25, -45, 45)),
    ]


@icon("biometric-padlock", CAT, "Padlock with a fingerprint whorl on its body instead of a keyhole",
      tags=["fingerprint lock", "smart lock", "biometric lock", "touch unlock", "secure", "fingerprint padlock"])
def _(S):
    return [
        line("M7.5 10V7A4.5 4.5 0 0 1 16.5 7V10"),
        shell(rect(3.5, 10, 17, 12, _pick(S, 1, 3.5))),
        detail("M9 20V17A3 3 0 0 1 15 17V20"),
        dot(12, 17.75, 1),
    ]


@icon("fingerprint-terminal", CAT, "Wall reader with a small screen above a fingerprint pad",
      tags=["time clock", "biometric reader", "door reader", "scanner", "attendance", "access control"])
def _(S):
    return [
        shell(rect(4.5, 2, 15, 20, _pick(S, 1.5, 4))),
        detail(rect(7.5, 5, 9, 4, 0)),
        detail("M9 19V16.5A3 3 0 0 1 15 16.5V19"),
        dot(12, 17.25, 0.9),
    ]


@icon("access-card-reader", CAT, "Wall card reader with a card held to it and contactless wave arcs between",
      tags=["badge reader", "tap card", "rfid reader", "door access", "swipe card", "contactless"])
def _(S):
    return [
        shell(rect(2, 3, 8, 18, _pick(S, 1, 3))),
        dot(6, 7, 1),
        line(arc(10, 12, 3.75, -45, 45)),
        line(arc(10, 12, 6.25, -40, 40)),
        shell(rect(16.5, 7, 5.5, 10, _pick(S, 0.5, 1.5))),
    ]


@icon("identity-verification", CAT, "ID card beside a face inside scan brackets",
      tags=["kyc", "verify identity", "id check", "face match", "selfie check", "document check"])
def _(S):
    return [
        shell(rect(1.5, 6.5, 10, 11, _pick(S, 1, 2.5))),
        dot(6.5, 10.75, 1.25),
        detail(seg(4, 14.5, 9, 14.5)),
        *brackets(S, 14, 5.5, 22.5, 18.5, 2.5),
        line(seg(16.5, 10.5, 16.5, 12)), line(seg(20, 10.5, 20, 12)),
        line(poly([(16.5, 15), (18.25, 16), (20, 15)], r=S.r * 0.5)),
    ]


@icon("id-card-scan", CAT, "ID card with photo and lines framed by camera scan brackets",
      tags=["scan id", "document scan", "capture id", "kyc", "driving licence", "camera frame"])
def _(S):
    return [
        *brackets(S, 1.5, 2.5, 22.5, 21.5, 4),
        shell(rect(5.5, 7.5, 13, 9, _pick(S, 1, 2))),
        dot(9, 11, 1.1),
        detail(seg(12.5, 10.5, 16, 10.5)), detail(seg(12.5, 13.5, 16, 13.5)),
    ]


@icon("age-verification", CAT, "ID card with a photo mark and the number 18",
      tags=["age check", "over 18", "adult", "legal age", "id check", "restricted"])
def _(S):
    return [
        shell(rect(1.5, 4.5, 21, 15, _pick(S, 1, 3))),
        dot(6, 10, 1.25),
        detail(seg(4, 15, 8, 15)),
        detail(seg(11, 9, 11, 15)),
        detail(seg(9.5, 10.5, 11, 9)),
        detail(rect(14, 9, 5, 6, 0)),
        detail(seg(14, 12, 19, 12)),
    ]


@icon("account-recovery", CAT, "Life ring buoy with a person in its centre",
      tags=["regain access", "lifebuoy", "reset account", "rescue", "locked out", "restore"])
def _(S):
    k = 0.7071
    ro = 9.5 if S.name == "line" else 9.75
    ri = 4.75 if S.name == "line" else 5
    return [
        shell(circle(12, 12, ro)),
        detail(circle(12, 12, ri)),
        detail(seg(12 + ri * k, 12 + ri * k, 12 + ro * k, 12 + ro * k)),
        detail(seg(12 - ri * k, 12 + ri * k, 12 - ro * k, 12 + ro * k)),
        detail(seg(12 + ri * k, 12 - ri * k, 12 + ro * k, 12 - ro * k)),
        detail(seg(12 - ri * k, 12 - ri * k, 12 - ro * k, 12 - ro * k)),
        dot(12, 10.5, 1.2),
        dot(12, 13.75, 1.2),
    ]


@icon("key-switch", CAT, "Round panel switch with a key in its centre and two position marks",
      tags=["key lock switch", "ignition", "keyed switch", "turn key", "panel", "on off key"])
def _(S):
    return [
        shell(circle(12, 12, 9.5)),
        detail(rect(9, 7.5, 6, 3.5, _pick(S, 0, 1.5))),
        detail(seg(12, 11, 12, 17)),
        dot(5.5, 12, 1), dot(18.5, 12, 1),
    ]


@icon("door-release-button", CAT, "Wall plate with a large round push button and a small doorway above it",
      tags=["exit button", "request to exit", "push to exit", "door opener", "access control", "buzzer"])
def _(S):
    return [
        shell(rect(4, 2, 16, 20, _pick(S, 1, 4))),
        detail(poly([(9, 10), (9, 5), (15, 5), (15, 10)])),
        detail(circle(12, 15.5, 3.25)),
    ]


@icon("full-height-turnstile", CAT, "Tall revolving turnstile cage with a central post and bars between fixed grilles",
      tags=["revolving gate", "security gate", "access gate", "entry control", "cage turnstile", "barrier"])
def _(S):
    return [
        line(seg(2, 2.5, 22, 2.5)), line(seg(2, 21.5, 22, 21.5)),
        line(seg(2.5, 2.5, 2.5, 21.5)), line(seg(21.5, 2.5, 21.5, 21.5)),
        line(seg(12, 2.5, 12, 21.5)),
        line(seg(5, 8, 12, 6.5)), line(seg(19, 8, 12, 6.5)),
        line(seg(5, 13.5, 19, 13.5)),
        line(seg(5, 19, 12, 17.5)), line(seg(19, 19, 12, 17.5)),
    ]


@icon("cipher-wheel", CAT, "Two concentric rings with tick marks between them and a pin in the centre",
      tags=["cipher disk", "decoder ring", "caesar", "encryption wheel", "secret code", "rotating rings"])
def _(S):
    parts = [shell(circle(12, 12, 9.75)), detail(circle(12, 12, 5))]
    for i in range(12):
        a = math.radians(i * 30)
        parts.append(detail(seg(12 + 6.6 * math.cos(a), 12 + 6.6 * math.sin(a), 12 + 8.1 * math.cos(a), 12 + 8.1 * math.sin(a))))
    parts.append(dot(12, 12, 1.25))
    return parts


@icon("rotor-cipher-machine", CAT, "Boxy cipher machine with three rotors on top and keys on the front",
      tags=["code machine", "wartime cipher", "rotors", "encryption machine", "vintage crypto"])
def _(S):
    return [
        line(poly([(4.5, 9), (4.5, 3.5), (8.5, 3.5), (8.5, 9)])),
        line(poly([(10, 9), (10, 3.5), (14, 3.5), (14, 9)])),
        line(poly([(15.5, 9), (15.5, 3.5), (19.5, 3.5), (19.5, 9)])),
        shell(rect(2, 9, 20, 12.5, _pick(S, 1, 3))),
        dot(6, 13.25, 1), dot(10, 13.25, 1), dot(14, 13.25, 1), dot(18, 13.25, 1),
        dot(8, 17.5, 1), dot(12, 17.5, 1), dot(16, 17.5, 1),
    ]


@icon("scytale", CAT, "Rod with a paper strip wound around it in a slanted spiral",
      tags=["ancient cipher", "spartan", "transposition", "strip", "wrapped message", "rod cipher"])
def _(S):
    return [
        shell(rect(2, 6.5, 20, 11, _pick(S, 1, 4))),
        detail(seg(6.5, 6.5, 9.5, 17.5)),
        detail(seg(12.5, 6.5, 15.5, 17.5)),
        dot(11, 10, 0.9),
        dot(17, 14, 0.9),
    ]


@icon("key-exchange", CAT, "Two keys facing each other with arrows passing between them",
      tags=["diffie hellman", "key swap", "public key exchange", "handshake", "secure channel", "share keys"])
def _(S):
    return [
        shell(circle(5, 5, 2.75)),
        line(seg(7.75, 5, 14.5, 5)), line(seg(12.5, 5, 12.5, 7.5)),
        shell(circle(19, 19, 2.75)),
        line(seg(16.25, 19, 9.5, 19)), line(seg(11.5, 19, 11.5, 16.5)),
        line(seg(4, 10.5, 19, 10.5)),
        line(poly([(16.5, 8.5), (19, 10.5), (16.5, 12.5)], r=S.r * 0.3)),
        line(seg(20, 13.5, 5, 13.5)),
        line(poly([(7.5, 11.5), (5, 13.5), (7.5, 15.5)], r=S.r * 0.3)),
    ]


@icon("end-to-end-encryption", CAT, "Chat bubble with a padlock inside and a dot at each end of its line",
      tags=["e2ee", "secure messaging", "private chat", "encrypted chat", "messenger", "lock"])
def _(S):
    return [
        shell(poly([(3, 3), (21, 3), (21, 16.5), (10, 16.5), (5.5, 20.5), (5.5, 16.5), (3, 16.5)], closed=True, r=S.r)),
        detail(rect(9, 9.5, 6, 4.5, _pick(S, 0, 1))),
        detail("M10.5 9.5V8.5A1.5 1.5 0 0 1 13.5 8.5V9.5"),
    ]


@icon("certificate-chain", CAT, "Three small certificates stepping down a diagonal and linked together",
      tags=["trust chain", "ssl chain", "root certificate", "intermediate certificate", "pki", "tls"])
def _(S):
    return [
        shell(rect(1.5, 2, 10, 5.5, _pick(S, 0.5, 2))),
        shell(rect(7, 9.25, 10, 5.5, _pick(S, 0.5, 2))),
        shell(rect(12.5, 16.5, 10, 5.5, _pick(S, 0.5, 2))),
        line(seg(8.5, 7.5, 8.5, 9.25)), line(seg(14, 14.75, 14, 16.5)),
        dot(4.5, 4.75, 0.9),
    ]


@icon("invisible-ink", CAT, "Sheet with faint dotted lines and a small flame under its corner revealing solid text",
      tags=["secret message", "hidden writing", "lemon juice", "heat reveal", "spy paper", "concealed text"])
def _(S):
    return [
        shell(rect(3, 2.5, 12, 17.5, _pick(S, 0.5, 2.5))),
        dot(6.5, 6.5, 0.9), dot(9, 6.5, 0.9), dot(11.5, 6.5, 0.9),
        dot(6.5, 10, 0.9), dot(9, 10, 0.9), dot(11.5, 10, 0.9),
        detail(seg(6, 14, 12, 14)), detail(seg(6, 17, 10, 17)),
        shell("M19 12C19.5 14.5 22 15.5 22 18A3 3 0 0 1 16 18C16 16.5 17 15.5 17.5 14.5C18 15.5 18.5 15.5 18.5 14.5C18.5 13.5 19 13 19 12Z"),
    ]


@icon("steganography", CAT, "Picture with mountains and sun and a magnifier over its corner revealing text lines",
      tags=["hidden data", "image hiding", "concealed message", "watermark", "covert", "image secret"])
def _(S):
    return [
        shell(rect(2, 3, 14, 12, _pick(S, 0.5, 2.5))),
        line(poly([(4.5, 13), (8, 8.5), (10.5, 11.5), (12.5, 9.5)], r=S.r * 0.5)),
        dot(12.5, 6, 1.1),
        shell(circle(16.5, 16.5, 4.5)),
        line(seg(19.8, 19.8, 22, 22)),
        detail(seg(14.5, 16.5, 18.5, 16.5)),
    ]


@icon("one-time-pad", CAT, "Tear-off notepad with a torn top edge and rows of short code groups",
      tags=["otp pad", "unbreakable cipher", "code pad", "spy notepad", "random key pad", "cipher pad"])
def _(S):
    return [
        shell(poly([(4, 21.5), (4, 5), (6.5, 3.5), (9, 5), (11.5, 3.5), (14, 5), (16.5, 3.5), (20, 5), (20, 21.5)], closed=True, r=S.r * 0.3)),
        detail(seg(7, 10.5, 11, 10.5)), detail(seg(13.5, 10.5, 17, 10.5)),
        detail(seg(7, 14.5, 11, 14.5)), detail(seg(13.5, 14.5, 17, 14.5)),
        detail(seg(7, 18.5, 11, 18.5)), detail(seg(13.5, 18.5, 17, 18.5)),
    ]


@icon("split-key", CAT, "Key broken into three separate pieces laid along a diagonal",
      tags=["key shards", "shamir", "secret sharing", "broken key", "key fragments", "multi party"])
def _(S):
    u = 0.7071

    def at(t, off=0.0):
        return (12 + t * u - off * u, 12 + t * u + off * u)
    c = at(-11.2)
    return [
        shell(circle(c[0], c[1], 2.75)),
        line(seg(*at(-8.4), *at(-6.8))),
        line(seg(*at(-3.5), *at(1))), line(seg(*at(-1.2), *at(-1.2, 3))),
        line(seg(*at(5), *at(11.5))), line(seg(*at(8), *at(8, 3))), line(seg(*at(11.5), *at(11.5, 3))),
    ]


@icon("face-blur", CAT, "Head and shoulders with the face filled by a checker of square pixels",
      tags=["pixelate face", "anonymize", "hide identity", "censor face", "privacy filter", "blurred person"])
def _(S):
    r = 0.5 if S.name == "rounded" else 0
    return [
        shell(circle(12, 8, 5.5)),
        line(poly([(3.5, 22), (3.5, 21), (6, 17.5), (12, 16.5), (18, 17.5), (20.5, 21), (20.5, 22)], r=S.r)),
        sq(8.9, 4.9, 2.2, 2.2, r), sq(13.1, 4.9, 2.2, 2.2, r), sq(11, 7, 2.2, 2.2, r),
        sq(8.9, 9.1, 2.2, 2.2, r), sq(13.1, 9.1, 2.2, 2.2, r),
    ]


@icon("redacted-document", CAT, "Document page with text lines, two of them replaced by thick solid bars",
      tags=["censored", "blacked out", "classified", "confidential", "sensitive text", "foia"])
def _(S):
    r = 0.5 if S.name == "rounded" else 0
    return [
        shell(rect(4, 2, 16, 20, _pick(S, 1, 3))),
        detail(seg(7.5, 5.5, 16.5, 5.5)),
        sq(7.5, 8.5, 9, 3.25, r),
        detail(seg(7.5, 15, 13.5, 15)),
        sq(7.5, 17.5, 9, 3, r),
    ]


@icon("data-masking", CAT, "Input field showing four bullet characters followed by plain characters",
      tags=["hidden digits", "partial number", "obscured card number", "asterisks", "mask input", "tokenize"])
def _(S):
    return [
        shell(rect(1.5, 6.5, 21, 11, _pick(S, 1, 4))),
        dot(5, 12, 1), dot(8, 12, 1), dot(11, 12, 1), dot(14, 12, 1),
        detail(seg(17.5, 9.5, 17.5, 14.5)), detail(seg(20, 9.5, 20, 14.5)),
    ]


@icon("privacy-screen", CAT, "Laptop whose screen is covered in vertical louver lines",
      tags=["privacy filter", "anti snoop", "shoulder surfing", "screen protector", "louvers", "blackout screen"])
def _(S):
    return [
        shell(rect(3, 3, 18, 13, _pick(S, 1, 3))),
        detail(seg(8, 6.5, 8, 12.5)), detail(seg(12, 6.5, 12, 12.5)), detail(seg(16, 6.5, 16, 12.5)),
        line(seg(1.5, 19.5, 22.5, 19.5)),
    ]


@icon("webcam-cover", CAT, "Laptop camera lens half covered by a small sliding shutter",
      tags=["camera cover", "webcam shutter", "spy protection", "slider", "laptop camera", "block camera"])
def _(S):
    return [
        shell(rect(2, 5.5, 20, 11, _pick(S, 1, 4))),
        detail(circle(8.5, 11, 2.25)),
        detail(rect(10.5, 8.25, 8, 5.5, 2.5 if S.name == "rounded" else 0.5)),
        line(seg(4, 20.5, 20, 20.5)),
    ]


@icon("faraday-pouch", CAT, "Phone poking out of a pouch beside signal arcs crossed by a slash",
      tags=["signal blocking bag", "faraday bag", "shield phone", "no signal", "rf blocking", "forensic bag"])
def _(S):
    return [
        line(poly([(3.5, 12.5), (3.5, 2.5), (11, 2.5), (11, 12.5)], r=S.r)),
        shell(rect(1.5, 12.5, 21, 9, _pick(S, 1, 3))),
        detail(seg(1.5, 16, 22.5, 16)),
        line(arc(13, 7.5, 3.25, -45, 45)),
        line(arc(13, 7.5, 6.5, -45, 45)),
        line(seg(14.5, 3.5, 21, 10)),
    ]


@icon("signal-jammer", CAT, "Small box with four antennas and a zigzag line above it",
      tags=["jamming", "radio blocker", "cell blocker", "interference", "rf jammer", "antenna box"])
def _(S):
    return [
        shell(rect(3.5, 14, 17, 7.5, _pick(S, 1, 3))),
        line(seg(6.5, 14, 4.5, 8)), line(seg(9.5, 14, 9.5, 8)), line(seg(14.5, 14, 14.5, 8)), line(seg(17.5, 14, 19.5, 8)),
        line(poly([(7, 4.5), (9.5, 2.5), (12, 4.5), (14.5, 2.5), (17, 4.5)], r=S.r * 0.3)),
        dot(8, 17.75, 1), dot(12, 17.75, 1),
    ]


@icon("rfid-blocking-wallet", CAT, "Wallet with a card slot line and a small shield on its front",
      tags=["rfid protection", "card skimming", "anti theft wallet", "contactless blocker", "shield wallet", "nfc blocking"])
def _(S):
    return [
        shell(rect(2, 5.5, 20, 15, _pick(S, 1, 3.5))),
        detail(seg(2, 9.5, 22, 9.5)),
        detail("M11 12L14.5 13.2V15.5C14.5 17.4 13 18.5 11 19.3C9 18.5 7.5 17.4 7.5 15.5V13.2Z"),
        dot(18.5, 15.5, 1),
    ]


@icon("tracking-cookie", CAT, "Cookie with chips and a small open eye in its middle",
      tags=["web tracker", "third party cookie", "ad tracking", "watching", "browser cookie", "surveillance"])
def _(S):
    r = 0.4 if S.name == "rounded" else 0
    return [
        shell(circle(12, 12, 9.75)),
        detail(_pick(S, "M7.5 12C9 9.75 15 9.75 16.5 12C15 14.25 9 14.25 7.5 12Z",
                     "M7.7 11.5C9.2 9.75 14.8 9.75 16.3 11.5Q16.6 12 16.3 12.5C14.8 14.25 9.2 14.25 7.7 12.5Q7.4 12 7.7 11.5Z")),
        sq(6, 6, 2, 2, r), sq(16, 5.5, 2, 2, r), sq(16.5, 16.5, 2, 2, r), sq(5.5, 16, 2, 2, r),
    ]


@icon("location-tracking", CAT, "Map pin with an eye in its head and a dotted trail behind it",
      tags=["gps tracking", "being watched", "geolocation", "follow location", "surveillance", "pin eye"])
def _(S):
    return [
        shell(_pick(S, "M14.5 21.5L8 14.5A7.25 7.25 0 1 1 21 14.5Z", "M14.5 21.5C14.5 21.5 7.5 15 7.5 10A7 7 0 0 1 21.5 10C21.5 15 14.5 21.5 14.5 21.5Z")),
        detail("M11 10C12.3 8 16.7 8 18 10C16.7 12 12.3 12 11 10Z"),
        dot(14.5, 10, 0.9),
        dot(2.5, 21, 1), dot(6, 21, 1),
    ]


@icon("app-permissions", CAT, "Dialog box with a small camera at the top and two buttons below",
      tags=["permission prompt", "allow camera", "access request", "consent dialog", "allow deny", "mobile privacy"])
def _(S):
    r = 0.5 if S.name == "rounded" else 0
    return [
        shell(rect(3, 2.5, 18, 19, _pick(S, 1.5, 4))),
        detail(rect(8.5, 6, 7, 5, _pick(S, 0, 1))),
        dot(12, 8.5, 1),
        sq(6, 15, 7.5, 3.5, r), sq(15.5, 15, 2.75, 3.5, r),
    ]


@icon("data-protection", CAT, "Database cylinder with a shield at its lower right",
      tags=["secure data", "protected database", "backup safe", "gdpr", "data security", "storage shield"])
def _(S):
    return [
        shell("M1.5 5.5A5.5 2.5 0 0 1 12.5 5.5V11.5A5.5 2.5 0 0 1 1.5 11.5Z"),
        detail("M1.5 8.5A5.5 2.5 0 0 0 12.5 8.5"),
        shell(_pick(S, "M16.5 9.5L22 11.7V15.5C22 18.5 19.8 20.6 16.5 22C13.2 20.6 11 18.5 11 15.5V11.7Z",
                    "M16.5 9.5L21 11.2Q22 11.6 22 12.7V15.5C22 18.5 19.8 20.6 16.5 22C13.2 20.6 11 18.5 11 15.5V12.7Q11 11.6 12 11.2Z")),
    ]


@icon("digital-footprint", CAT, "Bare footprint with a row of toes and a few pixels trailing behind the heel",
      tags=["online trail", "data trail", "web history", "pixel foot", "activity trace", "internet traces"])
def _(S):
    r = 0.5 if S.name == "rounded" else 0
    return [
        shell("M10 10C7.5 10 6.5 12 6.5 14C6.5 16 8 17 8.5 18.5C9 20.5 10 21.5 12 21.5C14.5 21.5 15.5 20 15 18C14.5 16 16.5 15 16.5 13C16.5 10.5 14.5 9.5 13 9.5Z"),
        dot(7.5, 7, 1.3), dot(11, 5, 1.3), dot(14.5, 5.5, 1.3), dot(17.5, 8, 1.3),
        *([dot(20, 16.5, 1), dot(20.5, 20.5, 1)] if S.name == "rounded" else [sq(19, 15.5, 2, 2), sq(19.5, 19.5, 2, 2)]),
    ]


@icon("data-erasure", CAT, "Person silhouette whose lower half is being rubbed out by an eraser with crumbs falling",
      tags=["wipe data", "delete profile", "right to be forgotten", "eraser", "remove identity", "clean up"])
def _(S):
    return [
        shell(circle(12, 4.75, 2.75)),
        shell("M5 15A7 5.5 0 0 1 19 15Z"),
        shell(rcen(12, 19.25, 10, 4, -12, r=S.r * 0.5)),
        dot(4.25, 18.5, 1), dot(20.25, 18, 1), dot(19, 22, 0.9),
    ]


@icon("disappearing-message", CAT, "Chat bubble whose right side dissolves into dots, with a small timer at its corner",
      tags=["self destruct", "vanishing chat", "ephemeral", "timed message", "auto delete", "timer"])
def _(S):
    return [
        line(poly([(12, 3.5), (6, 3.5), (3, 6.5), (3, 12), (6, 15), (8, 15), (8, 19), (11, 15.5), (12, 15)], r=S.r)),
        dot(15.5, 4.5, 1), dot(19, 7, 1), dot(15, 9, 1), dot(20, 11, 1),
        shell(circle(17.5, 18, 3.5)),
        dot(17.5, 18, 0.8),
        line(seg(17.5, 14.5, 17.5, 13.5)),
    ]


@icon("drive-destruction", CAT, "Hard drive with a hammer striking its top and a crack across its face",
      tags=["destroy disk", "smash hard drive", "data destruction", "physical wipe", "hammer", "sanitize media"])
def _(S):
    return [
        line(seg(2.5, 2.5, 6.5, 6.5)),
        shell(rcen(9, 7, 8, 4.5, -45, r=S.r * 0.5)),
        shell(rect(3, 12.5, 18, 9, _pick(S, 1, 3))),
        detail(poly([(11, 12.5), (12.5, 16), (10, 18), (12, 21.5)], r=S.r * 0.5)),
        dot(17.5, 18.5, 1),
    ]


@icon("secure-shredding-bin", CAT, "Locked wheelie bin with a document slot in its lid and a padlock on the front",
      tags=["confidential waste", "shred bin", "document disposal", "locked bin", "secure disposal", "office shredding"])
def _(S):
    return [
        shell(rect(4, 2, 16, 4.5, _pick(S, 0.5, 2))),
        detail(seg(8.5, 4.25, 15.5, 4.25)),
        shell(poly([(5.5, 6.5), (18.5, 6.5), (17.25, 19.5), (6.75, 19.5)], closed=True, r=S.r * 0.5)),
        detail(rect(9.25, 12.5, 5.5, 4, _pick(S, 0, 1))),
        detail("M10.5 12.5V11A1.5 1.5 0 0 1 13.5 11V12.5"),
        dot(8, 21.25, 1.1), dot(16, 21.25, 1.1),
    ]


@icon("parental-control", CAT, "Small child figure standing in front of a large shield",
      tags=["child safety", "kids protection", "family filter", "content controls", "guardian", "safe kids"])
def _(S):
    return [
        shell(_pick(S, "M12 2.5L20 5.5V11C20 16 16.6 19.8 12 21.5C7.4 19.8 4 16 4 11V5.5Z",
                    "M10.95 2.9L5.05 5.1Q4 5.5 4 6.6V11C4 16 7.4 19.8 12 21.5C16.6 19.8 20 16 20 11V6.6Q20 5.5 18.95 5.1L13.05 2.9Q12 2.5 10.95 2.9Z")),
        dot(12, 8.5, 1.9),
        Part("dot", poly([(8.75, 17.5), (10, 12), (14, 12), (15.25, 17.5)], closed=True)),
    ]


@icon("item-tracker-tag", CAT, "Small rounded tag on a key ring with a key and signal arcs above",
      tags=["bluetooth tracker", "find my keys", "lost item", "locator tag", "keychain tracker", "tag"])
def _(S):
    return [
        line(arc(8.5, 10, 3.5, -130, -50)),
        line(arc(8.5, 10, 7, -130, -50)),
        shell(rect(4.5, 10, 8, 8, _pick(S, 1, 3))),
        dot(7.5, 13, 0.9),
        shell(circle(16.5, 15, 3)),
        line(seg(19.5, 15, 22.5, 15)), line(seg(21.5, 15, 21.5, 17.5)),
    ]
