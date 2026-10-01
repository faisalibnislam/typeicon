"""Pinned-source integrity, archive safety, and the append-only codepoint registry."""
import base64
import hashlib
import io
import json
import tarfile

import pytest

from typeicon_import.registry import CodepointRegistry, NameRegistry
from typeicon_import.sources import IntegrityError, load_manifest, safe_extract, verify_integrity


def test_integrity_verification():
    data = b"hello"
    good = "sha512-" + base64.b64encode(hashlib.sha512(data).digest()).decode()
    verify_integrity(data, good)
    with pytest.raises(IntegrityError, match="mismatch"):
        verify_integrity(b"tampered", good)
    with pytest.raises(IntegrityError, match="unsupported"):
        verify_integrity(data, "md5-abc")


def _tar(tmp_path, members):
    p = tmp_path / "t.tgz"
    with tarfile.open(p, "w:gz") as tf:
        for name, payload, kind in members:
            info = tarfile.TarInfo(name)
            if kind == "sym":
                info.type = tarfile.SYMTYPE
                info.linkname = "/etc/passwd"
                tf.addfile(info)
            else:
                info.size = len(payload)
                tf.addfile(info, io.BytesIO(payload))
    return p


def test_safe_extract_blocks_traversal(tmp_path):
    with pytest.raises(IntegrityError, match="unsafe path"):
        safe_extract(_tar(tmp_path, [("package/../../evil.txt", b"x", "file")]), tmp_path / "out")
    with pytest.raises(IntegrityError, match="unsafe path"):
        safe_extract(_tar(tmp_path, [("/abs/evil.txt", b"x", "file")]), tmp_path / "out2")


def test_safe_extract_skips_links_and_is_read_only(tmp_path):
    out = safe_extract(_tar(tmp_path, [("package/a.svg", b"<svg/>", "file"), ("package/link", b"", "sym")]), tmp_path / "o")
    assert (out / "package/a.svg").exists()
    assert not (out / "package/link").exists()
    assert not ((out / "package/a.svg").stat().st_mode & 0o222)  # originals are immutable


def test_manifest_has_provenance_for_every_source():
    for s in load_manifest():
        raw = s.raw
        for key in ("slug", "area", "displayName", "version", "license", "copyright", "retrievedAt", "styles", "review"):
            assert raw.get(key), (s.slug, key)
        assert raw["license"]["spdx"] and raw["license"]["file"]
        if raw["kind"] == "npm":
            assert raw["integrity"].startswith("sha512-") and raw["tarball"].startswith("https://")


def test_registry_append_only(tmp_path):
    reg = CodepointRegistry(tmp_path / "cp.json")
    a = reg.allocate("core", ["home", "search"])
    assert a == {"home": 0xF0000, "search": 0xF0001}
    reg.save()
    prev = json.loads((tmp_path / "cp.json").read_text())
    reg2 = CodepointRegistry(tmp_path / "cp.json")
    b = reg2.allocate("core", ["arrow", "home", "search"])  # new name appended; existing untouched
    assert b == {"arrow": 0xF0002, "home": 0xF0000, "search": 0xF0001}
    assert reg2.check_append_only(prev) == []
    reg2.doc["namespaces"]["core"]["assignments"]["home"] = 0xF0005
    assert any("changed" in p for p in reg2.check_append_only(prev))
    reg2.doc["namespaces"]["core"]["assignments"]["home"] = 0xF0001
    assert any("assigned to both" in p for p in reg2.check_append_only(prev))


def test_bmp_mirror_and_pack_ranges(tmp_path):
    reg = CodepointRegistry(tmp_path / "cp.json")
    assert reg.bmp_mirror("core", 0xF0000) == 0xE000
    assert reg.bmp_mirror("core", 0xF0000 + 6399) == 0xE000 + 6399
    assert reg.bmp_mirror("core", 0xF0000 + 6400) is None
    assert reg.bmp_mirror("pack:tabler", 0x100000) is None
    assert reg.allocate("pack:tabler", ["tabler-home"]) == {"tabler-home": 0x100000}


def test_committed_registry_is_append_only_against_itself():
    from typeicon_import.sources import repo_root
    path = repo_root() / "assets/registry/codepoints.json"
    doc = json.loads(path.read_text())
    reg = CodepointRegistry(path)
    assert reg.check_append_only(doc) == []
    for ns, space in doc["namespaces"].items():
        cps = list(space["assignments"].values())
        assert len(cps) == len(set(cps)), ns
        assert all(space["base"] <= c < space["base"] + space["limit"] for c in cps), ns


def test_name_registry_collisions():
    n = NameRegistry()
    assert n.claim("core", "home", "d1", "canonical")
    assert n.claim("core", "home", "d1", "canonical")  # idempotent for the same owner
    assert not n.claim("core", "home", "d2", "alias")
    assert n.claim("pack:tabler", "home", "d3", "pack-local")  # different namespace
    assert n.errors and "collides" in n.errors[0]
