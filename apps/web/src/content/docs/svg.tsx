import Link from "next/link";
import type { DocMeta } from "./types";

export const meta: DocMeta = {
  slug: "svg",
  title: "SVG",
  description: "Use TypeIcon icons as individual SVG files, inline SVG, or an SVG sprite.",
  section: "Web",
  order: 2,
};

export default function Page() {
  return (
    <>
      <h1>{meta.title}</h1>
      <p>
        SVG is the most predictable way to put icons on the web and in design tools. There is no font to load and no
        ligature shaping to go wrong, and each icon is drawn with <code>currentColor</code> so it follows the text color.
      </p>

      <h2 id="files">Individual files</h2>
      <p>
        The release archive (and the per-source SVG zips on <Link href="/downloads">Downloads</Link>) contains one file per
        icon and style:
      </p>
      <pre><code>{`svg/<source>/<style>/<name>.svg

svg/typeicon-core/line/home.svg
svg/typeicon-core/rounded/home.svg
svg/typeicon-core/thin/home.svg
svg/simple-icons/brand/brand-github.svg`}</code></pre>
      <p>
        Sources are <code>typeicon-core</code> (styles <code>filled</code>, <code>line</code>, <code>rounded</code>, <code>thin</code>) and{" "}
        <code>simple-icons</code> for brand logos (style <code>brand</code>). You can also copy an icon&apos;s SVG straight
        from its page on the site. A <code>thin</code> file exists only where Thin differs from Line. Brand logos are trademarks of their owners; use them only to refer to that brand.
      </p>

      <h2 id="inline">Inline SVG</h2>
      <p>Paste the file contents into your HTML. Hide decorative icons from assistive technology:</p>
      <pre><code>{`<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
     fill="none" stroke="currentColor" stroke-width="2"
     aria-hidden="true" focusable="false">
  ...
</svg>`}</code></pre>
      <p>
        If the icon carries meaning on its own, give it <code>role=&quot;img&quot;</code> and a <code>&lt;title&gt;</code>{" "}
        instead. See <Link href="/docs/accessibility">Accessibility</Link>.
      </p>

      <h2 id="sprites">Sprites</h2>
      <p>
        Each source and style also ships as one sprite file, <code>sprites/&lt;source&gt;-&lt;style&gt;.svg</code>, with one{" "}
        <code>&lt;symbol&gt;</code> per icon. Symbol ids follow <code>typeicon-&lt;style&gt;-&lt;name&gt;</code>:
      </p>
      <div style={{ overflowX: "auto" }}>
        <table>
          <thead>
            <tr><th>Sprite file</th><th>Example symbol id</th></tr>
          </thead>
          <tbody>
            <tr><td><code>sprites/typeicon-core-line.svg</code></td><td><code>typeicon-line-home</code></td></tr>
            <tr><td><code>sprites/typeicon-core-filled.svg</code></td><td><code>typeicon-filled-home</code></td></tr>
            <tr><td><code>sprites/typeicon-core-thin.svg</code></td><td><code>typeicon-thin-home</code></td></tr>
            <tr><td><code>sprites/simple-icons-brand.svg</code></td><td><code>typeicon-brand-brand-github</code></td></tr>
          </tbody>
        </table>
      </div>
      <pre><code>{`<svg width="24" height="24" aria-hidden="true" focusable="false">
  <use href="/sprites/typeicon-core-line.svg#typeicon-line-home"></use>
</svg>`}</code></pre>
      <p>
        Serve the sprite from the same origin as the page; browsers do not load external <code>&lt;use&gt;</code>{" "}
        references across origins. A complete example is in <code>examples/svg-sprite.html</code> in the release archive.
      </p>

      <h2 id="design-tools">In design tools</h2>
      <p>
        Most design apps, including Figma, accept pasted or dropped SVG as editable vectors. This is also the fallback when a
        tool does not support ligatures; see <Link href="/docs/figma">Figma</Link>.
      </p>

      <h2 id="frameworks">Frameworks</h2>
      <p>
        For React or Vue, the <Link href="/docs/react">React</Link> and <Link href="/docs/vue">Vue</Link> packages wrap the
        same SVG artwork in typed components.
      </p>
    </>
  );
}
