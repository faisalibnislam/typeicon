import { NextResponse } from "next/server";
import { sql } from "drizzle-orm";
import { z } from "zod";
import { db } from "@/db";
import { handle, readJson } from "@/lib/api";
import { audit } from "@/lib/audit";
import { getKit } from "@/lib/kits";
import { ownKit } from "@/lib/ownership";
import { apiUser } from "@/lib/session";

type Ctx = { params: Promise<{ id: string }> };

export const GET = handle(async (_req, ctx: Ctx) => {
  const user = await apiUser();
  const { id } = await ctx.params;
  await ownKit(user.id, id);
  return NextResponse.json(await getKit(id));
});

const patch = z.object({
  name: z.string().trim().min(1).max(60).optional(),
  // Usage control only: browsers send Origin/Referer, but font files served publicly can still be fetched directly.
  allowedDomains: z.array(z.string().trim().toLowerCase().regex(/^(\*\.)?[a-z0-9-]+(\.[a-z0-9-]+)+$|^localhost(:\d+)?$/)).max(20).optional(),
});

export const PATCH = handle(async (req, ctx: Ctx) => {
  const user = await apiUser();
  const { id } = await ctx.params;
  await ownKit(user.id, id);
  const body = await readJson(req, patch);
  if (body.name) await db.execute(sql`UPDATE kits SET name = ${body.name}, updated_at = now() WHERE id = ${id}`);
  if (body.allowedDomains) {
    const arr = sql`ARRAY[${sql.join(body.allowedDomains.map((d) => sql`${d}`), sql`, `)}]::text[]`;
    await db.execute(sql`UPDATE kits SET allowed_domains = ${body.allowedDomains.length ? arr : sql`'{}'::text[]`}, updated_at = now() WHERE id = ${id}`);
  }
  return NextResponse.json({ ok: true });
});

export const DELETE = handle(async (_req, ctx: Ctx) => {
  const user = await apiUser();
  const { id } = await ctx.params;
  await ownKit(user.id, id);
  await db.execute(sql`DELETE FROM kits WHERE id = ${id}`);
  await audit(user.id, "kit.delete", "kit", id);
  return NextResponse.json({ ok: true });
});
