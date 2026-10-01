// UI iframe code. Runs in a sandboxed iframe with a `null` origin; all
// network access is restricted by manifest.networkAccess (Figma enforces it
// via CSP). Untrusted SVG markup from the API is never assigned to
// innerHTML: previews are rebuilt node-by-node from an allow-list.

import type { MainToUi, UiToMain } from './messages';
import {
  buildSearchUrl,
  parseCatalogPage,
  validateApiBase,
  type AreaFilter,
  type CatalogItem,
  type StyleFilter,
} from './shared';

declare const __DEFAULT_API_BASE__: string;

const PER_PAGE = 48;
const DEBOUNCE_MS = 250;
const FETCH_TIMEOUT_MS = 15_000;

// ---------------------------------------------------------------------------
// State
// ---------------------------------------------------------------------------

interface State {
  apiBase: string;
  defaultApiBase: string;
  q: string;
  style: StyleFilter;
  area: AreaFilter;
  page: number;
  pages: number;
  total: number;
  items: CatalogItem[];
  selected: number;
  loading: boolean;
  settingsReady: boolean;
}

const state: State = {
  apiBase: __DEFAULT_API_BASE__,
  defaultApiBase: __DEFAULT_API_BASE__,
  q: '',
  style: 'all',
  area: 'all',
  page: 0,
  pages: 0,
  total: 0,
  items: [],
  selected: -1,
  loading: false,
  settingsReady: false,
};

// ---------------------------------------------------------------------------
// DOM
// ---------------------------------------------------------------------------

function $(id: string): HTMLElement {
  const el = document.getElementById(id);
  if (!el) throw new Error(`Missing #${id}`);
  return el;
}

const main = $('scroller');
const qInput = $('q') as HTMLInputElement;
const grid = $('grid');
const statusEl = $('status');
const moreBtn = $('more') as HTMLButtonElement;
const details = $('details');
const insertBtn = $('insert') as HTMLButtonElement;
const useColor = $('use-color') as HTMLInputElement;
const colorInput = $('color') as HTMLInputElement;
const colorHint = $('color-hint');
const settingsPanel = $('settings');
const settingsToggle = $('settings-toggle') as HTMLButtonElement;
const apiBaseInput = $('api-base') as HTMLInputElement;
const apiHint = $('api-hint');
const apiErr = $('api-err');

function send(msg: UiToMain): void {
  parent.postMessage({ pluginMessage: msg }, '*');
}

function setStatus(text: string, isError = false): void {
  statusEl.textContent = text;
  statusEl.classList.toggle('error', isError);
}

// ---------------------------------------------------------------------------
// Safe SVG preview: parse with DOMParser, rebuild only allow-listed nodes
// and attributes with createElementNS/setAttribute. No innerHTML.
// ---------------------------------------------------------------------------

const SVG_NS = 'http://www.w3.org/2000/svg';
const ALLOWED_ELEMENTS = new Set([
  'svg', 'g', 'path', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'rect',
  'defs', 'clipPath', 'mask', 'linearGradient', 'radialGradient', 'stop',
]);
const ALLOWED_ATTRS = new Set([
  'viewBox', 'fill', 'stroke', 'stroke-width', 'stroke-linecap', 'stroke-linejoin',
  'stroke-miterlimit', 'stroke-dasharray', 'stroke-dashoffset', 'fill-rule', 'clip-rule',
  'd', 'cx', 'cy', 'r', 'rx', 'ry', 'x', 'y', 'x1', 'y1', 'x2', 'y2', 'width', 'height',
  'points', 'transform', 'opacity', 'fill-opacity', 'stroke-opacity', 'id', 'clip-path',
  'mask', 'offset', 'stop-color', 'stop-opacity', 'gradientUnits', 'gradientTransform',
  'fx', 'fy', 'vector-effect',
]);
const SAFE_URL_REF = /^url\(#[\w-]+\)$/;

function cloneSafe(src: Element): SVGElement | null {
  if (src.namespaceURI !== SVG_NS || !ALLOWED_ELEMENTS.has(src.localName)) return null;
  const out = document.createElementNS(SVG_NS, src.localName);
  for (const attr of Array.from(src.attributes)) {
    if (attr.namespaceURI !== null || !ALLOWED_ATTRS.has(attr.name)) continue;
    const v = attr.value;
    if (/url\(/i.test(v) && !SAFE_URL_REF.test(v.trim())) continue;
    out.setAttribute(attr.name, v);
  }
  for (const child of Array.from(src.children)) {
    const c = cloneSafe(child);
    if (c) out.appendChild(c);
  }
  return out;
}

function svgPreview(markup: string): SVGElement | null {
  const doc = new DOMParser().parseFromString(markup, 'image/svg+xml');
  if (doc.getElementsByTagName('parsererror').length > 0) return null;
  const root = doc.documentElement;
  if (root.localName !== 'svg') return null;
  const svg = cloneSafe(root);
  if (!svg) return null;
  svg.setAttribute('width', '24');
  svg.setAttribute('height', '24');
  svg.setAttribute('aria-hidden', 'true');
  svg.setAttribute('focusable', 'false');
  return svg;
}

// ---------------------------------------------------------------------------
// Rendering
// ---------------------------------------------------------------------------

function styleLabel(item: CatalogItem): string {
  return item.style ?? (state.style === 'all' ? 'default' : state.style);
}

function renderCell(item: CatalogItem, index: number): HTMLButtonElement {
  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'cell';
  btn.setAttribute('role', 'option');
  btn.setAttribute('aria-selected', 'false');
  btn.tabIndex = -1;
  btn.dataset.index = String(index);

  const preview = item.svg && item.style ? svgPreview(item.svg) : null;
  if (preview) {
    btn.appendChild(preview);
    btn.title = `${item.name} · ${item.style} · ${item.sourceName} · ${item.license}`;
    btn.setAttribute('aria-label', `${item.name}, ${item.style}, ${item.sourceName}, ${item.license}`);
  } else {
    btn.classList.add('unavailable');
    btn.setAttribute('aria-disabled', 'true');
    const na = document.createElement('span');
    na.className = 'na';
    na.setAttribute('aria-hidden', 'true');
    btn.appendChild(na);
    btn.title = `${item.name}: unavailable in this style`;
    btn.setAttribute('aria-label', `${item.name}, unavailable in this style`);
  }
  const label = document.createElement('span');
  label.className = 'label';
  label.textContent = item.name;
  btn.appendChild(label);
  return btn;
}

function appendItems(items: CatalogItem[], offset: number): void {
  const frag = document.createDocumentFragment();
  items.forEach((item, i) => frag.appendChild(renderCell(item, offset + i)));
  grid.appendChild(frag);
}

function cells(): HTMLButtonElement[] {
  return Array.from(grid.querySelectorAll<HTMLButtonElement>('.cell'));
}

function isInsertable(item: CatalogItem | undefined): item is CatalogItem & { svg: string; style: NonNullable<CatalogItem['style']> } {
  return !!item && !!item.svg && !!item.style;
}

function renderDetails(): void {
  details.textContent = '';
  const item = state.items[state.selected];
  if (!item) {
    const hint = document.createElement('div');
    hint.className = 'sub';
    hint.textContent = 'Select an icon. Enter inserts the focused icon.';
    details.appendChild(hint);
    insertBtn.disabled = true;
    return;
  }
  const title = document.createElement('div');
  title.textContent = `${item.name} · ${styleLabel(item)}`;
  const sub = document.createElement('div');
  sub.className = 'sub';
  sub.textContent = isInsertable(item)
    ? `${item.sourceName} · ${item.license}`
    : `Unavailable in this style · ${item.sourceName} · ${item.license}`;
  details.append(title, sub);
  insertBtn.disabled = !isInsertable(item);
}

function select(index: number, focus: boolean): void {
  const all = cells();
  if (index < 0 || index >= all.length) return;
  const prev = all[state.selected];
  if (prev) {
    prev.setAttribute('aria-selected', 'false');
    prev.tabIndex = -1;
  }
  state.selected = index;
  const cur = all[index];
  cur.setAttribute('aria-selected', 'true');
  cur.tabIndex = 0;
  if (focus) cur.focus();
  cur.scrollIntoView({ block: 'nearest' });
  renderDetails();
}

function updateMore(): void {
  moreBtn.classList.toggle('show', state.page > 0 && state.page < state.pages && !state.loading);
}

// ---------------------------------------------------------------------------
// Fetching
// ---------------------------------------------------------------------------

let inflight: AbortController | null = null;
let requestSeq = 0;

async function load(page: number): Promise<void> {
  inflight?.abort();
  const controller = new AbortController();
  inflight = controller;
  const seq = ++requestSeq;
  const timer = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);

  state.loading = true;
  updateMore();
  if (page === 1) setStatus('Searching…');

  const url = buildSearchUrl(state.apiBase, { q: state.q, style: state.style, area: state.area, page, per: PER_PAGE });
  try {
    const res = await fetch(url, { signal: controller.signal, credentials: 'omit', headers: { Accept: 'application/json' } });
    if (!res.ok) throw new Error(`The catalog API returned HTTP ${res.status}.`);
    const parsed = parseCatalogPage(await res.json());
    if (!parsed.ok) throw new Error(parsed.error);
    if (seq !== requestSeq) return;

    const data = parsed.value;
    if (page === 1) {
      grid.textContent = '';
      state.items = [];
      state.selected = -1;
      renderDetails();
      main.scrollTop = 0;
    }
    const offset = state.items.length;
    state.items = state.items.concat(data.items);
    state.page = data.page;
    state.pages = data.pages;
    state.total = data.total;
    appendItems(data.items, offset);

    if (state.items.length === 0) {
      setStatus(state.q ? `No icons match "${state.q}".` : 'No icons found.');
    } else {
      setStatus(`${state.total.toLocaleString()} icon${state.total === 1 ? '' : 's'} · showing ${state.items.length}`);
    }
    if (page === 1 && state.items.length > 0) select(0, false);
  } catch (err) {
    if (seq !== requestSeq) return;
    const aborted = err instanceof DOMException && err.name === 'AbortError';
    const msg = aborted
      ? 'The catalog request timed out.'
      : err instanceof TypeError
        ? `Could not reach ${state.apiBase}. Check your connection or the API base URL in settings.`
        : err instanceof Error
          ? err.message
          : 'Unknown error.';
    setStatus(msg, true);
  } finally {
    clearTimeout(timer);
    if (seq === requestSeq) {
      state.loading = false;
      inflight = null;
      updateMore();
    }
  }
}

let debounceTimer: ReturnType<typeof setTimeout> | undefined;

function search(): void {
  if (!state.settingsReady) return;
  state.page = 0;
  state.pages = 0;
  void load(1);
}

// ---------------------------------------------------------------------------
// Insert
// ---------------------------------------------------------------------------

function insert(index: number): void {
  const item = state.items[index];
  if (!isInsertable(item)) {
    setStatus(item ? `${item.name} is unavailable in this style.` : 'Nothing selected.', true);
    return;
  }
  send({
    type: 'insert',
    svg: item.svg,
    name: item.name,
    style: item.style,
    source: item.source,
    license: item.license,
    id: item.id,
    color: useColor.checked ? colorInput.value : null,
  });
}

// ---------------------------------------------------------------------------
// Events
// ---------------------------------------------------------------------------

qInput.addEventListener('input', () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    const next = qInput.value.trim();
    if (next === state.q && state.page > 0) return;
    state.q = next;
    search();
  }, DEBOUNCE_MS);
});

qInput.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowDown' && state.items.length > 0) {
    e.preventDefault();
    select(Math.max(0, state.selected), true);
  } else if (e.key === 'Enter') {
    e.preventDefault();
    clearTimeout(debounceTimer);
    const next = qInput.value.trim();
    if (next !== state.q) {
      state.q = next;
      search();
    } else if (state.selected >= 0) {
      insert(state.selected);
    }
  }
});

function segmented<T extends string>(groupId: string, attr: string, onChange: (v: T) => void): void {
  const group = $(groupId);
  group.addEventListener('click', (e) => {
    const btn = (e.target as HTMLElement).closest<HTMLButtonElement>(`button[data-${attr}]`);
    if (!btn) return;
    for (const b of Array.from(group.querySelectorAll('button'))) b.setAttribute('aria-pressed', String(b === btn));
    onChange(btn.dataset[attr] as T);
  });
}

segmented<StyleFilter>('style-group', 'style', (v) => {
  state.style = v;
  search();
});
segmented<AreaFilter>('area-group', 'area', (v) => {
  state.area = v;
  search();
});

function columns(): number {
  const all = cells();
  if (all.length < 2) return 1;
  const top = all[0].offsetTop;
  let n = 0;
  while (n < all.length && all[n].offsetTop === top) n++;
  return Math.max(1, n);
}

grid.addEventListener('click', (e) => {
  const cell = (e.target as HTMLElement).closest<HTMLButtonElement>('.cell');
  if (!cell) return;
  select(Number(cell.dataset.index), true);
});

grid.addEventListener('dblclick', (e) => {
  const cell = (e.target as HTMLElement).closest<HTMLButtonElement>('.cell');
  if (cell) insert(Number(cell.dataset.index));
});

grid.addEventListener('keydown', (e) => {
  const n = state.items.length;
  if (n === 0) return;
  const i = state.selected < 0 ? 0 : state.selected;
  let next = i;
  switch (e.key) {
    case 'ArrowRight': next = Math.min(n - 1, i + 1); break;
    case 'ArrowLeft': next = Math.max(0, i - 1); break;
    case 'ArrowDown': next = Math.min(n - 1, i + columns()); break;
    case 'ArrowUp':
      if (i - columns() < 0) {
        e.preventDefault();
        qInput.focus();
        return;
      }
      next = i - columns();
      break;
    case 'Home': next = 0; break;
    case 'End': next = n - 1; break;
    case 'Enter':
    case ' ':
      e.preventDefault();
      insert(i);
      return;
    default:
      return;
  }
  e.preventDefault();
  select(next, true);
});

insertBtn.addEventListener('click', () => insert(state.selected));
moreBtn.addEventListener('click', () => {
  if (state.page < state.pages) void load(state.page + 1);
});

function updateColorHint(): void {
  colorInput.disabled = !useColor.checked;
  colorHint.textContent = useColor.checked
    ? `currentColor → ${colorInput.value}`
    : 'Inserted as black (#000000)';
}
useColor.addEventListener('change', updateColorHint);
colorInput.addEventListener('input', updateColorHint);

// Settings --------------------------------------------------------------

function renderSettings(): void {
  apiBaseInput.value = state.apiBase;
  apiHint.textContent = `Default: ${state.defaultApiBase}. Only origins allowed by the plugin manifest can be used.`;
}

settingsToggle.addEventListener('click', () => {
  const open = !settingsPanel.classList.contains('open');
  settingsPanel.classList.toggle('open', open);
  settingsToggle.setAttribute('aria-expanded', String(open));
  if (open) {
    renderSettings();
    apiBaseInput.focus();
  }
});

function saveApiBase(value: string): void {
  const checked = validateApiBase(value);
  if (!checked.ok) {
    apiErr.textContent = checked.error;
    return;
  }
  apiErr.textContent = '';
  send({ type: 'set-settings', apiBase: checked.value });
}

$('api-save').addEventListener('click', () => saveApiBase(apiBaseInput.value));
$('api-reset').addEventListener('click', () => saveApiBase(state.defaultApiBase));
apiBaseInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    saveApiBase(apiBaseInput.value);
  }
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && settingsPanel.classList.contains('open')) {
    settingsPanel.classList.remove('open');
    settingsToggle.setAttribute('aria-expanded', 'false');
    qInput.focus();
  }
});

// Messages from the main thread ----------------------------------------

function applySettings(apiBase: string, defaultApiBase: string): void {
  const base = validateApiBase(apiBase);
  const def = validateApiBase(defaultApiBase);
  if (def.ok) state.defaultApiBase = def.value;
  const changed = !state.settingsReady || (base.ok && base.value !== state.apiBase);
  if (base.ok) state.apiBase = base.value;
  state.settingsReady = true;
  renderSettings();
  if (changed) search();
}

window.addEventListener('message', (event: MessageEvent) => {
  const msg = (event.data as { pluginMessage?: MainToUi } | null)?.pluginMessage;
  if (!msg || typeof msg !== 'object') return;
  switch (msg.type) {
    case 'settings':
      if (typeof msg.apiBase === 'string' && typeof msg.defaultApiBase === 'string') {
        apiErr.textContent = '';
        applySettings(msg.apiBase, msg.defaultApiBase);
      }
      break;
    case 'settings-error':
      apiErr.textContent = String(msg.error);
      break;
    case 'inserted':
      setStatus(`Inserted ${String(msg.name)}.`);
      break;
    case 'insert-error':
      setStatus(String(msg.error), true);
      break;
  }
});

// Boot -------------------------------------------------------------------

updateColorHint();
send({ type: 'get-settings' });
// If the main thread does not answer (e.g. the UI is opened directly in a
// browser for development), fall back to the build-time default.
setTimeout(() => {
  if (!state.settingsReady) applySettings(state.apiBase, state.defaultApiBase);
}, 1500);
