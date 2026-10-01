import Link from "next/link";
import type { DocMeta } from "./types";

export const meta: DocMeta = {
  slug: "installation",
  title: "Installation overview",
  description: "Choose how to use TypeIcon: desktop fonts, web fonts, SVG, or framework components.",
  section: "Start",
  order: 1,
};

export default function Page() {
  return (
    <>
      <h1>{meta.title}</h1>
      <p>TypeIcon ships the same icons in several forms. Pick the one that fits where you are working.</p>
      <table>
        <thead>
          <tr><th>You want to…</th><th>Use</th><th>Guide</th></tr>
        </thead>
        <tbody>
          <tr><td>Type icons in Figma, Sketch, Keynote or Word</td><td>Desktop OTF fonts</td><td><Link href="/docs/desktop">Desktop fonts</Link></td></tr>
          <tr><td>Build a new web interface</td><td>Inline SVG or React/Vue components</td><td><Link href="/docs/svg">SVG</Link>, <Link href="/docs/react">React</Link>, <Link href="/docs/vue">Vue</Link></td></tr>
          <tr><td>Use icons as text on the web</td><td>WOFF2 + CSS</td><td><Link href="/docs/web">Web fonts and CSS</Link></td></tr>
        </tbody>
      </table>
    </>
  );
}
