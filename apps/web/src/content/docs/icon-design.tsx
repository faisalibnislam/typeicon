import Link from "next/link";
import type { DocMeta } from "./types";

export const meta: DocMeta = {
  slug: "icon-design",
  title: "Icon design spec",
  description: "The TypeIcon Core grid, live area, stroke and the rules behind the Filled, Line, Rounded and Thin styles.",
  section: "Reference",
  order: 5,
};

export default function Page() {
  return (
    <>
      <h1>{meta.title}</h1>
      <p>
        This summarizes the rules TypeIcon Core icons are drawn to. Core icons are original artwork. Brand logos come from
        Simple Icons, keep their owners&apos; designs, and are not redrawn to this spec.
      </p>

      <h2 id="grid">Grid</h2>
      <div style={{ overflowX: "auto" }}>
        <table>
          <thead>
            <tr><th>Property</th><th>Value</th></tr>
          </thead>
          <tbody>
            <tr><td>Canvas</td><td>24 × 24</td></tr>
            <tr><td>Live area</td><td>2 to 22 on both axes (20 × 20), leaving 2 units of padding</td></tr>
            <tr><td>Stroke</td><td>2 units (Line, Rounded), 1 unit (Thin)</td></tr>
            <tr><td>Color</td><td><code>currentColor</code> in SVG output</td></tr>
          </tbody>
        </table>
      </div>

      <h2 id="styles">Styles</h2>
      <div style={{ overflowX: "auto" }}>
        <table>
          <thead>
            <tr><th>Style</th><th>Construction</th><th>Caps and joins</th><th>Corners</th></tr>
          </thead>
          <tbody>
            <tr><td>Line</td><td>2-unit outline</td><td>Butt caps, miter joins</td><td>Small radii</td></tr>
            <tr><td>Rounded</td><td>2-unit outline</td><td>Round caps, round joins</td><td>Softer radii</td></tr>
            <tr><td>Thin</td><td>1-unit outline</td><td>Butt caps, miter joins</td><td>Same radii as Line</td></tr>
            <tr><td>Filled</td><td>Solid shapes drawn for the style</td><td>n/a</td><td>n/a</td></tr>
          </tbody>
        </table>
      </div>
      <ul>
        <li>
          <strong>Rounded</strong> describes the stroke terminals and corners. It does not put a rounded square or circle
          container around the icon.
        </li>
        <li>
          <strong>Filled</strong> icons are designed as solid shapes in their own right. They are not the Line outline with
          a fill switched on.
        </li>
        <li>All styles share one name and one codepoint per concept, so switching style never changes the keyword.</li>
        <li>
          <strong>Thin</strong> is Line&apos;s geometry (butt caps, miter joins, the same corner radii) drawn with a 1-unit
          stroke, half the weight of Line. It is published only where it differs from Line. Icons made only of solid
          shapes have no distinct Thin and are not given one.
        </li>
      </ul>

      <h2 id="variants">Variants</h2>
      <p>
        Many Core icons have variants such as <code>file-plus</code>, <code>user-off</code> or <code>bell-lock</code>. A
        variant is its own named icon: the base icon plus a designed badge in the bottom-right corner. The base is cut away
        around the badge with a 1.5-unit gap that follows the badge&apos;s shape, so the badge stays readable at small sizes.
        The <code>off</code> variant uses a diagonal slash instead of a badge.
      </p>
      <ul>
        <li>
          There are 23 badges: plus, minus, check, x, off, lock, search, star, heart, alert, question, clock, settings, edit,
          share, download, upload, refresh, bolt, dollar, code, pause and play.
        </li>
        <li>
          Each category uses a set that makes sense for it (none, minimal, common or full). Math symbols get no variants;
          everyday objects get many.
        </li>
        <li>Every variant has Filled, Line and Rounded styles, like any other Core icon, plus Thin where it differs from Line.</li>
      </ul>

      <h2 id="output">SVG and font parity</h2>
      <p>
        We compare rendered SVG files (resvg) against rendered font glyphs (FreeType); the mean intersection-over-union is
        at least 0.99, so an icon looks the same whether you use it as SVG or as a font. The React and Vue components
        expose <code>strokeWidth</code> for stroke icons if you need a lighter or heavier line; the fonts always use the
        spec stroke.
      </p>

      <h2 id="custom">Designing custom icons for a kit</h2>
      <p>
        If you upload your own icons to a <Link href="/docs/subsets">kit</Link>, draw them on the same 24 × 24 grid inside
        the 2 to 22 live area so they sit well next to Core icons. Uploads are sanitized and checked before they are
        accepted, including a name-collision check.
      </p>
    </>
  );
}
