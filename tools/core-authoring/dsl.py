"""Part-based design language for TypeIcon Core icons (24 x 24 grid, 2 px stroke).

An icon is a list of parts. The designer chooses each part's role, and the three styles follow
the Core specification (docs/design/core-grid.md):

  shell(d)    closed outline.  Line/Rounded: 2 px stroke.  Filled: solid to the outer stroke edge.
  detail(d)   inner line.      Line/Rounded: 2 px stroke.  Filled: knocked out of the shells it
                               sits on (2 px counter); outside any shell it becomes a heavy stroke.
  line(d)     open stroke.     Line/Rounded: 2 px stroke.  Filled: 2.5 px stroke (heavier).
  dot(x,y,r)  small disc.      Solid in every style; inside a Filled shell it is knocked out.
  solid(d)    solid region.    Filled in every style (small markers only).

Shapes are built with the style object `S`, so Line and Rounded really differ:
  S.cap / S.join      butt + miter (Line)  vs  round + round (Rounded)
  S.r                 polyline fillet: 0 (Line) vs 1.5 (Rounded); use poly(..., r=S.r)
  S.R                 container radius: 2 (Line) vs 4 (Rounded); use rect(..., S.R)
  S.name              "line" | "rounded" for explicit per-style drawing when needed

Example:
    @icon("t-shirt", "clothing", "T-shirt with short sleeves", tags=["tee", "shirt"], aliases=["tee"])
    def _(S):
        return [shell(poly([(8,3),(3,6),(5,10),(7,9),(7,21),(17,21),(17,9),(19,10),(21,6),(16,3)], closed=True, r=S.r)),
                detail("M8 3a4 4 0 0 0 8 0")]

A per-icon `filled=` function (returning a pathops Path in grid units via geometry.P/ST/U/D) can
override the derived Filled design when the rule does not suit the drawing.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable

from geometry import (  # noqa: F401  (re-exported for icon modules)
    D, I, LINE, P, ROUNDED, SCALE, ST, U, Style, arc_d, circle_d, el_dot, el_path, fmt, path_to_d, polar,
    poly_d, rect_d, rotation, transform_path,
)
from pathops import Path

HEAVY = 2.5  # Filled weight for open strokes
KNOCK = 2.0  # Filled counter width for details


# --------------------------------------------------------------------------- shape helpers (return d-strings)

def poly(points, closed=False, r=0.0) -> str:
    return poly_d(points, closed=closed, r=r)


def rect(x, y, w, h, rx=0.0) -> str:
    return rect_d(x, y, w, h, rx)


def circle(cx, cy, r) -> str:
    return circle_d(cx, cy, r)


def ellipse(cx, cy, rx, ry) -> str:
    return (f"M{fmt(cx - rx)} {fmt(cy)}A{fmt(rx)} {fmt(ry)} 0 1 0 {fmt(cx + rx)} {fmt(cy)}"
            f"A{fmt(rx)} {fmt(ry)} 0 1 0 {fmt(cx - rx)} {fmt(cy)}Z")


def arc(cx, cy, r, start_deg, end_deg) -> str:
    """Arc clockwise on screen from start to end (0° = right, 90° = down)."""
    return arc_d(cx, cy, r, start_deg, end_deg)


def seg(x1, y1, x2, y2) -> str:
    return f"M{fmt(x1)} {fmt(y1)}L{fmt(x2)} {fmt(y2)}"


def pt_on(cx, cy, r, deg):
    return polar(cx, cy, r, deg)


def regular(cx, cy, r, n, start=-90.0):
    """Vertices of a regular polygon (for poly)."""
    return [polar(cx, cy, r, start + i * 360 / n) for i in range(n)]


# --------------------------------------------------------------------------- parts

@dataclass
class Part:
    kind: str  # shell | detail | line | dot | solid
    d: str
    attrs: dict = field(default_factory=dict)


def shell(d: str, **attrs) -> Part:
    return Part("shell", d, attrs)


def detail(d: str, **attrs) -> Part:
    return Part("detail", d, attrs)


def line(d: str, **attrs) -> Part:
    return Part("line", d, attrs)


def dot(x: float, y: float, r: float = 1.25) -> Part:
    return Part("dot", circle_d(x, y, r))


def solid(d: str) -> Part:
    return Part("solid", d)


# --------------------------------------------------------------------------- rendering

def stroke_elements(parts: list[Part]) -> list[str]:
    out = []
    for p in parts:
        if p.kind in ("dot", "solid"):
            out.append(el_path(p.d, fill="currentColor", stroke="none"))
        else:
            out.append(el_path(p.d, **p.attrs))
    return out


def _stroke_region(d: str, w: float, S: Style = LINE, miter: float = 4.0) -> Path:
    return ST(d, w, S.cap, S.join, miter)


def filled_region(parts_line: list[Part]) -> Path:
    """Derive the Filled design from the Line-style parts using the Core rules."""
    shells = [p for p in parts_line if p.kind == "shell"]
    body: Path | None = None
    for p in shells:
        miter = float(p.attrs.get("stroke_miterlimit", 4))
        r = U(P(p.d), _stroke_region(p.d, 2.0, LINE, miter))
        body = r if body is None else U(body, r)
    extras: list[Path] = []
    for p in parts_line:
        if p.kind == "detail":
            region = _stroke_region(p.d, KNOCK)
            if body is not None and abs(I(region, body).area) >= 0.5 * abs(region.area):
                body = D(body, region)
            else:
                extras.append(_stroke_region(p.d, HEAVY))
        elif p.kind == "dot":
            region = P(p.d)
            if body is not None and abs(I(region, body).area) >= 0.5 * abs(region.area):
                body = D(body, region)
            else:
                extras.append(region)
        elif p.kind == "line":
            miter = float(p.attrs.get("stroke_miterlimit", 4))
            extras.append(_stroke_region(p.d, HEAVY, LINE, miter))
        elif p.kind == "solid":
            extras.append(P(p.d))
    items = ([body] if body is not None else []) + extras
    if not items:
        raise ValueError("icon has no parts")
    return U(*items)


# --------------------------------------------------------------------------- registry

@dataclass
class DslIcon:
    name: str
    category: str
    description: str
    tags: list[str]
    aliases: list[str]
    draw: Callable[[Style], list[Part]]
    filled_override: Callable[[], Path] | None = None
    modifiers: str | None = None  # modifier set name for variants (None = category default)
    derived_from: dict | None = None

    def stroke(self, S: Style) -> list[str]:
        return stroke_elements(self.draw(S))

    def filled(self) -> Path:
        if self.filled_override:
            return self.filled_override()
        return filled_region(self.draw(LINE))


REGISTRY: list[DslIcon] = []


def icon(name: str, category: str, description: str, tags=(), aliases=(), filled=None, modifiers: str | None = None):
    def deco(fn):
        REGISTRY.append(DslIcon(name, category, description, list(tags), list(aliases), fn, filled, modifiers))
        return fn
    return deco


def angle_between(a, b) -> float:
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
