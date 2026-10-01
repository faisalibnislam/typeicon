import "server-only";
import { createHash } from "node:crypto";
import { sql } from "drizzle-orm";
import { db } from "@/db";

export const TOOLCHAIN = "typeicon-fonts/0.1.0";
export const BUILD_FORMATS = ["otf", "ttf", "woff2", "woff", "svg", "css"] as const;
export type BuildFormat = (typeof BUILD_FORMATS)[number];

export function slugify(name: string): string {
  return (
    name
      .toLowerCase()
      .normalize("NFKD")
      .replace(/[̀-ͯ]/g, "")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "")
      .slice(0, 32) || "subset"
  );
}

export interface ResolvedItem {
  variantId: string;
  designId: string;
  name: string;
  style: string;
  source: string;
  sourceName: string;
  license: string;
  route: string;
  fontSupported: boolean;
  svgSha256: string;
}

export async function resolveItems(items: { designId: string; style: string }[]): Promise<ResolvedItem[]> {
  if (!items.length) return [];
  const pairs = sql.join(items.map((i) => sql`(${i.designId}::uuid, ${i.style}::text)`), sql`, `);
  const r = await db.execute(sql`
    SELECT v.id AS variant_id, d.id AS design_id, d.name, v.style, sp.slug AS source, sp.display_name, d.license_id,
           v.route, v.font_supported, v.svg_sha256
    FROM (VALUES ${pairs}) AS want(design_id, style)
    JOIN variants v ON v.design_id = want.design_id AND v.style = want.style AND v.status = 'published'
    JOIN designs d ON d.id = v.design_id AND d.status = 'published'
    JOIN source_packs sp ON sp.id = d.source_pack_id
    ORDER BY sp.slug, v.style, d.name`);
  return (r.rows as Record<string, unknown>[]).map((x) => ({
    variantId: x.variant_id as string,
    designId: x.design_id as string,
    name: x.name as string,
    style: x.style as string,
    source: x.source as string,
    sourceName: x.display_name as string,
    license: x.license_id as string,
    route: x.route as string,
    fontSupported: Boolean(x.font_supported),
    svgSha256: x.svg_sha256 as string,
  }));
}

/** Cache key covers asset versions, selection, formats, naming, toolchain and access scope. */
export function buildCacheKey(parts: { scope: string; slug: string; formats: string[]; items: ResolvedItem[]; release: string; extra?: string }) {
  const h = createHash("sha256");
  h.update(JSON.stringify({
    toolchain: TOOLCHAIN,
    scope: parts.scope,
    slug: parts.slug,
    release: parts.release,
    formats: [...parts.formats].sort(),
    items: parts.items.map((i) => `${i.variantId}:${i.svgSha256}`).sort(),
    extra: parts.extra ?? "",
  }));
  return h.digest("hex");
}

export interface JobView {
  id: string;
  kind: string;
  status: string;
  error: string | null;
  attempts: number;
  createdAt: string;
  startedAt: string | null;
  finishedAt: string | null;
  result: Record<string, unknown> | null;
  cached: boolean;
}

export async function getJob(id: string): Promise<(JobView & { ownerId: string | null; scope: string }) | null> {
  const r = await db.execute(sql`SELECT id, kind, status, error, attempts, created_at, started_at, finished_at, result, owner_id, scope, payload
                                 FROM jobs WHERE id = ${id}`);
  const x = r.rows[0] as Record<string, unknown> | undefined;
  if (!x) return null;
  return {
    id: x.id as string,
    kind: x.kind as string,
    status: x.status as string,
    error: (x.error as string) ?? null,
    attempts: Number(x.attempts),
    createdAt: String(x.created_at),
    startedAt: x.started_at ? String(x.started_at) : null,
    finishedAt: x.finished_at ? String(x.finished_at) : null,
    result: (x.result as Record<string, unknown>) ?? null,
    cached: Boolean((x.payload as Record<string, unknown>)?.cachedFrom),
    ownerId: (x.owner_id as string) ?? null,
    scope: x.scope as string,
  };
}
