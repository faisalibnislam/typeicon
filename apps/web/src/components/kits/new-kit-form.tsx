"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";

export function NewKitForm({ disabled, limit }: { disabled: boolean; limit: number }) {
  const router = useRouter();
  const [name, setName] = useState("");
  const [err, setErr] = useState<string | null>(null);
  return (
    <form
      className="flex flex-wrap items-center gap-2"
      onSubmit={async (e) => {
        e.preventDefault();
        setErr(null);
        const r = await fetch("/api/kits", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ name }) });
        const d = await r.json().catch(() => ({}));
        if (r.ok) router.push(`/kits/${d.id}`);
        else setErr(d.error ?? `Could not create kit (${r.status})`);
      }}
    >
      <label htmlFor="kit-name" className="sr-only">Kit name</label>
      <input id="kit-name" value={name} onChange={(e) => setName(e.target.value)} maxLength={60} placeholder="New kit name" className="h-10 min-w-0 flex-1 rounded-xl border border-border bg-surface px-3 text-sm" />
      <button type="submit" disabled={disabled || !name.trim()} className="h-10 rounded-xl bg-accent px-4 text-sm font-semibold text-accent-contrast disabled:opacity-50">Create kit</button>
      {disabled && <p className="w-full text-xs text-muted">Your plan allows {limit} kits.</p>}
      {err && <p role="alert" className="w-full text-sm text-danger">{err}</p>}
    </form>
  );
}
