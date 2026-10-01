import Link from "next/link";
import { requireAdmin } from "@/lib/session";

export const dynamic = "force-dynamic";
export const metadata = { title: "Admin", robots: { index: false, follow: false } };

const NAV = [
  ["/admin", "Overview"],
  ["/admin/packs", "Packs"],
  ["/admin/icons", "Icons"],
  ["/admin/review", "Design review"],
  ["/admin/quality", "Duplicates & gaps"],
  ["/admin/imports", "Imports"],
  ["/admin/releases", "Releases"],
  ["/admin/jobs", "Jobs"],
];

export default async function AdminLayout({ children }: LayoutProps<"/admin">) {
  const admin = await requireAdmin();
  return (
    <div className="mx-auto grid max-w-[1440px] gap-8 px-4 pb-24 pt-6 sm:px-6 lg:grid-cols-[200px_1fr]">
      <nav aria-label="Admin" className="lg:sticky lg:top-20 lg:self-start">
        <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted">Admin</p>
        <ul className="space-y-0.5">
          {NAV.map(([href, label]) => (
            <li key={href}><Link href={href} className="block rounded-lg px-2.5 py-1.5 text-sm text-text-2 hover:bg-surface-2 hover:text-text">{label}</Link></li>
          ))}
        </ul>
        <p className="mt-4 text-xs text-muted">Signed in as {admin.email}</p>
      </nav>
      <div className="min-w-0">{children}</div>
    </div>
  );
}
