"use client";
import { useState } from "react";

export function ReleaseBuildForm() {
  const [version, setVersion] = useState("");
  const [date, setDate] = useState(new Date().toISOString().slice(0, 10));
  const [msg, setMsg] = useState<string | null>(null);
  return (
    <form
      className="flex flex-wrap items-end gap-2 rounded-2xl border border-dashed border-border-strong p-4"
      onSubmit={async (e) => {
        e.preventDefault();
        const r = await fetch("/api/admin/releases", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ action: "build", version, date }) });
        const d = await r.json().catch(() => ({}));
        setMsg(r.ok ? `Queued release build (job ${d.jobId}). The worker compiles and validates every family; a failed validation stops the release.` : d.error ?? d.issues?.[0]?.message ?? `Error ${r.status}`);
      }}
    >
      <label className="text-sm"><span className="mb-1 block text-text-2">Version</span><input value={version} onChange={(e) => setVersion(e.target.value)} placeholder="0.2.0" className="h-9 rounded-lg border border-border bg-bg px-2" /></label>
      <label className="text-sm"><span className="mb-1 block text-text-2">Release date</span><input type="date" value={date} onChange={(e) => setDate(e.target.value)} className="h-9 rounded-lg border border-border bg-bg px-2" /></label>
      <button className="h-9 rounded-lg bg-accent px-3 text-sm font-semibold text-accent-contrast">Build release</button>
      {msg && <p role="status" className="w-full text-sm text-text-2">{msg}</p>}
    </form>
  );
}
