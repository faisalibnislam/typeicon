import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { sql } from "drizzle-orm";
import { db } from "@/db";
import { CollectionActions } from "@/components/collections/collection-actions";
import { IconSvg } from "@/components/icon-svg";
import { requireUser } from "@/lib/session";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Collection", robots: { index: false } };

export default async function CollectionPage(props: PageProps<"/collections/[id]">) {
  const { id } = await props.params;
  const user = await requireUser(`/collections/${id}`);
  if (!/^[0-9a-f-]{36}$/.test(id)) notFound();
  const c = await db.execute(sql`SELECT id, name, owner_id FROM collections WHERE id = ${id}`);
  const col = c.rows[0] as { id: string; name: string; owner_id: string } | undefined;
  if (!col || col.owner_id !== user.id) notFound();
  const items = await db.execute(sql`
    SELECT d.id AS design_id, d.name, ci.style, v.svg, sp.slug AS source FROM collection_items ci
    JOIN designs d ON d.id = ci.design_id JOIN variants v ON v.design_id = ci.design_id AND v.style = ci.style
    JOIN source_packs sp ON sp.id = d.source_pack_id
    WHERE ci.collection_id = ${id} ORDER BY ci.position`);
  const rows = items.rows as { design_id: string; name: string; style: "filled" | "line" | "rounded" | "thin"; svg: string; source: string }[];
  return (
    <div className="mx-auto max-w-5xl px-4 pb-24 pt-8 sm:px-6">
      <nav className="mb-3 text-sm text-muted"><Link href="/collections" className="hover:text-text">Collections</Link> / {col.name}</nav>
      <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-2xl font-semibold tracking-tight">{col.name}</h1>
        <CollectionActions id={col.id} items={rows.map((r) => ({ designId: r.design_id, name: r.name, style: r.style, source: r.source, svg: r.svg }))} />
      </div>
      <ul className="grid grid-cols-[repeat(auto-fill,minmax(112px,1fr))] gap-2">
        {rows.map((r) => (
          <li key={r.design_id + r.style}>
            <Link href={`/icons/${r.name}?style=${r.style}`} className="flex h-28 flex-col items-center justify-center gap-2 rounded-xl border border-border bg-surface text-text hover:border-border-strong">
              <IconSvg svg={r.svg} size={28} />
              <span className="w-full truncate px-2 text-center text-xs text-text-2">{r.name}</span>
              <span className="text-[10px] text-muted">{r.style}</span>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
