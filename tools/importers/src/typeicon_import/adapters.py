"""Per-source adapters: turn a pinned source directory into RawIcon records.

Adapters never modify artwork. They only read the immutable original files and the
upstream metadata, and report each file's native style and the TypeIcon style it maps to.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from .sources import Source

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass
class RawIcon:
    source: str
    native_name: str
    native_style: str
    style: str
    path: Path  # absolute path of the original file
    rel_path: str  # path relative to the source root (provenance)
    tags: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)
    description: str = ""
    aliases: list[str] = field(default_factory=list)
    is_brand: bool = False
    derived_from: dict | None = None
    license: str | None = None  # per-icon license when it differs from the source's
    extra: dict = field(default_factory=dict)  # e.g. brand colour, source URL, guidelines
    keywords: list[str] = field(default_factory=list)  # search terms beyond the display tags
    context: str | None = None  # plain-language passage: what it shows, where it is used


def kebab(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return re.sub(r"-{2,}", "-", s)


def slug_category(c: str) -> str:
    return kebab(c.replace("&", "and"))


def _clean_tags(tags) -> list[str]:
    out = []
    for t in tags or []:
        t = str(t).strip().lower()
        if t and not t.startswith("*") and t not in out and len(t) <= 40:
            out.append(t)
    return out


def _style_files(src: Source, base: Path) -> Iterator[tuple[str, dict, str, Path]]:
    """Yield (native_style, style_cfg, native_name, file) for each style directory.

    A style's "dir" may be a list (Core: hand-authored bases + generated variants)."""
    styles = src["styles"]
    suffixes = [cfg.get("suffix", "") for cfg in styles.values() if cfg.get("suffix")]
    for native_style, cfg in styles.items():
        dirs = cfg["dir"] if isinstance(cfg["dir"], list) else [cfg["dir"]]
        suffix = cfg.get("suffix", "")
        for d in (base / name for name in dirs):
            for f in sorted(d.glob("*.svg")):
                stem = f.stem
                if suffix:
                    if not stem.endswith(suffix):
                        continue
                    stem = stem[: -len(suffix)]
                elif any(stem.endswith(x) and (d / f"{stem[:-len(x)]}.svg").exists() for x in suffixes):
                    continue  # belongs to a suffixed style stored in the same directory
                yield native_style, cfg, stem, f


def core_adapter(src: Source, base: Path) -> Iterator[RawIcon]:
    meta = {m["name"]: m for m in json.loads((base / "core-icons.json").read_text())["icons"]}
    for native_style, cfg, stem, f in _style_files(src, base):
        m = meta.get(stem)
        if m is None:
            raise ValueError(f"core SVG {f} has no metadata entry in core-icons.json")
        yield RawIcon(
            source=src.slug, native_name=stem, native_style=native_style, style=cfg["style"],
            path=f, rel_path=str(f.relative_to(base)), tags=_clean_tags(m["tags"]),
            categories=[m["category"]], description=m["description"], aliases=list(m["aliases"]),
            derived_from=m.get("derivedFrom"),
            extra={k: v for k, v in (("variantOf", m.get("variantOf")), ("designReview", m.get("review"))) if v},
            keywords=list(m.get("keywords") or []), context=m.get("context"),
        )


def simple_icons_adapter(src: Source, base: Path) -> Iterator[RawIcon]:
    """Brand logos. One style only; per-logo license, colour, source and guidelines are kept."""
    data = json.loads((base / src["metadata"]["file"]).read_text())
    meta = {d["slug"]: d for d in data}
    from .sources import repo_root
    search: dict[str, dict] = {}  # assets/sources/brand-keywords/*.json: what each brand is, for search
    for p in sorted((repo_root() / "assets/sources/brand-keywords").glob("*.json")):
        search.update(json.loads(p.read_text()))
    for native_style, cfg, stem, f in _style_files(src, base):
        m = meta.get(stem)
        if m is None:
            continue  # SVG without metadata: skip rather than guess its provenance
        lic = (m.get("license") or {}).get("type")
        aka = [kebab(a) for a in (m.get("aliases") or {}).get("aka", [])]
        yield RawIcon(
            source=src.slug, native_name=stem, native_style=native_style, style=cfg["style"],
            path=f, rel_path=str(f.relative_to(base)), tags=_clean_tags([m["title"].lower(), *aka]),
            categories=["brands"], description=f"{m['title']} logo. Trademark of its owner.",
            is_brand=True, license=lic,
            extra={"title": m["title"], "hex": m["hex"], "sourceUrl": m.get("source"),
                   "guidelines": m.get("guidelines"), "licenseUrl": (m.get("license") or {}).get("url")},
            keywords=list((search.get(stem) or {}).get("keywords", [])), context=(search.get(stem) or {}).get("context"),
        )


ADAPTERS = {
    "typeicon-core": core_adapter,
    "simple-icons": simple_icons_adapter,
}
