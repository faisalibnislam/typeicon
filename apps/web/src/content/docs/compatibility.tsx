import Link from "next/link";
import type { DocMeta } from "./types";

export const meta: DocMeta = {
  slug: "compatibility",
  title: "Compatibility",
  description: "What has been verified, what is untested, and how to test TypeIcon in your own apps.",
  section: "Reference",
  order: 2,
};

export default function Page() {
  return (
    <>
      <h1>{meta.title}</h1>
      <p>
        This page separates what we have actually tested from what we expect to work. &quot;Untested&quot; does not mean
        broken; it means nobody has run the steps yet. Reports are welcome.
      </p>

      <h2 id="verified">Verified</h2>
      <div style={{ overflowX: "auto" }}>
        <table>
          <thead>
            <tr><th>Check</th><th>Tool</th><th>Scope</th></tr>
          </thead>
          <tbody>
            <tr><td>Font file validity</td><td>OpenType Sanitizer 9.2.0 (the validator used by Chrome and Firefox)</td><td>All font files</td></tr>
            <tr>
              <td>Ligature shaping</td>
              <td>HarfBuzz via uharfbuzz 0.56.2</td>
              <td>Every keyword and alias in every family, including prefix collisions, unknown input, the supplementary PUA <code>cmap</code> (format 12) and style switching</td>
            </tr>
            <tr><td>Subset fonts</td><td>HarfBuzz</td><td>Re-shaped independently after subsetting</td></tr>
            <tr><td>SVG vs font artwork</td><td>resvg vs FreeType raster comparison</td><td>Mean IoU of at least 0.99</td></tr>
            <tr><td>Web demo</td><td>Chromium-based browser (Claude desktop app browser pane)</td><td>macOS 27</td></tr>
            <tr><td>React tree-shaking</td><td>Production bundle</td><td>3 imported icons, only those 3 in output (about 2.3 KB minified, React external)</td></tr>
          </tbody>
        </table>
      </div>

      <h2 id="matrix">App matrix</h2>
      <div style={{ overflowX: "auto" }}>
        <table>
          <thead>
            <tr><th>App or platform</th><th>Status</th><th>How to test</th></tr>
          </thead>
          <tbody>
            <tr><td>Chromium-based browsers (web fonts)</td><td>Verified (macOS)</td><td>Open <code>examples/ligatures.html</code> and <code>examples/css-classes.html</code></td></tr>
            <tr><td>Safari</td><td>Untested</td><td>Open both example pages; check icons, then toggle reduced motion and confirm <code>typeicon-spin</code> stops</td></tr>
            <tr><td>Firefox</td><td>Untested</td><td>Same as Safari</td></tr>
            <tr><td>macOS Font Book installation</td><td>Untested</td><td>Double-click <code>TypeIconLine-Regular.otf</code>, click Install Font, confirm Font Book shows the family without warnings</td></tr>
            <tr><td>Windows installation</td><td>Untested</td><td>Right-click the OTF, Install, then confirm it appears in Settings, Personalization, Fonts</td></tr>
            <tr><td>Figma desktop</td><td>Untested</td><td>See <Link href="/docs/figma">Figma</Link>, then run the ligature test below</td></tr>
            <tr><td>Figma in the browser</td><td>Untested</td><td>Install Figma&apos;s font installer, reload, then run the ligature test</td></tr>
            <tr><td>Sketch</td><td>Untested</td><td>Ligature test in a text layer</td></tr>
            <tr><td>Adobe Illustrator</td><td>Untested</td><td>Ligature test; check the OpenType panel if ligatures do not apply</td></tr>
            <tr><td>Affinity Designer</td><td>Untested</td><td>Ligature test; check the Typography panel if ligatures do not apply</td></tr>
            <tr><td>Apple Keynote and Pages</td><td>Untested</td><td>Ligature test in a text box</td></tr>
            <tr><td>Microsoft Word and PowerPoint</td><td>Untested</td><td>Ligature test; note whether ligatures apply by default or need to be enabled</td></tr>
          </tbody>
        </table>
      </div>

      <h2 id="ligature-test">Ligature test</h2>
      <p>Run this in any app you want to check. Use <code>TypeIcon Line</code> unless noted.</p>
      <ol>
        <li>Type <code>home</code>: expect one home icon.</li>
        <li>Type <code>arrow arrow-right arrow-right-circle</code>: expect three different icons.</li>
        <li>Type <code>house</code>: expect the home icon (alias).</li>
        <li>Type <code>Home</code> and <code>hom</code>: expect plain letters.</li>
        <li>Switch the text to <code>TypeIcon Filled</code>, <code>TypeIcon Rounded</code> and <code>TypeIcon Thin</code>: the icons change style (Thin shows plain text for icons that have no distinct Thin).</li>
        <li>In <code>TypeIcon Brands</code>, type <code>brand-github</code> and <code>github</code>: both should give the GitHub logo.</li>
        <li>Paste a glyph copied with <strong>Copy glyph</strong>: expect the icon in the matching family.</li>
      </ol>
      <p>Record the app version, operating system and result for each step.</p>

      <h2 id="known-limits">Known limitations</h2>
      <ul>
        <li>A known name inside a longer word is substituted (<code>homework</code> gives the home icon plus &quot;work&quot;).</li>
        <li>Some older software cannot enter characters above <code>U+FFFF</code>. Use the Core BMP mirror or a subset font; see <Link href="/docs/glyphs">Glyphs and codepoints</Link>.</li>
        <li>No codepoint compatibility with Font Awesome.</li>
      </ul>
    </>
  );
}
