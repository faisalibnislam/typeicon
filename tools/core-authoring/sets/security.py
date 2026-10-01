"""TypeIcon Core: security & privacy."""
import math

from dsl import (  # noqa: F401
    LINE, ROUNDED, arc, circle, detail, dot, ellipse, filled_region, icon, line, poly, pt_on, rect, regular, seg, shell, solid,
)
from geometry import D, P, ST, U, fmt, path_to_d

CAT = "security"


def _pick(S, sharp, soft):
    return sharp if S.name == "line" else soft


# --------------------------------------------------------------------------- shared shapes

_SHIELD = "M12 2.5L20 5.5V11C20 16 16.6 19.8 12 21.5C7.4 19.8 4 16 4 11V5.5Z"
_SHIELD_ROUND = ("M10.95 2.9L5.05 5.1Q4 5.5 4 6.6V11C4 16 7.4 19.8 12 21.5C16.6 19.8 20 16 20 11V6.6"
                 "Q20 5.5 18.95 5.1L13.05 2.9Q12 2.5 10.95 2.9Z")


def _shield(S):
    return shell(_pick(S, _SHIELD, _SHIELD_ROUND))


_EYE = "M2 12C4.5 7 8 5 12 5C16 5 19.5 7 22 12C19.5 17 16 19 12 19C8 19 4.5 17 2 12Z"
_EYE_ROUND = ("M2.7 11.2C5 7.2 8.3 5 12 5C15.7 5 19 7.2 21.3 11.2Q21.8 12 21.3 12.8"
              "C19 16.8 15.7 19 12 19C8.3 19 5 16.8 2.7 12.8Q2.2 12 2.7 11.2Z")


def _brackets(S, inset=3.0, arm=4.5):
    """Four corner brackets of a scanning frame."""
    a, b = inset, 24 - inset
    return [line(poly(pts, r=S.r)) for pts in (
        [(a, a + arm), (a, a), (a + arm, a)], [(b - arm, a), (b, a), (b, a + arm)],
        [(a, b - arm), (a, b), (a + arm, b)], [(b - arm, b), (b, b), (b, b - arm)])]


# =========================================================================== shields

@icon("shield-check", CAT, "Shield with a check mark; protected or secure",
      tags=["protected", "secure", "safe", "verified", "security", "antivirus"], aliases=["shield-ok"])
def _(S):
    return [_shield(S), detail(poly([(8.5, 11.5), (11, 14), (15.5, 9)], r=S.r * 0.5))]


@icon("shield-lock", CAT, "Shield with a padlock; locked-down protection",
      tags=["protection", "locked", "secure", "encryption", "privacy", "security"])
def _(S):
    return [_shield(S), detail(rect(8.75, 10.5, 6.5, 5.5, _pick(S, 0.5, 1.5))),
            detail("M10.25 10.5V9A1.75 1.75 0 0 1 13.75 9V10.5")]


@icon("shield-x", CAT, "Shield with a cross; unprotected or threat blocked",
      tags=["unprotected", "blocked", "threat", "insecure", "security", "denied"])
def _(S):
    return [_shield(S), detail(seg(9.5, 8.5, 14.5, 13.5)), detail(seg(14.5, 8.5, 9.5, 13.5))]


# =========================================================================== biometrics

def _fingerprint(S, cx=12.0, cy=11.0):
    return [
        line(f"M{fmt(cx - 9)} {fmt(cy + 4.5)}V{fmt(cy)}A9 9 0 0 1 {fmt(cx + 9)} {fmt(cy)}V{fmt(cy + 2.5)}"),
        line(f"M{fmt(cx - 5.5)} {fmt(cy + 8)}V{fmt(cy)}A5.5 5.5 0 0 1 {fmt(cx + 5.5)} {fmt(cy)}V{fmt(cy + 5)}"),
        line(f"M{fmt(cx - 2)} {fmt(cy + 10.5)}V{fmt(cy)}A2 2 0 0 1 {fmt(cx + 2)} {fmt(cy)}V{fmt(cy + 7)}"),
    ]


@icon("fingerprint", CAT, "Fingerprint ridges; biometric identity",
      tags=["fingerprint", "biometric", "touch id", "identity", "unlock", "scan"], aliases=["fingerprint-id"])
def _(S):
    return _fingerprint(S)


@icon("face-id", CAT, "Face inside scanning corners; face recognition",
      tags=["face id", "face recognition", "biometric", "unlock", "identity", "scan"], aliases=["face-unlock"])
def _(S):
    return [*_brackets(S),
            line(seg(9, 8.5, 9, 10.5)), line(seg(15, 8.5, 15, 10.5)),
            line(poly([(12, 9), (12, 13), (11, 13)], r=S.r * 0.3)),
            line("M8.5 15.5C10.5 17.3 13.5 17.3 15.5 15.5")]


# =========================================================================== keys and locks

@icon("key-round", CAT, "Key with a large round bow, upright",
      tags=["key", "access", "unlock", "password", "credentials", "round key"], aliases=["round-key"])
def _(S):
    return [shell(circle(12, 7.5, 5)), dot(12, 7.5, 1.6),
            line(seg(12, 12.5, 12, 21.5)), line(seg(12, 16, 8.5, 16)), line(seg(12, 19.5, 9.5, 19.5))]


def _keyhole_d(S, cx=12.0, cy=8.5, r=5.0, y0=12.9, bottom=21.0, half=4.0):
    dy = y0 - cy
    dx = math.sqrt(r * r - dy * dy)
    xl, xr = cx - dx, cx + dx
    if S.name == "line":
        base = f"L{fmt(cx - half)} {fmt(bottom)}H{fmt(cx + half)}"
    else:
        base = (f"L{fmt(cx - half + 0.35)} {fmt(bottom - 1.9)}Q{fmt(cx - half)} {fmt(bottom)} {fmt(cx - half + 1.9)} {fmt(bottom)}"
                f"H{fmt(cx + half - 1.9)}Q{fmt(cx + half)} {fmt(bottom)} {fmt(cx + half - 0.35)} {fmt(bottom - 1.9)}")
    return f"M{fmt(xl)} {fmt(y0)}" + base + f"L{fmt(xr)} {fmt(y0)}A{r} {r} 0 1 0 {fmt(xl)} {fmt(y0)}Z"


@icon("keyhole", CAT, "Keyhole shape; a lock or restricted access",
      tags=["keyhole", "lock", "access", "private", "restricted", "secure"])
def _(S):
    return [shell(_keyhole_d(S))]


@icon("lock-keyhole", CAT, "Closed padlock with a keyhole",
      tags=["lock", "padlock", "keyhole", "secure", "locked", "private"], aliases=["padlock"])
def _(S):
    return [line("M7.5 10.5V7.5A4.5 4.5 0 0 1 16.5 7.5V10.5"),
            shell(rect(4, 10.5, 16, 11, _pick(S, 1, 3))),
            dot(12, 15, 1.75), detail(seg(12, 15, 12, 18.5))]


@icon("password", CAT, "Input field with masked characters and a cursor",
      tags=["password", "passcode", "pin", "masked", "credentials", "login"], aliases=["passcode"])
def _(S):
    return [shell(rect(2.5, 6.5, 19, 11, min(S.R, 3))),
            dot(6.5, 12, 1.5), dot(10.5, 12, 1.5), dot(14.5, 12, 1.5),
            detail(seg(18, 9.5, 18, 14.5))]


@icon("safe", CAT, "Strongbox with a combination dial and feet",
      tags=["safe", "strongbox", "valuables", "deposit", "secure", "money"], aliases=["strongbox"])
def _(S):
    return [shell(rect(3, 3, 18, 15.5, S.R)),
            detail(circle(13.5, 10.75, 3.5)),
            detail(seg(6.5, 6.5, 6.5, 8.5)), detail(seg(6.5, 13, 6.5, 15)),
            line(seg(6.5, 18.5, 6.5, 21)), line(seg(17.5, 18.5, 17.5, 21))]


@icon("vault", CAT, "Vault door with a spoked handle wheel",
      tags=["vault", "bank vault", "secure storage", "treasury", "deposit", "safe"], aliases=["bank-vault"])
def _(S):
    spokes = [detail(seg(*pt_on(13, 12, 2.5, a), *pt_on(13, 12, 6, a))) for a in (45, 135, 225, 315)]
    return [shell(rect(2.5, 2.5, 19, 19, S.R)), detail(circle(13, 12, 2.5)), *spokes,
            detail(seg(5.5, 6.5, 5.5, 9)), detail(seg(5.5, 15, 5.5, 17.5))]


# =========================================================================== visibility

_SLASH = seg(3.5, 3.5, 20.5, 20.5)


def _eye_off_stroke(S):
    d = _pick(S, _EYE, _EYE_ROUND)
    base = U(ST(d, 2, S.cap, S.join), ST(circle(12, 12, 3), 2, S.cap, S.join))
    return D(base, ST(_SLASH, 5, "round", "round"))


def _eye_off_filled():
    body = U(D(U(P(_EYE), ST(_EYE, 2)), P(circle(12, 12, 4.5))), P(circle(12, 12, 2.75)))
    return U(D(body, ST(_SLASH, 5.5, "round", "round")), ST(_SLASH, 2.5))


@icon("eye-off", CAT, "Eye with a slash; hidden or not visible",
      tags=["hidden", "invisible", "hide", "private", "unseen", "visibility"], aliases=["hidden", "invisible"],
      filled=_eye_off_filled)
def _(S):
    return [solid(path_to_d(_eye_off_stroke(S))), line(_SLASH)]


def _hat(S, y=10.5, top=3.5, w=(6.5, 17.5), brim=(2.5, 21.5), inset=1.25):
    (l, r), (bl, br) = w, brim
    return [shell(poly([(l, y), (l + inset, top), (r - inset, top), (r, y)], closed=True, r=S.r)),
            line(seg(bl, y, br, y))]


@icon("incognito", CAT, "Hat and round glasses; private or incognito browsing",
      tags=["incognito", "private browsing", "anonymous", "hidden", "disguise", "privacy"], aliases=["private-browsing"])
def _(S):
    return [*_hat(S),
            shell(circle(7, 16.5, 3)), shell(circle(17, 16.5, 3)),
            line("M10 16.5C11 15.5 13 15.5 14 16.5")]


@icon("spy", CAT, "Agent in a hat, dark glasses and a raised collar",
      tags=["spy", "agent", "secret agent", "undercover", "espionage", "anonymous"], aliases=["secret-agent"])
def _(S):
    return [*_hat(S, y=7.5, top=2.5, w=(8, 16), brim=(4.5, 19.5), inset=1),
            line("M8.5 9.5C8.5 11.5 10 13 12 13C14 13 15.5 11.5 15.5 9.5"),
            line(seg(8.5, 10, 15.5, 10)),
            line(poly([(3.5, 21), (3.5, 19), (5.5, 16), (9, 15), (12, 18.5), (15, 15), (18.5, 16), (20.5, 19), (20.5, 21)], r=S.r))]


# =========================================================================== alarms

@icon("alarm", CAT, "Alarm bell ringing; an intruder alarm",
      tags=["alarm", "burglar alarm", "intruder", "alert", "ringing", "security"], aliases=["burglar-alarm"])
def _(S):
    return [shell(circle(12, 12, 5.5)), detail(seg(12, 8.75, 12, 12.5)), dot(12, 15, 1.1),
            line(arc(12, 12, 9, 140, 220)), line(arc(12, 12, 9, 320, 400))]


@icon("siren", CAT, "Rotating warning light with rays; an emergency siren",
      tags=["siren", "beacon", "emergency", "warning light", "alert", "police"], aliases=["beacon"])
def _(S):
    return [shell("M6.5 17.5V13.5A5.5 5.5 0 0 1 17.5 13.5V17.5Z"),
            shell(rect(4, 17.5, 16, 3.5, min(S.R, 1.5))),
            detail("M9.5 13.5A2.5 2.5 0 0 1 12 11"),
            line(seg(12, 2, 12, 4.5)), line(seg(4.5, 5, 6.2, 6.7)), line(seg(19.5, 5, 17.8, 6.7)),
            line(seg(2, 11.5, 4, 11.5)), line(seg(20, 11.5, 22, 11.5))]


# =========================================================================== identity

@icon("id-badge", CAT, "Clip-on ID badge with a photo of a person",
      tags=["id badge", "identity", "employee", "pass", "lanyard", "staff"], aliases=["staff-badge"])
def _(S):
    return [shell(rect(4.5, 4.5, 15, 17, min(S.R, 3))),
            shell(rect(9.5, 2.5, 5, 4, _pick(S, 0.5, 1.5))),
            detail(circle(12, 11.5, 2.5)),
            detail("M7.5 18.5C8 16.3 9.8 15 12 15C14.2 15 16 16.3 16.5 18.5")]


@icon("verified", CAT, "Person with a check mark; a verified identity",
      tags=["verified", "identity", "confirmed", "trusted", "kyc", "account"], aliases=["verified-user"])
def _(S):
    return [shell(circle(8.5, 7.5, 3.75)),
            line("M2.5 21V19.5C2.5 16.2 5.2 14 8.5 14C10.4 14 12 14.6 13.2 15.6"),
            line(poly([(14.5, 9), (17, 11.5), (21.5, 6.5)], r=S.r * 0.5))]


@icon("security-certificate", CAT, "Certificate with a seal and ribbons; an SSL or security certificate",
      tags=["certificate", "ssl", "tls", "https", "trust", "seal"], aliases=["ssl-certificate"])
def _(S):
    return [shell(rect(2.5, 3, 19, 13, min(S.R, 3))),
            detail(circle(7.75, 9.5, 2.5)),
            detail(seg(12.5, 7, 18, 7)), detail(seg(12.5, 11.5, 16, 11.5)),
            line(poly([(6.5, 16), (6, 21), (7.75, 19.75), (9.5, 21), (9, 16)], r=S.r * 0.3))]


# =========================================================================== network defence

@icon("firewall", CAT, "Brick wall with a flame rising from it; a network firewall",
      tags=["firewall", "network security", "wall", "block", "protection", "filter"])
def _(S):
    flame = _pick(S, "M12 2.5C9.5 5 8 7.2 8 9.2C8 10.6 8.8 11.5 9.5 11.5H14.5C15.2 11.5 16 10.6 16 9.2C16 7.2 14.5 5 12 2.5Z",
                  "M11.3 3.2C9.2 5.4 8 7.4 8 9.2C8 10.6 8.8 11.5 9.5 11.5H14.5C15.2 11.5 16 10.6 16 9.2C16 7.4 14.8 5.4 12.7 3.2Q12 2.5 11.3 3.2Z")
    return [shell(flame),
            shell(rect(3, 11.5, 18, 9.5, S.R * 0.6)),
            detail(seg(3, 16.25, 21, 16.25)),
            detail(seg(8, 11.5, 8, 16.25)), detail(seg(16, 11.5, 16, 16.25)), detail(seg(12, 16.25, 12, 21))]


def _virus(S, filled=False):
    spikes = []
    for i in range(8):
        a = i * 45 - 90
        spikes.append(line(seg(*pt_on(12, 12, 5.5, a), *pt_on(12, 12, 7.5, a))))
        x, y = pt_on(12, 12, 8.6, a)
        spikes.append(dot(x, y, 1.4) if S.name == "rounded" else solid(rect(x - 1.25, y - 1.25, 2.5, 2.5)))
    return [shell(circle(12, 12, 5.5)), dot(10.25, 11, 1.1), dot(13.75, 13.25, 1.1), *spikes]


@icon("virus", CAT, "Virus particle with spikes; malware or infection",
      tags=["virus", "malware", "infection", "threat", "bug", "germ"], aliases=["malware"])
def _(S):
    return _virus(S)


# =========================================================================== authentication

@icon("two-factor", CAT, "Phone beside a shield with a check; two-factor authentication",
      tags=["2fa", "two-factor", "mfa", "authentication", "verification", "login"], aliases=["2fa", "mfa"])
def _(S):
    small_shield = "M18 2.5L21.5 3.9V7.5C21.5 10 20 11.8 18 12.5C16 11.8 14.5 10 14.5 7.5V3.9Z"
    small_round = "M17.4 2.7L15.1 3.7Q14.5 3.9 14.5 4.5V7.5C14.5 10 16 11.8 18 12.5C20 11.8 21.5 10 21.5 7.5V4.5Q21.5 3.9 20.9 3.7L18.6 2.7Q18 2.5 17.4 2.7Z"
    return [shell(rect(2.5, 3, 9, 18.5, min(S.R, 2.5))), detail(seg(5.5, 17.5, 8.5, 17.5)),
            shell(_pick(S, small_shield, small_round))]


@icon("otp", CAT, "Code entry split into separate cells; a one-time passcode",
      tags=["otp", "one-time password", "verification code", "pin", "sms code", "2fa"], aliases=["one-time-password"])
def _(S):
    return [shell(rect(2.5, 6.5, 19, 11, min(S.R, 3))),
            detail(seg(8.83, 6.5, 8.83, 17.5)), detail(seg(15.17, 6.5, 15.17, 17.5)),
            dot(5.67, 12, 1.5), dot(12, 12, 1.5), dot(18.33, 12, 1.5)]


@icon("captcha", CAT, "Ticked checkbox beside distorted text; a human-verification test",
      tags=["captcha", "not a robot", "human check", "bot protection", "verification", "spam"])
def _(S):
    wave = "M14 {y}C15 {a} 16.2 {a} 17.2 {y}C18.2 {b} 19.5 {b} 20.5 {y}"
    return [shell(rect(2.5, 7.5, 9, 9, min(S.R, 2))),
            detail(poly([(4.75, 12), (6.5, 13.75), (9.25, 10.25)], r=S.r * 0.5)),
            line(wave.format(y=9.5, a=8, b=11)), line(wave.format(y=14.5, a=13, b=16))]


@icon("scan-face", CAT, "Head and shoulders inside scanning corners with a scan line",
      tags=["face scan", "face recognition", "scan", "biometric", "identity", "camera"])
def _(S):
    return [*_brackets(S),
            line(circle(12, 9.5, 3)),
            line("M6.5 19.5C7 16.8 9.2 15 12 15C14.8 15 17 16.8 17.5 19.5"),
            line(seg(2.5, 12, 21.5, 12))]


@icon("access-card", CAT, "Key card with a contactless signal; an access or RFID card",
      tags=["access card", "key card", "rfid", "badge", "contactless", "entry"], aliases=["rfid-card"])
def _(S):
    return [shell(rect(3, 8.5, 11, 13, min(S.R, 2.5))), detail(seg(6.5, 12, 10.5, 12)),
            line(arc(13.5, 9, 3.5, 275, 355)), line(arc(13.5, 9, 7, 275, 355))]


@icon("door-lock", CAT, "Door handle plate with a lever and keyhole",
      tags=["door lock", "door handle", "lock", "entry", "home security", "latch"], aliases=["door-handle"])
def _(S):
    return [shell(rect(5, 2.5, 8, 19, _pick(S, 1, 4))),
            line(seg(9, 8, 20.5, 8)),
            dot(9, 15, 1.6), detail(seg(9, 15, 9, 18))]


# =========================================================================== people and privacy

@icon("guard", CAT, "Security guard in a peaked cap with a badge",
      tags=["guard", "security guard", "officer", "watchman", "bouncer", "patrol"], aliases=["security-guard"])
def _(S):
    return [shell(poly([(6.5, 7.5), (4.5, 4.5), (12, 2), (19.5, 4.5), (17.5, 7.5)], closed=True, r=S.r * 0.6)),
            line("M8 9C8 11.4 9.8 13 12 13C14.2 13 16 11.4 16 9"),
            shell("M3.5 21.5V19.5C3.5 17 5.5 15.5 8.5 15.5H15.5C18.5 15.5 20.5 17 20.5 19.5V21.5Z"),
            dot(8, 18.5, 1.25)]


@icon("privacy", CAT, "Shield protecting a person; personal data privacy",
      tags=["privacy", "personal data", "gdpr", "protection", "user", "confidential"], aliases=["data-privacy"])
def _(S):
    return [_shield(S), detail(circle(12, 9.25, 2.25)),
            detail("M8 16.5C8.4 14.6 10 13.5 12 13.5C14 13.5 15.6 14.6 16 16.5")]


@icon("mask-privacy", CAT, "Eye mask worn to hide one's identity",
      tags=["mask", "masquerade", "anonymous", "disguise", "privacy", "hidden identity"])
def _(S):
    if S.name == "line":
        d = ("M2 6.5L6 8C8.5 8.9 10.2 9.3 12 9.3C13.8 9.3 15.5 8.9 18 8L22 6.5V12C22 15.6 19.8 17.5 17 17.5"
             "C14.8 17.5 13.5 15.5 12 15.5C10.5 15.5 9.2 17.5 7 17.5C4.2 17.5 2 15.6 2 12Z")
    else:
        d = ("M2.5 9C2.5 7.5 3.8 6.6 5.2 7.1L6.5 7.6C8.7 8.6 10.3 9.3 12 9.3C13.7 9.3 15.3 8.6 17.5 7.6L18.8 7.1"
             "C20.2 6.6 21.5 7.5 21.5 9V12C21.5 15.4 19.5 17.5 17 17.5C14.8 17.5 13.5 15.5 12 15.5"
             "C10.5 15.5 9.2 17.5 7 17.5C4.5 17.5 2.5 15.4 2.5 12Z")
    return [shell(d), detail(ellipse(7.5, 12.5, 2, 1.25)), detail(ellipse(16.5, 12.5, 2, 1.25))]


@icon("detective-glass", CAT, "Magnifying glass over a fingerprint; an investigation",
      tags=["investigate", "forensics", "detective", "inspect", "evidence", "audit"], aliases=["investigate"])
def _(S):
    return [shell(circle(14, 10, 7)),
            detail("M11 14.5V10A3 3 0 0 1 17 10V13"), detail(seg(14, 10, 14, 15.5)),
            line(seg(9.05, 14.95, 3, 21))]


@icon("warning-shield", CAT, "Shield with an exclamation mark; a security warning",
      tags=["security warning", "alert", "threat", "risk", "caution", "vulnerability"], aliases=["shield-alert"])
def _(S):
    return [_shield(S), detail(seg(12, 6.5, 12, 12)), dot(12, 15.25, 1.3)]


@icon("bomb-disposal", CAT, "Bomb whose fuse has been cut; bomb disposal or defusing",
      tags=["bomb disposal", "defuse", "explosive", "eod", "threat", "danger"], aliases=["defuse"])
def _(S):
    neck = [pt_on(9.5, 14.5, 6.5, -60), pt_on(9.5, 14.5, 6.5, -30)]
    return [shell(circle(9.5, 14.5, 6.5)),
            shell(poly([(11.6, 7.4), (14.4, 6.2), (17.8, 9.6), (16.6, 12.4)], closed=True, r=_pick(S, 0, 0.8))),
            detail(arc(9.5, 14.5, 3.5, 190, 250)),
            line("M16.1 6.9C16.6 5.4 17.3 4.6 18 4.2"),
            line("M20 3.2C20.6 2.9 21.2 2.8 21.8 2.9")]


@icon("biometric", CAT, "Fingerprint inside scanning corners; biometric authentication",
      tags=["biometric", "fingerprint scan", "touch id", "authentication", "identity", "scan"], aliases=["fingerprint-scan"])
def _(S):
    cx, cy = 12, 11.5
    return [*_brackets(S),
            line(f"M{cx - 5} {cy + 5}V{cy}A5 5 0 0 1 {cx + 5} {cy}V{cy + 3}"),
            line(f"M{cx - 1.5} {cy + 6}V{cy}A1.5 1.5 0 0 1 {cx + 1.5} {cy}V{cy + 4}")]


@icon("retina-scan", CAT, "Eye inside scanning corners; an iris or retina scan",
      tags=["retina scan", "iris scan", "eye scan", "biometric", "identity", "recognition"], aliases=["iris-scan"])
def _(S):
    eye = ("M5 12C6.8 9 9.2 7.5 12 7.5C14.8 7.5 17.2 9 19 12C17.2 15 14.8 16.5 12 16.5C9.2 16.5 6.8 15 5 12Z" if S.name == "line"
           else "M5.6 11.1C7.4 8.6 9.6 7.5 12 7.5C14.4 7.5 16.6 8.6 18.4 11.1Q19 12 18.4 12.9C16.6 15.4 14.4 16.5 12 16.5C9.6 16.5 7.4 15.4 5.6 12.9Q5 12 5.6 11.1Z")
    return [*_brackets(S), shell(eye), detail(circle(12, 12, 2))]
