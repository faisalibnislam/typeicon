"""TypeIcon Core: tech, batch 001 (version control, CI/CD, files, architecture patterns)."""
import math
import re

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar
from pathops import Path  # noqa: F401

CAT = "tech"


def node(x, y, r=2.5):
    return shell(circle(x, y, r))


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def tx(d, s=1.0, dx=0.0, dy=0.0):
    """Scale and translate an absolute path made of M L H V A Z commands."""
    toks = re.findall(r"[MLHVAZ]|-?\d*\.?\d+", d)
    out, i = [], 0
    while i < len(toks):
        c = toks[i]
        i += 1
        if c in "ML":
            out.append(f"{c}{fmt(float(toks[i]) * s + dx)} {fmt(float(toks[i + 1]) * s + dy)}")
            i += 2
        elif c == "H":
            out.append(f"H{fmt(float(toks[i]) * s + dx)}")
            i += 1
        elif c == "V":
            out.append(f"V{fmt(float(toks[i]) * s + dy)}")
            i += 1
        elif c == "A":
            rx, ry, rot, la, sw, x, y = toks[i:i + 7]
            out.append(f"A{fmt(float(rx) * s)} {fmt(float(ry) * s)} {rot} {la} {sw} {fmt(float(x) * s + dx)} {fmt(float(y) * s + dy)}")
            i += 7
        else:
            out.append("Z")
    return "".join(out)


_CLOUD_LINE = "M4.5 19H19.5A3.8 3.8 0 0 0 18 11.7A6 6 0 0 0 6.5 10A4.7 4.7 0 0 0 4.5 19Z"
_CLOUD_ROUND = "M7 19H17.5A4.5 4.5 0 0 0 18 10.03A6 6 0 0 0 6.34 9.1A5 5 0 0 0 7 19Z"


def cloud(S, s, x0, base):
    """The library cloud scaled by s, left edge (Line) at x0, flat base at y = base."""
    d = _CLOUD_LINE if S.name == "line" else _CLOUD_ROUND
    return tx(d, s, x0 - 1.69 * s, base - 19 * s)


_MOON = "M20.5 14.5A8.5 8.5 0 1 1 9.5 3.5A7 7 0 0 0 20.5 14.5Z"


def moon(s, x0, y0):
    return tx(_MOON, s, x0 - 4.08 * s, y0 - 3.5 * s)


def xf(pts, deg, ox, oy):
    """Rotate local points clockwise about the local origin, then translate to (ox, oy)."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(ox + x * c - y * s, oy + x * s + y * c) for x, y in pts]


def hammer(S, deg, ox, oy, reach=7.0):
    """Small claw-less hammer: head centred on local (0,-3), handle running down local +y."""
    head = xf([(-4, -5), (4, -5), (4, -1), (-4, -1)], deg, ox, oy)
    h = xf([(0, -1), (0, reach)], deg, ox, oy)
    return [shell(poly(head, closed=True, r=S.r * 0.6)), line(seg(h[0][0], h[0][1], h[1][0], h[1][1]))]


def page(S, x0=4.5, x1=19.5, y0=2.5, y1=21.5, fold=5.5):
    """Document page with a folded top-right corner."""
    pts = [(x0, y0), (x1 - fold, y0), (x1, y0 + fold), (x1, y1), (x0, y1)]
    return [shell(poly(pts, closed=True, r=S.r)),
            detail(poly([(x1 - fold, y0), (x1 - fold, y0 + fold), (x1, y0 + fold)], r=S.r * 0.5))]


def bend(S, pts, soft=3.0):
    return poly(pts, r=0 if S.name == "line" else soft)


def check(S, x, y, k=1.0):
    return poly([(x - 2.5 * k, y), (x - 0.7 * k, y + 1.8 * k), (x + 2.5 * k, y - 2 * k)], r=S.r * 0.5)


# ============================================================================ version control

@icon("git-stash", CAT, "Three shallow drawer trays with a commit dot tucked into the top one",
      tags=["git stash", "shelve", "save changes", "version control", "temporary", "drawer"])
def _(S):
    return [shell(rect(3, 3, 18, 6.5, min(S.R, 2.5))),
            dot(12, 6.25, 1.5),
            line(poly([(3, 12.5), (3, 15.5), (21, 15.5), (21, 12.5)], r=S.r * 0.6)),
            line(poly([(3, 18.5), (3, 21), (21, 21), (21, 18.5)], r=S.r * 0.6))]


@icon("git-cherry-pick", CAT, "Commit line of three dots with one commit picked off as a cherry on a stem",
      tags=["cherry pick", "git", "version control", "commit", "select commit", "fruit"])
def _(S):
    return [node(5.5, 4.5, 2), node(5.5, 12, 2), node(5.5, 19.5, 2),
            line(seg(5.5, 6.9, 5.5, 9.6)), line(seg(5.5, 14.4, 5.5, 17.1)),
            node(16.5, 16.5, 3.5),
            line(poly([(16.5, 13), (16.5, 8.5), (12.5, 4.5)], r=S.r * 1.2)),
            line(seg(12.5, 4.5, 10, 4.5))]


@icon("git-blame", CAT, "Code lines each with a small author dot on the left margin",
      tags=["git blame", "annotate", "author", "who changed", "version control", "history", "praise"])
def _(S):
    return [dot(5, 5.5, 1.9), line(seg(10, 5.5, 21, 5.5)),
            dot(5, 12, 1.9), line(seg(10, 12, 17, 12)),
            dot(5, 18.5, 1.9), line(seg(10, 18.5, 19.5, 18.5))]


@icon("git-bisect", CAT, "Commit line cut at its midpoint by a bar, with a magnifier over the lower half",
      tags=["git bisect", "binary search", "find bug", "regression", "version control", "split"])
def _(S):
    return [node(6, 4.5, 2), node(6, 19.5, 2),
            line(seg(6, 6.9, 6, 17.1)),
            line(seg(2.5, 12, 9.5, 12)),
            shell(circle(16, 14, 4.25)),
            line(seg(19.2, 17.2, 21.5, 19.5))]


@icon("git-submodule", CAT, "Repository box holding a smaller nested repository box with a commit dot",
      tags=["git submodule", "nested repo", "dependency", "repository", "version control", "subproject"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, S.R)),
            detail(rect(7, 8, 10, 10, min(S.R, 2))),
            dot(12, 13, 1.5)]


@icon("git-worktree", CAT, "One commit dot branching into two separate folders below it",
      tags=["git worktree", "working tree", "folders", "checkout", "branches", "version control"])
def _(S):
    return [node(12, 4.5, 2.25),
            line(seg(12, 6.75, 12, 10.5)),
            line(bend(S, [(6.25, 14), (6.25, 10.5), (17.75, 10.5), (17.75, 14)], 2.5)),
            shell(poly([(2.5, 13), (5.5, 13), (7, 14.5), (10, 14.5), (10, 21), (2.5, 21)], closed=True, r=S.r * 0.6)),
            shell(poly([(21.5, 13), (18.5, 13), (17, 14.5), (14, 14.5), (14, 21), (21.5, 21)], closed=True, r=S.r * 0.6))]


@icon("git-tag-annotated", CAT, "Commit dot on a line with a tag hanging from it holding two text lines",
      tags=["git tag", "annotated tag", "release tag", "version", "label", "version control"])
def _(S):
    return [node(12, 4.5, 2),
            line(seg(2.5, 4.5, 9.5, 4.5)), line(seg(14.5, 4.5, 21.5, 4.5)),
            line(seg(12, 6.5, 12, 9)),
            shell(poly([(9, 9), (15, 9), (18, 12), (18, 21.5), (6, 21.5), (6, 12)], closed=True, r=S.r)),
            detail(seg(9.5, 14.5, 14.5, 14.5)), detail(seg(9.5, 18, 14.5, 18))]


@icon("git-pull", CAT, "Cloud at the top with an arrow coming down onto a commit dot",
      tags=["git pull", "fetch", "download changes", "sync", "remote", "version control"])
def _(S):
    return [shell(cloud(S, 0.52, 6.8, 10)),
            line(seg(12, 12.5, 12, 15.5)),
            line(poly([(9.5, 13.5), (12, 16), (14.5, 13.5)], r=S.r * 0.5)),
            dot(12, 20, 2),
            line(seg(3, 20, 8.5, 20)), line(seg(15.5, 20, 21, 20))]


@icon("git-hook", CAT, "Commit dot on a line with a fishing hook hanging from it",
      tags=["git hook", "pre-commit", "trigger", "automation", "script", "version control", "fishing"])
def _(S):
    return [node(15, 4.5, 2.25),
            line(seg(3, 4.5, 12.75, 4.5)), line(seg(17.25, 4.5, 21.5, 4.5)),
            line(f"M15 6.75V15.5A4.75 4.75 0 0 1 5.5 15.5V13"),
            line(poly([(3, 15), (5.5, 12.5), (8, 15)], r=S.r * 0.5))]


@icon("git-ignore-file", CAT, "Document page with a slashed circle in its lower corner and short text lines",
      tags=["gitignore", "ignore file", "exclude", "untracked", "version control", "not tracked"])
def _(S):
    return [line(poly([(9, 21.5), (3.5, 21.5), (3.5, 2.5), (10.5, 2.5), (15.5, 7.5), (15.5, 9)], r=S.r)),
            detail(poly([(10.5, 2.5), (10.5, 7.5), (15.5, 7.5)], r=S.r * 0.5)),
            line(seg(7, 12, 11, 12)), line(seg(7, 16.5, 9, 16.5)),
            shell(circle(17, 17, 4)),
            detail(seg(14.2, 19.8, 19.8, 14.2))]


@icon("git-log", CAT, "Vertical line of commit dots, each with a short text line to its right",
      tags=["git log", "history", "commits", "timeline", "version control", "changelog"])
def _(S):
    return [line(seg(5.5, 5, 5.5, 19)),
            dot(5.5, 5, 2.25), dot(5.5, 12, 2.25), dot(5.5, 19, 2.25),
            line(seg(10.5, 5, 21, 5)), line(seg(10.5, 12, 17.5, 12)), line(seg(10.5, 19, 19.5, 19))]


@icon("git-diff-split", CAT, "Two side by side panes with minus signs on the left and plus signs on the right",
      tags=["split diff", "side by side", "compare", "changes", "code review", "version control"])
def _(S):
    return [shell(rect(2.5, 3.5, 8.5, 17, min(S.R, 2.5))), shell(rect(13, 3.5, 8.5, 17, min(S.R, 2.5))),
            detail(seg(4.75, 9, 8.75, 9)), detail(seg(4.75, 15, 8.75, 15)),
            detail(seg(15.25, 9, 19.25, 9)), detail(seg(17.25, 7, 17.25, 11)),
            detail(seg(15.25, 15, 19.25, 15)), detail(seg(17.25, 13, 17.25, 17))]


@icon("pull-request-approved", CAT, "Two commit dots joined by a branch line that ends in a circle holding a check",
      tags=["approved pull request", "code review", "merge approved", "lgtm", "accepted", "version control"])
def _(S):
    return [node(5.5, 5.5, 2.25), node(5.5, 18.5, 2.25),
            line(seg(5.5, 7.75, 5.5, 16.25)),
            line(bend(S, [(8, 18.5), (16.5, 18.5), (16.5, 12.5)], 3)),
            shell(circle(16.5, 7.5, 5)),
            detail(check(S, 16.5, 7.5, 0.95))]


@icon("patch-file", CAT, "Document page with a stitched square patch sewn onto its center",
      tags=["patch", "diff file", "fix", "hotfix", "apply patch", "stitched", "file"])
def _(S):
    return [*page(S, 3.5, 20.5, 2.5, 21.5, 5.5),
            detail(rect(8, 10.5, 8, 8, min(S.R, 1.5))),
            detail(seg(10.5, 13, 13.5, 16))]


@icon("monorepo", CAT, "One large repository box holding a two by two grid of small package blocks",
      tags=["monorepo", "single repository", "workspace", "packages", "mono repo", "multi package"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, S.R)),
            sq(5.5, 5.5, 5.5, 5.5, 1), sq(13, 5.5, 5.5, 5.5, 1),
            sq(5.5, 13, 5.5, 5.5, 1), sq(13, 13, 5.5, 5.5, 1)]


def gear(S, cx, cy, ro, ri, n=8):
    step = 360 / n
    pts = []
    for i in range(n):
        c = -90 + i * step
        pts += [polar(cx, cy, ri, c - 0.30 * step), polar(cx, cy, ro, c - 0.17 * step),
                polar(cx, cy, ro, c + 0.17 * step), polar(cx, cy, ri, c + 0.30 * step)]
    return poly(pts, closed=True, r=S.r * 0.4)


# ============================================================================ build, test and release

@icon("build-status", CAT, "Hammer beside a round status light holding a check mark",
      tags=["build status", "build passing", "ci status", "build passed", "badge", "continuous integration"])
def _(S):
    return [*hammer(S, -45, 8.6, 8.6, 3.5),
            shell(circle(16.5, 16.5, 4.5)),
            detail(check(S, 16.5, 16.5, 0.8))]


@icon("nightly-build", CAT, "Crescent moon above a gear, an automated overnight build",
      tags=["nightly build", "night build", "scheduled build", "overnight", "daily build", "ci", "moon", "automation"])
def _(S):
    return [shell(moon(0.62, 2.5, 2.5)),
            shell(gear(S, 16, 16, 5.6, 4.2)),
            detail(circle(16, 16, 1.3))]


@icon("test-coverage", CAT, "Page of code lines with a progress ring three quarters filled in the lower corner",
      tags=["test coverage", "coverage", "code coverage", "tested lines", "percentage", "unit tests", "progress"])
def _(S):
    return [line(poly([(9, 21.5), (3.5, 21.5), (3.5, 2.5), (10.5, 2.5), (15.5, 7.5), (15.5, 9)], r=S.r)),
            detail(poly([(10.5, 2.5), (10.5, 7.5), (15.5, 7.5)], r=S.r * 0.5)),
            line(seg(7, 11, 11, 11)), line(seg(7, 15.5, 9.5, 15.5)),
            line(arc(17, 17, 4.5, -90, 180))]


@icon("end-to-end-test", CAT, "Two small circles at the ends of a long line with a checked circle in the middle",
      tags=["e2e test", "end to end", "integration test", "full flow test", "qa", "test passed", "automation"])
def _(S):
    return [node(4, 12, 2),
            line(seg(6, 12, 8, 12)), line(seg(16, 12, 18, 12)),
            shell(circle(12, 12, 4)),
            detail(check(S, 12, 12, 0.75)),
            node(20, 12, 2)]


@icon("smoke-test", CAT, "Laptop with a check mark on its screen and a wisp of smoke rising above it",
      tags=["smoke test", "sanity check", "quick test", "basic test", "build verification", "qa", "laptop"])
def _(S):
    return [shell(rect(4.5, 9, 15, 9, min(S.R, 2))),
            detail(check(S, 12, 13.5, 0.85)),
            line(seg(2.5, 21, 21.5, 21)),
            line("M9 6.5C7.5 5.2 10.5 4 9 2.5"), line("M15 6.5C13.5 5.2 16.5 4 15 2.5")]


@icon("load-test", CAT, "Server box pressed down by a heavy weight block with a carry handle",
      tags=["load test", "stress test", "performance test", "capacity", "benchmark", "weight", "traffic"])
def _(S):
    return [line(poly([(9.5, 5.5), (9.5, 3), (14.5, 3), (14.5, 5.5)], r=S.r * 0.6)),
            shell(poly([(8, 5.5), (16, 5.5), (20.5, 11.5), (3.5, 11.5)], closed=True, r=S.r)),
            shell(rect(3.5, 15, 17, 6.5, min(S.R, 2.5))),
            dot(7.5, 18.25, 1.1), detail(seg(11, 18.25, 16.5, 18.25))]


@icon("test-case", CAT, "Clipboard with a clip, holding one checkbox and a line of text",
      tags=["test case", "test plan", "checklist", "qa", "scenario", "test steps", "clipboard"])
def _(S):
    return [shell(rect(3.5, 4.5, 17, 17, S.R)),
            shell(rect(8.5, 2.5, 7, 4, 1)),
            detail(rect(7, 11, 5, 5, 1)),
            detail(seg(14.5, 13.5, 17, 13.5)),
            detail(seg(7.5, 19, 16.5, 19))]


@icon("canary-deployment", CAT, "Small songbird perched on top of a server box",
      tags=["canary release", "canary deploy", "gradual rollout", "test release", "bird", "progressive delivery"])
def _(S):
    return [shell(poly([(2.5, 11), (8.5, 6.5), (12, 4), (16, 4), (17.5, 6), (20.5, 7.5), (17.5, 8.5), (17, 11), (13, 13), (7, 12.5)],
                       closed=True, r=S.r * 1.2)),
            dot(15, 6.8, 0.9),
            line(seg(10.5, 13, 10.5, 15.5)), line(seg(13.5, 13, 13.5, 15.5)),
            shell(rect(3, 15.5, 18, 6, min(S.R, 2.5))),
            dot(7, 18.5, 1.1), dot(10.75, 18.5, 1.1)]


@icon("blue-green-deployment", CAT, "Two identical server boxes side by side with a toggle switch below them",
      tags=["blue green", "blue-green deploy", "zero downtime", "switchover", "release strategy", "toggle", "servers"])
def _(S):
    def box(x):
        return [shell(rect(x, 2.5, 7.5, 10.5, min(S.R, 2.5))), detail(seg(x, 7.75, x + 7.5, 7.75)),
                dot(x + 3.75, 5.1, 1.1), dot(x + 3.75, 10.4, 1.1)]
    return [*box(3), *box(13.5),
            shell(rect(5.5, 17, 13, 5, min(S.R, 2.5))),
            dot(15.25, 19.5, 1.4)]


@icon("rolling-update", CAT, "Row of three server boxes with a curved arrow sweeping across their tops",
      tags=["rolling update", "rolling deploy", "gradual update", "staged rollout", "zero downtime", "refresh", "servers"])
def _(S):
    return [shell(rect(3, 15, 4, 6.5, min(S.R, 1.5))), shell(rect(10, 15, 4, 6.5, min(S.R, 1.5))),
            shell(rect(17, 15, 4, 6.5, min(S.R, 1.5))),
            line(arc(12, 11.5, 8, 180, 360)),
            line(poly([(17.8, 9.3), (20, 11.5), (22.2, 9.3)], r=S.r * 0.5))]


@icon("feature-flag", CAT, "Pennant flag on a pole with a toggle switch at the base",
      tags=["feature flag", "feature toggle", "flag", "release toggle", "experiment", "switch", "rollout"])
def _(S):
    return [line(seg(6.5, 3.5, 6.5, 15)),
            shell(poly([(6.5, 3.5), (19.5, 7), (6.5, 10.5)], closed=True, r=S.r * 0.8)),
            shell(rect(3, 16, 18, 5.5, min(S.R, 2.75))),
            dot(16.5, 18.75, 1.5)]


@icon("artifact-registry", CAT, "Shelf holding three sealed boxes, each with a small label",
      tags=["artifact registry", "package registry", "container registry", "binary repository", "storage", "shelf", "builds"])
def _(S):
    bx = [3, 10, 17]
    return [*[shell(rect(x, 7.5, 4, 10, min(S.R, 1.5))) for x in bx],
            *[dot(x + 2, 12.5, 0.8) for x in bx],
            line(seg(2.5, 21, 21.5, 21))]


@icon("cron-job", CAT, "Clock face with a small gear overlapping its lower right",
      tags=["cron", "cron job", "scheduled task", "crontab", "timer", "recurring job", "scheduler"])
def _(S):
    return [line(arc(10.5, 10.5, 7.5, 105, 345)),
            line(poly([(10.5, 6.5), (10.5, 10.5), (13.5, 12.5)], r=S.r * 0.5)),
            shell(gear(S, 17, 17, 4.6, 3.4)),
            detail(circle(17, 17, 1))]


@icon("job-scheduler", CAT, "Calendar page with a gear in its center and a clock hand on the gear",
      tags=["job scheduler", "scheduler", "scheduled jobs", "calendar", "automation", "planned task", "timetable"])
def _(S):
    return [shell(rect(3, 5, 18, 16.5, S.R)),
            line(seg(8, 2.5, 8, 6.5)), line(seg(16, 2.5, 16, 6.5)),
            detail(gear(S, 12, 13.5, 5.2, 3.9)),
            detail(poly([(12, 11), (12, 13.5), (14.2, 13.5)], r=S.r * 0.4))]


def behind(body: Path, cutter_d: str, gap=1.5, hole=None) -> Part:
    """A solid region seen behind a window: body minus the window grown by gap, minus an optional hole."""
    cut = U(P(cutter_d), ST(cutter_d, 2 + 2 * gap, "round", "round"))
    out = D(body, cut)
    if hole:
        out = D(out, P(hole))
    return solid(path_to_d(out))


# ============================================================================ automation and processes

@icon("background-job", CAT, "Solid gear half hidden behind a window outline",
      tags=["background job", "background task", "worker", "async job", "queue job", "running quietly", "hidden process"])
def _(S):
    win = rect(10, 10, 11.5, 11.5, min(S.R, 3))
    return [behind(P(gear(S, 9, 9, 7, 5.4)), win, 1.5, circle(9, 9, 2.2)),
            shell(win),
            detail(seg(10, 14.5, 21.5, 14.5))]


@icon("worker-process", CAT, "Gear with a small hard hat sitting on top of it",
      tags=["worker", "worker process", "job runner", "builder", "hard hat", "background worker", "thread"])
def _(S):
    return [shell("M7 8A5 5 0 0 1 17 8Z"),
            line(seg(4.5, 8, 19.5, 8)),
            shell(gear(S, 12, 16, 5, 3.7)),
            detail(circle(12, 16, 1.2))]


@icon("daemon-process", CAT, "Gear with two small horns and a spade tail, a friendly background process",
      tags=["daemon", "background service", "service process", "demon", "system service", "unix", "horns"])
def _(S):
    return [shell(gear(S, 12, 14, 5.2, 3.9)),
            detail(circle(12, 14, 1.2)),
            line("M8.8 9.6C6.5 8.8 5.5 6.8 6 3.8"), line("M15.2 9.6C17.5 8.8 18.5 6.8 18 3.8"),
            line("M16.5 18C19 18.8 20 20 20 21"),
            line(poly([(18.2, 20.2), (20, 22), (21.8, 20.2)], r=S.r * 0.4))]


@icon("merge-queue", CAT, "Three lines lined up in single file converging into one arrow",
      tags=["merge queue", "merge train", "commit queue", "serial merge", "converge", "single file", "ci queue"])
def _(S):
    return [line(bend(S, [(3, 5), (7, 5), (12, 12)], 4)),
            line(seg(3, 12, 20, 12)),
            line(bend(S, [(3, 19), (7, 19), (12, 12)], 4)),
            line(poly([(17, 9), (20.5, 12), (17, 15)], r=S.r * 0.5))]


@icon("deployment-pipeline", CAT, "Conveyor belt carrying a box toward a cloud at its far end",
      tags=["deployment pipeline", "delivery pipeline", "ci/cd", "release pipeline", "conveyor", "ship to cloud", "devops"])
def _(S):
    return [shell(cloud(S, 0.5, 12.5, 10)),
            shell(rect(5, 9, 5, 4.5, 1)),
            shell(rect(2.5, 15.5, 15, 5, min(S.R, 2.5))),
            dot(6.5, 18, 1), dot(13.5, 18, 1)]


@icon("devops-loop", CAT, "Infinity loop with a small gear in its left loop and a rocket in its right loop",
      tags=["devops", "infinity loop", "continuous delivery", "ci cd cycle", "lifecycle", "development operations", "rocket"])
def _(S):
    rk = xf([(0, -3.6), (1.3, -1.2), (1.3, 1.4), (2.6, 3), (0, 2.2), (-2.6, 3), (-1.3, 1.4), (-1.3, -1.2)], 45, 17.5, 12)
    return [line("M12 12C10.5 9.5 9 7.5 6.5 7.5A4.5 4.5 0 0 0 6.5 16.5C9 16.5 10.5 14.5 12 12"
                 "C13.5 9.5 15 7.5 17.5 7.5A4.5 4.5 0 0 1 17.5 16.5C15 16.5 13.5 14.5 12 12Z"),
            solid(gear(S, 6.5, 12, 2.9, 2.1, 6)),
            solid(poly(rk, closed=True, r=0))]


@icon("build-cache", CAT, "Box with a lightning bolt beside a stack of three layered disks",
      tags=["build cache", "cache layer", "incremental build", "stored build", "faster builds", "artifact cache", "bolt"])
def _(S):
    bolt = [(8, 8.2), (5.2, 12.3), (7.6, 12.3), (6.4, 15.8), (9.2, 11.4), (6.8, 11.4)]
    return [shell(rect(2.5, 6, 9.5, 12, min(S.R, 2.5))),
            Part("dot", poly(bolt, closed=True)),
            shell(ellipse(18, 7.5, 4, 2)),
            line(seg(14, 7.5, 14, 16)), line(seg(22, 7.5, 22, 16)),
            line("M14 11.75A4 2 0 0 0 22 11.75"), line("M14 16A4 2 0 0 0 22 16")]


@icon("code-coverage-report", CAT, "Report page with a vertical axis and three horizontal bars of different lengths",
      tags=["coverage report", "test report", "code coverage", "percent covered", "progress bars", "qa report", "metrics"])
def _(S):
    return [*page(S),
            detail(seg(7.5, 9.5, 7.5, 19.5)),
            detail(seg(10.5, 11, 16.5, 11)), detail(seg(10.5, 15, 14.5, 15)), detail(seg(10.5, 19, 12.5, 19))]


@icon("staging-environment", CAT, "Theatre stage with tied-back curtains and a server box standing on the stage",
      tags=["staging", "staging environment", "pre-production", "preview environment", "stage", "theatre", "rehearsal"])
def _(S):
    return [shell(poly([(2.5, 3.5), (7.5, 3.5), (2.5, 12.5)], closed=True, r=S.r * 0.6)),
            shell(poly([(21.5, 3.5), (16.5, 3.5), (21.5, 12.5)], closed=True, r=S.r * 0.6)),
            shell(rect(8.75, 7.5, 6.5, 7.5, min(S.R, 1.5))), dot(12, 10.5, 0.9),
            shell(rect(2.5, 17.5, 19, 4, min(S.R, 1.5)))]


@icon("dev-environment", CAT, "Laptop with code brackets on its screen and a small wrench beside it",
      tags=["dev environment", "development environment", "local setup", "workstation", "coding setup", "ide", "developer tools"])
def _(S):
    wr = xf([(-1.2, 6.5), (-1.2, 0), (-2.8, -1.5), (-2.8, -5.5), (-1.2, -5.5), (-1.2, -3.2), (1.2, -3.2),
             (1.2, -5.5), (2.8, -5.5), (2.8, -1.5), (1.2, 0), (1.2, 6.5)], 45, 17, 16.5)
    return [shell(rect(2.5, 3.5, 11, 9.5, min(S.R, 2))),
            detail(poly([(6.75, 6.2), (5, 8.25), (6.75, 10.3)], r=S.r * 0.4)),
            detail(poly([(9.25, 6.2), (11, 8.25), (9.25, 10.3)], r=S.r * 0.4)),
            line(seg(1.5, 16, 14.5, 16)),
            shell(poly(wr, closed=True, r=S.r * 0.4))]


@icon("yaml-file", CAT, "Document page with dash-prefixed lines stepping in by indentation",
      tags=["yaml", "yml", "config file", "configuration", "indentation", "manifest", "settings file"])
def _(S):
    return [*page(S),
            line(seg(7.5, 10.5, 12, 10.5)),
            dot(9, 14.5, 0.9), line(seg(11.5, 14.5, 16, 14.5)),
            dot(9, 18.5, 0.9), line(seg(11.5, 18.5, 16, 18.5))]


@icon("env-file", CAT, "Document page with key and value lines and a small padlock in the corner",
      tags=["env file", "dotenv", "environment variables", "secrets file", "config", ".env", "private settings"])
def _(S):
    return [line(poly([(10, 21.5), (3.5, 21.5), (3.5, 2.5), (10.5, 2.5), (15.5, 7.5), (15.5, 9)], r=S.r)),
            detail(poly([(10.5, 2.5), (10.5, 7.5), (15.5, 7.5)], r=S.r * 0.5)),
            line(seg(7, 11, 11, 11)), line(seg(7, 15.5, 9.5, 15.5)),
            shell(rect(13.5, 16, 8, 6, 1.2)),
            line("M15.5 16V14A2 2 0 0 1 19.5 14V16"),
            dot(17.5, 19, 0.9)]


@icon("container-file", CAT, "Document page with a shipping container outline drawn on it",
      tags=["container file", "container image definition", "build file", "image recipe", "containerfile", "shipping container"])
def _(S):
    return [*page(S, 3.5, 20.5),
            detail(rect(7.5, 10.5, 9, 8, min(S.R, 1.5))),
            detail(seg(12, 10.5, 12, 18.5))]


@icon("script-file", CAT, "Scroll with a curled bottom edge and code brackets in its middle",
      tags=["script", "script file", "scripting", "automation script", "scroll", "code", "macro"])
def _(S):
    return [shell("M8.5 3.5H19.5V17.5A3.5 3.5 0 0 1 16 21H5.5A3.5 3.5 0 0 0 8.5 17.5Z"),
            detail(poly([(13, 8), (11.2, 10.5), (13, 13)], r=S.r * 0.4)),
            detail(poly([(16, 8), (17.8, 10.5), (16, 13)], r=S.r * 0.4))]


@icon("shell-script", CAT, "Document page with a chevron prompt and an underscore cursor",
      tags=["shell script", "bash script", "sh file", "command file", "terminal script", "prompt", "cli"])
def _(S):
    return [*page(S),
            detail(poly([(8, 11), (11, 14), (8, 17)], r=S.r * 0.5)),
            detail(seg(12.5, 17.5, 16.5, 17.5))]


def chev(S, x, y, w, h, left=True):
    """Small angle bracket centred on (x, y), pointing left (<) or right (>)."""
    tip = x - w / 2 if left else x + w / 2
    back = x + w / 2 if left else x - w / 2
    return poly([(back, y - h / 2), (tip, y), (back, y + h / 2)], r=S.r * 0.4)


def brace(S, x, y0, y1, left=True):
    d = 1 if left else -1
    ym = (y0 + y1) / 2
    return poly([(x + 1.6 * d, y0), (x, y0), (x, ym - 1.5), (x - 1.5 * d, ym), (x, ym + 1.5), (x, y1), (x + 1.6 * d, y1)], r=S.r * 0.6)


# ============================================================================ files

@icon("sql-file", CAT, "Document page with a small database cylinder on it",
      tags=["sql", "sql file", "database file", "query file", "dump", "schema file", ".sql"])
def _(S):
    return [*page(S, 3.5, 20.5),
            detail(ellipse(12, 11.5, 4, 1.7)),
            detail("M8 11.5V17.5"), detail("M16 11.5V17.5"),
            detail("M8 17.5A4 1.7 0 0 0 16 17.5")]


@icon("xml-file", CAT, "Document page with angle brackets and a slash inside",
      tags=["xml", "xml file", "markup", "tag file", "feed", "sitemap", "angle brackets"])
def _(S):
    return [*page(S, 3.5, 20.5),
            detail(chev(S, 8.5, 13.5, 2.5, 6, True)), detail(chev(S, 15.5, 13.5, 2.5, 6, False)),
            detail(seg(13.2, 10.8, 10.8, 16.2))]


@icon("html-file", CAT, "Document page with an angle bracket tag around an equals sign",
      tags=["html", "html file", "web page file", "markup file", "webpage", "tag attribute", ".html"])
def _(S):
    return [*page(S, 3.5, 20.5),
            detail(chev(S, 7.8, 13.75, 2.4, 6.5, True)), detail(chev(S, 16.2, 13.75, 2.4, 6.5, False)),
            detail(seg(10.6, 12, 13.4, 12)), detail(seg(10.6, 15.5, 13.4, 15.5))]


@icon("css-file", CAT, "Document page with a pair of curly braces holding a colon",
      tags=["css", "css file", "stylesheet", "style rules", "styles", "curly braces", ".css"])
def _(S):
    return [*page(S, 3.5, 20.5),
            detail(brace(S, 8, 10.5, 18.5, True)), detail(brace(S, 16, 10.5, 18.5, False)),
            dot(12, 12.5, 0.9), dot(12, 16.5, 0.9)]


@icon("code-file", CAT, "Document page with angle code brackets in the middle",
      tags=["code file", "source file", "source code", "program file", "script", "angle brackets", "programming"])
def _(S):
    return [*page(S, 3.5, 20.5),
            detail(chev(S, 8.5, 14, 3.2, 7, True)), detail(chev(S, 15.5, 14, 3.2, 7, False))]


@icon("binary-file", CAT, "Document page filled with two rows of ones and zeros",
      tags=["binary", "binary file", "bits", "ones and zeros", "machine code", "executable", "raw data"])
def _(S):
    return [*page(S),
            detail(seg(8, 10, 8, 13.5)), dot(12, 11.75, 1.3), detail(seg(16, 10, 16, 13.5)),
            dot(8, 17.25, 1.3), detail(seg(12, 15.5, 12, 19)), dot(16, 17.25, 1.3)]


@icon("license-file", CAT, "Document page with a small scale of justice on it",
      tags=["license", "license file", "licence", "legal", "terms", "copyright", "open source license"])
def _(S):
    return [*page(S, 3.5, 20.5),
            detail(seg(12, 9.5, 12, 18.5)), detail(seg(9.5, 18.5, 14.5, 18.5)),
            detail(seg(7.5, 11, 16.5, 11)),
            detail("M6.2 14.5A1.8 1.8 0 0 0 9.8 14.5"), detail("M14.2 14.5A1.8 1.8 0 0 0 17.8 14.5")]


@icon("lockfile", CAT, "Document page with a padlock in its center",
      tags=["lockfile", "lock file", "dependency lock", "pinned versions", "package lock", "locked dependencies", "reproducible"])
def _(S):
    return [*page(S, 3.5, 20.5, 2.5, 21.5, 4.5),
            detail(rect(8.5, 13, 7, 5.5, 1)),
            detail("M9.8 13V11.3A2.2 2.2 0 0 1 14.2 11.3V13")]


@icon("iso-image", CAT, "Optical disc overlapping the corner of a document page",
      tags=["iso", "iso image", "disc image", "cd image", "dvd image", "installer disc", "optical disc"])
def _(S):
    return [line(poly([(9, 21.5), (3.5, 21.5), (3.5, 2.5), (10.5, 2.5), (15.5, 7.5), (15.5, 9.5)], r=S.r)),
            detail(poly([(10.5, 2.5), (10.5, 7.5), (15.5, 7.5)], r=S.r * 0.5)),
            line(seg(7, 11, 10, 11)),
            shell(circle(16.5, 16.5, 5)),
            dot(16.5, 16.5, 1.3)]


@icon("disk-image", CAT, "Hard drive shape inside a frame drawn with only its corners",
      tags=["disk image", "drive image", "backup image", "virtual disk", "disk copy", "hard drive"])
def _(S):
    return [line(poly([(2.5, 7), (2.5, 2.5), (7, 2.5)], r=S.r * 0.5)), line(poly([(17, 2.5), (21.5, 2.5), (21.5, 7)], r=S.r * 0.5)),
            line(poly([(2.5, 17), (2.5, 21.5), (7, 21.5)], r=S.r * 0.5)), line(poly([(17, 21.5), (21.5, 21.5), (21.5, 17)], r=S.r * 0.5)),
            shell(rect(6, 9, 12, 6.5, min(S.R, 2))),
            dot(9, 12.25, 1), detail(seg(12, 12.25, 15, 12.25))]


# ============================================================================ architecture

def hexagon(cx, cy, r, rr=0.0):
    return poly([polar(cx, cy, r, -90 + 60 * i) for i in range(6)], closed=True, r=rr)


_MS = [(9.3, 8), (14.7, 8), (6.6, 12.7), (12, 12.7), (17.4, 12.7), (9.3, 17.4)]


def _ms_filled():
    return U(*[P(hexagon(x, y, 2.75)) for x, y in _MS])


@icon("microservices", CAT, "Six small hexagons packed in a honeycomb cluster",
      tags=["microservices", "micro services", "service architecture", "distributed system", "small services", "honeycomb", "modules"],
      filled=_ms_filled)
def _(S):
    rr = 0 if S.name == "line" else 0.9
    return [shell(hexagon(x, y, 3, rr)) for x, y in _MS]


@icon("monolithic-architecture", CAT, "Single tall block divided by horizontal layer lines",
      tags=["monolith", "monolithic", "single application", "layered architecture", "all in one", "big app", "tiers"])
def _(S):
    return [shell(rect(5.5, 2.5, 13, 19, S.R)),
            detail(seg(5.5, 8.75, 18.5, 8.75)), detail(seg(5.5, 15.25, 18.5, 15.25)),
            dot(9, 5.6, 1), dot(9, 12, 1), dot(9, 18.4, 1)]


@icon("service-mesh", CAT, "Four small boxes at the corners, each linked to every other by crossing lines",
      tags=["service mesh", "mesh network", "interconnected services", "sidecar proxies", "full mesh", "network of services", "linked nodes"])
def _(S):
    return [line(seg(7.5, 5, 16.5, 5)), line(seg(7.5, 19, 16.5, 19)),
            line(seg(5, 7.5, 5, 16.5)), line(seg(19, 7.5, 19, 16.5)),
            line(seg(7.5, 7.5, 16.5, 16.5)), line(seg(16.5, 7.5, 7.5, 16.5)),
            shell(rect(2.5, 2.5, 5, 5, min(S.R, 2.5))), shell(rect(16.5, 2.5, 5, 5, min(S.R, 2.5))),
            shell(rect(2.5, 16.5, 5, 5, min(S.R, 2.5))), shell(rect(16.5, 16.5, 5, 5, min(S.R, 2.5)))]


@icon("sidecar-container", CAT, "Large ribbed container with a small container attached to its side",
      tags=["sidecar", "sidecar container", "helper container", "pod", "companion process", "attached container"])
def _(S):
    return [shell(rect(2.5, 4.5, 12, 15, min(S.R, 2.5))),
            detail(seg(6.5, 8, 6.5, 16)), detail(seg(10.5, 8, 10.5, 16)),
            shell(rect(16.5, 9, 5, 6.5, min(S.R, 1.5))),
            line(seg(14.5, 12.25, 16.5, 12.25))]


@icon("api-gateway", CAT, "Archway gate with three lines fanning out from it to small boxes",
      tags=["api gateway", "gateway", "entry point", "edge service", "routing", "fan out", "gate"])
def _(S):
    return [shell("M2.5 21V11A4.75 4.75 0 0 1 12 11V21Z"),
            line(seg(12, 12.5, 17.5, 5.5)), line(seg(12, 12.5, 17.5, 12.5)), line(seg(12, 12.5, 17.5, 19.5)),
            sq(17.5, 3.5, 4, 4, 0.8), sq(17.5, 10.5, 4, 4, 0.8), sq(17.5, 17.5, 4, 4, 0.8)]


def arrow_head(S, cx, cy, r, deg, size=3.0, k=0.85):
    """Chevron arrowhead at the clockwise end of an arc about (cx, cy)."""
    a = math.radians(deg)
    ex, ey = cx + r * math.cos(a), cy + r * math.sin(a)
    tx_, ty_ = -math.sin(a), math.cos(a)
    nx, ny = math.cos(a), math.sin(a)
    w1 = (ex - tx_ * size + nx * size * k, ey - ty_ * size + ny * size * k)
    w2 = (ex - tx_ * size - nx * size * k, ey - ty_ * size - ny * size * k)
    return poly([w1, (ex + tx_ * 0.4, ey + ty_ * 0.4), w2], r=S.r * 0.5)


def bolt(cx, cy, s=1.0):
    pts = [(1.6, -6), (-3.4, 1.2), (-0.4, 1.2), (-1.6, 6.5), (3.4, -1.4), (0.4, -1.4)]
    return [(cx + x * s, cy + y * s) for x, y in pts]


# ============================================================================ networking and messaging

@icon("load-balancer", CAT, "One circle at the top splitting into three lines that lead to three boxes",
      tags=["load balancer", "load balancing", "traffic distribution", "round robin", "fan out", "scale out", "balancer"])
def _(S):
    bx = [2.5, 9.5, 16.5]
    return [node(12, 4.5, 2.5),
            line(seg(12, 7, 12, 15.5)),
            line(bend(S, [(5, 15.5), (5, 11.5), (19, 11.5), (19, 15.5)], 3)),
            *[shell(rect(x, 15.5, 5, 5.5, min(S.R, 2))) for x in bx]]


@icon("content-delivery-network", CAT, "Globe with four small server squares placed around its outline",
      tags=["cdn", "content delivery network", "edge servers", "global delivery", "distribution", "worldwide", "caching nodes"])
def _(S):
    k = 0.5 if S.name == "line" else 1.4
    return [shell(circle(12, 12, 5.5)),
            detail(ellipse(12, 12, 2.2, 5.5)),
            sq(10.25, 1.5, 3.5, 3.5, k), sq(10.25, 19, 3.5, 3.5, k),
            sq(1.5, 10.25, 3.5, 3.5, k), sq(19, 10.25, 3.5, 3.5, k)]


@icon("edge-computing", CAT, "Cloud with a line dropping to a small chip with pins at the network edge",
      tags=["edge computing", "edge node", "edge device", "fog computing", "local processing", "iot edge", "chip"])
def _(S):
    return [shell(cloud(S, 0.5, 7, 10)),
            line(seg(12, 10, 12, 15)),
            shell(rect(8.75, 15, 6.5, 6.5, min(S.R, 1.5))),
            line(seg(5.5, 17, 8.75, 17)), line(seg(5.5, 19.5, 8.75, 19.5)),
            line(seg(15.25, 17, 18.5, 17)), line(seg(15.25, 19.5, 18.5, 19.5))]


@icon("event-bus", CAT, "Horizontal bus bar with three short lines dropping down to small solid boxes",
      tags=["event bus", "message bus", "bus", "publish subscribe backbone", "integration bus", "enterprise bus", "broadcast"])
def _(S):
    bx = [2.5, 9.5, 16.5]
    return [shell(rect(2.5, 3, 19, 4.5, min(S.R, 3))),
            *[line(seg(x + 2.5, 7.5, x + 2.5, 15.5)) for x in bx],
            *[sq(x, 15.5, 5, 5.5, 0.8 if S.name == "line" else 1.8) for x in bx]]


@icon("message-broker", CAT, "Central hub box marked with an envelope flap, arrows arriving on the left and leaving on the right",
      tags=["message broker", "message queue", "mq", "queue", "messaging hub", "envelopes"])
def _(S):
    return [shell(rect(7.5, 4.5, 9, 15, S.R)),
            detail(poly([(10, 10), (12, 12.5), (14, 10)], r=S.r * 0.5)),
            detail(seg(10, 15, 14, 15)),
            line(seg(2, 9, 6.5, 9)), line(poly([(4.5, 7), (6.5, 9), (4.5, 11)], r=S.r * 0.4)),
            line(seg(2, 15, 6.5, 15)), line(poly([(4.5, 13), (6.5, 15), (4.5, 17)], r=S.r * 0.4)),
            line(seg(17.5, 9, 22, 9)), line(poly([(20, 7), (22, 9), (20, 11)], r=S.r * 0.4)),
            line(seg(17.5, 15, 22, 15)), line(poly([(20, 13), (22, 15), (20, 17)], r=S.r * 0.4))]


@icon("pub-sub", CAT, "Broadcast tower on the left sending signal arcs toward three small boxes on the right",
      tags=["pub sub", "publish subscribe", "publisher", "subscribers", "broadcast", "topic", "notifications"])
def _(S):
    return [line(poly([(2.5, 21), (6, 12.5), (9.5, 21)], r=S.r * 0.4)),
            line(seg(3.8, 17.5, 8.2, 17.5)),
            dot(6, 9.5, 1.5),
            line(arc(6, 9.5, 4, -50, 50)), line(arc(6, 9.5, 7.5, -50, 50)),
            sq(16.5, 3.5, 4.5, 4.5, 1), sq(16.5, 10, 4.5, 4.5, 1), sq(16.5, 16.5, 4.5, 4.5, 1)]


@icon("event-stream", CAT, "Wavy line carrying small square packets along its length",
      tags=["event stream", "data stream", "streaming", "stream processing", "packets", "flow of events", "real time"])
def _(S):
    return [line("M2.5 15C5.5 15 6.5 9 9 9S12.5 15 15 15S18.5 9 21.5 9"),
            sq(7, 7, 4, 4, 0.8), sq(13, 13, 4, 4, 0.8), sq(19, 7, 3.5, 4, 0.8)]


@icon("event-driven", CAT, "Lightning bolt striking toward a small box that sends out a ripple ring",
      tags=["event driven", "event-driven architecture", "trigger", "reactive", "on event", "handler", "ripple"])
def _(S):
    return [shell(poly(bolt(7, 9.5, 1.2), closed=True, r=S.r * 0.4)),
            shell(circle(17, 16.5, 5)),
            sq(14.9, 14.4, 4.2, 4.2, 0.6 if S.name == "line" else 1.4)]


@icon("client-server", CAT, "Laptop on the left linked by a double line to a server tower on the right",
      tags=["client server", "client and server", "request response", "two tier", "network model", "web app", "laptop"])
def _(S):
    return [shell(rect(2, 7, 8, 6, min(S.R, 1.5))),
            line(seg(1.5, 16, 10.5, 16)),
            line(seg(11.5, 10, 14.5, 10)), line(seg(11.5, 13.5, 14.5, 13.5)),
            shell(rect(15.5, 3.5, 6, 17, min(S.R, 2))),
            dot(18.5, 7.25, 1), detail(seg(16.5, 11.5, 20.5, 11.5)), dot(18.5, 16, 1)]


@icon("peer-to-peer", CAT, "Three screens in a triangle, each connected to the other two",
      tags=["peer to peer", "p2p", "decentralized", "torrent", "mesh of peers", "direct connection", "distributed"])
def _(S):
    return [line(seg(11, 8.2, 6, 16)), line(seg(13, 8.2, 18, 16)), line(seg(8, 18.5, 16, 18.5)),
            shell(rect(8.75, 2.5, 6.5, 5, min(S.R, 1.5))),
            shell(rect(2.5, 16, 6.5, 5, min(S.R, 1.5))), shell(rect(15, 16, 6.5, 5, min(S.R, 1.5)))]


@icon("cache-memory", CAT, "Chip outline with pins on every side and a lightning bolt in its center",
      tags=["cache", "cache memory", "fast memory", "l1 cache", "memory chip", "ram", "speed"])
def _(S):
    pins = [9.5, 14.5]
    return [shell(rect(5.5, 5.5, 13, 13, min(S.R, 3))),
            Part("dot", poly(bolt(12, 12, 0.85), closed=True)),
            *[line(seg(x, 2.5, x, 5.5)) for x in pins], *[line(seg(x, 18.5, x, 21.5)) for x in pins],
            *[line(seg(2.5, y, 5.5, y)) for y in pins], *[line(seg(18.5, y, 21.5, y)) for y in pins]]


@icon("rate-limiter", CAT, "Funnel with a speedometer needle beside its spout",
      tags=["rate limit", "rate limiter", "throttle", "throttling", "requests per second", "quota", "funnel"])
def _(S):
    return [shell(poly([(2.5, 3.5), (14.5, 3.5), (10.5, 11.5), (10.5, 20), (6.5, 20), (6.5, 11.5)], closed=True, r=S.r * 0.8)),
            line(arc(18, 15.5, 3.7, 180, 360)), line(seg(13.5, 15.5, 22.5, 15.5)),
            line(seg(18, 15.5, 19.8, 12.6))]


@icon("circuit-breaker-pattern", CAT, "Service box above a broken chain link with a lightning bolt in the gap",
      tags=["circuit breaker", "fail fast", "resilience", "fault tolerance", "broken link", "service protection", "cut off"])
def _(S):
    return [shell(rect(6.5, 2.5, 11, 7, min(S.R, 2))), dot(9.5, 6, 1), detail(seg(12, 6, 15, 6)),
            line("M9 13.5H7.5A3.5 3.5 0 0 0 7.5 20.5H9"), line("M15 13.5H16.5A3.5 3.5 0 0 1 16.5 20.5H15"),
            Part("dot", poly(bolt(12, 17, 0.55), closed=True))]


@icon("retry-policy", CAT, "Circular arrow wrapped around the number three",
      tags=["retry", "retry policy", "retries", "backoff", "try again", "attempts", "repeat request"])
def _(S):
    return [line(arc(12, 12, 8.5, -45, 225)),
            line(arrow_head(S, 12, 12, 8.5, 225, 3.2)),
            line("M9.5 8.7H14.5L11.8 11.9A3.2 3.2 0 1 1 9.2 16.2")]


@icon("request-timeout", CAT, "Hourglass above a broken chain link, a request that took too long",
      tags=["timeout", "request timeout", "timed out", "deadline exceeded", "too slow", "connection lost", "hourglass"])
def _(S):
    return [shell(poly([(7.5, 2.5), (16.5, 2.5), (12.8, 8.5), (16.5, 14.5), (7.5, 14.5), (11.2, 8.5)], closed=True, r=S.r * 0.6)),
            line("M9.5 17.5H8.5A2 2 0 0 0 8.5 21.5H9.5"), line("M14.5 17.5H15.5A2 2 0 0 1 15.5 21.5H14.5")]


@icon("callback-function", CAT, "Function parentheses with a curved arrow looping back up into them",
      tags=["callback", "callback function", "call back", "handler", "continuation", "async return", "function"])
def _(S):
    return [line("M9 3C6 6.5 6 10.5 9 14"), line("M15 3C18 6.5 18 10.5 15 14"),
            line(bend(S, [(16.5, 15.5), (16.5, 20.5), (7.5, 20.5), (7.5, 15.5)], 3)),
            line(poly([(5.2, 17.5), (7.5, 15), (9.8, 17.5)], r=S.r * 0.4))]


@icon("object-storage-bucket", CAT, "Pail bucket with three small cubes sitting above its rim",
      tags=["object storage", "bucket", "blob storage", "storage bucket", "files in cloud", "cubes"])
def _(S):
    return [shell(poly([(4, 9), (20, 9), (18, 21), (6, 21)], closed=True, r=S.r)),
            detail(seg(4.7, 13.5, 19.3, 13.5)),
            sq(5.5, 3.5, 3.5, 3.5, 0.6), sq(10.25, 3.5, 3.5, 3.5, 0.6), sq(15, 3.5, 3.5, 3.5, 0.6)]


@icon("cloud-database", CAT, "Cloud outline with a database cylinder standing in front of its base",
      tags=["cloud database", "managed database", "dbaas", "hosted database", "cloud storage", "data in the cloud", "cylinder"])
def _(S):
    cyl = "M7.5 15.5V19.5A4.5 1.9 0 0 0 16.5 19.5V15.5A4.5 1.9 0 0 0 7.5 15.5Z"
    cd = cloud(S, 0.82, 3.5, 17)
    body = ST(cd, 2, S.cap, S.join)
    return [behind(body, cyl, 1.2),
            shell(cyl),
            detail("M7.5 15.5A4.5 1.9 0 0 0 16.5 15.5")]
