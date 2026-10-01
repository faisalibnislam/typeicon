#!/usr/bin/env node
// TypeIcon developer-package generator.
//
//   node packages/scripts/generate.mjs [--release <dir>] [--skip-tsc] [--quiet]
//
// Reads a validated release (default: the newest dist/releases/<version>/typeicon-release)
// and writes the git-ignored generated trees of:
//   packages/catalog/dist        metadata JSON, per-icon JSON, name unions
//   packages/icons-svg/dist      SVG files, sprites, licences
//   packages/icons-webfont/dist  woff2/woff, CSS, licences
//   packages/icons-react/generated + dist (base compiled with tsc)
//   packages/icons-vue/generated   + dist (base compiled with tsc)
//
// Output is deterministic (sorted, no timestamps) and the script is
// idempotent: every generated tree is removed and rebuilt from the release.
// Only Node built-ins are used; `tsc` is spawned once per framework package.

if (!process.env.UV_THREADPOOL_SIZE) process.env.UV_THREADPOOL_SIZE = '16';

import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import fsp from 'node:fs/promises';
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(SCRIPT_DIR, '..', '..');
const PACKAGES = path.join(REPO_ROOT, 'packages');
const DEFAULT_RELEASE = (() => {
  const dir = path.join(REPO_ROOT, 'dist', 'releases');
  const semver = (v) => v.split('.').map(Number);
  const cmp = (a, b) => { const [x, y] = [semver(a), semver(b)]; for (let i = 0; i < 3; i++) if (x[i] !== y[i]) return x[i] - y[i]; return 0; };
  const versions = fs.existsSync(dir) ? fs.readdirSync(dir).filter((v) => /^\d+\.\d+\.\d+$/.test(v)).sort(cmp) : [];
  return path.join(dir, versions.at(-1) ?? '0.0.0', 'typeicon-release');
})();

const STYLE_ORDER = ['filled', 'line', 'rounded', 'thin', 'brand'];
const SOURCE_ORDER = ['typeicon-core', 'simple-icons'];
const NAME_RE = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

const CHILD_TAGS = new Set(['path', 'circle', 'rect', 'ellipse', 'line', 'polyline', 'polygon', 'g']);
const PRESENTATION_ATTRS = new Set([
  'fill', 'fill-opacity', 'fill-rule', 'clip-rule', 'opacity',
  'stroke', 'stroke-width', 'stroke-linecap', 'stroke-linejoin', 'stroke-miterlimit',
  'stroke-dasharray', 'stroke-dashoffset', 'stroke-opacity', 'transform',
]);
const GEOMETRY_ATTRS = new Set([
  'd', 'cx', 'cy', 'r', 'rx', 'ry', 'x', 'y', 'width', 'height', 'x1', 'y1', 'x2', 'y2', 'points',
]);
const ROOT_DROP = new Set(['width', 'height', 'xmlns', 'xmlns:xlink', 'version']);

// ---------------------------------------------------------------- CLI

function parseArgs(argv) {
  const opts = { release: DEFAULT_RELEASE, skipTsc: false, quiet: false };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--release') opts.release = path.resolve(argv[++i] ?? '');
    else if (arg.startsWith('--release=')) opts.release = path.resolve(arg.slice(10));
    else if (arg === '--skip-tsc') opts.skipTsc = true;
    else if (arg === '--quiet') opts.quiet = true;
    else if (arg === '-h' || arg === '--help') {
      console.log('Usage: node packages/scripts/generate.mjs [--release <dir>] [--skip-tsc] [--quiet]');
      process.exit(0);
    } else throw new Error(`Unknown argument: ${arg}`);
  }
  return opts;
}

// ---------------------------------------------------------------- SVG parsing

const ENTITIES = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'" };

function decodeEntities(value, file) {
  return value.replace(/&(#x[0-9a-f]+|#[0-9]+|[a-z]+);/gi, (m, body) => {
    if (body[0] === '#') {
      const code = body[1] === 'x' || body[1] === 'X' ? parseInt(body.slice(2), 16) : parseInt(body.slice(1), 10);
      return String.fromCodePoint(code);
    }
    const ch = ENTITIES[body.toLowerCase()];
    if (ch === undefined) throw new Error(`${file}: unsupported entity ${m}`);
    return ch;
  });
}

const TAG_RE = /<(\/?)([a-zA-Z][\w:-]*)((?:\s+[\w:.-]+\s*=\s*(?:"[^"]*"|'[^']*'))*)\s*(\/?)>/y;
const ATTR_RE = /([\w:.-]+)\s*=\s*(?:"([^"]*)"|'([^']*)')/g;

/** Parse a sanitized release SVG into { root: attrs, children: node[] }. Strict. */
function parseSvg(text, file) {
  const src = text.replace(/^﻿/, '').replace(/^<\?xml[^>]*\?>/, '');
  let pos = 0;
  const skipWs = () => {
    while (pos < src.length && /\s/.test(src[pos])) pos++;
  };
  const stack = [];
  let root = null;
  let rootChildren = null;
  skipWs();
  while (pos < src.length) {
    TAG_RE.lastIndex = pos;
    const m = TAG_RE.exec(src);
    if (!m) throw new Error(`${file}: unexpected content at offset ${pos}: ${JSON.stringify(src.slice(pos, pos + 40))}`);
    pos = TAG_RE.lastIndex;
    const [, closing, tag, rawAttrs, selfClosing] = m;
    if (closing) {
      const open = stack.pop();
      if (!open || open.tag !== tag) throw new Error(`${file}: mismatched </${tag}>`);
      skipWs();
      continue;
    }
    const attrs = {};
    for (const a of rawAttrs.matchAll(ATTR_RE)) {
      const value = decodeEntities(a[2] ?? a[3] ?? '', file);
      if (Object.prototype.hasOwnProperty.call(attrs, a[1])) throw new Error(`${file}: duplicate attribute ${a[1]}`);
      attrs[a[1]] = value;
    }
    if (!root) {
      if (tag !== 'svg') throw new Error(`${file}: root element is <${tag}>`);
      root = attrs;
      rootChildren = [];
      if (selfClosing) throw new Error(`${file}: empty <svg/>`);
      stack.push({ tag, children: rootChildren });
    } else {
      if (!CHILD_TAGS.has(tag)) throw new Error(`${file}: disallowed element <${tag}>`);
      for (const name of Object.keys(attrs)) {
        if (!PRESENTATION_ATTRS.has(name) && !GEOMETRY_ATTRS.has(name)) {
          throw new Error(`${file}: disallowed attribute ${name} on <${tag}>`);
        }
        if (/url\(|javascript:/i.test(attrs[name])) throw new Error(`${file}: unsafe value on ${name}`);
      }
      const parent = stack[stack.length - 1];
      if (!parent) throw new Error(`${file}: content after </svg>`);
      const node = { tag, attrs, children: [] };
      parent.children.push(node);
      if (!selfClosing) stack.push({ tag, children: node.children });
    }
    skipWs();
  }
  if (!root || stack.length) throw new Error(`${file}: unterminated SVG`);
  if (!root.viewBox) throw new Error(`${file}: missing viewBox`);
  const rootAttrs = {};
  for (const [name, value] of Object.entries(root)) {
    if (ROOT_DROP.has(name)) continue;
    if (name !== 'viewBox' && !PRESENTATION_ATTRS.has(name)) throw new Error(`${file}: disallowed root attribute ${name}`);
    rootAttrs[name] = value;
  }
  // Drop leaf nodes that can never paint (e.g. Tabler's `<path stroke="none"
  // fill="none" d="M0 0h24v24H0z"/>` bounding box). Saves bytes per icon.
  const visible = (nodes) =>
    nodes
      .filter((n) => n.children.length > 0 || !(n.attrs.fill === 'none' && n.attrs.stroke === 'none'))
      .map((n) => ({ ...n, children: visible(n.children) }));
  const children = visible(rootChildren);
  if (children.length === 0) throw new Error(`${file}: SVG has no drawable children`);
  return { root: rootAttrs, children };
}

// ---------------------------------------------------------------- Serialisation

const IDENT_RE = /^[A-Za-z_$][\w$]*$/;
const camel = (name) => name.replace(/-([a-z])/g, (_, c) => c.toUpperCase());

function objectLiteral(attrs, mapName) {
  const parts = [];
  for (const [name, value] of Object.entries(attrs)) {
    const key = mapName(name);
    parts.push(`${IDENT_RE.test(key) ? key : JSON.stringify(key)}:${JSON.stringify(value)}`);
  }
  return `{${parts.join(',')}}`;
}

function nodeLiteral(nodes, mapName) {
  return `[${nodes
    .map((n) =>
      n.children.length
        ? `[${JSON.stringify(n.tag)},${objectLiteral(n.attrs, mapName)},${nodeLiteral(n.children, mapName)}]`
        : `[${JSON.stringify(n.tag)},${objectLiteral(n.attrs, mapName)}]`,
    )
    .join(',')}]`;
}

const reactName = (name) => (name === 'viewBox' ? name : camel(name));
const vueName = (name) => name;

function pascal(name) {
  return name
    .split(/[^a-zA-Z0-9]+/)
    .filter(Boolean)
    .map((p) => p[0].toUpperCase() + p.slice(1))
    .join('');
}

function docComment(icon, style) {
  const kw = (icon.keywords || []).slice(0, 8).join(', ');
  const text = `TypeIcon \`${icon.name}\` (${icon.source} / ${style}), ${icon.license}.${kw ? ` Keywords: ${kw}.` : ''}`;
  return `/** ${text.replace(/\*\//g, '* /')} */`;
}

// ---------------------------------------------------------------- File helpers

async function rmrf(dir) {
  await fsp.rm(dir, { recursive: true, force: true });
}

/** Write many files quickly: mkdir each directory once, then a bounded write pool. */
async function writeFiles(files, concurrency = 96) {
  const dirs = [...new Set(files.map(([p]) => path.dirname(p)))].sort();
  for (const dir of dirs) fs.mkdirSync(dir, { recursive: true });
  let index = 0;
  const worker = async () => {
    while (index < files.length) {
      const [file, content] = files[index++];
      await fsp.writeFile(file, content);
    }
  };
  await Promise.all(Array.from({ length: Math.min(concurrency, files.length) }, worker));
}

async function copyTree(src, dst) {
  await fsp.cp(src, dst, { recursive: true, force: true, errorOnExist: false });
}

function stableJson(value, indent = 1) {
  return `${JSON.stringify(value, null, indent)}\n`;
}

// ---------------------------------------------------------------- Main

async function main() {
  const t0 = performance.now();
  const opts = parseArgs(process.argv.slice(2));
  const log = (...a) => {
    if (!opts.quiet) console.log(...a);
  };
  const rel = opts.release;
  for (const sub of ['metadata/icons.json', 'metadata/families.json', 'svg', 'sprites', 'webfonts', 'css', 'licenses']) {
    if (!fs.existsSync(path.join(rel, sub))) throw new Error(`Release is missing ${sub}: ${rel}`);
  }
  log(`release: ${path.relative(REPO_ROOT, rel) || rel}`);

  const iconsRaw = fs.readFileSync(path.join(rel, 'metadata', 'icons.json'), 'utf8');
  const familiesRaw = fs.readFileSync(path.join(rel, 'metadata', 'families.json'), 'utf8');
  const manifestPath = path.join(rel, 'metadata', 'manifest.json');
  const manifestRaw = fs.existsSync(manifestPath) ? fs.readFileSync(manifestPath, 'utf8') : null;
  const manifest = manifestRaw ? JSON.parse(manifestRaw) : { version: 'unknown' };
  const icons = JSON.parse(iconsRaw).slice().sort((a, b) => (a.name < b.name ? -1 : a.name > b.name ? 1 : 0));

  // Validate names and collect variants.
  const seen = new Set();
  const variants = [];
  for (const icon of icons) {
    if (!NAME_RE.test(icon.name)) throw new Error(`Invalid icon name: ${icon.name}`);
    if (seen.has(icon.name)) throw new Error(`Duplicate icon name: ${icon.name}`);
    seen.add(icon.name);
    if (!SOURCE_ORDER.includes(icon.source)) throw new Error(`Unknown source ${icon.source} (${icon.name})`);
    if (icon.area !== 'core' && icon.area !== 'brands') throw new Error(`Unknown area ${icon.area} (${icon.name})`);
    if (icon.area === 'core' && icon.source !== 'typeicon-core') throw new Error(`Core icon from ${icon.source}: ${icon.name}`);
    for (const style of Object.keys(icon.styles)) {
      if (!STYLE_ORDER.includes(style)) throw new Error(`Unknown style ${style} (${icon.name})`);
    }
    for (const style of STYLE_ORDER) {
      const v = icon.styles[style];
      if (!v) continue;
      const expected = `svg/${icon.source}/${style}/${icon.name}.svg`;
      if (v.svg !== expected) throw new Error(`Unexpected svg path ${v.svg} (expected ${expected})`);
      const subpath = icon.area === 'core' ? `${style}/${icon.name}` : icon.area === 'brands' ? `brands/${icon.name}` : `${icon.source}/${style}/${icon.name}`;
      variants.push({ icon, style, meta: v, subpath });
    }
  }
  log(`icons: ${icons.length}  variants: ${variants.length}`);

  const checksums = new Map();
  const checksumPath = path.join(rel, 'checksums.sha256');
  if (fs.existsSync(checksumPath)) {
    for (const line of fs.readFileSync(checksumPath, 'utf8').split('\n')) {
      const m = line.match(/^([0-9a-f]{64})\s+\*?(.+)$/);
      if (m) checksums.set(m[2], m[1]);
    }
  }

  // Read + verify + parse all SVGs (bounded concurrency).
  const tRead = performance.now();
  let next = 0;
  const readWorker = async () => {
    while (next < variants.length) {
      const v = variants[next++];
      const file = path.join(rel, v.meta.svg);
      const buf = await fsp.readFile(file);
      // Integrity: release checksums.sha256 covers the exact file bytes.
      // (icons.json `svgSha256` hashes the canonical SVG without width/height.)
      const expected = checksums.get(v.meta.svg);
      if (expected) {
        const sha = createHash('sha256').update(buf).digest('hex');
        if (sha !== expected) throw new Error(`${v.meta.svg}: sha256 does not match checksums.sha256`);
      } else if (checksums.size) {
        throw new Error(`${v.meta.svg}: not listed in checksums.sha256`);
      }
      v.parsed = parseSvg(buf.toString('utf8'), v.meta.svg);
    }
  };
  await Promise.all(Array.from({ length: 64 }, readWorker));
  log(`parsed SVGs in ${((performance.now() - tRead) / 1000).toFixed(2)}s`);

  // Target directories.
  const dirs = {
    catalog: path.join(PACKAGES, 'catalog', 'dist'),
    svg: path.join(PACKAGES, 'icons-svg', 'dist'),
    webfont: path.join(PACKAGES, 'icons-webfont', 'dist'),
    react: path.join(PACKAGES, 'icons-react', 'generated'),
    vue: path.join(PACKAGES, 'icons-vue', 'generated'),
  };
  const tRm = performance.now();
  await Promise.all(Object.values(dirs).map(rmrf));
  log(`cleaned output in ${((performance.now() - tRm) / 1000).toFixed(2)}s`);

  const files = [];
  const stamp = {
    release: manifest.name ?? 'typeicon-release',
    version: manifest.version ?? 'unknown',
    icons: icons.length,
    variants: variants.length,
    iconsJsonSha256: createHash('sha256').update(iconsRaw).digest('hex'),
  };

  // --- React + Vue icon modules
  const HEADER = '// Generated by packages/scripts/generate.mjs. Do not edit.\n';
  const subpaths = [];
  for (const v of variants) {
    const { icon, style, subpath, parsed } = v;
    const depth = subpath.split('/').length - 1;
    const base = `${'../'.repeat(depth)}../dist/index.js`;
    const isStroke = typeof parsed.root.stroke === 'string' && parsed.root.stroke !== 'none';
    const doc = docComment(icon, style);
    const nameLit = JSON.stringify(icon.name);

    const reactJs =
      `${HEADER}${doc}\nimport { createIcon } from ${JSON.stringify(base)};\n` +
      `export default /*#__PURE__*/ createIcon(${nameLit}, ${nodeLiteral(parsed.children, reactName)}, ${objectLiteral(parsed.root, reactName)});\n`;
    const reactType = isStroke ? 'StrokeIconComponent' : 'FilledIconComponent';
    const reactDts =
      `${HEADER}import type { ${reactType} } from ${JSON.stringify(base)};\n` +
      `${doc}\ndeclare const ${pascal(icon.name)}: ${reactType};\nexport default ${pascal(icon.name)};\n`;

    const vueJs =
      `${HEADER}${doc}\nimport { createIcon } from ${JSON.stringify(base)};\n` +
      `export default /*#__PURE__*/ createIcon(${nameLit}, ${nodeLiteral(parsed.children, vueName)}, ${objectLiteral(parsed.root, vueName)});\n`;
    const vueDts =
      `${HEADER}import type { IconComponent } from ${JSON.stringify(base)};\n` +
      `${doc}\ndeclare const ${pascal(icon.name)}: IconComponent;\nexport default ${pascal(icon.name)};\n`;

    files.push([path.join(dirs.react, `${subpath}.js`), reactJs]);
    files.push([path.join(dirs.react, `${subpath}.d.ts`), reactDts]);
    files.push([path.join(dirs.vue, `${subpath}.js`), vueJs]);
    files.push([path.join(dirs.vue, `${subpath}.d.ts`), vueDts]);
    subpaths.push({ subpath, name: icon.name, source: icon.source, style, stroke: isStroke, viewBox: parsed.root.viewBox });
  }
  subpaths.sort((a, b) => (a.subpath < b.subpath ? -1 : a.subpath > b.subpath ? 1 : 0));
  // A machine-readable list of subpaths (not importable as a barrel: it is JSON).
  const subpathIndex = stableJson({ ...stamp, subpaths }, 0);
  files.push([path.join(dirs.react, 'subpaths.json'), subpathIndex]);
  files.push([path.join(dirs.vue, 'subpaths.json'), subpathIndex]);

  // --- Catalog
  files.push([path.join(dirs.catalog, 'icons.json'), iconsRaw]);
  files.push([path.join(dirs.catalog, 'families.json'), familiesRaw]);
  if (manifestRaw) files.push([path.join(dirs.catalog, 'manifest.json'), manifestRaw]);
  const nameEntries = icons.map((i) => ({
    name: i.name,
    source: i.source,
    area: i.area,
    styles: STYLE_ORDER.filter((s) => i.styles[s]),
  }));
  files.push([path.join(dirs.catalog, 'names.json'), `[\n${nameEntries.map((e) => JSON.stringify(e)).join(',\n')}\n]\n`]);
  for (const icon of icons) files.push([path.join(dirs.catalog, 'icon', `${icon.name}.json`), stableJson(icon)]);
  const union = (list) => (list.length ? list.map((n) => `  | ${JSON.stringify(n)}`).join('\n') : '  never');
  const namesDts =
    `${HEADER}` +
    `export type CoreIconName =\n${union(icons.filter((i) => i.area === 'core').map((i) => i.name))};\n` +
    `export type IconName =\n${union(icons.map((i) => i.name))};\n`;
  files.push([path.join(dirs.catalog, 'names.d.ts'), namesDts]);
  files.push([path.join(dirs.catalog, 'names.js'), `${HEADER}export {};\n`]);
  files.push([path.join(dirs.catalog, 'release.json'), stableJson(stamp)]);

  // --- Stamps for the asset packages
  files.push([path.join(dirs.svg, 'release.json'), stableJson(stamp)]);
  files.push([path.join(dirs.webfont, 'release.json'), stableJson(stamp)]);
  files.push([path.join(dirs.react, 'release.json'), stableJson(stamp)]);
  files.push([path.join(dirs.vue, 'release.json'), stableJson(stamp)]);

  const tWrite = performance.now();
  await writeFiles(files);
  log(`wrote ${files.length} generated files in ${((performance.now() - tWrite) / 1000).toFixed(2)}s`);

  // --- Copied assets
  const tCopy = performance.now();
  await Promise.all([
    copyTree(path.join(rel, 'svg'), path.join(dirs.svg, 'svg')),
    copyTree(path.join(rel, 'sprites'), path.join(dirs.svg, 'sprites')),
    copyTree(path.join(rel, 'webfonts'), path.join(dirs.webfont, 'webfonts')),
    copyTree(path.join(rel, 'css'), path.join(dirs.webfont, 'css')),
    ...Object.values(dirs).map((d) => copyTree(path.join(rel, 'licenses'), path.join(d, 'licenses'))),
  ]);
  checkCssUrls(path.join(dirs.webfont, 'css'));
  log(`copied assets in ${((performance.now() - tCopy) / 1000).toFixed(2)}s`);

  // --- Compile framework base modules
  if (!opts.skipTsc) {
    for (const pkg of ['icons-react', 'icons-vue']) {
      const tTsc = performance.now();
      compileBase(path.join(PACKAGES, pkg));
      log(`tsc ${pkg} in ${((performance.now() - tTsc) / 1000).toFixed(2)}s`);
    }
  }

  log(`done in ${((performance.now() - t0) / 1000).toFixed(2)}s`);
}

/** Every url() in the copied CSS must resolve to a copied file. */
function checkCssUrls(cssDir) {
  for (const name of fs.readdirSync(cssDir).sort()) {
    if (!name.endsWith('.css')) continue;
    const css = fs.readFileSync(path.join(cssDir, name), 'utf8');
    for (const m of css.matchAll(/url\(\s*["']?([^"')]+)["']?\s*\)/g)) {
      const ref = m[1];
      if (/^(?:[a-z]+:|\/)/i.test(ref)) throw new Error(`${name}: non-relative url(${ref})`);
      const target = path.resolve(cssDir, ref.split(/[?#]/)[0]);
      if (!fs.existsSync(target)) throw new Error(`${name}: url(${ref}) does not resolve`);
    }
  }
}

function compileBase(pkgDir) {
  const require = createRequire(path.join(pkgDir, 'package.json'));
  let tsc;
  try {
    tsc = require.resolve('typescript/bin/tsc');
  } catch {
    if (fs.existsSync(path.join(pkgDir, 'dist', 'index.js'))) {
      console.warn(`typescript not installed for ${pkgDir}; keeping existing dist/`);
      return;
    }
    throw new Error(`typescript is not installed for ${pkgDir}; run pnpm install`);
  }
  fs.rmSync(path.join(pkgDir, 'dist'), { recursive: true, force: true });
  const res = spawnSync(process.execPath, [tsc, '-p', path.join(pkgDir, 'tsconfig.json')], {
    cwd: pkgDir,
    stdio: 'inherit',
  });
  if (res.status !== 0) throw new Error(`tsc failed for ${pkgDir}`);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.stack : error);
  process.exit(1);
});
