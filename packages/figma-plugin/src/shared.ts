// Pure, dependency-free helpers shared by the main thread (code.ts), the UI
// (ui.ts) and the Node tests. Nothing in here may touch `figma`, the DOM or
// any other host global, and it must only use erasable TypeScript syntax so
// Node can run it directly with type stripping.

export const ICON_STYLES = ['filled', 'line', 'rounded', 'thin'] as const;
export type IconStyle = (typeof ICON_STYLES)[number];
export type StyleFilter = 'all' | IconStyle;
export type AreaFilter = 'all' | 'core' | 'brands';

/** Upper bound on an SVG we are willing to hand to createNodeFromSvg. */
export const MAX_SVG_LENGTH = 100_000;
/** Final size of the longest side of an inserted icon, in px. */
export const ICON_SIZE = 24;
export const DEFAULT_COLOR = '#000000';

export const PRODUCTION_API_BASE = 'https://typeicon.net';
export const DEV_API_BASE = 'http://localhost:3107';

/**
 * Origins the plugin may talk to. This MUST stay in sync with
 * manifest.json → networkAccess.allowedDomains / devAllowedDomains
 * (a test enforces it). Figma blocks anything else with a CSP error anyway;
 * validating here gives the user a readable error instead.
 */
export const ALLOWED_API_ORIGINS: readonly string[] = [PRODUCTION_API_BASE, DEV_API_BASE];

// ---------------------------------------------------------------------------
// API base URL handling
// ---------------------------------------------------------------------------

export type Result<T> = { ok: true; value: T } | { ok: false; error: string };

/** Normalises and allow-lists an API base URL. Returns the bare origin. */
export function validateApiBase(input: unknown): Result<string> {
  if (typeof input !== 'string') return { ok: false, error: 'API base URL must be a string.' };
  const trimmed = input.trim().replace(/\/+$/, '');
  if (trimmed.length === 0 || trimmed.length > 200) {
    return { ok: false, error: 'API base URL is empty or too long.' };
  }
  const m = /^(https?):\/\/([a-z0-9.-]+)(?::(\d{1,5}))?$/i.exec(trimmed);
  if (!m) {
    return { ok: false, error: 'Use an origin only, e.g. https://typeicon.net (no path or query).' };
  }
  const origin = `${m[1].toLowerCase()}://${m[2].toLowerCase()}${m[3] ? `:${m[3]}` : ''}`;
  if (!ALLOWED_API_ORIGINS.includes(origin)) {
    return {
      ok: false,
      error: `Not allowed by the plugin manifest. Allowed: ${ALLOWED_API_ORIGINS.join(', ')}`,
    };
  }
  return { ok: true, value: origin };
}

export interface SearchParams {
  q: string;
  style: StyleFilter;
  area: AreaFilter;
  page: number;
  per?: number;
}

export function buildSearchUrl(apiBase: string, p: SearchParams): string {
  // Built by hand (not URLSearchParams) so this module has no host dependencies.
  const pairs: Array<[string, string]> = [
    ['q', p.q.slice(0, 100)],
    ['style', p.style],
    ['area', p.area],
    ['page', String(Math.max(1, Math.floor(p.page)))],
    ['per', String(p.per ?? 48)],
  ];
  const qs = pairs.map(([k, v]) => `${k}=${encodeURIComponent(v)}`).join('&');
  return `${apiBase}/api/icons?${qs}`;
}

// ---------------------------------------------------------------------------
// API response parsing (defensive: the UI never trusts the network shape)
// ---------------------------------------------------------------------------

export interface CatalogItem {
  id: string;
  name: string;
  area: string;
  source: string;
  sourceName: string;
  license: string;
  styles: string[];
  style: IconStyle | null;
  svg: string | null;
}

export interface CatalogPage {
  page: number;
  pages: number;
  total: number;
  items: CatalogItem[];
}

function str(v: unknown, max: number): string {
  return typeof v === 'string' ? v.slice(0, max) : '';
}

function isStyle(v: unknown): v is IconStyle {
  return typeof v === 'string' && (ICON_STYLES as readonly string[]).includes(v);
}

export function parseCatalogPage(json: unknown): Result<CatalogPage> {
  if (!json || typeof json !== 'object') return { ok: false, error: 'Unexpected response from catalog API.' };
  const o = json as Record<string, unknown>;
  if (!Array.isArray(o.items)) return { ok: false, error: 'Unexpected response from catalog API (no items).' };
  const num = (v: unknown, d: number) => (typeof v === 'number' && Number.isFinite(v) ? v : d);
  const items: CatalogItem[] = [];
  for (const raw of o.items.slice(0, 200)) {
    if (!raw || typeof raw !== 'object') continue;
    const r = raw as Record<string, unknown>;
    const id = str(r.id, 128);
    const name = str(r.name, 128);
    if (!id || !name) continue;
    const svg = typeof r.svg === 'string' && isSvgMarkup(r.svg) ? r.svg : null;
    items.push({
      id,
      name,
      area: str(r.area, 32),
      source: str(r.source, 64),
      sourceName: str(r.sourceName, 128) || str(r.source, 64),
      license: str(r.license, 128),
      styles: Array.isArray(r.styles) ? r.styles.filter(isStyle) : [],
      style: isStyle(r.style) ? r.style : null,
      svg,
    });
  }
  return {
    ok: true,
    value: { page: num(o.page, 1), pages: num(o.pages, 1), total: num(o.total, items.length), items },
  };
}

// ---------------------------------------------------------------------------
// SVG + insert-message validation (used by the main thread before
// figma.createNodeFromSvg)
// ---------------------------------------------------------------------------

const FORBIDDEN_SVG = [
  /<script[\s>/]/i,
  /<foreignObject[\s>/]/i,
  /<iframe[\s>/]/i,
  /<image[\s>/]/i,
  /<use[\s>/]/i, // no external/internal references; catalog SVGs are flat paths
  /\son[a-z]+\s*=/i, // inline event handlers
  /javascript:/i,
  /<!ENTITY/i,
  /<!DOCTYPE/i,
  /(?:xlink:)?href\s*=\s*["'](?!#)/i, // any non-fragment href
  /url\(\s*["']?(?!#)/i, // external url() references
];

/** Cheap structural check: a single <svg>…</svg> document, no dangerous bits. */
export function isSvgMarkup(svg: string): boolean {
  if (svg.length === 0 || svg.length > MAX_SVG_LENGTH) return false;
  const s = svg.trim();
  if (!/^<svg[\s>]/i.test(s) || !/<\/svg>$/i.test(s)) return false;
  if ((s.match(/<svg[\s>]/gi) ?? []).length !== 1) return false;
  return !FORBIDDEN_SVG.some((re) => re.test(s));
}

export interface InsertRequest {
  svg: string;
  name: string;
  style: IconStyle;
  source: string;
  license: string;
  id: string;
  color: string | null;
}

const HEX_COLOR = /^#[0-9a-f]{6}$/i;
const SAFE_LABEL = /^[\w .:/@+()-]+$/;

export function validateInsertMessage(msg: unknown): Result<InsertRequest> {
  if (!msg || typeof msg !== 'object') return { ok: false, error: 'Malformed message.' };
  const m = msg as Record<string, unknown>;
  if (m.type !== 'insert') return { ok: false, error: 'Not an insert message.' };
  if (typeof m.svg !== 'string') return { ok: false, error: 'Missing SVG.' };
  if (m.svg.length > MAX_SVG_LENGTH) return { ok: false, error: 'SVG is too large.' };
  if (!isSvgMarkup(m.svg)) return { ok: false, error: 'Not a valid, safe SVG document.' };
  if (!isStyle(m.style)) return { ok: false, error: 'Unknown icon style.' };
  const fields: Array<[string, number]> = [
    ['name', 128],
    ['source', 64],
    ['license', 128],
    ['id', 128],
  ];
  for (const [key, max] of fields) {
    const v = m[key];
    if (typeof v !== 'string' || v.length === 0 || v.length > max || !SAFE_LABEL.test(v)) {
      return { ok: false, error: `Invalid ${key}.` };
    }
  }
  let color: string | null = null;
  if (m.color !== undefined && m.color !== null) {
    if (typeof m.color !== 'string' || !HEX_COLOR.test(m.color)) return { ok: false, error: 'Invalid color.' };
    color = m.color.toLowerCase();
  }
  return {
    ok: true,
    value: {
      svg: m.svg.trim(),
      name: m.name as string,
      style: m.style,
      source: m.source as string,
      license: m.license as string,
      id: m.id as string,
      color,
    },
  };
}

/** Replaces every `currentColor` with a concrete hex color (default black). */
export function applyColor(svg: string, color: string | null): string {
  const hex = color && HEX_COLOR.test(color) ? color : DEFAULT_COLOR;
  return svg.replace(/currentColor/gi, hex);
}

export function iconNodeName(style: IconStyle, name: string): string {
  return `typeicon/${style}/${name}`;
}

/**
 * Scale steps that bring the longest side to `target`. Figma's rescale()
 * requires factor >= 0.01, so very large viewBoxes are scaled in stages.
 */
export function rescaleSteps(width: number, height: number, target = ICON_SIZE): number[] {
  const longest = Math.max(width, height);
  if (!(longest > 0) || !Number.isFinite(longest)) return [];
  let remaining = target / longest;
  const steps: number[] = [];
  while (remaining < 0.01) {
    steps.push(0.01);
    remaining /= 0.01;
  }
  if (Math.abs(remaining - 1) > 1e-9) steps.push(remaining);
  return steps;
}
