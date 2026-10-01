import Link from "next/link";
import type { DocMeta } from "./types";

export const meta: DocMeta = {
  slug: "accessibility",
  title: "Accessibility",
  description: "Decorative and meaningful icons, icon-only buttons, ligature markup and reduced motion.",
  section: "Reference",
  order: 1,
};

export default function Page() {
  return (
    <>
      <h1>{meta.title}</h1>
      <p>
        An icon is either decorative (the text next to it already says the same thing) or meaningful (it is the only way
        the information is shown). Decide which before choosing the markup.
      </p>

      <h2 id="summary">At a glance</h2>
      <div style={{ overflowX: "auto" }}>
        <table>
          <thead>
            <tr><th>Situation</th><th>What to do</th></tr>
          </thead>
          <tbody>
            <tr><td>Icon next to visible text</td><td>Hide the icon: <code>aria-hidden=&quot;true&quot;</code></td></tr>
            <tr><td>Icon-only button or link</td><td>Name the button (<code>aria-label</code> or <code>typeicon-sr-only</code> text); hide the icon</td></tr>
            <tr><td>Standalone icon that carries meaning</td><td>Give the icon a text alternative (<code>title</code>, or <code>role=&quot;img&quot;</code> plus a label)</td></tr>
            <tr><td>Ligature markup</td><td>Always hide the span; the keyword would otherwise be read aloud</td></tr>
            <tr><td>Animated icon</td><td><code>typeicon-spin</code> stops automatically under reduced motion</td></tr>
          </tbody>
        </table>
      </div>

      <h2 id="decorative">Decorative icons</h2>
      <pre><code>{`<a href="/settings">
  <span class="typeicon typeicon-line typeicon-settings" aria-hidden="true"></span>
  Settings
</a>`}</code></pre>
      <p>
        The React and Vue components do this for you: with no <code>title</code> or <code>aria-label</code> they render{" "}
        <code>aria-hidden=&quot;true&quot;</code> and <code>focusable=&quot;false&quot;</code>.
      </p>

      <h2 id="buttons">Icon-only buttons</h2>
      <p>
        Put the accessible name on the interactive element, not on the icon. Either works:
      </p>
      <pre><code>{`<button type="button" aria-label="Close">
  <span class="typeicon typeicon-line typeicon-close" aria-hidden="true"></span>
</button>

<button type="button">
  <span class="typeicon typeicon-line typeicon-close" aria-hidden="true"></span>
  <span class="typeicon-sr-only">Close</span>
</button>`}</code></pre>
      <p>
        Visually hidden text (<code>typeicon-sr-only</code>) is also picked up by browser translation tools, which is a small
        advantage over <code>aria-label</code>. Consider a visible tooltip for sighted users who do not recognise the icon.
      </p>

      <h2 id="meaningful">Meaningful standalone icons</h2>
      <pre><code>{`<!-- CSS font -->
<span class="typeicon typeicon-filled typeicon-warning" aria-hidden="true"></span>
<span class="typeicon-sr-only">Warning</span>

<!-- React / Vue -->
<Warning title="Warning" />`}</code></pre>
      <p>
        With <code>title</code>, the components render <code>role=&quot;img&quot;</code>, a <code>&lt;title&gt;</code> and{" "}
        <code>aria-labelledby</code>. For inline SVG, add those yourself.
      </p>

      <h2 id="ligatures">Ligature markup</h2>
      <p>
        With ligatures, the DOM contains the literal keyword, for example <code>home</code>. The font draws an icon, but a
        screen reader still sees the word, and copy-paste or search picks it up too. Always add{" "}
        <code>aria-hidden=&quot;true&quot;</code> to ligature spans and provide the real label separately. Where possible,
        use codepoint classes or SVG instead; see <Link href="/docs/web">Web fonts and CSS</Link>.
      </p>

      <h2 id="motion">Reduced motion</h2>
      <p>
        <code>typeicon-spin</code> is disabled when the user has <code>prefers-reduced-motion: reduce</code> set. If you animate
        icons yourself, follow the same rule.
      </p>

      <h2 id="contrast">Color and contrast</h2>
      <p>
        Icons inherit the text color. Icons that convey information should meet the same non-text contrast you use for
        other UI elements, and should not rely on color alone to communicate state.
      </p>
    </>
  );
}
