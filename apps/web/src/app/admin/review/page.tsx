import { sql } from "drizzle-orm";
import { db } from "@/db";
import { IconSvg } from "@/components/icon-svg";

const SIZES = [16, 20, 24, 32, 48];

/** Design QA review sheet: every Core concept in every published style, at 16–48 px on light and dark. */
export default async function ReviewSheet(props: PageProps<"/admin/review">) {
  const sp = await props.searchParams;
  const source = typeof sp.source === "string" && /^[a-z0-9-]+$/.test(sp.source) ? sp.source : "typeicon-core";
  const r = await db.execute(sql`
    SELECT d.name, d.derived_from IS NOT NULL AS derived,
      json_object_agg(v.style, v.svg) FILTER (WHERE v.status = 'published') AS svgs,
      bool_or(v.review_status = 'proposed') AS proposed
    FROM designs d JOIN source_packs s ON s.id = d.source_pack_id JOIN variants v ON v.design_id = d.id
    WHERE s.slug = ${source} GROUP BY d.name, d.derived_from ORDER BY d.name LIMIT 300`);
  const rows = r.rows as { name: string; derived: boolean; svgs: Record<string, string> | null; proposed: boolean }[];
  return (
    <div>
      <h1 className="mb-1 text-2xl font-semibold tracking-tight">Design review sheet</h1>
      <p className="mb-4 text-sm text-muted">
        {source} · {rows.length} designs. Check stroke consistency, optical size and small-size legibility across Filled, Line, Rounded and Thin. Missing styles are shown as gaps, never substituted.
      </p>
      <div className="space-y-2">
        {rows.map((d) => (
          <section key={d.name} className="grid items-center gap-3 rounded-xl border border-border bg-surface p-3 lg:grid-cols-[180px_1fr_1fr]">
            <p className="font-mono text-sm">{d.name}{d.derived && <span className="ml-1 text-xs text-muted">(derived)</span>}{d.proposed && <span className="ml-1 text-xs text-danger">(proposed)</span>}</p>
            {(["light", "dark"] as const).map((bg) => (
              <div key={bg} className={bg === "light" ? "rounded-lg bg-white p-2 text-[#16161a]" : "rounded-lg bg-[#111113] p-2 text-[#ededf0]"}>
                {(["filled", "line", "rounded", "thin"] as const).map((st) => (
                  <div key={st} className="flex items-end gap-3 py-0.5">
                    <span className="w-12 text-[10px] opacity-60">{st}</span>
                    {d.svgs?.[st] ? SIZES.map((s) => <IconSvg key={s} svg={d.svgs![st]} size={s} />) : <span className="text-[10px] text-red-500">missing</span>}
                  </div>
                ))}
              </div>
            ))}
          </section>
        ))}
      </div>
    </div>
  );
}
