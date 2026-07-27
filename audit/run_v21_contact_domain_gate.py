#!/usr/bin/env python3
"""Static gate for the v21 legal name, email, canonical domain and redirects."""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

from lxml import html


BASE = Path(__file__).resolve().parents[1]
SITE = BASE / "site"
OUTPUT = BASE / "audit" / "v21-contact-domain-gate.json"

COMPANY = "ООО «Анко-глобал»"
EMAIL = "main.accentline@gmail.com"
DOMAIN = "https://ankoglobal.by"
OLD_VALUES = (
    "ООО «АкцентЛайн Групп»",
    "info@a-global.by",
    "info@a-line.by",
    "https://a-global.by",
)

PHP_BLOCK_RE = re.compile(r"<\?(?:php|=).*?\?>", re.I | re.S)
JSON_LD_RE = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.I | re.S,
)
CSS_URL_RE = re.compile(r"url\(\s*([\"']?)(.*?)\1\s*\)", re.I)


def local_target(value: str, source_dir: Path) -> Path | None:
    value = value.strip()
    if not value or value.startswith(("#", "data:", "mailto:", "tel:", "javascript:")):
        return None
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        return None
    path = unquote(parsed.path)
    if not path or "<?" in path or "<" in path:
        return None
    return SITE / path.lstrip("/") if path.startswith("/") else source_dir / path


def all_text_files() -> list[Path]:
    allowed = {".php", ".css", ".js", ".txt", ".xml", ".htaccess", ""}
    return sorted(
        path
        for path in SITE.rglob("*")
        if path.is_file()
        and (path.suffix.lower() in allowed or path.name == ".htaccess")
    )


def main() -> int:
    errors: list[str] = []
    text_files = all_text_files()
    sources = {
        path: path.read_text(encoding="utf-8", errors="replace") for path in text_files
    }
    combined = "\n".join(sources.values())

    old_occurrences: dict[str, list[str]] = {}
    for old in OLD_VALUES:
        files = [str(path.relative_to(SITE)) for path, text in sources.items() if old in text]
        old_occurrences[old] = files
        if files:
            errors.append(f"Старое значение {old!r} найдено в: {', '.join(files)}")

    config = sources[SITE / "inc" / "config.php"]
    required_config = {
        "domain": f"'domain'      => '{DOMAIN}'",
        "company": f"'company'     => '{COMPANY}'",
        "email": f"'email'       => '{EMAIL}'",
    }
    for key, expected in required_config.items():
        if expected not in config:
            errors.append(f"В config.php отсутствует ожидаемое значение {key}: {expected}")

    mailto_values = sorted(
        set(re.findall(r"mailto:([^\"'<>\s]+)", combined, flags=re.I))
    )
    if mailto_values != [EMAIL]:
        errors.append(f"Неожиданные mailto-адреса: {mailto_values}")

    jsonld_blocks = 0
    invalid_jsonld: list[str] = []
    organization_names: set[str] = set()
    for path in sorted(SITE.glob("*.php")):
        source = sources[path]
        for index, block in enumerate(JSON_LD_RE.findall(source), 1):
            jsonld_blocks += 1
            try:
                value = json.loads(block)
            except json.JSONDecodeError as exc:
                invalid_jsonld.append(f"{path.name}#{index}: {exc.msg}")
                continue
            if isinstance(value, dict) and value.get("@type") == "LocalBusiness":
                organization_names.add(str(value.get("alternateName", "")))
    if invalid_jsonld:
        errors.append("Некорректный JSON-LD: " + "; ".join(invalid_jsonld))
    if organization_names != {COMPANY}:
        errors.append(
            "alternateName LocalBusiness не совпадает с юридическим названием: "
            + repr(sorted(organization_names))
        )

    local_references = 0
    missing_references: list[str] = []
    for path in sorted(SITE.glob("*.php")):
        source = PHP_BLOCK_RE.sub("", sources[path])
        try:
            tree = html.fromstring(f"<div>{source}</div>")
        except Exception as exc:
            errors.append(f"HTML-фрагмент {path.name} не разобран: {exc}")
            continue
        for node in tree.xpath(".//*[@href or @src or @srcset]"):
            for attr in ("href", "src"):
                value = node.get(attr)
                if value is None:
                    continue
                target = local_target(value, path.parent)
                if target is None:
                    continue
                local_references += 1
                if not target.is_file():
                    missing_references.append(
                        f"{path.name}: {attr}={value} -> {target.relative_to(SITE)}"
                    )
            srcset = node.get("srcset")
            if srcset:
                for candidate in srcset.split(","):
                    value = candidate.strip().split()[0] if candidate.strip() else ""
                    target = local_target(value, path.parent)
                    if target is None:
                        continue
                    local_references += 1
                    if not target.is_file():
                        missing_references.append(
                            f"{path.name}: srcset={value} -> {target.relative_to(SITE)}"
                        )

    css_path = SITE / "css" / "style.css"
    for _, value in CSS_URL_RE.findall(sources[css_path]):
        target = local_target(value, css_path.parent)
        if target is None:
            continue
        local_references += 1
        if not target.is_file():
            missing_references.append(
                f"css/style.css: url={value} -> {target.relative_to(SITE)}"
            )
    if missing_references:
        errors.append("Отсутствующие локальные ресурсы: " + "; ".join(missing_references))

    sitemap = ET.parse(SITE / "sitemap.xml")
    sitemap_urls = []
    sitemap_image_urls = []
    for node in sitemap.getroot().iter():
        if node.tag.endswith("loc") and node.text:
            value = node.text.strip()
            if "/img/" in value:
                sitemap_image_urls.append(value)
            else:
                sitemap_urls.append(value)
    bad_sitemap_hosts = [
        value
        for value in sitemap_urls + sitemap_image_urls
        if urlsplit(value).scheme != "https"
        or urlsplit(value).netloc != "ankoglobal.by"
    ]
    if bad_sitemap_hosts:
        errors.append("Неканонические URL в Sitemap: " + "; ".join(bad_sitemap_hosts))

    robots = sources[SITE / "robots.txt"]
    if f"Sitemap: {DOMAIN}/sitemap.xml" not in robots:
        errors.append("robots.txt не указывает новый канонический Sitemap")

    htaccess = sources[SITE / ".htaccess"]
    redirect_checks = {
        "old_host_condition": r"\^\(\?:www\\\.\)\?a-line\\\.by\$",
        "old_host_target": f"RewriteRule ^ {DOMAIN}%{{REQUEST_URI}} [R=301,L,NE]",
        "canonical_host_condition": "!^ankoglobal\\.by$",
    }
    redirect_results = {
        "old_host_condition": bool(re.search(redirect_checks["old_host_condition"], htaccess)),
        "old_host_target": redirect_checks["old_host_target"] in htaccess,
        "canonical_host_condition": redirect_checks["canonical_host_condition"]
        in htaccess,
    }
    for key, passed in redirect_results.items():
        if not passed:
            errors.append(f"Не пройдена проверка .htaccess: {key}")

    result = {
        "status": "passed" if not errors else "failed",
        "canonical_domain": DOMAIN,
        "company": COMPANY,
        "email": EMAIL,
        "counts": {
            "php_files": len(list(SITE.rglob("*.php"))),
            "jsonld_blocks": jsonld_blocks,
            "sitemap_urls": len(sitemap_urls),
            "sitemap_image_urls": len(sitemap_image_urls),
            "local_references_checked": local_references,
            "company_occurrences": combined.count(COMPANY),
            "email_occurrences": combined.count(EMAIL),
            "canonical_domain_occurrences": combined.count(DOMAIN),
        },
        "old_occurrences": old_occurrences,
        "mailto_values": mailto_values,
        "organization_alternate_names": sorted(organization_names),
        "redirect_checks": redirect_results,
        "invalid_jsonld": invalid_jsonld,
        "missing_local_references": missing_references,
        "errors": errors,
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
