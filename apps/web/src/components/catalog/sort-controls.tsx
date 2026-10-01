"use client";
import { useRouter } from "next/navigation";
import type { SearchInput } from "@/lib/search-params";
import { PER_PAGE_OPTIONS, toQueryString } from "@/lib/search-params";

export function SortControls({ input }: { input: SearchInput }) {
  const router = useRouter();
  return (
    <div className="flex items-center gap-2">
      <label className="flex items-center gap-1.5 text-xs text-muted">
        Sort
        <select
          value={input.sort}
          onChange={(e) => router.push("/icons" + toQueryString(input, { sort: e.target.value as SearchInput["sort"], page: 1 }), { scroll: false })}
          className="h-8 rounded-lg border border-border bg-surface px-2 text-xs text-text"
        >
          <option value="relevance">{input.q ? "Relevance" : "Core first"}</option>
          <option value="name">Name</option>
          <option value="pack">Pack</option>
        </select>
      </label>
      <label className="flex items-center gap-1.5 text-xs text-muted">
        Per page
        <select
          value={input.per}
          onChange={(e) => router.push("/icons" + toQueryString(input, { per: Number(e.target.value), page: 1 }), { scroll: false })}
          className="h-8 rounded-lg border border-border bg-surface px-2 text-xs text-text"
        >
          {PER_PAGE_OPTIONS.map((n) => (
            <option key={n} value={n}>
              {n}
            </option>
          ))}
        </select>
      </label>
    </div>
  );
}
