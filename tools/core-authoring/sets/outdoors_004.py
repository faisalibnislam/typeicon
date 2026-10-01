"""TypeIcon Core: outdoors, batch 004 (camp and fishing gear)."""
from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, seg, shell, solid  # noqa: F401

CAT = "outdoors"


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


@icon("waterproof-case", CAT, "Hard-shell case with a carry handle and two front latches",
      tags=["dry case", "hard case", "protective case", "gear case", "dry box", "camping", "kayak"])
def _(S):
    return [
        line(poly([(9, 8), (9, 5), (15, 5), (15, 8)], r=S.r)),
        shell(rect(3, 8, 18, 12, S.R)),
        detail(seg(3, 12, 21, 12)),
        sq(6, 10.5, 3, 3.5, 0.5 if S.name == "rounded" else 0),
        sq(15, 10.5, 3, 3.5, 0.5 if S.name == "rounded" else 0),
    ]


@icon("rod-holder", CAT, "Stake with a forked rest holding a fishing rod at an angle",
      tags=["rod rest", "fishing", "fishing rod", "bank stick", "angler", "riverbank", "tackle"])
def _(S):
    return [
        line(poly([(5.5, 8), (8, 13.5), (10.5, 8)], r=S.r)),
        line(seg(8, 13.5, 8, 20)),
        line(seg(3, 20.5, 13, 20.5)),
        line(seg(3, 15.3, 21, 4)),
        line(seg(20.5, 4.5, 20.5, 10)),
    ]


@icon("ice-shanty", CAT, "Small gabled hut on skids with a round hole in the ice beside it",
      tags=["ice fishing", "fishing hut", "ice hut", "winter", "frozen lake", "shelter", "fishing shack"])
def _(S):
    return [
        shell(poly([(2.5, 16.5), (2.5, 9.5), (6.75, 5.5), (11, 9.5), (11, 16.5)], closed=True, r=S.r)),
        detail(poly([(5.5, 16.5), (5.5, 12.5), (8, 12.5), (8, 16.5)], r=S.r * 0.5)),
        line(poly([(2, 20.5), (12, 20.5), (13.5, 19)], r=S.r)),
        shell(ellipse(18.5, 19.5, 3.5, 2.2)),
    ]


@icon("log-bench", CAT, "Bench made from a split log resting on two tree stumps",
      tags=["park bench", "rustic bench", "campsite", "seat", "timber", "stump", "picnic"])
def _(S):
    return [
        shell(rect(2, 5.5, 20, 6.5, min(S.R, 3))),
        detail(seg(6, 8.75, 10, 8.75)),
        shell(rect(4, 14, 5, 7, min(S.R, 1.5))),
        shell(rect(15, 14, 5, 7, min(S.R, 1.5))),
    ]


@icon("hammock-stand", CAT, "Curved freestanding frame with a hammock slung between its raised ends",
      tags=["hammock", "garden", "relax", "backyard", "camping", "frame", "swing bed"])
def _(S):
    end = (lambda x: dot(x, 7, 1.5)) if S.name == "rounded" else (lambda x: sq(x - 1.25, 5.75, 2.5, 2.5))
    return [
        line("M3 7C3 18 8 20.5 12 20.5C16 20.5 21 18 21 7"),
        line("M3 7Q12 15 21 7"),
        end(3),
        end(21),
    ]
