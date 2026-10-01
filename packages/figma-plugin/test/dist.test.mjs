// Checks on the built artifacts: run `pnpm build` first.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { Script } from 'node:vm';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { ALLOWED_API_ORIGINS, DEV_API_BASE, PRODUCTION_API_BASE } from '../src/shared.ts';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const read = (p) => readFileSync(join(root, p), 'utf8');
const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr']);

/** Minimal HTML tag-balance check; script/style bodies are treated as raw text. */
function checkBalanced(html) {
  const stack = [];
  const re = /<!--[\s\S]*?-->|<!doctype[^>]*>|<\/?([a-zA-Z][\w-]*)\b[^>]*?(\/?)>/gi;
  let m;
  while ((m = re.exec(html))) {
    const tag = m[1]?.toLowerCase();
    if (!tag) continue;
    const closing = m[0].startsWith('</');
    if (closing) {
      const top = stack.pop();
      assert.equal(top, tag, `mismatched </${tag}> at ${m.index}, expected </${top}>`);
    } else if (!VOID.has(tag) && !m[2]) {
      stack.push(tag);
      if (tag === 'script' || tag === 'style') {
        const end = html.toLowerCase().indexOf(`</${tag}`, re.lastIndex);
        assert.ok(end > 0, `unterminated <${tag}>`);
        re.lastIndex = end;
      }
    }
  }
  assert.deepEqual(stack, [], `unclosed tags: ${stack.join(', ')}`);
}

test('dist files exist', () => {
  assert.ok(existsSync(join(root, 'dist/code.js')), 'dist/code.js missing. Run pnpm build');
  assert.ok(existsSync(join(root, 'dist/ui.html')), 'dist/ui.html missing. Run pnpm build');
});

test('dist/ui.html is well-formed and self-contained', () => {
  const html = read('dist/ui.html');
  assert.match(html, /^<!doctype html>/i);
  checkBalanced(html);
  const scripts = [...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)];
  assert.equal(scripts.length, 1, 'expected exactly one inline script');
  assert.equal(scripts[0][1].trim(), '', 'inline script must not have attributes (no src)');
  assert.doesNotMatch(html, /<!-- UI_SCRIPT -->/, 'placeholder was not replaced');
  assert.doesNotMatch(html, /<(?:link|img|iframe)\b[^>]*(?:src|href)\s*=\s*["']https?:/i, 'no external resources');
  // Syntax-check the inlined bundle (compiled, never executed).
  new Script(scripts[0][2], { filename: 'ui-inline.js' });
  // Every element id the UI looks up must exist.
  const ids = [...read('src/ui.ts').matchAll(/\$\('([\w-]+)'\)/g)].map((m) => m[1]);
  assert.ok(ids.length > 5);
  for (const id of ids) assert.match(html, new RegExp(`id="${id}"`), `#${id} missing from ui.html`);
});

test('UI CSP connect-src matches the allowed API origins', () => {
  const csp = /Content-Security-Policy" content="([^"]+)"/.exec(read('dist/ui.html'))?.[1] ?? '';
  const connect = /connect-src ([^;]+)/.exec(csp)?.[1].trim().split(/\s+/) ?? [];
  assert.deepEqual([...connect].sort(), [...ALLOWED_API_ORIGINS].sort());
  assert.match(csp, /default-src 'none'/);
});

test('dist/code.js parses and contains no eval', () => {
  const js = read('dist/code.js');
  new Script(js, { filename: 'code.js' });
  assert.doesNotMatch(js, /\beval\s*\(|new Function\s*\(/);
  assert.doesNotMatch(read('dist/ui.html'), /\beval\s*\(|new Function\s*\(/);
});

test('manifest uses current fields and matches the allow-list', () => {
  const m = JSON.parse(read('manifest.json'));
  assert.equal(m.api, '1.0.0');
  assert.equal(m.documentAccess, 'dynamic-page');
  assert.deepEqual(m.editorType, ['figma']);
  assert.equal(m.main, 'dist/code.js');
  assert.equal(m.ui, 'dist/ui.html');
  assert.deepEqual(m.networkAccess.allowedDomains, [PRODUCTION_API_BASE]);
  assert.deepEqual(m.networkAccess.devAllowedDomains, [DEV_API_BASE]);
  assert.equal(typeof m.networkAccess.reasoning, 'string');
  assert.deepEqual(
    [...m.networkAccess.allowedDomains, ...m.networkAccess.devAllowedDomains].sort(),
    [...ALLOWED_API_ORIGINS].sort(),
  );
});
