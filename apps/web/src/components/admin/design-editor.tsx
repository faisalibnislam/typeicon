"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";

export function DesignEditor({ name, initial }: { name: string; initial: { description: string; tags: string[]; categories: string[]; aliases: string[]; status: string } }) {
  const router = useRouter();
  const [f, setF] = useState({ ...initial, tags: initial.tags.join(", "), categories: initial.categories.join(", "), aliases: initial.aliases.join(", ") });
  const [msg, setMsg] = useState<string | null>(null);
  const list = (s: string) => s.split(",").map((x) => x.trim()).filter(Boolean);
  return (
    <form
      className="max-w-2xl space-y-3 rounded-2xl border border-border bg-surface p-4"
      onSubmit={async (e) => {
        e.preventDefault();
        const r = await fetch(`/api/admin/designs/${name}`, {
          method: "PATCH",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ description: f.description, tags: list(f.tags), categories: list(f.categories), aliases: list(f.aliases), status: f.status }),
        });
        const d = await r.json().catch(() => ({}));
        setMsg(r.ok ? "Saved. Alias changes reach fonts in the next release build." : d.error ?? d.issues?.[0]?.message ?? `Error ${r.status}`);
        if (r.ok) router.refresh();
      }}
    >
      <h2 className="font-semibold">Metadata</h2>
      {(["description", "tags", "categories", "aliases"] as const).map((k) => (
        <label key={k} className="block text-sm">
          <span className="mb-1 block capitalize text-text-2">{k}{k !== "description" && " (comma-separated)"}</span>
          <input value={f[k]} onChange={(e) => setF({ ...f, [k]: e.target.value })} className="h-9 w-full rounded-lg border border-border bg-bg px-2" />
        </label>
      ))}
      <label className="block text-sm">
        <span className="mb-1 block text-text-2">Status</span>
        <select value={f.status} onChange={(e) => setF({ ...f, status: e.target.value })} className="h-9 rounded-lg border border-border bg-bg px-2">
          <option>published</option><option>pending</option><option>deprecated</option>
        </select>
      </label>
      <p className="text-xs text-muted">Aliases are checked against the global name registry. Names are never changed: to rename, deprecate and add the old name as an alias of the new icon.</p>
      <button className="rounded-lg bg-accent px-3 py-1.5 text-sm font-semibold text-accent-contrast">Save</button>
      {msg && <p role="status" className="text-sm text-text-2">{msg}</p>}
    </form>
  );
}
