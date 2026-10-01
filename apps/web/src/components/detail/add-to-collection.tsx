"use client";
import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import * as Popover from "@radix-ui/react-popover";
import { useState } from "react";
import { useSession } from "@/lib/auth-client";
import { UiIcon } from "../ui-icon";

interface Col { id: string; name: string; items: number }

export function AddToCollection({ designId, style, disabled, onDone }: { designId: string; style: string; disabled?: boolean; onDone: (kind: "ok" | "error", text: string) => void }) {
  const { data: session } = useSession();
  const pathname = usePathname();
  const params = useSearchParams();
  const [cols, setCols] = useState<Col[] | null>(null);
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);

  async function load() {
    const r = await fetch("/api/collections");
    if (r.ok) setCols((await r.json()).collections);
    else setCols([]);
  }
  async function addTo(id: string, label: string) {
    setBusy(true);
    const r = await fetch(`/api/collections/${id}/items`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ designId, style }) });
    setBusy(false);
    onDone(r.ok ? "ok" : "error", r.ok ? `Saved to "${label}"` : `Could not save: ${(await r.json().catch(() => ({}))).error ?? r.status}`);
  }
  async function create() {
    if (!name.trim()) return;
    setBusy(true);
    const r = await fetch("/api/collections", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ name: name.trim(), items: [{ designId, style }] }) });
    setBusy(false);
    if (r.ok) {
      onDone("ok", `Created "${name.trim()}" with this icon`);
      setName("");
      load();
    } else onDone("error", `Could not create collection (${r.status})`);
  }

  const trigger = (
    <span className="inline-flex items-center gap-2 rounded-xl border border-border bg-surface px-3 py-2.5 text-sm font-medium text-text hover:bg-surface-2">
      <UiIcon name="bookmark" size={16} /> Save
    </span>
  );
  if (!session) {
    return (
      <Link href={`/sign-in?next=${encodeURIComponent(pathname + (params.toString() ? `?${params}` : ""))}`} aria-label="Sign in to save to a collection">
        {trigger}
      </Link>
    );
  }
  return (
    <Popover.Root onOpenChange={(o) => o && load()}>
      <Popover.Trigger disabled={disabled} aria-label="Save to collection">{trigger}</Popover.Trigger>
      <Popover.Portal>
        <Popover.Content align="start" sideOffset={6} className="z-50 w-72 rounded-xl border border-border bg-surface p-3 shadow-lg">
          <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted">Save to collection</p>
          {cols === null ? (
            <p className="text-sm text-muted">Loading…</p>
          ) : (
            <ul className="mb-3 max-h-48 space-y-1 overflow-y-auto">
              {cols.map((c) => (
                <li key={c.id}>
                  <button type="button" disabled={busy} onClick={() => addTo(c.id, c.name)} className="flex w-full items-center justify-between rounded-lg px-2 py-1.5 text-left text-sm hover:bg-surface-2">
                    <span className="truncate">{c.name}</span>
                    <span className="text-xs text-muted">{c.items}</span>
                  </button>
                </li>
              ))}
              {!cols.length && <li className="text-sm text-muted">No collections yet.</li>}
            </ul>
          )}
          <form onSubmit={(e) => { e.preventDefault(); create(); }} className="flex gap-2">
            <label htmlFor="new-col" className="sr-only">New collection name</label>
            <input id="new-col" value={name} maxLength={80} onChange={(e) => setName(e.target.value)} placeholder="New collection" className="h-8 min-w-0 flex-1 rounded-lg border border-border bg-bg px-2 text-sm" />
            <button type="submit" disabled={busy || !name.trim()} className="rounded-lg bg-accent px-3 text-sm font-medium text-accent-contrast disabled:opacity-50">Create</button>
          </form>
        </Popover.Content>
      </Popover.Portal>
    </Popover.Root>
  );
}
