"use client";
import * as Dialog from "@radix-ui/react-dialog";
import { usePathname, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { UiIcon } from "../ui-icon";

/** Bottom sheet wrapper for the filter panel on small screens. Closes when the URL changes. */
export function MobileFilters({ activeCount, children }: { activeCount: number; children: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  const pathname = usePathname();
  const params = useSearchParams();
  useEffect(() => setOpen(false), [pathname, params]);
  return (
    <Dialog.Root open={open} onOpenChange={setOpen}>
      <Dialog.Trigger className="inline-flex h-9 items-center gap-2 rounded-lg border border-border bg-surface px-3 text-sm font-medium text-text-2 hover:border-border-strong lg:hidden">
        <UiIcon name="filter" size={16} />
        Filters{activeCount > 0 && <span className="rounded-full bg-accent px-1.5 text-xs text-accent-contrast">{activeCount}</span>}
      </Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 z-50 bg-black/40" />
        <Dialog.Content className="fixed inset-x-0 bottom-0 z-50 max-h-[85dvh] overflow-y-auto rounded-t-2xl border-t border-border bg-surface p-5 pb-8 shadow-2xl">
          <div className="mb-4 flex items-center justify-between">
            <Dialog.Title className="text-base font-semibold">Filters</Dialog.Title>
            <Dialog.Close className="inline-flex h-9 w-9 items-center justify-center rounded-lg hover:bg-surface-2" aria-label="Close filters">
              <UiIcon name="close" size={18} />
            </Dialog.Close>
          </div>
          <Dialog.Description className="sr-only">Filter icons by catalog area, pack, category, license and brand.</Dialog.Description>
          {children}
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
