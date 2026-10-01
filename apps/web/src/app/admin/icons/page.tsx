import Link from "next/link";
import { sql } from "drizzle-orm";
import { db } from "@/db";
import { IconSvg } from "@/components/icon-svg";

export default async function AdminIcons(props: PageProps<"/admin/icons">) {
  const sp = await props.searchParams;
  const q = String(sp.q ?? "").toLowerCase().replace(/[^a-z0-9-]/g, "").slice(0, 64);
  const status = ["published", "pending", "rejected", "deprecated"].includes(String(sp.status)) ? String(sp.status) : "";
  const r = await db.execute(sql`
    SELECT d.name, d.status, d.area, d.published_styles, sp.slug AS source,
      (SELECT svg FROM variants v WHERE v.design_id = d.id ORDER BY array_position(ARRAY['line','rounded','filled']::text[], v.style) LIMIT 1) AS svg
    FROM designs d JOIN source_packs sp ON sp.id = d.source_pack_id
    WHERE (${q} = '' OR d.name LIKE ${q + "%"} OR d.local_name LIKE ${q + "%"}) AND (${status} = '' OR d.status = ${status})
    ORDER BY (d.area <> 'core'), d.name LIMIT 200`);
  return (
    <div>
      <h1 className="mb-4 text-2xl font-semibold tracking-tight">Icons</h1>
      <form className="mb-4 flex flex-wrap gap-2">
        <input name="q" defaultValue={q} placeholder="Name prefix" className="h-9 rounded-lg border border-border bg-surface px-3 text-sm" />
        <select name="status" defaultValue={status} className="h-9 rounded-lg border border-border bg-surface px-2 text-sm">
          <option value="">Any status</option><option>published</option><option>pending</option><option>rejected</option><option>deprecated</option>
        </select>
        <button className="h-9 rounded-lg bg-text px-3 text-sm text-bg">Filter</button>
      </form>
      <table className="w-full text-sm">
        <tbody>
          {(r.rows as { name: string; status: string; area: string; published_styles: string[]; source: string; svg: string | null }[]).map((d) => (
            <tr key={d.name} className="border-b border-border">
              <td className="w-10 py-1.5"><IconSvg svg={d.svg} size={20} /></td>
              <td><Link href={`/admin/icons/${d.name}`} className="font-mono hover:text-accent">{d.name}</Link></td>
              <td className="text-text-2">{d.source}</td>
              <td className="text-text-2">{d.published_styles.join(", ") || "none"}</td>
              <td className={d.status === "published" ? "text-success" : "text-danger"}>{d.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
