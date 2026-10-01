// Unit tests for the pure validation helpers used by the main thread before
// figma.createNodeFromSvg. Runs directly under Node's type stripping.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  MAX_SVG_LENGTH,
  applyColor,
  buildSearchUrl,
  iconNodeName,
  isSvgMarkup,
  parseCatalogPage,
  rescaleSteps,
  validateApiBase,
  validateInsertMessage,
} from '../src/shared.ts';

const SVG =
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 11L12 3L21 11"/></svg>';

const good = {
  type: 'insert',
  svg: SVG,
  name: 'home',
  style: 'line',
  source: 'typeicon-core',
  license: 'LicenseRef-TypeIcon-Core-Draft',
  id: '77766e69-c22e-5f1c-aefa-5548e674a4da',
  color: null,
};

test('accepts a well-formed insert message', () => {
  const r = validateInsertMessage(good);
  assert.equal(r.ok, true);
  if (r.ok) {
    assert.equal(r.value.name, 'home');
    assert.equal(r.value.color, null);
  }
});

test('accepts and normalises a custom hex color', () => {
  const r = validateInsertMessage({ ...good, color: '#FF00AA' });
  assert.equal(r.ok && r.value.color, '#ff00aa');
});

test('rejects non-object and wrong-type messages', () => {
  for (const bad of [null, undefined, 42, 'insert', [], { ...good, type: 'nope' }]) {
    assert.equal(validateInsertMessage(bad).ok, false, JSON.stringify(bad));
  }
});

test('rejects non-SVG payloads', () => {
  const payloads = [
    '',
    'hello',
    '<div>hi</div>',
    '<html><svg></svg></html>',
    '<svg viewBox="0 0 1 1"><path d="M0 0"/>', // unterminated
    '<svg></svg><svg></svg>', // two documents
    '<?xml version="1.0"?><!DOCTYPE svg [<!ENTITY x "y">]><svg></svg>',
    123,
  ];
  for (const svg of payloads) {
    assert.equal(validateInsertMessage({ ...good, svg }).ok, false, String(svg));
  }
});

test('rejects SVGs with scripts, handlers, foreign content or external refs', () => {
  const payloads = [
    '<svg><script>alert(1)</script></svg>',
    '<svg onload="alert(1)"><path d="M0 0"/></svg>',
    '<svg><foreignObject><div/></foreignObject></svg>',
    '<svg><image href="https://evil.example/x.png"/></svg>',
    '<svg><use xlink:href="https://evil.example/a.svg#x"/></svg>',
    '<svg><a href="javascript:alert(1)"><path d="M0 0"/></a></svg>',
    '<svg><path style="fill:url(https://evil.example/p)" d="M0 0"/></svg>',
  ];
  for (const svg of payloads) {
    assert.equal(isSvgMarkup(svg), false, svg);
    assert.equal(validateInsertMessage({ ...good, svg }).ok, false, svg);
  }
});

test('allows internal url(#id) references', () => {
  assert.equal(isSvgMarkup('<svg><defs><clipPath id="a"><rect/></clipPath></defs><g clip-path="url(#a)"/></svg>'), true);
});

test('rejects oversized SVGs', () => {
  const pad = 'M0 0'.repeat(Math.ceil(MAX_SVG_LENGTH / 4));
  const huge = `<svg viewBox="0 0 24 24"><path d="${pad}"/></svg>`;
  assert.ok(huge.length > MAX_SVG_LENGTH);
  const r = validateInsertMessage({ ...good, svg: huge });
  assert.equal(r.ok, false);
  assert.match(r.ok ? '' : r.error, /too large/);
});

test('rejects bad metadata fields', () => {
  assert.equal(validateInsertMessage({ ...good, style: 'bold' }).ok, false);
  assert.equal(validateInsertMessage({ ...good, name: '' }).ok, false);
  assert.equal(validateInsertMessage({ ...good, name: 'x'.repeat(129) }).ok, false);
  assert.equal(validateInsertMessage({ ...good, name: '<b>home</b>' }).ok, false);
  assert.equal(validateInsertMessage({ ...good, license: 42 }).ok, false);
  assert.equal(validateInsertMessage({ ...good, id: undefined }).ok, false);
  assert.equal(validateInsertMessage({ ...good, color: 'red' }).ok, false);
  assert.equal(validateInsertMessage({ ...good, color: '#fff' }).ok, false);
});

test('applyColor replaces currentColor, defaulting to black', () => {
  assert.equal(applyColor(SVG, null).includes('currentColor'), false);
  assert.ok(applyColor(SVG, null).includes('stroke="#000000"'));
  assert.ok(applyColor('<svg fill="CurrentColor"></svg>', '#123abc').includes('fill="#123abc"'));
  assert.ok(applyColor(SVG, 'javascript:1').includes('#000000'));
});

test('iconNodeName follows typeicon/<style>/<name>', () => {
  assert.equal(iconNodeName('filled', 'tabler-home'), 'typeicon/filled/tabler-home');
});

test('rescaleSteps preserves aspect ratio and respects the 0.01 floor', () => {
  const product = (xs: number[]) => xs.reduce((a, b) => a * b, 1);
  assert.deepEqual(rescaleSteps(24, 24), []);
  assert.ok(Math.abs(960 * product(rescaleSteps(960, 960)) - 24) < 1e-9);
  const tall = rescaleSteps(48, 96);
  assert.ok(Math.abs(96 * product(tall) - 24) < 1e-9);
  const huge = rescaleSteps(100_000, 50_000);
  assert.ok(huge.every((s) => s >= 0.01));
  assert.ok(Math.abs(100_000 * product(huge) - 24) < 1e-6);
  assert.deepEqual(rescaleSteps(0, 0), []);
});

test('validateApiBase only allows manifest-listed origins', () => {
  assert.deepEqual(validateApiBase('https://typeicon.net/'), { ok: true, value: 'https://typeicon.net' });
  assert.deepEqual(validateApiBase(' http://LOCALHOST:3107 '), { ok: true, value: 'http://localhost:3107' });
  for (const bad of ['https://evil.example', 'http://typeicon.net', 'https://typeicon.net/api', 'javascript:alert(1)', 'http://localhost:9999', '', 5]) {
    assert.equal(validateApiBase(bad).ok, false, String(bad));
  }
});

test('buildSearchUrl encodes parameters', () => {
  assert.equal(
    buildSearchUrl('http://localhost:3107', { q: 'a&b c', style: 'line', area: 'core', page: 2 }),
    'http://localhost:3107/api/icons?q=a%26b%20c&style=line&area=core&page=2&per=48',
  );
});

test('parseCatalogPage keeps unavailable styles as null and drops unsafe SVGs', () => {
  const r = parseCatalogPage({
    page: 1,
    pages: 3,
    total: 3,
    items: [
      { id: 'a', name: 'ok', area: 'core', source: 's', sourceName: 'S', license: 'MIT', styles: ['line'], style: 'line', svg: SVG },
      { id: 'b', name: 'missing', area: 'core', source: 's', sourceName: 'S', license: 'MIT', styles: ['filled'], style: null, svg: null },
      { id: 'c', name: 'evil', area: 'core', source: 's', sourceName: 'S', license: 'MIT', styles: ['line'], style: 'line', svg: '<svg onload="x()"></svg>' },
      { name: 'no-id' },
    ],
  });
  assert.equal(r.ok, true);
  if (!r.ok) return;
  assert.equal(r.value.items.length, 3);
  assert.equal(r.value.items[1].svg, null);
  assert.equal(r.value.items[2].svg, null);
  assert.equal(parseCatalogPage({ nope: true }).ok, false);
});
