import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { StaticGrid } from "@/components/static-grid";
import { listPacks } from "@/lib/catalog";
import { fmt, STYLE_LABEL } from "@/lib/format";
import { parseSearchParams, searchIcons } from "@/lib/search";

export const dynamic = "force-dynamic";

export async function generateMetadata(props: PageProps<"/packs/[slug]">): Promise<Metadata> {
  const { slug } = await props.params;
  const p = (await listPacks()).find((x) => x.slug === slug);
  return p ? { title: `${p.displayName}`, description: `${p.displayName} ${p.version} in TypeIcon: ${p.designs} icons, ${p.licenseId}.`, alternates: { canonical: `/packs/${slug}` } } : {};
}

export default async function PackPage(props: PageProps<"/packs/[slug]">) {
  const { slug } = await props.params;
  const p = (await listPacks()).find((x) => x.slug === slug);
  if (!p) notFound();
  const r = await searchIcons(parseSearchParams({ pack: slug, per: "96" }));
  return (
    <div className="mx-auto max-w-[1440px] px-4 pb-24 pt-8 sm:px-6">
      <nav aria-label="Breadcrumb" className="mb-3 text-sm text-muted"><Link href="/packs" className="hover:text-text">Packs</Link> / {p.displayName}</nav>
      <div className="grid grid-cols-[minmax(0,1fr)] gap-8 lg:grid-cols-[minmax(0,1fr)_380px]">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight">{p.displayName}</h1>
          <p className="mt-1 text-text-2">{p.area === "core" ? "TypeIcon Core" : "Brand logos"} · version {p.version} · {fmt(p.designs)} icons · {fmt(p.variants)} style variants</p>
          <h2 className="mb-2 mt-6 text-sm font-semibold">Style mapping</h2>
          <div className="overflow-x-auto rounded-xl border border-border bg-surface">
            <table className="w-full text-sm">
              <thead><tr className="border-b border-border text-left text-xs uppercase tracking-wider text-muted"><th className="px-3 py-2">Upstream style</th><th className="px-3 py-2">TypeIcon style</th><th className="px-3 py-2 text-right">Published</th></tr></thead>
              <tbody>
                {Object.entries(p.styleMapping).map(([native, m]) => (
                  <tr key={native} className="border-b border-border last:border-0">
                    <td className="px-3 py-2 text-text-2">{m.nativeLabel ?? native}</td>
                    <td className="px-3 py-2 text-text">{STYLE_LABEL[m.style] ?? m.style}</td>
                    <td className="px-3 py-2 text-right tabular-nums text-text-2">{fmt(p.byStyle[m.style] ?? 0)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {p.styleMappingNote && <p className="mt-2 text-sm text-muted">{p.styleMappingNote}</p>}
        </div>
        <aside className="rounded-2xl border border-border bg-surface p-4 text-sm">
          <h2 className="mb-3 font-semibold">Provenance</h2>
          <dl className="grid grid-cols-[100px_1fr] gap-x-3 gap-y-2">
            <dt className="text-muted">License</dt><dd><Link href={`/licenses#${p.slug}`} className="text-text hover:text-accent">{p.licenseId}</Link></dd>
            {p.copyright && (<><dt className="text-muted">Copyright</dt><dd className="text-text-2">{p.copyright}</dd></>)}
            {p.author && (<><dt className="text-muted">Author</dt><dd className="text-text-2">{p.author}</dd></>)}
            {p.upstreamUrl && (<><dt className="text-muted">Upstream</dt><dd className="break-all text-text-2">{p.upstreamUrl}</dd></>)}
            {p.distribution.package && (<><dt className="text-muted">Package</dt><dd className="break-all font-mono text-xs text-text-2">{p.distribution.package}@{p.version}</dd></>)}
            {p.distribution.integrity && (<><dt className="text-muted">Integrity</dt><dd className="break-all font-mono text-[10px] text-text-2">{p.distribution.integrity}</dd></>)}
            {p.retrievedAt && (<><dt className="text-muted">Retrieved</dt><dd className="text-text-2">{p.retrievedAt}</dd></>)}
            {p.attributionText && (<><dt className="text-muted">Attribution</dt><dd className="text-text-2">{p.attributionText}</dd></>)}
            <dt className="text-muted">Review</dt><dd className="text-text-2">{p.reviewStatus}{p.reviewNote ? `. ${p.reviewNote}` : ""}</dd>
          </dl>
          {p.modificationHistory.length > 0 && (
            <>
              <h3 className="mb-1 mt-4 font-medium">Modifications by TypeIcon</h3>
              <ul className="list-disc space-y-1 pl-5 text-text-2">{p.modificationHistory.map((m) => <li key={m}>{m}</li>)}</ul>
            </>
          )}
          {p.trademarkNote && <p className="mt-4 text-xs text-muted">{p.trademarkNote}</p>}
          {p.notices.map((n) => <p key={n} className="mt-2 text-xs text-muted">{n}</p>)}
        </aside>
      </div>
      <div className="mb-3 mt-10 flex items-center justify-between">
        <h2 className="text-lg font-semibold">Icons</h2>
        <Link href={`/icons?pack=${slug}`} className="text-sm text-accent hover:underline">All {fmt(p.designs)} in catalog →</Link>
      </div>
      <StaticGrid items={r.items} label={`${p.displayName} icons`} />
    </div>
  );
}
