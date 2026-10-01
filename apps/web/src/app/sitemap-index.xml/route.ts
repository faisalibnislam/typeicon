import { sql } from "drizzle-orm";
import { db } from "@/db";

const PER = 40_000;

/** Sitemap index listing the page sitemap and the non-empty icon sitemaps. */
export async function GET() {
  const base = (process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3107").replace(/\/$/, "");
  const r = await db.execute(sql`SELECT count(*)::int AS n FROM designs WHERE status = 'published'`);
  const chunks = Math.max(1, Math.ceil(Number((r.rows[0] as { n: number }).n) / PER));
  const urls = [`${base}/sitemap.xml`, ...Array.from({ length: chunks }, (_, i) => `${base}/icons/sitemap/${i}.xml`)];
  const body = `<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls
    .map((u) => `  <sitemap><loc>${u}</loc></sitemap>`)
    .join("\n")}\n</sitemapindex>\n`;
  return new Response(body, { headers: { "content-type": "application/xml; charset=utf-8", "cache-control": "public, max-age=3600" } });
}
