import Link from "next/link";
import type { Facet, SearchInput } from "@/lib/search-params";
import { toQueryString } from "@/lib/search-params";
import { fmt } from "@/lib/format";
import { cn } from "@/lib/cn";

type ListKey = "pack" | "category" | "license";

function toggle(input: SearchInput, key: ListKey, value: string): string {
  const cur = input[key];
  const next = cur.includes(value) ? cur.filter((v) => v !== value) : [...cur, value];
  return "/icons" + toQueryString(input, { [key]: next, page: 1 });
}

function FacetList({ title, input, keyName, facets, limit = 12 }: { title: string; input: SearchInput; keyName: ListKey; facets: Facet[]; limit?: number }) {
  const selected = input[keyName];
  const shown = [...facets.filter((f) => selected.includes(f.value)), ...facets.filter((f) => !selected.includes(f.value))].slice(0, Math.max(limit, selected.length));
  const extra = facets.length - shown.length;
  return (
    <fieldset className="border-t border-border py-4 first:border-t-0 first:pt-0">
      <legend className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted">{title}</legend>
      <ul className="space-y-0.5">
        {shown.map((f) => {
          const on = selected.includes(f.value);
          return (
            <li key={f.value}>
              <Link
                href={toggle(input, keyName, f.value)}
                scroll={false}
                className={cn("flex items-center gap-2.5 rounded-lg px-2 py-1.5 text-sm hover:bg-surface-2", on ? "text-text" : "text-text-2")}
              >
                <span aria-hidden="true" className={cn("flex h-4 w-4 shrink-0 items-center justify-center rounded border", on ? "border-accent bg-accent text-accent-contrast" : "border-border-strong")}>
                  {on && <svg width="10" height="10" viewBox="0 0 12 12"><path d="M2 6.5l2.5 2.5L10 3.5" fill="none" stroke="currentColor" strokeWidth="2" /></svg>}
                </span>
                <span className="min-w-0 flex-1 truncate">{f.label}</span>
                <span className="tabular-nums text-xs text-muted">{fmt(f.count)}</span>
                <span className="sr-only">{on ? "(selected, activate to remove)" : "(activate to filter)"}</span>
              </Link>
            </li>
          );
        })}
      </ul>
      {extra > 0 && <p className="mt-1 px-2 text-xs text-muted">+{extra} more with results. Refine your search to narrow the list.</p>}
    </fieldset>
  );
}

export function FilterPanel({ input, facets }: { input: SearchInput; facets: { packs: Facet[]; licenses: Facet[]; categories: Facet[]; areas: Facet[] } }) {
  const areaLink = (area: SearchInput["area"]) => "/icons" + toQueryString(input, { area, page: 1 });
  const areaCount = (a: string) => facets.areas.find((f) => f.value === a)?.count ?? 0;
  return (
    <div className="text-sm">
      <fieldset className="pb-4">
        <legend className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted">Catalog area</legend>
        <div className="grid grid-cols-3 gap-1 rounded-xl bg-surface-2 p-1">
          {(
            [
              ["all", "All", areaCount("core") + areaCount("brands")],
              ["core", "Core", areaCount("core")],
              ["brands", "Brands", areaCount("brands")],
            ] as const
          ).map(([v, l, n]) => (
            <Link
              key={v}
              href={areaLink(v)}
              scroll={false}
              aria-current={input.area === v ? "true" : undefined}
              className={cn("rounded-lg px-2 py-1.5 text-center text-xs font-medium", input.area === v ? "bg-surface text-text shadow-sm" : "text-muted hover:text-text")}
            >
              {l}
              <span className="block tabular-nums text-[11px] font-normal text-muted">{fmt(n)}</span>
            </Link>
          ))}
        </div>
      </fieldset>
      <FacetList title="Category" input={input} keyName="category" facets={facets.categories} limit={14} />
      <FacetList title="License" input={input} keyName="license" facets={facets.licenses} />
    </div>
  );
}
