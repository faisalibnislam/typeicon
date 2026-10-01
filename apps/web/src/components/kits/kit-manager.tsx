"use client";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import type { KitDetail } from "@/lib/kits";
import { bytes, STYLE_LABEL } from "@/lib/format";
import { IconSvgClient } from "../icon-svg-client";
import { useSelection } from "../selection/selection-provider";

const FORMATS = ["otf", "ttf", "woff2", "woff", "css", "svg"];

export function KitManager({ kit, caps, site }: { kit: KitDetail; caps: { customIcons: number; hostedKits: boolean; plan: string }; site: string }) {
  const router = useRouter();
  const { items } = useSelection();
  const [formats, setFormats] = useState(["otf", "woff2", "css", "svg"]);
  const [customSel, setCustomSel] = useState<string[]>(kit.customIcons.filter((c) => c.status === "ready").map((c) => c.id));
  const [msg, setMsg] = useState<{ ok: boolean; text: string } | null>(null);
  const [uploadName, setUploadName] = useState("");
  const [uploadStyle, setUploadStyle] = useState("line");
  const [domains, setDomains] = useState(kit.allowedDomains.join(", "));
  const pending = kit.customIcons.some((c) => c.status === "pending") || kit.versions.some((v) => v.job && ["queued", "running"].includes(v.job.status));

  useEffect(() => {
    if (!pending) return;
    const t = setInterval(() => router.refresh(), 2000);
    return () => clearInterval(t);
  }, [pending, router]);

  async function upload(file: File) {
    if (file.size > 65536) return setMsg({ ok: false, text: "SVG files must be 64 KB or smaller." });
    const svg = await file.text();
    const r = await fetch(`/api/kits/${kit.id}/icons`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ name: uploadName, style: uploadStyle, svg }) });
    const d = await r.json().catch(() => ({}));
    setMsg({ ok: r.ok, text: r.ok ? `Uploaded "${uploadName}". Checking it now.` : d.error ?? d.issues?.[0]?.message ?? `Upload failed (${r.status})` });
    if (r.ok) {
      setUploadName("");
      router.refresh();
    }
  }

  async function saveVersion() {
    const r = await fetch(`/api/kits/${kit.id}/versions`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ items: items.map((i) => ({ designId: i.designId, style: i.style })), customIconIds: customSel, formats }),
    });
    const d = await r.json().catch(() => ({}));
    setMsg({ ok: r.ok, text: r.ok ? `Saved version v${d.version}; building now` : d.error ?? `Could not save (${r.status})` });
    if (r.ok) router.refresh();
  }

  return (
    <div className="mt-8 space-y-8">
      {msg && <p role="status" className={msg.ok ? "text-sm text-success" : "text-sm text-danger"}>{msg.text}</p>}

      <section className="rounded-2xl border border-border bg-surface p-5">
        <h2 className="font-semibold">1. Catalog icons</h2>
        <p className="mt-1 text-sm text-text-2">The next version uses your current selection tray: <strong>{items.length}</strong> icon styles. Change the selection from any icon page.</p>
        <div className="mt-3 flex flex-wrap gap-1.5 text-text">
          {items.slice(0, 60).map((i) => <span key={i.designId + i.style} title={`${i.name} (${i.style})`} className="rounded-lg border border-border p-1.5"><IconSvgClient svg={i.svg} size={18} /></span>)}
        </div>
      </section>

      <section className="rounded-2xl border border-border bg-surface p-5">
        <h2 className="font-semibold">2. Private custom icons</h2>
        <p className="mt-1 text-sm text-text-2">
          Custom SVGs stay private to this kit. Each upload is sanitized (scripts, event handlers, external links and foreignObject removed; DTDs refused), checked for outline compatibility and name collisions, then marked ready or rejected.
        </p>
        {caps.customIcons > 0 ? (
          <form className="mt-3 flex flex-wrap items-end gap-2" onSubmit={(e) => { e.preventDefault(); const f = (e.currentTarget.elements.namedItem("file") as HTMLInputElement).files?.[0]; if (f) upload(f); }}>
            <label className="text-sm">
              <span className="mb-1 block text-text-2">Keyword name</span>
              <input value={uploadName} onChange={(e) => setUploadName(e.target.value.toLowerCase())} pattern="[a-z0-9]+(-[a-z0-9]+)*" minLength={2} maxLength={48} required className="h-9 rounded-lg border border-border bg-bg px-2" />
            </label>
            <label className="text-sm">
              <span className="mb-1 block text-text-2">Style</span>
              <select value={uploadStyle} onChange={(e) => setUploadStyle(e.target.value)} className="h-9 rounded-lg border border-border bg-bg px-2">
                {Object.entries(STYLE_LABEL).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
              </select>
            </label>
            <label className="text-sm">
              <span className="mb-1 block text-text-2">SVG file (max 64 KB)</span>
              <input name="file" type="file" accept=".svg,image/svg+xml" required className="text-sm" />
            </label>
            <button type="submit" className="h-9 rounded-lg bg-text px-3 text-sm font-medium text-bg">Upload</button>
          </form>
        ) : (
          <p className="mt-3 text-sm text-muted">Custom icons are not included in the {caps.plan} plan.</p>
        )}
        <ul className="mt-4 grid gap-2 sm:grid-cols-2">
          {kit.customIcons.map((c) => (
            <li key={c.id} className="flex items-center gap-3 rounded-xl border border-border p-2.5">
              {c.status === "ready" && (
                <input type="checkbox" aria-label={`Include ${c.name} in the next version`} checked={customSel.includes(c.id)} onChange={() => setCustomSel((s) => (s.includes(c.id) ? s.filter((x) => x !== c.id) : [...s, c.id]))} />
              )}
              <span className="text-text">{c.status === "ready" ? <IconSvgClient svg={c.svg} size={24} /> : <span className="inline-block h-6 w-6 rounded border border-dashed border-border-strong" />}</span>
              <span className="min-w-0 flex-1">
                <span className="block truncate font-mono text-sm">{c.name}</span>
                <span className="block text-xs text-muted">{STYLE_LABEL[c.style]} · U+{c.codepoint.toString(16).toUpperCase()} · {c.status}{c.route === "svg-only" ? " (SVG only)" : ""}</span>
                {c.reasons.length > 0 && <span className="block truncate text-[11px] text-muted" title={c.reasons.join("; ")}>{c.reasons.join("; ")}</span>}
              </span>
            </li>
          ))}
        </ul>
      </section>

      <section className="rounded-2xl border border-border bg-surface p-5">
        <h2 className="font-semibold">3. Save a version and build</h2>
        <p className="mt-1 text-sm text-text-2">Versions are immutable. Each build is private to you; cached files are never shared with other accounts.</p>
        <div className="mt-3 flex flex-wrap gap-2">
          {FORMATS.map((f) => (
            <label key={f} className="flex items-center gap-1.5 rounded-lg border border-border px-2.5 py-1.5 text-sm">
              <input type="checkbox" checked={formats.includes(f)} onChange={() => setFormats((s) => (s.includes(f) ? s.filter((x) => x !== f) : [...s, f]))} /> {f.toUpperCase()}
            </label>
          ))}
        </div>
        <button type="button" onClick={saveVersion} disabled={!formats.length || items.length + customSel.length === 0} className="mt-4 rounded-xl bg-accent px-4 py-2 text-sm font-semibold text-accent-contrast disabled:opacity-50">
          Save v{kit.currentVersion + 1} and build
        </button>
        <ul className="mt-5 divide-y divide-border rounded-xl border border-border">
          {kit.versions.map((v) => (
            <li key={v.version} className="flex flex-wrap items-center justify-between gap-2 px-3 py-2.5 text-sm">
              <span>
                <strong>v{v.version}</strong> <span className="text-muted">· {v.items} catalog + {v.customIcons} custom · {v.formats.join(", ")}</span>
              </span>
              {v.job?.status === "succeeded" && v.job.storageKey ? (
                <a href={`/api/files/${v.job.storageKey}`} className="text-accent hover:underline">Download {v.job.bytes ? bytes(v.job.bytes) : ""}</a>
              ) : (
                <span className={v.job?.status === "failed" ? "text-danger" : "text-muted"} title={v.job?.error ?? undefined}>{v.job?.status ?? "not built"}</span>
              )}
            </li>
          ))}
          {!kit.versions.length && <li className="px-3 py-3 text-sm text-muted">No versions yet.</li>}
        </ul>
      </section>

      <section className="rounded-2xl border border-border bg-surface p-5">
        <h2 className="font-semibold">4. Hosted CSS embed</h2>
        {caps.hostedKits ? (
          <>
            <p className="mt-1 text-sm text-text-2">Add this to your site. It always serves the latest successfully built version.</p>
            <pre className="mt-2 overflow-x-auto rounded-lg bg-surface-2 p-3 text-xs"><code>{`<link rel="stylesheet" href="${site}/api/kits/embed/${kit.embedId}/latest/kit.css">`}</code></pre>
            <form
              className="mt-3 flex flex-wrap items-end gap-2"
              onSubmit={async (e) => {
                e.preventDefault();
                const list = domains.split(",").map((d) => d.trim()).filter(Boolean);
                const r = await fetch(`/api/kits/${kit.id}`, { method: "PATCH", headers: { "content-type": "application/json" }, body: JSON.stringify({ allowedDomains: list }) });
                setMsg({ ok: r.ok, text: r.ok ? "Allowed domains saved" : "Invalid domain list" });
              }}
            >
              <label className="min-w-64 flex-1 text-sm">
                <span className="mb-1 block text-text-2">Allowed domains (comma-separated, optional)</span>
                <input value={domains} onChange={(e) => setDomains(e.target.value)} placeholder="example.com, *.example.com" className="h-9 w-full rounded-lg border border-border bg-bg px-2" />
              </label>
              <button className="h-9 rounded-lg border border-border px-3 text-sm">Save</button>
            </form>
            <p className="mt-2 text-xs text-muted">Domain restrictions are a usage control. Font files delivered to browsers are public, so anyone with the file URLs can still download them.</p>
          </>
        ) : (
          <p className="mt-1 text-sm text-muted">Hosted embeds are not included in the {caps.plan} plan. Download a version and self-host the CSS and fonts instead.</p>
        )}
      </section>
    </div>
  );
}
