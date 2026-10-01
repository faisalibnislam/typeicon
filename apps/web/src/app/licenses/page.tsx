import type { Metadata } from "next";
import { sql } from "drizzle-orm";
import { db } from "@/db";
import { listPacks } from "@/lib/catalog";
import { fmt } from "@/lib/format";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Licenses", description: "Licenses, copyright notices and attribution for every TypeIcon source.", alternates: { canonical: "/licenses" } };

export default async function LicensesPage() {
  const packs = await listPacks();
  const lic = await db.execute(sql`SELECT id, name, url, text FROM licenses`);
  const texts = Object.fromEntries((lic.rows as { id: string; name: string; url: string | null; text: string }[]).map((l) => [l.id, l]));
  return (
    <article className="prose-fi mx-auto max-w-4xl px-4 pb-24 pt-8 sm:px-6">
      <h1>Licenses</h1>
      <p>
        TypeIcon combines separately licensed collections. Each source keeps its own license. TypeIcon does not relicense third-party artwork, and those rights stay in place even if
        parts of the TypeIcon service later become paid. Every release archive and subset contains the relevant license texts under <code>licenses/</code>.
      </p>
      <table>
        <thead><tr><th>Source</th><th>License</th><th>Icons</th><th>Area</th></tr></thead>
        <tbody>
          {packs.map((p) => (
            <tr key={p.slug}><td><a href={`#${p.slug}`}>{p.displayName}</a></td><td>{p.licenseId}</td><td>{fmt(p.designs)}</td><td>{p.area}</td></tr>
          ))}
        </tbody>
      </table>
      <div className="note">
        <strong>TypeIcon Core license: not yet decided.</strong> The owner has not chosen public terms for the original Core artwork and fallback letterforms. Until then, Core assets are labelled
        <code>LicenseRef-TypeIcon-Core-Draft</code> and the catalog audit reports this as an open license gap.
      </div>
      {packs.map((p) => {
        const l = texts[p.licenseId];
        return (
          <section key={p.slug} id={p.slug}>
            <h2>{p.displayName}</h2>
            <p>
              {p.licenseId}{l?.url ? <> · <a href={l.url}>{l.url}</a></> : null} · {p.copyright}
              {p.attributionText ? <><br />Attribution: {p.attributionText}</> : null}
            </p>
            {p.trademarkNote && <p><em>{p.trademarkNote}</em></p>}
            {p.notices.map((n) => <p key={n}>{n}</p>)}
            <details>
              <summary>Full license text</summary>
              <pre><code>{l?.text}</code></pre>
            </details>
          </section>
        );
      })}
    </article>
  );
}
