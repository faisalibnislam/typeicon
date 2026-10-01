"""TypeIcon Core: development & code."""
from dsl import arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from dsl import ROUNDED, filled_region
from geometry import fmt

CAT = "development"


def _pick(S, sharp, soft):
    return sharp if S.name == "line" else soft


def _bend(S, pts, soft=4.0):
    """Connector polyline: sharp corners in Line, generous curves in Rounded."""
    return poly(pts, r=_pick(S, 0, soft))


def _node(x, y, r=2.5):
    return shell(circle(x, y, r))


# =========================================================================== code and terminals

@icon("code", CAT, "Angle brackets around a slash; source code",
      tags=["code", "programming", "developer", "html", "markup", "embed"], aliases=["code-brackets"])
def _(S):
    return [line(poly([(8, 6), (4, 12), (8, 18)], r=S.r)),
            line(poly([(16, 6), (20, 12), (16, 18)], r=S.r)),
            line(seg(13.75, 4.5, 10.25, 19.5))]


@icon("terminal", CAT, "Terminal window with a prompt and cursor",
      tags=["shell", "console", "bash", "prompt", "cli", "window"], aliases=["shell"])
def _(S):
    return [shell(rect(2.5, 4, 19, 16, S.R)),
            detail(poly([(6.5, 8.5), (9.5, 11.5), (6.5, 14.5)], r=S.r)),
            detail(seg(11.5, 14.5, 16, 14.5))]


@icon("command-line", CAT, "Command prompt: a chevron and an underscore cursor",
      tags=["cli", "prompt", "shell", "command", "input", "terminal"], aliases=["prompt"])
def _(S):
    return [line(poly([(4.5, 5.5), (11, 12), (4.5, 18.5)], r=S.r)),
            line(seg(13, 18.5, 20, 18.5))]


def _bug(S, cx=12.0, top=10.5, bottom=21.0, half=5.5, head=3.25):
    rx = _pick(S, 3.5, half)
    return [
        shell(rect(cx - half, top, 2 * half, bottom - top, rx)),
        shell(f"M{fmt(cx - head)} {fmt(top - 3.5)}A{head} {head} 0 0 1 {fmt(cx + head)} {fmt(top - 3.5)}Z"),
        detail(seg(cx, top, cx, bottom)),
        line(seg(cx - half, top + 3, cx - half - 3, top + 1.5)), line(seg(cx + half, top + 3, cx + half + 3, top + 1.5)),
        line(seg(cx - half, top + 6.5, cx - half - 3.5, top + 6.5)), line(seg(cx + half, top + 6.5, cx + half + 3.5, top + 6.5)),
        line(seg(cx - half + 0.5, top + 9.5, cx - half - 2.5, top + 11)), line(seg(cx + half - 0.5, top + 9.5, cx + half + 2.5, top + 11)),
    ]


@icon("bug", CAT, "A beetle; a software bug or defect",
      tags=["bug", "defect", "error", "issue", "insect", "beetle"], aliases=["defect"])
def _(S):
    return _bug(S)


# =========================================================================== version control

@icon("git-branch", CAT, "Version-control branch splitting off a main line",
      tags=["git", "branch", "version control", "vcs", "source"])
def _(S):
    return [_node(6, 5.5), _node(6, 18.5), _node(18, 5.5),
            line(seg(6, 8, 6, 16)),
            line(_bend(S, [(18, 8), (18, 13), (6, 13)], 4.5))]


@icon("git-commit", CAT, "A commit: a node on a horizontal line",
      tags=["git", "commit", "version control", "node", "history"], aliases=["commit"])
def _(S):
    return [line(seg(2.5, 12, 7, 12)), _node(12, 12, 4), line(seg(17, 12, 21.5, 12))]


@icon("git-merge", CAT, "Merge: a side branch joining back into the main line",
      tags=["git", "merge", "version control", "join", "combine"], )
def _(S):
    return [_node(6, 5.5), _node(6, 18.5), _node(18, 14),
            line(seg(6, 8, 6, 16)),
            line(_bend(S, [(6, 8), (6, 14), (15.5, 14)], 6) if S.name == "rounded" else poly([(6, 9), (11, 14), (15.5, 14)]))]


@icon("git-pull-request", CAT, "Pull request: a branch with an arrow pointing back to the main line",
      tags=["git", "pull request", "pr", "merge request", "review", "version control"], aliases=["pull-request", "merge-request"])
def _(S):
    return [_node(5.5, 5.5), _node(5.5, 18.5), _node(18.5, 18.5),
            line(seg(5.5, 8, 5.5, 16)),
            line(_bend(S, [(18.5, 16), (18.5, 5.5), (12.5, 5.5)], 4)),
            line(poly([(15, 3), (12.5, 5.5), (15, 8)], r=S.r * 0.5))]


@icon("git-compare", CAT, "Compare: two branches with arrows crossing between them",
      tags=["git", "compare", "diff", "version control", "swap"])
def _(S):
    return [_node(5.5, 5.5), _node(18.5, 18.5),
            line(_bend(S, [(5.5, 8), (5.5, 18.5), (11.5, 18.5)], 4)),
            line(poly([(9, 16), (11.5, 18.5), (9, 21)], r=S.r * 0.5)),
            line(_bend(S, [(18.5, 16), (18.5, 5.5), (12.5, 5.5)], 4)),
            line(poly([(15, 3), (12.5, 5.5), (15, 8)], r=S.r * 0.5))]


@icon("git-fork", CAT, "Fork: one line splitting into two branches",
      tags=["git", "fork", "copy", "version control", "split"], aliases=["fork-repo"])
def _(S):
    return [_node(6, 5.5), _node(18, 5.5), _node(12, 18.5),
            line(_bend(S, [(6, 8), (6, 12), (18, 12), (18, 8)], 3)),
            line(seg(12, 12, 12, 16))]


# =========================================================================== interfaces

@icon("api", CAT, "The letters API; an application programming interface",
      tags=["api", "interface", "endpoint", "integration", "rest", "sdk"])
def _(S):
    return [line(poly([(2.5, 17), (5.75, 7), (9, 17)], r=S.r * 0.5)), line(seg(3.8, 13.5, 7.7, 13.5)),
            line(poly([(11.5, 17), (11.5, 7), (13.5, 7)], r=S.r * 0.5)), line("M13.5 7A3 3 0 0 1 13.5 13H11.5"),
            line(seg(20.5, 7, 20.5, 17))]


@icon("webhook", CAT, "A hook hanging from a node, ending in an arrow; an event callback",
      tags=["webhook", "callback", "event", "hook", "integration", "trigger"])
def _(S):
    return [_node(16, 5.5),
            line("M16 8V14.5A5 5 0 0 1 6 14.5V13"),
            line(poly([(3.5, 14.5), (6, 12), (8.5, 14.5)], r=S.r * 0.5))]


@icon("braces", CAT, "Curly braces; a code block or object",
      tags=["curly brackets", "code", "object", "json", "block", "programming"], aliases=["curly-braces"])
def _(S):
    if S.name == "line":
        left = poly([(9, 3.5), (6.5, 3.5), (6.5, 10), (4, 12), (6.5, 14), (6.5, 20.5), (9, 20.5)])
        right = poly([(15, 3.5), (17.5, 3.5), (17.5, 10), (20, 12), (17.5, 14), (17.5, 20.5), (15, 20.5)])
    else:
        left = "M9 3.5H8.5C7.4 3.5 6.5 4.4 6.5 5.5V9.5C6.5 10.9 5.4 12 4 12C5.4 12 6.5 13.1 6.5 14.5V18.5C6.5 19.6 7.4 20.5 8.5 20.5H9"
        right = "M15 3.5H15.5C16.6 3.5 17.5 4.4 17.5 5.5V9.5C17.5 10.9 18.6 12 20 12C18.6 12 17.5 13.1 17.5 14.5V18.5C17.5 19.6 16.6 20.5 15.5 20.5H15"
    return [line(left), line(right)]


def _parens(S):
    return [line("M6.5 3.5C4.5 6 3.5 9 3.5 12C3.5 15 4.5 18 6.5 20.5"),
            line("M17.5 3.5C19.5 6 20.5 9 20.5 12C20.5 15 19.5 18 17.5 20.5")]


@icon("function", CAT, "A function sign between parentheses",
      tags=["function", "method", "procedure", "code", "programming"], aliases=["func"])
def _(S):
    return [*_parens(S),
            line("M15.5 5.5C15.1 4.3 14.3 3.7 13.2 3.7C11.9 3.7 11.1 4.5 10.9 5.9L9.4 18.5C9.2 19.7 8.6 20.3 7.8 20.3" if S.name == "rounded"
                 else "M15.5 3.7H13C11.9 3.7 11.1 4.5 10.9 5.9L9.4 20.3"),
            line(seg(8.5, 9.5, 14.5, 9.5))]


@icon("variable", CAT, "The letter x between parentheses; a variable",
      tags=["variable", "value", "parameter", "code", "programming", "x"])
def _(S):
    return [*_parens(S), line(seg(8.5, 8.5, 15.5, 15.5)), line(seg(15.5, 8.5, 8.5, 15.5))]


def _one(S, x, y, h=7):
    return line(poly([(x - 2, y + 1.5), (x, y), (x, y + h)], r=S.r * 0.5))


def _zero(S, x, y, h=7, w=4.5):
    return line(rect(x - w / 2, y, w, h, _pick(S, 1, w / 2)))


@icon("binary", CAT, "Binary digits one and zero",
      tags=["binary", "bits", "digits", "ones and zeros", "data", "code"], aliases=["bits"])
def _(S):
    return [_one(S, 7.5, 3.5), _zero(S, 16.5, 3.5), _zero(S, 7, 13.5), _one(S, 17, 13.5)]


@icon("regex", CAT, "Regular expression: an asterisk and a dot",
      tags=["regular expression", "pattern", "match", "wildcard", "search"], aliases=["regular-expression"])
def _(S):
    centre = (15.5, 8.5)
    arms = [line(seg(*pt_on(*centre, 4.75, a), *pt_on(*centre, 4.75, a + 180))) for a in (90, 30, 150)]
    mark = solid(rect(4, 15, 5, 5)) if S.name == "line" else dot(6.5, 17.5, 2.6)
    return [*arms, mark]


# =========================================================================== data and structure

@icon("database-table", CAT, "Data table with a header row and columns",
      tags=["table", "database", "rows", "columns", "sql", "records"], aliases=["db-table"])
def _(S):
    return [shell(rect(3, 4, 18, 16, S.R)),
            detail(seg(3, 9.5, 21, 9.5)), detail(seg(9.5, 9.5, 9.5, 20)), detail(seg(3, 14.75, 21, 14.75))]


@icon("schema", CAT, "Two linked tables; a database schema or entity diagram",
      tags=["schema", "entity", "relationship", "erd", "diagram", "database"], aliases=["erd"])
def _(S):
    rr = min(S.R, 2)
    return [shell(rect(12.5, 3, 8.5, 7.5, rr)), shell(rect(3, 13.5, 8.5, 7.5, rr)),
            line(_bend(S, [(12.5, 6.75), (7.25, 6.75), (7.25, 13.5)], 3))]


@icon("sitemap", CAT, "A page tree: one box linked to three below it",
      tags=["sitemap", "hierarchy", "tree", "structure", "pages", "organization"], aliases=["site-map"])
def _(S):
    rr = min(S.R, 1.5)
    return [shell(rect(8.5, 3, 7, 5.5, rr)),
            line(seg(12, 8.5, 12, 17)),
            line(_bend(S, [(4.5, 17), (4.5, 12.75), (19.5, 12.75), (19.5, 17)], 2)),
            shell(rect(2.5, 17, 4, 4, min(rr, 1))), shell(rect(10, 17, 4, 4, min(rr, 1))), shell(rect(17.5, 17, 4, 4, min(rr, 1)))]


# =========================================================================== infrastructure

_CLOUD_LINE = "M4.5 19H19.5A3.8 3.8 0 0 0 18 11.7A6 6 0 0 0 6.5 10A4.7 4.7 0 0 0 4.5 19Z"
_CLOUD_ROUND = "M7 19H17.5A4.5 4.5 0 0 0 18 10.03A6 6 0 0 0 6.34 9.1A5 5 0 0 0 7 19Z"


@icon("cloud-code", CAT, "Cloud with code brackets; cloud development or serverless code",
      tags=["cloud", "serverless", "code", "hosting", "deploy", "functions"])
def _(S):
    return [shell(_pick(S, _CLOUD_LINE, _CLOUD_ROUND)),
            detail(poly([(10, 11.5), (8, 13.75), (10, 16)], r=S.r * 0.5)),
            detail(poly([(14, 11.5), (16, 13.75), (14, 16)], r=S.r * 0.5))]


@icon("server-stack", CAT, "Three stacked server units with status lights",
      tags=["server", "rack", "hosting", "backend", "infrastructure", "data center"], aliases=["servers"])
def _(S):
    return [shell(rect(4, 3, 16, 18, S.R)),
            detail(seg(4, 9, 20, 9)), detail(seg(4, 15, 20, 15)),
            dot(7.75, 6, 1.25), dot(7.75, 12, 1.25), dot(7.75, 18, 1.25)]


@icon("container", CAT, "Ribbed shipping container; a software container",
      tags=["container", "docker", "image", "shipping", "devops", "runtime"])
def _(S):
    return [shell(rect(2.5, 6, 19, 12, min(S.R, 2.5))),
            detail(seg(7, 9, 7, 15)), detail(seg(12, 9, 12, 15)), detail(seg(17, 9, 17, 15))]


_HEX = [(12, 3), (19.79, 7.5), (19.79, 16.5), (12, 21), (4.21, 16.5), (4.21, 7.5)]


@icon("cube", CAT, "Isometric cube; a 3D object or module",
      tags=["cube", "3d", "box", "object", "module", "block"], aliases=["box-3d"])
def _(S):
    return [shell(poly(_HEX, closed=True, r=S.r)),
            detail(poly([(4.21, 7.5), (12, 12), (19.79, 7.5)], r=S.r * 0.5)), detail(seg(12, 12, 12, 21))]


@icon("package", CAT, "Taped cardboard box in 3D; a software package or bundle",
      tags=["package", "bundle", "module", "library", "dependency", "npm"], aliases=["bundle"])
def _(S):
    return [shell(poly(_HEX, closed=True, r=S.r)),
            detail(poly([(4.21, 7.5), (12, 12), (19.79, 7.5)], r=S.r * 0.5)), detail(seg(12, 12, 12, 21)),
            detail(poly([(8.1, 5.25), (15.9, 9.75), (15.9, 13.5)], r=S.r * 0.5))]


@icon("puzzle", CAT, "Square made of interlocking puzzle pieces; a plugin or extension",
      tags=["plugin", "extension", "add-on", "integration", "module", "jigsaw"], aliases=["plugin", "extension"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)),
            detail("M12 3V4.5A2.5 2.5 0 0 1 12 9.5V21"),
            detail("M3 12H4.5A2.5 2.5 0 0 0 9.5 12H21")]


def _rot_pts(pts, deg, cx=12.0, cy=12.0):
    import math
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


@icon("plug-connected", CAT, "Plug pushed into a socket; connected",
      tags=["connected", "plug", "connection", "integration", "online", "socket"])
def _(S):
    R = lambda pts: _rot_pts(pts, -45)  # noqa: E731
    rr = _pick(S, 0.5, 2.5)
    plug = poly(R([(2, -4), (8, -4), (8, 4), (2, 4)]), closed=True, r=rr)
    cup = poly(R([(-2, -5), (-8.5, -5), (-8.5, 5), (-2, 5)]), r=_pick(S, 0, 2.5))
    return [shell(plug), line(cup),
            line(seg(*R([(2, -2)])[0], *R([(-4.5, -2)])[0])),
            line(seg(*R([(2, 2)])[0], *R([(-4.5, 2)])[0])),
            line(seg(*R([(8, 0)])[0], *R([(12, 0)])[0])),
            line(seg(*R([(-8.5, 0)])[0], *R([(-12, 0)])[0]))]


@icon("api-key", CAT, "Key above code brackets; an API key or secret",
      tags=["api key", "secret", "credential", "token", "access", "auth"], aliases=["secret-key"])
def _(S):
    return [shell(circle(6.5, 7.5, 3.5)),
            line(poly([(10, 7.5), (20.5, 7.5), (20.5, 11)], r=S.r * 0.5)), line(seg(17, 7.5, 17, 10.5)),
            line(poly([(8, 14), (4.5, 17.25), (8, 20.5)], r=S.r * 0.5)),
            line(poly([(11.5, 14), (15, 17.25), (11.5, 20.5)], r=S.r * 0.5))]


@icon("token", CAT, "Coin with a hexagon; an access or crypto token",
      tags=["token", "coin", "auth token", "jwt", "crypto", "credit"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(poly(regular(12, 12, 4.5, 6), closed=True, r=S.r * 0.5))]


def _circle_hits(c1, r1, c2, r2):
    import math
    (x1, y1), (x2, y2) = c1, c2
    d = math.hypot(x2 - x1, y2 - y1)
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(r1 * r1 - a * a)
    mx, my = x1 + a * (x2 - x1) / d, y1 + a * (y2 - y1) / d
    return (mx + h * (y2 - y1) / d, my - h * (x2 - x1) / d), (mx - h * (y2 - y1) / d, my + h * (x2 - x1) / d)


def _bitten(cx, cy, r, bx, by, br):
    q, p = _circle_hits((cx, cy), r, (bx, by), br)
    return (f"M{fmt(p[0])} {fmt(p[1])}A{r} {r} 0 1 1 {fmt(q[0])} {fmt(q[1])}"
            f"A{br} {br} 0 0 0 {fmt(p[0])} {fmt(p[1])}Z")


def _cookie(S):
    body = _bitten(12, 12, 9, 19.5, 4.5, 4.5)
    chips = [(8, 8.5), (13, 13), (7.5, 15), (12.5, 18)]
    if S.name == "line":
        marks = [solid(rect(x - 1.25, y - 1.25, 2.5, 2.5)) for x, y in chips]
    else:
        marks = [dot(x, y, 1.4) for x, y in chips]
    return [shell(body), *marks]


icon("cookie", CAT, "Bitten cookie with chips; a browser cookie",
     tags=["cookie", "browser", "tracking", "consent", "session", "web"],
     filled=lambda: filled_region(_cookie(ROUNDED)))(_cookie)


_SHIELD = "M12 2.5L20 5.5V11C20 16 16.6 19.8 12 21.5C7.4 19.8 4 16 4 11V5.5Z"
_SHIELD_ROUND = ("M10.95 2.9L5.05 5.1Q4 5.5 4 6.6V11C4 16 7.4 19.8 12 21.5C16.6 19.8 20 16 20 11V6.6"
                 "Q20 5.5 18.95 5.1L13.05 2.9Q12 2.5 10.95 2.9Z")


@icon("shield-code", CAT, "Shield with code brackets; secure code",
      tags=["secure code", "security", "code", "protection", "appsec", "safe"])
def _(S):
    return [shell(_pick(S, _SHIELD, _SHIELD_ROUND)),
            detail(poly([(10, 8.5), (7.5, 11.25), (10, 14)], r=S.r * 0.5)),
            detail(poly([(14, 8.5), (16.5, 11.25), (14, 14)], r=S.r * 0.5))]


@icon("branch-tree", CAT, "Tree of branches with nodes; a branching structure",
      tags=["tree", "branches", "hierarchy", "nodes", "structure", "outline"])
def _(S):
    return [_node(5.5, 18.5), _node(18, 5.5), _node(18, 12),
            line(_bend(S, [(5.5, 16), (5.5, 5.5), (15.5, 5.5)], 3)),
            line(seg(5.5, 12, 15.5, 12))]


# =========================================================================== delivery

@icon("deploy", CAT, "Arrow going down into a server; deploy to a machine",
      tags=["deploy", "ship", "release", "server", "publish", "ci/cd"], aliases=["deployment"])
def _(S):
    return [line(seg(12, 3, 12, 10.5)), line(poly([(8.5, 7.5), (12, 11), (15.5, 7.5)], r=S.r * 0.5)),
            shell(rect(3, 14, 18, 7, min(S.R, 2.5))), dot(6.75, 17.5, 1.25), dot(10.25, 17.5, 1.25)]


@icon("pipeline", CAT, "Three stages linked in sequence; a build or CI pipeline",
      tags=["pipeline", "ci", "cd", "workflow", "stages", "build"], aliases=["ci-pipeline"])
def _(S):
    rr = min(S.R, 2)
    return [shell(rect(3, 3, 8, 5.5, rr)), shell(rect(13, 9.25, 8, 5.5, rr)), shell(rect(3, 15.5, 8, 5.5, rr)),
            line(_bend(S, [(11, 5.75), (17, 5.75), (17, 9.25)], 2.5)),
            line(_bend(S, [(17, 14.75), (17, 18.25), (11, 18.25)], 2.5))]


@icon("test-tube-code", CAT, "Test tube beside code brackets; code testing",
      tags=["testing", "unit test", "experiment", "lab", "qa", "code"])
def _(S):
    return [line(seg(3, 3.5, 11, 3.5)),
            shell("M4.5 3.5V17.5A2.5 2.5 0 0 0 9.5 17.5V3.5Z"),
            detail(seg(4.5, 11.5, 9.5, 11.5)),
            line(poly([(15.5, 4), (12.5, 7.5), (15.5, 11)], r=S.r * 0.5)),
            line(poly([(18, 4), (21, 7.5), (18, 11)], r=S.r * 0.5))]


@icon("debug", CAT, "Bug beside a play button; run and debug",
      tags=["debug", "debugger", "bug", "run", "troubleshoot", "fix"], aliases=["debugger"])
def _(S):
    return [*_bug(S, cx=9, top=11, bottom=21, half=4.5, head=2.75),
            shell(poly([(15, 2.5), (21.5, 6.5), (15, 10.5)], closed=True, r=S.r * 0.5))]


@icon("breakpoint", CAT, "Breakpoint tag marking a line of code",
      tags=["breakpoint", "debug", "pause", "marker", "line", "stop"])
def _(S):
    return [shell(poly([(3, 8.5), (10.5, 8.5), (14, 12), (10.5, 15.5), (3, 15.5)], closed=True, r=S.r * 0.5)),
            line(seg(16.5, 12, 21, 12)),
            line(seg(3, 4.5, 21, 4.5)), line(seg(3, 19.5, 16, 19.5))]


@icon("console", CAT, "Window with a title bar and a command prompt; a developer console",
      tags=["console", "devtools", "log", "output", "prompt", "window"], aliases=["dev-console"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(seg(3, 8.5, 21, 8.5)),
            dot(6.5, 5.75, 1), dot(9.5, 5.75, 1),
            detail(poly([(7, 11.5), (9.5, 14), (7, 16.5)], r=S.r * 0.5)), detail(seg(12, 16.5, 16.5, 16.5))]


_PAGE = [(5, 2.5), (14, 2.5), (19, 7.5), (19, 21.5), (5, 21.5)]


@icon("log-file", CAT, "Page of log entries, each with a bullet",
      tags=["log", "logs", "file", "entries", "audit", "output"], aliases=["logs"])
def _(S):
    rows = (11, 14.75, 18.5)
    return [shell(poly(_PAGE, closed=True, r=S.r)), detail(poly([(14, 2.5), (14, 7.5), (19, 7.5)], r=S.r * 0.5)),
            *[dot(8.5, y, 1.1) for y in rows],
            *[detail(seg(11, y, 15.5, y)) for y in rows]]


@icon("source-code", CAT, "Code block: a window holding angle brackets and a slash",
      tags=["source", "code", "program", "script", "snippet", "editor"])
def _(S):
    return [shell(rect(2.5, 4, 19, 16, S.R)),
            detail(poly([(8.5, 8.5), (6, 12), (8.5, 15.5)], r=S.r * 0.5)),
            detail(poly([(15.5, 8.5), (18, 12), (15.5, 15.5)], r=S.r * 0.5)),
            detail(seg(13, 8, 11, 16))]


@icon("repository", CAT, "Book with code brackets on its cover; a code repository",
      tags=["repository", "repo", "project", "source", "codebase", "git"], aliases=["repo"])
def _(S):
    return [shell(rect(4, 3, 16, 18, min(S.R, 3))), detail(seg(8, 3, 8, 21)),
            detail(poly([(13, 8.5), (11, 11), (13, 13.5)], r=S.r * 0.5)),
            detail(poly([(16, 8.5), (18, 11), (16, 13.5)], r=S.r * 0.5))]


# =========================================================================== releases and changes

@icon("tag-version", CAT, "Label tag marked with a v; a version tag",
      tags=["version", "tag", "release", "semver", "label", "git tag"], aliases=["version-tag"])
def _(S):
    return [shell(poly([(2.5, 12), (7.5, 6), (21, 6), (21, 18), (7.5, 18)], closed=True, r=S.r)),
            dot(8, 12, 1.25),
            detail(poly([(12, 9.5), (14.5, 14.5), (17, 9.5)], r=S.r * 0.5))]


@icon("release", CAT, "Open box with an arrow rising out of it; a new release",
      tags=["release", "publish", "ship", "launch", "version", "package"])
def _(S):
    return [shell(rect(4.5, 12.5, 15, 8.5, min(S.R, 2.5))),
            line(seg(4.5, 12.5, 2.5, 9)), line(seg(19.5, 12.5, 21.5, 9)),
            line(seg(12, 3.5, 12, 10)), line(poly([(8.75, 6.75), (12, 3.5), (15.25, 6.75)], r=S.r * 0.5))]


@icon("diff", CAT, "Page with a plus and a minus; a diff of changes",
      tags=["diff", "changes", "compare", "patch", "additions", "deletions"])
def _(S):
    return [shell(rect(4.5, 3, 15, 18, S.R)),
            detail(seg(12, 6.5, 12, 12.5)), detail(seg(9, 9.5, 15, 9.5)), detail(seg(9, 16.5, 15, 16.5))]


@icon("merge-conflict", CAT, "Two branches colliding in a node marked with a cross",
      tags=["merge conflict", "conflict", "git", "clash", "version control", "error"])
def _(S):
    if S.name == "line":
        legs = [line(poly([(5.5, 8), (5.5, 10), (9.2, 13.4)])), line(poly([(18.5, 8), (18.5, 10), (14.8, 13.4)]))]
    else:
        legs = [line("M5.5 8V9.5C5.5 11 6.5 12 9 13.3"), line("M18.5 8V9.5C18.5 11 17.5 12 15 13.3")]
    return [_node(5.5, 5.5), _node(18.5, 5.5), shell(circle(12, 16.5, 4.5)), *legs,
            detail(seg(10.5, 15, 13.5, 18)), detail(seg(13.5, 15, 10.5, 18))]


def _wrench_d(S):
    from dsl import D as _D, P as _P, U as _U
    from geometry import path_to_d
    a = -45
    R = lambda pts: _rot_pts(pts, a, 10.5, 13.5)  # noqa: E731
    handle = poly(R([(-9, -1.75), (3, -1.75), (3, 1.75), (-9, 1.75)]), closed=True)
    import math
    head_c = R([(5.5, 0)])[0]
    jaw = poly(R([(5.5, -1.6), (11, -1.6), (11, 1.6), (5.5, 1.6)]), closed=True)
    region = _D(_U(_P(handle), _P(circle(head_c[0], head_c[1], 4.25))), _P(jaw))
    return path_to_d(region)


@icon("hotfix", CAT, "Wrench with a lightning bolt; an urgent fix",
      tags=["hotfix", "patch", "fix", "urgent", "repair", "quick fix"], aliases=["quick-fix"])
def _(S):
    return [shell(_wrench_d(S), stroke_miterlimit="2"),
            shell(poly([(8.5, 2.5), (3.5, 8.5), (6.5, 8.5), (5.5, 12.5), (10, 6.5), (7, 6.5)], closed=True, r=S.r * 0.2),
                  stroke_miterlimit="2")]


# =========================================================================== computer science

@icon("algorithm", CAT, "Flowchart: a decision diamond branching into two steps",
      tags=["algorithm", "flowchart", "logic", "decision", "process", "steps"], aliases=["flowchart"])
def _(S):
    rr = min(S.R, 1.5)
    return [shell(poly([(12, 2.5), (16.5, 7), (12, 11.5), (7.5, 7)], closed=True, r=S.r * 0.5)),
            line(_bend(S, [(7.5, 7), (5.25, 7), (5.25, 15.5)], 2)),
            line(_bend(S, [(16.5, 7), (18.75, 7), (18.75, 15.5)], 2)),
            shell(rect(2.5, 15.5, 5.5, 5.5, rr)), shell(rect(16, 15.5, 5.5, 5.5, rr))]


def _nodes(S, pts, r=1.75):
    if S.name == "line":
        return [solid(rect(x - r, y - r, 2 * r, 2 * r)) for x, y in pts]
    return [dot(x, y, r) for x, y in pts]


_TREE = {"root": (12, 4), "l": (6.25, 11.5), "r": (17.75, 11.5), "ll": (3.5, 19.5), "lr": (9, 19.5)}


@icon("data-structure", CAT, "Binary tree of connected nodes; a data structure",
      tags=["data structure", "tree", "binary tree", "nodes", "hierarchy", "computer science"], aliases=["binary-tree"])
def _(S):
    t = _TREE
    edges = [("root", "l"), ("root", "r"), ("l", "ll"), ("l", "lr")]
    return [*_nodes(S, t.values(), 2), *[line(seg(*t[a], *t[b])) for a, b in edges]]


@icon("queue", CAT, "Row of cells with an arrow showing first-in, first-out order",
      tags=["queue", "fifo", "buffer", "line", "jobs", "messages"], aliases=["fifo"])
def _(S):
    return [shell(rect(3, 4, 18, 8, min(S.R, 2))), detail(seg(9, 4, 9, 12)), detail(seg(15, 4, 15, 12)),
            line(seg(3.5, 17.5, 19.5, 17.5)), line(poly([(16.5, 14.5), (19.5, 17.5), (16.5, 20.5)], r=S.r * 0.5))]


@icon("stack-data", CAT, "Items stacked in an open container; a last-in, first-out stack",
      tags=["stack", "lifo", "push", "pop", "data structure", "layers"], aliases=["lifo"])
def _(S):
    return [line(poly([(4, 4), (4, 20.5), (20, 20.5), (20, 4)], r=S.r)),
            line(seg(8, 8.5, 16, 8.5)), line(seg(8, 12.5, 16, 12.5)), line(seg(8, 16.5, 16, 16.5))]


def _edge(a, ra, b, rb):
    import math
    (x1, y1), (x2, y2) = a, b
    d = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    return seg(x1 + ux * ra, y1 + uy * ra, x2 - ux * rb, y2 - uy * rb)


def _gnode(S, x, y, r=2.5):
    if S.name == "line":
        return shell(rect(x - r, y - r, 2 * r, 2 * r))
    return shell(circle(x, y, r))


_GRAPH = {"a": (5.5, 5.5), "b": (18.5, 7), "c": (6.5, 18.5), "d": (15.5, 15.5)}


@icon("graph-nodes", CAT, "Nodes joined by edges; a graph or network of relations",
      tags=["graph", "nodes", "edges", "network", "relations", "connections"], aliases=["node-graph"])
def _(S):
    g = _GRAPH
    edges = [("a", "b"), ("a", "c"), ("a", "d"), ("b", "d"), ("c", "d")]
    return [*[_gnode(S, *g[k]) for k in g], *[line(_edge(g[a], 3.5, g[b], 3.5)) for a, b in edges]]


@icon("network-topology", CAT, "Central hub linked to four devices; a network topology",
      tags=["network", "topology", "hub", "star", "lan", "infrastructure"], aliases=["topology"])
def _(S):
    corners = [(5.5, 5.5), (18.5, 5.5), (5.5, 18.5), (18.5, 18.5)]
    hub = [(10, 10), (14, 10), (10, 14), (14, 14)]
    return [shell(rect(9.5, 9.5, 5, 5, _pick(S, 0.5, 2))), *[_node(x, y) for x, y in corners],
            *[line(seg(h[0] + (-0.5 if h[0] < 12 else 0.5), h[1] + (-0.5 if h[1] < 12 else 0.5),
                       c[0] + (1.8 if c[0] < 12 else -1.8), c[1] + (1.8 if c[1] < 12 else -1.8))) for h, c in zip(hub, corners)]]
