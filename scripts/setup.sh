#!/usr/bin/env bash
# One-command local setup (macOS/Linux, no Docker, no paid services).
# Requires: node >= 22, pnpm 10, uv, PostgreSQL 17 binaries (macOS: brew install uv postgresql@17).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
step() { printf "\n\033[1m==> %s\033[0m\n" "$*"; }

step "Checking prerequisites"
for c in node pnpm uv; do command -v "$c" >/dev/null || { echo "missing: $c"; exit 1; }; done

step "Python toolchain (uv, Python 3.12, pinned fontTools/pathops/uharfbuzz/OTS)"
uv python install 3.12 >/dev/null
uv sync --all-packages

step "Node packages"
pnpm install

step "Environment files"
if [ ! -f .env ]; then
  cp .env.example .env
  secret="$(openssl rand -base64 32 | tr -d '\n')"
  sed -i.bak "s|change-me-to-a-long-random-string|$secret|" .env && rm -f .env.bak
fi
[ -f apps/web/.env.local ] || cp .env apps/web/.env.local
set -a; source .env; set +a

step "PostgreSQL (local, .data/pg, port 54329)"
bash scripts/dev-db.sh start
(cd apps/web && pnpm db:migrate && DATABASE_URL="$TEST_DATABASE_URL" pnpm db:migrate)

step "Catalog: fetch pinned sources (integrity-checked), sanitize, convert outlines"
.venv/bin/python tools/core-authoring/export.py   # writes assets/core/core-icons.json (generated, not committed)
.venv/bin/typeicon-import build

step "Release: compile + validate every font family, package archives"
.venv/bin/typeicon-import release --version 0.3.0 --date 2026-09-30

step "Load catalog + release into PostgreSQL and storage"
.venv/bin/typeicon-import db-load --release 0.3.0 --overwrite-release
.venv/bin/typeicon-import db-load --database-url "$TEST_DATABASE_URL" --release 0.3.0

step "Catalog audit"
.venv/bin/typeicon-import audit --raster | head -20

step "Local test accounts (credentials written to .data/dev-credentials.json)"
(cd apps/web && npx tsx --conditions=react-server --tsconfig tsconfig.json scripts/seed-dev-users.ts)

step "Framework packages (React/Vue/SVG/webfont)"
node packages/scripts/generate.mjs --quiet

cat <<'MSG'

Done. Next:
  pnpm dev                 # website on http://localhost:3107
  pnpm worker              # background worker (subset/kit builds, imports, releases)
  pnpm test                # Python + web unit/integration tests
  pnpm test:e2e            # Playwright (needs dev server + worker binary)
MSG
