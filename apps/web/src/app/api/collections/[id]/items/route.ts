import { NextResponse } from "next/server";
import { sql } from "drizzle-orm";
import { z } from "zod";
import { db } from "@/db";
import { handle, readJson, styleSlug, uuid } from "@/lib/api";
import { apiUser, HttpError } from "@/lib/session";
import { ownCollection } from "@/lib/ownership";

type Ctx = { params: Promise<{ id: string }> };
const item = z.object({ designId: uuid, style: styleSlug });

export const POST = handle(async (req, ctx: Ctx) => {
  const user = await apiUser();
  const { id } = await ctx.params;
  await ownCollection(user.id, id);
  const body = await readJson(req, item);
  const r = await db.execute(sql`
    INSERT INTO collection_items (collection_id, design_id, style, position)
    SELECT ${id}, v.design_id, v.style, coalesce((SELECT max(position) + 1 FROM collection_items WHERE collection_id = ${id}), 0)
    FROM variants v JOIN designs d ON d.id = v.design_id
    WHERE v.design_id = ${body.designId} AND v.style = ${body.style} AND v.status = 'published' AND d.status = 'published'
    ON CONFLICT DO NOTHING RETURNING design_id`);
  const exists = await db.execute(sql`SELECT 1 FROM variants WHERE design_id = ${body.designId} AND style = ${body.style} AND status = 'published'`);
  if (!exists.rows.length) throw new HttpError(404, "That icon style is not published");
  await db.execute(sql`UPDATE collections SET updated_at = now() WHERE id = ${id}`);
  return NextResponse.json({ added: r.rows.length > 0 });
});

export const DELETE = handle(async (req, ctx: Ctx) => {
  const user = await apiUser();
  const { id } = await ctx.params;
  await ownCollection(user.id, id);
  const body = await readJson(req, item);
  await db.execute(sql`DELETE FROM collection_items WHERE collection_id = ${id} AND design_id = ${body.designId} AND style = ${body.style}`);
  return NextResponse.json({ ok: true });
});
