import { NextResponse } from "next/server";
import { sql } from "drizzle-orm";
import { z } from "zod";
import { db } from "@/db";
import { handle, readJson, styleSlug, uuid } from "@/lib/api";
import { audit } from "@/lib/audit";
import { apiUser } from "@/lib/session";

export const GET = handle(async () => {
  const user = await apiUser();
  const r = await db.execute(sql`
    SELECT c.id, c.name, c.is_public, c.updated_at, count(ci.design_id)::int AS items
    FROM collections c LEFT JOIN collection_items ci ON ci.collection_id = c.id
    WHERE c.owner_id = ${user.id} GROUP BY c.id ORDER BY c.updated_at DESC LIMIT 200`);
  return NextResponse.json({ collections: r.rows });
});

const createBody = z.object({
  name: z.string().trim().min(1).max(80),
  items: z.array(z.object({ designId: uuid, style: styleSlug })).max(500).optional(),
});

export const POST = handle(async (req) => {
  const user = await apiUser();
  const body = await readJson(req, createBody);
  const count = await db.execute(sql`SELECT count(*)::int AS n FROM collections WHERE owner_id = ${user.id}`);
  if (Number((count.rows[0] as { n: number }).n) >= 200) return NextResponse.json({ error: "Collection limit reached" }, { status: 409 });
  const id = await db.transaction(async (tx) => {
    const r = await tx.execute(sql`INSERT INTO collections (owner_id, name) VALUES (${user.id}, ${body.name}) RETURNING id`);
    const cid = (r.rows[0] as { id: string }).id;
    for (const [i, it] of (body.items ?? []).entries()) {
      await tx.execute(sql`
        INSERT INTO collection_items (collection_id, design_id, style, position)
        SELECT ${cid}, v.design_id, v.style, ${i} FROM variants v JOIN designs d ON d.id = v.design_id
        WHERE v.design_id = ${it.designId} AND v.style = ${it.style} AND v.status = 'published' AND d.status = 'published'
        ON CONFLICT DO NOTHING`);
    }
    return cid;
  });
  await audit(user.id, "collection.create", "collection", id, { items: body.items?.length ?? 0 });
  return NextResponse.json({ id }, { status: 201 });
});
