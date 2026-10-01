import Link from "next/link";
import type { DocMeta } from "./types";

export const meta: DocMeta = {
  slug: "troubleshooting",
  title: "Troubleshooting",
  description: "Fixes for keywords that stay as text, empty boxes, wrong icons, duplicate fonts and web font issues.",
  section: "Reference",
  order: 4,
};

export default function Page() {
  return (
    <>
      <h1>{meta.title}</h1>

      <h2 id="stays-text">The keyword stays as text</h2>
      <ul>
        <li>Check the font. The text must use the exact family, such as <code>TypeIcon Line</code>, not a similarly named font.</li>
        <li>Check the spelling. Keywords are lowercase kebab-case: <code>arrow-right</code>, not <code>Arrow Right</code> or <code>arrow_right</code>.</li>
        <li>Check that the name exists in that family. Search tags on the website are broader than font keywords; use the icon name or one of its explicit aliases.</li>
        <li>Check that ligatures are enabled in the app&apos;s OpenType or typography settings.</li>
        <li>Restart the app after installing the font.</li>
        <li>If the app does not support ligatures at all, paste the glyph instead (<Link href="/docs/glyphs">Glyphs and codepoints</Link>) or use <Link href="/docs/svg">SVG</Link>.</li>
      </ul>

      <h2 id="box">An empty box appears</h2>
      <p>
        An empty box is the font&apos;s <code>.notdef</code> glyph: the character is not in this font. Common causes:
      </p>
      <ul>
        <li>You pasted a copied glyph into a different family. PUA characters only work in the family they came from; a brand logo needs <code>TypeIcon Brands</code>.</li>
        <li>You are using a subset font that does not include that icon.</li>
        <li>The app substituted another font because the TypeIcon family is not installed on this machine.</li>
      </ul>

      <h2 id="wrong-icon">An icon appears in the middle of a word</h2>
      <p>
        Ligature fonts substitute any known name, even inside longer words: <code>homework</code> becomes the home icon plus{" "}
        <code>work</code>. Keep icons in their own text layer or run, and set body text in your normal typeface.
      </p>

      <h2 id="brand-styles">Brand logos have only one style</h2>
      <p>
        Brand logos come in a single <code>brand</code> style in the <code>TypeIcon Brands</code> family. They have no
        Filled, Line, Rounded or Thin versions, and TypeIcon does not generate them. Brand keywords do not work in the Core
        families, and Core keywords do not work in <code>TypeIcon Brands</code>.
      </p>

      <h2 id="old-version">Old icons or duplicate fonts</h2>
      <ol>
        <li>Quit the apps that use the font.</li>
        <li>Remove every older TypeIcon version: in Font Book select the families and choose <strong>Remove</strong>; on Windows use Settings, Personalization, Fonts.</li>
        <li>Install the new files. Family names do not change between releases, so this is the normal update path.</li>
        <li>If the old glyphs persist, clear the app&apos;s font cache or restart the computer.</li>
      </ol>

      <h2 id="collaborators">Collaborators see text instead of icons</h2>
      <p>
        Every person needs the same release installed. For files leaving your team, convert icons to vectors (in Figma,{" "}
        <strong>Flatten</strong>) or use SVG. See <Link href="/docs/figma">Figma</Link>.
      </p>

      <h2 id="cannot-type">An app cannot enter the character</h2>
      <p>
        Codepoints from <code>U+F0000</code> upward are supplementary characters. Some older software cannot type or paste
        them. Use the Core BMP mirror (<code>U+E000 + n</code>) or build a small subset font.
      </p>

      <h2 id="web">Web: icons missing or showing the keyword</h2>
      <ul>
        <li>Make sure the <code>css/</code> and <code>webfonts/</code> folders sit side by side; the CSS loads <code>../webfonts/</code>.</li>
        <li>Check the browser network panel for 404s on <code>.woff2</code> files, and that your server sends fonts with a font MIME type.</li>
        <li>If you load fonts from another origin, the server must send CORS headers for them.</li>
        <li>Every icon needs both <code>typeicon</code> and a family class, for example <code>typeicon typeicon-line typeicon-home</code>.</li>
        <li>Brand logos also need <code>typeicon-simple-icons.css</code> and the <code>typeicon-brands</code> family class, for example <code>typeicon typeicon-brands typeicon-brand-github</code>.</li>
        <li>If ligature markup shows the word, a parent style may override <code>font-feature-settings</code>. Switch to codepoint classes.</li>
      </ul>

      <h2 id="verify">Corrupted download</h2>
      <p>Run this inside the unzipped release folder. Every line should end in <code>OK</code>.</p>
      <pre><code>shasum -a 256 -c checksums.sha256</code></pre>

      <h2 id="more">Still stuck</h2>
      <p>
        Check <Link href="/docs/compatibility">Compatibility</Link> to see whether your app has been tested, and include the
        app version, operating system and the exact text you typed when reporting a problem.
      </p>
    </>
  );
}
