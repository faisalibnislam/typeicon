import type { Metadata } from "next";
import { sql } from "drizzle-orm";
import { db } from "@/db";
import { fmt } from "@/lib/format";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Changelog", description: "TypeIcon releases and catalog changes.", alternates: { canonical: "/changelog" } };

export default async function ChangelogPage() {
  const r = await db.execute(sql`SELECT version, release_date, status, counts, manifest FROM releases ORDER BY release_date DESC, created_at DESC`);
  const rels = r.rows as { version: string; release_date: string; status: string; counts: Record<string, number>; manifest: { families?: string[]; sources?: Record<string, { version: string; license: string }> } }[];
  return (
    <article className="prose-fi mx-auto max-w-3xl px-4 pb-24 pt-8 sm:px-6">
      <h1>Changelog</h1>
      {rels.map((rel) => (
        <section key={rel.version}>
          <h2>{rel.version} <small>{String(rel.release_date).slice(0, 10)} ({rel.status})</small></h2>
          <ul>
            <li>{fmt(rel.counts.icons ?? 0)} icons ({fmt(rel.counts.coreIcons ?? 0)} TypeIcon Core, {fmt(rel.counts.brandIcons ?? rel.counts.communityIcons ?? 0)} brand logos), {fmt(rel.counts.variants ?? 0)} style variants.</li>
            <li>{fmt(rel.counts.fontGlyphs ?? 0)} font glyphs across {rel.manifest.families?.length ?? 0} families: {rel.manifest.families?.join(", ")}.</li>
            <li>Sources: {Object.entries(rel.manifest.sources ?? {}).map(([k, v]) => `${k} ${v.version} (${v.license})`).join(", ")}.</li>
            <li>{fmt(rel.counts.svgOnlyVariants ?? 0)} variants are SVG-only because they cannot be represented as a single-colour outline.</li>
          </ul>
        </section>
      ))}
      {!rels.length && <p>No releases yet.</p>}
    </article>
  );
}
