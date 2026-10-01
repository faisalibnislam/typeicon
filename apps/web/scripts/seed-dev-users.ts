/**
 * Create local development/test accounts (never run against production).
 * Credentials are generated and written to .data/dev-credentials.json (git-ignored).
 *   pnpm tsx --conditions=react-server scripts/seed-dev-users.ts
 * Accounts: dev-admin@typeicon.test (role admin), dev-user@typeicon.test (plan "pro", for custom icons/hosting tests),
 *           dev-other@typeicon.test (plan "free", for ownership-isolation tests).
 */
import { randomBytes } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { sql } from "drizzle-orm";
import { db, pool } from "@/db";
import { auth } from "@/lib/auth";
import { repoRoot } from "@/lib/paths";

async function main() {
  const url = process.env.DATABASE_URL ?? "";
  if (!/localhost|127\.0\.0\.1/.test(url)) throw new Error("Refusing to seed dev users on a non-local database");
  const file = path.join(repoRoot(), ".data", "dev-credentials.json");
  const creds: Record<string, { email: string; password: string }> = existsSync(file) ? JSON.parse(readFileSync(file, "utf8")) : {};
  for (const [key, email, role, plan] of [
    ["admin", "dev-admin@typeicon.test", "admin", "free"],
    ["user", "dev-user@typeicon.test", "user", "pro"],
    ["other", "dev-other@typeicon.test", "user", "free"],
  ] as const) {
    const password = creds[key]?.password ?? randomBytes(18).toString("base64url");
    const exists = await db.execute(sql`SELECT id FROM "user" WHERE email = ${email}`);
    if (!exists.rows.length) await auth.api.signUpEmail({ body: { email, password, name: `Dev ${key}` } });
    await db.execute(sql`UPDATE "user" SET role = ${role} WHERE email = ${email}`);
    await db.execute(sql`INSERT INTO user_entitlements (user_id, plan_slug, source)
                         SELECT id, ${plan}, 'manual:dev-seed' FROM "user" WHERE email = ${email}
                         ON CONFLICT (user_id, plan_slug) DO NOTHING`);
    creds[key] = { email, password };
  }
  mkdirSync(path.dirname(file), { recursive: true });
  writeFileSync(file, JSON.stringify(creds, null, 2), { mode: 0o600 });
  console.log(`dev users ready; credentials in ${path.relative(repoRoot(), file)}`);
  await pool.end();
}
main().catch((e) => {
  console.error(e);
  process.exit(1);
});
