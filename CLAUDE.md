# TypeIcon: notes for coding agents

Read `README.md`, `docs/status.md` (current state and next tasks) and `docs/decisions.md` first.

## Non-negotiables

- Desktop fonts use real OpenType GSUB ligatures. Validate every font change with
  `.venv/bin/pytest tools/font-builder/tests` (OTS + HarfBuzz shaping + raster comparisons).
- Counts shown anywhere must come from published rows or `typeicon-import audit`. Never inflate them with
  aliases, brand logos, rotations or duplicates. Report Core base designs and variants separately. The Core goal
  (20,000 complete concepts, see `docs/policies/catalog-counts.md`) is **not met**.
- Never substitute a missing style. Never label identical geometry as two styles.
- `assets/registry/codepoints.json` is append-only. Never edit or reuse an assignment, including the `retired`
  section (codepoints of the removed Tabler, Phosphor and Material Symbols packs).
- The catalog is TypeIcon Core (original, Filled + Line + Rounded + Thin, with Thin published only where it differs from Line) plus brand logos from Simple Icons
  (`brand-` names, style `brand`, family TypeIcon Brands). Do not re-add third-party icon packs without an owner
  decision (`docs/decisions.md`). Never copy or trace another set's geometry into Core.
- Brand logos keep their recorded per-logo license and are trademarks of their owners. Never import Font Awesome
  Pro assets or unverified Iconify sets.
- Core authoring: follow `tools/core-authoring/AUTHORING.md` and pass `check.py` (quality gate + review sheets).
  AI- or agent-drawn batches are published flagged for human design review.
- Published releases are immutable: bump the version rather than overwrite (`db-load` enforces this).
- Font builds, imports and releases run in the worker, never inside a web request.

## Environment

- Local Postgres: `bash scripts/dev-db.sh start` (port 54329; DBs `typeicon`, `typeicon_test`, `typeicon_bench`).
- Web dev server: port **3107** (3000 is used by another project). `.claude/launch.json` has a `web` config.
- Env: `.env` (repo root) and `apps/web/.env.local`. Load with `set -a && source .env && set +a`.
- Next.js 16 has breaking changes. Read `apps/web/node_modules/next/dist/docs/` before using unfamiliar APIs
  (async params, `proxy.ts`, async sitemap ids).
- Scripts that import `server-only` modules need `npx tsx --conditions=react-server --tsconfig tsconfig.json …`.
- Test accounts: `apps/web/scripts/seed-dev-users.ts` writes credentials to `.data/dev-credentials.json`.
  Never print them.

## Tests

`pnpm test` (pytest + Vitest), `pnpm test:e2e` (Playwright; dev server must be running), `pnpm packages:verify`.
