#!/usr/bin/env python3
"""Static release gate for the ANKO GLOBAL deployable site directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit

from PIL import Image


ATTR_RE = re.compile(r"""(?:href|src)=["']([^"'<>]+)["']""", re.I)
SRCSET_RE = re.compile(r"""srcset=["']([^"']+)["']""", re.I)
CSS_URL_RE = re.compile(r"""url\(\s*["']?([^"')]+)""", re.I)
JSON_LD_RE = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.I | re.S,
)
CANONICAL_RE = re.compile(r"""\$canonical\s*=\s*["']([^"']+)["']""")
PRODUCT_H1_RE = re.compile(r'<h1[^>]+class=["\'][^"\']*\bpdp__title\b[^"\']*["\']', re.I)
SEARCH_INDEX_RE = re.compile(r"var INDEX_DATA = (\[.*?\]);", re.S)
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
SKIP_PREFIXES = ("#", "tel:", "mailto:", "data:", "javascript:", "//")


def local_target(raw: str, source: Path, site: Path) -> Path | None:
    value = raw.strip()
    if not value or value.startswith(SKIP_PREFIXES):
        return None
    parsed = urlsplit(value)
    if parsed.scheme in {"http", "https"}:
        return None
    path = parsed.path
    if not path:
        return None
    if path.startswith("/"):
        return site / path.lstrip("/")
    return source.parent / path


def extract_references(path: Path, site: Path) -> list[tuple[str, Path]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    values = ATTR_RE.findall(text)
    for srcset in SRCSET_RE.findall(text):
        values.extend(item.strip().split()[0] for item in srcset.split(",") if item.strip())
    if path.suffix == ".css":
        values.extend(CSS_URL_RE.findall(text))
    refs: list[tuple[str, Path]] = []
    for raw in values:
        target = local_target(raw, path, site)
        if target is not None:
            refs.append((raw, target))
    return refs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("site", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    site = args.site.resolve()

    errors: list[str] = []
    warnings: list[str] = []
    php_files = sorted(site.glob("*.php"))
    product_files = sorted(site.glob("product-*.php"))
    redirects = {
        path
        for path in product_files
        if re.search(r"header\(\s*['\"]Location:", path.read_text(encoding="utf-8"))
    }
    canonical_products = [path for path in product_files if path not in redirects]
    categories = sorted(site.glob("category-*.php"))

    # PHP delimiter sanity and required product structure.
    canonicals: dict[str, str] = {}
    for path in php_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        opens = len(re.findall(r"<\?(?:php|=)", text, re.I))
        closes = text.count("?>")
        if opens not in {closes, closes + 1}:
            errors.append(f"{path.name}: unbalanced PHP delimiters ({opens}/{closes})")
        canonical = CANONICAL_RE.search(text)
        if canonical:
            canonicals[path.name] = canonical.group(1)
            if canonical.group(1) != path.name and path.name != "index.php":
                errors.append(
                    f"{path.name}: canonical points to {canonical.group(1)}"
                )
        if path in canonical_products and not PRODUCT_H1_RE.search(text):
            errors.append(f"{path.name}: missing product h1")

        for block in JSON_LD_RE.findall(text):
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                errors.append(f"{path.name}: invalid JSON-LD ({exc.msg})")

    # Local HTML/CSS asset references.
    checked_references = 0
    missing_references: list[str] = []
    for path in sorted(
        [*site.glob("*.php"), *site.glob("*.html"), *site.rglob("*.css")]
    ):
        for raw, target in extract_references(path, site):
            checked_references += 1
            if not target.exists():
                missing_references.append(
                    f"{path.relative_to(site)} -> {raw}"
                )
    errors.extend(f"missing local reference: {item}" for item in missing_references)

    # Gallery paths are defined in JavaScript rather than HTML attributes.
    gallery_js = site / "js" / "product-galleries.js"
    gallery_paths = []
    if gallery_js.exists():
        gallery_paths = re.findall(
            r"['\"]([^'\"]+\.(?:jpe?g|png|webp|gif))['\"]",
            gallery_js.read_text(encoding="utf-8"),
            re.I,
        )
        for raw in gallery_paths:
            checked_references += 1
            if not (site / "img" / "gallery" / "a-line" / raw).is_file():
                errors.append(f"missing gallery image: {raw}")

    # Decode every raster image.
    image_files = sorted(
        path
        for path in site.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )
    image_failures = []
    for path in image_files:
        try:
            with Image.open(path) as image:
                image.verify()
            with Image.open(path) as image:
                if image.width < 1 or image.height < 1:
                    raise ValueError("zero-sized image")
        except Exception as exc:  # Pillow raises format-specific exceptions.
            image_failures.append(f"{path.relative_to(site)}: {exc}")
    errors.extend(f"invalid image: {item}" for item in image_failures)

    # Sitemap must be valid, unique, and cover every canonical category/product.
    sitemap_path = site / "sitemap.xml"
    sitemap_urls: list[str] = []
    if sitemap_path.exists():
        try:
            root = ET.parse(sitemap_path).getroot()
            ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            sitemap_urls = [
                node.text.strip()
                for node in root.findall("sm:url/sm:loc", ns)
                if node.text
            ]
        except ET.ParseError as exc:
            errors.append(f"sitemap.xml: {exc}")
    else:
        errors.append("sitemap.xml: missing")
    duplicates = [url for url, count in Counter(sitemap_urls).items() if count > 1]
    errors.extend(f"sitemap.xml: duplicate URL {url}" for url in duplicates)
    sitemap_paths = {urlsplit(url).path.rsplit("/", 1)[-1] or "index.php" for url in sitemap_urls}
    for path in [*categories, *canonical_products]:
        if path.name not in sitemap_paths:
            errors.append(f"sitemap.xml: missing {path.name}")
    for path in redirects:
        if path.name in sitemap_paths:
            errors.append(f"sitemap.xml: redirect URL included {path.name}")

    # Search index must be valid and contain every category/product exactly once.
    search_path = site / "js" / "search.js"
    search_items: list[dict] = []
    if search_path.exists():
        match = SEARCH_INDEX_RE.search(search_path.read_text(encoding="utf-8"))
        if match:
            try:
                search_items = json.loads(match.group(1))
            except json.JSONDecodeError as exc:
                errors.append(f"search.js: invalid index ({exc.msg})")
        else:
            errors.append("search.js: INDEX_DATA not found")
    else:
        errors.append("search.js: missing")
    search_urls = [item.get("u") for item in search_items]
    for path in [*categories, *canonical_products]:
        count = search_urls.count(path.name)
        if count != 1:
            errors.append(f"search.js: {path.name} occurs {count} times")
    for path in redirects:
        if path.name in search_urls:
            errors.append(f"search.js: redirect indexed {path.name}")

    # Catch accidental duplicate product source pages.
    hashes: defaultdict[str, list[str]] = defaultdict(list)
    for path in canonical_products:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        hashes[digest].append(path.name)
    duplicate_pages = [names for names in hashes.values() if len(names) > 1]
    errors.extend(f"duplicate product pages: {', '.join(names)}" for names in duplicate_pages)

    # Lightweight CSS delimiter check (comments removed first).
    css_files = sorted(site.rglob("*.css"))
    for path in css_files:
        text = re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.S)
        if text.count("{") != text.count("}"):
            errors.append(f"{path.relative_to(site)}: unbalanced CSS braces")

    report = {
        "status": "passed" if not errors else "failed",
        "php_files": len(php_files),
        "canonical_product_pages": len(canonical_products),
        "redirect_pages": len(redirects),
        "category_pages": len(categories),
        "search_items": len(search_items),
        "sitemap_urls": len(sitemap_urls),
        "local_references_checked": checked_references,
        "gallery_links_checked": len(gallery_paths),
        "images_decoded": len(image_files),
        "json_ld_blocks_checked": sum(
            len(JSON_LD_RE.findall(path.read_text(encoding="utf-8", errors="replace")))
            for path in php_files
        ),
        "duplicate_product_groups": len(duplicate_pages),
        "errors": errors,
        "warnings": warnings,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
