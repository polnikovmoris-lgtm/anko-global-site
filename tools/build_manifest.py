#!/usr/bin/env python3
"""Build a deterministic SHA-256 manifest for the release directory."""

from __future__ import annotations

import hashlib
from pathlib import Path


root = Path(__file__).resolve().parents[1]
output = root / "FILE-MANIFEST-SHA256.txt"
ignored_parts = {"__pycache__", ".DS_Store"}
paths = sorted(
    path
    for path in root.rglob("*")
    if path.is_file()
    and path != output
    and not any(part in ignored_parts for part in path.parts)
    and path.suffix != ".pyc"
)
lines = []
for path in paths:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    lines.append(f"{digest}  {path.relative_to(root).as_posix()}")
output.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Manifest: {len(paths)} files")
