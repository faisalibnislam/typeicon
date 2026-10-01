"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";

/** Small admin action: sends JSON to an admin API and refreshes the page. */
export function ActionButton({ url, method = "POST", body, label, confirmText, variant = "default" }: { url: string; method?: string; body?: unknown; label: string; confirmText?: string; variant?: "default" | "danger" | "primary" }) {
  const router = useRouter();
  const [state, setState] = useState<string | null>(null);
  const cls = variant === "danger" ? "border-danger text-danger" : variant === "primary" ? "border-accent bg-accent text-accent-contrast" : "border-border text-text-2";
  return (
    <span className="inline-flex items-center gap-2">
      <button
        type="button"
        className={`rounded-lg border px-2.5 py-1 text-xs font-medium hover:opacity-80 ${cls}`}
        onClick={async () => {
          if (confirmText && !confirm(confirmText)) return;
          setState("…");
          const r = await fetch(url, { method, headers: { "content-type": "application/json" }, body: body ? JSON.stringify(body) : undefined });
          const d = await r.json().catch(() => ({}));
          setState(r.ok ? "done" : d.error ?? `error ${r.status}`);
          if (r.ok) router.refresh();
        }}
      >
        {label}
      </button>
      {state && <span role="status" className="text-xs text-muted">{state}</span>}
    </span>
  );
}
