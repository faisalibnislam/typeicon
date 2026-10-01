# Benchmarks

Measured 2026-09-30 on one development machine. These are single-run measurements, not guarantees.
Raw results: `build/bench/search-latency.json`, `build/bench/font-scaling.json`, `build/bench/browser-font-load.json`.

**Environment:** Apple M5 Pro (18 cores), macOS 27, Node 24.21, PostgreSQL 17 (Homebrew, local, default
configuration), Python 3.12, fontTools 4.66.1, uharfbuzz 0.56.2, OTS 9.2.0, Chromium via Playwright 1.63.
The search benchmark ran while the font benchmark occupied one CPU core, so its numbers are slightly pessimistic.

## Search at target scale

Dataset: separate database `typeicon_bench` containing the real catalog plus 140,000 synthetic designs
(`scripts/bench-seed.sql`, refuses to run outside a `*_bench` database) → **150,675 designs, 301,234 variants**.
Synthetic rows never exist in the public database, so they cannot reach public counts.

Workload (`apps/web/scripts/bench-search.ts`): 600 requests at concurrency 8, each calling the production
`searchIcons()`: the page query, the count, and five facet queries (styles, packs, licenses, categories, areas).
The mix was 30% exact names, 20% single words, 15% three-letter prefixes, 10% two-word queries, 10% typos,
10% filtered browsing without a query, and 5% deep pages (page 20–50).

| Query kind | n | p50 ms | p95 ms | max ms |
|---|---:|---:|---:|---:|
| exact name | 180 | 43.9 | 55.8 | 62.4 |
| single word | 120 | 21.0 | 30.4 | 35.3 |
| prefix | 90 | 22.9 | 37.9 | 50.5 |
| multi-word | 60 | 17.4 | 27.1 | 29.8 |
| typo | 60 | 16.9 | 30.1 | 33.6 |
| filtered browse | 60 | 66.4 | 74.7 | 76.5 |
| deep page (OFFSET) | 30 | 135.5 | 176.9 | 207.5 |
| **overall** | **600** | **26.1** | **102.2** | **207.5** |

Throughput: 210 searches/s. **The p95 target of < 300 ms is met** for this workload.

Bottlenecks and next steps:
- Deep pages use `OFFSET` and are the slowest class. Switch to keyset pagination on `(area <> 'core', local_name, name)` if deep browsing becomes common.
- Every search runs 7 queries, and facets dominate filtered browsing. Cache facet counts for empty queries if needed.
- Real 24-hour latency is recorded in `search_metrics` and shown in `/admin`. Query text is never stored.

## Font scaling tiers

`tools/font-builder/bench/font_scaling.py` compiles one style font per tier with real outlines from the
catalog (cycled to reach the tier size) and 2 keywords per glyph (like pack fonts).

| Glyphs | Keywords | Compile (s) | OTF | TTF | WOFF2 | GSUB | OTS | HarfBuzz load | Shaping correct | Shape 200 keywords |
|---:|---:|---:|---:|---:|---:|---|---|---:|---|---:|
| 5,000 | 10,000 | 10.8 | 1.2 MB | 1.2 MB | 371 KB | 1 Extension lookup, 4 subtables | pass (all formats) | 1.4 ms | yes | 9.6 ms |
| 20,000 | 40,000 | 147.5 | 7.8 MB | 7.2 MB | 955 KB | 1 Extension lookup, 17 subtables | pass | 1.4 ms | yes | 36.9 ms |
| 50,000 | 100,000 | 958.2 | 19.5 MB | 18.1 MB | 1.18 MB* | 1 Extension lookup, 43 subtables | pass | 3.6 ms | yes | 91.6 ms |

\* The WOFF2 figure is optimistic: the tier reuses about 10,000 distinct outlines, which Brotli compresses well.
50,000 unique outlines would produce a larger WOFF2. The OTF and TTF sizes are representative.

**Chromium** (`build/bench/browser-font-load.json`) loaded each WOFF2 through the `FontFace` API and rendered
keywords with `liga`. Load time was 10 ms (5k), 31 ms (20k) and **69 ms (50k)**. Canonical keywords and aliases
at the start, middle and end of the name set rendered as one 1-em icon; an unknown keyword rendered as text.

Conclusions:
- One 50,000-icon font per style is **technically valid**: under the 65,535 glyph limit, no GSUB offset overflow
  (Extension lookups), OTS-clean, and shaped correctly by HarfBuzz and Chromium.
- **Compile time is superlinear** (4× glyphs → 13.6× time). A full three-style release at 50k concepts would take
  roughly 16 minutes per format per family in one process. The release builder already compiles families in
  parallel. Before promising that scale, profile feaLib and ligature subtable building and consider generating
  GSUB directly with `otlLib` builders.
- Desktop OTF/TTF files of about 19 MB are larger than many design tools expect. **Untested** in Figma, Sketch,
  Illustrator and Office at this size. Keep split packs (`MAX_GLYPHS_PER_FONT`, "Part N" families) and
  category/custom fonts available, and test desktop apps before choosing one-file-per-style for the full catalog.
- Current release families (at most 5,165 glyphs) sit comfortably in the first tier.
