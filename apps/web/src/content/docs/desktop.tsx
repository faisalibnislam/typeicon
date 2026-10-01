import Link from "next/link";
import type { DocMeta } from "./types";

export const meta: DocMeta = {
  slug: "desktop",
  title: "Desktop fonts",
  description: "Install the TypeIcon OTF fonts and type icon names as ligatures in design and office apps.",
  section: "Desktop",
  order: 1,
};

export default function Page() {
  return (
    <>
      <h1>{meta.title}</h1>
      <p>
        Every TypeIcon family is a real OpenType font with ligatures. Install it, pick the family, type <code>home</code>, and
        the word turns into the home icon. Nothing else is required: no plugin, no copy-paste of special characters.
      </p>

      <h2 id="families">Font families</h2>
      <p>
        Each style is a separate family with one <strong>Regular</strong> style. Filled, Line, Rounded and Thin are families, not
        weights, so you switch style by changing the font family, not the weight menu.
      </p>
      <div style={{ overflowX: "auto" }}>
        <table>
          <thead>
            <tr><th>Family name</th><th>Contents</th><th>License</th></tr>
          </thead>
          <tbody>
            <tr><td><code>TypeIcon Filled</code></td><td>TypeIcon Core, Filled style</td><td>See <code>licenses/</code></td></tr>
            <tr><td><code>TypeIcon Line</code></td><td>TypeIcon Core, Line style</td><td>See <code>licenses/</code></td></tr>
            <tr><td><code>TypeIcon Rounded</code></td><td>TypeIcon Core, Rounded style</td><td>See <code>licenses/</code></td></tr>
            <tr><td><code>TypeIcon Thin</code></td><td>TypeIcon Core, Thin style (only icons whose Thin differs from Line)</td><td>See <code>licenses/</code></td></tr>
            <tr><td><code>TypeIcon Brands</code></td><td>Brand logos from Simple Icons (one style)</td><td>CC0-1.0 collection; per-logo terms in <code>licenses/</code></td></tr>
          </tbody>
        </table>
      </div>
      <p>
        The Filled, Line and Rounded families contain the same icons, so any Core keyword works in all three. TypeIcon Thin contains only the icons that have a distinct Thin style; other keywords show as plain text in it. Glyph counts for each
        family are listed on <Link href="/downloads">Downloads</Link> and in <code>metadata/manifest.json</code> inside the
        release. Brand logos are trademarks of their owners: use them only to refer to that brand and follow its
        guidelines. Simple Icons releases the collection under CC0, but some logos carry their own license; those are
        listed in <code>licenses/simple-icons/PER-ICON-LICENSES.md</code>.
      </p>

      <h2 id="download">Download</h2>
      <p>
        Get the fonts from <Link href="/downloads">Downloads</Link>. You can take the complete archive, the desktop archive
        with every family, or a single-family desktop zip. Desktop fonts live in the <code>desktop/</code> folder and come
        as OTF (CFF outlines) and TTF. Use the <strong>OTF</strong> unless an app only accepts TTF. The WOFF and WOFF2 files
        in <code>webfonts/</code> are for browsers and should not be installed on your computer.
      </p>
      <p>To confirm the download is intact, run this in the unzipped folder:</p>
      <pre><code>shasum -a 256 -c checksums.sha256</code></pre>

      <h2 id="install">Install</h2>
      <h3>macOS</h3>
      <ol>
        <li>Double-click a file such as <code>TypeIconLine-Regular.otf</code>.</li>
        <li>In Font Book, click <strong>Install Font</strong>. You can also copy the files to <code>~/Library/Fonts</code>.</li>
        <li>Quit and reopen any app that should see the new font.</li>
      </ol>
      <h3>Windows</h3>
      <ol>
        <li>Right-click the OTF file.</li>
        <li>Choose <strong>Install</strong> (just you) or <strong>Install for all users</strong>.</li>
        <li>Restart the apps you want to use it in.</li>
      </ol>
      <div className="note">
        <p>
          <strong>Untested:</strong> installation through macOS Font Book and on Windows has not been checked by us yet.
          See <Link href="/docs/compatibility">Compatibility</Link> for the test steps and current status.
        </p>
      </div>

      <h2 id="typing">Typing icons</h2>
      <ol>
        <li>Create a text box and set the font to the exact family, for example <code>TypeIcon Line</code>.</li>
        <li>Make sure ligatures are turned on. Most apps enable standard ligatures by default; some hide the switch in an OpenType or typography panel.</li>
        <li>Type the icon name in lowercase: <code>home</code>, <code>arrow-right</code>, <code>settings</code>.</li>
      </ol>

      <h3>Keyword rules</h3>
      <ul>
        <li>Names are lowercase ASCII in kebab-case and at least two characters long.</li>
        <li>Matching is case-sensitive. <code>Home</code> stays as the letters H-o-m-e.</li>
        <li>
          Core families also accept a few explicit aliases, for example <code>house</code>, <code>gear</code>,{" "}
          <code>cog</code>, <code>magnify</code>, <code>find</code>, <code>times</code> and <code>pencil</code>.
        </li>
        <li>
          <code>TypeIcon Brands</code> accepts both the full name (<code>brand-github</code>) and the short name
          (<code>github</code>).
        </li>
        <li>
          The longest name wins. <code>arrow</code>, <code>arrow-right</code> and <code>arrow-right-circle</code> each resolve
          to their own icon.
        </li>
        <li>An unknown or unfinished word such as <code>hom</code> stays readable as plain letters.</li>
        <li>If a glyph is missing from a font, you see an empty box (the <code>.notdef</code> glyph) rather than a wrong icon.</li>
      </ul>
      <p>
        The website search also matches tags and synonyms. Those extra words are for finding icons only; the fonts know
        just the icon names and the explicit aliases. Copy the name shown on the icon page to be sure.
      </p>

      <h3>Keep icons in their own text</h3>
      <p>
        A ligature font replaces any known name it finds, even inside a longer word. Typing <code>homework</code> in an icon
        family gives you the home icon followed by <code>work</code>. To avoid surprises:
      </p>
      <ul>
        <li>Put icons in a dedicated text layer, or in their own run of text set in the icon family.</li>
        <li>Separate several keywords with spaces: <code>home settings search</code>.</li>
        <li>Keep body copy in your regular typeface.</li>
      </ul>

      <h2 id="updating">Updating and duplicates</h2>
      <p>
        Family names stay the same across releases, so updating means replacing the old files with the new ones. Remove the
        previous version first so the system does not keep two copies:
      </p>
      <ul>
        <li>macOS: open Font Book, select the TypeIcon families and choose <strong>Remove</strong>.</li>
        <li>Windows: go to Settings, Personalization, Fonts, open each TypeIcon family and uninstall it.</li>
      </ul>
      <p>
        Then install the new files and restart your apps. If an app still shows the old glyphs, clear its font cache or
        restart the computer. More fixes are in <Link href="/docs/troubleshooting">Troubleshooting</Link>.
      </p>

      <h2 id="next">Next</h2>
      <ul>
        <li><Link href="/docs/figma">Using the fonts in Figma</Link></li>
        <li><Link href="/docs/glyphs">Copying glyphs when ligatures are not available</Link></li>
        <li><Link href="/docs/subsets">Building a smaller subset font</Link></li>
      </ul>
    </>
  );
}
