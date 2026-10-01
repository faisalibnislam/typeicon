# Decision log

Newest last. Each entry: decision, why, consequences.

1. **Monorepo: pnpm workspaces (TypeScript) + uv workspace (Python).** The web app and packages are
   TypeScript; font compilation and SVG geometry need fontTools, skia-pathops, uharfbuzz and OTS, which are
   Python. One `pyproject.toml` workspace (`tools/font-builder`, `tools/importers`, `apps/worker`) with pinned versions.
2. **Next.js 16 App Router, React 19, Tailwind v4, Radix primitives, Drizzle + node-postgres, Better Auth.**
   Current stable versions at the time of writing. Next 16 specifics: async `params`/`searchParams`, `proxy.ts` instead
   of middleware, async sitemap ids. No `cacheComponents`; catalog pages are dynamic and bounded.
3. **Local development without Docker.** The development machine had no Docker, so `scripts/dev-db.sh` runs
   Homebrew PostgreSQL 17 from `.data/pg`, and `STORAGE_DRIVER=fs` stores objects in `.data/storage`.
   `docker-compose.yml` (Postgres + MinIO + worker + web) is provided but has not been run.
4. **Community packs from upstream npm tarballs** (`@tabler/icons`, `@phosphor-icons/core`,
   `@material-symbols/svg-400`), pinned by SRI integrity. These are the upstream projects' own distributions,
   except Material Symbols, which uses the widely used marella packaging of Google's repository. That
   provenance chain is recorded.
5. **TypeIcon Core is original and small.** 70 concepts drawn with `tools/core-authoring` (60 → 66 counted
   after audit-driven redesigns; 4 rotation-derived). Community packs are not promoted into Core automatically:
   the rules require design QA, and promoting another project's artwork as "TypeIcon Core" is a brand and
   ownership decision for the owner.
6. **Style mapping for packs uses the TypeIcon axis with native labels.** Tabler Outline and Phosphor Regular
   are round-cap/round-join outlines, so they map to Rounded. Material Outlined maps to Line, Rounded to Rounded,
   and Outlined FILL 1 to Filled. Missing styles are unavailable, never substituted. Upstream files whose geometry
   is identical to another style (1,855 Material FILL 1 files) are not published as a separate style.
7. **Own SVG→outline converter** instead of picosvg: stroke expansion happens after transforming to font units
   (1200 UPM), because Skia's stroker tolerance is absolute. picosvg's quadratic approximation of arcs was about
   0.24 px off at 24 px.
8. **UPM 1200, ascent 1050, descent 150.** 24-grid units map to 50 font units exactly. Win metrics cover real
   glyph bounds to avoid clipping.
9. **One ligature lookup for the whole name set** (`liga` + `rlig`, DFLT + latn), promoted to Extension lookups
   above 1,500 rules. This gives true leftmost-longest matching (`arrow` / `arrow-right` / `arrow-right-circle`).
   Aliases point at the same glyph. Keywords must be at least 2 characters: a one-letter alias (`x`) replaced
   every "x" in text and was removed.
10. **Codepoints are integers in an append-only committed registry** (`assets/registry/codepoints.json`). Core
    uses Plane 15 with a permanent BMP mirror for the first 6,400 concepts; each pack uses Plane 16 in its own family.
11. **ASCII fallback letterforms are original** (monoline, in `fallback.py`), so the fonts carry no
    third-party text-font license.
12. **Subsets use fontTools subsetting** with an explicit glyph list and `layout_closure=False`. With closure on,
    keeping ASCII would retain every ligature output. Private custom icons are compiled with the same compiler.
    Every subset is re-validated, including a negative check that unselected keywords stay as text.
13. **Jobs in PostgreSQL** (`FOR UPDATE SKIP LOCKED`, heartbeats, stale recovery, exponential backoff) rather
    than an extra queue service. Each job runs in a separate process with rlimits and a timeout.
14. **Search in PostgreSQL** (weighted tsvector + pg_trgm + synonym expansion). At 150,675 designs, p95 is
    102 ms at concurrency 8 (docs/benchmarks.md), so no dedicated search engine is needed yet.
15. **Release immutability.** Versioned storage objects must be byte-identical on reload. A different build
    requires a new version.
16. **Core license left as a draft.** Public terms for original Core artwork are the owner's decision. The audit
    reports the gap, and archives label Core `LicenseRef-TypeIcon-Core-Draft`.
17. **Entitlements are capability data without prices.** `plans` hold build quotas, custom-icon limits and
    hosted-kit flags. Checkout stays hidden until a billing provider is configured.
18. **Pack font family names** use `TypeIcon <Pack> <Style>`. "Material" is Google's trademark, and the owner
    should confirm this naming with counsel (recorded in the manifest's `trademarkNote`).
19. **2026-09-30: Community packs removed; brand logos added; Core goal set to 20,000.** Owner decision.
    *Supersedes entries 4, 6 and 18 and the pack parts of entries 5 and 10.*
    - Tabler Icons, Phosphor Icons and Material Symbols are removed entirely: sources, fonts, CSS, packages and site
      pages. The catalog is now (1) **TypeIcon Core**, original hand-authored icons in Filled, Line and Rounded,
      and (2) **brand logos**. Pack artwork never counted toward the goal and is no longer shown or packaged.
    - Their codepoint assignments move to the `retired` section of `assets/registry/codepoints.json`. They stay
      there and are never reused.
    - **Brand logos** come from Simple Icons 16.33.0 (npm, pinned by SRI). The collection is CC0-1.0, but Simple
      Icons says that does not cover every logo, so per-logo licenses are recorded and logos under CC-BY-SA,
      non-commercial, GPL/AGPL, MPL or custom terms are quarantined (94 at import). Logos are trademarks of their
      owners; a disclaimer ships in `licenses/simple-icons/`. Model: style `brand` (native label "Logo"), family
      **TypeIcon Brands** (`TypeIconBrands-Regular`, CSS family class `typeicon-brands`), names prefixed `brand-`
      (`brand-github`, with the short name `github` also typed in the font), area `brands`, namespace
      `pack:brands` from U+100000. Brand logos **never** count toward the Core goal.
    - Site: search/filter area values are `all | core | brands`; the nav has **Brands** (`/icons?style=brand`) and
      **Packs** is renamed **Sources** (`/packs` still routes).
    - **Core goal: 20,000 complete Core concepts** (was 50,000). A complete concept is a base design or a designed
      variant, each with approved Filled, Line and Rounded. **Variants** are real named concepts built from a base
      plus a designed badge in the bottom-right corner with a 1.5 px shape-following gap (`file-plus`,
      `user-off`, `bell-lock`), from 23 badges; each category picks a modifier set (none / minimal / common /
      full) so only variants that make sense are drawn. Rotated directional siblings still do not count, and base
      and variant totals are always reported separately.
    - Authoring runs through `tools/core-authoring` (`AUTHORING.md`, `dsl.py` part roles, `modifiers.py`,
      `check.py`, `export.py`, `plan.json` with 42 categories and ~1,976 planned bases). AI/agent-drawn batches are
      published flagged for human design review.
    - Consequences: release **0.2.0** (4 families: core-filled, core-line, core-rounded, brands) replaces 0.1.0,
      which was deleted locally (never published). The "curate a community design into Core" idea is dropped.
20. **2026-10-01: Thin added as the fourth Core style.** Owner decision. Thin is Line's geometry (butt caps, miter
    joins, same corner radii) drawn with a 1 px stroke, half the weight of Line's 2 px. Every Core icon is still
    drawn once and exported in all styles. Thin is published wherever it differs from Line; icons made only of solid
    shapes have no distinct Thin and are not given one, because TypeIcon never publishes identical artwork as two
    styles.
    - Codes: style slug `thin`, font family `TypeIcon Thin` (PostScript `TypeIconThin-Regular`), CSS class
      `typeicon-thin`, React and Vue subpath `@typeicon/react/thin/<name>`, SVG directory `svg/thin/`, sprite
      `typeicon-core-thin.svg`, release files `TypeIconThin-Regular.*`. Brand logos stay a single style.
    - The Core goal still counts icons with Filled, Line and Rounded. Thin does not change the count, and Thin
      counts are reported only from published rows or `fonticonic-import audit`.
    - Consequences: the Thin family has fewer glyphs than the other Core families, so some Core keywords show as
      plain text when set in `TypeIcon Thin`. Docs and site copy say so.
