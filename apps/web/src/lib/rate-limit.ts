import "server-only";
import { createHash } from "node:crypto";
import { sql } from "drizzle-orm";
import { db } from "@/db";

/** Fixed-window counter in Postgres (works across instances; no extra service). */
export async function hitRateLimit(key: string, limit: number, windowSeconds: number) {
  const r = await db.execute(sql`
    INSERT INTO rate_limits (key, window_start, count)
    VALUES (${key}, to_timestamp(floor(extract(epoch FROM now()) / ${windowSeconds}) * ${windowSeconds}), 1)
    ON CONFLICT (key, window_start) DO UPDATE SET count = rate_limits.count + 1
    RETURNING count, window_start`);
  const row = r.rows[0] as { count: number; window_start: string };
  const resetAt = new Date(new Date(row.window_start).getTime() + windowSeconds * 1000);
  return { ok: row.count <= limit, count: row.count, remaining: Math.max(0, limit - row.count), resetAt };
}

/** Pseudonymous client key: never stores the raw IP address. */
export function clientKey(req: Request): string {
  const ip = (req.headers.get("x-forwarded-for") ?? "").split(",")[0].trim() || req.headers.get("x-real-ip") || "local";
  return createHash("sha256").update(`${ip}|${process.env.BETTER_AUTH_SECRET ?? ""}`).digest("hex").slice(0, 24);
}
