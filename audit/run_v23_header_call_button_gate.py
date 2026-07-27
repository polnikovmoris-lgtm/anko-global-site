#!/usr/bin/env python3
"""Verify the v23 header call-button size, color, scope and cache version."""

from __future__ import annotations

import json
import re
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
SITE = BASE / "site"
OUTPUT = BASE / "audit" / "v23-header-call-button-gate.json"


def luminance(hex_color: str) -> float:
    channels = [int(hex_color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        channel / 12.92
        if channel <= 0.04045
        else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_with_white(hex_color: str) -> float:
    return 1.05 / (luminance(hex_color) + 0.05)


def main() -> int:
    site_css = (SITE / "css" / "style.css").read_text(encoding="utf-8")
    source_css = (BASE / "source" / "css" / "style.css").read_text(encoding="utf-8")
    head = (SITE / "inc" / "head.php").read_text(encoding="utf-8")

    rule_match = re.search(
        r"\.header__right \.btn--call\s*\{(?P<body>.*?)\}",
        site_css,
        flags=re.DOTALL,
    )
    rule = rule_match.group("body") if rule_match else ""
    base_call_match = re.search(
        r"(?m)^\.btn--call\s*\{(?P<body>.*?)\}",
        site_css,
        flags=re.DOTALL,
    )
    base_call_rule = base_call_match.group("body") if base_call_match else ""
    color = "#3D825F"
    contrast = contrast_with_white(color)

    checks = {
        "site_source_css_identical": site_css == source_css,
        "header_rule_present": bool(rule_match),
        "height_48": "min-height: 48px" in rule,
        "font_16": "font-size: 16px" in rule,
        "padding_12_20": "padding: 12px 20px" in rule,
        "gap_8": "gap: 8px" in rule,
        "reference_color_exact": f"--header-call: {color}" in site_css,
        "header_uses_reference_color": "background: var(--header-call)" in rule,
        "base_call_remains_dark": "background: var(--ink)" in base_call_rule,
        "mobile_touch_target_48": (
            "min-width: 48px" in site_css
            and ".btn--call.btn--icon-mobile" in site_css
        ),
        "white_text_contrast_aa": contrast >= 4.5,
        "css_cache_v23": "css/style.css?v=20260726-v23" in head,
    }
    errors = [name for name, passed in checks.items() if not passed]
    result = {
        "status": "passed" if not errors else "failed",
        "reference_color": color,
        "white_text_contrast_ratio": round(contrast, 2),
        "checks": checks,
        "errors": errors,
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
