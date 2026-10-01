"use client";
import { useState } from "react";
import { bytes } from "@/lib/format";

/** One-click category pack. Identical packs are reused from the build cache. */
export function CategoryPack({ category, packs }: { category: string; packs: { value: string; label: string; count: number }[] }) {
  const [pack, setPack] = useState(packs[0]?.value ?? "");
  const [style, setStyle] = useState("line");
  const [state, setState] = useState<{ text: string; url?: string } | null>(null);
  async function run() {
    setState({ text: "Queued…" });
    const r = await fetch("/api/builds/category", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ category, pack, style, formats: ["otf", "woff2", "css", "svg"] }) });
    const d = await r.json().catch(() => ({}));
    if (!r.ok) return setState({ text: d.error ?? `Failed (${r.status})` });
    const poll = async () => {
      const s = await (await fetch(`/api/builds/${d.jobId}`)).json();
      if (s.status === "succeeded" && s.download) setState({ text: `Ready · ${bytes(s.download.bytes)}`, url: s.download.url });
      else if (s.status === "failed") setState({ text: `Failed: ${s.error?.split("\n")[0]}` });
      else {
        setState({ text: s.status === "running" ? "Building…" : "Queued…" });
        setTimeout(poll, 1500);
      }
    };
    poll();
  }
  if (!packs.length) return null;
  return (
    <div className="flex flex-wrap items-center gap-2 rounded-xl border border-border bg-surface p-3 text-sm">
      <span className="font-medium">Category pack</span>
      <label className="sr-only" htmlFor="cp-pack">Pack</label>
      <select id="cp-pack" value={pack} onChange={(e) => setPack(e.target.value)} className="h-8 rounded-lg border border-border bg-bg px-2">
        {packs.map((p) => <option key={p.value} value={p.value}>{p.label} ({p.count})</option>)}
      </select>
      <label className="sr-only" htmlFor="cp-style">Style</label>
      <select id="cp-style" value={style} onChange={(e) => setStyle(e.target.value)} className="h-8 rounded-lg border border-border bg-bg px-2">
        <option value="filled">Filled</option><option value="line">Line</option><option value="rounded">Rounded</option><option value="thin">Thin</option>
      </select>
      <button type="button" onClick={run} className="h-8 rounded-lg bg-accent px-3 font-semibold text-accent-contrast">Build fonts + SVG</button>
      {state && (state.url ? <a href={state.url} className="font-medium text-accent underline underline-offset-2">Download · {state.text}</a> : <span role="status" className="text-muted">{state.text}</span>)}
    </div>
  );
}
