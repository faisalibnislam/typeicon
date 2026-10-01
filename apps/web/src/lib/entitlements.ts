import "server-only";
import { sql } from "drizzle-orm";
import { db } from "@/db";

/**
 * Capability layer for future free/pro/team plans. No prices live here and checkout stays
 * hidden until billing is configured (BILLING_PROVIDER + product ids). Downloadable-use rights
 * come from each source license and are never reduced by a plan; plans only govern service
 * capacity (build quotas, custom uploads, hosted kits).
 */
export interface Capabilities {
  plan: string;
  subsetBuildsPerHour: number;
  maxSubsetIcons: number;
  customIcons: number;
  kits: number;
  hostedKits: boolean;
}

const ANONYMOUS: Capabilities = {
  plan: "anonymous",
  subsetBuildsPerHour: Number(process.env.ANON_SUBSET_BUILDS_PER_HOUR ?? 10),
  maxSubsetIcons: Math.min(Number(process.env.MAX_SUBSET_ICONS ?? 500), 200),
  customIcons: 0,
  kits: 0,
  hostedKits: false,
};

export async function capabilitiesFor(userId: string | null): Promise<Capabilities> {
  if (!userId) return ANONYMOUS;
  const r = await db.execute(sql`
    SELECT p.slug, p.capabilities FROM plans p
    WHERE p.slug = coalesce(
      (SELECT e.plan_slug FROM user_entitlements e WHERE e.user_id = ${userId} AND (e.ends_at IS NULL OR e.ends_at > now())
       ORDER BY e.starts_at DESC LIMIT 1),
      (SELECT slug FROM plans WHERE is_default LIMIT 1))`);
  const row = r.rows[0] as { slug: string; capabilities: Record<string, number | boolean> } | undefined;
  if (!row) return { ...ANONYMOUS, plan: "free", kits: 3 };
  const c = row.capabilities;
  return {
    plan: row.slug,
    subsetBuildsPerHour: Number(c.subsetBuildsPerHour ?? 20),
    maxSubsetIcons: Math.min(Number(c.maxSubsetIcons ?? 500), Number(process.env.MAX_SUBSET_ICONS ?? 500)),
    customIcons: Number(c.customIcons ?? 0),
    kits: Number(c.kits ?? 3),
    hostedKits: Boolean(c.hostedKits),
  };
}

export const billingEnabled = () => Boolean(process.env.BILLING_PROVIDER);
