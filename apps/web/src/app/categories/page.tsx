import type { Metadata } from "next";
import Link from "next/link";
import { listCategories } from "@/lib/catalog";
import { fmt } from "@/lib/format";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Categories", description: "Browse TypeIcon icons by category.", alternates: { canonical: "/categories" } };

export default async function CategoriesPage() {
  const cats = await listCategories();
  return (
    <div className="mx-auto max-w-[1200px] px-4 pb-24 pt-8 sm:px-6">
      <h1 className="text-3xl font-semibold tracking-tight">Categories</h1>
      <p className="mb-8 mt-2 text-text-2">Categories come from TypeIcon Core metadata; brand logos are grouped under Brands. Counts include published icons only.</p>
      <ul className="grid gap-2 sm:grid-cols-2 lg:grid-cols-4">
        {cats.map((c) => (
          <li key={c.slug}>
            <Link href={`/categories/${c.slug}`} className="flex items-center justify-between rounded-xl border border-border bg-surface px-4 py-3 hover:border-border-strong">
              <span className="font-medium text-text">{c.name}</span>
              <span className="text-xs tabular-nums text-muted">
                {fmt(c.count)}
                {c.coreCount > 0 && <span className="ml-1 text-accent">· {c.coreCount} Core</span>}
              </span>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
