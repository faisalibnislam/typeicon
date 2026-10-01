"""Geometry helpers for authoring TypeIcon Core icons on the 24 x 24 grid.

Stroke styles (Line, Rounded) are emitted as editable stroke-based SVG elements.
Filled designs are built with explicit boolean geometry (skia-pathops) and emitted
as a single nonzero path. Boolean work happens at 100x scale so Skia's stroker
tolerance stays far below a pixel, then coordinates are scaled back to the grid.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path
from pathops import LineCap, LineJoin, Path, PathOp, PathOpsError, op

SCALE = 100.0


@dataclass(frozen=True)
class Style:
    name: str
    cap: str  # SVG stroke-linecap
    join: str  # SVG stroke-linejoin
    R: float  # container corner radius
    r: float  # polyline fillet radius
    w: float = 2.0  # stroke width in grid units
    slug: str = ""  # output name when it differs from `name` (Thin draws exactly like Line)


LINE = Style("line", "butt", "miter", R=2.0, r=0.0)
ROUNDED = Style("rounded", "round", "round", R=4.0, r=1.5)
# Thin: Line's geometry (butt caps, miter joins) with half the stroke weight. Designs are drawn once; the
# centre lines are shared with Line, only the painted width changes.
# `name` stays "line" so drawings that branch on S.name use their Line geometry.
THIN = Style("line", "butt", "miter", R=2.0, r=0.0, w=1.0, slug="thin")


def fmt(v: float) -> str:
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def pt(p) -> str:
    return f"{fmt(p[0])} {fmt(p[1])}"


# --------------------------------------------------------------------------- d-strings

def poly_d(points, closed=False, r=0.0) -> str:
    """Polyline/polygon path with circular fillets of radius r at interior corners."""
    pts = [tuple(map(float, p)) for p in points]
    n = len(pts)
    if r <= 0 or n < 3:
        d = "M" + pt(pts[0]) + "".join("L" + pt(p) for p in pts[1:])
        return d + ("Z" if closed else "")

    def corner(i):
        p = pts[i]
        a = pts[i - 1]
        b = pts[(i + 1) % n]
        ux, uy = a[0] - p[0], a[1] - p[1]
        vx, vy = b[0] - p[0], b[1] - p[1]
        la, lb = math.hypot(ux, uy), math.hypot(vx, vy)
        ux, uy, vx, vy = ux / la, uy / la, vx / lb, vy / lb
        cos_t = max(-1.0, min(1.0, ux * vx + uy * vy))
        theta = math.acos(cos_t)
        if theta < 1e-3 or abs(theta - math.pi) < 1e-3:
            return None
        rr = r
        t = rr / math.tan(theta / 2)
        limit = min(la, lb) / 2
        if t > limit:
            t = limit
            rr = t * math.tan(theta / 2)
        t1 = (p[0] + ux * t, p[1] + uy * t)
        t2 = (p[0] + vx * t, p[1] + vy * t)
        cross = ux * vy - uy * vx
        sweep = 0 if cross > 0 else 1
        return t1, t2, rr, sweep

    out = []
    if closed:
        c0 = corner(0)
        start = c0[1] if c0 else pts[0]
        out.append("M" + pt(start))
        for i in list(range(1, n)) + [0]:
            c = corner(i)
            if c:
                t1, t2, rr, sweep = c
                out.append("L" + pt(t1) + f"A{fmt(rr)} {fmt(rr)} 0 0 {sweep} " + pt(t2))
            else:
                out.append("L" + pt(pts[i]))
        out.append("Z")
    else:
        out.append("M" + pt(pts[0]))
        for i in range(1, n - 1):
            c = corner(i)
            if c:
                t1, t2, rr, sweep = c
                out.append("L" + pt(t1) + f"A{fmt(rr)} {fmt(rr)} 0 0 {sweep} " + pt(t2))
            else:
                out.append("L" + pt(pts[i]))
        out.append("L" + pt(pts[-1]))
    return "".join(out)


def circle_d(cx, cy, r) -> str:
    return (
        f"M{fmt(cx - r)} {fmt(cy)}A{fmt(r)} {fmt(r)} 0 1 0 {fmt(cx + r)} {fmt(cy)}"
        f"A{fmt(r)} {fmt(r)} 0 1 0 {fmt(cx - r)} {fmt(cy)}Z"
    )


def rect_d(x, y, w, h, rx=0.0) -> str:
    rx = max(0.0, min(rx, w / 2, h / 2))
    if rx == 0:
        return f"M{fmt(x)} {fmt(y)}H{fmt(x + w)}V{fmt(y + h)}H{fmt(x)}Z"
    a = f"A{fmt(rx)} {fmt(rx)} 0 0 1 "
    return (
        f"M{fmt(x + rx)} {fmt(y)}H{fmt(x + w - rx)}{a}{fmt(x + w)} {fmt(y + rx)}"
        f"V{fmt(y + h - rx)}{a}{fmt(x + w - rx)} {fmt(y + h)}H{fmt(x + rx)}"
        f"{a}{fmt(x)} {fmt(y + h - rx)}V{fmt(y + rx)}{a}{fmt(x + rx)} {fmt(y)}Z"
    )


def polar(cx, cy, r, deg):
    a = math.radians(deg)
    return (cx + r * math.cos(a), cy + r * math.sin(a))


def arc_d(cx, cy, r, start_deg, end_deg) -> str:
    """Arc on circle, clockwise on screen (increasing angle, y-down) from start to end."""
    sweep_total = (end_deg - start_deg) % 360 or 360
    p0 = polar(cx, cy, r, start_deg)
    p1 = polar(cx, cy, r, end_deg)
    large = 1 if sweep_total > 180 else 0
    return f"M{pt(p0)}A{fmt(r)} {fmt(r)} 0 {large} 1 {pt(p1)}"


# --------------------------------------------------------------------------- stroke elements

def el_path(d, **attrs) -> str:
    extra = "".join(f' {k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<path d="{d}"{extra}/>'


def el_dot(cx, cy, r) -> str:
    """Solid dot used inside stroke styles (i, ?, !)."""
    return el_path(circle_d(cx, cy, r), fill="currentColor", stroke="none")


# --------------------------------------------------------------------------- filled booleans

_CAP = {"butt": LineCap.BUTT_CAP, "round": LineCap.ROUND_CAP, "square": LineCap.SQUARE_CAP}
_JOIN = {"miter": LineJoin.MITER_JOIN, "round": LineJoin.ROUND_JOIN, "bevel": LineJoin.BEVEL_JOIN}


def P(d: str) -> Path:
    """Filled region from a d-string (scaled)."""
    p = Path()
    parse_path(d, TransformPen(p.getPen(), (SCALE, 0, 0, SCALE, 0, 0)))
    p.simplify(fix_winding=True)
    return p


def ST(d: str, w: float = 2.0, cap: str = "butt", join: str = "miter", miter: float = 4.0) -> Path:
    """Stroke outline region of a d-string (scaled)."""
    p = Path()
    parse_path(d, TransformPen(p.getPen(), (SCALE, 0, 0, SCALE, 0, 0)))
    p.stroke(w * SCALE, _CAP[cap], _JOIN[join], miter)
    p.convertConicsToQuads()
    p.simplify(fix_winding=True)
    return p


_NUDGES = [(0.001, 0.0), (0.0, 0.001), (-0.001, 0.0), (0.0, -0.001), (0.001, 0.001)]  # grid units: invisible


def _consistent_union(a: Path, b: Path, out: Path) -> bool:
    """|a ∪ b| = |a| + |b| - |a ∩ b|, and a union is never smaller than an input. Skia can get a union (and
    the matching intersection) wrong without raising when edges coincide exactly."""
    try:
        inter = abs(op(a, b, PathOp.INTERSECTION, fix_winding=True).area)
    except PathOpsError:
        return False
    got = abs(out.area)
    return got >= max(abs(a.area), abs(b.area)) - 2.0 and abs(got - (abs(a.area) + abs(b.area) - inter)) <= 0.005 * got + 2.0


def _op(a: Path, b: Path, kind) -> Path:
    """Skia boolean op that tolerates exactly coincident edges (e.g. a solid header flush with a stroked frame):
    if Skia rejects the pair or returns an inconsistent union, retry with b moved by a thousandth of a pixel."""
    for dx, dy in [(0.0, 0.0), *_NUDGES]:
        bb = b
        if dx or dy:
            bb = Path()
            b.draw(TransformPen(bb.getPen(), (1, 0, 0, 1, dx * SCALE, dy * SCALE)))
        try:
            out = op(a, bb, kind, fix_winding=True)
        except PathOpsError:
            continue
        if kind != PathOp.UNION or _consistent_union(a, bb, out):
            return out
    raise PathOpsError(f"{kind} failed or gave an inconsistent result even after nudging")


def U(*paths: Path) -> Path:
    out = paths[0]
    for p in paths[1:]:
        out = _op(out, p, PathOp.UNION)
    return out


def D(a: Path, *bs: Path) -> Path:
    out = a
    for b in bs:
        out = _op(out, b, PathOp.DIFFERENCE)
    return out


def I(a: Path, b: Path) -> Path:  # noqa: E743
    return _op(a, b, PathOp.INTERSECTION)


def transform_path(p: Path, matrix) -> Path:
    """Apply an affine (a, b, c, d, e, f) given in grid units to a scaled path."""
    a, b, c, d, e, f = matrix
    out = Path()
    p.draw(TransformPen(out.getPen(), (a, b, c, d, e * SCALE, f * SCALE)))
    out.simplify(fix_winding=True)
    return out


def path_to_d(p: Path) -> str:
    p = Path(p)
    p.simplify(fix_winding=True, clockwise=False)
    pen = SVGPathPen(None, ntos=fmt)
    p.draw(TransformPen(pen, (1 / SCALE, 0, 0, 1 / SCALE, 0, 0)))
    return pen.getCommands()


def rotation(deg: float, cx: float = 12, cy: float = 12):
    a = math.radians(deg)
    cos_a, sin_a = round(math.cos(a), 12), round(math.sin(a), 12)
    return (cos_a, sin_a, -sin_a, cos_a, cx - cos_a * cx + sin_a * cy, cy - sin_a * cx - cos_a * cy)
