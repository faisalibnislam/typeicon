"use client";
import * as Dialog from "@radix-ui/react-dialog";
import { useRouter, useSearchParams } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { cn } from "@/lib/cn";
import { useResultsNav } from "../catalog/results-nav";
import { CopyName } from "../copy-name";
import { UiIcon } from "../ui-icon";

/**
 * Icon detail shown over the catalog (intercepted /icons/[slug] route). The URL is the icon's own
 * shareable URL; Escape, the close button, the backdrop and browser Back all return to the results.
 * Arrow keys / side buttons step through the results that were visible in the grid.
 */
export function IconModal({
  name,
  codepointHex,
  summary,
  children,
}: {
  name: string;
  codepointHex: string | null;
  summary: React.ReactNode;
  children: React.ReactNode;
}) {
  const router = useRouter();
  const params = useSearchParams();
  const { entries } = useResultsNav();
  const [linkCopied, setLinkCopied] = useState(false);
  const idx = entries.findIndex((e) => e.name === name);
  const prev = idx > 0 ? entries[idx - 1] : null;
  const next = idx >= 0 && idx < entries.length - 1 ? entries[idx + 1] : null;
  const style = params.get("style");

  const go = useCallback(
    (e: { name: string; style: string | null } | null) => {
      if (!e) return;
      // Keep the chosen style when the next icon has it; otherwise the grid's display style.
      const s = e.style ?? style;
      router.replace(`/icons/${e.name}${s ? `?style=${s}` : ""}`, { scroll: false });
    },
    [router, style],
  );

  useEffect(() => {
    const onKey = (ev: KeyboardEvent) => {
      const t = ev.target as HTMLElement;
      if (["INPUT", "TEXTAREA", "SELECT"].includes(t.tagName) || t.isContentEditable || t.closest("[role=tablist],[role=radiogroup]")) return;
      if (ev.key === "ArrowLeft") go(prev);
      if (ev.key === "ArrowRight") go(next);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [go, prev, next]);

  async function copyLink() {
    try {
      await navigator.clipboard.writeText(`${window.location.origin}/icons/${name}${style ? `?style=${style}` : ""}`);
      setLinkCopied(true);
      setTimeout(() => setLinkCopied(false), 1600);
    } catch {}
  }

  const arrow = "fixed top-1/2 z-[60] hidden h-12 w-12 -translate-y-1/2 items-center justify-center rounded-full bg-surface/90 text-text shadow-lg ring-1 ring-border hover:bg-surface md:flex";
  return (
    <Dialog.Root open onOpenChange={(open) => !open && router.back()}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 z-50 bg-[#0d0d0f]/55 backdrop-blur-[2px]" />
        {prev && (
          <button type="button" data-modal-nav onClick={() => go(prev)} className={cn(arrow, "left-4")} aria-label={`Previous icon: ${prev.name}`}>
            <UiIcon name="arrow-left" size={20} />
          </button>
        )}
        {next && (
          <button type="button" data-modal-nav onClick={() => go(next)} className={cn(arrow, "right-4")} aria-label={`Next icon: ${next.name}`}>
            <UiIcon name="arrow-right" size={20} />
          </button>
        )}
        <Dialog.Content
          aria-describedby={undefined}
          onPointerDownOutside={(e) => {
            if ((e.target as HTMLElement | null)?.closest("[data-modal-nav]")) e.preventDefault();
          }}
          className="fixed left-1/2 top-4 z-50 flex max-h-[calc(100dvh-2rem)] w-[calc(100vw-1.5rem)] max-w-[1080px] -translate-x-1/2 flex-col overflow-hidden rounded-2xl border border-border bg-bg shadow-2xl sm:top-8 sm:max-h-[calc(100dvh-4rem)]"
        >
          <header className="flex flex-wrap items-center gap-x-3 gap-y-2 border-b border-border px-4 pb-3 pt-4 sm:px-6">
            <Dialog.Title asChild>
              <div className="flex min-w-0 items-center gap-2">
                <CopyName name={name} as="h2" className="truncate text-2xl" />
                <button type="button" onClick={copyLink} className="relative rounded-lg p-1.5 text-muted hover:bg-surface-2 hover:text-text" aria-label="Copy link to this icon">
                  <UiIcon name="link" size={18} />
                  <span role="status" className={cn("pointer-events-none absolute -top-7 left-1/2 -translate-x-1/2 whitespace-nowrap rounded-md bg-text px-2 py-0.5 text-xs text-bg transition-opacity", linkCopied ? "opacity-100" : "opacity-0")}>
                    {linkCopied ? "Link copied" : ""}
                  </span>
                </button>
              </div>
            </Dialog.Title>
            <div className="ml-auto flex items-center gap-1">
              {codepointHex && <span className="mr-2 font-mono text-xs text-muted" title="Unicode (private use)">{codepointHex}</span>}
              {/* Plain <a>: a full page load, so the route is not intercepted into the modal again. */}
              <a href={`/icons/${name}${style ? `?style=${style}` : ""}`} className="rounded-lg p-1.5 text-muted hover:bg-surface-2 hover:text-text" aria-label="Open the full icon page" title="Open full page">
                <UiIcon name="external-link" size={18} />
              </a>
              <Dialog.Close className="rounded-lg p-1.5 text-muted hover:bg-surface-2 hover:text-text" aria-label="Close" title="Close (Esc)">
                <UiIcon name="close" size={20} />
              </Dialog.Close>
            </div>
            <div className="w-full">{summary}</div>
          </header>
          <div className="min-h-0 flex-1 overflow-y-auto px-4 py-5 sm:px-6">{children}</div>
          {entries.length > 1 && idx >= 0 && (
            <footer className="flex items-center justify-between border-t border-border px-4 py-2 text-xs text-muted sm:px-6">
              <button type="button" disabled={!prev} onClick={() => go(prev)} className="rounded-md px-2 py-1 hover:bg-surface-2 disabled:opacity-40">← Prev</button>
              <span>{idx + 1} of {entries.length} on this page · arrow keys to browse</span>
              <button type="button" disabled={!next} onClick={() => go(next)} className="rounded-md px-2 py-1 hover:bg-surface-2 disabled:opacity-40">Next →</button>
            </footer>
          )}
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
