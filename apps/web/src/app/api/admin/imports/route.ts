import { NextResponse } from "next/server";
import { sql } from "drizzle-orm";
import { z } from "zod";
import { db } from "@/db";
import { handle, readJson } from "@/lib/api";
import { audit } from "@/lib/audit";
import { apiUser } from "@/lib/session";

/** Queue a catalog import (pinned sources from assets/sources/manifest.json). Dry runs change nothing. */
export const POST = handle(async (req) => {
  const admin = await apiUser({ admin: true });
  const body = await readJson(req, z.object({ sources: z.array(z.string().regex(/^[a-z0-9-]{2,40}$/)).max(20), dryRun: z.boolean() }));
  const r = await db.execute(sql`INSERT INTO jobs (kind, owner_id, scope, payload, max_attempts)
    VALUES ('catalog_import', ${admin.id}, 'admin', ${JSON.stringify(body)}::jsonb, 1) RETURNING id`);
  const id = (r.rows[0] as { id: string }).id;
  await audit(admin.id, "catalog.import.queue", "job", id, body);
  return NextResponse.json({ jobId: id }, { status: 202 });
});
