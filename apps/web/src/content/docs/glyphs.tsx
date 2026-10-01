import Link from "next/link";
import type { DocMeta } from "./types";

export const meta: DocMeta = {
  slug: "glyphs",
  title: "Glyphs and codepoints",
  description: "Private Use Area codepoints, the BMP mirror, and pasting glyphs when ligatures are unavailable.",
  section: "Reference",
  order: 3,
};

export default function Page() {
  return (
    <>
      <h1>{meta.title}</h1>
      <p>
        Ligatures are the easiest way to use the fonts, but every icon also has its own character in the Unicode Private Use
        Area (PUA). Use that character when an app ignores ligatures, when you need a single character (for example in a
        spreadsheet cell or a CSS <code>content</code> value), or when you want the icon to survive retyping.
      </p>

      <h2 id="ranges">Codepoint ranges</h2>
      <div style={{ overflowX: "auto" }}>
        <table>
          <thead>
            <tr><th>Set</th><th>Range</th><th>Notes</th></tr>
          </thead>
          <tbody>
            <tr><td>Core (Filled, Line, Rounded, Thin)</td><td><code>U+F0000 + n</code></td><td>Plane 15 PUA. Same codepoint in all Core families. Thin has glyphs only for icons with a distinct Thin style.</td></tr>
            <tr><td>Core BMP mirror</td><td><code>U+E000 + n</code></td><td>Permanent copy of the first 6,400 Core concepts in the Basic Multilingual Plane.</td></tr>
            <tr><td>Brands</td><td><code>U+100000 + n</code></td><td>Plane 16 PUA. Only meaningful in the <code>TypeIcon Brands</code> family.</td></tr>
            <tr><td>Kit custom icons</td><td><code>U+10F000 + n</code></td><td>Your private uploads in a <Link href="/docs/subsets">kit</Link>.</td></tr>
          </tbody>
        </table>
      </div>
      <ul>
        <li>Codepoints are permanent. Once assigned, a codepoint is never reused for a different icon in the same set.</li>
        <li>
          The full mapping for each family is in <code>metadata/glyph-maps/&lt;family&gt;.json</code> inside the release
          archive, and <code>metadata/icons.json</code> lists every icon.
        </li>
        <li>TypeIcon does not reuse Font Awesome codepoints. Swapping fonts in an existing Font Awesome document will not map icons across.</li>
      </ul>

      <h2 id="copy">Copying a glyph</h2>
      <ol>
        <li>Open an icon and choose <strong>Copy glyph</strong> in the detail view.</li>
        <li>Paste into a text box.</li>
        <li>Set that text to the matching family, for example <code>TypeIcon Line</code> for a Core icon or <code>TypeIcon Brands</code> for a brand logo.</li>
      </ol>
      <div className="note">
        <p>
          A PUA character has no meaning on its own. It only shows the icon in the family it came from. In any other font it
          appears as an empty box or nothing at all. Core and Brands use separate ranges, so a brand character pasted into a
          Core family (or the reverse) shows an empty box.
        </p>
      </div>

      <h2 id="supplementary">Supplementary characters</h2>
      <p>
        <code>U+F0000</code> and above sit outside the Basic Multilingual Plane. They take 4 bytes in UTF-8 and a surrogate
        pair in UTF-16. Modern software handles this fine; the fonts include a format 12 <code>cmap</code> for these
        characters and we have tested it with HarfBuzz. Some older apps and input methods cannot type or paste them. In
        that case:
      </p>
      <ul>
        <li>For Core icons, use the BMP mirror at <code>U+E000 + n</code>.</li>
        <li>For brand logos, build a small <Link href="/docs/subsets">subset or kit</Link> font, or use <Link href="/docs/svg">SVG</Link>.</li>
      </ul>

      <h2 id="css">In CSS</h2>
      <p>The web CSS uses the same codepoints for its icon classes, so they work without ligature support:</p>
      <pre><code>{`.typeicon-home::before { content: "\\F0023"; }
.typeicon-brand-github::before { content: "\\100444"; }`}</code></pre>
      <p>
        See <Link href="/docs/web">Web fonts and CSS</Link> for the markup.
      </p>
    </>
  );
}
