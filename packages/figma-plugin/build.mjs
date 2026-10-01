// Builds the plugin into dist/:
//   dist/code.js  – main thread bundle (referenced by manifest.main)
//   dist/ui.html  – UI with its JS bundle inlined (referenced by manifest.ui)
// Usage: node build.mjs [--dev]
import { build } from 'esbuild';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(fileURLToPath(import.meta.url));
const dev = process.argv.includes('--dev');
const defaultApiBase = dev ? 'http://localhost:3107' : 'https://typeicon.net';

const common = {
  bundle: true,
  format: 'iife',
  // The Figma main-thread sandbox is not a full browser; stay conservative.
  target: 'es2017',
  minify: !dev,
  legalComments: 'none',
  logLevel: 'warning',
  define: { __DEFAULT_API_BASE__: JSON.stringify(defaultApiBase) },
};

await mkdir(join(root, 'dist'), { recursive: true });

await build({
  ...common,
  entryPoints: [join(root, 'src/code.ts')],
  outfile: join(root, 'dist/code.js'),
});

const ui = await build({
  ...common,
  target: 'es2020',
  entryPoints: [join(root, 'src/ui.ts')],
  write: false,
});
// Escape any closing-script sequence so the inline script cannot terminate early.
const uiJs = ui.outputFiles[0].text.replace(/<\/(script)/gi, '<\\/$1');
const template = await readFile(join(root, 'src/ui.html'), 'utf8');
const marker = '<!-- UI_SCRIPT -->';
if (!template.includes(marker)) throw new Error(`src/ui.html is missing ${marker}`);
const html = template.replace(marker, () => `<script>\n${uiJs}</script>`);
await writeFile(join(root, 'dist/ui.html'), html);

console.log(`Built dist/code.js and dist/ui.html (${dev ? 'dev' : 'production'}; default API ${defaultApiBase})`);
