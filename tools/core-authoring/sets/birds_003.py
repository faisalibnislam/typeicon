"""TypeIcon Core: birds (batch 003).

Birdwatching gear and bird-related signs, drawn from the objects themselves.
"""
from dsl import Part, circle, detail, ellipse, icon, line, poly, rect, seg, shell  # noqa: F401
from geometry import P, ST, U, path_to_d

CAT = "birds"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def thick(d, w, S):
    """Outline of a stroke of width w along d."""
    return path_to_d(ST(d, w, S.cap, S.join))


def mark(d):
    """Solid silhouette: solid in Line and Rounded, knocked out of a Filled body."""
    return Part("dot", d)


# ============================================================================ gear

@icon("spotting-scope", CAT, "Birding spotting scope with an eyepiece angled upward, mounted on a small tripod",
      tags=["scope", "birdwatching", "birding", "telescope", "optics", "tripod", "zoom"])
def _(S):
    k = min(S.R, 1.5)
    tube = rect(7.5, 6.5, 11, 5, min(k, 1))
    hood = rect(17, 5, 4.5, 8, k)
    eye = poly([(11, 8.1), (5.6, 2.7), (2.7, 5.6), (8.1, 11)], closed=True, r=S.r * 0.4)
    legs = poly([(6.5, 21), (12.5, 14.5), (18.5, 21)], r=S.r)
    return [shell(union(tube, hood, eye)), detail(seg(17, 6.5, 17, 11.5)), line(seg(12.5, 12, 12.5, 21)), line(legs)]


# ============================================================================ signs

@icon("duck-crossing", CAT, "Triangular warning road sign showing a mother duck walking with a duckling",
      tags=["road sign", "warning", "ducks", "ducklings", "wildlife crossing", "caution"])
def _(S):
    sign = poly([(12, 2.5), (22, 20.5), (2, 20.5)], closed=True, r=S.r * 1.3)
    r = L(S, 0, 0.4)
    mother = union(ellipse(11.6, 16.2, 3.2, 1.9),
                   poly([(13.4, 15), (15.3, 13.6), (14.8, 16.2)], closed=True, r=r),
                   thick("M10.5 15.2L11.1 12.4", 2.2, S),
                   circle(11.4, 11.6, 1.6),
                   poly([(10.4, 11.1), (8.9, 12.1), (10.5, 12.6)], closed=True, r=r))
    chick = union(ellipse(17.3, 17.9, 1.3, 0.95), circle(16.6, 16.6, 0.95))
    return [shell(sign), mark(mother), mark(chick)]
