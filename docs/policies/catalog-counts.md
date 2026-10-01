# Catalog count policy

TypeIcon's target is **at least 20,000 complete TypeIcon Core concepts, each with approved Filled, Line and
Rounded variants, i.e. ≥60,000 published Core concept/style assets.** Thin is published only where it differs from Line and does not change the target or the counts. A complete concept is either a base design
or a designed variant (see below). This target is not met until `catalog-audit.json` says so.

(The target was 50,000 until 2026-09-30; see `docs/decisions.md`, entry 19.)

## Definitions

| Term | Meaning | Counted from |
|---|---|---|
| **Concept** | A semantic idea (`home`). Shared by designs from different sources for search. | `concepts` with ≥1 published variant |
| **Design** | One source's artwork family for a concept (`home` in Core, `brand-github` in Brands). Has a canonical name. | `designs` with ≥1 published variant |
| **Variant** (style variant) | One design in one actual style (Core `home` / Line). The unit that is downloadable. | `variants` where `status = 'published'` |
| **Alias** | An extra name that resolves to an existing design. Never counted as an icon. | `aliases` |
| **Core base design** | A Core design drawn individually (`file`, `user`, `bell`). | audit |
| **Core variant** (base + badge) | A separately named Core concept built from a base plus a designed badge in the bottom-right corner, cut from the base with a 1.5 px shape-following gap (`file-plus`, `user-off`, `bell-lock`). One of 23 badges; each category's modifier set (none / minimal / common / full) decides which exist. | audit |
| **Complete Core concept** | A Core base design or Core variant with published Filled **and** Line **and** Rounded styles. | audit |
| **Font-supported asset** | A published style variant whose outline passed font conversion and is in a released font. | `glyph_assignments` joined to release |
| **Brand logo** | A published logo from the Brands source (Simple Icons, style `brand`, `area = 'brands'`). Shown and downloadable, **never** counted toward the Core target. | published `designs` with `area = 'brands'` (`is_brand`) |

"Variant" means two different things: a *style variant* (one design in one style) and a *Core variant* (base +
badge concept). Reports say which one they mean.

## Reporting rules

- Core base designs and Core variants are **always reported separately**, alongside their sum. Never publish only
  the sum.
- Brand logos are reported on their own line and never added to Core totals or to the gap.
- Current numbers live in `docs/catalog-audit.md`; other docs point there instead of repeating counts.

## What is never counted

- Renamed duplicates, aliases, deprecated names.
- Flipped, rotated, recoloured or re-exported copies of the same geometry. Rotated directional siblings
  (`arrow-down` from `arrow-right`) are published but do not count. The export detects these from the artwork
  itself (`tools/core-authoring/transforms.py`: Line and Filled rasterised at 32 px, the 8 symmetries of the
  square applied, IoU ≥ 0.97 in both styles), so a sibling drawn by rotating or mirroring coordinates by hand,
  or two names that happen to share one drawing, is recorded as `derivedFrom` whether or not its author marked
  it. Transform-derived designs get no generated variants.
- The same geometry labelled with multiple styles. The audit rasterises each Core concept's styles and flags
  pairs whose masks are identical (IoU ≥ 0.995) as `identical_geometry`. They do not count as complete.
- Mechanically generated fills (`fill` toggled on an outline). Automated proposals are stored with
  `review_status = 'proposed'` and are excluded until approved by a reviewer.
- Brand logos, and any artwork from removed sources (Tabler, Phosphor, Material Symbols).
- Synthetic load-test rows. They live in a separate schema (`loadtest`) and are never read by public queries.
- Quarantined assets (unknown/incompatible license, failed validation).

## Where counts appear

- Home page and `/icons` read `catalog_stats` computed from the same published rows as the catalog query.
- Marketing copy must use the computed numbers; never hard-coded targets.
- A local development dataset displays its actual size.

## Audit outputs

`pnpm audit:catalog` (→ `typeicon-import audit`) writes:

- `build/audit/catalog-audit.json`: machine-readable counts (Core bases and variants separately, brand logos),
  missing variants, duplicate groups, unsupported font assets, license gaps, remaining gap to 20,000 complete
  Core concepts.
- `docs/catalog-audit.md`: readable report of the same data.
