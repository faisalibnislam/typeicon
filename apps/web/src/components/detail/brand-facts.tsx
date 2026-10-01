import type { DesignDetail } from "@/lib/catalog";

/** Brand-logo facts: official colour, source, guidelines and the trademark notice. */
export function BrandFacts({ design }: { design: DesignDetail }) {
  const a = design.attributes;
  return (
    <div className="mt-3 max-w-3xl space-y-2 rounded-xl border border-border bg-surface p-3 text-sm text-text-2">
      <p className="flex flex-wrap items-center gap-x-4 gap-y-1">
        <span className="font-medium text-text">{a.title ?? design.name}</span>
        {a.hex && (
          <span className="inline-flex items-center gap-1.5">
            <span className="h-4 w-4 rounded border border-border" style={{ background: `#${a.hex}` }} aria-hidden="true" />
            <span className="font-mono text-xs">#{a.hex}</span>
          </span>
        )}
        {a.sourceUrl && <a href={a.sourceUrl} rel="noopener noreferrer nofollow" className="text-accent underline underline-offset-2">Logo source</a>}
        {a.guidelines && <a href={a.guidelines} rel="noopener noreferrer nofollow" className="text-accent underline underline-offset-2">Brand guidelines</a>}
        {a.licenseUrl && <a href={a.licenseUrl} rel="noopener noreferrer nofollow" className="text-accent underline underline-offset-2">Logo license ({design.license.id})</a>}
      </p>
      <p className="text-xs text-muted">
        This logo is a trademark of its owner. Use it only to refer to the brand, follow the brand&apos;s guidelines, and don&apos;t alter it.
        Brand logos come in one style only. They are imported from Simple Icons and are not TypeIcon artwork.
      </p>
    </div>
  );
}
