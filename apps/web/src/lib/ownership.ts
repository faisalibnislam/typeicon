import "server-only";
import { sql } from "drizzle-orm";
import { db } from "@/db";
import { uuid } from "./api";
import { HttpError } from "./session";

/** Same 404 for "missing" and "not yours", so other users' resources are not revealed. */
export async function ownCollection(userId: string, id: string) {
  if (!uuid.safeParse(id).success) throw new HttpError(404, "Not found");
  const r = await db.execute(sql`SELECT owner_id FROM collections WHERE id = ${id}`);
  const row = r.rows[0] as { owner_id: string } | undefined;
  if (!row || row.owner_id !== userId) throw new HttpError(404, "Not found");
}

export async function ownKit(userId: string, id: string) {
  if (!uuid.safeParse(id).success) throw new HttpError(404, "Not found");
  const r = await db.execute(sql`SELECT owner_id FROM kits WHERE id = ${id}`);
  const row = r.rows[0] as { owner_id: string } | undefined;
  if (!row || row.owner_id !== userId) throw new HttpError(404, "Not found");
}
