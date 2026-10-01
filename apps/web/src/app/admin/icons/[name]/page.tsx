import Link from "next/link";
import { notFound } from "next/navigation";
import { sql } from "drizzle-orm";
import { db } from "@/db";
import { ActionButton } from "@/components/admin/action-button";
import { DesignEditor } from "@/components/admin/design-editor";
import { IconSvg } from "@/components/icon-svg";

export default async function AdminIcon(props: PageProps<"/admin/icons/[name]">) {
  const { name } = await props.params;
  const d = await db.execute(sql`SELECT d.*, sp.slug AS source, c.slug AS concept FROM designs d JOIN source_packs sp ON sp.id = d.source_pack_id
                                 JOIN concepts c ON c.id = d.concept_id WHERE d.name = ${name}`);
  const row = d.rows[0] as Record<string, unknown> | undefined;
  if (!row) notFound();
  const v = await db.execute(sql`SELECT id, style, native_label, status, review_status, route, reasons, svg, source_path, source_sha256, svg_sha256, duplicate_of_style
                                 FROM variants WHERE design_id = ${row.id as string} ORDER BY style`);
  return (
    <div className="space-y-6">
      <p className="text-sm text-muted"><Link href="/admin/icons" className="hover:text-text">Icons</Link> / {name}</p>
      <h1 className="font-mono text-2xl font-semibold">{name}</h1>
      <p className="text-sm text-muted">Source {String(row.source)} · concept {String(row.concept)} · namespace {String(row.namespace)} · codepoint {row.codepoint ? `U+${Number(row.codepoint).toString(16).toUpperCase()}` : "none"} · status {String(row.status)} · <Link href={`/icons/${name}`} className="text-accent">public page</Link></p>
      <section className="grid gap-3 md:grid-cols-3">
        {(v.rows as Record<string, unknown>[]).map((x) => (
          <div key={x.id as string} className="rounded-2xl border border-border bg-surface p-4 text-sm">
            <div className="mb-3 flex gap-4 text-text">
              {[16, 24, 48].map((s) => <IconSvg key={s} svg={(x.svg as string) ?? null} size={s} />)}
            </div>
            <p className="font-medium">{String(x.style)} <span className="font-normal text-muted">({String(x.native_label)})</span></p>
            <p className="text-xs text-muted">status {String(x.status)} · review {String(x.review_status)} · route {String(x.route)}</p>
            {(x.reasons as string[]).length > 0 && <p className="mt-1 text-xs text-danger">{(x.reasons as string[]).join("; ")}</p>}
            <p className="mt-1 break-all font-mono text-[10px] text-muted">{String(x.source_path)} · {String(x.source_sha256).slice(0, 12)}</p>
            <div className="mt-2 flex gap-2">
              <ActionButton url={`/api/admin/variants/${x.id}`} body={{ decision: "approved" }} label="Approve" />
              <ActionButton url={`/api/admin/variants/${x.id}`} body={{ decision: "rejected" }} label="Reject" variant="danger" confirmText="Reject and unpublish this variant?" />
            </div>
          </div>
        ))}
      </section>
      <DesignEditor
        name={name}
        initial={{ description: (row.description as string) ?? "", tags: row.tags as string[], categories: row.category_slugs as string[], aliases: row.alias_names as string[], status: row.status as string }}
      />
    </div>
  );
}
