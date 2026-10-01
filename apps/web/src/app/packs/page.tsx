import type { Metadata } from "next";
import Link from "next/link";
import { listPacks } from "@/lib/catalog";
import { fmt, STYLE_LABEL } from "@/lib/format";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Packs", description: "TypeIcon Core and the brand-logo collection, with versions, licenses and style coverage.", alternates: { canonical: "/packs" } };

export default async function PacksPage() {
  const packs = await listPacks();
  return (
    <div className="mx-auto max-w-[1200px] px-4 pb-24 pt-8 sm:px-6">
      <h1 className="text-3xl font-semibold tracking-tight">Packs</h1>
      <p className="mb-8 mt-2 max-w-3xl text-text-2">
        TypeIcon Core is original artwork designed to one specification with four styles (Filled, Line, Rounded and Thin). Brand logos are a separate area imported from Simple Icons: one style each, trademarks of their owners, and never counted toward the Core catalog goal.
      </p>
      <ul className="grid gap-4 md:grid-cols-2">
        {packs.map((p) => (
          <li key={p.slug}>
            <Link href={`/packs/${p.slug}`} className="block h-full rounded-2xl border border-border bg-surface p-5 hover:border-border-strong">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <h2 className="text-lg font-semibold text-text">{p.displayName}</h2>
                  <p className="text-sm text-muted">{p.area === "core" ? "TypeIcon Core" : "Brand logos"} · v{p.version} · {p.licenseId}</p>
                </div>
                <span className="rounded-full bg-surface-2 px-2.5 py-1 text-sm tabular-nums text-text">{fmt(p.designs)}</span>
              </div>
              <dl className="mt-4 grid grid-cols-3 gap-2 text-center">
                {(p.area === "brands" ? (["brand"] as const) : (["filled", "line", "rounded", "thin"] as const)).map((s) => (
                  <div key={s} className="rounded-xl bg-surface-2 px-2 py-2">
                    <dt className="text-[11px] text-muted">{STYLE_LABEL[s]}</dt>
                    <dd className={p.byStyle[s] ? "text-sm font-medium tabular-nums text-text" : "text-sm text-muted"}>{p.byStyle[s] ? fmt(p.byStyle[s]) : "0"}</dd>
                  </div>
                ))}
              </dl>
              {p.reviewStatus !== "approved" && <p className="mt-3 text-xs text-danger">Review status: {p.reviewStatus}</p>}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
