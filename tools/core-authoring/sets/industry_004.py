"""TypeIcon Core: industry, batch 004."""
from dsl import arc, circle, detail, dot, icon, line, poly, rect, seg, shell, solid  # noqa: F401

CAT = "industry"


@icon("stacker-crane", CAT, "Tall mast on a floor rail between two storage racks, with a carriage lifting a pallet partway up.",
      tags=["asrs", "warehouse", "automated storage", "rack", "pallet", "lift", "logistics"])
def _(S):
    return [
        line(poly([(2, 4), (6, 4)])), line(poly([(2, 11), (6, 11)])), line(poly([(2, 18), (6, 18)])),
        line(poly([(18, 4), (22, 4)])), line(poly([(18, 11), (22, 11)])), line(poly([(18, 18), (22, 18)])),
        line(seg(3, 4, 3, 18)), line(seg(21, 4, 21, 18)),
        line(seg(2, 21, 22, 21)),
        line(seg(12, 3, 12, 18)),
        shell(rect(8, 9, 8, 4, min(S.R, 1.5))),
    ]
