import { NextResponse } from "next/server";
import { sql } from "drizzle-orm";
import { z } from "zod";
import { db } from "@/db";
import { enqueueOutbox, recomputeStats } from "@/lib/admin";
import { handle, readJson } from "@/lib/api";
import { audit } from "@/lib/audit";
import { apiUser, HttpError } from "@/lib/session";

/** Approve or withdraw a whole source pack. Approval publishes its validated variants; withdrawal unpublishes them. */
export const POST = handle(async (req, ctx: { params: Promise<{ slug: string }> }) => {
  const admin = await apiUser({ admin: true });
  const { slug } = await ctx.params;
  const body = await readJson(req, z.object({ status: z.enum(["approved", "rejected", "pending"]), note: z.string().max(500).optional() }));
  const r = await db.transaction(async (tx) => {
    const p = await tx.execute(sql`UPDATE source_packs SET review_status = ${body.status}, reviewed_by = ${admin.email}, reviewed_at = now(),
      review_note = coalesce(${body.note ?? null}, review_note), updated_at = now() WHERE slug = ${slug} RETURNING id`);
    if (!p.rows.length) throw new HttpError(404, "Unknown pack");
    const id = (p.rows[0] as { id: string }).id;
    const target = body.status === "approved" ? "published" : "pending";
    const v = await tx.execute(sql`UPDATE variants v SET status = ${target}, updated_at = now() FROM designs d
      WHERE v.design_id = d.id AND d.source_pack_id = ${id} AND v.status IN ('published','pending') AND v.route <> 'rejected' RETURNING v.id`);
    await tx.execute(sql`UPDATE designs d SET status = CASE WHEN ${target} = 'published' AND EXISTS (SELECT 1 FROM variants v WHERE v.design_id = d.id AND v.status = 'published') THEN 'published' ELSE 'pending' END,
      published_styles = coalesce((SELECT array_agg(v.style ORDER BY v.style) FROM variants v WHERE v.design_id = d.id AND v.status = 'published'), '{}')
      WHERE d.source_pack_id = ${id}`);
    return v.rows.length;
  });
  await recomputeStats();
  await enqueueOutbox("catalog.pack_review", { slug, status: body.status });
  await audit(admin.id, "pack.review", "source_pack", slug, { status: body.status, variants: r });
  return NextResponse.json({ ok: true, variants: r });
});
