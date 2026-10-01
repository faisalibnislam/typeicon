import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { CategoryPack } from "@/components/category-pack";
import { StaticGrid } from "@/components/static-grid";
import { getCategory } from "@/lib/catalog";
import { fmt } from "@/lib/format";
import { parseSearchParams, searchIcons } from "@/lib/search";

export const dynamic = "force-dynamic";

export async function generateMetadata(props: PageProps<"/categories/[slug]">): Promise<Metadata> {
  const c = await getCategory((await props.params).slug);
  return c ? { title: `${c.name} icons`, description: `${c.name} icons in TypeIcon.`, alternates: { canonical: `/categories/${c.slug}` } } : {};
}

export default async function CategoryPage(props: PageProps<"/categories/[slug]">) {
  const { slug } = await props.params;
  const cat = await getCategory(slug);
  if (!cat) notFound();
  const r = await searchIcons(parseSearchParams({ category: slug, per: "192" }));
  return (
    <div className="mx-auto max-w-[1440px] px-4 pb-24 pt-8 sm:px-6">
      <nav aria-label="Breadcrumb" className="mb-3 text-sm text-muted"><Link href="/categories" className="hover:text-text">Categories</Link> / {cat.name}</nav>
      <div className="mb-6 flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight">{cat.name}</h1>
          <p className="mt-1 text-sm text-text-2">{fmt(r.total)} icons · {r.facets.packs.map((p) => `${p.label} ${fmt(p.count)}`).join(" · ")}</p>
        </div>
        <Link href={`/icons?category=${slug}`} className="rounded-xl border border-border bg-surface px-3.5 py-2 text-sm font-medium hover:bg-surface-2">Filter and search in catalog →</Link>
      </div>
      <div className="mb-5">
        <CategoryPack category={slug} packs={r.facets.packs.filter((p) => p.count <= 500)} />
      </div>
      <StaticGrid items={r.items} label={`${cat.name} icons`} />
      {r.total > r.items.length && (
        <p className="mt-6 text-center text-sm"><Link href={`/icons?category=${slug}&page=2&per=192`} className="text-accent underline underline-offset-2 hover:text-accent-hover">Show more ({fmt(r.total - r.items.length)} remaining)</Link></p>
      )}
    </div>
  );
}
