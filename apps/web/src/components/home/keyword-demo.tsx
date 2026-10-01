"use client";
import { useState } from "react";
import { cn } from "@/lib/cn";

const FAMILIES = [
  { style: "filled", family: "TypeIcon Filled" },
  { style: "line", family: "TypeIcon Line" },
  { style: "rounded", family: "TypeIcon Rounded" },
] as const;

/**
 * Types into a textarea set in the real TypeIcon web fonts. Substitution is performed by the
 * browser's shaping engine from the font's GSUB `liga` table. There is no JavaScript replacement.
 */
export function KeywordDemo() {
  const [text, setText] = useState("home search settings user arrow-right");
  const [style, setStyle] = useState<(typeof FAMILIES)[number]["style"]>("line");
  const fam = FAMILIES.find((f) => f.style === style)!;
  return (
    <div className="rounded-2xl border border-border bg-surface p-4 sm:p-5">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <div role="radiogroup" aria-label="Font family" className="inline-flex rounded-xl bg-surface-2 p-1">
          {FAMILIES.map((f) => (
            <button
              key={f.style}
              type="button"
              role="radio"
              aria-checked={style === f.style}
              onClick={() => setStyle(f.style)}
              className={cn("rounded-lg px-3 py-1.5 text-sm font-medium", style === f.style ? "bg-surface text-text shadow-sm" : "text-muted hover:text-text")}
            >
              {f.family.replace("TypeIcon ", "")}
            </button>
          ))}
        </div>
        <span className="font-mono text-xs text-muted">font-family: &quot;{fam.family}&quot;</span>
      </div>
      <label htmlFor="kw-demo" className="sr-only">
        Type icon keywords
      </label>
      <textarea
        id="kw-demo"
        value={text}
        onChange={(e) => setText(e.target.value.slice(0, 200))}
        rows={2}
        spellCheck={false}
        autoCapitalize="none"
        autoCorrect="off"
        className="w-full resize-none rounded-xl border border-border bg-bg px-4 py-3 text-[44px] leading-[1.25] text-text focus:border-accent focus:outline-none"
        style={{ fontFamily: `"${fam.family}", monospace`, fontFeatureSettings: '"liga" 1, "rlig" 1', letterSpacing: "normal" }}
      />
      <p className="mt-2 text-sm text-muted">
        Edit the text: <code className="font-mono text-text-2">home</code> becomes the icon, <code className="font-mono text-text-2">hom</code> stays letters. Switch families and the keywords keep their meaning.
        This box uses the generated WOFF2 fonts and the browser&apos;s own OpenType shaping, the same GSUB rules as the desktop OTF files.
      </p>
    </div>
  );
}
