import { NextResponse } from "next/server";
import { sql } from "drizzle-orm";
import { z } from "zod";
import { db } from "@/db";
import { handle, readJson } from "@/lib/api";
import { audit } from "@/lib/audit";
import { apiUser, HttpError } from "@/lib/session";

const semver = z.string().regex(/^\d+\.\d{1,2}\.\d$/, "Use MAJOR.MINOR.PATCH with minor < 100 and patch < 10");

/** Queue a release build (compile + validate every family, package archives), or change a release's status. */
export const POST = handle(async (req) => {
  const admin = await apiUser({ admin: true });
  const body = await readJson(
    req,
    z.discriminatedUnion("action", [
      z.object({ action: z.literal("build"), version: semver, date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/) }),
      z.object({ action: z.literal("status"), version: semver, status: z.enum(["approved", "published", "retired"]) }),
    ]),
  );
  if (body.action === "build") {
    const r = await db.execute(sql`INSERT INTO jobs (kind, owner_id, scope, payload, max_attempts)
      VALUES ('release_build', ${admin.id}, 'admin', ${JSON.stringify({ version: body.version, date: body.date })}::jsonb, 1) RETURNING id`);
    const id = (r.rows[0] as { id: string }).id;
    await audit(admin.id, "release.build.queue", "release", body.version, { jobId: id });
    return NextResponse.json({ jobId: id }, { status: 202 });
  }
  const r = await db.execute(sql`UPDATE releases SET status = ${body.status},
      approved_by = CASE WHEN ${body.status} = 'approved' THEN ${admin.email} ELSE approved_by END,
      approved_at = CASE WHEN ${body.status} = 'approved' THEN now() ELSE approved_at END,
      published_at = CASE WHEN ${body.status} = 'published' THEN coalesce(published_at, now()) ELSE published_at END
    WHERE version = ${body.version} RETURNING id`);
  if (!r.rows.length) throw new HttpError(404, "Unknown release");
  await audit(admin.id, `release.${body.status}`, "release", body.version);
  return NextResponse.json({ ok: true });
});
