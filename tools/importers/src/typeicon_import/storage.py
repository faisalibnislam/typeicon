"""Object storage: local filesystem (default, no credentials) or S3-compatible (R2, MinIO, S3).

Keys are POSIX-style relative paths such as "releases/0.1.0/typeicon-0.1.0-desktop.zip"
or "builds/private/<userId>/<cacheKey>/kit.zip". Keys are validated so a caller can never
escape the storage root.
"""
from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

from .sources import repo_root

KEY_RE = re.compile(r"^[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*$")


def check_key(key: str) -> str:
    if not KEY_RE.match(key) or ".." in key.split("/"):
        raise ValueError(f"invalid storage key {key!r}")
    return key


class FsStorage:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        p = (self.root / check_key(key)).resolve()
        if self.root not in p.parents:
            raise ValueError("storage key escapes root")
        return p

    def put_file(self, key: str, src: Path, content_type: str = "application/octet-stream") -> None:
        dest = self._path(key)
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmp = dest.with_suffix(dest.suffix + ".tmp")
        shutil.copyfile(src, tmp)
        tmp.replace(dest)

    def put_bytes(self, key: str, data: bytes, content_type: str = "application/octet-stream") -> None:
        dest = self._path(key)
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmp = dest.with_suffix(dest.suffix + ".tmp")
        tmp.write_bytes(data)
        tmp.replace(dest)

    def exists(self, key: str) -> bool:
        return self._path(key).exists()

    def get_bytes(self, key: str) -> bytes:
        return self._path(key).read_bytes()


class S3Storage:
    def __init__(self):
        import boto3
        self.bucket = os.environ["S3_BUCKET"]
        self.client = boto3.client(
            "s3",
            endpoint_url=os.environ.get("S3_ENDPOINT") or None,
            region_name=os.environ.get("S3_REGION", "auto"),
            aws_access_key_id=os.environ.get("S3_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("S3_SECRET_ACCESS_KEY"),
        )

    def put_file(self, key: str, src: Path, content_type: str = "application/octet-stream") -> None:
        self.client.upload_file(str(src), self.bucket, check_key(key), ExtraArgs={"ContentType": content_type})

    def put_bytes(self, key: str, data: bytes, content_type: str = "application/octet-stream") -> None:
        self.client.put_object(Bucket=self.bucket, Key=check_key(key), Body=data, ContentType=content_type)

    def exists(self, key: str) -> bool:
        try:
            self.client.head_object(Bucket=self.bucket, Key=check_key(key))
            return True
        except Exception:  # noqa: BLE001 - botocore ClientError 404
            return False

    def get_bytes(self, key: str) -> bytes:
        return self.client.get_object(Bucket=self.bucket, Key=check_key(key))["Body"].read()


def get_storage():
    driver = os.environ.get("STORAGE_DRIVER", "fs")
    if driver == "s3":
        return S3Storage()
    root = Path(os.environ.get("STORAGE_FS_ROOT", ".data/storage"))
    if not root.is_absolute():
        root = repo_root() / root
    return FsStorage(root)


CONTENT_TYPES = {
    ".zip": "application/zip", ".json": "application/json", ".otf": "font/otf", ".ttf": "font/ttf",
    ".woff2": "font/woff2", ".woff": "font/woff", ".css": "text/css; charset=utf-8", ".svg": "image/svg+xml",
}


def content_type_for(name: str) -> str:
    return CONTENT_TYPES.get(Path(name).suffix, "application/octet-stream")
