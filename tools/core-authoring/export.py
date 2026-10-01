"""Write TypeIcon Core SVGs + metadata from the design sources.

Usage: .venv/bin/python tools/core-authoring/export.py [--only CATEGORY ...] [--no-variants]

Design sources:
  icons.py        v0.1 icons (hand-built geometry)
  sets/*.py       part-based icons (dsl.py), one module per category
  modifiers.py    variant badges; variants are generated from each category's modifier set

Outputs:
  assets/core/svg/{filled,line,rounded}/<name>.svg           base icons (committed, canonical)
  assets/core/svg-variants/{filled,line,rounded}/<name>.svg  generated variants (git-ignored, reproducible)
  assets/core/core-icons.json                                 names, aliases, tags, categories, provenance
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path as FsPath

HERE = FsPath(__file__).resolve().parent
sys.path.insert(0, str(HERE))

ROOT = HERE.parents[1]
OUT = ROOT / "assets" / "core"
STYLES = ("line", "rounded", "filled", "thin")


def load_all():
    """Return (bases, variants) as lists of icon objects with .stroke(S) and .filled()."""
    from icons import ICONS
    import dsl
    from modifiers import MODIFIERS, SEARCH, SETS, compose

    for f in sorted((HERE / "sets").glob("*.py")):
        if f.name.startswith("_"):
            continue
        importlib.import_module(f"sets.{f.stem}")
    plan = json.loads((HERE / "plan.json").read_text())
    cat_mods = {**plan["existingCategoryModifiers"], **{k: v["modifiers"] for k, v in plan["categories"].items()}}

    bases = list(ICONS) + list(dsl.REGISTRY)
    names = [b.name for b in bases]
    dupes = {n for n in names if names.count(n) > 1}
    if dupes:
        raise SystemExit(f"duplicate icon names: {sorted(dupes)}")
    taken = set(names)
    alias_owner: dict[str, str] = {}
    for b in bases:
        for a in b.aliases:
            if a in taken:
                raise SystemExit(f"alias {a!r} of {b.name} collides with an icon name")
            if a in alias_owner:
                raise SystemExit(f"alias {a!r} is used by both {alias_owner[a]} and {b.name}")
            alias_owner[a] = b.name
    # A drawn icon can claim a variant's name through an alias (e.g. unpin -> pin-off): no generated duplicate.
    taken |= {a for b in bases for a in b.aliases}
    variants = []
    for b in bases:
        if b.derived_from:  # no variants of rotated siblings
            continue
        mset = getattr(b, "modifiers", None) or cat_mods.get(b.category, "none")
        for suffix in SETS[mset]:
            if b.name.endswith("-" + suffix) or b.name == suffix:
                continue
            name = f"{b.name}-{suffix}"
            if name in taken:
                continue
            mod = MODIFIERS[suffix]
            desc = f"{b.description.rstrip('.')}. Variant for {SEARCH[suffix][0].format(n=_words(b.name))}."
            variants.append(compose(b, mod, name, b.category, desc, list(dict.fromkeys(b.tags + mod.tags))))
            taken.add(name)
    return bases, variants


def _words(name: str) -> str:
    return name.replace("-", " ")


def _search_meta(ic, variant_of: dict | None, bases_by_name: dict, kw: dict) -> tuple[list[str], str | None]:
    """(keywords, context) for search. Bases come from keywords/<category>.json; variants combine the base's
    entry with the badge's meaning, e.g. file-plus: "add file", "new file", "create file"."""
    from modifiers import MODIFIERS, SEARCH
    if not variant_of:
        entry = kw.get(ic.name) or {}
        return _dedupe(entry.get("keywords", []), exclude={ic.name, *ic.tags}), entry.get("context")
    base = bases_by_name[variant_of["name"]]
    entry = kw.get(base.name) or {}
    suffix = variant_of["modifier"]
    use, phrases = SEARCH[suffix]
    noun = _words(base.name)
    # Single words only from the base: its phrases ("add user" on follow) would make every badge variant of it
    # match that phrase. The variant's own phrases come from its badge ("add file", "new file").
    inherited = [k for k in entry.get("keywords", []) if " " not in k][:18]
    words = [p.format(n=noun) for p in phrases] + MODIFIERS[suffix].tags + inherited
    article = "an" if suffix[0] in "aeiou" else "a"
    context = f"The {noun} icon with {article} {suffix} badge in the corner, for {use.format(n=noun)}."
    if entry.get("context"):
        context += " " + entry["context"]
    return _dedupe(words, exclude={ic.name, *ic.tags}), context


def _dedupe(words, exclude=()) -> list[str]:
    seen, out = set(exclude), []
    for w in words:
        w = w.strip().lower()
        if w and w not in seen:
            seen.add(w)
            out.append(w)
    return out


def stroke_svg(elements: list[str], S, rotate: int | None) -> str:
    from geometry import fmt
    body = "\n".join("  " + e for e in elements)
    if rotate:
        body = f'  <g transform="rotate({rotate} 12 12)">\n' + "\n".join("  " + ln for ln in body.splitlines()) + "\n  </g>"
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
        f'fill="none" stroke="currentColor" stroke-width="{fmt(S.w)}" stroke-linecap="{S.cap}" '
        f'stroke-linejoin="{S.join}">\n{body}\n</svg>\n'
    )


def filled_svg(d: str) -> str:
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
            f'fill="currentColor">\n  <path d="{d}"/>\n</svg>\n')


def _write_if_changed(p: FsPath, text: str) -> bool:
    if p.exists() and p.read_text() == text:
        return False
    p.write_text(text)
    return True


_CACHE: dict = {}


def _render_chunk(args) -> tuple[int, list[str]]:
    """Worker: render a slice of icons by name (modules are re-imported in each process)."""
    names, variant_dir_names = args
    from geometry import LINE, ROUNDED, THIN, path_to_d, rotation, transform_path
    if "all" not in _CACHE:
        bases, variants = load_all()
        _CACHE["all"] = {i.name: i for i in bases + variants}
    idx = _CACHE["all"]
    written, errors = 0, []
    for name in names:
        ic = idx[name]
        sub = "svg-variants" if name in variant_dir_names else "svg"
        try:
            rot = ic.derived_from.get("rotate") if ic.derived_from else None
            for S in (LINE, ROUNDED, THIN):
                written += _write_if_changed(OUT / sub / (S.slug or S.name) / f"{name}.svg", stroke_svg(ic.stroke(S), S, rot))
            filled = ic.filled()
            if rot:
                filled = transform_path(filled, rotation(rot))
            written += _write_if_changed(OUT / sub / "filled" / f"{name}.svg", filled_svg(path_to_d(filled)))
        except Exception as e:  # noqa: BLE001 - report every broken icon at once
            errors.append(f"{name}: {type(e).__name__}: {e}")
    return written, errors


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", action="append", help="only render these categories (metadata is always complete)")
    ap.add_argument("--no-variants", action="store_true")
    args = ap.parse_args()
    bases, variants = load_all()
    # Rotations / mirrors / copies of another design are published but never counted and get no variants.
    from transforms import detect
    detected = detect(bases)
    for b in bases:
        if b.name in detected:
            b.derived_from = detected[b.name]
    variants = [v for v in variants if v.derived_from["name"] not in detected]
    if args.no_variants:
        variants = []
    for sub in ("svg", "svg-variants"):
        for s in STYLES:
            (OUT / sub / s).mkdir(parents=True, exist_ok=True)

    todo = [i for i in bases + variants if not args.only or i.category in args.only]
    variant_names = {v.name for v in variants}
    names = [i.name for i in todo]
    chunk = max(20, len(names) // (os.cpu_count() or 4) // 4)
    jobs = [(names[i:i + chunk], variant_names) for i in range(0, len(names), chunk)]
    written, errors = 0, []
    with ProcessPoolExecutor() as pool:
        for w, e in pool.map(_render_chunk, jobs):
            written += w
            errors += e
    if errors:
        print("\n".join(errors[:50]), file=sys.stderr)
        raise SystemExit(f"{len(errors)} icons failed to render")

    # Remove SVGs of icons that no longer exist (renamed/removed designs).
    live = {i.name for i in bases} | variant_names
    removed = 0
    if not args.only:
        for sub in ("svg", "svg-variants"):
            for s in STYLES:
                for f in (OUT / sub / s).glob("*.svg"):
                    if f.stem not in live or (sub == "svg" and f.stem in variant_names) or (sub == "svg-variants" and f.stem not in variant_names):
                        f.unlink()
                        removed += 1

    # Every Core design is published but awaits human design review; designers' concerns are attached as notes.
    notes = json.loads((HERE / "review-notes.json").read_text())["notes"]
    unknown = sorted(set(notes) - {i.name for i in bases})
    if unknown:
        raise SystemExit(f"review-notes.json names unknown icons: {unknown}")
    from keywords import load_all as load_keywords
    kw = load_keywords()
    bases_by_name = {b.name: b for b in bases}
    meta = []
    for ic in bases + variants:
        is_var = ic.name in variant_names
        df = ic.derived_from or None
        meta.append({
            "name": ic.name, "category": ic.category, "description": ic.description, "tags": ic.tags,
            "aliases": ic.aliases, "styles": ["filled", "line", "rounded", "thin"],
            "derivedFrom": {"name": df["name"], "transform": df["transform"]} if df and "transform" in df else None,
            "variantOf": {"name": df["name"], "modifier": df["modifier"]} if df and "modifier" in df else None,
            "dir": "svg-variants" if is_var else "svg",
            "author": "TypeIcon", "origin": "original",
            "review": {"status": "pending", "note": notes.get(ic.name)},
            **dict(zip(("keywords", "context"), _search_meta(
                ic, {"name": df["name"], "modifier": df["modifier"]} if df and "modifier" in df else None, bases_by_name, kw))),
        })
    doc = {"$comment": "Generated by tools/core-authoring/export.py. SVG files are generated from the design sources.",
           "grid": 24, "strokeWidth": 2, "counts": {"base": len(bases), "variants": len(variants)},
           "icons": sorted(meta, key=lambda m: m["name"])}
    (OUT / "core-icons.json").write_text(json.dumps(doc, indent=1) + "\n")
    print(f"{len(bases)} base icons ({sum(1 for b in bases if b.derived_from)} transform-derived) + {len(variants)} variants; "
          f"{written} files written, {removed} stale removed")


if __name__ == "__main__":
    main()
