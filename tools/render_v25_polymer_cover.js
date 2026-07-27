#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const root = path.resolve(__dirname, '..');
const site = path.join(root, 'site');
const auditDir = path.join(root, 'audit', 'v25-browser');
fs.mkdirSync(auditDir, { recursive: true });

const catalog = fs.readFileSync(path.join(site, 'catalog.php'), 'utf8');
const css = fs.readFileSync(path.join(site, 'css', 'style.css'), 'utf8');
const cardMatch = catalog.match(
  /<a class="category card" href="category-polimer\.php"[\s\S]*?<\/a>/
);
if (!cardMatch) {
  throw new Error('Polymer category card was not found in catalog.php');
}

const card = cardMatch[0]
  .replaceAll('img/', `${path.join(site, 'img')}/`)
  .replaceAll('href="category-polimer.php"', 'href="#"');

const html = `<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>${css}</style>
  <style>
    body { background: #fff; }
    .qa-shell { padding: 24px 0; }
    .qa-shell .categories { display: grid; grid-template-columns: minmax(0, 360px); }
  </style>
</head>
<body>
  <main class="qa-shell">
    <div class="wrap">
      <div class="categories categories--catalog">${card}</div>
    </div>
  </main>
</body>
</html>`;

const scenarios = [
  { name: 'desktop', width: 1440, height: 1100 },
  { name: 'mobile', width: 390, height: 1000 },
];

(async () => {
  const browser = await chromium.launch({ headless: true });
  const results = [];
  for (const scenario of scenarios) {
    const page = await browser.newPage({
      viewport: { width: scenario.width, height: scenario.height },
      deviceScaleFactor: 1,
    });
    await page.setContent(html, { waitUntil: 'load' });
    await page.waitForFunction(() => {
      const image = document.querySelector('.category__img');
      return image && image.complete && image.naturalWidth > 0;
    });
    const metrics = await page.evaluate(() => {
      const image = document.querySelector('.category__img');
      const card = document.querySelector('.category.card');
      return {
        imageLoaded: image.complete && image.naturalWidth > 0,
        currentSource: image.currentSrc,
        imageNaturalSize: [image.naturalWidth, image.naturalHeight],
        cardWidth: Math.round(card.getBoundingClientRect().width),
        horizontalOverflow: document.documentElement.scrollWidth > innerWidth,
      };
    });
    const screenshot = path.join(auditDir, `${scenario.name}.png`);
    await page.screenshot({ path: screenshot, fullPage: true });
    results.push({ ...scenario, ...metrics, screenshot: path.relative(root, screenshot) });
    await page.close();
  }
  await browser.close();

  const errors = [];
  for (const result of results) {
    if (!result.imageLoaded) errors.push(`${result.name}: image did not load`);
    if (result.horizontalOverflow) errors.push(`${result.name}: horizontal overflow`);
    if (!result.currentSource.includes('category-cover-polimery')) {
      errors.push(`${result.name}: wrong image source`);
    }
  }
  const report = {
    status: errors.length ? 'failed' : 'passed',
    scenarios: results,
    errors,
  };
  fs.writeFileSync(
    path.join(root, 'audit', 'v25-browser-gate.json'),
    JSON.stringify(report, null, 2) + '\n'
  );
  console.log(JSON.stringify(report, null, 2));
  process.exitCode = errors.length ? 1 : 0;
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
