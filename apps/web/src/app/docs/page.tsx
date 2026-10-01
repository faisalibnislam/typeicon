import type { Metadata } from "next";
import Link from "next/link";
import { docs } from "@/content/docs";

export const metadata: Metadata = { title: "Documentation", description: "Install and use TypeIcon fonts, SVGs and components.", alternates: { canonical: "/docs" } };

export default function DocsIndex() {
  return (
    <article className="prose-fi max-w-3xl">
      <h1>Documentation</h1>
      <p>Guides for desktop keyword fonts, web fonts, SVG and components, plus accessibility and troubleshooting.</p>
      <ul>
        {[...docs].sort((a, b) => a.meta.order - b.meta.order).map((d) => (
          <li key={d.meta.slug}>
            <Link href={`/docs/${d.meta.slug}`}>{d.meta.title}</Link>: {d.meta.description}
          </li>
        ))}
      </ul>
    </article>
  );
}
