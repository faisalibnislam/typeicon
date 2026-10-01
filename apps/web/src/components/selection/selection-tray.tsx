"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { IconSvgClient } from "../icon-svg-client";
import { UiIcon } from "../ui-icon";
import { useSelection } from "./selection-provider";

export function SelectionTray() {
  const { items, remove, clear } = useSelection();
  const [open, setOpen] = useState(true);
  const pathname = usePathname();
  const [announce, setAnnounce] = useState("");
  if (!items.length || pathname.startsWith("/downloads/subset")) return null;
  return (
    <section aria-label="Selected icons" className="fixed inset-x-0 bottom-0 z-40 border-t border-border bg-surface/95 shadow-[0_-8px_24px_rgba(0,0,0,0.06)] backdrop-blur">
      <div className="mx-auto flex max-w-[1440px] items-center gap-3 px-4 py-2.5 sm:px-6">
        <button
          type="button"
          onClick={() => setOpen((o) => !o)}
          aria-expanded={open}
          className="inline-flex shrink-0 items-center gap-2 rounded-lg px-2 py-1.5 text-sm font-medium text-text hover:bg-surface-2"
        >
          <span className="inline-flex h-6 min-w-6 items-center justify-center rounded-full bg-accent px-1.5 text-xs font-semibold text-accent-contrast">{items.length}</span>
          selected
          <UiIcon name="chevron-down" size={16} className={open ? "" : "rotate-180"} />
        </button>
        {open && (
          <ul className="scrollbar-thin flex min-w-0 flex-1 gap-1 overflow-x-auto py-1" aria-label="Selection">
            {items.map((i) => (
              <li key={`${i.designId}:${i.style}`}>
                <button
                  type="button"
                  title={`Remove ${i.name} (${i.style})`}
                  aria-label={`Remove ${i.name} ${i.style} from selection`}
                  onClick={() => {
                    remove(i.designId, i.style);
                    setAnnounce(`Removed ${i.name}`);
                  }}
                  className="group relative flex h-10 w-10 items-center justify-center rounded-lg border border-border bg-bg text-text hover:border-danger"
                >
                  <IconSvgClient svg={i.svg} size={20} />
                  <span className="absolute -right-1 -top-1 hidden h-4 w-4 items-center justify-center rounded-full bg-danger text-[10px] text-white group-hover:flex">×</span>
                </button>
              </li>
            ))}
          </ul>
        )}
        {!open && <div className="flex-1" />}
        <div className="flex shrink-0 items-center gap-2">
          <button type="button" onClick={clear} className="rounded-lg px-3 py-2 text-sm text-muted hover:bg-surface-2 hover:text-text">
            Clear
          </button>
          <Link href="/downloads/subset" className="inline-flex items-center gap-2 rounded-lg bg-accent px-3.5 py-2 text-sm font-semibold text-accent-contrast hover:bg-accent-hover">
            <UiIcon name="download" size={16} />
            Build subset
          </Link>
        </div>
      </div>
      <p className="sr-only" aria-live="polite">{announce}</p>
    </section>
  );
}
