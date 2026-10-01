"""Catalog audit: computed, honest counts and gaps.

Writes build/audit/catalog-audit.json and docs/catalog-audit.md from the catalog build
(build/catalog/designs.jsonl), the latest release metadata and the source manifest.

Counting rules (docs/policies/catalog-counts.md):
  * complete Core concept = Core design with published filled + line + rounded variants,
    not transform-derived, and no pair of its styles rasterising identically.
  * aliases, brand logos, SVG-only variants and synthetic rows never count toward the goal;
    base designs and variants (base + designed badge) are reported separately.
"""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import date
from pathlib import Path

from .build import load_designs
from .sources import load_manifest, repo_root

TARGET = 20_000  # owner goal 2026-09-30: 20,000 unique drawn Core concepts; badge variants come on top
IDENTICAL_IOU = 0.995


def _raster_identical(designs: list[dict]) -> dict[str, list[str]]:
    """Rasterise each Core design's styles at 48px and flag style pairs that are visually identical."""
    from typeicon_fonts.raster import mask_iou, render_svg_mask
    flagged: dict[str, list[str]] = {}
    for d in designs:
        if d["area"] != "core" or (d.get("extra") or {}).get("variantOf"):
            continue  # variants: base + distinct badge; checking the bases is sufficient
        masks = {v["style"]: render_svg_mask(v["svg"], 48) for v in d["variants"] if v["status"] == "published" and v.get("svg")}
        styles = sorted(masks)
        for i, a in enumerate(styles):
            for b in styles[i + 1:]:
                iou = mask_iou(masks[a], masks[b])
                if iou >= IDENTICAL_IOU:
                    flagged.setdefault(d["name"], []).append(f"{a}~{b} IoU {iou:.4f}")
    return flagged


def run_audit(root: Path | None = None, raster: bool = True) -> dict:
    root = root or repo_root()
    manifest = {s.slug: s.raw for s in load_manifest(root)}
    designs = load_designs(root)
    styles = ("filled", "line", "rounded")

    pub = lambda d: [v for v in d["variants"] if v["status"] == "published"]  # noqa: E731
    core = [d for d in designs if d["area"] == "core"]
    community = [d for d in designs if d["area"] not in ("core",)]
    identical = _raster_identical(core) if raster else {}

    complete, derived, incomplete, variants_complete = [], [], [], []
    for d in core:
        have = {v["style"] for v in pub(d)}
        if not set(styles) <= have:
            incomplete.append({"name": d["name"], "missing": sorted(set(styles) - have)})
        elif d.get("derivedFrom"):
            derived.append({"name": d["name"], "derivedFrom": d["derivedFrom"]})
        elif d["name"] in identical:
            incomplete.append({"name": d["name"], "identicalStyles": identical[d["name"]]})
        elif (d.get("extra") or {}).get("variantOf"):
            variants_complete.append(d["name"])
        else:
            complete.append(d["name"])

    missing_community = defaultdict(lambda: defaultdict(int))
    for d in community:
        mapped = {m["style"] for m in manifest[d["source"]]["styles"].values()}
        have = {v["style"] for v in pub(d)}
        for s in sorted(mapped - have):
            missing_community[d["source"]][s] += 1

    sha_groups = defaultdict(list)
    for d in designs:
        for v in pub(d):
            if v.get("svgSha256"):
                sha_groups[v["svgSha256"]].append(f"{d['name']}:{v['style']}")
    duplicate_groups = [{"svgSha256": k, "members": sorted(m)} for k, m in sha_groups.items() if len({x.split(':')[0] for x in m}) > 1]
    duplicate_groups.sort(key=lambda g: (-len(g["members"]), g["members"][0]))

    unsupported = [{"name": d["name"], "style": v["style"], "reasons": v["reasons"]}
                   for d in designs for v in pub(d) if v["route"] != "font"]
    rejected = defaultdict(int)
    for d in designs:
        for v in d["variants"]:
            if v["status"] == "rejected":
                for r in v["reasons"] or ["rejected"]:
                    rejected[r] += 1

    license_gaps = []
    for slug, s in manifest.items():
        lic = s["license"]
        if lic.get("ownerDecisionRequired") or lic["spdx"].startswith("LicenseRef-") and "Draft" in lic["spdx"]:
            license_gaps.append({"source": slug, "issue": f"license {lic['spdx']} requires an owner decision before public redistribution"})
        if not (root / lic["file"]).exists():
            license_gaps.append({"source": slug, "issue": f"license file missing: {lic['file']}"})
        if s.get("review", {}).get("by", "").startswith("bootstrap"):
            license_gaps.append({"source": slug, "issue": "pack approval was recorded by the bootstrap import; owner confirmation required before public launch"})
        for n in s.get("notices", []):
            license_gaps.append({"source": slug, "issue": f"notice to re-check: {n}"})

    release_dir = sorted((root / "dist" / "releases").glob("*/typeicon-release/metadata/manifest.json"))
    release = json.loads(release_dir[-1].read_text()) if release_dir else None
    aliases = sum(len(d.get("aliases", [])) for d in designs)
    variants_pub = sum(len(pub(d)) for d in designs)
    concepts = {d["concept"] for d in designs if pub(d)}

    summary = {
        "auditDate": date.today().isoformat(),
        "goal": {"uniqueCoreConcepts": TARGET, "coreConceptStyleAssets": TARGET * 3},
        "coreCompleteConcepts": len(complete) + len(variants_complete),
        "coreBaseConcepts": len(complete),
        "coreVariantConcepts": len(variants_complete),
        "gapToGoal": max(0, TARGET - len(complete)),
        "coreDesigns": len(core),
        "coreTransformDerived": len(derived),
        "coreIncomplete": len(incomplete),
        "coreApprovedVariants": sum(len(pub(d)) for d in core),
        "communityDesigns": len(community),
        "communityVariants": sum(len(pub(d)) for d in community),
        "brandQuarantined": sum(1 for d in community if any(v["status"] == "quarantined" for v in d["variants"])),
        "distinctConceptsAllSources": len(concepts),
        "publishedVariantsAllSources": variants_pub,
        "aliases": aliases,
        "fontSupportedVariants": variants_pub - len(unsupported),
        "svgOnlyVariants": len(unsupported),
        "duplicateGroups": len(duplicate_groups),
        "licenseGaps": len(license_gaps),
        "coreIdenticalStyleFlags": len(identical),
        "rasterCheck": raster,
        "releaseCounts": release["counts"] if release else None,
    }
    audit = {
        "summary": summary,
        "definitions": "See docs/policies/catalog-counts.md",
        "core": {"complete": sorted(complete), "transformDerived": derived, "incomplete": incomplete,
                 "identicalStyleFlags": identical},
        "missingVariants": {"core": incomplete, "community": {k: dict(v) for k, v in missing_community.items()}},
        "duplicateGroups": duplicate_groups[:500],
        "unsupportedFontAssets": unsupported,
        "rejectedVariantReasons": dict(sorted(rejected.items(), key=lambda kv: -kv[1])),
        "licenseGaps": license_gaps,
        "sources": {slug: {"version": s["version"], "license": s["license"]["spdx"], "area": s["area"]} for slug, s in manifest.items()},
    }
    out = root / "build" / "audit"
    out.mkdir(parents=True, exist_ok=True)
    (out / "catalog-audit.json").write_text(json.dumps(audit, indent=1) + "\n")
    (root / "docs" / "catalog-audit.md").write_text(_markdown(audit))
    return audit


def _markdown(a: dict) -> str:
    s = a["summary"]
    f = lambda n: f"{n:,}"  # noqa: E731
    lines = [
        "# Catalog audit", "",
        f"Generated {s['auditDate']} by `typeicon-import audit` from the catalog build. Machine-readable copy: `build/audit/catalog-audit.json`.", "",
        "## The goal and where it stands", "",
        f"- **Goal:** {f(s['goal']['uniqueCoreConcepts'])} unique, individually drawn TypeIcon Core concepts, each with approved Filled, Line and Rounded variants ({f(s['goal']['coreConceptStyleAssets'])} concept/style assets).",
        f"- **Unique drawn Core concepts today:** {f(s['coreBaseConcepts'])} (rotations and mirrors of another design excluded).",
        f"- **Badge variants on top:** {f(s['coreVariantConcepts'])} (base + designed badge, e.g. `file-plus`); all Core icons together: {f(s['coreCompleteConcepts'])}.",
        f"- **Remaining gap:** {f(s['gapToGoal'])} unique concepts." + (" **The goal is not met.**" if s['gapToGoal'] else " The goal is met."), "",
        "| Measure | Count |", "|---|---:|",
        f"| Core designs | {f(s['coreDesigns'])} |",
        f"| Core complete three-style concepts (counted) | {f(s['coreCompleteConcepts'])} |",
        f"| Core directional variants derived by rotation (not counted) | {f(s['coreTransformDerived'])} |",
        f"| Core designs incomplete or with identical styles | {f(s['coreIncomplete'])} |",
        f"| Core approved variants | {f(s['coreApprovedVariants'])} |",
        f"| Core base designs (drawn individually) | {f(s['coreBaseConcepts'])} |",
        f"| Core variants (base + badge) | {f(s['coreVariantConcepts'])} |",
        f"| Brand logos (Simple Icons; never counted toward the goal) | {f(s['communityDesigns'])} |",
        f"| Distinct concepts across all sources (search concepts) | {f(s['distinctConceptsAllSources'])} |",
        f"| Published variants across all sources | {f(s['publishedVariantsAllSources'])} |",
        f"| Explicit aliases (not icons) | {f(s['aliases'])} |",
        f"| Variants compiled into fonts | {f(s['fontSupportedVariants'])} |",
        f"| SVG-only variants | {f(s['svgOnlyVariants'])} |",
        f"| Groups of identical artwork under different names | {f(s['duplicateGroups'])} |",
        f"| License gaps / open items | {f(s['licenseGaps'])} |", "",
        f"Raster identical-style check: {'run' if s['rasterCheck'] else 'skipped'}; {s['coreIdenticalStyleFlags']} Core designs flagged (styles with IoU ≥ {IDENTICAL_IOU} at 48 px).", "",
        "## Transform-derived Core designs", "",
    ]
    lines += [f"- `{d['name']}` = {d['derivedFrom']['transform']} of `{d['derivedFrom']['name']}`" for d in a["core"]["transformDerived"]] or ["- none"]
    lines += ["", "## Missing variants", "", "Core:"]
    lines += [f"- `{d['name']}`: {d}" for d in a["missingVariants"]["core"]] or ["- none"]
    lines += ["", "Brand logos (Simple Icons) have a single Brand style; logos whose own license is not on the allowlist are quarantined:"]
    lines += [f"- {src}: " + ", ".join(f"{k} {f(v)}" for k, v in m.items()) for src, m in a["missingVariants"]["community"].items()] or ["- none"]
    lines += [f"- quarantined logos: {f(s['brandQuarantined'])}", "", "## License gaps and open items", ""]
    lines += [f"- **{g['source']}**: {g['issue']}" for g in a["licenseGaps"]] or ["- none"]
    lines += ["", "## Unsupported in fonts", ""]
    lines += [f"- `{u['name']}` ({u['style']}): {'; '.join(u['reasons'])}" for u in a["unsupportedFontAssets"][:50]] or ["- none"]
    lines += ["", "## Why variants were not published", ""]
    lines += [f"- {k}: {f(v)}" for k, v in a["rejectedVariantReasons"].items()] or ["- none"]
    lines += ["", "## Duplicate artwork groups (first 25)", ""]
    lines += [f"- {', '.join(g['members'][:6])}{' …' if len(g['members']) > 6 else ''}" for g in a["duplicateGroups"][:25]] or ["- none"]
    lines += ["", "## What closing the gap requires", "",
              f"Reaching {f(TARGET)} complete Core concepts is a design programme, not a software task: {f(s['gapToGoal'])} more concepts, "
              "each drawn in Filled, Line and Rounded. All Core artwork is original (no third-party or community artwork):",
              "1. Draw the remaining base concepts in tools/core-authoring/plan.json with the part-based DSL (tools/core-authoring/AUTHORING.md), "
              "passing check.py and a human review of the review sheets.",
              "2. Each new base concept adds the variants of its category's modifier set (none / minimal 5 / common 14 / full 23).",
              "3. Agent-drawn batches are published and flagged for human design review; fix or remove anything that fails review.", ""]
    return "\n".join(lines)
