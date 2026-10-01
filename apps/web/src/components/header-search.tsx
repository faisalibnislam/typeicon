"use client";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { UiIcon } from "./ui-icon";

/** Global search box. On /icons it drives the catalog query (debounced, URL-synced). */
export function HeaderSearch({ autoFocusKey = "/" }: { autoFocusKey?: string }) {
  const router = useRouter();
  const pathname = usePathname();
  const params = useSearchParams();
  const onCatalog = pathname === "/icons";
  const urlQ = onCatalog ? (params.get("q") ?? "") : "";
  const [value, setValue] = useState(urlQ);
  const inputRef = useRef<HTMLInputElement>(null);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => setValue(urlQ), [urlQ]);
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement;
      if (e.key === autoFocusKey && !["INPUT", "TEXTAREA", "SELECT"].includes(t.tagName) && !t.isContentEditable) {
        e.preventDefault();
        inputRef.current?.focus();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [autoFocusKey]);

  function go(q: string, replace: boolean) {
    const next = new URLSearchParams(onCatalog ? params.toString() : "");
    if (q) next.set("q", q.slice(0, 64));
    else next.delete("q");
    next.delete("page");
    const url = `/icons${next.toString() ? `?${next}` : ""}`;
    if (replace && onCatalog) router.replace(url, { scroll: false });
    else router.push(url);
  }

  return (
    <form
      role="search"
      className="relative w-full"
      onSubmit={(e) => {
        e.preventDefault();
        if (timer.current) clearTimeout(timer.current);
        go(value.trim(), false);
      }}
    >
      <label htmlFor="global-search" className="sr-only">
        Search icons
      </label>
      <UiIcon name="search" size={18} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-muted" />
      <input
        ref={inputRef}
        id="global-search"
        type="search"
        inputMode="search"
        autoComplete="off"
        spellCheck={false}
        maxLength={64}
        placeholder="Search icons, e.g. home, gear, arrow right"
        value={value}
        onChange={(e) => {
          const v = e.target.value;
          setValue(v);
          if (onCatalog) {
            if (timer.current) clearTimeout(timer.current);
            timer.current = setTimeout(() => go(v.trim(), true), 250);
          }
        }}
        className="h-10 w-full rounded-xl border border-border bg-surface pl-10 pr-12 text-[15px] text-text placeholder:text-muted/80 hover:border-border-strong focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/25"
      />
      <kbd className="pointer-events-none absolute right-3 top-1/2 hidden -translate-y-1/2 rounded border border-border bg-surface-2 px-1.5 font-mono text-[11px] text-muted sm:block">
        /
      </kbd>
    </form>
  );
}
