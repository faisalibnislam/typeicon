import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { KitManager } from "@/components/kits/kit-manager";
import { capabilitiesFor } from "@/lib/entitlements";
import { getKit } from "@/lib/kits";
import { requireUser } from "@/lib/session";
import { db } from "@/db";
import { sql } from "drizzle-orm";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Kit", robots: { index: false } };

export default async function KitPage(props: PageProps<"/kits/[id]">) {
  const { id } = await props.params;
  const user = await requireUser(`/kits/${id}`);
  if (!/^[0-9a-f-]{36}$/.test(id)) notFound();
  const own = await db.execute(sql`SELECT owner_id FROM kits WHERE id = ${id}`);
  if ((own.rows[0] as { owner_id: string } | undefined)?.owner_id !== user.id) notFound();
  const [kit, caps] = await Promise.all([getKit(id), capabilitiesFor(user.id)]);
  if (!kit) notFound();
  const site = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3107";
  return (
    <div className="mx-auto max-w-5xl px-4 pb-24 pt-8 sm:px-6">
      <nav className="mb-3 text-sm text-muted"><Link href="/kits" className="hover:text-text">Kits</Link> / {kit.name}</nav>
      <h1 className="text-2xl font-semibold tracking-tight">{kit.name}</h1>
      <p className="mt-1 text-sm text-muted">{kit.pinnedRelease ? `Pinned to release ${kit.pinnedRelease}` : "No release pinned"} · current version v{kit.currentVersion} · embed ID <code className="font-mono">{kit.embedId}</code> (public identifier, not a secret)</p>
      <KitManager kit={kit} caps={{ customIcons: caps.customIcons, hostedKits: caps.hostedKits, plan: caps.plan }} site={site} />
    </div>
  );
}
