import Link from "next/link";
import type { DocMeta } from "./types";

export const meta: DocMeta = {
  slug: "vue",
  title: "Vue",
  description: "Typed, tree-shakeable Vue 3 components for every TypeIcon icon.",
  section: "Web",
  order: 4,
};

export default function Page() {
  return (
    <>
      <h1>{meta.title}</h1>
      <p>
        <code>@typeicon/vue</code> mirrors the <Link href="/docs/react">React package</Link>: one module per icon, each
        rendering inline SVG, with the same import paths and props.
      </p>
      <div className="note">
        <p>
          The package is currently a local workspace package in the TypeIcon repository and is not published to a public
          npm registry. Add it as a workspace or local dependency. It requires Vue 3.5 or newer.
        </p>
      </div>

      <h2 id="usage">Usage</h2>
      <pre><code>{`<script setup lang="ts">
import Home from "@typeicon/vue/line/home";
import Settings from "@typeicon/vue/rounded/settings";
import BrandGithub from "@typeicon/vue/brands/brand-github";
</script>

<template>
  <nav>
    <Home />
    <Settings :size="20" color="tomato" />
    <BrandGithub title="GitHub" />
  </nav>
</template>`}</code></pre>

      <h3>Import paths</h3>
      <div style={{ overflowX: "auto" }}>
        <table>
          <thead>
            <tr><th>Set</th><th>Pattern</th><th>Example</th></tr>
          </thead>
          <tbody>
            <tr><td>Core</td><td><code>@typeicon/vue/&lt;style&gt;/&lt;name&gt;</code></td><td><code>@typeicon/vue/filled/home</code></td></tr>
            <tr><td>Brand logos</td><td><code>@typeicon/vue/brands/&lt;name&gt;</code></td><td><code>@typeicon/vue/brands/brand-github</code></td></tr>
          </tbody>
        </table>
      </div>
      <p>
        Brand logos have a single style and keep their <code>brand-</code> prefix. There is no barrel import of the catalog,
        so only what you import is bundled.
      </p>

      <h2 id="props">Props</h2>
      <div style={{ overflowX: "auto" }}>
        <table>
          <thead>
            <tr><th>Prop</th><th>Default</th><th>Description</th></tr>
          </thead>
          <tbody>
            <tr><td><code>size</code></td><td><code>24</code></td><td>Height in px (number) or any CSS length (string).</td></tr>
            <tr><td><code>color</code></td><td>inherited</td><td>Sets CSS <code>color</code>; the artwork paints with <code>currentColor</code>.</td></tr>
            <tr><td><code>stroke-width</code></td><td>artwork value</td><td>Stroke icons only (Core Line, Rounded and Thin). Ignored on Filled icons and brand logos.</td></tr>
            <tr><td><code>title</code></td><td></td><td>Accessible name, rendered as <code>&lt;title&gt;</code>.</td></tr>
          </tbody>
        </table>
      </div>
      <p>
        Other attributes such as <code>class</code>, <code>aria-label</code> and standard SVG attributes fall through to the{" "}
        <code>&lt;svg&gt;</code>.
      </p>

      <h2 id="a11y">Accessibility</h2>
      <ul>
        <li>
          Without <code>title</code> or <code>aria-label</code>, the icon renders <code>aria-hidden=&quot;true&quot;</code> and{" "}
          <code>focusable=&quot;false&quot;</code>.
        </li>
        <li>
          With <code>title</code>, it renders <code>role=&quot;img&quot;</code>, a <code>&lt;title&gt;</code> with a unique
          id, and <code>aria-labelledby</code>.
        </li>
        <li>With <code>aria-label</code>, it renders <code>role=&quot;img&quot;</code> and uses your label.</li>
      </ul>
      <pre><code>{`<button type="button" aria-label="Search">
  <Search />
</button>`}</code></pre>
      <p>
        See <Link href="/docs/accessibility">Accessibility</Link> for more patterns.
      </p>

      <h2 id="bundle">Bundle size</h2>
      <p>
        The package is marked <code>sideEffects: false</code> and each icon is its own module, so bundlers drop icons you do
        not import. Our measured tree-shaking check was run on the React package; the Vue package uses the same structure.
      </p>

      <h2 id="example">Example</h2>
      <p>
        A working component ships in the release archive at <code>examples/vue/App.vue</code>.
      </p>
    </>
  );
}
