#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import json
import mimetypes
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
OUT = ROOT / 'audit' / 'v26'
ORIGIN = 'https://ankoglobal.local/'
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg'}
PLACEHOLDER_SVG = b'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="800" viewBox="0 0 1280 800"><rect width="1280" height="800" fill="#eef1ec"/></svg>'
RENDER_CACHE = {}
VIEWPORTS = [(320, 900), (1440, 1000)]


def sitemap_paths() -> list[str]:
    root = ET.parse(SITE / 'sitemap.xml').getroot()
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    paths = []
    for node in root.findall('s:url/s:loc', ns):
        if not node.text:
            continue
        path = urlsplit(node.text.strip()).path or '/index.php'
        if path == '/':
            path = '/index.php'
        paths.append(path)
    return paths


def render_php(path: str) -> str:
    if path in RENDER_CACHE:
        return RENDER_CACHE[path]
    filename = path.lstrip('/') or 'index.php'
    proc = subprocess.run(
        ['php', filename],
        cwd=SITE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f'{filename}: PHP render failed: {proc.stderr.decode("utf-8", "replace")}')
    html = proc.stdout.decode('utf-8', 'replace')
    # A base URL lets the browser request real local assets; Playwright fulfills them from disk.
    html = html.replace('<head>', f'<head><base href="{ORIGIN}">', 1)
    # The production gallery identifies the page from location.pathname. set_content stays on about:blank,
    # so provide an audit-only equivalent without changing production code.
    current = filename.replace('\\', '/').split('/')[-1]
    html = html.replace('</head>', f'<script>window.__ANKO_AUDIT_PAGE__={json.dumps(current)};</script></head>', 1)
    RENDER_CACHE[path] = html
    return html


def make_route_assets(full_images: bool):
    async def route_assets(route):
        parsed = urlsplit(route.request.url)
        if parsed.netloc != 'ankoglobal.local':
            await route.abort()
            return
        rel = unquote(parsed.path.lstrip('/'))
        target = (SITE / rel).resolve()
        try:
            target.relative_to(SITE.resolve())
        except ValueError:
            await route.fulfill(status=403, body='forbidden')
            return
        if not target.is_file():
            await route.fulfill(status=404, body='not found')
            return
        if not full_images and target.suffix.lower() in IMAGE_EXTS:
            await route.fulfill(status=200, body=PLACEHOLDER_SVG, content_type='image/svg+xml')
            return
        body = target.read_bytes()
        mime = mimetypes.guess_type(target.name)[0] or 'application/octet-stream'
        if target.name == 'product-galleries.js':
            text = body.decode('utf-8')
            text = text.replace(
                "var page = window.location.pathname.split('/').pop() || '';",
                "var page = window.__ANKO_AUDIT_PAGE__ || window.location.pathname.split('/').pop() || '';",
            )
            body = text.encode('utf-8')
            mime = 'application/javascript'
        await route.fulfill(status=200, body=body, content_type=mime)
    return route_assets


async def load_rendered(page, path: str):
    html = render_php(path)
    await page.set_content(html, wait_until='domcontentloaded', timeout=10000)
    await page.wait_for_timeout(60)


async def scroll_lazy(page):
    await page.evaluate('''async () => {
      const delay = ms => new Promise(r => setTimeout(r, ms));
      const max = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
      for (let y = 0; y < max; y += Math.max(350, window.innerHeight * 0.75)) {
        window.scrollTo(0, y);
        await delay(1);
      }
      window.scrollTo(0, max);
      await delay(20);
      window.scrollTo(0, 0);
      await delay(5);
    }''')


async def audit_page(page, path: str, width: int, height: int) -> dict:
    errors = []
    console_errors = []
    page_errors = []

    def on_console(msg):
        if msg.type == 'error':
            console_errors.append(msg.text)

    def on_page_error(exc):
        page_errors.append(str(exc))

    page.on('console', on_console)
    page.on('pageerror', on_page_error)
    status = 200
    metrics = {}
    try:
        await load_rendered(page, path)
        await scroll_lazy(page)
        metrics = await page.evaluate('''() => {
          const de = document.documentElement;
          const body = document.body;
          const imgs = [...document.images];
          return {
            title: document.title.trim(),
            h1: document.querySelectorAll('h1').length,
            scrollWidth: Math.max(de.scrollWidth, body ? body.scrollWidth : 0),
            viewportWidth: window.innerWidth,
            brokenImages: imgs.filter(img => img.complete && img.naturalWidth === 0 && !img.classList.contains('analytics-pixel')).map(img => img.getAttribute('src')),
            bodyText: body ? body.innerText.trim().length : 0,
          };
        }''')
        if not metrics['title']:
            errors.append('empty title')
        if metrics['h1'] != 1:
            errors.append(f"h1 count {metrics['h1']}")
        if metrics['scrollWidth'] > metrics['viewportWidth'] + 1:
            errors.append(f"horizontal overflow {metrics['scrollWidth']}>{metrics['viewportWidth']}")
        if metrics['brokenImages']:
            errors.append('broken images: ' + ', '.join(str(x) for x in metrics['brokenImages'][:5]))
        if metrics['bodyText'] < 80:
            errors.append(f"too little body text {metrics['bodyText']}")
    except (PlaywrightTimeoutError, RuntimeError) as exc:
        errors.append(str(exc))
        status = None
    finally:
        page.remove_listener('console', on_console)
        page.remove_listener('pageerror', on_page_error)

    if console_errors:
        errors.extend('console: ' + item for item in console_errors)
    if page_errors:
        errors.extend('pageerror: ' + item for item in page_errors)
    return {'path': path, 'viewport': [width, height], 'status': status, 'metrics': metrics, 'errors': errors}


async def new_page(browser, width, height, full_images=False):
    page = await browser.new_page(viewport={'width': width, 'height': height}, device_scale_factor=1)
    await page.route('**/*', make_route_assets(full_images))
    return page


async def targeted_checks(browser) -> dict:
    result = {}

    page = await new_page(browser, 320, 900, full_images=True)
    await load_rendered(page, '/product-burovoi-nozh.php')
    phone = await page.locator('.buybox__phone').evaluate('''el => {
      const r = el.getBoundingClientRect();
      const p = el.closest('.buybox').getBoundingClientRect();
      const cs = getComputedStyle(el);
      return {
        whiteSpace: cs.whiteSpace,
        left: r.left, right: r.right, top: r.top, bottom: r.bottom,
        parentLeft: p.left, parentRight: p.right,
        rectCount: el.getClientRects().length,
        documentWidth: document.documentElement.scrollWidth,
        viewportWidth: innerWidth
      };
    }''')
    result['mobile_phone'] = {
        'passed': phone['whiteSpace'] == 'nowrap' and phone['right'] <= phone['parentRight'] + 1 and phone['left'] >= phone['parentLeft'] - 1 and phone['documentWidth'] <= phone['viewportWidth'] + 1,
        'metrics': phone,
    }
    await page.screenshot(path=str(OUT / 'mobile-product-phone-320.png'), full_page=True)
    await page.close()

    page = await new_page(browser, 375, 900, full_images=True)
    await load_rendered(page, '/catalog.php')
    padding = await page.locator('.page-head').evaluate('''el => {
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return {left:r.left, right:r.right, width:r.width, viewport:innerWidth, paddingLeft:cs.paddingLeft, paddingRight:cs.paddingRight};
    }''')
    await page.locator('#catalog-search').fill('бентонит')
    await page.wait_for_timeout(150)
    filter_state = await page.evaluate('''() => ({
      visible: [...document.querySelectorAll('[data-search-name]')].filter(x => !x.hidden).map(x => x.getAttribute('data-search-name')),
      hidden: [...document.querySelectorAll('[data-search-name]')].filter(x => x.hidden).length
    })''')
    result['catalog_mobile_padding'] = {'passed': float(padding['paddingLeft'][:-2]) >= 16 and float(padding['paddingRight'][:-2]) >= 16, 'metrics': padding}
    result['catalog_filter'] = {'passed': len(filter_state['visible']) == 1 and 'Бентониты' in filter_state['visible'][0] and filter_state['hidden'] >= 7, 'metrics': filter_state}
    await page.screenshot(path=str(OUT / 'mobile-catalog-375.png'), full_page=True)
    await page.close()

    page = await new_page(browser, 375, 900, full_images=True)
    await load_rendered(page, '/contacts.php')
    contact_metrics = await page.evaluate('''() => {
      const head = document.querySelector('.page-head').getBoundingClientRect();
      const card = document.querySelector('.contact-card').getBoundingClientRect();
      const headStyle = getComputedStyle(document.querySelector('.page-head'));
      return {
        viewport: innerWidth,
        headLeft: head.left, headRight: head.right,
        headPaddingLeft: headStyle.paddingLeft, headPaddingRight: headStyle.paddingRight,
        cardLeft: card.left, cardRight: card.right,
        scrollWidth: document.documentElement.scrollWidth
      };
    }''')
    result['contacts_mobile_padding'] = {
        'passed': float(contact_metrics['headPaddingLeft'][:-2]) >= 16 and contact_metrics['cardLeft'] >= 16 and contact_metrics['cardRight'] <= contact_metrics['viewport'] - 16 and contact_metrics['scrollWidth'] <= contact_metrics['viewport'] + 1,
        'metrics': contact_metrics,
    }
    await page.screenshot(path=str(OUT / 'mobile-contacts-375.png'), full_page=True)
    await page.close()

    page = await new_page(browser, 390, 900, full_images=True)
    await load_rendered(page, '/index.php')
    first = page.locator('[data-review-gallery]').first
    await first.click()
    await page.wait_for_timeout(150)
    opened = await page.evaluate('''() => {
      const box = document.querySelector('[data-review-lightbox]');
      const img = document.querySelector('[data-review-image]');
      return {
        hidden: box.hidden,
        bodyClass: document.body.classList.contains('lightbox-open'),
        src: img.getAttribute('src'),
        naturalWidth: img.naturalWidth,
        active: document.activeElement && document.activeElement.className
      };
    }''')
    first_src = opened['src']
    await page.locator('[data-review-next]').click()
    await page.wait_for_timeout(100)
    second_src = await page.locator('[data-review-image]').get_attribute('src')
    await page.screenshot(path=str(OUT / 'mobile-reviews-lightbox-390.png'), full_page=False)
    await page.keyboard.press('Escape')
    closed = await page.evaluate('''() => ({
      hidden: document.querySelector('[data-review-lightbox]').hidden,
      bodyClass: document.body.classList.contains('lightbox-open'),
      focusReturned: document.activeElement === document.querySelector('[data-review-gallery]')
    })''')
    result['reviews_lightbox'] = {
        'passed': not opened['hidden'] and opened['bodyClass'] and opened['naturalWidth'] > 0 and first_src != second_src and closed['hidden'] and not closed['bodyClass'] and closed['focusReturned'],
        'metrics': {'opened': opened, 'second_src': second_src, 'closed': closed},
    }
    await page.close()

    page = await new_page(browser, 390, 900, full_images=True)
    await load_rendered(page, '/product-burovoi-nozh.php')
    await page.locator('[data-menu-toggle]').click()
    menu_open = await page.locator('[data-menu-toggle]').get_attribute('aria-expanded')
    await page.keyboard.press('Escape')
    menu_closed = await page.locator('[data-menu-toggle]').get_attribute('aria-expanded')
    opener = page.locator('[data-kp-open]').first
    await opener.click()
    await page.wait_for_timeout(80)
    modal_open = await page.locator('[data-kp-modal]').evaluate('el => !el.hidden')
    active_name = await page.evaluate('document.activeElement && document.activeElement.getAttribute("name")')
    await page.keyboard.press('Escape')
    modal_closed = await page.locator('[data-kp-modal]').evaluate('el => el.hidden')
    result['menu_and_kp_modal'] = {
        'passed': menu_open == 'true' and menu_closed == 'false' and modal_open and active_name == 'phone' and modal_closed,
        'metrics': {'menu_open': menu_open, 'menu_closed': menu_closed, 'modal_open': modal_open, 'active_name': active_name, 'modal_closed': modal_closed},
    }
    await page.close()

    # Product thumbnail gallery should still initialize on product pages.
    page = await new_page(browser, 390, 900, full_images=True)
    await load_rendered(page, '/product-burovoi-nozh.php')
    thumbs = await page.locator('[data-gallery-thumb]').count()
    if thumbs:
        first_main = await page.locator('[data-gallery-main]').get_attribute('src')
        await page.locator('[data-gallery-thumb]').nth(1).click()
        second_main = await page.locator('[data-gallery-main]').get_attribute('src')
    else:
        first_main = second_main = None
    result['product_gallery'] = {'passed': thumbs == 4 and first_main != second_main, 'metrics': {'thumbs': thumbs, 'first_main': first_main, 'second_main': second_main}}
    await page.close()

    return result


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    paths = sitemap_paths()
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        for width, height in VIEWPORTS:
            page = await new_page(browser, width, height)
            for path in paths:
                results.append(await audit_page(page, path, width, height))
            await page.close()
        targeted = await targeted_checks(browser)
        await browser.close()

    failures = [r for r in results if r['errors']]
    targeted_failures = {k:v for k,v in targeted.items() if not v['passed']}
    report = {
        'status': 'passed' if not failures and not targeted_failures else 'failed',
        'render_mode': 'PHP CLI output + Chromium set_content + intercepted local assets',
        'note': 'Direct browser URL navigation is disabled by the managed runtime; production PHP was rendered before Chromium checks.',
        'sitemap_urls': len(paths),
        'viewports': [list(v) for v in VIEWPORTS],
        'page_viewport_scenarios': len(results),
        'failed_page_scenarios': len(failures),
        'failures': failures,
        'targeted_checks': targeted,
        'targeted_failures': targeted_failures,
    }
    (OUT / 'browser-audit-v26.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({
        'status': report['status'],
        'sitemap_urls': report['sitemap_urls'],
        'page_viewport_scenarios': report['page_viewport_scenarios'],
        'failed_page_scenarios': report['failed_page_scenarios'],
        'targeted': {k:v['passed'] for k,v in targeted.items()},
    }, ensure_ascii=False, indent=2))
    return 0 if report['status'] == 'passed' else 1

if __name__ == '__main__':
    raise SystemExit(asyncio.run(main()))
