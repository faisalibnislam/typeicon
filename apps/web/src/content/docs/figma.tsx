import Link from "next/link";
import type { DocMeta } from "./types";

export const meta: DocMeta = {
  slug: "figma",
  title: "Figma",
  description: "Use TypeIcon ligature fonts in Figma, share files with collaborators, and hand off icons.",
  section: "Desktop",
  order: 2,
};

export default function Page() {
  return (
    <>
      <h1>{meta.title}</h1>
      <div className="note">
        <p>
          <strong>Untested in Figma.</strong> We have verified ligature shaping with HarfBuzz, but not yet inside Figma
          desktop or Figma in the browser. The Figma UI names below come from Figma&apos;s help center as of
          September 2026; the checklist on <Link href="/docs/compatibility">Compatibility</Link> lists the exact test steps.
        </p>
      </div>

      <h2 id="install">1. Install the font</h2>
      <ol>
        <li>
          Install the <strong>OTF</strong> file for the family you want (see <Link href="/docs/desktop">Desktop fonts</Link>).
          Figma reads locally installed <code>.otf</code> and <code>.ttf</code> files. Do not install the WOFF or WOFF2 files;
          those are for websites.
        </li>
        <li>
          <strong>Figma desktop app:</strong> the font installer is built in. Restart the app after installing the font.
        </li>
        <li>
          <strong>Figma in the browser:</strong> install Figma&apos;s font installer (Figma calls it the Figma font
          installer, or FigmaAgent), then reload any open design files.
        </li>
      </ol>
      <p>
        Figma&apos;s instructions: <a href="https://help.figma.com/hc/en-us/articles/360039956894-Add-a-font-to-Figma">Add a font to Figma</a>.
      </p>

      <h2 id="type">2. Type an icon</h2>
      <ol>
        <li>Create or select a text layer.</li>
        <li>
          Open the <strong>Font</strong> menu in the right sidebar. To find the font quickly, use the filter dropdown and pick{" "}
          <strong>Installed by you</strong>, then search for the family.
        </li>
        <li>Choose the exact family, for example <code>TypeIcon Line</code>. Its only style is Regular.</li>
        <li>
          Check that ligatures are on: in the <strong>Typography</strong> section of the properties panel, open the type
          settings and go to the <strong>Details</strong> tab. Under <strong>Letterforms</strong>, make sure{" "}
          <strong>Ligatures</strong> is enabled.
        </li>
        <li>Type the keyword, such as <code>home</code> or <code>arrow-right</code>.</li>
      </ol>
      <p>
        Figma&apos;s instructions:{" "}
        <a href="https://help.figma.com/hc/en-us/articles/4913951097367-Use-OpenType-features">Use OpenType features</a>.
      </p>
      <p>
        Put each icon, or a row of icons separated by spaces, in its own text layer. A known name inside a longer word is
        replaced too, so <code>homework</code> becomes the home icon plus <code>work</code>. Switching a layer between{" "}
        <code>TypeIcon Filled</code>, <code>TypeIcon Line</code>, <code>TypeIcon Rounded</code> and <code>TypeIcon Thin</code> keeps the same
        keyword and changes the style.
      </p>

      <h2 id="collaborators">Collaborators</h2>
      <p>
        Everyone editing the file needs the same TypeIcon release installed. Without it, Figma reports a missing font and
        the layer shows the keyword as plain fallback text.
      </p>

      <h2 id="handoff">Handoff</h2>
      <p>
        If people outside your team will open the file, convert icon text to vector shapes. Select the layer, right-click
        and choose <strong>Flatten</strong>. The icon then looks the same everywhere, but it is no longer editable text:
        you cannot change the keyword or switch the family afterwards. Keep an unflattened copy if you might need to edit
        it later.
      </p>
      <p>
        Figma&apos;s instructions:{" "}
        <a href="https://help.figma.com/hc/en-us/articles/360047239073-Convert-text-to-vector-paths">Convert text to vector paths</a>.
      </p>

      <h2 id="fallbacks">If ligatures do not work</h2>
      <ul>
        <li>
          <strong>Paste the glyph.</strong> In the icon detail view, <strong>Copy glyph</strong> puts the icon&apos;s
          private-use character on your clipboard. Paste it into a text layer set to the matching family. See{" "}
          <Link href="/docs/glyphs">Glyphs and codepoints</Link>.
        </li>
        <li>
          <strong>Use SVG.</strong> Copy or download the SVG from the icon page and paste it into Figma as a vector. See{" "}
          <Link href="/docs/svg">SVG</Link>.
        </li>
        <li>
          <strong>TypeIcon Figma plugin.</strong> Source code lives in <code>packages/figma-plugin</code> in the TypeIcon
          repository. It is not published to the Figma Community and has not been tested inside Figma yet.
        </li>
      </ul>
      <p>
        Still stuck? Check <Link href="/docs/troubleshooting">Troubleshooting</Link>.
      </p>
    </>
  );
}
