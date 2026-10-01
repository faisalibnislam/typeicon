// @typeicon/catalog: small helpers over the TypeIcon metadata.
// Importing this module does NOT load icons.json or any SVG data; per-icon
// metadata is loaded lazily from `dist/icon/<name>.json`.

/** Icon sources (packs) in the release. */
export const SOURCES = Object.freeze(['typeicon-core', 'simple-icons']);

/** Normalised style slots. */
export const STYLES = Object.freeze(['filled', 'line', 'rounded', 'thin', 'brand']);

const NAME_RE = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

/** True when `name` is a syntactically valid TypeIcon icon name. */
export function isValidIconName(name) {
  return typeof name === 'string' && name.length <= 128 && NAME_RE.test(name);
}

/**
 * Load one icon's metadata by name without loading the full catalog.
 * Resolves to `undefined` when no icon has that name.
 */
export async function getIcon(name) {
  if (!isValidIconName(name)) return undefined;
  try {
    const mod = await import(`./dist/icon/${name}.json`, { with: { type: 'json' } });
    return mod.default;
  } catch (error) {
    const code = error && typeof error === 'object' ? error.code : undefined;
    if (code === 'ERR_MODULE_NOT_FOUND' || code === 'ENOENT' || code === 'MODULE_NOT_FOUND') {
      return undefined;
    }
    throw error;
  }
}

/** Find an icon by name (or alias, when `matchAliases` is true) in an already-loaded list. */
export function findIcon(icons, name, { matchAliases = false } = {}) {
  for (const icon of icons) if (icon.name === name) return icon;
  if (matchAliases) {
    for (const icon of icons) if (icon.aliases && icon.aliases.includes(name)) return icon;
  }
  return undefined;
}

/**
 * Framework subpath of an icon style, e.g. `line/home` (Core) or
 * `brands/brand-github` (brand logos). Returns `undefined` if the style
 * does not exist for that icon.
 */
export function iconSubpath(icon, style) {
  if (!icon || !icon.styles || !icon.styles[style]) return undefined;
  if (icon.area === 'core') return `${style}/${icon.name}`;
  return icon.area === 'brands' ? `brands/${icon.name}` : `${icon.source}/${style}/${icon.name}`;
}

/** Full import specifier for a framework package, e.g. `@typeicon/react/line/home`. */
export function iconImportPath(icon, style, framework = 'react') {
  const subpath = iconSubpath(icon, style);
  if (!subpath) return undefined;
  const pkg = framework === 'vue' ? '@typeicon/vue' : '@typeicon/react';
  return `${pkg}/${subpath}`;
}

/** Specifier of the SVG file in `@typeicon/icons-svg`, e.g. `@typeicon/icons-svg/svg/simple-icons/brand/brand-github.svg`. */
export function svgImportPath(icon, style) {
  const variant = icon && icon.styles ? icon.styles[style] : undefined;
  return variant ? `@typeicon/icons-svg/${variant.svg}` : undefined;
}
