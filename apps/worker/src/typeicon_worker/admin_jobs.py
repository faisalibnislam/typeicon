"""Admin jobs: pinned catalog imports and release builds (long-running; never in a web request)."""
from __future__ import annotations

import os

from .queue import Job, PermanentError


def run_catalog_import(job: Job, database_url: str) -> dict:
    from typeicon_import.build import build_catalog
    from typeicon_import.db import load_catalog
    from typeicon_import.sources import load_manifest

    known = {s.slug for s in load_manifest()}
    sources = job.payload.get("sources") or sorted(known)
    unknown = [s for s in sources if s not in known]
    if unknown:
        raise PermanentError(f"unknown sources {unknown}; add them to assets/sources/manifest.json first")
    lines: list[str] = []
    report = build_catalog(only=sources, dry_run=bool(job.payload.get("dryRun")), log=lines.append)
    summary = {"dryRun": bool(job.payload.get("dryRun")), "sources": report["sources"],
               "errors": report["errors"][:50], "nameCollisions": report["nameCollisions"][:50],
               "newCodepoints": report["newCodepoints"], "log": lines[-20:]}
    if not job.payload.get("dryRun"):
        loaded = load_catalog(database_url, release_version=None, actor=f"admin-job:{job.id}")
        summary["loaded"] = {"designs": loaded["designs"], "variants": loaded["variants"]}
    return summary


def run_release_build(job: Job, database_url: str) -> dict:
    from typeicon_import.db import load_catalog
    from typeicon_import.release import build_release

    version, date = job.payload["version"], job.payload["date"]
    idx = build_release(version, date, workers=int(os.environ.get("RELEASE_BUILD_WORKERS", "4")))
    loaded = load_catalog(database_url, release_version=version, actor=f"admin-job:{job.id}")
    return {"version": version, "counts": idx["counts"], "archives": len(idx["archives"]), "release": loaded.get("release")}
