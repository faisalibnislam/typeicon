import type { Metadata } from "next";
import Link from "next/link";
import { sql } from "drizzle-orm";
import { db } from "@/db";
import { billingEnabled, capabilitiesFor } from "@/lib/entitlements";
import { requireUser } from "@/lib/session";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Account", robots: { index: false } };

export default async function AccountPage() {
  const user = await requireUser("/account");
  const caps = await capabilitiesFor(user.id);
  const counts = await db.execute(sql`SELECT
      (SELECT count(*)::int FROM collections WHERE owner_id = ${user.id}) AS collections,
      (SELECT count(*)::int FROM kits WHERE owner_id = ${user.id}) AS kits,
      (SELECT count(*)::int FROM jobs WHERE owner_id = ${user.id}) AS builds`);
  const c = counts.rows[0] as { collections: number; kits: number; builds: number };
  const jobs = await db.execute(sql`SELECT id, kind, status, created_at, result->>'fileName' AS file, result->>'storageKey' AS key
                                    FROM jobs WHERE owner_id = ${user.id} ORDER BY created_at DESC LIMIT 10`);
  return (
    <div className="mx-auto max-w-4xl px-4 pb-24 pt-8 sm:px-6">
      <h1 className="text-2xl font-semibold tracking-tight">Account</h1>
      <p className="mt-1 text-sm text-muted">{user.name} · {user.email}{user.role === "admin" && " · admin"}</p>
      <div className="mt-6 grid gap-3 sm:grid-cols-3">
        <Link href="/collections" className="rounded-2xl border border-border bg-surface p-4 hover:border-border-strong"><p className="text-sm text-muted">Collections</p><p className="text-2xl font-semibold">{c.collections}</p></Link>
        <Link href="/kits" className="rounded-2xl border border-border bg-surface p-4 hover:border-border-strong"><p className="text-sm text-muted">Kits</p><p className="text-2xl font-semibold">{c.kits} <span className="text-sm font-normal text-muted">of {caps.kits}</span></p></Link>
        <div className="rounded-2xl border border-border bg-surface p-4"><p className="text-sm text-muted">Builds</p><p className="text-2xl font-semibold">{c.builds}</p></div>
      </div>
      <section className="mt-8 rounded-2xl border border-border bg-surface p-5">
        <h2 className="font-semibold">Plan and limits</h2>
        <p className="mt-1 text-sm text-text-2">Plan: <strong>{caps.plan}</strong> · {caps.subsetBuildsPerHour} subset builds per hour · up to {caps.maxSubsetIcons} icon styles per subset · {caps.customIcons} custom icons · hosted kits {caps.hostedKits ? "enabled" : "not included"}</p>
        <p className="mt-2 text-xs text-muted">
          {billingEnabled() ? "Plan changes are managed by the billing provider." : "Paid plans are not available: pricing has not been set and checkout is disabled."} Plans only change service capacity; they never change the license terms of downloaded icons.
        </p>
      </section>
      <section className="mt-8">
        <h2 className="mb-2 font-semibold">Recent builds</h2>
        <ul className="divide-y divide-border rounded-2xl border border-border bg-surface">
          {(jobs.rows as { id: string; kind: string; status: string; created_at: string; file: string | null; key: string | null }[]).map((j) => (
            <li key={j.id} className="flex items-center justify-between gap-3 px-4 py-3 text-sm">
              <span className="truncate">{j.file ?? j.kind} <span className="text-muted">· {String(j.created_at).slice(0, 16)}</span></span>
              {j.key && j.status === "succeeded" ? <a href={`/api/files/${j.key}`} className="text-accent hover:underline">Download</a> : <span className="text-muted">{j.status}</span>}
            </li>
          ))}
          {!jobs.rows.length && <li className="px-4 py-3 text-sm text-muted">No builds yet.</li>}
        </ul>
      </section>
    </div>
  );
}
