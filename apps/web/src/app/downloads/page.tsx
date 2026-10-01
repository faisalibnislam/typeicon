import type { Metadata } from "next";
import Link from "next/link";
import { UiIcon } from "@/components/ui-icon";
import { getLatestRelease, listPacks } from "@/lib/catalog";
import { bytes, fmt, STYLE_LABEL } from "@/lib/format";

export const dynamic = "force-dynamic";
export const metadata: Metadata = {
  title: "Downloads",
  description: "Download TypeIcon desktop fonts (OTF/TTF), web fonts, SVGs and metadata, or build a custom subset.",
  alternates: { canonical: "/downloads" },
};

export default async function DownloadsPage() {
  const [release, packs] = await Promise.all([getLatestRelease(), listPacks()]);
  if (!release) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-16">
        <h1 className="text-2xl font-semibold">Downloads</h1>
        <p className="mt-2 text-text-2">No release has been published yet. Run the release build and catalog load (see README).</p>
      </div>
    );
  }
  const href = (file: string) => `/api/files/releases/${release.version}/${file}`;
  const main = ["complete", "desktop", "web", "svg", "metadata"]
    .map((k) => release.archives.find((a) => a.kind === k))
    .filter(Boolean) as typeof release.archives;
  const packName = Object.fromEntries(packs.map((p) => [p.slug, p.displayName]));
  const familyZip = (slug: string) => release.archives.find((a) => a.kind === "family-desktop" && a.meta.slug === slug);

  return (
    <div className="mx-auto max-w-[1200px] px-4 pb-24 pt-8 sm:px-6">
      <header className="mb-8">
        <h1 className="text-3xl font-semibold tracking-tight">Downloads</h1>
        <p className="mt-2 max-w-2xl text-text-2">
          Release <strong className="text-text">{release.version}</strong> ({release.releaseDate}) · {fmt(release.counts.icons ?? 0)} icons,{" "}
          {fmt(release.counts.variants ?? 0)} style variants, {fmt(release.counts.fontGlyphs ?? 0)} font glyphs. Archives are static, versioned files with SHA-256 checksums.
        </p>
      </header>

      <section aria-labelledby="bundles" className="mb-12">
        <h2 id="bundles" className="mb-3 text-lg font-semibold">Release archives</h2>
        <ul className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
          {main.map((a) => (
            <li key={a.file} className="flex flex-col rounded-2xl border border-border bg-surface p-5">
              <h3 className="font-semibold text-text">{a.label}</h3>
              <p className="mt-1 text-sm text-muted">
                {a.kind === "desktop" && "OTF and TTF for every family. Install these for Figma and other desktop apps."}
                {a.kind === "web" && "WOFF2, WOFF, CSS and runnable HTML examples."}
                {a.kind === "svg" && "Sanitized SVG files and symbol sprites for every style."}
                {a.kind === "metadata" && "Names, aliases, codepoints, glyph maps and manifests (JSON + TypeScript types)."}
                {a.kind === "complete" && "Everything above in one archive, with licenses and checksums."}
              </p>
              <div className="mt-4 flex items-center justify-between gap-3">
                <a href={href(a.file)} className="inline-flex items-center gap-2 rounded-xl bg-accent px-3.5 py-2 text-sm font-semibold text-accent-contrast hover:bg-accent-hover">
                  <UiIcon name="download" size={16} /> {bytes(a.bytes)}
                </a>
                <span className="text-xs text-muted">{fmt(Number(a.meta.files ?? 0))} files</span>
              </div>
              <p className="mt-3 break-all font-mono text-[10px] text-muted" title="SHA-256">sha256 {a.sha256}</p>
            </li>
          ))}
          <li className="flex flex-col rounded-2xl border border-dashed border-border-strong p-5">
            <h3 className="font-semibold text-text">Custom subset</h3>
            <p className="mt-1 text-sm text-muted">Pick only the icons you need. Get small, uniquely named fonts plus CSS and SVGs.</p>
            <Link href="/downloads/subset" className="mt-4 inline-flex w-fit items-center gap-2 rounded-xl border border-border bg-surface px-3.5 py-2 text-sm font-semibold text-text hover:bg-surface-2">
              Build a subset →
            </Link>
          </li>
        </ul>
      </section>

      <section aria-labelledby="families" className="mb-12">
        <h2 id="families" className="mb-1 text-lg font-semibold">Font families</h2>
        <p className="mb-4 max-w-3xl text-sm text-text-2">
          After installing, choose exactly this family name in your app. Each family is a separate font with one Regular style, so switching the family switches the style while your keywords stay the same. TypeIcon Thin contains only icons whose Thin differs from Line.
        </p>
        <div className="overflow-x-auto rounded-2xl border border-border bg-surface">
          <table className="w-full min-w-[860px] text-sm">
            <thead>
              <tr className="border-b border-border text-left text-xs uppercase tracking-wider text-muted">
                <th scope="col" className="px-4 py-3">Installed family name</th>
                <th scope="col" className="px-4 py-3">Source</th>
                <th scope="col" className="px-4 py-3">Style</th>
                <th scope="col" className="px-4 py-3 text-right">Glyphs</th>
                <th scope="col" className="px-4 py-3 text-right">Keywords</th>
                <th scope="col" className="px-4 py-3">Checks</th>
                <th scope="col" className="px-4 py-3">Download</th>
              </tr>
            </thead>
            <tbody>
              {release.families.map((f) => {
                const zip = familyZip(f.slug);
                const otf = f.validation.otf?.stats as { ots?: string; shapingChecked?: number } | undefined;
                return (
                  <tr key={f.slug} className="border-b border-border last:border-0">
                    <th scope="row" className="px-4 py-3 text-left font-medium text-text">{f.family}</th>
                    <td className="px-4 py-3 text-text-2">{packName[f.source] ?? f.source}</td>
                    <td className="px-4 py-3 text-text-2">{STYLE_LABEL[f.style]}</td>
                    <td className="px-4 py-3 text-right tabular-nums text-text-2">{fmt(f.glyphCount)}</td>
                    <td className="px-4 py-3 text-right tabular-nums text-text-2">{fmt(f.keywordCount)}</td>
                    <td className="px-4 py-3 text-xs text-muted">
                      OTS {otf?.ots ?? "not run"} · {fmt(otf?.shapingChecked ?? 0)} keywords shaped
                      {f.raster && <> · raster IoU ≥ {f.raster.minIoU}</>}
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex flex-wrap gap-1.5 text-xs">
                        {zip && <a href={href(zip.file)} className="rounded-lg bg-text px-2.5 py-1 font-medium text-bg">ZIP {bytes(zip.bytes)}</a>}
                        {f.files.otf && <a href={href(`desktop/${f.files.otf.name}`)} className="rounded-lg border border-border px-2 py-1 text-text-2 hover:border-border-strong">OTF</a>}
                        {f.files.ttf && <a href={href(`desktop/${f.files.ttf.name}`)} className="rounded-lg border border-border px-2 py-1 text-text-2 hover:border-border-strong">TTF</a>}
                        {f.files.woff2 && <a href={href(`webfonts/${f.files.woff2.name}`)} className="rounded-lg border border-border px-2 py-1 text-text-2 hover:border-border-strong">WOFF2</a>}
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
        <p className="mt-3 text-xs text-muted">
          Checks: OpenType Sanitizer (the validator browsers use), HarfBuzz shaping of every keyword and alias, and a raster comparison between each glyph and its SVG.
          Desktop app behaviour (Figma, Sketch, Office) is listed separately on the <Link href="/docs/compatibility" className="text-accent underline underline-offset-2 hover:text-accent-hover">compatibility</Link> page.
        </p>
      </section>

      <section aria-labelledby="svgzips">
        <h2 id="svgzips" className="mb-3 text-lg font-semibold">SVGs by source</h2>
        <ul className="flex flex-wrap gap-2">
          {release.archives
            .filter((a) => a.kind === "source-svg")
            .map((a) => (
              <li key={a.file}>
                <a href={href(a.file)} className="inline-flex items-center gap-2 rounded-xl border border-border bg-surface px-3 py-2 text-sm text-text-2 hover:border-border-strong">
                  {a.label} <span className="text-xs text-muted">{bytes(a.bytes)}</span>
                </a>
              </li>
            ))}
        </ul>
        <p className="mt-4 text-sm text-muted">
          Every archive contains <code className="font-mono">licenses/</code> with each source&apos;s license and attribution. Brand logos keep their own licenses and remain trademarks of their owners (see{" "}
          <Link href="/licenses" className="text-accent underline underline-offset-2 hover:text-accent-hover">Licenses</Link>).
        </p>
      </section>
    </div>
  );
}
