"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { type SelectedIcon, useSelection } from "../selection/selection-provider";

export function CollectionActions({ id, items }: { id: string; items: SelectedIcon[] }) {
  const { add } = useSelection();
  const router = useRouter();
  const [msg, setMsg] = useState("");
  return (
    <div className="flex items-center gap-2">
      <button type="button" onClick={() => { add(items); setMsg(`Added ${items.length} icons to your selection`); }} className="rounded-xl border border-border bg-surface px-3 py-2 text-sm font-medium hover:bg-surface-2">
        Add all to subset
      </button>
      <button
        type="button"
        onClick={async () => {
          if (!confirm("Delete this collection? This cannot be undone.")) return;
          const r = await fetch(`/api/collections/${id}`, { method: "DELETE" });
          if (r.ok) router.push("/collections");
          else setMsg("Could not delete the collection");
        }}
        className="rounded-xl px-3 py-2 text-sm text-danger hover:bg-surface-2"
      >
        Delete
      </button>
      <span role="status" className="text-sm text-muted">{msg}</span>
    </div>
  );
}
