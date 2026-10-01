"""Convert a sanitized SVG into a font-ready outline (skia-pathops Path in font units).

Pipeline per painted element:
  shape -> path data -> compose transforms (element CTM x viewBox->font matrix with y flip)
  fill   : path in font space, fill-rule honoured (evenodd -> winding)
  stroke : stroked *after* transforming to font units (Skia stroker tolerance is absolute,
           so stroking at 1200 UPM keeps curve error far below a pixel). Width is scaled by
           the transform's uniform scale; non-uniform scale/skew under a stroke is refused.
  clip   : clip-path=url(#id) regions are intersected.
All regions are unioned (overlap removal) and orientation is fixed later per output format
(TrueType clockwise, CFF counter-clockwise). Holes are preserved by winding.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field

from fontTools.misc.transform import Transform
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path
from pathops import FillType, LineCap, LineJoin, Path, PathOp, op

from .svg_sanitize import SVG_NS, SvgRejected, _local, parse_view_box, safe_parse

UPM = 1200
ASCENT = 1050
DESCENT = 150  # positive magnitude

_CAPS = {"butt": LineCap.BUTT_CAP, "round": LineCap.ROUND_CAP, "square": LineCap.SQUARE_CAP}
_JOINS = {"miter": LineJoin.MITER_JOIN, "round": LineJoin.ROUND_JOIN, "bevel": LineJoin.BEVEL_JOIN,
          "miter-clip": LineJoin.MITER_JOIN, "arcs": LineJoin.ROUND_JOIN}

INHERITED = ("fill", "fill-rule", "stroke", "stroke-width", "stroke-linecap", "stroke-linejoin",
             "stroke-miterlimit", "stroke-dasharray", "stroke-dashoffset", "visibility", "clip-rule")
DEFAULTS = {"fill": "black", "fill-rule": "nonzero", "stroke": "none", "stroke-width": "1",
            "stroke-linecap": "butt", "stroke-linejoin": "miter", "stroke-miterlimit": "4",
            "stroke-dasharray": "none", "stroke-dashoffset": "0", "visibility": "visible",
            "clip-rule": "nonzero"}


class OutlineError(ValueError):
    pass


@dataclass
class Outline:
    path: Path
    advance: int
    view_box: tuple[float, float, float, float]
    warnings: list[str] = field(default_factory=list)

    @property
    def bounds(self):
        return self.path.bounds


# --------------------------------------------------------------------------- parsing helpers

_NUM = re.compile(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")


def _f(v, default=0.0) -> float:
    if v is None:
        return default
    m = _NUM.match(str(v).strip())
    if not m:
        return default
    return float(m.group(0))


def parse_transform(s: str | None) -> Transform:
    t = Transform()
    if not s:
        return t
    for name, args in re.findall(r"(matrix|translate|scale|rotate|skewX|skewY)\s*\(([^)]*)\)", s):
        a = [float(x) for x in _NUM.findall(args)]
        if name == "matrix" and len(a) == 6:
            m = Transform(*a)
        elif name == "translate":
            m = Transform().translate(a[0], a[1] if len(a) > 1 else 0)
        elif name == "scale":
            m = Transform().scale(a[0], a[1] if len(a) > 1 else a[0])
        elif name == "rotate":
            ang = math.radians(a[0])
            if len(a) == 3:
                m = Transform().translate(a[1], a[2]).rotate(ang).translate(-a[1], -a[2])
            else:
                m = Transform().rotate(ang)
        elif name == "skewX":
            m = Transform().skew(math.radians(a[0]), 0)
        elif name == "skewY":
            m = Transform().skew(0, math.radians(a[0]))
        else:
            raise OutlineError(f"bad transform {name}({args})")
        t = t.transform(m)
    return t


def _points(s: str) -> list[float]:
    return [float(x) for x in _NUM.findall(s or "")]


def shape_to_d(el) -> str | None:
    name = _local(el.tag)
    if name == "path":
        return el.get("d") or None
    if name == "rect":
        x, y, w, h = (_f(el.get(k)) for k in ("x", "y", "width", "height"))
        if w <= 0 or h <= 0:
            return None
        rx, ry = el.get("rx"), el.get("ry")
        rxf = _f(rx if rx is not None else ry)
        ryf = _f(ry if ry is not None else rx)
        rxf, ryf = min(rxf, w / 2), min(ryf, h / 2)
        if rxf <= 0 or ryf <= 0:
            return f"M{x} {y}H{x + w}V{y + h}H{x}Z"
        a = f"A{rxf} {ryf} 0 0 1 "
        return (f"M{x + rxf} {y}H{x + w - rxf}{a}{x + w} {y + ryf}V{y + h - ryf}{a}{x + w - rxf} {y + h}"
                f"H{x + rxf}{a}{x} {y + h - ryf}V{y + ryf}{a}{x + rxf} {y}Z")
    if name in ("circle", "ellipse"):
        cx, cy = _f(el.get("cx")), _f(el.get("cy"))
        if name == "circle":
            rx = ry = _f(el.get("r"))
        else:
            rx, ry = _f(el.get("rx")), _f(el.get("ry"))
        if rx <= 0 or ry <= 0:
            return None
        return (f"M{cx - rx} {cy}A{rx} {ry} 0 1 0 {cx + rx} {cy}A{rx} {ry} 0 1 0 {cx - rx} {cy}Z")
    if name == "line":
        x1, y1, x2, y2 = (_f(el.get(k)) for k in ("x1", "y1", "x2", "y2"))
        return f"M{x1} {y1}L{x2} {y2}"
    if name in ("polyline", "polygon"):
        pts = _points(el.get("points"))
        if len(pts) < 4:
            return None
        d = f"M{pts[0]} {pts[1]}" + "".join(f"L{pts[i]} {pts[i + 1]}" for i in range(2, len(pts) - 1, 2))
        return d + ("Z" if name == "polygon" else "")
    return None


def _path_from_d(d: str, matrix: Transform, fill_rule: str = "nonzero") -> Path:
    p = Path()
    parse_path(d, TransformPen(p.getPen(), tuple(matrix)))
    if fill_rule == "evenodd":
        p.fillType = FillType.EVEN_ODD
    return p


def _uniform_scale(m: Transform) -> float | None:
    a, b, c, d = m.xx, m.xy, m.yx, m.yy
    sx, sy = math.hypot(a, b), math.hypot(c, d)
    if sx == 0 or abs(sx - sy) > 1e-6 * max(sx, sy) or abs(a * c + b * d) > 1e-6 * sx * sy:
        return None
    return sx


_NUDGES = [(0.05, 0.0), (0.0, 0.05), (-0.05, 0.0), (0.0, -0.05), (0.05, 0.05)]  # font units: invisible


def _union(a: Path | None, b: Path) -> Path:
    """Union that checks Skia's answer. Skia can return a wrong union (and a wrong intersection) without raising
    when edges coincide exactly, e.g. a solid band flush with a stroked frame. Each attempt must satisfy
    |a ∪ b| = |a| + |b| - |a ∩ b| and be no smaller than either input; otherwise b is retried moved by 1/20 of a
    font unit, and an error is raised rather than shipping a glyph with parts missing."""
    if a is None:
        out = Path(b)
        out.simplify(fix_winding=True)
        return out
    for dx, dy in [(0.0, 0.0), *_NUDGES]:
        bb = b
        if dx or dy:
            bb = Path()
            b.draw(TransformPen(bb.getPen(), (1, 0, 0, 1, dx, dy)))
        try:
            out = op(a, bb, PathOp.UNION, fix_winding=True)
            inter = abs(op(a, bb, PathOp.INTERSECTION, fix_winding=True).area)
        except Exception:  # noqa: BLE001 - pathops raises PathOpsError on degenerate input; retry nudged
            continue
        got = abs(out.area)
        if got >= max(abs(a.area), abs(bb.area)) - 2.0 and abs(got - (abs(a.area) + abs(bb.area) - inter)) <= 0.005 * got + 2.0:
            return out
    raise OutlineError("boolean union gave an inconsistent result (coincident edges); adjust the drawing slightly")


# --------------------------------------------------------------------------- main entry

def svg_to_outline(svg: bytes | str, upm: int = UPM, ascent: int = ASCENT, descent: int = DESCENT) -> Outline:
    """Convert (already sanitized) SVG into a single unioned outline in font units, y-up."""
    if isinstance(svg, str):
        svg = svg.encode("utf-8")
    root = safe_parse(svg)
    minx, miny, vw, vh = parse_view_box(root)
    s = upm / vh
    base = Transform(s, 0, 0, -s, -minx * s, ascent + miny * s)
    advance = round(vw * s)
    warnings: list[str] = []
    clip_defs = {el.get("id"): el for el in root.iter() if _local(el.tag) == "clipPath" and el.get("id")}

    def region_of(el, ctm: Transform, style: dict) -> Path | None:
        name = _local(el.tag)
        if style.get("display") == "none" or el.get("display") == "none":
            return None
        if name in ("defs", "clipPath", "title", "desc"):
            return None
        local = dict(style)
        for k in INHERITED:
            if el.get(k) is not None and el.get(k) != "inherit":
                local[k] = el.get(k).strip()
        # Transform.transform(other) maps points through `other` first, then `self`.
        m = ctm.transform(parse_transform(el.get("transform"))) if el.get("transform") else ctm
        for k in ("opacity", "fill-opacity", "stroke-opacity"):
            if el.get(k) is not None and _f(el.get(k), 1.0) == 0:
                return None
        result: Path | None = None
        if name in ("svg", "g"):
            for child in el:
                if isinstance(child.tag, str) and child.tag.startswith("{" + SVG_NS):
                    r = region_of(child, m, local)
                    if r is not None:
                        result = _union(result, r)
        elif name in ("path", "circle", "ellipse", "rect", "line", "polyline", "polygon"):
            if local.get("visibility") in ("hidden", "collapse"):
                return None
            d = shape_to_d(el)
            if not d:
                return None
            fill, stroke = local["fill"].lower(), local["stroke"].lower()
            if fill not in ("none", "transparent") and name != "line":
                fp = _path_from_d(d, m, local.get("fill-rule", "nonzero"))
                fp.simplify(fix_winding=True)
                result = _union(result, fp)
            if stroke not in ("none", "transparent"):
                width = _f(local.get("stroke-width"), 1.0)
                if width > 0:
                    k = _uniform_scale(m)
                    if k is None:
                        raise OutlineError("stroke under non-uniform transform is not supported")
                    sp = _path_from_d(d, m)
                    dash = local.get("stroke-dasharray", "none")
                    dash_arr = None if dash in ("none", "") else [v * k for v in _points(dash)]
                    if dash_arr and sum(dash_arr) <= 0:
                        dash_arr = None
                    cap = _CAPS.get(local.get("stroke-linecap", "butt"), LineCap.BUTT_CAP)
                    join = _JOINS.get(local.get("stroke-linejoin", "miter"), LineJoin.MITER_JOIN)
                    sp.stroke(width * k, cap, join, _f(local.get("stroke-miterlimit"), 4.0),
                              dash_array=dash_arr, dash_offset=_f(local.get("stroke-dashoffset")) * k)
                    sp.convertConicsToQuads()
                    sp.simplify(fix_winding=True)
                    result = _union(result, sp)
        else:
            return None

        cp = el.get("clip-path")
        if cp and result is not None:
            ref = re.match(r"url\(#([-\w.:]+)\)", cp.strip())
            clip_el = clip_defs.get(ref.group(1)) if ref else None
            if clip_el is None:
                raise OutlineError(f"unresolved clip-path {cp}")
            if clip_el.get("clipPathUnits") == "objectBoundingBox":
                raise OutlineError("clipPathUnits=objectBoundingBox is not supported")
            cm = ctm.transform(parse_transform(clip_el.get("transform")))
            clip_region = None
            for child in clip_el:
                if not isinstance(child.tag, str):
                    continue
                cd = shape_to_d(child)
                if cd:
                    cmm = cm.transform(parse_transform(child.get("transform")))
                    rule = child.get("clip-rule") or clip_el.get("clip-rule") or "nonzero"
                    cpth = _path_from_d(cd, cmm, rule)
                    cpth.simplify(fix_winding=True)
                    clip_region = _union(clip_region, cpth)
            if clip_region is None:
                return None
            result = op(result, clip_region, PathOp.INTERSECTION, fix_winding=True)
        return result

    style = dict(DEFAULTS)
    path = region_of(root, base, style)
    if path is None or abs(path.area) < 1e-6:
        raise OutlineError("SVG has no painted area")
    path.simplify(fix_winding=True)
    xmin, ymin, xmax, ymax = path.bounds
    tol = upm * 0.02
    if xmin < -tol or xmax > advance + tol or ymin < -descent - tol or ymax > ascent + tol:
        warnings.append("artwork extends outside the viewBox")
    return Outline(path=path, advance=advance, view_box=(minx, miny, vw, vh), warnings=warnings)


def outline_for_file(path: str) -> Outline:
    with open(path, "rb") as fh:
        return svg_to_outline(fh.read())


__all__ = ["Outline", "OutlineError", "SvgRejected", "svg_to_outline", "UPM", "ASCENT", "DESCENT"]
