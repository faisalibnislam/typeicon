"""TypeIcon Core: computer hardware, 3D printing and fabrication (batch 003)."""
from dsl import Part, circle, detail, dot, icon, line, poly, rect, seg, shell, solid  # noqa: F401

CAT = "hardware-pc"


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


@icon("resin-3d-printer", CAT, "Boxy printer with a build plate lifting a small printed object out of a shallow vat",
      tags=["sla printer", "msla", "resin", "3d printing", "additive manufacturing", "vat", "build plate"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 4))),
        detail(seg(7, 8, 17, 8)),
        Part("dot", rect(9.5, 11, 5, 3, 1 if S.name == "rounded" else 0)),
        detail(seg(7, 17, 17, 17)),
    ]


@icon("filament-spool", CAT, "Round spool of wound filament with one loose strand trailing off the side",
      tags=["3d printer filament", "pla", "abs", "reel", "wire", "plastic", "roll"])
def _(S):
    hub = Part("dot", rect(10, 10, 4, 4, 0)) if S.name == "line" else dot(12, 12, 2)
    return [
        shell(circle(11, 11, 8.5)),
        detail(circle(11, 11, 4.5)),
        hub,
        line("M17 17c1.5 2.5 2.5 3.5 5 3.5"),
    ]


@icon("3d-printer-nozzle", CAT, "Heater block with a cone-shaped nozzle laying plastic onto stacked layers below",
      tags=["hotend", "extruder", "3d printing", "fdm", "print head", "heater block", "layers"])
def _(S):
    return [
        shell(rect(6, 2, 12, 5, rr(S, 2))),
        shell(poly([(8, 7), (16, 7), (13, 11), (11, 11)], closed=True, r=S.r * 0.3)),
        line(seg(6, 15, 18, 15)),
        line(seg(4, 19.5, 20, 19.5)),
    ]


@icon("laser-engraver", CAT, "Open gantry frame with a laser head firing a short beam onto a board with a burned mark",
      tags=["laser cutter", "engraving", "etching", "cnc", "fabrication", "maker", "wood burning", "diode laser"])
def _(S):
    return [
        line(poly([(3, 21), (3, 3), (21, 3), (21, 21)], r=S.r)),
        shell(rect(9, 5, 6, 5, rr(S, 1.5))),
        line(seg(12, 10, 12, 13.5)),
        shell(rect(7, 16, 10, 5, rr(S, 1.5))),
    ]
