#!/usr/bin/env python3
"""Verify the v24 category-cover and product-image integration."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
WORKSPACE = ROOT.parent
BASELINE = WORKSPACE / "anko-global-v23-2026-07-26" / "site"
OUTPUT = ROOT / "audit" / "v24-product-images-gate.json"

COVERS = {
    "category-cover-ustanovki": "category-ustanovki.php",
    "category-cover-smazki": "category-smazki.php",
    "category-cover-lokacia": "category-lokacia.php",
    "category-cover-normet": "category-normet.php",
}

PRODUCTS = [
    ("product-normet-geotek", "category-normet.php", "product-normet-geotek.php"),
    ("product-normet-tamacryl", "category-normet.php", "product-normet-tamacryl.php"),
    ("product-normet-tamcem", "category-normet.php", "product-normet-tamcem.php"),
    ("product-normet-tamcrete", "category-normet.php", "product-normet-tamcrete.php"),
    ("product-normet-tamgrease", "category-normet.php", "product-normet-tamgrease.php"),
    ("product-normet-tampur", "category-normet.php", "product-normet-tampur.php"),
    ("product-normet-tamrez", "category-normet.php", "product-normet-tamrez.php"),
    ("product-normet-tamseal", "category-normet.php", "product-normet-tamseal.php"),
    ("product-normet-tamshot", "category-normet.php", "product-normet-tamshot.php"),
    ("product-normet-tamsil", "category-normet.php", "product-normet-tamsil.php"),
    ("product-normet-tamsoil", "category-normet.php", "product-normet-tamsoil.php"),
    ("product-smazka-vermeer", "category-smazki.php", "product-smazka-vermeer.php"),
    ("product-smazka-jet-lube", "category-smazki.php", "product-smazka-jet-lube.php"),
    ("product-smazka-ditchwitch", "category-smazki.php", "product-smazka-ditchwitch.php"),
    ("product-smazka-rf", "category-smazki.php", "product-smazka-rf.php"),
    ("product-lokatori-digitrak", "category-lokacia.php", "product-lokatori-digitrak.php"),
    ("product-lokatori-rf", "category-lokacia.php", "product-lokatori-rf.php"),
    ("product-zondi", "category-lokacia.php", "product-zondi.php"),
]

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
    all_bases = [*COVERS, *(base for base, _, _ in PRODUCTS)]
    checked_assets = 0

    for base in all_bases:
        for suffix, expected_size in VARIANTS.items():
            path = SITE / "img" / f"{base}{suffix}"
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
    sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8")
    for base, category_file in COVERS.items():
        category = (SITE / category_file).read_text(encoding="utf-8")
        if base not in catalog:
            errors.append(f"catalog.php does not reference {base}")
        if f"$og_image = 'img/{base}.jpg';" not in category:
            errors.append(f"{category_file} does not use {base} as Open Graph image")
        if f"https://ankoglobal.by/img/{base}.jpg" not in sitemap:
            errors.append(f"sitemap.xml does not reference {base}")
    if "category-cover-ustanovki" not in homepage:
        errors.append("index.php does not use the drilling-rig redraw")

    changed_product_jpgs = 0
    captioned_product_pages = 0
    for base, category_file, product_file in PRODUCTS:
        category = (SITE / category_file).read_text(encoding="utf-8")
        product = (SITE / product_file).read_text(encoding="utf-8")
        if base not in category:
            errors.append(f"{category_file} does not reference {base}")
        if base not in product:
            errors.append(f"{product_file} does not reference {base}")
        if "table-note" not in product:
            errors.append(f"{product_file} lacks an image clarification")
        else:
            captioned_product_pages += 1

        current = SITE / "img" / f"{base}.jpg"
        baseline = BASELINE / "img" / f"{base}.jpg"
        if not baseline.is_file():
            errors.append(f"v23 baseline image is missing: {baseline.name}")
        elif sha256(current) == sha256(baseline):
            errors.append(f"{base}.jpg was not changed from v23")
        else:
            changed_product_jpgs += 1

    overlay_references = []
    for path in [*SITE.glob("*.php"), SITE / "css" / "style.css"]:
        if "normet-logo-badge" in path.read_text(encoding="utf-8", errors="replace"):
            overlay_references.append(path.relative_to(SITE).as_posix())
    if overlay_references:
        errors.append(f"obsolete Normet overlays remain: {overlay_references}")

    archive = WORKSPACE / "anko-global-header-call-button-2026-07-26-v23.zip"
    expected_v23_sha = "675f4913edd35bf4234bc99e0fd699a6134cdf1f26009a4f613b69c2ef70c6e0"
    actual_v23_sha = sha256(archive) if archive.is_file() else None
    if actual_v23_sha != expected_v23_sha:
        errors.append("the v23 source archive checksum changed")

    report = {
        "status": "passed" if not errors else "failed",
        "category_covers": len(COVERS),
        "product_images": len(PRODUCTS),
        "adaptive_assets_checked": checked_assets,
        "expected_adaptive_assets": len(all_bases) * len(VARIANTS),
        "product_jpgs_changed_from_v23": changed_product_jpgs,
        "product_pages_with_image_clarification": captioned_product_pages,
        "obsolete_normet_overlay_references": overlay_references,
        "v23_archive_sha256": actual_v23_sha,
        "v23_archive_preserved": actual_v23_sha == expected_v23_sha,
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
