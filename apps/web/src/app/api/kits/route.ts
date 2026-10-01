import { NextResponse } from "next/server";
import { sql } from "drizzle-orm";
import { z } from "zod";
import { db } from "@/db";
import { handle, readJson } from "@/lib/api";
import { audit } from "@/lib/audit";
import { slugify } from "@/lib/builds";
import { capabilitiesFor } from "@/lib/entitlements";
import { newEmbedId } from "@/lib/kits";
import { apiUser, HttpError } from "@/lib/session";

export const GET = handle(async () => {
  const user = await apiUser();
  const r = await db.execute(sql`SELECT id, name, slug, current_version, updated_at FROM kits WHERE owner_id = ${user.id} ORDER BY updated_at DESC`);
  return NextResponse.json({ kits: r.rows });
});

export const POST = handle(async (req) => {
  const user = await apiUser();
  const caps = await capabilitiesFor(user.id);
  const body = await readJson(req, z.object({ name: z.string().trim().min(1).max(60) }));
  const n = await db.execute(sql`SELECT count(*)::int AS n FROM kits WHERE owner_id = ${user.id}`);
  if (Number((n.rows[0] as { n: number }).n) >= caps.kits) throw new HttpError(409, `The ${caps.plan} plan allows ${caps.kits} kits.`);
  let slug = slugify(body.name);
  const clash = await db.execute(sql`SELECT 1 FROM kits WHERE owner_id = ${user.id} AND slug = ${slug}`);
  if (clash.rows.length) slug = `${slug.slice(0, 26)}-${Date.now().toString(36).slice(-5)}`;
  const r = await db.execute(sql`
    INSERT INTO kits (owner_id, name, slug, embed_id, pinned_release_id)
    VALUES (${user.id}, ${body.name}, ${slug}, ${newEmbedId()},
            (SELECT id FROM releases WHERE status = 'published' ORDER BY release_date DESC, created_at DESC LIMIT 1))
    RETURNING id`);
  const id = (r.rows[0] as { id: string }).id;
  await audit(user.id, "kit.create", "kit", id);
  return NextResponse.json({ id }, { status: 201 });
});
