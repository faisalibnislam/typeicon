import { sql } from "drizzle-orm";
import { db } from "@/db";
import { ActionButton } from "@/components/admin/action-button";
import { ReleaseBuildForm } from "@/components/admin/release-build-form";
import { fmt } from "@/lib/format";

export default async function Releases() {
  const r = await db.execute(sql`SELECT r.version, r.release_date, r.status, r.counts, r.approved_by, r.approved_at,
      (SELECT json_agg(json_build_object('family', f.family, 'glyphs', f.glyph_count, 'ots', f.validation->'otf'->'stats'->>'ots', 'min', f.raster->>'minIoU') ORDER BY f.family) FROM font_bundles f WHERE f.release_id = r.id) AS fams
    FROM releases r ORDER BY r.release_date DESC, r.created_at DESC`);
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold tracking-tight">Releases</h1>
      <ReleaseBuildForm />
      {(r.rows as { version: string; release_date: string; status: string; counts: Record<string, number>; approved_by: string | null; fams: { family: string; glyphs: number; ots: string; min: string }[] | null }[]).map((rel) => (
        <section key={rel.version} className="rounded-2xl border border-border bg-surface p-4">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <h2 className="font-semibold">{rel.version} <span className="font-normal text-muted">{String(rel.release_date).slice(0, 10)} · {rel.status}{rel.approved_by ? ` · approved by ${rel.approved_by}` : ""}</span></h2>
            <div className="flex gap-2">
              <ActionButton url="/api/admin/releases" body={{ action: "status", version: rel.version, status: "approved" }} label="Approve" />
              <ActionButton url="/api/admin/releases" body={{ action: "status", version: rel.version, status: "published" }} label="Publish" variant="primary" />
              <ActionButton url="/api/admin/releases" body={{ action: "status", version: rel.version, status: "retired" }} label="Retire" variant="danger" confirmText="Retire this release? Its files remain downloadable by direct link." />
            </div>
          </div>
          <p className="mt-1 text-sm text-text-2">{fmt(rel.counts.icons ?? 0)} icons · {fmt(rel.counts.variants ?? 0)} variants · {fmt(rel.counts.fontGlyphs ?? 0)} glyphs</p>
          <table className="mt-3 w-full text-xs"><tbody>
            {(rel.fams ?? []).map((f) => <tr key={f.family} className="border-b border-border"><td className="py-1">{f.family}</td><td className="tabular-nums">{fmt(f.glyphs)}</td><td>OTS {f.ots}</td><td>raster min IoU {f.min}</td></tr>)}
          </tbody></table>
        </section>
      ))}
    </div>
  );
}
