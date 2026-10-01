"use client";
import Link from "next/link";
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import { signOut, useSession } from "@/lib/auth-client";
import { UiIcon } from "./ui-icon";

export function AccountMenu() {
  const { data, isPending } = useSession();
  if (isPending) return <span className="h-9 w-9" aria-hidden="true" />;
  if (!data) {
    return (
      <Link href="/sign-in" className="inline-flex h-9 items-center rounded-lg px-3 text-sm font-medium text-text-2 hover:bg-surface-2 hover:text-text">
        Sign in
      </Link>
    );
  }
  const role = (data.user as { role?: string }).role;
  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger className="inline-flex h-9 items-center gap-2 rounded-lg px-2 text-sm text-text-2 hover:bg-surface-2" aria-label="Account menu">
        <UiIcon name="user" size={18} />
        <span className="hidden max-w-32 truncate md:inline">{data.user.name || data.user.email}</span>
      </DropdownMenu.Trigger>
      <DropdownMenu.Portal>
        <DropdownMenu.Content align="end" sideOffset={6} className="z-50 min-w-48 rounded-xl border border-border bg-surface p-1 shadow-lg">
          {[
            ["/account", "Account"],
            ["/collections", "Collections"],
            ["/kits", "Kits"],
            ...(role === "admin" ? [["/admin", "Admin"]] : []),
          ].map(([href, label]) => (
            <DropdownMenu.Item key={href} asChild>
              <Link href={href} className="block rounded-lg px-3 py-2 text-sm text-text-2 outline-none data-[highlighted]:bg-surface-2 data-[highlighted]:text-text">
                {label}
              </Link>
            </DropdownMenu.Item>
          ))}
          <DropdownMenu.Separator className="my-1 h-px bg-border" />
          <DropdownMenu.Item
            onSelect={() => signOut().then(() => (window.location.href = "/"))}
            className="cursor-pointer rounded-lg px-3 py-2 text-sm text-text-2 outline-none data-[highlighted]:bg-surface-2"
          >
            Sign out
          </DropdownMenu.Item>
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
}
