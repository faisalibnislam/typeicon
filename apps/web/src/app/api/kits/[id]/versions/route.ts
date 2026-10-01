import { createHash } from "node:crypto";
import { NextResponse } from "next/server";
import { sql } from "drizzle-orm";
import { z } from "zod";
import { db } from "@/db";
import { handle, readJson, styleSlug, uuid } from "@/lib/api";
import { audit } from "@/lib/audit";
import { BUILD_FORMATS, TOOLCHAIN, resolveItems } from "@/lib/builds";
import { capabilitiesFor } from "@/lib/entitlements";
import { ownKit } from "@/lib/ownership";
import { hitRateLimit } from "@/lib/rate-limit";
import { apiUser, HttpError } from "@/lib/session";

type Ctx = { params: Promise<{ id: string }> };

const body = z.object({
  items: z.array(z.object({ designId: uuid, style: styleSlug })).max(5000),
  customIconIds: z.array(uuid).max(2000),
  formats: z.array(z.enum(BUILD_FORMATS)).min(1),
});

/** Save an immutable kit version (pinned to the kit's release) and queue its private build. */
export const POST = handle(async (req, ctx: Ctx) => {
  const user = await apiUser();
  const { id } = await ctx.params;
  await ownKit(user.id, id);
  const caps = await capabilitiesFor(user.id);
  const input = await readJson(req, body, 512 * 1024);
  const items = await resolveItems(input.items);
  if (items.length !== input.items.length) throw new HttpError(422, "Some selected icon styles are not published.");
  if (items.length + input.customIconIds.length === 0) throw new HttpError(422, "A kit version needs at least one icon.");
  if (items.length > caps.maxSubsetIcons) throw new HttpError(422, `At most ${caps.maxSubsetIcons} catalog icon styles per kit on the ${caps.plan} plan.`);
  if (input.customIconIds.length) {
    const own = await db.execute(sql`SELECT count(*)::int AS n FROM custom_icons WHERE kit_id = ${id} AND owner_id = ${user.id}
      AND status = 'ready' AND archived_at IS NULL AND id IN (${sql.join(input.customIconIds.map((c) => sql`${c}`), sql`, `)})`);
    if (Number((own.rows[0] as { n: number }).n) !== new Set(input.customIconIds).size) throw new HttpError(422, "Custom icons must belong to this kit and pass validation first.");
  }
  const rl = await hitRateLimit(`kit:user:${user.id}`, Number(process.env.KIT_BUILDS_PER_HOUR ?? 20), 3600);
  if (!rl.ok) throw new HttpError(429, "Kit build limit reached for this hour.");

  const selection = { items: items.map((i) => ({ designId: i.designId, style: i.style, variantId: i.variantId })), customIconIds: [...new Set(input.customIconIds)].sort() };
  const release = await db.execute(sql`SELECT r.version FROM kits k JOIN releases r ON r.id = k.pinned_release_id WHERE k.id = ${id}`);
  const releaseVersion = (release.rows[0] as { version: string } | undefined)?.version;
  if (!releaseVersion) throw new HttpError(409, "This kit is not pinned to a published release.");
  const contentHash = createHash("sha256")
    .update(JSON.stringify({ items: items.map((i) => `${i.variantId}:${i.svgSha256}`).sort(), custom: selection.customIconIds, formats: [...input.formats].sort(), release: releaseVersion, toolchain: TOOLCHAIN }))
    .digest("hex");

  const out = await db.transaction(async (tx) => {
    const k = await tx.execute(sql`UPDATE kits SET current_version = current_version + 1, updated_at = now() WHERE id = ${id} RETURNING current_version, slug`);
    const { current_version: version, slug } = k.rows[0] as { current_version: number; slug: string };
    const v = await tx.execute(sql`
      INSERT INTO kit_versions (kit_id, version, selection, formats, content_hash, created_by)
      VALUES (${id}, ${version}, ${JSON.stringify(selection)}::jsonb, ARRAY[${sql.join(input.formats.map((f) => sql`${f}`), sql`, `)}]::text[], ${contentHash}, ${user.id})
      RETURNING id`);
    const kitVersionId = (v.rows[0] as { id: string }).id;
    // Private scope: cache keys include the owner, so private assets never leak through a shared cache.
    const scope = `private:${user.id}`;
    const cacheKey = createHash("sha256").update(`${scope}|${slug}|${contentHash}`).digest("hex");
    const j = await tx.execute(sql`
      INSERT INTO jobs (kind, owner_id, scope, cache_key, payload)
      VALUES ('kit_build', ${user.id}, ${scope}, ${cacheKey},
              ${JSON.stringify({ kitId: id, kitVersionId, version, slug, formats: input.formats, release: releaseVersion, toolchain: TOOLCHAIN, hosted: caps.hostedKits })}::jsonb)
      RETURNING id`);
    return { version, kitVersionId, jobId: (j.rows[0] as { id: string }).id };
  });
  await audit(user.id, "kit.version", "kit", id, { version: out.version, items: items.length, custom: input.customIconIds.length });
  return NextResponse.json(out, { status: 202 });
});
