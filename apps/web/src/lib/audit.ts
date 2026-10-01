import "server-only";
import { sql } from "drizzle-orm";
import { db } from "@/db";

export async function audit(actorId: string | null, action: string, subjectType: string, subjectId?: string | null, data: Record<string, unknown> = {}) {
  await db.execute(sql`INSERT INTO audit_events (actor_id, action, subject_type, subject_id, data)
    VALUES (${actorId}, ${action}, ${subjectType}, ${subjectId ?? null}, ${JSON.stringify(data)}::jsonb)`);
}
