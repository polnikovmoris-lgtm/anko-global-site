#!/usr/bin/env python3
"""Static pre-release gate for responsive, accessibility and form safeguards."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


VIEWPORTS = [320, 375, 390, 768, 1024, 1440, 1920]
REQUIRED_BREAKPOINTS = [380, 420, 560, 620, 700, 900, 1000, 1024, 1180, 1499]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("site", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    site = args.site.resolve()
    css = (site / "css/style.css").read_text(encoding="utf-8")
    head = (site / "inc/head.php").read_text(encoding="utf-8")
    footer = (site / "inc/footer.php").read_text(encoding="utf-8")
    main_js = (site / "js/main.js").read_text(encoding="utf-8")
    gallery_js = (site / "js/product-galleries.js").read_text(encoding="utf-8")
    send = (site / "send.php").read_text(encoding="utf-8")
    robots = (site / "robots.txt").read_text(encoding="utf-8")
    page_texts = {
        path.name: path.read_text(encoding="utf-8", errors="replace")
        for path in sorted(site.glob("*.php"))
    }

    errors: list[str] = []
    warnings: list[str] = []

    breakpoints = sorted(
        {
            int(value)
            for value in re.findall(r"@media\s*\(\s*max-width:\s*(\d+)px\s*\)", css)
        }
    )
    missing_breakpoints = [value for value in REQUIRED_BREAKPOINTS if value not in breakpoints]
    if missing_breakpoints:
        errors.append(f"CSS is missing expected breakpoints: {missing_breakpoints}")

    viewport_regimes = {}
    for width in VIEWPORTS:
        viewport_regimes[str(width)] = [
            breakpoint for breakpoint in breakpoints if width <= breakpoint
        ]

    required_css_checks = {
        "fluid_container": ".wrap { max-width: var(--wrap);" in css
        and "width: 100%;" in css,
        "mobile_single_column": (
            ".categories, .categories--catalog, .products, .steps { grid-template-columns: 1fr; }"
            in css
        ),
        "pdp_stacks_at_1000": ".pdp { grid-template-columns: 1fr;" in css,
        "mobile_gallery_scroll": "scroll-snap-type: x proximity" in css,
        "mobile_table_wrap": ".spec-table td," in css
        and "overflow-wrap: anywhere" in css,
        "rig_tables_scroll": ".table-scroll { overflow-x: auto;" in css
        and ".spec-table--rigs { min-width: 720px;" in css,
        "narrow_phone_wrap": ".buybox__phone" in css
        and "overflow-wrap: anywhere" in css,
        "safe_area_callbar": "env(safe-area-inset-bottom)" in css,
        "reduced_motion": "@media (prefers-reduced-motion: reduce)" in css,
    }
    errors.extend(
        f"responsive CSS check failed: {name}"
        for name, passed in required_css_checks.items()
        if not passed
    )

    if 'name="viewport" content="width=device-width, initial-scale=1"' not in head:
        errors.append("responsive viewport meta is missing")

    source_tags = []
    for name, text in page_texts.items():
        for tag in re.findall(r"<source\b[^>]*>", text, re.I):
            source_tags.append((name, tag))
    sources_without_sizes = [
        name for name, tag in source_tags if not re.search(r"\bsizes=", tag, re.I)
    ]
    if sources_without_sizes:
        errors.append(
            f"{len(sources_without_sizes)} responsive source tags lack sizes"
        )

    rig_table_pages = [
        name
        for name, text in page_texts.items()
        if "spec-table--rigs" in text and "table-scroll" not in text
    ]
    if rig_table_pages:
        errors.append(f"wide rig tables lack scroll wrappers: {rig_table_pages}")

    forms = []
    for name, text in {**page_texts, "inc/footer.php": footer}.items():
        for form in re.findall(
            r'<form\b[^>]*data-lead-form[^>]*>(.*?)</form>', text, re.I | re.S
        ):
            checks = {
                "phone": bool(re.search(r'name=["\']phone["\']', form, re.I)),
                "phone_inputmode": bool(re.search(r'inputmode=["\']tel["\']', form, re.I)),
                "phone_minlength": bool(re.search(r'minlength=["\']7["\']', form, re.I)),
                "csrf": bool(re.search(r'name=["\']csrf["\']', form, re.I)),
                "honeypot": bool(re.search(r'name=["\']company["\']', form, re.I)),
                "consent": bool(re.search(r'name=["\']consent["\']', form, re.I)),
                "live_status": "data-form-status" in form
                and 'aria-live="assertive"' in form,
            }
            forms.append({"source": name, "checks": checks})
            for check, passed in checks.items():
                if not passed:
                    errors.append(f"{name}: lead form check failed: {check}")

    security_checks = {
        "post_only": "REQUEST_METHOD" in send and "respond(405" in send,
        "request_size_limit": "CONTENT_LENGTH" in send and "respond(413" in send,
        "csrf_server_validation": "hash_equals" in send and "respond(419" in send,
        "consent_server_validation": "$consentAccepted" in send
        and "respond(422" in send,
        "honeypot": "Honeypot" in send,
        "phone_server_validation": "strlen($digits) < 7" in send,
        "atomic_rate_limit": "flock($rateHandle, LOCK_EX)" in send
        and "ftruncate($rateHandle, 0)" in send,
        "five_per_hour_limit": "count($attempts) >= 5" in send,
        "safe_mail_configuration": "FILTER_VALIDATE_EMAIL" in send,
        "no_store_response": "Cache-Control: no-store" in send,
        "staged_csp": "Content-Security-Policy-Report-Only" in head
        and "CSP_ENFORCE" in head
        and "'nonce-" in head,
    }
    errors.extend(
        f"form/security check failed: {name}"
        for name, passed in security_checks.items()
        if not passed
    )

    accessibility_checks = {
        "skip_link_focus": "mainContent.focus()" in main_js,
        "focus_visible": ":focus-visible" in css,
        "minimum_button_height": ".btn {" in css and "min-height: 56px;" in css,
        "burger_48_square": "min-width: 48px; min-height: 48px;" in css,
        "modal_inert_background": "child.inert = true" in main_js,
        "modal_focus_return": "kpLastOpener" in main_js
        and "kpLastOpener.focus()" in main_js,
        "form_live_region": 'aria-live="assertive"' in footer,
        "gallery_buttons": "aria-pressed" in gallery_js
        and "role', 'group'" in gallery_js,
        "gallery_keyboard": "ArrowLeft" in gallery_js and "ArrowRight" in gallery_js,
        "reduced_motion": "prefers-reduced-motion" in css,
    }
    errors.extend(
        f"accessibility check failed: {name}"
        for name, passed in accessibility_checks.items()
        if not passed
    )

    ai_rules = {}
    for bot in (
        "GPTBot",
        "OAI-SearchBot",
        "ChatGPT-User",
        "Google-Extended",
        "ClaudeBot",
        "PerplexityBot",
    ):
        ai_rules[bot] = bool(
            re.search(
                rf"User-agent:\s*{re.escape(bot)}\s*(?:\r?\n)+Allow:\s*/",
                robots,
                re.I,
            )
        )
    if not ai_rules["ChatGPT-User"]:
        warnings.append(
            "ChatGPT-User has no explicit group; owner decision is required before changing AI crawler policy"
        )

    report = {
        "status": "passed" if not errors else "failed",
        "scope": "static pre-release checks; no browser rendering or server execution",
        "viewports_reviewed": VIEWPORTS,
        "css_breakpoints": breakpoints,
        "viewport_css_regimes": viewport_regimes,
        "responsive_checks": required_css_checks,
        "responsive_source_tags": len(source_tags),
        "responsive_sources_without_sizes": len(sources_without_sizes),
        "lead_forms_checked": forms,
        "security_checks": security_checks,
        "accessibility_checks": accessibility_checks,
        "ai_crawler_rules_unchanged": ai_rules,
        "requires_public_https": [
            "real-browser layout and interaction at all seven viewports",
            "HTTP status, redirects, headers, HSTS and enforced CSP",
            "mail delivery and Telegram integration",
            "Lighthouse, TTFB and Core Web Vitals",
            "Google, Yandex, Bing and AI crawler fetchability",
        ],
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
