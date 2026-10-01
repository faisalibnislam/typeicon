import { NextResponse } from "next/server";
import { sql } from "drizzle-orm";
import { z } from "zod";
import { db } from "@/db";
import { handle, readJson, styleSlug, uuid } from "@/lib/api";
import { audit } from "@/lib/audit";
import { capabilitiesFor } from "@/lib/entitlements";
import { KIT_CODEPOINT_BASE, KIT_CODEPOINT_LIMIT } from "@/lib/kits";
import { ownKit } from "@/lib/ownership";
import { apiUser, HttpError } from "@/lib/session";

type Ctx = { params: Promise<{ id: string }> };
const MAX_BYTES = Number(process.env.MAX_CUSTOM_SVG_BYTES ?? 65536);

const upload = z.object({
  name: z.string().regex(/^(?=.{2,48}$)[a-z0-9]+(?:-[a-z0-9]+)*$/, "Use 2–48 lowercase letters, digits and hyphens"),
  style: styleSlug,
  svg: z.string().min(20).max(MAX_BYTES),
});

/**
 * Upload a private custom SVG. The web tier only stores it (bounded, never rendered).
 * The worker's hardened sanitizer (no DTD/entities/network, allow-listed elements) validates
 * it, converts it to a font outline, and marks it ready or rejected.
 */
export const POST = handle(async (req, ctx: Ctx) => {
  const user = await apiUser();
  const { id } = await ctx.params;
  await ownKit(user.id, id);
  const caps = await capabilitiesFor(user.id);
  const body = await readJson(req, upload, MAX_BYTES + 4096);
  if (!/^\s*(<\?xml[^>]*>\s*)?<svg[\s>]/i.test(body.svg)) throw new HttpError(422, "The file must be an SVG document.");
  const used = await db.execute(sql`SELECT count(*)::int AS n FROM custom_icons WHERE owner_id = ${user.id} AND archived_at IS NULL`);
  if (Number((used.rows[0] as { n: number }).n) >= caps.customIcons) {
    throw new HttpError(403, caps.customIcons ? `The ${caps.plan} plan allows ${caps.customIcons} custom icons.` : `Custom icons are not included in the ${caps.plan} plan.`);
  }
  // Name collisions: never shadow a Core name or alias, and unique per kit + style.
  const clash = await db.execute(sql`SELECT kind FROM name_registry WHERE namespace = 'core' AND name = ${body.name}
                                     UNION ALL SELECT 'custom' FROM custom_icons WHERE kit_id = ${id} AND name = ${body.name} AND style = ${body.style} AND archived_at IS NULL`);
  if (clash.rows.length) throw new HttpError(409, `"${body.name}" is already used by ${(clash.rows[0] as { kind: string }).kind === "custom" ? "another custom icon in this kit" : "a TypeIcon Core icon"}.`);
  const r = await db.transaction(async (tx) => {
    // Lock the kit row so concurrent uploads allocate codepoints one at a time.
    await tx.execute(sql`SELECT id FROM kits WHERE id = ${id} FOR UPDATE`);
    // Codepoint: reuse the kit's existing assignment for this name (shared across styles), else allocate the next one. Never reused.
    const existing = await tx.execute(sql`SELECT codepoint FROM custom_icons WHERE kit_id = ${id} AND name = ${body.name} LIMIT 1`);
    let cp = (existing.rows[0] as { codepoint: number } | undefined)?.codepoint;
    if (!cp) {
      const max = await tx.execute(sql`SELECT coalesce(max(codepoint), ${KIT_CODEPOINT_BASE - 1})::int AS m FROM custom_icons WHERE kit_id = ${id}`);
      cp = Number((max.rows[0] as { m: number }).m) + 1;
      if (cp >= KIT_CODEPOINT_BASE + KIT_CODEPOINT_LIMIT) throw new HttpError(409, "This kit has used all custom codepoints.");
    }
    const ins = await tx.execute(sql`
      INSERT INTO custom_icons (owner_id, kit_id, name, style, status, raw_svg, codepoint)
      VALUES (${user.id}, ${id}, ${body.name}, ${body.style}, 'pending', ${body.svg}, ${cp}) RETURNING id`);
    const iconId = (ins.rows[0] as { id: string }).id;
    await tx.execute(sql`INSERT INTO jobs (kind, owner_id, scope, payload, max_attempts)
                         VALUES ('custom_icon_check', ${user.id}, ${`private:${user.id}`}, ${JSON.stringify({ customIconId: iconId, kitId: id })}::jsonb, 2)`);
    return { iconId, codepoint: cp };
  });
  await audit(user.id, "custom_icon.upload", "custom_icon", r.iconId, { kitId: id, bytes: body.svg.length });
  return NextResponse.json({ id: r.iconId, codepoint: r.codepoint, status: "pending" }, { status: 202 });
});

export const DELETE = handle(async (req, ctx: Ctx) => {
  const user = await apiUser();
  const { id } = await ctx.params;
  await ownKit(user.id, id);
  const body = await readJson(req, z.object({ iconId: uuid }));
  await db.execute(sql`UPDATE custom_icons SET archived_at = now(), raw_svg = NULL WHERE id = ${body.iconId} AND kit_id = ${id} AND owner_id = ${user.id}`);
  return NextResponse.json({ ok: true });
});
