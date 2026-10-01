import Link from "next/link";
import type { SearchInput } from "@/lib/search-params";
import { toQueryString } from "@/lib/search-params";
import { cn } from "@/lib/cn";

export function Pagination({ input, pages }: { input: SearchInput; pages: number }) {
  if (pages <= 1) return null;
  const cur = input.page;
  const nums = new Set([1, pages, cur - 2, cur - 1, cur, cur + 1, cur + 2].filter((n) => n >= 1 && n <= pages));
  const sorted = [...nums].sort((a, b) => a - b);
  const href = (page: number) => "/icons" + toQueryString(input, { page });
  return (
    <nav aria-label="Pagination" className="mt-8 flex flex-wrap items-center justify-center gap-1">
      {cur > 1 ? (
        <Link href={href(cur - 1)} rel="prev" className="rounded-lg px-3 py-2 text-sm text-text-2 hover:bg-surface-2">
          ← Previous
        </Link>
      ) : (
        <span aria-disabled="true" className="px-3 py-2 text-sm text-muted">← Previous</span>
      )}
      {sorted.map((n, idx) => (
        <span key={n} className="flex items-center">
          {idx > 0 && sorted[idx - 1] !== n - 1 && <span className="px-1 text-muted">…</span>}
          <Link
            href={href(n)}
            aria-current={n === cur ? "page" : undefined}
            className={cn("min-w-9 rounded-lg px-2.5 py-2 text-center text-sm tabular-nums", n === cur ? "bg-text text-bg" : "text-text-2 hover:bg-surface-2")}
          >
            {n}
          </Link>
        </span>
      ))}
      {cur < pages ? (
        <Link href={href(cur + 1)} rel="next" className="rounded-lg px-3 py-2 text-sm text-text-2 hover:bg-surface-2">
          Next →
        </Link>
      ) : (
        <span aria-disabled="true" className="px-3 py-2 text-sm text-muted">Next →</span>
      )}
    </nav>
  );
}
