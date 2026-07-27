#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const PhpParser = require('php-parser');

const root = path.resolve(__dirname, '..');
const site = path.join(root, 'site');
const output = path.join(root, 'audit', 'php-parser-v24.json');
const engine = new PhpParser.Engine({
  parser: { extractDoc: true, php7: true },
  ast: { withPositions: true }
});

function collect(directory) {
  return fs.readdirSync(directory, { withFileTypes: true })
    .flatMap((entry) => {
      const target = path.join(directory, entry.name);
      return entry.isDirectory() ? collect(target) : [target];
    })
    .filter((target) => target.endsWith('.php'))
    .sort();
}

const files = collect(site);
const errors = [];

for (const file of files) {
  try {
    engine.parseCode(fs.readFileSync(file, 'utf8'), path.relative(site, file));
  } catch (error) {
    errors.push({
      file: path.relative(site, file).split(path.sep).join('/'),
      message: error.message
    });
  }
}

const result = {
  status: errors.length ? 'failed' : 'passed',
  parser: 'php-parser@3.2.5',
  php_files_checked: files.length,
  errors
};

fs.writeFileSync(output, JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify(result, null, 2));
process.exitCode = errors.length ? 1 : 0;
