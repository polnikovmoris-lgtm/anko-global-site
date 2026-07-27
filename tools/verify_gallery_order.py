#!/usr/bin/env python3
"""Verify ANKO gallery order against the original a-line product pages."""

from __future__ import annotations

import argparse
import re
import tempfile
import zipfile
from pathlib import Path


PAGE_MAP = {
    "product-adapter.php": "instrument-adapter.html",
    "product-burovoi-nozh.php": "instrument-burovoi-nozh.html",
    "product-burovoi-pilot.php": "instrument-burovoi-pilot.html",
    "product-kluch-trubnii.php": "instrument-kluch-trubnii.html",
    "product-mufta-startovoy.php": "instrument-mufta-startovoy-shtangi.html",
    "product-nsu.php": "instrument-nsu.html",
    "product-rasshiritel.php": "instrument-rasshiritel.html",
    "product-shtanga-burovaya.php": "instrument-shtanga-burovaya.html",
    "product-shtanga-startovaya.php": "instrument-shtanga-startovaya.html",
    "product-burovie-golovi.php": "instrument-smennie-burovie-golovi.html",
    "product-vertlugi.php": "instrument-vertlugi.html",
    "product-vkladishi-tiskov.php": "instrument-vkladki-tiskov.html",
    "product-vstavki-nozha.php": "instrument-vstavki-nozha.html",
    "product-zahvat-tsangovii.php": "instrument-zahvat-tsangovii.html",
    "product-lokatori-digitrak.php": "lokatsionnie-sistemi-americanskie-lokatori.html",
    "product-lokatori-rf.php": "lokatsionnie-sistemi-russkie-lokatori.html",
    "product-ditchwitch-hdd.php": "ustanovka-ditchwitch-hdd.html",
    "product-fdp-hdd.php": "ustanovka-fdp-hdd.html",
    "product-goodeng-hdd.php": "ustanovka-goodeng-hdd.html",
    "product-igla-20t.php": "ustanovka-igla-20t.html",
    "product-igla-20tvm.php": "ustanovka-igla-20tb.html",
    "product-igla-32t.php": "ustanovka-igla-32t.html",
    "product-vermeer-hdd.php": "ustanovka-vermeer-hdd.html",
    "product-xcmg-hdd.php": "ustanovka-xcmg-hdd.html",
}

THUMB_RE = re.compile(
    r'<img[^>]*class=["\'][^"\']*img-thumbnail[^"\']*["\'][^>]*src=["\']([^"\']+)',
    re.I,
)
ENTRY_RE = re.compile(r"'([^']+\.php)'\s*:\s*\[([^\]]+)\]")
PATH_RE = re.compile(r"'([^']+)'")
RASTER_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".avif"}


def sequence_key(path: str) -> str:
    """Compare gallery identity and order independently of output image format."""
    candidate = Path(path)
    if candidate.suffix.lower() in RASTER_SUFFIXES:
        candidate = candidate.with_suffix("")
    return candidate.as_posix()


def short_source_path(path: str) -> str:
    if "/locator/" in path:
        return "locator/" + path.split("/locator/", 1)[1]
    markers = ("/tools/", "/drill-machines/")
    for marker in markers:
        if marker in path:
            return path.split(marker, 1)[1]
    raise ValueError(f"Unsupported a-line image path: {path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("aline_zip", type=Path)
    parser.add_argument(
        "--site",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "site",
    )
    args = parser.parse_args()

    js_path = args.site / "js" / "product-galleries.js"
    js_text = js_path.read_text(encoding="utf-8")
    actual = {
        page: PATH_RE.findall(values)
        for page, values in ENTRY_RE.findall(js_text)
    }

    failures: list[str] = []
    checked_links = 0
    with tempfile.TemporaryDirectory(prefix="aline-gallery-order-") as temp_dir:
        with zipfile.ZipFile(args.aline_zip) as archive:
            archive.extractall(temp_dir)
        roots = list(Path(temp_dir).glob("**/a-line.by"))
        if len(roots) != 1:
            raise RuntimeError(f"Expected one a-line.by directory, found {len(roots)}")
        source_root = roots[0]

        for anko_page, aline_page in PAGE_MAP.items():
            source_html = (source_root / aline_page).read_text(
                encoding="utf-8", errors="ignore"
            )
            expected = [short_source_path(path) for path in THUMB_RE.findall(source_html)]
            found = actual.get(anko_page)
            if found is None or list(map(sequence_key, found)) != list(
                map(sequence_key, expected)
            ):
                failures.append(
                    f"{anko_page}: expected {expected!r}, found {found!r}"
                )
                continue
            for relative_path in found:
                checked_links += 1
                if not (args.site / "img" / "gallery" / "a-line" / relative_path).is_file():
                    failures.append(f"{anko_page}: missing {relative_path}")

    if failures:
        print("\n".join(failures))
        return 1
    print(
        f"PASS: {len(PAGE_MAP)} galleries, {checked_links} ordered image links, "
        "0 sequence mismatches, 0 missing files"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
