import Link from "next/link";
import { sql } from "drizzle-orm";
import { db } from "@/db";
import { fmt } from "@/lib/format";

export default async function Quality() {
  const [dupes, coreGaps, conceptSpread, rejected, review] = await Promise.all([
    db.execute(sql`SELECT v.svg_sha256, count(*)::int AS n, array_agg(d.name || ':' || v.style ORDER BY d.name) AS members
                   FROM variants v JOIN designs d ON d.id = v.design_id WHERE v.status = 'published' AND v.svg_sha256 IS NOT NULL
                   GROUP BY v.svg_sha256 HAVING count(DISTINCT d.id) > 1 ORDER BY n DESC LIMIT 100`),
    db.execute(sql`SELECT d.name, d.published_styles FROM designs d WHERE d.area = 'core' AND NOT d.published_styles @> ARRAY['filled','line','rounded'] ORDER BY d.name`),
    db.execute(sql`SELECT c.slug, count(*)::int AS n, array_agg(d.name ORDER BY d.name) AS names FROM designs d JOIN concepts c ON c.id = d.concept_id
                   WHERE d.status = 'published' GROUP BY c.slug HAVING count(*) > 2 ORDER BY n DESC LIMIT 30`),
    db.execute(sql`SELECT reason, count(*)::int AS n FROM variants, unnest(reasons) AS reason WHERE status <> 'published' GROUP BY reason ORDER BY n DESC LIMIT 30`),
    db.execute(sql`SELECT count(*) FILTER (WHERE attributes->'designReview'->>'status' = 'pending')::int AS pending,
                          coalesce(json_agg(json_build_object('name', name, 'note', attributes->'designReview'->>'note') ORDER BY name)
                            FILTER (WHERE attributes->'designReview'->>'note' IS NOT NULL), '[]') AS flagged
                   FROM designs WHERE area = 'core'`),
  ]);
  const rv = review.rows[0] as { pending: number; flagged: { name: string; note: string }[] };
  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-semibold tracking-tight">Duplicates and gaps</h1>
      <section>
        <h2 className="mb-2 font-semibold">Awaiting human design review ({fmt(rv.pending)} Core designs)</h2>
        <p className="mb-2 text-sm text-muted">Every Core design is published and flagged until a designer approves it. The designers who drew each batch raised these {fmt(rv.flagged.length)} first:</p>
        <ul className="space-y-1 text-sm">
          {rv.flagged.map((f) => (
            <li key={f.name}><Link href={`/admin/icons/${f.name}`} className="font-mono">{f.name}</Link>: {f.note}</li>
          ))}
        </ul>
      </section>
      <section>
        <h2 className="mb-2 font-semibold">Identical artwork published under different names ({fmt(dupes.rows.length)} groups)</h2>
        <p className="mb-2 text-sm text-muted">Same sanitized SVG checksum. These are not double-counted in Core targets; review whether one should become an alias.</p>
        <ul className="space-y-1 text-sm">
          {(dupes.rows as { svg_sha256: string; members: string[] }[]).map((g) => (
            <li key={g.svg_sha256} className="rounded-lg border border-border bg-surface px-3 py-1.5"><span className="font-mono text-[11px] text-muted">{g.svg_sha256.slice(0, 10)}</span> {g.members.join(", ")}</li>
          ))}
        </ul>
      </section>
      <section>
        <h2 className="mb-2 font-semibold">Core designs missing a style ({fmt(coreGaps.rows.length)})</h2>
        {coreGaps.rows.length ? (
          <ul className="text-sm">{(coreGaps.rows as { name: string; published_styles: string[] }[]).map((d) => <li key={d.name}><Link href={`/admin/icons/${d.name}`} className="font-mono">{d.name}</Link>: has {d.published_styles.join(", ") || "none"}</li>)}</ul>
        ) : (
          <p className="text-sm text-success">Every Core design has Filled, Line and Rounded.</p>
        )}
      </section>
      <section>
        <h2 className="mb-2 font-semibold">Concepts with many designs</h2>
        <ul className="text-sm">{(conceptSpread.rows as { slug: string; n: number; names: string[] }[]).map((c) => <li key={c.slug}><strong>{c.slug}</strong> ({c.n}): {c.names.join(", ")}</li>)}</ul>
      </section>
      <section>
        <h2 className="mb-2 font-semibold">Why variants are not published</h2>
        <table className="text-sm"><tbody>{(rejected.rows as { reason: string; n: number }[]).map((r) => <tr key={r.reason}><td className="pr-4">{r.reason}</td><td className="tabular-nums">{fmt(r.n)}</td></tr>)}</tbody></table>
      </section>
    </div>
  );
}
