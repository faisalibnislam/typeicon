import { NextResponse } from "next/server";
import { sql } from "drizzle-orm";
import { db } from "@/db";
import { handle, uuid } from "@/lib/api";
import { audit } from "@/lib/audit";
import { apiUser, HttpError } from "@/lib/session";

/** Retry a failed job (resets attempts; the worker picks it up). */
export const POST = handle(async (_req, ctx: { params: Promise<{ id: string }> }) => {
  const admin = await apiUser({ admin: true });
  const { id } = await ctx.params;
  if (!uuid.safeParse(id).success) throw new HttpError(404, "Not found");
  const r = await db.execute(sql`UPDATE jobs SET status = 'queued', attempts = 0, run_after = now(), error = NULL, locked_by = NULL
                                 WHERE id = ${id} AND status IN ('failed','cancelled') RETURNING id`);
  if (!r.rows.length) throw new HttpError(409, "Only failed or cancelled jobs can be retried");
  await audit(admin.id, "job.retry", "job", id);
  return NextResponse.json({ ok: true });
});
