import { sql } from "drizzle-orm";
import { db } from "@/db";
import { ActionButton } from "@/components/admin/action-button";
import { listPacks } from "@/lib/catalog";

export default async function Imports() {
  const [packs, jobs] = await Promise.all([
    listPacks(),
    db.execute(sql`SELECT id, status, payload, result, error, created_at FROM jobs WHERE kind = 'catalog_import' ORDER BY created_at DESC LIMIT 10`),
  ]);
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold tracking-tight">Imports</h1>
      <p className="max-w-3xl text-sm text-muted">
        Imports read pinned sources from <code>assets/sources/manifest.json</code> (upstream version, tarball integrity, license). Run a dry run first: it validates and reports without writing the registry or database.
        Re-running is idempotent; converted outlines are cached by checksum. To add a new source, add it to the manifest in the repository and review its license.
      </p>
      <table className="w-full text-sm">
        <tbody>
          {packs.map((p) => (
            <tr key={p.slug} className="border-b border-border">
              <td className="py-2 font-medium">{p.displayName} <span className="text-muted">{p.version}</span></td>
              <td className="text-xs text-muted">{p.licenseId}</td>
              <td className="text-right">
                <span className="inline-flex gap-2">
                  <ActionButton url="/api/admin/imports" body={{ sources: [p.slug], dryRun: true }} label="Dry run" />
                  <ActionButton url="/api/admin/imports" body={{ sources: [p.slug], dryRun: false }} label="Import" variant="primary" confirmText={`Import ${p.displayName} into the live catalog?`} />
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <section>
        <h2 className="mb-2 font-semibold">Recent import jobs</h2>
        <ul className="space-y-2">
          {(jobs.rows as { id: string; status: string; payload: unknown; result: unknown; error: string | null; created_at: string }[]).map((j) => (
            <li key={j.id} className="rounded-xl border border-border bg-surface p-3 text-xs">
              <p><strong>{j.status}</strong> · {String(j.created_at).slice(0, 19)} · {JSON.stringify(j.payload)}</p>
              {j.error && <pre className="mt-1 whitespace-pre-wrap text-danger">{j.error}</pre>}
              {j.result ? <pre className="mt-1 max-h-60 overflow-auto whitespace-pre-wrap text-muted">{JSON.stringify(j.result, null, 1)}</pre> : null}
            </li>
          ))}
          {!jobs.rows.length && <li className="text-sm text-muted">No import jobs yet.</li>}
        </ul>
      </section>
    </div>
  );
}
