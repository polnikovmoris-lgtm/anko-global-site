#!/usr/bin/env python3
"""Verify the v25 polymer-category cover without changing the product image."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
WORKSPACE = ROOT.parent
BASELINE = WORKSPACE / "anko-global-v24-2026-07-26" / "site"
OUTPUT = ROOT / "audit" / "v25-polymer-cover-gate.json"

COVER_BASE = "category-cover-polimery"
PRODUCT_BASE = "generated/polymer-polymersplus-vis"
VARIANTS = {
    "-640.webp": (640, 400),
    "-960.webp": (960, 600),
    ".webp": (1280, 800),
    ".jpg": (1280, 800),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    errors: list[str] = []
    checked_assets = 0

    for suffix, expected_size in VARIANTS.items():
        path = SITE / "img" / f"{COVER_BASE}{suffix}"
        if not path.is_file():
            errors.append(f"missing image variant: {path.relative_to(SITE)}")
            continue
        checked_assets += 1
        try:
            with Image.open(path) as image:
                actual_size = (image.width, image.height)
                image.verify()
            if actual_size != expected_size:
                errors.append(
                    f"{path.relative_to(SITE)}: {actual_size} != {expected_size}"
                )
        except Exception as exc:
            errors.append(f"{path.relative_to(SITE)}: invalid image ({exc})")

    catalog = (SITE / "catalog.php").read_text(encoding="utf-8")
    homepage = (SITE / "index.php").read_text(encoding="utf-8")
    category = (SITE / "category-polimer.php").read_text(encoding="utf-8")
    product = (SITE / "product-polymersplus-vis.php").read_text(encoding="utf-8")
    sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8")

    expected_references = {
        "catalog.php": COVER_BASE in catalog,
        "index.php": COVER_BASE in homepage,
        "category-polimer.php": (
            f"$og_image = 'img/{COVER_BASE}.jpg';" in category
        ),
        "sitemap.xml": (
            f"https://ankoglobal.by/img/{COVER_BASE}.jpg" in sitemap
            and "Полимеры и реагенты для бурового раствора ГНБ" in sitemap
        ),
    }
    for name, present in expected_references.items():
        if not present:
            errors.append(f"{name} does not reference the v25 polymer cover")

    if COVER_BASE in product:
        errors.append("product-polymersplus-vis.php incorrectly uses the category cover")
    if PRODUCT_BASE not in product:
        errors.append("product-polymersplus-vis.php lost its product-specific image")

    product_variants_preserved = 0
    for suffix in VARIANTS:
        current = SITE / "img" / f"{PRODUCT_BASE}{suffix}"
        baseline = BASELINE / "img" / f"{PRODUCT_BASE}{suffix}"
        if not current.is_file() or not baseline.is_file():
            errors.append(f"missing product baseline/current variant: {suffix}")
        elif sha256(current) != sha256(baseline):
            errors.append(f"product image changed unexpectedly: {current.name}")
        else:
            product_variants_preserved += 1

    cover_jpg = SITE / "img" / f"{COVER_BASE}.jpg"
    old_product_jpg = BASELINE / "img" / f"{PRODUCT_BASE}.jpg"
    if cover_jpg.is_file() and old_product_jpg.is_file():
        if sha256(cover_jpg) == sha256(old_product_jpg):
            errors.append("new category cover is identical to the old product image")

    v24_archive = WORKSPACE / "anko-global-product-images-2026-07-26-v24.zip"
    expected_v24_sha = (
        "d32006b79551802b38a0f8f47e715ae18476a6948a1a7f247d783dd7ec9164ee"
    )
    actual_v24_sha = sha256(v24_archive) if v24_archive.is_file() else None
    if actual_v24_sha != expected_v24_sha:
        errors.append("the v24 source archive checksum changed")

    report = {
        "status": "passed" if not errors else "failed",
        "cover_variants_checked": checked_assets,
        "expected_cover_variants": len(VARIANTS),
        "cover_dimensions": list(VARIANTS.values()),
        "references": expected_references,
        "product_image_variants_preserved": product_variants_preserved,
        "v24_archive_sha256": actual_v24_sha,
        "v24_archive_preserved": actual_v24_sha == expected_v24_sha,
        "errors": errors,
    }
    OUTPUT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
