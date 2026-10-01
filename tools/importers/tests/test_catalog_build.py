"""Catalog build: idempotency, dry runs, honest status and identical-geometry rejection (on the real sources)."""
import hashlib
import json

import pytest

from typeicon_import.build import build_catalog, geometry_signature, load_designs
from typeicon_import.sources import repo_root

ROOT = repo_root()


@pytest.fixture(scope="module")
def designs():
    return load_designs(ROOT)


def test_dry_run_changes_nothing():
    reg = ROOT / "assets/registry/codepoints.json"
    cat = ROOT / "build/catalog/designs.jsonl"
    before = (hashlib.sha256(reg.read_bytes()).hexdigest(), hashlib.sha256(cat.read_bytes()).hexdigest())
    rep = build_catalog(only=["typeicon-core"], offline=True, dry_run=True, log=lambda *_: None)
    assert rep["newCodepoints"] == 0
    after = (hashlib.sha256(reg.read_bytes()).hexdigest(), hashlib.sha256(cat.read_bytes()).hexdigest())
    assert before == after


def test_rebuild_is_idempotent():
    reg = ROOT / "assets/registry/codepoints.json"
    before = hashlib.sha256(reg.read_bytes()).hexdigest()
    rep = build_catalog(offline=True, log=lambda *_: None)
    assert rep["newCodepoints"] == 0
    assert hashlib.sha256(reg.read_bytes()).hexdigest() == before


def test_stable_ids_and_names(designs):
    ids = [d["id"] for d in designs]
    assert len(ids) == len(set(ids))
    names = [d["name"] for d in designs]
    assert len(names) == len(set(names))
    for d in designs:
        if d["area"] == "brands":
            assert d["name"].startswith("brand-")
        for v in d["variants"]:
            assert v["sourceSha256"] and len(v["sourceSha256"]) == 64


def test_identical_geometry_is_never_published_as_two_styles(designs):
    for d in designs:
        sigs = [geometry_signature(v["svg"]) for v in d["variants"] if v["status"] == "published" and v.get("svg")]
        assert len(sigs) == len(set(sigs)), d["name"]


def test_incompatible_brand_licenses_are_quarantined(designs):
    allowed = {"CC0-1.0", "Unlicense", "MIT", "Apache-2.0", "BSD-3-Clause", "CC-BY-2.5", "CC-BY-3.0", "CC-BY-4.0"}
    brands = [d for d in designs if d["source"] == "simple-icons"]
    q = [d for d in brands if any(v["status"] == "quarantined" for v in d["variants"])]
    published = [d for d in brands if any(v["status"] == "published" for v in d["variants"])]
    assert q and all(d["license"] not in allowed for d in q)
    # share-alike, non-commercial, no-derivatives, copyleft and custom logos are never published
    assert published and all(d["license"] in allowed for d in published)
    assert all(d.get("codepoint") is None for d in q)  # quarantined logos never enter fonts


def test_only_core_and_brands_remain(designs):
    assert {d["source"] for d in designs} == {"typeicon-core", "simple-icons"}


def test_variants_record_their_base(designs):
    names = {d["name"] for d in designs}
    variants = [d for d in designs if (d.get("extra") or {}).get("variantOf")]
    assert variants
    for d in variants:
        vo = d["extra"]["variantOf"]
        assert vo["name"] in names and d["name"] == f"{vo['name']}-{vo['modifier']}"


def test_core_is_complete_and_font_ready(designs):
    core = [d for d in designs if d["area"] == "core"]
    assert len(core) >= 70
    for d in core:
        styles = {v["style"]: v for v in d["variants"] if v["status"] == "published"}
        assert set(styles) - {"thin"} == {"filled", "line", "rounded"}, d["name"]  # Thin only where it differs from Line
        assert all(v["route"] == "font" for v in styles.values())


def test_brand_icons_flagged(designs):
    assert all(d["isBrand"] for d in designs if d["source"] == "simple-icons")
    assert not any(d["isBrand"] for d in designs if d["area"] == "core")


def test_audit_counts_are_honest():
    from typeicon_import.audit import run_audit
    a = run_audit(ROOT, raster=False)
    s = a["summary"]
    assert s["coreCompleteConcepts"] + s["coreTransformDerived"] + s["coreIncomplete"] == s["coreDesigns"]
    assert s["coreCompleteConcepts"] == s["coreBaseConcepts"] + s["coreVariantConcepts"]
    assert s["gapToGoal"] == max(0, 20000 - s["coreBaseConcepts"])  # goal: 20,000 unique drawn concepts
    assert s["communityDesigns"] > 0 and "communityDesigns" not in ("coreCompleteConcepts",)
    assert any(g["source"] == "typeicon-core" for g in a["licenseGaps"])  # the draft Core license is reported
    json.dumps(a)
