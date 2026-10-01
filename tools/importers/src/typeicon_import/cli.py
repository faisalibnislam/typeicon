"""typeicon-import CLI.

  typeicon-import fetch [--source SLUG ...]          download + verify pinned sources
  typeicon-import build [--source SLUG ...] [--dry-run] [--offline]
  typeicon-import audit                               write catalog-audit.json + report
  typeicon-import db-load [--database-url URL]        transactional load into PostgreSQL
  typeicon-import check-registry --against FILE       append-only check vs a previous registry
  typeicon-import release --version 0.1.0 --date 2026-09-30 [--source SLUG ...]
  typeicon-import pull-overrides                      export admin metadata edits to assets/registry/overrides.json
"""
from __future__ import annotations

import argparse
import json
import sys


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="typeicon-import")
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch")
    f.add_argument("--source", action="append")
    b = sub.add_parser("build")
    b.add_argument("--source", action="append")
    b.add_argument("--dry-run", action="store_true")
    b.add_argument("--offline", action="store_true")
    b.add_argument("--workers", type=int)
    a = sub.add_parser("audit")
    a.add_argument("--raster", action="store_true", help="also rasterise Core styles to detect identical geometry")
    d = sub.add_parser("db-load")
    d.add_argument("--database-url")
    d.add_argument("--release", default="0.1.0", help="release version to load (use 'none' to skip)")
    d.add_argument("--overwrite-release", action="store_true", help="replace stored files of an unpublished local release")
    d.add_argument("--prune-removed", action="store_true", help="delete sources that were removed from the manifest")
    r = sub.add_parser("release")
    r.add_argument("--version", required=True)
    r.add_argument("--date", required=True, help="release date (ISO), used for deterministic timestamps")
    r.add_argument("--source", action="append")
    r.add_argument("--workers", type=int)
    sub.add_parser("pull-overrides")
    c = sub.add_parser("check-registry")
    c.add_argument("--against", required=True)
    args = ap.parse_args(argv)

    if args.cmd == "fetch":
        from .sources import load_manifest, repo_root, source_dir
        root = repo_root()
        for s in load_manifest(root):
            if args.source and s.slug not in args.source:
                continue
            print(s.slug, "->", source_dir(s, root))
        return 0
    if args.cmd == "build":
        from .build import build_catalog
        rep = build_catalog(only=args.source, offline=args.offline, dry_run=args.dry_run, workers=args.workers)
        print(json.dumps({k: rep[k] for k in ("sources", "totalDesigns", "newCodepoints")}, indent=2, default=dict))
        if rep["errors"]:
            print(f"{len(rep['errors'])} errors (see build/catalog/report.json)", file=sys.stderr)
        return 0
    if args.cmd == "audit":
        from .audit import run_audit
        audit = run_audit(raster=args.raster)
        print(json.dumps(audit["summary"], indent=2))
        return 0
    if args.cmd == "db-load":
        from .db import load_catalog
        rel = None if args.release == "none" else args.release
        print(json.dumps(load_catalog(args.database_url, release_version=rel, overwrite_release=args.overwrite_release, prune_removed=args.prune_removed), indent=2, default=str))
        return 0
    if args.cmd == "release":
        from .release import build_release
        idx = build_release(args.version, args.date, only_sources=args.source, workers=args.workers)
        print(json.dumps(idx["counts"], indent=2))
        return 0
    if args.cmd == "pull-overrides":
        from .db import pull_overrides
        print(json.dumps(pull_overrides(), indent=2))
        return 0
    if args.cmd == "check-registry":
        from .registry import CodepointRegistry
        from .sources import repo_root
        reg = CodepointRegistry(repo_root() / "assets" / "registry" / "codepoints.json")
        with open(args.against) as fh:
            problems = reg.check_append_only(json.load(fh))
        for p in problems:
            print(p, file=sys.stderr)
        return 1 if problems else 0
    return 2


if __name__ == "__main__":
    sys.exit(main())


def review_main() -> int:
    """typeicon-review-sheets [version]: write build/review/core-<style>.png from the release fonts."""
    import json as _json
    from typeicon_fonts.review import review_sheet
    from .build import load_designs
    from .sources import repo_root
    version = sys.argv[1] if len(sys.argv) > 1 else "0.1.0"
    root = repo_root()
    rel = root / "dist" / "releases" / version / "typeicon-release"
    fams = {f["slug"]: f for f in _json.loads((rel / "metadata/families.json").read_text())}
    core = [d for d in load_designs(root) if d["area"] == "core"]
    for style in ("filled", "line", "rounded", "thin"):
        font = rel / "desktop" / fams[f"core-{style}"]["files"]["otf"]["name"]
        items = [{"name": d["name"], "style": style, "svg": v["svg"], "font": str(font), "codepoint": d["codepoint"]}
                 for d in core for v in d["variants"] if v["style"] == style and v["status"] == "published"]
        out = review_sheet(items, root / "build" / "review" / f"core-{style}.png", f"TypeIcon Core {style} - release {version}")
        print(out)
    return 0
