# TypeIcon Core design specification

Status: v0.1 (first 70 concepts). Canonical sources: `assets/core/svg/{filled,line,rounded,thin}/*.svg`.
Design tooling that produced them: `tools/core-authoring/` (geometry helpers + per-icon definitions).

## Grid

| Property | Value |
|---|---|
| Canvas | 24 × 24 |
| Live area | 2–22 (20 × 20). Nothing may leave 0–24; the audit warns on artwork outside the viewBox. |
| Stroke (Line, Rounded) | 2 px (Thin: 1 px), centred on integer coordinates where possible so edges land on the pixel grid |
| Keyshapes | circle Ø18 (r 9), square 18 × 18, portrait 14 × 18, landscape 18 × 14 |
| Detail spacing | Minimum 2 px between separate strokes; knock-outs in Filled are ≥ 1.75 px |
| Small-size rule | Every icon must stay recognisable at 16 px; review at 16, 20, 24, 32, 48 px on light and dark |

## The styles

Fill and corner treatment are separate design dimensions. The Core styles are Filled, Line, Rounded and Thin. Thin is a weight variant of Line that is published only where it differs from Line (see below).

| Style | Definition |
|---|---|
| **Line** | 2 px outline, butt caps, miter joins (miter limit 4; 2 on very acute corners), sharp polyline corners, 2 px container corner radius. Crisp and technical. |
| **Rounded** | The same skeleton as Line with round caps, round joins, 1.5 px fillets on polyline corners and 4 px container corners. Softer terminals and corners. **Not** a rounded container drawn around the icon. |
| **Filled** | Explicitly drawn solid geometry: silhouettes filled to the outer edge of the Line outline, interior detail knocked out as counters (≥ 1.75 px). Pure stroke symbols (check, plus, arrows, chevrons) become heavier solid forms with solid heads. Never produced by switching on `fill` for an outline. |

| **Thin** | Line's geometry (butt caps, miter joins, same corner radii) drawn with a 1 px stroke, half the weight of Line. Published only where it differs from Line: icons made only of solid shapes have no distinct Thin and are not given one. The variant badge gap stays 1.5 px, measured from the thin badge stroke. Never published as identical artwork to Line. |

Relationship: Line and Rounded share one skeleton per concept, so a keyword swaps style cleanly.
Filled shares the outer silhouette of Line, so switching Line ↔ Filled does not shift optical size.
Thin shares Line's skeleton exactly and differs only in stroke weight. Thin does not change the Core goal count,
which counts icons with Filled, Line and Rounded.

## Rules the pipeline enforces

- The styles of a concept must not rasterise identically. The audit renders each pair at 48 px and
  flags IoU ≥ 0.995 (`identical_geometry`). Flagged concepts do not count toward the Core goal. The first
  audit flagged six designs (cloud, eye, heart, map-pin, phone, shield); their Rounded (and, for cloud and
  phone, Line) geometry was redrawn so the styles genuinely differ.
- Directional siblings produced by rotating another design (`arrow-left` = `arrow-right` rotated 180°) are
  recorded as `derivedFrom` and never counted as independent artwork.
- SVG is canonical. Font outlines are derived at build time (strokes expanded at font scale, overlaps
  removed, holes preserved) and compared against the SVG by raster IoU (≥ 0.95 at 96 px for Core).

## Extending the style model

The `styles` table is data, not an enum. Thin was added as the fourth Core style (2026-10-01). Future families (Rounded Filled, Duotone, Sharp) are added as
new style rows plus source-manifest mappings; each becomes its own font family (as `TypeIcon Thin` did), never a
weight of an existing family. Duotone and other multi-tone artwork is SVG-only unless a COLR font workflow is
added deliberately.

## Variants (badges)

A variant is a separately named concept built from a base design and a designed badge, e.g. `file-plus`,
`user-off`, `bell-lock` (`tools/core-authoring/modifiers.py`).

- The badge sits in the bottom-right box (13–23 on both axes); `off` is a full diagonal slash from 3,3 to 21,21.
- The base is cut away around the badge with a shape-following gap of 1.5 px, so the badge reads at 16 px.
  Line/Rounded variants emit the base as its outlined region (gap removed) plus the badge as editable strokes;
  Filled subtracts the gap from the base's Filled design and adds the badge's Filled design.
- Each category picks a modifier set: none, minimal (plus, minus, check, x, off), common (14) or full (23).
  Symbols such as math signs, arrows, shapes and letters take none.
- Designers keep a base's identifying detail out of the bottom-right quadrant where the category takes badges.
- Variants count toward the goal as complete concepts, but are always reported separately from base designs.

## Review

- `/admin/review` renders every design in all styles at 16–48 px on light and dark.
- `typeicon-review-sheets <version>` writes `build/review/core-<style>.png`, placing each canonical SVG (resvg)
  next to its compiled font glyph (FreeType) at the same sizes.
- Human design QA is still required: v0.1 Core artwork was authored with the tooling in this repository and
  approved only by the bootstrap import (see docs/catalog-audit.md license/approval notes).
