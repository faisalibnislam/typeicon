#!/usr/bin/env bash
# Integrate new Core designs: export SVGs -> catalog build -> local release -> load dev + test DBs -> audit.
# Usage: scripts/integrate-core.sh <release-version>   (e.g. 0.3.0; a new version per integration, releases are immutable)
set -euo pipefail
cd "$(dirname "$0")/.."
VERSION="${1:?usage: scripts/integrate-core.sh <release-version>}"
set -a; source apps/web/.env.local; set +a

.venv/bin/python tools/core-authoring/export.py
.venv/bin/typeicon-import build
.venv/bin/typeicon-import release --version "$VERSION" --date "$(date +%F)"
.venv/bin/typeicon-import db-load --release "$VERSION" --database-url "$DATABASE_URL"
.venv/bin/typeicon-import db-load --release "$VERSION" --database-url "$TEST_DATABASE_URL"
.venv/bin/typeicon-import audit --raster
node packages/scripts/generate.mjs --quiet
