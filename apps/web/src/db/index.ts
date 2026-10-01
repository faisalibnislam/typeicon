import "server-only";
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";
import * as authSchema from "./auth-schema";
import * as schema from "./schema";

const globalForDb = globalThis as unknown as { typeiconPool?: Pool };

function createPool() {
  const connectionString = process.env.DATABASE_URL;
  if (!connectionString) throw new Error("DATABASE_URL is not set (see .env.example)");
  return new Pool({
    connectionString,
    max: Number(process.env.DATABASE_POOL_MAX ?? 10),
    statement_timeout: 10_000, // bounded queries: no request may hold the DB for long
    idleTimeoutMillis: 30_000,
  });
}

export const pool = globalForDb.typeiconPool ?? createPool();
if (process.env.NODE_ENV !== "production") globalForDb.typeiconPool = pool;

export const db = drizzle(pool, { schema: { ...schema, ...authSchema }, casing: "snake_case" });
export { schema, authSchema };
