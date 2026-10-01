import { NextResponse } from "next/server";
import { sql } from "drizzle-orm";
import { z } from "zod";
import { db } from "@/db";
import { recomputeStats } from "@/lib/admin";
import { handle, readJson, uuid } from "@/lib/api";
import { audit } from "@/lib/audit";
import { apiUser, HttpError } from "@/lib/session";

/** Design QA decision on one variant. Rejected variants are unpublished; approval republishes if it passed validation. */
export const POST = handle(async (req, ctx: { params: Promise<{ id: string }> }) => {
  const admin = await apiUser({ admin: true });
  const { id } = await ctx.params;
  if (!uuid.safeParse(id).success) throw new HttpError(404, "Not found");
  const body = await readJson(req, z.object({ decision: z.enum(["approved", "rejected"]), note: z.string().max(500).optional() }));
  const r = await db.execute(sql`UPDATE variants SET review_status = ${body.decision},
      status = CASE WHEN ${body.decision} = 'approved' AND route <> 'rejected' THEN 'published' ELSE 'rejected' END, updated_at = now()
    WHERE id = ${id} RETURNING design_id`);
  if (!r.rows.length) throw new HttpError(404, "Not found");
  const designId = (r.rows[0] as { design_id: string }).design_id;
  await db.execute(sql`UPDATE designs d SET published_styles = coalesce((SELECT array_agg(v.style ORDER BY v.style) FROM variants v WHERE v.design_id = d.id AND v.status = 'published'), '{}'),
    status = CASE WHEN EXISTS (SELECT 1 FROM variants v WHERE v.design_id = d.id AND v.status = 'published') THEN 'published' ELSE 'pending' END WHERE d.id = ${designId}`);
  await recomputeStats();
  await audit(admin.id, `variant.${body.decision}`, "variant", id, { note: body.note });
  return NextResponse.json({ ok: true });
});
