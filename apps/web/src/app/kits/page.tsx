import type { Metadata } from "next";
import Link from "next/link";
import { sql } from "drizzle-orm";
import { db } from "@/db";
import { NewKitForm } from "@/components/kits/new-kit-form";
import { capabilitiesFor } from "@/lib/entitlements";
import { requireUser } from "@/lib/session";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Kits", robots: { index: false } };

export default async function KitsPage() {
  const user = await requireUser("/kits");
  const caps = await capabilitiesFor(user.id);
  const r = await db.execute(sql`SELECT k.id, k.name, k.current_version, k.updated_at, r.version AS release
                                 FROM kits k LEFT JOIN releases r ON r.id = k.pinned_release_id WHERE k.owner_id = ${user.id} ORDER BY k.updated_at DESC`);
  const kits = r.rows as { id: string; name: string; current_version: number; release: string | null }[];
  return (
    <div className="mx-auto max-w-4xl px-4 pb-24 pt-8 sm:px-6">
      <h1 className="text-2xl font-semibold tracking-tight">Kits</h1>
      <p className="mb-6 mt-1 max-w-2xl text-sm text-text-2">
        A kit is a saved project: selected icons and styles pinned to a catalog release, optional private custom SVGs, and immutable versions you can rebuild or download at any time.
      </p>
      <NewKitForm disabled={kits.length >= caps.kits} limit={caps.kits} />
      <ul className="mt-6 divide-y divide-border rounded-2xl border border-border bg-surface">
        {kits.map((k) => (
          <li key={k.id}>
            <Link href={`/kits/${k.id}`} className="flex items-center justify-between px-4 py-3 hover:bg-surface-2">
              <span className="font-medium text-text">{k.name}</span>
              <span className="text-xs text-muted">v{k.current_version} · {k.release ? `release ${k.release}` : "no release pinned"}</span>
            </Link>
          </li>
        ))}
        {!kits.length && <li className="px-4 py-6 text-center text-sm text-muted">No kits yet.</li>}
      </ul>
    </div>
  );
}
