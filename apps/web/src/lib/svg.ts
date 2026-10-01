/**
 * Defense in depth for rendering catalog SVG markup inline. Catalog SVGs are sanitized by the
 * import pipeline (allow-listed elements/attributes). This second check refuses anything that
 * could execute or load external content if a row were ever tampered with.
 */
const FORBIDDEN = /<\s*(script|foreignObject|iframe|image|use|a|style|animate|set)\b|\son[a-z]+\s*=|(?:href|xlink:href)\s*=|javascript:|url\(\s*['"]?(?!#)/i;

export function isSafeSvg(svg: string | null | undefined): svg is string {
  return typeof svg === "string" && svg.startsWith("<svg") && svg.length < 600_000 && !FORBIDDEN.test(svg);
}

/** Add sizing/a11y attributes to the root element. */
export function sizedSvg(svg: string, opts: { size?: number | string; label?: string; className?: string } = {}): string {
  const attrs: string[] = [];
  if (opts.size !== undefined) {
    const vb = svg.match(/viewBox="([^"]+)"/)?.[1]?.split(/[\s,]+/).map(Number);
    const ratio = vb && vb[3] > 0 ? vb[2] / vb[3] : 1;
    const h = typeof opts.size === "number" ? opts.size : opts.size;
    const w = typeof opts.size === "number" ? Math.round(opts.size * ratio * 100) / 100 : opts.size;
    attrs.push(`width="${w}"`, `height="${h}"`);
  }
  if (opts.label) attrs.push(`role="img"`, `aria-label="${opts.label.replace(/["<>&]/g, "")}"`);
  else attrs.push(`aria-hidden="true"`, `focusable="false"`);
  if (opts.className) attrs.push(`class="${opts.className.replace(/["<>&]/g, "")}"`);
  return svg.replace(/^<svg\b/, `<svg ${attrs.join(" ")}`);
}

/** Wrap the SVG's children in a transform group (rotation/flip) for previews and downloads. */
export function transformedSvg(svg: string, t: { rotate: number; flipX: boolean; flipY: boolean }): string {
  if (!t.rotate && !t.flipX && !t.flipY) return svg;
  const vb = svg.match(/viewBox="([^"]+)"/)?.[1]?.split(/[\s,]+/).map(Number) ?? [0, 0, 24, 24];
  const cx = vb[0] + vb[2] / 2;
  const cy = vb[1] + vb[3] / 2;
  const parts = [`translate(${cx} ${cy})`];
  if (t.rotate) parts.push(`rotate(${t.rotate})`);
  if (t.flipX || t.flipY) parts.push(`scale(${t.flipX ? -1 : 1} ${t.flipY ? -1 : 1})`);
  parts.push(`translate(${-cx} ${-cy})`);
  return svg.replace(/^(<svg[^>]*>)([\s\S]*)(<\/svg>)$/, `$1<g transform="${parts.join(" ")}">$2</g>$3`);
}

/** Replace currentColor with an explicit colour (for downloads that should carry a colour). */
export function coloredSvg(svg: string, color: string | null): string {
  if (!color || !/^#[0-9a-fA-F]{3,8}$/.test(color)) return svg;
  return svg.replace(/currentColor/g, color);
}
