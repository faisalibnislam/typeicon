import Link from "next/link";
import type { DocMeta } from "./types";

export const meta: DocMeta = {
  slug: "react",
  title: "React",
  description: "Typed, tree-shakeable React components for every TypeIcon icon.",
  section: "Web",
  order: 3,
};

export default function Page() {
  return (
    <>
      <h1>{meta.title}</h1>
      <p>
        <code>@typeicon/react</code> exposes each icon as its own module that renders inline SVG. You import exactly the
        icons you use; nothing else ends up in your bundle.
      </p>
      <div className="note">
        <p>
          The package is currently a local workspace package in the TypeIcon repository. It has not been published to a
          public npm registry, so add it to your project as a workspace or local dependency for now. React 18 or newer is
          required.
        </p>
      </div>

      <h2 id="usage">Usage</h2>
      <pre><code>{`import Home from "@typeicon/react/line/home";
import Settings from "@typeicon/react/rounded/settings";
import BrandGithub from "@typeicon/react/brands/brand-github";

export function Toolbar() {
  return (
    <nav>
      <Home />
      <Settings size={20} color="tomato" />
      <BrandGithub title="GitHub" />
    </nav>
  );
}`}</code></pre>

      <h3>Import paths</h3>
      <div style={{ overflowX: "auto" }}>
        <table>
          <thead>
            <tr><th>Set</th><th>Pattern</th><th>Example</th></tr>
          </thead>
          <tbody>
            <tr><td>Core</td><td><code>@typeicon/react/&lt;style&gt;/&lt;name&gt;</code></td><td><code>@typeicon/react/filled/home</code></td></tr>
            <tr><td>Brand logos</td><td><code>@typeicon/react/brands/&lt;name&gt;</code></td><td><code>@typeicon/react/brands/brand-github</code></td></tr>
          </tbody>
        </table>
      </div>
      <p>
        Core styles are <code>filled</code>, <code>line</code>, <code>rounded</code> and <code>thin</code> (for example <code>@typeicon/react/thin/home</code>). Thin exists only for icons whose Thin differs from Line. Brand logos have a single style
        and keep their <code>brand-</code> prefix. There is intentionally no barrel import of the whole catalog.
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
            <tr><td><code>strokeWidth</code></td><td>artwork value</td><td>Stroke icons only (Core Line, Rounded and Thin). Not available on Filled icons or brand logos.</td></tr>
            <tr><td><code>className</code></td><td></td><td>Passed to the <code>&lt;svg&gt;</code>.</td></tr>
            <tr><td><code>title</code></td><td></td><td>Accessible name, rendered as <code>&lt;title&gt;</code>.</td></tr>
            <tr><td><code>aria-label</code></td><td></td><td>Accessible name without a tooltip.</td></tr>
            <tr><td><code>ref</code></td><td></td><td>Forwarded to the <code>&lt;svg&gt;</code> element.</td></tr>
          </tbody>
        </table>
      </div>
      <p>Any other standard SVG attribute is passed through to the root element.</p>

      <h2 id="a11y">Accessibility</h2>
      <ul>
        <li>
          With no <code>title</code> or <code>aria-label</code>, the icon is decorative: it renders{" "}
          <code>aria-hidden=&quot;true&quot;</code> and <code>focusable=&quot;false&quot;</code>.
        </li>
        <li>
          With <code>title</code>, it renders <code>role=&quot;img&quot;</code>, a <code>&lt;title&gt;</code> with a unique
          id, and <code>aria-labelledby</code> pointing at it.
        </li>
        <li>With <code>aria-label</code>, it renders <code>role=&quot;img&quot;</code> and uses your label.</li>
      </ul>
      <pre><code>{`import Search from "@typeicon/react/line/search";
import Warning from "@typeicon/react/filled/warning";

// Icon-only button: name the button, keep the icon decorative
<button type="button" aria-label="Search">
  <Search />
</button>

// Standalone meaningful icon
<Warning title="Warning" />`}</code></pre>
      <p>
        More in <Link href="/docs/accessibility">Accessibility</Link>.
      </p>

      <h2 id="bundle">Bundle size</h2>
      <p>
        The package is marked <code>sideEffects: false</code>, and every icon is a separate module. We checked this with a
        production build that imports three icons: the output contained only those three, at about 2.3 KB minified with
        React treated as external.
      </p>

      <h2 id="example">Example</h2>
      <p>
        A small working app ships in the release archive at <code>examples/react/App.tsx</code>. Prefer to drop in plain
        markup instead? See <Link href="/docs/svg">SVG</Link>.
      </p>
    </>
  );
}
