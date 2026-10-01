import Link from "next/link";
import type { DocMeta } from "./types";

export const meta: DocMeta = {
  slug: "subsets",
  title: "Custom subsets and kits",
  description: "Build a font with only the icons you need, and save it as a versioned kit with optional custom icons.",
  section: "Start",
  order: 2,
};

export default function Page() {
  return (
    <>
      <h1>{meta.title}</h1>
      <p>
        The full fonts hold every icon in a release, and the Brands font alone has thousands of logos. A subset contains only
        the icons you pick, which keeps web fonts small and makes desktop fonts easier to share with a team.
      </p>

      <h2 id="builder">Subset builder</h2>
      <p>
        Open <Link href="/downloads/subset">/downloads/subset</Link>.
      </p>
      <ol>
        <li>Select icons. They collect in the tray at the bottom of the screen, and the tray keeps your selection as you move between pages.</li>
        <li>Choose the styles to include.</li>
        <li>Choose formats: OTF, TTF, WOFF2, WOFF, SVG and CSS.</li>
        <li>Give the project a name.</li>
        <li>Review the licenses of the sources you selected.</li>
        <li>Start the build.</li>
      </ol>
      <p>
        The build moves through <strong>queued</strong>, <strong>running</strong>, and then <strong>succeeded</strong> (with a
        download link) or <strong>failed</strong>. Builds run in a background worker, never inside the web request. Build rate limits apply.
      </p>

      <h2 id="names">Family names</h2>
      <p>
        Subset fonts get their own family names, made from the project slug and a content hash, for example:
      </p>
      <pre><code>TypeIcon Kit acme a1b2c3 Line</code></pre>
      <p>
        Two different subsets therefore never share a name, and installing one cannot overwrite another in a font cache.
        In our verification, subset fonts are re-shaped independently with HarfBuzz to confirm their ligatures still work.
      </p>

      <h2 id="caching">Caching</h2>
      <p>
        An identical request returns the previous result instead of rebuilding. The cache key is a hash of the selection,
        the asset versions, the toolchain and the access scope. Builds that include private custom icons never share a
        cache entry with public builds.
      </p>

      <h2 id="kits">Kits</h2>
      <p>
        A kit is a saved subset project. Kits live at <Link href="/kits">/kits</Link> and require signing in.
      </p>
      <ul>
        <li><strong>Versions:</strong> each kit version is immutable and pinned to a catalog release, so a build you shipped does not change under you.</li>
        <li>
          <strong>Custom icons:</strong> you can upload your own SVGs. Uploads are sanitized, checked for outlines, and
          checked for name collisions with existing icons. They are private to your kit and use codepoints from{" "}
          <code>U+10F000</code>.
        </li>
        <li><strong>Hosted CSS:</strong> optionally, a kit can be served as a hosted CSS embed.</li>
      </ul>
      <div className="note">
        <p>
          The kit embed ID is public, not a secret: anyone who views your site can see it. Domain restrictions are usage
          controls. They do not protect font files that are delivered publicly to browsers, so do not put anything
          confidential in a hosted kit.
        </p>
      </div>

      <h2 id="related">Related</h2>
      <ul>
        <li><Link href="/docs/glyphs">Glyphs and codepoints</Link></li>
        <li><Link href="/docs/web">Web fonts and CSS</Link></li>
        <li><Link href="/docs/desktop">Desktop fonts</Link></li>
      </ul>
    </>
  );
}
