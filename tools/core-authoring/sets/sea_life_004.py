"""TypeIcon Core: sea life (batch sea_life_004).

Baleen, a sectioned nautilus, a giant clam and two beach warning signs.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401

CAT = "sea-life"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def mark(d):
    """Small solid mark: solid in stroke styles, knocked out of a Filled body."""
    return Part("dot", d)


@icon("baleen-plates", CAT, "Side view of a whale head with its mouth open and a comb of baleen plates hanging from the upper jaw",
      tags=["baleen", "whale", "filter feeder", "humpback", "mouth", "krill", "marine mammal"])
def _(S):
    r = L(S, 0, 1.5)
    head = poly([(3, 12.5), (3, 9), (6, 5), (12, 3.5), (18, 5), (21, 9), (21, 12.5)], closed=True, r=r) if r else \
        "M3 12.5C3 6 7 3.5 12 3.5C17 3.5 21 6 21 12.5Z"
    plates = [line(seg(x, 12.5, x, 17)) for x in (6.5, 10, 13.5)]
    jaw = line("M3 19C8 22 16 22 21 19")
    return [shell(head), dot(17.5, 8, 1.1), *plates[:3], jaw]


@icon("nautilus-shell-section", CAT, "Spiral shell cut in half showing curved chambers that grow larger toward the opening",
      tags=["nautilus", "cross section", "chambers", "spiral", "shell", "mollusc", "cutaway"])
def _(S):
    cx, cy = 12.5, 12
    pts = []
    n = 40
    for i in range(n + 1):
        t = i / n
        th = math.radians(-60 + 520 * t)
        rr = 1.2 + 6.6 * t
        pts.append((cx + rr * math.cos(th), cy + rr * math.sin(th)))
    d = "M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in pts)
    parts = [shell(circle(cx, cy, 9)), detail(d)]
    for deg in (20, 110, 200):
        a = math.radians(deg)
        parts.append(detail(seg(cx + 5.2 * math.cos(a), cy + 5.2 * math.sin(a), cx + 8 * math.cos(a), cy + 8 * math.sin(a))))
    return parts


@icon("giant-clam", CAT, "Big clam lying open with wavy zigzag shell lips and a soft mantle between them",
      tags=["clam", "bivalve", "shell", "reef", "mollusc", "tridacna", "open shell"])
def _(S):
    r = L(S, 0, 1)
    top = poly([(3, 9), (3, 6), (7, 3.5), (12, 3), (17, 3.5), (21, 6), (21, 9), (18.5, 7.5), (16, 9), (13.5, 7.5), (11, 9),
                (8.5, 7.5), (6, 9)], closed=True, r=r)
    bot = poly([(3, 15), (6, 16.5), (8.5, 15), (11, 16.5), (13.5, 15), (16, 16.5), (18.5, 15), (21, 15), (21, 18), (17, 20.5),
                (12, 21), (7, 20.5), (3, 18)], closed=True, r=r)
    return [shell(top), shell(bot), detail("M7 12C9 10.5 10 13.5 12 12C14 10.5 15 13.5 17 12")]


def _sign(S, inner):
    r = L(S, 0, 2)
    tri = poly([(12, 2), (22, 18), (2, 18)], closed=True, r=r)
    return [shell(tri), line(seg(12, 18, 12, 22)), *inner]


@icon("shark-warning-sign", CAT, "Triangular beach warning sign on a post showing a shark fin above a wave",
      tags=["shark", "beach", "warning", "danger", "swimming", "sign", "fin", "safety"])
def _(S):
    return _sign(S, [mark("M8.5 14C10.5 13 11.2 10.5 10.8 7.5C13.5 9 15.5 11.5 16 14Z"), detail("M7 16C8.5 14.8 9.5 17 11 16C12.5 15 13.5 17 15 16C16 15.5 16.5 15.5 17 15.8")])


@icon("jellyfish-warning-sign", CAT, "Triangular beach warning sign on a post showing a jellyfish",
      tags=["jellyfish", "sting", "beach", "warning", "danger", "swimming", "sign", "safety"])
def _(S):
    return _sign(S, [mark("M8.5 11.5A3.5 3.5 0 0 1 15.5 11.5Z"), detail("M9.5 12.5C8.5 13.5 10.5 14.5 9.5 16"),
                     detail("M12 12.5L12 16"), detail("M14.5 12.5C15.5 13.5 13.5 14.5 14.5 16")])
