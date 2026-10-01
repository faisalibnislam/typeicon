"""Font family planning: which published variants go into which font file.

Rules
  * Core: one family per style (TypeIcon Filled / Line / Rounded), codepoints shared.
  * Brands: one family, "TypeIcon Brands".
  * Families larger than MAX_GLYPHS_PER_FONT are split into explicit "Part N" families with
    unique family/PostScript names and a manifest of contents.
  * Only variants with status=published and route=font are compiled. SVG-only artwork is
    listed as unsupported in the manifest.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from fontTools.svgLib.path import parse_path
from pathops import Path

from typeicon_fonts.compiler import GlyphSpec

# OpenType allows 65,535 glyph ids; ligature input glyphs (a-z, 0-9, "-") and .notdef need a few. One font per style
# is what desktop users expect (install "TypeIcon Line", type any icon name), so only split beyond this.
MAX_GLYPHS_PER_FONT = 65_000
STYLE_TITLES = {"filled": "Filled", "line": "Line", "rounded": "Rounded", "thin": "Thin", "brand": "Brands"}
PACK_TITLES: dict[str, str] = {}


@dataclass
class Family:
    slug: str  # "core-line", "tabler-rounded", "tabler-rounded-part-2"
    family: str  # "TypeIcon Line"
    ps_name: str  # "TypeIconLine-Regular"
    source: str
    area: str
    style: str
    css_class: str  # "typeicon-line" | "typeicon-pack-tabler-rounded"
    entries: list[tuple[dict, dict]] = field(default_factory=list)  # (design, variant)
    part: int | None = None

    @property
    def file_base(self) -> str:
        return self.ps_name


def keywords_for(design: dict) -> list[str]:
    kws = [design["name"]]
    if design["area"] != "core" and len(design["localName"]) >= 2 and design["localName"] not in kws:
        kws.append(design["localName"])
    for a in design.get("aliases", []):
        if a not in kws:
            kws.append(a)
    return kws


def codepoints_for(design: dict) -> list[int]:
    cps = [design["codepoint"]]
    if design.get("bmpCodepoint"):
        cps.append(design["bmpCodepoint"])
    return cps


def outline_path(outline: dict) -> Path:
    p = Path()
    parse_path(outline["d"], p.getPen())
    return p


def glyph_spec(design: dict, variant: dict) -> GlyphSpec:
    cp = design["codepoint"]
    return GlyphSpec(
        glyph_name=f"u{cp:04X}" if cp > 0xFFFF else f"uni{cp:04X}",
        codepoints=codepoints_for(design),
        keywords=keywords_for(design),
        outline=outline_path(variant["outline"]),
        advance=variant["outline"]["advance"],
    )


def plan_families(designs: list[dict], max_glyphs: int = MAX_GLYPHS_PER_FONT) -> tuple[list[Family], list[dict]]:
    """Group published font-ready variants into families. Returns (families, unsupported)."""
    groups: dict[tuple[str, str], list[tuple[dict, dict]]] = {}
    unsupported: list[dict] = []
    for d in designs:
        if d.get("codepoint") is None:
            continue
        for v in d["variants"]:
            if v["status"] != "published":
                continue
            if v["route"] != "font" or not v.get("outline"):
                unsupported.append({"name": d["name"], "style": v["style"], "reasons": v["reasons"]})
                continue
            groups.setdefault((d["source"], v["style"]), []).append((d, v))

    families: list[Family] = []
    for (source, style), entries in sorted(groups.items()):
        entries.sort(key=lambda e: e[0]["codepoint"])
        st = STYLE_TITLES.get(style, style.title())
        area = entries[0][0]["area"]
        if area == "core":
            fam, ps, slug, css = f"TypeIcon {st}", f"TypeIcon{st}-Regular", f"core-{style}", f"typeicon-{style}"
        elif area == "brands":
            fam, ps, slug, css = "TypeIcon Brands", "TypeIconBrands-Regular", "brands", "typeicon-brands"
        else:
            pt = PACK_TITLES.get(source, source.title())
            fam, ps, slug, css = (f"TypeIcon {pt} {st}", f"TypeIcon{pt}{st}-Regular",
                                  f"{source}-{style}", f"typeicon-pack-{source}-{style}")
        chunks = [entries[i:i + max_glyphs] for i in range(0, len(entries), max_glyphs)]
        for i, chunk in enumerate(chunks):
            if len(chunks) == 1:
                families.append(Family(slug, fam, ps, source, area, style, css, chunk))
            else:
                n = i + 1
                families.append(Family(
                    f"{slug}-part-{n}", f"{fam} Part {n}", ps.replace("-Regular", f"Part{n}-Regular"),
                    source, area, style, f"{css}-part-{n}", chunk, part=n,
                ))
    return families, unsupported
