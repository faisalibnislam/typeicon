import Link from "next/link";
import type { DocMeta } from "./types";

export const meta: DocMeta = {
  slug: "web",
  title: "Web fonts and CSS",
  description: "Self-host the WOFF2 fonts and use TypeIcon icons with CSS classes or ligatures.",
  section: "Web",
  order: 1,
};

export default function Page() {
  return (
    <>
      <h1>{meta.title}</h1>
      <p>
        The web build is plain CSS plus WOFF2 and WOFF files that you host yourself. For new interfaces, inline{" "}
        <Link href="/docs/svg">SVG</Link> or the <Link href="/docs/react">React</Link> and <Link href="/docs/vue">Vue</Link>{" "}
        components are usually a better fit. Reach for the font when you want icons that behave like text.
      </p>

      <h2 id="setup">Setup</h2>
      <ol>
        <li>
          Download the web archive from <Link href="/downloads">Downloads</Link>. You need the <code>css/</code> and{" "}
          <code>webfonts/</code> folders.
        </li>
        <li>
          Copy both folders into your static files, keeping them side by side. The CSS loads fonts from{" "}
          <code>../webfonts/</code>.
        </li>
        <li>Link the stylesheets you use:</li>
      </ol>
      <pre><code>{`<!-- Core: Filled, Line, Rounded, Thin, plus the shared .typeicon base and utility classes -->
<link rel="stylesheet" href="/css/typeicon.css">

<!-- Optional: brand logos (needs typeicon.css for the base classes) -->
<link rel="stylesheet" href="/css/typeicon-simple-icons.css">`}</code></pre>
      <p>
        Each <code>@font-face</code> rule lists WOFF2 first and WOFF second and uses <code>font-display: block</code>, so the
        browser briefly hides the icon until the font arrives instead of flashing the keyword text.
      </p>

      <h2 id="markup">Markup</h2>
      <p>Every icon needs the base class <code>typeicon</code> and a family class. Then choose one of two ways to pick the icon.</p>

      <h3>Codepoint classes (recommended)</h3>
      <pre><code>{`<span class="typeicon typeicon-line typeicon-home" aria-hidden="true"></span>`}</code></pre>
      <p>
        The <code>typeicon-home</code> class inserts the icon&apos;s codepoint with <code>::before</code>. It works even where
        ligatures are disabled, and there is no keyword text for screen readers or copy-paste to pick up.
      </p>

      <h3>Ligatures</h3>
      <pre><code>{`<span class="typeicon typeicon-line" aria-hidden="true">home</span>`}</code></pre>
      <p>
        The text inside the span is the keyword. The <code>.typeicon</code> class turns on <code>liga</code> and{" "}
        <code>rlig</code> and resets letter-spacing and text-transform so the keyword is not altered by surrounding styles.
        Always keep <code>aria-hidden=&quot;true&quot;</code>, otherwise assistive technology reads the word aloud.
      </p>

      <h2 id="families">Family classes</h2>
      <div style={{ overflowX: "auto" }}>
        <table>
          <thead>
            <tr><th>Class</th><th>Font family</th><th>Stylesheet</th></tr>
          </thead>
          <tbody>
            <tr><td><code>typeicon-filled</code></td><td>TypeIcon Filled</td><td rowSpan={4}><code>typeicon.css</code></td></tr>
            <tr><td><code>typeicon-line</code></td><td>TypeIcon Line</td></tr>
            <tr><td><code>typeicon-rounded</code></td><td>TypeIcon Rounded</td></tr>
            <tr><td><code>typeicon-thin</code></td><td>TypeIcon Thin</td></tr>
            <tr><td><code>typeicon-brands</code></td><td>TypeIcon Brands</td><td><code>typeicon-simple-icons.css</code></td></tr>
          </tbody>
        </table>
      </div>
      <p>Brand logos use their full <code>brand-</code> name in the codepoint class:</p>
      <pre><code>{`<span class="typeicon typeicon-brands typeicon-brand-github" aria-hidden="true"></span>`}</code></pre>
      <p>
        Brand logos are trademarks of their owners. Use them only to refer to that brand, and follow its brand guidelines.
      </p>

      <h2 id="utilities">Utility classes</h2>
      <div style={{ overflowX: "auto" }}>
        <table>
          <thead>
            <tr><th>Class</th><th>Effect</th></tr>
          </thead>
          <tbody>
            <tr><td><code>typeicon-fw</code></td><td>Fixed width, for aligning icons in lists and menus</td></tr>
            <tr><td><code>typeicon-xs</code>, <code>typeicon-sm</code>, <code>typeicon-lg</code></td><td>Smaller or larger relative to the surrounding text</td></tr>
            <tr><td><code>typeicon-2x</code> to <code>typeicon-5x</code></td><td>Multiples of the current font size</td></tr>
            <tr><td><code>typeicon-rotate-90</code>, <code>typeicon-rotate-180</code>, <code>typeicon-rotate-270</code></td><td>Rotation</td></tr>
            <tr><td><code>typeicon-flip-horizontal</code>, <code>typeicon-flip-vertical</code>, <code>typeicon-flip-both</code></td><td>Mirroring</td></tr>
            <tr><td><code>typeicon-spin</code></td><td>Continuous rotation; turned off when the user prefers reduced motion</td></tr>
            <tr><td><code>typeicon-sr-only</code></td><td>Visually hidden text that screen readers still announce</td></tr>
          </tbody>
        </table>
      </div>
      <p>
        Icons inherit <code>color</code> and <code>font-size</code> from their parent, and <code>.typeicon</code> sets{" "}
        <code>vertical-align: -0.125em</code> so they sit on the text baseline.
      </p>

      <h2 id="buttons">Icon buttons</h2>
      <pre><code>{`<button type="button">
  <span class="typeicon typeicon-line typeicon-search" aria-hidden="true"></span>
  <span class="typeicon-sr-only">Search</span>
</button>`}</code></pre>
      <p>
        More patterns are in <Link href="/docs/accessibility">Accessibility</Link>. Working examples ship in the release
        archive as <code>examples/css-classes.html</code> and <code>examples/ligatures.html</code>.
      </p>

      <h2 id="size">Keeping it small</h2>
      <p>
        The Brands font contains thousands of logos, and the Core fonts grow with every release. If you only need a few
        dozen icons, build a{" "}
        <Link href="/docs/subsets">custom subset</Link> with just those icons.
      </p>
    </>
  );
}
