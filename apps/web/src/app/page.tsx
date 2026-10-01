import Link from "next/link";
import { KeywordDemo } from "@/components/home/keyword-demo";
import { IconSvg } from "@/components/icon-svg";
import { UiIcon } from "@/components/ui-icon";
import { getCoreSamples, getLatestRelease, getStats, listCategories } from "@/lib/catalog";
import { bytes, fmt } from "@/lib/format";

export const dynamic = "force-dynamic";

const SAMPLE = ["home", "search", "settings", "user", "bell", "heart", "mail", "calendar", "camera", "lock", "download", "trash", "chat", "star", "map-pin", "bolt"];

export default async function Home() {
  const [stats, release, samples, categories] = await Promise.all([getStats(), getLatestRelease(), getCoreSamples(SAMPLE), listCategories()]);
  const fontFace = release
    ? ["Filled", "Line", "Rounded"]
        .map((s) => `@font-face{font-family:"TypeIcon ${s}";src:url("/api/files/releases/${release.version}/webfonts/TypeIcon${s}-Regular.woff2") format("woff2");font-display:block}`)
        .join("")
    : "";
  const desktop = release?.archives.find((a) => a.kind === "desktop");
  const coreCats = categories.filter((c) => c.coreCount > 0).slice(0, 10);

  return (
    <div>
      {fontFace && <style dangerouslySetInnerHTML={{ __html: fontFace }} />}
      <section className="mx-auto grid max-w-[1440px] gap-10 px-4 pb-12 pt-12 sm:px-6 lg:grid-cols-[1fr_1.1fr] lg:pt-16">
        <div className="flex flex-col justify-center">
          <p className="mb-4 inline-flex w-fit items-center gap-2 rounded-full border border-border bg-surface px-3 py-1 text-xs text-text-2">
            <span className="h-1.5 w-1.5 rounded-full bg-accent" /> {release ? `Release ${release.version}` : "No release yet"} · OTF, TTF, WOFF2, SVG
          </p>
          <h1 className="text-4xl font-semibold leading-[1.05] tracking-[-0.035em] text-text sm:text-5xl lg:text-6xl">
            Icons you can type.
          </h1>
          <p className="mt-5 max-w-xl text-lg leading-relaxed text-text-2">
            Install a TypeIcon font, type <code className="rounded bg-surface-2 px-1.5 font-mono text-[0.9em]">home</code> in Figma or any app with ligatures, and get the icon.
            Change the font family to change the style. Or grab the SVG, PNG and code.
          </p>
          <form action="/icons" className="relative mt-7 max-w-xl" role="search">
            <label htmlFor="hero-search" className="sr-only">Search icons</label>
            <UiIcon name="search" size={20} className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-muted" />
            <input id="hero-search" name="q" type="search" maxLength={64} placeholder="Search icons" className="h-13 w-full rounded-2xl border border-border-strong bg-surface pl-12 pr-28 text-base shadow-sm focus:border-accent focus:outline-none focus:ring-4 focus:ring-accent/15" />
            <button type="submit" className="absolute right-2 top-1/2 -translate-y-1/2 rounded-xl bg-text px-4 py-2 text-sm font-semibold text-bg hover:opacity-90">Search</button>
          </form>
          <div className="mt-5 flex flex-wrap gap-3 text-sm">
            <Link href="/downloads" className="inline-flex items-center gap-2 rounded-xl bg-accent px-4 py-2.5 font-semibold text-accent-contrast hover:bg-accent-hover">
              <UiIcon name="download" size={16} /> Download desktop fonts{desktop ? ` · ${bytes(desktop.bytes)}` : ""}
            </Link>
            <Link href="/docs/desktop" className="inline-flex items-center gap-2 rounded-xl border border-border bg-surface px-4 py-2.5 font-medium text-text hover:bg-surface-2">
              How ligatures work
            </Link>
          </div>
        </div>
        <KeywordDemo />
      </section>

      <section className="mx-auto max-w-[1440px] px-4 sm:px-6" aria-labelledby="styles-h">
        <div className="mb-4 flex items-end justify-between">
          <h2 id="styles-h" className="text-xl font-semibold tracking-tight">Four styles, one keyword</h2>
          <Link href="/icons?area=core" className="text-sm text-accent hover:underline">All Core icons →</Link>
        </div>
        <div className="overflow-x-auto rounded-2xl border border-border bg-surface">
          <table className="w-full min-w-[720px]">
            <caption className="sr-only">TypeIcon Core icons in Filled, Line, Rounded and Thin</caption>
            <tbody>
              {(["filled", "line", "rounded", "thin"] as const).map((s) => (
                <tr key={s} className="border-b border-border last:border-0">
                  <th scope="row" className="w-48 whitespace-nowrap px-5 py-4 text-left align-middle">
                    <Link href={`/styles/${s}`} className="text-sm font-semibold text-text hover:text-accent">TypeIcon {s[0].toUpperCase() + s.slice(1)}</Link>
                    <span className="block text-xs text-muted">{s === "filled" ? "Solid shapes" : s === "line" ? "2px outline, sharp corners" : s === "thin" ? "1px outline, sharp corners" : "Round caps and joins"}</span>
                  </th>
                  {SAMPLE.map((n) => (
                    <td key={n} className="px-2 py-4 text-center text-text">
                      <Link href={`/icons/${n}?style=${s}`} className="inline-flex rounded-lg p-1.5 hover:bg-surface-2" title={`${n} (${s})`}>
                        <IconSvg svg={samples[n]?.[s] ?? null} size={24} label={`${n}, ${s}`} />
                      </Link>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="mt-2 text-xs text-muted">Rounded means round caps, round joins and softer corners on the outline. It is not a rounded container around each icon. Thin is Line drawn with a 1px stroke; it is published only where it differs from Line.</p>
      </section>

      {stats && (
        <section className="mx-auto mt-14 max-w-[1440px] px-4 sm:px-6" aria-labelledby="stats-h">
          <h2 id="stats-h" className="mb-4 text-xl font-semibold tracking-tight">What is in the catalog today</h2>
          <dl className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {[
              [fmt(stats.core.designs), "TypeIcon Core icons", `each in Filled, Line and Rounded (plus Thin where it differs from Line): ${fmt(stats.core.base ?? stats.core.designs)} individually drawn designs + ${fmt(stats.core.variants ?? 0)} variants (a design plus a badge such as plus, lock or off)`],
              [fmt(stats.designs.brands), "brand logos", "in a separate Brands area, one style each, from Simple Icons; trademarks of their owners, never counted as Core icons"],
              [fmt(stats.variants.total), "downloadable style variants", `${fmt(stats.variants.fontSupported)} of them are in fonts; ${fmt(stats.variants.svgOnly)} SVG-only`],
              [`${fmt(stats.target.gap)}`, "unique Core icons still to draw", `The goal is ${fmt(stats.target.uniqueCoreConcepts)} unique Core icons, each in Filled, Line and Rounded, with badge variants on top. Counts are computed from published records.`],
            ].map(([n, label, note]) => (
              <div key={label} className="rounded-2xl border border-border bg-surface p-5">
                <dt className="text-sm text-text-2">{label}</dt>
                <dd className="mt-1 text-3xl font-semibold tabular-nums tracking-tight text-text">{n}</dd>
                <dd className="mt-2 text-xs leading-relaxed text-muted">{note}</dd>
              </div>
            ))}
          </dl>
        </section>
      )}

      <section className="mx-auto mt-14 grid max-w-[1440px] gap-6 px-4 sm:px-6 lg:grid-cols-3" aria-label="Get started">
        {[
          ["Desktop", "Install OTF fonts on macOS or Windows, then type keywords in Figma, Sketch, Keynote or Word.", "/docs/desktop", "Desktop guide"],
          ["Web", "Use the WOFF2 fonts with CSS classes or ligatures, or inline SVG and React/Vue components.", "/docs/web", "Web guide"],
          ["Subsets", "Pick only the icons you need and generate a small, uniquely named font kit.", "/downloads/subset", "Build a subset"],
        ].map(([t, d, href, cta]) => (
          <Link key={t} href={href} className="group rounded-2xl border border-border bg-surface p-6 hover:border-border-strong">
            <h2 className="text-base font-semibold text-text">{t}</h2>
            <p className="mt-2 text-sm leading-relaxed text-text-2">{d}</p>
            <span className="mt-4 inline-block text-sm font-medium text-accent group-hover:underline">{cta} →</span>
          </Link>
        ))}
      </section>

      {coreCats.length > 0 && (
        <section className="mx-auto mt-14 max-w-[1440px] px-4 sm:px-6" aria-labelledby="cats-h">
          <h2 id="cats-h" className="mb-4 text-xl font-semibold tracking-tight">Browse by category</h2>
          <ul className="flex flex-wrap gap-2">
            {categories.slice(0, 28).map((c) => (
              <li key={c.slug}>
                <Link href={`/categories/${c.slug}`} className="inline-flex items-center gap-2 rounded-full border border-border bg-surface px-3.5 py-1.5 text-sm text-text-2 hover:border-border-strong hover:text-text">
                  {c.name}
                  <span className="text-xs tabular-nums text-muted">{fmt(c.count)}</span>
                </Link>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
