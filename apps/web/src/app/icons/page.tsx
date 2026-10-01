import type { Metadata } from "next";
import Link from "next/link";
import { Suspense } from "react";
import { FilterPanel } from "@/components/catalog/filter-panel";
import { IconResults } from "@/components/catalog/icon-results";
import { MobileFilters } from "@/components/catalog/mobile-filters";
import { Pagination } from "@/components/catalog/pagination";
import { SortControls } from "@/components/catalog/sort-controls";
import { UiIcon } from "@/components/ui-icon";
import { cn } from "@/lib/cn";
import { fmt, STYLE_LABEL } from "@/lib/format";
import { parseSearchParams, searchIcons, toQueryString } from "@/lib/search";

export const dynamic = "force-dynamic";

export async function generateMetadata(props: PageProps<"/icons">): Promise<Metadata> {
  const input = parseSearchParams(await props.searchParams);
  const filtered = input.q || input.category.length || input.pack.length || input.license.length || input.page > 1;
  return {
    title: input.q ? `"${input.q}" icons` : "Icons",
    description: "Search TypeIcon Core icons and brand logos by name, alias, tag and category.",
    alternates: { canonical: "/icons" },
    // Filter permutations are not indexed; the canonical catalog page is.
    robots: filtered ? { index: false, follow: true } : undefined,
  };
}

export default async function IconsPage(props: PageProps<"/icons">) {
  const input = parseSearchParams(await props.searchParams);
  const result = await searchIcons(input);
  const { facets } = result;
  const allCount = input.style === "all" || input.missing ? result.total : result.total + result.missingInStyle;
  const chips: { label: string; href: string }[] = [];
  if (input.q) chips.push({ label: `"${input.q}"`, href: "/icons" + toQueryString(input, { q: "", page: 1 }) });
  for (const p of input.pack) chips.push({ label: facets.packs.find((f) => f.value === p)?.label ?? p, href: "/icons" + toQueryString(input, { pack: input.pack.filter((x) => x !== p), page: 1 }) });
  for (const c of input.category) chips.push({ label: c.replace(/-/g, " "), href: "/icons" + toQueryString(input, { category: input.category.filter((x) => x !== c), page: 1 }) });
  for (const l of input.license) chips.push({ label: l, href: "/icons" + toQueryString(input, { license: input.license.filter((x) => x !== l), page: 1 }) });
  if (input.area !== "all") chips.push({ label: input.area === "core" ? "Core only" : "Brands only", href: "/icons" + toQueryString(input, { area: "all", page: 1 }) });
  if (input.brands !== "include") chips.push({ label: input.brands === "only" ? "Brands only" : "No brands", href: "/icons" + toQueryString(input, { brands: "include", page: 1 }) });
  const activeFilters = chips.length - (input.q ? 1 : 0);
  const styleTabs = [{ value: "all", label: "All", count: allCount }, ...facets.styles.map((s) => ({ value: s.value, label: s.value === "brand" ? "Brands" : s.label, count: s.count }))];
  const panel = <FilterPanel input={input} facets={facets} />;

  return (
    <div className="mx-auto max-w-[1440px] px-4 pb-32 pt-6 sm:px-6">
      <div className="mb-5 flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-text">{input.q ? <>Icons matching &quot;{input.q}&quot;</> : "Icons"}</h1>
          <p className="mt-1 text-sm text-muted" aria-live="polite">
            <span className="font-medium text-text-2 tabular-nums">{fmt(result.total)}</span> {result.total === 1 ? "icon" : "icons"}
            {input.style !== "all" && <> in {STYLE_LABEL[input.style]}</>}
            {input.missing && <> (including {fmt(result.missingInStyle)} without this style)</>}
            <span className="ml-2 text-xs">· {result.tookMs.toFixed(0)} ms</span>
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Suspense>
            <MobileFilters activeCount={activeFilters}>{panel}</MobileFilters>
          </Suspense>
          <SortControls input={input} />
        </div>
      </div>

      <nav aria-label="Style" className="mb-4 flex gap-1 overflow-x-auto border-b border-border">
        {styleTabs.map((t) => {
          const on = input.style === t.value;
          return (
            <Link
              key={t.value}
              href={"/icons" + toQueryString(input, { style: t.value as typeof input.style, page: 1, missing: false })}
              scroll={false}
              aria-current={on ? "page" : undefined}
              className={cn(
                "-mb-px flex shrink-0 items-center gap-2 border-b-2 px-3 py-2.5 text-sm font-medium",
                on ? "border-accent text-text" : "border-transparent text-muted hover:text-text",
              )}
            >
              {t.label}
              <span className="rounded-full bg-surface-2 px-1.5 text-[11px] tabular-nums text-muted">{fmt(t.count)}</span>
            </Link>
          );
        })}
      </nav>

      {chips.length > 0 && (
        <ul className="mb-4 flex flex-wrap items-center gap-2" aria-label="Active filters">
          {chips.map((c) => (
            <li key={c.href + c.label}>
              <Link href={c.href} scroll={false} className="inline-flex items-center gap-1.5 rounded-full border border-border bg-surface px-3 py-1 text-xs text-text-2 hover:border-border-strong">
                {c.label}
                <UiIcon name="close" size={12} label={`Remove filter ${c.label}`} />
              </Link>
            </li>
          ))}
          <li>
            <Link href={`/icons${input.style !== "all" ? `?style=${input.style}` : ""}`} className="text-xs text-accent hover:underline">
              Clear all
            </Link>
          </li>
        </ul>
      )}

      <div className="grid grid-cols-[minmax(0,1fr)] gap-8 lg:grid-cols-[232px_minmax(0,1fr)]">
        <aside className="hidden lg:block" aria-label="Filters">
          <div className="sticky top-20 max-h-[calc(100dvh-6rem)] overflow-y-auto pr-2 scrollbar-thin">{panel}</div>
        </aside>
        <div className="min-w-0">
          {input.style !== "all" && result.missingInStyle > 0 && !input.missing && (
            <p className="mb-3 rounded-xl border border-border bg-surface px-4 py-2.5 text-sm text-text-2">
              {fmt(result.missingInStyle)} matching {result.missingInStyle === 1 ? "icon has" : "icons have"} no {STYLE_LABEL[input.style]} style and{" "}
              {result.missingInStyle === 1 ? "is" : "are"} hidden. TypeIcon never substitutes a different style.{" "}
              <Link href={"/icons" + toQueryString(input, { missing: true, page: 1 })} className="text-accent underline underline-offset-2 hover:text-accent-hover">
                Show them as unavailable
              </Link>
            </p>
          )}
          {result.items.length ? (
            <Suspense>
              <IconResults items={result.items} requestedStyle={input.style} />
            </Suspense>
          ) : (
            <div className="rounded-2xl border border-dashed border-border-strong px-6 py-16 text-center">
              <p className="text-base font-medium text-text">No icons match {input.q ? <>&quot;{input.q}&quot;</> : "these filters"}.</p>
              <p className="mx-auto mt-2 max-w-md text-sm text-muted">
                Try a shorter word, a synonym (house, gear, magnify), or remove filters. Fonts only understand exact keywords, but search also checks aliases, tags and categories.
              </p>
              <Link href="/icons" className="mt-4 inline-block text-sm text-accent hover:underline">
                Browse all icons
              </Link>
            </div>
          )}
          <Pagination input={input} pages={result.pages} />
        </div>
      </div>
    </div>
  );
}
