"use client";
import Link from "next/link";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useCallback, useMemo, useRef, useState } from "react";
import type { DesignDetail, VariantDetail } from "@/lib/catalog";
import { cn } from "@/lib/cn";
import { hex, STYLE_LABEL } from "@/lib/format";
import { coloredSvg, isSafeSvg, sizedSvg, transformedSvg } from "@/lib/svg";
import { IconSvgClient } from "../icon-svg-client";
import { useSelection } from "../selection/selection-provider";
import { UiIcon } from "../ui-icon";
import { AddToCollection } from "./add-to-collection";

const STYLES = ["filled", "line", "rounded", "thin"] as const;
const PNG_SIZES = [32, 64, 128, 256, 512, 1024];
const REVIEW_SIZES = [16, 20, 24, 32, 48];

function pascal(name: string) {
  return name.replace(/(^|-)([a-z0-9])/g, (_, __, c: string) => c.toUpperCase()).replace(/^(\d)/, "Icon$1");
}

function download(filename: string, blob: Blob) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
}

export function IconDetail({ design, cssHref, compact = false }: { design: DesignDetail; cssHref: string | null; compact?: boolean }) {
  const router = useRouter();
  const pathname = usePathname();
  const params = useSearchParams();
  const STYLE_SET = (design.area === "brands" ? ["brand"] : STYLES) as readonly string[];
  const byStyle = useMemo(() => Object.fromEntries(design.variants.map((v) => [v.style, v])) as Partial<Record<string, VariantDetail>>, [design]);
  const requested = params.get("style") ?? "";
  const fallback = (["line", "rounded", "filled", "brand"] as const).find((s) => byStyle[s]) ?? "line";
  const style = (STYLE_SET.includes(requested) ? requested : fallback) as "filled" | "line" | "rounded" | "thin" | "brand";
  const variant = byStyle[style];

  const [size, setSize] = useState(96);
  const [color, setColor] = useState<string | null>(null);
  const [bg, setBg] = useState<"light" | "dark" | "checker">("light");
  const [rotate, setRotate] = useState(0);
  const [flipX, setFlipX] = useState(false);
  const [flipY, setFlipY] = useState(false);
  const [pngSize, setPngSize] = useState(256);
  const [status, setStatus] = useState<{ kind: "ok" | "error"; text: string } | null>(null);
  const [tab, setTab] = useState<"html" | "css" | "svg" | "react" | "vue">("html");
  const statusTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const selection = useSelection();

  const say = useCallback((kind: "ok" | "error", text: string) => {
    setStatus({ kind, text });
    if (statusTimer.current) clearTimeout(statusTimer.current);
    statusTimer.current = setTimeout(() => setStatus(null), 4000);
  }, []);

  const setStyle = (s: string) => {
    const next = new URLSearchParams(params.toString());
    next.set("style", s);
    // Native history update (synced by Next.js) instead of a router navigation: a navigation to
    // /icons/[slug] would be intercepted by the icon modal route and open a modal over this page.
    window.history.replaceState(null, "", `${pathname}?${next}`);
  };

  const transform = { rotate, flipX, flipY };
  const customized = rotate !== 0 || flipX || flipY || !!color;
  const finalSvg = useMemo(() => {
    if (!variant?.svg || !isSafeSvg(variant.svg)) return null;
    let s = transformedSvg(variant.svg, transform);
    s = coloredSvg(s, color);
    if (!s.includes("xmlns=")) s = s.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ');
    return s;
  }, [variant, rotate, flipX, flipY, color]); // eslint-disable-line react-hooks/exhaustive-deps

  async function copy(text: string, what: string) {
    try {
      await navigator.clipboard.writeText(text);
      say("ok", `Copied ${what}`);
    } catch {
      say("error", `Could not access the clipboard. Select the ${what} text and copy it manually.`);
    }
  }

  function downloadSvg() {
    if (!finalSvg) return say("error", "This style has no SVG available.");
    const vb = variant!.viewBox ?? [0, 0, 24, 24];
    const file = sizedSvg(finalSvg, { size: 24 }).replace(/ aria-hidden="true" focusable="false"/, "");
    download(`${design.name}-${style}.svg`, new Blob([file + "\n"], { type: "image/svg+xml" }));
    say("ok", `Downloaded ${design.name}-${style}.svg${customized ? " with your color/rotation" : ""} (viewBox ${vb.join(" ")})`);
  }

  async function downloadPng() {
    if (!variant?.svg) return say("error", "This style has no SVG available.");
    try {
      const vb = variant.viewBox ?? [0, 0, 24, 24];
      const ratio = vb[2] / vb[3];
      const w = Math.round(pngSize * ratio);
      const colored = coloredSvg(transformedSvg(variant.svg, transform), color ?? "#000000");
      const svgText = sizedSvg(colored.includes("xmlns=") ? colored : colored.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" '), { size: pngSize });
      const img = new Image();
      const url = URL.createObjectURL(new Blob([svgText], { type: "image/svg+xml" }));
      await new Promise<void>((res, rej) => {
        img.onload = () => res();
        img.onerror = () => rej(new Error("render failed"));
        img.src = url;
      });
      const canvas = document.createElement("canvas");
      canvas.width = w;
      canvas.height = pngSize;
      const ctx = canvas.getContext("2d");
      if (!ctx) throw new Error("no canvas");
      ctx.drawImage(img, 0, 0, w, pngSize);
      URL.revokeObjectURL(url);
      const blob = await new Promise<Blob | null>((res) => canvas.toBlob(res, "image/png"));
      if (!blob) throw new Error("encode failed");
      download(`${design.name}-${style}-${pngSize}.png`, blob);
      say("ok", `Downloaded ${w}×${pngSize} PNG with transparent background`);
    } catch (e) {
      say("error", `PNG export failed: ${(e as Error).message}`);
    }
  }

  const glyph = design.codepoint ? String.fromCodePoint(design.codepoint) : null;
  const keyword = variant?.keywords?.[0] ?? design.name;
  const family = variant?.fontFamily ?? null;
  const familyClass = variant?.cssClass ?? (design.area === "core" ? `typeicon-${style}` : null);
  const comp = pascal(design.name);
  const subpath = design.area === "core" ? `${style}/${design.name}` : `brands/${design.name}`;
  const snippets = {
    html: `<!-- Ligature: the font turns the keyword into the icon. Decorative, so hidden from screen readers. -->\n<span class="typeicon ${familyClass ?? ""}" aria-hidden="true">${keyword}</span>\n\n<!-- Icon-only button: give the button an accessible name. -->\n<button type="button" aria-label="${design.localName.replace(/-/g, " ")}">\n  <span class="typeicon ${familyClass ?? ""}" aria-hidden="true">${keyword}</span>\n</button>`,
    css: `<!-- Codepoint class (works without ligatures) -->\n<link rel="stylesheet" href="${cssHref ?? "css/typeicon.css"}">\n<span class="typeicon ${familyClass ?? ""} typeicon-${design.name}" aria-hidden="true"></span>\n\n/* Generated rule */\n.typeicon-${design.name}::before { content: "\\${design.codepoint?.toString(16).toUpperCase() ?? ""}"; }`,
    svg: finalSvg ?? "",
    react: `import ${comp} from "@typeicon/react/${subpath}";\n\n// Decorative (aria-hidden by default)\n<${comp} size={24} />\n\n// Meaningful: pass a title\n<${comp} size={24} title="${design.localName.replace(/-/g, " ")}" />`,
    vue: `<script setup lang="ts">\nimport ${comp} from "@typeicon/vue/${subpath}";\n</script>\n\n<template>\n  <${comp} :size="24" />\n</template>`,
  };
  const inSelection = variant ? selection.has(design.id, style) : false;

  return (
    <div className={cn("grid grid-cols-[minmax(0,1fr)]", compact ? "gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]" : "gap-8 xl:grid-cols-[minmax(0,1fr)_420px]")}>
      <div className="min-w-0 space-y-6">
        {/* Style switcher */}
        <div role="radiogroup" aria-label="Style" className="inline-flex rounded-xl border border-border bg-surface p-1">
          {STYLE_SET.map((s) => {
            const v = byStyle[s];
            return (
              <button
                key={s}
                type="button"
                role="radio"
                aria-checked={style === s}
                disabled={!v}
                onClick={() => setStyle(s)}
                className={cn(
                  "rounded-lg px-4 py-2 text-sm font-medium",
                  style === s ? "bg-text text-bg" : v ? "text-text-2 hover:bg-surface-2" : "cursor-not-allowed text-muted/60 line-through",
                )}
                title={v ? `${STYLE_LABEL[s]} (${v.nativeLabel})` : `${STYLE_LABEL[s]} is not available for this icon`}
              >
                {STYLE_LABEL[s]}
              </button>
            );
          })}
        </div>

        {/* Preview */}
        <div
          className={cn(
            "relative flex items-center justify-center overflow-hidden rounded-2xl border border-border",
            compact ? "min-h-[240px]" : "min-h-[320px]",
            bg === "light" && "bg-white text-[#16161a]",
            bg === "dark" && "bg-[#111113] text-[#ededf0]",
            bg === "checker" && "checker text-[#16161a]",
          )}
        >
          {variant?.svg ? (
            <span style={color ? { color } : undefined}>
              <IconSvgClient svg={transformedSvg(variant.svg, transform)} size={size} label={`${design.name} (${STYLE_LABEL[style]})`} />
            </span>
          ) : (
            <div className="text-center">
              <p className="text-base font-medium">No {STYLE_LABEL[style]} style</p>
              <p className="mt-1 text-sm opacity-70">This design is not published in {STYLE_LABEL[style]}. TypeIcon does not substitute another style.</p>
            </div>
          )}
          {variant && (
            <span className="absolute bottom-3 left-3 rounded-md bg-black/5 px-2 py-1 text-[11px] opacity-80 dark:bg-white/10">
              {design.source.displayName}: {variant.nativeLabel}
            </span>
          )}
        </div>

        {/* Controls */}
        <div className="rounded-2xl border border-border bg-surface p-4">
          <div className="flex flex-wrap items-center gap-x-6 gap-y-3">
            <label className="flex items-center gap-2 text-sm text-text-2">
              Size
              <input type="range" min={16} max={256} step={8} value={size} onChange={(e) => setSize(Number(e.target.value))} className="w-32 accent-[var(--accent)]" />
              <span className="w-12 tabular-nums text-muted">{size}px</span>
            </label>
            <div className="flex items-center gap-2 text-sm text-text-2">
              <label htmlFor="detail-color">Color</label>
              <input id="detail-color" type="color" value={color ?? "#16161a"} onChange={(e) => setColor(e.target.value)} className="h-8 w-9 cursor-pointer rounded border border-border bg-surface p-0.5" />
              {["#16161a", "#c2410c", "#1d4ed8", "#15803d"].map((c) => (
                <button key={c} type="button" onClick={() => setColor(c)} aria-label={`Color ${c}`} className="h-5 w-5 rounded-full border border-border" style={{ background: c }} />
              ))}
              {color && (
                <button type="button" onClick={() => setColor(null)} className="text-xs text-accent hover:underline">
                  currentColor
                </button>
              )}
            </div>
            <div role="radiogroup" aria-label="Background" className="flex items-center gap-1 text-sm">
              {(["light", "dark", "checker"] as const).map((b) => (
                <button key={b} type="button" role="radio" aria-checked={bg === b} onClick={() => setBg(b)} className={cn("rounded-lg border px-2 py-1 text-xs capitalize", bg === b ? "border-accent text-text" : "border-border text-muted")}>
                  {b === "checker" ? "Transparent" : b}
                </button>
              ))}
            </div>
            <div className="flex items-center gap-1 text-sm">
              <button type="button" onClick={() => setRotate((r) => (r + 90) % 360)} className="rounded-lg border border-border px-2 py-1 text-xs text-text-2 hover:border-border-strong" aria-label={`Rotate 90 degrees (currently ${rotate})`}>
                Rotate {rotate}°
              </button>
              <button type="button" aria-pressed={flipX} onClick={() => setFlipX((v) => !v)} className={cn("rounded-lg border px-2 py-1 text-xs", flipX ? "border-accent text-text" : "border-border text-text-2")}>
                Flip H
              </button>
              <button type="button" aria-pressed={flipY} onClick={() => setFlipY((v) => !v)} className={cn("rounded-lg border px-2 py-1 text-xs", flipY ? "border-accent text-text" : "border-border text-text-2")}>
                Flip V
              </button>
              {(rotate || flipX || flipY) && (
                <button type="button" onClick={() => { setRotate(0); setFlipX(false); setFlipY(false); }} className="text-xs text-accent hover:underline">
                  Reset
                </button>
              )}
            </div>
          </div>
          <p className="mt-3 text-xs text-muted">
            Color, rotation and flip apply to the preview, the SVG download, the PNG download and the copied SVG. Size and background apply to the preview only.
            HTML, CSS, React and Vue snippets always use <code>currentColor</code> and no transform.
          </p>
        </div>

        {/* Small-size review strip */}
        {!compact && variant?.svg && (
          <section aria-labelledby="size-check">
            <h2 id="size-check" className="mb-2 text-sm font-semibold text-text">Size check</h2>
            <div className="grid gap-2 sm:grid-cols-2">
              {(["light", "dark"] as const).map((b) => (
                <div key={b} className={cn("flex items-end gap-5 rounded-xl border border-border px-4 py-3", b === "light" ? "bg-white text-[#16161a]" : "bg-[#111113] text-[#ededf0]")}>
                  {REVIEW_SIZES.map((s) => (
                    <div key={s} className="flex flex-col items-center gap-1">
                      <IconSvgClient svg={variant.svg} size={s} />
                      <span className="text-[10px] opacity-60">{s}</span>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Style comparison */}
        {!compact && design.area !== "brands" && <section aria-labelledby="compare">
          <h2 id="compare" className="mb-2 text-sm font-semibold text-text">All styles</h2>
          <ul className="grid grid-cols-3 gap-2">
            {STYLES.map((s) => {
              const v = byStyle[s];
              return (
                <li key={s}>
                  <button
                    type="button"
                    disabled={!v}
                    onClick={() => setStyle(s)}
                    className={cn(
                      "flex w-full flex-col items-center gap-2 rounded-xl border px-2 py-4 text-center",
                      v ? "border-border bg-surface hover:border-border-strong" : "cursor-default border-dashed border-border-strong",
                      style === s && v && "border-accent",
                    )}
                  >
                    {v ? <IconSvgClient svg={v.svg} size={40} /> : <span className="flex h-10 items-center text-xs text-muted">Unavailable</span>}
                    <span className="text-sm font-medium text-text">{STYLE_LABEL[s]}</span>
                    <span className="line-clamp-2 text-[11px] text-muted">{v ? v.nativeLabel : "Not published"}</span>
                  </button>
                </li>
              );
            })}
          </ul>
        </section>}
      </div>

      {/* Side panel */}
      <aside className="min-w-0 space-y-5" aria-label="Use this icon">
        <div className="flex flex-wrap gap-2">
          <button type="button" onClick={downloadSvg} disabled={!variant} className="inline-flex items-center gap-2 rounded-xl bg-accent px-4 py-2.5 text-sm font-semibold text-accent-contrast hover:bg-accent-hover disabled:opacity-50">
            <UiIcon name="download" size={16} /> Download SVG
          </button>
          <div className="inline-flex items-stretch overflow-hidden rounded-xl border border-border bg-surface">
            <button type="button" onClick={downloadPng} disabled={!variant} className="inline-flex items-center gap-2 px-3 py-2.5 text-sm font-medium text-text hover:bg-surface-2 disabled:opacity-50">
              <UiIcon name="image" size={16} /> PNG
            </button>
            <label className="sr-only" htmlFor="png-size">PNG size</label>
            <select id="png-size" value={pngSize} onChange={(e) => setPngSize(Number(e.target.value))} className="border-l border-border bg-surface px-2 text-xs text-text-2">
              {PNG_SIZES.map((s) => (
                <option key={s} value={s}>{s}px</option>
              ))}
            </select>
          </div>
          <button
            type="button"
            disabled={!variant}
            onClick={() => {
              if (!variant) return;
              selection.toggle({ designId: design.id, name: design.name, style, source: design.source.slug, svg: variant.svg });
              say("ok", inSelection ? "Removed from selection" : "Added to selection. Build a subset from the tray.");
            }}
            aria-pressed={inSelection}
            className="inline-flex items-center gap-2 rounded-xl border border-border bg-surface px-3 py-2.5 text-sm font-medium text-text hover:bg-surface-2 disabled:opacity-50"
          >
            <UiIcon name={inSelection ? "check" : "plus"} size={16} /> {inSelection ? "In subset" : "Add to subset"}
          </button>
          <AddToCollection designId={design.id} style={style} disabled={!variant} onDone={say} />
          <button type="button" onClick={() => copy(window.location.href, "link")} className="inline-flex items-center gap-2 rounded-xl border border-border bg-surface px-3 py-2.5 text-sm font-medium text-text hover:bg-surface-2">
            <UiIcon name="link" size={16} /> Copy link
          </button>
        </div>
        <p role="status" aria-live="polite" className={cn("min-h-5 text-sm", status?.kind === "error" ? "text-danger" : "text-success")}>
          {status?.text}
        </p>

        {/* Font / glyph */}
        <section className="rounded-2xl border border-border bg-surface p-4" aria-labelledby="font-h">
          <h2 id="font-h" className="mb-3 text-sm font-semibold text-text">Font and glyph</h2>
          {variant?.fontSupported && family ? (
            <dl className="grid grid-cols-[110px_1fr] gap-x-3 gap-y-2 text-sm">
              <dt className="text-muted">Font family</dt>
              <dd className="font-medium text-text">{family}</dd>
              <dt className="text-muted">Keyword</dt>
              <dd className="flex items-center gap-2">
                <code className="rounded bg-surface-2 px-1.5 py-0.5 font-mono text-[13px] text-text">{keyword}</code>
                <button type="button" onClick={() => copy(keyword, "keyword")} className="text-xs text-accent hover:underline">Copy</button>
              </dd>
              {variant.keywords.length > 1 && (
                <>
                  <dt className="text-muted">Also types as</dt>
                  <dd className="font-mono text-[13px] text-text-2">{variant.keywords.slice(1).join(", ")}</dd>
                </>
              )}
              <dt className="text-muted">Unicode</dt>
              <dd className="font-mono text-[13px] text-text">
                {design.codepoint ? hex(design.codepoint) : "none"}
                {design.bmpCodepoint ? <span className="text-muted"> · BMP {hex(design.bmpCodepoint)}</span> : null}
              </dd>
              <dt className="text-muted">Glyph</dt>
              <dd className="flex flex-wrap items-center gap-2">
                {glyph && (
                  <>
                    <button type="button" onClick={() => copy(glyph, "glyph character")} className="rounded-lg border border-border px-2 py-1 text-xs text-text-2 hover:border-border-strong">
                      Copy glyph
                    </button>
                    {design.bmpCodepoint && (
                      <button type="button" onClick={() => copy(String.fromCodePoint(design.bmpCodepoint!), "BMP glyph character")} className="rounded-lg border border-border px-2 py-1 text-xs text-text-2 hover:border-border-strong">
                        Copy BMP glyph
                      </button>
                    )}
                  </>
                )}
              </dd>
              <dt className="text-muted">CSS class</dt>
              <dd className="font-mono text-[13px] text-text-2">
                typeicon {familyClass} typeicon-{design.name}
              </dd>
            </dl>
          ) : (
            <p className="text-sm text-text-2">
              {variant ? `This style is delivered as SVG only${variant.reasons.length ? ` (${variant.reasons.join("; ")})` : ""}.` : "Select an available style."}
            </p>
          )}
          <p className="mt-3 text-xs text-muted">
            A copied private-use character only shows this icon when the text uses the exact font family above. In other fonts it appears as a box or nothing.
          </p>
        </section>

        {/* Code */}
        <section className="rounded-2xl border border-border bg-surface" aria-labelledby="code-h">
          <div className="flex items-center justify-between border-b border-border px-4 pt-3">
            <h2 id="code-h" className="sr-only">Code</h2>
            <div role="tablist" aria-label="Code format" className="-mb-px flex gap-1">
              {(["html", "css", "svg", "react", "vue"] as const).map((t) => (
                <button key={t} role="tab" type="button" aria-selected={tab === t} onClick={() => setTab(t)} className={cn("border-b-2 px-2.5 py-2 text-xs font-medium uppercase tracking-wide", tab === t ? "border-accent text-text" : "border-transparent text-muted hover:text-text")}>
                  {t}
                </button>
              ))}
            </div>
            <button type="button" onClick={() => copy(snippets[tab], `${tab.toUpperCase()} snippet`)} className="mb-2 inline-flex items-center gap-1 rounded-lg px-2 py-1 text-xs text-accent hover:bg-accent-soft">
              <UiIcon name="copy" size={14} /> Copy
            </button>
          </div>
          <pre role="tabpanel" tabIndex={0} aria-label="Code snippet" className="max-h-72 overflow-auto p-4 text-[12px] leading-relaxed text-text-2">
            <code>{snippets[tab]}</code>
          </pre>
          {(tab === "react" || tab === "vue") && (
            <p className="border-t border-border px-4 py-2 text-xs text-muted">
              <code>@typeicon/{tab}</code> is a local workspace package in this repository. No npm scope has been registered yet.
            </p>
          )}
        </section>

        {/* Provenance */}
        {!compact && <section className="rounded-2xl border border-border bg-surface p-4" aria-labelledby="source-h">
          <h2 id="source-h" className="mb-3 text-sm font-semibold text-text">Source and license</h2>
          <dl className="grid grid-cols-[110px_1fr] gap-x-3 gap-y-2 text-sm">
            <dt className="text-muted">Source</dt>
            <dd>
              <Link href={`/packs/${design.source.slug}`} className="text-text hover:text-accent">{design.source.displayName}</Link>
              <span className="text-muted"> {design.source.version}</span>
            </dd>
            <dt className="text-muted">License</dt>
            <dd>
              <Link href={`/licenses#${design.source.slug}`} className="text-text hover:text-accent">{design.license.id}</Link>
            </dd>
            {design.source.copyright && (
              <>
                <dt className="text-muted">Copyright</dt>
                <dd className="text-text-2">{design.source.copyright}</dd>
              </>
            )}
            {design.source.attributionRequired && design.source.attributionText && (
              <>
                <dt className="text-muted">Attribution</dt>
                <dd className="text-text-2">{design.source.attributionText}</dd>
              </>
            )}
            {variant && (
              <>
                <dt className="text-muted">Upstream file</dt>
                <dd className="break-all font-mono text-[11px] text-text-2">{variant.sourcePath}</dd>
                <dt className="text-muted">Checksums</dt>
                <dd className="break-all font-mono text-[11px] text-text-2" title="sha256 of the original upstream file / of the sanitized SVG">
                  src {variant.sourceSha256.slice(0, 16)}… · svg {variant.svgSha256?.slice(0, 16)}…
                </dd>
                <dt className="text-muted">Variant ID</dt>
                <dd className="break-all font-mono text-[11px] text-text-2">{variant.id}</dd>
              </>
            )}
            {design.release && (
              <>
                <dt className="text-muted">Release</dt>
                <dd className="text-text-2">Since {design.release.version} ({design.release.releaseDate})</dd>
              </>
            )}
          </dl>
          {design.source.trademarkNote && <p className="mt-3 text-xs text-muted">{design.source.trademarkNote}</p>}
          {design.isBrand && <p className="mt-3 text-xs text-muted">Brand icons depict trademarks of their respective owners. Use them only to refer to those brands.</p>}
        </section>}
      </aside>
    </div>
  );
}
