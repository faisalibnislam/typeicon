import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { StaticGrid } from "@/components/static-grid";
import { fmt } from "@/lib/format";
import { parseSearchParams, searchIcons } from "@/lib/search";

export const dynamic = "force-dynamic";

const STYLES: Record<string, { name: string; family: string; body: string[] }> = {
  filled: {
    name: "Filled",
    family: "TypeIcon Filled",
    body: [
      "Solid shapes drawn to the outer edge of the Line outline, with interior details knocked out as 2px counters.",
      "Filled designs are drawn per icon. They are never produced by switching on a fill for an outline.",
      "Pure stroke symbols (check, plus, arrows) are drawn as heavier solid forms with solid arrowheads, so Filled never repeats Line geometry.",
    ],
  },
  line: {
    name: "Line",
    family: "TypeIcon Line",
    body: ["2px outlines on the 24×24 grid with butt caps, miter joins, sharp polyline corners and 2px container corners.", "Drawn for sizes from 16 to 24px."],
  },
  rounded: {
    name: "Rounded",
    family: "TypeIcon Rounded",
    body: [
      "The same 2px outline skeleton as Line, with round caps, round joins, 1.5px fillets on polyline corners and 4px container corners.",
      "Rounded is about corner and terminal treatment. It is not a rounded square placed around each icon.",
    ],
  },
  thin: {
    name: "Thin",
    family: "TypeIcon Thin",
    body: [
      "Line geometry (butt caps, miter joins, the same corner radii) drawn with a 1px stroke, half the weight of Line.",
      "Thin is published only where it differs from Line. Icons made only of solid shapes have no distinct Thin and are not given one.",
    ],
  },
};

export function generateStaticParams() {
  return Object.keys(STYLES).map((slug) => ({ slug }));
}

export async function generateMetadata(props: PageProps<"/styles/[slug]">): Promise<Metadata> {
  const s = STYLES[(await props.params).slug];
  return s ? { title: `${s.name} style`, description: s.body[0], alternates: { canonical: `/styles/${(await props.params).slug}` } } : {};
}

export default async function StylePage(props: PageProps<"/styles/[slug]">) {
  const { slug } = await props.params;
  const s = STYLES[slug];
  if (!s) notFound();
  const [core, all] = await Promise.all([
    searchIcons(parseSearchParams({ style: slug, area: "core", per: "96" })),
    searchIcons(parseSearchParams({ style: slug, per: "48" })),
  ]);
  return (
    <div className="mx-auto max-w-[1440px] px-4 pb-24 pt-8 sm:px-6">
      <div className="mb-2 flex gap-2 text-sm">
        {Object.entries(STYLES).map(([k, v]) => (
          <Link key={k} href={`/styles/${k}`} aria-current={k === slug ? "page" : undefined} className={k === slug ? "rounded-lg bg-text px-3 py-1.5 text-bg" : "rounded-lg px-3 py-1.5 text-text-2 hover:bg-surface-2"}>{v.name}</Link>
        ))}
      </div>
      <h1 className="mt-4 text-3xl font-semibold tracking-tight">{s.name}</h1>
      <p className="mt-1 text-sm text-muted">Desktop and web family: <strong className="text-text">{s.family}</strong></p>
      <ul className="mb-8 mt-3 max-w-3xl list-disc space-y-1 pl-5 text-text-2">{s.body.map((b) => <li key={b}>{b}</li>)}</ul>
      <h2 className="mb-3 text-lg font-semibold">TypeIcon Core in {s.name} <span className="text-sm font-normal text-muted">({fmt(core.total)})</span></h2>
      <StaticGrid items={core.items} label={`Core ${s.name} icons`} />
      <div className="mb-3 mt-10 flex items-end justify-between">
        <h2 className="text-lg font-semibold">All packs in {s.name} <span className="text-sm font-normal text-muted">({fmt(all.total)})</span></h2>
        <Link href={`/icons?style=${slug}`} className="text-sm text-accent hover:underline">Browse all →</Link>
      </div>
      <p className="mb-3 text-sm text-muted">{all.facets.packs.map((p) => `${p.label}: ${fmt(p.count)}`).join(" · ")}. Packs without this style are not shown; their icons are never substituted.</p>
    </div>
  );
}
