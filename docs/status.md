# Status and next tasks

Last updated 2026-09-30 (after the catalog change: community packs removed, brand logos added, Core goal set to
20,000; see `docs/decisions.md` entry 19). Nothing is committed, pushed, published or deployed.

## 1. Software implemented and tested

| Area | State | Evidence |
|---|---|---|
| SVG sanitizer (no DTD/entities/network, allow-list, routing to SVG-only) | Done | `tools/font-builder/tests/test_sanitize.py` |
| SVG → font outline (transforms, strokes at font scale, holes, clip paths, y-flip, viewBox/aspect) | Done | `test_outline.py` |
| OpenType compiler (OTF CFF + TTF glyf + WOFF2/WOFF, GSUB `liga`/`rlig` single lookup + Extension, cmap 4/12, names, visible .notdef, ASCII fallback, deterministic) | Done | `test_compiler.py`, OTS 9.2.0, HarfBuzz |
| Acceptance demo: `home search settings user arrow-right` in Filled, Line and Rounded, shared keywords, independent subset, SVG↔glyph raster match | Done | `test_core_acceptance.py` |
| Pinned importer for brand logos (Simple Icons 16.33.0), integrity, safe extraction, per-logo license quarantine, idempotent/dry-run builds, identical-geometry rejection | Done | `tools/importers/tests/*`, `/admin/imports` |
| Append-only codepoint registry (Plane 15 Core + BMP mirror, Plane 16 brands, kit range; removed packs kept under `retired`) | Done | `test_sources_registry.py` |
| Release builder (release 0.2.0: 4 families validated, Core Filled/Line/Rounded + Brands; archives, CSS, SVG, sprites, metadata, licenses, examples, checksums). Release 0.1.0 was deleted locally | Done | `test_release.py` |
| PostgreSQL schema + migrations, transactional loader, outbox, immutable releases | Done | `db/migrations`, loader, outbox processor |
| Website: home with live WOFF2 ligature demo, catalog (area filter all/core/brands), detail, categories/styles, Brands (`/icons?style=brand`) and Sources (`/packs`) nav, downloads, subset builder, collections, kits, docs (13 pages), licenses, changelog, admin | Done | Playwright tests incl. axe and mobile overflow checks |
| Search (ranking, synonyms, typos, facets, bounded pages) | Done | Vitest integration; benchmark p95 102 ms at 150,675 designs |
| Worker (Postgres queue, SKIP LOCKED, retries, stale recovery, rlimits; subset/kit/custom-icon/import/release jobs) | Done | `apps/worker/tests`, E2E subset + kits |
| Security: CSRF origin checks, ownership 404s, private build scope, malicious SVG, rate limits, admin rejection | Done | `tests/e2e/kits.spec.ts`, `subset-and-auth.spec.ts` |
| React/Vue/SVG/webfont/catalog packages, tree-shaking proof | Done | `node packages/scripts/verify.mjs` 72/72 |
| Core authoring pipeline (`tools/core-authoring`: DSL part roles, 23 badge modifiers, `plan.json` with 42 categories / ~1,976 planned bases, `check.py` quality gate + review sheets, `export.py`) | Done | Review sheets in `build/review/` |
| Figma plugin source | Built + unit-tested | Node tests; **never run inside Figma**; source filter still uses the removed `community` area |
| Docker Compose, Dockerfiles, CI workflow | Written | **Not run** (no Docker here; nothing pushed) |

## 2. Real catalog totals

See `docs/catalog-audit.md` (regenerate with `pnpm audit:catalog`); it is the source of truth and changes as new
Core waves land. **The goal is 20,000 complete Core concepts and it is not met.** On 2026-09-30 the catalog had
80 Core base designs (4 rotation-derived, not counted) and 1,054 Core variants (base + designed badge), every one in
Filled, Line and Rounded (Thin was added as a fourth style on 2026-10-01, published only where it differs from Line, and is not counted toward the goal), plus 3,369 published brand logos (94 quarantined for their per-logo license). Brand logos
never count toward the goal. Base and variant totals are always reported separately.

## 3. Verified vs unverified behaviour

Verified: OTS on every font; HarfBuzz shaping of every keyword and alias in every family; subsets re-shaped
independently; raster SVG↔glyph agreement; Chromium web-font ligatures (including a 50,000-glyph WOFF2).
**Unverified** (see `docs/compatibility-checklist.md`): Figma desktop and browser, Sketch, Illustrator, Affinity,
Keynote, Office, Safari, Firefox, macOS Font Book and Windows installation, the Figma plugin inside Figma,
Docker Compose, the production deployment and the CI workflow.

## 4. Owner decisions and external work required

1. **Core artwork production** to close the gap to 20,000 complete concepts (current gap in `docs/catalog-audit.md`):
   draw more bases and variants with `tools/core-authoring` (`AUTHORING.md`, `plan.json`) to `docs/design/core-grid.md`,
   or commission designers. This is the dominant dependency.
2. **Licenses:** choose terms for the TypeIcon code and for Core artwork (currently `LicenseRef-TypeIcon-Core-Draft`).
3. **Brand logos:** confirm the bootstrap approval of the Simple Icons source, the per-logo quarantine rules and the
   trademark disclaimer (`assets/sources/licenses/simple-icons/DISCLAIMER.md`) with counsel before public launch.
4. **Human design QA** of Core icons, especially AI/agent-drawn batches, which are published flagged for review
   (review sheets in `/admin/review` and `build/review/`).
5. Infrastructure accounts: managed Postgres, S3/R2 + CDN, worker host, domain, email provider (for verification and
   password reset), npm scope (`@typeicon`), Figma plugin publication. No purchases were made.
6. Pricing and billing provider (checkout stays hidden until configured).

## 5. Next engineering tasks

- Keep drawing Core waves from `plan.json`; re-run `check.py`, export, release (new version) and the audit after each.
- Email verification and password reset (Better Auth needs an email provider), plus optional OAuth providers.
- Figma plugin: replace the **Packs** source button (`area=community`) with **Brands** (`area=brands`).
- The audit report's closing section and "Missing variants" wording still mention 50,000 and Community Packs;
  update the text in `typeicon-import audit`.
- `package.json` (`release:build`) and `scripts/setup.sh` still pin release 0.1.0; bump them to the current release.
- Re-check the brand logos in release 0.2.0 whose recorded per-logo license is share-alike, non-commercial or
  no-derivatives (for example `brand-sass`, `brand-tauri`, `brand-ruby`) against the quarantine rule.
- Keyset pagination for deep catalog pages; facet caching for empty queries.
- Faster GSUB generation for 20k+ glyph fonts (otlLib builders instead of feaLib); per-family release parallelism tuning.
- A manual Figma / desktop test pass; record results in `docs/compatibility-checklist.md`.
- Run `docker compose up` and the CI workflow once Docker and a remote exist.

## Resume

```bash
bash scripts/dev-db.sh start && pnpm dev   # site on :3107
pnpm worker                               # jobs
pnpm test && pnpm test:e2e                # all tests
```

## Pending for release 0.4.0 (Thin style)

Once a release that contains the Thin font family is built and loaded, add `thin` to `FAMILIES` in
`apps/web/src/components/home/keyword-demo.tsx` and to the `@font-face` list in `apps/web/src/app/page.tsx`.
Release 0.3.0 has no Thin family, so adding them earlier would request font files that do not exist.
