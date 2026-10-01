"""Safe SVG parsing and allow-list sanitation.

Security properties:
  * No DTDs, entities, network access or external resources (XXE / billion-laughs safe).
  * Bounded input size, element count and nesting depth.
  * Scripts, event handlers, foreignObject, external links, <style> and animation are removed.
  * Paint servers (gradients/patterns), raster images, text, filters, masks and multicolour
    artwork are never silently changed: the asset is routed to SVG-only delivery with a reason.

The sanitized SVG is the "normalized display derivative": strokes are kept (editable),
colours are unified to currentColor, the viewBox and aspect ratio are preserved.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from lxml import etree

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"

MAX_BYTES = 512 * 1024
MAX_ELEMENTS = 4000
MAX_DEPTH = 32

# Elements kept for both display and font conversion.
SHAPES = {"path", "circle", "ellipse", "rect", "line", "polyline", "polygon"}
CONTAINERS = {"svg", "g", "defs", "clipPath"}
KEEP = SHAPES | CONTAINERS
# Elements dropped silently: metadata and dangerous/interactive content.
DROP = {
    "title", "desc", "metadata", "script", "style", "foreignObject", "animate", "animateMotion",
    "animateTransform", "set", "discard", "a", "switch", "cursor", "view",
}
# Elements that cannot be represented as a monochrome font outline -> SVG-only.
SVG_ONLY = {
    "linearGradient": "gradient", "radialGradient": "gradient", "pattern": "pattern",
    "image": "raster image", "text": "text", "tspan": "text", "textPath": "text",
    "filter": "filter", "mask": "mask", "use": "use/symbol reference", "symbol": "use/symbol reference",
    "marker": "marker",
}

PRESENTATION = {
    "fill", "fill-rule", "fill-opacity", "stroke", "stroke-width", "stroke-linecap", "stroke-linejoin",
    "stroke-miterlimit", "stroke-dasharray", "stroke-dashoffset", "stroke-opacity", "opacity",
    "transform", "clip-path", "clip-rule", "display", "visibility", "color",
}
GEOMETRY = {
    "path": {"d"}, "circle": {"cx", "cy", "r"}, "ellipse": {"cx", "cy", "rx", "ry"},
    "rect": {"x", "y", "width", "height", "rx", "ry"}, "line": {"x1", "y1", "x2", "y2"},
    "polyline": {"points"}, "polygon": {"points"}, "svg": {"viewBox", "width", "height"},
    "g": set(), "defs": set(), "clipPath": {"clipPathUnits"},
}
BLACKS = {"#000", "#000000", "black", "rgb(0,0,0)", "currentcolor"}


class SvgRejected(ValueError):
    pass


@dataclass
class SanitizeResult:
    svg: str  # sanitized display SVG (utf-8 text)
    view_box: tuple[float, float, float, float]
    route: str  # "font" | "svg-only"
    reasons: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)


def _local(tag) -> str:
    if not isinstance(tag, str):
        return ""
    return tag.split("}", 1)[1] if tag.startswith("{") else tag


def _parse_style(style: str) -> dict[str, str]:
    out = {}
    for decl in style.split(";"):
        if ":" in decl:
            k, v = decl.split(":", 1)
            out[k.strip().lower()] = v.strip()
    return out


def parse_view_box(root) -> tuple[float, float, float, float]:
    vb = root.get("viewBox")
    if vb:
        parts = [float(p) for p in re.split(r"[\s,]+", vb.strip()) if p]
        if len(parts) != 4 or parts[2] <= 0 or parts[3] <= 0:
            raise SvgRejected(f"invalid viewBox {vb!r}")
        return tuple(parts)  # type: ignore[return-value]
    w, h = root.get("width"), root.get("height")
    try:
        wf, hf = float(re.sub(r"px$", "", w or "")), float(re.sub(r"px$", "", h or ""))
    except ValueError as e:
        raise SvgRejected("missing viewBox and numeric width/height") from e
    if wf <= 0 or hf <= 0:
        raise SvgRejected("non-positive width/height")
    return (0.0, 0.0, wf, hf)


def safe_parse(data: bytes):
    if len(data) > MAX_BYTES:
        raise SvgRejected(f"SVG larger than {MAX_BYTES} bytes")
    if b"<!DOCTYPE" in data[:4096].upper() or b"<!ENTITY" in data.upper():
        raise SvgRejected("DOCTYPE/ENTITY declarations are not allowed")
    parser = etree.XMLParser(
        resolve_entities=False, no_network=True, load_dtd=False, dtd_validation=False,
        huge_tree=False, remove_comments=True, remove_pis=True, recover=False,
    )
    try:
        root = etree.fromstring(data, parser)
    except etree.XMLSyntaxError as e:
        raise SvgRejected(f"XML syntax error: {e}") from e
    if _local(root.tag) != "svg":
        raise SvgRejected("root element is not <svg>")
    count = 0
    for el in root.iter():
        count += 1
        if count > MAX_ELEMENTS:
            raise SvgRejected("too many elements")
    def depth(e, d=0):
        if d > MAX_DEPTH:
            raise SvgRejected("nesting too deep")
        for c in e:
            depth(c, d + 1)
    depth(root)
    return root


def sanitize_svg(data: bytes | str) -> SanitizeResult:
    if isinstance(data, str):
        data = data.encode("utf-8")
    root = safe_parse(data)
    view_box = parse_view_box(root)
    reasons: list[str] = []
    removed: list[str] = []
    colors: set[str] = set()
    ids: set[str] = set()

    for el in list(root.iter()):
        if not isinstance(el.tag, str):
            continue
        ns = el.tag[1:].split("}")[0] if el.tag.startswith("{") else SVG_NS
        name = _local(el.tag)
        parent = el.getparent()
        if ns != SVG_NS:
            removed.append(f"foreign element {name}")
            if parent is not None:
                parent.remove(el)
            continue
        if name in SVG_ONLY:
            reasons.append(SVG_ONLY[name])
            if name in ("use", "symbol"):
                href = el.get("href") or el.get(f"{{{XLINK_NS}}}href") or ""
                if not href.startswith("#"):
                    removed.append(f"external reference on <{name}>")
                    if parent is not None:
                        parent.remove(el)
            continue
        if name in DROP:
            removed.append(f"<{name}>")
            if parent is not None:
                parent.remove(el)
            continue
        if name not in KEEP:
            removed.append(f"unsupported <{name}>")
            if parent is not None:
                parent.remove(el)
            continue

        # style="" -> presentation attributes (allow-listed only)
        style = el.attrib.pop("style", None)
        if style:
            for k, v in _parse_style(style).items():
                # Only local url(#id) references survive; external url() is dropped.
                if k in PRESENTATION and not re.search(r"url\(\s*['\"]?(?!#)", v, re.I):
                    el.set(k, v)
        allowed = PRESENTATION | GEOMETRY.get(name, set()) | {"id"}
        for attr in list(el.attrib):
            local = _local(attr)
            if attr.startswith("{") or local not in allowed:
                del el.attrib[attr]
                if local.lower().startswith("on"):
                    removed.append(f"event handler {local}")
        if el.get("id"):
            ids.add(el.get("id"))
        for paint_attr in ("fill", "stroke"):
            v = el.get(paint_attr)
            if v is None:
                continue
            lv = v.strip().lower().replace(" ", "")
            if lv.startswith("url("):
                reasons.append("paint server (gradient/pattern)")
            elif lv not in ("none", "currentcolor", "inherit", "transparent"):
                colors.add(lv)
        for op_attr in ("opacity", "fill-opacity", "stroke-opacity"):
            v = el.get(op_attr)
            if v is not None:
                try:
                    f = float(v.rstrip("%")) / (100 if v.endswith("%") else 1)
                except ValueError:
                    f = 1.0
                if 0 < f < 1:
                    reasons.append("partial opacity (multi-tone artwork)")
        cp = el.get("clip-path")
        if cp and not re.fullmatch(r"url\(#[-\w.:]+\)", cp.strip()):
            del el.attrib["clip-path"]
            removed.append("non-local clip-path")

    non_black = {c for c in colors if c not in BLACKS}
    if len(non_black) > 1 or (non_black and colors & BLACKS):
        reasons.append("multicolour artwork")

    # Unify single colour to currentColor so the icon inherits text colour.
    if not any(r in ("multicolour artwork",) for r in reasons):
        for el in root.iter():
            for paint_attr in ("fill", "stroke"):
                v = el.get(paint_attr)
                if v and v.strip().lower() not in ("none", "currentcolor", "inherit", "transparent") and not v.lower().startswith("url("):
                    el.set(paint_attr, "currentColor")
        if root.get("fill") is None:
            root.set("fill", "currentColor")

    # Normalise root: keep viewBox (aspect ratio preserved), drop fixed pixel size.
    for a in ("width", "height"):
        if a in root.attrib:
            del root.attrib[a]
    root.set("viewBox", " ".join(_num(v) for v in view_box))
    etree.cleanup_namespaces(root)
    svg = etree.tostring(root, encoding="unicode")
    svg = re.sub(r">\s+<", "><", svg).strip()
    return SanitizeResult(
        svg=svg, view_box=view_box, route="svg-only" if reasons else "font",
        reasons=sorted(set(reasons)), removed=removed,
    )


def _num(v: float) -> str:
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s
