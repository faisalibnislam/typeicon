"use client";
import Link from "next/link";
import { useEffect, useMemo, useRef, useState } from "react";
import { cn } from "@/lib/cn";
import { bytes, STYLE_LABEL } from "@/lib/format";
import { IconSvgClient } from "../icon-svg-client";
import { useSelection } from "../selection/selection-provider";
import { UiIcon } from "../ui-icon";

const FORMATS = [
  { id: "otf", label: "OTF", note: "Desktop (Figma, Sketch, Office)" },
  { id: "ttf", label: "TTF", note: "Desktop, older apps" },
  { id: "woff2", label: "WOFF2", note: "Web" },
  { id: "woff", label: "WOFF", note: "Web, legacy browsers" },
  { id: "css", label: "CSS", note: "@font-face + classes" },
  { id: "svg", label: "SVG", note: "Individual files" },
] as const;

interface Review {
  items: { designId: string; name: string; style: string; sourceName: string; license: string; fontSupported: boolean }[];
  missing: { designId: string; style: string }[];
  families: { family: string; source: string; style: string; count: number }[];
  svgOnly: { name: string; style: string }[];
  licenses: { license: string; sources: string[] }[];
  limits: { maxIcons: number; buildsPerHour: number; plan: string };
}
interface Status {
  id: string;
  status: "queued" | "running" | "succeeded" | "failed";
  attempts: number;
  error: string | null;
  cached: boolean;
  download: { url: string; fileName: string; bytes: number; sha256: string } | null;
  manifest: { families: { family: string; style: string; glyphs: number }[]; svgOnly: { name: string }[] } | null;
}

export function SubsetBuilder() {
  const { items, remove, clear } = useSelection();
  const [name, setName] = useState("My project");
  const [formats, setFormats] = useState<string[]>(["otf", "woff2", "css", "svg"]);
  const [review, setReview] = useState<Review | null>(null);
  const [reviewError, setReviewError] = useState<string | null>(null);
  const [status, setStatus] = useState<Status | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const poll = useRef<ReturnType<typeof setTimeout> | null>(null);
  const payloadItems = useMemo(() => items.map((i) => ({ designId: i.designId, style: i.style })), [items]);

  useEffect(() => {
    if (!payloadItems.length) {
      setReview(null);
      return;
    }
    const ctl = new AbortController();
    fetch("/api/builds/review", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ items: payloadItems }), signal: ctl.signal })
      .then(async (r) => (r.ok ? setReview(await r.json()) : setReviewError(`Review failed (${r.status})`)))
      .catch((e) => e.name !== "AbortError" && setReviewError("Network error while reviewing the selection"));
    return () => ctl.abort();
  }, [payloadItems]);

  useEffect(() => () => {
    if (poll.current) clearTimeout(poll.current);
  }, []);

  async function track(id: string) {
    const r = await fetch(`/api/builds/${id}`);
    if (!r.ok) {
      setSubmitError(`Could not read build status (${r.status})`);
      return;
    }
    const s: Status = await r.json();
    setStatus(s);
    if (s.status === "queued" || s.status === "running") poll.current = setTimeout(() => track(id), 1500);
  }

  async function build() {
    setBusy(true);
    setSubmitError(null);
    setStatus(null);
    try {
      const r = await fetch("/api/builds", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ name, items: payloadItems, formats }) });
      const data = await r.json().catch(() => ({}));
      if (!r.ok) {
        setSubmitError(data.error ?? `Build request failed (${r.status})`);
        return;
      }
      await track(data.jobId);
    } finally {
      setBusy(false);
    }
  }

  if (!items.length) {
    return (
      <div className="rounded-2xl border border-dashed border-border-strong px-6 py-14 text-center">
        <p className="text-base font-medium text-text">Your selection is empty.</p>
        <p className="mx-auto mt-2 max-w-md text-sm text-muted">Browse icons and press + on the icons you want, in the style you want. The selection tray follows you across pages.</p>
        <Link href="/icons" className="mt-4 inline-block rounded-xl bg-accent px-4 py-2 text-sm font-semibold text-accent-contrast">Browse icons</Link>
      </div>
    );
  }
  const over = review ? items.length > review.limits.maxIcons : false;
  const inProgress = status && (status.status === "queued" || status.status === "running");

  return (
    <div className="grid grid-cols-[minmax(0,1fr)] gap-8 lg:grid-cols-[minmax(0,1fr)_380px]">
      <section aria-labelledby="sel-h" className="min-w-0">
        <div className="mb-3 flex items-center justify-between">
          <h2 id="sel-h" className="text-base font-semibold">1. Selected icons <span className="text-muted">({items.length})</span></h2>
          <button type="button" onClick={clear} className="text-sm text-muted hover:text-danger">Clear all</button>
        </div>
        <ul className="grid grid-cols-[repeat(auto-fill,minmax(150px,1fr))] gap-2">
          {items.map((i) => {
            const rv = review?.items.find((x) => x.designId === i.designId && x.style === i.style);
            return (
              <li key={`${i.designId}:${i.style}`} className="flex items-center gap-2 rounded-xl border border-border bg-surface p-2">
                <IconSvgClient svg={i.svg} size={24} className="shrink-0 text-text" />
                <div className="min-w-0 flex-1">
                  <p className="truncate text-xs font-medium text-text">{i.name}</p>
                  <p className="truncate text-[11px] text-muted">
                    {STYLE_LABEL[i.style]}
                    {rv && !rv.fontSupported && " · SVG only"}
                  </p>
                </div>
                <button type="button" onClick={() => remove(i.designId, i.style)} aria-label={`Remove ${i.name} ${i.style}`} className="rounded-md p-1 text-muted hover:bg-surface-2 hover:text-danger">
                  <UiIcon name="close" size={14} />
                </button>
              </li>
            );
          })}
        </ul>
      </section>

      <aside className="space-y-5">
        <section aria-labelledby="rev-h" className="rounded-2xl border border-border bg-surface p-4">
          <h2 id="rev-h" className="mb-2 text-base font-semibold">2. Review</h2>
          {reviewError && <p className="text-sm text-danger">{reviewError}</p>}
          {!review && !reviewError && <p className="text-sm text-muted">Checking compatibility…</p>}
          {review && (
            <div className="space-y-3 text-sm">
              {review.missing.length > 0 && <p className="text-danger">{review.missing.length} selected styles are no longer published and will be rejected. Remove them to continue.</p>}
              {over && <p className="text-danger">The {review.limits.plan} limit is {review.limits.maxIcons} icon styles per subset.</p>}
              <div>
                <p className="mb-1 font-medium text-text">Font families to be built</p>
                {review.families.length ? (
                  <ul className="space-y-1">
                    {review.families.map((f) => (
                      <li key={f.source + f.style} className="flex justify-between gap-2 text-text-2">
                        <span className="truncate">{f.family.replace("<name> <hash> ", "")}</span>
                        <span className="tabular-nums text-muted">{f.count}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-muted">None (SVG only)</p>
                )}
                <p className="mt-1 text-xs text-muted">One family per source and style; each name includes your project name and a build hash.</p>
              </div>
              {review.svgOnly.length > 0 && <p className="text-text-2">{review.svgOnly.length} icons are SVG-only and are delivered in the SVG folder, not in fonts.</p>}
              <div>
                <p className="mb-1 font-medium text-text">Licenses included</p>
                <ul className="space-y-1 text-text-2">
                  {review.licenses.map((l) => (
                    <li key={l.license}>
                      <Link href="/licenses" className="font-mono text-xs hover:text-accent">{l.license}</Link>: {l.sources.join(", ")}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </section>

        <section aria-labelledby="opt-h" className="rounded-2xl border border-border bg-surface p-4">
          <h2 id="opt-h" className="mb-3 text-base font-semibold">3. Name and formats</h2>
          <label htmlFor="proj" className="mb-1 block text-sm text-text-2">Project name</label>
          <input id="proj" value={name} maxLength={60} onChange={(e) => setName(e.target.value)} className="mb-4 h-10 w-full rounded-xl border border-border bg-bg px-3 text-sm" />
          <fieldset>
            <legend className="mb-2 text-sm text-text-2">Formats</legend>
            <div className="grid grid-cols-2 gap-2">
              {FORMATS.map((f) => {
                const on = formats.includes(f.id);
                return (
                  <label key={f.id} className={cn("flex cursor-pointer items-start gap-2 rounded-xl border p-2.5", on ? "border-accent bg-accent-soft/40" : "border-border")}>
                    <input type="checkbox" checked={on} onChange={() => setFormats((cur) => (on ? cur.filter((x) => x !== f.id) : [...cur, f.id]))} className="mt-0.5 accent-[var(--accent)]" />
                    <span>
                      <span className="block text-sm font-medium text-text">{f.label}</span>
                      <span className="block text-[11px] text-muted">{f.note}</span>
                    </span>
                  </label>
                );
              })}
            </div>
          </fieldset>
          <button
            type="button"
            onClick={build}
            disabled={busy || !!inProgress || !name.trim() || !formats.length || !review || review.missing.length > 0 || over}
            className="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-xl bg-accent px-4 py-2.5 text-sm font-semibold text-accent-contrast hover:bg-accent-hover disabled:opacity-50"
          >
            <UiIcon name="download" size={16} /> {busy ? "Submitting…" : "Build subset"}
          </button>
          {submitError && <p className="mt-2 text-sm text-danger" role="alert">{submitError}</p>}
        </section>

        {status && (
          <section aria-labelledby="st-h" className="rounded-2xl border border-border bg-surface p-4" aria-live="polite">
            <h2 id="st-h" className="mb-2 text-base font-semibold">4. Build</h2>
            <ol className="mb-3 flex items-center gap-2 text-xs">
              {(["queued", "running", "succeeded"] as const).map((s, idx) => {
                const order = { queued: 0, running: 1, succeeded: 2, failed: 2 }[status.status];
                const done = idx < order || status.status === "succeeded";
                const active = (idx === order && status.status !== "succeeded") || (status.status === "succeeded" && s === "succeeded");
                return (
                  <li key={s} className={cn("rounded-full px-2.5 py-1 capitalize", active ? "bg-text text-bg" : done ? "bg-surface-3 text-text" : "bg-surface-2 text-muted")}>
                    {s}
                  </li>
                );
              })}
              {status.status === "failed" && <li className="rounded-full bg-danger px-2.5 py-1 text-white">failed</li>}
            </ol>
            {inProgress && <p className="text-sm text-text-2">Building in the background worker{status.attempts > 1 ? ` (attempt ${status.attempts})` : ""}…</p>}
            {status.status === "failed" && <p className="text-sm text-danger">Build failed: {status.error?.split("\n")[0] ?? "unknown error"}. Retries are automatic for temporary errors.</p>}
            {status.status === "succeeded" && status.download && (
              <div className="space-y-3 text-sm">
                <a href={status.download.url} className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-text px-4 py-2.5 font-semibold text-bg hover:opacity-90">
                  <UiIcon name="download" size={16} /> Download {status.download.fileName} ({bytes(status.download.bytes)})
                </a>
                {status.cached && <p className="text-xs text-muted">An identical build already existed, so it was reused.</p>}
                <p className="break-all font-mono text-[11px] text-muted">sha256 {status.download.sha256}</p>
                {status.manifest && status.manifest.families.length > 0 && (
                  <div>
                    <p className="mb-1 font-medium text-text">Installed family names</p>
                    <ul className="space-y-1 text-text-2">
                      {status.manifest.families.map((f) => (
                        <li key={f.family} className="font-mono text-xs">{f.family}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </section>
        )}
      </aside>
    </div>
  );
}
