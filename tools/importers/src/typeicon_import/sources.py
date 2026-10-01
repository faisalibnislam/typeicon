"""Source manifest loading, pinned fetch with integrity verification, safe extraction."""
from __future__ import annotations

import base64
import hashlib
import json
import os
import shutil
import tarfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path

MAX_MEMBERS = 60_000
MAX_TOTAL_BYTES = 400 * 1024 * 1024
MAX_MEMBER_BYTES = 8 * 1024 * 1024


def repo_root() -> Path:
    env = os.environ.get("TYPEICON_ROOT")
    if env:
        return Path(env).resolve()
    here = Path(__file__).resolve()
    for p in here.parents:
        if (p / "assets" / "sources" / "manifest.json").exists():
            return p
    raise RuntimeError("cannot locate repository root (set TYPEICON_ROOT)")


@dataclass
class Source:
    raw: dict

    @property
    def slug(self) -> str:
        return self.raw["slug"]

    @property
    def area(self) -> str:
        return self.raw["area"]

    @property
    def namespace(self) -> str:
        return self.raw["namespace"]

    @property
    def prefix(self) -> str:
        return self.raw.get("namePrefix", "")

    @property
    def version(self) -> str:
        return self.raw["version"]

    @property
    def approved(self) -> bool:
        return self.raw.get("review", {}).get("status") == "approved"

    def __getitem__(self, k):
        return self.raw[k]

    def get(self, k, default=None):
        return self.raw.get(k, default)


def load_manifest(root: Path | None = None) -> list[Source]:
    root = root or repo_root()
    doc = json.loads((root / "assets" / "sources" / "manifest.json").read_text())
    slugs = [s["slug"] for s in doc["sources"]]
    if len(slugs) != len(set(slugs)):
        raise ValueError("duplicate source slugs in manifest")
    prefixes = [s.get("namePrefix") for s in doc["sources"] if s.get("namePrefix")]
    if len(prefixes) != len(set(prefixes)):
        raise ValueError("duplicate name prefixes in manifest")
    return [Source(s) for s in doc["sources"]]


class IntegrityError(RuntimeError):
    pass


def verify_integrity(data: bytes, integrity: str) -> None:
    algo, _, b64 = integrity.partition("-")
    if algo not in ("sha512", "sha384", "sha256"):
        raise IntegrityError(f"unsupported integrity algorithm {algo}")
    digest = base64.b64encode(hashlib.new(algo, data).digest()).decode()
    if digest != b64:
        raise IntegrityError(f"integrity mismatch: expected {integrity}, got {algo}-{digest}")


def fetch_tarball(src: Source, root: Path, offline: bool = False) -> Path:
    cache = root / ".cache" / "tarballs"
    cache.mkdir(parents=True, exist_ok=True)
    dest = cache / Path(src["tarball"]).name
    if dest.exists():
        verify_integrity(dest.read_bytes(), src["integrity"])
        return dest
    if offline:
        raise FileNotFoundError(f"{dest} missing and offline mode is set")
    req = urllib.request.Request(src["tarball"], headers={"User-Agent": "typeicon-importer"})
    with urllib.request.urlopen(req, timeout=120) as resp:  # noqa: S310 - pinned https URL from manifest
        data = resp.read(MAX_TOTAL_BYTES + 1)
    if len(data) > MAX_TOTAL_BYTES:
        raise IntegrityError("tarball exceeds size limit")
    verify_integrity(data, src["integrity"])
    tmp = dest.with_suffix(".part")
    tmp.write_bytes(data)
    tmp.replace(dest)
    return dest


def safe_extract(tarball: Path, dest: Path) -> Path:
    """Extract with traversal protection and decompression limits. Idempotent."""
    marker = dest / ".complete"
    if marker.exists():
        return dest
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    total = 0
    with tarfile.open(tarball, "r:gz") as tf:
        members = []
        for i, m in enumerate(tf):
            if i >= MAX_MEMBERS:
                raise IntegrityError("archive has too many members")
            if not (m.isfile() or m.isdir()):
                continue  # no symlinks, devices or hard links
            name = Path(m.name)
            if name.is_absolute() or ".." in name.parts:
                raise IntegrityError(f"unsafe path in archive: {m.name}")
            if m.size > MAX_MEMBER_BYTES:
                raise IntegrityError(f"archive member too large: {m.name}")
            total += m.size
            if total > MAX_TOTAL_BYTES:
                raise IntegrityError("archive expands beyond size limit")
            members.append(m)
        tf.extractall(dest, members=members, filter="data")
    # Originals are immutable once extracted.
    for p in dest.rglob("*"):
        if p.is_file():
            p.chmod(0o444)
    marker.write_text("ok\n")
    return dest


def source_dir(src: Source, root: Path, offline: bool = False) -> Path:
    """Directory containing the immutable original files for a source."""
    if src["kind"] == "local":
        return root / src["path"]
    tarball = fetch_tarball(src, root, offline=offline)
    out = safe_extract(tarball, root / ".cache" / "sources" / src.slug / src.version)
    return out / "package"
