import type { Metadata } from "next";
import Link from "next/link";
import { sql } from "drizzle-orm";
import { db } from "@/db";
import { IconSvg } from "@/components/icon-svg";
import { requireUser } from "@/lib/session";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Collections", robots: { index: false } };

export default async function CollectionsPage() {
  const user = await requireUser("/collections");
  const r = await db.execute(sql`
    SELECT c.id, c.name, c.is_public, c.updated_at, count(ci.design_id)::int AS n,
      (SELECT json_agg(x.svg) FROM (SELECT v.svg FROM collection_items ci2 JOIN variants v ON v.design_id = ci2.design_id AND v.style = ci2.style
        WHERE ci2.collection_id = c.id ORDER BY ci2.position LIMIT 8) x) AS preview
    FROM collections c LEFT JOIN collection_items ci ON ci.collection_id = c.id
    WHERE c.owner_id = ${user.id} GROUP BY c.id ORDER BY c.updated_at DESC`);
  const rows = r.rows as { id: string; name: string; is_public: boolean; n: number; preview: string[] | null }[];
  return (
    <div className="mx-auto max-w-5xl px-4 pb-24 pt-8 sm:px-6">
      <h1 className="text-2xl font-semibold tracking-tight">Collections</h1>
      <p className="mb-6 mt-1 text-sm text-muted">Save icons in specific styles from any icon page. Collections are private.</p>
      <ul className="grid gap-3 sm:grid-cols-2">
        {rows.map((c) => (
          <li key={c.id}>
            <Link href={`/collections/${c.id}`} className="block rounded-2xl border border-border bg-surface p-4 hover:border-border-strong">
              <p className="font-medium text-text">{c.name}</p>
              <p className="text-xs text-muted">{c.n} icons</p>
              <div className="mt-3 flex gap-2 text-text">{(c.preview ?? []).map((s, i) => <IconSvg key={i} svg={s} size={20} />)}</div>
            </Link>
          </li>
        ))}
      </ul>
      {!rows.length && <p className="rounded-2xl border border-dashed border-border-strong p-10 text-center text-sm text-muted">No collections yet. Open any icon and choose Save.</p>}
    </div>
  );
}
