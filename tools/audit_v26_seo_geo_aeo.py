#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
OUT = ROOT / 'audit' / 'v26'
DOMAIN = 'https://ankoglobal.by'


def sitemap_entries():
    tree = ET.parse(SITE / 'sitemap.xml')
    root = tree.getroot()
    ns = {
        's': 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'i': 'http://www.google.com/schemas/sitemap-image/1.1',
    }
    result = []
    for u in root.findall('s:url', ns):
        loc = (u.findtext('s:loc', default='', namespaces=ns) or '').strip()
        lastmod = (u.findtext('s:lastmod', default='', namespaces=ns) or '').strip()
        images = [(x.text or '').strip() for x in u.findall('i:image/i:loc', ns) if x.text]
        result.append({'loc': loc, 'lastmod': lastmod, 'images': images})
    return result


def render(path: str) -> str:
    parsed = urlsplit(path)
    filename = parsed.path.lstrip('/') or 'index.php'
    proc = subprocess.run(
        ['php', filename], cwd=SITE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if proc.returncode != 0:
        raise RuntimeError(f'{filename}: {proc.stderr.decode("utf-8", "replace")}')
    return proc.stdout.decode('utf-8', 'replace')


def local_path_for_url(url: str) -> Path | None:
    p = urlsplit(url)
    if p.netloc and p.netloc != 'ankoglobal.by':
        return None
    rel = p.path.lstrip('/')
    if not rel:
        rel = 'index.php'
    target = (SITE / rel).resolve()
    try:
        target.relative_to(SITE.resolve())
    except ValueError:
        return None
    return target


def flatten_jsonld(value, out):
    if isinstance(value, list):
        for x in value:
            flatten_jsonld(x, out)
    elif isinstance(value, dict):
        if '@type' in value:
            typ = value['@type']
            if isinstance(typ, list):
                out.extend(str(x) for x in typ)
            else:
                out.append(str(typ))
        for child in value.values():
            flatten_jsonld(child, out)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    entries = sitemap_entries()
    errors = []
    warnings = []
    pages = []
    all_titles = []
    all_descs = []
    schema_types = Counter()
    missing_alt_total = 0
    local_links_checked = 0
    visible_faq_questions = []
    schema_faq_questions = []

    if len(entries) != 81:
        errors.append(f'sitemap URL count is {len(entries)}, expected 81')
    if len({e['loc'] for e in entries}) != len(entries):
        errors.append('duplicate URLs in sitemap')
    if any(e['lastmod'] != '2026-07-26' for e in entries):
        warnings.append('not all sitemap lastmod values match final release date')

    for entry in entries:
        loc = entry['loc']
        if not loc.startswith(DOMAIN + '/') and loc != DOMAIN:
            errors.append(f'foreign or invalid sitemap URL: {loc}')
            continue
        path = urlsplit(loc).path or '/'
        target = local_path_for_url(loc)
        if target is None or not target.is_file():
            errors.append(f'sitemap target missing: {loc}')
            continue
        try:
            html = render(path)
        except RuntimeError as exc:
            errors.append(str(exc))
            continue
        soup = BeautifulSoup(html, 'lxml')
        title = soup.title.get_text(' ', strip=True) if soup.title else ''
        desc_tag = soup.find('meta', attrs={'name': re.compile('^description$', re.I)})
        desc = (desc_tag.get('content') or '').strip() if desc_tag else ''
        canonical_tag = soup.find('link', rel=lambda value: value and 'canonical' in value)
        canonical = (canonical_tag.get('href') or '').strip() if canonical_tag else ''
        robots_tag = soup.find('meta', attrs={'name': re.compile('^robots$', re.I)})
        robots = (robots_tag.get('content') or '').lower() if robots_tag else ''
        h1s = [x.get_text(' ', strip=True) for x in soup.find_all('h1')]
        imgs = soup.find_all('img')
        missing_alt = [img.get('src', '') for img in imgs if not img.has_attr('alt')]
        missing_alt_total += len(missing_alt)

        jsonld_errors = []
        page_types = []
        jsonld_objects = []
        for node in soup.find_all('script', attrs={'type': 'application/ld+json'}):
            raw = node.string or node.get_text()
            try:
                obj = json.loads(raw)
                jsonld_objects.append(obj)
                flatten_jsonld(obj, page_types)
            except Exception as exc:
                jsonld_errors.append(str(exc))
        schema_types.update(page_types)

        page_errors = []
        page_warnings = []
        if not title:
            page_errors.append('missing title')
        if not desc:
            page_errors.append('missing meta description')
        if canonical != loc:
            page_errors.append(f'canonical mismatch: {canonical!r}')
        if 'noindex' in robots:
            page_errors.append('unexpected noindex')
        if len(h1s) != 1:
            page_errors.append(f'h1 count {len(h1s)}')
        if missing_alt:
            page_errors.append(f'{len(missing_alt)} img elements lack alt attribute')
        if jsonld_errors:
            page_errors.append(f'{len(jsonld_errors)} invalid JSON-LD blocks')
        if not soup.find('meta', property='og:title') or not soup.find('meta', property='og:image'):
            page_errors.append('incomplete Open Graph metadata')
        if not soup.find('meta', attrs={'name': 'twitter:card'}):
            page_errors.append('missing Twitter card metadata')
        if len(title) > 70:
            page_warnings.append(f'long title: {len(title)} characters')
        if len(desc) < 70 or len(desc) > 200:
            page_warnings.append(f'description length: {len(desc)} characters')

        for link in soup.find_all('a', href=True):
            href = (link.get('href') or '').strip()
            if not href or href.startswith(('#', 'tel:', 'mailto:', 'javascript:')):
                continue
            abs_url = urljoin(loc, href)
            parsed = urlsplit(abs_url)
            if parsed.netloc == 'ankoglobal.by':
                local_links_checked += 1
                target_link = local_path_for_url(abs_url)
                if target_link is None or not target_link.is_file():
                    page_errors.append(f'broken internal link: {href}')

        for image_url in entry['images']:
            image_target = local_path_for_url(image_url)
            if image_target is None or not image_target.is_file():
                page_errors.append(f'missing sitemap image: {image_url}')

        if path in ('/', '/index.php'):
            # Compare visible FAQ headings/questions with structured FAQ content.
            for item in soup.select('.faq__question, [data-faq-question], details summary'):
                text = item.get_text(' ', strip=True)
                if text:
                    visible_faq_questions.append(text)
            def collect_faq(obj):
                if isinstance(obj, list):
                    for x in obj: collect_faq(x)
                elif isinstance(obj, dict):
                    if obj.get('@type') == 'FAQPage':
                        for q in obj.get('mainEntity', []):
                            if isinstance(q, dict) and q.get('name'):
                                schema_faq_questions.append(str(q['name']).strip())
                    for v in obj.values():
                        collect_faq(v)
            for obj in jsonld_objects:
                collect_faq(obj)

        all_titles.append(title)
        all_descs.append(desc)
        pages.append({
            'url': loc,
            'title': title,
            'description_length': len(desc),
            'canonical': canonical,
            'h1': h1s,
            'schema_types': sorted(set(page_types)),
            'images': len(imgs),
            'missing_alt': missing_alt,
            'errors': sorted(set(page_errors)),
            'warnings': sorted(set(page_warnings)),
        })
        errors.extend(f'{loc}: {e}' for e in sorted(set(page_errors)))
        warnings.extend(f'{loc}: {w}' for w in sorted(set(page_warnings)))

    duplicate_titles = sorted(k for k, v in Counter(all_titles).items() if k and v > 1)
    duplicate_descs = sorted(k for k, v in Counter(all_descs).items() if k and v > 1)
    if duplicate_titles:
        errors.append(f'duplicate titles: {duplicate_titles}')
    if duplicate_descs:
        errors.append(f'duplicate descriptions: {duplicate_descs}')

    robots = (SITE / 'robots.txt').read_text(encoding='utf-8')
    required_bots = ['OAI-SearchBot', 'ChatGPT-User', 'GPTBot', 'PerplexityBot', 'ClaudeBot', 'Google-Extended']
    missing_bots = [x for x in required_bots if f'User-agent: {x}' not in robots]
    if missing_bots:
        errors.append('missing explicit AI crawler directives: ' + ', '.join(missing_bots))
    if 'Sitemap: https://ankoglobal.by/sitemap.xml' not in robots:
        errors.append('robots.txt does not reference production sitemap')
    if 'Disallow: /send.php' not in robots or 'Disallow: /thanks.php' not in robots:
        errors.append('service endpoints are not excluded from crawling')

    required_schema = {
        'BreadcrumbList': 80,
        'Product': 68,
        'CollectionPage': 9,
        'ItemList': 9,
        'LocalBusiness': 2,
        'FAQPage': 1,
        'WebSite': 1,
    }
    for typ, minimum in required_schema.items():
        if schema_types[typ] < minimum:
            errors.append(f'schema type {typ}: {schema_types[typ]}, expected at least {minimum}')

    if sorted(visible_faq_questions) != sorted(schema_faq_questions):
        errors.append('FAQPage structured questions do not match visible FAQ questions')

    product_pages = [p for p in pages if 'Product' in p['schema_types']]
    products_with_offer = sum('Offer' in p['schema_types'] for p in product_pages)
    product_note = (
        'Product identity markup is present on all product pages. Offer markup was intentionally not fabricated '
        'because the site uses request-based pricing; rich-result eligibility should be revisited when real public '
        'price, currency, availability and offer URLs are available.'
    )

    result = {
        'status': 'passed' if not errors else 'failed',
        'scope': 'pre-deployment static/rendered audit',
        'sitemap_urls': len(entries),
        'pages_rendered': len(pages),
        'unique_titles': len(set(all_titles)),
        'unique_descriptions': len(set(all_descs)),
        'local_links_checked': local_links_checked,
        'images_missing_alt_attribute': missing_alt_total,
        'schema_blocks_by_type': dict(sorted(schema_types.items())),
        'product_pages': len(product_pages),
        'product_pages_with_offer_schema': products_with_offer,
        'faq_visible_questions': len(visible_faq_questions),
        'faq_schema_questions': len(schema_faq_questions),
        'ai_crawlers_explicitly_allowed': required_bots,
        'technical_baselines': {
            'seo': not errors,
            'ai_search': not errors,
            'geo': not errors,
            'aeo': not errors,
        },
        'limitations': [
            product_note,
            'Live HTTPS, response headers, CDN/WAF crawler access, form delivery and actual indexing cannot be validated until deployment.',
            'Search Console, Bing Webmaster Tools, Bing Places and IndexNow require post-deployment ownership/configuration.',
        ],
        'errors': errors,
        'warnings': warnings,
        'pages': pages,
    }
    out = OUT / 'seo-ai-geo-aeo-audit-v26.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in (
        'status','sitemap_urls','pages_rendered','unique_titles','unique_descriptions',
        'local_links_checked','images_missing_alt_attribute','schema_blocks_by_type',
        'product_pages','product_pages_with_offer_schema','faq_visible_questions',
        'faq_schema_questions','errors','warnings')}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == '__main__':
    main()
