import type { MetadataRoute } from "next";
import { sql } from "drizzle-orm";
import { db } from "@/db";

export const dynamic = "force-dynamic";
export const ICONS_PER_SITEMAP = 40_000; // below the 50,000-URL protocol limit
export const ICON_SITEMAPS = 8; // capacity 320,000 canonical icon pages; unused chunks are empty

export async function generateSitemaps() {
  return Array.from({ length: ICON_SITEMAPS }, (_, id) => ({ id }));
}

/** One canonical URL per published design (style variants are query params and not listed separately). */
export default async function sitemap(props: { id: Promise<string> }): Promise<MetadataRoute.Sitemap> {
  const id = Number(await props.id);
  const base = (process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3107").replace(/\/$/, "");
  const r = await db.execute(sql`SELECT name, updated_at FROM designs WHERE status = 'published'
                                 ORDER BY (area <> 'core'), name LIMIT ${ICONS_PER_SITEMAP} OFFSET ${id * ICONS_PER_SITEMAP}`);
  return (r.rows as { name: string; updated_at: string }[]).map((d) => ({ url: `${base}/icons/${d.name}`, lastModified: new Date(d.updated_at) }));
}
