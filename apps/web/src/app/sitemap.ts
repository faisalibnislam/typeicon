import type { MetadataRoute } from "next";
import { sql } from "drizzle-orm";
import { db } from "@/db";
import { docs } from "@/content/docs";

export const dynamic = "force-dynamic";
const site = () => (process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3107").replace(/\/$/, "");

/** Non-icon pages. Icon detail pages are in /icons/sitemap/<n>.xml; both are listed in /sitemap-index.xml. */
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const base = site();
  const [cats, packs] = await Promise.all([
    db.execute(sql`SELECT slug FROM categories c WHERE EXISTS (SELECT 1 FROM design_categories dc JOIN designs d ON d.id = dc.design_id AND d.status = 'published' WHERE dc.category_id = c.id)`),
    db.execute(sql`SELECT slug FROM source_packs WHERE review_status = 'approved'`),
  ]);
  const fixed = ["", "/icons", "/downloads", "/docs", "/categories", "/packs", "/licenses", "/changelog", "/styles/filled", "/styles/line", "/styles/rounded", "/styles/thin"];
  return [
    ...fixed.map((p) => ({ url: `${base}${p}`, changeFrequency: "weekly" as const, priority: p === "" ? 1 : 0.8 })),
    ...docs.map((d) => ({ url: `${base}/docs/${d.meta.slug}`, changeFrequency: "monthly" as const, priority: 0.6 })),
    ...(cats.rows as { slug: string }[]).map((c) => ({ url: `${base}/categories/${c.slug}`, priority: 0.5 })),
    ...(packs.rows as { slug: string }[]).map((p) => ({ url: `${base}/packs/${p.slug}`, priority: 0.6 })),
  ];
}
