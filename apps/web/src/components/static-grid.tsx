import Link from "next/link";
import type { IconCard } from "@/lib/search-params";
import { RegisterResults } from "./catalog/register-results";
import { IconSvg } from "./icon-svg";

/** Server-rendered icon grid for curated listing pages (no client JS needed). */
export function StaticGrid({ items, label }: { items: IconCard[]; label: string }) {
  return (
    <>
    <RegisterResults entries={items.map((i) => ({ name: i.name, style: i.displayStyle }))} />
    <ul className="grid grid-cols-[repeat(auto-fill,minmax(112px,1fr))] gap-2" aria-label={label}>
      {items.map((i) => (
        <li key={i.id}>
          <Link
            href={`/icons/${i.name}${i.displayStyle ? `?style=${i.displayStyle}` : ""}`}
            className="flex h-[116px] flex-col items-center justify-center gap-2 rounded-xl border border-border bg-surface px-2 text-center hover:border-border-strong hover:bg-surface-2"
          >
            <span className="flex flex-1 items-center text-text">
              {i.displayStyle ? <IconSvg svg={i.svg} size={28} /> : <span className="text-[11px] text-muted">Unavailable</span>}
            </span>
            <span className="w-full truncate pb-2 text-[12px] text-text-2">{i.name}</span>
          </Link>
        </li>
      ))}
    </ul>
    </>
  );
}
