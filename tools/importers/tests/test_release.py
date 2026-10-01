"""Release artifacts: checksums, ZIP integrity, licenses, and per-family validation records."""
import hashlib
import json
import zipfile
from pathlib import Path

import pytest

from typeicon_import.sources import repo_root

REL = repo_root() / "dist/releases/0.4.0"
pytestmark = pytest.mark.skipif(not (REL / "archives/index.json").exists(), reason="release 0.4.0 not built")


def test_checksums_match():
    out = REL / "typeicon-release"
    lines = (out / "checksums.sha256").read_text().splitlines()
    assert len(lines) > 1000
    for line in lines[::97]:  # sample every 97th file
        digest, rel = line.split("  ", 1)
        assert hashlib.sha256((out / rel).read_bytes()).hexdigest() == digest, rel


def test_archives_crc_and_required_contents():
    idx = json.loads((REL / "archives/index.json").read_text())
    for a in idx["archives"]:
        p = REL / "archives" / a["file"]
        assert hashlib.sha256(p.read_bytes()).hexdigest() == a["sha256"]
        with zipfile.ZipFile(p) as zf:
            assert zf.testzip() is None
            names = zf.namelist()
            assert any(n.endswith("licenses/ATTRIBUTION.md") for n in names), a["file"]
            assert any(n.endswith("README.md") for n in names), a["file"]
            assert all(".." not in n and not n.startswith("/") for n in names)
    complete = next(a for a in idx["archives"] if a["kind"] == "complete")
    with zipfile.ZipFile(REL / "archives" / complete["file"]) as zf:
        tops = {n.split("/")[1] for n in zf.namelist() if n.count("/") >= 2}
    assert {"desktop", "webfonts", "css", "svg", "sprites", "metadata", "licenses", "examples"} <= tops


def test_every_family_validated():
    fams = json.loads((REL / "typeicon-release/metadata/families.json").read_text())
    assert {f["family"] for f in fams} >= {"TypeIcon Filled", "TypeIcon Line", "TypeIcon Rounded"}
    for f in fams:
        for fmt in ("otf", "ttf", "woff2"):
            v = f["validation"][fmt]
            assert v["ok"] and v["stats"]["ots"] == "pass" and v["stats"]["shapingChecked"] == f["keywords"], (f["family"], fmt)
        assert f["raster"]["minIoU"] >= 0.85


def test_css_urls_resolve():
    import re
    css_dir = REL / "typeicon-release/css"
    for css in css_dir.glob("*.css"):
        for url in re.findall(r'url\("([^"]+)"\)', css.read_text()):
            assert (css_dir / url).resolve().exists(), (css.name, url)
