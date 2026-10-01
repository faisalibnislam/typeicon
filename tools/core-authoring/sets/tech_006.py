"""TypeIcon Core: tech (batch 006)."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "tech"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, n):
    return min(S.R, n)


def head(S, x, y, deg, size=2.6):
    """Open arrowhead whose tip is at (x, y) and which points along deg (0 = right, 90 = down)."""
    pts = [(x + size * math.cos(math.radians(deg + 180 + a)), y + size * math.sin(math.radians(deg + 180 + a)))
           for a in (-40, 40)]
    return line(poly([pts[0], (x, y), pts[1]], r=min(S.r, 0.6)))


def chev(S, pts):
    return line(poly(pts, r=S.r))


def rot(d, deg, cx, cy):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def doc_d(S, x, y, w, h, c=4):
    return poly([(x, y), (x + w - c, y), (x + w, y + c), (x + w, y + h), (x, y + h)], closed=True, r=S.r)


_BRAIN = ("M6.5 17C4.3 16.6 3 14.8 3 12.8C3 11.3 3.6 10.2 4.5 9.5C4.3 6.6 6.4 4.5 9 4.5C10.2 3.6 11.5 3.2 13 3.3"
          "C15.3 3.4 17 4.6 17.8 6.3C19.9 7 21 8.8 21 10.8C21 13.3 19.2 15.2 16.8 15.4C16.3 16.8 15 17.7 13.5 17.7L11 17.4Z")
_BRAIN_FOLDS = ["M7.5 9.3C8.3 8.2 9.8 8 11 8.7", "M12.5 6.5C13.8 7 14.4 8.2 14.2 9.5",
                "M8 13C9.3 13.8 11 13.6 12 12.5", "M15.5 11.5C16.8 11.5 17.8 10.8 18.3 9.8"]


def _brain_tr(d, cx, cy, w):
    s = w / 18.0
    return path_to_d(transform_path(P(d), (s, 0, 0, s, cx - 12 * s, cy - 10.5 * s)))


def brain_d(cx, cy, w):
    """Side view brain (with stem) of width w centred on (cx, cy)."""
    return _brain_tr(_BRAIN, cx, cy, w)


def brain_folds(cx, cy, w, n=4):
    return [_brain_tr(f, cx, cy, w) for f in _BRAIN_FOLDS[:n]]


def brain_solid(cx, cy, w, k=1.0):
    """Solid brain with a fold knocked out (for small brains)."""
    cut = _brain_tr("M8.5 9C10 10 10.5 11.5 9.5 13", cx, cy, w)
    cut2 = _brain_tr("M13 6.5C14.5 8 14.5 10 13.5 11.5", cx, cy, w)
    return path_to_d(D(P(brain_d(cx, cy, w)), ST(cut, k, "butt", "miter"), ST(cut2, k, "butt", "miter")))


def cyl(S, x, y, w, h, ry=1.5):
    """Small database cylinder: returns (outline, front-of-lid arc)."""
    r = w / 2
    out = (f"M{fmt(x)} {fmt(y + ry)}A{fmt(r)} {fmt(ry)} 0 0 1 {fmt(x + w)} {fmt(y + ry)}V{fmt(y + h - ry)}"
           f"A{fmt(r)} {fmt(ry)} 0 0 1 {fmt(x)} {fmt(y + h - ry)}Z")
    lid = f"M{fmt(x)} {fmt(y + ry)}A{fmt(r)} {fmt(ry)} 0 0 0 {fmt(x + w)} {fmt(y + ry)}"
    return out, lid


# ---------------------------------------------------------------------------

@icon("symlink", CAT, "Document page with a chain link curling off its lower corner",
      tags=["symbolic link", "shortcut", "file link", "alias", "soft link", "ln -s"])
def _(S):
    return [shell(doc_d(S, 3, 2, 10, 13, 4)), detail(seg(6, 8, 10, 8)), detail(seg(6, 11, 8.5, 11)),
            *_chain(S, 17.5, 17.5)]


def _chain(S, cx, cy):
    def lk(sx):
        o = f"M{fmt(cx + sx * 0.6)} {fmt(cy - 2.5)}H{fmt(cx + sx * 3.2)}A2.5 2.5 0 0 {0 if sx < 0 else 1} {fmt(cx + sx * 3.2)} {fmt(cy + 2.5)}H{fmt(cx + sx * 0.6)}"
        return line(rot(o, -45, cx, cy))
    return [lk(-1), lk(1), line(rot(f"M{fmt(cx - 1.8)} {fmt(cy)}H{fmt(cx + 1.8)}", -45, cx, cy))]


@icon("file-permissions", CAT, "Document page holding three rows, each with a check mark and a short line",
      tags=["file access", "chmod", "access rights", "read write execute", "file mode", "allowed"])
def _(S):
    out = [shell(doc_d(S, 4.5, 2, 15, 20, 5))]
    for y in (10, 14.5, 19):
        out += [detail(poly([(7.5, y - 0.2), (8.8, y + 1.2), (11, y - 1.6)], r=0)), detail(seg(13.5, y, 16.5, y))]
    return out


@icon("split-terminal", CAT, "Terminal window divided into two side by side panes, each with a prompt chevron",
      tags=["tmux", "panes", "command line", "shell", "console", "split view"])
def _(S):
    return [shell(rect(2, 4, 20, 16, rr(S, 3))), detail(seg(12, 4, 12, 20)),
            detail(poly([(5, 9), (7.5, 12), (5, 15)], r=S.r * 0.4)), detail(poly([(15, 9), (17.5, 12), (15, 15)], r=S.r * 0.4))]


@icon("line-numbers", CAT, "Column of numbered markers beside short lines of text",
      tags=["gutter", "code editor", "row numbers", "source code", "text editor", "line count"])
def _(S):
    out = [line(seg(8.5, 2.5, 8.5, 21.5))]
    for y, x2 in ((5, 20), (10, 17), (15, 21), (20, 15)):
        out += [dot(4, y, 1.4), line(seg(12, y, x2, y))]
    return out


@icon("code-minimap", CAT, "Editor window with code lines on the left and a narrow overview strip with a viewport box on the right",
      tags=["code overview", "editor map", "scroll map", "minimap", "viewport", "source code"])
def _(S):
    return [shell(rect(2, 3, 20, 18, rr(S, 3))), detail(seg(14.5, 3, 14.5, 21)),
            detail(seg(5.5, 8, 11, 8)), detail(seg(5.5, 12, 9, 12)), detail(seg(5.5, 16, 11, 16)),
            Part("dot", rect(16.5, 8.5, 3.5, 7, 0.5))]


@icon("single-sign-on", CAT, "One key with three lines fanning out to three small app windows",
      tags=["sso", "one login", "shared login", "identity", "authentication", "access"])
def _(S):
    out = [shell(circle(4.8, 12, 2.8)), line(seg(7.6, 12, 10, 12))]
    for y in (4.5, 12, 19.5):
        out += [line(poly([(10, 12), (16, y)])), shell(rect(16, y - 2.5, 6, 5, L(S, 0.5, 2)))]
    return out


@icon("mac-address", CAT, "Network adapter chip with pins on both sides above groups of dot pairs separated by colons",
      tags=["hardware address", "network adapter", "nic", "physical address", "ethernet", "identifier"])
def _(S):
    out = [shell(rect(6.5, 2.5, 11, 10, rr(S, 2))), detail(seg(9.5, 7.5, 14.5, 7.5))]
    for y in (5.5, 9.5):
        out += [line(seg(2.5, y, 6.5, y)), line(seg(17.5, y, 21.5, y))]
    for x in (3, 5.4, 10.6, 13, 18.2, 20.6):
        out.append(dot(x, 19, 1.05))
    for x in (8, 15.6):
        out += [dot(x, 17.7, 0.85), dot(x, 20.3, 0.85)]
    return out


@icon("bastion-host", CAT, "Castle tower with a server box set into its base",
      tags=["jump box", "jump host", "gateway server", "secure access", "hardened server", "network security"])
def _(S):
    r = L(S, 0, 0.6)
    tower = [(6, 21), (6, 10), (4, 10), (4, 3), (8, 3), (8, 6), (10.5, 6), (10.5, 3), (13.5, 3), (13.5, 6), (16, 6),
             (16, 3), (20, 3), (20, 10), (18, 10), (18, 21)]
    return [shell(poly(tower, closed=True, r=r)), detail(rect(8.5, 13, 7, 5.5, rr(S, 1.5)))]


@icon("code-signing", CAT, "Angle brackets above a signature squiggle and a small seal",
      tags=["signed code", "digital signature", "code certificate", "publisher", "trusted code", "authenticode"])
def _(S):
    return [chev(S, [(8, 3), (3, 7.5), (8, 12)]), chev(S, [(16, 3), (21, 7.5), (16, 12)]),
            line("M2.5 19.5C4 16 6 16 6.5 19.5S9 22 11.5 17.5"),
            shell(poly([(18.5 + 3.3 * math.cos(math.radians(a)), 17.5 + 3.3 * math.sin(math.radians(a))) for a in range(0, 360, 45)], closed=True, r=S.r)),
            dot(18.5, 17.5, 0.9)]


@icon("software-bill-of-materials", CAT, "Clipboard list with a small package box beside each line",
      tags=["sbom", "dependency list", "component list", "supply chain", "inventory", "packages"])
def _(S):
    out = [shell(rect(4, 4, 16, 18, rr(S, 3))), shell(rect(9, 2, 6, 4, rr(S, 1.5)))]
    for y in (11, 15, 19):
        out += [Part("dot", rect(7, y - 1.5, 3, 3, 0.4)), detail(seg(12.5, y, 17, y))]
    return out


@icon("code-freeze", CAT, "Angle brackets with a snowflake between them",
      tags=["release freeze", "no deploys", "merge freeze", "feature freeze", "lockdown", "change window"])
def _(S):
    out = [chev(S, [(5.2, 6), (2.2, 12), (5.2, 18)]), chev(S, [(18.8, 6), (21.8, 12), (18.8, 18)])]
    for a in (90, 30, 150):
        dx, dy = 5.4 * math.cos(math.radians(a)), 5.4 * math.sin(math.radians(a))
        out.append(line(seg(12 - dx, 12 - dy, 12 + dx, 12 + dy)))
    return out


@icon("tokenizer", CAT, "A line of text split into three separate rounded token blocks",
      tags=["tokens", "text splitting", "nlp", "language model", "word pieces", "lexer"])
def _(S):
    r = L(S, 1.5, 3)
    return [shell(rect(2, 3.5, 9, 6.5, r)), shell(rect(13, 3.5, 9, 6.5, r)), shell(rect(2, 14, 12, 6.5, r)),
            line(seg(18, 14, 18, 20.5))]


@icon("model-quantization", CAT, "Stepped staircase bars with a smooth rising curve above them",
      tags=["quantisation", "low precision", "int8", "compression", "model size", "rounding"])
def _(S):
    steps = [(3, 21), (3, 17), (7.5, 17), (7.5, 13.5), (12, 13.5), (12, 10), (16.5, 10), (16.5, 6.5), (21, 6.5), (21, 21)]
    return [shell(poly(steps, closed=True, r=S.r * 0.5)), line("M3 11.5C10 11.5 12 3 21 2.5")]


@icon("knowledge-distillation", CAT, "Large brain on the left narrowing through a funnel into a small solid brain",
      tags=["teacher student", "model compression", "distil", "distillation", "small model", "transfer"])
def _(S):
    return [shell(brain_d(7, 12, 12.5)), *[detail(f) for f in brain_folds(7, 12, 12.5, 2)],
            shell(poly([(13.5, 7.5), (13.5, 16.5), (17.5, 13), (17.5, 11)], closed=True, r=S.r * 0.6)),
            Part("solid", brain_solid(20.2, 12, 5.2, 0.7))]


@icon("federated-learning", CAT, "Three small phones sending lines up to one central brain",
      tags=["distributed training", "on device learning", "privacy preserving", "edge devices", "collaborative model", "decentralized"])
def _(S):
    out = [shell(brain_d(12, 6.5, 11.5)), detail(brain_folds(12, 6.5, 11.5, 1)[0])]
    for x in (2.5, 9.5, 16.5):
        out.append(shell(rect(x, 14.5, 5, 7.5, rr(S, 1.5))))
    out += [line(seg(12, 13.5, 12, 14.5))] if False else []
    out += [line(poly([(5, 14.5), (5, 13), (9, 12.5)], r=S.r * 0.5)), line(poly([(19, 14.5), (19, 13), (15, 12.5)], r=S.r * 0.5)),
            line(seg(12, 12.5, 12, 14.5))]
    return out


@icon("transfer-learning", CAT, "Brain on the upper left with an arrow carrying a small block to a second brain",
      tags=["pretrained model", "fine tuning", "reuse knowledge", "model reuse", "domain adaptation", "knowledge transfer"])
def _(S):
    return [shell(brain_d(7.2, 7, 11)), shell(brain_d(16.8, 17, 11)),
            line(poly([(13.5, 4.5), (19.5, 4.5), (19.5, 9.5)], r=S.r)), head(S, 19.5, 10.2, 90),
            Part("solid", rect(3.5, 17, 4, 4, 0.5)) if False else Part("solid", rect(2.5, 17.5, 4, 4, 0.6))]


@icon("ai-guardrails", CAT, "Road lane lined by guard rails with a sparkle in the lane",
      tags=["ai safety", "safety rails", "content filter", "responsible ai", "boundaries", "alignment"])
def _(S):
    out = [line(seg(4, 21.5, 7, 2.5)), line(seg(20, 21.5, 17, 2.5))]
    for y in (6.5, 13, 19.5):
        xl = 7 - (y - 2.5) * 3 / 19
        out += [line(seg(xl - 3, y, xl, y)), line(seg(24 - xl, y, 27 - xl, y))]
    out.append(solid(poly([(12, 7), (13.2, 10.8), (17, 12), (13.2, 13.2), (12, 17), (10.8, 13.2), (7, 12), (10.8, 10.8)], closed=True)))
    return out


@icon("diffusion-model", CAT, "Square of scattered noise dots turning into a clean image frame with an arrow",
      tags=["image generation", "denoising", "generative ai", "noise to image", "stable diffusion", "text to image"])
def _(S):
    out = [shell(rect(2.5, 2.5, 8.5, 8.5, rr(S, 1.5)))]
    out += [dot(5, 5, 0.9), dot(8.5, 4.8, 0.9), dot(6.2, 8.5, 0.9), dot(9, 8.2, 0.7)]
    out += [shell(rect(13.5, 13.5, 8, 8, rr(S, 1.5))), detail(poly([(15.5, 19.5), (17.5, 17), (19.5, 19.5)], r=S.r * 0.3)),
            line(poly([(11.5, 6.8), (17.5, 6.8), (17.5, 11.5)], r=S.r)), head(S, 17.5, 12, 90)]
    return out


@icon("autoencoder", CAT, "Network of dots shaped like a bow tie, wide at both ends and narrow in the middle",
      tags=["encoder decoder", "latent space", "bottleneck", "neural network", "compression", "unsupervised"])
def _(S):
    out = []
    left = [(3.5, 5), (3.5, 12), (3.5, 19)]
    mid = [(12, 9.5), (12, 14.5)]
    right = [(20.5, 5), (20.5, 12), (20.5, 19)]
    for x, y in left:
        for mx, my in mid:
            if abs(y - my) < 8:
                out += [line(seg(x, y, mx, my)), line(seg(24 - x, y, 24 - mx, my))]
    for p in left + mid + right:
        out.append(dot(p[0], p[1], 2) if S.name == "rounded" else solid(rect(p[0] - 1.8, p[1] - 1.8, 3.6, 3.6)))
    return out


@icon("generative-adversarial-network", CAT, "Two robot heads facing each other above a pair of opposing arrows",
      tags=["gan", "generator discriminator", "adversarial", "two networks", "deep fake", "generative ai"])
def _(S):
    out = [shell(rect(2, 2.5, 9, 9, rr(S, 2))), shell(rect(13, 2.5, 9, 9, rr(S, 2))),
           dot(5, 6.5, 0.95), dot(8, 6.5, 0.95), dot(16, 6.5, 0.95), dot(19, 6.5, 0.95),
           line(seg(3, 16, 21, 16)), head(S, 21, 16, 0), line(seg(21, 20.5, 3, 20.5)), head(S, 3, 20.5, 180)]
    return out


@icon("recurrent-neural-network", CAT, "Single circle node with a looping arrow leaving its top and coming back in, plus input and output lines",
      tags=["rnn", "sequence model", "feedback loop", "lstm", "time series", "neural network"])
def _(S):
    return [shell(circle(12, 15, 4.5)), line(seg(2, 15, 7.5, 15)), line(seg(16.5, 15, 22, 15)),
            line("M8.6 9.4C2.5 1 21.5 1 15.4 8.8"), head(S, 15.5, 9.6, 120, 3.4)]


@icon("semantic-query", CAT, "Magnifying glass with a small brain inside its lens",
      tags=["semantic search", "meaning search", "vector search", "natural language search", "intent", "embedding search"])
def _(S):
    return [shell(circle(10, 10, 7.6)), line(seg(15.7, 15.7, 21, 21)), Part("dot", brain_solid(10, 9.8, 8.5, 0.8))]


@icon("robotic-process-automation", CAT, "Robot arm reaching to press a cursor arrow inside a window",
      tags=["rpa", "bot automation", "workflow automation", "software robot", "click automation", "back office"])
def _(S):
    cur = [(5.5, 5.5), (5.5, 12), (7.4, 10.4), (8.8, 13.3), (10.4, 12.6), (9, 9.8), (11.4, 9.7)]
    return [shell(rect(2, 3, 14, 12, rr(S, 2))), Part("dot", poly(cur, closed=True)),
            solid(rect(17, 20, 5, 2)), line(poly([(19.5, 20), (19.5, 15.5), (13.5, 12.5)], r=S.r)), dot(19.5, 15.5, 1.6)]


@icon("low-code-builder", CAT, "Three staggered puzzle blocks snapped together, the top one showing code brackets",
      tags=["no code", "visual programming", "drag and drop builder", "app builder", "citizen developer", "blocks"])
def _(S):
    return [shell(rect(2, 2, 17, 8.5, rr(S, 2.5))), detail(poly([(8, 4.8), (5.8, 6.25), (8, 7.7)], r=0)),
            detail(poly([(13, 4.8), (15.2, 6.25), (13, 7.7)], r=0)),
            shell(rect(7, 13, 15, 3.5, rr(S, 1.5))), shell(rect(2, 19, 15, 3, rr(S, 1.2))),
            solid(circle(12, 11.75, 1.4)), solid(circle(9, 17.75, 1.4))]


@icon("multi-core-processor", CAT, "Processor chip with its centre divided into four square cores and pins on every side",
      tags=["multicore", "cpu cores", "quad core", "parallel processing", "chip", "threads"])
def _(S):
    out = [shell(rect(5.5, 5.5, 13, 13, rr(S, 3))), detail(seg(12, 5.5, 12, 18.5)), detail(seg(5.5, 12, 18.5, 12))]
    for v in (9, 15):
        out += [line(seg(v, 2, v, 5.5)), line(seg(v, 18.5, v, 22)), line(seg(2, v, 5.5, v)), line(seg(18.5, v, 22, v))]
    return out


@icon("geo-replication", CAT, "Globe above two database cylinders joined by a small arc",
      tags=["multi region", "regional copies", "data replication", "disaster recovery", "global database", "cloud regions"])
def _(S):
    ry = L(S, 1.1, 1.8)
    c1, l1 = cyl(S, 2.5, 14.5, 7.5, 7.5, ry)
    c2, l2 = cyl(S, 14, 14.5, 7.5, 7.5, ry)
    return [shell(circle(12, 7, 4.6)), detail(ellipse(12, 7, 1.8, 4.6)), detail(seg(7.4, 7, 16.6, 7)),
            shell(c1), detail(l1), shell(c2), detail(l2), line("M10.8 19C11.5 20.2 12.5 20.2 13.2 19")]


@icon("api-versioning", CAT, "Rounded box holding angle brackets with a small version tag hanging from its corner",
      tags=["api version", "v1 v2", "release tag", "semver", "endpoint version", "backward compatibility"])
def _(S):
    tag = [(0, -4.2), (3.6, -1.6), (3.6, 4), (-3.6, 4), (-3.6, -1.6)]
    a = math.radians(18)
    pts = [(17.8 + x * math.cos(a) - y * math.sin(a), 18 + x * math.sin(a) + y * math.cos(a)) for x, y in tag]
    hx, hy = 0, -0.9
    return [shell(rect(2, 2.5, 16, 11, rr(S, 3))), detail(poly([(8.5, 6.2), (6, 8) , (8.5, 9.8)], r=0)),
            detail(poly([(11.5, 6.2), (14, 8), (11.5, 9.8)], r=0)),
            shell(poly(pts, closed=True, r=S.r * 0.6)),
            dot(17.8 + hx * math.cos(a) - hy * math.sin(a), 18 + hx * math.sin(a) + hy * math.cos(a), 0.9)]


@icon("breaking-change", CAT, "Angle bracket broken in two with a jagged crack where its tip should be",
      tags=["incompatible change", "major version", "api break", "deprecation", "regression", "semver major"])
def _(S):
    return [line(poly([(17, 3), (9.5, 8.8)], r=0)), line(poly([(9.5, 15.2), (17, 21)], r=0)),
            line(poly([(7.6, 7.6), (4.6, 10.4), (7.4, 12), (4.6, 13.8), (7.6, 16.4)], r=S.r * 0.3))]
