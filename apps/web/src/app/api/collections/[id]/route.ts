import { NextResponse } from "next/server";
import { sql } from "drizzle-orm";
import { z } from "zod";
import { db } from "@/db";
import { handle, readJson } from "@/lib/api";
import { ownCollection } from "@/lib/ownership";
import { audit } from "@/lib/audit";
import { apiUser } from "@/lib/session";

type Ctx = { params: Promise<{ id: string }> };

export const PATCH = handle(async (req, ctx: Ctx) => {
  const user = await apiUser();
  const { id } = await ctx.params;
  await ownCollection(user.id, id);
  const body = await readJson(req, z.object({ name: z.string().trim().min(1).max(80).optional(), isPublic: z.boolean().optional() }));
  await db.execute(sql`UPDATE collections SET name = coalesce(${body.name ?? null}, name),
    is_public = coalesce(${body.isPublic ?? null}, is_public), updated_at = now() WHERE id = ${id}`);
  return NextResponse.json({ ok: true });
});

export const DELETE = handle(async (_req, ctx: Ctx) => {
  const user = await apiUser();
  const { id } = await ctx.params;
  await ownCollection(user.id, id);
  await db.execute(sql`DELETE FROM collections WHERE id = ${id}`);
  await audit(user.id, "collection.delete", "collection", id);
  return NextResponse.json({ ok: true });
});
