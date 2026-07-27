#!/usr/bin/env node
'use strict';

const fs = require('fs');
const fsp = fs.promises;
const path = require('path');
const sharp = require('sharp');

const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site');
const IMAGE_ROOT = path.join(SITE, 'img');
const GALLERY_ROOT = path.join(IMAGE_ROOT, 'gallery', 'a-line');
const GALLERY_JS = path.join(SITE, 'js', 'product-galleries.js');
const REPORT = path.join(ROOT, 'audit', 'v20-media-optimization.json');
const TEXT_EXTENSIONS = new Set(['.php', '.css', '.js', '.xml', '.txt', '.html']);

async function walk(directory) {
  const result = [];
  for (const entry of await fsp.readdir(directory, { withFileTypes: true })) {
    const item = path.join(directory, entry.name);
    if (entry.isDirectory()) result.push(...await walk(item));
    else if (entry.isFile()) result.push(item);
  }
  return result;
}

function safeGalleryPath(relativePath) {
  const normalized = path.posix.normalize(relativePath);
  if (normalized.startsWith('../') || path.isAbsolute(normalized)) {
    throw new Error('Unsafe gallery path: ' + relativePath);
  }
  return normalized;
}

async function main() {
  const initialGallerySource = await fsp.readFile(GALLERY_JS, 'utf8');
  const galleryPaths = [...initialGallerySource.matchAll(
    /['"]([^'"]+\.(?:jpe?g|png))['"]/gi
  )].map((match) => safeGalleryPath(match[1]));
  const uniqueGalleryPaths = [...new Set(galleryPaths)];

  const converted = [];
  let updatedGallerySource = initialGallerySource;

  for (const relativePath of uniqueGalleryPaths) {
    const source = path.join(GALLERY_ROOT, relativePath);
    const outputRelative = relativePath.replace(/\.(?:jpe?g|png)$/i, '.webp');
    const output = path.join(GALLERY_ROOT, outputRelative);
    const sourceBytes = (await fsp.stat(source)).size;
    const buffer = await sharp(source)
      .rotate()
      .resize({ width: 1600, height: 1600, fit: 'inside', withoutEnlargement: true })
      .webp({ quality: 80, effort: 6 })
      .toBuffer();

    const metadata = await sharp(buffer).metadata();
    if (metadata.format !== 'webp' || !metadata.width || !metadata.height) {
      throw new Error('Generated file failed validation: ' + outputRelative);
    }

    await fsp.mkdir(path.dirname(output), { recursive: true });
    await fsp.writeFile(output, buffer);
    updatedGallerySource = updatedGallerySource.split(relativePath).join(outputRelative);
    converted.push({
      source: relativePath,
      output: outputRelative,
      before_bytes: sourceBytes,
      after_bytes: buffer.length,
      width: metadata.width,
      height: metadata.height,
    });
  }

  await fsp.writeFile(GALLERY_JS, updatedGallerySource, 'utf8');

  for (const item of converted) {
    const source = path.join(GALLERY_ROOT, item.source);
    if (fs.existsSync(source)) await fsp.unlink(source);
  }

  const siteFiles = await walk(SITE);
  const texts = [];
  for (const file of siteFiles) {
    if (TEXT_EXTENSIONS.has(path.extname(file).toLowerCase())) {
      texts.push(await fsp.readFile(file, 'utf8'));
    }
  }
  const allText = texts.join('\n');
  const finalGallerySource = await fsp.readFile(GALLERY_JS, 'utf8');
  const imageFiles = (await walk(IMAGE_ROOT)).filter((file) => fs.statSync(file).isFile());
  const unused = [];

  for (const file of imageFiles) {
    const relativePath = path.relative(IMAGE_ROOT, file).split(path.sep).join('/');
    const galleryRelative = relativePath.startsWith('gallery/a-line/')
      ? relativePath.slice('gallery/a-line/'.length)
      : '';
    const referenced = allText.includes('img/' + relativePath)
      || (galleryRelative !== '' && finalGallerySource.includes(galleryRelative));
    if (!referenced) {
      unused.push({ path: relativePath, bytes: (await fsp.stat(file)).size });
    }
  }

  for (const item of unused) {
    await fsp.unlink(path.join(IMAGE_ROOT, item.path));
  }

  const report = {
    gallery_entries: galleryPaths.length,
    unique_gallery_images: uniqueGalleryPaths.length,
    converted_images: converted.length,
    gallery_bytes_before: converted.reduce((sum, item) => sum + item.before_bytes, 0),
    gallery_bytes_after: converted.reduce((sum, item) => sum + item.after_bytes, 0),
    gallery_bytes_saved: converted.reduce(
      (sum, item) => sum + item.before_bytes - item.after_bytes,
      0
    ),
    unused_files_removed: unused.length,
    unused_bytes_removed: unused.reduce((sum, item) => sum + item.bytes, 0),
    converted,
    unused,
  };
  await fsp.mkdir(path.dirname(REPORT), { recursive: true });
  await fsp.writeFile(REPORT, JSON.stringify(report, null, 2) + '\n', 'utf8');
  process.stdout.write(JSON.stringify({
    gallery_entries: report.gallery_entries,
    converted_images: report.converted_images,
    gallery_bytes_saved: report.gallery_bytes_saved,
    unused_files_removed: report.unused_files_removed,
    unused_bytes_removed: report.unused_bytes_removed,
  }, null, 2) + '\n');
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
