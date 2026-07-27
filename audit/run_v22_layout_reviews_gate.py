#!/usr/bin/env python3
"""Verify the v22 information-page layout and restored review letters."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from lxml import html
from PIL import Image


BASE = Path(__file__).resolve().parents[1]
SITE = BASE / "site"
OUTPUT = BASE / "audit" / "v22-layout-reviews-gate.json"

EXPECTED_LETTERS = {
    "hydrogeoservice-letter.jpg": "55120f7e7333cf0e04a5d7c6a8aeda4437a038b3a16eed3ff9a6443e940d95f1",
    "bursetstroy-letter.jpg": "e517432cd2dae55bf90d49afc31a4209b807a2f8e043ff1f787e42ef38852942",
    "minskmetrostroy-letter.jpg": "e3dd4b84129c7493f4924d37c77e73879b6671be892f29dbbda67df17bee04f4",
    "proftec-letter.jpg": "fe52aa30addc0af9fd4a7d3627519e663a9e539afe1bec918cfabf574efaa36c",
}


def parse_fragment(path: Path):
    source = path.read_text(encoding="utf-8")
    return source, html.fromstring(f"<div>{source}</div>")


def main() -> int:
    errors: list[str] = []
    checks: dict[str, object] = {}

    for filename in ("about.php", "delivery.php"):
        source, tree = parse_fragment(SITE / filename)
        wide = tree.xpath('.//div[contains(concat(" ", normalize-space(@class), " "), " info-page ")]')
        narrow = tree.xpath('.//div[contains(concat(" ", normalize-space(@class), " "), " pdp-content ")]')
        checks[f"{filename}_wide_container"] = len(wide) == 1 and not narrow
        if not checks[f"{filename}_wide_container"]:
            errors.append(f"{filename} не использует единственный широкий контейнер info-page")
        if 'class="wrap info-page"' not in source:
            errors.append(f"{filename}: отсутствует связка wrap info-page")

    _, delivery_tree = parse_fragment(SITE / "delivery.php")
    order_items = delivery_tree.xpath(
        './/ol[contains(concat(" ", normalize-space(@class), " "), " order-steps ")]/li'
    )
    checks["delivery_order_steps"] = len(order_items) == 3
    if len(order_items) != 3:
        errors.append(f"На странице доставки найдено {len(order_items)} шагов вместо 3")

    index_source, index_tree = parse_fragment(SITE / "index.php")
    reviews = index_tree.xpath('.//section[@id="reviews"]')
    letters = index_tree.xpath('.//section[@id="reviews"]//a[contains(concat(" ", normalize-space(@class), " "), " letter ")]')
    checks["reviews_section"] = len(reviews) == 1
    checks["review_letters"] = len(letters) == 4
    if len(reviews) != 1:
        errors.append("На главной отсутствует единственный раздел #reviews")
    if len(letters) != 4:
        errors.append(f"В разделе отзывов найдено {len(letters)} писем вместо 4")
    if "Строительная организация" in index_source:
        errors.append("На главной остался неподтверждённый анонимный текстовый отзыв")

    image_checks = []
    reviews_dir = SITE / "img" / "reviews"
    for full_name, expected_hash in EXPECTED_LETTERS.items():
        full = reviews_dir / full_name
        thumb = reviews_dir / full_name.replace(".jpg", "-thumb.webp")
        item = {"full": full_name, "thumb": thumb.name}
        if not full.is_file() or not thumb.is_file():
            errors.append(f"Отсутствует оригинал или превью {full_name}")
            item["status"] = "missing"
            image_checks.append(item)
            continue
        digest = hashlib.sha256(full.read_bytes()).hexdigest()
        with Image.open(full) as image:
            full_size = image.size
        with Image.open(thumb) as image:
            thumb_size = image.size
        item.update(
            {
                "status": "passed",
                "original_hash_matches": digest == expected_hash,
                "full_size": full_size,
                "thumb_size": thumb_size,
            }
        )
        if digest != expected_hash:
            errors.append(f"{full_name}: оригинал отличается от архивного письма")
        if full_size != (1654, 2339) or thumb_size != (640, 905):
            errors.append(
                f"{full_name}: неожиданные размеры оригинала {full_size} или превью {thumb_size}"
            )
        image_checks.append(item)

    site_css = (SITE / "css" / "style.css").read_bytes()
    source_css = (BASE / "source" / "css" / "style.css").read_bytes()
    css_text = site_css.decode("utf-8")
    css_requirements = {
        "css_mirror": site_css == source_css,
        "full_wrap": "--wrap: 1180px" in css_text,
        "info_page_rule": ".info-page { max-width: var(--wrap); }" in css_text,
        "three_desktop_steps": "grid-template-columns: repeat(3, minmax(0, 1fr));" in css_text,
        "two_tablet_letters": ".reviews, .letters { grid-template-columns: 1fr 1fr; }" in css_text,
        "one_narrow_letter": ".letters { grid-template-columns: 1fr; }" in css_text,
    }
    checks.update(css_requirements)
    for name, passed in css_requirements.items():
        if not passed:
            errors.append(f"Не пройдена CSS-проверка: {name}")

    footer = (SITE / "inc" / "footer.php").read_text(encoding="utf-8")
    head = (SITE / "inc" / "head.php").read_text(encoding="utf-8")
    checks["reviews_navigation"] = (
        'href="index.php#reviews"' in footer and 'href="index.php#reviews"' in head
    )
    if not checks["reviews_navigation"]:
        errors.append("Ссылка на отзывы отсутствует в мобильной навигации или футере")

    result = {
        "status": "passed" if not errors else "failed",
        "checks": checks,
        "review_images": image_checks,
        "errors": errors,
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
