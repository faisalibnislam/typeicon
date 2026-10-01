/** Grant the admin role to an existing account: pnpm tsx --conditions=react-server scripts/grant-admin.ts someone@example.com */
import { sql } from "drizzle-orm";
import { db, pool } from "@/db";

async function main() {
  const email = process.argv[2];
  if (!email) throw new Error("usage: grant-admin.ts <email>");
  const r = await db.execute(sql`UPDATE "user" SET role = 'admin' WHERE email = ${email} RETURNING id`);
  if (!r.rows.length) throw new Error(`no account with email ${email}`);
  await db.execute(sql`INSERT INTO audit_events (actor_id, action, subject_type, subject_id) VALUES ('system:cli', 'user.grant_admin', 'user', ${(r.rows[0] as { id: string }).id})`);
  console.log(`granted admin to ${email}`);
  await pool.end();
}
main().catch((e) => {
  console.error(e.message);
  process.exit(1);
});
