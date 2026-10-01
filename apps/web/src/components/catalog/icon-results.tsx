"use client";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";
import type { IconCard } from "@/lib/search-params";
import { fmt, hex, STYLE_LABEL } from "@/lib/format";
import { cn } from "@/lib/cn";
import { IconSvgClient } from "../icon-svg-client";
import { useSelection } from "../selection/selection-provider";
import { UiIcon } from "../ui-icon";
import { usePreviewPrefs } from "./preview-prefs";
import { RegisterResults } from "./register-results";

type View = "grid" | "list" | "cheatsheet";

export function IconResults({ items, requestedStyle }: { items: IconCard[]; requestedStyle: string }) {
  const params = useSearchParams();
  const router = useRouter();
  const view = (["grid", "list", "cheatsheet"].includes(params.get("view") ?? "") ? params.get("view") : "grid") as View;
  const [prefs, setPrefs] = usePreviewPrefs();
  const selection = useSelection();
  const [announce, setAnnounce] = useState("");

  const setView = (v: View) => {
    const next = new URLSearchParams(params.toString());
    if (v === "grid") next.delete("view");
    else next.set("view", v);
    router.replace(`/icons${next.toString() ? `?${next}` : ""}`, { scroll: false });
  };
  const toggle = (i: IconCard) => {
    if (!i.displayStyle) return;
    const on = selection.has(i.id, i.displayStyle);
    selection.toggle({ designId: i.id, name: i.name, style: i.displayStyle, source: i.source, svg: i.svg });
    setAnnounce(`${on ? "Removed" : "Added"} ${i.name} ${i.displayStyle} ${on ? "from" : "to"} selection`);
  };
  const colorStyle = prefs.color ? { color: prefs.color } : undefined;

  return (
    <div>
      <div className="mb-3 flex flex-wrap items-center gap-x-4 gap-y-2">
        <div role="group" aria-label="View" className="inline-flex rounded-lg border border-border bg-surface p-0.5">
          {(["grid", "list", "cheatsheet"] as View[]).map((v) => (
            <button
              key={v}
              type="button"
              onClick={() => setView(v)}
              aria-pressed={view === v}
              className={cn("rounded-md px-2.5 py-1 text-xs font-medium capitalize", view === v ? "bg-surface-3 text-text" : "text-muted hover:text-text")}
            >
              {v}
            </button>
          ))}
        </div>
        <label className="flex items-center gap-2 text-xs text-muted">
          Size
          <input
            type="range"
            min={16}
            max={64}
            step={4}
            value={prefs.size}
            onChange={(e) => setPrefs({ size: Number(e.target.value) })}
            className="w-24 accent-[var(--accent)]"
            aria-valuetext={`${prefs.size} pixels`}
          />
          <span className="w-9 tabular-nums text-text-2">{prefs.size}px</span>
        </label>
        <div className="flex items-center gap-2 text-xs text-muted">
          <label htmlFor="preview-color">Color</label>
          <input
            id="preview-color"
            type="color"
            value={prefs.color ?? "#16161a"}
            onChange={(e) => setPrefs({ color: e.target.value })}
            className="h-7 w-8 cursor-pointer rounded border border-border bg-surface p-0.5"
          />
          {prefs.color && (
            <button type="button" onClick={() => setPrefs({ color: null })} className="text-xs text-accent hover:underline">
              Reset
            </button>
          )}
        </div>
        <span className="text-xs text-muted">Preview settings only change how results are displayed.</span>
      </div>
      <p className="sr-only" aria-live="polite">{announce}</p>
      <RegisterResults entries={items.map((i) => ({ name: i.name, style: i.displayStyle }))} />

      {view === "grid" && (
        <ul className="grid grid-cols-[repeat(auto-fill,minmax(112px,1fr))] gap-2" aria-label="Icons">
          {items.map((i) => {
            const selected = !!i.displayStyle && selection.has(i.id, i.displayStyle);
            const href = `/icons/${i.name}${i.displayStyle ? `?style=${i.displayStyle}` : ""}`;
            return (
              <li key={i.id} className="group relative">
                <Link
                  href={href}
                  className={cn(
                    "flex h-[124px] flex-col items-center justify-center gap-2 rounded-xl border bg-surface px-2 pt-2 text-center transition-colors",
                    i.displayStyle ? "border-border hover:border-border-strong hover:bg-surface-2" : "border-dashed border-border-strong bg-transparent",
                    selected && "border-accent ring-1 ring-accent",
                  )}
                >
                  <span className="flex flex-1 items-center justify-center text-text" style={colorStyle}>
                    {i.displayStyle ? (
                      <IconSvgClient svg={i.svg} size={prefs.size} />
                    ) : (
                      <span className="px-1 text-[11px] leading-tight text-muted">No {STYLE_LABEL[requestedStyle]} style</span>
                    )}
                  </span>
                  <span className="w-full truncate pb-2 text-[12px] text-text-2">{i.name}</span>
                </Link>
                {i.area === "brands" && (
                  <span className="pointer-events-none absolute left-2 top-2 rounded bg-surface-2 px-1 text-[10px] text-muted">Brand</span>
                )}
                {i.displayStyle && (
                  <button
                    type="button"
                    onClick={() => toggle(i)}
                    aria-pressed={selected}
                    aria-label={`${selected ? "Remove" : "Add"} ${i.name} (${i.displayStyle}) ${selected ? "from" : "to"} selection`}
                    className={cn(
                      "absolute right-1.5 top-1.5 flex h-7 w-7 items-center justify-center rounded-lg border text-text-2 transition-opacity",
                      selected ? "border-accent bg-accent text-accent-contrast opacity-100" : "border-border bg-surface opacity-0 group-hover:opacity-100 focus-visible:opacity-100",
                    )}
                  >
                    <UiIcon name={selected ? "check" : "plus"} size={14} />
                  </button>
                )}
              </li>
            );
          })}
        </ul>
      )}

      {view === "list" && (
        <div className="overflow-x-auto rounded-xl border border-border bg-surface">
          <table className="w-full text-sm">
            <caption className="sr-only">Icons</caption>
            <thead>
              <tr className="border-b border-border text-left text-xs uppercase tracking-wider text-muted">
                <th scope="col" className="w-12 px-3 py-2"><span className="sr-only">Preview</span></th>
                <th scope="col" className="px-3 py-2 font-semibold">Name</th>
                <th scope="col" className="px-3 py-2 font-semibold">Source</th>
                <th scope="col" className="px-3 py-2 font-semibold">Styles</th>
                <th scope="col" className="px-3 py-2 font-semibold">Unicode</th>
                <th scope="col" className="px-3 py-2 font-semibold">License</th>
                <th scope="col" className="px-3 py-2"><span className="sr-only">Select</span></th>
              </tr>
            </thead>
            <tbody>
              {items.map((i) => {
                const selected = !!i.displayStyle && selection.has(i.id, i.displayStyle);
                return (
                  <tr key={i.id} className="border-b border-border last:border-0 hover:bg-surface-2">
                    <td className="px-3 py-2 text-text" style={colorStyle}>
                      {i.displayStyle ? <IconSvgClient svg={i.svg} size={Math.min(prefs.size, 32)} /> : <span className="text-xs text-muted">Unavailable</span>}
                    </td>
                    <td className="px-3 py-2">
                      <Link href={`/icons/${i.name}${i.displayStyle ? `?style=${i.displayStyle}` : ""}`} className="font-medium text-text hover:text-accent">
                        {i.name}
                      </Link>
                    </td>
                    <td className="px-3 py-2 text-text-2">{i.sourceName}</td>
                    <td className="px-3 py-2 text-text-2">{i.styles.map((s) => STYLE_LABEL[s]).join(", ")}</td>
                    <td className="px-3 py-2 font-mono text-xs text-text-2">{i.codepoint ? hex(i.codepoint) : "none"}</td>
                    <td className="px-3 py-2 text-xs text-text-2">{i.license}</td>
                    <td className="px-3 py-2 text-right">
                      {i.displayStyle && (
                        <button type="button" onClick={() => toggle(i)} aria-pressed={selected} className="rounded-lg border border-border px-2 py-1 text-xs hover:border-border-strong">
                          {selected ? "Selected" : "Select"}
                        </button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {view === "cheatsheet" && (
        <ul className="grid grid-cols-[repeat(auto-fill,minmax(220px,1fr))] gap-x-4 gap-y-1 rounded-xl border border-border bg-surface p-3" aria-label="Icons cheatsheet">
          {items.map((i) => (
            <li key={i.id}>
              <Link href={`/icons/${i.name}`} className="flex items-center gap-3 rounded-lg px-2 py-1.5 hover:bg-surface-2">
                <span className="text-text" style={colorStyle}>
                  {i.displayStyle ? <IconSvgClient svg={i.svg} size={20} /> : <span className="inline-block h-5 w-5 rounded border border-dashed border-border-strong" />}
                </span>
                <span className="min-w-0 flex-1 truncate font-mono text-xs text-text">{i.name}</span>
                <span className="font-mono text-[11px] text-muted">{i.codepoint ? hex(i.codepoint).slice(2) : ""}</span>
              </Link>
            </li>
          ))}
        </ul>
      )}
      {!items.length && <p className="sr-only">No results</p>}
      <p className="mt-2 text-xs text-muted">{fmt(items.length)} shown on this page.</p>
    </div>
  );
}
