export const fmt = (n: number) => new Intl.NumberFormat("en-US").format(n);
export const hex = (cp: number) => `U+${cp.toString(16).toUpperCase().padStart(4, "0")}`;
export function bytes(n: number): string {
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(n < 10240 ? 1 : 0)} KB`;
  return `${(n / 1024 / 1024).toFixed(1)} MB`;
}
export const STYLE_LABEL: Record<string, string> = { filled: "Filled", line: "Line", rounded: "Rounded", thin: "Thin", brand: "Brand" };
export const cssEscapeCodepoint = (cp: number) => `\\${cp.toString(16).toUpperCase()}`;
