"""Deterministic packaging helpers shared by the release builder and the worker."""
from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path

ZIP_DATE = (2026, 1, 1, 0, 0, 0)


class PackagingError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_checksums(root: Path, name: str = "checksums.sha256") -> Path:
    files = sorted(p for p in root.rglob("*") if p.is_file() and p.name != name)
    out = root / name
    out.write_text("".join(f"{sha256_file(p)}  {p.relative_to(root).as_posix()}\n" for p in files))
    return out


def write_zip(zip_path: Path, base: Path, members: list[Path], prefix: str) -> dict:
    """Deterministic ZIP: sorted entries, fixed timestamps and permissions; CRC-verified after writing."""
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = zip_path.with_suffix(".tmp")
    total = 0
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for p in sorted(members):
            rel = p.relative_to(base).as_posix()
            info = zipfile.ZipInfo(f"{prefix}/{rel}", date_time=ZIP_DATE)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            data = p.read_bytes()
            total += len(data)
            zf.writestr(info, data, compresslevel=9)
    tmp.replace(zip_path)
    with zipfile.ZipFile(zip_path) as zf:
        bad = zf.testzip()
        if bad:
            raise PackagingError(f"CRC failure in {zip_path.name}: {bad}")
    return {"file": zip_path.name, "bytes": zip_path.stat().st_size, "uncompressedBytes": total,
            "files": len(members), "sha256": sha256_file(zip_path)}
