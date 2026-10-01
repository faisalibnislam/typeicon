# Deployment and operations

Nothing has been deployed. This guide describes a production setup; it has not been exercised end to end.

## Topology

| Component | Recommended | Notes |
|---|---|---|
| Web (`apps/web`) | Vercel, or any Node 24 host (Docker image `apps/web/Dockerfile`, `output: "standalone"`) | Stateless. Never runs font builds. |
| Worker (`apps/worker`) | Long-running container (Fly.io, Railway, ECS/Fargate, a VM) with 2 vCPU / 3 GB | Must not be a short-lived serverless function: release builds take minutes and use a process pool. |
| PostgreSQL 17 | Managed (Neon, Supabase, RDS, Cloud SQL) with `pg_trgm` | Point-in-time recovery enabled. |
| Object storage | Cloudflare R2 or S3 behind a CDN | Public prefix `releases/`; private prefix `builds/private/`; kit embeds `kits/`. |
| Auth | Better Auth (in the web app, sessions in Postgres) | Set `BETTER_AUTH_SECRET`, `BETTER_AUTH_URL`. |

## Environment

See `.env.example`. Production additionally needs `STORAGE_DRIVER=s3`, `S3_*`, optionally
`S3_PUBLIC_BASE_URL` (CDN origin for `releases/`, which then redirects instead of streaming) and
`CDN_PURGE_URL` / `CDN_PURGE_TOKEN` for the outbox purge handler.

Storage bucket policy: only `releases/*` may be public-read. `builds/private/*` must stay private; the web
app streams those after an ownership check, or issues short-lived signed URLs.

## First deployment

```bash
# 1. Database
DATABASE_URL=… pnpm db:migrate
# 2. Build and publish the catalog + release from a machine with the repository (or run the worker's catalog-init)
typeicon-import build
typeicon-import release --version 0.1.0 --date 2026-09-30
DATABASE_URL=… STORAGE_DRIVER=s3 … typeicon-import db-load --release 0.1.0
# 3. First admin: create an account in the web UI, then
DATABASE_URL=… pnpm --filter @typeicon/web exec tsx --conditions=react-server scripts/grant-admin.ts you@example.com
# 4. Start the worker
typeicon-worker
```

## Releases

- Versions are immutable. `db-load` refuses to replace an existing release object whose bytes differ
  (`ReleaseImmutableError`). Bump the version instead. `--overwrite-release` exists only for unpublished local builds.
- Admins queue release builds from `/admin/releases`. The worker compiles every family, and any OTS, shaping,
  clipping or raster failure stops the release. After a successful build, approve and publish it.
- Retention: keep every published release's archives (they are referenced by kits pinned to that release).
  Build caches under `builds/` can be pruned by `last_used_at` (for example 90 days) because they are
  reproducible from the pinned inputs.

## Migrations and rollback

- Migrations live in `db/migrations` (drizzle-kit generated, reviewed, committed) and are applied with
  `pnpm db:migrate`, which also ensures `pg_trgm`.
- Write migrations to be backward compatible for one release (add columns and tables first, remove later) so the
  previous web build can keep running during a rollback.
- Rolling back the web app is a redeploy of the previous build. Rolling back a catalog change means
  re-running `db-load` from the previous commit's `build/catalog` (idempotent upserts), or restoring the database.

## Backup and restore

```bash
pg_dump --format=custom --no-owner "$DATABASE_URL" > typeicon-$(date +%F).dump    # nightly, plus PITR
pg_restore --clean --if-exists --no-owner -d "$DATABASE_URL" typeicon-YYYY-MM-DD.dump
```

The database can also be rebuilt from the repository: `assets/` + `assets/registry/codepoints.json` +
pinned sources reproduce the catalog. The codepoint registry is committed and append-only, so it is the one
file that must never be lost or rewritten (CI runs `typeicon-import check-registry --against <previous>`).
Object storage: enable versioning on the bucket; release objects are immutable by policy.

## Worker limits and security

- Each job runs in a separate process with `RLIMIT_CPU`, `RLIMIT_AS` (Linux) and a wall-clock timeout
  (`WORKER_JOB_TIMEOUT_SECONDS`, admin jobs `WORKER_RELEASE_TIMEOUT_SECONDS` / `WORKER_IMPORT_TIMEOUT_SECONDS`).
  The container adds hard memory and CPU caps.
- Custom SVG uploads are bounded (64 KB) at the web tier and parsed only by the worker's sanitizer (no DTDs,
  entities, network or external resources; allow-listed elements). Archive extraction is traversal-safe with size limits.
- Build caches are keyed by `scope`, so private assets can never be served from another user's cache entry.

## Metrics to watch (no personal data collected)

| Metric | Source |
|---|---|
| Search latency p50/p95 | `search_metrics` (query length and timing only, never the query text); shown in `/admin` |
| Queue depth, failed jobs | `jobs` grouped by status; `/admin/jobs` |
| Download throughput | `audit_events` with action `download` (no IP, no user id) |
| Catalog completeness | `catalog_stats`, `build/audit/catalog-audit.json` |
| Import failures | `catalog_import` jobs and their reports in `/admin/imports` |
| Outbox backlog | `outbox` rows with `processed_at IS NULL` |
