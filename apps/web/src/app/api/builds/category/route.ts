import { sql } from "drizzle-orm";
import { z } from "zod";
import { db } from "@/db";
import { handle, readJson, styleSlug } from "@/lib/api";
import { BUILD_FORMATS } from "@/lib/builds";
import { getSessionUser, HttpError } from "@/lib/session";
import { queueSubsetBuild } from "@/lib/subset-queue";

/** Category pack: every published font-ready icon in a category + style + pack, built as a cached subset. */
export const POST = handle(async (req) => {
  const user = await getSessionUser();
  const input = await readJson(req, z.object({
    category: z.string().regex(/^[a-z0-9-]{1,64}$/),
    style: styleSlug,
    pack: z.string().regex(/^[a-z0-9-]{1,40}$/),
    formats: z.array(z.enum(BUILD_FORMATS)).min(1),
  }));
  const r = await db.execute(sql`
    SELECT d.id AS design_id, v.style FROM designs d JOIN variants v ON v.design_id = d.id AND v.style = ${input.style} AND v.status = 'published'
    JOIN source_packs sp ON sp.id = d.source_pack_id
    WHERE d.status = 'published' AND sp.slug = ${input.pack} AND d.category_slugs @> ARRAY[${input.category}]::text[]
    ORDER BY d.name LIMIT 501`);
  const items = (r.rows as { design_id: string; style: string }[]).map((x) => ({ designId: x.design_id, style: x.style }));
  if (!items.length) throw new HttpError(404, "No icons in this category, pack and style.");
  return queueSubsetBuild(req, user, { name: `${input.pack} ${input.category} ${input.style}`, items, formats: input.formats });
});
