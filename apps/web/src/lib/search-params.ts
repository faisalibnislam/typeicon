/** Catalog URL state: parsing, validation and serialization (shared by server and client). */
import { z } from "zod";

/** Core styles (every Core icon has all three) plus the single "brand" style of brand logos. */
export const STYLE_SLUGS = ["filled", "line", "rounded", "thin", "brand"] as const;
export const CORE_STYLES = ["filled", "line", "rounded", "thin"] as const;
export type StyleSlug = (typeof STYLE_SLUGS)[number];
export const PER_PAGE_OPTIONS = [48, 96, 192] as const;
export const MAX_QUERY_LENGTH = 64;

const slug = z.string().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/).max(64);
const list = (max: number) =>
  z
    .union([z.string(), z.array(z.string())])
    .optional()
    .transform((v) => (v === undefined ? [] : Array.isArray(v) ? v : v.split(",")))
    .transform((v) => [...new Set(v.filter((s) => slug.safeParse(s).success))].slice(0, max));

export const searchParamsSchema = z.object({
  q: z
    .string()
    .optional()
    .transform((v) => (v ?? "").slice(0, MAX_QUERY_LENGTH)),
  style: z.enum(["all", ...STYLE_SLUGS]).catch("all").default("all"),
  category: list(10),
  pack: list(10),
  license: z
    .union([z.string(), z.array(z.string())])
    .optional()
    .transform((v) => (v === undefined ? [] : Array.isArray(v) ? v : v.split(",")))
    .transform((v) => v.filter((s) => /^[A-Za-z0-9.+-]{1,64}$/.test(s)).slice(0, 5)),
  area: z.enum(["all", "core", "brands"]).catch("all").default("all"),
  brands: z.enum(["include", "exclude", "only"]).catch("include").default("include"),
  sort: z.enum(["relevance", "name", "pack"]).catch("relevance").default("relevance"),
  page: z.coerce.number().int().min(1).max(500).catch(1).default(1),
  per: z.coerce
    .number()
    .refine((n) => (PER_PAGE_OPTIONS as readonly number[]).includes(n))
    .catch(96)
    .default(96),
  missing: z
    .enum(["0", "1"])
    .catch("0")
    .default("0")
    .transform((v) => v === "1"),
});
export type SearchInput = z.infer<typeof searchParamsSchema>;

export interface IconCard {
  id: string;
  name: string;
  localName: string;
  area: "core" | "brands";
  isBrand: boolean;
  source: string;
  sourceName: string;
  license: string;
  codepoint: number | null;
  styles: StyleSlug[];
  displayStyle: StyleSlug | null;
  svg: string | null;
}

export interface Facet {
  value: string;
  label: string;
  count: number;
}


export function parseSearchParams(raw: Record<string, string | string[] | undefined>): SearchInput {
  return searchParamsSchema.parse(raw);
}

/** Lowercase ASCII, spaces/underscores -> hyphen, anything else dropped. */
export function normalizeQuery(q: string): string {
  return q
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[_\s]+/g, "-")
    .replace(/[^a-z0-9-]/g, "")
    .replace(/-{2,}/g, "-")
    .replace(/^-|-$/g, "")
    .slice(0, MAX_QUERY_LENGTH);
}

/** Serialize search input back to a URL query string (stable key order, defaults omitted). */
export function toQueryString(input: Partial<SearchInput>, overrides: Partial<SearchInput> = {}): string {
  const v = { ...input, ...overrides };
  const p = new URLSearchParams();
  if (v.q) p.set("q", v.q);
  if (v.style && v.style !== "all") p.set("style", v.style);
  if (v.category?.length) p.set("category", v.category.join(","));
  if (v.pack?.length) p.set("pack", v.pack.join(","));
  if (v.license?.length) p.set("license", v.license.join(","));
  if (v.area && v.area !== "all") p.set("area", v.area);
  if (v.brands && v.brands !== "include") p.set("brands", v.brands);
  if (v.sort && v.sort !== "relevance") p.set("sort", v.sort);
  if (v.per && v.per !== 96) p.set("per", String(v.per));
  if (v.missing) p.set("missing", "1");
  if (v.page && v.page > 1) p.set("page", String(v.page));
  const s = p.toString();
  return s ? `?${s}` : "";
}
