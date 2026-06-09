#!/usr/bin/env python3
"""
Generate version and meta.json for the resources/ directory.

Scans all files under resources/ (excluding version and meta.json themselves),
computes MD5 hashes and file sizes, then writes:
  - resources/meta.json  (file manifest)
  - resources/version    (aggregate MD5 of all file hashes)

Run this script after modifying any file in resources/.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path, PurePosixPath

REPO_ROOT = Path(__file__).resolve().parent.parent
RESOURCES_DIR = REPO_ROOT / "resources"

EXCLUDED_FILES = {"version", "meta.json"}


def _md5_of_file(file_path: Path) -> str:
    h = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _relative_posix_path(file_path: Path) -> str:
    return str(PurePosixPath(file_path.relative_to(RESOURCES_DIR)))


def main() -> int:
    if not RESOURCES_DIR.is_dir():
        print(f"Error: resources directory not found: {RESOURCES_DIR}", file=sys.stderr)
        return 1

    files_info = []
    for file_path in sorted(RESOURCES_DIR.rglob("*")):
        if not file_path.is_file():
            continue
        rel_path = _relative_posix_path(file_path)
        if rel_path in EXCLUDED_FILES:
            continue
        md5 = _md5_of_file(file_path)
        size = file_path.stat().st_size
        files_info.append({"path": rel_path, "md5": md5, "size": size})

    meta = {"file_count": len(files_info), "files": files_info}
    meta_json = json.dumps(meta, indent=2, ensure_ascii=False) + "\n"

    version_hash = hashlib.md5(
        "".join(f["md5"] for f in files_info).encode()
    ).hexdigest()

    meta_path = RESOURCES_DIR / "meta.json"
    version_path = RESOURCES_DIR / "version"

    meta_path.write_text(meta_json, encoding="utf-8")
    version_path.write_text(version_hash + "\n", encoding="utf-8")

    print(f"Generated meta.json: {len(files_info)} files")
    print(f"Generated version: {version_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
