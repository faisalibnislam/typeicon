import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { docs, getDoc } from "@/content/docs";

export function generateStaticParams() {
  return docs.map((d) => ({ slug: d.meta.slug }));
}

export async function generateMetadata(props: PageProps<"/docs/[slug]">): Promise<Metadata> {
  const doc = getDoc((await props.params).slug);
  if (!doc) return {};
  return { title: doc.meta.title, description: doc.meta.description, alternates: { canonical: `/docs/${doc.meta.slug}` } };
}

export default async function DocPage(props: PageProps<"/docs/[slug]">) {
  const doc = getDoc((await props.params).slug);
  if (!doc) notFound();
  const { Page } = doc;
  return (
    <article className="prose-fi max-w-3xl">
      <Page />
    </article>
  );
}
