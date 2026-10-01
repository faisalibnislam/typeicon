"""TypeIcon Core: privacy 003 (cyber threats, covert devices, physical security, forensics, ciphers)."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar, rotation, transform_path

CAT = "privacy"


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def head(S, x, y, deg, s=3.0, spread=42, kind=line):
    """Open arrow head with its tip at (x, y) pointing along deg (0 = right, 90 = down)."""
    a = math.radians(deg + 180)
    sp = math.radians(spread)
    p1 = (x + s * math.cos(a - sp), y + s * math.sin(a - sp))
    p2 = (x + s * math.cos(a + sp), y + s * math.sin(a + sp))
    return kind(poly([p1, (x, y), p2], r=0 if S.name == "line" else 0.6))


def face(S, cx, cy, hw, hh):
    """Face outline (tall rounded oval)."""
    return rect(cx - hw, cy - hh, 2 * hw, 2 * hh, hw * (0.75 if S.name == "line" else 1.0))


def window(x, y, w, h, S, bar=3.0):
    return [shell(rect(x, y, w, h, rr(S, 2))), detail(seg(x, y + bar, x + w, y + bar))]


def rotp(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * sn, cy + (x - cx) * sn + (y - cy) * c) for x, y in pts]


# ============================================================================ chunk 1

@icon("password-spraying", CAT, "Watering can tilted to pour a spray of small drops",
      tags=["password spraying", "brute force", "credential attack", "login attack", "watering can", "hacking", "spray"])
def _(S):
    T = lambda pts: [(x + 1.5, y - 2.5) for x, y in rotp(pts, 25, 8, 14)]
    body = T([(4, 10), (12, 10), (12, 19.5), (4, 19.5)])
    handle = T([(4, 12), (1.5, 12), (1.5, 17.5), (4, 17.5)])
    spout = T([(12, 17), (18.5, 11)])
    rose = T([(16.3, 8.6), (20.7, 13.4)])
    return [
        shell(poly(body, closed=True, r=S.r)),
        line(poly(handle, r=S.r)),
        line(poly(spout)),
        shell(poly(rose + [], r=0)) if False else line(poly(rose)),
        dot(20, 17.5, 1.25), dot(16.5, 20.5, 1.25), dot(21, 21, 1.0),
    ]


@icon("clickjacking", CAT, "Cursor clicking a visible button while a hidden button outline sits under it",
      tags=["clickjacking", "ui redress", "hidden button", "click hijack", "web attack", "deceptive click", "cursor"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 13, 7, rr(S, 2))),
        line(poly([(19.5, 7.5), (21.5, 7.5), (21.5, 20.5), (11, 20.5), (11, 18.5)])),
        shell(poly([(8, 7), (8, 17), (10.5, 14.8), (12.3, 19), (14.3, 18.2), (12.5, 14), (15.5, 14)], closed=True, r=S.r * 0.3)),
    ]


@icon("supply-chain-attack", CAT, "Shipping box on a conveyor with a small bug sitting on the lid",
      tags=["supply chain attack", "software supply chain", "compromised package", "bug", "conveyor", "shipping", "malware"])
def _(S):
    return [
        shell(rect(5, 10.5, 14, 6.5, rr(S, 1.5))),
        detail(seg(12, 10.5, 12, 17)),
        shell(rect(2.5, 17, 19, 4.5, rr(S, 2))),
        Part("solid", ellipse(12, 7, 2.6, 1.9)),
        line(seg(9, 5, 10.3, 6.3)), line(seg(15, 5, 13.7, 6.3)),
        line(seg(9, 9, 10, 8)), line(seg(15, 9, 14, 8)),
    ]


@icon("popup-adware", CAT, "Browser window with two more popup windows cascading over it",
      tags=["adware", "popup", "pop-up ads", "browser ads", "windows", "spam", "unwanted ads"])
def _(S):
    return [
        line(poly([(13.5, 6.5), (13.5, 2.5), (2.5, 2.5), (2.5, 10.5), (7.5, 10.5)])),
        line(seg(2.5, 5.5, 13.5, 5.5)),
        line(poly([(12.5, 14.5), (7.5, 14.5), (7.5, 6.5), (18.5, 6.5), (18.5, 12.5)])),
        line(seg(7.5, 9.5, 18.5, 9.5)),
        shell(rect(12.5, 12.5, 9, 9, rr(S, 2))),
        detail(seg(12.5, 15.5, 21.5, 15.5)),
    ]


@icon("certificate-pinning", CAT, "Certificate card with a ribbon seal and a push pin through its top edge",
      tags=["certificate pinning", "ssl pinning", "tls", "trusted certificate", "push pin", "public key pinning", "pinned"])
def _(S):
    return [
        shell(rect(2.5, 6.5, 19, 11.5, rr(S, 2))),
        detail(seg(5.5, 12.2, 11, 12.2)),
        detail(seg(5.5, 15, 9, 15)),
        shell(circle(16.5, 12.5, 2.4)),
        line(seg(15.3, 15, 14.6, 21)),
        line(seg(17.7, 15, 18.4, 21)),
        line(seg(4.5, 2.5, 9.5, 2.5)),
        line(seg(7, 2.5, 7, 9)),
    ]


@icon("deepfake", CAT, "Face outline with its right half broken into offset glitch strips",
      tags=["deepfake", "fake face", "synthetic media", "ai generated", "face swap", "manipulated video", "glitch"])
def _(S):
    h = 9
    return [
        line(f"M12 {12 - h}A7 {h} 0 0 0 12 {12 + h}"),
        line(seg(12, 3, 12, 6.5)), line(seg(12, 17.5, 12, 21)),
        dot(8.5, 10, 1.2),
        detail(seg(7.5, 15.5, 10, 15.5)),
        line(seg(14.5, 5, 18.5, 5)),
        line(seg(16, 9, 20.5, 9)),
        line(seg(14.5, 13, 19, 13)),
        line(seg(16.5, 17, 19, 17)),
    ]


@icon("voice-cloning", CAT, "Two matching rows of sound bars with an arrow copying the top one to the bottom",
      tags=["voice cloning", "voice deepfake", "audio copy", "speech synthesis", "soundwave", "voice impersonation", "duplicate voice"])
def _(S):
    hs = [1.5, 3.5, 2.5, 3.5, 1.5]
    out = []
    for i, h in enumerate(hs):
        x = 4 + 4 * i
        out.append(line(seg(x, 5 - h + 0.5, x, 5 + h - 0.5)))
        out.append(line(seg(x, 19 - h + 0.5, x, 19 + h - 0.5)))
    return out + [line(seg(12, 9.6, 12, 14)), head(S, 12, 14.4, 90, 2.6)]


@icon("sim-swap", CAT, "Two SIM cards side by side with curved swap arrows above and below",
      tags=["sim swap", "sim card", "sim hijack", "number port", "phone takeover", "swap", "mobile fraud"])
def _(S):
    def sim(x):
        return poly([(x, 9), (x + 5, 9), (x + 7, 11), (x + 7, 17.5), (x, 17.5)], closed=True, r=S.r * 0.6)
    return [
        shell(sim(2.5)), shell(sim(14.5)),
        line("M6 6.5Q12 2 18 6.5"),
        head(S, 18.2, 6.6, 50, 2.8),
        line("M18 20Q12 24.5 6 20"),
        head(S, 5.8, 19.9, 230, 2.8),
    ]


@icon("mobile-key", CAT, "Smartphone held near a door lock with contactless wave arcs between them",
      tags=["mobile key", "digital key", "phone unlock", "contactless", "nfc", "smart lock", "tap to unlock"])
def _(S):
    return [
        shell(rect(2.5, 5, 7.5, 14, rr(S, 2))),
        detail(seg(5, 16, 7.5, 16)),
        line(arc(10, 9.5, 3.6, -50, 50)),
        shell(rect(17, 3.5, 4.5, 17, rr(S, 1.5))),
        dot(19.25, 8, 1.1),
        line(seg(17, 16, 13, 16)),
    ]


@icon("server-cage", CAT, "Server rack with bars across the front and a padlock hanging in the centre",
      tags=["server cage", "locked rack", "data center", "secure server", "cage", "colocation", "rack lock"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, S.R)),
        detail(seg(7, 2.5, 7, 21.5)),
        detail(seg(17, 2.5, 17, 21.5)),
        Part("dot", rect(9.25, 12.5, 5.5, 5.5, rr(S, 1.2))),
        detail(poly([(10.75, 12.5), (10.75, 9.5), (13.25, 9.5), (13.25, 12.5)], r=S.r * 0.5)),
    ]


@icon("door-security-bar", CAT, "Door with a brace bar wedged from under the handle down to the floor",
      tags=["door brace", "security bar", "door jammer", "barricade", "home security", "door lock bar", "police lock"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 12, 19, rr(S, 1.5))),
        dot(12.5, 11, 1.3),
        line(seg(2, 21.5, 22, 21.5)),
        shell(poly([(11, 13.5), (13.5, 12.5), (21, 19.5), (19.5, 21)], closed=True, r=S.r * 0.4)),
    ]


@icon("searchlight", CAT, "Round lamp on a pivot stand throwing a wide cone of light upward",
      tags=["searchlight", "spotlight", "floodlight", "security light", "beam", "patrol light", "lookout"])
def _(S):
    c = polar(9, 13, 0, 0)
    fx, fy = 11.1, 10.9
    out = [shell(arc(9, 13, 6.2, 45, 225) + "Z")]
    for d in (-32, 0, 32):
        a = math.radians(-45 + d)
        out.append(line(poly([(fx + 3.6 * math.cos(a), fy + 3.6 * math.sin(a)), (fx + 9.2 * math.cos(a), fy + 9.2 * math.sin(a))])))
    return out + [line(seg(9, 19.2, 9, 21.5)), line(seg(5, 21.5, 13, 21.5))]


@icon("face-matching", CAT, "Two faces with landmark points joined by a double headed arrow",
      tags=["face matching", "face comparison", "facial recognition", "identity verification", "biometric match", "compare faces", "face id"])
def _(S):
    return [
        shell(face(S, 6.5, 9, 4, 5.5)),
        shell(face(S, 17.5, 9, 4, 5.5)),
        dot(5, 8, 1), dot(8, 8, 1), dot(16, 8, 1), dot(19, 8, 1),
        dot(6.5, 11.6, 0.9), dot(17.5, 11.6, 0.9),
        line(seg(5.5, 19, 18.5, 19)),
        head(S, 4.5, 19, 180, 2.8), head(S, 19.5, 19, 0, 2.8),
    ]


@icon("screen-monitoring", CAT, "Desktop monitor showing a large open eye on its screen",
      tags=["screen monitoring", "employee monitoring", "screen capture", "watching screen", "surveillance", "spyware", "remote viewing"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 13.5, rr(S, 2))),
        detail("M6.5 10.2Q12 4.6 17.5 10.2Q12 15.8 6.5 10.2Z"),
        dot(12, 10.2, 1.6),
        line(seg(12, 17, 12, 20.5)),
        line(seg(8, 20.5, 16, 20.5)),
    ]


@icon("browser-fingerprinting", CAT, "Browser window with a fingerprint whorl inside the page area",
      tags=["browser fingerprinting", "device fingerprint", "tracking", "canvas fingerprint", "web tracking", "user identification", "fingerprint"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 18, rr(S, 2))),
        detail(seg(2.5, 7, 21.5, 7)),
        dot(12, 14.5, 1.5),
        detail(arc(12, 14.5, 4.6, 160, 380)),
        dot(5, 5, 0.8), dot(7.5, 5, 0.8),
    ]


# ============================================================================ chunk 2

@icon("one-way-mirror", CAT, "Mirror with diagonal reflection lines and a faint head visible through its right half",
      tags=["one way mirror", "two way mirror", "interrogation", "observation glass", "mirror", "spying", "reflective glass"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        detail(seg(5.5, 10.5, 9.5, 6.5)),
        detail(seg(5.5, 16.5, 12, 10)),
        detail("M13.4 13.5Q16.5 9.5 19.6 13.5Q16.5 17.5 13.4 13.5Z"),
        dot(16.5, 13.5, 1.2),
    ]


@icon("rf-bug-detector", CAT, "Handheld detector with a short antenna, a meter gauge and a sensitivity dial",
      tags=["bug detector", "rf detector", "bug sweeper", "counter surveillance", "hidden microphone", "signal detector", "tscm"])
def _(S):
    return [
        shell(rect(5.5, 8.5, 13, 13, rr(S, 3))),
        line(seg(9, 8.5, 9, 3.5)),
        dot(9, 3, 1.3),
        detail(arc(12, 15, 3.8, 180, 360)),
        detail(seg(12, 15, 13.5, 12.5)),
        dot(12, 18.6, 1.1),
        line(arc(9, 5, 5, -50, 10)),
    ]


@icon("burn-after-reading", CAT, "Folded letter with a small flame rising beside its bottom corner",
      tags=["burn after reading", "self destruct", "secret message", "confidential letter", "flame", "destroy", "spy letter"])
def _(S):
    return [
        shell(rect(2.5, 10.5, 10, 9.5, rr(S, 2))),
        detail(poly([(2.5, 10.5), (7.5, 15), (12.5, 10.5)], r=S.r * 0.4)),
        shell("M18 2.8C18 8 22 10.5 22 15.6A4 4 0 0 1 14 15.6C14 13 15.4 11.3 16.6 10C16.8 12 17.6 12.6 18.4 12.6C18.8 9 18.8 6 18 2.8Z"),
    ]


@icon("hollow-book-safe", CAT, "Hardcover book with a rectangular cutout in its pages holding a key",
      tags=["hollow book", "book safe", "hidden key", "stash", "secret compartment", "diversion safe", "hiding place"])
def _(S):
    return [
        shell(rect(3, 3.5, 18, 17, rr(S, 2.5))),
        detail(seg(6, 3.5, 6, 20.5)),
        detail(rect(9, 8, 9.5, 8, rr(S, 1))),
        dot(11.3, 12, 1.3),
        line(seg(11.3, 12, 16.3, 12)),
        line(seg(14.8, 12, 14.8, 14)),
    ]


@icon("diversion-safe-can", CAT, "Drink can with its top lifted off, revealing rolled banknotes inside",
      tags=["diversion safe", "fake can", "hidden cash", "stash can", "secret storage", "hide money", "can safe"])
def _(S):
    return [
        shell(rect(6, 11, 12, 10.5, rr(S, 3))),
        detail(seg(6, 15.5, 18, 15.5)),
        line(seg(7, 2.5, 17, 2.5)),
        Part("solid", rect(8, 5.6, 3.5, 5, 1.2)),
        Part("solid", rect(12.5, 5.6, 3.5, 5, 1.2)),
    ]


@icon("key-hider-rock", CAT, "Garden rock with a small drawer slid open underneath showing a key",
      tags=["key hider", "fake rock", "spare key", "hide a key", "garden rock", "hidden compartment", "stash"])
def _(S):
    return [
        shell("M2.5 13.5Q2.5 4.5 12 4.5Q21.5 4.5 21.5 13.5Z"),
        line(poly([(6.5, 13.5), (6.5, 21), (17.5, 21), (17.5, 13.5)], r=S.r * 0.5)),
        dot(9.8, 17, 1.4),
        line(seg(9.8, 17, 15, 17)),
    ]


@icon("badge-wallet", CAT, "Open bifold wallet with a shield badge on the left flap and an ID card on the right",
      tags=["badge wallet", "police badge", "credentials holder", "id holder", "detective", "investigator", "law enforcement id"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 19, 15, rr(S, 2.5))),
        detail(seg(12, 4.5, 12, 19.5)),
        detail(poly([(5, 8), (9.5, 8), (9.5, 12.5), (7.25, 16), (5, 12.5)], closed=True, r=S.r * 0.4)),
        detail(rect(14.5, 8, 5, 8, rr(S, 1))),
    ]


@icon("fingerprint-ink-pad", CAT, "Ink pad in an open tin with a fingertip pressed down onto it",
      tags=["ink pad", "fingerprinting", "fingerprint card", "ink", "finger", "booking", "forensics"])
def _(S):
    return [
        shell(rect(3, 14, 18, 7.5, rr(S, 2))),
        detail(seg(6.5, 17.8, 17.5, 17.8)),
        shell(rect(8.5, 2.5, 7, 11.5, 3.5 if S.name == "rounded" else 2.5)),
        detail(arc(12, 8.5, 1.4, 180, 360)),
    ]


@icon("machine-readable-zone", CAT, "Identity document card with a photo box on top and rows of code characters along the bottom",
      tags=["mrz", "passport", "machine readable zone", "travel document", "id card", "ocr line", "identity document"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 2.5))),
        detail(rect(5.5, 5.5, 5.5, 5.5, rr(S, 1))),
        detail(seg(13.5, 6.5, 18.5, 6.5)),
        detail(seg(13.5, 10, 17, 10)),
        detail(seg(5.5, 14.5, 7.5, 14.5)), detail(seg(9.5, 14.5, 11.5, 14.5)), detail(seg(13.5, 14.5, 18.5, 14.5)),
        detail(seg(5.5, 18, 10.5, 18)), detail(seg(12.5, 18, 14.5, 18)), detail(seg(16.5, 18, 18.5, 18)),
    ]


@icon("shoeprint-evidence", CAT, "Shoe sole print with tread marks beside an L-shaped forensic scale ruler",
      tags=["shoeprint", "footprint", "crime scene", "evidence", "forensic scale", "tread", "footwear evidence"])
def _(S):
    return [
        shell(ellipse(8, 8, 4.6, 5)),
        detail(seg(5.6, 7, 10.4, 7)),
        shell(ellipse(8.3, 18, 3.2, 3.8)),
        line(poly([(14.5, 21), (21, 21), (21, 3)])),
        line(seg(18.5, 7, 21, 7)), line(seg(18.5, 11, 21, 11)), line(seg(18.5, 15, 21, 15)),
        line(seg(15, 18, 15, 21)) if False else line(seg(18, 21, 18, 18.5)),
    ]


@icon("interrogation-room", CAT, "Hanging cone lamp above a small table with one chair on each side",
      tags=["interrogation", "interview room", "police questioning", "suspect", "lamp", "table and chairs", "investigation"])
def _(S):
    return [
        line(seg(12, 2, 12, 4.5)),
        shell(poly([(9.5, 4.5), (14.5, 4.5), (17.5, 10), (6.5, 10)], closed=True, r=S.r * 0.5)),
        line(seg(7, 14.5, 17, 14.5)),
        line(seg(8.5, 14.5, 8.5, 21.5)), line(seg(15.5, 14.5, 15.5, 21.5)),
        line(seg(2.5, 12, 2.5, 21.5)), line(seg(2.5, 17.5, 5.5, 17.5)),
        line(seg(21.5, 12, 21.5, 21.5)), line(seg(18.5, 17.5, 21.5, 17.5)),
    ]


@icon("investigation-board", CAT, "Cork board with four pinned photos joined by zigzag string",
      tags=["investigation board", "evidence board", "conspiracy board", "case board", "detective", "red string", "pinned photos"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 18, rr(S, 2))),
        detail(rect(5, 5.5, 4, 4)), detail(rect(15, 5.5, 4, 4)),
        detail(rect(5, 13.5, 4, 4)), detail(rect(15, 13.5, 4, 4)),
        detail(poly([(9, 7.5), (12, 11.5), (12, 14.5), (15, 15.5)])),
    ]


@icon("ball-and-chain", CAT, "Heavy iron ball joined by a short chain to an open ankle shackle",
      tags=["ball and chain", "prisoner", "shackle", "burden", "captivity", "restraint", "jail"])
def _(S):
    return [
        shell(circle(8.5, 15, 5.8)),
        line(seg(12.5, 10.8, 15.5, 7.5)),
        line(arc(17.5, 6.5, 3.6, 130, 440)),
        dot(6.3, 13, 1.1),
    ]


@icon("guard-shoulder-patch", CAT, "Shield shaped shoulder patch with a banner strip across the top and a star in the centre",
      tags=["guard patch", "security badge", "shoulder patch", "uniform", "emblem", "security guard", "insignia"])
def _(S):
    pts = [polar(12, 14.3, 3.6 if i % 2 == 0 else 1.6, -90 + i * 36) for i in range(10)]
    return [
        shell(poly([(4.5, 2.5), (19.5, 2.5), (19.5, 13), (12, 21.5), (4.5, 13)], closed=True, r=S.r)),
        detail(seg(4.5, 7.5, 19.5, 7.5)),
        Part("dot", poly(pts, closed=True)),
    ]


@icon("password-reuse", CAT, "One key at the top with three arrows pointing from it to three doors in a row",
      tags=["password reuse", "same password", "credential stuffing", "key reuse", "one key many doors", "weak security", "shared password"])
def _(S):
    return [
        shell(circle(7, 4.5, 2.3)),
        line(seg(9.3, 4.5, 18, 4.5)),
        line(seg(16, 4.5, 16, 6.3)),
        line(seg(10.5, 8.5, 6, 12.3)), head(S, 5.6, 12.6, 130, 2.4),
        line(seg(12, 8.5, 12, 12.3)), head(S, 12, 12.8, 90, 2.4),
        line(seg(13.5, 8.5, 18, 12.3)), head(S, 18.4, 12.6, 50, 2.4),
        shell(rect(2.5, 15, 5, 6.5, rr(S, 1.2))),
        shell(rect(9.5, 15, 5, 6.5, rr(S, 1.2))),
        shell(rect(16.5, 15, 5, 6.5, rr(S, 1.2))),
    ]


# ============================================================================ chunk 3

@icon("evil-twin-wifi", CAT, "Two wifi signal symbols side by side, the right one wearing small devil horns",
      tags=["evil twin", "rogue access point", "fake wifi", "wifi spoofing", "wireless attack", "devil", "hotspot impersonation"])
def _(S):
    def wifi(cx, cy):
        return [line(arc(cx, cy, 3.2, -135, -45)), line(arc(cx, cy, 6.6, -135, -45)), dot(cx, cy, 1.3)]
    return wifi(6, 19.5) + wifi(18, 19.5) + [
        Part("solid", poly([(14.8, 10.8), (14.6, 5.2), (18.2, 8.3)], closed=True)),
        Part("solid", poly([(21.2, 10.8), (21.4, 5.2), (17.8, 8.3)], closed=True)),
    ]


@icon("shoulder-surfing", CAT, "Seated person at a laptop with a second head peering over their shoulder",
      tags=["shoulder surfing", "peeping", "over the shoulder", "spying on screen", "privacy screen", "password stealing", "snooping"])
def _(S):
    return [
        shell(circle(4.8, 5, 2.3)),
        line(seg(7.3, 5.6, 14, 9)),
        shell(circle(9, 11.5, 2.8)),
        line("M3.5 21.5V19.5A5.5 4.8 0 0 1 14.5 19.5V21.5"),
        shell(rect(15, 10, 7, 6, rr(S, 1.2))),
        line(seg(14, 19, 22.5, 19)),
    ]


@icon("tailgating-entry", CAT, "Open doorway with two people walking through close together, one right behind the other",
      tags=["tailgating", "piggybacking", "unauthorized entry", "door access", "following someone in", "physical security", "two people"])
def _(S):
    return [
        line(poly([(2.5, 21.5), (2.5, 2.5), (21.5, 2.5), (21.5, 21.5)], r=S.r)),
        dot(8.3, 8.3, 1.9), line(seg(8.3, 11, 8.3, 15.5)), line(poly([(6.6, 21.5), (8.3, 15.5), (10, 21.5)])),
        dot(15.7, 8.3, 1.9), line(seg(15.7, 11, 15.7, 15.5)), line(poly([(14, 21.5), (15.7, 15.5), (17.4, 21.5)])),
    ]


@icon("dumpster-diving", CAT, "Open waste bin with its lid raised and a hand pulling a document page out",
      tags=["dumpster diving", "trash", "garbage", "discarded documents", "data theft", "waste bin", "shredding reminder"])
def _(S):
    return [
        line(poly([(9.5, 10.5), (9.5, 4.5), (17.5, 4.5), (17.5, 10.5)])),
        detail(seg(12, 7.5, 15, 7.5)) if False else line(seg(12, 8, 15, 8)),
        shell(circle(19.5, 3.8, 1.8)) if False else dot(19.5, 4, 1.8),
        shell(poly([(4.5, 10.5), (19.5, 10.5), (18, 21.5), (6, 21.5)], closed=True, r=S.r * 0.5)),
        detail(seg(10, 14, 10.3, 18)), detail(seg(14, 14, 13.7, 18)),
        line(poly([(3.5, 8), (2.5, 4.5), (8, 3.2)])),
    ]


@icon("social-engineering", CAT, "Hand holding a puppet control bar with strings running down to a small person figure",
      tags=["social engineering", "manipulation", "puppet", "puppeteer", "phishing", "human hacking", "deception"])
def _(S):
    return [
        shell(circle(12, 3.6, 1.7)),
        line(seg(12, 5.3, 12, 8)),
        line(seg(6, 8, 18, 8)),
        line(seg(6, 8, 9.3, 16.5)), line(seg(18, 8, 14.7, 16.5)), line(seg(12, 8, 12, 12.4)),
        dot(12, 14.2, 1.8),
        line(seg(9.3, 16.5, 14.7, 16.5)),
        line(seg(12, 16.5, 12, 19.3)),
        line(poly([(9.3, 22), (12, 19.3), (14.7, 22)])),
    ]


@icon("malware-analysis", CAT, "Microscope seen from the side with a small bug on the stage under the lens",
      tags=["malware analysis", "reverse engineering", "virus analysis", "bug", "microscope", "threat research", "sandbox"])
def _(S):
    tube = rotp([(9.3, 2.5), (13.7, 2.5), (13.7, 9.5), (9.3, 9.5)], -18, 11.5, 6)
    return [
        shell(poly(tube, closed=True, r=S.r * 0.4)),
        line("M20 21.5C21.5 15 20 10 16.5 6.5"),
        line(seg(4, 21.5, 20.5, 21.5)),
        line(seg(4.5, 17, 18, 17)),
        Part("solid", ellipse(9, 14.4, 2.2, 1.5)),
        line(seg(7, 12.8, 8, 13.5)), line(seg(11, 12.8, 10, 13.5)),
    ]


@icon("data-diode", CAT, "Box with one arrow passing through left to right and a barrier blocking the reverse direction",
      tags=["data diode", "one way transfer", "unidirectional gateway", "air gap", "network security", "one-way", "industrial security"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 17, rr(S, 2.5))),
        detail(seg(6, 9, 18, 9)), head(S, 18.4, 9, 0, 3, kind=detail),
        detail(seg(17.5, 15.2, 11, 15.2)), head(S, 10.6, 15.2, 180, 3, kind=detail),
        detail(seg(6.5, 12.3, 6.5, 18.2)),
    ]


@icon("photo-metadata", CAT, "Photo with a mountain and sun and a tag attached at its corner",
      tags=["photo metadata", "exif", "geotag", "image data", "location tag", "picture info", "hidden photo data"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 15.5, 13, rr(S, 2))),
        dot(6.5, 7.5, 1.4),
        detail(poly([(4, 14.5), (8.5, 10.5), (11, 13), (13, 11), (16.5, 14.5)])),
        shell(poly([(13.5, 13.5), (21.5, 13.5), (21.5, 21.5), (13.5, 21.5), (11.5, 17.5)], closed=True, r=S.r * 0.4)),
        dot(14.6, 17.5, 0.9),
        detail(seg(17.5, 16.3, 19.5, 16.3)), detail(seg(17.5, 19, 19.5, 19)),
    ]


@icon("censorship", CAT, "Speech bubble with a solid black bar across its middle hiding the text",
      tags=["censorship", "redacted", "censored", "blocked speech", "black bar", "free speech", "bleep"])
def _(S):
    return [
        shell(poly([(3, 3), (21, 3), (21, 16.5), (11.5, 16.5), (7, 21), (7, 16.5), (3, 16.5)], closed=True, r=S.r)),
        Part("dot", rect(5.5, 7, 13, 3.6, rr(S, 1))),
    ]


@icon("credit-freeze", CAT, "Credit card encased in an ice cube outline with a small snowflake at the corner",
      tags=["credit freeze", "security freeze", "frozen credit", "identity theft protection", "ice", "card lock", "snowflake"])
def _(S):
    return [
        shell(rect(2.5, 7, 16, 14, rr(S, 3.5))),
        shell(rect(6, 11, 9, 6, rr(S, 1))),
        detail(seg(6, 13.3, 15, 13.3)),
        line(seg(19.5, 2.5, 19.5, 8)), line(seg(16.8, 4, 22.2, 6.5)), line(seg(22.2, 4, 16.8, 6.5)),
    ]


@icon("cipher-table", CAT, "Square grid of letter cells with the top row and left column shaded as keys",
      tags=["cipher table", "vigenere", "tabula recta", "letter grid", "substitution table", "cryptography", "key square"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(7.5, 3, 7.5, 21)), detail(seg(12, 3, 12, 21)), detail(seg(16.5, 3, 16.5, 21)),
        detail(seg(3, 7.5, 21, 7.5)), detail(seg(3, 12, 21, 12)), detail(seg(3, 16.5, 21, 16.5)),
        Part("dot", rect(8.5, 4, 11.5, 2.6)), Part("dot", rect(4, 8.5, 2.6, 11.5)),
    ]


@icon("pigpen-cipher", CAT, "Tic-tac-toe grid beside an X shape, with dots placed in some compartments",
      tags=["pigpen cipher", "masonic cipher", "freemason cipher", "grid cipher", "secret alphabet", "tic tac toe", "code symbols"])
def _(S):
    return [
        line(seg(6.5, 2.5, 6.5, 13.5)), line(seg(10.5, 2.5, 10.5, 13.5)),
        line(seg(2.5, 6.5, 13.5, 6.5)), line(seg(2.5, 10.5, 13.5, 10.5)),
        dot(8.5, 8.5, 1.0),
        line(seg(14.5, 14.5, 21.5, 21.5)), line(seg(21.5, 14.5, 14.5, 21.5)),
        dot(18, 17.4, 0.9),
    ]


@icon("keypad-usb-drive", CAT, "Chunky USB drive with a small numeric keypad on its body and a status light",
      tags=["encrypted usb", "keypad usb", "secure flash drive", "pin usb", "hardware encrypted drive", "pen drive", "secure storage"])
def _(S):
    return [
        shell(rect(2.5, 6.5, 14.5, 11, rr(S, 2.5))),
        shell(rect(17, 9.5, 4.5, 5, rr(S, 1))),
        dot(6, 10.3, 1.1), dot(9.5, 10.3, 1.1), dot(13, 10.3, 1.1),
        dot(6, 13.8, 1.1), dot(9.5, 13.8, 1.1),
        detail(seg(12.3, 13.8, 13.7, 13.8)),
    ]


@icon("open-safe", CAT, "Safe with its door swung open showing a shelf with stacked gold bars",
      tags=["open safe", "vault", "gold bars", "treasure", "strongbox", "unlocked safe", "valuables"])
def _(S):
    return [
        shell(rect(3, 3.5, 13, 17, rr(S, 1.5))),
        detail(seg(3, 12, 16, 12)),
        Part("dot", rect(5.5, 8, 4, 2.8)), Part("dot", rect(10.5, 8, 3.5, 2.8)),
        Part("dot", rect(5.5, 15.3, 4, 3)), Part("dot", rect(10.5, 15.3, 3.5, 3)),
        shell(poly([(18, 4.5), (21.5, 6), (21.5, 18), (18, 19.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("forensic-uv-light", CAT, "Handheld flashlight shining a cone of light that reveals a partial fingerprint",
      tags=["uv light", "forensic light", "fingerprint reveal", "black light", "crime scene", "latent print", "flashlight"])
def _(S):
    torch = rotp([(4.2, 0.5), (7.8, 0.5), (7.8, 7), (9.4, 7), (9.4, 11), (2.6, 11), (2.6, 7), (4.2, 7)], -45, 6, 6)
    torch = [(x + 1.4, y + 1.4) for x, y in torch]
    return [
        shell(poly(torch, closed=True, r=S.r * 0.4)),
        line(seg(12.7, 9.6, 21.5, 12)),
        line(seg(9.6, 12.7, 12, 21.5)),
        dot(16, 16, 1.2),
        line(arc(16, 16, 4.3, 190, 300)),
    ]


@icon("composite-sketch", CAT, "Sketch pad with a simple face drawing and a pencil beside it",
      tags=["composite sketch", "police sketch", "suspect drawing", "facial composite", "identikit", "witness drawing", "pencil"])
def _(S):
    return [
        shell(rect(2.5, 3, 13, 18, rr(S, 2))),
        detail(face(S, 9, 11.5, 3.3, 5)),
        dot(7.7, 10, 0.9), dot(10.3, 10, 0.9),
        detail(seg(8, 14, 10, 14)),
        shell(poly([(18, 3), (21.5, 3), (21.5, 14.5), (19.75, 19), (18, 14.5)], closed=True, r=S.r * 0.4)),
        detail(seg(18, 7, 21.5, 7)),
    ]


@icon("stakeout", CAT, "Side view of a parked car with binoculars poking out of the driver window",
      tags=["stakeout", "surveillance car", "spying", "binoculars", "detective", "parked car", "observation"])
def _(S):
    return [
        shell(poly([(2.5, 16.5), (2.5, 13), (6, 12.5), (8.5, 9), (15.5, 9), (18.5, 12.5), (21.5, 13), (21.5, 16.5)], closed=True, r=S.r)),
        Part("solid", circle(7, 17, 2.4)), Part("solid", circle(17, 17, 2.4)),
        shell(poly(rotp([(10.5, 9.5), (10.5, 6), (9, 6), (9, 2.2), (15, 2.2), (15, 6), (13.5, 6), (13.5, 9.5)], -32, 12, 9.5), closed=True, r=S.r * 0.3)),
    ]


@icon("bulletproof-glass", CAT, "Thick window pane in a frame with a bullet impact ring whose cracks stay in one spot",
      tags=["bulletproof glass", "ballistic glass", "armored window", "impact", "shatterproof", "security glazing", "bullet resistant"])
def _(S):
    spokes = [detail(seg(*polar(12, 12, 6.4, a), *polar(12, 12, 9.2, a))) for a in (45, 135, 225, 315)]
    return [
        shell(rect(2.5, 2.5, 19, 19, S.R)),
        dot(12, 12, 1.5),
        detail(circle(12, 12, 3.8)),
    ] + spokes


@icon("alarm-zone-map", CAT, "Floor plan with three rooms, each marked by a sensor dot with a small wave arc",
      tags=["alarm zones", "floor plan", "sensors", "motion detector", "intruder alarm", "security zones", "building security"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 17, rr(S, 2))),
        detail(seg(11, 3.5, 11, 20.5)),
        detail(seg(11, 12, 21.5, 12)),
        dot(5.8, 12, 1.1), line(arc(5.8, 12, 2.6, -55, 55)),
        dot(14.3, 7.7, 1.1), line(arc(14.3, 7.7, 2.6, -55, 55)),
        dot(14.3, 16.3, 1.1), line(arc(14.3, 16.3, 2.6, -55, 55)),
    ]


@icon("email-alias", CAT, "Envelope marked with an at sign and a curved arrow looping to a second smaller envelope",
      tags=["email alias", "forwarding address", "masked email", "burner email", "relay address", "plus address", "hide my email"])
def _(S):
    return [
        shell(rect(2.5, 3, 14.5, 10.5, rr(S, 2))),
        detail(circle(9.75, 8.2, 1.6)),
        detail(seg(11.6, 7.2, 11.6, 9.4)),
        line("M6.5 15.5Q6.5 20 12.5 19.5"),
        head(S, 13.4, 19.5, 0, 2.8),
        shell(rect(15.5, 15, 6, 5.5, rr(S, 1.2))),
    ]


@icon("strike-plate", CAT, "Vertical door frame plate with two screw holes and a rectangular latch opening",
      tags=["strike plate", "door frame plate", "latch plate", "deadbolt", "door reinforcement", "break in", "door hardware"])
def _(S):
    return [
        shell(rect(6.5, 2.5, 11, 19, S.R)),
        dot(12, 5.9, 1.3), dot(12, 18.1, 1.3),
        detail(rect(9.5, 9.3, 5, 5.4, rr(S, 1))),
    ]


@icon("bolt-seal", CAT, "Steel bolt seal with a round headed pin pushed into a barrel locking body",
      tags=["bolt seal", "container seal", "shipping seal", "tamper evident", "freight security", "high security seal", "pin lock"])
def _(S):
    return [
        shell(circle(5, 12, 3.4)),
        line(seg(8.4, 12, 14, 12)),
        shell(rect(13, 7.5, 8.5, 9, rr(S, 2))),
        detail(seg(17.2, 7.5, 17.2, 16.5)),
    ]


@icon("panopticon", CAT, "Top view of a round prison ring of cells around a central watchtower",
      tags=["panopticon", "surveillance architecture", "prison design", "watchtower", "constant observation", "circular prison", "big brother"])
def _(S):
    r0, r1 = (5.6, 9.5) if S.name == "line" else (6.7, 8.4)
    spokes = [detail(seg(*polar(12, 12, r0, a), *polar(12, 12, r1, a))) for a in range(22, 360, 45)]
    ring = poly([polar(12, 12, 10 if S.name == "line" else 9.6, -90 + i * 30) for i in range(12)], closed=True, r=S.r)
    return [shell(ring), detail(circle(12, 12, 5.5)), dot(12, 12, 1.6)] + spokes


@icon("shrouded-padlock", CAT, "Squat padlock whose body rises on both sides to shield most of the short shackle",
      tags=["shrouded padlock", "high security padlock", "protected shackle", "bolt cutter resistant", "lock", "heavy duty lock", "disc lock"])
def _(S):
    return [
        shell(poly([(3, 21.5), (3, 4.5), (7.5, 4.5), (7.5, 9.5), (16.5, 9.5), (16.5, 4.5), (21, 4.5), (21, 21.5)], closed=True, r=S.r)),
        line(poly([(10.5, 9.5), (10.5, 7), (13.5, 7), (13.5, 9.5)])),
        dot(12, 14.5, 1.5),
        detail(seg(12, 15.5, 12, 18.5)),
    ]


@icon("laser-microphone", CAT, "Small box device aiming a dashed laser beam at a window pane with the beam bouncing back",
      tags=["laser microphone", "eavesdropping", "window vibration", "long range bug", "espionage", "listening device", "spy tech"])
def _(S):
    return [
        shell(rect(2.5, 12.5, 6.5, 9, rr(S, 1.5))),
        dot(5.75, 17, 1.2),
        shell(rect(17.5, 3, 4, 18, rr(S, 1))),
        line(seg(10, 14.6, 12, 13.6)), line(seg(14, 12.6, 16, 11.6)),
        line(seg(15.3, 9.2, 13.3, 8.3)), line(seg(11.3, 7.4, 9.5, 6.5)),
    ]


def _syr(tip, u, v):
    a = math.radians(-45)
    return (tip[0] + u * math.cos(a) - v * math.sin(a), tip[1] + u * math.sin(a) + v * math.cos(a))


@icon("prompt-injection", CAT, "Chat bubble with a syringe needle pushing into its side",
      tags=["prompt injection", "ai attack", "llm security", "jailbreak prompt", "malicious instruction", "chatbot", "syringe"])
def _(S):
    tip = (12.5, 12.5)
    P_ = lambda u, v: _syr(tip, u, v)
    return [
        shell(poly([(2.5, 7), (14.5, 7), (14.5, 17), (8, 17), (5, 20.5), (5, 17), (2.5, 17)], closed=True, r=S.r)),
        detail(seg(5.5, 10.5, 11.5, 10.5)),
        line(poly([P_(0, 0), P_(3.2, 0)])),
        shell(poly([P_(3.2, -2), P_(9.5, -2), P_(9.5, 2), P_(3.2, 2)], closed=True, r=S.r * 0.4)),
        line(poly([P_(9.5, 0), P_(12.2, 0)])),
        line(poly([P_(12.2, -2.4), P_(12.2, 2.4)])),
    ]


@icon("device-jailbreak", CAT, "Smartphone with a broken chain wrapped around it, one link snapped open",
      tags=["jailbreak", "root", "device unlock", "broken chain", "bypass restrictions", "phone hacking", "unlocked phone"])
def _(S):
    return [
        shell(rect(7.5, 2.5, 9, 19, rr(S, 2.5))),
        detail(seg(11, 5.5, 13, 5.5)),
        line(seg(7.5, 12, 16.5, 12)),
        line(ellipse(4.6, 12, 2.8, 1.8)),
        line(arc(19.4, 12, 2.6, 40, 320)),
    ]


@icon("drink-cover", CAT, "Tall glass with a stretchy fabric cap over its rim and a straw poking through a small hole",
      tags=["drink cover", "drink spiking", "glass cover", "scrunchie lid", "safe drink", "nightlife safety", "straw"])
def _(S):
    return [
        shell(poly([(6.5, 8.5), (17.5, 8.5), (16, 21.5), (8, 21.5)], closed=True, r=S.r * 0.5)),
        line("M5 8.5Q12 3.5 19 8.5"),
        line(poly([(13, 5.8), (15.5, 2.5)])),
        detail(seg(7.8, 14, 16.2, 14)),
    ]


@icon("usb-data-blocker", CAT, "Small USB adapter plug with a shield on its body, sitting between a cable and a port",
      tags=["usb data blocker", "juice jacking", "charge only", "usb condom", "safe charging", "public charging", "data protection"])
def _(S):
    return [
        line(seg(1.5, 12, 5.5, 12)),
        shell(rect(5.5, 5, 11, 14, rr(S, 2.5))),
        Part("dot", poly([(8.8, 8), (13.2, 8), (13.2, 12.2), (11, 15.5), (8.8, 12.2)], closed=True, r=S.r * 0.4)),
        shell(rect(16.5, 9.2, 5.5, 5.6, rr(S, 1))),
    ]


@icon("security-screw", CAT, "Screw head seen from above with a six point star recess and a pin in its centre",
      tags=["security screw", "torx pin", "tamper proof screw", "anti theft fastener", "star recess", "tamper resistant", "fastener"])
def _(S):
    pts = [polar(12, 12, 6.3 if i % 2 == 0 else 3.9, -90 + i * 30) for i in range(12)]
    return [
        shell(circle(12, 12, 9.5)),
        detail(poly(pts, closed=True, r=S.r * 0.6)),
        dot(12, 12, 1.1),
    ]


# ============================================================================ chunk 5

@icon("asset-tag", CAT, "Rectangular label with a barcode and a number line stuck on the corner of a laptop",
      tags=["asset tag", "inventory label", "barcode sticker", "property tag", "equipment tracking", "laptop label", "serial number"])
def _(S):
    return [
        shell(rect(4, 2.5, 15, 9.5, rr(S, 2))),
        line(poly([(2, 15.5), (22, 15.5)])),
        shell(rect(11, 11.5, 11, 10, rr(S, 1.5))),
        Part("dot", rect(13, 13.5, 1.4, 3.6)), Part("dot", rect(15.6, 13.5, 1, 3.6)),
        Part("dot", rect(17.4, 13.5, 1.8, 3.6)), Part("dot", rect(19.8, 13.5, 1, 3.6)),
        detail(seg(13, 19.3, 20, 19.3)),
    ]


@icon("key-impression", CAT, "Wax block with a key shaped imprint pressed into it and a key lifting away above",
      tags=["key impression", "key copy", "key duplication", "wax mold", "key cloning", "lock picking", "key mould"])
def _(S):
    return [
        shell(circle(7.5, 5.5, 2.5)),
        line(seg(10, 5.5, 18, 5.5)),
        line(seg(15.5, 5.5, 15.5, 8)),
        shell(rect(2.5, 11.5, 19, 10, rr(S, 2))),
        dot(7.5, 16.5, 1.6),
        detail(seg(7.5, 16.5, 17.5, 16.5)),
    ]


@icon("locked-display-case", CAT, "Glass cabinet with two shelves of items and a small keyhole lock on its front",
      tags=["display case", "glass cabinet", "locked cabinet", "museum case", "showcase", "trophy case", "jewelry case"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 19, S.R)),
        detail(seg(3.5, 9.8, 20.5, 9.8)),
        detail(seg(3.5, 16, 20.5, 16)),
        Part("dot", rect(6.5, 5.6, 3, 2.8)), Part("dot", circle(14.5, 7, 1.5)),
        Part("dot", circle(8, 12.6, 1.4)), Part("dot", rect(12, 11.5, 3, 2.4)),
        dot(12, 19, 1.1),
    ]


@icon("apartment-entry-panel", CAT, "Wall panel with a camera lens at the top, a speaker slot and a grid of call buttons",
      tags=["entry panel", "intercom", "door buzzer", "video doorbell", "apartment intercom", "call buttons", "door phone"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 13, 19, rr(S, 2.5))),
        dot(12, 6.2, 1.8),
        detail(seg(8.5, 10.5, 15.5, 10.5)),
        dot(9.5, 15, 1.1), dot(14.5, 15, 1.1), dot(9.5, 18.2, 1.1), dot(14.5, 18.2, 1.1),
    ]


@icon("key-fingerprint", CAT, "Key whose round bow contains a small fingerprint whorl, with the blade pointing to the lower right",
      tags=["biometric key", "fingerprint key", "digital key", "smart key", "key", "biometric access", "authentication"])
def _(S):
    return [
        shell(circle(8.5, 8.5, 6.2)),
        dot(8.5, 8.5, 1), detail(arc(8.5, 8.5, 3.2, 160, 400)),
        line(seg(13, 13, 21, 21)),
        line(seg(16.4, 16.4, 14.4, 18.4)), line(seg(19.4, 19.4, 17.4, 21.4)),
    ]


@icon("guilloche-rosette", CAT, "Round rosette of overlapping looped lines, like the security pattern printed on banknotes",
      tags=["guilloche", "rosette", "security pattern", "banknote pattern", "anti counterfeit", "spirograph", "engraving"])
def _(S):
    out = []
    for a in (0, 60, 120):
        d = "M2.5 12Q12 6.2 21.5 12Q12 17.8 2.5 12Z" if S.name == "line" else ellipse(12, 12, 9.5, 4.2)
        out.append(line(path_to_d(transform_path(P(d), rotation(a, 12, 12)))))
    return out


@icon("group-lockout-hasp", CAT, "Scissor style lockout hasp with a round jaw at the top and three small padlocks hanging from it",
      tags=["lockout hasp", "lockout tagout", "loto", "group lock", "safety lock", "multi lock hasp", "padlock"])
def _(S):
    return [
        shell(circle(12, 5, 3.2)),
        line(seg(12, 8.2, 12, 9.5)),
        shell(rect(2.5, 9.5, 19, 3.2, rr(S, 1))),
        line(seg(5.5, 12.7, 5.5, 14.5)), line(seg(12, 12.7, 12, 14.5)), line(seg(18.5, 12.7, 18.5, 14.5)),
        shell(rect(3.2, 14.5, 4.6, 6.5, rr(S, 1.2))),
        shell(rect(9.7, 14.5, 4.6, 6.5, rr(S, 1.2))),
        shell(rect(16.2, 14.5, 4.6, 6.5, rr(S, 1.2))),
    ]


@icon("cyberbullying", CAT, "Smartphone with an angry jagged speech burst pointing toward a small sad face",
      tags=["cyberbullying", "online harassment", "trolling", "abusive messages", "hate message", "bullying", "digital abuse"])
def _(S):
    burst = [polar(14.5, 7.6, 4.7 if i % 2 == 0 else 2.8, -90 + i * 36) for i in range(10)]
    return [
        shell(rect(2.5, 8.5, 7.5, 13, rr(S, 2))),
        detail(seg(5, 18.5, 7.5, 18.5)),
        shell(poly(burst, closed=True, r=S.r * 0.4)),
        shell(circle(17, 17, 4.2)),
        dot(15.7, 16, 0.8), dot(18.3, 16, 0.8),
        line(arc(17, 20.6, 1.9, 205, 335)),
    ]


@icon("doxxing", CAT, "Profile card with an avatar and text lines beside a map pin with a house popping out of it",
      tags=["doxxing", "doxing", "address leak", "personal information leak", "home address", "privacy violation", "exposed details"])
def _(S):
    return [
        shell(rect(2.5, 3, 13.5, 12, rr(S, 2))),
        dot(7, 7.7, 1.7),
        detail(seg(5, 11.5, 11, 11.5)),
        shell("M18 22C14.8 18.2 14 16.3 14 14.2A4 4 0 0 1 22 14.2C22 16.3 21.2 18.2 18 22Z"),
        Part("dot", poly([(16, 14.8), (18, 12.6), (20, 14.8), (20, 16.4), (16, 16.4)], closed=True)),
    ]


@icon("catfishing", CAT, "Profile photo frame with a fish silhouette in place of a face and text lines beneath",
      tags=["catfishing", "fake profile", "fake identity", "online deception", "romance scam", "fish", "impersonation"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 13.5, rr(S, 2.5))),
        Part("dot", ellipse(10.8, 9.2, 4, 2.7)),
        Part("dot", poly([(13.8, 9.2), (17.4, 6.4), (17.4, 12)], closed=True)),
        line(seg(4.5, 18.5, 19.5, 18.5)),
        line(seg(4.5, 21.3, 12.5, 21.3)),
    ]


@icon("cell-triangulation", CAT, "Three cell areas around three towers overlapping at one central point",
      tags=["cell triangulation", "location tracking", "tower tracking", "phone location", "cell site", "signal trilateration", "positioning"])
def _(S):
    cs = [(12, 8), (7.5, 16), (16.5, 16)]
    out = []
    for cx, cy in cs:
        out.append(shell(poly([polar(cx, cy, 5.6, -90 + i * 60) for i in range(6)], closed=True, r=S.r)))
    return out + [dot(cx, cy, 1.3) for cx, cy in cs]


@icon("id-card-printer", CAT, "Compact desktop printer with an ID card with photo sliding out of its front slot",
      tags=["id card printer", "badge printer", "card printer", "photo id", "access badge", "employee badge", "printing"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 11.5, rr(S, 2.5))),
        detail(seg(5.5, 7, 18.5, 7)),
        line(poly([(7, 13), (7, 21.5), (17, 21.5), (17, 13)])),
        dot(10.5, 17, 1.5),
        line(seg(13.3, 16.5, 14.6, 16.5)), line(seg(13.3, 19, 14.6, 19)),
    ]


@icon("cipher-cylinder", CAT, "Stack of thin lettered discs on a central axle, each disc turned a little differently",
      tags=["cipher cylinder", "wheel cipher", "jefferson disk", "encryption device", "rotating discs", "mechanical cipher", "cryptex"])
def _(S):
    return [
        shell(rect(4, 5.5, 16, 13, rr(S, 2.5))),
        detail(seg(8, 5.5, 8, 18.5)), detail(seg(12, 5.5, 12, 18.5)), detail(seg(16, 5.5, 16, 18.5)),
        dot(6, 9, 0.9), dot(10, 14.5, 0.9), dot(14, 9.5, 0.9), dot(18, 15, 0.9),
        line(seg(1.5, 12, 4, 12)), line(seg(20, 12, 22.5, 12)),
    ]


@icon("package-theft", CAT, "Parcel box on a doorstep with a hand reaching down from above to grab it",
      tags=["package theft", "porch pirate", "parcel theft", "stolen delivery", "grab and run", "doorstep", "hand"])
def _(S):
    return [
        shell(rect(6.5, 2.5, 11, 5, rr(S, 2.5))),
        line(seg(9, 7.5, 9, 10.8)), line(seg(12, 7.5, 12, 10.8)), line(seg(15, 7.5, 15, 10.8)),
        shell(rect(3.5, 12.5, 17, 9, rr(S, 1.5))),
        detail(seg(12, 12.5, 12, 17)),
    ]


@icon("bike-theft", CAT, "Bicycle side view with a cut U-lock beside it, one prong snapped short",
      tags=["bike theft", "bicycle theft", "cut lock", "broken lock", "stolen bike", "u lock", "cycling security"])
def _(S):
    return [
        shell(circle(6, 16.5, 4.2)), shell(circle(18, 16.5, 4.2)),
        line(poly([(6, 16.5), (9.5, 10), (16, 10), (18, 16.5)])),
        line(poly([(9.5, 10), (11.5, 16.5), (16, 10)])),
        line(seg(8, 8, 11, 8)),
        line("M15.5 8L17.5 5.5H20"),
        line("M3.5 2.5V6A2.5 2.5 0 0 0 8.5 6V4"),
    ]


@icon("dead-drop-spike", CAT, "Hollow metal spike pushed into the ground with its cap lifted off and a rolled note inside",
      tags=["dead drop", "spy drop", "hidden message", "ground spike", "secret handoff", "geocache", "espionage"])
def _(S):
    return [
        shell(poly([(8.5, 9), (15.5, 9), (15.5, 16), (12, 21.5), (8.5, 16)], closed=True, r=S.r * 0.4)),
        line(seg(2.5, 13.5, 6, 13.5)), line(seg(18, 13.5, 21.5, 13.5)),
        line(seg(8, 2.5, 16, 2.5)),
        Part("solid", rect(10.5, 4.8, 3, 5, 1.1)),
    ]


def _cloud():
    return path_to_d(U(P(circle(10.5, 17.5, 3.4)), P(circle(15, 14.8, 4.6)), P(circle(19.2, 18.2, 2.9)), P(rect(10.5, 17, 8.7, 4.2, 0))))


@icon("security-fog-machine", CAT, "Wall mounted box blowing a large billowing cloud of fog from its nozzle",
      tags=["fog machine", "security fog", "fog cannon", "burglar deterrent", "smoke screen", "anti theft", "vault protection"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 8.5, 6, rr(S, 2))),
        line(seg(11, 5.5, 13, 5.5)),
        shell(_cloud()),
    ]


@icon("visitor-log", CAT, "Open sign-in book with ruled rows and a pen on a chain lying across it",
      tags=["visitor log", "sign in sheet", "guest book", "visitor book", "check in", "register", "front desk"])
def _(S):
    return [
        shell(poly([(2.5, 5), (12, 7), (21.5, 5), (21.5, 19), (12, 21), (2.5, 19)], closed=True, r=S.r)),
        detail(seg(12, 7, 12, 21)),
        detail(seg(5, 10.8, 9.5, 11.6)), detail(seg(5, 14.6, 9.5, 15.4)),
        detail(seg(14.5, 12.5, 19, 11.7)), detail(seg(14.5, 16.3, 19, 15.5)),
        line(seg(17, 8.2, 14.2, 13.2)),
    ]


@icon("security-robot", CAT, "Cone shaped wheeled patrol robot with a camera dome on top and a light band around its middle",
      tags=["security robot", "patrol robot", "guard robot", "autonomous patrol", "surveillance robot", "robotic guard", "cone robot"])
def _(S):
    return [
        shell(arc(12, 9, 3.8, 180, 360) + "Z"),
        shell(poly([(8, 9), (16, 9), (19, 19), (5, 19)], closed=True, r=S.r * 0.5)),
        detail(seg(6.3, 14, 17.7, 14)),
        dot(12, 6.2, 1),
        Part("solid", circle(8, 20.7, 1.5)), Part("solid", circle(16, 20.7, 1.5)),
    ]


@icon("cctv-joystick-controller", CAT, "Control desk unit with a tall joystick on the right and a display and keys on the left",
      tags=["cctv controller", "ptz joystick", "camera control", "security console", "joystick", "surveillance desk", "control panel"])
def _(S):
    return [
        shell(rect(2.5, 12.5, 19, 9, rr(S, 2.5))),
        detail(rect(5, 14.5, 7.5, 3.2, rr(S, 0.6))),
        dot(6, 19.8, 0.9), dot(9, 19.8, 0.9), dot(12, 19.8, 0.9),
        line(seg(17, 12.5, 17, 6.5)),
        shell(circle(17, 4.6, 2.3)),
    ]
