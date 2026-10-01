import "server-only";
import { NextResponse } from "next/server";
import { sql } from "drizzle-orm";
import { db } from "@/db";
import { audit } from "./audit";
import { TOOLCHAIN, buildCacheKey, resolveItems, slugify } from "./builds";
import { getLatestRelease } from "./catalog";
import { capabilitiesFor } from "./entitlements";
import { clientKey, hitRateLimit } from "./rate-limit";
import { type SessionUser, HttpError } from "./session";

/** Queue a public subset build (shared by the subset builder and category packs). The worker does the work. */
export async function queueSubsetBuild(req: Request, user: SessionUser | null, input: { name: string; items: { designId: string; style: string }[]; formats: string[] }) {
  const caps = await capabilitiesFor(user?.id ?? null);
  const unique = [...new Map(input.items.map((i) => [`${i.designId}:${i.style}`, i])).values()];
  if (unique.length > caps.maxSubsetIcons) throw new HttpError(422, `A subset can contain at most ${caps.maxSubsetIcons} icon styles on the ${caps.plan} plan.`);
  const items = await resolveItems(unique);
  if (items.length !== unique.length) throw new HttpError(422, `${unique.length - items.length} selected icon styles are not published and were rejected.`);
  const formats = [...new Set(input.formats)];
  const fontFormats = formats.filter((f) => ["otf", "ttf", "woff2", "woff"].includes(f));
  if (fontFormats.length && !items.some((i) => i.fontSupported)) throw new HttpError(422, "None of the selected icons can be compiled into a font (SVG-only). Choose SVG output.");

  const release = await getLatestRelease();
  if (!release) throw new HttpError(503, "No published release is available yet.");
  const slug = slugify(input.name);
  const scope = "public"; // subsets only contain public catalog assets; private kits use scope private:<user>
  const cacheKey = buildCacheKey({ scope, slug, formats, items, release: release.version });

  // Cache hit: an identical build already exists, so reuse its artifact (no worker time).
  const cached = await db.execute(sql`SELECT storage_key, file_name, bytes, sha256, manifest, job_id FROM build_artifacts
                                      WHERE scope = ${scope} AND cache_key = ${cacheKey}`);
  if (cached.rows.length) {
    const a = cached.rows[0] as Record<string, unknown>;
    await db.execute(sql`UPDATE build_artifacts SET last_used_at = now() WHERE scope = ${scope} AND cache_key = ${cacheKey}`);
    const r = await db.execute(sql`
      INSERT INTO jobs (kind, status, owner_id, scope, cache_key, payload, result, started_at, finished_at)
      VALUES ('subset_build', 'succeeded', ${user?.id ?? null}, ${scope}, ${cacheKey},
              ${JSON.stringify({ name: input.name, slug, formats, cachedFrom: a.job_id })}::jsonb,
              ${JSON.stringify({ storageKey: a.storage_key, fileName: a.file_name, bytes: Number(a.bytes), sha256: a.sha256, manifest: a.manifest })}::jsonb,
              now(), now())
      RETURNING id`);
    return NextResponse.json({ jobId: (r.rows[0] as { id: string }).id, status: "succeeded", cached: true }, { status: 200 });
  }

  const limitKey = user ? `subset:user:${user.id}` : `subset:anon:${clientKey(req)}`;
  const rl = await hitRateLimit(limitKey, caps.subsetBuildsPerHour, 3600);
  if (!rl.ok) {
    return NextResponse.json(
      { error: `Build limit reached (${caps.subsetBuildsPerHour} per hour on the ${caps.plan} plan). Try again after ${rl.resetAt.toISOString()}.` },
      { status: 429, headers: { "retry-after": String(Math.ceil((rl.resetAt.getTime() - Date.now()) / 1000)) } },
    );
  }
  const existing = await db.execute(sql`SELECT id FROM jobs WHERE scope = ${scope} AND cache_key = ${cacheKey} AND status IN ('queued','running') LIMIT 1`);
  if (existing.rows.length) return NextResponse.json({ jobId: (existing.rows[0] as { id: string }).id, status: "queued", deduplicated: true }, { status: 202 });

  const payload = {
    name: input.name,
    slug,
    formats,
    release: release.version,
    toolchain: TOOLCHAIN,
    items: items.map((i) => ({ variantId: i.variantId, designId: i.designId, name: i.name, style: i.style, source: i.source })),
  };
  const r = await db.execute(sql`
    INSERT INTO jobs (kind, status, owner_id, scope, cache_key, payload, max_attempts)
    VALUES ('subset_build', 'queued', ${user?.id ?? null}, ${scope}, ${cacheKey}, ${JSON.stringify(payload)}::jsonb, 3)
    RETURNING id`);
  const jobId = (r.rows[0] as { id: string }).id;
  await audit(user?.id ?? null, "build.queue", "job", jobId, { items: items.length, formats });
  return NextResponse.json({ jobId, status: "queued" }, { status: 202 });
}
