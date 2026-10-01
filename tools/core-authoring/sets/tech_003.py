"""TypeIcon Core: tech (developer concepts, batch 003): systems, concurrency, data structures, language
features, tooling and agile practice."""
import math

from dsl import arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "tech"


def _pick(S, sharp, soft):
    return sharp if S.name == "line" else soft


def head(S, x, y, deg, L=3.2, spread=42):
    """Arrowhead chevron with its tip at (x, y) pointing along deg."""
    a1, a2 = math.radians(deg + 180 - spread), math.radians(deg + 180 + spread)
    p1 = (x + L * math.cos(a1), y + L * math.sin(a1))
    p2 = (x + L * math.cos(a2), y + L * math.sin(a2))
    return line(poly([p1, (x, y), p2], r=S.r))


def arc_arrow(S, cx, cy, r, a0, a1, L=3.2):
    tip = polar(cx, cy, r, a1)
    return [line(arc(cx, cy, r, a0, a1)), head(S, tip[0], tip[1], a1 + 90, L)]


def gear_d(S, cx, cy, ro, ri, n=8, hw_o=11.0, hw_i=17.0):
    pts = []
    for i in range(n):
        a = i * 360 / n
        pts += [polar(cx, cy, ri, a - hw_i), polar(cx, cy, ro, a - hw_o),
                polar(cx, cy, ro, a + hw_o), polar(cx, cy, ri, a + hw_i)]
    return poly(pts, closed=True, r=_pick(S, 0, 0.5))


def wave(x, y, n, w=4.0, h=2.5):
    return f"M{fmt(x)} {fmt(y)}q{fmt(w / 2)} {fmt(-h)} {fmt(w)} 0" + f"t{fmt(w)} 0" * (n - 1)


def padlock(S, cx, top, bw=11, bh=8, sh=3.0):
    """Padlock: shackle above a body, body top at `top`."""
    return [shell(rect(cx - bw / 2, top, bw, bh, min(S.R, 2))),
            line(f"M{fmt(cx - sh)} {fmt(top)}V{fmt(top - 2.5)}a{fmt(sh)} {fmt(sh)} 0 0 1 {fmt(2 * sh)} 0V{fmt(top)}")]


def person(S, cx, cy, r=2.75, sh=6.0, bottom=None):
    """Head and shoulders: head circle at (cx, cy)."""
    by = cy + r + 1.5 if bottom is None else bottom
    return [shell(circle(cx, cy, r)),
            line(f"M{fmt(cx - sh)} {fmt(by + 5)}v-1a{fmt(sh)} {fmt(sh * 0.6)} 0 0 1 {fmt(2 * sh)} 0v1")]


# =========================================================================== chunk 1: systems and concurrency

@icon("system-snapshot", CAT, "A server box inside camera viewfinder corners.",
      tags=["snapshot", "backup", "server", "restore point", "capture", "vm"])
def _(S):
    c = 2.5
    return [line(poly([(c, 8), (c, c), (8, c)], r=S.r)), line(poly([(16, c), (24 - c, c), (24 - c, 8)], r=S.r)),
            line(poly([(c, 16), (c, 24 - c), (8, 24 - c)], r=S.r)), line(poly([(16, 24 - c), (24 - c, 24 - c), (24 - c, 16)], r=S.r)),
            shell(rect(7, 8, 10, 8, min(S.R, 2))), detail(seg(7, 12, 17, 12)), dot(14.5, 14, 0.9)]


@icon("raid-array", CAT, "Four hard drives in a grid joined by a bracket above.",
      tags=["raid", "disk array", "hard drives", "redundancy", "storage", "mirroring"])
def _(S):
    out = [line(poly([(5.5, 7), (5.5, 3.5), (18.5, 3.5), (18.5, 7)], r=S.r))]
    for x in (3, 13):
        for y in (9.5, 16):
            out += [shell(rect(x, y, 8, 3.5, min(S.R, 1.5))), dot(x + 6, y + 1.75, 0.6)]
    return out


@icon("storage-array", CAT, "A tall cabinet with rows of drive slots and status lights.",
      tags=["san", "nas", "disk shelf", "rack", "drives", "storage cabinet"])
def _(S):
    out = [shell(rect(4.5, 2.5, 15, 19, min(S.R, 2.5))), detail(seg(4.5, 8.5, 19.5, 8.5)), detail(seg(4.5, 14.5, 19.5, 14.5))]
    for y in (5.5, 11.5, 18):
        out += [dot(8.5, y, 1.0), detail(seg(12, y, 16, y))]
    return out


@icon("block-storage", CAT, "Three flat blocks stacked and joined edge to edge.",
      tags=["block device", "volume", "disk volume", "ebs", "blocks", "storage"])
def _(S):
    out = [line(seg(12, 6, 12, 18))]
    for y in (3.5, 10.5, 17.5):
        out.append(shell(rect(3, y, 18, 3, _pick(S, 0, 1.5))))
    return out


@icon("tape-backup", CAT, "A tape cartridge with a label strip and a window showing two reels.",
      tags=["tape", "cassette", "archive", "backup", "cold storage", "magnetic tape"])
def _(S):
    return [shell(rect(2.5, 4.5, 19, 15, min(S.R, 3))), detail(seg(6, 8.2, 18, 8.2)),
            detail(rect(6, 11, 12, 5.5, 2.75)), dot(9.5, 13.75, 1.1), dot(14.5, 13.75, 1.1)]


@icon("system-monitor", CAT, "A window with a title bar and three bar meters.",
      tags=["task manager", "resource monitor", "cpu", "memory usage", "metrics", "performance"])
def _(S):
    return [shell(rect(2.5, 3.5, 19, 17, S.R)), detail(seg(2.5, 8, 21.5, 8)),
            detail(seg(7, 17.5, 7, 13)), detail(seg(12, 17.5, 12, 11)), detail(seg(17, 17.5, 17, 14.5))]


@icon("process-tree", CAT, "A gear at the top with lines branching down to three child processes.",
      tags=["process", "parent child", "fork", "pid", "hierarchy", "os"])
def _(S):
    out = [shell(gear_d(S, 12, 5.5, 4.5, 3.4, 8)), detail(circle(12, 5.5, 1.2))]
    out += [line(poly([(12, 10.5), (12, 13), (4.5, 13), (4.5, 16)], r=_pick(S, 0, 1.5))), line(seg(12, 13, 12, 16)),
            line(poly([(12, 13), (19.5, 13), (19.5, 16)], r=_pick(S, 0, 1.5)))]
    for x in (4.5, 12, 19.5):
        out.append(shell(circle(x, 19, 2.5)))
    return out


@icon("execution-thread", CAT, "A needle trailing a wavy thread behind it.",
      tags=["thread", "thread of execution", "stitch", "needle", "concurrency", "flow"])
def _(S):
    return [line(seg(21.5, 2.5, 14, 10)), line("M19.5 4.5C23 10 16 12 12 14S7 19 3 18")]


@icon("multithreading", CAT, "Three parallel wavy threads running side by side with arrow tips.",
      tags=["parallel", "threads", "concurrent", "multithread", "multi-threaded", "concurrency"], aliases=["multi-threading"])
def _(S):
    out = []
    for y in (5.5, 12, 18.5):
        out += [line(wave(3, y, 3, 4, 2.2)), head(S, 20.5, y, 0, 3.4)]
    return out


@icon("mutex", CAT, "A padlock sitting on a single wavy thread line.",
      tags=["lock", "mutual exclusion", "critical section", "synchronization", "thread safety", "semaphore"])
def _(S):
    return padlock(S, 12, 8.5, 11, 7.5, 3.0) + [line(wave(2.5, 20.5, 4, 4.75, 1.8))]


@icon("deadlock", CAT, "Two arrows chasing each other in a circle around a padlock.",
      tags=["deadlock", "blocked", "stuck", "circular wait", "concurrency", "hang"])
def _(S):
    out = arc_arrow(S, 12, 12, 9, 200, 330, 3.0) + arc_arrow(S, 12, 12, 9, 20, 150, 3.0)
    out += [solid(rect(9.5, 11.5, 5, 4)), line("M10.5 11.5V10.5a1.5 1.5 0 0 1 3 0V11.5")]
    return out


@icon("race-condition", CAT, "Two arrows racing toward one box under a finish flag.",
      tags=["race", "concurrency bug", "data race", "timing", "nondeterministic", "threads"])
def _(S):
    return [line(seg(2.5, 14, 10, 14)), head(S, 11.5, 14, 0, 3.0), line(seg(2.5, 19.5, 10, 19.5)), head(S, 11.5, 19.5, 0, 3.0),
            shell(rect(14.5, 11.5, 7, 9, min(S.R, 2))),
            line(seg(18, 11.5, 18, 2.5)), solid("M18 2.5L22.5 4.5L18 6.5Z")]


@icon("memory-leak", CAT, "A RAM stick with drops dripping from its bottom edge.",
      tags=["leak", "ram", "memory", "out of memory", "oom", "garbage collection"])
def _(S):
    drop = lambda x, y: f"M{fmt(x)} {fmt(y)}C{fmt(x + 0.6)} {fmt(y + 1.6)} {fmt(x + 2)} {fmt(y + 2.8)} {fmt(x + 2)} {fmt(y + 4.2)}a2 2 0 0 1 -4 0C{fmt(x - 2)} {fmt(y + 2.8)} {fmt(x - 0.6)} {fmt(y + 1.6)} {fmt(x)} {fmt(y)}Z"
    return [shell(rect(2.5, 3.5, 19, 8, min(S.R, 2))), dot(7, 7.5, 1.1), dot(12, 7.5, 1.1), dot(17, 7.5, 1.1),
            shell(drop(8, 14.5)), shell(drop(16, 15.5))]


@icon("heap-memory", CAT, "A pile of uneven stacked blocks of different sizes.",
      tags=["heap", "dynamic memory", "allocation", "malloc", "memory pool", "pile"])
def _(S):
    R = _pick(S, 0, 1.5)
    return [shell(rect(3, 16, 8, 4.5, R)), shell(rect(13.5, 15.5, 7.5, 5, R)),
            shell(rect(5, 9.5, 5, 3.5, R)), shell(rect(13, 8, 7, 4, R)),
            shell(rect(8, 3, 6, 3, R))]


@icon("event-loop", CAT, "A looping arrow with small task squares riding around it.",
      tags=["event loop", "async", "queue", "tick", "javascript runtime", "scheduler"])
def _(S):
    out = []
    for a in (175, 355):
        x, y = polar(12, 12, 8.5, a)
        out.append(solid(rect(x - 2, y - 2, 4, 4)))
    out += arc_arrow(S, 12, 12, 8.5, 205, 320, 3.0) + arc_arrow(S, 12, 12, 8.5, 25, 140, 3.0)
    return out


# =========================================================================== chunk 2: errors, control flow, types


def brace(S, x, y0, y1, left=True, w=2.5, part=line):
    mid = (y0 + y1) / 2
    k = 1 if left else -1
    x0 = x + k * w   # outer end points
    tip = x - k * w
    d = (f"M{fmt(x0)} {fmt(y0)}Q{fmt(x)} {fmt(y0)} {fmt(x)} {fmt(y0 + w)}V{fmt(mid - w)}Q{fmt(x)} {fmt(mid)} {fmt(tip)} {fmt(mid)}"
         f"Q{fmt(x)} {fmt(mid)} {fmt(x)} {fmt(mid + w)}V{fmt(y1 - w)}Q{fmt(x)} {fmt(y1)} {fmt(x0)} {fmt(y1)}")
    return part(d)


def hashsign(S, cx, cy, s=10.0, gap=4.0):
    h, g = s / 2, gap / 2
    return [line(seg(cx - g, cy - h, cx - g, cy + h)), line(seg(cx + g, cy - h, cx + g, cy + h)),
            line(seg(cx - h, cy - g, cx + h, cy - g)), line(seg(cx - h, cy + g, cx + h, cy + g))]


@icon("stack-trace", CAT, "A list of indented lines with an arrow pointing up to the top line.",
      tags=["call stack", "traceback", "backtrace", "debug", "error log", "frames"])
def _(S):
    out = [line(seg(3.5, 20, 3.5, 5)), head(S, 3.5, 4, -90, 3.2)]
    for y, x in ((5, 8), (10, 10), (15, 12), (20, 14)):
        out.append(line(seg(x, y, 21, y)))
    return out


@icon("exception-error", CAT, "Curly braces around an exclamation mark.",
      tags=["exception", "throw", "error handling", "try catch", "runtime error", "fault"])
def _(S):
    return [brace(S, 6.5, 3, 21, True), brace(S, 17.5, 3, 21, False),
            line(seg(12, 6.5, 12, 13)), dot(12, 17, 1.4)]


@icon("syntax-error", CAT, "Code lines with a wavy underline beneath the last words.",
      tags=["syntax", "parse error", "typo", "squiggle", "invalid code", "lint warning"])
def _(S):
    return [line(seg(3, 5, 9, 5)), line(seg(12, 5, 20, 5)), line(seg(6, 10.5, 12, 10.5)), line(seg(15, 10.5, 21, 10.5)),
            line(seg(3, 16, 8, 16)), line(wave(11.5, 19, 3, 3.2, 1.8))]


@icon("compile-error", CAT, "A gear with a cross mark beside it.",
      tags=["build failed", "compiler", "compilation", "gear", "broken build", "error"])
def _(S):
    return [shell(gear_d(S, 9, 9, 6.6, 5.0, 8)), detail(circle(9, 9, 1.8)),
            line(seg(16.5, 16.5, 21.5, 21.5)), line(seg(21.5, 16.5, 16.5, 21.5))]


@icon("null-pointer", CAT, "An arrow pointing into an empty dashed circle.",
      tags=["null", "nil", "none", "undefined", "empty reference", "segfault"])
def _(S):
    out = [line(seg(2.5, 12, 8, 12)), head(S, 9.5, 12, 0, 3.2)]
    for a in range(0, 360, 60):
        out.append(line(arc(16, 12, 5.5, a + 8, a + 38)))
    return out


@icon("infinite-loop", CAT, "A circular arrow with an infinity mark inside it.",
      tags=["endless loop", "infinity", "forever", "while true", "repeat", "never ends"])
def _(S):
    return arc_arrow(S, 12, 12, 9.5, 20, 320, 3.2) + [
        line("M12 12C10.5 8.8 6.5 8.8 6.5 12S10.5 15.2 12 12S17.5 8.8 17.5 12S13.5 15.2 12 12Z")]


@icon("recursion", CAT, "A square spiral winding inward toward the centre.",
      tags=["recursive", "self call", "spiral", "nested", "repeat", "function calls itself"])
def _(S):
    r = _pick(S, 0, 1.5)
    return [line(poly([(3, 21), (3, 3), (21, 3), (21, 21), (8, 21), (8, 8), (16, 8), (16, 16), (12, 16), (12, 12)], r=r))]


@icon("conditional-branch", CAT, "A decision diamond with two exits, one ending in a check and one in a cross.",
      tags=["if else", "decision", "condition", "branching", "flowchart", "true false"])
def _(S):
    return [shell(poly([(12, 2), (17, 6), (12, 10), (7, 6)], closed=True, r=S.r * 0.6)),
            line(seg(12, 10, 12, 12.5)),
            line(poly([(6, 16), (6, 12.5), (18, 12.5), (18, 16)], r=S.r)),
            line(poly([(3.5, 19), (5.5, 21), (8.5, 17.5)], r=S.r * 0.5)),
            line(seg(16, 17.5, 20, 21.5)), line(seg(20, 17.5, 16, 21.5))]


@icon("switch-case", CAT, "One line splitting into three parallel tracks like a railway switch.",
      tags=["switch", "case", "multi-way branch", "router", "points", "select"])
def _(S):
    r = _pick(S, 0, 3)
    return [line(poly([(2.5, 12), (8, 12), (11.5, 5), (19, 5)], r=r)), line(seg(2.5, 12, 19, 12)),
            line(poly([(8, 12), (11.5, 19), (19, 19)], r=r)),
            head(S, 21.5, 5, 0, 3), head(S, 21.5, 12, 0, 3), head(S, 21.5, 19, 0, 3)]


@icon("boolean-type", CAT, "A pill split in half with a check on one side and a cross on the other.",
      tags=["boolean", "bool", "true false", "binary", "toggle value", "data type"])
def _(S):
    return [shell(rect(2.5, 6, 19, 12, _pick(S, 3, 6))), detail(seg(12, 6, 12, 18)),
            detail(poly([(5.5, 12), (7.3, 14), (10, 10)], r=0)),
            detail(seg(14.5, 9.5, 18.5, 14.5 - 0.5)), detail(seg(18.5, 9.5, 14.5, 14))]


@icon("integer-type", CAT, "The digits 1, 2 and 3 in a row.",
      tags=["integer", "int", "number", "whole number", "numeric", "data type"])
def _(S):
    r = _pick(S, 0, 1)
    return [line(poly([(2.5, 9), (4.5, 7), (4.5, 17)], r=r)),
            line(poly([(8.5, 9.5), (9.5, 7.5), (13, 7.5), (14.5, 9.5), (14.5, 11.5), (8.5, 17), (14.5, 17)], r=r)),
            line(poly([(17.5, 8), (19, 7.5), (21.5, 9), (21.5, 11), (19.5, 12), (21.5, 13.5), (21.5, 15.5), (19, 17), (17.5, 16.5)], r=r))]


def q6(x, y):
    return [dot(x, y, 2.2), line(f"M{fmt(x - 2.2)} {fmt(y)}c0 -3.5 1 -5 3.2 -6")]


def q9(x, y):
    return [dot(x, y, 2.2), line(f"M{fmt(x + 2.2)} {fmt(y)}c0 3.5 -1 5 -3.2 6")]


@icon("string-type", CAT, "Opening and closing quotation marks.",
      tags=["string", "text", "quotes", "str", "characters", "data type"])
def _(S):
    return q6(4.5, 15.5) + q6(10.5, 15.5) + q9(13.5, 8.5) + q9(19.5, 8.5)


@icon("linked-list", CAT, "Three boxes stepping down the grid, each linked to the next by an elbow arrow.",
      tags=["linked list", "nodes", "pointers", "data structure", "next pointer", "chain"])
def _(S):
    R = _pick(S, 0, 1)
    return [shell(rect(2, 2, 4.5, 4.5, R)), shell(rect(9.75, 9.75, 4.5, 4.5, R)), shell(rect(17.5, 17.5, 4.5, 4.5, R)),
            line(poly([(7.5, 4.25), (12, 4.25), (12, 7)], r=0)), head(S, 12, 8.4, 90, 2.6),
            line(poly([(15.25, 12), (19.75, 12), (19.75, 14.8)], r=0)), head(S, 19.75, 16.2, 90, 2.6)]


@icon("hash-map", CAT, "Two columns of cells with arrows from the left cells to the right cells.",
      tags=["hash table", "dictionary", "key value", "map", "associative array", "buckets"])
def _(S):
    out = []
    for x in (2.5, 16.5):
        out += [shell(rect(x, 3, 5, 18, min(S.R, 2))), detail(seg(x, 9, x + 5, 9)), detail(seg(x, 15, x + 5, 15))]
    out += [line(seg(10, 6, 14, 6)), head(S, 14.6, 6, 0, 2.4), line(seg(10, 12, 14, 18)), head(S, 14.2, 18.1, 45, 2.4)]
    return out


@icon("hash-function", CAT, "A long line passing through an arrow and coming out as a short hash block.",
      tags=["hash", "digest", "checksum", "sha", "md5", "fingerprint", "one way"])
def _(S):
    return [line(seg(2.5, 3.5, 21.5, 3.5)), line(seg(12, 6.5, 12, 9)), head(S, 12, 10.5, 90, 3.0)] + hashsign(S, 12, 17, 9, 3.6)


@icon("sorting-algorithm", CAT, "Bars of increasing height with two opposing swap arrows above the first bars.",
      tags=["sort", "bubble sort", "order", "swap", "ascending", "algorithm"])
def _(S):
    out = []
    for x, top in ((4, 19), (9.5, 16.5), (15, 14), (20.5, 11.5)):
        out.append(line(seg(x, 22, x, top)))
    out += [line(seg(3, 3.5, 11, 3.5)), head(S, 12.5, 3.5, 0, 3.0), line(seg(13, 9, 5, 9)), head(S, 3.5, 9, 180, 3.0)]
    return out


# =========================================================================== chunk 3: structures and language features

def node(x, y, r=2.2):
    return shell(circle(x, y, r))


def hollow(S, x, y, r=2.4):
    return shell(circle(x, y, r) if S.name == "rounded" else rect(x - r, y - r, 2 * r, 2 * r))


@icon("tree-traversal", CAT, "A small tree where the visited nodes are solid and the others are hollow.",
      tags=["tree", "dfs", "bfs", "binary tree", "walk", "visit nodes", "depth first"])
def _(S):
    return [line(seg(10.3, 6.4, 7.6, 10.2)), line(seg(13.7, 6.4, 16.4, 10.2)),
            line(seg(5.3, 14.6, 4.4, 17.2)), line(seg(7.7, 14.6, 8.6, 17.2)),
            solid(circle(12, 4.6, 2.6)), solid(circle(6.5, 12.5, 2.6)), solid(circle(3.5, 19.5, 2.6)),
            hollow(S, 17.5, 12.5), hollow(S, 9.5, 19.5)]


@icon("trie-structure", CAT, "A root dot with branches ending in small letter boxes.",
      tags=["trie", "prefix tree", "autocomplete tree", "radix", "dictionary tree", "letters"])
def _(S):
    R = _pick(S, 0, 1)
    out = [solid(circle(12, 4, 2.2)),
           line(poly([(12, 6), (12, 8)], r=0)),
           line(poly([(4.5, 11), (4.5, 8), (19.5, 8), (19.5, 11)], r=S.r)), line(seg(12, 8, 12, 11))]
    for x in (4.5, 12, 19.5):
        out.append(shell(rect(x - 2, 11.5, 4, 4, R)))
    out += [line(seg(4.5, 17.5, 4.5, 19)), line(seg(12, 17.5, 12, 19)), solid(circle(4.5, 20.5, 1.4)), solid(circle(12, 20.5, 1.4))]
    return out


@icon("big-o-notation", CAT, "A capital O followed by parentheses with an n inside.",
      tags=["big o", "complexity", "time complexity", "o(n)", "algorithm analysis", "asymptotic"])
def _(S):
    return [line(ellipse(5.5, 12, 3, 4.6)), line("M11.5 5.5C9.5 9.5 9.5 14.5 11.5 18.5"),
            line("M14.5 16.5V11"), line("M14.5 13a2.2 2.2 0 0 1 4.4 0v3.5"),
            line("M21 5.5C23 9.5 23 14.5 21 18.5")]


@icon("pointer-reference", CAT, "An ampersand with an arrow extending from it.",
      tags=["pointer", "reference", "address of", "ampersand", "memory address", "c pointer"])
def _(S):
    return [line("M14 19.5L5.2 10.2C3.4 8 4.4 3.6 8.4 3.6S12.8 8 9.2 10.8C5.2 14 3.5 15.5 3.5 17S5.6 20.5 8.2 20.5 11.8 19 14 15"),
            line(seg(15.5, 12, 21, 12)), head(S, 21.5, 12, 0, 3.2)]


@icon("class-object", CAT, "A box divided into a title bar and two stacked sections.",
      tags=["class", "object", "oop", "uml class", "attributes methods", "object oriented"])
def _(S):
    return [shell(rect(3.5, 2.5, 17, 19, S.R)), detail(seg(3.5, 8.5, 20.5, 8.5)), detail(seg(3.5, 15, 20.5, 15)),
            detail(seg(8, 5.5, 16, 5.5))]


@icon("inheritance", CAT, "Two boxes with a hollow triangle arrow pointing from the lower box to the upper one.",
      tags=["extends", "subclass", "parent child", "oop", "uml generalization", "derived class"])
def _(S):
    R = _pick(S, 0, 1.5)
    return [shell(rect(6, 2.5, 12, 4, R)), shell(poly([(12, 9.5), (8.5, 14.5), (15.5, 14.5)], closed=True, r=S.r * 0.4)),
            line(seg(12, 14.5, 12, 17.5)), shell(rect(6, 17.5, 12, 3.5, R))]


@icon("code-interface", CAT, "A circle on a stick joined to a class box, the lollipop notation.",
      tags=["interface", "lollipop", "uml interface", "api contract", "implements", "oop"])
def _(S):
    return [node(12, 4.8, 2.6), line(seg(12, 7.4, 12, 12)), shell(rect(4, 12, 16, 9, min(S.R, 2.5))), detail(seg(4, 16, 20, 16))]


@icon("code-module", CAT, "A cube with code brackets on its front face.",
      tags=["module", "package", "library", "component", "cube", "code package"])
def _(S):
    return [shell(rect(3, 9, 12, 12, min(S.R, 2))), line(poly([(3, 9), (7, 4), (19.5, 4), (15, 9)], r=0)),
            line(poly([(19.5, 4), (19.5, 16), (15, 21)], r=0)),
            detail(poly([(7.8, 12.5), (6, 15), (7.8, 17.5)], r=0)), detail(poly([(10.2, 12.5), (12, 15), (10.2, 17.5)], r=0))]


@icon("namespace", CAT, "A folder with curly braces on its body.",
      tags=["namespace", "scope", "package name", "folder", "grouping", "braces"])
def _(S):
    return [shell(poly([(2.5, 20), (2.5, 4.5), (9.5, 4.5), (12, 7.5), (21.5, 7.5), (21.5, 20)], closed=True, r=S.r)),
            brace(S, 8.5, 10.5, 17.5, True, 1.6, detail), brace(S, 15.5, 10.5, 17.5, False, 1.6, detail)]


@icon("import-statement", CAT, "A tray with an arrow dropping into it and angle brackets above.",
      tags=["import", "require", "include", "load module", "dependency", "using"])
def _(S):
    return [line(poly([(3.5, 12.5), (3.5, 20.5), (20.5, 20.5), (20.5, 12.5)], r=S.r)),
            line(seg(12, 4, 12, 12)), head(S, 12, 14, 90, 3.4),
            line(poly([(6.5, 3.5), (4, 6), (6.5, 8.5)], r=0)), line(poly([(17.5, 3.5), (20, 6), (17.5, 8.5)], r=0))]


@icon("enum-type", CAT, "A short numbered list of three items inside curly braces.",
      tags=["enum", "enumeration", "constants list", "named values", "options", "variants"])
def _(S):
    out = [brace(S, 4.5, 3, 21, True), brace(S, 19.5, 3, 21, False)]
    for y in (7.5, 12, 16.5):
        out += [dot(9.5, y, 1.1), line(seg(12.5, y, 15.5, y))]
    return out


@icon("constant-value", CAT, "A padlock with a pi sign on its body.",
      tags=["constant", "const", "immutable", "final", "readonly", "fixed value"])
def _(S):
    return [shell(rect(4.5, 10, 15, 11, min(S.R, 2.5))), line("M8 10V7a4 4 0 0 1 8 0v3"),
            detail(seg(8.5, 13.7, 15.5, 13.7)), detail(seg(10.5, 13.7, 10.5, 18)), detail(seg(13.5, 13.7, 13.5, 18))]


@icon("generic-type", CAT, "Angle brackets around a capital letter T.",
      tags=["generics", "template", "type parameter", "t", "angle brackets", "parametric"])
def _(S):
    return [line(poly([(7, 5.5), (2.5, 12), (7, 18.5)], r=S.r)), line(poly([(17, 5.5), (21.5, 12), (17, 18.5)], r=S.r)),
            line(seg(9, 7.5, 15, 7.5)), line(seg(12, 7.5, 12, 17))]


@icon("type-annotation", CAT, "A colon followed by a capital letter T in a box.",
      tags=["type hint", "typing", "static types", "typescript", "annotation", "colon"])
def _(S):
    return [dot(5, 9.5, 1.4), dot(5, 15, 1.4), shell(rect(9.5, 5, 12, 14, min(S.R, 3))),
            detail(seg(12.5, 9.2, 18.5, 9.2)), detail(seg(15.5, 9.2, 15.5, 15.5))]


@icon("iterator", CAT, "An arrow stepping down onto one dot in a row of dots.",
      tags=["iterate", "next", "cursor", "loop over", "for each", "step through"])
def _(S):
    out = [line(seg(9.5, 3, 9.5, 11)), head(S, 9.5, 12.5, 90, 3.4)]
    for x in (3.5, 9.5, 15.5, 21):
        out.append(dot(x, 18, 1.7))
    return out


# =========================================================================== chunk 4: language tooling

def chev_l(S, x, cy, h=4.0, w=3.5, part=line):
    return part(poly([(x + w, cy - h), (x, cy), (x + w, cy + h)], r=S.r * 0.5))


def chev_r(S, x, cy, h=4.0, w=3.5, part=line):
    return part(poly([(x - w, cy - h), (x, cy), (x - w, cy + h)], r=S.r * 0.5))


@icon("code-decorator", CAT, "An at sign sitting on top of function parentheses.",
      tags=["decorator", "annotation", "at sign", "attribute", "wrapper", "python decorator"])
def _(S):
    return [line(arc(12, 8, 5.8, 25, 340)), shell(circle(11.4, 8.3, 2.0)), line(seg(13.4, 6.4, 13.4, 10.2)),
            line("M9 15C6.8 17.5 6.8 19.5 9 22"), line("M15 15C17.2 17.5 17.2 19.5 15 22")]


@icon("async-await", CAT, "An hourglass beside a forward arrow.",
      tags=["async", "await", "promise", "wait", "asynchronous", "pending"])
def _(S):
    r = S.r * 0.4
    return [shell(poly([(3.5, 3.5), (12.5, 3.5), (8, 11.5)], closed=True, r=r)),
            shell(poly([(8, 12.5), (3.5, 20.5), (12.5, 20.5)], closed=True, r=r)),
            line(seg(15.5, 12, 21, 12)), head(S, 21.5, 12, 0, 3.2)]


@icon("code-comment", CAT, "Two slashes followed by a speech bubble.",
      tags=["comment", "slashes", "annotation", "note in code", "double slash", "documentation"])
def _(S):
    return [line(seg(3, 18.5, 6, 6.5)), line(seg(7.5, 18.5, 10.5, 6.5)),
            shell(poly([(13.5, 5), (21.5, 5), (21.5, 14), (17.5, 14), (14.5, 17.5), (14.5, 14), (13.5, 14)], closed=True, r=S.r))]


@icon("todo-comment", CAT, "Code lines with a small empty check box before the first one.",
      tags=["todo", "fixme", "task in code", "pending work", "checkbox", "reminder"])
def _(S):
    return [shell(rect(3, 4, 6, 6, min(S.R, 1.5))), line(seg(12.5, 7, 21, 7)),
            line(seg(6, 14, 16, 14)), line(seg(6, 19, 13, 19))]


@icon("autocomplete", CAT, "A text cursor with a dropdown list of three suggestions below.",
      tags=["suggestions", "intellisense", "completion", "dropdown", "typeahead", "code completion"])
def _(S):
    return [line(seg(3, 5, 9, 5)), line(seg(12, 2.5, 12, 7.5)),
            shell(rect(3, 10, 18, 11.5, min(S.R, 2))),
            detail(seg(6.5, 13, 15, 13)), detail(seg(6.5, 16, 17.5, 16)), detail(seg(6.5, 19, 12.5, 19))]


@icon("code-formatter", CAT, "Messy lines on the left becoming neat indented lines on the right, with a wand between.",
      tags=["formatter", "prettify", "beautify", "indent", "auto format", "clean code"])
def _(S):
    out = [line(seg(3, 5, 8, 5)), line(seg(2.5, 10, 6, 10)), line(seg(4, 15, 9, 15)), line(seg(2.5, 20, 7, 20)),
           line(seg(15.5, 5, 21.5, 5)), line(seg(17.5, 10, 21.5, 10)), line(seg(17.5, 15, 21.5, 15)), line(seg(15.5, 20, 21.5, 20)),
           line(seg(10, 17.5, 13.5, 9)), dot(12.7, 5.7, 1.0)]
    return out


@icon("linter", CAT, "A lint roller rolling over lines of code.",
      tags=["lint", "lint roller", "code quality", "static analysis", "eslint", "clean up"])
def _(S):
    return [shell(rect(2.5, 3, 15, 6.5, min(S.R, 3))),
            line(poly([(17.5, 6.2), (21, 6.2), (21, 12.5), (10, 12.5), (10, 15)], r=S.r)),
            line(seg(8.5, 15, 11.5, 15)), line(seg(3, 20, 8, 20)), line(seg(11, 20, 21, 20))]


@icon("refactor", CAT, "Code angle brackets inside a circular arrow.",
      tags=["restructure", "rewrite", "clean code", "rework", "code improvement", "cycle"])
def _(S):
    return arc_arrow(S, 12, 12, 9.5, 195, 330, 3.0) + arc_arrow(S, 12, 12, 9.5, 15, 150, 3.0) + [
        chev_l(S, 7.5, 12, 3.2, 2.6), chev_r(S, 16.5, 12, 3.2, 2.6)]


@icon("minify", CAT, "A code page squeezed from both sides by inward arrows.",
      tags=["minification", "compress code", "uglify", "reduce size", "squeeze", "shrink"])
def _(S):
    return [shell(rect(8, 3, 8, 18, min(S.R, 2))), detail(seg(10.5, 8, 13.5, 8)), detail(seg(10.5, 12, 13.5, 12)),
            detail(seg(10.5, 16, 13.5, 16)),
            line(seg(2, 12, 4.5, 12)), head(S, 5.5, 12, 0, 2.6), line(seg(22, 12, 19.5, 12)), head(S, 18.5, 12, 180, 2.6)]


@icon("compiler", CAT, "A gear turning source into binary ones and zeros.",
      tags=["compile", "build", "binary", "machine code", "source to binary", "gcc"])
def _(S):
    return [shell(gear_d(S, 8, 12, 6.2, 4.8, 8)), detail(circle(8, 12, 1.7)),
            line(poly([(17.5, 5.5), (19, 4), (19, 10)], r=0)), line(ellipse(19, 17.5, 1.6, 2.6))]


@icon("code-interpreter", CAT, "Code angle brackets with a speech bubble beside them.",
      tags=["interpreter", "run code", "execute", "script", "python", "runtime"])
def _(S):
    return [line(poly([(5.5, 7.5), (2.5, 12), (5.5, 16.5)], r=S.r)), line(poly([(8, 7.5), (11, 12), (8, 16.5)], r=S.r)),
            shell(poly([(13.5, 5), (21.5, 5), (21.5, 13), (18.5, 13), (16, 16.5), (16, 13), (13.5, 13)], closed=True, r=S.r))]


@icon("transpiler", CAT, "Two code pages with a swap arrow between them.",
      tags=["transpile", "source to source", "babel", "convert language", "translate code", "swap"])
def _(S):
    return [shell(rect(2.5, 5, 6, 14, min(S.R, 2))), shell(rect(15.5, 5, 6, 14, min(S.R, 2))),
            detail(seg(4.5, 10, 6.5, 10)), detail(seg(17.5, 14, 19.5, 14)),
            line(seg(10.5, 9.5, 13, 9.5)), head(S, 13.8, 9.5, 0, 2.4), line(seg(13.5, 14.5, 11, 14.5)), head(S, 10.2, 14.5, 180, 2.4)]


@icon("bundler", CAT, "Several small files tied together with a band into one bundle.",
      tags=["bundle", "webpack", "package files", "build output", "tie together", "assets"])
def _(S):
    R = _pick(S, 0, 1)
    return [shell(rect(2.5, 4, 4.5, 16, R)), shell(rect(9.75, 4, 4.5, 16, R)), shell(rect(17, 4, 4.5, 16, R)),
            detail(seg(1.5, 12, 22.5, 12))]


@icon("dependency-tree", CAT, "A box at the top linked down to two boxes, with one more box below.",
      tags=["dependencies", "package tree", "imports graph", "requires", "hierarchy", "npm ls"])
def _(S):
    R = _pick(S, 0, 1)
    return [shell(rect(8.5, 3, 7, 3, R)), shell(rect(2.5, 11, 7, 3, R)), shell(rect(14.5, 11, 7, 3, R)), shell(rect(2.5, 19, 7, 3, R)),
            line(seg(12, 7, 12, 8.5)), line(poly([(6, 10), (6, 8.5), (18, 8.5), (18, 10)], r=0)),
            line(seg(6, 15, 6, 18))]


@icon("plugin-socket", CAT, "A puzzle piece with two pins plugged into a wall socket.",
      tags=["plugin", "addon", "extension", "socket", "plug in", "integration"])
def _(S):
    return [shell("M2.5 9.5h2.7a1.9 1.9 0 1 1 3.8 0h2.5v9h-9z"),
            line(seg(12, 12, 14.5, 12)), line(seg(12, 16, 14.5, 16)),
            shell(rect(14.5, 5, 7, 14, min(S.R, 2.5))), detail(seg(18, 9, 18, 15))]


@icon("hot-reload", CAT, "A flame beside a circular refresh arrow.",
      tags=["hot reload", "live reload", "hmr", "refresh", "dev server", "fast refresh"])
def _(S):
    flame = "M8 4.5C8.5 7 13 8.5 13 14a5 5 0 0 1-10 0c0-2.5 1.5-4 2.5-5 .3 1.5 1 2.2 2 2.4C7.2 9 7 6.5 8 4.5z"
    return [shell(flame), detail("M8 20.5a1.8 1.8 0 0 1-1.8-1.8c0-1.3 1.8-2.2 1.8-3.8 0 1.6 1.8 2.5 1.8 3.8A1.8 1.8 0 0 1 8 20.5z"),
            line(arc(17, 14, 3.8, 40, 330)), head(S, *polar(17, 14, 3.8, 330), 330 + 90, 2.8)]


@icon("repl-prompt", CAT, "A window holding three chevrons and a text cursor.",
      tags=["repl", "interactive shell", "prompt", ">>>", "console", "read eval print loop"])
def _(S):
    return [shell(rect(2.5, 4, 19, 16, S.R)),
            detail(poly([(5.5, 10), (7.3, 12), (5.5, 14)], r=0)), detail(poly([(9, 10), (10.8, 12), (9, 14)], r=0)),
            detail(poly([(12.5, 10), (14.3, 12), (12.5, 14)], r=0)), detail(seg(17.5, 10.5, 17.5, 14.5))]


@icon("notebook-cell", CAT, "A page with two stacked cells, each with a small play button on its left.",
      tags=["jupyter", "notebook", "code cell", "run cell", "cell", "data science"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, S.R)),
            detail(rect(10, 5.5, 8, 4.5, min(S.R, 1.5))), detail(rect(10, 14, 8, 4.5, min(S.R, 1.5))),
            solid("M5 5.8L8 7.7L5 9.6Z"), solid("M5 14.3L8 16.2L5 18.1Z")]


@icon("inspect-element", CAT, "A cursor arrow clicking on a dashed selection box holding angle brackets.",
      tags=["inspect", "devtools", "dom", "element picker", "select element", "browser tools"])
def _(S):
    return [line(poly([(2.5, 7), (2.5, 2.5), (7, 2.5)], r=0)), line(poly([(11, 2.5), (15.5, 2.5), (15.5, 7)], r=0)),
            line(poly([(2.5, 11), (2.5, 15.5), (7, 15.5)], r=0)),
            chev_l(S, 5.5, 9, 2.2, 1.8), chev_r(S, 12.5, 9, 2.2, 1.8),
            shell(poly([(12.5, 10.5), (12.5, 20.5), (15.2, 17.8), (17.3, 21.3), (19, 20.3), (17, 16.8), (20.5, 16.8)], closed=True, r=S.r * 0.3))]


@icon("watch-expression", CAT, "An eye above code angle brackets.",
      tags=["watch", "debugger", "monitor variable", "expression", "observe value", "inspect"])
def _(S):
    eye = ellipse(12, 7, 9.5, 4.6) if S.name == "rounded" else "M2.5 7Q12 -2 21.5 7Q12 16 2.5 7Z"
    return [line(eye), shell(circle(12, 7, 1.9)),
            line(poly([(8, 14.5), (4, 18), (8, 21.5)], r=S.r)), line(poly([(16, 14.5), (20, 18), (16, 21.5)], r=S.r))]


@icon("profiler", CAT, "A stopwatch with code angle brackets on its face.",
      tags=["profiling", "performance", "benchmark", "timing", "cpu profile", "stopwatch"])
def _(S):
    out = [shell(circle(12, 13.5, 8.5)), line(seg(10, 2.5, 14, 2.5)), line(seg(12, 2.5, 12, 5))]
    out += [chev_l(S, 8.6, 13.5, 3, 2.3, detail), chev_r(S, 15.4, 13.5, 3, 2.3, detail)]
    out.append(line(seg(19.2, 6, 20.7, 4.5)) if S.name == "line" else line(seg(19, 5.8, 20.4, 4.4)))
    return out


@icon("performance-trace", CAT, "A timeline of bars of varied length with a small stopwatch.",
      tags=["trace", "flame graph", "timeline", "waterfall trace", "devtools performance", "spans"])
def _(S):
    return [line(seg(2.5, 4.5, 14, 4.5)), line(seg(6, 9.5, 20, 9.5)), line(seg(3, 14.5, 8.5, 14.5)), line(seg(3, 19.5, 11, 19.5)),
            shell(circle(18, 17, 3.8)), line(seg(18, 17, 18, 15.2)), line(seg(18, 17, 19.8, 17))]


# =========================================================================== chunk 5: people and practice

from dsl import P, U  # noqa: E402
from geometry import path_to_d  # noqa: E402


def merged(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def flame_d(x, y, k=1.0):
    """Small flame, tip at (x, y), about 6k wide and 8k tall."""
    return (f"M{fmt(x)} {fmt(y)}C{fmt(x + 0.5 * k)} {fmt(y + 2.5 * k)} {fmt(x + 3.2 * k)} {fmt(y + 3.8 * k)} {fmt(x + 3.2 * k)} {fmt(y + 6 * k)}"
            f"a{fmt(3.2 * k)} {fmt(3.2 * k)} 0 0 1 {fmt(-6.4 * k)} 0c0-1.6 {fmt(0.8 * k)}-2.6 {fmt(1.6 * k)}-3.4c.2 1 .7 1.4 {fmt(1.2 * k)} 1.5"
            f"C{fmt(x - 1.8 * k)} {fmt(y + 3.5 * k)} {fmt(x - 0.5 * k)} {fmt(y + 1.6 * k)} {fmt(x)} {fmt(y)}z")


@icon("rubber-duck-debugging", CAT, "A rubber duck sitting below a small bug.",
      tags=["rubber duck", "duck", "debugging", "explain code", "bug", "problem solving"])
def _(S):
    body = merged(ellipse(10.5, 16.8, 7.3, 4.3), circle(6.5, 10, 3.4),
                  poly([(3.6, 11.3), (9.4, 11.3), (11, 15.6), (4.5, 15.6)], closed=True),
                  poly([(16, 16.2), (19.2, 13.5), (18.6, 18.5)], closed=True))
    return [shell(body), solid("M4 9.2L1.4 10.2L4 11.4Z"), dot(6, 9.3, 0.95),
            shell(ellipse(19, 7.5, 2, 2.8)), line(seg(18, 4.6, 17, 3)), line(seg(20, 4.6, 21, 3))]


@icon("technical-debt", CAT, "Code angle brackets chained to a heavy ball.",
      tags=["tech debt", "legacy code", "burden", "ball and chain", "shortcuts", "maintenance"])
def _(S):
    return [line(poly([(8, 3), (4, 6.5), (8, 10)], r=S.r)), line(poly([(16, 3), (20, 6.5), (16, 10)], r=S.r)),
            dot(12, 7, 1.1), dot(12, 10.3, 1.1), dot(12, 13.6, 1.1), solid(circle(12, 18.8, 3.8))]


@icon("code-smell", CAT, "Code angle brackets with wavy stink lines rising above.",
      tags=["smell", "bad code", "anti-pattern", "technical smell", "stink", "refactor needed"])
def _(S):
    out = []
    for x in (6.5, 12, 17.5):
        out.append(line(f"M{fmt(x)} 2.5q2 2.1 0 4.2t0 4.2"))
    out += [line(poly([(8.5, 14.5), (4, 18), (8.5, 21.5)], r=S.r)), line(poly([(15.5, 14.5), (20, 18), (15.5, 21.5)], r=S.r)),
            line(seg(13.2, 14.5, 10.8, 21.5))]
    return out


@icon("pair-programming", CAT, "Two heads side by side above one shared laptop.",
      tags=["pairing", "mob programming", "collaboration", "two developers", "driver navigator", "teamwork"])
def _(S):
    return [shell(circle(6, 5, 2.6)), shell(circle(18, 5, 2.6)),
            shell(rect(4.5, 11.5, 15, 7, min(S.R, 2))), line(seg(2, 21.5, 22, 21.5))]


@icon("hackathon", CAT, "A laptop whose screen shows a flame.",
      tags=["hack day", "coding marathon", "game jam", "competition", "sprint event", "build fast"])
def _(S):
    return [shell(rect(2.5, 3.5, 19, 12.5, min(S.R, 2.5))), line(seg(1.5, 20, 22.5, 20)),
            detail(flame_d(12, 5.4, 0.88))]


@icon("code-contributor", CAT, "A person head and shoulders with a small commit dot badge.",
      tags=["contributor", "developer", "author", "open source", "committer", "maintainer"])
def _(S):
    return [shell(circle(9, 7, 3.4)), line("M2.5 20v-1a6.5 5 0 0 1 11 -3.5"),
            line(seg(14, 18.5, 15.5, 18.5)), shell(circle(18.5, 18.5, 2.6)), line(seg(21, 18.5, 22, 18.5))]


@icon("feature-request", CAT, "A speech bubble holding a lightbulb and a plus sign.",
      tags=["feature", "suggestion", "idea", "enhancement", "request", "wish"])
def _(S):
    return [shell(poly([(2.5, 3.5), (21.5, 3.5), (21.5, 17), (13, 17), (9, 21.5), (9, 17), (2.5, 17)], closed=True, r=S.r)),
            detail(circle(8, 9.2, 2.2)), detail(seg(6.9, 13, 9.1, 13)),
            detail(seg(15.5, 7, 15.5, 12.5)), detail(seg(12.8, 9.7, 18.2, 9.7))]


@icon("user-story", CAT, "An index card with a person head and three text lines.",
      tags=["story", "requirements", "agile card", "persona", "acceptance criteria", "backlog item"])
def _(S):
    return [shell(rect(2.5, 4, 19, 16, S.R)), detail(circle(8, 10, 1.9)), detail("M4.8 17c0-2 1.4-3 3.2-3s3.2 1 3.2 3"),
            detail(seg(13.5, 8.5, 18.5, 8.5)), detail(seg(13.5, 12, 18.5, 12)), detail(seg(13.5, 15.5, 17, 15.5))]


@icon("story-points", CAT, "A planning poker card with a large number five.",
      tags=["estimation", "planning poker", "points", "agile", "effort", "sizing"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 19, S.R)),
            detail("M14.8 7H10l-.6 4.2c.7-.5 1.5-.8 2.5-.8 1.8 0 2.9 1.2 2.9 2.9 0 1.9-1.3 3.1-3.3 3.1-1 0-1.8-.3-2.4-.8")]


@icon("burndown-chart", CAT, "A line graph falling from the top left to the bottom right with a flame at the start.",
      tags=["burn down", "sprint chart", "remaining work", "agile", "progress", "scrum"])
def _(S):
    return [line(poly([(2.5, 2.5), (2.5, 21.5), (21.5, 21.5)], r=S.r)),
            line(poly([(7, 12), (11, 14), (14, 17), (20, 18.5)], r=S.r)),
            shell(flame_d(7.5, 4.2, 0.55))]


@icon("velocity-chart", CAT, "Bars rising to a tall last bar with speed lines trailing it.",
      tags=["velocity", "sprint velocity", "throughput", "agile metrics", "speed", "bar chart"])
def _(S):
    return [line(seg(4, 22, 4, 16)), line(seg(10, 22, 10, 13)), line(seg(16.5, 22, 16.5, 8.5)), line(seg(21, 22, 21, 3)),
            line(seg(6, 4.5, 17, 4.5)), line(seg(3.5, 9, 10.5, 9))]


@icon("waterfall-methodology", CAT, "A staircase of bars cascading down and to the right, one phase after another.",
      tags=["waterfall", "sequential phases", "project management", "sdlc", "stages", "cascade"])
def _(S):
    out = []
    for i in range(5):
        x = 2.5 + 3.3 * i
        y = 3.5 + 4.5 * i
        out.append(line(seg(x, y, x + 5.5, y)))
    return out
