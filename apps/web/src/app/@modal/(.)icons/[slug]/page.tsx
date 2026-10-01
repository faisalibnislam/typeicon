import Link from "next/link";
import { notFound } from "next/navigation";
import { IconDetail } from "@/components/detail/icon-detail";
import { IconModal } from "@/components/detail/icon-modal";
import { getDesign, getLatestRelease } from "@/lib/catalog";
import { hex } from "@/lib/format";

/**
 * Intercepted /icons/[slug]: when an icon is opened by a client-side click, it appears in a modal
 * over the current page. A direct visit or refresh renders the full page in app/icons/[slug].
 */
export default async function IconModalPage(props: PageProps<"/icons/[slug]">) {
  const { slug } = await props.params;
  const design = await getDesign(slug);
  if (!design) notFound();
  const release = await getLatestRelease();
  const cssHref = release ? `/api/files/releases/${release.version}/css/${design.area === "core" ? "typeicon.css" : `typeicon-${design.source.slug}.css`}` : null;
  const summary = (
    <div className="flex flex-wrap items-center gap-x-2 gap-y-1.5 text-xs">
      <span className="rounded-full bg-accent-soft px-2 py-0.5 font-medium text-accent">{design.area === "core" ? "TypeIcon Core" : design.source.displayName}</span>
      <Link href={`/licenses#${design.source.slug}`} className="rounded-full border border-border px-2 py-0.5 text-text-2 hover:border-border-strong">{design.license.id}</Link>
      {design.categories.map((c) => (
        <Link key={c} href={`/categories/${c}`} className="rounded-full border border-border px-2 py-0.5 text-text-2 hover:border-border-strong">{c.replace(/-/g, " ")}</Link>
      ))}
      {design.aliases.length > 0 && <span className="text-muted">aliases: {design.aliases.join(", ")}</span>}
      {design.isBrand && <span className="text-muted">Brand logo, a trademark of its owner</span>}
      {design.release && <span className="text-muted">since {design.release.version}</span>}
    </div>
  );
  return (
    <IconModal name={design.name} codepointHex={design.codepoint ? hex(design.codepoint) : null} summary={summary}>
      <IconDetail design={design} cssHref={cssHref} compact />
    </IconModal>
  );
}
