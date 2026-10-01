import { sql } from "drizzle-orm";
import { db } from "@/db";
import { ActionButton } from "@/components/admin/action-button";

export default async function Jobs(props: PageProps<"/admin/jobs">) {
  const sp = await props.searchParams;
  const status = ["queued", "running", "succeeded", "failed"].includes(String(sp.status)) ? String(sp.status) : "";
  const r = await db.execute(sql`SELECT id, kind, status, attempts, max_attempts, error, created_at, finished_at, scope, left(result::text, 300) AS result
                                 FROM jobs WHERE (${status} = '' OR status = ${status}) ORDER BY created_at DESC LIMIT 100`);
  return (
    <div>
      <h1 className="mb-3 text-2xl font-semibold tracking-tight">Jobs</h1>
      <p className="mb-4 text-sm">Filter: {["", "queued", "running", "succeeded", "failed"].map((s) => <a key={s} href={`/admin/jobs${s ? `?status=${s}` : ""}`} className="mr-3 text-accent">{s || "all"}</a>)}</p>
      <ul className="space-y-2">
        {(r.rows as Record<string, string | number | null>[]).map((j) => (
          <li key={String(j.id)} className="rounded-xl border border-border bg-surface p-3 text-sm">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <span><strong>{j.kind}</strong> <span className={j.status === "failed" ? "text-danger" : "text-muted"}>{j.status}</span> <span className="text-xs text-muted">attempt {j.attempts}/{j.max_attempts} · {j.scope} · {String(j.created_at).slice(0, 19)}</span></span>
              {j.status === "failed" && <ActionButton url={`/api/admin/jobs/${j.id}`} label="Retry" />}
            </div>
            {j.error && <pre className="mt-2 max-h-32 overflow-auto whitespace-pre-wrap text-xs text-danger">{String(j.error)}</pre>}
            {j.result && <pre className="mt-2 max-h-24 overflow-auto whitespace-pre-wrap text-[11px] text-muted">{String(j.result)}</pre>}
          </li>
        ))}
      </ul>
    </div>
  );
}
