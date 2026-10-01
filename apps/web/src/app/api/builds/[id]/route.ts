import { NextResponse } from "next/server";
import { uuid } from "@/lib/api";
import { getJob } from "@/lib/builds";
import { getSessionUser } from "@/lib/session";

/** Build status. Public-scope jobs are readable by id (unguessable UUID); private jobs only by the owner. */
export async function GET(_req: Request, ctx: { params: Promise<{ id: string }> }) {
  const { id } = await ctx.params;
  if (!uuid.safeParse(id).success) return NextResponse.json({ error: "Not found" }, { status: 404 });
  const job = await getJob(id);
  if (!job) return NextResponse.json({ error: "Not found" }, { status: 404 });
  if (job.scope !== "public") {
    const user = await getSessionUser();
    if (!user || user.id !== job.ownerId) return NextResponse.json({ error: "Not found" }, { status: 404 });
  }
  const res = job.result as { storageKey?: string; fileName?: string; bytes?: number; sha256?: string; manifest?: Record<string, unknown> } | null;
  return NextResponse.json(
    {
      id: job.id,
      status: job.status,
      attempts: job.attempts,
      error: job.status === "failed" ? job.error : null,
      createdAt: job.createdAt,
      startedAt: job.startedAt,
      finishedAt: job.finishedAt,
      cached: job.cached,
      download: res?.storageKey ? { url: `/api/files/${res.storageKey}`, fileName: res.fileName, bytes: res.bytes, sha256: res.sha256 } : null,
      manifest: res?.manifest ?? null,
    },
    { headers: { "cache-control": "no-store" } },
  );
}
