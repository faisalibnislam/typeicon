"use client";
import Link from "next/link";
import * as Dialog from "@radix-ui/react-dialog";
import { useState } from "react";
import { UiIcon } from "./ui-icon";

const LINKS = [
  ["/icons", "Icons"],
  ["/downloads", "Downloads"],
  ["/docs", "Docs"],
  ["/icons?style=brand", "Brands"],
  ["/packs", "Sources"],
  ["/categories", "Categories"],
  ["/licenses", "Licenses"],
  ["/changelog", "Changelog"],
];

export function MobileNav() {
  const [open, setOpen] = useState(false);
  return (
    <Dialog.Root open={open} onOpenChange={setOpen}>
      <Dialog.Trigger className="inline-flex h-9 w-9 items-center justify-center rounded-lg text-text-2 hover:bg-surface-2 lg:hidden" aria-label="Open menu">
        <UiIcon name="menu" size={20} />
      </Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 z-50 bg-black/40" />
        <Dialog.Content className="fixed inset-y-0 left-0 z-50 w-72 border-r border-border bg-surface p-4 shadow-xl">
          <div className="mb-4 flex items-center justify-between">
            <Dialog.Title className="text-sm font-semibold text-text">Menu</Dialog.Title>
            <Dialog.Close className="inline-flex h-9 w-9 items-center justify-center rounded-lg hover:bg-surface-2" aria-label="Close menu">
              <UiIcon name="close" size={18} />
            </Dialog.Close>
          </div>
          <nav aria-label="Mobile">
            <ul className="space-y-1">
              {LINKS.map(([href, label]) => (
                <li key={href}>
                  <Link href={href} onClick={() => setOpen(false)} className="block rounded-lg px-3 py-2 text-[15px] text-text-2 hover:bg-surface-2 hover:text-text">
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
