import { readFile } from "node:fs/promises";
import path from "node:path";
import { sql } from "drizzle-orm";
import { db } from "@/db";
import { getStats } from "@/lib/catalog";
import { fmt } from "@/lib/format";
import { repoRoot } from "@/lib/paths";

export default async function AdminHome() {
  const [stats, jobs, lat, dl, outbox, recent] = await Promise.all([
    getStats(),
    db.execute(sql`SELECT kind, status, count(*)::int AS n FROM jobs GROUP BY kind, status ORDER BY kind, status`),
    db.execute(sql`SELECT count(*)::int AS n, percentile_cont(0.5) WITHIN GROUP (ORDER BY duration_ms) AS p50,
                          percentile_cont(0.95) WITHIN GROUP (ORDER BY duration_ms) AS p95, max(duration_ms) AS max
                   FROM search_metrics WHERE created_at > now() - interval '24 hours'`),
    db.execute(sql`SELECT count(*)::int AS n FROM audit_events WHERE action = 'download' AND created_at > now() - interval '24 hours'`),
    db.execute(sql`SELECT count(*)::int AS n FROM outbox WHERE processed_at IS NULL`),
    db.execute(sql`SELECT actor_id, action, subject_type, subject_id, created_at FROM audit_events ORDER BY id DESC LIMIT 15`),
  ]);
  let audit: { summary?: Record<string, unknown> } | null = null;
  try {
    audit = JSON.parse(await readFile(path.join(repoRoot(), "build/audit/catalog-audit.json"), "utf8"));
  } catch {}
  const l = lat.rows[0] as { n: number; p50: number | null; p95: number | null; max: number | null };
  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-semibold tracking-tight">Overview</h1>
      {stats && (
        <dl className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
          {[
            ["Published designs", fmt(stats.designs.total), `${fmt(stats.designs.core)} Core · ${fmt(stats.designs.brands)} brand logos`],
            ["Published variants", fmt(stats.variants.total), `${fmt(stats.variants.fontSupported)} in fonts · ${fmt(stats.variants.svgOnly)} SVG-only`],
            ["Unique Core toward goal", fmt(stats.target.current), `gap ${fmt(stats.target.gap)} to ${fmt(stats.target.uniqueCoreConcepts)}`],
            ["Search p95 (24h)", l.p95 != null ? `${l.p95.toFixed(1)} ms` : "No data", `${fmt(l.n)} searches · p50 ${l.p50 != null ? `${l.p50.toFixed(1)} ms` : "n/a"}`],
            ["Archive downloads (24h)", fmt((dl.rows[0] as { n: number }).n), "counted without personal data"],
            ["Outbox pending", fmt((outbox.rows[0] as { n: number }).n), "derived-system updates not yet processed"],
          ].map(([t, v, n]) => (
            <div key={t} className="rounded-2xl border border-border bg-surface p-4">
              <dt className="text-sm text-muted">{t}</dt>
              <dd className="text-2xl font-semibold tabular-nums">{v}</dd>
              <dd className="text-xs text-muted">{n}</dd>
            </div>
          ))}
        </dl>
      )}
      <section>
        <h2 className="mb-2 font-semibold">Queue</h2>
        <table className="w-full max-w-xl text-sm">
          <tbody>
            {(jobs.rows as { kind: string; status: string; n: number }[]).map((j) => (
              <tr key={j.kind + j.status} className="border-b border-border"><td className="py-1.5">{j.kind}</td><td className={j.status === "failed" ? "text-danger" : "text-text-2"}>{j.status}</td><td className="text-right tabular-nums">{j.n}</td></tr>
            ))}
          </tbody>
        </table>
      </section>
      <section>
        <h2 className="mb-2 font-semibold">Catalog audit</h2>
        {audit?.summary ? <pre className="overflow-x-auto rounded-xl border border-border bg-surface p-3 text-xs">{JSON.stringify(audit.summary, null, 2)}</pre> : <p className="text-sm text-muted">No audit yet. Run <code>pnpm audit:catalog</code>.</p>}
      </section>
      <section>
        <h2 className="mb-2 font-semibold">Recent activity</h2>
        <ul className="divide-y divide-border rounded-xl border border-border bg-surface text-sm">
          {(recent.rows as { actor_id: string | null; action: string; subject_type: string; subject_id: string | null; created_at: string }[]).map((e, i) => (
            <li key={i} className="flex justify-between gap-3 px-3 py-2"><span><strong>{e.action}</strong> <span className="text-muted">{e.subject_type} {e.subject_id?.slice(0, 40)}</span></span><span className="text-xs text-muted">{String(e.created_at).slice(0, 19)}</span></li>
          ))}
        </ul>
      </section>
    </div>
  );
}
