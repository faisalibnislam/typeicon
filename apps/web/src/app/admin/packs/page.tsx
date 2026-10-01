import { ActionButton } from "@/components/admin/action-button";
import { listPacks } from "@/lib/catalog";
import { fmt } from "@/lib/format";

export default async function AdminPacks() {
  const packs = await listPacks();
  return (
    <div>
      <h1 className="mb-1 text-2xl font-semibold tracking-tight">Packs</h1>
      <p className="mb-6 text-sm text-muted">Pack-level license and provenance review. Approving publishes the pack&apos;s validated variants; withdrawing unpublishes them (they stay in the database).</p>
      <div className="space-y-4">
        {packs.map((p) => (
          <section key={p.slug} className="rounded-2xl border border-border bg-surface p-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <h2 className="font-semibold">{p.displayName} <span className="font-normal text-muted">{p.version} · {p.licenseId} · {p.area}</span></h2>
                <p className="text-xs text-muted">{fmt(p.designs)} published designs · {Object.entries(p.byStyle).map(([s, n]) => `${s} ${fmt(n)}`).join(" · ")}</p>
              </div>
              <div className="flex items-center gap-2">
                <span className={p.reviewStatus === "approved" ? "text-sm text-success" : "text-sm text-danger"}>{p.reviewStatus}</span>
                {p.reviewStatus !== "approved" && <ActionButton url={`/api/admin/packs/${p.slug}`} body={{ status: "approved" }} label="Approve" variant="primary" />}
                {p.reviewStatus === "approved" && <ActionButton url={`/api/admin/packs/${p.slug}`} body={{ status: "pending" }} label="Withdraw" variant="danger" confirmText={`Unpublish every ${p.displayName} icon?`} />}
              </div>
            </div>
            <dl className="mt-3 grid gap-x-4 gap-y-1 text-xs sm:grid-cols-[140px_1fr]">
              <dt className="text-muted">Integrity</dt><dd className="break-all font-mono">{p.distribution.integrity ?? "local source"}</dd>
              <dt className="text-muted">Upstream</dt><dd>{p.upstreamUrl}</dd>
              <dt className="text-muted">Copyright</dt><dd>{p.copyright}</dd>
              <dt className="text-muted">Review note</dt><dd>{p.reviewNote ?? "None"}</dd>
              <dt className="text-muted">Modifications</dt><dd>{p.modificationHistory.join("; ") || "None"}</dd>
            </dl>
          </section>
        ))}
      </div>
    </div>
  );
}
