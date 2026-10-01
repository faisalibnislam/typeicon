#!/usr/bin/env node
// TypeIcon developer-package verification.
//
//   node packages/scripts/verify.mjs
//
// Requires `pnpm install` and `node packages/scripts/generate.mjs` first.
// Checks: generated tree structure and package exports, catalog helpers,
// TypeScript declarations (tsc --noEmit on both samples), production bundles
// and tree-shaking (esbuild), React SSR (react-dom/server) and Vue SSR
// (@vue/server-renderer). Exits non-zero if any check fails.

import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import zlib from 'node:zlib';

import * as esbuild from 'esbuild';
import { createElement, createRef, Fragment } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { createSSRApp, h } from 'vue';
import { renderToString } from '@vue/server-renderer';

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(SCRIPT_DIR, '..', '..');
const PACKAGES = path.join(REPO_ROOT, 'packages');
const EXAMPLES = path.join(REPO_ROOT, 'examples');

const REACT_ICON_BUDGET = 15 * 1024; // bytes, minified, react external
const VUE_ICON_BUDGET = 15 * 1024; // bytes, minified, vue external
const NEGATIVE_SAMPLE_SIZE = 20;
const SEED = 0xf0c1c0;

// ------------------------------------------------------------- tiny harness

const results = [];
let currentSection = '';
function section(name) {
  currentSection = name;
  console.log(`\n== ${name}`);
}
function check(label, ok, detail = '') {
  results.push({ section: currentSection, label, ok: Boolean(ok), detail });
  console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${label}${detail ? `  (${detail})` : ''}`);
  return Boolean(ok);
}
function info(line) {
  console.log(`  ....  ${line}`);
}
async function guard(label, fn) {
  try {
    await fn();
  } catch (error) {
    check(label, false, error instanceof Error ? error.message.split('\n')[0] : String(error));
    if (process.env.VERIFY_DEBUG) console.error(error);
  }
}

function walk(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(p, out);
    else out.push(p);
  }
  return out;
}

function mulberry32(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const kb = (n) => `${(n / 1024).toFixed(2)} KB`;
const gz = (buf) => zlib.gzipSync(buf, { level: 9 }).length;

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

/** Extract `d` attribute values from a generated icon module. */
function pathData(moduleSource) {
  return [...moduleSource.matchAll(/\bd:"((?:[^"\\]|\\.)*)"/g)].map((m) => JSON.parse(`"${m[1]}"`));
}

function attr(markup, name) {
  const m = markup.match(new RegExp(`<svg[^>]*\\s${name}="([^"]*)"`));
  return m ? m[1] : undefined;
}

// ------------------------------------------------------------- checks

async function checkStructure() {
  section('Generated packages & exports');
  const reactGen = path.join(PACKAGES, 'icons-react', 'generated');
  const vueGen = path.join(PACKAGES, 'icons-vue', 'generated');
  for (const dir of [reactGen, vueGen, path.join(PACKAGES, 'catalog', 'dist'), path.join(PACKAGES, 'icons-svg', 'dist')]) {
    if (!fs.existsSync(dir)) {
      check(`${path.relative(REPO_ROOT, dir)} exists`, false, 'run: node packages/scripts/generate.mjs');
      return null;
    }
  }
  const icons = readJson(path.join(PACKAGES, 'catalog', 'dist', 'icons.json'));
  const variants = icons.reduce((n, i) => n + Object.keys(i.styles).length, 0);
  info(`catalog: ${icons.length} icons, ${variants} style variants`);

  for (const [label, dir] of [['@typeicon/react', reactGen], ['@typeicon/vue', vueGen]]) {
    const files = walk(dir);
    const js = files.filter((f) => f.endsWith('.js'));
    const dts = new Set(files.filter((f) => f.endsWith('.d.ts')));
    check(`${label}: one module per variant`, js.length === variants, `${js.length} modules`);
    check(`${label}: every module has a .d.ts`, js.every((f) => dts.has(f.replace(/\.js$/, '.d.ts'))));
    const index = readJson(path.join(dir, 'subpaths.json'));
    check(`${label}: subpaths.json lists every variant`, index.subpaths.length === variants);
  }

  const require = createRequire(import.meta.url);
  for (const pkg of ['@typeicon/react', '@typeicon/vue']) {
    const pj = require(`${pkg}/package.json`);
    check(`${pkg}: sideEffects is false`, pj.sideEffects === false);
    const root = await import(pkg);
    check(`${pkg}: root export only exposes createIcon (no barrel)`, Object.keys(root).join(',') === 'createIcon', Object.keys(root).join(','));
    const baseFile = fileURLToPath(import.meta.resolve(pkg));
    const src = fs.readFileSync(baseFile, 'utf8');
    const imports = [...src.matchAll(/\bfrom\s+['"]([^'"]+)['"]/g)].map((m) => m[1]);
    const framework = pkg === '@typeicon/react' ? 'react' : 'vue';
    check(`${pkg}: base module imports only ${framework}`, imports.every((s) => s === framework), imports.join(', '));
    check(`${pkg}: base module is small`, fs.statSync(baseFile).size < 8 * 1024, kb(fs.statSync(baseFile).size));
  }

  // Subpath resolution through the exports maps.
  const specs = [
    '@typeicon/react/line/home',
    '@typeicon/react/rounded/search',
    '@typeicon/react/filled/home',
    '@typeicon/react/brands/brand-github',
    '@typeicon/vue/line/home',
    '@typeicon/vue/brands/brand-github',
    '@typeicon/icons-svg/svg/typeicon-core/line/home.svg',
    '@typeicon/icons-svg/svg/simple-icons/brand/brand-github.svg',
    '@typeicon/icons-svg/sprites/simple-icons-brand.svg',
    '@typeicon/icons-webfont/typeicon.css',
    '@typeicon/icons-webfont/css/typeicon-simple-icons.css',
    '@typeicon/icons-webfont/webfonts/TypeIconLine-Regular.woff2',
    '@typeicon/catalog/icons.json',
    '@typeicon/catalog/families.json',
    '@typeicon/catalog/icon/brand-github.json',
  ];
  let resolved = 0;
  for (const spec of specs) {
    try {
      if (fs.existsSync(fileURLToPath(import.meta.resolve(spec)))) resolved++;
      else check(`resolve ${spec}`, false, 'file missing');
    } catch (error) {
      check(`resolve ${spec}`, false, error.message.split('\n')[0]);
    }
  }
  check(`exports maps resolve ${specs.length} representative subpaths to files`, resolved === specs.length, `${resolved}/${specs.length}`);

  const svgCount = walk(path.join(PACKAGES, 'icons-svg', 'dist', 'svg')).filter((f) => f.endsWith('.svg')).length;
  check('@typeicon/icons-svg: one SVG per variant', svgCount === variants, `${svgCount} files`);

  const cssDir = path.join(PACKAGES, 'icons-webfont', 'dist', 'css');
  let urls = 0;
  let bad = [];
  for (const name of fs.readdirSync(cssDir).filter((n) => n.endsWith('.css'))) {
    const css = fs.readFileSync(path.join(cssDir, name), 'utf8');
    for (const m of css.matchAll(/url\(\s*["']?([^"')]+)["']?\s*\)/g)) {
      urls++;
      if (/^(?:[a-z]+:|\/)/i.test(m[1]) || !fs.existsSync(path.resolve(cssDir, m[1]))) bad.push(`${name}:${m[1]}`);
    }
  }
  check('@typeicon/icons-webfont: every CSS url() is relative and resolves', urls > 0 && bad.length === 0, `${urls} urls${bad.length ? `, bad: ${bad.slice(0, 3).join(' ')}` : ''}`);

  // Catalog helpers.
  const catalog = await import('@typeicon/catalog');
  const th = await catalog.getIcon('brand-github');
  check('catalog.getIcon("brand-github") loads one icon lazily', th && th.name === 'brand-github' && th.styles.brand);
  check('catalog.getIcon of unknown / unsafe names → undefined', (await catalog.getIcon('no-such-icon-xyz')) === undefined && (await catalog.getIcon('../icons')) === undefined);
  const home = await catalog.getIcon('home');
  check(
    'catalog.iconImportPath builds Core and brand subpaths',
    catalog.iconImportPath(home, 'line') === '@typeicon/react/line/home' &&
      catalog.iconImportPath(th, 'brand', 'vue') === '@typeicon/vue/brands/brand-github' &&
      catalog.iconImportPath(th, 'line') === undefined &&
      catalog.svgImportPath(th, 'brand') === '@typeicon/icons-svg/svg/simple-icons/brand/brand-github.svg',
  );
  const catalogSrc = fs.readFileSync(fileURLToPath(import.meta.resolve('@typeicon/catalog')), 'utf8');
  check('catalog root module does not statically import icons.json', !/^\s*import\s[^(]*icons\.json/m.test(catalogSrc));

  return { icons };
}

function runTsc(dir) {
  const require = createRequire(path.join(dir, 'package.json'));
  const tsc = require.resolve('typescript/bin/tsc');
  const res = spawnSync(process.execPath, [tsc, '--noEmit', '-p', path.join(dir, 'tsconfig.json')], {
    cwd: dir,
    encoding: 'utf8',
  });
  return { ok: res.status === 0, output: `${res.stdout}${res.stderr}`.trim() };
}

function checkTypes() {
  section('TypeScript declarations (tsc --noEmit)');
  for (const name of ['react-sample', 'vue-sample']) {
    const dir = path.join(EXAMPLES, name);
    const { ok, output } = runTsc(dir);
    check(`examples/${name}: tsc --noEmit (incl. @ts-expect-error negatives)`, ok, ok ? '' : output.split('\n').slice(0, 3).join(' | '));
  }
  // Catalog declarations (index.d.ts + generated name unions) compile on their own.
  const require = createRequire(import.meta.url);
  const res = spawnSync(
    process.execPath,
    [require.resolve('typescript/bin/tsc'), '--noEmit', '--strict', '--skipLibCheck', 'false', '--module', 'nodenext', '--moduleResolution', 'nodenext', path.join(PACKAGES, 'catalog', 'index.d.ts')],
    { cwd: path.join(PACKAGES, 'catalog'), encoding: 'utf8' },
  );
  check('@typeicon/catalog: index.d.ts + dist/names.d.ts typecheck', res.status === 0, res.status === 0 ? '' : `${res.stdout}${res.stderr}`.split('\n').slice(0, 3).join(' | '));
}

function sampleImports(dir) {
  const specs = new Set();
  for (const file of walk(path.join(dir, 'src'))) {
    for (const m of fs.readFileSync(file, 'utf8').matchAll(/from\s+['"](@typeicon\/(?:react|vue)\/[^'"]+)['"]/g)) specs.add(m[1]);
  }
  return specs;
}

async function bundle(dir, entry, { external = [], define = {} } = {}) {
  const res = await esbuild.build({
    absWorkingDir: dir,
    entryPoints: [entry],
    bundle: true,
    minify: true,
    format: 'esm',
    target: 'es2022',
    jsx: 'automatic',
    write: false,
    outdir: 'dist',
    external,
    define: { 'process.env.NODE_ENV': '"production"', ...define },
    logLevel: 'silent',
    metafile: true,
  });
  const out = res.outputFiles.find((f) => f.path.endsWith('.js'));
  return { code: out.text, bytes: out.contents.length, gzip: gz(out.contents), meta: res.metafile };
}

async function checkBundles(icons) {
  section('Production bundles & tree-shaking (esbuild --bundle --minify --format=esm)');
  const reactGen = path.join(PACKAGES, 'icons-react', 'generated');

  const samples = [
    {
      name: 'react-sample',
      entry: 'src/main.tsx',
      appEntry: 'src/App.tsx',
      external: ['react', 'react-dom', 'react/jsx-runtime'],
      budget: REACT_ICON_BUDGET,
      define: {},
    },
    {
      name: 'vue-sample',
      entry: 'src/main.ts',
      appEntry: 'src/App.ts',
      external: ['vue'],
      budget: VUE_ICON_BUDGET,
      define: {
        __VUE_OPTIONS_API__: 'false',
        __VUE_PROD_DEVTOOLS__: 'false',
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: 'false',
      },
    },
  ];

  // Imported icons (from the bundled App entry) and every icon referenced anywhere in the samples.
  const referenced = new Set();
  for (const s of samples) for (const spec of sampleImports(path.join(EXAMPLES, s.name))) referenced.add(spec.replace(/^@typeicon\/(react|vue)\//, ''));

  const subpathOf = (icon, style) => (icon.area === 'core' ? `${style}/${icon.name}` : icon.area === 'brands' ? `brands/${icon.name}` : `${icon.source}/${style}/${icon.name}`);
  const allVariants = [];
  for (const icon of icons) for (const style of Object.keys(icon.styles).sort()) allVariants.push({ icon, style, subpath: subpathOf(icon, style) });

  for (const s of samples) {
    const dir = path.join(EXAMPLES, s.name);
    const appSrc = fs.readFileSync(path.join(dir, s.appEntry), 'utf8');
    const imported = [...appSrc.matchAll(/from\s+['"]@typeicon\/(?:react|vue)\/([^'"]+)['"]/g)].map((m) => m[1]);
    const importedPaths = imported.map((sp) => pathData(fs.readFileSync(path.join(reactGen, `${sp}.js`), 'utf8')));
    const importedD = new Set(importedPaths.flat());
    info(`${s.name}: imports ${imported.join(', ')}`);

    const full = await bundle(dir, s.entry, { define: s.define });
    const iconsOnly = await bundle(dir, s.entry, { external: s.external, define: s.define });
    fs.mkdirSync(path.join(dir, 'dist'), { recursive: true });
    fs.writeFileSync(path.join(dir, 'dist', 'app.js'), full.code);
    fs.writeFileSync(path.join(dir, 'dist', 'icons-only.js'), iconsOnly.code);
    info(`${s.name}: full bundle ${kb(full.bytes)} (gzip ${kb(full.gzip)}); icons+app with framework external ${kb(iconsOnly.bytes)} (gzip ${kb(iconsOnly.gzip)})`);

    const inputs = Object.keys(full.meta.inputs).filter((p) => /generated\//.test(p));
    check(`${s.name}: bundle pulls exactly the ${imported.length} imported icon modules`, inputs.length === imported.length, inputs.map((p) => p.replace(/^.*generated\//, '')).join(', '));

    for (const [i, sp] of imported.entries()) {
      const missing = importedPaths[i].filter((d) => !full.code.includes(d));
      check(`${s.name}: bundle contains path data of ${sp}`, missing.length === 0, `${importedPaths[i].length} paths`);
    }
    const viewBoxes = (iconsOnly.code.match(/viewBox:"/g) || []).length;
    check(`${s.name}: icons-only bundle holds ${imported.length} icon definitions`, viewBoxes === imported.length, `${viewBoxes} viewBox literals`);

    // Negative control: deterministic random sample of non-imported icons.
    const rand = mulberry32(SEED);
    const pool = allVariants.filter((v) => !referenced.has(v.subpath));
    const negatives = [];
    const tried = new Set();
    while (negatives.length < NEGATIVE_SAMPLE_SIZE && tried.size < pool.length) {
      const v = pool[Math.floor(rand() * pool.length)];
      if (tried.has(v.subpath)) continue;
      tried.add(v.subpath);
      const ds = pathData(fs.readFileSync(path.join(reactGen, `${v.subpath}.js`), 'utf8')).filter((d) => !importedD.has(d));
      if (!ds.length) continue;
      const longest = ds.reduce((a, b) => (b.length > a.length ? b : a));
      const snippet = longest.slice(0, 48);
      if ([...importedD].some((d) => d.includes(snippet))) continue;
      negatives.push({ ...v, snippet });
    }
    const leakedPath = negatives.filter((n) => full.code.includes(n.snippet) || iconsOnly.code.includes(n.snippet));
    const leakedName = negatives.filter((n) => iconsOnly.code.includes(JSON.stringify(n.icon.name)));
    check(
      `${s.name}: none of ${negatives.length} random non-imported icons leak (path data)`,
      negatives.length === NEGATIVE_SAMPLE_SIZE && leakedPath.length === 0,
      leakedPath.length ? `leaked: ${leakedPath.map((n) => n.subpath).join(', ')}` : `e.g. ${negatives.slice(0, 3).map((n) => n.subpath).join(', ')}`,
    );
    check(`${s.name}: none of the random non-imported icon names appear`, leakedName.length === 0, leakedName.map((n) => n.icon.name).join(', '));
    check(`${s.name}: icon payload (framework external) < ${kb(s.budget)}`, iconsOnly.bytes < s.budget, kb(iconsOnly.bytes));
  }
}

async function checkReactSsr() {
  section('React SSR (react-dom/server renderToStaticMarkup)');
  const Home = (await import('@typeicon/react/line/home')).default;
  const Search = (await import('@typeicon/react/rounded/search')).default;
  const HomeFilled = (await import('@typeicon/react/filled/home')).default;
  const Github = (await import('@typeicon/react/brands/brand-github')).default;
  const render = (C, props) => renderToStaticMarkup(createElement(C, props));

  const def = render(Home);
  check('default: aria-hidden="true" and focusable="false"', attr(def, 'aria-hidden') === 'true' && attr(def, 'focusable') === 'false', def.slice(0, 90));
  check('default: no role, no <title>', attr(def, 'role') === undefined && !def.includes('<title'));
  check('default: 24×24, viewBox 0 0 24 24, currentColor stroke', attr(def, 'width') === '24' && attr(def, 'height') === '24' && attr(def, 'viewBox') === '0 0 24 24' && attr(def, 'stroke') === 'currentColor');
  check('children rendered as real <path> elements (no innerHTML)', (def.match(/<path /g) || []).length === 3);

  const titled = render(Home, { title: 'Home' });
  const labelledBy = attr(titled, 'aria-labelledby');
  const titleId = (titled.match(/<title id="([^"]+)">Home<\/title>/) || [])[1];
  check('title="Home": role="img", <title>, aria-labelledby → title id', attr(titled, 'role') === 'img' && titleId && labelledBy === titleId, `id=${titleId}`);
  check('title="Home": not aria-hidden', attr(titled, 'aria-hidden') === undefined);

  const two = renderToStaticMarkup(createElement(Fragment, null, createElement(Home, { title: 'A' }), createElement(Search, { title: 'B' })));
  const ids = [...two.matchAll(/<title id="([^"]+)"/g)].map((m) => m[1]);
  check('two titled icons get distinct title ids', ids.length === 2 && ids[0] !== ids[1], ids.join(' vs '));
  const again = renderToStaticMarkup(createElement(Fragment, null, createElement(Home, { title: 'A' }), createElement(Search, { title: 'B' })));
  check('title ids are stable across renders', two === again);

  const labelled = render(Search, { 'aria-label': 'Search' });
  check('aria-label: role="img", not aria-hidden, no <title>', attr(labelled, 'role') === 'img' && attr(labelled, 'aria-hidden') === undefined && !labelled.includes('<title'));

  const big = render(Home, { size: 32 });
  check('size={32} → width="32" height="32"', attr(big, 'width') === '32' && attr(big, 'height') === '32');
  const em = render(Home, { size: '1.5em' });
  check('size="1.5em" → width/height="1.5em"', attr(em, 'width') === '1.5em' && attr(em, 'height') === '1.5em');

  const logo = render(Github);
  check('brand logo renders fill-based, 24×24, viewBox 0 0 24 24', attr(logo, 'viewBox') === '0 0 24 24' && attr(logo, 'width') === '24' && attr(logo, 'stroke') === undefined, attr(logo, 'viewBox'));

  const sw = render(Home, { strokeWidth: 1.5 });
  check('strokeWidth overrides stroke-width on stroke icons', attr(sw, 'stroke-width') === '1.5');
  const swFilled = render(Github, { strokeWidth: 3 });
  check('strokeWidth is ignored on fill-based icons', attr(swFilled, 'stroke-width') === undefined);

  const styled = render(Home, { color: 'red', className: 'nav-icon', 'data-testid': 'x', style: { marginTop: 2 } });
  check('color / className / extra SVG props pass through', attr(styled, 'color') === 'red' && attr(styled, 'class') === 'nav-icon' && attr(styled, 'data-testid') === 'x' && /margin-top:2px/.test(attr(styled, 'style') || ''));

  const explicit = render(Home, { 'aria-hidden': false });
  check('explicit aria-hidden prop wins', attr(explicit, 'aria-hidden') === 'false');

  // Ref forwarding: the icon is a forwardRef component and forwards the ref to <svg>.
  const ref = createRef();
  let forwarded;
  function Probe() {
    const el = Home.render({ size: 16 }, ref);
    forwarded = el.props.ref ?? el.ref;
    return el;
  }
  renderToStaticMarkup(createElement(Probe));
  check('forwardRef: component forwards ref to the <svg> element', Home.$$typeof === Symbol.for('react.forward_ref') && forwarded === ref);
  check('displayName derived from icon name', Home.displayName === 'Home' && Github.displayName === 'BrandGithub' && HomeFilled.displayName === 'Home');
}

async function checkVueSsr() {
  section('Vue SSR (@vue/server-renderer renderToString)');
  const Home = (await import('@typeicon/vue/line/home')).default;
  const Search = (await import('@typeicon/vue/rounded/search')).default;
  const HomeFilled = (await import('@typeicon/vue/filled/home')).default;
  const Github = (await import('@typeicon/vue/brands/brand-github')).default;
  const render = (C, props = {}) => renderToString(createSSRApp({ render: () => h(C, props) }));

  const def = await render(Home);
  check('default: aria-hidden="true" and focusable="false"', attr(def, 'aria-hidden') === 'true' && attr(def, 'focusable') === 'false', def.slice(0, 90));
  check('default: no role, no <title>', attr(def, 'role') === undefined && !def.includes('<title'));
  check('default: 24×24, viewBox 0 0 24 24', attr(def, 'width') === '24' && attr(def, 'height') === '24' && attr(def, 'viewBox') === '0 0 24 24');
  check('children rendered as real <path> elements', (def.match(/<path /g) || []).length === 3);

  const titled = await render(Home, { title: 'Home' });
  const titleId = (titled.match(/<title id="([^"]+)">Home<\/title>/) || [])[1];
  check('title="Home": role="img", <title>, aria-labelledby → title id', attr(titled, 'role') === 'img' && titleId && attr(titled, 'aria-labelledby') === titleId, `id=${titleId}`);
  check('title="Home": not aria-hidden', attr(titled, 'aria-hidden') === undefined);

  const two = await renderToString(createSSRApp({ render: () => h('div', [h(Home, { title: 'A' }), h(Search, { title: 'B' })]) }));
  const ids = [...two.matchAll(/<title id="([^"]+)"/g)].map((m) => m[1]);
  check('two titled icons get distinct title ids', ids.length === 2 && ids[0] !== ids[1], ids.join(' vs '));

  const labelled = await render(Search, { 'aria-label': 'Search' });
  check('aria-label: role="img", not aria-hidden, no <title>', attr(labelled, 'role') === 'img' && attr(labelled, 'aria-hidden') === undefined && !labelled.includes('<title'));

  const big = await render(Home, { size: 32 });
  check('size=32 → width="32" height="32"', attr(big, 'width') === '32' && attr(big, 'height') === '32');

  const logo = await render(Github);
  check('brand logo renders fill-based, viewBox 0 0 24 24', attr(logo, 'viewBox') === '0 0 24 24' && attr(logo, 'stroke') === undefined, attr(logo, 'viewBox'));

  const sw = await render(Home, { strokeWidth: 1.5 });
  check('strokeWidth overrides stroke-width on stroke icons', attr(sw, 'stroke-width') === '1.5');
  const swFilled = await render(Github, { strokeWidth: 3 });
  check('strokeWidth is ignored on fill-based icons', attr(swFilled, 'stroke-width') === undefined);

  const styled = await render(Home, { color: 'red', class: 'nav-icon', 'data-testid': 'x' });
  check('color / class / fallthrough attrs pass through', attr(styled, 'color') === 'red' && attr(styled, 'class') === 'nav-icon' && attr(styled, 'data-testid') === 'x');
  check('component name derived from icon name', Home.name === 'Home' && Github.name === 'BrandGithub' && HomeFilled.name === 'Home');
}

// ------------------------------------------------------------- main

const t0 = performance.now();
let structure = null;
await guard('structure checks', async () => {
  structure = await checkStructure();
});
await guard('type checks', async () => checkTypes());
if (structure) await guard('bundle checks', async () => checkBundles(structure.icons));
await guard('React SSR checks', checkReactSsr);
await guard('Vue SSR checks', checkVueSsr);

const failed = results.filter((r) => !r.ok);
console.log(`\n${results.length - failed.length}/${results.length} checks passed in ${((performance.now() - t0) / 1000).toFixed(1)}s`);
if (failed.length) {
  console.log('Failures:');
  for (const f of failed) console.log(`  - [${f.section}] ${f.label}${f.detail ? ` (${f.detail})` : ''}`);
  process.exit(1);
}
