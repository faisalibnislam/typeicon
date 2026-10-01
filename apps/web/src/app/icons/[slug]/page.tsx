import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Suspense } from "react";
import { CopyName } from "@/components/copy-name";
import { IconDetail } from "@/components/detail/icon-detail";
import { BrandFacts } from "@/components/detail/brand-facts";
import { IconSvg } from "@/components/icon-svg";
import { getDesign, getLatestRelease, getRelated } from "@/lib/catalog";
import { STYLE_LABEL } from "@/lib/format";

export const dynamic = "force-dynamic";

export async function generateMetadata(props: PageProps<"/icons/[slug]">): Promise<Metadata> {
  const { slug } = await props.params;
  const d = await getDesign(slug);
  if (!d) return { title: "Icon not found" };
  const styles = d.variants.map((v) => STYLE_LABEL[v.style]).join(", ");
  return {
    title: d.area === "brands" ? `${d.attributes.title ?? d.name} logo` : `${d.name} icon`,
    description: `${d.name} from ${d.source.displayName} (${d.license.id}). Styles: ${styles}. Download SVG or PNG, copy code, or type "${d.name}" with a TypeIcon font.`,
    alternates: { canonical: `/icons/${d.name}` },
  };
}

export default async function IconPage(props: PageProps<"/icons/[slug]">) {
  const { slug } = await props.params;
  const design = await getDesign(slug);
  if (!design) notFound();
  const [related, release] = await Promise.all([getRelated(design), getLatestRelease()]);
  const searchTerms = [...new Set([...design.tags, ...design.keywords])];
  const cssHref = release ? `/api/files/releases/${release.version}/css/${design.area === "core" ? "typeicon.css" : `typeicon-${design.source.slug}.css`}` : null;
  const site = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3107";
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "ImageObject",
    name: `${design.name} icon`,
    description: design.description ?? `${design.name} icon from ${design.source.displayName}`,
    contentUrl: `${site}/api/icons/${design.name}/svg?style=${design.variants[0]?.style ?? "line"}`,
    encodingFormat: "image/svg+xml",
    license: design.license.url ?? `${site}/licenses#${design.source.slug}`,
    creditText: design.source.attributionText ?? design.source.displayName,
    copyrightNotice: design.source.copyright ?? undefined,
    keywords: [...design.tags, ...design.aliases, ...design.keywords.slice(0, 20)].join(", "),
  };

  return (
    <div className="mx-auto max-w-[1440px] px-4 pb-32 pt-6 sm:px-6">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd).replace(/</g, "\\u003c") }} />
      <nav aria-label="Breadcrumb" className="mb-4 text-sm text-muted">
        <ol className="flex flex-wrap items-center gap-1.5">
          <li><Link href="/icons" className="hover:text-text">Icons</Link></li>
          <li aria-hidden="true">/</li>
          <li><Link href={`/packs/${design.source.slug}`} className="hover:text-text">{design.source.displayName}</Link></li>
          <li aria-hidden="true">/</li>
          <li aria-current="page" className="text-text-2">{design.name}</li>
        </ol>
      </nav>
      <header className="mb-6">
        <div className="flex flex-wrap items-center gap-3">
          <CopyName name={design.name} className="text-3xl" />
          <span className="rounded-full border border-border px-2.5 py-0.5 text-xs text-text-2">{design.area === "core" ? "TypeIcon Core" : "Brand logo"}</span>
          {design.isBrand && <span className="rounded-full border border-border px-2.5 py-0.5 text-xs text-text-2">Brand</span>}
        </div>
        {design.description && <p className="mt-2 max-w-2xl text-text-2">{design.description}</p>}
        {design.context && <p className="mt-2 max-w-2xl text-sm text-muted">{design.context}</p>}
        <div className="mt-3 flex flex-wrap gap-x-6 gap-y-2 text-sm">
          {design.aliases.length > 0 && (
            <p className="text-muted">Aliases: {design.aliases.map((a) => <code key={a} className="mr-1 rounded bg-surface-2 px-1.5 py-0.5 font-mono text-xs text-text-2">{a}</code>)}</p>
          )}
          {design.categories.length > 0 && (
            <p className="text-muted">
              Categories:{" "}
              {design.categories.map((c, i) => (
                <span key={c}>{i > 0 && ", "}<Link href={`/categories/${c}`} className="text-text-2 underline decoration-border-strong underline-offset-2 hover:text-accent">{c.replace(/-/g, " ")}</Link></span>
              ))}
            </p>
          )}
        </div>
        {design.attributes.variantOf && (
          <p className="mt-2 text-sm text-muted">
            Variant of <Link href={`/icons/${design.attributes.variantOf.name}`} className="text-text-2 underline decoration-border-strong underline-offset-2 hover:text-accent">{design.attributes.variantOf.name}</Link> with the &quot;{design.attributes.variantOf.modifier}&quot; badge.
          </p>
        )}
        {design.derivedFrom && (
          <p className="mt-2 text-sm text-muted">
            Derived from <Link href={`/icons/${design.derivedFrom.name}`} className="text-text-2 underline decoration-border-strong underline-offset-2 hover:text-accent">{design.derivedFrom.name}</Link> ({design.derivedFrom.transform.replace(/rotate\((\d+) 12 12\)/, "rotated $1°")}); not counted as independent artwork.
          </p>
        )}
        {design.attributes.designReview?.status === "pending" && (
          <p className="mt-2 text-sm text-muted">Newly drawn and not yet reviewed by a designer.</p>
        )}
        {design.area === "brands" && <BrandFacts design={design} />}
      </header>

      <Suspense>
        <IconDetail design={design} cssHref={cssHref} />
      </Suspense>

      {searchTerms.length > 0 && (
        <section className="mt-10" aria-labelledby="tags-h">
          <h2 id="tags-h" className="mb-2 text-sm font-semibold text-text">Search tags</h2>
          <ul className="flex flex-wrap gap-1.5">
            {searchTerms.map((t) => (
              <li key={t}>
                <Link href={`/icons?q=${encodeURIComponent(t)}`} className="rounded-full border border-border bg-surface px-2.5 py-1 text-xs text-text-2 hover:border-border-strong">{t}</Link>
              </li>
            ))}
          </ul>
          <p className="mt-2 text-xs text-muted">Tags help website search only. Fonts respond to the keyword and explicit aliases.</p>
        </section>
      )}

      {related.length > 0 && (
        <section className="mt-10" aria-labelledby="related-h">
          <h2 id="related-h" className="mb-3 text-sm font-semibold text-text">Related icons</h2>
          <ul className="grid grid-cols-[repeat(auto-fill,minmax(104px,1fr))] gap-2">
            {related.map((r) => (
              <li key={r.name}>
                <Link href={`/icons/${r.name}?style=${r.style}`} className="flex h-[104px] flex-col items-center justify-center gap-2 rounded-xl border border-border bg-surface px-2 text-center hover:border-border-strong">
                  <IconSvg svg={r.svg} size={26} />
                  <span className="w-full truncate text-[11px] text-text-2">{r.name}</span>
                  <span className="sr-only">{r.relation === "same-concept" ? `(same concept, ${r.sourceName})` : "(same category)"}</span>
                </Link>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
