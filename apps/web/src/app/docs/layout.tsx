import Link from "next/link";
import { docs } from "@/content/docs";

export default function DocsLayout({ children }: LayoutProps<"/docs">) {
  const sections = ["Start", "Desktop", "Web", "Reference"] as const;
  return (
    <div className="mx-auto grid max-w-[1200px] gap-10 px-4 pb-24 pt-8 sm:px-6 lg:grid-cols-[220px_1fr]">
      <nav aria-label="Documentation" className="lg:sticky lg:top-20 lg:self-start">
        {sections.map((s) => {
          const items = docs.filter((d) => d.meta.section === s).sort((a, b) => a.meta.order - b.meta.order);
          if (!items.length) return null;
          return (
            <div key={s} className="mb-5">
              <h2 className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted">{s}</h2>
              <ul className="space-y-0.5">
                {items.map((d) => (
                  <li key={d.meta.slug}>
                    <Link href={`/docs/${d.meta.slug}`} className="block rounded-lg px-2 py-1.5 text-sm text-text-2 hover:bg-surface-2 hover:text-text">
                      {d.meta.title}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          );
        })}
      </nav>
      <div className="min-w-0">{children}</div>
    </div>
  );
}
